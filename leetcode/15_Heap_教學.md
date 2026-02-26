# LeetCode 教學 #15：Heap / Priority Queue 完全攻略

> **適用對象**：LeetCode 初學者，準備 Google 面試
> **前置知識**：Python 基礎（list 語法）、Binary Tree 概念、Big-O
> **配套程式**：`15_Heap_Priority_Queue.py`（可直接執行看 step-by-step trace）

---

## 第一章：Heap 基礎 — 從零開始

### 1.1 什麼是 Heap（堆積）？

**Heap** 是一種特殊的 **Complete Binary Tree（完全二元樹）**，滿足一個簡單的規則：

- **Min Heap（最小堆）**：每個 parent 的值 **<=** 所有 children 的值 → root 一定是**最小值**
- **Max Heap（最大堆）**：每個 parent 的值 **>=** 所有 children 的值 → root 一定是**最大值**

```
Min Heap 範例：                 Max Heap 範例：

       1                              9
      / \                            / \
     3   2                          7   8
    / \                            / \
   7   6                          3   5

每個父節點 <= 子節點              每個父節點 >= 子節點
root = 最小值 = 1                root = 最大值 = 9
```

**注意**：Heap **不是** sorted！左子和右子之間沒有大小關係。上面的 Min Heap 中，左子 3 > 右子 2，這完全合法。Heap 只保證 **parent <= children**（Min Heap）。

**Complete Binary Tree（完全二元樹）** 的定義：
- 每一層都填滿，**除了最後一層**
- 最後一層的節點**靠左對齊**

```
完全二元樹 ✓         不是完全二元樹 ✗

       1                    1
      / \                  / \
     3   2                3   2
    / \                    \
   7   6                    7
                     （最後一層沒有靠左）
```

---

### 1.2 為什麼用 Array 存 Heap？

因為 Complete Binary Tree 的結構非常規律，可以完美對應到 array 的 index：

```
        1            Tree 畫法
       / \
      3   2
     / \
    7   6

Array 畫法（0-indexed）：
index:  [ 0 ][ 1 ][ 2 ][ 3 ][ 4 ]
value:  [ 1 ][ 3 ][ 2 ][ 7 ][ 6 ]
```

**Index 公式**（背起來，面試常用）：

| 關係 | 公式 | 範例（index 1 的節點 = 3） |
|------|------|---------------------------|
| Left Child 左子 | `2 * i + 1` | 2*1+1 = 3 → array[3] = 7 |
| Right Child 右子 | `2 * i + 2` | 2*1+2 = 4 → array[4] = 6 |
| Parent 父節點 | `(i - 1) // 2` | (1-1)//2 = 0 → array[0] = 1 |

**驗證**：index 0 的左子 = 2*0+1 = 1（值 3），右子 = 2*0+2 = 2（值 2），正確！

再看一個大一點的例子：

```
           2
         /   \
        5     7
       / \   /
      8   6 9

Array：
index:  [ 0 ][ 1 ][ 2 ][ 3 ][ 4 ][ 5 ]
value:  [ 2 ][ 5 ][ 7 ][ 8 ][ 6 ][ 9 ]

驗證：
  index 2（值 7）的 left child = 2*2+1 = 5 → array[5] = 9 ✓
  index 4（值 6）的 parent = (4-1)//2 = 1 → array[1] = 5 ✓
```

用 array 的好處：**不需要指標**，直接用 index 算 parent/child，省空間又快。

---

### 1.3 Heap 的核心操作

#### 操作一：heappush — 加入新元素（Bubble Up / Sift Up）

**步驟**：
1. 把新元素放到 array **最後面**（維持 Complete Binary Tree）
2. 跟 parent 比較，如果比 parent 小（Min Heap），就**往上交換**
3. 重複直到 heap property 恢復

**Example 1**：把 `2` 插入 Min Heap `[3, 5, 7, 8, 6]`

```
原始 heap（array = [3, 5, 7, 8, 6]）：

        3
       / \
      5   7
     / \
    8   6

Step 1: 把 2 放到最後面 → array = [3, 5, 7, 8, 6, 2]

        3
       / \
      5   7
     / \ /
    8  6 2     ← 2 在 index 5

Step 2: 2 的 parent = (5-1)//2 = index 2（值 7）
        2 < 7 → 交換！

        3
       / \
      5   2    ← 2 升到 index 2
     / \ /
    8  6 7

    array = [3, 5, 2, 8, 6, 7]

Step 3: 2 的 parent = (2-1)//2 = index 0（值 3）
        2 < 3 → 交換！

        2      ← 2 成為新 root
       / \
      5   3
     / \ /
    8  6 7

    array = [2, 5, 3, 8, 6, 7]

Step 4: 2 已經是 root，沒有 parent → 結束！
```

最終：`[3, 5, 7, 8, 6]` → 插入 2 → `[2, 5, 3, 8, 6, 7]`

**Example 2**：把 `10` 插入 Min Heap `[1, 3, 2, 7, 6]`

```
原始：
        1
       / \
      3   2
     / \
    7   6

Step 1: 放到最後 → array = [1, 3, 2, 7, 6, 10]

        1
       / \
      3   2
     / \ /
    7  6 10    ← 10 在 index 5

Step 2: 10 的 parent = index 2（值 2）
        10 > 2 → 不需要交換 → 結束！

    array = [1, 3, 2, 7, 6, 10]
```

因為 10 比 parent 大，它待在原地就好。Bubble Up 最多走 O(log n) 層。

---

#### 操作二：heappop — 取出最小值（Bubble Down / Sift Down）

**步驟**：
1. 取出 root（最小值）
2. 把 array **最後一個元素**搬到 root
3. 跟兩個 children 中**較小的**比較，如果比它大就**往下交換**
4. 重複直到 heap property 恢復

**Example 1**：從 Min Heap `[2, 5, 3, 8, 6, 7]` 做 heappop

```
Step 1: 取出 root = 2（這就是 return 的值）
        把最後一個元素 7 搬到 root

        7      ← 7 從最後搬到 root
       / \
      5   3
     / \
    8   6

    array = [7, 5, 3, 8, 6]

Step 2: 7 的 children = index 1（值 5）和 index 2（值 3）
        較小的 child = 3（index 2）
        7 > 3 → 交換！

        3
       / \
      5   7    ← 7 降到 index 2
     / \
    8   6

    array = [3, 5, 7, 8, 6]

Step 3: 7 的 children = index 5（不存在）
        沒有 children → 結束！

最終：pop 回傳 2，heap 變成 [3, 5, 7, 8, 6]
```

**Example 2**：從 Min Heap `[1, 4, 2, 8, 5, 6, 3]` 做 heappop

```
原始：
         1
        / \
       4   2
      / \ / \
     8  5 6  3

Step 1: 取出 1，把最後一個 3 搬到 root

         3
        / \
       4   2
      / \ /
     8  5 6

    array = [3, 4, 2, 8, 5, 6]

Step 2: 3 的 children = 4 和 2
        較小的 = 2（index 2）
        3 > 2 → 交換！

         2
        / \
       4   3
      / \ /
     8  5 6

Step 3: 3 的 children = index 5（值 6），index 6（不存在）
        只有一個 child = 6
        3 < 6 → 不交換 → 結束！

最終：pop 回傳 1，heap = [2, 4, 3, 8, 5, 6]
```

---

#### 操作三：heapify — 把任意 array 變成 heap，O(n)

直覺想法：對每個元素做 heappush → O(n log n)。但有更快的方法！

**Heapify 策略**：從最後一個有子節點的 node 開始，**由後往前**做 Bubble Down。

**為什麼是 O(n) 不是 O(n log n)？** 因為大部分節點在底層，底層節點 Bubble Down 的距離短（甚至為 0），只有少數頂層節點需要 Bubble Down 很遠。數學上加總起來是 O(n)。

**Example**：heapify `[9, 4, 7, 1, 3]`

```
先畫成 tree（不管 heap property）：

        9
       / \
      4   7
     / \
    1   3

最後一個有子節點的 index = (5-1)//2 = 2... 不對
  n=5，最後一個有子節點的 = (n//2)-1 = 1

Step 1: 處理 index 1（值 4）
  children: index 3（值 1）, index 4（值 3）
  最小 child = 1
  4 > 1 → 交換

        9
       / \
      1   7
     / \
    4   3

Step 2: 處理 index 0（值 9）
  children: index 1（值 1）, index 2（值 7）
  最小 child = 1
  9 > 1 → 交換

        1
       / \
      9   7
     / \
    4   3

  繼續 bubble down 9：
  9 的 children: index 3（值 4）, index 4（值 3）
  最小 child = 3
  9 > 3 → 交換

        1
       / \
      3   7
     / \
    4   9

  9 沒有更多 children → 結束

最終：array = [1, 3, 7, 4, 9] → 合法 Min Heap ✓
```

---

### 1.4 時間複雜度總整理

| 操作 | 時間複雜度 | 說明 |
|------|-----------|------|
| `heappush` | O(log n) | Bubble Up 最多 log n 層 |
| `heappop` | O(log n) | Bubble Down 最多 log n 層 |
| `peek (heap[0])` | O(1) | 直接讀 root |
| `heapify` | O(n) | 由後往前 Bubble Down |
| `heapreplace` | O(log n) | pop + push 合一 |

---

### 1.5 Python `heapq` 模組 — Min Heap only!

Python 的 `heapq` **只提供 Min Heap**。要用 Max Heap → **存負值**！

```python
import heapq

# === Min Heap 基本操作 ===
h = []
heapq.heappush(h, 5)      # h = [5]
heapq.heappush(h, 3)      # h = [3, 5]
heapq.heappush(h, 8)      # h = [3, 5, 8]
heapq.heappush(h, 1)      # h = [1, 3, 8, 5]

print(h[0])                # 1 — peek 最小值，O(1)
val = heapq.heappop(h)     # val = 1, h = [3, 5, 8]

# === 從現有 list 建 heap ===
arr = [9, 4, 7, 1, 3]
heapq.heapify(arr)         # arr = [1, 3, 7, 9, 4]，O(n)

# === heapreplace: pop 最小 + push 新值（一步完成） ===
old_min = heapq.heapreplace(arr, 6)  # pop 1, push 6

# === nlargest / nsmallest ===
data = [10, 3, 7, 1, 9, 5]
heapq.nlargest(3, data)    # [10, 9, 7]
heapq.nsmallest(3, data)   # [1, 3, 5]
```

**Max Heap 技巧 — 存負值**：

```python
import heapq

# 想要 Max Heap 存 [3, 1, 4, 1, 5]
max_heap = []
for val in [3, 1, 4, 1, 5]:
    heapq.heappush(max_heap, -val)   # 存 -3, -1, -4, -1, -5

# max_heap = [-5, -4, -3, -1, -1]（min heap of negatives）

biggest = -heapq.heappop(max_heap)   # pop -5, 取負 = 5（最大值）
print(biggest)  # 5
```

**Tuple 排序規則**：heapq 比較 tuple 時，先比第一個元素，相同再比第二個：

```python
h = []
heapq.heappush(h, (3, "apple"))
heapq.heappush(h, (1, "banana"))
heapq.heappush(h, (3, "cherry"))
# h[0] = (1, "banana") — 先比數字，1 最小
```

---

## 第二章：Top K 問題 — 面試最常見

面試看到 "Top K" 或 "Kth largest/smallest"，**第一反應就是 Heap**。

核心思路：**維護一個大小為 K 的 heap**，最終 heap 裡剩下的就是 Top K。

---

### 2.1 Kth Largest Element in an Array — LeetCode 215

**題目**：給一個未排序 array `nums` 和整數 `k`，找出第 `k` 大的元素。

**三種方法比較**：

| 方法 | Time | Space | 特點 |
|------|------|-------|------|
| Sort 排序 | O(n log n) | O(n) | 最簡單但最慢 |
| Min Heap of size k | O(n log k) | O(k) | 面試首選 |
| QuickSelect | O(n) avg | O(1) | 最快但 worst case O(n^2) |

**Approach 2（重點）：Min Heap of size k**

思路：
- 維護一個大小最多為 k 的 **Min Heap**
- 遍歷每個元素：
  - heap 沒滿 → 直接 push
  - heap 滿了且新元素 > heap 頂（目前最小）→ replace
  - 否則 skip
- 遍歷完後，heap 頂就是第 k 大

為什麼？heap 裡永遠保留「目前見過最大的 k 個」，heap 頂（最小的那個）正好是第 k 大。

**Example 1**：`nums = [3, 2, 1, 5, 6, 4], k = 2`

```
目標：第 2 大 → 排序後 [1,2,3,4,5,6]，答案 = 5

維護 min heap of size 2：

Step 1: push 3 → heap = [3]              (size=1 < k=2，直接 push)
Step 2: push 2 → heap = [2, 3]           (size=2 = k，滿了)
Step 3: num=1, heap[0]=2, 1 <= 2 → skip  (1 不可能是 top 2)
Step 4: num=5, heap[0]=2, 5 > 2 → replace → heap = [3, 5]
        （踢掉 2，放入 5，heap 自動調整）
Step 5: num=6, heap[0]=3, 6 > 3 → replace → heap = [5, 6]
        （踢掉 3，放入 6）
Step 6: num=4, heap[0]=5, 4 <= 5 → skip  (4 不是 top 2)

最終：heap = [5, 6]，heap[0] = 5 = 第 2 大 ✓
```

**Example 2**：`nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4`

```
目標：第 4 大 → 排序後 [1,2,2,3,3,4,5,5,6]，答案 = 4

Step 1: push 3 → heap = [3]
Step 2: push 2 → heap = [2, 3]
Step 3: push 3 → heap = [2, 3, 3]
Step 4: push 1 → heap = [1, 2, 3, 3]     (size=4=k，滿了)
Step 5: num=2, heap[0]=1, 2 > 1 → replace → heap = [2, 2, 3, 3]
Step 6: num=4, heap[0]=2, 4 > 2 → replace → heap = [2, 3, 3, 4]
Step 7: num=5, heap[0]=2, 5 > 2 → replace → heap = [3, 3, 4, 5]
        （注意 heapreplace 後 heap 自動重排）
Step 8: num=5, heap[0]=3, 5 > 3 → replace → heap = [3, 4, 5, 5]
Step 9: num=6, heap[0]=3, 6 > 3 → replace → heap = [4, 5, 5, 6]

最終：heap[0] = 4 = 第 4 大 ✓
```

**Python 程式碼**：

```python
import heapq

def findKthLargest(nums, k):
    heap = []
    for num in nums:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif num > heap[0]:
            heapq.heapreplace(heap, num)  # pop min + push num
    return heap[0]
```

**Approach 3：QuickSelect — 平均 O(n)**

概念類似 QuickSort，但每次只遞迴一邊：
1. 選 pivot，partition
2. 如果 pivot 位置 = n-k → 找到了
3. 如果 < n-k → 往右找
4. 如果 > n-k → 往左找

面試時 heap 解法更安全（穩定 O(n log k)），QuickSelect 最差 O(n^2)。

---

### 2.2 Top K Frequent Elements — LeetCode 347

**題目**：給一個 array `nums` 和整數 `k`，回傳出現頻率前 k 高的元素。

**步驟**：
1. 用 HashMap（Counter）統計每個元素的出現次數
2. 用 Min Heap of size k 維護頻率最高的 k 個

**Example 1**：`nums = [1,1,1,2,2,3], k = 2`

```
Step 1: 統計頻率
  Counter = {1: 3, 2: 2, 3: 1}

Step 2: Min Heap of size k=2（存 (freq, num) tuple）

  處理 (3, 1): heap size < 2 → push → heap = [(3, 1)]
  處理 (2, 2): heap size < 2 → push → heap = [(2, 2), (3, 1)]
  處理 (1, 3): freq=1, heap[0]=(2,2), 1 <= 2 → skip
               （freq 1 不可能是 top 2）

最終 heap 中的元素 = [2, 1]（freq 前 2 高） ✓
```

**Example 2**：`nums = [4,4,4,6,6,6,2,2,8], k = 3`

```
Step 1: Counter = {4: 3, 6: 3, 2: 2, 8: 1}

Step 2: Min Heap of size k=3

  處理 (3, 4): push → heap = [(3, 4)]
  處理 (3, 6): push → heap = [(3, 4), (3, 6)]
  處理 (2, 2): push → heap = [(2, 2), (3, 6), (3, 4)]  (size=3=k)
  處理 (1, 8): freq=1, heap[0]=(2,2), 1 <= 2 → skip

最終 heap 中的元素 = {4, 6, 2} ✓
```

**Python 程式碼**：

```python
from collections import Counter
import heapq

def topKFrequent(nums, k):
    freq = Counter(nums)
    heap = []
    for num, cnt in freq.items():
        if len(heap) < k:
            heapq.heappush(heap, (cnt, num))
        elif cnt > heap[0][0]:
            heapq.heapreplace(heap, (cnt, num))
    return [num for cnt, num in heap]
```

---

### 2.3 K Closest Points to Origin — LeetCode 973

**題目**：給一組 2D 座標 `points` 和整數 `k`，找出距離原點最近的 `k` 個點。

距離公式：`dist = x^2 + y^2`（不需要開根號，比較大小即可）

**關鍵轉換**：
- 要找「最近的 k 個」→ 用 **Max Heap of size k**
- Python 只有 min heap → 存 **負距離** `(-dist, x, y)`
- 當 heap 滿了，新點的距離比 heap 頂（目前最遠的）近 → replace

**Example 1**：`points = [[1,3],[-2,2],[0,1]], k = 2`

```
距離計算：
  (1,3):  dist = 1+9 = 10
  (-2,2): dist = 4+4 = 8
  (0,1):  dist = 0+1 = 1

Max heap of size k=2（存負距離）：

  處理 (1,3): push (-10, 1, 3) → heap = [(-10, 1, 3)]
  處理 (-2,2): push (-8, -2, 2) → heap = [(-10, 1, 3), (-8, -2, 2)]
              (size=2=k，滿了)
  處理 (0,1): dist=1, 目前 max dist = -heap[0][0] = 10
              1 < 10 → replace!
              pop (-10, 1, 3), push (-1, 0, 1)
              → heap = [(-8, -2, 2), (-1, 0, 1)]

最終：[[-2,2], [0,1]] ← 距離 8 和 1，正確 ✓
```

**Example 2**：`points = [[3,3],[5,-1],[-2,4]], k = 2`

```
距離計算：
  (3,3):  dist = 9+9 = 18
  (5,-1): dist = 25+1 = 26
  (-2,4): dist = 4+16 = 20

Max heap of size k=2：

  處理 (3,3):  push (-18, 3, 3) → heap = [(-18, 3, 3)]
  處理 (5,-1): push (-26, 5, -1) → heap = [(-26, 5, -1), (-18, 3, 3)]
              (size=2=k，滿了。目前最遠 = dist 26)
  處理 (-2,4): dist=20, max dist=26
              20 < 26 → replace!
              pop (-26, 5, -1), push (-20, -2, 4)
              → heap = [(-20, -2, 4), (-18, 3, 3)]

最終：[[-2,4], [3,3]] ← 距離 20 和 18，正確 ✓
（排除了距離 26 的 (5,-1)）
```

**Python 程式碼**：

```python
import heapq

def kClosest(points, k):
    heap = []  # max heap via negation: (-dist, x, y)
    for x, y in points:
        dist = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-dist, x, y))
        elif -dist > heap[0][0]:  # new dist < current max dist
            heapq.heapreplace(heap, (-dist, x, y))
    return [[x, y] for _, x, y in heap]
```

---

## 第三章：合併型（Merge with Heap）

Heap 天生適合「**從多個 sorted 來源中持續取最小值**」的場景。

---

### 3.1 Merge K Sorted Lists — LeetCode 23（Google 高頻）

**題目**：給 `k` 個已排序的 linked list，合併成一個排序的 linked list。

**思路**：
1. 把每個 list 的第一個元素放入 Min Heap
2. Pop 最小的，接到結果 list
3. 把 pop 出來那個 list 的 next element push 進 heap
4. 重複直到 heap 為空

**Time**: O(N log K)，N = 所有節點總數，K = list 數量
**Space**: O(K)（heap 最多存 K 個元素）

**Example 1**：`lists = [[1,4,5], [1,3,4], [2,6]]`

```
初始化：push 每個 list 的第一個元素
  heap = [(1, list0), (1, list1), (2, list2)]
  result = []

Step 1: pop (1, list0) → result = [1]
        list0 的 next = 4 → push (4, list0)
        heap = [(1, list1), (2, list2), (4, list0)]

Step 2: pop (1, list1) → result = [1, 1]
        list1 的 next = 3 → push (3, list1)
        heap = [(2, list2), (4, list0), (3, list1)]

Step 3: pop (2, list2) → result = [1, 1, 2]
        list2 的 next = 6 → push (6, list2)
        heap = [(3, list1), (4, list0), (6, list2)]

Step 4: pop (3, list1) → result = [1, 1, 2, 3]
        list1 的 next = 4 → push (4, list1)
        heap = [(4, list0), (4, list1), (6, list2)]

Step 5: pop (4, list0) → result = [1, 1, 2, 3, 4]
        list0 的 next = 5 → push (5, list0)
        heap = [(4, list1), (6, list2), (5, list0)]

Step 6: pop (4, list1) → result = [1, 1, 2, 3, 4, 4]
        list1 沒有 next → 不 push
        heap = [(5, list0), (6, list2)]

Step 7: pop (5, list0) → result = [1, 1, 2, 3, 4, 4, 5]
        list0 沒有 next → 不 push
        heap = [(6, list2)]

Step 8: pop (6, list2) → result = [1, 1, 2, 3, 4, 4, 5, 6]
        list2 沒有 next → heap 為空 → 結束

最終：1 → 1 → 2 → 3 → 4 → 4 → 5 → 6 ✓
```

**Example 2**：Edge case `lists = [[], [1]]`

```
初始化：
  list0 = [] → 空的，skip
  list1 = [1] → push (1, list1)
  heap = [(1, list1)]

Step 1: pop (1, list1) → result = [1]
        list1 沒有 next → heap 為空 → 結束

最終：1 ✓
```

**Python 程式碼**：

```python
import heapq

def mergeKLists(lists):
    heap = []
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode(0)
    cur = dummy
    counter = len(lists)

    while heap:
        val, idx, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            counter += 1  # tiebreaker，避免 ListNode 比較
            heapq.heappush(heap, (node.next.val, counter, node.next))

    return dummy.next
```

> **注意**：heap 裡存 `(val, counter, node)` 而非 `(val, node)`。因為 Python 比較 tuple 時，如果 val 相同會比較第二個元素。`ListNode` 沒有定義比較運算子，會報錯。用遞增的 `counter` 作為 tiebreaker。

---

### 3.2 Find Median from Data Stream — LeetCode 295（Google Hard 高頻）

**題目**：設計一個資料結構，支援：
- `addNum(num)` — 加入一個整數
- `findMedian()` — 回傳目前所有數字的中位數

**核心思路：Two Heaps（雙堆）**

```
          ┌──────────────┐    ┌──────────────┐
          │  max_heap    │    │  min_heap    │
          │  (左半部)     │    │  (右半部)     │
          │              │    │              │
          │  存較小的數   │    │  存較大的數   │
          │  root = 左半  │    │  root = 右半  │
          │  最大值       │    │  最小值       │
          └──────────────┘    └──────────────┘

規則：
  1. max_heap 的所有值 <= min_heap 的所有值
  2. 大小差最多 1（max_heap 可以多 1 個）

中位數：
  - 奇數個元素 → max_heap 的 root
  - 偶數個元素 → (max_heap root + min_heap root) / 2
```

**Example 1**：依序 addNum(1), addNum(2), findMedian(), addNum(3), findMedian()

```
addNum(1):
  Step 1: push 1 到 max_heap → max_heap = [1]
  Step 2: 檢查 max_heap 的 max <= min_heap 的 min？
          min_heap 是空的 → OK
  Step 3: 大小平衡？ max_heap=1, min_heap=0 → 差1 → OK
  狀態: max_heap = [1], min_heap = []
          ↳ 所有數字: [1]

addNum(2):
  Step 1: push 2 到 max_heap → max_heap = [2, 1]（root=2）
  Step 2: max_heap 的 max=2 > min_heap 的 min？ min_heap 空 → 跳過
          但 max_heap size=2 > min_heap size=0 + 1 → 不平衡！
  Step 3: 把 max_heap 的 root (2) 移到 min_heap
          max_heap = [1], min_heap = [2]
  狀態: max_heap = [1], min_heap = [2]
          ↳ 左半 [1] | 右半 [2]

findMedian():
  max_heap size=1 = min_heap size=1 → 偶數
  median = (1 + 2) / 2 = 1.5 ✓

addNum(3):
  Step 1: push 3 到 max_heap → max_heap = [3, 1]
  Step 2: max_heap 的 max=3 > min_heap 的 min=2 → 違反！
          把 3 從 max_heap 移到 min_heap
          max_heap = [1], min_heap = [2, 3]
  Step 3: min_heap size=2 > max_heap size=1 → 不平衡
          把 min_heap 的 root (2) 移到 max_heap
          max_heap = [2, 1], min_heap = [3]
  狀態: max_heap = [2, 1], min_heap = [3]
          ↳ 左半 [1, 2] | 右半 [3]

findMedian():
  max_heap size=2 > min_heap size=1 → 奇數
  median = max_heap root = 2 ✓
  （排序後 [1,2,3]，中位數確實是 2）
```

**Example 2**：addNum(5), addNum(2), addNum(8), addNum(1), addNum(4)

```
addNum(5):
  max_heap = [5], min_heap = []
  ↳ 所有數字 [5], median = 5

addNum(2):
  push 2 → max_heap = [5, 2]
  size 差 > 1 → move 5 to min_heap
  max_heap = [2], min_heap = [5]
  ↳ 左 [2] | 右 [5], median = (2+5)/2 = 3.5

addNum(8):
  push 8 → max_heap = [8, 2]
  max=8 > min's min=5 → move 8 to min_heap
  max_heap = [2], min_heap = [5, 8]
  min_heap size > max_heap size → move 5 to max_heap
  max_heap = [5, 2], min_heap = [8]
  ↳ 左 [2,5] | 右 [8], median = 5

addNum(1):
  push 1 → max_heap = [5, 2, 1]
  max=5 <= min's min=8 → OK
  max size=3 > min size=1 + 1 → move 5 to min_heap
  max_heap = [2, 1], min_heap = [5, 8]
  ↳ 左 [1,2] | 右 [5,8], median = (2+5)/2 = 3.5

addNum(4):
  push 4 → max_heap = [4, 1, 2]
  max=4 <= min's min=5 → OK
  max size=3 > min size=2 + 1 → move 4 to min_heap
  max_heap = [2, 1], min_heap = [4, 5, 8]
  min size=3 > max size=2 → move 4 to max_heap
  max_heap = [4, 1, 2], min_heap = [5, 8]
  ↳ 左 [1,2,4] | 右 [5,8], median = 4
  （排序 [1,2,4,5,8]，中位數 = 4 ✓）
```

**Python 程式碼**：

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # 左半（存負值）
        self.min_heap = []  # 右半

    def addNum(self, num):
        # Step 1: 先加入 max_heap
        heapq.heappush(self.max_heap, -num)
        # Step 2: 確保 max_heap 的 max <= min_heap 的 min
        if self.min_heap and -self.max_heap[0] > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        # Step 3: 平衡大小
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2
```

---

## 第四章：排程型（Scheduling with Heap）

排程問題常常需要「每次取出優先度最高的任務」→ 天然適合 Heap。

---

### 4.1 Task Scheduler — LeetCode 621

**題目**：有一組 tasks（如 `["A","A","A","B","B","B"]`），冷卻時間 `n`。同一種 task 之間至少要間隔 `n` 個時間單位。求最少需要多少時間。

**思路：Max Heap + Cooldown Queue**
1. 統計每種 task 的頻率，放入 Max Heap
2. 每個 cycle = n+1 個 time slot
3. 每個 cycle 中，從 heap 取出最多 n+1 個 task 執行（頻率高的優先）
4. 執行完的 task 頻率 -1，如果還有剩就暫存
5. Cycle 結束把暫存的放回 heap

**Example 1**：`tasks = ["A","A","A","B","B","B"], n = 2`

```
頻率: A=3, B=3
Max heap (負值): [-3, -3]
每個 cycle 有 n+1 = 3 個 slot

Cycle 1 (t=1~3):
  slot 1: pop -3 (A, 剩餘 2) → 暫存 [-2]
  slot 2: pop -3 (B, 剩餘 2) → 暫存 [-2, -2]
  slot 3: heap 空了 → idle
  time = 3
  push 暫存回 heap → heap = [-2, -2]

Cycle 2 (t=4~6):
  slot 1: pop -2 (A, 剩餘 1) → 暫存 [-1]
  slot 2: pop -2 (B, 剩餘 1) → 暫存 [-1, -1]
  slot 3: heap 空了 → idle
  time = 6
  push back → heap = [-1, -1]

Cycle 3 (t=7~8):
  slot 1: pop -1 (A, 剩餘 0) → 不暫存
  slot 2: pop -1 (B, 剩餘 0) → 不暫存
  slot 3: heap 空 + 暫存空 → cycle 結束
  time = 8

排程結果: A B _ A B _ A B
總時間 = 8 ✓
```

**Example 2**：`tasks = ["A","A","A","A","B","B","C"], n = 2`

```
頻率: A=4, B=2, C=1
Max heap: [-4, -2, -1]

Cycle 1 (n+1=3 slots):
  slot 1: pop -4 (A, 剩餘 3)
  slot 2: pop -2 (B, 剩餘 1)
  slot 3: pop -1 (C, 剩餘 0)
  time = 3, push back [-3, -1]

Cycle 2:
  slot 1: pop -3 (A, 剩餘 2)
  slot 2: pop -1 (B, 剩餘 0)
  slot 3: heap 空 → idle
  time = 6, push back [-2]

Cycle 3:
  slot 1: pop -2 (A, 剩餘 1)
  slot 2: heap 空 → idle
  slot 3: heap 空 → idle (暫存非空，所以要 idle)
  time = 9, push back [-1]

Cycle 4:
  slot 1: pop -1 (A, 剩餘 0)
  time = 10

排程: A B C A B _ A _ _ A
總時間 = 10 ✓
```

**Python 程式碼**：

```python
from collections import Counter
import heapq

def leastInterval(tasks, n):
    freq = Counter(tasks)
    heap = [-cnt for cnt in freq.values()]
    heapq.heapify(heap)

    time = 0
    while heap:
        cycle = []
        for _ in range(n + 1):
            if heap:
                cnt = heapq.heappop(heap)
                if cnt + 1 < 0:      # 還有剩餘
                    cycle.append(cnt + 1)
                time += 1
            elif cycle:
                time += 1            # idle
        for item in cycle:
            heapq.heappush(heap, item)

    return time
```

---

### 4.2 Meeting Rooms II — LeetCode 253

**題目**：給一組會議時間 `intervals = [[start, end], ...]`，求同一時間最多需要幾間會議室。

**思路：Min Heap 存結束時間**
1. 按 start 排序
2. 遍歷每個會議：
   - 如果 heap 頂（最早結束的會議）<= 當前 start → 可以複用那間會議室（pop）
   - 否則需要新的會議室
3. Push 當前會議的 end
4. Heap size = 同時使用的會議室數

**Example 1**：`intervals = [[0,30],[5,10],[15,20]]`

```
排序後: [[0,30],[5,10],[15,20]]

會議 [0,30]:
  heap 空 → 需要新 room
  push end=30 → heap = [30]
  rooms = 1

會議 [5,10]:
  heap[0] = 30 > 5 → 沒有空的 room → 需要新 room
  push end=10 → heap = [10, 30]
  rooms = 2

會議 [15,20]:
  heap[0] = 10 <= 15 → room 空出來了 → 複用！
  pop 10, push end=20 → heap = [20, 30]
  rooms = 2（沒有增加）

最終：2 間會議室 ✓
```

**Example 2**：`intervals = [[9,10],[4,9],[5,17],[2,6]]`

```
排序後: [[2,6],[4,9],[5,17],[9,10]]

會議 [2,6]:
  heap 空 → 新 room
  heap = [6], rooms = 1

會議 [4,9]:
  heap[0]=6 > 4 → 新 room
  heap = [6, 9], rooms = 2

會議 [5,17]:
  heap[0]=6 > 5 → 新 room
  heap = [6, 9, 17], rooms = 3

會議 [9,10]:
  heap[0]=6 <= 9 → 複用！pop 6, push 10
  heap = [9, 10, 17], rooms = 3

最終：3 間會議室 ✓
（時間線上，[2,6], [4,9], [5,17] 三個重疊，需要 3 間）
```

**Python 程式碼**：

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])

    heap = []  # 存每間 room 的結束時間
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)   # 複用
        heapq.heappush(heap, end)

    return len(heap)
```

---

## 第五章：Heap vs Sort vs QuickSelect — 什麼時候用什麼

### 5.1 三種方法比較

```
┌──────────────┬──────────────┬─────────┬──────────────────────────┐
│ 方法         │ Time         │ Space   │ 適用場景                 │
├──────────────┼──────────────┼─────────┼──────────────────────────┤
│ Sort 排序    │ O(n log n)   │ O(n)    │ 需要完整排序結果         │
│              │              │         │ 資料量小、一次性操作     │
│              │              │         │ k 接近 n 時             │
├──────────────┼──────────────┼─────────┼──────────────────────────┤
│ Heap (Top K) │ O(n log k)   │ O(k)   │ 只需前 K 個             │
│              │              │         │ Streaming data（串流）   │
│              │              │         │ k << n 時特別高效       │
├──────────────┼──────────────┼─────────┼──────────────────────────┤
│ QuickSelect  │ O(n) avg     │ O(1)   │ 只需第 K 個（不需排序） │
│              │ O(n^2) worst │         │ 可修改原 array          │
│              │              │         │ 不適合 streaming        │
└──────────────┴──────────────┴─────────┴──────────────────────────┘
```

### 5.2 決策指南

**看到這些關鍵字 → 用 Heap**：
- "Top K"、"Kth largest"、"Kth smallest"
- "Merge K sorted ..."
- "Streaming" 或 "data stream"、"online"
- "Scheduling" + 需要貪心
- "Median" of running data

**看到這些 → 考慮 Sort**：
- 需要完整排序結果
- k 接近 n（heap 沒有速度優勢）
- 資料量很小

**看到這些 → 考慮 QuickSelect**：
- 只要第 K 個元素（不需要前 K 個的列表）
- 可以修改原 array
- 追求平均最佳時間

### 5.3 Streaming Data 一定用 Heap

```
場景：資料不斷流入，隨時要查詢 Top K 或 Median

  數據流: 5, 2, 8, 1, 9, 3, 7, ...
          ↓  ↓  ↓  ↓  ↓  ↓  ↓
       每次加入新數字後，馬上回答 "目前第 3 大是什麼？"

Sort 做法：每次重新排序 → O(n log n) per query → 太慢！
Heap 做法：維護 size-3 min heap → O(log 3) per insert → 超快！
```

### 5.4 常見 Heap 題型速查表

```
┌─────────────────────────────────┬──────────┬──────────────────────┐
│ 題目                            │ Heap 類型 │ 關鍵技巧             │
├─────────────────────────────────┼──────────┼──────────────────────┤
│ LC 215 Kth Largest              │ Min, sz k│ 維護 k 個最大        │
│ LC 347 Top K Frequent           │ Min, sz k│ Counter + heap       │
│ LC 973 K Closest Points         │ Max, sz k│ 負距離               │
│ LC 23  Merge K Sorted Lists     │ Min      │ 多路合併             │
│ LC 295 Find Median (Stream)     │ Two heaps│ max_heap + min_heap  │
│ LC 621 Task Scheduler           │ Max      │ 頻率 + cooldown      │
│ LC 253 Meeting Rooms II         │ Min      │ 結束時間             │
│ LC 767 Reorganize String        │ Max      │ 頻率 + 交替放        │
│ LC 632 Smallest Range K Lists   │ Min      │ 類似 merge k sorted  │
│ LC 378 Kth Smallest in Matrix   │ Min      │ 多路合併             │
│ LC 703 Kth Largest in Stream    │ Min, sz k│ streaming + heap     │
│ LC 1046 Last Stone Weight       │ Max      │ 模擬 + 負值          │
└─────────────────────────────────┴──────────┴──────────────────────┘
```

---

## 附錄：heapq 操作速查表

```
┌──────────────────────────────────┬────────┬──────────────────────────┐
│ 操作                             │ 複雜度 │ 說明                     │
├──────────────────────────────────┼────────┼──────────────────────────┤
│ heapq.heappush(heap, item)       │ O(logn)│ 加入元素                 │
│ heapq.heappop(heap)              │ O(logn)│ 取出並移除最小值         │
│ heap[0]                          │ O(1)   │ 查看最小值（peek）       │
│ heapq.heapify(list)              │ O(n)   │ 原地轉換為 heap          │
│ heapq.heapreplace(heap, item)    │ O(logn)│ pop + push（一步完成）   │
│ heapq.heappushpop(heap, item)    │ O(logn)│ push + pop（一步完成）   │
│ heapq.nlargest(k, iterable)      │O(nlogk)│ 取前 k 大               │
│ heapq.nsmallest(k, iterable)     │O(nlogk)│ 取前 k 小               │
├──────────────────────────────────┼────────┼──────────────────────────┤
│ Max Heap 技巧:                   │        │                          │
│   heapq.heappush(h, -val)        │        │ push 負值                │
│   -heapq.heappop(h)              │        │ pop 後取負還原           │
├──────────────────────────────────┼────────┼──────────────────────────┤
│ Tuple 排序:                      │        │                          │
│   heapq.heappush(h, (pri, data)) │        │ 先比 pri，相同再比 data  │
│   用 counter 作 tiebreaker       │        │ 避免 data 無法比較       │
├──────────────────────────────────┼────────┼──────────────────────────┤
│ heapreplace vs heappushpop:      │        │                          │
│   heapreplace: 先 pop 再 push    │        │ 保證 pop 的是舊 min      │
│   heappushpop: 先 push 再 pop    │        │ x 最小會直接回傳 x      │
└──────────────────────────────────┴────────┴──────────────────────────┘
```

**面試口訣**：

> 1. 看到 "Top K" → Min Heap of size K
> 2. 看到 "Merge K sorted" → Min Heap of size K
> 3. 看到 "Data Stream + Median" → Two Heaps
> 4. 看到 "Scheduling" → Max Heap of frequencies
> 5. Python 只有 Min Heap → Max Heap 用負值！
