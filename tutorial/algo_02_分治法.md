# 演算法教學 02：分治法 (Divide and Conquer)

> 台大演算法課教學講義
> 分治法是演算法設計中最基礎也最優雅的範式之一。它的核心思想簡單到只有三個字：拆、解、合。

---

## 1. 分治法的框架

### 1.1 三步驟

每個分治演算法都遵循同樣的三步驟：

1. **Divide（分）：** 把原問題拆成若干個規模較小的**同類型**子問題
2. **Conquer（治）：** 遞迴地解決每個子問題；當子問題夠小時直接解決（base case）
3. **Combine（合）：** 把子問題的解合併成原問題的解

```
DIVIDE-AND-CONQUER(problem):
    if problem is small enough:        // base case
        solve directly and return

    subproblems = DIVIDE(problem)       // Step 1: Divide

    for each subproblem in subproblems: // Step 2: Conquer
        subsolution = DIVIDE-AND-CONQUER(subproblem)

    solution = COMBINE(subsolutions)    // Step 3: Combine
    return solution
```

### 1.2 時間分析

分治法的時間複雜度通常可以寫成：

$$
T(n) = a \cdot T\!\left(\frac{n}{b}\right) + f(n)
$$

其中：
- **a** = 子問題的數量
- **n/b** = 每個子問題的大小
- **f(n)** = Divide + Combine 的工作量

然後就可以用 Master Theorem 來解這個遞迴式（詳見教學 01）。

---

## 2. 設計分治演算法的思路

### 2.1 何時適用分治法？

分治法適合以下情況：

1. **問題可以自然地拆成同類型的子問題** ─ 如陣列可以拆成左半和右半
2. **子問題之間是獨立的** ─ 解一個子問題不需要另一個子問題的結果
3. **合併步驟有效率** ─ 合併不能太慢，否則省不了時間
4. **問題具有某種「結構遞迴性」** ─ 小問題和大問題有相同的結構

### 2.2 何時不適用？

1. **子問題重疊（overlapping subproblems）** ─ 這時應該用 DP
2. **無法有效合併** ─ 有些問題拆開容易，合起來卻很難
3. **問題不能自然拆分** ─ 例如某些圖論問題
4. **Greedy 就能解決** ─ 不需要遞迴

### 2.3 分治法 vs 動態規劃 (DP) 的判斷

| 特徵 | 分治法 | DP |
|------|--------|-----|
| 子問題是否重疊 | 不重疊（獨立） | 重疊（同一子問題被算很多次） |
| 解法方向 | 通常 top-down | 通常 bottom-up（也可 top-down + memo） |
| 典型例子 | Merge Sort, Quick Sort | LCS, Knapsack |
| 時間節省方式 | 減少工作量 | 避免重複計算 |

**關鍵判斷：** 把遞迴樹畫出來，如果不同分支會算到「同一個子問題」，那就是 DP 的場景。

---

## 3. 經典分治演算法

### 3.1 Merge Sort（合併排序）

#### 觀念

Merge Sort 的想法簡單到令人感動：

1. 把陣列分成左半和右半
2. 分別排序左半和右半（遞迴）
3. 把兩個已排序的陣列合併成一個已排序的陣列

#### 虛擬碼

```
MERGE-SORT(A, p, r):
    if p < r:                          // 至少兩個元素
        q = floor((p + r) / 2)        // 中間點
        MERGE-SORT(A, p, q)           // 排序左半
        MERGE-SORT(A, q+1, r)         // 排序右半
        MERGE(A, p, q, r)             // 合併

MERGE(A, p, q, r):
    // 建立暫存陣列
    L = A[p..q]       // 左半複製
    R = A[q+1..r]     // 右半複製
    在 L 和 R 末端加上哨兵 ∞

    i = 1, j = 1
    for k = p to r:
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1
```

#### Step-by-step 範例

排序陣列 A = [38, 27, 43, 3, 9, 82, 10]

```
原始：[38, 27, 43, 3, 9, 82, 10]

Divide:
  左半：[38, 27, 43, 3]
  右半：[9, 82, 10]

左半繼續 Divide:
  [38, 27] 和 [43, 3]

  [38, 27] → [38] [27] → Merge → [27, 38]
  [43, 3]  → [43] [3]  → Merge → [3, 43]

  Merge [27, 38] 和 [3, 43]:
    比較 27 vs 3  → 取 3   → [3, ...]
    比較 27 vs 43 → 取 27  → [3, 27, ...]
    比較 38 vs 43 → 取 38  → [3, 27, 38, ...]
    剩下 43              → [3, 27, 38, 43]

右半繼續 Divide:
  [9, 82] 和 [10]

  [9, 82] → [9] [82] → Merge → [9, 82]
  [10] 已經排好了

  Merge [9, 82] 和 [10]:
    比較 9 vs 10  → 取 9   → [9, ...]
    比較 82 vs 10 → 取 10  → [9, 10, ...]
    剩下 82              → [9, 10, 82]

最後 Merge [3, 27, 38, 43] 和 [9, 10, 82]:
    比較 3 vs 9   → 取 3   → [3]
    比較 27 vs 9  → 取 9   → [3, 9]
    比較 27 vs 10 → 取 10  → [3, 9, 10]
    比較 27 vs 82 → 取 27  → [3, 9, 10, 27]
    比較 38 vs 82 → 取 38  → [3, 9, 10, 27, 38]
    比較 43 vs 82 → 取 43  → [3, 9, 10, 27, 38, 43]
    剩下 82              → [3, 9, 10, 27, 38, 43, 82]

結果：[3, 9, 10, 27, 38, 43, 82] ✓
```

#### 時間分析

$$T(n) = 2T(n/2) + \Theta(n)$$

- Divide：$\Theta(1)$（只是算中間點）
- Conquer：$2T(n/2)$（兩個子問題）
- Combine（Merge）：$\Theta(n)$（掃過所有元素一次）

用 Master Theorem：a=2, b=2, $n^{\log_2 2} = n$，$f(n) = \Theta(n)$，Case 2。

$$T(n) = \Theta(n \log n)$$

**重要：Merge Sort 的 best/worst/average case 全部都是 $\Theta(n \log n)$。** 它不會因為輸入的好壞而改變。

**空間複雜度：** $\Theta(n)$（需要暫存陣列）。

---

### 3.2 Quick Sort（快速排序）

#### 觀念

Quick Sort 跟 Merge Sort 相反：
- Merge Sort 是「拆很簡單，合很費工」
- Quick Sort 是「拆很費工（partition），合很簡單（不用做）」

1. 選一個 pivot
2. 把比 pivot 小的放左邊，比 pivot 大的放右邊（Partition）
3. 遞迴排序左右兩邊

#### 虛擬碼

```
QUICKSORT(A, p, r):
    if p < r:
        q = PARTITION(A, p, r)    // q 是 pivot 的最終位置
        QUICKSORT(A, p, q-1)      // 排序左半
        QUICKSORT(A, q+1, r)      // 排序右半

PARTITION(A, p, r):
    pivot = A[r]                  // 選最後一個元素當 pivot
    i = p - 1                     // i 指向「小於等於 pivot 區域」的最後一個
    for j = p to r-1:
        if A[j] <= pivot:
            i = i + 1
            swap A[i] and A[j]
    swap A[i+1] and A[r]          // 把 pivot 放到正確位置
    return i + 1
```

#### Step-by-step 範例

Partition 陣列 A = [2, 8, 7, 1, 3, 5, 6, 4]，pivot = 4

```
初始：[2, 8, 7, 1, 3, 5, 6, 4]    i = -1

j=0: A[0]=2 ≤ 4? Yes → i=0, swap A[0],A[0] → [2, 8, 7, 1, 3, 5, 6, 4]
j=1: A[1]=8 ≤ 4? No  → 不動
j=2: A[2]=7 ≤ 4? No  → 不動
j=3: A[3]=1 ≤ 4? Yes → i=1, swap A[1],A[3] → [2, 1, 7, 8, 3, 5, 6, 4]
j=4: A[4]=3 ≤ 4? Yes → i=2, swap A[2],A[4] → [2, 1, 3, 8, 7, 5, 6, 4]
j=5: A[5]=5 ≤ 4? No  → 不動
j=6: A[6]=6 ≤ 4? No  → 不動

最後：swap A[i+1],A[r] = swap A[3],A[7] → [2, 1, 3, 4, 7, 5, 6, 8]
                                              ≤4     pivot  >4
回傳 q = 3
```

#### 時間分析

**Worst case：$\Theta(n^2)$**

當 partition 極度不平衡（每次 pivot 是最小或最大元素）：

$$T(n) = T(n-1) + T(0) + \Theta(n) = T(n-1) + \Theta(n)$$

展開：$T(n) = \Theta(n) + \Theta(n-1) + \cdots + \Theta(1) = \Theta(n^2)$

**Best case：$\Theta(n \log n)$**

當 partition 完美平衡（每次正好對半分）：

$$T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$$

**Average case：$\Theta(n \log n)$**

假設所有排列等機率出現：

$$
T(n) = \frac{1}{n} \sum_{q=0}^{n-1} \left[T(q) + T(n-1-q)\right] + \Theta(n)
$$

利用對稱性 $T(q) + T(n-1-q)$ 出現兩次：

$$
T(n) = \frac{2}{n} \sum_{q=0}^{n-1} T(q) + \Theta(n)
$$

可以用代入法證明 $T(n) = O(n \log n)$。具體來說，猜 $T(n) \leq cn\ln n$：

$$
T(n) \leq \frac{2}{n} \sum_{q=1}^{n-1} cq\ln q + \Theta(n)
$$

利用積分近似 $\sum_{q=1}^{n-1} q\ln q \leq \int_1^n x\ln x\,dx = \frac{n^2\ln n}{2} - \frac{n^2}{4}$：

$$
T(n) \leq \frac{2c}{n}\left(\frac{n^2\ln n}{2} - \frac{n^2}{4}\right) + \Theta(n) = cn\ln n - \frac{cn}{2} + \Theta(n)
$$

只要 c 夠大（使得 $-cn/2 + \Theta(n) \leq 0$），就有 $T(n) \leq cn\ln n$。

**Randomized Quick Sort：** 隨機選 pivot，期望時間 $O(n \log n)$。

---

### 3.3 Binary Search（二分搜尋）

#### 觀念

在已排序的陣列中搜尋目標值。每次比較中間元素：
- 若等於目標，找到了
- 若大於目標，往左半找
- 若小於目標，往右半找

每次砍掉一半，所以只需 O(log n) 次比較。

#### 虛擬碼

```
BINARY-SEARCH(A, target, low, high):
    if low > high:
        return NOT_FOUND

    mid = floor((low + high) / 2)

    if A[mid] == target:
        return mid
    else if A[mid] > target:
        return BINARY-SEARCH(A, target, low, mid - 1)
    else:
        return BINARY-SEARCH(A, target, mid + 1, high)
```

#### Step-by-step 範例

A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]，搜尋 target = 23

```
Step 1: low=0, high=9, mid=4, A[4]=16
        16 < 23 → 往右找 → low=5, high=9

Step 2: low=5, high=9, mid=7, A[7]=56
        56 > 23 → 往左找 → low=5, high=6

Step 3: low=5, high=6, mid=5, A[5]=23
        23 == 23 → 找到了！回傳 index 5
```

#### 時間分析

$$T(n) = T(n/2) + \Theta(1)$$

Master Theorem：a=1, b=2, $n^{\log_2 1} = 1$，$f(n) = \Theta(1)$，Case 2。

$$T(n) = \Theta(\log n)$$

---

### 3.4 Counting Inversions（計算逆序對）

#### 問題定義

給定陣列 A[1..n]，逆序對 (inversion) 是一對 (i, j)，其中 i < j 但 A[i] > A[j]。求逆序對的總數。

**應用：** 衡量兩個排名有多不同（例如推薦系統中的相似度）。

#### 暴力法

檢查所有 $\binom{n}{2}$ 對，$O(n^2)$。

#### 分治法（Merge Sort 的巧妙變形）

**關鍵觀察：** 逆序對可以分成三類：
1. 左半內部的逆序對（兩個元素都在左半）
2. 右半內部的逆序對（兩個元素都在右半）
3. 跨越的逆序對（一個在左半，一個在右半）

第 1、2 類遞迴解決。第 3 類在 Merge 時順便數！

**為什麼 Merge 時可以數跨越逆序對？**

當我們 Merge 左半 L 和右半 R 時，如果從 R 取了一個元素 R[j]（因為 R[j] < L[i]），那麼 L 中從 i 到末尾的所有元素都跟 R[j] 構成逆序對。因為 L 已經排好序了，L[i] ≤ L[i+1] ≤ ... ，全部都 > R[j]。

#### 虛擬碼

```
COUNT-INVERSIONS(A, p, r):
    if p >= r:
        return 0

    q = floor((p + r) / 2)
    left_inv = COUNT-INVERSIONS(A, p, q)
    right_inv = COUNT-INVERSIONS(A, q+1, r)
    cross_inv = MERGE-AND-COUNT(A, p, q, r)

    return left_inv + right_inv + cross_inv

MERGE-AND-COUNT(A, p, q, r):
    L = A[p..q]
    R = A[q+1..r]
    inversions = 0
    i = 1, j = 1, k = p

    while i <= |L| and j <= |R|:
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            inversions = inversions + (|L| - i + 1)   // 關鍵！
            j = j + 1
        k = k + 1

    // 把剩下的複製過去
    copy remaining L or R into A
    return inversions
```

#### Step-by-step 範例

A = [2, 4, 1, 3, 5]

```
Divide: [2, 4, 1] 和 [3, 5]

左半 [2, 4, 1]:
  Divide: [2, 4] 和 [1]

  [2, 4] → [2] [4] → Merge → [2, 4], 跨越逆序對 = 0
  [1] 不需處理

  Merge [2, 4] 和 [1]:
    比較 2 vs 1 → 取 1, 逆序對 += (2-1+1) = 2（因為 2>1, 4>1）
    剩下 2, 4 複製
    結果 [1, 2, 4], 跨越逆序對 = 2

  左半內部逆序對 = 0
  右半內部逆序對 = 0
  跨越逆序對 = 2
  左半合計 = 2

右半 [3, 5]:
  Divide: [3] 和 [5]
  Merge → [3, 5], 跨越逆序對 = 0
  右半合計 = 0

最後 Merge [1, 2, 4] 和 [3, 5]:
  比較 1 vs 3 → 取 1, 逆序對 += 0
  比較 2 vs 3 → 取 2, 逆序對 += 0
  比較 4 vs 3 → 取 3, 逆序對 += (3-3+1) = 1（因為 4>3）
  比較 4 vs 5 → 取 4, 逆序對 += 0
  剩下 5 複製
  跨越逆序對 = 1

總逆序對 = 2 + 0 + 1 = 3

驗證：(2,1), (4,1), (4,3) → 確實是 3 個 ✓
```

**時間複雜度：** 跟 Merge Sort 一樣，$\Theta(n \log n)$。

---

### 3.5 Closest Pair of Points（最近點對）

#### 問題定義

給定平面上 n 個點，找出距離最近的一對點。

#### 暴力法

檢查所有 $\binom{n}{2}$ 對，$O(n^2)$。

#### 分治法：$O(n \log n)$

**Step 1：預處理**

把所有點按 x 座標排序（$O(n \log n)$），得到 $P_x$。同時按 y 座標排序，得到 $P_y$。

**Step 2：Divide**

用 x 座標的中位數畫一條垂直線 L，把點分成左半 Q 和右半 R。

**Step 3：Conquer**

遞迴求左半的最近點對距離 $\delta_L$ 和右半的最近點對距離 $\delta_R$。

令 $\delta = \min(\delta_L, \delta_R)$。

**Step 4：Combine（這是最精彩的部分！）**

有沒有可能最近點對橫跨左右兩半？

建立一個「strip」（帶狀區域）：所有 x 座標跟分割線距離 < $\delta$ 的點。

```
       |← δ →|← δ →|
       |     L     |
  Q    | strip |    R
       |      |
```

**關鍵定理：strip 中，每個點最多只需要跟它上方（y 座標較大的）7 個點比較！**

**為什麼是 7 個？完整推導：**

考慮 strip 中一個 $\delta \times 2\delta$ 的矩形（寬 $2\delta$，高 $\delta$）。這個矩形可以分成 8 個 $\delta/2 \times \delta/2$ 的小方格。

每個小方格的對角線長度 = $\frac{\delta}{\sqrt{2}} < \delta$。

如果一個小方格裡有兩個以上的點，那這兩個點的距離 < $\delta$，與 $\delta$ 的定義矛盾（$\delta$ 是左半或右半各自的最近距離）。

所以每個小方格最多 1 個點，8 個小方格最多 8 個點（包含自己），所以每個點最多跟 7 個點比較。

因此 strip 部分的工作量是 $O(7n) = O(n)$。

#### 虛擬碼

```
CLOSEST-PAIR(P):
    Px = P sorted by x-coordinate
    Py = P sorted by y-coordinate
    return CLOSEST-PAIR-REC(Px, Py)

CLOSEST-PAIR-REC(Px, Py):
    if |Px| <= 3:
        return brute-force 解

    // Divide
    mid = Px[|Px|/2]
    Qx, Rx = 左半和右半（依 x 排序）
    Qy, Ry = 左半和右半（依 y 排序）

    // Conquer
    (q1, q2, δL) = CLOSEST-PAIR-REC(Qx, Qy)
    (r1, r2, δR) = CLOSEST-PAIR-REC(Rx, Ry)
    δ = min(δL, δR)

    // Combine: 處理 strip
    S = Py 中所有 |x - mid.x| < δ 的點（已按 y 排序）

    for i = 0 to |S|-1:
        for j = i+1 to min(i+7, |S|-1):   // 最多看 7 個！
            if dist(S[i], S[j]) < δ:
                δ = dist(S[i], S[j])
                best_pair = (S[i], S[j])

    return best_pair with δ
```

#### 時間分析

$$T(n) = 2T(n/2) + O(n)$$

（每層的 Divide 和 Combine 都是 $O(n)$）

Master Theorem：Case 2 → $T(n) = O(n \log n)$。

加上預處理排序 $O(n \log n)$，總時間 $O(n \log n)$。

---

### 3.6 Median of Two Sorted Arrays

#### 問題定義

給定兩個已排序的陣列 A[1..m] 和 B[1..n]，找出合併後的中位數（第 (m+n)/2 小的元素）。要求 $O(\log(\min(m,n)))$。

#### 觀念

我們要在 A 中找一個切割點 i，在 B 中找一個切割點 j，使得：
- 左半總共有 (m+n+1)/2 個元素：i + j = (m+n+1)/2
- 左半最大值 ≤ 右半最小值：A[i-1] ≤ B[j] 且 B[j-1] ≤ A[i]

因為 j 由 i 決定（j = (m+n+1)/2 - i），所以只需要在 A 上做二分搜尋。

#### 虛擬碼

```
MEDIAN-OF-TWO-SORTED(A, B):
    // 確保 A 是較短的陣列
    if |A| > |B|:
        swap A and B

    m = |A|, n = |B|
    low = 0, high = m

    while low <= high:
        i = (low + high) / 2          // A 中的切割點
        j = (m + n + 1) / 2 - i       // B 中的切割點

        if i > 0 and A[i-1] > B[j]:   // A 的左半太大
            high = i - 1               // 左移切割點
        else if i < m and B[j-1] > A[i]:  // B 的左半太大
            low = i + 1                // 右移切割點
        else:
            // 找到正確的切割點
            if i == 0: max_left = B[j-1]
            else if j == 0: max_left = A[i-1]
            else: max_left = max(A[i-1], B[j-1])

            if (m + n) is odd:
                return max_left

            if i == m: min_right = B[j]
            else if j == n: min_right = A[i]
            else: min_right = min(A[i], B[j])

            return (max_left + min_right) / 2
```

#### Step-by-step 範例

A = [1, 3, 8, 9, 15], B = [7, 11, 18, 19, 21, 25]

m = 5, n = 6, 合併後 11 個元素，中位數是第 6 個。

half = (5+6+1)/2 = 6

```
Step 1: low=0, high=5
  i = 2, j = 6-2 = 4
  A 的左半：[1, 3]          A 的右半：[8, 9, 15]
  B 的左半：[7, 11, 18, 19]  B 的右半：[21, 25]

  檢查：A[i-1]=3 ≤ B[j]=21 ✓
  檢查：B[j-1]=19 ≤ A[i]=8 ✗ → 19 > 8，B 左半太大 → low = 3

Step 2: low=3, high=5
  i = 4, j = 6-4 = 2
  A 的左半：[1, 3, 8, 9]    A 的右半：[15]
  B 的左半：[7, 11]          B 的右半：[18, 19, 21, 25]

  檢查：A[i-1]=9 ≤ B[j]=18 ✓
  檢查：B[j-1]=11 ≤ A[i]=15 ✓ → 找到了！

  max_left = max(9, 11) = 11
  11 個元素（奇數），回傳 11

驗證：合併後 [1, 3, 7, 8, 9, 11, 15, 18, 19, 21, 25]
                                   ↑
                              第 6 個 = 11 ✓
```

**時間複雜度：** $O(\log(\min(m,n)))$，只在較短的陣列上做二分搜尋。

---

### 3.7 Karatsuba 乘法

#### 問題定義

計算兩個 n 位數 X 和 Y 的乘積。小學方法是 $O(n^2)$。

#### 觀念

把 X 和 Y 各分成高位和低位兩半：

$X = X_H \cdot 10^{n/2} + X_L$
$Y = Y_H \cdot 10^{n/2} + Y_L$

$$
X \cdot Y = X_H Y_H \cdot 10^n + (X_H Y_L + X_L Y_H) \cdot 10^{n/2} + X_L Y_L
$$

直接算需要 4 次 n/2 位乘法：$T(n) = 4T(n/2) + O(n) = O(n^2)$，沒省到。

**Karatsuba 的天才想法：**

令：
- $P_1 = X_H \cdot Y_H$
- $P_2 = X_L \cdot Y_L$
- $P_3 = (X_H + X_L)(Y_H + Y_L)$

則 $X_H Y_L + X_L Y_H = P_3 - P_1 - P_2$

只需要 **3 次** n/2 位乘法！

$$T(n) = 3T(n/2) + O(n)$$

Master Theorem：$n^{\log_2 3} \approx n^{1.585}$，Case 1。

$$T(n) = O(n^{\log_2 3}) \approx O(n^{1.585})$$

---

## 4. Selection 演算法（Median of Medians）

### 4.1 問題定義

在未排序的陣列中找第 k 小的元素。

### 4.2 Quickselect（Randomized）

跟 Quick Sort 一樣做 Partition，但只遞迴進入包含第 k 小元素的那一半。

期望時間：$O(n)$（但最壞 $O(n^2)$）。

### 4.3 Median of Medians：確定性 O(n)

**關鍵想法：** 用一個聰明的方法選 pivot，保證 partition 不會太不平衡。

#### 虛擬碼

```
SELECT(A, k):
    if |A| <= 5:
        sort A and return the k-th element

    // Step 1: 把 A 分成每組 5 個
    groups = divide A into groups of 5

    // Step 2: 找每組的中位數
    medians = [median of each group]      // O(n) 時間（每組 O(1)）

    // Step 3: 遞迴找中位數的中位數
    pivot = SELECT(medians, |medians|/2)  // T(n/5)

    // Step 4: 用這個 pivot 做 partition
    L, E, G = partition A into (<pivot, =pivot, >pivot)

    // Step 5: 遞迴進入正確的一邊
    if k <= |L|:
        return SELECT(L, k)              // T(7n/10)
    else if k <= |L| + |E|:
        return pivot
    else:
        return SELECT(G, k - |L| - |E|)  // T(7n/10)
```

#### 為什麼分 5 組？

**核心問題：** 我們需要保證用 median of medians 當 pivot 時，partition 兩邊都不會太大。

**分析：** 假設分成每組 g 個元素。

中位數的中位數 p 至少大於：
- 每組中位數中，有一半的中位數 ≤ p
- 這些組中，每組又有 ⌈g/2⌉ 個元素 ≤ 各自的中位數

所以 p 至少大於 $\frac{1}{2} \cdot \lceil n/g \rceil \cdot \lceil g/2 \rceil \approx \frac{n}{4}$ 個元素。

同理，p 也至少小於大約 n/4 個元素。

所以最壞情況下，遞迴進入的那邊最多有約 $\frac{3n}{4}$ 個元素。但我們更精確地算：

對 g = 5：
- 至少有 $3 \cdot \lceil \frac{1}{2} \lceil n/5 \rceil \rceil \geq \frac{3n}{10} - 6$ 個元素 ≤ p
- 所以另一邊最多 $n - \frac{3n}{10} + 6 = \frac{7n}{10} + 6$ 個元素

遞迴式：
$$T(n) = T(n/5) + T(7n/10) + O(n)$$

$n/5 + 7n/10 = 9n/10 < n$，所以每層的「問題總量」以 9/10 的比率遞減。

用代入法可證 $T(n) = O(n)$：

猜 $T(n) \leq cn$：
$$T(n) \leq c \cdot n/5 + c \cdot 7n/10 + an = cn(1/5 + 7/10) + an = \frac{9cn}{10} + an$$

要 $\frac{9cn}{10} + an \leq cn$，即 $an \leq \frac{cn}{10}$，$c \geq 10a$。✓

**如果分 3 組呢？**

$T(n) = T(n/3) + T(2n/3) + O(n)$

$n/3 + 2n/3 = n$，不收斂！每層問題總量不減少，最後是 $O(n \log n)$，不是線性。

**如果分 7 組呢？**

也可以！$T(n) = T(n/7) + T(5n/7) + O(n)$，$1/7 + 5/7 = 6/7 < 1$，也是 $O(n)$。

但 5 是讓分析成立的**最小奇數**。分 5 組在實作上也比較方便（組內排序快）。

---

## 5. 完整 Trace Through 範例

### 範例 1：Merge Sort 完整追蹤

A = [5, 2, 4, 7, 1, 3, 2, 6]

```
MS([5,2,4,7,1,3,2,6])
├── MS([5,2,4,7])
│   ├── MS([5,2])
│   │   ├── MS([5]) → [5]
│   │   └── MS([2]) → [2]
│   │   └── Merge([5],[2]) → [2,5]
│   └── MS([4,7])
│       ├── MS([4]) → [4]
│       └── MS([7]) → [7]
│       └── Merge([4],[7]) → [4,7]
│   └── Merge([2,5],[4,7]):
│       2<4 → [2], 5>4 → [2,4], 5<7 → [2,4,5], 7 → [2,4,5,7]
└── MS([1,3,2,6])
    ├── MS([1,3])
    │   ├── MS([1]) → [1]
    │   └── MS([3]) → [3]
    │   └── Merge([1],[3]) → [1,3]
    └── MS([2,6])
        ├── MS([2]) → [2]
        └── MS([6]) → [6]
        └── Merge([2],[6]) → [2,6]
    └── Merge([1,3],[2,6]):
        1<2 → [1], 3>2 → [1,2], 3<6 → [1,2,3], 6 → [1,2,3,6]
└── Merge([2,4,5,7],[1,2,3,6]):
    2>1 → [1]
    2=2 → [1,2]（取左邊的2）
    4>2 → [1,2,2]
    4>3 → [1,2,2,3]
    4<6 → [1,2,2,3,4]
    5<6 → [1,2,2,3,4,5]
    7>6 → [1,2,2,3,4,5,6]
    7   → [1,2,2,3,4,5,6,7]

最終結果：[1, 2, 2, 3, 4, 5, 6, 7] ✓
```

---

### 範例 2：Quick Sort 完整追蹤

A = [3, 7, 8, 5, 2, 1, 9, 5, 4]

```
QS([3,7,8,5,2,1,9,5,4])
  Partition with pivot=4:
    掃描：3≤4→放左, 7>4, 8>4, 5>4, 2≤4→放左, 1≤4→放左, 9>4, 5>4
    結果：[3,2,1, | 4 | ,7,8,5,9,5]
    pivot 在 index 3

  QS([3,2,1])
    Partition with pivot=1:
      掃描：3>1, 2>1
      結果：[| 1 | ,2,3]
      pivot 在 index 0

    QS([]) → 空
    QS([2,3])
      Partition with pivot=3:
        掃描：2≤3→放左
        結果：[2, | 3 |]
      QS([2]) → 已排好
      QS([]) → 空

    結果：[1, 2, 3]

  QS([7,8,5,9,5])
    Partition with pivot=5:
      掃描：7>5, 8>5, 5≤5→放左, 9>5
      結果：[5, | 5 | ,8,7,9]
      pivot 在 index 1（相對）

    QS([5]) → 已排好
    QS([8,7,9])
      Partition with pivot=9:
        掃描：8≤9→放左, 7≤9→放左
        結果：[8,7, | 9 |]
      QS([8,7])
        Partition with pivot=7:
          掃描：8>7
          結果：[| 7 | ,8]
        → [7, 8]
      QS([]) → 空
      結果：[7, 8, 9]

    結果：[5, 5, 7, 8, 9]

最終結果：[1, 2, 3, 4, 5, 5, 7, 8, 9] ✓
```

---

### 範例 3：Counting Inversions 完整追蹤

A = [5, 3, 1, 4, 2]

所有逆序對：(5,3), (5,1), (5,4), (5,2), (3,1), (3,2), (4,2) = 7 個

```
CI([5,3,1,4,2])
├── CI([5,3,1])
│   ├── CI([5,3])
│   │   ├── CI([5]) → 0
│   │   └── CI([3]) → 0
│   │   └── Merge-Count([5],[3]):
│   │       5>3 → 取 3, inv += 1 (因為 5>3)
│   │       取 5
│   │       → [3,5], 跨越逆序=1
│   │   左半逆序 = 0+0+1 = 1
│   │
│   └── CI([1]) → 0
│   └── Merge-Count([3,5],[1]):
│       3>1 → 取 1, inv += 2 (因為 3,5 都 >1)
│       取 3, 取 5
│       → [1,3,5], 跨越逆序=2
│   左半合計 = 1+0+2 = 3
│
└── CI([4,2])
    ├── CI([4]) → 0
    └── CI([2]) → 0
    └── Merge-Count([4],[2]):
        4>2 → 取 2, inv += 1
        取 4
        → [2,4], 跨越逆序=1
    右半合計 = 0+0+1 = 1

Merge-Count([1,3,5],[2,4]):
  1<2 → 取 1, inv += 0
  3>2 → 取 2, inv += 2 (因為 3,5 都 >2)
  3<4 → 取 3, inv += 0
  5>4 → 取 4, inv += 1 (因為 5>4)
  取 5
  → [1,2,3,4,5], 跨越逆序=3

總計 = 3 + 1 + 3 = 7 ✓
```

---

## 6. 常見陷阱

### 陷阱 1：忘記 Quick Sort 的 Worst Case

Quick Sort 在最壞情況下是 $O(n^2)$，不是 $O(n \log n)$！

- 已排序的陣列 + 選最後一個當 pivot = 最壞情況
- 解法：Randomized pivot 或 Median of Medians

### 陷阱 2：Closest Pair 的 Strip 部分

很多人以為 strip 部分是 $O(n^2)$ 的（因為要比較所有配對），但其實只需要每個點看最多 7 個鄰居，所以是 $O(n)$。

### 陷阱 3：Merge Sort 需要額外空間

Merge Sort 是 $O(n)$ 額外空間的。如果題目要求 in-place 排序，不能直接用。（雖然有 in-place merge sort，但常數很大。）

### 陷阱 4：Binary Search 的整數溢位

`mid = (low + high) / 2` 在 low + high 很大時可能溢位。正確寫法：`mid = low + (high - low) / 2`。

### 陷阱 5：分治的 Base Case 處理不當

遞迴一定要有正確的 base case，否則會無限遞迴。Base case 通常是 n = 1 或 n ≤ 某個常數。

### 陷阱 6：Karatsuba 的加法位數問題

$X_H + X_L$ 和 $Y_H + Y_L$ 可能是 n/2 + 1 位（進位），要小心處理。

---

## 7. 何時使用 / 不使用分治法

### 使用分治法的信號

1. 問題可以自然地拆成**同類型**的子問題
2. 子問題之間**獨立**（不共享子子問題）
3. 存在**高效的合併步驟**
4. 你想把 $O(n^2)$ 降到 $O(n \log n)$ 或更好

### 不使用分治法的信號

1. 子問題**高度重疊** → 用 DP
2. **每步都能做出局部最優選擇** → 用 Greedy
3. 問題在**圖上**，沒有自然的分割方式
4. 分割後**合併成本太高**，抵消了分割的好處
