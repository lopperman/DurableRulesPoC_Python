from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rules', methods=['GET'])
def get_rules():
    rule_definition = {
        "task": "task_a",
        "conditions": [
            {
                "type": "in",
                "field": "region",
                "values": ["EU", "US", "APAC"]
            },
            {
                "type": "branch",
                "if": {
                    "field": "region",
                    "equals": "EU"
                },
                "then": {
                    "field": "compliance",
                    "equals": "GDPR"
                }
            }
        ]
    }
    return jsonify(rule_definition)

if __name__ == '__main__':
    app.run(port=5001)
