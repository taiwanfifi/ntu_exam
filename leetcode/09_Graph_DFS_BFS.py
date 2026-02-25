"""
09_Graph_DFS_BFS.py — Graph 基礎：DFS / BFS / Connected Components
=======================================================================
LeetCode 面試準備教材 | Google / NVIDIA 導向
適用對象：初學者 | 每題附 step-by-step 數值追蹤

執行方式：python 09_Graph_DFS_BFS.py
"""

from collections import deque, defaultdict
from typing import List, Optional, Dict, Set, Tuple
import copy

# ============================================================
# Section 0: 圖的基礎表示法 (Graph Representations)
# ============================================================

def section0_graph_representations(verbose: bool = True) -> None:
    """
    三種圖的表示法：
    1. Adjacency List（鄰接表）— 最常用！面試 90% 都用這個
    2. Adjacency Matrix（鄰接矩陣）— 稠密圖 or 需要 O(1) 查邊
    3. Edge List（邊列表）— 輸入格式常見，通常需轉換

    有向 (Directed) vs 無向 (Undirected)：
    - 無向圖：邊 (u,v) 表示 u→v 且 v→u，兩邊都要加
    - 有向圖：邊 (u,v) 只表示 u→v

    時間 / 空間複雜度比較：
    ┌──────────────┬─────────────┬──────────────┬────────────┐
    │ 操作          │ Adj List    │ Adj Matrix   │ Edge List  │
    ├──────────────┼─────────────┼──────────────┼────────────┤
    │ 空間          │ O(V + E)    │ O(V^2)       │ O(E)       │
    │ 加邊          │ O(1)        │ O(1)         │ O(1)       │
    │ 查邊 (u,v)?   │ O(degree)   │ O(1)         │ O(E)       │
    │ 列出鄰居      │ O(degree)   │ O(V)         │ O(E)       │
    └──────────────┴─────────────┴──────────────┴────────────┘
    """
    if not verbose:
        return

    print("=" * 65)
    print("Section 0: 圖的基礎表示法 (Graph Representations)")
    print("=" * 65)

    # ── Example 1: 無向圖 (Undirected) ──
    # Graph:  0 --- 1
    #         |     |
    #         2 --- 3
    print("\n--- Example 1: 無向圖 4 個節點 ---")
    print("# Graph:  0 --- 1")
    print("#         |     |")
    print("#         2 --- 3")
    print("# edges = [[0,1], [0,2], [1,3], [2,3]]")

    edges_1 = [[0, 1], [0, 2], [1, 3], [2, 3]]
    n1 = 4

    # (a) Edge List → Adjacency List
    adj_list_1: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges_1:
        adj_list_1[u].append(v)  # u → v
        adj_list_1[v].append(u)  # v → u（無向，雙邊都加）
    print(f"\nAdjacency List (dict):")
    for node in range(n1):
        print(f"  {node}: {adj_list_1[node]}")
    # 0: [1, 2]
    # 1: [0, 3]
    # 2: [0, 3]
    # 3: [1, 2]

    # (b) Edge List → Adjacency Matrix
    adj_matrix_1 = [[0] * n1 for _ in range(n1)]
    for u, v in edges_1:
        adj_matrix_1[u][v] = 1
        adj_matrix_1[v][u] = 1  # 無向
    print(f"\nAdjacency Matrix:")
    print(f"    0  1  2  3")
    for i in range(n1):
        row_str = "  ".join(str(x) for x in adj_matrix_1[i])
        print(f"  {i}: {row_str}")
    # 0: 0  1  1  0
    # 1: 1  0  0  1
    # 2: 1  0  0  1
    # 3: 0  1  1  0

    # (c) Adjacency Matrix → Edge List
    edges_from_matrix = []
    for i in range(n1):
        for j in range(i + 1, n1):  # j > i 避免重複
            if adj_matrix_1[i][j] == 1:
                edges_from_matrix.append([i, j])
    print(f"\nMatrix → Edge List: {edges_from_matrix}")

    # ── Example 2: 有向圖 (Directed) ──
    # Graph:  0 → 1
    #         ↓   ↓
    #         2 → 3
    print("\n--- Example 2: 有向圖 4 個節點 ---")
    print("# Graph:  0 → 1")
    print("#         ↓   ↓")
    print("#         2 → 3")
    print("# edges = [[0,1], [0,2], [1,3], [2,3]]")

    edges_2 = [[0, 1], [0, 2], [1, 3], [2, 3]]
    adj_list_2: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges_2:
        adj_list_2[u].append(v)  # 有向：只加 u → v
    print(f"\nAdjacency List (directed):")
    for node in range(n1):
        print(f"  {node}: {adj_list_2[node]}")
    # 0: [1, 2]   ← 0 可以到 1 和 2
    # 1: [3]       ← 1 只能到 3
    # 2: [3]       ← 2 只能到 3
    # 3: []        ← 3 沒有出邊

    adj_matrix_2 = [[0] * n1 for _ in range(n1)]
    for u, v in edges_2:
        adj_matrix_2[u][v] = 1  # 有向：只標一個方向
    print(f"\nAdjacency Matrix (directed):")
    print(f"    0  1  2  3")
    for i in range(n1):
        row_str = "  ".join(str(x) for x in adj_matrix_2[i])
        print(f"  {i}: {row_str}")

    # ── Example 3: 帶權重的圖 (Weighted) ──
    # Graph:  0 --5-- 1
    #         |       |
    #        (3)     (2)
    #         |       |
    #         2 --4-- 3
    print("\n--- Example 3: 帶權重無向圖 ---")
    print("# Graph:  0 --5-- 1")
    print("#         |       |")
    print("#        (3)     (2)")
    print("#         |       |")
    print("#         2 --4-- 3")
    print("# edges = [[0,1,5], [0,2,3], [1,3,2], [2,3,4]]")

    weighted_edges = [[0, 1, 5], [0, 2, 3], [1, 3, 2], [2, 3, 4]]
    adj_weighted: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for u, v, w in weighted_edges:
        adj_weighted[u].append((v, w))
        adj_weighted[v].append((u, w))
    print(f"\nWeighted Adjacency List:")
    for node in range(n1):
        print(f"  {node}: {adj_weighted[node]}")
    # 0: [(1, 5), (2, 3)]
    # 1: [(0, 5), (3, 2)]
    # 2: [(0, 3), (3, 4)]
    # 3: [(1, 2), (2, 4)]

    print("\n" + "-" * 40)
    print("重點整理：")
    print("  1. 面試中 90% 用 Adjacency List（dict of lists）")
    print("  2. 無向圖：每條邊加兩次（u→v, v→u）")
    print("  3. 有向圖：每條邊只加一次（u→v）")
    print("  4. 帶權重：list 裡存 (neighbor, weight) tuple")


# ============================================================
# Section 1: Graph DFS
# ============================================================

# ---- 1a. Number of Islands (DFS version) ----
# LeetCode 200: https://leetcode.com/problems/number-of-islands/

def num_islands_dfs(grid: List[List[str]], verbose: bool = False) -> int:
    """
    給一個 m x n 的 grid，'1' 是陸地，'0' 是水。
    找有幾個島嶼（上下左右相連的 '1' 算同一島）。

    思路：遍歷每個格子，遇到 '1' 就 DFS 把整座島標記為 visited，count += 1
    Time: O(m * n)  |  Space: O(m * n) worst case for recursion stack
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0
    step = [0]

    def dfs(r: int, c: int) -> None:
        # 超出邊界 or 是水 → 停
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '#'  # 標記為已訪問（改成 '#' 避免重複）
        step[0] += 1
        if verbose:
            print(f"    Step {step[0]}: DFS visit ({r},{c}), mark as '#'")
        # 四個方向
        dfs(r + 1, c)  # 下
        dfs(r - 1, c)  # 上
        dfs(r, c + 1)  # 右
        dfs(r, c - 1)  # 左

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                if verbose:
                    print(f"  Found island #{count} starting at ({r},{c})")
                step[0] = 0
                dfs(r, c)

    return count


def demo_num_islands_dfs(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("1a. Number of Islands — DFS (LeetCode 200)")
    print("=" * 65)

    # Example 1
    grid1 = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1'],
    ]
    print("\nExample 1:")
    print("  Grid:")
    for row in grid1:
        print("   ", row)
    # 初始: 3 座島
    # 島1: (0,0)(0,1)(1,0)(1,1)
    # 島2: (2,2)
    # 島3: (3,3)(3,4)
    g1 = [row[:] for row in grid1]
    result1 = num_islands_dfs(g1, verbose)
    print(f"  Answer: {result1}")  # 3
    assert result1 == 3

    # Example 2
    grid2 = [
        ['1', '1', '1'],
        ['0', '1', '0'],
        ['1', '1', '1'],
    ]
    print("\nExample 2:")
    print("  Grid:")
    for row in grid2:
        print("   ", row)
    g2 = [row[:] for row in grid2]
    result2 = num_islands_dfs(g2, verbose)
    print(f"  Answer: {result2}")  # 1 (全部相連)
    assert result2 == 1

    # Example 3: all water
    grid3 = [
        ['0', '0'],
        ['0', '0'],
    ]
    print("\nExample 3:")
    print("  Grid (all water):")
    for row in grid3:
        print("   ", row)
    g3 = [row[:] for row in grid3]
    result3 = num_islands_dfs(g3, verbose)
    print(f"  Answer: {result3}")  # 0
    assert result3 == 0


# ---- 1b. Clone Graph ----
# LeetCode 133: https://leetcode.com/problems/clone-graph/

class GraphNode:
    """Graph node for Clone Graph problem."""
    def __init__(self, val: int = 0, neighbors: List['GraphNode'] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


def clone_graph(node: Optional[GraphNode], verbose: bool = False) -> Optional[GraphNode]:
    """
    深複製一個無向圖。

    思路：DFS + HashMap（old node → new node）
    - 遇到已複製的節點 → 直接從 map 取
    - 遇到新節點 → 建立 clone，DFS 複製所有鄰居

    Time: O(V + E)  |  Space: O(V)
    """
    if not node:
        return None

    old_to_new: Dict[GraphNode, GraphNode] = {}
    step = [0]

    def dfs(n: GraphNode) -> GraphNode:
        if n in old_to_new:
            if verbose:
                print(f"    Node {n.val} already cloned, return from map")
            return old_to_new[n]

        step[0] += 1
        clone = GraphNode(n.val)
        old_to_new[n] = clone
        if verbose:
            nbr_vals = [nb.val for nb in n.neighbors]
            print(f"    Step {step[0]}: Clone node {n.val}, neighbors={nbr_vals}")
            print(f"      visited map: {{{', '.join(f'{k.val}→clone({v.val})' for k, v in old_to_new.items())}}}")

        for neighbor in n.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)


def demo_clone_graph(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("1b. Clone Graph — DFS + HashMap (LeetCode 133)")
    print("=" * 65)

    # Helper to build graph from adjacency list
    def build_graph(adj: List[List[int]]) -> Optional[GraphNode]:
        if not adj:
            return None
        nodes = {i + 1: GraphNode(i + 1) for i in range(len(adj))}
        for i, neighbors in enumerate(adj):
            nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
        return nodes[1]

    # Example 1:  1 --- 2
    #             |     |
    #             4 --- 3
    print("\n--- Example 1 ---")
    print("# Graph:  1 --- 2")
    print("#         |     |")
    print("#         4 --- 3")
    adj1 = [[2, 4], [1, 3], [2, 4], [1, 3]]
    node1 = build_graph(adj1)
    cloned1 = clone_graph(node1, verbose)
    print(f"  Original node1.val={node1.val}, id={id(node1)}")
    print(f"  Cloned   node1.val={cloned1.val}, id={id(cloned1)}")
    print(f"  Same object? {node1 is cloned1}")  # False
    assert node1 is not cloned1
    assert cloned1.val == 1

    # Example 2: single node
    print("\n--- Example 2: single node ---")
    single = GraphNode(1)
    cloned_s = clone_graph(single, verbose)
    print(f"  Original id={id(single)}, Cloned id={id(cloned_s)}")
    assert single is not cloned_s

    # Example 3: triangle 1-2-3
    print("\n--- Example 3: triangle 1-2-3 ---")
    print("# Graph:  1 --- 2")
    print("#          \\   /")
    print("#            3")
    adj3 = [[2, 3], [1, 3], [1, 2]]
    node3 = build_graph(adj3)
    cloned3 = clone_graph(node3, verbose)
    assert cloned3.val == 1
    assert len(cloned3.neighbors) == 2
    print(f"  Clone successful: node {cloned3.val} has {len(cloned3.neighbors)} neighbors")


# ---- 1c. Number of Connected Components ----
# LeetCode 323: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

def count_components(n: int, edges: List[List[int]], verbose: bool = False) -> int:
    """
    給 n 個節點 (0 ~ n-1) 和邊列表，找 connected components 數量。

    思路：建 adjacency list，DFS 遍歷，每次從未訪問節點開始 = 新的 component
    Time: O(V + E)  |  Space: O(V + E)
    """
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited: Set[int] = set()
    components = 0

    def dfs(node: int, comp_id: int) -> None:
        visited.add(node)
        if verbose:
            print(f"    Visit node {node} (component {comp_id})")
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor, comp_id)

    for i in range(n):
        if i not in visited:
            components += 1
            if verbose:
                print(f"  Start component {components} from node {i}")
            dfs(i, components)

    return components


def demo_count_components(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("1c. Number of Connected Components — DFS (LeetCode 323)")
    print("=" * 65)

    # Example 1
    # 0 --- 1    2 --- 3    4
    print("\n--- Example 1 ---")
    print("# 0 --- 1    2 --- 3    4  (isolated)")
    n1, edges1 = 5, [[0, 1], [2, 3]]
    result1 = count_components(n1, edges1, verbose)
    print(f"  Components: {result1}")  # 3
    assert result1 == 3

    # Example 2: all connected in a line
    # 0 --- 1 --- 2 --- 3
    print("\n--- Example 2 ---")
    print("# 0 --- 1 --- 2 --- 3  (one component)")
    n2, edges2 = 4, [[0, 1], [1, 2], [2, 3]]
    result2 = count_components(n2, edges2, verbose)
    print(f"  Components: {result2}")  # 1
    assert result2 == 1

    # Example 3: two triangles
    # 0-1-2 triangle + 3-4-5 triangle
    print("\n--- Example 3 ---")
    print("# Triangle 0-1-2 + Triangle 3-4-5")
    n3, edges3 = 6, [[0, 1], [1, 2], [0, 2], [3, 4], [4, 5], [3, 5]]
    result3 = count_components(n3, edges3, verbose)
    print(f"  Components: {result3}")  # 2
    assert result3 == 2


# ---- 1d. All Paths From Source to Target ----
# LeetCode 797: https://leetcode.com/problems/all-paths-from-source-to-target/

def all_paths_source_target(graph: List[List[int]], verbose: bool = False) -> List[List[int]]:
    """
    給一個 DAG（有向無環圖），以 adjacency list 表示。
    找從 node 0 到 node n-1 的所有路徑。

    思路：DFS + Backtracking
    - 維護當前 path
    - 到達 target → 加入 result
    - 回溯（pop）繼續探索

    Time: O(2^n * n) worst case  |  Space: O(n) for path
    """
    target = len(graph) - 1
    result = []
    step = [0]

    def dfs(node: int, path: List[int]) -> None:
        if node == target:
            result.append(path[:])  # 重要：要複製！
            if verbose:
                print(f"    Reached target! path = {path}")
            return

        for neighbor in graph[node]:
            step[0] += 1
            path.append(neighbor)
            if verbose:
                print(f"    Step {step[0]}: at node {node}, go to {neighbor}, path = {path}")
            dfs(neighbor, path)
            path.pop()  # backtrack
            if verbose:
                print(f"    Backtrack: pop {neighbor}, path = {path}")

    dfs(0, [0])
    return result


def demo_all_paths(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("1d. All Paths From Source to Target — DFS (LeetCode 797)")
    print("=" * 65)

    # Example 1: graph = [[1,2],[3],[3],[]]
    # 0 → 1 → 3
    # 0 → 2 → 3
    print("\n--- Example 1 ---")
    print("# DAG:  0 → 1 → 3")
    print("#       ↓       ↑")
    print("#       2 ──────┘")
    graph1 = [[1, 2], [3], [3], []]
    paths1 = all_paths_source_target(graph1, verbose)
    print(f"  All paths 0→3: {paths1}")  # [[0,1,3],[0,2,3]]
    assert sorted(paths1) == sorted([[0, 1, 3], [0, 2, 3]])

    # Example 2: graph = [[4,3,1],[3,2,4],[3],[4],[]]
    # 多條路徑
    print("\n--- Example 2 ---")
    print("# DAG: 0→{4,3,1}, 1→{3,2,4}, 2→{3}, 3→{4}, 4=target")
    graph2 = [[4, 3, 1], [3, 2, 4], [3], [4], []]
    paths2 = all_paths_source_target(graph2, verbose)
    print(f"  All paths 0→4: {paths2}")
    # [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]

    # Example 3: simple chain
    # 0 → 1 → 2
    print("\n--- Example 3: simple chain ---")
    print("# DAG: 0 → 1 → 2")
    graph3 = [[1], [2], []]
    paths3 = all_paths_source_target(graph3, verbose)
    print(f"  All paths 0→2: {paths3}")  # [[0,1,2]]
    assert paths3 == [[0, 1, 2]]


# ============================================================
# Section 2: Graph BFS
# ============================================================

# ---- 2a. Number of Islands (BFS version) ----

def num_islands_bfs(grid: List[List[str]], verbose: bool = False) -> int:
    """
    與 DFS 版本相同問題，改用 BFS。

    差異：DFS 用 recursion stack，BFS 用 queue
    - BFS 先處理同一層的鄰居，再往外擴展（像漣漪）
    - DFS 先一條路走到底，再回頭

    Time: O(m * n)  |  Space: O(min(m, n)) for queue
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def bfs(r: int, c: int) -> None:
        queue = deque([(r, c)])
        grid[r][c] = '#'
        step = 0
        while queue:
            cr, cc = queue.popleft()
            step += 1
            if verbose:
                print(f"    Step {step}: dequeue ({cr},{cc}), queue size={len(queue)}")
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '#'
                    queue.append((nr, nc))
                    if verbose:
                        print(f"      enqueue ({nr},{nc})")

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                if verbose:
                    print(f"  Found island #{count} at ({r},{c}), starting BFS")
                bfs(r, c)

    return count


def demo_num_islands_bfs(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("2a. Number of Islands — BFS version (LeetCode 200)")
    print("=" * 65)
    print("  Comparison: DFS goes deep first; BFS spreads outward layer by layer")

    grid1 = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1'],
    ]
    print("\nExample 1:")
    for row in grid1:
        print("   ", row)
    g1 = [row[:] for row in grid1]
    r1 = num_islands_bfs(g1, verbose)
    print(f"  Answer: {r1}")  # 3
    assert r1 == 3

    grid2 = [
        ['1', '0', '1', '0'],
        ['0', '1', '0', '1'],
        ['1', '0', '1', '0'],
    ]
    print("\nExample 2 (checkerboard):")
    for row in grid2:
        print("   ", row)
    g2 = [row[:] for row in grid2]
    r2 = num_islands_bfs(g2, verbose)
    print(f"  Answer: {r2}")  # 6 (each '1' is isolated)
    assert r2 == 6

    grid3 = [
        ['1', '1', '1'],
        ['1', '0', '1'],
        ['1', '1', '1'],
    ]
    print("\nExample 3 (donut shape):")
    for row in grid3:
        print("   ", row)
    g3 = [row[:] for row in grid3]
    r3 = num_islands_bfs(g3, verbose)
    print(f"  Answer: {r3}")  # 1
    assert r3 == 1


# ---- 2b. Rotting Oranges ----
# LeetCode 994: https://leetcode.com/problems/rotting-oranges/

def oranges_rotting(grid: List[List[int]], verbose: bool = False) -> int:
    """
    0 = 空, 1 = 新鮮橘子, 2 = 腐爛橘子
    每分鐘，腐爛橘子會感染上下左右的新鮮橘子。
    回傳所有橘子腐爛所需的最少分鐘數；如果不可能，回傳 -1。

    思路：Multi-source BFS（多源 BFS）
    - 把所有初始腐爛橘子放入 queue（多個起點同時開始）
    - 每一輪 BFS = 1 分鐘
    - 結束後檢查是否還有新鮮橘子

    Time: O(m * n)  |  Space: O(m * n)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    # Step 1: 找出所有腐爛橘子（多源起點）+ 計算新鮮數
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if verbose:
        print(f"  Initial: {len(queue)} rotten, {fresh} fresh")

    if fresh == 0:
        return 0

    minutes = 0
    while queue and fresh > 0:
        minutes += 1
        if verbose:
            print(f"  Minute {minutes}: processing {len(queue)} rotten oranges")
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
                    if verbose:
                        print(f"    ({nr},{nc}) becomes rotten, fresh left={fresh}")

    return minutes if fresh == 0 else -1


def demo_rotting_oranges(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("2b. Rotting Oranges — Multi-source BFS (LeetCode 994)")
    print("=" * 65)

    # Example 1
    # 2 1 1      2 2 1      2 2 2      2 2 2
    # 1 1 0  →   2 1 0  →   2 2 0  →   2 2 0   = 4 minutes
    # 0 1 1      0 1 1      0 2 1      0 2 2
    grid1 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    print("\nExample 1:")
    print("  Grid:  2 1 1")
    print("         1 1 0")
    print("         0 1 1")
    g1 = [row[:] for row in grid1]
    r1 = oranges_rotting(g1, verbose)
    print(f"  Answer: {r1} minutes")  # 4
    assert r1 == 4

    # Example 2: impossible
    grid2 = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    print("\nExample 2 (impossible — isolated fresh orange):")
    print("  Grid:  2 1 1")
    print("         0 1 1")
    print("         1 0 1")
    g2 = [row[:] for row in grid2]
    r2 = oranges_rotting(g2, verbose)
    print(f"  Answer: {r2}")  # -1
    assert r2 == -1

    # Example 3: already all rotten or empty
    grid3 = [[0, 2]]
    print("\nExample 3 (no fresh oranges):")
    print("  Grid:  0 2")
    g3 = [row[:] for row in grid3]
    r3 = oranges_rotting(g3, verbose)
    print(f"  Answer: {r3}")  # 0
    assert r3 == 0


# ---- 2c. 01 Matrix ----
# LeetCode 542: https://leetcode.com/problems/01-matrix/

def update_matrix(mat: List[List[int]], verbose: bool = False) -> List[List[int]]:
    """
    給一個 01 矩陣，求每個格子到最近 0 的距離。

    思路：Multi-source BFS（從所有 0 開始向外擴展）
    - 把所有 0 放入 queue（距離=0）
    - BFS 每擴一層 → 距離 +1
    - 比「從每個 1 找最近 0」快很多！

    Time: O(m * n)  |  Space: O(m * n)
    """
    rows, cols = len(mat), len(mat[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    queue = deque()

    # 所有 0 作為 BFS 起點
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    if verbose:
        print(f"  BFS sources (all 0s): {len(queue)} cells")

    level = 0
    while queue:
        size = len(queue)
        level += 1
        for _ in range(size):
            r, c = queue.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > dist[r][c] + 1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
                    if verbose:
                        print(f"    ({nr},{nc}) dist = {dist[nr][nc]}")

    return dist


def demo_01_matrix(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("2c. 01 Matrix — BFS from targets (LeetCode 542)")
    print("=" * 65)

    # Example 1
    mat1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print("\nExample 1:")
    print("  Input:   0 0 0")
    print("           0 1 0")
    print("           0 0 0")
    r1 = update_matrix([row[:] for row in mat1], verbose)
    print("  Output:")
    for row in r1:
        print("          ", row)
    # [[0,0,0],[0,1,0],[0,0,0]]
    assert r1 == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

    # Example 2
    mat2 = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    print("\nExample 2:")
    print("  Input:   0 0 0")
    print("           0 1 0")
    print("           1 1 1")
    r2 = update_matrix([row[:] for row in mat2], verbose)
    print("  Output:")
    for row in r2:
        print("          ", row)
    # [[0,0,0],[0,1,0],[1,2,1]]
    assert r2 == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]

    # Example 3: larger
    mat3 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 0],
    ]
    print("\nExample 3:")
    print("  Input:   1 1 1")
    print("           1 1 1")
    print("           1 1 0")
    r3 = update_matrix([row[:] for row in mat3], verbose)
    print("  Output:")
    for row in r3:
        print("          ", row)
    # [[4,3,2],[3,2,1],[2,1,0]]
    assert r3 == [[4, 3, 2], [3, 2, 1], [2, 1, 0]]


# ---- 2d. Word Ladder ----
# LeetCode 127: https://leetcode.com/problems/word-ladder/

def ladder_length(begin_word: str, end_word: str, word_list: List[str],
                  verbose: bool = False) -> int:
    """
    從 beginWord 變換到 endWord，每次只能改一個字母，且中間的字必須在 wordList 中。
    求最短變換序列的長度（包含首尾）。

    思路：BFS — 每個 word 是一個節點，差一個字母的 word 之間有邊
    - 建立「pattern → words」的 map，例如 "h*t" → ["hot", "hat"]
    - BFS level by level，level 數 = 變換步數

    Time: O(M^2 * N) where M=word length, N=word count
    Space: O(M^2 * N)
    """
    if end_word not in word_list:
        return 0

    word_set = set(word_list)
    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    if verbose:
        print(f"  Start: '{begin_word}' → Target: '{end_word}'")
        print(f"  Word list: {word_list}")

    while queue:
        word, level = queue.popleft()
        if verbose:
            print(f"  Level {level}: processing '{word}'")

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i + 1:]
                if next_word == end_word:
                    if verbose:
                        print(f"    Found! '{word}' → '{next_word}' at level {level + 1}")
                    return level + 1
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, level + 1))
                    if verbose:
                        print(f"    '{word}' → '{next_word}' (enqueue, level {level + 1})")

    return 0


def demo_word_ladder(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("2d. Word Ladder — BFS level-by-level (LeetCode 127)")
    print("=" * 65)

    # Example 1: hit → cog
    # hit → hot → dot → dog → cog  (length = 5)
    print("\n--- Example 1: 'hit' → 'cog' ---")
    r1 = ladder_length("hit", "cog",
                        ["hot", "dot", "dog", "lot", "log", "cog"], verbose)
    print(f"  Shortest transformation length: {r1}")  # 5
    assert r1 == 5

    # Example 2: hit → cog (cog not in list)
    print("\n--- Example 2: 'hit' → 'cog' (cog not in list) ---")
    r2 = ladder_length("hit", "cog",
                        ["hot", "dot", "dog", "lot", "log"], verbose)
    print(f"  Shortest transformation length: {r2}")  # 0
    assert r2 == 0

    # Example 3: a → c
    print("\n--- Example 3: 'a' → 'c' ---")
    r3 = ladder_length("a", "c", ["a", "b", "c"], verbose)
    print(f"  Shortest transformation length: {r3}")  # 2
    assert r3 == 2


# ============================================================
# Section 3: Grid 類特殊 DFS/BFS
# ============================================================

# ---- 3a. Surrounded Regions ----
# LeetCode 130: https://leetcode.com/problems/surrounded-regions/

def solve_surrounded(board: List[List[str]], verbose: bool = False) -> None:
    """
    把被 'X' 完全包圍的 'O' 翻成 'X'。
    邊界上的 'O' 和它相連的 'O' 不算被包圍。

    逆向思維（Reverse Thinking）：
    - 不是找「被包圍的 O」，而是找「不被包圍的 O」
    - 從邊界上的 O 開始 DFS，標記為 safe
    - 最後：safe → 'O'，其他 O → 'X'

    Time: O(m * n)  |  Space: O(m * n)
    """
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'S'  # Safe — connected to border
        if verbose:
            print(f"    Mark ({r},{c}) as Safe")
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Step 1: DFS from all border 'O's
    if verbose:
        print("  Step 1: Mark border-connected O's as Safe")
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and board[r][c] == 'O':
                if verbose:
                    print(f"  Border O at ({r},{c}), start DFS:")
                dfs(r, c)

    # Step 2: Flip
    if verbose:
        print("  Step 2: S→O (safe), O→X (captured)")
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'  # captured
            elif board[r][c] == 'S':
                board[r][c] = 'O'  # restore safe


def demo_surrounded_regions(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("3a. Surrounded Regions — Reverse DFS from border (LeetCode 130)")
    print("=" * 65)

    # Example 1
    board1 = [
        ['X', 'X', 'X', 'X'],
        ['X', 'O', 'O', 'X'],
        ['X', 'X', 'O', 'X'],
        ['X', 'O', 'X', 'X'],
    ]
    print("\nExample 1:")
    print("  Before:")
    for row in board1:
        print("   ", row)
    b1 = [row[:] for row in board1]
    solve_surrounded(b1, verbose)
    print("  After:")
    for row in b1:
        print("   ", row)
    # All O's are surrounded → all become X
    expected1 = [['X'] * 4, ['X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X'], ['X', 'O', 'X', 'X']]
    # Actually (3,1) is on the border-adjacent? Let me check:
    # (3,1) is not on the border (row 3 is last row → it IS border)
    # So (3,1) is a border O → safe!
    assert b1[3][1] == 'O'  # border O stays
    assert b1[1][1] == 'X'  # inner O captured

    # Example 2: O on border connects to inner O
    board2 = [
        ['X', 'O', 'X'],
        ['O', 'O', 'X'],
        ['X', 'X', 'X'],
    ]
    print("\nExample 2 (border O connects inward):")
    print("  Before:")
    for row in board2:
        print("   ", row)
    b2 = [row[:] for row in board2]
    solve_surrounded(b2, verbose)
    print("  After:")
    for row in b2:
        print("   ", row)
    # (0,1) is border O → connects to (1,1) and (1,0)
    assert b2[0][1] == 'O'
    assert b2[1][0] == 'O'
    assert b2[1][1] == 'O'

    # Example 3: all O
    board3 = [['O', 'O'], ['O', 'O']]
    print("\nExample 3 (all O — all on border):")
    print("  Before:")
    for row in board3:
        print("   ", row)
    b3 = [row[:] for row in board3]
    solve_surrounded(b3, verbose)
    print("  After:")
    for row in b3:
        print("   ", row)
    assert b3 == [['O', 'O'], ['O', 'O']]


# ---- 3b. Pacific Atlantic Water Flow ----
# LeetCode 417: https://leetcode.com/problems/pacific-atlantic-water-flow/

def pacific_atlantic(heights: List[List[int]], verbose: bool = False) -> List[List[int]]:
    """
    左/上邊界是 Pacific，右/下邊界是 Atlantic。
    水往低處流。找出哪些格子的水能同時流到兩個大洋。

    逆向思維：從海洋「逆流而上」DFS
    - 從 Pacific 邊界開始 DFS，找能到達的格子（往高處走）
    - 從 Atlantic 邊界開始 DFS，找能到達的格子
    - 兩組交集 = 答案

    Time: O(m * n)  |  Space: O(m * n)
    """
    if not heights:
        return []

    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r: int, c: int, reachable: Set, prev_height: int) -> None:
        if (r, c) in reachable:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if heights[r][c] < prev_height:
            return
        reachable.add((r, c))
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dfs(r + dr, c + dc, reachable, heights[r][c])

    # Pacific: top row + left column
    for c in range(cols):
        dfs(0, c, pacific, heights[0][c])
    for r in range(rows):
        dfs(r, 0, pacific, heights[r][0])

    # Atlantic: bottom row + right column
    for c in range(cols):
        dfs(rows - 1, c, atlantic, heights[rows - 1][c])
    for r in range(rows):
        dfs(r, cols - 1, atlantic, heights[r][cols - 1])

    result = sorted([[r, c] for r, c in pacific & atlantic])

    if verbose:
        print(f"  Pacific reachable: {sorted(pacific)}")
        print(f"  Atlantic reachable: {sorted(atlantic)}")
        print(f"  Both (intersection): {result}")

    return result


def demo_pacific_atlantic(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("3b. Pacific Atlantic Water Flow — Reverse DFS (LeetCode 417)")
    print("=" * 65)
    print("  Key insight: DFS from ocean borders UPHILL (reverse flow)")

    # Example 1
    heights1 = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    print("\nExample 1:")
    print("  Heights:")
    for row in heights1:
        print("   ", row)
    r1 = pacific_atlantic(heights1, verbose)
    print(f"  Cells reaching both oceans: {r1}")
    # Expected: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

    # Example 2: 1x1
    print("\nExample 2 (1x1 grid):")
    heights2 = [[1]]
    r2 = pacific_atlantic(heights2, verbose)
    print(f"  Result: {r2}")  # [[0,0]]
    assert r2 == [[0, 0]]

    # Example 3: flat grid
    print("\nExample 3 (all same height):")
    heights3 = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    r3 = pacific_atlantic(heights3, verbose)
    print(f"  Result: {r3}")
    assert len(r3) == 9  # all cells reach both


# ---- 3c. Shortest Path in Binary Matrix ----
# LeetCode 1091: https://leetcode.com/problems/shortest-path-in-binary-matrix/

def shortest_path_binary_matrix(grid: List[List[int]], verbose: bool = False) -> int:
    """
    在 n x n 的 01 矩陣中，找從 (0,0) 到 (n-1,n-1) 的最短路徑。
    可以走 8 個方向（含對角線），只能走 0 的格子。

    思路：BFS（無權圖最短路徑就用 BFS！）
    - 8 方向擴展
    - 回傳路徑長度（格子數）

    Time: O(n^2)  |  Space: O(n^2)
    """
    n = len(grid)
    if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
        return -1

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    queue = deque([(0, 0, 1)])  # (row, col, path_length)
    grid[0][0] = 1  # mark visited

    step = 0
    while queue:
        r, c, dist = queue.popleft()
        step += 1
        if verbose and step <= 15:
            print(f"    Step {step}: dequeue ({r},{c}) dist={dist}")

        if r == n - 1 and c == n - 1:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                queue.append((nr, nc, dist + 1))
                if verbose and step <= 15:
                    print(f"      enqueue ({nr},{nc}) dist={dist + 1}")

    return -1


def demo_shortest_path_binary(verbose: bool = True) -> None:
    print("\n" + "=" * 65)
    print("3c. Shortest Path in Binary Matrix — BFS 8-dir (LeetCode 1091)")
    print("=" * 65)

    # Example 1
    grid1 = [[0, 1], [1, 0]]
    print("\nExample 1:")
    print("  Grid: 0 1")
    print("        1 0")
    g1 = [row[:] for row in grid1]
    r1 = shortest_path_binary_matrix(g1, verbose)
    print(f"  Shortest path length: {r1}")  # 2 (diagonal)
    assert r1 == 2

    # Example 2
    grid2 = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    print("\nExample 2:")
    print("  Grid: 0 0 0")
    print("        1 1 0")
    print("        1 1 0")
    g2 = [row[:] for row in grid2]
    r2 = shortest_path_binary_matrix(g2, verbose)
    print(f"  Shortest path length: {r2}")  # 4
    assert r2 == 4

    # Example 3: blocked
    grid3 = [[1, 0, 0], [1, 1, 0], [1, 1, 0]]
    print("\nExample 3 (start blocked):")
    print("  Grid: 1 0 0")
    print("        1 1 0")
    print("        1 1 0")
    g3 = [row[:] for row in grid3]
    r3 = shortest_path_binary_matrix(g3, verbose)
    print(f"  Shortest path length: {r3}")  # -1
    assert r3 == -1


# ============================================================
# Section 4: Graph DFS vs BFS 比較與選擇
# ============================================================

def section4_dfs_vs_bfs_comparison(verbose: bool = True) -> None:
    """
    CRITICAL: 什麼時候用 DFS，什麼時候用 BFS？

    ┌──────────────────────────┬────────────────────────────────────┐
    │ 用 BFS                    │ 用 DFS                              │
    ├──────────────────────────┼────────────────────────────────────┤
    │ 最短路徑（unweighted）    │ 找所有路徑 / 排列 / 組合            │
    │ Level-order traversal    │ Cycle detection                     │
    │ 找最近的 X               │ Connected components                │
    │ Multi-source 同時擴展    │ Topological sort                    │
    │ 擴散/感染類問題          │ 判斷連通性（reachability）           │
    │ 圖的「直徑」(shortest)   │ Backtracking / 剪枝                 │
    └──────────────────────────┴────────────────────────────────────┘

    記憶口訣：
    - "shortest / nearest / level" → BFS
    - "all / every / connected / path" → DFS
    """
    if not verbose:
        return

    print("\n" + "=" * 65)
    print("Section 4: DFS vs BFS — 比較與選擇指南")
    print("=" * 65)

    print("""
    ┌──────────────────────────────────────────────────────────────┐
    │             DFS vs BFS 選擇決策樹                            │
    ├──────────────────────────────────────────────────────────────┤
    │                                                              │
    │  Q1: 要找最短路徑（unweighted graph）嗎？                     │
    │      YES → BFS ★                                            │
    │      NO  → 繼續                                              │
    │                                                              │
    │  Q2: 要找所有路徑 / 所有組合 / 排列？                         │
    │      YES → DFS + Backtracking ★                             │
    │      NO  → 繼續                                              │
    │                                                              │
    │  Q3: 是 level-by-level 或 layer-by-layer 的擴散？             │
    │      YES → BFS (multi-source 如果多起點) ★                   │
    │      NO  → 繼續                                              │
    │                                                              │
    │  Q4: 要做 topological sort？                                  │
    │      YES → DFS (post-order) 或 BFS (Kahn's) ★               │
    │      NO  → 繼續                                              │
    │                                                              │
    │  Q5: 只需判斷「能不能到達」或「幾個連通分量」？                │
    │      YES → DFS 或 BFS 都行（DFS 寫起來較簡短）★              │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
    """)

    # ── 同一題用 DFS 和 BFS 兩種方式解 ──
    print("--- Demo: 同一個圖，DFS vs BFS traversal order ---")
    print()
    print("# Graph:  0 --- 1 --- 2")
    print("#         |           |")
    print("#         3 --- 4 --- 5")
    print()

    adj = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 5],
        3: [0, 4],
        4: [3, 5],
        5: [2, 4],
    }

    # DFS traversal
    def dfs_order(start: int) -> List[int]:
        visited = set()
        order = []

        def dfs(node: int) -> None:
            visited.add(node)
            order.append(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return order

    # BFS traversal
    def bfs_order(start: int) -> List[int]:
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    dfs_result = dfs_order(0)
    bfs_result = bfs_order(0)

    print(f"  DFS from 0: {dfs_result}")
    # DFS: 0 → 1 → 2 → 5 → 4 → 3 (goes deep first)
    print(f"    Goes deep: 0→1→2→5→4→3")
    print()
    print(f"  BFS from 0: {bfs_result}")
    # BFS: 0 → 1, 3 → 2, 4 → 5 (level by level)
    print(f"    Goes wide: 0 → [1,3] → [2,4] → [5]")

    print()
    print("--- Key difference: BFS finds shortest path ---")
    print()
    print("  BFS from 0 to 5:")
    print("    Level 0: {0}")
    print("    Level 1: {1, 3}")
    print("    Level 2: {2, 4}")
    print("    Level 3: {5}  ← found! shortest distance = 3")
    print()
    print("  DFS from 0 to 5:")
    print("    Path found: 0→1→2→5 (length 3, happens to be shortest)")
    print("    But DFS does NOT guarantee shortest path!")
    print("    If adj[0] = [3, 1], DFS might find 0→3→4→5 first")

    print()
    print("--- Multi-source BFS 概念 ---")
    print()
    print("  普通 BFS：一個起點，像丟一顆石頭進水裡的漣漪")
    print("  Multi-source BFS：多個起點，像同時丟多顆石頭")
    print()
    print("  應用場景：")
    print("    - Rotting Oranges: 所有腐爛橘子「同時」開始擴散")
    print("    - 01 Matrix: 從所有 0 同時向外 BFS 找最短距離")
    print("    - Walls and Gates: 從所有 gate 同時 BFS")
    print()
    print("  實作方式：把所有起點先全部放入 queue，然後正常 BFS")
    print("    queue = deque(all_sources)  # 不是只放一個！")

    # ── 經典題型分類 ──
    print()
    print("--- 經典題型分類表 ---")
    print()
    print("  [BFS 類]")
    print("    - Number of Islands (BFS version)")
    print("    - Rotting Oranges (multi-source BFS) ★★★")
    print("    - 01 Matrix (multi-source BFS)")
    print("    - Word Ladder (shortest transformation)")
    print("    - Shortest Path in Binary Matrix (8-dir BFS)")
    print("    - Walls and Gates")
    print("    - Open the Lock")
    print()
    print("  [DFS 類]")
    print("    - Number of Islands (DFS version)")
    print("    - Clone Graph (DFS + HashMap)")
    print("    - Connected Components")
    print("    - All Paths From Source to Target (DFS + backtrack)")
    print("    - Surrounded Regions (border DFS)")
    print("    - Pacific Atlantic Water Flow (reverse DFS)")
    print("    - Course Schedule (cycle detection)")
    print()
    print("  [DFS 和 BFS 都行]")
    print("    - Number of Islands")
    print("    - Flood Fill")
    print("    - Connected Components")
    print("    - 判斷圖是否連通")

    # ── 複雜度比較 ──
    print()
    print("--- 時間 / 空間複雜度 ---")
    print()
    print("  兩者的時間複雜度相同：O(V + E)")
    print("  空間差異：")
    print("    DFS: O(V) recursion stack（worst case: 長鏈圖）")
    print("    BFS: O(V) queue（worst case: 星狀圖，所有節點連到中心）")
    print()
    print("  Grid 問題中（m x n）：")
    print("    Time: O(m * n)")
    print("    DFS Space: O(m * n) worst case recursion depth")
    print("    BFS Space: O(min(m, n)) — queue 最寬處")


# ============================================================
# main() — 執行所有範例
# ============================================================

def main():
    print("╔" + "═" * 63 + "╗")
    print("║  09_Graph_DFS_BFS.py — Graph 基礎 DFS / BFS 完整教學       ║")
    print("║  LeetCode 面試準備 | Google / NVIDIA 導向                   ║")
    print("╚" + "═" * 63 + "╝")
    print()
    print("目錄 Table of Contents:")
    print("  Section 0: 圖的基礎表示法 (Graph Representations)")
    print("  Section 1: Graph DFS")
    print("    1a. Number of Islands (DFS)")
    print("    1b. Clone Graph")
    print("    1c. Number of Connected Components")
    print("    1d. All Paths From Source to Target")
    print("  Section 2: Graph BFS")
    print("    2a. Number of Islands (BFS)")
    print("    2b. Rotting Oranges (Multi-source BFS)")
    print("    2c. 01 Matrix (BFS from targets)")
    print("    2d. Word Ladder")
    print("  Section 3: Grid 類特殊 DFS/BFS")
    print("    3a. Surrounded Regions")
    print("    3b. Pacific Atlantic Water Flow")
    print("    3c. Shortest Path in Binary Matrix")
    print("  Section 4: DFS vs BFS 比較與選擇")

    v = True  # verbose mode — 顯示詳細追蹤

    # Section 0
    section0_graph_representations(v)

    # Section 1: Graph DFS
    demo_num_islands_dfs(v)
    demo_clone_graph(v)
    demo_count_components(v)
    demo_all_paths(v)

    # Section 2: Graph BFS
    demo_num_islands_bfs(v)
    demo_rotting_oranges(v)
    demo_01_matrix(v)
    demo_word_ladder(v)

    # Section 3: Grid special DFS/BFS
    demo_surrounded_regions(v)
    demo_pacific_atlantic(v)
    demo_shortest_path_binary(v)

    # Section 4: DFS vs BFS comparison
    section4_dfs_vs_bfs_comparison(v)

    print()
    print("=" * 65)
    print("ALL ASSERTIONS PASSED — 所有測試通過！")
    print("=" * 65)
    print()
    print("學習建議 Study Tips:")
    print("  1. 先掌握 Section 0 的圖表示法（面試一定要會建圖）")
    print("  2. DFS: 先學 Number of Islands (grid DFS 的入門題)")
    print("  3. BFS: 先學 Rotting Oranges (multi-source BFS 經典)")
    print("  4. 熟記 Section 4 的 DFS vs BFS 決策樹")
    print("  5. Google 高頻: Word Ladder, Clone Graph, Islands")
    print("  6. NVIDIA 高頻: Shortest Path, Connected Components")


if __name__ == "__main__":
    main()
