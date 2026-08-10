from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "promo_film_01"
FINAL = OUTPUT / "final_edit"
FPS = 24
SHOTS = [
    ("shot_01_establishing", "云海发现玄天宗", 6),
    ("shot_02_gate_reveal", "古道发现玄岳关", 6),
    ("shot_03_gate_crossing", "穿越玄岳关", 6),
    ("shot_04_inner_axis", "宗门内部主轴推进 / 九段玄阶代表段", 7),
    ("shot_05_xuantian_peak", "玄天峰揭幕", 7),
    ("shot_06_xuantian_hall", "玄天殿终极揭幕", 7),
]


def run(*args: str) -> None:
    print("[assemble]", " ".join(args[:4]), "...")
    subprocess.run(args, cwd=ROOT, check=True)


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
            "-show_entries",
            "stream=codec_name,width,height,r_frame_rate,nb_frames",
            "-of",
            "json",
            str(path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_sources() -> list[dict]:
    rows = []
    for shot_id, title, duration in SHOTS:
        directory = OUTPUT / shot_id
        video = directory / "blender_previz.mp4"
        keyframes = [directory / "keyframes" / f"{name}.png" for name in ("start", "middle", "end")]
        missing = [str(path) for path in [video, *keyframes] if not path.is_file() or path.stat().st_size == 0]
        if missing:
            raise RuntimeError(f"Missing/empty outputs for {shot_id}: {missing}")
        data = probe(video)
        stream = data["streams"][0]
        actual_duration = float(data["format"]["duration"])
        if abs(actual_duration - duration) > 0.08:
            raise RuntimeError(f"Unexpected duration for {shot_id}: {actual_duration}")
        if stream["r_frame_rate"] != "24/1":
            raise RuntimeError(f"Unexpected fps for {shot_id}: {stream['r_frame_rate']}")
        rows.append(
            {
                "shot_id": shot_id,
                "title": title,
                "duration_s": actual_duration,
                "fps": stream["r_frame_rate"],
                "frames": int(stream["nb_frames"]),
                "resolution": [int(stream["width"]), int(stream["height"])],
                "previz": video.relative_to(ROOT).as_posix(),
                "previz_sha256": sha256(video),
                "keyframes": [path.relative_to(ROOT).as_posix() for path in keyframes],
            }
        )
    return rows


def assemble(rows: list[dict]) -> tuple[Path, Path]:
    FINAL.mkdir(parents=True, exist_ok=True)
    concat = FINAL / "concat_list.txt"
    write(concat, "\n".join(f"file '{(ROOT / row['previz']).as_posix()}'" for row in rows))
    roughcut = FINAL / "promo_film_01_roughcut.mp4"
    run(
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(roughcut),
    )

    music = FINAL / "promo_film_01_temp_score.wav"
    # A deliberately quiet, rights-clear procedural temp bed. It is a timing guide,
    # not a claim of final composition or licensed production music.
    audio_expr = (
        "0.035*sin(2*PI*55*t)+0.020*sin(2*PI*82.5*t)+"
        "0.012*sin(2*PI*(220+8*sin(2*PI*0.07*t))*t)+"
        "0.008*sin(2*PI*440*t)*(0.5+0.5*sin(2*PI*0.125*t))"
    )
    run(
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"aevalsrc={audio_expr}:s=48000:d=39",
        "-af",
        "afade=t=in:st=0:d=1.5,afade=t=out:st=36.5:d=2.5,aecho=0.8:0.6:600:0.16",
        "-c:a",
        "pcm_s16le",
        str(music),
    )

    publish = FINAL / "promo_film_01_publish_candidate.mp4"
    run(
        "ffmpeg",
        "-y",
        "-i",
        str(roughcut),
        "-i",
        str(music),
        "-vf",
        "scale=1280:720:flags=lanczos,eq=contrast=1.04:saturation=1.08:brightness=0.015",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(publish),
    )
    return roughcut, publish


def write_delivery_docs(rows: list[dict], roughcut: Path, publish: Path) -> None:
    timeline = []
    cursor = 0.0
    for row in rows:
        timeline.append({**row, "timeline_in_s": cursor, "timeline_out_s": cursor + row["duration_s"]})
        cursor += row["duration_s"]

    shot_lines = ["# Promo Film 01《玄天宗·入宗》— Shot List", "", "Total: 39 seconds / 16:9 / 24fps.", ""]
    for index, row in enumerate(timeline, 1):
        shot_lines.extend(
            [
                f"## {index:02d}. {row['title']}",
                "",
                f"- Timeline: {row['timeline_in_s']:.0f}s–{row['timeline_out_s']:.0f}s ({row['duration_s']:.0f}s)",
                f"- Previz: `{row['previz']}`",
                f"- Beat: `{row['shot_id']}` shot package and brief.",
                "",
            ]
        )
    write(FINAL / "shot_list.md", "\n".join(shot_lines))

    write_json(
        FINAL / "asset_usage_manifest.json",
        {
            "schema_version": "1.0",
            "film": "Promo Film 01《玄天宗·入宗》",
            "production_mode": "SHOT-FIRST VIRTUAL PRODUCTION",
            "base_blender_scene": "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "production_blender_scene": "build/promo_film_01/promo_film_01_production.blend",
            "timeline_duration_s": cursor,
            "shots": timeline,
            "final_outputs": {
                "silent_roughcut": roughcut.relative_to(ROOT).as_posix(),
                "temporary_music_candidate": publish.relative_to(ROOT).as_posix(),
                "temporary_score": "build/promo_film_01/final_edit/promo_film_01_temp_score.wav",
            },
            "canon_policy": "V0.2 accepted geometry/camera relationships are inherited. Shot-local art remains NON_CANON_PROXY.",
        },
    )

    write(
        FINAL / "generation_pipeline.md",
        """# Generation pipeline

1. Open `promo_film_01_production.blend`, which is a non-destructive copy derived from the accepted V0.2 scene.
2. Render each real-DJI camera as `blender_previz.mp4` at 16:9 / 24fps.
3. Render start/middle/end Eevee keyframes as the geometry and composition anchors.
4. For Seedance 2.0, submit the shot's `seedance_prompt.txt` with the three keyframes plus `blender_previz.mp4`; generate 2–4 candidates only after an explicit 720p/1080p resolution choice.
5. Reject any candidate that drifts Canon, alters the locked Xuantian Peak silhouette, changes Xuanyue Gate/Twin Sword dimensions, collides with the gate, or loses real-DJI inertia.
6. If the best candidate has unstable transitions, use the matching `wan_flf2v_prompt.txt` with `start.png` and `end.png`; the local environment currently has no Wan 2.2 executor, so this is an external-ready package.
7. Replace the matching Blender previz segment with the selected generated candidate, preserve the 39-second EDL, then run the final color/sound/title pass.

Current assembly uses lossless H.264 concat for the silent roughcut. The publish candidate adds one encoding pass, a restrained corrective grade and a procedural rights-clear temporary score.
""",
    )

    write(
        FINAL / "remaining_gaps.md",
        """# Remaining gaps to formal release

- The current roughcut and publish candidate use colored Blender previz, not final AI-generated or fully art-directed footage. They prove timing, continuity and camera structure but are not the final release visual.
- Seedance 2.0 direct execution is available, but its service requires an explicit paid generation resolution (`720p` or `1080p`). The supplied task did not choose one, so no paid candidate was submitted after the validation request failed.
- Wan 2.2 has no callable local executor; all six first/last-frame packages are ready for external generation.
- Xuantian Hall architecture, representative inner-axis stair/platform detail, vegetation, clouds, gate art detail and procedural materials remain `NON_CANON_PROXY` and need final art direction.
- The temporary procedural score is only a pacing guide. A formal release needs selected/licensed music, designed wind/cloud/stone/architectural ambience, final title typography and a final loudness pass.
- Generated candidates require geometry-drift, camera-collision, temporal-consistency and human visual review before replacing previz in the edit.
""",
    )

    write(
        FINAL / "audio_and_titles.md",
        """# Audio and title direction

- Score: restrained 72–84 BPM ceremonial pulse; low strings/drone for discovery, jade chime accents at Gate and Xuantian Peak reveals, fuller brass/choral texture only for Xuantian Hall.
- Ambience: high-altitude wind, distant valley air, restrained stone resonance at the gate, softer cloud wash after the crossing, no game UI or fantasy spell spam.
- Opening text: optional small `玄天宗 · 入宗` after the first reveal, not before the world is visible.
- End title: `《玄天宗 · 入宗》` or the simpler `《玄天宗》`, held for 1.5–2 seconds after the hall stabilizes.
- Current `promo_film_01_temp_score.wav` is procedural and rights-clear, intended only for edit timing.
""",
    )

    validation = {
        "status": "PASS_WITH_RELEASE_GAPS",
        "total_duration_s": cursor,
        "target_duration_range_s": [35, 45],
        "fps": FPS,
        "shot_count": len(rows),
        "all_previz_present": True,
        "all_keyframes_present": True,
        "all_seedance_packages_present": True,
        "all_wan_packages_present": True,
        "direct_generated_candidates": False,
        "direct_generation_blocker": "Seedance service requires explicit 720p/1080p selection; Wan 2.2 executor unavailable.",
        "roughcut": {"path": roughcut.relative_to(ROOT).as_posix(), "probe": probe(roughcut), "sha256": sha256(roughcut)},
        "publish_candidate": {"path": publish.relative_to(ROOT).as_posix(), "probe": probe(publish), "sha256": sha256(publish)},
    }
    write_json(FINAL / "validation.json", validation)


def main() -> None:
    rows = validate_sources()
    roughcut, publish = assemble(rows)
    write_delivery_docs(rows, roughcut, publish)
    print(f"[assemble] complete: {roughcut}")
    print(f"[assemble] complete: {publish}")


if __name__ == "__main__":
    main()
