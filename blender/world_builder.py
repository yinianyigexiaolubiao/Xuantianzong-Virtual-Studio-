from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from xtz_common import load_world_json, repo_root
from builders import (
    add_world_envelope,
    animate_camera_from_path,
    build_ancient_road,
    build_axis,
    build_cameras,
    build_gate,
    build_key_assets,
    build_peaks,
    clear_xtz_scene,
)


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.035, 0.045, 0.065)


def load_preview_path() -> dict:
    path = repo_root() / "data" / "world" / "preview_camera_paths.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["paths"][0]


def write_manifest(
    scene,
    peak_count: int,
    key_asset_count: int,
    frame_end: int,
    gate_data: dict,
    road_data: dict,
    axis_data: dict,
    key_assets_data: dict,
):
    out = repo_root() / "build" / "digital_twin_v0.1_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "project": "Xuantianzong Virtual Studio",
        "milestone": "Digital Twin V0.1",
        "canon": scene["xtz_canon"],
        "peak_count": peak_count,
        "gate_anchor_status": gate_data["world_anchor"]["status"],
        "gate_anchor": {
            "center_km": gate_data["world_anchor"]["center_km"],
            "ground_elevation_m": gate_data["world_anchor"]["ground_elevation_m"],
        },
        "ancient_road_status": road_data["status"],
        "ancient_road_control_points": len(road_data["control_points"]),
        "ancient_road_actual_length_km": road_data["actual_length_km"],
        "central_axis_status": axis_data["status"],
        "central_axis_control_nodes": len(axis_data["axis_nodes_km"]),
        "central_axis_actual_length_km": axis_data["actual_length_km"],
        "key_assets_status": key_assets_data["status"],
        "v0_1_key_asset_proxy_count": key_asset_count,
        "continuous_entry_route": "接引院 → 十二里入山古道 → 玄岳关 → 九段玄阶 → 接天阵台 → 玄天峰核心建筑群",
        "frame_start": scene.frame_start,
        "frame_end": frame_end,
        "fps": scene.render.fps,
        "preview_camera": "XTZ_CAM_DJI_28MM_PROXY",
        "preview_duration_s": frame_end / scene.render.fps,
        "deliverables": {
            "blend": "build/xuantianzong_digital_twin_v0.1.blend",
            "global_graybox": "build/xuantianzong_digital_twin_v0.1_global_graybox.png",
            "gate_preview_video": "build/xuantianzong_digital_twin_v0.1_gate_preview.mp4",
            "validation_report": "build/digital_twin_v0.1_validation.md"
        },
        "warning": scene["xtz_warning"],
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[XTZ] Wrote manifest: {out}")


def build():
    configure_scene()
    clear_xtz_scene()

    peaks = load_world_json("peaks.json")
    gate = load_world_json("xuanyue_gate.json")
    ancient_road = load_world_json("ancient_road.json")
    axis = load_world_json("central_axis.json")
    key_assets = load_world_json("key_assets.json")
    cameras = load_world_json("camera_e1.json")
    preview_path = load_preview_path()

    width_km, depth_km = peaks["coordinate_system"]["envelope_km"]
    add_world_envelope(width_km, depth_km)
    peak_objects = build_peaks(peaks)

    # A1/B1 anchors and control points are read directly from locked Canon data.
    # Meshes remain proxy geometry until detailed asset design is approved.
    gate_result = build_gate(gate)
    road_obj, road_points = build_ancient_road(ancient_road)
    axis_obj, axis_points = build_axis(axis)
    key_asset_objects = build_key_assets(key_assets)

    road_end = Vector(road_points[-1])
    axis_start = Vector(axis_points[0])
    if (road_end - axis_start).length > 0.01:
        raise ValueError("Ancient-road A8 and central-axis start are not spatially continuous")

    expected_asset_names = {"接天阵台", "接天阵门", "礼制等候院", "玄天殿", "祖师堂", "掌门院", "魂灯殿"}
    built_asset_names = {obj["xtz_name"] for obj in key_asset_objects}
    if not expected_asset_names.issubset(built_asset_names):
        missing = sorted(expected_asset_names - built_asset_names)
        raise ValueError(f"Missing required B1 V0.1 key-asset proxies: {missing}")

    camera_result = build_cameras(cameras, axis_points)
    frame_end = animate_camera_from_path(camera_result["drone"], preview_path)

    scene = bpy.context.scene
    scene["xtz_project"] = "Xuantianzong Virtual Studio"
    scene["xtz_milestone"] = "Digital Twin V0.1"
    scene["xtz_canon"] = peaks["canon"]
    scene["xtz_gate_anchor_status"] = gate["world_anchor"]["status"]
    scene["xtz_ancient_road_status"] = ancient_road["status"]
    scene["xtz_axis_status"] = axis["status"]
    scene["xtz_key_assets_status"] = key_assets["status"]
    scene["xtz_warning"] = (
        "A1/B1 world anchors, control points and approved envelopes are locked. Graybox meshes, detailed road/stair geometry, "
        "E1 preview rig and DJI preview path remain engineering proxies unless explicitly promoted by a later approved specification."
    )

    write_manifest(
        scene,
        len(peak_objects),
        len(key_asset_objects),
        frame_end,
        gate,
        ancient_road,
        axis,
        key_assets,
    )

    print(
        f"[XTZ] Built {len(peak_objects)} peak proxies, gate proxy at A1 anchor {tuple(gate_result['anchor'])}, "
        f"ancient road with {len(road_points)} locked A1 control points, "
        f"central axis with {len(axis_points)} locked A1 control nodes, "
        f"{len(key_asset_objects)} B1 core asset proxies, "
        f"{1 + len(camera_result['e1'])} cameras and preview animation."
    )
    print(f"[XTZ] Ancient-road status: {road_obj['xtz_geometry_status']}")
    print(f"[XTZ] Axis status: {axis_obj['xtz_geometry_status']}")
    print("[XTZ] Entry-route continuity: PASS (ancient-road A8 == central-axis start == Xuanyue Gate)")

    if os.environ.get("XTZ_SAVE_BLEND") == "1":
        out = repo_root() / "build" / "xuantianzong_digital_twin_v0.1.blend"
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"[XTZ] Saved {out}")


if __name__ == "__main__":
    build()
