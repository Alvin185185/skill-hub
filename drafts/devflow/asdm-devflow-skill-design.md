# asdm-devflow Skill 需求与决策基线

> 状态：已完成（需求与决策基线），待详细设计与实现
> 日期：2026-08-25
> 文档角色：需求与决策基线（DEVFLOW-REQ）
> 概要设计：[asdm-devflow-skill-overall-design.md](asdm-devflow-skill-overall-design.md)
> 追溯状态：`in_sync`
> 需求版本：`1.3`
> 最近同步变更：`CR-003`

---

## 1. 背景与目标

### 1.1 来源

基于既有阶段化研发流程的机制分析，吸收结构化访谈、阶段门禁、调研续作和任务验证等有效能力，构建一套**完全独立演进**的项目与特性研发全流程 Skill。本 Skill 重新定义自己的状态、协议和文档，不与任何既有流程系统做运行时衔接、取代或迁移。

### 1.2 当前流程能力与未解决的问题

当前流程已经覆盖「流程串联」：阶段门禁、文档落盘和跨会话续作，但存在 8 个质量与执行闭环缺口：

| 编号 | 缺口 | 现有覆盖情况 |
|------|------|-------------|
| `GAP-001` | 拆解后缺少 AI 执行 + 按要求检测的环节 | 进度检查只做事后 DoD 对照，无人消费 Plan 的验证步骤 |
| `GAP-002` | 修改一个文档，前置/后续文档无同步机制 | 完全没有，所有命令单向「向前生成」 |
| `GAP-003` | 生成文档无质量验收（人工审核耗时大） | review 只有结构性检查（章节/链接/格式），无内容质量检查 |
| `GAP-004` | 前置/后续/当前文档的上下文一致性无检测 | Review 只做局部一致性检查，不查文档链上下游 |
| `GAP-005` | 文档无多角色审核 | 完全没有，review 是单一审查员视角 |
| `GAP-006` | 文档「看着靠谱其实不靠谱」（幻觉） | 只有事后抽查，无生成时的 grounding 强制 |
| `GAP-007` | 页面无设计、审核与一致性机制 | 完全没有，无 UI 设计文档、无效果图生成、无视觉一致性检测 |
| `GAP-008` | 只能在已有项目中规划特性，无法从想法创建完整项目 | 默认已有仓库、代码、构建和运行环境，没有 Project 生命周期和 MVP 交付门禁 |

### 1.3 目标

构建「**机器状态驱动、文档承载事实**」的项目与特性研发流水线，覆盖需求→设计→拆解→执行→评审→变更维护全闭环，以证据链与追溯矩阵两条质量主线根治上述 8 个缺口（含完整项目创建和页面设计/审核机制）。机器可读状态负责工作对象、阶段、依赖和过期判定；Markdown 文档负责让人理解和审核需求、设计与证据。

七个命令保持不变，同一条链同时处理 `Project` 和 `Feature`。AskMe 首次确定 `subject_type=project|feature` 并持久化；后续命令读取状态选择对应分支，不重新猜测。Project 模式从项目想法建立可运行工程基线，并编排 MVP Feature，直到项目达到 `mvp_ready`；Feature 模式在已建立的 Project 基线上交付单项能力。UI 机制仍采用「**融合进现有步骤**」原则，不单独新增命令或文档阶段。

### 1.4 核心需求登记

| 编号 | 需求 | 来源缺口 | 概要设计落点 |
|------|------|----------|----------------|
| `REQ-001` | 七个命令必须处理统一工作对象，并以 `subject_type`、`subject_id` 和 `project_id` 持久化身份 | `GAP-008` | `DES-001`、`FLOW-001`、`CONTRACT-001` |
| `REQ-002` | Project 和 Feature 必须共用 AskMe→Overall→Detailed→Breakdown→Execute→Review→Sync 全流程 | `GAP-001`、`GAP-008` | `DES-002`、`MOD-002`、`FLOW-002` |
| `REQ-003` | 阶段、依赖、任务、版本、过期和恢复必须由机器可读状态驱动 | `GAP-002`、`GAP-004` | `STATE-001`、`FLOW-003`、`CONTRACT-002` |
| `REQ-004` | 当前有效基线与待审批变更必须分离，变更确认后才传播到下游 | `GAP-002`、`GAP-004` | `STATE-002`、`FLOW-004` |
| `REQ-005` | 需求、设计、任务、实现和验证必须形成可回源证据链 | `GAP-003`、`GAP-006` | `MOD-004`、`NFR-001` |
| `REQ-006` | 实施者与验收者必须职责隔离，standard/full 使用独立 Verifier | `GAP-001`、`GAP-005` | `MOD-005`、`FLOW-005` |
| `REQ-007` | UI 决策、效果图、实现和浏览器验证必须融入现有阶段 | `GAP-007` | `MOD-006`、`FLOW-006` |
| `REQ-008` | Project 必须先达到 `foundation_ready`，再编排 MVP Feature，最终达到 `mvp_ready` | `GAP-008` | `STATE-003`、`FLOW-007` |
| `REQ-009` | 工作流深度必须按 `light/standard/full` 风险档位执行，高风险只能升级 | `GAP-003`、`GAP-006` | `NFR-002`、`FLOW-008` |
| `REQ-010` | Review 和 Sync 必须执行跨制品收敛检查并处置缺失、冲突、过期和计划外实现 | `GAP-003`、`GAP-004` | `MOD-007`、`NFR-003` |

以上条目是需求层事实。概要设计可以增加技术补充，但不得改变这些需求语义；需要改变时必须先通过 Sync 更新本文件。

---

## 2. 纳入 Skill 的能力

| # | 能力 | Skill 中的设计 |
|---|------|----------------|
| 1 | 前置条件门禁 | 所有命令统一检查状态、产物、依赖和 stale 标记 |
| 2 | 决策点结构化访谈 | 问题、背景、选项、推荐、确认、理由和验收标准绑定 |
| 3 | 两阶段调研与会话续作 | 调研先落盘冻结，再进入设计；中断后从状态恢复 |
| 4 | 固定骨架与扩展区 | 模板提供稳定结构，复杂项目允许增加受控章节 |
| 5 | 纵向切片与验证步骤 | 每个任务覆盖端到端能力，并包含可执行判定协议 |
| 6 | 反假设原则 | 语义定位文档和代码事实，不预设输入文档结构 |
| 7 | 结构化输出 | 所有命令返回统一 JSON 和明确的 `next_steps` |
| 8 | 行为、规范、模板三层解耦 | `SKILL.md`、references 和 assets 分离维护 |
| 9 | 人类索引与追溯锚点 | INDEX、文档锚点和 `state.json` 分别承担可读与机器状态 |
| 10 | Markdown 质量检查 | 统一执行 markdownlint 和文档格式规则 |

### 2.1 同类项目可吸收的设计

| 项目 | 可吸收优点 | 本方案落点 |
|------|-----------|-----------|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | 在实现前后做跨制品一致性与收敛检查 | 新增 §5.8 收敛检查，自动生成缺口任务 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 将当前有效规范与待审批变更分开，审批后再归档合并 | 每个特性增加 `changes/`，sync 先产出 proposal/impact，确认后再修改基线 |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | 按工作复杂度选择不同深度的规划路径 | 新增 §3.5 轻量/标准/完整三档工作流 |
| 结构化状态工作流方法 | 用结构化状态支撑阶段恢复、任务依赖与自动化 | 新增 `state.json`，作为阶段与依赖状态的权威来源 |
| [OpenSSF Scorecard](https://scorecard.dev/) | 按风险和策略执行可度量检查，而非所有项目固定同一阈值 | E1 与验证步骤改为风险分级覆盖率 |

---

## 3. 通用化架构

**skill 本体通用，项目配置外置**。skill 不硬编码任何项目特定内容（工作项系统、模块清单、路径）；每个使用项目在仓库根放 `.devflow/config.md`，skill 启动时读取，未找到则用内置默认值。

工作对象采用两级模型：

```text
Project (PJ-xxx)
  └── Feature* (FT-xxx)
```

七个命令处理统一的 `subject`，其身份由 `subject_type` 和 `subject_id` 确定。`Project` 是一级对象，负责产品目标、工程基线和 MVP；`Feature` 是 Project 的子对象，负责一项可独立验收的业务能力。`subject_type` 在 AskMe 初始化时确定并写入状态，AskMe 完成后不得由后续命令重新推断或静默修改。

### 3.1 config.md 配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `project_id_mode` | Project 编号生成方式；当前工作区默认一个主 Project | `auto`（PJ-001…） |
| `feature_id_mode` | `auto`（顺序自增 FT-001…）或 `work_item`（外部工作项编号映射 FT-{id}） | `auto` |
| `tracker_url_template` | 外部追踪链接模板；配置后文档头部带追踪链接并强制收集 ID，未配置则跳过 | 不配置 |
| `docs_root` | devflow 文档根目录 | `docs/devflow/` |
| `index_file` | 人类可读 Project/Feature 索引（skill 根据状态自动维护） | `{docs_root}/INDEX.md` |
| `modules` | 模块清单（名称→编号映射，用于特性归属） | 不分模块 |
| `repos` | 代码库清单（detailed 调研阶段扫描范围提示） | 自动扫描子目录/子模块 |
| `build_commands` | 目录→构建命令映射（execute 的构建检查） | 询问用户 |
| `runtime` | 进程目录、启动/停止/重建命令、端口、健康检查、日志文件、浏览器入口；供 execute/review 复现运行环境 | 未配置则按任务询问 |
| `code_index` | 内置代码关系索引的存储位置、扫描范围、刷新策略；不依赖外部 Ontology 服务 | `{repo_root}/.devflow/code-index/` |
| `workflow_profile` | `auto` / `light` / `standard` / `full`；控制文档深度、评审角色和核查覆盖率 | `auto` |

### 3.2 工作对象路由与身份

AskMe 按以下优先级确定工作对象：显式 `PJ-xxx/FT-xxx` → 已绑定的当前对象 → 唯一进行中的对象 → 仓库与用户意图判断 → 用户确认。空目录、空仓库或用户明确提出完整产品时默认候选 Project；已存在 `ready` Project 且用户提出局部能力时默认候选 Feature。存在多个合理对象时必须询问，不能猜测。

AskMe 初始化后将身份写入权威状态：

```json
{
  "subject_type": "project",
  "subject_id": "PJ-001",
  "project_id": "PJ-001",
  "phase": "clarifying"
}
```

Feature 状态必须额外包含 `feature_id` 和父 `project_id`。每个命令输出都携带 `subject_type`、`subject_id` 和 `project_id`；下一命令通过 `subject_id` 定位状态并读取分支，不从 Markdown 正文重新判断。

工作对象类型在 AskMe 完成前可以经用户确认纠正；AskMe 完成后改变类型必须废弃原对象并创建正确对象，或通过 sync 留下可审计记录，不得原地静默翻转。

### 3.3 Skill 目录结构

```text
.codebuddy/skills/asdm-devflow/
├── SKILL.md                     ← 调度器：命令路由 / 阶段判定表 / 共享机制
├── references/
│   ├── config-schema.md         ← 项目配置 schema 与默认值
│   ├── command-askme.md         ← 需求访谈
│   ├── command-overall.md       ← 概要设计
│   ├── command-detailed.md      ← 代码调研 + 详细设计（两阶段）
│   ├── command-breakdown.md     ← 实施拆解
│   ├── command-execute.md       ← 任务执行与验证
│   ├── command-review.md        ← 双模式多角色评审
│   ├── command-sync.md          ← 变更传播
│   ├── code-intelligence.md     ← 内置代码关系索引、查询与影响分析
│   ├── agent-orchestration.md   ← Coordinator/Worker/Verifier 编排协议
│   ├── runtime-verification.md  ← 可复现运行、日志调试与运行时验证
│   ├── evidence-rules.md        ← 证据链规范
│   ├── traceability.md          ← 追溯矩阵规范
│   ├── review-roles.md          ← 多角色评审规范
│   ├── workflow-profiles.md     ← 风险分级与三档工作流
│   ├── state-schema.md          ← state.json schema、状态迁移与过期规则
│   ├── convergence.md           ← 跨制品收敛检查规范
│   └── ui-generation.md         ← UI 效果图生成能力（新增）
└── assets/
    ├── askme-template.md        ← 需求访谈文档模板
    ├── overall-template.md      ← 概要设计文档模板
    ├── detailed-template.md     ← 详细设计文档模板
    ├── plan-template.md         ← 实施计划文档模板
    └── style-tokens-template.json ← 风格 token 模板（新增）
```

### 3.4 Project 与 Feature 文档链

```text
.devflow/
├── config.md
├── work-items.json                    ← subject_id 到状态文件的定位索引
├── project-state.json                 ← Project 机器状态
├── features/FT-{id}/state.json        ← Feature 机器状态
└── code-index/                        ← 按仓库/commit 版本化的代码关系索引

{docs_root}/
├── INDEX.md                           ← Project 与 Feature 人类可读索引
├── project/
│   ├── PJ-{id}-AskMe.md
│   ├── PJ-{id}-Overall.md
│   ├── PJ-{id}-CodeResearch-{repo}.md
│   ├── PJ-{id}-Detailed.md
│   ├── PJ-{id}-Plan.md
│   ├── PJ-{id}-Review-{mode}-{date}.md
│   └── changes/
└── features/FT-{id}-{name}/
    ├── FT-{id}-{name}-AskMe.md
    ├── FT-{id}-{name}-Feature-Overall.md
    ├── FT-{id}-{name}-CodeResearch-{repo}.md
    ├── FT-{id}-{name}-Feature-Detailed.md
    ├── FT-{id}-{name}-Plan.md
    ├── FT-{id}-{name}-Review-{mode}-{date}.md
    └── changes/
```

**事实与状态边界**：已批准的 AskMe/Overall/Detailed/Plan 是当前有效内容基线；`changes/` 中的 proposal 只是待审批建议，未确认前不得被下游当成有效事实。Project 使用 `project-state.json`，Feature 使用自己的 `state.json`；二者是阶段、依赖、版本和过期状态的权威来源。`work-items.json` 只负责定位，INDEX 与 Markdown 状态标记是人类可读投影，冲突时以对应对象状态为准并报 error。

**跨文件一致性协议**：状态文件、INDEX 和 Markdown 无法组成文件系统级多文件事务，因此每次阶段更新必须生成唯一 `operation_id`。先校验新状态和全部待写投影，再原子写入带 `projection_status=pending` 的对象状态，随后更新 INDEX 和 Markdown，全部成功后再次原子写入 `projection_status=in_sync`。任一步失败均保留同一 `operation_id`、失败目标和重放信息；恢复时先完成或回滚该操作，禁止在 `pending` 状态继续下游命令。

**独立性边界**：本 Skill 不依赖外部编排、关系分析或状态服务。代码关系能力以 Skill 自己维护的索引实现；任务编排、运行时验证和日志调试由 Skill 自己定义协议和产物。外部工具只能作为可探测、可替换的底层工具，不能成为流程前置依赖。

**代码关系索引边界**：索引是导航和影响分析加速层，不是事实最终来源。索引中的符号、关系和快照必须能回指源码文件/行号；无法回指的结果只能标为待核实，不得直接写入 E1 事实。

代码索引的 `commit`、构建时间、扫描范围和错误列表由对应对象状态的 `code_index` 记录；Project greenfield 初始阶段允许 `code_index.status=not_initialized`，但必须标记 `assurance=baseline`，并在基础任务中建立索引。索引不存在、对应 commit 变化或存在未处理分析错误时，相关 Detailed/sync 结果必须标记 `stale` 或 `assurance=degraded`，不得静默当作完整影响分析。

依赖方向固定：`AskMe → Overall → Detailed → Plan → 实现`，Project 和 Feature 都使用这条链。Project Breakdown 产出工程基础任务与 MVP Feature 清单；Project Execute 先把项目推进到 `foundation_ready`，再编排子 Feature 链，全部 MVP Feature 通过后由 Project Review 判定 `mvp_ready`。禁止**静默**跳阶段；light 路径可将阶段显式记为 `not_applicable` 或合并为精简产物，但必须在对象状态中记录理由、风险判定和仍然保留的验收/验证义务。

### 3.5 风险分级工作流

7 个命令保持不变，`workflow_profile` 只控制执行深度。`auto` 在 askme 开始时根据影响范围给出档位和依据，用户可覆盖；一旦出现高风险信号必须升级，不能自动降级。

| 档位 | 适用范围 | 允许精简 | 不可省略 |
|------|---------|---------|---------|
| `light` | 小缺陷、局部配置/文案、低风险单模块改动 | 决策点合并；Overall 可标 `not_applicable`；Detailed/Plan 使用精简模板；评审角色按需合并 | 可判定验收标准、代码/配置证据、验证命令、实现偏差、impl review |
| `standard` | 普通业务特性、跨前后端但边界清晰 | 使用当前默认流程与抽查比例 | 完整文档链、追溯矩阵、design + impl review |
| `full` | 安全/权限、数据迁移、外部契约、支付、合规、多仓库或不可逆变更 | 不允许精简；关键声明和关键验证全量核查 | 完整流程、回滚方案、独立验收、全角色评审、收敛检查 |

自动升级信号：权限或敏感数据、数据库 schema/迁移、公开 API/消息契约、不可逆操作、跨仓库发布、生产基础设施、核心交易链路。无法判断风险时默认 `standard`，不得默认 `light`。

---

## 4. 命令设计

七个命令保持同一名称和主阶段，但每次只处理一个由 `subject_type` 标识的工作对象。调度器先通过 `subject_id` 读取权威状态，再加载 Project 或 Feature 分支。后续命令不得重新判断对象类型。

| 命令 | Project 分支 | Feature 分支 |
|------|--------------|--------------|
| askme | 项目目标、MVP、用户、产品和运行约束 | 特性范围、行为、边界和验收 |
| overall | 产品模块、核心流程、总体架构和 MVP 地图 | 特性场景、页面范围和受影响模块 |
| detailed | 技术选型、仓库结构、工程基线和 MVP 技术设计 | 基于现有项目代码完成特性设计 |
| breakdown | 工程基础任务 + MVP Feature 清单及依赖 | 特性纵向切片任务 |
| execute | 建立工程基线并编排 MVP Feature 链 | 实施单项特性任务 |
| review | 判定 `foundation_ready` 或 `mvp_ready` | 判定特性实现是否完成 |
| sync | Project 变化向子 Feature 传播 | Feature 变化反查 Project 基线 |

### 4.1 askme — 需求访谈

**对象识别前置**：显式 ID 优先；无 ID 时检查项目状态、代码和用户意图。空仓库或完整产品意图作为 Project 候选，已存在 ready Project 中的局部能力作为 Feature 候选；存在歧义时把对象类型作为第一个决策点。确定后分配 `PJ-xxx` 或 `FT-xxx`，写入 `subject_type`、`subject_id` 和 `project_id`。必须确定负责人（默认 `git config user.name`）。

**Project 访谈**：确认项目目标、目标用户、MVP 与非目标、核心能力、端形态、用户流程、数据与敏感性、权限、多租户和审计、外部集成、技术栈约束、仓库组织、部署环境、可观测性、备份恢复、安全要求及项目级验收标准。

**Feature 访谈**：沿用既有的用户故事、范围、正常/异常/边界、依赖、非功能要求、UI 决策和验收标准访谈；正常情况下父 Project 必须至少为 `foundation_ready`。

**流程**：

1. **对象识别**：确定 Project/Feature；AskMe 完成前可经用户确认纠正，完成后不得静默翻转
2. **L0 调研**（轻量，ad-hoc）：Feature 确认现有功能；Project 检查空目录、已有代码、可复用资产和环境约束。能从仓库回答的不问用户，结果直接进决策点背景
3. 按对象模板创建 AskMe 文档，初始化权威状态并注册 work-items/INDEX（状态 🟣 澄清中）
4. 结构化决策点访谈：问题→背景→选项表→推荐→用户结论→验收标准；按 `subject_type` 加载对应问题体系
5. **UI 关键决策点**（涉及页面时强制）：端形态、关键交互、设计系统、可访问性等级和响应式范围
6. 分批向用户确认，每轮问答后立即写盘（跨会话可恢复）
7. 每个已确认决策点补写可判定验收标准，Project 额外形成 MVP 完成标准
8. 全部 ✅ 后状态改「已完成」，输出携带 `subject_type/subject_id/project_id` 的 JSON + next_steps(overall)

**恢复与续访**：已有未完成 AskMe 则从最近未确认决策点续访；要求变更已确认决策时转 sync。

### 4.2 overall — 概要设计

**门禁**：AskMe 存在且状态「已完成」、全部决策点 ✅。

**Project 分支目标**：将项目决策组织为人可理解的产品与系统总体方案，包含目标用户、核心场景、产品模块地图、端到端业务流程、客户端/服务端/数据/基础设施边界、仓库组织、MVP Feature 清单、非目标、依赖和主要风险。空仓库没有“现有资产”不构成失败，应明确记录 greenfield 基线和待选技术资产。

**Feature 分支目标**：将特性决策组织为总体概述、使用场景、受影响模块、页面清单和可复用现有资产，并说明它与父 Project 总体设计的关系。

**流程**：

1. 通过 `subject_id` 读取状态并选择 Project/Feature 分支，不重新推断
2. **L1 调研**：Feature 调研 UI 资产和现有架构；Project 调研空仓库状态、已有资产、组织约束和可用工程基线
3. 提取 AskMe 输入，Project 生成项目总体方案和 MVP 地图，Feature 生成特性总体方案
4. **页面清单**（涉及 UI 时强制）：核心页面、职责、信息架构和关键路径；每个场景标注来源决策点
5. design 评审（PM + 架构师 + UX，最多 3 轮修复循环）
6. 更新对象状态和 INDEX（状态 🟠 设计中）
7. markdownlint + B1–B5
8. JSON + next_steps(detailed)

**硬规则**：场景和 MVP Feature 必须可溯源到决策点，无法溯源视为镀金；不越阶段写字段级接口、组件树或任务细节。

### 4.3 detailed — 代码调研与详细设计（两阶段）

**门禁**：Overall 已完成、AskMe 全部决策点 ✅。

**Project 分支**：没有可用业务代码时不把缺失代码判定为错误，而是建立 greenfield 设计基线：技术栈及版本、仓库/包组织、模块边界、配置和环境、基础数据模型、认证授权、构建测试、部署和最小可运行版本。已有部分代码时，对可复用部分做代码调研，并将未初始化能力标为 `not_initialized`。

**Feature 分支**：采用两阶段深度调研，必须以父 Project 的架构和状态为约束。

**阶段一（L2 调研，深度冻结）**：

- 确定代码库清单（config repos 或自动扫描）→ 用户确认
- 初始化或刷新 skill 自己的代码关系索引（符号、调用、继承/实现、依赖、测试关联），记录索引对应的 commit；索引不可用时退化为逐次 LSP/搜索分析，不阻塞低风险特性
- 对变更入口先执行关系查询：调用方、被调用方、继承/实现方、相关测试和模块依赖；查询结果只用于定位，必须回到源码/LSP 核实并附文件/行号
- 逐库 code-explorer 扫描（一次一库），子 agent 任务扩展：
  - 原任务：扫代码结构/接口/数据模型/部署
  - **扩展任务（涉及 UI 时）**：扫设计系统路径、组件库 token 清单、现有页面清单、路由结构、现有可复用组件
- 每库产出 `CodeResearch-{repo}.md`（关键发现编号 `{repo简称}-G{n}`，每条附代码引用；UI 资产归入 `## UI 资产` 章节），并在文档中记录索引版本、查询结果和回源核实结果
- 歧义必须提问确认
- 完成后提示用户新会话续作

**阶段二（设计）**：检测调研文件齐备则进入，缺失只补扫（跨会话断点续作）→ 生成 Detailed：

- Overall 骨架继承 + Agent 自由扩展区（按复杂度决定章节）
- **`## UI 设计` 章节**（涉及 UI 时强制）：
  - 引用 SVG 效果图（每页面一份 `mockup-{page}.svg`，由 ui-generation 生成，详见 §5.6）
  - 字段对照表（页面字段 ↔ API schema 双向对照，作为 E4 证据载体）
  - 组件清单（复用/新增标注 + 设计系统 token）
  - 状态机（含空态/错误态/加载态）
- **`## 前端实现` 章节**（涉及 UI 时强制，与 UI 设计分离）：
  - 路由结构、组件树、状态管理方案、数据流、关键交互逻辑
  - 表单校验、错误处理、响应式策略、可访问性（ARIA/键盘导航/focus 管理）
  - 简单特性可写「按 UI 设计实现，无复杂前端工程」
- **后端 API 章节**：接口契约/数据模型/部署要求（无 UI 特性此章节为主）
- DoD（逐项可判定、标注来源、初始全 ❌）
- 假设清单（A1 声明集中）
- 追溯矩阵（决策点→场景→DoD 全覆盖；UI 一致性靠 E3/E4 证据约束，不加追溯环）
- design 评审（全部 4 角色 + 前端专家）+ 修复循环
- 更新 INDEX 链接
- JSON + next_steps(breakdown)

**硬规则**：DoD 禁止模糊表述（「性能好」❌→「P95 < 500ms」✅，无法量化须给人工验证步骤）；两阶段不在同一会话连续执行（除非用户明确要求）。

### 4.4 breakdown — 实施拆解

**门禁**：Overall 与 Detailed 均存在且 Detailed 已通过设计评审。

**Project 分支组装**：Plan 必须拆出两类内容：

1. 项目基础任务：仓库/工程骨架、配置和环境、构建启动、基础数据、认证授权、测试和部署门禁；
2. MVP Feature 清单：每个 MVP Feature 作为父 Project 下的子对象，明确依赖和进入 Feature 链的条件。

项目任务完成并通过 Project Review 后，状态为 `foundation_ready`；MVP Feature 全部完成并通过最终 Project Review 后，状态为 `mvp_ready`。

**输入理解（反假设）**：禁止假设 Detailed 章节结构；扫描全部标题后语义定位变更范围/技术方案/API/数据模型/UI 设计/前端实现/DoD；已有任务分解作为参考但不照搬。

**纵向切片（强制）**：禁止按技术层横向拆分；每个任务 = 用户可感知的端到端能力闭环（入口到出口穿过所有层）、完成即可独立验证、单一能力、1~3 天工作量、不过度拆分/合并；纯基础设施归 P1 前置且尽量少。Phase 按依赖链自然分组。

**任务标准结构**：`{P.T}` 编号 + 类型化描述子节（部署要求/工程属性/核心逻辑/校验范围/配置要点/UI 实现要点，参数值必须从 Detailed 提取）+ 交付物 + 验证步骤（checkbox，`V{P.T.N}` 编号，「操作→预期」+ 验证命令，每任务 4~8 条覆盖正常/异常/边界/安全/UI 视觉）。涉及运行时的任务必须同时写明启动/重建方式、端口、健康检查、日志来源和如何确认使用最新代码；不得用「页面正常」「看起来没问题」作为预期。

**UI 任务验证步骤**（涉及 UI 时强制）：视觉一致性验证（playwright 截图 vs SVG 效果图对照）、可访问性扫描（axe-core 跑无 critical/serious）、交互路径验证（关键路径脚本）。

**组装**：项目概述→进度概要表（⏳）→各 Phase→实施顺序→风险→变更模块总览→追溯矩阵（DoD↔任务↔验证步骤全覆盖）→ design 评审（开发+测试+前端专家，重点审验证步骤可执行性）→ JSON + next_steps(execute)。

### 4.5 execute — 任务执行与验证（堵缺口 1）

**门禁**：Plan 存在且有 ⏳ 任务。任务选择：用户指定或「实施顺序建议」中第一个前置已完成的未完成任务。

**Project 分支**：先执行项目基础任务，不能在工程尚未达到 `foundation_ready` 时默认并行推进业务 Feature；基础任务通过后，Coordinator 按 MVP Feature 清单创建/恢复子 Feature，并复用同一七命令链完成子 Feature。Project Execute 不把所有 MVP 业务代码塞进一个 Project 任务。

**单任务循环**：

1. 读任务上下文（任务定义 + Detailed 设计项 + 相关 G 编号）；「⚠️ 需在执行时确认」项先问用户
2. 按 profile 选择执行方式：`light` 可由当前 agent 直接执行；`standard/full` 默认由 Coordinator 创建一个边界明确的 Worker 执行，当前 agent 只负责上下文准备、调度和汇总。Worker 只接收当前任务、相关设计证据和验证步骤，不承担跨任务决策。
3. 实现；修改源码后立即执行 config `build_commands` 对应构建，失败先修复。涉及运行时的任务按 `runtime-verification` 协议启动/重建进程、健康检查并记录日志位置。
4. 逐条执行 `V{P.T.N}` 命令，**实际比对输出与预期断言**（禁止「看起来差不多」）：通过则勾选；失败进入「现象→证据→假设→修复→重建/重启→再验证」循环，同一问题最多 3 轮；仍失败标 🔴 阻塞、停止后续、上报。
5. UI 任务额外验证（涉及 UI 时）：
   - **视觉验证子agent**：playwright 截图实现页面 vs SVG 效果图，AI 视觉模型做一致性对比（pixel diff 或语义对比），偏差 < 阈值通过
   - **可访问性扫描子agent**：axe-core / pa11y 跑 WCAG 扫描，0 critical/serious 通过
   - **交互验证子agent**：playwright 跑关键路径脚本，状态切换/表单校验/键盘可达全通过
6. 全部 ✅ 后由独立 Verifier 子 agent 按 DoD 和验证步骤重跑（见 §5.5），Coordinator 只接收结构化 pass/fail、实际输出和证据位置；Verifier 不得复用 Worker 的自评结论。
7. 验收通过后更新进度概要表 ⏳→✅；**实现与设计的偏差显式登记**（偏差+原因），禁止静默偏离。
8. 追加「执行记录」（时间、Coordinator/Worker/Verifier 标识、关键命令实际输出摘要、日志/截图/API 证据、重试与偏差），供 review 抽查。

**单任务确认制**：每任务完成即停，汇报结果，用户确认后继续下一任务。

**完成判定**：execute 自检通过 ≠ 任务关闭。Worker 完成后必须由独立 Verifier 子 agent 只拿 DoD + 验证步骤 + 代码，独立跑 `V{P.T.N}` 命令、独立比对输出与预期断言、独立判 pass/fail；父 Coordinator 不参与判断过程只收结论，切断「自己写预期自己判」的自评环。Verifier 通过后进入 impl 评审，impl 评审通过才关闭（🔒）。验证依赖运行环境时须按配置启动/构造最小环境，无法构造标「需人工环境验证」上报，不得视为通过。

### 4.6 review — 双模式多角色评审（堵缺口 3/5/6/7）

**模式判定**：审文档 → design；审实现 → impl。

**Project 分支收尾**：基础任务完成后检查构建、启动、健康检查、最小运行路径和工程安全，判定 `foundation_ready`；所有 MVP Feature 的 impl review 通过后，再检查项目级验收和端到端路径，判定 `mvp_ready`。Feature 分支仍按单项特性判定 `implemented`。

**design 模式**（读入文档链至最深阶段）：

- L1 结构检查：章节完整（对照模板）、目录锚点、修订记录、链接有效、markdownlint、B1–B5；**涉及 UI 时**额外查核心页面清单完整性、每页面含状态机/空错载态/组件清单/字段→API 对照、设计系统 token 使用率
- L1 可执行性检查：验证步骤是否包含真实命令、预期输出、环境前置、端口/路径来源、执行顺序和任务边界；涉及运行时的步骤必须能通过 `runtime` 配置复现，禁止把主观判断写成验收条件
- L2 多角色评审（见 5.3 角色表，按阶段最少组合，**每角色 spawn 独立子 agent**（见 §5.5）——子 agent 只收文档+角色 prompt，互不见对方意见，父 agent 汇总分歧；每角色必须引用具体位置）
- L3 事实核查：全部技术性声明分级 E1/E2/E3/E4/E5/A1/F1
  - E1 按 §5.1 风险规则抽查——**抽查由独立子 agent 执行**（见 §5.5），子 agent 用 `lsp goToDefinition` / `read_file` 机械验证引用的文件/类/行号真实存在，禁止 AI 自报「已抽查」
  - **E3 抽查**（涉及 UI 时）：子 agent 用 `read_file` 读 SVG 文本，验证字段名在 SVG 中确实出现、style-tokens.json 与 SVG 内容一致
  - **E4 抽查**（涉及 UI 时）：子 agent 用 `lsp` 找 API 接口定义，机械对照字段对照表
  - F1 隐性编造标 error
- 一致性检测：按追溯矩阵规范查上下游断链与跨文档同事实冲突
- 执行 §5.8 收敛检查：需求、设计、计划之间的缺失/部分覆盖/矛盾必须收敛为修正文档或显式 follow-up 任务
- 报告落盘 `Review-design-{date}.md`；可自动修复的（结构/格式/证据标注）就地修复复检，需用户决策的列「待裁决」清单，最多 3 轮

**impl 模式**（读 Detailed + Plan 含执行记录 + 偏差清单，扫描代码）：

- 设计符合性审查员：双向偏差矩阵（「设计有但未实现」/「实现了但设计没有」），核对已登记偏差合理性，DoD 状态与代码实际一致性
- 代码质量审查员：缺陷（空指针/泄漏/并发/事务/错误处理）、安全（注入/越权/敏感信息）、契约一致性、测试覆盖
- **UI 符合性审查员**（涉及 UI 时）：实现页面 vs SVG 效果图视觉一致性、可访问性扫描结果、响应式断点、跨页面风格一致性
- 运行时符合性审查：抽查进程启动/健康检查/最新代码确认、API 或页面实际结果、日志关键路径；跨进程问题必须使用 request/task/correlation id 追踪
- 验收审查员：**由独立子 agent 担任**（见 §5.5），按工作流档位和风险重跑验证步骤，抽查 execute 声称通过的真实性（比对实际输出与执行记录），补充边界异常临时验证；高风险验证必须 100% 重跑；结论：通过 / 有条件通过（附条件清单）/ 不通过
- 执行 §5.8 收敛检查：比较 AskMe/Overall/Detailed/Plan/代码/测试，未实现、部分实现、计划外实现和契约矛盾必须形成明确处置

**收尾**：通过后任务 ✅→🔒、DoD 状态同步、INDEX 状态按完成度更新（全 ✅→✅ 已实现，否则 🟡 实现中）；不通过回 execute 修复或回 sync 做设计变更后重审。

### 4.7 sync — 变更传播（堵缺口 2/4）

sync 支持两种入口模式：

Sync 同时支持 Project 和 Feature 作为来源或目标。Project 级架构、技术栈、认证、数据和运行时变化必须反向检查所有子 Feature；Feature 暴露出的基础能力缺口需要回写 Project proposal，而不是只在 Feature 中打补丁。

| 模式 | 入参 | 工作流 |
|------|------|--------|
| **变更模式**（现有） | 源文档+位置+旧值→新值+原因 | 直接进影响分析 |
| **修正模式**（新增） | 位置+现象（「这里不对，应该是 X」） | 先根因分析定位源文档，再修正+影响分析 |

**触发**：需求/决策变化（变更模式）、设计修正、实现偏差回写、外部变化、发现某处不对（修正模式）。

**变更模式流程**：

1. **建立提案**：分配 `CR-{seq}`，将来源文档/位置/旧值→新值/原因写入 `changes/CR-{seq}-proposal.md`；此时不得改当前有效基线
2. **影响分析**：先用 skill 自维护的代码关系索引查询调用方、被调用方、继承/实现方、相关测试和模块依赖，再沿文档依赖图逐层推导受影响区段；索引结果必须回源码/LSP 核实。将文档/章节/代码/动作（更新/删除/新增）写入 `changes/CR-{seq}-impact.md`；影响已完成 Plan 任务时标「已实现部分受影响」纳入返工项；变更影响上游同样回溯
3. **零影响也要落证据**：允许影响文档数为 0，但必须记录检查过的依赖、代码引用和「无下游影响」推导，不制造无意义文档改动
4. **确认后合并基线**（用户确认影响清单后才执行）：逐级修改当前有效文档并标注 `CR-{seq}`；新模糊点→登记新决策点回 askme 补访；失效任务/验证步骤重写；返工任务显式标「返工」禁止静默吞并
5. **一致性复检并归档**：重查受影响区段追溯矩阵、关键事实跨文档一致性和 §5.8 收敛检查；成功后更新 `state.json` 版本/过期项并将 proposal/impact 移入 `changes/archive/`，拒绝的提案也归档但不修改基线
6. 输出 JSON：CR 编号、提案状态、影响文档数、修改项数、新增决策点/返工任务、复检结果

**修正模式流程**：

1. **报告位置+现象**：用户告知「这里不对」+ 位置（文档/章节/代码行）+ 现象（应该是 X）
2. **根因分析**（关键步骤）：沿依赖图回溯——这个错误源自哪个文档？可能是 AskMe 决策点错了/Overall 场景错了/Detailed 设计错了/Plan 任务错了/代码错了；用代码关系索引（调用/继承/依赖/测试）+ 追溯矩阵 + E1/E2/E3/E4/E5 证据做回溯定位，索引结果必须回源码核实；输出根因文档清单 + 各文档的具体错误位置
3. **建立修正提案**：将根因、建议修正和证据写入 `changes/CR-{seq}-proposal.md`，当前基线保持不变
4. 影响分析（复用变更模式第 2 步起）：沿依赖图正向传播
5. 用户确认后同步修改所有受影响产物（文档 + 代码 + UI 设计章节 + SVG 效果图）
6. 一致性与收敛复检，更新 `state.json` 并归档提案
7. 输出 JSON：根因文档 + 修正项 + 影响文档/产物 + CR 编号 + 提案状态

**SVG 效果图变更**：设计稿（SVG）变更时，影响图独立一条链：`SVG 效果图 → UI 设计章节 → Detailed(API 契约/前端实现) → Plan(前端任务/验证步骤) → 已实现页面(返工)`。修正模式触发时，先回溯 SVG 是否仍是当前最新（如 ui-generation 重新生成），再传播影响。

**硬规则**：每次变更都必须做影响分析，但不得为了形式强制修改无关文档；「无下游影响」必须附推导依据。决策点翻转必须回 AskMe 更新，禁止绕过源文档直改下游；待审批 proposal 不得污染当前有效基线；跨文档同事实冲突按 error 处理。

---

## 5. 横切机制

### 5.1 证据链（evidence-rules，堵缺口 6/7）

| 类别 | 判定 | 标注方式 |
|------|------|---------|
| E1 代码证据 | 引用实际存在的文件/类/接口/配置 | Markdown 链接或行内代码 |
| E2 文档证据 | 引用已确认决策或调研发现 | 「依据决策点 N」/「依据 {repo}-G{n}」 |
| E3 视觉证据 | SVG 效果图文件存在 + 字段名在 SVG 文本中出现 + style-tokens 与 SVG 一致 | SVG 文件链接 + 字段位置 |
| E4 契约证据 | 页面字段 ↔ API schema 双向对照 | 字段对照表（Detailed UI 章节内） |
| E5 运行时证据 | 真实进程/API/页面/日志/测试输出证明行为已发生且符合断言 | 执行记录中的命令、实际输出、日志/截图/API 响应位置 |
| A1 显式假设 | 未经确认的推断，已声明 | 「⚠️ 假设待验证」集中清单 |
| F1 隐性编造 | 无证据又不标假设 | **禁止出现** |

生成时：描述存量系统前必须扫描代码；路径先验证存在；具体值（字段/签名/版本/端口）必须来自调研或用户输入；验证命令的路径端口参数须有证据，否则标「⚠️ 需在执行时确认」。代码关系索引只作为导航加速，所有 E1 声明必须回指源码/LSP；涉及行为正确性的声明必须补充 E5 运行时证据。

核查时（review L3）：声明全量分级，E1 覆盖率按风险而不是固定一刀切

- 所有档位：安全/权限、数据迁移、外部 API/消息契约、不可逆操作相关声明 100% 核查
- `light`：直接变更范围内的 E1 全量核查；范围之外不扩散抽查
- `standard`：E1 总体抽查 ≥30%，关键路径与边界条件优先
- `full`：E1 总体抽查 ≥50%，所有关键技术声明 100% 核查
- E1 抽查由独立子 agent 执行（见 §5.5），用 `lsp goToDefinition` / `read_file` 机械验证引用真实存在，禁止 AI 自报「已抽查」
- **E3 抽查**（涉及 UI 时）：子 agent 用 `read_file` 读 SVG 文本，机械验证字段名在 SVG 中确实出现、style-tokens.json 与 SVG 内容一致
- **E4 抽查**（涉及 UI 时）：子 agent 用 `lsp` 找 API 接口定义，机械对照字段对照表
- F1 识别为 error（「不靠谱文档」主要来源：具体数值无出处、声称的现有功能无代码对应、接口字段与代码不符、UI 字段与 API schema 不一致）
- E5 核查：涉及运行时行为、跨进程链路、缓存/队列/异步状态或 UI 交互的关键声明，必须抽查真实命令输出、日志、API 响应或浏览器结果；只有静态代码检查不能替代 E5。

### 5.2 追溯矩阵（traceability，堵缺口 4）

追溯链：`决策点 D{N} → 场景 S{N} → DoD DD{N.M} → 任务 T{P.T} → 验证步骤 V{P.T.N}`。

**不加新环**——UI 一致性靠 E3/E4 证据约束，不靠追溯环。理由：UI 内容分布在各阶段章节内，强行入环会产生多对多追溯，矩阵复杂度爆炸；E3（视觉证据）+ E4（契约证据）已能保证 UI 一致性。

各命令正向/反向追溯义务 + 一致性检查项（断链/镀金/同事实冲突/状态不符，error/warning 分级）。矩阵作为独立章节落盘于 Detailed 与 Plan 末尾，状态列 ⏳/🔄/✅/🔒。

### 5.3 多角色评审（review-roles，堵缺口 5/7）

| 模式 | 角色 | 核心视角 |
|------|------|---------|
| design | 产品经理 | 需求覆盖、场景完整、验收标准可判定、边界异常识别 |
| design | 架构师 | 技术可行（对照调研证据）、架构一致、依赖合理、数据模型自洽 |
| design | 开发 | 粒度 1~3 天、依赖可线性执行、存量代码引用真实、实现遗漏（配置/迁移/兼容/回滚） |
| design | 测试 | DoD 可测、验证步骤覆盖四类路径、命令真实可执行、不可自动化项有人工步骤 |
| design | **UX 设计师**（新增） | 信息架构/交互流程/可用性/空错载态覆盖/可访问性设计 |
| design | **前端专家**（新增） | 组件复用率/状态管理可行性/路由结构/性能（首屏/交互延迟） |
| impl | 设计符合性审查员 | 双向偏差矩阵、登记偏差合理性、DoD 状态与代码一致 |
| impl | 代码质量审查员 | 缺陷、安全、契约一致性、测试覆盖 |
| impl | 验收审查员 | 独立重跑验证、抽查真实性、补充边界验证、验收结论 |
| impl | **UI 符合性审查员**（新增，涉及 UI 时） | 实现 vs SVG 效果图视觉一致性、可访问性扫描结果、响应式断点、跨页面风格一致性 |

各阶段最少角色组合：

| 阶段 | 原组合 | 新组合（涉及 UI 时） |
|------|--------|---------------------|
| AskMe | PM+架构 | 不变 |
| Overall | PM+架构 | PM+架构+UX |
| Detailed | 全部 4 | 全部 4 + 前端专家 |
| Plan | 开发+测试 | 开发+测试+前端专家 |

**每角色由独立子 agent 担任**（见 §5.5）——子 agent 只收文档+角色 prompt，互不见对方意见，独立输出意见（引用具体位置，禁止泛泛评价）；父 agent 汇总后，通过标准 error=0 且无 fail；修复循环最多 3 轮后仍不通过，或子 agent 之间分歧无法收敛时，整理分歧上报**真人裁决者**（见 §5.5.4）——真人不参与流程执行，仅在子 agent 分歧或验收 fail 争议时介入，事件驱动而非流程驱动。

### 5.4 通用共享规则

1. 前置门禁不满足即终止，输出缺失清单与补救指引
2. 文档必须落盘（禁止仅对话输出），写入前 markdownlint + B1–B5
3. 每阶段完成更新 INDEX 状态与链接，输出结构化 JSON（`subject_type`/`subject_id`/`project_id`/`phase`/`status`/产出路径/`next_steps`）
4. 命令文件按需加载：调度器路由后只读当前命令文件及其引用的规范
5. **调研分层**（见 §5.7）：每个阶段按需做不同粒度调研（L0/L1/L2），不集中在 Detailed
6. **状态写入顺序**：按 §3.4 的 `operation_id + projection_status` 协议更新对象状态、INDEX 和 Markdown；任一步失败都标记 `state_sync_error` 并停止向下游推进
7. **档位可升级不可静默降级**：执行中发现高风险信号时立即升级 profile 并补齐缺失门禁；降级必须由用户确认并记录理由
8. **独立能力自持**：代码关系索引、任务编排、运行时验证和日志调试由 Skill 自己定义协议与产物；不得把外部服务作为门禁或事实来源
9. **运行时证据留存**：凡执行了进程/API/浏览器/日志验证，必须把命令、预期、实际输出和证据位置写入执行记录，供独立 Verifier 和 review 抽查

### 5.5 子 agent 调度机制（质量保证强化）

> 本节是对 §4.5/§4.6/§5.1/§5.3 中「独立子 agent」机制的统一定义。
>
> 子 agent 的本质价值是**切断上下文继承**——子 agent 不带父 agent 写代码/写文档时的论证偏见，只带着「任务+代码/文档」独立判断，从而把「靠 LLM 自觉」的质量门转变为「靠独立核查」的质量门，把「看着能保证」推向「能保证」。

本节同时定义任务编排协议：Coordinator 负责阶段路由、上下文裁剪、子任务关系和结果汇总；Worker 负责单一实施任务；Verifier 负责独立验收。该协议由 skill 自己实现，不依赖外部任务系统。

#### 5.5.1 spawn 原则

1. **独立上下文**：子 agent 不继承父 agent 的前序对话，只收明确输入（文档路径 + 角色 prompt + 工具权限）
2. **互不见意见**：多个子 agent 并行时，彼此不共享输出，父 agent 汇总后才可见
3. **机械优先**：能用工具机械验证的（LSP / file exists / build 输出比对 / SVG 文本解析 / axe-core 扫描），子 agent 必须用工具，不得凭语义判断
4. **结论回传**：子 agent 只回传结构化结论（pass/fail + 证据 + 位置），不回传推理过程，父 agent 不被带偏
5. **职责隔离**：Worker 不关闭任务，Verifier 不修改预期断言，Coordinator 不把 Worker 自报结果当成验收结论
6. **父子可恢复**：每个 Worker/Verifier 都记录 `parent_task_id`、输入快照、输出产物、状态和失败原因；会话中断后从最近状态恢复

#### 5.5.2 按阶段 spawn 方案

| 阶段 | spawn 什么 | 输入 | 输出 |
|------|-----------|------|------|
| Detailed 代码调研 | code-explorer 子 agent（每库一个） | 代码库路径 | `CodeResearch-{repo}.md`（含 `## UI 资产` 章节，附代码引用） |
| Detailed 代码关系分析 | code-index 子 agent（按仓库/变更范围） | 代码库路径 + 变更入口 | `.devflow/code-index/` 更新 + 关系查询结果（可回源） |
| Detailed/Overall 多角色评审 | 并行 spawn PM/架构/开发/测试/UX/前端专家 子 agent | 文档 + 角色 prompt | 各角色独立意见（引用具体位置） |
| Execute 验收 | 独立验收子 agent | DoD + 验证步骤 + 代码 | pass/fail + 实际输出 + 偏差 |
| Execute 实施编排 | Coordinator → Worker → Verifier | Plan 任务 + Detailed 设计项 + 验证步骤 | 父子任务状态、执行记录、独立验收结论 |
| Execute UI 验证（涉及 UI 时） | 视觉验证 / 可访问性扫描 / 交互验证 子 agent | playwright 截图 + SVG 效果图 / 页面 URL | 一致性 pass/fail + a11y 扫描结果 |
| Review impl | 设计符合性 / 代码质量 / 验收重跑 / UI 符合性 四类子 agent | Detailed + Plan + 代码 + SVG | 偏差矩阵 / 缺陷清单 / 重跑结果 / UI 一致性结果 |
| Review L3 证据抽查 | E1 / E3 / E4 抽查子 agent | 文档 + 引用清单 + SVG 文件 + 字段对照表 | 抽查结果（引用真实 / 不存在 / 字段一致） |
| Sync 影响分析 | 依赖扫描子 agent | 变更点 + 代码库 | 受影响文档/章节清单 |
| Sync 修正模式 | 根因分析子 agent | 位置 + 现象 + 文档链 | 根因文档清单 + 各文档错误位置 |
| UI 生成（见 §5.6） | 多模态生成子 agent | style-tokens + 页面描述 | SVG 效果图 |

#### 5.5.3 最小可行组合（落地优先级）

只做以下五件，「看着能保证」即大面积转为「能保证」：

1. **execute 实施 Worker + 独立 Verifier**（P0，收益最大）：切断「自己实现自己验收」的自评环
2. **内置代码关系索引**（P0）：用 LSP/搜索/解析建立可回源的调用、继承、依赖和测试关系，支持 detailed/sync 影响分析
3. **E1 证据机械抽查子 agent**（P0）：用 `lsp goToDefinition` / `read_file` 验证引用真实存在，替代 AI 自报「已抽查 30%」
4. **运行时验证与日志调试协议**（P0）：按 runtime 配置复现进程/API/页面，保留 E5 实际证据，失败按假设循环处理
5. **多角色评审并行子 agent**（P1）：每角色独立上下文，父 agent 只在分歧时找真人

**UI 相关最小可行组合**（涉及 UI 时）：

1. **视觉验证子 agent**（P0）：playwright 截图 vs SVG 效果图机械对比，切断「自己实现自己说像」自评环
2. **E3/E4 证据机械抽查子 agent**（P1）：用 `read_file` / `lsp` 验证 SVG 字段、API 契约真实存在
3. **UI 符合性审查子 agent**（P1）：impl 评审独立核查实现 vs 效果图

#### 5.5.4 真人角色最小化

多角色全交子 agent 后，真人只剩**一个位置**：

> **裁决者**：仅在子 agent 之间分歧无法收敛、或验收子 agent 判 fail 但实现者不服时介入。
> 事件驱动而非流程驱动，工作量从「每阶段都要审」降到「偶尔仲裁」。

#### 5.5.5 已知局限（子 agent 也救不了的）

1. **同模型同源幻觉**：父子同模型可能各自幻觉同一个错。若平台支持给子 agent 指定不同模型，优先在 **execute 验收** 和 **review impl 验收重跑** 两位换模型。
2. **内容正确性天花板**：子 agent 把下限从「流程不乱」抬到「对抗性核查」，但「设计本身对不对」仍受模型能力限制。
3. **真人不能为零**：子 agent 分歧 + 验收 fail 争议终需人拍板，但频次极低。
4. **多模态生成质量天花板**（UI 特有）：skill 自生 SVG 效果图受多模态模型能力限制，复杂布局/精确字段可能需人工调整。
5. **隔离能力不可假定**：若平台不能保证子 agent 独立上下文、独立工具执行或指定模型，报告必须标记 `assurance=degraded`、列出缺失能力，不能仍宣称完成了独立验收。

### 5.6 UI 效果图生成能力（新增，堵缺口 7）

> 封装为 `references/ui-generation.md`，由 detailed 阶段二调用。本节定义能力规范。

#### 5.6.1 定位

UI = **截图级效果图（SVG 格式）**，作为实现视觉标准，页面照这个做。由 skill 自己生成，不依赖外部 Figma。

理由：SVG 是文本，可 AI 直接生成、可 diff、可机械解析（E3 抽查子 agent 可 `read_file` 读内容验证字段）、项目已有先例（docs 下 56 个 SVG）。

#### 5.6.2 三段式工作流

```text
阶段一：风格识别（静态分析，不访问 URL）
  ├─ 用户输入：路径 / URL / 功能描述（三种均支持）
  ├─ skill 解析输入 → 路径（URL 提取 path 部分，功能描述语义匹配）
  ├─ 读项目路由配置 → 路径 → 组件文件
  │   └─ 多框架支持：React Router / Vue Router / Next.js (App/Pages Router) / Angular
  ├─ 读组件文件 + import 链 → 提取样式信息
  │   └─ 来源：CSS 变量 / 主题文件 / Tailwind class / styled-components / CSS Module / 组件库主题覆盖 / inline style
  ├─ 多页面交叉验证，汇总 style-tokens.json
  └─ 路径找不到组件 → 让用户直接给源码路径作为兜底

阶段二：风格约束生成（产出 SVG）
  └─ 调用多模态技能生成 SVG，prompt 模板注入 style-tokens 作为约束

阶段三：质量检测（不通过重生成，最多 3 轮）
  ├─ 风格一致性：解析 SVG 文本 vs style-tokens 比对（机械可查）
  ├─ 多页面一致性：多个 SVG 之间风格变量比对（配色/字号/圆角/间距不漂移）
  └─ 字段准确性：字段名在 SVG 文本中确实出现（vs Detailed UI 章节字段清单）
```

#### 5.6.3 用户输入支持

| 输入形式 | 处理 |
|---------|------|
| 纯路径 `/products` | 直接用 |
| 完整 URL `http://xxx/products` | 正则提取 path 部分 `/products` |
| 功能描述 `商品列表页` | 语义匹配：路由 `name`/`title` 字段 → 组件文件名（如 `ProductsList.tsx` 含 "Products"）→ 多候选时让用户确认 |

#### 5.6.4 多框架路由识别

| 框架 | 路由配置位置 | 识别方式 |
|------|------------|---------|
| React Router | `routes.tsx` / `App.tsx` 的 `<Route>` 或 `createBrowserRouter` | `search_content` 找 `path:\s*['"]/products` |
| Vue Router | `router/index.ts` 的 `routes` 数组 | 同上 |
| Next.js (App Router) | 文件系统 `app/products/page.tsx` | `search_file` 找 `app/**/page.tsx` |
| Next.js (Pages Router) | `pages/products/index.tsx` | `search_file` 找 `pages/**` |
| Angular | `*.routing.ts` 的 `Routes` 数组 | `search_content` 找 `path:` |

跟踪组件文件用 `lsp goToDefinition`，处理懒加载、嵌套路由、动态路由。

#### 5.6.5 质量检测机制

两道关：

| 关 | 检测者 | 检测什么 |
|----|--------|---------|
| 内置检测（生成时） | ui-generation 内部 | 风格一致性 / 多页面一致性 / 字段准确性 |
| 浏览器验证（execute 时） | Playwright + axe-core/pa11y | 实际渲染、响应式、溢出/重叠、交互、可访问性 |
| 独立复核（review 时） | UI 符合性审查子 agent | SVG 效果图 vs 浏览器实际截图（最终一致性） |

SVG 文本检查只能证明字段和 token 被写入，不能证明浏览器真实渲染正确；最终 UI 结论必须基于目标桌面/移动视口的浏览器截图与交互结果。独立子 agent 复核用于切断「自己生成自己判」自评环。

#### 5.6.6 退化策略

| 情况 | 退化方案 |
|------|---------|
| 多模态技能不可用 | 不生成 SVG，由用户提供外部图 + Markdown 字段描述 |
| 多框架路由找不到组件 | 让用户直接给源码路径 |
| 现有系统无主题文件/CSS 变量 | 退化到「让用户提供参考」或默认设计系统（Material/Ant Design） |
| AI 生成 SVG 不准 | 退化到 ASCII 框图 + Mermaid flowchart（描述结构）+ 字段对照表（描述内容） |

### 5.7 调研分层机制（新增）

> 调研不该只在 Detailed 做。每个阶段都做调研，粒度不同，只有 Detailed 阶段一保留独立文档。

| 阶段 | 调研类型 | 粒度 | 产出形式 | 是否独立文档 |
|------|---------|------|---------|------------|
| askme | 现有功能确认 | L0 轻量 | 决策点背景（附 E1 代码引用） | 否，写入 AskMe |
| overall | UI 资产 + 现有架构 | L1 中等 | Overall 文档内 `## 现有资产` 章节 | 否，文档内章节 |
| detailed 阶段一 | 深度代码（接口/数据模型/部署 + UI 资产） | L2 重量 | `CodeResearch-{repo}.md`（含 `## UI 资产`） | **是**（冻结结论） |
| breakdown | 定向（任务相关代码定位） | L0 轻量 | 任务背景 | 否，写入 Plan |
| execute | 任务上下文 | L0 轻量 | 执行记录 | 否，写入执行记录 |

**Detailed 阶段一保留独立文档的理由**：Detailed 阶段二要基于「冻结的调研结论」做设计决策，不能基于动态扫描的代码（上下文容量 + 事实收集 vs 决策分离）。其他阶段调研是辅助性的，直接写进对应文档章节即可。

**与证据链的耦合**：

| 调研层 | 证据类别 | 标注方式 |
|--------|---------|---------|
| L0 | E1 代码证据 | 行内代码引用 |
| L1 | E1 + E2（文档证据，引用 Overall 内 `## 现有资产`） | 「依据 Overall §现有资产」 |
| L2 | E1 + E2（引用 `CodeResearch-{repo}.md` 的 `{repo}-G{n}`） | 「依据 {repo}-G{n}」 |

### 5.8 收敛检查（convergence）

> 不新增命令，由 review(design/impl) 和 sync 复检阶段调用。目的不是再生成一份泛泛报告，而是确保需求、设计、任务和实现最终指向同一件事。

**输入**：AskMe 决策点与验收标准、Overall 场景、Detailed 设计/DoD/API/UI 契约、Plan 任务与验证步骤、实现代码与测试、代码关系索引（如已构建）、运行时执行记录与 E5 证据、已批准偏差、未决 proposal。

**检查维度**：

1. **缺失**：上游有要求，下游没有设计、任务、实现或验证
2. **部分覆盖**：只覆盖正常路径，边界/错误/权限/响应式等要求遗漏
3. **矛盾**：同一字段、状态、接口、数值或行为在不同制品中定义不一致
4. **计划外实现**：代码存在但任何已批准需求/设计/偏差记录都没有来源
5. **过期**：上游版本已变化，下游仍引用旧版本或 `state.json` 标记 stale
6. **关系/运行时缺证据**：代码关系索引无法回源，或行为声明缺少实际 API/日志/页面/测试证据

**输出与处置**：每项输出 `source → target → status(missing/partial/conflict/unplanned/stale) → evidence → action`。能确定修复方式的生成或更新 Plan follow-up 任务；涉及需求取舍的进入 sync proposal；误报须记录排除依据。error 未清零不得宣称 design/impl review 通过，warning 必须有负责人或明确接受记录。

**范围控制**：只检查当前 profile 要求的制品和本次变更影响范围；`full` 对完整文档链与关键实现做全量收敛，`light` 对直接变更范围做全量收敛，避免把小修复扩成无边界审计。

---

## 6. SKILL.md 调度器设计

- **命令路由表**：7 命令触发意图 → 对应 command 文件；执行命令前必须完整读取对应文件
- **内部能力路由**：不新增用户命令；`detailed/sync` 按需调用内置 code-index 能力，`execute/review` 按 profile 调用 Coordinator/Worker/Verifier 与 runtime-verification 能力。所有能力由 skill 自己提供，外部工具仅作为底层探测与执行手段。
- **对象和阶段判定（自动路由）**：用户说「继续 PJ-XXX/FT-XXX」时先通过 `work-items.json` 定位对应状态文件，再读取 `subject_type`、`phase`、`artifact`、`task`、`dependency`、`stale` 状态；仅在旧对象没有状态文件时，才按文档存在性恢复并补建状态文件。用户只说「继续」时，若存在多个进行中的对象必须让用户选择。下表是恢复映射，不是运行时唯一判断依据：

| 对象状态 | 后续产物 | 路由 |
|----------|----------|------|
| 不存在 | — | askme，先确定 `subject_type` |
| AskMe 未完成 | — | askme 续访 |
| AskMe 已完成 | Overall 不存在 | overall，按 `subject_type` 分支 |
| Overall 已完成 | Detailed 不存在 | detailed，Project/Feature 分支 |
| Detailed 已完成 | Plan 不存在 | breakdown，Project 产出基础任务与 MVP Feature 清单 |
| Plan 有未完成任务 | — | execute；Project 先基础任务，之后编排子 Feature |
| Plan 全完成未评审 | — | review；Project 判定 `foundation_ready` 或 `mvp_ready` |

- **变更优先级**：存在已确认但未合并的 CR，或当前阶段依赖被标 stale 时，先路由 sync，禁止继续消费过期设计
- **档位路由**：askme 首次进入时解析 `workflow_profile`；`auto` 必须落盘风险信号与选档理由，后续命令按同一档位加载对应规则
- frontmatter description 覆盖触发词：FT 编号、需求澄清、设计、拆解、执行、评审、同步、继续/下一步、**这里不对、错了、修正、修复、根因、为什么**（修正模式触发词，新增）

---

## 7. 执行计划（待「开始执行」指令）

对已创建的 `.codebuddy/skills/asdm-devflow/` 做：

1. **配置解耦**：SKILL.md、7 个命令文件和模板不得硬编码工作项、追踪系统、模块编号或项目路径，统一改为读取 `.devflow/config.md`（未配置用默认值）
2. **新增 `references/config-schema.md`**
3. **索引逻辑改为自动维护 `{docs_root}/INDEX.md`**（列：编号/名称/状态/负责人/文档链接）
4. **调整 4 个模板**：头部元信息配置驱动（追踪链接仅配置时出现）
5. 清理初始化遗留示例文件（`references/api_reference.md`、`scripts/`、`assets/` 示例）
6. markdownlint 全量校验 + 打包验证
7. **新增 UI 机制**（基于本设计补强）：
   - 新增 `references/ui-generation.md`（UI 效果图生成能力规范）
   - 新增 `assets/style-tokens-template.json`（风格 token 模板）
   - 4 个命令文件（askme/overall/detailed/breakdown）增加 UI 职责描述
   - execute/review/sync 命令文件增加 UI 验证/审查/变更传播逻辑
   - detailed-template 增加 `## UI 设计` 和 `## 前端实现` 章节
   - evidence-rules.md 增加 E3/E4 类别
   - review-roles.md 增加 UX/前端专家/UI 符合性角色
8. **sync 命令扩展修正模式**：sync 命令文件增加修正模式入口（根因分析 → 修正 → 影响传播）
9. **新增风险分级工作流**：增加 `references/workflow-profiles.md`，为 light/standard/full 定义门禁、模板深度、评审角色与核查覆盖率
10. **新增机器可读状态**：增加 `references/state-schema.md`，实现每特性 `state.json` 的初始化、原子更新、状态迁移、stale 标记及 INDEX/Markdown 投影
11. **sync 引入提案区**：实现 `changes/` proposal/impact/archive 生命周期，确认前不修改当前有效基线
12. **新增收敛检查**：增加 `references/convergence.md`，接入 review(design/impl) 与 sync 复检并能生成 follow-up 任务
13. **新增内置代码关系分析**：增加 `references/code-intelligence.md` 与 Skill 自维护的 `.devflow/code-index/` 结构；实现符号/调用/继承/依赖/测试关系构建、刷新、查询和回源核实
14. **新增 Coordinator/Worker/Verifier 编排**：增加 `references/agent-orchestration.md`，实现父子任务、职责隔离、上下文裁剪、结果协议、恢复与失败重试
15. **新增运行时验证与调试协议**：增加 `references/runtime-verification.md`，实现 runtime 配置、进程/健康检查/日志记录、E5 证据、假设循环和清理规则
16. **更新状态与模板**：state.json 增加 code-index、parent/worker/verifier、runtime evidence 字段；Plan/执行记录模板增加实际输出和证据位置

### 7.1 落地优先级（基于 §5.5 子 agent 机制 + UI 机制）

| 优先级 | 动作 | 收益 |
|-------|------|------|
| P0 | 统一 JSON 输出与本地执行记录 | 保证阶段结果、验证证据和失败信息可追溯，不依赖外部上报服务 |
| P0 | 写完 SKILL.md frontmatter description + 路由表 | 触发可靠 |
| P0 | state.json schema + 原子状态迁移 + INDEX 投影 | 阶段恢复与过期检测可靠 |
| P0 | 内置代码关系索引（构建/查询/回源核实） | Detailed/sync 有真实影响分析能力 |
| P0 | Coordinator → Worker → Verifier 编排 | 切断实施自评环 |
| P0 | runtime 配置 + 可复现运行 + E5 证据 | 真实运行结果可复核 |
| P0 | execute 验收位 spawn 独立子 agent | 切断验收自评环 |
| P0 | UI 效果图生成能力（ui-generation.md + 三段式工作流） | 页面有正式承载位 |
| P0 | execute 视觉验证子 agent（涉及 UI 时） | 切断「自己实现自己说像」自评环 |
| P1 | E1 证据机械抽查子 agent | 替代自报 |
| P1 | light/standard/full 风险分级工作流 | 小改动不过度工程，高风险不漏门禁 |
| P1 | sync proposal/impact/archive 生命周期 | 当前有效事实与待议变更不混淆 |
| P1 | review/sync 收敛检查 | 自动发现缺失、部分覆盖、矛盾与计划外实现 |
| P1 | 多角色评审并行子 agent | 真对抗 |
| P1 | E3/E4 证据类别 + 抽查子 agent（涉及 UI 时） | 治理 UI 幻觉 |
| P1 | 多角色评审增 UX/前端专家/UI 符合性（涉及 UI 时） | 真对抗 UI 质量 |
| P1 | 可访问性扫描子 agent（涉及 UI 时） | 机械保证 a11y |
| P1 | 运行时日志调试循环与 correlation id | 跨进程问题可定位、可复现 |
| P2 | sync 修正模式（根因分析 → 修正 → 影响传播） | 错误发现闭环 |
| P2 | sync 影响分析用 `lsp findReferences` 机械扫依赖 | 图变提取 |
| P2 | 多框架路由识别全覆盖（React Router/Vue Router/Next.js/Angular） | 跨项目通用 |
| P2 | 存量特性迁移指引 | 不让两套永久并存 |

---

## 8. 决策记录

| 编号 | 决策点 | 结论 | 轮次 |
|------|--------|------|------|
| `DEC-001` | skill 覆盖范围 | 生成线+执行+质量+维护全闭环 7 命令 | 初稿+用户补缺口后 |
| `DEC-002` | 组织形态 | 1 个 skill 内命令分发（三层解耦：调度/命令/规范） | 用户确认 |
| `DEC-003` | 多角色评审 | 双模式（design 审文档 / impl 审实现），不只设计阶段 | 用户确认 |
| `DEC-004` | 独立性边界 | 能力在 Skill 内重新定义和实现，不依赖既有流程系统 | 用户确认 |
| `DEC-005` | 通用化 | skill 本体通用，项目配置外置 `.devflow/config.md` | 用户确认 |
| `DEC-006` | execute 粒度 | 单任务确认制 | 建议，无异议 |
| `DEC-007` | sync 粒度 | 影响清单用户确认后再同步 | 建议，无异议 |
| `DEC-008` | 命名/位置 | `asdm-devflow`，project scope `.codebuddy/skills/` | 建议，无异议 |
| `DEC-009` | 验收环节归属 | execute 验收由独立子 agent 执行，禁止实现者自评 | 批判性复盘新增 |
| `DEC-010` | 多角色评审执行体 | 每角色 spawn 独立子 agent，互不见意见，真人仅做分歧裁决 | 批判性复盘新增 |
| `DEC-011` | E1 证据抽查 | 由独立子 agent 用 LSP / `read_file` 机械验证，禁止 AI 自报 | 批判性复盘新增 |
| `DEC-012` | 外部上报范围 | 不引入外部上报服务；阶段结果以 JSON、Markdown、state.json 和本地执行记录承载 | 本轮范围确认 |
| `DEC-013` | 同模型幻觉局限 | 子 agent 切断自评但救不了同源幻觉；关键位优先换不同模型子 agent | 批判性复盘新增 |
| `DEC-014` | UI 机制定位 | UI = 截图级 SVG 效果图，由 skill 自生，不依赖外部 Figma | UI 补强新增 |
| `DEC-015` | UI 融合而非新增 | UI 内容分散到各阶段承担，不单独新增命令/文档阶段 | UI 补强新增 |
| `DEC-016` | UI 不存历史截图基线 | 直接看最新产物，sync 触发时重新生成或传播影响 | UI 补强新增 |
| `DEC-017` | UI 风格识别 | 静态分析（路径→路由配置→组件文件→源码），不访问 URL；多框架支持 | UI 补强新增 |
| `DEC-018` | UI 质量检测 | 三类机械检测（风格/多页面一致/字段准确）+ review 时独立复核 | UI 补强新增 |
| `DEC-019` | 工程层 UI 设计归属 | 归 Detailed `## 前端实现` 章节，与 `## UI 设计`（效果图）分离 | UI 补强新增 |
| `DEC-020` | E3/E4 证据新增 | E3 视觉证据（SVG）+ E4 契约证据（字段↔API），不可互相替代 | UI 补强新增 |
| `DEC-021` | 追溯矩阵不加新环 | UI 一致性靠 E3/E4 证据约束，不靠追溯环 | UI 补强新增 |
| `DEC-022` | sync 修正模式 | sync 支持变更模式 + 修正模式（根因分析）双入口 | UI 补强新增 |
| `DEC-023` | 调研分层 | 调研贯穿全流程 L0/L1/L2，只有 Detailed 阶段一保留独立文档 | 调研补强新增 |
| `DEC-024` | UI 多模态生成局限 | 多模态模型能力天花板，复杂布局/精确字段可能需人工调整 | UI 补强新增 |
| `DEC-025` | 工作流分级 | 7 命令不变，按 light/standard/full 控制执行深度；高风险只可升级不可自动降级 | 同类项目复盘新增 |
| `DEC-026` | 状态权威来源 | state.json 管阶段/依赖/版本/stale，INDEX 与 Markdown 是人类可读投影 | 同类项目复盘新增 |
| `DEC-027` | 当前基线与提案分离 | sync 先写 changes proposal/impact，确认后才修改有效文档并归档 | 同类项目复盘新增 |
| `DEC-028` | 最终收敛 | review 与 sync 比较需求/设计/任务/代码/测试，缺口转 follow-up 或 CR | 同类项目复盘新增 |
| `DEC-029` | 风险化核查 | 安全/迁移/外部契约等关键声明 100% 核查，其余按 profile 设覆盖率 | 同类项目复盘新增 |
| `DEC-030` | 代码关系能力落点 | 只吸收代码关系索引、关系查询和影响分析机制；由 Skill 自己实现，不依赖外部关系服务 | 本轮独立性澄清 |
| `DEC-031` | 代码索引事实边界 | code-index 只做导航和影响分析加速；所有关系结果必须回源码/LSP，无法回源不得作为 E1 事实 | 本轮独立性澄清 |
| `DEC-032` | 执行编排能力落点 | 吸收运行时复现、日志调试、验证步骤审查和 Coordinator/Worker/Verifier 编排；由 Skill 自己定义协议和产物 | 本轮选择性吸收 |
| `DEC-033` | 实施编排模式 | light 可直接执行；standard/full 默认 Coordinator 调度 Worker，独立 Verifier 验收；父子任务状态写入 state.json | 本轮选择性吸收 |
| `DEC-034` | 运行时证据 | 新增 E5 运行时证据，行为声明必须有 API/页面/日志/测试实际输出；静态代码检查不能替代运行时证据 | 本轮选择性吸收 |

### 8.1 约束与优先级登记

| 编号 | 类型 | 内容 |
|------|------|------|
| `CON-001` | 独立性 | 不依赖外部流程系统、状态服务、任务数据库或上报服务才能运行 |
| `CON-002` | 阶段控制 | 不得静默跳过阶段；精简必须以 `not_applicable` 和理由显式记录 |
| `CON-003` | 事实边界 | 代码关系索引只能导航，E1 事实必须回指源码或 LSP |
| `CON-004` | 变更控制 | 未审批 proposal 不得覆盖当前有效基线或被下游消费 |
| `CON-005` | 对象身份 | AskMe 完成后不得由后续命令重新推断或静默改变 `subject_type` |
| `PRI-001` | P0 | 先实现统一状态、路由、输出和恢复，再扩展自动化能力 |
| `PRI-002` | P0 | Project `foundation_ready` 和 Feature 独立验收是 MVP 必须具备的门禁 |
| `PRI-003` | P1 | UI、收敛检查和多角色评审按风险档位完整接入 |

## 9. 双文档追溯与同步约定

本文件是 `DEVFLOW-REQ` 需求与决策基线，概要设计文件是 `DEVFLOW-DESIGN`。两份文件共同构成 asdm-devflow 的设计基线，但事实不重复定义：本文件负责需求、缺口、约束和已确认决策；概要设计负责模块、流程、状态、契约和非功能设计。

### 9.1 统一编号

| 编号前缀 | 归属文档 | 含义 |
|----------|----------|------|
| `REQ-xxx` | 本文件 | 用户目标、范围和可交付需求 |
| `GAP-xxx` | 本文件 | 现有体系的能力缺口 |
| `DEC-xxx` | 本文件 | 已确认的方案决策（对应第 8 节决策记录编号） |
| `CON-xxx` | 本文件 | 不可违反的约束或边界 |
| `PRI-xxx` | 本文件 | 优先级和落地要求 |
| `DES-xxx` | 概要设计 | 总体架构或关键设计 |
| `MOD-xxx` | 概要设计 | 模块职责和依赖 |
| `FLOW-xxx` | 概要设计 | 生命周期、时序和状态流转 |
| `STATE-xxx` | 概要设计 | 状态模型和一致性规则 |
| `CONTRACT-xxx` | 概要设计 | 输入、输出和内部数据契约 |
| `NFR-xxx` | 概要设计 | 安全、可靠性、可维护性等非功能设计 |

需求条目必须记录对应的设计落点；概要设计条目必须记录需求依据。没有上游依据的设计内容必须标记为假设、技术补充或待确认，不得默认为已确认需求。

### 9.2 双向同步规则

1. 需求、决策、范围或优先级变化时，必须分析受影响的 `DES`、`MOD`、`FLOW`、`STATE` 和 `CONTRACT` 条目，并同步更新概要设计。
2. 架构、流程、状态或契约变化时，必须判断是否改变需求语义；若改变，先同步更新本文件中的 `REQ`/`DEC`，再更新概要设计。
3. 同一次变更使用同一个 `CR-xxx`，两份文件的修订记录、版本号、变更原因和影响范围必须一致。
4. 任一文件发现事实冲突时，状态改为 `conflict`，禁止继续向下游生成或消费设计，直到冲突被裁决并同步清除。
5. 两份文件不是全文镜像；同一事实只在其归属文档中定义一次，另一份文档通过编号和锚点引用。
6. 不引入外部上报服务。阶段结果、同步状态、审核证据和变更记录仅通过 JSON、Markdown、`state.json` 及本地执行记录承载。

### 9.3 当前同步基线

| 基线项 | 值 |
|--------|----|
| 需求文档 | `DEVFLOW-REQ` |
| 概要设计文档 | `DEVFLOW-DESIGN` |
| 同步状态 | `in_sync` |
| 最近变更 | `CR-003` |
| 当前需求版本 | `1.3` |
| 当前概要设计版本 | `3.1` |
| 外部上报范围 | 明确排除 |

概要设计文档必须在每次同步后更新本表对应信息；只有两份文档均为 `in_sync` 时，才能将概要设计交给后续详细设计或实现阶段继续消费。

## 10. 修订记录

| 日期 | 版本 | 变更 | 影响范围 |
|------|------|------|----------|
| 2026-08-25 | 1.3 | `CR-003`：补齐 Project/Feature 双对象需求，建立实际追溯编号，统一目录、状态投影和同步基线 | 需求基线、总体设计、AskMe 设计 |

## 11. 下游交付清单

下游必须完成：

1. 文件级 schema、命令提示词、错误码和模板；
2. 可加载的 `SKILL.md` 及七个命令参考文件；
3. 状态迁移、原子投影、证据和收敛检查的自动化测试；
4. 实现完成后的 design/impl review 证据。

需求变化必须使用第 9 节定义的 `CR-*` 同步协议。

## 12. 文档演进与拆分关系

本文件是本主题最初形成的完整大设计母稿。由于内容同时覆盖需求、总体架构、
AskMe、执行、评审、同步和 UI 等多个层级，后续维护按以下链路拆分：

```text
AskMe → Overall → Detail → 开发文档 / Skill 实现
```

- [asdm-devflow-skill-askme-design.md](asdm-devflow-skill-askme-design.md)：记录
  设计这个 Skill 时的需求澄清和决策确认；
- [asdm-devflow-skill-overall-design.md](asdm-devflow-skill-overall-design.md)：记录
  基于已确认决策形成的总体架构和生命周期；
- [asdm-devflow-skill-detail-design.md](asdm-devflow-skill-detail-design.md)：记录
  文件级 Schema、命令参考、模板、协议和测试设计；
- `.codebuddy/skills/asdm-devflow/`：消费 Detail 后形成的实际开发文档和实现。

母稿保留用于历史追溯和拆分完整性核对。拆分文档不得静默改变母稿中已确认的需求；
发现语义变化时，必须按第 9 节的 `CR-*` 规则同步。
