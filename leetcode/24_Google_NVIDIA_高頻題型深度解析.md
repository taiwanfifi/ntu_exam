# Google & NVIDIA 高頻題型深度解析

> **適用對象**：目標 Google / NVIDIA 的面試準備者
> **定位**：公司專屬的題型頻率分析、面試格式拆解、50 題必刷清單
> **語言**：繁體中文解說 + English technical terms
> **核心原則**：每一條建議都可以直接執行，不講廢話

---

## 目錄

| Part | 內容 | 頁內連結 |
|------|------|---------|
| A | Google 面試深度解析 | [Part A](#part-a-google-面試深度解析) |
| B | NVIDIA 面試深度解析 | [Part B](#part-b-nvidia-面試深度解析) |
| C | 50 題必刷清單 | [Part C](#part-c-50-題必刷清單) |
| D | 面試前一天的終極複習清單 | [Part D](#part-d-面試前一天的終極複習清單) |

---

# Part A: Google 面試深度解析

---

## 第一章：Google 面試格式完全拆解

### 1.1 面試流程

```
階段 1: Recruiter Call（30 min）
└── 非技術，確認背景、期望職級、時間線

階段 2: Phone Screen（45 min）
├── 1 位工程師
├── 1-2 題 Coding（通常 Medium，偶爾 Easy→Medium 連續）
├── 在 Google Docs 或自選 IDE 上寫 code
└── 通過率約 30-40%

階段 3: Onsite（4-5 rounds，各 45 min）
├── Round 1: Coding/Algorithm ★
├── Round 2: Coding/Algorithm ★
├── Round 3: Coding/Algorithm ★（L5+ 可能換 System Design）
├── Round 4: System Design（L4+ 才考）
└── Round 5: Googleyness & Leadership（行為面試）
```

### 1.2 職級對照 (Level)

| Level | 對應經驗 | 面試重點 | Coding 難度 |
|-------|---------|---------|------------|
| L3 | New Grad / 0-2 年 | 純 Coding（3 rounds） | Medium 為主 |
| L4 | 2-5 年 | Coding + 簡易 System Design | Medium-Hard |
| L5 | 5-10 年（Senior） | Coding + 完整 System Design | Hard 會出現 |
| L6+ | Staff+ | Design 占比更大 | Hard + 開放式 |

### 1.3 時間分配 (45 分鐘 Coding Round)

```
[0:00-0:02]  寒暄 + 自我介紹
[0:02-0:05]  讀題 + 問 Clarifying Questions
[0:05-0:10]  口述 Brute Force → 優化思路
[0:10-0:12]  確認思路，面試官同意後才寫 code
[0:12-0:32]  寫 code（20 分鐘是黃金寫 code 時間）
[0:32-0:38]  Dry run + Edge cases
[0:38-0:42]  Follow-up 問題（面試官加碼）
[0:42-0:45]  你問面試官的問題
```

**關鍵**：Google 面試官會在你寫完第一題後追加 follow-up，這是區分 Hire / Strong Hire 的關鍵。

---

## 第二章：Google 最愛的 15 個題型（按頻率排序）

---

### Tier 1 -- 幾乎必考（每次 onsite 至少碰到一題）

---

#### 題型 1: Graph 遍歷 (DFS/BFS on Grid/Graph)

**頻率**：每次面試都會碰到至少一題
**為什麼 Google 愛考**：測試基本功 + 可以無限追加 follow-up + 可以討論分散式

##### 代表題

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 200 | Number of Islands | Medium | Grid DFS/BFS 經典入門 |
| 994 | Rotting Oranges | Medium | Multi-source BFS |
| 127 | Word Ladder | Hard | BFS 最短路徑 |
| 417 | Pacific Atlantic Water Flow | Medium | 反向 DFS from 邊界 |
| 1091 | Shortest Path in Binary Matrix | Medium | BFS on Grid |
| 733 | Flood Fill | Easy | 最基本的 Grid DFS |

##### 常見 Follow-up 以及你該怎麼回答

```
Follow-up 1: "如果 grid 非常大（10^9 x 10^9）怎麼辦？"
→ 回答：無法放進記憶體，需要分散式處理。
  - 把 grid 分割成 chunks
  - 每個 chunk 獨立做 DFS/BFS
  - 再把邊界上的 component merge（用 Union-Find）

Follow-up 2: "如果有不同類型的 island？"
→ 回答：對每種類型分別做 DFS/BFS，或用 HashMap 追蹤 island signature

Follow-up 3: "如何找最大的 island？"
→ 回答：DFS 時記錄每個 component 的 size，取最大值
```

##### 你必須能寫出的模板（10 分鐘內完成）

```python
# Grid BFS Template
from collections import deque

def bfs_grid(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    def bfs(r, c):
        queue = deque([(r, c)])
        visited.add((r, c))
        while queue:
            cr, cc = queue.popleft()
            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and grid[nr][nc] == 1):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                bfs(r, c)
                count += 1
    return count
```

**時間預算**：你應該能在 8-10 分鐘內從零寫出乾淨的 Grid BFS/DFS。如果超過 15 分鐘，表示還不夠熟。

---

#### 題型 2: Tree DFS (Path/Value Problems)

**頻率**：幾乎必考
**為什麼 Google 愛考**：考 recursion 理解深度 + 可以考各種 return 值技巧

##### 代表題

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 124 | Binary Tree Maximum Path Sum | Hard | 全域變數追蹤最大值，遞迴回傳單邊最大 |
| 543 | Diameter of Binary Tree | Easy | 跟 124 同套路，回傳深度，更新直徑 |
| 236 | Lowest Common Ancestor | Medium | 後序遍歷 + null 回傳邏輯 |
| 297 | Serialize and Deserialize Binary Tree | Hard | Preorder DFS + Queue 重建 |
| 98 | Validate Binary Search Tree | Medium | Inorder 或帶 range 的 DFS |
| 105 | Construct Binary Tree from Preorder and Inorder | Medium | 遞迴分割 |

##### 常見 Follow-up

```
Follow-up 1: "如果是 N-ary Tree？"
→ 回答：把 left/right 改成 for child in node.children，邏輯完全一樣

Follow-up 2: "如果 Tree 很深（10^5 層）？"
→ 回答：Recursion 會 stack overflow，改用 iterative DFS（自己維護 stack）

Follow-up 3: "Serialize 的格式能不能更省空間？"
→ 回答：可以用 bit encoding 或省略 null marker
```

##### 必背模板

```python
# Tree DFS — 同時追蹤「全域最優」和「回傳值」的雙軌模板
class Solution:
    def maxPathSum(self, root):
        self.result = float('-inf')

        def dfs(node):
            if not node:
                return 0
            left = max(dfs(node.left), 0)   # 負數不如不取
            right = max(dfs(node.right), 0)
            # 全域更新：左 + 自己 + 右
            self.result = max(self.result, left + node.val + right)
            # 回傳：只能選一邊 + 自己（給上層用）
            return node.val + max(left, right)

        dfs(root)
        return self.result
```

**時間預算**：Medium Tree 題 12-15 分鐘，Hard 題（如 LC 124）20 分鐘。

---

#### 題型 3: Binary Search 變形

**頻率**：幾乎必考
**為什麼 Google 愛考**：包裝成實際問題後，很多人認不出來是 Binary Search

##### 代表題

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 875 | Koko Eating Bananas | Medium | Binary Search on Answer 經典 |
| 1011 | Capacity To Ship Packages | Medium | 同 875 套路 |
| 410 | Split Array Largest Sum | Hard | Binary Search on Answer + 驗證 |
| 33 | Search in Rotated Sorted Array | Medium | 判斷哪半邊有序 |
| 153 | Find Minimum in Rotated Sorted Array | Medium | 比較 mid 和 right |
| 4 | Median of Two Sorted Arrays | Hard | Binary Search on 分割線 |

##### Google 最愛的考法：Binary Search on Answer

```
問題模式：
  "最少需要多少 ___，才能在 ___ 條件下完成 ___？"
  "最大的最小值是多少？" / "最小的最大值是多少？"

解題框架：
  1. 確定答案的搜尋範圍 [lo, hi]
  2. 寫一個 feasible(mid) 函數，判斷 mid 這個答案是否可行
  3. Binary Search 找最小可行 / 最大可行
```

##### 必背模板

```python
# Binary Search on Answer — 找最小可行答案
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid        # mid 可行，嘗試更小
        else:
            lo = mid + 1    # mid 不可行，答案更大
    return lo

# 範例：LC 875 Koko Eating Bananas
def minEatingSpeed(piles, h):
    def feasible(speed):
        return sum((p + speed - 1) // speed for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**時間預算**：標準 Binary Search 5-8 分鐘。Search on Answer 12-15 分鐘（含 feasible 函數）。

---

#### 題型 4: HashMap/HashSet 應用

**頻率**：極高（幾乎每次至少作為某題的子步驟出現）

##### 代表題

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 1 | Two Sum | Easy | HashMap 存 complement |
| 560 | Subarray Sum Equals K | Medium | Prefix Sum + HashMap |
| 49 | Group Anagrams | Medium | sorted string 當 key |
| 128 | Longest Consecutive Sequence | Medium | HashSet + 只從起點開始 |
| 380 | Insert Delete GetRandom O(1) | Medium | HashMap + Array 配合 |
| 146 | LRU Cache | Medium | HashMap + Doubly Linked List |

##### 常見 Follow-up

```
Follow-up: "如果資料量太大放不進記憶體？"
→ 回答：External hashing — 先對 key hash 分桶到 disk，每個桶分別處理

Follow-up: "如果有 hash collision 怎麼辦？"
→ 回答：Chaining（linked list）或 Open Addressing。
  Python dict 用 open addressing with probing。
```

**時間預算**：HashMap 基礎題 8-10 分鐘。Prefix Sum + HashMap 組合 12-15 分鐘。

---

#### 題型 5: Sliding Window

**頻率**：極高

##### 代表題

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 3 | Longest Substring Without Repeating Characters | Medium | 可變窗口 + HashSet |
| 76 | Minimum Window Substring | Hard | 計數窗口 + need/have |
| 239 | Sliding Window Maximum | Hard | Monotonic Deque |
| 567 | Permutation in String | Medium | 固定窗口 + 字元計數 |
| 438 | Find All Anagrams in a String | Medium | 同 567 |

##### 必背模板

```python
# Sliding Window — 可變長度求最長
def longest_window(s):
    window = {}  # 或 set
    left = 0
    result = 0
    for right in range(len(s)):
        # 擴張：加入 s[right]
        window[s[right]] = window.get(s[right], 0) + 1
        # 收縮：違反條件時移動 left
        while invalid_condition(window):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        result = max(result, right - left + 1)
    return result
```

**時間預算**：Medium Sliding Window 10-12 分鐘。Hard（如 LC 76）15-18 分鐘。

---

### Tier 2 -- 高頻（每 2-3 次 onsite 碰到一題）

---

#### 題型 6: Topological Sort (Course Schedule 類型)

**代表題**：LC 207 Course Schedule, LC 210 Course Schedule II, LC 269 Alien Dictionary

**為什麼 Google 愛考**：Google 內部大量依賴圖（build systems, task scheduling）

```python
# Kahn's Algorithm (BFS-based TopSort)
from collections import deque, defaultdict

def topological_sort(num_nodes, edges):
    graph = defaultdict(list)
    in_degree = [0] * num_nodes
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_nodes else []  # 空 = 有環
```

---

#### 題型 7: Union-Find

**代表題**：LC 323 Number of Connected Components, LC 684 Redundant Connection, LC 721 Accounts Merge

```python
# Union-Find with Path Compression + Union by Rank
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # 已經連通
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

---

#### 題型 8: Dynamic Programming (Edit Distance / LCS 類型)

**代表題**：LC 72 Edit Distance, LC 1143 LCS, LC 322 Coin Change, LC 300 LIS

**Google DP 考法特色**：通常不會考太難的 DP，但會要求你清楚說明狀態定義和轉移方程。

```
面試時的表達框架：
1. "Let me define the state: dp[i] represents ..."
2. "The transition is: dp[i] = ... because ..."
3. "Base case: dp[0] = ... because ..."
4. "The answer is dp[n] / max(dp)"
5. "Time: O(...), Space: O(...)"
```

---

#### 題型 9: Backtracking (N-Queens, Word Search)

**代表題**：LC 79 Word Search, LC 51 N-Queens, LC 22 Generate Parentheses, LC 17 Letter Combinations

**時間預算**：Backtracking Medium 15 分鐘，Hard 20 分鐘。

---

#### 題型 10: Monotonic Stack

**代表題**：LC 84 Largest Rectangle in Histogram, LC 739 Daily Temperatures, LC 496 Next Greater Element

---

### Tier 3 -- 中頻（每 4-5 次 onsite 碰到一題）

| 題型 | 代表題 | 備註 |
|------|--------|------|
| Trie | LC 208 Implement Trie, LC 212 Word Search II | 自動補全相關 |
| Dijkstra | LC 743 Network Delay Time, LC 787 Cheapest Flights | 加權圖最短路 |
| Two Heaps (Median) | LC 295 Find Median from Data Stream | 維護動態中位數 |
| Merge K Sorted | LC 23 Merge K Sorted Lists | Heap 應用 |
| Design 題 | LC 146 LRU Cache, LC 460 LFU Cache | 資料結構設計 |

---

## 第三章：Google 面試的 10 個特殊模式

Google 面試官有一套經典的「追問模式」。提前準備好這些 follow-up 的回答，會讓你從 Lean Hire 變成 Strong Hire。

### 模式 1: "What if the input is very large?"

```
觸發條件：你給出 O(n) 或 O(n log n) 的解法後
面試官想聽到的：

情境 A — 資料太大放不進記憶體：
  → External Sort / External Hashing
  → MapReduce 思維：Map 階段分散處理，Reduce 階段合併
  → Streaming Algorithm（一次只看一筆資料）

情境 B — 需要更快的查詢：
  → Preprocessing（建索引）
  → Cache frequently accessed results

你的回答模板：
  "If the input doesn't fit in memory, I would consider
   partitioning it into chunks, processing each chunk
   independently, and then merging the results."
```

### 模式 2: "What if we need real-time?"

```
面試官想聽到的：
  → Batch processing vs Stream processing 的 tradeoff
  → 是否可以用近似值（approximate algorithm）
  → 預處理 + O(1) 查詢
  → 考慮 latency vs throughput 的 tradeoff
```

### 模式 3: "Can you do better?"

```
面試官想聽到的（按順序嘗試）：
  1. 降低時間複雜度：O(n^2) → O(n log n) → O(n)
  2. 降低空間複雜度：O(n) → O(1)
  3. 如果已經是最優，說："This is optimal because
     we need to look at every element at least once,
     so O(n) is the lower bound."
```

### 模式 4: "What about edge cases?"

```
你應該主動提到的 Edge Cases 清單：
  □ 空輸入：[], "", null
  □ 單一元素：[1], "a"
  □ 所有元素相同：[5,5,5,5]
  □ 負數：[-1, -2, 3]
  □ 溢位：int 超過 2^31
  □ 有重複：[1,2,2,3]
  □ 已排序 / 反向排序
  □ 極端大小：n = 0, n = 1, n = 10^5
```

### 模式 5: "What if there are duplicates?"

```
常見處理方式：
  → 排序後跳過：while i < n and nums[i] == nums[i-1]: i += 1
  → 用 Set 去重
  → HashMap 計數
  → 在 Backtracking 中加入 used[] 或排序 + 跳過
```

### 模式 6: Follow-up 連環炮（Easy → Medium → Hard）

```
範例流程：
  Q1 (5 min): "Given a sorted array, find if a target exists."
              → Binary Search, O(log n)
  Q2 (10 min): "Now the array is rotated. Find the target."
              → LC 33, 判斷哪半邊有序
  Q3 (15 min): "Now there might be duplicates."
              → LC 81, worst case O(n)
  Q4 (10 min): "How would you test this? Write test cases."

策略：
  - 前面的題要快！Q1 如果花太久，後面沒時間
  - 每題寫完立刻說 "Ready for the next one"
```

### 模式 7: Multi-part 問題（A 的輸出當 B 的輸入）

```
範例：
  Part A: "Parse this log file and extract timestamps"
  Part B: "Now find the peak hour"
  Part C: "Now optimize for streaming input"

策略：
  - Part A 的 code 要模組化，方便 Part B 呼叫
  - 用好的 function naming，讓面試官看懂你的架構
```

### 模式 8: Constraint 改變（"Now what if n is 10^9?"）

```
常見轉換：
  n ≤ 10^4  → O(n^2) 可以
  n ≤ 10^5  → O(n log n) 或 O(n)
  n ≤ 10^9  → O(log n) 或 O(1)，通常需要數學公式
  n ≤ 10^18 → O(log n) 用 Binary Search / 快速冪
```

### 模式 9: "What's the space complexity? Can you reduce it?"

```
常見優化：
  → 2D DP 表格 → 只保留上一行（滾動陣列）
  → HashMap → 排序 + Two Pointers
  → DFS 遞迴 → Iterative + 自維護 Stack
  → 開新 array → In-place 修改
```

### 模式 10: "Write tests for your code"

```
你應該列出的 Test Cases：
  1. Normal case（題目給的 example）
  2. Edge case: empty input
  3. Edge case: single element
  4. Edge case: all same elements
  5. Edge case: negative numbers / zeros
  6. Large input（描述即可，不用真的跑）
  7. Boundary: 答案在第一個/最後一個位置

表達方式：
  "Let me trace through my code with this test case:
   input = [2,7,11,15], target = 9
   Step 1: check 2, complement 7, not in map, add {2:0}
   Step 2: check 7, complement 2, found in map at index 0
   Return [0, 1]. Correct."
```

---

# Part B: NVIDIA 面試深度解析

---

## 第四章：NVIDIA 面試格式

### 4.1 面試流程

```
階段 1: Recruiter Screen（20-30 min）
└── 背景確認、職位匹配

階段 2: Phone Screen（45-60 min）
├── 1-2 題 Coding
├── 可能包含 C/C++ 相關問題（視職位而定）
└── 可能問基本的 OS / Memory 概念

階段 3: Onsite（4-6 rounds）
├── Round 1-2: Coding/Algorithm
├── Round 3: System Design / Architecture
├── Round 4: Domain Knowledge（GPU, CUDA, Parallel Computing）
├── Round 5: Behavioral
└── Round 6: Hiring Manager（部分職位）
```

### 4.2 NVIDIA vs Google 的關鍵差異

| 面向 | Google | NVIDIA |
|------|--------|--------|
| 算法難度 | Medium-Hard 為主 | Medium 為主，偶爾 Hard |
| Domain Knowledge | 不考 | 可能考 GPU/CUDA 基礎 |
| 語言偏好 | Python/Java/C++ 皆可 | C/C++ 略有加分 |
| Bit Manipulation | 偶爾考 | 高頻！硬體公司特色 |
| Matrix 操作 | 中等頻率 | 高頻！GPU = 矩陣運算 |
| 平行化思維 | System Design 中提到 | 可能直接問你怎麼 parallelize |
| System Design | 分散式系統為主 | 偏向低層系統設計 |

### 4.3 NVIDIA 重視的特質

```
1. 系統思維（Systems Thinking）
   → 不只會解算法，還要理解 memory access pattern
   → 知道 cache locality 對效能的影響

2. 算法效率意識
   → 不只是對的，還要快
   → 常問 "How would you optimize this for performance?"

3. 平行計算直覺
   → "Which part of this algorithm can be parallelized?"
   → "What are the data dependencies?"

4. 底層理解
   → Bit manipulation 要很熟
   → 理解 integer overflow, floating point precision
```

---

## 第五章：NVIDIA 最愛的題型

---

### 題型 1: Array/Matrix 操作

**頻率**：幾乎必考（GPU 的核心就是矩陣運算）

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 48 | Rotate Image | Medium | 轉置 + 反轉 |
| 54 | Spiral Matrix | Medium | 四邊界收縮 |
| 73 | Set Matrix Zeroes | Medium | 用第一行/列當標記 |
| 240 | Search a 2D Matrix II | Medium | 從右上角開始搜尋 |
| 289 | Game of Life | Medium | In-place 用 bit encoding |
| 59 | Spiral Matrix II | Medium | 生成 spiral |

##### NVIDIA 特有 Follow-up

```
Follow-up: "How would you parallelize this matrix operation?"
→ 回答框架：
  1. 識別 data dependency — 哪些 cell 的計算依賴其他 cell？
  2. 如果每個 cell 獨立 → 可以完美平行（embarrassingly parallel）
  3. 如果有依賴 → 考慮 wavefront parallelism（對角線一起算）
  4. 考慮 memory access pattern — row-major vs column-major
```

---

### 題型 2: Bit Manipulation

**頻率**：NVIDIA 超愛考！比 Google 高得多

| LC# | 題名 | 難度 | 核心技巧 |
|-----|------|------|---------|
| 191 | Number of 1 Bits | Easy | n & (n-1) 消除最低位 1 |
| 338 | Counting Bits | Easy | dp[i] = dp[i >> 1] + (i & 1) |
| 190 | Reverse Bits | Easy | 逐位反轉 |
| 136 | Single Number | Easy | XOR 所有數 |
| 137 | Single Number II | Medium | 逐位統計 mod 3 |
| 260 | Single Number III | Medium | XOR 分組 |
| 371 | Sum of Two Integers | Medium | Carry + XOR 模擬加法 |
| 201 | Bitwise AND of Numbers Range | Medium | 找公共 prefix |

##### NVIDIA 面試中的 Bit 題特色

```
不只是 LeetCode 原題，還可能問：

1. "Implement multiply using only bit operations"
   → Left shift = 乘 2，分解成 2 的冪次加總

2. "Find the two's complement of a number"
   → ~n + 1

3. "Check if a number is a power of 2"
   → n > 0 and n & (n-1) == 0

4. "Count bits set to 1 in all numbers from 0 to n"
   → LC 338 的變形

5. "Swap two numbers without extra variable"
   → a ^= b; b ^= a; a ^= b
```

##### 必背 Bit 操作速查表

```
操作                    | 寫法              | 用途
------------------------|-------------------|---------------------------
取得第 i 位             | (n >> i) & 1      | 檢查特定位
設定第 i 位為 1         | n | (1 << i)      | 開旗標
清除第 i 位             | n & ~(1 << i)     | 關旗標
切換第 i 位             | n ^ (1 << i)      | 翻轉
清除最低位的 1          | n & (n - 1)       | 計算 popcount
取得最低位的 1          | n & (-n)          | Fenwick Tree
判斷是否 2 的冪次       | n & (n - 1) == 0  | 快速判斷
取得全 1 mask (k 位)    | (1 << k) - 1     | 取低 k 位
```

---

### 題型 3: Graph 算法

**頻率**：高頻（GPU 計算圖、task dependency）

| LC# | 題名 | 難度 | 為什麼 NVIDIA 考 |
|-----|------|------|-----------------|
| 207 | Course Schedule | Medium | Task dependency |
| 210 | Course Schedule II | Medium | 需要具體排程順序 |
| 200 | Number of Islands | Medium | 基礎 Graph 能力 |
| 743 | Network Delay Time | Medium | Dijkstra, routing |
| 133 | Clone Graph | Medium | Deep copy 能力 |

---

### 題型 4: Dynamic Programming

**頻率**：高頻

| LC# | 題名 | 難度 | 核心 |
|-----|------|------|------|
| 70 | Climbing Stairs | Easy | DP 入門 |
| 322 | Coin Change | Medium | Unbounded Knapsack |
| 300 | Longest Increasing Subsequence | Medium | O(n log n) 解法加分 |
| 72 | Edit Distance | Medium | 2D DP 經典 |
| 62 | Unique Paths | Medium | Grid DP |

---

### 題型 5: Sorting/Searching

**頻率**：高頻

| LC# | 題名 | 難度 | 核心 |
|-----|------|------|------|
| 215 | Kth Largest Element in Array | Medium | Quick Select O(n) |
| 75 | Sort Colors | Medium | Dutch National Flag |
| 56 | Merge Intervals | Medium | Sort + Merge |
| 33 | Search in Rotated Sorted Array | Medium | Modified Binary Search |
| 347 | Top K Frequent Elements | Medium | Bucket Sort / Heap |

---

### 題型 6: Parallel Thinking 問題

這是 NVIDIA 獨有的面試維度。面試官可能在你解完一題後問：

```
模式 A: "How would you parallelize this?"
  → 識別可以獨立運算的部分
  → 識別需要同步 (synchronization) 的部分
  → 討論 thread 數量、work distribution

模式 B: "What are the data dependencies?"
  → 畫出 dependency graph
  → 找出 critical path
  → 識別可平行的 independent chains

模式 C: "What's the memory access pattern?"
  → Row-major vs Column-major
  → Coalesced memory access（GPU 最愛）
  → Cache line 的影響

範例回答（Merge Sort 平行化）：
  "Merge Sort has a natural divide-and-conquer structure.
   The two recursive halves are independent, so they can
   be processed in parallel. However, the merge step
   requires both halves to be completed, so that's a
   synchronization point. With p processors, we can
   achieve O(n/p * log n) per processor, but the merge
   step is sequential unless we use a parallel merge
   algorithm, which runs in O(log^2 n) with n processors."
```

---

### 題型 7: System Design (NVIDIA 風格)

NVIDIA 的 System Design 跟 Google 不同，偏向底層系統：

```
常見題目：
1. "Design a GPU task scheduler"
2. "Design a memory allocator"
3. "Design a parallel file processing system"
4. "Design a data pipeline for ML training"

你需要討論的面向：
  □ Memory hierarchy (L1/L2 cache, shared memory, global memory)
  □ Thread management (thread pool, work stealing)
  □ Data locality
  □ Synchronization primitives (mutex, semaphore, barrier)
  □ Load balancing
```

---

## 第六章：NVIDIA 特有的面試問題類型

### 類型 1: "How would you optimize this for GPU?"

```
回答框架：
  1. 資料平行性：每個元素的計算是否獨立？
     → YES → 每個 GPU thread 處理一個元素
  2. Memory access：是否 coalesced（連續存取）？
     → 相鄰 thread 存取相鄰記憶體 = 最快
  3. Branch divergence：是否有 if-else 分支？
     → GPU 上所有 thread 在同一 warp 中必須執行同一指令
     → 分支太多 → 效能大降
  4. Shared memory：是否有重複讀取？
     → 是 → 先載入 shared memory，再從那裡讀取
```

### 類型 2: Matrix 相關問題

```
常見問法：
  - "Multiply two large matrices efficiently"
  - "Transpose a matrix in-place"
  - "Rotate a matrix 90 degrees"

加分回答：
  "For GPU matrix multiplication, we would use tiled
   matrix multiplication. Each thread block loads a
   tile of A and B into shared memory, computes the
   partial product, and accumulates the results."
```

### 類型 3: Bit Manipulation 進階

```
NVIDIA 面試中可能出現的 Bit 題：
  1. "Extract bits [i, j] from a number"
     → (n >> i) & ((1 << (j - i + 1)) - 1)

  2. "Find the position of the highest set bit"
     → 持續右移直到為 0，或用 math.log2

  3. "Implement a fast popcount"
     → Divide and conquer bit counting:
       n = n - ((n >> 1) & 0x55555555)
       n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
       n = (n + (n >> 4)) & 0x0F0F0F0F
       return (n * 0x01010101) >> 24
```

---

# Part C: 50 題必刷清單

---

## Google 必刷 30 題

按優先順序排列。**前 15 題是最高優先級，如果時間不夠就只刷這些。**

| 優先 | LC# | 題名 | 難度 | 算法家族 | 為什麼 Google 愛考 | 目標時間 |
|------|-----|------|------|---------|-------------------|---------|
| 1 | 200 | Number of Islands | Med | Graph BFS/DFS | Grid 遍歷基本功 | 10 min |
| 2 | 1 | Two Sum | Easy | HashMap | 面試第一題熱身 | 5 min |
| 3 | 236 | Lowest Common Ancestor | Med | Tree DFS | 經典 Tree 題，follow-up 多 | 12 min |
| 4 | 33 | Search in Rotated Sorted Array | Med | Binary Search | 變形 BS 最經典 | 12 min |
| 5 | 3 | Longest Substring Without Repeating | Med | Sliding Window | Window 基本功 | 10 min |
| 6 | 207 | Course Schedule | Med | TopSort | 依賴關係問題 | 12 min |
| 7 | 124 | Binary Tree Maximum Path Sum | Hard | Tree DFS | 雙軌回傳模式 | 18 min |
| 8 | 146 | LRU Cache | Med | Design | 資料結構設計能力 | 20 min |
| 9 | 560 | Subarray Sum Equals K | Med | Prefix Sum + HashMap | 前綴和技巧 | 12 min |
| 10 | 76 | Minimum Window Substring | Hard | Sliding Window | Window 最難題之一 | 18 min |
| 11 | 875 | Koko Eating Bananas | Med | BS on Answer | Google 最愛的 BS 包裝 | 15 min |
| 12 | 994 | Rotting Oranges | Med | Multi-source BFS | BFS 變形 | 12 min |
| 13 | 127 | Word Ladder | Hard | BFS | 字串搜尋 | 18 min |
| 14 | 297 | Serialize and Deserialize BT | Hard | Tree DFS | 序列化能力 | 20 min |
| 15 | 84 | Largest Rectangle in Histogram | Hard | Monotonic Stack | Stack 經典 | 18 min |
| 16 | 543 | Diameter of Binary Tree | Easy | Tree DFS | 簡單但考點深 | 8 min |
| 17 | 98 | Validate BST | Med | Tree DFS | BST 性質 | 10 min |
| 18 | 417 | Pacific Atlantic Water Flow | Med | Graph DFS | 反向搜尋思維 | 15 min |
| 19 | 322 | Coin Change | Med | DP | DP 基本功 | 12 min |
| 20 | 72 | Edit Distance | Med | DP 2D | DP 進階 | 15 min |
| 21 | 23 | Merge K Sorted Lists | Hard | Heap | Heap 應用 | 15 min |
| 22 | 295 | Find Median from Data Stream | Hard | Two Heaps | 動態中位數 | 15 min |
| 23 | 208 | Implement Trie | Med | Trie | 基本實作 | 12 min |
| 24 | 79 | Word Search | Med | Backtracking | 回溯基本功 | 15 min |
| 25 | 128 | Longest Consecutive Sequence | Med | HashSet | O(n) 思維 | 10 min |
| 26 | 739 | Daily Temperatures | Med | Monotonic Stack | Stack 應用 | 10 min |
| 27 | 743 | Network Delay Time | Med | Dijkstra | 最短路徑 | 15 min |
| 28 | 380 | Insert Delete GetRandom O(1) | Med | Design | 資料結構設計 | 15 min |
| 29 | 22 | Generate Parentheses | Med | Backtracking | 產生合法序列 | 12 min |
| 30 | 4 | Median of Two Sorted Arrays | Hard | Binary Search | 面試硬題代表 | 25 min |

### Google 30 題的算法分布

```
Graph BFS/DFS:    4 題 (200, 994, 127, 417)
Tree DFS:         5 題 (236, 124, 543, 98, 297)
Binary Search:    3 題 (33, 875, 4)
HashMap/Set:      3 題 (1, 560, 128)
Sliding Window:   2 題 (3, 76)
TopSort:          1 題 (207)
DP:               2 題 (322, 72)
Monotonic Stack:  2 題 (84, 739)
Heap:             2 題 (23, 295)
Backtracking:     2 題 (79, 22)
Trie:             1 題 (208)
Dijkstra:         1 題 (743)
Design:           2 題 (146, 380)
```

---

## NVIDIA 必刷 20 題

| 優先 | LC# | 題名 | 難度 | 算法家族 | 為什麼 NVIDIA 考 | 目標時間 |
|------|-----|------|------|---------|-----------------|---------|
| 1 | 48 | Rotate Image | Med | Matrix | 矩陣操作基本功 | 10 min |
| 2 | 136 | Single Number | Easy | Bit | XOR 經典 | 3 min |
| 3 | 200 | Number of Islands | Med | Graph | 基礎 Graph | 10 min |
| 4 | 191 | Number of 1 Bits | Easy | Bit | n & (n-1) 技巧 | 5 min |
| 5 | 207 | Course Schedule | Med | TopSort | Task dependency | 12 min |
| 6 | 56 | Merge Intervals | Med | Sort | Scheduling 相關 | 10 min |
| 7 | 75 | Sort Colors | Med | Sort | Dutch Flag, O(1) space | 10 min |
| 8 | 371 | Sum of Two Integers | Med | Bit | 用 bit 模擬加法 | 12 min |
| 9 | 215 | Kth Largest Element | Med | Quick Select | O(n) 平均 | 12 min |
| 10 | 54 | Spiral Matrix | Med | Matrix | 矩陣遍歷 | 12 min |
| 11 | 338 | Counting Bits | Easy | Bit/DP | Bit + DP 結合 | 8 min |
| 12 | 73 | Set Matrix Zeroes | Med | Matrix | In-place 技巧 | 12 min |
| 13 | 190 | Reverse Bits | Easy | Bit | 逐位操作 | 8 min |
| 14 | 322 | Coin Change | Med | DP | DP 基本功 | 12 min |
| 15 | 300 | Longest Increasing Subsequence | Med | DP | O(n log n) 加分 | 15 min |
| 16 | 141 | Linked List Cycle | Easy | Linked List | 快慢指標 | 5 min |
| 17 | 240 | Search a 2D Matrix II | Med | Matrix/Search | 矩陣搜尋 | 10 min |
| 18 | 289 | Game of Life | Med | Matrix | In-place bit encoding | 15 min |
| 19 | 260 | Single Number III | Med | Bit | XOR 分組技巧 | 12 min |
| 20 | 62 | Unique Paths | Med | DP | Grid DP | 8 min |

### NVIDIA 20 題的算法分布

```
Bit Manipulation:  6 題 (136, 191, 371, 338, 190, 260)
Matrix:            5 題 (48, 54, 73, 240, 289)
Graph/TopSort:     2 題 (200, 207)
DP:                3 題 (322, 300, 62)
Sorting/Selection: 3 題 (56, 75, 215)
Linked List:       1 題 (141)
```

### 兩家重疊題（刷一次抵兩家）

```
LC 200 Number of Islands    — Google ★★★★★ / NVIDIA ★★★★
LC 207 Course Schedule       — Google ★★★★  / NVIDIA ★★★★
LC 322 Coin Change           — Google ★★★★  / NVIDIA ★★★★
LC 56  Merge Intervals       — Google ★★★   / NVIDIA ★★★★
LC 33  Search in Rotated     — Google ★★★★★ / NVIDIA ★★★
```

---

# Part D: 面試前一天的終極複習清單

---

## 30 分鐘：算法模板速覽

逐一掃過以下 12 個模板，確認你能「不查資料直接寫出來」：

### 模板 1: BFS on Grid (3 min)

```python
from collections import deque
def bfs(grid, sr, sc):
    rows, cols = len(grid), len(grid[0])
    visited = {(sr, sc)}
    queue = deque([(sr, sc)])
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and grid[nr][nc]==1:
                visited.add((nr,nc))
                queue.append((nr,nc))
```

### 模板 2: DFS on Grid (2 min)

```python
def dfs(grid, r, c, visited):
    if r<0 or r>=len(grid) or c<0 or c>=len(grid[0]) or (r,c) in visited or grid[r][c]==0:
        return
    visited.add((r,c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r+dr, c+dc, visited)
```

### 模板 3: Tree DFS with Global Tracking (2 min)

```python
def solve(root):
    result = [float('-inf')]
    def dfs(node):
        if not node: return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        result[0] = max(result[0], left + node.val + right)
        return node.val + max(left, right)
    dfs(root)
    return result[0]
```

### 模板 4: Binary Search (2 min)

```python
def binary_search(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 模板 5: Sliding Window (2 min)

```python
def sliding_window(s):
    window = {}
    left = result = 0
    for right in range(len(s)):
        window[s[right]] = window.get(s[right], 0) + 1
        while invalid(window):
            window[s[left]] -= 1
            if window[s[left]] == 0: del window[s[left]]
            left += 1
        result = max(result, right - left + 1)
    return result
```

### 模板 6: TopSort - Kahn's Algorithm (3 min)

```python
from collections import deque, defaultdict
def topo_sort(n, edges):
    graph = defaultdict(list)
    in_deg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        in_deg[v] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            in_deg[nei] -= 1
            if in_deg[nei] == 0: q.append(nei)
    return order if len(order) == n else []
```

### 模板 7: Union-Find (3 min)

```python
class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

### 模板 8: Backtracking (3 min)

```python
def backtrack(candidates, target, start, path, result):
    if target == 0:
        result.append(path[:])
        return
    for i in range(start, len(candidates)):
        if candidates[i] > target: break
        if i > start and candidates[i] == candidates[i-1]: continue  # 去重
        path.append(candidates[i])
        backtrack(candidates, target - candidates[i], i + 1, path, result)
        path.pop()
```

### 模板 9: Dijkstra (3 min)

```python
import heapq
from collections import defaultdict
def dijkstra(n, edges, src):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

### 模板 10: Monotonic Stack (2 min)

```python
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # 存 index
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result
```

### 模板 11: Two Heaps for Median (3 min)

```python
import heapq
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap
    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

### 模板 12: Trie (3 min)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children: return False
            node = node.children[ch]
        return node.is_end
```

---

## 15 分鐘：Edge Case 清單總覽

面試寫完 code 後，主動對面試官說："Let me think about edge cases." 然後逐一檢查：

### 通用 Edge Cases（適用所有題型）

```
□ 空輸入          → [], "", None, 0
□ 單一元素        → [1], "a", tree with one node
□ 兩個元素        → [1,2] — 特別是 Two Pointers 類題
□ 全部相同        → [5,5,5,5,5]
□ 負數            → [-1, -2, -3]
□ 零              → [0, 0, 0] 或包含 0
□ 最大/最小值     → 2^31 - 1, -2^31
□ 已排序          → 升序/降序
□ 有重複          → [1,1,2,2,3,3]
```

### 各題型特有 Edge Cases

```
Binary Search:
  □ target 不存在
  □ target 在第一個/最後一個位置
  □ 只有一個元素且等於/不等於 target

Tree:
  □ 空 tree (root = None)
  □ 只有左子樹 / 只有右子樹（skewed tree）
  □ 完美平衡 tree

Graph:
  □ Disconnected graph（多個 component）
  □ 單一節點，無邊
  □ 有自環 (self-loop)
  □ 有環 (cycle)

Sliding Window:
  □ 窗口大小 > 陣列長度
  □ 所有字元都相同
  □ 答案是整個陣列

DP:
  □ n = 0, n = 1
  □ 所有值為 0
  □ 所有值為負數
```

---

## 15 分鐘：面試溝通模板

### 開場 (Clarifying Questions)

```
聽完題目後，先問：

1. "Just to make sure I understand correctly — [重述題目]?"
2. "What's the expected size of the input? Can n be up to 10^5?"
3. "Can there be duplicates in the array?"
4. "Is the input sorted?"
5. "Should I return the indices or the values?"
6. "Can the input be empty or null?"
7. "Are there negative numbers?"
```

### 思路說明

```
"Let me think about this for a moment."
（停 15-30 秒，組織思路，這是完全可以的）

"My first thought is a brute force approach:
 [描述暴力解]. This would be O(n^2) time.

 To optimize, I notice that [觀察].
 So I can use [算法/資料結構], which gives us
 O(n log n) / O(n) time and O(n) / O(1) space.

 Does this approach sound reasonable before I start coding?"
```

### 寫 Code 時

```
邊寫邊說：
  "First, I'll initialize my variables..."
  "Now I'm iterating through the array..."
  "This condition handles the case where..."
  "Let me use a descriptive variable name here..."

卡住時：
  "Let me step back and think about this part..."
  "I think there might be an off-by-one issue here,
   let me trace through a small example..."
```

### Dry Run

```
"Let me trace through an example:
 input = [2, 7, 11, 15], target = 9

 Iteration 1: num = 2, complement = 7
   → 7 not in hashmap → add 2:0 to map
 Iteration 2: num = 7, complement = 2
   → 2 is in hashmap at index 0!
   → return [0, 1]

 This matches the expected output."
```

### 被問 "Can you do better?" 時

```
"Let me think about what's causing the bottleneck...

 [情境 A：可以優化]
 The current O(n^2) comes from the nested loop.
 If I sort the array first, I can use two pointers,
 bringing it down to O(n log n).

 [情境 B：已經最優]
 I believe O(n) is optimal here because we need to
 examine every element at least once. The space is O(1)
 which is also optimal."
```

### 結束時問面試官的問題

```
好問題（展示你有想法）：
1. "What's the most interesting technical challenge
    your team has worked on recently?"
2. "How does the team approach code reviews and
    testing at scale?"
3. "What does the onboarding process look like?"

避免的問題：
  ✕ 薪水相關（等 offer 再談）
  ✕ "Did I do well?"（面試官不能回答）
  ✕ 可以 Google 到答案的問題
```

---

## 面試當天 Morning Checklist

```
□ 提前 15 分鐘上線/到場
□ 準備好 IDE / Google Docs（確認打字順暢）
□ 準備一杯水
□ 深呼吸三次

□ 心態設定：
  - 面試官是你的合作者，不是敵人
  - 他們希望你成功（hiring 比 rejecting 更好）
  - 卡住是正常的，展示你的 problem-solving process
  - 不要沉默超過 60 秒，說出你在想什麼

□ 時間管理：
  - 前 5 分鐘：讀題 + 問問題
  - 5-10 分鐘：說思路
  - 10-35 分鐘：寫 code
  - 35-40 分鐘：Dry run + edge case
  - 最後 5 分鐘：問問題
```

---

## 附錄：複雜度速查表（考前最後一眼）

| 算法 | Time | Space | 何時用 |
|------|------|-------|--------|
| Binary Search | O(log n) | O(1) | Sorted array, search on answer |
| Two Pointers | O(n) | O(1) | Sorted array, pair finding |
| Sliding Window | O(n) | O(k) | Contiguous subarray/substring |
| HashMap lookup | O(1) avg | O(n) | Fast lookup, counting |
| BFS | O(V+E) | O(V) | Shortest path (unweighted), level order |
| DFS | O(V+E) | O(V) | Path finding, connected components |
| TopSort | O(V+E) | O(V) | DAG ordering, dependency |
| Union-Find | O(alpha(n)) | O(n) | Dynamic connectivity |
| Dijkstra | O(E log V) | O(V) | Weighted shortest path (non-negative) |
| DP | varies | varies | Optimal substructure + overlapping subproblems |
| Backtracking | O(k^n) | O(n) | Generate all valid combinations |
| Merge Sort | O(n log n) | O(n) | Stable sort, merge k lists |
| Quick Select | O(n) avg | O(1) | Kth element |
| Monotonic Stack | O(n) | O(n) | Next greater/smaller element |
| Trie | O(L) | O(AL) | Prefix search (L=word length, A=alphabet) |
| Heap ops | O(log n) | O(n) | Top K, dynamic median |

---

> **最後提醒**：這份清單不是讓你「背答案」，而是讓你在面試中有 pattern 可以快速調用。真正的功夫在於每一題都自己從零寫過、debug 過、trace 過。刷題時每題至少寫兩遍：第一遍理解，第二遍限時。祝你拿到 offer！
