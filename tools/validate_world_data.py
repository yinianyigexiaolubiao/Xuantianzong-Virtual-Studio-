from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "data" / "world"


def load(name: str) -> dict:
    path = WORLD / name
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str):
    raise AssertionError(message)


def main():
    peaks = load("peaks.json")
    gate = load("xuanyue_gate.json")
    axis = load("central_axis.json")
    cameras = load("camera_e1.json")
    preview = load("preview_camera_paths.json")

    if peaks["rules"]["formal_peak_count"] != 9:
        fail("formal_peak_count must be 9")
    if len(peaks["peaks"]) != 9:
        fail("peaks array must contain exactly 9 peaks")

    floating = [p for p in peaks["peaks"] if p.get("floating")]
    if len(floating) != 1 or floating[0]["name"] != "玄天峰":
        fail("玄天峰 must be the only large floating main peak")

    ids = [p["id"] for p in peaks["peaks"]]
    if len(ids) != len(set(ids)):
        fail("peak IDs must be unique")

    if gate["dimensions_m"] != {"width": 52, "depth": 18, "height": 34}:
        fail("玄岳关 locked body dimensions changed")
    if gate["twin_swords"]["height_m"] != 44:
        fail("双阙剑 locked height changed")
    if gate["twin_swords"]["axis_distance_m"] != 68:
        fail("双阙剑 locked axis distance changed")

    if axis["nine_stages"]["segments"] != 9:
        fail("中央登宗主轴 must contain nine stages")
    if axis["nine_stages"]["stairs"] != 3600:
        fail("九段玄阶 total stair count must remain 3600")
    if "no straight sky staircase" not in axis["nine_stages"]["rule"]:
        fail("central-axis anti-straight-stair rule is missing")

    if cameras["drone_camera"]["lens_equivalent"] != "24-35mm":
        fail("DJI camera range must remain 24-35mm equivalent")

    for path in preview["paths"]:
        if path["canon_status"] != "NON_CANON_PROXY":
            fail("V0.1 preview paths must remain NON_CANON_PROXY until reviewed")
        if len(path["keyframes"]) < 2:
            fail("preview path requires at least two keyframes")

    print("[XTZ] world data validation: PASS")
    print("[XTZ] 9 peaks / 1 floating main peak / gate / swords / axis / camera rules verified")


if __name__ == "__main__":
    main()
