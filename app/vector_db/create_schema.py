from helper.base_define import dd
from vector_db.base_define import WeaviateClientSingleton

def create_schema():
    # 使用單例模式創建 Weaviate 客戶端
    client = WeaviateClientSingleton("http://weaviate:8080")

    # 創建 schema
    table = {
        "class": "Table",
        "properties": [
            {
                "name": "name",
                "dataType": ["text"],
            },
            {
                "name": "ref",
                "dataType": ["object"],
                "nestedProperties": [
                    {"dataType": ["text[]"], "name": "tag"},
                    {"dataType": ["text"], "name": "shape"},
                    {"dataType": ["text"], "name": "search_default_column"},
                ],
            },
        ],
        "vectorizer": "text2vec-transformers",  # this could be any vectorizer
        "vectorIndexConfig": {
            "distance": "cosine",
        },
        "moduleConfig": {
            "text2vec-transformers": {
                "model": "all-MiniLM-L6-v2"
            }
        }
    }

    column = {
        "class": "Column",
        "properties": [
            {
                "name": "name",
                "dataType": ["text"],
            },
            {
                "name": "ref",
                "dataType": ["object"],
                "nestedProperties": [
                    {"dataType": ["text[]"], "name": "tag"},
                    {"dataType": ["text"], "name": "table"},
                ],
            }
        ],
        "vectorizer": "text2vec-transformers",  # this could be any vectorizer
        "vectorIndexConfig": {
            "distance": "cosine",
        },
        "moduleConfig": {
            "text2vec-transformers": {
                "model": "all-MiniLM-L6-v2"
            }
        }
    }

    value = {
        "class": "Value",
        "properties": [
            {
                "name": "name",
                "dataType": ["text"],
            },
            {
                "name": "ref",
                "dataType": ["object"],
                "nestedProperties": [
                    {"dataType": ["text[]"], "name": "tag"},
                    {"dataType": ["text"], "name": "table"},
                    {"dataType": ["text"], "name": "table_shape"},
                    {"dataType": ["text"], "name": "column"},
                ],
            },
        ],
        "vectorizer": "text2vec-transformers",  # this could be any vectorizer
        "vectorIndexConfig": {
            "distance": "cosine",
        },
        "moduleConfig": {
            "text2vec-transformers": {
                "model": "all-MiniLM-L6-v2"
            }
        }
    }

    # 刪除所有 schema
    client.schema.delete_all()
    # client.schema.get()
    # 嘗試創建schema，如果已存在則忽略錯誤
    try:
        client.schema.create_class(table)
        client.schema.create_class(column)
        client.schema.create_class(value)
    except Exception as e:
        dd(f"[create_schema] error: {e}")