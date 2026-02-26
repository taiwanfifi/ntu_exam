# 白板 Coding 模板速查｜45 Templates for Whiteboard Interviews

> 面試前 30 分鐘速查。每個模板 = 最精簡可執行碼 + 一句話用途 + 複雜度。
> 背熟這些骨架，上場只需填入題目邏輯。

---

## A. 基礎資料結構模板

---

### Template 1: HashMap One-Pass (Two Sum Pattern)

📌 用途：在 array 中找兩數滿足某條件，一次遍歷完成
⏱ 複雜度：Time O(n), Space O(n)
🔑 關鍵：邊查邊存，用 complement 當 key

```python
def two_sum(nums, target):
    seen = {}                        # val -> index
    for i, num in enumerate(nums):
        comp = target - num          # 計算互補值
        if comp in seen:             # 之前見過 → 找到答案
            return [seen[comp], i]
        seen[num] = i                # 存起來給後面的數查
    return []
```

適用題目：LC 1, LC 167, LC 653

---

### Template 2: HashMap Frequency Count

📌 用途：統計元素出現次數，找眾數 / top-k / 重複
⏱ 複雜度：Time O(n), Space O(n)
🔑 關鍵：Counter 是最常用的面試工具之一

```python
from collections import Counter

def freq_pattern(nums):
    count = Counter(nums)            # {val: freq}
    # 或手動：
    # count = {}
    # for x in nums:
    #     count[x] = count.get(x, 0) + 1
    for val, freq in count.items():
        if freq > len(nums) // 2:    # 依題意判斷
            return val
```

適用題目：LC 169, LC 347, LC 451

---

### Template 3: HashSet Dedup

📌 用途：去重 / O(1) 查存在性 / 找交集差集
⏱ 複雜度：Time O(n), Space O(n)
🔑 關鍵：set 的 in 操作是 O(1)

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:              # O(1) 查詢
            return True
        seen.add(num)
    return False
```

適用題目：LC 217, LC 128, LC 349

---

### Template 4: Stack — Matching Pattern

📌 用途：括號匹配 / 巢狀結構驗證
⏱ 複雜度：Time O(n), Space O(n)
🔑 關鍵：遇到開括號 push，遇到閉括號 pop 比對

```python
def is_valid(s):
    stack = []
    match = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in match:               # 閉括號
            if not stack or stack[-1] != match[c]:
                return False
            stack.pop()
        else:
            stack.append(c)          # 開括號 push
    return len(stack) == 0           # 全部配對完
```

適用題目：LC 20, LC 32, LC 71

---

### Template 5: Monotonic Stack — Next Greater Element

📌 用途：對每個元素找右邊（或左邊）第一個更大/更小的值
⏱ 複雜度：Time O(n), Space O(n)
🔑 關鍵：stack 存 index，維持單調遞減（找 next greater）

```python
def next_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []                       # 存 index，對應值單調遞減
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()        # nums[i] 是 idx 的 next greater
            res[idx] = nums[i]
        stack.append(i)
    return res
```

適用題目：LC 496, LC 503, LC 739, LC 84

---

### Template 6: Min Heap / Max Heap

📌 用途：動態取最小/最大值、Top-K 問題
⏱ 複雜度：push/pop O(log n)
🔑 關鍵：Python heapq 是 min heap；max heap 用負號

```python
import heapq

# --- Min Heap ---
min_heap = []
heapq.heappush(min_heap, val)
smallest = heapq.heappop(min_heap)

# --- Max Heap（取負） ---
max_heap = []
heapq.heappush(max_heap, -val)
largest = -heapq.heappop(max_heap)

# --- Top K Smallest ---
def top_k_smallest(nums, k):
    return heapq.nsmallest(k, nums)

# --- Top K Largest（用 size-k min heap） ---
def top_k_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)              # O(k)
    for num in nums[k:]:
        if num > heap[0]:            # 比堆頂大才換
            heapq.heapreplace(heap, num)
    return heap
```

適用題目：LC 215, LC 347, LC 295, LC 373

---

### Template 7: Deque — Sliding Window Maximum

📌 用途：滑動窗口內的最大/最小值
⏱ 複雜度：Time O(n), Space O(k)
🔑 關鍵：deque 存 index，維持單調遞減，隊首就是窗口最大

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()                     # 存 index，值單調遞減
    res = []
    for i in range(len(nums)):
        while dq and nums[i] >= nums[dq[-1]]:
            dq.pop()                 # 移除比當前小的（沒用了）
        dq.append(i)
        if dq[0] <= i - k:          # 隊首超出窗口範圍
            dq.popleft()
        if i >= k - 1:              # 窗口形成後開始收集
            res.append(nums[dq[0]])
    return res
```

適用題目：LC 239

---

### Template 8: Trie (Prefix Tree)

📌 用途：前綴搜尋 / 自動補全 / 字典查詢
⏱ 複雜度：insert/search O(L)，L = 字串長度
🔑 關鍵：每個節點是 dict of children + is_end flag

```python
class TrieNode:
    def __init__(self):
        self.children = {}           # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True           # 標記字尾

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._find(prefix) is not None

    def _find(self, s):
        node = self.root
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
```

適用題目：LC 208, LC 211, LC 212

---

### Template 9: Union-Find (Disjoint Set)

📌 用途：動態連通性 / 判斷環 / 計算連通分量數
⏱ 複雜度：近 O(1) per operation（均攤）
🔑 關鍵：path compression + union by rank

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n               # 連通分量數

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False             # 已連通 → 有環
        if self.rank[px] < self.rank[py]:
            px, py = py, px          # rank 大的當 parent
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        return True
```

適用題目：LC 200, LC 547, LC 684, LC 323

---

### Template 10: Linked List Reversal

📌 用途：反轉整條或部分鏈表
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：三指針 prev/curr/next，逐一翻轉指向

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next              # 先存下一個
        curr.next = prev             # 翻轉指向
        prev = curr                  # prev 前進
        curr = nxt                   # curr 前進
    return prev                      # prev 是新頭
```

適用題目：LC 206, LC 92, LC 25, LC 234

---

## B. 搜尋模板（Binary Search）

---

### Template 11: Binary Search — Standard (left <= right)

📌 用途：在排序陣列中找精確值
⏱ 複雜度：Time O(log n), Space O(1)
🔑 關鍵：left <= right，找到就返回，找不到返回 -1

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:                  # 搜索區間 [lo, hi]
        mid = lo + (hi - lo) // 2   # 防溢位
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

適用題目：LC 704, LC 33, LC 74

---

### Template 12: Binary Search — Find Left Bound (left < right)

📌 用途：找第一個 >= target 的位置（lower bound）
⏱ 複雜度：Time O(log n), Space O(1)
🔑 關鍵：left < right，收縮到唯一位置，不提前返回

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)           # 注意 hi = len(nums)
    while lo < hi:                   # 搜索區間 [lo, hi)
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1             # mid 不可能是答案
        else:
            hi = mid                 # mid 可能是答案，保留
    return lo                        # lo == hi 就是插入點
```

適用題目：LC 34, LC 35, LC 278

---

### Template 13: Binary Search — Template 3 (left + 1 < right)

📌 用途：需要比較鄰居的場景（peak / valley）
⏱ 複雜度：Time O(log n), Space O(1)
🔑 關鍵：結束時 lo+1==hi，兩個候選人都要檢查

```python
def search_template3(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo + 1 < hi:              # 保證 lo 和 hi 不相鄰
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid                 # 不 +1，因為 mid 可能是答案
        else:
            hi = mid
    # 結束後檢查 lo 和 hi
    if nums[lo] == target: return lo
    if nums[hi] == target: return hi
    return -1
```

適用題目：LC 162, LC 153

---

### Template 14: Binary Search on Answer

📌 用途：答案有單調性時，二分搜答案本身
⏱ 複雜度：Time O(n log(range)), Space O(1)
🔑 關鍵：定義 feasible(mid) 判斷 mid 是否可行

```python
def binary_search_on_answer(nums, threshold):
    lo, hi = min(nums), max(nums)    # 答案的可能範圍
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):            # mid 可行 → 嘗試更小的
            hi = mid
        else:
            lo = mid + 1
    return lo

def feasible(mid):
    # 依題意實作：mid 當作答案，判斷是否滿足條件
    pass
```

適用題目：LC 875, LC 1011, LC 410

---

## C. 雙指針模板

---

### Template 15: Two Pointers — Opposite Direction

📌 用途：排序陣列上從兩端夾擊（two sum sorted / 容器盛水）
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：依據比較結果決定移動哪端

```python
def two_pointer_opposite(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1                  # 太小 → 左指針右移
        else:
            hi -= 1                  # 太大 → 右指針左移
    return []
```

適用題目：LC 167, LC 11, LC 42, LC 15

---

### Template 16: Two Pointers — Same Direction (Remove Duplicates)

📌 用途：原地移除 / 去重 / 移動元素
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：slow 指向下一個要寫入的位置，fast 掃描全部

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0                         # slow 指向最後一個保留的位置
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]: # 發現新值
            slow += 1
            nums[slow] = nums[fast]  # 寫入
    return slow + 1
```

適用題目：LC 26, LC 27, LC 283, LC 80

---

### Template 17: Fast-Slow Pointers (Floyd's Cycle Detection)

📌 用途：鏈表找環 / 找環入口 / 找中點
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：slow 走 1 步、fast 走 2 步，相遇即有環

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next             # 走 1 步
        fast = fast.next.next        # 走 2 步
        if slow == fast:
            return True              # 相遇 → 有環
    return False

def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head              # 重置 slow 到頭
            while slow != fast:
                slow = slow.next
                fast = fast.next     # 都走 1 步
            return slow              # 相遇點就是環入口
    return None
```

適用題目：LC 141, LC 142, LC 287, LC 876

---

## D. 滑動窗口模板

---

### Template 18: Fixed Size Window

📌 用途：固定長度 k 的窗口統計（平均值 / 最大和）
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：窗口滿了後，加右減左同步進行

```python
def fixed_window(nums, k):
    window_sum = sum(nums[:k])       # 初始窗口
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i]        # 加入右邊新元素
        window_sum -= nums[i - k]    # 移除左邊舊元素
        best = max(best, window_sum)
    return best
```

適用題目：LC 643, LC 1456

---

### Template 19: Variable Window — Find Shortest

📌 用途：找滿足條件的最短子陣列
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：條件滿足時 shrink left，記錄最小長度

```python
def min_window_size(nums, target):
    left = 0
    curr_sum = 0
    best = float('inf')
    for right in range(len(nums)):
        curr_sum += nums[right]      # 擴大窗口
        while curr_sum >= target:    # 條件滿足 → 收縮
            best = min(best, right - left + 1)
            curr_sum -= nums[left]
            left += 1
    return best if best != float('inf') else 0
```

適用題目：LC 209, LC 76

---

### Template 20: Variable Window — Find Longest

📌 用途：找滿足條件的最長子陣列/子字串
⏱ 複雜度：Time O(n), Space O(k)
🔑 關鍵：條件違反時 shrink left，否則一直擴大

```python
def max_window_size(s, k):
    left = 0
    window = {}                      # char -> count
    best = 0
    for right in range(len(s)):
        window[s[right]] = window.get(s[right], 0) + 1
        while len(window) > k:      # 違反條件 → 收縮
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

適用題目：LC 3, LC 159, LC 340, LC 424

---

### Template 21: Counter Window (Minimum Window Substring)

📌 用途：在字串中找包含所有目標字元的最短窗口
⏱ 複雜度：Time O(n), Space O(k)
🔑 關鍵：用 need counter + formed 計數追蹤匹配進度

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)                # 需要的字元及數量
    missing = len(t)                 # 還缺多少個字元
    left = 0
    best = (float('inf'), 0, 0)      # (長度, left, right)
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1             # 有效匹配
        need[c] -= 1
        while missing == 0:          # 全部匹配 → 收縮
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1         # 又缺了
            left += 1
    return s[best[1]:best[2]+1] if best[0] != float('inf') else ""
```

適用題目：LC 76, LC 567, LC 438

---

## E. Tree 模板

---

### Template 22: DFS Preorder (Root → Left → Right)

📌 用途：複製樹 / 序列化 / 前序遍歷
⏱ 複雜度：Time O(n), Space O(h)
🔑 關鍵：先處理 root，再遞迴左右

```python
# --- Recursive ---
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# --- Iterative ---
def preorder_iter(root):
    if not root:
        return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)         # 先處理
        if node.right:
            stack.append(node.right) # 右先入（後出）
        if node.left:
            stack.append(node.left)  # 左後入（先出）
    return res
```

適用題目：LC 144, LC 114

---

### Template 23: DFS Inorder (Left → Root → Right)

📌 用途：BST 中序 = 排序結果
⏱ 複雜度：Time O(n), Space O(h)
🔑 關鍵：一路走到最左，處理，再去右子樹

```python
# --- Recursive ---
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# --- Iterative ---
def inorder_iter(root):
    stack, res = [], []
    curr = root
    while curr or stack:
        while curr:                  # 一路往左走到底
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()           # 回溯
        res.append(curr.val)         # 處理
        curr = curr.right            # 轉向右子樹
    return res
```

適用題目：LC 94, LC 230, LC 98

---

### Template 24: DFS Postorder (Left → Right → Root)

📌 用途：刪除樹 / 計算高度 / 後序遍歷
⏱ 複雜度：Time O(n), Space O(h)
🔑 關鍵：先處理子樹，最後處理 root

```python
# --- Recursive ---
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# --- Iterative（前序反轉法：root→right→left 再 reverse） ---
def postorder_iter(root):
    if not root:
        return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.left:
            stack.append(node.left)  # 左先入
        if node.right:
            stack.append(node.right) # 右後入
    return res[::-1]                 # 反轉 → 後序
```

適用題目：LC 145, LC 104, LC 543

---

### Template 25: BFS Level Order Traversal

📌 用途：層序遍歷 / 最短路徑 / 逐層處理
⏱ 複雜度：Time O(n), Space O(w)，w = 最大寬度
🔑 關鍵：用 queue，每層用 for loop 處理固定數量

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    queue = deque([root])
    res = []
    while queue:
        level = []
        for _ in range(len(queue)):  # 這一層有幾個就處理幾個
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
```

適用題目：LC 102, LC 103, LC 107, LC 199

---

### Template 26: BST Validate (Range Check)

📌 用途：驗證二元搜尋樹 / BST 性質判斷
⏱ 複雜度：Time O(n), Space O(h)
🔑 關鍵：每個節點帶上合法的 (min, max) 範圍

```python
def is_valid_bst(root):
    def helper(node, lo, hi):
        if not node:
            return True
        if node.val <= lo or node.val >= hi:
            return False             # 超出合法範圍
        return (helper(node.left, lo, node.val) and   # 左子樹 < node
                helper(node.right, node.val, hi))      # 右子樹 > node
    return helper(root, float('-inf'), float('inf'))
```

適用題目：LC 98, LC 700, LC 450

---

## F. Graph 模板

---

### Template 27: DFS on Adjacency List

📌 用途：圖的連通性 / 路徑搜尋 / 連通分量
⏱ 複雜度：Time O(V+E), Space O(V)
🔑 關鍵：visited set 防止重複訪問

```python
def dfs_graph(graph, start):
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:     # graph = {node: [neighbors]}
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return visited
```

適用題目：LC 133, LC 323, LC 547

---

### Template 28: BFS on Adjacency List

📌 用途：最短路徑（無權圖）/ 層序處理
⏱ 複雜度：Time O(V+E), Space O(V)
🔑 關鍵：queue + visited，第一次到達就是最短

```python
from collections import deque

def bfs_graph(graph, start, target):
    queue = deque([start])
    visited = {start}
    steps = 0
    while queue:
        for _ in range(len(queue)):      # 逐層
            node = queue.popleft()
            if node == target:
                return steps
            for nei in graph[node]:
                if nei not in visited:
                    visited.add(nei)
                    queue.append(nei)
        steps += 1
    return -1
```

適用題目：LC 127, LC 752, LC 863

---

### Template 29: DFS on Grid (4-Directional)

📌 用途：島嶼問題 / flood fill / 連通區域
⏱ 複雜度：Time O(m*n), Space O(m*n)
🔑 關鍵：4 方向 + 邊界檢查 + 標記已訪問

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return                       # 越界
        if grid[r][c] != '1':
            return                       # 水或已訪問
        grid[r][c] = '0'                 # 標記已訪問
        dfs(r+1, c)                      # 下
        dfs(r-1, c)                      # 上
        dfs(r, c+1)                      # 右
        dfs(r, c-1)                      # 左

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

適用題目：LC 200, LC 695, LC 733

---

### Template 30: BFS on Grid

📌 用途：grid 上最短路徑 / 多源 BFS
⏱ 複雜度：Time O(m*n), Space O(m*n)
🔑 關鍵：queue 存座標，visited 用 set 或改 grid 值

```python
from collections import deque

def shortest_path_grid(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(0, 0, 0)])           # (row, col, dist)
    visited = {(0, 0)}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        r, c, dist = queue.popleft()
        if r == rows-1 and c == cols-1:
            return dist                  # 到達終點
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited and grid[nr][nc] == 0:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    return -1
```

適用題目：LC 994, LC 286, LC 1091

---

### Template 31: Topological Sort (Kahn's BFS)

📌 用途：課程排序 / 任務依賴 / 檢測有向圖環
⏱ 複雜度：Time O(V+E), Space O(V+E)
🔑 關鍵：indegree 為 0 的先入 queue，BFS 逐一剝離

```python
from collections import deque, defaultdict

def topo_sort(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1

    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:       # 所有前置都完成
                queue.append(nei)
    return order if len(order) == num_courses else []  # 有環則不完整
```

適用題目：LC 207, LC 210, LC 269

---

### Template 32: Dijkstra's Algorithm

📌 用途：有權圖最短路徑（非負權重）
⏱ 複雜度：Time O((V+E) log V), Space O(V+E)
🔑 關鍵：min heap + relaxation，每個點只處理一次

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start, n):
    # graph = defaultdict(list)  # node -> [(weight, neighbor)]
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]              # (cost, node)
    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue                 # 已有更短路徑，跳過
        for w, v in graph[u]:
            if cost + w < dist[v]:
                dist[v] = cost + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

適用題目：LC 743, LC 787, LC 1514

---

## G. DP 模板

---

### Template 33: 1D DP (House Robber Pattern)

📌 用途：線性序列上的最優決策（取或不取）
⏱ 複雜度：Time O(n), Space O(1) 可優化
🔑 關鍵：dp[i] = max(dp[i-1], dp[i-2] + nums[i])

```python
def rob(nums):
    if len(nums) <= 2:
        return max(nums, default=0)
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])  # 不搶i vs 搶i
        prev2, prev1 = prev1, curr
    return prev1
```

適用題目：LC 198, LC 213, LC 70, LC 746

---

### Template 34: 2D DP (LCS / Edit Distance Pattern)

📌 用途：兩個序列的比對（最長公共子序列 / 編輯距離）
⏱ 複雜度：Time O(m*n), Space O(m*n)
🔑 關鍵：dp[i][j] 代表 s1[:i] 和 s2[:j] 的子問題答案

```python
def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1     # 匹配
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # 跳過一邊
    return dp[m][n]

# Edit Distance 框架同理，三個操作取 min：
# dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 if match else 1))
```

適用題目：LC 1143, LC 72, LC 583, LC 718

---

### Template 35: 0/1 Knapsack

📌 用途：每個物品只能用一次，求最大價值 / 是否能湊出目標
⏱ 複雜度：Time O(n*W), Space O(W)
🔑 關鍵：1D 優化時內層倒序遍歷（確保每個物品只用一次）

```python
def knapsack_01(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):  # 倒序！
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[W]

# Subset Sum 變體（能否湊出 target）：
def can_partition(nums, target):
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for t in range(target, num - 1, -1):     # 倒序
            dp[t] = dp[t] or dp[t - num]
    return dp[target]
```

適用題目：LC 416, LC 494, LC 474

---

### Template 36: Unbounded Knapsack

📌 用途：每個物品可重複使用（零錢兌換 / 完全背包）
⏱ 複雜度：Time O(n*W), Space O(W)
🔑 關鍵：內層正序遍歷（允許重複使用同一物品）

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):         # 正序！
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# 組合數（order 不重要）：外層遍歷物品，內層遍歷容量
# 排列數（order 重要）：外層遍歷容量，內層遍歷物品
```

適用題目：LC 322, LC 518, LC 377

---

### Template 37: Kadane's Algorithm (Maximum Subarray)

📌 用途：最大連續子陣列和
⏱ 複雜度：Time O(n), Space O(1)
🔑 關鍵：curr_sum 如果 < 0 就重新開始

```python
def max_subarray(nums):
    curr_sum = best = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)  # 接著加 vs 重新開始
        best = max(best, curr_sum)
    return best
```

適用題目：LC 53, LC 152（乘積版需同時追蹤 min/max）, LC 918

---

## H. Backtracking 模板

---

### Template 38: Subsets

📌 用途：列舉所有子集 / 組合
⏱ 複雜度：Time O(2^n), Space O(n)
🔑 關鍵：每個元素 選 or 不選，用 start 避免重複

```python
def subsets(nums):
    res = []
    def backtrack(start, path):
        res.append(path[:])              # 每個 path 都是合法子集
        for i in range(start, len(nums)):
            path.append(nums[i])         # 選
            backtrack(i + 1, path)       # 下一個從 i+1 開始
            path.pop()                   # 撤銷
    backtrack(0, [])
    return res

# 有重複元素版本（nums 先排序）：
# if i > start and nums[i] == nums[i-1]: continue  # 跳過重複
```

適用題目：LC 78, LC 90

---

### Template 39: Permutations

📌 用途：全排列
⏱ 複雜度：Time O(n!), Space O(n)
🔑 關鍵：用 used 陣列標記已使用的元素（或 swap）

```python
def permutations(nums):
    res = []
    used = [False] * len(nums)
    def backtrack(path):
        if len(path) == len(nums):
            res.append(path[:])          # 長度夠了 → 一組排列
            return
        for i in range(len(nums)):
            if used[i]:
                continue                 # 已使用，跳過
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()                   # 撤銷
            used[i] = False
    backtrack([])
    return res
```

適用題目：LC 46, LC 47（有重複時加排序 + 剪枝）

---

### Template 40: Combinations

📌 用途：從 n 個中選 k 個
⏱ 複雜度：Time O(C(n,k)), Space O(k)
🔑 關鍵：同 subsets 但只在 len(path)==k 時收集

```python
def combine(n, k):
    res = []
    def backtrack(start, path):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return res

# 剪枝優化：range(start, n - (k - len(path)) + 2)
```

適用題目：LC 77, LC 39, LC 40, LC 216

---

### Template 41: Grid Backtracking (N-Queens Pattern)

📌 用途：在 grid 上放置 / 搜尋所有合法配置
⏱ 複雜度：依題目而定
🔑 關鍵：逐行放置 + 用 set 追蹤衝突的列/對角線

```python
def solve_n_queens(n):
    res = []
    cols = set()                         # 已佔用的列
    diag1 = set()                        # 主對角線 (r - c)
    diag2 = set()                        # 副對角線 (r + c)

    def backtrack(r, board):
        if r == n:
            res.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue                 # 衝突，跳過
            board[r][c] = 'Q'
            cols.add(c); diag1.add(r-c); diag2.add(r+c)
            backtrack(r + 1, board)
            board[r][c] = '.'            # 撤銷
            cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)

    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, board)
    return res
```

適用題目：LC 51, LC 52, LC 37

---

## I. Sorting 模板

---

### Template 42: Merge Sort

📌 用途：穩定排序 / 計算逆序對
⏱ 複雜度：Time O(n log n), Space O(n)
🔑 關鍵：分治 — 切半 → 遞迴排序 → 合併

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res
```

適用題目：LC 912, LC 148, LC 315

---

### Template 43: Quick Sort (Lomuto Partition)

📌 用途：原地排序 / Quick Select 找第 k 大
⏱ 複雜度：Time O(n log n) avg, Space O(log n)
🔑 關鍵：選 pivot，小的放左、大的放右，遞迴

```python
import random

def quick_sort(arr, lo, hi):
    if lo >= hi:
        return
    pivot_idx = partition(arr, lo, hi)
    quick_sort(arr, lo, pivot_idx - 1)
    quick_sort(arr, pivot_idx + 1, hi)

def partition(arr, lo, hi):
    rand = random.randint(lo, hi)
    arr[rand], arr[hi] = arr[hi], arr[rand]  # 隨機 pivot 防最壞
    pivot = arr[hi]
    i = lo                                    # i = 下一個放小值的位置
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]        # pivot 歸位
    return i

# Quick Select（找第 k 小）：
# 只遞迴包含 k 的那一半 → Time O(n) avg
```

適用題目：LC 912, LC 215, LC 973

---

## J. 其他模板

---

### Template 44: Prefix Sum

📌 用途：O(1) 查詢任意區間和 / subarray sum 問題
⏱ 複雜度：Build O(n), Query O(1)
🔑 關鍵：prefix[i] = sum(nums[0..i-1])，區間和 = prefix[r+1] - prefix[l]

```python
# 建立 prefix sum
def build_prefix(nums):
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i+1] = prefix[i] + nums[i]
    return prefix
    # 區間 [l, r] 的和 = prefix[r+1] - prefix[l]

# Subarray Sum Equals K（用 HashMap 記錄 prefix sum 出現次數）
def subarray_sum(nums, k):
    count = 0
    curr_sum = 0
    prefix_count = {0: 1}                # base case
    for num in nums:
        curr_sum += num
        if curr_sum - k in prefix_count: # 存在某個前綴使得區間和 = k
            count += prefix_count[curr_sum - k]
        prefix_count[curr_sum] = prefix_count.get(curr_sum, 0) + 1
    return count
```

適用題目：LC 303, LC 560, LC 523, LC 974

---

### Template 45: Bit Manipulation Tricks

📌 用途：位元運算技巧速查
⏱ 複雜度：Time O(1) per operation
🔑 關鍵：熟記這些公式，面試直接用

```python
# 常用位元操作
n & (n - 1)        # 清除最低位的 1（判斷 2 的冪：結果 == 0）
n & (-n)           # 取出最低位的 1
n | (n + 1)        # 將最低位的 0 設為 1
n ^ n == 0         # 相同數 XOR = 0（找唯一出現一次的數）

# 計算 1 的個數 (Hamming Weight)
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)                    # 每次消掉最低位的 1
        count += 1
    return count

# 找唯一出現一次的數（其餘出現兩次）
def single_number(nums):
    res = 0
    for num in nums:
        res ^= num                       # 成對的互相消掉
    return res

# 判斷是否為 2 的冪
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

適用題目：LC 136, LC 191, LC 338, LC 231

---

## 速查索引表

| # | 模板 | 核心結構 | 典型題 |
|---|------|----------|--------|
| 1 | HashMap One-Pass | dict | LC 1 |
| 2 | Frequency Count | Counter | LC 347 |
| 3 | HashSet Dedup | set | LC 217 |
| 4 | Stack Matching | stack | LC 20 |
| 5 | Monotonic Stack | stack | LC 739 |
| 6 | Heap | heapq | LC 215 |
| 7 | Deque Window | deque | LC 239 |
| 8 | Trie | dict tree | LC 208 |
| 9 | Union-Find | parent[] | LC 684 |
| 10 | List Reversal | prev/curr | LC 206 |
| 11 | BS Standard | lo<=hi | LC 704 |
| 12 | BS Left Bound | lo<hi | LC 34 |
| 13 | BS Template 3 | lo+1<hi | LC 162 |
| 14 | BS on Answer | feasible() | LC 875 |
| 15 | 2P Opposite | lo/hi | LC 11 |
| 16 | 2P Same Dir | slow/fast | LC 26 |
| 17 | Fast-Slow | cycle | LC 141 |
| 18 | Fixed Window | sum+/-  | LC 643 |
| 19 | Var Window Short | shrink | LC 209 |
| 20 | Var Window Long | expand | LC 3 |
| 21 | Counter Window | missing | LC 76 |
| 22 | Preorder | root-L-R | LC 144 |
| 23 | Inorder | L-root-R | LC 94 |
| 24 | Postorder | L-R-root | LC 145 |
| 25 | BFS Level | queue | LC 102 |
| 26 | BST Validate | range | LC 98 |
| 27 | Graph DFS | visited | LC 133 |
| 28 | Graph BFS | queue | LC 127 |
| 29 | Grid DFS | 4-dir | LC 200 |
| 30 | Grid BFS | queue+dir | LC 994 |
| 31 | Topo Sort | indegree | LC 207 |
| 32 | Dijkstra | heap+dist | LC 743 |
| 33 | 1D DP | prev1/prev2 | LC 198 |
| 34 | 2D DP | dp[i][j] | LC 1143 |
| 35 | 0/1 Knapsack | 倒序 | LC 416 |
| 36 | Unbounded KS | 正序 | LC 322 |
| 37 | Kadane | curr/best | LC 53 |
| 38 | Subsets | start | LC 78 |
| 39 | Permutations | used[] | LC 46 |
| 40 | Combinations | start+k | LC 77 |
| 41 | Grid Backtrack | sets | LC 51 |
| 42 | Merge Sort | 分治合併 | LC 148 |
| 43 | Quick Sort | partition | LC 215 |
| 44 | Prefix Sum | prefix[] | LC 560 |
| 45 | Bit Tricks | XOR/AND | LC 136 |

---

> 最後提醒：白板 coding 的關鍵不是記住每一行，而是記住**骨架**。
> 先寫出模板骨架，再填入題目特定邏輯 — 這就是 pattern matching 的威力。
