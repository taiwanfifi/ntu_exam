# LeetCode 08 - Tree BFS & BST 完整教學

> 目標讀者：基礎較弱、準備 Google 面試的工程師
> 教學方式：每個概念至少 2 個完整 step-by-step 數值追蹤範例，所有樹都畫 ASCII art
> 語言：繁體中文 + English terms

---

## 目錄

- [第一章：BFS 層序遍歷 — 用 Queue 一層一層走](#第一章bfs-層序遍歷--用-queue-一層一層走)
  - [1.1 Level Order Traversal (LC 102)](#11-level-order-traversal-lc-102)
  - [1.2 Zigzag Level Order Traversal (LC 103)](#12-zigzag-level-order-traversal-lc-103)
  - [1.3 Binary Tree Right Side View (LC 199)](#13-binary-tree-right-side-view-lc-199)
- [第二章：BFS 應用](#第二章bfs-應用)
  - [2.1 Minimum Depth of Binary Tree (LC 111)](#21-minimum-depth-of-binary-tree-lc-111)
  - [2.2 Symmetric Tree (LC 101)](#22-symmetric-tree-lc-101)
- [第三章：BST 二元搜尋樹 — 從零開始](#第三章bst-二元搜尋樹--從零開始)
  - [3.1 Validate BST (LC 98)](#31-validate-bst-lc-98)
  - [3.2 Search in BST (LC 700)](#32-search-in-bst-lc-700)
  - [3.3 Insert into BST (LC 701)](#33-insert-into-bst-lc-701)
  - [3.4 Delete Node in BST (LC 450)](#34-delete-node-in-bst-lc-450)
- [第四章：BST 利用中序特性](#第四章bst-利用中序特性)
  - [4.1 Kth Smallest Element in BST (LC 230)](#41-kth-smallest-element-in-bst-lc-230)
  - [4.2 LCA of BST (LC 235)](#42-lca-of-bst-lc-235)
- [第五章：DFS vs BFS 完整比較](#第五章dfs-vs-bfs-完整比較)

---

## 第一章：BFS 層序遍歷 — 用 Queue 一層一層走

### 核心概念

BFS（Breadth-First Search，廣度優先搜尋）在樹上的應用就是 **Level-Order Traversal（層序遍歷）**。

**核心思路**：用一個 Queue（佇列），把每一層的節點排好隊，一層處理完才進下一層。

```
想像消防員從大門進入一棟大樓：
- 先把 1 樓所有房間走完
- 再上 2 樓走完所有房間
- 再上 3 樓……
這就是 BFS — 一層一層來，不會跳層。
```

### BFS 模板（Template）— 逐行解說

```python
from collections import deque

def bfs_template(root):
    if not root:
        return []

    result = []
    queue = deque([root])        # Step 1: 把根節點放進 queue

    while queue:                 # Step 2: 只要 queue 不是空的就繼續
        level_size = len(queue)  # Step 3: 記下「這一層」有幾個節點
        level = []

        for _ in range(level_size):     # Step 4: 只處理這一層的節點
            node = queue.popleft()      # Step 5: 取出隊首
            level.append(node.val)      # Step 6: 處理當前節點

            if node.left:               # Step 7: 左小孩入隊（下一層）
                queue.append(node.left)
            if node.right:              # Step 8: 右小孩入隊（下一層）
                queue.append(node.right)

        result.append(level)    # Step 9: 這一層收集完畢，存入結果
    return result
```

**為什麼用 `level_size = len(queue)`？**
因為在 for 迴圈裡，我們會不斷 `append` 下一層的節點進 queue。如果不先記住「這一層有幾個」，就分不清哪些是本層、哪些是下一層。

**時間複雜度**：O(n) — 每個節點恰好進出 queue 一次
**空間複雜度**：O(n) — 最寬的一層最多 n/2 個節點（完全二元樹的最後一層）

---

### 1.1 Level Order Traversal (LC 102)

**題目**：給一棵二元樹，回傳層序遍歷結果（每層是一個 list）。

#### 範例 1：`[3, 9, 20, null, null, 15, 7]`

```
        3          ← Level 0
       / \
      9   20       ← Level 1
         /  \
        15   7     ← Level 2
```

**完整追蹤**：

```
初始狀態：queue = [3]

━━━ Level 0 ━━━
  level_size = 1 (queue 裡有 1 個節點)
  i=0: popleft → 3,  加入左孩子 9, 加入右孩子 20
       queue = [9, 20]
  level = [3]
  result = [[3]]

━━━ Level 1 ━━━
  level_size = 2 (queue 裡有 2 個節點)
  i=0: popleft → 9,  沒有左孩子, 沒有右孩子
       queue = [20]
  i=1: popleft → 20, 加入左孩子 15, 加入右孩子 7
       queue = [15, 7]
  level = [9, 20]
  result = [[3], [9, 20]]

━━━ Level 2 ━━━
  level_size = 2 (queue 裡有 2 個節點)
  i=0: popleft → 15, 沒有左孩子, 沒有右孩子
       queue = [7]
  i=1: popleft → 7,  沒有左孩子, 沒有右孩子
       queue = []
  level = [15, 7]
  result = [[3], [9, 20], [15, 7]]

queue 為空，結束！
回傳 [[3], [9, 20], [15, 7]]
```

#### 範例 2：`[1, 2, 3, 4, 5, 6, 7]`（完全二元樹 Complete Binary Tree）

```
          1            ← Level 0
        /   \
       2     3         ← Level 1
      / \   / \
     4   5 6   7      ← Level 2
```

**完整追蹤**：

```
初始狀態：queue = [1]

━━━ Level 0 ━━━
  level_size = 1
  i=0: popleft → 1, 加入 2, 加入 3
       queue = [2, 3]
  level = [1]
  result = [[1]]

━━━ Level 1 ━━━
  level_size = 2
  i=0: popleft → 2, 加入 4, 加入 5
       queue = [3, 4, 5]
  i=1: popleft → 3, 加入 6, 加入 7
       queue = [4, 5, 6, 7]
  level = [2, 3]
  result = [[1], [2, 3]]

━━━ Level 2 ━━━
  level_size = 4
  i=0: popleft → 4, 無孩子  → queue = [5, 6, 7]
  i=1: popleft → 5, 無孩子  → queue = [6, 7]
  i=2: popleft → 6, 無孩子  → queue = [7]
  i=3: popleft → 7, 無孩子  → queue = []
  level = [4, 5, 6, 7]
  result = [[1], [2, 3], [4, 5, 6, 7]]

回傳 [[1], [2, 3], [4, 5, 6, 7]]
```

**觀察**：完全二元樹的每一層都是滿的（最後一層可能例外），queue 在處理最後一層時達到最大寬度。

---

### 1.2 Zigzag Level Order Traversal (LC 103)

**題目**：層序遍歷，但奇數層要反轉順序（Level 0 左→右，Level 1 右→左，Level 2 左→右……）。

**關鍵技巧**：跟普通 level order 完全一樣，只是在偶數層（0, 2, 4...）正常加入 level，奇數層（1, 3, 5...）把 level 反轉。

```python
def zigzag_level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    left_to_right = True  # 控制方向的旗標

    while queue:
        level_size = len(queue)
        level = deque()  # 用 deque 方便兩端插入

        for _ in range(level_size):
            node = queue.popleft()

            if left_to_right:
                level.append(node.val)       # 正常：加到右邊
            else:
                level.appendleft(node.val)   # 反轉：加到左邊

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(level))
        left_to_right = not left_to_right    # 每層切換方向
    return result
```

#### 範例 1：`[3, 9, 20, null, null, 15, 7]`

```
        3          ← Level 0 (左→右)
       / \
      9   20       ← Level 1 (右→左)
         /  \
        15   7     ← Level 2 (左→右)
```

**完整追蹤**：

```
初始：queue = [3], left_to_right = True

━━━ Level 0 (left_to_right = True) ━━━
  level_size = 1
  popleft → 3, 方向正常 → level = [3]
  加入孩子 → queue = [9, 20]
  result = [[3]]
  切換方向 → left_to_right = False

━━━ Level 1 (left_to_right = False) ━━━
  level_size = 2
  popleft → 9,  反轉 → appendleft(9)  → level = [9]
  popleft → 20, 反轉 → appendleft(20) → level = [20, 9]
  加入孩子 → queue = [15, 7]
  result = [[3], [20, 9]]
  切換方向 → left_to_right = True

━━━ Level 2 (left_to_right = True) ━━━
  level_size = 2
  popleft → 15, 正常 → append(15) → level = [15]
  popleft → 7,  正常 → append(7)  → level = [15, 7]
  queue = []
  result = [[3], [20, 9], [15, 7]]

回傳 [[3], [20, 9], [15, 7]]
```

#### 範例 2：`[1, 2, 3, 4, 5, 6, 7]`

```
          1            ← Level 0 (左→右): [1]
        /   \
       2     3         ← Level 1 (右→左): [3, 2]
      / \   / \
     4   5 6   7      ← Level 2 (左→右): [4, 5, 6, 7]
```

**完整追蹤**：

```
━━━ Level 0 (left_to_right = True) ━━━
  popleft → 1, append(1) → level = [1]
  result = [[1]]

━━━ Level 1 (left_to_right = False) ━━━
  popleft → 2, appendleft(2) → level = [2]
  popleft → 3, appendleft(3) → level = [3, 2]
  result = [[1], [3, 2]]

━━━ Level 2 (left_to_right = True) ━━━
  popleft → 4, append(4) → level = [4]
  popleft → 5, append(5) → level = [4, 5]
  popleft → 6, append(6) → level = [4, 5, 6]
  popleft → 7, append(7) → level = [4, 5, 6, 7]
  result = [[1], [3, 2], [4, 5, 6, 7]]

回傳 [[1], [3, 2], [4, 5, 6, 7]]
```

---

### 1.3 Binary Tree Right Side View (LC 199)

> Google 高頻題！

**題目**：想像你站在樹的右邊看，能看到哪些節點？回傳從上到下看到的值。

**關鍵洞察**：就是每一層的「最後一個節點」。用 BFS level-order，取每層最後一個元素即可。

```python
def right_side_view(root):
    if not root:
        return []
    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:    # 這一層的最後一個！
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

#### 範例 1：`[1, 2, 3, null, 5, null, 4]`

```
        1            ← 看到 1
       / \
      2   3          ← 看到 3（最右邊）
       \    \
        5    4       ← 看到 4（最右邊）
```

**追蹤**：

```
━━━ Level 0 ━━━  level_size = 1
  i=0 (最後一個!): node=1 → result = [1]
  queue = [2, 3]

━━━ Level 1 ━━━  level_size = 2
  i=0: node=2 (不是最後)
  i=1 (最後一個!): node=3 → result = [1, 3]
  queue = [5, 4]

━━━ Level 2 ━━━  level_size = 2
  i=0: node=5 (不是最後)
  i=1 (最後一個!): node=4 → result = [1, 3, 4]

回傳 [1, 3, 4]
```

#### 範例 2（陷阱！）：`[1, 2, 3, 4, null, null, null]`

```
        1            ← 看到 1
       / \
      2   3          ← 看到 3
     /
    4                ← 看到 4（注意！右邊沒有節點，左邊的 4 反而看得到）
```

**這是面試常見的陷阱**：右側視圖不等於「一直往右走」！Level 2 只有左子樹的節點 4，所以 4 就是那層唯一可見的。

**追蹤**：

```
━━━ Level 0 ━━━  level_size = 1
  i=0 (最後一個!): node=1 → result = [1]
  queue = [2, 3]

━━━ Level 1 ━━━  level_size = 2
  i=0: node=2, 加入左孩子 4
  i=1 (最後一個!): node=3, 無孩子
  queue = [4]

━━━ Level 2 ━━━  level_size = 1
  i=0 (最後一個!): node=4 → result = [1, 3, 4]

回傳 [1, 3, 4]   ← 4 在左邊但仍然可見！
```

**面試要點**：如果用「一直往右走」的方法，會漏掉 4。BFS 每層取最後一個才是正確做法。

---

## 第二章：BFS 應用

### 2.1 Minimum Depth of Binary Tree (LC 111)

**題目**：找到根到最近葉子節點的最短路徑長度。

**為什麼 BFS 比 DFS 更適合這題？**

```
BFS 思路：一層一層往下走，第一次碰到「葉子節點」就是答案！
          可以提前終止（early termination），不用看完整棵樹。

DFS 思路：必須走完所有路徑，才能比較出最小值。
          如果最淺的葉子在左邊，右邊有一棵很深的子樹，DFS 還是會全部走完。
```

```python
def min_depth_bfs(root):
    if not root:
        return 0
    queue = deque([(root, 1)])  # (node, depth)

    while queue:
        node, depth = queue.popleft()

        # 碰到葉子節點 → 直接回傳（BFS 保證最先碰到的葉子是最淺的）
        if not node.left and not node.right:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
```

#### 範例 1：`[3, 9, 20, null, null, 15, 7]`

```
        3          depth=1
       / \
      9   20       depth=2
         /  \
        15   7     depth=3
```

**追蹤**：

```
queue = [(3, 1)]

Step 1: popleft → (3, 1)
  3 有左右孩子，不是葉子
  queue = [(9, 2), (20, 2)]

Step 2: popleft → (9, 2)
  9 沒有左右孩子 → 是葉子！
  return 2   ← 直接結束！不需要看 20, 15, 7

答案：2
```

**注意**：BFS 只看了 2 個節點就結束了。DFS 需要走完所有 5 個節點。

#### 範例 2：`[2, null, 3, null, 4, null, 5, null, 6]`（歪斜樹）

```
    2             depth=1
     \
      3           depth=2
       \
        4         depth=3
         \
          5       depth=4
           \
            6     depth=5
```

**追蹤**：

```
queue = [(2, 1)]

Step 1: (2, 1) → 只有右孩子，不是葉子 → queue = [(3, 2)]
Step 2: (3, 2) → 只有右孩子，不是葉子 → queue = [(4, 3)]
Step 3: (4, 3) → 只有右孩子，不是葉子 → queue = [(5, 4)]
Step 4: (5, 4) → 只有右孩子，不是葉子 → queue = [(6, 5)]
Step 5: (6, 5) → 沒有孩子 → 是葉子！return 5

答案：5
```

**易錯點**：「只有一邊有孩子」的節點不是葉子！葉子必須左右都為 null。所以 depth=1 的節點 2 不算葉子（它有右孩子）。

**BFS vs DFS 比較（此題）**：

| | BFS | DFS |
|---|---|---|
| 思路 | 一層一層找，第一個葉子就是答案 | 遞迴找所有葉子，取最小 |
| 時間（最佳情況） | O(找到第一個葉子) — 可能很快 | O(n) — 必須全部走完 |
| 時間（最差情況） | O(n) — 歪斜樹 | O(n) |
| 空間 | O(最寬層) | O(樹高) — 歪斜樹可能 O(n) |
| 適合 | 答案可能在淺層 | 需要遍歷所有路徑 |

---

### 2.2 Symmetric Tree (LC 101)

**題目**：判斷一棵樹是否為對稱的（鏡像）。

**BFS 做法**：用 queue 放「一對一對」的節點，每次取出一對來比較。

```python
def is_symmetric(root):
    if not root:
        return True
    queue = deque([(root.left, root.right)])  # 放一對鏡像節點

    while queue:
        left, right = queue.popleft()

        if not left and not right:   # 都是 null → OK
            continue
        if not left or not right:    # 只有一邊是 null → 不對稱
            return False
        if left.val != right.val:    # 值不同 → 不對稱
            return False

        # 鏡像配對：左的左 配 右的右，左的右 配 右的左
        queue.append((left.left, right.right))
        queue.append((left.right, right.left))

    return True
```

#### 範例 1（對稱）：`[1, 2, 2, 3, 4, 4, 3]`

```
          1
        /   \
       2     2       ← 鏡像
      / \   / \
     3   4 4   3     ← 鏡像
```

**追蹤**：

```
queue = [(2, 2)]

Step 1: popleft → (2, 2)
  left.val=2, right.val=2 → 相等 ✓
  加入 (2.left, 2.right) = (3, 3)   ← 左的左 配 右的右
  加入 (2.right, 2.left) = (4, 4)   ← 左的右 配 右的左
  queue = [(3, 3), (4, 4)]

Step 2: popleft → (3, 3)
  left.val=3, right.val=3 → 相等 ✓
  加入 (null, null), (null, null)
  queue = [(4, 4), (null, null), (null, null)]

Step 3: popleft → (4, 4)
  left.val=4, right.val=4 → 相等 ✓
  加入 (null, null), (null, null)

Step 4-7: 都是 (null, null) → continue

queue 為空 → return True ✓
```

#### 範例 2（不對稱）：`[1, 2, 2, null, 3, null, 3]`

```
          1
        /   \
       2     2
        \     \
         3     3     ← 不是鏡像！都在右邊
```

**追蹤**：

```
queue = [(2, 2)]

Step 1: popleft → (2, 2)
  left.val=2, right.val=2 → 相等 ✓
  加入 (2.left, 2.right) = (null, 3)   ← 左的左 配 右的右
  加入 (2.right, 2.left) = (3, null)   ← 左的右 配 右的左
  queue = [(null, 3), (3, null)]

Step 2: popleft → (null, 3)
  left 是 null, right 不是 null → 不對稱！
  return False ✗
```

**為什麼不對稱**：鏡像要求左子樹的左邊 = 右子樹的右邊。但左子樹的左邊是 null，右子樹的右邊是 3，不一樣。

---

## 第三章：BST 二元搜尋樹 — 從零開始

### BST 是什麼？

**Binary Search Tree（二元搜尋樹）**是一種特殊的二元樹，滿足：

```
對於每一個節點 node：
  - 左子樹中「所有」節點的值 < node.val
  - 右子樹中「所有」節點的值 > node.val
```

**注意「所有」二字！** 不是只看直接孩子，是整棵子樹！這是最常見的錯誤。

```
    ✓ 合法的 BST          ✗ 不合法的 BST
        5                      5
       / \                    / \
      3   7                  3   7
     / \   \                / \   \
    1   4   9              1   6   9
                                ^
                           6 在 5 的左子樹中，但 6 > 5 → 違反！
```

### 為什麼用 BST？

因為 BST 的結構讓我們可以像 Binary Search 一樣，每次排除一半：

| 操作 | BST (平衡) | 未排序 Array | 已排序 Array |
|------|-----------|-------------|-------------|
| 搜尋 | O(log n) | O(n) | O(log n) |
| 插入 | O(log n) | O(1) | O(n) |
| 刪除 | O(log n) | O(n) | O(n) |

### BST 最重要的性質：Inorder = Sorted

```
BST 的中序遍歷（inorder traversal: 左→根→右）結果是遞增排序的！
```

```
        5
       / \
      3   7
     / \   \
    1   4   9

Inorder: 1 → 3 → 4 → 5 → 7 → 9   ← 遞增！
```

這個性質超級好用，後面很多題目都會利用它。

### BST vs Heap vs HashMap

| | BST | Heap (堆積) | HashMap |
|---|---|---|---|
| 結構 | 二元樹 left<root<right | 完全二元樹 parent≤child | 雜湊表 |
| 搜尋 | O(log n) | O(n) | O(1) 平均 |
| 最小值 | O(log n) 走到最左 | O(1) 堆頂 | O(n) |
| 插入 | O(log n) | O(log n) | O(1) 平均 |
| 有序遍歷 | O(n) inorder | 不支援 | 不支援 |
| 使用場景 | 需要有序+搜尋 | 只要最大/最小 | 只要快速查找 |

---

### 3.1 Validate BST (LC 98)

> 經典易錯題！面試時常見。

**題目**：判斷一棵樹是否是合法的 BST。

#### 錯誤做法（很多人的第一反應）

```python
# ✗ 錯誤！只檢查 node 和直接孩子的關係
def is_valid_bst_WRONG(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return is_valid_bst_WRONG(root.left) and is_valid_bst_WRONG(root.right)
```

**為什麼錯？** 看這棵樹：

```
        5
       / \
      1   7
         / \
        3   8
        ^
        3 < 7 ✓（只看父子）
        但 3 < 5，而 3 在 5 的右子樹中 → 應該 > 5 → 不合法！
        上面的錯誤程式碼不會抓到這個問題
```

#### 正確做法：維護有效範圍 [lo, hi]

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if root.val <= lo or root.val >= hi:
        return False

    # 往左走：上界更新為當前值（左邊的所有值必須 < 當前值）
    # 往右走：下界更新為當前值（右邊的所有值必須 > 當前值）
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

#### 範例 1（不合法）：`[5, 1, 4, null, null, 3, 6]`

```
        5
       / \
      1   4       ← 4 < 5，但 4 在 5 的右子樹 → 不合法
         / \
        3   6
```

**追蹤（每個節點的有效範圍）**：

```
validate(5, lo=-inf, hi=+inf)
  5 > -inf ✓ 且 5 < +inf ✓ → 繼續

  ┣━ validate(1, lo=-inf, hi=5)      ← 左子樹必須 < 5
  │   1 > -inf ✓ 且 1 < 5 ✓ → OK
  │   ┣━ validate(null) → True
  │   ┗━ validate(null) → True
  │   return True ✓
  │
  ┗━ validate(4, lo=5, hi=+inf)      ← 右子樹必須 > 5
      4 > 5? NO! 4 ≤ 5 → return False ✗

最終回傳 False
```

**注意**：問題出在節點 4，它是 5 的右孩子，但 4 < 5，所以不合法。不需要繼續看 3 和 6。

#### 範例 2（合法）：`[2, 1, 3]`

```
        2
       / \
      1   3
```

**追蹤**：

```
validate(2, lo=-inf, hi=+inf)
  2 > -inf ✓ 且 2 < +inf ✓

  ┣━ validate(1, lo=-inf, hi=2)      ← 左子樹必須 < 2
  │   1 > -inf ✓ 且 1 < 2 ✓
  │   ┣━ validate(null) → True
  │   ┗━ validate(null) → True
  │   return True ✓
  │
  ┗━ validate(3, lo=2, hi=+inf)      ← 右子樹必須 > 2
      3 > 2 ✓ 且 3 < +inf ✓
      ┣━ validate(null) → True
      ┗━ validate(null) → True
      return True ✓

最終回傳 True ✓
```

---

### 3.2 Search in BST (LC 700)

**題目**：在 BST 中搜尋目標值，回傳該子樹（或 null）。

**核心**：BST 的搜尋就像二分搜尋 — 每次排除一半。

```python
def search_bst(root, target):
    while root:
        if target == root.val:
            return root          # 找到了！
        elif target < root.val:
            root = root.left     # 目標比較小 → 去左邊找
        else:
            root = root.right    # 目標比較大 → 去右邊找
    return None                  # 沒找到
```

#### 範例 1：在下面的 BST 中搜尋 `target = 2`

```
        4
       / \
      2   7
     / \
    1   3
```

**追蹤**：

```
Step 1: root=4, target=2
  2 < 4 → 往左走

Step 2: root=2, target=2
  2 == 2 → 找到了！回傳以 2 為根的子樹

        2
       / \
      1   3

只走了 2 步就找到（O(log n) = O(log 5) ≈ 2 步）
```

#### 範例 2：在同一棵 BST 中搜尋 `target = 5`

```
        4
       / \
      2   7
     / \
    1   3
```

**追蹤**：

```
Step 1: root=4, target=5
  5 > 4 → 往右走

Step 2: root=7, target=5
  5 < 7 → 往左走

Step 3: root=null（7 沒有左孩子）
  → 回傳 None（找不到 5）

只走了 2 步就確定不存在
```

---

### 3.3 Insert into BST (LC 701)

**題目**：將一個值插入 BST，保持 BST 性質。

**核心**：像搜尋一樣走到正確的空位，把新節點放進去。

```python
def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)     # 找到空位，建新節點

    if val < root.val:
        root.left = insert_into_bst(root.left, val)    # 去左邊插
    else:
        root.right = insert_into_bst(root.right, val)  # 去右邊插

    return root
```

#### 範例 1：插入 `val = 5`

```
插入前：                  插入後：
        4                      4
       / \                    / \
      2   7                  2   7
     / \                    / \ /
    1   3                  1  3 5
```

**追蹤**：

```
insert(root=4, val=5)
  5 > 4 → 往右
  insert(root=7, val=5)
    5 < 7 → 往左
    insert(root=null, val=5)
      root 是 null → 建新節點 TreeNode(5)，回傳
    7.left = TreeNode(5) ← 掛上去
  回傳 7
回傳 4（整棵樹不變，只是多了 5）
```

#### 範例 2：插入 `val = 0`

```
插入前：                  插入後：
        4                      4
       / \                    / \
      2   7                  2   7
     / \                    / \
    1   3                  1   3
                          /
                         0
```

**追蹤**：

```
insert(root=4, val=0)
  0 < 4 → 往左
  insert(root=2, val=0)
    0 < 2 → 往左
    insert(root=1, val=0)
      0 < 1 → 往左
      insert(root=null, val=0)
        建新節點 TreeNode(0)，回傳
      1.left = TreeNode(0)
    回傳 1
  回傳 2
回傳 4

路徑：4 → 2 → 1 → 新建 0（3 步，O(log n)）
```

---

### 3.4 Delete Node in BST (LC 450)

> BST 最複雜的基本操作！面試必考。

**題目**：刪除 BST 中指定值的節點，保持 BST 性質。

**三種情況**：

```
Case 1: 刪除葉子節點 → 直接移除（最簡單）

        5              5
       / \    刪除1   / \
      3   7  ───→   3   7
     /
    1

Case 2: 刪除只有一個孩子的節點 → 用孩子取代自己

        5              5
       / \    刪除3   / \
      3   7  ───→   1   7
     /
    1

Case 3: 刪除有兩個孩子的節點 → 用「中序後繼者」(inorder successor) 取代
       （中序後繼者 = 右子樹中最小的值）

        5              6
       / \    刪除5   / \
      3   7  ───→   3   7
     / \  /        / \
    1  4 6        1   4
```

```python
def delete_node(root, key):
    if not root:
        return None

    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # 找到要刪除的節點了！

        # Case 1 & 2: 沒有左孩子 → 用右孩子取代（含葉子情況：右孩子也是 null）
        if not root.left:
            return root.right

        # Case 2: 沒有右孩子 → 用左孩子取代
        if not root.right:
            return root.left

        # Case 3: 有兩個孩子 → 找右子樹最小值（中序後繼者）
        successor = root.right
        while successor.left:
            successor = successor.left

        root.val = successor.val  # 用後繼者的值覆蓋
        root.right = delete_node(root.right, successor.val)  # 刪除後繼者

    return root
```

#### 範例 1（Case 1 — 刪除葉子）：刪除 `key = 4`

```
        5              5
       / \            / \
      3   7   ──→    3   7
     / \            /
    1   4          1
```

**追蹤**：

```
delete(root=5, key=4)
  4 < 5 → 往左
  delete(root=3, key=4)
    4 > 3 → 往右
    delete(root=4, key=4)
      找到了！root.val == key
      root.left = null, 所以 return root.right = null
    3.right = null  ← 4 被移除了
  回傳 3
回傳 5

結果：4 被直接刪掉（因為它是葉子，沒有孩子）
```

#### 範例 2（Case 3 — 刪除有兩個孩子的節點）：刪除 `key = 5`

```
        5                    6
       / \                  / \
      3   8      ──→       3   8
     / \  / \             / \    \
    1  4 6   9           1   4    9
          \
           7
```

**追蹤**：

```
delete(root=5, key=5)
  找到了！root.val == key
  root.left = 3 (存在), root.right = 8 (存在) → Case 3!

  找右子樹最小值（中序後繼者）：
    successor = 8
    8.left = 6 → successor = 6
    6.left = null → 停！successor = 6

  用 6 覆蓋 5 → root.val = 6

  現在要從右子樹刪除 6：
  delete(root=8, key=6)
    6 < 8 → 往左
    delete(root=6, key=6)
      找到了！
      root.left = null → return root.right = 7
    8.left = 7
  回傳 8

  root(原本是 5，現在值是 6).right = 8
回傳 root

最終的樹：
        6
       / \
      3   8
     / \  / \
    1  4 7   9
```

**為什麼用中序後繼者？** 因為它是「右子樹中最小的」，用它取代被刪節點後：
- 它比左子樹所有值都大（因為它在右子樹中）
- 它比右子樹其他值都小（因為它是最小的）
- BST 性質完美保持！

---

## 第四章：BST 利用中序特性

### 4.1 Kth Smallest Element in BST (LC 230)

**題目**：找 BST 中第 k 小的元素。

**關鍵洞察**：BST 的 inorder traversal = 遞增排序。所以 inorder 走到第 k 個就是答案！

```python
def kth_smallest(root, k):
    stack = []
    curr = root
    count = 0

    while stack or curr:
        # 一路往左走到底
        while curr:
            stack.append(curr)
            curr = curr.left

        # 彈出 = 中序訪問
        curr = stack.pop()
        count += 1

        if count == k:
            return curr.val   # 第 k 個！

        # 轉向右子樹
        curr = curr.right
```

#### 範例 1：`k = 3`

```
        5
       / \
      3   6
     / \
    2   4
   /
  1

Inorder: 1, 2, 3, 4, 5, 6
第 3 小 = 3
```

**追蹤**：

```
stack = [], curr = 5

━━ 往左走到底 ━━
  push 5, curr=3
  push 3, curr=2
  push 2, curr=1
  push 1, curr=null (停)
  stack = [5, 3, 2, 1]

pop → 1, count=1 (不是第 3 個)
  curr = 1.right = null

━━ 往左走到底 ━━
  curr 已經是 null，跳過

pop → 2, count=2 (不是第 3 個)
  curr = 2.right = null

pop → 3, count=3 → 就是第 3 個！return 3 ✓
```

#### 範例 2：`k = 1`（找最小值）

```
        3
       / \
      1   4
       \
        2

Inorder: 1, 2, 3, 4
第 1 小 = 1
```

**追蹤**：

```
stack = [], curr = 3

━━ 往左走到底 ━━
  push 3, curr=1
  push 1, curr=null (停)
  stack = [3, 1]

pop → 1, count=1 → 就是第 1 個！return 1 ✓
```

**觀察**：找第 1 小 = 找 BST 最左邊的節點，只需 O(h) 步（h = 樹高）。

---

### 4.2 Lowest Common Ancestor of BST (LC 235)

**題目**：在 BST 中找兩個節點 p, q 的最低公共祖先 (LCA)。

**為什麼 BST 的 LCA 比一般二元樹簡單？**

一般二元樹的 LCA 需要遞迴檢查左右子樹（LC 236）。但 BST 有排序性質，可以用值的大小來判斷方向：

```
如果 p, q 都小於 node → LCA 在左子樹
如果 p, q 都大於 node → LCA 在右子樹
如果 p, q 分別在兩邊（或其中一個就是 node）→ node 就是 LCA！
```

```python
def lowest_common_ancestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left       # 都比 root 小 → 往左
        elif p.val > root.val and q.val > root.val:
            root = root.right      # 都比 root 大 → 往右
        else:
            return root            # 分岔點 → 就是 LCA！
```

#### 範例 1：找 `p=2, q=8` 的 LCA

```
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

**追蹤**：

```
Step 1: root=6, p=2, q=8
  p=2 < 6, q=8 > 6 → 分岔！（一個在左，一個在右）
  return 6

答案：6

路徑：只走 1 步！因為 2 和 8 一個在 6 的左邊、一個在右邊。
```

#### 範例 2：找 `p=2, q=4` 的 LCA

```
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

**追蹤**：

```
Step 1: root=6, p=2, q=4
  p=2 < 6 且 q=4 < 6 → 都比 6 小 → 往左

Step 2: root=2, p=2, q=4
  p=2 == root → 不滿足「都小於」也不滿足「都大於」→ 分岔！
  return 2

答案：2

解釋：2 本身就是 p，而 4 在 2 的右子樹中。所以 2 就是 LCA。
LCA 不一定是「在兩者中間」的節點，可以就是其中一個。
```

**時間複雜度**：O(h)，h 是樹高。平衡 BST 中 h = O(log n)。

---

## 第五章：DFS vs BFS 完整比較

### 全面比較表

| 比較項目 | DFS (深度優先) | BFS (廣度優先) |
|---------|--------------|--------------|
| **資料結構** | Stack（或遞迴呼叫棧） | Queue |
| **探索順序** | 一條路走到底再回頭 | 一層一層展開 |
| **空間複雜度** | O(h) — h 是樹高 | O(w) — w 是最大寬度 |
| **平衡樹空間** | O(log n) | O(n/2) = O(n) |
| **歪斜樹空間** | O(n) | O(1) |
| **是否找最短路** | 不保證（除非窮舉所有路徑） | 天然保證最短路 |
| **遍歷變體** | preorder / inorder / postorder | level-order |

### DFS 好的場景

```
1. 需要探索所有路徑（例：路徑總和、排列組合）
2. 需要利用 inorder/preorder/postorder 的特殊性質
3. 樹很「寬」（BFS 的 queue 會很大）
4. 需要回溯（Backtracking）
5. BST 相關題目（利用 inorder = sorted）
```

### BFS 好的場景

```
1. 找最短路徑 / 最小深度（BFS 第一次碰到就是最短）
2. 層序遍歷（需要知道每一層的資訊）
3. 樹很「深」但很「窄」（DFS 的 stack 會很大）
4. 需要逐層處理（例：zigzag、右視圖）
5. 圖的最短路徑（unweighted）
```

### 同一題 DFS vs BFS：Maximum Depth (LC 104)

```
        3
       / \
      9   20
         /  \
        15   7
```

**DFS 解法**（遞迴，3 行）：

```python
def max_depth_dfs(root):
    if not root:
        return 0
    return 1 + max(max_depth_dfs(root.left), max_depth_dfs(root.right))
```

```
追蹤：
  max_depth(3)
    = 1 + max(max_depth(9), max_depth(20))
    = 1 + max(
        1 + max(max_depth(null), max_depth(null)) = 1 + max(0, 0) = 1,
        1 + max(max_depth(15), max_depth(7))
          = 1 + max(
              1 + max(0, 0) = 1,
              1 + max(0, 0) = 1
            ) = 1 + 1 = 2
      )
    = 1 + max(1, 2) = 3

答案：3
```

**BFS 解法**（逐層計數）：

```python
def max_depth_bfs(root):
    if not root:
        return 0
    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
```

```
追蹤：
  depth=0, queue=[3]

  Level 1: depth=1, 處理 3, queue=[9, 20]
  Level 2: depth=2, 處理 9 和 20, queue=[15, 7]
  Level 3: depth=3, 處理 15 和 7, queue=[]

  queue 為空，return depth=3
```

**比較**：

| | DFS | BFS |
|---|---|---|
| 程式碼 | 3 行，更簡潔 | 約 10 行 |
| 空間 | O(h) = O(3) = O(3) | O(w) = O(2)（最寬層有 2 個） |
| 思路 | 遞迴分治 | 逐層計數 |

這題 DFS 和 BFS 都很好，但 DFS 的程式碼更簡潔。

### 什麼時候兩者差異最大？

```
情境 1：非常寬的樹（例：完全二元樹 depth=20）
  - 最寬層有 2^19 = 524,288 個節點
  - BFS 的 queue 需要存 50 萬個節點 → 記憶體爆炸！
  - DFS 的 stack 只需要 20 層 → 輕鬆
  → 用 DFS！

情境 2：非常深的歪斜樹（像 linked list，10 萬個節點）
  - DFS 遞迴 10 萬層 → stack overflow！
  - BFS 的 queue 每層只有 1 個節點 → 輕鬆
  → 用 BFS！（或 iterative DFS）

情境 3：找最短路徑（例：minimum depth）
  - BFS 碰到第一個葉子就是答案 → 可以提前結束
  - DFS 必須走完所有路徑才能比較
  → 用 BFS！

情境 4：需要回溯 / 路徑記錄（例：所有根到葉路徑）
  - DFS 天然支援回溯（遞迴 return 後自動回到上一步）
  - BFS 要額外記錄路徑，很麻煩
  → 用 DFS！
```

### 面試快速判斷法

```
面試碰到 Tree 題，問自己這三個問題：

Q1: 需要逐層處理嗎？（level order, zigzag, right side view）
    → Yes → BFS

Q2: 需要找最短路徑 / 最小深度嗎？
    → Yes → BFS（可以 early termination）

Q3: 需要遍歷所有路徑 / 用到 inorder 性質 / 回溯？
    → Yes → DFS

如果都不是，兩者都可以，選你比較熟的。
面試時能清楚說出「我選 BFS 因為需要逐層處理」就能加分。
```

---

## 總結：本章重點一覽

| 題目 | 類型 | 核心技巧 | 時間 | 空間 |
|------|------|---------|------|------|
| LC 102 Level Order | BFS | Queue + level_size | O(n) | O(n) |
| LC 103 Zigzag | BFS | 交替方向 appendleft | O(n) | O(n) |
| LC 199 Right Side View | BFS | 每層最後一個 | O(n) | O(n) |
| LC 111 Min Depth | BFS | 第一個葉子 = 答案 | O(n) | O(n) |
| LC 101 Symmetric | BFS | Queue 放鏡像配對 | O(n) | O(n) |
| LC 98 Validate BST | DFS | 維護 [lo, hi] 範圍 | O(n) | O(h) |
| LC 700 Search BST | BST | 二分搜尋走法 | O(h) | O(1) |
| LC 701 Insert BST | BST | 找到空位插入 | O(h) | O(h) |
| LC 450 Delete BST | BST | 三種情況 + 中序後繼者 | O(h) | O(h) |
| LC 230 Kth Smallest | BST | Inorder = sorted | O(h+k) | O(h) |
| LC 235 LCA of BST | BST | 值的大小判斷方向 | O(h) | O(1) |

> h = 樹高。平衡樹 h = O(log n)，歪斜樹 h = O(n)。

**下一步**：搭配 `08_Tree_BFS_BST.py` 實際執行每一題的程式碼，觀察 verbose 模式的輸出。
