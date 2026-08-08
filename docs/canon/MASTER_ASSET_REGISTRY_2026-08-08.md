# 玄天宗 Master Asset Registry — 2026-08-08

## 目的

这是玄天宗当前工程的**总资产登记入口**。它不取代各源文件，而是记录：什么仍然有效、什么只是技术控制、什么被后续锁定覆盖、什么二进制本体已找到、什么只有 manifest/文档引用、什么已经废弃。

资产若没有进入本注册体系，不得因为“聊天里提过”“某张图画过”而自动成为正式工程资产。

## 状态定义

- `BASE_CANON`：基础世界母本。
- `POST_CANON_LOCKED_OVERRIDE`：晚于基础母本、用户明确锁定、仅覆盖指定字段的正式增量修订。
- `TECH_CONTROL`：坐标、比例、功能、相机、灰模等工程控制。
- `ASSET_CONTROL`：专项正式资产规则。
- `DERIVED_BINARY`：由控制文件产生的 OBJ/GLB/PNG 等。
- `VISUAL_REFERENCE`：只供气质/构图参考，不能覆盖精确参数。
- `HISTORICAL`：版本演化证据。
- `DEPRECATED`：明确禁止回流。

二进制可用性：

- `DIRECT_FOUND`：File Library 中检索到文件本体。
- `MANIFEST_VERIFIED`：正式 manifest 记录文件名、大小与 SHA256，但本次 File Library 未直接返回二进制条目。
- `REFERENCED_ONLY`：技术文档提及，尚无 manifest 或直接文件结果。

---

# A. 基础世界母本

## A-001｜V1.6.1 全量合并锁定版

分类：`BASE_CANON`

已直接找到：
- `玄天宗世界设定总纲_V1.6.1_全量合并锁定版.docx`
- `玄天宗世界设定总纲_V1.6.1_全量合并锁定版.pdf`
- `玄天宗世界设定总纲_V1.6.1_全量合并锁定版.txt`
- `玄天宗世界设定总纲_V1.6.1_全量合并锁定版_设计参数.json`

状态：当前世界基础母本，直接整合 V1.6 + A1 + B1 + C1。

重要补充：2026-08-07 后续确有新的专项资产被用户明确 LOCKED。此类变更按 `POST_CANON_LOCKED_OVERRIDES.md` 执行，仅覆盖明确字段；不能把 V1.6.1 整体降级。

---

# B. 世界技术控制

## B-001｜A1 总平面与高程控制

分类：`TECH_CONTROL`

直接找到：
- `玄天宗_V1.6-A_总平面与高程控制书_A1正式版.pdf`
- D1 历史初设 DOCX/PDF
- A1/D1 锁定参数已经合并进 V1.6.1 设计参数 JSON

控制：8×12km坐标、九峰、古道、九段玄阶、玄天峰、后山、水系、小浮岩、三神木、玄岳关、双阙剑。

## B-002｜B1 九峰功能与关键资产布局

分类：`TECH_CONTROL`

直接找到：
- `玄天宗_V1.6-B_九峰功能与关键资产布局_B1正式版.docx`
- `玄天宗_V1.6-B_九峰功能与关键资产布局_B1正式版.pdf`
- B1 总确认稿 DOCX/PDF
- B1 设计参数 JSON（File Library 已检索到）

控制：九峰功能、人口、建筑覆盖、中央资产、交通、空域。

## B-003｜C1 视觉与高阶神兽出镜控制

分类：`TECH_CONTROL / VISUAL_CONTROL`

直接找到过：C1 正式 DOCX/PDF 与设计参数 JSON。

控制：S/A/B/C视觉等级、材质、光色、神兽出镜、静态/无人机/手机影像验收。

## B-004｜E1 V12固定相机与视线控制

分类：`TECH_CONTROL / CAMERA_CONTROL`

直接找到过：E1 DOCX/PDF。

控制：约 `(0,3.33km,695m)`、50mm、-24/0/+24°三幅虚拟拼接、总水平视场约68°；用于战略母图和遮挡检查，**不是真实 DJI 航线**。

## B-005｜F1 三维灰模与比例控制

分类：`TECH_CONTROL / GRAYBOX_CONTROL`

直接找到：
- `玄天宗_V1.6-F_三维灰模与比例控制书_F1总确认稿.docx`
- `玄天宗_V1.6-F_三维灰模与比例控制书_F1总确认稿.pdf`
- `玄天宗_V1.6-F_F1_三维灰模场景.obj` — `DIRECT_FOUND`

文档还明确提供 GLB 版本，但本次精确 File Library 检索未返回 GLB 本体：`REFERENCED_ONLY`。

控制：100m连续地形网格、东西两条连续山系、中央谷地、北部遮挡山脊、1450×1050m/400–470m厚重倒悬玄天峰、B1包络块体、E1套合。

---

# C. 后置六兽正式资产系统

## C-001｜神兽创作强制门禁 V2.0

分类：`ASSET_CONTROL / POST_CANON_LOCKED_OVERRIDE_SUPPORT`

直接找到：
- `玄天宗_神兽创作流程_当前生效标准.json`
- `玄天宗_神兽创作流程_当前生效标准.txt`
- `README_强制执行.txt`

状态：`LOCKED`

锁定包：`玄天宗_神兽创作强制门禁_V2.0.zip`
SHA256：`7b780a9b7bf948fef21b0e5c977e84593e46e1e7bebdc2a0be073fb3004d5866`

ZIP 和独立 `CANONICAL_BEASTS.json` 当前在 File Library 搜索中未作为独立条目返回；但其唯一真源地位被当前生效标准、正式资产注册表和 F2 三重引用。状态记为 `REFERENCED_BY_MULTIPLE_LOCKED_SOURCES`，不能退回旧尺寸。

## C-002｜六兽神话学约束层 V1.0

分类：`ASSET_CONTROL`

直接找到：`六兽神话学约束层_V1.0_锁定版.json`

状态：锁定。

关键：玄雷夔一足无角；毕方一足；夫诸四独立角根；九天玄应龙为玄天宗衍生无翅东方祖龙；玄武龟蛇双灵且蛇不得龙化。

## C-003｜比例数据正式锁定源

分类：`ASSET_CONTROL / PARTIALLY_SUPERSEDED`

直接找到：`比例数据_正式锁定源.json`

其中当前有效的大尺度六兽数字与正式资产注册表一致；但玄雷夔“主雷角55m/显圣130m”已被后续 `deprecated_fields` 废止。此文件必须经过后续废除字段过滤后使用，禁止整文件盲读。

## C-004｜六兽正式资产注册表 V1.0

分类：`POST_CANON_LOCKED_OVERRIDE / ASSET_CONTROL`

直接找到：`六兽正式资产注册表_V1.0_LOCKED.json`

状态：`LOCKED`
批准说明：用户总审通过。

这是六兽当前正式尺寸、硬视觉约束、禁用项和 approved-art SHA256 的权威注册表之一。

## C-005｜REFERENCE_HASHES

分类：`ASSET_CONTROL / HASH_REFERENCE`

直接找到：`REFERENCE_HASHES.json`

记录白泽及六兽 V0.9 资产卡等参考文件 SHA256；其中 V0.9 卡本身标 `REFERENCE_ONLY_NOT_V1_LOCKED`，后续由 V1.0 LOCKED 注册表选择 approved art。

---

# D. F2 / F3 / G1 神兽与正式母图链

## D-001｜F2 六兽真实尺度植入

分类：`POST_CANON_LOCKED_OVERRIDE / TECH_CONTROL`

直接找到：
- `F2_六兽真实尺度植入_设计参数与验收.json`
- `F2_LOCK_RELEASE_NOTE.txt`
- `MANIFEST_SHA256.json`

状态：`LOCKED`，用户明确确认锁定。

F2 manifest 已验证下列派生文件及 SHA256/大小：
- `01_F2_六兽常态世界空间试放总平面.png`
- `02_F2_常态量级复验.png`
- `F2_LOCK_RELEASE_NOTE.txt`
- `F2_六兽真实尺度植入_设计参数与验收.json`
- `F2_白泽_常态真实尺度试放.glb`
- `F2_玄雷夔_常态真实尺度试放.glb`
- `F2_毕方_常态真实尺度试放.glb`
- `F2_夫诸_常态真实尺度试放.glb`
- `F2_九天玄应龙_常态真实尺度试放.glb`
- `F2_太玄玄武_常态真实尺度试放.glb`
- `玄天宗_V1.6-F2_六兽常态真实尺度_技术总场景.glb`
- manifest 自身

上述 GLB/PNG 当前未作为独立 File Library 条目返回，登记为 `MANIFEST_VERIFIED`，不是“文件不存在”。

## D-002｜F3 六兽形态深化与 V12 套合

分类：`TECH_CONTROL / ASSET_CONTROL`

直接找到：`F3_形态深化与V12套合_设计参数.json`

源文件状态：`REVIEW`
下游状态：`PASSED_BY_G1`

引用输出：
- `玄天宗_V1.6-F3_六兽LOD1.5_与F1总场景.glb`
- 六个个体 LOD1.5 GLB
- `01_F3_V12六兽套合投影.png`
- `02_F3_V12可见性矩阵.png`

这些派生二进制本次未直接检索到独立条目，且未发现独立 F3 SHA256 manifest，因此登记为 `REFERENCED_ONLY`。不得把 F3 源文件自身状态伪写成 LOCKED；但 G1 已明确继承其“通过”结论。

## D-003｜G1 正式母图生成控制

分类：`TECH_CONTROL / FUTURE_HERO_IMAGE_CONTROL`

直接找到：`玄天宗_V1.6-G1_正式母图生成控制稿_已锁定记录.json`

状态：`LOCKED`

基础：E1 + F2 LOCKED + F3 PASSED + V1.6视觉规则。

---

# E. Visual References

分类：`VISUAL_REFERENCE`

已发现代表性文件：
- `玄天宗世界设定总纲_V1.5_V12视觉母图整合正式版.docx/pdf`
- `玄天宗_全宗宏大战略总图_正式母图_V5.png`
- `玄天宗_全宗宏大战略总图_正式标注版_V6.png`
- `玄天宗_全宗宏大战略总图_正式母图_V6.jpeg`
- `玄天宗_全宗宏大战略总图_远景与双剑精修版_V11.png`

用途：光色、层级、构图语言、历史视觉方向。

禁止：从图像反推精确坐标；覆盖 A1/B1/V1.6.1；把 AI 糊块或临时地标提升成 Canon。

---

# F. Historical World-Bible Chain

分类：`HISTORICAL`

已发现：
- V1.0 DOCX
- V1.1 DOCX
- V1.2 DOCX
- V1.3 建筑视觉定稿版及延续版本
- V1.4 最新总图整合定稿版
- V1.5 V12视觉母图整合正式版 DOCX/PDF
- V1.6 全量校核锁定版 DOCX/PDF/TXT
- V1.6-A D1 初步设计稿 DOCX/PDF
- `数字玄天宗_项目状态档案_2026-08-04.md`

用途：追溯来源与设计演化。不得覆盖当前有效母本/后置锁定模块。

---

# G. Deprecated Rules

分类：`DEPRECATED`

明确禁止回流：
- 五峰版本。
- 九座规则孤立圆锥。
- 九座大型浮岛/规则圆环。
- 玄岳关直通玄天殿的白色笔直天梯。
- 玄天峰薄圆盘/UFO/平台。
- 西方黑城堡、灰暗魔山、全宗冷蓝霓虹。
- 所有自然/生产材料一律白玉化。
- E1三幅拼接伪装真实 DJI 单镜头。
- 玄雷夔任何“主雷角/雷角”字段。
- 九天玄应龙任何翅膀字段。

---

# H. 当前二进制可恢复性结论

### 已直接找到本体

- F1 OBJ。
- V1.6.1 DOCX/PDF/TXT/设计参数 JSON。
- A1/B1/C1/E1/F1 等主要控制文档（至少其正式文档/参数文件已检索到）。
- F2/F3/G1 控制文件。

### 有正式 SHA256 manifest，但本体本次未直接返回

- F2 六个个体 GLB。
- F2 总场景 GLB。
- F2 两张审查 PNG。

这类资产是“manifest 可验证、File Library 当前未直接索引”，不得误报为丢失。

### 仅有技术文档引用，尚无独立本体/manifest结果

- F1 GLB。
- F3 Master/个体 GLB 与两张套合图。
- 神兽门禁 V2.0 ZIP 与独立 CANONICAL_BEASTS.json。

这些属于**可追踪缺口**，不影响 V0.2 玄岳关 Mini Spatial Proof；未来使用对应资产前应从原工作空间/归档重新恢复并校验。

---

# I. 当前 Authority Resolution

执行顺序不是简单“最新文件赢”，而是：

```text
BASE_WORLD_CANON: V1.6.1
        ↓
SCOPED POST-CANON LOCKED OVERRIDES
        ↓
TECH/ASSET CONTROL that agrees with above
        ↓
Derived binary / visual reference
        ↓
Historical / deprecated
```

当前唯一确认的 post-canon override 域：`OVR-BEAST-001`。

详见：
- `docs/canon/POST_CANON_LOCKED_OVERRIDES.md`
- `data/canon/post_canon_overrides.json`

---

# J. 维护门禁

从现在开始：

1. 新正式资产必须登记到本注册表及机器 JSON。
2. 如果只是新增资产，不与母本冲突：登记即可，不创建 override。
3. 如果覆盖现有锁定字段：必须有明确用户批准，并登记 post-canon override。
4. DRAFT/REVIEW/概念图不具备自动覆盖权。
5. 派生二进制应优先建立 SHA256 manifest。
6. 大型 GLB/BLEND/视频推荐 Git LFS/对象存储；普通 Git 保存参数、manifest、索引和可重建代码。
7. 每次 Digital Twin milestone 前必须先读取 Master Registry + Override Registry。
