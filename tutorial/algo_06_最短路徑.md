# 演算法筆記 06：最短路徑 (Shortest Paths)

> 台大演算法課教學講義
> 本篇涵蓋：Dijkstra、Bellman-Ford、DAG 最短路、Floyd-Warshall、Johnson's Algorithm

---

## 一、最短路徑問題分類

最短路徑是圖論中最經典的問題之一。在正式講演算法之前，我們先把問題分清楚，因為**不同的情境要用不同的演算法**。

### 1.1 依「問幾組答案」分類

| 類型 | 說明 | 代表演算法 |
|------|------|-----------|
| **單源最短路 (Single-Source Shortest Paths, SSSP)** | 給定一個起點 s，求 s 到所有其他點的最短距離 | Dijkstra、Bellman-Ford、DAG relaxation |
| **全對最短路 (All-Pairs Shortest Paths, APSP)** | 求任意兩點之間的最短距離 | Floyd-Warshall、Johnson's |

### 1.2 依「邊的性質」分類

| 邊的性質 | 可用演算法 | 備註 |
|----------|-----------|------|
| **正權邊 (非負權)** | Dijkstra | 最快的 SSSP |
| **可能有負權邊（但無負環）** | Bellman-Ford | 較慢但能處理負權 |
| **DAG（有向無環圖）** | 拓撲排序 + relaxation | 可處理負權，且只要 O(V+E) |
| **可能有負環** | Bellman-Ford 可偵測 | Floyd-Warshall 也能偵測 |

**重要觀念**：「負環」讓最短路徑沒有意義——你可以一直繞負環讓距離趨近 -∞。所以我們通常假設「沒有負環」，或者只是要偵測負環是否存在。

---

## 二、Relaxation（鬆弛）的概念

### 2.1 什麼是 Relaxation？

所有最短路演算法的核心操作都是同一個——**relaxation（鬆弛）**。

想像你目前估計從 s 到 v 的最短距離是 `dist[v] = 10`。現在你發現有一條邊 (u, v)，而 `dist[u] + w(u,v) = 7`。既然有更短的路，你當然要更新！這個「嘗試用更短的路來更新估計值」的操作，就叫 relaxation。

```
RELAX(u, v, w):
    if dist[v] > dist[u] + w(u, v):
        dist[v] = dist[u] + w(u, v)
        pred[v] = u          // 記錄前驅節點，方便之後回溯路徑
```

### 2.2 Relaxation 的重要性質

**性質 1（上界性質, Upper-Bound Property）**：
在整個演算法過程中，`dist[v]` 永遠 >= 實際最短距離 δ(s,v)。一旦 `dist[v] = δ(s,v)`，它就不會再改變。

> **推導**：初始時 `dist[s] = 0 = δ(s,s)`，`dist[v] = ∞ ≥ δ(s,v)` 對所有 v ≠ s。每次 relax 操作設定 `dist[v] = dist[u] + w(u,v)`。因為 δ(s,v) ≤ δ(s,u) + w(u,v)（三角不等式），且 dist[u] ≥ δ(s,u)（歸納假設），所以更新後 dist[v] = dist[u] + w(u,v) ≥ δ(s,u) + w(u,v) ≥ δ(s,v)。也就是 dist[v] 永遠不會小於真正的最短距離。

**性質 2（路徑鬆弛性質, Path Relaxation Property）**：
如果 s → v₁ → v₂ → ... → vₖ 是 s 到 vₖ 的最短路，而我們**依序**對 (s,v₁), (v₁,v₂), ..., (vₖ₋₁,vₖ) 做 relax（中間可以穿插其他 relax），那麼最終 `dist[vₖ] = δ(s,vₖ)`。

> **推導**：用數學歸納法。relax (s,v₁) 之後，dist[v₁] ≤ dist[s] + w(s,v₁) = 0 + w(s,v₁) = δ(s,v₁)。又由上界性質 dist[v₁] ≥ δ(s,v₁)，所以 dist[v₁] = δ(s,v₁)。然後 relax (v₁,v₂)，同理得 dist[v₂] = δ(s,v₂)。以此類推到 vₖ。

這個性質是 Bellman-Ford 正確性的基礎。

**性質 3（收斂性質, Convergence Property）**：
如果 s ⇝ u → v 是某條最短路，且在 relax(u,v) 之前已經有 dist[u] = δ(s,u)，那麼 relax 之後 dist[v] = δ(s,v)。

---

## 三、Dijkstra 演算法

### 3.1 適用條件

**所有邊權 w(u,v) ≥ 0**。這是 Dijkstra 最重要的前提。

### 3.2 核心思路

Dijkstra 是一個 **greedy** 演算法。它維護一個集合 S，代表「已經確定最短距離的點」。每次從「還沒確定的點」中，挑 dist 值最小的點 u 加入 S，然後用 u 去 relax 它的所有鄰居。

直覺上：如果所有邊都非負，那「目前 dist 最小的未確定點」一定已經是最短距離了——因為沒有任何其他路能繞過來讓它更短。

### 3.3 完整虛擬碼

```
DIJKSTRA(G, w, s):
    // 初始化
    for each vertex v in G.V:
        dist[v] = ∞
        pred[v] = NIL
    dist[s] = 0

    S = ∅                       // 已確定最短距離的頂點集合
    Q = MIN-PRIORITY-QUEUE(G.V) // 以 dist 值為 key 的最小優先佇列

    while Q is not empty:
        u = EXTRACT-MIN(Q)      // 取出 dist 最小的頂點
        S = S ∪ {u}
        for each edge (u, v) in G.Adj[u]:
            if dist[v] > dist[u] + w(u, v):
                dist[v] = dist[u] + w(u, v)
                pred[v] = u
                DECREASE-KEY(Q, v, dist[v])

    return dist[], pred[]
```

### 3.4 正確性推導

**定理**：當頂點 u 從優先佇列中被 extract 出來時，dist[u] = δ(s, u)。

**證明（反證法 + 歸納法）**：

假設 u 是**第一個**被 extract 出來時 dist[u] ≠ δ(s,u) 的頂點。

1. u ≠ s（因為 dist[s] = 0 = δ(s,s)）。
2. 在 u 被 extract 之前，S 中所有頂點 v 都有 dist[v] = δ(s,v)（因為 u 是第一個出錯的）。
3. 因為 dist[u] ≠ δ(s,u)，由上界性質知 dist[u] > δ(s,u)。所以存在一條從 s 到 u 的最短路 P。
4. 考慮路徑 P 上，第一個不在 S 中的頂點 y（它前面的頂點 x 在 S 中）。
5. 因為 x 在 S 中且 dist[x] = δ(s,x)，而且 (x,y) 已經被 relax 過（x 被 extract 時做的），所以 dist[y] = δ(s,y)。
6. 因為 y 在從 s 到 u 的最短路上，且**邊權非負**：

   δ(s,y) ≤ δ(s,u) < dist[u]

7. 但 u 是從 Q 中被 extract 出來的最小值！所以 dist[u] ≤ dist[y] = δ(s,y)。
8. 這和第 6 步矛盾。所以假設不成立，u 不可能出錯。 ∎

**關鍵**：第 6 步用到「邊權非負」。如果有負權邊，δ(s,y) 可能 > δ(s,u)，整個推導就崩掉了。

### 3.5 時間複雜度推導

Dijkstra 的時間取決於優先佇列的實作方式。

**操作次數分析**：
- EXTRACT-MIN 被呼叫 |V| 次（每個點 extract 一次）
- DECREASE-KEY 最多被呼叫 |E| 次（每條邊最多觸發一次 relax）

| 優先佇列實作 | EXTRACT-MIN | DECREASE-KEY | 總時間 |
|-------------|-------------|-------------|--------|
| Array（陣列） | O(V) | O(1) | O(V²) |
| Binary Heap（二元堆） | O(log V) | O(log V) | O((V+E) log V) |
| Fibonacci Heap（費式堆） | O(log V) amortized | O(1) amortized | O(E + V log V) |

**推導（Binary Heap）**：
- V 次 EXTRACT-MIN，每次 O(log V) → O(V log V)
- 最多 E 次 DECREASE-KEY，每次 O(log V) → O(E log V)
- 總計：O(V log V + E log V) = O((V+E) log V)

**推導（Fibonacci Heap）**：
- V 次 EXTRACT-MIN，每次 amortized O(log V) → O(V log V)
- 最多 E 次 DECREASE-KEY，每次 amortized O(1) → O(E)
- 總計：O(V log V + E) = O(E + V log V)

> **實務上**：Binary heap 最常用。Fibonacci heap 理論上更快，但常數大、實作複雜，實務中不一定真的比較快。對稠密圖（E ≈ V²），array 版的 O(V²) 反而可能最快。

### 3.6 手動 Trace Through 範例

考慮以下有向圖：

```
頂點：{A, B, C, D, E}
邊：
  A → B : 10
  A → C : 3
  B → C : 1
  B → D : 2
  C → B : 4
  C → D : 8
  C → E : 2
  D → E : 7
  E → D : 9
```

起點 s = A。

**初始狀態**：

| 頂點 | dist | pred | 在 Q 中？ |
|------|------|------|----------|
| A | 0 | NIL | Yes |
| B | ∞ | NIL | Yes |
| C | ∞ | NIL | Yes |
| D | ∞ | NIL | Yes |
| E | ∞ | NIL | Yes |

---

**第 1 步：Extract-Min → A (dist=0)**

S = {A}

Relax A 的鄰居：
- Relax(A, B): dist[B] = min(∞, 0+10) = 10, pred[B] = A
- Relax(A, C): dist[C] = min(∞, 0+3) = 3, pred[C] = A

| 頂點 | dist | pred | 在 Q 中？ |
|------|------|------|----------|
| A | **0** | NIL | No (已 extract) |
| B | 10 | A | Yes |
| C | 3 | A | Yes |
| D | ∞ | NIL | Yes |
| E | ∞ | NIL | Yes |

---

**第 2 步：Extract-Min → C (dist=3)**

S = {A, C}

Relax C 的鄰居：
- Relax(C, B): dist[B] = min(10, 3+4) = 7, pred[B] = C  ← 更新了！
- Relax(C, D): dist[D] = min(∞, 3+8) = 11, pred[D] = C
- Relax(C, E): dist[E] = min(∞, 3+2) = 5, pred[E] = C

| 頂點 | dist | pred | 在 Q 中？ |
|------|------|------|----------|
| A | **0** | NIL | No |
| B | 7 | C | Yes |
| C | **3** | A | No |
| D | 11 | C | Yes |
| E | 5 | C | Yes |

---

**第 3 步：Extract-Min → E (dist=5)**

S = {A, C, E}

Relax E 的鄰居：
- Relax(E, D): dist[D] = min(11, 5+9) = 11, 不更新（14 > 11）

| 頂點 | dist | pred | 在 Q 中？ |
|------|------|------|----------|
| A | **0** | NIL | No |
| B | 7 | C | Yes |
| C | **3** | A | No |
| D | 11 | C | Yes |
| E | **5** | C | No |

---

**第 4 步：Extract-Min → B (dist=7)**

S = {A, C, E, B}

Relax B 的鄰居：
- Relax(B, C): dist[C] = min(3, 7+1) = 3, 不更新（C 已 extract）
- Relax(B, D): dist[D] = min(11, 7+2) = 9, pred[D] = B  ← 更新了！

| 頂點 | dist | pred | 在 Q 中？ |
|------|------|------|----------|
| A | **0** | NIL | No |
| B | **7** | C | No |
| C | **3** | A | No |
| D | 9 | B | Yes |
| E | **5** | C | No |

---

**第 5 步：Extract-Min → D (dist=9)**

S = {A, C, E, B, D}

Relax D 的鄰居：
- Relax(D, E): dist[E] = min(5, 9+7) = 5, 不更新

**最終結果**：

| 頂點 | δ(A, v) | 最短路 |
|------|---------|--------|
| A | 0 | A |
| B | 7 | A → C → B |
| C | 3 | A → C |
| D | 9 | A → C → B → D |
| E | 5 | A → C → E |

### 3.7 為什麼 Dijkstra 不能處理負權？

**反例**：

```
    A ---1--→ B
    |         |
    3        -5
    |         |
    ↓         ↓
    C ---2--→ D
```

邊：A→B:1, A→C:3, B→D:-5, C→D:2

Dijkstra 的執行：
1. Extract A (dist=0)：relax 得 dist[B]=1, dist[C]=3
2. Extract B (dist=1)：relax 得 dist[D]=1+(-5)=-4
3. Extract C (dist=3)：relax 得 dist[D]=min(-4, 3+2)=-4, 不更新
4. Extract D (dist=-4)

Dijkstra 得到 dist[D] = -4，路徑 A→B→D。這個例子碰巧是對的。

但換一個例子：

```
    A ---1--→ B ---1--→ C
    |                   ↑
    5                  -10
    |                   |
    ↓                   |
    D ------------------+
```

邊：A→B:1, B→C:1, A→D:5, D→C:-10

Dijkstra 的執行：
1. Extract A (dist=0)：relax 得 dist[B]=1, dist[D]=5
2. Extract B (dist=1)：relax 得 dist[C]=1+1=2
3. Extract C (dist=2)：**C 被鎖定為 dist=2**
4. Extract D (dist=5)：relax 得 dist[C]=min(2, 5+(-10))=min(2,-5)=-5
   但 C 已經被 extract 了！在標準 Dijkstra 中，C 不會被更新。

正確答案：δ(A,C) = 5 + (-10) = -5（走 A→D→C）
Dijkstra 的答案：dist[C] = 2（走 A→B→C）→ **錯誤！**

**原因**：Dijkstra 的正確性依賴「一旦 extract 出來就是最終答案」。這需要邊權非負——否則後面 extract 的點可能透過負權邊提供更短的路到之前已確定的點。

---

## 四、Bellman-Ford 演算法

### 4.1 適用條件

可以處理**負權邊**，並且能**偵測負環**。只要求沒有從 s 可達的負環。

### 4.2 核心思路

暴力但有效：對**所有邊**做 relaxation，重複 V-1 輪。

### 4.3 完整虛擬碼

```
BELLMAN-FORD(G, w, s):
    // 初始化
    for each vertex v in G.V:
        dist[v] = ∞
        pred[v] = NIL
    dist[s] = 0

    // 主迴圈：做 V-1 輪 relaxation
    for i = 1 to |V| - 1:
        for each edge (u, v) in G.E:
            RELAX(u, v, w)

    // 負環偵測
    for each edge (u, v) in G.E:
        if dist[v] > dist[u] + w(u, v):
            return "存在負環！"

    return dist[], pred[]
```

### 4.4 正確性推導

**定理**：如果圖 G 不包含從 s 可達的負環，那麼 Bellman-Ford 結束後，對所有從 s 可達的頂點 v，dist[v] = δ(s,v)。

**證明**：

利用**Path Relaxation Property**。

設 s = v₀ → v₁ → v₂ → ... → vₖ 是 s 到 vₖ 的某條最短路。因為沒有負環，最短路最多經過 V-1 條邊（不可能重複經過同一個頂點），所以 k ≤ V-1。

- 第 1 輪遍歷所有邊，一定會遍歷到邊 (v₀, v₁)，做了 relax(v₀, v₁)。
  由收斂性質，之後 dist[v₁] = δ(s, v₁)。
- 第 2 輪遍歷所有邊，一定會遍歷到邊 (v₁, v₂)，做了 relax(v₁, v₂)。
  因為 dist[v₁] 已經等於 δ(s, v₁)，由收斂性質，之後 dist[v₂] = δ(s, v₂)。
- ...
- 第 i 輪之後，dist[vᵢ] = δ(s, vᵢ)。
- 第 k 輪（k ≤ V-1）之後，dist[vₖ] = δ(s, vₖ)。

所以 V-1 輪之後，所有最短路都被正確計算。 ∎

### 4.5 為什麼做 V-1 輪？

任何最短路（在無負環圖中）最多包含 V-1 條邊（因為最短路不會重複經過頂點）。每一輪 relax 所有邊，至少能「確定」最短路上的一條邊。所以 V-1 輪就足以確定長度最多 V-1 條邊的最短路。

- 第 1 輪後：確定了最短路上第 1 條邊
- 第 2 輪後：確定了最短路上前 2 條邊
- ...
- 第 V-1 輪後：確定了最短路上所有邊

### 4.6 負環偵測

**原理**：V-1 輪之後，如果沒有負環，所有 dist 值都已經是最短距離，不可能再被 relax。

如果第 V 輪還能 relax 某條邊 (u,v)，即 `dist[v] > dist[u] + w(u,v)`，那就表示存在一個能讓距離無限縮小的負環。

**直覺理解**：V-1 輪足以處理任何最短路。如果第 V 輪還能改善，表示有一條「更短」的路用了 ≥ V 條邊，這只可能在有負環的情況下發生。

### 4.7 手動 Trace Through 範例

考慮以下有向圖：

```
頂點：{S, A, B, C, D}
邊：
  S → A : 6
  S → B : 7
  A → B : 8
  A → C : 5
  A → D : -4
  B → A : -3
  B → C : 9
  B → D : -2 (修正：此邊用於展示)
  C → B : -2 (修正：改用更簡單的例子)
  D → C : 7
  D → S : 2
```

讓我們用一個更清楚的小例子：

```
頂點：{S, A, B, C}
邊（共 5 條）：
  (S, A) : 5
  (S, B) : 8
  (A, B) : -3
  (A, C) : 6
  (B, C) : 3
```

起點 s = S。

假設每輪遍歷邊的順序為：(S,A), (S,B), (A,B), (A,C), (B,C)

**初始**：dist = [S:0, A:∞, B:∞, C:∞]

---

**第 1 輪**：

| 邊 | 條件 | 動作 | dist 更新 |
|----|------|------|----------|
| (S,A) | dist[A]=∞ > dist[S]+5=5 | relax | dist[A]=5, pred[A]=S |
| (S,B) | dist[B]=∞ > dist[S]+8=8 | relax | dist[B]=8, pred[B]=S |
| (A,B) | dist[B]=8 > dist[A]+(-3)=2 | relax | dist[B]=2, pred[B]=A |
| (A,C) | dist[C]=∞ > dist[A]+6=11 | relax | dist[C]=11, pred[C]=A |
| (B,C) | dist[C]=11 > dist[B]+3=5 | relax | dist[C]=5, pred[C]=B |

第 1 輪後：dist = [S:0, A:5, B:2, C:5]

---

**第 2 輪**：

| 邊 | 條件 | 動作 | dist 更新 |
|----|------|------|----------|
| (S,A) | dist[A]=5 > 0+5=5? No | 不更新 | |
| (S,B) | dist[B]=2 > 0+8=8? No | 不更新 | |
| (A,B) | dist[B]=2 > 5+(-3)=2? No | 不更新 | |
| (A,C) | dist[C]=5 > 5+6=11? No | 不更新 | |
| (B,C) | dist[C]=5 > 2+3=5? No | 不更新 | |

第 2 輪沒有任何更新 → 可以提前結束。

---

**第 3 輪 (V-1=3)**：同樣沒有更新。

**負環偵測**：再跑一輪，沒有任何 relax 成功 → 沒有負環。

**最終結果**：

| 頂點 | δ(S, v) | 最短路 |
|------|---------|--------|
| S | 0 | S |
| A | 5 | S → A |
| B | 2 | S → A → B |
| C | 5 | S → A → B → C |

注意 B 的最短路不是直接 S→B（距離 8），而是 S→A→B（距離 5+(-3)=2），負權邊讓繞路反而更短！

### 4.8 Dijkstra vs Bellman-Ford 比較

| 比較項目 | Dijkstra | Bellman-Ford |
|---------|----------|-------------|
| 時間複雜度 | O((V+E) log V) [binary heap] | O(VE) |
| 負權邊 | 不行 | 可以 |
| 負環偵測 | 不行 | 可以 |
| 思路 | Greedy | 暴力 relax V-1 輪 |
| 實務速度 | 快 | 慢 |
| 適用場景 | 邊權非負的 SSSP | 有負權邊的 SSSP |

---

## 五、DAG 最短路

### 5.1 核心思路

如果圖是 DAG（有向無環圖），就算有**負權邊**也不需要 Bellman-Ford！只要：

1. 做拓撲排序
2. 按拓撲序依次 relax 每個頂點的出邊

### 5.2 完整虛擬碼

```
DAG-SHORTEST-PATHS(G, w, s):
    topological_order = TOPOLOGICAL-SORT(G)

    for each vertex v in G.V:
        dist[v] = ∞
        pred[v] = NIL
    dist[s] = 0

    for each vertex u in topological_order:
        for each edge (u, v) in G.Adj[u]:
            RELAX(u, v, w)

    return dist[], pred[]
```

### 5.3 為什麼可以處理負權？

**關鍵洞察**：拓撲排序保證了——當我們處理頂點 u 時，所有指向 u 的邊 (x, u) 的起點 x 都已經被處理過了。

所以當我們 relax u 的出邊時，dist[u] 已經是最終的最短距離。這意味著：
- 不需要重複 relax（每條邊只被 relax 一次）
- 負權邊不會造成問題（因為沒有環，不會繞回來）

**正確性推導**：

設最短路為 s = v₀ → v₁ → ... → vₖ。在拓撲序中，v₀ 在 v₁ 前面，v₁ 在 v₂ 前面，以此類推。所以邊 (v₀,v₁) 在邊 (v₁,v₂) 之前被 relax。由 Path Relaxation Property，dist[vₖ] = δ(s,vₖ)。

### 5.4 時間複雜度

- 拓撲排序：O(V + E)
- 每條邊被 relax 恰好一次：O(V + E)
- 總計：**O(V + E)**

比 Dijkstra 和 Bellman-Ford 都快！

### 5.5 最長路的變形

在 DAG 中，最長路問題也可以用類似方法解決！（注意：在一般圖中，最長路是 NP-hard 問題。）

方法 1：把所有邊權取負，跑 DAG 最短路，結果再取負。

方法 2：直接修改 relax 操作：

```
// 原本（最短路）：
if dist[v] > dist[u] + w(u, v):
    dist[v] = dist[u] + w(u, v)

// 改為（最長路）：
if dist[v] < dist[u] + w(u, v):
    dist[v] = dist[u] + w(u, v)
```

初始化也要改：dist[s] = 0，其他設為 -∞。

---

## 六、Floyd-Warshall 演算法

### 6.1 適用場景

求**全對最短路（All-Pairs Shortest Paths）**。可以處理**負權邊**（但不能有負環）。

### 6.2 DP 遞迴式推導

這是一個精巧的 DP。把頂點編號為 1, 2, ..., n。

定義：**d^(k)[i][j]** = 從 i 到 j，只允許用 {1, 2, ..., k} 作為中繼點的最短距離。

基底情況（k = 0，不允許任何中繼點）：
```
d^(0)[i][j] = w(i, j)    如果 (i,j) 是邊
d^(0)[i][i] = 0
d^(0)[i][j] = ∞          其他
```

遞迴式：考慮中繼點 k 的兩種情況：
1. 最短路**不經過** k：那就是 d^(k-1)[i][j]
2. 最短路**經過** k：那就是 d^(k-1)[i][k] + d^(k-1)[k][j]

取較小的：

> **d^(k)[i][j] = min( d^(k-1)[i][j],  d^(k-1)[i][k] + d^(k-1)[k][j] )**

最終答案：d^(n)[i][j] = δ(i, j)。

**為什麼這是對的？** 因為 d^(n)[i][j] 允許所有頂點作為中繼點，所以就是真正的最短距離。

### 6.3 完整虛擬碼

```
FLOYD-WARSHALL(W):
    n = |V|
    D = W                    // D[i][j] = w(i,j)，初始化為鄰接矩陣
    // D[i][i] = 0 for all i
    // D[i][j] = ∞ if no edge (i,j)

    for k = 1 to n:                          // 中繼點
        for i = 1 to n:                      // 起點
            for j = 1 to n:                  // 終點
                if D[i][j] > D[i][k] + D[k][j]:
                    D[i][j] = D[i][k] + D[k][j]

    return D
```

**時間複雜度**：三層迴圈，每層 n → **O(V³)**
**空間複雜度**：O(V²)（可以原地更新，不需要存每一層的 D^(k)）

> **為什麼可以原地更新？** 在計算 D^(k) 時，D[i][k] 和 D[k][j] 不會被「更早」的 D^(k) 改變（因為 D^(k)[i][k] = D^(k-1)[i][k]，D^(k)[k][j] = D^(k-1)[k][j]——經過 k 到 k 等於直接到 k，加入中繼點 k 不會改變 i→k 或 k→j 的距離）。

### 6.4 手動 Trace Through 範例

考慮有向圖，頂點 {1, 2, 3, 4}：

```
邊：
  1 → 2 : 3
  1 → 3 : 8
  2 → 3 : 2
  2 → 4 : 1 (修正：改用完整例子)
  3 → 4 : 1
  4 → 1 : 2
  4 → 2 : -5 (此為負權邊)
```

繪製成鄰接矩陣：

**D^(0)（初始）**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 8 | ∞ |
| 2 | ∞ | 0 | 2 | 1 |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 2 | -5 | ∞ | 0 |

---

**k=1（中繼點 1）**：對所有 (i,j)，檢查 D[i][1] + D[1][j] 是否比 D[i][j] 小。

需要看哪些 i 可以到 1（即 D[i][1] ≠ ∞）：i=1 (D=0), i=4 (D=2)。
需要看 1 可以到哪些 j（即 D[1][j] ≠ ∞）：j=1 (D=0), j=2 (D=3), j=3 (D=8)。

有意義的更新（i=4 經過 1 到 j）：
- D[4][2] = min(-5, D[4][1]+D[1][2]) = min(-5, 2+3) = min(-5, 5) = -5，不變
- D[4][3] = min(∞, D[4][1]+D[1][3]) = min(∞, 2+8) = 10，**更新！**

**D^(1)**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 8 | ∞ |
| 2 | ∞ | 0 | 2 | 1 |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 2 | -5 | **10** | 0 |

---

**k=2（中繼點 2）**：

哪些 i 可以到 2？i=1 (D=3), i=2 (D=0), i=4 (D=-5)。
2 可以到哪些 j？j=2 (D=0), j=3 (D=2), j=4 (D=1)。

有意義的更新：
- D[1][3] = min(8, D[1][2]+D[2][3]) = min(8, 3+2) = 5，**更新！**
- D[1][4] = min(∞, D[1][2]+D[2][4]) = min(∞, 3+1) = 4，**更新！**
- D[4][3] = min(10, D[4][2]+D[2][3]) = min(10, -5+2) = -3，**更新！**
- D[4][4] = min(0, D[4][2]+D[2][4]) = min(0, -5+1) = -4...

等等，D[4][4] = -4 < 0？這表示從 4 出發繞回 4 的距離是負的 → **存在負環**！路徑是 4→1→2→4（距離 2+3+1=6）不對…讓我重新檢查。

4→2 (距離 -5)，2→4 (距離 1)，所以 4→2→4 距離 = -5+1 = -4 < 0。

確實存在負環 4→2→4（或者說 2→4→2 也是）。所以這個例子有負環。讓我修改例子。

**修改例子**（無負環版本）：

```
頂點 {1, 2, 3, 4}
邊：
  1 → 2 : 3
  1 → 3 : 8
  2 → 3 : 2
  3 → 4 : 1
  4 → 1 : 7
  4 → 2 : 4
```

**D^(0)（初始）**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 8 | ∞ |
| 2 | ∞ | 0 | 2 | ∞ |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 7 | 4 | ∞ | 0 |

---

**k=1（中繼點 1）**：檢查是否 D[i][j] > D[i][1] + D[1][j]

能到 1 的：i=1(0), i=4(7)。1 能到的：j=1(0), j=2(3), j=3(8)。

- D[4][2] = min(4, 7+3) = min(4, 10) = 4，不變
- D[4][3] = min(∞, 7+8) = 15，**更新！**

**D^(1)**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 8 | ∞ |
| 2 | ∞ | 0 | 2 | ∞ |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 7 | 4 | **15** | 0 |

---

**k=2（中繼點 2）**：

能到 2 的：i=1(3), i=2(0), i=4(4)。2 能到的：j=2(0), j=3(2)。

- D[1][3] = min(8, 3+2) = 5，**更新！**
- D[4][3] = min(15, 4+2) = 6，**更新！**

**D^(2)**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | **5** | ∞ |
| 2 | ∞ | 0 | 2 | ∞ |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 7 | 4 | **6** | 0 |

---

**k=3（中繼點 3）**：

能到 3 的：i=1(5), i=2(2), i=3(0), i=4(6)。3 能到的：j=3(0), j=4(1)。

- D[1][4] = min(∞, 5+1) = 6，**更新！**
- D[2][4] = min(∞, 2+1) = 3，**更新！**
- D[4][4] = min(0, 6+1) = 7，不變

**D^(3)**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 5 | **6** |
| 2 | ∞ | 0 | 2 | **3** |
| 3 | ∞ | ∞ | 0 | 1 |
| 4 | 7 | 4 | 6 | 0 |

---

**k=4（中繼點 4）**：

能到 4 的：i=1(6), i=2(3), i=3(1), i=4(0)。4 能到的：j=1(7), j=2(4), j=3(6)。

- D[1][1] = min(0, 6+7) = 0，不變
- D[1][2] = min(3, 6+4) = 3，不變
- D[1][3] = min(5, 6+6) = 5，不變
- D[2][1] = min(∞, 3+7) = 10，**更新！**
- D[2][2] = min(0, 3+4) = 0，不變
- D[2][3] = min(2, 3+6) = 2，不變
- D[3][1] = min(∞, 1+7) = 8，**更新！**
- D[3][2] = min(∞, 1+4) = 5，**更新！**
- D[3][3] = min(0, 1+6) = 0，不變

**D^(4)（最終結果）**：

|   | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 0 | 3 | 5 | 6 |
| 2 | **10** | 0 | 2 | 3 |
| 3 | **8** | **5** | 0 | 1 |
| 4 | 7 | 4 | 6 | 0 |

驗證：對角線都是 0（沒有負環）。

### 6.5 負環偵測

在 Floyd-Warshall 結束後，只需檢查對角線：

> 如果 D[i][i] < 0 對某個 i 成立，則圖中存在負環。

因為 D[i][i] 代表從 i 出發回到 i 的最短距離，如果小於 0，表示有一個總權重為負的環。

### 6.6 變形：Maximum Capacity Path

**問題**：在一個有容量的網路中，找從 i 到 j 的路徑，使得路徑上的**最小容量**最大化（瓶頸路徑問題）。

**修改方式**：
- 原本的 `+` 改成 `min`（路徑的容量 = 各邊容量的最小值）
- 原本的 `min` 改成 `max`（我們要最大化路徑容量）

```
// 原本：D[i][j] = min(D[i][j], D[i][k] + D[k][j])
// 改為：D[i][j] = max(D[i][j], min(D[i][k], D[k][j]))
```

初始化：D[i][j] = c(i,j) 如果有邊，否則 D[i][j] = 0（或 -∞）；D[i][i] = ∞。

---

## 七、Johnson's Algorithm（路徑重加權）

### 7.1 動機

- 如果要求 APSP 且有負權邊，Floyd-Warshall 要 O(V³)。
- 如果邊很少（稀疏圖），有沒有更快的方法？
- 想法：把負權邊「消除」，然後跑 V 次 Dijkstra。

### 7.2 核心概念：Reweighting

定義新權重：**w'(u, v) = w(u, v) + h(u) - h(v)**

其中 h(v) 是某個「勢函數」。

**性質 1**：新權重不改變最短路的「路徑選擇」。
> 因為 s → v₁ → v₂ → ... → t 的新總權重 = 原總權重 + h(s) - h(t)。h(s) - h(t) 對所有 s 到 t 的路都一樣，所以最短路不變。

**性質 2**：如果選 h(v) = δ(q, v)（q 是新加的虛擬源點，到所有頂點有邊權 0 的邊），那麼 w'(u,v) ≥ 0。
> 因為三角不等式：δ(q, v) ≤ δ(q, u) + w(u, v)，即 w(u,v) + h(u) - h(v) ≥ 0。

### 7.3 演算法步驟

```
JOHNSON(G, w):
    1. 新增虛擬源點 q，加邊 (q, v) 權重 0 對所有 v
    2. 用 Bellman-Ford 從 q 出發，計算 h(v) = δ(q, v)
       - 如果偵測到負環，回報
    3. 對每條邊：w'(u,v) = w(u,v) + h(u) - h(v)
    4. 對每個頂點 u，用 Dijkstra 以 u 為源點在 w' 上跑 SSSP
    5. 還原真正距離：δ(u,v) = dist'(u,v) - h(u) + h(v)
```

### 7.4 時間複雜度

- Bellman-Ford：O(VE)
- V 次 Dijkstra（binary heap）：V × O((V+E) log V)
- 總計：**O(V² log V + VE)**

對稀疏圖（E = O(V)），這是 O(V² log V)，遠比 Floyd-Warshall 的 O(V³) 快。

---

## 八、全部最短路演算法比較

| 演算法 | 問題類型 | 時間複雜度 | 負權邊？ | 負環偵測？ | 適用場景 |
|--------|---------|-----------|---------|-----------|---------|
| **Dijkstra** (binary heap) | SSSP | O((V+E) log V) | 不行 | 不行 | 邊權非負的 SSSP |
| **Dijkstra** (Fibonacci heap) | SSSP | O(E + V log V) | 不行 | 不行 | 邊權非負、邊很多 |
| **Bellman-Ford** | SSSP | O(VE) | 可以 | 可以 | 有負權邊的 SSSP |
| **DAG 最短路** | SSSP (DAG) | O(V + E) | 可以 | N/A (DAG 無環) | DAG 上的 SSSP |
| **Floyd-Warshall** | APSP | O(V³) | 可以 | 可以 | 稠密圖的 APSP |
| **Johnson's** | APSP | O(V² log V + VE) | 可以 | 可以 | 稀疏圖的 APSP |

### 選擇指南

```
需要 SSSP 還是 APSP？
├── SSSP
│   ├── 圖是 DAG？ → DAG 最短路 O(V+E)
│   ├── 邊權非負？ → Dijkstra O((V+E) log V)
│   └── 有負權邊？ → Bellman-Ford O(VE)
└── APSP
    ├── 稠密圖 (E ≈ V²)？ → Floyd-Warshall O(V³)
    └── 稀疏圖？ → Johnson's O(V² log V + VE)
```

---

## 九、常見陷阱

1. **用 Dijkstra 處理負權邊**：這是最常見的錯誤。就算「大部分」邊是正的、只有一條負權邊，Dijkstra 都可能給出錯誤答案。

2. **Bellman-Ford 的邊遍歷順序**：不影響正確性，但可能影響收斂速度。

3. **Floyd-Warshall 的迴圈順序**：k 必須在最外層！`for k, for i, for j` 不能寫成 `for i, for j, for k`。

4. **忘記初始化 dist[s] = 0**：這會讓所有距離都是 ∞。

5. **在 Dijkstra 中 extract 同一個點兩次**：如果用的是 lazy deletion 的 priority queue（例如 C++ 的 `priority_queue`），同一個點可能被 push 多次。要在 extract 時檢查是否已經處理過。

6. **Bellman-Ford 負環偵測只偵測「從 s 可達」的負環**：如果負環從 s 不可達，Bellman-Ford 不會偵測到。

7. **Floyd-Warshall 忘記處理 D[i][i] = 0**：初始化時對角線要設為 0。

8. **Johnson's Algorithm 忘記還原真正距離**：Dijkstra 在 reweighted graph 上得到的距離不是真正距離，要記得轉回來。

---

*最短路問題是圖論的基礎中的基礎，建議多手動 trace 幾次，直到完全內化為止。*
