import spacy
from sentence_transformers import SentenceTransformer
import weaviate

# 連接到 Weaviate 伺服器
client = weaviate.Client("http://weaviate:8080")
schema = {
    "classes": [
        {
            "class": "Sentence",
            "description": "A class to store sentences and their embeddings",
            "properties": [
                {
                    "name": "text",
                    "dataType": ["text"],
                    "description": "The original sentence text",
                },
                {
                    "name": "embedding",
                    "dataType": ["vector"],
                    "description": "The SBERT embedding of the sentence",
                },
            ],
        },
    ],
}

nlp = spacy.load("en_core_web_md")
sentence = "List suppliers who supply red parts?"
doc = nlp(sentence) # 使用 spaCy 處理句子

# 初始化SBERT模型
model = SentenceTransformer('all-MiniLM-L6-v2')
segSen=[]
for token in doc: # 輸出每個詞彙的文本、通用詞性和詳細詞性
    segSen.append(token.text)
    # print(f"{token.text:12} {token.pos_:10} {token.dep_}")

    embedding = model.encode(token.text) # 將句子轉換成向量
    data_object = {
        "text": token.text,
        # 將 ndarray 轉換為一個可以被 JSON 序列化的格式，意即使用 .tolist() 方法將 ndarray 轉換為列表。
        "embedding": {"vector": embedding.tolist()},
    }
    vcid = client.data_object.create(data_object, "Sentence")
    print(f"Created Sentence with UUID: {vcid}")

