---
name: team_manager
description: 允许 CEO 核心智能体管理、生成和同步整个一人公司 AI 团队架构的技能。
version: 1.0.0
---

# Team Manager Skill

该技能赋予了核心管理者（CEO Agent）极高的权力，允许你直接从远程代码仓库拉取最新的组织架构定义，并自动在 OpenClaw 引擎内部组建、更新或销毁其他子 Agent（如 Assistant、Executor 等）。

这是一个高度自动化的技能，依靠你（CEO）来判断何时该“招聘（创建）”新员工，何时该“同步”公司规章制度。

## Tools (工具能力)

### 1. `sync_team_architecture`
- **Description**: 将团队的最新架构（存放所有单体 Agent 的定位、技能和价值观属性）从 GitHub 拉取下来，并将这些配置自动拆解、分发覆盖到 OpenClaw 引擎运行时的每个独立 Agent 专属目录中（即每个 Agent 自己单独的 SOUL, IDENTITY 等文件）。这通常在人类老板提示 "重新组建架构" 或 "更新团队" 时触发。
- **Command**: `python {SKILL_DIR}/scripts/sync_team.py --action pull_and_sync`
- **Permissions**: 系统文件读写权限、Shell 执行权限。

### 2. `export_team_state`
- **Description**: 如果 CEO 在业务执行中动态调整了团队成员的配置设置，或成员在持续沟通中记录了新的长期经验，使用此工具将 OpenClaw 的底层碎片化实际运行时参数提取整合回统一的 Markdown 架构代码库中，并自动提交(Push)反向备份回 GitHub，完成团队自我进化的固化。
- **Command**: `python {SKILL_DIR}/scripts/sync_team.py --action push_to_github`
- **Permissions**: Git 网络推送权限。

### 3. `team_health_check`
- **Description**: 运行全团队的运行状态与文件完整性扫描（Health Check）。用于列出哪些长效 Agent 的实体注册丢失、工作区损坏或者缺失核心的记忆文件（MEMORY.md）。当遇到多特工协作故障时，你可以率先运行它来进行排障（Troubleshooting）。
- **Command**: `python {SKILL_DIR}/scripts/sync_team.py --action health_check`
- **Permissions**: Shell 系统只读探测权限。
