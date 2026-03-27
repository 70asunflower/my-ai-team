# 共享协作空间

> 为多 Agent 团队创建共享的文件存储空间，便于协作和文件流转

## 背景

当团队有多个 Agent 时，每个 Agent 都有自己独立的 workspace。但有些文件需要跨 Agent 共享和协作：
- 正式报告
- 团队配置
- 模板资源

## 解决方案

创建共享协作空间 `~/.openclaw/shared/`

## 目录结构

```
~/.openclaw/shared/
├── README.md              # 使用说明
├── documents/            # 正式文档
│   ├── meeting/          # 会议记录
│   └── planning/         # 规划文档
├── reports/              # 报告
│   ├── daily/           # 日报 (按日期子目录)
│   ├── weekly/         # 周报
│   └── research/       # 研究报告
├── configs/              # 共享配置
│   ├── agents/          # Agent 公共配置
│   └── templates/      # 配置模板
├── resources/            # 资源/参考
│   ├── templates/       # 文档模板
│   └── references/     # 参考资料
└── archive/              # 归档
    └── YYYY/           # 按年份归档
```

## 使用规范

### 1. 文件命名
```
<日期>_<类型>_<描述>.md
例如：2026-03-27_daily_团队日报.md
```

### 2. 协作规则
- 跨 Agent 协作的文件存 `shared/`
- 各 Agent 私有文件存各自 workspace
- 报告按时间归档

### 3. 访问路径
```bash
# 所有 Agent 可通过绝对路径访问
~/.openclaw/shared/reports/daily/2026-03-27_团队日报.md

# 或通过环境变量
$OPENCLAW_STATE_DIR/shared/
```

## 示例

### 团队日报流程

1. **CEO** 创建日报模板 → `shared/documents/templates/daily-report.md`
2. **Assistant** 填写当日内容 → `shared/reports/daily/2026-03-27.md`
3. **Reviewer** 审核 → 评论区反馈
4. **CEO** 汇总 → 推送给用户

## 与各 Agent Workspace 的关系

```
┌─────────────────────────────────────────────────────┐
│                   ~/.openclaw/shared/                │
│  (所有 Agent 可访问 - 协作文件)                      │
└─────────────────────────────────────────────────────┘
         ↑                    ↑                    ↑
    ┌────────┐          ┌────────┐          ┌────────┐
    │ Agent1 │          │ Agent2 │          │ Agent3 │
    │workspace│          │workspace│          │workspace│
    │(私有)   │          │(私有)   │          │(私有)   │
    └────────┘          └────────┘          └────────┘
```

- **私有文件**: 每个 Agent 的 workspace
- **协作文件**: 共享空间 shared/
- **只读参考**: 共享空间 resources/