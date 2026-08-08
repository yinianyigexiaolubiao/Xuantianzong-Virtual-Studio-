from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = args.root / "build" / "v0.2"
    manifest = load(output / "digital_twin_v0.2_manifest.json")
    geometry = load(output / "geometry_validation.json")
    camera = load(output / "camera_metrics.json")
    deterministic = load(output / "deterministic_rebuild_report.json")
    qc = sorted((output / "qc").glob("*.png"))
    media = {
        "blend": output / "xuantianzong_mini_digital_twin_v0.2.blend",
        "preview": output / "xuantianzong_gate_flythrough_v0.2.mp4",
        "global": output / "xuantianzong_mini_digital_twin_v0.2_global.png",
    }
    missing = [str(path) for path in media.values() if not path.is_file() or path.stat().st_size == 0]
    expected_qc_count = int(manifest["qc_camera_count"])
    overall = "PASS" if not missing and len(qc) >= expected_qc_count >= 10 and geometry["status"] == camera["status"] == deterministic["status"] == "PASS" else "FAIL"
    proxies = manifest["non_canon_proxy_objects"]
    not_visual = manifest.get("locked_design_not_visually_validated", [])
    lines = [
        "# Digital Twin V0.2 Validation Report",
        "",
        f"Overall: **{overall}**",
        "",
        "## Machine validation",
        "",
        f"- Geometry: {geometry['status']} ({len(geometry['checks'])} checks)",
        f"- DJI camera metrics: {camera['status']} — max speed {camera['max_speed_mps']:.3f} m/s, max acceleration {camera['max_acceleration_mps2']:.3f} m/s², max jerk {camera['max_jerk_mps3']:.3f} m/s³, max yaw rate {camera['max_yaw_rate_deg_s']:.3f}°/s",
        f"- Deterministic rebuild: {deterministic['status']}",
        f"- QC stills: {expected_qc_count} required render views present",
        f"- Missing/empty deliverables: {missing or 'none'}",
        "",
        "## NON_CANON_PROXY",
        "",
        "All items below are temporary graybox/proof objects and are not promoted to Canon:",
        "",
        *[f"- {name}" for name in proxies],
        "",
        "## LOCKED_DESIGN_NOT_VISUALLY_VALIDATED",
        "",
        *([f"- {name}" for name in not_visual] if not_visual else ["- None for the V0.2 acceptance scope."]),
        "",
    ]
    report = output / "validation.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"V0_2_VALIDATION_REPORT: {overall} output={report}")
    if overall != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
