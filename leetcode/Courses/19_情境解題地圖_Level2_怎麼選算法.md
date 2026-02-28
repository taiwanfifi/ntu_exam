# 情境解題地圖 Level 2：算法家族內部 — 怎麼選具體算法？

> **定位**：Level 1 告訴你「這是 Graph 問題，用最短路徑」。Level 2 告訴你「用 Dijkstra 還是 Bellman-Ford」。
> **適用對象**：已能辨識算法家族，但在變體選擇上仍不確定的面試準備者
> **核心原則**：不解釋算法內部原理，只講 **選擇決策 (Decision-Making)**
> **語言**：繁體中文 + English 技術術語
> **思維模式**：像 Senior Google Interviewer 一樣評估你的算法選擇能力

---

## 目錄

| Part | 內容 | 頁內連結 |
|------|------|---------|
| A | 十大算法家族內部選擇矩陣（100+ 決策規則） | [Part A](#part-a-每個算法家族內部的選擇矩陣) |
| B | 資料結構選擇矩陣 | [Part B](#part-b-資料結構選擇矩陣) |
| C | 複雜度需求逆推算法 | [Part C](#part-c-複雜度需求--算法逆推) |
| D | 常見陷阱 — 看起來像 A 但其實是 B | [Part D](#part-d-常見陷阱--看起來像-a-但其實是-b) |

---

# Part A: 每個算法家族內部的選擇矩陣

---

## 家族 1：Two Pointers — 選哪種指針模式？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 原因 | 代表題 |
|---|---|---|---|---|
| 1 | 已排序 + 找兩數配對 | 對向雙指針 (Opposite) | 從兩端夾擊，每次可排除一端 | LC 167 Two Sum II |
| 2 | 已排序 + 找三數配對 | 固定一個 + 對向雙指針 | 外層 for 固定 i，內層雙指針 | LC 15 3Sum |
| 3 | 已排序 + 原地去重 | 同向雙指針 (Same Direction) | slow=寫入位，fast=讀取位 | LC 26 Remove Duplicates |
| 4 | 已排序 + 原地移除特定值 | 同向雙指針 | 同上邏輯 | LC 27 Remove Element |
| 5 | 鏈表找中點 | 快慢指針 (Fast-Slow) | fast 走兩步，slow 走一步 | LC 876 Middle of Linked List |
| 6 | 鏈表偵測環 | 快慢指針 | fast 終會追上 slow | LC 141 Linked List Cycle |
| 7 | 鏈表找環入口 | 快慢指針 + 數學推導 | 相遇後重置一個指針到 head | LC 142 Linked List Cycle II |
| 8 | 判斷 Palindrome | 對向雙指針 | 左右往中間走，逐字比較 | LC 125 Valid Palindrome |
| 9 | 合併兩個已排序陣列 | 同向雙指針 (各自一個) | 比較後選小的 | LC 88 Merge Sorted Array |
| 10 | 未排序 + 找配對 | **不用雙指針！用 HashMap** | 未排序無法用排除邏輯 | LC 1 Two Sum |

### 關鍵決策樹

```
Q: 資料已排序嗎？
├── YES → Q: 要找配對（pair/triplet）嗎？
│         ├── YES → 對向雙指針（從兩端夾擊）
│         └── NO → Q: 要原地修改陣列嗎？
│                   ├── YES → 同向雙指針（slow寫/fast讀）
│                   └── NO → 可能不需要 Two Pointers
└── NO → Q: 是鏈表問題嗎？
          ├── YES → 快慢指針
          └── NO → **別用 Two Pointers，改用 HashMap / Sliding Window**
```

### 易混淆對照

| 題目 | 錯誤選擇 | 正確選擇 | 為什麼 |
|------|---------|---------|--------|
| LC 1 Two Sum (unsorted) | Two Pointers | HashMap | 未排序，雙指針無法排除 |
| LC 167 Two Sum II (sorted) | HashMap | Two Pointers | 已排序，O(1) space 更優 |
| LC 11 Container With Most Water | Sliding Window | 對向雙指針 | 不是連續子陣列，是選兩端 |
| LC 42 Trapping Rain Water | 純雙指針 | 雙指針 OR 單調棧 | 雙指針可解但需理解 leftMax/rightMax |

---

## 家族 2：Sliding Window — 選哪種窗口模式？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 窗口行為 | 代表題 |
|---|---|---|---|---|
| 11 | 固定大小 k 的子陣列最值 | 固定窗口 (Fixed) | 窗口大小始終 = k | LC 643 Max Average Subarray |
| 12 | 求**最短**的滿足條件的子陣列 | 可變窗口 (Shrink when valid) | 滿足條件時嘗試縮小 | LC 209 Min Size Subarray Sum |
| 13 | 求**最長**的滿足條件的子陣列 | 可變窗口 (Shrink when invalid) | 違反條件時縮小 | LC 3 Longest Substring Without Repeating |
| 14 | 需要匹配字元集合 | 計數窗口 + HashMap | need/have 追蹤匹配狀態 | LC 76 Minimum Window Substring |
| 15 | 子陣列中不同元素數 ≤ k | 可變窗口 + HashMap | HashMap 追蹤各元素頻率 | LC 340 Longest Substring with At Most K Distinct |
| 16 | 有負數的子陣列和 | **不用 Sliding Window！** | 負數破壞窗口單調性 | LC 560 Subarray Sum Equals K |
| 17 | 子陣列乘積 | 可變窗口（全正數時） | 類似和的窗口 | LC 713 Subarray Product Less Than K |
| 18 | 固定窗口 + 要窗口內最大值 | 固定窗口 + Monotonic Deque | Deque 維護單調遞減序列 | LC 239 Sliding Window Maximum |

### 關鍵決策樹

```
Q: 子陣列/子字串中有負數嗎？
├── YES → ❌ 不能用 Sliding Window → 用 Prefix Sum + HashMap
└── NO → Q: 窗口大小已知嗎？
          ├── YES → 固定窗口：右進左出，維護窗口狀態
          └── NO → Q: 求最短還是最長？
                    ├── 最短 → 滿足時 shrink（while valid, shrink）
                    └── 最長 → 違反時 shrink（while invalid, shrink）
```

### 「最短」vs「最長」模板差異（這是面試高頻考點）

```
# 求最短：滿足條件後不斷 shrink，在 shrink 過程中更新答案
while right < n:
    window.add(arr[right])
    while window_is_valid():        # ← 滿足時 shrink
        ans = min(ans, right - left + 1)   # ← 在 shrink 時更新
        window.remove(arr[left])
        left += 1
    right += 1

# 求最長：違反條件時 shrink，在 expand 過程中更新答案
while right < n:
    window.add(arr[right])
    while window_is_invalid():      # ← 違反時 shrink
        window.remove(arr[left])
        left += 1
    ans = max(ans, right - left + 1)       # ← 在 expand 後更新
    right += 1
```

### 易混淆對照

| 題目 | 錯誤選擇 | 正確選擇 | 為什麼 |
|------|---------|---------|--------|
| LC 560 Subarray Sum = k (有負數) | Sliding Window | Prefix Sum + HashMap | 負數破壞單調性 |
| LC 209 Min Subarray Sum ≥ target (全正數) | Prefix Sum | Sliding Window | 全正數可用窗口 O(n) |
| LC 239 Sliding Window Maximum | 普通 Sliding Window | Sliding Window + Monotonic Deque | 需要 O(1) 取窗口最大值 |
| LC 438 Find All Anagrams | Two Pointers | Fixed Sliding Window + counting | 窗口大小 = pattern 長度 |

---

## 家族 3：Binary Search — 選哪個模板？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 迴圈條件 | 回傳值 | 代表題 |
|---|---|---|---|---|---|
| 19 | 找精確值是否存在 | Template 1 (Exact Match) | `left <= right` | `mid` or `-1` | LC 704 Binary Search |
| 20 | 找左邊界 (first occurrence) | Template 2 (Left Bound) | `left < right` | `left` | LC 34 Find First and Last Position |
| 21 | 找右邊界 (last occurrence) | Template 2 變體 | `left < right` | `left - 1` | LC 34 (right part) |
| 22 | 不確定用哪個模板 | Template 3 (Safe) | `left + 1 < right` | 後處理 left/right | 任何 binary search 題 |
| 23 | 搜尋空間是答案值域 | Binary Search on Answer | 看情況選 T1/T2 | `left` (通常) | LC 875 Koko Eating Bananas |
| 24 | Rotated Sorted Array | Template 1 + 判斷哪半有序 | `left <= right` | `mid` | LC 33 Search in Rotated Sorted Array |
| 25 | 找 Peak Element | Template 2 | `left < right` | `left` | LC 162 Find Peak Element |
| 26 | 矩陣中搜尋 | 展平成 1D + Template 1 | `left <= right` | `mid` | LC 74 Search a 2D Matrix |

### 三大模板一覽（只看選擇，不看實作）

```
Template 1: left <= right       → 搜尋空間每輪 -1，最後 left > right 退出
  適用：精確查找，找到就回傳
  結束狀態：left = right + 1（搜尋空間為空）

Template 2: left < right        → 搜尋空間每輪至少 -1，最後 left == right
  適用：找邊界（第一個滿足/最後一個滿足）
  結束狀態：left == right（答案就在這）

Template 3: left + 1 < right    → 搜尋空間每輪 -1，最後 left + 1 == right
  適用：不確定的時候用這個最安全
  結束狀態：left 和 right 相鄰，需要手動檢查兩個
```

### Binary Search on Answer — 什麼時候用？

```
當你看到這些特徵，就用 Binary Search on Answer:
1. 題目問「最小的最大值」或「最大的最小值」(minimax)
2. 答案有明確的上下界
3. 可以寫一個 feasible(x) 函數判斷「答案 ≤ x 是否可行」
4. feasible(x) 有單調性：x 增大時，從 False 變成 True（或反過來）

經典例子:
- LC 875 Koko Eating Bananas: 最小速度 → feasible = 能在 h 小時內吃完嗎？
- LC 1011 Capacity To Ship: 最小載重 → feasible = 能在 days 天內運完嗎？
- LC 410 Split Array Largest Sum: 最小的最大子陣列和
```

### 易混淆對照

| 題目 | 錯誤選擇 | 正確選擇 | 為什麼 |
|------|---------|---------|--------|
| LC 34 Find First Position | Template 1 | Template 2 (Left Bound) | 找邊界不是找精確值 |
| LC 162 Find Peak Element | Template 1 | Template 2 | 沒有精確 target，找轉折點 |
| LC 875 Koko Eating Bananas | 線性搜尋 | Binary Search on Answer | 答案空間有序且可判斷 |
| LC 4 Median of Two Sorted Arrays | Merge | Binary Search on partition | O(n) 不夠好，需要 O(log n) |

---

## 家族 4：Tree DFS — Preorder vs Inorder vs Postorder？

### 選擇矩陣

| # | 你遇到的情況 | 遍歷方式 | 原因 | 代表題 |
|---|---|---|---|---|
| 27 | 從上往下傳遞資訊（如路徑和） | Preorder | 先處理自己，把資訊傳給子節點 | LC 112 Path Sum |
| 28 | 從下往上收集結果（如高度、直徑） | Postorder | 先取得子樹結果，再彙總 | LC 104 Maximum Depth |
| 29 | BST 排序相關操作 | Inorder | BST 中序遍歷 = 排序序列 | LC 230 Kth Smallest in BST |
| 30 | 求深度 (depth) | Preorder（帶 depth 參數） | 深度是從根往下算的 | LC 111 Minimum Depth |
| 31 | 求高度 (height) | Postorder | 高度是從葉往上算的 | LC 110 Balanced Binary Tree |
| 32 | 求直徑 (diameter) | Postorder | 需要左右子樹高度相加 | LC 543 Diameter of Binary Tree |
| 33 | 路徑和（根到葉） | Preorder（傳遞 remaining target） | 沿途扣減 target | LC 112 Path Sum |
| 34 | 路徑和（任意起點） | Preorder + Prefix Sum | 用 HashMap 記錄路徑前綴和 | LC 437 Path Sum III |
| 35 | 修改樹結構（翻轉、刪除） | Postorder 較安全 / Preorder 也行 | Postorder 先處理子再改自己 | LC 226 Invert Binary Tree |
| 36 | 序列化 / 反序列化 | Preorder 或 Level Order | Preorder 最容易重建 | LC 297 Serialize and Deserialize |
| 37 | 驗證 BST | Inorder（檢查是否遞增） | BST 中序 = sorted | LC 98 Validate BST |
| 38 | LCA (Lowest Common Ancestor) | Postorder | 從下往上找到兩個節點的交匯點 | LC 236 LCA of Binary Tree |

### 關鍵決策樹

```
Q: 資訊的流向是什麼？
├── 從上往下（parent → child）→ Preorder
│   - 典型參數：depth, path_sum, remaining_target
├── 從下往上（child → parent）→ Postorder
│   - 典型回傳值：height, size, is_valid, subtree_sum
└── 需要排序序列（BST 限定）→ Inorder
    - BST inorder = sorted array
```

### Recursive vs Iterative DFS 怎麼選？

| 情境 | 選擇 | 原因 |
|------|------|------|
| 面試（一般情況） | Recursive | 程式碼短，容易寫對 |
| 面試官要求 iterative | Iterative + Stack | 需要準備的標準變體 |
| 可能 stack overflow（樹極深） | Iterative + Stack | 避免 recursion depth 限制 |
| Morris Traversal | 只在面試官追問 O(1) space 時 | 改變樹結構，需要還原 |

---

## 家族 5：Graph Traversal — DFS vs BFS？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 原因 | 代表題 |
|---|---|---|---|---|
| 39 | 最短路徑（無權圖） | BFS | BFS 天然按層展開 = 最短 | LC 127 Word Ladder |
| 40 | 最短路徑（加權圖） | **不用 BFS！** → 見家族 6 | BFS 不保證加權最短路 | — |
| 41 | 列出所有路徑 | DFS + 回溯 | DFS 自然探索所有分支 | LC 797 All Paths From Source to Target |
| 42 | 連通分量計數 | DFS 或 BFS 皆可 | 都能遍歷整個連通分量 | LC 200 Number of Islands |
| 43 | 拓撲排序 | BFS (Kahn's) 或 DFS | BFS 更直觀；DFS 需要逆序 | LC 207 Course Schedule |
| 44 | 環偵測（有向圖） | DFS + 三色標記 | 灰色 = 正在處理中 = 遇到就是環 | LC 207 Course Schedule |
| 45 | 環偵測（無向圖） | DFS (檢查 parent) 或 Union-Find | Union-Find 更簡潔 | LC 684 Redundant Connection |
| 46 | 二分圖判斷 (Bipartite) | BFS 或 DFS + 染色 | 相鄰節點必須不同色 | LC 785 Is Graph Bipartite |
| 47 | 矩陣上的搜尋（Island 類） | DFS（程式碼短）或 BFS | DFS 遞迴更簡潔 | LC 200 Number of Islands |
| 48 | 多起點最短路徑 | 多源 BFS (Multi-source BFS) | 所有起點同時入 Queue | LC 994 Rotting Oranges |

### 關鍵決策樹

```
Q: 要找最短路徑嗎？
├── YES → Q: 有權重嗎？
│         ├── NO → BFS（保證最短）
│         └── YES → 見家族 6（Dijkstra / Bellman-Ford）
└── NO → Q: 要列出所有路徑/組合嗎？
          ├── YES → DFS + 回溯
          └── NO → Q: 只要判斷連通性/遍歷？
                    ├── YES → DFS 或 BFS 皆可（DFS 程式碼通常更短）
                    └── 其他 → 看具體問題
```

### BFS 的四種變體（面試必備）

| 變體 | 說明 | 代表題 |
|------|------|--------|
| 標準 BFS | 一層一層展開 | LC 102 Level Order Traversal |
| 多源 BFS | 多個起點同時入 Queue | LC 994 Rotting Oranges |
| 0-1 BFS | 邊權只有 0 和 1，用 Deque | LC 1368 Min Cost to Make Valid Path |
| 雙向 BFS | 從起點和終點同時搜尋 | LC 127 Word Ladder (最佳化) |

---

## 家族 6：Shortest Path — BFS vs Dijkstra vs Bellman-Ford vs Floyd-Warshall？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 時間複雜度 | 代表題 |
|---|---|---|---|---|
| 49 | 無權圖最短路 | BFS | O(V+E) | LC 127 Word Ladder |
| 50 | 正權圖 + 單源最短路 | Dijkstra (min-heap) | O((V+E) log V) | LC 743 Network Delay Time |
| 51 | 有負權邊 + 單源最短路 | Bellman-Ford | O(VE) | LC 787 Cheapest Flights (modified) |
| 52 | 限制最多 K 步 | Modified Bellman-Ford (K rounds) | O(KE) | LC 787 Cheapest Flights Within K Stops |
| 53 | 所有點對最短路 | Floyd-Warshall | O(V^3) | LC 1334 Find the City |
| 54 | 邊權只有 0 和 1 | 0-1 BFS (Deque) | O(V+E) | LC 1368 Min Cost Path |
| 55 | DAG (有向無環圖) | Topological Sort + Relaxation | O(V+E) | — |
| 56 | 偵測負環 | Bellman-Ford (第 V 輪還能更新) | O(VE) | — |

### 關鍵決策樹

```
Q: 邊有權重嗎？
├── NO → BFS（最快最簡單）
└── YES → Q: 有負權邊嗎？
          ├── NO → Q: 單源還是多源？
          │         ├── 單源 → Dijkstra
          │         └── 所有點對 → Floyd-Warshall（V 小的時候）或 多次 Dijkstra
          └── YES → Q: 有負環嗎？
                    ├── 可能 → Bellman-Ford（可偵測負環）
                    └── 沒有 → Bellman-Ford 或 SPFA
```

### 致命錯誤

```
❌ 加權圖用 BFS → BFS 只保證「步數最少」，不保證「權重和最小」
❌ 有負權用 Dijkstra → Dijkstra 的 greedy 假設在負權下失效
❌ V 很大時用 Floyd-Warshall → O(V^3) 只適合 V ≤ 400 左右
```

---

## 家族 7：Dynamic Programming — 哪種 DP 模式？

### 選擇矩陣

| # | 你遇到的情況 | DP 模式 | 狀態定義 | 代表題 |
|---|---|---|---|---|
| 57 | 一維序列的最優解 | 1D 線性 DP | dp[i] = 到第 i 個的最優解 | LC 70 Climbing Stairs |
| 58 | 一維 + 選/不選 | 1D 決策 DP | dp[i] = 考慮前 i 個的最優解 | LC 198 House Robber |
| 59 | 兩個字串比較 | 2D 字串 DP | dp[i][j] = s1[0..i] 和 s2[0..j] 的結果 | LC 1143 LCS |
| 60 | 格子路徑 | 2D 網格 DP | dp[i][j] = 到 (i,j) 的結果 | LC 62 Unique Paths |
| 61 | 選/不選 + 容量限制 | 0/1 Knapsack | dp[i][w] = 前 i 物 + 容量 w 的最大值 | LC 416 Partition Equal Subset Sum |
| 62 | 可重複選 + 容量限制 | 完全背包 (Unbounded Knapsack) | dp[w] = 容量 w 的最優解 | LC 322 Coin Change |
| 63 | 區間最值 | 區間 DP (Interval DP) | dp[i][j] = 區間 [i..j] 的最優解 | LC 516 Longest Palindromic Subseq |
| 64 | 樹上的 DP | Tree DP (DFS + DP) | dp[node] = 以 node 為根的子樹結果 | LC 337 House Robber III |
| 65 | 帶狀態壓縮 | Bitmask DP | dp[mask] = 某子集的最優解 | LC 1986 Min Sessions |
| 66 | 計數問題（多少種方式） | 計數 DP | dp[i] = 到 i 的方案數 | LC 70 Climbing Stairs |
| 67 | 最長遞增子序列 | LIS 專用 DP | dp[i] = 以 i 結尾的最長長度 (or patience sort) | LC 300 LIS |

### 關鍵決策樹

```
Q: 有幾個維度的輸入？
├── 一個序列 → Q: 有容量/資源限制嗎？
│               ├── NO → 1D DP (dp[i])
│               └── YES → Q: 每個元素可以重複選嗎？
│                         ├── NO → 0/1 Knapsack
│                         └── YES → 完全背包
├── 兩個序列 → 2D 字串 DP (dp[i][j])
├── 格子/矩陣 → 2D 網格 DP (dp[i][j])
├── 區間操作 → 區間 DP (dp[l][r])
└── 樹結構 → Tree DP (DFS post-order)
```

### Top-Down vs Bottom-Up 怎麼選？

| 情境 | 選擇 | 原因 |
|------|------|------|
| 面試中不確定轉移順序 | Top-Down (Memoization) | 不需要手動確定填表順序 |
| 狀態空間稀疏（很多狀態不會被訪問到） | Top-Down | 只計算需要的狀態 |
| 需要空間優化（滾動陣列） | Bottom-Up | 容易看出哪些狀態可以丟棄 |
| 轉移方程和順序很清楚 | Bottom-Up | 通常常數更小 |
| Tree DP | Top-Down (遞迴天然的) | 樹的 DFS 就是 top-down |

### 背包問題選擇速查

```
Q: 每個物品可以選幾次？
├── 只能選 1 次 → 0/1 Knapsack
│   內層循環：for w in range(W, w_i-1, -1)   ← 倒序！
├── 可以選無限次 → 完全背包
│   內層循環：for w in range(w_i, W+1)        ← 正序！
└── 每個物品最多選 k_i 次 → 多重背包（面試很少考）

Q: 求什麼？
├── 最大價值 → dp[w] = max(dp[w], dp[w-w_i] + v_i)
├── 方案數   → dp[w] = dp[w] + dp[w-w_i]
└── 能否恰好裝滿 → dp[w] = dp[w] or dp[w-w_i]
```

### 易混淆對照

| 題目 | 看起來像 | 實際上是 | 為什麼 |
|------|---------|---------|--------|
| LC 322 Coin Change | 0/1 Knapsack | 完全背包 | 硬幣可以重複選 |
| LC 416 Partition Equal Subset Sum | 完全背包 | 0/1 Knapsack | 每個數只能用一次 |
| LC 518 Coin Change 2 (方案數) | Coin Change | 完全背包計數 | 同 Coin Change 但求方案數不是最少個數 |
| LC 139 Word Break | Backtracking | DP (完全背包變體) | 字典中的字可以重複使用 |

---

## 家族 8：Backtracking — 子集 vs 排列 vs 組合？

### 選擇矩陣

| # | 你遇到的情況 | 模式 | 關鍵差異 | 代表題 |
|---|---|---|---|---|
| 68 | 列出所有子集 | Subsets 模式 | 每個元素選或不選 | LC 78 Subsets |
| 69 | 列出所有排列 | Permutations 模式 | 每個元素都要用，順序不同算不同 | LC 46 Permutations |
| 70 | 列出所有組合 (大小固定) | Combinations 模式 | 選 k 個，順序不重要 | LC 77 Combinations |
| 71 | 組合 + 數字可重複選 | Combination Sum 模式 | 同個元素可以用多次 | LC 39 Combination Sum |
| 72 | 有重複元素 + 結果不能重複 | 排序 + 跳過重複 | `if i > start and nums[i] == nums[i-1]: continue` | LC 40 Combination Sum II |
| 73 | 矩陣搜尋（找路徑） | Grid DFS + 回溯 | 標記 visited，回溯時取消 | LC 79 Word Search |
| 74 | N-Queens 類放置問題 | 約束回溯 | 多維 visited 追蹤行/列/對角線 | LC 51 N-Queens |

### 三大模式的核心差異

```
Subsets:           for i in range(start, n):   → 不回頭（start 遞增）
                     choose(i); recurse(i+1); unchoose(i)
                     # 每次 recurse 都是一個答案
                     時間複雜度: O(2^n)

Permutations:      for i in range(0, n):       → 從頭開始（但跳過已選的）
                     if used[i]: continue
                     choose(i); recurse(); unchoose(i)
                     # 只有長度 = n 時才是答案
                     時間複雜度: O(n!)

Combinations(k):   for i in range(start, n):   → 不回頭 + 剪枝
                     choose(i); recurse(i+1); unchoose(i)
                     # 只有長度 = k 時才是答案
                     時間複雜度: O(C(n,k))
```

### 去重技巧對照

| 情境 | 去重方式 | 說明 |
|------|---------|------|
| 元素本身有重複，結果不能重複 | 排序 + `nums[i] == nums[i-1]` 跳過 | LC 40, LC 90 |
| 排列中有重複元素 | 排序 + `nums[i] == nums[i-1] and not used[i-1]` | LC 47 |
| 組合中同一元素可重複選 | `recurse(i)` 而非 `recurse(i+1)` | LC 39 |

---

## 家族 9：Greedy vs DP — 怎麼判斷用哪個？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 判斷方式 | 代表題 |
|---|---|---|---|---|
| 75 | 局部最優 → 全域最優（可證明） | Greedy | 找不到反例 | LC 55 Jump Game |
| 76 | 最優解需要比較多個子問題 | DP | 貪心會漏掉更優解 | LC 322 Coin Change |
| 77 | 區間排程 / 選活動 | Greedy（按結束時間排序） | 經典可證明的 greedy | LC 435 Non-overlapping Intervals |
| 78 | 跳躍遊戲（能否到達） | Greedy（追蹤最遠可達位置） | 只需要 boolean | LC 55 Jump Game |
| 79 | 跳躍遊戲（最少跳幾次） | Greedy（BFS-like 層級思維） | 每一「層」是一跳的範圍 | LC 45 Jump Game II |
| 80 | 最少硬幣數 | DP（不是 Greedy！） | Greedy 在某些幣制下失敗 | LC 322 Coin Change |
| 81 | Task scheduling | Greedy + Sorting | 排序後配對 | LC 621 Task Scheduler |
| 82 | 分配餅乾/資源 | Greedy + Sorting | 排序後從小到大配 | LC 455 Assign Cookies |

### 關鍵判斷法

```
Step 1: 嘗試 Greedy — 想一個「直覺上最好」的局部策略
Step 2: 找反例 (Counterexample)
  ├── 找到反例 → ❌ Greedy 失敗 → 用 DP
  └── 找不到反例 → ✓ Greedy 可能可行（面試時可以用）

經典反例:
  硬幣 = [1, 3, 4]，target = 6
  Greedy: 4 + 1 + 1 = 3 枚 ← 錯！
  DP:     3 + 3 = 2 枚     ← 對！
```

### Greedy 常見可證明場景

| 場景 | Greedy 策略 | 為什麼可行 |
|------|------------|-----------|
| 區間排程 | 按結束時間排序 | 早結束 → 留更多空間給後面 |
| 分數背包 | 按 value/weight 排序 | 可以取一部分 |
| Huffman Coding | 每次合併最小的兩個 | 頻率低的放深處 |
| 最大子陣列和 (Kadane's) | 局部和 < 0 就重置 | 負數前綴只會拖累 |
| Jump Game (can reach?) | 維護最遠可達 | 能到的地方越遠越好 |

---

## 家族 10：Union-Find vs DFS/BFS — 連通性問題怎麼選？

### 選擇矩陣

| # | 你遇到的情況 | 選擇 | 原因 | 代表題 |
|---|---|---|---|---|
| 83 | 靜態連通分量計數 | DFS/BFS 或 Union-Find | 都可以，DFS/BFS 較直觀 | LC 200 Number of Islands |
| 84 | 動態加邊 + 查連通性 | Union-Find | O(1) amortized 合併和查詢 | LC 323 Number of Connected Components |
| 85 | 判斷加這條邊會不會形成環 | Union-Find | find(u) == find(v) → 已連通 → 環 | LC 684 Redundant Connection |
| 86 | 需要找連通分量的具體節點列表 | DFS/BFS | DFS/BFS 天然遍歷所有節點 | LC 547 Number of Provinces |
| 87 | 有權重的連通性（如比值關係） | Weighted Union-Find 或 BFS | Union-Find 需要維護權重 | LC 399 Evaluate Division |
| 88 | MST (Minimum Spanning Tree) | Kruskal's (Union-Find) | 排序邊 + Union-Find 判斷環 | LC 1584 Min Cost to Connect Points |
| 89 | 帳號合併 / 等價類 | Union-Find | 多對多的合併關係 | LC 721 Accounts Merge |

### 關鍵決策樹

```
Q: 邊是動態加入的嗎？（online 問題）
├── YES → Union-Find（最佳選擇）
└── NO → Q: 需要遍歷每個連通分量的節點嗎？
          ├── YES → DFS/BFS
          └── NO → Q: 只需要判斷連通性/計數？
                    ├── YES → 兩者皆可，Union-Find 更快
                    └── 其他 → 看具體需求
```

---

# Part B: 資料結構選擇矩陣

## 通用選擇表

| # | 你的需求 | 選擇 | 時間複雜度 | 為什麼不選其他 |
|---|---------|------|-----------|--------------|
| 90 | O(1) 查找 key → value | HashMap | O(1) avg | Array 需要 O(n) 搜尋 |
| 91 | O(1) 查找是否存在 | HashSet | O(1) avg | Array 需要 O(n)；sorted array 需要 O(log n) |
| 92 | 保持排序 + O(log n) 插入/刪除 | BST / SortedList | O(log n) | HashMap 無序；Array 插入 O(n) |
| 93 | 快速取最大值或最小值 | Heap (Priority Queue) | O(log n) push/pop，O(1) peek | Sorted Array 插入 O(n)；HashMap 找最大 O(n) |
| 94 | LIFO (後進先出) | Stack | O(1) push/pop | — |
| 95 | FIFO (先進先出) | Queue / Deque | O(1) enqueue/dequeue | — |
| 96 | 前綴搜尋 (prefix lookup) | Trie | O(m) 其中 m = 前綴長度 | HashMap 只能精確匹配 |
| 97 | 動態連通性 (union/find) | Union-Find | O(α(n)) ≈ O(1) amortized | DFS/BFS 每次查詢 O(V+E) |
| 98 | 區間查詢/更新 | Segment Tree / BIT | O(log n) 查詢/更新 | Array 更新 O(1) 但查詢 O(n) |
| 99 | O(1) 取最大值 + 正常 Stack | Monotonic Stack / Max Stack | O(1) | 普通 Stack 取最大 O(n) |
| 100 | 需要 LRU 緩存 | HashMap + Doubly Linked List | O(1) get/put | 純 HashMap 無法追蹤順序 |

## 進階場景選擇

| 場景 | 最佳選擇 | 次佳選擇 | 別用這個 |
|------|---------|---------|---------|
| Top K 問題 | Min-Heap (大小 K) | QuickSelect | Sort (O(n log n) 太慢) |
| 找中位數 (streaming) | 兩個 Heap (max + min) | SortedList | 一個 Heap (不夠) |
| 合併 K 個有序 List | Min-Heap | Divide & Conquer | 兩兩合併 (效率差) |
| 計數 + 取 Top K Frequent | HashMap + Heap 或 Bucket Sort | — | TreeMap (overkill) |
| 下一個更大元素 | Monotonic Stack | — | Brute Force O(n^2) |
| 滑動窗口最大值 | Monotonic Deque | — | 每次 O(k) 掃描 |
| 圖的表示（稀疏圖） | Adjacency List | — | Adjacency Matrix (浪費空間) |
| 圖的表示（稠密圖 / 查 edge 存在） | Adjacency Matrix | — | Adjacency List (查 edge O(V)) |

---

# Part C: 複雜度需求 → 算法逆推

> 面試官說「需要 O(n log n)」，或你算出 n = 10^5 需要 O(n log n) 以下 — 可以逆推出可能的算法。

## 從 n 的範圍推算法

| n 的大約範圍 | 可接受的複雜度 | 可能的算法 |
|-------------|--------------|-----------|
| n ≤ 10 | O(n!) / O(2^n) | Backtracking (全排列) |
| n ≤ 20 | O(2^n) | Backtracking / Bitmask DP |
| n ≤ 100 | O(n^3) | Floyd-Warshall / 區間 DP |
| n ≤ 1,000 | O(n^2) | DP / Brute Force with optimization |
| n ≤ 10,000 | O(n^2) (borderline) | 可能需要 O(n log n) |
| n ≤ 100,000 | O(n log n) | Sort + something / Binary Search / Heap |
| n ≤ 1,000,000 | O(n) | HashMap / Two Pointers / Sliding Window / Greedy |
| n ≤ 10^9 | O(log n) / O(sqrt(n)) | Binary Search / Math |

## 從目標複雜度推算法

| 目標複雜度 | 可能的算法 | 代表題 |
|-----------|-----------|--------|
| O(1) | Math / Bit Manipulation | LC 231 Power of Two |
| O(log n) | Binary Search | LC 704 Binary Search |
| O(n) | HashMap / Two Pointers / Sliding Window / Greedy / Kadane's | LC 1, LC 3, LC 53 |
| O(n log n) | Sort + Greedy / Sort + Two Pointers / Binary Search 外加線性掃描 / Heap | LC 15, LC 56, LC 347 |
| O(n^2) | DP (2D on 1 sequence) / Brute Force (nested loops) | LC 5, LC 300 (naive) |
| O(n * m) | DP (2 sequences of size n, m) / BFS on grid | LC 1143, LC 62 |
| O(n * W) | Knapsack DP | LC 322, LC 416 |
| O(V + E) | BFS / DFS / Topological Sort | LC 200, LC 207 |
| O((V+E) log V) | Dijkstra | LC 743 |
| O(VE) | Bellman-Ford | LC 787 |
| O(V^3) | Floyd-Warshall | LC 1334 |
| O(2^n) | Backtracking (subsets) / Bitmask DP | LC 78, LC 698 |
| O(n!) | Backtracking (permutations) | LC 46, LC 51 |

## 常見面試複雜度觸發點

```
面試官：「你能做到 O(n) 嗎？」
  → 思考：HashMap (空間換時間) / Two Pointers (需要排序的前提) / Sliding Window / Greedy

面試官：「空間必須 O(1)。」
  → 思考：Two Pointers / 原地修改 / Bit Manipulation / Morris Traversal

面試官：「能比 O(n^2) 更快嗎？」
  → 思考：排序 O(n log n) 後用什麼？/ Binary Search / Heap / Divide and Conquer

面試官：「n 很大（10^6 以上）。」
  → 思考：O(n) 或 O(n log n) 的算法，不能用 O(n^2)
```

---

# Part D: 常見陷阱 — 看起來像 A 但其實是 B

> 這是面試中拉開差距的關鍵：選錯算法 → 浪費 15 分鐘 → 面試失敗。

## 陷阱全覽（30+ 條）

### 陷阱 1-10：基礎算法混淆

| # | 問題描述 | 看起來像 | 其實是 | 關鍵差異 |
|---|---------|---------|--------|---------|
| 1 | Find pair, unsorted array | Two Pointers | HashMap | 未排序無法用 Two Pointers |
| 2 | Subarray sum = k, 有負數 | Sliding Window | Prefix Sum + HashMap | 負數破壞窗口單調性 |
| 3 | Shortest path, weighted graph | BFS | Dijkstra | BFS 只適用無權圖 |
| 4 | Minimum coins to make amount | Greedy | DP (完全背包) | Greedy 在 [1,3,4] target=6 失敗 |
| 5 | Jump Game I (can reach?) | DP | Greedy | 只需要 boolean，greedy O(n) 更快 |
| 6 | Jump Game II (min jumps) | Simple Greedy | BFS-like Greedy（層級思維） | 需要計算「層數」 |
| 7 | Longest substring without repeat | Two Pointers | Sliding Window + HashSet | 需要動態維護窗口內容 |
| 8 | Two Sum (return indices) | Sorting + Two Pointers | HashMap | 排序會打亂原始 index |
| 9 | Kth largest element | Sort | QuickSelect / Min-Heap | Sort O(n log n)，QuickSelect O(n) avg |
| 10 | Merge intervals | Two Pointers | Sort + Linear Scan | 先排序，再合併 |

### 陷阱 11-20：進階算法混淆

| # | 問題描述 | 看起來像 | 其實是 | 關鍵差異 |
|---|---------|---------|--------|---------|
| 11 | Maximum subarray sum | Sliding Window | Kadane's (DP/Greedy) | 有負數不能用窗口 |
| 12 | Word Break | Backtracking | DP (Bottom-up) | Backtracking 超時，DP O(n^2) |
| 13 | Edit Distance | Greedy | 2D DP | 多種操作的最優組合無法 greedy |
| 14 | Course Schedule (can finish?) | BFS 層序 | Topological Sort (DFS 或 Kahn's) | 拓撲排序才能判斷 DAG |
| 15 | Course Schedule II (find order) | DFS 遍歷 | Topological Sort + 輸出順序 | 普通 DFS 不保證拓撲序 |
| 16 | 0/1 Knapsack | Greedy (先拿 value/weight 高的) | DP | 分數背包才能 greedy，0/1 不行 |
| 17 | Palindrome Partitioning | Pure DP | Backtracking + DP 預處理 | 需要列出所有方案，不只是數量 |
| 18 | Number of Islands | Union-Find | DFS/BFS (更簡單) | 靜態圖 DFS/BFS 更直觀 |
| 19 | Accounts Merge | DFS | Union-Find (更自然) | 多對多合併關係用 Union-Find |
| 20 | Median from Data Stream | Sorted Array | Two Heaps | Sorted Array 插入 O(n)，Heap O(log n) |

### 陷阱 21-30：微妙的變體混淆

| # | 問題描述 | 看起來像 | 其實是 | 關鍵差異 |
|---|---------|---------|--------|---------|
| 21 | Subsets (有重複元素) | 標準 Subsets | Subsets + 排序 + 跳過重複 | 不去重會有重複子集 |
| 22 | Combination Sum II (每個只能用一次) | Combination Sum | Combination Sum + 去重 | 需要 `i > start` 跳過邏輯 |
| 23 | BST 的 Kth Smallest | Binary Search | Inorder DFS (第 k 個停止) | 是樹遍歷問題不是搜尋 |
| 24 | LCA in BST | 通用 LCA 做法 | 利用 BST 性質簡化 | BST 的大小關係可以剪枝 |
| 25 | Stock Buy/Sell (one transaction) | DP | Greedy (追蹤 min price) | 只有一次交易時 greedy 更簡潔 |
| 26 | Stock Buy/Sell (k transactions) | Greedy | DP | 多次交易的最優解需要 DP |
| 27 | Longest Palindromic Substring | DP | Expand Around Center | DP O(n^2) space，展開法 O(1) space |
| 28 | Longest Palindromic Subsequence | Expand Around Center | DP | 子序列不連續，不能用展開法 |
| 29 | Trapping Rain Water | Sliding Window | Two Pointers 或 Monotonic Stack | 不是子陣列問題 |
| 30 | Next Greater Element (circular) | 標準 Monotonic Stack | Monotonic Stack + 陣列複製（2n 處理） | 循環需要走兩遍 |

### 陷阱 31-36：Graph 陷阱

| # | 問題描述 | 看起來像 | 其實是 | 關鍵差異 |
|---|---------|---------|--------|---------|
| 31 | Shortest path with negative weights | Dijkstra | Bellman-Ford | Dijkstra 的 greedy 在負權下失效 |
| 32 | Cheapest flights within K stops | Dijkstra | Modified Bellman-Ford (K rounds) | 步數限制改變了問題性質 |
| 33 | Detect cycle in undirected graph | DFS 三色 | DFS (檢查 parent) 或 Union-Find | 無向圖不需要三色，只需要 parent check |
| 34 | Detect cycle in directed graph | Union-Find | DFS 三色標記 | Union-Find 在有向圖不能直接判斷環 |
| 35 | Bipartite check | DFS 全遍歷 | BFS/DFS + 雙色染色 | 需要染色而非單純遍歷 |
| 36 | Minimum Spanning Tree | Dijkstra | Kruskal's (Union-Find) 或 Prim's | Dijkstra 是最短路，不是 MST |

---

## 總結：面試中的算法選擇 Checklist

面試時拿到題目後，按照以下順序思考：

```
Step 1: 辨識問題類型（Level 1）
  → 這是什麼類型？Array? Graph? Tree? DP?

Step 2: 選擇具體算法（Level 2 — 本文件）
  → 在這個家族內，哪個變體最適合？

Step 3: 驗證選擇
  □ 資料特性是否符合？（排序？正數？無權？）
  □ 時間複雜度是否符合 n 的範圍？
  □ 有沒有反例可以推翻我的選擇？

Step 4: 跟面試官確認
  → 「I'm thinking of using Dijkstra because the graph has non-negative weights.
      Does that approach sound reasonable?」
```

### 十大致命選擇錯誤（面試場上最常犯）

```
 1. 未排序用 Two Pointers          → 用 HashMap
 2. 有負數用 Sliding Window        → 用 Prefix Sum + HashMap
 3. 加權圖用 BFS 求最短路          → 用 Dijkstra
 4. 0/1 Knapsack 用 Greedy         → 用 DP
 5. 有向圖環偵測用 Union-Find      → 用 DFS 三色
 6. 求所有方案用 DP                → 用 Backtracking（DP 通常只求數量或最值）
 7. 忘記 BST 的 Inorder = Sorted   → 白白用了更複雜的做法
 8. Dijkstra 處理負權邊            → 用 Bellman-Ford
 9. 大 V 用 Floyd-Warshall         → 用 Dijkstra 跑多次
10. Backtracking 不剪枝            → TLE（面試直接掛）
```

### 算法選擇的「一句話」速查表

| 看到什麼 | 一句話選擇 |
|---------|-----------|
| sorted + find pair | 對向 Two Pointers |
| unsorted + find pair | HashMap |
| contiguous subarray + all positive | Sliding Window |
| contiguous subarray + has negative | Prefix Sum + HashMap |
| sorted + find target / boundary | Binary Search |
| answer space is monotonic | Binary Search on Answer |
| tree + info flows down | Preorder DFS |
| tree + info flows up | Postorder DFS |
| BST + sorted order needed | Inorder DFS |
| graph + shortest path + unweighted | BFS |
| graph + shortest path + positive weights | Dijkstra |
| graph + shortest path + negative weights | Bellman-Ford |
| graph + all pairs shortest | Floyd-Warshall (V small) |
| graph + ordering dependencies | Topological Sort |
| dynamic connectivity / merge sets | Union-Find |
| sequence + optimal value | DP |
| choose or not choose + capacity | Knapsack DP |
| enumerate all subsets | Backtracking (Subsets) |
| enumerate all orderings | Backtracking (Permutations) |
| choose k items from n | Backtracking (Combinations) |
| interval scheduling | Greedy (sort by end time) |
| can reach / can achieve (boolean) | Greedy (if provable) |
| next greater / smaller element | Monotonic Stack |
| top K elements | Heap |
| prefix matching | Trie |
| streaming median | Two Heaps |
| LRU / ordered + O(1) access | HashMap + Doubly Linked List |
| range sum query (static) | Prefix Sum |
| range sum query (dynamic updates) | Segment Tree / BIT |
