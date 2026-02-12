# 演算法筆記 07：最小生成樹 (Minimum Spanning Tree, MST)

> 台大演算法課教學講義
> 本篇涵蓋：Cut Property、Cycle Property、Kruskal、Prim、Union-Find、MST 性質與常見問題

---

## 一、MST 問題定義

### 1.1 什麼是生成樹？

給定一個**連通無向圖** G = (V, E)，**生成樹 (Spanning Tree)** 是 G 的一個子圖 T = (V, E')，滿足：
1. T 包含 G 的**所有頂點**
2. T 是一棵**樹**（連通且無環）
3. T 恰好有 |V| - 1 條邊

### 1.2 什麼是最小生成樹？

如果每條邊 e 有權重 w(e)，那麼**最小生成樹 (MST)** 就是所有生成樹中，邊權總和最小的那一棵。

> **MST = argmin_{T 是生成樹} Σ_{e ∈ T} w(e)**

### 1.3 基本性質

- MST 不一定唯一（當有邊權相同時可能有多棵）
- 如果所有邊權互不相同，MST 唯一（後面會證明）
- MST 是**全域最佳**，不只是局部最佳

---

## 二、兩大核心定理

Kruskal 和 Prim 的正確性都建立在以下兩個定理上。這兩個定理非常重要，建議完整理解推導。

### 2.1 Cut Property（切割性質）

**定義 — Cut（切割）**：
把 V 分成兩個非空集合 S 和 V\S，這個劃分稱為一個 cut (S, V\S)。一條邊 (u,v) 如果 u ∈ S 且 v ∈ V\S（或反過來），就稱它**跨越 (cross)** 這個 cut。

**Cut Property 定理**：
設 (S, V\S) 是任意一個 cut，e 是跨越這個 cut 的**唯一最輕邊（strictly lightest crossing edge）**，那麼 e 必然在每一棵 MST 中。

更一般的版本（邊權可能相同）：設 (S, V\S) 是任意一個 cut，e 是跨越這個 cut 的**某一條最輕邊**，那麼存在一棵 MST 包含 e。

**完整推導**：

假設 T 是某棵 MST，且 e = (u, v) 是跨越 cut (S, V\S) 的唯一最輕邊，但 e ∉ T。我們要推出矛盾。

1. 因為 T 是生成樹且連通，T 中存在一條從 u 到 v 的路徑 P。
2. 路徑 P 從 u（在 S 中）走到 v（在 V\S 中），所以 P 上一定有另一條邊 e' 也跨越 cut (S, V\S)。
3. 因為 e 是唯一最輕的跨越邊，所以 w(e) < w(e')。
4. 構造新生成樹 T' = T - {e'} + {e}：
   - T' 仍然連通（因為 e' 被拿掉後 u 和 v 斷了，但 e 重新把它們接起來）
   - T' 仍然有 |V| - 1 條邊
   - T' 是生成樹
5. T' 的總權重 = w(T) - w(e') + w(e) < w(T)。
6. 這和 T 是 MST 矛盾！所以 e 必須在 T 中。 ∎

> **口語理解**：如果有一條邊是跨越某個切割的「獨一無二最輕」邊，它一定在 MST 中。因為如果不用它，就必須用更重的邊來連接兩側，成本更高。

### 2.2 Cycle Property（環性質）

**Cycle Property 定理**：
設 C 是圖 G 中的任意一個環，e 是 C 中的**唯一最重邊（strictly heaviest edge in cycle）**，那麼 e 不在任何 MST 中。

**完整推導**：

假設 T 是某棵 MST，e 是環 C 中的唯一最重邊，但 e ∈ T。我們要推出矛盾。

1. 從 T 中移除 e = (u, v)。因為 T 是樹，移除一條邊後會把 T 分成兩個連通分量，形成一個 cut (S, V\S)，其中 u ∈ S, v ∈ V\S。
2. 環 C 經過 e = (u, v)，且環的其他邊構成一條從 u 到 v 的路徑。這條路徑上一定有另一條邊 e' 也跨越 cut (S, V\S)。
3. 因為 e 是環 C 中的唯一最重邊，所以 w(e') < w(e)。
4. 構造 T' = T - {e} + {e'}：
   - T' 仍然連通（e' 重新連接了兩側）
   - T' 仍然有 |V| - 1 條邊
   - T' 是生成樹
5. w(T') = w(T) - w(e) + w(e') < w(T)。
6. 矛盾！所以 e ∉ T。 ∎

> **口語理解**：環中最重的邊是「多餘的」——把它拿掉，環上的其他邊仍能維持連通，而且總權重更小。

---

## 三、Kruskal 演算法

### 3.1 核心思路

把所有邊按權重排序，從最輕的開始，一條一條加入。如果加入這條邊**不會形成環**，就加；否則跳過。

### 3.2 完整虛擬碼

```
KRUSKAL(G, w):
    T = ∅                           // MST 的邊集合
    將 G.E 的所有邊按 w 值遞增排序

    // 初始化 Union-Find：每個頂點是自己的集合
    for each vertex v in G.V:
        MAKE-SET(v)

    for each edge (u, v) in sorted order:
        if FIND-SET(u) ≠ FIND-SET(v):  // u 和 v 不在同一個連通分量
            T = T ∪ {(u, v)}
            UNION(u, v)

    return T
```

### 3.3 正確性推導

**利用 Cut Property 證明**：

每次 Kruskal 加入一條邊 e = (u, v) 時，u 和 v 在不同的連通分量中。

設 S 是 u 所在的連通分量（就是目前的 Union-Find 集合）。那麼 (S, V\S) 是一個 cut。

邊 e 跨越了這個 cut。而且，所有**比 e 更輕**的跨越邊 e' 一定已經被考慮過了（因為我們按權重遞增處理）。如果 e' 也跨越這個 cut，那 e' 的兩端也分別在 S 和 V\S 中，但 e' 沒被加入 → 表示 e' 加入時會形成環 → 表示 e' 的兩端在之前已經被其他更輕的邊連通了 → 矛盾（e' 的兩端分別在 S 和 V\S 中，不可能已連通）。

所以 e 是跨越 cut (S, V\S) 的最輕邊。由 Cut Property，e 可以安全地被包含在某棵 MST 中。

透過歸納法，Kruskal 選的每一條邊都可以屬於某棵 MST → Kruskal 的結果是 MST。 ∎

### 3.4 時間複雜度推導

1. **排序**：O(E log E) = O(E log V)（因為 E ≤ V²，所以 log E ≤ 2 log V = O(log V)）
2. **Union-Find 操作**：
   - E 次 FIND-SET
   - 最多 V-1 次 UNION
   - 使用 union by rank + path compression → 每次操作 amortized O(α(V))
   - 總計 O(E · α(V))，其中 α 是極慢增長的反 Ackermann 函數（實際上可視為常數）

**總時間**：O(E log E) + O(E · α(V)) = **O(E log E)** = **O(E log V)**

排序是瓶頸。

### 3.5 Union-Find 資料結構

Union-Find（或 Disjoint Set Union, DSU）用來維護一堆不相交集合，支援兩個操作：
- **FIND(x)**：找 x 所屬集合的代表元素
- **UNION(x, y)**：合併 x 和 y 所在的集合

#### 基本實作：用樹（forest）

每個集合是一棵樹，根節點是代表元素。

```
MAKE-SET(x):
    parent[x] = x
    rank[x] = 0

FIND(x):
    if parent[x] ≠ x:
        parent[x] = FIND(parent[x])    // 路徑壓縮！
    return parent[x]

UNION(x, y):
    rx = FIND(x)
    ry = FIND(y)
    if rx == ry: return

    // Union by rank
    if rank[rx] < rank[ry]:
        parent[rx] = ry
    else if rank[rx] > rank[ry]:
        parent[ry] = rx
    else:
        parent[ry] = rx
        rank[rx] = rank[rx] + 1
```

#### 兩大優化

1. **Union by Rank（按秩合併）**：
   - 每個根有一個 rank（大約是樹高的上界）
   - 合併時，把 rank 小的掛到 rank 大的下面
   - 防止樹退化成鏈

2. **Path Compression（路徑壓縮）**：
   - FIND 時，把路上所有節點直接指向根
   - 大幅降低後續 FIND 的時間

兩個都用上之後，m 次操作的總時間是 O(m · α(n))，其中 α 是反 Ackermann 函數。

> α(n) 增長極慢：α(2^65536) = 5。對所有實際問題，α(n) ≤ 4，可以視為常數。

### 3.6 手動 Trace Through 範例

考慮以下無向圖：

```
頂點：{A, B, C, D, E, F}
邊（排序前）：
  (A, B) : 4
  (A, F) : 2
  (B, C) : 6
  (B, F) : 5
  (C, D) : 3
  (C, F) : 1
  (D, E) : 2
  (E, F) : 4
```

**步驟 1：排序邊**

| 排名 | 邊 | 權重 |
|------|-----|------|
| 1 | (C, F) | 1 |
| 2 | (A, F) | 2 |
| 3 | (D, E) | 2 |
| 4 | (C, D) | 3 |
| 5 | (A, B) | 4 |
| 6 | (E, F) | 4 |
| 7 | (B, F) | 5 |
| 8 | (B, C) | 6 |

**步驟 2：初始化**

每個頂點自成一個集合：{A}, {B}, {C}, {D}, {E}, {F}

**步驟 3：依序考慮每條邊**

| # | 邊 | 權重 | FIND | 動作 | 集合狀態 | T |
|---|-----|------|------|------|---------|---|
| 1 | (C,F) | 1 | C≠F | 加入！UNION(C,F) | {A},{B},{C,F},{D},{E} | {(C,F)} |
| 2 | (A,F) | 2 | A≠F(=C) | 加入！UNION(A,F) | {A,C,F},{B},{D},{E} | {(C,F),(A,F)} |
| 3 | (D,E) | 2 | D≠E | 加入！UNION(D,E) | {A,C,F},{B},{D,E} | {(C,F),(A,F),(D,E)} |
| 4 | (C,D) | 3 | C(=A)≠D | 加入！UNION(C,D) | {A,C,D,E,F},{B} | {(C,F),(A,F),(D,E),(C,D)} |
| 5 | (A,B) | 4 | A≠B | 加入！UNION(A,B) | {A,B,C,D,E,F} | {(C,F),(A,F),(D,E),(C,D),(A,B)} |
| 6 | (E,F) | 4 | E(=A)=F(=A) | 跳過（形成環） | - | - |
| 7 | (B,F) | 5 | B(=A)=F(=A) | 跳過 | - | - |
| 8 | (B,C) | 6 | B(=A)=C(=A) | 跳過 | - | - |

已選 5 條邊 = V-1 = 6-1，完成！

**MST 的邊**：{(C,F):1, (A,F):2, (D,E):2, (C,D):3, (A,B):4}
**MST 總權重**：1 + 2 + 2 + 3 + 4 = **12**

```
MST 結構：
    A ---4--- B
    |
    2
    |
    F ---1--- C ---3--- D ---2--- E
```

---

## 四、Prim 演算法

### 4.1 核心思路

從某個起始頂點開始，逐步**長大**——每次加入一條「從已選頂點到未選頂點」的最輕邊。

這和 Dijkstra 非常像！差別在於 priority queue 的 key：
- **Dijkstra**：key[v] = dist[s→v]（起點到 v 的最短距離）
- **Prim**：key[v] = 連接 v 到已選集合的最輕邊的權重

### 4.2 完整虛擬碼

```
PRIM(G, w, r):
    // r 是起始頂點（任意選）
    for each vertex v in G.V:
        key[v] = ∞         // 到已選集合的最小連接權重
        pred[v] = NIL
        in_MST[v] = false
    key[r] = 0

    Q = MIN-PRIORITY-QUEUE(G.V)   // 以 key 值為優先級

    while Q is not empty:
        u = EXTRACT-MIN(Q)
        in_MST[u] = true

        for each edge (u, v) in G.Adj[u]:
            if not in_MST[v] and w(u, v) < key[v]:
                key[v] = w(u, v)
                pred[v] = u
                DECREASE-KEY(Q, v, key[v])

    return pred[]   // pred 定義了 MST 的邊
```

### 4.3 正確性推導

**利用 Cut Property**：

每次 Prim extract 一個頂點 u 時，設 S 是目前 in_MST 為 true 的頂點集合（包含剛加入的 u 之前的那些）。

在加入 u 之前，(S, V\S) 是一個 cut。u 是 V\S 中 key 值最小的頂點，而 key[u] = w(pred[u], u)，這條邊 (pred[u], u) 跨越 cut (S, V\S)。

key[u] 是最小的，表示 (pred[u], u) 是跨越 cut 的最輕邊（或之一）。

由 Cut Property，這條邊可以安全地被包含在 MST 中。 ∎

### 4.4 時間複雜度推導

和 Dijkstra 完全一樣的分析：
- EXTRACT-MIN：|V| 次
- DECREASE-KEY：最多 |E| 次

| 優先佇列 | 總時間 |
|----------|--------|
| Array | O(V²) |
| Binary Heap | O((V+E) log V) = **O(E log V)** |
| Fibonacci Heap | O(E + V log V) |

> 對稠密圖 (E ≈ V²)，array 版本的 O(V²) 反而比 binary heap 版本好。

### 4.5 Prim vs Dijkstra 的相似性和差異

| | Prim | Dijkstra |
|---|------|----------|
| 問題 | MST | SSSP |
| key 的意義 | 到已選集合的最輕邊權重 | 從 s 到該點的最短距離 |
| 更新規則 | key[v] = w(u,v) | dist[v] = dist[u] + w(u,v) |
| 貪心策略 | 選最輕的跨越邊 | 選最近的未確定點 |
| 正確性基礎 | Cut Property | Greedy + 非負邊權 |
| 虛擬碼結構 | 幾乎一模一樣 | 幾乎一模一樣 |

**關鍵差異在更新規則**：
- Prim：`if w(u,v) < key[v]: key[v] = w(u,v)`  （只看這條邊本身的權重）
- Dijkstra：`if dist[u]+w(u,v) < dist[v]: dist[v] = dist[u]+w(u,v)` （看從源點累積到 v 的距離）

### 4.6 手動 Trace Through 範例

用和 Kruskal 一樣的圖：

```
頂點：{A, B, C, D, E, F}
邊：
  (A, B) : 4,  (A, F) : 2,  (B, C) : 6,  (B, F) : 5
  (C, D) : 3,  (C, F) : 1,  (D, E) : 2,  (E, F) : 4
```

起點 r = A。

**初始**：

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | No |
| B | ∞ | NIL | No |
| C | ∞ | NIL | No |
| D | ∞ | NIL | No |
| E | ∞ | NIL | No |
| F | ∞ | NIL | No |

---

**第 1 步：Extract-Min → A (key=0)**

in_MST[A] = true。檢查 A 的鄰居：
- (A,B): w=4 < key[B]=∞ → key[B]=4, pred[B]=A
- (A,F): w=2 < key[F]=∞ → key[F]=2, pred[F]=A

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | **Yes** |
| B | 4 | A | No |
| C | ∞ | NIL | No |
| D | ∞ | NIL | No |
| E | ∞ | NIL | No |
| F | 2 | A | No |

MST 邊（到目前為止）：（尚無）

---

**第 2 步：Extract-Min → F (key=2)**

in_MST[F] = true。**MST 加入邊 (A,F):2**。

檢查 F 的鄰居：
- (F,A): A 已在 MST，跳過
- (F,B): w=5 > key[B]=4 → 不更新
- (F,C): w=1 < key[C]=∞ → key[C]=1, pred[C]=F
- (F,E): w=4 < key[E]=∞ → key[E]=4, pred[E]=F

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | Yes |
| B | 4 | A | No |
| C | 1 | F | No |
| D | ∞ | NIL | No |
| E | 4 | F | No |
| F | 2 | A | **Yes** |

---

**第 3 步：Extract-Min → C (key=1)**

in_MST[C] = true。**MST 加入邊 (F,C):1**。

檢查 C 的鄰居：
- (C,F): F 已在 MST，跳過
- (C,B): w=6 > key[B]=4 → 不更新
- (C,D): w=3 < key[D]=∞ → key[D]=3, pred[D]=C

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | Yes |
| B | 4 | A | No |
| C | 1 | F | **Yes** |
| D | 3 | C | No |
| E | 4 | F | No |
| F | 2 | A | Yes |

---

**第 4 步：Extract-Min → D (key=3)**

in_MST[D] = true。**MST 加入邊 (C,D):3**。

檢查 D 的鄰居：
- (D,C): C 已在 MST，跳過
- (D,E): w=2 < key[E]=4 → key[E]=2, pred[E]=D  ← 更新了！

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | Yes |
| B | 4 | A | No |
| C | 1 | F | Yes |
| D | 3 | C | **Yes** |
| E | 2 | D | No |
| F | 2 | A | Yes |

---

**第 5 步：Extract-Min → E (key=2)**

in_MST[E] = true。**MST 加入邊 (D,E):2**。

檢查 E 的鄰居：
- (E,D): D 已在 MST，跳過
- (E,F): F 已在 MST，跳過

| 頂點 | key | pred | in_MST |
|------|-----|------|--------|
| A | 0 | NIL | Yes |
| B | 4 | A | No |
| C | 1 | F | Yes |
| D | 3 | C | Yes |
| E | 2 | D | **Yes** |
| F | 2 | A | Yes |

---

**第 6 步：Extract-Min → B (key=4)**

in_MST[B] = true。**MST 加入邊 (A,B):4**。

所有頂點都在 MST 中了。

**MST 的邊**：{(A,F):2, (F,C):1, (C,D):3, (D,E):2, (A,B):4}
**MST 總權重**：2 + 1 + 3 + 2 + 4 = **12**

和 Kruskal 得到的結果一樣！

---

## 五、Kruskal vs Prim 的比較

| 比較項目 | Kruskal | Prim |
|---------|---------|------|
| 策略 | 全域排序，選最輕不形成環的邊 | 從一點出發，逐步擴展 |
| 資料結構 | Union-Find | Priority Queue |
| 時間複雜度 | O(E log V) | O(E log V) [binary heap] |
| 稀疏圖 | 較好（E 小，排序快） | 差不多 |
| 稠密圖 | 較慢（E ≈ V²） | O(V²) [array] 可能更好 |
| 實作難度 | 需要 Union-Find | 和 Dijkstra 幾乎一樣 |
| 圖的表示 | 邊列表即可 | 需要鄰接表 |
| 適合場景 | 邊已排序、稀疏圖 | 稠密圖、需要從特定點開始 |

---

## 六、MST 的性質和常見問題

### 6.1 邊權都不同 → MST 唯一

**定理**：如果圖 G 的所有邊權互不相同，那麼 MST 唯一。

**推導**：

假設有兩棵不同的 MST：T₁ 和 T₂。那麼存在某條邊 e 在 T₁ 中但不在 T₂ 中。

設 e 是 T₁ \ T₂ 中**權重最小**的邊。

1. 把 e 加入 T₂，會形成一個環 C（因為 T₂ 是生成樹，加任何邊都會形成環）。
2. 環 C 上除了 e 之外，所有邊都在 T₂ 中。
3. 環 C 上一定有某條邊 e' 不在 T₁ 中（否則 C 也存在於 T₁ 中，但 T₁ 是樹不可能有環）。
4. 因為 e' ∈ T₂ \ T₁，且 e 是 T₁ \ T₂ 中最輕的：
   - 如果 w(e') < w(e)：那 e' ∈ T₂ \ T₁，考慮 T₁ + {e'} 會形成環 C'，C' 上最重邊如果是 e，那由 Cycle Property 應該 e ∉ T₁，矛盾。更嚴謹地說...

讓我用更直接的方法：

**更簡潔的推導**（用 Cycle Property）：

假設有兩棵不同的 MST：T₁ 和 T₂。

考慮 e = 在 T₁ 和 T₂ 中不同的邊裡，**權重最小**的邊。不妨設 e ∈ T₁, e ∉ T₂。

把 e 加入 T₂ 形成環 C。C 上所有邊（除了 e）都在 T₂ 中。

- C 上一定有某邊 e' ∉ T₁（理由同上）。
- e' 是 T₁ 和 T₂ 的差異邊，且 e 是權重最小的差異邊，所以 w(e) ≤ w(e')。
- 又因為所有邊權不同，w(e) < w(e')（不可能相等）。
- 所以 e' 是環 C 中（嚴格地）比 e 重的邊。但 e 也在 C 中。
- 如果 e' 是 C 中的最重邊，由 Cycle Property，e' ∉ T₂。但 e' ∈ T₂，矛盾！
- 如果 e' 不是 C 中最重邊，那 C 的最重邊 e'' 一定在 T₂ 中（因為 C 的邊除 e 外都在 T₂ 中），由 Cycle Property，e'' ∉ T₂，矛盾！

所以不可能存在兩棵不同的 MST。 ∎

### 6.2 加入新邊後 MST 的更新

**問題**：已知圖 G 的 MST 為 T。現在加入一條新邊 e = (u, v, w)。如何有效率地更新 MST？

**O(V) 演算法**：

1. 把 e 加入 T。T 有 V-1 條邊，加入 e 後有 V 條邊，恰好形成一個環 C。
2. 找到環 C 中的最重邊 e_max（用 BFS/DFS 在 T 上找 u 到 v 的路徑，再和 e 比較）。
3. 如果 e_max = e（新邊是最重的），MST 不變。
4. 否則，移除 e_max，加入 e。新的 T' = T - {e_max} + {e} 就是新的 MST。

**正確性**：由 Cycle Property，環中最重的邊不在 MST 中。

**時間**：在樹上找路徑是 O(V)。

### 6.3 修改邊權後 MST 的更新

**問題**：邊 e = (u,v) 的權重從 w 改成 w'。如何更新 MST？

**情況 1：e 在 MST 中**
- 如果 w' < w（變輕了）：MST 不變（它本來就在 MST 中，變輕只會讓它更有理由在）。
- 如果 w' > w（變重了）：移除 e 後 T 分成兩個連通分量 S₁, S₂。找跨越 (S₁, S₂) 的最輕邊。如果 e（新權重）仍是最輕的，不變；否則換成那條更輕的邊。→ O(V+E)（需要掃描所有邊找最輕跨越邊）

**情況 2：e 不在 MST 中**
- 如果 w' > w（變重了）：MST 不變（它本來就不在 MST 中，變重更不會在）。
- 如果 w' < w（變輕了）：把 e 加入 T 形成環，找環中最重邊。如果 e（新權重）不是最重的，就用 e 替換最重邊。→ O(V)

### 6.4 錯誤的 Divide and Conquer MST 演算法（反例）

有些同學會想：「把頂點分成兩半 V₁ 和 V₂，分別求 MST₁ 和 MST₂，然後用最輕的跨越邊連起來。」

**這是錯的！**

**反例**：

```
      1       10       1
  A ----- B ------ C ----- D
  |                        |
  +----------2-------------+
```

邊：(A,B):1, (B,C):10, (C,D):1, (A,D):2

正確 MST：{(A,B):1, (A,D):2, (C,D):1}，總權重 4。

現在做 D&C，分成 V₁={A,B} 和 V₂={C,D}：
- MST₁ = {(A,B):1}
- MST₂ = {(C,D):1}
- 跨越邊：(B,C):10 和 (A,D):2。最輕的是 (A,D):2。
- 結果：{(A,B):1, (C,D):1, (A,D):2}，總權重 4。

這個例子碰巧對了。但看另一個劃分 V₁={A,C}, V₂={B,D}：
- V₁ 的誘導子圖沒有邊（A 和 C 之間沒有直接邊）→ MST₁ 只有 A 和 C 各自孤立
- 這個劃分行不通——V₁ 不連通。

更根本的問題：**D&C 忽略了可能兩邊各自的 MST 中有邊需要被跨越邊替換的情況**。

真正的反例（更明確）：

```
V₁ = {A, B}, V₂ = {C, D}

邊：(A,B):5, (C,D):5, (A,C):1, (B,D):1, (A,D):10, (B,C):10
```

- MST₁ = {(A,B):5}
- MST₂ = {(C,D):5}
- 最輕跨越邊 = (A,C):1
- D&C 結果：{(A,B):5, (C,D):5, (A,C):1}，總權重 = 11

正確 MST：{(A,C):1, (B,D):1, (A,B):5} 或 {(A,C):1, (B,D):1, (C,D):5}，總權重 = 7。

**D&C 結果 11 > 正確答案 7**，D&C 是錯的！

問題在於：D&C 強制保留了 MST₁ 中的邊 (A,B):5 和 MST₂ 中的邊 (C,D):5，但實際上跨越的邊 (A,C):1 和 (B,D):1 應該讓我們重新考慮內部的邊。

---

## 七、額外 Trace Through 範例

### 範例 2：Kruskal 和 Prim 在另一個圖上

```
頂點：{1, 2, 3, 4, 5}
邊：
  (1,2):2, (1,3):3, (1,4):6
  (2,3):5, (2,5):3
  (3,4):2, (3,5):4
  (4,5):6
```

#### Kruskal Trace

排序：(1,2):2, (3,4):2, (1,3):3, (2,5):3, (3,5):4, (2,3):5, (1,4):6, (4,5):6

| # | 邊 | 權重 | FIND 結果 | 動作 | 集合 |
|---|-----|------|----------|------|------|
| 1 | (1,2) | 2 | 1≠2 | 加入 | {1,2},{3},{4},{5} |
| 2 | (3,4) | 2 | 3≠4 | 加入 | {1,2},{3,4},{5} |
| 3 | (1,3) | 3 | 1≠3 | 加入 | {1,2,3,4},{5} |
| 4 | (2,5) | 3 | 2≠5 | 加入 | {1,2,3,4,5} → 完成！ |

MST = {(1,2):2, (3,4):2, (1,3):3, (2,5):3}，總權重 = 10。

注意第 3 步：加入 (1,3) 連接了 {1,2} 和 {3,4}，形成大集合 {1,2,3,4}。
第 5 步不用考慮了，因為已經有 V-1 = 4 條邊。

#### Prim Trace（起點 = 1）

| 步驟 | Extract | MST 邊 | key 更新 |
|------|---------|--------|---------|
| 初始 | - | - | key[1]=0, 其餘 ∞ |
| 1 | 1 (key=0) | - | key[2]=2(pred=1), key[3]=3(pred=1), key[4]=6(pred=1) |
| 2 | 2 (key=2) | (1,2):2 | key[5]=3(pred=2), key[3]=min(3,5)=3 不變 |
| 3 | 3 (key=3) | (1,3):3 | key[4]=min(6,2)=2(pred=3)更新！, key[5]=min(3,4)=3 不變 |
| 4 | 4 (key=2) | (3,4):2 | key[5]=min(3,6)=3 不變 |
| 5 | 5 (key=3) | (2,5):3 | 鄰居都在 MST 中 |

MST = {(1,2):2, (1,3):3, (3,4):2, (2,5):3}，總權重 = 10。

和 Kruskal 完全一樣！

---

## 八、常見陷阱

1. **忘記 MST 要求圖連通**：如果圖不連通，不存在生成樹。此時可以找 Minimum Spanning Forest（每個連通分量各做一棵 MST）。

2. **邊權可以為負嗎？** 可以！MST 演算法對負權邊完全沒問題。（和最短路不同，MST 不怕負權。）

3. **MST 不等於最短路樹**：MST 最小化的是邊權總和；Dijkstra 的 shortest path tree 最小化的是每個點到源點的距離。兩者通常不同。

4. **Kruskal 忘記在 UNION 之前做 FIND**：必須先 FIND 再比較，不能直接比較頂點值。

5. **Prim 中更新 key 時用了 Dijkstra 的方式**：key[v] 應該是 w(u,v)，不是 key[u] + w(u,v)！

6. **以為 MST 一定唯一**：只有在邊權全部互不相同時才唯一。有相同邊權時可能有多棵 MST。

7. **D&C 做 MST 是錯的**：如上面 6.4 的反例所示。

---

*MST 是圖論中的經典問題，Cut Property 和 Cycle Property 是理解一切的基礎。確保這兩個定理的推導你能自己從頭寫出來。*
