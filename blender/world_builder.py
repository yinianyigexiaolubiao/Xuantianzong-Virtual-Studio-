from __future__ import annotations

import os
import sys
from pathlib import Path

import bpy

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from xtz_common import load_world_json, repo_root
from builders import add_world_envelope, build_axis, build_cameras, build_gate, build_peaks, clear_xtz_scene


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 24


def build():
    configure_scene()
    clear_xtz_scene()
    peaks = load_world_json("peaks.json")
    gate = load_world_json("xuanyue_gate.json")
    axis = load_world_json("central_axis.json")
    cameras = load_world_json("camera_e1.json")

    width_km, depth_km = peaks["coordinate_system"]["envelope_km"]
    add_world_envelope(width_km, depth_km)
    peak_objects = build_peaks(peaks)

    gate_result = build_gate(gate, anchor=(0.0, 2000.0, 0.0))
    axis_obj, axis_points = build_axis(axis, start=(0.0, 2000.0, 2.0))
    camera_result = build_cameras(cameras, axis_points)

    scene = bpy.context.scene
    scene["xtz_project"] = "Xuantianzong Virtual Studio"
    scene["xtz_milestone"] = "Digital Twin V0.1"
    scene["xtz_canon"] = peaks["canon"]
    scene["xtz_warning"] = "Graybox prototype. NON_CANON_PROXY objects must not be promoted to production Canon without an explicit locked spec."

    print(f"[XTZ] Built {len(peak_objects)} peaks, gate proxy, axis preview and {1 + len(camera_result['e1'])} cameras.")

    if os.environ.get("XTZ_SAVE_BLEND") == "1":
        out = repo_root() / "build" / "xuantianzong_digital_twin_v0.1.blend"
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"[XTZ] Saved {out}")


if __name__ == "__main__":
    build()
