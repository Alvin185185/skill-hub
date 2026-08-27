# skill-hub

个人 Skill 源仓库，统一收纳、管理各类自研 Skill，支持快速加载与复用，沉淀可复用的自动化 / AI 能力单元。

## 目录结构

```text
skill-hub/
├── skills/                 # 已验证、可日常使用的 Skill 源码
├── drafts/                 # 开发中或待验证的 Skill
└── archive/                # 已废弃或被替代的历史版本
```

## 生命周期

新想法先放入 `drafts/`，完成基本验证后移动到 `skills/`。被替代的 Skill 移入 `archive/`，不要直接删除，以便追溯历史和恢复使用。

## Skill 目录约定

每个 Skill 使用一个独立目录，至少包含 `SKILL.md`，并在文件头声明 `name` 和 `description`。需要时可以在 Skill 目录内添加 `references/`、`scripts/`、`assets/` 或 `tests/`，保持 Skill 自包含、可复制和离线可用。

`skills/` 是正式发布源目录；面向 Cursor、Claude Code、CodeBuddy 或 ASDM 的安装包和生成文件属于派生物，不直接提交到这里。

## 当前状态

仓库目前处于初始化阶段，先专注于 Skill 源码的沉淀和复用。

## 文档校验

AskMe 设计稿提交前运行：

```bash
python3 scripts/check-askme-structure.py
python3 scripts/test-check-askme-structure.py
```

校验会阻止任何带 `.n` 的决策标题，并检查决策编号重复。说明性角色、成功标准、非目标和能力清单不单独编号；真正独立的问题必须使用同级连续编号。GitHub Actions 会在 push 和 Pull Request 时自动运行检查和回归测试。

GitHub Actions 不能阻止本地 `git commit`。要阻止直接合并到 `main`，必须在 GitHub 分支保护规则中将 `askme-structure` 检查设为必需状态并禁止直接推送；本地提交前拦截则需另行安装 pre-commit hook。

启用本地提交前检查：

```bash
pre-commit install
```
