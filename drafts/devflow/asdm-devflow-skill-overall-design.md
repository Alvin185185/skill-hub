# asdm-devflow Skill 总体设计

> 状态：已完成（总体设计基线），待详细设计与实现
> 日期：2026-08-31
> 文档角色：Skill 的完整总体设计（DEVFLOW-DESIGN）
> 需求基线：[asdm-devflow-skill-design.md](asdm-devflow-skill-design.md)
> AskMe 设计：[asdm-devflow-skill-askme-design.md](asdm-devflow-skill-askme-design.md)
> 详细设计：[asdm-devflow-skill-detail-design.md](asdm-devflow-skill-detail-design.md)
> 追溯状态：`in_sync`
> 设计版本：`3.2`
> 对应需求版本：`1.3`
> 最近同步变更：`CR-003`

## 1. 这是什么 Skill

`asdm-devflow` 是一个面向 Project 和 Feature 的 AI 研发工作流 Skill。它既能把
一个完整产品想法推进到可运行的 MVP，也能在现有 Project 基线上把单项 Feature
推进到可验证交付，过程中持续保存文档、状态、证据和变更记录。

它不是一个只会生成 Markdown 的写作助手，也不是把几个命令串起来的菜单。
它要解决的是 AI 开发过程中常见的四类断点：

1. 需求被拆解后，没有可靠的实施和验证闭环；
2. 上游文档改变后，下游设计、任务和实现仍然使用旧内容；
3. 文档看起来完整，却没有事实证据和独立验收；
4. 多阶段工作跨会话继续时，AI 不知道当前真实状态；
5. 空仓库或新产品只有想法，没有建立工程基线和编排 MVP Feature 的流程。

因此，Skill 的核心不是某一个命令，而是“文档事实 + 机器状态 + 证据链”
共同驱动的一条统一研发流水线。需求基线中的目标和八个缺口见
`asdm-devflow-skill-design.md` §1。

## 2. 用户最终会怎样使用它

用户可以从完整 Project 或单项 Feature 进入同一条七命令链。

Project 路径如下：

```text
“从空仓库创建一个客户支持系统”
          ↓
AskMe / Overall / Detailed / Breakdown
          ↓
Execute：建立仓库、构建、运行时和安全工程基线
          ↓
Review：达到 foundation_ready
          ↓
按 MVP 清单创建并编排 Feature
          ↓
Project Review：端到端验收，达到 mvp_ready
```

Feature 路径如下：

```text
“我想增加批量导出”
          ↓
AskMe：澄清目标、范围、边界和验收标准
          ↓
Overall：形成场景、页面清单和总体方案
          ↓
Detailed：调查代码，冻结事实，写技术和 UI 设计
          ↓
Breakdown：把设计切成可独立验证的纵向任务
          ↓
Execute：Worker 实施，构建并运行验证，Verifier 独立验收
          ↓
Review：检查设计质量、实现符合性和证据真实性
          ↓
完成，或通过 Sync 处理新的变化
```

用户在任何阶段都可以离开。下一次输入“继续 PJ-xxx”或“继续 FT-xxx”时，Skill
先通过 `.devflow/work-items.json` 定位对象状态，再读取 `subject_type`、阶段、未完成
任务、父子依赖、过期项和待处理变更，从正确断点恢复，而不是重新猜测对象和阶段。

## 3. 能力地图

### 3.1 七个用户命令

| 命令 | Project 分支 | Feature 分支 |
|------|--------------|--------------|
| `askme` | 确认项目目标、MVP、用户和产品/运行约束 | 确认特性范围、行为、边界和验收 |
| `overall` | 形成模块、核心流程、总体架构和 MVP 地图 | 形成场景、页面范围和受影响模块 |
| `detailed` | 设计技术栈、仓库结构、工程基线和 MVP 技术边界 | 基于父 Project 和现有代码完成特性设计 |
| `breakdown` | 产生工程基础任务和 MVP Feature 清单 | 产生可独立验证的纵向任务 |
| `execute` | 建立工程基线并编排 MVP Feature 链 | 实施一个任务并取得运行时证据 |
| `review` | 判定 `foundation_ready` 或 `mvp_ready` | 判定设计或实现是否可靠 |
| `sync` | 向子 Feature 传播项目级变化 | 反查父 Project 并传播特性变化 |

### 3.2 七个命令之外的共享能力

| 共享能力 | 解决的问题 | 谁使用 |
| ---------- | ------------ | --------- |
| 项目配置 | Skill 如何知道文档、仓库、运行时在哪里 | 所有命令 |
| 状态管理 | 跨会话恢复和阶段门禁如何可靠 | 所有命令 |
| 产物管理 | 文档、索引、变更和执行记录如何落盘 | 所有命令 |
| 代码智能 | 如何定位调用、依赖和测试关系 | Detailed、Sync、Review |
| 证据管理 | 如何证明文档中的事实和行为 | Detailed、Execute、Review |
| Agent 编排 | 如何隔离实施者和验收者的判断 | Execute、Review |
| 运行时验证 | 如何启动环境并取得真实行为证据 | Execute、Review |
| UI 能力 | 如何引用设计约束、生成 SVG 并验证真实页面 | Overall、Detailed、Execute、Review |
| 收敛检查 | 如何发现缺失、矛盾和计划外实现 | Review、Sync |

## 4. 总体架构

### 4.1 分层

```text
用户意图和阶段命令
          ↓
调度层：SKILL.md
  识别意图、读取状态、选择命令、加载上下文
          ↓
命令层：七个 command 文件
  定义当前阶段的目标、步骤、输入、输出和门禁
          ↓
共享能力层
  配置 / 状态 / 产物 / 证据 / 代码智能 / Agent / 运行时 / UI
          ↓
底层工具
  文件系统、搜索、LSP、构建工具、浏览器和测试工具
```

调度层负责“现在应该做什么”，命令层负责“这一阶段怎么做”，共享能力层
负责“如何可靠地完成并留下证据”。这三层不能互相越权。

### 4.2 依赖方向

Project 和 Feature 都遵循相同的阶段依赖方向：

```text
AskMe → Overall → Detailed → Plan → 实现与验证
                                      ↑       ↓
                                      └─ Review
```

变更不沿着主流程静默向前覆盖，而是走：

```text
任意节点 → Sync 提案 → 影响分析 → 用户确认 → 更新受影响节点 → 复检
```

未审批的 proposal、过期的上游产物和冲突状态都不能被下游命令消费。

Project 还具有父子编排依赖：

```text
Project Plan 基础任务 → Project foundation_ready
                              ↓
                    MVP Feature 子对象链
                              ↓
                 Project 端到端 Review → mvp_ready
```

Feature 默认要求父 Project 已达到 `foundation_ready`。父 Project 的架构、认证、
数据或运行时基线发生变化时，Sync 必须检查相关 Feature 并按影响标记 `stale`。

### 4.3 独立性边界

Skill 独立维护自己的状态、代码关系索引、Agent 编排和运行时验证协议。
它不依赖外部编排、本体、任务数据库或上报服务。项目原有工具可以被探测和调用，
但工具不可用时必须明确降低 assurance，而不是假装已完成。

### 4.4 设计条目登记

| 编号 | 设计条目 | 需求依据 |
|------|----------|----------|
| `DES-001` | 统一工作对象模型和身份路由 | `REQ-001`、`DEC-005`、`DEC-026` |
| `DES-002` | Project/Feature 共用七命令和共享能力层 | `REQ-002`、`DEC-001`、`DEC-002` |
| `MOD-002` | 七个命令模块按 `subject_type` 选择分支 | `REQ-002` |
| `MOD-004` | 证据管理和可回源核查模块 | `REQ-005`、`DEC-011`、`DEC-034` |
| `MOD-005` | Coordinator/Worker/Verifier 编排模块 | `REQ-006`、`DEC-009`、`DEC-033` |
| `MOD-006` | 跨阶段 UI 设计与验证模块 | `REQ-007`、`DEC-014`、`DEC-015` |
| `MOD-007` | Review/Sync 收敛检查模块 | `REQ-010`、`DEC-028` |
| `FLOW-001` | 工作对象识别、绑定和恢复流程 | `REQ-001`、`CON-005` |
| `FLOW-002` | 七阶段主流程 | `REQ-002` |
| `FLOW-003` | 状态更新、投影和故障恢复流程 | `REQ-003` |
| `FLOW-004` | proposal→impact→确认→传播→归档流程 | `REQ-004` |
| `FLOW-005` | Worker 实施和 Verifier 独立验收流程 | `REQ-006` |
| `FLOW-006` | UI 决策→效果图→实现→浏览器验证流程 | `REQ-007` |
| `FLOW-007` | Project 基础任务→Feature 编排→MVP 验收流程 | `REQ-008` |
| `FLOW-008` | 风险识别、选档和只升不降流程 | `REQ-009` |
| `STATE-001` | 对象阶段、依赖、任务、版本和 stale 状态 | `REQ-003` |
| `STATE-002` | 当前基线与待审批变更状态分离 | `REQ-004` |
| `STATE-003` | `foundation_ready`、Feature 汇总和 `mvp_ready` 状态 | `REQ-008` |
| `CONTRACT-001` | 统一对象身份和命令输出契约 | `REQ-001` |
| `CONTRACT-002` | `operation_id` 和投影同步契约 | `REQ-003` |
| `NFR-001` | 关键事实和行为声明必须可回源 | `REQ-005`、`CON-003` |
| `NFR-002` | 风险档位控制流程深度和核查覆盖率 | `REQ-009` |
| `NFR-003` | error 未清零不得宣称设计或实现完成 | `REQ-010` |

## 5. 文档和状态如何共同工作

### 5.1 文档链

对象状态与人类文档分开存放，唯一目录规范如下：

```text
.devflow/
├── config.md
├── work-items.json
├── project-state.json
└── features/FT-{id}/state.json

{docs_root}/
├── INDEX.md
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
    ├── mockup-{page}.svg
    ├── style-tokens.json       # 现有系统扫描快照，不是第二份人工设计源
    └── changes/
```

不是每个对象都需要所有文件。`light` 档可以显式标记某个阶段
`not_applicable`，但不能静默跳过验收或验证义务。

### 5.2 谁是事实来源

- Project 的 `.devflow/project-state.json` 和 Feature 自己的 `state.json` 是机器状态、阶段、依赖和过期信息的唯一权威来源。
- `.devflow/work-items.json` 只负责从 `subject_id` 定位对象状态，不保存阶段事实。
- 已批准的 Markdown 是人类可读事实和证据的载体。
- INDEX 是由状态投影生成的人类索引，不是独立事实来源。
- `changes/` 中的 proposal 在确认前只是候选变更。
- 代码关系索引只用于导航和影响分析，源码本身才是代码事实来源。

### 5.3 状态写入顺序

所有命令共享同一投影协议：

```text
生成 operation_id
  → 校验状态与全部投影
  → 原子写入 projection_status=pending 的对象状态
  → 更新 INDEX 和 Markdown
  → 原子写入 projection_status=in_sync
```

中间一步失败时，命令停止向下游推进，保留 `operation_id`、失败投影和重放信息，
并记录 `state_sync_error`。恢复时必须先完成或回滚 pending 操作。

## 6. 生命周期和阶段门禁

### 6.1 状态流转

Project 生命周期：

```text
clarifying → designed → detailed → planned_for_dev
  → executing_foundation → foundation_review → foundation_ready
  → orchestrating_features → mvp_review → mvp_ready
```

Feature 生命周期：

```text
clarifying → designed → detailed → planned_for_dev
  → executing → verifying → reviewing → implemented
```

任何阶段都可能进入 `blocked`、`stale` 或 `conflict`。这些状态必须优先处理，
不能通过“继续”命令绕过。

Project 与 Feature 的父子状态规则如下：

- 父 Project 未达到 `foundation_ready` 时，Feature 可以规划，但默认不得进入 Execute；
- Project 的技术栈、认证、数据、公共契约或运行时基线变化时，受影响 Feature 标记 `stale`；
- Feature 发现项目级基础能力缺口时，创建 Project proposal，不在 Feature 内静默绕过；
- Project 的 `mvp_ready` 必须由全部必需 MVP Feature 通过 impl review 和项目级端到端验收共同决定。

### 6.2 阶段门禁

| 命令 | 通用门禁 | Project 成功条件 | Feature 成功条件 |
|------|----------|-----------------|-----------------|
| AskMe | 对象可识别或可分配 | 项目决策、MVP 范围和项目验收可判定 | 特性决策和验收可判定 |
| Overall | AskMe 已完成 | 模块、核心流程、架构边界和 MVP 地图明确 | 场景、范围、页面和受影响模块明确 |
| Detailed | Overall 已完成 | greenfield/存量调研冻结，工程基线设计完成 | 代码调研冻结，技术设计和 DoD 完成 |
| Breakdown | Detailed 通过 design review | 基础任务、MVP Feature 清单和依赖完整 | 任务、验证和追溯完整 |
| Execute | Plan 有可执行任务 | 基础任务通过后达到 `foundation_ready`，再编排 Feature | 实施、验证和 Verifier 通过 |
| Review | 对应产物或实现存在 | 判定 `foundation_ready` 或最终 `mvp_ready` | error 清零，warning 有结论 |
| Sync | 存在变化、错误或过期 | 传播到受影响 Feature | 必要时反查并更新 Project proposal |

门禁检查应返回缺失项和补救动作，而不是只返回一个“前置条件不满足”。

## 7. 七个命令的完整行为

### 7.1 AskMe：把想法变成决策

AskMe 的完整设计见
[asdm-devflow-skill-askme-design.md](asdm-devflow-skill-askme-design.md)。

它负责：

1. 识别新 Project/Feature 或恢复已有对象；
2. 通过 work-items 读取配置、INDEX 和对象状态；
3. 用 L0 代码确认减少无效问题；
4. 分批展示决策点、选项和推荐；
5. 记录用户选择、理由和验收标准；
6. 每轮落盘并支持恢复；
7. 所有必需决策完成后进入 Overall。

Project 分支确认目标用户、MVP/非目标、核心能力、端形态、数据和权限、部署运维、
安全与项目级验收；Feature 分支确认单项能力的范围、正常/异常/边界行为、依赖和验收。
AskMe 不决定组件、API、数据库或任务拆分。

### 7.2 Overall：让人看懂要做什么

Overall 是第一份完整的方案说明。它不是 Detailed 的缩写，也不是把 AskMe
原文复制一遍。它要把已确认的需求组织成一个人能审阅的总体方案。

Overall 至少回答：

- 谁在什么场景下使用这项能力；
- 用户从哪里进入，经过哪些步骤完成目标；
- 哪些页面、模块或外部系统会受到影响；
- 现有代码和资产中哪些可以复用；
- 方案的范围、非目标、依赖和主要风险是什么；
- 哪些问题必须留给 Detailed 决定。

Project 分支还必须给出产品模块地图、端到端核心流程、客户端/服务端/数据/基础设施
边界、仓库组织和可追溯的 MVP Feature 清单。Feature 分支必须说明与父 Project
总体设计的关系，不得引入与父基线冲突的新架构事实。

Overall 的流程是：

1. 检查 AskMe 已完成且没有 stale/conflict；
2. 读取决策点、验收标准和范围边界；
3. 做 L1 调研，识别现有架构、页面和设计资产；
4. 编写总体概述、用户场景、页面清单和现有资产；
5. 进行产品、架构和 UX 视角的设计评审；
6. 通过门禁后更新 INDEX 和状态，进入 Detailed。

涉及 UI 时，Overall 需要说明页面职责和用户路径，但不定义具体组件树、
API 字段或 CSS 实现。

### 7.3 Detailed：把总体方案落到代码事实

Detailed 分成两个阶段，原因是“调查事实”和“基于事实做设计”不能混在一起。

Project greenfield 分支没有业务代码时，调研冻结的是仓库现状、可用工具和组织约束，
随后设计技术栈、仓库/包结构、认证授权、基础数据、构建测试、部署运行和最小可运行
工程基线；缺少存量代码不是失败。Feature 分支则以父 Project 基线和现有代码为约束。

#### 阶段一：代码调研冻结

Skill 确认代码库范围，建立或刷新可回源的代码关系索引，并由 code-explorer
扫描接口、数据模型、部署方式、测试和 UI 资产。每个代码库生成一份
`CodeResearch-{repo}.md`，关键发现附文件和行号。

#### 阶段二：详细设计

在调研文件齐备后，生成：

- 技术方案、模块和数据流；
- API 契约和数据模型；
- 前端路由、组件树、状态管理和交互；
- UI 设计、字段到 API 对照、空错载态和效果图；
- DoD、假设清单和需求到实现的追溯矩阵。

Detailed 不能把代码索引结果直接当成事实，所有关键声明必须回源源码或 LSP。

### 7.4 Breakdown：把设计切成可验证任务

Breakdown 不重新设计功能，而是扫描 Detailed 的全部章节，按语义找到变更范围、
技术方案、UI、API、DoD 和约束，然后切成纵向切片任务。

Project Breakdown 必须分为两组：第一组是建立工程基线的基础任务；第二组是带依赖、
进入条件和项目级验收贡献的 MVP Feature 清单。Feature Breakdown 仍按端到端用户能力
切片，不能按前端/后端/测试简单横切。

一个任务应该：

- 是用户可感知的端到端能力；
- 有明确交付物；
- 可以独立验证；
- 通常需要 1 到 3 天；
- 包含正常、异常、边界和安全验证；
- 涉及 UI 时包含截图、可访问性和交互路径验证。

任务按依赖分 Phase，而不是简单按前端、后端、测试横向切开。

### 7.5 Execute：实施和独立验收

Execute 消费一个 Plan 任务，完成一次实施闭环：

```text
读取任务和设计证据
      ↓
Coordinator 裁剪上下文
      ↓
Worker 实施并记录输出
      ↓
构建、启动和执行验证步骤
      ↓
独立 Verifier 重跑并判定 pass/fail
      ↓
记录偏差，进入 impl review 或返工
```

Worker 不能关闭任务，不能修改验收预期。Verifier 只拿到设计中的 DoD、验证步骤、
代码和必要环境，不使用 Worker 的自评结论。

验证失败时记录“现象、证据、假设、修复、重建、再次验证”。同一问题最多自动
尝试三轮，仍失败则标记阻塞并停止后续任务。

Project Execute 先实施基础任务；基础任务经 Project Review 达到 `foundation_ready`
后，Coordinator 才按 MVP 清单创建或恢复子 Feature。它不能把所有 MVP 业务实现塞进
一个 Project 任务。Feature Execute 只实施当前 Feature 的一个可验证任务。

### 7.6 Review：检查设计和实现是否可靠

Review 有两个模式：

#### design review

检查文档结构、链接、事实证据、需求覆盖、技术可行性、DoD 可测性、UI 完整性、
多角色意见和跨制品收敛。

#### impl review

检查设计与实现的双向偏差、代码质量、安全、契约、测试、运行时结果、UI 一致性，
并由独立验收角色抽查 Execute 的结论。

Review 只能报告问题或创建 follow-up，不能绕过 Sync 直接改变需求语义。

Project 的 design review 检查总体架构、工程基线和 MVP 地图；基础任务完成后的 impl
review 判定 `foundation_ready`；全部必需 Feature 完成后，再以项目级核心路径、运行、
安全和验收标准判定 `mvp_ready`。Feature review 判定单项设计或实现是否通过。

### 7.7 Sync：有控制地传播变化

Sync 有两种入口：

- **变更模式**：用户明确给出旧值、新值和原因；
- **修正模式**：用户指出“这里不对”，Skill 先沿追溯链定位根因。

两种模式都必须经历：

```text
创建 CR proposal
      ↓
影响分析
      ↓
用户确认影响清单
      ↓
更新受影响文档、任务和实现
      ↓
追溯与收敛复检
      ↓
归档 proposal/impact
```

确认前不能修改当前有效基线。若只是技术优化且不改变需求语义，也要记录无语义
变化的依据。

Project 级技术栈、认证、数据、公共契约和运行时变化必须检查全部相关子 Feature；
Feature 暴露出的基础能力缺口必须反向创建 Project proposal。父子传播结果都写入同一
CR 的 impact 清单，不能只修一个对象而遗漏另一层。

## 8. 共享能力的实现逻辑

### 8.1 项目配置

Skill 本体不能硬编码某个项目的工作项系统、模块编号或路径。启动时读取
`.devflow/config.md`，配置至少包括：

- Project/Feature 编号模式和追踪链接模板；
- 文档根目录和 INDEX 路径；
- 模块、仓库和构建命令；
- 运行时启动、健康检查和日志位置；
- code-index 存储和刷新策略；
- `light/standard/full` 工作流档位。

缺少配置时使用默认值；需要项目特有信息才能继续时询问用户并记录假设。

### 8.2 代码关系索引

索引帮助 Skill 快速找到调用方、被调用方、继承关系、依赖和测试，但不替代源码。
每次索引记录对应 commit、扫描范围、构建时间和错误。查询结果必须能回指文件和
行号；无法回源的结果只能标记为待核实。

### 8.3 证据链

文档中的声明按证据等级管理：

| 等级 | 证明什么 | 例子 |
| ------ | ---------- | ------ |
| E1 | 代码、接口、配置确实存在 | 文件、符号、行号 |
| E2 | 需求或调研结论已确认 | 决策点、CodeResearch 发现 |
| E3 | UI 效果图和风格 token 一致 | SVG 字段和 token |
| E4 | 页面字段与 API 契约一致 | 双向字段对照表 |
| E5 | 行为真实发生且符合断言 | API、页面、日志、测试输出 |
| A1 | 尚未确认的显式假设 | “执行时确认端口” |

没有证据又没有标记为假设的内容属于隐性编造，Review 必须报错。

### 8.4 Agent 编排

标准和完整档位使用三种角色：

- Coordinator：识别阶段、裁剪上下文、管理父子任务和汇总结果；
- Worker：实施一个边界明确的任务；
- Verifier：独立重跑验证并返回结构化结论。

角色之间需要隔离上下文。每个运行记录 `parent_task_id`、输入快照、输出产物、
状态和失败原因，使会话中断后可以恢复。

### 8.5 运行时验证

涉及行为的声明不能只靠静态代码判断。Skill 根据 `runtime` 配置启动或重建进程，
执行健康检查、API/页面操作、日志收集和证据保存。验证记录必须包含：

- 使用的命令和环境；
- 预期断言；
- 实际输出；
- 日志、截图或响应位置；
- 重试和清理结果。

### 8.6 UI 能力

UI 能力贯穿 Overall、Detailed、Execute 和 Review：

1. Overall 说明页面职责和用户路径；
2. Detailed 生成 UI 设计、组件清单、状态机、字段对照和 SVG 效果图；
3. Execute 用 Playwright 验证实际渲染、交互、响应式和可访问性；
4. Review 独立比较实现截图和效果图，检查跨页面一致性。

SVG 是可追踪的文本设计产物，但 SVG 文本检查不能代替浏览器验证。

## 9. 评审和收敛

### 9.1 多角色评审

设计评审按阶段组合角色：

- AskMe：产品和架构视角；
- Overall：产品、架构和 UX；
- Detailed：产品、架构、开发、测试，涉及 UI 时加前端专家；
- Breakdown：开发和测试，涉及 UI 时加前端专家。

实现评审包括设计符合性、代码质量、验收、运行时和 UI 符合性角色。每个角色
独立阅读输入并引用具体位置，父 Agent 只汇总意见和分歧。

### 9.2 收敛检查

Review 和 Sync 都要比较：

```text
AskMe → Overall → Detailed → Plan → 代码/测试/运行时证据
```

检查六类问题：

1. 上游要求没有下游设计或验证；
2. 只覆盖正常路径，遗漏错误、权限或边界；
3. 同一字段、状态、接口或数值互相矛盾；
4. 代码存在但没有批准的需求、设计或偏差来源；
5. 下游引用旧版本，已经 stale；
6. 关系索引无法回源或行为缺少 E5 证据。

每项问题都输出来源、目标、状态、证据和处置动作。

## 10. 完整系统示例

### 10.1 从空仓库创建 Project

假设用户提出“创建一个内部客户支持系统”：

1. AskMe 将对象识别为 `PJ-001`，确认目标用户、MVP 能力、部署约束、权限、安全和项目级验收。
2. Overall 形成工单、知识库、用户与权限模块地图，并把三个 MVP Feature 追溯到项目决策。
3. Detailed 记录空仓库和可用工具事实，设计仓库结构、技术栈、认证、数据、构建、测试和部署基线。
4. Breakdown 先生成工程基础任务，再生成带依赖的 `FT-001` 至 `FT-003` MVP 清单。
5. Execute 完成工程基础任务，Project Review 实际构建、启动和健康检查后标记 `foundation_ready`。
6. Coordinator 逐个创建或恢复 MVP Feature，并让每个 Feature 复用同一七命令链。
7. 全部必需 Feature 的 impl review 通过后，Project Review 执行端到端核心路径，最终判定 `mvp_ready`。

### 10.2 在现有 Project 中交付 Feature

假设用户要“给用户列表增加批量导出”：

1. AskMe 确认管理员权限、字段范围、数量上限、同步/异步方式和手机端行为。
2. Overall 形成“管理员从用户列表筛选用户、提交导出、查看结果”的场景，
   列出用户列表页、导出任务页和下载结果的页面职责。
3. Detailed 调查现有列表接口、权限中间件、任务队列和下载存储，决定复用哪些
   模块、增加哪些接口，并写出错误状态和 DoD。
4. Breakdown 将能力切成“提交导出任务”“查看任务状态”“下载结果”三个纵向任务，
   每个任务都有 API、前端、权限和验证步骤。
5. Execute 由 Worker 实施第一个任务，启动服务并实际调用接口；Verifier 在不知道
   Worker 自评的情况下重跑权限和正常路径验证。
6. Review 检查实现是否覆盖 D1 的权限决策，运行时是否真的生成文件，页面是否符合
   UI 设计。
7. 用户后来把上限从 10,000 改成 50,000，Sync 创建 CR，分析任务队列、超时、
   验证步骤和已完成代码的影响，确认后才同步。

两个例子说明：七个命令不是七份互不相关的文档，而是同一个对象的事实逐阶段变得
更具体、更可执行、更有证据；Project 还负责工程基线和子 Feature 的生命周期编排。

## 11. 工作流档位

### `light`

适用于局部文案、配置和低风险小修复。可以合并 AskMe 问题、标记 Overall
`not_applicable` 或使用精简模板，但必须保留验收、代码证据、验证命令和实现评审。

### `standard`

适用于普通业务特性。使用完整文档链、追溯矩阵、设计评审、Worker/Verifier 和
实现评审，是无法判断风险时的默认档位。

### `full`

适用于安全、权限、数据迁移、外部契约、支付、合规、生产基础设施和不可逆变化。
关键声明全量核查，必须有回滚、独立验收、全角色评审和完整收敛检查。

## 12. 生成 Skill 时的实现边界

### 12.1 Overall 和 AskMe 必须定义的内容

- 用户体验和阶段目的；
- 每个命令的能力、输入、输出和主要流程；
- 阶段门禁和状态转换；
- 共享能力什么时候被调用；
- 异常、冲突、过期和恢复行为；
- 文档、状态和证据如何协作；
- 典型场景和验收方式。

### 12.2 Detail 才定义的内容

后续 `asdm-devflow-skill-detail-design.md` 可以进一步规定：

- `SKILL.md` 和各 `command-*.md` 的具体章节；
- `state.json` 的字段级 Schema；
- 统一 JSON 的完整字段和错误码；
- 模板正文和提示词组织；
- 代码索引、运行时验证和 Agent 记录的具体格式；
- 打包、加载和自动化测试用例。

Detail 可以细化实现，但不能首次发明 AskMe/Overall 中没有的核心能力或阶段逻辑。

### 12.3 AskMe、Overall 与 Detail 的边界

AskMe 只确认会改变 Skill 目标、范围、流程、外部契约或质量门禁的设计决策，并规定如何根据事实、风险和未知项动态生成运行时决策。AskMe 不维护固定的项目问题清单，也不登记跨阶段的“延迟确认项”。

Overall 承接已确认的阶段能力、命令边界、阶段门禁、共享能力路由和架构级约束，包括 Skill 的命名、安装范围和总体目录边界。Detail 承接文件级实现，包括模板章节和锚点、Markdown/Schema 规则、统一错误码、style token、代码索引和路由识别、索引刷新、运行时验证、迁移字段映射、脚本和自动化测试。

如果某项会改变 AskMe 的范围、流程或契约，必须返回 AskMe 创建正式决策；如果只决定 Overall 的架构或 Detail 的文件级实现，则在对应阶段确认，不得以 AskMe 中的待确认列表替代阶段门禁。

## 13. 设计取舍

### 为什么状态和 Markdown 分开

Markdown 适合人读和评审，JSON 适合机器判断阶段、依赖和过期。让其中一个同时
承担两种职责，会导致状态难以恢复或文档难以理解。

### 为什么变更需要 proposal

直接覆盖已批准文档会让 AI 无法判断下游是否仍然有效。proposal/impact 把“建议改变
什么”和“当前已经是什么”分开，用户确认后才合并。

### 为什么需要独立 Verifier

实现者自己写代码、自己选择预期、自己宣布通过，会形成自评闭环。Verifier 只接收
验收预期和实际代码，才能提供基本的独立性。

### 为什么 Detailed 需要冻结调研

动态扫描和设计决策混在同一会话中，容易因为上下文变化或遗漏而产生幻觉。先冻结
带证据的代码调研，再基于它设计，能让后续决策可回查。

## 14. 总体设计完成标准

阅读本文件和 AskMe 设计后，人应该能说清楚：

- 这个 Skill 解决什么问题；
- 七个命令分别做什么；
- 一个 Project 如何从想法走到 `foundation_ready` 和 `mvp_ready`；
- 一个 Feature 如何在父 Project 基线上从需求走到交付；
- 中断、失败、变更和冲突如何处理；
- 哪些能力是共享的，何时被调用；
- 哪些内容属于 Overall/Detailed，哪些属于文件级实现。

生成 Skill 的 AI 还必须据此完成：

- 调度和恢复逻辑；
- 七个命令的门禁、输入、输出和错误处理；
- 状态、产物、证据和变更的持久化；
- Worker/Verifier、Review、Sync 和 UI 验证的能力接入；
- Markdown、链接、Schema、打包和加载检查。

## 15. 修订记录

| 日期 | 版本 | 变更说明 |
| ------ | ------ | ---------- |
| 2026-08-25 | 3.0 | 从生成约束摘要改为面向人和 AI 的完整总体设计，补充能力、流程、状态、异常和示例 |
| 2026-08-25 | 3.1 | `CR-003`：补齐 Project/Feature 双分支、父子生命周期、统一目录、状态投影协议和双向追溯 |
| 2026-08-31 | 3.2 | 明确 AskMe 动态决策生成与 Overall/Detail 的阶段边界，移除延迟确认项作为 AskMe 交接产物 |

## 16. Detail 入口条件

进入 Detail 前，必须已经确定能力地图、分层架构、Project/Feature 生命周期、
七个命令、共享能力、状态边界和评审/收敛机制。

## 17. 向 Detail 交接

进入 [asdm-devflow-skill-detail-design.md](asdm-devflow-skill-detail-design.md)，
将模块、流程、状态、契约和非功能要求转成文件级 Schema、命令参考、模板、脚本
接口和测试用例；Detail 定稿后再生成 `.codebuddy/skills/asdm-devflow/` 的开发文档。
