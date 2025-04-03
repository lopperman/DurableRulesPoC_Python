import multiprocessing
import requests
import json
import time
import subprocess
import os

# kill code: kill $(lsof -ti :5010 -i :5001 -i :5002 -i :5003)

# Paths to your service files
SERVICES = {
    "router": "router.py",
    "task_firewall": "services/task_firewall.py",
    "task_router": "services/task_router.py",
    "task_switch": "services/task_switch.py"
}

# Folder with your test request files
TEST_REQUESTS_DIR = "./tests/test_requests"
TEST_FILES = [
    "matches_firewall.json",
    "matches_nothing.json",
    "matches_router_switch.json"
]

def run_service(file):
    subprocess.run(["python", file])

if __name__ == "__main__":
    # Start each microservice
    procs = []
    for name, file in SERVICES.items():
        p = multiprocessing.Process(target=run_service, args=(file,))
        p.start()
        procs.append(p)

    print("Waiting for services to start...")
    time.sleep(3)

    # Iterate through test files and evaluate them
    for filename in TEST_FILES:
        full_path = os.path.join(TEST_REQUESTS_DIR, filename)
        print(f"\nEvaluating request: {filename}")

        try:
            with open(full_path) as f:
                data = json.load(f)
            response = requests.post("http://localhost:5010/evaluate", json=data)
            print("Qualified Tasks:", response.json().get("qualified_tasks"))
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Cleanup
    print("\nStopping all services...")
    for p in procs:
        print(f"Stopping process {p.pid}")
        if p.is_alive():
            p.kill()  # More forceful than terminate()
            p.join(timeout=2)  # Wait up to 2 seconds for process to end
            if p.is_alive():
                print(f"Warning: Process {p.pid} could not be killed")
        else:
            print(f"Process {p.pid} killed successfully")
