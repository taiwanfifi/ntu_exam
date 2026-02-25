#!/usr/bin/env python3
"""
=============================================================================
LeetCode 雙指針模式完全攻略 (Array + Two Pointers)
=============================================================================
目標讀者：準備 Google / NVIDIA 面試的初學者
教學風格：每題 3 個範例，每個範例都有完整的 step-by-step 數值追蹤
語言：繁體中文解說 + English technical terms

直接執行：python 01_Array_Two_Pointers.py
=============================================================================
"""
from typing import List


# ============================================================================
# Section 1: 對向雙指針 (Opposite Direction Two Pointers)
# ============================================================================
# 核心概念：兩個指針分別從陣列的「頭」和「尾」出發，向中間靠攏。
# 適用時機：
#   - 陣列已排序 (sorted)
#   - 需要找「一對」滿足條件的元素
#   - 需要比較兩端的值來做決策
# Time Complexity 通常為 O(n)，因為每個元素最多被訪問一次。
# ============================================================================


# ---------------------------------------------------------------------------
# 1-1. Two Sum II (LeetCode 167) - Input Array Is Sorted
# ---------------------------------------------------------------------------
# 題意：給定一個已排序的陣列 numbers 和一個目標值 target，
#       找出兩個數字使得它們的和等於 target。回傳 1-indexed 答案。
#
# 為什麼用對向雙指針？
#   - 陣列已排序 → 如果 sum 太大就縮右邊，太小就推左邊
#   - 保證恰好一組解 → 不需要處理多組解的情況
#
# 範例 1: numbers = [2, 7, 11, 15], target = 9
#
# 初始狀態: left=0, right=3
# Step 1: numbers[0]+numbers[3] = 2+15 = 17 > 9 → right-- → right=2
# Step 2: numbers[0]+numbers[2] = 2+11 = 13 > 9 → right-- → right=1
# Step 3: numbers[0]+numbers[1] = 2+7  = 9 == 9 ✓ → return [1, 2]
#
# 範例 2: numbers = [1, 3, 4, 5, 7, 10, 11], target = 9
#
# 初始狀態: left=0, right=6
# Step 1: numbers[0]+numbers[6] = 1+11 = 12 > 9 → right-- → right=5
# Step 2: numbers[0]+numbers[5] = 1+10 = 11 > 9 → right-- → right=4
# Step 3: numbers[0]+numbers[4] = 1+7  = 8  < 9 → left++  → left=1
# Step 4: numbers[1]+numbers[4] = 3+7  = 10 > 9 → right-- → right=3
# Step 5: numbers[1]+numbers[3] = 3+5  = 8  < 9 → left++  → left=2
# Step 6: numbers[2]+numbers[3] = 4+5  = 9 == 9 ✓ → return [3, 4]
#
# 範例 3: numbers = [2, 3, 4], target = 6
#
# 初始狀態: left=0, right=2
# Step 1: numbers[0]+numbers[2] = 2+4 = 6 == 6 ✓ → return [1, 3]
# （一步就找到！最佳情況。）

def two_sum_ii(numbers: List[int], target: int, verbose: bool = False) -> List[int]:
    """Two Sum II - sorted array，對向雙指針解法。"""
    left, right = 0, len(numbers) - 1
    step = 0

    if verbose:
        print(f"  初始狀態: left={left}, right={right}")

    while left < right:
        current_sum = numbers[left] + numbers[right]
        step += 1

        if verbose:
            op = "==" if current_sum == target else (">" if current_sum > target else "<")
            print(f"  Step {step}: numbers[{left}]+numbers[{right}] "
                  f"= {numbers[left]}+{numbers[right]} = {current_sum} {op} {target}", end="")

        if current_sum == target:
            if verbose:
                print(f" ✓ → return [{left+1}, {right+1}]")
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum > target:
            right -= 1
            if verbose:
                print(f" → right-- → right={right}")
        else:
            left += 1
            if verbose:
                print(f" → left++  → left={left}")

    return []  # 題目保證有解，不會到這裡


# ---------------------------------------------------------------------------
# 1-2. Container With Most Water (LeetCode 11)
# ---------------------------------------------------------------------------
# 題意：給定 n 條垂直線（高度陣列 height），找出兩條線與 x 軸圍成的
#       容器能裝最多水。面積 = min(height[l], height[r]) * (r - l)
#
# 為什麼 greedy 有效？
#   - 寬度一定在縮小（因為指針向內移動）
#   - 所以我們必須嘗試讓「高度」變大來補償寬度的減少
#   - 移動較矮的那一端，才有「機會」遇到更高的線 → 面積可能變大
#   - 移動較高的那一端 → min 值不會增加，寬度還變小 → 面積一定變小或不變
#
# 範例 1: height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
#
# 初始狀態: left=0, right=8, max_area=0
# Step 1: area = min(1,7)*(8-0) = 1*8 = 8   → max=8   → height[0]=1 < height[8]=7 → left++
# Step 2: area = min(8,7)*(8-1) = 7*7 = 49  → max=49  → height[1]=8 > height[8]=7 → right--
# Step 3: area = min(8,3)*(7-1) = 3*6 = 18  → max=49  → height[7]=3 < height[1]=8 → right--
# Step 4: area = min(8,8)*(6-1) = 8*5 = 40  → max=49  → height[1]=8==height[6]=8  → left++
# Step 5: area = min(6,8)*(6-2) = 6*4 = 24  → max=49  → height[2]=6 < height[6]=8 → left++
# Step 6: area = min(2,8)*(6-3) = 2*3 = 6   → max=49  → height[3]=2 < height[6]=8 → left++
# Step 7: area = min(5,8)*(6-4) = 5*2 = 10  → max=49  → height[4]=5 < height[6]=8 → left++
# Step 8: area = min(4,8)*(6-5) = 4*1 = 4   → max=49  → height[5]=4 < height[6]=8 → left++
# left=6 == right=6 → 結束，答案 = 49
#
# 範例 2: height = [1, 1]
#
# 初始狀態: left=0, right=1, max_area=0
# Step 1: area = min(1,1)*(1-0) = 1*1 = 1 → max=1 → 相等 → left++
# left=1 == right=1 → 結束，答案 = 1
#
# 範例 3: height = [4, 3, 2, 1, 4]
#
# 初始狀態: left=0, right=4, max_area=0
# Step 1: area = min(4,4)*(4-0) = 4*4 = 16 → max=16 → 相等 → left++
# Step 2: area = min(3,4)*(4-1) = 3*3 = 9  → max=16 → height[1]=3 < height[4]=4 → left++
# Step 3: area = min(2,4)*(4-2) = 2*2 = 4  → max=16 → height[2]=2 < height[4]=4 → left++
# Step 4: area = min(1,4)*(4-3) = 1*1 = 1  → max=16 → height[3]=1 < height[4]=4 → left++
# left=4 == right=4 → 結束，答案 = 16

def container_with_most_water(height: List[int], verbose: bool = False) -> int:
    """Container With Most Water，對向雙指針 + greedy。"""
    left, right = 0, len(height) - 1
    max_area = 0
    step = 0

    if verbose:
        print(f"  初始狀態: left={left}, right={right}, max_area={max_area}")

    while left < right:
        h = min(height[left], height[right])
        w = right - left
        area = h * w
        max_area = max(max_area, area)
        step += 1

        if verbose:
            print(f"  Step {step}: area = min({height[left]},{height[right]})"
                  f"*({right}-{left}) = {h}*{w} = {area} → max={max_area}", end="")

        if height[left] < height[right]:
            if verbose:
                print(f" → height[{left}]={height[left]} < height[{right}]={height[right]} → left++")
            left += 1
        else:
            if verbose:
                if height[left] == height[right]:
                    print(f" → 相等 → left++")
                else:
                    print(f" → height[{left}]={height[left]} > height[{right}]={height[right]} → right--")
            if height[left] > height[right]:
                right -= 1
            else:
                left += 1

    if verbose:
        print(f"  left={left} == right={right} → 結束，答案 = {max_area}")
    return max_area


# ---------------------------------------------------------------------------
# 1-3. Valid Palindrome (LeetCode 125)
# ---------------------------------------------------------------------------
# 題意：判斷字串是否為 palindrome（回文），只考慮字母和數字，忽略大小寫。
#
# 為什麼用對向雙指針？
#   - 回文的定義就是「頭尾對稱」
#   - 從兩端向中間比較，一旦不同就 return False
#
# 範例 1: s = "A man, a plan, a canal: Panama"
#   清理後: "amanaplanacanalpanama"  (長度 21)
#   left=0('a'), right=20('a') → 相同 → left++, right--
#   left=1('m'), right=19('m') → 相同 → ...
#   全部匹配 → return True
#
# 範例 2: s = "race a car"
#   清理後: "raceacar"  (長度 8)
#   left=0('r'), right=7('r') → match
#   left=1('a'), right=6('a') → match
#   left=2('c'), right=5('c') → match
#   left=3('e'), right=4('a') → 'e' != 'a' → return False
#
# 範例 3: s = "0P"
#   清理後: "0p"  (長度 2)
#   left=0('0'), right=1('p') → '0' != 'p' → return False

def valid_palindrome(s: str, verbose: bool = False) -> bool:
    """Valid Palindrome，對向雙指針（直接在原字串上跳過非字母數字）。"""
    left, right = 0, len(s) - 1
    step = 0

    if verbose:
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        print(f"  清理後: \"{cleaned}\" (長度 {len(cleaned)})")

    while left < right:
        # 跳過非字母數字
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if left >= right:
            break

        step += 1
        cl, cr = s[left].lower(), s[right].lower()

        if verbose:
            match_str = "match" if cl == cr else f"'{cl}' != '{cr}'"
            print(f"  Step {step}: left={left}('{cl}'), right={right}('{cr}') → {match_str}")

        if cl != cr:
            if verbose:
                print(f"  → return False")
            return False

        left += 1
        right -= 1

    if verbose:
        print(f"  全部匹配 → return True")
    return True


# ---------------------------------------------------------------------------
# 1-4. 3Sum (LeetCode 15)
# ---------------------------------------------------------------------------
# 題意：找出陣列中所有三元組 [a, b, c] 使得 a + b + c = 0，不可重複。
#
# 核心策略：排序 + 固定一個數 + Two Sum II（對向雙指針找另外兩個）
# 去重技巧：
#   1. 外層迴圈：如果 nums[i] == nums[i-1]，跳過（避免固定相同的數）
#   2. 內層迴圈：找到一組解後，left 和 right 都要跳過重複值
#
# 範例 1: nums = [-1, 0, 1, 2, -1, -4]
#   排序後: [-4, -1, -1, 0, 1, 2]
#
#   i=0, nums[i]=-4, target=4, left=1, right=5
#     Step 1: -1+2 = 1 < 4 → left++ → left=2
#     Step 2: -1+2 = 1 < 4 → left++ → left=3
#     Step 3:  0+2 = 2 < 4 → left++ → left=4
#     Step 4:  1+2 = 3 < 4 → left++ → left=5, left>=right → 結束
#
#   i=1, nums[i]=-1, target=1, left=2, right=5
#     Step 1: -1+2 = 1 == 1 ✓ → 找到 [-1, -1, 2]
#       → left 跳過重複: left=3, right 跳過重複: right=4
#     Step 2:  0+1 = 1 == 1 ✓ → 找到 [-1, 0, 1]
#       → left=4, right=3, left>=right → 結束
#
#   i=2, nums[i]=-1, 與 nums[1]相同 → 跳過
#   i=3, nums[i]=0, target=0, left=4, right=5
#     Step 1: 1+2 = 3 > 0 → right-- → right=4, left>=right → 結束
#
#   結果: [[-1, -1, 2], [-1, 0, 1]]
#
# 範例 2: nums = [0, 0, 0, 0]
#   排序後: [0, 0, 0, 0]
#
#   i=0, nums[i]=0, target=0, left=1, right=3
#     Step 1: 0+0 = 0 == 0 ✓ → 找到 [0, 0, 0]
#       → left 跳過重複: left=3, right 跳過重複: right=1 → 結束
#   i=1, nums[i]=0, 與 nums[0]相同 → 跳過
#   i=2, 同上 → 跳過
#
#   結果: [[0, 0, 0]]
#
# 範例 3: nums = [-2, 0, 1, 1, 2]
#   排序後: [-2, 0, 1, 1, 2]
#
#   i=0, nums[i]=-2, target=2, left=1, right=4
#     Step 1: 0+2 = 2 == 2 ✓ → 找到 [-2, 0, 2]
#       → left=2, right=3
#     Step 2: 1+1 = 2 == 2 ✓ → 找到 [-2, 1, 1]
#       → left=4, right=2 → 結束
#   i=1, nums[i]=0, target=0, left=2, right=4
#     Step 1: 1+2 = 3 > 0 → right-- → right=3
#     Step 2: 1+1 = 2 > 0 → right-- → right=2, left>=right → 結束
#
#   結果: [[-2, 0, 2], [-2, 1, 1]]

def three_sum(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """3Sum，排序 + 固定一數 + 對向雙指針。"""
    nums.sort()
    result = []

    if verbose:
        print(f"  排序後: {nums}")

    for i in range(len(nums) - 2):
        # 剪枝：最小值已 > 0，不可能三數和為 0
        if nums[i] > 0:
            break
        # 去重：跳過相同的 nums[i]
        if i > 0 and nums[i] == nums[i - 1]:
            if verbose:
                print(f"\n  i={i}, nums[i]={nums[i]}, 與 nums[{i-1}]相同 → 跳過")
            continue

        target = -nums[i]
        left, right = i + 1, len(nums) - 1
        step = 0

        if verbose:
            print(f"\n  i={i}, nums[i]={nums[i]}, target={target}, left={left}, right={right}")

        while left < right:
            current_sum = nums[left] + nums[right]
            step += 1

            if current_sum == target:
                triplet = [nums[i], nums[left], nums[right]]
                result.append(triplet)
                if verbose:
                    print(f"    Step {step}: {nums[left]}+{nums[right]} = {current_sum} "
                          f"== {target} ✓ → 找到 {triplet}")
                # 跳過重複
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
                if verbose:
                    print(f"      → 跳過重複後: left={left}, right={right}")
            elif current_sum < target:
                if verbose:
                    print(f"    Step {step}: {nums[left]}+{nums[right]} = {current_sum} "
                          f"< {target} → left++")
                left += 1
            else:
                if verbose:
                    print(f"    Step {step}: {nums[left]}+{nums[right]} = {current_sum} "
                          f"> {target} → right--")
                right -= 1

    if verbose:
        print(f"\n  結果: {result}")
    return result


# ============================================================================
# Section 2: 同向雙指針 (Same Direction Two Pointers)
# ============================================================================
# 核心概念：兩個指針都從陣列的「左端」出發，向同一個方向移動。
# 常見角色：
#   - slow pointer（慢指針）：指向「結果陣列」的寫入位置
#   - fast pointer（快指針）：掃描原陣列的每個元素
# 適用時機：
#   - In-place 修改陣列（移除 / 去重 / 分區）
#   - 需要維護一個「已處理區域」和「待處理區域」
# ============================================================================


# ---------------------------------------------------------------------------
# 2-1. Remove Duplicates from Sorted Array (LeetCode 26)
# ---------------------------------------------------------------------------
# 題意：在已排序陣列中原地 (in-place) 移除重複元素，回傳新長度。
#
# 策略：slow 指向「下一個要寫入的位置」，fast 掃描整個陣列。
#       當 nums[fast] != nums[slow-1] 時，寫入並推進 slow。
#
# 範例 1: nums = [1, 1, 2]
#
#   初始: slow=1, fast=1
#   fast=1: nums[1]=1 == nums[0]=1 → 跳過
#   fast=2: nums[2]=2 != nums[0]=1 → nums[1]=2, slow=2
#   結果: 長度=2, nums[:2]=[1, 2]
#
# 範例 2: nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
#
#   初始: slow=1, fast=1
#   fast=1: nums[1]=0 == nums[0]=0 → 跳過
#   fast=2: nums[2]=1 != nums[0]=0 → nums[1]=1, slow=2
#   fast=3: nums[3]=1 == nums[1]=1 → 跳過
#   fast=4: nums[4]=1 == nums[1]=1 → 跳過
#   fast=5: nums[5]=2 != nums[1]=1 → nums[2]=2, slow=3
#   fast=6: nums[6]=2 == nums[2]=2 → 跳過
#   fast=7: nums[7]=3 != nums[2]=2 → nums[3]=3, slow=4
#   fast=8: nums[8]=3 == nums[3]=3 → 跳過
#   fast=9: nums[9]=4 != nums[3]=3 → nums[4]=4, slow=5
#   結果: 長度=5, nums[:5]=[0, 1, 2, 3, 4]
#
# 範例 3: nums = [1, 2, 3]  (無重複)
#
#   初始: slow=1, fast=1
#   fast=1: nums[1]=2 != nums[0]=1 → nums[1]=2, slow=2
#   fast=2: nums[2]=3 != nums[1]=2 → nums[2]=3, slow=3
#   結果: 長度=3, nums[:3]=[1, 2, 3] (不變)

def remove_duplicates(nums: List[int], verbose: bool = False) -> int:
    """Remove Duplicates from Sorted Array，同向雙指針。"""
    if not nums:
        return 0

    slow = 1  # 下一個要寫入的位置

    if verbose:
        print(f"  初始: slow={slow}, 陣列={nums}")

    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow - 1]:
            if verbose:
                print(f"  fast={fast}: nums[{fast}]={nums[fast]} != "
                      f"nums[{slow-1}]={nums[slow-1]} → nums[{slow}]={nums[fast]}, slow={slow+1}")
            nums[slow] = nums[fast]
            slow += 1
        else:
            if verbose:
                print(f"  fast={fast}: nums[{fast}]={nums[fast]} == "
                      f"nums[{slow-1}]={nums[slow-1]} → 跳過")

    if verbose:
        print(f"  結果: 長度={slow}, nums[:{slow}]={nums[:slow]}")
    return slow


# ---------------------------------------------------------------------------
# 2-2. Move Zeroes (LeetCode 283)
# ---------------------------------------------------------------------------
# 題意：將所有 0 移到陣列末尾，同時保持非零元素的相對順序。必須 in-place。
#
# 策略：slow 指向「下一個非零值該放的位置」，fast 掃描全部。
#       遇到非零就 swap(nums[slow], nums[fast])，然後 slow++。
#
# 範例 1: nums = [0, 1, 0, 3, 12]
#
#   初始: slow=0
#   fast=0: nums[0]=0 → 是零 → 跳過
#   fast=1: nums[1]=1 → 非零 → swap(nums[0], nums[1]) → [1, 0, 0, 3, 12], slow=1
#   fast=2: nums[2]=0 → 是零 → 跳過
#   fast=3: nums[3]=3 → 非零 → swap(nums[1], nums[3]) → [1, 3, 0, 0, 12], slow=2
#   fast=4: nums[4]=12→ 非零 → swap(nums[2], nums[4]) → [1, 3, 12, 0, 0], slow=3
#   結果: [1, 3, 12, 0, 0]
#
# 範例 2: nums = [0, 0, 1]
#
#   初始: slow=0
#   fast=0: nums[0]=0 → 跳過
#   fast=1: nums[1]=0 → 跳過
#   fast=2: nums[2]=1 → swap(nums[0], nums[2]) → [1, 0, 0], slow=1
#   結果: [1, 0, 0]
#
# 範例 3: nums = [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
#
#   初始: slow=0
#   fast=0: 4 → 非零 → swap(nums[0],nums[0]) → 不變, slow=1
#   fast=1: 2 → 非零 → swap(nums[1],nums[1]) → 不變, slow=2
#   fast=2: 4 → 非零 → swap(nums[2],nums[2]) → 不變, slow=3
#   fast=3: 0 → 跳過
#   fast=4: 0 → 跳過
#   fast=5: 3 → 非零 → swap(nums[3],nums[5]) → [4,2,4,3,0,0,0,5,1,0], slow=4
#   fast=6: 0 → 跳過
#   fast=7: 5 → 非零 → swap(nums[4],nums[7]) → [4,2,4,3,5,0,0,0,1,0], slow=5
#   fast=8: 1 → 非零 → swap(nums[5],nums[8]) → [4,2,4,3,5,1,0,0,0,0], slow=6
#   fast=9: 0 → 跳過
#   結果: [4, 2, 4, 3, 5, 1, 0, 0, 0, 0]

def move_zeroes(nums: List[int], verbose: bool = False) -> None:
    """Move Zeroes，同向雙指針 swap 法。"""
    slow = 0

    if verbose:
        print(f"  初始: slow={slow}, 陣列={nums}")

    for fast in range(len(nums)):
        if nums[fast] != 0:
            if verbose:
                if slow == fast:
                    print(f"  fast={fast}: {nums[fast]} → 非零 → "
                          f"swap(nums[{slow}],nums[{fast}]) → 不變, slow={slow+1}")
                else:
                    print(f"  fast={fast}: {nums[fast]} → 非零 → "
                          f"swap(nums[{slow}],nums[{fast}])", end="")
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
            if verbose and slow - 1 != fast:
                print(f" → {nums}, slow={slow}")
        else:
            if verbose:
                print(f"  fast={fast}: {nums[fast]} → 是零 → 跳過")

    if verbose:
        print(f"  結果: {nums}")


# ---------------------------------------------------------------------------
# 2-3. Remove Element (LeetCode 27)
# ---------------------------------------------------------------------------
# 題意：原地移除陣列中所有等於 val 的元素，回傳新長度。不需要保持順序。
#
# 策略（保持順序版）：slow 指向寫入位，fast 掃描，遇到 != val 就寫入。
#
# 範例 1: nums = [3, 2, 2, 3], val = 3
#
#   初始: slow=0
#   fast=0: nums[0]=3 == val → 跳過
#   fast=1: nums[1]=2 != val → nums[0]=2, slow=1
#   fast=2: nums[2]=2 != val → nums[1]=2, slow=2
#   fast=3: nums[3]=3 == val → 跳過
#   結果: 長度=2, nums[:2]=[2, 2]
#
# 範例 2: nums = [0, 1, 2, 2, 3, 0, 4, 2], val = 2
#
#   初始: slow=0
#   fast=0: 0 != 2 → nums[0]=0, slow=1
#   fast=1: 1 != 2 → nums[1]=1, slow=2
#   fast=2: 2 == 2 → 跳過
#   fast=3: 2 == 2 → 跳過
#   fast=4: 3 != 2 → nums[2]=3, slow=3
#   fast=5: 0 != 2 → nums[3]=0, slow=4
#   fast=6: 4 != 2 → nums[4]=4, slow=5
#   fast=7: 2 == 2 → 跳過
#   結果: 長度=5, nums[:5]=[0, 1, 3, 0, 4]
#
# 範例 3: nums = [1], val = 1
#
#   初始: slow=0
#   fast=0: 1 == 1 → 跳過
#   結果: 長度=0, nums[:0]=[]

def remove_element(nums: List[int], val: int, verbose: bool = False) -> int:
    """Remove Element，同向雙指針。"""
    slow = 0

    if verbose:
        print(f"  初始: slow={slow}, val={val}, 陣列={nums}")

    for fast in range(len(nums)):
        if nums[fast] != val:
            if verbose:
                print(f"  fast={fast}: {nums[fast]} != {val} → nums[{slow}]={nums[fast]}, slow={slow+1}")
            nums[slow] = nums[fast]
            slow += 1
        else:
            if verbose:
                print(f"  fast={fast}: {nums[fast]} == {val} → 跳過")

    if verbose:
        print(f"  結果: 長度={slow}, nums[:{slow}]={nums[:slow]}")
    return slow


# ============================================================================
# Section 3: 快慢指針 (Fast-Slow Pointers / Floyd's Cycle Detection)
# ============================================================================
# 核心概念：
#   - slow 每次走 1 步，fast 每次走 2 步
#   - 如果存在 cycle，fast 一定會追上 slow（就像操場跑步）
#   - 追上後（Phase 1 結束），把其中一個指針放回起點，
#     兩個都改成每次走 1 步，再次相遇的地方就是 cycle 入口（Phase 2）
#
# 數學原理（為什麼 Phase 2 有效）：
#   設起點到 cycle 入口距離 = a，入口到相遇點 = b，相遇點繞回入口 = c
#   Phase 1 結束時：
#     slow 走了 a + b 步
#     fast 走了 a + b + (b + c) = a + 2b + c 步
#     因為 fast = 2 * slow → a + 2b + c = 2(a + b) → c = a
#   所以 Phase 2 兩個指針各走 a 步就會在入口相遇！
# ============================================================================


# ---------------------------------------------------------------------------
# 3-1. Find the Duplicate Number (LeetCode 287)
# ---------------------------------------------------------------------------
# 題意：陣列有 n+1 個整數，範圍 [1, n]，恰好有一個重複數字，找出它。
#       限制：不能修改陣列、O(1) 額外空間。
#
# 關鍵洞察：把 nums[i] 視為「指向 index nums[i]」的指針
#   → 形成一個 linked list，重複的數字就是 cycle 的入口
#
# 範例 1: nums = [1, 3, 4, 2, 2]
#   index:  0  1  2  3  4
#   value:  1  3  4  2  2
#
#   把它視為 linked list:
#   0 → nums[0]=1 → nums[1]=3 → nums[3]=2 → nums[2]=4 → nums[4]=2 → nums[2]=4 ...
#   也就是: 0 → 1 → 3 → 2 → 4 → 2 → 4 → 2 → ...  (cycle 在 2 和 4 之間)
#
#   Phase 1 (找相遇點):
#     初始: slow=0, fast=0
#     Step 1: slow=nums[0]=1, fast=nums[nums[0]]=nums[1]=3
#     Step 2: slow=nums[1]=3, fast=nums[nums[3]]=nums[2]=4
#     Step 3: slow=nums[3]=2, fast=nums[nums[4]]=nums[2]=4
#     Step 4: slow=nums[2]=4, fast=nums[nums[4]]=nums[2]=4
#     slow==fast==4 → 相遇！
#
#   Phase 2 (找入口):
#     slow=4, slow2=0
#     Step 1: slow=nums[4]=2, slow2=nums[0]=1
#     Step 2: slow=nums[2]=4, slow2=nums[1]=3
#     Step 3: slow=nums[4]=2, slow2=nums[3]=2
#     slow==slow2==2 → 重複數字是 2 ✓
#
# 範例 2: nums = [3, 1, 3, 4, 2]
#   index:  0  1  2  3  4
#   value:  3  1  3  4  2
#
#   Linked list: 0→3→4→2→3→4→2→...  (cycle: 3→4→2→3)
#
#   Phase 1:
#     初始: slow=0, fast=0
#     Step 1: slow=nums[0]=3, fast=nums[nums[0]]=nums[3]=4
#     Step 2: slow=nums[3]=4, fast=nums[nums[4]]=nums[2]=3
#     Step 3: slow=nums[4]=2, fast=nums[nums[3]]=nums[4]=2
#     slow==fast==2 → 相遇！
#
#   Phase 2:
#     slow=2, slow2=0
#     Step 1: slow=nums[2]=3, slow2=nums[0]=3
#     slow==slow2==3 → 重複數字是 3 ✓
#
# 範例 3: nums = [2, 5, 9, 6, 9, 3, 8, 9, 7, 1]
#   n=9, 重複數字是 9
#   index:  0  1  2  3  4  5  6  7  8  9
#   value:  2  5  9  6  9  3  8  9  7  1
#
#   Linked list: 0→2→9→1→5→3→6→8→7→9→1→5→...
#   cycle 入口在 9 之後回到 1 再到 ... 到 9，入口就是 9
#
#   Phase 1:
#     初始: slow=0, fast=0
#     Step 1: slow=nums[0]=2,  fast=nums[nums[0]]=nums[2]=9
#     Step 2: slow=nums[2]=9,  fast=nums[nums[9]]=nums[1]=5
#     Step 3: slow=nums[9]=1,  fast=nums[nums[5]]=nums[3]=6
#     Step 4: slow=nums[1]=5,  fast=nums[nums[6]]=nums[8]=7
#     Step 5: slow=nums[5]=3,  fast=nums[nums[7]]=nums[9]=1
#     Step 6: slow=nums[3]=6,  fast=nums[nums[1]]=nums[5]=3
#     Step 7: slow=nums[6]=8,  fast=nums[nums[3]]=nums[6]=8
#     slow==fast==8 → 相遇！
#
#   Phase 2:
#     slow=8, slow2=0
#     Step 1: slow=nums[8]=7, slow2=nums[0]=2
#     Step 2: slow=nums[7]=9, slow2=nums[2]=9
#     slow==slow2==9 → 重複數字是 9 ✓

def find_duplicate(nums: List[int], verbose: bool = False) -> int:
    """Find the Duplicate Number，Floyd's cycle detection。"""
    # Phase 1: 快慢指針找相遇點
    slow = fast = 0
    step = 0

    if verbose:
        print(f"  陣列: {nums}")
        print(f"  Phase 1 (找相遇點):")
        print(f"    初始: slow=0, fast=0")

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        step += 1

        if verbose:
            print(f"    Step {step}: slow={slow}, fast={fast}")

        if slow == fast:
            if verbose:
                print(f"    slow==fast=={slow} → 相遇！")
            break

    # Phase 2: 找 cycle 入口
    slow2 = 0
    step = 0

    if verbose:
        print(f"  Phase 2 (找入口):")
        print(f"    slow={slow}, slow2=0")

    while slow != slow2:
        slow = nums[slow]
        slow2 = nums[slow2]
        step += 1

        if verbose:
            print(f"    Step {step}: slow={slow}, slow2={slow2}")

    if verbose:
        print(f"    slow==slow2=={slow} → 重複數字是 {slow} ✓")

    return slow


# ============================================================================
# Section 4: 對向 vs 同向 vs 快慢 — 完整比較與決策框架
# ============================================================================
#
# ┌─────────────┬──────────────────┬──────────────────┬──────────────────────┐
# │   類型       │ 對向雙指針        │ 同向雙指針        │ 快慢指針              │
# │             │ (Opposite Dir.)  │ (Same Dir.)      │ (Fast-Slow)          │
# ├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
# │ 指針起點     │ 一頭一尾          │ 都從頭開始        │ 都從頭開始            │
# │ 移動方向     │ 向中間靠攏        │ 同方向前進        │ 同方向，速度不同       │
# │ 終止條件     │ left >= right    │ fast 到底         │ 兩指針相遇            │
# │ 時間複雜度   │ O(n)             │ O(n)             │ O(n)                 │
# │ 空間複雜度   │ O(1)             │ O(1)             │ O(1)                 │
# ├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
# │ 前提條件     │ 通常需要排序       │ 不一定要排序       │ 需要有 cycle 結構     │
# │ 典型題型     │ Two Sum (sorted) │ 去重/移除/分區     │ 環偵測/找重複          │
# │             │ Container Water  │ Move Zeroes      │ Linked List Cycle    │
# │             │ 3Sum / 4Sum      │ Remove Element   │ Find Duplicate       │
# │             │ Valid Palindrome │ Remove Duplicates│ Happy Number         │
# ├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
# │ 決策關鍵問題 │ 「兩端的資訊能否  │ 「需要 in-place   │ 「問題能否轉化為       │
# │             │  幫助我做決策？」  │  篩選/重排嗎？」  │  環偵測？」           │
# └─────────────┴──────────────────┴──────────────────┴──────────────────────┘
#
# 決策流程 (Decision Framework):
#
#   1. 陣列已排序 + 找一對/多對滿足條件的元素？
#      → 對向雙指針 (Two Sum II, 3Sum, Container Water)
#
#   2. 需要 in-place 去重/移除/把某類元素挪到一邊？
#      → 同向雙指針 (Remove Duplicates, Move Zeroes, Remove Element)
#
#   3. 問題可以轉化成「在某個 sequence 中偵測環」？
#      → 快慢指針 (Find Duplicate, Linked List Cycle, Happy Number)
#
#   4. 題目有「回文」性質（頭尾對稱）？
#      → 對向雙指針 (Valid Palindrome)
#
# 面試小提醒：
#   - 先問面試官 input 是否排序 → 排序的話，優先想對向雙指針
#   - 如果要求 O(1) space + in-place → 想同向雙指針
#   - 如果限制不能修改原陣列且 O(1) space → 想快慢指針
#   - 3Sum / 4Sum 本質上是「排序 + 固定 k-2 個 + Two Sum II」


def print_section_header(title: str) -> None:
    """列印段落標題。"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_problem_header(title: str) -> None:
    """列印題目標題。"""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ============================================================================
# Main: 執行所有範例並印出 step-by-step traces
# ============================================================================
def main():
    # ==================================================================
    # Section 1: 對向雙指針
    # ==================================================================
    print_section_header("Section 1: 對向雙指針 (Opposite Direction Two Pointers)")

    # --- Two Sum II ---
    print_problem_header("1-1. Two Sum II (LeetCode 167)")

    print("\n▸ 範例 1: numbers=[2,7,11,15], target=9")
    result = two_sum_ii([2, 7, 11, 15], 9, verbose=True)
    assert result == [1, 2], f"Expected [1,2], got {result}"

    print("\n▸ 範例 2: numbers=[1,3,4,5,7,10,11], target=9")
    result = two_sum_ii([1, 3, 4, 5, 7, 10, 11], 9, verbose=True)
    assert result == [3, 4], f"Expected [3,4], got {result}"

    print("\n▸ 範例 3: numbers=[2,3,4], target=6")
    result = two_sum_ii([2, 3, 4], 6, verbose=True)
    assert result == [1, 3], f"Expected [1,3], got {result}"

    # --- Container With Most Water ---
    print_problem_header("1-2. Container With Most Water (LeetCode 11)")

    print("\n▸ 範例 1: height=[1,8,6,2,5,4,8,3,7]")
    result = container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7], verbose=True)
    assert result == 49, f"Expected 49, got {result}"

    print("\n▸ 範例 2: height=[1,1]")
    result = container_with_most_water([1, 1], verbose=True)
    assert result == 1, f"Expected 1, got {result}"

    print("\n▸ 範例 3: height=[4,3,2,1,4]")
    result = container_with_most_water([4, 3, 2, 1, 4], verbose=True)
    assert result == 16, f"Expected 16, got {result}"

    # --- Valid Palindrome ---
    print_problem_header("1-3. Valid Palindrome (LeetCode 125)")

    print("\n▸ 範例 1: s='A man, a plan, a canal: Panama'")
    result = valid_palindrome("A man, a plan, a canal: Panama", verbose=True)
    assert result is True, f"Expected True, got {result}"

    print("\n▸ 範例 2: s='race a car'")
    result = valid_palindrome("race a car", verbose=True)
    assert result is False, f"Expected False, got {result}"

    print("\n▸ 範例 3: s='0P'")
    result = valid_palindrome("0P", verbose=True)
    assert result is False, f"Expected False, got {result}"

    # --- 3Sum ---
    print_problem_header("1-4. 3Sum (LeetCode 15)")

    print("\n▸ 範例 1: nums=[-1,0,1,2,-1,-4]")
    result = three_sum([-1, 0, 1, 2, -1, -4], verbose=True)
    assert result == [[-1, -1, 2], [-1, 0, 1]], f"Unexpected: {result}"

    print("\n▸ 範例 2: nums=[0,0,0,0]")
    result = three_sum([0, 0, 0, 0], verbose=True)
    assert result == [[0, 0, 0]], f"Unexpected: {result}"

    print("\n▸ 範例 3: nums=[-2,0,1,1,2]")
    result = three_sum([-2, 0, 1, 1, 2], verbose=True)
    assert result == [[-2, 0, 2], [-2, 1, 1]], f"Unexpected: {result}"

    # ==================================================================
    # Section 2: 同向雙指針
    # ==================================================================
    print_section_header("Section 2: 同向雙指針 (Same Direction Two Pointers)")

    # --- Remove Duplicates ---
    print_problem_header("2-1. Remove Duplicates from Sorted Array (LeetCode 26)")

    print("\n▸ 範例 1: nums=[1,1,2]")
    nums = [1, 1, 2]
    k = remove_duplicates(nums, verbose=True)
    assert k == 2 and nums[:k] == [1, 2]

    print("\n▸ 範例 2: nums=[0,0,1,1,1,2,2,3,3,4]")
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates(nums, verbose=True)
    assert k == 5 and nums[:k] == [0, 1, 2, 3, 4]

    print("\n▸ 範例 3: nums=[1,2,3]")
    nums = [1, 2, 3]
    k = remove_duplicates(nums, verbose=True)
    assert k == 3 and nums[:k] == [1, 2, 3]

    # --- Move Zeroes ---
    print_problem_header("2-2. Move Zeroes (LeetCode 283)")

    print("\n▸ 範例 1: nums=[0,1,0,3,12]")
    nums = [0, 1, 0, 3, 12]
    move_zeroes(nums, verbose=True)
    assert nums == [1, 3, 12, 0, 0], f"Unexpected: {nums}"

    print("\n▸ 範例 2: nums=[0,0,1]")
    nums = [0, 0, 1]
    move_zeroes(nums, verbose=True)
    assert nums == [1, 0, 0], f"Unexpected: {nums}"

    print("\n▸ 範例 3: nums=[4,2,4,0,0,3,0,5,1,0]")
    nums = [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]
    move_zeroes(nums, verbose=True)
    assert nums == [4, 2, 4, 3, 5, 1, 0, 0, 0, 0], f"Unexpected: {nums}"

    # --- Remove Element ---
    print_problem_header("2-3. Remove Element (LeetCode 27)")

    print("\n▸ 範例 1: nums=[3,2,2,3], val=3")
    nums = [3, 2, 2, 3]
    k = remove_element(nums, 3, verbose=True)
    assert k == 2 and sorted(nums[:k]) == [2, 2]

    print("\n▸ 範例 2: nums=[0,1,2,2,3,0,4,2], val=2")
    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    k = remove_element(nums, 2, verbose=True)
    assert k == 5 and sorted(nums[:k]) == [0, 0, 1, 3, 4]

    print("\n▸ 範例 3: nums=[1], val=1")
    nums = [1]
    k = remove_element(nums, 1, verbose=True)
    assert k == 0

    # ==================================================================
    # Section 3: 快慢指針
    # ==================================================================
    print_section_header("Section 3: 快慢指針 (Fast-Slow / Floyd's Cycle Detection)")

    print_problem_header("3-1. Find the Duplicate Number (LeetCode 287)")

    print("\n▸ 範例 1: nums=[1,3,4,2,2]")
    result = find_duplicate([1, 3, 4, 2, 2], verbose=True)
    assert result == 2, f"Expected 2, got {result}"

    print("\n▸ 範例 2: nums=[3,1,3,4,2]")
    result = find_duplicate([3, 1, 3, 4, 2], verbose=True)
    assert result == 3, f"Expected 3, got {result}"

    print("\n▸ 範例 3: nums=[2,5,9,6,9,3,8,9,7,1]")
    result = find_duplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1], verbose=True)
    assert result == 9, f"Expected 9, got {result}"

    # ==================================================================
    # Section 4: 比較總結
    # ==================================================================
    print_section_header("Section 4: 對向 vs 同向 vs 快慢 — 比較與決策框架")

    print("""
┌─────────────┬──────────────────┬──────────────────┬──────────────────────┐
│   類型       │ 對向雙指針        │ 同向雙指針        │ 快慢指針              │
│             │ (Opposite Dir.)  │ (Same Dir.)      │ (Fast-Slow)          │
├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ 指針起點     │ 一頭一尾          │ 都從頭開始        │ 都從頭開始            │
│ 移動方向     │ 向中間靠攏        │ 同方向前進        │ 同方向，速度不同       │
│ 終止條件     │ left >= right    │ fast 到底         │ 兩指針相遇            │
│ 時間複雜度   │ O(n)             │ O(n)             │ O(n)                 │
│ 空間複雜度   │ O(1)             │ O(1)             │ O(1)                 │
├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ 前提條件     │ 通常需要排序       │ 不一定要排序       │ 需要有 cycle 結構     │
│ 典型題型     │ Two Sum (sorted) │ 去重/移除/分區     │ 環偵測/找重複          │
│             │ Container Water  │ Move Zeroes      │ Linked List Cycle    │
│             │ 3Sum / 4Sum      │ Remove Element   │ Find Duplicate       │
│             │ Valid Palindrome │ Remove Duplicates│ Happy Number         │
└─────────────┴──────────────────┴──────────────────┴──────────────────────┘

決策流程 (Decision Framework):

  Q1: 陣列已排序 + 找一對/多對滿足條件的元素？
      → YES → 對向雙指針

  Q2: 需要 in-place 去重 / 移除特定值 / 把某類元素挪到一邊？
      → YES → 同向雙指針

  Q3: 問題可以轉化成「在某個 sequence 中偵測環」？
      → YES → 快慢指針 (Floyd's Cycle Detection)

  Q4: 題目有「回文」性質（頭尾對稱）？
      → YES → 對向雙指針

面試實戰提醒:
  - 先問面試官: input 是否已排序？ → 排序就優先想對向雙指針
  - 如果要求 O(1) space + in-place 修改 → 想同向雙指針
  - 如果限制不能修改原陣列且 O(1) space → 想快慢指針
  - 3Sum/4Sum 本質 = 排序 + 固定 k-2 個 + Two Sum II
""")

    # ==================================================================
    # 全部測試通過
    # ==================================================================
    print("=" * 70)
    print("  ALL TESTS PASSED! 所有測試通過！")
    print("=" * 70)


if __name__ == "__main__":
    main()
