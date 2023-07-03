import json

import numpy as np
from app import app
from app.service.word_similarity.embeddings import get_feature_vector
from app.service.ann.faiss_ann import add_to_index_batch, save_index, clear_index as clear
from flask import request
from app.service.ann.faiss_ann import get_ann_knode_ids
from general.service_clients import get_chain_style_title, knode_check_all

@app.route("/debug")
def hello_world():
    return "hello world"

@app.route("/knode/<int:knode_id>/similar")
def get_nearest_neighbors(knode_id: int):
    count: int = int(request.args.get("count"))
    knode_feature: np.array = get_feature_vector([get_chain_style_title(knode_id)])
    res = json.dumps(get_ann_knode_ids(knode_feature, count)) if knode_feature is not None else "[]"
    return res

@app.route("/index", methods=["DELETE"])
def clear_index():
    clear()
    return "done"

@app.route("/index", methods=["POST"])
def add_index():
    data: dict = request.json
    ids: list[int] = [knodeId if type(knodeId) is int else int(knodeId) for knodeId in data["knodeIds"]]
    chunk_size = 100
    chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
    for chunk in chunks:
        features = get_feature_vector([get_chain_style_title(knode_id) for knode_id in chunk])
        mapping = {chunk[i]: features[i] for i in range(0, len(chunk))}
        add_to_index_batch(mapping)
        print("data added to index ...")
    save_index()
    print("Done!")
    return ""

@app.route("/index/refresh", methods=["POST"])
def refresh_index():
    clear()
    print("index refreshing ...")
    knodes = knode_check_all()
    ids = [int(knode["id"]) for knode in knodes]
    chunk_size = 100
    chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
    for chunk in chunks:
        features = get_feature_vector([get_chain_style_title(knode_id) for knode_id in chunk])
        mapping = {chunk[i]: features[i] for i in range(0, len(chunk))}
        add_to_index_batch(mapping)
        print("data added to index ...")
    save_index()
    print("Done!")
    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=31595)


