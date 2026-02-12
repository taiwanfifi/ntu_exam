# 演算法教學 05：圖論基礎 —— BFS 與 DFS

> 台大資工演算法課程教學講義
> 本講義涵蓋：觀念解說、定理推導、虛擬碼、計算範例、何時使用、常見陷阱

---

## 本章基礎觀念（零基礎必讀）

### 為什麼需要學圖論？

你每天都在跟「圖」打交道，只是可能不知道：

- **社交網路**就是一個圖：每個人是一個「節點」，如果兩個人是朋友，就在他們之間畫一條「邊」。Facebook 推薦「你可能認識的人」就是在圖上做搜尋。
- **Google 地圖**就是一個圖：每個路口是節點，每條路是邊（有長度/時間）。導航就是在圖上找最短路徑。
- **修課規劃**就是一個圖：每門課是節點，如果 A 是 B 的先修課，就畫一條從 A 到 B 的箭頭。安排修課順序就是「拓撲排序」。
- **網頁之間的超連結**就是一個圖：Google 的 PageRank 演算法就是在分析這個圖的結構。

「圖」是電腦科學中最通用的資料結構之一，很多看似不同的問題都可以轉化為圖上的問題。而 BFS 和 DFS 就是在圖上「探索」的兩種最基本方式，幾乎所有進階圖論演算法都建立在它們之上。

### 什麼是「圖」（Graph）？

一個圖就是**一群東西（節點）加上它們之間的關係（邊）**。

```
用圖表示朋友關係：

  Alice --- Bob --- Charlie
    |               |
  Diana ---------- Eve

節點（vertex/node）= 每個人
邊（edge）= 朋友關係
```

**有向圖 vs 無向圖**：
- **無向圖**：邊沒有方向。「Alice 和 Bob 是朋友」→ Alice 到 Bob 有邊，Bob 到 Alice 也有邊。
- **有向圖**：邊有方向。「Alice 追蹤 Bob 的 IG」不代表 Bob 也追蹤 Alice。

### 用同一個圖展示兩種表示法

以下面的 4 節點無向圖為例：

```
    1 --- 2
    |     |
    3 --- 4
```

邊：{1-2, 1-3, 2-4, 3-4}

**Adjacency Matrix（鄰接矩陣）**——用表格記錄「誰跟誰相連」：

```
    1  2  3  4
1 [ 0  1  1  0 ]    ← 1 跟 2、3 相連
2 [ 1  0  0  1 ]    ← 2 跟 1、4 相連
3 [ 1  0  0  1 ]    ← 3 跟 1、4 相連
4 [ 0  1  1  0 ]    ← 4 跟 2、3 相連
```

想知道「1 和 4 之間有邊嗎？」→ 查 Matrix[1][4] = 0 → 沒有！$O(1)$ 就能查到。

**Adjacency List（鄰接串列）**——用清單記錄「每個人的朋友有誰」：

```
1 → [2, 3]
2 → [1, 4]
3 → [1, 4]
4 → [2, 3]
```

想知道「1 的朋友有誰？」→ 查 List[1] = [2, 3] → 直接看到！

| 比較 | Matrix | List |
|------|--------|------|
| 空間 | $O(n^2)$，不管有幾條邊 | $O(n + m)$，邊少就省空間 |
| 查「A 和 B 有邊嗎？」 | $O(1)$ 超快 | $O(degree)$ 要掃清單 |
| 列出所有鄰居 | $O(n)$ 要掃整行 | $O(degree)$ 只看有的 |
| 適合 | 邊很多的「密集圖」 | 邊不多的「稀疏圖」（大部分情況） |

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 圖 | Graph | 一群東西加上它們的關係 | 社交網路、地圖 |
| 節點/頂點 | Vertex / Node | 圖中的「東西」 | 人、城市、網頁 |
| 邊 | Edge | 兩個節點之間的「關係」 | 朋友關係、道路 |
| 有向圖 | Directed Graph | 邊有方向（A→B 不代表 B→A） | IG 追蹤、先修課關係 |
| 無向圖 | Undirected Graph | 邊沒有方向（A-B 雙向都通） | Facebook 好友 |
| 鄰接矩陣 | Adjacency Matrix | 用二維表格記錄圖的結構 | 見上方範例 |
| 鄰接串列 | Adjacency List | 用清單記錄每個節點的鄰居 | 見上方範例 |
| 度 | Degree | 一個節點有幾條邊 | 節點 1 的 degree = 2 |
| BFS | Breadth-First Search | 廣度優先搜尋——一層一層往外擴展 | 找無權圖最短路 |
| DFS | Depth-First Search | 深度優先搜尋——一條路走到底再回頭 | 環偵測、拓撲排序 |
| 佇列 | Queue | 先進先出的資料結構（排隊） | BFS 使用 |
| 堆疊 | Stack | 後進先出的資料結構（疊盤子） | DFS 使用 |
| 拓撲排序 | Topological Sort | 有向無環圖的線性排列，箭頭都朝右 | 修課順序 |
| 強連通分量 | SCC (Strongly Connected Component) | 有向圖中互相都能到達的最大節點群 | 見第 5 節 |
| 環 | Cycle | 從某點出發走一圈能回到自己 | A→B→C→A |
| DAG | Directed Acyclic Graph | 有向無環圖 | 先修課關係（不能循環先修） |

### 前置知識

- **程式基礎**：理解 Queue（佇列）和 Stack（堆疊）的操作
  - Queue：像排隊——先排的先走（FIFO）
  - Stack：像疊盤子——最後放的最先拿（LIFO）
- **遞迴**：DFS 通常用遞迴實作
- 不需要先學 algo_01~04 的內容就能讀本章

---

## 目錄

1. [圖的表示法](#1-圖的表示法)
2. [BFS（廣度優先搜尋）](#2-bfs廣度優先搜尋)
3. [DFS（深度優先搜尋）](#3-dfs深度優先搜尋)
4. [拓撲排序](#4-拓撲排序topological-sort)
5. [強連通分量 (SCC)](#5-強連通分量scc)
6. [環偵測](#6-環偵測cycle-detection)
7. [二部圖判斷](#7-二部圖判斷bipartite-checking)
8. [無向圖 DFS 的特殊性質](#8-無向圖-dfs-的特殊性質)

---

## 1. 圖的表示法

### 1.1 基本定義

一個圖 G = (V, E)，其中 V 是頂點集合，E 是邊集合。

- **有向圖 (Directed Graph)**：邊有方向，(u, v) ≠ (v, u)
- **無向圖 (Undirected Graph)**：邊無方向，{u, v} = {v, u}
- |V| = n（頂點數），|E| = m（邊數）
- 無向圖：0 ≤ m ≤ n(n-1)/2
- 有向圖：0 ≤ m ≤ n(n-1)

### 1.2 Adjacency Matrix（鄰接矩陣）

用一個 n × n 的矩陣 A 表示：

```
A[i][j] = 1  如果 (i, j) ∈ E
A[i][j] = 0  否則
```

對有權圖，A[i][j] 存邊的權重（不存在的邊用 ∞ 或特殊值表示）。

**空間複雜度**：O(V²)

**操作複雜度**：
| 操作 | 複雜度 |
|------|--------|
| 檢查 (u,v) 是否有邊 | O(1) |
| 列出 u 的所有鄰居 | O(V) |
| 加入/刪除一條邊 | O(1) |
| 列出所有邊 | O(V²) |

### 1.3 Adjacency List（鄰接串列）

對每個頂點 u，維護一個串列 Adj[u]，包含所有與 u 相鄰的頂點。

```
範例（無向圖）:
    1 --- 2
    |     |
    3 --- 4

Adj[1] = [2, 3]
Adj[2] = [1, 4]
Adj[3] = [1, 4]
Adj[4] = [2, 3]
```

**空間複雜度**：O(V + E)

**操作複雜度**：
| 操作 | 複雜度 |
|------|--------|
| 檢查 (u,v) 是否有邊 | O(degree(u)) |
| 列出 u 的所有鄰居 | O(degree(u)) |
| 加入一條邊 | O(1) |
| 刪除一條邊 | O(degree(u)) |
| 列出所有邊 | O(V + E) |

### 1.4 比較：何時用哪個？

| 面向 | Adjacency Matrix | Adjacency List |
|------|-------------------|----------------|
| 空間 | O(V²) | O(V + E) |
| 稀疏圖 (E ≪ V²) | 浪費空間 | **適合** |
| 稠密圖 (E ≈ V²) | **適合** | 也可以 |
| 查詢邊是否存在 | **O(1)** | O(degree) |
| 遍歷所有鄰居 | O(V) | **O(degree)** |
| BFS / DFS | O(V²) | **O(V+E)** |
| Floyd-Warshall | **適合**（需要矩陣） | 不方便 |
| 加邊 | O(1) | O(1) |

**經驗法則**：
- 大部分演算法用 **Adjacency List**（因為大部分圖是稀疏的）
- 需要快速查詢邊存在性或做矩陣運算時用 **Adjacency Matrix**
- 考試中如果沒特別說明，通常假設用 Adjacency List

---

## 2. BFS（廣度優先搜尋）

### 2.1 核心思想

從起點 s 出發，先拜訪距離 s 為 1 的所有頂點，再拜訪距離 s 為 2 的所有頂點，以此類推。就像在水面丟一顆石頭，波紋一圈一圈往外擴散。

BFS 使用一個 **Queue（佇列）** 來維護「即將拜訪的頂點」。

### 2.2 完整虛擬碼

```
BFS(G, s):
    // G = (V, E): 圖, s: 起點
    for each vertex u ∈ V - {s}:
        u.color ← WHITE        // 未被發現
        u.d ← ∞                // 距離初始化為無限大
        u.π ← NIL              // 前驅節點

    s.color ← GRAY              // 起點已被發現但未處理完
    s.d ← 0
    s.π ← NIL

    Q ← empty queue
    ENQUEUE(Q, s)

    while Q is not empty:
        u ← DEQUEUE(Q)
        for each v ∈ Adj[u]:        // 掃描 u 的所有鄰居
            if v.color == WHITE:     // v 尚未被發現
                v.color ← GRAY
                v.d ← u.d + 1
                v.π ← u
                ENQUEUE(Q, v)
        u.color ← BLACK             // u 的所有鄰居都處理完了
```

**顏色的意義**：
- **WHITE**：尚未被發現
- **GRAY**：已發現，在 Queue 中，鄰居尚未全部探索
- **BLACK**：已發現，所有鄰居都已探索

### 2.3 時間複雜度推導 O(V + E)

讓我們仔細推導：

1. **初始化**：for 迴圈走過所有頂點 → O(V)

2. **主迴圈**：while Q is not empty
   - 每個頂點最多被 ENQUEUE 一次（因為只有 WHITE 的頂點才會被加入）
   - 每個頂點最多被 DEQUEUE 一次
   - 所以外層 while 迴圈最多執行 **V 次**

3. **內層 for 迴圈**：for each v ∈ Adj[u]
   - 對每個頂點 u，掃描它的所有鄰居
   - 頂點 u 的鄰居數量 = degree(u)
   - 所有頂點的 degree 加總：
     - 無向圖：Σ degree(u) = 2|E|
     - 有向圖：Σ out-degree(u) = |E|
   - 所以內層迴圈**總共**執行 O(E) 次

4. **總計**：O(V) + O(V) + O(E) = **O(V + E)**

**重點**：這裡的 O(E) 不是「每個頂點做 O(E)」，而是「所有頂點加起來做 O(E)」。這是一種 **aggregate analysis（聚合分析）**。

### 2.4 BFS 的重要性質

#### 性質 1：最短路（無權圖）

**定理**：BFS 完成後，對每個可達的頂點 v，v.d 等於從 s 到 v 的最短路徑長度（邊數）。

**證明概略**：

定義 δ(s, v) = 從 s 到 v 的最短路徑長度。

**Claim 1**：v.d ≥ δ(s, v)（BFS 給的距離不會比真正最短路短）

歸納法：
- s.d = 0 = δ(s, s) ✓
- 對 BFS 中從 u 發現的 v：v.d = u.d + 1 ≥ δ(s, u) + 1 ≥ δ(s, v)
  （最後一步因為 δ(s, v) ≤ δ(s, u) + 1，三角不等式）

**Claim 2**：v.d ≤ δ(s, v)（BFS 給的距離不會比真正最短路長）

用歸納法和 BFS 的 FIFO 性質。Queue 中頂點的 d 值是非遞減的，所以 BFS 按「層次」探索，不會跳層。

**結合 Claim 1 和 2**：v.d = δ(s, v)。QED

#### 性質 2：BFS Tree

由所有的 π 指標構成的樹稱為 BFS 樹。BFS 樹中，從 s 到任何頂點 v 的路徑就是 G 中從 s 到 v 的最短路徑。

#### 性質 3：層次遍歷

BFS 本質上就是一種層次遍歷（level-order traversal）。第 0 層是 s，第 1 層是 s 的鄰居，第 2 層是第 1 層的未訪問鄰居，以此類推。

### 2.5 BFS 小規模範例：逐步展示 Queue 變化

> **給初學者**：BFS 的核心就是一個 Queue。以下用一個 5 節點的圖，讓你清楚看到每一步 Queue 怎麼變化。
>
> ```
> 圖：
>     1 --- 2
>     |     |
>     3 --- 4 --- 5
> ```
>
> 從節點 1 出發做 BFS：
>
> | 步驟 | 動作 | Queue 狀態 | 已拜訪 | 說明 |
> |------|------|-----------|--------|------|
> | 初始 | 1 放入 Queue | [**1**] | {1} | 起點 |
> | 1 | 取出 1，看鄰居 2, 3 | [**2, 3**] | {1, 2, 3} | 距離 1 的先放入 |
> | 2 | 取出 2，看鄰居 1, 4 | [3, **4**] | {1, 2, 3, 4} | 1 已拜訪跳過 |
> | 3 | 取出 3，看鄰居 1, 4 | [4] | {1, 2, 3, 4} | 1, 4 都已拜訪 |
> | 4 | 取出 4，看鄰居 2, 3, 5 | [**5**] | {1, 2, 3, 4, 5} | 2, 3 已拜訪 |
> | 5 | 取出 5，看鄰居 4 | [] | {1, 2, 3, 4, 5} | 4 已拜訪 |
> | 結束 | Queue 空了 | [] | 全部拜訪完 | |
>
> **結果**：
> - 拜訪順序：1 → 2 → 3 → 4 → 5
> - 距離：1(0), 2(1), 3(1), 4(2), 5(3)
>
> 注意 BFS 是**一層一層**往外擴展的：先把距離 1 的節點（2, 3）全部處理完，才處理距離 2 的（4）。

### 2.6 手動 Trace Through 範例（完整版）

考慮以下無向圖：

```
    A --- B --- C
    |         |
    D --- E --- F
```

邊：{A-B, B-C, A-D, D-E, E-F, C-F}

從 **A** 出發做 BFS（假設鄰居按字母序處理）：

```
初始狀態:
  所有頂點 WHITE, d = ∞
  A: GRAY, d = 0
  Queue: [A]

Step 1: DEQUEUE → A
  檢查 A 的鄰居: B(WHITE), D(WHITE)
    B: GRAY, d = 1, π = A → ENQUEUE
    D: GRAY, d = 1, π = A → ENQUEUE
  A: BLACK
  Queue: [B, D]

Step 2: DEQUEUE → B
  檢查 B 的鄰居: A(BLACK), C(WHITE)
    A: 已非 WHITE，跳過
    C: GRAY, d = 2, π = B → ENQUEUE
  B: BLACK
  Queue: [D, C]

Step 3: DEQUEUE → D
  檢查 D 的鄰居: A(BLACK), E(WHITE)
    A: 已非 WHITE，跳過
    E: GRAY, d = 2, π = D → ENQUEUE
  D: BLACK
  Queue: [C, E]

Step 4: DEQUEUE → C
  檢查 C 的鄰居: B(BLACK), F(WHITE)
    B: 已非 WHITE，跳過
    F: GRAY, d = 3, π = C → ENQUEUE
  C: BLACK
  Queue: [E, F]

Step 5: DEQUEUE → E
  檢查 E 的鄰居: D(BLACK), F(GRAY)
    D: 已非 WHITE，跳過
    F: 已非 WHITE，跳過
  E: BLACK
  Queue: [F]

Step 6: DEQUEUE → F
  檢查 F 的鄰居: E(BLACK), C(BLACK)
    都不是 WHITE，跳過
  F: BLACK
  Queue: []

結束！
```

**結果表格**：

| 頂點 | d (距離) | π (前驅) | 發現順序 |
|------|---------|---------|---------|
| A | 0 | NIL | 1 |
| B | 1 | A | 2 |
| D | 1 | A | 3 |
| C | 2 | B | 4 |
| E | 2 | D | 5 |
| F | 3 | C | 6 |

**BFS Tree**：
```
        A (d=0)
       / \
      B   D (d=1)
      |   |
      C   E (d=2)
      |
      F (d=3)
```

### 2.7 BFS 的應用

#### 2.7.1 連通分量（Connected Components）

對無向圖，從未訪問的頂點反覆做 BFS，每次 BFS 就找到一個連通分量。

```
CONNECTED-COMPONENTS(G):
    component_id ← 0
    for each vertex u ∈ V:
        u.cc ← -1                // 未標記

    for each vertex u ∈ V:
        if u.cc == -1:
            component_id ← component_id + 1
            BFS-MARK(G, u, component_id)

BFS-MARK(G, s, id):
    // 標準 BFS，但把所有發現的頂點標記為 id
    s.cc ← id
    Q ← [s]
    while Q not empty:
        u ← DEQUEUE(Q)
        for each v ∈ Adj[u]:
            if v.cc == -1:
                v.cc ← id
                ENQUEUE(Q, v)
```

時間複雜度：O(V + E)

#### 2.7.2 二部圖判斷

見第 7 節。

#### 2.7.3 最短路（無權圖）

BFS 本身就計算了最短路。如果要找最短路徑（而不只是距離），沿著 π 指標回溯即可：

```
PRINT-PATH(s, v):
    if v == s:
        print s
    else if v.π == NIL:
        print "沒有路徑"
    else:
        PRINT-PATH(s, v.π)
        print v
```

---

## 3. DFS（深度優先搜尋）

### 3.1 核心思想

DFS 的策略是「一條路走到底」：從起點出發，盡量往深處走，走不動了就回溯（backtrack）。

DFS 使用遞迴（或顯式 Stack）來實現。

### 3.2 完整虛擬碼（含 discovery/finish time）

```
DFS(G):
    for each vertex u ∈ V:
        u.color ← WHITE
        u.π ← NIL
    time ← 0                    // 全域時間戳

    for each vertex u ∈ V:      // 確保所有頂點都被訪問（圖可能不連通）
        if u.color == WHITE:
            DFS-VISIT(G, u)

DFS-VISIT(G, u):
    time ← time + 1
    u.d ← time                  // discovery time（發現時間）
    u.color ← GRAY              // 正在處理

    for each v ∈ Adj[u]:
        if v.color == WHITE:
            v.π ← u
            DFS-VISIT(G, v)

    u.color ← BLACK
    time ← time + 1
    u.f ← time                  // finish time（完成時間）
```

**時間戳的意義**：
- **u.d (discovery time)**：頂點 u 第一次被發現的時刻
- **u.f (finish time)**：頂點 u 的所有後代都處理完的時刻
- 永遠有 u.d < u.f
- 時間戳範圍：1 到 2|V|（每個頂點貢獻 2 個時間戳）

### 3.3 時間複雜度推導 O(V + E)

1. **DFS 主函數**：
   - 初始化迴圈：O(V)
   - 外層 for 迴圈檢查所有頂點：O(V)
   - 但 DFS-VISIT 只在 u 是 WHITE 時呼叫

2. **DFS-VISIT 的分析**：
   - 每個頂點最多被 DFS-VISIT 呼叫一次（因為呼叫時立即變 GRAY）
   - 所以 DFS-VISIT 被呼叫 **恰好 V 次**
   - 在每次 DFS-VISIT(u) 中，for 迴圈掃描 Adj[u]
   - 所有呼叫的 Adj[u] 掃描總量 = Σ |Adj[u]| = O(E)（有向圖）或 O(2E) = O(E)（無向圖）

3. **總計**：O(V) + O(V) + O(E) = **O(V + E)**

（跟 BFS 的推導邏輯完全一樣，都是 aggregate analysis。）

### 3.4 四種邊的分類

DFS 會將圖中的邊分成四類。這個分類對後續的演算法（拓撲排序、SCC）非常重要。

在 DFS 過程中，當我們在 DFS-VISIT(u) 中掃描邊 (u, v) 時：

#### 3.4.1 定義

1. **Tree Edge（樹邊）**：v 是 WHITE → (u, v) 是 DFS 樹的一部分
   - v 第一次被發現，透過這條邊

2. **Back Edge（回邊）**：v 是 GRAY → (u, v) 指向 u 的祖先
   - v 正在被處理（在遞迴堆疊中），代表找到一個環（在有向圖中）

3. **Forward Edge（前向邊）**：v 是 BLACK 且 u.d < v.d → (u, v) 指向 u 的後代
   - v 已經處理完，而且 v 是在 u 之後才被發現的（u 是 v 的祖先）

4. **Cross Edge（交叉邊）**：v 是 BLACK 且 u.d > v.d → (u, v) 連接不同子樹
   - v 已經處理完，而且 v 是在 u 之前就被發現並完成的

#### 3.4.2 判斷方法（用顏色）

```
在 DFS-VISIT(u) 中掃描邊 (u, v):

if v.color == WHITE:
    (u, v) 是 Tree Edge

else if v.color == GRAY:
    (u, v) 是 Back Edge

else:  // v.color == BLACK
    if u.d < v.d:
        (u, v) 是 Forward Edge
    else:
        (u, v) 是 Cross Edge
```

**記憶口訣**：
- WHITE → Tree（第一次見到，加入樹）
- GRAY → Back（正在處理的祖先，形成環）
- BLACK + 我先 → Forward（我是祖先，指向後代）
- BLACK + 他先 → Cross（不同子樹之間）

#### 3.4.3 有向圖 vs 無向圖中邊類型的差異

這是一個**關鍵的區別**：

| 邊類型 | 有向圖 | 無向圖 |
|--------|--------|--------|
| Tree Edge | 有 | 有 |
| Back Edge | 有 | 有 |
| Forward Edge | 有 | **沒有** |
| Cross Edge | 有 | **沒有** |

**無向圖中只有 Tree Edge 和 Back Edge！**（詳見第 8 節的推導）

### 3.5 DFS 小規模範例：逐步展示遞迴/Stack 的變化

> **給初學者**：DFS 跟 BFS 用同一張圖，這樣你可以比較兩者的差異。
>
> ```
> 圖（跟上面 BFS 的同一張）：
>     1 --- 2
>     |     |
>     3 --- 4 --- 5
> ```
>
> 從節點 1 出發做 DFS（鄰居按數字小的優先）：
>
> | 步驟 | 遞迴呼叫 | Stack（呼叫堆疊） | 動作 |
> |------|----------|------------------|------|
> | 1 | DFS(1) | [1] | 1 變灰色，看鄰居 2（白色）→ 進入 |
> | 2 | DFS(2) | [1, 2] | 2 變灰色，看鄰居 1（灰色，跳過）、4（白色）→ 進入 |
> | 3 | DFS(4) | [1, 2, 4] | 4 變灰色，看鄰居 2（灰色，跳過）、3（白色）→ 進入 |
> | 4 | DFS(3) | [1, 2, 4, 3] | 3 變灰色，看鄰居 1（灰色，跳過）、4（灰色，跳過）→ 沒有白色鄰居 |
> | 5 | 3 完成 | [1, 2, 4] | 3 變黑色，回到 DFS(4) |
> | 6 | 回到 DFS(4) | [1, 2, 4] | 4 繼續看鄰居 5（白色）→ 進入 |
> | 7 | DFS(5) | [1, 2, 4, 5] | 5 變灰色，看鄰居 4（灰色，跳過）→ 沒有白色鄰居 |
> | 8 | 5 完成 | [1, 2, 4] | 5 變黑色，回到 DFS(4) |
> | 9 | 4 完成 | [1, 2] | 4 變黑色，回到 DFS(2) |
> | 10 | 2 完成 | [1] | 2 變黑色，回到 DFS(1) |
> | 11 | 看 1 的鄰居 3 | [1] | 3 已經是黑色，跳過 |
> | 12 | 1 完成 | [] | 1 變黑色，結束 |
>
> **拜訪順序**：1 → 2 → 4 → 3 → 5
>
> **對比 BFS**：BFS 的順序是 1 → 2 → 3 → 4 → 5（一層一層），DFS 的順序是 1 → 2 → 4 → 3 → 5（一條路走到底再回頭）。
>
> 注意 DFS 是**往深處鑽**的：1 → 2 → 4 → 3（走到底！）才回頭，然後再走 5。

### 3.6 手動 Trace Through 範例（有向圖完整版）

考慮以下有向圖：

```
    A → B → C
    ↓       ↑
    D → E → F
        ↓
        G
```

邊：A→B, A→D, B→C, D→E, E→F, E→G, F→C

假設鄰居按字母序處理，從 A 開始 DFS：

```
time = 0

DFS-VISIT(A):
    time = 1, A.d = 1, A → GRAY

    掃描 A 的鄰居:

    B (WHITE) → Tree Edge
    DFS-VISIT(B):
        time = 2, B.d = 2, B → GRAY

        掃描 B 的鄰居:

        C (WHITE) → Tree Edge
        DFS-VISIT(C):
            time = 3, C.d = 3, C → GRAY

            C 沒有出邊（或所有鄰居都不是 WHITE）

            time = 4, C.f = 4, C → BLACK

        B 的鄰居掃完
        time = 5, B.f = 5, B → BLACK

    D (WHITE) → Tree Edge
    DFS-VISIT(D):
        time = 6, D.d = 6, D → GRAY

        掃描 D 的鄰居:

        E (WHITE) → Tree Edge
        DFS-VISIT(E):
            time = 7, E.d = 7, E → GRAY

            掃描 E 的鄰居:

            F (WHITE) → Tree Edge
            DFS-VISIT(F):
                time = 8, F.d = 8, F → GRAY

                掃描 F 的鄰居:

                C (BLACK, C.d=3 < F.d=8? 是的，
                   但 F 不是 C 的祖先，C.d=3 < F.d=8)
                   F.d=8 > C.d=3 → Cross Edge

                time = 9, F.f = 9, F → BLACK

            G (WHITE) → Tree Edge
            DFS-VISIT(G):
                time = 10, G.d = 10, G → GRAY

                G 沒有出邊

                time = 11, G.f = 11, G → BLACK

            E 的鄰居掃完
            time = 12, E.f = 12, E → BLACK

        D 的鄰居掃完
        time = 13, D.f = 13, D → BLACK

    A 的鄰居掃完
    time = 14, A.f = 14, A → BLACK
```

**結果表格**：

| 頂點 | d (發現) | f (完成) | π (前驅) |
|------|---------|---------|---------|
| A | 1 | 14 | NIL |
| B | 2 | 5 | A |
| C | 3 | 4 | B |
| D | 6 | 13 | A |
| E | 7 | 12 | D |
| F | 8 | 9 | E |
| G | 10 | 11 | E |

**邊分類**：

| 邊 | v 的顏色 | 類型 |
|----|---------|------|
| A→B | WHITE | Tree Edge |
| B→C | WHITE | Tree Edge |
| A→D | WHITE | Tree Edge |
| D→E | WHITE | Tree Edge |
| E→F | WHITE | Tree Edge |
| F→C | BLACK (u.d=8 > v.d=3) | Cross Edge |
| E→G | WHITE | Tree Edge |

**DFS Tree**：
```
        A [1/14]
       / \
      B    D [6/13]
      |    |
      C    E [7/12]
    [3/4]  / \
          F   G
        [8/9] [10/11]
```

**時間戳括號表示**：
```
A: [1 ────────────────────────── 14]
B: [2 ──── 5]
C:   [3 ─ 4]
D:            [6 ──────────── 13]
E:              [7 ──────── 12]
F:                [8 ─ 9]
G:                      [10 ─ 11]
```

### 3.7 白色路徑定理和括號定理

#### 3.7.1 括號定理（Parenthesis Theorem）

**定理**：在 DFS 中，對任意兩個頂點 u 和 v，以下三者恰有一個成立：

1. **[u.d, u.f] 和 [v.d, v.f] 完全不重疊**：u 和 v 不在同一棵 DFS 子樹中
2. **[u.d, u.f] ⊂ [v.d, v.f]**：u 是 v 的後代
3. **[v.d, v.f] ⊂ [u.d, u.f]**：v 是 u 的後代

**不可能出現部分重疊的情況**（例如 u.d < v.d < u.f < v.f 是不可能的）。

**證明概略**：
- 如果 u.d < v.d：
  - 情況 a：v 在 u 完成之前被發現（v.d < u.f）→ v 是 u 的後代，v 一定在 u 完成之前完成 → v.f < u.f → [v.d, v.f] ⊂ [u.d, u.f]
  - 情況 b：v 在 u 完成之後被發現（v.d > u.f）→ 完全不重疊
- 如果 v.d < u.d：對稱的分析

所以時間戳區間要嘛包含、要嘛不重疊，就像括號一樣。

**範例驗證**：

用上面的結果：
```
A [1, 14] 和 B [2, 5]：  [2,5] ⊂ [1,14] → B 是 A 的後代  ✓
A [1, 14] 和 D [6, 13]：  [6,13] ⊂ [1,14] → D 是 A 的後代  ✓
B [2, 5] 和 D [6, 13]：  完全不重疊 → 不同子樹  ✓
B [2, 5] 和 F [8, 9]：   完全不重疊 → 不同子樹  ✓
E [7, 12] 和 F [8, 9]：  [8,9] ⊂ [7,12] → F 是 E 的後代  ✓
```

#### 3.7.2 白色路徑定理（White-Path Theorem）

**定理**：在 DFS 森林中，頂點 v 是頂點 u 的後代，若且唯若在 DFS-VISIT(u) 被呼叫的時刻（即時間 u.d），存在一條從 u 到 v 的路徑，且路徑上所有頂點都是 WHITE。

**直覺**：如果從 u 到 v 有一條全白的路，DFS 一定會沿著某條路找到 v（因為 DFS 會走到底），所以 v 會成為 u 的後代。

**證明**：

(→) 如果 v 是 u 的後代：
在 DFS-VISIT(u) 開始時，u 到 v 的樹路徑上的所有頂點都還是 WHITE（因為它們都是在 u 之後才被發現的）。

(←) 如果存在全白路徑 u = w₀, w₁, ..., wₖ = v：
- w₁ 是 WHITE，所以 DFS-VISIT(u) 會（直接或間接）呼叫 DFS-VISIT(w₁)
- 依此類推，w₂ 也會被 u 的子樹發現
- 最終 v = wₖ 會成為 u 的後代。QED

---

## 4. 拓撲排序（Topological Sort）

### 4.1 定義

對一個 DAG（有向無環圖），拓撲排序是一個頂點的線性排列，使得對每條邊 (u, v)，u 在排列中出現在 v 之前。

**直覺**：如果 u → v 代表「u 必須在 v 之前完成」，拓撲排序就是一個合法的完成順序。

**存在條件**：拓撲排序存在 ⟺ 圖是 DAG（沒有環）。

### 4.2 拓撲排序的直覺——用「修課順序」理解

> **生活中的例子**：假設你要規劃這學期的修課順序，有以下先修限制：
>
> - 微積分 → 線性代數（先修微積分才能修線代）
> - 微積分 → 機率
> - 程式設計 → 資料結構
> - 資料結構 → 演算法
> - 線性代數 → 演算法
>
> 畫成有向圖：
> ```
> 微積分 → 線性代數 → 演算法
>   ↓                   ↑
> 機率    程式設計 → 資料結構
> ```
>
> 拓撲排序就是找一個修課順序，讓每門課都在它的先修課之後。例如：
> - 微積分, 程式設計, 機率, 線性代數, 資料結構, 演算法 （合法）
> - 程式設計, 微積分, 資料結構, 線性代數, 機率, 演算法 （也合法）
> - 演算法, 微積分, ... （不合法！演算法排在微積分前面了）
>
> **注意**：如果先修關係有環（例如 A 要先修 B，B 又要先修 A），就不可能排出合法的順序！
> 所以拓撲排序只能對 **DAG**（有向無環圖）做。

### 4.3 方法一：DFS 方法（Finish Time 遞減排序）

#### 4.3.1 演算法

```
TOPOLOGICAL-SORT-DFS(G):
    呼叫 DFS(G) 計算每個頂點的 finish time u.f
    按 u.f 遞減排序所有頂點
    return 排序結果
```

或者更實際的寫法：

```
TOPOLOGICAL-SORT-DFS(G):
    L ← empty linked list
    for each vertex u ∈ V:
        u.color ← WHITE

    for each vertex u ∈ V:
        if u.color == WHITE:
            DFS-VISIT-TOPO(G, u, L)

    return L

DFS-VISIT-TOPO(G, u, L):
    u.color ← GRAY
    for each v ∈ Adj[u]:
        if v.color == WHITE:
            DFS-VISIT-TOPO(G, v, L)
    u.color ← BLACK
    L.INSERT-FRONT(u)          // 完成時插到最前面
```

#### 4.3.2 正確性推導

**定理**：在 DAG 的 DFS 中，對任何邊 (u, v)，u.f > v.f。

**證明**：考慮邊 (u, v)。在 DFS 掃描到 (u, v) 時：

- **Case 1**：v 是 WHITE → DFS-VISIT(v) 被呼叫 → v 在 u 之前完成 → v.f < u.f ✓
- **Case 2**：v 是 BLACK → v 已經完成 → v.f < time < u.f ✓
- **Case 3**：v 是 GRAY → v 正在處理中 → 表示存在從 v 到 u 的路徑 → 加上邊 (u, v) 就形成環 → 矛盾！（DAG 沒有環）

所以在 DAG 中，Case 3 不可能發生。Cases 1 和 2 都保證 u.f > v.f。

因此，按 finish time 遞減排序後，對每條邊 (u, v)，u 排在 v 前面 → 合法的拓撲排序。QED

**時間複雜度**：DFS O(V + E) + 排序（其實用鏈表的 INSERT-FRONT 就不需要排序）= **O(V + E)**

#### 4.3.3 計算範例

```
DAG:
    A → B → D
    A → C → D
    C → E

DFS（假設按字母序）:

DFS-VISIT(A):
  A.d = 1, GRAY
  → B (WHITE)
    DFS-VISIT(B):
      B.d = 2, GRAY
      → D (WHITE)
        DFS-VISIT(D):
          D.d = 3, GRAY
          D 沒有出邊
          D.f = 4, BLACK → L = [D]
      B.f = 5, BLACK → L = [B, D]
  → C (WHITE)
    DFS-VISIT(C):
      C.d = 6, GRAY
      → D (BLACK, 跳過)
      → E (WHITE)
        DFS-VISIT(E):
          E.d = 7, GRAY
          E 沒有出邊
          E.f = 8, BLACK → L = [E, B, D]
      C.f = 9, BLACK → L = [C, E, B, D]
  A.f = 10, BLACK → L = [A, C, E, B, D]

拓撲排序: A, C, E, B, D

驗證: A→B ✓, A→C ✓, B→D ✓, C→D ✓, C→E ✓
所有邊的起點都在終點之前 ✓
```

### 4.4 方法二：Kahn's Algorithm（BFS 方法）

#### 4.4.1 核心想法

反覆找到入度（in-degree）為 0 的頂點，輸出它，然後刪掉它和它的出邊（這會讓其他頂點的入度減少）。

如果一個頂點入度為 0，代表沒有任何前驅必須在它之前完成，所以可以先處理它。

#### 4.4.2 虛擬碼

```
KAHN-TOPOLOGICAL-SORT(G):
    // 計算所有頂點的入度
    for each vertex u ∈ V:
        in_degree[u] ← 0
    for each edge (u, v) ∈ E:
        in_degree[v] ← in_degree[v] + 1

    Q ← empty queue
    for each vertex u ∈ V:
        if in_degree[u] == 0:
            ENQUEUE(Q, u)

    L ← empty list              // 拓撲排序結果
    count ← 0                   // 計算已處理的頂點數

    while Q is not empty:
        u ← DEQUEUE(Q)
        L.append(u)
        count ← count + 1

        for each v ∈ Adj[u]:    // u 的所有出邊
            in_degree[v] ← in_degree[v] - 1
            if in_degree[v] == 0:
                ENQUEUE(Q, v)

    if count ≠ |V|:
        return "圖有環，無法拓撲排序"
    return L
```

**時間複雜度**：
- 計算入度：O(V + E)
- 主迴圈：每個頂點入隊出隊一次 O(V)，每條邊被處理一次 O(E)
- 總計：**O(V + E)**

#### 4.4.3 計算範例

```
DAG:
    A → B → D
    A → C → D
    C → E

初始入度: A:0, B:1, C:1, D:2, E:1
Q = [A]  (只有 A 入度為 0)

Step 1: DEQUEUE → A, L = [A]
  A→B: in_degree[B] = 1-1 = 0 → ENQUEUE(B)
  A→C: in_degree[C] = 1-1 = 0 → ENQUEUE(C)
  Q = [B, C]

Step 2: DEQUEUE → B, L = [A, B]
  B→D: in_degree[D] = 2-1 = 1 → 不入隊
  Q = [C]

Step 3: DEQUEUE → C, L = [A, B, C]
  C→D: in_degree[D] = 1-1 = 0 → ENQUEUE(D)
  C→E: in_degree[E] = 1-1 = 0 → ENQUEUE(E)
  Q = [D, E]

Step 4: DEQUEUE → D, L = [A, B, C, D]
  D 沒有出邊
  Q = [E]

Step 5: DEQUEUE → E, L = [A, B, C, D, E]
  E 沒有出邊
  Q = []

結果: 拓撲排序 = [A, B, C, D, E]
count = 5 = |V| → 沒有環 ✓
```

### 4.5 兩種方法的比較

| 面向 | DFS 方法 | Kahn's Algorithm |
|------|---------|------------------|
| 基於 | DFS + finish time | BFS + in-degree |
| 時間複雜度 | O(V + E) | O(V + E) |
| 能否偵測環 | 可以（看有沒有 back edge） | 可以（看 count 是否 = |V|） |
| 實作難度 | 遞迴，簡潔 | 迭代，直觀 |
| 結果順序 | finish time 遞減 | 入度為 0 的先出 |
| 字典序最小的拓撲排序 | 不容易 | **容易**（用 min-heap 取代 queue） |
| 增量式 | 不方便 | 較方便 |

### 4.6 何時拓撲排序唯一？→ DAG Hamiltonian Path

**定理**：一個 DAG 的拓撲排序是唯一的，若且唯若 DAG 中存在一條 Hamiltonian Path（經過所有頂點恰好一次的路徑）。

**等價條件**：拓撲排序唯一 ⟺ 拓撲排序中每對相鄰頂點之間都有邊。

**證明**：

(→) 如果拓撲排序唯一，令其為 v₁, v₂, ..., vₙ。
- 如果某個 (vᵢ, vᵢ₊₁) 不是邊，那麼 vᵢ 和 vᵢ₊₁ 可以互換位置（因為沒有從 vᵢ 到 vᵢ₊₁ 的直接約束），而得到另一個合法的拓撲排序。矛盾。
- 所以每對相鄰頂點都有邊 → v₁ → v₂ → ... → vₙ 是 Hamiltonian Path。

(←) 如果存在 Hamiltonian Path v₁ → v₂ → ... → vₙ，那麼：
- 在任何拓撲排序中，v₁ 必須在 v₂ 前面，v₂ 必須在 v₃ 前面，...
- 所有頂點的相對順序都被固定了 → 拓撲排序唯一。

**應用**：在 Kahn's Algorithm 中，如果每一步 queue 裡都恰好只有一個元素，那拓撲排序就是唯一的。

---

## 5. 強連通分量（SCC）

### 5.1 定義

在有向圖中，一個**強連通分量（Strongly Connected Component, SCC）**是一個最大的頂點子集 C，使得 C 中的任意兩個頂點 u, v 之間都可以互相到達（u 到 v 有路，v 到 u 也有路）。

**SCC 的重要性質**：
- 每個頂點恰好屬於一個 SCC
- 把每個 SCC 縮成一個點後，得到的圖（稱為 **condensation graph** 或 **component graph**）一定是 DAG

### 5.2 Kosaraju 演算法

#### 5.2.1 演算法步驟

```
KOSARAJU-SCC(G):
    // Step 1: 對 G 做 DFS，記錄 finish time
    呼叫 DFS(G)
    在 DFS 中，當每個頂點完成時，push 到 stack S

    // Step 2: 計算反向圖 G^T
    G^T ← TRANSPOSE(G)        // 反轉所有邊的方向

    // Step 3: 按 finish time 遞減順序，對 G^T 做 DFS
    標記所有頂點為 WHITE
    while S is not empty:
        u ← S.POP()
        if u.color == WHITE:
            DFS-VISIT(G^T, u)    // 這次 DFS 找到的所有頂點構成一個 SCC
```

#### 5.2.2 虛擬碼（更詳細版本）

```
KOSARAJU-SCC(G):
    // Step 1: 第一次 DFS
    for each vertex u ∈ V:
        u.color ← WHITE
    S ← empty stack
    time ← 0
    for each vertex u ∈ V:
        if u.color == WHITE:
            DFS-VISIT-1(G, u, S)

    // Step 2: 構造反向圖
    G^T ← 新建空圖，頂點集與 G 相同
    for each edge (u, v) ∈ G.E:
        G^T 加入邊 (v, u)

    // Step 3: 第二次 DFS（按 finish time 遞減序）
    for each vertex u ∈ V:
        u.color ← WHITE
    scc_id ← 0
    while S is not empty:
        u ← S.POP()
        if u.color == WHITE:
            scc_id ← scc_id + 1
            DFS-VISIT-2(G^T, u, scc_id)

DFS-VISIT-1(G, u, S):
    u.color ← GRAY
    for each v ∈ G.Adj[u]:
        if v.color == WHITE:
            DFS-VISIT-1(G, v, S)
    u.color ← BLACK
    S.PUSH(u)

DFS-VISIT-2(G^T, u, scc_id):
    u.color ← GRAY
    u.scc ← scc_id
    for each v ∈ G^T.Adj[u]:
        if v.color == WHITE:
            DFS-VISIT-2(G^T, v, scc_id)
    u.color ← BLACK
```

#### 5.2.3 正確性推導

**為什麼 Kosaraju 有效？**

核心思想：如果 u 和 v 在同一個 SCC 中，那麼在 G 和 G^T 中，u 和 v 都互相可達。

**關鍵引理**：在第一次 DFS 中，如果 SCC C₁ 有邊連到 SCC C₂，那麼 C₁ 中某個頂點的 finish time > C₂ 中所有頂點的 finish time。

更精確地說：令 f(C) = max{u.f : u ∈ C}。如果 C₁ → C₂ 有邊，那麼 f(C₁) > f(C₂)。

**證明**：
- 令 u 是 C₁ 中第一個被發現的頂點
- Case 1：u 在 C₂ 中任何頂點之前被發現。那麼 u 可以到達 C₁ 和 C₂ 的所有頂點（因為 C₁ 是 SCC，且 C₁ → C₂ 有邊）。由白色路徑定理，C₂ 的所有頂點都是 u 的後代。所以 u.f > C₂ 中所有頂點的 f。
- Case 2：C₂ 中某個頂點 v 在 u 之前被發現。v 不能到達 u（否則加上 C₁ → C₂ 的邊，C₁ 和 C₂ 就不是不同的 SCC 了）。所以 v 會在發現 u 之前完成。然後 u 被發現後，會走遍 C₁ 的所有頂點。所以 u.f > v.f。

**第二次 DFS 的邏輯**：
- 在 G^T 中，邊的方向反轉了。如果 G 中 C₁ → C₂，則 G^T 中 C₂ → C₁。
- 我們按 finish time 遞減順序做 DFS，所以先處理 f(C) 最大的 SCC。
- 在 G^T 中，從 C₁（f 最大的）出發做 DFS：
  - C₁ 內的頂點互相可達（SCC 性質在轉置後不變）→ 會找到 C₁ 的所有頂點
  - C₁ 不能到達其他 SCC（因為在 G^T 中，原來 C₁ → C₂ 的邊變成了 C₂ → C₁）
  - 所以只會找到 C₁ 的頂點 → 正確識別一個 SCC

**時間複雜度**：
- 第一次 DFS：O(V + E)
- 轉置圖：O(V + E)
- 第二次 DFS：O(V + E)
- 總計：**O(V + E)**

#### 5.2.4 手動 Trace Through 範例

```
有向圖 G:
    A → B
    B → C
    C → A        (SCC: {A, B, C})
    C → D
    D → E
    E → F
    F → D        (SCC: {D, E, F})
    E → G        (SCC: {G})

邊: A→B, B→C, C→A, C→D, D→E, E→F, F→D, E→G
```

**Step 1：第一次 DFS on G**（假設按字母序）

```
DFS-VISIT(A):
  A.d=1, GRAY
  → B (WHITE)
    DFS-VISIT(B):
      B.d=2, GRAY
      → C (WHITE)
        DFS-VISIT(C):
          C.d=3, GRAY
          → A (GRAY) → Back Edge, 跳過
          → D (WHITE)
            DFS-VISIT(D):
              D.d=4, GRAY
              → E (WHITE)
                DFS-VISIT(E):
                  E.d=5, GRAY
                  → F (WHITE)
                    DFS-VISIT(F):
                      F.d=6, GRAY
                      → D (GRAY) → Back Edge, 跳過
                      F.f=7, BLACK → PUSH(F)
                  → G (WHITE)
                    DFS-VISIT(G):
                      G.d=8, GRAY
                      G.f=9, BLACK → PUSH(G)
                  E.f=10, BLACK → PUSH(E)
              D.f=11, BLACK → PUSH(D)
          C.f=12, BLACK → PUSH(C)
      B.f=13, BLACK → PUSH(B)
  A.f=14, BLACK → PUSH(A)

Stack S (top to bottom): [A, B, C, D, E, G, F]
Finish times: F:7, G:9, E:10, D:11, C:12, B:13, A:14
```

**Step 2：構造 G^T**

```
G^T 的邊: B→A, C→B, A→C, D→C, E→D, F→E, D→F, G→E
```

**Step 3：第二次 DFS on G^T（按 stack 順序 pop）**

```
POP A (WHITE):
  DFS-VISIT-2(G^T, A, scc=1):
    A → GRAY, scc=1
    G^T.Adj[A] = [C]
    → C (WHITE)
      DFS-VISIT-2(G^T, C, scc=1):
        C → GRAY, scc=1
        G^T.Adj[C] = [B]
        → B (WHITE)
          DFS-VISIT-2(G^T, B, scc=1):
            B → GRAY, scc=1
            G^T.Adj[B] = [A]
            → A (GRAY) → 跳過
            B → BLACK
        C → BLACK
    A → BLACK
  SCC 1: {A, B, C} ✓

POP B (非 WHITE, 跳過)
POP C (非 WHITE, 跳過)

POP D (WHITE):
  DFS-VISIT-2(G^T, D, scc=2):
    D → GRAY, scc=2
    G^T.Adj[D] = [C, F]
    → C (非 WHITE) → 跳過
    → F (WHITE)
      DFS-VISIT-2(G^T, F, scc=2):
        F → GRAY, scc=2
        G^T.Adj[F] = [E]
        → E (WHITE)
          DFS-VISIT-2(G^T, E, scc=2):
            E → GRAY, scc=2
            G^T.Adj[E] = [D, G]
            → D (GRAY) → 跳過
            → G (WHITE)
              ... 等等，G 應該是自己的 SCC

  讓我重新仔細看...
  G^T.Adj[E] = [D, G]
            → D (GRAY) → 跳過
            → G (WHITE)
              DFS-VISIT-2(G^T, G, scc=2):
                G → GRAY, scc=2
                G^T.Adj[G] = [E]
                → E (GRAY) → 跳過
                G → BLACK
            E → BLACK
        F → BLACK
    D → BLACK
  SCC 2: {D, E, F, G}
```

等一下，這裡出了問題。G 應該是自己的 SCC（因為 G 只有入邊 E→G，沒有出邊回到任何地方）。讓我重新檢查。

在原圖 G 中：E→G 存在，但 G 沒有出邊。所以 G 自己是一個 SCC。

問題出在 Stack 的順序。讓我重新做：

Stack 的 pop 順序是 finish time 遞減：A(14), B(13), C(12), D(11), E(10), G(9), F(7)

```
POP A → SCC 1: 找到 {A, C, B} = {A, B, C} ✓

POP B → 已訪問
POP C → 已訪問

POP D (WHITE):
  在 G^T 中從 D 出發 DFS：
  G^T.Adj[D] = [C, F]
  → C：已訪問，跳過
  → F (WHITE)：
    G^T.Adj[F] = [E]
    → E (WHITE)：
      G^T.Adj[E] = [D, G]
      → D (GRAY)：跳過
      → G (WHITE)：
        G^T.Adj[G] = [E]
        → E (GRAY)：跳過
        G 完成
      E 完成
    F 完成
  D 完成
  SCC 2: {D, F, E, G}
```

嗯，按照這個執行，SCC 2 包含了 G。但 G 不應該在 {D, E, F} 的 SCC 裡。

讓我重新思考：在原圖中 E→G，在 G^T 中 G→E。所以在 G^T 中從 D 出發，可以到達 F→E→...→D（這是 SCC {D,E,F}），而且 E 可以到 G（等等不對，G^T 中是 G→E，不是 E→G）。

G^T 中的邊是：B→A, C→B, A→C, D→C, E→D, F→E, D→F, G→E

所以在 G^T 中：
- 從 D 出發：D→C（已訪問），D→F
- 從 F：F→E
- 從 E：E→D（已在路上），E 沒有到 G 的邊
- G→E 是存在的，但不是 E→G

所以從 D 出發的 DFS 在 G^T 中只會找到 {D, F, E}。G 沒辦法從 D 到達（因為 G^T 中是 G→E，不是 E→G）。

讓我重新執行：

```
POP D (WHITE):
  DFS-VISIT-2(G^T, D, scc=2):
    D → GRAY, scc=2
    G^T.Adj[D] = [C, F]
    → C (BLACK) → 跳過
    → F (WHITE)
      DFS-VISIT-2(G^T, F, scc=2):
        F → GRAY, scc=2
        G^T.Adj[F] = [E]
        → E (WHITE)
          DFS-VISIT-2(G^T, E, scc=2):
            E → GRAY, scc=2
            G^T.Adj[E] = [D]     // ← 只有 E→D（來自原圖的 D→E 反轉）
            → D (GRAY) → 跳過
            E → BLACK
        F → BLACK
    D → BLACK
  SCC 2: {D, F, E} ✓

POP E → 已訪問

POP G (WHITE):
  DFS-VISIT-2(G^T, G, scc=3):
    G → GRAY, scc=3
    G^T.Adj[G] = [E]           // 來自原圖 E→G 的反轉
    → E (BLACK) → 跳過
    G → BLACK
  SCC 3: {G} ✓

POP F → 已訪問
```

**最終結果**：
- SCC 1: {A, B, C}
- SCC 2: {D, E, F}
- SCC 3: {G}

**Component Graph (DAG)**：
```
{A,B,C} → {D,E,F} → {G}
```

---

### 5.3 Tarjan 演算法

#### 5.3.1 核心思想

Tarjan 的方法只需要**一次 DFS**。它維護一個 stack，並利用 **low-link** 值來判斷 SCC。

**low-link 值**：對頂點 u，low[u] 是 u 能夠通過 DFS 子樹中的邊（包含最多一條 back edge 或 cross edge to stack）到達的最小 discovery time。

更精確的定義：low[u] = min({u.d} ∪ {v.d : v 在 stack 中，且 u 的子樹中某個頂點有邊到 v})

當 low[u] == u.d 時，u 是其所在 SCC 的**根**（在 DFS 樹中）。

#### 5.3.2 完整虛擬碼

```
TARJAN-SCC(G):
    time ← 0
    S ← empty stack                    // 用來追蹤當前路徑上的節點
    for each vertex u ∈ V:
        u.d ← -1                      // 未訪問
        u.on_stack ← false

    for each vertex u ∈ V:
        if u.d == -1:
            STRONGCONNECT(u)

STRONGCONNECT(u):
    time ← time + 1
    u.d ← time
    u.low ← time                      // 初始 low = 自己的 discovery time
    S.PUSH(u)
    u.on_stack ← true

    for each v ∈ Adj[u]:
        if v.d == -1:                  // v 未訪問 → Tree Edge
            STRONGCONNECT(v)
            u.low ← min(u.low, v.low)  // 子節點的 low 值可能更小
        else if v.on_stack:            // v 在 stack 中 → Back Edge
            u.low ← min(u.low, v.d)   // 更新 low 值

    // 如果 u 是 SCC 的根
    if u.low == u.d:
        SCC ← {}
        repeat:
            v ← S.POP()
            v.on_stack ← false
            SCC ← SCC ∪ {v}
        until v == u
        輸出 SCC
```

#### 5.3.3 重要細節

1. `u.low ← min(u.low, v.low)`：當 v 是透過 tree edge 發現的子節點時，v 能到達的最小值也是 u 能到達的。

2. `u.low ← min(u.low, v.d)`：當 v 在 stack 中時（back edge），u 可以回到 v，所以更新 low 為 v.d。

3. **為什麼不用 `v.low` 而是用 `v.d` 對 back edge？** 兩種寫法在很多場合都正確，但用 `v.d` 是 Tarjan 原始論文的定義，更符合 low-link 的嚴格語義。在某些實作中用 `v.low` 也可以得到正確結果（因為 v 在 stack 上代表 v 和 u 在同一個 SCC 候選中）。

4. `u.low == u.d`：這代表 u 沒有辦法通過任何邊回到更早（更上層）的頂點 → u 是 SCC 的根 → 把 stack 中 u 以上的頂點全部 pop 出來，就是一個 SCC。

#### 5.3.4 手動 Trace Through 範例

用跟 Kosaraju 一樣的圖：

```
A → B, B → C, C → A, C → D, D → E, E → F, F → D, E → G
```

```
time = 0, Stack = []

STRONGCONNECT(A):
  time=1, A.d=1, A.low=1, PUSH(A), Stack=[A]
  → B (未訪問)
    STRONGCONNECT(B):
      time=2, B.d=2, B.low=2, PUSH(B), Stack=[A,B]
      → C (未訪問)
        STRONGCONNECT(C):
          time=3, C.d=3, C.low=3, PUSH(C), Stack=[A,B,C]
          → A (on_stack): C.low = min(3, A.d=1) = 1
          → D (未訪問)
            STRONGCONNECT(D):
              time=4, D.d=4, D.low=4, PUSH(D), Stack=[A,B,C,D]
              → E (未訪問)
                STRONGCONNECT(E):
                  time=5, E.d=5, E.low=5, PUSH(E), Stack=[A,B,C,D,E]
                  → F (未訪問)
                    STRONGCONNECT(F):
                      time=6, F.d=6, F.low=6, PUSH(F), Stack=[A,B,C,D,E,F]
                      → D (on_stack): F.low = min(6, D.d=4) = 4
                      檢查: F.low(4) ≠ F.d(6) → F 不是 SCC 根
                  E.low = min(E.low=5, F.low=4) = 4
                  → G (未訪問)
                    STRONGCONNECT(G):
                      time=7, G.d=7, G.low=7, PUSH(G), Stack=[A,B,C,D,E,F,G]
                      G 沒有出邊
                      檢查: G.low(7) == G.d(7) → G 是 SCC 根！
                      POP G → SCC = {G}
                      Stack=[A,B,C,D,E,F]
                  E.low = min(E.low=4, G.low=7) = 4  // G.low 已不影響
                  // 注意：G 已被 pop 出 stack 了，所以 G.low 不影響 E
                  // 但在代碼中，因為 G 是通過 tree edge 發現的，
                  // 所以用 min(E.low, G.low) = min(4, 7) = 4
                  檢查: E.low(4) ≠ E.d(5) → E 不是 SCC 根
              D.low = min(D.low=4, E.low=4) = 4
              檢查: D.low(4) == D.d(4) → D 是 SCC 根！
              POP: F(off stack), E(off stack), D(off stack)
              SCC = {D, E, F}
              Stack=[A,B,C]
          C.low = min(C.low=1, D.low=4) = 1
          // 但等等 D 已經 pop 了...
          // 在代碼中，D 是 tree edge child，所以用 min(C.low, D.low)
          // C.low = min(1, 4) = 1
          檢查: C.low(1) ≠ C.d(3) → C 不是 SCC 根
      B.low = min(B.low=2, C.low=1) = 1
      檢查: B.low(1) ≠ B.d(2) → B 不是 SCC 根
  A.low = min(A.low=1, B.low=1) = 1
  檢查: A.low(1) == A.d(1) → A 是 SCC 根！
  POP: C(off stack), B(off stack), A(off stack)
  SCC = {A, B, C}
  Stack=[]
```

**結果**：
- SCC 1: {G}（先被找到）
- SCC 2: {D, E, F}
- SCC 3: {A, B, C}

**注意**：Tarjan 找 SCC 的順序是**反向拓撲序**（先找到匯點 SCC，最後找到源頭 SCC）。

#### 5.3.5 Kosaraju vs Tarjan 比較

| 面向 | Kosaraju | Tarjan |
|------|----------|--------|
| DFS 次數 | 2 次 | 1 次 |
| 需要反向圖 | 是 | 否 |
| 額外空間 | O(V+E)（反向圖） | O(V)（stack） |
| 實作難度 | 較簡單，兩次標準 DFS | 較複雜，需要 low-link |
| SCC 輸出順序 | 正向拓撲序 | 反向拓撲序 |
| 時間複雜度 | O(V + E) | O(V + E) |

---

## 6. 環偵測（Cycle Detection）

### 6.1 有向圖：DFS 看 Back Edge

**定理**：有向圖有環 ⟺ DFS 中存在 back edge。

**證明**：

(→) 如果圖有環 v₁ → v₂ → ... → vₖ → v₁：
- 令 vᵢ 是環上第一個被 DFS 發現的頂點
- 由白色路徑定理，vᵢ₊₁, ..., vₖ 都會成為 vᵢ 的後代
- 邊 vₖ → v₁ = vᵢ 就是從後代到祖先的邊 → back edge

(←) 如果存在 back edge (u, v)：
- v 是 u 的祖先（v 是 GRAY 時被發現 back edge）
- 從 v 到 u 有一條 tree path，加上 back edge (u, v) → 形成環

**虛擬碼**：

```
HAS-CYCLE-DIRECTED(G):
    for each vertex u ∈ V:
        u.color ← WHITE

    for each vertex u ∈ V:
        if u.color == WHITE:
            if DFS-CYCLE(G, u):
                return true
    return false

DFS-CYCLE(G, u):
    u.color ← GRAY
    for each v ∈ Adj[u]:
        if v.color == GRAY:        // Back edge found!
            return true
        if v.color == WHITE:
            if DFS-CYCLE(G, v):
                return true
    u.color ← BLACK
    return false
```

**時間複雜度**：O(V + E)

### 6.2 無向圖：DFS 或 Union-Find

#### 6.2.1 DFS 方法

無向圖中，DFS 看到一個已訪問的鄰居（不是父節點）就代表有環。

```
HAS-CYCLE-UNDIRECTED-DFS(G):
    for each vertex u ∈ V:
        u.color ← WHITE

    for each vertex u ∈ V:
        if u.color == WHITE:
            if DFS-CYCLE-UNDIR(G, u, NIL):
                return true
    return false

DFS-CYCLE-UNDIR(G, u, parent):
    u.color ← GRAY
    for each v ∈ Adj[u]:
        if v == parent:
            continue               // 跳過來的那條邊（避免把無向邊的反方向誤認為環）
        if v.color == GRAY:
            return true             // 找到環！
        if v.color == WHITE:
            if DFS-CYCLE-UNDIR(G, v, u):
                return true
    u.color ← BLACK
    return false
```

**注意**：無向圖中每條邊 {u, v} 在鄰接表中出現兩次（u 的鄰居有 v，v 的鄰居有 u）。所以需要排除「走回父節點」的情況，避免誤判。

**特殊情況**：如果 u 和 v 之間有多重邊（平行邊），用 parent 判斷可能出錯。更嚴謹的做法是用邊的編號來判斷。

#### 6.2.2 Union-Find 方法

```
HAS-CYCLE-UNION-FIND(G):
    初始化 Union-Find，每個頂點各自為一個集合

    for each edge {u, v} ∈ E:
        root_u ← FIND(u)
        root_v ← FIND(v)
        if root_u == root_v:
            return true            // u 和 v 已連通，再加邊就形成環
        UNION(root_u, root_v)

    return false
```

**時間複雜度**：O(E × α(V))，其中 α 是 inverse Ackermann function（幾乎是常數）。

**Union-Find vs DFS 的比較**：
| 面向 | DFS | Union-Find |
|------|-----|------------|
| 時間 | O(V + E) | O(E α(V)) ≈ O(E) |
| 適用 | 有向圖和無向圖 | **只適用無向圖** |
| 額外功能 | 可以找到環的具體位置 | 只能判斷有沒有環 |
| 線上處理 | 需要重新 DFS | 可以**動態加邊**並判斷 |

---

## 7. 二部圖判斷（Bipartite Checking）

### 7.1 定義

一個圖是**二部圖（Bipartite Graph）**，如果可以把頂點分成兩組 L 和 R，使得所有邊都是一端在 L、一端在 R（沒有同組內的邊）。

**等價條件**：圖是二部圖 ⟺ 圖沒有奇數長度的環。

### 7.2 BFS 上色法

**想法**：用 BFS 做「二著色」。把起點塗成紅色，它的鄰居塗成藍色，藍色的鄰居塗成紅色，以此類推。如果發現某個鄰居已經被塗成跟自己相同的顏色 → 不是二部圖。

### 7.3 虛擬碼

```
IS-BIPARTITE(G):
    for each vertex u ∈ V:
        u.color ← UNCOLORED

    for each vertex u ∈ V:            // 處理不連通圖
        if u.color == UNCOLORED:
            if not BFS-BIPARTITE(G, u):
                return false
    return true

BFS-BIPARTITE(G, s):
    s.color ← RED
    Q ← [s]

    while Q is not empty:
        u ← DEQUEUE(Q)
        for each v ∈ Adj[u]:
            if v.color == UNCOLORED:
                v.color ← opposite(u.color)   // RED→BLUE, BLUE→RED
                ENQUEUE(Q, v)
            else if v.color == u.color:
                return false                   // 同色鄰居 → 有奇環 → 不是二部圖
    return true
```

### 7.4 計算範例

**例 1：二部圖**

```
    A --- B
    |     |
    C --- D

BFS from A:
  A: RED, Q = [A]
  DEQUEUE A: B(UNCOLORED)→BLUE, C(UNCOLORED)→BLUE
    Q = [B, C]
  DEQUEUE B: A(RED≠BLUE ✓), D(UNCOLORED)→RED
    Q = [C, D]
  DEQUEUE C: A(RED≠BLUE ✓), D(RED≠BLUE ✓)
    Q = [D]
  DEQUEUE D: B(BLUE≠RED ✓), C(BLUE≠RED ✓)
    Q = []

結果: 二部圖！ L = {A, D}(RED), R = {B, C}(BLUE)
```

**例 2：非二部圖**

```
    A --- B
    |   / |
    C --- D
    (三角形 A-B-C 存在)

邊: A-B, A-C, B-C, B-D, C-D

BFS from A:
  A: RED, Q = [A]
  DEQUEUE A: B(UNCOLORED)→BLUE, C(UNCOLORED)→BLUE
    Q = [B, C]
  DEQUEUE B: A(RED≠BLUE ✓), C(BLUE==BLUE ✗) → 衝突！

結果: 不是二部圖！
（因為 A-B-C 是奇數長度的環，長度 3）
```

### 7.5 正確性

**定理**：BFS 上色法正確判斷二部圖。

**證明**：
- 如果圖是二部圖：存在合法的二著色。BFS 上色法會找到一個（因為 BFS 按層交替著色，第 0, 2, 4... 層一色，第 1, 3, 5... 層另一色）。不會出現同色衝突。
- 如果圖不是二部圖：存在奇環。在 BFS 中，奇環的某條邊兩端會在同一層或相鄰的奇數層差，導致同色衝突。

**時間複雜度**：O(V + E)（就是一次 BFS）

---

## 8. 無向圖 DFS 的特殊性質

### 8.1 性質陳述

**定理**：在無向圖的 DFS 中，只會出現 Tree Edge 和 Back Edge。不會有 Forward Edge 和 Cross Edge。

這是一個非常重要的性質，跟有向圖的 DFS 有本質區別。

### 8.2 推導：為什麼沒有 Forward Edge？

**什麼是 Forward Edge？** 在有向圖中，(u, v) 是 Forward Edge 代表 v 是 u 的後代（在 DFS 樹中），而且 v 不是透過 (u, v) 這條邊被發現的。

在無向圖中，假設 (u, v) 是一條非樹邊，且 v 是 u 的後代。那麼：
- v 在 DFS 樹中是 u 的後代
- 當 DFS 到達 v 時，v 被某個 u 的後代（或 u 本身）發現
- 但考慮 DFS-VISIT(v) 的過程：v 的鄰居包含 u（因為是無向圖）
- 在 DFS-VISIT(v) 中掃描到 u 時，u 的狀態是 GRAY（因為 u 是 v 的祖先，尚未完成）
- 所以邊 (v, u) 被判定為 **Back Edge**

那邊 (u, v) 呢？其實在無向圖中，邊 {u, v} 只被分類一次——在 DFS 先處理到它的那個方向分類。

如果先處理 (u, v) 方向（在 DFS-VISIT(u) 時）：
- 如果 v 是 WHITE：(u, v) 是 Tree Edge
- 如果 v 是 GRAY：(u, v) 是 Back Edge（v 是 u 的祖先）
- v 不可能是 BLACK（見下面的證明）

**關鍵觀察：在無向圖的 DFS 中，掃描到的非 WHITE 鄰居一定是 GRAY，不可能是 BLACK。**

### 8.3 推導：為什麼沒有 Cross Edge？

**什麼是 Cross Edge？** (u, v) 是 Cross Edge 代表 u 和 v 不在同一棵 DFS 子樹的祖先-後代關係中，而且 v 已經完成（BLACK）。

**反證法**：假設在無向圖 DFS 中存在 Cross Edge (u, v)，其中 v 是 BLACK。

由於 v 是 BLACK，v 已經完全處理完畢。在 DFS-VISIT(v) 過程中，v 的所有鄰居都會被掃描。因為是無向圖，u 是 v 的鄰居。所以在 DFS-VISIT(v) 中，u 會被掃描到。

此時 u 的狀態是什麼？
- 如果 u 是 WHITE：(v, u) 會是 Tree Edge，u 成為 v 的後代 → v.d < u.d < u.f < v.f → 當後來 DFS-VISIT(u) 掃描到 v 時，v 已經 BLACK 且 v.d < u.d，但 v 是 u 的祖先而非「不相關的頂點」→ 矛盾（不會是 Cross Edge，如果 v 是 u 的祖先那應該 v.f > u.f，但 v 已 BLACK 表示 v.f 已設定且 v.f < u 開始處理時的 time...）

讓我重新用更清晰的方式推導。

**更清晰的推導**：

假設在 DFS-VISIT(u) 中掃描到邊 {u, v}，而 v 是 BLACK。

v 是 BLACK 意味著 DFS-VISIT(v) 已經開始並結束了。在 DFS-VISIT(v) 的過程中，v 一定掃描過它的所有鄰居，包括 u（因為是無向邊）。

在 DFS-VISIT(v) 掃描 u 時，如果 u 是 WHITE，DFS 會進入 u（tree edge），使 u 成為 v 的後代。那麼 u.f < v.f，且 v 在 u 完成之後才能完成。但我們此刻正在 DFS-VISIT(u) 中（u 是 GRAY），所以 u 還沒完成。這代表 v 也不可能已完成（因為 u 是 v 的後代，u 沒完成 v 就不能完成）。矛盾！所以 v 不可能是 BLACK 在 u 是 GRAY 的情況下。

等等，讓我再理清：我們說的是「在 DFS-VISIT(u) 中掃描到 v，v 是 BLACK」。這意味著 v.f 已經被設定了（v 完成了）。

回想一下 DFS-VISIT(v) 時掃描到 u 的情況：
- 如果那時 u 是 WHITE：u 會成為 v 的後代，DFS 會先完成 u 再完成 v。但此刻 u 正在被處理（GRAY）而 v 已完成（BLACK），這表示 u 在 v 完成後才開始或仍在處理——但如果 u 是 v 的後代，u 應該在 v 之前完成。矛盾。

更精確地說：
- 如果 DFS-VISIT(v) 掃描 u 時 u 是 WHITE → u 成為 v 的後代 → u.d > v.d 且 u.f < v.f → 括號 [u.d, u.f] ⊂ [v.d, v.f] → 在 u 完成之前 v 不能完成 → v.f > u.f → 但現在 u 還在 GRAY 而 v 已 BLACK → v 在 u 完成前就完成了 → v.f < u.f → 矛盾！

- 如果 DFS-VISIT(v) 掃描 u 時 u 是 GRAY → 邊 {v, u} 被分類為 Back Edge（u 是 v 的祖先）→ 也就是說 u 在 DFS 樹中是 v 的祖先 → 此時 v 在 u 的子樹中 → v 必須在 u 之前完成。但我們現在在 DFS-VISIT(u) 中，u 是 GRAY，v 是 BLACK。如果 v 是 u 的後代，那 v.f < u.f 是合理的。**但這不是 Cross Edge，而是 Forward Edge（如果從 u 看向 v）或者說 v 是 u 的後代。**

  但等等，如果 v 是 u 的後代，那 v 一定是在 DFS-VISIT(u) 的某個遞迴呼叫中被訪問的。所以 v 的 discovery time > u 的 discovery time。在 DFS-VISIT(u) 中掃描到已完成的後代 v，這在有向圖中是 Forward Edge。但在無向圖中，這種情況不會發生：

  v 是 u 的後代，在 DFS 樹中 u 到 v 有一條路徑。在 DFS-VISIT(v) 中掃描到 u 時，u 是 GRAY → 被分類為 Back Edge。邊 {u, v} 已經在 DFS-VISIT(v) 時被「使用」了（作為 back edge 從 v 的角度看）。後來在 DFS-VISIT(u) 中再掃描到 v 時...

  實際上，無向圖的邊 {u, v} 在 DFS 中會被掃描兩次（從 u 看一次，從 v 看一次），但我們通常只在第一次遇到時分類。

讓我給一個更簡潔的證明：

### 8.4 簡潔證明

**定理**：在無向圖 DFS 中，不存在 Cross Edge。

**證明**：假設存在邊 {u, v}，在 DFS-VISIT(u) 中掃描到 v 時 v 是 BLACK（已完成），且 u 和 v 沒有祖先-後代關係（即 cross edge 的定義）。

由括號定理，u 和 v 的時間戳區間不重疊：要嘛 [u.d, u.f] 和 [v.d, v.f] 完全分開。

因為 v 已完成（BLACK），v.f < 當前時間 ≤ u.f。又因為我們假設不重疊且沒有包含關係，所以 v.f < u.d（v 在 u 開始之前就結束了）。

但這意味著在 DFS-VISIT(v) 的過程中，u 還是 WHITE。DFS-VISIT(v) 會掃描 v 的所有鄰居，包括 u。因為 u 是 WHITE，DFS 會呼叫 DFS-VISIT(u)，使 u 成為 v 的後代。但這就有了祖先-後代關係，跟我們的假設矛盾！

所以 Cross Edge 不存在。

**同理可得 Forward Edge 也不存在**：如果 v 是 u 的後代且 v 已完成，那 {u, v} 這條邊在 DFS-VISIT(v) 時就會被看到（v 掃描 u，u 是 GRAY → back edge），而不是等到 DFS-VISIT(u) 才分類為 forward edge。由於無向邊是雙向的，它在第一次被分類時就「確定了」。

**結論**：無向圖 DFS 中，每條非樹邊都是 Back Edge。

### 8.5 直覺總結

**為什麼有向圖可以有 Cross Edge 和 Forward Edge，而無向圖不行？**

關鍵在於**無向邊是雙向的**。如果 v 在 u 「不知道」的情況下被訪問完了（這是有向圖中 Cross Edge 的場景），那在無向圖中，v 在被訪問的過程中一定會看到 u（因為邊是雙向的），而那時候 u 如果是 WHITE，v 就會先把 u 拉進自己的子樹。所以不可能存在「互不相干的兩棵子樹之間有邊」的情況。

換句話說：**無向圖的 DFS 特別「貪心」——任何跟你相鄰的白色頂點都會被你拉進來，不可能被別人先拉走而你不知道。**

---

## 常見陷阱

### 陷阱 1：BFS/DFS 忘了處理不連通圖

如果圖不連通，從一個頂點出發的 BFS/DFS 只能到達同一個連通分量的頂點。別忘了外層迴圈！

### 陷阱 2：混淆有向圖和無向圖的邊分類

有向圖有四種邊，無向圖只有兩種。考試時一定要先確認是有向還是無向圖。

### 陷阱 3：無向圖 DFS 環偵測忘了排除父節點

無向邊 {u, v} 會在鄰接表中出現兩次。從 u 到 v 後，v 的鄰居列表中有 u，但這不代表有環——只是同一條邊。要傳入 parent 參數來避免。

### 陷阱 4：拓撲排序搞混方向

DFS 方法是按 finish time **遞減**排序（最後完成的排前面）。不是 discovery time！也不是遞增！

### 陷阱 5：Kosaraju 的第二次 DFS 忘了用反向圖

第一次 DFS 用原圖 G，第二次用 G^T。順序不能搞反。

### 陷阱 6：Tarjan 演算法的 low-link 更新

- Tree edge child v：`u.low = min(u.low, v.low)`
- Back edge to v（v on stack）：`u.low = min(u.low, v.d)`
- v 不在 stack 上（已屬於某個 SCC）：**不更新**

最後一點很容易忘記。如果 v 已經被 pop 出 stack（屬於另一個已確定的 SCC），就不應該用它來更新 u 的 low-link。

### 陷阱 7：時間複雜度 O(V+E) 的推導

不是「每個頂點做 O(E) 的工作」（那樣是 O(VE)），而是「所有頂點加起來做 O(E) 的工作」。這是 aggregate analysis。考試時如果要推導，要說清楚這一點。

### 陷阱 8：二部圖判斷忘了處理所有連通分量

圖的每個連通分量可以獨立判斷是否二部。要對所有未上色的頂點都做一次 BFS。

### 陷阱 9：SCC 在無向圖上沒有意義

SCC 是有向圖的概念。在無向圖中，對應的概念是「連通分量」（Connected Component），用 BFS/DFS 就能找到，不需要 Kosaraju 或 Tarjan。

### 陷阱 10：DAG 和拓撲排序的前提

拓撲排序只能對 **DAG** 做。如果圖有環，就沒有拓撲排序。記得先判斷有沒有環！

---

## 小結

| 主題 | 關鍵重點 |
|------|---------|
| 圖的表示法 | Matrix: O(V²) 空間，O(1) 查邊；List: O(V+E) 空間，O(deg) 查邊 |
| BFS | Queue，O(V+E)，無權圖最短路，層次遍歷 |
| DFS | 遞迴/Stack，O(V+E)，discovery/finish time，四種邊分類 |
| 括號定理 | 時間戳區間要嘛包含要嘛不重疊 |
| 白色路徑定理 | v 是 u 的後代 ⟺ u 發現時有全白路到 v |
| 拓撲排序 | DFS finish time 遞減 或 Kahn's BFS，只對 DAG |
| SCC | Kosaraju (2次DFS) 或 Tarjan (1次DFS+low-link) |
| 環偵測 | 有向：back edge；無向：DFS+parent 或 Union-Find |
| 二部圖 | BFS 上色，有奇環就不是二部圖 |
| 無向圖 DFS | 只有 Tree Edge 和 Back Edge（沒有 Cross/Forward） |

---

## 自我檢測題

### 觀念題

1. **BFS vs DFS**：
   - (a) BFS 用什麼資料結構？DFS 用什麼？
   - (b) 哪一個能找到無權圖的最短路徑？
   - (c) 如果你想「一條路走到底再回頭」，你用哪個？

2. **圖的表示法**：什麼情況用 Adjacency Matrix 比較好？什麼情況用 Adjacency List？

3. **拓撲排序**：以下圖能做拓撲排序嗎？為什麼？
   - (a) A → B → C → A
   - (b) A → B, A → C, B → D, C → D

4. **四種邊**：在有向圖的 DFS 中，看到灰色的鄰居代表什麼類型的邊？這代表圖有什麼性質？

### 計算題

5. **BFS 手動追蹤**：對以下圖從 A 出發做 BFS，寫出每步的 Queue 狀態和每個節點的距離。
   ```
   A → B, A → C, B → D, C → D, D → E
   ```

6. **DFS 手動追蹤**：對上面同一張圖從 A 出發做 DFS，寫出每個節點的 discovery time 和 finish time。

7. **拓撲排序（Kahn's Algorithm）**：對以下 DAG 用 Kahn's Algorithm（入度法）求拓撲排序。
   ```
   修課圖：
   微積分 → 線代
   微積分 → 機率
   程設 → 資結
   線代 → 演算法
   資結 → 演算法
   ```

8. **環偵測**：以下有向圖有環嗎？用 DFS 的 back edge 概念判斷。
   ```
   A → B, B → C, C → D, D → B
   ```

9. **SCC**：對以下有向圖找出所有的強連通分量。
   ```
   1 → 2, 2 → 3, 3 → 1, 3 → 4, 4 → 5, 5 → 4
   ```

### 參考答案提示

- 第 1(a) 題：BFS 用 Queue（先進先出），DFS 用 Stack 或遞迴（後進先出）
- 第 1(b) 題：BFS
- 第 3(a) 題：不能，因為有環 A→B→C→A
- 第 3(b) 題：能，因為是 DAG。一個合法排序是 A, B, C, D（或 A, C, B, D）
- 第 4 題：Back Edge，代表圖中有環
- 第 7 題：初始入度：微積分(0), 程設(0), 線代(1), 機率(1), 資結(1), 演算法(2)。可能的排序：微積分, 程設, 線代, 機率, 資結, 演算法
- 第 8 題：有環 B→C→D→B。DFS 中從 D 看到灰色的 B 時會發現 back edge
- 第 9 題：SCC 1 = {1, 2, 3}（互相可達），SCC 2 = {4, 5}（互相可達）
