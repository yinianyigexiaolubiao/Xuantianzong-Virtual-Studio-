from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "promo_film_01"
PRODUCTION_BLEND = OUTPUT / "promo_film_01_production.blend"
FPS = 24
PROXY = "NON_CANON_PROXY"

SHOTS = {
    "shot_01_establishing": {"duration_s": 6, "lens": 28.0},
    "shot_02_gate_reveal": {"duration_s": 6, "lens": 28.0},
    "shot_03_gate_crossing": {"duration_s": 6, "lens": 28.0},
    "shot_04_inner_axis": {"duration_s": 7, "lens": 32.0},
    "shot_05_xuantian_peak": {"duration_s": 7, "lens": 32.0},
    "shot_06_xuantian_hall": {"duration_s": 7, "lens": 35.0},
}

MATS: dict[str, bpy.types.Material] = {}


def collection(name: str) -> bpy.types.Collection:
    current = bpy.data.collections.get(name)
    if current is None:
        current = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(current)
    return current


def move_to(obj: bpy.types.Object, target: bpy.types.Collection) -> bpy.types.Object:
    if obj.name not in target.objects:
        target.objects.link(obj)
    for current in list(obj.users_collection):
        if current != target:
            current.objects.unlink(obj)
    return obj


def tag(obj: bpy.types.Object, reason: str) -> bpy.types.Object:
    obj["xtz_status"] = PROXY
    obj["xtz_geometry_status"] = PROXY
    obj["xtz_reason"] = reason
    obj["xtz_production"] = "Promo Film 01《玄天宗·入宗》"
    return obj


def material(name: str, color, metallic=0.0, roughness=0.7, emission=None) -> bpy.types.Material:
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.metallic = metallic
    mat.roughness = roughness
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission is not None:
            bsdf.inputs["Emission Color"].default_value = emission
            bsdf.inputs["Emission Strength"].default_value = 1.6
    return mat


def setup_materials() -> None:
    MATS.update(
        terrain=material("XTZ_PROMO_MAT_TERRAIN", (0.23, 0.34, 0.24, 1.0), roughness=0.88),
        rock=material("XTZ_PROMO_MAT_ROCK", (0.22, 0.28, 0.25, 1.0), roughness=0.94),
        xuan=material("XTZ_PROMO_MAT_XUANTIAN", (0.18, 0.25, 0.22, 1.0), roughness=0.9),
        road=material("XTZ_PROMO_MAT_ROAD", (0.63, 0.57, 0.45, 1.0), roughness=0.82),
        jade=material("XTZ_PROMO_MAT_JADE", (0.88, 0.92, 0.86, 1.0), roughness=0.42),
        jade_warm=material("XTZ_PROMO_MAT_JADE_WARM", (0.96, 0.91, 0.76, 1.0), roughness=0.36),
        gold=material("XTZ_PROMO_MAT_GOLD", (0.72, 0.47, 0.13, 1.0), metallic=0.55, roughness=0.28),
        vermilion=material("XTZ_PROMO_MAT_VERMILION", (0.48, 0.055, 0.035, 1.0), roughness=0.5),
        sword=material("XTZ_PROMO_MAT_SWORD", (0.76, 0.91, 0.96, 1.0), metallic=0.2, roughness=0.24, emission=(0.12, 0.48, 0.7, 1.0)),
        cloud=material("XTZ_PROMO_MAT_CLOUD", (0.92, 0.95, 0.96, 1.0), roughness=0.95),
        tree=material("XTZ_PROMO_MAT_TREE", (0.07, 0.18, 0.10, 1.0), roughness=0.95),
        trunk=material("XTZ_PROMO_MAT_TRUNK", (0.14, 0.075, 0.035, 1.0), roughness=0.95),
        water=material("XTZ_PROMO_MAT_WATER", (0.19, 0.48, 0.58, 1.0), metallic=0.05, roughness=0.18),
    )


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    if not hasattr(obj.data, "materials"):
        return
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def recolor_base_scene() -> None:
    for obj in bpy.data.objects:
        name = obj.name
        if name == "XTZ_V02_F1_CONTINUOUS_TERRAIN":
            assign(obj, MATS["terrain"])
        elif "PASS_ROCK" in name:
            assign(obj, MATS["rock"])
        elif "ANCIENT_ROAD" in name or "INTERIOR_ROUTE" in name:
            assign(obj, MATS["road"])
        elif "GATE_" in name or "FORECOURT" in name:
            assign(obj, MATS["jade"])
        elif "SWORD_" in name:
            assign(obj, MATS["sword"] if "BASE" not in name else MATS["jade_warm"])
        elif name == "XTZ_V02_XUANTIAN_HEAVY_INVERTED_BODY":
            assign(obj, MATS["xuan"])
            obj["xtz_visual_lock"] = "LOCKED_VISUALLY_VALIDATED: geometry and silhouette unchanged"
        elif "XTZ_V02_B1_" in name:
            assign(obj, MATS["jade_warm"])


def add_cube(name: str, dimensions, location, mat, target, rotation=(0.0, 0.0, 0.0), reason="shot-local art proxy"):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    assign(obj, mat)
    return tag(obj, reason)


def add_cylinder(name: str, radius: float, depth: float, location, mat, target, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, target)
    assign(obj, mat)
    return tag(obj, "shot-local architectural/vegetation proxy")


def add_cone(name: str, radius: float, depth: float, location, mat, target, vertices=10):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, target)
    assign(obj, mat)
    return tag(obj, "shot-local vegetation proxy")


def add_cloud(name: str, location, scale, target):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    assign(obj, MATS["cloud"])
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return tag(obj, "procedural cloud bank; atmosphere only, NON_CANON_PROXY")


def build_clouds() -> None:
    target = collection("XTZ_PROMO_Atmosphere")
    rng = random.Random(20260810)
    specs = []
    for index in range(38):
        x = rng.uniform(-3900.0, 3900.0)
        y = rng.uniform(500.0, 10200.0)
        z = rng.choice((rng.uniform(520.0, 720.0), rng.uniform(1040.0, 1260.0)))
        specs.append((x, y, z, rng.uniform(150.0, 420.0), rng.uniform(65.0, 170.0), rng.uniform(18.0, 45.0)))
    specs.extend(
        [
            (-720.0, 8800.0, 1270.0, 310.0, 110.0, 28.0),
            (650.0, 9000.0, 1325.0, 360.0, 125.0, 34.0),
            (-420.0, 9650.0, 1380.0, 270.0, 100.0, 25.0),
            (430.0, 9500.0, 1400.0, 290.0, 105.0, 26.0),
        ]
    )
    for index, (x, y, z, sx, sy, sz) in enumerate(specs, 1):
        add_cloud(f"XTZ_PROMO_CLOUD_{index:03d}", (x, y, z), (sx, sy, sz), target)


def add_tree(name: str, location, scale=1.0) -> None:
    target = collection("XTZ_PROMO_Vegetation")
    x, y, z = location
    add_cylinder(name + "_TRUNK", 0.55 * scale, 6.0 * scale, (x, y, z + 3.0 * scale), MATS["trunk"], target, 8)
    add_cone(name + "_CROWN_A", 4.0 * scale, 8.0 * scale, (x, y, z + 9.0 * scale), MATS["tree"], target, 10)
    add_cone(name + "_CROWN_B", 3.0 * scale, 7.0 * scale, (x, y, z + 13.0 * scale), MATS["tree"], target, 10)


def build_vegetation() -> None:
    rng = random.Random(6103700)
    gate_positions = [(-120.0, 3540.0), (-95.0, 3590.0), (90.0, 3560.0), (115.0, 3610.0), (-125.0, 3790.0), (120.0, 3820.0)]
    axis_positions = [(-85.0, 3920.0), (80.0, 3960.0), (-150.0, 4060.0), (45.0, 4100.0), (-235.0, 4160.0), (-320.0, 4240.0)]
    for index, (x, y) in enumerate(gate_positions + axis_positions, 1):
        terrain = bpy.data.objects.get("XTZ_V02_F1_CONTINUOUS_TERRAIN")
        z = 620.0 if y < 3850 else 645.0 + (y - 3850.0) * 0.09
        add_tree(f"XTZ_PROMO_TREE_{index:03d}", (x + rng.uniform(-15, 15), y + rng.uniform(-18, 18), z), rng.uniform(1.1, 1.8))


def roof_pair(prefix: str, center, width: float, depth: float, z: float, target, scale=1.0) -> None:
    x, y = center
    pitch = math.radians(17.0)
    add_cube(prefix + "_SOUTH", (width, depth * 0.58, 1.6 * scale), (x, y - depth * 0.23, z), MATS["jade"], target, rotation=(pitch, 0.0, 0.0))
    add_cube(prefix + "_NORTH", (width, depth * 0.58, 1.6 * scale), (x, y + depth * 0.23, z), MATS["jade"], target, rotation=(-pitch, 0.0, 0.0))
    add_cube(prefix + "_RIDGE", (width + 2.0 * scale, 1.2 * scale, 1.8 * scale), (x, y, z + 1.2 * scale), MATS["gold"], target)


def build_gate_dressing() -> None:
    target = collection("XTZ_PROMO_GateHero")
    # Additive art detail only. The accepted V0.2 locked body meshes remain untouched.
    roof_pair("XTZ_PROMO_GATE_ROOF", (0.0, 3700.0), 61.0, 25.0, 644.0, target, 1.0)
    for x in (-24.0, -8.0, 8.0, 24.0):
        add_cube(f"XTZ_PROMO_GATE_GOLD_COLUMN_{int(x):+03d}", (1.2, 1.2, 25.0), (x, 3690.3, 625.0), MATS["gold"], target)
    add_cube("XTZ_PROMO_GATE_PLAQUE", (8.8, 0.8, 2.4), (0.0, 3690.2, 634.8), MATS["jade_warm"], target)
    add_cube("XTZ_PROMO_GATE_PLAQUE_GOLD", (6.8, 0.25, 0.6), (0.0, 3689.75, 634.8), MATS["gold"], target)


def build_inner_axis_hero() -> None:
    target = collection("XTZ_PROMO_InnerAxisHero")
    start = Vector((-105.0, 4015.0, 653.0))
    end = Vector((-270.0, 4215.0, 674.0))
    count = 22
    for index in range(count):
        t = index / (count - 1)
        center = start.lerp(end, t)
        center.x += 18.0 * math.sin(t * math.pi)
        center.z += 0.55
        add_cube(
            f"XTZ_PROMO_AXIS_STEP_{index + 1:03d}",
            (16.0, 11.5, 1.1),
            center,
            MATS["jade"],
            target,
            rotation=(0.0, 0.0, math.radians(8.0 + 18.0 * t)),
            reason="representative stage stair art; NON_CANON_PROXY; does not redefine 3600-step Canon",
        )
    add_cube("XTZ_PROMO_AXIS_PLATFORM", (42.0, 34.0, 2.2), (-285.0, 4235.0, 675.2), MATS["jade_warm"], target, rotation=(0.0, 0.0, math.radians(24.0)))
    for x in (-299.0, -271.0):
        add_cube(f"XTZ_PROMO_AXIS_GATE_COLUMN_{int(x)}", (3.2, 3.2, 18.0), (x, 4250.0, 685.0), MATS["vermilion"], target)
    roof_pair("XTZ_PROMO_AXIS_GATE_ROOF", (-285.0, 4250.0), 38.0, 13.0, 695.0, target, 0.75)
    add_cube("XTZ_PROMO_AXIS_GATE_BEAM", (33.0, 2.0, 2.5), (-285.0, 4250.0, 690.0), MATS["gold"], target)


def build_xuantian_hall_hero() -> None:
    target = collection("XTZ_PROMO_XuantianHallHero")
    source = bpy.data.objects.get("XTZ_V02_B1_XTZ-BLD-002_玄天殿")
    if source:
        source.hide_render = True
        source["xtz_promo_replaced_by"] = "NON_CANON_PROXY art inside unchanged B1 envelope"
    # Everything remains inside the locked 98×76×45m B1 envelope at (0,9310,1610).
    add_cube("XTZ_PROMO_HALL_PODIUM", (98.0, 76.0, 6.0), (0.0, 9310.0, 1613.0), MATS["jade_warm"], target)
    add_cube("XTZ_PROMO_HALL_BODY", (78.0, 54.0, 24.0), (0.0, 9310.0, 1628.0), MATS["vermilion"], target)
    for x in (-32.0, -21.0, -10.0, 10.0, 21.0, 32.0):
        add_cylinder(f"XTZ_PROMO_HALL_COLUMN_{int(x):+03d}", 1.25, 23.0, (x, 9282.0, 1628.5), MATS["gold"], target, 12)
    roof_pair("XTZ_PROMO_HALL_ROOF_LOWER", (0.0, 9310.0), 94.0, 64.0, 1642.0, target, 1.25)
    roof_pair("XTZ_PROMO_HALL_ROOF_UPPER", (0.0, 9311.0), 72.0, 44.0, 1648.0, target, 1.0)
    add_cube("XTZ_PROMO_HALL_PLAQUE", (16.0, 1.0, 4.0), (0.0, 9281.5, 1638.0), MATS["jade_warm"], target)
    add_cube("XTZ_PROMO_HALL_PLAQUE_GOLD", (12.0, 0.3, 0.8), (0.0, 9280.9, 1638.0), MATS["gold"], target)
    # Forecourt uses the existing peak-top surface only as a shot-local visible platform.
    add_cube("XTZ_PROMO_HALL_FORECOURT", (92.0, 72.0, 2.0), (0.0, 9240.0, 1608.0), MATS["jade"], target)
    for index in range(10):
        y = 9188.0 + index * 5.2
        z = 1597.0 + index * 1.1
        add_cube(f"XTZ_PROMO_HALL_STEP_{index + 1:02d}", (38.0, 6.0, 1.2), (0.0, y, z), MATS["jade_warm"], target)


def point_rotation(location, target):
    return (Vector(target) - Vector(location)).to_track_quat("-Z", "Y")


def add_camera(name: str, lens: float) -> bpy.types.Object:
    target = collection("XTZ_PROMO_Cameras")
    data = bpy.data.cameras.get(name + "_DATA") or bpy.data.cameras.new(name + "_DATA")
    data.lens = lens
    data.sensor_width = 36.0
    data.clip_start = 0.2
    data.clip_end = 30000.0
    camera = bpy.data.objects.get(name)
    if camera is None:
        camera = bpy.data.objects.new(name, data)
        target.objects.link(camera)
    camera.rotation_mode = "QUATERNION"
    tag(camera, "real-DJI shot camera proxy; independent from Canon")
    camera["xtz_lens_equivalent_mm"] = lens
    camera["xtz_motion_rule"] = "separated planned position / gimbal look direction / eased speed; no FPV"
    return camera


def key_camera(camera, frame: int, location, target) -> None:
    camera.location = location
    camera.rotation_quaternion = point_rotation(location, target)
    camera.keyframe_insert("location", frame=frame)
    camera.keyframe_insert("rotation_quaternion", frame=frame)


def set_interpolation(camera: bpy.types.Object, mode="BEZIER") -> None:
    if not camera.animation_data or not camera.animation_data.action:
        return
    for curve in camera.animation_data.action.fcurves:
        for point in curve.keyframe_points:
            point.interpolation = mode
            if mode == "BEZIER":
                point.handle_left_type = "AUTO_CLAMPED"
                point.handle_right_type = "AUTO_CLAMPED"


def animate_authored_camera(shot_id: str, positions, targets) -> None:
    config = SHOTS[shot_id]
    camera = add_camera("XTZ_PROMO_CAM_" + shot_id.upper(), config["lens"])
    end = int(config["duration_s"] * FPS)
    count = len(positions)
    for index, (location, target) in enumerate(zip(positions, targets)):
        frame = 1 + round(index * (end - 1) / (count - 1))
        key_camera(camera, frame, location, target)
    set_interpolation(camera, "BEZIER")
    camera["xtz_shot_id"] = shot_id
    camera["xtz_duration_s"] = config["duration_s"]


def animate_from_accepted_v02(shot_id: str, source_start: int, source_end: int) -> None:
    source = bpy.data.objects["XTZ_V02_CAM_DJI_28MM"]
    config = SHOTS[shot_id]
    camera = add_camera("XTZ_PROMO_CAM_" + shot_id.upper(), config["lens"])
    end = int(config["duration_s"] * FPS)
    samples = 19
    for index in range(samples):
        t = index / (samples - 1)
        source_frame = round(source_start + (source_end - source_start) * t)
        bpy.context.scene.frame_set(source_frame)
        bpy.context.view_layer.update()
        matrix = source.matrix_world.copy()
        frame = 1 + round((end - 1) * t)
        camera.location = matrix.translation
        camera.rotation_quaternion = matrix.to_quaternion()
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_quaternion", frame=frame)
    set_interpolation(camera, "BEZIER")
    camera["xtz_shot_id"] = shot_id
    camera["xtz_duration_s"] = config["duration_s"]
    camera["xtz_inheritance"] = f"direct world-transform resample of accepted V0.2 camera frames {source_start}-{source_end}"


def build_cameras() -> None:
    animate_authored_camera(
        "shot_01_establishing",
        [
            (2500.0, 900.0, 2050.0),
            (2250.0, 1450.0, 2110.0),
            (1960.0, 2100.0, 2190.0),
            (1630.0, 2750.0, 2260.0),
            (1350.0, 3300.0, 2310.0),
        ],
        [
            (0.0, 7350.0, 1170.0),
            (0.0, 7550.0, 1210.0),
            (0.0, 7800.0, 1260.0),
            (0.0, 8050.0, 1310.0),
            (0.0, 8350.0, 1360.0),
        ],
    )
    animate_from_accepted_v02("shot_02_gate_reveal", 1, 193)
    animate_from_accepted_v02("shot_03_gate_crossing", 193, 337)
    animate_authored_camera(
        "shot_04_inner_axis",
        [
            (25.0, 3830.0, 675.0),
            (-20.0, 3910.0, 687.0),
            (-80.0, 4010.0, 703.0),
            (-145.0, 4110.0, 721.0),
            (-205.0, 4180.0, 738.0),
        ],
        [
            (-110.0, 4030.0, 670.0),
            (-160.0, 4100.0, 680.0),
            (-235.0, 4200.0, 691.0),
            (-285.0, 4250.0, 695.0),
            (-330.0, 4330.0, 715.0),
        ],
    )
    animate_authored_camera(
        "shot_05_xuantian_peak",
        [
            (-900.0, 6800.0, 1420.0),
            (-760.0, 7150.0, 1445.0),
            (-600.0, 7500.0, 1475.0),
            (-440.0, 7820.0, 1510.0),
            (-300.0, 8100.0, 1540.0),
        ],
        [
            (-120.0, 9050.0, 1470.0),
            (-80.0, 9160.0, 1485.0),
            (-30.0, 9280.0, 1500.0),
            (0.0, 9350.0, 1515.0),
            (0.0, 9350.0, 1530.0),
        ],
    )
    animate_authored_camera(
        "shot_06_xuantian_hall",
        [
            (260.0, 8820.0, 1560.0),
            (220.0, 8925.0, 1578.0),
            (165.0, 9040.0, 1595.0),
            (105.0, 9125.0, 1610.0),
            (70.0, 9165.0, 1622.0),
        ],
        [
            (0.0, 9300.0, 1628.0),
            (0.0, 9305.0, 1632.0),
            (0.0, 9310.0, 1636.0),
            (0.0, 9310.0, 1638.0),
            (0.0, 9310.0, 1638.0),
        ],
    )


def setup_world() -> None:
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.render.fps = FPS
    scene.render.fps_base = 1.0
    scene.world.color = (0.48, 0.68, 0.82)
    scene.world.use_nodes = True
    nodes = scene.world.node_tree.nodes
    links = scene.world.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputWorld")
    background = nodes.new("ShaderNodeBackground")
    background.inputs["Strength"].default_value = 0.55
    sky = nodes.new("ShaderNodeTexSky")
    sky.sky_type = "NISHITA"
    sky.sun_elevation = math.radians(22.0)
    sky.sun_rotation = math.radians(135.0)
    sky.altitude = 900.0
    sky.air_density = 0.85
    sky.dust_density = 0.25
    links.new(sky.outputs["Color"], background.inputs["Color"])
    links.new(background.outputs["Background"], output.inputs["Surface"])
    for obj in list(bpy.data.objects):
        if obj.name.startswith("XTZ_PROMO_LIGHT_"):
            bpy.data.objects.remove(obj, do_unlink=True)
    sun_data = bpy.data.lights.new("XTZ_PROMO_LIGHT_SUN_DATA", "SUN")
    sun_data.energy = 2.2
    sun_data.angle = math.radians(4.0)
    sun = bpy.data.objects.new("XTZ_PROMO_LIGHT_SUN", sun_data)
    collection("XTZ_PROMO_Lighting").objects.link(sun)
    sun.rotation_euler = (math.radians(35.0), math.radians(-18.0), math.radians(-35.0))
    tag(sun, "shot lighting proxy")
    scene["xtz_project"] = "Promo Film 01《玄天宗·入宗》"
    scene["xtz_production_mode"] = "SHOT-FIRST VIRTUAL PRODUCTION"
    scene["xtz_base_scene"] = "Digital Twin V0.2.2 COMPLETED"
    scene["xtz_xuantian_peak_lock"] = "LOCKED_VISUALLY_VALIDATED; geometry untouched"


def setup_scene() -> None:
    if not bpy.data.filepath:
        raise RuntimeError("Open the accepted V0.2 blend before setup")
    setup_materials()
    recolor_base_scene()
    setup_world()
    build_clouds()
    build_vegetation()
    build_gate_dressing()
    build_inner_axis_hero()
    build_xuantian_hall_hero()
    build_cameras()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(PRODUCTION_BLEND))
    print(f"[promo] production blend saved: {PRODUCTION_BLEND}")


def camera_for(shot_id: str) -> bpy.types.Object:
    return bpy.data.objects["XTZ_PROMO_CAM_" + shot_id.upper()]


def configure_workbench(scene) -> None:
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.display.shading.light = "STUDIO"
    scene.display.shading.studio_light = "paint.sl"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.background_type = "WORLD"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "WORLD"
    scene.display.shading.curvature_ridge_factor = 1.5
    scene.display.shading.curvature_valley_factor = 1.1
    scene.world.color = (0.46, 0.66, 0.80)


def configure_eevee(scene) -> None:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.look = "AgX - Medium High Contrast"


def render_shot(shot_id: str) -> None:
    config = SHOTS[shot_id]
    shot_dir = OUTPUT / shot_id
    key_dir = shot_dir / "keyframes"
    shot_dir.mkdir(parents=True, exist_ok=True)
    key_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.camera = camera_for(shot_id)
    scene.frame_start = 1
    scene.frame_end = config["duration_s"] * FPS
    scene.render.fps = FPS

    configure_workbench(scene)
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    scene.render.filepath = str(shot_dir / "blender_previz.mp4")
    bpy.ops.render.render(animation=True)
    print(f"[promo] previz rendered: {scene.render.filepath}")

    configure_eevee(scene)
    frames = ((1, "start"), ((scene.frame_end + 1) // 2, "middle"), (scene.frame_end, "end"))
    for frame, label in frames:
        scene.frame_set(frame)
        scene.render.filepath = str(key_dir / f"{label}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[promo] keyframe rendered: {scene.render.filepath}")


def render_selected() -> None:
    requested = os.environ.get("XTZ_PROMO_SHOT", "all").strip().lower()
    selected = list(SHOTS) if requested == "all" else [requested]
    for shot_id in selected:
        if shot_id not in SHOTS:
            raise RuntimeError(f"Unknown XTZ_PROMO_SHOT: {shot_id}")
        render_shot(shot_id)
    bpy.ops.wm.save_as_mainfile(filepath=str(PRODUCTION_BLEND))


def write_camera_manifest() -> None:
    result = {"schema_version": "1.0", "fps": FPS, "shots": {}}
    scene = bpy.context.scene
    for shot_id, config in SHOTS.items():
        camera = camera_for(shot_id)
        samples = []
        for frame in (1, (config["duration_s"] * FPS + 1) // 2, config["duration_s"] * FPS):
            scene.frame_set(frame)
            samples.append(
                {
                    "frame": frame,
                    "location_m": [round(v, 4) for v in camera.matrix_world.translation],
                    "rotation_quaternion": [round(v, 8) for v in camera.matrix_world.to_quaternion()],
                }
            )
        result["shots"][shot_id] = {
            "duration_s": config["duration_s"],
            "lens_equivalent_mm": config["lens"],
            "camera": camera.name,
            "inheritance": camera.get("xtz_inheritance", "authored real-DJI shot path proxy"),
            "samples": samples,
        }
    (OUTPUT / "camera_manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    mode = os.environ.get("XTZ_PROMO_MODE", "all").strip().lower()
    if mode in {"all", "setup"}:
        setup_scene()
    if mode in {"all", "render"}:
        render_selected()
    write_camera_manifest()


if __name__ == "__main__":
    main()
