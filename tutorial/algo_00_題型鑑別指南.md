# 演算法 題型鑑別指南

> **核心目的**：看到題目，立刻判斷用什麼演算法、什麼技巧、什麼證明方法。

---

# 第一部分：最佳化問題 — DP vs Greedy vs D&C

## 決策流程圖

```
你要解一個最佳化問題
    │
    ├── 問題有最優子結構？ ──No──→ 暴力搜索 / 其他
    │        │
    │       Yes
    │        │
    ├── 貪心選擇性質成立？ ──Yes──→ Greedy ✓
    │        │                      （通常 O(n log n)）
    │       No / 不確定
    │        │
    ├── 子問題有重疊？ ──Yes──→ DP ✓
    │        │                  （通常 O(n²) 或 O(nW)）
    │       No
    │        │
    └── 子問題獨立？ ──Yes──→ Divide & Conquer ✓
                              （通常 O(n log n)）
```

## DP vs Greedy 核心差異

| | DP | Greedy |
|---|---|---|
| **決策方式** | 考慮所有子問題後做最佳選擇 | 每步做局部最佳選擇，不回頭 |
| **保證最優？** | ✓ 總是最優 | 需要證明（Exchange Argument） |
| **時間** | 通常較慢（填表） | 通常較快（一次掃描） |
| **適用線索** | 「最小/最大 cost」＋子問題重疊 | 「最小/最大數量」＋局部最優=全局最優 |
| **典型** | Knapsack, LCS, Shortest Path | Activity Selection, Huffman, MST |

### 判斷 Greedy 能用的信號

1. 問題有**matroid 結構**（交換性）
2. 可以排序後一次掃過
3. 每步的局部最優不會影響未來的選擇
4. Exchange argument 可以證明

### 判斷必須用 DP 的信號

1. 子問題**互相依賴**（一個子問題的選擇影響另一個的可行解）
2. 有**背包約束**（容量/預算限制）
3. 有**序列/字串比對**性質
4. Greedy 的反例很容易找到

---

## 經典問題分類速查

### Greedy 問題
| 問題 | 關鍵特徵 | Greedy 策略 |
|------|----------|------------|
| Activity Selection | 區間不重疊 | 選最早結束的 |
| Huffman Coding | 前綴碼最短平均長 | 合併最小頻率 |
| Fractional Knapsack | 可以切割 | CP值最高的先拿 |
| 找零錢 (特殊面額) | 標準幣值系統 | 最大面額先 |
| Kruskal/Prim (MST) | 最小生成樹 | 最輕安全邊 |
| Dijkstra | 非負權最短路 | 最近未訪問節點 |

### DP 問題
| 問題 | 子問題定義 | 複雜度 |
|------|-----------|--------|
| 0/1 Knapsack | dp[i][w] = 前i物品、容量w | O(nW) |
| LCS | dp[i][j] = X[1..i] vs Y[1..j] | O(mn) |
| LIS | dp[i] = 以A[i]結尾的LIS | O(n²) or O(n log n) |
| Edit Distance | dp[i][j] = X[1..i]→Y[1..j] | O(mn) |
| Matrix Chain | dp[i][j] = 乘A_i到A_j | O(n³) |
| Optimal BST | dp[i][j] = key i到j的最小搜尋代價 | O(n³) or O(n²) |
| 回文插入 | dp[i][j] = S[i..j]變回文 | O(n²) |
| Shortest Path (BF) | dp[v][k] = 用≤k邊到v | O(VE) |
| Floyd-Warshall | dp[i][j][k] = 經由1..k | O(V³) |

### Divide & Conquer 問題
| 問題 | 分割 | 合併 | 複雜度 |
|------|------|------|--------|
| Merge Sort | 分兩半 | merge O(n) | O(n log n) |
| Counting Inversions | 分兩半 | merge+count O(n) | O(n log n) |
| Closest Pair | 分兩半 | strip O(n) | O(n log n) |
| Median of 2 arrays | 丟一半 | 比較中位數 | O(log n) |
| Karatsuba 乘法 | 分數字 | 3次子乘法 | O(n^1.585) |

---

# 第二部分：圖論問題決策樹

```
圖論問題
  │
  ├── 遍歷/搜尋？
  │     ├── 最短路徑？ → 第三部分
  │     ├── 連通性？ → BFS/DFS
  │     ├── 環偵測？ → DFS (back edge)
  │     ├── 拓撲排序？ → DFS finish time / Kahn's
  │     └── SCC？ → Kosaraju / Tarjan
  │
  ├── 最佳化？
  │     ├── MST？ → Kruskal / Prim
  │     ├── Max Flow？ → Ford-Fulkerson / Edmonds-Karp
  │     └── Matching？ → 轉 Max Flow / Hungarian
  │
  └── NP 問題？ → 第四部分
```

### BFS vs DFS — 什麼時候用哪個？

| 需求 | BFS | DFS |
|------|-----|-----|
| 最短路（無權） | ✓ 保證最短 | ✗ |
| 連通分量 | ✓ | ✓ |
| 環偵測 | ✓（但較複雜） | ✓（看 back edge，更簡單） |
| 拓撲排序 | ✓（Kahn's） | ✓（finish time 遞減） |
| SCC | ✗ | ✓（Kosaraju / Tarjan） |
| 二部圖判斷 | ✓（交替上色） | ✓ |
| 最短路/層次 | ✓ | ✗ |
| 回溯搜尋 | ✗ | ✓ |

---

# 第三部分：最短路徑選擇

```
最短路徑問題
  │
  ├── Single source or All pairs?
  │     │
  │     ├── Single Source:
  │     │     ├── 無權圖？ → BFS O(V+E)
  │     │     ├── 非負權？ → Dijkstra O(E + V log V)
  │     │     ├── 有負權？ → Bellman-Ford O(VE)
  │     │     └── DAG？ → 拓撲排序 + relax O(V+E)
  │     │
  │     └── All Pairs:
  │           ├── 一般圖？ → Floyd-Warshall O(V³)
  │           └── 非負權？ → V 次 Dijkstra O(VE + V²log V)
  │
  └── 特殊問題？
        ├── 負環偵測？ → Bellman-Ford 第V輪檢查
        ├── 最大容量路？ → 修改 Floyd-Warshall (max + min)
        └── 最長路 (DAG)？ → 拓撲排序 + relax (取max)
```

### 各算法比較

| 演算法 | 時間 | 負權 | 負環 | 適用 |
|--------|------|------|------|------|
| BFS | O(V+E) | ✗ | ✗ | 無權圖 |
| Dijkstra | O(E+V log V) | ✗ | ✗ | 非負權單源 |
| Bellman-Ford | O(VE) | ✓ | 可偵測 | 有負權單源 |
| DAG relax | O(V+E) | ✓ | N/A(DAG) | DAG |
| Floyd-Warshall | O(V³) | ✓ | 可偵測 | 全對最短路 |
| Johnson's | O(VE+V²log V) | ✓(reweight) | — | 稀疏圖全對 |

### 為什麼 Dijkstra 不能處理負權？

Dijkstra 假設：一旦節點 u 被 extract-min，dist[u] 就是最終答案。

但有負權邊時，可能存在一條繞遠路但經過負邊的更短路徑，在 u 被取出後才被發現。

**經典反例**：s→a=1, s→b=5, b→a=-10。Dijkstra 先確定 dist[a]=1，但實際 dist[a]=5+(-10)=-5。

---

# 第四部分：NP-Complete 問題判斷

## 什麼時候該「設計演算法」vs「證明 NP-complete」？

```
問題
  │
  ├── 有特殊結構？
  │     ├── DAG？ → 可能有多項式解（拓撲排序）
  │     ├── 二部圖？ → 可能有多項式解（matching）
  │     ├── 樹？ → 通常有 O(n) 或 O(n²) 解
  │     └── 固定參數？ → 可能有 pseudo-polynomial 解
  │
  ├── 像不像已知 NPC 問題？
  │     ├── 像 SAT？ → 可能 NPC
  │     ├── 像 Knapsack？ → 可能 NPC（但有 pseudo-poly DP）
  │     ├── 像 Ham Cycle？ → 可能 NPC
  │     └── 像 Independent Set？ → 可能 NPC
  │
  └── 判斷困難度
        ├── 能否在 poly time 驗證？ → 是 → ∈ NP
        └── 能否從已知 NPC 歸約？ → 是 → NP-hard
```

## NPC 歸約的標準流程

1. **證明 L ∈ NP**：描述 certificate + poly-time verifier
2. **選擇已知 NPC 問題 L'**（從歸約鏈中選最近的）
3. **構造歸約 f**：x ∈ L' ⟺ f(x) ∈ L
4. **證明正確性**（⟹ 和 ⟸ 兩方向）
5. **證明歸約是多項式時間**

### 常用歸約鏈

```
Circuit-SAT → SAT → 3-SAT → {CLIQUE, Vertex Cover, Independent Set,
                               Subset Sum, Ham Cycle, 3-Coloring}

3-SAT → Independent Set → Vertex Cover → Clique
3-SAT → Subset Sum → Partition → Knapsack
3-SAT → Ham Cycle → Ham Path → TSP
Ham Path → DCST (K=2)
Ham Cycle → Subgraph Isomorphism
```

### P 裡的「偽裝成 NPC」問題

| 看起來難... | 但其實 ∈ P 的原因 |
|------------|-------------------|
| 2-SAT | Implication graph + SCC |
| DAG Ham Path | 拓撲排序唯一性檢查 |
| MST | Greedy (Kruskal/Prim) |
| Bipartite Matching | Max Flow |
| Shortest Path | Dijkstra/BF |
| Euler Circuit | 每個點偶數度 → 存在 |

---

# 第五部分：遞迴式求解方法選擇

```
T(n) = aT(n/b) + f(n)
  │
  ├── 符合 Master Theorem？
  │     ├── f(n) vs n^{log_b a} 比較
  │     │     ├── f(n) 多項式小 → Case 1: T = Θ(n^{log_b a})
  │     │     ├── f(n) 相等 → Case 2: T = Θ(n^{log_b a} log n)
  │     │     └── f(n) 多項式大 + 正規性 → Case 3: T = Θ(f(n))
  │     └── f(n) = Θ(n^{log_b a} log^k n)? → Extended: T = Θ(n^{log_b a} log^{k+1} n)
  │
  ├── 不符合 Master Theorem？
  │     ├── 遞迴樹法 → 畫出展開，算每層總和
  │     └── 代入法 → 猜測 + 數學歸納法
  │
  └── 特殊形式？
        ├── T(n) = T(√n) + ... → 令 m = log n 變換
        ├── T(n) = √n T(√n) + n → 展開 + 變數替換
        └── T(n) = T(n/2) + T(n/4) + ... → 遞迴樹（不等分）
```

### Master Theorem 快速判斷

**記法**：先算 $n^{log_b a}$，然後和 f(n) 比較。

| a | b | n^{log_b a} | f(n) | Case | T(n) |
|---|---|-------------|------|------|------|
| 4 | 2 | n² | n | 1 | Θ(n²) |
| 2 | 2 | n | n | 2 | Θ(n log n) |
| 2 | 2 | n | n² | 3 | Θ(n²) |
| 4 | 2 | n² | n² | 2 | Θ(n² log n) |
| 4 | 2 | n² | n²log n | Ext.2 | Θ(n² log²n) |
| 7 | 2 | n^2.81 | n² | 1 | Θ(n^2.81) |

### 代入法的技巧

1. 先用遞迴樹猜答案
2. 猜 T(n) ≤ cn^k（或 cn^k - dn 等，可能要減低階項）
3. 代入遞迴式，用歸納法證明
4. **常見陷阱**：猜 T(n) ≤ cn 不行時，試 T(n) ≤ cn - d

---

# 第六部分：證明方法選擇

## 演算法正確性證明

| 方法 | 適用 | 做法 |
|------|------|------|
| **Exchange Argument** | Greedy | 假設最優解 S*≠S，找第一個不同處交換，證不變差 |
| **Greedy stays ahead** | Greedy | 歸納證明 Greedy 每步都 ≥ 任何其他策略 |
| **Loop Invariant** | 迭代演算法 | 定義 invariant，證三步：Init/Maint/Term |
| **Cut-and-paste** | DP optimal substructure | 反證：若子問題不最優 → 可替換得更優 → 矛盾 |
| **數學歸納** | 遞迴演算法 | 基底 + 歸納步驟 |

## 下界證明

| 方法 | 適用 |
|------|------|
| Information-theoretic (決策樹) | Comparison-based sorting Ω(n log n) |
| Adversary argument | 搜尋/選擇問題 |
| Reduction | 從已知下界問題歸約 |

---

# 第七部分：攤銷分析三方法

```
需要攤銷分析
  │
  ├── Aggregate（聚合）法：直接算 n 次操作總成本 / n
  │     → 適合：明確知道「昂貴操作」發生頻率
  │     → 例子：Binary counter increment
  │
  ├── Accounting（記帳）法：每次操作多收一點「信用」
  │     → 適合：可以直觀分配成本
  │     → 例子：Stack with multipop
  │
  └── Potential（勢能）法：定義 Φ(Dᵢ)，â = c + ΔΦ
        → 適合：需要嚴格證明
        → 例子：Dynamic table, Splay tree, α-balanced BST
```

### Potential Method 核心

$$\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$$

- **要求**：Φ(Dₙ) ≥ Φ(D₀)（保證攤銷總成本 ≥ 實際總成本）
- 常見 Φ 選法：
  - Dynamic table: Φ = |2·num - size| 或 2num - size (α≥1/2) 和 size/2 - num (α<1/2)
  - Binary counter: Φ = 1 的個數
  - Splay tree: Φ = Σ log(size(x))

---

# 第八部分：複雜度速查

## 常見時間複雜度排序（由快到慢）

$$O(1) < O(\log\log n) < O(\log n) < O(\sqrt{n}) < O(n) < O(n\log n) < O(n^2) < O(n^3) < O(2^n) < O(n!) < O(n^n)$$

## 實用判斷

| 複雜度 | n=10⁶ 時大約 | 適合的題目規模 |
|--------|-------------|--------------|
| O(n) | 10⁶ | n ≤ 10⁸ |
| O(n log n) | 2×10⁷ | n ≤ 10⁷ |
| O(n²) | 10¹² | n ≤ 10⁴ |
| O(n³) | 10¹⁸ | n ≤ 500 |
| O(2ⁿ) | 巨大 | n ≤ 25 |

## 考試中的時間複雜度提示

- 題目要求 O(n) → 想 Greedy / Linear scan / Bucket
- 題目要求 O(n log n) → 想 Sort + Sweep / D&C / Priority Queue
- 題目要求 O(n²) → 想 DP (2D table)
- 題目要求 O(n³) → 想 DP (interval / Floyd-Warshall / Matrix Chain)
- 題目要求 polynomial in nk → 想 DP with extra dimension
- 題目要求 O(V+E) → 想 BFS / DFS / Topological Sort
- 題目要求 O(E log V) → 想 Dijkstra / Kruskal / Prim
