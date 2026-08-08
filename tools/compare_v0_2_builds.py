from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("a_snapshot", type=Path)
    parser.add_argument("b_snapshot", type=Path)
    parser.add_argument("a_manifest", type=Path)
    parser.add_argument("b_manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    a_snapshot, b_snapshot = load(args.a_snapshot), load(args.b_snapshot)
    a_manifest, b_manifest = load(args.a_manifest), load(args.b_manifest)
    checks = {
        "object_transforms_and_bounds": a_snapshot["objects"] == b_snapshot["objects"],
        "terrain_control_data": a_snapshot["terrain_control_data"] == b_snapshot["terrain_control_data"],
        "camera_samples": a_snapshot["camera_samples"] == b_snapshot["camera_samples"],
        "camera_metrics": a_snapshot["camera_metrics"] == b_snapshot["camera_metrics"],
        "manifest": a_manifest == b_manifest == a_snapshot["manifest"] == b_snapshot["manifest"],
    }
    payload = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "comparison": checks,
        "inputs": {
            "a_snapshot": {"path": str(args.a_snapshot), "sha256": digest(args.a_snapshot)},
            "b_snapshot": {"path": str(args.b_snapshot), "sha256": digest(args.b_snapshot)},
            "a_manifest": {"path": str(args.a_manifest), "sha256": digest(args.a_manifest)},
            "b_manifest": {"path": str(args.b_manifest), "sha256": digest(args.b_manifest)},
        },
        "note": "Independent clean Blender builds compared at rounded machine-readable state level; .blend container bytes are not required to match.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"DETERMINISTIC_REBUILD: {payload['status']} output={args.output}")
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
