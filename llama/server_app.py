from flask import Flask, request, jsonify
from llm import execute_pipeline, load_llm_in_memory

app = Flask(__name__)

pipe = load_llm_in_memory()

@app.route('/ASK-LAMA', methods=['POST'])
def hello_world():
    execute_pipeline(pipe, str(request.data))

    return jsonify({"result": "OK"})
