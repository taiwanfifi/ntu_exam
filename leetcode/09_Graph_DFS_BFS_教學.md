# 09 Graph DFS & BFS 教學講義

> **適用對象**：基礎較弱、準備 Google 面試的初學者
> **搭配檔案**：`09_Graph_DFS_BFS.py`（可執行的 Python 程式碼）
> **教學風格**：每個概念至少 2 個完整範例，附 ASCII 圖解 + step-by-step 追蹤

---

## 第一章：圖的基礎 — 從零開始

### 1.1 什麼是圖 (Graph)？

**圖 (Graph)** = **節點 (Nodes / Vertices)** + **邊 (Edges)**

你可以把圖想成「城市 + 道路」：
- 每個城市是一個 **node（節點）**
- 每條道路是一條 **edge（邊）**

```
    最簡單的圖：3 個節點，2 條邊

         A ---- B
         |
         C

    Nodes = {A, B, C}
    Edges = {(A,B), (A,C)}
```

**圖 vs 陣列 vs 鏈結串列**：
- Array：元素排成一列，用 index 存取
- Linked List：每個節點指向下一個
- **Graph：每個節點可以連到「任意數量」的其他節點！** 這就是圖強大的地方

---

### 1.2 有向 vs 無向 (Directed vs Undirected)

#### 無向圖 (Undirected Graph)

邊沒有方向，A 到 B 跟 B 到 A 是一樣的。就像**雙向道路**。

```
    無向圖 (Undirected)

      0 ---- 1
      |      |
      3 ---- 2

    邊: (0,1), (1,2), (2,3), (3,0)
    0 可以走到 1，1 也可以走到 0
```

#### 有向圖 (Directed Graph)

邊有方向！A->B 不代表 B->A。就像**單行道**。

```
    有向圖 (Directed)

      0 ----> 1
      |       |
      v       v
      3 ----> 2

    邊: (0,1), (0,3), (1,2), (3,2)
    0 可以走到 1，但 1 不能直接走到 0！
```

**面試關鍵**：看到 "undirected" 就要在 adjacency list 裡**兩邊都加**。

---

### 1.3 加權 vs 無權 (Weighted vs Unweighted)

```
    無權圖 (Unweighted)         加權圖 (Weighted)

      A --- B                    A --5-- B
      |     |                    |       |
      C --- D                   3       2
                                 |       |
                                 C --7-- D

    所有邊的「成本」相同            每條邊有不同的「成本/距離/權重」
```

- **Unweighted**：BFS 直接找最短路徑（邊數最少 = 最短）
- **Weighted**：需要 Dijkstra 等演算法（見 `11_Graph_Shortest_Path.py`）
- 本篇（第 09 章）專注在 **unweighted** 的情況

---

### 1.4 環 vs 無環 (Cycle vs Acyclic)

```
    有環 (Cyclic)              無環 (Acyclic / DAG)

      0 --- 1                    0 ---> 1
      |     |                    |      |
      3 --- 2                    v      v
                                 3      2
    可以從 0 走回 0：
    0→1→2→3→0 (一個環！)         沒有辦法從任何點走回自己
```

- **DAG** = Directed Acyclic Graph（有向無環圖），在 Topological Sort 中超重要
- **偵測環 (Cycle Detection)** 是面試經典題型（DFS + visited 狀態）

---

### 1.5 三種圖的表示法

面試中，你需要知道三種表示法，但 **90% 的時間用 Adjacency List**。

#### 表示法一：鄰接表 Adjacency List（最常用！）

用一個 dictionary（或 array of lists），key = 節點，value = 鄰居列表。

```python
# 無向圖:
#   0 --- 1
#   |     |
#   3 --- 2

graph = {
    0: [1, 3],
    1: [0, 2],
    2: [1, 3],
    3: [2, 0]
}
```

**優點**：空間 O(V+E)，列出鄰居 O(degree)，面試最常用
**缺點**：查「邊 (u,v) 是否存在？」要 O(degree)

#### 表示法二：鄰接矩陣 Adjacency Matrix

用一個 V x V 的 2D 陣列，`matrix[i][j] = 1` 表示 i 到 j 有邊。

```python
# 同一張無向圖:
#   0 --- 1
#   |     |
#   3 --- 2

matrix = [
    #  0  1  2  3
    [0, 1, 0, 1],  # 0 的鄰居: 1, 3
    [1, 0, 1, 0],  # 1 的鄰居: 0, 2
    [0, 1, 0, 1],  # 2 的鄰居: 1, 3
    [1, 0, 1, 0],  # 3 的鄰居: 0, 2
]
```

**優點**：查邊 O(1)
**缺點**：空間 O(V^2)，稀疏圖（sparse graph）很浪費

#### 表示法三：邊列表 Edge List

把所有邊存成一個 list。

```python
# 同一張圖
edges = [[0,1], [0,3], [1,2], [2,3]]
```

**優點**：空間 O(E)，輸入格式常見
**缺點**：查鄰居要掃整個 list O(E)，面試中通常需要先轉成 adjacency list

---

### 1.6 如何從 Edge List 建 Adjacency List（面試必備！）

這是面試的第一步：拿到 edges，先建圖。

```python
from collections import defaultdict

def build_graph(n, edges, directed=False):
    """
    n: 節點數量 (0 到 n-1)
    edges: [[u, v], [u, v], ...] 邊列表
    directed: True=有向, False=無向
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)  # 無向圖：雙向都加！
    return graph
```

**範例 1：無向圖**

```
輸入: n=4, edges=[[0,1],[1,2],[2,3],[0,3]]

建圖過程:
  處理 [0,1]: graph[0].append(1), graph[1].append(0)
  處理 [1,2]: graph[1].append(2), graph[2].append(1)
  處理 [2,3]: graph[2].append(3), graph[3].append(2)
  處理 [0,3]: graph[0].append(3), graph[3].append(0)

結果:
  graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [2, 0]}

圖長這樣:
    0 ---- 1
    |      |
    3 ---- 2
```

**範例 2：有向圖**

```
輸入: n=4, edges=[[0,1],[0,2],[1,3],[2,3]], directed=True

建圖過程:
  處理 [0,1]: graph[0].append(1)        (只加單向！)
  處理 [0,2]: graph[0].append(2)
  處理 [1,3]: graph[1].append(3)
  處理 [2,3]: graph[2].append(3)

結果:
  graph = {0: [1, 2], 1: [3], 2: [3]}
  注意：3 沒有出邊，所以 graph[3] = []

圖長這樣:
    0 ----> 1
    |       |
    v       v
    2 ----> 3
```

---

### 1.7 Graph vs Tree：樹是圖的特例

```
    Tree（樹）                    Graph（圖）
    ─────────                    ──────────
    - 連通 (connected)           - 可以不連通
    - 無環 (acyclic)             - 可以有環
    - V 個節點有 V-1 條邊         - 邊數任意
    - 任意兩點間恰好一條路徑       - 可以有多條路徑
    - 有根節點 (root)             - 沒有特定起點
    - 不需要 visited set          - 一定需要 visited set！

    Tree:                        Graph:
        1                         1 --- 2
       / \                        |   / |
      2   3                       |  /  |
     / \                          | /   |
    4   5                         3 --- 4
                                  (有環: 1→2→3→1)
```

**核心差異**：在 Tree 上做 DFS/BFS，不需要 visited（因為沒有環）。但在 **Graph 上一定要用 visited set**，否則會無窮迴圈！

---

## 第二章：Graph DFS — 深度優先搜尋

### 2.0 DFS on Graph vs DFS on Tree

```
    Tree DFS:                       Graph DFS:
    不需要 visited                    必須有 visited set！
    因為 tree 沒有環                   因為 graph 可能有環

    def dfs_tree(node):              def dfs_graph(node, visited):
        if not node:                     if node in visited:
            return                           return
        # process node                  visited.add(node)
        dfs_tree(node.left)              # process node
        dfs_tree(node.right)             for neighbor in graph[node]:
                                             dfs_graph(neighbor, visited)
```

**為什麼需要 visited？看這個例子：**

```
    Graph:  0 --- 1
            |     |
            3 --- 2

    如果沒有 visited，從 0 出發：
    dfs(0) → dfs(1) → dfs(0) → dfs(1) → ... 無窮迴圈！

    有了 visited：
    dfs(0): visited={0}, 走鄰居 1, 3
      dfs(1): visited={0,1}, 走鄰居 0(已visited,跳過), 2
        dfs(2): visited={0,1,2}, 走鄰居 1(skip), 3
          dfs(3): visited={0,1,2,3}, 走鄰居 2(skip), 0(skip)
    結束！每個節點只走一次。
```

---

### 2.0.1 DFS 模板：遞迴版 (Recursive)

```python
def dfs_recursive(graph, start):
    """
    graph: adjacency list, e.g. {0: [1,2], 1: [0,3], ...}
    start: 起始節點
    """
    visited = set()

    def dfs(node):
        visited.add(node)
        print(f"  訪問 {node}")       # 在這裡處理節點
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return visited
```

### 2.0.2 DFS 模板：迭代版 (Iterative with Stack)

```python
def dfs_iterative(graph, start):
    """用 stack 模擬遞迴"""
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()           # LIFO: 後進先出
        if node in visited:
            continue
        visited.add(node)
        print(f"  訪問 {node}")
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return visited
```

**注意**：迭代版的訪問順序可能跟遞迴版不同（因為 stack pop 的順序），但都是合法的 DFS。

---

### 2.0.3 時間複雜度：O(V + E)

```
為什麼是 O(V + E)？

V = 節點數, E = 邊數

- 每個節點最多被訪問 1 次（因為 visited set）→ O(V)
- 每條邊最多被檢查 2 次（無向圖: u→v 和 v→u）→ O(E)
- 總計: O(V + E)

空間複雜度:
- visited set: O(V)
- 遞迴版的 call stack: 最壞 O(V)（一條鏈）
- 總計: O(V)
```

---

### 2.1 Number of Islands (LeetCode 200) — 面試最經典圖題

**題目**：給一個 m x n 的 2D grid，'1' 代表陸地，'0' 代表水。計算有幾個島嶼（island）。相連的 '1' 算同一個島。

**核心觀念**：Grid = 隱性的圖 (Implicit Graph)

```
每個 cell 是一個 node
每個 cell 的上下左右鄰居就是 edges（最多 4 條）

    (0,0) -- (0,1) -- (0,2)
      |        |        |
    (1,0) -- (1,1) -- (1,2)
      |        |        |
    (2,0) -- (2,1) -- (2,2)
```

**策略**：
1. 掃描整個 grid
2. 遇到 '1' 就 island_count += 1
3. 從這個 '1' 開始 DFS，把所有相連的 '1' 都標記為已訪問（改成 '0'）
4. 繼續掃描找下一個未訪問的 '1'

```python
def numIslands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        # 邊界檢查 + 是否是陸地
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'    # 標記為已訪問（沉島！）
        dfs(r + 1, c)        # 下
        dfs(r - 1, c)        # 上
        dfs(r, c + 1)        # 右
        dfs(r, c - 1)        # 左

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1   # 找到新島嶼！
                dfs(r, c)    # 把整個島沉掉

    return count
```

#### 範例 1：完整追蹤

```
輸入 grid:
    1 1 0 0 0
    1 1 0 0 0
    0 0 1 0 0
    0 0 0 1 1

初始: count = 0

=== 掃描 (0,0): grid[0][0]='1' → count=1, 開始 DFS ===

DFS(0,0): 改成'0', 往下→DFS(1,0), 往右→DFS(0,1)
  DFS(1,0): 改成'0', 往右→DFS(1,1)
    DFS(1,1): 改成'0', 往上→DFS(0,1)
      DFS(0,1): 改成'0', 鄰居都是'0'或已訪問
    其他鄰居都是水或已訪問

DFS 結束後 grid:
    0 0 0 0 0     ← 第一座島 (4 cells) 全部「沉掉」
    0 0 0 0 0
    0 0 1 0 0
    0 0 0 1 1

=== 掃描 (2,2): grid[2][2]='1' → count=2, DFS 把它沉掉 ===

    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0     ← 第二座島 (1 cell) 沉了
    0 0 0 1 1

=== 掃描 (3,3): grid[3][3]='1' → count=3, DFS 沉掉 (3,3) 和 (3,4) ===

答案: count = 3 (三座島)
```

#### 範例 2：只有一座大島

```
輸入 grid:        DFS 從 (0,0) 開始，像水蔓延把 9 個 cell 全部沉掉
    1 1 1         掃描剩餘: 全部都是'0'，不會再 count++
    1 1 1
    1 1 1         答案: count = 1
```

#### Corner Cases

```
Case 1: 全是水        Case 2: 單一 cell      Case 3: 棋盤格
  0 0 0                  1                     1 0 1
  0 0 0                                        0 1 0
  0 0 0                answer = 1              1 0 1
  answer = 0                                   answer = 5
```

**複雜度**：
- Time: O(M * N) — 每個 cell 最多被訪問一次
- Space: O(M * N) — 遞迴深度最壞情況（全是陸地時）

---

### 2.2 Clone Graph (LeetCode 133)

**題目**：給一個 undirected graph 的某個節點 reference，回傳整個圖的 **deep copy**（深拷貝）。

**節點定義**：

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []
```

**核心觀念**：DFS + HashMap（old node -> new node 映射）

```
為什麼需要 HashMap？

    原圖:  1 --- 2       如果不用 HashMap:
           |     |       clone(1) → 建 new1, 走鄰居 2
           4 --- 3       clone(2) → 建 new2, 走鄰居 1
                         clone(1) → 又建一個 new1?? 重複了！

    用 HashMap:
    old_to_new = {
        original_node_1: cloned_node_1,
        original_node_2: cloned_node_2,
        ...
    }
    遇到已經在 HashMap 裡的節點 → 直接回傳 cloned 版本
```

```python
def cloneGraph(node):
    if not node:
        return None

    old_to_new = {}  # old node → new node

    def dfs(node):
        if node in old_to_new:
            return old_to_new[node]  # 已經 clone 過了！

        # 建新節點（先不加 neighbors）
        clone = Node(node.val)
        old_to_new[node] = clone     # 馬上記錄！防止無窮迴圈

        # 遞迴 clone 所有 neighbors
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)
```

#### 範例 1：4 個節點的環

```
原圖:                        clone 的圖:
    1 ---- 2                     c1 ---- c2
    |      |                     |       |
    4 ---- 3                     c4 ---- c3

=== DFS 追蹤 ===

dfs(1): 建 clone1, old_to_new={1:c1}, 走鄰居 [2,4]
  ├─ dfs(2): 建 clone2, old_to_new={1:c1, 2:c2}, 走鄰居 [1,3]
  │   ├─ dfs(1): 已在 map → return c1 ✓ (不會重複建!)
  │   └─ dfs(3): 建 clone3, 走鄰居 [2,4]
  │       ├─ dfs(2): 已在 map → return c2 ✓
  │       └─ dfs(4): 建 clone4, 走鄰居 [1,3]
  │           ├─ dfs(1): return c1 ✓
  │           └─ dfs(3): return c3 ✓
  │           c4.neighbors = [c1, c3]
  │       c3.neighbors = [c2, c4]
  │   c2.neighbors = [c1, c3]
  └─ dfs(4): 已在 map → return c4 ✓
  c1.neighbors = [c2, c4]

結構完全一樣，但是全新的節點物件！
```

#### 範例 2：只有一個節點

```
原圖:
    1 (沒有 neighbors)

dfs(1):
  1 不在 old_to_new → 建 clone1(val=1)
  old_to_new = {1: clone1}
  neighbors = [] → 不走任何鄰居
  clone1.neighbors = []
  return clone1

答案: clone1 (val=1, neighbors=[])
```

**複雜度**：
- Time: O(V + E) — 每個節點和邊各訪問一次
- Space: O(V) — HashMap + recursion stack

---

### 2.3 All Paths From Source to Target (LeetCode 797)

**題目**：給一個 DAG（有向無環圖），找出從 node 0 到 node n-1 的**所有路徑**。

**核心觀念**：DFS + Backtracking

```
因為是 DAG（無環），所以：
1. 不需要 visited set！（不會走回頭路造成無窮迴圈）
2. 同一個節點可以被不同路徑經過
3. 用 backtracking: 加入 → 探索 → 移除
```

```python
def allPathsSourceTarget(graph):
    """
    graph: adjacency list, graph[i] = list of nodes reachable from i
    例如 graph = [[1,2],[3],[3],[]] 表示:
      0 → 1, 2
      1 → 3
      2 → 3
      3 → (沒有出邊)
    """
    result = []
    target = len(graph) - 1

    def dfs(node, path):
        if node == target:
            result.append(path[:])   # 找到一條完整路徑！記得 copy
            return

        for neighbor in graph[node]:
            path.append(neighbor)     # 選擇
            dfs(neighbor, path)       # 探索
            path.pop()                # 撤銷選擇 (backtrack)

    dfs(0, [0])   # 從 node 0 開始，path 初始包含 0
    return result
```

#### 範例 1：graph = [[1,2],[3],[3],[]]

```
圖的結構:
    0 ----> 1
    |       |
    v       v
    2 ----> 3 (target)

    0 可以走到 1, 2
    1 可以走到 3
    2 可以走到 3
    3 沒有出邊 (target!)

=== DFS 追蹤 ===

dfs(0, [0]):
  鄰居: [1, 2]

  ├─ path=[0,1], dfs(1, [0,1]):
  │   鄰居: [3]
  │   └─ path=[0,1,3], dfs(3, [0,1,3]):
  │       node==target → result.append([0,1,3]) ✓
  │   pop → path=[0,1]
  │ pop → path=[0]
  │
  └─ path=[0,2], dfs(2, [0,2]):
      鄰居: [3]
      └─ path=[0,2,3], dfs(3, [0,2,3]):
          node==target → result.append([0,2,3]) ✓
      pop → path=[0,2]
    pop → path=[0]

答案: [[0,1,3], [0,2,3]]
```

#### 範例 2：graph = [[4,3,1],[3,2,4],[3],[4],[]]

```
圖: 0→{4,3,1}, 1→{3,2,4}, 2→{3}, 3→{4}, target=4

DFS 探索所有路徑 (backtracking):
  0→4              ✓ 到達 target
  0→3→4            ✓
  0→1→3→4          ✓
  0→1→2→3→4        ✓
  0→1→4            ✓

答案: [[0,4], [0,3,4], [0,1,3,4], [0,1,2,3,4], [0,1,4]]
```

**複雜度**：
- Time: O(2^V * V) — 最壞情況每個節點都可能在路徑中
- Space: O(V) — recursion depth

---

## 第三章：Graph BFS — 廣度優先搜尋

### 3.0 BFS 核心觀念

**BFS = 一層一層往外擴散**，就像在池塘丟石頭，波紋一圈一圈往外擴。

```
    BFS 從 node 0 開始:

    第 0 層: {0}
    第 1 層: {1, 3}         ← 0 的鄰居
    第 2 層: {2}            ← 1,3 的鄰居（排除已訪問的）

        0          Layer 0
       / \
      1   3        Layer 1
       \ /
        2          Layer 2
```

**超級重要**：BFS 在 **unweighted graph** 上自動找到最短路徑！
因為 BFS 是一層一層往外走的，第一次到達某個節點的時候，走的步數就是最少的。

### 3.0.1 BFS 模板

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()       # FIFO: 先進先出
        print(f"  訪問 {node}")
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # 加入 queue 時就標記！
                queue.append(neighbor)
```

**關鍵細節**：
- 用 `deque`，不要用 list（list.pop(0) 是 O(n)，deque.popleft() 是 O(1)）
- 在**加入 queue 時**就標記 visited，不是在 pop 出來時。否則同一個節點可能被加入多次

### 3.0.2 BFS 模板（帶層數追蹤）

```python
def bfs_with_level(graph, start):
    visited = set([start])
    queue = deque([start])
    level = 0

    while queue:
        size = len(queue)                    # 當前這一層有幾個節點
        print(f"Layer {level}: ", end="")
        for _ in range(size):                # 只處理這一層
            node = queue.popleft()
            print(f"{node} ", end="")
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        print()
        level += 1
```

---

### 3.1 Rotting Oranges (LeetCode 994) — Multi-source BFS

**題目**：一個 grid 裡有新鮮橘子 (1) 和腐爛橘子 (2)。每分鐘，腐爛橘子會讓上下左右的新鮮橘子也腐爛。問：最少幾分鐘所有橘子都腐爛？如果有橘子永遠不會腐爛，回傳 -1。

**核心觀念**：Multi-source BFS（多源 BFS）

```
普通 BFS: 從 1 個起點開始擴散
Multi-source BFS: 從「多個起點」同時開始擴散！

就像「火災」：如果多個地方同時起火，火焰從所有起火點同時往外擴散。
在這題：所有腐爛橘子同時開始「感染」。
```

```python
def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # Step 1: 找出所有腐爛橘子 (起點) + 計算新鮮橘子數量
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))    # 所有腐爛橘子都是起點！
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0   # 沒有新鮮橘子，不需要等

    minutes = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # 上下左右

    # Step 2: BFS — 每一層 = 1 分鐘
    while queue:
        size = len(queue)
        infected = False
        for _ in range(size):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2       # 感染！
                    fresh_count -= 1
                    queue.append((nr, nc))
                    infected = True
        if infected:
            minutes += 1

    return minutes if fresh_count == 0 else -1
```

#### 範例 1：完整追蹤

```
輸入 grid:         初始: queue=[(0,0)], fresh=6
    2 1 1
    1 1 0
    0 1 1

t=0→1: (0,0) 感染右(0,1)和下(1,0)    fresh=4
     2  2  1
     2  1  0
     0  1  1

t=1→2: (0,1)感染右(0,2)和下(1,1), (1,0)鄰居已感染或=0    fresh=2
     2  2  2
     2  2  0
     0  1  1

t=2→3: (1,1) 感染下(2,1)    fresh=1
     2  2  2
     2  2  0
     0  2  1

t=3→4: (2,1) 感染右(2,2)    fresh=0
     2  2  2
     2  2  0
     0  2  2

fresh_count=0 → 答案: 4 分鐘
```

#### 範例 2：有橘子無法被感染

```
輸入 grid:
    2 1 1
    0 1 1
    1 0 1

初始: queue=[(0,0)], fresh_count=6

t=0→1: (0,0) 感染 (0,1), (可能感染 (1,0)=0 跳過)
t=1→2: (0,1) 感染 (0,2), (1,1)
t=2→3: (0,2) 無新鮮鄰居, (1,1) 感染 (1,2)
t=3→4: (1,2) 感染 (2,2)

    最終 grid:
     2  2  2
     0  2  2
     1  0  2
              ↑
    (2,0) 的值是 1，但它被 0 包圍，永遠不會被感染！

fresh_count = 1 (還有 1 個新鮮的)

答案: -1 (不可能全部腐爛)
```

**複雜度**：
- Time: O(M * N) — 每個 cell 最多進出 queue 一次
- Space: O(M * N) — queue 最壞裝所有 cell

---

### 3.2 Word Ladder (LeetCode 127) — Google Hard 經典

**題目**：給 beginWord, endWord, 和一個 wordList。每次只能改一個字母，且改後的字必須在 wordList 中。問從 beginWord 變到 endWord 最少要幾步？

**核心觀念**：每個 word 是一個 node，差一個字母的 word 之間有 edge。BFS 找最短路徑！

```
為什麼這是圖的問題？

    "hit" → "hot" → "dot" → "dog" → "cog"

    每個 word 是一個 node
    如果兩個 word 只差 1 個字母 → 它們之間有一條 edge
    BFS 找最短路徑 = 最少轉換次數
```

```python
def ladderLength(beginWord, endWord, wordList):
    wordSet = set(wordList)
    if endWord not in wordSet:
        return 0

    queue = deque([(beginWord, 1)])   # (word, step)
    visited = set([beginWord])

    while queue:
        word, step = queue.popleft()

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word == endWord:
                    return step + 1
                if new_word in wordSet and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, step + 1))

    return 0  # 無法到達
```

#### 範例 1："hit" -> "cog"

```
beginWord = "hit", endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]

隱性的圖 (差 1 個字母的 word 之間有邊):
    hit --- hot --- dot --- dog --- cog
             |       |              |
             +--- lot --- log ------+

=== BFS 逐層追蹤 ===

Layer 1: ["hit"]
  "hit" → 改每個位置試 a~z → 找到 "hot" (在 wordSet)

Layer 2: ["hot"]
  "hot" → 找到 "dot", "lot"

Layer 3: ["dot", "lot"]
  "dot" → 找到 "dog"
  "lot" → 找到 "log"

Layer 4: ["dog", "log"]
  "dog" → 改第 0 位試到 'c' → "cog" == endWord!
  return step=4+1 = 5

答案: 5,  路徑: hit → hot → dot → dog → cog
```

#### 範例 2：無法到達

```
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]   ← 沒有 "cog"！

wordSet 裡沒有 endWord → 直接 return 0

答案: 0
```

**為什麼用 BFS 不用 DFS？**

```
BFS 保證找到最短路徑！
DFS 可能先走一條很長的路才到 endWord。

    hit → hot → dot → dog → cog   (BFS: 5 步)
    hit → hot → lot → log → cog   (DFS 可能先走這條，也是 5 步)
    但如果圖更複雜，DFS 可能走 10 步才到
```

**複雜度**：
- Time: O(M^2 * N)，M = word length, N = wordList size
- Space: O(M * N)

---

### 3.3 Shortest Path in Binary Matrix (LeetCode 1091)

**題目**：在 n x n 的 binary grid 中，找從左上角 (0,0) 到右下角 (n-1,n-1) 的最短路徑。可以走 **8 個方向**（包括對角線）。只能走 0 的格子，回傳路徑長度。

**核心觀念**：8-directional BFS

```
普通 grid BFS: 4 方向 (上下左右)
這題: 8 方向！多了 4 個對角線

    ↖  ↑  ↗
     \ | /
    ← [X] →
     / | \
    ↙  ↓  ↘
```

```python
def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1    # 起點或終點被擋住

    directions = [
        (-1,-1), (-1,0), (-1,1),
        (0,-1),          (0,1),
        (1,-1),  (1,0),  (1,1)
    ]

    queue = deque([(0, 0, 1)])   # (row, col, path_length)
    grid[0][0] = 1               # 標記已訪問（把 0 改成 1）

    while queue:
        r, c, dist = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist          # BFS 第一次到達 = 最短！

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1       # 標記已訪問
                queue.append((nr, nc, dist + 1))

    return -1  # 到不了
```

#### 範例 1：有路徑

```
輸入 grid:       n=3, 起點(0,0), 終點(2,2)
    0 0 0
    1 1 0
    1 1 0

=== BFS 追蹤 (8方向) ===

pop(0,0,dist=1): 右鄰(0,1)=0 加入(dist=2), 其他鄰居=1或超出
pop(0,1,dist=2): 右(0,2)=0 加入(dist=3), 右下(1,2)=0 加入(dist=3)
pop(0,2,dist=3): 鄰居都已訪問/超出
pop(1,2,dist=3): 下(2,2)=0 加入(dist=4)
pop(2,2,dist=4): 到達終點！ return 4

路徑: (0,0) → (0,1) → (1,2) → (2,2)
    S  →  .         答案: 4
    1  1  ↓
    1  1  E
```

#### 範例 2：沒有路徑

```
輸入 grid:
    0 1 0
    1 1 0
    0 0 0

    S  1  0
    1  1  0
    0  0  E

從 (0,0) 出發，8 方向鄰居全是 1 或超出邊界！
queue 馬上變空。

答案: -1 (起點被牆壁包圍)
```

**複雜度**：
- Time: O(N^2) — 每個 cell 最多進出 queue 一次
- Space: O(N^2) — queue 最壞裝所有 cell

---

## 第四章：Grid DFS/BFS 特殊技巧

### 4.1 Surrounded Regions (LeetCode 130)

**題目**：給一個 m x n 的 board，包含 'X' 和 'O'。把所有被 'X' **完全包圍**的 'O' 翻成 'X'。邊界上的 'O'（以及與邊界 'O' 相連的 'O'）不翻。

**核心觀念**：反向思考！

```
直覺思考: 找被包圍的 O → 很難判斷！

反向思考:
  1. 從邊界上的 O 開始 DFS/BFS
  2. 標記所有「與邊界相連的 O」為安全 (用 'S' 標記)
  3. 掃描整個 board:
     - 'O' → 改成 'X'（這些是被包圍的！）
     - 'S' → 改回 'O'（這些跟邊界相連，不被包圍）
```

```python
def solve(board):
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'S'    # 標記為安全 (Safe)
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    # Step 1: 從四個邊界開始 DFS
    for r in range(rows):
        dfs(r, 0)            # 左邊界
        dfs(r, cols - 1)     # 右邊界
    for c in range(cols):
        dfs(0, c)            # 上邊界
        dfs(rows - 1, c)     # 下邊界

    # Step 2: 翻轉
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'    # 被包圍的 O → X
            elif board[r][c] == 'S':
                board[r][c] = 'O'    # 安全的 S → 改回 O
```

#### 範例 1：有被包圍的 O

```
輸入:                    Step 1: 邊界 DFS         Step 2: 翻轉
    X X X X              X X X X                   X X X X
    X O O X     →        X O O X          →        X X X X  ← 被包圍→X
    X X O X              X X O X                   X X X X
    X O X X              X S X X                   X O X X  ← S改回O

只有 (3,1) 是邊界上的 O → DFS 標為 'S'
(3,1) 的鄰居全是 X → 只標記了 1 個 'S'
中間的 O: (1,1),(1,2),(2,2) 沒跟邊界連 → 翻成 X
```

#### 範例 2：O 與邊界相連

```
輸入:               DFS from 邊界(0,1):      翻轉後:
    X O X X         X S X X                   X O X X
    X O O X    →    X S S X         →         X O O X
    X X O X         X X S X                   X X O X
    X X X X         X X X X                   X X X X

(0,1) 是邊界 O → DFS: (0,1)→(1,1)→(1,2)→(2,2) 全標 'S'
所有 O 都跟邊界相連 → 全部改回 'O'，沒有任何翻轉！
```

**複雜度**：
- Time: O(M * N)
- Space: O(M * N) — DFS recursion stack

---

### 4.2 Pacific Atlantic Water Flow (LeetCode 417)

**題目**：給一個 m x n 的高度矩陣 `heights`。水可以從高處流向低處（或等高）的四方向鄰居。左邊和上邊是太平洋 (Pacific)，右邊和下邊是大西洋 (Atlantic)。找出所有**同時能流到太平洋和大西洋**的格子。

**核心觀念**：反向！從海洋出發，往「上坡」走

```
正向思考: 從每個 cell 出發，看能不能流到兩個海洋 → O(M*N * M*N) 太慢！

反向思考:
  1. 從太平洋邊界出發，BFS/DFS 往上坡走 → 能到的 = 能流到太平洋的
  2. 從大西洋邊界出發，BFS/DFS 往上坡走 → 能到的 = 能流到大西洋的
  3. 取交集 = 同時能流到兩邊的！

為什麼要「往上坡走」？
  因為我們是反向的！原本水是從高往低流到海洋。
  反向就是從海洋（低處）往高處回溯。
```

```
Pacific (太平洋) — 碰到上邊和左邊

  ~ ~ ~ ~ ~
  ~ 1 2 2 3 (5) ~
  ~ 3 2 3 (4)(4) ~          ← 括號 = 能流到 Atlantic
  ~ 2 4 5 3 1 ~
  ~ (6)(7)(1)(4)(5) ~
  ~ ~ ~ ~ ~

Atlantic (大西洋) — 碰到下邊和右邊
```

```python
def pacificAtlantic(heights):
    if not heights:
        return []

    rows, cols = len(heights), len(heights[0])
    pacific = set()    # 能流到太平洋的 cells
    atlantic = set()   # 能流到大西洋的 cells

    def dfs(r, c, reachable, prev_height):
        if (r, c) in reachable:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if heights[r][c] < prev_height:  # 只能往上坡走（反向）
            return

        reachable.add((r, c))
        curr = heights[r][c]
        dfs(r+1, c, reachable, curr)
        dfs(r-1, c, reachable, curr)
        dfs(r, c+1, reachable, curr)
        dfs(r, c-1, reachable, curr)

    # 從太平洋邊界出發 (上邊 + 左邊)
    for c in range(cols):
        dfs(0, c, pacific, 0)        # 上邊 (row=0)
    for r in range(rows):
        dfs(r, 0, pacific, 0)        # 左邊 (col=0)

    # 從大西洋邊界出發 (下邊 + 右邊)
    for c in range(cols):
        dfs(rows-1, c, atlantic, 0)  # 下邊
    for r in range(rows):
        dfs(r, cols-1, atlantic, 0)  # 右邊

    # 取交集
    return list(pacific & atlantic)
```

#### 範例：完整追蹤

```
heights:
    1 2 2 3 5       P = 能流到 Pacific
    3 2 3 4 4       A = 能流到 Atlantic
    2 4 5 3 1       B = 能流到 Both (答案)
    6 7 1 4 5

Pacific (從上邊+左邊 DFS 往上坡走):
    P P P P P       從 (0,0)=1 往上坡: (0,1)=2,(1,0)=3...
    P P P P P       從 (2,0)=2 往上坡: (3,0)=6,(3,1)=7...
    P P P . .       高處的 cell 容易流到左上的太平洋
    P P . . .

Atlantic (從下邊+右邊 DFS 往上坡走):
    . . . . A       從 (3,4)=5, (3,0)=6 等邊界往上坡走
    . . . A A       高處的 cell 容易流到右下的大西洋
    . . A . .
    A A A A A

交集 (Pacific ∩ Atlantic):
    . . . . B       (0,4)
    . . . B B       (1,3), (1,4)
    . . B . .       (2,2)
    B B . . .       (3,0), (3,1)

答案: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1]]
```

**複雜度**：
- Time: O(M * N) — 每個 cell 最多被兩次 DFS 各訪問一次
- Space: O(M * N) — pacific set + atlantic set

---

## 第五章：DFS vs BFS 在圖上的選擇

### 5.1 什麼時候用 BFS？

```
BFS 適用場景:
┌─────────────────────────────────────────────────────┐
│ 1. 最短路徑 (Shortest Path) — unweighted graph     │
│    → Word Ladder, Shortest Path in Binary Matrix    │
│                                                     │
│ 2. 最近的 XX (Nearest something)                    │
│    → Nearest exit, nearest 0 in matrix              │
│                                                     │
│ 3. Level-order / 層序遍歷                            │
│    → Rotting Oranges (每分鐘 = 一層)                 │
│                                                     │
│ 4. Multi-source BFS                                 │
│    → 多個起點同時擴散                                 │
└─────────────────────────────────────────────────────┘
```

### 5.2 什麼時候用 DFS？

```
DFS 適用場景:
┌─────────────────────────────────────────────────────┐
│ 1. 連通性 (Connectivity)                            │
│    → Number of Islands, Connected Components        │
│                                                     │
│ 2. 所有路徑 (All Paths)                              │
│    → All Paths Source to Target                     │
│                                                     │
│ 3. 環偵測 (Cycle Detection)                          │
│    → Course Schedule (用 DFS 的三色標記法)            │
│                                                     │
│ 4. Topological Sort                                 │
│    → 見 10_Graph_TopSort_UnionFind.py               │
│                                                     │
│ 5. 反向標記 (Boundary DFS)                           │
│    → Surrounded Regions, Pacific Atlantic           │
└─────────────────────────────────────────────────────┘
```

### 5.3 Multi-source BFS 概念整理

```
普通 BFS:
  queue = [起點]
  一個點開始往外擴散

Multi-source BFS:
  queue = [起點1, 起點2, 起點3, ...]
  多個點同時往外擴散！

經典題目:
  - Rotting Oranges: 所有腐爛橘子同時擴散
  - Walls and Gates: 所有 gate 同時往外填最短距離
  - 01 Matrix: 所有 0 同時往外找最近距離

觀念:
  把所有起點一起丟進 queue，之後就跟普通 BFS 一模一樣！
  這是因為：多源 BFS 其實等於加一個「虛擬起點」連到所有真正的起點。
```

### 5.4 時間/空間複雜度比較

```
┌──────────┬───────────────┬──────────────────────────┐
│          │ Time          │ Space                    │
├──────────┼───────────────┼──────────────────────────┤
│ DFS      │ O(V + E)      │ O(V) recursion stack     │
│          │               │ (最壞=一條鏈)             │
├──────────┼───────────────┼──────────────────────────┤
│ BFS      │ O(V + E)      │ O(V) queue               │
│          │               │ (最壞=所有節點同一層)      │
├──────────┼───────────────┼──────────────────────────┤
│ Grid DFS │ O(M * N)      │ O(M * N) recursion stack │
├──────────┼───────────────┼──────────────────────────┤
│ Grid BFS │ O(M * N)      │ O(M * N) queue           │
└──────────┴───────────────┴──────────────────────────┘

兩者時間一樣！差別在:
  - DFS 用 stack (recursion or explicit)
  - BFS 用 queue (deque)
  - DFS 空間取決於「深度」
  - BFS 空間取決於「寬度」(最寬的一層)
```

### 5.5 面試速查表：看到什麼關鍵字 → 用什麼

```
┌──────────────────────────────┬──────────────────┐
│ 關鍵字 / 題型                 │ 選擇             │
├──────────────────────────────┼──────────────────┤
│ "shortest path" (unweighted) │ BFS              │
│ "minimum steps"              │ BFS              │
│ "nearest / closest"          │ BFS              │
│ "level by level"             │ BFS              │
│ "simultaneously / spread"    │ Multi-source BFS │
├──────────────────────────────┼──────────────────┤
│ "find all paths"             │ DFS+Backtracking │
│ "connected components"       │ DFS or BFS       │
│ "number of islands"          │ DFS or BFS       │
│ "cycle detection"            │ DFS              │
│ "topological order"          │ DFS or BFS(Kahn) │
│ "surrounded / border"        │ DFS from border  │
│ "can reach from X"           │ DFS or BFS       │
├──────────────────────────────┼──────────────────┤
│ "shortest path" (weighted)   │ Dijkstra (見 11) │
│ "minimum spanning tree"      │ Prim / Kruskal   │
└──────────────────────────────┴──────────────────┘
```

---

## 附錄：常見錯誤與面試提醒

### A. Graph 常見錯誤 Top 5

```
錯誤 1: 忘了 visited set → 無窮迴圈
  修正: Graph DFS/BFS 一定要有 visited！

錯誤 2: BFS 用 list 而非 deque
  list.pop(0) = O(n), deque.popleft() = O(1)
  修正: from collections import deque

錯誤 3: BFS 在 pop 時才標 visited，而非加入 queue 時
  這會導致同一個節點被加入 queue 多次
  修正: 在 queue.append() 之前就 visited.add()

錯誤 4: 無向圖只加了一個方向的邊
  修正: graph[u].append(v) AND graph[v].append(u)

錯誤 5: Grid 問題忘了邊界檢查
  修正: if 0 <= r < rows and 0 <= c < cols
```

### B. 面試時的 Grid 方向模板

```python
# 4 方向 (上下左右)
directions_4 = [(0,1), (0,-1), (1,0), (-1,0)]

# 8 方向 (含對角線)
directions_8 = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),          (0,1),
    (1,-1),  (1,0),  (1,1)
]

# 使用方式:
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # process (nr, nc)
```

### C. 面試溝通技巧

```
1. 看到 Graph 題，先問面試官:
   - "Is this directed or undirected?"
   - "Can there be cycles?"
   - "Is the graph connected?"
   - "How is the graph represented? Edge list or adjacency list?"

2. 寫 code 前先說策略:
   - "I'll use BFS because we need the shortest path in an unweighted graph."
   - "I'll use DFS from the border to mark safe cells, then flip the rest."

3. 分析複雜度:
   - "Time is O(V+E) because we visit each node once and check each edge once."
   - "For grid problems, V = M*N and E = 4*M*N, so it's O(M*N)."
```

---

## 本章學習路徑建議

```
Day 1: 第一章 (圖的基礎) + 第二章 2.0 (DFS 模板)
       → 動手建圖: edge list → adjacency list
       → 自己在紙上跑一次 DFS

Day 2: 2.1 Number of Islands
       → 在 LeetCode 上 AC 後，試試 BFS 版本
       → Corner cases: 空 grid, 全 1, 全 0

Day 3: 2.2 Clone Graph + 2.3 All Paths
       → Clone Graph 的 HashMap 技巧很重要
       → All Paths 練習 backtracking on DAG

Day 4: 第三章 3.0 (BFS 模板) + 3.1 Rotting Oranges
       → 理解 multi-source BFS 的概念
       → 手動追蹤 grid 每一輪的變化

Day 5: 3.2 Word Ladder + 3.3 Shortest Path in Binary Matrix
       → Word Ladder 是 Google 經典！要能在 25 分鐘內寫出
       → 8 方向 BFS 要熟練

Day 6: 第四章 Surrounded Regions + Pacific Atlantic
       → 反向思考 (從邊界出發) 是重要的 pattern
       → 要能解釋為什麼反向更高效

Day 7: 第五章 總整理 + 複習
       → 做 DFS vs BFS 的選擇練習
       → 不看 code，自己重寫每道題
```
