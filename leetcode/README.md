# LeetCode 面試準備教材：Google / NVIDIA 導向

> **適用對象**：LeetCode 初學者（尚未刷過 Easy），準備 Google / NVIDIA 面試
> **教學風格**：每題皆附 step-by-step 數值範例，用「跑一次給你看」取代抽象描述
> **語言**：Traditional Chinese + English 技術術語

---

## 目錄

1. [檔案總覽](#檔案總覽)
2. [學習路線圖（四階段）](#學習路線圖)
3. [檔案依賴關係與建議順序](#檔案依賴關係與建議順序)
4. [面試準備時間表](#面試準備時間表)
5. [Google / NVIDIA 常考題型分析](#googlenvidia-常考題型分析)
6. [每個檔案的簡介](#每個檔案的簡介)
7. [如何使用本教材](#如何使用本教材)

---

## 檔案總覽

### A. 可執行 Python 程式碼（18 檔案，20,007 行）

| 編號 | 檔名 | 主題 | 難度階段 |
|------|------|------|----------|
| 00 | `00_解題框架_總覽.py` | Master Decision Tree — 看到什麼用什麼 | 所有階段 |
| 01 | `01_Array_Two_Pointers.py` | Array 基礎 + Two Pointers | Phase 1 |
| 02 | `02_Sliding_Window.py` | Sliding Window（固定/可變長度） | Phase 1 |
| 03 | `03_HashMap_HashSet.py` | HashMap / HashSet 應用 | Phase 1 |
| 04 | `04_Stack_Queue_Monotonic.py` | Stack / Queue / Monotonic Stack | Phase 1 |
| 05 | `05_Linked_List.py` | Linked List 操作與技巧 | Phase 1 |
| 06 | `06_Binary_Search.py` | Binary Search 及其變形 | Phase 2 |
| 07 | `07_Tree_DFS.py` | Tree + DFS（前/中/後序） | Phase 2 |
| 08 | `08_Tree_BFS_BST.py` | Tree BFS (Level Order) + BST 性質 | Phase 2 |
| 09 | `09_Graph_DFS_BFS.py` | Graph 基礎 — DFS / BFS / Connected Components | Phase 2 |
| 10 | `10_Graph_TopSort_UnionFind.py` | Topological Sort + Union-Find + Dijkstra | Phase 3 |
| 11 | `11_DP_1D.py` | Dynamic Programming 一維 | Phase 2 |
| 12 | `12_DP_2D_Knapsack.py` | DP 二維 + Knapsack + LCS / LIS | Phase 3 |
| 13 | `13_Backtracking.py` | Backtracking（排列/組合/子集） | Phase 3 |
| 14 | `14_Greedy.py` | Greedy 策略 | Phase 2 |
| 15 | `15_Heap_Priority_Queue.py` | Heap / Priority Queue | Phase 2 |
| 16 | `16_Trie.py` | Trie (Prefix Tree) | Phase 3 |
| 17 | `17_Sort_And_Bit.py` | Sorting 演算法 + Bit Manipulation | Phase 3 |

### B. 教科書級教學講義（17 檔案，23,446 行）

> 每個主題配一份 .md，含公式推導、2+ 數值範例、step-by-step 走法、corner case 整理

| 編號 | 檔名 | 行數 |
|------|------|------|
| 01 | `01_Array_Two_Pointers_教學.md` | 1,278 |
| 02 | `02_Sliding_Window_教學.md` | 1,732 |
| 03 | `03_HashMap_HashSet_教學.md` | 1,298 |
| 04 | `04_Stack_Queue_教學.md` | 1,497 |
| 05 | `05_Linked_List_教學.md` | 1,266 |
| 06 | `06_Binary_Search_教學.md` | 1,513 |
| 07 | `07_Tree_DFS_教學.md` | 1,331 |
| 08 | `08_Tree_BFS_BST_教學.md` | 1,405 |
| 09 | `09_Graph_DFS_BFS_教學.md` | 1,458 |
| 10 | `10_Graph_Advanced_教學.md` | 1,462 |
| 11 | `11_DP_1D_教學.md` | 1,484 |
| 12 | `12_DP_2D_Knapsack_教學.md` | 1,480 |
| 13 | `13_Backtracking_教學.md` | 1,499 |
| 14 | `14_Greedy_教學.md` | 1,395 |
| 15 | `15_Heap_教學.md` | 1,166 |
| 16 | `16_Trie_教學.md` | 991 |
| 17 | `17_Sort_Bit_教學.md` | 1,191 |

### C. 情境式解題地圖 — 管理顧問式思維（3 檔案，3,088 行）

> 從「問題長什麼樣」出發，而非從「算法叫什麼」出發

| 編號 | 檔名 | 核心內容 | 行數 |
|------|------|---------|------|
| 18 | `18_情境解題地圖_Level1_問題是什麼.md` | 8 大問題類型 × 120+ 情境 | 1,383 |
| 19 | `19_情境解題地圖_Level2_怎麼選算法.md` | 139 條決策規則 × 算法選擇矩陣 | 709 |
| 20 | `20_情境解題地圖_Level3_交叉與實戰.md` | 30 種算法組合 + 40 題鑑別 + 20 模擬 | 996 |

### D. 進階實戰指南（12 檔案，15,904 行）

| 編號 | 檔名 | 核心內容 | 行數 |
|------|------|---------|------|
| 21 | `21_從Easy到Hard的進化路線.md` | 15 條 Easy→Medium→Hard 進化鏈 | 1,432 |
| 22 | `22_解題思考過程_面試官視角.md` | 20 題完整思考過程紀錄 | 1,334 |
| 23 | `23_相似題鑑別大全_100組易混淆題目.md` | 85 組易混淆題目對比 | 1,112 |
| 24 | `24_Google_NVIDIA_高頻題型深度解析.md` | 50 道 Google/NVIDIA 必刷題深度攻略 | 1,397 |
| 25 | `25_Edge_Case陷阱大全.md` | 12 章 edge case 陷阱 | 1,488 |
| 26 | `26_白板Coding模板速查_所有算法模板.md` | 45 個白板模板 | 1,364 |
| 27 | `27_時間空間複雜度完全指南.md` | Big-O 分析 + 攤銷 + 面試應答 | 1,203 |
| 28 | `28_算法之間的深層連結與等價.md` | 11 章算法等價關係 + 統一圖論視角 | 1,201 |
| 29 | `29_面試模擬題組_5回合實戰.md` | 5 回合完整模擬面試 | 1,199 |
| 30 | `30_Python面試技巧與常用API速查.md` | Python 面試技巧與 API 速查 | 1,182 |
| 31 | `31_Hard題拆解術_如何把難題變簡單.md` | 5 策略 × 30 道 Hard 題拆解 | 1,547 |
| 32 | `32_資料結構設計題_LRU_Trie等.md` | 9 道資料結構設計題完整實作 | 1,445 |

---

## 學習路線圖

```
Phase 1: Foundation（地基）        Phase 2: Intermediate（進階）
┌─────────────────────────┐       ┌──────────────────────────┐
│ 00 解題框架（先讀！）     │       │ 06 Binary Search          │
│ 01 Array + Two Pointers  │       │ 07 Tree DFS               │
│ 02 Sliding Window        │  ──►  │ 08 Tree BFS + BST         │
│ 03 HashMap / HashSet     │       │ 09 Graph DFS / BFS        │
│ 04 Stack / Queue         │       │ 11 DP 1D                  │
│ 05 Linked List           │       │ 14 Greedy                 │
└─────────────────────────┘       │ 15 Heap / Priority Queue  │
                                   └──────────────────────────┘
                                              │
                                              ▼
Phase 3: Advanced（高階）          Phase 4: Mock Interview（模擬面試）
┌──────────────────────────┐      ┌──────────────────────────────┐
│ 10 Graph TopSort+UnionFind│      │ 回頭重做 Phase 1-3 的題目    │
│ 12 DP 2D + Knapsack      │      │ 限時 25 分鐘/題              │
│ 13 Backtracking          │      │ 口述解題（用英文練習）        │
│ 16 Trie                  │      │ 29 模擬面試題組              │
│ 17 Sort + Bit            │      │ 32 資料結構設計題            │
└──────────────────────────┘      └──────────────────────────────┘
```

### 各 Phase 目標

| Phase | 目標 | 預期完成題數 | 對應 LeetCode 難度 |
|-------|------|------------|-------------------|
| 1 — Foundation | 學會基本資料結構操作 + 暴力解 → 最佳解的思考流程 | 40-50 題 | Easy + Easy-Medium |
| 2 — Intermediate | 掌握 Tree / Graph / DP 入門 + Binary Search 變形 | 50-60 題 | Medium |
| 3 — Advanced | 征服 Hard 級模式 + 複合型問題 | 40-50 題 | Medium-Hard |
| 4 — Mock Interview | 限時練習 + 口述思路 + Edge Case 訓練 | 複習為主 | 混合 |

---

## 檔案依賴關係與建議順序

```
00 解題框架 ──────────────────────────────── (先讀，隨時回來查)
     │
     ├── 01 Array + Two Pointers ◄── 起點
     │    ├── 02 Sliding Window（延伸 Two Pointers 概念）
     │    └── 06 Binary Search（Array 上的搜尋）
     │
     ├── 03 HashMap / HashSet ◄── 與 01 平行學習
     │    └── 16 Trie（HashMap 的樹狀延伸）
     │
     ├── 04 Stack / Queue
     │    └── 15 Heap / Priority Queue（Queue 的延伸）
     │
     ├── 05 Linked List ◄── 獨立主題，可穿插
     │
     ├── 07 Tree DFS ◄── 需要先會 Recursion 概念
     │    ├── 08 Tree BFS + BST（Tree 的另一種走法）
     │    └── 13 Backtracking（DFS 的延伸應用）
     │
     ├── 09 Graph DFS / BFS ◄── 需要先會 07, 08
     │    └── 10 TopSort + Union-Find + Dijkstra
     │
     ├── 11 DP 1D ◄── 需要先會 Recursion
     │    └── 12 DP 2D + Knapsack
     │
     ├── 14 Greedy ◄── 可獨立學習，但建議在 DP 之後
     │
     └── 17 Sort + Bit ◄── 獨立主題，穿插學習
```

### 嚴格的先修關係（必須遵守）

| 檔案 | 先修 |
|------|------|
| 02 Sliding Window | 01 Array + Two Pointers |
| 06 Binary Search | 01 Array + Two Pointers |
| 08 Tree BFS + BST | 07 Tree DFS |
| 09 Graph DFS / BFS | 07 Tree DFS + 08 Tree BFS |
| 10 TopSort + UnionFind | 09 Graph DFS / BFS |
| 12 DP 2D | 11 DP 1D |
| 13 Backtracking | 07 Tree DFS |
| 16 Trie | 03 HashMap |

### 建議的學習搭配

每學完一個 `.py` 檔案，搭配閱讀對應的 `_教學.md` 檔案加深理解。
進入 Phase 3 後，搭配閱讀 18-20 情境解題地圖，建立「問題→算法」的直覺。
面試前衝刺，搭配 21-32 進階實戰指南。

---

## 面試準備時間表

### 4 週衝刺版（每天 3-4 小時）

> 適合：已有一定程式基礎，時間緊迫

| 週次 | 內容 | 每日題數 | 重點 |
|------|------|---------|------|
| Week 1 | 00 + 01 + 02 + 03 + 04 + 05 | 3-4 題/天 | 打穩 Array/String/HashMap 基礎 |
| Week 2 | 06 + 07 + 08 + 11 + 14 + 15 | 3-4 題/天 | Binary Search + Tree + DP 入門 |
| Week 3 | 09 + 10 + 12 + 13 | 2-3 題/天 | Graph + DP 進階 + Backtracking |
| Week 4 | 16 + 17 + 29 模擬面試 | 2 題/天 + 模擬 | 補缺 + 限時練習 |

### 8 週穩健版（每天 2-3 小時）

> 適合：初學者，建議的最低準備時間

| 週次 | 內容 | 每日題數 |
|------|------|---------|
| Week 1 | 00 框架 + 01 Array/Two Pointers | 2 題/天 |
| Week 2 | 02 Sliding Window + 03 HashMap | 2 題/天 |
| Week 3 | 04 Stack/Queue + 05 Linked List + 06 Binary Search | 2-3 題/天 |
| Week 4 | 07 Tree DFS + 08 Tree BFS/BST | 2-3 題/天 |
| Week 5 | 09 Graph + 10 TopSort/UnionFind/Dijkstra | 2 題/天 |
| Week 6 | 11 DP 1D + 12 DP 2D/Knapsack | 2 題/天 |
| Week 7 | 13 Backtracking + 14 Greedy + 15 Heap + 16 Trie + 17 Sort/Bit | 2-3 題/天 |
| Week 8 | 18-20 情境地圖 + 29 模擬面試（每天一場 45 分鐘模擬） | 2 題 + 模擬 |

### 12 週從容版（每天 1.5-2 小時）

> 適合：完全零基礎，想扎實學會每個概念

| 週次 | 內容 |
|------|------|
| Week 1-2 | 00 框架 + 01 Array/Two Pointers（反覆練習直到熟練） |
| Week 3 | 02 Sliding Window |
| Week 4 | 03 HashMap + 04 Stack/Queue |
| Week 5 | 05 Linked List + 06 Binary Search |
| Week 6 | 07 Tree DFS + 08 Tree BFS/BST |
| Week 7 | 09 Graph + 10 TopSort/UnionFind/Dijkstra |
| Week 8 | 11 DP 1D |
| Week 9 | 12 DP 2D + Knapsack |
| Week 10 | 13 Backtracking + 14 Greedy + 15 Heap + 16 Trie + 17 Sort/Bit |
| Week 11 | 18-20 情境地圖 + 21-28 進階指南 |
| Week 12 | 29 模擬面試 + 31 Hard拆解 + 32 設計題（每天限時練 2 題 + 口述） |

---

## Google / NVIDIA 常考題型分析

### Google 面試特色

```
Google 面試 = 45 分鐘 = 5 分鐘寒暄 + 35 分鐘 Coding + 5 分鐘提問

重點考察：
├── 1. Array / String 操作 ★★★★★（幾乎每場都有）
│    → 01, 02, 03
├── 2. Tree / Graph ★★★★★（第二常見）
│    → 07, 08, 09, 10
├── 3. Dynamic Programming ★★★★☆
│    → 11, 12
├── 4. Binary Search 變形 ★★★★☆（愛考 search in rotated array 類型）
│    → 06
├── 5. Backtracking ★★★☆☆
│    → 13
├── 6. System Design 相關的 Data Structure ★★★☆☆
│    → 15 (Heap), 16 (Trie), 32 (設計題)
└── 7. Greedy + Math ★★☆☆☆
     → 14
```

**Google 高頻考題模式：**
- Two Sum / Three Sum 變形
- Sliding Window Maximum / Minimum
- Binary Search on Answer（答案上做二分搜尋）
- Tree 的 LCA (Lowest Common Ancestor)
- Graph 的 BFS 最短路徑
- DP 的 House Robber / Coin Change 系列
- Backtracking 的 Word Search / Letter Combinations
- Design HashMap / LRU Cache

### NVIDIA 面試特色

```
NVIDIA 面試特色（偏向系統 + 算法結合）：
├── 1. Array / Matrix 操作 ★★★★★
│    → 01, 12（矩陣 DP）
├── 2. Graph 算法 ★★★★★（因為 GPU 計算圖）
│    → 09, 10
├── 3. Sorting + Searching ★★★★☆
│    → 06, 17
├── 4. Bit Manipulation ★★★★☆（硬體相關職位必考）
│    → 17
├── 5. Dynamic Programming ★★★☆☆
│    → 11, 12
├── 6. Linked List / Memory 操作 ★★★☆☆（考記憶體觀念）
│    → 05
└── 7. Heap / Priority Queue ★★★☆☆（Task Scheduling 相關）
     → 15
```

**NVIDIA 高頻考題模式：**
- Matrix Rotation / Spiral Order
- Graph 的 Topological Sort（Task Dependency）
- Bit Manipulation（Count Bits, Power of Two）
- Merge Intervals（Scheduling）
- Sort Colors / Kth Largest（排序變形）
- Linked List Cycle Detection
- Shortest Path（Dijkstra 用於 routing）

### 兩家共同的高頻主題（優先準備）

| 優先級 | 主題 | 對應檔案 | 建議題數 |
|--------|------|---------|---------|
| ★★★★★ | Array + Two Pointers | 01 | 10+ 題 |
| ★★★★★ | HashMap / HashSet | 03 | 8+ 題 |
| ★★★★★ | Binary Search | 06 | 8+ 題 |
| ★★★★★ | Tree DFS / BFS | 07, 08 | 10+ 題 |
| ★★★★★ | Graph BFS / DFS | 09 | 8+ 題 |
| ★★★★☆ | Dynamic Programming | 11, 12 | 10+ 題 |
| ★★★★☆ | Sliding Window | 02 | 5+ 題 |
| ★★★☆☆ | Stack / Queue | 04 | 5+ 題 |
| ★★★☆☆ | Backtracking | 13 | 5+ 題 |
| ★★★☆☆ | Heap | 15 | 5+ 題 |
| ★★☆☆☆ | Greedy | 14 | 3+ 題 |
| ★★☆☆☆ | Trie | 16 | 3+ 題 |
| ★★☆☆☆ | Sort + Bit | 17 | 5+ 題 |

---

## 每個檔案的簡介

### `00_解題框架_總覽.py` — Master Decision Tree

**可直接執行的 Python 檔案。** 包含：
- 完整的「看到什麼關鍵字 → 用什麼演算法」對照表
- 所有算法的時間/空間複雜度速查表
- 20+ 種常見 Pattern 辨識範例
- Decision Tree 函數：輸入題目特徵，輸出建議演算法
- `python 00_解題框架_總覽.py` 即可印出完整框架

**用途**：解題前先查這個檔案，培養「Pattern 辨識」直覺。

---

### `01_Array_Two_Pointers.py` — Array 基礎 + Two Pointers

**核心概念**：
- Array 的基本操作（traverse, insert, delete）
- Two Pointers 三種模式：同向、反向、快慢指標
- Prefix Sum 前綴和技巧

**經典題目**：Two Sum, Three Sum, Container With Most Water, Remove Duplicates, Trapping Rain Water

---

### `02_Sliding_Window.py` — Sliding Window

**核心概念**：
- 固定長度視窗 vs 可變長度視窗
- 視窗的擴張與收縮邏輯
- 何時該用 Sliding Window 而非 Two Pointers

**經典題目**：Maximum Average Subarray, Longest Substring Without Repeating Characters, Minimum Window Substring

---

### `03_HashMap_HashSet.py` — HashMap / HashSet 應用

**核心概念**：
- Hash Table 的原理（collision handling）
- HashMap 用於 counting / grouping / lookup
- HashSet 用於 deduplication / existence check

**經典題目**：Two Sum, Group Anagrams, Longest Consecutive Sequence, Valid Sudoku

---

### `04_Stack_Queue_Monotonic.py` — Stack / Queue / Monotonic Stack

**核心概念**：
- Stack (LIFO) vs Queue (FIFO) 使用時機
- Monotonic Stack：找「下一個更大/更小元素」
- 括號匹配、表達式求值

**經典題目**：Valid Parentheses, Daily Temperatures, Next Greater Element, Min Stack

---

### `05_Linked_List.py` — Linked List 操作

**核心概念**：
- Singly vs Doubly Linked List
- Dummy Head 技巧（簡化邊界情況）
- 快慢指標找中點 / 偵測環

**經典題目**：Reverse Linked List, Merge Two Sorted Lists, Linked List Cycle, Remove Nth Node From End

---

### `06_Binary_Search.py` — Binary Search 及其變形

**核心概念**：
- 標準 Binary Search + 邊界處理（left, right, mid 的選擇）
- Lower Bound / Upper Bound
- Search on Answer（在答案空間做二分搜尋）

**經典題目**：Search in Rotated Sorted Array, Find Peak Element, Koko Eating Bananas, Median of Two Sorted Arrays

---

### `07_Tree_DFS.py` — Tree + DFS

**核心概念**：
- 前序 (Preorder) / 中序 (Inorder) / 後序 (Postorder) 遍歷
- Recursive vs Iterative DFS
- Tree 的常見技巧：求高度、判斷平衡、路徑和

**經典題目**：Maximum Depth, Invert Binary Tree, Path Sum, Lowest Common Ancestor, Diameter of Binary Tree

---

### `08_Tree_BFS_BST.py` — Tree BFS + BST 性質

**核心概念**：
- Level Order Traversal（用 Queue）
- BST 的 Inorder 是排序的！
- BST 的搜尋、插入、刪除

**經典題目**：Binary Tree Level Order Traversal, Validate BST, Kth Smallest Element in BST, Serialize and Deserialize Binary Tree

---

### `09_Graph_DFS_BFS.py` — Graph 基礎

**核心概念**：
- Graph 的表示法：Adjacency List vs Adjacency Matrix
- DFS / BFS 在 Graph 上的應用
- Connected Components / Cycle Detection

**經典題目**：Number of Islands, Clone Graph, Pacific Atlantic Water Flow, Course Schedule

---

### `10_Graph_TopSort_UnionFind.py` — Topological Sort + Union-Find + Dijkstra

**核心概念**：
- Topological Sort（Kahn's Algorithm / DFS-based）
- Union-Find（Disjoint Set）with Path Compression + Union by Rank
- Dijkstra 最短路徑算法

**經典題目**：Course Schedule II, Alien Dictionary, Number of Connected Components, Redundant Connection, Network Delay Time

---

### `11_DP_1D.py` — Dynamic Programming 一維

**核心概念**：
- DP 的本質：重疊子問題 + 最優子結構
- Top-Down (Memoization) vs Bottom-Up (Tabulation)
- 狀態定義 → 轉移方程 → Base Case → 計算順序

**經典題目**：Climbing Stairs, House Robber, Coin Change, Longest Increasing Subsequence, Word Break

---

### `12_DP_2D_Knapsack.py` — DP 二維 + Knapsack

**核心概念**：
- 二維 DP 表格的填充方向
- 0/1 Knapsack vs Unbounded Knapsack
- LCS (Longest Common Subsequence) / Edit Distance

**經典題目**：Unique Paths, Longest Common Subsequence, Edit Distance, 0/1 Knapsack, Partition Equal Subset Sum

---

### `13_Backtracking.py` — Backtracking

**核心概念**：
- Backtracking = DFS + 剪枝 (Pruning)
- 排列 (Permutation) vs 組合 (Combination) vs 子集 (Subset)
- 去重技巧（排序後跳過重複元素）

**經典題目**：Subsets, Permutations, Combination Sum, N-Queens, Word Search

---

### `14_Greedy.py` — Greedy 策略

**核心概念**：
- Greedy 的適用條件：局部最優 → 全域最優
- 常見 Greedy 策略：排序後貪心、區間貪心
- Greedy vs DP：如何判斷該用哪一個

**經典題目**：Jump Game, Merge Intervals, Non-overlapping Intervals, Task Scheduler, Gas Station

---

### `15_Heap_Priority_Queue.py` — Heap / Priority Queue

**核心概念**：
- Min-Heap vs Max-Heap
- Python 的 `heapq` 模組（預設 Min-Heap）
- Top K 問題的統一解法

**經典題目**：Kth Largest Element, Top K Frequent Elements, Merge K Sorted Lists, Find Median from Data Stream

---

### `16_Trie.py` — Trie (Prefix Tree)

**核心概念**：
- Trie 的結構與實作
- Insert / Search / StartsWith
- Trie 在自動補全、拼字檢查的應用

**經典題目**：Implement Trie, Word Search II, Design Add and Search Words Data Structure

---

### `17_Sort_And_Bit.py` — Sorting + Bit Manipulation

**核心概念**：
- Quick Sort / Merge Sort / Counting Sort 原理
- Bit 操作：AND, OR, XOR, Shift
- 常見 Bit 技巧：`n & (n-1)`, `n & (-n)`

**經典題目**：Sort Colors, Merge Intervals (sort-based), Single Number, Counting Bits, Reverse Bits

---

## 如何使用本教材

### Step 1：先執行 `00_解題框架_總覽.py`

```bash
cd /Users/william/Downloads/phd_exam/leetcode/
python 00_解題框架_總覽.py
```

把輸出印出來（或截圖），解題時隨時對照。

### Step 2：按照路線圖順序閱讀 + 實作

每個主題有三層材料：
1. **`.py` 檔案** — 直接 `python filename.py` 執行，看數值 trace
2. **`_教學.md` 檔案** — 教科書級深度講解，含公式推導、2+ 範例、corner case
3. **進階指南 (18-32)** — 情境地圖、模擬面試、Hard 拆解等

學習流程：先讀 `.md` 教學 → 跑 `.py` 看 trace → 到 LeetCode 實際寫 → 卡住回來查

### Step 3：建立自己的錯題本

每次寫錯的題目，記下：
1. 題號和題目名稱
2. 自己一開始的錯誤思路
3. 正確的 pattern 是什麼
4. 為什麼沒有辨識出來

### Step 4：模擬面試

- 用計時器，每題 25 分鐘
- 先口述思路（英文），再寫 code
- 寫完後分析時間/空間複雜度
- 想 edge cases：空陣列、一個元素、負數、overflow

### 面試當天的解題流程

```
1. 聽完題目 → 問 clarifying questions（2 分鐘）
   - Input 的範圍？（size, value range）
   - 有沒有 duplicate？是否 sorted？
   - 要求 return 什麼？（index? value? boolean?）

2. 想解法 + 說出來（5 分鐘）
   - 先說 brute force → 再優化
   - 用 00_解題框架 的 decision tree 辨識 pattern
   - 說出時間/空間複雜度

3. 寫 code（15-20 分鐘）
   - 先寫 function signature
   - 邊寫邊解釋
   - 變數命名要有意義

4. Test + Debug（5 分鐘）
   - 用一個小 example 手動 trace
   - 想 edge cases
   - 修 bug（不要慌）
```

---

## 總結

本教材共 **51 個檔案、62,989 行**，涵蓋 LeetCode 面試所需的所有核心主題：

| 類別 | 檔案數 | 行數 | 說明 |
|------|--------|------|------|
| A. Python 程式碼 | 18 | 20,007 | 可直接執行，每題附 step-by-step 數值 trace |
| B. 教學講義 | 17 | 23,446 | 教科書級，含公式推導、2+ 範例、corner case |
| C. 情境解題地圖 | 3 | 3,088 | 管理顧問式：從問題情境→算法選擇 |
| D. 進階實戰指南 | 12 | 15,904 | 模擬面試、Hard 拆解、模板速查等 |
| README | 1 | 544 | 本檔 |
| **合計** | **51** | **62,989** | |

每個 `.py` 檔案：`python filename.py` 直接跑，用具體數字走一遍。
每個 `.md` 檔案：從「不懂」到「懂」的完整教學，不跳步驟。

祝準備順利，拿到 Google / NVIDIA offer!
