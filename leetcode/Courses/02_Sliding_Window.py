"""
==============================================================================
  LeetCode 刷題教學：Sliding Window（滑動窗口）
  目標公司：Google / NVIDIA
  難度定位：Beginner → Intermediate
  教學語言：Traditional Chinese + English technical terms
==============================================================================

滑動窗口 (Sliding Window) 是處理「連續子陣列 / 子字串」問題的核心技巧。
核心思想：維護一個窗口 [left, right]，透過移動左右邊界來遍歷所有可能的子序列，
避免暴力法的 O(n^2) 時間複雜度，降至 O(n)。

三大類型：
  1. Fixed Size Window（固定大小窗口）：窗口大小 k 不變
  2. Variable Size Window（可變大小窗口）：窗口大小根據條件伸縮
  3. Window with Counter（窗口 + HashMap 計數）：需要追蹤字元頻率

本檔案所有程式碼皆可直接執行 (python3 02_Sliding_Window.py)
"""

from collections import defaultdict, Counter


# ============================================================================
# Section 1: 固定大小窗口 (Fixed Size Window)
# ============================================================================
# 模板：窗口大小固定為 k，right 每前進一步，left 也前進一步（當窗口已滿時）
#
# 模板程式碼：
#   for right in range(len(arr)):
#       加入 arr[right] 到窗口
#       if right >= k - 1:        # 窗口已達大小 k
#           記錄/更新答案
#           移除 arr[left] 從窗口
#           left += 1

# --------------------------------------------------------------------------
# 1.1 Maximum Sum Subarray of Size K（大小為 K 的最大子陣列和）
# --------------------------------------------------------------------------
# 題目：給定陣列和整數 k，找出大小恰好為 k 的連續子陣列的最大和。
# 思路：維護大小為 k 的窗口，滑動時加入右邊元素、移除左邊元素。
# Time: O(n), Space: O(1)

def max_sum_subarray_k(arr: list, k: int, verbose: bool = False) -> int:
    """找出大小為 k 的連續子陣列的最大和"""
    n = len(arr)
    if n < k:
        return 0

    window_sum = 0
    max_sum = float('-inf')
    left = 0

    for right in range(n):
        window_sum += arr[right]

        if verbose:
            window_str = str(arr[left:right + 1])
            print(f"  Step {right + 1}: right={right}, 加入 arr[{right}]={arr[right]} "
                  f"→ window_sum={window_sum}, window={window_str}")

        if right >= k - 1:  # 窗口已達大小 k
            max_sum = max(max_sum, window_sum)
            if verbose:
                print(f"    ✓ 窗口滿 k={k}, max_sum 更新為 {max_sum}")
            window_sum -= arr[left]  # 移除最左邊元素
            if verbose:
                print(f"    移除 arr[{left}]={arr[left]}, window_sum → {window_sum}")
            left += 1

    return max_sum


# --------------------------------------------------------------------------
# 1.2 Maximum Average Subarray I (LeetCode 643)
# --------------------------------------------------------------------------
# 題目：找出長度為 k 的連續子陣列的最大平均值。
# 思路：與 1.1 相同，最後除以 k。
# Time: O(n), Space: O(1)

def find_max_average(nums: list, k: int, verbose: bool = False) -> float:
    """找出大小為 k 的連續子陣列的最大平均值"""
    n = len(nums)
    window_sum = 0
    max_sum = float('-inf')
    left = 0

    for right in range(n):
        window_sum += nums[right]

        if verbose:
            print(f"  Step {right + 1}: right={right}, 加入 nums[{right}]={nums[right]} "
                  f"→ window_sum={window_sum}, window={nums[left:right + 1]}")

        if right >= k - 1:
            max_sum = max(max_sum, window_sum)
            if verbose:
                avg = window_sum / k
                print(f"    ✓ 窗口滿, avg={avg:.2f}, max_avg={max_sum / k:.2f}")
            window_sum -= nums[left]
            if verbose:
                print(f"    移除 nums[{left}]={nums[left]}, window_sum → {window_sum}")
            left += 1

    return max_sum / k


# --------------------------------------------------------------------------
# 1.3 Contains Duplicate II (LeetCode 219)
# --------------------------------------------------------------------------
# 題目：陣列中是否存在 nums[i] == nums[j] 且 abs(i-j) <= k。
# 思路：維護大小為 k 的 set 窗口，檢查新元素是否已在 set 中。
# Time: O(n), Space: O(k)

def contains_nearby_duplicate(nums: list, k: int, verbose: bool = False) -> bool:
    """檢查是否有重複元素在距離 k 以內"""
    window_set = set()
    left = 0

    for right in range(len(nums)):
        if verbose:
            print(f"  Step {right + 1}: right={right}, nums[{right}]={nums[right]}, "
                  f"window_set={window_set}")

        if nums[right] in window_set:
            if verbose:
                print(f"    ✓ 找到重複！nums[{right}]={nums[right]} 已在窗口中")
            return True

        window_set.add(nums[right])

        if right >= k:  # 窗口超過 k，移除最左邊
            window_set.remove(nums[left])
            if verbose:
                print(f"    窗口超過 k={k}, 移除 nums[{left}]={nums[left]}, "
                      f"set → {window_set}")
            left += 1

    return False


# ============================================================================
# Section 2: 可變大小窗口 (Variable Size Window)
# ============================================================================
# 模板：窗口大小不固定，根據條件收縮左邊界。
#
# 模板程式碼（找最短）：
#   for right in range(len(arr)):
#       加入 arr[right] 到窗口
#       while 窗口滿足條件:
#           更新答案（取最小）
#           移除 arr[left]，left += 1
#
# 模板程式碼（找最長）：
#   for right in range(len(arr)):
#       加入 arr[right] 到窗口
#       while 窗口不滿足條件:
#           移除 arr[left]，left += 1
#       更新答案（取最大）

# --------------------------------------------------------------------------
# 2.1 Minimum Size Subarray Sum (LeetCode 209)
# --------------------------------------------------------------------------
# 題目：找出和 >= target 的最短連續子陣列長度。
# 思路：right 擴張直到 sum >= target，然後收縮 left 找最短。
# Time: O(n), Space: O(1)

def min_subarray_len(target: int, nums: list, verbose: bool = False) -> int:
    """找出和 >= target 的最短連續子陣列長度"""
    n = len(nums)
    left = 0
    window_sum = 0
    min_len = float('inf')
    step = 0

    for right in range(n):
        window_sum += nums[right]
        step += 1

        if verbose:
            print(f"  Step {step}: right={right}, 加入 nums[{right}]={nums[right]} "
                  f"→ sum={window_sum}, window={nums[left:right + 1]}")

        while window_sum >= target:
            curr_len = right - left + 1
            min_len = min(min_len, curr_len)
            if verbose:
                print(f"    ✓ sum={window_sum} >= {target}, len={curr_len}, "
                      f"min_len={min_len}")
            window_sum -= nums[left]
            if verbose:
                print(f"    收縮: 移除 nums[{left}]={nums[left]}, "
                      f"sum → {window_sum}, left → {left + 1}")
            left += 1

    return min_len if min_len != float('inf') else 0


# --------------------------------------------------------------------------
# 2.2 Longest Substring Without Repeating Characters (LeetCode 3)
# --------------------------------------------------------------------------
# 題目：找出不含重複字元的最長子字串長度。
# 思路：用 set 追蹤窗口內字元，遇到重複就收縮 left。
# Time: O(n), Space: O(min(n, charset))

def length_of_longest_substring(s: str, verbose: bool = False) -> int:
    """找出不含重複字元的最長子字串長度"""
    char_set = set()
    left = 0
    max_len = 0
    step = 0

    for right in range(len(s)):
        step += 1
        if verbose:
            print(f"  Step {step}: right={right}, char='{s[right]}', "
                  f"char_set={char_set}")

        while s[right] in char_set:
            if verbose:
                print(f"    '{s[right]}' 重複! 移除 '{s[left]}', left → {left + 1}")
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        curr_len = right - left + 1
        max_len = max(max_len, curr_len)

        if verbose:
            print(f"    加入 '{s[right]}', window='{s[left:right + 1]}', "
                  f"len={curr_len}, max_len={max_len}")

    return max_len


# --------------------------------------------------------------------------
# 2.3 Longest Substring with At Most K Distinct Characters (LeetCode 340)
# --------------------------------------------------------------------------
# 題目：找出最多包含 k 個不同字元的最長子字串長度。
# 思路：用 HashMap 記錄字元頻率，超過 k 種時收縮 left。
# Time: O(n), Space: O(k)

def longest_k_distinct(s: str, k: int, verbose: bool = False) -> int:
    """找出最多 k 個不同字元的最長子字串長度"""
    if k == 0 or not s:
        return 0

    char_count = defaultdict(int)
    left = 0
    max_len = 0
    step = 0

    for right in range(len(s)):
        step += 1
        char_count[s[right]] += 1

        if verbose:
            print(f"  Step {step}: right={right}, char='{s[right]}', "
                  f"count={dict(char_count)}, distinct={len(char_count)}")

        while len(char_count) > k:
            if verbose:
                print(f"    distinct={len(char_count)} > k={k}, "
                      f"移除 '{s[left]}'")
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
            if verbose:
                print(f"    left → {left}, count={dict(char_count)}")

        curr_len = right - left + 1
        max_len = max(max_len, curr_len)
        if verbose:
            print(f"    window='{s[left:right + 1]}', len={curr_len}, "
                  f"max_len={max_len}")

    return max_len


# ============================================================================
# Section 3: 窗口計數型 (Window with Counter / HashMap)
# ============================================================================
# 模板：用 HashMap 追蹤窗口內字元頻率，對比目標頻率。
#
# 核心變數：
#   - need: 目標字元頻率 (Counter of target)
#   - window: 當前窗口字元頻率
#   - formed: 已滿足條件的字元種類數
#   - required: 需要滿足的字元種類總數

# --------------------------------------------------------------------------
# 3.1 Minimum Window Substring (LeetCode 76)
# --------------------------------------------------------------------------
# 題目：在 s 中找出包含 t 所有字元的最短子字串。
# 思路：擴張 right 直到包含所有字元，收縮 left 找最短。
# Time: O(|s| + |t|), Space: O(|s| + |t|)

def min_window(s: str, t: str, verbose: bool = False) -> str:
    """找出 s 中包含 t 所有字元的最短子字串"""
    if not s or not t or len(s) < len(t):
        return ""

    need = Counter(t)           # 需要的字元頻率
    required = len(need)        # 需要滿足的字元種類數
    window = defaultdict(int)   # 窗口內字元頻率
    formed = 0                  # 已滿足的字元種類數

    left = 0
    result = (float('inf'), 0, 0)  # (長度, left, right)
    step = 0

    if verbose:
        print(f"  need={dict(need)}, required={required}")

    for right in range(len(s)):
        step += 1
        char = s[right]
        window[char] += 1

        # 檢查這個字元是否剛好滿足需求
        if char in need and window[char] == need[char]:
            formed += 1

        if verbose:
            print(f"  Step {step}: right={right}, char='{char}' → "
                  f"window={dict(window)}, formed={formed}/{required}")
            vis = s[:left] + "[" + s[left:right + 1] + "]" + s[right + 1:]
            print(f"    {vis}")

        # 嘗試收縮左邊界
        while formed == required:
            curr_len = right - left + 1
            if curr_len < result[0]:
                result = (curr_len, left, right)
                if verbose:
                    print(f"    ✓ 找到候選: '{s[left:right + 1]}', len={curr_len}")

            # 移除左邊字元
            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                formed -= 1
            left += 1
            if verbose:
                print(f"    收縮: 移除 '{left_char}', left → {left}, "
                      f"formed={formed}")

    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]


# --------------------------------------------------------------------------
# 3.2 Find All Anagrams in a String (LeetCode 438)
# --------------------------------------------------------------------------
# 題目：找出 s 中所有 p 的 anagram 的起始索引。
# 思路：固定大小窗口 (len(p)) + Counter 比對。
# Time: O(n), Space: O(1) -- 最多 26 個字母

def find_anagrams(s: str, p: str, verbose: bool = False) -> list:
    """找出 s 中所有 p 的 anagram（字母重排）的起始索引"""
    if len(s) < len(p):
        return []

    need = Counter(p)
    required = len(need)
    window = defaultdict(int)
    formed = 0
    result = []
    left = 0
    step = 0

    if verbose:
        print(f"  need={dict(need)}, required={required}, window_size={len(p)}")

    for right in range(len(s)):
        step += 1
        char = s[right]
        window[char] += 1

        if char in need and window[char] == need[char]:
            formed += 1

        if verbose:
            print(f"  Step {step}: right={right}, char='{char}', "
                  f"window={dict(window)}, formed={formed}/{required}")

        # 窗口超過 len(p) 時，收縮左邊
        if right - left + 1 > len(p):
            left_char = s[left]
            if left_char in need and window[left_char] == need[left_char]:
                formed -= 1
            window[left_char] -= 1
            if window[left_char] == 0:
                del window[left_char]
            left += 1
            if verbose:
                print(f"    收縮: 移除 '{left_char}', left → {left}")

        if formed == required:
            result.append(left)
            if verbose:
                print(f"    ✓ 找到 anagram 起始於 index {left}: "
                      f"'{s[left:right + 1]}'")

    return result


# --------------------------------------------------------------------------
# 3.3 Permutation in String (LeetCode 567)
# --------------------------------------------------------------------------
# 題目：判斷 s2 是否包含 s1 的排列（permutation）。
# 思路：與 3.2 幾乎相同，但只需回傳 True/False。
# Time: O(n), Space: O(1)

def check_inclusion(s1: str, s2: str, verbose: bool = False) -> bool:
    """判斷 s2 是否包含 s1 的排列"""
    if len(s1) > len(s2):
        return False

    need = Counter(s1)
    required = len(need)
    window = defaultdict(int)
    formed = 0
    left = 0
    step = 0

    if verbose:
        print(f"  need={dict(need)}, required={required}, window_size={len(s1)}")

    for right in range(len(s2)):
        step += 1
        char = s2[right]
        window[char] += 1

        if char in need and window[char] == need[char]:
            formed += 1

        if verbose:
            print(f"  Step {step}: right={right}, char='{char}', "
                  f"window={dict(window)}, formed={formed}/{required}")

        if right - left + 1 > len(s1):
            left_char = s2[left]
            if left_char in need and window[left_char] == need[left_char]:
                formed -= 1
            window[left_char] -= 1
            if window[left_char] == 0:
                del window[left_char]
            left += 1
            if verbose:
                print(f"    收縮: 移除 '{left_char}', left → {left}")

        if formed == required:
            if verbose:
                print(f"    ✓ 找到排列: '{s2[left:right + 1]}'")
            return True

    return False


# ============================================================================
# Section 4: 固定 vs 可變 vs 計數 — 比較與決策樹
# ============================================================================
#
# ┌─ 問題要求「連續子陣列/子字串」嗎？
# │
# ├─ 否 → 不適用 Sliding Window
# │
# └─ 是 → 窗口大小固定嗎？
#     │
#     ├─ 是（題目給定 k）
#     │   └─ 使用【Fixed Size Window】
#     │       例：Max Sum Subarray of Size K, Max Average, Contains Duplicate II
#     │
#     └─ 否（窗口大小不固定）
#         │
#         ├─ 需要追蹤字元頻率/計數嗎？
#         │   │
#         │   ├─ 是 → 使用【Window + Counter/HashMap】
#         │   │   例：Min Window Substring, Find Anagrams, Permutation in String
#         │   │
#         │   └─ 否 → 使用【Variable Size Window】
#         │       例：Min Size Subarray Sum, Longest Substring Without Repeat
#         │
#         └─ 找最長還是最短？
#             ├─ 最短 → 滿足條件時收縮 (while valid, shrink)
#             └─ 最長 → 不滿足條件時收縮 (while invalid, shrink)
#
# ======================== 三大模板總結 ========================
#
# 【模板一：Fixed Size】
#   left = 0
#   for right in range(n):
#       加入 arr[right]
#       if right >= k - 1:
#           更新答案
#           移除 arr[left]; left += 1
#
# 【模板二：Variable Size (找最短)】
#   left = 0
#   for right in range(n):
#       加入 arr[right]
#       while 滿足條件:
#           更新答案(min)
#           移除 arr[left]; left += 1
#
# 【模板三：Window + Counter】
#   need = Counter(target)
#   required = len(need)
#   formed = 0
#   left = 0
#   for right in range(n):
#       char = s[right]
#       window[char] += 1
#       if char in need and window[char] == need[char]:
#           formed += 1
#       while formed == required:
#           更新答案
#           移除 s[left]; 若 window < need 則 formed -= 1; left += 1


# ============================================================================
# main() — 執行所有範例與測試
# ============================================================================

def main():
    print("=" * 70)
    print(" Sliding Window 滑動窗口 — 完整教學與範例")
    print("=" * 70)

    # ==================================================================
    # Section 1: 固定大小窗口
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 1: 固定大小窗口 (Fixed Size Window)")
    print("=" * 70)

    # --- 1.1 Maximum Sum Subarray of Size K ---
    print("\n--- 1.1 Maximum Sum Subarray of Size K ---")

    print("\n範例 1: arr=[2,1,5,1,3,2], k=3")
    # 手動 trace:
    # Step 1: right=0, 加入 2 → sum=2, window=[2]
    # Step 2: right=1, 加入 1 → sum=3, window=[2,1]
    # Step 3: right=2, 加入 5 → sum=8, window=[2,1,5] ✓ max=8, 移除 2, sum=6
    # Step 4: right=3, 加入 1 → sum=7, window=[1,5,1] ✓ max=8, 移除 1, sum=6
    # Step 5: right=4, 加入 3 → sum=9, window=[5,1,3] ✓ max=9, 移除 5, sum=4
    # Step 6: right=5, 加入 2 → sum=6, window=[1,3,2] ✓ max=9, 移除 1, sum=5
    # 答案: 9
    result = max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3, verbose=True)
    print(f"  結果: {result}")
    assert result == 9

    print("\n範例 2: arr=[1,9,-1,-2,7,3,-1,2], k=4")
    # 窗口和: [1,9,-1,-2]=7, [9,-1,-2,7]=13, [-1,-2,7,3]=7,
    #         [-2,7,3,-1]=7, [7,3,-1,2]=11 → max=13
    result = max_sum_subarray_k([1, 9, -1, -2, 7, 3, -1, 2], 4, verbose=True)
    print(f"  結果: {result}")
    assert result == 13

    print("\n範例 3: arr=[4,2,1,7,8,1,2,8,1,0], k=3")
    # 窗口和: [4,2,1]=7, [2,1,7]=10, [1,7,8]=16, [7,8,1]=16,
    #         [8,1,2]=11, [1,2,8]=11, [2,8,1]=11, [8,1,0]=9 → max=16
    result = max_sum_subarray_k([4, 2, 1, 7, 8, 1, 2, 8, 1, 0], 3, verbose=True)
    print(f"  結果: {result}")
    assert result == 16

    # --- 1.2 Maximum Average Subarray ---
    print("\n--- 1.2 Maximum Average Subarray I (LC 643) ---")

    print("\n範例 1: nums=[1,12,-5,-6,50,3], k=4")
    # 窗口和: [1,12,-5,-6]=2→avg=0.5, [12,-5,-6,50]=51→avg=12.75,
    #         [-5,-6,50,3]=42→avg=10.5 → max_avg=12.75
    result = find_max_average([1, 12, -5, -6, 50, 3], 4, verbose=True)
    print(f"  結果: {result:.5f}")
    assert abs(result - 12.75) < 1e-5

    print("\n範例 2: nums=[5,5,5,5,5], k=2")
    # 所有窗口和 = 10 → avg = 5.0
    result = find_max_average([5, 5, 5, 5, 5], 2, verbose=True)
    print(f"  結果: {result:.5f}")
    assert abs(result - 5.0) < 1e-5

    print("\n範例 3: nums=[0,4,0,3,2], k=1")
    # 每個元素自己就是窗口 → max = 4
    result = find_max_average([0, 4, 0, 3, 2], 1, verbose=True)
    print(f"  結果: {result:.5f}")
    assert abs(result - 4.0) < 1e-5

    # --- 1.3 Contains Duplicate II ---
    print("\n--- 1.3 Contains Duplicate II (LC 219) ---")

    print("\n範例 1: nums=[1,2,3,1], k=3")
    # Step 1: right=0, 1 → set={1}
    # Step 2: right=1, 2 → set={1,2}
    # Step 3: right=2, 3 → set={1,2,3}
    # Step 4: right=3, 1 → 1 in set! → True (|3-0|=3 <= 3)
    result = contains_nearby_duplicate([1, 2, 3, 1], 3, verbose=True)
    print(f"  結果: {result}")
    assert result is True

    print("\n範例 2: nums=[1,0,1,1], k=1")
    # Step 1: right=0, 1 → set={1}
    # Step 2: right=1, 0 → set={1,0}, 移除 nums[0]=1 → set={0}
    # Step 3: right=2, 1 → set={0,1}, 移除 nums[1]=0 → set={1}
    # Step 4: right=3, 1 → 1 in set! → True
    result = contains_nearby_duplicate([1, 0, 1, 1], 1, verbose=True)
    print(f"  結果: {result}")
    assert result is True

    print("\n範例 3: nums=[1,2,3,1,2,3], k=2")
    # 窗口大小 2，每次只看前後 2 格，無重複在範圍內 → False
    result = contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2, verbose=True)
    print(f"  結果: {result}")
    assert result is False

    # ==================================================================
    # Section 2: 可變大小窗口
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 2: 可變大小窗口 (Variable Size Window)")
    print("=" * 70)

    # --- 2.1 Minimum Size Subarray Sum ---
    print("\n--- 2.1 Minimum Size Subarray Sum (LC 209) ---")

    print("\n範例 1: target=7, nums=[2,3,1,2,4,3]")
    # right=0: sum=2 < 7
    # right=1: sum=5 < 7
    # right=2: sum=6 < 7
    # right=3: sum=8 >= 7 → len=4, 收縮: 移除2→sum=6
    # right=4: sum=10 >= 7 → len=4, 收縮: 移除3→sum=7 → len=3, 收縮: 移除1→sum=6
    # right=5: sum=9 >= 7 → len=3, 收縮: 移除2→sum=7 → len=2, 收縮: 移除4→sum=3
    # 答案: 2 (子陣列 [4,3])
    result = min_subarray_len(7, [2, 3, 1, 2, 4, 3], verbose=True)
    print(f"  結果: {result}")
    assert result == 2

    print("\n範例 2: target=4, nums=[1,4,4]")
    # right=0: sum=1 < 4
    # right=1: sum=5 >= 4 → len=2, 收縮: 移除1→sum=4 → len=1! 收縮: 移除4→sum=0
    # right=2: sum=4 >= 4 → len=1!
    # 答案: 1
    result = min_subarray_len(4, [1, 4, 4], verbose=True)
    print(f"  結果: {result}")
    assert result == 1

    print("\n範例 3: target=11, nums=[1,1,1,1,1,1,1,1]")
    # 全部加起來 = 8 < 11 → 不可能 → 0
    result = min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1], verbose=True)
    print(f"  結果: {result}")
    assert result == 0

    # --- 2.2 Longest Substring Without Repeating Characters ---
    print("\n--- 2.2 Longest Substring Without Repeating Characters (LC 3) ---")

    print("\n範例 1: s='abcabcbb'")
    # Step 1: 'a' → set={a}, window='a', len=1, max=1
    # Step 2: 'b' → set={a,b}, window='ab', len=2, max=2
    # Step 3: 'c' → set={a,b,c}, window='abc', len=3, max=3
    # Step 4: 'a' → 重複! 移除 'a' → set={b,c}
    #         加入 'a' → set={b,c,a}, window='bca', len=3, max=3
    # Step 5: 'b' → 重複! 移除 'b' → set={c,a}
    #         加入 'b' → set={c,a,b}, window='cab', len=3, max=3
    # Step 6: 'c' → 重複! 移除 'c' → set={a,b}
    #         加入 'c' → set={a,b,c}, window='abc', len=3, max=3
    # Step 7: 'b' → 重複! 移除 'a' → {b,c}, 還重複! 移除 'b' → {c}
    #         加入 'b' → {c,b}, window='cb', len=2, max=3
    # Step 8: 'b' → 重複! 移除 'c' → {b}, 還重複! 移除 'b' → {}
    #         加入 'b' → {b}, window='b', len=1, max=3
    # 答案: 3
    result = length_of_longest_substring("abcabcbb", verbose=True)
    print(f"  結果: {result}")
    assert result == 3

    print("\n範例 2: s='bbbbb'")
    # 每次都重複，window 只能是單個 'b' → max=1
    result = length_of_longest_substring("bbbbb", verbose=True)
    print(f"  結果: {result}")
    assert result == 1

    print("\n範例 3: s='pwwkew'")
    # Step 1: 'p' → {p}, window='p', max=1
    # Step 2: 'w' → {p,w}, window='pw', max=2
    # Step 3: 'w' → 重複! 移除 'p' → {w}, 重複! 移除 'w' → {}
    #         加入 'w' → {w}, window='w', max=2
    # Step 4: 'k' → {w,k}, window='wk', max=2
    # Step 5: 'e' → {w,k,e}, window='wke', max=3
    # Step 6: 'w' → 重複! 移除 'w' → {k,e}
    #         加入 'w' → {k,e,w}, window='kew', max=3
    # 答案: 3
    result = length_of_longest_substring("pwwkew", verbose=True)
    print(f"  結果: {result}")
    assert result == 3

    # --- 2.3 Longest Substring with At Most K Distinct Characters ---
    print("\n--- 2.3 Longest Substring with At Most K Distinct Characters (LC 340) ---")

    print("\n範例 1: s='eceba', k=2")
    # Step 1: 'e' → {e:1}, distinct=1 <= 2, window='e', max=1
    # Step 2: 'c' → {e:1,c:1}, distinct=2 <= 2, window='ec', max=2
    # Step 3: 'e' → {e:2,c:1}, distinct=2 <= 2, window='ece', max=3
    # Step 4: 'b' → {e:2,c:1,b:1}, distinct=3 > 2!
    #         移除 'e' → {e:1,c:1,b:1}, 還 > 2! 移除 'c' → {e:1,b:1}
    #         window='eb', max=3
    # Step 5: 'a' → {e:1,b:1,a:1}, distinct=3 > 2!
    #         移除 'e' → {b:1,a:1}, window='ba', max=3
    # 答案: 3 ('ece')
    result = longest_k_distinct("eceba", 2, verbose=True)
    print(f"  結果: {result}")
    assert result == 3

    print("\n範例 2: s='aaahhibc', k=2")
    # 'aaa' → distinct=1, 'aaahh' → distinct=2 → len=5
    # 'aaahhi' → distinct=3 → 收縮到 'hhi' → distinct=2 → len=3
    # 最長 = 5 ('aaahh')
    result = longest_k_distinct("aaahhibc", 2, verbose=True)
    print(f"  結果: {result}")
    assert result == 5

    print("\n範例 3: s='aabbcc', k=3")
    # 最多 3 種字元，全部都只有 3 種 → 整個字串 = 6
    result = longest_k_distinct("aabbcc", 3, verbose=True)
    print(f"  結果: {result}")
    assert result == 6

    # ==================================================================
    # Section 3: 窗口計數型
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 3: 窗口計數型 (Window with Counter/HashMap)")
    print("=" * 70)

    # --- 3.1 Minimum Window Substring ---
    print("\n--- 3.1 Minimum Window Substring (LC 76) ---")

    print("\n範例 1: s='ADOBECODEBANC', t='ABC'")
    # need={A:1, B:1, C:1}, required=3
    #
    # right=0: 'A' → window={A:1} → formed=1/3
    #          [A]DOBECODEBANC
    # right=1: 'D' → window={A:1,D:1} → formed=1/3
    #          [AD]OBECODEBANC
    # right=2: 'O' → window={A:1,D:1,O:1} → formed=1/3
    # right=3: 'B' → window={...,B:1} → formed=2/3
    # right=4: 'E' → window={...,E:1} → formed=2/3
    # right=5: 'C' → window={...,C:1} → formed=3/3 ✓
    #          找到 'ADOBEC' len=6
    #          收縮: 移除 'A' → formed=2/3
    # right=9: 'B' → formed=3/3 again → 'CODEBA' 等
    # right=10: 'A' → formed=3/3 → 繼續收縮
    # right=12: 'C' → 最終收縮到 'BANC' len=4 ✓
    # 答案: 'BANC'
    result = min_window("ADOBECODEBANC", "ABC", verbose=True)
    print(f"  結果: '{result}'")
    assert result == "BANC"

    print("\n範例 2: s='a', t='a'")
    result = min_window("a", "a", verbose=True)
    print(f"  結果: '{result}'")
    assert result == "a"

    print("\n範例 3: s='a', t='aa'")
    # 需要 2 個 'a'，但 s 只有 1 個 → 不可能 → ""
    result = min_window("a", "aa", verbose=True)
    print(f"  結果: '{result}'")
    assert result == ""

    # --- 3.2 Find All Anagrams in String ---
    print("\n--- 3.2 Find All Anagrams in a String (LC 438) ---")

    print("\n範例 1: s='cbaebabacd', p='abc'")
    # need={a:1,b:1,c:1}, window_size=3
    # index 0: 'cba' → formed=3 ✓ → result=[0]
    # index 1: 'bae' → formed=2 (少了 c)
    # ...
    # index 6: 'bac' → formed=3 ✓ → result=[0,6]
    # 答案: [0, 6]
    result = find_anagrams("cbaebabacd", "abc", verbose=True)
    print(f"  結果: {result}")
    assert result == [0, 6]

    print("\n範例 2: s='abab', p='ab'")
    # need={a:1,b:1}, window_size=2
    # 'ab' ✓, 'ba' ✓, 'ab' ✓ → [0,1,2]
    result = find_anagrams("abab", "ab", verbose=True)
    print(f"  結果: {result}")
    assert result == [0, 1, 2]

    print("\n範例 3: s='aaaaaaaaaa', p='aaaa'")
    # need={a:4}, window_size=4
    # 每個位置都是 'aaaa' → [0,1,2,3,4,5,6]
    result = find_anagrams("aaaaaaaaaa", "aaaa", verbose=True)
    print(f"  結果: {result}")
    assert result == [0, 1, 2, 3, 4, 5, 6]

    # --- 3.3 Permutation in String ---
    print("\n--- 3.3 Permutation in String (LC 567) ---")

    print("\n範例 1: s1='ab', s2='eidbaooo'")
    # need={a:1,b:1}, window_size=2
    # 'ei' → no, 'id' → no, 'db' → no, 'ba' → ✓ True
    result = check_inclusion("ab", "eidbaooo", verbose=True)
    print(f"  結果: {result}")
    assert result is True

    print("\n範例 2: s1='ab', s2='eidboaoo'")
    # 沒有連續的 'ab' 或 'ba' → False
    result = check_inclusion("ab", "eidboaoo", verbose=True)
    print(f"  結果: {result}")
    assert result is False

    print("\n範例 3: s1='adc', s2='dcda'")
    # need={a:1,d:1,c:1}, window_size=3
    # 'dcd' → d:2,c:1 → formed: c ok, d 超過 → no
    # 'cda' → c:1,d:1,a:1 → ✓ True
    result = check_inclusion("adc", "dcda", verbose=True)
    print(f"  結果: {result}")
    assert result is True

    # ==================================================================
    # Section 4: 比較總結
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 4: 三大模式比較總結")
    print("=" * 70)
    print("""
    ┌──────────────────┬────────────────────┬─────────────────────┬────────────────────────┐
    │     類型         │  Fixed Size Window │ Variable Size Window│ Window + Counter       │
    ├──────────────────┼────────────────────┼─────────────────────┼────────────────────────┤
    │ 窗口大小         │ 固定 k             │ 動態伸縮            │ 動態伸縮               │
    │ 左邊界移動時機   │ right >= k-1 時    │ 滿足/違反條件時     │ formed == required 時  │
    │ 資料結構         │ sum / set          │ sum / set           │ HashMap (Counter)      │
    │ 典型題目         │ Max Sum K          │ Min Subarray Sum    │ Min Window Substring   │
    │                  │ Max Average        │ Longest No Repeat   │ Find Anagrams          │
    │                  │ Contains Dup II    │ K Distinct Chars    │ Permutation in String  │
    │ 時間複雜度       │ O(n)               │ O(n)                │ O(n)                   │
    └──────────────────┴────────────────────┴─────────────────────┴────────────────────────┘

    決策流程:
    1. 題目是否涉及「連續子陣列/子字串」？ → 否: 不用 Sliding Window
    2. 窗口大小是否固定(題目給了 k)？    → 是: Fixed Size Window
    3. 是否需要比對字元頻率？             → 是: Window + Counter
    4. 找最短？ → while(valid) shrink     → 找最長？ → while(invalid) shrink
    """)

    print("=" * 70)
    print(" 全部測試通過！All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
