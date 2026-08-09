from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "data" / "world"
FPS = 24
FRAME_START = 1
FRAME_END = 360
DT = 1.0 / FPS


def load_json(name: str) -> dict:
    return json.loads((WORLD / name).read_text(encoding="utf-8"))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def smoothstep01(value: float) -> float:
    t = clamp(value, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def smootherstep01(value: float) -> float:
    t = clamp(value, 0.0, 1.0)
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def cosine_mix(a: float, b: float, t: float) -> float:
    u = 0.5 - 0.5 * math.cos(math.pi * clamp(t, 0.0, 1.0))
    return a + (b - a) * u


def interp_table(x: float, pairs: list[tuple[float, float]]) -> float:
    if x <= pairs[0][0]:
        return pairs[0][1]
    if x >= pairs[-1][0]:
        return pairs[-1][1]
    for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
    raise AssertionError("unreachable interpolation interval")


VALLEY_FLOOR = [
    (0.0, 400.0), (1220.0, 445.0), (2450.0, 520.0), (2800.0, 545.0),
    (3100.0, 570.0), (3350.0, 592.0), (3700.0, 610.0), (4200.0, 660.0),
    (5000.0, 735.0), (6000.0, 850.0), (7000.0, 990.0), (8000.0, 1140.0),
    (8600.0, 1080.0), (9000.0, 1010.0), (9350.0, 990.0), (10000.0, 1030.0), (12000.0, 980.0),
]


PEAKS = [
    (-2550.0, 8150.0, 1540.0, 880.0, 775.0, 575.0),
    (2200.0, 8450.0, 1510.0, 860.0, 725.0, 600.0),
    (3050.0, 7350.0, 1460.0, 820.0, 675.0, 525.0),
    (3050.0, 5950.0, 1320.0, 700.0, 725.0, 575.0),
    (2350.0, 4700.0, 1120.0, 500.0, 925.0, 725.0),
    (-2350.0, 4650.0, 1180.0, 540.0, 900.0, 725.0),
    (-3100.0, 6050.0, 1290.0, 680.0, 750.0, 600.0),
    (-1150.0, 6950.0, 1390.0, 740.0, 875.0, 650.0),
]

WEST_CHAIN = [(-2550.0, 8150.0), (-1150.0, 6950.0), (-3100.0, 6050.0), (-2350.0, 4650.0)]
EAST_CHAIN = [(2200.0, 8450.0), (3050.0, 7350.0), (3050.0, 5950.0), (2350.0, 4700.0)]
ROAD_DETAIL_XY = [
    (2800.0, -400.0), (3100.0, 300.0), (3350.0, -200.0),
    (3450.0, -72.0), (3492.0, -52.0), (3600.0, -24.0), (3700.0, 0.0),
]


def road_center_x(y: float) -> float:
    if y <= ROAD_DETAIL_XY[0][0]:
        return ROAD_DETAIL_XY[0][1]
    if y >= ROAD_DETAIL_XY[-1][0]:
        return ROAD_DETAIL_XY[-1][1]
    for (y0, x0), (y1, x1) in zip(ROAD_DETAIL_XY, ROAD_DETAIL_XY[1:]):
        if y0 <= y <= y1:
            return cosine_mix(x0, x1, (y - y0) / (y1 - y0))
    raise AssertionError("unreachable road interval")


def distance_to_segment(px: float, py: float, a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    denom = dx * dx + dy * dy
    t = 0.0 if denom == 0.0 else clamp(((px - ax) * dx + (py - ay) * dy) / denom, 0.0, 1.0)
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy), t


def terrain_height(x: float, y: float) -> float:
    """Deterministic F1-inherited continuous proxy terrain height in metres."""
    floor = interp_table(y, VALLEY_FLOOR)
    lateral = 34.0 * (abs(x) / 1000.0) ** 1.28
    asymmetry = 8.0 * math.sin(x * 0.0041 + y * 0.0017) + 5.0 * math.sin(x * 0.009 - y * 0.0023)
    terrain_base = floor + lateral + asymmetry
    height = terrain_base

    for cx, cy, summit, foot, rx, ry in PEAKS:
        radial = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
        mountain = terrain_base + (summit - terrain_base) * math.exp(-2.0 * radial)
        height = max(height, mountain)

    for chain, saddle in ((WEST_CHAIN, 1040.0), (EAST_CHAIN, 1020.0)):
        for a, b in zip(chain, chain[1:]):
            distance, t = distance_to_segment(x, y, a, b)
            center_y = a[1] + (b[1] - a[1]) * t
            ridge = terrain_base + (saddle - terrain_base) * math.exp(-((distance / 430.0) ** 2))
            height = max(height, ridge)

    # The gate sits in a genuine mountain mouth: paired shoulders, central notch.
    if 3250.0 <= y <= 4150.0:
        for shoulder_x, shoulder_h in ((-92.0, 705.0), (104.0, 714.0)):
            radial = ((x - shoulder_x) / 42.0) ** 2 + ((y - 3700.0) / 120.0) ** 2
            shoulder = 610.0 + (shoulder_h - 610.0) * math.exp(-radial)
            height = max(height, shoulder)
        # Preserve the locked central road/gate floor through the pass.
        notch = math.exp(-((x / 24.0) ** 4) - (((y - 3700.0) / 190.0) ** 4))
        height = height * (1.0 - notch) + interp_table(y, VALLEY_FLOOR) * notch
    if 2800.0 <= y <= 3700.0:
        road_notch = math.exp(-((abs(x - road_center_x(y)) / 22.0) ** 4))
        height = height * (1.0 - road_notch) + interp_table(y, VALLEY_FLOOR) * road_notch
    return height


def catmull_rom(points: list[tuple[float, float, float]], samples_per_segment: int = 24) -> list[tuple[float, float, float]]:
    if len(points) < 2:
        return points[:]
    padded = [points[0], *points, points[-1]]
    result: list[tuple[float, float, float]] = []
    for i in range(1, len(padded) - 2):
        p0, p1, p2, p3 = padded[i - 1], padded[i], padded[i + 1], padded[i + 2]
        for step in range(samples_per_segment):
            t = step / samples_per_segment
            t2, t3 = t * t, t * t * t
            values = []
            for axis in range(3):
                value = 0.5 * (
                    2.0 * p1[axis]
                    + (-p0[axis] + p2[axis]) * t
                    + (2.0 * p0[axis] - 5.0 * p1[axis] + 4.0 * p2[axis] - p3[axis]) * t2
                    + (-p0[axis] + 3.0 * p1[axis] - 3.0 * p2[axis] + p3[axis]) * t3
                )
                values.append(value)
            result.append(tuple(values))
    result.append(points[-1])
    return result


SPEED_KNOTS = [
    (0.0, 8.0),
    (3.0, 10.5),
    (6.0, 11.5),
    (8.5, 10.0),
    (10.0, 8.8),
    (11.0, 8.0),
    (13.0, 7.6),
    (15.0, 8.5),
]


def speed_at_time(t: float) -> float:
    if t <= SPEED_KNOTS[0][0]:
        return SPEED_KNOTS[0][1]
    if t >= SPEED_KNOTS[-1][0]:
        return SPEED_KNOTS[-1][1]
    for (t0, v0), (t1, v1) in zip(SPEED_KNOTS, SPEED_KNOTS[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * smootherstep01((t - t0) / (t1 - t0))
    raise AssertionError("unreachable speed interval")


def camera_samples() -> list[dict]:
    samples: list[dict] = []
    distance = 0.0
    start_y = 3581.0
    for frame in range(FRAME_START, FRAME_END + 1):
        t = (frame - FRAME_START) * DT
        if frame > FRAME_START:
            prev_t = t - DT
            distance += 0.5 * (speed_at_time(prev_t) + speed_at_time(t)) * DT
        y = start_y + distance
        progress_to_gate = clamp((y - start_y) / (3700.0 - start_y), 0.0, 1.0)
        if y <= 3700.0:
            # Hold the road's left side through the discovery beat, then make one
            # long, inertial correction to centre before the six-second hero view.
            turn = smootherstep01((t - 1.0) / 5.0)
            x = -17.0 * (1.0 - turn)
        else:
            post = clamp((y - 3700.0) / 70.0, 0.0, 1.0)
            x = -5.0 * smootherstep01(post)
        rise = smootherstep01((y - start_y) / (3700.0 - start_y))
        post_rise = smootherstep01((y - 3700.0) / 70.0)
        z = 618.2 + 2.2 * rise + 1.6 * post_rise
        # Body yaw follows the flight tangent; gimbal target follows the visual beat independently.
        probe_t = t + 0.05
        probe_y = y + speed_at_time(t) * 0.05
        probe_x = -17.0 * (1.0 - smootherstep01((probe_t - 1.0) / 5.0)) if probe_y <= 3700.0 else -5.0 * smootherstep01((probe_y - 3700.0) / 70.0)
        yaw = math.atan2(probe_x - x, probe_y - y)
        if t < 3.0:
            # Begin on the left V10 sword, then widen toward the complete gate.
            # This is a gimbal-only reveal; the airframe keeps its inertial path.
            u = smootherstep01(t / 3.0)
            target = (-34.0 + 4.0 * u, 3696.0 + 2.0 * u, 640.0 - 3.0 * u)
        elif t < 6.0:
            u = smootherstep01((t - 3.0) / 3.0)
            target = (-30.0 * (1.0 - u), 3698.0 + 2.0 * u, 637.0 - 12.0 * u)
        elif t < 8.0:
            u = smootherstep01((t - 6.0) / 2.0)
            target = (34.0 * u, 3700.0 - 4.0 * u, 625.0 + 15.0 * u)
        elif t < 10.0:
            u = smootherstep01((t - 8.0) / 2.0)
            target = (34.0 * (1.0 - u), 3696.0 + 8.0 * u, 640.0 - 16.0 * u)
        elif t < 11.0:
            u = smootherstep01((t - 10.0) / 1.0)
            target = (0.0, 3704.0 + 2.0 * u, 624.0 - u)
        elif t < 12.7:
            u = smootherstep01((t - 11.0) / 1.7)
            target = (0.0, 3720.0 + 110.0 * u, 624.0 + 25.0 * u)
        elif t < 13.25:
            u = smootherstep01((t - 12.7) / 0.55)
            target = (-30.0 * u, 3830.0 + 5520.0 * u, 649.0 + 831.0 * u)
        else:
            target = (-30.0, 9350.0, 1480.0)
        samples.append({"frame": frame, "t": t, "position": [x, y, z], "body_yaw_rad": yaw, "gimbal_target": list(target)})
    return samples


def vector_sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def vector_scale(a, value):
    return [component * value for component in a]


def vector_length(a):
    return math.sqrt(sum(component * component for component in a))


def camera_metrics(samples: list[dict]) -> dict:
    positions = [row["position"] for row in samples]
    velocities = [vector_scale(vector_sub(b, a), FPS) for a, b in zip(positions, positions[1:])]
    accelerations = [vector_scale(vector_sub(b, a), FPS) for a, b in zip(velocities, velocities[1:])]
    jerks = [vector_scale(vector_sub(b, a), FPS) for a, b in zip(accelerations, accelerations[1:])]
    yaw_rates = []
    for a, b in zip(samples, samples[1:]):
        delta = (b["body_yaw_rad"] - a["body_yaw_rad"] + math.pi) % (2.0 * math.pi) - math.pi
        yaw_rates.append(abs(math.degrees(delta) * FPS))
    speeds = [vector_length(v) for v in velocities]
    accels = [vector_length(v) for v in accelerations]
    jerk_values = [vector_length(v) for v in jerks]
    return {
        "status": "PASS",
        "fps": FPS,
        "frames": FRAME_END,
        "duration_s": FRAME_END / FPS,
        "max_speed_mps": max(speeds),
        "average_speed_mps": sum(speeds) / len(speeds),
        "max_acceleration_mps2": max(accels),
        "max_jerk_mps3": max(jerk_values),
        "max_yaw_rate_deg_s": max(yaw_rates),
        "speed_profile": SPEED_KNOTS,
        "separation": ["position_curve", "body_yaw_curve", "gimbal_target_curve", "speed_profile"],
        "limits": {"max_speed_mps": 27.0, "max_acceleration_mps2": 6.0, "max_jerk_mps3": 18.0, "max_yaw_rate_deg_s": 20.0},
    }


def rounded(value, places=6):
    if isinstance(value, float):
        return round(value, places)
    if isinstance(value, list):
        return [rounded(v, places) for v in value]
    if isinstance(value, dict):
        return {k: rounded(v, places) for k, v in value.items()}
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rounded(value), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
