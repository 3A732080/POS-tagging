from vector_db.base_define import WeaviateClientSingleton

def delete_data(uuid = "" , className = "Table"):
    # 使用單例模式創建 Weaviate 客戶端
    client = WeaviateClientSingleton("http://weaviate:8080")

    client.data_object.delete(
        class_name = className,
        uuid = uuid
    )
