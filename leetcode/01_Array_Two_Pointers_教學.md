# Array & Two Pointers 完全教學手冊

> **適用對象**：基礎較弱、準備 Google / NVIDIA 面試的工程師
> **教學風格**：大學教科書等級，每個觀念都有 2+ 組完整數值追蹤
> **語言**：繁體中文解說 + English technical terms
> **配套程式**：`01_Array_Two_Pointers.py`（可直接執行驗證所有範例）

---

## 第一章：Array 基礎觀念

### 1.1 什麼是 Array？

Array（陣列）是一塊**連續的記憶體空間**，裡面儲存相同型別的元素。

```
記憶體位址（假設起始位址 = 1000，每個 int 佔 4 bytes）：

  index:    0      1      2      3      4
         ┌──────┬──────┬──────┬──────┬──────┐
  value: │  10  │  20  │  30  │  40  │  50  │
         └──────┴──────┴──────┴──────┴──────┘
  addr:  1000   1004   1008   1012   1016
```

**為什麼 index access 是 O(1)？**

因為記憶體是連續的，所以只要知道：
- 起始位址 `base_addr`
- 每個元素大小 `element_size`
- 想存取的 index `i`

就能直接算出位址：

```
addr(i) = base_addr + i × element_size
```

**範例計算**：
- `arr[0]` 的位址 = 1000 + 0 × 4 = 1000
- `arr[3]` 的位址 = 1000 + 3 × 4 = 1012
- `arr[4]` 的位址 = 1000 + 4 × 4 = 1016

不需要從頭走到尾，一步到位，所以是 O(1)。

### 1.2 Array vs Linked List vs HashMap

```
┌──────────────┬──────────┬─────────────┬──────────┐
│   操作        │  Array   │ Linked List │ HashMap  │
├──────────────┼──────────┼─────────────┼──────────┤
│ 以 index 讀取 │  O(1)    │    O(n)     │   N/A    │
│ 以 key 讀取   │  N/A     │    N/A      │ O(1) avg │
│ 搜尋特定值    │  O(n)    │    O(n)     │ O(1) avg │
│ 頭部插入      │  O(n)    │    O(1)     │   N/A    │
│ 尾部插入      │  O(1)*   │    O(1)**   │ O(1) avg │
│ 中間插入      │  O(n)    │    O(1)***  │   N/A    │
│ 刪除          │  O(n)    │    O(1)***  │ O(1) avg │
│ 記憶體        │ 連續     │  分散       │  分散     │
│ Cache 友善度  │ 非常好   │    差       │   中等    │
└──────────────┴──────────┴─────────────┴──────────┘
*  amortized    ** 若有 tail pointer    *** 若已知位置
```

**面試重點**：Array 的 cache locality 非常好。因為元素連續存放，CPU cache line 一次載入就能涵蓋多個元素。Linked List 的 node 散落在記憶體各處，每次存取都可能 cache miss。

### 1.3 常見操作與時間複雜度

#### Traverse（遍歷）— O(n)

```python
for i in range(len(arr)):     # by index
    print(arr[i])

for val in arr:               # by value (Pythonic)
    print(val)
```

#### Insert（插入）— O(n) worst case

在 index `k` 處插入，後面所有元素要往後移一格：

```
插入前: [10, 20, 30, 40, 50]    在 index=2 插入 25

Step 1: 把 index 4→5:  [10, 20, 30, 40, _, 50]  ← 50 往後移
Step 2: 把 index 3→4:  [10, 20, 30, _, 40, 50]  ← 40 往後移
Step 3: 把 index 2→3:  [10, 20, _, 30, 40, 50]  ← 30 往後移
Step 4: 寫入 index 2:  [10, 20, 25, 30, 40, 50] ✓

移動了 3 個元素（n-k 個），最差 O(n)
```

#### Delete（刪除）— O(n) worst case

刪除 index `k`，後面所有元素要往前移一格：

```
刪除前: [10, 20, 30, 40, 50]    刪除 index=1 的元素 (20)

Step 1: 把 index 2→1:  [10, 30, 30, 40, 50]
Step 2: 把 index 3→2:  [10, 30, 40, 40, 50]
Step 3: 把 index 4→3:  [10, 30, 40, 50, 50]
Step 4: 長度 -1:       [10, 30, 40, 50]  ✓

移動了 3 個元素（n-k-1 個），最差 O(n)
```

### 1.4 In-place Modification（原地修改）

**為什麼面試官愛考 in-place？**

因為它測試你能否：
1. 不使用額外空間（O(1) space）
2. 巧妙地用指針管理「已處理」和「未處理」的區域
3. 理解覆寫順序（先寫還是先移？）

```
In-place 的核心思想：
用指針把 array 分成兩個區域

  [已處理的結果 | 還沒處理的原始資料]
        ↑                ↑
      slow             fast

slow 左邊 = 最終答案
fast 負責掃描每個元素，決定要不要放進「已處理區域」
```

這就是第四章「同向雙指針」的精髓。

---

## 第二章：雙指針的核心思想

### 2.1 為什麼需要 Two Pointers？

考慮一個簡單問題：在 sorted array 中找兩個數的和 = target。

**暴力解法 O(n^2)**：兩層 for loop，每對都試一次。
```python
for i in range(n):
    for j in range(i+1, n):
        if nums[i] + nums[j] == target:
            return [i, j]
```

**數值範例**：nums = [1, 3, 5, 7, 9], target = 8
```
i=0: (1,3)=4 (1,5)=6 (1,7)=8 ✓ 找到！但試了 3 次
如果答案在最後面，要試 n(n-1)/2 次 = O(n²)
```

**Two Pointers O(n)**：利用 sorted 的性質，一次排除一整行/列。
```
left=0, right=4: 1+9=10 > 8 → right-- (9 太大，跟所有人配都太大)
left=0, right=3: 1+7=8 == 8 ✓ 只試了 2 次！
```

**關鍵洞察**：因為 array 是 sorted 的，每一步我們都能**排除一整個指針的所有配對**，而不只是排除一對。這就是從 O(n^2) 降到 O(n) 的秘密。

### 2.2 三種 Two Pointers 類型

```
類型 1: 對向雙指針 (Opposite Direction)
  ┌───┬───┬───┬───┬───┬───┬───┐
  │   │   │   │   │   │   │   │
  └───┴───┴───┴───┴───┴───┴───┘
   L→                       ←R
  兩端出發，向中間靠攏
  適用：sorted array 找配對、palindrome、container water

類型 2: 同向雙指針 (Same Direction)
  ┌───┬───┬───┬───┬───┬───┬───┐
  │   │   │   │   │   │   │   │
  └───┴───┴───┴───┴───┴───┴───┘
   S→ F→
  同端出發，同方向前進，速度不同
  適用：in-place 去重、移除、分區

類型 3: 快慢指針 (Fast-Slow / Floyd's)
  ┌───┬───┬───┬───┬───┐
  │   │   │   │   │   │ ←─┐
  └───┴───┴───┴───┴───┘   │
   S→ F→→                  │
         └─────────────────┘  (cycle)
  同起點出發，fast 走兩步 slow 走一步
  適用：cycle detection、找重複數字
```

---

## 第三章：對向雙指針 (Opposite Direction)

### 3.1 Two Sum II — LeetCode 167

#### 問題描述

給定一個**已排序（升序）**的整數陣列 `numbers` 和一個目標值 `target`，找出兩個數字使得它們的和恰好等於 `target`。回傳這兩個數的 index（1-indexed）。

**限制**：恰好一組解、不能用同一個元素兩次。

#### 暴力解法 O(n^2) — 為什麼慢？

```python
for i in range(n):
    for j in range(i+1, n):
        if numbers[i] + numbers[j] == target:
            return [i+1, j+1]
```

對於 n=10000 的陣列，最差要做 ~50,000,000 次加法。太慢了。

#### 雙指針解法 O(n)

```
核心邏輯（Pseudocode）：

left = 0
right = len(numbers) - 1

while left < right:
    current_sum = numbers[left] + numbers[right]

    if current_sum == target:
        return [left+1, right+1]    # 找到答案
    elif current_sum > target:
        right -= 1                  # sum 太大，需要變小 → 右邊往左移
    else:
        left += 1                   # sum 太小，需要變大 → 左邊往右移
```

**為什麼這樣做是正確的？（直覺解釋）**

想像一個矩陣，row 是 left 的選擇，column 是 right 的選擇：

```
            right →  0    1    2    3
  left ↓         (val=2)(val=7)(val=11)(val=15)
  0 (val=2)       4    9✓   13   17
  1 (val=7)       -    14   18   22
  2 (val=11)      -    -    22   26
  3 (val=15)      -    -    -    30
```

target = 9。我們從右上角 (left=0, right=3) 出發：
- 17 > 9 → 這一整列（right=3）跟 left=1,2,3 配一定更大，全部排除 → right--
- 13 > 9 → 同理排除 right=2 那一整列 → right--
- 9 == 9 → 找到！

每一步排除一行或一列，最多走 n 步。

#### 範例 1：nums = [2, 7, 11, 15], target = 9

```
初始狀態:
  [2, 7, 11, 15]
   L            R        left=0 (值=2), right=3 (值=15)

Step 1: sum = nums[0] + nums[3] = 2 + 15 = 17
        17 > 9 → 太大了！right-- → right=2
  [2, 7, 11, 15]
   L        R

Step 2: sum = nums[0] + nums[2] = 2 + 11 = 13
        13 > 9 → 還是太大！right-- → right=1
  [2, 7, 11, 15]
   L   R

Step 3: sum = nums[0] + nums[1] = 2 + 7 = 9
        9 == 9 ✓ 找到了！
        return [1, 2]  (1-indexed)
```

共走了 3 步。

#### 範例 2：nums = [1, 3, 4, 5, 7, 10, 11], target = 9

```
初始狀態:
  [1, 3, 4, 5, 7, 10, 11]
   L                   R     left=0 (值=1), right=6 (值=11)

Step 1: sum = 1 + 11 = 12 > 9 → right-- → right=5
  [1, 3, 4, 5, 7, 10, 11]
   L               R

Step 2: sum = 1 + 10 = 11 > 9 → right-- → right=4
  [1, 3, 4, 5, 7, 10, 11]
   L           R

Step 3: sum = 1 + 7 = 8 < 9 → 太小了！left++ → left=1
  [1, 3, 4, 5, 7, 10, 11]
      L        R

Step 4: sum = 3 + 7 = 10 > 9 → right-- → right=3
  [1, 3, 4, 5, 7, 10, 11]
      L     R

Step 5: sum = 3 + 5 = 8 < 9 → left++ → left=2
  [1, 3, 4, 5, 7, 10, 11]
         L  R

Step 6: sum = 4 + 5 = 9 == 9 ✓ 找到了！
        return [3, 4]  (1-indexed)
```

共走了 6 步（array 長度 7，符合 O(n)）。

#### Corner Cases

| Case | 說明 | 處理方式 |
|------|------|----------|
| 只有兩個元素 | `[1, 2]`, target=3 | 第一步就找到 |
| target 很大 | `[1,2,3]`, target=5 | left 會一直推到跟 right 相鄰 |
| 有重複元素 | `[1,1,2,3]`, target=2 | 正常運作，因為 sorted |

#### 白板面試技巧

1. **先確認**：「Is the array sorted?」→ 這決定能不能用 two pointers
2. **先問**：「Are there duplicate values?」→ 影響去重邏輯
3. **先問**：「Is the answer 0-indexed or 1-indexed?」→ 167 題是 1-indexed
4. **寫 code 時**：先寫 `while left < right`，再填裡面的邏輯

---

### 3.2 Container With Most Water — LeetCode 11

#### 問題描述

給定 `n` 條垂直線段（以高度陣列 `height` 表示），選兩條線和 x 軸圍成容器，求最大裝水量。

```
面積公式: area = min(height[left], height[right]) × (right - left)
                 ─────────────────────────────────   ──────────────
                       高度（取較矮的）                   寬度
```

#### 為什麼 Greedy 有效？（數學直覺證明）

起初 left=0, right=n-1，寬度最大。之後每移動一步，寬度必然 -1。

**移動較矮的那一端**：min(height) 有機會變大 → 面積可能增加
**移動較高的那一端**：min(height) 不可能變大（因為瓶頸在矮的那邊）→ 寬度 -1 但高度不增 → 面積一定不增

所以每次移動矮的那端是最優策略，不會錯過最優解。

#### Pseudocode

```
left = 0, right = n-1, max_area = 0

while left < right:
    area = min(height[left], height[right]) × (right - left)
    max_area = max(max_area, area)

    if height[left] < height[right]:
        left++      # 移動矮的
    else:
        right--     # 移動矮的（或相等時任移一邊）
```

#### 範例 1：height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

```
初始: left=0, right=8, max_area=0

  index: 0  1  2  3  4  5  6  7  8
  value: 1  8  6  2  5  4  8  3  7

Step 1: area = min(1,7) × (8-0) = 1 × 8 = 8
        max_area = 8
        height[0]=1 < height[8]=7 → left++

        圖示:
        |        |              |
        |  |     |        |    |
        |  |  |  |        |    |
        |  |  |  |  |     |    |
        |  |  |  |  |  |  |    |
        |  |  |  |  |  |  |  | |
        |  |  |  |  |  |  |  | |
        L= |  |  |  |  |  |  | =R  area=8
        0  1  2  3  4  5  6  7  8

Step 2: area = min(8,7) × (8-1) = 7 × 7 = 49
        max_area = 49
        height[1]=8 > height[8]=7 → right--

Step 3: area = min(8,3) × (7-1) = 3 × 6 = 18
        max_area = 49 (不更新)
        height[7]=3 < height[1]=8 → right--

Step 4: area = min(8,8) × (6-1) = 8 × 5 = 40
        max_area = 49 (不更新)
        height[1]=8 == height[6]=8 → left++ (相等任移一邊)

Step 5: area = min(6,8) × (6-2) = 6 × 4 = 24
        max_area = 49 (不更新)
        height[2]=6 < height[6]=8 → left++

Step 6: area = min(2,8) × (6-3) = 2 × 3 = 6
        max_area = 49
        height[3]=2 < height[6]=8 → left++

Step 7: area = min(5,8) × (6-4) = 5 × 2 = 10
        max_area = 49
        height[4]=5 < height[6]=8 → left++

Step 8: area = min(4,8) × (6-5) = 4 × 1 = 4
        max_area = 49
        height[5]=4 < height[6]=8 → left++

left=6 == right=6 → 結束

答案 = 49（出現在 Step 2：index 1 和 8，高度 8 和 7，寬度 7）
```

#### 範例 2：height = [4, 3, 2, 1, 4]

```
初始: left=0, right=4, max_area=0

Step 1: area = min(4,4) × (4-0) = 4 × 4 = 16
        max_area = 16
        height[0]=4 == height[4]=4 → left++

Step 2: area = min(3,4) × (4-1) = 3 × 3 = 9
        max_area = 16
        height[1]=3 < height[4]=4 → left++

Step 3: area = min(2,4) × (4-2) = 2 × 2 = 4
        max_area = 16
        height[2]=2 < height[4]=4 → left++

Step 4: area = min(1,4) × (4-3) = 1 × 1 = 1
        max_area = 16
        height[3]=1 < height[4]=4 → left++

left=4 == right=4 → 結束
答案 = 16
```

#### Corner Cases

| Case | 範例 | 注意 |
|------|------|------|
| 只有兩條線 | `[1,1]` | 一步就結束 |
| 高度相等 | `[5,5,5,5]` | 任移一邊都可以 |
| 遞增陣列 | `[1,2,3,4,5]` | 最大面積在兩端不一定最大 |

---

### 3.3 Valid Palindrome — LeetCode 125

#### 問題描述

判斷字串是否為 palindrome（回文），只考慮字母和數字（alphanumeric），忽略大小寫。

#### 核心思路

回文 = 頭尾對稱。從兩端向中間比，遇到非 alphanumeric 就跳過。

```
Pseudocode:
left = 0, right = len(s) - 1

while left < right:
    while left < right and not isAlphanumeric(s[left]):
        left++          # 跳過非字母數字
    while left < right and not isAlphanumeric(s[right]):
        right--         # 跳過非字母數字

    if toLower(s[left]) != toLower(s[right]):
        return False    # 不對稱
    left++
    right--

return True             # 全部匹配
```

#### 範例 1：s = "A man, a plan, a canal: Panama"

```
清理後等效字串: "amanaplanacanalpanama" (長度 21)

但我們不需要真的清理，直接在原字串上跳過非 alphanumeric：

原字串:  A   m a n ,   a   p l a n ,   a   c a n a l :   P a n a m a
index:   0  1 2 3 4 5  6  7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29

Step 1:  left=0('A'→'a'), right=29('a') → 'a'=='a' ✓
Step 2:  left=1('m'), right=28('m') → match ✓
Step 3:  left=2('a'), right=27('a') → match ✓
Step 4:  left=3('n'), right=26('n') → match ✓
Step 5:  left=4(',') → 跳過 → left=5(' ') → 跳過 → left=6('a')
         right=25('a')
         'a'=='a' ✓
  ...（每對都匹配）
Step 最終: left >= right → 結束

return True ✓ 這是回文！
```

#### 範例 2：s = "race a car"

```
清理後等效字串: "raceacar" (長度 8)

Step 1: left=0('r'), right=9('r') → match ✓
Step 2: left=1('a'), right=8('a') → match ✓
Step 3: left=2('c'), right=7('c') → match ✓
Step 4: left=3('e'), right=5(' ') → 跳過 → right=4('a')
        'e' != 'a' → return False ✗

不是回文！在第 4 步就發現了。
```

#### Corner Cases

| Case | 輸入 | 結果 | 說明 |
|------|------|------|------|
| 空字串 | `""` | True | 空字串視為回文 |
| 單一字元 | `"a"` | True | left >= right 直接通過 |
| 全部相同 | `"aaaa"` | True | 每步都匹配 |
| 只有符號 | `".,!"` | True | 跳過所有字元後 left>=right |
| 數字混合 | `"0P"` | False | '0' != 'p' |

---

### 3.4 3Sum — LeetCode 15（Google 高頻題）

#### 問題描述

找出陣列中所有三元組 `[a, b, c]` 使得 `a + b + c = 0`，結果不可重複。

#### 核心策略：排序 + 固定一個 + Two Sum II

```
Step 1: 排序陣列                          O(n log n)
Step 2: 外層 loop 固定第一個數 nums[i]     O(n)
Step 3: 內層用對向雙指針找另外兩個         O(n)
        target = -nums[i]
        在 nums[i+1 ... n-1] 中找兩數和 = target

總時間: O(n log n) + O(n) × O(n) = O(n²)
```

#### 去重是最難的部分！

```
去重規則 1（外層）：
  如果 nums[i] == nums[i-1]，跳過
  原因：固定相同的數會產生重複的三元組

去重規則 2（內層，找到解之後）：
  while nums[left] == nums[left+1]: left++
  while nums[right] == nums[right-1]: right--
  然後 left++, right--
  原因：跳過相同的值，避免產生相同的配對
```

#### 範例 1：nums = [-1, 0, 1, 2, -1, -4]

```
Step 0: 排序 → [-4, -1, -1, 0, 1, 2]

═══ i=0, nums[i]=-4, target=4, left=1, right=5 ═══

  [-4, -1, -1,  0,  1,  2]
   fix  L                R

  Step 1: -1 + 2 = 1 < 4 → left++
  Step 2: -1 + 2 = 1 < 4 → left++
  Step 3:  0 + 2 = 2 < 4 → left++
  Step 4:  1 + 2 = 3 < 4 → left++
  left=5 >= right=5 → 結束（-4 太小了，配不出 4）

═══ i=1, nums[i]=-1, target=1, left=2, right=5 ═══

  [-4, -1, -1,  0,  1,  2]
        fix  L              R

  Step 1: -1 + 2 = 1 == 1 ✓ → 找到 [-1, -1, 2]
    → 跳過重複：left 的下一個是 0（不同），right 的前一個是 1（不同）
    → left=3, right=4

  Step 2:  0 + 1 = 1 == 1 ✓ → 找到 [-1, 0, 1]
    → left=4, right=3 → left >= right → 結束

═══ i=2, nums[i]=-1 ═══
  nums[2]=-1 == nums[1]=-1 → 跳過！（去重規則 1）

═══ i=3, nums[i]=0, target=0, left=4, right=5 ═══

  Step 1: 1 + 2 = 3 > 0 → right--
  right=4, left=4 >= right=4 → 結束

最終結果: [[-1, -1, 2], [-1, 0, 1]]
```

#### 範例 2：nums = [0, 0, 0, 0]

```
Step 0: 排序 → [0, 0, 0, 0]

═══ i=0, nums[i]=0, target=0, left=1, right=3 ═══

  [ 0,  0,  0,  0]
   fix  L       R

  Step 1: 0 + 0 = 0 == 0 ✓ → 找到 [0, 0, 0]
    → 跳過重複：left 的下一個也是 0 → left=2，再下一個也是 0 → left=3
                 right 的前一個也是 0 → right=2，再前一個也是 0 → right=1
    → left=3, right=1 → left >= right → 結束

═══ i=1, nums[i]=0 ═══
  nums[1]=0 == nums[0]=0 → 跳過！

═══ i=2, 同理跳過 ═══

最終結果: [[0, 0, 0]]

注意：雖然有 4 個 0，但因為去重，只有一個 [0,0,0]。
```

#### Corner Cases & 面試小技巧

| Case | 處理 |
|------|------|
| 陣列長度 < 3 | 直接 return [] |
| 全是正數 | 排序後 nums[0]>0 → 三數和不可能=0 → 剪枝 |
| 全是零 | 只有一個解 [0,0,0] |
| 很多重複 | 去重邏輯是重點 |

**面試時先跟面試官說**：
1. "I'll sort the array first, which takes O(n log n)."
2. "Then I'll fix one number and use two pointers for the other two."
3. "The tricky part is deduplication — I'll skip duplicate values at both the outer loop and inner loop."

---

## 第四章：同向雙指針 (Same Direction)

### 4.1 Remove Duplicates from Sorted Array — LeetCode 26

#### 問題描述

給定一個**已排序**的陣列，原地（in-place）移除重複元素，使每個元素只出現一次。回傳新長度 `k`，陣列的前 `k` 個元素即為結果。

#### 核心思路

```
slow = "寫入位置" (write pointer)
fast = "讀取位置" (read pointer)

規則：
  fast 掃描每個元素
  如果 nums[fast] != nums[slow-1]（跟上一個寫入的不同）
    → 把 nums[fast] 寫入 nums[slow]
    → slow++

  [已經確定不重複的部分 | 待處理]
                       ↑       ↑
                      slow    fast
```

#### Pseudocode

```python
slow = 1                          # index 0 的元素一定保留
for fast in range(1, len(nums)):
    if nums[fast] != nums[slow - 1]:
        nums[slow] = nums[fast]
        slow += 1
return slow
```

#### 範例 1：nums = [1, 1, 2]

```
初始: slow=1
  [1, 1, 2]
      S  F=1

fast=1: nums[1]=1 == nums[0]=1 → 重複，跳過
  [1, 1, 2]
      S     F=2

fast=2: nums[2]=2 != nums[0]=1 → 不同！寫入
  nums[1] = 2, slow = 2
  [1, 2, 2]
         S

結果: 長度=2, 前 2 個元素 = [1, 2] ✓
```

#### 範例 2：nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]

```
初始: slow=1
  [ 0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
       S
       F=1

fast=1: nums[1]=0 == nums[0]=0 → 跳過

fast=2: nums[2]=1 != nums[0]=0 → 寫入 nums[1]=1, slow=2
  陣列: [0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
              S

fast=3: nums[3]=1 == nums[1]=1 → 跳過

fast=4: nums[4]=1 == nums[1]=1 → 跳過

fast=5: nums[5]=2 != nums[1]=1 → 寫入 nums[2]=2, slow=3
  陣列: [0, 1, 2, 1, 1, 2, 2, 3, 3, 4]
                 S

fast=6: nums[6]=2 == nums[2]=2 → 跳過

fast=7: nums[7]=3 != nums[2]=2 → 寫入 nums[3]=3, slow=4
  陣列: [0, 1, 2, 3, 1, 2, 2, 3, 3, 4]
                    S

fast=8: nums[8]=3 == nums[3]=3 → 跳過

fast=9: nums[9]=4 != nums[3]=3 → 寫入 nums[4]=4, slow=5
  陣列: [0, 1, 2, 3, 4, 2, 2, 3, 3, 4]
                       S

結果: 長度=5, 前 5 個元素 = [0, 1, 2, 3, 4] ✓
      （後面的元素不重要，題目不管）
```

#### Corner Cases

| Case | 輸入 | 結果 |
|------|------|------|
| 空陣列 | `[]` | 0 |
| 單一元素 | `[5]` | 1 |
| 無重複 | `[1,2,3]` | 3（不變） |
| 全部相同 | `[7,7,7,7]` | 1 |

---

### 4.2 Move Zeroes — LeetCode 283

#### 問題描述

將陣列中所有 `0` 移到末尾，同時保持非零元素的相對順序。必須 in-place，不能 copy 陣列。

#### 核心思路

```
slow = "下一個非零值該放的位置"
fast = "掃描位置"

遇到非零 → swap(nums[slow], nums[fast]), slow++
遇到零   → 跳過（fast 繼續前進）

效果：
  [非零元素（保持原順序）| 零]
                        ↑
                       slow
```

#### Pseudocode

```python
slow = 0
for fast in range(len(nums)):
    if nums[fast] != 0:
        swap(nums[slow], nums[fast])
        slow += 1
```

#### 範例 1：nums = [0, 1, 0, 3, 12]

```
初始: slow=0
  [0, 1, 0, 3, 12]
   S
   F=0

fast=0: nums[0]=0 → 是零，跳過
  [0, 1, 0, 3, 12]
   S     F=1

fast=1: nums[1]=1 → 非零！swap(nums[0], nums[1])
  [1, 0, 0, 3, 12]   (0 和 1 交換)
      S     F=2       slow=1

fast=2: nums[2]=0 → 是零，跳過
  [1, 0, 0, 3, 12]
      S        F=3

fast=3: nums[3]=3 → 非零！swap(nums[1], nums[3])
  [1, 3, 0, 0, 12]   (0 和 3 交換)
         S     F=4    slow=2

fast=4: nums[4]=12 → 非零！swap(nums[2], nums[4])
  [1, 3, 12, 0, 0]   (0 和 12 交換)
             S        slow=3

結果: [1, 3, 12, 0, 0] ✓
```

#### 範例 2：nums = [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]

```
初始: slow=0

fast=0: 4 → 非零 → swap(nums[0],nums[0]) → 不動, slow=1
  [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
      S

fast=1: 2 → 非零 → swap(nums[1],nums[1]) → 不動, slow=2
  [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
         S

fast=2: 4 → 非零 → swap(nums[2],nums[2]) → 不動, slow=3
  [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
            S

fast=3: 0 → 跳過
fast=4: 0 → 跳過

fast=5: 3 → 非零 → swap(nums[3],nums[5])
  [4, 2, 4, 3, 0, 0, 0, 5, 1, 0]    (index 3 的 0 和 index 5 的 3 交換)
               S                      slow=4

fast=6: 0 → 跳過

fast=7: 5 → 非零 → swap(nums[4],nums[7])
  [4, 2, 4, 3, 5, 0, 0, 0, 1, 0]    slow=5

fast=8: 1 → 非零 → swap(nums[5],nums[8])
  [4, 2, 4, 3, 5, 1, 0, 0, 0, 0]    slow=6

fast=9: 0 → 跳過

結果: [4, 2, 4, 3, 5, 1, 0, 0, 0, 0] ✓
```

#### Corner Cases

| Case | 輸入 | 結果 |
|------|------|------|
| 全是零 | `[0,0,0]` | `[0,0,0]`（不變） |
| 沒有零 | `[1,2,3]` | `[1,2,3]`（不變） |
| 單一元素 | `[0]` | `[0]` |

---

### 4.3 Remove Element — LeetCode 27

#### 問題描述

原地移除陣列中所有等於 `val` 的元素，回傳新長度。

#### 核心思路 — 跟 Remove Duplicates 非常像

```
slow = "寫入位置"
fast = "讀取位置"

規則：
  if nums[fast] != val → 寫入 nums[slow], slow++
  if nums[fast] == val → 跳過

差異對比：
  Remove Duplicates: 跳過「跟前一個寫入值相同」的元素
  Remove Element:    跳過「等於 val」的元素
  Move Zeroes:       跳過「等於 0」的元素（其實跟 Remove Element 幾乎一樣）
```

#### Pseudocode

```python
slow = 0
for fast in range(len(nums)):
    if nums[fast] != val:
        nums[slow] = nums[fast]
        slow += 1
return slow
```

#### 範例 1：nums = [3, 2, 2, 3], val = 3

```
初始: slow=0

fast=0: nums[0]=3 == val=3 → 跳過
fast=1: nums[1]=2 != val=3 → nums[0]=2, slow=1
  [2, 2, 2, 3]
      S

fast=2: nums[2]=2 != val=3 → nums[1]=2, slow=2
  [2, 2, 2, 3]
         S

fast=3: nums[3]=3 == val=3 → 跳過

結果: 長度=2, nums[:2]=[2, 2] ✓
```

#### 範例 2：nums = [0, 1, 2, 2, 3, 0, 4, 2], val = 2

```
初始: slow=0

fast=0: 0 != 2 → nums[0]=0, slow=1
fast=1: 1 != 2 → nums[1]=1, slow=2
fast=2: 2 == 2 → 跳過
fast=3: 2 == 2 → 跳過
fast=4: 3 != 2 → nums[2]=3, slow=3
fast=5: 0 != 2 → nums[3]=0, slow=4
fast=6: 4 != 2 → nums[4]=4, slow=5
fast=7: 2 == 2 → 跳過

結果: 長度=5, nums[:5]=[0, 1, 3, 0, 4] ✓

陣列狀態變化：
  初始:     [0, 1, 2, 2, 3, 0, 4, 2]
  fast=0後: [0, 1, 2, 2, 3, 0, 4, 2]  slow=1
  fast=1後: [0, 1, 2, 2, 3, 0, 4, 2]  slow=2
  fast=4後: [0, 1, 3, 2, 3, 0, 4, 2]  slow=3  (index 2 被覆寫為 3)
  fast=5後: [0, 1, 3, 0, 3, 0, 4, 2]  slow=4
  fast=6後: [0, 1, 3, 0, 4, 0, 4, 2]  slow=5
```

#### 三題比較

```
┌──────────────────┬─────────────────────┬──────────────────┐
│      題目        │     跳過條件          │     寫入條件      │
├──────────────────┼─────────────────────┼──────────────────┤
│ Remove Duplicates│ nums[f]==nums[s-1]  │ nums[f]!=nums[s-1]│
│ Remove Element   │ nums[f]==val        │ nums[f]!=val      │
│ Move Zeroes      │ nums[f]==0          │ nums[f]!=0        │
└──────────────────┴─────────────────────┴──────────────────┘

本質完全相同：slow/fast，遇到「要保留的」就寫入 slow 位置。
唯一差別是「什麼算要保留的」。
```

---

## 第五章：快慢指針 (Fast-Slow / Floyd's Cycle Detection)

### 5.1 Find the Duplicate Number — LeetCode 287

#### 問題描述

陣列有 `n+1` 個整數，每個值都在 `[1, n]` 範圍內，恰好有一個重複的數字（可能重複多次），找出它。

**限制**：
- 不能修改原陣列
- 只能用 O(1) 額外空間
- 時間 O(n)

這些限制排除了 sort（O(n log n) 且修改陣列）、HashSet（O(n) space）、暴力（O(n^2)）。

#### 關鍵洞察：把 Array 當成 Linked List

因為每個值都在 `[1, n]` 範圍內，我們可以把 `nums[i]` 視為「指向 index nums[i]」的指針：

```
index:  0  1  2  3  4
value:  1  3  4  2  2

把它畫成 linked list：
  從 index 0 出發：
  0 → nums[0]=1 → nums[1]=3 → nums[3]=2 → nums[2]=4 → nums[4]=2 → nums[2]=4 → ...

  簡化：0 → 1 → 3 → 2 → 4 → 2 → 4 → 2 → ...
                       ↑       ↓
                       └── 4 ──┘   ← 這就是 cycle！

  重複的數字 = cycle 的入口 = 2
```

**為什麼重複數字 = cycle 入口？**

如果數字 `d` 重複了，代表有兩個不同的 index `i` 和 `j` 都使得 `nums[i] = nums[j] = d`。也就是說，`i` 和 `j` 都「指向」index `d`。當你從某條路徑走到 `d`，又從另一條路徑走到 `d`，就形成了 cycle，而 `d` 就是 cycle 入口。

#### Floyd's Cycle Detection 兩階段演算法

**Phase 1：找相遇點**

```
slow 從 index 0 出發，每次走一步：slow = nums[slow]
fast 從 index 0 出發，每次走兩步：fast = nums[nums[fast]]

因為有 cycle，fast 終會追上 slow（想像操場跑步，快的人一定會追上慢的人）
```

**Phase 2：找 cycle 入口**

```
把一個指針放回 index 0，另一個留在相遇點
兩個都改成每次走一步
再次相遇的地方 = cycle 入口 = 重複數字
```

**數學推導（為什麼 Phase 2 有效）**

```
設：
  a = 從起點到 cycle 入口的距離
  b = 從入口到相遇點的距離
  C = cycle 的總長度

Phase 1 結束時：
  slow 走了 a + b 步
  fast 走了 a + b + nC 步（在 cycle 裡多繞了 n 圈）

因為 fast 速度是 slow 的 2 倍：
  2(a + b) = a + b + nC
  a + b = nC
  a = nC - b

這表示：從起點走 a 步 = 從相遇點走 nC - b 步
而從相遇點走 C - b 步剛好回到入口（再多走 (n-1)C 圈還是在入口）

所以：從起點和從相遇點同時以速度 1 前進，會在入口相遇！
```

#### 範例 1：nums = [1, 3, 4, 2, 2]

```
Linked List 結構：
  0 → 1 → 3 → 2 → 4 ─┐
                  ↑    │
                  └────┘

  a=3 (0→1→3→2，從 0 到入口 2 走 3 步... 不對，讓我們直接追蹤)

═══ Phase 1：找相遇點 ═══

  初始: slow=0, fast=0

  Step 1:
    slow = nums[0] = 1
    fast = nums[nums[0]] = nums[1] = 3
    slow=1, fast=3 → 不相等

  Step 2:
    slow = nums[1] = 3
    fast = nums[nums[3]] = nums[2] = 4
    slow=3, fast=4 → 不相等

  Step 3:
    slow = nums[3] = 2
    fast = nums[nums[4]] = nums[2] = 4
    slow=2, fast=4 → 不相等

  Step 4:
    slow = nums[2] = 4
    fast = nums[nums[4]] = nums[2] = 4
    slow=4, fast=4 → 相遇！

═══ Phase 2：找入口 ═══

  slow 留在 4，slow2 從 0 出發，都走一步

  Step 1:
    slow  = nums[4] = 2
    slow2 = nums[0] = 1
    不相等

  Step 2:
    slow  = nums[2] = 4
    slow2 = nums[1] = 3
    不相等

  Step 3:
    slow  = nums[4] = 2
    slow2 = nums[3] = 2
    相遇！slow == slow2 == 2

重複數字是 2 ✓
```

#### 範例 2：nums = [3, 1, 3, 4, 2]

```
Linked List 結構：
  0 → 3 → 4 → 2 → 3 ─┐
          ↑            │
          └────────────┘

═══ Phase 1：找相遇點 ═══

  初始: slow=0, fast=0

  Step 1:
    slow = nums[0] = 3
    fast = nums[nums[0]] = nums[3] = 4
    slow=3, fast=4

  Step 2:
    slow = nums[3] = 4
    fast = nums[nums[4]] = nums[2] = 3
    slow=4, fast=3

  Step 3:
    slow = nums[4] = 2
    fast = nums[nums[3]] = nums[4] = 2
    slow=2, fast=2 → 相遇！

═══ Phase 2：找入口 ═══

  slow=2, slow2=0

  Step 1:
    slow  = nums[2] = 3
    slow2 = nums[0] = 3
    相遇！slow == slow2 == 3

重複數字是 3 ✓（只需 1 步就找到入口）
```

#### 完整程式碼

```python
def findDuplicate(nums):
    # Phase 1: 快慢指針找相遇點
    slow = fast = 0
    while True:
        slow = nums[slow]           # 走一步
        fast = nums[nums[fast]]     # 走兩步
        if slow == fast:
            break

    # Phase 2: 找 cycle 入口
    slow2 = 0
    while slow != slow2:
        slow = nums[slow]           # 都走一步
        slow2 = nums[slow2]

    return slow  # 入口 = 重複數字
```

#### Corner Cases

| Case | 範例 | 注意 |
|------|------|------|
| 重複出現多次 | `[2,2,2,2,2]` | cycle 很短，但演算法照樣有效 |
| 重複在開頭 | `[1,1,2]` | 正常運作 |
| 大陣列 | n=100000 | O(n) 時間 O(1) 空間，完全 OK |

---

## 第六章：方法比較與面試決策

### 6.1 完整決策樹

```
看到 Array 題目
│
├─ 陣列已排序？
│  ├─ YES → 找兩數/三數/四數之和？
│  │         ├─ YES → 對向雙指針 (Two Sum II, 3Sum, 4Sum)
│  │         └─ NO  → 二分搜尋 (Binary Search，下一章)
│  └─ NO  → 繼續往下判斷
│
├─ 要求 in-place 修改？（去重/移除/搬移）
│  ├─ YES → 同向雙指針 (Remove Duplicates, Move Zeroes, Remove Element)
│  └─ NO  → 繼續往下判斷
│
├─ 題目有「回文」、「頭尾對稱」性質？
│  ├─ YES → 對向雙指針 (Valid Palindrome)
│  └─ NO  → 繼續往下判斷
│
├─ 需要偵測 cycle 或找重複且限制 O(1) space 不能改原陣列？
│  ├─ YES → 快慢指針 / Floyd's (Find Duplicate, Linked List Cycle)
│  └─ NO  → 繼續往下判斷
│
├─ 需要連續子陣列的最大/最小/恰好符合某條件？
│  └─ → Sliding Window（下一章）
│
└─ 需要快速查找某元素是否存在？
   └─ → HashMap / HashSet（第三章）
```

### 6.2 三種 Two Pointers 並排比較

```
┌─────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│             │   對向雙指針          │   同向雙指針          │   快慢指針            │
│             │ (Opposite Direction) │ (Same Direction)     │ (Fast-Slow / Floyd)  │
├─────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 指針起點     │ left=0, right=n-1   │ slow=0, fast=0       │ slow=0, fast=0       │
│ 移動方向     │ ← 向中間靠攏 →       │ → 同方向前進 →       │ → 同方向，速度不同 →  │
│ 移動規則     │ 依比較結果移左或右    │ fast 每次+1          │ slow+1, fast+2       │
│ 終止條件     │ left >= right       │ fast 到底            │ 兩指針相遇            │
│ 前提條件     │ 通常需要排序         │ 不一定要排序          │ 需要有 cycle 結構     │
├─────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 時間複雜度   │ O(n)                │ O(n)                 │ O(n)                │
│ 空間複雜度   │ O(1)                │ O(1)                 │ O(1)                │
├─────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 經典題目     │ Two Sum II (167)    │ Remove Dup (26)      │ Find Dup (287)      │
│             │ Container Water (11)│ Move Zeroes (283)    │ LL Cycle (141/142)  │
│             │ Valid Palindrome(125)│ Remove Element (27)  │ Happy Number (202)  │
│             │ 3Sum (15)           │ Sort Colors (75)     │ Middle of LL (876)  │
└─────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

### 6.3 常見錯誤與避免方式

```
錯誤 1: 對向雙指針忘記 while left < right 的 < 寫成 <=
  → 會多做一步，可能造成重複計算或 index out of bounds

錯誤 2: 3Sum 去重邏輯寫錯
  → 外層要 if i > 0 and nums[i] == nums[i-1]: continue
  → 不是 nums[i] == nums[i+1]！那樣會跳過有效的起始值

錯誤 3: 同向雙指針 slow 的初始值搞錯
  → Remove Duplicates: slow=1（第一個元素一定保留）
  → Move Zeroes / Remove Element: slow=0

錯誤 4: Floyd's Algorithm Phase 2 搞錯起始點
  → 一個從「相遇點」繼續走，一個從「index 0」開始走
  → 不是兩個都從 0 開始！

錯誤 5: Container Water 相等時不知道移哪邊
  → 相等時移哪邊都可以（結果一樣），但不能不移
```

### 6.4 面試框架：Clarify → Approach → Code → Test

```
Step 1: Clarify（釐清問題）— 花 1-2 分鐘
  "Is the array sorted?"
  "Can there be duplicates?"
  "Should I return indices or values?"
  "Is the answer 0-indexed or 1-indexed?"
  "Can I modify the original array?"
  "What about edge cases — empty array? single element?"

Step 2: Approach（說明方法）— 花 2-3 分鐘
  "I'm thinking of using two pointers because..."
  "The time complexity would be O(n) and space O(1)."
  "Let me walk through an example first..."
  （在白板上畫出指針移動的過程）

Step 3: Code（寫程式）— 花 10-15 分鐘
  先寫框架（function signature, while loop）
  再填邏輯
  注意命名清楚（left/right 或 slow/fast）

Step 4: Test（測試）— 花 3-5 分鐘
  用範例 dry run 你的 code
  測 corner case: 空陣列、只有一個元素、全部相同
  確認 return 值是否正確（index vs value, 0 vs 1 indexed）
```

### 6.5 本章所有題目的 LeetCode 題號速查

| 題目 | 題號 | 難度 | 指針類型 | Google 頻率 |
|------|------|------|----------|------------|
| Two Sum II | 167 | Medium | 對向 | 中 |
| Container With Most Water | 11 | Medium | 對向 | 高 |
| Valid Palindrome | 125 | Easy | 對向 | 中 |
| 3Sum | 15 | Medium | 對向 | 非常高 |
| Remove Duplicates | 26 | Easy | 同向 | 中 |
| Move Zeroes | 283 | Easy | 同向 | 高 |
| Remove Element | 27 | Easy | 同向 | 低 |
| Find Duplicate Number | 287 | Medium | 快慢 | 高 |

---

> **下一章預告**：`02_Sliding_Window_教學.md` — 滑動窗口，同向雙指針的進階應用，
> 用於「連續子陣列/子字串」問題。Two Pointers 是 Sliding Window 的基礎，
> 務必先把本章練熟！
