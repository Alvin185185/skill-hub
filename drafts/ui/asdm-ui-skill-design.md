# asdm-ui Skill 设计

> 状态：设计中
> 日期：2026-08-31
> 文档角色：固定 UI Skill 的独立设计（实现由独立方负责）
> 调用方：`asdm-devflow`
> 追溯状态：`needs_review`
> 设计版本：`1.0`

## 1. 定位

`asdm-ui` 是独立维护的 UI 专项 Skill。本文件只产出它的设计，不负责其实现；
后续由独立实现方完成页面风格分析、UI 设计产物生成、页面实现或修改，以及 UI
专项验证。它不是一次任务中临时创建的 Skill，而是具有稳定名称、版本和调用协议
的固定能力包。

`asdm-devflow` 负责判断任务是否涉及 UI、调用 `asdm-ui`、传递结构化输入、接收
结果并把结果纳入研发阶段、门禁、状态和证据链；不负责实现 `asdm-ui` 的内部 UI
处理逻辑。

## 2. 范围

### 2.1 目标

- 从现有项目识别路由、页面、组件和样式来源；
- 汇总可复用的设计 Token 和页面约束；
- 按页面场景生成或修改 UI，并生成可 diff 的 SVG 效果图；
- 对实现页面执行渲染、响应式、交互、溢出、重叠和可访问性验证；
- 输出可被 `asdm-devflow` 消费的产物、状态、错误和证据。

### 2.2 非目标

- 不负责需求访谈、总体设计、任务拆解或通用变更编排；
- 不负责决定整个研发流程是否放行；
- 不访问外部 URL 获取视觉参考；
- 不要求用户提供参考图；
- 不在运行时创建新的 Skill；
- 不以降低视觉标准的方式绕过失败。

## 3. 固定能力和版本

Skill 标识固定为 `asdm-ui`。调用方必须指定已安装版本，响应中必须返回实际
版本和支持的操作。版本不兼容、Skill 未安装或能力不可用时，调用应失败并返回
`blocked` 所需的信息，不得静默改用未声明的替代流程。

支持的操作：

| 操作 | 用途 |
|---|---|
| `inspect` | 扫描项目并生成风格与页面资产摘要 |
| `design` | 根据页面输入生成 SVG 效果图和 UI 设计产物 |
| `implement` | 根据已确认的效果图和约束实现或修改页面 |
| `verify` | 对已实现页面执行 UI 专项验证 |
| `repair` | 根据失败记录执行诊断、修复和复检 |

## 4. 调用输入

调用请求使用结构化 JSON，至少包含：

```json
{
  "skill_id": "asdm-ui",
  "skill_version": "1.x",
  "operation": "design|implement|verify|repair",
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

`asdm-devflow` 必须传入已确认的页面范围和上游版本。`asdm-ui` 不得自行扩大
页面范围或补造未提供的业务事实；缺少必要输入时返回可诊断错误。

## 5. 执行流程

### 5.1 风格和页面识别

`inspect` 静态扫描项目，不访问 URL，识别：

- React Router、Vue Router、Next.js App/Pages Router、Angular 路由；
- 页面组件、组件 import 链和可复用资产；
- CSS 变量、主题文件、Tailwind class、styled-components、CSS Module；
- 组件库主题覆盖和 inline style。

扫描结果写入 `style-tokens.json` 和页面资产索引，并保留扫描范围、命中来源、
未识别项和扫描版本。

### 5.2 生成或修改

`design` 根据页面输入和 Token 约束生成每页面的
`mockup-{page}.svg`。`implement` 根据已确认效果图实现或修改页面。每次操作
都记录输入版本、工具、工具版本、Token 版本、时间、产物路径和关联工作项。

### 5.3 UI 专项验证

`verify` 使用真实浏览器执行：

- 页面渲染和截图；
- 桌面与移动视口响应式检查；
- 关键交互路径；
- 溢出、遮挡和元素重叠检查；
- axe-core 或 pa11y 可访问性扫描；
- 效果图与浏览器截图的视觉对照。

机械检测至少覆盖风格一致性、多页面一致性和字段准确性。检测工具可以是
Playwright、axe-core、pa11y 或项目内等价工具，但使用的工具和版本必须记录。

## 6. 角色边界

| 角色 | 责任 |
|---|---|
| `asdm-devflow` Coordinator | 判断触发、组装请求、控制阶段门禁、归档结果 |
| UI Worker | 执行 `asdm-ui` 的 `inspect/design/implement/repair` 操作 |
| Verifier | 独立执行浏览器、响应式、交互和可访问性验证 |
| UI Reviewer | 独立复核效果图与浏览器截图的视觉符合性 |

执行 UI 的 Worker 不得直接把自己的自检结果当作最终通过依据。Verifier 和
UI Reviewer 必须返回独立结论及证据位置。

## 7. 失败、修复和阻塞

生成、扫描、检测或渲染失败时，必须记录：

- 错误码和原始错误；
- 根因假设；
- 修复动作；
- 重试输入版本和结果；
- 最终证据或阻塞原因。

自动流程最多执行三轮“诊断 → 修复 → 重生成/复检”。三轮后仍失败，或固定
Skill 不可用、页面无法定位、必要主题无法识别时，返回 `blocked`。不得自动
降级视觉标准、跳过验证或要求用户补充参考图。

## 8. 输出契约

响应至少包含：

```json
{
  "skill_id": "asdm-ui",
  "skill_version": "1.x",
  "operation": "design",
  "status": "completed|failed|blocked",
  "artifacts": [],
  "verification": [],
  "errors": [],
  "retry_history": [],
  "evidence": [],
  "upstream_versions": {},
  "next_action": "..."
}
```

产物、验证结果和证据必须可由 `asdm-devflow` 写入当前工作项的权威工作文档。
`asdm-ui` 不创建第二份流程状态源；它只返回领域结果和证据引用。

## 9. 与 asdm-devflow 的交接

调用方向为单向请求/响应：

```text
asdm-devflow
  → 固定 skill_id/version
  → 页面、场景、字段、状态、Token、视口和上游版本
  ← UI 产物、验证结论、错误、重试记录和证据引用
```

`asdm-devflow` 负责把返回结果映射到 Overall、Detailed、Breakdown、Execute、
Review 和 Sync 的相应产物及门禁。UI 产物发生变化时，`asdm-devflow` 负责影响
分析和返工传播；`asdm-ui` 负责提供新旧产物及其版本关系。

## 10. 验收标准

- 能在至少一种支持的前端框架中完成 `inspect → design → implement → verify`；
- 每个受影响页面都有 SVG 效果图、实现结果和浏览器验证证据；
- 输入版本、Skill 版本、Token 版本、工具版本和重试历史可追溯；
- UI Worker、Verifier、UI Reviewer 的结论彼此独立；
- 失败经过诊断和修复，三轮后仍失败能稳定返回 `blocked`；
- `asdm-devflow` 能按固定协议调用并消费结果；
- 不存在临时创建 Skill、要求用户补参考图或自动降级标准的路径。

## 11. 后续实现交付物

- `SKILL.md` 入口和固定 Skill 元数据；
- 输入/输出 schema 与调用协议；
- 风格扫描、效果图、验证和修复规范；
- 必要脚本、模板、Token 资产和测试；
- 与 `asdm-devflow` 的集成测试和示例证据。
