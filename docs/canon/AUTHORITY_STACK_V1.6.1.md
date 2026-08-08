# Canon Authority Stack — V1.6.1 + Scoped Locked Overlays

## Purpose

This document is the engineering conflict-resolution order for Xuantianzong Virtual Studio.

## Core rule

`玄天宗世界设定总纲 V1.6.1` is the **BASE_WORLD_CANON**: the current integrated world master for geography, institutions, architecture hierarchy, A1/B1/C1 data and all fields not explicitly superseded later.

V1.6.1 also requires new formal assets to be written back into parameter JSON / asset indexes. The project continued after V1.6.1 and some specialist modules were later explicitly approved and LOCKED by the user.

Therefore the actual authority model is:

```text
1. BASE_WORLD_CANON — V1.6.1
2. SCOPED_POST_CANON_LOCKED_OVERRIDE — later explicit user-approved LOCKED modules, only for their declared fields
3. ACTIVE TECH/ASSET CONTROLS consistent with 1+2
4. DERIVED binaries and visual references
5. Historical files / concepts / prompts
```

A later file does **not** win merely because it is newer. It must meet the override gate in `POST_CANON_LOCKED_OVERRIDES.md`.

## Active base control stack

- **V1.6.1** — base world master and locked parameter export.
- **A1** — coordinates, elevation, terrain, ancient road, central axis, rear zone, water, gate/sword engineering detail; integrated into V1.6.1.
- **B1** — peak functions, population, key assets, traffic/airspace; integrated into V1.6.1.
- **C1** — visual hierarchy, materials, image/video and high-tier-beast filming policy; integrated into V1.6.1.
- **E1** — V12 strategic camera / visibility control only; not a real DJI path.
- **F1** — graybox/proportion control: continuous terrain, ridge chains, central valley, heavy inverted Xuantian Peak, B1 envelopes.
- **F2/F3** — specialist high-tier beast scale/placement and shape/V12 fit, under the scoped beast override rules.
- **G1** — later formal hero/master-image control, inheriting E1 + F2 LOCKED + F3 PASSED.

## Confirmed post-canon override

### OVR-BEAST-001 — Six high-tier beasts

V1.6.1 was generated around 2026-08-07 01:59Z. Later that day the beast workflow, mythology constraints, V1.0 formal asset registry and F2 were explicitly user-approved/LOCKED; G1 later requires beast dimensions to be read only from Canonical.

Therefore the later beast module supersedes V1.6.1's older dimensions/wing fields **only for these six beasts**:

- 白泽
- 玄雷夔
- 毕方
- 夫诸
- 九天玄应龙
- 太玄玄武

Use:
- `data/canon/post_canon_overrides.json`
- `docs/canon/POST_CANON_LOCKED_OVERRIDES.md`

Important examples:
- 九天玄应龙 is currently a **wingless** Xuantianzong-derived Oriental ancestral dragon; normal body length 1200m; 1800m is its normal occupancy/coil-control envelope.
- 玄雷夔 is one-footed and **has no horns**. Old thunder-horn fields are deprecated and must never resurrect.

## Explicitly checked fields that do NOT need an override

The following current values already exist directly in V1.6.1 and remain base Canon:

- 建木480m / 扶桑320m / 若木260m; 若木 `(2.00,4.45)`.
- 玄天峰 1.45×1.05km, highest ridge1680m, deepest inverted spire1210m, main vertical depth400–470m.
- 玄岳关52×18×34m; central opening11×15m.
- 双阙剑44m, axis spacing68m, V10 double-edged straight-sword identity.
- nine-peak macro topology, ancient road, nine-stage axis, rear zone and water system.

## Canon vs validation state

A locked design value is not automatically visually validated.

Use these engineering labels:

- `LOCKED_DESIGN`
- `LOCKED_GEOMETRY_VALIDATED`
- `LOCKED_VISUALLY_VALIDATED`
- `LOCKED_DESIGN_NOT_VISUALLY_VALIDATED`
- `NON_CANON_PROXY`

## Binary evidence policy

Do not confuse “not directly returned by File Library search” with “never existed”.

Use:
- `DIRECT_FOUND`
- `MANIFEST_VERIFIED`
- `REFERENCED_ONLY`

Example: F2 GLBs are `MANIFEST_VERIFIED`: the locked F2 SHA256 manifest records their names, sizes and hashes even though this census did not surface the individual GLBs as independent File Library results.

## Non-negotiable world rules

- Exactly nine formal peaks.
- Only 玄天峰 is a large floating main peak.
- Eight terrestrial peaks form continuous ridge/saddle/valley systems, not isolated cones.
- 玄天峰 reads as a full heavy inverted mountain, never a disk/plate/UFO.
- Mountains remain larger than buildings.
- The ceremonial route bends with terrain and cannot be a straight sky stair.
- 玄岳关 + 双阙剑 are strong foreground anchors; 玄天峰/玄天殿 are the ultimate distant center.
- Rear restricted assets remain occluded from prohibited front views.
- E1 is a virtual strategic stitched camera, not real DJI.

## Change-control rule

If visual tests expose a problem with a locked value:

1. Do not silently edit the Canon JSON.
2. Mark `LOCKED_DESIGN_NOT_VISUALLY_VALIDATED`.
3. Rule out proxy/camera/render implementation errors first.
4. Only propose a Canon change after the failure persists.
5. Any later approved change must be registered in `MASTER_ASSET_REGISTRY` and, if it supersedes an existing field, in `post_canon_overrides.json`.

## Required indexes

Every engineering session that changes Canon/assets must read:

- `docs/canon/MASTER_ASSET_REGISTRY_2026-08-08.md`
- `data/canon/master_asset_registry_2026-08-08.json`
- `docs/canon/POST_CANON_LOCKED_OVERRIDES.md`
- `data/canon/post_canon_overrides.json`
