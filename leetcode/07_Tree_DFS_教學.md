# 07 - Tree & DFS 完整教學：從零開始到 Google 面試

> **目標讀者**：基礎薄弱、準備 Google 面試的工程師
> **教學原則**：每個概念至少 2 個範例，每個範例都畫 ASCII 樹、追蹤遞迴 call stack
> **語言**：繁體中文 + English 關鍵術語

---

## 第一章：Tree 基礎觀念 — 從零開始

### 1.1 什麼是樹？(What is a Tree?)

**樹 (Tree)** 是一種「階層式 (hierarchical)」資料結構，就像家族族譜或公司組織圖。

**核心術語**：
| 英文 | 中文 | 說明 |
|------|------|------|
| Node | 節點 | 樹上的每一個元素 |
| Edge | 邊 | 連接兩個節點的線 |
| Root | 根節點 | 最上面、沒有父節點的節點 |
| Leaf | 葉節點 | 最下面、沒有子節點的節點 |
| Parent | 父節點 | 某節點的上一層 |
| Child | 子節點 | 某節點的下一層 |
| Subtree | 子樹 | 以某節點為根的整棵樹 |

```
         1          <-- Root（根節點）
        / \
       2   3        <-- 2 和 3 是 1 的 Children（子節點）
      / \   \
     4   5   6      <-- Leaves（葉節點，沒有子節點）

     1 是 2 的 Parent（父節點）
     以 2 為根的子樹：{ 2, 4, 5 }
     邊 (Edge) 的數量 = 節點數 - 1 = 5
```

### 1.2 Binary Tree（二元樹）

**二元樹**的規則很簡單：**每個節點最多只有 2 個子節點**（左子 left、右子 right）。

LeetCode 上 90% 的樹題都是二元樹。

### 1.3 Depth、Height、Level — 容易搞混的三個詞

```
         1          Level 0    Depth 0
        / \
       2   3        Level 1    Depth 1
      / \
     4   5          Level 2    Depth 2

  Depth（深度）：從 root 到該節點的邊數（root depth = 0）
  Height（高度）：從該節點到最遠 leaf 的邊數
    - 節點 1 的 height = 2
    - 節點 2 的 height = 1
    - 節點 4 的 height = 0（leaf）
  Level = Depth（同一層的節點 depth 相同）
  樹的高度 = root 的 height = 2
```

> **注意**：有些題目定義 depth 從 1 開始（root depth = 1），這時「最大深度」會多 1。LeetCode 104 就是這種定義。看題目要仔細。

### 1.4 程式碼中的 TreeNode

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # 節點的值
        self.left = left    # 左子節點（也是 TreeNode 或 None）
        self.right = right  # 右子節點（也是 TreeNode 或 None）
```

就這麼簡單！一個節點只有三樣東西：**值、左指標、右指標**。

### 1.5 LeetCode 如何表示樹？Level-order Array

LeetCode 用 **level-order（層序）** 陣列表示一棵樹。`null` 表示該位置沒有節點。

**Example 1**：`[1, 2, 3, null, 4]`

```
拆解過程：
  index 0: 1   → root
  index 1: 2   → 1 的左子
  index 2: 3   → 1 的右子
  index 3: null → 2 的左子 = 空
  index 4: 4   → 2 的右子

結果：
       1
      / \
     2   3
      \
       4
```

**Example 2**：`[3, 9, 20, null, null, 15, 7]`

```
拆解過程（一層一層填）：
  Level 0:  3             → root
  Level 1:  9, 20         → 3 的左、右子
  Level 2:  null, null    → 9 的左右子都空
            15, 7         → 20 的左、右子

結果：
       3
      / \
     9   20
        /  \
       15   7
```

---

## 第二章：三種遍歷 — 核心中的核心

**遍歷 (Traversal)** = 按某種順序「拜訪」樹上的每個節點。

三種 DFS 遍歷的差別只在於「什麼時候處理 root」：

| 遍歷 | 順序 | 口訣 |
|------|------|------|
| Preorder（前序）| Root → Left → Right | 先拜訪自己，再去左邊，再去右邊 |
| Inorder（中序）| Left → Root → Right | 先去最左邊，拜訪自己，再去右邊 |
| Postorder（後序）| Left → Right → Root | 先處理所有子樹，最後才處理自己 |

---

### 2.1 Preorder 前序遍歷：Root → Left → Right

#### 遞迴寫法（Recursive）

```python
def preorder(root):
    if not root:
        return []
    result = []
    def dfs(node):
        if not node:
            return
        result.append(node.val)   # 1. 先處理自己
        dfs(node.left)            # 2. 再去左邊
        dfs(node.right)           # 3. 最後去右邊
    dfs(root)
    return result
```

#### 迭代寫法（Iterative with Stack）

```python
def preorder_iterative(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        # 注意：先 push right，再 push left
        # 因為 stack 是 LIFO，left 會先被 pop 出來
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result
```

#### Example 1：基本二元樹

```
Tree:
       1
      / \
     2   3
    / \
   4   5

Call Stack 追蹤（縮排表示遞迴深度）：
dfs(1)                          → visit 1, result = [1]
  dfs(2)                        → visit 2, result = [1, 2]
    dfs(4)                      → visit 4, result = [1, 2, 4]
      dfs(None) → return
      dfs(None) → return
    return                      ← 回到 dfs(2)
    dfs(5)                      → visit 5, result = [1, 2, 4, 5]
      dfs(None) → return
      dfs(None) → return
    return                      ← 回到 dfs(2)
  return                        ← 回到 dfs(1)
  dfs(3)                        → visit 3, result = [1, 2, 4, 5, 3]
    dfs(None) → return
    dfs(None) → return
  return

Preorder 結果：[1, 2, 4, 5, 3]
```

#### Example 2：不對稱的樹

```
Tree:
       5
      / \
     3   8
      \   \
       4   9

Call Stack 追蹤：
dfs(5)                          → visit 5, result = [5]
  dfs(3)                        → visit 3, result = [5, 3]
    dfs(None) → return          （3 沒有左子）
    dfs(4)                      → visit 4, result = [5, 3, 4]
      dfs(None) → return
      dfs(None) → return
    return
  return
  dfs(8)                        → visit 8, result = [5, 3, 4, 8]
    dfs(None) → return          （8 沒有左子）
    dfs(9)                      → visit 9, result = [5, 3, 4, 8, 9]
      dfs(None) → return
      dfs(None) → return
    return
  return

Preorder 結果：[5, 3, 4, 8, 9]
```

---

### 2.2 Inorder 中序遍歷：Left → Root → Right

#### 遞迴寫法

```python
def inorder(root):
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)            # 1. 先去最左邊
        result.append(node.val)   # 2. 拜訪自己
        dfs(node.right)           # 3. 再去右邊
    dfs(root)
    return result
```

#### 迭代寫法

```python
def inorder_iterative(root):
    result = []
    stack = []
    curr = root
    while curr or stack:
        # 一路往左走到底
        while curr:
            stack.append(curr)
            curr = curr.left
        # 彈出 = 訪問
        curr = stack.pop()
        result.append(curr.val)
        # 轉向右子樹
        curr = curr.right
    return result
```

> **KEY INSIGHT**：Inorder 對 BST（二元搜尋樹）會得到 **sorted order（排序結果）**！這是面試超級重要的觀念。

#### Example 1：一般二元樹

```
Tree:
       1
      / \
     2   3
    / \
   4   5

Call Stack 追蹤：
dfs(1)
  dfs(2)
    dfs(4)
      dfs(None) → return
      → visit 4, result = [4]       ← 最左邊的節點最先被拜訪
      dfs(None) → return
    return
    → visit 2, result = [4, 2]      ← 左子樹處理完，拜訪自己
    dfs(5)
      dfs(None) → return
      → visit 5, result = [4, 2, 5]
      dfs(None) → return
    return
  return
  → visit 1, result = [4, 2, 5, 1]  ← root 在中間被拜訪
  dfs(3)
    dfs(None) → return
    → visit 3, result = [4, 2, 5, 1, 3]
    dfs(None) → return
  return

Inorder 結果：[4, 2, 5, 1, 3]
```

#### Example 2：BST — Inorder = Sorted!

```
Tree (BST):
       5
      / \
     3   8
    / \   \
   1   4   9

Call Stack 追蹤：
dfs(5)
  dfs(3)
    dfs(1)
      dfs(None) → return
      → visit 1, result = [1]
      dfs(None) → return
    → visit 3, result = [1, 3]
    dfs(4)
      dfs(None) → return
      → visit 4, result = [1, 3, 4]
      dfs(None) → return
  → visit 5, result = [1, 3, 4, 5]
  dfs(8)
    dfs(None) → return
    → visit 8, result = [1, 3, 4, 5, 8]
    dfs(9)
      dfs(None) → return
      → visit 9, result = [1, 3, 4, 5, 8, 9]
      dfs(None) → return

Inorder 結果：[1, 3, 4, 5, 8, 9]  ← 完美排序！
```

---

### 2.3 Postorder 後序遍歷：Left → Right → Root

#### 遞迴寫法

```python
def postorder(root):
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)            # 1. 先去左邊
        dfs(node.right)           # 2. 再去右邊
        result.append(node.val)   # 3. 最後才處理自己
    dfs(root)
    return result
```

#### 迭代寫法（巧妙技巧）

```python
def postorder_iterative(root):
    # 技巧：做「反向 preorder」(Root → Right → Left)，再翻轉
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:              # 先 push left（後 pop）
            stack.append(node.left)
        if node.right:             # 再 push right（先 pop）
            stack.append(node.right)
    return result[::-1]            # 翻轉！
```

> **KEY INSIGHT**：Postorder 是「先處理子樹，最後處理自己」—— 這就是 **bottom-up（由下往上）** 的思維。大多數 Tree DP / 計算高度 / 判斷平衡的題目都是 postorder 模式！

#### Example 1：基本二元樹

```
Tree:
       1
      / \
     2   3
    / \
   4   5

Call Stack 追蹤：
dfs(1)
  dfs(2)
    dfs(4)
      dfs(None) → return
      dfs(None) → return
      → visit 4, result = [4]       ← 葉節點最先被處理
    dfs(5)
      dfs(None) → return
      dfs(None) → return
      → visit 5, result = [4, 5]
    → visit 2, result = [4, 5, 2]   ← 子樹處理完才處理 parent
  dfs(3)
    dfs(None) → return
    dfs(None) → return
    → visit 3, result = [4, 5, 2, 3]
  → visit 1, result = [4, 5, 2, 3, 1] ← root 最後被處理

Postorder 結果：[4, 5, 2, 3, 1]
```

#### Example 2：有深度的樹

```
Tree:
       10
      /  \
     20   30
    /
   40

Call Stack 追蹤：
dfs(10)
  dfs(20)
    dfs(40)
      dfs(None) → return
      dfs(None) → return
      → visit 40, result = [40]
    dfs(None) → return              （20 沒有右子）
    → visit 20, result = [40, 20]
  dfs(30)
    dfs(None) → return
    dfs(None) → return
    → visit 30, result = [40, 20, 30]
  → visit 10, result = [40, 20, 30, 10]

Postorder 結果：[40, 20, 30, 10]
```

---

### 2.4 三種遍歷並排比較

用同一棵樹，看三種遍歷的差異：

```
Tree:
       1
      / \
     2   3
    / \
   4   5

Preorder  (Root-L-R): [1, 2, 4, 5, 3]   ← root 在最前面
Inorder   (L-Root-R): [4, 2, 5, 1, 3]   ← root 在中間
Postorder (L-R-Root): [4, 5, 2, 3, 1]   ← root 在最後面
```

**什麼時候用哪種？速查表**：

| 情境 | 用哪種 | 為什麼 |
|------|--------|--------|
| 計算高度、深度 | Postorder | 先算子樹高度，才能算自己 |
| 判斷平衡 | Postorder | 先知道子樹高度差，才能判斷 |
| Diameter / Max Path Sum | Postorder + 全域變數 | Bottom-up 收集，順便更新最佳解 |
| Path Sum（路徑和）| Preorder | Top-down 傳遞剩餘目標值 |
| 序列化 / 複製樹 | Preorder | 先建 root，再建子樹 |
| BST 排序 / 第 K 小 | Inorder | BST Inorder = sorted |
| 刪除整棵樹 | Postorder | 先刪子節點，才能刪父節點 |

---

## 第三章：DFS 求值型（Calculate Values）

### 3.1 Maximum Depth of Binary Tree（LC 104）

> **題意**：回傳二元樹的最大深度。root 到最遠 leaf 的節點數。

**核心公式**：
```
depth(node) = 1 + max(depth(left), depth(right))
depth(None) = 0
```

這就是 **postorder 模式**：先算子樹深度，再算自己。

```python
def maxDepth(root):
    if not root:
        return 0
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    return 1 + max(left_depth, right_depth)
```

#### Example 1

```
Tree:
       3
      / \
     9   20
        /  \
       15   7

Recursion Tree（遞迴展開）：

maxDepth(3)
├── maxDepth(9)
│   ├── maxDepth(None) = 0
│   └── maxDepth(None) = 0
│   → return 1 + max(0, 0) = 1
└── maxDepth(20)
    ├── maxDepth(15)
    │   ├── maxDepth(None) = 0
    │   └── maxDepth(None) = 0
    │   → return 1 + max(0, 0) = 1
    └── maxDepth(7)
        ├── maxDepth(None) = 0
        └── maxDepth(None) = 0
        → return 1 + max(0, 0) = 1
    → return 1 + max(1, 1) = 2
→ return 1 + max(1, 2) = 3

答案：3
```

#### Example 2

```
Tree:
     1
      \
       2
        \
         3

Recursion Tree：

maxDepth(1)
├── maxDepth(None) = 0       （沒有左子）
└── maxDepth(2)
    ├── maxDepth(None) = 0
    └── maxDepth(3)
        ├── maxDepth(None) = 0
        └── maxDepth(None) = 0
        → return 1 + max(0, 0) = 1
    → return 1 + max(0, 1) = 2
→ return 1 + max(0, 2) = 3

答案：3（偏斜樹，深度 = 節點數）
```

**時間複雜度**：O(n)，每個節點拜訪一次
**空間複雜度**：O(h)，h = 樹高（遞迴堆疊深度）

---

### 3.2 Diameter of Binary Tree（LC 543）— Google 高頻

> **題意**：二元樹的「直徑」= 任意兩個節點之間最長路徑的**邊數**。

**關鍵觀察**：最長路徑不一定經過 root！

**核心想法**：
- 對每個節點，經過它的最長路徑 = **左子樹深度 + 右子樹深度**
- 用一個全域變數 `max_diameter` 記錄目前看到的最大值
- 同樣是 **postorder 模式**（先算子樹，再更新答案）

```python
def diameterOfBinaryTree(root):
    max_diameter = 0

    def depth(node):
        nonlocal max_diameter
        if not node:
            return 0
        left_d = depth(node.left)
        right_d = depth(node.right)
        # 經過這個節點的路徑長度 = 左深度 + 右深度
        max_diameter = max(max_diameter, left_d + right_d)
        # 回傳給父節點：只能選一邊（不能分叉）
        return 1 + max(left_d, right_d)

    depth(root)
    return max_diameter
```

#### Example 1：最長路徑經過 root

```
Tree:
       1
      / \
     2   3
    / \
   4   5

逐節點計算：

depth(4): left=0, right=0 → diameter=max(0, 0+0)=0 → return 1
depth(5): left=0, right=0 → diameter=max(0, 0+0)=0 → return 1
depth(2): left=1, right=1 → diameter=max(0, 1+1)=2 → return 1+max(1,1)=2
depth(3): left=0, right=0 → diameter=max(2, 0+0)=2 → return 1
depth(1): left=2, right=1 → diameter=max(2, 2+1)=3 → return 1+max(2,1)=3

答案：3（路徑 4→2→1→3 或 5→2→1→3）

圖示最長路徑：
       1
      / \
    [2]  [3]
    /
  [4]
  路徑：4 → 2 → 1 → 3，共 3 條邊
```

#### Example 2：最長路徑不經過 root！

```
Tree:
         1
        /
       2
      / \
     3   4
    /     \
   5       6

逐節點計算：

depth(5): left=0, right=0 → diameter=0   → return 1
depth(3): left=1, right=0 → diameter=max(0, 1)=1   → return 2
depth(6): left=0, right=0 → diameter=max(1, 0)=1   → return 1
depth(4): left=0, right=1 → diameter=max(1, 1)=1   → return 2
depth(2): left=2, right=2 → diameter=max(1, 2+2)=4 → return 3  *** 最大值在這裡！
depth(1): left=3, right=0 → diameter=max(4, 3+0)=4 → return 4

答案：4（路徑 5→3→2→4→6，不經過 root！）

圖示最長路徑：
         1
        /
       [2]
      /   \
    [3]   [4]
    /       \
  [5]      [6]
  路徑：5 → 3 → 2 → 4 → 6，共 4 條邊
```

> **面試重點**：Diameter 和後面的 Maximum Path Sum (LC 124) 用完全相同的模式：postorder + nonlocal 全域變數。這個模式 Google 超愛考。

---

### 3.3 Balanced Binary Tree（LC 110）

> **題意**：判斷一棵二元樹是否「高度平衡」。平衡 = 每個節點的左右子樹高度差 <= 1。

**技巧**：用 `-1` 表示「不平衡」，提前終止遞迴（剪枝 pruning）。

```python
def isBalanced(root):
    def check(node):
        if not node:
            return 0                    # 空節點高度 = 0
        left_h = check(node.left)
        if left_h == -1:
            return -1                   # 左子樹不平衡，直接放棄
        right_h = check(node.right)
        if right_h == -1:
            return -1                   # 右子樹不平衡，直接放棄
        if abs(left_h - right_h) > 1:
            return -1                   # 自己不平衡
        return 1 + max(left_h, right_h) # 回傳高度

    return check(root) != -1
```

#### Example 1：平衡的樹

```
Tree:
       3
      / \
     9   20
        /  \
       15   7

逐節點計算：
check(9):  left=0, right=0 → |0-0|=0 <= 1 → return 1
check(15): left=0, right=0 → return 1
check(7):  left=0, right=0 → return 1
check(20): left=1, right=1 → |1-1|=0 <= 1 → return 2
check(3):  left=1, right=2 → |1-2|=1 <= 1 → return 3

答案：True（每個節點左右高度差都 <= 1）
```

#### Example 2：不平衡的樹

```
Tree:
         1
        / \
       2   2
      / \
     3   3
    / \
   4   4

逐節點計算：
check(4左): return 1
check(4右): return 1
check(3左): left=1, right=1 → return 2
check(3右): left=0, right=0 → return 1
check(2左): left=2, right=1 → |2-1|=1 <= 1 → return 3
check(2右): left=0, right=0 → return 1
check(1):   left=3, right=1 → |3-1|=2 > 1 → return -1  *** 不平衡！

答案：False（root 左子樹高度 3，右子樹高度 1，差 2 > 1）
```

---

## 第四章：DFS 路徑型（Path Problems）

### 4.1 Path Sum（LC 112）

> **題意**：判斷是否存在一條 root-to-leaf 路徑，使得路徑上所有節點值的和等於 `targetSum`。

**核心技巧**：每往下走一層，`target` 減去當前節點的值。到 leaf 時檢查剩餘值是否為 0。

```python
def hasPathSum(root, targetSum):
    if not root:
        return False
    # 到 leaf 了，檢查剩餘值
    if not root.left and not root.right:
        return root.val == targetSum
    # 往下走，target 扣掉當前值
    return (hasPathSum(root.left, targetSum - root.val) or
            hasPathSum(root.right, targetSum - root.val))
```

#### Example 1：找到路徑

```
Tree:                    target = 22
       5
      / \
     4   8
    /   / \
   11  13  4
  / \       \
 7   2       1

追蹤 remaining target（剩餘目標值）：

hasPathSum(5, 22):   remaining = 22
├── hasPathSum(4, 17):   remaining = 17
│   ├── hasPathSum(11, 13):   remaining = 13
│   │   ├── hasPathSum(7, 2):   remaining = 2
│   │   │   leaf! 7 != 2 → False
│   │   └── hasPathSum(2, 2):   remaining = 2
│   │       leaf! 2 == 2 → True !!!
│   │   → return True
│   → return True
→ return True

答案：True（路徑 5→4→11→2，和 = 22）
```

#### Example 2：找不到路徑

```
Tree:                    target = 10
     1
    / \
   2   3

追蹤：
hasPathSum(1, 10):   remaining = 10
├── hasPathSum(2, 9):   remaining = 9
│   leaf! 2 != 9 → False
└── hasPathSum(3, 9):   remaining = 9
    leaf! 3 != 9 → False
→ return False

答案：False（路徑 1→2=3，路徑 1→3=4，都不是 10）
```

---

### 4.2 Path Sum II（LC 113）— Backtracking on Tree

> **題意**：找出**所有** root-to-leaf 路徑，使得路徑和等於 `targetSum`。

**核心技巧**：Backtracking（回溯法）！
- `path.append(node.val)` → 加入路徑
- 遞迴左右子樹
- `path.pop()` → 回溯（把剛加的移除）

```python
def pathSum(root, targetSum):
    result = []

    def dfs(node, remain, path):
        if not node:
            return
        path.append(node.val)

        # 到 leaf 了，檢查和
        if not node.left and not node.right and remain == node.val:
            result.append(path[:])   # 注意：要複製 path！不能直接 append path

        dfs(node.left, remain - node.val, path)
        dfs(node.right, remain - node.val, path)

        path.pop()   # 回溯！把剛加的節點移除

    dfs(root, targetSum, [])
    return result
```

#### Example 1

```
Tree:                    target = 22
       5
      / \
     4   8
    /   / \
   11  13  4
  / \     / \
 7   2   5   1

逐步追蹤 path 和 remain：

dfs(5, 22, [])          → path = [5]
  dfs(4, 17, [5])       → path = [5, 4]
    dfs(11, 13, [5,4])  → path = [5, 4, 11]
      dfs(7, 2, [5,4,11])  → path = [5, 4, 11, 7]
        leaf! 7 != 2 → skip
        path.pop() → path = [5, 4, 11]    ← BACKTRACK
      dfs(2, 2, [5,4,11])  → path = [5, 4, 11, 2]
        leaf! 2 == 2 → FOUND! result = [[5, 4, 11, 2]]
        path.pop() → path = [5, 4, 11]    ← BACKTRACK
      path.pop() → path = [5, 4]          ← BACKTRACK
    path.pop() → path = [5]               ← BACKTRACK
  dfs(8, 17, [5])       → path = [5, 8]
    dfs(13, 9, [5,8])   → path = [5, 8, 13]
      leaf! 13 != 9 → skip
      path.pop() → path = [5, 8]          ← BACKTRACK
    dfs(4, 9, [5,8])    → path = [5, 8, 4]
      dfs(5, 5, [5,8,4])  → path = [5, 8, 4, 5]
        leaf! 5 == 5 → FOUND! result = [[5,4,11,2], [5,8,4,5]]
        path.pop() → path = [5, 8, 4]     ← BACKTRACK
      dfs(1, 5, [5,8,4])  → path = [5, 8, 4, 1]
        leaf! 1 != 5 → skip
        path.pop() → path = [5, 8, 4]     ← BACKTRACK
      path.pop() → path = [5, 8]          ← BACKTRACK
    path.pop() → path = [5]               ← BACKTRACK
  path.pop() → path = []                  ← BACKTRACK

答案：[[5, 4, 11, 2], [5, 8, 4, 5]]
```

#### Example 2

```
Tree:                    target = 6
     1
    / \
   2   2
  /     \
 3       3

追蹤：
dfs(1, 6, [])        → path = [1]
  dfs(2, 5, [1])     → path = [1, 2]
    dfs(3, 3, [1,2]) → path = [1, 2, 3]
      leaf! 3 == 3 → FOUND! result = [[1, 2, 3]]
      path.pop()   → path = [1, 2]
    dfs(None) → return
    path.pop() → path = [1]
  dfs(2, 5, [1])     → path = [1, 2]
    dfs(None) → return
    dfs(3, 3, [1,2]) → path = [1, 2, 3]
      leaf! 3 == 3 → FOUND! result = [[1,2,3], [1,2,3]]
      path.pop()   → path = [1, 2]
    path.pop() → path = [1]
  path.pop() → path = []

答案：[[1, 2, 3], [1, 2, 3]]（兩條對稱路徑）
```

> **常見錯誤**：`result.append(path)` 而不是 `result.append(path[:])` — 這會導致所有結果都指向同一個 list，最後全部變成空 list！一定要**複製**。

---

### 4.3 Binary Tree Maximum Path Sum（LC 124）— Google Hard

> **題意**：找到二元樹中任意路徑的最大節點值總和。路徑可以不經過 root，但不能分叉。

**和 Diameter 完全相同的模式！** 只是把「邊數」換成「節點值的和」。

**核心想法**：
1. 對每個節點，計算「經過此節點的最大路徑和」= `left_gain + node.val + right_gain`
2. 負貢獻的子樹直接捨棄（取 0）
3. 回傳給父節點時，只能選一邊（路徑不能分叉）

```python
def maxPathSum(root):
    best = float('-inf')

    def dfs(node):
        nonlocal best
        if not node:
            return 0
        # 左右子樹的最大貢獻（負的就不要，取 0）
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        # 經過此節點的完整路徑和
        path_sum = left_gain + node.val + right_gain
        best = max(best, path_sum)
        # 回傳給父：只能選一邊！
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return best
```

#### Example 1

```
Tree:
     -10
     / \
    9   20
       / \
      15   7

逐節點計算（bottom-up）：

dfs(9):  left=0, right=0
         left_gain = max(0, 0) = 0
         right_gain = max(0, 0) = 0
         path_sum = 0 + 9 + 0 = 9,   best = max(-inf, 9) = 9
         return 9 + max(0, 0) = 9

dfs(15): left=0, right=0
         path_sum = 0 + 15 + 0 = 15, best = max(9, 15) = 15
         return 15

dfs(7):  left=0, right=0
         path_sum = 0 + 7 + 0 = 7,   best = max(15, 7) = 15
         return 7

dfs(20): left_gain = max(15, 0) = 15
         right_gain = max(7, 0) = 7
         path_sum = 15 + 20 + 7 = 42, best = max(15, 42) = 42 ***
         return 20 + max(15, 7) = 35

dfs(-10): left_gain = max(9, 0) = 9
          right_gain = max(35, 0) = 35
          path_sum = 9 + (-10) + 35 = 34, best = max(42, 34) = 42
          return -10 + max(9, 35) = 25

答案：42（路徑 15→20→7，不經過 root！）

圖示最大路徑：
     -10
     / \
    9  [20]
       / \
     [15] [7]
```

#### Example 2：全部負數

```
Tree:
     -3
     / \
   -2   -1

逐節點計算：

dfs(-2): left=0, right=0
         left_gain = 0, right_gain = 0   （負數子樹不存在，但自身也是負的）
         path_sum = 0 + (-2) + 0 = -2,  best = max(-inf, -2) = -2
         return -2 + max(0, 0) = -2

dfs(-1): path_sum = 0 + (-1) + 0 = -1,  best = max(-2, -1) = -1
         return -1

dfs(-3): left_gain = max(-2, 0) = 0      ← 負的！直接捨棄
         right_gain = max(-1, 0) = 0      ← 負的！直接捨棄
         path_sum = 0 + (-3) + 0 = -3,   best = max(-1, -3) = -1
         return -3 + max(0, 0) = -3

答案：-1（全負數時，取最大的那個單一節點 -1）
```

> **面試 Pattern 總結**：LC 543 (Diameter) 和 LC 124 (Max Path Sum) 是同一個模式：
> 1. Postorder DFS
> 2. 在每個節點計算「經過此節點的最佳解」
> 3. 用 `nonlocal` 全域變數追蹤 overall best
> 4. 回傳給父節點只能選一邊

---

## 第五章：DFS 建構型（Build Trees）

### 5.1 Invert Binary Tree（LC 226）

> **題意**：翻轉二元樹。每個節點的左右子樹互換。

```python
def invertTree(root):
    if not root:
        return None
    # 交換左右子樹
    root.left, root.right = root.right, root.left
    # 遞迴翻轉
    invertTree(root.left)
    invertTree(root.right)
    return root
```

#### Example 1

```
Before:            After:
       4               4
      / \             / \
     2   7           7   2
    / \ / \         / \ / \
   1  3 6  9       9  6 3  1

逐步追蹤：
invertTree(4): swap(2, 7) → 4 的左變 7、右變 2
  invertTree(7): swap(6, 9) → 7 的左變 9、右變 6
    invertTree(9): leaf → return
    invertTree(6): leaf → return
  invertTree(2): swap(1, 3) → 2 的左變 3、右變 1
    invertTree(3): leaf → return
    invertTree(1): leaf → return
```

#### Example 2

```
Before:            After:
     2                 2
    / \               / \
   1   3             3   1

invertTree(2): swap(1, 3)
  invertTree(3): leaf → return
  invertTree(1): leaf → return

就是這麼簡單！每個節點的左右指標互換。
```

---

### 5.2 Construct Binary Tree from Preorder and Inorder Traversal（LC 105）

> **題意**：給你 preorder 和 inorder 兩個陣列，還原出原來的二元樹。

**核心觀察（這是本題的精髓）**：

1. **Preorder 的第一個元素永遠是 root**
2. **在 Inorder 中找到 root 的位置 `idx`**：
   - `inorder[:idx]` = 左子樹的 inorder
   - `inorder[idx+1:]` = 右子樹的 inorder
3. **左子樹的大小 = `idx`**（inorder 中 root 左邊有幾個元素）
4. 用這個大小去切割 preorder：
   - `preorder[1:idx+1]` = 左子樹的 preorder
   - `preorder[idx+1:]` = 右子樹的 preorder

```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None

    # 用 HashMap 加速查找 inorder 中的位置
    inorder_map = {val: i for i, val in enumerate(inorder)}

    def helper(pre_left, pre_right, in_left, in_right):
        if pre_left > pre_right:
            return None

        root_val = preorder[pre_left]          # preorder 第一個 = root
        root = TreeNode(root_val)
        idx = inorder_map[root_val]            # root 在 inorder 中的位置
        left_size = idx - in_left              # 左子樹的節點數

        # 遞迴建立左右子樹
        root.left = helper(pre_left + 1, pre_left + left_size,
                           in_left, idx - 1)
        root.right = helper(pre_left + left_size + 1, pre_right,
                            idx + 1, in_right)
        return root

    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)
```

#### Example 1：Step-by-Step

```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]

Step 1: root = preorder[0] = 3
        在 inorder 中找 3 → idx = 1
        左子樹 inorder = [9]       (idx 左邊)
        右子樹 inorder = [15,20,7] (idx 右邊)
        left_size = 1

        preorder 切割：
        左子樹 preorder = [9]          (index 1 to 1)
        右子樹 preorder = [20, 15, 7]  (index 2 to 4)

                3
               / \
             [9] [20,15,7]

Step 2: 建左子樹
        root = 9，在 inorder [9] 中 idx = 0
        left_size = 0 → 沒有左子
        右邊也沒有 → 9 是葉節點

                3
               / \
              9  [20,15,7]

Step 3: 建右子樹
        root = preorder 中下一個 = 20
        在 inorder [15, 20, 7] 中找 20 → idx = 1
        左子樹 inorder = [15], 右子樹 inorder = [7]

                3
               / \
              9   20
                 / \
               [15] [7]

Step 4: 15 和 7 都是葉節點

最終結果：
       3
      / \
     9   20
        /  \
       15   7
```

#### Example 2：左偏斜的樹

```
preorder = [1, 2, 3]
inorder  = [3, 2, 1]

Step 1: root = 1
        在 inorder [3,2,1] 中找 1 → idx = 2
        左子樹 inorder = [3, 2]   (idx 左邊有 2 個)
        右子樹 inorder = []        (idx 右邊沒有)
        left_size = 2

        preorder 切割：
        左子樹 preorder = [2, 3]
        右子樹 preorder = []

             1
            /
          [2,3]

Step 2: 建左子樹
        root = 2
        在 inorder [3, 2] 中找 2 → idx = 1
        左子樹 inorder = [3], 右子樹 = []
        left_size = 1

             1
            /
           2
          /
        [3]

Step 3: 3 是葉節點

最終結果：
     1
    /
   2
  /
 3

驗證：
  preorder(1→2→3) = [1, 2, 3] ✓
  inorder(3→2→1)  = [3, 2, 1] ✓
```

**為什麼這個方法一定正確？**

數學上，preorder 和 inorder 可以唯一確定一棵二元樹（假設沒有重複值）。因為：
- Preorder 告訴你「誰是 root」
- Inorder 告訴你「誰在 root 左邊、誰在 root 右邊」
- 兩個資訊結合，可以遞迴地確定每一層的結構

**時間複雜度**：O(n)（HashMap 查找 O(1)，每個節點只建一次）
**空間複雜度**：O(n)（HashMap + 遞迴堆疊）

---

## 第六章：面試框架

### 6.1 Top-down vs Bottom-up 決策

面試看到 Tree 題目，第一步問自己：

```
我需要的資訊是從上面傳下來的？ → Top-down (Preorder)
還是從下面算上來的？           → Bottom-up (Postorder)

判斷方法：
  如果你需要「先知道子樹的結果」才能算出當前節點的答案
  → Bottom-up (Postorder)
  → 例：高度、深度、是否平衡、直徑

  如果你需要「把父節點的資訊傳給子節點」
  → Top-down (Preorder)
  → 例：路徑和、剩餘目標值

  如果你需要 BST 的排序特性
  → Inorder
```

### 6.2 Tree DFS 解題模板

```python
def solve(root):
    # 1. Base case
    if not root:
        return <base_value>     # 通常是 0, None, True, False

    # 2. 遞迴求解左右子樹
    left_result = solve(root.left)
    right_result = solve(root.right)

    # 3. 合併結果（Postorder 核心步驟）
    current_result = <combine>(root.val, left_result, right_result)

    # 4. (如果需要全域最佳解) 更新全域變數
    # nonlocal best
    # best = max(best, <something>)

    return current_result
```

### 6.3 需要全域變數的模式（Diameter / Max Path Sum）

```python
def solve_with_global(root):
    best = <initial_value>     # -inf 或 0

    def dfs(node):
        nonlocal best
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        # 在此節點「拐彎」的最佳解
        best = max(best, <combine_both_sides>(left, right, node.val))

        # 回傳給父：只能選一邊
        return <pick_one_side>(left, right, node.val)

    dfs(root)
    return best
```

### 6.4 Whiteboard Tips

**畫圖**：
- 面試一定要畫樹！用小例子（3~5 個節點）手動跑一遍。
- 考慮 edge cases：空樹、只有一個節點、全偏左/右。

**遞迴三要素**：
1. **Base case**：`if not node: return ...` — 什麼時候停？
2. **Recursive step**：對左右子樹遞迴 — 子問題是什麼？
3. **Combine**：把左右結果合併 — 怎麼從子答案得到當前答案？

**時間/空間分析（幾乎所有 Tree DFS 題都一樣）**：
- Time: O(n) — 每個節點拜訪一次
- Space: O(h) — 遞迴堆疊深度 = 樹高
  - 最好情況（平衡樹）：O(log n)
  - 最差情況（偏斜樹）：O(n)

### 6.5 本章題目一覽 + 難度

| # | 題目 | 難度 | 模式 | Google 頻率 |
|---|------|------|------|-------------|
| 104 | Maximum Depth | Easy | Postorder 求值 | 中 |
| 543 | Diameter of Binary Tree | Easy | Postorder + 全域變數 | 高 |
| 110 | Balanced Binary Tree | Easy | Postorder 判定 | 中 |
| 112 | Path Sum | Easy | Preorder 路徑 | 中 |
| 113 | Path Sum II | Medium | Preorder + Backtracking | 中 |
| 124 | Max Path Sum | Hard | Postorder + 全域變數 | 極高 |
| 226 | Invert Binary Tree | Easy | Preorder 建構 | 中 |
| 105 | Construct from Pre+In | Medium | 分治法 | 高 |

### 6.6 學習路線建議

```
Week 1: 三種遍歷 — 遞迴 + 迭代都要能秒寫
         ↓
Week 2: LC 104, 110, 226 — 最基本的 postorder / preorder
         ↓
Week 3: LC 543, 112, 113 — Diameter + Path Sum 系列
         ↓
Week 4: LC 124, 105 — Hard 題 + 建構題
         ↓
Week 5: 混合練習 — 看到題目能立刻判斷用哪種遍歷
```

> **最終心法**：Tree 題的本質就是遞迴。搞懂「base case 是什麼、子問題是什麼、怎麼合併結果」，90% 的 Tree 題都能解。剩下 10% 需要 BFS 或特殊技巧，那是下一章的內容。
