# Codex Engineering Contract — Xuantianzong Virtual Studio

## Authority

The repository is governed by locked 玄天宗 Canon. Engineering convenience must never overwrite world truth.

## Rules

1. Do not edit `data/world/` unless a task explicitly says a Canon parameter has been approved or changed.
2. Treat `NON_CANON_PROXY` as disposable geometry, never as approved lore.
3. Unknown dimensions/coordinates must be explicit Proxy parameters or TODOs; never invent them silently.
4. Run `python tools/validate_world_data.py` after any world-data change.
5. Blender scripts must be deterministic from the same JSON inputs.
6. Keep E1 strategic master-camera logic separate from real DJI camera paths.
7. No production video-model integration may move canonical peak centers to improve composition.
8. Put generated `.blend` outputs under `build/`; do not commit large binaries directly. Use Git LFS/object storage when necessary.

## Immediate engineering milestone

Digital Twin V0.1:

- make `blender/world_builder.py` runnable in Blender 4.x;
- verify all nine peak proxies;
- verify gate/sword dimensional proxies;
- verify the axis preview is clearly marked non-canonical;
- verify camera objects are created;
- save a graybox `.blend` and viewport preview;
- report missing Canon fields instead of guessing them.

## Definition of done

A fresh clone plus Blender can reproduce the same graybox from repository data without manual object placement.
