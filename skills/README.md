# 正式 Skill

这里存放已经过基本验证、可以日常复用的 Skill。每个子目录对应一个独立 Skill，目录名使用稳定的 kebab-case 标识。

建议的最小结构：

```text
<skill-id>/
└── SKILL.md
```

复杂 Skill 可以按需增加 `references/`、`scripts/`、`assets/` 和 `tests/`。Skill 应尽量自包含，不依赖本机绝对路径或未声明的外部文件。
