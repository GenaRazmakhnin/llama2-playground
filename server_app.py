from flask import Flask, request, jsonify
from llm import execute_pipeline, load_llm_in_memory

app = Flask(__name__)

pipe = load_llm_in_memory()

@app.route('/ASK-LAMA', methods=['POST'])
def hello_world():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON and contain 'numbers' field"}), 400

    if request.json is not None:
        text = request.json['text']

        execute_pipeline(pipe, text)
    
        return jsonify({"result": "OK"})
    
    return jsonify({ "result": None })
