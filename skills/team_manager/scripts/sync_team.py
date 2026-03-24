import os
import sys
import subprocess
import shutil
import re

# 约定：GitHub 架构仓库的根目录
# 相对路径回退: scripts/ -> team_manager/ -> skills/ -> my-ai-team/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ARCH_AGENTS_DIR = os.path.join(REPO_ROOT, "agents")
GLOBAL_SOUL = os.path.join(REPO_ROOT, "SOUL.md")

# 约定：OpenClaw 实际存放各个单独 Agent 工作区的底层目录 
# 根据 OpenClaw 多智能体设计，每个 agent 生成后都有独立的 workspace-<agent_id> 文件夹存配置文件
OPENCLAW_ROOT_DIR = os.environ.get("OPENCLAW_DATA_DIR", os.path.expanduser("~/.openclaw"))

def run_command(cmd, cwd=None):
    print(f">> 执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令报错:\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def pull_and_sync():
    """从 GitHub 拉取最新架构，并拆解复制给每一个 OpenClaw Agent 单体文件池中"""
    print("📥 [CEO 权限] 正在拉取最新的 GitHub 团队架构设计...")
    
    if os.path.exists(os.path.join(REPO_ROOT, ".git")):
        run_command(["git", "pull"], cwd=REPO_ROOT)
    else:
        print("⚠️ 架构目录检测不到 .git 仓库状态，将直接使用当前本地架构文件。")
    
    if not os.path.exists(OPENCLAW_ROOT_DIR):
        os.makedirs(OPENCLAW_ROOT_DIR, exist_ok=True)
        print(f"📁 已在引擎侧初始化 Agent 运行时根文件路径: {OPENCLAW_ROOT_DIR}")

    # 读取总体规划设计中的每个 agent 文件
    for filename in os.listdir(ARCH_AGENTS_DIR):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(ARCH_AGENTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 精确提取 ID 以定位其在引擎内的实例槽位
        id_match = re.search(r'id:\s*([a-zA-Z0-9_]+)', content)
        if not id_match:
            print(f"⚠️ 跳过 {filename}: 无效的格式，未检测到 ID 标记。")
            continue
        agent_id = id_match.group(1).strip()
        
        # 检查是否已经在引擎中注册过该 Agent
        result = run_command(["openclaw", "agents", "list"])
        if agent_id not in result.stdout:
            print(f"   ✨ 检测到新 Agent [{agent_id}]，正在通过 CLI 注册...")
            run_command(["openclaw", "agents", "add", agent_id])
        else:
            print(f"   🔄 Agent [{agent_id}] 已在 openclaw.json 中注册，开始同步配置...")
            
        # 根据 OpenClaw 默认路径，寻找或设立 workspace
        agent_workspace_dir = os.path.join(OPENCLAW_ROOT_DIR, f"workspace-{agent_id}")
        os.makedirs(agent_workspace_dir, exist_ok=True)
        
        # OpenClaw 单体隔离逻辑：
        # 将团队全局的规章制度与代理特定的角色设定剥离注入对应原本自动生成的 Md 文件
        soul_target = os.path.join(agent_workspace_dir, "SOUL.md")
        identity_target = os.path.join(agent_workspace_dir, "IDENTITY.md")
        
        # 1. 注入灵魂 (覆盖掉默认的 SOUL.md，聚合全局容错+底线)
        with open(soul_target, 'w', encoding='utf-8') as f:
            if os.path.exists(GLOBAL_SOUL):
                with open(GLOBAL_SOUL, 'r', encoding='utf-8') as gs:
                    f.write(gs.read() + "\n\n---\n\n")
            f.write("# Agent 特定行为准则\n" + content)
                
        # 2. 注入岗位身份 (覆盖生成的 IDENTITY.md)
        with open(identity_target, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ 成功覆盖并激活 Agent 实例配置: {agent_workspace_dir}")
        
    print("🎯 所有特工组织机构已成功映射至 OpenClaw 引擎池，团队已重组完毕。")

def push_to_github():
    """将 OpenClaw 底层的运行变化或自进化状态反向收集回架构库并备份推送"""
    print("📤 [CEO 权限] 正在收集团队全量运行资料，准备逆向提取并打包架构配置...")
    
    # 这里可添加根据 runtime 实际变化改写回 ./agents 的具体同步逻辑
    
    run_command(["git", "add", "."], cwd=REPO_ROOT)
    run_command(["git", "commit", "-m", "chore: CEO 主动同步并保存 OpenClaw 最新组织状态"], cwd=REPO_ROOT)
    run_command(["git", "push"], cwd=REPO_ROOT)
    print("✅ 团队整体状态与架构演化已成功备份至 GitHub。")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Team Builder Tool for CEO")
    parser.add_argument("--action", choices=["pull_and_sync", "push_to_github"], required=True)
    args = parser.parse_args()
    
    if args.action == "pull_and_sync":
        pull_and_sync()
    elif args.action == "push_to_github":
        push_to_github()
