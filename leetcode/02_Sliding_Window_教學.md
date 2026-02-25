# Sliding Window（滑動窗口）完整教學

> **適用對象**：LeetCode 初學者，準備 Google / NVIDIA 面試
> **前置知識**：Array 基本操作、for loop、Python dict/set
> **配套程式**：`02_Sliding_Window.py`（可直接執行驗證）
> **教學風格**：教科書級，每個概念至少 2 個完整數值範例 + 逐步計算

---

## 目錄

- [第一章：Sliding Window 核心思想](#第一章sliding-window-核心思想)
- [第二章：固定大小窗口 Fixed Size Window](#第二章固定大小窗口-fixed-size-window)
- [第三章：可變大小窗口 Variable Size Window](#第三章可變大小窗口-variable-size-window)
- [第四章：計數型窗口 Counter Window with HashMap](#第四章計數型窗口-counter-window-with-hashmap)
- [第五章：三種窗口類型比較與決策](#第五章三種窗口類型比較與決策)

---

# 第一章：Sliding Window 核心思想

## 1.1 從暴力法到滑動窗口：為什麼需要這個技巧？

**問題場景**：給定一個陣列，找出所有「連續子陣列」中滿足某條件的最佳解。

### 暴力法的問題 — O(n^2)

假設要找大小為 3 的子陣列的最大和。暴力法會：

```
陣列: [2, 1, 5, 1, 3, 2]

窗口1: [2, 1, 5]       → 2+1+5 = 8    （計算了 3 次加法）
窗口2: [1, 5, 1]       → 1+5+1 = 7    （又計算了 3 次加法）
窗口3: [5, 1, 3]       → 5+1+3 = 9    （又計算了 3 次加法）
窗口4: [1, 3, 2]       → 1+3+2 = 6    （又計算了 3 次加法）
```

暴力法對每個窗口重新計算所有元素的和。n 個元素、窗口大小 k → 共 (n-k+1) 個窗口，每個窗口花 O(k) → 總共 **O(n * k)**。

**關鍵觀察**：窗口1 `[2,1,5]` 和窗口2 `[1,5,1]` 之間，其實只差了一個元素！

```
窗口1: [2, 1, 5]    sum = 8
         ↓
       移除 2, 加入 1
         ↓
窗口2: [1, 5, 1]    sum = 8 - 2 + 1 = 7    （只需 1 次減法 + 1 次加法！）
```

這就是 Sliding Window 的核心：**重複利用已經計算過的結果**，只更新「進入」和「離開」窗口的元素。

### 滑動窗口 — O(n)

```
公式: new_sum = old_sum - 離開的元素 + 進入的元素
```

每個元素最多進入窗口一次、離開窗口一次 → 總共 **O(n)**。

## 1.2 視覺化：想像一個窗口在陣列上滑動

```
陣列:    [2] [1] [5] [1] [3] [2]
索引:     0   1   2   3   4   5

Step 1:  [2   1   5]  1   3   2      window = [0..2], sum = 8
          ─────────
Step 2:   2  [1   5   1]  3   2      window = [1..3], sum = 7
              ─────────
Step 3:   2   1  [5   1   3]  2      window = [2..4], sum = 9  ← 最大!
                  ─────────
Step 4:   2   1   5  [1   3   2]     window = [3..5], sum = 6
                      ─────────
```

窗口就像一個相框，從左向右滑動，每次向右移動一格：
- **右邊界 (right)** 向右擴張：納入新元素
- **左邊界 (left)** 向右收縮：移除舊元素

## 1.3 三種類型的滑動窗口

| 類型 | 窗口大小 | 何時收縮左邊界 | 典型題目 |
|------|----------|---------------|----------|
| **Fixed Size** | 固定為 k | 當 `right >= k-1` | Max Sum Subarray of Size K |
| **Variable Size** | 動態伸縮 | 條件滿足/違反時 | Longest Substring Without Repeat |
| **Counter + HashMap** | 動態伸縮 | `formed == required` 時 | Minimum Window Substring |

## 1.4 如何識別 Sliding Window 題目？

看到以下**關鍵詞**，就要想到 Sliding Window：

```
- "subarray"（連續子陣列）
- "substring"（連續子字串）
- "consecutive"（連續的）
- "window of size k"
- "contiguous"（相鄰的）
- "longest / shortest ... with condition"
- "minimum / maximum ... subarray / substring"
```

**不適用** Sliding Window 的情況：
- subsequence（子序列，不需要連續）→ 用 DP
- 需要排序 → 用 Sort
- 需要所有組合 → 用 Backtracking

---

# 第二章：固定大小窗口 (Fixed Size Window)

## 模板 (Template)

```python
def fixed_window(arr, k):
    left = 0
    # 初始化窗口狀態（sum, set, count 等）

    for right in range(len(arr)):
        # 1. 將 arr[right] 加入窗口
        加入 arr[right] 到窗口狀態

        # 2. 檢查窗口是否已達大小 k
        if right >= k - 1:           # right 從 0 開始，所以 right = k-1 時窗口滿
            # 3. 記錄/更新答案
            更新答案

            # 4. 移除最左邊元素，左邊界右移
            移除 arr[left] 從窗口狀態
            left += 1

    return 答案
```

**逐行解讀**：
- `left = 0`：左邊界從 0 開始
- `for right in range(n)`：右邊界一步一步向右走
- `right >= k - 1`：index 從 0 開始，right = k-1 時窗口恰好有 k 個元素（例如 k=3：right=2 時有 3 個元素）
- 窗口滿了之後，每次 right 右移一格，left 也右移一格，保持大小 k

---

## 2.1 Maximum Sum Subarray of Size K（大小為 K 的最大子陣列和）

**題目**：給定一個整數陣列 `arr` 和一個整數 `k`，找出大小恰好為 `k` 的連續子陣列的最大和。

**核心公式**：
```
window_sum = window_sum - arr[left] + arr[right]
```

### 範例 1：arr = [2, 1, 5, 1, 3, 2], k = 3

```
初始狀態: left=0, window_sum=0, max_sum=-inf

Step 1: right=0
  加入 arr[0]=2 → window_sum = 0 + 2 = 2
  窗口 = [2]  (大小 1 < k=3，還沒滿)
  ┌───┐
  │ 2 │  1   5   1   3   2
  └───┘

Step 2: right=1
  加入 arr[1]=1 → window_sum = 2 + 1 = 3
  窗口 = [2, 1]  (大小 2 < k=3，還沒滿)
  ┌───────┐
  │ 2   1 │  5   1   3   2
  └───────┘

Step 3: right=2
  加入 arr[2]=5 → window_sum = 3 + 5 = 8
  窗口 = [2, 1, 5]  (大小 3 == k，滿了!)
  ┌───────────┐
  │ 2   1   5 │  1   3   2
  └───────────┘
  → max_sum = max(-inf, 8) = 8
  → 移除 arr[left]=arr[0]=2, window_sum = 8 - 2 = 6, left = 1

Step 4: right=3
  加入 arr[3]=1 → window_sum = 6 + 1 = 7
  窗口 = [1, 5, 1]  (大小 3 == k)
      ┌───────────┐
   2  │ 1   5   1 │  3   2
      └───────────┘
  → max_sum = max(8, 7) = 8  (不更新)
  → 移除 arr[1]=1, window_sum = 7 - 1 = 6, left = 2

Step 5: right=4
  加入 arr[4]=3 → window_sum = 6 + 3 = 9
  窗口 = [5, 1, 3]  (大小 3 == k)
          ┌───────────┐
   2   1  │ 5   1   3 │  2
          └───────────┘
  → max_sum = max(8, 9) = 9  ← 更新!
  → 移除 arr[2]=5, window_sum = 9 - 5 = 4, left = 3

Step 6: right=5
  加入 arr[5]=2 → window_sum = 4 + 2 = 6
  窗口 = [1, 3, 2]  (大小 3 == k)
              ┌───────────┐
   2   1   5  │ 1   3   2 │
              └───────────┘
  → max_sum = max(9, 6) = 9  (不更新)
  → 移除 arr[3]=1, window_sum = 6 - 1 = 5, left = 4

答案: max_sum = 9  (子陣列 [5, 1, 3])
```

**驗算**：所有大小為 3 的子陣列和：
- [2,1,5] = 8
- [1,5,1] = 7
- [5,1,3] = 9 (最大)
- [1,3,2] = 6

### 範例 2：arr = [2, 3, 4, 1, 5], k = 2

```
初始狀態: left=0, window_sum=0, max_sum=-inf

Step 1: right=0
  加入 arr[0]=2 → window_sum = 2
  窗口 = [2]  (大小 1 < k=2)
  ┌───┐
  │ 2 │  3   4   1   5
  └───┘

Step 2: right=1
  加入 arr[1]=3 → window_sum = 2 + 3 = 5
  窗口 = [2, 3]  (大小 2 == k，滿了!)
  ┌───────┐
  │ 2   3 │  4   1   5
  └───────┘
  → max_sum = max(-inf, 5) = 5
  → 移除 arr[0]=2, window_sum = 5 - 2 = 3, left = 1

Step 3: right=2
  加入 arr[2]=4 → window_sum = 3 + 4 = 7
  窗口 = [3, 4]
      ┌───────┐
   2  │ 3   4 │  1   5
      └───────┘
  → max_sum = max(5, 7) = 7  ← 更新!
  → 移除 arr[1]=3, window_sum = 7 - 3 = 4, left = 2

Step 4: right=3
  加入 arr[3]=1 → window_sum = 4 + 1 = 5
  窗口 = [4, 1]
          ┌───────┐
   2   3  │ 4   1 │  5
          └───────┘
  → max_sum = max(7, 5) = 7  (不更新)
  → 移除 arr[2]=4, window_sum = 5 - 4 = 1, left = 3

Step 5: right=4
  加入 arr[4]=5 → window_sum = 1 + 5 = 6
  窗口 = [1, 5]
              ┌───────┐
   2   3   4  │ 1   5 │
              └───────┘
  → max_sum = max(7, 6) = 7  (不更新)
  → 移除 arr[3]=1, window_sum = 6 - 1 = 5, left = 4

答案: max_sum = 7  (子陣列 [3, 4])
```

### Corner Cases

| Case | 說明 | 處理方式 |
|------|------|---------|
| `k = 1` | 每個元素自己就是窗口 | 等同找最大值 |
| `k = n` | 整個陣列就是一個窗口 | 等同求整個陣列的和 |
| 全部相同元素 | 如 `[5,5,5,5]`, k=2 | 每個窗口和都一樣 |
| 有負數 | 如 `[-1,2,-3,4]`, k=2 | 照常運作，負數會被減掉 |

---

## 2.2 Maximum Average Subarray I (LeetCode 643)

**題目**：給定一個整數陣列 `nums` 和整數 `k`，找出長度為 `k` 的連續子陣列的最大平均值。

**公式**：
```
average = window_sum / k
max_average = max_sum / k   （只需在最後除一次）
```

**技巧**：比較平均值等同比較總和（因為 k 是常數），所以只需追蹤 max_sum，最後再除以 k。

### 範例 1：nums = [1, 12, -5, -6, 50, 3], k = 4

```
初始: left=0, window_sum=0, max_sum=-inf

Step 1: right=0, 加入 1 → sum=1, 窗口=[1] (未滿)
Step 2: right=1, 加入 12 → sum=13, 窗口=[1,12] (未滿)
Step 3: right=2, 加入 -5 → sum=8, 窗口=[1,12,-5] (未滿)

Step 4: right=3, 加入 -6 → sum=2
  窗口=[1, 12, -5, -6]  (滿! k=4)
  ┌──────────────────┐
  │ 1  12  -5  -6    │ 50   3
  └──────────────────┘
  avg = 2/4 = 0.5
  max_sum = max(-inf, 2) = 2
  移除 nums[0]=1 → sum = 2-1 = 1, left=1

Step 5: right=4, 加入 50 → sum=1+50=51
  窗口=[12, -5, -6, 50]
     ┌──────────────────┐
  1  │ 12  -5  -6  50   │  3
     └──────────────────┘
  avg = 51/4 = 12.75
  max_sum = max(2, 51) = 51  ← 更新!
  移除 nums[1]=12 → sum = 51-12 = 39, left=2

Step 6: right=5, 加入 3 → sum=39+3=42
  窗口=[-5, -6, 50, 3]
         ┌──────────────────┐
  1  12  │ -5  -6  50   3   │
         └──────────────────┘
  avg = 42/4 = 10.5
  max_sum = max(51, 42) = 51  (不更新)
  移除 nums[2]=-5 → sum = 42-(-5) = 47, left=3

答案: max_average = 51 / 4 = 12.75
最大平均子陣列: [12, -5, -6, 50]
```

### 範例 2：nums = [5, 5, 5, 5, 5], k = 2

```
初始: left=0, window_sum=0, max_sum=-inf

Step 1: right=0, 加入 5 → sum=5, 窗口=[5] (未滿)

Step 2: right=1, 加入 5 → sum=10, 窗口=[5,5] (滿!)
  avg = 10/2 = 5.0, max_sum = 10
  移除 5 → sum=5, left=1

Step 3: right=2, 加入 5 → sum=10, 窗口=[5,5] (滿!)
  avg = 10/2 = 5.0, max_sum = 10 (不變)
  移除 5 → sum=5, left=2

Step 4: right=3, 加入 5 → sum=10, max_sum = 10 (不變), 移除 5, left=3
Step 5: right=4, 加入 5 → sum=10, max_sum = 10 (不變), 移除 5, left=4

答案: max_average = 10 / 2 = 5.0
全部元素相同 → 所有窗口平均值都一樣。
```

---

## 2.3 Contains Duplicate II (LeetCode 219)

**題目**：給定整數陣列 `nums` 和整數 `k`，判斷是否存在兩個不同索引 `i` 和 `j`，使得 `nums[i] == nums[j]` 且 `|i - j| <= k`。

**思路**：用 **set** 作為窗口（不是 sum），set 裡面放的是窗口內的元素值。
- 窗口大小最多為 k（代表往前看 k 個元素）
- 如果新元素已經在 set 中 → 找到重複，return True
- 如果窗口超過 k → 移除最老的元素

**關鍵差異**：這題用 **set** 而非 **sum** 作為窗口狀態。

### 範例 1：nums = [1, 2, 3, 1], k = 3

```
初始: left=0, window_set={}

Step 1: right=0, nums[0]=1
  1 in set{} ? → No
  加入 1 → set={1}
  窗口大小=1 (right-left+1=1) <= k+1=4, 不需移除
  ┌───┐
  │ 1 │  2   3   1
  └───┘   set = {1}

Step 2: right=1, nums[1]=2
  2 in set{1} ? → No
  加入 2 → set={1, 2}
  ┌───────┐
  │ 1   2 │  3   1
  └───────┘   set = {1, 2}

Step 3: right=2, nums[2]=3
  3 in set{1,2} ? → No
  加入 3 → set={1, 2, 3}
  ┌───────────┐
  │ 1   2   3 │  1
  └───────────┘   set = {1, 2, 3}

Step 4: right=3, nums[3]=1
  1 in set{1,2,3} ? → Yes!
  |3 - 0| = 3 <= k=3 ✓
  return True

答案: True  (nums[0]=1 和 nums[3]=1，距離 3 <= k=3)
```

### 範例 2：nums = [1, 2, 3, 1, 2, 3], k = 2

```
初始: left=0, window_set={}

Step 1: right=0, nums[0]=1
  1 in {} ? → No, 加入 → set={1}

Step 2: right=1, nums[1]=2
  2 in {1} ? → No, 加入 → set={1, 2}

Step 3: right=2, nums[2]=3
  3 in {1, 2} ? → No, 加入 → set={1, 2, 3}
  right=2 >= k=2 → 窗口超大，移除 nums[left]=nums[0]=1
  set = {2, 3}, left=1

Step 4: right=3, nums[3]=1
  1 in {2, 3} ? → No, 加入 → set={1, 2, 3}
  right=3 >= k=2 → 移除 nums[1]=2
  set = {1, 3}, left=2

Step 5: right=4, nums[4]=2
  2 in {1, 3} ? → No, 加入 → set={1, 2, 3}
  right=4 >= k=2 → 移除 nums[2]=3
  set = {1, 2}, left=3

Step 6: right=5, nums[5]=3
  3 in {1, 2} ? → No, 加入 → set={1, 2, 3}
  right=5 >= k=2 → 移除 nums[3]=1
  set = {2, 3}, left=4

遍歷完畢，沒有找到重複。
答案: False  (重複元素的距離都是 3 > k=2)
```

**分析**：nums[0]=1 和 nums[3]=1 的距離是 3 > k=2，所以不算。同理 nums[1]=2 和 nums[4]=2 距離也是 3。

---

# 第三章：可變大小窗口 (Variable Size Window)

這是 Sliding Window 最重要的變體，也是面試中最常考的類型。

## 核心觀念

固定窗口的 left 是「自動」移動的（窗口滿了就移）。可變窗口的 left 是「條件性」移動的：
- **找最短**：窗口「滿足」條件時，嘗試收縮左邊界 → `while (valid): shrink`
- **找最長**：窗口「違反」條件時，嘗試收縮左邊界 → `while (invalid): shrink`

```
              找最短                              找最長
     ┌──────────────────────┐           ┌──────────────────────┐
     │ for right in range:  │           │ for right in range:  │
     │   加入 arr[right]     │           │   加入 arr[right]     │
     │   while 滿足條件:     │           │   while 不滿足條件:   │
     │     更新答案(取min)   │           │     移除 arr[left]    │
     │     移除 arr[left]    │           │     left += 1        │
     │     left += 1        │           │   更新答案(取max)     │
     └──────────────────────┘           └──────────────────────┘
```

**為什麼收縮左邊界而不是右邊界？**

因為 right 是由 for loop 控制、只會往右走。left 是我們主動控制的。收縮左邊界 = 縮小窗口。這樣保證每個元素最多被 left 和 right 各訪問一次 → O(n)。

## 模板（找最短版本）

```python
def variable_window_min(arr, target):
    left = 0
    window_state = 初始值   # 如 sum=0
    min_len = float('inf')

    for right in range(len(arr)):
        # 1. 擴張：將 arr[right] 加入窗口
        更新 window_state（如 sum += arr[right]）

        # 2. 收縮：當窗口滿足條件時，嘗試縮小
        while window_state 滿足條件:
            # 記錄答案
            min_len = min(min_len, right - left + 1)
            # 移除左邊元素
            更新 window_state（如 sum -= arr[left]）
            left += 1

    return min_len if min_len != float('inf') else 0
```

## 模板（找最長版本）

```python
def variable_window_max(arr):
    left = 0
    window_state = 初始值
    max_len = 0

    for right in range(len(arr)):
        # 1. 擴張：將 arr[right] 加入窗口
        更新 window_state

        # 2. 收縮：當窗口不滿足條件時，縮小
        while window_state 不滿足條件:
            更新 window_state（移除 arr[left]）
            left += 1

        # 3. 此時窗口一定合法，記錄答案
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## 3.1 Minimum Size Subarray Sum (LeetCode 209)

**題目**：給定一個正整數陣列 `nums` 和一個正整數 `target`，找出和 >= target 的最短連續子陣列長度。如果不存在，回傳 0。

**分類**：可變大小窗口，**找最短** → `while (valid): shrink`

**為什麼用 while 而不是 if？** 因為收縮一次之後，窗口可能仍然滿足條件，需要繼續收縮直到不滿足為止。

### 範例 1：target = 7, nums = [2, 3, 1, 2, 4, 3]

```
初始: left=0, window_sum=0, min_len=inf

=== right=0: 加入 nums[0]=2 ===
  window_sum = 0 + 2 = 2
  窗口 = [2], sum=2
  sum=2 < target=7 → 不收縮
  ┌───┐
  │ 2 │  3   1   2   4   3       sum=2 < 7
  └───┘

=== right=1: 加入 nums[1]=3 ===
  window_sum = 2 + 3 = 5
  窗口 = [2, 3], sum=5
  sum=5 < 7 → 不收縮
  ┌───────┐
  │ 2   3 │  1   2   4   3       sum=5 < 7
  └───────┘

=== right=2: 加入 nums[2]=1 ===
  window_sum = 5 + 1 = 6
  窗口 = [2, 3, 1], sum=6
  sum=6 < 7 → 不收縮
  ┌───────────┐
  │ 2   3   1 │  2   4   3       sum=6 < 7
  └───────────┘

=== right=3: 加入 nums[3]=2 ===
  window_sum = 6 + 2 = 8
  窗口 = [2, 3, 1, 2], sum=8
  ┌────────────────┐
  │ 2   3   1   2  │  4   3       sum=8 >= 7 ✓
  └────────────────┘
  → 收縮 iteration 1:
    min_len = min(inf, 4) = 4   (目前最短 = 4)
    移除 nums[0]=2, sum = 8-2 = 6, left=1
    sum=6 < 7 → 停止收縮

=== right=4: 加入 nums[4]=4 ===
  window_sum = 6 + 4 = 10
  窗口 = [3, 1, 2, 4], sum=10
     ┌────────────────┐
  2  │ 3   1   2   4  │  3        sum=10 >= 7 ✓
     └────────────────┘
  → 收縮 iteration 1:
    min_len = min(4, 4) = 4
    移除 nums[1]=3, sum = 10-3 = 7, left=2
    sum=7 >= 7 → 繼續收縮!
  → 收縮 iteration 2:
    min_len = min(4, 3) = 3   (更新! 窗口 [1,2,4])
    移除 nums[2]=1, sum = 7-1 = 6, left=3
    sum=6 < 7 → 停止收縮

=== right=5: 加入 nums[5]=3 ===
  window_sum = 6 + 3 = 9
  窗口 = [2, 4, 3], sum=9
              ┌───────────┐
  2   3   1   │ 2   4   3 │       sum=9 >= 7 ✓
              └───────────┘
  → 收縮 iteration 1:
    min_len = min(3, 3) = 3
    移除 nums[3]=2, sum = 9-2 = 7, left=4
    sum=7 >= 7 → 繼續收縮!
  → 收縮 iteration 2:
    min_len = min(3, 2) = 2   ← 更新! 窗口 [4, 3]
    移除 nums[4]=4, sum = 7-4 = 3, left=5
    sum=3 < 7 → 停止收縮

答案: min_len = 2  (子陣列 [4, 3]，和為 7 >= 7)
```

### 範例 2：target = 4, nums = [1, 4, 4]

```
初始: left=0, window_sum=0, min_len=inf

=== right=0: 加入 nums[0]=1 ===
  sum = 1, 窗口=[1]
  sum=1 < 4 → 不收縮

=== right=1: 加入 nums[1]=4 ===
  sum = 1+4 = 5, 窗口=[1, 4]
  sum=5 >= 4 ✓
  → 收縮 iteration 1:
    min_len = min(inf, 2) = 2  (窗口 [1,4])
    移除 nums[0]=1, sum = 5-1 = 4, left=1
    sum=4 >= 4 → 繼續!
  → 收縮 iteration 2:
    min_len = min(2, 1) = 1  (窗口 [4]，只有一個元素!)
    移除 nums[1]=4, sum = 4-4 = 0, left=2
    sum=0 < 4 → 停止

=== right=2: 加入 nums[2]=4 ===
  sum = 0+4 = 4, 窗口=[4]
  sum=4 >= 4 ✓
  → 收縮:
    min_len = min(1, 1) = 1
    移除 nums[2]=4, sum = 0, left=3
    停止

答案: min_len = 1  (元素 4 本身就 >= target)
```

### 為什麼從左邊收縮（而不是從右邊）？

```
假設窗口 [2, 3, 1, 2, 4, 3]，sum=15 >= 7

如果從右邊移除:
  [2, 3, 1, 2, 4] sum=12  ← 可能錯過左邊更短的解

如果從左邊移除:
  [3, 1, 2, 4, 3] sum=13  ← 正確!因為 right 會繼續往右走，
                              左邊才需要我們主動縮
```

右邊界由 for loop 自動擴張，我們只需要控制左邊界。這是 Sliding Window 的設計哲學：**右邊只擴不縮，左邊只縮不擴**。

---

## 3.2 Longest Substring Without Repeating Characters (LeetCode 3)

**Google 高頻題** | **難度: Medium**

**題目**：給定字串 `s`，找出不含重複字元的最長子字串長度。

**分類**：可變大小窗口，**找最長** → `while (invalid): shrink`

**資料結構**：用 **set** 追蹤窗口內有哪些字元
- 加入字元：`char_set.add(s[right])`
- 移除字元：`char_set.remove(s[left])`
- 檢查重複：`s[right] in char_set`

### 範例 1：s = "abcabcbb"

```
初始: left=0, char_set={}, max_len=0

=== Step 1: right=0, char='a' ===
  'a' in {} ? → No
  加入 'a' → set={'a'}
  窗口 = "a" (s[0..0])
  len = 0-0+1 = 1, max_len = max(0, 1) = 1
  ┌───┐
  │ a │ b  c  a  b  c  b  b      set={a}, max=1
  └───┘

=== Step 2: right=1, char='b' ===
  'b' in {'a'} ? → No
  加入 'b' → set={'a','b'}
  窗口 = "ab" (s[0..1])
  len = 2, max_len = 2
  ┌──────┐
  │ a  b │ c  a  b  c  b  b      set={a,b}, max=2
  └──────┘

=== Step 3: right=2, char='c' ===
  'c' in {'a','b'} ? → No
  加入 'c' → set={'a','b','c'}
  窗口 = "abc" (s[0..2])
  len = 3, max_len = 3
  ┌─────────┐
  │ a  b  c │ a  b  c  b  b      set={a,b,c}, max=3
  └─────────┘

=== Step 4: right=3, char='a' ===
  'a' in {'a','b','c'} ? → Yes! 重複!
  → 收縮: 移除 s[left]=s[0]='a', set={'b','c'}, left=1
  'a' in {'b','c'} ? → No, 停止收縮
  加入 'a' → set={'b','c','a'}
  窗口 = "bca" (s[1..3])
  len = 3, max_len = 3
     ┌─────────┐
  a  │ b  c  a │ b  c  b  b      set={b,c,a}, max=3
     └─────────┘

=== Step 5: right=4, char='b' ===
  'b' in {'b','c','a'} ? → Yes! 重複!
  → 收縮: 移除 s[1]='b', set={'c','a'}, left=2
  'b' in {'c','a'} ? → No, 停止
  加入 'b' → set={'c','a','b'}
  窗口 = "cab" (s[2..4])
  len = 3, max_len = 3
        ┌─────────┐
  a  b  │ c  a  b │ c  b  b      set={c,a,b}, max=3
        └─────────┘

=== Step 6: right=5, char='c' ===
  'c' in {'c','a','b'} ? → Yes! 重複!
  → 收縮: 移除 s[2]='c', set={'a','b'}, left=3
  'c' in {'a','b'} ? → No, 停止
  加入 'c' → set={'a','b','c'}
  窗口 = "abc" (s[3..5])
  len = 3, max_len = 3
           ┌─────────┐
  a  b  c  │ a  b  c │ b  b      set={a,b,c}, max=3
           └─────────┘

=== Step 7: right=6, char='b' ===
  'b' in {'a','b','c'} ? → Yes! 重複!
  → 收縮 iter 1: 移除 s[3]='a', set={'b','c'}, left=4
    'b' in {'b','c'} ? → Yes! 還重複!
  → 收縮 iter 2: 移除 s[4]='b', set={'c'}, left=5
    'b' in {'c'} ? → No, 停止
  加入 'b' → set={'c','b'}
  窗口 = "cb" (s[5..6])
  len = 2, max_len = 3
                 ┌──────┐
  a  b  c  a  b  │ c  b │ b      set={c,b}, max=3
                 └──────┘

=== Step 8: right=7, char='b' ===
  'b' in {'c','b'} ? → Yes! 重複!
  → 收縮 iter 1: 移除 s[5]='c', set={'b'}, left=6
    'b' in {'b'} ? → Yes! 還重複!
  → 收縮 iter 2: 移除 s[6]='b', set={}, left=7
    'b' in {} ? → No, 停止
  加入 'b' → set={'b'}
  窗口 = "b" (s[7..7])
  len = 1, max_len = 3
                    ┌───┐
  a  b  c  a  b  c  b │b│        set={b}, max=3
                    └───┘

答案: max_len = 3  (子字串 "abc" 或 "bca" 或 "cab" 或 "abc")
```

### 範例 2：s = "pwwkew"

```
初始: left=0, char_set={}, max_len=0

=== Step 1: right=0, char='p' ===
  'p' in {} ? → No
  set={'p'}, 窗口="p", len=1, max=1

=== Step 2: right=1, char='w' ===
  'w' in {'p'} ? → No
  set={'p','w'}, 窗口="pw", len=2, max=2

=== Step 3: right=2, char='w' ===
  'w' in {'p','w'} ? → Yes! 重複!
  → 移除 s[0]='p', set={'w'}, left=1
    'w' in {'w'} ? → Yes! 還重複!
  → 移除 s[1]='w', set={}, left=2
    'w' in {} ? → No, 停止
  加入 'w' → set={'w'}
  窗口 = "w" (s[2..2]), len=1, max=2
        ┌───┐
  p  w  │ w │ k  e  w              set={w}, max=2
        └───┘

=== Step 4: right=3, char='k' ===
  'k' in {'w'} ? → No
  set={'w','k'}, 窗口="wk", len=2, max=2

=== Step 5: right=4, char='e' ===
  'e' in {'w','k'} ? → No
  set={'w','k','e'}, 窗口="wke", len=3, max=3  ← 更新!
        ┌───────────┐
  p  w  │ w   k   e │ w            set={w,k,e}, max=3
        └───────────┘

=== Step 6: right=5, char='w' ===
  'w' in {'w','k','e'} ? → Yes! 重複!
  → 移除 s[2]='w', set={'k','e'}, left=3
    'w' in {'k','e'} ? → No, 停止
  加入 'w' → set={'k','e','w'}
  窗口 = "kew" (s[3..5]), len=3, max=3
              ┌───────────┐
  p  w  w     │ k   e   w │        set={k,e,w}, max=3
              └───────────┘

答案: max_len = 3  (子字串 "wke" 或 "kew")
```

### Corner Cases

| Case | 輸入 | 輸出 | 說明 |
|------|------|------|------|
| 空字串 | `""` | `0` | 沒有字元 |
| 全部相同 | `"bbbbb"` | `1` | 每次都重複，窗口最大只有 1 |
| 全部不同 | `"abcde"` | `5` | 整個字串就是答案 |
| 單一字元 | `"a"` | `1` | 就是那個字元本身 |

---

## 3.3 Longest Substring with At Most K Distinct Characters (LeetCode 340)

**題目**：給定字串 `s` 和整數 `k`，找出最多包含 `k` 個不同字元的最長子字串長度。

**分類**：可變大小窗口，**找最長** → `while (invalid): shrink`

**資料結構**：**HashMap** (dict) 記錄每個字元在窗口中出現的次數。
- `char_count[c]`：字元 `c` 在窗口中的出現次數
- `len(char_count)` = 窗口中不同字元的種類數
- 當 `len(char_count) > k` → 窗口不合法，需要收縮

**與 LC 3 的關係**：LC 3 是 "0 個重複" = "每個字元最多出現 1 次"。LC 340 是更一般化的版本："最多 k 種不同字元"。當 k 趨近無窮大時，就不需要收縮了。

### 範例 1：s = "eceba", k = 2

```
初始: left=0, char_count={}, max_len=0

=== Step 1: right=0, char='e' ===
  char_count['e'] += 1 → {'e': 1}
  distinct = 1 種 <= k=2 → 合法
  窗口 = "e" (s[0..0]), len=1, max=1
  ┌───┐
  │ e │ c  e  b  a      count={'e':1}, distinct=1, max=1
  └───┘

=== Step 2: right=1, char='c' ===
  char_count['c'] += 1 → {'e': 1, 'c': 1}
  distinct = 2 種 <= k=2 → 合法
  窗口 = "ec" (s[0..1]), len=2, max=2
  ┌──────┐
  │ e  c │ e  b  a      count={'e':1,'c':1}, distinct=2, max=2
  └──────┘

=== Step 3: right=2, char='e' ===
  char_count['e'] += 1 → {'e': 2, 'c': 1}
  distinct = 2 種 <= k=2 → 合法
  窗口 = "ece" (s[0..2]), len=3, max=3
  ┌─────────┐
  │ e  c  e │ b  a      count={'e':2,'c':1}, distinct=2, max=3
  └─────────┘

=== Step 4: right=3, char='b' ===
  char_count['b'] += 1 → {'e': 2, 'c': 1, 'b': 1}
  distinct = 3 種 > k=2 → 不合法! 需要收縮!

  → 收縮 iter 1:
    移除 s[left]=s[0]='e', char_count['e'] = 2-1 = 1
    count = {'e': 1, 'c': 1, 'b': 1}, distinct = 3 > 2 → 繼續!
    left = 1

  → 收縮 iter 2:
    移除 s[left]=s[1]='c', char_count['c'] = 1-1 = 0
    count['c'] == 0 → 刪除 'c' → count = {'e': 1, 'b': 1}
    distinct = 2 <= 2 → 停止收縮
    left = 2

  窗口 = "eb" (s[2..3]), len=2, max=3
           ┌──────┐
  e  c     │ e  b │ a      count={'e':1,'b':1}, distinct=2, max=3
           └──────┘

=== Step 5: right=4, char='a' ===
  char_count['a'] += 1 → {'e': 1, 'b': 1, 'a': 1}
  distinct = 3 種 > k=2 → 不合法! 收縮!

  → 收縮 iter 1:
    移除 s[2]='e', char_count['e'] = 1-1 = 0 → 刪除 'e'
    count = {'b': 1, 'a': 1}, distinct = 2 <= 2 → 停止
    left = 3

  窗口 = "ba" (s[3..4]), len=2, max=3
              ┌──────┐
  e  c  e     │ b  a │      count={'b':1,'a':1}, distinct=2, max=3
              └──────┘

答案: max_len = 3  (子字串 "ece"，包含 e, c 兩種字元)
```

### 範例 2：s = "aaahhibc", k = 2

```
初始: left=0, char_count={}, max_len=0

=== Step 1: right=0, char='a' ===
  count={'a':1}, distinct=1 <= 2
  窗口="a", len=1, max=1

=== Step 2: right=1, char='a' ===
  count={'a':2}, distinct=1 <= 2
  窗口="aa", len=2, max=2

=== Step 3: right=2, char='a' ===
  count={'a':3}, distinct=1 <= 2
  窗口="aaa", len=3, max=3

=== Step 4: right=3, char='h' ===
  count={'a':3, 'h':1}, distinct=2 <= 2
  窗口="aaah", len=4, max=4
  ┌──────────────┐
  │ a  a  a  h   │ h  i  b  c    count={'a':3,'h':1}, max=4
  └──────────────┘

=== Step 5: right=4, char='h' ===
  count={'a':3, 'h':2}, distinct=2 <= 2
  窗口="aaahh", len=5, max=5  ← 更新!
  ┌─────────────────┐
  │ a  a  a  h  h   │ i  b  c    count={'a':3,'h':2}, max=5
  └─────────────────┘

=== Step 6: right=5, char='i' ===
  count={'a':3, 'h':2, 'i':1}, distinct=3 > 2 → 不合法!

  → 收縮 iter 1: 移除 s[0]='a', count={'a':2,'h':2,'i':1}, distinct=3, left=1
  → 收縮 iter 2: 移除 s[1]='a', count={'a':1,'h':2,'i':1}, distinct=3, left=2
  → 收縮 iter 3: 移除 s[2]='a', count['a']=0→刪除, count={'h':2,'i':1}, distinct=2, left=3

  窗口="hhi" (s[3..5]), len=3, max=5
              ┌─────────┐
  a  a  a     │ h  h  i │ b  c    count={'h':2,'i':1}, max=5
              └─────────┘

=== Step 7: right=6, char='b' ===
  count={'h':2,'i':1,'b':1}, distinct=3 > 2 → 不合法!

  → 收縮 iter 1: 移除 s[3]='h', count={'h':1,'i':1,'b':1}, distinct=3, left=4
  → 收縮 iter 2: 移除 s[4]='h', count['h']=0→刪除, count={'i':1,'b':1}, distinct=2, left=5

  窗口="ib" (s[5..6]), len=2, max=5

=== Step 8: right=7, char='c' ===
  count={'i':1,'b':1,'c':1}, distinct=3 > 2 → 不合法!

  → 收縮: 移除 s[5]='i', count={'b':1,'c':1}, distinct=2, left=6

  窗口="bc" (s[6..7]), len=2, max=5

答案: max_len = 5  (子字串 "aaahh"，包含 a, h 兩種字元)
```

**泛化思考**：
- LC 3 (no repeating) 相當於 k = len(所有不同字元)，但每個字元只能出現一次
- LC 340 (at most k distinct) 不限制每個字元的出現次數，只限制「種類數」

---

# 第四章：計數型窗口 (Counter Window with HashMap)

這是 Sliding Window 中最難的類型。需要同時追蹤「目標需求」和「窗口狀態」兩個 HashMap。

## 核心概念

我們有兩個 HashMap 和兩個計數器：

```
need{}      → 目標需要什麼？（例如：t="ABC" → need = {A:1, B:1, C:1}）
window{}    → 目前窗口裡有什麼？

required    → 需要滿足幾「種」字元？（= len(need)）
formed      → 目前已滿足幾「種」字元？

當 formed == required → 窗口包含了所有目標字元
```

**formed 的更新規則**：
- 當 `window[char] == need[char]` 時，`formed += 1`（這「種」字元剛好滿足）
- 當 `window[char] < need[char]` 時（收縮後），`formed -= 1`（這「種」字元不再滿足）

## 模板（Counter Window）

```python
from collections import Counter, defaultdict

def counter_window(s, t):
    need = Counter(t)           # 目標頻率
    required = len(need)        # 需要滿足的字元種類數
    window = defaultdict(int)   # 窗口內字元頻率
    formed = 0                  # 已滿足的字元種類數

    left = 0
    result = (float('inf'), 0, 0)  # (長度, left, right)

    for right in range(len(s)):
        char = s[right]
        window[char] += 1

        # 這「種」字元的數量剛好達到目標
        if char in need and window[char] == need[char]:
            formed += 1

        # 嘗試收縮
        while formed == required:
            # 更新答案
            curr_len = right - left + 1
            if curr_len < result[0]:
                result = (curr_len, left, right)

            # 移除左邊字元
            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]
```

**逐行解讀**：

| 行 | 程式碼 | 說明 |
|---|--------|------|
| 1 | `need = Counter(t)` | 計算目標字串每個字元需要幾個 |
| 2 | `required = len(need)` | 有幾「種」字元需要滿足 |
| 3 | `window = defaultdict(int)` | 窗口內每個字元出現幾次 |
| 4 | `formed = 0` | 目前滿足了幾種 |
| 5 | `window[char] += 1` | 右邊界字元加入窗口 |
| 6 | `if window[char] == need[char]` | 這種字元「剛好」達標（不是 >=） |
| 7 | `while formed == required` | 所有種類都達標 → 嘗試收縮 |
| 8 | `window[left_char] -= 1` | 收縮：移除左邊字元 |
| 9 | `if window < need[left_char]` | 移除後如果「不夠了」→ formed 減少 |

**為什麼 formed 用 `==` 而不是 `>=` 判斷？**

```
假設 need = {A:2}（需要 2 個 A）
  window[A] = 1 → formed 不增加（還不夠）
  window[A] = 2 → formed += 1（剛好夠）
  window[A] = 3 → formed 不變（超過了，但已經計過了）

收縮時：
  window[A] = 3→2 → formed 不變（還夠）
  window[A] = 2→1 → formed -= 1（不夠了！用 < 判斷）
```

---

## 4.1 Minimum Window Substring (LeetCode 76)

**Google 經典題** | **難度: Hard** | **Sliding Window 最難的題目**

**題目**：給定字串 `s` 和字串 `t`，找出 `s` 中包含 `t` 所有字元的最短子字串。如果不存在，回傳空字串。

**注意**：`t` 中的字元可能有重複！例如 `t="AABC"` 需要 2 個 A、1 個 B、1 個 C。

### 範例 1：s = "ADOBECODEBANC", t = "ABC" （超詳細逐步追蹤）

```
預處理:
  need = Counter("ABC") = {'A': 1, 'B': 1, 'C': 1}
  required = 3  (需要滿足 3 種字元: A, B, C)
  window = {}
  formed = 0
  result = (inf, 0, 0)

字串:  A  D  O  B  E  C  O  D  E  B  A  N  C
索引:  0  1  2  3  4  5  6  7  8  9  10 11 12

=== right=0, char='A' ===
  window['A'] = 0+1 = 1
  'A' in need? Yes. window['A']=1 == need['A']=1? Yes → formed = 0+1 = 1
  window = {'A':1}
  formed = 1/3 (還不夠)
  [A]DOBECODEBANC

=== right=1, char='D' ===
  window['D'] = 1
  'D' in need? No → formed 不變 = 1
  window = {'A':1, 'D':1}
  formed = 1/3
  [AD]OBECODEBANC

=== right=2, char='O' ===
  window['O'] = 1
  'O' in need? No → formed = 1
  window = {'A':1, 'D':1, 'O':1}
  [ADO]BECODEBANC

=== right=3, char='B' ===
  window['B'] = 1
  'B' in need? Yes. window['B']=1 == need['B']=1? Yes → formed = 2
  window = {'A':1, 'D':1, 'O':1, 'B':1}
  formed = 2/3
  [ADOB]ECODEBANC

=== right=4, char='E' ===
  window['E'] = 1
  'E' in need? No → formed = 2
  [ADOBE]CODEBANC

=== right=5, char='C' ===
  window['C'] = 1
  'C' in need? Yes. window['C']=1 == need['C']=1? Yes → formed = 3

  *** formed=3 == required=3 → 窗口包含所有目標字元! ***
  [ADOBEC]ODEBANC
  window = {'A':1, 'D':1, 'O':1, 'B':1, 'E':1, 'C':1}

  → 進入 while 迴圈（嘗試收縮）:
    curr_len = 5-0+1 = 6
    result = (6, 0, 5)  即 "ADOBEC"
    移除 s[0]='A': window['A'] = 1-1 = 0
      'A' in need? Yes. window['A']=0 < need['A']=1? Yes → formed = 2
      left = 1
    formed=2 != 3 → 退出 while

=== right=6, char='O' ===
  window['O'] = 2, formed=2/3
  A[DOBECO]DEBANC

=== right=7, char='D' ===
  window['D'] = 2, formed=2/3
  A[DOBECOD]EBANC

=== right=8, char='E' ===
  window['E'] = 2, formed=2/3
  A[DOBECODE]BANC

=== right=9, char='B' ===
  window['B'] = 2
  'B' in need? Yes. window['B']=2 == need['B']=1? No (2 != 1) → formed 不變 = 2
  A[DOBECODEB]ANC

=== right=10, char='A' ===
  window['A'] = 1
  'A' in need? Yes. window['A']=1 == need['A']=1? Yes → formed = 3

  *** formed=3 == required=3 → 又包含所有目標字元了! ***
  A[DOBECODEBA]NC
  window = {'A':1, 'D':2, 'O':2, 'B':2, 'E':2, 'C':1}

  → 收縮 iter 1:
    curr_len = 10-1+1 = 10, result 仍為 (6, 0, 5)
    移除 s[1]='D': window['D'] = 1
      'D' not in need → formed 不變 = 3
      left = 2
    formed=3 → 繼續收縮!

  → 收縮 iter 2:
    curr_len = 10-2+1 = 9, result 仍為 (6, 0, 5)
    移除 s[2]='O': window['O'] = 1
      'O' not in need → formed = 3
      left = 3
    繼續!

  → 收縮 iter 3:
    curr_len = 10-3+1 = 8, result 仍為 (6, 0, 5)
    移除 s[3]='B': window['B'] = 1
      'B' in need? Yes. window['B']=1 >= need['B']=1? Yes → formed = 3
      left = 4
    繼續!

  → 收縮 iter 4:
    curr_len = 10-4+1 = 7, result 仍為 (6, 0, 5)
    移除 s[4]='E': window['E'] = 1
      'E' not in need → formed = 3
      left = 5
    繼續!

  → 收縮 iter 5:
    curr_len = 10-5+1 = 6, result 仍為 (6, 0, 5)（一樣長）
    移除 s[5]='C': window['C'] = 0
      'C' in need? Yes. window['C']=0 < need['C']=1? Yes → formed = 2
      left = 6
    formed=2 → 退出 while

=== right=11, char='N' ===
  window['N'] = 1, formed=2/3
  ADOBEC[ODEBA N]C

=== right=12, char='C' ===
  window['C'] = 1
  'C' in need? Yes. window['C']=1 == need['C']=1? Yes → formed = 3

  *** formed=3 == required=3 ***
  ADOBEC[ODEBANC]
  window = {'A':1, 'D':1, 'O':1, 'B':1, 'E':1, 'C':1, 'N':1}

  → 收縮 iter 1:
    curr_len = 12-6+1 = 7, result 仍 (6, 0, 5)
    移除 s[6]='O': window['O'] = 0, not in need → formed=3
    left=7, 繼續!

  → 收縮 iter 2:
    curr_len = 12-7+1 = 6, result 仍 (6, 0, 5)
    移除 s[7]='D': window['D'] = 0, not in need → formed=3
    left=8, 繼續!

  → 收縮 iter 3:
    curr_len = 12-8+1 = 5, result = (5, 8, 12)  ← 更新! "EBANC"
    移除 s[8]='E': window['E'] = 0, not in need → formed=3
    left=9, 繼續!

  → 收縮 iter 4:
    curr_len = 12-9+1 = 4, result = (4, 9, 12)  ← 更新! "BANC"
    移除 s[9]='B': window['B'] = 0
      'B' in need? Yes. window['B']=0 < need['B']=1? Yes → formed=2
    left=10
    formed=2 → 退出 while

遍歷結束。

答案: s[9:13] = "BANC"，長度 4
```

**追蹤摘要**：

```
候選結果:
  "ADOBEC"  len=6  (right=5, left=0)
  "EBANC"   len=5  (right=12, left=8)
  "BANC"    len=4  (right=12, left=9)  ← 最短!
```

### 範例 2：s = "a", t = "a"

```
need = {'a': 1}, required = 1
window = {}, formed = 0

=== right=0, char='a' ===
  window['a'] = 1
  'a' in need, window['a']=1 == need['a']=1 → formed = 1

  formed=1 == required=1 → 收縮:
    curr_len = 0-0+1 = 1, result = (1, 0, 0)
    移除 s[0]='a': window['a'] = 0
    'a' in need, window['a']=0 < need['a']=1 → formed = 0
    left = 1

答案: s[0:1] = "a"
```

### Corner Cases

| Case | 說明 | 結果 |
|------|------|------|
| `s="a", t="aa"` | t 需要 2 個 a，s 只有 1 個 | `""` (不可能) |
| `s="ab", t="b"` | t 只需要 b | `"b"` |
| t 有重複字元 | `t="AABC"` → need={A:2,B:1,C:1} | 需要 2 個 A 才算 formed |
| s 完全不含 t 的字元 | `s="xyz", t="abc"` | `""` |

---

## 4.2 Find All Anagrams in a String (LeetCode 438)

**題目**：給定字串 `s` 和字串 `p`，找出 `s` 中所有 `p` 的 anagram（字母重排）的起始索引。

**與 LC 76 的關係**：這題其實是「固定大小窗口 + Counter」的結合。窗口大小固定為 `len(p)`。

**核心思路**：
1. 窗口大小固定 = `len(p)`
2. 用 need/window/formed/required 追蹤字元頻率
3. 當 `formed == required` 且窗口大小剛好是 `len(p)` → 找到一個 anagram

### 範例 1：s = "cbaebabacd", p = "abc"

```
預處理:
  need = Counter("abc") = {'a':1, 'b':1, 'c':1}
  required = 3
  window_size = len("abc") = 3

字串:  c  b  a  e  b  a  b  a  c  d
索引:  0  1  2  3  4  5  6  7  8  9

=== right=0, char='c' ===
  window = {'c':1}
  'c' in need, window['c']=1 == need['c']=1 → formed=1
  窗口大小 = 0-0+1 = 1 < 3 → 不檢查
  [c] b  a  e  b  a  b  a  c  d

=== right=1, char='b' ===
  window = {'c':1, 'b':1}
  'b' in need, window['b']=1 == need['b']=1 → formed=2
  窗口大小 = 2 < 3 → 不檢查
  [c  b] a  e  b  a  b  a  c  d

=== right=2, char='a' ===
  window = {'c':1, 'b':1, 'a':1}
  'a' in need, window['a']=1 == need['a']=1 → formed=3
  窗口大小 = 3 == 3 → 檢查!
  formed=3 == required=3 → 找到 anagram!
  result = [0]  (起始索引 0, 子字串 "cba")
  [c  b  a] e  b  a  b  a  c  d

  窗口已滿，移除左邊:
  移除 s[0]='c': window['c'] = 0
    'c' in need, window['c']=0 < need['c']=1 → formed=2
  left=1

=== right=3, char='e' ===
  window = {'b':1, 'a':1, 'e':1}
  'e' not in need → formed=2
  窗口大小 = 3-1+1 = 3 → 檢查: formed=2 != 3 → 不是 anagram
   c [b  a  e] b  a  b  a  c  d

  移除 s[1]='b': window['b']=0, formed 降為 1
  left=2

=== right=4, char='b' ===
  window = {'a':1, 'e':1, 'b':1}
  'b' in need, window['b']=1==need['b']=1 → formed=2
  窗口大小=3 → 檢查: formed=2 != 3
   c  b [a  e  b] a  b  a  c  d

  移除 s[2]='a': window['a']=0, formed 降為 1
  left=3

=== right=5, char='a' ===
  window = {'e':1, 'b':1, 'a':1}
  'a' in need, window['a']=1==1 → formed=2
  窗口大小=3 → formed=2 != 3
   c  b  a [e  b  a] b  a  c  d

  移除 s[3]='e': not in need, formed=2
  left=4

=== right=6, char='b' ===
  window = {'b':2, 'a':1}
  'b' in need, window['b']=2 != need['b']=1 → formed 不變 = 2
  窗口大小=3 → formed=2 != 3
   c  b  a  e [b  a  b] a  c  d

  移除 s[4]='b': window['b']=1
    window['b']=1 == need['b']=1 → 但這是移除時的 == 判斷，不加 formed
    (注意：移除時只看 < 才減 formed)
  left=5

=== right=7, char='a' ===
  window = {'a':2, 'b':1}
  'a' in need, window['a']=2 != need['a']=1 → formed 不變 = 2
  窗口大小=3 → formed=2 != 3
   c  b  a  e  b [a  b  a] c  d

  移除 s[5]='a': window['a']=1
    window['a']=1 == need['a']=1 → 不觸發 formed 減少
  left=6

=== right=8, char='c' ===
  window = {'b':1, 'a':1, 'c':1}
  'c' in need, window['c']=1==need['c']=1 → formed=3
  窗口大小=3 → 檢查!
  formed=3 == required=3 → 找到 anagram!
  result = [0, 6]  (起始索引 6, 子字串 "bac")
   c  b  a  e  b  a [b  a  c] d

  移除 s[6]='b': window['b']=0
    window['b']=0 < need['b']=1 → formed=2
  left=7

=== right=9, char='d' ===
  window = {'a':1, 'c':1, 'd':1}
  'd' not in need → formed=2
  formed=2 != 3
  移除 s[7]='a': formed 降為 1
  left=8

答案: [0, 6]
  - s[0:3] = "cba" (abc 的重排)
  - s[6:9] = "bac" (abc 的重排)
```

### 範例 2：s = "abab", p = "ab"

```
need = {'a':1, 'b':1}, required=2, window_size=2

=== right=0, char='a' ===
  window={'a':1}, formed=1 ('a' 滿足)
  窗口大小=1 < 2

=== right=1, char='b' ===
  window={'a':1,'b':1}, formed=2 ('b' 也滿足)
  窗口大小=2 == 2 → formed=2==2 → 找到! result=[0] ("ab")
  移除 s[0]='a': window={'b':1}, formed=1
  left=1

=== right=2, char='a' ===
  window={'b':1,'a':1}, formed=2
  窗口大小=2 → formed=2==2 → 找到! result=[0,1] ("ba")
  移除 s[1]='b': window={'a':1}, formed=1
  left=2

=== right=3, char='b' ===
  window={'a':1,'b':1}, formed=2
  窗口大小=2 → formed=2==2 → 找到! result=[0,1,2] ("ab")
  移除 s[2]='a': formed=1
  left=3

答案: [0, 1, 2]
  - s[0:2]="ab", s[1:3]="ba", s[2:4]="ab"  全部都是 "ab" 的 anagram
```

---

## 4.3 Permutation in String (LeetCode 567)

**題目**：判斷 `s2` 是否包含 `s1` 的排列（permutation）。

**與 LC 438 的關係**：幾乎完全相同！LC 438 要找「所有」anagram 的位置，LC 567 只要找到「一個」就回傳 True。

### 範例 1：s1 = "ab", s2 = "eidbaooo"

```
need = Counter("ab") = {'a':1, 'b':1}
required = 2, window_size = 2

字串:  e  i  d  b  a  o  o  o
索引:  0  1  2  3  4  5  6  7

=== right=0, char='e' ===
  window={'e':1}, 'e' not in need → formed=0
  窗口大小=1 < 2

=== right=1, char='i' ===
  window={'e':1,'i':1}, formed=0
  窗口大小=2 → formed=0 != 2 → 不是
  移除 s[0]='e', left=1

=== right=2, char='d' ===
  window={'i':1,'d':1}, formed=0
  窗口大小=2 → formed=0 != 2
  移除 s[1]='i', left=2

=== right=3, char='b' ===
  window={'d':1,'b':1}, 'b' in need, window['b']=1==need['b']=1 → formed=1
  窗口大小=2 → formed=1 != 2
  移除 s[2]='d', left=3

=== right=4, char='a' ===
  window={'b':1,'a':1}, 'a' in need, window['a']=1==need['a']=1 → formed=2
  窗口大小=2 → formed=2 == required=2
  → 找到排列! s2[3:5] = "ba"
  return True

答案: True  ("ba" 是 "ab" 的排列)
```

### 範例 2：s1 = "ab", s2 = "eidboaoo"

```
need = {'a':1, 'b':1}, required=2, window_size=2

字串:  e  i  d  b  o  a  o  o
索引:  0  1  2  3  4  5  6  7

right=0: window={'e':1}, formed=0, 窗口大小=1
right=1: window={'e':1,'i':1}, formed=0, 大小=2→不是, 移除'e', left=1
right=2: window={'i':1,'d':1}, formed=0, 大小=2→不是, 移除'i', left=2
right=3: window={'d':1,'b':1}, formed=1 (b滿足), 大小=2→不是(1!=2), 移除'd', left=3
right=4: window={'b':1,'o':1}, 'o' not in need, formed=1, 大小=2→不是, 移除'b', formed=0, left=4
right=5: window={'o':1,'a':1}, formed=1 (a滿足), 大小=2→不是(1!=2), 移除'o', left=5
right=6: window={'a':1,'o':1}, formed=1, 大小=2→不是, 移除'a', formed=0, left=6
right=7: window={'o':2}, formed=0, 大小=2→不是, 移除s[6]='o', left=7

遍歷結束，從未 formed==required。
答案: False  (b 和 a 之間隔了 'o'，不連續)
```

**關鍵差異**：s2="eidboaoo" 中 'b' 在 index 3，'a' 在 index 5，中間隔了 'o'，所以沒有長度為 2 的窗口同時包含 'a' 和 'b'。

---

# 第五章：三種窗口類型比較與決策

## 5.1 比較表

```
┌──────────────┬─────────────────────┬─────────────────────┬─────────────────────────┐
│              │ Fixed Size Window   │ Variable Size Window│ Counter + HashMap       │
│              │ (固定大小窗口)       │ (可變大小窗口)       │ (計數型窗口)             │
├──────────────┼─────────────────────┼─────────────────────┼─────────────────────────┤
│ 窗口大小     │ 固定 = k            │ 動態伸縮            │ 動態伸縮                │
│              │                     │                     │                         │
│ 何時收縮     │ right >= k-1        │ 滿足/違反條件       │ formed == required      │
│ 左邊界       │ (自動)              │ (條件觸發)          │ (條件觸發)              │
│              │                     │                     │                         │
│ 窗口狀態     │ sum 或 set          │ sum 或 set          │ 2 個 HashMap            │
│ 資料結構     │                     │                     │ (need + window)         │
│              │                     │                     │                         │
│ 典型題目     │ Max Sum Subarray K  │ Min Subarray Sum    │ Min Window Substring    │
│              │ Max Average (643)   │ No Repeat (3)       │ Find Anagrams (438)     │
│              │ Contains Dup (219)  │ K Distinct (340)    │ Permutation (567)       │
│              │                     │                     │                         │
│ 難度         │ Easy                │ Medium              │ Medium ~ Hard           │
│              │                     │                     │                         │
│ 時間複雜度   │ O(n)                │ O(n)                │ O(n)                    │
│ 空間複雜度   │ O(1) 或 O(k)        │ O(n) 或 O(k)        │ O(|t|) 或 O(|charset|) │
└──────────────┴─────────────────────┴─────────────────────┴─────────────────────────┘
```

## 5.2 決策流程圖

```
題目來了!
│
├── 關鍵詞有 "subarray" / "substring" / "consecutive" / "contiguous" ?
│   │
│   ├── No → 可能不是 Sliding Window
│   │        考慮: DP, Two Pointers, Binary Search, etc.
│   │
│   └── Yes → 可能是 Sliding Window!
│       │
│       ├── 窗口大小固定嗎？ (題目明確給了 k)
│       │   │
│       │   ├── Yes → 【Fixed Size Window】
│       │   │        套用固定窗口模板
│       │   │        例: "subarray of size k", "window of length k"
│       │   │
│       │   └── No → 窗口大小不固定
│       │       │
│       │       ├── 需要匹配/比對「字元頻率」嗎？
│       │       │   │
│       │       │   ├── Yes → 【Counter + HashMap】
│       │       │   │        用 need/window/formed/required
│       │       │   │        例: "contains all characters of t"
│       │       │   │             "anagram", "permutation"
│       │       │   │
│       │       │   └── No → 【Variable Size Window】
│       │       │        │
│       │       │        ├── 找最短？
│       │       │        │   → while (valid): shrink, update min
│       │       │        │   例: "minimum length subarray with sum >= k"
│       │       │        │
│       │       │        └── 找最長？
│       │       │            → while (invalid): shrink, then update max
│       │       │            例: "longest substring without repeating"
│       │       │                 "longest with at most k distinct"
```

## 5.3 常見錯誤 (Common Mistakes)

### 錯誤 1：while vs if

```python
# 錯誤: 用 if 只收縮一次
if window_sum >= target:        # 只收縮一次就跳出
    min_len = min(...)
    window_sum -= arr[left]
    left += 1

# 正確: 用 while 持續收縮到不滿足為止
while window_sum >= target:     # 可能需要收縮多次!
    min_len = min(...)
    window_sum -= arr[left]
    left += 1
```

**為什麼**：收縮一次後，可能仍然滿足條件。例如 `[1,1,1,100]`，target=7，加入 100 後需要收縮好幾次。

### 錯誤 2：formed 的判斷條件

```python
# 錯誤: 用 >= 判斷 formed 增加
if char in need and window[char] >= need[char]:
    formed += 1    # 如果 window[char] 從 2→3，也會觸發! 重複計算!

# 正確: 用 == 判斷（只在「剛好達標」時觸發一次）
if char in need and window[char] == need[char]:
    formed += 1    # 從 0→1 或 1→2 等，剛好等於 need 時才加
```

### 錯誤 3：忘記在收縮時更新答案

```python
# 錯誤: 收縮完才更新（錯過最佳解）
while formed == required:
    window[s[left]] -= 1
    ...
    left += 1
min_len = min(min_len, right - left + 1)   # 收縮後的窗口已經不合法了!

# 正確: 在收縮前先更新答案
while formed == required:
    min_len = min(min_len, right - left + 1)   # 先記錄
    window[s[left]] -= 1
    ...
    left += 1
```

### 錯誤 4：固定窗口的 off-by-one

```python
# 錯誤: 用 right >= k
if right >= k:              # 窗口有 k+1 個元素時才觸發!

# 正確: 用 right >= k-1
if right >= k - 1:          # 窗口剛好有 k 個元素時觸發
```

因為 right 從 0 開始，`right = k-1` 時窗口有 `k-1-0+1 = k` 個元素。

### 錯誤 5：Counter 窗口中忘記刪除計數為 0 的鍵

```python
# 可能有問題: char_count 中殘留 0 值的鍵
char_count[s[left]] -= 1
# 此時 char_count 可能是 {'a': 0, 'b': 1, 'c': 1}
# len(char_count) = 3，但實際只有 2 種有效字元!

# 正確做法: 計數歸 0 時刪除鍵
char_count[s[left]] -= 1
if char_count[s[left]] == 0:
    del char_count[s[left]]
# 現在 len(char_count) 正確反映實際的不同字元數
```

## 5.4 面試白板策略 (Interview Whiteboard Tips)

### Step 1：確認是 Sliding Window

向面試官確認：
- "這題是找連續子陣列/子字串對吧？" → 確認 Sliding Window 適用
- "窗口大小是固定的還是可變的？" → 決定用哪個模板

### Step 2：選擇模板，寫出骨架

```python
# 先寫這個骨架，再填入細節
left = 0
for right in range(n):
    # 加入 arr[right]
    # if/while 條件:
    #     更新答案
    #     移除 arr[left]; left += 1
```

### Step 3：確認邊界條件

在白板上寫下 corner cases：
- 空輸入
- k > n（窗口比陣列大）
- 全部相同元素
- 答案不存在

### Step 4：跑一個小例子

用 n=5~6 的例子手動 trace，確認邏輯正確。

### Step 5：分析複雜度

- Time: O(n) — 每個元素最多被 left 和 right 各訪問一次
- Space: O(1) / O(k) / O(|charset|) 看題目

### 模板速記卡

```
┌─────────────────────────────────────────────────┐
│ Fixed:    for r: add → if r>=k-1: ans, remove   │
│ Var-min:  for r: add → while valid: ans, remove │
│ Var-max:  for r: add → while invalid: remove→ans│
│ Counter:  for r: add, formed++ → while formed   │
│           ==required: ans, remove, formed--      │
└─────────────────────────────────────────────────┘
```

## 5.5 時間複雜度為什麼是 O(n)？

很多人疑惑：外層 `for` 迴圈 + 內層 `while` 迴圈，不是 O(n^2) 嗎？

**關鍵洞察**：`left` 指標在整個演算法過程中，從 0 移到最多 n-1，**只會向右移動，永遠不會回頭**。

```
left 的移動總次數 <= n
right 的移動總次數 = n

total operations = left 移動次數 + right 移動次數 <= n + n = 2n = O(n)
```

雖然 while 迴圈可能在某一步跑很多次，但「欠的」會在後面的步驟「還回來」（left 不會回頭）。這是一個 **amortized analysis（均攤分析）** 的經典案例。

**具體例子**：

```
nums = [1, 1, 1, 1, 100], target = 100

right=0: left=0, sum=1   (不收縮)
right=1: left=0, sum=2   (不收縮)
right=2: left=0, sum=3   (不收縮)
right=3: left=0, sum=4   (不收縮)
right=4: left=0, sum=104 (收縮! left 從 0 連續移到 4，共 4 次)

right 移動了 5 次，left 移動了 4 次 → 共 9 次 = O(n)
不是 5 * 4 = 20 次!
```

---

## 附錄：題目清單與刷題順序

### 建議刷題順序（由易到難）

```
Phase 1: Fixed Size Window
  1. Maximum Sum Subarray of Size K        (Easy, 基礎)
  2. LC 643 - Maximum Average Subarray I   (Easy)
  3. LC 219 - Contains Duplicate II        (Easy)

Phase 2: Variable Size Window
  4. LC 209 - Minimum Size Subarray Sum    (Medium)
  5. LC 3   - Longest Substring No Repeat  (Medium, Google 高頻!)
  6. LC 340 - K Distinct Characters         (Medium)

Phase 3: Counter + HashMap
  7. LC 567 - Permutation in String        (Medium)
  8. LC 438 - Find All Anagrams            (Medium)
  9. LC 76  - Minimum Window Substring     (Hard, Google 經典!)
```

### Google / NVIDIA 高頻 Sliding Window 題目

| 題號 | 題目 | 難度 | 公司 | 類型 |
|------|------|------|------|------|
| 3 | Longest Substring Without Repeating | Medium | Google | Variable |
| 76 | Minimum Window Substring | Hard | Google | Counter |
| 209 | Minimum Size Subarray Sum | Medium | Google | Variable |
| 239 | Sliding Window Maximum | Hard | Google/NVIDIA | Fixed + Deque |
| 340 | Longest Substring K Distinct | Medium | Google | Variable |
| 438 | Find All Anagrams | Medium | Google | Counter |
| 567 | Permutation in String | Medium | NVIDIA | Counter |
| 643 | Maximum Average Subarray I | Easy | -- | Fixed |
| 904 | Fruit Into Baskets | Medium | Google | Variable (k=2) |
| 1004 | Max Consecutive Ones III | Medium | Google | Variable |
