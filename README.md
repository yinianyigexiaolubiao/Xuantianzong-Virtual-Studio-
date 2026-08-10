# 玄天宗 / Xuantianzong — Project Archive + Virtual Studio

Current active engineering phase: **Digital Twin V0.2 — Mini Spatial Proof**.

This repository is now the **project-level engineering/archive index for the entire recovered 玄天宗 project**, not only the Blender Digital Twin branch.

It preserves and classifies:

- current world Canon and technical controls;
- Digital Twin / AI Virtual Studio engineering;
- historical visual mother images and strategic maps;
- promotional-film / real-DJI production rules;
- disciple phone-content and 五蕴测灵石 content lineage;
- 《玄元炼气诀》 text and ancient-book publishing branch;
- historical 数字玄天宗 V0.1–V0.3 lineage;
- high-tier beasts / sacred trees / F2-F3-G1 controls;
- superseded world-bible and technical versions.

Core active film pipeline remains:

`Canon / Registered Locked Assets → Machine Data → Blender Digital Twin → Camera/QC → Control Passes → AI Video → Final Film`

## Read first — full project

1. `docs/project/MASTER_PROJECT_REGISTRY_2026-08-08.md` — human-readable full-project census.
2. `data/project/master_project_registry_2026-08-08.json` — machine-readable full-project registry.
3. `docs/project/SYNC_STATUS_2026-08-08.md` — what is physically mirrored vs File-Library-only/manifest/reference evidence.
4. `CODEX.md` — engineering contract and current milestone.

Then read the active Canon stack:

5. `docs/canon/AUTHORITY_STACK_V1.6.1.md`
6. `docs/canon/MASTER_ASSET_REGISTRY_2026-08-08.md`
7. `data/canon/master_asset_registry_2026-08-08.json`
8. `docs/canon/POST_CANON_LOCKED_OVERRIDES.md`
9. `data/canon/post_canon_overrides.json`
10. `docs/canon/ASSET_CLASSIFICATION_2026-08-08.md`
11. `data/canon/source_registry_v1.6.1.json`
12. `data/world/*.json`

For V0.2 also read:

13. `docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md`

## Project-level archive modules

The full project registry must always contain exactly these recovered branches:

1. `CANON_AND_WORLD`
2. `DIGITAL_TWIN`
3. `VISUAL_ASSETS`
4. `PROMO_FILM_AND_DJI`
5. `PHONE_CONTENT`
6. `XUANYUAN_LIANQI`
7. `DIGITAL_XUANTIANZONG`
8. `BEASTS_AND_SACRED_TREES`
9. `HISTORICAL_ARCHIVE`

`tools/validate_project_registry.py` and CI prevent one of these branches from silently disappearing from the repository index.

## Archive honesty rule

**Registered is not the same as physically mirrored.**

Some older PNG/PDF/DOCX/OBJ/GLB/TXT artifacts are directly present in ChatGPT File Library, but the current File Library search interface does not expose arbitrary raw bytes to the GitHub connector. They are therefore recorded honestly with states such as:

- `FILE_LIBRARY_ONLY_BINARY`
- `FILE_LIBRARY_ONLY_TEXT`
- `MANIFEST_VERIFIED`
- `REFERENCED_ONLY`

An artifact may be marked `GITHUB_MIRRORED` only when exact content/bytes are actually present here. See `docs/project/SYNC_STATUS_2026-08-08.md`.

## Current world authority

### Base world Canon

**玄天宗世界设定总纲 V1.6.1 · 全量合并锁定版** is the `BASE_WORLD_CANON`.

It is the integrated master for geography, nine peaks, institutions, architecture hierarchy and every field not explicitly superseded by a later registered LOCKED scoped module.

### Scoped post-Canon locked assets

A later explicit user-approved LOCKED specialist module may supersede V1.6.1 **only inside its registered lock scope**.

Current confirmed scoped override:

- `OVR-BEAST-001` — six high-tier beasts.

Examples:
- 玄雷夔: one leg, **no horns**.
- 九天玄应龙: **wingless** Oriental ancestral dragon; normal physical body length 1200m.

Do not use “newer file wins” as a general rule. Drafts, review files, prompts and concept images cannot override Canon on their own.

## Recovered non-Digital-Twin branches

### 《玄元炼气诀》

Recovered text lineage, ancient-book layout iterations, generated pages and a **214-page `玄元炼气诀_古籍真本版_无标点.pdf`** are registered under `XUANYUAN_LIANQI`.

Archive guide: `docs/archive/xuanyuan_lianqi/README.md`.

### 数字玄天宗

The historical V0.3 living-world/canon-engine snapshot is mirrored at:

`docs/archive/digital_xuantianzong/STATUS_2026-08-04.md`

Its then-current V1.3 authority is historical; current world authority is V1.6.1/current scoped locks.

### Visual-development lineage

Historical gate, Xuantian Hall, nine-peak maps and strategic mother-image families are registered and classified rather than discarded.

Archive guide: `docs/archive/visual_assets/README.md`.

### Promo film / DJI / 小云雀 lineage

The approved direction is **宣传片，不是纪录片**, with no invented protagonist and a real-DJI physical-flight premise.

Archive guide: `docs/archive/promo_film/README.md`.

### Phone-content / spirit-stone lineage

Real-phone imaging rules and the outer-disciple 五蕴测灵石 introduction branch are preserved at:

`docs/archive/phone_content/README.md`.

## Current Digital Twin status

### V0.1 — Engineering Proof

Completed and preserved under `build/`.

It proved:

`registered world data → Blender → .blend → render → 15s MP4`

V0.1 is not the visual-spatial target: its flat base, isolated cone massing and disk-like Xuantian Peak exposed implementation gaps against F1/C1/E1.

### V0.2 — Mini Spatial Proof

Engineering validation is complete, but human visual acceptance remains open. V0.2.2 uses a single continuous Xuantian mountain mesh, local terrain-occlusion gate discovery, stronger neutral twin-sword projection and a settled centreline gate run under `build/v0.2/`.

Primary scope:
- final 800–1000m of 十二里入山古道;
- continuous valley/mountain-pass massing around 玄岳关;
- 玄岳关 + 双阙剑;
- 300–500m interior valley;
- distant heavy inverted 玄天峰 silhouette;
- physically plausible DJI motion;
- Canon + Geometry + Visual + Camera + Deterministic-Rebuild validation.

## Non-negotiable topology

- Nine formal peaks.
- Only 玄天峰 is a large floating main peak.
- Eight terrestrial peaks form continuous ridge systems, not isolated cones.
- Xuantian Peak is a heavy inverted mountain, never a plate/UFO.
- The ceremonial axis bends with terrain and is never a straight sky stair.
- E1 strategic stitched camera is not a real DJI single-lens shot.

## Downstream boundary

V0.2.2 engineering checks pass, while both visual and camera-visual acceptance remain `PENDING_HUMAN_REVIEW`. Its `NON_CANON_PROXY` graybox geometry is not automatically promoted to Canon or final high-detail art, and GitHub Issue #2 remains open until explicit human approval.
