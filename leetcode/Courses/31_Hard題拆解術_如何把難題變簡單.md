# Hard 題拆解術：如何把難題變簡單

> **適用對象**：已學完 01-20 基礎算法、面對 Hard 題會慌的工程師
> **核心主張**：Hard 題不存在，只有多個 Easy/Medium 的組合
> **語言**：繁體中文解說 + English technical terms
> **前置閱讀**：21_從Easy到Hard的進化路線.md、22_解題思考過程_面試官視角.md

---

## 目錄

| 章 | 內容 | 頁內連結 |
|----|------|---------|
| 1 | 核心觀念 — Hard 題不存在 | [第一章](#第一章核心觀念--hard-題不存在只有多個-easymedium-的組合) |
| 2 | 拆解的五種策略 | [第二章](#第二章拆解的五種策略) |
| 3 | 30 道 Hard 題的完整拆解 | [第三章](#第三章30-道-hard-題的完整拆解) |
| 4 | 面試中的拆解溝通 | [第四章](#第四章面試中的拆解溝通) |

---

# 第一章：核心觀念 — Hard 題不存在，只有多個 Easy/Medium 的組合

## 1.1 Google 面試的 Hard 題公式

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Google Hard 題 = Pattern A + Pattern B + 一個 Twist   │
│                                                         │
│   如果你能識別 Pattern A 和 B，                           │
│   Hard 就變成了兩個你已經會的題目。                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

這不是雞湯，這是事實。來看數據：

```
LeetCode Hard 題的組成分析（Top 50 高頻 Hard）

單一算法就能解的 Hard：         ~10%  ← 只是 edge case 多
兩個 Easy pattern 組合的 Hard：  ~55%  ← 最大宗！
一個 Medium + 一個 twist：      ~25%  ← 需要一個巧妙轉換
真正需要新知識的 Hard：          ~10%  ← 極少數

結論：90% 的 Hard 題，你已經會解了，只是不知道怎麼拆。
```

## 1.2 為什麼你覺得 Hard 難？

```
你的大腦看到 Hard 題時的反應：

❌ 錯誤路徑：
  看到題目 → 「我沒見過這題」→ 慌 → 試暴力法 → TLE → 放棄

✅ 正確路徑：
  看到題目 → 「這題由哪些子問題組成？」
           → 識別 Pattern A → 「這個我會！」
           → 識別 Pattern B → 「這個也會！」
           → 組合 A + B → 「原來如此！」
```

核心差異：**你不是在解一道 Hard 題，你是在解兩道 Easy 題。**

## 1.3 拆解的心理模型：像 Debug 一樣解題

你是工程師，你每天都在做 decomposition。

```
工程師的日常                    解 Hard 題
─────────────────────────────────────────────────────
一個大 feature                  一道 Hard 題
  ├── 前端組件 A                  ├── 子問題 A（Easy pattern）
  ├── API endpoint B              ├── 子問題 B（Medium pattern）
  └── DB migration C              └── 組合邏輯（twist）

你不會一次寫完整個 feature，     你也不應該一次想出 Hard 的完整解法。
你會拆成 PR 分開做。             你應該拆成子問題分開想。
```

---

# 第二章：拆解的五種策略

## 策略 1：分層拆解 (Layer Decomposition)

### 核心概念

把問題分成**獨立的步驟**，每步用不同算法。就像蓋房子：先打地基，再砌牆，再蓋屋頂。

```
辨識訊號：
- 問題有明顯的「先...再...」結構
- 某個 intermediate result 可以作為下一步的 input
- 問題可以分成 preprocessing + main logic + postprocessing
```

### 範例 A：LC 84 Largest Rectangle in Histogram (Hard)

```
原問題：在 histogram 中找最大矩形面積

拆解思路：對每個 bar，如果我知道它能向左延伸多遠、向右延伸多遠，
         就能算出以它為高的最大矩形。

子問題 A：對每個 bar，找左邊第一個更矮的 bar
  → 這就是「找前一個更小元素」→ Monotonic Stack (Easy pattern!)

子問題 B：對每個 bar，找右邊第一個更矮的 bar
  → 同上，反方向的 Monotonic Stack (Easy pattern!)

組合：
  width[i] = right_boundary[i] - left_boundary[i] - 1
  area[i] = heights[i] × width[i]
  answer = max(area[i]) for all i

拆解結果：LC 84 = 2 次 Monotonic Stack + 1 次線性掃描
```

```python
def largestRectangleArea(heights):
    n = len(heights)
    left = [-1] * n   # 子問題 A: 左邊第一個更矮的 index
    right = [n] * n    # 子問題 B: 右邊第一個更矮的 index

    # --- Layer 1: Monotonic Stack 找左邊界 ---
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # --- Layer 2: Monotonic Stack 找右邊界 ---
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # --- Layer 3: 組合計算 ---
    return max(heights[i] * (right[i] - left[i] - 1) for i in range(n))
```

### 範例 B：LC 85 Maximal Rectangle (Hard)

```
原問題：在 0/1 matrix 中找最大全 1 矩形

拆解思路：如果我把每一行看作 histogram 的底部，
         問題就變成「對每行求最大矩形」！

子問題 A：把 2D matrix 轉成逐行的 histogram
  → 簡單的累加掃描（Easy!）
  → 如果 matrix[i][j] == '1'，histogram[j] += 1，否則 histogram[j] = 0

子問題 B：對每行的 histogram 求最大矩形
  → 這就是 LC 84！我們剛剛解過了！

拆解結果：LC 85 = 行掃描 O(m×n) + m 次 LC 84 O(n) = O(m×n)
```

```python
def maximalRectangle(matrix):
    if not matrix:
        return 0
    cols = len(matrix[0])
    histogram = [0] * cols
    max_area = 0

    for row in matrix:
        # --- Layer 1: 建立這一行的 histogram ---
        for j in range(cols):
            histogram[j] = histogram[j] + 1 if row[j] == '1' else 0

        # --- Layer 2: 套用 LC 84 ---
        max_area = max(max_area, largestRectangleArea(histogram))

    return max_area
```

### 範例 C：LC 234 Palindrome Linked List (Medium)

```
原問題：判斷 linked list 是否為 palindrome（O(1) space）

子問題 A：找中點 → Fast-Slow Pointers (Easy!)
子問題 B：反轉後半段 → Reverse Linked List (Easy! LC 206)
子問題 C：比較前後兩段 → 簡單遍歷 (Easy!)

拆解結果：三個 Easy 題的組合
```

### 策略 1 的辨識口訣

```
「這道題需要什麼 intermediate result？」
「如果有人先幫我算好 X，這題就變簡單了嗎？」
→ 如果是，X 就是你的子問題。
```

---

## 策略 2：抽象轉換 (Abstraction / Reduction)

### 核心概念

把問題**轉換**成你已經認識的問題。就像數學的「令 x =...」，把陌生的方程式變成熟悉的形式。

```
辨識訊號：
- 問題「長得不像」任何你認識的 pattern，但「感覺上」跟某個 pattern 很像
- 問題有隱藏的結構（隱式圖、隱式的狀態轉移）
- 改變問題的「觀看角度」可以簡化問題
```

### 範例 A：LC 416 Partition Equal Subset Sum (Medium)

```
原問題：能否把陣列分成兩個子集，使兩邊的和相等？

轉換鏈：
  Step 1: 兩邊和相等 → 每邊的和 = total / 2
  Step 2: 如果 total 是奇數 → 直接 return False
  Step 3: 問題變成：能否找到子集，使其和 = total / 2？
  Step 4: 這就是 0/1 Knapsack Problem！
    - 每個數字就是一個「物品」
    - 物品的 weight = value = nums[i]
    - 背包容量 = total / 2
    - 問的是：能不能剛好裝滿？

拆解結果：數學觀察（total/2）+ 0/1 Knapsack DP
```

```python
def canPartition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2

    # 標準 0/1 Knapsack
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):  # 反向遍歷！
            dp[j] = dp[j] or dp[j - num]
    return dp[target]
```

### 範例 B：LC 287 Find the Duplicate Number (Medium)

```
原問題：n+1 個數字，值在 [1, n]，找出重複的那個（不能改陣列，O(1) space）

轉換鏈：
  Step 1: 把 index → value 看作 node → next pointer
    - index 0 的值是 nums[0]，所以 node 0 指向 node nums[0]
    - index 1 的值是 nums[1]，所以 node 1 指向 node nums[1]
  Step 2: 因為有重複值，所以有兩個不同的 index 指向同一個 node → 形成環！
  Step 3: 找環的入口 = 找重複的數字 → Floyd's Cycle Detection

拆解結果：Array → 隱式 Linked List 的轉換 + Floyd's Algorithm
```

```python
def findDuplicate(nums):
    # Phase 1: Floyd's - 找到環中的相遇點
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: 找環的入口
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

### 範例 C：LC 127 Word Ladder (Hard)

```
原問題：從 word A 到 word B，每次只能改一個字母，最少幾步？

轉換鏈：
  Step 1: 每個 word 是一個 node
  Step 2: 兩個 word 如果只差一個字母 → 它們之間有一條 edge
  Step 3: 「最少幾步」= 無權圖的最短路徑 → BFS！

拆解結果：建立隱式圖 + BFS
```

```python
from collections import deque

def ladderLength(beginWord, endWord, wordList):
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, steps = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word == endWord:
                    return steps + 1
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, steps + 1))
    return 0
```

### 策略 2 的辨識口訣

```
「這個問題換個角度看，像不像我認識的某個問題？」
「如果我把 X 當成 Y 來看待...」
→ Array 當 Linked List、Word 當 Graph Node、Subset Sum 當 Knapsack
```

---

## 策略 3：增加維度 (Dimension Extension)

### 核心概念

你已經會 1D 版本，現在要解 2D 版本。秘訣是：**固定一個維度，對另一個維度套用 1D 解法。**

```
辨識訊號：
- 題目明顯是某個經典題的 2D 版本
- Input 從 array 變成 matrix
- 從「一個變數」變成「兩個變數」
```

### 經典的維度擴展對照表

```
1D → 2D 進化對照
──────────────────────────────────────────────────────────────────
LC 53  Maximum Subarray        →  LC 363 Max Sum of Rectangle ≤ K
  1D Kadane's Algorithm            固定 top/bottom 兩行 + 壓成 1D + Kadane's

LC 84  Largest Rect in Hist    →  LC 85  Maximal Rectangle
  1D Monotonic Stack               逐行建 histogram + 套 LC 84

LC 1   Two Sum                 →  LC 15  3Sum
  HashMap O(n)                     固定一個元素 + Two Pointers O(n²)

LC 121 Best Time Buy/Sell I    →  LC 123 Best Time Buy/Sell III (2 transactions)
  一次交易 dp                       兩次交易 → 狀態機 DP

LC 70  Climbing Stairs          →  LC 62  Unique Paths
  1D DP                             2D DP (m×n grid)

LC 300 Longest Increasing Sub  →  LC 354 Russian Doll Envelopes
  1D LIS (dp 或 patience sort)      Sort by width + LIS on height
```

### 維度擴展的通用模板

```python
# 1D 版本
def solve_1d(arr):
    # 你已經會的算法
    pass

# 2D 版本
def solve_2d(matrix):
    m, n = len(matrix), len(matrix[0])
    result = 初始值

    for i in range(m):          # 固定一個維度
        compressed = [0] * n    # 壓成 1D
        for j in range(i, m):   # 枚舉另一個維度
            for k in range(n):
                compressed[k] += matrix[j][k]  # 壓縮
            result = max(result, solve_1d(compressed))  # 套用 1D 解法

    return result
```

### 策略 3 的辨識口訣

```
「這題是不是某個 1D 經典題的 2D 版本？」
「如果我固定一個維度，能不能降回 1D？」
→ 固定行 / 固定列 / 固定一個元素 → 對剩下的套 1D 解法
```

---

## 策略 4：條件放寬 (Constraint Relaxation)

### 核心概念

先解決**沒有某個約束**的簡單版本，再把約束加回去。就像學游泳：先在淺水區學會動作，再去深水區。

```
辨識訊號：
- 題目是某個經典題的「加強版」
- 多了一個條件（circular、duplicates、negative numbers）
- 去掉那個條件後，題目就是你會的
```

### 範例 A：LC 213 House Robber II (Medium → Circular)

```
約束：房屋排成一圈（首尾相連）
放寬：如果房屋排成一排呢？→ 那就是 LC 198 House Robber (Easy!)

加回約束：
  如果選了 house[0]，就不能選 house[n-1]
  如果選了 house[n-1]，就不能選 house[0]

  → 拆成兩個線性問題：
    Case A: 考慮 house[0..n-2]（不考慮最後一間）
    Case B: 考慮 house[1..n-1]（不考慮第一間）
    答案 = max(Case A, Case B)

拆解結果：LC 213 = 2 次 LC 198
```

```python
def rob(nums):
    if len(nums) == 1:
        return nums[0]

    def rob_linear(houses):  # LC 198
        prev, curr = 0, 0
        for h in houses:
            prev, curr = curr, max(curr, prev + h)
        return curr

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### 範例 B：LC 81 Search in Rotated Sorted Array II (with duplicates)

```
約束：有重複元素
放寬：如果沒有重複呢？→ 那就是 LC 33 (Medium)

加回約束：
  原本 nums[left] < nums[mid] 可以確定左半有序
  但現在 nums[left] == nums[mid] 時，無法判斷！

  → 處理方式：當 nums[left] == nums[mid] 時，left += 1（跳過）
  → 最壞情況從 O(log n) 退化為 O(n)，但大多數情況仍是 O(log n)

拆解結果：LC 81 = LC 33 + 一行 edge case 處理
```

### 範例 C：LC 123 Best Time to Buy and Sell Stock III (at most 2 transactions)

```
約束：最多做 2 次交易
放寬：如果只做 1 次交易？→ 那就是 LC 121 (Easy!)

加回約束：
  方法 1（分層拆解）：
    對每個分割點 i，左邊做一次最佳交易 + 右邊做一次最佳交易
    left_profit[i] = LC 121 on prices[0..i]
    right_profit[i] = LC 121 on prices[i..n-1]（反向）
    答案 = max(left_profit[i] + right_profit[i])

  方法 2（狀態機 DP）：
    追蹤 4 個狀態：buy1, sell1, buy2, sell2

拆解結果：LC 123 = 2 次 LC 121 + 枚舉分割點
```

### 策略 4 的辨識口訣

```
「這題跟哪個經典題很像？多了什麼條件？」
「如果把那個條件去掉，我會解嗎？」
「怎麼把那個條件加回去？需要改哪裡？」
```

---

## 策略 5：反向思考 (Reverse Thinking)

### 核心概念

正面很難想，那就**從答案倒推**。反過來想，問題可能會簡單得多。

```
辨識訊號：
- 正向枚舉狀態太多、組合爆炸
- 「找 X」很難，但「找不是 X 的」很簡單
- 「先做什麼」很難決定，但「最後做什麼」很容易分析
```

### 範例 A：LC 130 Surrounded Regions

```
正向思考：找出所有被 X 包圍的 O → 要判斷每個 O 區域是否完全被包圍 → 複雜

反向思考：找出所有「不被包圍」的 O → 從邊界開始 DFS → 超級簡單！
         剩下的 O 就是被包圍的。

步驟：
  1. 從四邊邊界上的所有 O 開始 DFS/BFS
  2. 標記所有能從邊界到達的 O 為 'S' (safe)
  3. 遍歷整個 matrix：O → X（被包圍），S → O（恢復）
```

### 範例 B：LC 42 Trapping Rain Water (Hard)

```
正向思考：計算整體能存多少水 → 不知道從哪下手

反向思考（逐格計算）：
  每個位置能存多少水？
  water[i] = min(左邊最高的牆, 右邊最高的牆) - height[i]

  子問題 A：left_max[i] = max(heights[0..i])  → 一次左掃描
  子問題 B：right_max[i] = max(heights[i..n-1]) → 一次右掃描
  組合：water[i] = max(0, min(left_max[i], right_max[i]) - heights[i])
```

```python
def trap(height):
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])

    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
```

### 範例 C：LC 312 Burst Balloons (Hard)

```
正向思考：先戳哪個氣球？→ 每戳一個，鄰居就改變 → 組合爆炸！

反向思考：最後戳哪個氣球？
  如果 balloon[k] 是最後被戳的，那麼：
  - 它左邊的氣球已經全部戳完了（子問題：left part）
  - 它右邊的氣球已經全部戳完了（子問題：right part）
  - 最後戳 k 的收益 = nums[left] × nums[k] × nums[right]

  → 這就是區間 DP！dp[i][j] = 戳完 (i,j) 之間所有氣球的最大收益

拆解結果：反向思考 + 區間 DP
```

```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):          # 區間長度
        for i in range(n - length):     # 區間起點
            j = i + length              # 區間終點
            for k in range(i + 1, j):   # 最後戳的氣球
                dp[i][j] = max(dp[i][j],
                    dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])

    return dp[0][n-1]
```

### 策略 5 的辨識口訣

```
「正面想很複雜？那反過來呢？」
「找 X 很難？那找 not X 呢？」
「先做什麼很難決定？那最後做什麼呢？」
```

---

## 五種策略速查表

```
┌─────────────────────────────────────────────────────────────────┐
│  策略           辨識訊號                     典型題目            │
├─────────────────────────────────────────────────────────────────┤
│  1.分層拆解     有明顯先後步驟               LC 84/85/234       │
│  2.抽象轉換     「像」某個已知問題            LC 287/416/127     │
│  3.增加維度     1D 經典題的 2D 版            LC 85/363/354      │
│  4.條件放寬     經典題 + 額外約束            LC 81/213/123      │
│  5.反向思考     正向組合爆炸                 LC 42/130/312      │
├─────────────────────────────────────────────────────────────────┤
│  口訣：層 → 轉 → 維 → 寬 → 反                                  │
│  「先拆層，再轉換，看維度，放條件，反著想」                        │
└─────────────────────────────────────────────────────────────────┘
```

---

# 第三章：30 道 Hard 題的完整拆解

每道題按統一格式呈現：

```
格式說明：
  [第一反應] → 看到題目時的直覺判斷
  [拆解策略] → 使用哪種策略
  [子問題]   → 拆成哪些子問題
  [算法]     → 每個子問題用什麼算法
  [組合]     → 如何將子問題的結果組合成最終答案
```

---

## 3.1 LC 4 Median of Two Sorted Arrays (Hard)

```
題意：兩個 sorted arrays，找合併後的中位數，要求 O(log(m+n))

[第一反應] sorted + O(log) → Binary Search
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  A: 「找中位數」→ 轉換成「找第 k 小的元素」(k = (m+n)/2)
  B: 「在兩個 sorted arrays 找第 k 小」→ Binary Search 比較兩邊第 k/2 個
[算法]
  A: 數學轉換
  B: Binary Search — 每次排除 k/2 個元素
[組合]
  如果 (m+n) 是奇數：findKth(k=(m+n)/2+1)
  如果 (m+n) 是偶數：(findKth(k/2) + findKth(k/2+1)) / 2

Time: O(log(m+n)), Space: O(log(m+n)) for recursion
```

---

## 3.2 LC 10 Regular Expression Matching (Hard)

```
題意：實現 regex matching，支援 '.' 和 '*'

[第一反應] 字串匹配 + 特殊字元 → DP 或 Backtracking
[拆解策略] 策略 4 — 條件放寬
[子問題]
  放寬 1: 如果沒有 '*'？→ 簡單逐字比對，'.' 匹配任意字元
  放寬 2: 加回 '*'？→ 'x*' 可以匹配 0 次或多次
    - 匹配 0 次：dp[i][j] = dp[i][j+2]（跳過 x*）
    - 匹配 1+ 次：dp[i][j] = dp[i-1][j] if s[i-1] matches p[j]
[算法] 2D DP，dp[i][j] = s[0..i-1] 是否匹配 p[0..j-1]
[組合]
  base case: dp[0][0] = True
  遞推：分 p[j-1] 是否為 '*' 兩種情況

Time: O(m×n), Space: O(m×n)
```

---

## 3.3 LC 23 Merge K Sorted Lists (Hard)

```
題意：合併 k 個 sorted linked lists

[第一反應] 合併兩個是 Easy (LC 21)，k 個就重複做？
[拆解策略] 策略 1 — 分層拆解
[子問題]
  方法 A（Divide and Conquer）：
    子問題：兩兩合併 → LC 21 Merge Two Sorted Lists (Easy!)
    組合：log(k) 輪，每輪合併一半的 lists

  方法 B（Min Heap）：
    子問題 1：建 min heap 放 k 個 list 的頭節點
    子問題 2：每次 pop 最小的，加入它的 next
    → 這就是 Heap 的基本操作 (Easy!)
[算法] Divide & Conquer 或 Min Heap
[組合]
  D&C: 遞迴合併
  Heap: 持續 pop + push 直到 heap 為空

Time: O(N log k), Space: O(k) for heap
```

---

## 3.4 LC 25 Reverse Nodes in K-Group (Hard)

```
題意：每 k 個 node 一組反轉 linked list

[第一反應] 反轉 linked list 我會 (LC 206)，每次反轉 k 個就好
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 數 k 個 node（是否夠一組）→ 遍歷計數 (Easy)
  B: 反轉一段 linked list → LC 206 的變體 (Easy)
  C: 將反轉後的段接回原鏈 → 指標操作 (Easy)
[算法] 三個 Easy 操作的迭代/遞迴
[組合] 重複：數 k 個 → 反轉 → 接回 → 移動到下一段

Time: O(n), Space: O(1) iterative / O(n/k) recursive
```

---

## 3.5 LC 32 Longest Valid Parentheses (Hard)

```
題意：找最長有效括號子串的長度

[第一反應] 括號 → Stack；最長 → DP？兩個方向都能解
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  方法 A（Stack）：
    轉換：stack 不只存括號，還存 index
    用 stack 底部元素作為「上一個無效位置」

  方法 B（DP）：
    dp[i] = 以 s[i] 結尾的最長有效括號長度
    s[i]=='(' → dp[i]=0
    s[i]==')' → 找它匹配的 '(' 在哪裡
[算法] Stack with index 或 1D DP
[組合] Stack: 每次匹配成功時更新 max_len = i - stack[-1]

Time: O(n), Space: O(n)
```

---

## 3.6 LC 41 First Missing Positive (Hard)

```
題意：未排序陣列，找最小的缺失正整數，O(n) time + O(1) space

[第一反應] 排序？O(n log n)。HashSet？O(n) space。都不行！
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  轉換：把 array 本身當作 HashSet！
  nums[i] 應該放在 index nums[i]-1 的位置
  → 這就是 Cyclic Sort pattern！
[算法]
  Step 1: Cyclic Sort — 把每個數放到「正確位置」
  Step 2: 線性掃描 — 找第一個 nums[i] != i+1 的位置
[組合] Cyclic Sort + 線性掃描

Time: O(n), Space: O(1)
```

---

## 3.7 LC 42 Trapping Rain Water (Hard)

```
題意：計算 elevation map 能接多少雨水

[第一反應] 跟 histogram 有關？像 LC 84？
[拆解策略] 策略 5 — 反向思考（逐格計算）
[子問題]
  核心觀察：water[i] = min(left_max[i], right_max[i]) - height[i]
  A: 預計算每個位置的 left_max → 左掃描 O(n)
  B: 預計算每個位置的 right_max → 右掃描 O(n)
  C: 逐格計算水量 → 線性掃描 O(n)
[算法] 前綴最大值 + 後綴最大值 + 線性掃描
[組合] 三次 O(n) 掃描

進階：Two Pointers 做到 O(1) space
  左右指標向中間移動，每次移動較矮的一邊

Time: O(n), Space: O(n) 或 O(1)
```

---

## 3.8 LC 44 Wildcard Matching (Hard)

```
題意：實現 wildcard matching，'?' 匹配單字元，'*' 匹配任意序列

[第一反應] 跟 LC 10 很像！String matching → DP
[拆解策略] 策略 4 — 條件放寬
[子問題]
  放寬 1: 沒有 '*' 和 '?'？→ 逐字比對
  放寬 2: 加回 '?'？→ '?' 匹配任何單一字元，簡單
  放寬 3: 加回 '*'？→ '*' 匹配任意序列
    - 匹配 0 個字元：dp[i][j] = dp[i][j-1]
    - 匹配 1+ 個字元：dp[i][j] = dp[i-1][j]
[算法] 2D DP，dp[i][j] = s[0..i-1] 是否匹配 p[0..j-1]
[組合] 與 LC 10 類似但更簡單（'*' 不需要跟前一個字元綁定）

Time: O(m×n), Space: O(m×n)
```

---

## 3.9 LC 51 N-Queens (Hard)

```
題意：在 N×N 棋盤上放 N 個皇后，使它們互不攻擊

[第一反應] 放置 + 限制條件 → Backtracking
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 逐行放置（每行恰好放一個皇后）→ 決定每行放在哪一列
  B: 合法性檢查：同列？同對角線？同反對角線？
     - 同列：col_used set
     - 主對角線：row - col 相同 → diag_used set
     - 反對角線：row + col 相同 → anti_diag_used set
  C: 回溯：放不下就退回上一行
[算法] Backtracking + 三個 Set 做 O(1) 合法性檢查
[組合] 逐行嘗試每一列 → 檢查合法 → 遞迴下一行 → 回溯

Time: O(N!), Space: O(N²)
```

---

## 3.10 LC 72 Edit Distance (Hard)

```
題意：word1 變成 word2 的最少操作次數（insert、delete、replace）

[第一反應] 兩個字串 + 最少操作 → 經典 2D DP
[拆解策略] 策略 4 — 條件放寬
[子問題]
  放寬：如果只允許 insert？→ 就是 LCS 的變體
  加回：三種操作都允許時，每步有三個選擇

  dp[i][j] = word1[0..i-1] 變成 word2[0..j-1] 的最少操作
  如果 word1[i-1] == word2[j-1]：dp[i][j] = dp[i-1][j-1]
  否則：dp[i][j] = 1 + min(
    dp[i-1][j],      // delete
    dp[i][j-1],      // insert
    dp[i-1][j-1]     // replace
  )
[算法] 2D DP
[組合] 填表 → 右下角就是答案

Time: O(m×n), Space: O(m×n) 可優化到 O(n)
```

---

## 3.11 LC 76 Minimum Window Substring (Hard)

```
題意：在 s 中找包含 t 所有字元的最短子串

[第一反應] 子串 + 最短 → Sliding Window
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 用 HashMap 統計 t 中每個字元的需求量
  B: 擴張右邊界直到窗口滿足所有需求（標準 Sliding Window expand）
  C: 收縮左邊界找最小窗口（標準 Sliding Window shrink）
  D: 用 formed 計數器追蹤已滿足的字元數量
[算法] Sliding Window + HashMap（兩個 Easy pattern 的組合）
[組合] 外層右移 right，內層嘗試左移 left，同時維護 window counts

Time: O(|s| + |t|), Space: O(|s| + |t|)
```

---

## 3.12 LC 84 Largest Rectangle in Histogram (Hard)

```
（詳見第二章策略 1 的完整拆解）

[第一反應] 每個 bar 為高，找最寬 → 需要快速找左右邊界
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 找每個 bar 的左邊界 → Monotonic Stack
  B: 找每個 bar 的右邊界 → Monotonic Stack
  C: 計算面積 → 線性掃描
[算法] 2 次 Monotonic Stack + 線性掃描
[組合] area[i] = heights[i] × (right[i] - left[i] - 1)

Time: O(n), Space: O(n)
```

---

## 3.13 LC 85 Maximal Rectangle (Hard)

```
（詳見第二章策略 1 & 3 的完整拆解）

[第一反應] 2D 矩形 → 能不能降維到 1D？
[拆解策略] 策略 3 — 增加維度（LC 84 的 2D 版本）
[子問題]
  A: 逐行建 histogram → 線性掃描
  B: 每行套 LC 84 → Monotonic Stack
[算法] 行掃描 + LC 84
[組合] 逐行累加 histogram，每行求一次最大矩形

Time: O(m×n), Space: O(n)
```

---

## 3.14 LC 124 Binary Tree Maximum Path Sum (Hard)

```
題意：找 binary tree 中的最大路徑和（路徑可以不經過 root）

[第一反應] Tree + 最大 → DFS + 某種 max 計算
[拆解策略] 策略 1 — 分層拆解
[子問題]
  核心觀察：對每個 node，它能貢獻的路徑有兩種：
    A: 作為「彎曲點」的路徑：left + node + right（不能再往上）
    B: 作為「直線段」向上延伸：node + max(left, right)

  DFS 返回 B（可以向上延伸的最大值）
  在過程中用 global max 記錄 A（包含彎曲路徑的最大值）
[算法] Post-order DFS
[組合]
  對每個 node：
    left_gain = max(0, dfs(node.left))
    right_gain = max(0, dfs(node.right))
    global_max = max(global_max, node.val + left_gain + right_gain)
    return node.val + max(left_gain, right_gain)

Time: O(n), Space: O(h) where h = tree height
```

---

## 3.15 LC 127 Word Ladder (Hard)

```
（詳見第二章策略 2 的完整拆解）

[第一反應] 最短轉換序列 → BFS？但在哪裡 BFS？
[拆解策略] 策略 2 — 抽象轉換（words → implicit graph）
[子問題]
  A: 建立隱式圖 — word 是 node，差一字母是 edge
  B: BFS 找最短路徑
[算法] Implicit Graph + BFS
[組合] 對每個 word 嘗試改每一位，如果在 wordList 中就是鄰居

Time: O(M² × N) where M = word length, N = wordList size
```

---

## 3.16 LC 128 Longest Consecutive Sequence (Hard)

```
題意：未排序陣列找最長連續序列，O(n) time

[第一反應] O(n) 不能排序 → HashSet
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  轉換：只從「序列起點」開始計數
  如果 num-1 不在 set 中 → num 是某個序列的起點
  A: 建 HashSet → O(n)
  B: 對每個起點，向右延伸計數 → 均攤 O(n)
[算法] HashSet + 智慧枚舉
[組合]
  for num in nums:
      if num - 1 not in s:  # 是起點
          count consecutive from num

Time: O(n), Space: O(n)
```

---

## 3.17 LC 212 Word Search II (Hard)

```
題意：在 2D board 上找出所有給定單詞

[第一反應] 搜索多個 word → 一個一個搜太慢 → 需要 Trie
[拆解策略] 策略 1 — 分層拆解 + 策略 2 — 抽象轉換
[子問題]
  A: 把所有 words 建成 Trie → 標準 Trie 操作
  B: 從 board 每個格子 DFS，同時在 Trie 上走 → DFS + Trie 結合
  C: 剪枝：Trie node 沒有對應子節點時回溯
[算法] Trie + DFS/Backtracking
[組合] DFS 在 board 上走的同時，在 Trie 上走 → 一次 DFS 找所有 words

Time: O(M×N × 4^L) where L = max word length,
      but Trie pruning makes it much faster in practice
```

---

## 3.18 LC 239 Sliding Window Maximum (Hard)

```
題意：size 為 k 的 sliding window 的最大值

[第一反應] Sliding Window + 最大值 → 需要高效取 max → Monotonic Deque
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 維護一個 monotonic decreasing deque
  B: 窗口滑動時：
     - 左端移出：如果 deque front 是要移出的元素，pop front
     - 右端加入：從 back 移除所有比新元素小的 → push back
     - 取 max：deque front 就是當前窗口最大值
[算法] Monotonic Deque（Deque 的 Easy 操作組合）
[組合] 滑動窗口 + deque 維護

Time: O(n), Space: O(k)
```

---

## 3.19 LC 269 Alien Dictionary (Hard)

```
題意：給定外星語言排序的字典，推導字母順序

[第一反應] 字母順序 → 相對順序 → 有向圖 → Topological Sort
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  A: 從相鄰 word pair 推導字母間的順序關係
     → 比較兩個相鄰 word，第一個不同的字母給出一條有向邊
  B: 建有向圖 → Adjacency List
  C: Topological Sort → BFS (Kahn's) 或 DFS
  D: 偵測矛盾（有環 → return ""）
[算法] Graph Building + Topological Sort
[組合]
  提取邊 → 建圖 → Topo Sort → 檢查是否所有節點都被訪問

Time: O(C) where C = total characters in all words
```

---

## 3.20 LC 295 Find Median from Data Stream (Hard)

```
題意：支持插入數字和取中位數的資料結構

[第一反應] 維護有序結構 + 快速取中間 → 兩個 Heap
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: Max Heap 存較小的一半
  B: Min Heap 存較大的一半
  C: 平衡兩個 heap（大小差不超過 1）
  D: 中位數 = max_heap 的 top（或兩個 top 的平均）
[算法] 兩個 Heap（都是 Easy 的 heap 操作）
[組合]
  addNum: 加到 max_heap → 平衡到 min_heap → 再平衡
  findMedian: 看兩個 heap 的 top

Time: O(log n) insert, O(1) query, Space: O(n)
```

---

## 3.21 LC 297 Serialize and Deserialize Binary Tree (Hard)

```
題意：將 binary tree 序列化成字串，再反序列化回來

[第一反應] Tree 遍歷 → Preorder/BFS 都行
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: Serialize — Preorder DFS，null 用特殊符號（如 "#"）
  B: Deserialize — 按同樣的 Preorder 順序重建
     用 iterator/index 逐個讀取值，遇到 "#" 返回 None
[算法] Preorder DFS（兩個方向各做一次）
[組合] 序列化與反序列化使用相同的遍歷順序

Time: O(n), Space: O(n)
```

---

## 3.22 LC 312 Burst Balloons (Hard)

```
（詳見第二章策略 5 的完整拆解）

[第一反應] 每戳一個氣球鄰居改變 → 狀態太多 → 需要反向思考
[拆解策略] 策略 5 — 反向思考
[子問題]
  反向：最後戳哪個？→ 左右兩邊已經戳完 → 區間 DP
  dp[i][j] = 戳完 (i, j) 之間所有氣球的最大收益
  枚舉最後戳的 k：dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])
[算法] 區間 DP
[組合] 從小區間到大區間填表

Time: O(n³), Space: O(n²)
```

---

## 3.23 LC 315 Count of Smaller Numbers After Self (Hard)

```
題意：對每個元素，計算右邊比它小的元素個數

[第一反應] 暴力 O(n²) → 需要更快 → Merge Sort or BIT
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  方法 A（Merge Sort）：
    轉換：Merge Sort 在 merge 時，自然知道「右邊有幾個比左邊小」
    merge 時，如果右邊元素先被取出，代表它比左邊剩餘的都小

  方法 B（BIT / Fenwick Tree）：
    從右往左掃描，每個數插入 BIT
    查詢 BIT 中比當前數小的有幾個
[算法] Modified Merge Sort 或 Binary Indexed Tree
[組合] Merge Sort: 在合併時累計 count；BIT: 插入 + 前綴查詢

Time: O(n log n), Space: O(n)
```

---

## 3.24 LC 329 Longest Increasing Path in a Matrix (Hard)

```
題意：在 matrix 中找最長嚴格遞增路徑

[第一反應] Matrix + 路徑 → DFS；最長 → 需要記憶化
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 從每個格子出發 DFS → 標準 4 方向 DFS
  B: 記憶化避免重複計算 → Memoization (dp[i][j])
  C: 不需要 visited 標記！因為嚴格遞增保證不會走回頭路
[算法] DFS + Memoization (Top-down DP)
[組合]
  dp[i][j] = 1 + max(dfs(nx, ny)) for valid neighbors (nx, ny)
  answer = max(dp[i][j]) for all (i, j)

Time: O(m×n), Space: O(m×n)
```

---

## 3.25 LC 336 Palindrome Pairs (Hard)

```
題意：找出所有 (i,j) 使得 words[i]+words[j] 是 palindrome

[第一反應] 暴力 O(n² × k) → 需要優化 → Trie 或 HashMap
[拆解策略] 策略 1 — 分層拆解
[子問題]
  核心觀察：words[i] + words[j] 是 palindrome 的三種情況：
    Case 1: words[j] 是 words[i] 的反轉 → HashMap 查找
    Case 2: words[i] 較長，words[i] 的前綴反轉 = words[j]，且 words[i] 剩餘部分是 palindrome
    Case 3: words[j] 較長，對稱版本
  A: 建 HashMap: {reversed_word: index}
  B: 對每個 word 枚舉分割點，檢查上述三種情況
[算法] HashMap + Palindrome Check + String Split
[組合] 三種 case 分別處理，注意去重

Time: O(n × k²) where k = average word length
```

---

## 3.26 LC 410 Split Array Largest Sum (Hard)

```
題意：把 array 分成 m 段，最小化「各段之和的最大值」

[第一反應] 最小化最大值 → Binary Search on Answer！
[拆解策略] 策略 2 — 抽象轉換
[子問題]
  轉換：「分成 m 段使最大和最小」
    → 等價於「給定上限 mid，能否把 array 分成 ≤ m 段，使每段和 ≤ mid？」

  A: Binary Search on answer space [max(nums), sum(nums)]
  B: Greedy check：給定 mid，貪心地分段（能不超過 mid 就往後加）
[算法] Binary Search + Greedy Validation
[組合]
  lo, hi = max(nums), sum(nums)
  while lo < hi:
      mid = (lo + hi) // 2
      if can_split(mid, m): hi = mid    # 可以分 → 試更小的上限
      else: lo = mid + 1                # 不行 → 放寬上限

Time: O(n × log(sum - max)), Space: O(1)
```

---

## 3.27 LC 432 All O'one Data Structure (Hard)

```
題意：支持 inc(key), dec(key), getMaxKey(), getMinKey() 全部 O(1)

[第一反應] 全 O(1) → 不能用 heap → 需要 Doubly Linked List + HashMap
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: HashMap: key → count（查找 key 的計數）
  B: HashMap: key → node pointer（定位 key 所在的 DLL node）
  C: Doubly Linked List：每個 node 代表一個 count 值，存該 count 的所有 keys
     - 按 count 排序 → head 是 min, tail 是 max
  D: inc/dec 時把 key 從一個 node 移到相鄰 node
[算法] DLL + 兩個 HashMap（都是 Easy 的資料結構操作）
[組合] HashMap 做 O(1) 查找 + DLL 做 O(1) 移動和取 min/max

Time: all operations O(1), Space: O(n)
```

---

## 3.28 LC 460 LFU Cache (Hard)

```
題意：實現 Least Frequently Used Cache，get 和 put 都 O(1)

[第一反應] LRU 我會 (LC 146)，LFU 加了 frequency → 多一層結構
[拆解策略] 策略 4 — 條件放寬
[子問題]
  放寬：如果不考慮 frequency？→ 那就是 LRU (LC 146, Medium)
  加回 frequency：
    A: HashMap: key → value（基本查找）
    B: HashMap: key → frequency（追蹤使用頻率）
    C: HashMap: frequency → OrderedDict / DLL（每個頻率一個 LRU list）
    D: 維護 min_freq（快速找到最小頻率）
[算法] 3 個 HashMap + min_freq 變數（LRU 的強化版）
[組合]
  get: 更新 freq, 從舊 freq list 移到新 freq list
  put: 如果滿了 → 移除 min_freq list 的 LRU 元素

Time: O(1) for all operations, Space: O(capacity)
```

---

## 3.29 LC 787 Cheapest Flights Within K Stops (Hard)

```
題意：最多 k 次轉機，從 src 到 dst 的最便宜航班

[第一反應] 最短路徑 + 限制步數 → Modified BFS or Bellman-Ford
[拆解策略] 策略 4 — 條件放寬
[子問題]
  放寬：沒有 k 次限制？→ 那就是 Dijkstra（Medium pattern）
  加回 k 次限制：
    方法 A: Bellman-Ford 跑 k+1 輪（天然支持步數限制）
    方法 B: BFS with level limit（最多走 k+1 層）
    方法 C: Modified Dijkstra with (cost, city, stops_left) state
[算法] Bellman-Ford（最直觀）或 BFS with pruning
[組合]
  for i in range(k + 1):      # 最多 k+1 條邊
      for each edge (u, v, w):
          relax edge

Time: O(k × E), Space: O(V)
```

---

## 3.30 LC 1235 Maximum Profit in Job Scheduling (Hard)

```
題意：有 n 個工作（start, end, profit），選不重疊的工作使利潤最大

[第一反應] 選/不選 + 不重疊 → DP + 排序 + Binary Search
[拆解策略] 策略 1 — 分層拆解
[子問題]
  A: 按 endTime 排序 → 標準排序 (Easy)
  B: DP: dp[i] = 考慮前 i 個工作的最大利潤
     - 不選 job i: dp[i] = dp[i-1]
     - 選 job i: dp[i] = profit[i] + dp[j]（j 是最後一個 end ≤ start[i] 的工作）
  C: 找 j → Binary Search on endTimes (Easy!)
[算法] Sort + DP + Binary Search（三個 Easy pattern 的組合）
[組合]
  sort by endTime
  for each job i:
      j = bisect_right(endTimes, startTime[i])  # Binary Search
      dp[i] = max(dp[i-1], profit[i] + dp[j])

Time: O(n log n), Space: O(n)
```

---

## 30 題拆解速查表

```
┌──────┬─────────────────────────────┬──────────────┬──────────────────────┐
│ 題號 │ 題目名稱                      │ 拆解策略      │ 核心子問題             │
├──────┼─────────────────────────────┼──────────────┼──────────────────────┤
│   4  │ Median of Two Sorted Arrays │ 抽象轉換      │ 數學轉換 + Binary Search │
│  10  │ Regular Expression Matching │ 條件放寬      │ 分 case 的 2D DP       │
│  23  │ Merge K Sorted Lists       │ 分層拆解      │ D&C Merge 或 Min Heap  │
│  25  │ Reverse Nodes in K-Group   │ 分層拆解      │ 數 k 個 + 反轉 + 接回   │
│  32  │ Longest Valid Parentheses  │ 抽象轉換      │ Stack with index 或 DP │
│  41  │ First Missing Positive     │ 抽象轉換      │ Cyclic Sort + 掃描     │
│  42  │ Trapping Rain Water        │ 反向思考      │ 前綴 max + 後綴 max    │
│  44  │ Wildcard Matching          │ 條件放寬      │ 2D DP 分 case          │
│  51  │ N-Queens                   │ 分層拆解      │ Backtracking + 3 Sets  │
│  72  │ Edit Distance              │ 條件放寬      │ 2D DP 三操作          │
│  76  │ Minimum Window Substring   │ 分層拆解      │ Sliding Window + HashMap│
│  84  │ Largest Rect in Histogram  │ 分層拆解      │ 2× Monotonic Stack    │
│  85  │ Maximal Rectangle          │ 增加維度      │ 行掃描 + LC 84        │
│ 124  │ Binary Tree Max Path Sum   │ 分層拆解      │ DFS 分彎/直兩種路徑    │
│ 127  │ Word Ladder                │ 抽象轉換      │ 隱式圖 + BFS          │
│ 128  │ Longest Consecutive Seq    │ 抽象轉換      │ HashSet + 起點計數     │
│ 212  │ Word Search II             │ 分層+轉換     │ Trie + DFS            │
│ 239  │ Sliding Window Maximum     │ 分層拆解      │ Monotonic Deque       │
│ 269  │ Alien Dictionary           │ 抽象轉換      │ 建圖 + Topo Sort      │
│ 295  │ Find Median from Stream    │ 分層拆解      │ 兩個 Heap             │
│ 297  │ Serialize/Deserialize Tree │ 分層拆解      │ Preorder DFS × 2      │
│ 312  │ Burst Balloons             │ 反向思考      │ 反向 + 區間 DP        │
│ 315  │ Count Smaller After Self   │ 抽象轉換      │ Merge Sort 或 BIT     │
│ 329  │ Longest Increasing Path    │ 分層拆解      │ DFS + Memoization     │
│ 336  │ Palindrome Pairs           │ 分層拆解      │ HashMap + 3 Cases     │
│ 410  │ Split Array Largest Sum    │ 抽象轉換      │ BS on Answer + Greedy │
│ 432  │ All O'one Data Structure   │ 分層拆解      │ DLL + 2 HashMaps      │
│ 460  │ LFU Cache                  │ 條件放寬      │ LRU 加 frequency 層   │
│ 787  │ Cheapest Flights K Stops   │ 條件放寬      │ Bellman-Ford k+1 輪   │
│1235  │ Max Profit Job Scheduling  │ 分層拆解      │ Sort + DP + BS        │
└──────┴─────────────────────────────┴──────────────┴──────────────────────┘
```

### 策略分布統計

```
分層拆解 (Layer Decomposition):    15 題 (50%)  ← 最常用！
抽象轉換 (Abstraction/Reduction):   9 題 (30%)  ← 第二常用
條件放寬 (Constraint Relaxation):   5 題 (17%)
反向思考 (Reverse Thinking):        2 題 ( 7%)
增加維度 (Dimension Extension):     1 題 ( 3%)

（注意：有些題用了多種策略，以主要策略計算）

結論：學會「分層拆解」和「抽象轉換」就能應付 80% 的 Hard 題。
```

---

# 第四章：面試中的拆解溝通

## 4.1 為什麼溝通比解題更重要

```
Google 的評分維度：
  1. Coding Ability          — 你能不能寫出 code
  2. Problem Solving         — 你怎麼分析問題  ← 拆解能力在這裡
  3. Communication           — 你怎麼表達思路  ← 拆解溝通在這裡
  4. Algorithm Knowledge     — 你知不知道算法

一個人沉默 15 分鐘然後寫出正確答案 → 可能過
一個人邊分析邊溝通，展示清晰的分解過程 → 一定過

面試官在意的不是「你答對了」，而是「你是怎麼想到的」。
```

## 4.2 拆解溝通的四步模板

### Step 1：表達初步觀察 (Observation)

```
模板：
"Looking at this problem, I notice that [觀察 1] and [觀察 2]."
"This reminds me of [類似的問題/pattern]."

範例（LC 85 Maximal Rectangle）：
"Looking at this problem, I notice that if I fix a row as the base,
 the heights above it form a histogram. This reminds me of LC 84,
 Largest Rectangle in Histogram."
```

### Step 2：宣告拆解計畫 (Decomposition Plan)

```
模板：
"I think I can break this down into [N] sub-problems:
 1. First, [sub-problem A], which I can solve with [algorithm A].
 2. Then, [sub-problem B], which I can solve with [algorithm B].
 Let me start with sub-problem A."

範例（LC 85 Maximal Rectangle）：
"I can break this into two sub-problems:
 1. First, for each row, build a histogram of heights — this is a
    simple O(n) scan.
 2. Then, for each histogram, find the largest rectangle — this is
    the classic monotonic stack approach from LC 84.
 The overall complexity would be O(m×n). Let me start coding the
 histogram construction."
```

### Step 3：逐步執行並解說 (Step-by-Step Execution)

```
模板：
"For sub-problem A, I'll [具體做法]..."
"Now that I have [intermediate result], I can move to sub-problem B..."

範例：
"For the histogram part, I'll maintain an array where histogram[j]
 increments by 1 if matrix[i][j] is '1', and resets to 0 otherwise."

"Now that I have the histogram for this row, I'll apply the monotonic
 stack approach to find the largest rectangle..."
```

### Step 4：驗證與總結 (Verification)

```
模板：
"Let me verify with [test case]..."
"The overall time complexity is [X] because [reasoning]."
"The space complexity is [Y]."

範例：
"Let me trace through a small example to verify...
 The time complexity is O(m×n) — we scan m rows, and for each row
 the monotonic stack runs in O(n).
 The space complexity is O(n) for the histogram and stack."
```

## 4.3 拆解溝通的完整範例

以下是面試中處理 LC 1235 Maximum Profit in Job Scheduling 的完整對話示範：

```
面試官: "You have n jobs with start times, end times, and profits.
        Select non-overlapping jobs to maximize profit."

你: "Let me make sure I understand — jobs can't overlap, and I want
     to maximize total profit. Can I assume all values are positive?"

面試官: "Yes."

你: "I see three sub-problems here:

     First, if I sort jobs by end time, I can process them in order.

     Second, for each job, I have two choices — take it or skip it.
     If I skip it, my profit is the same as the previous best.
     If I take it, I need to find the latest non-overlapping job —
     that's a binary search on end times.

     So the structure is: Sort + DP + Binary Search.

     The DP recurrence would be:
       dp[i] = max(dp[i-1], profit[i] + dp[last_non_overlapping])

     Time complexity: O(n log n) for sorting and binary searches.
     Space: O(n) for the DP array.

     Let me code this up, starting with the sort..."

[開始寫 code，邊寫邊解釋每一步]
```

## 4.4 常見溝通陷阱

```
┌──────────────────────────────────────────────────────────────┐
│  陷阱                          正確做法                       │
├──────────────────────────────────────────────────────────────┤
│  沉默思考太久（>2 min）        說出你在想什麼，即使不確定      │
│  直接開始寫 code               先口頭描述 approach            │
│  說「我知道答案」然後寫         展示你的推導過程               │
│  卡住時不說話                  說 "I'm considering X vs Y..." │
│  只說 high-level idea          具體到子問題和算法              │
│  用中文思考英文表達困難         準備好常用的英文模板句          │
└──────────────────────────────────────────────────────────────┘
```

## 4.5 面試溝通的英文工具句

### 分析階段
```
"Let me first understand what the problem is asking..."
"I notice that [observation]."
"This looks like a variant of [known problem]."
"The key insight here is [insight]."
"I think the key constraint is [constraint], which suggests [approach]."
```

### 拆解階段
```
"I'd like to break this into [N] parts:"
"The first sub-problem is [A], which I can handle with [algorithm]."
"Once I have [intermediate result], the second part becomes [B]."
"This reduces to [known problem] because [reason]."
```

### 寫 code 階段
```
"Let me start with [sub-problem A]..."
"Here I'm using [data structure] because [reason]."
"This loop handles the case where [condition]..."
"Now I'll combine the results from both sub-problems..."
```

### 卡住時
```
"Let me take a step back and think about this differently."
"I'm stuck on [specific part]. Let me consider [alternative approach]."
"What if I try the reverse direction — instead of [X], what about [Y]?"
"Can I solve a simpler version first and then add [constraint]?"
```

### 總結階段
```
"The overall approach is [summary]."
"Time complexity is O([X]) because [reasoning]."
"One possible optimization would be [improvement]."
"Let me verify with this test case: [example]."
```

---

## 本章總結：拆解就是你的超能力

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  記住這個公式：                                                   │
│                                                                 │
│  Hard 題 = Pattern A + Pattern B + Twist                        │
│                                                                 │
│  你的工作不是「解 Hard 題」，                                      │
│  而是「把 Hard 題拆成你已經會的 Easy/Medium 題」。                   │
│                                                                 │
│  五種策略的使用優先順序：                                           │
│  1. 分層拆解 — 有先後步驟嗎？                                     │
│  2. 抽象轉換 — 像不像我認識的問題？                                │
│  3. 增加維度 — 是 1D 題的 2D 版嗎？                               │
│  4. 條件放寬 — 去掉某個條件就會了嗎？                              │
│  5. 反向思考 — 反過來想會更簡單嗎？                                │
│                                                                 │
│  面試溝通口訣：                                                   │
│  觀察 → 宣告拆解計畫 → 逐步執行 → 驗證                            │
│                                                                 │
│  「I can break this into N sub-problems...」                     │
│  — 這句話是你在面試中最有力的武器。                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

> **下一步**：把這 30 題的拆解過程內化。每道 Hard 題，先不看答案，自己嘗試用五種策略拆解。如果 5 分鐘內能拆成子問題，你就已經「會」了。剩下的只是把子問題的 code 寫出來 — 而那些你在 01-17 早就練過了。