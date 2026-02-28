# 從 Easy 到 Hard 的進化路線：演算法 Pattern 進化地圖

> **適用對象**：已讀完基礎教學（01-18），想理解 Hard 題為何不可怕的人
> **核心觀念**：每一道 Hard 題都是某個 Easy 題加了 1-2 個 twist 的結果
> **語言**：繁體中文解說 + English technical terms

---

## 目錄

1. [核心哲學：Hard = Easy + Twists](#核心哲學hard--easy--twists)
2. [Pattern 1: Two Sum 進化鏈](#pattern-1-two-sum-進化鏈)
3. [Pattern 2: Binary Search 進化鏈](#pattern-2-binary-search-進化鏈)
4. [Pattern 3: Sliding Window 進化鏈](#pattern-3-sliding-window-進化鏈)
5. [Pattern 4: DFS on Tree 進化鏈](#pattern-4-dfs-on-tree-進化鏈)
6. [Pattern 5: BFS 進化鏈](#pattern-5-bfs-進化鏈)
7. [Pattern 6: Graph 進化鏈](#pattern-6-graph-進化鏈)
8. [Pattern 7: DP 進化鏈](#pattern-7-dp-進化鏈)
9. [Pattern 8: Backtracking 進化鏈](#pattern-8-backtracking-進化鏈)
10. [Pattern 9: Stack 進化鏈](#pattern-9-stack-進化鏈)
11. [Pattern 10: Heap 進化鏈](#pattern-10-heap-進化鏈)
12. [Pattern 11: Union-Find 進化鏈](#pattern-11-union-find-進化鏈)
13. [Pattern 12: Trie 進化鏈](#pattern-12-trie-進化鏈)
14. [Pattern 13: Bit Manipulation 進化鏈](#pattern-13-bit-manipulation-進化鏈)
15. [Pattern 14: Greedy 進化鏈](#pattern-14-greedy-進化鏈)
16. [Pattern 15: Prefix Sum 進化鏈](#pattern-15-prefix-sum-進化鏈)
17. [進化地圖總覽](#進化地圖總覽)
18. [面試實戰：如何拆解未知的 Hard 題](#面試實戰如何拆解未知的-hard-題)

---

## 核心哲學：Hard = Easy + Twists

### 一個關鍵的心理突破

大多數人看到 Hard 題會想：「這是一種全新的、我沒見過的演算法。」

**錯。**

真相是：

```
Hard 題 = 你已經會的 Easy/Medium 題 + 1~2 個額外的 twist

其中 twist 通常是以下幾種：
  1. 多一個維度（1D → 2D、一個變數 → 兩個變數）
  2. 搜尋空間變抽象（在 array 裡找值 → 在「答案」上找值）
  3. 資料結構不直接給你（需要自己建圖、建 histogram）
  4. 組合兩個已知 pattern（Monotonic Stack + DP、BFS + Binary Search）
  5. Edge case 爆炸多（需要處理大量邊界情況）
```

### 進化的規律

每個 pattern 的進化幾乎都遵循同樣的路徑：

```
Stage 1: 裸算法     — 最基本的形式，沒有任何變化
  ↓
Stage 2: 加條件     — 輸入有特殊性質（sorted、unique、bounded）
  ↓
Stage 3: 加維度     — 問題從 1D 變 2D，或需要追蹤更多狀態
  ↓
Stage 4: 加組合     — 需要結合另一個 pattern 才能解
  ↓
Stage 5: 抽象化     — 搜尋空間、圖的結構不再明確給你，需要自己建模
```

### 你的解題策略

面對一道沒見過的題目，問自己三個問題：

```
Q1: 「這題的 BASE PATTERN 是什麼？」
    → 它本質上是 Two Pointers？BFS？DP？

Q2: 「加了什麼 TWIST？」
    → 排序了？二維了？需要去重？需要建圖？

Q3: 「我會不會沒有 twist 的版本？」
    → 如果會，那你只需要搞定 twist 的部分
```

---

## Pattern 1: Two Sum 進化鏈

### 進化路線圖

```
LC #1 Two Sum (Easy)
  │  BASE: HashMap 存 complement
  │
  │  ＋ 輸入已排序
  ▼
LC #167 Two Sum II (Medium)
  │  TWIST: 排序 → 可以用 Two Pointers 代替 HashMap
  │
  │  ＋ 多一個數
  ▼
LC #15 3Sum (Medium)
  │  TWIST: 固定一個數 → 內層變 Two Sum II
  │         ＋ 去重（跳過重複元素）
  │
  │  ＋ 再多一個數
  ▼
LC #18 4Sum (Medium)
  │  TWIST: 固定兩個數 → 內層還是 Two Sum II
  │         ＋ 更複雜的去重
  │
  │  ＋ 目標不是固定值而是最接近
  ▼
LC #16 3Sum Closest (Medium)
     TWIST: 沒有精確解 → 追蹤全域 min diff
```

### 每一層加了什麼

| Level | 題目 | 新增的複雜度 | 核心 Insight |
|-------|------|-------------|-------------|
| 1 | Two Sum | 無 | `complement = target - nums[i]`，存進 HashMap |
| 2 | Two Sum II | 已排序 | 排序 → Two Pointers 可以 O(1) space |
| 3 | 3Sum | 多一個數 + 去重 | 外層 for loop 固定一個，內層 Two Pointers |
| 4 | 4Sum | 再多一個 + 去重 | 兩層 for loop 固定兩個，內層 Two Pointers |

### 程式碼對比：看進化如何發生

```python
# === Level 1: Two Sum (HashMap) ===
def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i

# === Level 2: Two Sum II (Two Pointers，因為 sorted) ===
def twoSumII(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:   return [left + 1, right + 1]
        elif s < target:  left += 1
        else:             right -= 1

# === Level 3: 3Sum = 固定一個 + Two Sum II + 去重 ===
def threeSum(nums):
    nums.sort()                          # ← 新增：先排序
    result = []
    for i in range(len(nums) - 2):       # ← 新增：外層固定一個
        if i > 0 and nums[i] == nums[i-1]:
            continue                      # ← 新增：去重
        # 內層就是 Two Sum II
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:
                    left += 1             # ← 新增：內層去重
                while left < right and nums[right] == nums[right-1]:
                    right -= 1            # ← 新增：內層去重
                left += 1; right -= 1
            elif s < 0: left += 1
            else:        right -= 1
    return result
```

### 辨識技巧

> 看到「找 N 個數的組合使得 sum = target」→ 先想 Two Sum，然後用 N-2 層迴圈降維。

---

## Pattern 2: Binary Search 進化鏈

### 進化路線圖

```
LC #704 Binary Search (Easy)
  │  BASE: sorted array, 找到就回傳
  │
  │  ＋ 不是找精確值，而是找邊界
  ▼
LC #34 First & Last Position (Medium)
  │  TWIST: 左邊界 + 右邊界，兩次 Binary Search
  │
  │  ＋ 陣列被旋轉過
  ▼
LC #33 Search in Rotated Sorted Array (Medium)
  │  TWIST: 判斷哪半邊是有序的，然後決定搜哪邊
  │
  │  ＋ 有重複元素
  ▼
LC #81 Search in Rotated Array II (Medium)
  │  TWIST: nums[left] == nums[mid] 時無法判斷 → worst case O(n)
  │
  │  ＋ 搜尋空間是「答案」而不是 array
  ▼
LC #410 Split Array Largest Sum (Hard)
     TWIST: Binary Search on Answer
            + Greedy check function 驗證 mid 是否可行
```

### 進化要素分析

```
找值 → 找邊界 → 非標準陣列 → 抽象搜尋空間

每一步的 "aha!" insight：
  Level 1: mid == target 就回傳
  Level 2: 即使找到了也不停，繼續壓縮邊界
  Level 3: 先判斷 [left, mid] 和 [mid, right] 哪段有序
  Level 4: 搜尋的不是 array index，而是「答案的可能值」
```

### 最關鍵的進化：Binary Search on Answer

```python
# === Level 1: 標準 Binary Search ===
# 搜尋空間 = array 的 index
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# === Level 4: Binary Search on Answer ===
# 搜尋空間 = 答案的可能範圍 [max(nums), sum(nums)]
# LC #410 Split Array Largest Sum
def splitArray(nums, k):
    def can_split(max_sum):
        """能不能在每段 sum <= max_sum 的情況下分成 <= k 段？"""
        count, curr = 1, 0
        for n in nums:
            if curr + n > max_sum:
                count += 1
                curr = n
            else:
                curr += n
        return count <= k

    lo, hi = max(nums), sum(nums)  # ← 搜尋空間是答案範圍！
    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(mid):         # ← Greedy check
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 辨識技巧

> 看到「最小化最大值」或「最大化最小值」→ 幾乎一定是 Binary Search on Answer。
> 關鍵問句：「如果答案是 X，我能不能用 Greedy 驗證可不可行？」如果可以 → 用 Binary Search on Answer。

---

## Pattern 3: Sliding Window 進化鏈

### 進化路線圖

```
LC #643 Max Average Subarray I (Easy)
  │  BASE: 固定大小的窗口，滑動求最大平均
  │
  │  ＋ 窗口大小不固定
  ▼
LC #3 Longest Substring Without Repeating (Medium)
  │  TWIST: 窗口收縮條件 = 遇到重複字元
  │         用 HashSet 追蹤窗口內的字元
  │
  │  ＋ 不只是去重，而是要匹配一個字元集合
  ▼
LC #567 Permutation in String (Medium)
  │  TWIST: 用 HashMap 計數，窗口大小 = pattern 長度
  │         比對兩個 HashMap 是否相等
  │
  │  ＋ 找最短的包含所有目標字元的子字串
  ▼
LC #76 Minimum Window Substring (Hard)
     TWIST: 可變窗口 + HashMap 計數
            + formed/required 追蹤（幾個字元已滿足）
            + 先擴張到合法，再收縮找最短
```

### 進化要素分析

```
固定窗口 → 可變窗口 → 可變窗口 + 簡單條件 → 可變窗口 + 複雜計數
                ↑                                    ↑
           收縮條件很簡單                         收縮條件需要多個計數器
           （有重複就縮）                         （所有字元都滿足才合法）
```

### 程式碼對比

```python
# === Level 1: 固定窗口 ===
def maxAverage(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # 進一個出一個
        max_sum = max(max_sum, window_sum)
    return max_sum / k

# === Level 2: 可變窗口 + HashSet ===
def lengthOfLongestSubstring(s):
    seen = set()
    left = max_len = 0
    for right in range(len(s)):
        while s[right] in seen:        # 收縮條件：有重複
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len

# === Level 3 (Hard): 可變窗口 + 複雜計數 ===
# LC #76 Minimum Window Substring
def minWindow(s, t):
    from collections import Counter
    need = Counter(t)             # 需要的字元計數
    missing = len(t)              # 還缺幾個字元
    left = 0
    best = (0, float('inf'))      # (start, end)

    for right, char in enumerate(s):
        if need[char] > 0:        # 這個字元是我們需要的
            missing -= 1
        need[char] -= 1

        while missing == 0:       # 所有字元都湊齊了 → 嘗試收縮
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[s[left]] += 1
            if need[s[left]] > 0: # 收縮後又缺一個了
                missing += 1
            left += 1

    return "" if best[1] == float('inf') else s[best[0]:best[1]+1]
```

### 辨識技巧

> 看到「連續子陣列/子字串」+ 「最長/最短」→ Sliding Window。
> 如果窗口大小固定 → Level 1 模板；如果大小可變 → 關鍵在於「什麼條件下收縮」。

---

## Pattern 4: DFS on Tree 進化鏈

### 進化路線圖

```
LC #104 Maximum Depth (Easy)
  │  BASE: return 1 + max(left, right)
  │
  │  ＋ 需要全域追蹤（不只是回傳值）
  ▼
LC #543 Diameter of Binary Tree (Medium)
  │  TWIST: 每個節點算 left_depth + right_depth
  │         用全域變數追蹤歷史最大
  │
  │  ＋ 不是深度而是 sum，且路徑可不經過 root
  ▼
LC #124 Binary Tree Maximum Path Sum (Hard)
  │  TWIST: 對每個節點：
  │         - 回傳值 = node.val + max(left, right, 0)（單邊延伸）
  │         - 全域更新 = node.val + max(left,0) + max(right,0)（穿越）
  │         需要區分「回傳給父節點的值」vs「全域答案的候選」
  │
  │  ＋ 路徑和要等於某個 target
  ▼
LC #437 Path Sum III (Medium)
     TWIST: 用 Prefix Sum + HashMap 在 DFS 中追蹤路徑和
```

### 關鍵進化：「回傳值」vs「全域答案」的分離

```
Level 1 (Max Depth):
    回傳值 = 答案，直接 return

Level 2 (Diameter):
    回傳值 ≠ 答案
    回傳值 = 「我這邊最長的單邊深度」（給父節點用）
    答案 = 「經過我的最長路徑 = left + right」（全域追蹤 max）

Level 3 (Max Path Sum):
    同 Level 2 的結構，但：
    - 值可以是負數 → 要 max(child, 0)
    - 路徑可以只有自己 → node.val 本身就是候選答案
```

### 程式碼對比

```python
# === Level 1: Maximum Depth ===
def maxDepth(root):
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# === Level 2: Diameter ===
def diameterOfBinaryTree(root):
    max_diameter = 0
    def depth(node):
        nonlocal max_diameter
        if not node: return 0
        left = depth(node.left)
        right = depth(node.right)
        max_diameter = max(max_diameter, left + right)  # ← 全域追蹤
        return 1 + max(left, right)                     # ← 回傳單邊
    depth(root)
    return max_diameter

# === Level 3: Maximum Path Sum (Hard) ===
def maxPathSum(root):
    max_sum = float('-inf')
    def gain(node):
        nonlocal max_sum
        if not node: return 0
        left = max(gain(node.left), 0)    # ← 負數就不要
        right = max(gain(node.right), 0)  # ← 負數就不要
        # 穿越路徑（左 → 我 → 右）→ 更新全域答案
        max_sum = max(max_sum, node.val + left + right)
        # 回傳給父節點：只能選一邊
        return node.val + max(left, right)
    gain(root)
    return max_sum
```

### 辨識技巧

> 如果遞迴的回傳值直接就是答案 → Level 1。
> 如果回傳值是「給父節點的資訊」，答案需要另外追蹤 → Level 2/3。
> 關鍵問句：「在這個節點，答案的形狀長什麼樣？可以往兩邊伸展嗎？」

---

## Pattern 5: BFS 進化鏈

### 進化路線圖

```
LC #102 Level Order Traversal (Medium)
  │  BASE: Queue + 逐層處理
  │
  │  ＋ 在 grid 上做 BFS
  ▼
LC #200 Number of Islands (Medium)
  │  TWIST: 4 方向擴展 + visited 標記
  │         每次發現新島 → BFS 把整座島標記完
  │
  │  ＋ 多個起點同時出發
  ▼
LC #994 Rotting Oranges (Medium)
  │  TWIST: Multi-source BFS — 所有起點同時入 queue
  │         level = 經過的分鐘數
  │
  │  ＋ 圖不是直接給你，需要自己建
  ▼
LC #127 Word Ladder (Hard)
  │  TWIST: 隱式圖（implicit graph）
  │         每個 word 是一個 node
  │         差一個字母的 word 之間有 edge
  │         BFS 找最短轉換路徑
  │
  │  ＋ 同時從兩端搜尋
  ▼
LC #126 Word Ladder II (Hard)
     TWIST: Bidirectional BFS + 記錄所有最短路徑
            需要 BFS 建層 + DFS 回溯找路徑
```

### 進化要素分析

```
樹上 BFS → Grid BFS → Multi-source BFS → Implicit Graph BFS → Bidirectional BFS

每一步新增的 twist：
  Level 1: 直接給你樹結構，queue 跑一跑就好
  Level 2: 在 grid 上，要處理 4 方向 + 邊界 + visited
  Level 3: 不是一個起點，是一堆起點同時開始
  Level 4: graph 不是直接給你的，需要自己建（或用 pattern matching 生成 neighbors）
  Level 5: 從兩端同時搜尋 + 記錄所有路徑
```

### 程式碼對比

```python
from collections import deque

# === Level 1: Level Order Traversal ===
def levelOrder(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):  # ← 一次處理一整層
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# === Level 2: Number of Islands (Grid BFS) ===
def numIslands(grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                count += 1
                queue = deque([(i, j)])
                grid[i][j] = '0'           # ← visited 標記
                while queue:
                    r, c = queue.popleft()
                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:  # ← 4 方向
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) \
                           and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
    return count

# === Level 3: Rotting Oranges (Multi-source BFS) ===
def orangesRotting(grid):
    queue = deque()
    fresh = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 2:
                queue.append((i, j, 0))    # ← 所有腐爛橘子同時入 queue
            elif grid[i][j] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) \
               and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                queue.append((nr, nc, t + 1))
    return minutes if fresh == 0 else -1
```

### 辨識技巧

> 看到「最短距離」→ BFS。看到「所有點同時擴散」→ Multi-source BFS。
> 看到「從 A 轉換成 B，每次改一點」→ Implicit Graph BFS。

---

## Pattern 6: Graph 進化鏈

### 進化路線圖

```
LC #207 Course Schedule (Medium)
  │  BASE: 偵測有向圖是否有環 → Topological Sort (Kahn's)
  │
  │  ＋ 要回傳一個合法的順序
  ▼
LC #210 Course Schedule II (Medium)
  │  TWIST: 同樣的 TopSort，但要記錄 pop 出來的順序
  │
  │  ＋ 圖不是直接給你的，需要從字串推導
  ▼
LC #269 Alien Dictionary (Hard)
  │  TWIST: 1. 從排序好的字串 list 推導字母順序 → 建圖
  │         2. 比較相鄰字串找邊
  │         3. Edge case: "abc" before "ab" → 非法
  │         4. TopSort 得到字母順序
  │
  │  ＋ 圖有權重 + 找最短路
  ▼
LC #743 Network Delay Time (Medium)
  │  TWIST: Weighted Graph + Dijkstra
  │
  │  ＋ 有步數限制
  ▼
LC #787 Cheapest Flights Within K Stops (Medium)
     TWIST: Dijkstra/BFS + 限制最多 K 次中轉
            需要修改鬆弛條件
```

### 進化要素分析

```
給你圖 + 偵測環
  → 給你圖 + 求順序
    → 不給圖 + 自己建圖 + 求順序
      → 給你帶權圖 + 求最短路
        → 帶權圖 + 額外限制條件

建圖能力是 Hard Graph 題的分水嶺。
Easy/Medium: 題目直接給你 edge list
Hard: 題目給你一堆字串/狀態，你要自己推導出 graph 結構
```

### 關鍵程式碼：Alien Dictionary（建圖 + TopSort）

```python
# LC #269 Alien Dictionary (Hard)
def alienOrder(words):
    from collections import defaultdict, deque

    # Step 1: 找出所有出現過的字母
    chars = set(c for w in words for c in w)
    in_degree = {c: 0 for c in chars}
    graph = defaultdict(set)

    # Step 2: 比較相鄰字串，推導出邊 ← 這是 Hard 的核心 twist
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        # Edge case: "abc" before "ab" is invalid
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break  # 只看第一個不同的字元

    # Step 3: 標準 TopSort (Kahn's) ← 這部分跟 Course Schedule 一模一樣
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for nei in graph[c]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                queue.append(nei)

    return "".join(result) if len(result) == len(chars) else ""
```

### 辨識技巧

> 看到「依賴關係」「先後順序」→ Topological Sort。
> 看到「最短/最便宜路徑」→ Dijkstra/BFS。
> 關鍵判斷：圖是直接給你的，還是需要自己建？需要建圖 → 難度自動升一級。

---

## Pattern 7: DP 進化鏈

### 進化路線圖

```
LC #70 Climbing Stairs (Easy)
  │  BASE: dp[i] = dp[i-1] + dp[i-2]（Fibonacci 變形）
  │
  │  ＋ 有「選或不選」的決策
  ▼
LC #198 House Robber (Medium)
  │  TWIST: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
  │         不能選相鄰的
  │
  │  ＋ 陣列是環形的
  ▼
LC #213 House Robber II (Medium)
  │  TWIST: 頭尾相連 → 拆成兩個線性問題
  │         max(rob(0..n-2), rob(1..n-1))
  │
  │  ＋ 從一維變二維
  ▼
LC #1143 Longest Common Subsequence (Medium)
  │  TWIST: dp[i][j] = 兩個字串的狀態
  │         match → dp[i-1][j-1]+1
  │         不 match → max(dp[i-1][j], dp[i][j-1])
  │
  │  ＋ 有三種操作可選
  ▼
LC #72 Edit Distance (Medium-Hard)
  │  TWIST: dp[i][j] = min(insert, delete, replace)
  │         三路取 min 而非兩路取 max
  │
  │  ＋ 需要空間優化 + 更複雜的狀態定義
  ▼
LC #312 Burst Balloons (Hard)
     TWIST: 區間 DP — dp[i][j] = range [i,j] 的最優解
            「最後戳哪個氣球」而非「先戳哪個」（逆向思維）
```

### DP 進化的五個階段

```
Stage 1: 一維線性 DP
  狀態: dp[i] = 前 i 個元素的最優解
  例: Climbing Stairs, House Robber

Stage 2: 一維 DP + 變形
  狀態: dp[i] 但有額外約束（環形、多狀態）
  例: House Robber II, Paint House

Stage 3: 二維 DP（兩個序列）
  狀態: dp[i][j] = 第一個序列前 i 個 vs 第二個序列前 j 個
  例: LCS, Edit Distance

Stage 4: 二維 DP（背包）
  狀態: dp[i][j] = 前 i 個物品、容量 j 的最優解
  例: 0/1 Knapsack, Coin Change, Partition Equal Subset Sum

Stage 5: 區間 DP / 高階 DP
  狀態: dp[i][j] = 區間 [i, j] 的最優解
  例: Burst Balloons, Stone Game
```

### 程式碼對比：狀態轉移的進化

```python
# === Stage 1: 一維 DP ===
# Climbing Stairs
dp[i] = dp[i-1] + dp[i-2]

# === Stage 2: 一維 DP + 決策 ===
# House Robber
dp[i] = max(dp[i-1],          # 不搶第 i 家
             dp[i-2] + nums[i]) # 搶第 i 家

# === Stage 3: 二維 DP ===
# LCS
dp[i][j] = dp[i-1][j-1] + 1            if s1[i]==s2[j]
          = max(dp[i-1][j], dp[i][j-1]) otherwise

# === Stage 4: 二維 DP（三路決策）===
# Edit Distance
dp[i][j] = dp[i-1][j-1]                 if s1[i]==s2[j]  (不操作)
          = 1 + min(dp[i-1][j],          # delete
                    dp[i][j-1],          # insert
                    dp[i-1][j-1])        # replace

# === Stage 5: 區間 DP ===
# Burst Balloons
dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])
           for k in range(i+1, j)  # k = 最後戳的氣球
```

### 辨識技巧

> 看到「最優值」「方案數」「是否可行」→ 先想 DP。
> 狀態定義看「需要幾個變數描述子問題」→ 幾個變數就是幾維 DP。
> 轉移方程看「在當前位置有幾種選擇」→ 選擇數 = 轉移的路數。

---

## Pattern 8: Backtracking 進化鏈

### 進化路線圖

```
LC #78 Subsets (Medium)
  │  BASE: 每個元素選或不選，收集所有可能
  │
  │  ＋ 有重複元素
  ▼
LC #90 Subsets II (Medium)
  │  TWIST: 排序 + 同層跳過重複
  │         if i > start and nums[i] == nums[i-1]: continue
  │
  │  ＋ 有目標和的約束
  ▼
LC #39 Combination Sum (Medium)
  │  TWIST: 可以重複使用元素 → 下一層的 start 不 +1
  │         當 remain == 0 → 找到一組解
  │
  │  ＋ 棋盤上的約束
  ▼
LC #51 N-Queens (Hard)
  │  TWIST: 三個約束：行、列、對角線
  │         用 set 追蹤已佔用的列 / 主對角線 / 副對角線
  │
  │  ＋ 更多約束（行+列+九宮格）
  ▼
LC #37 Sudoku Solver (Hard)
     TWIST: 三重約束（行 / 列 / 3x3 box）
            需要找下一個空格 → 嘗試 1-9 → 驗證 → 回溯
            回溯時要撤銷操作
```

### 進化的本質：約束越來越複雜

```
Backtracking 的框架永遠一樣：

def backtrack(path, choices):
    if 達到目標:
        收集 path
        return
    for choice in choices:
        if 不合法: continue     ← 進化的重點在這裡！
        path.add(choice)
        backtrack(path, next_choices)
        path.remove(choice)

Easy → Hard 的差別：
  Easy:   「不合法」= 簡單判斷（已用過）
  Medium: 「不合法」= 一兩個條件（重複、超過 target）
  Hard:   「不合法」= 多重條件交叉檢查（行+列+對角線+九宮格）
```

### 程式碼對比

```python
# === Level 1: Subsets（最基本的 backtracking）===
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])       # 每個狀態都是一個解
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# === Level 2: Subsets II（加去重）===
def subsetsWithDup(nums):
    nums.sort()                      # ← 新增：排序
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue             # ← 新增：同層去重
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result

# === Level 3: N-Queens（棋盤約束）===
def solveNQueens(n):
    result = []
    cols = set()        # ← 新增：追蹤被佔用的列
    diag1 = set()       # ← 新增：追蹤主對角線 (row - col)
    diag2 = set()       # ← 新增：追蹤副對角線 (row + col)

    def backtrack(row, queens):
        if row == n:
            result.append(queens[:])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue  # ← 三重約束檢查
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            queens.append(col)
            backtrack(row + 1, queens)
            queens.pop()
            cols.remove(col)          # ← 撤銷
            diag1.remove(row - col)
            diag2.remove(row + col)
    backtrack(0, [])
    return result
```

### 辨識技巧

> 看到「列出所有可能」「所有組合/排列」→ Backtracking。
> 判斷難度的關鍵：「合法性檢查有多複雜？需要追蹤幾個約束？」

---

## Pattern 9: Stack 進化鏈

### 進化路線圖

```
LC #20 Valid Parentheses (Easy)
  │  BASE: 遇到左括號 push，遇到右括號 pop 並比對
  │
  │  ＋ 不只是配對，而是找「下一個更大的」
  ▼
LC #739 Daily Temperatures (Medium)
  │  TWIST: Monotonic Stack（單調遞減棧）
  │         棧裡存 index，遇到更大的 → pop 並算距離
  │
  │  ＋ 不只是找下一個更大，而是計算面積
  ▼
LC #84 Largest Rectangle in Histogram (Hard)
  │  TWIST: Monotonic Stack + 寬度計算
  │         每個 bar pop 出來時，計算「以它為高度」的最大矩形
  │         寬度 = 右邊界 - 左邊界 - 1
  │
  │  ＋ 從一維變二維
  ▼
LC #85 Maximal Rectangle (Hard)
     TWIST: 逐行建 histogram → 對每行呼叫 Largest Rectangle
            把二維問題拆成 n 個一維問題
```

### 進化要素分析

```
括號配對 → 找下一個更大 → 面積計算 → 二維擴展

Monotonic Stack 是 Stack 進化的核心轉捩點：
  配對型 Stack → 只要 push/pop 看是否匹配
  Monotonic Stack → 維護一個有序結構，pop 時計算答案
```

### 程式碼對比

```python
# === Level 1: Valid Parentheses ===
def isValid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in mapping:
            if not stack or stack[-1] != mapping[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return len(stack) == 0

# === Level 2: Daily Temperatures (Monotonic Stack) ===
def dailyTemperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []                          # 存 index，遞減棧
    for i in range(n):
        while stack and temps[i] > temps[stack[-1]]:
            j = stack.pop()
            result[j] = i - j           # ← pop 時算距離
        stack.append(i)
    return result

# === Level 3: Largest Rectangle in Histogram (Hard) ===
def largestRectangleArea(heights):
    stack = []
    max_area = 0
    heights.append(0)                   # ← 哨兵：確保最後全部 pop
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1  # ← 寬度計算
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# === Level 4: Maximal Rectangle (Hard) ===
def maximalRectangle(matrix):
    if not matrix: return 0
    n = len(matrix[0])
    heights = [0] * n
    max_area = 0
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0  # ← 建 histogram
        max_area = max(max_area, largestRectangleArea(heights[:]))  # ← 復用 Level 3
    return max_area
```

### 辨識技巧

> 看到「下一個更大/更小」→ Monotonic Stack。
> 看到「直方圖」「柱狀圖」→ Monotonic Stack 計算面積。
> 看到「二維矩陣中最大矩形」→ 逐行 histogram + Largest Rectangle。

---

## Pattern 10: Heap 進化鏈

### 進化路線圖

```
LC #703 Kth Largest Element in a Stream (Easy)
  │  BASE: 維護一個 size = K 的 Min Heap
  │        堆頂就是第 K 大
  │
  │  ＋ 合併多個有序來源
  ▼
LC #23 Merge K Sorted Lists (Hard)
  │  TWIST: Multi-way merge — Heap 裡放每個 list 的當前最小
  │         pop 最小的 → 把它的 next 推入 Heap
  │
  │  ＋ 動態維護中位數
  ▼
LC #295 Find Median from Data Stream (Hard)
  │  TWIST: Two Heaps — Max Heap（左半）+ Min Heap（右半）
  │         保持兩邊 size 差 <= 1
  │         中位數 = 較大堆的堆頂 或 兩堆頂的平均
  │
  │  ＋ 不只是中位數，而是動態的 Top K
  ▼
LC #480 Sliding Window Median (Hard)
     TWIST: Two Heaps + Lazy Deletion（延遲刪除）
            窗口滑動時需要移除離開窗口的元素
            但 Heap 不支援任意刪除 → 用延遲刪除標記
```

### 進化要素分析

```
一個 Heap → 多路合併 → 兩個 Heap 對偶結構 → Heap + 動態窗口

Heap 題的關鍵問題：「我需要快速取得什麼？」
  - 第 K 大 → Min Heap of size K
  - 多路最小 → Min Heap 放每路的頭
  - 中位數 → 左半 Max Heap + 右半 Min Heap
```

### 程式碼：Two Heaps 技巧

```python
import heapq

# === Level 3: Find Median from Data Stream ===
class MedianFinder:
    def __init__(self):
        self.lo = []  # Max Heap (存負數模擬)，存較小的一半
        self.hi = []  # Min Heap，存較大的一半

    def addNum(self, num):
        heapq.heappush(self.lo, -num)              # 先放左邊
        heapq.heappush(self.hi, -heapq.heappop(self.lo))  # 左邊最大的丟右邊
        if len(self.hi) > len(self.lo):             # 保持左邊 >= 右邊
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

### 辨識技巧

> 看到「第 K 大/小」→ Heap。
> 看到「合併多個有序序列」→ Heap 做 multi-way merge。
> 看到「動態中位數」→ Two Heaps。

---

## Pattern 11: Union-Find 進化鏈

### 進化路線圖

```
LC #547 Number of Provinces (Medium)
  │  BASE: 基本 Union-Find，算連通分量個數
  │
  │  ＋ 判斷加邊是否形成環
  ▼
LC #684 Redundant Connection (Medium)
  │  TWIST: 如果 union(u, v) 時已經在同一集合 → 這條邊多餘
  │
  │  ＋ 動態連通 + 查詢
  ▼
LC #305 Number of Islands II (Hard)
  │  TWIST: 每次「加一塊陸地」後回報島嶼數量
  │         初始 count++，然後跟四周合併（每合併一次 count--）
  │
  │  ＋ 處理等式/不等式方程
  ▼
LC #399 Evaluate Division (Medium)
     TWIST: Weighted Union-Find
            每條邊帶權重（a/b = 2.0）
            查詢 a/c = a/b * b/c → 路徑上的權重乘積
```

### 進化要素分析

```
算連通分量 → 偵測環 → 動態增量 → 帶權重

Union-Find 的三板斧（所有級別都需要）：
  1. Path Compression: find(x) 時壓扁路徑
  2. Union by Rank: 小樹接大樹
  3. count 追蹤：每次 union 成功 → count -= 1
```

### 辨識技巧

> 看到「動態連通性」「是否在同一組」→ Union-Find。
> 看到「離線/增量地加邊並查詢」→ Union-Find 比 BFS 更有效。

---

## Pattern 12: Trie 進化鏈

### 進化路線圖

```
LC #208 Implement Trie (Medium)
  │  BASE: insert / search / startsWith
  │
  │  ＋ 支援萬用字元 '.'
  ▼
LC #211 Add and Search Word (Medium)
  │  TWIST: search 遇到 '.' → 對所有子節點做 DFS
  │
  │  ＋ 在 board 上搜尋多個 word
  ▼
LC #212 Word Search II (Hard)
     TWIST: Trie + Backtracking on Grid
            把所有 words 建成 Trie
            在 board 上 DFS，沿著 Trie 節點走
            比逐個 word 搜尋快非常多
```

### 進化要素分析

```
基本插入/查詢 → 模糊匹配 → Trie + 另一個 pattern（Backtracking）

Hard Trie 題的特徵：Trie 不是主角，而是加速器。
  LC #212 的本質是 Grid Backtracking
  Trie 的作用是讓你在 backtrack 時提前剪枝
```

### 辨識技巧

> 看到「前綴搜尋」「自動補全」→ Trie。
> 看到「在 grid/matrix 中搜尋多個 word」→ Trie + Backtracking。

---

## Pattern 13: Bit Manipulation 進化鏈

### 進化路線圖

```
LC #136 Single Number (Easy)
  │  BASE: XOR 全部 → 重複的抵消，剩下的就是答案
  │        a ^ a = 0, a ^ 0 = a
  │
  │  ＋ 有兩個不重複的
  ▼
LC #260 Single Number III (Medium)
  │  TWIST: 先 XOR 全部得到 a^b
  │         找到 a^b 中任一個 1 bit → 以此 bit 分兩組
  │         分別 XOR 兩組 → 得到 a 和 b
  │
  │  ＋ 每個數出現三次，只有一個出現一次
  ▼
LC #137 Single Number II (Medium)
     TWIST: 不能只用 XOR
            用 bit 計數：每個 bit position 累加出現次數 % 3
            或用狀態機（two, one 變數追蹤）
```

### Bit 進化的核心

```
單一 XOR → 分組 XOR → 位元計數/狀態機

Easy Bit 題: 一個性質解決（XOR 抵消）
Medium Bit 題: 需要組合多個 bit 操作
Hard Bit 題: 需要逐 bit 分析 + 可能結合其他 pattern
```

### 辨識技巧

> 看到「出現一次/兩次」→ XOR。看到「出現 K 次中找異類」→ 位元計數。
> 看到「不用額外空間」「O(1) space」→ 考慮 Bit Manipulation。

---

## Pattern 14: Greedy 進化鏈

### 進化路線圖

```
LC #455 Assign Cookies (Easy)
  │  BASE: 排序 + 雙指標貪心匹配
  │
  │  ＋ 判斷是否可達
  ▼
LC #55 Jump Game (Medium)
  │  TWIST: 維護「最遠可達位置」
  │         每一步更新 farthest = max(farthest, i + nums[i])
  │
  │  ＋ 要最少步數
  ▼
LC #45 Jump Game II (Medium)
  │  TWIST: 類似 BFS 的層次概念
  │         在當前「可達範圍」內找下一層的最遠距離
  │
  │  ＋ 區間問題
  ▼
LC #56 Merge Intervals (Medium)
  │  TWIST: 排序後依序合併重疊區間
  │
  │  ＋ 最少移除幾個區間使得不重疊
  ▼
LC #435 Non-overlapping Intervals (Medium)
  │  TWIST: 按結束時間排序 → 結束越早越好 → 貪心選不衝突的
  │
  │  ＋ 多維度貪心 + 複雜排序
  ▼
LC #630 Course Schedule III (Hard)
     TWIST: 按 deadline 排序 + Max Heap 動態替換
            如果加了某課超時 → pop 最耗時的課替換
```

### Greedy 進化的核心

```
簡單排序貪心 → 維護一個全域量 → 區間貪心 → 貪心 + 資料結構

Greedy 的難點不在於演算法本身，而在於：
  1. 你怎麼知道 Greedy 是對的？（證明最優子結構）
  2. 你按什麼排序？（排序標準決定成敗）
  3. 需要搭配什麼輔助結構？（Heap、Stack 等）
```

### 辨識技巧

> 看到「最少/最多」+ 直覺上「先處理某種元素比較好」→ 試 Greedy。
> 看到「區間」+ 排序 → Greedy。
> 不確定 Greedy 對不對 → 先想 DP，如果 DP 可以但 Greedy 更簡單 → 用 Greedy。

---

## Pattern 15: Prefix Sum 進化鏈

### 進化路線圖

```
LC #303 Range Sum Query (Easy)
  │  BASE: prefix[i] = sum(nums[0..i-1])
  │        rangeSum(l, r) = prefix[r+1] - prefix[l]
  │
  │  ＋ 二維矩陣
  ▼
LC #304 Range Sum Query 2D (Medium)
  │  TWIST: 二維前綴和
  │         prefix[i][j] = 左上角到 (i,j) 的總和
  │         區域和 = 容斥原理（加減四個矩形）
  │
  │  ＋ 不是找固定範圍的和，而是找「和為 K 的子陣列」
  ▼
LC #560 Subarray Sum Equals K (Medium)
  │  TWIST: Prefix Sum + HashMap
  │         如果 prefix[j] - prefix[i] == k → 區間 [i+1, j] 的和為 k
  │         HashMap 存「某個 prefix sum 出現過幾次」
  │
  │  ＋ 找「可整除 K」的最長子陣列
  ▼
LC #523 Continuous Subarray Sum (Medium)
  │  TWIST: Prefix Sum mod K + HashMap
  │         如果 prefix[j] % k == prefix[i] % k → 區間和整除 k
  │
  │  ＋ 二維 + 「和為 target」
  ▼
LC #363 Max Sum of Rectangle No Larger Than K (Hard)
     TWIST: 固定左右列 → 壓縮成一維
            一維用 Prefix Sum + Sorted Set (TreeSet)
            在 sorted set 中 binary search 找最接近的前綴和
```

### 進化要素分析

```
一維前綴和 → 二維前綴和 → 前綴和 + HashMap → 前綴和 + 取餘 → 多 pattern 組合

Prefix Sum 的核心思想永遠不變：
  sum(i..j) = prefix[j+1] - prefix[i]

但 twist 在於「你要找什麼」：
  Easy:   直接查區間和
  Medium: 找特定和 → 用 HashMap 加速
  Hard:   二維壓縮成一維 + 結合其他資料結構
```

### 辨識技巧

> 看到「子陣列的和」「區間和」→ Prefix Sum。
> 看到「和為 K」→ Prefix Sum + HashMap。
> 看到「二維區間和」→ 二維 Prefix Sum 或壓縮降維。

---

## 進化地圖總覽

以下是所有 15 個 pattern 的進化路線，一圖看清全貌。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Easy → Medium → Hard 進化地圖                      │
├─────────────┬─────────────────┬──────────────────┬──────────────────────┤
│   Pattern   │     Easy        │    Medium         │       Hard          │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Two Sum     │ HashMap lookup  │ +sorted→2 Ptr    │                     │
│             │                 │ +多一個→3Sum     │                     │
│             │                 │ +再多一→4Sum     │                     │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Binary      │ 找到就回傳       │ +找邊界          │ +BS on Answer       │
│ Search      │                 │ +旋轉陣列        │  +Greedy Check      │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Sliding     │ 固定窗口         │ +可變+HashSet    │ +可變+HashMap       │
│ Window      │                 │                  │  +formed計數        │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Tree DFS    │ max depth       │ +全域追蹤        │ +路徑可彎折         │
│             │ (直接回傳)       │ (Diameter)       │  +負數處理          │
│             │                 │                  │ (Max Path Sum)      │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ BFS         │ Level Order     │ +Grid BFS        │ +Implicit Graph     │
│             │                 │ +Multi-source    │ +Bidirectional      │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Graph       │                 │ TopSort基本      │ +自己建圖           │
│             │                 │ +記錄順序        │  +edge case處理     │
│             │                 │ +Dijkstra        │ (Alien Dictionary)  │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ DP          │ Fibonacci型     │ +選/不選          │ +區間 DP            │
│             │ dp[i]=dp[i-1]   │ +二維(LCS)       │ +逆向思維          │
│             │  +dp[i-2]       │ +三路(Edit Dist) │ (Burst Balloons)   │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Backtrack   │                 │ Subsets 基本     │ +棋盤約束           │
│             │                 │ +去重            │ (N-Queens)          │
│             │                 │ +目標和          │ +三重約束           │
│             │                 │                  │ (Sudoku Solver)     │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Stack       │ 括號配對         │ Monotonic Stack  │ +面積計算           │
│             │                 │ (Next Greater)   │ (Histogram)         │
│             │                 │                  │ +二維擴展           │
│             │                 │                  │ (Maximal Rect)      │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Heap        │ Kth Largest     │                  │ Multi-way Merge     │
│             │ (size K)        │                  │ Two Heaps           │
│             │                 │                  │ (Median Stream)     │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Union-Find  │                 │ 連通分量+偵測環   │ +動態增量           │
│             │                 │                  │ +帶權重             │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Trie        │                 │ 基本 insert/     │ +Trie+Backtracking  │
│             │                 │ search           │ (Word Search II)    │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Bit         │ XOR 抵消        │ +分組 XOR        │                     │
│ Manipulate  │ (Single Number) │ +位元計數        │                     │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Greedy      │ 排序+匹配       │ +維護最遠距離    │ +Greedy+Heap       │
│             │                 │ +區間合併/移除   │ (Course Sched III)  │
├─────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Prefix Sum  │ 一維區間和       │ +二維區間和      │ +壓縮降維          │
│             │                 │ +HashMap找和為K  │  +Sorted Set       │
└─────────────┴─────────────────┴──────────────────┴──────────────────────┘
```

### 各 Pattern 「Hard 化」的 5 大 Twist 統計

```
Twist 類型                     出現在哪些 Pattern
──────────────────────────────────────────────────────────
1. 多一個維度 (1D→2D)         Stack, Prefix Sum, DP
2. 搜尋空間抽象化             Binary Search, BFS
3. 自己建圖/建結構             Graph, Trie, Heap
4. 組合兩個 Pattern           Trie+Backtrack, BS+Greedy, Stack+DP, Greedy+Heap
5. Edge Case 爆炸             Graph(Alien Dict), Backtrack(Sudoku)
```

---

## 面試實戰：如何拆解未知的 Hard 題

### Step-by-Step 拆解流程

```
第 1 步：讀題後，問自己「這題的輸入/輸出像什麼？」
  - Array + 找某個值 → Two Pointers / Binary Search / Sliding Window
  - Tree/Graph 結構 → DFS / BFS / TopSort / Union-Find
  - 「最優解」「方案數」 → DP
  - 「列出所有」 → Backtracking

第 2 步：確認 Base Pattern 後，問「有什麼不一樣的地方？」
  - 排序了？→ 可以用 Two Pointers / Binary Search
  - 多維了？→ 需要升維或壓縮降維
  - 圖不直接給？→ 需要建圖
  - 有額外約束？→ 需要更複雜的驗證

第 3 步：識別 Twist 後，套用對應的處理方法
  - 多一維 → 外層迴圈 + 內層用已知算法
  - 抽象搜尋空間 → Binary Search on Answer
  - 需建圖 → 先花時間把圖建出來，剩下用標準算法
  - 兩個 Pattern 組合 → 一個做主體，一個做輔助

第 4 步：寫 code 前，先用小範例驗證你的思路
  - 特別注意 edge case（空輸入、一個元素、全相同等）
```

### 常見的 Hard 題 = Pattern A + Pattern B 組合

| Hard 題 | Pattern A | Pattern B | 組合方式 |
|---------|-----------|-----------|---------|
| Split Array Largest Sum | Binary Search | Greedy | BS 猜答案，Greedy 驗證 |
| Word Search II | Backtracking | Trie | Trie 加速 Backtracking 剪枝 |
| Maximal Rectangle | Stack (Histogram) | DP (逐行) | 每行建 histogram 後用 Stack 解 |
| Sliding Window Median | Sliding Window | Two Heaps | 窗口滑動時動態維護中位數 |
| Alien Dictionary | Graph (TopSort) | String比較 | 比較字串建邊，TopSort求順序 |
| Trapping Rain Water | Two Pointers | Monotonic Stack | 兩種解法都可以（經典面試題） |
| Course Schedule III | Greedy (排序) | Heap | 按 deadline 排序，Heap 動態替換 |
| Burst Balloons | DP (區間) | 逆向思維 | 「最後戳」而非「先戳」 |

### 最終心法

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   「Hard 題不是新的演算法，而是你已經會的東西的排列組合。」   │
│                                                          │
│   你要練的不是「學更多演算法」，                             │
│   而是「辨識 base pattern」+「識別 twist」的速度。           │
│                                                          │
│   把這 15 條進化鏈背熟，                                   │
│   面試時看到 Hard 題，你就能在 30 秒內定位到：               │
│   「這是 Pattern X 的 Level Y 進化，twist 是 Z。」          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

> **建議搭配使用**：
> - `00_解題框架_總覽.py` — Pattern 辨識的快速查表
> - `01-18` 各主題教學 — 每個 Base Pattern 的詳細教學
> - 本文件 — 理解 Easy → Hard 的進化邏輯，消除對 Hard 的恐懼
