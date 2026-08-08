from __future__ import annotations

import os
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "v0.2"
QC_OUTPUT = OUTPUT / "qc"


def configure_workbench(width: int, height: int):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.display.shading.light = "STUDIO"
    scene.display.shading.studio_light = "paint.sl"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.background_type = "WORLD"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "WORLD"
    scene.display.shading.curvature_ridge_factor = 1.4
    scene.display.shading.curvature_valley_factor = 1.0
    scene.world.color = (0.78, 0.82, 0.86)
    return scene


def render_still(scene, camera_name: str, path: Path, width=960, height=540):
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.camera = bpy.data.objects[camera_name]
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    print(f"[XTZ V0.2] RENDERED {path}")


def render_qc(scene):
    QC_OUTPUT.mkdir(parents=True, exist_ok=True)
    cameras = sorted(obj.name for obj in bpy.data.objects if obj.name.startswith("XTZ_CAM_QC_"))
    if len(cameras) < 10:
        raise RuntimeError(f"Expected >=10 QC cameras, found {len(cameras)}")
    for index, camera_name in enumerate(cameras, 1):
        render_still(scene, camera_name, QC_OUTPUT / f"qc_{index:02d}_{camera_name.removeprefix('XTZ_CAM_QC_').lower()}.png")
    render_still(scene, "XTZ_CAM_QC_12_F1_STRATEGIC", OUTPUT / "xuantianzong_mini_digital_twin_v0.2_global.png", 1600, 900)


def render_video(scene):
    scene.camera = bpy.data.objects["XTZ_V02_CAM_DJI_28MM"]
    scene.frame_start = 1
    scene.frame_end = 360
    scene.render.fps = 24
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    scene.render.filepath = str(OUTPUT / "xuantianzong_gate_flythrough_v0.2.mp4")
    bpy.ops.render.render(animation=True)
    print(f"[XTZ V0.2] VIDEO RENDERED {scene.render.filepath}")


def main():
    if not bpy.data.filepath:
        raise RuntimeError("Open the V0.2 blend before running the renderer")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    scene = configure_workbench(960, 540)
    mode = os.environ.get("XTZ_V02_RENDER_MODE", "all").lower()
    if mode in {"all", "qc"}:
        render_qc(scene)
    if mode in {"all", "video"}:
        render_video(scene)
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)


if __name__ == "__main__":
    main()
