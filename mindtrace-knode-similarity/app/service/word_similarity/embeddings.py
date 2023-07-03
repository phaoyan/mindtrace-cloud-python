from .text_to_vec_embeddings import get_feature_vector_text2vec

dimension = 768
def get_feature_vector(text):
    return get_feature_vector_text2vec(text)

