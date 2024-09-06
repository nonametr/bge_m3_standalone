import time

import torch
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from FlagEmbedding import BGEM3FlagModel

app = Flask(__name__)
CORS(app)

bge_m3_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device="cuda")

known_gpus = {
    "RTX 2080": 1,
    "RTX 4090": 8,
    "RTX 4080": 6,
    "RTX 4080S": 7,
    "RTX 3090": 5,
    "RTX 3080": 4,
}

def get_gpu_flops():
    A = torch.randn(1000, 1000, device='cuda')
    B = torch.randn(1000, 1000, device='cuda')

    # Warm up
    for _ in range(10):
        C = torch.matmul(A, B)

    start_time = time.time()
    for _ in range(1000):
        C = torch.matmul(A, B)
    elapsed_time = time.time() - start_time

    num_operations = 2 * 1000**3 * 1000  # Matrix multiplication
    flops = num_operations / elapsed_time

    return flops

@app.route('/embeddings/generate/from_prompts', methods=['POST'])
def generate_embeddings_from_prompts_standalone():
    start_time = time.time()
    pp_prompt_list = request.json.get('prompts', [])

    result = bge_m3_model.encode(pp_prompt_list, batch_size=12, max_length=8192)

    return jsonify({"success": True, "duration": time.time() - start_time, "embeddings": result['dense_vecs'].tolist()})


@app.route('/info/gpu', methods=['GET'])
def get_gpu_info():
    # gpu_perf = int(get_gpu_flops() / 1e12)
    # gpu_weight = int(gpu_perf / 10) + 1
    gpu_name = torch.cuda.get_device_name(0)
    return jsonify({"gpu": gpu_name, "weight": known_gpus.get(gpu_name, 1)})


@app.route('/health_check', methods=['GET'])
def health_check():
    return Response(status=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8093)
