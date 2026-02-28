# Backtracking 回溯法 完全教學手冊

> **適用對象**：基礎較弱、準備 Google 面試的工程師
> **教學風格**：大學教科書等級，每個觀念都有 2+ 組完整數值追蹤，附完整 decision tree
> **語言**：繁體中文解說 + English technical terms
> **配套程式**：`13_Backtracking.py`（可直接執行驗證所有範例）

---

## 第一章：回溯法核心概念 -- 用迷宮來理解

### 1.1 什麼是 Backtracking？

**一句話定義**：Backtracking = DFS + undo choice（深度優先搜尋 + 撤銷選擇）

想像你站在一座迷宮的入口：

```
┌───────────────────────────────────────┐
│  START                                │
│  ↓                                    │
│  ○ ─── 岔路 1 ─── 死路 ✗             │
│  │                                    │
│  │     退回 (backtrack!)              │
│  │                                    │
│  ○ ─── 岔路 2 ─── 又一個岔路          │
│                     │                 │
│               岔路 2a ── 死路 ✗        │
│                     │                 │
│               退回! │                 │
│                     │                 │
│               岔路 2b ── EXIT ✓       │
└───────────────────────────────────────┘
```

你的策略：
1. 走到岔路口 → **選一個方向走**（make choice）
2. 走到死路 → **退回上一個岔路口**（backtrack / undo choice）
3. 換另一個方向走 → **繼續探索**（try next choice）
4. 找到出口 → **記錄這條路徑**（save to result）

**這就是 Backtracking 的全部！** 它不是什麼高深的演算法，就是「有系統地嘗試所有可能，走不通就回頭」。

### 1.2 萬用模板 (Universal Template)

所有回溯問題都能套用這個模板：

```python
def backtrack(path, choices):
    # Base case: 達成目標
    if goal_reached:
        result.append(path[:])   # 注意：一定要複製 path！
        return

    for choice in choices:
        if choice is valid:          # 剪枝 (pruning)
            path.append(choice)      # 1. 做選擇 (add to path)
            backtrack(path, new_choices)  # 2. 遞迴探索
            path.pop()               # 3. 撤銷選擇 (remove from path)
                                     #    ↑↑↑ THIS IS THE KEY! ↑↑↑
```

**為什麼要 `path[:]` 而不是直接 `path`？**

```
Python 裡 list 是 reference type。如果你寫 result.append(path)，
你存的是 path 的「記憶體位址」，不是它當下的內容。
之後 path 被改動（pop、append），result 裡的值也會跟著變。

path[:]  = 複製一份新的 list（shallow copy）
list(path) = 同樣效果
path.copy() = 同樣效果
```

### 1.3 時間複雜度概覽

```
┌──────────────────────┬───────────────┬──────────────────────┐
│  問題類型              │ 時間複雜度      │ 說明                  │
├──────────────────────┼───────────────┼──────────────────────┤
│ Subsets (子集)         │ O(2^n)        │ 每個元素選或不選        │
│ Permutations (排列)   │ O(n!)         │ n 個位置，第 i 位有     │
│                      │               │ n-i 個選擇             │
│ Combinations C(n,k)  │ O(C(n,k))     │ 從 n 選 k             │
│ N-Queens             │ O(n!)         │ 每行放一個，逐行剪枝    │
└──────────────────────┴───────────────┴──────────────────────┘
```

Backtracking 的時間複雜度通常是指數級或階乘級，這是因為我們在嘗試所有可能。
**剪枝（Pruning）** 可以大幅減少實際搜尋量，但最壞情況不變。

### 1.4 回溯法的三個關鍵問題

面對任何回溯題目，你要回答三個問題：

```
Q1: path 是什麼？           → 目前已做的選擇序列
Q2: choices 有哪些？        → 在這一步，還有哪些選項可選
Q3: base case 是什麼？      → 什麼時候停止遞迴、收集答案
```

把這三個問題回答清楚，程式碼幾乎就寫出來了。

---

## 第二章：子集型 (Subsets)

### 2.1 Subsets -- LeetCode 78

#### 問題描述

給定一個**不含重複元素**的整數陣列 `nums`，回傳其所有子集（冪集合，power set）。結果中不可有重複子集。

#### 核心思路

對於 `nums` 中的每個元素，只有兩種選擇：**選它**（include）或**不選它**（exclude）。
我們用 `start` index 來避免走回頭路（確保每個子集裡的元素是按原陣列順序排列的）。

```
三個關鍵問題：
  Q1: path = 目前選中的元素
  Q2: choices = nums[start], nums[start+1], ..., nums[n-1]
  Q3: base case = 每個節點都是合法子集，走到 start==n 就停
```

#### Decision Tree for nums = [1, 2, 3] -- 完整展開

```
backtrack(start=0, path=[])
│
├── 選 1: backtrack(start=1, path=[1])
│   │
│   ├── 選 2: backtrack(start=2, path=[1,2])
│   │   │
│   │   ├── 選 3: backtrack(start=3, path=[1,2,3])
│   │   │         start=3 == len(nums) → 收集 [1,2,3] ✓
│   │   │         (其實不需要等到底，每個節點都收集)
│   │   │
│   │   └── 不選 3 (for loop 結束): 收集 [1,2] ✓
│   │
│   ├── 選 3: backtrack(start=3, path=[1,3])
│   │         收集 [1,3] ✓
│   │
│   └── 不選 2,3 (for loop 結束): 收集 [1] ✓
│
├── 選 2: backtrack(start=2, path=[2])
│   │
│   ├── 選 3: backtrack(start=3, path=[2,3])
│   │         收集 [2,3] ✓
│   │
│   └── 不選 3: 收集 [2] ✓
│
├── 選 3: backtrack(start=3, path=[3])
│         收集 [3] ✓
│
└── 不選任何 (初始): 收集 [] ✓

結果: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
共 2^3 = 8 個子集
```

**另一種理解方式**（include/exclude 二元決策樹）：

```
                                  []
                          /               \
                     include 1          exclude 1
                       [1]                 []
                    /       \           /       \
               include 2  exclude 2 include 2  exclude 2
                [1,2]      [1]       [2]        []
               /    \     /   \     /   \      /   \
             +3    skip  +3   skip +3   skip  +3   skip
           [1,2,3] [1,2] [1,3] [1] [2,3] [2]  [3]  []
```

兩棵樹產生的結果一模一樣，只是遍歷順序不同。面試中用第一種（for loop + start）比較好寫。

#### Pseudocode

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])     # 每個節點都是合法子集

        for i in range(start, len(nums)):
            path.append(nums[i])        # 做選擇
            backtrack(i + 1, path)       # 遞迴（i+1 確保不走回頭路）
            path.pop()                   # 撤銷選擇

    backtrack(0, [])
    return result
```

#### 範例 1：nums = [1, 2, 3] -- 逐步追蹤

```
backtrack(0,[])   → 收集 []
  i=0: append 1 → backtrack(1,[1]) → 收集 [1]
    i=1: append 2 → backtrack(2,[1,2]) → 收集 [1,2]
      i=2: append 3 → backtrack(3,[1,2,3]) → 收集 [1,2,3], return
      pop→[1,2]
    pop→[1]
    i=2: append 3 → backtrack(3,[1,3]) → 收集 [1,3], return
    pop→[1]
  pop→[]
  i=1: append 2 → backtrack(2,[2]) → 收集 [2]
    i=2: append 3 → backtrack(3,[2,3]) → 收集 [2,3], return
    pop→[2]
  pop→[]
  i=2: append 3 → backtrack(3,[3]) → 收集 [3], return
  pop→[]

最終 result = [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

#### 範例 2：nums = [0, 1] -- 更簡單的例子建立直覺

```
Decision Tree:
                []
              /    \
            [0]     []
           /   \      \
        [0,1]  [0]   [1]    []
                        (已收集過)

逐步追蹤：
  backtrack(0, [])
    → 收集 []

    i=0: path=[0], backtrack(1, [0])
      → 收集 [0]
      i=1: path=[0,1], backtrack(2, [0,1])
        → 收集 [0,1]
        return
      pop → path=[0]
      return
    pop → path=[]

    i=1: path=[1], backtrack(2, [1])
      → 收集 [1]
      return
    pop → path=[]

result = [[], [0], [0,1], [1]]
共 2^2 = 4 個子集 ✓
```

#### 複雜度分析

```
時間: O(n * 2^n)
  - 共 2^n 個子集
  - 每個子集平均長度 n/2，複製需 O(n/2)
  - 總計 O(n * 2^n)

空間: O(n)（遞迴深度 = n）
```

---

### 2.2 Subsets II -- LeetCode 90（含重複元素）

#### 問題描述

給定一個**可能包含重複元素**的整數陣列 `nums`，回傳所有不重複的子集。

#### 核心思路

跟 LC 78 相比，多了一個去重步驟：

```
KEY: 先排序 (sort)，然後在同一層的 for loop 中：
     如果 nums[i] == nums[i-1] 且 i > start → 跳過！

為什麼 i > start？
  → i == start 時是「這一層的第一個選擇」，不能跳過
  → i > start 時代表「同一層已經用過相同的值」，必須跳過

為什麼要排序？
  → 排序後相同的值會相鄰，才能用 nums[i]==nums[i-1] 偵測重複
```

#### Pseudocode

```python
def subsetsWithDup(nums):
    nums.sort()              # 關鍵！先排序
    result = []

    def backtrack(start, path):
        result.append(path[:])

        for i in range(start, len(nums)):
            # 去重：同一層中，跳過跟前一個相同的值
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

#### 範例 1：nums = [1, 2, 2] -- 展示哪些分支被剪枝

```
排序後: [1, 2, 2]

Decision Tree（✗ 表示被剪枝）:

backtrack(0, [])
│
├── i=0, pick 1: backtrack(1, [1])
│   │
│   ├── i=1, pick 2: backtrack(2, [1,2])
│   │   │
│   │   ├── i=2, pick 2: backtrack(3, [1,2,2])
│   │   │         收集 [1,2,2] ✓
│   │   │
│   │   └── 收集 [1,2] ✓
│   │
│   ├── i=2, pick 2: i>start(1) 且 nums[2]==nums[1] → SKIP ✗
│   │       （如果不跳過，會重複產生 [1,2]）
│   │
│   └── 收集 [1] ✓
│
├── i=1, pick 2: backtrack(2, [2])
│   │
│   ├── i=2, pick 2: backtrack(3, [2,2])
│   │         收集 [2,2] ✓
│   │
│   └── 收集 [2] ✓
│
├── i=2, pick 2: i>start(0) 且 nums[2]==nums[1] → SKIP ✗
│       （如果不跳過，會重複產生 [2]）
│
└── 收集 [] ✓

result = [[], [1], [1,2], [1,2,2], [2], [2,2]]
共 6 個子集 ✓
```

**對比不剪枝的情況**：如果不 skip，i=2 的 pick 2 會產生重複的 [2]、[1,2] 等。

#### 範例 2：nums = [1, 1, 1] -- 極端重複案例

```
排序後: [1, 1, 1]

Decision Tree:

backtrack(0, [])
│
├── i=0, pick 1: backtrack(1, [1])
│   │
│   ├── i=1, pick 1: backtrack(2, [1,1])
│   │   │
│   │   ├── i=2, pick 1: backtrack(3, [1,1,1])
│   │   │         收集 [1,1,1] ✓
│   │   │
│   │   └── 收集 [1,1] ✓
│   │
│   ├── i=2, pick 1: i>1 且 nums[2]==nums[1] → SKIP ✗
│   │
│   └── 收集 [1] ✓
│
├── i=1, pick 1: i>0 且 nums[1]==nums[0] → SKIP ✗
│
├── i=2, pick 1: i>0 且 nums[2]==nums[1] → SKIP ✗
│
└── 收集 [] ✓

result = [[], [1], [1,1], [1,1,1]]
共 4 個子集 ✓

注意：3 個相同元素只會產生 4 個子集（選 0 個、1 個、2 個、3 個），
      而非 2^3 = 8 個。大量重複被剪枝掉了！
```

---

## 第三章：排列型 (Permutations)

### 3.1 Permutations -- LeetCode 46

#### 問題描述

給定一個**不含重複數字**的陣列 `nums`，回傳其所有可能的排列。

#### 核心思路

排列跟子集最大的不同：**順序很重要**。[1,2] 和 [2,1] 是不同的排列。

```
子集: 用 start index 確保往前走，不回頭
排列: 用 used[] boolean 陣列，標記哪些元素已經用過

三個關鍵問題：
  Q1: path = 目前的排列序列
  Q2: choices = 所有 used[i]==False 的元素
  Q3: base case = len(path) == len(nums) → 排列完成
```

#### Pseudocode

```python
def permute(nums):
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue          # 已經用過，跳過
            used[i] = True            # 標記為已用
            path.append(nums[i])      # 做選擇
            backtrack(path)           # 遞迴
            path.pop()                # 撤銷選擇
            used[i] = False           # 取消標記

    backtrack([])
    return result
```

#### Decision Tree for nums = [1, 2, 3] -- 完整 6 個排列

```
backtrack(path=[])
├── pick 1 (used=[T,F,F])
│   ├── pick 2 (used=[T,T,F])
│   │   └── pick 3 (used=[T,T,T])
│   │       path=[1,2,3] → 收集 ✓
│   │       undo 3, used=[T,T,F]
│   └── pick 3 (used=[T,F,T])
│       └── pick 2 (used=[T,T,T])
│           path=[1,3,2] → 收集 ✓
│           undo 2, used=[T,F,T]
│       undo 3, used=[T,F,F]
│   undo 1, used=[F,F,F]
│
├── pick 2 (used=[F,T,F])
│   ├── pick 1 (used=[T,T,F])
│   │   └── pick 3 (used=[T,T,T])
│   │       path=[2,1,3] → 收集 ✓
│   └── pick 3 (used=[F,T,T])
│       └── pick 1 (used=[T,T,T])
│           path=[2,3,1] → 收集 ✓
│
└── pick 3 (used=[F,F,T])
    ├── pick 1 (used=[T,F,T])
    │   └── pick 2 (used=[T,T,T])
    │       path=[3,1,2] → 收集 ✓
    └── pick 2 (used=[F,T,T])
        └── pick 1 (used=[T,T,T])
            path=[3,2,1] → 收集 ✓

result = [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
共 3! = 6 個排列 ✓
```

#### 範例 1：nums = [1, 2, 3] -- 逐步追蹤

```
path=[], used=[F,F,F]
  pick 1 → [1], [T,F,F]
    pick 2 → [1,2], [T,T,F]
      pick 3 → [1,2,3] ✓, pop→[1,2]
    pop→[1]
    pick 3 → [1,3], [T,F,T]
      pick 2 → [1,3,2] ✓, pop→[1,3]
    pop→[1]
  pop→[]
  pick 2 → [2], [F,T,F]
    pick 1 → [2,1] → pick 3 → [2,1,3] ✓
    pick 3 → [2,3] → pick 1 → [2,3,1] ✓
  pop→[]
  pick 3 → [3], [F,F,T]
    pick 1 → [3,1] → pick 2 → [3,1,2] ✓
    pick 2 → [3,2] → pick 1 → [3,2,1] ✓

result = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

#### 範例 2：nums = [0, 1] -- 更簡單的例子

```
Decision Tree:
  backtrack(path=[])
  ├── pick 0: backtrack(path=[0])
  │   └── pick 1: path=[0,1] → 收集 ✓
  └── pick 1: backtrack(path=[1])
      └── pick 0: path=[1,0] → 收集 ✓

result = [[0,1], [1,0]]
共 2! = 2 個排列 ✓
```

---

### 3.2 Permutations II -- LeetCode 47（含重複元素）

#### 問題描述

給定一個**可能包含重複數字**的陣列 `nums`，回傳所有不重複的排列。

#### 核心思路

跟 LC 46 一樣用 `used[]` 陣列，但多一個剪枝條件：

```
剪枝條件：
  if nums[i] == nums[i-1] and not used[i-1]:
      continue

意思：如果前一個相同的數字「沒被用」（在同一層被撤銷了），
      那現在用這個相同的數字就會產生重複排列，所以跳過。

為什麼是 not used[i-1]？
  → used[i-1] == True：前一個在「更上層」被選了，現在選 nums[i] 不會重複
  → used[i-1] == False：前一個在「同一層」剛被撤銷，現在選 nums[i] 會重複

前提：必須先排序，讓相同的數字相鄰！
```

#### Pseudocode

```python
def permuteUnique(nums):
    nums.sort()             # 關鍵！先排序
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue
            # 去重：同一層中，跳過跟前一個相同且前一個未使用的
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result
```

#### 範例 1：nums = [1, 1, 2] -- 展示哪些分支被剪枝

```
排序後: [1, 1, 2]  (index: 0=1, 1=1, 2=2)

Decision Tree（✗ = 被剪枝）:

backtrack(path=[])
│
├── i=0, pick nums[0]=1, used=[T,F,F]
│   │
│   ├── i=1, pick nums[1]=1, used=[T,T,F]
│   │   │
│   │   └── i=2, pick nums[2]=2
│   │       path=[1,1,2] → 收集 ✓
│   │
│   └── i=2, pick nums[2]=2, used=[T,F,T]
│       │
│       └── i=1, pick nums[1]=1
│           path=[1,2,1] → 收集 ✓
│
├── i=1, pick nums[1]=1:
│   nums[1]==nums[0] 且 !used[0] → SKIP ✗
│   （如果不跳過，會產生跟 i=0 完全一樣的排列 [1,1,2] 和 [1,2,1]）
│
└── i=2, pick nums[2]=2, used=[F,F,T]
    │
    ├── i=0, pick nums[0]=1, used=[T,F,T]
    │   │
    │   └── i=1, pick nums[1]=1
    │       path=[2,1,1] → 收集 ✓
    │
    └── i=1, pick nums[1]=1:
        nums[1]==nums[0] 且 !used[0] → SKIP ✗

result = [[1,1,2], [1,2,1], [2,1,1]]
共 3!/2! = 3 個不重複排列 ✓

（若無去重會產生 6 個排列，其中每對都重複一次）
```

#### 關鍵理解：為什麼 `not used[i-1]` 能去重？

```
以 [1a, 1b, 2] 為例（1a 和 1b 值相同但用 a、b 區分）：

約定：相同的值，一定先用前面的（1a），再用後面的（1b）。

!used[i-1] = True（1a 沒被用）→ 1a 在同一層已試過又撤銷了
  → 現在用 1b 會產生一模一樣的子樹 → 跳過！

!used[i-1] = False（1a 正被用）→ 符合「先 1a 再 1b」→ 允許
```

---

## 第四章：組合型 (Combinations)

### 4.1 Combinations C(n, k) -- LeetCode 77

#### 問題描述

給定兩個整數 `n` 和 `k`，回傳 `[1, n]` 中所有大小為 `k` 的組合。

#### 核心思路

跟 Subsets 非常像，但多了一個限制：**只在 len(path) == k 時收集**。

```
三個關鍵問題：
  Q1: path = 目前選中的數字
  Q2: choices = start, start+1, ..., n
  Q3: base case = len(path) == k → 收集

剪枝優化：
  如果「剩餘可選的數字」< 「還需要的數字」，直接 return。
  具體: if n - i + 1 < k - len(path): break
  (剩餘 n-i+1 個數，需要 k-len(path) 個)
```

#### Pseudocode

```python
def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return

        # 剪枝：剩餘不夠選的就不用繼續了
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):  # 剪枝
                break
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

#### 範例 1：n=4, k=2 -- 完整 Decision Tree

```
backtrack(1, [])
│
├── pick 1: backtrack(2, [1])
│   ├── pick 2: path=[1,2], len==k → 收集 [1,2] ✓
│   ├── pick 3: path=[1,3], len==k → 收集 [1,3] ✓
│   └── pick 4: path=[1,4], len==k → 收集 [1,4] ✓
│
├── pick 2: backtrack(3, [2])
│   ├── pick 3: path=[2,3] → 收集 [2,3] ✓
│   └── pick 4: path=[2,4] → 收集 [2,4] ✓
│
├── pick 3: backtrack(4, [3])
│   └── pick 4: path=[3,4] → 收集 [3,4] ✓
│
└── pick 4: backtrack(5, [4])
    需要再選 1 個，但 start=5 > n=4，沒得選 → return
    （剪枝：n-4+1=1 < k-len(path)=2-1=1？不是，是 1==1，不剪。
      但 for loop range(5,5) 是空的，自然結束）

result = [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
共 C(4,2) = 6 個 ✓
```

#### 範例 2：n=5, k=3 -- 展示剪枝效果

```
backtrack(1, [])
├── pick 1 → pick 2 → pick {3,4,5}: [1,2,3] [1,2,4] [1,2,5] ✓
│          → pick 3 → pick {4,5}:   [1,3,4] [1,3,5] ✓
│          → pick 4 → pick 5:       [1,4,5] ✓
│          → pick 5: 需要 2 個但只剩 0 個 → 剪枝 ✗
├── pick 2 → [2,3,4] [2,3,5] [2,4,5] ✓
├── pick 3 → [3,4,5] ✓
├── pick 4: 需要 3 個但只剩 2 個 → 剪枝 ✗
└── pick 5: 需要 3 個但只剩 1 個 → 剪枝 ✗

result = [[1,2,3],[1,2,4],[1,2,5],[1,3,4],[1,3,5],[1,4,5],
          [2,3,4],[2,3,5],[2,4,5],[3,4,5]]
共 C(5,3) = 10 個 ✓
```

---

### 4.2 Combination Sum -- LeetCode 39（可重複使用元素）

#### 問題描述

給定不含重複元素的正整數陣列 `candidates` 和目標值 `target`，找出所有和等於 `target` 的組合。**同一個數字可以被重複選取**。

#### 核心思路

```
跟子集的差異：
  子集:            backtrack(i+1, path) → 每個元素最多用一次
  Combination Sum: backtrack(i, path)   → 同一個元素可以重複用（start 不加 1）

三個關鍵問題：
  Q1: path = 目前選的數字
  Q2: choices = candidates[start], candidates[start+1], ...
  Q3: base case = sum(path) == target → 收集
               or sum(path) > target → 剪枝 return
```

#### Pseudocode

```python
def combinationSum(candidates, target):
    candidates.sort()     # 排序有助於剪枝
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:    # 剪枝：後面更大，都不用試了
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i 不是 i+1！
            path.pop()

    backtrack(0, [], target)
    return result
```

#### 範例 1：candidates = [2, 3, 6, 7], target = 7

```
backtrack(0, [], remaining=7)
│
├── +2: remaining=5
│   ├── +2: remaining=3
│   │   ├── +2: remaining=1 → 2>1 break ✗
│   │   └── +3: remaining=0 → 收集 [2,2,3] ✓
│   │   (6>3 break)
│   ├── +3: remaining=2 → 3>2 break ✗
│   (6>5 break)
│
├── +3: remaining=4
│   ├── +3: remaining=1 → 3>1 break ✗
│   (6>4 break)
│
├── +6: remaining=1 → 6>1 break ✗
│
└── +7: remaining=0 → 收集 [7] ✓

result = [[2,2,3], [7]]
```

#### 範例 2：candidates = [2, 3, 5], target = 8

```
backtrack(0, [], remaining=8)
├── +2 → +2 → +2 → +2: remaining=0 → 收集 [2,2,2,2] ✓
├── +2 → +3 → +3: remaining=0 → 收集 [2,3,3] ✓
├── +3 → +5: remaining=0 → 收集 [3,5] ✓
└── (所有其他路徑在剪枝 candidates[i]>remaining 處終止)

result = [[2,2,2,2], [2,3,3], [3,5]]
```

---

### 4.3 Combination Sum II -- LeetCode 40（不可重複，但有重複元素）

#### 問題描述

給定一個可能含有重複元素的正整數陣列 `candidates` 和目標值 `target`，找出所有和等於 `target` 的組合。**每個數字只能用一次**。

#### 核心思路

```
跟 LC 39 的差異：
  LC 39: 無重複元素，可重複使用 → backtrack(i, ...)
  LC 40: 有重複元素，不可重複使用 → backtrack(i+1, ...) + 去重

去重邏輯跟 Subsets II (LC 90) 完全一樣：
  排序後，if i > start and candidates[i] == candidates[i-1]: continue
```

#### Pseudocode

```python
def combinationSum2(candidates, target):
    candidates.sort()     # 排序！
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:     # 剪枝
                break
            if i > start and candidates[i] == candidates[i - 1]:  # 去重
                continue
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # i+1!
            path.pop()

    backtrack(0, [], target)
    return result
```

#### 範例 1：candidates = [10, 1, 2, 7, 6, 1, 5], target = 8

```
排序後: [1, 1, 2, 5, 6, 7, 10]

backtrack(0, [], 8)
├── +1(i=0): remaining=7
│   ├── +1(i=1): remaining=6
│   │   ├── +2: remaining=4 → 5>4 break
│   │   └── +6(i=4): remaining=0 → 收集 [1,1,6] ✓
│   ├── +2(i=2): remaining=5 → +5: remaining=0 → 收集 [1,2,5] ✓
│   ├── +5(i=3): remaining=2 → 6>2 break
│   └── +7(i=5): remaining=0 → 收集 [1,7] ✓
│
├── +1(i=1): i>0 且 ==前一個 → SKIP ✗（去重）
│
├── +2(i=2): remaining=6 → +6: remaining=0 → 收集 [2,6] ✓
│
└── +5 以後: 都不夠或太大 → break

result = [[1,1,6], [1,2,5], [1,7], [2,6]]
```

#### 範例 2：candidates = [2, 5, 2, 1, 2], target = 5

```
排序後: [1, 2, 2, 2, 5]

backtrack(0, [], 5)
├── +1(i=0): remaining=4
│   ├── +2(i=1) → +2(i=2): remaining=0 → 收集 [1,2,2] ✓
│   │            (+2(i=3): SKIP 去重 ✗)
│   ├── +2(i=2): SKIP（i>start 且 ==前一個）✗
│   └── +5: 5>4 break
├── +2(i=1): remaining=3 → +2(i=2) remaining=1 → 2>1 break
├── +2(i=2): SKIP 去重 ✗  |  +2(i=3): SKIP 去重 ✗
└── +5(i=4): remaining=0 → 收集 [5] ✓

result = [[1,2,2], [5]]
```

---

### 4.4 Letter Combinations of a Phone Number -- LeetCode 17

#### 問題描述

給定一個包含數字 2-9 的字串，回傳所有可能的字母組合（參考手機九宮格鍵盤）。

```
┌───────┬───────┬───────┐
│   1   │ 2 abc │ 3 def │
├───────┼───────┼───────┤
│ 4 ghi │ 5 jkl │ 6 mno │
├───────┼───────┼───────┤
│ 7 pqrs│ 8 tuv │ 9 wxyz│
└───────┴───────┴───────┘
```

#### 核心思路

```
這題不需要 start index 也不需要 used[]。
因為每個位置（digit）的選擇互不影響：
  第一個 digit → 選一個字母
  第二個 digit → 選一個字母
  ...
類似 n 層巢狀 for loop，但用遞迴實現。

三個關鍵問題：
  Q1: path = 目前拼出的字母字串
  Q2: choices = 當前 digit 對應的字母列表
  Q3: base case = len(path) == len(digits) → 收集
```

#### Pseudocode

```python
def letterCombinations(digits):
    if not digits:
        return []

    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(index, path):
        if index == len(digits):
            result.append("".join(path))
            return

        for letter in phone[digits[index]]:
            path.append(letter)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

#### 範例 1：digits = "23"

```
Decision Tree:

backtrack(0, [])
│  digits[0]='2' → choices = 'abc'
│
├── pick 'a': backtrack(1, ['a'])
│   │  digits[1]='3' → choices = 'def'
│   ├── pick 'd': path=['a','d'] → 收集 "ad" ✓
│   ├── pick 'e': path=['a','e'] → 收集 "ae" ✓
│   └── pick 'f': path=['a','f'] → 收集 "af" ✓
│
├── pick 'b': backtrack(1, ['b'])
│   ├── pick 'd': 收集 "bd" ✓
│   ├── pick 'e': 收集 "be" ✓
│   └── pick 'f': 收集 "bf" ✓
│
└── pick 'c': backtrack(1, ['c'])
    ├── pick 'd': 收集 "cd" ✓
    ├── pick 'e': 收集 "ce" ✓
    └── pick 'f': 收集 "cf" ✓

result = ["ad","ae","af","bd","be","bf","cd","ce","cf"]
共 3 × 3 = 9 個 ✓
```

#### 範例 2：digits = "79"

```
Decision Tree:

backtrack(0, [])
│  digits[0]='7' → choices = 'pqrs'（4 個字母）
│
├── pick 'p': backtrack(1, ['p'])
│   │  digits[1]='9' → choices = 'wxyz'（4 個字母）
│   ├── 'w' → "pw" ✓
│   ├── 'x' → "px" ✓
│   ├── 'y' → "py" ✓
│   └── 'z' → "pz" ✓
│
├── pick 'q': → "qw","qx","qy","qz" ✓
│
├── pick 'r': → "rw","rx","ry","rz" ✓
│
└── pick 's': → "sw","sx","sy","sz" ✓

result = ["pw","px","py","pz","qw","qx","qy","qz",
          "rw","rx","ry","rz","sw","sx","sy","sz"]
共 4 × 4 = 16 個 ✓
```

#### 複雜度

```
時間: O(4^n × n)，n 為 digits 長度
  最壞情況每個 digit 有 4 個字母（如 7 和 9），共 4^n 個組合，
  每個組合拼接字串 O(n)。

空間: O(n)（遞迴深度）
```

---

## 第五章：棋盤型 (Grid Backtracking)

### 5.1 N-Queens -- LeetCode 51（經典中的經典）

#### 問題描述

在 n x n 的棋盤上放 n 個皇后，使得任何兩個皇后都不能互相攻擊（不能在同一行、同一列、同一對角線上）。回傳所有合法的擺法。

#### 核心思路

```
策略：逐行放置（每行放一個皇后），這樣自動滿足「不同行」的限制。
     只需檢查「不同列」和「不同對角線」。

對角線的數學性質（KEY INSIGHT）：
  主對角線 (\): 同一條對角線上，row - col 的值相同
  副對角線 (/): 同一條對角線上，row + col 的值相同

  例如 4×4 棋盤上 row-col 的值:
      col: 0   1   2   3
  row 0:   0  -1  -2  -3
  row 1:   1   0  -1  -2
  row 2:   2   1   0  -1
  row 3:   3   2   1   0
  → 同一 \ 對角線的 row-col 值相同

  row+col 的值:
      col: 0   1   2   3
  row 0:   0   1   2   3
  row 1:   1   2   3   4
  row 2:   2   3   4   5
  row 3:   3   4   5   6
  → 同一 / 對角線的 row+col 值相同

用三個 set 記錄已佔用的:
  cols:     已佔用的列
  diag1:    已佔用的 \ 對角線 (row - col)
  diag2:    已佔用的 / 對角線 (row + col)
```

#### Pseudocode

```python
def solveNQueens(n):
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    cols = set()
    diag1 = set()   # row - col
    diag2 = set()   # row + col

    def backtrack(row):
        if row == n:
            # 收集結果：把 board 轉成字串列表
            result.append(["".join(r) for r in board])
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue         # 衝突，跳過

            # 放置皇后
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)   # 下一行

            # 移除皇后（回溯）
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result
```

#### 範例：n=4 -- 逐步追蹤（展示衝突與回溯）

```
4x4 棋盤，需要放 4 個皇后。用 cols/diag1(row-col)/diag2(row+col) 檢查衝突。

═══ 嘗試 Q 在 (0,0) ═══
  Q . . .    cols={0}, diag1={0}, diag2={0}
  . . . .
  . . . .
  . . . .

  Row 1: (1,0) col衝突 ✗ | (1,1) diag1衝突(0) ✗ | (1,2) OK → 放Q
    Q . . .    +cols={2}, +diag1={-1}, +diag2={3}
    . . Q .
    Row 2: 全部衝突（col/diag1/diag2 都被佔滿）→ 回溯移除(1,2)

  (1,3) OK → 放Q
    Q . . .    +cols={3}, +diag1={-2}, +diag2={4}
    . . . Q
    Row 2: (2,1) OK → 放Q
      Q . . .
      . . . Q    但 Row 3 全部衝突 → 回溯移除(2,1)
      . Q . .
    Row 2 其他位置全衝突 → 回溯移除(1,3)

  Row 1 全失敗 → 回溯移除(0,0)

═══ 嘗試 Q 在 (0,1) ═══
  . Q . .    cols={1}, diag1={-1}, diag2={1}

  Row 1: (1,0) diag2衝突(1) ✗ | (1,1) col衝突 ✗ | (1,2) diag1衝突 ✗ | (1,3) OK
    . Q . .
    . . . Q    +cols={3}, +diag1={-2}, +diag2={4}

    Row 2: (2,0) 全部 OK → 放Q
      . Q . .
      . . . Q    +cols={0}, +diag1={2}, +diag2={2}
      Q . . .

      Row 3: (3,0)col衝突 | (3,1)col衝突 | (3,2) OK! → 放Q
        . Q . .
        . . . Q
        Q . . .    ← row=4 == n → 收集解 1 ✓✓✓
        . . Q .

═══ 嘗試 Q 在 (0,2) ═══
  . . Q .    cols={2}, diag1={-2}, diag2={2}

  Row 1: (1,0) OK → 放Q
    . . Q .
    Q . . .

    Row 2: (2,3) OK → 放Q
      . . Q .
      Q . . .
      . . . Q

      Row 3: (3,1) OK! → 放Q
        . . Q .
        Q . . .    ← row=4 == n → 收集解 2 ✓✓✓
        . . . Q
        . Q . .

═══ (0,3) 嘗試後無新解 ═══

最終 n=4 共 2 個解:
  解 1:          解 2:
  . Q . .        . . Q .
  . . . Q        Q . . .
  Q . . .        . . . Q
  . . Q .        . Q . .
```

#### Corner Case: n=1

```
只有一個格子，放一個皇后：
  Q

result = [["Q"]]
```

---

### 5.2 Word Search -- LeetCode 79

#### 問題描述

給定一個 m x n 的字元棋盤 `board` 和一個字串 `word`，判斷 `word` 是否能在棋盤上由相鄰（上下左右）格子組成。每個格子只能用一次。

#### 核心思路

```
這是 Grid 上的 DFS + Backtracking：
1. 找到 word 的第一個字母作為起點
2. 從起點往上下左右四個方向 DFS
3. 每走一步，比對下一個字母
4. 走過的格子標記為 visited（或改成特殊字元）
5. 走不通就回溯（取消標記）

三個關鍵問題：
  Q1: path = 目前匹配到 word 的第幾個字母
  Q2: choices = 上、下、左、右四個方向
  Q3: base case = 匹配完 word 所有字母 → return True
```

#### Pseudocode

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, k):
        """從 (r,c) 出發，嘗試匹配 word[k:]"""
        if k == len(word):
            return True           # 全部匹配成功

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False          # 越界
        if board[r][c] != word[k]:
            return False          # 字母不匹配

        # 標記已訪問（直接改棋盤，省空間）
        temp = board[r][c]
        board[r][c] = '#'

        # 往四個方向探索
        found = (backtrack(r+1, c, k+1) or
                 backtrack(r-1, c, k+1) or
                 backtrack(r, c+1, k+1) or
                 backtrack(r, c-1, k+1))

        # 回溯：恢復棋盤
        board[r][c] = temp

        return found

    for i in range(rows):
        for j in range(cols):
            if backtrack(i, j, 0):
                return True
    return False
```

#### 範例 1：board, word = "ABCCED"

```
Board:             word = "ABCCED"
  A  B  C  E
  S  F  C  S       從 (0,0) 出發:
  A  D  E  E

Step 1: (0,0)='A'✓ → Step 2: 右(0,1)='B'✓ → Step 3: 右(0,2)='C'✓
Step 4: 下(1,2)='C'✓ → Step 5: 下(2,2)='E'✓ → Step 6: 左(2,1)='D'✓

  #  #  #  E       路徑: A(0,0) → B(0,1) → C(0,2)
  S  F  #  S              → C(1,2) → E(2,2) → D(2,1)
  A  #  #  E       k=6 == len(word) → return True ✓
```

#### 範例 2：board 同上, word = "ABCB"

```
word = "ABCB"
(0,0)='A'✓ → (0,1)='B'✓(標記#) → (0,2)='C'✓
→ 需要 'B': 上越界 | 下'C'✗ | 左'#'已訪問✗ | 右'E'✗
→ 全部失敗！回溯。B 只在 (0,1) 但已用過。
return False ✓（每個格子只能用一次）
```

#### 複雜度

```
時間: O(m × n × 3^L)
  m×n 個起點，每步有 3 個方向（不走回頭路）
  L 為 word 長度

空間: O(L)（遞迴深度 = word 長度）
```

---

## 第六章：子集 vs 排列 vs 組合 -- 終極比較

### 6.1 三大類型對照表

```
┌────────────────┬───────────────┬──────────────────┬───────────────────┐
│                │   Subsets     │  Permutations    │   Combinations    │
│                │   子集         │  排列             │   組合             │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 順序重要嗎？    │   No          │   Yes            │   No              │
│ [1,2]==[2,1]? │   相同        │   不同            │   相同             │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 用全部元素嗎？  │   不一定       │   全部都用        │   選 k 個          │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 避免重複的方式  │  start index  │  used[] array    │  start index      │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 結果數量       │    2^n        │     n!           │    C(n,k)         │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 遞迴下一層     │ backtrack     │ backtrack        │ backtrack         │
│                │ (i+1, path)  │ (path)           │ (i+1, path)      │
│                │              │ (check used[])   │ (stop at len k)  │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 收集時機       │ 每個節點      │ 葉子節點          │ len(path)==k 時   │
│                │ (包含空集)    │ (len==n)         │                   │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 有重複元素時    │ sort +        │ sort +           │ sort +            │
│ 額外處理       │ skip if       │ skip if          │ skip if           │
│                │ nums[i]==     │ nums[i]==        │ nums[i]==         │
│                │ nums[i-1]    │ nums[i-1] and    │ nums[i-1]        │
│                │ and i>start  │ !used[i-1]       │ and i>start      │
├────────────────┼───────────────┼──────────────────┼───────────────────┤
│ 代表題目       │ LC 78, 90     │ LC 46, 47        │ LC 77, 39, 40    │
└────────────────┴───────────────┴──────────────────┴───────────────────┘
```

### 6.2 面試決策流程圖

```
看到回溯類題目
│
├─ 結果的元素順序重要嗎？
│   │
│   ├─ YES → 排列型 (Permutations)
│   │   ├─ 有重複元素？ → LC 47 (sort + used[] + 去重)
│   │   └─ 無重複？ → LC 46 (used[] array)
│   │
│   └─ NO → 子集/組合型
│       │
│       ├─ 要選特定 k 個？或有 target sum？
│       │   ├─ YES → 組合型 (Combinations)
│       │   │   ├─ 元素可重複使用？ → LC 39 (start=i)
│       │   │   ├─ 元素不可重複使用，有重複元素？ → LC 40 (start=i+1 + 去重)
│       │   │   └─ 純粹選 k 個？ → LC 77
│       │   └─ NO → 子集型 (Subsets)
│       │       ├─ 有重複元素？ → LC 90 (sort + 去重)
│       │       └─ 無重複？ → LC 78
│       │
│       └─ 棋盤/格子問題？
│           ├─ 放置類？ → N-Queens (LC 51)
│           └─ 搜尋路徑類？ → Word Search (LC 79)
```

### 6.3 三種模板並排比較

```python
# ═══ Subsets 模板 ═══
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])           # 每個節點都收集
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)       # i+1: 不走回頭路
            path.pop()
    backtrack(0, [])
    return result

# ═══ Permutations 模板 ═══
def permutations(nums):
    result = []
    used = [False] * len(nums)
    def backtrack(path):
        if len(path) == len(nums):       # 葉子節點才收集
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)              # 不需要 start（可回頭選）
            path.pop()
            used[i] = False
    backtrack([])
    return result

# ═══ Combinations 模板 ═══
def combinations(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:               # 長度達 k 時收集
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)       # i+1: 不走回頭路
            path.pop()
    backtrack(1, [])
    return result
```

---

## 第七章：面試實戰

### 7.1 白板策略：回溯題的五步法

```
Step 1: 辨識題型 (30 秒)
  "This looks like a backtracking problem because we need to
   enumerate all possible [subsets/permutations/combinations]."

  判斷依據：
  - 題目說「所有可能的 xxx」→ 幾乎確定是 backtracking
  - 題目說「找出所有方案」→ backtracking
  - 涉及「選或不選」、「排列組合」→ backtracking

Step 2: 回答三個問題 (1 分鐘)
  "Let me define three things:
   1. What is the path? → [你的回答]
   2. What are the choices? → [你的回答]
   3. What is the base case? → [你的回答]"

Step 3: 畫 Decision Tree (2 分鐘)
  在白板上畫出一個小例子的 decision tree。
  這是 backtracking 題最有說服力的溝通方式。
  不需要畫完整棵樹，畫 2-3 層夠面試官理解即可。

Step 4: 寫程式碼 (10 分鐘)
  先寫模板框架：
    def backtrack(___):
        if ___:
            result.append(path[:])
            return
        for ___ in ___:
            path.append(___)
            backtrack(___)
            path.pop()
  再填入具體邏輯。

Step 5: 驗證 + 分析複雜度 (3 分鐘)
  用 Step 3 畫的 tree 做 dry run。
  說出時間複雜度和空間複雜度。
```

### 7.2 常見面試追問 (Follow-up Questions)

```
Q: "Can you optimize this?"
A: 剪枝 (Pruning)！三種常見策略：
  1. 排序 + 提前終止: if candidates[i] > remaining: break
  2. 去重: if i > start and nums[i] == nums[i-1]: continue
  3. 數學判斷剩餘可行性: if n-i+1 < k-len(path): break

Q: "What if we need only one solution instead of all?"
A: backtrack 返回 True 時立刻 return True，不繼續搜尋。

Q: "What is the time complexity?"
A: Subsets O(2^n) | Permutations O(n!) | Combinations O(C(n,k))
   Pruning 減少常數因子，但最壞情況不變。

Q: "Can you do it iteratively?"
A: Subsets 可用迭代（result += [s+[num] for s in result]），
   但排列/組合用遞迴更直觀，面試建議用遞迴。
```

### 7.3 Google 高頻回溯題清單

```
┌─────┬──────────────────────────────────┬────────┬──────────┬──────────┐
│ 題號 │ 題目                              │ 難度    │ 類型      │ 頻率     │
├─────┼──────────────────────────────────┼────────┼──────────┼──────────┤
│  78  │ Subsets                          │ Medium │ 子集      │ 高       │
│  90  │ Subsets II                       │ Medium │ 子集      │ 中       │
│  46  │ Permutations                     │ Medium │ 排列      │ 高       │
│  47  │ Permutations II                  │ Medium │ 排列      │ 中       │
│  77  │ Combinations                     │ Medium │ 組合      │ 中       │
│  39  │ Combination Sum                  │ Medium │ 組合      │ 高       │
│  40  │ Combination Sum II               │ Medium │ 組合      │ 中       │
│  17  │ Letter Combinations Phone Number │ Medium │ 組合      │ 高       │
│  51  │ N-Queens                         │ Hard   │ 棋盤      │ 中       │
│  79  │ Word Search                      │ Medium │ 棋盤      │ 非常高   │
│  22  │ Generate Parentheses             │ Medium │ 特殊      │ 非常高   │
│  131 │ Palindrome Partitioning          │ Medium │ 分割      │ 中       │
│  93  │ Restore IP Addresses             │ Medium │ 分割      │ 中       │
└─────┴──────────────────────────────────┴────────┴──────────┴──────────┘
```

### 7.4 回溯法常見錯誤清單

```
1. 忘記複製 path: ✗ result.append(path) → ✓ result.append(path[:])
2. 子集/組合忘記 start index → 產生重複如 [1,2] 和 [2,1]
3. 排列忘記 used[] 陣列 → 同一元素被重複選取
4. Combination Sum start 搞錯:
   可重複用 backtrack(i,...) | 不可重複用 backtrack(i+1,...)
5. 有重複元素忘記先排序 → 去重條件 nums[i]==nums[i-1] 失效
6. N-Queens 忘記對角線: 必須檢查 row-col 和 row+col
7. Word Search 忘記恢復棋盤: 回溯時要 board[r][c] = temp
```

### 7.5 總結：回溯法的本質

```
回溯法的本質就是一棵 Decision Tree（決策樹）。

               ROOT
             /  |  \
          選 A  選 B  選 C     ← 第一層：第一個選擇
          /|\   /|\   /|\
         ... ... ...           ← 第二層：第二個選擇
         ...                   ← ...
        葉子節點 = 最終結果      ← 收集答案

你要做的只有三件事：
  1. 在每個節點做出選擇 (make choice)
  2. 遞迴到下一層 (recurse)
  3. 回到這一層時撤銷選擇 (undo choice)

不要害怕 Backtracking。
它不是什麼神秘的演算法，就是暴力搜尋 + 聰明的剪枝。
把 Decision Tree 畫出來，程式碼就自然寫出來了。
```

> **配套練習**：執行 `python3 13_Backtracking.py` 查看所有範例的完整輸出。
> **下一章預告**：`14_Greedy_教學.md` -- 貪心演算法，看起來像 Backtracking 但不需要回溯的情況。
