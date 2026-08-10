#!/usr/bin/env python3
"""Create objective review frames, contact sheets, and the candidate-01 first pass."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "promo_film_01"
REVIEW = BUILD / "review"
SHOTS = (
    "shot_01_establishing",
    "shot_02_gate_reveal",
    "shot_03_gate_crossing",
    "shot_04_inner_axis",
    "shot_05_xuantian_peak",
    "shot_06_xuantian_hall",
)
POSITIONS = (("start", 0.02), ("25%", 0.25), ("50%", 0.50), ("75%", 0.75), ("end", 0.98))


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/msyh.ttc"),
    ):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def extract_frames() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    for shot in SHOTS:
        frame_dir = REVIEW / "frames" / shot
        frame_dir.mkdir(parents=True, exist_ok=True)
        rows: list[list[Path]] = []
        for index in (1, 2):
            video = BUILD / shot / "generated_candidates" / f"candidate_seedance_{index:02d}.mp4"
            clip_duration = duration(video)
            row = []
            for label, fraction in POSITIONS:
                target = frame_dir / f"candidate_seedance_{index:02d}_{label.replace('%', 'pct')}.jpg"
                run(
                    "ffmpeg", "-y", "-loglevel", "error", "-ss", f"{clip_duration * fraction:.4f}",
                    "-i", str(video), "-frames:v", "1", "-q:v", "2", str(target),
                )
                row.append(target)
            rows.append(row)
        make_sheet(shot, rows)


def make_sheet(shot: str, rows: list[list[Path]]) -> None:
    cell_w, cell_h, label_h = 384, 216, 32
    canvas = Image.new("RGB", (cell_w * 5, (cell_h + label_h) * 2 + 48), (22, 22, 22))
    draw = ImageDraw.Draw(canvas)
    small = font(20)
    title = font(24)
    draw.text((12, 8), shot, fill="white", font=title)
    for row_index, row in enumerate(rows):
        y0 = 48 + row_index * (cell_h + label_h)
        for column, path in enumerate(row):
            image = Image.open(path).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            x0 = column * cell_w
            canvas.paste(image, (x0, y0))
            position_label = POSITIONS[column][0]
            draw.rectangle((x0, y0 + cell_h, x0 + cell_w, y0 + cell_h + label_h), fill=(12, 12, 12))
            draw.text(
                (x0 + 8, y0 + cell_h + 4),
                f"candidate_{row_index + 1:02d}  {position_label}",
                fill="white",
                font=small,
            )
    short_shot = "_".join(shot.split("_")[:2])
    canvas.save(REVIEW / f"{short_shot}_candidates.jpg", quality=94, subsampling=0)


def build_first_pass() -> None:
    concat_file = REVIEW / "firstpass_concat.txt"
    concat_file.write_text(
        "".join(
            f"file '{(BUILD / shot / 'generated_candidates' / 'candidate_seedance_01.mp4').as_posix()}'\n"
            for shot in SHOTS
        ),
        encoding="utf-8",
    )
    output = BUILD / "promo_film_01_seedance_firstpass.mp4"
    run(
        "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-map", "0:v:0", "-c", "copy", "-movflags", "+faststart", str(output),
    )
    concat_file.unlink()


if __name__ == "__main__":
    extract_frames()
    build_first_pass()
