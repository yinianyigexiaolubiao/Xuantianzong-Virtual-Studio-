from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "data" / "world"


def load(name):
    return json.loads((WORLD / name).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    peaks = load("peaks.json")
    gate = load("xuanyue_gate.json")
    axis = load("central_axis.json")
    camera = load("camera_e1.json")

    items = peaks["peaks"]
    require(len(items) == 9, "Canon requires exactly nine formal peaks")
    require(len({p["id"] for p in items}) == 9, "Peak asset IDs must be unique")
    require(len({p["name"] for p in items}) == 9, "Peak names must be unique")
    floating = [p for p in items if p.get("floating")]
    require(len(floating) == 1, "Exactly one large floating main peak is allowed")
    require(floating[0]["name"] == "玄天峰", "The unique floating main peak must be 玄天峰")

    for p in items:
        require(len(p["center_km"]) == 2, f"{p['name']} center_km invalid")
        require(p["summit_elevation_m"] > 0, f"{p['name']} summit invalid")
        require(all(v > 0 for v in p["core_body_km"]), f"{p['name']} core body invalid")

    dims = gate["dimensions_m"]
    require(all(dims[k] > 0 for k in ("width", "depth", "height")), "Gate dimensions invalid")
    sword = gate["twin_swords"]
    require(sword["height_m"] == 44, "Twin sword height must remain 44m")
    require(sword["axis_distance_m"] == 68, "Twin sword axis distance must remain 68m")
    require("double-edged straight sword" in sword["shape"], "Twin swords must remain straight double-edged")

    require(axis["nine_stages"]["stairs"] == 3600, "Central axis must keep 3600 stairs")
    require(axis["nine_stages"]["segments"] == 9, "Central axis must keep nine stages")
    require(axis["total_centerline_km"] == 7.2, "Central axis centerline must remain 7.2 km")

    require(camera["drone_camera"]["lens_equivalent"] == "24-35mm", "DJI lens range must remain 24–35mm")
    require(camera["master_camera"]["lens_equivalent"] == "50mm three-frame horizontal virtual stitch", "E1 master camera definition changed unexpectedly")

    print("XTZ world data validation: PASS")
    print("9 peaks / 1 floating main peak / gate / swords / axis / E1 camera validated.")


if __name__ == "__main__":
    main()
