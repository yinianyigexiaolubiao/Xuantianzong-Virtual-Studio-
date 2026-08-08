from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "project" / "master_project_registry_2026-08-08.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(REGISTRY_PATH.exists(), f"Missing project registry: {REGISTRY_PATH.relative_to(ROOT)}")
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    required = set(data.get("required_modules", []))
    expected = {
        "CANON_AND_WORLD",
        "DIGITAL_TWIN",
        "VISUAL_ASSETS",
        "PROMO_FILM_AND_DJI",
        "PHONE_CONTENT",
        "XUANYUAN_LIANQI",
        "DIGITAL_XUANTIANZONG",
        "BEASTS_AND_SACRED_TREES",
        "HISTORICAL_ARCHIVE",
    }
    require(required == expected, f"Required project modules drifted: {sorted(required)}")

    modules = data.get("modules", [])
    module_ids = [m.get("id") for m in modules]
    require(len(module_ids) == len(set(module_ids)), "Duplicate project module IDs")
    require(set(module_ids) == expected, f"Project module coverage mismatch: {sorted(module_ids)}")

    valid_sync_states = set(data.get("sync_states", {}))
    require(valid_sync_states, "sync_states must not be empty")

    asset_ids: list[str] = []
    by_id: dict[str, dict] = {}
    for module in modules:
        assets = module.get("assets", [])
        require(assets, f"Module {module['id']} has no registered assets")
        for asset in assets:
            aid = asset.get("id")
            require(aid, f"Asset without ID in module {module['id']}")
            require(asset.get("title"), f"Asset {aid} missing title")
            require(asset.get("source"), f"Asset {aid} missing source")
            require(asset.get("class"), f"Asset {aid} missing class")
            state = asset.get("sync_state")
            require(state in valid_sync_states, f"Asset {aid} has unknown sync_state={state}")
            if state == "GITHUB_MIRRORED":
                require(asset.get("github_path") or asset.get("github_ref"), f"Mirrored asset {aid} missing GitHub path/ref")
            if state in {"FILE_LIBRARY_ONLY_BINARY", "FILE_LIBRARY_ONLY_TEXT"}:
                require(not asset.get("github_path"), f"File-Library-only asset {aid} must not pretend to have a GitHub mirror path")
            asset_ids.append(aid)
            by_id[aid] = asset

    require(len(asset_ids) == len(set(asset_ids)), "Duplicate asset IDs in project registry")

    # Anchor assets from each previously separate project branch.
    anchors = {
        "CW-V161-DOCX",
        "DT-V01-BLEND",
        "VA-STRATEGIC-V11",
        "PF-CURRENT-BRIEF",
        "PC-SPIRIT-STONE-INTRO",
        "XLQ-TRUE-NO-NOTE",
        "XLQ-PDF-TRUEBOOK",
        "DX-STATUS-20260804",
        "BST-F2",
        "HA-V10",
    }
    require(anchors.issubset(by_id), f"Missing project anchor assets: {sorted(anchors - set(by_id))}")

    # Important archive honesty checks.
    require(by_id["XLQ-PDF-TRUEBOOK"]["sync_state"] == "FILE_LIBRARY_ONLY_BINARY", "214-page Xuan Yuan book PDF must not be falsely marked mirrored")
    require(by_id["XLQ-TRUE-NO-NOTE"]["sync_state"] == "FILE_LIBRARY_ONLY_TEXT", "Preferred long Xuan Yuan source must not be falsely marked mirrored")
    require(by_id["DX-STATUS-20260804"]["sync_state"] == "GITHUB_MIRRORED", "Digital Xuantianzong status snapshot should be mirrored")
    require(by_id["PF-CURRENT-BRIEF"]["sync_state"] == "GITHUB_MIRRORED", "Promo-film archival brief should be mirrored")
    require(by_id["PC-C1-RULES"]["sync_state"] == "GITHUB_MIRRORED", "Phone-content archival brief should be mirrored")

    required_repo_files = [
        "docs/project/MASTER_PROJECT_REGISTRY_2026-08-08.md",
        "docs/project/SYNC_STATUS_2026-08-08.md",
        "docs/archive/digital_xuantianzong/STATUS_2026-08-04.md",
        "docs/archive/promo_film/README.md",
        "docs/archive/phone_content/README.md",
        "docs/archive/xuanyuan_lianqi/README.md",
        "docs/archive/visual_assets/README.md",
        "data/canon/master_asset_registry_2026-08-08.json",
    ]
    missing_files = [p for p in required_repo_files if not (ROOT / p).exists()]
    require(not missing_files, f"Missing project archive documents: {missing_files}")

    # Canon and project registries must remain separate layers.
    canon = json.loads((ROOT / "data/canon/master_asset_registry_2026-08-08.json").read_text(encoding="utf-8"))
    require(canon.get("project") == "Xuantianzong Virtual Studio", "Canon subregistry identity drifted")
    canon_module = next(m for m in modules if m["id"] == "CANON_AND_WORLD")
    require(canon_module.get("subregistry") == "data/canon/master_asset_registry_2026-08-08.json", "Project registry must point to Canon subregistry")

    print("PROJECT_REGISTRY_VALIDATION: PASS")
    print(f"modules={len(modules)} assets={len(asset_ids)}")
    print("coverage=CANON,DIGITAL_TWIN,VISUAL,PROMO,PHONE,XUANYUAN,DIGITAL_XUANTIANZONG,BEASTS,HISTORY")


if __name__ == "__main__":
    main()
