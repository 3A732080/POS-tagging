from helper.base_define import dump
from enum import Enum

class Shape(Enum):
    diamond = 'diamond'  # 菱形
    predicate = 'predicate'  # 橢圓形
    entity = 'entity'  # 矩形

class Connection:
    def __init__(self, node, name):
        self.node = node  # 連接到的節點
        self.name = name  # 連線的名稱

    def __repr__(self):
        return f"<Connection(node={self.node}, name={self.name})>"

class Node:
    def __init__(self, shape, name, id, ref: dict = {}):
        self.id = id  # 給每個節點一個唯一的標識符
        self.shape = shape
        self.name = name
        self.ref = ref
        self.connections = []

    def connect(self, other_node, connection_name = ''):
        # 建立連接時，同時指定連線的名稱
        self.connections.append(Connection(other_node, connection_name))

    def __repr__(self):
        return f"< Node(id = {self.id}, shape = {self.shape}, name = {self.name}) >" 
        # 返回一個格式化的字符串，其中包含節點的 ID、形狀和名稱。

class Graph:
    def __init__(self):
        self.nodes = []

    def append(self, node: Node):
        self.nodes.append(node)

        return

    def insert(self, shape, name, id, ref: dict = {}):
        """插入一個新節點到圖中"""
        if self.search_by_shape_and_name(shape, name) == None:
            newNode = Node(shape, name, id, ref)
            self.nodes.append(newNode)
            dump("建立 Node -> shape:" + shape + ", name:" + name)

            return newNode

        return None

    def search_connections(self, shape_from, shape_to):
        """搜尋所有指定形狀連接的節點對，包括雙向連接"""
        connections = []
        for node in self.nodes:
            if node.shape == shape_from:
                for connection in node.connections:
                    if connection.node.shape == shape_to:
                        dump(f"{node}")
                        dump(f"連接到")
                        dump(f"{connection.node}")
                        connections.append((node, connection.node))
            elif node.shape == shape_to:  # 檢查反向連接
                for connection in node.connections:
                    if connection.node.shape == shape_from:
                        dump(f"{connection.node}")
                        dump(f"連接到")
                        dump(f"{node}")
                        connections.append((connection.node, node))  # 順序反過來，以匹配搜尋方向
        return connections

    def search_by_name(self, name):
        lists = []

        for node in self.nodes:
            if node.name == name:
                # dump(f"對應的節點 :{node}") # 待修改

                lists.append(node)

        return lists

    def search_by_shape(self, shape):
        lists = []

        for node in self.nodes:
            if node.shape == shape:
                lists.append(node)

        return lists

    def search_by_shape_to_another_shape_and_name(self, shape_from, shape_to, goal_node_name):
        for node in self.nodes:
            if node.shape == shape_from:
                for connection in node.connections:
                    if connection.node.shape == shape_to and connection.node.name == goal_node_name:
                        return node

        return None

    def search_by_shape_and_name(self, shape, name):
        for node in self.nodes:
            if  node.shape == shape and node.name == name:
                # dump(f"對應的節點 :{node}")

                return node

        return None

    def search_connection_by_name(self, connectionName):
        lists = []

        """根據連線名稱搜尋連線"""
        for node in self.nodes:
            for connection in node.connections:
                if connection.name == connectionName:
                    # dump(f"找到連線：{node} 連接到 {connection.node}")
                    lists.append((node, connection.node))

        return lists

# # 使用範例
# graph = Graph()
# n1 = graph.insert(Shape.entity.value, 'Suppliers')
# n2 = graph.insert(Shape.predicate.value, 'sname = ?')
# n3 = graph.insert(Shape.diamond.value, 'Shipments')
# n4 = graph.insert(Shape.entity.value, 'Parts')
# n5 = graph.insert(Shape.predicate.value, 'color = red')

# # 建立帶有命名連線的節點之間的關係
# n1.connect(n2, "connection1")
# n1.connect(n3, "connection2")
# n3.connect(n4, "connection3")
# n4.connect(n5, "abc")  # 特別注意這條連線，名稱為 "abc"

# diamondToDiamond = graph.search_connections(Shape.entity.value, Shape.diamond.value)

# shipmentNodes = graph.search_by_name("color = red")

# # 搜索名稱為 "abc" 的連線
# connections = graph.search_connection_by_name("abc")
