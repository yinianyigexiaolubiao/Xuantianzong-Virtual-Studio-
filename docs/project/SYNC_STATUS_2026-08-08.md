# 玄天宗项目归档同步状态 — 2026-08-08

## Definition of completion

This report separates two goals that must not be conflated:

1. **Project representation completeness** — every recovered branch/artifact is classified and represented in GitHub with an explicit evidence/sync state.
2. **Physical binary mirroring completeness** — exact bytes for every historical File Library PDF/PNG/OBJ/GLB/TXT are physically copied into GitHub.

The first goal is enforceable by this repository. The second depends on a transport path that can expose exact File Library bytes.

## Project representation status

Mandatory modules represented in `data/project/master_project_registry_2026-08-08.json`:

- [x] CANON_AND_WORLD
- [x] DIGITAL_TWIN
- [x] VISUAL_ASSETS
- [x] PROMO_FILM_AND_DJI
- [x] PHONE_CONTENT
- [x] XUANYUAN_LIANQI
- [x] DIGITAL_XUANTIANZONG
- [x] BEASTS_AND_SACRED_TREES
- [x] HISTORICAL_ARCHIVE

## Exact content currently mirrored in GitHub

Examples include:

- Digital Twin Blender/Python/data system;
- V0.1 `.blend`, PNG, MP4 and reports;
- Canon/authority/subregistry documentation and machine registries;
- recovered Digital Xuantianzong V0.3 historical status snapshot;
- recovered project briefs for promo-film/DJI and phone-content branches;
- recovered project-level documentation for 《玄元炼气诀》 and visual-asset lineage.

## Direct File Library artifacts not physically mirrored

The archive has direct evidence for important binaries/texts that the current File Library search interface can identify/open but does not expose as arbitrary raw bytes to the GitHub connector. These are deliberately marked with non-mirrored states.

Major examples:

### 《玄元炼气诀》

- preferred long source TXT `玄元炼气诀_真传重写版_无说明.txt`;
- 214-page `玄元炼气诀_古籍真本版_无标点.pdf`;
- other vertical-layout PDF iterations;
- ancient-book page PNGs and generated page batches.

### Historical visual assets

- Xuantian Hall mother-image/revision family;
- early gate/spirit-stone images;
- nine-peak maps V1/V3;
- strategic whole-sect images V5/V6/V11;
- visual spec sheets from the V1.6 transition.

### Historical source/control documents

Many DOCX/PDF originals remain File-Library binaries while their role/current authority is represented by GitHub registries and machine projections.

### F1/F2/F3 binary lineage

- F1 OBJ: directly found in File Library; metadata registered;
- F2 GLBs/PNGs: manifest-verified with hash/size states in the Canon asset registry;
- selected F3 outputs: referenced-only unless stronger evidence is recovered.

## Why these are not falsely copied

A GitHub file with reconstructed/truncated text is **not** an exact archive. A registry entry with `FILE_LIBRARY_ONLY_BINARY`, `FILE_LIBRARY_ONLY_TEXT`, `MANIFEST_VERIFIED` or `REFERENCED_ONLY` is more reliable than pretending a partial reconstruction is the original.

## Migration rule

If exact bytes later become available (user upload, direct file export, local project folder, or another connector that exposes them), migrate them into an appropriate `archive/` or external release/LFS storage location and change the corresponding `sync_state` to `GITHUB_MIRRORED` only after hash/size verification.

## Current engineering use

The absence of historical binary mirroring does **not** authorize Codex to recreate them from memory. Use current Canon/registered controls for active work; historical binaries are reference/evidence assets only unless formally promoted.
