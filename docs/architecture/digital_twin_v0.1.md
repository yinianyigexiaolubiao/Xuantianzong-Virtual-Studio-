# Digital Twin V0.1 — Implementation Specification

## Purpose

V0.1 proves that 玄天宗 can exist as a repeatable spatial filming location. It is not a final terrain model, architectural art pass, material pass, or AI video. The acceptance target is spatial continuity.

## Canon vs Proxy

Every generated object must be either:

- **Canon-controlled** — value comes directly from locked machine-readable data.
- **NON_CANON_PROXY** — geometry/location exists only to make the graybox inspectable and must not become lore or final art.

At V0.1 the nine peak centers, elevations, core spans, gate dimensions, twin-sword height/spacing, world envelope, axis length/stage count and camera lens rules are Canon-controlled.

Still Proxy until dedicated locked data is serialized:

- exact 玄岳关 world anchor;
- exact A1 central-axis waypoint coordinates;
- 玄天峰 lower-body depth/profile;
- exact 玄天殿 geometry and placement on 玄天峰;
- exact E1 rig transform;
- production DJI flight paths.

## Blender output

Running `blender/world_builder.py` creates:

- 8 km × 12 km world-envelope guide;
- nine peak proxy objects;
- 玄岳关 dimensional proxy;
- two V10 straight-sword proxies at 68 m axis separation and 44 m height;
- a nine-stage bent ceremonial-axis preview;
- one 28 mm DJI preview camera;
- three 50 mm cameras representing the E1 virtual stitch.

## Acceptance gates

1. exactly nine formal peaks are generated;
2. only 玄天峰 is flagged as a large floating main peak;
3. all peak XY centers and summit elevations match `peaks.json`;
4. 玄岳关 bounding dimensions are 52 × 18 × 34 m;
5. twin swords are 44 m high and 68 m apart on axis;
6. ceremonial-axis preview is visibly non-straight and marked NON_CANON_PROXY;
7. E1 and DJI cameras remain separate systems;
8. no script silently writes a missing Proxy value back into Canon JSON.

## Next lock required

Before V0.2 production paths, serialize the A1 exact waypoint/control-point table for:

`玄岳关 → 迎仙坪 → 九段玄阶 → 玄武门 → 玄天门 → 镇岳广场/北斗坛 → 接天阵台`.
