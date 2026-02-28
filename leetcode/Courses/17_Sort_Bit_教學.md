# 排序演算法 + 位元運算 完全教學 (Sorting Algorithms + Bit Manipulation)

> **適用對象**：LeetCode 初學者，準備 Google 面試
> **前置知識**：Array 基本操作、遞迴（Recursion）概念、Python 基礎
> **配套程式**：`17_Sort_And_Bit.py`（可直接執行看 step-by-step trace）
> **教學風格**：教科書級，每個概念至少 2 個完整數值範例 + 逐步計算

---

## 目錄

### Part A：排序演算法
- [第一章：為什麼要學排序？](#第一章為什麼要學排序)
- [第二章：基礎排序 O(n^2) -- 理解概念即可](#第二章基礎排序-on2----理解概念即可)
- [第三章：Merge Sort -- 面試必會](#第三章merge-sort----面試必會)
- [第四章：Quick Sort -- 面試必會](#第四章quick-sort----面試必會)
- [第五章：排序應用題](#第五章排序應用題)
- [第六章：排序比較表與面試決策指南](#第六章排序比較表與面試決策指南)

### Part B：位元運算
- [第七章：位元基礎 -- 從零開始](#第七章位元基礎----從零開始)
- [第八章：位元應用題](#第八章位元應用題)

---

# Part A：排序演算法 (Sorting Algorithms)

---

# 第一章：為什麼要學排序？

### 1.1 排序是一切的基礎

很多演算法題目的前提是「資料已經排好序」。例如：

| 題目類型 | 為什麼需要排序？ |
|---------|-----------------|
| **Binary Search** | 前提就是 sorted array |
| **Two Pointers** | 排序後才能用左右指標夾逼 |
| **Merge Intervals** | 排序後才能線性掃描合併 |
| **找第 K 大/小** | Quick Select 來自 Quick Sort 的 partition |
| **Custom Order** | 自訂 comparator 排序（如 LC 179） |

### 1.2 面試怎麼考排序？

Google 面試中排序的考法：

1. **直接考**：「請從零實作 merge sort」-- 考你能不能不看任何提示寫出來
2. **間接考**：題目本身需要排序作為前處理步驟
3. **變形考**：在特殊條件下排序（如 Sort Colors 只有 0/1/2 三種值）
4. **分析考**：「你的解法時間複雜度是什麼？為什麼？」-- 你得懂 O(n log n) 怎麼來的

---

# 第二章：基礎排序 O(n^2) -- 理解概念即可

> 這三種排序面試不會直接考實作，但它們的**核心動作**是理解進階排序的基礎。

---

## 2.1 Bubble Sort（泡沫排序）

**核心思想**：相鄰元素兩兩比較，如果順序錯了就交換。每一輪把最大的元素「冒泡」到最右邊。

```
每一輪的動作：
從左到右掃描，比較 arr[j] 和 arr[j+1]
如果 arr[j] > arr[j+1]，就交換它們
```

### 範例 1：[5, 3, 1, 4, 2]

```
=== Pass 1：把最大值 5 冒泡到最右邊 ===
[5, 3, 1, 4, 2]  compare 5 > 3? Yes → swap → [3, 5, 1, 4, 2]
[3, 5, 1, 4, 2]  compare 5 > 1? Yes → swap → [3, 1, 5, 4, 2]
[3, 1, 5, 4, 2]  compare 5 > 4? Yes → swap → [3, 1, 4, 5, 2]
[3, 1, 4, 5, 2]  compare 5 > 2? Yes → swap → [3, 1, 4, 2, 5]  ← 5 到位

=== Pass 2：把次大值 4 冒泡 ===
[3, 1, 4, 2, 5]  compare 3 > 1? Yes → swap → [1, 3, 4, 2, 5]
[1, 3, 4, 2, 5]  compare 3 > 4? No           [1, 3, 4, 2, 5]
[1, 3, 4, 2, 5]  compare 4 > 2? Yes → swap → [1, 3, 2, 4, 5]  ← 4 到位

=== Pass 3：把 3 冒泡 ===
[1, 3, 2, 4, 5]  compare 1 > 3? No           [1, 3, 2, 4, 5]
[1, 3, 2, 4, 5]  compare 3 > 2? Yes → swap → [1, 2, 3, 4, 5]  ← 3 到位

=== Pass 4：檢查 ===
[1, 2, 3, 4, 5]  compare 1 > 2? No → 沒有任何交換 → 提前結束!

結果: [1, 2, 3, 4, 5] ✓
```

### 範例 2：[2, 1, 3, 2]

```
Pass 1: [2,1,3,2] → swap(2,1) → [1,2,3,2] → no swap → swap(3,2) → [1,2,2,3]
Pass 2: [1,2,2,3] → no swaps → 提前結束!
結果: [1, 2, 2, 3] ✓
```

**Bubble Sort 特性**：Time O(n^2), Space O(1), **Stable: Yes**, In-place: Yes

---

## 2.2 Selection Sort（選擇排序）

**核心思想**：每次從未排序的部分找出**最小值**，放到已排序部分的末尾。

```
每一輪的動作：
在 arr[i..n-1] 中找到最小值的 index
把它和 arr[i] 交換
```

### 範例 1：[5, 3, 1, 4, 2]

```
=== Pass 1：在 [5,3,1,4,2] 中找最小值 ===
最小值 = 1 (index = 2)，swap arr[0] ↔ arr[2]
[5, 3, 1, 4, 2] → [1, 3, 5, 4, 2]    已排序: [1]

=== Pass 2：在 [3,5,4,2] 中找最小值 ===
最小值 = 2 (index = 4)，swap arr[1] ↔ arr[4]
[1, 3, 5, 4, 2] → [1, 2, 5, 4, 3]    已排序: [1, 2]

=== Pass 3：在 [5,4,3] 中找最小值 ===
最小值 = 3 (index = 4)，swap arr[2] ↔ arr[4]
[1, 2, 5, 4, 3] → [1, 2, 3, 4, 5]    已排序: [1, 2, 3]

=== Pass 4：在 [4,5] 中找最小值 ===
最小值 = 4 (index = 3)，已在正確位置
[1, 2, 3, 4, 5] → [1, 2, 3, 4, 5]    已排序: [1, 2, 3, 4]

結果: [1, 2, 3, 4, 5] ✓
```

### 範例 2：[8, 4, 2, 6]

```
Pass 1: min=2(idx=2), swap arr[0]↔arr[2] → [2, 4, 8, 6]
Pass 2: min=4(idx=1), 已在正確位置       → [2, 4, 8, 6]
Pass 3: min=6(idx=3), swap arr[2]↔arr[3] → [2, 4, 6, 8] ✓
```

**Selection Sort 特性**：Time O(n^2) always, Space O(1), **Stable: No**, In-place: Yes

> **為什麼不穩定？** [5a, 3, 5b, 1]，Pass 1 把 1 和 5a 交換 → [1, 3, 5b, 5a]。5a 跑到 5b 後面了。

---

## 2.3 Insertion Sort（插入排序）

**核心思想**：像打撲克牌整理手牌一樣，每次拿起一張新牌，**插入**到已排好的牌中正確位置。

```
每一輪的動作：
拿起 arr[i]（key）
往左看，把比 key 大的元素往右移一格
找到 key 該放的位置，放下去
```

### 範例 1：[5, 3, 1, 4, 2]

```
初始: [5, 3, 1, 4, 2]    已排序: [5]    手上拿: -

=== Round 1: 拿起 arr[1] = 3 ===
  [5, _, 1, 4, 2]   3 < 5? Yes → 5 右移  → [_, 5, 1, 4, 2]
  沒有更左的了 → 放下 3
  [3, 5, 1, 4, 2]   已排序: [3, 5]

=== Round 2: 拿起 arr[2] = 1 ===
  [3, 5, _, 4, 2]   1 < 5? Yes → 5 右移  → [3, _, 5, 4, 2]
                     1 < 3? Yes → 3 右移  → [_, 3, 5, 4, 2]
  沒有更左的了 → 放下 1
  [1, 3, 5, 4, 2]   已排序: [1, 3, 5]

=== Round 3: 拿起 arr[3] = 4 ===
  [1, 3, 5, _, 2]   4 < 5? Yes → 5 右移  → [1, 3, _, 5, 2]
                     4 < 3? No → 放下 4
  [1, 3, 4, 5, 2]   已排序: [1, 3, 4, 5]

=== Round 4: 拿起 arr[4] = 2 ===
  [1, 3, 4, 5, _]   2 < 5? Yes → 5 右移  → [1, 3, 4, _, 5]
                     2 < 4? Yes → 4 右移  → [1, 3, _, 4, 5]
                     2 < 3? Yes → 3 右移  → [1, _, 3, 4, 5]
                     2 < 1? No → 放下 2
  [1, 2, 3, 4, 5]   已排序: [1, 2, 3, 4, 5]

結果: [1, 2, 3, 4, 5] ✓
```

### 範例 2：[3, 1, 4, 1]

```
Round 1: 拿起 1。1<3 → 3 右移 → 放下 1       → [1, 3, 4, 1]
Round 2: 拿起 4。4<3? No → 放下 4             → [1, 3, 4, 1]
Round 3: 拿起 1。1<4 → 移, 1<3 → 移, 1<1? No → [1, 1, 3, 4] ✓
```

**Insertion Sort 特性**：Time O(n^2) worst, O(n) best (already sorted), Space O(1), **Stable: Yes**, In-place: Yes

> **什麼時候最好？** 資料「幾乎已排序」時接近 O(n)。Python 的 Timsort 就利用了這個特性。

---

## 2.4 基礎排序比較

| 排序 | 最佳 | 平均 | 最差 | Space | Stable? | 什麼時候有用？ |
|------|------|------|------|-------|---------|-------------|
| Bubble | O(n) | O(n^2) | O(n^2) | O(1) | Yes | 教學用，幾乎不實用 |
| Selection | O(n^2) | O(n^2) | O(n^2) | O(1) | No | swap 次數最少 (最多 n-1 次) |
| Insertion | O(n) | O(n^2) | O(n^2) | O(1) | Yes | 幾乎排好的資料、小規模資料 |

---

# 第三章：Merge Sort -- 面試必會

## 3.1 核心思想：Divide and Conquer（分治法）

1. **Divide**：把陣列從中間切成兩半
2. **Conquer**：遞迴地對左半和右半分別排序
3. **Combine**：把兩個已排好的半邊合併成一個排好的陣列

**直覺**：兩疊已排好的撲克牌，每次比較牌頂，拿小的放到結果中，就完成合併了。

## 3.2 為什麼是 O(n log n)？

```
Level 0: [████████]           → 1組 × 8元素
Level 1: [████]  [████]       → 2組 × 4元素   每一層合併時
Level 2: [██][██] [██][██]    → 4組 × 2元素   每個元素被處理一次
Level 3: [][][][]  [][][][]   → 8組 × 1元素   → 每層 O(n) 工作

層數 = log₂(n)，每層 O(n) → 總計 O(n log n)
```

## 3.3 Merge Process 詳解（兩個指標合併）

合併兩個已排序陣列是 Merge Sort 的關鍵。兩個指標 i, j 各指向左右陣列的開頭，每次取較小的放入結果：

```
left = [3, 27, 38]    right = [9, 10, 82]    result = []

Step 1: 3 vs 9  → 取3  [3]              Step 4: 27 vs 82 → 取27 [3,9,10,27]
Step 2: 27 vs 9 → 取9  [3,9]            Step 5: 38 vs 82 → 取38 [3,9,10,27,38]
Step 3: 27 vs 10→ 取10 [3,9,10]         Step 6: left用完 → 加82 [3,9,10,27,38,82]
```

```python
def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= 保證穩定性
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

> **穩定性（Stability）**：值相同的元素，排序後保持原始相對順序。Merge Sort 用 `<=` 比較時是穩定的。

---

## 3.4 完整 Merge Sort 程式碼

```python
def merge_sort(arr):
    if len(arr) <= 1:        # Base case: 0 或 1 個元素已經排好了
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # 遞迴排左半
    right = merge_sort(arr[mid:])   # 遞迴排右半
    return merge(left, right)       # 合併兩個已排序的半邊
```

---

## 3.5 範例 1：[38, 27, 43, 3, 9, 82, 10] -- 完整追蹤

```
=== 分割階段（Divide）===

Level 0: [38, 27, 43, 3, 9, 82, 10]
          ↙                     ↘
Level 1: [38, 27, 43, 3]        [9, 82, 10]
          ↙          ↘            ↙        ↘
Level 2: [38, 27]   [43, 3]    [9, 82]    [10]
          ↙   ↘      ↙   ↘      ↙   ↘
Level 3: [38] [27]  [43] [3]  [9]  [82]   [10]

每個陣列只剩 1 個元素 → 已排好（base case）

=== 合併階段（Merge）===

--- Level 3 → Level 2 ---

merge([38], [27]):
  38 vs 27 → 27 < 38, 取 27 → 38 剩餘 → [27, 38] ✓

merge([43], [3]):
  43 vs 3 → 3 < 43, 取 3 → 43 剩餘 → [3, 43] ✓

merge([9], [82]):
  9 vs 82 → 9 < 82, 取 9 → 82 剩餘 → [9, 82] ✓

[10] 只有一個 → [10] ✓

--- Level 2 → Level 1 ---

merge([27, 38], [3, 43]):
  27 vs 3  → 取 3   result=[3]
  27 vs 43 → 取 27  result=[3, 27]
  38 vs 43 → 取 38  result=[3, 27, 38]
  43 剩餘          result=[3, 27, 38, 43] ✓

merge([9, 82], [10]):
  9 vs 10  → 取 9   result=[9]
  82 vs 10 → 取 10  result=[9, 10]
  82 剩餘          result=[9, 10, 82] ✓

--- Level 1 → Level 0 ---

merge([3, 27, 38, 43], [9, 10, 82]):
  3  vs 9  → 取 3   result=[3]
  27 vs 9  → 取 9   result=[3, 9]
  27 vs 10 → 取 10  result=[3, 9, 10]
  27 vs 82 → 取 27  result=[3, 9, 10, 27]
  38 vs 82 → 取 38  result=[3, 9, 10, 27, 38]
  43 vs 82 → 取 43  result=[3, 9, 10, 27, 38, 43]
  82 剩餘          result=[3, 9, 10, 27, 38, 43, 82] ✓

最終結果: [3, 9, 10, 27, 38, 43, 82]
```

## 3.6 範例 2：[5, 1, 4, 2, 8]

```
=== 分割 ===
[5, 1, 4, 2, 8]
  ↙           ↘
[5, 1]       [4, 2, 8]
 ↙  ↘        ↙       ↘
[5] [1]    [4]      [2, 8]
                     ↙   ↘
                   [2]   [8]

=== 合併 ===

merge([5], [1]) → 1 < 5 → [1, 5]

merge([2], [8]) → 2 < 8 → [2, 8]

merge([4], [2, 8]):
  4 vs 2 → 取 2  [2]
  4 vs 8 → 取 4  [2, 4]
  8 剩餘         [2, 4, 8]

merge([1, 5], [2, 4, 8]):
  1 vs 2 → 取 1  [1]
  5 vs 2 → 取 2  [1, 2]
  5 vs 4 → 取 4  [1, 2, 4]
  5 vs 8 → 取 5  [1, 2, 4, 5]
  8 剩餘         [1, 2, 4, 5, 8]

最終結果: [1, 2, 4, 5, 8] ✓
```

## 3.7 Merge Sort 複雜度

Time: **O(n log n)** best/avg/worst（保證不退化，最大優勢）。Space: **O(n)**。**Stable: Yes**。Not in-place。

---

# 第四章：Quick Sort -- 面試必會

## 4.1 核心思想

1. 選一個 **pivot**（樞軸）
2. **Partition**：< pivot 放左邊，> pivot 放右邊
3. 遞迴對左右分別 Quick Sort

> 和 Merge Sort 的區別：Merge Sort 先遞迴後合併（工作在合併時做），Quick Sort 先 partition（就是工作）後遞迴（不需合併）。

## 4.2 Partition 詳解（Lomuto Partition Scheme）

選最後一個元素為 pivot。指標 i 標記「小於 pivot 區域」的右邊界，j 從左掃到右，`arr[j] < pivot` 時 swap 並 i++。最後 pivot 放到 i 的位置。結果：`[< pivot] [pivot] [>= pivot]`

```python
def partition(arr, low, high):
    pivot, i = arr[high], low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i
```

## 4.3 範例 1：[3, 6, 8, 10, 1, 2, 1] -- 完整 Partition 追蹤

選 pivot = arr[6] = 1（最後一個元素）。

```
初始: [3, 6, 8, 10, 1, 2, 1]    pivot = 1, i = 0
       i

j=0: 3 < 1? No    j=1: 6 < 1? No    j=2: 8 < 1? No
j=3: 10 < 1? No   j=4: 1 < 1? No    j=5: 2 < 1? No

→ i 一直沒動（沒有元素 < 1）
→ swap arr[i=0] ↔ arr[6] (pivot)
→ [1, 6, 8, 10, 1, 2, 3]    pivot_index = 0

結果: 左邊 []（空的）, 右邊 [6, 8, 10, 1, 2, 3]
```

> 這個例子展示 pivot 選太小的問題 -- 分割極度不均衡。

## 4.4 範例 2：[10, 7, 8, 9, 1, 5] -- 完整追蹤

選 pivot = arr[5] = 5（最後一個元素）。

```
初始: [10, 7, 8, 9, 1, 5]    pivot = 5, i = 0
       i

j=0: 10 < 5? No     i 不動
j=1: 7 < 5? No      i 不動
j=2: 8 < 5? No      i 不動
j=3: 9 < 5? No      i 不動
j=4: 1 < 5? Yes!    swap arr[i=0] ↔ arr[4] → [1, 7, 8, 9, 10, 5]    i=1

迴圈結束。swap arr[i=1] ↔ arr[5] (pivot):
→ [1, 5, 8, 9, 10, 7]    pivot_index = 1

結果: 左邊 [1], 右邊 [8, 9, 10, 7]
```

接下來遞迴對 [1] 和 [8, 9, 10, 7] 各自做 Quick Sort。

## 4.5 完整 Quick Sort 追蹤：[10, 7, 8, 9, 1, 5]

```
quicksort([10, 7, 8, 9, 1, 5])
  │
  ├─ partition → pivot=5 at index 1 → [1, 5, 8, 9, 10, 7]
  │
  ├─ quicksort([1])              → base case, return [1]
  │
  └─ quicksort([8, 9, 10, 7])
       │
       ├─ partition → pivot=7 at index 0 → [7, 9, 10, 8]
       │
       ├─ quicksort([])           → base case, return []
       │
       └─ quicksort([9, 10, 8])
            │
            ├─ partition → pivot=8 at index 0 → [8, 10, 9]
            │
            ├─ quicksort([])       → base case
            │
            └─ quicksort([10, 9])
                 │
                 ├─ partition → pivot=9 at index 0 → [9, 10]
                 │
                 ├─ quicksort([])   → base case
                 │
                 └─ quicksort([10]) → base case

最終結果: [1, 5, 7, 8, 9, 10] ✓
```

## 4.6 Quick Sort 的最壞情況

```
已排序的 [1, 2, 3, 4, 5]，每次選最後一個為 pivot：
  pivot=5 → [1,2,3,4] + [5] + []     ← 每層只減少 1 個元素
  pivot=4 → [1,2,3] + [4] + []
  pivot=3 → [1,2] + [3] + []
  ...
→ n 層 × O(n) = O(n^2)
```

**解法：隨機選 pivot**，先 `swap(arr[random_idx], arr[high])` 再 partition。

## 4.7 Quick Sort 複雜度

Time: O(n log n) best/avg，**O(n^2) worst**。Space: O(log n) call stack。**Stable: No**。In-place: Yes。

---

# 第五章：排序應用題

---

## 5.1 Sort Colors / Dutch National Flag (LC 75)

**題目**：陣列只有 0, 1, 2 三種值，原地排序。不能用 `sort()`。

**思路**：三個指標 low, mid, high。

```
[0..low-1] 都是0 | [low..mid-1] 都是1 | [mid..high] 未處理 | [high+1..n-1] 都是2
```

**規則**：
- `arr[mid] == 0`：swap(arr[low], arr[mid])，low++, mid++
- `arr[mid] == 1`：mid++
- `arr[mid] == 2`：swap(arr[mid], arr[high])，high--（mid 不動！換來的值還沒檢查）

### 範例 1：[2, 0, 2, 1, 1, 0]

```
初始: low=0, mid=0, high=5
      [2, 0, 2, 1, 1, 0]
       ↑mid            ↑high

Step 1: arr[mid]=2 → swap(arr[0], arr[5]), high--
        [0, 0, 2, 1, 1, 2]    low=0, mid=0, high=4
         ↑mid         ↑high

Step 2: arr[mid]=0 → swap(arr[0], arr[0]), low++, mid++
        [0, 0, 2, 1, 1, 2]    low=1, mid=1, high=4
            ↑mid      ↑high

Step 3: arr[mid]=0 → swap(arr[1], arr[1]), low++, mid++
        [0, 0, 2, 1, 1, 2]    low=2, mid=2, high=4
               ↑mid   ↑high

Step 4: arr[mid]=2 → swap(arr[2], arr[4]), high--
        [0, 0, 1, 1, 2, 2]    low=2, mid=2, high=3
               ↑mid↑high

Step 5: arr[mid]=1 → mid++
        [0, 0, 1, 1, 2, 2]    low=2, mid=3, high=3
                  ↑mid
                  ↑high

Step 6: arr[mid]=1 → mid++
        [0, 0, 1, 1, 2, 2]    low=2, mid=4, high=3

mid > high → 結束!

結果: [0, 0, 1, 1, 2, 2] ✓
```

### 範例 2：[1, 2, 0]

```
初始: low=0, mid=0, high=2
      [1, 2, 0]
       ↑        ↑

Step 1: arr[mid]=1 → mid++
        [1, 2, 0]    low=0, mid=1, high=2

Step 2: arr[mid]=2 → swap(arr[1], arr[2]), high--
        [1, 0, 2]    low=0, mid=1, high=1

Step 3: arr[mid]=0 → swap(arr[0], arr[1]), low++, mid++
        [0, 1, 2]    low=1, mid=2, high=1

mid > high → 結束!

結果: [0, 1, 2] ✓
```

**Python 程式碼**：

```python
def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

Time: O(n), Space: O(1)

---

## 5.2 Merge Sorted Array (LC 88)

**題目**：兩個已排序陣列 nums1（大小 m+n，後面 n 個位置是 0）和 nums2（大小 n），合併到 nums1 中。

**關鍵思路**：從**尾端**開始合併（從右往左填），不會覆蓋 nums1 還沒處理的元素。用三個指標 p1, p2, p 分別指向 nums1 有效部分末尾、nums2 末尾、填入位置末尾。

### 範例 1：nums1 = [1,2,3,0,0,0], m=3, nums2 = [2,5,6], n=3

```
p1=2, p2=2, p=5

Step 1: 3 vs 6 → 6大, 放6到p=5 → [1,2,3,0,0,6]  p2=1, p=4
Step 2: 3 vs 5 → 5大, 放5到p=4 → [1,2,3,0,5,6]  p2=0, p=3
Step 3: 3 vs 2 → 3大, 放3到p=3 → [1,2,3,3,5,6]  p1=1, p=2
Step 4: 2 vs 2 → 等, 放nums2的2 → [1,2,2,3,5,6]  p2=-1

p2 < 0 → 結束! 結果: [1, 2, 2, 3, 5, 6] ✓
```

### 範例 2：nums1 = [4,5,6,0,0,0], m=3, nums2 = [1,2,3], n=3

```
Step 1: 6>3 放6 → [4,5,6,0,0,6]   Step 2: 5>3 放5 → [4,5,6,0,5,6]
Step 3: 4>3 放4 → [4,5,6,4,5,6]   p1<0 → 複製 nums2 剩餘 [1,2,3]
結果: [1, 2, 3, 4, 5, 6] ✓
```

**Python 程式碼**：

```python
def merge(nums1, m, nums2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    # 如果 nums2 還有剩餘，複製過去
    nums1[:p2 + 1] = nums2[:p2 + 1]
```

Time: O(m+n), Space: O(1)

---

## 5.3 Largest Number (LC 179)

**題目**：給一組非負整數，排列成最大的數字。例如 [10, 2] → "210"。

**關鍵思路**：自訂比較器！比較 `str(a)+str(b)` vs `str(b)+str(a)` 哪個比較大。例如 3 vs 30："330" > "303" → 3 排在 30 前面。

### 範例 1：[10, 2]

```
比較 10 和 2：
  "102" vs "210"
  "210" > "102" → 2 排在 10 前面

排列: [2, 10] → "210"

結果: "210" ✓
```

### 範例 2：[3, 30, 34, 5, 9]

```
關鍵比較：
  3 vs 30:  "330" vs "303" → 3 排前面
  3 vs 34:  "334" vs "343" → 34 排前面
  5 vs 9:   "59" vs "95"   → 9 排前面

排序結果: [9, 5, 34, 3, 30] → "9534330" ✓
```

**Python 程式碼**：

```python
from functools import cmp_to_key

def largestNumber(nums):
    # 自訂比較：如果 "ab" > "ba"，a 排前面
    def compare(a, b):
        if a + b > b + a:
            return -1  # a 排前面
        elif a + b < b + a:
            return 1   # b 排前面
        else:
            return 0

    strs = [str(x) for x in nums]
    strs.sort(key=cmp_to_key(compare))

    result = ''.join(strs)
    return '0' if result[0] == '0' else result  # 處理全 0 的情況
```

Time: O(n log n), Space: O(n)

---

# 第六章：排序比較表與面試決策指南

## 6.1 完整排序比較表

| 排序演算法 | Best | Average | Worst | Space | Stable? | In-place? |
|-----------|------|---------|-------|-------|---------|-----------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1) | No | Yes |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| **Merge Sort** | O(n log n) | O(n log n) | **O(n log n)** | **O(n)** | **Yes** | No |
| **Quick Sort** | O(n log n) | O(n log n) | O(n^2) | O(log n) | No | **Yes** |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | No |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) | Yes | No |

## 6.2 面試決策指南

| 需求 | 選擇 |
|------|------|
| 需要穩定排序 | Merge Sort |
| 需要保證 O(n log n) worst case | Merge Sort 或 Heap Sort |
| 記憶體有限（不能 O(n) 空間） | Quick Sort 或 Heap Sort |
| 資料幾乎已排好 | Insertion Sort（接近 O(n)） |
| 值域很小（如只有 0,1,2） | Counting Sort / Dutch National Flag |
| 面試一般情況 | 直接用 `sorted()` / `.sort()`，除非題目要求自己實作 |

## 6.3 Python 的 Timsort

Python 的 `sorted()` / `list.sort()` 使用 **Timsort** = Merge Sort + Insertion Sort 混合。先找自然形成的已排序片段，短片段用 Insertion Sort，再用 Merge Sort 合併。保證 O(n log n) worst case，Stable: Yes。

> 面試中除非題目特別要求你實作排序，否則直接用 `sort()` / `sorted()` 就好。

---

# Part B：位元運算 (Bit Manipulation)

---

# 第七章：位元基礎 -- 從零開始

## 7.1 二進位表示法（Binary Representation）

電腦用**二進位（binary）**儲存數字，只有 0 和 1。

```
十進位 → 二進位                         轉換方法（以 13 為例）：
 0 → 0000    4 → 0100    8 → 1000      13÷2=6...1 → 6÷2=3...0
 1 → 0001    5 → 0101    9 → 1001      3÷2=1...1  → 1÷2=0...1
 2 → 0010    6 → 0110   10 → 1010      從下往上讀：1101
 3 → 0011    7 → 0111                  驗證：8+4+0+1 = 13 ✓
```

## 7.2 六種位元運算子

### AND（&）：兩個都是 1 才是 1

```
規則：0&0=0, 0&1=0, 1&0=0, 1&1=1

範例：5 & 3
  5 = 1 0 1
  3 = 0 1 1
  ─────────
  & = 0 0 1 = 1

口訣：「兩個都亮燈才亮」
用途：檢查某一位是否為 1、清除某些位
```

### OR（|）：任一個是 1 就是 1

```
規則：0|0=0, 0|1=1, 1|0=1, 1|1=1

範例：5 | 3
  5 = 1 0 1
  3 = 0 1 1
  ─────────
  | = 1 1 1 = 7

口訣：「任一個亮燈就亮」
用途：設定某一位為 1
```

### XOR（^）：不同才是 1

```
規則：0^0=0, 0^1=1, 1^0=1, 1^1=0

範例：5 ^ 3
  5 = 1 0 1
  3 = 0 1 1
  ─────────
  ^ = 1 1 0 = 6

口訣：「不一樣才亮」
用途：找出唯一不同的元素、翻轉某些位
```

### NOT（~）：全部翻轉

```
~5 = ...1111 1010    Python 中 ~n = -(n+1)，所以 ~5 = -6
```

### Left Shift（<<）：左移 = 乘以 2

```
3 << 1 = 011 → 110 = 6     (3 × 2)
3 << 2 = 011 → 1100 = 12   (3 × 4)
規則：n << k = n × 2^k
```

### Right Shift（>>）：右移 = 除以 2（向下取整）

```
7 >> 1 = 111 → 011 = 3     (7 ÷ 2 = 3)
12 >> 2 = 1100 → 0011 = 3  (12 ÷ 4 = 3)
規則：n >> k = n ÷ 2^k（向下取整）
```

---

## 7.3 三個超重要的位元技巧

### 技巧 1：n & (n-1) -- 移除最低位的 1

**原理**：n-1 會把 n 的最低位 1 變成 0，並把它右邊的 0 都變成 1。AND 之後就把最低位的 1 消掉了。

```
範例 1: n = 6 = 110
  n-1   = 5 = 101
  n&(n-1) =  100 = 4

  原本：1 1 0
             ↑ 最低位的 1
  結果：1 0 0   ← 被移除了

範例 2: n = 12 = 1100
  n-1    = 11 = 1011
  n&(n-1) =    1000 = 8

  原本：1 1 0 0
           ↑ 最低位的 1
  結果：1 0 0 0   ← 被移除了

範例 3: n = 7 = 111
  n-1   = 6 = 110
  n&(n-1) =  110 = 6

  原本：1 1 1
             ↑ 最低位的 1
  結果：1 1 0   ← 被移除了
```

**應用**：計算 1 的個數、判斷是否為 2 的冪次。

### 技巧 2：n & (-n) -- 取出最低位的 1

```
n = 6 = 110    →  n & (-n) = 010 = 2  （最低位的 1 在第 1 位）
n = 12 = 1100  →  n & (-n) = 0100 = 4 （最低位的 1 在第 2 位）
```

**應用**：Binary Indexed Tree (Fenwick Tree) 中大量使用。

### 技巧 3：XOR 的三大性質

```
性質 1: a ^ a = 0       5 ^ 5 = 000 = 0
性質 2: a ^ 0 = a       5 ^ 0 = 101 = 5
性質 3: 交換律+結合律    a ^ b ^ a = (a^a) ^ b = 0 ^ b = b
→ 重複的會被消掉！這是 Single Number 的核心原理。
```

---

# 第八章：位元應用題

---

## 8.1 Single Number (LC 136)

**題目**：每個元素出現兩次，只有一個出現一次，找出它。**思路**：全部 XOR，重複的消掉，剩下答案。

### 範例 1：[2, 2, 1]

```
result = 0
0 ^ 2 = 2    (000 ^ 010 = 010)
2 ^ 2 = 0    (010 ^ 010 = 000)  ← 兩個 2 消掉了!
0 ^ 1 = 1    (000 ^ 001 = 001)

答案: 1 ✓
```

### 範例 2：[4, 1, 2, 1, 2]

```
0^4=4 → 4^1=5 → 5^2=7 → 7^1=6 → 6^2=4

驗證（交換律）：4 ^ (1^1) ^ (2^2) = 4 ^ 0 ^ 0 = 4 ✓
```

**Python 程式碼**：

```python
def singleNumber(nums):
    result = 0
    for n in nums:
        result ^= n
    return result
```

Time: O(n), Space: O(1)

---

## 8.2 Number of 1 Bits / Hamming Weight (LC 191)

**題目**：計算整數的二進位中有多少個 1。**思路**：反覆 `n & (n-1)` 移除最低位的 1，每次計數 +1。

### 範例 1：n = 11 (二進位 = 1011)

```
count = 0

Round 1: n = 1011
  n-1   = 1010
  n & (n-1) = 1011 & 1010 = 1010    count = 1
  （移除了最右邊的 1）

Round 2: n = 1010
  n-1   = 1001
  n & (n-1) = 1010 & 1001 = 1000    count = 2
  （移除了倒數第二位的 1）

Round 3: n = 1000
  n-1   = 0111
  n & (n-1) = 1000 & 0111 = 0000    count = 3
  （移除了最高位的 1）

n = 0 → 結束

答案: 3（1011 有三個 1）✓
```

### 範例 2：n = 128 (二進位 = 10000000)

```
count = 0

Round 1: n = 10000000
  n-1   = 01111111
  n & (n-1) = 10000000 & 01111111 = 00000000    count = 1

n = 0 → 結束

答案: 1（10000000 只有一個 1）✓
```

**Python 程式碼**：

```python
def hammingWeight(n):
    count = 0
    while n:
        n &= (n - 1)   # 移除最低位的 1
        count += 1
    return count
```

Time: O(k)，k = 1 的個數, Space: O(1)

---

## 8.3 Power of Two (LC 231)

**題目**：判斷 n 是否為 2 的冪次（1, 2, 4, 8, 16, ...）。

**觀察**：2 的冪次在二進位中**只有一個 1**（1=0001, 2=0010, 4=0100, 8=1000）。如果 `n & (n-1) == 0`，表示只有一個 1。

### 範例 1：n = 16

```
n    = 10000
n-1  = 01111
n & (n-1) = 00000 = 0    → 是 2 的冪次 ✓
```

### 範例 2：n = 6

```
n    = 110
n-1  = 101
n & (n-1) = 100 = 4 ≠ 0    → 不是 2 的冪次 ✗
```

**Python 程式碼**：

```python
def isPowerOfTwo(n):
    return n > 0 and (n & (n - 1)) == 0
```

> 注意 n > 0 的檢查！n = 0 時 n & (n-1) = 0 但 0 不是 2 的冪次。

Time: O(1), Space: O(1)

---

## 8.4 Missing Number (LC 268)

**題目**：0 到 n 的數字中少了一個，陣列有 n 個數，找出缺少的那個。

**思路**：XOR 所有的 index（0 到 n）和所有的值，出現兩次的會消掉，剩下的就是缺少的。

```
原理：
  假設 nums = [3, 0, 1]，應該有 0, 1, 2, 3

  XOR 所有 index: 0 ^ 1 ^ 2 ^ 3    （index 0 到 n，n = len(nums) = 3）
  XOR 所有 value: 3 ^ 0 ^ 1

  合起來: (0 ^ 1 ^ 2 ^ 3) ^ (3 ^ 0 ^ 1)
        = (0^0) ^ (1^1) ^ (3^3) ^ 2
        = 0 ^ 0 ^ 0 ^ 2
        = 2                          ← 就是缺少的那個!
```

### 範例 1：nums = [3, 0, 1]

```
n = len(nums) = 3，所以數字應該是 0, 1, 2, 3

result = n = 3

i=0: result ^= i ^ nums[i] = 3 ^ 0 ^ 3 = 0
  3 = 011
  0 = 000
  XOR = 011
  3 = 011
  XOR = 000 = 0

i=1: result ^= i ^ nums[i] = 0 ^ 1 ^ 0 = 1
  0 = 000
  1 = 001
  XOR = 001
  0 = 000
  XOR = 001 = 1

i=2: result ^= i ^ nums[i] = 1 ^ 2 ^ 1 = 2
  1 = 001
  2 = 010
  XOR = 011
  1 = 001
  XOR = 010 = 2

答案: 2 ✓
```

### 範例 2：nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]

```
n=9, result 從 9 開始，逐步 XOR (index ^ value)：
9→0→7→1→0→7→7→6→1→8

答案: 8 ✓  （0~9 中缺少 8）
```

**Python 程式碼**：

```python
def missingNumber(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

Time: O(n), Space: O(1)

---

## 8.5 Subsets using Bitmask (LC 78)

**題目**：給定一組不重複的數字，列出所有子集（power set）。

**思路**：n 個元素有 2^n 個子集。用 0 到 2^n - 1 的二進位數當作遮罩（bitmask），第 i 位是 1 代表取第 i 個元素。

```
核心概念：
  n = 3 個元素 → 2^3 = 8 個子集
  用 000 到 111 的 bitmask 表示每個子集

  bitmask 的第 i 位 = 1 → 取 nums[i]
  bitmask 的第 i 位 = 0 → 不取 nums[i]
```

### 範例：nums = [1, 2, 3]

```
n = 3, 共 2^3 = 8 個子集

bitmask    二進位    意義                  子集
─────────────────────────────────────────────
   0       0 0 0    不取任何元素           []
   1       0 0 1    取 nums[0]=1          [1]
   2       0 1 0    取 nums[1]=2          [2]
   3       0 1 1    取 nums[0,1]          [1, 2]
   4       1 0 0    取 nums[2]=3          [3]
   5       1 0 1    取 nums[0,2]          [1, 3]
   6       1 1 0    取 nums[1,2]          [2, 3]
   7       1 1 1    取 nums[0,1,2]        [1, 2, 3]

詳細 trace（以 bitmask = 5 = 101 為例）：
  bit 0（最右邊）: 1 → 取 nums[0] = 1
  bit 1: 0 → 不取 nums[1]
  bit 2（最左邊）: 1 → 取 nums[2] = 3
  → 子集 = [1, 3]

  怎麼檢查第 i 位是否為 1？
  用 mask & (1 << i) 如果不為 0，表示第 i 位是 1

  mask = 5 = 101
  i=0: 101 & 001 = 001 ≠ 0 → 取 nums[0]=1 ✓
  i=1: 101 & 010 = 000 = 0 → 不取 ✓
  i=2: 101 & 100 = 100 ≠ 0 → 取 nums[2]=3 ✓
```

### 第二個範例：nums = [a, b]

```
mask=0(00):[]  mask=1(01):[a]  mask=2(10):[b]  mask=3(11):[a,b]
```

**Python 程式碼**：

```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):     # 0 到 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):    # 第 i 位是 1 嗎？
                subset.append(nums[i])
        result.append(subset)
    return result
```

Time: O(n * 2^n), Space: O(n * 2^n)

> **面試提示**：Bitmask 方法適合元素數量不大的情況（n <= 20 左右），因為 2^20 = 1,048,576 還可以接受。

---

## 位元運算速查表

| 操作 | 程式碼 | 用途 |
|------|--------|------|
| 檢查第 i 位 | `n & (1 << i)` | 判斷某位是 0 還是 1 |
| 設定第 i 位為 1 | `n \| (1 << i)` | 強制某位為 1 |
| 清除第 i 位 | `n & ~(1 << i)` | 強制某位為 0 |
| 翻轉第 i 位 | `n ^ (1 << i)` | 0 變 1、1 變 0 |
| 移除最低位的 1 | `n & (n-1)` | 計數、判斷 2 的冪次 |
| 取出最低位的 1 | `n & (-n)` | Fenwick Tree |
| 判斷是否為 2 的冪次 | `n > 0 and n & (n-1) == 0` | 只有一個 1 |
| 所有位都是 1？ | `n & (n+1) == 0` | 如 7=111, 15=1111 |
| 乘以 2^k | `n << k` | 快速乘法 |
| 除以 2^k | `n >> k` | 快速除法 |

---

## 總結：本篇重點回顧

### Part A：排序

| 你必須會的 | 程度 |
|-----------|------|
| Merge Sort 完整實作 | 能從零寫出、能分析 O(n log n) |
| Quick Sort 完整實作 | 能寫 partition、知道 worst case |
| 穩定性的意義 | 面試常問 |
| Sort Colors (三指標) | Dutch National Flag 經典題 |
| 自訂 comparator | Python 的 cmp_to_key |

### Part B：位元運算

| 你必須會的 | 程度 |
|-----------|------|
| 六種運算子 | 能手動計算二進位結果 |
| n & (n-1) | 知道它做什麼、三種應用 |
| XOR 性質 | a^a=0, a^0=a |
| Single Number | 秒解 |
| Bitmask 子集 | 能寫出來、知道時間複雜度 |

> **下一步**：配合 `17_Sort_And_Bit.py` 實際執行，看每個範例的 step-by-step 輸出，加深印象。
