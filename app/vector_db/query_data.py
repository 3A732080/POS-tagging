from vector_db.base_define import WeaviateClientSingleton
from helper.base_define import data_get

# 語義搜索
def semantic_search(target, select, search):
    # 使用單例模式創建 Weaviate 客戶端
    client = WeaviateClientSingleton("http://weaviate:8080")

    query_result = client.query.get(
        class_name = target,
        properties = select
    ).with_near_text({
        "concepts": search,
        "boost": 2,  # 提升 "enterprise" 的權重，使其在搜尋結果中更加突出
        "certainty": 0.65

    }).with_additional([
        # "vector",
        "id",
        "distance"
    ]).with_limit(5).do()

    return query_result

# 檢查回傳是否有匹配值
def is_empty_result(response, keyName):
    res = data_get(response, "data.Get."+ keyName, [])

    return isinstance(res, list) and len(res) == 0