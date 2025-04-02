from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rules', methods=['GET'])
def get_rules():
    rule_definition = {
        "task": "task_switch",
        "conditions": [
            {"type": "eq", "field": "Device_Type", "value": "switch"},
            {
                "type": "xor",
                "conditions": [
                    {"type": "eq", "field": "Device_Function_Code", "value": "PER"},
                    {"type": "eq", "field": "Device_Function_Code", "value": "MON"},
                    {"type": "eq", "field": "Device_Function_Code", "value": "SEC"}
                ]
            }
        ]
    }
    return jsonify(rule_definition)

if __name__ == '__main__':
    app.run(port=5003)
