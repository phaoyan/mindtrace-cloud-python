import json
import os
import faiss
from ..word_similarity.embeddings import dimension

abspath = os.path.abspath(os.path.dirname(__file__))

index_src = os.path.join(abspath, "src.index")
if os.path.exists(index_src):
    index = faiss.read_index(index_src)
else:
    index = faiss.IndexFlatIP(dimension)

mapping_src = os.path.join(abspath, "mapping.json")
if os.path.exists(mapping_src):
    with open(mapping_src, 'r') as mapping_json:
        mapping: dict = json.load(mapping_json)
else:
    mapping: dict = {}

