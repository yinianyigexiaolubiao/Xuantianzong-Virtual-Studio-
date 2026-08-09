from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from v0_2_common import (
    FRAME_END,
    FRAME_START,
    FPS,
    ROAD_DETAIL_XY,
    ROOT,
    camera_metrics,
    camera_samples,
    catmull_rom,
    load_json,
    rounded,
    terrain_height,
    write_json,
)


PROXY = "NON_CANON_PROXY"
LOCKED = "LOCKED_GEOMETRY_VALIDATED"
OUTPUT_DIR = ROOT / "build" / "v0.2"


def collection(name: str):
    value = bpy.data.collections.get(name)
    if value is None:
        value = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(value)
    return value


def move_to(obj, target):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    target.objects.link(obj)


def material(name: str, rgba):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.metallic = 0.0
    mat.roughness = 0.82
    return mat


MATS = {}


def setup_materials():
    MATS.update(
        terrain=material("XTZ_V02_MAT_TERRAIN", (0.46, 0.50, 0.53, 1.0)),
        rock=material("XTZ_V02_MAT_ROCK", (0.38, 0.42, 0.45, 1.0)),
        road=material("XTZ_V02_MAT_ROAD", (0.66, 0.62, 0.53, 1.0)),
        jade=material("XTZ_V02_MAT_JADE", (0.88, 0.90, 0.89, 1.0)),
        sword=material("XTZ_V02_MAT_SWORD", (0.70, 0.73, 0.74, 1.0)),
        xuan=material("XTZ_V02_MAT_XUANTIAN", (0.31, 0.35, 0.38, 1.0)),
        core=material("XTZ_V02_MAT_CORE", (0.74, 0.66, 0.45, 1.0)),
    )


def tag(obj, status=PROXY, reason="V0.2 engineering proxy"):
    obj["xtz_status"] = status
    obj["xtz_geometry_status"] = status
    obj["xtz_reason"] = reason
    return obj


def add_cube(name, dimensions, location, target, mat=None, status=PROXY, reason="V0.2 envelope proxy"):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    tag(obj, status, reason)
    if mat is not None:
        obj.data.materials.append(mat)
    return obj


def configure_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.render.fps = FPS
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.world.color = (0.80, 0.84, 0.88)
    scene["xtz_project"] = "Xuantianzong Virtual Studio"
    scene["xtz_milestone"] = "Digital Twin V0.2.1 Visual Acceptance Repair"
    scene["xtz_proxy_policy"] = PROXY
    scene["xtz_f1_inheritance"] = "continuous terrain / west-east ridge chains / central valley / heavy inverted Xuantian Peak"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.materials):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def build_terrain():
    target = collection("XTZ_V02_Terrain")
    step = 50
    xs = list(range(-4000, 4001, step))
    ys = list(range(0, 12001, step))
    verts = [(float(x), float(y), terrain_height(float(x), float(y))) for y in ys for x in xs]
    width = len(xs)
    faces = []
    for row in range(len(ys) - 1):
        for col in range(width - 1):
            a = row * width + col
            faces.append((a, a + 1, a + 1 + width, a + width))
    mesh = bpy.data.meshes.new("XTZ_V02_F1_CONTINUOUS_TERRAIN_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("XTZ_V02_F1_CONTINUOUS_TERRAIN", mesh)
    target.objects.link(obj)
    tag(obj, PROXY, "F1-inherited deterministic 50m continuous terrain massing; not Canon surface")
    obj["xtz_grid_step_m"] = step
    obj["xtz_west_chain"] = "天剑峰→镇岳峰→天工峰→灵兽峰"
    obj["xtz_east_chain"] = "寒渊峰→紫微峰→丹霞峰→万木峰"
    obj["xtz_has_valley"] = True
    obj["xtz_has_gate_pass"] = True
    obj.data.materials.append(MATS["terrain"])
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    return obj


def build_peak_anchors(peaks_data):
    target = collection("XTZ_V02_PeakAnchors")
    anchors = []
    for peak in peaks_data["peaks"]:
        x, y = peak["center_km"]
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(x * 1000.0, y * 1000.0, peak["summit_elevation_m"]))
        obj = bpy.context.object
        obj.name = f"XTZ_V02_PEAK_ANCHOR_{peak['id']}_{peak['name']}"
        move_to(obj, target)
        obj["xtz_asset_id"] = peak["id"]
        obj["xtz_name"] = peak["name"]
        obj["xtz_formal_peak"] = True
        obj["xtz_floating"] = bool(peak.get("floating"))
        obj["xtz_anchor_status"] = "CANON_A1_LOCKED"
        obj["xtz_summit_elevation_m"] = peak["summit_elevation_m"]
        anchors.append(obj)
    return anchors


def build_xuantian_peak(peaks_data):
    data = next(p for p in peaks_data["peaks"] if p.get("floating"))
    target = collection("XTZ_V02_XuantianPeak")
    cx, cy = (data["center_km"][0] * 1000.0, data["center_km"][1] * 1000.0)
    ring_specs = [
        (1210.0, 38.0, 28.0, 30.0, -12.0),
        (1270.0, 110.0, 82.0, 48.0, -18.0),
        (1335.0, 205.0, 155.0, -42.0, 20.0),
        (1400.0, 325.0, 245.0, 42.0, -24.0),
        (1460.0, 450.0, 330.0, -24.0, 18.0),
        (1515.0, 560.0, 410.0, 0.0, 0.0),
    ]
    count = 28
    verts = []
    for ring_index, (z, rx, ry, ox, oy) in enumerate(ring_specs):
        for i in range(count):
            angle = 2.0 * math.pi * i / count
            irregular = 0.82 + 0.11 * math.sin(i * 2.17 + ring_index * 0.61) + 0.06 * math.sin(i * 0.83 - ring_index)
            if ring_index == len(ring_specs) - 1 and i in (0, count // 2):
                irregular = 1.0
            local_z = z + (0.0 if ring_index == 0 else 13.0 * math.sin(i * 1.43 + ring_index * 0.8))
            verts.append((cx + ox + rx * irregular * math.cos(angle), cy + oy + ry * irregular * math.sin(angle), local_z))
    faces = []
    for ring in range(len(ring_specs) - 1):
        base = ring * count
        nxt = (ring + 1) * count
        for i in range(count):
            j = (i + 1) % count
            faces.append((base + i, base + j, nxt + j, nxt + i))
    top_center = len(verts)
    verts.append((cx - 35.0, cy + 20.0, 1582.0))
    base = (len(ring_specs) - 1) * count
    for i in range(count):
        faces.append((base + i, base + (i + 1) % count, top_center))
    mesh = bpy.data.meshes.new("XTZ_V02_XUANTIAN_HEAVY_INVERTED_BODY_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    body = bpy.data.objects.new("XTZ_V02_XUANTIAN_HEAVY_INVERTED_BODY", mesh)
    target.objects.link(body)
    tag(body, PROXY, "Heavy irregular inverted silhouette inside locked Xuantian envelope")
    body["xtz_asset_id"] = data["id"]
    body["xtz_plan_envelope_m"] = "1450x1050"
    body["xtz_deepest_spire_m"] = 1210.0
    body.data.materials.append(MATS["xuan"])

    def crag_mesh(name, center, base_z, rx, ry, shoulder_z, top_z, sides, phase):
        x, y = center
        crag_verts = []
        for level, (z, factor) in enumerate(((base_z, 1.0), (shoulder_z, 0.52))):
            for i in range(sides):
                angle = 2.0 * math.pi * i / sides
                irregular = 0.78 + 0.16 * math.sin(i * 1.71 + phase + level) + 0.05 * math.sin(i * 3.13 - phase)
                crag_verts.append((x + rx * factor * irregular * math.cos(angle), y + ry * factor * irregular * math.sin(angle), z + 8.0 * math.sin(i * 1.27 + phase)))
        apex = len(crag_verts)
        crag_verts.append((x + rx * 0.13 * math.sin(phase), y + ry * 0.11 * math.cos(phase), top_z))
        crag_faces = []
        for i in range(sides):
            j = (i + 1) % sides
            crag_faces.append((i, j, sides + j, sides + i))
            crag_faces.append((sides + i, sides + j, apex))
        crag_mesh_data = bpy.data.meshes.new(name + "_MESH")
        crag_mesh_data.from_pydata(crag_verts, [], crag_faces)
        crag_mesh_data.update()
        obj = bpy.data.objects.new(name, crag_mesh_data)
        target.objects.link(obj)
        tag(obj, PROXY, "Asymmetric natural crown crag; locked Xuantian envelope unchanged")
        obj["xtz_asset_id"] = data["id"]
        obj["xtz_formal_peak"] = False
        obj.data.materials.append(MATS["xuan"])
        return obj

    crown_specs = [
        ((cx - 365.0, cy - 45.0), 1448.0, 210.0, 165.0, 1555.0, 1628.0, 11, 0.4),
        ((cx - 175.0, cy + 35.0), 1445.0, 245.0, 190.0, 1578.0, 1670.0, 13, 1.2),
        ((cx + 65.0, cy + 105.0), 1440.0, 270.0, 210.0, 1585.0, 1680.0, 15, 2.0),
        ((cx + 285.0, cy - 25.0), 1450.0, 220.0, 175.0, 1565.0, 1652.0, 12, 2.8),
        ((cx + 445.0, cy + 85.0), 1460.0, 125.0, 125.0, 1545.0, 1615.0, 9, 3.6),
    ]
    crowns = [crag_mesh(f"XTZ_V02_XUANTIAN_NATURAL_CROWN_{index:02d}", *spec) for index, spec in enumerate(crown_specs, 1)]

    def secondary_spire(name, tip, ring_center, rx, ry, ring_z, phase):
        sides = 11
        spire_verts = [tip]
        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            irregular = 0.78 + 0.16 * math.sin(i * 1.83 + phase)
            spire_verts.append((ring_center[0] + rx * irregular * math.cos(angle), ring_center[1] + ry * irregular * math.sin(angle), ring_z + 9.0 * math.sin(i * 1.19 + phase)))
        faces = [(0, 1 + i, 1 + (i + 1) % sides) for i in range(sides)]
        spire_mesh = bpy.data.meshes.new(name + "_MESH")
        spire_mesh.from_pydata(spire_verts, [], faces)
        spire_mesh.update()
        obj = bpy.data.objects.new(name, spire_mesh)
        target.objects.link(obj)
        tag(obj, PROXY, "Secondary inverted rock convergence; Xuantian Canon envelope unchanged")
        obj["xtz_asset_id"] = data["id"]
        obj.data.materials.append(MATS["xuan"])
        return obj

    secondary = [
        secondary_spire("XTZ_V02_XUANTIAN_SECONDARY_SPIRE_01", (cx - 300.0, cy - 10.0, 1288.0), (cx - 205.0, cy, 0.0), 220.0, 180.0, 1475.0, 0.7),
        secondary_spire("XTZ_V02_XUANTIAN_SECONDARY_SPIRE_02", (cx + 330.0, cy + 35.0, 1322.0), (cx + 220.0, cy + 20.0, 0.0), 205.0, 165.0, 1482.0, 2.1),
    ]
    return body, crowns + secondary


def add_rock(name, location, scale, rotation, target):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    tag(obj, PROXY, "Mountain-pass rock mass integrated with continuous terrain")
    obj.data.materials.append(MATS["rock"])
    return obj


def build_gate_pass_massing():
    target = collection("XTZ_V02_GatePassMassing")
    specs = [
        ("WEST_A", (-155.0, 3690.0, 650.0), (95.0, 150.0, 75.0), (0.1, 0.2, 0.05)),
        ("WEST_B", (-175.0, 3780.0, 665.0), (130.0, 210.0, 95.0), (-0.1, 0.15, -0.18)),
        ("EAST_A", (160.0, 3705.0, 655.0), (105.0, 165.0, 82.0), (-0.08, 0.12, -0.04)),
        ("EAST_B", (205.0, 3790.0, 678.0), (145.0, 225.0, 105.0), (0.05, -0.18, 0.15)),
        ("WEST_FORE", (-265.0, 3480.0, 635.0), (190.0, 300.0, 100.0), (0.12, 0.05, 0.1)),
        ("EAST_FORE", (290.0, 3500.0, 640.0), (210.0, 320.0, 110.0), (-0.1, 0.08, -0.12)),
    ]
    return [add_rock(f"XTZ_V02_PASS_ROCK_{label}", loc, scale, rot, target) for label, loc, scale, rot in specs]


def build_ribbon(name, points, widths, target, mat, reason):
    verts = []
    faces = []
    for i, point in enumerate(points):
        p = Vector(point)
        before = Vector(points[max(0, i - 1)])
        after = Vector(points[min(len(points) - 1, i + 1)])
        tangent = after - before
        tangent.z = 0.0
        if tangent.length == 0.0:
            tangent = Vector((0.0, 1.0, 0.0))
        tangent.normalize()
        side = Vector((-tangent.y, tangent.x, 0.0))
        half = widths[i] / 2.0
        verts.extend([tuple(p - side * half), tuple(p + side * half)])
        if i > 0:
            base = (i - 1) * 2
            faces.append((base, base + 1, base + 3, base + 2))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    target.objects.link(obj)
    tag(obj, PROXY, reason)
    obj.data.materials.append(mat)
    return obj


def build_routes(road_data, axis_data):
    target = collection("XTZ_V02_Routes")
    control = []
    for y, x in ROAD_DETAIL_XY:
        z = terrain_height(x, y) + 0.8
        control.append((x, y, z))
    smooth = catmull_rom(control, 18)
    smooth = [(x, y, terrain_height(x, y) + 0.8) for x, y, _ in smooth]
    widths = []
    for _, y, _ in smooth:
        widths.append(12.0 if y >= 3520.0 else 6.0)
    road = build_ribbon("XTZ_V02_ANCIENT_ROAD_SMOOTH_PROXY", smooth, widths, target, MATS["road"], "Smooth terrain-conforming visible road through locked A5-A8 control regions")
    road["xtz_asset_id"] = road_data["asset_id"]
    road["xtz_locked_controls"] = "A5,A6,A7,A8"

    internal_control = [(0.0, 3700.0, 611.0), (18.0, 3800.0, 625.0), (-45.0, 3920.0, 642.0), (-130.0, 4070.0, 658.0), (-300.0, 4250.0, 674.0)]
    internal = catmull_rom(internal_control, 22)
    internal = [(x, y, max(z, terrain_height(x, y) + 0.8)) for x, y, z in internal]
    axis = build_ribbon("XTZ_V02_INTERIOR_ROUTE_SMOOTH_PROXY", internal, [8.0] * len(internal), target, MATS["road"], "First 500m interior route; A1 stage-1 endpoint remains locked")
    axis["xtz_asset_id"] = axis_data["asset_id"]
    axis["xtz_locked_start"] = "A1 node 0 (0,3700,610)"
    axis["xtz_locked_end_dependency"] = "A1 node 1 (-380,4250,674)"
    return road, axis, smooth, internal


def build_gate(gate_data):
    target = collection("XTZ_V02_XuanyueGate")
    x, y = (gate_data["world_anchor"]["center_km"][0] * 1000.0, gate_data["world_anchor"]["center_km"][1] * 1000.0)
    z = float(gate_data["world_anchor"]["ground_elevation_m"])
    width = float(gate_data["dimensions_m"]["width"])
    depth = float(gate_data["dimensions_m"]["depth"])
    height = float(gate_data["dimensions_m"]["height"])
    opening_w = float(gate_data["main_gate"]["clear_width"])
    opening_h = float(gate_data["main_gate"]["clear_height"])
    side_w = (width - opening_w) / 2.0
    left = add_cube("XTZ_V02_GATE_BODY_LEFT", (side_w, depth, height), (x - (opening_w + side_w) / 2.0, y, z + height / 2.0), target, MATS["jade"], LOCKED, "Locked gate body envelope")
    right = add_cube("XTZ_V02_GATE_BODY_RIGHT", (side_w, depth, height), (x + (opening_w + side_w) / 2.0, y, z + height / 2.0), target, MATS["jade"], LOCKED, "Locked gate body envelope")
    lintel_h = height - opening_h
    lintel = add_cube("XTZ_V02_GATE_BODY_LINTEL", (opening_w, depth, lintel_h), (x, y, z + opening_h + lintel_h / 2.0), target, MATS["jade"], LOCKED, "Locked gate body envelope")
    for obj in (left, right, lintel):
        obj["xtz_asset_id"] = gate_data["asset_id"]
        obj["xtz_anchor_status"] = "CANON_A1_LOCKED"
    eave = add_cube("XTZ_V02_GATE_EAVE_PROXY", (58.0, 21.0, 2.2), (x, y, z + 32.0), target, MATS["jade"], PROXY, "Graybox eave; locked body bbox remains separate")
    platform = add_cube("XTZ_V02_GATE_FORECOURT_PROXY", (84.0, 32.0, 1.2), (x, y - 25.0, z + 0.6), target, MATS["jade"], PROXY, "Locked plan size with proxy thickness")
    return [left, right, lintel], [eave, platform]


def sword_blade_mesh(name, x, y, base_z, data, target):
    height = float(data["height_m"])
    blade_len = float(data["blade_length_m"])
    width = sum(data["blade_max_width_m"]) / 2.0
    thickness = float(data["body_max_thickness_m"])
    blade_bottom = base_z + height - blade_len
    levels = [
        (blade_bottom, width * 0.92),
        (base_z + height - 8.0, width),
        (base_z + height - 3.0, width * 0.62),
        (base_z + height, 0.0),
    ]
    verts = []
    for z, level_width in levels:
        half = level_width / 2.0
        verts.extend([
            (x - half, y, z),
            (x, y - thickness / 2.0, z),
            (x + half, y, z),
            (x, y + thickness / 2.0, z),
        ])
    faces = []
    for level in range(len(levels) - 1):
        a, b = level * 4, (level + 1) * 4
        for side in range(4):
            faces.append((a + side, a + (side + 1) % 4, b + (side + 1) % 4, b + side))
    faces.append((0, 1, 2, 3))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    target.objects.link(obj)
    tag(obj, PROXY, "V10 double-edged straight-sword graybox silhouette; dimensions locked")
    obj.data.materials.append(MATS["sword"])
    return obj, blade_bottom


def build_swords(gate_data):
    target = collection("XTZ_V02_TwinSwords")
    data = gate_data["twin_swords"]
    anchor_x = gate_data["world_anchor"]["center_km"][0] * 1000.0
    anchor_y = gate_data["world_anchor"]["center_km"][1] * 1000.0
    ground = float(gate_data["world_anchor"]["ground_elevation_m"])
    base_h = float(data["base_height_m"])
    front = sum(data["front_offset_m"]) / 2.0
    objects = []
    for side, offset in (("WEST", data["axes_local_x_m"][0]), ("EAST", data["axes_local_x_m"][1])):
        x = anchor_x + float(offset)
        y = anchor_y - front
        base = add_cube(f"XTZ_V02_SWORD_{side}_BASE", (*data["base_plan_m"], base_h), (x, y, ground + base_h / 2.0), target, MATS["jade"], PROXY, "Locked base plan/height, graybox form")
        sword_z = ground + base_h
        blade, blade_bottom = sword_blade_mesh(f"XTZ_V02_SWORD_{side}_BLADE", x, y, sword_z, data, target)
        pommel_h = float(data["pommel_m"])
        pommel = add_cube(f"XTZ_V02_SWORD_{side}_POMMEL", (2.8, 1.8, pommel_h), (x, y, sword_z + pommel_h / 2.0), target, MATS["sword"], PROXY, "V10 sword pommel proxy")
        grip_bottom = sword_z + pommel_h
        guard_z = blade_bottom - 0.6
        grip = add_cube(f"XTZ_V02_SWORD_{side}_GRIP", (1.8, 1.4, guard_z - grip_bottom), (x, y, (guard_z + grip_bottom) / 2.0), target, MATS["sword"], PROXY, "V10 sword grip proxy")
        guard = add_cube(f"XTZ_V02_SWORD_{side}_GUARD", (float(data["hilt_guard_m"]), 2.2, 1.6), (x, y, guard_z + 0.8), target, MATS["sword"], PROXY, "V10 sword guard proxy with readable transverse silhouette")
        for obj in (base, blade, pommel, grip, guard):
            obj["xtz_asset_id"] = data["asset_id"]
            obj["xtz_sword_side"] = side
            obj["xtz_locked_height_m"] = data["height_m"]
            obj["xtz_locked_axis_distance_m"] = data["axis_distance_m"]
        objects.extend([base, blade, pommel, grip, guard])
    return objects


def build_core_assets(key_assets):
    target = collection("XTZ_V02_B1_Core")
    built = []
    for asset in key_assets["assets"]:
        if not asset.get("v0_1_build") or "plan_m" not in asset:
            continue
        x, y = asset["coord_km"]
        w, d = asset["plan_m"]
        h = asset["height_m"]
        obj = add_cube(f"XTZ_V02_B1_{asset['id']}_{asset['name']}", (w, d, h), (x * 1000.0, y * 1000.0, asset["elevation_m"] + h / 2.0), target, MATS["core"], PROXY, "B1 locked anchor/envelope; building art remains proxy")
        obj["xtz_asset_id"] = asset["id"]
        obj["xtz_name"] = asset["name"]
        obj["xtz_anchor_status"] = "CANON_B1_LOCKED"
        if asset.get("visual_rank"):
            obj["xtz_visual_rank"] = asset["visual_rank"]
        built.append(obj)
    return built


def animate_camera():
    target = collection("XTZ_V02_Cameras")
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    body = bpy.context.object
    body.name = "XTZ_V02_DJI_BODY"
    move_to(body, target)
    tag(body, PROXY, "DJI position and body-yaw animation rig")
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    gimbal = bpy.context.object
    gimbal.name = "XTZ_V02_DJI_GIMBAL"
    move_to(gimbal, target)
    gimbal.parent = body
    tag(gimbal, PROXY, "Independent gimbal target/orientation animation")
    camera_data = bpy.data.cameras.new("XTZ_V02_CAM_DJI_28MM_DATA")
    camera_data.lens = 28.0
    camera_data.sensor_width = 36.0
    camera_data.clip_start = 0.2
    camera_data.clip_end = 20000.0
    camera = bpy.data.objects.new("XTZ_V02_CAM_DJI_28MM", camera_data)
    target.objects.link(camera)
    camera.parent = gimbal
    tag(camera, PROXY, "28mm-equivalent engineering DJI preview")
    camera["xtz_camera_system"] = "DJI physical proxy"
    camera["xtz_curve_separation"] = "body.location / body.yaw / gimbal.rotation / speed profile"

    samples = camera_samples()
    for row in samples:
        frame = row["frame"]
        body.location = row["position"]
        body.rotation_euler = (0.0, 0.0, row["body_yaw_rad"])
        body.keyframe_insert("location", frame=frame)
        body.keyframe_insert("rotation_euler", index=2, frame=frame)
        direction_world = Vector(row["gimbal_target"]) - Vector(row["position"])
        direction_local = direction_world.copy()
        direction_local.rotate(body.rotation_euler.to_matrix().inverted())
        gimbal.rotation_euler = direction_local.to_track_quat("-Z", "Y").to_euler()
        gimbal.keyframe_insert("rotation_euler", frame=frame)
    for obj in (body, gimbal):
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for point in fcurve.keyframe_points:
                    point.interpolation = "LINEAR"
    bpy.context.scene.camera = camera
    return body, gimbal, camera, samples


def add_qc_camera(name, location, target_point, lens=42.0, ortho_scale=None):
    data = bpy.data.cameras.new(name + "_DATA")
    data.lens = lens
    data.sensor_width = 36.0
    data.clip_start = 1.0
    data.clip_end = 25000.0
    if ortho_scale is not None:
        data.type = "ORTHO"
        data.ortho_scale = ortho_scale
    cam = bpy.data.objects.new(name, data)
    collection("XTZ_V02_QC_Cameras").objects.link(cam)
    cam.location = location
    cam.rotation_euler = (Vector(target_point) - cam.location).to_track_quat("-Z", "Y").to_euler()
    tag(cam, PROXY, "Fixed Visual QC camera")
    return cam


def build_qc_cameras():
    specs = [
        ("XTZ_CAM_QC_01_ROAD_TO_GATE", (-520.0, 2700.0, 930.0), (0.0, 3700.0, 626.0), 52.0, None),
        ("XTZ_CAM_QC_02_GATE_FRONT", (0.0, 3475.0, 656.0), (0.0, 3700.0, 630.0), 35.0, None),
        ("XTZ_CAM_QC_03_LEFT_SWORD", (0.0, 3500.0, 650.0), (-34.0, 3700.0, 632.0), 85.0, None),
        ("XTZ_CAM_QC_04_RIGHT_SWORD", (0.0, 3500.0, 650.0), (34.0, 3700.0, 632.0), 85.0, None),
        ("XTZ_CAM_QC_05_GATE_OVERHEAD", (0.0, 3400.0, 1050.0), (0.0, 3700.0, 610.0), 45.0, None),
        ("XTZ_CAM_QC_06_PASS_WHOLE", (0.0, 2700.0, 1220.0), (0.0, 3720.0, 630.0), 48.0, None),
        ("XTZ_CAM_QC_07_POST_GATE_REVERSE", (-20.0, 4200.0, 740.0), (0.0, 3700.0, 625.0), 50.0, None),
        ("XTZ_CAM_QC_08_INTERIOR_TO_XUANTIAN", (-80.0, 3950.0, 690.0), (0.0, 9350.0, 1470.0), 48.0, None),
        ("XTZ_CAM_QC_09_XUANTIAN_SILHOUETTE", (0.0, 5200.0, 950.0), (0.0, 9350.0, 1470.0), 55.0, None),
        ("XTZ_CAM_QC_10_MINI_AERIAL", (2500.0, 1500.0, 3600.0), (0.0, 5700.0, 850.0), 42.0, None),
        ("XTZ_CAM_QC_11_GATE_AND_DISTANT_PEAK", (0.0, 3250.0, 760.0), (0.0, 6000.0, 980.0), 34.0, None),
        ("XTZ_CAM_QC_12_F1_STRATEGIC", (6200.0, -1800.0, 8200.0), (0.0, 6000.0, 900.0), 38.0, None),
    ]
    return [add_qc_camera(*spec) for spec in specs]


def build_specialized_qc_cameras():
    peak_specs = [
        ("XTZ_CAM_XTPEAK_QC_01_GATE_LONG", (0.0, 3920.0, 735.0), (0.0, 9350.0, 1480.0), 62.0, None),
        ("XTZ_CAM_XTPEAK_QC_02_INTERIOR_LONG", (-180.0, 4300.0, 815.0), (0.0, 9350.0, 1480.0), 58.0, None),
        ("XTZ_CAM_XTPEAK_QC_03_FRONT_45", (1850.0, 6100.0, 1320.0), (0.0, 9350.0, 1480.0), 52.0, None),
        ("XTZ_CAM_XTPEAK_QC_04_LOW_ANGLE", (0.0, 7600.0, 1115.0), (0.0, 9350.0, 1480.0), 35.0, None),
    ]
    sword_specs = [
        ("XTZ_CAM_SWORD_QC_01_VALLEY_LONG", (-45.0, 3490.0, 665.0), (0.0, 3700.0, 634.0), 48.0, None),
        ("XTZ_CAM_SWORD_QC_02_GATE_FRONT", (0.0, 3475.0, 690.0), (0.0, 3700.0, 634.0), 52.0, None),
        ("XTZ_CAM_SWORD_QC_03_LEFT_MID", (-34.0, 3610.0, 637.0), (-34.0, 3696.0, 634.0), 35.0, None),
        ("XTZ_CAM_SWORD_QC_04_RIGHT_MID", (34.0, 3610.0, 637.0), (34.0, 3696.0, 634.0), 35.0, None),
    ]
    return [add_qc_camera(*spec) for spec in peak_specs], [add_qc_camera(*spec) for spec in sword_specs]


def bounds_world(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return {
        "min": [min(p[i] for p in points) for i in range(3)],
        "max": [max(p[i] for p in points) for i in range(3)],
    }


def deterministic_snapshot(samples, manifest):
    objects = {}
    for obj in sorted(bpy.data.objects, key=lambda item: item.name):
        state = {
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale),
        }
        if obj.type == "MESH":
            state["dimensions"] = list(obj.dimensions)
            state["bounds"] = bounds_world(obj)
        objects[obj.name] = state
    terrain_controls = []
    for x, y in ((-400, 2800), (300, 3100), (-200, 3350), (0, 3700), (-380, 4250), (-1000, 3700), (1000, 3700), (0, 9350)):
        terrain_controls.append({"xy": [x, y], "height": terrain_height(x, y)})
    return rounded({
        "schema": "v0.2-deterministic-snapshot-1",
        "objects": objects,
        "terrain_control_data": terrain_controls,
        "camera_samples": samples,
        "camera_metrics": camera_metrics(samples),
        "manifest": manifest,
    })


def build_manifest(anchors, core, qc, peak_qc, sword_qc, samples):
    proxies = sorted(obj.name for obj in bpy.data.objects if obj.get("xtz_status") == PROXY)
    return {
        "project": "Xuantianzong Virtual Studio",
        "milestone": "Digital Twin V0.2.1 Visual Acceptance Repair",
        "authority": "V1.6.1 BASE_WORLD_CANON + registered scoped overrides",
        "scope": "final 800-1000m ancient road / Xuanyue mountain pass / gate+swords / first 300-500m interior / distant Xuantian silhouette",
        "formal_peak_count": len(anchors),
        "large_floating_main_peak_count": sum(1 for a in anchors if a.get("xtz_floating")),
        "b1_core_asset_count": len(core),
        "qc_camera_count": len(qc),
        "xuantian_peak_qc_camera_count": len(peak_qc),
        "twin_sword_fixed_qc_camera_count": len(sword_qc),
        "twin_sword_dji_keyframe_qc_count": 2,
        "dji_keyframe_qc_count": 9,
        "camera_frame_count": len(samples),
        "fps": FPS,
        "duration_s": FRAME_END / FPS,
        "locked": {
            "gate_anchor_m": [0.0, 3700.0, 610.0],
            "gate_body_m": [52.0, 18.0, 34.0],
            "central_opening_m": [11.0, 15.0],
            "twin_sword_height_m": 44.0,
            "twin_sword_axis_distance_m": 68.0,
            "xuantian_vertical_m": [1210.0, 1680.0],
        },
        "proxy_policy": PROXY,
        "visual_acceptance_policy": "PENDING_HUMAN_REVIEW unless explicitly approved by a human",
        "non_canon_proxy_objects": proxies,
        "locked_design_not_visually_validated": [],
    }


def main():
    output_blend = Path(os.environ.get("XTZ_V02_OUT_BLEND", OUTPUT_DIR / "xuantianzong_mini_digital_twin_v0.2.blend"))
    snapshot_path = Path(os.environ.get("XTZ_V02_SNAPSHOT", OUTPUT_DIR / "snapshot.json"))
    manifest_path = Path(os.environ.get("XTZ_V02_MANIFEST", OUTPUT_DIR / "manifest.json"))
    output_blend.parent.mkdir(parents=True, exist_ok=True)
    clear_scene()
    configure_scene()
    setup_materials()
    peaks = load_json("peaks.json")
    road = load_json("ancient_road.json")
    axis = load_json("central_axis.json")
    gate = load_json("xuanyue_gate.json")
    key_assets = load_json("key_assets.json")
    build_terrain()
    anchors = build_peak_anchors(peaks)
    build_xuantian_peak(peaks)
    build_gate_pass_massing()
    build_routes(road, axis)
    build_gate(gate)
    build_swords(gate)
    core = build_core_assets(key_assets)
    _, _, _, samples = animate_camera()
    qc = build_qc_cameras()
    peak_qc, sword_qc = build_specialized_qc_cameras()
    manifest = build_manifest(anchors, core, qc, peak_qc, sword_qc, samples)
    snapshot = deterministic_snapshot(samples, manifest)
    write_json(manifest_path, manifest)
    write_json(snapshot_path, snapshot)
    bpy.context.scene["xtz_manifest_sha256"] = hashlib.sha256(json.dumps(rounded(manifest), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
    print(f"[XTZ V0.2] BUILD PASS blend={output_blend} snapshot={snapshot_path} manifest={manifest_path}")


if __name__ == "__main__":
    main()
