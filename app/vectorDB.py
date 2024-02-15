from sentence_transformers import SentenceTransformer
import weaviate

# 連接到 Weaviate 伺服器
client = weaviate.Client("http://weaviate:8080")

# 檢查連接是否成功
if client.is_ready():
    print("成功連接到 Weaviate!")
else:
    print("連接到 Weaviate 失敗。")


# client.schema.delete_all()
# client.schema.get()

# 初始化 SBERT 模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 確保 Weaviate 實例中有相應的schema設定
# 創建一個 schema 的範例。
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

# 嘗試創建schema，如果已存在則忽略錯誤
# try:
#     client.schema.create(schema)
# except Exception as e:
#     print(f"Error creating schema: {e}")

def store_text_with_embedding(text):
    embedding = model.encode(text)
    data_object = {
        "text": text,
        # 將 ndarray 轉換為一個可以被 JSON 序列化的格式，意即使用 .tolist() 方法將 ndarray 轉換為列表。
        "embedding": {"vector": embedding.tolist()},
    }
    vcid = client.data_object.create(data_object, "Sentence")
    print(f"Created Sentence with UUID: {vcid}")

store_text_with_embedding("List suppliers who supply red parts?")
# print("數據添加成功。")
