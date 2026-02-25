#!/usr/bin/env python3
"""
=============================================================================
LeetCode 排序演算法 + 位元運算完全攻略 (Sorting Algorithms + Bit Manipulation)
=============================================================================
目標讀者：準備 Google / NVIDIA 面試的初學者
教學風格：每題多個範例，每個範例都有完整的 step-by-step 數值追蹤
語言：繁體中文解說 + English technical terms

直接執行：python 17_Sort_And_Bit.py
=============================================================================
"""
from typing import List, Optional


# ████████████████████████████████████████████████████████████████████████████
# Part A: 排序演算法 (Sorting Algorithms)
# ████████████████████████████████████████████████████████████████████████████


# ============================================================================
# Section 1: 基礎排序 (Basic Sorts) - 理解概念
# ============================================================================
# 這三種排序都是 O(n^2)，面試中不會直接考，但理解它們的「核心動作」
# 對理解進階排序非常有幫助。
# ============================================================================


# ---------------------------------------------------------------------------
# 1-1. Bubble Sort (泡沫排序)
# ---------------------------------------------------------------------------
# 核心概念：相鄰元素兩兩比較，大的往右「冒泡」。
# 每一輪結束後，最大的元素會被推到最右邊（已排好的位置）。
#
# Time: O(n^2) worst/avg, O(n) best (already sorted, with early stop)
# Space: O(1), Stable: Yes, In-place: Yes
#
# 範例: arr = [5, 3, 8, 1, 2]
#
# === Pass 1 (把最大值 8 冒泡到最右邊) ===
# [5, 3, 8, 1, 2]  compare 5>3 → swap → [3, 5, 8, 1, 2]
# [3, 5, 8, 1, 2]  compare 5>8? No     → [3, 5, 8, 1, 2]
# [3, 5, 8, 1, 2]  compare 8>1 → swap → [3, 5, 1, 8, 2]
# [3, 5, 1, 8, 2]  compare 8>2 → swap → [3, 5, 1, 2, 8]  ← 8 到位
#
# === Pass 2 (把次大值 5 冒泡) ===
# [3, 5, 1, 2, 8]  compare 3>5? No     → [3, 5, 1, 2, 8]
# [3, 5, 1, 2, 8]  compare 5>1 → swap → [3, 1, 5, 2, 8]
# [3, 1, 5, 2, 8]  compare 5>2 → swap → [3, 1, 2, 5, 8]  ← 5 到位
#
# === Pass 3 ===
# [3, 1, 2, 5, 8]  compare 3>1 → swap → [1, 3, 2, 5, 8]
# [1, 3, 2, 5, 8]  compare 3>2 → swap → [1, 2, 3, 5, 8]  ← 3 到位
#
# === Pass 4 ===
# [1, 2, 3, 5, 8]  compare 1>2? No → no swaps → 提前結束!
#
# 結果: [1, 2, 3, 5, 8]

def bubble_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Bubble Sort - 泡沫排序，相鄰元素兩兩比較交換。"""
    a = arr[:]  # 不修改原陣列
    n = len(a)
    for i in range(n - 1):
        swapped = False
        if verbose:
            print(f"  === Pass {i + 1} ===")
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                if verbose:
                    print(f"  {a}  compare {a[j]}>{a[j+1]} → swap", end="")
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                if verbose:
                    print(f" → {a}")
            else:
                if verbose:
                    print(f"  {a}  compare {a[j]}>{a[j+1]}? No")
        if not swapped:
            if verbose:
                print(f"  No swaps in this pass → 提前結束!")
            break
    return a


# ---------------------------------------------------------------------------
# 1-2. Selection Sort (選擇排序)
# ---------------------------------------------------------------------------
# 核心概念：每次從未排序區間中「選出最小值」，放到已排序區間的末尾。
#
# Time: O(n^2) always, Space: O(1), Stable: No, In-place: Yes
#
# 範例: arr = [4, 2, 7, 1, 3]
#
# Pass 1: 未排序=[4,2,7,1,3], 最小值=1(idx=3), swap arr[0]↔arr[3]
#          → [1, 2, 7, 4, 3]  已排序: [1]
# Pass 2: 未排序=[2,7,4,3], 最小值=2(idx=1), 已在正確位置
#          → [1, 2, 7, 4, 3]  已排序: [1, 2]
# Pass 3: 未排序=[7,4,3], 最小值=3(idx=4), swap arr[2]↔arr[4]
#          → [1, 2, 3, 4, 7]  已排序: [1, 2, 3]
# Pass 4: 未排序=[4,7], 最小值=4(idx=3), 已在正確位置
#          → [1, 2, 3, 4, 7]  已排序: [1, 2, 3, 4]
# 結果: [1, 2, 3, 4, 7]

def selection_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Selection Sort - 選擇排序，每次選最小值放到前面。"""
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if verbose:
            status = f"swap arr[{i}]↔arr[{min_idx}]" if min_idx != i else "已在正確位置"
            print(f"  Pass {i+1}: 未排序={a[i:]}, 最小值={a[min_idx]}(idx={min_idx}), {status}")
        a[i], a[min_idx] = a[min_idx], a[i]
        if verbose:
            print(f"          → {a}  已排序: {a[:i+1]}")
    return a


# ---------------------------------------------------------------------------
# 1-3. Insertion Sort (插入排序)
# ---------------------------------------------------------------------------
# 核心概念：像打撲克牌一樣，把每張新牌插入到手牌中的正確位置。
#
# Time: O(n^2) worst/avg, O(n) best (already sorted)
# Space: O(1), Stable: Yes, In-place: Yes
#
# 範例: arr = [5, 2, 4, 6, 1]
#
# 初始: [5 | 2, 4, 6, 1]  (| 左邊是已排序區)
# Pass 1: 取出 key=2, 比較 5>2 → 5右移 → 插入 → [2, 5 | 4, 6, 1]
# Pass 2: 取出 key=4, 比較 5>4 → 5右移, 比較 2>4? No → 插入 → [2, 4, 5 | 6, 1]
# Pass 3: 取出 key=6, 比較 5>6? No → 直接放入 → [2, 4, 5, 6 | 1]
# Pass 4: 取出 key=1, 比較 6>1,5>1,4>1,2>1 → 全部右移 → 插入 → [1, 2, 4, 5, 6]

def insertion_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Insertion Sort - 插入排序，像整理撲克牌。"""
    a = arr[:]
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        shifts = []
        while j >= 0 and a[j] > key:
            shifts.append(a[j])
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        if verbose:
            shift_str = ",".join(str(s) for s in shifts) if shifts else "無需移動"
            print(f"  Pass {i}: key={key}, 右移: [{shift_str}] → {a}")
    return a


# ============================================================================
# Section 2: 進階排序 (Advanced Sorts) - 面試必備
# ============================================================================


# ---------------------------------------------------------------------------
# 2-1. Merge Sort (合併排序) - Divide and Conquer
# ---------------------------------------------------------------------------
# 核心概念：
#   1. Divide: 把陣列切成兩半
#   2. Conquer: 遞迴排序左右兩半
#   3. Merge: 把兩個已排序的子陣列合併成一個
#
# Time: O(n log n) always, Space: O(n), Stable: Yes, In-place: No
#
# 範例 1: arr = [38, 27, 43, 3, 9, 82, 10]
#
# Split 階段:
# [38, 27, 43, 3, 9, 82, 10]
#    /                    \
# [38, 27, 43]        [3, 9, 82, 10]
#   /      \            /          \
# [38]  [27, 43]    [3, 9]    [82, 10]
#        /    \      /   \      /    \
#      [27]  [43]  [3]  [9]  [82]  [10]
#
# Merge 階段 (由下而上):
# merge([27], [43]) → [27, 43]    (27<43, 直接排好)
# merge([38], [27,43]) → [27, 38, 43]  (比較: 38>27→取27, 38<43→取38, 取43)
# merge([3], [9]) → [3, 9]
# merge([82], [10]) → [10, 82]
# merge([3,9], [10,82]) → [3, 9, 10, 82]
# merge([27,38,43], [3,9,10,82]) → [3, 9, 10, 27, 38, 43, 82]
#   比較過程: 27>3→取3, 27>9→取9, 27>10→取10, 27<82→取27, 38<82→取38, 43<82→取43, 取82
#
# 範例 2: arr = [5, 1, 4, 2]
# Split: [5,1] [4,2] → [5],[1] [4],[2]
# Merge: [1,5] [2,4] → [1,2,4,5]
#   比較: 1<2→取1, 5>2→取2, 5>4→取4, 取5
#
# 範例 3: arr = [3, 1]
# Split: [3], [1]
# Merge: 3>1 → [1, 3]  (最簡單的 case)

def merge_sort(arr: List[int], verbose: bool = False, depth: int = 0) -> List[int]:
    """Merge Sort - 合併排序，分治法經典應用。"""
    indent = "  " + "    " * depth
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    if verbose:
        print(f"{indent}Split: {arr} → {arr[:mid]} | {arr[mid:]}")

    left = merge_sort(arr[:mid], verbose, depth + 1)
    right = merge_sort(arr[mid:], verbose, depth + 1)

    # Merge two sorted halves
    result = []
    i = j = 0
    merge_steps = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merge_steps.append(f"{left[i]}<={right[j]}→取{left[i]}")
            result.append(left[i])
            i += 1
        else:
            merge_steps.append(f"{left[i]}>{right[j]}→取{right[j]}")
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])

    if verbose:
        print(f"{indent}Merge: {left} + {right} → {result}")
    return result


# ---------------------------------------------------------------------------
# 2-2. Quick Sort (快速排序) - 面試最常考
# ---------------------------------------------------------------------------
# 核心概念：
#   1. 選一個 pivot (樞紐)
#   2. Partition: 把小於 pivot 的放左邊，大於 pivot 的放右邊
#   3. 遞迴排序左右兩邊
#
# Time: O(n log n) avg, O(n^2) worst, Space: O(log n), Stable: No
#
# 範例 1: arr = [3, 6, 8, 10, 1, 2, 1]  pivot = arr[-1] = 1
#
# 初始: [3, 6, 8, 10, 1, 2, 1], pivot=1, i=-1
# j=0: 3>1, skip                          i=-1
# j=1: 6>1, skip                          i=-1
# j=2: 8>1, skip                          i=-1
# j=3: 10>1, skip                         i=-1
# j=4: 1<=1, i=0, swap arr[0]↔arr[4] → [1, 6, 8, 10, 3, 2, 1]
# j=5: 2>1, skip                          i=0
# 最後 swap arr[1]↔arr[6] (pivot) → [1, 1, 8, 10, 3, 2, 6]
# pivot index = 1
# 左邊: [1], 右邊: [8, 10, 3, 2, 6] → 遞迴排序
#
# 範例 2: arr = [10, 7, 8, 9, 1, 5], pivot = 5
# j=0: 10>5, skip         i=-1
# j=1: 7>5, skip          i=-1
# j=2: 8>5, skip          i=-1
# j=3: 9>5, skip          i=-1
# j=4: 1<=5, i=0, swap arr[0]↔arr[4] → [1, 7, 8, 9, 10, 5]
# 最後 swap arr[1]↔arr[5] → [1, 5, 8, 9, 10, 7]
# pivot index = 1, 左邊: [1], 右邊: [8, 9, 10, 7]
#
# 範例 3: arr = [2, 1, 3], pivot = 3
# j=0: 2<=3, i=0, swap arr[0]↔arr[0] → [2, 1, 3] (same)
# j=1: 1<=3, i=1, swap arr[1]↔arr[1] → [2, 1, 3] (same)
# 最後 swap arr[2]↔arr[2] → [2, 1, 3], pivot index=2
# 左邊 [2,1] 遞迴 → [1,2], 右邊 [] → 結果: [1, 2, 3]

def quick_sort(arr: List[int], verbose: bool = False, depth: int = 0) -> List[int]:
    """Quick Sort - 快速排序，使用 Lomuto partition。"""
    a = arr[:]
    _quick_sort_helper(a, 0, len(a) - 1, verbose, depth)
    return a

def _quick_sort_helper(a: List[int], low: int, high: int,
                        verbose: bool, depth: int) -> None:
    indent = "  " + "    " * depth
    if low < high:
        pivot_val = a[high]
        if verbose:
            print(f"{indent}QSort {a[low:high+1]}, pivot={pivot_val}")
        i = low - 1
        for j in range(low, high):
            if a[j] <= pivot_val:
                i += 1
                a[i], a[j] = a[j], a[i]
                if verbose:
                    print(f"{indent}  j={j}: {a[j]}<=pivot, swap → {a[low:high+1]}")
            else:
                if verbose:
                    print(f"{indent}  j={j}: {a[j]}>pivot, skip")
        a[i + 1], a[high] = a[high], a[i + 1]
        pi = i + 1
        if verbose:
            print(f"{indent}  Place pivot → {a[low:high+1]}, pivot at idx {pi}")
        _quick_sort_helper(a, low, pi - 1, verbose, depth + 1)
        _quick_sort_helper(a, pi + 1, high, verbose, depth + 1)


# ---------------------------------------------------------------------------
# 2-3. Heap Sort (堆積排序)
# ---------------------------------------------------------------------------
# 核心概念：
#   1. Build Max Heap: 把陣列變成 max heap
#   2. 反覆取出最大值 (root)，放到陣列尾端
#
# Time: O(n log n) always, Space: O(1), Stable: No, In-place: Yes
#
# 範例 1: arr = [4, 10, 3, 5, 1]
#
# Step 1 - Build Max Heap:
#   原始:        4            heapify 後:    10
#              /   \                        /    \
#            10     3                      5      3
#           /  \                          / \
#          5    1                        4   1
#   → Max Heap: [10, 5, 3, 4, 1]
#
# Step 2 - Extract max repeatedly:
#   swap root(10)↔last(1) → [1, 5, 3, 4, |10]  heapify → [5, 4, 3, 1, |10]
#   swap root(5)↔last(1)  → [1, 4, 3, |5, 10]  heapify → [4, 1, 3, |5, 10]
#   swap root(4)↔last(3)  → [3, 1, |4, 5, 10]  heapify → [3, 1, |4, 5, 10]
#   swap root(3)↔last(1)  → [1, |3, 4, 5, 10]  done!
#   結果: [1, 3, 4, 5, 10]
#
# 範例 2: arr = [12, 11, 13, 5, 6, 7]
# Build max heap: [13, 11, 12, 5, 6, 7]
# Extract: 13→末, heapify → [12, 11, 7, 5, 6, |13]
# Extract: 12→末, heapify → [11, 6, 7, 5, |12, 13]
# Extract: 11→末 → [7, 6, 5, |11, 12, 13]
# Extract: 7→末  → [6, 5, |7, 11, 12, 13]
# Extract: 6→末  → [5, |6, 7, 11, 12, 13]
# 結果: [5, 6, 7, 11, 12, 13]

def heap_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Heap Sort - 堆積排序，利用 max heap 反覆取最大值。"""
    a = arr[:]
    n = len(a)

    def heapify(size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size and a[left] > a[largest]:
            largest = left
        if right < size and a[right] > a[largest]:
            largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            heapify(size, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    if verbose:
        print(f"  Build Max Heap: {a}")

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        if verbose:
            print(f"  swap root({a[0]})↔last({a[i]})", end="")
        a[0], a[i] = a[i], a[0]
        heapify(i, 0)
        if verbose:
            print(f" → heapify → {a[:i]} | sorted: {a[i:]}")
    return a


# ---------------------------------------------------------------------------
# 2-4. Counting Sort (計數排序) - 特殊情況用
# ---------------------------------------------------------------------------
# 適用：元素範圍有限（如 0~k），不基於比較。
# Time: O(n + k), Space: O(k), Stable: Yes
#
# 範例: arr = [4, 2, 2, 8, 3, 3, 1]
# 找最大值 max=8, 建立 count[0..8]
# 計數: count = [0, 1, 2, 1, 1, 0, 0, 0, 1]
#                0  1  2  3  4  5  6  7  8
# 累積: count = [0, 1, 3, 4, 5, 5, 5, 5, 6]  (前綴和)
# 反向填入 output → [1, 2, 2, 3, 3, 4, 8]

def counting_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Counting Sort - 計數排序，非比較型，適用於有限範圍的整數。"""
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    if verbose:
        print(f"  Count array: {count}")
    # 直接展開
    result = []
    for val in range(len(count)):
        result.extend([val] * count[val])
    if verbose:
        print(f"  Result: {result}")
    return result


# ---------------------------------------------------------------------------
# 2-5. Radix Sort (基數排序) - 特殊情況用
# ---------------------------------------------------------------------------
# 核心：按位數排序，從最低位到最高位，每位用 stable sort (如 counting sort)。
# Time: O(d * (n + k)), d=位數, k=基數(10), Space: O(n + k)
#
# 範例: arr = [170, 45, 75, 90, 802, 24, 2, 66]
# 按個位: [170, 90, 802, 2, 24, 45, 75, 66]
# 按十位: [802, 2, 24, 45, 66, 170, 75, 90]
# 按百位: [2, 24, 45, 66, 75, 90, 170, 802]

def radix_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """Radix Sort - 基數排序，從最低位到最高位逐位排序。"""
    if not arr:
        return []
    a = arr[:]
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        # Counting sort by current digit
        output = [0] * len(a)
        count = [0] * 10
        for num in a:
            idx = (num // exp) % 10
            count[idx] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(len(a) - 1, -1, -1):
            idx = (a[i] // exp) % 10
            output[count[idx] - 1] = a[i]
            count[idx] -= 1
        a = output
        if verbose:
            digit_name = {1: "個位", 10: "十位", 100: "百位", 1000: "千位"}
            name = digit_name.get(exp, f"{exp}位")
            print(f"  按{name}: {a}")
        exp *= 10
    return a


# ============================================================================
# Section 3: 排序應用題 (Sorting Application Problems)
# ============================================================================


# ---------------------------------------------------------------------------
# 3-1. Sort Colors (LeetCode 75) - Dutch National Flag Problem
# ---------------------------------------------------------------------------
# 題意：陣列只含 0, 1, 2，原地排序。
# 解法：三指針 (low, mid, high)
#   - low: 下一個 0 該放的位置
#   - mid: 當前掃描位置
#   - high: 下一個 2 該放的位置
#
# 規則：
#   - arr[mid]==0: swap(arr[low], arr[mid]), low++, mid++
#   - arr[mid]==1: mid++ (1 在中間，不用動)
#   - arr[mid]==2: swap(arr[mid], arr[high]), high-- (mid 不動，因為換來的可能是 0)
#
# 範例 1: [2, 0, 2, 1, 1, 0]
# 初始: low=0, mid=0, high=5
# Step 1: arr[0]=2, swap arr[0]↔arr[5] → [0, 0, 2, 1, 1, 2], high=4
# Step 2: arr[0]=0, swap arr[0]↔arr[0] → [0, 0, 2, 1, 1, 2], low=1, mid=1
# Step 3: arr[1]=0, swap arr[1]↔arr[1] → [0, 0, 2, 1, 1, 2], low=2, mid=2
# Step 4: arr[2]=2, swap arr[2]↔arr[4] → [0, 0, 1, 1, 2, 2], high=3
# Step 5: arr[2]=1, mid=3
# Step 6: arr[3]=1, mid=4 > high=3 → 結束!
# 結果: [0, 0, 1, 1, 2, 2]
#
# 範例 2: [1, 0, 2]
# low=0, mid=0, high=2
# Step 1: arr[0]=1, mid++ → mid=1
# Step 2: arr[1]=0, swap arr[0]↔arr[1] → [0, 1, 2], low=1, mid=2
# Step 3: mid=2 > high=2? No. arr[2]=2, swap arr[2]↔arr[2] → [0, 1, 2], high=1
# Step 4: mid=2 > high=1 → 結束!
# 結果: [0, 1, 2]
#
# 範例 3: [2, 2, 0, 0, 1]
# low=0, mid=0, high=4
# Step 1: arr[0]=2, swap arr[0]↔arr[4] → [1, 2, 0, 0, 2], high=3
# Step 2: arr[0]=1, mid=1
# Step 3: arr[1]=2, swap arr[1]↔arr[3] → [1, 0, 0, 2, 2], high=2
# Step 4: arr[1]=0, swap arr[0]↔arr[1] → [0, 1, 0, 2, 2], low=1, mid=2
# Step 5: arr[2]=0, swap arr[1]↔arr[2] → [0, 0, 1, 2, 2], low=2, mid=3
# Step 6: mid=3 > high=2 → 結束!
# 結果: [0, 0, 1, 2, 2]

def sort_colors(nums: List[int], verbose: bool = False) -> List[int]:
    """Sort Colors (Dutch National Flag) - 三指針原地排序 0/1/2。"""
    a = nums[:]
    low, mid, high = 0, 0, len(a) - 1
    step = 0

    if verbose:
        print(f"  初始: {a}, low={low}, mid={mid}, high={high}")

    while mid <= high:
        step += 1
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            if verbose:
                print(f"  Step {step}: arr[{mid}]=0, swap arr[{low}]↔arr[{mid}] → {a}, low={low+1}, mid={mid+1}")
            low += 1
            mid += 1
        elif a[mid] == 1:
            if verbose:
                print(f"  Step {step}: arr[{mid}]=1, mid++ → mid={mid+1}")
            mid += 1
        else:  # a[mid] == 2
            a[mid], a[high] = a[high], a[mid]
            if verbose:
                print(f"  Step {step}: arr[{mid}]=2, swap arr[{mid}]↔arr[{high}] → {a}, high={high-1}")
            high -= 1
    return a


# ---------------------------------------------------------------------------
# 3-2. Merge Sorted Array (LeetCode 88)
# ---------------------------------------------------------------------------
# 題意：兩個已排序的陣列 nums1 (大小 m+n，後 n 位是 0) 和 nums2 (大小 n)，
#       把 nums2 merge 到 nums1 裡面。
#
# 關鍵技巧：從尾端開始 merge！避免覆蓋問題。
#
# 範例 1: nums1 = [1,2,3,0,0,0], m=3, nums2 = [2,5,6], n=3
# p1=2, p2=2, p=5
# Step 1: nums1[2]=3 vs nums2[2]=6 → 6>3 → nums1[5]=6, p2=1, p=4
# Step 2: nums1[2]=3 vs nums2[1]=5 → 5>3 → nums1[4]=5, p2=0, p=3
# Step 3: nums1[2]=3 vs nums2[0]=2 → 3>2 → nums1[3]=3, p1=1, p=2
# Step 4: nums1[1]=2 vs nums2[0]=2 → 2>=2 → nums1[2]=2, p1=0, p=1
# Step 5: nums1[0]=1 vs nums2[0]=2 → 2>1 → nums1[1]=2, p2=-1
# 結果: [1, 2, 2, 3, 5, 6]
#
# 範例 2: nums1 = [4,5,6,0,0,0], m=3, nums2 = [1,2,3], n=3
# p1=2, p2=2, p=5
# Step 1: 6>3 → nums1[5]=6, p1=1
# Step 2: 5>3 → nums1[4]=5, p1=0
# Step 3: 4>3 → nums1[3]=4, p1=-1
# p1<0, copy remaining nums2 → nums1[0..2] = [1,2,3]
# 結果: [1, 2, 3, 4, 5, 6]
#
# 範例 3: nums1 = [1], m=1, nums2 = [], n=0
# n=0, 不需要 merge → 結果: [1]

def merge_sorted_array(nums1: List[int], m: int, nums2: List[int], n: int,
                        verbose: bool = False) -> List[int]:
    """Merge Sorted Array - 從尾端 merge 兩個已排序陣列。"""
    p1, p2, p = m - 1, n - 1, m + n - 1
    step = 0

    while p1 >= 0 and p2 >= 0:
        step += 1
        if nums1[p1] >= nums2[p2]:
            if verbose:
                print(f"  Step {step}: nums1[{p1}]={nums1[p1]} >= nums2[{p2}]={nums2[p2]}"
                      f" → nums1[{p}]={nums1[p1]}")
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            if verbose:
                print(f"  Step {step}: nums2[{p2}]={nums2[p2]} > nums1[{p1}]={nums1[p1]}"
                      f" → nums1[{p}]={nums2[p2]}")
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1

    # Copy remaining nums2 elements (if any)
    while p2 >= 0:
        nums1[p] = nums2[p2]
        if verbose:
            print(f"  Copy remaining: nums1[{p}]={nums2[p2]}")
        p2 -= 1
        p -= 1

    return nums1


# ---------------------------------------------------------------------------
# 3-3. Sort List (LeetCode 148) - Merge Sort on Linked List
# ---------------------------------------------------------------------------
# 題意：對 linked list 排序，要求 O(n log n) time, O(1) space。
# 解法：用 merge sort (找中點 → 切半 → 遞迴 → 合併)
#
# 我們用 Python list 模擬 linked list 的行為，重點在展示 merge sort 邏輯。
#
# 範例 1: [4, 2, 1, 3]
# 找中點 → 切半: [4, 2] | [1, 3]
# 左邊 [4, 2] → 切半 [4] | [2] → merge → [2, 4]
# 右邊 [1, 3] → 切半 [1] | [3] → merge → [1, 3]
# merge [2, 4] + [1, 3]:
#   2>1→取1, 2<3→取2, 4>3→取3, 取4 → [1, 2, 3, 4]
#
# 範例 2: [-1, 5, 3, 4, 0]
# 切半: [-1, 5] | [3, 4, 0]
# [-1, 5] → [-1] | [5] → merge → [-1, 5]
# [3, 4, 0] → [3] | [4, 0] → [4] | [0] → merge → [0, 4]
#   merge [3] + [0, 4] → [0, 3, 4]
# merge [-1, 5] + [0, 3, 4]:
#   -1<0→取-1, 5>0→取0, 5>3→取3, 5>4→取4, 取5 → [-1, 0, 3, 4, 5]

class ListNode:
    """簡易 Linked List node。"""
    def __init__(self, val: int = 0, nxt: 'ListNode' = None):
        self.val = val
        self.next = nxt

def list_to_linked(arr: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def linked_to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def sort_list(head: Optional[ListNode], verbose: bool = False,
              depth: int = 0) -> Optional[ListNode]:
    """Sort List - 對 linked list 做 merge sort。"""
    indent = "  " + "    " * depth
    if not head or not head.next:
        return head

    if verbose:
        print(f"{indent}Sort: {linked_to_list(head)}")

    # Find middle using slow/fast pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None  # cut

    if verbose:
        print(f"{indent}  Split → {linked_to_list(head)} | {linked_to_list(mid)}")

    left = sort_list(head, verbose, depth + 1)
    right = sort_list(mid, verbose, depth + 1)

    # Merge two sorted lists
    dummy = ListNode(0)
    cur = dummy
    while left and right:
        if left.val <= right.val:
            cur.next = left
            left = left.next
        else:
            cur.next = right
            right = right.next
        cur = cur.next
    cur.next = left or right

    if verbose:
        print(f"{indent}  Merged → {linked_to_list(dummy.next)}")
    return dummy.next


# ---------------------------------------------------------------------------
# 3-4. Largest Number (LeetCode 179)
# ---------------------------------------------------------------------------
# 題意：給定一組非負整數，排列成最大的數字（回傳字串）。
# 關鍵：自訂比較器！比較 str(a)+str(b) vs str(b)+str(a)
#
# 範例 1: nums = [10, 2]
# "210" vs "102" → "210" > "102" → 2 排前面 → "210"
#
# 範例 2: nums = [3, 30, 34, 5, 9]
# 自訂排序: 比較拼接結果
#   9 vs 5: "95" vs "59" → 9 先
#   9 vs 34: "934" vs "349" → 9 先
#   5 vs 34: "534" vs "345" → 5 先
#   34 vs 3: "343" vs "334" → 34 先
#   3 vs 30: "330" vs "303" → 3 先
# 排序結果: [9, 5, 34, 3, 30] → "9534330"
#
# 範例 3: nums = [0, 0, 0]
# 全是 0 → 特殊處理回傳 "0" 而非 "000"

import functools

def largest_number(nums: List[int], verbose: bool = False) -> str:
    """Largest Number - 自訂比較器，將數字拼成最大值。"""
    strs = [str(n) for n in nums]

    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1  # a should come first
        elif a + b < b + a:
            return 1
        return 0

    strs.sort(key=functools.cmp_to_key(compare))

    if verbose:
        print(f"  排序後: {strs}")
        for i in range(len(strs)):
            for j in range(i + 1, min(i + 3, len(strs))):
                print(f"    比較 '{strs[i]}'+'{strs[j]}'="
                      f"'{strs[i]+strs[j]}' vs '{strs[j]+strs[i]}'")

    result = "".join(strs)
    if result[0] == "0":
        return "0"
    return result


# ============================================================================
# Section 4: 排序算法比較 (Sorting Algorithm Comparison)
# ============================================================================

def print_sort_comparison():
    """印出排序演算法完整比較表。"""
    print("""
  ┌──────────────┬───────────┬───────────┬───────────┬───────┬────────┬────────┐
  │ Algorithm    │ Best      │ Average   │ Worst     │ Space │ Stable │In-place│
  ├──────────────┼───────────┼───────────┼───────────┼───────┼────────┼────────┤
  │ Bubble Sort  │ O(n)      │ O(n^2)    │ O(n^2)    │ O(1)  │ Yes    │ Yes    │
  │ Selection    │ O(n^2)    │ O(n^2)    │ O(n^2)    │ O(1)  │ No     │ Yes    │
  │ Insertion    │ O(n)      │ O(n^2)    │ O(n^2)    │ O(1)  │ Yes    │ Yes    │
  │ Merge Sort   │ O(n logn) │ O(n logn) │ O(n logn) │ O(n)  │ Yes    │ No     │
  │ Quick Sort   │ O(n logn) │ O(n logn) │ O(n^2)    │O(logn)│ No     │ Yes    │
  │ Heap Sort    │ O(n logn) │ O(n logn) │ O(n logn) │ O(1)  │ No     │ Yes    │
  │ Counting     │ O(n+k)   │ O(n+k)    │ O(n+k)    │ O(k)  │ Yes    │ No     │
  │ Radix Sort   │ O(d(n+k))│ O(d(n+k)) │ O(d(n+k)) │O(n+k) │ Yes    │ No     │
  │ Timsort*     │ O(n)      │ O(n logn) │ O(n logn) │ O(n)  │ Yes    │ No     │
  └──────────────┴───────────┴───────────┴───────────┴───────┴────────┴────────┘
  * Timsort = Python 內建 sorted() / list.sort() 使用的演算法
    混合了 Merge Sort + Insertion Sort，在實務中表現極佳。

  何時用哪種排序？
  ┌──────────────────────────────────┬────────────────────────┐
  │ 情境                            │ 建議                    │
  ├──────────────────────────────────┼────────────────────────┤
  │ 一般面試題                       │ 直接用 sorted() / .sort()│
  │ 需要 stable sort                 │ Merge Sort / Timsort    │
  │ 資料量小 (<50)                   │ Insertion Sort          │
  │ 資料接近已排序                    │ Insertion Sort / Timsort│
  │ 需要 in-place + O(n logn)       │ Quick Sort / Heap Sort  │
  │ 整數且範圍有限                    │ Counting / Radix Sort   │
  │ Linked List 排序                │ Merge Sort              │
  └──────────────────────────────────┴────────────────────────┘
""")


# ████████████████████████████████████████████████████████████████████████████
# Part B: 位元運算 (Bit Manipulation)
# ████████████████████████████████████████████████████████████████████████████


# ============================================================================
# Section 5: 位元基礎 (Bit Basics)
# ============================================================================
# 六種基本位元運算：
#   AND (&)  : 兩個都是 1 才是 1
#   OR  (|)  : 有一個是 1 就是 1
#   XOR (^)  : 不同才是 1（相同為 0）
#   NOT (~)  : 0 變 1，1 變 0（Python 中 ~n = -(n+1)）
#   左移 (<<) : 所有位元左移，右邊補 0，等於 ×2
#   右移 (>>) : 所有位元右移，左邊補 0（正數），等於 ÷2
#
# 範例 1: a=5 (101), b=3 (011)
#   a & b = 101 & 011 = 001 = 1   (只有最低位都是 1)
#   a | b = 101 | 011 = 111 = 7   (三個位都有至少一個 1)
#   a ^ b = 101 ^ 011 = 110 = 6   (最高位和中間位不同)
#   ~a    = ~101 = ...11111010 = -6 (Python 用補數表示)
#   a << 1 = 1010 = 10             (左移一位 = ×2)
#   a >> 1 = 10 = 2               (右移一位 = ÷2，丟掉最低位)
#
# 範例 2: n=12 (1100), m=10 (1010)
#   n & m  = 1100 & 1010 = 1000 = 8
#   n | m  = 1100 | 1010 = 1110 = 14
#   n ^ m  = 1100 ^ 1010 = 0110 = 6
#   n << 2 = 110000 = 48           (左移兩位 = ×4)
#   n >> 2 = 11 = 3               (右移兩位 = ÷4)
#
# 範例 3: 重要 trick 展示 n=6 (110)
#   n & (n-1) = 110 & 101 = 100 = 4  (移除最低的 set bit)
#   n & (-n)  = 110 & 010 = 010 = 2  (isolate 最低的 set bit)
#   解釋：-n 在二的補數中是 ~n + 1
#     -6 = ~110 + 1 = ...11111001 + 1 = ...11111010
#     6 & -6 = 000...110 & 111...010 = 000...010 = 2
#
# XOR 三大性質：
#   a ^ a = 0  (自己 XOR 自己 = 0)
#   a ^ 0 = a  (任何數 XOR 0 = 自己)
#   交換律 + 結合律: a ^ b ^ a = b
# ============================================================================

def bit_basics_demo(verbose: bool = False):
    """展示位元運算基礎。"""
    if not verbose:
        return
    pairs = [(5, 3), (12, 10)]
    for a, b in pairs:
        print(f"\n  a={a} ({bin(a)}), b={b} ({bin(b)})")
        print(f"    a & b  = {bin(a)} & {bin(b)} = {bin(a & b)} = {a & b}")
        print(f"    a | b  = {bin(a)} | {bin(b)} = {bin(a | b)} = {a | b}")
        print(f"    a ^ b  = {bin(a)} ^ {bin(b)} = {bin(a ^ b)} = {a ^ b}")
        print(f"    a << 1 = {bin(a << 1)} = {a << 1}")
        print(f"    a >> 1 = {bin(a >> 1)} = {a >> 1}")

    print("\n  --- 重要 Tricks ---")
    for n in [6, 12, 10]:
        print(f"  n={n} ({bin(n)}):")
        print(f"    n & (n-1) = {bin(n)} & {bin(n-1)} = {bin(n & (n-1))} = {n & (n-1)}"
              f"  (移除最低 set bit)")
        print(f"    n & (-n)  = {n & (-n)}  (isolate 最低 set bit)")


# ============================================================================
# Section 6: 位元應用題 (Bit Manipulation Problems)
# ============================================================================


# ---------------------------------------------------------------------------
# 6-1. Single Number (LeetCode 136)
# ---------------------------------------------------------------------------
# 題意：每個元素出現兩次，只有一個出現一次，找出它。
# 解法：XOR 所有元素！因為 a^a=0, a^0=a
#
# 範例 1: nums = [2, 2, 1]
# 計算過程 (用 binary):
#   result = 0          (000)
#   result ^= 2: 000 ^ 010 = 010 (=2)
#   result ^= 2: 010 ^ 010 = 000 (=0)  ← 2^2 抵消了!
#   result ^= 1: 000 ^ 001 = 001 (=1)  ← 剩下 1
#   答案: 1
#
# 範例 2: nums = [4, 1, 2, 1, 2]
#   result = 0          (000)
#   result ^= 4: 000 ^ 100 = 100 (=4)
#   result ^= 1: 100 ^ 001 = 101 (=5)
#   result ^= 2: 101 ^ 010 = 111 (=7)
#   result ^= 1: 111 ^ 001 = 110 (=6)  ← 1^1 抵消
#   result ^= 2: 110 ^ 010 = 100 (=4)  ← 2^2 抵消
#   答案: 4
#
# 範例 3: nums = [1]
#   result = 0 ^ 1 = 1  (只有一個元素)

def single_number(nums: List[int], verbose: bool = False) -> int:
    """Single Number - XOR 所有元素，成對的會抵消。"""
    result = 0
    for num in nums:
        old = result
        result ^= num
        if verbose:
            print(f"  result ^= {num}: {bin(old)} ^ {bin(num)} = {bin(result)} (={result})")
    return result


# ---------------------------------------------------------------------------
# 6-2. Number of 1 Bits (LeetCode 191) - Hamming Weight
# ---------------------------------------------------------------------------
# 題意：給定一個整數，計算其二進位表示中 1 的個數。
# 解法：反覆用 n & (n-1) 移除最低的 set bit，計數幾次變成 0。
#
# 範例 1: n = 11 (binary: 1011)
#   n=1011, n-1=1010, n&(n-1)=1010 → count=1 (移除最低位的 1)
#   n=1010, n-1=1001, n&(n-1)=1000 → count=2
#   n=1000, n-1=0111, n&(n-1)=0000 → count=3
#   n=0 → 結束! 答案: 3
#
# 範例 2: n = 128 (binary: 10000000)
#   n=10000000, n-1=01111111, n&(n-1)=00000000 → count=1
#   n=0 → 結束! 答案: 1  (只有一個 1)
#
# 範例 3: n = 15 (binary: 1111)
#   n=1111, n&(n-1)=1110 → count=1
#   n=1110, n&(n-1)=1100 → count=2
#   n=1100, n&(n-1)=1000 → count=3
#   n=1000, n&(n-1)=0000 → count=4
#   答案: 4

def hamming_weight(n: int, verbose: bool = False) -> int:
    """Number of 1 Bits - 用 n & (n-1) 反覆移除最低 set bit。"""
    count = 0
    while n:
        old_n = n
        n &= (n - 1)
        count += 1
        if verbose:
            print(f"  n={bin(old_n)}, n&(n-1)={bin(n)} → count={count}")
    return count


# ---------------------------------------------------------------------------
# 6-3. Counting Bits (LeetCode 338)
# ---------------------------------------------------------------------------
# 題意：給定 n，回傳 [0, 1, ..., n] 中每個數字的 1 的個數。
# 解法：dp[i] = dp[i & (i-1)] + 1  (移除最低 set bit 後 +1)
#
# 範例 1: n = 5
# dp[0] = 0                          (0 = 0b0)
# dp[1] = dp[1&0] + 1 = dp[0]+1 = 1  (1 = 0b1)
# dp[2] = dp[2&1] + 1 = dp[0]+1 = 1  (2 = 0b10)
# dp[3] = dp[3&2] + 1 = dp[2]+1 = 2  (3 = 0b11)
# dp[4] = dp[4&3] + 1 = dp[0]+1 = 1  (4 = 0b100)
# dp[5] = dp[5&4] + 1 = dp[4]+1 = 2  (5 = 0b101)
# 答案: [0, 1, 1, 2, 1, 2]
#
# 範例 2: n = 2
# dp = [0, 1, 1]
#
# 範例 3: n = 8
# dp = [0, 1, 1, 2, 1, 2, 2, 3, 1]
# 注意 dp[8]=1 因為 8=1000，只有一個 1

def counting_bits(n: int, verbose: bool = False) -> List[int]:
    """Counting Bits - DP，dp[i] = dp[i & (i-1)] + 1。"""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i & (i - 1)] + 1
        if verbose:
            print(f"  dp[{i}] = dp[{i}&{i-1}] + 1 = dp[{i & (i-1)}]+1 = {dp[i]}"
                  f"  ({i} = {bin(i)})")
    return dp


# ---------------------------------------------------------------------------
# 6-4. Power of Two (LeetCode 231)
# ---------------------------------------------------------------------------
# 題意：判斷一個數是不是 2 的冪。
# 解法：2 的冪只有一個 set bit → n > 0 and n & (n-1) == 0
#
# 範例 1: n = 16 (binary: 10000)
#   n > 0? Yes.
#   n & (n-1) = 10000 & 01111 = 00000 = 0 ✓ → True
#
# 範例 2: n = 6 (binary: 110)
#   n > 0? Yes.
#   n & (n-1) = 110 & 101 = 100 = 4 ≠ 0 → False
#
# 範例 3: n = 1 (binary: 1)
#   n > 0? Yes.
#   n & (n-1) = 1 & 0 = 0 ✓ → True (2^0 = 1)

def is_power_of_two(n: int, verbose: bool = False) -> bool:
    """Power of Two - 2 的冪只有一個 set bit。"""
    if verbose:
        if n > 0:
            print(f"  n={n} ({bin(n)}), n&(n-1) = {bin(n)} & {bin(n-1)} = "
                  f"{bin(n & (n-1))} = {n & (n-1)}")
        else:
            print(f"  n={n}, not positive → False")
    return n > 0 and (n & (n - 1)) == 0


# ---------------------------------------------------------------------------
# 6-5. Missing Number (LeetCode 268)
# ---------------------------------------------------------------------------
# 題意：給定 [0, n] 範圍內的 n 個不同整數，找出缺少的那個。
# 解法：XOR！把索引和值全部 XOR，成對的抵消，剩下的就是缺少的。
#
# 範例 1: nums = [3, 0, 1]  (n=3, 範圍 [0,3])
#   XOR 所有 index: 0 ^ 1 ^ 2 = 3
#   XOR 所有 value: 3 ^ 0 ^ 1 = 2
#   XOR(index) ^ XOR(value) = 3 ^ 2 = 1?
#   不對，更簡單的做法：初始 result = n，然後 XOR 所有 i ^ nums[i]
#   result = 3 (= n)
#   i=0: result ^= 0 ^ 3 = 3 ^ 0 ^ 3 = 0
#   i=1: result ^= 1 ^ 0 = 0 ^ 1 ^ 0 = 1
#   i=2: result ^= 2 ^ 1 = 1 ^ 2 ^ 1 = 2
#   答案: 2 ✓
#
# 範例 2: nums = [0, 1]  (n=2, 範圍 [0,2])
#   result = 2
#   i=0: result ^= 0 ^ 0 = 2
#   i=1: result ^= 1 ^ 1 = 2
#   答案: 2 ✓
#
# 範例 3: nums = [9,6,4,2,3,5,7,0,1]  (n=9, 範圍 [0,9])
#   result = 9
#   依序 XOR... 最後 result = 8
#   答案: 8 ✓

def missing_number(nums: List[int], verbose: bool = False) -> int:
    """Missing Number - XOR 索引和值，成對抵消找出缺少的數。"""
    n = len(nums)
    result = n  # 初始化為 n
    if verbose:
        print(f"  初始 result = {n} (= len)")
    for i in range(n):
        old = result
        result ^= i ^ nums[i]
        if verbose:
            print(f"  i={i}: result ^= {i} ^ {nums[i]} = {old} ^ {i} ^ {nums[i]} = {result}")
    return result


# ---------------------------------------------------------------------------
# 6-6. Reverse Bits (LeetCode 190)
# ---------------------------------------------------------------------------
# 題意：反轉一個 32-bit 無號整數的位元。
# 解法：逐位取出，放到結果的對稱位置。
#
# 範例 1: n = 13 (binary: 00000000000000000000000000001101)
#   反轉後: 10110000000000000000000000000000 = 2952790016
#   過程 (只顯示非零步驟):
#   bit 0: n的第0位=1 → 放到result的第31位 → result |= (1<<31)
#   bit 2: n的第2位=1 → 放到result的第29位 → result |= (1<<29)
#   bit 3: n的第3位=1 → 放到result的第28位 → result |= (1<<28)
#
# 範例 2: n = 43261596 (binary: 00000010100101000001111010011100)
#   反轉後: 964176192

def reverse_bits(n: int, verbose: bool = False) -> int:
    """Reverse Bits - 逐位反轉 32-bit 整數。"""
    result = 0
    for i in range(32):
        bit = (n >> i) & 1
        if bit:
            result |= (1 << (31 - i))
            if verbose:
                print(f"  bit {i}: n的第{i}位=1 → 放到result的第{31-i}位")
    if verbose:
        print(f"  Result: {result} ({bin(result)})")
    return result


# ============================================================================
# Section 7: 位元進階 (Advanced Bit Manipulation)
# ============================================================================


# ---------------------------------------------------------------------------
# 7-1. Single Number II (LeetCode 137)
# ---------------------------------------------------------------------------
# 題意：每個元素出現三次，只有一個出現一次，找出它。
# 解法：對每一個 bit 位計算所有數字在該位的 1 的個數，mod 3 就是答案在該位的值。
#
# 範例 1: nums = [2, 2, 3, 2]
#   2 = 10, 2 = 10, 3 = 11, 2 = 10
#   bit 0: 0+0+1+0 = 1, 1 % 3 = 1
#   bit 1: 1+1+1+1 = 4, 4 % 3 = 1
#   答案: 11 (binary) = 3 ✓
#
# 範例 2: nums = [0, 1, 0, 1, 0, 1, 99]
#   99 = 1100011
#   bit 0: 0+1+0+1+0+1+1 = 4, 4%3 = 1
#   bit 1: 0+0+0+0+0+0+1 = 1, 1%3 = 1
#   bit 5: 0+0+0+0+0+0+1 = 1, 1%3 = 1
#   bit 6: 0+0+0+0+0+0+1 = 1, 1%3 = 1
#   答案: 1100011 = 99 ✓

def single_number_ii(nums: List[int], verbose: bool = False) -> int:
    """Single Number II - 統計每個 bit 的 1 個數，mod 3。"""
    result = 0
    for i in range(32):
        bit_sum = 0
        for num in nums:
            bit_sum += (num >> i) & 1
        if bit_sum % 3:
            result |= (1 << i)
            if verbose:
                print(f"  bit {i}: sum={bit_sum}, {bit_sum}%3={bit_sum%3} → set bit {i}")
    # Handle negative numbers in Python (32-bit two's complement)
    if result >= (1 << 31):
        result -= (1 << 32)
    if verbose:
        print(f"  答案: {result}")
    return result


# ---------------------------------------------------------------------------
# 7-2. Subsets (LeetCode 78) - Bitmask 解法
# ---------------------------------------------------------------------------
# 題意：給定一個不含重複元素的整數陣列，回傳所有子集。
# 解法：用 bitmask！n 個元素有 2^n 個子集，每個子集對應一個 n-bit 的數字。
#
# 範例 1: nums = [1, 2, 3]  (n=3, 共 2^3=8 個子集)
#   mask=000 (0) → []
#   mask=001 (1) → [1]        (第0位=1 → 選 nums[0])
#   mask=010 (2) → [2]        (第1位=1 → 選 nums[1])
#   mask=011 (3) → [1, 2]     (第0,1位=1 → 選 nums[0], nums[1])
#   mask=100 (4) → [3]
#   mask=101 (5) → [1, 3]
#   mask=110 (6) → [2, 3]
#   mask=111 (7) → [1, 2, 3]
#
# 範例 2: nums = [0]  (n=1, 共 2 個子集)
#   mask=0 → []
#   mask=1 → [0]
#
# 範例 3: nums = [1, 2]  (n=2, 共 4 個子集)
#   mask=00 (0) → []
#   mask=01 (1) → [1]
#   mask=10 (2) → [2]
#   mask=11 (3) → [1, 2]

def subsets_bitmask(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """Subsets - 用 bitmask 枚舉所有子集。"""
    n = len(nums)
    total = 1 << n  # 2^n
    result = []

    for mask in range(total):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
        if verbose:
            bits = format(mask, f'0{n}b')
            print(f"  mask={bits} ({mask}) → {subset}")
    return result


# ============================================================================
# main() - 執行所有範例
# ============================================================================

def main():
    print("=" * 72)
    print("Part A: 排序演算法 (Sorting Algorithms)")
    print("=" * 72)

    # --- Section 1: 基礎排序 ---
    print("\n" + "─" * 72)
    print("Section 1: 基礎排序 (Basic Sorts)")
    print("─" * 72)

    print("\n【1-1】Bubble Sort 泡沫排序")
    arr = [5, 3, 8, 1, 2]
    print(f"  Input: {arr}")
    result = bubble_sort(arr, verbose=True)
    print(f"  Output: {result}")
    assert result == sorted(arr)

    print("\n【1-2】Selection Sort 選擇排序")
    arr = [4, 2, 7, 1, 3]
    print(f"  Input: {arr}")
    result = selection_sort(arr, verbose=True)
    print(f"  Output: {result}")
    assert result == sorted(arr)

    print("\n【1-3】Insertion Sort 插入排序")
    arr = [5, 2, 4, 6, 1]
    print(f"  Input: {arr}")
    result = insertion_sort(arr, verbose=True)
    print(f"  Output: {result}")
    assert result == sorted(arr)

    # --- Section 2: 進階排序 ---
    print("\n" + "─" * 72)
    print("Section 2: 進階排序 (Advanced Sorts)")
    print("─" * 72)

    print("\n【2-1】Merge Sort 合併排序")
    for arr in [[38, 27, 43, 3, 9, 82, 10], [5, 1, 4, 2], [3, 1]]:
        print(f"\n  Input: {arr}")
        result = merge_sort(arr, verbose=True)
        print(f"  Output: {result}")
        assert result == sorted(arr)

    print("\n【2-2】Quick Sort 快速排序")
    for arr in [[3, 6, 8, 10, 1, 2, 1], [10, 7, 8, 9, 1, 5], [2, 1, 3]]:
        print(f"\n  Input: {arr}")
        result = quick_sort(arr, verbose=True)
        print(f"  Output: {result}")
        assert result == sorted(arr)

    print("\n【2-3】Heap Sort 堆積排序")
    for arr in [[4, 10, 3, 5, 1], [12, 11, 13, 5, 6, 7]]:
        print(f"\n  Input: {arr}")
        result = heap_sort(arr, verbose=True)
        print(f"  Output: {result}")
        assert result == sorted(arr)

    print("\n【2-4】Counting Sort 計數排序")
    arr = [4, 2, 2, 8, 3, 3, 1]
    print(f"  Input: {arr}")
    result = counting_sort(arr, verbose=True)
    print(f"  Output: {result}")
    assert result == sorted(arr)

    print("\n【2-5】Radix Sort 基數排序")
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"  Input: {arr}")
    result = radix_sort(arr, verbose=True)
    print(f"  Output: {result}")
    assert result == sorted(arr)

    # --- Section 3: 排序應用題 ---
    print("\n" + "─" * 72)
    print("Section 3: 排序應用題 (Sorting Application Problems)")
    print("─" * 72)

    print("\n【3-1】Sort Colors (Dutch National Flag)")
    for arr in [[2, 0, 2, 1, 1, 0], [1, 0, 2], [2, 2, 0, 0, 1]]:
        print(f"\n  Input: {arr}")
        result = sort_colors(arr, verbose=True)
        print(f"  Output: {result}")
        assert result == sorted(arr)

    print("\n【3-2】Merge Sorted Array")
    cases = [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3),
        ([1], 1, [], 0),
    ]
    for nums1, m, nums2, n in cases:
        print(f"\n  Input: nums1={nums1}, m={m}, nums2={nums2}, n={n}")
        result = merge_sorted_array(nums1[:], m, nums2[:], n, verbose=True)
        print(f"  Output: {result}")

    print("\n【3-3】Sort List (Merge Sort on Linked List)")
    for arr in [[4, 2, 1, 3], [-1, 5, 3, 4, 0]]:
        print(f"\n  Input: {arr}")
        head = list_to_linked(arr)
        sorted_head = sort_list(head, verbose=True)
        result = linked_to_list(sorted_head)
        print(f"  Output: {result}")
        assert result == sorted(arr)

    print("\n【3-4】Largest Number")
    for nums in [[10, 2], [3, 30, 34, 5, 9], [0, 0, 0]]:
        print(f"\n  Input: {nums}")
        result = largest_number(nums, verbose=True)
        print(f"  Output: \"{result}\"")

    # --- Section 4: 排序算法比較 ---
    print("\n" + "─" * 72)
    print("Section 4: 排序算法比較表")
    print("─" * 72)
    print_sort_comparison()

    # ====================================================================
    print("\n" + "=" * 72)
    print("Part B: 位元運算 (Bit Manipulation)")
    print("=" * 72)

    # --- Section 5: 位元基礎 ---
    print("\n" + "─" * 72)
    print("Section 5: 位元基礎 (Bit Basics)")
    print("─" * 72)
    bit_basics_demo(verbose=True)

    # --- Section 6: 位元應用題 ---
    print("\n" + "─" * 72)
    print("Section 6: 位元應用題 (Bit Manipulation Problems)")
    print("─" * 72)

    print("\n【6-1】Single Number (XOR)")
    for nums in [[2, 2, 1], [4, 1, 2, 1, 2], [1]]:
        print(f"\n  Input: {nums}")
        result = single_number(nums, verbose=True)
        print(f"  答案: {result}")

    print("\n【6-2】Number of 1 Bits (Hamming Weight)")
    for n in [11, 128, 15]:
        print(f"\n  Input: n={n} ({bin(n)})")
        result = hamming_weight(n, verbose=True)
        print(f"  答案: {result}")

    print("\n【6-3】Counting Bits")
    for n in [5, 2, 8]:
        print(f"\n  Input: n={n}")
        result = counting_bits(n, verbose=True)
        print(f"  答案: {result}")

    print("\n【6-4】Power of Two")
    for n in [16, 6, 1]:
        print(f"\n  Input: n={n}")
        result = is_power_of_two(n, verbose=True)
        print(f"  答案: {result}")

    print("\n【6-5】Missing Number (XOR)")
    for nums in [[3, 0, 1], [0, 1], [9, 6, 4, 2, 3, 5, 7, 0, 1]]:
        print(f"\n  Input: {nums}")
        result = missing_number(nums, verbose=True)
        print(f"  答案: {result}")

    print("\n【6-6】Reverse Bits")
    for n in [13, 43261596]:
        print(f"\n  Input: n={n} ({bin(n)})")
        result = reverse_bits(n, verbose=True)
        print(f"  答案: {result}")

    # --- Section 7: 位元進階 ---
    print("\n" + "─" * 72)
    print("Section 7: 位元進階 (Advanced Bit Manipulation)")
    print("─" * 72)

    print("\n【7-1】Single Number II (每個元素出現 3 次)")
    for nums in [[2, 2, 3, 2], [0, 1, 0, 1, 0, 1, 99]]:
        print(f"\n  Input: {nums}")
        result = single_number_ii(nums, verbose=True)
        print(f"  答案: {result}")

    print("\n【7-2】Subsets (Bitmask)")
    for nums in [[1, 2, 3], [0], [1, 2]]:
        print(f"\n  Input: {nums}")
        result = subsets_bitmask(nums, verbose=True)
        print(f"  共 {len(result)} 個子集")

    print("\n" + "=" * 72)
    print("全部測試通過！排序演算法 + 位元運算攻略完成！")
    print("=" * 72)


if __name__ == "__main__":
    main()
