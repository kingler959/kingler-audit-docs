import { readFileSync, writeFileSync } from "fs";
import { describe, expect, it } from "vitest";
import { getGameDecoder } from "../src/generated/accounts/game";

describe("Targeting known unsupported old Game layout", () => {
  it("records the generated TypeScript decoder outcome for exact base bytes", () => {
    // This is a compatibility characterization, not proof that the runtime safely refuses
    // every old layout. Rust currently accepts the same Game bytes and sees zero research nodes.
    const fixturePath = process.env.TARGETING_OLD_GAME_FIXTURE;
    if (!fixturePath) {
      throw new Error("TARGETING_OLD_GAME_FIXTURE is required");
    }
    const resultPath = process.env.TARGETING_TS_RESULT;
    if (!resultPath) {
      throw new Error("TARGETING_TS_RESULT is required");
    }

    const bytes = readFileSync(fixturePath);
    let outcome:
      | { status: "decoded"; nodeCount: number }
      | { status: "error"; message: string };
    try {
      const game = getGameDecoder().decode(bytes);
      outcome = {
        status: "decoded",
        nodeCount: game.researchTreeDefinitions.nodes.unsizedList.length,
      };
    } catch (error) {
      outcome = {
        status: "error",
        message: error instanceof Error ? error.message : String(error),
      };
    }

    console.log(`TARGETING_PROOF_TS=${JSON.stringify(outcome)}`);
    writeFileSync(resultPath, `${JSON.stringify(outcome, null, 2)}\n`);
    expect(outcome.status).toBe("error");
    if (outcome.status === "error") {
      expect(outcome.message).toMatch(/Codec \[u16\] expected 2 bytes, got 1/);
    }
  });
});
