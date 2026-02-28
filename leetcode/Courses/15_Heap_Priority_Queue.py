"""
==============================================================================
  LeetCode 教學筆記 #15 — Heap / Priority Queue
  （堆積 / 優先佇列）

  Target: Google / NVIDIA 面試準備
  Level : Beginner → Intermediate（從零開始，逐步進階）
  Style : 每題 3 組 step-by-step 數值追蹤，看懂 heap 每一步的變化

  Usage : python 15_Heap_Priority_Queue.py
==============================================================================
"""

import heapq
from typing import List, Optional
from collections import Counter, defaultdict


# ============================================================================
#  SECTION 1: Heap 基礎概念（Heap Fundamentals）
# ============================================================================
#
#  Heap（堆積）是一種 Complete Binary Tree（完全二元樹），滿足：
#    - Min Heap（最小堆）：parent <= children → root 是最小值
#    - Max Heap（最大堆）：parent >= children → root 是最大值
#
#  Python heapq 模組 → 只支援 Min Heap
#    要做 Max Heap → 存「負值」 (-value)
#
#  用 array 表示樹：index i 的
#    - parent = (i-1) // 2
#    - left child = 2*i + 1
#    - right child = 2*i + 2
#
#  Time Complexity:
#    - heappush   : O(log n) — 新元素從底部 sift up
#    - heappop    : O(log n) — 取 root，最後元素補上再 sift down
#    - heap[0]    : O(1)     — peek 最小值
#    - heapify    : O(n)     — 把整個 list 原地變 heap（比逐一 push 快！）
#    - nlargest(k): O(n log k)
#    - nsmallest(k): O(n log k)
# ============================================================================

def demo_heap_basics():
    print("=" * 70)
    print("SECTION 1: Heap 基礎概念（Heap Fundamentals）")
    print("=" * 70)

    # --- 範例 1: 基本 heappush / heappop ---
    # nums = [5, 3, 8, 1, 2]，逐一 push 進 min heap
    #
    # Step 1: push 5 → heap = [5]
    # Step 2: push 3 → heap = [3, 5]        (3 < 5, sift up)
    # Step 3: push 8 → heap = [3, 5, 8]     (8 > 3, 留在原位)
    # Step 4: push 1 → heap = [1, 3, 8, 5]  (1 sift up 到 root)
    # Step 5: push 2 → heap = [1, 2, 8, 5, 3] (2 sift up 到 index 1)
    #
    # pop: 取出 1 → heap = [2, 3, 8, 5]
    # pop: 取出 2 → heap = [3, 5, 8]
    print("\n範例 1: 基本 heappush / heappop")
    print("  nums = [5, 3, 8, 1, 2]")
    h = []
    for val in [5, 3, 8, 1, 2]:
        heapq.heappush(h, val)
        print(f"  push {val} → heap = {h}")
    print()
    while h:
        val = heapq.heappop(h)
        print(f"  pop → {val}, heap = {h}")

    # --- 範例 2: heapify 原地轉換 ---
    # arr = [9, 4, 7, 1, 3, 6]
    # heapify → arr = [1, 3, 6, 4, 9, 7]  (O(n) 時間)
    print("\n範例 2: heapify 原地轉換")
    arr = [9, 4, 7, 1, 3, 6]
    print(f"  原始: {arr}")
    heapq.heapify(arr)
    print(f"  heapify 後: {arr}")
    print(f"  最小值 (peek): arr[0] = {arr[0]}")
    assert arr[0] == 1

    # --- 範例 3: Max Heap 用負值技巧 ---
    # 要找最大值 → push (-value)，pop 出來再取負
    # nums = [3, 1, 4, 1, 5]
    #
    # push -3 → heap = [-3]
    # push -1 → heap = [-3, -1]
    # push -4 → heap = [-4, -1, -3]
    # push -1 → heap = [-4, -1, -3, -1]
    # push -5 → heap = [-5, -4, -3, -1, -1]
    #
    # pop → -(-5) = 5 (最大值)
    print("\n範例 3: Max Heap（負值技巧）")
    print("  nums = [3, 1, 4, 1, 5]")
    max_h = []
    for val in [3, 1, 4, 1, 5]:
        heapq.heappush(max_h, -val)
        print(f"  push -{val} → heap = {max_h}  (actual values: {[-x for x in max_h]})")
    print()
    top = -heapq.heappop(max_h)
    print(f"  pop max → {top}  (popped {-top} from heap)")
    assert top == 5

    # --- nlargest / nsmallest ---
    print("\n補充: nlargest / nsmallest")
    data = [10, 3, 7, 1, 9, 5]
    print(f"  data = {data}")
    print(f"  nlargest(3)  = {heapq.nlargest(3, data)}")
    print(f"  nsmallest(3) = {heapq.nsmallest(3, data)}")
    print()


# ============================================================================
#  SECTION 2: Top K 問題（Top K Problems）
# ============================================================================

# ----------------------------------------------------------------------------
#  2-1  Kth Largest Element in an Array — LeetCode 215
#
#  方法 A: Min Heap of size k → 維護 k 個最大值，root 就是第 k 大
#          Time: O(n log k)   Space: O(k)
#
#  方法 B: QuickSelect → 平均 O(n)，最差 O(n^2)
# ----------------------------------------------------------------------------

def find_kth_largest(nums: List[int], k: int, verbose: bool = False) -> int:
    """Min Heap of size k: 只保留 k 個最大的，heap[0] 即第 k 大。"""
    heap = []
    for i, num in enumerate(nums):
        if len(heap) < k:
            heapq.heappush(heap, num)
            if verbose:
                print(f"  Step {i+1}: push {num} → heap = {heap}")
        elif num > heap[0]:
            old = heapq.heapreplace(heap, num)  # pop min + push num (一步完成)
            if verbose:
                print(f"  Step {i+1}: {num} > heap[0]={old} → replace → heap = {heap}")
        else:
            if verbose:
                print(f"  Step {i+1}: {num} <= heap[0]={heap[0]} → skip")
    return heap[0]


def find_kth_largest_quickselect(nums: List[int], k: int, verbose: bool = False) -> int:
    """QuickSelect: 平均 O(n)，原地分區找第 k 大。"""
    target = len(nums) - k  # 第 k 大 = 排序後 index (n-k)

    def quickselect(left: int, right: int) -> int:
        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]
        if verbose:
            print(f"  partition pivot={pivot}, store={store}, array={nums[left:right+1]}")
        if store == target:
            return nums[store]
        elif store < target:
            return quickselect(store + 1, right)
        else:
            return quickselect(left, store - 1)

    return quickselect(0, len(nums) - 1)


def demo_kth_largest():
    print("=" * 70)
    print("2-1  Kth Largest Element — LeetCode 215")
    print("=" * 70)

    # 範例 1: nums = [3,2,1,5,6,4], k = 2
    # Min heap of size k=2:
    # Step 1: push 3 → heap = [3]
    # Step 2: push 2 → heap = [2, 3]   (size=k, full)
    # Step 3: 1 <= heap[0]=2 → skip
    # Step 4: 5 > heap[0]=2 → replace → heap = [3, 5]
    # Step 5: 6 > heap[0]=3 → replace → heap = [5, 6]
    # Step 6: 4 <= heap[0]=5 → skip
    # Result: heap[0] = 5 ✓
    print("\n範例 1: nums = [3,2,1,5,6,4], k = 2")
    assert find_kth_largest([3,2,1,5,6,4], 2, verbose=True) == 5

    # 範例 2: nums = [3,2,3,1,2,4,5,5,6], k = 4
    # 排序後 = [1,2,2,3,3,4,5,5,6], 第 4 大 = 4
    print("\n範例 2: nums = [3,2,3,1,2,4,5,5,6], k = 4")
    assert find_kth_largest([3,2,3,1,2,4,5,5,6], 4, verbose=True) == 4

    # 範例 3: nums = [1], k = 1
    print("\n範例 3: nums = [1], k = 1")
    assert find_kth_largest([1], 1, verbose=True) == 1

    # QuickSelect 示範
    print("\n  --- QuickSelect 方法 ---")
    assert find_kth_largest_quickselect([3,2,1,5,6,4], 2, verbose=True) == 5
    print()


# ----------------------------------------------------------------------------
#  2-2  Top K Frequent Elements — LeetCode 347
#
#  Step 1: Counter 統計頻率
#  Step 2: Min Heap of size k → 保留頻率最高的 k 個
#  Time: O(n log k)   Space: O(n)
# ----------------------------------------------------------------------------

def top_k_frequent(nums: List[int], k: int, verbose: bool = False) -> List[int]:
    """用 min heap of size k 找出出現頻率前 k 高的元素。"""
    freq = Counter(nums)
    if verbose:
        print(f"  頻率統計: {dict(freq)}")

    heap = []  # stores (frequency, number)
    for num, cnt in freq.items():
        if len(heap) < k:
            heapq.heappush(heap, (cnt, num))
            if verbose:
                print(f"  push ({cnt}, {num}) → heap = {heap}")
        elif cnt > heap[0][0]:
            old = heapq.heapreplace(heap, (cnt, num))
            if verbose:
                print(f"  ({cnt}, {num}) > min={old} → replace → heap = {heap}")
        else:
            if verbose:
                print(f"  ({cnt}, {num}) <= min freq {heap[0][0]} → skip")

    result = [num for _, num in heap]
    return result


def demo_top_k_frequent():
    print("=" * 70)
    print("2-2  Top K Frequent Elements — LeetCode 347")
    print("=" * 70)

    # 範例 1: nums = [1,1,1,2,2,3], k = 2
    # freq = {1:3, 2:2, 3:1}
    # heap size k=2:
    #   push (3,1) → heap = [(3,1)]
    #   push (2,2) → heap = [(2,2), (3,1)]
    #   (1,3) <= min freq 2 → skip
    # Result: [2, 1] (頻率最高的 2 個)
    print("\n範例 1: nums = [1,1,1,2,2,3], k = 2")
    res = top_k_frequent([1,1,1,2,2,3], 2, verbose=True)
    assert set(res) == {1, 2}
    print(f"  → Result: {res}")

    # 範例 2: nums = [4,4,4,3,3,2,2,2,1], k = 2
    # freq = {4:3, 3:2, 2:3, 1:1}
    print("\n範例 2: nums = [4,4,4,3,3,2,2,2,1], k = 2")
    res = top_k_frequent([4,4,4,3,3,2,2,2,1], 2, verbose=True)
    assert set(res) == {4, 2}
    print(f"  → Result: {res}")

    # 範例 3: nums = [1], k = 1
    print("\n範例 3: nums = [1], k = 1")
    res = top_k_frequent([1], 1, verbose=True)
    assert res == [1]
    print(f"  → Result: {res}")
    print()


# ----------------------------------------------------------------------------
#  2-3  K Closest Points to Origin — LeetCode 973
#
#  距離 = x^2 + y^2（不需要開根號，比較大小即可）
#  Max Heap of size k：保留距離最小的 k 個點
#    → 存 (-distance, point)，超過 k 個時 pop 掉距離最大的
#  Time: O(n log k)   Space: O(k)
# ----------------------------------------------------------------------------

def k_closest(points: List[List[int]], k: int, verbose: bool = False) -> List[List[int]]:
    """Max heap of size k (用負距離)：保留最近的 k 個點。"""
    heap = []  # stores (-distance, x, y)
    for x, y in points:
        dist = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-dist, x, y))
            if verbose:
                print(f"  push ({x},{y}) dist={dist} → heap(neg) = {heap}")
        elif -dist > heap[0][0]:  # dist < -heap[0][0] (current max distance)
            old = heapq.heapreplace(heap, (-dist, x, y))
            if verbose:
                print(f"  ({x},{y}) dist={dist} < max_dist={-old[0]} → replace → heap = {heap}")
        else:
            if verbose:
                print(f"  ({x},{y}) dist={dist} >= max_dist={-heap[0][0]} → skip")
    return [[x, y] for _, x, y in heap]


def demo_k_closest():
    print("=" * 70)
    print("2-3  K Closest Points to Origin — LeetCode 973")
    print("=" * 70)

    # 範例 1: points = [[1,3],[-2,2]], k = 1
    # dist(1,3) = 1+9 = 10
    # dist(-2,2) = 4+4 = 8
    # Max heap size 1:
    #   push (1,3) dist=10 → heap = [(-10,1,3)]
    #   (-2,2) dist=8 < max=10 → replace → heap = [(-8,-2,2)]
    # Result: [[-2,2]]
    print("\n範例 1: points = [[1,3],[-2,2]], k = 1")
    res = k_closest([[1,3],[-2,2]], 1, verbose=True)
    print(f"  → Result: {res}")
    assert res == [[-2, 2]]

    # 範例 2: points = [[3,3],[5,-1],[-2,4]], k = 2
    # dist(3,3)=18, dist(5,-1)=26, dist(-2,4)=20
    print("\n範例 2: points = [[3,3],[5,-1],[-2,4]], k = 2")
    res = k_closest([[3,3],[5,-1],[-2,4]], 2, verbose=True)
    print(f"  → Result: {res}")
    result_set = {(p[0], p[1]) for p in res}
    assert result_set == {(3, 3), (-2, 4)}

    # 範例 3: points = [[0,1],[1,0],[0,-1]], k = 2
    # all dist = 1 → any 2 of them
    print("\n範例 3: points = [[0,1],[1,0],[0,-1]], k = 2")
    res = k_closest([[0,1],[1,0],[0,-1]], 2, verbose=True)
    print(f"  → Result: {res}")
    assert len(res) == 2
    print()


# ----------------------------------------------------------------------------
#  2-4  Sort Characters By Frequency — LeetCode 451
#
#  Step 1: Counter 統計頻率
#  Step 2: Max Heap（存 (-freq, char)），依序 pop 組字串
#  Time: O(n log k) where k = distinct chars   Space: O(n)
# ----------------------------------------------------------------------------

def frequency_sort(s: str, verbose: bool = False) -> str:
    """依字元頻率排序：高頻在前。"""
    freq = Counter(s)
    if verbose:
        print(f"  頻率: {dict(freq)}")

    # Max heap: 存 (-count, char)
    heap = [(-cnt, ch) for ch, cnt in freq.items()]
    heapq.heapify(heap)
    if verbose:
        print(f"  Max heap (neg): {heap}")

    result = []
    while heap:
        neg_cnt, ch = heapq.heappop(heap)
        cnt = -neg_cnt
        result.append(ch * cnt)
        if verbose:
            print(f"  pop '{ch}' x {cnt} → building: '{''.join(result)}'")

    return "".join(result)


def demo_frequency_sort():
    print("=" * 70)
    print("2-4  Sort Characters By Frequency — LeetCode 451")
    print("=" * 70)

    # 範例 1: s = "tree"
    # freq: t=1, r=1, e=2 → "eert" or "eetr"
    print("\n範例 1: s = 'tree'")
    res = frequency_sort("tree", verbose=True)
    print(f"  → Result: '{res}'")
    assert res[0:2] == "ee"  # e must come first (freq=2)

    # 範例 2: s = "cccaaa"
    # freq: c=3, a=3 → "cccaaa" or "aaaccc"
    print("\n範例 2: s = 'cccaaa'")
    res = frequency_sort("cccaaa", verbose=True)
    print(f"  → Result: '{res}'")
    assert len(res) == 6

    # 範例 3: s = "Aabb"
    # freq: A=1, a=1, b=2 → "bbAa" or "bbaA"
    print("\n範例 3: s = 'Aabb'")
    res = frequency_sort("Aabb", verbose=True)
    print(f"  → Result: '{res}'")
    assert res[0:2] == "bb"
    print()


# ============================================================================
#  SECTION 3: 合併型（Merge with Heap）
# ============================================================================

# ----------------------------------------------------------------------------
#  3-1  Merge K Sorted Lists — LeetCode 23
#
#  把 K 個 sorted linked list 的當前最小值放入 min heap，
#  每次 pop 最小的接到結果，再把它的 next push 進去。
#
#  Time: O(N log K)  where N = total nodes, K = number of lists
#  Space: O(K)
# ----------------------------------------------------------------------------

class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

    def __repr__(self):
        vals = []
        cur = self
        while cur:
            vals.append(str(cur.val))
            cur = cur.next
        return " → ".join(vals)


def merge_k_lists(lists: List[Optional[ListNode]], verbose: bool = False) -> Optional[ListNode]:
    """用 min heap 合併 K 個 sorted linked lists。"""
    heap = []
    # 把每個 list 的 head 放入 heap
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))
    if verbose:
        print(f"  初始 heap: {[(v, i) for v, i, _ in heap]}")

    dummy = ListNode(0)
    cur = dummy
    counter = len(lists)  # 用 counter 避免 ListNode 比較

    while heap:
        val, idx, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if verbose:
            print(f"  pop ({val}, list{idx}) → result 接上 {val}", end="")
        if node.next:
            counter += 1
            heapq.heappush(heap, (node.next.val, counter, node.next))
            if verbose:
                print(f"  | push ({node.next.val})", end="")
        if verbose:
            print(f"  | heap = {[(v, i) for v, i, _ in heap]}")

    return dummy.next


def make_list(arr: List[int]) -> Optional[ListNode]:
    """從 array 建立 linked list。"""
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for v in arr[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def demo_merge_k_lists():
    print("=" * 70)
    print("3-1  Merge K Sorted Lists — LeetCode 23")
    print("=" * 70)

    # 範例 1: lists = [[1,4,5],[1,3,4],[2,6]]
    # 初始 heap: [(1,0), (1,1), (2,2)]
    # pop (1,list0) → push 4 → heap: [(1,1), (2,2), (4,...)]
    # pop (1,list1) → push 3 → heap: [(2,2), (3,...), (4,...)]
    # pop (2,list2) → push 6 → heap: [(3,...), (4,...), (6,...)]
    # pop (3,...) → push 4 → ...
    # Result: 1→1→2→3→4→4→5→6
    print("\n範例 1: [[1,4,5],[1,3,4],[2,6]]")
    l1 = make_list([1,4,5])
    l2 = make_list([1,3,4])
    l3 = make_list([2,6])
    res = merge_k_lists([l1, l2, l3], verbose=True)
    print(f"  → Result: {res}")

    # 範例 2: lists = [[], [1]]
    print("\n範例 2: [[], [1]]")
    res = merge_k_lists([make_list([]), make_list([1])], verbose=True)
    print(f"  → Result: {res}")
    assert res.val == 1

    # 範例 3: lists = [[2,5],[1,3,7],[4,6]]
    print("\n範例 3: [[2,5],[1,3,7],[4,6]]")
    res = merge_k_lists([make_list([2,5]), make_list([1,3,7]), make_list([4,6])], verbose=True)
    print(f"  → Result: {res}")
    print()


# ----------------------------------------------------------------------------
#  3-2  Find Median from Data Stream — LeetCode 295
#
#  核心概念：用兩個 heap 維護中位數
#    - max_heap (左半部，存負值): 較小的那一半
#    - min_heap (右半部): 較大的那一半
#
#  規則：
#    1. max_heap 的大小 >= min_heap（最多多 1 個）
#    2. max_heap 的最大值 <= min_heap 的最小值
#
#  中位數：
#    - 奇數個 → max_heap 的 root
#    - 偶數個 → (max_heap root + min_heap root) / 2
#
#  Time: addNum O(log n), findMedian O(1)
# ----------------------------------------------------------------------------

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # 左半 (存負值模擬 max heap)
        self.min_heap = []  # 右半 (正常 min heap)

    def addNum(self, num: int, verbose: bool = False) -> None:
        # Step 1: 先加入 max_heap
        heapq.heappush(self.max_heap, -num)
        # Step 2: 確保 max_heap 的最大值 <= min_heap 的最小值
        if self.min_heap and (-self.max_heap[0]) > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        # Step 3: 平衡大小：max_heap 最多比 min_heap 多 1
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

        if verbose:
            left = sorted([-x for x in self.max_heap], reverse=True)
            right = sorted(self.min_heap)
            print(f"  add({num}) → left(max)={left}, right(min)={right}, median={self.findMedian()}")

    def findMedian(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2


def demo_median_finder():
    print("=" * 70)
    print("3-2  Find Median from Data Stream — LeetCode 295")
    print("=" * 70)

    # 範例 1: addNum 順序 [2, 3, 4]
    # add(2): left=[2], right=[]       → median = 2
    # add(3): left=[2], right=[3]      → median = 2.5
    # add(4): left=[2,3], right=[4]... → left=[2], right=[3,4] → med=2.5
    #   actually: left=[3,2], right=[4] hmm...
    #   Let me re-trace: add 2 → max_heap=[-2], min=[]
    #   add 3 → push -3 to max → max=[-3,-2], then -(-3)=3 > nothing → ok
    #     but max size=2 > min size 0 +1 → move 3 to min → max=[-2], min=[3]
    #     median = (2+3)/2 = 2.5
    #   add 4 → push -4 to max → max=[-4,-2], -(-4)=4 > min[0]=3 → move 4 to min
    #     max=[-2], min=[3,4], but min size=2 > max size=1 → move 3 to max
    #     max=[-3,-2], min=[4] → median = 3
    print("\n範例 1: stream = [2, 3, 4]")
    mf = MedianFinder()
    mf.addNum(2, verbose=True)
    assert mf.findMedian() == 2
    mf.addNum(3, verbose=True)
    assert mf.findMedian() == 2.5
    mf.addNum(4, verbose=True)
    assert mf.findMedian() == 3

    # 範例 2: stream = [5, 2, 8, 1]
    # add(5): left=[5], right=[]  → median=5
    # add(2): left=[2], right=[5] → median=3.5
    # add(8): left=[2,5], right=[8]... → left=[5,2], right=[8] → med=5
    # add(1): left=[2,1], right=[5,8] → med=(2+5)/2=3.5
    print("\n範例 2: stream = [5, 2, 8, 1]")
    mf2 = MedianFinder()
    for num in [5, 2, 8, 1]:
        mf2.addNum(num, verbose=True)
    assert mf2.findMedian() == 3.5

    # 範例 3: stream = [1, 1, 1, 1]
    print("\n範例 3: stream = [1, 1, 1, 1]")
    mf3 = MedianFinder()
    for num in [1, 1, 1, 1]:
        mf3.addNum(num, verbose=True)
    assert mf3.findMedian() == 1.0
    print()


# ----------------------------------------------------------------------------
#  3-3  Smallest Range Covering Elements from K Lists — LeetCode 632
#
#  概念：K 個 sorted list，找最小區間 [a, b] 使得每個 list 至少有一個元素在內。
#
#  做法：
#    1. 把每個 list 的第一個元素放入 min heap，同時記錄當前最大值 cur_max
#    2. 每次 pop 最小值 → 區間 = [heap[0], cur_max]
#    3. 把 pop 出來那個 list 的下一個元素 push 進去，更新 cur_max
#    4. 某個 list 用完就停
#
#  Time: O(N log K)   Space: O(K)
# ----------------------------------------------------------------------------

def smallest_range(nums: List[List[int]], verbose: bool = False) -> List[int]:
    """找覆蓋 K 個 lists 的最小區間。"""
    heap = []
    cur_max = float('-inf')
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        cur_max = max(cur_max, lst[0])
    if verbose:
        print(f"  初始: heap = {[(v,i,j) for v,i,j in heap]}, cur_max = {cur_max}")

    best = [float('-inf'), float('inf')]

    while heap:
        cur_min, list_idx, elem_idx = heapq.heappop(heap)
        # 更新最佳區間
        if cur_max - cur_min < best[1] - best[0]:
            best = [cur_min, cur_max]
        if verbose:
            print(f"  pop ({cur_min}, list{list_idx}) → range=[{cur_min},{cur_max}], "
                  f"best={best}")
        # 推入該 list 的下一個元素
        if elem_idx + 1 < len(nums[list_idx]):
            nxt = nums[list_idx][elem_idx + 1]
            heapq.heappush(heap, (nxt, list_idx, elem_idx + 1))
            cur_max = max(cur_max, nxt)
        else:
            break  # 某個 list 用完，不可能再覆蓋所有 list

    return best


def demo_smallest_range():
    print("=" * 70)
    print("3-3  Smallest Range Covering K Lists — LeetCode 632")
    print("=" * 70)

    # 範例 1: nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
    # 初始: heap = [(0,1,0),(4,0,0),(5,2,0)], cur_max = 5
    # pop 0 → range [0,5], push 9 → cur_max=9
    # pop 4 → range [4,9], push 10 → cur_max=10
    # pop 5 → range [5,10], push 18 → cur_max=18
    # pop 9 → range [9,18], push 12 → cur_max=18
    # pop 10 → range [10,18], push 15 → cur_max=18
    # pop 12 → range [12,18], push 20 → cur_max=20
    # pop 15 → range [15,20], push 24 → cur_max=24
    # pop 18 → range [18,24], push 22 → cur_max=24
    # pop 20 → range [20,24] (size=4), best so far [20,24]
    # Result: [20,24]
    print("\n範例 1: [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]")
    res = smallest_range([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]], verbose=True)
    print(f"  → Result: {res}")
    assert res == [20, 24]

    # 範例 2: nums = [[1,2,3],[1,2,3],[1,2,3]]
    # All lists start with 1 → range [1,1] is optimal
    print("\n範例 2: [[1,2,3],[1,2,3],[1,2,3]]")
    res = smallest_range([[1,2,3],[1,2,3],[1,2,3]], verbose=True)
    print(f"  → Result: {res}")
    assert res == [1, 1]
    print()


# ============================================================================
#  SECTION 4: 排程 / 貪心 + Heap（Scheduling / Greedy + Heap）
# ============================================================================

# ----------------------------------------------------------------------------
#  4-1  Task Scheduler — LeetCode 621
#
#  有 tasks (字元陣列) 和冷卻時間 n，同一種 task 之間至少間隔 n。
#  目標：最少多少時間單位完成所有 task。
#
#  貪心 + Max Heap:
#    1. 統計頻率，放入 max heap
#    2. 每個 cycle = n+1 個 slot
#    3. 每個 cycle 從 heap pop 最多 n+1 個 task 執行
#    4. 未完成的（頻率-1 > 0）暫存，cycle 結束後 push 回去
#
#  Time: O(N * n)   Space: O(26) = O(1)
# ----------------------------------------------------------------------------

def least_interval(tasks: List[str], n: int, verbose: bool = False) -> int:
    """計算完成所有 task 的最少時間單位。"""
    freq = Counter(tasks)
    # Max heap (負頻率)
    heap = [-cnt for cnt in freq.values()]
    heapq.heapify(heap)
    if verbose:
        print(f"  頻率: {dict(freq)}")
        print(f"  Max heap (neg): {heap}")

    time = 0
    while heap:
        cycle = []
        for _ in range(n + 1):  # 每個 cycle 最多 n+1 個 slot
            if heap:
                cnt = heapq.heappop(heap)
                if cnt + 1 < 0:  # 還有剩餘（記住是負數）
                    cycle.append(cnt + 1)
                time += 1
                if verbose:
                    print(f"  t={time}: execute task (remaining={-(cnt+1)})", end="")
            elif cycle:
                time += 1  # idle
                if verbose:
                    print(f"  t={time}: idle", end="")
            if verbose and (heap or cycle):
                print()

        # 把未完成的 push 回 heap
        for item in cycle:
            heapq.heappush(heap, item)
        if verbose and cycle:
            print(f"  --- end cycle, push back {[-x for x in cycle]} ---")

    return time


def demo_task_scheduler():
    print("=" * 70)
    print("4-1  Task Scheduler — LeetCode 621")
    print("=" * 70)

    # 範例 1: tasks = ["A","A","A","B","B","B"], n = 2
    # freq: A=3, B=3, heap(neg) = [-3, -3]
    # Cycle 1: pop A(3), pop B(3) → slot1=A, slot2=B, slot3=idle → time=3
    #   push back A(2), B(2)
    # Cycle 2: A, B, idle → time=6, push back A(1), B(1)
    # Cycle 3: A, B → time=8
    # Total = 8
    print("\n範例 1: tasks = ['A','A','A','B','B','B'], n = 2")
    res = least_interval(["A","A","A","B","B","B"], 2, verbose=True)
    print(f"  → Result: {res}")
    assert res == 8

    # 範例 2: tasks = ["A","A","A","B","B","B"], n = 0
    # n=0 → no cooldown → 6
    print("\n範例 2: tasks = ['A','A','A','B','B','B'], n = 0")
    res = least_interval(["A","A","A","B","B","B"], 0, verbose=True)
    print(f"  → Result: {res}")
    assert res == 6

    # 範例 3: tasks = ["A","A","A","A","B","B","C"], n = 2
    # freq: A=4, B=2, C=1 → heap [-4,-2,-1]
    # Cycle 1: A(4), B(2), C(1) → push back A(3), B(1) → time=3
    # Cycle 2: A(3), B(1), idle → push back A(2) → time=6
    # Cycle 3: A(2), idle, idle → push back A(1) → time=9
    # Cycle 4: A(1) → time=10
    # Total = 10
    print("\n範例 3: tasks = ['A','A','A','A','B','B','C'], n = 2")
    res = least_interval(["A","A","A","A","B","B","C"], 2, verbose=True)
    print(f"  → Result: {res}")
    assert res == 10
    print()


# ----------------------------------------------------------------------------
#  4-2  Reorganize String — LeetCode 767
#
#  重排字串使得相鄰字元不同。若不可能回傳 ""。
#
#  Max Heap 貪心：每次取頻率最高的字元放入結果，
#    如果它跟上一個放的相同 → 改取第二高的。
#
#  不可能的條件：max_freq > (len(s)+1) // 2
#
#  Time: O(n log 26) = O(n)   Space: O(26) = O(1)
# ----------------------------------------------------------------------------

def reorganize_string(s: str, verbose: bool = False) -> str:
    freq = Counter(s)
    max_freq = max(freq.values())
    if max_freq > (len(s) + 1) // 2:
        if verbose:
            print(f"  max_freq={max_freq} > (len+1)//2={(len(s)+1)//2} → 不可能")
        return ""

    # Max heap: (-count, char)
    heap = [(-cnt, ch) for ch, cnt in freq.items()]
    heapq.heapify(heap)
    if verbose:
        print(f"  頻率: {dict(freq)}")

    result = []
    prev_cnt, prev_ch = 0, ''

    while heap:
        cnt, ch = heapq.heappop(heap)
        # 如果前一個字元還有剩餘，push 回去
        if prev_cnt < 0:
            heapq.heappush(heap, (prev_cnt, prev_ch))
        result.append(ch)
        prev_cnt = cnt + 1  # 用掉一個（負數 + 1 → 趨近 0）
        prev_ch = ch
        if verbose:
            print(f"  pick '{ch}' (remaining={-cnt-1}) → result = '{''.join(result)}'")

    res = "".join(result)
    return res


def demo_reorganize_string():
    print("=" * 70)
    print("4-2  Reorganize String — LeetCode 767")
    print("=" * 70)

    # 範例 1: s = "aab"
    # freq: a=2, b=1 → max_freq=2 <= (3+1)//2=2 → ok
    # heap: [(-2,'a'), (-1,'b')]
    # pick 'a'(1) → "a", prev=('a',1)
    # pick 'b'(0) → "ab", push back 'a'(1)
    # pick 'a'(0) → "aba"
    # Result: "aba"
    print("\n範例 1: s = 'aab'")
    res = reorganize_string("aab", verbose=True)
    print(f"  → Result: '{res}'")
    assert len(res) == 3 and all(res[i] != res[i+1] for i in range(len(res)-1))

    # 範例 2: s = "aaab"
    # freq: a=3, b=1 → max_freq=3 > (4+1)//2=2 → 不可能
    print("\n範例 2: s = 'aaab'")
    res = reorganize_string("aaab", verbose=True)
    print(f"  → Result: '{res}'")
    assert res == ""

    # 範例 3: s = "aabb"
    # freq: a=2, b=2 → ok
    print("\n範例 3: s = 'aabb'")
    res = reorganize_string("aabb", verbose=True)
    print(f"  → Result: '{res}'")
    assert len(res) == 4 and all(res[i] != res[i+1] for i in range(len(res)-1))
    print()


# ----------------------------------------------------------------------------
#  4-3  Meeting Rooms II — LeetCode 253
#
#  給一組會議區間 [start, end]，求最少需要幾間會議室。
#
#  Min Heap 做法：
#    1. 按 start 排序
#    2. heap 存「目前使用中的會議室結束時間」
#    3. 新會議來時，如果 heap[0] <= start → 可以複用（pop 掉）
#    4. push 新會議的 end
#    5. heap 的大小 = 同時使用的會議室數量
#
#  Time: O(n log n)   Space: O(n)
# ----------------------------------------------------------------------------

def min_meeting_rooms(intervals: List[List[int]], verbose: bool = False) -> int:
    """計算最少需要的會議室數量。"""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    if verbose:
        print(f"  排序後: {intervals}")

    heap = []  # 存各會議室的結束時間
    for start, end in intervals:
        if heap and heap[0] <= start:
            old_end = heapq.heappop(heap)
            if verbose:
                print(f"  會議 [{start},{end}]: room 結束時間 {old_end} <= {start} → 複用", end="")
        else:
            if verbose:
                print(f"  會議 [{start},{end}]: 需要新 room", end="")
        heapq.heappush(heap, end)
        if verbose:
            print(f"  → rooms heap = {sorted(heap)}, count = {len(heap)}")

    return len(heap)


def demo_meeting_rooms():
    print("=" * 70)
    print("4-3  Meeting Rooms II — LeetCode 253")
    print("=" * 70)

    # 範例 1: intervals = [[0,30],[5,10],[15,20]]
    # 排序: [[0,30],[5,10],[15,20]]
    # [0,30]: 新 room → heap = [30], count=1
    # [5,10]: 30 > 5 → 新 room → heap = [10,30], count=2
    # [15,20]: 10 <= 15 → 複用 → pop 10, push 20 → heap = [20,30], count=2
    # Result: 2
    print("\n範例 1: intervals = [[0,30],[5,10],[15,20]]")
    assert min_meeting_rooms([[0,30],[5,10],[15,20]], verbose=True) == 2

    # 範例 2: intervals = [[7,10],[2,4]]
    # 排序: [[2,4],[7,10]]
    # [2,4]: 新 room → heap=[4], count=1
    # [7,10]: 4 <= 7 → 複用 → heap=[10], count=1
    # Result: 1
    print("\n範例 2: intervals = [[7,10],[2,4]]")
    assert min_meeting_rooms([[7,10],[2,4]], verbose=True) == 1

    # 範例 3: intervals = [[1,5],[2,6],[3,7],[4,8]]
    # 全部重疊 → 4 間
    print("\n範例 3: intervals = [[1,5],[2,6],[3,7],[4,8]]")
    assert min_meeting_rooms([[1,5],[2,6],[3,7],[4,8]], verbose=True) == 4
    print()


# ============================================================================
#  SECTION 5: Heap vs Sort vs QuickSelect 比較
#  （Heap vs Sort vs QuickSelect Comparison）
# ============================================================================

def print_comparison():
    print("=" * 70)
    print("SECTION 5: Heap vs Sort vs QuickSelect 比較")
    print("=" * 70)
    print("""
┌──────────────┬──────────────────┬───────────────┬──────────────────────┐
│   方法       │  Time            │  Space        │  適用場景            │
├──────────────┼──────────────────┼───────────────┼──────────────────────┤
│ Sort 排序    │ O(n log n)       │ O(n) or O(1)  │ 需要完整排序結果      │
│              │                  │               │ 資料量小、一次性操作   │
├──────────────┼──────────────────┼───────────────┼──────────────────────┤
│ Heap (Top K) │ O(n log k)       │ O(k)          │ 只需前 K 個           │
│              │                  │               │ Streaming data（串流）│
│              │                  │               │ k << n 時特別高效     │
├──────────────┼──────────────────┼───────────────┼──────────────────────┤
│ QuickSelect  │ O(n) avg         │ O(1)          │ 只需第 K 個（不需排序）│
│              │ O(n^2) worst     │               │ 可修改原 array        │
│              │                  │               │ 不適合 streaming      │
└──────────────┴──────────────────┴───────────────┴──────────────────────┘

重要結論（Key Takeaways）:

1. Streaming Data → Heap 最佳
   - 資料持續流入，不知道總量 → 只能用 heap
   - 例如: Find Median from Data Stream

2. 只要第 K 個元素 → QuickSelect（平均最快）
   - 但面試中 heap 更安全（worst case O(n log k) vs O(n^2)）

3. k 接近 n → 直接 sort
   - 當 k ≈ n 時，heap 的 O(n log k) ≈ O(n log n)，不如直接排序

4. Python 特殊技巧:
   - heapq.nlargest(k, iterable)  — 內部用 heap，適合 k 小的情況
   - heapq.nsmallest(k, iterable) — 同上
   - sorted(iterable)[:k]         — k 大時反而更快

5. 面試中 Heap 的常見信號:
   - 題目出現 "Top K"、"Kth largest/smallest"
   - 題目出現 "merge sorted"
   - 題目需要 "streaming" 或 "online" 處理
   - 題目需要 "scheduling" 搭配 greedy
""")


# ============================================================================
#  BONUS: 常用 heapq 操作速查表
# ============================================================================

def print_heapq_cheatsheet():
    print("=" * 70)
    print("BONUS: heapq 操作速查表（Cheatsheet）")
    print("=" * 70)
    print("""
┌───────────────────────────────┬────────┬──────────────────────────────┐
│ 操作                          │ 複雜度 │ 說明                         │
├───────────────────────────────┼────────┼──────────────────────────────┤
│ heapq.heappush(heap, item)    │ O(logn)│ 加入元素                     │
│ heapq.heappop(heap)           │ O(logn)│ 取出最小值                   │
│ heap[0]                       │ O(1)   │ 查看最小值（peek）            │
│ heapq.heapify(list)           │ O(n)   │ 原地轉換為 heap              │
│ heapq.heapreplace(heap, item) │ O(logn)│ pop + push（一步完成，更快）  │
│ heapq.heappushpop(heap, item) │ O(logn)│ push + pop（一步完成）        │
│ heapq.nlargest(k, iterable)   │O(nlogk)│ 取前 k 大                    │
│ heapq.nsmallest(k, iterable)  │O(nlogk)│ 取前 k 小                    │
├───────────────────────────────┼────────┼──────────────────────────────┤
│ Max Heap 技巧:                │        │ push/pop 時取負值             │
│   heapq.heappush(h, -val)     │        │ push 負值                    │
│   -heapq.heappop(h)           │        │ pop 後取負還原               │
├───────────────────────────────┼────────┼──────────────────────────────┤
│ Tuple 排序:                   │        │ (priority, tiebreaker, data) │
│   heapq.heappush(h, (1,'a'))  │        │ 先比第一欄，相同再比第二欄    │
└───────────────────────────────┴────────┴──────────────────────────────┘

heapreplace vs heappushpop:
  heapreplace(h, x): 先 pop 再 push → 保證 pop 的是舊的 min
  heappushpop(h, x): 先 push 再 pop → 如果 x 最小會直接回傳 x
""")


# ============================================================================
#  main()
# ============================================================================

def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║  LeetCode #15 — Heap / Priority Queue（堆積 / 優先佇列）        ║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Section 1: Heap 基礎概念
    demo_heap_basics()

    # Section 2: Top K 問題
    demo_kth_largest()
    demo_top_k_frequent()
    demo_k_closest()
    demo_frequency_sort()

    # Section 3: 合併型
    demo_merge_k_lists()
    demo_median_finder()
    demo_smallest_range()

    # Section 4: 排程 / 貪心 + Heap
    demo_task_scheduler()
    demo_reorganize_string()
    demo_meeting_rooms()

    # Section 5: 比較總結
    print_comparison()

    # Bonus: Cheatsheet
    print_heapq_cheatsheet()

    print("=" * 70)
    print("  ALL EXAMPLES PASSED — 全部範例通過！")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
