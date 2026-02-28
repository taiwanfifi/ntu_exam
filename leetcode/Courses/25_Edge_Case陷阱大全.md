# Edge Case 陷阱大全 — 面試前必須知道的每一個坑

> **定位**：LeetCode / Google 面試中所有會讓你 WA、TLE、RE 的 edge case 百科全書
> **適用對象**：刷題到一定量但仍「偶爾 WA 找不出原因」的面試準備者
> **核心信念**：AC 和 WA 的差距不是算法不會，是 edge case 沒想到
> **語言**：繁體中文 + English 技術術語
> **配套**：每個陷阱都有 concrete code + 數值範例，不講空話

---

## 目錄

| 章 | 主題 | 頁內連結 |
|----|------|---------|
| 1 | 為什麼 Edge Case 決定面試成敗 | [第一章](#第一章為什麼-edge-case-決定面試成敗) |
| 2 | 通用陷阱（所有題都要注意） | [第二章](#第二章通用陷阱所有題都要注意) |
| 3 | Binary Search 陷阱 | [第三章](#第三章binary-search-陷阱最多-bug-的算法) |
| 4 | Tree 陷阱 | [第四章](#第四章tree-陷阱) |
| 5 | Graph 陷阱 | [第五章](#第五章graph-陷阱) |
| 6 | DP 陷阱 | [第六章](#第六章dp-陷阱) |
| 7 | Sliding Window 陷阱 | [第七章](#第七章sliding-window-陷阱) |
| 8 | Stack 陷阱 | [第八章](#第八章stack-陷阱) |
| 9 | Linked List 陷阱 | [第九章](#第九章linked-list-陷阱) |
| 10 | Backtracking 陷阱 | [第十章](#第十章backtracking-陷阱) |
| 11 | Python 語言特有陷阱 | [第十一章](#第十一章python-語言特有陷阱) |
| 12 | 面試中的 Edge Case 提問模板 | [第十二章](#第十二章面試中的-edge-case-提問模板) |

---

# 第一章：為什麼 Edge Case 決定面試成敗

```
Google 面試評分四維度：
1. Coding          — 能寫出 code
2. Algorithms      — 選對算法
3. Communication   — 溝通清楚
4. Edge Cases      — 邊界處理 ← 直接決定 Hire / No Hire 的邊界

你算法寫對但 edge case 沒處理 = Lean No Hire
你算法有小瑕疵但 edge case 考慮周全 = Lean Hire

面試官在想：「這個人進了 Google，code 部署到 production...
 遇到空輸入會 crash 嗎？遇到負數會算出荒謬結果嗎？」
Edge case = Production Readiness，不是加分題，是基本要求。
```

## 1.3 常見的 5 種 Edge Case 來源

```
來源 1：空 (Empty)
  → 空陣列、空字串、空樹、空圖
  → 最常見，也最容易漏

來源 2：一 (Single)
  → 只有一個元素、只有一個節點
  → 很多算法在 n=1 時邏輯不同

來源 3：邊界 (Boundary)
  → 第一個元素、最後一個元素
  → i-1 和 i+1 越界
  → 最大值、最小值剛好在端點

來源 4：溢出 (Overflow)
  → 整數上溢 / 下溢（Java/C++ 的 2^31 - 1）
  → 乘法溢出（兩個大數相乘）
  → Python 不會溢出，但其他語言會！

來源 5：特殊值 (Special Values)
  → 0（除以零、乘以零）
  → 負數（影響排序、比較、取餘）
  → 重複值（去重邏輯）
  → float('inf')、-float('inf')

記憶口訣：「空一邊溢特」
```

---

# 第二章：通用陷阱（所有題都要注意）

> 不管你在解什麼題，以下 15 個陷阱你都要過一遍。

## 通用陷阱速查表

| # | 陷阱 | 觸發條件 | 後果 | 預防方法 | 嚴重度 |
|---|------|---------|------|---------|--------|
| 1 | 空輸入 | `nums=[]`, `s=""` | IndexError / 返回錯誤值 | 開頭 `if not nums: return ...` | ★★★★★ |
| 2 | 單元素 | `nums=[1]`, `s="a"` | 邏輯不走迴圈直接跳出 | 手動驗證 n=1 | ★★★★☆ |
| 3 | 全相同 | `[5,5,5,5]` | 去重失敗 / 二分搜尋失敗 | 考慮此 case | ★★★★☆ |
| 4 | 負數 | `[-1,-2,3]` | sum 計算錯 / 排序假設錯 | 確認題目是否有負 | ★★★★☆ |
| 5 | 整數溢出 | `2^31 - 1 + 1` | Python 沒問題，Java/C++ 爆掉 | `mid = left + (right-left)//2` | ★★★★★ |
| 6 | 零值 | `amount=0`, `n=0` | 邊界初始化錯誤 | 注意 dp[0] 初始值 | ★★★★☆ |
| 7 | 最大/最小值初始化 | `float('inf')`, `-float('inf')` | 比較邏輯出錯 | 注意初始化方向 | ★★★☆☆ |
| 8 | Off-by-one | `range(n)` vs `range(n+1)` | 少算或多算一個 | 邊界值帶入驗證 | ★★★★★ |
| 9 | 浮點精度 | `0.1 + 0.2 != 0.3` | 比較失敗 | 用 `abs(a-b) < 1e-9` | ★★★☆☆ |
| 10 | 修改正在遍歷的集合 | for loop 中 remove 元素 | 跳過元素或 RuntimeError | 用新 list 或倒序遍歷 | ★★★★☆ |
| 11 | 遞迴深度 | n=10000 的 linked list | RecursionError (Python 預設 1000) | 改用迭代 / `sys.setrecursionlimit` | ★★★☆☆ |
| 12 | 回傳型別錯誤 | 該回 list 回了 generator | Judge 判錯 | 確認回傳型別 | ★★★☆☆ |
| 13 | 字串不可變 | `s[0] = 'A'` | TypeError | 轉 list 再操作 | ★★★☆☆ |
| 14 | 空格 / 特殊字元 | `"  hello  "`, `"a,b.c"` | split 結果有空字串 | strip + 過濾 | ★★★☆☆ |
| 15 | 大小寫 | `"AbC"` | 比較失敗 | `.lower()` 統一 | ★★☆☆☆ |

## 陷阱 #5 詳解：整數溢出（面試最高頻）

```python
# Python 不會溢出（大數自動擴展），但 Java/C++ 會！

# 問題：計算 mid
left, right = 0, 2**31 - 1  # right = 2147483647

# 錯誤（Java/C++）：
mid = (left + right) // 2     # left + right 溢出！

# 正確：
mid = left + (right - left) // 2  # 不會溢出

# 同理，乘法也要注意：
# Java: int a = 100000; int b = 100000; int c = a * b;
# c = 1410065408（溢出了！正確答案是 10000000000）
# 解法：用 long → long c = (long)a * b;
```

## 陷阱 #8 詳解：Off-by-one（永恆的痛）

```python
# 場景 1：遍歷範圍
nums = [1, 2, 3, 4, 5]  # 長度 5
for i in range(len(nums)):      # i = 0,1,2,3,4 ✓
for i in range(len(nums) - 1):  # i = 0,1,2,3   ✓（比較相鄰元素時）
for i in range(1, len(nums)):   # i = 1,2,3,4   ✓（從第二個開始）

# 場景 2：子字串
s = "hello"
s[1:3]   # "el"  — 包含 index 1，不包含 index 3
s[:3]    # "hel" — 前 3 個字元
s[3:]    # "lo"  — 從 index 3 到結尾

# 場景 3：DP 陣列大小
# 「爬 n 階樓梯」→ dp 大小 = n+1（因為包含 dp[0] 到 dp[n]）
# 「n 個字元的字串」→ dp 大小 = n+1（dp[0] 代表空字串）
```

---

# 第三章：Binary Search 陷阱（最多 Bug 的算法！）

> Binary Search 看似簡單，但它是面試中 bug 率最高的算法。差一個 `=`、差一個 `+1`，結果完全不同。

## 陷阱 3.1：無限循環 (Infinite Loop)

```python
# 經典無限循環場景：
left, right = 0, 1
# 每次 mid = left + (right - left) // 2 = 0 + 0 = 0
# 如果條件是 left = mid → left 永遠是 0 → 無限循環！

# 具體範例：在 [1, 3] 中找 3
nums = [1, 3]
left, right = 0, 1

# 迴圈 1: mid = 0, nums[0]=1 < 3, left = mid = 0  ← 沒動！無限循環！

# 解法：當 left = mid 時，用上取整
# mid = left + (right - left + 1) // 2
left, right = 0, 1
# mid = 0 + (1 - 0 + 1) // 2 = 1
# nums[1] = 3 → 找到！

# 完整的安全模板：
def binary_search_safe(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:           # 注意是 <=
        mid = left + (right - left) // 2  # 防溢出
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1         # 注意是 +1
        else:
            right = mid - 1        # 注意是 -1
    return -1
```

## 陷阱 3.2：Off-by-one — Left Bound vs Right Bound

```python
# 找 Left Bound（第一個 >= target 的位置）
# nums = [1, 2, 2, 2, 3], target = 2 → 答案是 index 1

def left_bound(nums, target):
    left, right = 0, len(nums)  # 注意：right = len(nums)，不是 len-1
    while left < right:          # 注意：< 不是 <=
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid          # 注意：不是 mid-1
    return left

# 找 Right Bound（最後一個 <= target 的位置）
# nums = [1, 2, 2, 2, 3], target = 2 → 答案是 index 3

def right_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:   # 注意：<= 不是 <
            left = mid + 1
        else:
            right = mid
    return left - 1               # 注意：回傳 left-1

# 常見錯誤：把 left bound 和 right bound 的 < / <= 搞混
# 口訣：找左邊界 → nums[mid] < target → left = mid+1
#       找右邊界 → nums[mid] <= target → left = mid+1，最後 return left-1
```

## 陷阱 3.3：搜尋空間為空 / 結果越界

```python
# 搜尋後 left 可能超出陣列範圍！
nums = [1, 3, 5]
target = 6
# left_bound 回傳 3 → 超出陣列！必須檢查：
result = left_bound(nums, 6)
if result < len(nums) and nums[result] == 6:
    print("Found")
else:
    print("Not Found")  # ← 會走這裡
```

## 陷阱 3.4：旋轉數組有重複元素

```python
# LC 81: Search in Rotated Sorted Array II
# nums = [1, 0, 1, 1, 1], target = 0

# 問題：nums[left]=1, nums[mid]=1, nums[right]=1
# 你無法判斷哪邊是有序的！

# 解法：當 nums[left] == nums[mid] == nums[right] 時，收縮邊界
def search_rotated_dup(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return True

        # 關鍵：無法判斷時，收縮邊界
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:  # 左半有序
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                          # 右半有序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return False

# 注意：加了 left += 1; right -= 1 後，worst case 變成 O(n)
# 例如 [1,1,1,...,1,0,1,...,1,1] → 每次只縮 1 → O(n)
```

## 陷阱 3.5：Binary Search on Answer — check 函數的邊界

```python
# LC 875: Koko Eating Bananas
# piles = [3, 6, 7, 11], h = 8
# 找最小速度 k，使得 k 根/小時能在 h 小時內吃完

# check(k): 速度 k 能否在 h 小時內吃完？
import math
def can_finish(piles, h, k):
    hours = sum(math.ceil(p / k) for p in piles)
    return hours <= h

# 陷阱 1：搜尋範圍的左右邊界
left = 1                   # 最小速度是 1（不是 0！除以 0 會 crash）
right = max(piles)         # 最大速度 = 最大堆（一次吃完最大堆）

# 陷阱 2：check 函數的 <= 還是 <
# 這裡是「找最小的 k 使得 can_finish 為 True」→ left bound 模板
while left < right:
    mid = left + (right - left) // 2
    if can_finish(piles, h, mid):
        right = mid        # mid 可以 → 試更小的
    else:
        left = mid + 1     # mid 不行 → 要更大的
return left

# 陷阱 3：ceil division 的實作
# math.ceil(p / k) 用浮點數，可能有精度問題
# 更安全的寫法：(p + k - 1) // k（整數運算，無精度問題）
```

---

# 第四章：Tree 陷阱

## 陷阱 4.1：空樹

```python
# 最基本但最常忘記的
def maxDepth(root):
    if root is None:       # ← 忘了這行就 crash
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# 面試中，面試官給的第一個 test case 通常就是 root = None
# 回傳值要看題目：depth 回 0、path sum 回 False、list 回 []
```

## 陷阱 4.2：單節點與偏斜樹

```python
# 單節點：root = TreeNode(1)，很多遞迴在 n=1 時邏輯不同
# 偏斜樹：退化成 linked list → 遞迴深度=n 可能 StackOverflow
#   1 → 2 → 3 → 4 (每個只有右子)
# 影響：BST 搜尋從 O(log n) 退化到 O(n)
# 防護：面試時主動說 "worst case is a skewed tree"
```

## 陷阱 4.4：Min Depth 的經典陷阱（超高頻考點）

```python
# LC 111: Minimum Depth of Binary Tree
# 定義：從 root 到最近的 **葉子節點** 的路徑長度

#     1
#    /
#   2
# 正確答案：min depth = 2（葉子是 node 2）
# 錯誤答案：min depth = 1（把 None 當成葉子了！）

# 錯誤寫法：
def minDepth_WRONG(root):
    if not root:
        return 0
    return 1 + min(minDepth_WRONG(root.left), minDepth_WRONG(root.right))
    # root=1 時：min(minDepth(2), minDepth(None)) = min(2, 0) = 0
    # 回傳 1 + 0 = 1 ← 錯！None 不是葉子！

# 正確寫法：
def minDepth_CORRECT(root):
    if not root:
        return 0
    if not root.left:           # 左子樹空 → 只算右子樹
        return 1 + minDepth_CORRECT(root.right)
    if not root.right:          # 右子樹空 → 只算左子樹
        return 1 + minDepth_CORRECT(root.left)
    return 1 + min(minDepth_CORRECT(root.left), minDepth_CORRECT(root.right))
```

## 陷阱 4.5：BST 驗證只比較 parent-child 是不夠的

```python
# LC 98: Validate BST
#       5
#      / \
#     1   6
#        / \
#       3   7    ← 3 < 5，違反 BST！但 3 > 6 的左子？不對，3 < 6 才是左子

# 光比較 node.val > node.left.val 是不夠的
# 要傳遞整個合法範圍 [low, high]

# 錯誤寫法：
def isValidBST_WRONG(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:   # 只看一層
        return False
    if root.right and root.right.val <= root.val:  # 只看一層
        return False
    return isValidBST_WRONG(root.left) and isValidBST_WRONG(root.right)
# [5,1,6,null,null,3,7] → 回傳 True（錯！3 應該 > 5）

# 正確寫法：
def isValidBST(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True
    if root.val <= low or root.val >= high:
        return False
    return (isValidBST(root.left, low, root.val) and
            isValidBST(root.right, root.val, high))
```

## 陷阱 4.6：Path Sum 中的負數 — 不能提前剪枝

```python
# LC 112: Path Sum
# target = 7
#       1
#      / \
#     -3   5
#    /
#   9

# 路徑 1 → -3 → 9 = 7 ✓
# 但如果你在 node=-3 時看到 current_sum = 1+(-3) = -2 < 7 就剪枝
# 你就錯過了後面的 9！

# 錯誤剪枝（假設所有值為正的時候才能這樣寫）：
def pathSum_WRONG(root, target, current=0):
    if not root:
        return False
    current += root.val
    if current > target:    # ← 如果有負數，這個剪枝是錯的！
        return False
    if not root.left and not root.right:
        return current == target
    return pathSum_WRONG(root.left, target, current) or \
           pathSum_WRONG(root.right, target, current)

# 正確寫法：不剪枝，走完所有路徑
def pathSum_CORRECT(root, target):
    if not root:
        return False
    target -= root.val
    if not root.left and not root.right:
        return target == 0
    return pathSum_CORRECT(root.left, target) or \
           pathSum_CORRECT(root.right, target)
```

---

# 第五章：Graph 陷阱

## 陷阱 5.1：自環 (Self-loop)

```python
# 鄰接表中 node → node
edges = [[0,1], [1,2], [2,2]]  # node 2 有自環！

# 影響 1：DFS/BFS 如果不標 visited → 無限循環
# 影響 2：degree 計算出錯（自環讓 degree +2 還是 +1？）
# 影響 3：拓撲排序中自環 = cycle → 不可能排序

# 建圖時注意：
graph = defaultdict(list)
for u, v in edges:
    if u != v:  # 過濾自環（如果題目需要）
        graph[u].append(v)
        graph[v].append(u)
```

## 陷阱 5.2：重複邊

```python
# edges = [[0,1], [0,1], [1,2]]  # 0-1 出現兩次！
# 影響：graph[0] = [1, 1]，遍歷走兩次
# 解法：用 set 建圖
graph = defaultdict(set)  # set 而不是 list → 自動去重
for u, v in edges:
    graph[u].add(v)
    graph[v].add(u)
```

## 陷阱 5.3：斷開的圖 (Disconnected Graph)

```python
# 很多人假設圖是連通的，但題目可能給斷開的圖！
# nodes: 0, 1, 2, 3, 4
# edges: [[0,1], [2,3]]  → 0-1 一組，2-3 一組，4 孤立

# 如果你只從 node 0 開始 BFS → 你只會訪問到 0 和 1
# node 2, 3, 4 完全被忽略

# 正確做法：遍歷所有起點
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = 0
    for node in range(n):         # ← 必須從每個 node 嘗試
        if node not in visited:
            bfs(node, graph, visited)
            components += 1
    return components
```

## 陷阱 5.4：有向 vs 無向搞混

```python
# 有向圖：edge (u, v) 表示 u → v（單向）
# 無向圖：edge (u, v) 表示 u ↔ v（雙向）

# 建圖時的差別：
# 有向圖：
for u, v in edges:
    graph[u].append(v)       # 只加一個方向

# 無向圖：
for u, v in edges:
    graph[u].append(v)       # 加兩個方向
    graph[v].append(u)

# 搞混的後果：
# 1. 無向圖只加了單向 → 有些路徑找不到
# 2. 有向圖加了雙向 → Cycle detection 誤判、拓撲排序失敗

# 面試中問清楚："Is this a directed or undirected graph?"
```

## 陷阱 5.5：Grid 邊界檢查

```python
# Grid (m x n) 的四個方向遍歷
directions = [(0,1), (0,-1), (1,0), (-1,0)]

def is_valid(i, j, rows, cols):
    return 0 <= i < rows and 0 <= j < cols

# 常見 bug：
# 1. 忘記檢查 → IndexError
# 2. 用 i >= 0 and i < rows 但忘了 j
# 3. rows 和 cols 寫反了（grid[i][j] 中 i 是 row，j 是 col）

# 安全模板：
for di, dj in directions:
    ni, nj = i + di, j + dj
    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] not in visited:
        # process (ni, nj)
        pass
```

## 陷阱 5.6：BFS 中 visited 的標記時機（超重要！）

```python
# 錯誤：在 dequeue 時標記 visited
def bfs_WRONG(start, graph):
    queue = deque([start])
    visited = set()
    while queue:
        node = queue.popleft()
        visited.add(node)          # ← 太晚了！
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
    # 問題：node A 和 node B 都把 node C 加入 queue
    # → C 被加入兩次 → 處理兩次 → TLE（嚴重時指數級膨脹）

# 正確：在 enqueue 時標記 visited
def bfs_CORRECT(start, graph):
    queue = deque([start])
    visited = {start}              # ← 起點也要標記！
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # ← 在加入 queue 時就標記
                queue.append(neighbor)

# 數值範例：
# Graph: 0-1, 0-2, 1-3, 2-3
# 錯誤做法：queue 中 3 會被加兩次（來自 1 和 2）
# 正確做法：3 第一次被某鄰居發現就標記，不會重複加入
```

---

# 第六章：DP 陷阱

## 陷阱 6.1：dp[0] 初始化錯誤

```python
# LC 70: Climbing Stairs — 爬 n 階樓梯，每次 1 或 2 步
# dp[i] = 到達第 i 階的方法數
# dp[0] = 1（站在地上，一種方式「什麼都不做」）
# dp[1] = 1（走一步）
# dp[i] = dp[i-1] + dp[i-2]

# LC 322: Coin Change — 最少硬幣湊出 amount
# dp[i] = 湊出金額 i 的最少硬幣數
# dp[0] = 0（金額 0 需要 0 枚硬幣）
# dp[i] = float('inf')（初始化為不可能）

# 口訣：
# 計數問題 → dp[0] = 1（空集算一種）
# 最小值問題 → dp[0] = 0，其餘 inf
# 最大值問題 → dp[0] = 0，其餘 -inf 或 0
# 布林問題 → dp[0] = True

# 常見錯誤：
# Coin Change 回傳 dp[amount]，但忘記檢查是否仍為 inf
# → 應該回傳 dp[amount] if dp[amount] != float('inf') else -1
```

## 陷阱 6.2：邊界 i-1, i-2 越界

```python
# Climbing Stairs: dp[i] = dp[i-1] + dp[i-2]
# 當 i=0 時，i-1=-1 和 i-2=-2 都越界！

# 錯誤：
dp = [0] * (n + 1)
for i in range(n + 1):
    dp[i] = dp[i-1] + dp[i-2]  # i=0 時 crash！

# 正確：先初始化 base case，迴圈從 2 開始
dp = [0] * (n + 1)
dp[0] = 1
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]

# 更安全：n=0 或 n=1 時直接 return
if n <= 1:
    return 1
```

## 陷阱 6.3：Coin Change — amount=0

```python
# LC 322: Coin Change
# amount = 0, coins = [1, 2, 5]
# 答案是 0（不需要任何硬幣），不是 -1

def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0                    # ← 這行是關鍵
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# amount=0 → 直接回傳 dp[0] = 0 ✓
```

## 陷阱 6.4：0/1 Knapsack 迴圈方向

```python
# 這是 DP 中最常搞混的地方！

# 0/1 Knapsack（每個物品只能用一次）→ 容量從大到小遍歷
for i in range(len(items)):
    for w in range(W, items[i].weight - 1, -1):  # 反向！
        dp[w] = max(dp[w], dp[w - items[i].weight] + items[i].value)

# Complete Knapsack（每個物品可以用無限次）→ 容量從小到大遍歷
for i in range(len(items)):
    for w in range(items[i].weight, W + 1):       # 正向！
        dp[w] = max(dp[w], dp[w - items[i].weight] + items[i].value)

# 為什麼？
# 反向：dp[w] 用的是上一輪（物品 i-1）的 dp[w - weight]
#       → 物品 i 只用了一次 ✓
# 正向：dp[w] 用的是本輪（物品 i）已更新的 dp[w - weight]
#       → 物品 i 可能被重複使用 ✓

# 數值範例：items = [{weight:2, value:3}], W = 4
# 反向（0/1）：dp[4]=3, dp[2]=3  → 物品只用 1 次
# 正向（完全）：dp[2]=3, dp[4]=6 → 物品用了 2 次
```

## 陷阱 6.5：字串 DP 的索引偏移

```python
# LC 1143: Longest Common Subsequence
# s1 = "abcde", s2 = "ace"

# dp[i][j] = s1[:i] 和 s2[:j] 的 LCS 長度
# 注意：dp[0][j] 和 dp[i][0] 代表空字串，值為 0

# 陷阱：dp[i][j] 對應的字元是 s1[i-1] 和 s2[j-1]，不是 s1[i] 和 s2[j]！

m, n = len(s1), len(s2)
dp = [[0] * (n + 1) for _ in range(m + 1)]

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:      # ← i-1 和 j-1，不是 i 和 j！
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])

# 常見 bug：用 s1[i] == s2[j] → IndexError（因為 i 可以到 m）
```

## 陷阱 6.6：Palindrome DP 的填表順序

```python
# LC 516: Longest Palindromic Subsequence
# dp[i][j] = s[i..j] 中最長回文子序列的長度

# 遞推關係：
# s[i] == s[j] → dp[i][j] = dp[i+1][j-1] + 2
# s[i] != s[j] → dp[i][j] = max(dp[i+1][j], dp[i][j-1])

# 陷阱：dp[i][j] 依賴 dp[i+1][j-1]，所以 i 必須從大到小填！

n = len(s)
dp = [[0] * n for _ in range(n)]

# Base case: 長度 1 的子串
for i in range(n):
    dp[i][i] = 1

# 填表：i 從下到上（大到小），j 從左到右（小到大）
for i in range(n - 2, -1, -1):     # i: n-2 → 0
    for j in range(i + 1, n):       # j: i+1 → n-1
        if s[i] == s[j]:
            dp[i][j] = dp[i+1][j-1] + 2
        else:
            dp[i][j] = max(dp[i+1][j], dp[i][j-1])

# 如果 i 從小到大填 → dp[i+1][j-1] 還沒算 → 答案全錯
```

---

# 第七章：Sliding Window 陷阱

## 陷阱 7.1：有負數時 Sliding Window 失效

```python
# Sliding Window 的前提：窗口擴大時 sum 增加，縮小時 sum 減少
# 如果有負數，這個前提不成立！

# 例：找 sum >= 7 的最短子陣列
nums = [2, -1, 2, 3, -2, 4, 1]

# Sliding Window 的邏輯：
# sum < 7 → 擴大窗口
# sum >= 7 → 縮小窗口
# 但 [-1] 讓你縮小窗口時 sum 反而變大！邏輯崩潰。

# 解法：有負數時用 Prefix Sum + Monotonic Deque 或其他方法
# LC 209 (Minimum Size Subarray Sum) 明確說了 positive integers
# 如果面試題沒說 → 你必須問 "Are all numbers positive?"
```

## 陷阱 7.2：窗口大小 > 陣列長度

```python
# 例：找大小為 k 的窗口最大和，但 k > len(nums)
nums = [1, 2, 3]
k = 5

# 如果不檢查 → 窗口永遠湊不到 k 個元素 → 回傳錯誤結果或 crash
def max_window_sum(nums, k):
    if k > len(nums):
        return -1            # 或 raise Error，看題目要求

    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## 陷阱 7.3：計數窗口 formed 的更新時機

```python
# LC 76: Minimum Window Substring
# 陷阱：formed 只在某字元的 window_count「剛好等於」need_count 時 +1
#       不是每次加入字元都 +1！

# 擴大窗口：
if c in need and window_counts[c] == need[c]:   # 「剛好達到」→ +1
    formed += 1

# 縮小窗口：
if left_c in need and window_counts[left_c] < need[left_c]:  # 「剛好不夠」→ -1
    formed -= 1

# 錯誤：每次加入都 +1 → formed 會超過 required → 提前 shrink → 遺漏答案
```

## 陷阱 7.4：Shrink 條件用 while 不是 if

```python
# 左邊界可能需要連續縮小多次

# 錯誤：
if window_is_valid():
    update_answer()
    l += 1                   # 只縮了一次！

# 正確：
while window_is_valid():
    update_answer()
    l += 1                   # 可能連續縮小多次

# 具體例子：
# nums = [1, 1, 1, 1, 1, 100], target = 100
# 當 r 到 index 5 (值=100) 時，sum = 105 >= 100
# 需要持續 shrink 直到 sum < 100
# l 需要從 0 一路移到 5，不是只移一步
```

---

# 第八章：Stack 陷阱

## 陷阱 8.1：空 stack pop

```python
# 在 pop 之前必須檢查 stack 是否為空

# 錯誤：
stack = []
top = stack.pop()   # IndexError: pop from empty list

# 正確：
if stack:
    top = stack.pop()

# 或用條件表達式：
top = stack.pop() if stack else default_value

# 面試中常見場景：括號匹配
s = "]"
stack = []
if s[0] in [')', ']', '}']:
    if not stack:          # ← 沒有對應的開括號
        return False
    stack.pop()
```

## 陷阱 8.2：Monotonic Stack 方向搞混

```python
# Next Greater Element → 用遞減 stack（從 top 到 bottom 遞減）
# Next Smaller Element → 用遞增 stack（從 top 到 bottom 遞增）

# LC 496: Next Greater Element
# 找每個元素右邊第一個比它大的元素

# 正確（遞減 stack）：
def nextGreaterElement(nums):
    result = [-1] * len(nums)
    stack = []  # 存 index，stack 中對應的值從 bottom 到 top 遞減

    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]   # nums[i] 是 idx 的 Next Greater
        stack.append(i)
    return result

# nums = [2, 1, 2, 4, 3]
# i=0: stack=[0]                    (2)
# i=1: 1 < 2, stack=[0,1]          (2,1)
# i=2: 2 > 1, pop 1→result[1]=2;   2==2 不 pop; stack=[0,2]
# i=3: 4 > 2, pop 2→result[2]=4;   4 > 2, pop 0→result[0]=4; stack=[3]
# i=4: 3 < 4, stack=[3,4]
# result = [4, 2, 4, -1, -1]

# 常見錯誤：用遞增 stack 找 Next Greater → 結果完全相反
```

## 陷阱 8.3：Largest Rectangle — 忘記處理剩餘元素

```python
# LC 84: Largest Rectangle in Histogram
# heights = [2, 1, 5, 6, 2, 3]

def largestRectangleArea(heights):
    stack = []  # 存 index，遞增 stack
    max_area = 0

    for i in range(len(heights)):
        while stack and heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1 if stack else i
            max_area = max(max_area, h * w)
        stack.append(i)

    # 陷阱：迴圈結束後 stack 裡可能還有元素！
    # 如果不處理 → 遺漏了一些矩形
    while stack:
        h = heights[stack.pop()]
        w = len(heights) - stack[-1] - 1 if stack else len(heights)
        max_area = max(max_area, h * w)

    return max_area

# 更簡潔的寫法：在 heights 末尾加一個 0，強制清空 stack
def largestRectangleArea_v2(heights):
    heights.append(0)            # ← 加一個 0
    stack = []
    max_area = 0
    for i in range(len(heights)):
        while stack and heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1 if stack else i
            max_area = max(max_area, h * w)
        stack.append(i)
    heights.pop()                # 還原（禮貌）
    return max_area
```

## 陷阱 8.4：括號匹配 — 多種括號類型

```python
# LC 20: Valid Parentheses
# s = "([)]" → False
# s = "{[]}" → True

def isValid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in mapping:
            # 陷阱 1：stack 可能為空（沒有對應的開括號）
            if not stack:
                return False
            top = stack.pop()
            # 陷阱 2：彈出的開括號可能不匹配
            if top != mapping[char]:
                return False
        else:
            stack.append(char)

    # 陷阱 3：遍歷完 stack 可能還有剩餘（多餘的開括號）
    return len(stack) == 0

# 測試 edge cases：
# ""     → True (空字串)
# "("    → False (stack 不空)
# ")"    → False (stack 為空時遇到閉括號)
# "(]"   → False (不匹配)
```

---

# 第九章：Linked List 陷阱

## 陷阱 9.1：Head 被刪除 — 用 Dummy Node

```python
# LC 203: Remove Linked List Elements
# head = [1,2,6,3,4,5,6], val = 6
# 如果 head 自己就要被刪除呢？head = [6,6,1,2]

# 錯誤（不用 dummy）：
def removeElements_WRONG(head, val):
    curr = head
    while curr and curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return head    # ← 如果 head.val == val，head 沒被處理！

# 正確（用 dummy node）：
def removeElements(head, val):
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return dummy.next  # ← dummy.next 才是新的 head

# 口訣：只要 head 可能被刪/改，就用 dummy node
```

## 陷阱 9.2：修改 next 前沒保存 — 鏈斷了

```python
# LC 206: Reverse Linked List
# 1 → 2 → 3 → None

# 錯誤：
def reverse_WRONG(head):
    curr = head
    while curr:
        curr.next = prev      # ← curr.next 被改了！下一個節點找不到了
        prev = curr
        curr = curr.next       # ← curr.next 已經是 prev 了，不是原來的下一個

# 正確：先保存 next
def reverse_CORRECT(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next  # ← 先保存！
        curr.next = prev
        prev = curr
        curr = next_node       # ← 用保存的
    return prev
```

## 陷阱 9.3：快慢指針 — fast.next 可能是 None

```python
# LC 141: Linked List Cycle

# 錯誤：
def hasCycle_WRONG(head):
    slow = fast = head
    while fast:
        slow = slow.next
        fast = fast.next.next    # ← fast.next 可能是 None！
    return False

# 如果 list 長度為偶數且無環：
# 1 → 2 → 3 → 4 → None
# fast 走到 4 時，fast.next = None
# fast.next.next → NoneType has no attribute 'next' → crash！

# 正確：
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:    # ← 檢查 fast AND fast.next
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

## 陷阱 9.4：反轉後忘記斷開原本的 next — 形成環

```python
# LC 92: Reverse Linked List II (反轉 position left 到 right)
# 1 → 2 → 3 → 4 → 5, left=2, right=4
# 結果：1 → 4 → 3 → 2 → 5

# 反轉 2→3→4 變成 4→3→2 後
# 如果 node 2 的 next 還指向 node 3 → 形成 2→3→2→3→... 的環！

# 正確做法：
# 反轉前保存 left 前一個節點 (node 1) 和 left 節點 (node 2)
# 反轉後：
#   node_1.next = 反轉後的頭 (node 4)
#   node_2.next = right 後一個節點 (node 5)

def reverseBetween(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy

    for _ in range(left - 1):
        prev = prev.next

    # prev = node before 'left'
    curr = prev.next            # curr = left node (node 2)

    for _ in range(right - left):
        next_node = curr.next          # next_node = 3 (then 4)
        curr.next = next_node.next     # 2→4 (then 2→5)  ← 斷開！
        next_node.next = prev.next     # 3→2 (then 4→3)
        prev.next = next_node          # prev→3 (then prev→4)

    return dummy.next
```

---

# 第十章：Backtracking 陷阱

## 陷阱 10.1：忘記 undo choice

```python
# 經典 Backtracking 模板：
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])
        return
    for choice in choices:
        path.append(choice)     # Make choice
        backtrack(path, ...)
        path.pop()              # ← Undo choice！忘了這行 → 結果全錯

# 例：Permutations [1,2,3]
# 如果不 pop：
# path 會持續增長：[1,2,3,2,3,1,3,1,2,...]
# 永遠不會回溯，結果完全錯誤

# 完整範例：
def permute(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()         # ← 關鍵！
    backtrack([], nums)
    return result
```

## 陷阱 10.2：path[:] vs path — 所有結果指向同一個 list

```python
# Python 的 list 是 reference type！

# 錯誤：
result.append(path)     # ← 加入的是 path 的「引用」
# 後續 path 被修改時，已加入 result 的也會被改
# 最後 result 裡所有元素都是同一個空 list []

# 正確：
result.append(path[:])  # ← 加入的是 path 的「複製」
# 或
result.append(list(path))
# 或
result.append(path.copy())

# 數值範例：
path = [1, 2, 3]
result = []

# 錯誤：
result.append(path)
path.pop()              # path = [1, 2]
print(result)           # [[1, 2]]  ← result 被連帶修改了！

# 正確：
result.append(path[:])
path.pop()              # path = [1, 2]
print(result)           # [[1, 2, 3]]  ← result 不受影響 ✓
```

## 陷阱 10.3：去重忘記先 sort

```python
# LC 40: Combination Sum II
# candidates = [10,1,2,7,6,1,5], target = 8
# 有重複元素！需要去重

# 去重策略：排序 + 跳過同層重複
# 如果不排序 → 相同的數字不相鄰 → 無法用 candidates[i]==candidates[i-1] 去重

def combinationSum2(candidates, target):
    candidates.sort()          # ← 必須先排序！
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            # 去重：跳過同層重複
            if i > start and candidates[i] == candidates[i-1]:
                continue       # ← 不排序的話這行無效
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

## 陷阱 10.4：start=i vs start=i+1

```python
# Combination Sum（可重複使用）vs Combination Sum II（不可重複使用）

# LC 39: 可重複使用 → 遞迴時傳 start=i
def combinationSum(candidates, target):
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])     # ← start=i（可以重複用自己）
            path.pop()
    candidates.sort()
    backtrack(0, [], target)
    return result

# LC 40: 不可重複使用 → 遞迴時傳 start=i+1
# backtrack(i + 1, path, remaining - candidates[i])  # ← start=i+1（不能重複用自己）

# 搞混的後果：
# i 傳成 i+1 → 少了重複使用的組合（漏答案）
# i+1 傳成 i → 每個元素被無限使用（多答案或 TLE）
```

---

# 第十一章：Python 語言特有陷阱

## 陷阱 11.1：list.sort() vs sorted()

```python
# list.sort() → 原地排序，回傳 None
# sorted()    → 回傳新 list，原 list 不變

nums = [3, 1, 2]

# 錯誤：
result = nums.sort()
print(result)           # None ← 不是排序後的 list！
print(nums)             # [1, 2, 3] ← nums 本身被改了

# 正確用法 1：原地排序（不需要原始順序）
nums.sort()
# nums = [1, 2, 3]

# 正確用法 2：保留原始順序
sorted_nums = sorted(nums)
# sorted_nums = [1, 2, 3], nums = [3, 1, 2]

# 面試中常見 bug：
# intervals.sort(key=lambda x: x[0])  ← 正確，原地排序
# intervals = intervals.sort(...)      ← 錯！intervals 變成 None
```

## 陷阱 11.2：Mutable Default Arguments

```python
# Python 的 default argument 只在函數定義時創建一次！

# 超級危險：
def append_to(element, target=[]):
    target.append(element)
    return target

print(append_to(1))    # [1]
print(append_to(2))    # [1, 2] ← 不是 [2]！用了同一個 list！

# 在 LeetCode 中的場景：
class Solution:
    def dfs(self, node, path=[]):     # ← 危險！
        path.append(node.val)
        # 所有 dfs 調用共用同一個 path list

# 正確：
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

class Solution:
    def dfs(self, node, path=None):
        if path is None:
            path = []
        path.append(node.val)
```

## 陷阱 11.3：Integer Division 負數行為

```python
# Python 的 // 是 floor division（向負無窮取整）
# C++/Java 的 / 是 truncation toward zero（向零取整）

print(7 // 2)       # 3  ← 兩個語言都一樣
print(-7 // 2)      # -4 ← Python（floor toward -inf）
# C++/Java: -7 / 2 = -3（truncate toward 0）

# 如果題目要求向零取整（模擬 C++ 行為）：
result = int(-7 / 2)   # -3 ← 用 int() 截斷

# 或更安全的寫法：
import math
result = math.trunc(-7 / 2)  # -3

# 面試中的坑：
# LC 29: Divide Two Integers 明確要求 truncation toward zero
# 如果用 Python 的 // → 負數結果差 1
```

## 陷阱 11.4：Shallow Copy vs Deep Copy

```python
# 一維 list：path[:] 就夠了
path = [1, 2, 3]
copy = path[:]
copy.append(4)
print(path)       # [1, 2, 3] ← 不受影響 ✓

# 二維 list：[:] 是 shallow copy！內層 list 還是共用的！
matrix = [[1, 2], [3, 4]]
copy = matrix[:]
copy[0][0] = 99
print(matrix)     # [[99, 2], [3, 4]] ← 被修改了！

# 解法：用 deep copy
import copy
matrix = [[1, 2], [3, 4]]
deep = copy.deepcopy(matrix)
deep[0][0] = 99
print(matrix)     # [[1, 2], [3, 4]] ← 不受影響 ✓

# 二維 list 的手動深拷貝（比 deepcopy 快）：
deep = [row[:] for row in matrix]

# 面試中的場景：
# Backtracking 中 path 是二維（如 N-Queens 的棋盤）
# 加入 result 時必須深拷貝
result.append([row[:] for row in board])
```

## 陷阱 11.5：heapq 是 min heap only

```python
import heapq

# Python 的 heapq 只支持 min heap！

# 如果你要 max heap：取反（negate）
nums = [3, 1, 4, 1, 5, 9]
max_heap = [-x for x in nums]
heapq.heapify(max_heap)

# pop 最大值：
largest = -heapq.heappop(max_heap)  # 9

# push 新值：
heapq.heappush(max_heap, -7)

# 常見 bug：
# 忘記取反 → 以為是 max heap 實際是 min heap → 結果完全相反

# 面試中的場景：
# Top K Largest → 用 min heap (size K)
# Top K Smallest → 用 max heap (size K)
# 這很反直覺，但原因是：
# 找最大的 K 個 → 維護一個 min heap，堆頂是 K 個裡最小的
#                  新元素比堆頂大 → 替換 → 堆裡永遠是最大的 K 個

# 如果用 tuple → 按第一個元素排序
heapq.heappush(heap, (distance, node))  # 按 distance 排序
```

## 陷阱 11.6：Dictionary Ordering

```python
# Python 3.7+ dict 保持 insertion order，但面試中建議用 OrderedDict 更明確
from collections import OrderedDict

# LRU Cache 常用 OrderedDict 的專有方法：
# cache.move_to_end(key)        → 移到末尾（最近使用）
# cache.popitem(last=False)     → 移除最早的（LRU eviction）
# 普通 dict 沒有這兩個方法
```

---

# 第十二章：面試中的 Edge Case 提問模板

## 12.1 開始寫 code 之前必須問的問題

```
你聽完題目後，不要馬上寫 code。
花 1-2 分鐘問 clarifying questions。
面試官會非常 appreciate 這個行為。

這不是浪費時間，這是展現 senior engineer 思維。
```

## 12.2 通用提問模板

```
關於輸入：
1. "Can the input be empty?"
   （輸入可以是空的嗎？）

2. "Can there be negative numbers?"
   （有負數嗎？）

3. "Can there be duplicates?"
   （有重複值嗎？）

4. "What's the range of n? And the range of values?"
   （n 的範圍？值的範圍？）

5. "Should I handle integer overflow?"
   （需要處理整數溢出嗎？）

6. "Is the input sorted?"
   （輸入已排序嗎？）

7. "Can I modify the input in-place?"
   （可以原地修改輸入嗎？）
```

## 12.3 按題型的特化提問

```
Array / String：
- "Are all elements positive?"       → 決定能否用 Sliding Window
- "Can the array have length 0?"     → 空陣列處理
- "Are there Unicode characters?"    → 影響字元集大小

Tree：
- "Can the tree be empty (null root)?"
- "Is it a BST or general binary tree?"
- "Can values be negative?"          → 影響 path sum 剪枝
- "Are values unique?"               → 影響搜尋策略

Graph：
- "Is it directed or undirected?"
- "Can there be cycles?"
- "Can there be self-loops?"
- "Is the graph connected?"
- "Can there be duplicate edges?"
- "Are edge weights positive?"       → 決定能否用 Dijkstra

DP：
- "What should I return when input is empty / zero?"
- "Can values be negative?"          → 影響最優子結構

Linked List：
- "Can the list be empty?"
- "Can there be cycles?"
- "Is it singly or doubly linked?"
```

## 12.4 提問後的行動 + 寫完後驗證

```
根據答案調整策略：
- "Yes, negative numbers" → Sliding Window 作廢 → 改 Prefix Sum
- "Graph can be disconnected" → 需要遍歷所有節點作為起點
- "n up to 10^5" → O(n^2) 會 TLE → 必須 O(n log n) 或 O(n)
- "Values 0 to 10^9" → 不能用值當 index → 用 HashMap

寫完 code 後主動測試（不要等面試官提醒）：
"Let me trace through a few edge cases to verify."
→ Step 1: 正常 case  → Step 2: 空輸入  → Step 3: 單元素  → Step 4: 極端值
這段花 2 分鐘，但在面試官心中價值千金。
```

---

# 附錄：Edge Case 速查表（一頁總整理）

```
┌─────────────────────────────────────────────────────────────┐
│                  EDGE CASE 速查表                            │
├──────────────┬──────────────────────────────────────────────┤
│ Binary Search│ 無限循環、off-by-one、空搜尋、重複元素旋轉    │
│              │ check 函數邊界、mid 上取整 vs 下取整          │
├──────────────┼──────────────────────────────────────────────┤
│ Tree         │ 空樹、單節點、偏斜樹、min depth 葉子定義     │
│              │ BST 驗證用 range、path sum 有負數不能剪枝     │
├──────────────┼──────────────────────────────────────────────┤
│ Graph        │ 自環、重複邊、斷開的圖、有向vs無向            │
│              │ Grid 邊界、visited 標記、BFS enqueue 時標記   │
├──────────────┼──────────────────────────────────────────────┤
│ DP           │ dp[0] 初始化、i-1越界、amount=0              │
│              │ 0/1 反向 vs 完全正向、字串 index 偏移 1       │
│              │ Palindrome 填表順序從短到長                   │
├──────────────┼──────────────────────────────────────────────┤
│ Sliding Win  │ 有負數失效、窗口>陣列長、formed 更新時機      │
│              │ shrink 用 while 不是 if                      │
├──────────────┼──────────────────────────────────────────────┤
│ Stack        │ 空 stack pop、Monotonic Stack 方向            │
│              │ Largest Rectangle 剩餘元素、括號 stack 為空   │
├──────────────┼──────────────────────────────────────────────┤
│ Linked List  │ head 被刪用 dummy、改 next 前先保存           │
│              │ fast.next 可能 None、反轉後斷開舊 next        │
├──────────────┼──────────────────────────────────────────────┤
│ Backtracking │ 忘記 pop（undo choice）、path[:] 複製         │
│              │ 去重先 sort、start=i vs i+1                  │
├──────────────┼──────────────────────────────────────────────┤
│ Python       │ sort()=None、mutable default、-7//2=-4       │
│              │ shallow copy 二維危險、heapq min only         │
├──────────────┼──────────────────────────────────────────────┤
│ 通用         │ 空輸入、單元素、全相同、負數、零              │
│              │ 整數溢出、off-by-one、浮點精度                │
│              │ 遍歷中修改集合、遞迴深度                      │
└──────────────┴──────────────────────────────────────────────┘

面試前默念口訣：「空一邊溢特」
空 → 空輸入
一 → 單元素
邊 → 邊界值
溢 → 整數溢出
特 → 特殊值（0, 負數, 重複, inf）
```
