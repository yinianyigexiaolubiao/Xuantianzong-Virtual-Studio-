# F1 Inheritance and Digital Twin V0.2 Rules

## Why this exists

Digital Twin V0.1 proved the engineering chain but exposed a mismatch with the older, more mature F1 spatial-control logic: flat base plane, disconnected cone peaks, hard-polyline route reading and a disk-like Xuantian Peak silhouette.

V0.2 MUST correct those implementation artifacts by inheriting F1. It is not a new terrain concept.

## Source stack

V0.2 spatial implementation shall read the following in order:

`V1.6.1 → A1 → B1 → C1 → E1 → F1 → current V0.2 implementation`

G1 is future hero-image control and must not rewrite geometry.

## F1 rules that are now mandatory

### 1. Continuous terrain instead of isolated cones

F1 uses a 100m regular terrain grid at whole-sect massing level.

Required macro ridge chains:
- West: 天剑峰 → 镇岳峰 → 天工峰 → 灵兽峰
- East: 寒渊峰 → 紫微峰 → 丹霞峰 → 万木峰

The eight terrestrial peaks must share ridges/saddles/foothill masses. Their locked A1 centers and summit/foot envelopes remain unchanged.

### 2. Central valley must remain a valley

The central entry corridor must be a terrain valley with layered side ridges, roads and water corridors. It must not read as:
- a flat board;
- a trench cut through a heightfield;
- a perfectly symmetric artificial canyon;
- a straight ceremonial boulevard.

### 3. Rear mountain massing is part of the world

North of Xuantian Peak, create proxy massing for 地根背脊 and 伏渊岭 so that the rear zone exists spatially and restricted sites remain occluded from prohibited front views.

### 4. Xuantian Peak must be a heavy inverted mountain

Locked control envelope:
- plan envelope: approx. 1.45km × 1.05km;
- natural highest ridge: 1680m;
- main palace terrace: 1605–1615m;
- deepest inverted spire: 1210m;
- main vertical body depth: 400–470m.

Proxy silhouette requirements:
- irregular natural upper mountain crown;
- broad suspended mountain mass;
- tapering inverted lower rock body;
- identifiable bottom spire;
- no disk, saucer, thin slab, regular ellipse or UFO reading.

### 5. Building proxies remain envelopes

B1 key assets remain simple blocks at this stage. They exist to validate hierarchy and spatial occupancy, not architectural detail.

Primary test:
> mountain mass > building mass; nature > artificial construction.

### 6. E1 strategic-view checks remain useful

E1 is not the DJI camera, but V0.2 should preserve an E1-style QC view because it tests whole-world hierarchy.

E1 checks:
- Xuantian Peak is the first/ultimate visual center.
- Xuanyue Gate + Twin Swords are readable foreground anchors.
- at least six terrestrial peaks have independent silhouettes;
- all eight terrestrial peaks remain grounded and ridge-connected;
- Xuantian Peak inverted lower edge is substantially visible;
- rear ridges exist while restricted rear assets stay hidden.

## V0.2 mini-spatial scope

Primary detailed zone:
- final 800–1000m of the Twelve-Li Ancient Road;
- terrain pass into Xuanyue Gate;
- Xuanyue Gate and Twin Swords;
- 300–500m interior valley after the gate;
- distant Xuantian Peak silhouette.

The remainder of the 8km × 12km world may stay low-resolution massing, but must not contradict F1 topology.

## Path implementation rule

A1 control points are macro constraints, not directly visible hard corners.

Implementation sequence:
`locked A1 nodes → smooth terrain-conforming centerline → local switchbacks/platforms → visible road/stair geometry`

Do not move the locked nodes.

## Camera implementation rule

DJI path must separate:
- position curve;
- body/yaw curve;
- gimbal pitch/target curve;
- speed profile.

Minimum motion QC should report speed, acceleration, jerk and yaw-rate maxima. A mathematically continuous constant-rate rail move is not sufficient.

## Graybox rendering standard

Use a bright neutral gray/white QC setup with readable shadows. V0.2 QC is for silhouette, scale, occlusion and terrain continuity; dark cinematic atmosphere is counterproductive at this stage.

## Validation ladder

V0.2 must pass three distinct layers:

1. `Canon Validator` — source data unchanged and internally valid.
2. `Geometry Validator` — generated transforms, bounds, clearances, collisions and continuity valid.
3. `Visual QC` — fixed renders show the intended mountain/valley/silhouette reading.

A PASS in one layer does not imply PASS in another.

## V0.1 preservation

Do not overwrite V0.1 delivery artifacts. They are retained as `Engineering Proof` evidence that the generator pipeline works.
