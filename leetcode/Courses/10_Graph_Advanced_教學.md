# 10 — Graph 進階：拓撲排序 + 並查集 + 最短路徑 教學講義

> **適用對象**：LeetCode 初學者，準備 Google 面試
> **前置知識**：09_Graph_DFS_BFS.py（Graph 基礎 — DFS / BFS）
> **教學風格**：每個概念至少 2 個 step-by-step 數值 trace，用「跑一次給你看」取代抽象描述
> **語言**：Traditional Chinese + English 技術術語
> **配套程式碼**：`10_Graph_TopSort_UnionFind.py`

---

## 目錄

- [第一章：拓撲排序 Topological Sort — 有向無環圖 DAG](#第一章拓撲排序-topological-sort--有向無環圖-dag)
  - [1.1 Course Schedule (LC 207)](#11-course-schedule-lc-207)
  - [1.2 Course Schedule II (LC 210)](#12-course-schedule-ii-lc-210)
  - [1.3 Alien Dictionary (LC 269)](#13-alien-dictionary-lc-269--google-經典)
- [第二章：Union-Find 並查集 — 從零開始](#第二章union-find-並查集--從零開始)
  - [2.1 手動 Trace parent 陣列](#21-手動-trace-parent-陣列)
  - [2.2 Number of Connected Components (LC 323)](#22-number-of-connected-components-lc-323)
  - [2.3 Redundant Connection (LC 684)](#23-redundant-connection-lc-684)
  - [2.4 Accounts Merge (LC 721)](#24-accounts-merge-lc-721--google-高頻)
- [第三章：最短路徑 Shortest Path](#第三章最短路徑-shortest-path)
  - [3.1 Network Delay Time (LC 743)](#31-network-delay-time-lc-743)
  - [3.2 Cheapest Flights Within K Stops (LC 787)](#32-cheapest-flights-within-k-stops-lc-787)
  - [Bellman-Ford 演算法](#bellman-ford-演算法--可處理負權重)
- [第四章：三種算法比較 — 決策樹](#第四章三種算法比較--決策樹)

---

## 第一章：拓撲排序 Topological Sort — 有向無環圖 DAG

### 什麼是拓撲排序？

**Topological Sort** = 將 DAG (Directed Acyclic Graph, 有向無環圖) 的所有節點排成一條線，使得**對於每一條邊 u -> v，u 都排在 v 前面**。

**生活比喻**：

```
想像大學選課：
  「資料結構」需要先修「程式設計」
  「演算法」需要先修「資料結構」和「離散數學」

  程式設計 → 資料結構 → 演算法
  離散數學 ──────────↗

  合法的修課順序 (拓撲序):
    程式設計 → 離散數學 → 資料結構 → 演算法    (OK)
    離散數學 → 程式設計 → 資料結構 → 演算法    (OK)
    資料結構 → 程式設計 → ...                   (WRONG! 資料結構排在程式設計前面)
```

**重要前提：只有 DAG 才有拓撲排序。如果圖有環 (cycle)，就不可能排出來。**

---

### BFS 方法 — Kahn's Algorithm

Kahn's Algorithm 是面試最常用的拓撲排序方法，用 BFS 思維，非常直覺。

**核心觀念：indegree (入度)**

- indegree = 有多少條邊指向該節點
- indegree = 0 的節點 = 沒有前置條件，可以先處理

**演算法步驟**：

```
Step 1: 計算每個節點的 indegree
Step 2: 把所有 indegree = 0 的節點放入 queue
Step 3: 從 queue 取出一個節點 u
        - 把 u 加入結果
        - 把 u 的所有鄰居的 indegree - 1
        - 如果有鄰居 indegree 變成 0，加入 queue
Step 4: 重複 Step 3 直到 queue 空
Step 5: 如果結果包含所有節點 → 合法拓撲序
        如果結果不包含所有節點 → 有環!
```

**Python 模板**：

```python
from collections import defaultdict, deque

def topological_sort_bfs(num_nodes, edges):
    """
    edges[i] = [a, b] 表示 b → a (b 是 a 的前置)
    回傳拓撲排序結果，如果有環回傳 []
    """
    # Step 1: 建圖 + 計算 indegree
    graph = defaultdict(list)
    indegree = [0] * num_nodes

    for a, b in edges:
        graph[b].append(a)   # b → a
        indegree[a] += 1

    # Step 2: indegree=0 的放入 queue
    queue = deque()
    for i in range(num_nodes):
        if indegree[i] == 0:
            queue.append(i)

    # Step 3-4: BFS
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # Step 5: 檢查
    if len(order) == num_nodes:
        return order      # 合法拓撲序
    else:
        return []          # 有環!
```

**時間複雜度**: O(V + E)，每個節點和邊各處理一次
**空間複雜度**: O(V + E)，圖 + queue

---

### 1.1 Course Schedule (LC 207)

> **題意**：有 `numCourses` 門課，`prerequisites[i] = [a, b]` 表示修 a 之前必須先修 b。
> 判斷能否修完所有課程。（本質：有向圖有沒有環？）

#### Example 1：無環，可以修完

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

先修關係:
  修課 1 前要先修 0  →  0 → 1
  修課 2 前要先修 0  →  0 → 2
  修課 3 前要先修 1  →  1 → 3
  修課 3 前要先修 2  →  2 → 3

畫圖:
        0
       / \
      v   v
      1   2
       \ /
        v
        3
```

**Step-by-step trace**：

```
Step 1: 建圖 + 計算 indegree
  graph = {0: [1, 2], 1: [3], 2: [3]}
  indegree = [0, 1, 1, 2]
               ↑  ↑  ↑  ↑
               0  1  2  3

  節點 0: 沒有邊指向它 → indegree = 0
  節點 1: 邊 0→1        → indegree = 1
  節點 2: 邊 0→2        → indegree = 1
  節點 3: 邊 1→3, 2→3   → indegree = 2

Step 2: indegree = 0 的放入 queue
  queue = [0]

Step 3: BFS 開始

  === Iteration 1 ===
  取出 node = 0
  count = 1
  處理鄰居:
    鄰居 1: indegree[1] = 1 - 1 = 0 → 加入 queue
    鄰居 2: indegree[2] = 1 - 1 = 0 → 加入 queue
  indegree = [0, 0, 0, 2]
  queue = [1, 2]

  === Iteration 2 ===
  取出 node = 1
  count = 2
  處理鄰居:
    鄰居 3: indegree[3] = 2 - 1 = 1 → 不加入 queue (還不是 0)
  indegree = [0, 0, 0, 1]
  queue = [2]

  === Iteration 3 ===
  取出 node = 2
  count = 3
  處理鄰居:
    鄰居 3: indegree[3] = 1 - 1 = 0 → 加入 queue
  indegree = [0, 0, 0, 0]
  queue = [3]

  === Iteration 4 ===
  取出 node = 3
  count = 4
  鄰居: 無
  queue = []

Step 5: count = 4 == numCourses = 4 → 可以修完!

Output: True
```

#### Example 2：有環，無法修完

```
Input: numCourses = 3, prerequisites = [[0,1],[1,2],[2,0]]

先修關係:
  修 0 前要修 1 → 1 → 0
  修 1 前要修 2 → 2 → 1
  修 2 前要修 0 → 0 → 2

畫圖:
  0 → 2 → 1 → 0    (三角環!)
```

**Step-by-step trace**：

```
Step 1: 建圖 + 計算 indegree
  graph = {1: [0], 2: [1], 0: [2]}
  indegree = [1, 1, 1]

  每個節點都有 1 條邊指向它!

Step 2: indegree = 0 的放入 queue
  queue = []   (沒有 indegree = 0 的節點!)

Step 3: BFS
  queue 是空的，直接結束。
  count = 0

Step 5: count = 0 != numCourses = 3 → 有環! 無法修完!

Output: False
```

**為什麼有環就排不出來？**
環裡的每個節點都互相依賴，indegree 永遠不會變成 0。就像 A 等 B、B 等 C、C 等 A，誰都沒辦法先開始。

#### Corner Cases

- **沒有先修條件**: `prerequisites = []` → 所有 indegree 都是 0 → 全部直接排完 → True
- **自我迴圈**: `prerequisites = [[0,0]]` → 課 0 要先修課 0 → indegree[0] = 1 永遠不降 → 有環 → False

---

### 1.2 Course Schedule II (LC 210)

> **題意**：和 207 一樣的設定，但要**回傳一個合法的修課順序**。如果有環，回傳空陣列。

這題的解法和 207 完全一樣，只是多一步：把 BFS 過程中取出的節點**按順序記錄下來**。

#### Example 1：有合法順序

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]

（同 1.1 Example 1 的圖）
        0
       / \
      v   v
      1   2
       \ /
        v
        3
```

**Step-by-step trace**（只列關鍵部分）：

```
indegree = [0, 1, 1, 2]
queue = [0]

Iteration 1: pop 0 → order = [0]
  鄰居 1: indegree 1→0, 加入 queue
  鄰居 2: indegree 1→0, 加入 queue
  queue = [1, 2]

Iteration 2: pop 1 → order = [0, 1]
  鄰居 3: indegree 2→1
  queue = [2]

Iteration 3: pop 2 → order = [0, 1, 2]
  鄰居 3: indegree 1→0, 加入 queue
  queue = [3]

Iteration 4: pop 3 → order = [0, 1, 2, 3]
  queue = []

len(order) = 4 == numCourses = 4

Output: [0, 1, 2, 3]
```

注意：拓撲排序的結果**不唯一**。`[0, 2, 1, 3]` 也是合法答案（因為 1 和 2 之間沒有先後關係）。

#### Example 2：三條獨立鏈

```
Input: numCourses = 6, prerequisites = [[1,0],[3,2],[5,4]]

圖: 0→1, 2→3, 4→5  (三條獨立的鏈)

indegree = [0, 1, 0, 1, 0, 1]

queue = [0, 2, 4]  (三個 indegree=0 的起點)

Iteration 1: pop 0 → order = [0], 鄰居 1 indegree→0, queue = [2, 4, 1]
Iteration 2: pop 2 → order = [0, 2], 鄰居 3 indegree→0, queue = [4, 1, 3]
Iteration 3: pop 4 → order = [0, 2, 4], 鄰居 5 indegree→0, queue = [1, 3, 5]
Iteration 4: pop 1 → order = [0, 2, 4, 1]
Iteration 5: pop 3 → order = [0, 2, 4, 1, 3]
Iteration 6: pop 5 → order = [0, 2, 4, 1, 3, 5]

Output: [0, 2, 4, 1, 3, 5]
```

---

### 1.3 Alien Dictionary (LC 269) — Google 經典

> **題意**：給定一組按照**外星字母順序**排序的單字，推導出字母的順序。

這題是 Google 面試的經典題，核心思路是：**從排序過的單字中提取字母間的先後關係 → 建立有向圖 → 拓撲排序**。

**如何提取字母順序？** 比較相鄰的兩個單字，找到**第一個不同的字母**：

```
words = ["wrt", "wrf"]
比較:  w = w (一樣，跳過)
       r = r (一樣，跳過)
       t ≠ f → 得到邊: t → f (t 排在 f 前面)
```

#### Example 1：完整推導

```
Input: words = ["wrt", "wrf", "er", "ett", "rftt"]

Step 1: 比較相鄰單字，提取邊

  "wrt" vs "wrf":
    w=w ✓, r=r ✓, t≠f → 邊: t → f

  "wrf" vs "er":
    w≠e → 邊: w → e

  "er" vs "ett":
    e=e ✓, r≠t → 邊: r → t

  "ett" vs "rftt":
    e≠r → 邊: e → r

Step 2: 收集所有字母
  all_chars = {w, r, t, f, e}

Step 3: 建圖
  graph = {t: [f], w: [e], r: [t], e: [r]}

  畫出來:
    w → e → r → t → f

Step 4: 計算 indegree
  w: 0  (沒有邊指向 w)
  e: 1  (w → e)
  r: 1  (e → r)
  t: 1  (r → t)
  f: 1  (t → f)

  indegree = {w:0, e:1, r:1, t:1, f:1}

Step 5: Kahn's BFS
  queue = [w]  (indegree = 0)

  Iteration 1: pop 'w' → result = "w"
    鄰居 'e': indegree 1→0, 加入 queue
    queue = [e]

  Iteration 2: pop 'e' → result = "we"
    鄰居 'r': indegree 1→0, 加入 queue
    queue = [r]

  Iteration 3: pop 'r' → result = "wer"
    鄰居 't': indegree 1→0, 加入 queue
    queue = [t]

  Iteration 4: pop 't' → result = "wert"
    鄰居 'f': indegree 1→0, 加入 queue
    queue = [f]

  Iteration 5: pop 'f' → result = "wertf"
    queue = []

  len(result) = 5 == len(all_chars) = 5

Output: "wertf"
```

#### Example 2：含無效輸入

```
Input: words = ["abc", "ab"]

比較 "abc" vs "ab":
  "abc" 比 "ab" 長，但 "ab" 是 "abc" 的 prefix。
  在合法的字典序中，短的一定在長的前面（像英文字典 "ab" < "abc"）。
  但這裡 "abc" 排在 "ab" 前面 → 矛盾!

Output: ""  (無效的輸入)
```

**面試注意事項**：

1. 一定要處理 prefix 矛盾的情況
2. 只看**第一個不同的字母**就 break，後面的字母不提供資訊
3. 可能有多個合法答案（拓撲序不唯一），回傳任一個都可以

---

## 第二章：Union-Find 並查集 — 從零開始

### 什麼問題需要 Union-Find？

Union-Find 解決的核心問題是：**「A 和 B 是否在同一組？」**

```
生活比喻：
  想像你在管理社群：
  - 一開始每個人都是獨立的
  - 有人告訴你「小明和小華是朋友」→ 把他們合併成一組
  - 又有人說「小華和小美是朋友」→ 小美也加入那一組
  - 現在問你「小明和小美是朋友嗎？」→ 是! 因為同一組
```

### 兩個基本操作

| 操作 | 功能 | 比喻 |
|------|------|------|
| `find(x)` | 找 x 屬於哪一組（回傳代表元素/root） | 「小明的組長是誰？」 |
| `union(x, y)` | 合併 x 和 y 所在的組 | 「小明和小華的組合併」 |

### 從零開始建構

#### 第 1 步：Naive 版本 — parent 陣列

```
每個節點有一個 parent（父節點）。
初始時，每個人的 parent 是自己（自己是自己的組長）。

parent = [0, 1, 2, 3, 4]   ← 5 個節點，各自獨立
          ↑  ↑  ↑  ↑  ↑
          0  1  2  3  4

find(x): 沿著 parent 一路往上找，直到找到 root (parent[root] == root)
union(x, y): 把 x 的 root 接到 y 的 root 下面
```

#### 第 2 步：Path Compression 路徑壓縮

**問題**：如果樹很深，find 每次都要走很長的路。

```
最糟情況（退化成鏈表）:
  0 ← 1 ← 2 ← 3 ← 4
  find(4) 要走 4 步!

路徑壓縮的想法：
  find 的時候，順便把路上的節點全部直接指向 root。

  find(4):
    原本: 4 → 3 → 2 → 1 → 0 (root)
    壓縮後:
         0  (root)
       / | \ \
      1  2  3  4     ← 全部直接指向 root!

  下次 find(4) 只需 1 步!
```

**程式碼**：

```python
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])  # 遞迴壓縮
    return self.parent[x]
```

#### 第 3 步：Union by Rank 按秩合併

**問題**：union 時如果總是把 A 接到 B 下面，可能產生很高的樹。

```
不好的 union:
  union(0,1): 把 0 接到 1 下面 → 高度 2
  union(2,1): 把 2 接到 1 下面 → 高度 2
  union(3,0): 把 3 接到 0 下面 → 高度 3!

        1
       / \
      0   2
      |
      3         ← 越來越高

好的 union (按秩):
  記錄每棵樹的「秩」(rank，大約等於高度)。
  union 時把矮的樹接到高的樹下面。

  union(0,1): rank 相同，0→1, rank[1]++
  union(2,1): rank[2]=0 < rank[1]=1, 2→1
  union(3,1): rank[3]=0 < rank[1]=1, 3→1

        1         ← 高度始終是 2!
      / | \
      0  2  3
```

**程式碼**：

```python
def union(self, x, y):
    root_x = self.find(x)
    root_y = self.find(y)

    if root_x == root_y:
        return False  # 已經同一組

    # Union by Rank: 矮的接到高的下面
    if self.rank[root_x] < self.rank[root_y]:
        self.parent[root_x] = root_y
    elif self.rank[root_x] > self.rank[root_y]:
        self.parent[root_y] = root_x
    else:
        self.parent[root_y] = root_x
        self.rank[root_x] += 1

    self.count -= 1  # 連通分量數 -1
    return True
```

#### 為什麼 Path Compression + Union by Rank 給出 O(alpha(n)) 約等於 O(1)?

```
alpha(n) 是反阿克曼函數 (Inverse Ackermann Function)。
對於任何實際可能的 n（即使 n = 宇宙中的原子數），alpha(n) <= 5。
所以在面試中，可以直接說 Union-Find 的 find/union 是 O(1) amortized。
```

---

### 完整 Union-Find Class 模板

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # 每個節點的父節點
        self.rank = [0] * n           # 秩
        self.count = n                # 連通分量數

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

---

### 2.1 手動 Trace parent 陣列

#### Example 1：基本操作 trace

```
初始: 5 個節點 (0~4)
parent = [0, 1, 2, 3, 4]    ← 每個人都是自己的 root
rank   = [0, 0, 0, 0, 0]
count  = 5                   ← 5 個連通分量

--- union(0, 1) ---
  find(0) = 0, find(1) = 1
  root_0 = 0, root_1 = 1
  rank[0] = 0 == rank[1] = 0 → 1 接到 0 下面, rank[0]++

  parent = [0, 0, 2, 3, 4]
                ↑
                1 的 parent 從 1 變成 0
  rank   = [1, 0, 0, 0, 0]
  count  = 4

  樹的樣子:
    0    2    3    4
    |
    1

--- union(2, 3) ---
  find(2) = 2, find(3) = 3
  rank[2] = 0 == rank[3] = 0 → 3 接到 2 下面, rank[2]++

  parent = [0, 0, 2, 2, 4]
                      ↑
                      3 的 parent 從 3 變成 2
  rank   = [1, 0, 1, 0, 0]
  count  = 3

  樹的樣子:
    0    2    4
    |    |
    1    3

--- union(0, 2) --- 合併兩個小組
  find(0) = 0, find(2) = 2
  rank[0] = 1 == rank[2] = 1 → 2 接到 0 下面, rank[0]++

  parent = [0, 0, 0, 2, 4]
                   ↑
                   2 的 parent 從 2 變成 0
  rank   = [2, 0, 1, 0, 0]
  count  = 2

  樹的樣子:
      0        4
     / \
    1   2
        |
        3

--- find(3) --- 路徑壓縮
  find(3):
    parent[3] = 2, 不是 root → 遞迴 find(2)
      find(2):
        parent[2] = 0, 不是 root → 遞迴 find(0)
          find(0):
            parent[0] = 0, 是 root → 回傳 0
        parent[2] = 0 (壓縮: 2 直接指向 0)
        回傳 0
    parent[3] = 0 (壓縮: 3 直接指向 0)
    回傳 0

  壓縮前:              壓縮後:
      0        4           0          4
     / \                / | \
    1   2              1   2   3
        |
        3

  parent = [0, 0, 0, 0, 4]    ← 3 從指向 2 變成直接指向 0

--- connected(1, 3) ---
  find(1) = 0, find(3) = 0 → 相同 → True! (同組)

--- connected(1, 4) ---
  find(1) = 0, find(4) = 4 → 不同 → False! (不同組)
```

#### Example 2：較大範例，展示路徑壓縮效果

```
初始: 6 個節點 (0~5)
parent = [0, 1, 2, 3, 4, 5]
rank   = [0, 0, 0, 0, 0, 0]

--- 依序做 union(1,0), union(2,1), union(3,2), union(4,3) ---

union(1,0): 0→1 下面, rank[1]++
  parent = [1, 1, 2, 3, 4, 5], rank = [0, 1, 0, 0, 0, 0]

union(2,1): rank[2]=0 < rank[1]=1, 2→1
  parent = [1, 1, 1, 3, 4, 5], rank = [0, 1, 0, 0, 0, 0]

union(3,2): find(3)=3, find(2)=1. rank[3]=0 < rank[1]=1, 3→1
  parent = [1, 1, 1, 1, 4, 5], rank = [0, 1, 0, 0, 0, 0]

union(4,3): find(4)=4, find(3)=1. rank[4]=0 < rank[1]=1, 4→1
  parent = [1, 1, 1, 1, 1, 5], rank = [0, 1, 0, 0, 0, 0]

  樹:       1          5
          / | \ \
         0  2  3  4

--- union(5,0) ---
  find(5) = 5
  find(0): parent[0]=1, parent[1]=1 → root=1. 壓縮: parent[0]=1 (已是)
  find(0) = 1
  rank[5]=0 < rank[1]=1 → 5→1

  parent = [1, 1, 1, 1, 1, 1]     ← 全部指向 1!
  count = 1

  所有節點都在同一組，find 都是 O(1)。
```

---

### 2.2 Number of Connected Components (LC 323)

> **題意**：有 n 個節點和一些邊，計算無向圖中**連通分量的數量**。

#### Example 1

```
Input: n = 5, edges = [[0,1],[1,2],[3,4]]

圖:
  0 - 1 - 2     3 - 4

  兩個連通分量: {0,1,2} 和 {3,4}
```

**Step-by-step trace**：

```
初始: parent = [0,1,2,3,4], count = 5

--- 處理邊 (0,1) ---
  union(0,1): find(0)=0, find(1)=1
  rank 相同 → 1 接到 0 下面, rank[0]++
  parent = [0, 0, 2, 3, 4], count = 4

--- 處理邊 (1,2) ---
  union(1,2): find(1)=0, find(2)=2
  rank[0]=1 > rank[2]=0 → 2 接到 0 下面
  parent = [0, 0, 0, 3, 4], count = 3

--- 處理邊 (3,4) ---
  union(3,4): find(3)=3, find(4)=4
  rank 相同 → 4 接到 3 下面, rank[3]++
  parent = [0, 0, 0, 3, 3], count = 2

最終 count = 2

Output: 2
```

#### Example 2：全部相連

```
Input: n = 4, edges = [[0,1],[1,2],[2,3]]

--- union(0,1) → count = 3
--- union(1,2): find(1)=0, find(2)=2 → union(0,2) → count = 2
--- union(2,3): find(2)=0, find(3)=3 → union(0,3) → count = 1

Output: 1
```

**程式碼**：

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count
```

---

### 2.3 Redundant Connection (LC 684)

> **題意**：一棵 n 個節點的樹，多加了一條邊變成有環。找出那條多餘的邊。
> 如果有多個答案，回傳最後出現的那條。

**核心觀念**：依序加邊，如果 `union` 回傳 `False`（兩個節點已經在同一組），代表這條邊會形成環 → 這就是多餘的邊!

#### Example 1

```
Input: edges = [[1,2],[1,3],[2,3]]

樹: 1-2, 1-3
多餘邊: 2-3 (加了就有環)

圖:
    1
   / \
  2 - 3    ← 2-3 是多餘的
```

**Step-by-step trace**：

```
初始: parent = [0,1,2,3], count = 3  (節點從 1 開始，分配 n+1 空間)

--- 加邊 (1,2) ---
  union(1,2): find(1)=1, find(2)=2
  不同組 → 合併! 2 接到 1 下面
  parent = [0, 1, 1, 3]

--- 加邊 (1,3) ---
  union(1,3): find(1)=1, find(3)=3
  不同組 → 合併! 3 接到 1 下面
  parent = [0, 1, 1, 1]

--- 加邊 (2,3) ---
  union(2,3): find(2)=1, find(3)=1
  同一組!! → 這條邊是多餘的!

Output: [2, 3]
```

#### Example 2

```
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]

--- 加邊 (1,2) ---
  union(1,2): 不同組 → 合併
  parent = [0, 1, 1, 3, 4, 5]

--- 加邊 (2,3) ---
  union(2,3): find(2)=1, find(3)=3 → 不同 → 合併
  parent = [0, 1, 1, 1, 4, 5]

--- 加邊 (3,4) ---
  union(3,4): find(3)=1, find(4)=4 → 不同 → 合併
  parent = [0, 1, 1, 1, 1, 5]

--- 加邊 (1,4) ---
  union(1,4): find(1)=1, find(4)=1 → 同組!! 多餘的邊!

Output: [1, 4]

(邊 [1,5] 還沒處理到就找到答案了，但演算法是依序處理所有邊，
 找到第一條造成環的邊即回傳)
```

---

### 2.4 Accounts Merge (LC 721) — Google 高頻

> **題意**：有一組帳號，每個帳號是 `[name, email1, email2, ...]`。
> 如果兩個帳號有相同的 email，合併它們。回傳合併後的帳號。

**思路**：

```
1. 每個 email 分配一個 ID
2. 同一個帳號裡的 email 全部 union (它們屬於同一個人)
3. 用 find 把同組的 email 收集在一起
4. 排序後輸出
```

#### Example：詳細 trace

```
Input:
  accounts = [
    ["John", "john1@mail.com", "john_ai@mail.com"],    ← 帳號 0
    ["John", "john2@mail.com"],                         ← 帳號 1
    ["John", "john1@mail.com", "john2@mail.com"],       ← 帳號 2
    ["Mary", "mary@mail.com"]                           ← 帳號 3
  ]

Step 1: 分配 email ID
  john1@mail.com   → ID 0
  john_ai@mail.com → ID 1
  john2@mail.com   → ID 2
  mary@mail.com    → ID 3

Step 2: 同帳號的 email 做 union

  帳號 0: ["John", "john1@mail.com", "john_ai@mail.com"]
    union(ID0, ID1) → union(0, 1)
    parent = [0, 0, 2, 3]   ← 1 接到 0

  帳號 1: ["John", "john2@mail.com"]
    只有一個 email，不需要 union

  帳號 2: ["John", "john1@mail.com", "john2@mail.com"]
    union(ID0, ID2) → union(0, 2)
    find(0) = 0, find(2) = 2 → 不同組 → 合併!
    parent = [0, 0, 0, 3]   ← 2 也接到 0

  帳號 3: ["Mary", "mary@mail.com"]
    只有一個 email，不需要 union

Step 3: 用 find 收集同組

  john1@mail.com  (ID 0): find(0) = 0 → 組 0
  john_ai@mail.com (ID 1): find(1) = 0 → 組 0
  john2@mail.com  (ID 2): find(2) = 0 → 組 0
  mary@mail.com   (ID 3): find(3) = 3 → 組 3

  組 0: [john1@mail.com, john_ai@mail.com, john2@mail.com]
  組 3: [mary@mail.com]

Step 4: 排序 + 加上名字

Output:
  ["John", "john1@mail.com", "john2@mail.com", "john_ai@mail.com"]
  ["Mary", "mary@mail.com"]
```

**重點觀察**：

- 帳號 0 和帳號 2 都有 `john1@mail.com` → 它們的 email 會被 union 在一起
- 帳號 1 有 `john2@mail.com`，帳號 2 也有 `john2@mail.com` → 也被合併
- 結果：三個 John 帳號全部合併成一個!

---

## 第三章：最短路徑 Shortest Path

### Dijkstra's Algorithm — 加權圖最短路徑

**適用條件：所有邊的權重 >= 0 (非負)**

**核心觀念**：

```
Dijkstra = 「貪心」找最短路徑
  1. 維護一個 distance 表：dist[node] = 從起點到 node 的目前已知最短距離
  2. 初始: dist[start] = 0, 其餘 = INF
  3. 用 min-heap 每次取出距離最小的未拜訪節點
  4. 對它的鄰居做 relaxation (嘗試更新更短的距離)
  5. 重複直到 heap 空
```

**什麼是 Relaxation?**

```
如果 dist[u] + weight(u,v) < dist[v]:
    dist[v] = dist[u] + weight(u,v)    ← 找到更短的路!
```

**Python 模板**：

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start, n):
    """
    graph = {node: [(neighbor, weight), ...]}
    回傳 dist dict: {node: shortest_distance}
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0
    visited = set()
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph.get(u, []):
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist
```

**時間複雜度**: O((V + E) log V)  (用 min-heap)
**空間複雜度**: O(V + E)

#### Dijkstra Trace Example 1：5 個節點

```
圖:
  0 --4--> 1
  0 --1--> 2
  2 --2--> 1
  1 --1--> 3
  2 --5--> 3
  3 --3--> 4

  graph = {
    0: [(1,4), (2,1)],
    2: [(1,2), (3,5)],
    1: [(3,1)],
    3: [(4,3)]
  }
  start = 0
```

**Step-by-step trace**：

```
初始:
  dist = {0:0, 1:INF, 2:INF, 3:INF, 4:INF}
  visited = {}
  heap = [(0, 0)]

=== Pop (dist=0, node=0) ===
  visited = {0}
  鄰居:
    node 1: 0 + 4 = 4 < INF → dist[1] = 4, push(4,1)
    node 2: 0 + 1 = 1 < INF → dist[2] = 1, push(1,2)
  dist = {0:0, 1:4, 2:1, 3:INF, 4:INF}
  heap = [(1,2), (4,1)]

=== Pop (dist=1, node=2) ===
  visited = {0, 2}
  鄰居:
    node 1: 1 + 2 = 3 < 4 → dist[1] = 3, push(3,1)    ← 更短的路!
    node 3: 1 + 5 = 6 < INF → dist[3] = 6, push(6,3)
  dist = {0:0, 1:3, 2:1, 3:6, 4:INF}
  heap = [(3,1), (4,1), (6,3)]

=== Pop (dist=3, node=1) ===
  visited = {0, 2, 1}
  鄰居:
    node 3: 3 + 1 = 4 < 6 → dist[3] = 4, push(4,3)    ← 又更短!
  dist = {0:0, 1:3, 2:1, 3:4, 4:INF}
  heap = [(4,1), (4,3), (6,3)]

=== Pop (dist=4, node=1) ===
  node 1 already visited → skip

=== Pop (dist=4, node=3) ===
  visited = {0, 2, 1, 3}
  鄰居:
    node 4: 4 + 3 = 7 < INF → dist[4] = 7, push(7,4)
  dist = {0:0, 1:3, 2:1, 3:4, 4:7}
  heap = [(6,3), (7,4)]

=== Pop (dist=6, node=3) ===
  node 3 already visited → skip

=== Pop (dist=7, node=4) ===
  visited = {0, 2, 1, 3, 4}
  無鄰居

heap 空，結束!

最終 dist = {0:0, 1:3, 2:1, 3:4, 4:7}

最短路徑:
  0→0: 0 (自己)
  0→1: 3 (0→2→1, 走 1+2=3, 比直走 0→1 的 4 更短!)
  0→2: 1 (直走)
  0→3: 4 (0→2→1→3, 走 1+2+1=4)
  0→4: 7 (0→2→1→3→4, 走 1+2+1+3=7)
```

#### Dijkstra Trace Example 2：4 個節點

```
圖:
  0 --1--> 1
  0 --4--> 2
  1 --2--> 2
  1 --6--> 3
  2 --3--> 3

  start = 0

初始: dist = {0:0, 1:INF, 2:INF, 3:INF}
      heap = [(0,0)]

Pop (0, 0): visited={0}
  → dist[1] = 0+1 = 1
  → dist[2] = 0+4 = 4
  dist = {0:0, 1:1, 2:4, 3:INF}
  heap = [(1,1), (4,2)]

Pop (1, 1): visited={0,1}
  → dist[2] = min(4, 1+2=3) = 3   ← 更短!
  → dist[3] = 1+6 = 7
  dist = {0:0, 1:1, 2:3, 3:7}
  heap = [(3,2), (4,2), (7,3)]

Pop (3, 2): visited={0,1,2}
  → dist[3] = min(7, 3+3=6) = 6   ← 更短!
  dist = {0:0, 1:1, 2:3, 3:6}
  heap = [(4,2), (6,3), (7,3)]

Pop (4, 2): visited, skip
Pop (6, 3): visited={0,1,2,3}
Pop (7, 3): visited, skip

最終 dist = {0:0, 1:1, 2:3, 3:6}

最短路徑 0→3: 0→1→2→3 (1+2+3=6), 比 0→1→3 (1+6=7) 更短
```

---

### 3.1 Network Delay Time (LC 743)

> **題意**：有 n 個網路節點，`times[i] = [u, v, w]` 表示從 u 到 v 傳輸花費 w 時間。
> 從節點 k 發出信號，回傳所有節點收到信號的最短時間。如果有節點收不到，回傳 -1。

**本質**：Dijkstra 求單源最短路徑，答案 = max(所有最短距離)。

#### Example 1

```
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2

圖 (節點從 1 開始):
  2 --1--> 1
  2 --1--> 3
  3 --1--> 4

      2
     / \
    v   v
    1   3
        |
        v
        4

start = 2
```

**Step-by-step trace**：

```
初始: dist = {1:INF, 2:0, 3:INF, 4:INF}
      heap = [(0, 2)]

Pop (0, 2): visited={2}
  → dist[1] = 0+1 = 1
  → dist[3] = 0+1 = 1
  dist = {1:1, 2:0, 3:1, 4:INF}
  heap = [(1,1), (1,3)]

Pop (1, 1): visited={2,1}
  無鄰居
  heap = [(1,3)]

Pop (1, 3): visited={2,1,3}
  → dist[4] = 1+1 = 2
  dist = {1:1, 2:0, 3:1, 4:2}
  heap = [(2,4)]

Pop (2, 4): visited={2,1,3,4}
  無鄰居

所有節點都有到達 → max(dist) = max(0,1,1,2) = 2

Output: 2
```

#### Example 2：有節點不可達

```
Input: times = [[1,2,1]], n = 2, k = 2

圖: 1 --1--> 2  (只有 1→2 的邊)
start = 2

dist = {1:INF, 2:0}

Pop (0, 2): visited={2}
  無鄰居 (2 沒有出邊)

dist[1] = INF → 節點 1 收不到信號!

Output: -1
```

---

### 3.2 Cheapest Flights Within K Stops (LC 787)

> **題意**：有 n 個城市和航班 `flights[i] = [from, to, price]`。
> 找從 src 到 dst 最便宜的航班，**最多經過 k 個中轉站**。

**為什麼不能直接用 Dijkstra？** 因為有「最多 k 個中轉」的限制。Dijkstra 只關心最短距離，不管經過幾個站。

**方法：Modified Bellman-Ford**

```
k 個中轉 = 最多 k+1 條邊
做 k+1 輪 relaxation，每輪對所有邊做更新。
重要：每輪要用「上一輪的 dist」來更新，避免連鎖反應。
```

#### Example 1

```
Input: n=4, flights=[[0,1,100],[1,2,100],[2,3,100],[0,3,500]]
       src=0, dst=3, k=1

圖:
  0 --100--> 1 --100--> 2 --100--> 3
  0 ----------500----------> 3

  路線選擇:
    直飛 0→3: cost=500, 0 個中轉 (OK)
    0→1→2→3: cost=300, 2 個中轉 (超過 k=1!)
    0→1→3: 不存在此邊

  k=1 只能最多 1 個中轉站 (= 最多 2 條邊)
```

**Step-by-step trace**：

```
初始: dist = [0, INF, INF, INF]

=== Round 0 (第 1 條邊) ===
  用 prev_dist = [0, INF, INF, INF] 做更新

  邊 (0→1, 100): prev[0]=0, 0+100=100 < INF → dist[1] = 100
  邊 (1→2, 100): prev[1]=INF, skip (出發點不可達)
  邊 (2→3, 100): prev[2]=INF, skip
  邊 (0→3, 500): prev[0]=0, 0+500=500 < INF → dist[3] = 500

  Round 0 結束: dist = [0, 100, INF, 500]

=== Round 1 (第 2 條邊, 最後一輪因為 k=1) ===
  用 prev_dist = [0, 100, INF, 500] 做更新

  邊 (0→1, 100): 0+100=100 = dist[1], no update
  邊 (1→2, 100): prev[1]=100, 100+100=200 < INF → dist[2] = 200
  邊 (2→3, 100): prev[2]=INF, skip (上一輪 2 不可達!)
  邊 (0→3, 500): 0+500=500 = dist[3], no update

  Round 1 結束: dist = [0, 100, 200, 500]

  注意：雖然 dist[2]=200，但 2→3 的更新要用 prev_dist[2]=INF，
  所以 dist[3] 不會被更新成 200+100=300。
  這就是為什麼要用上一輪的 dist!

dist[3] = 500

Output: 500
```

#### Example 2：k=2 就能更便宜

```
同樣的圖, 但 k=2 (最多 2 個中轉 = 3 條邊)

=== Round 0 ===
  dist = [0, 100, INF, 500]  (同上)

=== Round 1 ===
  prev_dist = [0, 100, INF, 500]
  邊 (1→2): 100+100=200 → dist[2] = 200
  dist = [0, 100, 200, 500]

=== Round 2 (多了這一輪!) ===
  prev_dist = [0, 100, 200, 500]
  邊 (2→3): prev[2]=200, 200+100=300 < 500 → dist[3] = 300   ← 找到更便宜的!

  dist = [0, 100, 200, 300]

Output: 300  (0→1→2→3, 2 個中轉)
```

---

### Bellman-Ford 演算法 — 可處理負權重

**和 Dijkstra 的關鍵差異**：

| | Dijkstra | Bellman-Ford |
|---|---|---|
| 邊權重 | 必須 >= 0 | 可以有負權 |
| 時間複雜度 | O((V+E) log V) | O(V * E) |
| 負環偵測 | 不能 | 可以 |
| 方法 | 貪心 + min-heap | V-1 輪 relaxation |

**演算法步驟**：

```
1. dist[src] = 0, 其餘 = INF
2. 做 V-1 輪，每輪對「所有邊」做 relaxation
   (為什麼 V-1 輪? 最短路徑最多 V-1 條邊)
3. 第 V 輪如果還能更新 → 有負環 (negative cycle)!
```

#### Example：有負權邊的圖

```
5 nodes (0~4), src = 0
邊:
  0→1 (w=6), 0→2 (w=7)
  1→2 (w=8), 1→3 (w=5), 1→4 (w=-4)
  2→3 (w=-3), 2→4 (w=9)
  3→1 (w=-2)
  4→3 (w=7)

初始: dist = [0, INF, INF, INF, INF]

=== Round 1 ===
  邊 0→1: 0+6=6 < INF → dist[1]=6
  邊 0→2: 0+7=7 < INF → dist[2]=7
  邊 1→2: 6+8=14 > 7, no update
  邊 1→3: 6+5=11 < INF → dist[3]=11
  邊 1→4: 6+(-4)=2 < INF → dist[4]=2
  邊 2→3: 7+(-3)=4 < 11 → dist[3]=4
  邊 2→4: 7+9=16 > 2, no update
  邊 3→1: 4+(-2)=2 < 6 → dist[1]=2      ← 負權讓距離變更短!
  邊 4→3: 2+7=9 > 4, no update

  Round 1: dist = [0, 2, 7, 4, 2]

=== Round 2 ===
  邊 0→1: 0+6=6 > 2, no update
  邊 0→2: 0+7=7 = 7, no update
  邊 1→2: 2+8=10 > 7, no update
  邊 1→3: 2+5=7 > 4, no update
  邊 1→4: 2+(-4)=-2 < 2 → dist[4]=-2    ← 更短!
  邊 2→3: 7+(-3)=4 = 4, no update
  邊 2→4: 7+9=16 > -2, no update
  邊 3→1: 4+(-2)=2 = 2, no update
  邊 4→3: (-2)+7=5 > 4, no update

  Round 2: dist = [0, 2, 7, 4, -2]

=== Round 3 ===
  所有邊都 no update → 提前結束!

=== 負環檢查 (Round V) ===
  對所有邊再做一次 relaxation，如果還能更新 → 有負環
  這個例子沒有負環。

最終: dist = [0, 2, 7, 4, -2]

最短路徑:
  0→0: 0
  0→1: 2  (0→2→3→1, 走 7+(-3)+(-2)=2)
  0→2: 7  (直走)
  0→3: 4  (0→2→3, 走 7+(-3)=4)
  0→4: -2 (0→2→3→1→4, 走 7+(-3)+(-2)+(-4)=-2)
```

---

## 第四章：三種算法比較 — 決策樹

### 速查表

```
┌──────────────────┬──────────────────────────┬────────────────────────────────┐
│   演算法          │  適用場景                 │  關鍵判斷字眼                   │
├──────────────────┼──────────────────────────┼────────────────────────────────┤
│ Topological Sort │ 排序依賴關係的任務        │ 「順序」「先修」「依賴」        │
│ (Kahn's BFS)     │ DAG 環偵測               │ 有向圖 + 排序 or 判環          │
├──────────────────┼──────────────────────────┼────────────────────────────────┤
│ Union-Find       │ 判斷連通性 / 分組         │ 「是否相連」「分成幾組」        │
│ (並查集)          │ 找多餘的邊               │ 無向圖 + 動態加邊              │
├──────────────────┼──────────────────────────┼────────────────────────────────┤
│ Dijkstra         │ 加權最短路徑              │ 「最短距離」「最小花費」        │
│                  │ 非負權重                  │ 有權重 >= 0                    │
├──────────────────┼──────────────────────────┼────────────────────────────────┤
│ Bellman-Ford     │ 負權邊 / 限制步數         │ 「有負權」「最多 K 步」         │
└──────────────────┴──────────────────────────┴────────────────────────────────┘
```

### 面試快速判斷流程

```
題目跟圖有關?
│
├─ 有向圖?
│   ├─ 問「順序」「依賴」「有沒有環」
│   │   → Topological Sort (Kahn's BFS)
│   │   代表題: Course Schedule, Alien Dictionary
│   │
│   └─ 問「最短路徑」「最小花費」
│       ├─ 邊權重 >= 0 → Dijkstra
│       │   代表題: Network Delay Time
│       └─ 有負權 or 限制步數 → Bellman-Ford
│           代表題: Cheapest Flights Within K Stops
│
└─ 無向圖?
    ├─ 問「是否連通」「分成幾組」「合併」
    │   → Union-Find
    │   代表題: Number of Connected Components, Accounts Merge
    │
    ├─ 問「多餘的邊」「形成環的邊」
    │   → Union-Find
    │   代表題: Redundant Connection
    │
    └─ 問「最短路徑」(無權重)
        → BFS (參考 09_Graph_DFS_BFS.py)
```

### 複雜度比較

```
┌──────────────────┬─────────────────────┬───────────────┐
│   演算法          │  時間複雜度          │  空間複雜度    │
├──────────────────┼─────────────────────┼───────────────┤
│ Topological Sort │ O(V + E)            │ O(V + E)      │
│ Union-Find       │ O(E * alpha(V))     │ O(V)          │
│                  │ ≈ O(E)              │               │
│ Dijkstra         │ O((V+E) log V)      │ O(V + E)      │
│ Bellman-Ford     │ O(V * E)            │ O(V)          │
└──────────────────┴─────────────────────┴───────────────┘
```

### Google 常考題型

| 題目 | 演算法 | 難度 |
|------|--------|------|
| Course Schedule (207) | Topological Sort | Medium |
| Course Schedule II (210) | Topological Sort | Medium |
| Alien Dictionary (269) | Topological Sort | Hard |
| Number of Connected Components (323) | Union-Find | Medium |
| Redundant Connection (684) | Union-Find | Medium |
| Accounts Merge (721) | Union-Find | Medium |
| Network Delay Time (743) | Dijkstra | Medium |
| Cheapest Flights Within K Stops (787) | Bellman-Ford | Medium |

---

## 學習 Checklist

```
[ ] 拓撲排序 (Topological Sort)
    [ ] 理解 indegree 的概念
    [ ] 能手寫 Kahn's Algorithm (BFS)
    [ ] 能判斷有向圖有沒有環
    [ ] 能解 Course Schedule I/II
    [ ] 能解 Alien Dictionary (建圖 + TopSort)

[ ] Union-Find (並查集)
    [ ] 理解 parent 陣列的意義
    [ ] 能實作 find() with Path Compression
    [ ] 能實作 union() with Union by Rank
    [ ] 能手動 trace parent 陣列的變化
    [ ] 能解 Connected Components / Redundant Connection / Accounts Merge

[ ] 最短路徑 (Shortest Path)
    [ ] 理解 Dijkstra 的 relaxation 過程
    [ ] 能手動 trace distance table 的更新
    [ ] 知道 Dijkstra 不能處理負權邊
    [ ] 能解 Network Delay Time
    [ ] 理解 Bellman-Ford 的 V-1 輪 relaxation
    [ ] 知道何時用 Dijkstra vs Bellman-Ford

[ ] 三種演算法的選擇
    [ ] 看到「順序/依賴」→ TopSort
    [ ] 看到「分組/連通」→ Union-Find
    [ ] 看到「最短距離」→ Dijkstra / Bellman-Ford
```

---

> 配套程式碼：`10_Graph_TopSort_UnionFind.py`，執行 `python 10_Graph_TopSort_UnionFind.py` 可以看到所有範例的完整 trace 輸出。
