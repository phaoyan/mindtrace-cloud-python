import json
import faiss
import numpy as np
from ..utils import FeatureVector
from . import index, mapping, index_src, mapping_src


def get_ann_knode_ids(feature: FeatureVector, count: int) -> list[list]:
    result = index.search(feature, count)
    return [[mapping[str(result[1][0][i])], float(result[0][0][i])]
            for i in range(0, count)
            if mapping.keys().__contains__(str(result[1][0][i]))]


def add_to_index(feature: FeatureVector, knode_id: int) -> None:
    index.add(feature)
    mapping[index.ntotal] = knode_id


def add_to_index_batch(id_feature_mapping: dict) -> None:
    r"""
    :param id_feature_mapping: 如{"15495132546": [ ... ], ...}
    :return: None
    """
    items = id_feature_mapping.items()
    matrix = np.vstack([feature for (knode_id, feature) in items])
    cur = index.ntotal
    index.add(matrix)
    for knode_id, feature in items:
        mapping[str(cur)] = knode_id
        cur += 1


def save_index():
    faiss.write_index(index, index_src)
    with open(mapping_src, 'w') as mapping_file:
        json.dump(mapping, mapping_file, ensure_ascii=False, indent=4)


def clear_index():
    index.reset()
    mapping.clear()
    faiss.write_index(index, index_src)
    with open(mapping_src, 'w') as mapping_file:
        json.dump(mapping, mapping_file, ensure_ascii=False, indent=4)
