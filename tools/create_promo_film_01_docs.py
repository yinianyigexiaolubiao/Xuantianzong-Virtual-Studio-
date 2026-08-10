from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "promo_film_01"


SHOTS = [
    {
        "id": "shot_01_establishing",
        "number": "01",
        "title": "云海发现玄天宗",
        "duration_s": 6,
        "beat": "云海和群峰之间首次发现玄天宗；玄天峰只是远方核心，不提前给特写。",
        "camera": "28mm 等效真实 DJI，大范围缓慢推进并轻微上升，低 yaw、无 FPV 横滚。",
        "visible_zone": "全宗远景体量关系、南部云海、东西连续山系、远方玄天峰。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "build/v0.2/xuantianzong_mini_v0.2_global.png",
            "data/world/peaks.json",
        ],
        "non_drift": "九峰宏观拓扑不漂移；只有玄天峰是大型悬浮主峰；玄天峰当前整体轮廓保持 LOCKED_VISUALLY_VALIDATED。",
    },
    {
        "id": "shot_02_gate_reveal",
        "number": "02",
        "title": "古道发现玄岳关",
        "duration_s": 6,
        "beat": "沿山谷古道推进，利用已验收遮挡关系逐步发现玄岳关和双阙剑。",
        "camera": "继承 V0.2 已通过的 DJI Gate Reveal 时间段；受控前推、轻升、缓慢揭示。",
        "visible_zone": "A7-A8 古道、关前山体、玄岳关、双阙剑。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "build/v0.2/xuantianzong_mini_v0.2_gate_preview.mp4",
            "build/v0.2/qc/qc_01_01_road_to_gate.png",
            "data/world/xuanyue_gate.json",
        ],
        "non_drift": "玄岳关 52×18×34m；双阙剑 44m、68m 轴距、V10 双刃直剑；不重新设计已验收 Gate Reveal。",
    },
    {
        "id": "shot_03_gate_crossing",
        "number": "03",
        "title": "穿越玄岳关",
        "duration_s": 6,
        "beat": "稳定穿过中央门洞，门后道路和地形展开，远方玄天峰形成视觉奖励。",
        "camera": "直接重采样 V0.2 已通过的穿门相机世界变换；真实 DJI、减速穿门、无瞬移。",
        "visible_zone": "玄岳关中央 11×15m 净洞、门后 300–500m 路线、远方玄天峰。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "build/v0.2/xuantianzong_mini_v0.2_gate_preview.mp4",
            "build/v0.2/qc/dji_keyframes/dji_qc_11p5s.png",
            "data/world/preview_camera_paths.json",
        ],
        "non_drift": "必须从中央门洞通过，不穿墙、不撞门楣；门后空间奖励和已验收 Camera 逻辑不得回退。",
    },
    {
        "id": "shot_04_inner_axis",
        "number": "04",
        "title": "宗门内部主轴推进 / 九段玄阶代表段",
        "duration_s": 7,
        "beat": "在 300–500m Hero Zone 中呈现山路、白玉玄阶、平台、礼制山门和转折后的远景展开。",
        "camera": "32mm 等效 DJI，沿地形前推并缓升；速度有惯性，转折温和，避免轨道匀速感。",
        "visible_zone": "A1 第1段内的代表性镜头岛；不建设或伪装完整 7.2km。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "data/world/central_axis.json",
            "docs/architecture/F1_INHERITANCE_AND_V0.2_RULES.md",
        ],
        "non_drift": "九段总计 3600 级、7.2km 且随山势回折；镜头岛为 NON_CANON_PROXY，不移动 A1 控制节点。",
    },
    {
        "id": "shot_05_xuantian_peak",
        "number": "05",
        "title": "玄天峰揭幕",
        "duration_s": 7,
        "beat": "从内部高处逐步揭开玄天峰完整悬浮体量，形成第一视觉高潮。",
        "camera": "32mm 等效 DJI，克制侧向漂移、缓慢上升，最终稳定保持峰体完整可读。",
        "visible_zone": "玄天峰 Hero Zone、周边云层、必要的前景山脊和远处建筑尺度参照。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "build/v0.2/qc/xuantian_peak/xtpeak_qc_05.png",
            "data/world/peaks.json",
        ],
        "non_drift": "当前 V0.2.2 玄天峰悬浮体量、主要轮廓和视觉身份为 LOCKED_VISUALLY_VALIDATED，禁止换形。",
    },
    {
        "id": "shot_06_xuantian_hall",
        "number": "06",
        "title": "玄天殿终极揭幕",
        "duration_s": 7,
        "beat": "靠近峰顶接引层和前庭，缓升揭开玄天殿，最终稳定为整片终极视觉确认。",
        "camera": "35mm 等效 DJI，克制接近与轻微弧线，结束前至少稳定 1 秒。",
        "visible_zone": "B1 玄天殿坐标/包络内的 Hero Zone、前庭、玉阶及必要峰顶边缘。",
        "refs": [
            "build/v0.2/xuantianzong_mini_digital_twin_v0.2.blend",
            "data/world/key_assets.json",
            "data/world/peaks.json",
        ],
        "non_drift": "玄天殿保持 S 级终极视觉中心；锚点 (0,9.31km)、标高 1610m、98×76×45m 包络不移动；建筑美术仍为 NON_CANON_PROXY。",
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seedance_prompt(shot: dict) -> str:
    return f"""Promo Film 01《玄天宗·入宗》镜头 {shot['number']}：{shot['title']}。

画面任务：{shot['beat']}
画面风格：明亮清透的国风仙侠，玉白、淡金、少量朱红层级，宏大、庄严、神圣、真实存在；真实自然光、清晰空气透视，不是黑暗西幻、纪录片、游戏演示或静态概念图轮播。
相机：{shot['camera']}
必须保持：{shot['non_drift']}

参考视频：blender_previz.mp4，严格学习相机路径、节奏、镜头方向和 reveal 时机。
参考图：keyframes/start.png、keyframes/middle.png、keyframes/end.png，保持建筑、峰体、道路和遮挡关系连续。
禁止：空间瞬移、山峰或建筑变形、额外大型浮岛、穿墙、FPV 横滚、鱼眼、无惯性自由摄像机、全局冷蓝霓虹、随机人物/神兽/飞舟。
输出：16:9，24fps，时长 {shot['duration_s']} 秒，连续单镜头。
"""


def wan_prompt(shot: dict) -> str:
    return f"""Wan 2.2 First/Last Frame Video Package — Promo Film 01 Shot {shot['number']}

首帧：keyframes/start.png
尾帧：keyframes/end.png
中间构图锚点：keyframes/middle.png
运动参考：blender_previz.mp4

在 {shot['duration_s']} 秒连续单镜头内，从首帧自然过渡到尾帧。{shot['beat']}
相机运动必须遵循：{shot['camera']}
风格统一为明亮清透国风仙侠，玉白+淡金+少量朱红，真实 DJI 拍摄真实存在的仙门宗派。
锁定不漂移：{shot['non_drift']}
不要增加人物、神兽、飞舟或新建筑；不要改变山体轮廓、门洞、道路方向和相对尺度；不要瞬移、穿墙、横滚或产生橡皮形变。
输出：16:9，24fps，{shot['duration_s']} 秒。
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for shot in SHOTS:
        directory = OUTPUT / shot["id"]
        (directory / "keyframes").mkdir(parents=True, exist_ok=True)
        (directory / "generated_candidates").mkdir(parents=True, exist_ok=True)
        write(
            directory / "shot_brief.md",
            f"""# Shot {shot['number']} — {shot['title']}

## Editorial purpose

{shot['beat']}

## Duration and format

- Target: {shot['duration_s']} seconds
- 16:9 / 24fps / one continuous shot
- Role in 39-second structure: shot {shot['number']} of 6

## Camera

{shot['camera']}

## Shot island / Hero Zone

{shot['visible_zone']}

## Canon and accepted geometry guardrail

{shot['non_drift']}

All newly added set dressing, procedural materials, atmosphere, shot-local stair/platform construction and architectural art detail are `NON_CANON_PROXY`. They may support the shot but cannot redefine Canon.

## Acceptance

- Camera is visibly moving for the full shot and lands gently.
- Start/middle/end frames form one spatially continuous take.
- No forbidden topology, geometry drift, teleport, wall collision or FPV behavior.
- The frame contributes a distinct beat; it is not a static still used as a fake shot.
""",
        )
        write(directory / "seedance_prompt.txt", seedance_prompt(shot))
        write(directory / "wan_flf2v_prompt.txt", wan_prompt(shot))
        write(
            directory / "notes.md",
            f"""# Production notes — Shot {shot['number']}

- Status: BLENDER_PREVIZ_AND_GENERATION_PACKAGE_READY
- Blender source: `build/promo_film_01/promo_film_01_production.blend`
- Previz target: `blender_previz.mp4`
- Keyframe targets: `keyframes/start.png`, `keyframes/middle.png`, `keyframes/end.png`
- Direct candidate target: `generated_candidates/`
- Visible zone: {shot['visible_zone']}
- Proxy boundary: shot-local atmosphere, vegetation, stairs/platform detail and architecture art remain `NON_CANON_PROXY`.
""",
        )
        write(
            directory / "generated_candidates" / "README.md",
            """# Generated candidates

No paid model candidate has been generated yet. The local Seedance 2.0 executor is available, but the service requires an explicit `720p` or `1080p` resolution choice. The current task did not select one, so the failed validation request was not retried with an invented paid specification.

Use the parent folder's `seedance_prompt.txt`, three files under `keyframes/`, and `blender_previz.mp4` after the resolution is explicitly chosen. Wan 2.2 currently has no local executor; use `wan_flf2v_prompt.txt` externally.
""",
        )
        write_json(
            directory / "reference_manifest.json",
            {
                "schema_version": "1.0",
                "film": "Promo Film 01《玄天宗·入宗》",
                "shot_id": shot["id"],
                "title": shot["title"],
                "duration_s": shot["duration_s"],
                "fps": 24,
                "aspect_ratio": "16:9",
                "blender_source": "build/promo_film_01/promo_film_01_production.blend",
                "source_references": shot["refs"],
                "generated_outputs": {
                    "previz": f"build/promo_film_01/{shot['id']}/blender_previz.mp4",
                    "keyframes": [
                        f"build/promo_film_01/{shot['id']}/keyframes/start.png",
                        f"build/promo_film_01/{shot['id']}/keyframes/middle.png",
                        f"build/promo_film_01/{shot['id']}/keyframes/end.png",
                    ],
                    "candidates": f"build/promo_film_01/{shot['id']}/generated_candidates/",
                },
                "canon_non_drift": shot["non_drift"],
                "proxy_policy": "All shot-local art additions are NON_CANON_PROXY and cannot update Canon.",
            },
        )

    write(
        OUTPUT / "README.md",
        """# Promo Film 01《玄天宗·入宗》

Production mode: `SHOT-FIRST VIRTUAL PRODUCTION`.

This fast-line project builds six bounded Shot Islands/Hero Zones from the accepted V0.2 spatial proof. It does not wait for a full Digital Twin art pass and does not modify the accepted V0.2 source scene.

Shot order: establishing → gate reveal → gate crossing → inner axis → Xuantian Peak → Xuantian Hall.

Locked guardrails: V0.2 gate/sword/terrain relationship, accepted gate-camera logic, and the `LOCKED_VISUALLY_VALIDATED` Xuantian Peak massing/silhouette.
""",
    )
    print(f"[promo docs] wrote {len(SHOTS)} shot packages under {OUTPUT}")


if __name__ == "__main__":
    main()
