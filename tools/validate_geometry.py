from __future__ import annotations

import json
import math
import sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError as exc:
    raise SystemExit("Run with Blender: blender --background <blend> --python tools/validate_geometry.py") from exc


ROOT = Path(__file__).resolve().parents[1]
BLENDER_DIR = ROOT / "blender"
if str(BLENDER_DIR) not in sys.path:
    sys.path.insert(0, str(BLENDER_DIR))

from v0_2_common import camera_metrics, camera_samples, load_json, rounded, terrain_height, write_json


def world_bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return [min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]


def dimensions_of(objects):
    mins, maxs = [], []
    for obj in objects:
        low, high = world_bounds(obj)
        mins.append(low)
        maxs.append(high)
    low = [min(v[i] for v in mins) for i in range(3)]
    high = [max(v[i] for v in maxs) for i in range(3)]
    return low, high, [high[i] - low[i] for i in range(3)]


def close(actual, expected, tolerance=1e-4):
    return abs(float(actual) - float(expected)) <= tolerance


def check(condition, name, details, results):
    entry = {"name": name, "status": "PASS" if condition else "FAIL", "details": details}
    results.append(entry)
    if not condition:
        raise AssertionError(f"{name}: {details}")


def point_in_expanded_bounds(point, low, high, margin):
    return all(low[i] - margin <= point[i] <= high[i] + margin for i in range(3))


def main():
    out_path = Path(sys.argv[sys.argv.index("--") + 1]) if "--" in sys.argv else ROOT / "build" / "v0.2" / "geometry_validation.json"
    metrics_path = out_path.parent / "camera_metrics.json"
    results = []
    gate_data = load_json("xuanyue_gate.json")
    peaks_data = load_json("peaks.json")
    key_assets = load_json("key_assets.json")

    gate_objs = [bpy.data.objects[name] for name in ("XTZ_V02_GATE_BODY_LEFT", "XTZ_V02_GATE_BODY_RIGHT", "XTZ_V02_GATE_BODY_LINTEL")]
    gate_low, gate_high, gate_dims = dimensions_of(gate_objs)
    check(all(close(v, e) for v, e in zip(gate_dims, (52.0, 18.0, 34.0))), "xuanyue_gate_bbox", {"actual_m": gate_dims, "expected_m": [52, 18, 34]}, results)
    check(all(close(v, e) for v, e in zip(gate_low, (-26.0, 3691.0, 610.0))), "xuanyue_gate_transform", {"bbox_min": gate_low, "anchor": [0, 3700, 610]}, results)

    left_high = world_bounds(bpy.data.objects["XTZ_V02_GATE_BODY_LEFT"])[1]
    right_low = world_bounds(bpy.data.objects["XTZ_V02_GATE_BODY_RIGHT"])[0]
    lintel_low = world_bounds(bpy.data.objects["XTZ_V02_GATE_BODY_LINTEL"])[0]
    opening = [right_low[0] - left_high[0], lintel_low[2] - 610.0]
    check(all(close(v, e) for v, e in zip(opening, (11.0, 15.0))), "central_opening_clearance", {"actual_m": opening, "expected_m": [11, 15]}, results)

    sword_bounds = {}
    axes = []
    for side in ("WEST", "EAST"):
        objs = [obj for obj in bpy.data.objects if obj.name.startswith(f"XTZ_V02_SWORD_{side}_") and not obj.name.endswith("_BASE")]
        low, high, dims = dimensions_of(objs)
        blade = bpy.data.objects[f"XTZ_V02_SWORD_{side}_BLADE"]
        vertices = [blade.matrix_world @ v.co for v in blade.data.vertices]
        axis = sum(p.x for p in vertices) / len(vertices)
        axes.append(axis)
        sword_bounds[side] = {"low": low, "high": high, "height_m": dims[2], "axis_x_m": axis}
        check(close(dims[2], 44.0), f"twin_sword_{side.lower()}_height", sword_bounds[side], results)
    check(close(axes[1] - axes[0], 68.0), "twin_sword_axis_distance", {"axes_x_m": axes, "distance_m": axes[1] - axes[0]}, results)

    terrain = bpy.data.objects.get("XTZ_V02_F1_CONTINUOUS_TERRAIN")
    check(terrain is not None and len(terrain.data.vertices) >= 38000, "continuous_terrain_exists", {"vertices": len(terrain.data.vertices) if terrain else 0}, results)
    pass_center = terrain_height(0.0, 3700.0)
    west_shoulder = terrain_height(-92.0, 3700.0)
    east_shoulder = terrain_height(104.0, 3700.0)
    check(close(pass_center, 610.0, 0.2) and west_shoulder > 690.0 and east_shoulder > 700.0, "xuanyue_gate_embedded_in_mountain_pass", {"center_m": pass_center, "west_m": west_shoulder, "east_m": east_shoulder}, results)

    road = bpy.data.objects.get("XTZ_V02_ANCIENT_ROAD_SMOOTH_PROXY")
    internal = bpy.data.objects.get("XTZ_V02_INTERIOR_ROUTE_SMOOTH_PROXY")
    check(road is not None and internal is not None and len(road.data.polygons) > 80 and len(internal.data.polygons) > 50, "road_geometry_continuity", {"approach_segments": len(road.data.polygons), "interior_segments": len(internal.data.polygons)}, results)
    road_points = [road.matrix_world @ v.co for v in road.data.vertices]
    internal_points = [internal.matrix_world @ v.co for v in internal.data.vertices]
    # A ribbon's two edge vertices are offset along the local normal, so neither
    # individual edge is the locked centreline endpoint.  Validate the midpoint
    # of the final/first edge pair instead.
    road_end = (road_points[-2] + road_points[-1]) / 2.0
    internal_start = (internal_points[0] + internal_points[1]) / 2.0
    check(
        (road_end - internal_start).length < 0.25
        and abs(road_end.y - 3700.0) < 0.1
        and abs(road_end.x) < 0.1,
        "road_gate_interior_continuity",
        {"approach_centerline_end": list(road_end), "interior_centerline_start": list(internal_start), "gap_m": (road_end - internal_start).length},
        results,
    )

    anchors = [obj for obj in bpy.data.objects if obj.name.startswith("XTZ_V02_PEAK_ANCHOR_")]
    floating = [obj for obj in anchors if obj.get("xtz_floating")]
    check(len(anchors) == 9 and len(floating) == 1 and floating[0].get("xtz_name") == "玄天峰", "single_floating_main_peak", {"formal_peaks": len(anchors), "floating": [o.get("xtz_name") for o in floating]}, results)

    expected_peaks = {p["id"]: p for p in peaks_data["peaks"]}
    peak_transform_ok = True
    peak_details = []
    for anchor in anchors:
        source = expected_peaks[anchor["xtz_asset_id"]]
        expected = [source["center_km"][0] * 1000.0, source["center_km"][1] * 1000.0, source["summit_elevation_m"]]
        actual = list(anchor.location)
        peak_transform_ok &= all(close(a, e) for a, e in zip(actual, expected))
        peak_details.append({"id": source["id"], "actual": actual, "expected": expected})
    check(peak_transform_ok, "canon_peak_anchor_transforms", peak_details, results)

    xuan_objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("XTZ_V02_XUANTIAN_")]
    xuan_low, xuan_high, xuan_dims = dimensions_of(xuan_objects)
    check(close(xuan_low[2], 1210.0, 0.1) and close(xuan_high[2], 1680.0, 0.1) and xuan_dims[0] <= 1450.01 and xuan_dims[1] <= 1050.01, "xuantian_locked_envelope", {"min": xuan_low, "max": xuan_high, "dimensions": xuan_dims}, results)

    locked_assets = {a["id"]: a for a in key_assets["assets"] if a.get("v0_1_build")}
    core_ok = True
    core_details = []
    for obj in bpy.data.objects:
        if not obj.name.startswith("XTZ_V02_B1_"):
            continue
        source = locked_assets[obj["xtz_asset_id"]]
        expected_loc = [source["coord_km"][0] * 1000.0, source["coord_km"][1] * 1000.0, source["elevation_m"] + source["height_m"] / 2.0]
        expected_dim = [*source["plan_m"], source["height_m"]]
        core_ok &= all(close(a, e) for a, e in zip(obj.location, expected_loc)) and all(close(a, e) for a, e in zip(obj.dimensions, expected_dim))
        core_details.append({"id": source["id"], "location": list(obj.location), "dimensions": list(obj.dimensions)})
    check(core_ok and len(core_details) == 7, "canon_b1_asset_transforms", core_details, results)

    samples = camera_samples()
    metrics = camera_metrics(samples)
    terrain_clearances = [row["position"][2] - terrain_height(row["position"][0], row["position"][1]) for row in samples]
    check(min(terrain_clearances) > 2.5, "camera_no_terrain_collision", {"minimum_clearance_m": min(terrain_clearances)}, results)
    inside_gate = [row for row in samples if 3691.0 <= row["position"][1] <= 3709.0]
    gate_clear = bool(inside_gate) and all(abs(row["position"][0]) < 5.5 and 610.0 < row["position"][2] < 625.0 for row in inside_gate)
    check(gate_clear and inside_gate[0]["position"][1] <= 3692.0 and inside_gate[-1]["position"][1] >= 3708.0, "camera_no_gate_or_lintel_collision", {"inside_frames": len(inside_gate), "first": inside_gate[0]["position"], "last": inside_gate[-1]["position"]}, results)

    sword_collision = False
    for row in samples:
        point = row["position"]
        for bounds in sword_bounds.values():
            if point_in_expanded_bounds(point, bounds["low"], bounds["high"], 1.0):
                sword_collision = True
    check(not sword_collision, "camera_no_twin_sword_collision", {"collision": sword_collision}, results)

    max_step = max(math.dist(a["position"], b["position"]) for a, b in zip(samples, samples[1:]))
    check(max_step < 1.2, "camera_path_continuity", {"max_frame_displacement_m": max_step}, results)
    for field, limit_field in (("max_speed_mps", "max_speed_mps"), ("max_acceleration_mps2", "max_acceleration_mps2"), ("max_jerk_mps3", "max_jerk_mps3"), ("max_yaw_rate_deg_s", "max_yaw_rate_deg_s")):
        check(metrics[field] <= metrics["limits"][limit_field], f"camera_{field}", {"actual": metrics[field], "limit": metrics["limits"][limit_field]}, results)
    check(metrics["max_yaw_rate_8_11_5_deg_s"] <= metrics["limits"]["max_yaw_rate_8_11_5_deg_s"], "camera_gate_run_local_yaw_rate", {"actual": metrics["max_yaw_rate_8_11_5_deg_s"], "limit": metrics["limits"]["max_yaw_rate_8_11_5_deg_s"]}, results)

    payload = rounded({
        "status": "PASS",
        "blend": bpy.data.filepath,
        "checks": results,
        "camera_metrics": metrics,
        "non_canon_proxy_count": sum(1 for obj in bpy.data.objects if obj.get("xtz_status") == "NON_CANON_PROXY"),
        "locked_design_not_visually_validated": [],
    })
    write_json(out_path, payload)
    write_json(metrics_path, metrics)
    print(f"GEOMETRY_VALIDATION: PASS checks={len(results)} output={out_path}")


if __name__ == "__main__":
    main()
