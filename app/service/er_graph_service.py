from helper.base_define import data_get, dd, dump
from graph.base_define import Shape, Node, Graph
from vector_db.query_data import is_empty_result, semantic_search
from service.sentence_analysis_service import SentenceAnalysis

def create_er_graph_by_data(data: dict):
    # 宣告藍圖
    graph = Graph()

    for table, content in data.items():
        temp = semantic_search(
            "Table",
            ["name", "ref { tag, shape, search_default_column }"],
            table
        )

        # 匹配到 Table
        if is_empty_result(temp, 'Table') != False:
            continue

        # 使用最相近(第一筆)
        graph.insert(
            temp["data"]["Get"]["Table"][0]["ref"]["shape"],
            table,
            temp["data"]["Get"]["Table"][0]["_additional"]["id"],
            temp["data"]["Get"]["Table"][0]["ref"]
        )

    for table, content in data.items():
        for temp in data_get(content, "attributes.relation", []):
            self_node_temp = graph.search_by_shape_and_name(content['attributes']['shape'], table)
            goal_node_temp = graph.search_by_shape_and_name(Shape.entity.value, temp['node_name'])

            if self_node_temp != None and goal_node_temp != None:
                self_node_temp.connect(goal_node_temp, temp['connection_name'])

    return graph

def create_er_graph_by_text(graph_org: Graph, text):
    graph_need = Graph()
    sentence_analysis = SentenceAnalysis()
    value_list = []

    value_list += prepare_create_er_graph_by_single_word(
        sentence_analysis,
        text
    )

    value_list += prepare_create_er_graph_by_clause(
        graph_org,
        graph_need,
        sentence_analysis,
        text
    )

    for temp in value_list:
        # 為 Value 找到對應的 Table 節點並連線
        table_node_temp = graph_need.search_by_shape_and_name(
            temp['ref']['table_shape'],
            temp['ref']['table'],
        )

        if table_node_temp == None:
            continue

        if table_node_temp.shape != Shape.entity.value:
            continue

        name_temp = temp['ref']['column'] + '=' + temp['name'] # 待修改：列舉可能的情況（>、<、=、!=）

        value_node_temp = graph_need.insert(Shape.predicate.value, name_temp, temp['id'])

        if value_node_temp != None:
            value_node_temp.connect(table_node_temp)
        # 待修改：
            # 1. 新增 Column 的情境：
                # 找出「目標提取詞」並將線標註為「heanoun」；
                # 當「線的名稱為 heanoun」，橢圓節點的資訊需要另外存（Table、column） --> T(Q)
            # 2. 找到節點後，需要將其連線的「線加名稱，如 subject、Object、modifier、headnoun、and、or」
            # 3. Value 連線的可能性有，1. 與矩形連接（ok），2.與菱形連接（ok），3.與橢圓連接（線的名稱為 and 或 or）

    return graph_need

def prepare_create_er_graph_by_single_word(sentence_analysis: SentenceAnalysis, text):
    res = sentence_analysis.single_word(text)

    return res['value_list']

def prepare_create_er_graph_by_clause(graph_org: Graph, graph_need: Graph, sentence_analysis: SentenceAnalysis, text: str):
    value_list = []

    data_lists = sentence_analysis.clause(text)

    for data_list in data_lists:
        node_head = semantic_search(
            "Table",
            ["name", "ref { tag, shape, search_default_column }"],
            data_list['modified_noun']
        )

        # 沒匹配到 Table
        if is_empty_result(node_head, 'Table') == True:
            continue

        node_head_name = node_head['data']['Get']['Table'][0]['name']
        node_head_shape = node_head['data']['Get']['Table'][0]['ref']['shape']

        # 不是矩形就略過
        if node_head_shape != Shape.entity.value:
            continue

        # 找不到關聯就略過
        node_mid = graph_org.search_by_shape_to_another_shape_and_name(Shape.diamond.value, Shape.entity.value, node_head_name)

        if node_mid == None:
            continue

        res_temp = sentence_analysis.single_word(data_list['condition'])

        res_table_list_temp = res_temp['table_list']

        # 連 table 都找不到則略過
        if not res_table_list_temp['diamond'] and not res_table_list_temp['entity'] and not res_table_list_temp['predicate']:
            continue

        # 連 value 都沒有則略過
        if not res_temp['value_list']:
            continue

        for temp in res_temp['value_list']:
            temp_ref = temp['ref']

            if temp_ref['table_shape'] != Shape.entity.value:
                continue

            node_tail = graph_org.search_by_shape_and_name(
                temp_ref['table_shape'],
                temp_ref['table'],
            )

            if node_tail == None:
                continue

            # 檢查是否有關聯
            relation_status = False

            for node_temp in node_mid.connections:
                if node_temp.node.shape == node_tail.shape and node_temp.node.name == node_tail.name:
                    relation_status = True

            if relation_status == False:
                continue

            for node_temp in node_mid.connections:
                graph_need.append(node_temp.node)

                # 判斷  headnoun
                if node_temp.node.name == node_head_name:
                    column_temp = node_temp.node.ref['search_default_column']
                    name_temp = column_temp + '= ?' # 暫時用 ?

                    search_default_node = graph_need.insert(Shape.predicate.value, name_temp, '')

                    node_temp.node.connect(search_default_node, 'headnoun')

            graph_need.append(node_mid)

        value_list = value_list + res_temp['value_list']

    return value_list
