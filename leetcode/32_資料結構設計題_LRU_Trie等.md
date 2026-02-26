# LeetCode 教學 #32：資料結構設計題 — LRU Cache, Trie, 與經典 Design Problems

> **適用對象**：LeetCode 中高階學習者，準備 Google / NVIDIA 面試
> **前置知識**：HashMap、Linked List、Stack/Queue、Tree、Heap 基本概念
> **核心理念**：Design 題考的不是「會不會某個資料結構」，而是「能不能把多個資料結構組合起來」
> **語言**：繁體中文解說 + English technical terms

---

## 目錄

| 章 | 主題 | 重要度 |
|----|------|--------|
| 1 | 設計題的本質 — 組合資料結構 | ★★★★★ |
| 2 | LRU Cache (LC 146) — Google 必考 | ★★★★★ |
| 3 | LFU Cache (LC 460) — Hard | ★★★★☆ |
| 4 | Min Stack (LC 155) — 基礎設計 | ★★★★☆ |
| 5 | Design HashMap (LC 706) | ★★★☆☆ |
| 6 | Implement Trie (LC 208) | ★★★★★ |
| 7 | Design Twitter (LC 355) | ★★★★☆ |
| 8 | Serialize/Deserialize Binary Tree (LC 297) | ★★★★★ |
| 9 | 用 Stack 實作 Queue / 用 Queue 實作 Stack (LC 232, 225) | ★★★★☆ |
| 10 | Design 題的面試策略 | ★★★★★ |
| 11 | 常見設計組合速查表 | ★★★★★ |

---

# 第一章：設計題的本質 — 組合資料結構

## 1.1 Design 題在考什麼？

一般的 LeetCode 題目問你：「給定輸入，求輸出。」
Design 題問你：「設計一個 class，支援這些操作，每個操作要符合指定的時間複雜度。」

**這本質上是一個資料結構選擇與組合的問題。**

```
一般題：input → algorithm → output
Design 題：定義 operations + 複雜度要求 → 選擇/組合 data structures → 實作 class
```

## 1.2 解題思考框架

每道 Design 題，都用這四步：

```
Step 1: 列出所有操作 (operations)
        例如 get(), put(), delete(), getMin()

Step 2: 確認每個操作的時間複雜度要求
        例如 get() 要 O(1)、put() 要 O(1)

Step 3: 對每個操作，思考哪個資料結構能做到
        O(1) 查找 → HashMap
        O(1) 插入/刪除 + 維護順序 → Doubly Linked List
        O(logn) 插入 + O(1) 取極值 → Heap
        前綴搜尋 → Trie

Step 4: 找到能同時滿足所有操作的「組合」
        單一資料結構通常不夠 → 需要組合兩個以上
```

## 1.3 為什麼需要「組合」？

因為沒有一種資料結構是萬能的：

| 資料結構 | 擅長 | 不擅長 |
|---------|------|--------|
| HashMap | O(1) 查找、插入、刪除 | 無法維護順序 |
| Array | O(1) 隨機存取 | O(n) 插入/刪除（中間位置） |
| Linked List | O(1) 插入/刪除（已知位置） | O(n) 查找 |
| Heap | O(1) 取最大/最小值 | O(n) 任意查找 |
| Trie | O(m) 前綴搜尋 | 只適用於字串 |

**組合的精髓**：用 A 的強項補 B 的弱項。

例如 LRU Cache 需要：
- O(1) 查找 → HashMap 擅長，Linked List 不擅長
- O(1) 移動順序 → Linked List 擅長，HashMap 不擅長
- 結論：HashMap + Doubly Linked List，互相補位

---

# 第二章：LRU Cache (LC 146) — Google 必考

> **難度**：Medium | **頻率**：Google 面試 Top 5 常考題
> **核心**：HashMap + Doubly Linked List

## 2.1 需求分析

設計一個 LRU (Least Recently Used) Cache，支援：

| 操作 | 說明 | 時間複雜度要求 |
|------|------|--------------|
| `get(key)` | 取得 key 對應的 value，若不存在回傳 -1 | O(1) |
| `put(key, value)` | 寫入/更新 key-value pair | O(1) |
| 當 cache 滿了 | 移除「最久沒被使用」的 entry | 自動觸發 |

**關鍵觀察**：每次 `get` 或 `put` 某個 key，那個 key 就變成「最近使用」。如果 cache 滿了要淘汰，淘汰的是「最久沒被 get/put 的那個」。

## 2.2 設計思考過程 — 為什麼是 HashMap + Doubly Linked List

**嘗試 1：只用 HashMap**

HashMap 可以 O(1) 查找和插入，但它**不記錄使用順序**。你無法知道哪個 key 是「最久未使用」的。

**嘗試 2：只用 Linked List**

Linked List 可以維護順序（最近使用的放頭部，最久未使用的在尾部）。但查找是 O(n) — 你必須從頭掃到尾才能找到某個 key。

**嘗試 3：HashMap + Singly Linked List**

HashMap 存 `key → node`，可以 O(1) 找到節點。但 Singly Linked List 刪除某個節點需要知道它的**前一個節點**，這又要 O(n) 遍歷。

**最終解法：HashMap + Doubly Linked List**

- HashMap: `key → Node`，O(1) 定位任何節點
- Doubly Linked List: 每個 Node 有 `prev` 和 `next`，可以 O(1) 從任何位置拆出節點、移到頭部

```
HashMap                 Doubly Linked List
┌─────────────────┐     ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
│ key1 → Node A  ─┼────►│ HEAD │◄──►│  A   │◄──►│  B   │◄──►│ TAIL │
│ key2 → Node B   │     │(dummy)│    │(k1,v1)│   │(k2,v2)│   │(dummy)│
└─────────────────┘     └──────┘    └──────┘    └──────┘    └──────┘
                          最近使用 ←──────────────────────→ 最久未使用
```

**為什麼用 dummy head 和 dummy tail？**
避免處理邊界條件。如果沒有 dummy nodes，當 list 只剩一個節點或變空時，需要大量 `if` 判斷。Dummy nodes 讓所有操作統一。

## 2.3 操作追蹤 — capacity = 2

我們逐步追蹤每個操作後的完整狀態：

```
初始狀態：
  list: HEAD ◄──► TAIL  (空的)
  map: {}
  size: 0

─────────────────────────────────────────────────────

操作 1: put(1, 1)
  key 1 不在 map 中 → 建立新 Node(1,1)
  將 Node 加到 HEAD 後面
  map 加入 {1: Node(1,1)}
  size: 1 (未超過 capacity=2)

  list: HEAD ◄──► [1:1] ◄──► TAIL
  map: {1: Node(1,1)}

─────────────────────────────────────────────────────

操作 2: put(2, 2)
  key 2 不在 map 中 → 建立新 Node(2,2)
  將 Node 加到 HEAD 後面
  map 加入 {2: Node(2,2)}
  size: 2 (未超過 capacity=2)

  list: HEAD ◄──► [2:2] ◄──► [1:1] ◄──► TAIL
  map: {1: Node(1,1), 2: Node(2,2)}
             (最近)              (最久)

─────────────────────────────────────────────────────

操作 3: get(1) → 回傳 1
  key 1 在 map 中 → 找到 Node(1,1)
  將 Node(1,1) 從當前位置拆出
  將 Node(1,1) 移到 HEAD 後面

  拆出前: HEAD ◄──► [2:2] ◄──► [1:1] ◄──► TAIL
  拆出後: HEAD ◄──► [2:2] ◄──► TAIL  (暫時)
  插入後: HEAD ◄──► [1:1] ◄──► [2:2] ◄──► TAIL

  list: HEAD ◄──► [1:1] ◄──► [2:2] ◄──► TAIL
  map: {1: Node(1,1), 2: Node(2,2)}  (map 不變)

─────────────────────────────────────────────────────

操作 4: put(3, 3)
  key 3 不在 map 中 → 建立新 Node(3,3)
  size 會變成 3 > capacity=2 → 先淘汰！
  淘汰 TAIL 前面的節點 = Node(2,2)
  從 list 移除 Node(2,2)
  從 map 刪除 key 2
  然後將 Node(3,3) 加到 HEAD 後面
  map 加入 {3: Node(3,3)}

  list: HEAD ◄──► [3:3] ◄──► [1:1] ◄──► TAIL
  map: {1: Node(1,1), 3: Node(3,3)}

─────────────────────────────────────────────────────

操作 5: get(2) → 回傳 -1
  key 2 不在 map 中 → 回傳 -1
  list 和 map 都不變

  list: HEAD ◄──► [3:3] ◄──► [1:1] ◄──► TAIL
  map: {1: Node(1,1), 3: Node(3,3)}

─────────────────────────────────────────────────────

操作 6: put(4, 4)
  key 4 不在 map 中 → 建立新 Node(4,4)
  size 會超過 → 淘汰 TAIL 前面的 Node(1,1)
  從 list 移除 Node(1,1), 從 map 刪除 key 1
  加入 Node(4,4) 到 HEAD 後面

  list: HEAD ◄──► [4:4] ◄──► [3:3] ◄──► TAIL
  map: {3: Node(3,3), 4: Node(4,4)}

─────────────────────────────────────────────────────

操作 7: get(1) → 回傳 -1  (已被淘汰)
操作 8: get(3) → 回傳 3   (移到最前面)

  list: HEAD ◄──► [3:3] ◄──► [4:4] ◄──► TAIL
  map: {3: Node(3,3), 4: Node(4,4)}
```

## 2.4 完整 Python 實作

```python
class ListNode:
    """Doubly Linked List 的節點"""
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}  # key → ListNode

        # 建立 dummy head 和 dummy tail
        self.head = ListNode()  # dummy head
        self.tail = ListNode()  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: ListNode):
        """從 doubly linked list 中拆出一個節點 — O(1)"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: ListNode):
        """把節點加到 HEAD 後面（表示最近使用）— O(1)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: ListNode):
        """拆出後移到最前面 — O(1)"""
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._move_to_front(node)  # 標記為最近使用
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            # key 已存在 → 更新 value + 移到最前面
            node = self.map[key]
            node.val = value
            self._move_to_front(node)
        else:
            # key 不存在 → 建立新節點
            new_node = ListNode(key, value)
            self.map[key] = new_node
            self._add_to_front(new_node)

            if len(self.map) > self.capacity:
                # 超過容量 → 淘汰 TAIL 前面的節點（最久未使用）
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.map[lru_node.key]  # 這就是為什麼 Node 要存 key！
```

**一個容易漏掉的細節**：為什麼 `ListNode` 要同時存 `key` 和 `val`？

因為淘汰時，我們從 Linked List 的尾部拿到一個 Node，需要知道它的 key 才能從 HashMap 中 `del self.map[key]`。如果 Node 只存 val，我們就無法從 HashMap 中刪掉它。

## 2.5 複雜度分析

| 操作 | 時間 | 空間 |
|------|------|------|
| `get(key)` | O(1) | — |
| `put(key, value)` | O(1) | — |
| 整體空間 | — | O(capacity) |

每個操作都是：HashMap 查找 O(1) + Linked List 指標操作 O(1) = O(1)。

---

# 第三章：LFU Cache (LC 460) — Hard

> **難度**：Hard | **核心**：HashMap + Frequency Map + Doubly Linked List per Frequency

## 3.1 需求分析

LFU (Least Frequently Used) Cache，與 LRU 的差別：

| | LRU | LFU |
|---|-----|-----|
| 淘汰標準 | 最久未使用（時間） | 使用次數最少（頻率） |
| 同分處理 | 不存在（時間唯一） | 頻率相同時，淘汰最久未使用的（LRU） |

操作：
- `get(key)`: O(1)，取得 value，該 key 的使用頻率 +1
- `put(key, value)`: O(1)，寫入/更新，淘汰時移除頻率最低的

## 3.2 設計思考

**挑戰 1：如何 O(1) 找到頻率最低的 key？**

用一個變數 `min_freq` 追蹤當前最低頻率。

**挑戰 2：同一頻率下有多個 key，如何 O(1) 淘汰最久未使用的？**

每個頻率對應一個 doubly linked list（本質上就是一個小型 LRU Cache）。

**整體結構**：

```
key_map:  key → Node          （O(1) 找到任何 key 的節點）
freq_map: freq → DoublyLinkedList  （每個頻率一條 list，維護 LRU 順序）
min_freq: int                 （追蹤當前最低頻率）

範例：capacity=3，已存入 (1,10) 用2次, (2,20) 用1次, (3,30) 用1次

min_freq = 1

freq_map:
  freq=1: HEAD ◄──► [3:30] ◄──► [2:20] ◄──► TAIL
                    (較新)       (較舊)
  freq=2: HEAD ◄──► [1:10] ◄──► TAIL

key_map:
  {1: Node(1,10,freq=2), 2: Node(2,20,freq=1), 3: Node(3,30,freq=1)}

淘汰時：找 freq_map[min_freq] 的 list，移除尾部（最舊的）= Node(2,20)
```

## 3.3 操作追蹤 — capacity = 2

```
初始：min_freq=0, key_map={}, freq_map={}

─────────────────────────────────────────────────────

操作 1: put(1, 10)
  key 1 不存在 → 建立 Node(key=1, val=10, freq=1)
  加入 key_map: {1: Node(1,10,freq=1)}
  加入 freq_map[1] 的 list 頭部
  min_freq = 1

  freq_map:  1: [1:10]
  key_map:   {1: Node(1,10,f=1)}
  min_freq:  1

─────────────────────────────────────────────────────

操作 2: put(2, 20)
  key 2 不存在 → 建立 Node(key=2, val=20, freq=1)
  size=2 = capacity → 不需淘汰
  加入 freq_map[1] 頭部，加入 key_map

  freq_map:  1: [2:20] ◄──► [1:10]
  key_map:   {1: Node(1,10,f=1), 2: Node(2,20,f=1)}
  min_freq:  1

─────────────────────────────────────────────────────

操作 3: get(1) → 回傳 10
  找到 Node(1,10,freq=1)
  freq 1→2：從 freq_map[1] 拆出，加入 freq_map[2] 頭部
  Node 的 freq 更新為 2
  freq_map[1] 還有 Node(2,20) → min_freq 不變

  freq_map:  1: [2:20]
             2: [1:10]
  key_map:   {1: Node(1,10,f=2), 2: Node(2,20,f=1)}
  min_freq:  1

─────────────────────────────────────────────────────

操作 4: put(3, 30)
  key 3 不存在，size 會超過 capacity → 淘汰！
  淘汰 freq_map[min_freq=1] 的尾部 = Node(2,20)
  從 key_map 刪除 key 2
  建立 Node(3,30,freq=1)，加入 freq_map[1] 頭部

  freq_map:  1: [3:30]
             2: [1:10]
  key_map:   {1: Node(1,10,f=2), 3: Node(3,30,f=1)}
  min_freq:  1

─────────────────────────────────────────────────────

操作 5: get(2) → 回傳 -1  (已被淘汰)

操作 6: get(3) → 回傳 30
  Node(3,30) freq 1→2
  freq_map[1] 變空 → 刪除
  min_freq 更新為 2（因為原本 min_freq=1 的 list 空了）

  freq_map:  2: [3:30] ◄──► [1:10]
  key_map:   {1: Node(1,10,f=2), 3: Node(3,30,f=2)}
  min_freq:  2
```

## 3.4 完整 Python 實作

```python
class LFUNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """帶 dummy head/tail 的雙向鏈結串列（用於同頻率的 LRU 順序）"""
    def __init__(self):
        self.head = LFUNode()
        self.tail = LFUNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self):
        """移除尾部（最久未使用），回傳被移除的節點"""
        if self.size == 0:
            return None
        last = self.tail.prev
        self.remove(last)
        return last

    def is_empty(self):
        return self.size == 0


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_map = {}       # key → LFUNode
        self.freq_map = {}      # freq → DoublyLinkedList
        self.min_freq = 0

    def _update_freq(self, node):
        """將節點的頻率 +1，並移到新頻率的 list"""
        old_freq = node.freq
        # 從舊頻率的 list 移除
        self.freq_map[old_freq].remove(node)
        # 如果舊頻率的 list 空了
        if self.freq_map[old_freq].is_empty():
            del self.freq_map[old_freq]
            if self.min_freq == old_freq:
                self.min_freq += 1  # min_freq 剛好 +1
        # 加入新頻率的 list
        node.freq += 1
        new_freq = node.freq
        if new_freq not in self.freq_map:
            self.freq_map[new_freq] = DoublyLinkedList()
        self.freq_map[new_freq].add_to_front(node)

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1
        node = self.key_map[key]
        self._update_freq(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.key_map:
            node = self.key_map[key]
            node.val = value
            self._update_freq(node)
        else:
            if len(self.key_map) >= self.capacity:
                # 淘汰 min_freq list 的尾部
                evict_list = self.freq_map[self.min_freq]
                evicted = evict_list.remove_last()
                del self.key_map[evicted.key]
                if evict_list.is_empty():
                    del self.freq_map[self.min_freq]
            # 新節點頻率一定是 1
            new_node = LFUNode(key, value)
            self.key_map[key] = new_node
            if 1 not in self.freq_map:
                self.freq_map[1] = DoublyLinkedList()
            self.freq_map[1].add_to_front(new_node)
            self.min_freq = 1  # 新插入的節點頻率最低，一定是 1
```

**`min_freq` 的巧妙更新**：
- `_update_freq` 中：如果舊頻率 list 空了且是 min_freq，則 `min_freq += 1`
- `put` 新 key 時：`min_freq = 1`（新節點的 freq 一定是 1，所以它一定是最低的）

---

# 第四章：Min Stack (LC 155) — 基礎設計

> **難度**：Medium | **核心**：兩個 Stack 並行

## 4.1 需求分析

設計一個 stack，除了 `push`, `pop`, `top` 之外，還要支援 `getMin()`，全部 O(1)。

**難點**：普通 stack 的 `getMin()` 需要 O(n) 掃描。如何做到 O(1)？

## 4.2 設計思考

**核心觀察**：當我們 push 一個新元素時，整個 stack 的最小值可能改變。當我們 pop 時，最小值也可能改變。所以我們需要追蹤**每個狀態下的最小值**。

**解法**：用一個輔助 stack (`min_stack`)，同步記錄「到目前為止的最小值」。

```
main_stack:  存實際元素
min_stack:   存「到這個位置為止的最小值」

兩個 stack 永遠保持同樣高度
每次 push：min_stack 存 min(新元素, min_stack 目前 top)
每次 pop：兩個 stack 一起 pop
getMin()：直接看 min_stack 的 top
```

## 4.3 操作追蹤

```
操作               main_stack    min_stack     getMin()
────────────────   ──────────    ──────────    ────────
push(5)            [5]           [5]           5
push(3)            [5,3]         [5,3]         3
push(7)            [5,3,7]       [5,3,3]       3       ← min 還是 3
push(1)            [5,3,7,1]     [5,3,3,1]     1       ← 新最小值
pop() → 1          [5,3,7]       [5,3,3]       3       ← 回到之前的 min
pop() → 7          [5,3]         [5,3]         3
push(2)            [5,3,2]       [5,3,2]       2
pop() → 2          [5,3]         [5,3]         3
pop() → 3          [5]           [5]           5
```

**為什麼這行得通？** 因為 min_stack 的每個位置記錄了「如果 main_stack 只有前 i 個元素，最小值是多少」。Pop 的時候一起 pop，就自動回復到前一個狀態。

## 4.4 完整 Python 實作

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # 平行的輔助 stack

    def push(self, val: int) -> None:
        self.stack.append(val)
        # min_stack 的 top = 到目前為止的最小值
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()  # 同步 pop

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]  # O(1)！
```

| 操作 | 時間 | 空間 |
|------|------|------|
| push / pop / top / getMin | O(1) | O(n) 輔助 stack |

---

# 第五章：Design HashMap (LC 706)

> **難度**：Easy | **核心**：Array of Buckets + Chaining

## 5.1 需求分析

自己實作一個 HashMap，支援 `put(key, value)`, `get(key)`, `remove(key)`。

不能用任何內建的 hash table library。

## 5.2 設計思考

```
Hash Table 的本質：
  array + hash function + collision handling

Hash function: key % bucket_size
Collision handling: Chaining（每個 bucket 是一個 linked list）
```

**bucket_size 的選擇**：
- 題目限制 key 範圍 0 ~ 10^6，操作次數最多 10^4
- 選一個質數作為 bucket_size（減少碰撞），例如 1009
- 為什麼用質數？因為質數作為除數時，hash 值的分佈更均勻

## 5.3 Collision 追蹤

```
bucket_size = 5（為了示範用小的）
hash(key) = key % 5

put(2, "A"):  hash(2)=2  → buckets[2]: [(2,"A")]
put(7, "B"):  hash(7)=2  → buckets[2]: [(2,"A"), (7,"B")]  ← collision!
put(3, "C"):  hash(3)=3  → buckets[3]: [(3,"C")]
get(7):       hash(7)=2  → 走訪 buckets[2]，找到 key=7 → 回傳 "B"
get(12):      hash(12)=2 → 走訪 buckets[2]，沒有 key=12 → 回傳 -1
put(2, "D"):  hash(2)=2  → 走訪 buckets[2]，找到 key=2，更新為 "D"
              buckets[2]: [(2,"D"), (7,"B")]
remove(2):    hash(2)=2  → 走訪 buckets[2]，找到 key=2，刪除
              buckets[2]: [(7,"B")]

最終：
  buckets[0]: []
  buckets[1]: []
  buckets[2]: [(7,"B")]
  buckets[3]: [(3,"C")]
  buckets[4]: []
```

## 5.4 完整 Python 實作

```python
class MyHashMap:
    def __init__(self):
        self.size = 1009  # 質數，減少碰撞
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # 更新
                return
        bucket.append((key, value))  # 新增

    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

**平均複雜度**：O(n/bucket_size)，如果 n << bucket_size，接近 O(1)。

---

# 第六章：Implement Trie (LC 208)

> **難度**：Medium | **核心**：TrieNode with children dict + is_end flag

## 6.1 需求分析

| 操作 | 說明 |
|------|------|
| `insert(word)` | 插入一個單字 |
| `search(word)` | 回傳 word 是否**完整存在** |
| `startsWith(prefix)` | 回傳是否有任何單字**以 prefix 開頭** |

## 6.2 TrieNode 結構

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char → TrieNode
        self.is_end = False  # 是否為某個完整單字的結尾
```

**為什麼用 `dict` 而不是 `[None]*26` array？**
- dict: 更 Pythonic，支援任意字元（不限小寫英文）
- array: 稍快（直接 index），但限制字元集
- 面試時用 dict 更安全，除非面試官特別要求

## 6.3 操作追蹤

插入 `"apple"`, `"app"`, `"bat"`，然後搜尋：

```
── insert("apple") ──────────────────────────────────

  root → 'a' → 'p' → 'p' → 'l' → 'e'*
  每步：如果 child 不存在就建立新 TrieNode
  最後一個字元的 node 標記 is_end = True

── insert("app") ────────────────────────────────────

  root → 'a' → 'p' → 'p'* → 'l' → 'e'*
  走到第二個 'p' 時，child 已存在 → 不需建立
  只在第二個 'p' 標記 is_end = True

── insert("bat") ────────────────────────────────────

  root ─┬─ 'a' → 'p' → 'p'* → 'l' → 'e'*
        └─ 'b' → 'a' → 't'*

── search("app") → True ─────────────────────────────

  root → 'a'(存在) → 'p'(存在) → 'p'(存在, is_end=True) → True

── search("ap") → False ─────────────────────────────

  root → 'a'(存在) → 'p'(存在, is_end=False) → False
  注意：'p' 節點存在但 is_end=False，所以 "ap" 不是完整單字

── startsWith("ap") → True ──────────────────────────

  root → 'a'(存在) → 'p'(存在) → True
  只要路徑存在就行，不管 is_end

── search("abc") → False ────────────────────────────

  root → 'a'(存在) → 找 'b' → children 中沒有 'b' → False
```

## 6.4 完整 Python 實作

```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char → TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True  # 標記完整單字結尾

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str):
        """沿著 prefix 路徑走，回傳最後一個節點（或 None）"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

**search 和 startsWith 的差別**：只差一個 `is_end` 檢查。`_find_node` 是共用邏輯，非常乾淨。

| 操作 | 時間 | 空間 |
|------|------|------|
| insert(word) | O(m)，m = word 長度 | O(m) 最多建 m 個新節點 |
| search(word) | O(m) | O(1) |
| startsWith(prefix) | O(m) | O(1) |

---

# 第七章：Design Twitter (LC 355)

> **難度**：Medium | **核心**：HashMap + Heap (Merge K Sorted Lists)

## 7.1 需求分析

| 操作 | 說明 |
|------|------|
| `postTweet(userId, tweetId)` | 使用者發一則推文 |
| `getNewsFeed(userId)` | 取得該使用者自己 + 追蹤對象的最新 10 則推文 |
| `follow(followerId, followeeId)` | followerId 追蹤 followeeId |
| `unfollow(followerId, followeeId)` | 取消追蹤 |

## 7.2 設計思考

```
需要的資料：
  1. 每個使用者的推文列表（含時間戳記） → HashMap: userId → list of (timestamp, tweetId)
  2. 每個使用者追蹤了誰                → HashMap: userId → set of followeeIds
  3. 全域的時間戳記                    → 遞增計數器

getNewsFeed 的挑戰：
  - 使用者可能追蹤 100 人，每人有 1000 則推文
  - 要找出所有來源中「最新的 10 則」
  - 這就是 Merge K Sorted Lists 問題！→ 用 Heap
```

**getNewsFeed 的過程**：

```
1. 收集自己 + 所有 followee 的推文列表 → K 個 sorted lists
2. 用 Max Heap，每個 list 先放入最新的那則
3. 每次 pop 最大的（最新的），把該 list 的下一則放入 heap
4. 重複直到收集 10 則或 heap 為空
```

## 7.3 操作追蹤

```
postTweet(1, 101)  → user1 tweets: [(time=0, id=101)]
postTweet(2, 201)  → user2 tweets: [(time=1, id=201)]
follow(1, 2)       → user1 follows: {2}
postTweet(2, 202)  → user2 tweets: [(time=1, id=201), (time=2, id=202)]
postTweet(1, 102)  → user1 tweets: [(time=0, id=101), (time=3, id=102)]

getNewsFeed(1):
  來源: user1 自己 + user2（追蹤的人）
  user1 最新: (time=3, id=102)
  user2 最新: (time=2, id=202)

  Heap (max heap by time):
    初始: [(-3, 102, user1, idx=1), (-2, 202, user2, idx=1)]
    pop (-3, 102) → result=[102]，push user1 的下一則 (-0, 101)
    Heap: [(-2, 202, user2, idx=1), (0, 101, user1, idx=0)]
    pop (-2, 202) → result=[102, 202]，push user2 的下一則 (-1, 201)
    pop (-1, 201) → result=[102, 202, 201]
    pop (0, 101)  → result=[102, 202, 201, 101]
    Heap 空了，結束

  回傳: [102, 202, 201, 101]（最新 → 最舊）
```

## 7.4 完整 Python 實作

```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)   # userId → [(time, tweetId), ...]
        self.follows = defaultdict(set)   # userId → set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> list:
        # 收集所有來源：自己 + 追蹤的人
        sources = self.follows[userId] | {userId}

        # Max Heap: 用負數模擬（Python 只有 min heap）
        heap = []
        for uid in sources:
            if self.tweets[uid]:
                idx = len(self.tweets[uid]) - 1  # 從最新的開始
                t, tid = self.tweets[uid][idx]
                heapq.heappush(heap, (-t, tid, uid, idx))

        result = []
        while heap and len(result) < 10:
            neg_t, tid, uid, idx = heapq.heappop(heap)
            result.append(tid)
            if idx > 0:  # 還有更舊的推文
                idx -= 1
                t, tid = self.tweets[uid][idx]
                heapq.heappush(heap, (-t, tid, uid, idx))

        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:  # 不能追蹤自己
            self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)
```

**為什麼用 Heap 而不是 sort 所有推文？**
- Sort 所有推文：O(N log N)，N = 所有推文總數
- Heap merge K lists（只取 10 則）：O(K + 10 log K)，K = 來源數
- 當推文很多但只要 10 則時，Heap 快非常多

---

# 第八章：Serialize/Deserialize Binary Tree (LC 297) — Google 常考

> **難度**：Hard | **核心**：BFS level-order 或 DFS preorder，配合 null marker

## 8.1 需求分析

把一棵 binary tree 轉成字串 (serialize)，再從字串還原回一模一樣的 tree (deserialize)。

**為什麼這題重要？** 這是很多系統設計的基礎 — 任何需要「傳輸」或「儲存」tree 結構的場景都用到這個概念。

## 8.2 方法一：BFS (Level-order)

```
     1
    / \
   2   3
      / \
     4   5

Serialize (BFS):
  Level 0: [1]
  Level 1: [2, 3]
  Level 2: [null, null, 4, 5]    ← 2 的左右子為 null

  結果: "1,2,3,null,null,4,5"
```

**BFS 逐步追蹤**：

```
Serialize:
  queue = [node(1)]
  result = []

  pop node(1) → result = ["1"]
    push left=node(2), push right=node(3)
    queue = [node(2), node(3)]

  pop node(2) → result = ["1","2"]
    left=None → result = ["1","2"], push null
    right=None → push null
    queue = [node(3), None, None]
    但我們直接加 "null" 到 result

  實際做法（更簡潔）：
  pop node(2) → append "2", push node(2).left=None, push node(2).right=None
  pop node(3) → append "3", push node(3).left=node(4), push node(3).right=node(5)
  pop None    → append "null" (不 push 任何東西)
  pop None    → append "null"
  pop node(4) → append "4", push None, push None
  pop node(5) → append "5", push None, push None
  pop None... (都是 null 的 leaf，但我們可以在這裡停止)

  最終: "1,2,3,null,null,4,5"

Deserialize:
  tokens = ["1","2","3","null","null","4","5"]
  root = Node(1)
  queue = [Node(1)]

  pop Node(1):
    left = tokens[1] = "2" → Node(2), queue.append(Node(2))
    right = tokens[2] = "3" → Node(3), queue.append(Node(3))

  pop Node(2):
    left = tokens[3] = "null" → None
    right = tokens[4] = "null" → None

  pop Node(3):
    left = tokens[5] = "4" → Node(4), queue.append(Node(4))
    right = tokens[6] = "5" → Node(5), queue.append(Node(5))

  結果:    1
          / \
         2   3
            / \
           4   5     ✓ 完全還原
```

## 8.3 方法二：DFS (Preorder)

```
     1
    / \
   2   3
      / \
     4   5

Preorder traversal (with null markers):
  visit 1 → "1"
  visit 2 → "2"
  visit null (2's left) → "null"
  visit null (2's right) → "null"
  visit 3 → "3"
  visit 4 → "4"
  visit null (4's left) → "null"
  visit null (4's right) → "null"
  visit 5 → "5"
  visit null (5's left) → "null"
  visit null (5's right) → "null"

  結果: "1,2,null,null,3,4,null,null,5,null,null"
```

**Deserialize DFS 追蹤**：

```
tokens = ["1","2","null","null","3","4","null","null","5","null","null"]
        index: 0   1     2      3    4   5     6      7    8     9     10

呼叫 dfs():
  token[0]="1" → 建立 Node(1)
    Node(1).left = dfs():
      token[1]="2" → 建立 Node(2)
        Node(2).left = dfs():
          token[2]="null" → return None
        Node(2).right = dfs():
          token[3]="null" → return None
      return Node(2)
    Node(1).right = dfs():
      token[4]="3" → 建立 Node(3)
        Node(3).left = dfs():
          token[5]="4" → 建立 Node(4)
            Node(4).left = dfs(): token[6]="null" → None
            Node(4).right = dfs(): token[7]="null" → None
          return Node(4)
        Node(3).right = dfs():
          token[8]="5" → 建立 Node(5)
            Node(5).left = dfs(): token[9]="null" → None
            Node(5).right = dfs(): token[10]="null" → None
          return Node(5)
      return Node(3)
  return Node(1)

結果：完全還原 ✓
```

## 8.4 完整 Python 實作 — BFS 版

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root) -> str:
        """BFS level-order，null 用 'null' 表示"""
        if not root:
            return ""
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        return ",".join(result)

    def deserialize(self, data: str):
        """從 BFS 字串還原 tree"""
        if not data:
            return None
        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(tokens):
            node = queue.popleft()
            # 左子
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1
            # 右子
            if i < len(tokens) and tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1
        return root
```

## 8.5 完整 Python 實作 — DFS 版

```python
class Codec:
    def serialize(self, root) -> str:
        """DFS preorder，null 用 'null' 表示"""
        result = []
        def dfs(node):
            if not node:
                result.append("null")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str):
        """從 DFS preorder 字串還原 tree"""
        if not data:
            return None
        tokens = iter(data.split(","))

        def dfs():
            val = next(tokens)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
```

**DFS 版為什麼用 `iter`？** 因為 `next(tokens)` 每次呼叫自動前進一步，不需要手動維護 index。這讓遞迴的程式碼非常乾淨。

**BFS vs DFS 的比較**：

| 面向 | BFS | DFS |
|------|-----|-----|
| 直覺性 | 像 LeetCode 題目的 tree 表示法 | 稍抽象 |
| 程式碼長度 | 稍長 | 更短 |
| 空間 | O(W)，W = tree 最寬那層 | O(H)，H = tree 高度 |
| 面試建議 | 推薦（容易解釋） | 推薦（程式碼更簡潔） |

---

# 第九章：Stack ↔ Queue 互相實作 (LC 232, LC 225)

> **核心概念**：用一種 LIFO/FIFO 結構模擬另一種

## 9.1 用兩個 Stack 實作 Queue (LC 232)

**核心觀察**：Stack 是反的（LIFO），如果把元素從一個 stack 倒到另一個 stack，順序就反過來了 — 反兩次就是正的（FIFO）！

```
push_stack（用於 push）:  元素進來放這裡
pop_stack （用於 pop）:   元素倒過來後從這裡出去

push(1): push_stack=[1],    pop_stack=[]
push(2): push_stack=[1,2],  pop_stack=[]
push(3): push_stack=[1,2,3],pop_stack=[]

pop():
  pop_stack 是空的 → 把 push_stack 全部倒過去
  push_stack=[1,2,3] → 逐一 pop 再 push 到 pop_stack
  pop 3 → pop_stack=[3]
  pop 2 → pop_stack=[3,2]
  pop 1 → pop_stack=[3,2,1]
  push_stack=[]

  現在 pop_stack=[3,2,1]，pop → 回傳 1 ✓ (FIFO!)
  pop_stack=[3,2]

pop():
  pop_stack 不是空的 → 直接 pop
  回傳 2 ✓
  pop_stack=[3]

push(4): push_stack=[4], pop_stack=[3]

pop():
  pop_stack 不是空的 → pop → 回傳 3 ✓
  pop_stack=[]

pop():
  pop_stack 空了 → 把 push_stack 倒過去
  pop_stack=[4]
  pop → 回傳 4 ✓
```

**Amortized O(1) 的關鍵**：每個元素最多被搬動一次（從 push_stack 到 pop_stack）。雖然偶爾一次 pop 會觸發 O(n) 的搬移，但攤提下來每個元素的操作是 O(1)。

```python
class MyQueue:
    def __init__(self):
        self.push_stack = []  # 新元素進來
        self.pop_stack = []   # 反轉後從這裡出去

    def push(self, x: int) -> None:
        self.push_stack.append(x)

    def pop(self) -> int:
        self._transfer()
        return self.pop_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.pop_stack[-1]

    def empty(self) -> bool:
        return not self.push_stack and not self.pop_stack

    def _transfer(self):
        """只在 pop_stack 空時才搬移 — 這是 amortized O(1) 的關鍵"""
        if not self.pop_stack:
            while self.push_stack:
                self.pop_stack.append(self.push_stack.pop())
```

## 9.2 用兩個 Queue 實作 Stack (LC 225)

**策略**：每次 push 時，讓新元素跑到 queue 的前面。

```
push(1): q = [1]
push(2): 先 append(2) → q = [1,2]
         然後把 2 前面的元素都重新排到後面：
         popleft 1, append 1 → q = [2,1]
         現在 2 在前面 ✓
push(3): append(3) → q = [2,1,3]
         popleft 2, append 2 → q = [1,3,2]
         popleft 1, append 1 → q = [3,2,1]
         現在 3 在前面 ✓

pop(): popleft → 3 ✓ (LIFO!)
pop(): popleft → 2 ✓
pop(): popleft → 1 ✓
```

```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        # 把前面的 n-1 個元素重新排到後面
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0
```

| 實作 | push | pop | 核心技巧 |
|------|------|-----|---------|
| Stack → Queue (LC 232) | O(1) | Amortized O(1) | 兩個 stack，延遲搬移 |
| Queue → Stack (LC 225) | O(n) | O(1) | push 時重排 queue |

---

# 第十章：Design 題的面試策略

## 10.1 五步解題法

```
Step 1: Clarify（釐清需求）
  - 確認所有操作和它們的時間複雜度要求
  - 問 edge cases: capacity=0? 空的時候 pop?
  - 問 thread-safety（通常面試不考，但問一下展示 senior 思維）

Step 2: Identify（辨識操作需求）
  - 列出每個操作需要的資料結構特性
  - 例如："get 要 O(1) → HashMap"、"維護順序 → Linked List"

Step 3: Combine（組合設計）
  - 畫出資料結構之間的關係圖
  - 解釋為什麼單一結構不夠，為什麼需要組合

Step 4: Interface first（先寫介面）
  - 先定義 class 和 method signatures
  - 用 pseudocode 描述每個 method 的邏輯
  - 確認面試官同意設計後再寫 code

Step 5: Trace（用例子驗證）
  - 在白板上追蹤 3-5 個操作
  - 展示你的設計確實能正確運作
```

## 10.2 常見陷阱

```
陷阱 1: 直接開始寫 code
  正確做法: 先花 3-5 分鐘討論設計，確認方向再寫

陷阱 2: 忘記 edge cases
  - capacity = 0
  - 操作空的 data structure
  - 重複 key 的處理
  - 極端輸入（非常大的 key、非常長的字串）

陷阱 3: 在 Linked List 操作時搞混指標順序
  正確做法: 永遠先設新節點的指標，再改舊節點的指標
  背口訣: "新先指，舊後改"

陷阱 4: Node 沒有存夠資訊
  - LRU 的 Node 要存 key（淘汰時要從 HashMap 刪除）
  - LFU 的 Node 要存 freq（升頻時要知道舊頻率）

陷阱 5: 忘記 Dummy Nodes
  用 dummy head/tail 能大幅減少邊界條件
  不用 dummy 時，insert 到空 list、delete 唯一節點都需要特判
```

## 10.3 時間分配建議（45 分鐘面試）

```
[0:00-0:03]  讀題 + Clarifying Questions
[0:03-0:08]  討論設計（畫資料結構關係圖）
[0:08-0:10]  寫 class 骨架 + method signatures
[0:10-0:30]  實作每個 method（20 分鐘）
[0:30-0:35]  用例子 trace 驗證
[0:35-0:40]  討論複雜度 + edge cases
[0:40-0:45]  Follow-up 問題
```

---

# 第十一章：常見設計組合速查表

## 11.1 需求 → 資料結構組合

| 需求組合 | 資料結構組合 | 代表題 | 難度 |
|---------|------------|--------|------|
| O(1) 查找 + O(1) 刪除 + 保持使用順序 | HashMap + Doubly Linked List | LRU Cache (LC 146) | Medium |
| O(1) 查找 + 頻率追蹤 + 同頻 LRU | HashMap + FreqMap + DLL per freq | LFU Cache (LC 460) | Hard |
| O(1) push/pop + O(1) getMin | Two Stacks (main + min) | Min Stack (LC 155) | Medium |
| O(1) 查找 + O(1) 插入/刪除 + O(1) getRandom | HashMap + Array (swap with last) | Insert Delete GetRandom O(1) (LC 380) | Medium |
| O(m) 插入 + O(m) 前綴搜尋 | Trie (Prefix Tree) | Implement Trie (LC 208) | Medium |
| 合併多來源 + 取 Top K | Heap (Priority Queue) | Design Twitter (LC 355) | Medium |
| 序列化 Tree 結構 | BFS/DFS + null markers | Serialize Binary Tree (LC 297) | Hard |
| FIFO from LIFO | Two Stacks (lazy transfer) | Queue using Stacks (LC 232) | Easy |
| LIFO from FIFO | Single Queue (rotate on push) | Stack using Queues (LC 225) | Easy |

## 11.2 資料結構的「能力表」

```
             查找    插入    刪除    有序  取極值  前綴搜尋
HashMap      O(1)    O(1)    O(1)    ✗      ✗        ✗
Array        O(n)*   O(1)**  O(n)    ✗      O(n)     ✗
Sorted Array O(logn) O(n)    O(n)    ✓      O(1)     O(logn)
Linked List  O(n)    O(1)*** O(1)***  ✓      O(n)     ✗
Heap         O(n)    O(logn) O(logn) 部分   O(1)     ✗
BST (balanced) O(logn) O(logn) O(logn) ✓    O(logn)  ✗
Trie         O(m)    O(m)    O(m)    ✗      ✗        O(m)

* Array: O(1) by index, O(n) by value
** Array: O(1) append to end
*** Linked List: O(1) if you have the pointer to the position
```

**如何使用這張表**：
1. 列出你的操作需求
2. 在表中找到每個操作最佳的結構
3. 如果沒有一個結構能同時滿足 → 組合它們

## 11.3 經典的「組合模式」

```
模式 1: HashMap + Ordered Structure
  用途: O(1) 查找 + 維護某種順序
  例子: LRU (HashMap + DLL), LFU (HashMap + FreqMap)

模式 2: HashMap + Array
  用途: O(1) 查找 + O(1) 隨機存取
  例子: Insert Delete GetRandom O(1) (LC 380)
  技巧: 刪除時把目標和 array 最後一個 swap，再 pop

模式 3: Two Stacks / Two Queues
  用途: 模擬另一種 LIFO/FIFO 行為
  例子: Min Stack, Queue from Stacks

模式 4: Trie + DFS/BFS
  用途: 字串搜尋 + 枚舉所有匹配
  例子: Word Search II (LC 212), Auto-complete

模式 5: Heap + HashMap
  用途: 動態維護 Top K + 快速查找
  例子: Top K Frequent Elements (LC 347), Design Twitter
```

## 11.4 面試快速決策流程

```
面試官說 "Design a ..."

你的腦中流程：

1. 列出所有操作 → 寫在白板左邊
2. 每個操作旁邊寫複雜度要求
3. 問自己：有沒有 O(1) 查找的需求？
   → Yes → 一定有 HashMap
4. 問自己：有沒有「順序」的需求？（最近/最久/頻率）
   → Yes → 需要 Linked List 或 Heap
5. 問自己：HashMap 能不能單獨解決？
   → No → 找第二個結構來補
6. 畫出兩個結構的關係圖
7. 跟面試官確認設計
8. 開始寫 code
```

---

## 總結：Design 題的核心心法

```
一句話總結：
  Design 題 = 辨識操作需求 + 選對資料結構 + 組合它們

三個核心能力：
  1. 熟悉每種資料結構的「能」與「不能」
  2. 能快速辨識 "O(1) 查找 + 順序維護 = HashMap + DLL" 這類模式
  3. 能用例子逐步追蹤，驗證設計正確性

最重要的五題（按優先度）：
  ★★★★★ LRU Cache (LC 146)     — 面試出現率最高
  ★★★★★ Implement Trie (LC 208) — 字串題的基石
  ★★★★★ Serialize Binary Tree (LC 297) — Google 愛考
  ★★★★☆ Design Twitter (LC 355) — 綜合能力展現
  ★★★★☆ Min Stack (LC 155)      — 基礎但必須秒殺
```
