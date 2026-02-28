# LeetCode 教學筆記 #04 — Stack, Queue & Monotonic Stack

> **堆疊、佇列與單調堆疊 — 從零開始的完整教學**
>
> Target: Google 面試準備 | Level: Beginner → Intermediate
>
> 本文每個概念都有 **完整的逐步數值追蹤**，包含 stack/queue 在每一步操作後的狀態。
> 基礎薄弱的讀者請務必用紙筆跟著追蹤一遍。

---

## 目錄

| 章 | 主題 | 重要度 |
|----|------|--------|
| 1 | Stack 與 Queue 基礎 | ★★★★★ |
| 2 | 基礎 Stack 題目 (LC 20, 155, 150) | ★★★★☆ |
| 3 | 單調棧 Monotonic Stack (LC 496, 739, 84) | ★★★★★ |
| 4 | Stack 模擬型 (LC 394, 227) | ★★★★☆ |
| 5 | 單調隊列 Monotonic Deque (LC 239) | ★★★★★ |
| 6 | 比較與決策框架 | ★★★★☆ |

---

# 第一章：Stack 與 Queue 基礎

## 1.1 Stack（堆疊）— LIFO (Last In, First Out)

**生活比喻：疊盤子** — 你在餐廳把盤子一個一個疊起來。要拿盤子時只能拿最上面那個。最後放上去的盤子最先被拿走，這就是 LIFO。

```
    ┌─────────┐
    │    C    │  ← top（最後放入，最先取出）
    ├─────────┤
    │    B    │
    ├─────────┤
    │    A    │  ← bottom（最先放入，最後取出）
    └─────────┘

    push(A) → push(B) → push(C)
    pop() → 取出 C
    pop() → 取出 B
    pop() → 取出 A
```

### 核心操作（全部 O(1)）

| 操作 | 說明 | Python (list) |
|------|------|---------------|
| `push(x)` | 將 x 放到頂端 | `stack.append(x)` |
| `pop()` | 移除並回傳頂端元素 | `stack.pop()` |
| `peek()` / `top()` | 查看頂端元素（不移除）| `stack[-1]` |
| `isEmpty()` | 是否為空 | `len(stack) == 0` |

### 範例追蹤 1：push/pop 基本操作

```
操作序列：push(10), push(20), push(30), pop(), peek(), pop()

Step 1: push(10)
  stack: [10]
         ^^^^
         top

Step 2: push(20)
  stack: [10, 20]
               ^^
               top

Step 3: push(30)
  stack: [10, 20, 30]
                   ^^
                   top

Step 4: pop() → 回傳 30
  stack: [10, 20]
               ^^
               top

Step 5: peek() → 回傳 20（不移除）
  stack: [10, 20]    ← 沒變
               ^^
               top

Step 6: pop() → 回傳 20
  stack: [10]
         ^^
         top
```

### 範例追蹤 2：空 stack 操作

```
操作序列：push(5), pop(), pop(), push(7), peek()

Step 1: push(5)       → stack: [5]
Step 2: pop() → 5     → stack: []    ← 空了！
Step 3: pop() → ERROR!  stack 為空（Python 拋出 IndexError）
  ※ 面試中一定要先檢查 isEmpty()
Step 4: push(7)       → stack: [7]
Step 5: peek() → 7    → stack: [7]   ← 沒變
```

### Python 實作

```python
# Python 用 list 當 stack（最自然的方式）
stack = []
stack.append(10)    # push
stack.append(20)    # push
val = stack.pop()   # pop → 20
top = stack[-1]     # peek → 10
is_empty = len(stack) == 0  # False
```

---

## 1.2 Queue（佇列）— FIFO (First In, First Out)

**生活比喻：排隊買票** — 先來的人先買票離開，後來的人排在後面等。

```
    enqueue（排隊加入）
         ↓
  ┌──┬──┬──┬──┐
  │ A│ B│ C│ D│  → dequeue（離開）
  └──┴──┴──┴──┘     先進先出：A 先離開
  back          front
  （隊尾）      （隊頭）
```

### 核心操作（全部 O(1)）

| 操作 | 說明 | Python (deque) |
|------|------|----------------|
| `enqueue(x)` | 加到隊尾 | `q.append(x)` |
| `dequeue()` | 移除並回傳隊頭 | `q.popleft()` |
| `front()` | 查看隊頭（不移除）| `q[0]` |
| `isEmpty()` | 是否為空 | `len(q) == 0` |

> **重要**：Python 的 `list.pop(0)` 是 O(n)！
> 要用 `collections.deque` 才能做到 O(1) 的 `popleft()`。

### 範例追蹤 1：enqueue/dequeue 基本操作

```
操作序列：enqueue(A), enqueue(B), enqueue(C), dequeue(), front(), dequeue()

Step 1: enqueue(A)
  queue: [A]
  front=A, back=A

Step 2: enqueue(B)
  queue: [A, B]
  front=A, back=B

Step 3: enqueue(C)
  queue: [A, B, C]
  front=A, back=C

Step 4: dequeue() → 回傳 A
  queue: [B, C]
  front=B, back=C

Step 5: front() → 回傳 B（不移除）
  queue: [B, C]    ← 沒變

Step 6: dequeue() → 回傳 B
  queue: [C]
  front=C, back=C
```

### Python 實作

```python
from collections import deque

q = deque()
q.append(10)       # enqueue
q.append(20)       # enqueue
val = q.popleft()  # dequeue → 10（O(1)！）
front = q[0]       # front → 20
is_empty = len(q) == 0  # False
```

---

## 1.3 Stack vs Queue — 何時用哪個？

> 需要「反轉順序 / 後進先出 / 配對匹配 / 巢狀結構」→ **Stack**
> 需要「保持順序 / 先進先出 / 層序遍歷 / 排隊處理」→ **Queue**

| 特性 | Stack (LIFO) | Queue (FIFO) |
|------|-------------|--------------|
| 順序 | 反轉 | 保持 |
| 典型應用 | 括號匹配、DFS、遞迴模擬、undo | BFS、層序遍歷、排程 |
| Python | `list` | `collections.deque` |

---

# 第二章：基礎 Stack 題目

## 2.1 Valid Parentheses — LeetCode 20（Easy）

### 題目

給一個只包含 `(`, `)`, `{`, `}`, `[`, `]` 的字串，判斷括號是否合法。核心觀念：

- 遇到**左括號** → push 進 stack
- 遇到**右括號** → pop stack 頂端，檢查是否匹配
- 最後 stack 為空 → 合法

```
配對關係：
  ')' 配對 '('
  '}' 配對 '{'
  ']' 配對 '['
```

### 範例 1："({[]})" → True（合法）

```
字串：( { [ ] } )
位置：0 1 2 3 4 5

Step 0: char='('  → 左括號 → push
  stack: ['(']

Step 1: char='{'  → 左括號 → push
  stack: ['(', '{']

Step 2: char='['  → 左括號 → push
  stack: ['(', '{', '[']

Step 3: char=']'  → 右括號 → pop 得到 '['，']' 配 '[' ✓
  stack: ['(', '{']

Step 4: char='}'  → 右括號 → pop 得到 '{'，'}' 配 '{' ✓
  stack: ['(']

Step 5: char=')'  → 右括號 → pop 得到 '('，')' 配 '(' ✓
  stack: []

最終 stack 為空 → return True ✓
```

### 範例 2："([)]" → False（不合法）

```
字串：( [ ) ]
位置：0 1 2 3

Step 0: char='('  → 左括號 → push
  stack: ['(']

Step 1: char='['  → 左括號 → push
  stack: ['(', '[']

Step 2: char=')'  → 右括號 → pop 得到 '['
  ')' 需要配 '('，但拿到 '[' → 不匹配！
  → return False ✗

問題出在：交叉嵌套 ([)] 是不合法的
正確的應該是：([]) 或 ([]())
```

### Corner Cases

```
1. 奇數長度 → 一定不合法（直接 return False 作為優化）
   例如 "(()" → 長度 3

2. 只有左括號 "(((" → stack 不為空 → False

3. 只有右括號 ")))" → pop 時 stack 為空 → False

4. 空字串 "" → stack 為空 → True
```

### 程式碼

```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:              # 右括號
            top = stack.pop() if stack else '#'
            if top != mapping[char]:
                return False
        else:                            # 左括號
            stack.append(char)

    return len(stack) == 0
```

**Time: O(n) | Space: O(n)**

---

## 2.2 Min Stack — LeetCode 155（Medium）

### 題目

設計一個 stack，除了 push/pop/top 之外，還要支援 `getMin()` — 回傳目前 stack 中的最小值。**所有操作都要 O(1)**。

**核心觀念**：用一個輔助 stack（min_stack），同步記錄「到目前為止的最小值」。

```
main_stack:  每次 push/pop 元素
min_stack:   每次 push 時，記錄 min(新值, 當前最小值)
             每次 pop 時，同步 pop

兩個 stack 永遠保持相同高度！
```

### 範例 1：push(-2), push(0), push(-3), getMin(), pop(), getMin()

```
操作：push(-2)
  main_stack: [-2]
  min_stack:  [-2]     ← min(-2) = -2
  getMin() = -2

操作：push(0)
  main_stack: [-2, 0]
  min_stack:  [-2, -2]  ← min(0, -2) = -2
  getMin() = -2

操作：push(-3)
  main_stack: [-2, 0, -3]
  min_stack:  [-2, -2, -3]  ← min(-3, -2) = -3
  getMin() = -3

操作：getMin()
  → 回傳 min_stack 頂端 = -3 ✓

操作：pop()
  main_stack: [-2, 0]      ← 移除 -3
  min_stack:  [-2, -2]     ← 同步移除 -3
  getMin() = -2            ← 自動恢復！

操作：getMin()
  → 回傳 min_stack 頂端 = -2 ✓
```

### 範例 2：push(1), push(1), push(2), getMin(), pop(), getMin()

```
操作：push(1)
  main_stack: [1]
  min_stack:  [1]      ← min(1) = 1

操作：push(1)
  main_stack: [1, 1]
  min_stack:  [1, 1]   ← min(1, 1) = 1（重複值也要記錄！）

操作：push(2)
  main_stack: [1, 1, 2]
  min_stack:  [1, 1, 1]  ← min(2, 1) = 1

操作：getMin() → 1 ✓

操作：pop()            ← 移除 2
  main_stack: [1, 1]
  min_stack:  [1, 1]

操作：getMin() → 1 ✓   ← 還有一個 1，最小值不變

※ 重點：如果 min_stack 只存「嚴格更小」的值，pop(1) 後會出錯！
   所以 min_stack 必須存 <= 的值（或像這裡每層都存當前最小值）。
```

### 程式碼

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        cur_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(cur_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

**Time: O(1) per operation | Space: O(n)**

---

## 2.3 Evaluate Reverse Polish Notation — LeetCode 150（Medium）

### 什麼是 RPN（逆波蘭表示法）？

一般數學式（中序 Infix）：`(2 + 1) * 3` → RPN（後序 Postfix）：`2 1 + 3 *`
RPN 的好處：不需要括號，也不需要考慮優先順序。電腦用 stack 一遍掃過就能算完。

### 核心規則

```
遇到數字 → push 進 stack
遇到運算子 → pop 兩個數，計算結果，push 回去
   ※ 注意順序：先 pop 的是右運算元(b)，再 pop 的是左運算元(a)
   ※ 計算 a op b（不是 b op a）
最後 stack 裡剩一個數就是答案
```

### 範例 1：["2", "1", "+", "3", "*"] → (2+1)*3 = 9

```
Token 1: "2" → 數字 → push
  stack: [2]

Token 2: "1" → 數字 → push
  stack: [2, 1]

Token 3: "+" → 運算子 → pop b=1, pop a=2 → 2+1=3 → push
  stack: [3]

Token 4: "3" → 數字 → push
  stack: [3, 3]

Token 5: "*" → 運算子 → pop b=3, pop a=3 → 3*3=9 → push
  stack: [9]

最終答案 = 9 ✓
```

### 範例 2：["4", "13", "5", "/", "+"] → 4+(13/5) = 6

```
Token 1: "4"  → push           → stack: [4]
Token 2: "13" → push           → stack: [4, 13]
Token 3: "5"  → push           → stack: [4, 13, 5]
Token 4: "/"  → pop b=5, a=13  → 13/5 = 2（向零取整）→ push
                                → stack: [4, 2]
Token 5: "+"  → pop b=2, a=4   → 4+2 = 6 → push
                                → stack: [6]

最終答案 = 6 ✓

※ 注意：Python 的 13//5=2，但 -13//5=-3（向下取整）
   題目要求向零取整，所以要用 int(13/5)=2, int(-13/5)=-2
```

### Corner Case：除法向零取整

Python 的 `//` 是向下取整：`-6 // 4 = -2` (錯！) 題目要向零取整：`int(-6 / 4) = -1` (正確)

### 程式碼

```python
def evalRPN(tokens: list[str]) -> int:
    stack = []
    ops = {'+', '-', '*', '/'}

    for t in tokens:
        if t in ops:
            b = stack.pop()
            a = stack.pop()
            if   t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else:          stack.append(int(a / b))  # 向零取整
        else:
            stack.append(int(t))

    return stack[0]
```

**Time: O(n) | Space: O(n)**

---

# 第三章：單調棧 (Monotonic Stack) — 面試重點！

## 3.0 什麼是 Monotonic Stack？

**定義**：stack 中的元素**永遠保持單調遞增或單調遞減**的順序。

```
單調遞減 stack（從 bottom 到 top 遞減）：
    ┌───┐
    │ 2 │  ← top（最小）
    ├───┤
    │ 5 │
    ├───┤
    │ 8 │  ← bottom（最大）
    └───┘
    8 > 5 > 2 → 遞減 ✓

如果要 push 6：
    6 > top(2) → pop 2
    6 > top(5) → pop 5
    push 6
    ┌───┐
    │ 6 │  ← top
    ├───┤
    │ 8 │  ← bottom
    └───┘
    8 > 6 → 仍然遞減 ✓
```

### 為什麼是 O(n)？

看起來 for loop 裡面有 while loop → O(n^2)？實際上每個元素最多被 push 一次、pop 一次。n 次 push + 最多 n 次 pop = 2n 次操作 → **攤銷 O(n)**。

面試必問："Why is this O(n)?" → "Each element is pushed and popped at most once. Total operations = 2n = O(n)."

### 核心 Pattern：尋找 "Next Greater / Smaller Element"

暴力法每個元素往右掃 → O(n^2)。單調棧一次掃描 → O(n)。

---

## 3.1 Next Greater Element I — LeetCode 496（Easy）

### 題目

給 `nums1`（是 `nums2` 的子集）和 `nums2`。
對 `nums1` 中每個元素，找到它在 `nums2` 中的位置，然後找右邊第一個比它大的元素。
找不到回傳 -1。

### 核心思路

1. 先用 monotonic stack 對 `nums2` 建立一個 map：`{元素: 下一個更大的元素}`
2. 然後直接查表回答 `nums1`

**方向：從右到左掃描 nums2，維護一個「單調遞減 stack」**

```
為什麼從右到左？
因為我們要找每個元素「右邊」第一個更大的元素。
從右到左掃，stack 裡存的就是「右邊還活著的候選人」。

為什麼遞減？
如果 stack 裡有一個小的值 x 壓在大的值 y 下面，
那 x 永遠不可能是任何人的 "next greater"（因為 y 比 x 大且更近）。
所以 x 應該被 pop 掉 → 只留遞減序列。
```

### 範例 1：nums1=[4,1,2], nums2=[1,3,4,2]

```
Step 1: 對 nums2 從右到左掃描，建立 next greater map

  i=3, val=2:
    stack=[]（空）→ nge[2]=-1（右邊沒有更大的）
    push 2 → stack=[2]

  i=2, val=4:
    stack=[2], top=2, 2<=4 → pop 2
    stack=[]（空）→ nge[4]=-1
    push 4 → stack=[4]

  i=1, val=3:
    stack=[4], top=4, 4>3 → 不 pop
    nge[3]=4（stack 頂就是 next greater）
    push 3 → stack=[4, 3]

  i=0, val=1:
    stack=[4, 3], top=3, 3>1 → 不 pop
    nge[1]=3
    push 1 → stack=[4, 3, 1]

Step 2: 建立好的 map = {2:-1, 4:-1, 3:4, 1:3}

Step 3: 查表
  nums1=[4, 1, 2]
  → [nge[4], nge[1], nge[2]]
  → [-1, 3, -1] ✓
```

### 範例 2：nums1=[2,4], nums2=[1,2,3,4]

```
對 nums2=[1,2,3,4] 從右到左掃描：

  i=3, val=4:
    stack=[] → nge[4]=-1
    push 4 → stack=[4]

  i=2, val=3:
    stack=[4], top=4>3 → 不 pop
    nge[3]=4
    push 3 → stack=[4, 3]

  i=1, val=2:
    stack=[4, 3], top=3>2 → 不 pop
    nge[2]=3
    push 2 → stack=[4, 3, 2]

  i=0, val=1:
    stack=[4, 3, 2], top=2>1 → 不 pop
    nge[1]=2
    push 1 → stack=[4, 3, 2, 1]

map = {4:-1, 3:4, 2:3, 1:2}

nums1=[2, 4] → [nge[2], nge[4]] → [3, -1] ✓
```

### 程式碼

```python
def nextGreaterElement(nums1: list[int], nums2: list[int]) -> list[int]:
    stack = []
    nge = {}  # next greater element map

    for i in range(len(nums2) - 1, -1, -1):
        val = nums2[i]
        while stack and stack[-1] <= val:
            stack.pop()
        nge[val] = stack[-1] if stack else -1
        stack.append(val)

    return [nge[x] for x in nums1]
```

**Time: O(n+m) | Space: O(n)**（n = len(nums2), m = len(nums1)）

---

## 3.2 Daily Temperatures — LeetCode 739（Medium）

### 題目

給一個每日溫度陣列 `temperatures`，回傳一個陣列：
每一天要等幾天才會有更高的溫度。等不到就是 0。

### 核心思路

**Stack 存 index（不是值！），維護「單調遞減 stack」（溫度從 bottom 到 top 遞減）。**

```
為什麼存 index？
因為答案要的是「天數差」，需要 index 來計算 i - prev_idx。

從左到右掃描：
  遇到更高溫度 → pop 出那些「在等更高溫」的 index，算天數差
  否則 → push 當前 index
```

### 範例 1：[73, 74, 75, 71, 69, 72, 76, 73]

```
index:  0   1   2   3   4   5   6   7
temp:  73  74  75  71  69  72  76  73
ans:    ?   ?   ?   ?   ?   ?   ?   ?

i=0, temp=73:
  stack 為空 → push 0
  stack(idx): [0]    stack(temp): [73]

i=1, temp=74:
  74 > stack top temp 73 → pop idx=0
    result[0] = 1 - 0 = 1  （等 1 天）
  stack 為空 → push 1
  stack(idx): [1]    stack(temp): [74]

i=2, temp=75:
  75 > stack top temp 74 → pop idx=1
    result[1] = 2 - 1 = 1  （等 1 天）
  stack 為空 → push 2
  stack(idx): [2]    stack(temp): [75]

i=3, temp=71:
  71 < stack top temp 75 → 不 pop → push 3
  stack(idx): [2, 3]    stack(temp): [75, 71]

i=4, temp=69:
  69 < stack top temp 71 → 不 pop → push 4
  stack(idx): [2, 3, 4]    stack(temp): [75, 71, 69]

i=5, temp=72:
  72 > stack top temp 69 → pop idx=4
    result[4] = 5 - 4 = 1  （等 1 天）
  72 > stack top temp 71 → pop idx=3
    result[3] = 5 - 3 = 2  （等 2 天）
  72 < stack top temp 75 → 不 pop → push 5
  stack(idx): [2, 5]    stack(temp): [75, 72]

i=6, temp=76:
  76 > stack top temp 72 → pop idx=5
    result[5] = 6 - 5 = 1  （等 1 天）
  76 > stack top temp 75 → pop idx=2
    result[2] = 6 - 2 = 4  （等 4 天）
  stack 為空 → push 6
  stack(idx): [6]    stack(temp): [76]

i=7, temp=73:
  73 < stack top temp 76 → 不 pop → push 7
  stack(idx): [6, 7]    stack(temp): [76, 73]

掃描結束。stack 裡剩餘的 index 表示「等不到更高溫」→ result 保持 0。

最終 result = [1, 1, 4, 2, 1, 1, 0, 0] ✓
```

### 範例 2：[30, 40, 50, 60]（持續上升）

```
index: 0   1   2   3
temp: 30  40  50  60

i=0, temp=30:
  push 0 → stack: [0]

i=1, temp=40:
  40>30 → pop idx=0, result[0]=1-0=1
  push 1 → stack: [1]

i=2, temp=50:
  50>40 → pop idx=1, result[1]=2-1=1
  push 2 → stack: [2]

i=3, temp=60:
  60>50 → pop idx=2, result[2]=3-2=1
  push 3 → stack: [3]

剩餘 idx=3 → result[3]=0

result = [1, 1, 1, 0] ✓

觀察：持續上升時，每個元素都只在 stack 待一步就被 pop。
```

### Corner Cases

```
1. 全部遞減 [60,50,40,30] → 沒有人能 pop 別人 → result=[0,0,0,0]
2. 全部相同 [50,50,50,50] → 相等不算「更高」→ result=[0,0,0,0]
3. 只有一天 [42] → result=[0]
```

### 程式碼

```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存 index

    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result
```

**Time: O(n) | Space: O(n)**

---

## 3.3 Largest Rectangle in Histogram — LeetCode 84（Hard）

### 這是 Google 面試經典 Hard 題！

### 題目

給一個直方圖（每個 bar 寬度 = 1），求最大矩形面積。

```
heights = [2, 1, 5, 6, 2, 3]

     ┌───┐
     │   │
  ┌──┤   │
  │  │   │         ┌───┐
  │  │   ├───┐     │   │
──┤  │   │   ├──┬──┤   │──
  │  │   │   │  │  │   │
──┤  ├───┤   ├──┤  ├───┤──
  │  │   │   │  │  │   │
──┴──┴───┴───┴──┴──┴───┴──
  2    1   5   6   2   3

最大矩形 = 5*2 = 10（高度 5，跨越 index 2-3）
```

### 為什麼這題難？

對每個 bar，要找「以它為高度的最大矩形」：
- 往左擴展到第一個「比它矮」的 bar → left boundary
- 往右擴展到第一個「比它矮」的 bar → right boundary
- **width = right - left - 1**
- **area = height * width**

暴力法對每個 bar 左右掃描 → O(n^2)。
Monotonic Stack → O(n)。

### 核心觀念

**維護一個「單調遞增 stack」（從 bottom 到 top 高度遞增）。**

```
stack 存 index。
當遇到比 stack 頂更矮的 bar 時：
  - pop 出 stack 頂（這個 bar 的右邊界就是當前位置 i）
  - pop 後的新 stack 頂就是左邊界
  - 計算面積

為什麼用遞增 stack？
  → 遞增 stack 中，每個元素的左邊界就是它下面那個元素。
  → 當一個更矮的 bar 出現，它就是右邊界。
```

### 關鍵公式

```
pop 出 index=j 時，heights[j] = h
  右邊界 = i（觸發 pop 的位置）
  左邊界 = stack[-1]（pop 後的新 stack 頂）

  ◆ 如果 stack 非空：width = i - stack[-1] - 1
  ◆ 如果 stack 為空：width = i（從最左邊延伸到 i-1）

  area = h * width
```

### 哨兵技巧

在 `heights` 結尾加上一個高度 0 的虛擬 bar，確保最後 stack 裡所有元素都能被 pop 出來計算面積。

### 範例 2（先看簡單的）：heights = [2, 4]

```
index:   0  1  (2=哨兵)
heights: 2  4  0

i=0, cur_h=2:
  stack=[] → push 0
  stack: [0]  heights: [2]

i=1, cur_h=4:
  4 > heights[0]=2 → 不 pop → push 1
  stack: [0, 1]  heights: [2, 4]

i=2, cur_h=0（哨兵）:
  0 < heights[1]=4 → pop idx=1
    h=4, stack=[0], w = 2-0-1 = 1
    area = 4*1 = 4, max_area = 4
  0 < heights[0]=2 → pop idx=0
    h=2, stack=[], w = 2（stack 為空，從最左延伸）
    area = 2*2 = 4, max_area = 4
  push 2 → stack: [2]

最大面積 = 4 ✓

解釋：高度 4、寬度 1 的矩形 (area=4)
      或 高度 2、寬度 2 的矩形 (area=4)
      兩者一樣大。
```

### 範例 1（完整）：heights = [2, 1, 5, 6, 2, 3]

```
index:   0  1  2  3  4  5  (6=哨兵)
heights: 2  1  5  6  2  3  0

i=0, cur_h=2:
  stack=[] → push 0
  stack: [0]  heights: [2]

i=1, cur_h=1:
  1 < heights[0]=2 → pop idx=0
    h=2, stack=[], w=1 (stack 為空)
    area = 2*1 = 2, max_area = 2
  push 1 → stack: [1]  heights: [1]

i=2, cur_h=5:
  5 > heights[1]=1 → 不 pop → push 2
  stack: [1, 2]  heights: [1, 5]

i=3, cur_h=6:
  6 > heights[2]=5 → 不 pop → push 3
  stack: [1, 2, 3]  heights: [1, 5, 6]

i=4, cur_h=2:
  2 < heights[3]=6 → pop idx=3
    h=6, stack=[1,2], w = 4-2-1 = 1
    area = 6*1 = 6, max_area = 6
  2 < heights[2]=5 → pop idx=2
    h=5, stack=[1], w = 4-1-1 = 2
    area = 5*2 = 10, max_area = 10  ← 這就是答案！
  2 > heights[1]=1 → 不 pop → push 4
  stack: [1, 4]  heights: [1, 2]

i=5, cur_h=3:
  3 > heights[4]=2 → 不 pop → push 5
  stack: [1, 4, 5]  heights: [1, 2, 3]

i=6, cur_h=0（哨兵）:
  0 < heights[5]=3 → pop idx=5
    h=3, stack=[1,4], w = 6-4-1 = 1
    area = 3*1 = 3, max_area = 10
  0 < heights[4]=2 → pop idx=4
    h=2, stack=[1], w = 6-1-1 = 4
    area = 2*4 = 8, max_area = 10
  0 < heights[1]=1 → pop idx=1
    h=1, stack=[], w = 6 (stack 為空)
    area = 1*6 = 6, max_area = 10
  push 6 → stack: [6]

最大面積 = 10 ✓

最大矩形視覺化：
     ┌───┐
     │   │
  ┌──┤   │
  │xxxxxxx│         ┌───┐
  │xxxxxxx├───┐     │   │
──┤  │xxx│   ├──┬──┤   │──
  │  │xxx│   │  │  │   │
──┤  ├xxx┤   ├──┤  ├───┤──
  │  │xxx│   │  │  │   │
──┴──┴───┴───┴──┴──┴───┴──
  2    1  [5] [6]  2   3

高度 5，從 index 2 到 index 3，寬度 2
面積 = 5 * 2 = 10
```

### 面積計算詳細解說

pop idx=2（h=5）時：右邊界=i=4，左邊界=stack[-1]=1，width=4-1-1=2（index 2 和 3）。
為什麼 index 3 可以包含？因為 heights[3]=6>=5，高度 5 可以延伸到 index 3。index 3 之前已被 pop（因為 6>5），代表它更高，不會限制寬度。

### Corner Cases

全部相同 `[3,3,3,3]` → 3*4=12 | 遞增 `[1,2,3,4]` → 哨兵觸發所有 pop | 遞減 `[4,3,2,1]` → 每步都 pop | 單一 bar `[5]` → 5

### 程式碼

```python
def largestRectangleArea(heights: list[int]) -> int:
    stack = []
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        cur_h = heights[i] if i < n else 0  # 哨兵

        while stack and cur_h < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * w)

        stack.append(i)

    return max_area
```

**Time: O(n) | Space: O(n)**

---

# 第四章：Stack 模擬型

## 4.1 Decode String — LeetCode 394（Medium）

### 題目

解碼字串，規則：`k[encoded_string]` → 將 `encoded_string` 重複 k 次。
可以巢狀：`3[a2[c]]` → `accaccacc`

### 核心觀念

用 stack 存 `(之前的字串, 重複次數)`。

```
遇到數字 → 累積數字（可能多位數，如 "12"）
遇到 '[' → 把 (current_str, current_num) push 進 stack，重置
遇到 ']' → pop 出 (prev_str, num)，組合成 prev_str + current_str * num
遇到字母 → 加到 current_str
```

### 範例 1："3[a2[c]]" → "accaccacc"

```
初始：current_str = "", current_num = 0

char='3' (digit):
  current_num = 0*10 + 3 = 3
  current_str = "", current_num = 3

char='[':
  push ("", 3) → stack = [("", 3)]
  reset: current_str = "", current_num = 0

char='a' (letter):
  current_str = "a"
  current_num = 0

char='2' (digit):
  current_num = 0*10 + 2 = 2
  current_str = "a", current_num = 2

char='[':
  push ("a", 2) → stack = [("", 3), ("a", 2)]
  reset: current_str = "", current_num = 0

char='c' (letter):
  current_str = "c"

char=']':
  pop → (prev_str="a", num=2)
  current_str = "a" + "c"*2 = "a" + "cc" = "acc"
  stack = [("", 3)]

char=']':
  pop → (prev_str="", num=3)
  current_str = "" + "acc"*3 = "accaccacc"
  stack = []

最終答案 = "accaccacc" ✓
```

### 範例 2："2[ab3[d]]ef" → "abdddabdddef"

```
初始：current_str = "", current_num = 0

char='2':  current_num = 2
char='[':  push ("", 2), reset
           stack = [("", 2)]
           current_str = "", current_num = 0

char='a':  current_str = "a"
char='b':  current_str = "ab"

char='3':  current_num = 3
char='[':  push ("ab", 3), reset
           stack = [("", 2), ("ab", 3)]
           current_str = "", current_num = 0

char='d':  current_str = "d"

char=']':  pop → ("ab", 3)
           current_str = "ab" + "d"*3 = "ab" + "ddd" = "abddd"
           stack = [("", 2)]

char=']':  pop → ("", 2)
           current_str = "" + "abddd"*2 = "abdddabddd"
           stack = []

char='e':  current_str = "abdddabddde"
char='f':  current_str = "abdddabdddef"

最終答案 = "abdddabdddef" ✓
```

### 程式碼

```python
def decodeString(s: str) -> str:
    stack = []
    current_str = ""
    current_num = 0

    for ch in s:
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)
        elif ch == '[':
            stack.append((current_str, current_num))
            current_str = ""
            current_num = 0
        elif ch == ']':
            prev_str, num = stack.pop()
            current_str = prev_str + current_str * num
        else:
            current_str += ch

    return current_str
```

**Time: O(output length) | Space: O(n)**

---

## 4.2 Basic Calculator II — LeetCode 227（Medium）

### 題目

計算一個只包含 `+`, `-`, `*`, `/` 和非負整數的表達式（可能有空格）。

例如 `"3+2*2"` → `7`

### 核心觀念：用 stack 處理運算子優先順序

```
關鍵想法：
  +/- 是低優先度 → 先把數字（帶正負號）push 進 stack，最後 sum
  *// 是高優先度 → 立刻 pop 出 stack 頂，計算完再 push 回去

用 prev_op 記錄「前一個運算子」：
  遇到新運算子（或字串結尾）時，根據 prev_op 決定怎麼處理 current_num
```

### 範例 1："3+2*2" → 7

```
初始：num=0, prev_op='+', stack=[]

i=0, ch='3' (digit): num = 3
  （不是運算子，繼續）

i=1, ch='+' (operator):
  prev_op='+' → push +3 → stack = [3]
  update: prev_op='+', num=0

i=2, ch='2' (digit): num = 2
i=3, ch='*' (operator):
  prev_op='+' → push +2 → stack = [3, 2]
  update: prev_op='*', num=0

i=4, ch='2' (digit): num = 2
  這是最後一個字元！也要觸發處理：
  prev_op='*' → pop 2, 計算 2*2=4, push 4 → stack = [3, 4]

最終：sum(stack) = sum([3, 4]) = 7 ✓

過程：3 + (2*2) = 3 + 4 = 7
stack 幫我們「延遲」了 + 的計算，讓 * 先算。
```

### 範例 2："14-3*2+11" → 19

```
初始：num=0, prev_op='+', stack=[]

ch='1': num=1
ch='4': num=14（多位數：1*10+4=14）

ch='-' (operator):
  prev_op='+' → push +14 → stack = [14]
  prev_op='-', num=0

ch='3': num=3

ch='*' (operator):
  prev_op='-' → push -3 → stack = [14, -3]
  prev_op='*', num=0

ch='2': num=2

ch='+' (operator):
  prev_op='*' → pop -3, 計算 -3*2=-6, push -6 → stack = [14, -6]
  prev_op='+', num=0

ch='1': num=1
ch='1': num=11

字串結尾：
  prev_op='+' → push +11 → stack = [14, -6, 11]

sum(stack) = 14 + (-6) + 11 = 19 ✓

解析：14 - 3*2 + 11 = 14 - 6 + 11 = 19
```

### 程式碼

```python
def calculate(s: str) -> int:
    stack = []
    num = 0
    prev_op = '+'

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)

        if ch in '+-*/' or i == len(s) - 1:
            if   prev_op == '+': stack.append(num)
            elif prev_op == '-': stack.append(-num)
            elif prev_op == '*': stack.append(stack.pop() * num)
            elif prev_op == '/': stack.append(int(stack.pop() / num))

            prev_op = ch
            num = 0

    return sum(stack)
```

**Time: O(n) | Space: O(n)**

---

# 第五章：單調隊列 (Monotonic Deque)

## 5.1 Sliding Window Maximum — LeetCode 239（Hard）— Google 高頻！

### 題目

給陣列 `nums` 和視窗大小 `k`，回傳每個滑動視窗的最大值。

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

視窗位置                   最大值
[1  3  -1] -3  5  3  6  7    3
 1 [3  -1  -3] 5  3  6  7    3
 1  3 [-1  -3  5] 3  6  7    5
 1  3  -1 [-3  5  3] 6  7    5
 1  3  -1  -3 [5  3  6] 7    6
 1  3  -1  -3  5 [3  6  7]   7

輸出：[3, 3, 5, 5, 6, 7]
```

### 為什麼不用 max heap？

Max Heap：每次加入/移除 O(log n)，需要 lazy deletion，總時間 O(n log n)。
Monotonic Deque：每個元素最多進出 deque 各一次，總時間 **O(n)**。

### 核心觀念：單調遞減 Deque

```
Deque 存 index，保持對應的值從 front 到 back 遞減。
front（隊頭）永遠是當前視窗的最大值。

三步驟（每一步都很重要）：
  1. 移除過期：如果 front 的 index 超出視窗範圍 → popleft
  2. 維護單調：從 back pop 掉所有 <= nums[i] 的元素
     （它們比新元素小又比新元素舊，永遠不可能成為最大值）
  3. 加入新元素：append 到 back
  4. 記錄答案：當視窗形成時（i >= k-1），front 就是最大值

為什麼遞減？
  如果 deque 裡有 [5, 3, 7]（非遞減），
  那 5 和 3 永遠不會是最大值（因為 7 比它們大且更新）。
  所以 5 和 3 應該被移除 → 只保留遞減序列。
```

### 範例 1：nums=[1,3,-1,-3,5,3,6,7], k=3

```
i=0, val=1:
  Step 1: deque=[], front 沒有過期的
  Step 2: deque=[], 沒東西可 pop
  Step 3: append 0 → deque=[0]
  視窗未形成（i=0 < k-1=2）
  deque(idx)=[0]  deque(val)=[1]

i=1, val=3:
  Step 1: front=0, 0 >= 1-3+1=-1 → 沒過期
  Step 2: nums[0]=1 <= 3 → pop back idx=0
          deque=[]
  Step 3: append 1 → deque=[1]
  視窗未形成（i=1 < k-1=2）
  deque(idx)=[1]  deque(val)=[3]

i=2, val=-1:
  Step 1: front=1, 1 >= 2-3+1=0 → 沒過期
  Step 2: nums[1]=3 > -1 → 不 pop（保持遞減）
  Step 3: append 2 → deque=[1, 2]
  ★ 視窗形成！max = nums[deque[0]] = nums[1] = 3
  deque(idx)=[1, 2]  deque(val)=[3, -1]  window=[1,3,-1]  → max=3

i=3, val=-3:
  Step 1: front=1, 1 >= 3-3+1=1 → 沒過期
  Step 2: nums[2]=-1 > -3 → 不 pop
  Step 3: append 3 → deque=[1, 2, 3]
  ★ max = nums[1] = 3
  deque(idx)=[1, 2, 3]  deque(val)=[3, -1, -3]  window=[3,-1,-3]  → max=3

i=4, val=5:
  Step 1: front=1, 1 >= 4-3+1=2? → 1 < 2 → 過期！popleft
          deque=[2, 3]
  Step 2: nums[3]=-3 <= 5 → pop back idx=3 → deque=[2]
          nums[2]=-1 <= 5 → pop back idx=2 → deque=[]
  Step 3: append 4 → deque=[4]
  ★ max = nums[4] = 5
  deque(idx)=[4]  deque(val)=[5]  window=[-1,-3,5]  → max=5

i=5, val=3:
  Step 1: front=4, 4 >= 5-3+1=3 → 沒過期
  Step 2: nums[4]=5 > 3 → 不 pop
  Step 3: append 5 → deque=[4, 5]
  ★ max = nums[4] = 5
  deque(idx)=[4, 5]  deque(val)=[5, 3]  window=[-3,5,3]  → max=5

i=6, val=6:
  Step 1: front=4, 4 >= 6-3+1=4 → 沒過期
  Step 2: nums[5]=3 <= 6 → pop back idx=5 → deque=[4]
          nums[4]=5 <= 6 → pop back idx=4 → deque=[]
  Step 3: append 6 → deque=[6]
  ★ max = nums[6] = 6
  deque(idx)=[6]  deque(val)=[6]  window=[5,3,6]  → max=6

i=7, val=7:
  Step 1: front=6, 6 >= 7-3+1=5 → 沒過期
  Step 2: nums[6]=6 <= 7 → pop back idx=6 → deque=[]
  Step 3: append 7 → deque=[7]
  ★ max = nums[7] = 7
  deque(idx)=[7]  deque(val)=[7]  window=[3,6,7]  → max=7

最終結果 = [3, 3, 5, 5, 6, 7] ✓
```

### 範例 2：nums=[1,-1], k=1

```
k=1 表示視窗大小為 1，每個元素本身就是最大值。

i=0, val=1:
  deque=[] → append 0 → deque=[0]
  i >= k-1=0 → max = nums[0] = 1

i=1, val=-1:
  front=0, 0 < 1-1+1=1 → 過期！popleft → deque=[]
  append 1 → deque=[1]
  max = nums[1] = -1

結果 = [1, -1] ✓
```

### Corner Cases

```
1. k=1 → 每個元素就是答案
2. k=n → 只有一個視窗，答案是全局最大值
3. 全部遞減 [5,4,3,2,1], k=3 → deque 會越來越長
   → 結果 [5,4,3]
4. 全部相同 [3,3,3,3], k=2 → 結果 [3,3,3]
```

### 程式碼

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    dq = deque()  # 存 index
    result = []

    for i in range(len(nums)):
        # 1. 移除超出視窗的 front
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # 2. 從 back pop 掉 <= nums[i] 的
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()

        # 3. 加入新元素
        dq.append(i)

        # 4. 視窗形成時記錄答案
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Time: O(n) | Space: O(k)**

---

# 第六章：比較與決策框架

## 6.1 四大資料結構比較

```
+---------------------+-------------------+------------------------------------+
| 資料結構            | 使用時機           | 經典題型                           |
+---------------------+-------------------+------------------------------------+
| Stack               | 配對匹配           | Valid Parentheses (LC 20)          |
| (堆疊 LIFO)        | 巢狀結構           | Decode String (LC 394)             |
|                     | 後進先出邏輯       | Evaluate RPN (LC 150)              |
|                     | 遞迴模擬           | Basic Calculator (LC 227)          |
+---------------------+-------------------+------------------------------------+
| Monotonic Stack     | "下一個更大/更小"  | Next Greater Element (LC 496)      |
| (單調堆疊)         | "左/右邊界"        | Daily Temperatures (LC 739)        |
|                     | "柱狀圖面積"       | Largest Rectangle (LC 84)          |
|                     | "接雨水"           | Trapping Rain Water (LC 42)        |
+---------------------+-------------------+------------------------------------+
| Queue               | FIFO 順序處理      | BFS (Level-order Traversal)        |
| (佇列 FIFO)        | 排程               | Design Circular Queue (LC 622)     |
+---------------------+-------------------+------------------------------------+
| Monotonic Deque     | 滑動視窗最大/最小  | Sliding Window Maximum (LC 239)    |
| (單調雙端佇列)     | 定長區間極值       | Shortest Subarray Sum >= K         |
+---------------------+-------------------+------------------------------------+
```

## 6.2 面試 Pattern 識別

```
┌─────────────────────────────────────────────────────────────────────────┐
│  看到這些關鍵字 → 立刻想到對應的資料結構                                 │
│                                                                         │
│  "matching" / "valid" / "parentheses"  → Stack                         │
│  "nested" / "decode" / "recursive"     → Stack                         │
│  "expression" / "calculator"           → Stack                         │
│                                                                         │
│  "next greater" / "next smaller"       → Monotonic Stack               │
│  "previous greater" / "previous smaller" → Monotonic Stack             │
│  "histogram" / "rectangle area"        → Monotonic Stack (遞增)         │
│  "trapping rain water"                 → Monotonic Stack               │
│                                                                         │
│  "sliding window" + "maximum/minimum"  → Monotonic Deque               │
│  "fixed window" + "extreme value"      → Monotonic Deque               │
│                                                                         │
│  "BFS" / "level order" / "shortest path (unweighted)" → Queue          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 6.3 Monotonic Stack 方向選擇

```
┌──────────────────────────────────┬──────────────────────────────────┐
│  找 Next Greater Element         │  找 Next Smaller Element         │
│  （右邊第一個更大的）            │  （右邊第一個更小的）            │
├──────────────────────────────────┼──────────────────────────────────┤
│  掃描方向：右 → 左              │  掃描方向：右 → 左              │
│  Stack 類型：遞減                │  Stack 類型：遞增                │
│  Pop 條件：stack[-1] <= val      │  Pop 條件：stack[-1] >= val      │
├──────────────────────────────────┼──────────────────────────────────┤
│  找 Previous Greater Element     │  找 Previous Smaller Element     │
│  （左邊第一個更大的）            │  （左邊第一個更小的）            │
├──────────────────────────────────┼──────────────────────────────────┤
│  掃描方向：左 → 右              │  掃描方向：左 → 右              │
│  Stack 類型：遞減                │  Stack 類型：遞增                │
│  Pop 條件：stack[-1] <= val      │  Pop 條件：stack[-1] >= val      │
└──────────────────────────────────┴──────────────────────────────────┘
```

**共通 Pattern：**
```python
# Next Greater Element（從右到左，遞減 stack）
for i in range(n - 1, -1, -1):
    while stack and stack[-1] <= nums[i]:
        stack.pop()
    result[i] = stack[-1] if stack else -1
    stack.append(nums[i])

# Histogram / 左右邊界型（從左到右，遞增 stack，存 index）
for i in range(n + 1):
    cur = heights[i] if i < n else 0
    while stack and cur < heights[stack[-1]]:
        h = heights[stack.pop()]
        w = i if not stack else i - stack[-1] - 1
        max_area = max(max_area, h * w)
    stack.append(i)
```

## 6.4 時間複雜度速查

| 題目 | Time | Space | 關鍵 |
|------|------|-------|------|
| Valid Parentheses | O(n) | O(n) | 一次遍歷 |
| Min Stack | O(1) per op | O(n) | 雙 stack 同步 |
| Evaluate RPN | O(n) | O(n) | 一次遍歷 |
| Next Greater Element | O(n) | O(n) | 每個元素 push/pop 各一次 |
| Daily Temperatures | O(n) | O(n) | 每個元素 push/pop 各一次 |
| Largest Rectangle | O(n) | O(n) | 每個元素 push/pop 各一次 |
| Decode String | O(output) | O(n) | 輸出長度可能很大 |
| Basic Calculator II | O(n) | O(n) | 一次遍歷 |
| Sliding Window Max | O(n) | O(k) | 每個元素進出 deque 各一次 |

## 6.5 面試 Tips

1. **Stack 題目通用模板**：決定 push 什麼（值/index/pair）→ 決定何時 pop → 決定 pop 時做什麼計算
2. **Monotonic Stack 必問 follow-up**："Why O(n)?" → "Each element pushed and popped at most once. Total = 2n = O(n)."
3. **LC 84 延伸**：LC 85 Maximal Rectangle（2D 版本）、LC 42 Trapping Rain Water
4. **Debug 技巧**：追蹤完整 stack 狀態、先用 2-3 個元素手動模擬、注意 stack 為空的邊界

---

## 本章題目索引

| # | 題目 | 難度 | 類型 | 章節 |
|---|------|------|------|------|
| 20 | Valid Parentheses | Easy | Stack | 2.1 |
| 155 | Min Stack | Medium | Stack | 2.2 |
| 150 | Evaluate RPN | Medium | Stack | 2.3 |
| 496 | Next Greater Element I | Easy | Monotonic Stack | 3.1 |
| 739 | Daily Temperatures | Medium | Monotonic Stack | 3.2 |
| 84 | Largest Rectangle in Histogram | Hard | Monotonic Stack | 3.3 |
| 394 | Decode String | Medium | Stack Simulation | 4.1 |
| 227 | Basic Calculator II | Medium | Stack Simulation | 4.2 |
| 239 | Sliding Window Maximum | Hard | Monotonic Deque | 5.1 |
