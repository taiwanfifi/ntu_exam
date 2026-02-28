"""
07_Tree_DFS.py - 樹的深度優先搜尋完整教學 (Tree DFS Complete Guide)
====================================================================
目標讀者: 準備 Google / NVIDIA 面試的初學者
教學方式: 每題 3 個範例，逐步追蹤遞迴呼叫堆疊 (call stack trace)
語言: 繁體中文 + English 關鍵術語
執行方式: python 07_Tree_DFS.py

Sections:
  1. 三種遍歷 (Preorder / Inorder / Postorder) - recursive & iterative
  2. DFS 求值型 (Max Depth, Min Depth, Diameter, Balanced)
  3. DFS 路徑型 (Path Sum, Path Sum II, Max Path Sum)
  4. DFS 建構/轉換型 (Invert, Flatten, Construct from Preorder+Inorder)
  5. 三種遍歷使用時機 Decision Tree
"""
from typing import List, Optional

# ============================================================
# TreeNode 定義 & 輔助函式 (TreeNode & Helper Utilities)
# ============================================================
class TreeNode:
    """二元樹節點 (Binary Tree Node)"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return f"TreeNode({self.val})"

def build_tree(vals: list) -> Optional[TreeNode]:
    """
    從 list 建立二元樹 (level-order).
    例: [1, 2, 3, None, 4] =>    1
                                 / \
                                2   3
                                 \
                                  4
    """
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root

def tree_to_list(root: Optional[TreeNode]) -> list:
    """二元樹轉回 list (level-order), 方便驗證"""
    if not root:
        return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result

def draw(label, lines):
    """印出樹的 ASCII 圖"""
    print(f"  {label}")
    for l in lines:
        print(f"  {l}")

# ============================================================
# Section 1: 三種遍歷 (Three Traversals) - 核心中的核心
# ============================================================

# ------ 1a. Preorder 前序遍歷: Root -> Left -> Right ------
def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """前序遍歷 - 遞迴版 (Recursive Preorder)"""
    result = []
    def dfs(node):
        if not node: return
        result.append(node.val)   # 先訪問 Root
        dfs(node.left)            # 再走 Left
        dfs(node.right)           # 最後 Right
    dfs(root)
    return result

def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """前序遍歷 - 迭代版: stack, 先 push right 再 push left (LIFO)"""
    if not root: return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)  # 先 push right
        if node.left:  stack.append(node.left)   # 再 push left => left 先 pop
    return result

def demo_preorder():
    print("=" * 60)
    print("1a. Preorder 前序遍歷: Root -> Left -> Right")
    print("=" * 60)
    # --- 範例 1 ---
    #       1            Preorder DFS 追蹤:
    #      / \           call dfs(1): visit 1, go left
    #     2   3            call dfs(2): visit 2, go left
    #    / \                 call dfs(4): visit 4, L=None, R=None -> return
    #   4   5              back to dfs(2): go right
    #                        call dfs(5): visit 5, L=None, R=None -> return
    #                      back to dfs(2): done -> return
    #                    back to dfs(1): go right
    #                      call dfs(3): visit 3, L=None, R=None -> return
    #                    Result: [1, 2, 4, 5, 3]
    t1 = build_tree([1, 2, 3, 4, 5])
    draw("[1,2,3,4,5]:", ["    1    ", "   / \\  ", "  2   3  ", " / \\    ", "4   5    "])
    r1, i1 = preorder_recursive(t1), preorder_iterative(t1)
    print(f"  Recursive: {r1}  |  Iterative: {i1}")
    assert r1 == [1, 2, 4, 5, 3] and r1 == i1

    # --- 範例 2 ---
    #   10        call dfs(10): visit 10, go left
    #   /           call dfs(20): visit 20, go left
    #  20             call dfs(30): visit 30 -> return
    #  /            back to dfs(20): right=None -> return
    # 30          back to dfs(10): right=None -> return
    #             Result: [10, 20, 30]
    t2 = build_tree([10, 20, None, 30])
    draw("[10,20,None,30] (左偏斜):", ["10  ", "/ ", "20  ", "/  ", "30  "])
    r2, i2 = preorder_recursive(t2), preorder_iterative(t2)
    print(f"  Recursive: {r2}  |  Iterative: {i2}")
    assert r2 == [10, 20, 30] and r2 == i2

    # --- 範例 3 ---
    #       5         call dfs(5): visit 5, go left
    #      / \          call dfs(3): visit 3 -> dfs(1): visit 1
    #     3   8           -> back, dfs(4): visit 4
    #    / \   \        back to dfs(5): go right
    #   1   4   9         call dfs(8): visit 8, dfs(9): visit 9
    #                   Result: [5, 3, 1, 4, 8, 9]
    t3 = build_tree([5, 3, 8, 1, 4, None, 9])
    draw("[5,3,8,1,4,None,9] (BST):", ["    5    ", "   / \\  ", "  3   8  ", " / \\   \\", "1   4   9"])
    r3, i3 = preorder_recursive(t3), preorder_iterative(t3)
    print(f"  Recursive: {r3}  |  Iterative: {i3}")
    assert r3 == [5, 3, 1, 4, 8, 9] and r3 == i3

# ------ 1b. Inorder 中序遍歷: Left -> Root -> Right ------
def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """中序遍歷 - 遞迴版"""
    result = []
    def dfs(node):
        if not node: return
        dfs(node.left)            # 先走 Left
        result.append(node.val)   # 訪問 Root
        dfs(node.right)           # 最後 Right
    dfs(root)
    return result

def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """中序遍歷 - 迭代版: 一路往左到底, pop 出來才訪問, 再轉向右"""
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:           # 一路往左
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()    # 彈出 = 訪問
        result.append(curr.val)
        curr = curr.right     # 轉向右子樹
    return result

def demo_inorder():
    print("\n" + "=" * 60)
    print("1b. Inorder 中序遍歷: Left -> Root -> Right")
    print("=" * 60)
    # --- 範例 1 ---
    #       1       call dfs(1): go left
    #      / \        call dfs(2): go left
    #     2   3         call dfs(4): L=None, visit 4, R=None -> return
    #    / \          back to dfs(2): visit 2, go right
    #   4   5           call dfs(5): L=None, visit 5, R=None -> return
    #                 back to dfs(1): visit 1, go right
    #                   call dfs(3): L=None, visit 3, R=None -> return
    #                 Result: [4, 2, 5, 1, 3]
    t1 = build_tree([1, 2, 3, 4, 5])
    draw("[1,2,3,4,5]:", ["    1    ", "   / \\  ", "  2   3  ", " / \\    ", "4   5    "])
    r1, i1 = inorder_recursive(t1), inorder_iterative(t1)
    print(f"  Recursive: {r1}  |  Iterative: {i1}")
    assert r1 == [4, 2, 5, 1, 3] and r1 == i1

    # --- 範例 2 ---
    #   10       dfs(10)->dfs(20)->dfs(30): L=None, visit 30 -> return
    #   /        back: visit 20 -> return, back: visit 10 -> return
    #  20        Result: [30, 20, 10]
    #  /
    # 30
    t2 = build_tree([10, 20, None, 30])
    draw("[10,20,None,30] (左偏斜):", ["10", "/", "20", "/", "30"])
    r2, i2 = inorder_recursive(t2), inorder_iterative(t2)
    print(f"  Recursive: {r2}  |  Iterative: {i2}")
    assert r2 == [30, 20, 10] and r2 == i2

    # --- 範例 3 (BST -> Inorder = sorted!) ---
    #       5       dfs(5)->dfs(3)->dfs(1): visit 1
    #      / \      back: visit 3, dfs(4): visit 4
    #     3   8     back to dfs(5): visit 5, dfs(8): L=None, visit 8
    #    / \   \      dfs(9): visit 9
    #   1   4   9   Result: [1, 3, 4, 5, 8, 9]  <-- sorted!
    t3 = build_tree([5, 3, 8, 1, 4, None, 9])
    draw("[5,3,8,1,4,None,9] (BST):", ["    5    ", "   / \\  ", "  3   8  ", " / \\   \\", "1   4   9"])
    r3, i3 = inorder_recursive(t3), inorder_iterative(t3)
    print(f"  Recursive: {r3}  |  Iterative: {i3}")
    print("  ** BST Inorder = sorted! **")
    assert r3 == [1, 3, 4, 5, 8, 9] and r3 == i3

# ------ 1c. Postorder 後序遍歷: Left -> Right -> Root ------
def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """後序遍歷 - 遞迴版"""
    result = []
    def dfs(node):
        if not node: return
        dfs(node.left)            # 先走 Left
        dfs(node.right)           # 再走 Right
        result.append(node.val)   # 最後訪問 Root
    dfs(root)
    return result

def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    後序迭代: 修改 preorder (Root->Right->Left), 最後反轉
    preorder 先 push left 再 push right => Root->Right->Left
    反轉 => Left->Right->Root = postorder
    """
    if not root: return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:  stack.append(node.left)   # 先 push left (後 pop)
        if node.right: stack.append(node.right)  # 再 push right (先 pop)
    return result[::-1]  # 反轉!

def demo_postorder():
    print("\n" + "=" * 60)
    print("1c. Postorder 後序遍歷: Left -> Right -> Root")
    print("=" * 60)
    # --- 範例 1 ---
    #       1       call dfs(1): go left
    #      / \        call dfs(2): go left
    #     2   3         call dfs(4): L=None, R=None, visit 4
    #    / \            call dfs(5): L=None, R=None, visit 5
    #   4   5         visit 2 -> return
    #                 call dfs(3): L=None, R=None, visit 3
    #                 visit 1 -> return
    #                 Result: [4, 5, 2, 3, 1]
    t1 = build_tree([1, 2, 3, 4, 5])
    draw("[1,2,3,4,5]:", ["    1    ", "   / \\  ", "  2   3  ", " / \\    ", "4   5    "])
    r1, i1 = postorder_recursive(t1), postorder_iterative(t1)
    print(f"  Recursive: {r1}  |  Iterative: {i1}")
    assert r1 == [4, 5, 2, 3, 1] and r1 == i1

    # --- 範例 2 ---
    # 10/20/30 左偏: dfs(30)->visit 30, back->visit 20, back->visit 10
    # Result: [30, 20, 10]
    t2 = build_tree([10, 20, None, 30])
    draw("[10,20,None,30]:", ["10", "/", "20", "/", "30"])
    r2, i2 = postorder_recursive(t2), postorder_iterative(t2)
    print(f"  Recursive: {r2}  |  Iterative: {i2}")
    assert r2 == [30, 20, 10] and r2 == i2

    # --- 範例 3 ---
    #       5       dfs(1)->visit 1, dfs(4)->visit 4, visit 3
    #      / \      dfs(9)->visit 9, visit 8, visit 5
    #     3   8     Result: [1, 4, 3, 9, 8, 5]
    #    / \   \
    #   1   4   9
    t3 = build_tree([5, 3, 8, 1, 4, None, 9])
    draw("[5,3,8,1,4,None,9]:", ["    5    ", "   / \\  ", "  3   8  ", " / \\   \\", "1   4   9"])
    r3, i3 = postorder_recursive(t3), postorder_iterative(t3)
    print(f"  Recursive: {r3}  |  Iterative: {i3}")
    assert r3 == [1, 4, 3, 9, 8, 5] and r3 == i3

    # 三種遍歷總結
    print("\n--- 三種遍歷總結 (同一棵樹 [1,2,3,4,5]) ---")
    t = build_tree([1, 2, 3, 4, 5])
    print(f"  Preorder  (Root-L-R): {preorder_recursive(t)}")
    print(f"  Inorder   (L-Root-R): {inorder_recursive(t)}")
    print(f"  Postorder (L-R-Root): {postorder_recursive(t)}")

# ============================================================
# Section 2: DFS 求值型 (DFS Value Problems)
# ============================================================

# ------ 2a. Maximum Depth (LeetCode 104) ------
def max_depth(root: Optional[TreeNode]) -> int:
    """最大深度 = max(左深度, 右深度) + 1. 思路: 後序 (先算子樹再算自己)"""
    if not root: return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1

def demo_max_depth():
    print("\n" + "=" * 60)
    print("2a. Maximum Depth 最大深度 (LeetCode 104)")
    print("=" * 60)
    # --- 範例 1 ---
    #       3       max_depth(3):
    #      / \        L = max_depth(9) = 1
    #     9  20       R = max_depth(20): L=max_depth(15)=1, R=max_depth(7)=1
    #       /  \          = max(1,1)+1 = 2
    #      15   7     = max(1, 2) + 1 = 3
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    draw("[3,9,20,None,None,15,7]:", ["    3   ", "   / \\ ", "  9  20 ", "    / \\", "   15  7"])
    print(f"  Max Depth = {max_depth(t1)}")
    assert max_depth(t1) == 3

    # --- 範例 2 ---
    #   1          max_depth(1): L=0, R=max_depth(2)=1
    #    \         = max(0,1)+1 = 2
    #     2
    t2 = build_tree([1, None, 2])
    draw("[1,None,2] (右偏斜):", ["1 ", " \\", "  2"])
    print(f"  Max Depth = {max_depth(t2)}")
    assert max_depth(t2) == 2

    # --- 範例 3 ---
    #       1       max_depth(1):
    #      / \        L = max_depth(2) -> max_depth(4) -> max_depth(5) = 1
    #     2   3         -> max(1,0)+1=2 -> max(2,0)+1=3
    #    /            R = max_depth(3) = 1
    #   4             = max(3,1)+1 = 4
    #  /
    # 5
    t3 = build_tree([1, 2, 3, 4, None, None, None, 5])
    draw("深度不平衡:", ["      1   ", "     / \\ ", "    2   3 ", "   /      ", "  4       ", " /        ", "5         "])
    print(f"  Max Depth = {max_depth(t3)}")
    assert max_depth(t3) == 4

# ------ 2b. Minimum Depth (LeetCode 111) ------
def min_depth(root: Optional[TreeNode]) -> int:
    """
    最小深度: 根到最近「葉節點」的距離
    陷阱! 跟 max_depth 不同: None 不是葉節點
    如果一邊是 None, 必須走另一邊
    """
    if not root: return 0
    if not root.left:  return min_depth(root.right) + 1  # 只有右子樹
    if not root.right: return min_depth(root.left) + 1   # 只有左子樹
    return min(min_depth(root.left), min_depth(root.right)) + 1

def demo_min_depth():
    print("\n" + "=" * 60)
    print("2b. Minimum Depth 最小深度 (LeetCode 111)")
    print("    陷阱: None 不是葉節點!")
    print("=" * 60)
    # --- 範例 1 ---
    #       3       min_depth(3):
    #      / \        L = min_depth(9) = 1 (leaf)
    #     9  20       R = min_depth(20) = min(1,1)+1 = 2
    #       /  \      = min(1, 2) + 1 = 2  (路徑: 3->9)
    #      15   7
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    draw("[3,9,20,None,None,15,7]:", ["    3   ", "   / \\ ", "  9  20 ", "    / \\", "   15  7"])
    print(f"  Min Depth = {min_depth(t1)}  (路徑: 3->9)")
    assert min_depth(t1) == 2

    # --- 範例 2 (陷阱!) ---
    #   1          min_depth(1): left=None -> min_depth(right)+1
    #    \           min_depth(2): left=None -> min_depth(3)+1 = 2
    #     2          = 2+1 = 3
    #      \         答案是 3, 不是 1! (None 不是葉節點)
    #       3
    t2 = build_tree([1, None, 2, None, 3])
    draw("[1,None,2,None,3] (陷阱!):", ["1 ", " \\", "  2", "   \\", "    3"])
    print(f"  Min Depth = {min_depth(t2)}  (不是 1! None 不是葉節點)")
    assert min_depth(t2) == 3

    # --- 範例 3 ---
    #       1       min_depth(1):
    #      / \        L=min_depth(2): left=None -> min_depth(4)+1=2
    #     2   3       R=min_depth(3): right=None -> ... wait
    #    /     \        left=None -> min_depth(5)+1 = 2
    #   4       5     = min(2, 2) + 1 = 3
    t3 = build_tree([1, 2, 3, 4, None, None, 5])
    draw("[1,2,3,4,None,None,5]:", ["    1   ", "   / \\ ", "  2   3 ", " /     \\", "4       5"])
    print(f"  Min Depth = {min_depth(t3)}")
    assert min_depth(t3) == 3

# ------ 2c. Diameter of Binary Tree (LeetCode 543) ------
def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    直徑 = 任意兩節點間最長路徑的邊數
    關鍵: 經過某節點的路徑長 = 左子樹深度 + 右子樹深度
    技巧: nonlocal 全域變數記錄最大值
    """
    diameter = 0
    def depth(node):
        nonlocal diameter
        if not node: return 0
        left_d = depth(node.left)
        right_d = depth(node.right)
        diameter = max(diameter, left_d + right_d)  # 經過此節點的路徑
        return max(left_d, right_d) + 1
    depth(root)
    return diameter

def demo_diameter():
    print("\n" + "=" * 60)
    print("2c. Diameter of Binary Tree 直徑 (LeetCode 543)")
    print("    技巧: nonlocal 全域變數")
    print("=" * 60)
    # --- 範例 1 ---
    #       1       depth(1):
    #      / \        depth(2): depth(4)=1, depth(5)=1
    #     2   3         diam=max(0,1+1)=2, return 2
    #    / \          depth(3): L=0, R=0, return 1
    #   4   5         diam=max(2, 2+1)=3, return 3
    #                 Final = 3 (路徑: 4->2->1->3)
    t1 = build_tree([1, 2, 3, 4, 5])
    draw("[1,2,3,4,5]:", ["    1    ", "   / \\  ", "  2   3  ", " / \\    ", "4   5    "])
    print(f"  Diameter = {diameter_of_binary_tree(t1)}  (路徑: 4->2->1->3)")
    assert diameter_of_binary_tree(t1) == 3

    # --- 範例 2 ---
    t2 = build_tree([1, 2])
    draw("[1,2]:", ["1", "/", "2"])
    print(f"  Diameter = {diameter_of_binary_tree(t2)}")
    assert diameter_of_binary_tree(t2) == 1

    # --- 範例 3 (最長路徑不經過 root!) ---
    #       1       depth(2):
    #      /          depth(3): depth(5)=1, R=0, diam=1, return 2
    #     2           depth(4): L=0, depth(6)=1, diam=1, return 2
    #    / \          diam = max(1, 2+2) = 4, return 3
    #   3   4       depth(1): diam = max(4, 3+0) = 4
    #  /     \      Final = 4 (路徑: 5->3->2->4->6, 不經過 root!)
    # 5       6
    t3 = build_tree([1, 2, None, 3, 4, 5, None, None, 6])
    draw("最長路徑不經過 root:", ["      1   ", "     /    ", "    2     ", "   / \\   ", "  3   4   ", " /     \\ ", "5       6 "])
    print(f"  Diameter = {diameter_of_binary_tree(t3)}  (路徑: 5->3->2->4->6)")
    assert diameter_of_binary_tree(t3) == 4

# ------ 2d. Balanced Binary Tree (LeetCode 110) ------
def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    平衡 = 每個節點的左右子樹高度差 <= 1
    技巧: 用 -1 表示「不平衡」, 提前終止 (剪枝)
    """
    def check(node):
        if not node: return 0
        left_h = check(node.left)
        if left_h == -1: return -1
        right_h = check(node.right)
        if right_h == -1: return -1
        if abs(left_h - right_h) > 1: return -1
        return max(left_h, right_h) + 1
    return check(root) != -1

def demo_balanced():
    print("\n" + "=" * 60)
    print("2d. Balanced Binary Tree 平衡判定 (LeetCode 110)")
    print("=" * 60)
    # --- 範例 1 ---
    #       3       check(3): L=check(9)=1, R=check(20)=2
    #      / \      |1-2|=1 <= 1 -> balanced (return 3)
    #     9  20
    #       /  \
    #      15   7
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    draw("[3,9,20,None,None,15,7]:", ["    3   ", "   / \\ ", "  9  20 ", "    / \\", "   15  7"])
    print(f"  Balanced? {is_balanced(t1)}")
    assert is_balanced(t1) is True

    # --- 範例 2 ---
    #       1       check(1): L=check(2)=3, R=check(2)=1
    #      / \      |3-1| = 2 > 1 -> return -1 -> False
    #     2   2
    #    / \
    #   3   3
    #  / \
    # 4   4
    t2 = build_tree([1, 2, 2, 3, 3, None, None, 4, 4])
    draw("[1,2,2,3,3,None,None,4,4]:", ["      1    ", "     / \\  ", "    2   2  ", "   / \\    ", "  3   3    ", " / \\      ", "4   4      "])
    print(f"  Balanced? {is_balanced(t2)}  (左邊太深)")
    assert is_balanced(t2) is False

    # --- 範例 3 ---
    print("\n  範例 3: 空樹 (None)")
    print(f"  Balanced? {is_balanced(None)}  (空樹視為平衡)")
    assert is_balanced(None) is True

# ============================================================
# Section 3: DFS 路徑型 (DFS Path Problems)
# ============================================================

# ------ 3a. Path Sum (LeetCode 112) ------
def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
    """
    判斷是否存在 root-to-leaf 路徑, 節點值總和 = target
    技巧: 每往下走, target 減去當前值; 到葉節點檢查是否 = 0
    """
    if not root: return False
    if not root.left and not root.right:  # 葉節點
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))

def demo_path_sum():
    print("\n" + "=" * 60)
    print("3a. Path Sum 路徑和 (LeetCode 112)")
    print("=" * 60)
    # --- 範例 1 ---
    #         5       has_path_sum(5, 22):
    #        / \        left: has_path_sum(4, 17):
    #       4   8         left: has_path_sum(11, 13):
    #      /   / \          left: has_path_sum(7, 2): leaf, 7!=2 -> False
    #     11  13  4         right: has_path_sum(2, 2): leaf, 2==2 -> True!
    #    /  \      \      路徑: 5->4->11->2 = 22
    #   7    2      1
    t1 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    draw("target=22:", ["      5     ", "     / \\   ", "    4   8   ", "   /   / \\ ", "  11  13  4 ", " /  \\      \\", "7    2      1"])
    print(f"  Path Sum 22? {has_path_sum(t1, 22)}  (路徑: 5->4->11->2)")
    assert has_path_sum(t1, 22) is True

    # --- 範例 2 ---
    #   1       has_path_sum(1, 5):
    #  / \        L: has_path_sum(2, 4): leaf, 2!=4 -> False
    # 2   3       R: has_path_sum(3, 4): leaf, 3!=4 -> False
    t2 = build_tree([1, 2, 3])
    draw("[1,2,3], target=5:", ["  1 ", " / \\", "2   3"])
    print(f"  Path Sum 5? {has_path_sum(t2, 5)}")
    assert has_path_sum(t2, 5) is False

    # --- 範例 3 ---
    #   1       has_path_sum(1, 4):
    #  / \        R: has_path_sum(3, 3): leaf, 3==3 -> True!
    # 2   3
    t3 = build_tree([1, 2, 3])
    draw("[1,2,3], target=4:", ["  1 ", " / \\", "2   3"])
    print(f"  Path Sum 4? {has_path_sum(t3, 4)}  (路徑: 1->3)")
    assert has_path_sum(t3, 4) is True

# ------ 3b. Path Sum II (LeetCode 113) ------
def path_sum_ii(root: Optional[TreeNode], target: int) -> List[List[int]]:
    """
    找出所有 root-to-leaf 路徑使得總和 = target
    技巧: backtracking - append -> 遞迴 -> pop (回溯)
    """
    result = []
    def dfs(node, remain, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remain == node.val:
            result.append(path[:])  # 複製! 不能直接 append path
        else:
            dfs(node.left, remain - node.val, path)
            dfs(node.right, remain - node.val, path)
        path.pop()  # 回溯 (backtrack)!
    dfs(root, target, [])
    return result

def demo_path_sum_ii():
    print("\n" + "=" * 60)
    print("3b. Path Sum II 所有路徑 (LeetCode 113) - Backtracking")
    print("=" * 60)
    # --- 範例 1 ---
    #         5       target=22, 追蹤:
    #        / \      dfs(5,22,[]): path=[5]
    #       4   8       dfs(4,17,[5]): path=[5,4]
    #      /   / \        dfs(11,13,[5,4]): path=[5,4,11]
    #     11  13  4         dfs(7,2,...): leaf, 7!=2 -> pop
    #    /  \    / \         dfs(2,2,...): leaf, 2==2 -> FOUND [5,4,11,2]! pop
    #   7    2  5   1     dfs(8,17,[5]): path=[5,8]
    #                       dfs(4,9,[5,8]): dfs(5,5,...): FOUND [5,8,4,5]!
    t1 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    draw("target=22:", ["       5      ", "      / \\    ", "     4   8    ", "    /   / \\  ", "   11  13  4  ", "  /  \\    / \\", " 7    2  5   1"])
    r1 = path_sum_ii(t1, 22)
    print(f"  Paths: {r1}")
    assert r1 == [[5, 4, 11, 2], [5, 8, 4, 5]]

    # --- 範例 2 ---
    #   1       dfs(1,3,[]): path=[1]
    #  / \        dfs(2,2,[1]): leaf, 2==2 -> FOUND [1,2]!
    # 2   3       dfs(3,2,[1]): leaf, 3!=2 -> pop
    t2 = build_tree([1, 2, 3])
    draw("[1,2,3], target=3:", ["  1 ", " / \\", "2   3"])
    r2 = path_sum_ii(t2, 3)
    print(f"  Paths: {r2}")
    assert r2 == [[1, 2]]

    # --- 範例 3 ---
    #     1       target=6: 兩條對稱路徑
    #    / \      [1,2,3] 和 [1,2,3]
    #   2   2
    #  /     \
    # 3       3
    t3 = build_tree([1, 2, 2, 3, None, None, 3])
    draw("[1,2,2,3,None,None,3], target=6:", ["    1   ", "   / \\ ", "  2   2 ", " /     \\", "3       3"])
    r3 = path_sum_ii(t3, 6)
    print(f"  Paths: {r3}  (兩條對稱路徑)")
    assert r3 == [[1, 2, 3], [1, 2, 3]]

# ------ 3c. Binary Tree Maximum Path Sum (LeetCode 124 - Hard) ------
def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    找任意路徑 (不一定經過 root) 的最大節點值總和. Google 熱門!
    路徑不能分叉, 但可以拐彎 (經過某節點連接左右).

    關鍵:
    - 每個節點: 經過此節點的路徑和 = left_gain + val + right_gain
    - 回傳給父: 只能選一邊 (不能分叉!) = val + max(left, right)
    - 負貢獻的子樹直接捨棄 (取 0)
    """
    best = float('-inf')
    def dfs(node):
        nonlocal best
        if not node: return 0
        left_gain = max(dfs(node.left), 0)    # 負的就不要
        right_gain = max(dfs(node.right), 0)
        best = max(best, left_gain + node.val + right_gain)  # 經過此節點
        return node.val + max(left_gain, right_gain)  # 回傳只選一邊
    dfs(root)
    return best

def demo_max_path_sum():
    print("\n" + "=" * 60)
    print("3c. Maximum Path Sum (LeetCode 124 - Hard, Google 熱門)")
    print("    技巧同 Diameter: nonlocal + 回傳只選一邊")
    print("=" * 60)
    # --- 範例 1 ---
    #   1       dfs(1):
    #  / \        left_gain = dfs(2) = 2 (leaf, path=2, best=2)
    # 2   3       right_gain = dfs(3) = 3 (leaf, path=3, best=3)
    #             path_through = 2+1+3 = 6, best=6
    #             return 1+max(2,3) = 4
    #             Final = 6 (路徑: 2->1->3)
    t1 = build_tree([1, 2, 3])
    draw("[1,2,3]:", ["  1 ", " / \\", "2   3"])
    print(f"  Max Path Sum = {max_path_sum(t1)}  (路徑: 2->1->3)")
    assert max_path_sum(t1) == 6

    # --- 範例 2 ---
    #    -10      dfs(-10):
    #    / \        dfs(9)=9 (best=9)
    #   9  20       dfs(20): dfs(15)=15, dfs(7)=7
    #     /  \        path=15+20+7=42, best=42, return 35
    #    15   7     left_gain=max(9,0)=9, right=max(35,0)=35
    #               path=9+(-10)+35=34, best=max(42,34)=42
    #               Final = 42 (路徑: 15->20->7, 不經過 root!)
    t2 = build_tree([-10, 9, 20, None, None, 15, 7])
    draw("[-10,9,20,None,None,15,7]:", ["   -10  ", "   / \\ ", "  9  20 ", "    / \\", "   15  7"])
    print(f"  Max Path Sum = {max_path_sum(t2)}  (路徑: 15->20->7)")
    assert max_path_sum(t2) == 42

    # --- 範例 3 (全負數) ---
    #    -3      dfs(-3):
    #    / \       dfs(-2): L=0,R=0, path=-2, best=-2, return -2
    #  -2  -1        left_gain = max(-2, 0) = 0 (負的不要!)
    #              dfs(-1): path=-1, best=-1, return -1
    #                right_gain = max(-1, 0) = 0
    #              path = 0+(-3)+0 = -3, best = max(-1,-3) = -1
    #              Final = -1 (只取一個節點)
    t3 = build_tree([-3, -2, -1])
    draw("[-3,-2,-1] (全負數):", ["   -3  ", "   / \\", "  -2 -1"])
    print(f"  Max Path Sum = {max_path_sum(t3)}  (只取 -1)")
    assert max_path_sum(t3) == -1

# ============================================================
# Section 4: DFS 建構/轉換型 (Build / Transform)
# ============================================================

# ------ 4a. Invert Binary Tree (LeetCode 226) ------
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """翻轉 = 每個節點的左右子樹互換, 遞迴處理"""
    if not root: return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root

def demo_invert():
    print("\n" + "=" * 60)
    print("4a. Invert Binary Tree 翻轉二元樹 (LeetCode 226)")
    print("=" * 60)
    # --- 範例 1 ---
    #   Before:       After:        invert(4): swap(2,7)
    #       4             4           invert(7): swap(6,9) -> {9,6}
    #      / \           / \          invert(2): swap(1,3) -> {3,1}
    #     2   7         7   2
    #    / \ / \       / \ / \
    #   1  3 6  9     9  6 3  1
    t1 = build_tree([4, 2, 7, 1, 3, 6, 9])
    print("\n  Before: [4,2,7,1,3,6,9]    After:")
    print("       4           4      ")
    print("      / \\         / \\    ")
    print("     2   7       7   2    ")
    print("    / \\ / \\     / \\ / \\ ")
    print("   1  3 6  9   9  6 3  1  ")
    invert_tree(t1)
    r1 = tree_to_list(t1)
    print(f"  After: {r1}")
    assert r1 == [4, 7, 2, 9, 6, 3, 1]

    # --- 範例 2 ---
    #   Before:   After:
    #     2         2       invert(2): swap(1,3)
    #    / \       / \
    #   1   3     3   1
    t2 = build_tree([2, 1, 3])
    invert_tree(t2)
    print(f"\n  [2,1,3] -> After: {tree_to_list(t2)}")
    assert tree_to_list(t2) == [2, 3, 1]

    # --- 範例 3 ---
    #   Before:    After:
    #     1          1      invert(1): swap(2, None)
    #    /            \       -> left=None, right=2
    #   2              2
    t3 = build_tree([1, 2])
    invert_tree(t3)
    print(f"  [1,2] -> After: {tree_to_list(t3)}  (左變右)")
    assert tree_to_list(t3) == [1, None, 2]

# ------ 4b. Flatten Binary Tree to Linked List (LeetCode 114) ------
def flatten(root: Optional[TreeNode]) -> None:
    """
    展平為鏈結串列 (in-place), preorder 順序
    所有 left=None, right=下一個節點
    技巧: 把右子樹接到左子樹最右邊, 再把左移到右
    """
    curr = root
    while curr:
        if curr.left:
            rightmost = curr.left  # 找左子樹最右節點
            while rightmost.right:
                rightmost = rightmost.right
            rightmost.right = curr.right  # 接上原本的右子樹
            curr.right = curr.left        # 左移到右
            curr.left = None
        curr = curr.right

def flatten_to_list(root: Optional[TreeNode]) -> List[int]:
    """輔助: 展平後轉 list"""
    result = []
    while root:
        result.append(root.val)
        assert root.left is None, "left should be None"
        root = root.right
    return result

def demo_flatten():
    print("\n" + "=" * 60)
    print("4b. Flatten to Linked List (LeetCode 114)")
    print("=" * 60)
    # --- 範例 1 ---
    #   Before:           After (linked list):
    #       1              1->2->3->4->5->6
    #      / \
    #     2   5           步驟:
    #    / \   \          curr=1: left=2, 左子樹最右=4
    #   3   4   6           4.right=5, 1.right=2, 1.left=None
    #                     curr=2: left=3, 最右=3, 3.right=4
    #                     curr=3->4->5->6: no left, move right
    t1 = build_tree([1, 2, 5, 3, 4, None, 6])
    draw("[1,2,5,3,4,None,6]:", ["    1    ", "   / \\  ", "  2   5  ", " / \\   \\", "3   4   6"])
    flatten(t1)
    r1 = flatten_to_list(t1)
    print(f"  Flattened: {r1}")
    assert r1 == [1, 2, 3, 4, 5, 6]

    # --- 範例 2 ---
    t2 = build_tree([1, 2, None, 3])
    draw("[1,2,None,3]:", ["  1", " / ", "2  ", "/  ", "3  "])
    flatten(t2)
    print(f"  Flattened: {flatten_to_list(t2)}")
    assert flatten_to_list(t2) == [1, 2, 3]

    # --- 範例 3 ---
    t3 = build_tree([1, None, 2, None, 3])
    print("\n  [1,None,2,None,3] (已展平, 不變)")
    flatten(t3)
    print(f"  Flattened: {flatten_to_list(t3)}")
    assert flatten_to_list(t3) == [1, 2, 3]

# ------ 4c. Construct from Preorder and Inorder (LeetCode 105) ------
def build_from_preorder_inorder(preorder: List[int],
                                 inorder: List[int]) -> Optional[TreeNode]:
    """
    從前序 + 中序重建二元樹

    核心觀察:
    1. preorder[0] = root
    2. 在 inorder 找 root 位置 idx:
       - inorder[:idx] = 左子樹中序, inorder[idx+1:] = 右子樹中序
    3. 左子樹大小 = idx:
       - preorder[1:idx+1] = 左子樹前序, preorder[idx+1:] = 右子樹前序
    4. 遞迴建左右
    """
    if not preorder or not inorder:
        return None
    inorder_map = {val: i for i, val in enumerate(inorder)}  # O(1) lookup

    def helper(pre_left, pre_right, in_left, in_right):
        if pre_left > pre_right: return None
        root_val = preorder[pre_left]
        root = TreeNode(root_val)
        idx = inorder_map[root_val]
        left_size = idx - in_left
        root.left = helper(pre_left + 1, pre_left + left_size,
                           in_left, idx - 1)
        root.right = helper(pre_left + left_size + 1, pre_right,
                            idx + 1, in_right)
        return root

    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)

def demo_build_tree():
    print("\n" + "=" * 60)
    print("4c. Construct from Preorder + Inorder (LeetCode 105)")
    print("=" * 60)
    # --- 範例 1 ---
    #   preorder = [3, 9, 20, 15, 7]
    #   inorder  = [9, 3, 15, 20, 7]
    #
    #   Step 1: root = preorder[0] = 3
    #   Step 2: 3 在 inorder idx=1 -> 左=[9], 右=[15,20,7]
    #   Step 3: 左 preorder=[9], 右 preorder=[20,15,7]
    #   Step 4: 遞迴建左 root=9 (葉), 建右 root=20 -> 左=15, 右=7
    #   Result:     3
    #              / \
    #             9  20
    #               /  \
    #              15   7
    pre1, ino1 = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    print(f"\n  範例 1: preorder={pre1}, inorder={ino1}")
    print("  Step 1: root=3, idx=1 -> 左 size=1, 右 size=3")
    print("  Step 2: 左 pre=[9], 右 pre=[20,15,7]")
    print("  Step 3: 遞迴 -> 建出 9(葉) 和 20->15,7")
    t1 = build_from_preorder_inorder(pre1, ino1)
    r1 = tree_to_list(t1)
    print(f"  Built: {r1}")
    draw("Result:", ["    3   ", "   / \\ ", "  9  20 ", "    / \\", "   15  7"])
    assert r1 == [3, 9, 20, None, None, 15, 7]

    # --- 範例 2 ---
    #   preorder = [1, 2, 4, 5, 3]
    #   inorder  = [4, 2, 5, 1, 3]
    #   root=1, idx=3 -> 左 size=3 [4,2,5], 右 size=1 [3]
    #   左: root=2, idx=1 in [4,2,5] -> 左=[4], 右=[5]
    #   Result:     1
    #              / \
    #             2   3
    #            / \
    #           4   5
    pre2, ino2 = [1, 2, 4, 5, 3], [4, 2, 5, 1, 3]
    print(f"\n  範例 2: preorder={pre2}, inorder={ino2}")
    print("  root=1, idx=3, 左 pre=[2,4,5] -> root=2, 子=[4],[5]")
    t2 = build_from_preorder_inorder(pre2, ino2)
    r2 = tree_to_list(t2)
    print(f"  Built: {r2}")
    assert r2 == [1, 2, 3, 4, 5]

    # --- 範例 3 ---
    #   preorder = [1, 2, 3]
    #   inorder  = [3, 2, 1]
    #   root=1, idx=2, 左 size=2, 右 size=0 -> 全偏左
    #   Result: 1->2->3 (left-skewed)
    pre3, ino3 = [1, 2, 3], [3, 2, 1]
    print(f"\n  範例 3: preorder={pre3}, inorder={ino3}")
    print("  root=1, idx=2, 左 size=2, 右 size=0 -> 全偏左")
    t3 = build_from_preorder_inorder(pre3, ino3)
    r3 = tree_to_list(t3)
    print(f"  Built: {r3}")
    draw("Result:", ["1  ", "/  ", "2  ", "/  ", "3  "])
    assert r3 == [1, 2, None, 3]

# ============================================================
# Section 5: Preorder vs Inorder vs Postorder 使用時機
# ============================================================
def demo_when_to_use():
    print("\n" + "=" * 60)
    print("Section 5: 三種遍歷使用時機 Decision Tree")
    print("=" * 60)
    print("""
  你需要什麼?
  |
  +-- 「由上往下」傳遞資訊 (top-down)
  |    -> Preorder (前序)
  |    例: 序列化樹, 複製樹, Path Sum
  |    特徵: 先處理 root, 再往下走
  |
  +-- 「由下往上」收集結果 (bottom-up)
  |    -> Postorder (後序)
  |    例: 計算高度, 判斷平衡, 刪除樹
  |    特徵: 先算子樹, 再算自己
  |    *** 大部分 Tree DFS 題目用 Postorder ***
  |
  +-- 需要排序結果 (BST)
  |    -> Inorder (中序)
  |    例: BST 驗證, 第 K 小元素
  |    特徵: BST 的 Inorder = sorted order
  |
  +-- 需要「全域最佳解」(跨越左右子樹)
       -> Postorder + nonlocal 全域變數
       例: Diameter, Maximum Path Sum
       特徵: 在每個節點「順便」更新全域最佳值

  === 記憶口訣 ===
  Preorder  = 「先做事, 再下去」 (top-down)
  Postorder = 「先下去, 再做事」 (bottom-up)
  Inorder   = 「BST 專用排序器」

  === 常見題目對應表 ===
  +----------------------------+-----------+
  | 題目                        | 遍歷類型  |
  +----------------------------+-----------+
  | Max/Min Depth               | Postorder |
  | Balanced Tree               | Postorder |
  | Diameter                    | Postorder |
  | Maximum Path Sum            | Postorder |
  | Invert Tree                 | Pre/Post  |
  | Path Sum                    | Preorder  |
  | Serialize/Deserialize       | Preorder  |
  | BST Validate                | Inorder   |
  | Kth Smallest in BST         | Inorder   |
  | Flatten to Linked List      | Preorder  |
  | Build from Pre+In           | Pre+In    |
  +----------------------------+-----------+""")

    # 驗證: Inorder on BST = sorted
    print("\n  驗證: BST 的 Inorder = sorted")
    bst = build_tree([8, 4, 12, 2, 6, 10, 14])
    draw("BST:", ["      8     ", "     / \\   ", "    4  12   ", "   / \\ / \\ ", "  2  6 10 14"])
    result = inorder_recursive(bst)
    print(f"  Inorder: {result}")
    assert result == sorted(result)
    print("  Sorted! Inorder on BST always gives sorted order.")

# ============================================================
# main() - 執行所有範例
# ============================================================
def main():
    print("=" * 60)
    print(" Tree DFS 完整教學 (Complete Tree DFS Guide)")
    print(" 準備 Google / NVIDIA 面試")
    print("=" * 60)

    # Section 1: 三種遍歷
    demo_preorder()
    demo_inorder()
    demo_postorder()

    # Section 2: DFS 求值型
    demo_max_depth()
    demo_min_depth()
    demo_diameter()
    demo_balanced()

    # Section 3: DFS 路徑型
    demo_path_sum()
    demo_path_sum_ii()
    demo_max_path_sum()

    # Section 4: DFS 建構/轉換型
    demo_invert()
    demo_flatten()
    demo_build_tree()

    # Section 5: 使用時機
    demo_when_to_use()

    print("\n" + "=" * 60)
    print(" ALL EXAMPLES PASSED!")
    print("=" * 60)
    print("""
  學習路線:
  1. 先熟練三種遍歷 (Section 1) - 遞迴 + 迭代都要會
  2. 再練 Section 2 四題 - 掌握 postorder 思維
  3. Path Sum 系列 (Section 3) - 理解 backtracking
  4. Maximum Path Sum = Diameter 延伸 - Google 愛考
  5. Section 4 建構題 - 理解 preorder/inorder 的關係
  6. 面試時先問: top-down or bottom-up? -> 決定用哪種遍歷

  時間複雜度: 所有題目 O(n), 每個節點訪問一次
  空間複雜度: O(h), h=樹高 (遞迴 call stack)
             最差 O(n) 偏斜樹, 最好 O(log n) 平衡樹
""")

if __name__ == "__main__":
    main()
