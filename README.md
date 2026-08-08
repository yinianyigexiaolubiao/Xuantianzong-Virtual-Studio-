# Xuantianzong Virtual Studio / 玄天宗虚拟制片系统

Current phase: **Digital Twin V0.2 — Mini Spatial Proof**

This repository builds 玄天宗 as a persistent, spatially consistent virtual production world.

Core pipeline:

`Canon → Machine Data → Blender Digital Twin → Camera/QC → Control Passes → AI Video → Final Film`

## Read first

1. `CODEX.md` — engineering contract and current milestone.
2. `docs/canon/AUTHORITY_STACK_V1.6.1.md` — authority/conflict order.
3. `docs/canon/ASSET_CLASSIFICATION_2026-08-08.md` — current vs historical vs deprecated sources.
4. `docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md` — mandatory graybox/topology rules for V0.2.
5. `data/canon/source_registry_v1.6.1.json` — machine-readable control-stack registry.
6. `data/world/*.json` — current machine-readable world parameters.

## Canon

The sole current Canon is:

**玄天宗世界设定总纲 V1.6.1 · 全量合并锁定版**

A1/B1/C1/E1/F1/G1 are retained as technical/visual control sources according to the authority stack; they may not override explicit V1.6.1 conflicts.

## Current status

### V0.1 — Engineering Proof

Completed and preserved under `build/`.

It proved the executable chain:

`Canon JSON → Blender → .blend → Render → 15s MP4`

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

## Non-negotiable topology

- Nine formal peaks.
- Only 玄天峰 is a large floating main peak.
- Eight terrestrial peaks form continuous ridge systems, not isolated cones.
- Xuantian Peak is a heavy inverted mountain, never a plate/UFO.
- The ceremonial axis bends with terrain and is never a straight sky stair.
- E1 strategic stitched camera is not a real DJI single-lens shot.

## Do not start yet

Until V0.2 spatial/camera QC passes, do not treat Seedance, Wan, ComfyUI, LoRA, Unreal or final high-detail art as the project bottleneck.
