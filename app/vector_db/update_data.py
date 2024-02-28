from vector_db.base_define import WeaviateClientSingleton

def update_data(uuid = "" , className = "Table", dataObject = {"name": "updated"}):
    # 使用單例模式創建 Weaviate 客戶端
    client = WeaviateClientSingleton("http://weaviate:8080")

    client.data_object.update(
        class_name = className,
        uuid = uuid,
        data_object = dataObject
    )
