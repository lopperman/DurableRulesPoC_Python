from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rules', methods=['GET'])
def get_rules():
    rule_definition = {
        "task": "task_b",
        "conditions": [
            {
                "type": "in",
                "field": "region",
                "values": ["EU", "US", "APAC"]
            }
        ]
    }
    return jsonify(rule_definition)

if __name__ == '__main__':
    app.run(port=5002)
