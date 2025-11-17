import sys

class Building:
    def __init__(self, b_id, name, location):
        self.id = b_id
        self.name = name
        self.location = location

class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, data):
        if root is None:
            return BSTNode(data)
        if data.id < root.data.id:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)
        return root

    def search(self, root, b_id):
        if root is None or root.data.id == b_id:
            return root
        if b_id < root.data.id:
            return self.search(root.left, b_id)
        return self.search(root.right, b_id)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.data.id, root.data.name, root.data.location)
            self.inorder(root.right)

    def preorder(self, root):
        if root:
            print(root.data.id, root.data.name, root.data.location)
            self.preorder(root.left)
            self.preorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.data.id, root.data.name, root.data.location)

    def get_height(self, root):
        if root is None:
            return 0
        left_h = self.get_height(root.left)
        right_h = self.get_height(root.right)
        if left_h > right_h:
            return left_h + 1
        else:
            return right_h + 1

class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, data):
        if not node:
            return AVLNode(data)
        if data.id < node.data.id:
            node.left = self.insert(node.left, data)
        else:
            node.right = self.insert(node.right, data)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and data.id < node.left.data.id:
            return self.right_rotate(node)
        if balance < -1 and data.id > node.right.data.id:
            return self.left_rotate(node)
        if balance > 1 and data.id > node.left.data.id:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and data.id < node.right.data.id:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.data.id, root.data.name, root.data.location)
            self.inorder(root.right)

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_matrix = [[0 for column in range(vertices)] for row in range(vertices)]
        self.adj_list = {}
        self.edges = []

    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.adj_matrix[v][u] = weight
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.edges.append([u, v, weight])

    def bfs(self, start_node):
        visited = [False] * self.V
        queue = []
        queue.append(start_node)
        visited[start_node] = True
        print("BFS Traversal:", end=" ")
        while queue:
            s = queue.pop(0)
            print(s, end=" ")
            if s in self.adj_list:
                for i in self.adj_list[s]:
                    if visited[i] == False:
                        queue.append(i)
                        visited[i] = True
        print()

    def dfs_util(self, v, visited):
        visited[v] = True
        print(v, end=" ")
        if v in self.adj_list:
            for i in self.adj_list[v]:
                if visited[i] == False:
                    self.dfs_util(i, visited)

    def dfs(self, start_node):
        visited = [False] * self.V
        print("DFS Traversal:", end=" ")
        self.dfs_util(start_node, visited)
        print()

    def dijkstra(self, src):
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        for cout in range(self.V):
            min_val = sys.maxsize
            min_index = -1
            for v in range(self.V):
                if dist[v] < min_val and sptSet[v] == False:
                    min_val = dist[v]
                    min_index = v
            u = min_index
            sptSet[u] = True
            for v in range(self.V):
                if self.adj_matrix[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.adj_matrix[u][v]:
                    dist[v] = dist[u] + self.adj_matrix[u][v]
        print("Optimal Paths (Dijkstra) from Node", src)
        for node in range(self.V):
            print("To Building", node, "Distance:", dist[node])

    def find_parent(self, parent, i):
        if parent[i] == i:
            return i
        return self.find_parent(parent, parent[i])

    def union_sets(self, parent, rank, x, y):
        xroot = self.find_parent(parent, x)
        yroot = self.find_parent(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []
        i = 0
        e = 0
        self.edges = sorted(self.edges, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1 and i < len(self.edges):
            u, v, w = self.edges[i]
            i = i + 1
            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union_sets(parent, rank, x, y)
        print("Utility Layout (Kruskal MST):")
        for u, v, weight in result:
            print("Cable from", u, "to", v, "Cost:", weight)

class ExpressionNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def evaluate_expression(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return int(root.value)
    left_sum = evaluate_expression(root.left)
    right_sum = evaluate_expression(root.right)
    if root.value == '+':
        return left_sum + right_sum
    if root.value == '-':
        return left_sum - right_sum
    if root.value == '*':
        return left_sum * right_sum
    if root.value == '/':
        return left_sum / right_sum
    return 0

print("--- 1. Building Data & BST Implementation ---")
bst = BST()
root = None
b1 = Building(101, "Library", "North Campus")
b2 = Building(102, "Engineering", "South Campus")
b3 = Building(100, "Admin", "Main Gate")
b4 = Building(103, "Cafeteria", "Center")

root = bst.insert(root, b1)
root = bst.insert(root, b2)
root = bst.insert(root, b3)
root = bst.insert(root, b4)

print("BST Inorder Traversal:")
bst.inorder(root)
print("BST Preorder Traversal:")
bst.preorder(root)
print("BST Postorder Traversal:")
bst.postorder(root)

search_res = bst.search(root, 102)
if search_res:
    print("Found Building:", search_res.data.name)
else:
    print("Building not found")

print("\n--- 2. AVL Tree Implementation ---")
avl = AVLTree()
avl_root = None
avl_root = avl.insert(avl_root, b1)
avl_root = avl.insert(avl_root, b2)
avl_root = avl.insert(avl_root, b3)
avl_root = avl.insert(avl_root, b4)

print("AVL Inorder Traversal:")
avl.inorder(avl_root)

bst_height = bst.get_height(root)
avl_height = avl.get_height(avl_root)
print("BST Height:", bst_height)
print("AVL Height:", avl_height)

print("\n--- 3. Graph Implementation & Traversals ---")
g = Graph(4) 
g.add_edge(0, 1, 10) 
g.add_edge(0, 2, 15) 
g.add_edge(1, 2, 5) 
g.add_edge(1, 3, 20) 
g.add_edge(2, 3, 30) 

g.bfs(0)
g.dfs(0)

print("\n--- 4. Optimal Path & Utility Planning ---")
g.dijkstra(0)
g.kruskal()

print("\n--- 5. Expression Tree for Energy Bill ---")
expr_root = ExpressionNode('+')
expr_root.left = ExpressionNode('*')
expr_root.left.left = ExpressionNode('50') 
expr_root.left.right = ExpressionNode('10')
expr_root.right = ExpressionNode('100') 

bill = evaluate_expression(expr_root)
print("Energy Bill Calculation (50 * 10) + 100 =", bill)