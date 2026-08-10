#!/usr/bin/env python3
"""Submit, poll, and download Promo Film 01 Seedance 2.0 candidates."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "promo_film_01"
API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
MODEL = "doubao-seedance-2-0-260128"
SHOTS = {
    "shot_01_establishing": (6, "f4848479-37b8-4c2e-b15b-656b76a3caf7"),
    "shot_02_gate_reveal": (6, "54f8c8e5-b40d-448a-bb1e-ff42c14ba6b9"),
    "shot_03_gate_crossing": (6, "bf1aa7d3-fc73-4d2e-9ac5-04a64f43303c"),
    "shot_04_inner_axis": (7, "609b63f4-f52f-4b40-9b63-02d32274f0fa"),
    "shot_05_xuantian_peak": (7, "a46d160c-94d2-41ab-8289-9874b4a5aaa7"),
    "shot_06_xuantian_hall": (7, "ab96bde7-2342-47c0-9700-5bb254ba11a2"),
}
S3_PREFIX = (
    "https://chatcut-production-mainbucketbucket-oxvbnfsx.s3.us-east-1.amazonaws.com/"
    "users/s2X8jwWe1zrAPBXF4trwcka230mIkKJ2/projects/"
    "f0b48b42-abd4-4cf4-9370-480b5e3f76e8/assets/video"
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def request(method: str, url: str, payload: dict | None = None) -> dict:
    key = os.environ.get("ARK_API_KEY")
    if not key:
        raise RuntimeError("ARK_API_KEY is not set")
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def data_url(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def prompt_for(shot_dir: Path) -> str:
    prompt = (shot_dir / "seedance_prompt.txt").read_text(encoding="utf-8")
    prompt = prompt.replace("参考视频：blender_previz.mp4", "参考视频1中的 Blender 预演")
    prompt = prompt.replace(
        "参考图：keyframes/start.png、keyframes/middle.png、keyframes/end.png",
        "参考图片1中的起始关键帧、图片2中的中段关键帧、图片3中的结束关键帧",
    )
    return prompt


def manifest_path(shot: str) -> Path:
    return BUILD / shot / "generated_candidates" / "candidate_manifest.json"


def load_manifest(shot: str, duration: int, prompt: str) -> dict:
    path = manifest_path(shot)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0",
        "shot_id": shot,
        "model": MODEL,
        "resolution": "1080p",
        "aspect_ratio": "16:9",
        "duration_s": duration,
        "fps": 24,
        "prompt": prompt,
        "reference_images": [
            f"build/promo_film_01/{shot}/keyframes/start.png",
            f"build/promo_film_01/{shot}/keyframes/middle.png",
            f"build/promo_film_01/{shot}/keyframes/end.png",
        ],
        "reference_video": f"build/promo_film_01/{shot}/blender_previz.mp4",
        "candidates": [],
    }


def save_manifest(shot: str, manifest: dict) -> None:
    path = manifest_path(shot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_smoke_record() -> None:
    shot = "shot_02_gate_reveal"
    duration, _ = SHOTS[shot]
    manifest = load_manifest(shot, duration, prompt_for(BUILD / shot))
    if not any(item["candidate_index"] == 1 for item in manifest["candidates"]):
        manifest["candidates"].append(
            {
                "candidate_index": 1,
                "task_id": "cgt-20260810132937-mm77b",
                "model": MODEL,
                "resolution": "1080p",
                "aspect_ratio": "16:9",
                "duration_s": 6,
                "fps": 24,
                "generation_timestamp": "2026-08-10T05:29:37Z",
                "api_status": "succeeded",
                "result_path": f"build/promo_film_01/{shot}/generated_candidates/candidate_seedance_01.mp4",
                "error": None,
                "completed_timestamp": "2026-08-10T05:33:21Z",
                "actual": {
                    "resolution": "1080p",
                    "ratio": "16:9",
                    "duration_s": 6,
                    "fps": 24,
                    "seed": 72457,
                },
            }
        )
        save_manifest(shot, manifest)


def submit_missing() -> None:
    ensure_smoke_record()
    for shot, (duration, video_id) in SHOTS.items():
        shot_dir = BUILD / shot
        prompt = prompt_for(shot_dir)
        manifest = load_manifest(shot, duration, prompt)
        present = {item["candidate_index"] for item in manifest["candidates"]}
        video_url = f"{S3_PREFIX}/{video_id}/blender_previz.mp4"
        content = [{"type": "text", "text": prompt}]
        for name in ("start.png", "middle.png", "end.png"):
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": data_url(shot_dir / "keyframes" / name)},
                    "role": "reference_image",
                }
            )
        content.append(
            {"type": "video_url", "video_url": {"url": video_url}, "role": "reference_video"}
        )
        for index in (1, 2):
            if index in present:
                continue
            try:
                result = request(
                    "POST",
                    API,
                    {
                        "model": MODEL,
                        "content": content,
                        "resolution": "1080p",
                        "ratio": "16:9",
                        "duration": duration,
                        "generate_audio": False,
                    },
                )
                record = {
                    "candidate_index": index,
                    "task_id": result["id"],
                    "model": MODEL,
                    "resolution": "1080p",
                    "aspect_ratio": "16:9",
                    "duration_s": duration,
                    "fps": 24,
                    "generation_timestamp": now(),
                    "api_status": "submitted",
                    "result_path": f"build/promo_film_01/{shot}/generated_candidates/candidate_seedance_{index:02d}.mp4",
                    "error": None,
                }
                print(f"SUBMITTED {shot} candidate {index:02d} {result['id']}", flush=True)
            except Exception as exc:  # preserve complete provider error in the manifest
                record = {
                    "candidate_index": index,
                    "task_id": None,
                    "model": MODEL,
                    "resolution": "1080p",
                    "aspect_ratio": "16:9",
                    "duration_s": duration,
                    "fps": 24,
                    "generation_timestamp": now(),
                    "api_status": "submission_failed",
                    "result_path": None,
                    "error": str(exc),
                }
                print(f"FAILED {shot} candidate {index:02d}: {exc}", flush=True)
            manifest["candidates"].append(record)
            save_manifest(shot, manifest)


def poll_and_download(interval: int, timeout: int) -> int:
    deadline = time.time() + timeout
    while True:
        pending = 0
        failed = 0
        for shot, (duration, _) in SHOTS.items():
            manifest = load_manifest(shot, duration, prompt_for(BUILD / shot))
            changed = False
            for item in manifest["candidates"]:
                if not item.get("task_id") or item["api_status"] in {"succeeded", "failed"}:
                    failed += item["api_status"] != "succeeded"
                    continue
                status = request("GET", f"{API}/{item['task_id']}")
                item["api_status"] = status["status"]
                changed = True
                if status["status"] == "succeeded":
                    target = ROOT / item["result_path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    urllib.request.urlretrieve(status["content"]["video_url"], target)
                    item["completed_timestamp"] = now()
                    item["actual"] = {
                        "resolution": status.get("resolution"),
                        "ratio": status.get("ratio"),
                        "duration_s": status.get("duration"),
                        "fps": status.get("framespersecond"),
                        "seed": status.get("seed"),
                    }
                    print(f"DOWNLOADED {item['result_path']}", flush=True)
                elif status["status"] == "failed":
                    item["error"] = json.dumps(status.get("error"), ensure_ascii=False)
                    failed += 1
                    print(f"FAILED {shot} candidate {item['candidate_index']:02d}: {item['error']}", flush=True)
                else:
                    pending += 1
            if changed:
                save_manifest(shot, manifest)
        print(f"STATUS pending={pending} failed={failed}", flush=True)
        if pending == 0:
            return 1 if failed else 0
        if time.time() >= deadline:
            print("Timed out with tasks still pending", file=sys.stderr)
            return 2
        time.sleep(interval)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "poll", "run"))
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=7200)
    args = parser.parse_args()
    if args.action in {"submit", "run"}:
        submit_missing()
    if args.action in {"poll", "run"}:
        return poll_and_download(args.interval, args.timeout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
