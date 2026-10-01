use sage::state::{
    AtlasBalance, Character, CharacterAssetCounts, CharacterModifier, CharacterModifierOwned,
    CharacterModifierSized, CharacterModifiersOwned, CharacterModifiersSized, CharacterOwned,
    CharacterSized, CharacterSync, CharacterSyncOwned, CharacterSyncSized, CheckInStreakInfo, Game,
    GameSized, Name, PilotXpBudget, ResearchNode, ResearchNodeId, ResearchNodeOwned,
    ResearchNodeSized, ResearchTreeDefinitions, ResearchTreeDefinitionsOwned,
    ResearchTreeDefinitionsSized, XpInfo, MAX_NAME_LENGTH,
};
use star_frame::client::DeserializeAccount;
use star_frame::prelude::*;
use star_frame::unsize::FromOwned;
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::mem::{align_of, offset_of, size_of};
use std::path::PathBuf;

fn encode_owned<T: FromOwned + ?Sized>(owned: T::Owned) -> Vec<u8> {
    let mut bytes = vec![0; T::byte_size(&owned)];
    let mut remaining = bytes.as_mut_slice();
    T::from_owned(owned, &mut remaining).expect("serialize exact old-layout value");
    assert!(remaining.is_empty());
    bytes
}

fn character_owned() -> CharacterOwned {
    CharacterOwned {
        version: 0,
        player_profile: KeyFor::new(Pubkey::default()),
        game_id: KeyFor::new(Pubkey::default()),
        bump: 0,
        check_in_info: CheckInStreakInfo::default(),
        xp_info: XpInfo::default(),
        atlas: AtlasBalance::new(0),
        counts: CharacterAssetCounts::default(),
        pilot_xp_budget: PilotXpBudget::default(),
        character_modifiers: CharacterModifiersOwned::default(),
    }
}

fn sync_owned() -> CharacterSyncOwned {
    CharacterSyncOwned {
        version: 0,
        character: KeyFor::<Character>::new(Pubkey::default()),
        game_id: KeyFor::<Game>::new(Pubkey::default()),
        research_seq_id: 0,
        unlocked_nodes_len: 0,
        next_node_index: 0,
        next_node_repeat: 0,
        bump: 0,
        modifiers: CharacterModifierOwned::default(),
    }
}

fn one_node_tree() -> ResearchTreeDefinitionsOwned {
    let node = ResearchNodeOwned {
        id: ResearchNodeId::from(1),
        name: Name::from([0; MAX_NAME_LENGTH]),
        atlas_cost: 0,
        max_level: 1,
        cost_growth_bps: 0,
        cargo_cost: BTreeMap::new(),
        required_tags: BTreeSet::new(),
        xp_cost: BTreeMap::new(),
        modifier: CharacterModifierOwned::default(),
    };
    ResearchTreeDefinitionsOwned {
        seq_id: 0,
        nodes: BTreeMap::from([(node.id, node)]),
    }
}

#[test]
fn emits_exact_base_old_layout_witnesses() {
    let fixture_path = std::env::var("TARGETING_OLD_GAME_FIXTURE").expect(
        "TARGETING_OLD_GAME_FIXTURE must point to bytes extracted from the base Git object",
    );
    let output_dir = PathBuf::from(
        std::env::var("TARGETING_PROOF_OUTPUT_DIR")
            .expect("TARGETING_PROOF_OUTPUT_DIR must be provided"),
    );
    fs::create_dir_all(&output_dir).expect("create proof output directory");

    let game_bytes = fs::read(&fixture_path).expect("read exact old Game bytes");
    let game = Game::deserialize_account(&game_bytes).expect("base decoder must decode base bytes");
    let node_ids = game
        .research_tree_definitions
        .nodes
        .keys()
        .map(ToString::to_string)
        .collect::<Vec<_>>();

    let modifier = CharacterModifierOwned::default();
    let character = character_owned();
    let sync = sync_owned();
    let tree = one_node_tree();
    let node = tree.nodes.values().next().expect("one-node tree");
    let node_byte_size = <ResearchNode as FromOwned>::byte_size(node);
    let tree_byte_size = <ResearchTreeDefinitions as FromOwned>::byte_size(&tree);

    let old_values = [
        (
            "old-character-modifier.bin",
            encode_owned::<CharacterModifier>(modifier),
        ),
        ("old-character.bin", encode_owned::<Character>(character)),
        (
            "old-character-sync.bin",
            encode_owned::<CharacterSync>(sync),
        ),
        (
            "old-research-tree-one-node.bin",
            encode_owned::<ResearchTreeDefinitions>(tree),
        ),
    ];
    for (name, bytes) in old_values {
        fs::write(output_dir.join(name), bytes).expect("write exact old-layout witness");
    }

    println!("TARGETING_PROOF_BASE_NODE_COUNT={}", node_ids.len());
    println!("TARGETING_PROOF_BASE_NODE_IDS={}", node_ids.join(","));
    println!(
        "TARGETING_PROOF_BASE_LAYOUT=character_modifier_sized:{},character_sized:{},character_modifiers_sized:{},character_sync_sized:{},research_node_sized:{},research_tree_definitions_sized:{},game_sized:{},scan_cool_down_offset:{},character_modifier_bytes:{},character_bytes:{},character_sync_bytes:{},research_node_bytes:{},research_tree_one_node_bytes:{}",
        size_of::<CharacterModifierSized>(),
        size_of::<CharacterSized>(),
        size_of::<CharacterModifiersSized>(),
        size_of::<CharacterSyncSized>(),
        size_of::<ResearchNodeSized>(),
        size_of::<ResearchTreeDefinitionsSized>(),
        size_of::<GameSized>(),
        offset_of!(CharacterModifierSized, scan_cool_down_modifier),
        <CharacterModifier as FromOwned>::byte_size(&CharacterModifierOwned::default()),
        <Character as FromOwned>::byte_size(&character_owned()),
        <CharacterSync as FromOwned>::byte_size(&sync_owned()),
        node_byte_size,
        tree_byte_size,
    );
    println!(
        "TARGETING_PROOF_BASE_ALIGNMENTS=character_modifier_sized:{},character_sized:{},character_sync_sized:{},research_node_sized:{},game_sized:{}",
        align_of::<CharacterModifierSized>(),
        align_of::<CharacterSized>(),
        align_of::<CharacterSyncSized>(),
        align_of::<ResearchNodeSized>(),
        align_of::<GameSized>(),
    );
}
