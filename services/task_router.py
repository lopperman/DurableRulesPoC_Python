from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rules', methods=['GET'])
def get_rules():
    rule_definition = {
        "task": "task_router",
        "conditions": [
            {"type": "eq", "field": "Device_Type", "value": "router"},
            {"type": "in", "field": "Site_Location", "values": ["NYC", "LON", "SFO"]},
            {
                "type": "or",
                "conditions": [
                    {"type": "eq", "field": "Managed_By_Group", "value": "netops"},
                    {"type": "eq", "field": "Supported_By_Group", "value": "infra"}
                ]
            }
        ]
    }
    return jsonify(rule_definition)

if __name__ == '__main__':
    app.run(port=5002)
