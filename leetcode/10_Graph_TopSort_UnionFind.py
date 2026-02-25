"""
=============================================================================
 10_Graph_TopSort_UnionFind.py
 拓撲排序 (Topological Sort) + 並查集 (Union-Find) + 最短路徑 (Shortest Path)
=============================================================================

適用對象：LeetCode 初學者，準備 Google / NVIDIA 面試
教學風格：每題皆附 step-by-step 數值 trace，用「跑一次給你看」取代抽象描述
語言：Traditional Chinese + English 技術術語
前置知識：09_Graph_DFS_BFS.py (Graph 基礎 — DFS / BFS)

目錄 (Table of Contents):
  Section 1: 拓撲排序 — BFS (Kahn's Algorithm)
    1.1 Course Schedule (can finish?)
    1.2 Course Schedule II (find order)
    1.3 Alien Dictionary (Google classic!)
  Section 2: 拓撲排序 — DFS
    2.1 Course Schedule with DFS (white/gray/black states)
    2.2 Kahn's BFS vs DFS 比較
    2.3 Cycle Detection in Directed Graph
  Section 3: Union-Find 基礎
    3.1 find() with Path Compression + union() with Rank
    3.2 Number of Connected Components
    3.3 Redundant Connection
  Section 4: Union-Find 進階
    4.1 Accounts Merge
    4.2 Number of Provinces
    4.3 Smallest String With Swaps
  Section 5: 最短路徑 (Shortest Path)
    5.1 Dijkstra's Algorithm
    5.2 Network Delay Time
    5.3 Cheapest Flights Within K Stops
    5.4 Bellman-Ford 概念
  Section 6: TopSort vs Union-Find vs Shortest Path 比較
"""

from collections import defaultdict, deque
import heapq
from typing import List, Optional

# =============================================================================
# Section 1: 拓撲排序 — BFS (Kahn's Algorithm)
# =============================================================================
# 拓撲排序 = 把 DAG 節點排成一條線，所有邊從左指向右。
# 想像選課：修「資料結構」前必須先修「程式設計」→ 找合法修課順序。
#
# Kahn's Algorithm 步驟:
#   1. 算每個節點的 indegree (入度)
#   2. indegree=0 的放入 queue → 3. 取出 → 鄰居 indegree-1
#   4. indegree 變 0 的加入 queue → 5. 重複到 queue 空
#   6. 結果長度 < 節點數 → 有環!

# ---------------------------------------------------------------------------
# 1.1 Course Schedule (LeetCode 207) — 能否修完所有課?
# ---------------------------------------------------------------------------
def can_finish_courses(num_courses: int,
                       prerequisites: List[List[int]],
                       verbose: bool = False) -> bool:
    """
    判斷能否修完所有課程（有沒有環）。
    prerequisites[i] = [a, b] 表示修 a 之前必須先修 b (b → a)。

    Time: O(V + E), Space: O(V + E)
    """
    # Step 1: 建圖 + 計算 indegree
    graph = defaultdict(list)
    indegree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)  # prereq → course
        indegree[course] += 1

    if verbose:
        print(f"  課程數: {num_courses}")
        print(f"  先修關係: {prerequisites}")
        print(f"  圖 (adjacency list): {dict(graph)}")
        print(f"  indegree: {indegree}")

    # Step 2: 把 indegree=0 的節點放入 queue
    queue = deque()
    for i in range(num_courses):
        if indegree[i] == 0:
            queue.append(i)

    if verbose:
        print(f"  初始 queue (indegree=0): {list(queue)}")

    # Step 3-5: BFS
    count = 0  # 已處理的課程數
    step = 0
    while queue:
        step += 1
        node = queue.popleft()
        count += 1

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

        if verbose:
            print(f"  Step {step}: pop {node}, "
                  f"indegree={indegree}, queue={list(queue)}, count={count}")

    result = count == num_courses
    if verbose:
        print(f"  結果: count={count}, numCourses={num_courses}, "
              f"canFinish={result}")
        if not result:
            print(f"  ⚠ 有環 (cycle)! 無法修完所有課程")
    return result

# ---------------------------------------------------------------------------
# 1.2 Course Schedule II (LeetCode 210) — 找出修課順序
# ---------------------------------------------------------------------------
def find_course_order(num_courses: int,
                      prerequisites: List[List[int]],
                      verbose: bool = False) -> List[int]:
    """
    回傳一個合法的修課順序。如果有環，回傳空 list。

    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    indegree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    if verbose:
        print(f"  課程數: {num_courses}")
        print(f"  先修關係: {prerequisites}")
        print(f"  圖: {dict(graph)}")
        print(f"  indegree: {indegree}")

    queue = deque()
    for i in range(num_courses):
        if indegree[i] == 0:
            queue.append(i)

    order = []
    step = 0

    if verbose:
        print(f"  初始 queue: {list(queue)}")

    while queue:
        step += 1
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

        if verbose:
            print(f"  Step {step}: pop {node}, "
                  f"indegree={indegree}, queue={list(queue)}, order={order}")

    if len(order) == num_courses:
        if verbose:
            print(f"  合法修課順序: {order}")
        return order
    else:
        if verbose:
            print(f"  有環! 已處理 {len(order)}/{num_courses}，回傳 []")
        return []

# ---------------------------------------------------------------------------
# 1.3 Alien Dictionary (LeetCode 269) — Google 經典題!
# ---------------------------------------------------------------------------
def alien_order(words: List[str], verbose: bool = False) -> str:
    """
    外星字典：給定一組按外星字母序排序的單字，推導字母順序。

    思路：比較相鄰單字，找出字母間的先後關係 → 建圖 → 拓撲排序。

    Time: O(C), C = 所有字元數總和, Space: O(1) (最多 26 字母)
    """
    # Step 1: 收集所有出現過的字母
    all_chars = set()
    for word in words:
        for c in word:
            all_chars.add(c)

    graph = defaultdict(set)  # 用 set 避免重複邊
    indegree = {c: 0 for c in all_chars}

    if verbose:
        print(f"  單字列表: {words}")
        print(f"  所有字母: {sorted(all_chars)}")

    # Step 2: 比較相鄰單字，建立邊
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        # 檢查 prefix 矛盾：如果 w1 比 w2 長，且 w2 是 w1 的 prefix → 無效
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            if verbose:
                print(f"  無效! '{w1}' > '{w2}' 但 '{w2}' 是 '{w1}' 的 prefix")
            return ""

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:  # 新的邊
                    graph[c1].add(c2)
                    indegree[c2] += 1
                    if verbose:
                        print(f"  比較 '{w1}' vs '{w2}': "
                              f"'{c1}' → '{c2}' (第一個不同字母)")
                break  # 只看第一個不同的字母

    if verbose:
        graph_str = {k: list(v) for k, v in graph.items()}
        print(f"  圖: {graph_str}")
        print(f"  indegree: {indegree}")

    # Step 3: Kahn's BFS
    queue = deque()
    for c in sorted(all_chars):  # sorted 確保在多解時回傳字典序最小
        if indegree[c] == 0:
            queue.append(c)

    result = []
    step = 0
    if verbose:
        print(f"  初始 queue: {list(queue)}")

    while queue:
        step += 1
        c = queue.popleft()
        result.append(c)

        for neighbor in sorted(graph[c]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

        if verbose:
            remaining_indeg = {k: v for k, v in indegree.items() if v > 0}
            print(f"  Step {step}: pop '{c}', "
                  f"remaining indegree={remaining_indeg}, "
                  f"queue={list(queue)}, result={''.join(result)}")

    if len(result) == len(all_chars):
        answer = "".join(result)
        if verbose:
            print(f"  外星字母順序: {answer}")
        return answer
    else:
        if verbose:
            print(f"  有環! 處理了 {len(result)}/{len(all_chars)} 個字母")
        return ""

# =============================================================================
# Section 2: 拓撲排序 — DFS (三色標記法)
# =============================================================================
# WHITE(0)=未造訪, GRAY(1)=處理中(在DFS路徑上), BLACK(2)=已完成
# 碰到 GRAY → 發現環 (back edge)！
# 節點完成後加到結果前面 (reverse postorder = 拓撲序)

# ---------------------------------------------------------------------------
# 2.1 Course Schedule — DFS Approach
# ---------------------------------------------------------------------------
WHITE, GRAY, BLACK = 0, 1, 2

def can_finish_dfs(num_courses: int,
                   prerequisites: List[List[int]],
                   verbose: bool = False) -> bool:
    """
    用 DFS 三色標記法判斷能否修完所有課程。

    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * num_courses
    color_names = {WHITE: "WHITE", GRAY: "GRAY", BLACK: "BLACK"}

    if verbose:
        print(f"  課程數: {num_courses}, 先修關係: {prerequisites}")
        print(f"  圖: {dict(graph)}")

    def dfs(node, depth=0):
        indent = "    " + "  " * depth
        color[node] = GRAY
        if verbose:
            colors = [color_names[c] for c in color]
            print(f"{indent}進入 node {node}, color → GRAY, "
                  f"states={colors}")

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                if verbose:
                    print(f"{indent}  鄰居 {neighbor} 是 GRAY → "
                          f"發現環 (cycle)!")
                return False  # 發現環
            if color[neighbor] == WHITE:
                if not dfs(neighbor, depth + 1):
                    return False

        color[node] = BLACK
        if verbose:
            colors = [color_names[c] for c in color]
            print(f"{indent}完成 node {node}, color → BLACK, "
                  f"states={colors}")
        return True

    for i in range(num_courses):
        if color[i] == WHITE:
            if verbose:
                print(f"  --- 從 node {i} 開始 DFS ---")
            if not dfs(i):
                if verbose:
                    print(f"  結果: 有環，無法修完!")
                return False

    if verbose:
        print(f"  結果: 無環，可以修完所有課程!")
    return True

# ---------------------------------------------------------------------------
# 2.3 Cycle Detection in Directed Graph
# ---------------------------------------------------------------------------
def has_cycle_directed(num_nodes: int,
                       edges: List[List[int]],
                       verbose: bool = False) -> bool:
    """
    偵測有向圖中是否有環。回傳 True 表示有環。

    使用 DFS 三色標記法：碰到 GRAY → 有環。

    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * num_nodes
    color_names = {WHITE: "W", GRAY: "G", BLACK: "B"}
    cycle_path = []  # 記錄環的路徑

    if verbose:
        print(f"  節點數: {num_nodes}, 邊: {edges}")

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # 找到環，提取環路徑
                cycle_start = path.index(neighbor)
                cycle_path.extend(path[cycle_start:])
                cycle_path.append(neighbor)  # 閉合環
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor, path):
                    return True

        path.pop()
        color[node] = BLACK
        return False

    for i in range(num_nodes):
        if color[i] == WHITE:
            if dfs(i, []):
                if verbose:
                    colors = [color_names[c] for c in color]
                    print(f"  發現環! 路徑: {' → '.join(map(str, cycle_path))}")
                    print(f"  node states: {colors}")
                return True

    if verbose:
        print(f"  無環 (DAG)")
    return False

# =============================================================================
# Section 3: Union-Find (並查集) 基礎
# =============================================================================
# 核心觀念: 解決「A 和 B 是否在同一組？」
#   union(A,B) = 合併群組, find(A) = 找群組代表, find(A)==find(B) → 同組
# 兩個優化:
#   1. Path Compression (路徑壓縮): find 時把路徑上節點直接指向 root → O(1)
#   2. Union by Rank (按秩合併): 矮的樹接到高的下面 → 避免退化成鏈表
# 時間: 幾乎 O(1) per operation (amortized O(α(n)))

class UnionFind:
    """
    Union-Find (Disjoint Set Union) 資料結構。

    支援：
      - find(x): 找 x 的 root，帶路徑壓縮
      - union(x, y): 合併 x 和 y 的集合，帶 rank 優化
      - connected(x, y): x 和 y 是否同組
    """

    def __init__(self, n: int, verbose: bool = False):
        self.parent = list(range(n))  # 每個節點的父節點，初始指向自己
        self.rank = [0] * n           # 每個節點的秩（樹高的上界）
        self.count = n                # 連通分量數
        self.verbose = verbose

        if verbose:
            print(f"  初始化 UnionFind(n={n})")
            print(f"    parent = {self.parent}")
            print(f"    rank   = {self.rank}")
            print(f"    連通分量數 = {self.count}")

    def find(self, x: int) -> int:
        """
        找 x 的 root (代表元素)，帶路徑壓縮 (path compression)。

        路徑壓縮的效果：
          find(3): 3 → 2 → 1 → 0(root)
          壓縮後:  3 → 0, 2 → 0, 1 → 0  (全部直接指向 root)
        """
        if self.verbose:
            # 記錄找 root 的路徑
            path = [x]
            curr = x
            while self.parent[curr] != curr:
                curr = self.parent[curr]
                path.append(curr)
            if len(path) > 1:
                print(f"    find({x}): 路徑 "
                      f"{'→'.join(map(str, path))}, root={curr}")

        # 遞迴版路徑壓縮
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        合併 x 和 y 所在的集合。回傳是否真的合併了（False = 已經同組）。
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            if self.verbose:
                print(f"    union({x},{y}): 已在同一組 "
                      f"(root={root_x})，跳過")
            return False  # 已經在同一組

        # Union by Rank: 矮的接到高的下面
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            if self.verbose:
                print(f"    union({x},{y}): rank[{root_x}]={self.rank[root_x]}"
                      f" < rank[{root_y}]={self.rank[root_y]}, "
                      f"{root_x}→{root_y}")
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            if self.verbose:
                print(f"    union({x},{y}): rank[{root_x}]={self.rank[root_x]}"
                      f" > rank[{root_y}]={self.rank[root_y]}, "
                      f"{root_y}→{root_x}")
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            if self.verbose:
                print(f"    union({x},{y}): rank 相同={self.rank[root_y]}, "
                      f"{root_y}→{root_x}, rank[{root_x}]→"
                      f"{self.rank[root_x]}")

        self.count -= 1
        if self.verbose:
            print(f"      parent = {self.parent}, rank = {self.rank}, "
                  f"連通分量數 = {self.count}")
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

# ---------------------------------------------------------------------------
# 3.2 Number of Connected Components (LeetCode 323)
# ---------------------------------------------------------------------------
def count_components(n: int, edges: List[List[int]],
                     verbose: bool = False) -> int:
    """
    計算無向圖中連通分量的數量。

    Time: O(V + E * α(V)), Space: O(V)
    """
    if verbose:
        print(f"  節點數: {n}, 邊: {edges}")

    uf = UnionFind(n, verbose=verbose)

    for u, v in edges:
        if verbose:
            print(f"  --- 處理邊 ({u},{v}) ---")
        uf.union(u, v)

    if verbose:
        print(f"  最終 parent = {uf.parent}")
        print(f"  連通分量數 = {uf.count}")
    return uf.count

# ---------------------------------------------------------------------------
# 3.3 Redundant Connection (LeetCode 684)
# ---------------------------------------------------------------------------
def find_redundant_connection(edges: List[List[int]],
                              verbose: bool = False) -> List[int]:
    """
    在一棵樹上多加了一條邊，找出這條多餘的邊。
    回傳最後一條會造成環的邊。

    觀念：依序加邊，如果 union 回傳 False（已在同組）→ 這就是多餘的邊！

    Time: O(E * α(V)), Space: O(V)
    """
    n = len(edges)

    if verbose:
        print(f"  邊數: {n}, 邊: {edges}")

    uf = UnionFind(n + 1, verbose=verbose)  # 節點從 1 開始

    for u, v in edges:
        if verbose:
            print(f"  --- 加邊 ({u},{v}) ---")
        if not uf.union(u, v):
            if verbose:
                print(f"  多餘的邊! ({u},{v}) 讓 {u} 和 {v} "
                      f"形成環 (已在同一組)")
            return [u, v]

    return []  # 不應該到這裡

# =============================================================================
# Section 4: Union-Find 進階
# =============================================================================

# ---------------------------------------------------------------------------
# 4.1 Accounts Merge (LeetCode 721)
# ---------------------------------------------------------------------------
def accounts_merge(accounts: List[List[str]],
                   verbose: bool = False) -> List[List[str]]:
    """
    合併帳號：如果兩個帳號有相同的 email，就合併。

    思路：
      1. 每個 email 映射到一個 id
      2. 同一個帳號內的 emails 全部 union
      3. 最後用 find 把同組的 emails 收集在一起

    Time: O(N * α(N)), N = email 總數, Space: O(N)
    """
    email_to_id = {}   # email → 數字 id
    email_to_name = {} # email → 帳號名稱
    next_id = 0

    if verbose:
        print(f"  帳號列表:")
        for i, acc in enumerate(accounts):
            print(f"    帳號 {i}: {acc}")

    # Step 1: 分配 id
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_id:
                email_to_id[email] = next_id
                next_id += 1
            email_to_name[email] = name

    if verbose:
        print(f"  email → id: {email_to_id}")

    # Step 2: Union 同帳號的 emails
    uf = UnionFind(next_id, verbose=verbose)

    for account in accounts:
        first_email = account[1]
        for email in account[2:]:
            if verbose:
                print(f"  union('{first_email}'[id={email_to_id[first_email]}]"
                      f", '{email}'[id={email_to_id[email]}])")
            uf.union(email_to_id[first_email], email_to_id[email])

    # Step 3: 用 find 收集同組 emails
    groups = defaultdict(list)
    for email, eid in email_to_id.items():
        root = uf.find(eid)
        groups[root].append(email)

    # Step 4: 組裝結果
    result = []
    for root, emails in groups.items():
        emails.sort()
        # 隨便挑一個 email 找名字
        name = email_to_name[emails[0]]
        result.append([name] + emails)

    result.sort()

    if verbose:
        print(f"  合併結果:")
        for r in result:
            print(f"    {r}")
    return result

# ---------------------------------------------------------------------------
# 4.2 Number of Provinces (LeetCode 547)
# ---------------------------------------------------------------------------
def find_num_provinces(is_connected: List[List[int]],
                       verbose: bool = False) -> int:
    """
    給定 n×n 鄰接矩陣，計算省份（連通分量）數量。

    Time: O(n^2 * α(n)), Space: O(n)
    """
    n = len(is_connected)

    if verbose:
        print(f"  城市數: {n}")
        print(f"  鄰接矩陣:")
        for i, row in enumerate(is_connected):
            print(f"    city {i}: {row}")

    uf = UnionFind(n, verbose=verbose)

    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j] == 1:
                if verbose:
                    print(f"  --- city {i} 和 city {j} 相連 ---")
                uf.union(i, j)

    if verbose:
        print(f"  省份數 = {uf.count}")
    return uf.count

# ---------------------------------------------------------------------------
# 4.3 Smallest String With Swaps (LeetCode 1202)
# ---------------------------------------------------------------------------
def smallest_string_with_swaps(s: str, pairs: List[List[int]],
                               verbose: bool = False) -> str:
    """
    給定字串 s 和可交換的 index pairs，回傳字典序最小的字串。

    觀念：同一組（connected component）內的字元可以任意排列
    → Union-Find 找組 → 每組內排序 → 重組字串

    Time: O(n log n + n * α(n)), Space: O(n)
    """
    n = len(s)

    if verbose:
        print(f"  字串: '{s}'")
        print(f"  可交換 pairs: {pairs}")

    uf = UnionFind(n, verbose=verbose)

    for i, j in pairs:
        if verbose:
            print(f"  --- union index {i}('{s[i]}') 和 {j}('{s[j]}') ---")
        uf.union(i, j)

    # 把同組的 index 收集在一起
    groups = defaultdict(list)
    for i in range(n):
        root = uf.find(i)
        groups[root].append(i)

    if verbose:
        print(f"  分組:")
        for root, indices in groups.items():
            chars = [s[i] for i in indices]
            print(f"    root={root}: indices={indices}, chars={chars}")

    # 每組內把字元排序，分配回去
    result = list(s)
    for root, indices in groups.items():
        chars = sorted(s[i] for i in indices)
        sorted_indices = sorted(indices)
        for idx, char in zip(sorted_indices, chars):
            result[idx] = char

    answer = "".join(result)
    if verbose:
        print(f"  結果: '{answer}'")
    return answer

# =============================================================================
# Section 5: 最短路徑 (Shortest Path)
# =============================================================================
# Dijkstra: 單源最短路徑，邊權 >= 0
#   1. dist[start]=0, 其餘=INF  2. min-heap取最小節點
#   3. relaxation更新鄰居距離  4. 重複到heap空
#   Time: O((V+E) log V) with min-heap

# ---------------------------------------------------------------------------
# 5.1 Dijkstra's Algorithm — 基礎實作
# ---------------------------------------------------------------------------
def dijkstra(graph_adj: dict, start: int, n: int,
             verbose: bool = False) -> dict:
    """
    Dijkstra 最短路徑演算法。

    Args:
        graph_adj: {node: [(neighbor, weight), ...]}
        start: 起點
        n: 節點數
        verbose: 是否印出過程

    Returns:
        dist: {node: shortest_distance}

    Time: O((V+E) log V), Space: O(V+E)
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0
    visited = set()
    heap = [(0, start)]  # (distance, node)

    if verbose:
        print(f"  起點: {start}, 節點數: {n}")
        print(f"  圖: {dict(graph_adj)}")
        print(f"  初始 dist: {dist}")

    step = 0
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        step += 1

        if verbose:
            print(f"  Step {step}: pop node={u}, dist={d}, visited={visited}")

        for v, w in graph_adj.get(u, []):
            new_dist = d + w
            if new_dist < dist[v]:
                old = dist[v]
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
                if verbose:
                    old_str = "INF" if old == float('inf') else str(old)
                    print(f"    relaxation: dist[{v}] = {old_str} → {new_dist}"
                          f" (經由 {u}, 邊權重={w})")

        if verbose:
            dist_str = {k: ("INF" if v == float('inf') else v)
                        for k, v in dist.items()}
            print(f"    目前 dist: {dist_str}")

    return dist

# ---------------------------------------------------------------------------
# 5.2 Network Delay Time (LeetCode 743)
# ---------------------------------------------------------------------------
def network_delay_time(times: List[List[int]], n: int, k: int,
                       verbose: bool = False) -> int:
    """
    從節點 k 發出信號，回傳所有節點收到信號的最短時間。
    如果有節點收不到，回傳 -1。

    times[i] = [u, v, w]: 從 u 到 v 花費 w 時間。

    本質就是 Dijkstra，答案 = max(所有最短距離)。

    Time: O((V+E) log V), Space: O(V+E)
    """
    if verbose:
        print(f"  times: {times}, 節點數: {n}, 起點: {k}")

    # 建圖 (注意 LeetCode 節點從 1 開始)
    graph_adj = defaultdict(list)
    for u, v, w in times:
        graph_adj[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    visited = set()
    heap = [(0, k)]

    if verbose:
        print(f"  圖: {dict(graph_adj)}")

    step = 0
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        step += 1

        if verbose:
            print(f"  Step {step}: pop node={u}, dist={d}")

        for v, w in graph_adj[u]:
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
                if verbose:
                    print(f"    relaxation: dist[{v}] → {new_dist}"
                          f" (經由 {u}, 邊權={w})")

        if verbose:
            dist_str = {k_: ("INF" if v_ == float('inf') else v_)
                        for k_, v_ in dist.items()}
            print(f"    dist: {dist_str}")

    max_dist = max(dist.values())
    result = -1 if max_dist == float('inf') else max_dist

    if verbose:
        print(f"  最大距離: {max_dist}, 結果: {result}")
    return result

# ---------------------------------------------------------------------------
# 5.3 Cheapest Flights Within K Stops (LeetCode 787)
# ---------------------------------------------------------------------------
def find_cheapest_price(n: int, flights: List[List[int]],
                        src: int, dst: int, k: int,
                        verbose: bool = False) -> int:
    """
    找從 src 到 dst 最多經過 k 個中轉站的最便宜航班。

    方法：Modified BFS (Bellman-Ford 精神)
      - 最多做 k+1 輪 relaxation（k 個中轉 = k+1 條邊）
      - 每輪對所有邊做 relaxation

    Time: O(K * E), Space: O(V)
    """
    if verbose:
        print(f"  節點: {n}, 航班: {flights}")
        print(f"  起點: {src}, 終點: {dst}, 最多中轉: {k}")

    dist = [float('inf')] * n
    dist[src] = 0

    if verbose:
        print(f"  初始 dist: {['INF' if d == float('inf') else d for d in dist]}")

    for i in range(k + 1):  # k 個中轉 = k+1 條邊
        # 重要：用上一輪的 dist 做 relaxation，避免一輪內連鎖更新
        prev_dist = dist[:]

        updated = False
        for u, v, w in flights:
            if prev_dist[u] != float('inf') and prev_dist[u] + w < dist[v]:
                dist[v] = prev_dist[u] + w
                updated = True
                if verbose:
                    print(f"    Round {i}: edge ({u}→{v}, cost={w}), "
                          f"dist[{v}] → {dist[v]}")

        if verbose:
            dist_str = ["INF" if d == float('inf') else d for d in dist]
            print(f"  Round {i} 結束: dist = {dist_str}")

        if not updated:
            if verbose:
                print(f"  提前結束: Round {i} 無更新")
            break

    result = -1 if dist[dst] == float('inf') else dist[dst]
    if verbose:
        print(f"  結果: {result}")
    return result

# ---------------------------------------------------------------------------
# 5.4 Bellman-Ford Algorithm — 概念 + 範例
# ---------------------------------------------------------------------------
def bellman_ford(n: int, edges: List[List[int]], src: int,
                 verbose: bool = False) -> List[int]:
    """
    Bellman-Ford 最短路徑演算法。可以處理負權邊，也能偵測負環。

    步驟：
      1. 初始化 dist[src] = 0，其餘 = INF
      2. 做 n-1 輪，每輪對所有邊做 relaxation
      3. 第 n 輪如果還能更新 → 有負環 (negative cycle)

    Time: O(V * E), Space: O(V)
    比 Dijkstra 慢，但能處理負權邊。
    """
    dist = [float('inf')] * n
    dist[src] = 0

    if verbose:
        print(f"  節點數: {n}, 邊: {edges}, 起點: {src}")
        print(f"  初始 dist: {['INF' if d == float('inf') else d for d in dist]}")

    # n-1 輪 relaxation
    for i in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
                if verbose:
                    print(f"    Round {i+1}: edge ({u}→{v}, w={w}), "
                          f"dist[{v}] → {dist[v]}")

        if verbose:
            dist_str = ["INF" if d == float('inf') else d for d in dist]
            print(f"  Round {i+1} 結束: dist = {dist_str}")

        if not updated:
            if verbose:
                print(f"  提前結束: Round {i+1} 無更新")
            break

    # 檢查負環
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            if verbose:
                print(f"  偵測到負環 (negative cycle)!")
            return []  # 代表有負環

    if verbose:
        dist_str = ["INF" if d == float('inf') else d for d in dist]
        print(f"  最終 dist: {dist_str}")
    return dist

# =============================================================================
# Section 6: TopSort vs Union-Find vs Shortest Path 比較
# =============================================================================

def comparison_demo(verbose: bool = True):
    """展示三種演算法的適用場景差異。"""
    if not verbose:
        return

    print("=" * 60)
    print("Section 6: TopSort vs Union-Find vs Shortest Path 比較")
    print("=" * 60)

    print("""
┌──────────────┬───────────────────────┬──────────────────────────────┐
│   演算法      │  適用場景              │  關鍵判斷                     │
├──────────────┼───────────────────────┼──────────────────────────────┤
│ TopSort      │ 排序依賴關係的任務     │ 「順序」「先修」「依賴」      │
│ (BFS/DFS)    │ DAG 環偵測            │ 有向圖 + 排序 or 判環        │
├──────────────┼───────────────────────┼──────────────────────────────┤
│ Union-Find   │ 判斷連通性 / 分組      │ 「是否相連」「分成幾組」      │
│ (並查集)      │ 找多餘的邊            │ 無向圖 + 動態加邊            │
├──────────────┼───────────────────────┼──────────────────────────────┤
│ Dijkstra     │ 加權最短路徑           │ 「最短距離」「最小花費」      │
│              │ 非負權重              │ 有權重 >= 0                  │
├──────────────┼───────────────────────┼──────────────────────────────┤
│ Bellman-Ford │ 負權邊 / 限制步數      │ 「有負權」「最多 K 步」       │
└──────────────┴───────────────────────┴──────────────────────────────┘

面試快速判斷流程:
  題目是圖?
  ├─ 有向圖?
  │   ├─ 問順序/依賴/有沒有環 → TopSort
  │   └─ 問最短路徑 → Dijkstra / Bellman-Ford
  └─ 無向圖?
      ├─ 問連通/分組 → Union-Find
      ├─ 問最短路徑 → Dijkstra / BFS
      └─ 找多餘邊 → Union-Find

Google 常考題型:
  - Alien Dictionary → TopSort (BFS Kahn's)
  - Course Schedule → TopSort (BFS or DFS)
  - Accounts Merge → Union-Find
  - Network Delay Time → Dijkstra

NVIDIA 常考題型:
  - Number of Provinces → Union-Find
  - Course Schedule II → TopSort
  - Cheapest Flights → Bellman-Ford / Modified BFS
""")

# =============================================================================
# main() — 所有範例的集中展示
# =============================================================================
def main():
    verbose = True

    # =================================================================
    # Section 1: 拓撲排序 — BFS (Kahn's Algorithm)
    # =================================================================
    print("=" * 70)
    print("Section 1: 拓撲排序 — BFS (Kahn's Algorithm)")
    print("=" * 70)

    # --- 1.1 Course Schedule ---
    print("\n" + "-" * 60)
    print("1.1 Course Schedule — 能否修完所有課?")
    print("-" * 60)

    # Example 1: 可以修完 (無環)
    # 圖: 0→1→3, 0→2→3
    print("\n[Example 1] 4 門課, prerequisites=[[1,0],[2,0],[3,1],[3,2]]")
    print("  圖: 0→1→3, 0→2→3")
    can_finish_courses(4, [[1, 0], [2, 0], [3, 1], [3, 2]], verbose)

    # Example 2: 有環，無法修完
    # 圖: 0→1→0 (環)
    print("\n[Example 2] 2 門課, prerequisites=[[1,0],[0,1]]")
    print("  圖: 0→1→0 (環!)")
    can_finish_courses(2, [[1, 0], [0, 1]], verbose)

    # Example 3: 較大的 DAG
    # 0→1, 0→2, 1→3, 2→3, 3→4
    print("\n[Example 3] 5 門課, prerequisites=[[1,0],[2,0],[3,1],[3,2],[4,3]]")
    print("  圖: 0→1→3→4, 0→2→3")
    can_finish_courses(5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]], verbose)

    # --- 1.2 Course Schedule II ---
    print("\n" + "-" * 60)
    print("1.2 Course Schedule II — 找出修課順序")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] 4 門課, prerequisites=[[1,0],[2,0],[3,1],[3,2]]")
    find_course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]], verbose)

    # Example 2: 有環
    print("\n[Example 2] 3 門課, prerequisites=[[0,1],[1,2],[2,0]]")
    print("  圖: 0→1→2→0 (三角環!)")
    find_course_order(3, [[0, 1], [1, 2], [2, 0]], verbose)

    # Example 3: 多個獨立鏈
    print("\n[Example 3] 6 門課, prerequisites=[[1,0],[3,2],[5,4]]")
    print("  圖: 0→1, 2→3, 4→5 (三條獨立鏈)")
    find_course_order(6, [[1, 0], [3, 2], [5, 4]], verbose)

    # --- 1.3 Alien Dictionary ---
    print("\n" + "-" * 60)
    print("1.3 Alien Dictionary (Google 經典!)")
    print("-" * 60)

    # Example 1
    print('\n[Example 1] words=["wrt","wrf","er","ett","rftt"]')
    alien_order(["wrt", "wrf", "er", "ett", "rftt"], verbose)

    # Example 2: 簡單兩個字
    print('\n[Example 2] words=["z","x"]')
    alien_order(["z", "x"], verbose)

    # Example 3: 無效 (prefix 矛盾)
    print('\n[Example 3] words=["abc","ab"]')
    print("  'abc' 在 'ab' 前面，但 'ab' 是 'abc' 的 prefix → 矛盾!")
    alien_order(["abc", "ab"], verbose)

    # =================================================================
    # Section 2: 拓撲排序 — DFS
    # =================================================================
    print("\n" + "=" * 70)
    print("Section 2: 拓撲排序 — DFS (三色標記法)")
    print("=" * 70)

    # --- 2.1 Course Schedule DFS ---
    print("\n" + "-" * 60)
    print("2.1 Course Schedule — DFS Approach")
    print("-" * 60)

    # Example 1: 無環
    print("\n[Example 1] 4 門課, prerequisites=[[1,0],[2,0],[3,1],[3,2]]")
    print("  期望: True (可修完)")
    can_finish_dfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]], verbose)

    # Example 2: 有環
    print("\n[Example 2] 3 門課, prerequisites=[[0,1],[1,2],[2,0]]")
    print("  圖: 0→1→2→0 (三角環!), 期望: False")
    can_finish_dfs(3, [[0, 1], [1, 2], [2, 0]], verbose)

    # Example 3: 兩個連通分量
    print("\n[Example 3] 4 門課, prerequisites=[[1,0],[3,2]]")
    print("  圖: 0→1, 2→3 (兩條獨立鏈), 期望: True")
    can_finish_dfs(4, [[1, 0], [3, 2]], verbose)

    # --- 2.2 BFS vs DFS 比較 ---
    print("\n" + "-" * 60)
    print("2.2 Kahn's BFS vs DFS 拓撲排序 比較")
    print("-" * 60)
    print("""
  ┌──────────────┬──────────────────────┬──────────────────────────┐
  │              │ Kahn's BFS            │ DFS 三色標記             │
  ├──────────────┼──────────────────────┼──────────────────────────┤
  │ 資料結構      │ Queue + indegree[]    │ Stack (遞迴) + color[]  │
  │ 環偵測        │ count < V             │ 碰到 GRAY               │
  │ 拓撲序取得    │ Queue 出來的順序       │ reverse postorder      │
  │ 優點         │ 直覺，容易實作         │ 環偵測更直觀             │
  │ 面試偏好      │ Google 面試常見       │ 適合需要環路徑的場景     │
  └──────────────┴──────────────────────┴──────────────────────────┘
  結論: 面試首選 Kahn's BFS (較直覺)，DFS 用在需要環路徑時。
""")

    # --- 2.3 Cycle Detection ---
    print("-" * 60)
    print("2.3 Cycle Detection in Directed Graph")
    print("-" * 60)

    # Example 1: 有環
    print("\n[Example 1] 4 nodes, edges=[[0,1],[1,2],[2,0],[2,3]]")
    print("  圖: 0→1→2→0 (環), 2→3")
    has_cycle_directed(4, [[0, 1], [1, 2], [2, 0], [2, 3]], verbose)

    # Example 2: 無環 (DAG)
    print("\n[Example 2] 4 nodes, edges=[[0,1],[0,2],[1,3],[2,3]]")
    print("  圖: 0→1→3, 0→2→3 (DAG)")
    has_cycle_directed(4, [[0, 1], [0, 2], [1, 3], [2, 3]], verbose)

    # Example 3: 自環
    print("\n[Example 3] 3 nodes, edges=[[0,1],[1,1],[1,2]]")
    print("  圖: 0→1→1 (自環!), 1→2")
    has_cycle_directed(3, [[0, 1], [1, 1], [1, 2]], verbose)

    # =================================================================
    # Section 3: Union-Find 基礎
    # =================================================================
    print("\n" + "=" * 70)
    print("Section 3: Union-Find (並查集) 基礎")
    print("=" * 70)

    # --- 3.1 Union-Find 視覺化教學 ---
    print("\n" + "-" * 60)
    print("3.1 Union-Find 操作: find() + union() 完整 trace")
    print("-" * 60)

    print("\n[教學 Demo] 5 個節點 (0~4)")
    print("  依序做: union(0,1), union(2,3), union(0,2), find(3)")
    print()

    uf_demo = UnionFind(5, verbose=True)
    print()
    print("  --- union(0, 1) ---")
    uf_demo.union(0, 1)
    print()
    print("  --- union(2, 3) ---")
    uf_demo.union(2, 3)
    print()
    print("  --- union(0, 2): 合併兩個小組 ---")
    uf_demo.union(0, 2)
    print()
    print("  --- find(3): 路徑壓縮 ---")
    root = uf_demo.find(3)
    print(f"    find(3) = {root}")
    print(f"    壓縮後 parent = {uf_demo.parent}")
    print()
    print("  --- connected(1, 3)? ---")
    print(f"    connected(1, 3) = {uf_demo.connected(1, 3)}")
    print(f"    connected(1, 4) = {uf_demo.connected(1, 4)}")

    # --- 3.2 Number of Connected Components ---
    print("\n" + "-" * 60)
    print("3.2 Number of Connected Components")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] n=5, edges=[[0,1],[1,2],[3,4]]")
    print("  圖: 0-1-2, 3-4 → 2 個連通分量")
    count_components(5, [[0, 1], [1, 2], [3, 4]], verbose)

    # Example 2: 全部相連
    print("\n[Example 2] n=4, edges=[[0,1],[1,2],[2,3]]")
    print("  圖: 0-1-2-3 → 1 個連通分量")
    count_components(4, [[0, 1], [1, 2], [2, 3]], verbose)

    # Example 3: 全部獨立
    print("\n[Example 3] n=4, edges=[]")
    print("  圖: 0, 1, 2, 3 (各自獨立) → 4 個連通分量")
    count_components(4, [], verbose)

    # --- 3.3 Redundant Connection ---
    print("\n" + "-" * 60)
    print("3.3 Redundant Connection — 找出多餘的邊")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] edges=[[1,2],[1,3],[2,3]]")
    print("  樹: 1-2, 1-3, 多餘邊: 2-3 (加了就有環)")
    find_redundant_connection([[1, 2], [1, 3], [2, 3]], verbose)

    # Example 2
    print("\n[Example 2] edges=[[1,2],[2,3],[3,4],[1,4],[1,5]]")
    print("  樹: 1-2-3-4, 1-5, 多餘邊: 1-4")
    find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],
                              verbose)

    # Example 3
    print("\n[Example 3] edges=[[1,2],[3,4],[2,3],[1,4]]")
    print("  樹: 1-2, 3-4, 2-3, 多餘邊: 1-4 (加了就有環)")
    find_redundant_connection([[1, 2], [3, 4], [2, 3], [1, 4]], verbose)

    # =================================================================
    # Section 4: Union-Find 進階
    # =================================================================
    print("\n" + "=" * 70)
    print("Section 4: Union-Find 進階")
    print("=" * 70)

    # --- 4.1 Accounts Merge ---
    print("\n" + "-" * 60)
    print("4.1 Accounts Merge")
    print("-" * 60)

    # Example 1
    print("\n[Example 1]")
    accounts1 = [
        ["John", "john1@mail.com", "john_ai@mail.com"],
        ["John", "john2@mail.com"],
        ["John", "john1@mail.com", "john2@mail.com"],
        ["Mary", "mary@mail.com"]
    ]
    accounts_merge(accounts1, verbose)

    # Example 2: 沒有可合併的
    print("\n[Example 2]")
    accounts2 = [
        ["Alice", "a@b.com"],
        ["Bob", "c@d.com"],
        ["Carol", "e@f.com"]
    ]
    accounts_merge(accounts2, verbose)

    # Example 3: 全部同一人
    print("\n[Example 3]")
    accounts3 = [
        ["Tom", "t1@m.com", "t2@m.com"],
        ["Tom", "t2@m.com", "t3@m.com"],
        ["Tom", "t3@m.com", "t4@m.com"]
    ]
    accounts_merge(accounts3, verbose)

    # --- 4.2 Number of Provinces ---
    print("\n" + "-" * 60)
    print("4.2 Number of Provinces")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] 3 城市, 0-1 相連, 2 獨立")
    find_num_provinces([[1, 1, 0], [1, 1, 0], [0, 0, 1]], verbose)

    # Example 2: 全部相連
    print("\n[Example 2] 3 城市, 全部相連")
    find_num_provinces([[1, 1, 1], [1, 1, 1], [1, 1, 1]], verbose)

    # Example 3: 全部獨立
    print("\n[Example 3] 3 城市, 全部獨立")
    find_num_provinces([[1, 0, 0], [0, 1, 0], [0, 0, 1]], verbose)

    # --- 4.3 Smallest String With Swaps ---
    print("\n" + "-" * 60)
    print("4.3 Smallest String With Swaps")
    print("-" * 60)

    # Example 1
    print('\n[Example 1] s="dcab", pairs=[[0,3],[1,2]]')
    print("  index 0,3 同組(d,b)→排序=b,d; index 1,2 同組(c,a)→排序=a,c")
    smallest_string_with_swaps("dcab", [[0, 3], [1, 2]], verbose)

    # Example 2
    print('\n[Example 2] s="dcab", pairs=[[0,3],[1,2],[0,2]]')
    print("  所有 index 同組(d,c,a,b)→排序=a,b,c,d")
    smallest_string_with_swaps("dcab", [[0, 3], [1, 2], [0, 2]], verbose)

    # Example 3
    print('\n[Example 3] s="cba", pairs=[[0,1],[1,2]]')
    print("  所有 index 同組 → 排序")
    smallest_string_with_swaps("cba", [[0, 1], [1, 2]], verbose)

    # =================================================================
    # Section 5: 最短路徑 (Shortest Path)
    # =================================================================
    print("\n" + "=" * 70)
    print("Section 5: 最短路徑 (Shortest Path)")
    print("=" * 70)

    # --- 5.1 Dijkstra's Algorithm ---
    print("\n" + "-" * 60)
    print("5.1 Dijkstra's Algorithm — 基礎範例")
    print("-" * 60)

    # Example 1: 簡單圖
    print("\n[Example 1] 5 nodes, start=0")
    print("  圖: 0→1(4), 0→2(1), 2→1(2), 1→3(1), 2→3(5), 3→4(3)")
    g1 = defaultdict(list)
    g1[0] = [(1, 4), (2, 1)]
    g1[2] = [(1, 2), (3, 5)]
    g1[1] = [(3, 1)]
    g1[3] = [(4, 3)]
    result = dijkstra(g1, 0, 5, verbose)
    print(f"  最終最短距離: {result}")

    # Example 2: 有多條路徑
    print("\n[Example 2] 4 nodes, start=0")
    print("  圖: 0→1(1), 0→2(4), 1→2(2), 1→3(6), 2→3(3)")
    g2 = defaultdict(list)
    g2[0] = [(1, 1), (2, 4)]
    g2[1] = [(2, 2), (3, 6)]
    g2[2] = [(3, 3)]
    result = dijkstra(g2, 0, 4, verbose)
    print(f"  最終最短距離: {result}")

    # Example 3: 不連通
    print("\n[Example 3] 3 nodes, start=0, node 2 不可達")
    print("  圖: 0→1(5)")
    g3 = defaultdict(list)
    g3[0] = [(1, 5)]
    result = dijkstra(g3, 0, 3, verbose)
    print(f"  最終最短距離: {result}")

    # --- 5.2 Network Delay Time ---
    print("\n" + "-" * 60)
    print("5.2 Network Delay Time (LeetCode 743)")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2")
    print("  圖: 2→1(1), 2→3(1), 3→4(1)")
    network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, verbose)

    # Example 2
    print("\n[Example 2] times=[[1,2,1]], n=2, k=1")
    network_delay_time([[1, 2, 1]], 2, 1, verbose)

    # Example 3: 有節點不可達
    print("\n[Example 3] times=[[1,2,1]], n=2, k=2")
    print("  從 node 2 出發，node 1 不可達")
    network_delay_time([[1, 2, 1]], 2, 2, verbose)

    # --- 5.3 Cheapest Flights Within K Stops ---
    print("\n" + "-" * 60)
    print("5.3 Cheapest Flights Within K Stops (LeetCode 787)")
    print("-" * 60)

    # Example 1
    print("\n[Example 1] n=4, flights=[[0,1,100],[1,2,100],[2,3,100],[0,3,500]]")
    print("  src=0, dst=3, k=1")
    print("  直飛 0→3 要 500，轉一次 0→1→2→3 要 300 但需 2 個中轉")
    print("  k=1 只能轉一次，所以 0→1→... 不夠，答案=500")
    find_cheapest_price(4,
                        [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 3, 500]],
                        0, 3, 1, verbose)

    # Example 2: k=2 就可以更便宜
    print("\n[Example 2] 同上但 k=2")
    find_cheapest_price(4,
                        [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 3, 500]],
                        0, 3, 2, verbose)

    # Example 3
    print("\n[Example 3] n=3, flights=[[0,1,100],[1,2,100],[0,2,500]]")
    print("  src=0, dst=2, k=1")
    find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
                        0, 2, 1, verbose)

    # --- 5.4 Bellman-Ford ---
    print("\n" + "-" * 60)
    print("5.4 Bellman-Ford Algorithm (可處理負權邊)")
    print("-" * 60)

    print("  Bellman-Ford vs Dijkstra:")
    print("    Dijkstra: O((V+E)logV), 不支援負權, 非負權最短路徑")
    print("    Bellman-Ford: O(V*E), 支援負權+負環偵測, 有負權/限制步數")

    # Example 1: 有負權邊
    print("[Example 1] 5 nodes, edges with negative weight")
    print("  邊: 0→1(6), 0→2(7), 1→2(8), 1→3(5), 1→4(-4), 2→3(-3), "
          "2→4(9), 3→1(-2), 4→3(7)")
    edges_bf = [
        [0, 1, 6], [0, 2, 7], [1, 2, 8], [1, 3, 5],
        [1, 4, -4], [2, 3, -3], [2, 4, 9], [3, 1, -2], [4, 3, 7]
    ]
    bellman_ford(5, edges_bf, 0, verbose)

    # Section 6: 比較總結
    comparison_demo(verbose)

    # 結語
    print("=" * 70)
    print("恭喜! 你已完成 Graph TopSort + Union-Find + Shortest Path!")
    print("=" * 70)
    print("""
  學習 checklist:
    [x] Kahn's BFS 拓撲排序 — 用 indegree + queue
    [x] DFS 拓撲排序 — 三色標記法 (WHITE/GRAY/BLACK)
    [x] 環偵測 — BFS 看 count < V / DFS 看 GRAY
    [x] Union-Find — find(路徑壓縮) + union(按秩合併)
    [x] Union-Find 應用 — 連通分量、多餘邊、帳號合併、字串交換
    [x] Dijkstra — min-heap + relaxation (非負權)
    [x] Bellman-Ford — V-1 輪 relaxation (可負權)
    [x] 何時用哪個演算法 — 看「有向/無向」+「問什麼」

  下一步建議:
    → 11_Graph_Shortest_Path.py (Floyd-Warshall, 更多最短路徑變形)
    → 12_DP_1D.py (動態規劃，面試重點!)
""")

if __name__ == "__main__":
    main()
