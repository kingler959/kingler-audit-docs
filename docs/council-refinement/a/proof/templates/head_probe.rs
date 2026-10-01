use sage::state::{
    AtlasBalance, Character, CharacterAssetCounts, CharacterModifier, CharacterModifierOwned,
    CharacterModifierSized, CharacterModifiersOwned, CharacterOwned, CharacterSized, CharacterSync,
    CharacterSyncOwned, CharacterSyncSized, CheckInStreakInfo, Game, GameSized, Name,
    PilotXpBudget, ResearchNode, ResearchNodeId, ResearchNodeOwned, ResearchNodeSized,
    ResearchTreeDefinitions, ResearchTreeDefinitionsOwned, ResearchTreeDefinitionsSized, XpInfo,
    MAX_NAME_LENGTH,
};
use star_frame::client::DeserializeAccount;
use star_frame::prelude::*;
use star_frame::unsize::{FromOwned, UnsizedType};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::mem::{align_of, offset_of, size_of};
use std::path::PathBuf;

fn read_witness(dir: &PathBuf, name: &str) -> Vec<u8> {
    fs::read(dir.join(name)).unwrap_or_else(|error| panic!("read {name}: {error}"))
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
fn records_known_unsupported_old_layout_result() {
    // This is a characterization witness, NOT a safety regression. A passing test means the
    // explicitly unsupported old-layout outcomes still match the pinned assessment. If runtime
    // refusal or migration is later implemented, this expectation must be deliberately replaced.
    let fixture_path = std::env::var("TARGETING_OLD_GAME_FIXTURE").expect(
        "TARGETING_OLD_GAME_FIXTURE must point to bytes extracted from the base Git object",
    );
    let output_dir = PathBuf::from(
        std::env::var("TARGETING_PROOF_OUTPUT_DIR")
            .expect("TARGETING_PROOF_OUTPUT_DIR must be provided"),
    );
    let expected_base_node_count: usize = std::env::var("TARGETING_EXPECTED_BASE_NODE_COUNT")
        .expect("TARGETING_EXPECTED_BASE_NODE_COUNT must be provided")
        .parse()
        .expect("base node count must be numeric");

    let old_modifier = read_witness(&output_dir, "old-character-modifier.bin");
    let old_character = read_witness(&output_dir, "old-character.bin");
    let old_sync = read_witness(&output_dir, "old-character-sync.bin");
    let old_tree = read_witness(&output_dir, "old-research-tree-one-node.bin");
    let old_game = fs::read(&fixture_path).expect("read exact old Game bytes");

    let modifier_error = format!(
        "{:?}",
        CharacterModifier::owned(&old_modifier)
            .expect_err("old CharacterModifier must reject under the head layout")
    );
    let character_error = format!(
        "{:?}",
        Character::owned(&old_character)
            .expect_err("old Character must reject under the head layout")
    );
    let sync_error = format!(
        "{:?}",
        CharacterSync::owned(&old_sync)
            .expect_err("old CharacterSync must reject under the head layout")
    );

    let tree = ResearchTreeDefinitions::owned(&old_tree)
        .expect("known unsupported result: old one-node tree is currently accepted");
    assert_eq!(
        tree.nodes.len(),
        0,
        "known unsupported result changed: old one-node tree no longer decodes as empty"
    );

    let game = Game::deserialize_account(&old_game)
        .expect("known unsupported result: old Game is currently accepted by the Rust decoder");
    assert_ne!(expected_base_node_count, 0);
    assert_eq!(
        game.research_tree_definitions.nodes.len(),
        0,
        "known unsupported result changed: old Game no longer decodes as an empty tree"
    );

    assert!(
        modifier_error.contains("RawSliceAdvance"),
        "{modifier_error}"
    );
    assert!(
        character_error.contains("RawSliceAdvance"),
        "{character_error}"
    );
    assert!(sync_error.contains("RawSliceAdvance"), "{sync_error}");

    println!(
        "TARGETING_PROOF_HEAD_RESULTS=character_modifier:reject_raw_slice,character:reject_raw_slice,character_sync:reject_raw_slice,research_tree_one_node:accept_zero_nodes,game_{}_nodes:accept_zero_nodes",
        expected_base_node_count
    );
    println!(
        "TARGETING_PROOF_HEAD_LAYOUT=character_modifier_sized:{},character_sized:{},character_sync_sized:{},research_node_sized:{},research_tree_definitions_sized:{},game_sized:{},scan_cool_down_offset:{},hit_chance_offset:{},character_modifier_bytes:{},character_bytes:{},character_sync_bytes:{},research_node_bytes:{},research_tree_one_node_bytes:{}",
        size_of::<CharacterModifierSized>(),
        size_of::<CharacterSized>(),
        size_of::<CharacterSyncSized>(),
        size_of::<ResearchNodeSized>(),
        size_of::<ResearchTreeDefinitionsSized>(),
        size_of::<GameSized>(),
        offset_of!(CharacterModifierSized, scan_cool_down_modifier),
        offset_of!(CharacterModifierSized, hit_chance_modifier),
        <CharacterModifier as FromOwned>::byte_size(&CharacterModifierOwned::default()),
        <Character as FromOwned>::byte_size(&character_owned()),
        <CharacterSync as FromOwned>::byte_size(&sync_owned()),
        <ResearchNode as FromOwned>::byte_size(
            one_node_tree().nodes.values().next().expect("one node"),
        ),
        <ResearchTreeDefinitions as FromOwned>::byte_size(&one_node_tree()),
    );
    println!(
        "TARGETING_PROOF_HEAD_ALIGNMENTS=character_modifier_sized:{},character_sized:{},character_sync_sized:{},research_node_sized:{},game_sized:{}",
        align_of::<CharacterModifierSized>(),
        align_of::<CharacterSized>(),
        align_of::<CharacterSyncSized>(),
        align_of::<ResearchNodeSized>(),
        align_of::<GameSized>(),
    );
}
