from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON_DIR = ROOT / "data" / "canon"


def load_json(name: str):
    path = CANON_DIR / name
    if not path.exists():
        raise AssertionError(f"Missing required Canon registry: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"Missing required authority document: {relative_path}")
    return path.read_text(encoding="utf-8")


def main():
    master = load_json("master_asset_registry_2026-08-08.json")
    overrides = load_json("post_canon_overrides.json")
    source = load_json("source_registry_v1.6.1.json")

    # Registry structural integrity.
    assets = master.get("assets", [])
    require(assets, "Master Asset Registry must not be empty")
    asset_ids = [a["id"] for a in assets]
    require(len(asset_ids) == len(set(asset_ids)), "Master Asset Registry contains duplicate asset IDs")

    base = source.get("base_world_canon", {})
    require(base.get("status") == "BASE_WORLD_CANON", "source registry must model V1.6.1 as BASE_WORLD_CANON")
    require("V1.6.1" in base.get("name", ""), "base world canon must be V1.6.1")

    policy = source.get("post_canon_override_policy", {})
    require(policy.get("registry") == "data/canon/post_canon_overrides.json", "source registry override path mismatch")
    active_ids = set(policy.get("active_overrides", []))
    override_records = overrides.get("overrides", [])
    override_ids = {o["id"] for o in override_records if o.get("status") == "ACTIVE_LOCKED_OVERRIDE"}
    require(active_ids == override_ids, f"Active override mismatch: source={sorted(active_ids)} override_registry={sorted(override_ids)}")

    require("OVR-BEAST-001" in active_ids, "OVR-BEAST-001 must remain active until explicitly superseded")
    beast = next(o for o in override_records if o["id"] == "OVR-BEAST-001")
    current = beast["current"]

    # Six-beast canonical invariants from the post-V1.6.1 locked asset workflow.
    require(set(current) == {"白泽", "玄雷夔", "毕方", "夫诸", "九天玄应龙", "太玄玄武"}, "Beast override must contain exactly six high-tier beasts")

    require(current["白泽"]["normal"] == {"shoulder_height_m": 90, "body_length_m": 150, "horn_crown_span_m": 120}, "白泽 normal dimensions drifted")
    require(current["玄雷夔"]["normal"] == {"max_body_height_m": 110, "body_length_m": 170}, "玄雷夔 normal dimensions drifted")
    require("one_leg" in current["玄雷夔"]["hard_visual"], "玄雷夔 must remain one-legged")
    require("no_horns" in current["玄雷夔"]["hard_visual"], "玄雷夔 must remain hornless")
    require(current["毕方"]["normal"] == {"standing_height_m": 120, "wingspan_m": 300}, "毕方 normal dimensions drifted")
    require("one_leg" in current["毕方"]["hard_visual"], "毕方 must remain one-legged")
    require(current["夫诸"]["normal"] == {"shoulder_height_m": 85, "body_length_m": 150, "four_horn_span_m": 130}, "夫诸 normal dimensions drifted")
    require("four_independent_horn_roots" in current["夫诸"]["hard_visual"], "夫诸 must retain four independent horn roots")

    dragon = current["九天玄应龙"]
    require(dragon["normal"] == {"body_length_m": 1200, "airspace_envelope_m": 1800}, "九天玄应龙 normal dimensions drifted")
    require("wingless_oriental_ancestral_dragon" in dragon["hard_visual"], "九天玄应龙 must remain wingless")
    require("wingspan_m" not in dragon["normal"], "Deprecated dragon wingspan field reintroduced")

    xuanwu = current["太玄玄武"]
    require(xuanwu["normal"] == {"shell_max_diameter_m": 850, "snake_length_m": 1400}, "太玄玄武 normal dimensions drifted")
    require("tortoise_snake_dual_spirit" in xuanwu["hard_visual"], "太玄玄武 must remain tortoise-snake dual spirit")
    require("snake_must_not_become_dragon" in xuanwu["hard_visual"], "玄武 snake must not dragonize")

    placements = beast["f2_locked_placements_m"]
    expected_placements = {
        "白泽": [3220, 7800, 1420],
        "玄雷夔": [-1780, 7550, 1220],
        "毕方": [3050, 6280, 1220],
        "夫诸": [2430, 8730, 1450],
        "九天玄应龙": [350, 9300, 2050],
        "太玄玄武": [950, 8050, 1010],
    }
    require(placements == expected_placements, "F2 LOCKED placements drifted")

    # Source-stack facts must preserve F2/F3 status accurately.
    controls = {c["id"]: c for c in source.get("control_stack", [])}
    require(controls["F2"].get("status") == "LOCKED_USER_CONFIRMED", "F2 must remain LOCKED_USER_CONFIRMED")
    require(controls["F2"].get("override_id") == "OVR-BEAST-001", "F2 must point to OVR-BEAST-001")
    require(controls["F3"].get("source_status") == "REVIEW", "F3 standalone source status must remain REVIEW unless separate lock evidence is added")
    require(controls["F3"].get("downstream_status") == "PASSED_BY_G1", "F3 downstream G1 pass evidence must be preserved")
    require(controls["G1"].get("status") == "LOCKED", "G1 must remain LOCKED")

    # Master registry binary evidence states must not overclaim recoverability.
    asset_map = {a["id"]: a for a in assets}
    require(asset_map["BIN-F1-OBJ"]["file_library"] == "DIRECT_FOUND", "F1 OBJ evidence state changed")
    require(asset_map["BIN-F1-GLB"]["file_library"] == "REFERENCED_ONLY", "F1 GLB must not be reported direct-found without evidence")
    require(asset_map["F2-MASTER-GLB"]["file_library"] == "MANIFEST_VERIFIED", "F2 master GLB evidence state must remain MANIFEST_VERIFIED unless direct recovery is recorded")
    require(asset_map["F3-MASTER-GLB"]["file_library"] == "REFERENCED_ONLY", "F3 master GLB evidence state must remain REFERENCED_ONLY unless stronger evidence is recorded")

    required_docs = [
        "docs/canon/AUTHORITY_STACK_V1.6.1.md",
        "docs/canon/MASTER_ASSET_REGISTRY_2026-08-08.md",
        "docs/canon/POST_CANON_LOCKED_OVERRIDES.md",
        "docs/canon/ASSET_CLASSIFICATION_2026-08-08.md",
        "CODEX.md",
        "README.md",
    ]
    for relative_path in required_docs:
        read_text(relative_path)

    # Critical entry documents must all expose the same authority model.
    entry_docs = {
        "README.md": read_text("README.md"),
        "CODEX.md": read_text("CODEX.md"),
        "docs/canon/AUTHORITY_STACK_V1.6.1.md": read_text("docs/canon/AUTHORITY_STACK_V1.6.1.md"),
        "docs/canon/ASSET_CLASSIFICATION_2026-08-08.md": read_text("docs/canon/ASSET_CLASSIFICATION_2026-08-08.md"),
    }
    for name, text in entry_docs.items():
        require("BASE_WORLD_CANON" in text, f"{name} must explicitly state BASE_WORLD_CANON")
        require("OVR-BEAST-001" in text, f"{name} must explicitly expose OVR-BEAST-001")

    # Prevent regression to the earlier oversimplified authority wording.
    stale_phrases = [
        "V1.6.1 is the sole current Canon",
        "The sole current Canon is",
        "V1.6.1 是唯一现行 Canon",
        "SOLE CURRENT CANON",
    ]
    for name, text in entry_docs.items():
        lowered = text.casefold()
        for phrase in stale_phrases:
            require(phrase.casefold() not in lowered, f"{name} reintroduced stale authority phrase: {phrase}")

    print("CANON_REGISTRY_VALIDATION: PASS")
    print(f"assets={len(assets)} active_overrides={sorted(active_ids)}")
    print("authority_docs=CONSISTENT base=V1.6.1 overlay=OVR-BEAST-001")
    print("beast_override=OVR-BEAST-001 F2=LOCKED F3=REVIEW/PASSED_BY_G1 G1=LOCKED")


if __name__ == "__main__":
    main()
