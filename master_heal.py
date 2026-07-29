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
    prompt = f"""
You are an expert Android NDK, C++, Android.mk, CMake, and Gradle senior build engineer.
Analyze the following GitHub Actions workflow build failure error logs.
You have FULL READ, WRITE, CREATE, and DELETE permissions across the repository files. 
- Default to fixing errors using the existing setup (e.g., Android.mk / ndkBuild).
- ONLY migrate to CMake or remove Android.mk if it is strictly necessary to resolve the build failure.
- If you decide to delete a file or create a new one (like CMakeLists.txt), specify it clearly.

You MUST output the exact file modifications or deletions using these exact block formats:

To modify or create a file:
=== FILE: path/to/file ===
[File content here]
=== END FILE ===

To delete an obsolete file:
=== DELETE: path/to/file ===
=== END DELETE ===

ERROR LOGS:
{error_logs[-4000:]}
"""
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    # Naya Retry aur Auto-Switch Logic
    for attempt in range(len(MODELS_POOL)):
        active_key = get_next_gemini_key()
        model_name = get_next_model()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={active_key}"
        
        print(f"[*] Using Model: {model_name} (Attempt {attempt + 1}/{len(MODELS_POOL)})...")
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            res_json = response.json()
            if "candidates" in res_json:
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
            else:
                error_msg = res_json.get('error', {}).get('message', 'Unknown Error')
                print(f"[!] Model {model_name} failed: {error_msg}. Switching to next model...")
                time.sleep(2)
                continue
        except Exception as e:
            print(f"[!] Request failed for {model_name}: {str(e)}. Switching to next model...")
            time.sleep(2)
            continue

    return f"API Error / Limit Reached: All models failed after retries."

def apply_ai_patches(ai_response):
    changes_made = []

    pattern_file = r"=== FILE:\s*(.*?)===\s*\n(.*?)\s*=== END FILE ==="
    matches_file = re.findall(pattern_file, ai_response, re.DOTALL)
    for file_path, content in matches_file:
        file_path = file_path.strip()
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        changes_made.append(f"Updated/Created: {file_path}")

    pattern_del = r"=== DELETE:\s*(.*?)===\s*=== END DELETE ==="
    matches_del = re.findall(pattern_del, ai_response, re.DOTALL)
    for file_path in matches_del:
        file_path = file_path.strip()
        if os.path.exists(file_path):
            os.remove(file_path)
            changes_made.append(f"Deleted: {file_path}")

    if not changes_made:
        with open("ai_fix_suggestion.txt", "w", encoding="utf-8") as f:
            f.write(ai_response)
        return []

    return changes_made

def master_loop():
    print("==================================================")
    print(" Starting Full-Auto Master Healer (Smart-Decision Mode)")
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

            print("[*] Automatically applying AI patches & file changes...")
            applied_changes = apply_ai_patches(ai_fix)

            if applied_changes:
                print(f"[+] CHANGES APPLIED: {', '.join(applied_changes)}")
                run_cmd("git add .")
                run_cmd('git commit -m "Auto-fix applied by master_heal.py with full permissions"')
                run_cmd("git push origin main --force")
                print("[+] Pushed code updates to GitHub, triggering workflow...")
                trigger_workflow_dispatch()
                time.sleep(15)
            else:
                print("[!] No patch blocks parsed. Saved full response to ai_fix_suggestion.txt")
                time.sleep(10)

if __name__ == "__main__":
    master_loop()
