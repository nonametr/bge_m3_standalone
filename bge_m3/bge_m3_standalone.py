import time
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from FlagEmbedding import BGEM3FlagModel

app = Flask(__name__)
CORS(app)

bge_m3_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device="cuda")

@app.route('/embeddings/generate/from_prompts', methods=['POST'])
def generate_embeddings_from_prompts_standalone():
    start_time = time.time()
    pp_prompt_list = request.json.get('prompts', [])

    result = bge_m3_model.encode(pp_prompt_list, batch_size=12, max_length=8192)

    return jsonify({"success": True, "duration": time.time() - start_time, "embeddings": result['dense_vecs'].tolist()})



@app.route('/health_check', methods=['GET'])
def health_check():
    return Response(status=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8093)
