# Binary Search 二分搜尋 — 完整教學講義

> **目標讀者**：基礎薄弱、準備 Google 面試的工程師
> **風格**：每個概念至少 2 組 step-by-step 數值追蹤，用「跑一次給你看」取代抽象描述
> **配套程式**：`06_Binary_Search.py`（可直接執行驗證所有範例）

---

## 目錄

| 章 | 主題 | 頁內連結 |
|----|------|---------|
| 1 | 二分搜尋的本質 | [第一章](#第一章二分搜尋的本質) |
| 2 | 三種模板（最重要！） | [第二章](#第二章三種模板--最重要的章節) |
| 3 | 標準題目 | [第三章](#第三章標準題目) |
| 4 | 旋轉數組 | [第四章](#第四章旋轉數組-rotated-array) |
| 5 | 答案二分（Google 最愛） | [第五章](#第五章答案二分-binary-search-on-answer--google-最愛) |
| 6 | 矩陣二分 | [第六章](#第六章矩陣二分) |
| 7 | 面試決策框架 | [第七章](#第七章面試決策框架) |

---

# 第一章：二分搜尋的本質

## 1.1 從線性搜尋到二分搜尋

**線性搜尋 Linear Search**：從頭掃到尾，最壞情況看完所有 n 個元素。

```
陣列: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
找 target = 23

Step 1: 看 index 0 → 2  ≠ 23
Step 2: 看 index 1 → 5  ≠ 23
Step 3: 看 index 2 → 8  ≠ 23
Step 4: 看 index 3 → 12 ≠ 23
Step 5: 看 index 4 → 16 ≠ 23
Step 6: 看 index 5 → 23 == 23 ✓ 找到！

最壞: n 步 → O(n)
```

**二分搜尋 Binary Search**：每一步砍掉一半，只需 log2(n) 步。

```
陣列: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
找 target = 23

Step 1: 看中間 index 4 → 16 < 23 → 砍掉左半邊
        剩下: [23, 38, 56, 72, 91]

Step 2: 看中間 index 7 → 56 > 23 → 砍掉右半邊
        剩下: [23, 38]

Step 3: 看中間 index 5 → 23 == 23 ✓ 找到！

只用 3 步！
```

## 1.2 為什麼是 O(log n)？決策樹的直覺

每一步把搜尋範圍砍一半，就像一棵二元樹：

```
                    n 個元素
                   /        \
              n/2             n/2          ← 第 1 步後剩 n/2
             /   \           /   \
          n/4    n/4      n/4    n/4       ← 第 2 步後剩 n/4
          ...    ...      ...    ...
            1      1        1      1       ← 第 k 步後剩 1
```

**數學推導**：

```
起始: n 個元素
第 1 步後: n / 2
第 2 步後: n / 4
第 3 步後: n / 8
...
第 k 步後: n / 2^k

當 n / 2^k = 1 時搜尋結束
→ 2^k = n
→ k = log₂(n)
```

**實際數字感受**：

| n (元素數量) | 線性搜尋 O(n) | 二分搜尋 O(log n) | 加速倍數 |
|-------------|--------------|-------------------|---------|
| 100 | 100 步 | 7 步 | 14x |
| 10,000 | 10,000 步 | 14 步 | 714x |
| 1,000,000 | 1,000,000 步 | 20 步 | 50,000x |
| 10^9 | 10 億步 | 30 步 | 3,300 萬x |

```
log₂(10^6) = 6 × log₂(10) ≈ 6 × 3.322 = 19.93 ≈ 20 步
```

**面試中記住**：n = 10^9 時，O(n) 會 TLE，O(log n) 只要約 30 步。
看到搜尋範圍很大 (10^9) + 有單調性 → 幾乎一定是二分搜尋！

## 1.3 前提條件：搜尋空間必須具有「單調性 Monotonic Property」

二分搜尋能用的**充分條件**：存在一個判斷函式 f(x)，使得

```
搜尋空間:  ... T T T T F F F F ...
                     ↑
               找這個分界點

或者

搜尋空間:  ... F F F F T T T T ...
                     ↑
               找這個分界點
```

重點：不一定要「排序好的陣列」！只要搜尋空間能分成「左邊全部滿足 / 右邊全部不滿足」就行。

## 1.4 ASCII 圖示：搜尋範圍的縮小過程

```
找 target = 23 在 [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

初始:
|<==================== 搜尋範圍 ====================>|
 2    5    8    12   16   23   38   56   72   91
[0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]
                          ↑mid=4, nums[4]=16 < 23

第一步後 (左半砍掉):
                               |<== 搜尋範圍 ==>|
 2    5    8    12   16   23   38   56   72   91
                         [5]  [6]  [7]  [8]  [9]
                                    ↑mid=7, nums[7]=56 > 23

第二步後 (右半砍掉):
                          |<= 範圍 =>|
 2    5    8    12   16   23   38   56   72   91
                         [5]  [6]
                          ↑mid=5, nums[5]=23 == 23 ✓
```

---

# 第二章：三種模板 — 最重要的章節！

> **核心觀念**：三種模板的差異在於「搜尋區間的定義」和「終止條件」。
> 選錯模板 → 無限迴圈或 off-by-one error。

## 2.1 Template 1: `while left <= right`（閉區間）

### 定義

```python
def binary_search_t1(nums, target):
    left, right = 0, len(nums) - 1    # 搜尋區間 [left, right] 閉區間

    while left <= right:               # 終止: left > right (區間為空)
        mid = left + (right - left) // 2   # 防溢位！

        if nums[mid] == target:
            return mid                 # 找到了
        elif nums[mid] < target:
            left = mid + 1             # 砍掉左半 [left, mid]
        else:
            right = mid - 1            # 砍掉右半 [mid, right]

    return -1                          # 沒找到
```

### 關鍵細節

| 項目 | 說明 |
|------|------|
| 搜尋區間 | `[left, right]` 閉區間，left 和 right 都在搜尋範圍內 |
| 終止條件 | `left > right`，表示區間為空 `[right+1, right]`，沒東西可搜 |
| 縮小範圍 | `left = mid + 1` 或 `right = mid - 1`（mid 已經比過，要排除） |
| 適用場景 | 找確切值（exact match） |

### 為什麼 `mid = left + (right - left) // 2` 而不是 `(left + right) // 2`？

```
假設 left = 2,000,000,000   right = 2,000,000,000
left + right = 4,000,000,000 > INT_MAX (2^31 - 1 = 2,147,483,647)
→ 整數溢位 (Integer Overflow)！

用 left + (right - left) // 2:
right - left = 0
left + 0 = 2,000,000,000 ✓ 不溢位

Python 有無限精度整數不會溢位，但 C++/Java 會！
面試時用防溢位寫法展示你的細心。
```

### Example 1: 找到 target

```
nums = [1, 3, 5, 7, 9, 11], target = 7
index:  0  1  2  3  4   5

--- Iteration 1 ---
left = 0, right = 5
mid = 0 + (5 - 0) // 2 = 2
nums[2] = 5

數字線:
[1    3    5    7    9    11]
 L              M              R
 0    1    2    3    4    5

5 < 7 → target 在右半邊 → left = mid + 1 = 3

--- Iteration 2 ---
left = 3, right = 5
mid = 3 + (5 - 3) // 2 = 4
nums[4] = 9

數字線:
[1    3    5    7    9    11]
                    L    M    R
                    3    4    5

9 > 7 → target 在左半邊 → right = mid - 1 = 3

--- Iteration 3 ---
left = 3, right = 3
mid = 3 + (3 - 3) // 2 = 3
nums[3] = 7

數字線:
[1    3    5    7    9    11]
                   LMR
                    3

7 == 7 → 找到！return 3 ✓

總步數: 3 步 (log₂6 ≈ 2.58，向上取整 = 3)
```

### Example 2: target 不存在

```
nums = [1, 3, 5, 7, 9, 11], target = 4
index:  0  1  2  3  4   5

--- Iteration 1 ---
left = 0, right = 5
mid = 0 + (5 - 0) // 2 = 2
nums[2] = 5

[1    3    5    7    9    11]
 L         M               R
 0    1    2    3    4     5

5 > 4 → right = mid - 1 = 1

--- Iteration 2 ---
left = 0, right = 1
mid = 0 + (1 - 0) // 2 = 0
nums[0] = 1

[1    3    5    7    9    11]
 LM   R
 0    1

1 < 4 → left = mid + 1 = 1

--- Iteration 3 ---
left = 1, right = 1
mid = 1 + (1 - 1) // 2 = 1
nums[1] = 3

[1    3    5    7    9    11]
      LMR
       1

3 < 4 → left = mid + 1 = 2

--- 終止 ---
left = 2, right = 1 → left > right → 迴圈結束
return -1 (沒找到)

注意: 此時 left = 2 指向 nums[2] = 5，正好是「如果要插入 4，應該放在 index 2」
→ 這就是 Search Insert Position (LC 35) 的原理！
```

---

## 2.2 Template 2: `while left < right`（左閉右開 / 收斂型）

### 定義

```python
# 找左邊界 (Leftmost / Lower Bound)
def left_bound(nums, target):
    left, right = 0, len(nums)    # 注意 right = len(nums)，不是 len-1

    while left < right:            # 終止: left == right (收斂到一個點)
        mid = left + (right - left) // 2

        if nums[mid] < target:
            left = mid + 1         # mid 太小，不可能是答案
        else:
            right = mid            # mid 可能是答案（不排除 mid！）

    return left                    # left == right，就是答案位置
```

```python
# 找右邊界 (Rightmost / Upper Bound)
def right_bound(nums, target):
    left, right = 0, len(nums)

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] <= target:    # 注意: <= 而非 <
            left = mid + 1         # mid 太小或等於 target，繼續往右找
        else:
            right = mid

    return left - 1                # 注意: 要減 1！
```

### 關鍵細節

| 項目 | 左邊界 | 右邊界 |
|------|--------|--------|
| 比較條件 | `nums[mid] < target` → `left = mid + 1` | `nums[mid] <= target` → `left = mid + 1` |
| right 收縮 | `right = mid`（mid 可能是答案） | `right = mid`（mid 可能是答案） |
| 返回值 | `left` | `left - 1` |
| 直覺 | 「第一個 >= target 的位置」 | 「最後一個 <= target 的位置」 |

### 左邊界 vs 右邊界的核心差異

```
nums = [1, 2, 2, 2, 3]

找左邊界 (leftmost 2):
  目標: 找「第一個 >= 2 的位置」
  條件: nums[mid] < 2 → left = mid + 1 (太小，丟掉)
        nums[mid] >= 2 → right = mid   (可能是答案，保留)

找右邊界 (rightmost 2):
  目標: 找「最後一個 <= 2 的位置」
  條件: nums[mid] <= 2 → left = mid + 1 (可能還有更右的，繼續)
        nums[mid] > 2  → right = mid   (太大，丟掉)
  返回 left - 1 (因為 left 指向「第一個 > target 的位置」)
```

### Example 1: 找左邊界 (leftmost 2)

```
nums = [1, 2, 2, 2, 3], target = 2
index:  0  1  2  3  4

--- Iteration 1 ---
left = 0, right = 5
mid = 0 + (5 - 0) // 2 = 2
nums[2] = 2

[1    2    2    2    3]  |
 L         M         R(虛)
 0    1    2    3    4   5

nums[2] = 2 >= target → right = mid = 2
(2 可能是答案，但左邊可能還有 2，所以保留 mid，縮小右界)

--- Iteration 2 ---
left = 0, right = 2
mid = 0 + (2 - 0) // 2 = 1
nums[1] = 2

[1    2    2    2    3]
 L    M    R
 0    1    2

nums[1] = 2 >= target → right = mid = 1
(又找到一個 2，繼續往左探索)

--- Iteration 3 ---
left = 0, right = 1
mid = 0 + (1 - 0) // 2 = 0
nums[0] = 1

[1    2    2    2    3]
 LM   R
 0    1

nums[0] = 1 < target → left = mid + 1 = 1
(1 太小，丟掉)

--- 終止 ---
left = 1, right = 1 → left == right → 迴圈結束
return left = 1

驗證: nums[1] = 2 ✓ 是最左邊的 2！
```

### Example 2: 找右邊界 (rightmost 2)

```
nums = [1, 2, 2, 2, 3], target = 2
index:  0  1  2  3  4

--- Iteration 1 ---
left = 0, right = 5
mid = 0 + (5 - 0) // 2 = 2
nums[2] = 2

[1    2    2    2    3]  |
 L         M         R(虛)
 0    1    2    3    4   5

nums[2] = 2 <= target → left = mid + 1 = 3
(2 <= target，右邊可能還有 2，繼續往右探索)

--- Iteration 2 ---
left = 3, right = 5
mid = 3 + (5 - 3) // 2 = 4
nums[4] = 3

[1    2    2    2    3]  |
                L    M   R(虛)
                3    4   5

nums[4] = 3 > target → right = mid = 4
(3 太大，丟掉)

--- Iteration 3 ---
left = 3, right = 4
mid = 3 + (4 - 3) // 2 = 3
nums[3] = 2

[1    2    2    2    3]
                LM   R
                3    4

nums[3] = 2 <= target → left = mid + 1 = 4
(繼續往右探索)

--- 終止 ---
left = 4, right = 4 → left == right → 迴圈結束
return left - 1 = 4 - 1 = 3

驗證: nums[3] = 2 ✓ 是最右邊的 2！
```

---

## 2.3 Template 3: `while left + 1 < right`（保留兩個候選）

### 定義

```python
def binary_search_t3(nums, target):
    left, right = 0, len(nums) - 1

    while left + 1 < right:          # 終止: left 和 right 相鄰
        mid = left + (right - left) // 2

        if nums[mid] == target:
            right = mid              # 或 left = mid (看要找左界還是右界)
        elif nums[mid] < target:
            left = mid               # 注意: 不是 mid + 1！
        else:
            right = mid              # 注意: 不是 mid - 1！

    # 後處理: 檢查 left 和 right 哪個是答案
    if nums[left] == target:
        return left
    if nums[right] == target:
        return right
    return -1
```

### 關鍵細節

| 項目 | 說明 |
|------|------|
| 搜尋區間 | left 和 right 之間至少隔一個元素 |
| 終止條件 | `left + 1 == right`，left 和 right 相鄰 |
| 縮小範圍 | `left = mid` 或 `right = mid`（不加減 1，因為 mid 不會等於 left 或 right） |
| 後處理 | 必須！迴圈結束後 left 和 right 都可能是答案，需要檢查 |
| 優點 | 不容易死迴圈（因為 mid 永遠嚴格在 left 和 right 之間） |
| 缺點 | 需要後處理，多寫幾行 |

### Example 1: 找確切值

```
nums = [1, 3, 5, 7, 9, 11], target = 7
index:  0  1  2  3  4   5

--- Iteration 1 ---
left = 0, right = 5
left + 1 = 1 < 5 = right ✓ 繼續
mid = 0 + (5 - 0) // 2 = 2
nums[2] = 5

[1    3    5    7    9    11]
 L         M               R
 0    1    2    3    4     5

5 < 7 → left = mid = 2

--- Iteration 2 ---
left = 2, right = 5
left + 1 = 3 < 5 = right ✓ 繼續
mid = 2 + (5 - 2) // 2 = 3
nums[3] = 7

[1    3    5    7    9    11]
            L    M          R
            2    3    4     5

7 == 7 → right = mid = 3 (往左找看還有沒有)

--- Iteration 3 ---
left = 2, right = 3
left + 1 = 3 = right → 不滿足 left + 1 < right → 迴圈結束

後處理:
- nums[left] = nums[2] = 5 ≠ 7
- nums[right] = nums[3] = 7 == 7 ✓
return 3
```

### Example 2: target 不存在

```
nums = [1, 3, 5, 7, 9, 11], target = 6
index:  0  1  2  3  4   5

--- Iteration 1 ---
left = 0, right = 5, mid = 2
nums[2] = 5 < 6 → left = 2

--- Iteration 2 ---
left = 2, right = 5, mid = 3
nums[3] = 7 > 6 → right = 3

--- 終止 ---
left = 2, right = 3 → left + 1 == right → 迴圈結束

後處理:
- nums[2] = 5 ≠ 6
- nums[3] = 7 ≠ 6
return -1 (沒找到)
```

---

## 2.4 三種模板並排比較表

| | Template 1 | Template 2 | Template 3 |
|---|---|---|---|
| **迴圈條件** | `left <= right` | `left < right` | `left + 1 < right` |
| **初始 right** | `len(nums) - 1` | `len(nums)` | `len(nums) - 1` |
| **搜尋區間** | `[left, right]` 閉 | `[left, right)` 半開 | `(left, right)` 開 |
| **終止時** | `left > right` | `left == right` | `left + 1 == right` |
| **left 更新** | `mid + 1` | `mid + 1` | `mid` |
| **right 更新** | `mid - 1` | `mid` | `mid` |
| **後處理** | 不需要 | 檢查 `left` | 檢查 `left` 和 `right` |
| **適用** | 找確切值 | 找邊界 | 任何(防死迴圈) |
| **死迴圈風險** | 無 | 中（注意 mid 計算） | 無 |

### 同一題用三種模板解 — LC 704 Binary Search

```python
# 題目: 在排序陣列中找 target，找到回傳 index，沒找到回傳 -1
# nums = [1, 3, 5, 7, 9], target = 5

# --- Template 1 ---
left, right = 0, 4          # [0, 4] 閉區間
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == 5: return mid
    elif nums[mid] < 5: left = mid + 1
    else: right = mid - 1

# --- Template 2 ---
left, right = 0, 5          # [0, 5) 半開區間
while left < right:
    mid = left + (right - left) // 2
    if nums[mid] < 5: left = mid + 1
    else: right = mid
# 結束時 left == right，檢查 nums[left] == 5?

# --- Template 3 ---
left, right = 0, 4
while left + 1 < right:
    mid = left + (right - left) // 2
    if nums[mid] < 5: left = mid
    elif nums[mid] > 5: right = mid
    else: return mid         # 或 left/right = mid
# 結束後檢查 nums[left] 和 nums[right]
```

### 建議

```
面試時的選擇策略:

1. 找確切值 → Template 1 (最直覺)
2. 找左邊界 / 右邊界 / 插入位置 → Template 2 (最常用)
3. 不確定邊界怎麼處理、怕死迴圈 → Template 3 (最安全)

Google 面試最常考: Template 2 的邊界變形
建議: Template 1 + Template 2 都要滾瓜爛熟
```

---

# 第三章：標準題目

## 3.1 Search Insert Position (LC 35)

**題目**：給定排序陣列和 target，找到 target 的 index。如果不在，回傳應該插入的位置。

**核心觀察**：這就是「找第一個 >= target 的位置」= Left Bound！

```python
def searchInsert(nums, target):
    left, right = 0, len(nums)     # Template 2

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
```

### Example 1: target 存在

```
nums = [1, 3, 5, 6], target = 5
index:  0  1  2  3

--- Iteration 1 ---
left = 0, right = 4, mid = 2
nums[2] = 5

[1    3    5    6]  |
 L         M    R(虛)
 0    1    2    3   4

5 >= 5 → right = mid = 2

--- Iteration 2 ---
left = 0, right = 2, mid = 1
nums[1] = 3

[1    3    5    6]
 L    M    R
 0    1    2

3 < 5 → left = mid + 1 = 2

--- 終止 ---
left = 2, right = 2 → return 2

nums[2] = 5 ✓ target 就在 index 2
```

### Example 2: target 不存在（要插入）

```
nums = [1, 3, 5, 6], target = 2
index:  0  1  2  3

--- Iteration 1 ---
left = 0, right = 4, mid = 2
nums[2] = 5 >= 2 → right = 2

--- Iteration 2 ---
left = 0, right = 2, mid = 1
nums[1] = 3 >= 2 → right = 1

--- Iteration 3 ---
left = 0, right = 1, mid = 0
nums[0] = 1 < 2 → left = 1

--- 終止 ---
left = 1, right = 1 → return 1

意思: 2 應該插入到 index 1（在 1 和 3 之間）
驗證: [1, 2, 3, 5, 6] ✓
```

---

## 3.2 Find First and Last Position of Element (LC 34)

**題目**：在排序陣列中找 target 的第一個和最後一個位置。如果不存在，回傳 [-1, -1]。

**核心觀察**：分別做一次「找左邊界」和「找右邊界」。

```python
def searchRange(nums, target):
    def findLeft(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    def findRight(nums, target):
        left, right = 0, len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] <= target:  # 注意 <=
                left = mid + 1
            else:
                right = mid
        return left - 1              # 注意 -1

    l = findLeft(nums, target)
    r = findRight(nums, target)

    if l <= r and l < len(nums) and nums[l] == target:
        return [l, r]
    return [-1, -1]
```

### Example 1: target 存在多個

```
nums = [5, 7, 7, 8, 8, 8, 10], target = 8
index:  0  1  2  3  4  5   6

=== 找左邊界 (first 8) ===

--- Iteration 1 ---
left = 0, right = 7, mid = 3
nums[3] = 8 >= 8 → right = 3

--- Iteration 2 ---
left = 0, right = 3, mid = 1
nums[1] = 7 < 8 → left = 2

--- Iteration 3 ---
left = 2, right = 3, mid = 2
nums[2] = 7 < 8 → left = 3

--- 終止 ---
left = 3, right = 3 → findLeft returns 3 ✓ (第一個 8)

=== 找右邊界 (last 8) ===

--- Iteration 1 ---
left = 0, right = 7, mid = 3
nums[3] = 8 <= 8 → left = 4

--- Iteration 2 ---
left = 4, right = 7, mid = 5
nums[5] = 8 <= 8 → left = 6

--- Iteration 3 ---
left = 6, right = 7, mid = 6
nums[6] = 10 > 8 → right = 6

--- 終止 ---
left = 6, right = 6 → findRight returns 6 - 1 = 5 ✓ (最後一個 8)

結果: [3, 5]
驗證: nums[3]=8, nums[4]=8, nums[5]=8 ✓
```

### Example 2: target 不存在

```
nums = [5, 7, 7, 8, 8, 10], target = 6
index:  0  1  2  3  4   5

=== 找左邊界 ===

--- Iteration 1 ---
left = 0, right = 6, mid = 3
nums[3] = 8 >= 6 → right = 3

--- Iteration 2 ---
left = 0, right = 3, mid = 1
nums[1] = 7 >= 6 → right = 1

--- Iteration 3 ---
left = 0, right = 1, mid = 0
nums[0] = 5 < 6 → left = 1

--- 終止 ---
findLeft returns 1

=== 找右邊界 ===

--- Iteration 1 ---
left = 0, right = 6, mid = 3
nums[3] = 8 > 6 → right = 3

--- Iteration 2 ---
left = 0, right = 3, mid = 1
nums[1] = 7 > 6 → right = 1

--- Iteration 3 ---
left = 0, right = 1, mid = 0
nums[0] = 5 <= 6 → left = 1

--- 終止 ---
findRight returns 1 - 1 = 0

檢查: l=1, r=0 → l > r → return [-1, -1] ✓ (6 不存在)
```

---

# 第四章：旋轉數組 (Rotated Array)

## 4.1 為什麼旋轉數組很棘手？

原始排序陣列旋轉後，變成兩段各自排序的子陣列：

```
原始:  [0, 1, 2, 3, 4, 5, 6, 7]

旋轉 4 次:
       [4, 5, 6, 7, 0, 1, 2, 3]
        ← 遞增 →  ← 遞增 →
        高段部分    低段部分

圖形化 (值 vs index):

值
7 |         *
6 |      *
5 |   *
4 | *
3 |                        *
2 |                     *
1 |                  *
0 |               *
  +--+--+--+--+--+--+--+--
    0  1  2  3  4  5  6  7  index

  看起來像一座「山」→ 先上升，突然下降，再上升
```

**關鍵觀察**：`mid` 切一刀，左半 `[left, mid]` 和右半 `[mid, right]` 至少有一半是排序的！

```
情況 A: mid 在高段          情況 B: mid 在低段
  *                              *
 * *                            * *
*   *                          *   *
     * ← mid 在這裡                  * ← mid 在這裡
      *                              *
       *                               *
左半排序 ✓, 右半不確定      左半不確定, 右半排序 ✓
```

## 4.2 Search in Rotated Sorted Array (LC 33)

**題目**：在旋轉排序陣列中搜尋 target，找到回傳 index，沒找到回傳 -1。陣列無重複。

**決策邏輯**：

```
1. 找 mid
2. 判斷哪半邊是排序的:
   - if nums[left] <= nums[mid] → 左半排序
   - else → 右半排序
3. 判斷 target 是否在排序的那半邊:
   - 如果在 → 搜尋那半邊
   - 如果不在 → 搜尋另一半邊
```

```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # 左半排序?
        if nums[left] <= nums[mid]:
            # target 在左半的排序範圍內?
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # 右半排序
        else:
            # target 在右半的排序範圍內?
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

### Example 1: target = 0（在低段）

```
nums = [4, 5, 6, 7, 0, 1, 2], target = 0
index:  0  1  2  3  4  5  6

--- Iteration 1 ---
left = 0, right = 6
mid = 3, nums[3] = 7

[4    5    6    7    0    1    2]
 L              M              R
 0    1    2    3    4    5    6

nums[0]=4 <= nums[3]=7 → 左半 [4,5,6,7] 是排序的
target=0 在 [4, 7) 範圍內? 4 <= 0? No!
→ target 不在左半 → left = mid + 1 = 4

--- Iteration 2 ---
left = 4, right = 6
mid = 5, nums[5] = 1

[4    5    6    7    0    1    2]
                     L    M    R
                     4    5    6

nums[4]=0 <= nums[5]=1 → 左半 [0,1] 是排序的
target=0 在 [0, 1) 範圍內? 0 <= 0 < 1? Yes!
→ right = mid - 1 = 4

--- Iteration 3 ---
left = 4, right = 4
mid = 4, nums[4] = 0

[4    5    6    7    0    1    2]
                    LMR
                     4

0 == 0 → 找到！return 4 ✓
```

### Example 2: target = 3（不存在）

```
nums = [4, 5, 6, 7, 0, 1, 2], target = 3
index:  0  1  2  3  4  5  6

--- Iteration 1 ---
left = 0, right = 6, mid = 3
nums[3] = 7

nums[0]=4 <= nums[3]=7 → 左半排序
4 <= 3? No → target 不在左半 → left = 4

--- Iteration 2 ---
left = 4, right = 6, mid = 5
nums[5] = 1

nums[4]=0 <= nums[5]=1 → 左半排序
0 <= 3 < 1? No (3 不小於 1) → target 不在左半 → left = 6

--- Iteration 3 ---
left = 6, right = 6, mid = 6
nums[6] = 2

2 ≠ 3
nums[6]=2 <= nums[6]=2 → 左半排序 (只有一個元素)
2 <= 3 < 2? No → left = 7

--- 終止 ---
left = 7 > right = 6 → return -1 ✓ (3 不在陣列中)
```

---

## 4.3 Find Minimum in Rotated Sorted Array (LC 153)

**題目**：找旋轉排序陣列中的最小值。無重複。

**核心觀察**：最小值是「斷裂點」。用 `nums[mid]` 跟 `nums[right]` 比較：

```
如果 nums[mid] > nums[right] → 最小值在右半邊 (mid 在高段)
如果 nums[mid] <= nums[right] → 最小值在左半邊 (包含 mid)
```

```python
def findMin(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1        # 最小值在 mid 右邊
        else:
            right = mid           # mid 可能就是最小值

    return nums[left]
```

### Example 1: 有旋轉

```
nums = [3, 4, 5, 1, 2]
index:  0  1  2  3  4

--- Iteration 1 ---
left = 0, right = 4
mid = 2, nums[2] = 5

[3    4    5    1    2]
 L         M         R
 0    1    2    3    4

nums[2]=5 > nums[4]=2 → 最小值在右半 → left = 3

--- Iteration 2 ---
left = 3, right = 4
mid = 3, nums[3] = 1

[3    4    5    1    2]
                L    R
                3    4

nums[3]=1 <= nums[4]=2 → mid 可能是最小值 → right = 3

--- 終止 ---
left = 3, right = 3 → return nums[3] = 1 ✓
```

### Example 2: 沒有旋轉（或旋轉了 n 次回到原位）

```
nums = [1, 2, 3, 4, 5]
index:  0  1  2  3  4

--- Iteration 1 ---
left = 0, right = 4, mid = 2
nums[2] = 3

nums[2]=3 <= nums[4]=5 → right = 2

--- Iteration 2 ---
left = 0, right = 2, mid = 1
nums[1] = 2

nums[1]=2 <= nums[2]=3 → right = 1

--- Iteration 3 ---
left = 0, right = 1, mid = 0
nums[0] = 1

nums[0]=1 <= nums[1]=2 → right = 0

--- 終止 ---
left = 0, right = 0 → return nums[0] = 1 ✓
```

---

# 第五章：答案二分 (Binary Search on Answer) — Google 最愛

## 5.1 概念：在答案空間上做二分搜尋

前面的二分搜尋都是「在陣列上搜尋」。答案二分是另一個維度：

```
傳統二分: 在 nums 裡找 target
          搜尋空間 = 陣列的 index

答案二分: 答案在某個範圍 [lo, hi] 內
          搜尋空間 = 答案的可能值
          用 check(mid) 判斷 mid 是否可行
```

**框架**：

```python
def binary_search_on_answer():
    lo, hi = min_possible_answer, max_possible_answer

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if check(mid):     # mid 可行嗎?
            hi = mid        # 可行 → 試試更小的 (找最小可行答案)
        else:
            lo = mid + 1    # 不可行 → 要更大

    return lo

def check(mid):
    # 根據題意，判斷 mid 是否是可行的答案
    # 回傳 True / False
    pass
```

**關鍵**：check(mid) 必須具有單調性！

```
答案空間:  [lo .................... hi]
check():    F  F  F  F  T  T  T  T  T
                        ↑
                  找這個分界點 = 最小可行答案
```

## 5.2 Koko Eating Bananas (LC 875)

**題目**：Koko 有 n 堆香蕉 `piles[i]`。她每小時吃 speed 根。如果那堆不夠 speed 根，她吃完那堆就停下等下一小時。守衛 h 小時後回來。求最小的 speed 使得 Koko 能在 h 小時內吃完。

**分析**：

```
speed 太小 → 來不及吃完 → check = False
speed 太大 → 可以吃完但不是最小 → check = True
speed 剛好 → 臨界點 → 這是我們要找的！

搜尋空間: speed ∈ [1, max(piles)]
check(speed): 以 speed 的速度，能在 h 小時內吃完嗎？
  total_hours = sum(ceil(pile / speed) for pile in piles)
  return total_hours <= h
```

```python
import math

def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = lo + (hi - lo) // 2

        # check: 以 mid 速度能吃完嗎?
        hours = sum(math.ceil(p / mid) for p in piles)

        if hours <= h:
            hi = mid        # 可以吃完 → 試更慢的速度
        else:
            lo = mid + 1    # 來不及 → 要更快

    return lo
```

### Example 1: piles = [3, 6, 7, 11], h = 8

```
搜尋空間: speed ∈ [1, 11]

--- Iteration 1 ---
lo = 1, hi = 11
mid = 1 + (11-1)//2 = 6

check(6): 每小時吃 6 根
  pile=3:  ceil(3/6)  = 1 小時
  pile=6:  ceil(6/6)  = 1 小時
  pile=7:  ceil(7/6)  = 2 小時
  pile=11: ceil(11/6) = 2 小時
  total = 1+1+2+2 = 6 小時 <= 8 ✓

hours=6 <= h=8 → 可以！但也許更慢也行 → hi = 6

--- Iteration 2 ---
lo = 1, hi = 6
mid = 1 + (6-1)//2 = 3

check(3): 每小時吃 3 根
  pile=3:  ceil(3/3)  = 1 小時
  pile=6:  ceil(6/3)  = 2 小時
  pile=7:  ceil(7/3)  = 3 小時
  pile=11: ceil(11/3) = 4 小時
  total = 1+2+3+4 = 10 小時 > 8 ✗

hours=10 > h=8 → 太慢！→ lo = 4

--- Iteration 3 ---
lo = 4, hi = 6
mid = 4 + (6-4)//2 = 5

check(5): 每小時吃 5 根
  pile=3:  ceil(3/5)  = 1 小時
  pile=6:  ceil(6/5)  = 2 小時
  pile=7:  ceil(7/5)  = 2 小時
  pile=11: ceil(11/5) = 3 小時
  total = 1+2+2+3 = 8 小時 <= 8 ✓

hours=8 <= h=8 → 可以！→ hi = 5

--- Iteration 4 ---
lo = 4, hi = 5
mid = 4 + (5-4)//2 = 4

check(4): 每小時吃 4 根
  pile=3:  ceil(3/4)  = 1 小時
  pile=6:  ceil(6/4)  = 2 小時
  pile=7:  ceil(7/4)  = 2 小時
  pile=11: ceil(11/4) = 3 小時
  total = 1+2+2+3 = 8 小時 <= 8 ✓

hours=8 <= h=8 → 可以！→ hi = 4

--- 終止 ---
lo = 4, hi = 4 → return 4

答案: speed = 4 ✓
驗證: [3,6,7,11] 以速度 4 → [1,2,2,3] = 8 小時，剛好！
```

### Example 2: piles = [30, 11, 23, 4, 20], h = 5

```
搜尋空間: speed ∈ [1, 30]

--- Iteration 1 ---
lo=1, hi=30, mid=15
check(15): ceil(30/15)+ceil(11/15)+ceil(23/15)+ceil(4/15)+ceil(20/15)
         = 2 + 1 + 2 + 1 + 2 = 8 > 5 ✗ → lo = 16

--- Iteration 2 ---
lo=16, hi=30, mid=23
check(23): ceil(30/23)+ceil(11/23)+ceil(23/23)+ceil(4/23)+ceil(20/23)
         = 2 + 1 + 1 + 1 + 1 = 6 > 5 ✗ → lo = 24

--- Iteration 3 ---
lo=24, hi=30, mid=27
check(27): ceil(30/27)+ceil(11/27)+ceil(23/27)+ceil(4/27)+ceil(20/27)
         = 2 + 1 + 1 + 1 + 1 = 6 > 5 ✗ → lo = 28

--- Iteration 4 ---
lo=28, hi=30, mid=29
check(29): ceil(30/29)+ceil(11/29)+ceil(23/29)+ceil(4/29)+ceil(20/29)
         = 2 + 1 + 1 + 1 + 1 = 6 > 5 ✗ → lo = 30

--- 終止 ---
lo=30, hi=30 → return 30

答案: speed = 30 ✓
驗證: 每堆最多 30，一小時一堆，5堆5小時剛好！
```

---

## 5.3 Split Array Largest Sum (LC 410) — Google Hard

**題目**：將陣列分成 k 個非空連續子陣列，使得這 k 個子陣列的「最大和」最小化。

**分析**：

```
直覺: 把「最大子陣列和」當作答案來二分搜尋！

搜尋空間: answer ∈ [max(nums), sum(nums)]
  - 最小可能: 每個元素自己一組，最大和 = max(nums)
  - 最大可能: 全部一組，最大和 = sum(nums)

check(max_sum): 限制每組和 <= max_sum，能分成 <= k 組嗎?
  - 貪心法: 從左到右累加，超過 max_sum 就開新一組
```

```python
def splitArray(nums, k):
    lo, hi = max(nums), sum(nums)

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if check(nums, mid, k):
            hi = mid        # 可行 → 試更小的 max_sum
        else:
            lo = mid + 1    # 不可行 → 需要更大的 max_sum

    return lo

def check(nums, max_sum, k):
    """限制每組和 <= max_sum，能分成 <= k 組嗎？"""
    groups = 1
    current_sum = 0

    for num in nums:
        if current_sum + num > max_sum:
            groups += 1
            current_sum = num
        else:
            current_sum += num

    return groups <= k
```

### Example 1: nums = [7, 2, 5, 10, 8], k = 2

```
搜尋空間: [max(10), sum(32)] = [10, 32]

--- Iteration 1 ---
lo=10, hi=32, mid=21

check(21, k=2): 每組和 <= 21
  current=0, groups=1
  +7  → current=7   (7<=21 ✓)
  +2  → current=9   (9<=21 ✓)
  +5  → current=14  (14<=21 ✓)
  +10 → current=24  (24>21 ✗) → groups=2, current=10
  +8  → current=18  (18<=21 ✓)
  groups=2 <= k=2 ✓

→ hi = 21

--- Iteration 2 ---
lo=10, hi=21, mid=15

check(15, k=2): 每組和 <= 15
  current=0, groups=1
  +7  → current=7
  +2  → current=9
  +5  → current=14  (14<=15 ✓)
  +10 → current=24  (24>15 ✗) → groups=2, current=10
  +8  → current=18  (18>15 ✗) → groups=3, current=8
  groups=3 > k=2 ✗

→ lo = 16

--- Iteration 3 ---
lo=16, hi=21, mid=18

check(18, k=2): 每組和 <= 18
  +7 → 7, +2 → 9, +5 → 14, +10 → 24>18 → groups=2, current=10
  +8 → 18 <= 18 ✓
  groups=2 <= 2 ✓

→ hi = 18

--- Iteration 4 ---
lo=16, hi=18, mid=17

check(17, k=2): 每組和 <= 17
  +7 → 7, +2 → 9, +5 → 14, +10 → 24>17 → groups=2, current=10
  +8 → 18 > 17 → groups=3
  groups=3 > 2 ✗

→ lo = 18

--- 終止 ---
lo=18, hi=18 → return 18

答案: 18
分法: [7, 2, 5] (sum=14) 和 [10, 8] (sum=18) → max = 18 ✓
```

### Example 2: nums = [1, 2, 3, 4, 5], k = 3

```
搜尋空間: [5, 15]

--- Iteration 1 ---
lo=5, hi=15, mid=10
check(10, k=3):
  +1→1, +2→3, +3→6, +4→10, +5→15>10 → groups=2, current=5
  groups=2 <= 3 ✓ → hi=10

--- Iteration 2 ---
lo=5, hi=10, mid=7
check(7, k=3):
  +1→1, +2→3, +3→6, +4→10>7 → groups=2, current=4
  +5→9>7 → groups=3, current=5
  groups=3 <= 3 ✓ → hi=7

--- Iteration 3 ---
lo=5, hi=7, mid=6
check(6, k=3):
  +1→1, +2→3, +3→6, +4→10>6 → groups=2, current=4
  +5→9>6 → groups=3, current=5
  groups=3 <= 3 ✓ → hi=6

--- Iteration 4 ---
lo=5, hi=6, mid=5
check(5, k=3):
  +1→1, +2→3, +3→6>5 → groups=2, current=3
  +4→7>5 → groups=3, current=4
  +5→9>5 → groups=4, current=5
  groups=4 > 3 ✗ → lo=6

--- 終止 ---
lo=6, hi=6 → return 6

答案: 6
分法: [1,2,3] (sum=6) 和 [4] (sum=4) 和 [5] (sum=5) → max=6 ✓
```

---

# 第六章：矩陣二分

## 6.1 Search a 2D Matrix (LC 74)

**題目**：m x n 矩陣，每行遞增，且每行第一個元素大於上一行最後一個元素。判斷 target 是否存在。

**核心觀察**：把 2D 矩陣攤平看成 1D 排序陣列！

```
矩陣:                         攤平:
[[ 1,  3,  5,  7],           [1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]
 [10, 11, 16, 20],            index: 0  1  2  3  4   5   6   7   8   9  10  11
 [23, 30, 34, 60]]

轉換公式:
  1D index → 2D: row = index // cols, col = index % cols
  例: index=7 → row = 7//4 = 1, col = 7%4 = 3 → matrix[1][3] = 20
```

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        row, col = mid // n, mid % n
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

### Example 1: target 存在

```
matrix = [[1, 3, 5, 7],
          [10,11,16,20],
          [23,30,34,60]]
target = 3
m=3, n=4, 總共 12 個元素

--- Iteration 1 ---
left=0, right=11, mid=5
row = 5//4 = 1, col = 5%4 = 1
matrix[1][1] = 11

11 > 3 → right = 4

--- Iteration 2 ---
left=0, right=4, mid=2
row = 2//4 = 0, col = 2%4 = 2
matrix[0][2] = 5

5 > 3 → right = 1

--- Iteration 3 ---
left=0, right=1, mid=0
row = 0//4 = 0, col = 0%4 = 0
matrix[0][0] = 1

1 < 3 → left = 1

--- Iteration 4 ---
left=1, right=1, mid=1
row = 1//4 = 0, col = 1%4 = 1
matrix[0][1] = 3

3 == 3 → return True ✓
```

### Example 2: target 不存在

```
matrix = [[1, 3, 5, 7],
          [10,11,16,20],
          [23,30,34,60]]
target = 13

--- Iteration 1 ---
left=0, right=11, mid=5
matrix[1][1] = 11 < 13 → left = 6

--- Iteration 2 ---
left=6, right=11, mid=8
matrix[2][0] = 23 > 13 → right = 7

--- Iteration 3 ---
left=6, right=7, mid=6
matrix[1][2] = 16 > 13 → right = 5

--- 終止 ---
left=6 > right=5 → return False ✓ (13 不在矩陣中)
```

---

## 6.2 Search a 2D Matrix II (LC 240) — 階梯法

**題目**：m x n 矩陣，每行遞增，每列遞增（但行首不一定大於上一行行尾）。

```
matrix = [[1,  4,  7, 11, 15],
          [2,  5,  8, 12, 19],
          [3,  6,  9, 16, 22],
          [10,13, 14, 17, 24],
          [18,21, 23, 26, 30]]

注意: 5 > 4 但 2 < 4，所以不能攤平成 1D！
```

**核心觀察**：從右上角出發（或左下角），像走樓梯一樣搜尋。

```
從右上角 (row=0, col=n-1) 出發:
- 如果 matrix[row][col] == target → 找到！
- 如果 matrix[row][col] > target → 往左走 (col--)
    (當前值太大，同一列下面只會更大，所以排除整列)
- 如果 matrix[row][col] < target → 往下走 (row++)
    (當前值太小，同一行左邊只會更小，所以排除整行)

每一步排除一行或一列 → O(m + n)
```

```python
def searchMatrixII(matrix, target):
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1    # 從右上角出發

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1        # 往左（排除一列）
        else:
            row += 1        # 往下（排除一行）

    return False
```

### Example 1: target = 5

```
matrix = [[ 1,  4,  7, 11, 15],
          [ 2,  5,  8, 12, 19],
          [ 3,  6,  9, 16, 22],
          [10, 13, 14, 17, 24],
          [18, 21, 23, 26, 30]]

起點: row=0, col=4 → matrix[0][4] = 15

--- Step 1 ---
(0,4) = 15 > 5 → 往左 col=3

  [ 1,  4,  7, [11], 15]    ← 排除 col=4
     ...

--- Step 2 ---
(0,3) = 11 > 5 → 往左 col=2

  [ 1,  4, [ 7], 11, 15]    ← 排除 col=3

--- Step 3 ---
(0,2) = 7 > 5 → 往左 col=1

  [ 1, [ 4],  7, 11, 15]    ← 排除 col=2

--- Step 4 ---
(0,1) = 4 < 5 → 往下 row=1

  [ 1,  4, ...]              ← 排除 row=0
  [ 2, [5], ...]

--- Step 5 ---
(1,1) = 5 == 5 → return True ✓

路徑視覺化 (用 * 標記走過的位置):
  [ 1,  *,  *,  *, *→15]
  [ 2, [5], 8, 12, 19]   ← 找到！
```

### Example 2: target = 20

```
matrix = [[ 1,  4,  7, 11, 15],
          [ 2,  5,  8, 12, 19],
          [ 3,  6,  9, 16, 22],
          [10, 13, 14, 17, 24],
          [18, 21, 23, 26, 30]]

--- Step 1 --- (0,4)=15 < 20 → 往下 row=1
--- Step 2 --- (1,4)=19 < 20 → 往下 row=2
--- Step 3 --- (2,4)=22 > 20 → 往左 col=3
--- Step 4 --- (2,3)=16 < 20 → 往下 row=3
--- Step 5 --- (3,3)=17 < 20 → 往下 row=4
--- Step 6 --- (4,3)=26 > 20 → 往左 col=2
--- Step 7 --- (4,2)=23 > 20 → 往左 col=1
--- Step 8 --- (4,1)=21 > 20 → 往左 col=0
--- Step 9 --- (4,0)=18 < 20 → 往下 row=5

row=5 >= m=5 → 超出矩陣 → return False ✓ (20 不在矩陣中)

路徑:
  [ 1,  4,  7, 11, *15]
  [ 2,  5,  8, 12, *19]
  [ 3,  6,  9, *16,*22]
  [10, 13, 14, *17, 24]
  [*18,*21,*23,*26, 30]
                       ↓ 出界

共 9 步 (m + n - 1 = 5 + 5 - 1 = 9，最壞情況)
```

---

# 第七章：面試決策框架

## 7.1 模板選擇決策樹

```
你需要二分搜尋嗎?
│
├─ 搜尋空間有單調性嗎? → No → 不適用二分搜尋
│
└─ Yes
    │
    ├─ 在陣列中找確切值?
    │   └─ Template 1: while left <= right
    │      回傳 mid 或 -1
    │
    ├─ 在陣列中找邊界 (第一個/最後一個)?
    │   └─ Template 2: while left < right
    │      左邊界: nums[mid] < target → left = mid+1; else right = mid
    │      右邊界: nums[mid] <= target → left = mid+1; else right = mid; return left-1
    │
    ├─ 旋轉數組?
    │   └─ Template 1: while left <= right
    │      判斷哪半排序 → target 在排序半嗎?
    │
    ├─ 答案二分 (搜尋空間不是陣列而是數值範圍)?
    │   └─ Template 2: while lo < hi
    │      定義 check(mid)，找最小可行答案
    │
    └─ 不確定 / 怕死迴圈?
        └─ Template 3: while left + 1 < right
           結束後檢查 left 和 right
```

## 7.2 識別「答案二分」的信號

```
看到以下關鍵字 → 很可能是答案二分:

1. "最小化最大值" (minimize the maximum)
   → LC 410 Split Array Largest Sum
   → LC 1011 Capacity To Ship Packages Within D Days

2. "最大化最小值" (maximize the minimum)
   → LC 1552 Magnetic Force Between Two Balls

3. "最少/最多需要多少" + 範圍很大 (10^9)
   → LC 875 Koko Eating Bananas
   → LC 1283 Find the Smallest Divisor

4. 答案有上下界且具有單調性
   → 答案越大越容易滿足 (或反過來)
```

## 7.3 常見陷阱與除錯

### 陷阱 1: 無限迴圈 (Infinite Loop)

```
發生原因: left 和 right 無法收斂

危險情境 (Template 2):
  left = 3, right = 4
  mid = 3 + (4-3)//2 = 3   ← mid == left！
  如果走 left = mid → left 還是 3 → 永遠不收斂！

解法:
  - 找左邊界: mid = left + (right-left)//2    (偏左，搭配 left = mid+1)
  - 找右邊界: mid = left + (right-left+1)//2  (偏右，搭配 right = mid-1)

  或者直接用 Template 3 避免問題。
```

### 陷阱 2: Off-by-One Error

```
常見錯誤:
1. right 初始值: len(nums) 還是 len(nums)-1?
   → Template 1: len(nums)-1 (閉區間)
   → Template 2: len(nums)   (半開區間)

2. 返回值: left 還是 left-1?
   → 找左邊界: return left
   → 找右邊界: return left-1

3. 邊界檢查: return 前要確認 index 在合法範圍內！
   → if left < len(nums) and nums[left] == target
```

### 陷阱 3: 旋轉數組的等號

```
nums[left] <= nums[mid]   (有等號！)
                ↑
不是 <，是 <=。因為 left 可能等於 mid (只剩兩個元素時)。
少了等號 → 判斷「哪半排序」會出錯。
```

## 7.4 Whiteboard 面試策略

```
Step 1: 確認問題 (1-2 min)
  - 輸入是排序的嗎？有重複嗎？
  - 要找什麼？確切值？邊界？最佳答案？
  - 搜尋空間是什麼？陣列 index？數值範圍？

Step 2: 選擇模板 (30 sec)
  - 用決策樹選模板
  - 跟面試官確認思路

Step 3: 寫程式 (5-8 min)
  - 先寫框架 (while 迴圈 + mid 計算)
  - 再填條件 (if/else 的邏輯)
  - 最後處理返回值

Step 4: Trace 一個例子 (2-3 min)
  - 用一個小例子手動跑一遍
  - 確認邊界情況

Step 5: 分析複雜度 (30 sec)
  - 時間: O(log n) 或 O(n log n) (答案二分中 check 是 O(n))
  - 空間: O(1)
```

## 7.5 複雜度速查表

| 題型 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 標準二分搜尋 | O(log n) | O(1) |
| 找左/右邊界 | O(log n) | O(1) |
| 旋轉數組搜尋 | O(log n) | O(1) |
| 旋轉數組找最小 | O(log n) | O(1) |
| 答案二分 (Koko) | O(n log M), M=max(piles) | O(1) |
| 答案二分 (Split Array) | O(n log S), S=sum(nums) | O(1) |
| 2D Matrix (LC 74) | O(log(m*n)) | O(1) |
| 2D Matrix II (LC 240) | O(m + n) | O(1) |

## 7.6 本章題目清單（建議刷題順序）

```
=== 入門 (先做) ===
[ ] LC 704  Binary Search                        ← Template 1 基礎
[ ] LC 35   Search Insert Position                ← Template 2 入門
[ ] LC 34   First and Last Position               ← 左右邊界

=== 進階 ===
[ ] LC 33   Search in Rotated Sorted Array        ← 旋轉數組
[ ] LC 153  Find Minimum in Rotated Sorted Array  ← 旋轉找最小
[ ] LC 74   Search a 2D Matrix                    ← 矩陣二分
[ ] LC 240  Search a 2D Matrix II                 ← 階梯法

=== Google 高頻 (必做) ===
[ ] LC 875  Koko Eating Bananas                   ← 答案二分入門
[ ] LC 410  Split Array Largest Sum               ← 答案二分 Hard
[ ] LC 1011 Capacity To Ship Packages             ← 答案二分變形

=== 挑戰 ===
[ ] LC 4    Median of Two Sorted Arrays           ← Hard 經典
[ ] LC 162  Find Peak Element                     ← 非排序二分
[ ] LC 1283 Find the Smallest Divisor             ← 答案二分
```

---

## 附錄：全章節公式與模板速查

```
╔═══════════════════════════════════════════════════════════╗
║                 Binary Search 速查卡                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  防溢位 mid:  mid = left + (right - left) // 2            ║
║                                                           ║
║  Template 1 (找確切值):                                    ║
║    while left <= right:                                   ║
║      if nums[mid] == target: return mid                   ║
║      elif nums[mid] < target: left = mid + 1              ║
║      else: right = mid - 1                                ║
║    return -1                                              ║
║                                                           ║
║  Template 2 (找邊界):                                      ║
║    左邊界: while left < right:                             ║
║      if nums[mid] < target: left = mid + 1                ║
║      else: right = mid                                    ║
║      return left                                          ║
║                                                           ║
║    右邊界: while left < right:                             ║
║      if nums[mid] <= target: left = mid + 1               ║
║      else: right = mid                                    ║
║      return left - 1                                      ║
║                                                           ║
║  答案二分:                                                 ║
║    while lo < hi:                                         ║
║      if check(mid): hi = mid                              ║
║      else: lo = mid + 1                                   ║
║    return lo                                              ║
║                                                           ║
║  旋轉數組:                                                 ║
║    if nums[left] <= nums[mid]: 左半排序                    ║
║    else: 右半排序                                          ║
║                                                           ║
║  2D → 1D: row = index // cols, col = index % cols         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```
