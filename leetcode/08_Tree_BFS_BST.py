"""
===============================================================================
  LeetCode 08 - Tree BFS (Level-Order) & BST 完整教學
  BFS 層序遍歷 + 二元搜尋樹 (Binary Search Tree)
===============================================================================

目標讀者：準備 Google/NVIDIA 面試的初學者
教學方式：每題 3 個 step-by-step 數值追蹤範例，queue 狀態逐步展示
語言：Traditional Chinese + English terms

Sections:
  1. BFS 層序遍歷 (Level-Order Traversal)
  2. BFS 應用題
  3. BST 性質 (BST Properties)
  4. BST 利用中序特性
  5. DFS vs BFS 完整比較

所有程式碼皆可直接執行 (Runnable)。
===============================================================================
"""

from collections import deque
from typing import List, Optional


# =============================================================================
#  TreeNode 定義 & 工具函式 (Helpers)
# =============================================================================

class TreeNode:
    """二元樹節點 (Binary Tree Node)"""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def build_tree(values: list) -> Optional[TreeNode]:
    """
    從 list 建立二元樹 (level-order), None 表示空節點。
    例: [3, 9, 20, None, None, 15, 7] 建出:
          3
         / \\
        9  20
          /  \\
         15   7
    """
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_str(root: Optional[TreeNode]) -> str:
    """將樹轉為簡潔字串表示"""
    if not root:
        return "None"
    vals = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            vals.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            vals.append("null")
    # 去掉尾巴的 null
    while vals and vals[-1] == "null":
        vals.pop()
    return "[" + ", ".join(vals) + "]"


# =============================================================================
#  Section 1: BFS 層序遍歷 (Level-Order Traversal)
# =============================================================================

# -----------------------------------------------------------------------------
#  1-1. Binary Tree Level Order Traversal (LC 102)
# -----------------------------------------------------------------------------
def level_order(root: Optional[TreeNode], verbose: bool = False) -> List[List[int]]:
    """
    層序遍歷：用 queue 逐層掃過整棵樹。
    Time: O(n)  Space: O(n)

    核心觀念：
    - 用 deque 當 queue
    - 每層開始前記錄 queue 長度 = 該層節點數
    - 處理完該層所有節點，加入下一層子節點
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    level_num = 0

    while queue:
        level_size = len(queue)
        current_level = []
        if verbose:
            print(f"  Level {level_num}: queue = {[n.val for n in queue]}")

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)
        if verbose:
            print(f"    處理後: level = {current_level}, 下一層 queue = {[n.val for n in queue]}")
        level_num += 1

    return result


def demo_level_order():
    """
    三個追蹤範例 (3 step-traced examples)
    """
    print("=" * 70)
    print("1-1. Binary Tree Level Order Traversal (LC 102)")
    print("=" * 70)

    # --- Example 1 ---
    #       3
    #      / \
    #     9  20
    #       /  \
    #      15   7
    #
    # Level-Order BFS:
    # 初始: queue = [3]
    # Level 0: process 3, add children -> queue = [9, 20] -> result = [[3]]
    # Level 1: process 9 (no children), process 20 (add 15,7)
    #          -> queue = [15, 7] -> result = [[3],[9,20]]
    # Level 2: process 15, process 7 -> queue = [] -> result = [[3],[9,20],[15,7]]
    print("\n--- Example 1: [3, 9, 20, None, None, 15, 7] ---")
    print("       3")
    print("      / \\")
    print("     9  20")
    print("       /  \\")
    print("      15   7")
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    r1 = level_order(t1, verbose=True)
    print(f"  => Output: {r1}")

    # --- Example 2: [1,2,3,4,5,None,6] -> [[1],[2,3],[4,5,6]] ---
    print("\n--- Example 2: [1, 2, 3, 4, 5, None, 6] ---")
    print("       1 / 2  3 / 4  5  6")
    t2 = build_tree([1, 2, 3, 4, 5, None, 6])
    r2 = level_order(t2, verbose=True)
    print(f"  => Output: {r2}")

    # --- Example 3: single node ---
    print("\n--- Example 3: [42] (single node) ---")
    print("   42")
    t3 = build_tree([42])
    r3 = level_order(t3, verbose=True)
    print(f"  => Output: {r3}")


# -----------------------------------------------------------------------------
#  1-2. Binary Tree Zigzag Level Order Traversal (LC 103)
# -----------------------------------------------------------------------------
def zigzag_level_order(root: Optional[TreeNode], verbose: bool = False) -> List[List[int]]:
    """
    鋸齒形 (Zigzag) 層序遍歷：偶數層左->右，奇數層右->左。
    做法：普通 BFS，奇數層 reverse 即可。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    level_num = 0

    while queue:
        level_size = len(queue)
        current_level = []
        if verbose:
            direction = "左→右" if level_num % 2 == 0 else "右→左"
            print(f"  Level {level_num} ({direction}): queue = {[n.val for n in queue]}")

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if level_num % 2 == 1:
            current_level.reverse()

        result.append(current_level)
        if verbose:
            print(f"    處理後: level = {current_level}")
        level_num += 1

    return result


def demo_zigzag():
    print("\n" + "=" * 70)
    print("1-2. Binary Tree Zigzag Level Order Traversal (LC 103)")
    print("=" * 70)

    # --- Example 1: Level 0 (左→右):[3], Level 1 (右→左):[20,9], Level 2 (左→右):[15,7]
    print("\n--- Example 1: [3, 9, 20, None, None, 15, 7] ---")
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    r1 = zigzag_level_order(t1, verbose=True)
    print(f"  => Output: {r1}")

    # --- Example 2: Level 0:[1], Level 1 (右→左):[3,2], Level 2:[4,5,6]
    print("\n--- Example 2: [1, 2, 3, 4, 5, None, 6] ---")
    t2 = build_tree([1, 2, 3, 4, 5, None, 6])
    r2 = zigzag_level_order(t2, verbose=True)
    print(f"  => Output: {r2}")

    # --- Example 3: deep tree, 4 levels of zigzag ---
    print("\n--- Example 3: deep zigzag ---")
    t3 = build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7])
    r3 = zigzag_level_order(t3, verbose=True)
    print(f"  => Output: {r3}")


# -----------------------------------------------------------------------------
#  1-3. Binary Tree Right Side View (LC 199)
# -----------------------------------------------------------------------------
def right_side_view(root: Optional[TreeNode], verbose: bool = False) -> List[int]:
    """
    右視圖：BFS 每層取最後一個節點。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    level_num = 0

    while queue:
        level_size = len(queue)
        if verbose:
            print(f"  Level {level_num}: queue = {[n.val for n in queue]}, 取最後一個")

        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                result.append(node.val)
                if verbose:
                    print(f"    右視看到: {node.val}")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level_num += 1

    return result


def demo_right_side_view():
    print("\n" + "=" * 70)
    print("1-3. Binary Tree Right Side View (LC 199)")
    print("=" * 70)

    # Example 1:  [3,9,20,null,null,15,7] -> [3, 20, 7]
    print("\n--- Example 1 ---")
    print("       3         <- 看到 3")
    print("      / \\")
    print("     9  20       <- 看到 20")
    print("       /  \\")
    print("      15   7     <- 看到 7")
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    print(f"  => Output: {right_side_view(t1, verbose=True)}")

    # Example 2: [1,2,3,4] -> [1, 3, 4]  左邊的 4 被擋住, 右視只看到 1,3,4
    print("\n--- Example 2: [1,2,3,4] -> 右視: [1, 3, 4] ---")
    t2 = build_tree([1, 2, 3, 4])
    print(f"  => Output: {right_side_view(t2, verbose=True)}")

    # Example 3: [1, 2] -> [1, 2]  左子也看得到因為右邊沒東西
    print("\n--- Example 3: [1, 2] -> 右視: [1, 2] ---")
    t3 = build_tree([1, 2])
    print(f"  => Output: {right_side_view(t3, verbose=True)}")


# -----------------------------------------------------------------------------
#  1-4. Average of Levels in Binary Tree (LC 637)
# -----------------------------------------------------------------------------
def average_of_levels(root: Optional[TreeNode], verbose: bool = False) -> List[float]:
    """
    每層平均值：BFS 逐層計算 sum / count。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    level_num = 0

    while queue:
        level_size = len(queue)
        level_sum = 0
        if verbose:
            print(f"  Level {level_num}: nodes = {[n.val for n in queue]}")

        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        avg = level_sum / level_size
        result.append(avg)
        if verbose:
            print(f"    sum={level_sum}, count={level_size}, avg={avg}")
        level_num += 1

    return result


def demo_average_of_levels():
    print("\n" + "=" * 70)
    print("1-4. Average of Levels in Binary Tree (LC 637)")
    print("=" * 70)

    # Example 1: [3,9,20,null,null,15,7]
    # Level 0: avg(3) = 3.0
    # Level 1: avg(9,20) = 14.5
    # Level 2: avg(15,7) = 11.0
    print("\n--- Example 1: [3, 9, 20, None, None, 15, 7] ---")
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    print(f"  => Output: {average_of_levels(t1, verbose=True)}")

    # Example 2: [1,2,3,4,5,6,7]
    # Level 0: avg(1) = 1.0
    # Level 1: avg(2,3) = 2.5
    # Level 2: avg(4,5,6,7) = 5.5
    print("\n--- Example 2: [1, 2, 3, 4, 5, 6, 7] (complete tree) ---")
    t2 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"  => Output: {average_of_levels(t2, verbose=True)}")

    # Example 3: [10, 5, 15]
    print("\n--- Example 3: [10, 5, 15] ---")
    t3 = build_tree([10, 5, 15])
    print(f"  => Output: {average_of_levels(t3, verbose=True)}")


# =============================================================================
#  Section 2: BFS 應用題
# =============================================================================

# -----------------------------------------------------------------------------
#  2-1. Minimum Depth of Binary Tree (LC 111) - BFS approach
# -----------------------------------------------------------------------------
def min_depth_bfs(root: Optional[TreeNode], verbose: bool = False) -> int:
    """
    最小深度 (BFS)：BFS 找到第一個葉節點就回傳，保證最短。
    比 DFS 好的地方：不需要走完整棵樹，找到第一個葉子就停。
    Time: O(n) worst  Space: O(n)
    """
    if not root:
        return 0
    queue = deque([(root, 1)])  # (node, depth)

    while queue:
        node, depth = queue.popleft()
        if verbose:
            print(f"  拜訪 node={node.val}, depth={depth}, "
                  f"left={'Y' if node.left else 'N'}, right={'Y' if node.right else 'N'}")

        # 找到葉節點 -> 立即回傳 (BFS 保證最先找到的是最淺的)
        if not node.left and not node.right:
            if verbose:
                print(f"  => 葉節點! 最小深度 = {depth}")
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0  # unreachable


def min_depth_dfs(root: Optional[TreeNode]) -> int:
    """DFS 版本 (對照用)"""
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth_dfs(root.right)
    if not root.right:
        return 1 + min_depth_dfs(root.left)
    return 1 + min(min_depth_dfs(root.left), min_depth_dfs(root.right))


def demo_min_depth():
    print("\n" + "=" * 70)
    print("2-1. Minimum Depth of Binary Tree (LC 111) - BFS vs DFS")
    print("=" * 70)

    # Example 1: [3,9,20,null,null,15,7] -> min depth = 2 (node 9 is leaf at depth 2)
    print("\n--- Example 1 ---")
    print("       3        depth=1")
    print("      / \\")
    print("     9  20      depth=2  (9 是葉節點, BFS 在此停止!)")
    print("       /  \\")
    print("      15   7    depth=3")
    t1 = build_tree([3, 9, 20, None, None, 15, 7])
    r_bfs = min_depth_bfs(t1, verbose=True)
    r_dfs = min_depth_dfs(t1)
    print(f"  BFS 結果: {r_bfs}, DFS 結果: {r_dfs}")

    # Example 2: skewed tree [1,2,null,3,null,4] -> min depth = 4
    print("\n--- Example 2: skewed (偏斜樹) 1->2->3->4 ---")
    print("  1->2->3->4  唯一葉節點在 depth=4")
    t2 = build_tree([1, 2, None, 3, None, 4])
    r_bfs = min_depth_bfs(t2, verbose=True)
    print(f"  BFS 結果: {r_bfs}")

    # Example 3: balanced [1,2,3] -> min depth = 2
    print("\n--- Example 3: [1, 2, 3] ---")
    print("     1     depth=1")
    print("    / \\")
    print("   2   3   depth=2 (兩個都是葉, BFS 在 level 2 馬上找到)")
    t3 = build_tree([1, 2, 3])
    print(f"  BFS 結果: {min_depth_bfs(t3, verbose=True)}")


# -----------------------------------------------------------------------------
#  2-2. Symmetric Tree (LC 101)
# -----------------------------------------------------------------------------
def is_symmetric(root: Optional[TreeNode], verbose: bool = False) -> bool:
    """
    對稱樹：BFS 用 queue 同時比較左右鏡像位置。
    把 (left, right) 成對放入 queue，每次取一對比較。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return True
    queue = deque([(root.left, root.right)])

    while queue:
        left, right = queue.popleft()
        if verbose:
            lv = left.val if left else None
            rv = right.val if right else None
            print(f"  比較: left={lv}, right={rv}", end="")

        if not left and not right:
            if verbose:
                print(" -> 都是 None, OK")
            continue
        if not left or not right:
            if verbose:
                print(" -> 一邊 None -> 不對稱!")
            return False
        if left.val != right.val:
            if verbose:
                print(f" -> {left.val} != {right.val} -> 不對稱!")
            return False

        if verbose:
            print(f" -> {left.val} == {right.val}, OK")

        # 鏡像配對: 左的左 vs 右的右, 左的右 vs 右的左
        queue.append((left.left, right.right))
        queue.append((left.right, right.left))

    return True


def demo_symmetric():
    print("\n" + "=" * 70)
    print("2-2. Symmetric Tree (LC 101)")
    print("=" * 70)

    # Example 1: symmetric [1,2,2,3,4,4,3]
    print("\n--- Example 1: Symmetric [1, 2, 2, 3, 4, 4, 3] ---")
    print("     1 / 2  2 / 3  4  4  3  (鏡像對稱)")
    t1 = build_tree([1, 2, 2, 3, 4, 4, 3])
    print(f"  => {is_symmetric(t1, verbose=True)}")

    # Example 2: not symmetric [1,2,2,null,3,null,3] - 兩個 3 都在右邊
    print("\n--- Example 2: Not Symmetric [1, 2, 2, None, 3, None, 3] ---")
    print("     1 / 2  2 / _  3  _  3  (3 都在右邊, 不鏡像)")
    t2 = build_tree([1, 2, 2, None, 3, None, 3])
    print(f"  => {is_symmetric(t2, verbose=True)}")

    # Example 3: single node (symmetric)
    print("\n--- Example 3: single node [5] ---")
    t3 = build_tree([5])
    print(f"  => {is_symmetric(t3, verbose=True)}")


# -----------------------------------------------------------------------------
#  2-3. Cousins in Binary Tree (LC 993)
# -----------------------------------------------------------------------------
def is_cousins(root: Optional[TreeNode], x: int, y: int,
               verbose: bool = False) -> bool:
    """
    表親節點：同一層 (same depth) 但不同父節點 (different parent)。
    BFS 逐層掃，記錄 x, y 的 parent 和 depth。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return False
    # queue stores (node, parent_val)
    queue = deque([(root, None)])
    level_num = 0

    while queue:
        level_size = len(queue)
        x_parent = y_parent = None

        if verbose:
            print(f"  Level {level_num}: nodes = {[(n.val, p) for n, p in queue]}")

        for _ in range(level_size):
            node, parent = queue.popleft()
            if node.val == x:
                x_parent = parent
            if node.val == y:
                y_parent = parent
            if node.left:
                queue.append((node.left, node.val))
            if node.right:
                queue.append((node.right, node.val))

        # 都在這層找到了
        if x_parent is not None and y_parent is not None:
            result = x_parent != y_parent
            if verbose:
                print(f"    找到! x={x} parent={x_parent}, y={y} parent={y_parent}")
                print(f"    同層且不同父? {result}")
            return result
        # 只找到一個 -> 不同層 -> 不是 cousins
        if x_parent is not None or y_parent is not None:
            if verbose:
                print(f"    只找到一個在這層 -> 不同層 -> False")
            return False

        level_num += 1

    return False


def demo_cousins():
    print("\n" + "=" * 70)
    print("2-3. Cousins in Binary Tree (LC 993)")
    print("=" * 70)

    # Example 1: 4 (parent=2) 和 5 (parent=3), 同層不同父 -> cousins!
    print("\n--- Example 1: [1,2,3,4,null,null,5], x=4, y=5 ---")
    print("  1 / 2  3 / 4  _  _  5   (4 parent=2, 5 parent=3 -> cousins)")
    t1 = build_tree([1, 2, 3, 4, None, None, 5])
    print(f"  => {is_cousins(t1, 4, 5, verbose=True)}")

    # Example 2: 4 和 5 同父 (parent=2) -> siblings, NOT cousins
    print("\n--- Example 2: [1,2,3,4,5], x=4, y=5 (同父=siblings) ---")
    t2 = build_tree([1, 2, 3, 4, 5])
    print(f"  => {is_cousins(t2, 4, 5, verbose=True)}")

    # Example 3: 2 和 3 同父 (parent=1) -> siblings
    print("\n--- Example 3: [1,2,3], x=2, y=3 (同父=siblings) ---")
    t3 = build_tree([1, 2, 3])
    print(f"  => {is_cousins(t3, 2, 3, verbose=True)}")


# -----------------------------------------------------------------------------
#  2-4. Populating Next Right Pointers in Each Node (LC 116)
# -----------------------------------------------------------------------------
class NodeWithNext:
    """帶 next 指標的節點"""
    def __init__(self, val: int = 0, left=None, right=None, nxt=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = nxt


def build_tree_with_next(values: list) -> Optional[NodeWithNext]:
    """建立帶 next 指標的樹 (next 初始為 None)"""
    if not values or values[0] is None:
        return None
    root = NodeWithNext(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = NodeWithNext(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = NodeWithNext(values[i])
            queue.append(node.right)
        i += 1
    return root


def connect_next_right(root: Optional[NodeWithNext],
                       verbose: bool = False) -> Optional[NodeWithNext]:
    """
    BFS 逐層連接 next 指標：同層每個節點 next 指向右邊。
    Time: O(n)  Space: O(n)
    """
    if not root:
        return None
    queue = deque([root])
    level_num = 0

    while queue:
        level_size = len(queue)
        if verbose:
            print(f"  Level {level_num}: nodes = {[n.val for n in queue]}")

        for i in range(level_size):
            node = queue.popleft()
            # 不是該層最後一個 -> next 指向 queue 前端 (同層下一個)
            if i < level_size - 1:
                node.next = queue[0]
                if verbose:
                    print(f"    {node.val}.next = {queue[0].val}")
            else:
                node.next = None
                if verbose:
                    print(f"    {node.val}.next = None (層末)")

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level_num += 1

    return root


def print_next_pointers(root: Optional[NodeWithNext]):
    """印出每層的 next 鏈"""
    node = root
    while node:
        curr = node
        level_str = ""
        while curr:
            level_str += f"{curr.val} -> "
            curr = curr.next
        level_str += "None"
        print(f"    {level_str}")
        node = node.left  # 往下一層


def demo_connect_next():
    print("\n" + "=" * 70)
    print("2-4. Populating Next Right Pointers (LC 116)")
    print("=" * 70)

    # Example 1: perfect binary tree, 每層 next 鏈: 1->None, 2->3->None, 4->5->6->7->None
    print("\n--- Example 1: [1,2,3,4,5,6,7] (perfect binary tree) ---")
    t1 = build_tree_with_next([1, 2, 3, 4, 5, 6, 7])
    connect_next_right(t1, verbose=True)
    print("  Next pointer 鏈:")
    print_next_pointers(t1)

    # Example 2: [1,2,3]
    print("\n--- Example 2: [1,2,3] ---")
    t2 = build_tree_with_next([1, 2, 3])
    connect_next_right(t2, verbose=True)
    print("  Next pointer 鏈:")
    print_next_pointers(t2)

    # Example 3: single node
    print("\n--- Example 3: [10] ---")
    t3 = build_tree_with_next([10])
    connect_next_right(t3, verbose=True)
    print("  Next pointer 鏈:")
    print_next_pointers(t3)


# =============================================================================
#  Section 3: BST 性質 (BST Properties)
# =============================================================================

# -----------------------------------------------------------------------------
#  3-1. Validate BST (LC 98)
# -----------------------------------------------------------------------------
def is_valid_bst(root: Optional[TreeNode], verbose: bool = False) -> bool:
    """
    驗證 BST：每個節點必須在 (low, high) 範圍內。
    左子樹所有值 < 當前節點, 右子樹所有值 > 當前節點。
    Time: O(n)  Space: O(h)

    關鍵：不能只比較 parent-child，要用 range 傳遞!
    """
    def helper(node, low, high, depth=0):
        if not node:
            return True
        indent = "    " * depth
        if verbose:
            lo_str = "-inf" if low == float('-inf') else str(low)
            hi_str = "+inf" if high == float('inf') else str(high)
            print(f"  {indent}node={node.val}, valid range=({lo_str}, {hi_str})", end="")

        if node.val <= low or node.val >= high:
            if verbose:
                print(f" -> INVALID! {node.val} 不在範圍內")
            return False
        if verbose:
            print(f" -> OK")

        return (helper(node.left, low, node.val, depth + 1) and
                helper(node.right, node.val, high, depth + 1))

    return helper(root, float('-inf'), float('inf'))


def demo_validate_bst():
    print("\n" + "=" * 70)
    print("3-1. Validate BST (LC 98)")
    print("=" * 70)

    # Example 1: valid BST [5,3,7,1,4,6,8]
    print("\n--- Example 1: Valid BST [5,3,7,1,4,6,8] ---")
    t1 = build_tree([5, 3, 7, 1, 4, 6, 8])
    print(f"  => {is_valid_bst(t1, verbose=True)}")

    # Example 2: invalid! 4 在 5 的右子樹但 4 < 5
    print("\n--- Example 2: Invalid BST [5,1,6,null,null,4,7] ---")
    print("  5 的右子樹有 4, 但 4 < 5 -> 違反 BST!")
    t2 = build_tree([5, 1, 6, None, None, 4, 7])
    print(f"  => {is_valid_bst(t2, verbose=True)}")

    # Example 3: [2, 2, 2] -> invalid (BST 要求嚴格不等式, 不允許重複)
    print("\n--- Example 3: [2, 2, 2] (重複值 -> invalid) ---")
    t3 = build_tree([2, 2, 2])
    print(f"  => {is_valid_bst(t3, verbose=True)}")


# -----------------------------------------------------------------------------
#  3-2. Search in BST (LC 700)
# -----------------------------------------------------------------------------
def search_bst(root: Optional[TreeNode], target: int,
               verbose: bool = False) -> Optional[TreeNode]:
    """
    BST 搜尋：利用 BST 性質每次排除一半。
    - target < node.val -> 往左
    - target > node.val -> 往右
    Time: O(log n) average, O(n) worst (skewed)
    Space: O(1) iterative
    """
    step = 0
    node = root
    while node:
        step += 1
        if verbose:
            if target < node.val:
                direction = "往左 (target < node)"
            elif target > node.val:
                direction = "往右 (target > node)"
            else:
                direction = "找到了!"
            print(f"  Step {step}: node={node.val}, target={target} -> {direction}")

        if target == node.val:
            return node
        elif target < node.val:
            node = node.left
        else:
            node = node.right

    if verbose:
        print(f"  走到 None, 沒找到 target={target}")
    return None


def demo_search_bst():
    print("\n" + "=" * 70)
    print("3-2. Search in BST (LC 700)")
    print("=" * 70)
    print("  BST 搜尋就像二分搜尋，每步排除一半 -> O(log n)")

    # BST: 8 / 3 10 / 1 6 _ 14 / _ _ 4 7
    tree_vals = [8, 3, 10, 1, 6, None, 14, None, None, 4, 7]
    t = build_tree(tree_vals)
    print("\n  BST: [8, 3, 10, 1, 6, _, 14, _, _, 4, 7]")

    # Example 1: search 4
    print("\n--- Example 1: search 4 ---")
    r1 = search_bst(t, 4, verbose=True)
    print(f"  => Found: {r1.val if r1 else None}")

    # Example 2: search 14
    print("\n--- Example 2: search 14 ---")
    r2 = search_bst(t, 14, verbose=True)
    print(f"  => Found: {r2.val if r2 else None}")

    # Example 3: search 5 (not exist)
    print("\n--- Example 3: search 5 (不存在) ---")
    r3 = search_bst(t, 5, verbose=True)
    print(f"  => Found: {r3.val if r3 else None}")


# -----------------------------------------------------------------------------
#  3-3. Insert into BST (LC 701)
# -----------------------------------------------------------------------------
def insert_bst(root: Optional[TreeNode], val: int,
               verbose: bool = False) -> TreeNode:
    """
    BST 插入：找到空位就插。新節點一定是葉節點。
    Time: O(log n) avg  Space: O(1) iterative
    """
    new_node = TreeNode(val)
    if not root:
        if verbose:
            print(f"  空樹, 新節點 {val} 成為 root")
        return new_node

    curr = root
    step = 0
    while True:
        step += 1
        if val < curr.val:
            if verbose:
                print(f"  Step {step}: {val} < {curr.val}, 往左")
            if not curr.left:
                curr.left = new_node
                if verbose:
                    print(f"  Step {step + 1}: 左子為空, 插入 {val}!")
                break
            curr = curr.left
        else:
            if verbose:
                print(f"  Step {step}: {val} > {curr.val}, 往右")
            if not curr.right:
                curr.right = new_node
                if verbose:
                    print(f"  Step {step + 1}: 右子為空, 插入 {val}!")
                break
            curr = curr.right

    return root


def demo_insert_bst():
    print("\n" + "=" * 70)
    print("3-3. Insert into BST (LC 701)")
    print("=" * 70)

    # Example 1: insert 5 into [4,2,7,1,3] -> 5 成為 3 的右子
    print("\n--- Example 1: insert 5 into [4,2,7,1,3] ---")
    t1 = build_tree([4, 2, 7, 1, 3])
    insert_bst(t1, 5, verbose=True)
    print(f"  樹: {tree_to_str(t1)}")

    # Example 2: insert 0 into [4,2,7,1,3]
    print("\n--- Example 2: insert 0 into [4,2,7,1,3] ---")
    t2 = build_tree([4, 2, 7, 1, 3])
    insert_bst(t2, 0, verbose=True)
    print(f"  樹: {tree_to_str(t2)}")

    # Example 3: insert into empty tree
    print("\n--- Example 3: insert 10 into empty tree ---")
    t3 = insert_bst(None, 10, verbose=True)
    print(f"  樹: {tree_to_str(t3)}")


# -----------------------------------------------------------------------------
#  3-4. Delete Node in BST (LC 450)
# -----------------------------------------------------------------------------
def delete_bst(root: Optional[TreeNode], key: int,
               verbose: bool = False) -> Optional[TreeNode]:
    """
    BST 刪除：三種情況
    Case 1: 葉節點 (leaf) -> 直接刪
    Case 2: 只有一個子節點 -> 用子節點取代
    Case 3: 有兩個子節點 -> 用右子樹最小值 (inorder successor) 取代

    Time: O(log n) avg  Space: O(h)
    """
    if not root:
        if verbose:
            print(f"  走到 None, key={key} 不存在")
        return None

    if key < root.val:
        if verbose:
            print(f"  {key} < {root.val}, 往左找")
        root.left = delete_bst(root.left, key, verbose)
    elif key > root.val:
        if verbose:
            print(f"  {key} > {root.val}, 往右找")
        root.right = delete_bst(root.right, key, verbose)
    else:
        # 找到要刪的節點
        if verbose:
            has_left = root.left is not None
            has_right = root.right is not None
            if not has_left and not has_right:
                case = "Case 1: 葉節點, 直接刪"
            elif not has_left or not has_right:
                case = "Case 2: 一個子節點, 用子取代"
            else:
                case = "Case 3: 兩個子節點, 找 inorder successor"
            print(f"  找到 node={root.val}! {case}")

        # Case 1 & 2: 沒有左子 or 沒有右子
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Case 3: 找右子樹最小值 (inorder successor)
        successor = root.right
        while successor.left:
            successor = successor.left
        if verbose:
            print(f"  Inorder successor = {successor.val}, 用它取代 {root.val}")
        root.val = successor.val
        root.right = delete_bst(root.right, successor.val, verbose)

    return root


def demo_delete_bst():
    print("\n" + "=" * 70)
    print("3-4. Delete Node in BST (LC 450)")
    print("=" * 70)

    # BST: [5,3,6,2,4,null,7] 用於以下三個範例
    # Example 1: delete leaf node 2
    print("\n--- Example 1: delete 2 (Case 1: 葉節點) ---")
    t1 = build_tree([5, 3, 6, 2, 4, None, 7])
    print(f"  Before: {tree_to_str(t1)}")
    t1 = delete_bst(t1, 2, verbose=True)
    print(f"  After:  {tree_to_str(t1)}")

    # Example 2: delete node 6 with one child
    print("\n--- Example 2: delete 6 (Case 2: 一個子節點 7) ---")
    t2 = build_tree([5, 3, 6, 2, 4, None, 7])
    print(f"  Before: {tree_to_str(t2)}")
    t2 = delete_bst(t2, 6, verbose=True)
    print(f"  After:  {tree_to_str(t2)}")

    # Example 3: delete node 3 with two children
    print("\n--- Example 3: delete 3 (Case 3: 兩個子 2, 4) ---")
    print("  Inorder successor of 3 = 4 (右子樹最小值)")
    t3 = build_tree([5, 3, 6, 2, 4, None, 7])
    print(f"  Before: {tree_to_str(t3)}")
    t3 = delete_bst(t3, 3, verbose=True)
    print(f"  After:  {tree_to_str(t3)}")


# =============================================================================
#  Section 4: BST 利用中序特性
# =============================================================================

# -----------------------------------------------------------------------------
#  4-1. Kth Smallest Element in BST (LC 230)
# -----------------------------------------------------------------------------
def kth_smallest(root: Optional[TreeNode], k: int,
                 verbose: bool = False) -> int:
    """
    BST 中序遍歷 = 遞增排序! 第 k 個就是答案。
    用 iterative inorder (stack) 避免走完整棵樹。
    Time: O(H + k)  Space: O(H)
    """
    stack = []
    node = root
    count = 0

    while stack or node:
        # 一路往左走到底
        while node:
            stack.append(node)
            if verbose:
                print(f"  push {node.val} to stack")
            node = node.left

        node = stack.pop()
        count += 1
        if verbose:
            print(f"  pop {node.val}, count={count}" +
                  (" <- 找到!" if count == k else ""))

        if count == k:
            return node.val

        node = node.right

    return -1  # unreachable if k is valid


def demo_kth_smallest():
    print("\n" + "=" * 70)
    print("4-1. Kth Smallest Element in BST (LC 230)")
    print("=" * 70)
    print("  BST 中序遍歷 (Inorder) = 遞增排序")

    # BST: [5,3,6,2,4,null,null,1], Inorder: 1,2,3,4,5,6
    t = build_tree([5, 3, 6, 2, 4, None, None, 1])
    print("\n  BST Inorder: 1, 2, 3, 4, 5, 6")

    # Example 1: k=1 -> 1
    print(f"\n--- Example 1: k=1 ---")
    print(f"  => {kth_smallest(t, 1, verbose=True)}")

    # Example 2: k=3 -> 3
    print(f"\n--- Example 2: k=3 ---")
    print(f"  => {kth_smallest(t, 3, verbose=True)}")

    # Example 3: k=5 -> 5
    print(f"\n--- Example 3: k=5 ---")
    print(f"  => {kth_smallest(t, 5, verbose=True)}")


# -----------------------------------------------------------------------------
#  4-2. Convert BST to Sorted Doubly Linked List (LC 426)
# -----------------------------------------------------------------------------
def bst_to_dll(root: Optional[TreeNode],
               verbose: bool = False) -> Optional[TreeNode]:
    """
    BST -> 排序雙向環狀鏈結串列 (Sorted Circular Doubly Linked List)
    用 inorder 遍歷，left = prev, right = next。
    最後首尾相連形成環。
    Time: O(n)  Space: O(h)
    """
    if not root:
        return None

    first = None  # 最小節點 (head)
    last = None   # 前一個拜訪的節點

    def inorder(node):
        nonlocal first, last
        if not node:
            return

        inorder(node.left)

        if verbose:
            print(f"  拜訪 node={node.val}, last={'None' if not last else last.val}")

        if last:
            # 連接 last <-> node
            last.right = node
            node.left = last
            if verbose:
                print(f"    連接: {last.val} <-> {node.val}")
        else:
            first = node
            if verbose:
                print(f"    first = {node.val}")

        last = node

        inorder(node.right)

    inorder(root)

    # 首尾相連形成環
    if first and last:
        first.left = last
        last.right = first
        if verbose:
            print(f"  環狀連接: {last.val} <-> {first.val} (tail <-> head)")

    return first


def print_dll(head: Optional[TreeNode], max_print: int = 10):
    """印出雙向環狀鏈結串列"""
    if not head:
        print("    (empty)")
        return
    result = []
    node = head
    for _ in range(max_print):
        result.append(str(node.val))
        node = node.right
        if node == head:
            break
    print(f"    Forward:  {' <-> '.join(result)} <-> (back to {head.val})")

    result_rev = []
    node = head.left  # tail
    for _ in range(max_print):
        result_rev.append(str(node.val))
        node = node.left
        if node == head.left:
            break
    print(f"    Backward: {' <-> '.join(result_rev)} <-> (back to {head.left.val})")


def demo_bst_to_dll():
    print("\n" + "=" * 70)
    print("4-2. Convert BST to Sorted Doubly Linked List (LC 426)")
    print("=" * 70)

    # Example 1: [4,2,5,1,3] -> 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> (back to 1)
    print("\n--- Example 1: [4, 2, 5, 1, 3] ---")
    t1 = build_tree([4, 2, 5, 1, 3])
    head1 = bst_to_dll(t1, verbose=True)
    print_dll(head1)

    # Example 2: [2, 1, 3]
    print("\n--- Example 2: [2, 1, 3] ---")
    t2 = build_tree([2, 1, 3])
    head2 = bst_to_dll(t2, verbose=True)
    print_dll(head2)

    # Example 3: single node [7]
    print("\n--- Example 3: [7] (single node) ---")
    t3 = build_tree([7])
    head3 = bst_to_dll(t3, verbose=True)
    print_dll(head3)


# -----------------------------------------------------------------------------
#  4-3. Lowest Common Ancestor of BST (LC 235)
# -----------------------------------------------------------------------------
def lca_bst(root: Optional[TreeNode], p: int, q: int,
            verbose: bool = False) -> Optional[int]:
    """
    BST 的 LCA：利用 BST 性質，不需要存路徑!
    - p, q 都 < node -> LCA 在左邊
    - p, q 都 > node -> LCA 在右邊
    - 否則 node 就是 LCA (分叉點)
    Time: O(log n) avg  Space: O(1)
    """
    node = root
    step = 0
    while node:
        step += 1
        if verbose:
            print(f"  Step {step}: node={node.val}, p={p}, q={q}", end="")

        if p < node.val and q < node.val:
            if verbose:
                print(f" -> 都 < {node.val}, 往左")
            node = node.left
        elif p > node.val and q > node.val:
            if verbose:
                print(f" -> 都 > {node.val}, 往右")
            node = node.right
        else:
            if verbose:
                print(f" -> 分叉! {p} 和 {q} 在 {node.val} 的兩側 (或等於)")
                print(f"  => LCA = {node.val}")
            return node.val

    return None


def demo_lca_bst():
    print("\n" + "=" * 70)
    print("4-3. Lowest Common Ancestor of BST (LC 235)")
    print("=" * 70)
    print("  關鍵：利用 BST 排序性質，只需 O(log n)!")

    # BST: [6,2,8,0,4,7,9,null,null,3,5]
    t = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    print("\n  BST: [6, 2, 8, 0, 4, 7, 9, _, _, 3, 5]")

    # Example 1: LCA(2, 8) = 6
    print("\n--- Example 1: LCA(2, 8) ---")
    print(f"  => {lca_bst(t, 2, 8, verbose=True)}")

    # Example 2: LCA(2, 4) = 2 (p is ancestor of q)
    print("\n--- Example 2: LCA(2, 4) ---")
    print(f"  => {lca_bst(t, 2, 4, verbose=True)}")

    # Example 3: LCA(3, 5) = 4
    print("\n--- Example 3: LCA(3, 5) ---")
    print(f"  => {lca_bst(t, 3, 5, verbose=True)}")


# =============================================================================
#  Section 5: DFS vs BFS 完整比較
# =============================================================================

def demo_dfs_vs_bfs():
    print("\n" + "=" * 70)
    print("Section 5: DFS vs BFS 完整比較")
    print("=" * 70)

    print("""
    +-----------------+----------------------------+----------------------------+
    |                 |     DFS (深度優先)          |     BFS (廣度優先)          |
    +-----------------+----------------------------+----------------------------+
    | 資料結構         | Stack (或遞迴 call stack)  | Queue (deque)              |
    | 走法             | 先走到底再回頭             | 一層一層往外擴展            |
    | Space 複雜度     | O(h) h=樹高               | O(w) w=最寬的那層           |
    |                 | balanced: O(log n)         | worst: O(n) (完全二元樹    |
    |                 | skewed: O(n)               | 最後一層有 n/2 個節點)     |
    +-----------------+----------------------------+----------------------------+
    | 適合問題         | - 路徑問題 (path sum)      | - 最短路徑 / 最小深度       |
    |                 | - 回溯法 (backtracking)    | - 逐層處理 (level-order)   |
    |                 | - 樹的形狀判斷             | - 找最近的節點              |
    |                 | - BST 中序遍歷             | - 圖的最短路 (unweighted)  |
    +-----------------+----------------------------+----------------------------+

    DFS 好用的場景 (Stack / Recursion):
    ┌──────────────────────────────────────────────────────────────────┐
    │ 1. Path Sum (LC 112/113) - 需要追蹤根到葉的路徑                 │
    │ 2. Validate BST (LC 98)  - 用 range [min, max] 遞迴傳遞        │
    │ 3. Serialize/Deserialize - preorder 容易重建樹                   │
    │ 4. Tree DP - 子問題由子樹結果組合 (diameter, max path sum)      │
    │ 5. Backtracking - 需要回溯狀態 (N-Queens, permutations)         │
    └──────────────────────────────────────────────────────────────────┘

    BFS 好用的場景 (Queue):
    ┌──────────────────────────────────────────────────────────────────┐
    │ 1. Level Order (LC 102)  - 天生就是一層一層處理                  │
    │ 2. Min Depth (LC 111)    - 第一個葉子就是答案，不需走完全部      │
    │ 3. Right Side View (199) - 每層最右邊                           │
    │ 4. Shortest Path in Graph - unweighted graph 用 BFS 找最短路    │
    │ 5. Word Ladder (LC 127)  - 找最短轉換序列                       │
    └──────────────────────────────────────────────────────────────────┘
    """)

    # --- 實際比較 ---
    print("  --- 實際比較: Min Depth (偏斜樹 1->2->3->4->5, 右邊 3 是葉) ---")
    print("  BFS: 掃到 Level 1 就找到葉節點 3, 看 3 個節點就停")
    print("  DFS: 先走完 1->2->4->5, 再回溯找 3, 看 5 個節點")
    print("  結論: 找最短/最淺 -> BFS 更有效率!")
    print()
    print("  --- 實際比較: Path Sum ---")
    print("  DFS: 沿路走到底加總, 回溯減掉, O(h) 空間")
    print("  BFS: 每節點存路徑和, O(w) 空間且更複雜")
    print("  結論: 路徑追蹤問題 -> DFS 更自然!")

    print()
    print("  === 口訣 ===")
    print('  "要找最短用 BFS, 要找路徑用 DFS"')
    print('  "一層一層選 BFS, 走到底再回選 DFS"')


# =============================================================================
#  Main - 執行所有範例
# =============================================================================

def main():
    print("=" * 70)
    print("  LeetCode 08 - Tree BFS & BST 完整教學")
    print("  所有範例皆附 step-by-step 追蹤")
    print("=" * 70)

    # --- Section 1: BFS 層序遍歷 ---
    print("\n\n" + "#" * 70)
    print("#  Section 1: BFS 層序遍歷 (Level-Order Traversal)")
    print("#" * 70)
    demo_level_order()
    demo_zigzag()
    demo_right_side_view()
    demo_average_of_levels()

    # --- Section 2: BFS 應用題 ---
    print("\n\n" + "#" * 70)
    print("#  Section 2: BFS 應用題")
    print("#" * 70)
    demo_min_depth()
    demo_symmetric()
    demo_cousins()
    demo_connect_next()

    # --- Section 3: BST 性質 ---
    print("\n\n" + "#" * 70)
    print("#  Section 3: BST 性質 (BST Properties)")
    print("#" * 70)
    demo_validate_bst()
    demo_search_bst()
    demo_insert_bst()
    demo_delete_bst()

    # --- Section 4: BST 利用中序特性 ---
    print("\n\n" + "#" * 70)
    print("#  Section 4: BST 利用中序特性 (Inorder Properties)")
    print("#" * 70)
    demo_kth_smallest()
    demo_bst_to_dll()
    demo_lca_bst()

    # --- Section 5: DFS vs BFS 比較 ---
    print("\n\n" + "#" * 70)
    print("#  Section 5: DFS vs BFS 完整比較")
    print("#" * 70)
    demo_dfs_vs_bfs()

    print("\n\n" + "=" * 70)
    print("  教學結束! 重點複習:")
    print("  1. BFS 核心: queue + 每層 for loop (len(queue) 次)")
    print("  2. BST 核心: 左 < 根 < 右, 中序遍歷 = 排序")
    print("  3. BST 搜尋/插入/刪除: O(log n), 利用排序性質每次排除一半")
    print("  4. 找最短 -> BFS, 找路徑 -> DFS")
    print("=" * 70)


if __name__ == "__main__":
    main()
