import subprocess
import json
import sys
import urllib.request

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def ask_ollama(prompt):
    payload = json.dumps({
        "model": MODEL,
        "prompt": f"你是一个电脑自动化助手。用户会用中文描述任务，你需要生成一系列 Windows PowerShell 命令来完成它。只返回命令，不要解释，每条命令用一行，不要用 markdown 代码块包裹。\n\n用户需求：{prompt}",
        "stream": False
    }).encode('utf-8')
    
    req = urllib.request.Request(OLLAMA_API, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data["response"].strip()
    except Exception as e:
        print(f"连接 Ollama 失败：{e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python auto.py 你的自然语言指令")
        sys.exit(1)
    
    user_input = " ".join(sys.argv[1:])
    print(f"🤖 正在咨询本地大脑（{MODEL}）…\n")
    commands = ask_ollama(user_input)
    
    if not commands:
        print("❌ 获取命令失败，请确保 ollama serve 正在另一个窗口运行")
        sys.exit(1)
    
    print("📋 本地大脑建议的命令：")
    print(commands)
    print("\n⚠️  请逐条检查，确认无误后输入 y 执行，输入 n 取消")
    confirm = input("是否执行？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("已取消")
        sys.exit(0)
    
    for cmd in commands.split('\n'):
        cmd = cmd.strip()
        if not cmd:
            continue
        print(f"\n▶️  执行：{cmd}")
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"⚠️  命令返回错误码 {result.returncode}")
            print(result.stderr)
    
    print("\n✅ 所有命令执行完毕")

if __name__ == "__main__":
    main()