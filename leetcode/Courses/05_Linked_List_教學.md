# Linked List 鏈結串列 -- 從零到 Google 面試完全教學

> **對象**：基礎薄弱、準備 Google 面試的工程師
> **原則**：每個指標變化都畫圖、每個概念至少 2 個範例、不跳步驟

---

## 第一章：Linked List 基礎 -- 從零開始

### 1.1 什麼是 Linked List？

**Array（陣列）** 是一塊連續的記憶體，元素緊挨著放。
**Linked List（鏈結串列）** 是一群散落在記憶體各處的 **節點（Node）**，每個節點用 **指標（Pointer）** 串在一起。

```
Array:
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │    記憶體連續
└───┴───┴───┴───┴───┘

Linked List:
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬──────┐
│ 1 │ ──┼───>│ 2 │ ──┼───>│ 3 │ ──┼───>│ 4 │ None │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴──────┘
 val  next    val  next    val  next    val   next
```

每個節點（Node）有兩個欄位：
- `val`：儲存的資料
- `next`：指向下一個節點的指標（最後一個指向 `None`）

### 1.2 Array vs Linked List 完整比較

| 操作 | Array | Linked List | 誰贏？ |
|------|-------|-------------|--------|
| **隨機存取** Access by index | O(1) 直接算位址 | O(n) 要從頭走 | Array |
| **頭部插入** Insert at head | O(n) 全部後移 | O(1) 改指標 | Linked List |
| **尾部插入** Insert at tail | O(1) amortized | O(n) 要走到尾 * | 看情況 |
| **中間插入** Insert at middle | O(n) 後半後移 | O(1) ** 改指標 | Linked List |
| **刪除** Delete | O(n) 後半前移 | O(1) ** 改指標 | Linked List |
| **記憶體** Memory | 連續、cache friendly | 分散、多用指標空間 | Array |

> \* 如果有 tail pointer 則尾部插入也是 O(1)
> \** 前提是你已經站在要插入/刪除的位置

**插入圖解 -- 在 2 和 3 之間插入 9：**

```
Array: 要把 3, 4, 5 全部往後搬  O(n)
┌───┬───┬───┬───┬───┐         ┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │   =>   │ 1 │ 2 │ 9 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┴───┘

Linked List: 只改兩個指標  O(1)
Before:  1 -> 2 -> 3 -> 4 -> None
                ↑
           改這裡的 next

After:   1 -> 2 -> 9 -> 3 -> 4 -> None
              │    ↑
              └────┘  2.next = 9, 9.next = 3
```

### 1.3 三種 Linked List

**1. Singly Linked List（單向鏈結串列）** -- 最常考！

```
head
 ↓
[1] -> [2] -> [3] -> [4] -> None

每個節點只有 next，只能往前走，不能回頭
```

**2. Doubly Linked List（雙向鏈結串列）**

```
None <-> [1] <-> [2] <-> [3] <-> [4] <-> None

每個節點有 prev 和 next，可以前後走
常用於：LRU Cache、瀏覽器上一頁/下一頁
```

**3. Circular Linked List（環形鏈結串列）**

```
[1] -> [2] -> [3] -> [4] --+
 ↑                          |
 +--------------------------+

最後一個節點的 next 指回 head，形成一個環
常用於：約瑟夫問題、循環佇列
```

### 1.4 Python 中的 ListNode 定義

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 儲存資料
        self.next = next    # 指向下一個節點（預設 None）
```

**建立 1 -> 2 -> 3 -> None：**

```python
# 方法一：一個一個建
node3 = ListNode(3)          # [3] -> None
node2 = ListNode(2, node3)   # [2] -> [3] -> None
node1 = ListNode(1, node2)   # [1] -> [2] -> [3] -> None
head = node1

# 方法二：從 list 建（面試常用的 helper）
def build_list(vals):
    if not vals:
        return None
    head = ListNode(vals[0])
    curr = head
    for v in vals[1:]:
        curr.next = ListNode(v)
        curr = curr.next
    return head

head = build_list([1, 2, 3])  # [1] -> [2] -> [3] -> None
```

### 1.5 遍歷 Linked List -- 最基本的操作

```python
def traverse(head):
    curr = head
    while curr is not None:    # 或寫 while curr:
        print(curr.val)
        curr = curr.next       # 移到下一個
```

**範例：走過 1 -> 2 -> 3 -> None**

```
初始:  curr = head = [1]
       curr
        ↓
       [1] -> [2] -> [3] -> None

第 1 步: 印出 1, curr = curr.next
               curr
                ↓
       [1] -> [2] -> [3] -> None

第 2 步: 印出 2, curr = curr.next
                      curr
                       ↓
       [1] -> [2] -> [3] -> None

第 3 步: 印出 3, curr = curr.next
                             curr
                              ↓
       [1] -> [2] -> [3] -> None (curr = None)

curr 是 None，while 結束！
```

---

## 第二章：反轉鏈結串列 -- 面試最愛

> 反轉鏈結串列是 **面試出現頻率最高** 的 Linked List 題目。
> Google、Meta、Amazon 都愛考。務必練到閉著眼睛也能寫。

### 2.1 Reverse Linked List (LC 206) -- Iterative 迭代法

**核心想法**：用三個指標 `prev`, `curr`, `nxt`，每一步把 `curr` 的箭頭反轉。

**公式（每一步重複）：**
```
nxt = curr.next       # 1. 先記住下一個（不然等等斷了找不到）
curr.next = prev      # 2. 反轉！curr 的箭頭指向前面
prev = curr           # 3. prev 往前走
curr = nxt            # 4. curr 往前走
```

#### 範例 1：反轉 1 -> 2 -> 3 -> 4 -> 5

```
初始狀態:
  prev = None
  curr = [1] -> [2] -> [3] -> [4] -> [5] -> None

┌──────────────────────────────────────────────────┐
│ Step 1                                           │
│ nxt = curr.next = [2]                            │
│                                                  │
│ curr.next = prev:                                │
│   None <- [1]    [2] -> [3] -> [4] -> [5] -> None│
│                                                  │
│ prev = curr = [1]                                │
│ curr = nxt = [2]                                 │
│                                                  │
│ 狀態: prev=[1], curr=[2]                         │
│   None <- [1]    [2] -> [3] -> [4] -> [5] -> None│
│            ↑      ↑                              │
│          prev   curr                             │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Step 2                                           │
│ nxt = curr.next = [3]                            │
│                                                  │
│ curr.next = prev:                                │
│   None <- [1] <- [2]    [3] -> [4] -> [5] -> None│
│                                                  │
│ prev = curr = [2]                                │
│ curr = nxt = [3]                                 │
│                                                  │
│ 狀態: prev=[2], curr=[3]                         │
│   None <- [1] <- [2]    [3] -> [4] -> [5] -> None│
│                   ↑      ↑                       │
│                 prev   curr                      │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Step 3                                           │
│ nxt = curr.next = [4]                            │
│                                                  │
│ curr.next = prev:                                │
│   None <- [1] <- [2] <- [3]    [4] -> [5] -> None│
│                                                  │
│ prev = curr = [3]                                │
│ curr = nxt = [4]                                 │
│                                                  │
│ 狀態: prev=[3], curr=[4]                         │
│   None <- [1] <- [2] <- [3]    [4] -> [5] -> None│
│                          ↑      ↑                │
│                        prev   curr               │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Step 4                                           │
│ nxt = curr.next = [5]                            │
│                                                  │
│ curr.next = prev:                                │
│   None <- [1] <- [2] <- [3] <- [4]    [5] -> None│
│                                                  │
│ prev = curr = [4]                                │
│ curr = nxt = [5]                                 │
│                                                  │
│ 狀態: prev=[4], curr=[5]                         │
│   None <- [1] <- [2] <- [3] <- [4]    [5] -> None│
│                                  ↑      ↑        │
│                                prev   curr       │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Step 5                                           │
│ nxt = curr.next = None                           │
│                                                  │
│ curr.next = prev:                                │
│   None <- [1] <- [2] <- [3] <- [4] <- [5]       │
│                                                  │
│ prev = curr = [5]                                │
│ curr = nxt = None                                │
│                                                  │
│ 狀態: prev=[5], curr=None → while 結束！          │
│   None <- [1] <- [2] <- [3] <- [4] <- [5]       │
│                                         ↑        │
│                                       prev       │
│                                    (new head!)    │
└──────────────────────────────────────────────────┘

結果: 5 -> 4 -> 3 -> 2 -> 1 -> None
```

#### 範例 2：反轉 1 -> 2（最小情況）

```
初始: prev=None, curr=[1]->[2]->None

Step 1: nxt=[2]
        curr.next = None  =>  None <- [1]   [2] -> None
        prev=[1], curr=[2]

Step 2: nxt=None
        curr.next = [1]  =>  None <- [1] <- [2]
        prev=[2], curr=None → 結束

結果: 2 -> 1 -> None
```

#### Corner Cases 邊界情況

```
空串列:  head = None → 直接 return None（while 不會執行）
單節點:  head = [7] -> None → prev=None, curr=[7]
         Step 1: nxt=None, curr.next=None, prev=[7], curr=None
         結果: [7] -> None（不變）
```

#### 完整程式碼

```python
def reverseList(head: ListNode) -> ListNode:
    prev, curr = None, head
    while curr:
        nxt = curr.next      # 記住下一個
        curr.next = prev     # 反轉箭頭
        prev = curr          # prev 前進
        curr = nxt           # curr 前進
    return prev              # prev 就是新的 head
```

**Time: O(n)** -- 每個節點走一次
**Space: O(1)** -- 只用三個指標變數

---

### 2.2 Reverse Linked List -- Recursive 遞迴法

**遞迴版最難的部分**：理解 recursion「回溯（unwind）」的時候在做什麼。

**核心邏輯：**
```python
def reverseList(head):
    # Base case: 空的或只有一個節點
    if not head or not head.next:
        return head

    # 遞迴：先把 head 後面的全部反轉
    new_head = reverseList(head.next)

    # 回溯時：讓「下一個節點」指回自己
    head.next.next = head
    head.next = None

    return new_head
```

#### 範例 1：反轉 1 -> 2 -> 3

```
呼叫 reverseList([1] -> [2] -> [3] -> None)
│
├─ head = [1], head.next = [2]
│  遞迴呼叫 reverseList([2] -> [3] -> None)
│  │
│  ├─ head = [2], head.next = [3]
│  │  遞迴呼叫 reverseList([3] -> None)
│  │  │
│  │  ├─ head = [3], head.next = None
│  │  │  ★ Base case! return [3]    ← new_head = [3]
│  │  │
│  │  回溯到 head=[2]:
│  │  new_head = [3]
│  │
│  │  執行 head.next.next = head:
│  │    [3].next = [2]
│  │    目前: [1] -> [2] <-> [3]    （[2] 和 [3] 互指！）
│  │
│  │  執行 head.next = None:
│  │    [2].next = None
│  │    目前: [1] -> X   None <- [2] <- [3]
│  │                              ↑
│  │    [1] 仍然指向 [2]（但 [2].next 已經是 None）
│  │
│  │  return new_head = [3]
│  │
│  回溯到 head=[1]:
│  new_head = [3]
│
│  執行 head.next.next = head:
│    [2].next = [1]
│    目前: None <- [3] <- [2]   [1] -> [2]
│                                但 [2].next 剛被改成 [1]
│                         所以: None <- [3] <- [2] <- [1]
│                                               ↑
│                                       但 [1] 還指向 [2]！
│
│  執行 head.next = None:
│    [1].next = None
│    最終: None <- [3] <- [2] <- [1] -> None
│
│  return new_head = [3]

結果: [3] -> [2] -> [1] -> None
```

#### 範例 2：反轉 5 -> 10

```
呼叫 reverseList([5] -> [10] -> None)
│
├─ head = [5], head.next = [10]
│  遞迴呼叫 reverseList([10] -> None)
│  │
│  ├─ head = [10], head.next = None
│  │  ★ Base case! return [10]
│  │
│  回溯到 head=[5]:
│  new_head = [10]
│
│  head.next.next = head:
│    [10].next = [5]
│    狀態: [5] <-> [10]
│
│  head.next = None:
│    [5].next = None
│    狀態: None <- [5] <- [10]
│
│  return [10]

結果: [10] -> [5] -> None
```

**Time: O(n)**, **Space: O(n)**（遞迴堆疊深度 n）

> **面試建議**：先寫 iterative，被問到才寫 recursive。Iterative 空間 O(1) 更優。

---

## 第三章：快慢指標 (Fast-Slow Pointers)

> 快慢指標是 Linked List 最重要的技巧之一。
> 核心概念：`slow` 每次走 1 步，`fast` 每次走 2 步。

### 3.1 Middle of Linked List (LC 876)

**題目**：找到鏈結串列的中間節點。如果有兩個中間節點，回傳第二個。

**為什麼快慢指標能找到中間？**
想像兩個人在跑道上跑步，一個跑一倍速、一個跑兩倍速。
當快的那個到達終點時，慢的剛好在中間！

```
slow 走了 k 步 → fast 走了 2k 步
fast 到尾巴 (走了 n 步) → slow 走了 n/2 步 → 剛好中間！
```

#### 範例 1：1 -> 2 -> 3 -> 4 -> 5（奇數個節點）

```
初始: slow = fast = [1]

  slow fast
   ↓    ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> None

Step 1: slow = slow.next = [2]
        fast = fast.next.next = [3]

         slow        fast
          ↓           ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> None

Step 2: slow = slow.next = [3]
        fast = fast.next.next = [5]

                slow               fast
                 ↓                  ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> None

檢查: fast.next = None → while 條件不滿足 → 結束！
slow = [3] ← 這就是中間節點！

驗證: 1,2,[3],4,5  ✓ 第 3 個確實是中間
```

#### 範例 2：1 -> 2 -> 3 -> 4 -> 5 -> 6（偶數個節點）

```
初始: slow = fast = [1]

Step 1: slow=[2], fast=[3]

         slow        fast
          ↓           ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> [6] -> None

Step 2: slow=[3], fast=[5]

                slow               fast
                 ↓                  ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> [6] -> None

Step 3: slow=[4], fast=None (fast.next.next 跳過 [6] 的 next)

                        slow                       fast
                         ↓                          ↓
  [1] -> [2] -> [3] -> [4] -> [5] -> [6] -> None  (已到底)

fast = None → while 條件不滿足 → 結束！
slow = [4] ← 偶數情況回傳第二個中間節點

驗證: 1,2,3,[4],5,6  ✓ 兩個中間是 3 和 4，回傳 4
```

#### 程式碼

```python
def middleNode(head: ListNode) -> ListNode:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Time: O(n)**, **Space: O(1)**

---

### 3.2 Linked List Cycle Detection (LC 141)

**題目**：判斷鏈結串列是否有環（cycle）。

**Floyd's Tortoise and Hare（龜兔演算法）**

想像兩個人在圓形跑道上跑步：
- 慢的（tortoise 烏龜）走 1 步
- 快的（hare 兔子）走 2 步
- 如果跑道是圓的，**快的一定會追上慢的**（就像快車繞操場追慢車）
- 如果跑道是直線（沒有環），快的會先到終點

#### 範例 1：有環 -- [3, 2, 0, -4]，尾巴接到 index 1（值=2）

```
結構:
  [3] -> [2] -> [0] -> [-4]
          ↑              |
          +--------------+     （-4 的 next 指向 2，形成環）

初始: slow = fast = [3]

Step 1: slow = [2], fast = [0]
         s          f
         ↓          ↓
  [3] -> [2] -> [0] -> [-4]
          ↑              |
          +--------------+

Step 2: slow = [0], fast = [2]  (fast: [0]->[-4]->...next=>[2])
                s    f
                ↓    ↓
  [3] -> [2] -> [0] -> [-4]
          ↑              |
          +--------------+
  (fast 從 [0] 走兩步: [0]->[−4]->[2])

Step 3: slow = [-4], fast = [-4]
                        s,f
                         ↓
  [3] -> [2] -> [0] -> [-4]
          ↑              |
          +--------------+
  (slow 從 [0]->[−4]，fast 從 [2]->[0]->[-4])

slow == fast! 有環！return True
```

#### 範例 2：無環 -- [1, 2, 3, 4]

```
  [1] -> [2] -> [3] -> [4] -> None

初始: slow = fast = [1]

Step 1: slow=[2], fast=[3]
Step 2: slow=[3], fast=None (fast: [3]->[4]->None, 再走一步越界)

fast = None → while 條件不滿足 → 結束
沒有相遇 → 無環！return False
```

#### 程式碼

```python
def hasCycle(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:       # 用 is 比較（同一個物件）
            return True
    return False
```

**Time: O(n)**, **Space: O(1)**

---

### 3.3 Linked List Cycle II (LC 142) -- 找環的入口

**題目**：不只判斷有沒有環，還要找到環的 **入口節點（entrance）**。

這題需要分兩個階段：
1. **Phase 1**：用快慢指標找到相遇點
2. **Phase 2**：從 head 和相遇點同時走，再次相遇處就是入口

#### 數學證明 -- 為什麼這樣做？

```
         F              a
head --------> entrance -----> meeting point
                  |                 |
                  |     C (環長)     |
                  +<---- (C - a) ---+

定義:
  F = head 到 entrance 的距離
  a = entrance 到 meeting point 的距離
  C = 環的長度

Phase 1 結束時:
  slow 走了: F + a 步
  fast 走了: F + a + n*C 步 (在環裡多繞了 n 圈)

  因為 fast 速度是 slow 的 2 倍:
    2(F + a) = F + a + n*C
    F + a = n*C
    F = n*C - a

這代表什麼？
  從 head 走 F 步 = 到 entrance
  從 meeting point 走 n*C - a 步:
    先走 C - a 步到 entrance（繞回入口），
    再繞 (n-1) 圈回到 entrance

  所以從 head 和 meeting point 同時出發，每次走一步，
  一定在 entrance 相遇！
```

#### 範例 1：[3, 2, 0, -4]，尾巴接到 index 1

```
        F=1         a=1
  [3] -------> [2] -----> [0] -> [-4]
                ↑                  |
                +------ C=3 ------+
                     (C-a=2)

Phase 1: 找相遇點
  初始: slow = fast = [3]

  Step 1: slow=[2], fast=[0]
  Step 2: slow=[0], fast=[2]
          (fast: [0]->[-4]->[2])
  Step 3: slow=[-4], fast=[-4]
          相遇在 [-4]！

Phase 2: 找入口
  ptr 從 head [3] 出發，slow 從相遇點 [-4] 出發

  Step 1: ptr=[2], slow=[2]
          (ptr: [3]->[2]，slow: [-4]->[2])

  ptr == slow！入口是 [2]！

驗證: F=1 步從 head 到 [2]，C-a = 3-1 = 2 步從 [-4] 到 [2]
     但 [-4] 只走了 1 步就到 [2]？
     因為 F = n*C - a = 1*3 - 2 = 1 ✓
```

#### 範例 2：[1, 2, 3, 4, 5]，尾巴接到 index 2（值=3）

```
          F=2            a=?
  [1] -> [2] -> [3] -> [4] -> [5]
                 ↑              |
                 +---- C=3 ----+

Phase 1: 找相遇點
  初始: slow = fast = [1]

  Step 1: slow=[2], fast=[3]
  Step 2: slow=[3], fast=[5]
          (fast: [3]->[4]->[5])
  Step 3: slow=[4], fast=[4]
          (slow: [3]->[4]，fast: [5]->[3]->[4])
          相遇在 [4]！

  所以 a = 1（從 entrance [3] 到 meeting [4] 距離 1）

Phase 2: 找入口
  ptr 從 head [1]，slow 從相遇點 [4]

  Step 1: ptr=[2], slow=[5]
          (ptr: [1]->[2]，slow: [4]->[5])
  Step 2: ptr=[3], slow=[3]
          (ptr: [2]->[3]，slow: [5]->[3])

  ptr == slow！入口是 [3]！

驗證: F=2, a=1, C=3
     F = n*C - a = 1*3 - 1 = 2 ✓
```

#### 程式碼

```python
def detectCycle(head: ListNode) -> ListNode:
    slow = fast = head

    # Phase 1: 找相遇點
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None          # 無環

    # Phase 2: 找入口
    ptr = head
    while ptr is not slow:
        ptr = ptr.next
        slow = slow.next
    return ptr               # 入口節點
```

**Time: O(n)**, **Space: O(1)**

---

## 第四章：合併與排序

### 4.1 Merge Two Sorted Lists (LC 21)

**題目**：合併兩個已排序的鏈結串列。

**核心想法**：比較兩個串列的頭，挑小的接上去。

**Dummy Node 技巧**：建立一個假的頭節點，這樣就不用特別處理「第一個節點」的邊界情況。

```
為什麼需要 dummy node？

沒有 dummy: 你需要先判斷誰是新 head，然後才能開始接
有 dummy:   永遠從 dummy 開始接，最後回傳 dummy.next

  dummy -> (接在這裡)
```

#### 範例 1：L1 = 1->2->4, L2 = 1->3->4

```
初始:
  L1: [1] -> [2] -> [4] -> None
  L2: [1] -> [3] -> [4] -> None
  dummy -> None    (tail 指向 dummy)

Step 1: L1.val(1) <= L2.val(1), pick L1 的 [1]
  dummy -> [1]
  L1 前進: L1 = [2] -> [4]
  L2 不動: L2 = [1] -> [3] -> [4]
  tail = [1]

Step 2: L1.val(2) > L2.val(1), pick L2 的 [1]
  dummy -> [1] -> [1]
  L1 不動: L1 = [2] -> [4]
  L2 前進: L2 = [3] -> [4]
  tail = [1]  (第二個 1)

Step 3: L1.val(2) < L2.val(3), pick L1 的 [2]
  dummy -> [1] -> [1] -> [2]
  L1 前進: L1 = [4]
  L2 不動: L2 = [3] -> [4]
  tail = [2]

Step 4: L1.val(4) > L2.val(3), pick L2 的 [3]
  dummy -> [1] -> [1] -> [2] -> [3]
  L1 不動: L1 = [4]
  L2 前進: L2 = [4]
  tail = [3]

Step 5: L1.val(4) <= L2.val(4), pick L1 的 [4]
  dummy -> [1] -> [1] -> [2] -> [3] -> [4]
  L1 前進: L1 = None
  L2 不動: L2 = [4]
  tail = [4]

L1 = None → while 結束
剩餘 L2 = [4] 直接接上:
  dummy -> [1] -> [1] -> [2] -> [3] -> [4] -> [4] -> None

回傳 dummy.next = [1] -> [1] -> [2] -> [3] -> [4] -> [4] -> None
```

#### 範例 2：L1 = 2->5, L2 = 1->3->7

```
Step 1: L1.val(2) > L2.val(1), pick [1]    → dummy->[1]
Step 2: L1.val(2) < L2.val(3), pick [2]    → dummy->[1]->[2]
Step 3: L1.val(5) > L2.val(3), pick [3]    → dummy->[1]->[2]->[3]
Step 4: L1.val(5) < L2.val(7), pick [5]    → dummy->[1]->[2]->[3]->[5]
L1=None, append L2=[7]:                     → dummy->[1]->[2]->[3]->[5]->[7]

結果: 1 -> 2 -> 3 -> 5 -> 7 -> None
```

#### 程式碼

```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(-1)     # dummy node
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2    # 接上剩餘部分
    return dummy.next
```

**Time: O(n+m)**, **Space: O(1)**

---

### 4.2 Sort List (LC 148) -- Merge Sort on Linked List

**題目**：排序一個鏈結串列。要求 O(n log n) 時間。

**為什麼用 Merge Sort？**
- Linked List 不支援隨機存取 → Quick Sort 的 partition 不方便
- Merge Sort 天然適合 Linked List：找中點切半 → 遞迴排序 → 合併

**步驟**：
1. 用快慢指標找中點
2. 從中點斷開，分成左右兩半
3. 遞迴排序左右
4. 合併兩個已排序串列

#### 範例：排序 4 -> 2 -> 1 -> 3

```
                    sort([4,2,1,3])
                   /               \
            找中點，斷開
           /                        \
    sort([4,2])                sort([1,3])
      /       \                  /       \
   找中點     找中點           找中點     找中點
   /    \     /    \           /    \     /    \
sort([4]) sort([2])      sort([1]) sort([3])
   |         |              |         |
  [4]       [2]            [1]       [3]
   \       /                \       /
  merge([4],[2])          merge([1],[3])
       |                       |
   [2] -> [4]             [1] -> [3]
       \                   /
      merge([2,4], [1,3])
              |
      [1] -> [2] -> [3] -> [4]

詳細 merge 過程 (merge [2,4] 和 [1,3]):
  Step 1: 2 > 1, pick [1]  → [1]
  Step 2: 2 < 3, pick [2]  → [1]->[2]
  Step 3: 4 > 3, pick [3]  → [1]->[2]->[3]
  剩餘 [4] 接上:            → [1]->[2]->[3]->[4]
```

#### 程式碼

```python
def sortList(head: ListNode) -> ListNode:
    # Base case
    if not head or not head.next:
        return head

    # Step 1: 找中點（注意 fast 從 head.next 開始，確保偶數時左半較短）
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: 從中點斷開
    mid = slow.next
    slow.next = None

    # Step 3: 遞迴排序
    left = sortList(head)
    right = sortList(mid)

    # Step 4: 合併
    return mergeTwoLists(left, right)
```

**Time: O(n log n)**, **Space: O(log n)** 遞迴堆疊

---

## 第五章：經典技巧

### 5.1 Remove Nth Node From End of List (LC 19)

**題目**：移除倒數第 n 個節點。要求 one-pass。

**Two-pointer gap 技巧**：
讓 `fast` 先走 n 步，然後 `fast` 和 `slow` 一起走。
當 `fast` 到尾巴時，`slow` 就在要刪除的節點 **前面**。

```
為什麼？

fast 先走 n 步 → fast 和 slow 之間差 n 步
當 fast 到結尾 → slow 在距離結尾 n 步的位置
也就是 → slow.next 就是倒數第 n 個！
```

#### 範例 1：1->2->3->4->5, n=2（刪除倒數第 2 個 = 刪除 4）

```
使用 dummy node（因為可能刪除 head）

dummy -> [1] -> [2] -> [3] -> [4] -> [5] -> None

Step 1: fast 先走 n+1 = 3 步
  fast 走 1 步: fast = [1]
  fast 走 2 步: fast = [2]
  fast 走 3 步: fast = [3]

  slow                          fast
   ↓                             ↓
  dummy -> [1] -> [2] -> [3] -> [4] -> [5] -> None

Step 2: fast 和 slow 一起走，直到 fast = None

  一起走 1 步: slow=[1], fast=[4]
           slow                  fast
            ↓                     ↓
  dummy -> [1] -> [2] -> [3] -> [4] -> [5] -> None

  一起走 2 步: slow=[2], fast=[5]
                  slow                  fast
                   ↓                     ↓
  dummy -> [1] -> [2] -> [3] -> [4] -> [5] -> None

  一起走 3 步: slow=[3], fast=None
                         slow                  fast
                          ↓                     ↓
  dummy -> [1] -> [2] -> [3] -> [4] -> [5] -> None

fast = None → 停！

Step 3: 刪除 slow.next = [4]
  slow.next = slow.next.next
  [3].next = [5]

  dummy -> [1] -> [2] -> [3] -> [5] -> None

結果: 1 -> 2 -> 3 -> 5 -> None ✓
```

#### 範例 2：1->2, n=2（刪除倒數第 2 個 = 刪除 head [1]）

```
dummy -> [1] -> [2] -> None

fast 先走 n+1 = 3 步:
  fast 走 1 步: [1]
  fast 走 2 步: [2]
  fast 走 3 步: None

slow = dummy, fast = None → while 直接結束

slow.next = slow.next.next
dummy.next = [2]

結果: 2 -> None ✓

(這就是 dummy node 的價值 -- 不用特判刪除 head 的情況！)
```

#### 程式碼

```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    fast = slow = dummy

    # fast 先走 n+1 步
    for _ in range(n + 1):
        fast = fast.next

    # 一起走
    while fast:
        fast = fast.next
        slow = slow.next

    # 刪除 slow.next
    slow.next = slow.next.next
    return dummy.next
```

**Time: O(n)**, **Space: O(1)**

---

### 5.2 Add Two Numbers (LC 2)

**題目**：兩個非負整數以反向 linked list 表示，求和。
- 342 存成 2 -> 4 -> 3
- 465 存成 5 -> 6 -> 4

**核心**：模擬手算加法，處理進位（carry）。

#### 範例 1：342 + 465 = 807

```
  L1: [2] -> [4] -> [3] -> None     (代表 342)
  L2: [5] -> [6] -> [4] -> None     (代表 465)
  carry = 0

Step 1 (個位): 2 + 5 + carry(0) = 7
  digit = 7, carry = 0
  result: dummy -> [7]
  L1=[4], L2=[6]

Step 2 (十位): 4 + 6 + carry(0) = 10
  digit = 0, carry = 1
  result: dummy -> [7] -> [0]
  L1=[3], L2=[4]

Step 3 (百位): 3 + 4 + carry(1) = 8
  digit = 8, carry = 0
  result: dummy -> [7] -> [0] -> [8]
  L1=None, L2=None

carry = 0, 且 L1=L2=None → 結束

結果: 7 -> 0 -> 8 -> None (代表 807) ✓
```

#### 範例 2：999 + 1 = 1000

```
  L1: [9] -> [9] -> [9] -> None     (代表 999)
  L2: [1] -> None                    (代表 1)
  carry = 0

Step 1: 9 + 1 + 0 = 10, digit=0, carry=1
  result: dummy -> [0]
  L1=[9], L2=None

Step 2: 9 + 0 + 1 = 10, digit=0, carry=1
  (L2 已經是 None, 所以 v2=0)
  result: dummy -> [0] -> [0]
  L1=[9], L2=None

Step 3: 9 + 0 + 1 = 10, digit=0, carry=1
  result: dummy -> [0] -> [0] -> [0]
  L1=None, L2=None

L1=None, L2=None, 但 carry=1！還要繼續！

Step 4: 0 + 0 + 1 = 1, digit=1, carry=0
  result: dummy -> [0] -> [0] -> [0] -> [1]

結果: 0 -> 0 -> 0 -> 1 -> None (代表 1000) ✓
```

#### 程式碼

```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry

        carry = total // 10
        digit = total % 10

        curr.next = ListNode(digit)
        curr = curr.next

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
```

**Time: O(max(m,n))**, **Space: O(max(m,n))**

> **重要**：while 條件是 `l1 or l2 or carry`，別忘了最後的 carry！

---

### 5.3 Palindrome Linked List (LC 234)

**題目**：判斷鏈結串列是否是回文（palindrome）。

**策略**（三步驟）：
1. 找中點（快慢指標）
2. 反轉後半段
3. 逐一比較前半和反轉後的後半

#### 範例：1 -> 2 -> 2 -> 1（是回文）

```
原始: [1] -> [2] -> [2] -> [1] -> None

=== Step 1: 找中點 ===
  slow=[1], fast=[1]
  Step 1: slow=[2], fast=[2] (第二個 2)
  fast.next = [1], fast.next.next = None → while 結束
  slow 停在 [2]（第一個 2）← 這是前半的最後一個節點

=== Step 2: 反轉後半段 ===
  後半段: slow.next = [2] -> [1] -> None
  斷開: slow.next = None

  前半: [1] -> [2] -> None
  後半: [2] -> [1] -> None

  反轉後半:
    prev=None, curr=[2]
    Step 1: [2].next=None → None<-[2], prev=[2], curr=[1]
    Step 2: [1].next=[2] → [1]->[2], prev=[1], curr=None

  反轉後: [1] -> [2] -> None

=== Step 3: 逐一比較 ===
  前半: [1] -> [2] -> None
  反轉後半: [1] -> [2] -> None

  比較 1: p1.val=1, p2.val=1 → 相同 ✓
  比較 2: p1.val=2, p2.val=2 → 相同 ✓
  p2 = None → 結束

  全部相同 → 是回文！return True
```

**再看一個不是回文的例子：1 -> 2 -> 3**

```
原始: [1] -> [2] -> [3] -> None

Step 1: 找中點
  slow=[2]（奇數情況，slow 在正中間）

Step 2: 反轉後半
  後半 = [3] -> None，反轉後 = [3] -> None
  前半 = [1] -> [2] -> None

Step 3: 比較
  p1.val=1, p2.val=3 → 不同！return False
```

#### 程式碼

```python
def isPalindrome(head: ListNode) -> bool:
    if not head or not head.next:
        return True

    # Step 1: 找中點（slow 停在前半末尾）
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: 反轉後半
    second_half = slow.next
    slow.next = None           # 斷開
    prev = None
    curr = second_half
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    reversed_half = prev       # 反轉後的頭

    # Step 3: 逐一比較
    p1, p2 = head, reversed_half
    while p2:                  # 後半可能較短（奇數情況）
        if p1.val != p2.val:
            return False
        p1 = p1.next
        p2 = p2.next
    return True
```

**Time: O(n)**, **Space: O(1)**

---

## 第六章：Dummy Node 技巧總結

### 6.1 什麼時候用 Dummy Node？

**規則：只要 head 可能被改變或刪除，就用 dummy node。**

```
常見場景:
1. 合併兩個串列     → head 不確定是誰的，用 dummy 開始建
2. 刪除節點         → 可能刪到 head，用 dummy 避免特判
3. 分隔串列         → 建新串列從空開始
4. 兩數相加         → 結果串列從空開始建

不需要 dummy 的場景:
1. 反轉串列         → head 不會被刪除（只是改方向）
2. 找中點           → 只是讀取，不修改結構
3. 環偵測           → 只是讀取
```

### 6.2 Dummy Node 模板

```python
def some_operation(head):
    dummy = ListNode(0)       # 建立假頭
    dummy.next = head         # 或 dummy.next = None（建新串列時）

    # ... 所有操作 ...

    return dummy.next         # 真正的 head
```

### 6.3 面試提示

```
1. 先問清楚：串列可能為空嗎？只有一個節點呢？
2. 如果 head 可能被刪/改 → 主動用 dummy node，面試官會欣賞
3. 不要忘記斷尾：操作完後確認最後一個節點 .next = None
4. 反轉是基礎中的基礎，Google 特別愛在此基礎上出變形題
5. 快慢指標 = 找中點 + 環偵測，記住這兩個用途就夠了
```

---

## 附錄：解題速查表

| 題目 | 核心技巧 | Time | Space | 難度 |
|------|----------|------|-------|------|
| LC 206 Reverse Linked List | prev/curr/nxt 三指標 | O(n) | O(1) | Easy |
| LC 876 Middle of Linked List | 快慢指標 | O(n) | O(1) | Easy |
| LC 141 Linked List Cycle | Floyd 快慢指標 | O(n) | O(1) | Easy |
| LC 21 Merge Two Sorted Lists | Dummy + 比較 | O(n+m) | O(1) | Easy |
| LC 2 Add Two Numbers | Dummy + carry | O(n) | O(n) | Medium |
| LC 19 Remove Nth From End | 雙指標 gap | O(n) | O(1) | Medium |
| LC 234 Palindrome Linked List | 找中 + 反轉 + 比較 | O(n) | O(1) | Medium |
| LC 142 Linked List Cycle II | Floyd + 數學 | O(n) | O(1) | Medium |
| LC 148 Sort List | Merge Sort | O(n log n) | O(log n) | Medium |

### 面試答題 SOP

```
1. 確認輸入：「串列可能為空嗎？有環嗎？值的範圍？」
2. 說出方法：「我打算用 [技巧名稱]，Time O(?), Space O(?)」
3. 畫圖確認：面試時在白板上畫 pointer 狀態
4. 寫程式碼：邊寫邊講每一行在做什麼
5. 測試：用簡單範例 dry-run，別忘了 edge cases
   - 空串列 (None)
   - 單節點 ([1] -> None)
   - 兩個節點 ([1] -> [2] -> None)
```
