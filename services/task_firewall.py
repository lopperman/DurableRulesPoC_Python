from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rules', methods=['GET'])
def get_rules():
    rule_definition = {
        "task": "task_firewall",
        "conditions": [
            {"type": "eq", "field": "Device_Vendor", "value": "fortinet"},
            {"type": "eq", "field": "Device_Function_Code", "value": "SEC"},
            {
                "type": "branch",
                "if": {"type": "eq", "field": "Is_Virtual", "value": False},
                "then": {"type": "eq", "field": "Device_SubFunction_Code", "value": "SEC"}
            }
        ]
    }
    return jsonify(rule_definition)

if __name__ == '__main__':
    app.run(port=5001)
