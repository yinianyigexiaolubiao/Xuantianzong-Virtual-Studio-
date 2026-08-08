from __future__ import annotations

from typing import Iterable

import bpy
from mathutils import Vector

NON_CANON_PROXY_TAG = "NON_CANON_PROXY"
CANON_A1_CONTROL_TAG = "CANON_A1_CONTROL_CURVE"
CANON_B1_ANCHOR_TAG = "CANON_B1_LOCKED"


def get_or_create_collection(name: str):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def clear_xtz_scene():
    """Delete only XTZ-generated objects, preserving unrelated user content."""
    for obj in list(bpy.data.objects):
        if obj.name.startswith("XTZ_"):
            bpy.data.objects.remove(obj, do_unlink=True)


def move_to_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def add_cube(name, size_xyz, location, collection):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size_xyz
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to_collection(obj, collection)
    return obj


def add_proxy_peak(peak: dict, collection):
    x_km, y_km = peak["center_km"]
    summit = float(peak["summit_elevation_m"])
    core_x_km, core_y_km = peak["core_body_km"]
    floating = bool(peak.get("floating"))
    foot = peak.get("primary_foot_elevation_m")

    if floating:
        deepest = peak.get("deepest_inverted_spire_elevation_m")
        if deepest is not None:
            base_z = float(deepest)
            proxy_height = summit - base_z
            unresolved = False
        else:
            proxy_height = 470.0
            base_z = summit - proxy_height
            unresolved = True
    else:
        if foot is None:
            raise ValueError(f"{peak['name']} missing primary_foot_elevation_m")
        base_z = float(foot)
        proxy_height = max(80.0, summit - base_z)
        unresolved = False

    radius_x = core_x_km * 500.0
    radius_y = core_y_km * 500.0
    bpy.ops.mesh.primitive_cone_add(
        vertices=48,
        radius1=1.0,
        radius2=0.16 if not floating else 0.38,
        depth=1.0,
        location=(x_km * 1000.0, y_km * 1000.0, base_z + proxy_height / 2.0),
    )
    obj = bpy.context.object
    obj.name = f"XTZ_PEAK_{peak['id']}_{peak['name']}"
    obj.scale = (radius_x, radius_y, proxy_height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to_collection(obj, collection)
    obj["xtz_asset_id"] = peak["id"]
    obj["xtz_name"] = peak["name"]
    obj["xtz_role"] = peak.get("role", "")
    obj["xtz_floating"] = floating
    obj["xtz_summit_elevation_m"] = summit
    obj["xtz_geometry_status"] = NON_CANON_PROXY_TAG
    obj["xtz_world_anchor_status"] = "CANON_A1_LOCKED"
    if unresolved:
        obj["xtz_unresolved"] = "Proxy mountain body; retain locked A1 center/envelope and refine geometry later."
    return obj


def build_peaks(peaks_data: dict):
    collection = get_or_create_collection("XTZ_Peaks")
    return [add_proxy_peak(p, collection) for p in peaks_data["peaks"]]


def _add_sword(name, height_m, x_m, y_m, base_z, collection):
    blade_h = height_m * 0.78
    grip_h = height_m * 0.12
    guard_w = height_m * 0.24
    blade = add_cube(f"{name}_Blade", (height_m * 0.085, height_m * 0.025, blade_h), (x_m, y_m, base_z + grip_h + blade_h / 2.0), collection)
    guard = add_cube(f"{name}_Guard", (guard_w, height_m * 0.05, height_m * 0.035), (x_m, y_m, base_z + grip_h), collection)
    grip = add_cube(f"{name}_Grip", (height_m * 0.045, height_m * 0.045, grip_h), (x_m, y_m, base_z + grip_h / 2.0), collection)
    pommel = add_cube(f"{name}_Pommel", (height_m * 0.07, height_m * 0.055, height_m * 0.05), (x_m, y_m, base_z), collection)
    blade["xtz_shape"] = "V10 double-edged straight sword proxy"
    blade["xtz_light_rule"] = "ice-blue only along blade edges/limited array patterns"
    for obj in (blade, guard, grip, pommel):
        obj["xtz_geometry_status"] = NON_CANON_PROXY_TAG
    return [blade, guard, grip, pommel]


def gate_anchor_m(gate_data: dict) -> tuple[float, float, float]:
    anchor = gate_data["world_anchor"]
    x_km, y_km = anchor["center_km"]
    return float(x_km) * 1000.0, float(y_km) * 1000.0, float(anchor["ground_elevation_m"])


def build_gate(gate_data: dict, anchor=None):
    """Build a simple gate proxy at the locked A1 world anchor."""
    collection = get_or_create_collection("XTZ_XuanyueGate")
    if anchor is None:
        anchor = gate_anchor_m(gate_data)

    width = float(gate_data["dimensions_m"]["width"])
    depth = float(gate_data["dimensions_m"]["depth"])
    height = float(gate_data["dimensions_m"]["height"])
    opening_w = float(gate_data["main_gate"]["clear_width"])
    opening_h = float(gate_data["main_gate"]["clear_height"])
    x, y, z = anchor
    side_w = (width - opening_w) / 2.0
    lintel_h = max(4.0, height - opening_h)

    left = add_cube("XTZ_GATE_LeftMass", (side_w, depth, height), (x - (opening_w + side_w) / 2.0, y, z + height / 2.0), collection)
    right = add_cube("XTZ_GATE_RightMass", (side_w, depth, height), (x + (opening_w + side_w) / 2.0, y, z + height / 2.0), collection)
    lintel = add_cube("XTZ_GATE_MainLintel", (opening_w, depth, lintel_h), (x, y, z + opening_h + lintel_h / 2.0), collection)

    platform = gate_data.get("front_platform_m", {})
    if platform:
        add_cube(
            "XTZ_GATE_FrontPlatform",
            (float(platform["width"]), float(platform["depth"]), 1.2),
            (x, y - depth / 2.0 - float(platform["depth"]) / 2.0, z + 0.6),
            collection,
        )

    for obj in (left, right, lintel):
        obj["xtz_asset_id"] = gate_data["asset_id"]
        obj["xtz_geometry_status"] = NON_CANON_PROXY_TAG
        obj["xtz_world_anchor_status"] = gate_data["world_anchor"]["status"]

    swords = gate_data["twin_swords"]
    sword_h = float(swords["height_m"])
    x_axes = [float(v) for v in swords.get("axes_local_x_m", [-sword_h / 2.0, sword_h / 2.0])]
    front_range = swords.get("front_offset_m", [4.0, 4.0])
    front_offset = (float(front_range[0]) + float(front_range[1])) / 2.0
    sword_y = y - front_offset
    base_z = z + float(swords.get("base_height_m", 0.0))

    sword_objects = _add_sword("XTZ_SWORD_WEST", sword_h, x + x_axes[0], sword_y, base_z, collection)
    sword_objects += _add_sword("XTZ_SWORD_EAST", sword_h, x + x_axes[1], sword_y, base_z, collection)
    for obj in sword_objects:
        obj["xtz_asset_id"] = swords["asset_id"]
        obj["xtz_world_anchor_status"] = "CANON_A1_LOCKED_RANGE_MIDPOINT_PROXY"
        obj["xtz_front_offset_m"] = front_offset
    return {"gate_objects": [left, right, lintel], "sword_objects": sword_objects, "anchor": Vector(anchor)}


def build_ancient_road(road_data: dict):
    """Build the locked A1 centerline-control curve from Jieyin Courtyard to Xuanyue Gate."""
    collection = get_or_create_collection("XTZ_AncientRoad")
    control_points = road_data["control_points"]
    points = [
        (
            float(cp["coord_km"][0]) * 1000.0,
            float(cp["coord_km"][1]) * 1000.0,
            float(cp["elev_m"]),
        )
        for cp in control_points
    ]

    curve_data = bpy.data.curves.new("XTZ_ANCIENT_ROAD_A1_ControlCurveData", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = float(road_data["widths_m"]["normal_clear"]) / 2.0
    curve_data.bevel_resolution = 2
    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1.0)

    obj = bpy.data.objects.new("XTZ_ANCIENT_ROAD_A1_CONTROL_CURVE", curve_data)
    collection.objects.link(obj)
    obj["xtz_asset_id"] = road_data["asset_id"]
    obj["xtz_geometry_status"] = CANON_A1_CONTROL_TAG
    obj["xtz_detail_status"] = "REQUIRES_D2_10M_AND_ASSET_1M_DETAIL"
    obj["xtz_control_point_count"] = len(control_points)
    obj["xtz_actual_length_km"] = float(road_data["actual_length_km"])
    obj["xtz_major_switchbacks"] = int(road_data["major_switchbacks"])
    obj["xtz_final_jade_approach_length_m"] = float(road_data["final_jade_approach_length_m"])
    obj["xtz_warning"] = (
        "A0-A8 are locked A1 control points. This polyline is a spatial-control guide, "
        "not the final 6km road-edge geometry."
    )
    return obj, points


def build_axis(axis_data: dict):
    """Build the locked A1 50m-control curve; detailed stair geometry is a later phase."""
    collection = get_or_create_collection("XTZ_CentralAxis")
    nodes = axis_data["axis_nodes_km"]
    elevations = axis_data["axis_node_elevations_m"]
    if len(nodes) != len(elevations):
        raise ValueError("axis_nodes_km and axis_node_elevations_m length mismatch")

    points = [
        (float(x_km) * 1000.0, float(y_km) * 1000.0, float(z_m))
        for (x_km, y_km), z_m in zip(nodes, elevations)
    ]

    curve_data = bpy.data.curves.new("XTZ_AXIS_A1_ControlCurveData", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 4.0
    curve_data.bevel_resolution = 2
    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1.0)

    obj = bpy.data.objects.new("XTZ_AXIS_A1_CONTROL_CURVE", curve_data)
    collection.objects.link(obj)
    obj["xtz_asset_id"] = axis_data["asset_id"]
    obj["xtz_geometry_status"] = CANON_A1_CONTROL_TAG
    obj["xtz_detail_status"] = "REQUIRES_D2_10M_AND_ASSET_1M_DETAIL"
    obj["xtz_warning"] = "A1 nodes are locked. Inter-node stairs/platforms are not final construction geometry."
    obj["xtz_stair_count"] = int(axis_data["total_steps"])
    obj["xtz_segment_count"] = len(axis_data["stages"])
    obj["xtz_max_continuous_sightline_m"] = int(axis_data["geometry_rules"]["max_continuous_route_alignment_sightline_m"])
    return obj, points


def build_key_assets(key_assets_data: dict):
    """Build B1-locked positional/size proxies for selected core assets."""
    collection = get_or_create_collection("XTZ_KeyAssets")
    built = []
    for asset in key_assets_data["assets"]:
        if not asset.get("v0_1_build"):
            continue
        if "plan_m" not in asset or "height_m" not in asset or asset.get("elevation_m") is None:
            continue

        x_km, y_km = asset["coord_km"]
        width_m, depth_m = asset["plan_m"]
        height_m = float(asset["height_m"])
        base_z = float(asset["elevation_m"])
        obj = add_cube(
            f"XTZ_ASSET_{asset['id']}_{asset['name']}",
            (float(width_m), float(depth_m), height_m),
            (float(x_km) * 1000.0, float(y_km) * 1000.0, base_z + height_m / 2.0),
            collection,
        )
        obj["xtz_asset_id"] = asset["id"]
        obj["xtz_name"] = asset["name"]
        obj["xtz_type"] = asset["type"]
        obj["xtz_world_anchor_status"] = CANON_B1_ANCHOR_TAG
        obj["xtz_geometry_status"] = NON_CANON_PROXY_TAG
        obj["xtz_base_elevation_m"] = base_z
        obj["xtz_plan_m"] = f"{width_m}x{depth_m}"
        obj["xtz_height_m"] = height_m
        if "visual_rank" in asset:
            obj["xtz_visual_rank"] = asset["visual_rank"]
        if "visibility" in asset:
            obj["xtz_visibility_rule"] = asset["visibility"]
        built.append(obj)
    return built


def add_camera(name, lens_mm, location, target, collection):
    cam_data = bpy.data.cameras.new(name + "_DATA")
    cam_data.lens = float(lens_mm)
    cam_data.sensor_width = 36.0
    cam = bpy.data.objects.new(name, cam_data)
    collection.objects.link(cam)
    cam.location = location
    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return cam


def build_cameras(camera_data: dict, axis_points: Iterable[tuple]):
    collection = get_or_create_collection("XTZ_Cameras")
    points = list(axis_points)
    start = Vector(points[0])
    target = Vector(points[min(2, len(points) - 1)])
    drone = add_camera("XTZ_CAM_DJI_28MM_PROXY", 28.0, (start.x, start.y - 120.0, start.z + 12.0), target, collection)
    drone["xtz_camera_system"] = camera_data["camera_system"]
    drone["xtz_usage"] = "real-drone path preview"
    drone["xtz_position_status"] = NON_CANON_PROXY_TAG

    center_target = Vector((0.0, 6800.0, 1050.0))
    rig_origin = Vector((0.0, 700.0, 1150.0))
    e1 = []
    for suffix, target_x in (("L", -1800.0), ("C", 0.0), ("R", 1800.0)):
        cam = add_camera(f"XTZ_CAM_E1_{suffix}_50MM_PROXY", 50.0, rig_origin, (target_x, center_target.y, center_target.z), collection)
        cam["xtz_camera_system"] = "E1 virtual three-frame stitch"
        cam["xtz_position_status"] = NON_CANON_PROXY_TAG
        e1.append(cam)
    bpy.context.scene.camera = drone
    return {"drone": drone, "e1": e1}


def animate_camera_from_path(camera, path_data: dict):
    """Keyframe a camera from a machine-readable engineering preview path."""
    scene = bpy.context.scene
    fps = int(path_data.get("fps", scene.render.fps))
    duration_s = float(path_data["duration_s"])
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = max(2, int(round(duration_s * fps)))

    keys = path_data["keyframes"]
    if len(keys) < 2:
        raise ValueError("preview camera path requires at least 2 keyframes")

    for key in keys:
        t = float(key["t"])
        frame = 1 + int(round(t * fps))
        location = Vector(key["location_m"])
        target = Vector(key["look_at_m"])
        camera.location = location
        direction = target - location
        camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    if camera.animation_data and camera.animation_data.action:
        action = camera.animation_data.action
        for fcurve in action.fcurves:
            for point in fcurve.keyframe_points:
                point.interpolation = "BEZIER"
                point.handle_left_type = "AUTO_CLAMPED"
                point.handle_right_type = "AUTO_CLAMPED"

    camera["xtz_path_id"] = path_data["path_id"]
    camera["xtz_path_status"] = path_data["canon_status"]
    camera["xtz_path_usage"] = path_data["usage"]
    return scene.frame_end


def add_world_envelope(width_km=8.0, depth_km=12.0):
    collection = get_or_create_collection("XTZ_WorldGuides")
    obj = add_cube("XTZ_WORLD_ENVELOPE_GUIDE", (width_km * 1000.0, depth_km * 1000.0, 10.0), (0.0, depth_km * 500.0, -5.0), collection)
    obj.display_type = "WIRE"
    obj.hide_render = True
    obj["xtz_geometry_status"] = "CANON_EXTENT_GUIDE"
    return obj
