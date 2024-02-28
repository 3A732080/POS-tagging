from helper.base_define import data_get, dd, dump
from graph.base_define import Shape, Node, Graph
from vector_db.create_schema import create_schema
from vector_db.insert_data import insert_data
from vector_db.query_data import is_empty_result, semantic_search
from vector_db.update_data import update_data
from vector_db.delete_data import delete_data
from service.er_graph_service import create_er_graph_by_data, create_er_graph_by_text

data = {
    "suppliers": {
        "attributes": {
            "shape": Shape.entity.value,
            "relation": [],
            "search_default_column": "sname",
        },
        "column": ["sno","sname","status","city"],
        "values":[
            ["S1", "Smith","20","London"],
            ["S2", "Jones","10","Paris"],
            ["S3", "Blake","30","Paris"],
            ["S4", "Clark","20","London"],
            ["S5", "Adames","30","Taipei"],
        ],
    },
    "shipments": {
        "attributes": {
            "shape": Shape.diamond.value,
            "relation": [
                {
                    "connection_name": "subject",
                    "node_name": "suppliers",
                },
                {
                    "connection_name": "object",
                    "node_name": "parts",
                }
            ],
            "search_default_column": "",
        },
        "column": ["sno","pno","qty"],
        "values":[
            ["S1", "P1","300"],
            ["S1", "P2","200"],
            ["S1", "P3","400"],
            ["S1", "P4","200"],
            ["S1", "P5","100"],
            ["S1", "P6","100"],
            ["S2", "P1","300"],
            ["S2", "P2","400"],
            ["S3", "P2","200"],
            ["S4", "P2","200"],
            ["S4", "P4","300"],
            ["S4", "P5","400"],
        ],
    },
    "parts": {
        "attributes": {
            "shape": Shape.entity.value,
            "relation": [],
            "search_default_column": "",
        },
        "column": ["pno","pname","color","weight","city"],
        "values":[
            ["P1", "Nuts","Red","12","London"],
            ["P2", "Bolt","Green","17","Paris"],
            ["P3", "Screw","Blue","17","Rome"],
            ["P4", "Screw","Red","14","London"],
            ["P5", "Cam","Blue","12","Paris"],
            ["P6", "Cog","Red","19","London"],
        ],
    }
}

text = "List suppliers who supply red parts?"

create_schema()
insert_data(data)
# 建立資料藍圖
graph_org = create_er_graph_by_data(data)
# 產生問句藍圖
graph_need = create_er_graph_by_text(graph_org, text)

# 根據問題，尋找目標節點
dump("已產生問句藍圖")
dump(graph_need.nodes)
graph_need.search_connections(Shape.diamond.value, Shape.entity.value)
graph_need.search_connections(Shape.predicate.value, Shape.entity.value)

# 待修正：
    # 找出輸入 1、2 間「是否存在其他節點」，列出其節點名稱、線的名稱
