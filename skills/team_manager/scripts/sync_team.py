import os
import sys
import subprocess
import shutil
import re
import time
import argparse
from datetime import datetime

# OpenClaw 数据存放目录，用于存放 workspace 和 openclaw.json
OPENCLAW_ROOT_DIR = os.environ.get("OPENCLAW_DATA_DIR", os.path.expanduser("~/.openclaw"))
OPENCLAW_JSON_PATH = os.path.join(OPENCLAW_ROOT_DIR, "openclaw.json")

def run_command(cmd, cwd=None):
    print(f">> 执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令报错:\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def backup_openclaw_config():
    """备份 openclaw.json，防止意外写入或中断导致注册表损坏"""
    if os.path.exists(OPENCLAW_JSON_PATH):
        backup_dir = os.path.join(OPENCLAW_ROOT_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"openclaw_{timestamp}.json")
        try:
            shutil.copy(OPENCLAW_JSON_PATH, backup_path)
            print(f"📦 已自动备份系统注册表: {backup_path}")
            
            # 清理旧备份（只保留最近 5 个）
            backups = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith("openclaw_")])
            for old_backup in backups[:-5]:
                try: os.remove(old_backup)
                except: pass
        except Exception as e:
            print(f"⚠️ 备份系统注册表失败: {e}")

def pull_and_sync(repo_root):
    """从 GitHub 拉取最新架构，并拆解复制给每一个 OpenClaw Agent 单体文件池中"""
    print(f"📥 [CEO 权限] 正在拉取基于仓库 ({repo_root}) 的团队架构设计...")
    
    arch_agents_dir = os.path.join(repo_root, "agents")
    global_soul = os.path.join(repo_root, "SOUL.md")
    
    if os.path.exists(os.path.join(repo_root, ".git")):
        run_command(["git", "pull"], cwd=repo_root)
    else:
        print("⚠️ 架构目录检测不到 .git 仓库状态，将直接使用指定挂载的本地架构文件。")
    
    if not os.path.exists(OPENCLAW_ROOT_DIR):
        os.makedirs(OPENCLAW_ROOT_DIR, exist_ok=True)
        print(f"📁 已在引擎侧初始化 Agent 运行时根文件路径: {OPENCLAW_ROOT_DIR}")
        
    backup_openclaw_config()

    # 读取总体规划设计中的每个 agent 文件
    for filename in os.listdir(arch_agents_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(arch_agents_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 精确提取 ID 以定位其在引擎内的实例槽位
        id_match = re.search(r'id:\s*([a-zA-Z0-9_]+)', content)
        if not id_match:
            print(f"⚠️ 跳过 {filename}: 无效的格式，未检测到 ID 标记。")
            continue
        agent_id = id_match.group(1).strip()
        
        # 强化：检查是否注册并进行自校验和容错注册
        is_registered = False
        result = run_command(["openclaw", "agents", "list"])
        if result.returncode == 0 and agent_id in result.stdout:
            is_registered = True
            
        if not is_registered:
            print(f"   ✨ 检测到 Agent [{agent_id}] 未注册，正在强制调用系统 CLI 初始化注册流程...")
            run_command(["openclaw", "agents", "add", agent_id])
            time.sleep(1) # 短暂硬等待防止文件 IO 或 JSON 锁导致生成不全
            
            # 回环验证
            verify_res = run_command(["openclaw", "agents", "list"])
            if agent_id not in verify_res.stdout:
                print(f"   ❌ 严重警告: Agent [{agent_id}] 官方核心注册流程似乎失败，跳过写入。")
                continue
        else:
            print(f"   🔄 Agent [{agent_id}] 已在主控表合法注册，开始跨文件域状态同步...")
            
        # 根据 OpenClaw 默认路径，寻找或设立 workspace
        agent_workspace_dir = os.path.join(OPENCLAW_ROOT_DIR, f"workspace-{agent_id}")
        os.makedirs(agent_workspace_dir, exist_ok=True)
        
        # 1. 注入灵魂 (覆盖掉默认的 SOUL.md，聚合全局容错+底线)
        soul_target = os.path.join(agent_workspace_dir, "SOUL.md")
        with open(soul_target, 'w', encoding='utf-8') as f:
            if os.path.exists(global_soul):
                with open(global_soul, 'r', encoding='utf-8') as gs:
                    f.write(gs.read() + "\n\n---\n\n")
            f.write("# Agent 特定行为准则\n" + content)
                
        # 2. 注入岗位身份 (覆盖生成的 IDENTITY.md)
        identity_target = os.path.join(agent_workspace_dir, "IDENTITY.md")
        with open(identity_target, 'w', encoding='utf-8') as f:
            f.write(content)

        # 3. 建立并激活长效记忆中枢 (MEMORY.md)
        # OpenClaw 架构里，具备 MEMORY 才能与用户发生深度历史交互，是“常驻员工”的重要标志
        memory_target = os.path.join(agent_workspace_dir, "MEMORY.md")
        if not os.path.exists(memory_target):
            with open(memory_target, 'w', encoding='utf-8') as f:
                f.write(f"# {agent_id} 长期记忆库 (Long-term Memory)\n\n> 💡 系统提示：这是你的专属存储区。请把核心的复盘经验、User 的特殊偏好以及长期延续的项目状态更新到此。\n\n## 核心经验与偏好\n- [示例] 暂无记录\n\n## 运作历史锚点\n\n")
            
        print(f"✅ 成功完全激活常驻 Agent 实例物理配置 (SOUL/IDENTITY/MEMORY): {agent_workspace_dir}")
        
    print("🎯 所有特工组织机构已成功映射至 OpenClaw 引擎池，团队重组验证完毕。")

def push_to_github(repo_root):
    """将 OpenClaw 底层的运行变化或自进化状态反向收集回架构库并备份推送"""
    print("📤 [CEO 权限] 正在收集团队全量运行资料，准备逆向提取并打包架构配置...")
    run_command(["git", "add", "."], cwd=repo_root)
    run_command(["git", "commit", "-m", "chore: CEO 主动同步并保存 OpenClaw 最新组织状态"], cwd=repo_root)
    run_command(["git", "push"], cwd=repo_root)
    print("✅ 团队整体状态与架构演化已成功备份至 GitHub。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Team Builder Tool for CEO")
    parser.add_argument("--action", choices=["pull_and_sync", "push_to_github"], required=True)
    parser.add_argument("--repo-path", help="指定 GitHub 架构仓库所在的绝对路径", default=None)
    args = parser.parse_args()
    
    # 路径健壮性优化：
    # 优先级: 命令行参数 > 环境变量 > 默认后退计算
    if args.repo_path:
        final_repo_root = os.path.abspath(args.repo_path)
    # 支持在 OS 层面挂入 MY_AI_TEAM_REPO
    elif os.environ.get("MY_AI_TEAM_REPO"):
        final_repo_root = os.path.abspath(os.environ.get("MY_AI_TEAM_REPO"))
    else:
        # 向后兼容由于被当做技能载入时__file__的计算 (非常脆弱)
        final_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    if args.action == "pull_and_sync":
        pull_and_sync(final_repo_root)
    elif args.action == "push_to_github":
        push_to_github(final_repo_root)
