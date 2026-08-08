# CODEX.md — Xuantianzong Virtual Studio Engineering Contract

## Authority

1. `玄天宗世界设定总纲 V1.6.1` is the sole current Canon.
2. Read `docs/canon/AUTHORITY_STACK_V1.6.1.md` before any world, camera or visual change.
3. Read `docs/canon/ASSET_CLASSIFICATION_2026-08-08.md` to determine whether a source is current, technical control, visual reference, historical or deprecated.
4. `data/world/*.json` is the machine-readable engineering projection of the current Canon.
5. `data/canon/source_registry_v1.6.1.json` records the formal control stack.
6. Any field, mesh, route or camera marked `NON_CANON_PROXY` is temporary and MUST NOT be promoted to Canon by code, rendering or inference.

## Current milestone

`Digital Twin V0.2 — Mini Spatial Proof`

V0.1 is preserved as `Engineering Proof`: it demonstrated `Canon → JSON → Blender → Render → MP4`, but its flat base plane, isolated cone peaks, hard-polyline road reading and disk-like Xuantian Peak silhouette do not satisfy the mature F1/C1/E1 spatial-reading requirements.

V0.2 MUST inherit `docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md` rather than invent a new terrain system from scratch.

## Required invariants

- Exactly nine formal peaks.
- Only 玄天峰 may be a large floating main peak.
- The eight terrestrial peaks are grounded and connected through ridges, saddles, foothills and valleys; never render them as nine isolated cones or floating islands.
- West ridge chain: 天剑峰 → 镇岳峰 → 天工峰 → 灵兽峰.
- East ridge chain: 寒渊峰 → 紫微峰 → 丹霞峰 → 万木峰.
- Xuantian Peak must read as a heavy, irregular inverted mountain within the locked A1 envelope; no disk, plate, ellipse or UFO silhouette.
- The central ceremonial route must conform to terrain and remain non-straight; locked A1 nodes are macro controls, not visible hard corners.
- 玄岳关 locked body dimensions: 52 m × 18 m × 34 m.
- 双阙剑 locked height: 44 m; axis distance: 68 m; V10 double-edged straight-sword identity.
- E1/V12 strategic camera is not a real DJI single-lens camera.
- DJI preview cameras use realistic 24–35 mm equivalent optics and physically plausible movement.
- Mountains and natural masses remain visually larger than buildings; low building coverage is intentional.

## Canon / validation labels

Use these statuses explicitly:

- `LOCKED_DESIGN`
- `LOCKED_GEOMETRY_VALIDATED`
- `LOCKED_VISUALLY_VALIDATED`
- `LOCKED_DESIGN_NOT_VISUALLY_VALIDATED`
- `NON_CANON_PROXY`

A Canon value is not automatically visually validated. If a rendered result looks wrong, first determine whether the proxy geometry/camera is wrong before proposing a Canon edit.

## Development rules

- Run `python tools/validate_world_data.py` before and after any edit to `data/world/`.
- V0.2 must add/use a Blender geometry validator for generated transforms, bounds, clearances, collisions and path continuity.
- Blender-generated objects must use the `XTZ_` prefix.
- New provisional coordinates or shapes must carry `NON_CANON_PROXY` metadata.
- Never silently invent missing canonical dimensions. Add an explicit TODO/proxy parameter instead.
- Preserve user-authored Blender objects when rebuilding; delete only generated `XTZ_` content.
- Prefer deterministic builders reading JSON over hand-positioned scene edits.
- Preserve V0.1 delivery artifacts; V0.2 writes to a separate output directory.
- Do not start Seedance/Wan/ComfyUI/LoRA/Unreal integration while the Mini Spatial Proof is still failing visual or camera QC.

## F1 inheritance

F1 is a spatial-control precedent and must be treated as an implementation requirement where consistent with V1.6.1:

- whole-world massing may start from a 100m terrain grid;
- the eight terrestrial peaks use continuous terrain, not separate primitive cones;
- central valley and rear mountain massing must exist;
- Xuantian Peak uses the locked ~1.45km × 1.05km, 400–470m heavy inverted envelope;
- B1 buildings remain envelope blocks in graybox phases;
- E1-style fixed QC views are used to check proportion/occlusion even though DJI uses a separate camera system.

## Camera rule

A camera path is not accepted merely because it is continuous.

DJI motion should separate:
- position curve;
- yaw/body orientation;
- gimbal pitch/target;
- speed profile.

Report or validate speed, acceleration, jerk and yaw-rate limits. Avoid constant-speed rail-camera behavior.

## Acceptance ladder

A milestone requires separate passes:

1. **Canon Validator** — source data/invariants pass.
2. **Geometry Validator** — generated scene transforms, bounds, clearances, terrain/route continuity and collision checks pass.
3. **Visual QC** — fixed bright-gray renders show correct silhouettes, hierarchy, occlusion and scale.
4. **Camera QC** — DJI preview reads as physically plausible aerial movement and produces a meaningful reveal after passing Xuanyue Gate.
5. **Deterministic Rebuild** — two clean builds reproduce the same locked transforms, bounds and camera data.

Do not claim complete success if only one layer passes.
