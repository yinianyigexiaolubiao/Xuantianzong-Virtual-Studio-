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


def approx_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(float(a) - float(b)) <= tol


def main():
    peaks = load("peaks.json")
    gate = load("xuanyue_gate.json")
    road = load("ancient_road.json")
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

    xuan = floating[0]
    if xuan.get("status") != "CANON_A1_LOCKED":
        fail("玄天峰 A1 envelope must remain locked")
    if xuan["center_km"] != [0.0, 9.35]:
        fail("玄天峰 center must remain (0.00, 9.35km)")
    if xuan["summit_elevation_m"] != 1680:
        fail("玄天峰 summit must remain 1680m")
    if xuan["deepest_inverted_spire_elevation_m"] != 1210:
        fail("玄天峰 deepest inverted spire must remain 1210m")
    if xuan["main_vertical_body_depth_m"] != [400, 470]:
        fail("玄天峰 main vertical body depth must remain 400-470m")
    if xuan["main_palace_terrace_elevation_m"] != [1605, 1615]:
        fail("玄天峰 main palace terrace must remain 1605-1615m")
    if xuan["central_clearance_m"] != [180, 250]:
        fail("玄天峰 central clearance must remain 180-250m")

    ids = [p["id"] for p in peaks["peaks"]]
    if len(ids) != len(set(ids)):
        fail("peak IDs must be unique")

    if gate["status"] != "CANON_A1_LOCKED":
        fail("玄岳关 must remain CANON_A1_LOCKED")
    if gate["world_anchor"]["center_km"] != [0.0, 3.7]:
        fail("玄岳关 A1 center must remain (0.00, 3.70km)")
    if gate["world_anchor"]["ground_elevation_m"] != 610:
        fail("玄岳关 ground elevation must remain 610m")
    if gate["dimensions_m"]["width"] != 52 or gate["dimensions_m"]["depth"] != 18 or gate["dimensions_m"]["height"] != 34:
        fail("玄岳关 locked body dimensions changed")
    if gate["dimensions_m"]["total_depth_with_eaves"] != 21:
        fail("玄岳关 total depth with eaves must remain 21m")
    if gate["twin_swords"]["height_m"] != 44:
        fail("双阙剑 locked height changed")
    if gate["twin_swords"]["axis_distance_m"] != 68:
        fail("双阙剑 locked axis distance changed")
    if gate["twin_swords"]["axes_local_x_m"] != [-34, 34]:
        fail("双阙剑 local X axes must remain -34m/+34m")

    expected_road = [
        ("A0", [0.05, 1.22], 445),
        ("A1", [-0.40, 1.50], 458),
        ("A2", [0.45, 1.80], 475),
        ("A3", [-0.50, 2.15], 495),
        ("A4", [0.40, 2.45], 520),
        ("A5", [-0.40, 2.80], 545),
        ("A6", [0.30, 3.10], 570),
        ("A7", [-0.20, 3.35], 592),
        ("A8", [0.00, 3.70], 610),
    ]
    if road["status"] != "CANON_A1_LOCKED":
        fail("twelve-li ancient road must remain CANON_A1_LOCKED")
    if len(road["control_points"]) != 9:
        fail("ancient road must contain A0-A8 control points")
    for actual, expected in zip(road["control_points"], expected_road):
        exp_id, exp_coord, exp_elev = expected
        if actual["id"] != exp_id or actual["coord_km"] != exp_coord or actual["elev_m"] != exp_elev:
            fail(f"ancient-road control point {exp_id} changed")
    if not approx_equal(road["actual_length_km"], 6.0):
        fail("ancient road actual length must remain 6.0km")
    if road["total_climb_m"] != 165:
        fail("ancient road climb must remain 165m")
    if road["major_switchbacks"] != 7:
        fail("ancient road major switchbacks must remain 7")
    if road["final_jade_approach_length_m"] != 180:
        fail("final jade approach must remain 180m")
    road_end = road["control_points"][-1]
    if road_end["coord_km"] != gate["world_anchor"]["center_km"] or road_end["elev_m"] != gate["world_anchor"]["ground_elevation_m"]:
        fail("ancient-road A8 must coincide with Xuanyue Gate A1 anchor")

    expected_nodes = [
        [0.0, 3.7], [-0.38, 4.25], [0.34, 4.83], [-0.45, 5.42], [0.37, 5.98],
        [-0.31, 6.57], [0.24, 7.17], [-0.18, 7.78], [0.12, 8.42], [0.0, 9.1],
    ]
    expected_elevs = [610, 674, 742, 812, 884, 958, 1034, 1112, 1192, 1270]

    if axis["status"] != "CANON_A1_LOCKED":
        fail("central axis must remain CANON_A1_LOCKED")
    if axis["axis_nodes_km"] != expected_nodes:
        fail("A1 central-axis control nodes changed")
    if axis["axis_node_elevations_m"] != expected_elevs:
        fail("A1 central-axis elevations changed")
    if len(axis["axis_nodes_km"]) != 10:
        fail("A1 central axis must contain 10 control nodes")
    if axis["start"]["coord_km"] != [0.0, 3.7] or axis["end"]["coord_km"] != [0.0, 9.1]:
        fail("central-axis start/end coordinates changed")
    if axis["start"]["elevation_m"] != 610 or axis["end"]["elevation_m"] != 1270:
        fail("central-axis start/end elevations changed")
    if road_end["coord_km"] != axis["start"]["coord_km"] or road_end["elev_m"] != axis["start"]["elevation_m"]:
        fail("ancient road and central axis must join exactly at Xuanyue Gate")
    if len(axis["stages"]) != 9:
        fail("中央登宗主轴 must contain nine stages")
    if sum(stage["steps"] for stage in axis["stages"]) != 3600:
        fail("九段玄阶 total stair count must remain 3600")
    if not approx_equal(sum(stage["length_km"] for stage in axis["stages"]), 7.2, tol=1e-6):
        fail("nine-stage actual length must sum to 7.2km")
    if axis["total_climb_m"] != 660:
        fail("nine-stage total climb must remain 660m")
    if axis["geometry_rules"]["max_continuous_route_alignment_sightline_m"] != 250:
        fail("max continuous route alignment sightline must remain 250m")
    if "no straight sky staircase" not in axis["nine_stages"]["rule"]:
        fail("central-axis anti-straight-stair rule is missing")

    if cameras["drone_camera"]["lens_equivalent"] != "24-35mm":
        fail("DJI camera range must remain 24-35mm equivalent")

    canonical_gate_anchor_m = [0.0, 3700.0, 610.0]
    opening_top_m = gate["world_anchor"]["ground_elevation_m"] + gate["main_gate"]["clear_height"]
    for path in preview["paths"]:
        if path["canon_status"] != "NON_CANON_PROXY":
            fail("V0.1 preview paths must remain NON_CANON_PROXY until reviewed")
        if path["anchor_dependency"]["gate_anchor_m"] != canonical_gate_anchor_m:
            fail("preview path must reference canonical A1 gate anchor")
        if path["anchor_dependency"]["status"] != "CANON_A1_LOCKED":
            fail("preview anchor dependency must be CANON_A1_LOCKED")
        if len(path["keyframes"]) < 2:
            fail("preview path requires at least two keyframes")
        gate_crossing = [k for k in path["keyframes"] if 3691.0 <= k["location_m"][1] <= 3709.0]
        if not gate_crossing:
            fail("preview path needs at least one keyframe inside the 18m-deep gate body")
        if any(k["location_m"][2] >= opening_top_m for k in gate_crossing):
            fail("preview camera crosses at/above the central opening top")

    print("[XTZ] world data validation: PASS")
    print("[XTZ] nine peaks / Xuantian vertical envelope / ancient road A0-A8 / gate / 10 A1 axis nodes / 3600 stairs verified")


if __name__ == "__main__":
    main()
