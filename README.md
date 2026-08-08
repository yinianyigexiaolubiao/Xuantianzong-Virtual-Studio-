# Xuantianzong Virtual Studio / 玄天宗虚拟制片系统

Current phase: **Digital Twin V0.2 — Mini Spatial Proof**

This repository builds 玄天宗 as a persistent, spatially consistent virtual production world.

Core pipeline:

`Canon / Registered Locked Assets → Machine Data → Blender Digital Twin → Camera/QC → Control Passes → AI Video → Final Film`

## Read first

1. `CODEX.md` — engineering contract and current milestone.
2. `docs/canon/AUTHORITY_STACK_V1.6.1.md` — current authority/conflict model.
3. `docs/canon/MASTER_ASSET_REGISTRY_2026-08-08.md` — complete engineering asset census.
4. `data/canon/master_asset_registry_2026-08-08.json` — machine-readable asset census.
5. `docs/canon/POST_CANON_LOCKED_OVERRIDES.md` — later user-approved scoped overrides.
6. `data/canon/post_canon_overrides.json` — machine-readable override registry.
7. `docs/canon/ASSET_CLASSIFICATION_2026-08-08.md` — source classification.
8. `docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md` — mandatory graybox/topology rules for V0.2.
9. `data/canon/source_registry_v1.6.1.json` — control-stack registry.
10. `data/world/*.json` — current Blender/world geometry projection.

## Authority model

### Base world canon

**玄天宗世界设定总纲 V1.6.1 · 全量合并锁定版** is the `BASE_WORLD_CANON`.

It remains the integrated master for geography, nine peaks, institutions, architecture hierarchy, A1/B1/C1 world parameters and every field not explicitly superseded later.

### Scoped post-canon locked assets

After V1.6.1 was produced, the project continued and some specialist asset modules were explicitly approved/LOCKED by the user. A later module may supersede V1.6.1 **only for the fields explicitly inside its lock scope**.

Current confirmed override:

- `OVR-BEAST-001` — six high-tier beasts.

Examples:
- 玄雷夔 is one-footed and **has no horns**; old thunder-horn fields are deprecated.
- 九天玄应龙 is a **wingless** Xuantianzong-derived Oriental ancestral dragon; normal body length 1200m.

Do not use “newer file wins” as a general rule. DRAFT/REVIEW files, prompts and concept images cannot override Canon by themselves.

## Current status

### V0.1 — Engineering Proof

Completed and preserved under `build/`.

It proved:

`registered world data → Blender → .blend → render → 15s MP4`

V0.1 is not the visual-spatial target: its flat base, isolated cone massing and disk-like Xuantian Peak reading exposed implementation gaps against F1/C1/E1.

### V0.2 — Mini Spatial Proof

Active work is tracked in GitHub Issue #2.

Primary scope:
- final 800–1000m of 十二里入山古道;
- real valley/mountain-pass massing around 玄岳关;
- 玄岳关 + 双阙剑;
- 300–500m interior valley;
- distant 玄天峰 inverted-mountain silhouette;
- physically plausible DJI camera motion;
- Canon + Geometry + Visual + Camera + Deterministic-Rebuild validation.

F2/F3 beast controls are preserved for later relevant shots but are not a reason to add high-tier beasts to the V0.2 gate proof.

## Recovered / verified historical engineering assets

The census confirmed that earlier work contains valuable technical assets rather than only obsolete pictures:

- F1 graybox DOCX/PDF and an actual F1 OBJ are directly discoverable.
- F2 is LOCKED; its manifest verifies six individual GLBs, a Master GLB and review PNGs with SHA256/size even though this census did not directly surface each binary as a File Library item.
- F3 source JSON exists; source status is REVIEW, while downstream locked G1 records F3 as passed.
- G1 is LOCKED formal master-image control.

See the Master Asset Registry for exact binary-evidence state (`DIRECT_FOUND`, `MANIFEST_VERIFIED`, `REFERENCED_ONLY`).

## Non-negotiable topology

- Nine formal peaks.
- Only 玄天峰 is a large floating main peak.
- Eight terrestrial peaks form continuous ridge systems, not isolated cones.
- Xuantian Peak is a heavy inverted mountain, never a plate/UFO.
- The ceremonial axis bends with terrain and is never a straight sky stair.
- E1 strategic stitched camera is not a real DJI single-lens shot.

## Do not start yet

Until V0.2 spatial/camera QC passes, do not treat Seedance, Wan, ComfyUI, LoRA, Unreal or final high-detail art as the project bottleneck.
