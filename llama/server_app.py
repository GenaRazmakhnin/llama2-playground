from flask import Flask, request, jsonify
from llm import execute_pipeline, load_llm_in_memory

app = Flask(__name__)

pipe = load_llm_in_memory()

@app.route('/ASK-LAMA', methods=['POST'])
def hello_world():
    # print(request.content_type)
    # print(request.data)

    # if not request.is_json:
    #     return jsonify({"error": "Request must be JSON and contain 'numbers' field"}), 400

    # if request.json is not None:
    #

    execute_pipeline(pipe, str(request.data))

    return jsonify({"result": "OK"})
