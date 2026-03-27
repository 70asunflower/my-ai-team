# Session Context 机制

> 当 API timeout 导致切换备用模型时，确保新模型能快速恢复上下文

## 问题

当 API request timeout 导致切换备用模型时，新模型没有完整上下文，造成：
- "乱来"行为
- 忘记之前的对话
- 信息不记得

## 解决方案

创建 `session-context.md` 存储实时会话状态。

### 文件位置
```
~/.openclaw/workspace-<agent>/memory/session-context.md
```

### 文件模板
```markdown
# Session Context - 当前会话状态

> 自动更新于: {timestamp}
> 此文件在每次任务完成时自动更新，API timeout 切换模型时会自动读取

---

## 🎯 当前任务
- [ ] 任务描述

## ✅ 已确认的信息
- 信息1: xxx
- 信息2: xxx

## 📝 最近的对话摘要
- 描述最近对话的主要内容

## ⚠️ 待办/注意事项
- 注意事项1

## 🔗 相关文件
- 相关文件路径

---

*此文件由系统自动维护，人工可编辑但会被覆盖*
```

## 工作流程

1. **每次任务完成** → 更新 session-context.md
2. **新模型启动** → 读取 session-context.md
3. **向用户确认** → 确认上下文是否正确

## 适用场景

- 多模型切换（timeout fallback）
- 长对话上下文恢复
- 多 agent 协作信息同步