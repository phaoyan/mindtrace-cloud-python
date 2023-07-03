import os.path

import torch
from sklearn.preprocessing import normalize
from transformers import BertModel, BertTokenizer

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

abspath = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(abspath, "models/shibing624")
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertModel.from_pretrained(model_path)
def get_feature_vector_text2vec(text):
    encoded_input = tokenizer(text, padding=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    # 归一化以实现余弦相似度
    return normalize(sentence_embeddings)


if __name__ == '__main__':
    print(get_feature_vector_text2vec(["微积分"]))
    # model_name = "shibing624/text2vec-base-chinese"
    # model = BertModel.from_pretrained(model_name)
    # tokenizers = BertTokenizer.from_pretrained(model_name)
    # model.save_pretrained("./")
    # tokenizers.save_pretrained("./")
