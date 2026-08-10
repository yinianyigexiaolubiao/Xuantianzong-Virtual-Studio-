# Generation pipeline

1. Open `promo_film_01_production.blend`, which is a non-destructive copy derived from the accepted V0.2 scene.
2. Render each real-DJI camera as `blender_previz.mp4` at 16:9 / 24fps.
3. Render start/middle/end Eevee keyframes as the geometry and composition anchors.
4. For Seedance 2.0, submit the shot's `seedance_prompt.txt` with the three keyframes plus `blender_previz.mp4`; the first pass is locked to two 1080p / 16:9 candidates per shot.
5. Reject any candidate that drifts Canon, alters the locked Xuantian Peak silhouette, changes Xuanyue Gate/Twin Sword dimensions, collides with the gate, or loses real-DJI inertia.
6. If the best candidate has unstable transitions, use the matching `wan_flf2v_prompt.txt` with `start.png` and `end.png`; the local environment currently has no Wan 2.2 executor, so this is an external-ready package.
7. Replace the matching Blender previz segment with the selected generated candidate, preserve the 39-second EDL, then run the final color/sound/title pass.

Current assembly uses lossless H.264 concat for the silent roughcut. The publish candidate adds one encoding pass, a restrained corrective grade and a procedural rights-clear temporary score.

The direct Ark first pass uses `doubao-seedance-2-0-260128`. All 12 tasks completed successfully. `promo_film_01_seedance_firstpass.mp4` is a separate 39-second candidate-01 assembly and does not overwrite the roughcut or publish candidate.
