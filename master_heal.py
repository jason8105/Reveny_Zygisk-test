import os
import time
import subprocess
import requests
import re
import zipfile
import io
import shutil

# API Keys aur Model rotation pool
API_KEYS_POOL = {
    1: os.environ.get("GEMINI_KEY_1", ""),
    2: os.environ.get("GEMINI_KEY_2", "")
}

MODELS_POOL = [
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-1.5-flash"
]

current_key_id = 1
current_model_idx = 0

def get_next_gemini_key():
    global current_key_id
    key = API_KEYS_POOL.get(current_key_id)
    current_key_id = (current_key_id % len(API_KEYS_POOL)) + 1
    return key

def get_next_model():
    global current_model_idx
    model = MODELS_POOL[current_model_idx]
    current_model_idx = (current_model_idx + 1) % len(MODELS_POOL)
    return model

REPO_OWNER = "jason8105"
REPO_NAME = "Reveny_Zygisk-test"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "vnd.github+json"
} if GITHUB_TOKEN else {}

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def trigger_workflow_dispatch():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/build.yml/dispatches"
    try:
        requests.post(url, headers=HEADERS, json={"ref": "main"}, timeout=10)
    except Exception:
        pass

def get_latest_workflow_run():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs?per_page=1"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15).json()
        runs = res.get("workflow_runs", [])
        if not runs:
            return None, None
        return runs[0]["id"], runs[0]["status"]
    except Exception:
        return None, None

def get_workflow_logs(run_id):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/logs"
    try:
        response = requests.get(url, headers=HEADERS, allow_redirects=True, timeout=120)
        if response.status_code == 200:
            log_dir = "downloaded_logs"
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall(log_dir)
            all_logs = ""
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as lf:
                            all_logs += f"\n--- {file} ---\n" + lf.read()
                    except Exception:
                        pass
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            return all_logs if all_logs else "Empty log files extracted."
        else:
            return f"Log fetch error: Status {response.status_code}"
    except Exception as e:
        return f"Log fetch error: {e}"

def ask_gemini_http(error_logs):
    active_key = get_next_gemini_key()
    model_name = get_next_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={active_key}"
    
    print(f"[*] Using Model: {model_name}...")

    prompt = f"""
You are an expert Android NDK, C++, CMake, and Gradle build engineer. 
The user wants to migrate/use CMake instead of Android.mk. The following GitHub Actions workflow build failed or needs configuration fixes for CMake.
Analyze the error logs and provide the exact file modifications using this exact block format:

=== FILE: path/to/file ===
[Corrected file or configuration content here]
=== END FILE ===

ERROR LOGS:
{error_logs[-4000:]}
"""
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        res_json = response.json()
        if "candidates" in res_json:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error / Limit Reached: {res_json}"
    except Exception as e:
        return f"API Error: {str(e)}"

def apply_ai_patches(ai_response):
    pattern = r"=== FILE:\s*(.*?)===\s*\n(.*?)\s*=== END FILE ==="
    matches = re.findall(pattern, ai_response, re.DOTALL)

    if not matches:
        with open("ai_fix_suggestion.txt", "w", encoding="utf-8") as f:
            f.write(ai_response)
        return []

    patched_files = []
    for file_path, content in matches:
        file_path = file_path.strip()
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        patched_files.append(file_path)
    return patched_files

def master_loop():
    print("==================================================")
    print(" Starting Full-Auto Master Healer (CMake Migration Mode)")
    print("==================================================")

    last_processed_run_id = None

    while True:
        try:
            subprocess.run("termux-wake-lock", shell=True, capture_output=True)
        except Exception:
            pass

        print("[*] Waiting for active workflow run...")
        run_id, status = get_latest_workflow_run()
        if not run_id or run_id == last_processed_run_id:
            time.sleep(10)
            continue

        print(f"[*] Monitoring Workflow Run ID: {run_id} | Status: {status}")

        while status in ["queued", "in_progress"]:
            time.sleep(10)
            _, status = get_latest_workflow_run()
            print(f"[*] Current status: {status}...")

        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
        run_details = requests.get(url, headers=HEADERS).json()
        conclusion = run_details.get("conclusion")

        last_processed_run_id = run_id

        if conclusion == "success":
            print("\n==================================================")
            print(" SUCCESS! Build passed cleanly across all files!")
            print("==================================================")
            break
        else:
            print(f"[!] Build failed with conclusion: {conclusion}. Fetching logs...")
            logs = get_workflow_logs(run_id)

            print("[*] Sending error logs to Gemini using rotating models & keys...")
            ai_fix = ask_gemini_http(logs)

            print("[*] Automatically rewriting files based on AI patches...")
            fixed_files = apply_ai_patches(ai_fix)

            if fixed_files:
                print(f"[+] FIXED FILES: {', '.join(fixed_files)}")
                run_cmd("git add .")
                run_cmd('git commit -m "Auto-fix CMake configuration via master_heal.py"')
                run_cmd("git push origin main --force")
                print("[+] Pushed code updates to GitHub, triggering workflow...")
                trigger_workflow_dispatch()
                time.sleep(15)
            else:
                print("[!] No patch blocks parsed. Saved full response to ai_fix_suggestion.txt")
                time.sleep(10)

if __name__ == "__main__":
    master_loop()
