# Greedy 貪心演算法完全教學手冊

> **適用對象**：基礎較弱、準備 Google 面試的工程師
> **教學風格**：大學教科書等級，每個觀念都有 2+ 組完整數值追蹤
> **語言**：繁體中文解說 + English technical terms
> **配套程式**：`14_Greedy.py`（可直接執行驗證所有範例）

---

## 第一章：Greedy 貪心法核心概念

### 1.1 什麼是 Greedy？

Greedy（貪心法）的精神只有一句話：

> **每一步都做出「當下看起來最好」的選擇，而且做了就不回頭。**

跟人生不一樣的是，在某些特定問題中，這種「只看眼前」的策略竟然能得到**全域最佳解（Global Optimum）**。

```
Greedy 的運作模式：

  問題 → 做出局部最佳選擇 → 子問題 → 做出局部最佳選擇 → 子問題 → ... → 解

  特徵：
  1. 每一步只考慮「當下」，不考慮未來的所有可能
  2. 一旦做了選擇就不回頭（no backtracking）
  3. 比 DP 快很多（通常 O(n) 或 O(n log n)），但不是所有問題都能用
```

### 1.2 什麼時候 Greedy 有效？

Greedy 能保證得到最佳解，必須同時滿足兩個數學性質：

```
條件 1: Greedy Choice Property（貪心選擇性質）
  → 做出「局部最佳」的選擇後，一定存在一個「全域最佳解」包含這個選擇
  → 白話：你的貪心選擇不會把你帶到死胡同

條件 2: Optimal Substructure（最佳子結構）
  → 做完一個選擇之後，剩下的子問題本身也有最佳子結構
  → 白話：大問題的最佳解可以從子問題的最佳解組合而來
  （注意：DP 也需要 optimal substructure，但 DP 不需要 greedy choice property）
```

### 1.3 什麼時候 Greedy 失敗？用 Counterexample 驗證！

**這是面試中最關鍵的判斷能力**：你怎麼知道一個問題能不能用 Greedy？

方法：試著找一個 counterexample（反例）。如果找不到，Greedy 大概可以用。

### 1.4 經典對比：Coin Change 硬幣找零

**Case 1: Coins = [1, 5, 10, 25], amount = 30 — Greedy 成功**

```
Greedy 策略：每次挑面額最大的硬幣

Step 1: 剩餘 30, 最大可用 = 25 → 選 25 → 剩餘 30 - 25 = 5
Step 2: 剩餘  5, 最大可用 = 5  → 選  5 → 剩餘  5 -  5 = 0
完成！

Greedy 結果: [25, 5] → 2 枚硬幣 ✓ 這就是最佳解！

為什麼成功？
因為這組面額有「倍數關係」的特性：
  25 = 5 × 5
  10 = 5 × 2
   5 = 5 × 1
   1 = 基礎單位
任何用小面額湊出來的組合，都能被更少的大面額取代。
```

**Case 2: Coins = [1, 3, 4], amount = 6 — Greedy 失敗！**

```
Greedy 策略：每次挑面額最大的硬幣

Step 1: 剩餘 6, 最大可用 = 4 → 選 4 → 剩餘 6 - 4 = 2
Step 2: 剩餘 2, 最大可用 = 1 → 選 1 → 剩餘 2 - 1 = 1
Step 3: 剩餘 1, 最大可用 = 1 → 選 1 → 剩餘 1 - 1 = 0
完成！

Greedy 結果: [4, 1, 1] → 3 枚硬幣 ✗ 不是最佳！

最佳解:       [3, 3]   → 2 枚硬幣 ✓

┌────────────────────────────────────────────────────────┐
│ 為什麼 Greedy 失敗？                                    │
│                                                        │
│ Greedy 選了 4 之後，剩餘 2 只能用 1+1（因為 3 > 2）。  │
│ 但如果一開始選 3，剩餘 3 可以完美用一個 3 來解決。      │
│                                                        │
│ 根本原因：面額之間不存在整除/倍數關係。                  │
│ 4 不是 3 的倍數，所以「先選最大」可能浪費空間。          │
│ 這種情況必須用 DP 考慮所有可能的組合。                   │
└────────────────────────────────────────────────────────┘
```

**DP 如何解 Case 2（簡要對比）**

```
DP 建表: dp[i] = 湊出金額 i 所需的最少硬幣數

  amount:  0   1   2   3   4   5   6
  dp:     [0,  1,  2,  1,  1,  2,  2]

  dp[0] = 0                     (不需要任何硬幣)
  dp[1] = dp[0]+1 = 1           (用 1 枚 1)
  dp[2] = dp[1]+1 = 2           (用 2 枚 1)
  dp[3] = min(dp[2]+1, dp[0]+1) = min(3, 1) = 1  (用 1 枚 3)
  dp[4] = min(dp[3]+1, dp[1]+1, dp[0]+1) = min(2, 2, 1) = 1  (用 1 枚 4)
  dp[5] = min(dp[4]+1, dp[2]+1) = min(2, 3) = 2  (用 4+1 或 3+2 都是 2 枚)
  dp[6] = min(dp[5]+1, dp[3]+1, dp[2]+1) = min(3, 2, 3) = 2  (用 3+3)

答案: dp[6] = 2 ✓

DP 考慮了所有可能，不會遺漏最佳解。
但時間 O(amount × len(coins))，比 Greedy 的 O(amount) 慢。
```

### 1.5 Greedy 的使用信號

```
看到以下關鍵字，考慮 Greedy：
  - "minimum number of..." / "maximum number of..."
  - "最少需要幾個..." / "最多能選幾個..."
  - 區間排程、活動選擇
  - 每一步的選擇互不影響後續選擇的結構

看到以下情況，Greedy 可能不適用：
  - "find all possible ways" → 通常是 backtracking
  - 選擇之間有複雜的依賴關係 → 通常是 DP
  - 找不到明確的排序/比較規則 → 可能需要 DP
```

---

## 第二章：區間問題 (Interval Problems) — Google 最愛類型

區間問題是 Greedy 最經典的應用場景。核心技巧：**先排序，再逐一掃描決策**。

### 2.1 Merge Intervals — LeetCode 56

#### 問題描述

給定一組區間 `intervals`，合併所有重疊（overlapping）的區間，回傳合併後的結果。

#### 核心思路

```
Step 1: 按 start 排序
Step 2: 逐一掃描，跟 merged 列表的最後一個區間比較
  - 如果 current.start <= last.end → 重疊！合併（擴展 end）
  - 如果 current.start >  last.end → 不重疊，新增一個區間

重疊判斷圖示：
  Case A: 重疊    last: [───────]
                  curr:    [────────]     curr.start <= last.end
                  合併: [────────────]

  Case B: 包含    last: [────────────]
                  curr:   [──────]        curr.start <= last.end
                  合併: [────────────]    (last.end 不變)

  Case C: 相鄰    last: [────]
                  curr:      [────]       curr.start <= last.end (相等)
                  合併: [─────────]

  Case D: 不重疊  last: [────]
                  curr:        [────]     curr.start > last.end
                  不合併，各自獨立
```

#### Pseudocode

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])   # 按 start 排序
    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        if intervals[i][0] <= merged[-1][1]:  # 重疊
            merged[-1][1] = max(merged[-1][1], intervals[i][1])
        else:                                  # 不重疊
            merged.append(intervals[i])

    return merged
```

**Time: O(n log n)**（排序主導），**Space: O(n)**（worst case 全部不重疊）

#### 範例 1：intervals = [[1,3],[2,6],[8,10],[15,18]]

```
Step 0: 排序（已排序）→ [[1,3],[2,6],[8,10],[15,18]]

初始: merged = [[1,3]]

Step 1: 比較 [2,6] 和 merged 最後一個 [1,3]
  2 <= 3？ YES → 重疊！
  合併: [1, max(3,6)] = [1,6]
  merged = [[1,6]]

  圖示: [1───3]
           [2──────6]
        [1─────────6]  ← 合併結果

Step 2: 比較 [8,10] 和 merged 最後一個 [1,6]
  8 <= 6？ NO → 不重疊
  新增 [8,10]
  merged = [[1,6],[8,10]]

Step 3: 比較 [15,18] 和 merged 最後一個 [8,10]
  15 <= 10？ NO → 不重疊
  新增 [15,18]
  merged = [[1,6],[8,10],[15,18]]

結果: [[1,6],[8,10],[15,18]] ✓
```

#### 範例 2：intervals = [[1,4],[4,5]]（邊界相鄰）

```
Step 0: 排序 → [[1,4],[4,5]]

初始: merged = [[1,4]]

Step 1: 比較 [4,5] 和 [1,4]
  4 <= 4？ YES → 重疊（相鄰也算重疊）！
  合併: [1, max(4,5)] = [1,5]
  merged = [[1,5]]

結果: [[1,5]] ✓

注意：[1,4] 和 [4,5] 在 x=4 這個點上「碰到」了，所以合併。
如果題目定義「touching = not overlapping」，判斷就要改成 < 而非 <=。
但 LeetCode 56 的定義是 touching = overlapping。
```

#### Corner Cases

```
┌───────────────────┬────────────────────────────────┬──────────────┐
│ Case              │ 輸入                            │ 結果          │
├───────────────────┼────────────────────────────────┼──────────────┤
│ 單一區間          │ [[1,3]]                        │ [[1,3]]      │
│ 全部重疊          │ [[1,4],[2,3],[0,5]]            │ [[0,5]]      │
│ 全部不重疊        │ [[1,2],[3,4],[5,6]]            │ 原樣不變      │
│ 巢狀包含          │ [[1,10],[2,3],[4,5]]           │ [[1,10]]     │
│ 排序前後不同      │ [[3,4],[1,2]]                  │ [[1,2],[3,4]]│
└───────────────────┴────────────────────────────────┴──────────────┘
```

---

### 2.2 Non-overlapping Intervals — LeetCode 435

#### 問題描述

給定一組區間，找出**最少要移除幾個區間**，才能使剩餘的區間彼此不重疊。

#### 核心思路：按 END 排序（不是 start！）

```
為什麼按 end 排序？

直覺：結束越早的區間，留給後面的「空間」越多。
如果我們總是保留「結束最早」的那一個，就能容納最多不重疊的區間。
這就是經典的 Activity Selection Problem（活動選擇問題）。

反過來想：
  最少移除數 = 總區間數 - 最多可保留的不重疊區間數
  所以問題等價於：找出最多有幾個不重疊的區間（sort by end + greedy）

演算法：
  1. 按 end time 排序
  2. 追蹤 current_end = 第一個區間的 end
  3. 對每個後續區間：
     - 如果 start >= current_end → 不重疊，保留，更新 current_end
     - 如果 start <  current_end → 重疊，移除（count++）
```

#### Pseudocode

```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])  # 按 end 排序！
    count = 0
    end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < end:    # 重疊
            count += 1               # 移除這個區間
        else:                         # 不重疊
            end = intervals[i][1]    # 更新 end

    return count
```

**Time: O(n log n)**，**Space: O(1)**（不計排序空間）

#### 範例 1：intervals = [[1,2],[2,3],[3,4],[1,3]]

```
Step 0: 按 end 排序 → [[1,2],[2,3],[1,3],[3,4]]
                             end=2  end=3  end=3  end=4

初始: 保留 [1,2], current_end = 2, count = 0

Step 1: 比較 [2,3], start=2 >= end=2？ YES → 不重疊，保留
  current_end = 3
  ──[1,2]
        ──[2,3]     ← 保留 ✓

Step 2: 比較 [1,3], start=1 >= end=3？ NO → 重疊！移除
  count = 1
  ──[1,2]
        ──[2,3]
  ──[1,────3]       ← 移除 ✗（跟 [2,3] 重疊）

Step 3: 比較 [3,4], start=3 >= end=3？ YES → 不重疊，保留
  current_end = 4
  ──[1,2]
        ──[2,3]
              ──[3,4]  ← 保留 ✓

結果: count = 1（只需移除 1 個區間 [1,3]） ✓
保留的區間: [1,2],[2,3],[3,4]
```

#### 範例 2：intervals = [[1,2],[1,2],[1,2]]（全部相同）

```
Step 0: 按 end 排序 → [[1,2],[1,2],[1,2]]（排序後不變）

初始: 保留 [1,2], current_end = 2, count = 0

Step 1: [1,2], start=1 < end=2？ YES → 重疊！移除。count = 1
Step 2: [1,2], start=1 < end=2？ YES → 重疊！移除。count = 2

結果: count = 2（保留 1 個，移除 2 個） ✓
```

#### 為什麼按 start 排序會出錯？

```
反例: intervals = [[1,100],[2,3],[4,5]]

按 start 排序: [[1,100],[2,3],[4,5]]
  保留 [1,100], end=100
  [2,3] start=2 < 100 → 移除
  [4,5] start=4 < 100 → 移除
  結果: 移除 2 個 ← 錯！

按 end 排序: [[2,3],[4,5],[1,100]]
  保留 [2,3], end=3
  [4,5] start=4 >= 3 → 保留, end=5
  [1,100] start=1 < 5 → 移除
  結果: 移除 1 個 ← 對！

按 start 排序時，[1,100] 這個「超長」區間先被選中，
把後面兩個短區間都擋掉了。按 end 排序就避免了這個問題。
```

---

### 2.3 Meeting Rooms II — LeetCode 253（Google 高頻）

#### 問題描述

給定一組會議的 `[start, end]` 時間，求**同時需要幾間會議室**（peak concurrent meetings）。

#### 核心思路：Sort by Start + Min-Heap

```
直覺：
  按開始時間排序後，依序安排每場會議。
  用一個 min-heap 記錄「每間會議室目前的結束時間」。
  - 新會議開始時，看 heap 頂端（最早結束的會議室）
  - 如果那間會議室已經結束（end <= new start）→ 重用，pop + push
  - 如果還沒結束 → 需要一間新的會議室，直接 push
  - heap 的大小 = 目前需要的會議室數量

為什麼用 min-heap？
  我們需要快速找到「最早結束」的會議室，看能不能重用。
  Min-heap 的 peek/pop/push 都是 O(log n)。
```

#### Pseudocode

```python
import heapq

def minMeetingRooms(intervals):
    intervals.sort(key=lambda x: x[0])  # 按 start 排序
    heap = []  # min-heap，存放每間會議室的結束時間

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # 重用最早結束的會議室
        heapq.heappush(heap, end)

    return len(heap)  # heap 大小 = 會議室數量
```

**Time: O(n log n)**，**Space: O(n)**

#### 範例 1：intervals = [[0,30],[5,10],[15,20]]

```
Step 0: 排序（已排序）→ [[0,30],[5,10],[15,20]]

初始: heap = []

Step 1: 會議 [0,30]
  heap 為空 → 開一間新會議室
  heap.push(30)
  heap = [30]  (1 間會議室)

  時間軸:
  Room 1: [0═══════════════════════════════30]
          0    5    10   15   20   25   30

Step 2: 會議 [5,10]
  heap 頂端 = 30, 30 > 5 → 會議室 1 還在用，不能重用
  heap.push(10)
  heap = [10, 30]  (2 間會議室)

  時間軸:
  Room 1: [0═══════════════════════════════30]
  Room 2:      [5════10]
          0    5    10   15   20   25   30

Step 3: 會議 [15,20]
  heap 頂端 = 10, 10 <= 15 → 會議室 2 已結束，可以重用！
  heap.pop() → 移除 10
  heap.push(20)
  heap = [20, 30]  (仍然 2 間會議室)

  時間軸:
  Room 1: [0═══════════════════════════════30]
  Room 2:      [5════10]  [15═══20]
          0    5    10   15   20   25   30

結果: len(heap) = 2 間會議室 ✓

peak 在 t=5~10 之間（Room 1 和 Room 2 同時使用）
```

#### 範例 2：intervals = [[7,10],[2,4]]（無重疊）

```
Step 0: 排序 → [[2,4],[7,10]]

初始: heap = []

Step 1: 會議 [2,4]
  heap 為空 → 新會議室
  heap.push(4)
  heap = [4]  (1 間)

Step 2: 會議 [7,10]
  heap 頂端 = 4, 4 <= 7 → 可以重用！
  heap.pop() → 移除 4
  heap.push(10)
  heap = [10]  (仍然 1 間)

  時間軸:
  Room 1: [2══4]     [7═══10]
          0    2   4    7   10

結果: 1 間會議室 ✓（兩場會議不重疊，一間就夠）
```

#### 替代解法：掃描線（Sweep Line）

```
另一種思路：把所有時間點拆成「事件」

  每個 [start, end] 拆成兩個事件：
    (start, +1)  → 會議開始，需求 +1
    (end,   -1)  → 會議結束，需求 -1

  排序所有事件，掃描並追蹤 concurrent count。

範例: [[0,30],[5,10],[15,20]]
  事件: [(0,+1), (5,+1), (10,-1), (15,+1), (20,-1), (30,-1)]

  t=0:  count=0+1=1
  t=5:  count=1+1=2  ← peak!
  t=10: count=2-1=1
  t=15: count=1+1=2  ← tied peak
  t=20: count=2-1=1
  t=30: count=1-1=0

  最大 count = 2 ✓
```

---

## 第三章：跳躍型 Greedy

### 3.1 Jump Game — LeetCode 55

#### 問題描述

陣列 `nums` 中，`nums[i]` 代表在 index `i` 最多能往前跳 `nums[i]` 步。從 index 0 出發，判斷能否到達最後一個 index。

#### 核心思路：追蹤 max_reach

```
Greedy 策略：
  維護一個 max_reach（目前能到達的最遠位置）
  從左到右掃描：
    - 如果 i > max_reach → 到不了 i，回傳 False
    - 否則更新 max_reach = max(max_reach, i + nums[i])
    - 如果 max_reach >= n-1 → 能到終點，回傳 True

為什麼 Greedy 有效？
  我們不需要知道「怎麼跳」，只需要知道「最遠能到哪」。
  每到一個位置就盡量擴展可達範圍，如果某個位置超出可達範圍就失敗。
```

#### Pseudocode

```python
def canJump(nums):
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True
```

**Time: O(n)**，**Space: O(1)**

#### 範例 1：nums = [2, 3, 1, 1, 4]（能到達）

```
n = 5, 目標 = index 4

初始: max_reach = 0

i=0: i=0 <= max_reach=0 ✓ (可以到達 index 0)
     max_reach = max(0, 0+2) = 2
     「從 index 0 可以跳到 index 1 或 2」

i=1: i=1 <= max_reach=2 ✓
     max_reach = max(2, 1+3) = 4
     「從 index 1 可以跳到最遠 index 4」
     4 >= 4 (n-1) → 已經能到終點了！

i=2: i=2 <= max_reach=4 ✓
     max_reach = max(4, 2+1) = 4 (不變)

i=3: i=3 <= max_reach=4 ✓
     max_reach = max(4, 3+1) = 4 (不變)

i=4: i=4 <= max_reach=4 ✓ → 到達終點！

return True ✓

追蹤圖:
  index:      0    1    2    3    4
  nums:      [2,   3,   1,   1,   4]
  max_reach:  2    4    4    4    4
              ↑    ↑
              初始  在這裡就確定能到終點了
```

#### 範例 2：nums = [3, 2, 1, 0, 4]（無法到達）

```
n = 5, 目標 = index 4

初始: max_reach = 0

i=0: i=0 <= 0 ✓
     max_reach = max(0, 0+3) = 3

i=1: i=1 <= 3 ✓
     max_reach = max(3, 1+2) = 3 (不變)

i=2: i=2 <= 3 ✓
     max_reach = max(3, 2+1) = 3 (不變)

i=3: i=3 <= 3 ✓
     max_reach = max(3, 3+0) = 3 (不變！因為 nums[3]=0)

i=4: i=4 > max_reach=3 ✗ → 到不了 index 4！

return False ✓

追蹤圖:
  index:      0    1    2    3    4
  nums:      [3,   2,   1,   0,   4]
  max_reach:  3    3    3    3    ← 卡在 3，永遠到不了 4
                             ↑
                          nums[3]=0 是死路！
                          所有能到 index 3 的路徑都被堵住了
```

---

### 3.2 Jump Game II — LeetCode 45

#### 問題描述

跟 Jump Game 一樣的設定，但**保證一定能到終點**，問**最少需要幾跳**？

#### 核心思路：BFS-like 分層擴展

```
把問題想成 BFS：
  第 0 跳可以到的範圍 = [0, 0]
  第 1 跳可以到的範圍 = [0+1, 能到最遠的地方]
  第 2 跳可以到的範圍 = [上一層最遠+1, 這一層能到最遠]
  ...

維護兩個變數：
  current_end = 當前這一跳能到的最遠位置
  farthest    = 在當前這一跳的範圍內，下一跳能到的最遠位置
  jumps       = 跳了幾次

當 i 走到 current_end 時，必須再跳一次：
  jumps++
  current_end = farthest
```

#### Pseudocode

```python
def jump(nums):
    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):  # 注意：不需要處理最後一個
        farthest = max(farthest, i + nums[i])
        if i == current_end:         # 到達這一跳的邊界
            jumps += 1
            current_end = farthest

    return jumps
```

**Time: O(n)**，**Space: O(1)**

#### 範例 1：nums = [2, 3, 1, 1, 4]

```
n = 5, 初始: jumps=0, current_end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2
     i==current_end (0==0) → 跳！jumps=1, current_end=2

     「第 1 跳：從 index 0 出發，能到 index 0~2」
     Jump 1 covers: [index 0] → can reach [index 1, index 2]

i=1: farthest = max(2, 1+3) = 4
     i != current_end (1 != 2) → 不跳，繼續探索

i=2: farthest = max(4, 2+1) = 4
     i==current_end (2==2) → 跳！jumps=2, current_end=4

     「第 2 跳：從 index 1 或 2 出發，能到 index 4」
     Jump 2 covers: [index 1, index 2] → can reach up to [index 4]

i=3: farthest = max(4, 3+1) = 4
     i != current_end (3 != 4) → 不跳

(i=4 是最後一個，不處理)

結果: jumps = 2 ✓

路徑: index 0 →(跳2步)→ index 2 →(跳... 不對)
實際最佳路徑: index 0 →(跳1步)→ index 1 →(跳3步)→ index 4
           或: index 0 →(跳2步)→ index 2 →(跳1步)→ index 3 →... 這需要3跳

最佳: 0 → 1 → 4 (2 跳) ✓

BFS 分層圖:
  Layer 0: [0]           (起點)
  Layer 1: [1, 2]        (從 0 可以跳到 1 或 2)
  Layer 2: [3, 4]        (從 1 可以跳到 2,3,4; 從 2 可以跳到 3)
  到達 index 4 在 Layer 2 → 2 跳
```

#### 範例 2：nums = [2, 3, 0, 1, 4]

```
n = 5, 初始: jumps=0, current_end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2
     i==current_end → jumps=1, current_end=2

i=1: farthest = max(2, 1+3) = 4
     i != current_end

i=2: farthest = max(4, 2+0) = 4  (nums[2]=0，但已經有 farthest=4)
     i==current_end → jumps=2, current_end=4

i=3: farthest = max(4, 3+1) = 4
     i != current_end

結果: jumps = 2 ✓

注意：雖然 nums[2]=0（死路），但從 index 1 可以直接跳到 index 4，
所以 farthest 在 i=1 就已經更新到 4 了。nums[2]=0 不影響結果。

BFS 分層:
  Layer 0: [0]
  Layer 1: [1, 2]
  Layer 2: [3, 4]        (index 1 的 nums[1]=3 可以跳到 4)
  2 跳 ✓
```

---

### 3.3 Gas Station — LeetCode 134

#### 問題描述

環形路線上有 `n` 個加油站，第 `i` 站有 `gas[i]` 單位的油，從 `i` 到 `i+1` 需要消耗 `cost[i]` 的油。油箱初始為空，求從哪個加油站出發可以繞完一圈。如果存在解，保證唯一。

#### 核心思路

```
觀察 1: 如果 sum(gas) < sum(cost) → 不可能繞完一圈，回傳 -1
觀察 2: 如果 sum(gas) >= sum(cost) → 一定存在一個起點可以繞完

Greedy 策略：
  追蹤 cumulative balance (油量 - 消耗)。
  如果在某個位置 balance 跌到負數 → 之前的所有起點都不行，
  下一個位置作為新的起點。

為什麼？
  如果從 start 出發到 i 時 balance < 0，
  那麼從 start 到 i 之間任何一點 j 出發也不行，
  因為 start→j 的 balance >= 0（否則早就失敗了），
  少了 start→j 這段正值，balance 只會更低。
```

#### Pseudocode

```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1

    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:       # 走不下去了
            start = i + 1  # 下一站作為新起點
            tank = 0        # 油箱重置

    return start
```

**Time: O(n)**，**Space: O(1)**

#### 範例 1：gas = [1,2,3,4,5], cost = [3,4,5,1,2]

```
sum(gas) = 15, sum(cost) = 15 → 15 >= 15，解存在

各站淨收益 (gas[i] - cost[i]):
  station:  0    1    2    3    4
  gas:     [1,   2,   3,   4,   5]
  cost:    [3,   4,   5,   1,   2]
  net:     [-2,  -2,  -2,  +3,  +3]

初始: start=0, tank=0

i=0: tank = 0 + (1-3) = -2
     tank < 0 → 從 0 出發不行！start=1, tank=0

i=1: tank = 0 + (2-4) = -2
     tank < 0 → 從 1 出發也不行！start=2, tank=0

i=2: tank = 0 + (3-5) = -2
     tank < 0 → 從 2 出發也不行！start=3, tank=0

i=3: tank = 0 + (4-1) = 3
     tank >= 0 ✓ 繼續

i=4: tank = 3 + (5-2) = 6
     tank >= 0 ✓ 繼續

結果: start = 3 ✓

驗證：從 station 3 出發繞一圈
  station 3: tank = 0 + 4 = 4, cost to 4 = 1, tank = 4 - 1 = 3
  station 4: tank = 3 + 5 = 8, cost to 0 = 2, tank = 8 - 2 = 6
  station 0: tank = 6 + 1 = 7, cost to 1 = 3, tank = 7 - 3 = 4
  station 1: tank = 4 + 2 = 6, cost to 2 = 4, tank = 6 - 4 = 2
  station 2: tank = 2 + 3 = 5, cost to 3 = 5, tank = 5 - 5 = 0
  全程 tank >= 0 ✓ 成功繞完！
```

#### 範例 2：gas = [2,3,4], cost = [3,4,3]

```
sum(gas) = 9, sum(cost) = 10 → 9 < 10，解不存在

各站淨收益:
  station:  0    1    2
  net:     [-1,  -1,  +1]
  總和 = -1 (不夠油繞一圈)

結果: -1 ✓
```

---

## 第四章：分配型 Greedy

### 4.1 Assign Cookies — LeetCode 455

#### 問題描述

有一群小孩，每個小孩有一個「滿足度門檻」`g[i]`。有一批餅乾，每塊餅乾大小為 `s[j]`。一塊餅乾 `s[j]` 只能給一個小孩，且只有在 `s[j] >= g[i]` 時小孩才會滿足。求最多能滿足幾個小孩。

#### 核心思路

```
Greedy 策略：
  把小孩和餅乾都排序。
  用最小的餅乾去滿足最容易滿足的小孩（門檻最低的）。
  如果最小的餅乾連最容易的小孩都滿足不了，那這塊餅乾就沒用。

為什麼有效？
  如果一塊大餅乾用來滿足容易的小孩，那難伺候的小孩就沒餅乾了。
  反過來，小餅乾能滿足容易的小孩，把大餅乾留給難伺候的 → 最優。
```

#### Pseudocode

```python
def findContentChildren(g, s):
    g.sort()  # 小孩門檻排序
    s.sort()  # 餅乾大小排序
    child = 0
    cookie = 0

    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:  # 這塊餅乾能滿足這個小孩
            child += 1              # 下一個小孩
        cookie += 1                 # 不管能不能滿足，這塊餅乾都用掉了（或跳過）

    return child
```

**Time: O(n log n + m log m)**，**Space: O(1)**

#### 範例 1：g = [1, 2, 3], s = [1, 1]

```
排序後: g = [1, 2, 3], s = [1, 1]

child=0, cookie=0: s[0]=1 >= g[0]=1？ YES → 滿足！child=1, cookie=1
child=1, cookie=1: s[1]=1 >= g[1]=2？ NO  → 跳過這塊餅乾。cookie=2
cookie=2 >= len(s)=2 → 結束

結果: 1 個小孩被滿足 ✓
（只有門檻=1 的小孩拿到餅乾，門檻=2 和 3 的沒有夠大的餅乾）
```

#### 範例 2：g = [1, 2], s = [1, 2, 3]

```
排序後: g = [1, 2], s = [1, 2, 3]

child=0, cookie=0: s[0]=1 >= g[0]=1？ YES → child=1, cookie=1
child=1, cookie=1: s[1]=2 >= g[1]=2？ YES → child=2, cookie=2
child=2 >= len(g)=2 → 結束

結果: 2 個小孩都被滿足 ✓（餅乾大小=3 的沒用到，但不影響）
```

---

### 4.2 Partition Labels — LeetCode 763

#### 問題描述

給一個字串 `s`，將它分割成盡可能多的部分（partitions），使得每個字母最多只出現在一個部分中。回傳每個部分的長度。

#### 核心思路

```
Greedy 策略：
  1. 先掃描一次，記錄每個字母「最後出現的位置」
  2. 再掃描一次：
     - 維護 current partition 的 end = max(end, last[char])
     - 當 i == end 時，這個 partition 結束，記錄長度

為什麼有效？
  如果字母 'a' 最後出現在 index 8，那包含 'a' 的 partition
  至少要延伸到 index 8。在 index 0~8 之間遇到的每個字母
  都可能把 end 推得更遠。當 i 追上 end 時，代表目前 partition
  裡的所有字母都不會再出現了，可以安全切割。
```

#### Pseudocode

```python
def partitionLabels(s):
    last = {}
    for i, ch in enumerate(s):
        last[ch] = i            # 記錄每個字母的最後位置

    result = []
    start = 0
    end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:            # 可以切割了
            result.append(end - start + 1)
            start = end + 1

    return result
```

**Time: O(n)**，**Space: O(1)**（最多 26 個字母）

#### 範例 1：s = "ababcbacadefegdehijhklij"

```
Step 1: 記錄每個字母的 last occurrence

  a: 8,  b: 5,  c: 7,  d: 14, e: 15
  f: 11, g: 13, h: 19, i: 22, j: 23
  k: 20, l: 21

Step 2: 掃描並分割

  index: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
  char:  a  b  a  b  c  b  a  c  a  d  e  f  e  g  d  e  h  i  j  h  k  l  i  j
  end:   8  5  8  5  7  5  8  7  8  14 15 11 15 13 14 15 19 22 23 19 20 21 22 23
                                     ↑                    ↑                       ↑
                                   i==end               i==end                  i==end

  i=0: ch='a', end=max(0,8)=8
  i=1: ch='b', end=max(8,5)=8
  i=2: ch='a', end=max(8,8)=8
  ...
  i=8: ch='a', end=8, i==end ✓ → partition 長度 = 8-0+1 = 9
       result = [9]

  i=9:  ch='d', end=max(9,14)=14, start=9
  i=10: ch='e', end=max(14,15)=15
  i=11: ch='f', end=max(15,11)=15
  i=12: ch='e', end=max(15,15)=15
  i=13: ch='g', end=max(15,13)=15
  i=14: ch='d', end=max(15,14)=15
  i=15: ch='e', end=15, i==end ✓ → partition 長度 = 15-9+1 = 7
       result = [9, 7]

  i=16: ch='h', end=max(16,19)=19, start=16
  i=17: ch='i', end=max(19,22)=22
  i=18: ch='j', end=max(22,23)=23
  i=19: ch='h', end=max(23,19)=23
  i=20: ch='k', end=max(23,20)=23
  i=21: ch='l', end=max(23,21)=23
  i=22: ch='i', end=max(23,22)=23
  i=23: ch='j', end=23, i==end ✓ → partition 長度 = 23-16+1 = 8
       result = [9, 7, 8]

結果: [9, 7, 8] ✓
分割: "ababcbaca" | "defegde" | "hijhklij"
```

#### 範例 2：s = "eccbbbbdec"

```
Step 1: last occurrence
  e: 9, c: 8, b: 6, d: 7

Step 2: 掃描

  index: 0  1  2  3  4  5  6  7  8  9
  char:  e  c  c  b  b  b  b  d  e  c
                                         ← 注意 'e' 和 'c' 在末尾出現

  i=0: ch='e', end=max(0,9)=9
  i=1: ch='c', end=max(9,8)=9
  ...
  i=9: ch='c', end=9, i==end ✓ → 長度 = 9-0+1 = 10

結果: [10] ✓（整個字串就是一個 partition，因為 'e' 橫跨整個字串）
```

---

## 第五章：數字/字串型 Greedy

### 5.1 Remove K Digits — LeetCode 402

#### 問題描述

給定一個代表非負整數的字串 `num` 和一個整數 `k`，移除 `k` 個數字，使得剩下的數字組成的整數最小。回傳結果字串。

#### 核心思路：Monotonic Stack + Greedy

```
直覺：
  為了讓結果最小，我們希望高位（左邊）的數字越小越好。
  所以：如果當前數字比前一個數字小，就把前一個刪掉。

Greedy 策略：
  用一個 stack（單調遞增棧）。
  對每個數字 d：
    while stack 不為空 AND stack 頂端 > d AND k > 0:
      pop stack（刪掉一個較大的數字）
      k--
    push d

  最後如果 k > 0（還沒刪夠），從 stack 尾端刪掉（最大的在尾端）。
  去除前導零。

為什麼用 stack？
  Stack 維護一個「遞增序列」。遇到更小的數字時，把前面較大的都彈出，
  這樣高位就變小了 → 結果更小。
```

#### Pseudocode

```python
def removeKdigits(num, k):
    stack = []
    for d in num:
        while stack and stack[-1] > d and k > 0:
            stack.pop()
            k -= 1
        stack.append(d)

    # 如果 k > 0，從尾端刪除
    while k > 0:
        stack.pop()
        k -= 1

    # 去除前導零，組合結果
    result = ''.join(stack).lstrip('0')
    return result if result else '0'
```

**Time: O(n)**，**Space: O(n)**

#### 範例 1：num = "1432219", k = 3

```
目標：刪 3 個數字，使結果最小

stack = [], k = 3

d='1': stack=[] → push
  stack = ['1']

d='4': stack[-1]='1' < '4' → 不 pop, push
  stack = ['1','4']

d='3': stack[-1]='4' > '3' AND k=3 > 0 → pop '4', k=2
  stack = ['1']
  stack[-1]='1' < '3' → 不 pop, push
  stack = ['1','3']

d='2': stack[-1]='3' > '2' AND k=2 > 0 → pop '3', k=1
  stack = ['1']
  stack[-1]='1' < '2' → 不 pop, push
  stack = ['1','2']

d='2': stack[-1]='2' == '2' → 不 pop, push
  stack = ['1','2','2']

d='1': stack[-1]='2' > '1' AND k=1 > 0 → pop '2', k=0
  stack = ['1','2']
  k=0 → 不再 pop, push
  stack = ['1','2','1']

d='9': stack[-1]='1' < '9' → 不 pop, push
  stack = ['1','2','1','9']

k=0，不需要從尾端再刪。

結果: "1219" ✓

過程視覺化:
  原始:   1 4 3 2 2 1 9
  刪 '4': 1 _ 3 2 2 1 9   (4 > 3, 刪 4)
  刪 '3': 1 _ _ 2 2 1 9   (3 > 2, 刪 3)
  刪 '2': 1 _ _ 2 _ 1 9   (第二個 2 > 1, 刪掉)
  結果:   1 2 1 9
```

#### 範例 2：num = "10200", k = 1

```
stack = [], k = 1

d='1': push → stack = ['1']
d='0': stack[-1]='1' > '0' AND k=1 > 0 → pop '1', k=0
  stack = []
  push → stack = ['0']
d='2': push → stack = ['0','2']
d='0': stack[-1]='2' > '0' BUT k=0 → 不 pop, push
  stack = ['0','2','0']
d='0': push → stack = ['0','2','0','0']

k=0，不再刪。

''.join(stack) = "0200"
lstrip('0') = "200"

結果: "200" ✓

注意：lstrip('0') 去掉了前導零。
如果結果是空字串（例如 num="10", k=2），回傳 "0"。
```

---

### 5.2 Task Scheduler — LeetCode 621

#### 問題描述

有一組任務（用字母表示），每個任務需要 1 單位時間執行。相同任務之間必須有至少 `n` 個時間單位的冷卻間隔（可以執行其他任務或 idle）。求完成所有任務需要的最少時間。

#### 核心思路：Idle Slots 公式

```
關鍵觀察：
  頻率最高的任務決定了最短的時間框架。

假設最高頻率的任務是 A，出現 max_freq 次。
把 A 排在框架的「固定位置」上：

  A _ _ _ A _ _ _ A
  |←n+1→| |←n+1→|

每兩個 A 之間有 n 個空位（cooldown），所以每個區塊的大小是 n+1。
有 max_freq 個 A，所以有 max_freq - 1 個「間隔區塊」。

框架: (max_freq - 1) × (n + 1) + count_of_max_freq_tasks

最後一個區塊不需要 cooldown，只需要放所有出現 max_freq 次的任務。

但如果任務很多，空位不夠放怎麼辦？
  那就不需要任何 idle，答案 = 任務總數（tasks 夠多就能填滿所有空位）。

公式:
  answer = max(len(tasks), (max_freq - 1) × (n + 1) + count_of_max_freq)
```

#### Pseudocode

```python
from collections import Counter

def leastInterval(tasks, n):
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_max = sum(1 for v in freq.values() if v == max_freq)

    result = (max_freq - 1) * (n + 1) + count_max
    return max(result, len(tasks))
```

**Time: O(n)**，**Space: O(1)**（最多 26 個字母）

#### 範例 1：tasks = ["A","A","A","B","B","B"], n = 2

```
頻率統計: A=3, B=3
max_freq = 3
count_max = 2 (A 和 B 都出現 3 次)

公式計算:
  result = (3-1) × (2+1) + 2 = 2 × 3 + 2 = 8
  len(tasks) = 6
  answer = max(8, 6) = 8

排程圖:
  slot:  1  2  3  4  5  6  7  8
  task:  A  B  _  A  B  _  A  B
         ↑     ↑  ↑     ↑  ↑
         A間隔2  A間隔2  最後

  區塊 1: [A, B, _]    (大小 n+1=3)
  區塊 2: [A, B, _]    (大小 n+1=3)
  最後:   [A, B]       (只有 count_max=2 個任務)

  總共: 3 + 3 + 2 = 8 ✓

  框架拆解:
  (max_freq - 1) = 2 個間隔區塊 × (n+1) = 3 每區塊 = 6
  + count_max = 2（最後一個區塊有 A 和 B）
  = 8
```

#### 範例 2：tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2

```
頻率統計: A=6, B=1, C=1, D=1, E=1, F=1, G=1
max_freq = 6
count_max = 1 (只有 A 出現 6 次)

公式計算:
  result = (6-1) × (2+1) + 1 = 5 × 3 + 1 = 16
  len(tasks) = 12
  answer = max(16, 12) = 16

排程圖:
  slot:  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
  task:  A  B  C  A  D  E  A  F  G  A  _  _  A  _  _  A
         ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑        ↑        ↑

  區塊 1: [A, B, C]
  區塊 2: [A, D, E]
  區塊 3: [A, F, G]
  區塊 4: [A, _, _]   ← 沒有其他任務了，必須 idle
  區塊 5: [A, _, _]   ← 同上
  最後:   [A]

  B~G 共 6 個不同任務填了前 3 個區塊的空位，
  後 2 個區塊沒任務可填，只能 idle。

  驗證: 5 × 3 + 1 = 16 ✓
```

#### 範例 3（不需要 idle 的情況）：tasks = ["A","A","A","B","B","B","C","C","C","D","D","E"], n = 2

```
頻率統計: A=3, B=3, C=3, D=2, E=1
max_freq = 3
count_max = 3 (A, B, C 都出現 3 次)

公式計算:
  result = (3-1) × (2+1) + 3 = 2 × 3 + 3 = 9
  len(tasks) = 12
  answer = max(9, 12) = 12  ← 任務總數更大！

排程圖:
  slot:  1  2  3  4  5  6  7  8  9  10 11 12
  task:  A  B  C  D  A  B  C  D  A  B  C  E

  完全不需要 idle！任務多到可以把所有空隙都填滿。
  答案就是任務總數 12 ✓
```

---

## 第六章：Greedy vs DP — 什麼時候用哪個？

### 6.1 核心判斷原則

```
Greedy 的特徵:
  ✓ 每一步做出「局部最佳」選擇，不回頭
  ✓ 選擇之間相對獨立（或可以用排序消除依賴）
  ✓ 通常 O(n) 或 O(n log n)
  ✓ 實作簡潔

DP 的特徵:
  ✓ 需要考慮「所有可能的子問題組合」
  ✓ 選擇之間有複雜的依賴關係
  ✓ 通常 O(n^2) 或更高
  ✓ 需要記憶化（memoization）或表格（tabulation）

判斷方法:
  1. 先想 Greedy：能不能找到一個排序/比較規則，使得每步局部最佳 = 全域最佳？
  2. 找反例：能不能找到一個 counterexample 讓 Greedy 失敗？
  3. 如果找不到反例 → 大概可以 Greedy
  4. 如果找到反例 → 必須用 DP（或其他方法）
```

### 6.2 經典問題分類比較表

```
┌──────────────────────────┬──────────┬──────────┬────────────────────────────┐
│ 問題                      │ Greedy?  │ DP?      │ 為什麼？                    │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Activity Selection        │ ✓        │ 也可以   │ 排序+選最早結束的 → 最優    │
│ (活動選擇)                │ O(nlogn) │ O(n^2)   │ Greedy choice property 成立│
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Coin Change               │ 有時候   │ ✓        │ 標準面額可以 Greedy         │
│ (硬幣找零)                │          │ O(n*k)   │ 非標準面額必須 DP           │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Jump Game                 │ ✓        │ 也可以   │ 只需追蹤 max_reach          │
│ (跳躍遊戲)                │ O(n)     │ O(n^2)   │ 不需要知道路徑              │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Jump Game II              │ ✓        │ 也可以   │ BFS-like 分層即可           │
│ (最少跳躍)                │ O(n)     │ O(n^2)   │                            │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ 0/1 Knapsack              │ ✗        │ ✓        │ 物品不能分割，Greedy 失敗   │
│ (0/1 背包)                │          │ O(nW)    │ 必須考慮所有取/不取組合     │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Fractional Knapsack       │ ✓        │ 不需要   │ 物品可以分割 → 按 CP 值排序 │
│ (分數背包)                │ O(nlogn) │          │ Greedy choice property 成立│
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Longest Increasing Subseq │ ✗        │ ✓        │ 不能只看局部，需要全域資訊  │
│ (最長遞增子序列)           │          │ O(nlogn) │ （二分搜尋優化版也用到      │
│                          │          │          │  Greedy 思想但本質是 DP）   │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Merge Intervals           │ ✓        │ 不需要   │ 排序後線性掃描              │
│ (合併區間)                │ O(nlogn) │          │                            │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Task Scheduler            │ ✓        │ 也可以   │ 公式直接算                  │
│ (任務排程)                │ O(n)     │          │                            │
├──────────────────────────┼──────────┼──────────┼────────────────────────────┤
│ Edit Distance             │ ✗        │ ✓        │ 三種操作的最佳組合          │
│ (編輯距離)                │          │ O(mn)    │ 無法用局部最佳推導          │
└──────────────────────────┴──────────┴──────────┴────────────────────────────┘
```

### 6.3 面試中的判斷流程

```
面試官問你一個優化問題：

Step 1: 問自己 — 能排序嗎？排序後有什麼性質？
  → 如果排序後可以「每步選最小/最大/最早結束」→ 試 Greedy

Step 2: 找反例
  → 想 2-3 個 edge case，看 Greedy 結果對不對
  → 如果找到反例 → 放棄 Greedy，改用 DP

Step 3: 如果確定 Greedy 有效，跟面試官解釋
  → "I believe greedy works here because of the greedy choice property:
      choosing the [earliest ending / smallest / etc.] never blocks
      a better solution."
  → 不需要嚴格數學證明，但要能用直覺解釋

Step 4: 如果不確定，問面試官
  → "I'm considering both greedy and DP approaches. Let me think about
      whether greedy is sufficient here..."
  → 面試官通常會引導你
```

### 6.4 本章所有題目的 LeetCode 題號速查

```
┌───────────────────────────┬──────┬────────┬──────────────┬──────────────┐
│ 題目                       │ 題號  │ 難度   │ Greedy 類型   │ Google 頻率  │
├───────────────────────────┼──────┼────────┼──────────────┼──────────────┤
│ Merge Intervals            │ 56   │ Medium │ 區間排序      │ 非常高       │
│ Non-overlapping Intervals  │ 435  │ Medium │ 區間(按end)   │ 高           │
│ Meeting Rooms II           │ 253  │ Medium │ 區間+Heap     │ 非常高       │
│ Jump Game                  │ 55   │ Medium │ 跳躍型        │ 高           │
│ Jump Game II               │ 45   │ Medium │ 跳躍型(BFS)   │ 高           │
│ Gas Station                │ 134  │ Medium │ 累積平衡      │ 中           │
│ Assign Cookies             │ 455  │ Easy   │ 分配型        │ 低           │
│ Partition Labels           │ 763  │ Medium │ 分配型        │ 高           │
│ Remove K Digits            │ 402  │ Medium │ 單調棧+Greedy │ 高           │
│ Task Scheduler             │ 621  │ Medium │ 數學+Greedy   │ 非常高       │
└───────────────────────────┴──────┴────────┴──────────────┴──────────────┘
```

### 6.5 常見錯誤與避免方式

```
錯誤 1: Non-overlapping Intervals 按 start 排序
  → 必須按 end 排序！按 start 排序會被超長區間誤導。
  → 記憶法：「結束早的留更多空間」

錯誤 2: Jump Game II 迴圈跑到最後一個 index
  → 應該是 range(len(nums) - 1)，不處理最後一個 index
  → 因為到了最後就不需要再跳了，多跳一次會多算

錯誤 3: Gas Station 忘記檢查 sum(gas) >= sum(cost)
  → 如果總油量不夠，不管從哪裡出發都不行
  → 先做這個全域檢查，再找起點

錯誤 4: Remove K Digits 忘記處理前導零
  → "10200" 刪除 '1' 後變成 "0200"，要 lstrip('0')
  → 結果為空時要回傳 "0" 而不是 ""

錯誤 5: Task Scheduler 公式忘記跟 len(tasks) 取 max
  → 當任務種類很多時，不需要 idle，答案就是 len(tasks)
  → answer = max(公式結果, 任務總數)

錯誤 6: Partition Labels 只看第一次出現而非最後一次
  → 必須看每個字母的「最後出現位置」
  → 因為 partition 必須包含該字母的所有出現
```

---

> **下一章預告**：`15_Heap_Priority_Queue_教學.md` — 堆積與優先佇列，
> 在 Greedy 問題中經常搭配使用（如 Meeting Rooms II 的 min-heap）。
> Greedy 負責決策邏輯，Heap 負責高效地找到「最佳候選者」。
