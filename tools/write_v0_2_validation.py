from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_human_acceptance(path: Path, fields: list[str]):
    if path.exists():
        return load(path)
    payload = {"status": "PENDING_HUMAN_REVIEW", **{field: "PENDING" for field in fields}}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = args.root / "build" / "v0.2"
    manifest = load(output / "manifest.json")
    geometry = load(output / "geometry_validation.json")
    camera = load(output / "camera_metrics.json")
    deterministic = load(output / "deterministic_rebuild_report.json")
    qc = sorted((output / "qc").glob("qc_*.png"))
    peak_qc = sorted((output / "qc" / "xuantian_peak").glob("*.png"))
    sword_qc = sorted((output / "qc" / "twin_swords").glob("*.png"))
    dji_qc = sorted((output / "qc" / "dji_keyframes").glob("*.png"))
    visual = ensure_human_acceptance(
        output / "visual_acceptance.json",
        ["xuantian_peak_silhouette", "twin_sword_visual_scale", "gate_reveal", "post_gate_reveal", "terrain_readability"],
    )
    camera_visual = ensure_human_acceptance(
        output / "camera_visual_acceptance.json",
        ["real_dji_feel", "approach_pacing", "gate_crossing_pacing", "reveal_timing", "post_gate_readability"],
    )
    media = {
        "blend": output / "xuantianzong_mini_digital_twin_v0.2.blend",
        "preview": output / "xuantianzong_mini_v0.2_gate_preview.mp4",
        "global": output / "xuantianzong_mini_v0.2_global.png",
    }
    missing = [str(path) for path in media.values() if not path.is_file() or path.stat().st_size == 0]
    expected_qc_count = int(manifest["qc_camera_count"])
    outputs_present = (
        not missing
        and len(qc) >= expected_qc_count >= 10
        and len(peak_qc) >= int(manifest["xuantian_peak_qc_camera_count"])
        and len(sword_qc) >= int(manifest["twin_sword_fixed_qc_camera_count"]) + int(manifest["twin_sword_dji_keyframe_qc_count"])
        and len(dji_qc) >= int(manifest["dji_keyframe_qc_count"])
    )
    engineering = "PASS" if outputs_present and geometry["status"] == camera["status"] == deterministic["status"] == "PASS" else "FAIL"
    if engineering != "PASS":
        overall = "FAIL"
    elif visual.get("status") == camera_visual.get("status") == "PASS":
        overall = "PASS"
    else:
        overall = "PENDING_HUMAN_REVIEW"
    proxies = manifest["non_canon_proxy_objects"]
    not_visual = manifest.get("locked_design_not_visually_validated", [])
    lines = [
        "# Digital Twin V0.2.2 Final Human Visual Repair — Validation Report",
        "",
        f"ENGINEERING_STATUS: **{engineering}**",
        f"VISUAL_ACCEPTANCE_STATUS: **{visual.get('status', 'INVALID')}**",
        f"CAMERA_VISUAL_ACCEPTANCE_STATUS: **{camera_visual.get('status', 'INVALID')}**",
        f"OVERALL_STATUS: **{overall}**",
        "",
        "## Machine validation",
        "",
        f"- Geometry: {geometry['status']} ({len(geometry['checks'])} checks)",
        f"- DJI camera metrics: {camera['status']} — max speed {camera['max_speed_mps']:.3f} m/s, max acceleration {camera['max_acceleration_mps2']:.3f} m/s², max jerk {camera['max_jerk_mps3']:.3f} m/s³, max yaw rate {camera['max_yaw_rate_deg_s']:.3f}°/s",
        f"- Deterministic rebuild: {deterministic['status']}",
        f"- QC stills: {expected_qc_count} required render views present",
        f"- Xuantian Peak silhouette QC: {len(peak_qc)} images",
        f"- Twin-sword QC: {len(sword_qc)} images",
        f"- DJI keyframe QC: {len(dji_qc)} images",
        "- Render output presence is not treated as human visual acceptance.",
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
    print(f"V0_2_VALIDATION_REPORT: engineering={engineering} overall={overall} output={report}")
    if engineering != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
