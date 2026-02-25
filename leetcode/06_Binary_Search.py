"""
=============================================================================
  LeetCode 06 - Binary Search 二分搜尋完整攻略
  Target: Google / NVIDIA 面試準備
  Level: Beginner → Intermediate
  Style: 每題 3 組 step-by-step 數值追蹤 (Traditional Chinese + English)
=============================================================================

目錄 Table of Contents:
  Section 1: 標準二分搜尋 (Standard Binary Search)
  Section 2: 左邊界 vs 右邊界 — 三種模板 (Three Templates)
  Section 3: 旋轉數組 (Rotated Array)
  Section 4: 答案二分 (Binary Search on Answer)
  Section 5: 矩陣二分 (Matrix Binary Search)
  Section 6: 三種模板完整比較 (Template Decision Tree)
"""

from typing import List, Optional, Tuple
import math

# =============================================================================
# Section 1: 標準二分搜尋 (Standard Binary Search)
# =============================================================================

# -----------------------------------------------------------------------------
# 1-1: Classic Binary Search 經典二分搜尋
# LeetCode 704. Binary Search
# 核心觀念: 每次砍掉一半搜尋空間 → O(log n)
# Template 1: while left <= right
# -----------------------------------------------------------------------------
def binary_search(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    在排序陣列中搜尋 target，找到回傳 index，找不到回傳 -1。
    時間 O(log n) / 空間 O(1)
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2  # 防溢位寫法 (avoid overflow)
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓ → return {mid}")
            return mid
        elif nums[mid] < target:
            if verbose:
                print(f" < {target} → left={mid + 1}")
            left = mid + 1
        else:
            if verbose:
                print(f" > {target} → right={mid - 1}")
            right = mid - 1

    if verbose:
        print(f"  Loop ended: left={left} > right={right} → not found, return -1")
    return -1


def demo_binary_search():
    print("=" * 70)
    print("1-1: Classic Binary Search 經典二分搜尋 (LeetCode 704)")
    print("=" * 70)

    # 範例 1: 找到 target（中間位置）
    nums1 = [1, 3, 5, 7, 9, 11]
    target1 = 7
    print(f"\n範例 1: nums={nums1}, target={target1}")
    print(f"  預期: 7 在 index 3 → return 3")
    # Step 1: left=0, right=5, mid=2 → nums[2]=5 < 7 → left=3
    # Step 2: left=3, right=5, mid=4 → nums[4]=9 > 7 → right=3
    # Step 3: left=3, right=3, mid=3 → nums[3]=7 == target ✓ → return 3
    result = binary_search(nums1, target1, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 2: target 不存在
    nums2 = [2, 4, 6, 8, 10]
    target2 = 5
    print(f"範例 2: nums={nums2}, target={target2}")
    print(f"  預期: 5 不存在 → return -1")
    # Step 1: left=0, right=4, mid=2 → nums[2]=6 > 5 → right=1
    # Step 2: left=0, right=1, mid=0 → nums[0]=2 < 5 → left=1
    # Step 3: left=1, right=1, mid=1 → nums[1]=4 < 5 → left=2
    # Loop ended: left=2 > right=1 → not found
    result = binary_search(nums2, target2, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 3: 邊界情況 — target 在最後一個元素
    nums3 = [1]
    target3 = 1
    print(f"範例 3 (edge case): nums={nums3}, target={target3}")
    print(f"  預期: 唯一元素就是 target → return 0")
    # Step 1: left=0, right=0, mid=0 → nums[0]=1 == target ✓ → return 0
    result = binary_search(nums3, target3, verbose=True)
    print(f"  結果: {result}\n")


# -----------------------------------------------------------------------------
# 1-2: Search Insert Position 搜尋插入位置
# LeetCode 35
# 核心: 找不到時 left 就是該插入的位置
# -----------------------------------------------------------------------------
def search_insert(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    找到 target 回傳 index；找不到回傳應插入的位置。
    關鍵洞見: 迴圈結束時 left 就是插入點 (第一個 >= target 的位置)
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓ → return {mid}")
            return mid
        elif nums[mid] < target:
            if verbose:
                print(f" < {target} → left={mid + 1}")
            left = mid + 1
        else:
            if verbose:
                print(f" > {target} → right={mid - 1}")
            right = mid - 1

    if verbose:
        print(f"  Loop ended: left={left} → insert position = {left}")
    return left


def demo_search_insert():
    print("=" * 70)
    print("1-2: Search Insert Position 搜尋插入位置 (LeetCode 35)")
    print("=" * 70)

    # 範例 1: target 存在
    nums1 = [1, 3, 5, 6]
    target1 = 5
    print(f"\n範例 1: nums={nums1}, target={target1}")
    print(f"  預期: 5 在 index 2 → return 2")
    # Step 1: left=0, right=3, mid=1 → nums[1]=3 < 5 → left=2
    # Step 2: left=2, right=3, mid=2 → nums[2]=5 == 5 ✓ → return 2
    result = search_insert(nums1, target1, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 2: target 不存在，插在中間
    nums2 = [1, 3, 5, 6]
    target2 = 4
    print(f"範例 2: nums={nums2}, target={target2}")
    print(f"  預期: 4 應插在 index 2 (在3和5之間) → return 2")
    # Step 1: left=0, right=3, mid=1 → nums[1]=3 < 4 → left=2
    # Step 2: left=2, right=3, mid=2 → nums[2]=5 > 4 → right=1
    # Loop ended: left=2 → insert position = 2
    result = search_insert(nums2, target2, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 3: target 比所有元素都大
    nums3 = [1, 3, 5, 6]
    target3 = 7
    print(f"範例 3: nums={nums3}, target={target3}")
    print(f"  預期: 7 比所有都大 → 插在最後 → return 4")
    # Step 1: left=0, right=3, mid=1 → nums[1]=3 < 7 → left=2
    # Step 2: left=2, right=3, mid=2 → nums[2]=5 < 7 → left=3
    # Step 3: left=3, right=3, mid=3 → nums[3]=6 < 7 → left=4
    # Loop ended: left=4 → insert position = 4
    result = search_insert(nums3, target3, verbose=True)
    print(f"  結果: {result}\n")


# -----------------------------------------------------------------------------
# 1-3: First and Last Position 第一個和最後一個位置
# LeetCode 34. Find First and Last Position of Element in Sorted Array
# 核心: 分別用 left bound 和 right bound 兩次二分
# -----------------------------------------------------------------------------
def find_first_position(nums: List[int], target: int, verbose: bool = False) -> int:
    """找 target 的最左邊出現位置 (left bound)"""
    left, right = 0, len(nums) - 1
    result = -1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  [左界] Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            result = mid  # 記錄候選答案，但繼續往左找
            if verbose:
                print(f" == {target} → 記錄 result={mid}, right={mid - 1} (繼續往左)")
            right = mid - 1
        elif nums[mid] < target:
            if verbose:
                print(f" < {target} → left={mid + 1}")
            left = mid + 1
        else:
            if verbose:
                print(f" > {target} → right={mid - 1}")
            right = mid - 1

    if verbose:
        print(f"  [左界] 最終: result={result}")
    return result


def find_last_position(nums: List[int], target: int, verbose: bool = False) -> int:
    """找 target 的最右邊出現位置 (right bound)"""
    left, right = 0, len(nums) - 1
    result = -1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  [右界] Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            result = mid  # 記錄候選答案，但繼續往右找
            if verbose:
                print(f" == {target} → 記錄 result={mid}, left={mid + 1} (繼續往右)")
            left = mid + 1
        elif nums[mid] < target:
            if verbose:
                print(f" < {target} → left={mid + 1}")
            left = mid + 1
        else:
            if verbose:
                print(f" > {target} → right={mid - 1}")
            right = mid - 1

    if verbose:
        print(f"  [右界] 最終: result={result}")
    return result


def search_range(nums: List[int], target: int, verbose: bool = False) -> List[int]:
    """回傳 [first, last] 出現位置"""
    first = find_first_position(nums, target, verbose)
    last = find_last_position(nums, target, verbose)
    return [first, last]


def demo_search_range():
    print("=" * 70)
    print("1-3: First and Last Position (LeetCode 34)")
    print("=" * 70)

    # 範例 1: 多個重複元素
    nums1 = [5, 7, 7, 8, 8, 8, 10]
    target1 = 8
    print(f"\n範例 1: nums={nums1}, target={target1}")
    print(f"  預期: 8 出現在 index 3~5 → [3, 5]")
    result = search_range(nums1, target1, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 2: target 只出現一次
    nums2 = [1, 2, 3, 4, 5]
    target2 = 3
    print(f"範例 2: nums={nums2}, target={target2}")
    print(f"  預期: 3 只在 index 2 → [2, 2]")
    result = search_range(nums2, target2, verbose=True)
    print(f"  結果: {result}\n")

    # 範例 3: target 不存在
    nums3 = [5, 7, 7, 8, 8, 10]
    target3 = 6
    print(f"範例 3: nums={nums3}, target={target3}")
    print(f"  預期: 6 不存在 → [-1, -1]")
    result = search_range(nums3, target3, verbose=True)
    print(f"  結果: {result}\n")


# =============================================================================
# Section 2: 左邊界 vs 右邊界 — 三種模板 (Three Templates)
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │ Template 1: while left <= right      → 精確查找              │
# │ Template 2: while left < right       → 找邊界 (不會錯過)     │
# │ Template 3: while left + 1 < right   → 永不越界 (最安全)     │
# └─────────────────────────────────────────────────────────────────┘

# -----------------------------------------------------------------------------
# 2-1: Template 1 — while left <= right (Standard)
# 用途: 精確查找某個值，搜尋空間每步縮小，結束時 left > right
# -----------------------------------------------------------------------------
def template1_standard(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    Template 1: while left <= right
    特點: 搜尋區間 [left, right]，每次排除 mid
    結束條件: left > right (搜尋空間為空)
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left <= right:  # 注意: <= (閉區間)
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")
        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓")
            return mid
        elif nums[mid] < target:
            left = mid + 1  # mid 已檢查，排除
            if verbose:
                print(f" < {target} → left={left}")
        else:
            right = mid - 1  # mid 已檢查，排除
            if verbose:
                print(f" > {target} → right={right}")
    if verbose:
        print(f"  結束: left={left}, right={right} → not found")
    return -1


# -----------------------------------------------------------------------------
# 2-2: Template 2 — while left < right (Left Bound)
# 用途: 找第一個滿足條件的位置，結束時 left == right
# -----------------------------------------------------------------------------
def template2_left_bound(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    Template 2: while left < right
    特點: 搜尋區間 [left, right)，結束時 left == right 就是答案
    用途: 找第一個 >= target 的位置 (lower_bound)
    """
    left, right = 0, len(nums)  # 注意: right = len(nums)，右開
    step = 0

    while left < right:  # 注意: < (不是 <=)
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")
        if nums[mid] >= target:  # 找第一個 >= target
            right = mid  # 注意: right = mid (不是 mid-1)，mid 可能是答案
            if verbose:
                print(f" >= {target} → right={right}")
        else:
            left = mid + 1
            if verbose:
                print(f" < {target} → left={left}")

    if verbose:
        found = left < len(nums) and nums[left] == target
        print(f"  結束: left==right=={left}"
              f" → {'found' if found else 'not exact match'}")
    # left == right 就是第一個 >= target 的位置
    if left < len(nums) and nums[left] == target:
        return left
    return -1


# -----------------------------------------------------------------------------
# 2-3: Template 3 — while left + 1 < right (Never Overshoot)
# 用途: 最安全，結束後 left 和 right 相鄰，再手動判斷
# -----------------------------------------------------------------------------
def template3_safe(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    Template 3: while left + 1 < right
    特點: 結束時 left 和 right 相鄰，不可能死迴圈
    缺點: 迴圈結束後需要額外判斷 left 和 right
    """
    if len(nums) == 0:
        return -1
    left, right = 0, len(nums) - 1
    step = 0

    while left + 1 < right:  # 保證 left 和 right 之間至少有一個元素
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")
        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓ → right={mid} (找左界所以往左收)")
            right = mid  # 若找左界，往左收
        elif nums[mid] < target:
            left = mid  # 注意: left = mid (不是 mid+1)
            if verbose:
                print(f" < {target} → left={left}")
        else:
            right = mid  # 注意: right = mid (不是 mid-1)
            if verbose:
                print(f" > {target} → right={right}")

    # 迴圈結束後，left 和 right 相鄰，手動判斷
    if verbose:
        print(f"  結束: left={left}, right={right} (相鄰)")
        print(f"  檢查 nums[{left}]={nums[left]}, nums[{right}]={nums[right]}")
    if nums[left] == target:
        return left
    if nums[right] == target:
        return right
    return -1


def demo_three_templates():
    print("=" * 70)
    print("Section 2: 三種模板比較 (Three Templates Comparison)")
    print("=" * 70)

    # --- Template 1 範例 ---
    print("\n--- Template 1: while left <= right (精確查找) ---")

    nums = [1, 3, 5, 7, 9, 11, 13]
    t = 9
    print(f"\n  T1 範例 1: nums={nums}, target={t}")
    print(f"  預期: return 4")
    r = template1_standard(nums, t, verbose=True)
    print(f"  結果: {r}\n")

    t = 6
    print(f"  T1 範例 2: nums={nums}, target={t}")
    print(f"  預期: return -1 (不存在)")
    r = template1_standard(nums, t, verbose=True)
    print(f"  結果: {r}\n")

    nums_s = [2, 5]
    t = 5
    print(f"  T1 範例 3: nums={nums_s}, target={t}")
    print(f"  預期: return 1")
    r = template1_standard(nums_s, t, verbose=True)
    print(f"  結果: {r}\n")

    # --- Template 2 範例 ---
    print("--- Template 2: while left < right (找左邊界 / lower_bound) ---")

    nums2 = [1, 2, 2, 2, 3, 4]
    t = 2
    print(f"\n  T2 範例 1: nums={nums2}, target={t}")
    print(f"  預期: 第一個 2 在 index 1 → return 1")
    # Step 1: left=0, right=6, mid=3 → nums[3]=2 >= 2 → right=3
    # Step 2: left=0, right=3, mid=1 → nums[1]=2 >= 2 → right=1
    # Step 3: left=0, right=1, mid=0 → nums[0]=1 < 2 → left=1
    # 結束: left==right==1
    r = template2_left_bound(nums2, t, verbose=True)
    print(f"  結果: {r}\n")

    t = 5
    print(f"  T2 範例 2: nums={nums2}, target={t}")
    print(f"  預期: 5 不存在 → return -1")
    r = template2_left_bound(nums2, t, verbose=True)
    print(f"  結果: {r}\n")

    nums2b = [1, 1, 1, 1]
    t = 1
    print(f"  T2 範例 3: nums={nums2b}, target={t}")
    print(f"  預期: 第一個 1 在 index 0 → return 0")
    r = template2_left_bound(nums2b, t, verbose=True)
    print(f"  結果: {r}\n")

    # --- Template 3 範例 ---
    print("--- Template 3: while left + 1 < right (最安全，永不越界) ---")

    nums3 = [1, 3, 3, 3, 5, 7]
    t = 3
    print(f"\n  T3 範例 1: nums={nums3}, target={t}")
    print(f"  預期: 第一個 3 在 index 1 → return 1")
    r = template3_safe(nums3, t, verbose=True)
    print(f"  結果: {r}\n")

    t = 4
    print(f"  T3 範例 2: nums={nums3}, target={t}")
    print(f"  預期: 4 不存在 → return -1")
    r = template3_safe(nums3, t, verbose=True)
    print(f"  結果: {r}\n")

    nums3b = [10, 20]
    t = 10
    print(f"  T3 範例 3: nums={nums3b}, target={t}")
    print(f"  預期: return 0")
    r = template3_safe(nums3b, t, verbose=True)
    print(f"  結果: {r}\n")

    # --- 同一題目用三種模板解 ---
    print("--- 同一題目三種模板對照 (Side-by-Side) ---")
    compare_nums = [1, 2, 4, 4, 4, 6, 8]
    compare_t = 4
    print(f"  問題: nums={compare_nums}, 找 target={compare_t}")
    print(f"\n  [Template 1] 找到任一個 4:")
    r1 = template1_standard(compare_nums, compare_t, verbose=True)
    print(f"  結果: index {r1}")
    print(f"\n  [Template 2] 找第一個 4 (left bound):")
    r2 = template2_left_bound(compare_nums, compare_t, verbose=True)
    print(f"  結果: index {r2}")
    print(f"\n  [Template 3] 找第一個 4 (safe):")
    r3 = template3_safe(compare_nums, compare_t, verbose=True)
    print(f"  結果: index {r3}")
    print()


# =============================================================================
# Section 3: 旋轉數組 (Rotated Array)
# =============================================================================

# -----------------------------------------------------------------------------
# 3-1: Search in Rotated Sorted Array 旋轉排序陣列搜尋
# LeetCode 33 — 沒有重複元素
# 核心: 每次至少有一半是有序的，判斷 target 在有序那半邊嗎？
# -----------------------------------------------------------------------------
def search_rotated(nums: List[int], target: int, verbose: bool = False) -> int:
    """
    旋轉排序陣列搜尋 (無重複)
    關鍵: mid 把陣列分兩半，至少有一半是排序好的
    判斷 target 是否在排序好的那一半 → 決定往哪邊走
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓ → return {mid}")
            return mid

        # 判斷哪一半是有序的
        left_val, mid_val, right_val = nums[left], nums[mid], nums[right]
        if left_val <= mid_val:
            # 左半有序 [left..mid]
            if left_val <= target < mid_val:
                right = mid - 1
                if verbose:
                    print(f"  左半有序[{left_val}..{mid_val}], "
                          f"{target}在左半 → right={right}")
            else:
                left = mid + 1
                if verbose:
                    print(f"  左半有序[{left_val}..{mid_val}], "
                          f"{target}不在左半 → left={left}")
        else:
            # 右半有序 [mid..right]
            if mid_val < target <= right_val:
                left = mid + 1
                if verbose:
                    print(f"  右半有序[{mid_val}..{right_val}], "
                          f"{target}在右半 → left={left}")
            else:
                right = mid - 1
                if verbose:
                    print(f"  右半有序[{mid_val}..{right_val}], "
                          f"{target}不在右半 → right={right}")

    if verbose:
        print(f"  未找到 → return -1")
    return -1


def demo_search_rotated():
    print("=" * 70)
    print("3-1: Search in Rotated Sorted Array (LeetCode 33)")
    print("=" * 70)

    # 範例 1: target 在右半
    nums1 = [4, 5, 6, 7, 0, 1, 2]
    t1 = 0
    print(f"\n範例 1: nums={nums1}, target={t1}")
    print(f"  原始排序: [0,1,2,4,5,6,7]，在 index 4 旋轉")
    print(f"  預期: 0 在 index 4 → return 4")
    r = search_rotated(nums1, t1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2: target 在左半
    t2 = 5
    print(f"範例 2: nums={nums1}, target={t2}")
    print(f"  預期: 5 在 index 1 → return 1")
    r = search_rotated(nums1, t2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3: target 不存在
    t3 = 3
    print(f"範例 3: nums={nums1}, target={t3}")
    print(f"  預期: 3 不存在 → return -1")
    r = search_rotated(nums1, t3, verbose=True)
    print(f"  結果: {r}\n")


# -----------------------------------------------------------------------------
# 3-2: Find Minimum in Rotated Sorted Array 找旋轉陣列最小值
# LeetCode 153
# 核心: 最小值在「斷層」的右邊，用 nums[mid] vs nums[right] 判斷
# -----------------------------------------------------------------------------
def find_min_rotated(nums: List[int], verbose: bool = False) -> int:
    """
    找旋轉排序陣列的最小值 (無重複)
    用 Template 2: while left < right
    比較 nums[mid] 和 nums[right] 來判斷最小值在哪半邊
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left < right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] > nums[right]:
            # 最小值在 mid 右邊（斷層在右半）
            left = mid + 1
            if verbose:
                print(f" > nums[{right}]={nums[right]} → 最小值在右半 → left={left}")
        else:
            # 最小值在 mid 或 mid 左邊
            right = mid
            if verbose:
                print(f" <= nums[{right}]={nums[right]} → right={mid}")

    if verbose:
        print(f"  結束: left==right=={left} → nums[{left}]={nums[left]}")
    return nums[left]


def demo_find_min_rotated():
    print("=" * 70)
    print("3-2: Find Minimum in Rotated Sorted Array (LeetCode 153)")
    print("=" * 70)

    # 範例 1: 正常旋轉
    nums1 = [3, 4, 5, 1, 2]
    print(f"\n範例 1: nums={nums1}")
    print(f"  預期: 最小值 = 1")
    # Step 1: left=0, right=4, mid=2 → nums[2]=5 > nums[4]=2 → left=3
    # Step 2: left=3, right=4, mid=3 → nums[3]=1 <= nums[4]=2 → right=3
    # 結束: left==right==3 → nums[3]=1
    r = find_min_rotated(nums1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2: 沒旋轉（已排序）
    nums2 = [1, 2, 3, 4, 5]
    print(f"範例 2: nums={nums2}")
    print(f"  預期: 最小值 = 1（沒有旋轉）")
    r = find_min_rotated(nums2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3: 旋轉到幾乎回來
    nums3 = [2, 1]
    print(f"範例 3: nums={nums3}")
    print(f"  預期: 最小值 = 1")
    r = find_min_rotated(nums3, verbose=True)
    print(f"  結果: {r}\n")


# -----------------------------------------------------------------------------
# 3-3: Search in Rotated Sorted Array II (有重複)
# LeetCode 81
# 核心: 遇到 nums[left]==nums[mid]==nums[right] 時，無法判斷 → left++, right--
# -----------------------------------------------------------------------------
def search_rotated_ii(nums: List[int], target: int, verbose: bool = False) -> bool:
    """
    旋轉排序陣列搜尋 (有重複)
    與 33 題差別: 遇到 nums[left] == nums[mid] == nums[right]
    無法判斷哪半有序 → 兩邊各縮一步
    最差 O(n)，平均仍 O(log n)
    """
    left, right = 0, len(nums) - 1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ nums[{mid}]={nums[mid]}", end="")

        if nums[mid] == target:
            if verbose:
                print(f" == {target} ✓")
            return True

        # 關鍵: 無法判斷時，兩邊各縮一步
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
            if verbose:
                print(f"  三者相等，無法判斷 → left={left}, right={right}")
            continue

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
                if verbose:
                    print(f"  左半有序, target 在左 → right={right}")
            else:
                left = mid + 1
                if verbose:
                    print(f"  左半有序, target 不在左 → left={left}")
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
                if verbose:
                    print(f"  右半有序, target 在右 → left={left}")
            else:
                right = mid - 1
                if verbose:
                    print(f"  右半有序, target 不在右 → right={right}")

    if verbose:
        print(f"  未找到 → return False")
    return False


def demo_search_rotated_ii():
    print("=" * 70)
    print("3-3: Search in Rotated Sorted Array II (LeetCode 81)")
    print("=" * 70)

    # 範例 1: 有重複，找到
    nums1 = [2, 5, 6, 0, 0, 1, 2]
    t1 = 0
    print(f"\n範例 1: nums={nums1}, target={t1}")
    print(f"  預期: True")
    r = search_rotated_ii(nums1, t1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2: 有重複，找不到
    t2 = 3
    print(f"範例 2: nums={nums1}, target={t2}")
    print(f"  預期: False")
    r = search_rotated_ii(nums1, t2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3: 大量重複導致退化
    nums3 = [1, 1, 1, 1, 1, 1, 2, 1, 1]
    t3 = 2
    print(f"範例 3: nums={nums3}, target={t3}")
    print(f"  預期: True（大量重複，可能退化為 O(n)）")
    r = search_rotated_ii(nums3, t3, verbose=True)
    print(f"  結果: {r}\n")


# =============================================================================
# Section 4: 答案二分 (Binary Search on Answer)
# =============================================================================
# 核心思想: 不是在陣列上二分，而是在「答案的可能範圍」上二分
# 檢查某個候選答案是否可行 → 如果可行就嘗試更好的答案

# -----------------------------------------------------------------------------
# 4-1: Koko Eating Bananas 吃香蕉問題
# LeetCode 875
# 二分搜尋的是「吃的速度 k」
# -----------------------------------------------------------------------------
def min_eating_speed(piles: List[int], h: int, verbose: bool = False) -> int:
    """
    Koko 要在 h 小時內吃完所有香蕉。
    每小時吃一堆，速度 k 根/小時，不夠一堆就花一整個小時。
    求最小速度 k。

    答案範圍: k ∈ [1, max(piles)]
    對 k 做二分，用 can_finish(k) 判斷是否可行
    """
    def hours_needed(speed: int) -> int:
        """以 speed 根/小時的速度，吃完所有堆需要幾小時"""
        return sum(math.ceil(pile / speed) for pile in piles)

    left, right = 1, max(piles)
    step = 0

    while left < right:
        mid = left + (right - left) // 2
        needed = hours_needed(mid)
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid(speed)={mid} "
                  f"→ 需要 {needed} 小時", end="")

        if needed <= h:
            # 速度夠快，試試更慢的
            right = mid
            if verbose:
                print(f" <= {h} ✓ 可行 → right={right}")
        else:
            # 速度太慢
            left = mid + 1
            if verbose:
                print(f" > {h} ✗ 太慢 → left={left}")

    if verbose:
        print(f"  結束: 最小速度 = {left}")
    return left


def demo_koko():
    print("=" * 70)
    print("4-1: Koko Eating Bananas 吃香蕉 (LeetCode 875)")
    print("=" * 70)

    # 範例 1
    piles1 = [3, 6, 7, 11]
    h1 = 8
    print(f"\n範例 1: piles={piles1}, h={h1}")
    print(f"  預期: 速度 4 → ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4)=1+2+2+3=8 ✓")
    r = min_eating_speed(piles1, h1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2
    piles2 = [30, 11, 23, 4, 20]
    h2 = 5
    print(f"範例 2: piles={piles2}, h={h2}")
    print(f"  預期: 速度 30 (每堆最多1小時，剛好5堆5小時)")
    r = min_eating_speed(piles2, h2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3
    piles3 = [30, 11, 23, 4, 20]
    h3 = 6
    print(f"範例 3: piles={piles3}, h={h3}")
    print(f"  預期: 速度 23")
    r = min_eating_speed(piles3, h3, verbose=True)
    print(f"  結果: {r}\n")


# -----------------------------------------------------------------------------
# 4-2: Split Array Largest Sum 分割陣列的最大和
# LeetCode 410
# 二分搜尋的是「最大子陣列和」的上限
# -----------------------------------------------------------------------------
def split_array(nums: List[int], k: int, verbose: bool = False) -> int:
    """
    將 nums 分成 k 個非空子陣列，最小化「最大子陣列和」。

    答案範圍: [max(nums), sum(nums)]
    - 最小可能: 每個元素自成一組，最大和 = max(nums)
    - 最大可能: 全部放一組，最大和 = sum(nums)
    """
    def can_split(max_sum: int) -> bool:
        """以 max_sum 為上限，能否分成 <= k 組？"""
        count = 1
        current = 0
        for num in nums:
            if current + num > max_sum:
                count += 1
                current = num
            else:
                current += num
        return count <= k

    left, right = max(nums), sum(nums)
    step = 0

    while left < right:
        mid = left + (right - left) // 2
        step += 1
        feasible = can_split(mid)
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid(max_sum)={mid} "
                  f"→ can_split={feasible}", end="")

        if feasible:
            right = mid
            if verbose:
                print(f" ✓ 可行，試更小 → right={right}")
        else:
            left = mid + 1
            if verbose:
                print(f" ✗ 不行，放大 → left={left}")

    if verbose:
        print(f"  結束: 最小化的最大和 = {left}")
    return left


def demo_split_array():
    print("=" * 70)
    print("4-2: Split Array Largest Sum (LeetCode 410)")
    print("=" * 70)

    # 範例 1
    nums1 = [7, 2, 5, 10, 8]
    k1 = 2
    print(f"\n範例 1: nums={nums1}, k={k1}")
    print(f"  預期: 18 → [7,2,5] 和 [10,8]，最大和=max(14,18)=18")
    r = split_array(nums1, k1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2
    nums2 = [1, 2, 3, 4, 5]
    k2 = 3
    print(f"範例 2: nums={nums2}, k={k2}")
    print(f"  預期: 6 → [1,2,3] [4] [5]，最大和=6")
    r = split_array(nums2, k2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3
    nums3 = [1, 4, 4]
    k3 = 3
    print(f"範例 3: nums={nums3}, k={k3}")
    print(f"  預期: 4 → [1] [4] [4]，每個一組，最大和=4")
    r = split_array(nums3, k3, verbose=True)
    print(f"  結果: {r}\n")


# -----------------------------------------------------------------------------
# 4-3: Capacity To Ship Packages 船運載重
# LeetCode 1011
# 二分搜尋的是「船的載重量」
# -----------------------------------------------------------------------------
def ship_within_days(weights: List[int], days: int, verbose: bool = False) -> int:
    """
    在 days 天內運完所有包裹，求最小載重。
    每天按順序裝，裝不下就隔天。

    答案範圍: [max(weights), sum(weights)]
    """
    def days_needed(capacity: int) -> int:
        """以 capacity 為載重，需要幾天？"""
        d = 1
        current = 0
        for w in weights:
            if current + w > capacity:
                d += 1
                current = w
            else:
                current += w
        return d

    left, right = max(weights), sum(weights)
    step = 0

    while left < right:
        mid = left + (right - left) // 2
        needed = days_needed(mid)
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, "
                  f"mid(capacity)={mid} → 需要 {needed} 天", end="")

        if needed <= days:
            right = mid
            if verbose:
                print(f" <= {days} ✓ → right={right}")
        else:
            left = mid + 1
            if verbose:
                print(f" > {days} ✗ → left={left}")

    if verbose:
        print(f"  結束: 最小載重 = {left}")
    return left


def demo_ship_packages():
    print("=" * 70)
    print("4-3: Capacity To Ship Packages (LeetCode 1011)")
    print("=" * 70)

    # 範例 1
    w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d1 = 5
    print(f"\n範例 1: weights={w1}, days={d1}")
    print(f"  預期: 15 → [1,2,3,4,5][6,7][8][9][10]")
    r = ship_within_days(w1, d1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2
    w2 = [3, 2, 2, 4, 1, 4]
    d2 = 3
    print(f"範例 2: weights={w2}, days={d2}")
    print(f"  預期: 6 → [3,2][2,4][1,4]")
    r = ship_within_days(w2, d2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3
    w3 = [1, 2, 3, 1, 1]
    d3 = 4
    print(f"範例 3: weights={w3}, days={d3}")
    print(f"  預期: 3 → [1,2][3][1,1] (只需3天，4天更寬裕)")
    r = ship_within_days(w3, d3, verbose=True)
    print(f"  結果: {r}\n")


# =============================================================================
# Section 5: 矩陣二分 (Matrix Binary Search)
# =============================================================================

# -----------------------------------------------------------------------------
# 5-1: Search a 2D Matrix 搜尋二維矩陣
# LeetCode 74
# 核心: 把 2D 矩陣攤平成 1D，用 index 轉換 row = mid // cols, col = mid % cols
# -----------------------------------------------------------------------------
def search_matrix(matrix: List[List[int]], target: int,
                  verbose: bool = False) -> bool:
    """
    每行遞增，且下一行的第一個 > 上一行最後一個 → 整體有序
    視為一維陣列做二分: index → (row, col) = (i // cols, i % cols)
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    step = 0

    while left <= right:
        mid = left + (right - left) // 2
        r, c = mid // cols, mid % cols
        val = matrix[r][c]
        step += 1
        if verbose:
            print(f"  Step {step}: left={left}, right={right}, mid={mid} "
                  f"→ matrix[{r}][{c}]={val}", end="")

        if val == target:
            if verbose:
                print(f" == {target} ✓")
            return True
        elif val < target:
            left = mid + 1
            if verbose:
                print(f" < {target} → left={left}")
        else:
            right = mid - 1
            if verbose:
                print(f" > {target} → right={right}")

    if verbose:
        print(f"  未找到 → return False")
    return False


def demo_search_matrix():
    print("=" * 70)
    print("5-1: Search a 2D Matrix (LeetCode 74)")
    print("=" * 70)

    matrix1 = [
        [1,  3,  5,  7],
        [10, 11, 16, 20],
        [23, 30, 34, 60]
    ]

    # 範例 1: 找到
    t1 = 3
    print(f"\n範例 1: target={t1}")
    print(f"  矩陣: {matrix1}")
    print(f"  攤平: [1,3,5,7,10,11,16,20,23,30,34,60]，找 3")
    print(f"  預期: True")
    # mid=5 → matrix[1][1]=11 > 3 → right=4
    # mid=2 → matrix[0][2]=5 > 3 → right=1
    # mid=0 → matrix[0][0]=1 < 3 → left=1
    # mid=1 → matrix[0][1]=3 == 3 ✓
    r = search_matrix(matrix1, t1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2: 找不到
    t2 = 13
    print(f"範例 2: target={t2}")
    print(f"  預期: False")
    r = search_matrix(matrix1, t2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3: 邊界 — 最後一個元素
    t3 = 60
    print(f"範例 3: target={t3}")
    print(f"  預期: True (最後一個元素)")
    r = search_matrix(matrix1, t3, verbose=True)
    print(f"  結果: {r}\n")


# -----------------------------------------------------------------------------
# 5-2: Search a 2D Matrix II 搜尋二維矩陣 II
# LeetCode 240
# 每行遞增，每列遞增，但下一行的頭不一定 > 上一行的尾
# 方法: 從右上角開始 (Staircase / Z字形走法)
# O(m + n)
# -----------------------------------------------------------------------------
def search_matrix_ii(matrix: List[List[int]], target: int,
                     verbose: bool = False) -> bool:
    """
    從右上角出發 (row=0, col=cols-1):
    - 若 val == target → 找到
    - 若 val > target → col-- (往左，排除這一列)
    - 若 val < target → row++ (往下，排除這一行)
    O(m + n) 時間
    """
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1
    step = 0

    while row < rows and col >= 0:
        val = matrix[row][col]
        step += 1
        if verbose:
            print(f"  Step {step}: row={row}, col={col} → "
                  f"matrix[{row}][{col}]={val}", end="")

        if val == target:
            if verbose:
                print(f" == {target} ✓")
            return True
        elif val > target:
            col -= 1
            if verbose:
                print(f" > {target} → col={col} (往左)")
        else:
            row += 1
            if verbose:
                print(f" < {target} → row={row} (往下)")

    if verbose:
        print(f"  超出邊界 → return False")
    return False


def demo_search_matrix_ii():
    print("=" * 70)
    print("5-2: Search a 2D Matrix II (LeetCode 240) — Staircase 走法")
    print("=" * 70)

    matrix2 = [
        [1,  4,  7, 11, 15],
        [2,  5,  8, 12, 19],
        [3,  6,  9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]

    # 範例 1: 找到
    t1 = 5
    print(f"\n範例 1: target={t1}")
    print(f"  矩陣 5x5，從右上角 (0,4)=15 出發")
    print(f"  預期: True")
    # Step 1: (0,4)=15 > 5 → col=3
    # Step 2: (0,3)=11 > 5 → col=2
    # Step 3: (0,2)=7 > 5 → col=1
    # Step 4: (0,1)=4 < 5 → row=1
    # Step 5: (1,1)=5 == 5 ✓
    r = search_matrix_ii(matrix2, t1, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 2: 找不到
    t2 = 20
    print(f"範例 2: target={t2}")
    print(f"  預期: False")
    r = search_matrix_ii(matrix2, t2, verbose=True)
    print(f"  結果: {r}\n")

    # 範例 3: 左下角元素
    t3 = 18
    print(f"範例 3: target={t3}")
    print(f"  預期: True (左下角)")
    r = search_matrix_ii(matrix2, t3, verbose=True)
    print(f"  結果: {r}\n")


# =============================================================================
# Section 6: 三種模板完整比較 (Template Decision Tree)
# =============================================================================

def demo_template_decision_tree():
    print("=" * 70)
    print("Section 6: 三種模板完整比較 — 決策樹 & 常見陷阱")
    print("=" * 70)

    decision_tree = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │               Binary Search Template 決策樹                        │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  你要找什麼？                                                       │
    │  ├── 精確找某個值 (exact match)                                     │
    │  │   └→ Template 1: while left <= right                            │
    │  │      例: LeetCode 704, 33, 74                                   │
    │  │                                                                  │
    │  ├── 找第一個滿足條件的位置 (first true / lower bound)             │
    │  │   └→ Template 2: while left < right                             │
    │  │      例: LeetCode 35, 153, 875, 410, 1011                      │
    │  │                                                                  │
    │  └── 怕死迴圈 / 邊界搞不清                                        │
    │      └→ Template 3: while left + 1 < right                        │
    │         例: 任何題目都能用，最安全但多一步判斷                      │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    三種模板對照表                                    │
    ├──────────┬──────────────────┬──────────────┬───────────────────────┤
    │ 特性      │ Template 1       │ Template 2   │ Template 3            │
    ├──────────┼──────────────────┼──────────────┼───────────────────────┤
    │ 條件      │ left <= right    │ left < right │ left + 1 < right     │
    │ 初始right │ len-1            │ len (或 len-1)│ len-1               │
    │ 縮小左    │ left = mid + 1   │ left = mid+1 │ left = mid           │
    │ 縮小右    │ right = mid - 1  │ right = mid  │ right = mid          │
    │ 結束狀態  │ left > right     │ left == right│ left + 1 == right    │
    │ 後處理    │ 不需要           │ 檢查 left    │ 檢查 left 和 right   │
    │ 死迴圈風險│ 無               │ 低(注意right)│ 無                   │
    ├──────────┼──────────────────┼──────────────┼───────────────────────┤
    │ 適合場景  │ 精確查找         │ 找邊界/答案  │ 萬用但需後處理       │
    └──────────┴──────────────────┴──────────────┴───────────────────────┘
    """
    print(decision_tree)

    pitfalls = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     常見陷阱 Common Pitfalls                        │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  1. 死迴圈 (Infinite Loop)                                         │
    │     原因: left < right 搭配 left = mid (當 left==mid 時不前進)     │
    │     解法: 用 mid = left + (right - left + 1) // 2 取上界           │
    │           或改用 Template 3                                        │
    │                                                                     │
    │  2. Off-by-one 差一錯誤                                            │
    │     Template 1: right = len-1 (閉區間)                             │
    │     Template 2: right = len   (開區間) ← 容易搞混！               │
    │                                                                     │
    │  3. 整數溢位 (Integer Overflow, 主要在 C++/Java)                   │
    │     錯: mid = (left + right) / 2                                   │
    │     對: mid = left + (right - left) / 2                            │
    │                                                                     │
    │  4. 答案二分的邊界設錯                                             │
    │     記住: left = 最小可能答案, right = 最大可能答案                │
    │     例: 吃香蕉 → left=1, right=max(piles)                         │
    │                                                                     │
    │  5. 旋轉陣列忘記處理重複                                           │
    │     LeetCode 81: nums[left]==nums[mid]==nums[right] → 縮邊界      │
    └─────────────────────────────────────────────────────────────────────┘
    """
    print(pitfalls)

    # 用程式碼展示死迴圈 pitfall
    print("  --- 陷阱演示: Template 2 死迴圈風險 ---")
    print("  問題: nums=[1,2], target=2, 用 left<right 但 left=mid")
    print("  ❌ 錯誤寫法:")
    print("     left=0, right=1, mid=0 → nums[0]=1 < 2 → left=mid=0 (沒前進!)")
    print("     left=0, right=1, mid=0 → ... 永遠迴圈")
    print()
    print("  ✅ 正確寫法:")
    print("     使用 left = mid + 1 或 mid = left + (right-left+1)//2")
    print()


# =============================================================================
# 補充: 完整模式匹配速查表 (Quick Reference)
# =============================================================================

def print_cheat_sheet():
    print("=" * 70)
    print("Binary Search 速查表 (Cheat Sheet)")
    print("=" * 70)
    sheet = """
    ┌────────────────────────┬────────────────────────────────────────────┐
    │ 題型                    │ 關鍵思路                                  │
    ├────────────────────────┼────────────────────────────────────────────┤
    │ 精確查找               │ T1: left<=right, return mid               │
    │ 找左界 (first >=)      │ T2: left<right, right=mid                 │
    │ 找右界 (last <=)       │ T2: left<right, left=mid+1, return left-1 │
    │ 找插入位置             │ T1: 結束後 return left                    │
    │ 旋轉陣列查找           │ T1: 判斷哪半有序                          │
    │ 旋轉陣列找最小值       │ T2: 比較 mid 和 right                    │
    │ 答案二分 (最小化)      │ T2: can(mid)? right=mid : left=mid+1     │
    │ 答案二分 (最大化)      │ T2: can(mid)? left=mid : right=mid-1     │
    │ 2D 矩陣 (全序)        │ 攤平成 1D: row=mid//cols, col=mid%cols    │
    │ 2D 矩陣 (行列序)      │ 右上角出發，Z字形 O(m+n)                 │
    └────────────────────────┴────────────────────────────────────────────┘

    時間複雜度:
    - 標準二分: O(log n)
    - 答案二分: O(n * log(答案範圍)) — n 是驗證一次的成本
    - 2D Matrix: O(log(m*n)) 或 O(m+n)
    - 旋轉陣列(有重複): 最差 O(n)
    """
    print(sheet)


# =============================================================================
# Main — 執行所有範例
# =============================================================================
def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║  LeetCode 06 - Binary Search 二分搜尋完整攻略                     ║")
    print("║  Target: Google / NVIDIA Interview Prep                           ║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Section 1: 標準二分搜尋
    demo_binary_search()
    demo_search_insert()
    demo_search_range()

    # Section 2: 三種模板
    demo_three_templates()

    # Section 3: 旋轉數組
    demo_search_rotated()
    demo_find_min_rotated()
    demo_search_rotated_ii()

    # Section 4: 答案二分
    demo_koko()
    demo_split_array()
    demo_ship_packages()

    # Section 5: 矩陣二分
    demo_search_matrix()
    demo_search_matrix_ii()

    # Section 6: 模板決策樹 & 陷阱
    demo_template_decision_tree()

    # 速查表
    print_cheat_sheet()

    print("=" * 70)
    print("全部範例執行完畢！All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
