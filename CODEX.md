# CODEX.md — Xuantianzong Virtual Studio Engineering Contract

## Authority

1. `玄天宗世界设定总纲 V1.6.1` is the sole current Canon.
2. `data/world/*.json` is the machine-readable engineering projection of that Canon.
3. Any field or position marked `NON_CANON_PROXY` is a temporary blockout and MUST NOT be promoted to Canon by code, rendering, or inference.

## Current milestone

`Digital Twin V0.1`

The goal is spatial correctness, not final art. Codex should prefer simple, auditable geometry over decorative invention.

## Required invariants

- Exactly nine formal peaks.
- Only 玄天峰 may be a large floating main peak.
- Do not turn the nine peaks into a ring of equal cones or isolated floating islands.
- Do not turn the central ceremonial axis into a straight white sky staircase.
- 玄岳关 locked body dimensions: 52 m × 18 m × 34 m.
- 双阙剑 locked height: 44 m; axis distance: 68 m; V10 double-edged straight-sword identity.
- E1/V12 strategic camera is not a real DJI single-lens camera.
- DJI preview cameras use realistic 24–35 mm equivalent optics and physically plausible movement.

## Development rules

- Run `python tools/validate_world_data.py` before and after any edit to `data/world/`.
- Blender-generated objects must use the `XTZ_` prefix.
- New provisional coordinates must carry `NON_CANON_PROXY` metadata.
- Never silently invent missing canonical dimensions. Add an explicit TODO or proxy parameter instead.
- Preserve user-authored Blender objects when rebuilding; delete only `XTZ_` generated content.
- Prefer deterministic builders reading JSON over hand-positioned scene edits.

## V0.1 build command

Interactive Blender: open `blender/world_builder.py` in Scripting and run it.

Headless save:

```bash
XTZ_SAVE_BLEND=1 blender --background --python blender/world_builder.py
```

Expected outputs:

- `build/xuantianzong_digital_twin_v0.1.blend`
- `build/digital_twin_v0.1_manifest.json`
- a 15-second proxy DJI gate-pass animation on `XTZ_CAM_DJI_28MM_PROXY`

## Acceptance gate

Do not start Seedance/Wan integration until the graybox passes:

1. nine-peak topology check;
2. single floating-main-peak check;
3. gate/sword dimensional check;
4. central-axis non-straightness check;
5. DJI camera path physical plausibility check;
6. no unlabelled proxy promoted to Canon.
