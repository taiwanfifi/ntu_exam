# LeetCode 教學 #03：HashMap / HashSet 完全攻略

> **適用對象**：LeetCode 初學者，準備 Google 面試
> **前置知識**：Python 基礎（list, dict, set 的語法）、Big-O 概念
> **配套程式**：`03_HashMap_HashSet.py`（可直接執行看 step-by-step trace）

---

## 第一章：Hash 的基礎原理

### 1.1 什麼是 Hashing？

想像你有一本電話簿，裡面有 100 萬筆資料。如果用 list 存，要找某個人的電話，最壞要從頭掃到尾，花 O(n) 時間。但如果你能用某種魔法，**直接算出那個人存在哪個位置**，就能 O(1) 拿到結果。

這個「魔法」就是 **Hash Function（雜湊函數）**。

```
Hash Function 的角色：

  key（鍵）  ──→  hash(key)  ──→  index（陣列索引）

  例如：
  "Alice"  ──→  hash("Alice")  ──→  3
  "Bob"    ──→  hash("Bob")    ──→  7
  "Carol"  ──→  hash("Carol")  ──→  1
```

**Hash Table（雜湊表）** 的本質就是：一個陣列 + 一個 hash function。

```
  index:  [  0  ][  1  ][  2  ][  3  ][  4  ][  5  ][  6  ][  7  ]
  value:  [     ][Carol][     ][Alice][     ][     ][     ][ Bob ]
```

你給它一個 key，它用 hash function 算出 index，直接跳到那個位置讀取。不需要掃描整個陣列。

---

### 1.2 Hash Function 的運作方式

一個簡化的 hash function 範例：

```
hash(key) = key 的某種數值 % table_size

範例：table_size = 8

hash("Alice") = (65+108+105+99+101) % 8 = 478 % 8 = 6
hash("Bob")   = (66+111+98)         % 8 = 275 % 8 = 3
hash("Carol") = (67+97+114+111+108) % 8 = 497 % 8 = 1
```

Python 的 `hash()` 內建函數就是做這件事（但更複雜、更均勻）。

**好的 Hash Function 的特性**：
1. **確定性（Deterministic）**：同一個 key 永遠算出同一個 index
2. **均勻分布（Uniform Distribution）**：不同的 key 盡量散到不同的 index
3. **快速計算（Fast Computation）**：計算 hash 值本身要 O(1)

---

### 1.3 Hash Collision（碰撞）

**問題**：兩個不同的 key 可能算出相同的 index！

```
hash("Alice") = 478 % 8 = 6
hash("Eve")   = (69+118+101) % 8 = 288 % 8 = 0  ← 沒碰撞
hash("Dan")   = (68+97+110) % 8 = 275 % 8 = 3
hash("Bob")   = (66+111+98) % 8 = 275 % 8 = 3   ← 碰撞！Dan 和 Bob 都是 3
```

這叫做 **Hash Collision（碰撞）**。處理碰撞有兩大策略：

#### 策略一：Chaining（鏈式法）— Python dict 採用的概念

每個 index 位置不只存一個值，而是存一個 linked list（鏈結串列）。碰撞時就把新元素加到鏈的尾端。

```
  index:  [0] → [Eve]
          [1] → [Carol]
          [2] → (空)
          [3] → [Dan] → [Bob]     ← 兩個元素串在一起
          [4] → (空)
          [5] → (空)
          [6] → [Alice]
          [7] → (空)

  查找 "Bob"：
  1. hash("Bob") = 3
  2. 到 index 3，走鏈結：Dan → 不是 → Bob → 找到了！
```

#### 策略二：Open Addressing（開放定址法）

碰撞時，往下找下一個空位。

```
  Linear Probing 範例：

  插入順序：Dan(→3), Bob(→3 碰撞, 往下找 →4)

  index:  [0] → [Eve]
          [1] → [Carol]
          [2] → (空)
          [3] → [Dan]     ← Dan 佔了 3
          [4] → [Bob]     ← Bob 碰撞，往下找到 4
          [5] → (空)
          [6] → [Alice]
          [7] → (空)

  查找 "Bob"：
  1. hash("Bob") = 3
  2. index 3 是 Dan，不是 Bob → 往下看
  3. index 4 是 Bob → 找到了！
```

**Python 實際做法**：Python 的 `dict` 使用的是 Open Addressing 的變體（不是純 linear probing，而是用二次探測的方式），但概念一樣。

---

### 1.4 為什麼 O(1)？ — 攤銷分析直覺

**理想情況**：hash function 夠均勻、table 夠大 → 每個 index 只有一個元素 → 查找 O(1)。

**最壞情況**：所有元素都碰撞到同一個 index → 退化成 linked list → 查找 O(n)。

**實際上**：Python 的 dict/set 會在元素太多時自動擴容（rehash），保持 load factor 在合理範圍，所以**平均時間是 O(1)**。

```
Hash Table 操作的時間複雜度：

┌──────────────┬──────────┬──────────┐
│ 操作          │ 平均     │ 最壞     │
├──────────────┼──────────┼──────────┤
│ 插入 (Insert) │ O(1)     │ O(n)     │
│ 查找 (Lookup) │ O(1)     │ O(n)     │
│ 刪除 (Delete) │ O(1)     │ O(n)     │
└──────────────┴──────────┴──────────┘

面試時說 O(1) 即可，但要知道最壞是 O(n)。
```

---

### 1.5 Python 的 dict vs set vs list

```
┌──────────────────┬────────────┬──────────────┬───────────────────────┐
│ 資料結構          │ 儲存內容    │ 查找時間      │ 使用場景               │
├──────────────────┼────────────┼──────────────┼───────────────────────┤
│ dict (HashMap)   │ key→value  │ O(1) average │ 需要 key 對應 value    │
│                  │            │              │ 計數、索引查找、分組   │
├──────────────────┼────────────┼──────────────┼───────────────────────┤
│ set (HashSet)    │ key only   │ O(1) average │ 只需判斷「有沒有」     │
│                  │            │              │ 去重、成員檢查         │
├──────────────────┼────────────┼──────────────┼───────────────────────┤
│ list (Array)     │ index→value│ O(1) by index│ 需要有序存取           │
│                  │            │ O(n) by value│ key 是連續整數         │
└──────────────────┴────────────┴──────────────┴───────────────────────┘

決策流程：
  你需要 key → value 的對應？ → 用 dict
  你只需要判斷「這個元素存不存在」？ → 用 set
  你的 key 是 0~25 的小整數（如字母頻率）？ → 用 list[26] (最快)
```

**Python 語法速查**：

```python
# dict
d = {}
d["apple"] = 3          # 插入/更新
print(d["apple"])        # 查找 → 3
print("apple" in d)      # 存在性檢查 → True
del d["apple"]           # 刪除
d.get("banana", 0)       # 查找，不存在回傳預設值 0

# set
s = set()
s.add(5)                 # 插入
print(5 in s)            # 存在性檢查 → True
s.remove(5)              # 刪除（不存在會 error）
s.discard(5)             # 刪除（不存在不會 error）

# collections.Counter（dict 的子類別）
from collections import Counter
c = Counter("aabbc")     # → Counter({'a': 2, 'b': 2, 'c': 1})
c.most_common(2)         # → [('a', 2), ('b', 2)]

# collections.defaultdict
from collections import defaultdict
dd = defaultdict(list)
dd["group1"].append("item")  # 自動初始化為空 list
```

---

## 第二章：計數型 HashMap（Frequency Counting）

### 2.1 Two Sum (LeetCode #1) — 面試最經典題

**題目**：給一個整數陣列 `nums` 和一個目標值 `target`，找出兩個數字使其和等於 target，回傳它們的索引。

**暴力解法 O(n^2)**：兩層迴圈，試所有配對。

```python
# Brute Force — O(n²) Time, O(1) Space
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**HashMap 解法 O(n)**：

**核心洞見**：如果我們要找 `nums[i] + nums[j] == target`，等價於找 `nums[j] == target - nums[i]`。所以我們可以：

1. 遍歷陣列時，把每個數字和它的索引存進 HashMap
2. 對當前數字，計算 `complement = target - nums[i]`
3. 查 HashMap 裡有沒有 `complement` → O(1)

```python
# HashMap — O(n) Time, O(n) Space
def two_sum(nums, target):
    lookup = {}  # num → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        lookup[num] = i
    return []
```

**為什麼 one-pass（一次遍歷）就夠？** 因為如果 `(i, j)` 是答案（i < j），當我們走到 j 時，i 已經被存進 map 了。所以我們不需要先建完整個 map 再查。

---

#### 範例 1：nums = [2, 7, 11, 15], target = 9

```
初始狀態：lookup = {}, target = 9

Step 1: i=0, num=2
  complement = 9 - 2 = 7
  7 在 lookup 裡嗎？ lookup = {} → 不在
  存入：lookup = {2: 0}

Step 2: i=1, num=7
  complement = 9 - 7 = 2
  2 在 lookup 裡嗎？ lookup = {2: 0} → 在！index = 0
  回傳 [0, 1] ✓

答案：nums[0] + nums[1] = 2 + 7 = 9 ✓
```

---

#### 範例 2：nums = [3, 2, 4], target = 6

```
初始狀態：lookup = {}, target = 6

Step 1: i=0, num=3
  complement = 6 - 3 = 3
  3 在 lookup 裡嗎？ lookup = {} → 不在
  存入：lookup = {3: 0}

Step 2: i=1, num=2
  complement = 6 - 2 = 4
  4 在 lookup 裡嗎？ lookup = {3: 0} → 不在
  存入：lookup = {3: 0, 2: 1}

Step 3: i=2, num=4
  complement = 6 - 4 = 2
  2 在 lookup 裡嗎？ lookup = {3: 0, 2: 1} → 在！index = 1
  回傳 [1, 2] ✓

答案：nums[1] + nums[2] = 2 + 4 = 6 ✓

注意：這裡 3+3=6 也等於 target，但 3 只出現一次（index 0），
      所以不能用同一個元素兩次。one-pass 天然避免了這個問題，
      因為我們先查 map 再存入——查的時候自己還沒進 map。
```

---

#### Corner Cases

| 狀況 | 範例 | 注意事項 |
|------|------|---------|
| 同一元素不能用兩次 | `[3,2,4], target=6` → [1,2] 而非 [0,0] | one-pass 自然處理 |
| 有負數 | `[-1,0,3,5], target=2` → complement = 2-(-1)=3 | 完全正常運作 |
| 剛好兩個相同元素 | `[3,3], target=6` → [0,1] | 第二個 3 查到第一個 3 |
| 答案在最後 | `[1,2,3,4], target=7` → [2,3] | 必須掃完才找到 |

**面試白板提示**：
- 先問：可以假設一定有解嗎？有多組解要回傳哪個？
- 先寫 brute force 讓面試官知道你懂，再說「我可以用 HashMap 優化」
- one-pass 寫法比 two-pass 更優雅，面試官更喜歡

---

### 2.2 Valid Anagram (LeetCode #242)

**題目**：給兩個字串 `s` 和 `t`，判斷 `t` 是否是 `s` 的 anagram（字母重排）。

**核心思路**：兩個字串是 anagram ⟺ 每個字母出現的次數完全相同。

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    for ch in t:
        count[ch] = count.get(ch, 0) - 1
        if count[ch] < 0:
            return False
    return True
```

**Time**: O(n), **Space**: O(1) — 最多 26 個英文字母，所以 space 是常數。

---

#### 範例 1：s = "anagram", t = "nagaram"

```
Step 0: len(s)=7, len(t)=7 → 長度相同，繼續

Phase 1 — 掃描 s，建立字頻表：
  ch='a' → count = {'a': 1}
  ch='n' → count = {'a': 1, 'n': 1}
  ch='a' → count = {'a': 2, 'n': 1}
  ch='g' → count = {'a': 2, 'n': 1, 'g': 1}
  ch='r' → count = {'a': 2, 'n': 1, 'g': 1, 'r': 1}
  ch='a' → count = {'a': 3, 'n': 1, 'g': 1, 'r': 1}
  ch='m' → count = {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}

Phase 2 — 掃描 t，遞減字頻：
  ch='n' → count['n'] = 1-1 = 0  → ≥0 OK
  ch='a' → count['a'] = 3-1 = 2  → ≥0 OK
  ch='g' → count['g'] = 1-1 = 0  → ≥0 OK
  ch='a' → count['a'] = 2-1 = 1  → ≥0 OK
  ch='r' → count['r'] = 1-1 = 0  → ≥0 OK
  ch='a' → count['a'] = 1-1 = 0  → ≥0 OK
  ch='m' → count['m'] = 1-1 = 0  → ≥0 OK

全部掃完且無 < 0 → return True ✓
```

---

#### 範例 2：s = "rat", t = "car"

```
Step 0: len(s)=3, len(t)=3 → 長度相同，繼續

Phase 1 — 掃描 s：
  ch='r' → count = {'r': 1}
  ch='a' → count = {'r': 1, 'a': 1}
  ch='t' → count = {'r': 1, 'a': 1, 't': 1}

Phase 2 — 掃描 t：
  ch='c' → count['c'] = 0-1 = -1  → < 0 → return False ✗

解釋：'c' 在 s 中不存在（次數為 0），但 t 中有 'c'，
      所以遞減後 < 0，立即知道不是 anagram。
```

**替代寫法**：用 `Counter` 一行搞定（面試時可以先說這個，再手寫展開版）

```python
from collections import Counter
def is_anagram(s, t):
    return Counter(s) == Counter(t)
```

---

### 2.3 Top K Frequent Elements (LeetCode #347)

**題目**：給一個整數陣列 `nums` 和一個整數 `k`，回傳出現頻率最高的前 `k` 個元素。

**三種解法比較**：

```
┌─────────────────────┬──────────────┬──────────┬──────────────────────┐
│ 方法                 │ Time         │ Space    │ 說明                  │
├─────────────────────┼──────────────┼──────────┼──────────────────────┤
│ 1. Sort by freq     │ O(n log n)   │ O(n)     │ 先計數，排序取前 k    │
│ 2. Min-Heap         │ O(n log k)   │ O(n)     │ 維護 size=k 的 heap   │
│ 3. Bucket Sort ★    │ O(n)         │ O(n)     │ 最佳！index=頻率      │
└─────────────────────┴──────────────┴──────────┴──────────────────────┘
```

**Bucket Sort 解法（最佳）**：

```python
def top_k_frequent(nums, k):
    # Step 1: 計算頻率
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1

    # Step 2: Bucket Sort — bucket[i] = 出現 i 次的元素們
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]
    for num, cnt in freq.items():
        buckets[cnt].append(num)

    # Step 3: 從高頻到低頻取，取滿 k 個
    result = []
    for i in range(n, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

**關鍵洞見**：為什麼可以用 bucket sort？因為頻率的範圍是 `[1, n]`（一個元素最多出現 n 次），所以我們可以開一個大小 n+1 的陣列，用頻率當 index。

---

#### 範例 1：nums = [1,1,1,2,2,3], k = 2

```
Step 1 — 計算頻率：
  遍歷 [1,1,1,2,2,3]
  freq = {1: 3, 2: 2, 3: 1}

Step 2 — Bucket Sort（n=6, 建 7 個 bucket）：
  bucket[0] = []
  bucket[1] = [3]        ← 3 出現 1 次
  bucket[2] = [2]        ← 2 出現 2 次
  bucket[3] = [1]        ← 1 出現 3 次
  bucket[4] = []
  bucket[5] = []
  bucket[6] = []

Step 3 — 從高頻取（從 bucket[6] 往回掃）：
  bucket[6] = [] → 跳過
  bucket[5] = [] → 跳過
  bucket[4] = [] → 跳過
  bucket[3] = [1] → result = [1]    （取了 1 個）
  bucket[2] = [2] → result = [1, 2] （取了 2 個 = k）→ 回傳！

答案：[1, 2] ✓（出現最多的是 1 和 2）
```

---

#### 範例 2：nums = [4,4,4,6,6,6,6,2], k = 1

```
Step 1 — 計算頻率：
  遍歷 [4,4,4,6,6,6,6,2]
  freq = {4: 3, 6: 4, 2: 1}

Step 2 — Bucket Sort（n=8, 建 9 個 bucket）：
  bucket[0] = []
  bucket[1] = [2]        ← 2 出現 1 次
  bucket[2] = []
  bucket[3] = [4]        ← 4 出現 3 次
  bucket[4] = [6]        ← 6 出現 4 次
  bucket[5] ~ bucket[8] = []

Step 3 — 從高頻取：
  bucket[8] ~ [5] = [] → 跳過
  bucket[4] = [6] → result = [6] （取了 1 個 = k）→ 回傳！

答案：[6] ✓（6 出現最多，4 次）
```

**面試白板提示**：
- 先說「最簡單是排序 O(n log n)」，再說「可以用 heap O(n log k)」，最後說「最佳解是 bucket sort O(n)」
- 面試官通常期望你至少想到 heap，bucket sort 是加分

---

## 第三章：映射型 HashMap（Mapping）

### 3.1 Group Anagrams (LeetCode #49)

**題目**：給一個字串陣列，把所有 anagram 分到同一組。

**核心洞見**：兩個字串是 anagram ⟺ 排序後的字串相同。所以用 `sorted(word)` 當 HashMap 的 key。

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))  # 排序後當 key
        groups[key].append(s)
    return list(groups.values())
```

**Time**: O(n * k log k)，n = 字串數量，k = 最長字串長度。
**Space**: O(n * k)。

---

#### 範例 1：strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

```
遍歷每個字串，算 sorted key：

  "eat" → sorted = "aet" → groups = {"aet": ["eat"]}
  "tea" → sorted = "aet" → groups = {"aet": ["eat", "tea"]}
  "tan" → sorted = "ant" → groups = {"aet": ["eat", "tea"], "ant": ["tan"]}
  "ate" → sorted = "aet" → groups = {"aet": ["eat", "tea", "ate"], "ant": ["tan"]}
  "nat" → sorted = "ant" → groups = {"aet": ["eat", "tea", "ate"], "ant": ["tan", "nat"]}
  "bat" → sorted = "abt" → groups = {"aet": ["eat","tea","ate"], "ant": ["tan","nat"], "abt": ["bat"]}

答案：[["eat","tea","ate"], ["tan","nat"], ["bat"]] ✓
```

---

#### 範例 2：strs = ["abc", "bca", "xyz", "zyx", "aaa"]

```
  "abc" → sorted = "abc" → groups = {"abc": ["abc"]}
  "bca" → sorted = "abc" → groups = {"abc": ["abc", "bca"]}
  "xyz" → sorted = "xyz" → groups = {"abc": ["abc","bca"], "xyz": ["xyz"]}
  "zyx" → sorted = "xyz" → groups = {"abc": ["abc","bca"], "xyz": ["xyz","zyx"]}
  "aaa" → sorted = "aaa" → groups = {"abc": ["abc","bca"], "xyz": ["xyz","zyx"], "aaa": ["aaa"]}

答案：[["abc","bca"], ["xyz","zyx"], ["aaa"]] ✓
```

**進階替代 key**：如果 k 很大，排序 O(k log k) 太慢，可以用 `tuple(Counter(s))` 或 `tuple(count[0..25])` 當 key，只要 O(k)。但面試中 sorted 已足夠。

---

### 3.2 Isomorphic Strings (LeetCode #205)

**題目**：給兩個字串 `s` 和 `t`，判斷它們是否同構。同構 = 可以把 s 中的每個字元替換成另一個字元得到 t，且替換必須一對一。

**為什麼需要雙向映射？**

```
只有單向映射的問題：

  s = "ab", t = "aa"

  如果只檢查 s→t：
    'a' → 'a' ✓
    'b' → 'a' ✓  （不同字元映射到同一個，但 s→t 沒檢查到！）

  結論：單向映射會漏判！需要同時檢查 s→t 和 t→s。
    s→t: 'a'→'a', 'b'→'a'  ✓
    t→s: 'a'→'a' 先建立，但 'a'→'b' 衝突！→ False ✓
```

```python
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    s_to_t = {}
    t_to_s = {}
    for sc, tc in zip(s, t):
        if sc in s_to_t and s_to_t[sc] != tc:
            return False
        if tc in t_to_s and t_to_s[tc] != sc:
            return False
        s_to_t[sc] = tc
        t_to_s[tc] = sc
    return True
```

**Time**: O(n), **Space**: O(n)

---

#### 範例 1：s = "egg", t = "add"

```
Step 1: sc='e', tc='a'
  s_to_t = {}, t_to_s = {}
  'e' 不在 s_to_t → OK
  'a' 不在 t_to_s → OK
  建立映射：s_to_t = {'e': 'a'}, t_to_s = {'a': 'e'}

Step 2: sc='g', tc='d'
  'g' 不在 s_to_t → OK
  'd' 不在 t_to_s → OK
  建立映射：s_to_t = {'e': 'a', 'g': 'd'}, t_to_s = {'a': 'e', 'd': 'g'}

Step 3: sc='g', tc='d'
  'g' 在 s_to_t 且 s_to_t['g'] = 'd' == tc → OK
  'd' 在 t_to_s 且 t_to_s['d'] = 'g' == sc → OK
  （映射一致，不需更新）

全部通過 → return True ✓

映射關係：e↔a, g↔d
```

---

#### 範例 2：s = "foo", t = "bar"

```
Step 1: sc='f', tc='b'
  建立映射：s_to_t = {'f': 'b'}, t_to_s = {'b': 'f'}

Step 2: sc='o', tc='a'
  建立映射：s_to_t = {'f': 'b', 'o': 'a'}, t_to_s = {'b': 'f', 'a': 'o'}

Step 3: sc='o', tc='r'
  'o' 在 s_to_t 且 s_to_t['o'] = 'a' ≠ 'r' → return False ✗

解釋：第二個 'o' 之前映射到 'a'，但現在要映射到 'r'，不一致！
```

---

### 3.3 Word Pattern (LeetCode #290)

**題目**：給一個 pattern 字串和一個空格分隔的字串 s，判斷 s 中的單字是否依循 pattern。

**思路完全同 Isomorphic Strings**：pattern 的字元 ↔ s 的單字 必須一對一映射。

```python
def word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    p_to_w = {}
    w_to_p = {}
    for p, w in zip(pattern, words):
        if p in p_to_w and p_to_w[p] != w:
            return False
        if w in w_to_p and w_to_p[w] != p:
            return False
        p_to_w[p] = w
        w_to_p[w] = p
    return True
```

---

#### 範例 1：pattern = "abba", s = "dog cat cat dog"

```
words = ["dog", "cat", "cat", "dog"]
len(pattern)=4 == len(words)=4 → OK

Step 1: p='a', w="dog"
  p_to_w = {}, w_to_p = {} → 都不在
  建立：p_to_w = {'a': "dog"}, w_to_p = {"dog": 'a'}

Step 2: p='b', w="cat"
  'b' 不在 p_to_w, "cat" 不在 w_to_p → OK
  建立：p_to_w = {'a': "dog", 'b': "cat"}, w_to_p = {"dog": 'a', "cat": 'b'}

Step 3: p='b', w="cat"
  p_to_w['b'] = "cat" == w → OK
  w_to_p["cat"] = 'b' == p → OK（一致）

Step 4: p='a', w="dog"
  p_to_w['a'] = "dog" == w → OK
  w_to_p["dog"] = 'a' == p → OK（一致）

全部通過 → return True ✓
```

---

#### 範例 2：pattern = "abba", s = "dog dog dog dog"

```
words = ["dog", "dog", "dog", "dog"]

Step 1: p='a', w="dog"
  建立：p_to_w = {'a': "dog"}, w_to_p = {"dog": 'a'}

Step 2: p='b', w="dog"
  'b' 不在 p_to_w → OK
  "dog" 在 w_to_p 且 w_to_p["dog"] = 'a' ≠ 'b' → return False ✗

解釋：'a' 和 'b' 不同的 pattern 字元不能映射到同一個 word "dog"。
```

---

## 第四章：HashSet 去重與查找

### 4.1 Longest Consecutive Sequence (LeetCode #128) — Google 高頻

**題目**：給一個未排序的整數陣列，找出最長連續整數序列的長度。要求 O(n) 時間。

**為什麼不能排序？** 排序是 O(n log n)，題目要求 O(n)。

**為什麼 HashSet 能做到 O(n)？**

**關鍵洞見**：
1. 把所有數字丟進 HashSet → O(n)
2. 遍歷 set 中的每個數字 num
3. **只從序列的起點開始計數**：如果 `num - 1` 不在 set 裡，代表 num 就是某個連續序列的起點
4. 從起點往上數：num, num+1, num+2, ... 直到不在 set 裡為止
5. 記錄最長長度

**為什麼是 O(n)？** 每個元素最多被訪問兩次：一次是在外層迴圈（判斷是否為起點），一次是在內層 while 計數。跳過非起點的元素不會觸發 while。

```python
def longest_consecutive(nums):
    if not nums:
        return 0
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:  # num 是序列起點
            cur = num
            length = 1
            while cur + 1 in num_set:
                cur += 1
                length += 1
            best = max(best, length)
    return best
```

---

#### 範例 1：nums = [100, 4, 200, 1, 3, 2]

```
Step 0: num_set = {1, 2, 3, 4, 100, 200}

遍歷 num_set 中的每個元素：

num = 1:
  1 - 1 = 0 → 0 不在 set → 1 是起點！
  往上數：1 → 2 在 set → 2 → 3 在 set → 3 → 4 在 set → 4 → 5 不在 set
  序列 = [1, 2, 3, 4], length = 4
  best = max(0, 4) = 4

num = 2:
  2 - 1 = 1 → 1 在 set → 2 不是起點 → 跳過

num = 3:
  3 - 1 = 2 → 2 在 set → 3 不是起點 → 跳過

num = 4:
  4 - 1 = 3 → 3 在 set → 4 不是起點 → 跳過

num = 100:
  100 - 1 = 99 → 99 不在 set → 100 是起點！
  往上數：100 → 101 不在 set
  序列 = [100], length = 1
  best = max(4, 1) = 4

num = 200:
  200 - 1 = 199 → 199 不在 set → 200 是起點！
  往上數：200 → 201 不在 set
  序列 = [200], length = 1
  best = max(4, 1) = 4

答案：4 ✓（最長連續序列是 [1,2,3,4]）
```

---

#### 範例 2：nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]

```
Step 0: num_set = {0, 1, 2, 3, 4, 5, 6, 7, 8}
（注意：重複的 0 被 set 自動去重）

遍歷 num_set：

num = 0:
  0 - 1 = -1 → -1 不在 set → 0 是起點！
  往上數：0→1→2→3→4→5→6→7→8→ 9 不在 set
  序列 = [0,1,2,3,4,5,6,7,8], length = 9
  best = max(0, 9) = 9

num = 1:  1-1=0 在 set → 跳過
num = 2:  2-1=1 在 set → 跳過
num = 3:  3-1=2 在 set → 跳過
num = 4:  4-1=3 在 set → 跳過
num = 5:  5-1=4 在 set → 跳過
num = 6:  6-1=5 在 set → 跳過
num = 7:  7-1=6 在 set → 跳過
num = 8:  8-1=7 在 set → 跳過

答案：9 ✓（最長連續序列是 [0,1,2,3,4,5,6,7,8]）

效率分析：
- 外層迴圈走了 9 個元素
- 只有 num=0 觸發了 while 迴圈（走了 9 步）
- 其他 8 個元素都被跳過
- 總操作次數 = 9 + 9 = 18 → O(n) ✓
```

---

#### Corner Cases

| 狀況 | 輸入 | 輸出 | 說明 |
|------|------|------|------|
| 空陣列 | `[]` | 0 | 開頭就 return 0 |
| 單一元素 | `[42]` | 1 | 42 是起點，length=1 |
| 全部相同 | `[5,5,5]` | 1 | set = {5}，只有 5 一個起點 |
| 已排序 | `[1,2,3,4]` | 4 | 正常運作 |
| 有負數 | `[-3,-2,-1,0]` | 4 | -3 是起點 |

**面試白板提示**：
- 先問：可以修改原陣列嗎？有重複元素嗎？有負數嗎？
- 關鍵要解釋清楚「為什麼只從起點開始數」以及「為什麼是 O(n)」
- 容易犯的錯：忘記 `if num - 1 not in num_set` 這個判斷，導致 O(n^2)

---

## 第五章：前綴和 + HashMap（Prefix Sum）— 進階必備

### 5.0 什麼是 Prefix Sum？

**前綴和**是一種預處理技巧，讓你能在 O(1) 時間算出任意子陣列的和。

```
原始陣列：    nums  = [3, 1, 4, 1, 5]
              index:   0  1  2  3  4

前綴和陣列：  prefix = [0, 3, 4, 8, 9, 14]
              index:    0  1  2  3  4   5

prefix[i] = nums[0] + nums[1] + ... + nums[i-1]

prefix[0] = 0                          （空前綴）
prefix[1] = 3                          （nums[0]）
prefix[2] = 3 + 1 = 4                  （nums[0..1]）
prefix[3] = 3 + 1 + 4 = 8             （nums[0..2]）
prefix[4] = 3 + 1 + 4 + 1 = 9         （nums[0..3]）
prefix[5] = 3 + 1 + 4 + 1 + 5 = 14   （nums[0..4]）
```

**子陣列和公式**：

```
sum(nums[i..j]) = prefix[j+1] - prefix[i]

範例：sum(nums[1..3]) = nums[1] + nums[2] + nums[3]
                       = 1 + 4 + 1
                       = 6

用前綴和：prefix[4] - prefix[1] = 9 - 3 = 6 ✓
```

**圖解**：

```
prefix:  [0,  3,  4,  8,  9, 14]
              ↑               ↑
           prefix[1]=3     prefix[4]=9

sum(nums[1..3]) = prefix[4] - prefix[1] = 9 - 3 = 6

即：從 prefix 中扣掉前面不要的部分，剩下的就是中間的子陣列和。
```

---

### 5.1 Subarray Sum Equals K (LeetCode #560) — Google 高頻

**題目**：給一個整數陣列 `nums` 和一個整數 `k`，找出和為 `k` 的連續子陣列個數。

**為什麼不能用 Sliding Window？**

```
Sliding Window 適用條件：陣列元素都是正數（或都是負數）。
因為這樣視窗擴大時 sum 一定增加，縮小時 sum 一定減少。

但這題的 nums 可以有負數！

反例：nums = [1, -1, 1, -1], k = 0
  如果用 sliding window，sum 增增減減，你不知道該擴張還是收縮。
```

**HashMap 解法的推導**：

```
目標：找所有 (i, j) 使得 sum(nums[i..j]) == k

用前綴和表示：
  sum(nums[i..j]) = prefix[j+1] - prefix[i] == k
  ⟹ prefix[i] = prefix[j+1] - k

也就是說：如果目前的前綴和是 curr_sum（= prefix[j+1]），
我們要找「之前有多少個前綴和 = curr_sum - k」。

用 HashMap 存 {前綴和: 出現次數}，就能 O(1) 查到！
```

```python
def subarray_sum(nums, k):
    prefix_count = {0: 1}  # 前綴和 0 出現 1 次（空前綴）
    curr_sum = 0
    result = 0
    for num in nums:
        curr_sum += num
        need = curr_sum - k
        if need in prefix_count:
            result += prefix_count[need]
        prefix_count[curr_sum] = prefix_count.get(curr_sum, 0) + 1
    return result
```

**為什麼初始化 `{0: 1}`？** 因為 prefix[0] = 0（空前綴），代表「從陣列開頭到某處的和」本身就可能等於 k。如果 curr_sum == k，那 need = curr_sum - k = 0，此時要能在 map 裡找到 0。

---

#### 範例 1：nums = [1, 1, 1], k = 2

```
初始：prefix_count = {0: 1}, curr_sum = 0, result = 0

Step 1: num = 1
  curr_sum = 0 + 1 = 1
  need = 1 - 2 = -1
  -1 在 prefix_count {0: 1} 嗎？ → 不在
  更新：prefix_count = {0: 1, 1: 1}
  result = 0

Step 2: num = 1
  curr_sum = 1 + 1 = 2
  need = 2 - 2 = 0
  0 在 prefix_count {0: 1, 1: 1} 嗎？ → 在！出現 1 次
  result = 0 + 1 = 1
  更新：prefix_count = {0: 1, 1: 1, 2: 1}

  解讀：curr_sum=2 且 need=0 在 map 中 → 代表從 index 0 開始的子陣列
        sum(nums[0..1]) = prefix[2] - prefix[0] = 2 - 0 = 2 == k ✓
        即子陣列 [1, 1]

Step 3: num = 1
  curr_sum = 2 + 1 = 3
  need = 3 - 2 = 1
  1 在 prefix_count {0: 1, 1: 1, 2: 1} 嗎？ → 在！出現 1 次
  result = 1 + 1 = 2
  更新：prefix_count = {0: 1, 1: 1, 2: 1, 3: 1}

  解讀：curr_sum=3 且 need=1 在 map 中（prefix[1]=1 在 index 1 後出現）
        sum(nums[1..2]) = prefix[3] - prefix[1] = 3 - 1 = 2 == k ✓
        即子陣列 [1, 1]（第二、三個元素）

答案：2 ✓

驗證：和為 2 的子陣列有：
  [1,1,_] → nums[0]+nums[1] = 2 ✓
  [_,1,1] → nums[1]+nums[2] = 2 ✓
  共 2 個 ✓
```

---

#### 範例 2：nums = [1, 2, 3, -1, 2], k = 3

```
初始：prefix_count = {0: 1}, curr_sum = 0, result = 0

Step 1: num = 1
  curr_sum = 1
  need = 1 - 3 = -2
  -2 在 map 嗎？ → 不在
  prefix_count = {0: 1, 1: 1}
  result = 0

Step 2: num = 2
  curr_sum = 1 + 2 = 3
  need = 3 - 3 = 0
  0 在 map 嗎？ → 在！出現 1 次
  result = 0 + 1 = 1
  prefix_count = {0: 1, 1: 1, 3: 1}

  找到子陣列：sum(nums[0..1]) = 1+2 = 3 ✓ → [1, 2]

Step 3: num = 3
  curr_sum = 3 + 3 = 6
  need = 6 - 3 = 3
  3 在 map 嗎？ → 在！出現 1 次
  result = 1 + 1 = 2
  prefix_count = {0: 1, 1: 1, 3: 1, 6: 1}

  找到子陣列：prefix[3]-prefix[?]=6-3=3 → prefix 在 index 2 後為 3
  即 sum(nums[2..2]) = 3 ✓ → [3]

Step 4: num = -1
  curr_sum = 6 + (-1) = 5
  need = 5 - 3 = 2
  2 在 map 嗎？ → 不在
  prefix_count = {0: 1, 1: 1, 3: 1, 6: 1, 5: 1}
  result = 2

Step 5: num = 2
  curr_sum = 5 + 2 = 7
  need = 7 - 3 = 4
  4 在 map 嗎？ → 不在
  prefix_count = {0: 1, 1: 1, 3: 1, 6: 1, 5: 1, 7: 1}
  result = 2

答案：2 ✓

驗證：和為 3 的子陣列有：
  [1, 2]          → 1+2 = 3 ✓
  [3]             → 3 = 3 ✓
  [3, -1, 2]      → 3+(-1)+2 = 4 ✗
  [-1, 2]         → -1+2 = 1 ✗
  [1, 2, 3, -1, 2]→ 7 ✗
  共 2 個 ✓
```

---

#### Corner Cases

| 狀況 | 範例 | 關鍵 |
|------|------|------|
| k = 0 | `[1,-1,1,-1], k=0` → 3 | need = curr_sum，會找到之前相同的 prefix sum |
| 單一元素 = k | `[3], k=3` → 1 | curr_sum=3, need=0, map 有 {0:1} |
| prefix sum 本身 = k | `[3,4,7], k=7` → 2 | [3,4] 和 [7] 都是 |
| 全部負數 | `[-1,-2,-3], k=-3` → 2 | [-1,-2] 和 [-3] |

**面試白板提示**：
- 先解釋「為什麼不能用 sliding window」（因為有負數）
- 畫出 prefix sum 的概念圖
- 解釋 `{0: 1}` 初始化的原因
- 強調 map 存的是 {前綴和 : 出現次數} 而非 {前綴和 : 索引}（因為要計數）

---

### 5.2 Continuous Subarray Sum (LeetCode #523)

**題目**：給一個非負整數陣列 `nums` 和一個正整數 `k`，判斷是否存在長度至少為 2 的連續子陣列，其和是 `k` 的倍數。

**核心洞見 — 模運算（Modular Arithmetic）**：

```
如果 (prefix[j] - prefix[i]) % k == 0
⟹ prefix[j] % k == prefix[i] % k

也就是說：如果兩個前綴和除以 k 的餘數相同，
那麼它們中間的子陣列和就是 k 的倍數！
```

**與 LC 560 的關鍵差異**：
- LC 560：map 存 `{prefix_sum: 出現次數}` → 因為要計算總數
- LC 523：map 存 `{prefix_sum % k: 最早出現的 index}` → 因為要確保長度 >= 2

```python
def check_subarray_sum(nums, k):
    remainder_map = {0: -1}  # 餘數 0 初始出現在 index -1（空前綴）
    curr_sum = 0
    for i, num in enumerate(nums):
        curr_sum += num
        rem = curr_sum % k
        if rem in remainder_map:
            if i - remainder_map[rem] >= 2:  # 長度 >= 2
                return True
            # 長度 < 2，不更新 map（保留最早的 index）
        else:
            remainder_map[rem] = i
    return False
```

**為什麼不更新 map？** 我們存的是「最早出現的 index」，因為越早 = 子陣列越長 = 越容易滿足 >= 2。如果更新成最新的 index，可能會漏掉合法答案。

---

#### 範例 1：nums = [23, 2, 4, 6, 7], k = 6

```
初始：remainder_map = {0: -1}, curr_sum = 0

Step 1: i=0, num=23
  curr_sum = 23
  rem = 23 % 6 = 5
  5 在 map 嗎？ → 不在
  remainder_map = {0: -1, 5: 0}

Step 2: i=1, num=2
  curr_sum = 23 + 2 = 25
  rem = 25 % 6 = 1
  1 在 map 嗎？ → 不在
  remainder_map = {0: -1, 5: 0, 1: 1}

Step 3: i=2, num=4
  curr_sum = 25 + 4 = 29
  rem = 29 % 6 = 5
  5 在 map 嗎？ → 在！ 最早在 index 0
  長度 = 2 - 0 = 2 >= 2 → return True ✓

解讀：
  prefix[3] % 6 = 29 % 6 = 5
  prefix[1] % 6 = 23 % 6 = 5
  ⟹ (prefix[3] - prefix[1]) % 6 = 0
  ⟹ sum(nums[1..2]) = nums[1] + nums[2] = 2 + 4 = 6 是 6 的倍數 ✓
```

---

#### 範例 2：nums = [23, 2, 6, 4, 7], k = 13

```
初始：remainder_map = {0: -1}, curr_sum = 0

Step 1: i=0, num=23
  curr_sum = 23, rem = 23 % 13 = 10
  10 不在 map → remainder_map = {0: -1, 10: 0}

Step 2: i=1, num=2
  curr_sum = 25, rem = 25 % 13 = 12
  12 不在 map → remainder_map = {0: -1, 10: 0, 12: 1}

Step 3: i=2, num=6
  curr_sum = 31, rem = 31 % 13 = 5
  5 不在 map → remainder_map = {0: -1, 10: 0, 12: 1, 5: 2}

Step 4: i=3, num=4
  curr_sum = 35, rem = 35 % 13 = 9
  9 不在 map → remainder_map = {0: -1, 10: 0, 12: 1, 5: 2, 9: 3}

Step 5: i=4, num=7
  curr_sum = 42, rem = 42 % 13 = 3
  3 不在 map → remainder_map = {0: -1, 10: 0, 12: 1, 5: 2, 9: 3, 3: 4}

全部掃完，沒找到 → return False ✗

驗證：
  [23,2] = 25, 25%13=12 ✗
  [2,6] = 8, 8%13≠0 ✗
  [6,4] = 10, 10%13≠0 ✗
  [4,7] = 11, 11%13≠0 ✗
  [23,2,6] = 31, 31%13≠0 ✗
  [2,6,4] = 12, 12%13≠0 ✗
  [6,4,7] = 17, 17%13=4≠0 ✗
  [23,2,6,4] = 35, 35%13≠0 ✗
  [2,6,4,7] = 19, 19%13≠0 ✗
  [23,2,6,4,7] = 42, 42%13≠0 ✗
  確實沒有 → False ✓
```

**面試白板提示**：
- 先說「這題跟 LC 560 類似，但用餘數替代 prefix sum」
- 解釋為什麼 `remainder_map = {0: -1}` → index -1 代表空前綴
- 解釋為什麼「不更新 map」→ 保留最早的 index，讓子陣列盡量長
- 關鍵公式：`prefix[j] % k == prefix[i] % k` ⟹ 中間子陣列和是 k 的倍數

---

## 第六章：HashMap 面試決策框架

### 6.1 Pattern Recognition — 看到什麼用什麼

```
┌─────────────────────────────────────┬──────────────────────────────────┐
│ 題目關鍵字 / 特徵                    │ 應該想到的方法                    │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "two numbers that add up to"        │ Two Sum pattern: dict 存互補數  │
│ "find a pair", "complement"         │                                  │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "anagram", "permutation"            │ Counter / 字頻比較              │
│ "rearrange letters"                 │                                  │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "group by", "categorize"            │ dict 以某種 key 分組             │
│ "group anagrams"                    │ sorted(word) 或 tuple(count)    │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "isomorphic", "pattern matching"    │ 雙向映射 dict (s→t 和 t→s)      │
│ "one-to-one mapping"               │                                  │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "consecutive", "longest streak"     │ HashSet + 找起點                 │
│                                     │ (num-1 not in set)              │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "subarray sum equals k"             │ Prefix Sum + HashMap             │
│ "contiguous subarray", "sum == k"   │ dict 存 {prefix_sum: count}     │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "subarray sum divisible by k"       │ Prefix Sum mod + HashMap         │
│ "multiple of k"                     │ dict 存 {remainder: index}       │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "contains duplicate"                │ HashSet 去重                     │
│ "unique", "distinct"                │                                  │
├─────────────────────────────────────┼──────────────────────────────────┤
│ "frequency", "most common"          │ Counter + 排序或 Bucket Sort     │
│ "top k frequent"                    │                                  │
└─────────────────────────────────────┴──────────────────────────────────┘
```

---

### 6.2 常見錯誤

```
錯誤 1：忘記 Two Sum 是「先查再存」
  ✗ 先存 lookup[num] = i，再查 complement → 可能查到自己
  ✓ 先查 complement，再存 lookup[num] = i

錯誤 2：Isomorphic 只做單向映射
  ✗ 只檢查 s→t → "ab"/"aa" 會誤判為 True
  ✓ 同時維護 s→t 和 t→s

錯誤 3：Longest Consecutive 忘記判斷起點
  ✗ 每個元素都從自己開始往上數 → O(n²)
  ✓ 只有 num-1 不在 set 的才往上數 → O(n)

錯誤 4：Prefix Sum 忘記初始化 {0: 1}
  ✗ prefix_count = {} → 漏掉從 index 0 開始的子陣列
  ✓ prefix_count = {0: 1}

錯誤 5：Continuous Subarray Sum 更新了 map 中的 index
  ✗ 碰到相同餘數時更新 index → 子陣列可能太短
  ✓ 保留最早的 index，不更新
```

---

### 6.3 白板面試技巧

**寫 HashMap 題目的標準流程**：

```
1. 確認需求
   - input/output 格式
   - edge cases（空陣列？重複？負數？）

2. 說出 brute force
   - "最暴力是 O(n²)，兩層迴圈試所有配對"

3. 說出 HashMap 優化
   - "我可以用 HashMap 把查找從 O(n) 降到 O(1)"
   - 明確說出 map 存什麼：{key: value} = {什麼: 什麼}

4. 寫 code
   - 先寫 function signature
   - 初始化 map
   - 主迴圈：「查 → 更新 → 存」

5. 走一遍小 example
   - 在白板上畫出 map 的狀態變化

6. 分析複雜度
   - Time: O(n) — 一次遍歷，每次 O(1) 查找
   - Space: O(n) — map 最多存 n 個元素
```

---

### 6.4 時間/空間複雜度總整理

```
┌─────────────────────────────┬───────────────┬──────────┐
│ 題目                         │ Time          │ Space    │
├─────────────────────────────┼───────────────┼──────────┤
│ Two Sum (LC 1)              │ O(n)          │ O(n)     │
│ Valid Anagram (LC 242)      │ O(n)          │ O(1)*    │
│ Top K Frequent (LC 347)     │ O(n)          │ O(n)     │
│ Group Anagrams (LC 49)      │ O(n * k log k)│ O(n * k) │
│ Isomorphic Strings (LC 205) │ O(n)          │ O(n)     │
│ Word Pattern (LC 290)       │ O(n)          │ O(n)     │
│ Longest Consecutive (LC 128)│ O(n)          │ O(n)     │
│ Subarray Sum = K (LC 560)   │ O(n)          │ O(n)     │
│ Continuous Sub Sum (LC 523) │ O(n)          │ O(n)     │
└─────────────────────────────┴───────────────┴──────────┘
* Anagram 的 space 是 O(1) 因為最多 26 個字母（字元集固定大小）
  k = 字串平均長度
```

---

### 6.5 延伸練習題

完成上面的核心題目後，建議繼續練習這些相關題目：

| 題號 | 題名 | 類型 | 難度 |
|------|------|------|------|
| LC 49 | Group Anagrams | 映射型 | Medium |
| LC 128 | Longest Consecutive Sequence | HashSet | Medium |
| LC 560 | Subarray Sum Equals K | Prefix Sum + HashMap | Medium |
| LC 1 | Two Sum | 計數型 | Easy |
| LC 242 | Valid Anagram | 計數型 | Easy |
| LC 383 | Ransom Note | 計數型 | Easy |
| LC 451 | Sort Characters By Frequency | Bucket Sort | Medium |
| LC 438 | Find All Anagrams in a String | Sliding Window + Counter | Medium |
| LC 525 | Contiguous Array | Prefix Sum + HashMap | Medium |
| LC 974 | Subarray Sums Divisible by K | Prefix Sum mod | Medium |
| LC 217 | Contains Duplicate | HashSet | Easy |
| LC 349 | Intersection of Two Arrays | HashSet | Easy |

---

> **本章總結**：HashMap 和 HashSet 的核心價值是把「查找」從 O(n) 降到 O(1)。面試中遇到需要「快速查找某個值是否存在」或「快速查找某個值對應的資訊」時，第一個想到的就是 Hash。配合 Prefix Sum 技巧，還能處理子陣列和的問題。掌握本章的 9 道經典題，HashMap/HashSet 的面試題就穩了。
