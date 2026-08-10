# CODEX.md — Xuantianzong Project + Virtual Studio Engineering Contract

## Project scope — read before doing anything

This repository is the **project-level archive and active engineering home for the recovered 玄天宗 project**, not merely a Blender/Digital-Twin codebase.

Before touching any project branch, read:

1. `docs/project/MASTER_PROJECT_REGISTRY_2026-08-08.md`
2. `data/project/master_project_registry_2026-08-08.json`
3. `docs/project/SYNC_STATUS_2026-08-08.md`

The project registry contains nine mandatory branches:

- `CANON_AND_WORLD`
- `DIGITAL_TWIN`
- `VISUAL_ASSETS`
- `PROMO_FILM_AND_DJI`
- `PHONE_CONTENT`
- `XUANYUAN_LIANQI`
- `DIGITAL_XUANTIANZONG`
- `BEASTS_AND_SACRED_TREES`
- `HISTORICAL_ARCHIVE`

Do not delete, rename away, ignore or silently redefine one of these branches merely because the current coding task concerns Digital Twin.

### Archive honesty

A registered historical file may be:

- `GITHUB_MIRRORED`
- `GITHUB_REGISTERED_METADATA`
- `FILE_LIBRARY_ONLY_BINARY`
- `FILE_LIBRARY_ONLY_TEXT`
- `MANIFEST_VERIFIED`
- `CHAT_RECORDED_SPEC`
- `REFERENCED_ONLY`

Never claim an old File Library artifact has been copied into GitHub unless exact content/bytes are actually present. Never recreate an old binary/text from memory and label it as the original.

If a previously unknown Xuantianzong project artifact is recovered, register it in `data/project/master_project_registry_2026-08-08.json` before using it as an official project asset.

## Canon authority — read before changing world data

1. `玄天宗世界设定总纲 V1.6.1` is the **BASE_WORLD_CANON**, not a license to erase later user-approved locked specialist assets.
2. Read `docs/canon/AUTHORITY_STACK_V1.6.1.md`.
3. Read `docs/canon/MASTER_ASSET_REGISTRY_2026-08-08.md` and `data/canon/master_asset_registry_2026-08-08.json`.
4. Read `docs/canon/POST_CANON_LOCKED_OVERRIDES.md` and `data/canon/post_canon_overrides.json`.
5. Read `docs/canon/ASSET_CLASSIFICATION_2026-08-08.md`.
6. `data/world/*.json` is the machine-readable geometry/world projection used by the current Blender build; it is **not automatically the sole source for specialist asset domains**.
7. If a field is listed in an active post-canon override, use the override source for that field and V1.6.1 for all unaffected fields.
8. Any field, mesh, route or camera marked `NON_CANON_PROXY` is temporary and MUST NOT be promoted to Canon by code, rendering or inference.

### Current scoped override

`OVR-BEAST-001` controls the six high-tier beasts.

Never resurrect superseded V1.6.1 beast values for those six. In particular:
- 玄雷夔: one leg, **no horns**; old thunder-horn fields are deprecated.
- 九天玄应龙: **wingless** Oriental ancestral dragon; normal physical body length 1200m; 1800m is the normal occupancy/coil-control envelope.

V0.2 does not need to place these beasts, but any code/document touched during V0.2 must not reintroduce the superseded fields.

## Other project branches that must remain preserved

### 《玄元炼气诀》

This is an independent cultivation-text/publishing branch, not disposable prose inside the Digital Twin project. See `docs/archive/xuanyuan_lianqi/README.md`.

The preferred recovered source is registered as `玄元炼气诀_真传重写版_无说明.txt`; its exact long text is File-Library-only until raw bytes/full payload can be migrated. Do not replace it with a partial reconstruction.

### 数字玄天宗

Historical V0.1–V0.3 living-world/canon-engine lineage is preserved in `docs/archive/digital_xuantianzong/STATUS_2026-08-04.md`. Its then-current V1.3 world authority is historical; do not use it to override current V1.6.1.

### Visual assets

Historical mother images/maps are catalogued under `VISUAL_ASSETS` and `docs/archive/visual_assets/README.md`. They may carry style/composition evidence but cannot override current geometry merely because they look attractive.

### Promo film / DJI / phone content

Preserve the production branches in:

- `docs/archive/promo_film/README.md`
- `docs/archive/phone_content/README.md`

Do not convert promotional-film work into documentary narration, invent a hero, or lose the real-DJI physical-flight premise.

## Completed milestone

`Digital Twin V0.2 — Mini Spatial Proof — COMPLETED`

V0.2.2 passed engineering, human visual and camera-visual acceptance. The current Xuantian Peak floating mass, primary silhouette and visual identity are `LOCKED_VISUALLY_VALIDATED`. Future material, rock-detail, architecture, vegetation, waterfall, cloud and mist art passes must preserve that overall form unless the user explicitly requests a change.

V0.1 is preserved as `Engineering Proof`: it demonstrated `Canon/Data → JSON → Blender → Render → MP4`, but its flat base plane, isolated cone peaks, hard-polyline road reading and disk-like Xuantian Peak silhouette do not satisfy the mature F1/C1/E1 spatial-reading requirements.

The completed V0.2 implementation inherits `docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md`; future work must not reinterpret its accepted proxy geometry as permission to redesign Canon.

## Active production — Promo Film 01

`Promo Film 01《玄天宗·入宗》` is the active **SHOT-FIRST VIRTUAL PRODUCTION** fast line under `build/promo_film_01/`. It uses six bounded Shot Islands/Hero Zones and a 39-second sequence; it does not wait for a complete V0.3–V0.5 world build.

The accepted V0.2 Xuanyue Gate/Twin Sword/terrain relationship and gate-camera logic are inherited. The Xuantian Peak mesh and `LOCKED_VISUALLY_VALIDATED` silhouette/massing must remain unchanged. New shot-local materials, clouds, vegetation, representative inner-axis construction, architecture art, lights and camera paths remain `NON_CANON_PROXY` and cannot update Canon.

## Required spatial invariants

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

A Canon value is not automatically visually validated. If a rendered result looks wrong, first determine whether proxy geometry/camera is wrong before proposing a Canon edit.

## Development rules

- Run `python tools/validate_project_registry.py` when changing project archive/index files.
- Run `python tools/validate_world_data.py` before and after any edit to `data/world/`.
- Run `python tools/validate_canon_registry.py` whenever Canon/authority/registered-lock files change.
- Before changing Canon/asset authority, verify the Canon Master Registry and Override Registry first.
- V0.2 must add/use a Blender geometry validator for generated transforms, bounds, clearances, collisions and path continuity.
- Blender-generated objects must use the `XTZ_` prefix.
- New provisional coordinates or shapes must carry `NON_CANON_PROXY` metadata.
- Never silently invent missing canonical dimensions. Add an explicit TODO/proxy parameter instead.
- Preserve user-authored Blender objects when rebuilding; delete only generated `XTZ_` content.
- Prefer deterministic builders reading registered machine data over hand-positioned scene edits.
- Preserve V0.1 delivery artifacts; V0.2 writes to a separate output directory.
- Do not start Seedance/Wan/ComfyUI/LoRA/Unreal integration while the Mini Spatial Proof is still failing visual or camera QC.
- Any new user-approved LOCKED asset must be added to the Canon Master Asset Registry. If it supersedes an existing locked field, it must also be registered as a scoped post-canon override.
- Any new project branch/artifact must also be represented in the full Project Registry.

## F1 inheritance

F1 is a spatial-control precedent and must be treated as an implementation requirement where consistent with the current authority stack:

- whole-world massing may start from a 100m terrain grid;
- the eight terrestrial peaks use continuous terrain, not separate primitive cones;
- central valley and rear mountain massing must exist;
- Xuantian Peak uses the locked ~1.45km × 1.05km, 400–470m heavy inverted envelope;
- B1 buildings remain envelope blocks in graybox phases;
- E1-style fixed QC views are used to check proportion/occlusion even though DJI uses a separate camera system.

A historical F1 OBJ exists in File Library and may be used as comparison/import evidence. Do not normalize its scale on import.

## Camera rule

A camera path is not accepted merely because it is continuous.

DJI motion should separate:
- position curve;
- yaw/body orientation;
- gimbal pitch/target;
- speed profile.

Report or validate speed, acceleration, jerk and yaw-rate limits. Avoid constant-speed rail-camera behavior.

## Acceptance ladder

A Digital Twin milestone requires separate passes:

1. **Project Registry Validator** — full project archive/index remains represented.
2. **Canon Validator** — source data/invariants pass.
3. **Geometry Validator** — generated scene transforms, bounds, clearances, terrain/route continuity and collision checks pass.
4. **Visual QC** — fixed bright-gray renders show correct silhouettes, hierarchy, occlusion and scale.
5. **Camera QC** — DJI preview reads as physically plausible aerial movement and produces a meaningful reveal after passing Xuanyue Gate.
6. **Deterministic Rebuild** — two clean builds reproduce the same locked transforms, bounds and camera data.

Do not claim complete success if only one layer passes.
