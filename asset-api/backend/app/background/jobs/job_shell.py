import subprocess
from backend.app.core.settings import config

def run_bash_shell(script_path: str, *args):
    """주어진 파일 경로의 쉘 스크립트를 실행하고, 추가 인자를 전달"""
    try:
        # 첫 번째 인자는 쉘 프로그램 경로로, 나머지는 그 인자로 설정
        which_bash = config.WHICH_BASH
        # result = subprocess.run(["/bin/bash", script_path, *args], check=True, capture_output=True, text=True)
        result = subprocess.run([which_bash, script_path, *args], check=True, capture_output=True, text=True)
        print("Shell script output:", result.stdout)  # 스크립트의 출력 결과
        return {"message": "Shell script executed successfully", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        print("Error executing shell script:", e.stderr)
        return {"error": f"Failed to execute shell script: {e.stderr}"}
