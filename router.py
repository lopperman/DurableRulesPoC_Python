import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define microservices that provide rules
TASK_MICROSERVICES = {
    "task_firewall": "http://localhost:5001/rules",
    "task_router": "http://localhost:5002/rules",
    "task_switch": "http://localhost:5003/rules"
}

def fetch_rules():
    rules = []
    for task_name, url in TASK_MICROSERVICES.items():
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                rule_def = resp.json()
                rules.append(rule_def)
        except Exception as e:
            print(f"Error fetching rules from {task_name}: {e}")
    return rules

def evaluate_condition(condition, request_data):
    condition_type = condition.get("type")

    if condition_type == "eq":
        return request_data.get(condition["field"]) == condition["value"]
    elif condition_type == "ne":
        return request_data.get(condition["field"]) != condition["value"]
    elif condition_type == "in":
        return request_data.get(condition["field"]) in condition["values"]
    elif condition_type == "exists":
        return condition["field"] in request_data
    elif condition_type == "not_exists":
        return condition["field"] not in request_data
    elif condition_type == "gt":
        return request_data.get(condition["field"]) > condition["value"]
    elif condition_type == "lt":
        return request_data.get(condition["field"]) < condition["value"]
    elif condition_type == "branch":
        if evaluate_condition(condition["if"], request_data):
            return evaluate_condition(condition["then"], request_data)
        return True
    elif condition_type in ["and", "or", "xor"]:
        evaluations = [evaluate_condition(sub, request_data) for sub in condition["conditions"]]
        if condition_type == "and":
            return all(evaluations)
        elif condition_type == "or":
            return any(evaluations)
        elif condition_type == "xor":
            return evaluations.count(True) == 1
    else:
        raise ValueError(f"Unsupported condition type: {condition_type}")

def evaluate_rule(rule_def, request_data):
    for condition in rule_def.get("conditions", []):
        if not evaluate_condition(condition, request_data):
            return False
    return True

@app.route('/evaluate', methods=['POST'])
def evaluate():
    req_data = request.get_json()
    qualified_tasks = []
    all_rules = fetch_rules()

    for rule_def in all_rules:
        if evaluate_rule(rule_def, req_data):
            qualified_tasks.append(rule_def["task"])

    return jsonify({"qualified_tasks": qualified_tasks})

if __name__ == '__main__':
    app.run(port=5010)
