import json
from flask import Flask
from flask import request, jsonify
from prediction.predict import predict_from_sentence
from util.amr import penman_to_dot
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def hello_world():
    sentence = request.args.get('sentence')
    print(sentence)
    amr_graph = predict_from_sentence(sentence)

    response = {}
    response['amr_graph'] = str(amr_graph)
    response['triples'] = amr_graph._triples
    response['edges'] = amr_graph.edges()
    response['top'] = amr_graph._top
    response['dot'] = penman_to_dot(amr_graph)

    return jsonify(response)