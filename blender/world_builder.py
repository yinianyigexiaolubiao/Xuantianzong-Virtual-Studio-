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


def write_manifest(scene, peak_count: int, frame_end: int):
    out = repo_root() / "build" / "digital_twin_v0.1_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "project": "Xuantianzong Virtual Studio",
        "milestone": "Digital Twin V0.1",
        "canon": scene["xtz_canon"],
        "peak_count": peak_count,
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

    # Engineering placeholders only until canonical absolute A1 waypoints are imported.
    build_gate(gate, anchor=(0.0, 2000.0, 0.0))
    _, axis_points = build_axis(axis, start=(0.0, 2000.0, 2.0))
    camera_result = build_cameras(cameras, axis_points)

    frame_end = animate_camera_from_path(camera_result["drone"], preview_path)

    scene = bpy.context.scene
    scene["xtz_project"] = "Xuantianzong Virtual Studio"
    scene["xtz_milestone"] = "Digital Twin V0.1"
    scene["xtz_canon"] = peaks["canon"]
    scene["xtz_warning"] = (
        "Graybox prototype. NON_CANON_PROXY objects/paths must not be promoted "
        "to production Canon without an explicit locked spec."
    )

    write_manifest(scene, len(peak_objects), frame_end)

    print(
        f"[XTZ] Built {len(peak_objects)} peaks, gate proxy, axis preview, "
        f"{1 + len(camera_result['e1'])} cameras and preview animation."
    )

    if os.environ.get("XTZ_SAVE_BLEND") == "1":
        out = repo_root() / "build" / "xuantianzong_digital_twin_v0.1.blend"
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"[XTZ] Saved {out}")


if __name__ == "__main__":
    build()
