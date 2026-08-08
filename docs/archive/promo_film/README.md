# 玄天宗宣传片 / Real-DJI Production Archive

This file preserves production decisions that were developed in project conversation but did not consistently exist as standalone files.

## Current creative direction

- **宣传片，不是纪录片。**
- Do not invent a random hero/protagonist to carry the film.
- The visual premise is: **a real DJI drone is physically flying through a real, persistent Xuantianzong**.
- Camera motion must remain physically plausible. The camera cannot teleport, orbit through walls, ignore inertia or use impossible fantasy-camera paths merely because an AI model permits it.
- The sect itself is the subject: scale, hierarchy, approach, reveal and spatial continuity are more important than character drama.

## Current Canon imaging boundary

From C1/E1/current Canon:

- real DJI: about **24–35mm equivalent**, 16:9;
- center-forward movement with a gradual rise;
- modest low-angle/upward framing where appropriate;
- limited yaw rather than constant dramatic orbiting;
- no extreme fisheye;
- preserve people, gate structures, trees, boats or other known-scale objects when useful so the audience can read giant scale;
- do not pass through ancestor-beast heads, eyes, thunder/fire danger domains or primary array eyes;
- E1/V12 50mm three-panel strategic view is a virtual master-image camera and must never be falsely described as one real DJI lens shot.

## Production architecture developed in the project

The long-term workflow is:

`Canon → 3D/Digital Twin → Camera Path → depth/normal/mask/pose controls → AI video model → visual QC → edit`

ComfyUI, Seedance, Wan or future generators are **render/orchestration layers**, not the source of Xuantianzong geography.

Real-world DJI footage may later be used for **camera-motion extraction** (camera tracking / VGGT / SLAM style workflow) so the flight dynamics can drive a Blender camera. The real clip is not allowed to redefine the sect's topology.

## 小云雀 / video-model workflow history

Project conversation explored combining the locked Xuantianzong world with 小云雀/video generation. The accepted principle was:

1. lock what is physically present in the shot from Canon/master assets;
2. specify real drone optics and flight path;
3. give the video model only the shot-local visual task;
4. never ask the model to invent the sect layout;
5. compare the result against Canon/Digital-Twin references and reject geometry drift.

This archival file preserves the workflow principle. Exact historical prompt strings were not recovered as standalone File Library files and therefore are not falsely reconstructed as exact originals.

## Historical 45-second promo-film intent

An earlier three-part cinematic concept used:

1. cloud-sea approach → gate reveal → pass Xuanyue Gate;
2. progress through the sect → mountain hierarchy opens up;
3. main-peak reveal → Xuantian Hall as final visual payoff.

**Retain only the cinematic rhythm.** The old geometry contained obsolete assumptions such as a straight white-jade axis and five-peak readings. Current V1.6.1/A1/F1 topology overrides those details.

## Historical first 10 stills

A batch of ten early shot-exploration stills was previously packaged with titles similar to:

1. 玄天宗外部远景
2. 玄岳关正面
3. 穿过玄岳关向内看
4. 宗门主轴航拍
5. 五大主峰整体
6. 主轴前进起始
7. 主轴前进中段
8. 五峰展开
9. 玄天殿方向
10. 玄天殿远距离首次显现

These are **Concept / Shot Exploration only**. Their five-peak/straight-axis content is superseded and must not become Canon or Digital-Twin geometry.

## Current promo-film shot rule after V0.1 QC

V0.1 proved the engineering chain but failed visual/camera acceptance. The immediate camera proof is intentionally smaller:

- final ancient-road valley approach;
- progressive Xuanyue Gate reveal;
- Twin Swords form readable left/right framing;
- slight rise and controlled deceleration;
- clean central-gate pass;
- after the gate, the space must **open up** into interior terrain/route depth with distant Xuantian Peak silhouette.

No more empty-sky/flat-ground ending.

## Visual language

- bright, clear Chinese xianxia;
- not dark Western fantasy;
- warm/white jade hierarchy + restrained gold + small vermilion where Canon allows;
- Twin Swords: ice-blue only on blade edges/limited array patterns, not a global blue cast;
- Xuantian Hall and Xuantian Peak retain highest hierarchy;
- Tyndall/golden natural light may be used with restraint;
- clouds/fog and subtle qi support depth, never replace geometry.

## Archive status

- Production decisions: `CHAT_RECORDED_SPEC` + C1/E1 controls.
- Exact old standalone 小云雀 prompts: **not directly recovered as files**.
- Historical early still binaries: not currently mirrored to GitHub and remain reference-only unless recovered separately.
- Current executable camera work lives in the Digital Twin branch and Issue #2.
