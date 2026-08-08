# Xuantianzong Virtual Studio / 玄天宗 AI 虚拟仙门影视制作系统

**Current milestone:** Digital Twin V0.1

**Sole canon:** `玄天宗世界设定总纲 V1.6.1 · 全量合并锁定版`（2026-08-07）。旧稿仅在不与 V1.6.1 冲突时作为历史参考。

## 目标

把玄天宗从“每次重新生成的一组 AI 图片”升级为一个可以反复进入拍摄、空间关系长期稳定的虚拟影视基地。

生产链：

`Canon → Digital Twin → Camera Path → Control Passes → Video Model → QC → Final Film`

## Digital Twin V0.1 范围

V0.1 只锁空间，不追求最终美术：

1. 8 km × 12 km 世界坐标框架；
2. 九座正式主峰的中心、高程与核心跨度；
3. 玄岳关 Proxy；
4. 双阙剑 Proxy；
5. 玄岳关至接天阵台的九段回折中央登宗轴线；
6. 唯一大型悬浮主峰玄天峰与玄天殿占位体；
7. E1 固定母图相机和真实 DJI 镜头预设。

## 核心不可违反规则

- 正式主峰为 **9 座**。
- **只有玄天峰**是大型悬浮主峰。
- 中央登宗轴总体向北但随山势左右偏移，禁止做成从玄岳关直通玄天殿的白色笔直天梯。
- 玄岳关与双阙剑是 A 级前景锚点；玄天峰与玄天殿是终极 S 级视觉中心。
- 双阙剑固定为 V10 双刃直剑，冷白玉质，冰蓝光仅沿双刃和少量阵纹克制流动。
- V12/E1 母图相机是 50mm 三幅虚拟拼接，不得冒充真实 DJI 单镜头。
- 真实 DJI 视频使用 24–35mm 等效焦段与符合物理规律的真实飞行轨迹。
- 三维灰模必须先服从 A1 坐标和高程，再放相机；禁止先凑构图再移动九峰。

## 目录

```text
docs/
  canon/          正典与版本权威
  architecture/   Digital Twin 技术设计
  camera/         E1 / DJI 摄影机规范
  production/     AI 视频生产管线
data/world/       机器可读 Canon 参数
blender/          Blender 自动建场脚本
shots/            Shot 包与 Camera Path
qc/               连续性与验收规则
tools/            辅助工具
```

## 快速开始

1. 安装 Blender 4.x。
2. 打开 `blender/world_builder.py` 并在 Blender Scripting 中运行。
3. 脚本生成九峰 Proxy、玄岳关、双阙剑、九段主轴、玄天峰、玄天殿占位体和相机。
4. 先验收灰模的坐标、距离、尺度、高差和视线，再进入 Seedance / Wan 等 AI 美化层。

> 注意：V0.1 中的山体与建筑只是 Proxy。它们的**位置和控制尺度是 Canon**，外形细节不是最终 Canon 美术。
