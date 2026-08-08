from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import bpy

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from xtz_common import load_world_json, repo_root
from builders import (
    add_world_envelope,
    animate_camera_from_path,
    build_axis,
    build_cameras,
    build_gate,
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


def load_preview_path() -> dict:
    path = repo_root() / "data" / "world" / "preview_camera_paths.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["paths"][0]


def write_manifest(scene, peak_count: int, frame_end: int, gate_data: dict, axis_data: dict):
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
        "central_axis_status": axis_data["status"],
        "central_axis_control_nodes": len(axis_data["axis_nodes_km"]),
        "frame_start": scene.frame_start,
        "frame_end": frame_end,
        "fps": scene.render.fps,
        "warning": scene["xtz_warning"],
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[XTZ] Wrote manifest: {out}")


def build():
    configure_scene()
    clear_xtz_scene()

    peaks = load_world_json("peaks.json")
    gate = load_world_json("xuanyue_gate.json")
    axis = load_world_json("central_axis.json")
    cameras = load_world_json("camera_e1.json")
    preview_path = load_preview_path()

    width_km, depth_km = peaks["coordinate_system"]["envelope_km"]
    add_world_envelope(width_km, depth_km)
    peak_objects = build_peaks(peaks)

    # World anchors/control nodes are read directly from locked A1 data.
    # Meshes are still proxy geometry and must not be mistaken for final asset art.
    gate_result = build_gate(gate)
    axis_obj, axis_points = build_axis(axis)
    camera_result = build_cameras(cameras, axis_points)

    frame_end = animate_camera_from_path(camera_result["drone"], preview_path)

    scene = bpy.context.scene
    scene["xtz_project"] = "Xuantianzong Virtual Studio"
    scene["xtz_milestone"] = "Digital Twin V0.1"
    scene["xtz_canon"] = peaks["canon"]
    scene["xtz_gate_anchor_status"] = gate["world_anchor"]["status"]
    scene["xtz_axis_status"] = axis["status"]
    scene["xtz_warning"] = (
        "A1 world anchors/control nodes are locked. Graybox meshes, E1 preview rig and DJI preview path "
        "remain engineering proxies unless explicitly promoted by a later approved specification."
    )

    write_manifest(scene, len(peak_objects), frame_end, gate, axis)

    print(
        f"[XTZ] Built {len(peak_objects)} peak proxies, gate proxy at A1 anchor {tuple(gate_result['anchor'])}, "
        f"A1 axis with {len(axis_points)} locked control nodes, "
        f"{1 + len(camera_result['e1'])} cameras and preview animation."
    )
    print(f"[XTZ] Axis object status: {axis_obj['xtz_geometry_status']}")

    if os.environ.get("XTZ_SAVE_BLEND") == "1":
        out = repo_root() / "build" / "xuantianzong_digital_twin_v0.1.blend"
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"[XTZ] Saved {out}")


if __name__ == "__main__":
    build()
