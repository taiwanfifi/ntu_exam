# Python 面試技巧與常用 API 速查手冊

> **適用對象**：準備 Google / NVIDIA 面試、使用 Python 刷題的工程師
> **本文主題**：面試中真正省時間的 Python 內建函式、資料結構、技巧與陷阱
> **語言**：繁體中文解說 + English technical terms
> **核心價值**：不是 Python 教學，是「面試場上 30 秒內寫出正確 code」的速查表

---

## 第一章：Python 面試必備 API

### 1.1 List 操作

List 是 Python 面試中最常用的資料結構，等同於其他語言的 dynamic array。

```python
# ==================== 建立 ====================
arr = [0] * n                              # n 個 0
arr = [[0] * cols for _ in range(rows)]    # 2D array（正確寫法）
arr = list(range(10))                      # [0, 1, 2, ..., 9]
arr = list(range(1, 11))                   # [1, 2, 3, ..., 10]
arr = list(range(0, 10, 2))               # [0, 2, 4, 6, 8]

# ==================== 基本操作 ====================
arr.append(x)       # O(1) amortized，加到尾部
arr.pop()            # O(1)，移除並回傳尾部元素
arr.pop(i)           # O(n)，移除 index i 的元素
arr.pop(0)           # O(n)，移除頭部 → 需要頻繁操作頭部請用 deque！
arr.insert(i, x)     # O(n)，在 index i 插入 x
arr.extend([1,2,3])  # O(k)，把另一個 list 接上去
arr.remove(x)        # O(n)，移除第一個等於 x 的元素，找不到會 ValueError
del arr[i]           # O(n)，刪除 index i

# ==================== 排序 ====================
arr.sort()                        # O(n log n)，in-place，回傳 None！
arr.sort(reverse=True)            # 降序 in-place
sorted(arr)                       # O(n log n)，回傳新 list，原 list 不變
sorted(arr, reverse=True)         # 降序，回傳新 list
arr.sort(key=lambda x: x[1])     # 按自訂 key 排序

# ==================== 查找 ====================
arr.index(x)      # O(n)，回傳第一個 x 的 index，找不到會 ValueError
x in arr           # O(n)，回傳 True/False
arr.count(x)       # O(n)，計算 x 出現幾次

# ==================== 反轉 ====================
arr.reverse()      # in-place，回傳 None
arr[::-1]          # 回傳新 list

# ==================== 其他實用 ====================
len(arr)           # O(1)
min(arr), max(arr) # O(n)
sum(arr)           # O(n)

# ==================== Slicing ====================
arr[i:j]       # 從 index i 到 j-1（不含 j）
arr[i:]        # 從 index i 到結尾
arr[:j]        # 從開頭到 j-1
arr[:]         # 淺複製整個 list
arr[::-1]      # 反轉
arr[::2]       # 每隔一個取（index 0, 2, 4, ...）
arr[1::2]      # 每隔一個取（index 1, 3, 5, ...）
```

**重大陷阱：2D Array 的建立**

```python
# ===== 錯誤寫法 =====
a = [[0] * 3] * 3
# 三行共享同一個 list reference！修改任何一行，其他行全部跟著改！
a[0][0] = 1
# a = [[1,0,0], [1,0,0], [1,0,0]]  ← 全改了！

# ===== 正確寫法 =====
a = [[0] * 3 for _ in range(3)]
# 每行都是獨立的 list
a[0][0] = 1
# a = [[1,0,0], [0,0,0], [0,0,0]]  ← 只改第一行 ✓
```

---

### 1.2 String 操作

Python 的 string 是 **immutable**（不可變），這是面試中最容易忘記的事。

```python
# ==================== 基本方法 ====================
s.lower()              # 全部轉小寫
s.upper()              # 全部轉大寫
s.strip()              # 去掉前後空白
s.lstrip()             # 去掉左邊空白
s.rstrip()             # 去掉右邊空白
s.split()              # 按空白切割成 list
s.split(',')           # 按逗號切割
','.join(lst)          # 把 list 用逗號接成字串
''.join(lst)           # 把 list 直接接起來（無分隔符）

# ==================== 判斷 ====================
s.isalpha()            # 全部是字母？
s.isdigit()            # 全部是數字？
s.isalnum()            # 全部是字母或數字？
s.islower()            # 全部是小寫？
s.isupper()            # 全部是大寫？

# ==================== 查找與替換 ====================
s.find('abc')          # 找子字串，回傳 index，找不到回傳 -1（比 index 安全！）
s.index('abc')         # 找子字串，找不到會 ValueError
s.count('a')           # 計算子字串出現次數
s.replace('old', 'new')  # 替換所有出現的子字串，回傳新字串
s.startswith('pre')    # 是否以 'pre' 開頭
s.endswith('suf')      # 是否以 'suf' 結尾

# ==================== ASCII 轉換 ====================
ord('a')               # 97
ord('A')               # 65
ord('0')               # 48
chr(97)                # 'a'
chr(65)                # 'A'

# ==================== 反轉 ====================
s[::-1]                # 反轉字串

# ==================== 格式化 ====================
f"value is {x}"        # f-string（Python 3.6+）
f"{x:02d}"             # 補零：5 → "05"
f"{x:b}"               # 轉二進位字串
```

**面試常見操作模式：修改字串**

```python
# 字串是 immutable，不能直接修改！
s = "hello"
# s[0] = 'H'  ← TypeError!

# 正確做法：轉 list → 修改 → 轉回 string
chars = list(s)        # ['h', 'e', 'l', 'l', 'o']
chars[0] = 'H'
s = ''.join(chars)     # "Hello"
```

**面試常見操作模式：字母頻率計算**

```python
# 方法一：用 Counter
from collections import Counter
freq = Counter(s)      # {'a': 3, 'b': 2, ...}

# 方法二：用 26 長度的 array（面試常見，因為只有小寫字母時更快）
freq = [0] * 26
for c in s:
    freq[ord(c) - ord('a')] += 1
```

---

### 1.3 Dictionary（Hash Map）

面試中最高頻的資料結構之一。平均 O(1) 查找、插入、刪除。

```python
# ==================== 建立 ====================
d = {}
d = dict()
d = {key: value for key, value in pairs}   # dict comprehension
d = dict(zip(keys, values))                 # 從兩個 list 建立

# ==================== 基本操作 ====================
d[key] = value         # O(1) 新增/修改
val = d[key]           # O(1) 取值，key 不存在會 KeyError
val = d.get(key)       # O(1) 取值，key 不存在回傳 None（安全！）
val = d.get(key, 0)    # O(1) 取值，key 不存在回傳 0（指定預設值）
del d[key]             # O(1) 刪除
key in d               # O(1) 檢查 key 是否存在

# ==================== 遍歷 ====================
for key in d:                      # 遍歷 keys
    pass
for key, val in d.items():         # 遍歷 key-value pairs
    pass
for val in d.values():             # 遍歷 values
    pass

# ==================== 其他 ====================
d.keys()               # 所有 keys（view object）
d.values()             # 所有 values
d.items()              # 所有 (key, value) pairs
d.pop(key)             # 移除並回傳 value
d.pop(key, default)    # 移除並回傳 value，不存在回傳 default
d.setdefault(key, []).append(val)  # key 不存在就設預設值，然後操作

# ==================== 排序 ====================
# 按 key 排序
sorted(d.items())                          # [(key1,val1), (key2,val2), ...]
# 按 value 排序
sorted(d.items(), key=lambda x: x[1])
# 按 value 降序
sorted(d.items(), key=lambda x: -x[1])
```

**defaultdict — 自動初始化的 dict**

```python
from collections import defaultdict

# defaultdict(int) — 預設值 0，完美用於計數
d = defaultdict(int)
d['apple'] += 1        # 不需要先檢查 key 是否存在！

# defaultdict(list) — 預設值 []，完美用於分組
d = defaultdict(list)
d['fruit'].append('apple')  # 不需要先初始化 list！

# defaultdict(set) — 預設值 set()
d = defaultdict(set)
d['fruit'].add('apple')

# 什麼時候用 defaultdict vs dict.get()？
# - 需要「自動建立並累加/追加」→ defaultdict
# - 只是「安全讀取，不存在給預設值」→ dict.get()
```

**Counter — 計數專用**

```python
from collections import Counter

c = Counter("aabbbcc")        # Counter({'b':3, 'a':2, 'c':2})
c = Counter([1,1,2,2,2,3])   # Counter({2:3, 1:2, 3:1})
c = Counter(arr)               # 對 list 計數

c.most_common(2)               # [('b',3), ('a',2)] — 前 2 名
c.most_common()                # 全部按頻率降序

c['a']                         # 取得 'a' 的計數，不存在回傳 0（不會 Error！）
c.update("aab")                # 加入更多元素
c.subtract("ab")               # 減去元素

# Counter 支援數學運算
c1 + c2                        # 合併計數
c1 - c2                        # 相減（結果只保留正數）
c1 & c2                        # 交集（取較小值）
c1 | c2                        # 聯集（取較大值）
```

---

### 1.4 Set

無序、不重複、O(1) 查找。面試中常用來「去重」或「O(1) 查找是否存在」。

```python
# ==================== 建立 ====================
s = set()
s = {1, 2, 3}
s = set([1, 2, 2, 3])         # {1, 2, 3}（自動去重）
s = set("aabbc")               # {'a', 'b', 'c'}

# ==================== 基本操作 ====================
s.add(x)               # O(1) 加入
s.remove(x)            # O(1) 移除，不存在會 KeyError！
s.discard(x)           # O(1) 移除，不存在不會 Error（安全版）
s.pop()                # O(1) 隨機移除一個元素並回傳
x in s                 # O(1) 查找
len(s)                 # O(1) 大小

# ==================== 集合運算 ====================
s1 & s2                # 交集 intersection
s1 | s2                # 聯集 union
s1 - s2                # 差集 difference（在 s1 但不在 s2）
s1 ^ s2                # 對稱差集 symmetric difference（不同時在兩者中）
s1 <= s2               # s1 是 s2 的子集？
s1 >= s2               # s1 是 s2 的超集？

# ==================== 常用面試 pattern ====================
# 去重
unique = list(set(arr))

# O(1) 查找
seen = set()
for x in arr:
    if x in seen:
        print("duplicate!")
    seen.add(x)

# frozenset — 不可變的 set，可以當 dict 的 key 或放進另一個 set
fs = frozenset([1, 2, 3])
```

**重要**：set 是**無序**的，不要假設任何遍歷順序！

---

### 1.5 Tuple

不可變的序列。面試中常用於：dict 的 key、heap 的元素、多值回傳。

```python
t = (1, 2, 3)
t = (1,)               # 單元素 tuple，逗號不能省！
x, y, z = (1, 2, 3)   # 解包 unpacking

# tuple 可以當 dict 的 key（因為 immutable & hashable）
d = {}
d[(1, 2)] = "point"   # ✓
# d[[1, 2]] = "point" # ✗ list 是 unhashable！

# tuple 在 heap 中用於多重排序
# 先比第一個元素，相同再比第二個
import heapq
heap = []
heapq.heappush(heap, (distance, node_id))
```

---

### 1.6 Collections 模組

#### deque — 雙端佇列

當你需要 O(1) 從**頭部**或**尾部**操作時，用 deque 取代 list。

```python
from collections import deque

dq = deque()
dq = deque([1, 2, 3])
dq = deque(maxlen=5)           # 固定長度，滿了自動丟棄最舊的

# ==================== O(1) 雙端操作 ====================
dq.append(x)                   # O(1) 右端加入
dq.appendleft(x)               # O(1) 左端加入
dq.pop()                        # O(1) 右端移除
dq.popleft()                    # O(1) 左端移除

# ==================== 其他 ====================
dq.extend([4, 5])              # 右端批量加入
dq.extendleft([0, -1])        # 左端批量加入（注意：順序會反轉！）
dq.rotate(k)                   # 向右旋轉 k 步（負數向左）
len(dq)                         # O(1)
dq[0]                           # O(1) 看左端
dq[-1]                          # O(1) 看右端
dq[i]                           # O(n) 中間存取！不適合隨機存取
```

**BFS 模板（deque 的經典應用）**

```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    while queue:
        node = queue.popleft()       # O(1)！如果用 list.pop(0) 是 O(n)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

#### OrderedDict（Python 3.7+ 的 dict 已經有序，較少用到）

```python
from collections import OrderedDict

# LRU Cache 的經典實作
class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # 移到最後（最近使用）
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 移除最前面（最久沒用）
```

---

### 1.7 Heapq 模組（Priority Queue）

Python 的 heapq 是 **Min Heap**（最小堆），每次 pop 出最小的元素。

```python
import heapq

# ==================== 基本操作 ====================
heap = []
heapq.heappush(heap, 5)        # O(log n) 加入
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
heapq.heappop(heap)             # O(log n) 回傳最小值 3
heap[0]                          # O(1) 看最小值（不移除）

# ==================== 建立 Heap ====================
arr = [5, 3, 7, 1, 9]
heapq.heapify(arr)              # O(n)! 比逐一 push 的 O(n log n) 更快
heapq.heappop(arr)              # 1

# ==================== 前 K 大/小 ====================
heapq.nlargest(k, arr)          # 前 k 大（回傳 sorted list）
heapq.nsmallest(k, arr)         # 前 k 小

# ==================== Max Heap — 取負數！ ====================
# Python 沒有 Max Heap，用「取負數」模擬
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -7)
largest = -heapq.heappop(max_heap)  # 7

# ==================== Tuple 排序 ====================
# heap 中放 tuple：先比第一個元素，相同再比第二個
heap = []
heapq.heappush(heap, (distance, node_id))
heapq.heappush(heap, (3, 'a'))
heapq.heappush(heap, (1, 'b'))
heapq.heappush(heap, (3, 'c'))
# pop 順序：(1,'b'), (3,'a'), (3,'c')

# ==================== heappushpop & heapreplace ====================
heapq.heappushpop(heap, x)     # push x 再 pop 最小，比分開做更快
heapq.heapreplace(heap, x)     # 先 pop 最小再 push x，比分開做更快
```

**經典面試題：Top K Frequent Elements**

```python
def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

### 1.8 Bisect 模組（Binary Search）

在**已排序的 list** 上做 O(log n) 二分搜尋。

```python
import bisect

arr = [1, 3, 3, 5, 7]

# ==================== 找插入位置 ====================
bisect.bisect_left(arr, 3)     # 2 — 回傳最左邊可以插入 3 的位置
bisect.bisect_right(arr, 3)    # 4 — 回傳最右邊可以插入 3 的位置
bisect.bisect(arr, 3)          # 4 — 等同 bisect_right

# ==================== 插入並保持排序 ====================
bisect.insort(arr, 4)          # arr = [1, 3, 3, 4, 5, 7]
bisect.insort_left(arr, 3)     # 插在最左邊的 3 前面
bisect.insort_right(arr, 3)    # 插在最右邊的 3 後面
```

**面試實戰：用 bisect 實作各種查找**

```python
import bisect

def binary_search(arr, x):
    """檢查 x 是否存在於 sorted array 中"""
    i = bisect.bisect_left(arr, x)
    return i < len(arr) and arr[i] == x

def count_occurrences(arr, x):
    """在 sorted array 中計算 x 出現幾次"""
    left = bisect.bisect_left(arr, x)
    right = bisect.bisect_right(arr, x)
    return right - left

def find_first_ge(arr, x):
    """找第一個 >= x 的元素的 index"""
    return bisect.bisect_left(arr, x)

def find_first_gt(arr, x):
    """找第一個 > x 的元素的 index"""
    return bisect.bisect_right(arr, x)
```

---

### 1.9 itertools 模組

產生排列、組合等，面試中 backtracking 題目有時可以直接用。

```python
from itertools import permutations, combinations, product, accumulate, chain

# ==================== 排列與組合 ====================
list(permutations([1,2,3]))        # 6 種全排列
list(permutations([1,2,3], 2))     # P(3,2) = 6 種
list(combinations([1,2,3], 2))     # C(3,2) = 3 種: (1,2),(1,3),(2,3)
list(combinations_with_replacement([1,2,3], 2))  # 可重複組合

# ==================== 笛卡爾積 ====================
list(product([0,1], repeat=3))     # 2^3 = 8 種: (0,0,0)~(1,1,1)
list(product('ab', 'cd'))          # ('a','c'),('a','d'),('b','c'),('b','d')

# ==================== 累積和（prefix sum） ====================
list(accumulate([1,2,3,4]))        # [1, 3, 6, 10]
list(accumulate([1,2,3,4], initial=0))  # [0, 1, 3, 6, 10]（Python 3.8+）

# ==================== 串接多個 iterable ====================
list(chain([1,2], [3,4], [5]))     # [1, 2, 3, 4, 5]
list(chain.from_iterable([[1,2],[3,4]]))  # [1, 2, 3, 4]
```

---

### 1.10 SortedContainers（第三方但面試可能允許提及）

Python 沒有內建的 balanced BST（像 Java 的 TreeMap），但 `sortedcontainers` 提供了。

```python
# 面試時通常不能 import，但可以跟面試官討論你知道這個概念
from sortedcontainers import SortedList, SortedDict, SortedSet

sl = SortedList([5, 1, 3])    # 自動排序 [1, 3, 5]
sl.add(4)                      # O(log n) [1, 3, 4, 5]
sl.remove(3)                   # O(log n) [1, 4, 5]
sl.bisect_left(4)              # 跟 bisect 一樣
sl[0]                           # 最小值
sl[-1]                          # 最大值

# 面試替代方案：用 heapq 或 bisect + list 模擬
```

---

## 第二章：面試中的 Python 技巧

### 2.1 List Comprehension（一行搞定）

寫得好可以讓面試官覺得你 Python 很熟練。

```python
# 基本
squares = [x**2 for x in range(10)]
evens = [x for x in arr if x % 2 == 0]

# 2D → 1D（flatten）
flat = [x for row in matrix for x in row]
# 等價於:
# flat = []
# for row in matrix:
#     for x in row:
#         flat.append(x)

# 帶條件
result = [x if x > 0 else 0 for x in arr]   # 負數變 0

# Dict comprehension
d = {k: v for k, v in pairs if v > 0}
char_to_idx = {c: i for i, c in enumerate(s)}

# Set comprehension
unique_lengths = {len(w) for w in words}
```

### 2.2 Lambda + Sorting（面試超高頻）

```python
# 按第二個元素排序
arr.sort(key=lambda x: x[1])

# 按第一個元素降序
arr.sort(key=lambda x: -x[0])

# Interval 題：按起始點排序
intervals.sort(key=lambda x: x[0])

# 多重排序：先按長度降序，再按字母序升序
words.sort(key=lambda w: (-len(w), w))

# 自訂排序（更複雜的情況）
from functools import cmp_to_key

def compare(a, b):
    # 回傳負數：a 排在 b 前面
    # 回傳正數：b 排在 a 前面
    # 回傳 0：相等
    if a + b > b + a:
        return -1
    elif a + b < b + a:
        return 1
    return 0

# 經典題：Largest Number（把數字組合成最大的數）
nums_str = [str(n) for n in nums]
nums_str.sort(key=cmp_to_key(compare))
```

### 2.3 常用數學函式

```python
import math

# ==================== 基本 ====================
abs(x)                          # 絕對值
max(a, b), min(a, b)           # 最大/最小
max(arr), min(arr)              # list 中的最大/最小
sum(arr)                        # 總和
pow(a, b)                       # a^b
pow(a, b, mod)                  # a^b % mod（快速冪，面試常用！）

# ==================== 特殊值 ====================
float('inf')                    # 正無窮大
float('-inf')                   # 負無窮大
# 用途：初始化最小值/最大值搜尋
min_val = float('inf')
max_val = float('-inf')

# ==================== 整數除法 ====================
a // b                          # Floor division（向下取整）
a % b                           # 模數（餘數）
divmod(a, b)                    # (a // b, a % b) 一次算兩個

# ==================== 進階 ====================
math.gcd(a, b)                  # 最大公因數 GCD
math.lcm(a, b)                  # 最小公倍數 LCM（Python 3.9+）
math.isqrt(n)                   # 整數平方根（Python 3.8+）
math.sqrt(n)                    # 浮點平方根
math.log2(n)                    # 以 2 為底的 log
math.log10(n)                   # 以 10 為底的 log
math.ceil(x)                    # 向上取整
math.floor(x)                   # 向下取整
math.factorial(n)               # n!

# ==================== 向上取整的面試技巧 ====================
# ceil(a / b) 的整數版本（避免浮點誤差）
result = (a + b - 1) // b       # ← 面試常用！
# 等價於 math.ceil(a / b)，但不需要 import math 也不會有浮點問題
```

### 2.4 Bit Manipulation（位元操作）

```python
# ==================== 基本運算 ====================
a & b          # AND
a | b          # OR
a ^ b          # XOR
~a             # NOT（取反）
a << n         # 左移 n 位（等於 a * 2^n）
a >> n         # 右移 n 位（等於 a // 2^n）

# ==================== 常用技巧 ====================
x & 1          # 判斷奇偶（等於 x % 2）
x & (x - 1)   # 去掉最低位的 1（判斷是否為 2 的冪：結果為 0 就是）
x | (x + 1)   # 把最低位的 0 變 1
x ^ x          # 任何數 XOR 自己 = 0
x ^ 0          # 任何數 XOR 0 = 自己

# ==================== Python 特有 ====================
bin(x)                  # 轉二進位字串 "0b1010"
bin(x).count('1')       # 計算 1 的個數（popcount / Hamming weight）
int('1010', 2)          # 二進位字串轉整數 → 10
x.bit_length()          # 需要多少 bit 表示（例如 10 → 4）

# ==================== 面試經典：只出現一次的數字 ====================
# nums 中只有一個數字出現一次，其他都出現兩次
result = 0
for n in nums:
    result ^= n
# result 就是那個只出現一次的數字（因為 x ^ x = 0）
```

### 2.5 常用 Pattern 速查

```python
# ==================== Swap ====================
a, b = b, a                # 不需要 temp 變數！

# ==================== Multiple Assignment ====================
x = y = z = 0
left, right = 0, len(arr) - 1

# ==================== Ternary Expression ====================
result = a if condition else b
# 等價於 C 的 result = condition ? a : b

# ==================== Infinity ====================
INF = float('inf')

# ==================== Matrix Directions ====================
# 4-directional（上下左右）
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# 8-directional（包含對角線）
directions = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]

# 使用方式
for dx, dy in directions:
    nx, ny = x + dx, y + dy
    if 0 <= nx < rows and 0 <= ny < cols:
        # (nx, ny) 是合法的鄰居
        pass

# ==================== Enumerate ====================
for i, val in enumerate(arr):          # i = index, val = value
    pass
for i, val in enumerate(arr, start=1): # index 從 1 開始

# ==================== Zip ====================
for a, b in zip(list1, list2):         # 同時遍歷兩個 list
    pass
# zip 以較短的為準；用 zip_longest 以較長的為準
from itertools import zip_longest
for a, b in zip_longest(list1, list2, fillvalue=0):
    pass

# ==================== Any / All ====================
any(x > 0 for x in arr)    # 至少一個 > 0？
all(x > 0 for x in arr)    # 全部 > 0？

# ==================== Map / Filter ====================
list(map(int, input().split()))    # 把輸入轉成 int list
list(filter(lambda x: x > 0, arr))  # 過濾正數
```

---

## 第三章：Python 面試陷阱（Gotchas）

這些是面試中最容易犯的錯誤，踩到一個可能就 GG。

### 陷阱 1：sort() 回傳 None

```python
# 錯誤 ✗
arr = arr.sort()       # arr 變成 None！因為 sort() 回傳 None

# 正確 ✓
arr.sort()             # in-place 排序，直接修改 arr
new_arr = sorted(arr)  # 回傳新 list，原 arr 不變
```

### 陷阱 2：List 是 reference，不是 copy

```python
# 錯誤 ✗
arr2 = arr1            # arr2 和 arr1 指向同一個 list！

# 正確 ✓
arr2 = arr1[:]         # 淺複製
arr2 = arr1.copy()     # 淺複製
arr2 = list(arr1)      # 淺複製

# 深複製（nested list 時需要）
import copy
arr2 = copy.deepcopy(arr1)
```

### 陷阱 3：2D Array 共享 reference

```python
# 錯誤 ✗（前面已提過，這裡再強調）
grid = [[0] * n] * m      # m 行共享同一個 list！

# 正確 ✓
grid = [[0] * n for _ in range(m)]
```

### 陷阱 4：負數的整數除法

```python
# Python 的 // 是「向下取整」，不是「向零取整」！
-7 // 2    # = -4（向下取整，往負無窮方向）
int(-7/2)  # = -3（向零取整，這是 C/Java 的行為）

# 面試中如果需要跟 C/Java 一致的行為：
# 用 int(a / b) 而不是 a // b
```

### 陷阱 5：String 是 immutable

```python
s = "hello"
# s[0] = 'H'  ← TypeError: 'str' object does not support item assignment

# 正確做法
chars = list(s)
chars[0] = 'H'
s = ''.join(chars)
```

### 陷阱 6：heapq 只有 Min Heap

```python
# Python 的 heapq 沒有 Max Heap！

# 模擬 Max Heap：所有值取負
import heapq
max_heap = []
heapq.heappush(max_heap, -val)     # push 時取負
top = -heapq.heappop(max_heap)     # pop 時取負回來
peek = -max_heap[0]                 # peek 時也要取負

# 如果是 tuple，只對排序 key 取負
heapq.heappush(max_heap, (-freq, word))  # 按頻率 max heap
```

### 陷阱 7：Recursion Limit

```python
import sys
sys.setrecursionlimit(10**6)   # 預設只有 1000！Deep recursion 會 crash

# 更好的做法：用 iterative + stack 取代 recursion
# 特別是在 DFS 中，用 explicit stack 更安全
```

### 陷阱 8：Mutable Default Argument

```python
# 錯誤 ✗
def add_item(item, lst=[]):   # 這個 [] 在所有呼叫間共享！
    lst.append(item)
    return lst

add_item(1)  # [1]
add_item(2)  # [1, 2]  ← 不是 [2]！因為用了同一個 list

# 正確 ✓
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 陷阱 9：for loop 中修改 list

```python
# 錯誤 ✗
for x in arr:
    if some_condition(x):
        arr.remove(x)     # 邊遍歷邊修改，會跳過元素！

# 正確 ✓
arr = [x for x in arr if not some_condition(x)]
# 或者
new_arr = []
for x in arr:
    if not some_condition(x):
        new_arr.append(x)
```

### 陷阱 10：deque O(1) vs list O(n)

```python
from collections import deque

# BFS 時用 deque，不要用 list！
queue = deque()
queue.append(x)          # O(1)
queue.popleft()           # O(1) ← 面試必須用這個！

# 如果用 list：
queue = []
queue.append(x)           # O(1)
queue.pop(0)              # O(n) ← 面試會被扣分！
```

---

## 第四章：面試程式碼風格

面試官看的不只是正確性，還有你的 **code quality**。

### 4.1 命名規範

```python
# ===== 好的命名 =====
left, right = 0, len(nums) - 1    # Two Pointer 的左右指標
slow, fast = head, head             # Fast & Slow Pointer
curr, prev, nxt = head, None, None  # Linked List 遍歷（注意：next 是保留字！）
rows, cols = len(grid), len(grid[0])  # Matrix 的行列
parent = {}                         # Union-Find 的 parent map

# ===== 不好的命名 =====
l, r = 0, len(nums) - 1            # l 太像 1，容易混淆
i, j = 0, len(nums) - 1            # 不如用 left, right 有意義
n = head                            # n 是什麼？
```

### 4.2 Edge Case 放在最前面

```python
def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Edge case first!
    if not head or not head.next:
        return head

    # Main logic
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

### 4.3 Helper Function（拆分邏輯）

```python
# 當主函式太複雜時，拆出 helper function
def solve(self, board):
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        """把邊界連通的 'O' 標記為 '#'"""
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = '#'
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc)

    # Step 1: 從邊界 DFS
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows-1 or c == 0 or c == cols-1) and board[r][c] == 'O':
                dfs(r, c)

    # Step 2: 翻轉
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == '#':
                board[r][c] = 'O'
```

### 4.4 Type Hints（加分項）

```python
from typing import List, Optional, Dict, Set, Tuple

def twoSum(self, nums: List[int], target: int) -> List[int]:
    pass

def isValid(self, s: str) -> bool:
    pass

def maxProfit(self, prices: List[int]) -> int:
    pass
```

面試時不強制要求 type hints，但寫了會讓面試官覺得你注重程式碼品質。

### 4.5 Docstring（簡短說明）

```python
def binary_search(arr: List[int], target: int) -> int:
    """Return index of target in sorted array, or -1 if not found."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2   # 避免 overflow（雖然 Python 不會）
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 第五章：面試實戰速查表

### 5.1 一秒鐘選對資料結構

```
需求                                    → 用什麼
─────────────────────────────────────────────────────
O(1) 查找某個值是否存在                   → set 或 dict
O(1) 查找 key 對應的 value               → dict
計數                                     → Counter 或 defaultdict(int)
分組                                     → defaultdict(list)
需要排序的資料 + 快速找 min/max           → heapq
需要 FIFO（先進先出）                     → deque
需要 LIFO（後進先出）                     → list（當 stack 用）
需要排序的 list + O(log n) 查找           → bisect + sorted list
需要去重                                  → set
需要保持插入順序 + 去重                   → dict（Python 3.7+ 保持順序）
```

### 5.2 一秒鐘選對內建函式

```
目標                          → 用什麼
──────────────────────────────────────────────────
排序（修改原 list）            → arr.sort()
排序（不修改原 list）          → sorted(arr)
反轉（修改原 list）            → arr.reverse()
反轉（不修改原 list）          → arr[::-1]
找最大值                       → max(arr)
找最小值                       → min(arr)
找最大值的 index               → arr.index(max(arr))
找前 k 大                      → heapq.nlargest(k, arr)
計數                           → Counter(arr)
去重                           → set(arr)
累積和                         → itertools.accumulate(arr)
二分搜尋                       → bisect.bisect_left(arr, x)
全排列                         → itertools.permutations(arr)
組合                           → itertools.combinations(arr, k)
```

### 5.3 時間複雜度速查

```
操作                              時間複雜度
──────────────────────────────────────────────
list.append()                     O(1) amortized
list.pop()                        O(1)
list.pop(0)                       O(n) ← 用 deque!
list[i]                           O(1)
list.insert(i, x)                O(n)
list.sort()                       O(n log n)
x in list                         O(n)

dict[key]                         O(1) average
key in dict                       O(1) average
dict.get(key)                     O(1) average

set.add()                         O(1) average
x in set                          O(1) average ← 比 list 快！

deque.append()                    O(1)
deque.appendleft()                O(1)
deque.popleft()                   O(1) ← 比 list.pop(0) 快！

heapq.heappush()                  O(log n)
heapq.heappop()                   O(log n)
heapq.heapify()                   O(n)

bisect.bisect_left()              O(log n)
bisect.insort()                   O(n)（因為要移動元素）

sorted()                          O(n log n)
min(), max(), sum()               O(n)
```

### 5.4 LeetCode 常見模板

```python
# ==================== Two Sum Pattern ====================
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

# ==================== Sliding Window ====================
def max_subarray_sum_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

# ==================== DFS on Tree ====================
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# ==================== BFS on Graph ====================
def bfs_shortest_path(graph, start, end):
    from collections import deque
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1

# ==================== Binary Search ====================
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# ==================== Union-Find ====================
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

---

## 第六章：Python 版本差異速查（面試偶爾會問）

```
功能                              最低版本     說明
─────────────────────────────────────────────────────────
f-string                          3.6         f"hello {name}"
dict 保持插入順序                   3.7         不需要 OrderedDict
math.isqrt()                      3.8         整數平方根
accumulate(initial=)              3.8         prefix sum 帶初始值
math.lcm()                        3.9         最小公倍數
dict union operator |             3.9         d1 | d2 合併 dict
match-case (pattern matching)     3.10        像 switch-case
```

**面試時**：Google / NVIDIA 通常用 Python 3.8+，上面列的大部分都能用。如果不確定，問面試官。

---

## 附錄：一頁速查卡（面試前 10 分鐘看這頁）

```
from collections import deque, defaultdict, Counter, OrderedDict
from heapq import heappush, heappop, heapify, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from itertools import permutations, combinations, product, accumulate
from functools import cmp_to_key, lru_cache
from typing import List, Optional
import math, sys

# 面試開頭可能要加
sys.setrecursionlimit(10**6)

# 記住
# sort() 回傳 None，sorted() 回傳新 list
# heapq 只有 min heap，max heap 用負數
# string immutable → list(s) 操作 → ''.join()
# [[0]*n]*m 共享 → [[0]*n for _ in range(m)]
# -7//2 = -4（Python 向下取整），int(-7/2) = -3（向零取整）
# deque.popleft() O(1)，list.pop(0) O(n)
# set/dict 查找 O(1)，list 查找 O(n)
# bisect 在 sorted list 上做 O(log n) 搜尋
# Counter 取不存在的 key 回傳 0，不會 Error
# directions = [(0,1),(0,-1),(1,0),(-1,0)]
```
