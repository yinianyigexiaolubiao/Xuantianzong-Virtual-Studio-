# Digital Twin V0.1 validation report

- Blender: 4.5.5 LTS
- World data validator: PASS before and after delivery (`python tools/validate_world_data.py`)
- Formal peaks: PASS — exactly 9
- Floating main peak: PASS — only 玄天峰; 1210–1680m vertical envelope (470m)
- Ancient road: PASS — A0–A8 locked controls, 6.0km Canon-declared length
- 玄岳关: PASS — anchor (0, 3700, 610m), body 52×18×34m
- 双阙剑: PASS — 44m each, 68m axis distance, V10 double-edged straight-sword proxy
- 九段玄阶: PASS — 10 locked nodes, 9 stages, 3600 generated tread boxes, 7.2km Canon-declared stage total, visibly bent
- B1 core assets: PASS — all 7 required locked anchors/envelopes generated
- Spatial continuity: PASS — 接引院 A0 proxy → ancient road A0–A8 → 玄岳关/axis shared anchor → nine-stage stairs → 接天阵台 → B1 core
- 玄天殿: PASS — visual rank S / ultimate visual center metadata preserved
- DJI preview: PASS — 360 frames at 24fps (15s); 25 sampled frames inside gate depth; maximum frame displacement 0.740m; no wall/lintel collision or teleport
- Global graybox: `build/xuantianzong_digital_twin_v0.1_global_graybox.png`
- Gate preview: `build/xuantianzong_digital_twin_v0.1_gate_preview.mp4`

## Remaining NON_CANON_PROXY items

The following remain engineering graybox/provisional by design and are not promoted to Canon:

- `XTZ_ASSET_XTZ-BLD-002_玄天殿`
- `XTZ_ASSET_XTZ-BLD-010_接天阵门`
- `XTZ_ASSET_XTZ-BLD-011_礼制等候院`
- `XTZ_ASSET_XTZ-BLD-012_祖师堂`
- `XTZ_ASSET_XTZ-BLD-013_掌门院`
- `XTZ_ASSET_XTZ-BLD-014_魂灯殿`
- `XTZ_ASSET_XTZ-PLT-001_接天阵台`
- `XTZ_CAM_DJI_28MM_PROXY`
- `XTZ_CAM_E1_C_50MM_PROXY`
- `XTZ_CAM_E1_L_50MM_PROXY`
- `XTZ_CAM_E1_R_50MM_PROXY`
- `XTZ_CAM_GLOBAL_GRAYBOX`
- `XTZ_GATE_LeftMass`
- `XTZ_GATE_MainLintel`
- `XTZ_GATE_RightMass`
- `XTZ_JIEYIN_COURTYARD_NON_CANON_PROXY`
- `XTZ_NINE_STAGE_STAIRS_3600_NON_CANON_PROXY`
- `XTZ_PEAK_XTZ-MTN-001_玄天峰`
- `XTZ_PEAK_XTZ-MTN-002_天剑峰`
- `XTZ_PEAK_XTZ-MTN-003_寒渊峰`
- `XTZ_PEAK_XTZ-MTN-004_紫微峰`
- `XTZ_PEAK_XTZ-MTN-005_丹霞峰`
- `XTZ_PEAK_XTZ-MTN-006_万木峰`
- `XTZ_PEAK_XTZ-MTN-007_灵兽峰`
- `XTZ_PEAK_XTZ-MTN-008_天工峰`
- `XTZ_PEAK_XTZ-MTN-009_镇岳峰`
- `XTZ_SWORD_EAST_Blade`
- `XTZ_SWORD_EAST_Grip`
- `XTZ_SWORD_EAST_Guard`
- `XTZ_SWORD_EAST_Pommel`
- `XTZ_SWORD_WEST_Blade`
- `XTZ_SWORD_WEST_Grip`
- `XTZ_SWORD_WEST_Guard`
- `XTZ_SWORD_WEST_Pommel`
- `XTZ_TERRAIN_ValleyMass_NON_CANON_PROXY`
- `XTZ_XUANTIAN_SUMMIT_CROWN_NON_CANON_PROXY`

Notable categories: all detailed peak/terrain surfaces; 接引院 volume; detailed road edges; inter-node stair/platform construction; 玄岳关 and V10 sword art geometry; all seven B1 building shapes; E1 rig transforms; global inspection camera; DJI flight path.

Canon note: the 7.2km value is the locked sum of the nine stage lengths. The 10 A1 control nodes are preserved verbatim; detailed inter-node route geometry remains Proxy pending D2.
