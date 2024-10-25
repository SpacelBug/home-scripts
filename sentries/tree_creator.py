class Node:

    right_edges = []
    left_edges = []

    def __init__(self, value):
        self.value = value

    def add_right_edge(self):
        self.right_edges.append(Edge(self, 'value'))


class Edge:

    left_node = None
    right_node = None

    def __init__(self, left_node: Node, right_node_value):
        self.left_node = left_node
        self.right_node = Node(right_node_value)


class TreeCreator:

    def __init__(self, root_name):
        self.root = Node(root_name)