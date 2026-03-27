# Self-Improvement 持续学习机制

> 通过"记录 → 沉淀 → 升级"循环，让 AI 团队持续学习和进化

## 核心概念

### 记录时机

| 场景 | 记录到 |
|------|--------|
| 用户纠正 (如"不对，应该这样做") | `.learnings/LEARNINGS.md` |
| 命令/操作失败 | `.learnings/ERRORS.md` |
| 用户想要缺失功能 | `.learnings/FEATURE_REQUESTS.md` |
| 发现自己的知识错误 | `.learnings/LEARNINGS.md` |
| 发现更好的方法 | `.learnings/LEARNINGS.md` |

### 记录格式

```markdown
## [LRN-YYYYMMDD-XXX] 分类

**Logged**: ISO-8601 时间戳
**Priority**: low | medium | high | critical
**Status**: pending | resolved | resolved-upgraded
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述

### Details
完整上下文

### Suggested Action
具体修复方案

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file
- Tags: tag1, tag2
```

### 升级规则

| 学习类型 | 升级目标 |
|---------|---------|
| 行为模式 | `SOUL.md` |
| 工作流改进 | `AGENTS.md` |
| 工具使用技巧 | `TOOLS.md` |
| 配置错误 | `TOOLS.md` |

## 定期回顾

### 频率
建议每 2 天回顾一次

### 回顾清单
- [ ] 检查 `.learnings/` 是否有新记录
- [ ] 识别可升级的模式
- [ ] 执行升级并更新状态为 "resolved-upgraded"

## 示例

### 原始记录
```markdown
## [LRN-20260327-001] session-context

**Logged**: 2026-03-27T09:30:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
API timeout 切换模型导致上下文丢失

### Suggested Action
创建 session-context.md 存储会话状态
```

### 升级后
状态更新为 `resolved-upgraded`，内容合并到 `TOOLS.md`

## 目录结构

```
~/.openclaw/workspace/
├── .learnings/
│   ├── LEARNINGS.md    # 一般学习
│   ├── ERRORS.md       # 错误记录
│   └── FEATURE_REQUESTS.md  # 功能请求
├── SOUL.md             # 行为模式（升级目标）
├── AGENTS.md           # 工作流（升级目标）
└── TOOLS.md            # 工具技巧（升级目标）
```