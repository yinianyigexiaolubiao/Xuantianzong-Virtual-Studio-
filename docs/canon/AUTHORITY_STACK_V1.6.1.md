# Canon Authority Stack — V1.6.1

## Purpose

This document is the engineering conflict-resolution order for all Xuantianzong Virtual Studio work.

## Authority order

1. **V1.6.1 explicit canon text and locked numeric values**
2. **Approved technical-control data derived from V1.6.1**
   - A1: coordinates, elevation, terrain, roads, water, rear zone, gate/sword scale
   - B1: peak functions, population, key-asset layout, traffic/airspace
   - C1: visual hierarchy, materials, image/video rules, high-tier beast appearance policy
3. **E1 fixed master-camera control** for V12 strategic-image reproduction only
4. **F1 graybox/proportion-control principles** for spatial validation
5. **G1 formal master-image control** for later hero-image production
6. Story, shot list, prompt, temporary concept art

Lower levels may never rewrite higher levels.

## V1.6.1 explicit supersession

V1.6.1 is the sole current canon and supersedes dispersed execution of earlier V1.6/A1/B1/C1 files. The older files remain useful as technical/source history only where they agree with V1.6.1.

Known superseded historical concepts include:
- five-peak versions;
- old color/material systems that conflict with C1/V1.6.1;
- early smaller sacred-tree sizes;
- old Ruomu coordinates;
- old assumptions about high-tier beasts being absolutely hidden from ordinary filming;
- interpretations that turn Xuantian Peak into a thin floating platform.

## Canon vs validation state

A locked design value is not automatically visually validated.

Use these engineering labels:

- `LOCKED_DESIGN`: approved canon/design value, not yet proven in rendered spatial context.
- `LOCKED_GEOMETRY_VALIDATED`: build result matches the locked transform/envelope and passes geometry tests.
- `LOCKED_VISUALLY_VALIDATED`: the locked design has also passed fixed-camera / DJI spatial-reading review.
- `NON_CANON_PROXY`: provisional geometry, path, camera transform or asset shape; never promotes itself to Canon.

Example: 双阙剑 44m height is Canon and geometry-validated, but its final visual dominance from the gate-approach camera remains subject to visual validation.

## Non-negotiable world rules

- Exactly nine formal peaks.
- Only 玄天峰 is a large floating main peak.
- Eight terrestrial peaks form continuous mountain systems via ridges, saddles and valleys.
- 玄天峰 must read as a full, heavy inverted mountain; never a disk, plate, oval platform or UFO.
- Mountains remain larger than buildings.
- The central ceremonial route bends with terrain and cannot be a straight sky stair.
- 玄岳关 and 双阙剑 are strong foreground anchors; 玄天峰/玄天殿 are the ultimate distant center.
- Rear-zone restricted assets are hidden by terrain from prohibited front views.
- E1 is a virtual strategic master camera, not a real DJI camera.

## Change-control rule

If visual tests expose a problem with a locked value:

1. Do not silently edit the JSON.
2. Mark the value `LOCKED_DESIGN_NOT_VISUALLY_VALIDATED` in the review report.
3. Re-test with better proxy geometry/camera implementation first.
4. Only propose a Canon change if the failure persists after implementation artifacts are ruled out.
