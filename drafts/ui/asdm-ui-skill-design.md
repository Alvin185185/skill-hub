# asdm-ui Skill 设计

> 状态：设计中
> 日期：2026-08-31
> 文档角色：固定 UI Skill 的独立设计（实现由独立方负责）
> 调用方：`asdm-devflow`
> 追溯状态：`needs_review`
> 设计版本：`1.1`

## 1. 定位

`asdm-ui` 是独立维护的 UI 效果图生成 Skill。本文件只产出它的设计，不负责其实现；
后续由独立实现方完成基于已确认设计输入的 SVG 效果图生成。它不是一次任务中临时
创建的 Skill，而是具有稳定名称、版本和调用协议的固定能力包。

`asdm-devflow` 负责判断任务是否涉及 UI、调用 `asdm-ui`、传递结构化输入、接收
结果并把结果纳入研发阶段、门禁、状态和证据链；不负责实现 `asdm-ui` 的内部 SVG
生成逻辑。真实页面的实现、测试和 Review 由 `asdm-devflow` 自身的 Worker、
Verifier 和 Reviewer 完成。

## 2. 范围

### 2.1 目标

- 根据 `asdm-devflow` 提供的页面需求、设计约束和现有系统事实生成或修改 UI；
- 为每个页面生成可 diff 的 SVG 效果图；
- 检查 SVG 是否可解析、可渲染，以及是否覆盖输入中声明的页面、字段、状态和视口；
- 输出可被 `asdm-devflow` 消费的 SVG 产物、生成状态、错误和元数据。

### 2.2 非目标

- 不负责需求访谈、总体设计、任务拆解或通用变更编排；
- 不负责页面实现、浏览器测试、可访问性扫描或实现符合性 Review；
- 不负责决定整个研发流程是否放行；
- 不访问外部 URL 获取视觉参考；
- 不要求用户提供参考图；
- 不在运行时创建新的 Skill；
- 不以降低视觉标准的方式绕过失败。

## 3. 固定能力和版本

Skill 标识固定为 `asdm-ui`。调用方必须指定已安装版本，响应中必须返回实际
版本和支持的操作。版本不兼容、Skill 未安装或能力不可用时，由调用方记录为阻塞；
`asdm-ui` 不静默改用未声明的替代流程。

支持的操作：

| 操作 | 用途 |
|---|---|
| `design` | 根据已确认的页面输入生成 SVG 效果图并执行 SVG 自检 |

## 4. 调用输入

调用请求使用结构化 JSON，至少包含：

```json
{
  "skill_id": "asdm-ui",
  "skill_version": "1.x",
  "operation": "design",
  "project_root": "...",
  "work_item_id": "PJ-... or FT-...",
  "page": {
    "page_id": "...",
    "page_type": "new|modified|extended|reused",
    "responsibility": "...",
    "scenarios": ["..."],
    "fields": [],
    "interaction_states": []
  },
  "style_tokens_ref": "...",
  "existing_assets": [],
  "target_viewports": [],
  "constraints": [],
  "upstream_versions": {}
}
```

`asdm-devflow` 必须传入已确认的页面范围、页面需求、设计限制、现有系统事实和上游
版本。`asdm-ui` 不得自行扩大页面范围或补造未提供的业务事实；缺少必要输入时返回
可诊断错误。

## 5. 执行流程

### 5.1 生成或修改

`design` 根据 `asdm-devflow` 传入的页面需求、现有系统事实和设计约束，生成每个
页面的 `mockup-{page}.svg`。生成后执行 SVG 解析和渲染自检。每次操作都记录输入
版本、工具、工具版本、约束版本、时间、产物路径和关联工作项。

### 5.2 SVG 自检

SVG 自检只判断生成产物本身是否有效，包括 XML/SVG 解析、基本渲染、目标视口尺寸
和输入中声明的页面范围、字段、状态覆盖。它不是需求符合性 Review，也不是实现
验收；后两者由 `asdm-devflow` 在后续阶段完成。

## 6. 角色边界

| 角色 | 责任 |
|---|---|
| `asdm-devflow` Coordinator | 判断触发、组装请求、控制阶段门禁、归档结果 |
| `asdm-ui` Worker | 执行 SVG 效果图生成和 SVG 自检 |
| `asdm-devflow` Design Reviewer | 审核 SVG 是否符合已确认需求、设计规则和现有系统约束 |
| `asdm-devflow` Verifier | 独立执行真实页面的浏览器、响应式、交互和可访问性验证 |
| `asdm-devflow` UI Reviewer | 对照 SVG 与浏览器截图复核实施符合性 |

## 7. 失败、修复和阻塞

SVG 生成、解析或渲染失败时，必须记录：

- 错误码和原始错误；
- 根因假设；
- 修复动作；
- 重试输入版本和结果；
- 最终证据或阻塞原因。

`asdm-ui` 只返回生成失败及其诊断信息。重试次数、设计 Review 失败后的重新生成、
实施失败后的 Worker 返工以及最终 `blocked` 均由 `asdm-devflow` 控制。不得自动
降级视觉标准、跳过后续验证或要求用户补充参考图。

## 8. 输出契约

响应至少包含：

```json
{
  "skill_id": "asdm-ui",
  "skill_version": "1.x",
  "operation": "design",
  "status": "completed|failed",
  "artifacts": [],
  "svg_check": {
    "status": "passed|failed",
    "parse": [],
    "render": [],
    "coverage": [],
    "evidence": []
  },
  "errors": [],
  "generation_metadata": {},
  "evidence": [],
  "upstream_versions": {},
  "next_action": "..."
}
```

SVG 产物、生成结果和证据必须可由 `asdm-devflow` 写入当前工作项的权威工作文档。
`asdm-ui` 不创建第二份流程状态源；它只返回 SVG 结果和生成证据。

## 9. 与 asdm-devflow 的交接

调用方向为单向请求/响应：

```text
asdm-devflow
  → 固定 skill_id/version
  → 页面、场景、字段、状态、Token、视口和上游版本
  ← SVG 产物、生成结果、错误、重试记录和证据引用
```

`asdm-devflow` 负责把返回结果映射到 Overall、Detailed、Breakdown、Execute、
Review 和 Sync 的相应产物及门禁。UI 产物发生变化时，`asdm-devflow` 负责设计
Review、真实页面验证、影响分析和返工传播；`asdm-ui` 只负责提供新旧 SVG 产物及其
生成版本关系。

## 10. 验收标准

- 能根据结构化页面输入生成每个受影响页面的 SVG 效果图；
- SVG 通过解析、渲染和输入覆盖自检；
- 输入中声明的页面、字段、状态和视口能够在 SVG 产物中追溯；
- 输入版本、Skill 版本、Token 版本、工具版本和重试历史可追溯；
- `asdm-devflow` 能按固定协议调用并消费 SVG 结果；
- 生成失败能返回可诊断错误，由 `asdm-devflow` 控制重试和最终 `blocked`；
- 不存在临时创建 Skill、要求用户补参考图或自动降级标准的路径。

## 11. 后续实现交付物

- `SKILL.md` 入口和固定 Skill 元数据；
- 输入/输出 schema 与调用协议；
- 效果图生成、自检和交接规范；
- 必要脚本、模板和生成测试；
- 与 `asdm-devflow` 的 SVG 调用集成测试和示例产物。
