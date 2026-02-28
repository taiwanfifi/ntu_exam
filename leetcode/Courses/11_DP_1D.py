"""
LeetCode 12: Dynamic Programming 一維 (1D DP)
==============================================
適用對象：LeetCode 初學者，準備 Google / NVIDIA 面試
教學風格：每題皆附 step-by-step 數值 trace，用「跑一次給你看」取代抽象描述

DP 是面試最難的主題之一，但有系統地學就不可怕。
本檔案從 Fibonacci 開始，一步步建立 DP 直覺。

每題都會展示：
  1. 暴力法 / 遞迴為什麼慢（Recursion Tree）
  2. 重疊子問題在哪裡（Overlapping Subproblems）
  3. 狀態轉移方程（Transition Formula）
  4. Bottom-up DP 表格逐步填充
  5. （選做）Top-down Memoization 版本

Google 高頻：Climbing Stairs, House Robber, Coin Change, LIS, Word Break
NVIDIA 高頻：Maximum Subarray, Stock 系列, Jump Game
"""

# ============================================================================
# Section 1: DP 核心概念 (Core Concepts)
# ============================================================================

def dp_core_concepts(verbose=True):
    """
    DP 的本質：
    1. Overlapping Subproblems（重疊子問題）— 相同子問題被重複計算
    2. Optimal Substructure（最優子結構）— 大問題的最優解包含子問題的最優解

    Top-down (Memoization，記憶化搜尋):
      - 從大問題往下遞迴，遇到算過的直接查表
      - 寫起來像遞迴，加一個 memo dict/array

    Bottom-up (Tabulation，列表法):
      - 從最小的子問題開始，一路填到大問題
      - 用迴圈 + dp array，不用遞迴
    """
    if not verbose:
        return

    print("=" * 70)
    print("Section 1: DP 核心概念 (Core Concepts)")
    print("=" * 70)
    print("""
    什麼是 Dynamic Programming？
    ────────────────────────────
    DP 不是一種特定演算法，而是一種「解題策略」：
    把大問題拆成小問題，記住小問題的答案，避免重複計算。

    兩個必要條件：
    ┌────────────────────────────────────────────────────────┐
    │ 1. Overlapping Subproblems（重疊子問題）                │
    │    → 同一個子問題會被計算多次                            │
    │    → 例如: fib(3) 在計算 fib(5) 時被算了很多次           │
    │                                                        │
    │ 2. Optimal Substructure（最優子結構）                   │
    │    → 大問題的最優解，可以由子問題的最優解推導出來          │
    │    → 例如: 到第 n 階的方法數 = 到第 n-1 階 + 到第 n-2 階 │
    └────────────────────────────────────────────────────────┘

    Top-down vs Bottom-up:
    ┌──────────────────┬──────────────────────────┐
    │  Top-down         │  Bottom-up               │
    │  (Memoization)    │  (Tabulation)            │
    ├──────────────────┼──────────────────────────┤
    │  遞迴 + memo      │  迴圈 + dp array         │
    │  從大問題往下拆    │  從最小子問題往上建       │
    │  比較直覺          │  通常比較快（無遞迴開銷） │
    │  可能 stack overflow│  不會 stack overflow    │
    └──────────────────┴──────────────────────────┘
    """)


# ────────────────────────────────────────────────────────────────
# Fibonacci: DP 的 Hello World
# ────────────────────────────────────────────────────────────────

def fibonacci_brute_force(n):
    """純遞迴 — O(2^n) 時間, O(n) 空間 (call stack)"""
    if n <= 1:
        return n
    return fibonacci_brute_force(n - 1) + fibonacci_brute_force(n - 2)


def fibonacci_memo(n, memo=None):
    """Top-down Memoization — O(n) 時間, O(n) 空間"""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tabulation(n):
    """Bottom-up Tabulation — O(n) 時間, O(n) 空間"""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fibonacci_optimized(n):
    """Space Optimized — O(n) 時間, O(1) 空間"""
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1


def fibonacci_demo(verbose=True):
    """Fibonacci 完整教學：從暴力到最優"""
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("Fibonacci: DP 的 Hello World")
    print("─" * 70)
    print("""
    fib(0)=0, fib(1)=1, fib(n) = fib(n-1) + fib(n-2)

    ── 範例 1: n = 5 ──────────────────────────────

    暴力遞迴的 Recursion Tree（看看有多少重複！）:
                        fib(5)
                       /      \\
                  fib(4)        fib(3)
                 /    \\        /    \\
            fib(3)   fib(2)  fib(2) fib(1)
           /    \\   /    \\   /    \\
      fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
      /    \\
    fib(1) fib(0)

    fib(3) 被算了 2 次! fib(2) 被算了 3 次! → 這就是「重疊子問題」

    Bottom-up DP 表格填充:
    dp[0] = 0
    dp[1] = 1
    dp[2] = dp[1] + dp[0] = 1 + 0 = 1
    dp[3] = dp[2] + dp[1] = 1 + 1 = 2
    dp[4] = dp[3] + dp[2] = 2 + 1 = 3
    dp[5] = dp[4] + dp[3] = 3 + 2 = 5

    dp = [0, 1, 1, 2, 3, 5] → answer = 5
    """)

    for n in [5, 8, 10]:
        result = fibonacci_optimized(n)
        dp = [0] * (n + 1)
        if n >= 1:
            dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        print(f"    ── 範例: n = {n} ──")
        print(f"    dp = {dp}")
        print(f"    fib({n}) = {result}\n")

    print("""    四種解法複雜度比較:
    ┌──────────────────┬───────────┬───────────┐
    │ 方法              │ Time      │ Space     │
    ├──────────────────┼───────────┼───────────┤
    │ 暴力遞迴          │ O(2^n)    │ O(n)      │
    │ Memoization       │ O(n)      │ O(n)      │
    │ Tabulation        │ O(n)      │ O(n)      │
    │ Space Optimized   │ O(n)      │ O(1)      │
    └──────────────────┴───────────┴───────────┘""")


# ============================================================================
# Section 2: 線性 DP (Linear DP)
# ============================================================================

# ────────────────────────────────────────────────────────────────
# LC 70. Climbing Stairs（爬樓梯）
# ────────────────────────────────────────────────────────────────

def climbing_stairs(n):
    """
    LC 70. Climbing Stairs
    每次可以爬 1 或 2 階，問爬到第 n 階有幾種方法。

    狀態: dp[i] = 爬到第 i 階的方法數
    轉移方程: dp[i] = dp[i-1] + dp[i-2]
      （到第 i 階 = 從 i-1 爬 1 步 + 從 i-2 爬 2 步）
    Base case: dp[1] = 1, dp[2] = 2

    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1


def climbing_stairs_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "=" * 70)
    print("Section 2: 線性 DP (Linear DP)")
    print("=" * 70)
    print("\n" + "─" * 70)
    print("LC 70. Climbing Stairs（爬樓梯）")
    print("─" * 70)
    print("""
    每次可以爬 1 或 2 階，問爬到第 n 階有幾種方法。

    轉移方程: dp[i] = dp[i-1] + dp[i-2]
    直覺: 要到第 i 階，只有兩種走法 —
          從第 i-1 階爬 1 步，或從第 i-2 階爬 2 步

    ── 範例 1: n = 3 ──────────────────────────────
    dp[1] = 1                    (只有 [1])
    dp[2] = 2                    ([1,1] 或 [2])
    dp[3] = dp[2] + dp[1] = 2 + 1 = 3
            ([1,1,1], [1,2], [2,1])

    dp = [_, 1, 2, 3] → answer = 3

    ── 範例 2: n = 5 ──────────────────────────────
    dp[1] = 1
    dp[2] = 2
    dp[3] = dp[2] + dp[1] = 2 + 1 = 3
    dp[4] = dp[3] + dp[2] = 3 + 2 = 5
    dp[5] = dp[4] + dp[3] = 5 + 3 = 8

    dp = [_, 1, 2, 3, 5, 8] → answer = 8

    ── 範例 3: n = 10 ─────────────────────────────
    dp = [_, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89] → answer = 89
    """)
    for n in [3, 5, 10]:
        print(f"    climbing_stairs({n}) = {climbing_stairs(n)}")


# ────────────────────────────────────────────────────────────────
# LC 198. House Robber（打家劫舍）
# ────────────────────────────────────────────────────────────────

def house_robber(nums):
    """
    LC 198. House Robber
    不能搶相鄰的房子，求最大金額。

    狀態: dp[i] = 搶 0..i 的最大金額
    轉移方程: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
      （第 i 間: 不搶 → 拿 dp[i-1] / 搶 → 拿 dp[i-2] + nums[i]）
    Base case: dp[0] = nums[0], dp[1] = max(nums[0], nums[1])

    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr
    return prev1


def house_robber_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 198. House Robber（打家劫舍）")
    print("─" * 70)
    print("""
    不能搶相鄰的房子，求能搶到的最大金額。

    關鍵決策: 對每間房子，只有兩個選擇 → 搶 or 不搶
    轉移方程: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
                       不搶第i間    搶第i間

    ── 範例 1: nums = [1, 2, 3, 1] ────────────────
    dp[0] = nums[0] = 1
    dp[1] = max(nums[0], nums[1]) = max(1, 2) = 2
    dp[2] = max(dp[1], dp[0] + nums[2]) = max(2, 1+3) = 4    ← 搶 0,2
    dp[3] = max(dp[2], dp[1] + nums[3]) = max(4, 2+1) = 4    ← 不搶 3

    dp = [1, 2, 4, 4] → answer = 4  (搶第 0, 2 間: 1+3=4)

    ── 範例 2: nums = [2, 7, 9, 3, 1] ────────────
    dp[0] = 2
    dp[1] = max(2, 7) = 7
    dp[2] = max(7, 2+9)  = max(7, 11) = 11   ← 搶 0,2
    dp[3] = max(11, 7+3)  = max(11, 10) = 11  ← 不搶 3
    dp[4] = max(11, 11+1) = max(11, 12) = 12  ← 搶 2,4

    dp = [2, 7, 11, 11, 12] → answer = 12  (搶第 0, 2, 4 間: 2+9+1=12)

    ── 範例 3: nums = [5, 3, 4, 11, 2] ───────────
    dp[0] = 5
    dp[1] = max(5, 3) = 5
    dp[2] = max(5, 5+4)  = max(5, 9)  = 9    ← 搶 0,2
    dp[3] = max(9, 5+11)  = max(9, 16) = 16   ← 搶 1,3 (or 0,3)
    dp[4] = max(16, 9+2)  = max(16, 11) = 16  ← 不搶 4

    dp = [5, 5, 9, 16, 16] → answer = 16  (搶第 0, 3 間: 5+11=16)
    """)
    tests = [[1, 2, 3, 1], [2, 7, 9, 3, 1], [5, 3, 4, 11, 2]]
    for nums in tests:
        print(f"    house_robber({nums}) = {house_robber(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 213. House Robber II（打家劫舍 II - 環形）
# ────────────────────────────────────────────────────────────────

def house_robber_ii(nums):
    """
    LC 213. House Robber II
    房子排成一圈（首尾相鄰），不能搶相鄰的。

    關鍵洞見: 第一間和最後一間不能同時搶！
    → 分兩種情況取 max:
      Case A: 搶 nums[0..n-2]（不含最後一間）
      Case B: 搶 nums[1..n-1]（不含第一間）

    Time: O(n), Space: O(1)
    """
    if len(nums) == 1:
        return nums[0]

    def rob_linear(arr):
        if not arr:
            return 0
        if len(arr) == 1:
            return arr[0]
        prev2, prev1 = arr[0], max(arr[0], arr[1])
        for i in range(2, len(arr)):
            curr = max(prev1, prev2 + arr[i])
            prev2, prev1 = prev1, curr
        return prev1

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def house_robber_ii_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 213. House Robber II（環形打家劫舍）")
    print("─" * 70)
    print("""
    房子排成一圈！→ 第一間和最後一間相鄰，不能同時搶。

    技巧: 拆成兩個 House Robber I 問題，取 max
      Case A: nums[0 .. n-2]  (可能搶第一間，不搶最後一間)
      Case B: nums[1 .. n-1]  (不搶第一間，可能搶最後一間)

    ── 範例 1: nums = [2, 3, 2] ───────────────────
    Case A: [2, 3]   → dp: [2, 3]       → max = 3
    Case B: [3, 2]   → dp: [3, 3]       → max = 3
    answer = max(3, 3) = 3   (搶第 1 間)

    ── 範例 2: nums = [1, 2, 3, 1] ───────────────
    Case A: [1, 2, 3] → dp: [1, 2, 4]   → max = 4  (搶 0,2)
    Case B: [2, 3, 1] → dp: [2, 3, 3]   → max = 3  (搶 1)
    answer = max(4, 3) = 4

    ── 範例 3: nums = [1, 3, 1, 3, 100] ──────────
    Case A: [1, 3, 1, 3]   → dp: [1, 3, 3, 6]     → max = 6
    Case B: [3, 1, 3, 100] → dp: [3, 3, 6, 103]   → max = 103
    answer = max(6, 103) = 103  (搶第 1 間 + 第 4 間: 3+100)
    """)
    tests = [[2, 3, 2], [1, 2, 3, 1], [1, 3, 1, 3, 100]]
    for nums in tests:
        print(f"    house_robber_ii({nums}) = {house_robber_ii(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 91. Decode Ways（解碼方法）
# ────────────────────────────────────────────────────────────────

def decode_ways(s):
    """
    LC 91. Decode Ways
    'A'=1, 'B'=2, ..., 'Z'=26。給一串數字字串，問有幾種解碼方式。

    狀態: dp[i] = s[0..i-1] 的解碼方法數
    轉移方程:
      - 如果 s[i-1] != '0': dp[i] += dp[i-1]  (單獨解碼 s[i-1])
      - 如果 10 <= int(s[i-2:i]) <= 26: dp[i] += dp[i-2]  (兩位一起解碼)
    Base case: dp[0] = 1 (空字串有一種解法), dp[1] = 0 if s[0]=='0' else 1

    Time: O(n), Space: O(1)
    """
    if not s or s[0] == '0':
        return 0
    n = len(s)
    prev2, prev1 = 1, 1  # dp[0], dp[1]
    for i in range(2, n + 1):
        curr = 0
        if s[i - 1] != '0':
            curr += prev1
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr
    return prev1


def decode_ways_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 91. Decode Ways（解碼方法）")
    print("─" * 70)
    print("""
    A=1, B=2, ..., Z=26。數字字串有幾種解碼方式？

    轉移方程:
      dp[i] = 0
      if s[i-1] != '0':              dp[i] += dp[i-1]   ← 單獨解碼一位
      if 10 <= int(s[i-2:i]) <= 26:  dp[i] += dp[i-2]   ← 兩位一起解碼

    ── 範例 1: s = "12" ───────────────────────────
    dp[0] = 1  (base case)
    dp[1] = 1  (s[0]='1' != '0')
    dp[2]: s[1]='2' != '0' → dp[2] += dp[1] = 1
           s[0:2]="12", 10<=12<=26 → dp[2] += dp[0] = 1+1 = 2

    dp = [1, 1, 2] → answer = 2
    解碼方式: "1,2" → "AB" 或 "12" → "L"

    ── 範例 2: s = "226" ──────────────────────────
    dp[0] = 1, dp[1] = 1
    dp[2]: s[1]='2' != '0' → dp[2] += dp[1] = 1
           s[0:2]="22", 10<=22<=26 → dp[2] += dp[0] = 1+1 = 2
    dp[3]: s[2]='6' != '0' → dp[3] += dp[2] = 2
           s[1:3]="26", 10<=26<=26 → dp[3] += dp[1] = 2+1 = 3

    dp = [1, 1, 2, 3] → answer = 3
    解碼方式: "2,2,6"→BBF, "22,6"→VF, "2,26"→BZ

    ── 範例 3: s = "106" ──────────────────────────
    dp[0] = 1, dp[1] = 1
    dp[2]: s[1]='0' == '0' → 不加 dp[1]（'0' 不能單獨解碼）
           s[0:2]="10", 10<=10<=26 → dp[2] += dp[0] = 1
    dp[3]: s[2]='6' != '0' → dp[3] += dp[2] = 1
           s[1:3]="06", 06 < 10 → 不加

    dp = [1, 1, 1, 1] → answer = 1
    唯一解碼方式: "10,6" → JF
    """)
    tests = ["12", "226", "106"]
    for s in tests:
        print(f"    decode_ways(\"{s}\") = {decode_ways(s)}")


# ============================================================================
# Section 3: 子序列 DP (Subsequence DP)
# ============================================================================

# ────────────────────────────────────────────────────────────────
# LC 300. Longest Increasing Subsequence (LIS)
# ────────────────────────────────────────────────────────────────

def longest_increasing_subsequence(nums):
    """
    LC 300. Longest Increasing Subsequence
    找最長嚴格遞增子序列的長度。

    方法 1: DP — O(n^2)
    狀態: dp[i] = 以 nums[i] 結尾的 LIS 長度
    轉移方程: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]
    Base case: dp[i] = 1 (每個元素自己就是長度 1 的 LIS)
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def lis_binary_search(nums):
    """
    LC 300. LIS — Binary Search 解法 O(n log n)

    維護一個 tails 陣列: tails[i] = 長度為 i+1 的遞增子序列的最小末尾元素
    對每個數，用 binary search 找它在 tails 中的位置：
    - 如果比 tails 所有元素都大 → append（LIS 變長）
    - 否則 → 替換掉第一個 >= 它的位置（讓末尾更小，有更多成長空間）
    """
    import bisect
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


def lis_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "=" * 70)
    print("Section 3: 子序列 DP (Subsequence DP)")
    print("=" * 70)
    print("\n" + "─" * 70)
    print("LC 300. Longest Increasing Subsequence (LIS)")
    print("─" * 70)
    print("""
    找最長嚴格遞增子序列（不需要連續）的長度。

    O(n^2) DP:
    dp[i] = 以 nums[i] 結尾的 LIS 長度
    dp[i] = max(dp[j]+1) for j < i where nums[j] < nums[i]

    ── 範例 1: nums = [10, 9, 2, 5, 3, 7, 101, 18] ──
    i=0: nums[0]=10, dp[0] = 1
    i=1: nums[1]=9,  沒有 j 使 nums[j]<9, dp[1] = 1
    i=2: nums[2]=2,  沒有 j 使 nums[j]<2, dp[2] = 1
    i=3: nums[3]=5,  nums[2]=2<5 → dp[3]=dp[2]+1=2
    i=4: nums[4]=3,  nums[2]=2<3 → dp[4]=dp[2]+1=2
    i=5: nums[5]=7,  nums[2]=2<7→dp[2]+1=2, nums[3]=5<7→dp[3]+1=3,
                      nums[4]=3<7→dp[4]+1=3  → dp[5]=3
    i=6: nums[6]=101, 很多 j 滿足 → 最大是 dp[5]+1=4
    i=7: nums[7]=18,  nums[5]=7<18→dp[5]+1=4, ...  → dp[7]=4

    dp = [1, 1, 1, 2, 2, 3, 4, 4] → answer = 4
    LIS: [2, 5, 7, 101] 或 [2, 3, 7, 101] 或 [2, 3, 7, 18]

    O(n log n) Binary Search (tails 陣列):
    處理 10: tails = [10]
    處理 9:  9 < 10, 替換 → tails = [9]
    處理 2:  2 < 9, 替換  → tails = [2]
    處理 5:  5 > 2, append → tails = [2, 5]
    處理 3:  3 > 2 但 < 5, 替換 5 → tails = [2, 3]
    處理 7:  7 > 3, append → tails = [2, 3, 7]
    處理 101: 101 > 7, append → tails = [2, 3, 7, 101]
    處理 18:  18 > 7 但 < 101, 替換 → tails = [2, 3, 7, 18]
    len(tails) = 4 → answer = 4

    ── 範例 2: nums = [0, 1, 0, 3, 2, 3] ─────────
    dp: i=0→1, i=1→2(0<1), i=2→1, i=3→3(0<1<3),
        i=4→3(0<1, then 0<2→max(2,dp[1]+1)=3), i=5→4(0<1<2<3)
    dp = [1, 2, 1, 3, 3, 4] → answer = 4
    LIS: [0, 1, 2, 3]

    ── 範例 3: nums = [7, 7, 7, 7] ───────────────
    嚴格遞增 → 7 不小於 7，全部都是 1
    dp = [1, 1, 1, 1] → answer = 1
    """)
    tests = [[10, 9, 2, 5, 3, 7, 101, 18], [0, 1, 0, 3, 2, 3], [7, 7, 7, 7]]
    for nums in tests:
        r1 = longest_increasing_subsequence(nums)
        r2 = lis_binary_search(nums)
        print(f"    LIS({nums})")
        print(f"      O(n^2) = {r1}, O(nlogn) = {r2}")


# ────────────────────────────────────────────────────────────────
# LC 53. Maximum Subarray (Kadane's Algorithm)
# ────────────────────────────────────────────────────────────────

def max_subarray(nums):
    """
    LC 53. Maximum Subarray
    找連續子陣列的最大和。

    Kadane's Algorithm:
    狀態: current_sum = 以當前元素結尾的最大子陣列和
    轉移方程: current_sum = max(nums[i], current_sum + nums[i])
      （選擇: 從 nums[i] 重新開始 / 把 nums[i] 接到前面的子陣列後面）

    Time: O(n), Space: O(1)
    """
    current_sum = max_sum = nums[0]
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    return max_sum


def max_subarray_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 53. Maximum Subarray — Kadane's Algorithm")
    print("─" * 70)
    print("""
    找連續子陣列的最大和。

    轉移方程: current_sum = max(nums[i], current_sum + nums[i])
    直覺: 對每個位置，決定「接著前面的子陣列」還是「重新開始」

    ── 範例 1: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] ──

    i=0: num=-2, cur=max(-2, -2)=-2,           best=-2
    i=1: num= 1, cur=max(1, -2+1)=max(1,-1)=1, best=1   ← 重新開始
    i=2: num=-3, cur=max(-3, 1-3)=max(-3,-2)=-2, best=1
    i=3: num= 4, cur=max(4, -2+4)=max(4, 2)=4, best=4   ← 重新開始
    i=4: num=-1, cur=max(-1, 4-1)=max(-1,3)=3,  best=4
    i=5: num= 2, cur=max(2, 3+2)=max(2, 5)=5,  best=5
    i=6: num= 1, cur=max(1, 5+1)=max(1, 6)=6,  best=6   ← 最大!
    i=7: num=-5, cur=max(-5, 6-5)=max(-5,1)=1,  best=6
    i=8: num= 4, cur=max(4, 1+4)=max(4, 5)=5,  best=6

    answer = 6, 子陣列 = [4, -1, 2, 1]

    ── 範例 2: nums = [5, 4, -1, 7, 8] ───────────
    i=0: cur=5,  best=5
    i=1: cur=max(4, 5+4)=9,   best=9
    i=2: cur=max(-1, 9-1)=8,  best=9
    i=3: cur=max(7, 8+7)=15,  best=15
    i=4: cur=max(8, 15+8)=23, best=23

    answer = 23, 子陣列 = [5, 4, -1, 7, 8] (全部)

    ── 範例 3: nums = [-3, -2, -1, -4] ───────────
    i=0: cur=-3, best=-3
    i=1: cur=max(-2, -3-2)=max(-2,-5)=-2, best=-2  ← 重新開始
    i=2: cur=max(-1, -2-1)=max(-1,-3)=-1, best=-1  ← 重新開始
    i=3: cur=max(-4, -1-4)=max(-4,-5)=-4, best=-1

    answer = -1  (全是負數時，選最大的那個)
    """)
    tests = [[-2, 1, -3, 4, -1, 2, 1, -5, 4], [5, 4, -1, 7, 8], [-3, -2, -1, -4]]
    for nums in tests:
        print(f"    max_subarray({nums}) = {max_subarray(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 152. Maximum Product Subarray
# ────────────────────────────────────────────────────────────────

def max_product_subarray(nums):
    """
    LC 152. Maximum Product Subarray
    找連續子陣列的最大乘積。

    關鍵: 負數 * 負數 = 正數！所以要同時追蹤最大值和最小值。
    轉移方程:
      cur_max = max(nums[i], cur_max * nums[i], cur_min * nums[i])
      cur_min = min(nums[i], cur_max * nums[i], cur_min * nums[i])

    Time: O(n), Space: O(1)
    """
    cur_max = cur_min = result = nums[0]
    for i in range(1, len(nums)):
        # 注意: 要用暫存，因為 cur_max 會在計算 cur_min 時被覆蓋
        candidates = (nums[i], cur_max * nums[i], cur_min * nums[i])
        cur_max = max(candidates)
        cur_min = min(candidates)
        result = max(result, cur_max)
    return result


def max_product_subarray_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 152. Maximum Product Subarray（最大乘積子陣列）")
    print("─" * 70)
    print("""
    找連續子陣列的最大乘積。
    陷阱: 負 * 負 = 正！必須同時追蹤 cur_max 和 cur_min。

    ── 範例 1: nums = [2, 3, -2, 4] ──────────────
    i=0: cur_max=2,  cur_min=2,  result=2
    i=1: candidates=(3, 2*3=6, 2*3=6)
         cur_max=6, cur_min=3, result=6
    i=2: candidates=(-2, 6*-2=-12, 3*-2=-6)
         cur_max=-2, cur_min=-12, result=6
    i=3: candidates=(4, -2*4=-8, -12*4=-48)
         cur_max=4, cur_min=-48, result=6

    answer = 6, 子陣列 = [2, 3]

    ── 範例 2: nums = [-2, 0, -1] ─────────────────
    i=0: cur_max=-2, cur_min=-2, result=-2
    i=1: candidates=(0, -2*0=0, -2*0=0)
         cur_max=0, cur_min=0, result=0
    i=2: candidates=(-1, 0*-1=0, 0*-1=0)
         cur_max=0, cur_min=-1, result=0

    answer = 0

    ── 範例 3: nums = [-2, 3, -4] ─────────────────
    i=0: cur_max=-2, cur_min=-2, result=-2
    i=1: candidates=(3, -2*3=-6, -2*3=-6)
         cur_max=3, cur_min=-6, result=3
    i=2: candidates=(-4, 3*-4=-12, -6*-4=24)
         cur_max=24, cur_min=-12, result=24     ← 負*負=正!

    answer = 24, 子陣列 = [-2, 3, -4]（全部相乘）
    """)
    tests = [[2, 3, -2, 4], [-2, 0, -1], [-2, 3, -4]]
    for nums in tests:
        print(f"    max_product_subarray({nums}) = {max_product_subarray(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 139. Word Break
# ────────────────────────────────────────────────────────────────

def word_break(s, wordDict):
    """
    LC 139. Word Break
    判斷字串 s 能否被拆成 wordDict 中的單字。

    狀態: dp[i] = s[0:i] 能否被拆成字典中的單字
    轉移方程: dp[i] = True if any(dp[j] and s[j:i] in wordSet) for j in 0..i-1
    Base case: dp[0] = True (空字串可以)

    Time: O(n^2 * m), Space: O(n)   (m = 平均單字長度, for substring comparison)
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]


def word_break_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 139. Word Break")
    print("─" * 70)
    print("""
    字串 s 能否用 wordDict 中的單字拼出來（單字可重複使用）？

    dp[i] = s[0:i] 能否被拆成字典單字
    dp[i] = True if 存在某個 j，使得 dp[j]=True 且 s[j:i] 在字典中

    ── 範例 1: s = "leetcode", wordDict = ["leet", "code"] ──
    dp[0] = True (base case)
    dp[1]: s[0:1]="l" not in dict → False
    dp[2]: s[0:2]="le" not in dict → False
    dp[3]: s[0:3]="lee" not in dict → False
    dp[4]: s[0:4]="leet" in dict, dp[0]=True → True!
    dp[5]: ... "eetc","etco" 都不在 → False
    dp[6]: ... False
    dp[7]: ... False
    dp[8]: s[4:8]="code" in dict, dp[4]=True → True!

    dp = [T, F, F, F, T, F, F, F, T] → answer = True
    拆法: "leet" + "code"

    ── 範例 2: s = "applepenapple", wordDict = ["apple","pen"] ──
    dp[0] = True
    dp[5]:  s[0:5]="apple" in dict, dp[0]=T → True
    dp[8]:  s[5:8]="pen" in dict, dp[5]=T → True
    dp[13]: s[8:13]="apple" in dict, dp[8]=T → True

    answer = True, 拆法: "apple" + "pen" + "apple"

    ── 範例 3: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"] ──
    dp[0] = True
    dp[3]:  s[0:3]="cat" in dict → True
    dp[4]:  s[0:4]="cats" in dict → True
    dp[7]:  s[3:7]="sand" in dict, dp[3]=T → True
            s[4:7]="and" in dict, dp[4]=T → True (也行)
    dp[9]:  需要 s[?:9] 在字典中且 dp[?]=T
            s[7:9]="og" not in dict
            s[6:9]="dog" in dict, 但 dp[6]?
            dp[6]: s[3:6]="san" not in, s[4:6]="an" not in → False
            所以 dp[9] = False

    answer = False  ("andog" 拆不出來)
    """)
    tests = [
        ("leetcode", ["leet", "code"]),
        ("applepenapple", ["apple", "pen"]),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"]),
    ]
    for s, wd in tests:
        print(f"    word_break(\"{s}\", {wd}) = {word_break(s, wd)}")


# ============================================================================
# Section 4: 買賣股票系列 (Stock Problems)
# ============================================================================

# ────────────────────────────────────────────────────────────────
# LC 121. Best Time to Buy and Sell Stock
# ────────────────────────────────────────────────────────────────

def max_profit_i(prices):
    """
    LC 121. Best Time to Buy and Sell Stock
    只能買賣一次，求最大利潤。

    追蹤到目前為止的最低價格 min_price，
    每天算「今天賣」的利潤 = prices[i] - min_price。

    Time: O(n), Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit


def max_profit_i_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "=" * 70)
    print("Section 4: 買賣股票系列 (Stock Problems)")
    print("=" * 70)
    print("\n" + "─" * 70)
    print("LC 121. Best Time to Buy and Sell Stock（只能買賣一次）")
    print("─" * 70)
    print("""
    只能買一次 + 賣一次，求最大利潤。

    策略: 遍歷時記住「到目前為止最低價」，每天算利潤。

    ── 範例 1: prices = [7, 1, 5, 3, 6, 4] ───────
    day 0: price=7, min=7,  profit=7-7=0, best=0
    day 1: price=1, min=1,  profit=1-1=0, best=0   ← 新最低價
    day 2: price=5, min=1,  profit=5-1=4, best=4
    day 3: price=3, min=1,  profit=3-1=2, best=4
    day 4: price=6, min=1,  profit=6-1=5, best=5   ← 最大利潤!
    day 5: price=4, min=1,  profit=4-1=3, best=5

    answer = 5  (day 1 買, day 4 賣: 6-1=5)

    ── 範例 2: prices = [7, 6, 4, 3, 1] ──────────
    價格一路下跌，無法獲利
    day 0: min=7, best=0
    day 1: min=6, profit=0, best=0
    day 2: min=4, profit=0, best=0
    day 3: min=3, profit=0, best=0
    day 4: min=1, profit=0, best=0

    answer = 0  (不要買)

    ── 範例 3: prices = [2, 4, 1, 7] ─────────────
    day 0: min=2, profit=0, best=0
    day 1: min=2, profit=4-2=2, best=2
    day 2: min=1, profit=0, best=2      ← 新最低價
    day 3: min=1, profit=7-1=6, best=6  ← 最大!

    answer = 6  (day 2 買, day 3 賣: 7-1=6)
    """)
    tests = [[7, 1, 5, 3, 6, 4], [7, 6, 4, 3, 1], [2, 4, 1, 7]]
    for prices in tests:
        print(f"    max_profit_i({prices}) = {max_profit_i(prices)}")


# ────────────────────────────────────────────────────────────────
# LC 122. Best Time to Buy and Sell Stock II
# ────────────────────────────────────────────────────────────────

def max_profit_ii(prices):
    """
    LC 122. Best Time to Buy and Sell Stock II
    可以買賣無限次（但同時最多持有一股），求最大利潤。

    貪心: 只要明天比今天貴，就今天買明天賣！
    等價於: 收集所有「上漲段」的利潤。

    Time: O(n), Space: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


def max_profit_ii_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 122. Best Time to Buy and Sell Stock II（無限次交易）")
    print("─" * 70)
    print("""
    可以買賣無限次，求最大總利潤。

    貪心策略: 所有「上漲日」的漲幅加起來就是答案！
    （等於每次 prices[i] > prices[i-1] 就賺 prices[i] - prices[i-1]）

    ── 範例 1: prices = [7, 1, 5, 3, 6, 4] ───────
    day 0→1: 1-7 = -6  (下跌，不交易)
    day 1→2: 5-1 = +4  (上漲，賺!)     profit = 4
    day 2→3: 3-5 = -2  (下跌，不交易)
    day 3→4: 6-3 = +3  (上漲，賺!)     profit = 4+3 = 7
    day 4→5: 4-6 = -2  (下跌，不交易)

    answer = 7  (day 1 買 day 2 賣 +4, day 3 買 day 4 賣 +3)

    ── 範例 2: prices = [1, 2, 3, 4, 5] ──────────
    day 0→1: +1, day 1→2: +1, day 2→3: +1, day 3→4: +1
    每天都漲 → profit = 1+1+1+1 = 4
    (等同 day 0 買 day 4 賣: 5-1=4)

    answer = 4

    ── 範例 3: prices = [7, 6, 4, 3, 1] ──────────
    每天都跌 → 沒有任何上漲段
    answer = 0
    """)
    tests = [[7, 1, 5, 3, 6, 4], [1, 2, 3, 4, 5], [7, 6, 4, 3, 1]]
    for prices in tests:
        print(f"    max_profit_ii({prices}) = {max_profit_ii(prices)}")


# ────────────────────────────────────────────────────────────────
# LC 309. Best Time to Buy and Sell Stock with Cooldown
# ────────────────────────────────────────────────────────────────

def max_profit_cooldown(prices):
    """
    LC 309. Best Time with Cooldown
    可以買賣無限次，但賣出後要冷卻一天才能再買。

    State Machine (狀態機):
    三個狀態:
      hold:    持有股票 (之前某天買了，還沒賣)
      sold:    剛剛賣出 (明天要冷卻)
      rest:    冷卻/空手 (沒有股票，可以買)

    轉移:
      hold[i] = max(hold[i-1], rest[i-1] - prices[i])  持有 or 今天買
      sold[i] = hold[i-1] + prices[i]                    今天賣
      rest[i] = max(rest[i-1], sold[i-1])                空手 or 冷卻完

    Time: O(n), Space: O(1)
    """
    if len(prices) <= 1:
        return 0
    hold = -prices[0]  # 第一天買
    sold = 0
    rest = 0
    for i in range(1, len(prices)):
        prev_hold = hold
        hold = max(hold, rest - prices[i])
        rest = max(rest, sold)
        sold = prev_hold + prices[i]
    return max(sold, rest)


def max_profit_cooldown_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 309. Best Time with Cooldown（含冷卻期）")
    print("─" * 70)
    print("""
    賣出後必須冷卻一天才能再買。用狀態機來思考！

    三個狀態:
    ┌──────┐  買入   ┌──────┐  賣出   ┌──────┐
    │ rest │ ──────► │ hold │ ──────► │ sold │
    │ 空手  │ ◄────── │ 持有  │        │ 剛賣  │
    └──┬───┘  不買    └──┬───┘        └──┬───┘
       │                 │                │
       └── 維持空手 ──────┘── 繼續持有     └── 冷卻 → rest

    ── 範例 1: prices = [1, 2, 3, 0, 2] ──────────
    初始: hold=-1, sold=0, rest=0

    day 1 (price=2):
      hold = max(-1, 0-2) = max(-1, -2) = -1    (繼續持有)
      rest = max(0, 0) = 0
      sold = -1+2 = 1                             (今天賣)

    day 2 (price=3):
      hold = max(-1, 0-3) = max(-1, -3) = -1    (繼續持有)
      rest = max(0, 1) = 1                        (冷卻完)
      sold = -1+3 = 2                             (今天賣)

    day 3 (price=0):
      hold = max(-1, 1-0) = max(-1, 1) = 1       (冷卻完後買!)
      rest = max(1, 2) = 2
      sold = -1+0 = -1                            (虧損，不好)

    day 4 (price=2):
      hold = max(1, 2-2) = max(1, 0) = 1         (繼續持有)
      rest = max(2, -1) = 2
      sold = 1+2 = 3                              (賣出獲利!)

    answer = max(sold=3, rest=2) = 3
    操作: day 0 買(1), day 2 賣(3), day 3 冷卻, day 3 買(0), day 4 賣(2)
    利潤: (3-1) + (2-0) = 2 + 2 = ...wait, 但 cooldown!
    正確: day 0 買, day 1 賣(+1), cooldown day 2, day 3 買, day 4 賣(+2) = 3

    ── 範例 2: prices = [1, 2, 4] ─────────────────
    初始: hold=-1, sold=0, rest=0
    day 1: hold=max(-1,0-2)=-1, rest=max(0,0)=0, sold=-1+2=1
    day 2: hold=max(-1,0-4)=-1, rest=max(0,1)=1, sold=-1+4=3

    answer = max(3, 1) = 3  (day 0 買, day 2 賣: 4-1=3)

    ── 範例 3: prices = [2, 1] ────────────────────
    初始: hold=-2, sold=0, rest=0
    day 1: hold=max(-2,0-1)=-1, rest=max(0,0)=0, sold=-2+1=-1

    answer = max(-1, 0) = 0  (不交易)
    """)
    tests = [[1, 2, 3, 0, 2], [1, 2, 4], [2, 1]]
    for prices in tests:
        print(f"    max_profit_cooldown({prices}) = {max_profit_cooldown(prices)}")


# ============================================================================
# Section 5: 跳躍型 DP (Jump Problems)
# ============================================================================

# ────────────────────────────────────────────────────────────────
# LC 55. Jump Game
# ────────────────────────────────────────────────────────────────

def can_jump(nums):
    """
    LC 55. Jump Game
    nums[i] = 從位置 i 最多可以跳幾步，判斷能否到達最後一個位置。

    Greedy: 維護「目前能到達的最遠位置」max_reach。
    如果 max_reach >= n-1，就能到終點。

    Time: O(n), Space: O(1)
    """
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True


def can_jump_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "=" * 70)
    print("Section 5: 跳躍型 DP (Jump Problems)")
    print("=" * 70)
    print("\n" + "─" * 70)
    print("LC 55. Jump Game")
    print("─" * 70)
    print("""
    nums[i] = 從位置 i 最多能跳幾步，能否到達最後？

    Greedy: 維護 max_reach（能到的最遠位置）
    如果某個 i > max_reach，代表走不到 i，return False

    ── 範例 1: nums = [2, 3, 1, 1, 4] ────────────
    i=0: 0 <= max_reach=0, max_reach = max(0, 0+2) = 2
    i=1: 1 <= 2, max_reach = max(2, 1+3) = 4
    i=2: 2 <= 4, max_reach = max(4, 2+1) = 4
    i=3: 3 <= 4, max_reach = max(4, 3+1) = 4
    i=4: 4 <= 4, max_reach = max(4, 4+4) = 8

    max_reach = 8 >= 4 → True

    ── 範例 2: nums = [3, 2, 1, 0, 4] ────────────
    i=0: max_reach = max(0, 0+3) = 3
    i=1: max_reach = max(3, 1+2) = 3
    i=2: max_reach = max(3, 2+1) = 3
    i=3: max_reach = max(3, 3+0) = 3    ← 卡住! 跳不過 0
    i=4: 4 > max_reach=3 → False!

    answer = False  (被 index 3 的 0 擋住了)

    ── 範例 3: nums = [1, 1, 1, 1, 1] ────────────
    每步跳 1，剛好能到:
    i=0: mr=1, i=1: mr=2, i=2: mr=3, i=3: mr=4, i=4: mr=5

    answer = True
    """)
    tests = [[2, 3, 1, 1, 4], [3, 2, 1, 0, 4], [1, 1, 1, 1, 1]]
    for nums in tests:
        print(f"    can_jump({nums}) = {can_jump(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 45. Jump Game II
# ────────────────────────────────────────────────────────────────

def jump_game_ii(nums):
    """
    LC 45. Jump Game II
    保證能到終點，求最少跳幾次。

    Greedy (BFS-like):
    把每次跳躍看成 BFS 的一層。
    - current_end: 當前這一跳能到的最遠邊界
    - farthest: 在這一跳的範圍內，下一跳能到的最遠位置

    Time: O(n), Space: O(1)
    """
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(len(nums) - 1):  # 不需要檢查最後一個
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps


def jump_game_ii_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 45. Jump Game II（最少跳幾次）")
    print("─" * 70)
    print("""
    保證能到終點，求最少跳幾次。

    策略: 類似 BFS 的層次遍歷
    current_end = 這一跳能到的最遠邊界
    farthest    = 在這一跳範圍內能到的最遠位置

    ── 範例 1: nums = [2, 3, 1, 1, 4] ────────────

    初始: jumps=0, current_end=0, farthest=0

    i=0: farthest = max(0, 0+2) = 2
         i == current_end(0) → jumps=1, current_end=2
         (第 1 跳: 可以到 index 0~2)

    i=1: farthest = max(2, 1+3) = 4
    i=2: farthest = max(4, 2+1) = 4
         i == current_end(2) → jumps=2, current_end=4
         (第 2 跳: 從 index 1 或 2 跳，最遠到 4)

    已到達終點! answer = 2
    路徑: index 0 → index 1 → index 4

    ── 範例 2: nums = [2, 3, 0, 1, 4] ────────────
    i=0: far=max(0,2)=2, i==end(0)→jumps=1, end=2
    i=1: far=max(2,4)=4
    i=2: far=max(4,2)=4, i==end(2)→jumps=2, end=4

    answer = 2 (0→1→4)

    ── 範例 3: nums = [1, 2, 1, 1, 1] ────────────
    i=0: far=1, i==end(0)→jumps=1, end=1
    i=1: far=max(1,3)=3, i==end(1)→jumps=2, end=3
    i=2: far=max(3,3)=3
    i=3: far=max(3,4)=4, i==end(3)→jumps=3, end=4

    answer = 3 (0→1→3→4 或 0→1→2→4)
    """)
    tests = [[2, 3, 1, 1, 4], [2, 3, 0, 1, 4], [1, 2, 1, 1, 1]]
    for nums in tests:
        print(f"    jump_game_ii({nums}) = {jump_game_ii(nums)}")


# ────────────────────────────────────────────────────────────────
# LC 322. Coin Change
# ────────────────────────────────────────────────────────────────

def coin_change(coins, amount):
    """
    LC 322. Coin Change
    用最少的硬幣湊出 amount，不能湊出回傳 -1。

    狀態: dp[i] = 湊出金額 i 的最少硬幣數
    轉移方程: dp[i] = min(dp[i - coin] + 1) for each coin in coins
    Base case: dp[0] = 0

    Time: O(amount * len(coins)), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_demo(verbose=True):
    if not verbose:
        return
    print("\n" + "─" * 70)
    print("LC 322. Coin Change（零錢兌換）")
    print("─" * 70)
    print("""
    用最少的硬幣湊出 amount。

    dp[i] = 湊出金額 i 的最少硬幣數
    dp[i] = min(dp[i - coin] + 1) for each coin

    這是「完全背包」問題的變形（每種硬幣可以無限使用）

    ── 範例 1: coins = [1, 2, 5], amount = 11 ────

    dp[0]  = 0
    dp[1]  = dp[0]+1 = 1                    (1)
    dp[2]  = min(dp[1]+1, dp[0]+1) = 1      (2)
    dp[3]  = min(dp[2]+1, dp[1]+1) = 2      (2+1)
    dp[4]  = min(dp[3]+1, dp[2]+1) = 2      (2+2)
    dp[5]  = min(dp[4]+1, dp[3]+1, dp[0]+1) = 1  (5)
    dp[6]  = min(dp[5]+1, dp[4]+1, dp[1]+1) = 2  (5+1)
    dp[7]  = min(dp[6]+1, dp[5]+1, dp[2]+1) = 2  (5+2)
    dp[8]  = min(dp[7]+1, dp[6]+1, dp[3]+1) = 3  (5+2+1)
    dp[9]  = min(dp[8]+1, dp[7]+1, dp[4]+1) = 3  (5+2+2)
    dp[10] = min(dp[9]+1, dp[8]+1, dp[5]+1) = 2  (5+5)
    dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = 3 (5+5+1)

    answer = 3  (5 + 5 + 1)

    ── 範例 2: coins = [2], amount = 3 ────────────
    dp[0] = 0
    dp[1] = inf  (2 > 1, 湊不出)
    dp[2] = dp[0]+1 = 1
    dp[3] = dp[1]+1 = inf  (湊不出!)

    answer = -1

    ── 範例 3: coins = [1, 3, 4], amount = 6 ─────
    dp[0] = 0
    dp[1] = dp[0]+1 = 1            (1)
    dp[2] = dp[1]+1 = 2            (1+1)
    dp[3] = min(dp[2]+1, dp[0]+1) = 1  (3)
    dp[4] = min(dp[3]+1, dp[1]+1, dp[0]+1) = 1  (4)
    dp[5] = min(dp[4]+1, dp[2]+1, dp[1]+1) = 2  (4+1 or 3+1+1)
    dp[6] = min(dp[5]+1, dp[3]+1, dp[2]+1) = 2  (3+3)

    answer = 2  (3 + 3)
    注意: 不是 4+1+1=3 枚! Greedy (先拿最大) 在這裡會錯!
    """)
    tests = [([1, 2, 5], 11), ([2], 3), ([1, 3, 4], 6)]
    for coins, amount in tests:
        print(f"    coin_change({coins}, {amount}) = {coin_change(coins, amount)}")


# ============================================================================
# Section 6: DP 思考框架 (How to Think in DP)
# ============================================================================

def dp_thinking_framework(verbose=True):
    if not verbose:
        return
    print("\n" + "=" * 70)
    print("Section 6: DP 思考框架 (How to Think in DP)")
    print("=" * 70)
    print("""
    ── Step 1: 如何辨識 DP 問題 ──────────────────

    看到這些關鍵字，想到 DP:
    ┌─────────────────────────────────────────────────┐
    │ "最少/最多/最大/最小" (optimization)              │
    │ "有幾種方法/方式" (counting)                      │
    │ "能不能/是否可以" (feasibility)                   │
    │ "在...的限制下" (constraint)                      │
    │                                                  │
    │ 常見模式:                                        │
    │ - 序列從左到右做決策 → 線性 DP                    │
    │ - 子字串/子序列 → 子序列 DP                       │
    │ - 容量/背包限制 → 背包 DP                        │
    │ - 網格/矩陣移動 → 二維 DP                        │
    └─────────────────────────────────────────────────┘

    ── Step 2: 如何定義 State（狀態）─────────────

    問自己: 「要完整描述到目前為止的情況，需要什麼資訊？」

    ┌────────────────┬─────────────────────────────────┐
    │ 問題類型        │ 狀態定義                         │
    ├────────────────┼─────────────────────────────────┤
    │ Climbing Stairs │ dp[i] = 到第 i 階的方法數        │
    │ House Robber    │ dp[i] = 搶 0..i 的最大金額       │
    │ Coin Change     │ dp[i] = 湊出金額 i 的最少硬幣   │
    │ LIS             │ dp[i] = 以 nums[i] 結尾的 LIS  │
    │ Word Break      │ dp[i] = s[0:i] 能否被拆成字典字  │
    │ Stock+Cooldown  │ hold/sold/rest 三個狀態          │
    └────────────────┴─────────────────────────────────┘

    ── Step 3: 如何寫 Transition（轉移方程）──────

    問自己: 「到達當前狀態的最後一步是什麼？」

    例: House Robber
    到達 dp[i] 的最後一步:
      - 不搶第 i 間 → 答案跟 dp[i-1] 一樣
      - 搶第 i 間   → dp[i-2] + nums[i]（跳過 i-1）
    → dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    例: Coin Change
    到達 dp[amount] 的最後一步:
      - 放一枚 coin_k → dp[amount - coin_k] + 1
    → dp[i] = min(dp[i - coin] + 1) for each coin

    ── Step 4: 如何優化空間 ──────────────────────

    觀察 dp[i] 依賴哪些之前的值:
    ┌────────────────────┬────────────────────────────┐
    │ 依賴                │ 優化方式                    │
    ├────────────────────┼────────────────────────────┤
    │ dp[i-1], dp[i-2]   │ 用 2 個變數 prev1, prev2   │
    │ dp[i-1] 那整列      │ 用 1 個一維陣列不斷覆寫     │
    │ dp[i-1] + dp[i-2]列│ 用 2 個一維陣列交替使用      │
    └────────────────────┴────────────────────────────┘

    ── DP 解題模板 ───────────────────────────────

    def solve_dp(input):
        # 1. 定義 dp 陣列 + base case
        dp = [base_value] * size
        dp[0] = ...  # base case

        # 2. 按照計算順序填表
        for i in range(start, end):
            for choice in all_choices:
                dp[i] = transition(dp[previous_states], choice)

        # 3. 回傳答案
        return dp[target]

    ── 本檔案的題目總覽 ──────────────────────────

    ┌───────────────────────────┬──────────────┬────────────┐
    │ 題目                       │ 轉移方程概要   │ 複雜度      │
    ├───────────────────────────┼──────────────┼────────────┤
    │ Fibonacci                  │ dp[i-1]+dp[i-2]│ O(n)/O(1) │
    │ Climbing Stairs            │ 同 Fibonacci   │ O(n)/O(1) │
    │ House Robber               │ max(skip,rob)  │ O(n)/O(1) │
    │ House Robber II            │ 拆兩個 HR I    │ O(n)/O(1) │
    │ Decode Ways                │ 1位 or 2位解碼 │ O(n)/O(1) │
    │ LIS (DP)                   │ max(dp[j]+1)   │ O(n^2)/O(n)│
    │ LIS (Binary Search)        │ tails 陣列     │O(nlogn)/O(n)│
    │ Maximum Subarray           │ max(num,cur+num)│ O(n)/O(1) │
    │ Max Product Subarray        │ track max+min │ O(n)/O(1) │
    │ Word Break                 │ dp[j] & substr │ O(n^2)/O(n)│
    │ Stock I                    │ min_price track│ O(n)/O(1) │
    │ Stock II                   │ 收集上漲段     │ O(n)/O(1) │
    │ Stock w/ Cooldown          │ 3-state machine│ O(n)/O(1) │
    │ Jump Game                  │ greedy reach   │ O(n)/O(1) │
    │ Jump Game II               │ BFS-like jumps │ O(n)/O(1) │
    │ Coin Change                │ min(dp[i-c]+1) │O(n*k)/O(n)│
    └───────────────────────────┴──────────────┴────────────┘

    面試建議:
    1. 先想暴力解（遞迴），確認有重疊子問題
    2. 加 memo → top-down
    3. 改成 bottom-up → 可以進一步優化空間
    4. 跟面試官確認：要不要優化空間？
    """)


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70)
    print(" LeetCode 12: Dynamic Programming 一維 (1D DP)")
    print(" 適用: Google / NVIDIA 面試準備")
    print("=" * 70)

    # Section 1: DP 核心概念
    dp_core_concepts(verbose=True)
    fibonacci_demo(verbose=True)

    # Section 2: 線性 DP
    climbing_stairs_demo(verbose=True)
    house_robber_demo(verbose=True)
    house_robber_ii_demo(verbose=True)
    decode_ways_demo(verbose=True)

    # Section 3: 子序列 DP
    lis_demo(verbose=True)
    max_subarray_demo(verbose=True)
    max_product_subarray_demo(verbose=True)
    word_break_demo(verbose=True)

    # Section 4: 買賣股票系列
    max_profit_i_demo(verbose=True)
    max_profit_ii_demo(verbose=True)
    max_profit_cooldown_demo(verbose=True)

    # Section 5: 跳躍型 DP
    can_jump_demo(verbose=True)
    jump_game_ii_demo(verbose=True)
    coin_change_demo(verbose=True)

    # Section 6: DP 思考框架
    dp_thinking_framework(verbose=True)

    # ── 驗證所有解法正確性 ──
    print("\n" + "=" * 70)
    print(" 驗證所有解法 (Verification)")
    print("=" * 70)

    all_pass = True

    # Fibonacci
    assert fibonacci_brute_force(10) == 55
    assert fibonacci_memo(10) == 55
    assert fibonacci_tabulation(10) == 55
    assert fibonacci_optimized(10) == 55
    print("  [PASS] Fibonacci")

    # Climbing Stairs
    assert climbing_stairs(3) == 3
    assert climbing_stairs(5) == 8
    print("  [PASS] Climbing Stairs")

    # House Robber
    assert house_robber([1, 2, 3, 1]) == 4
    assert house_robber([2, 7, 9, 3, 1]) == 12
    print("  [PASS] House Robber")

    # House Robber II
    assert house_robber_ii([2, 3, 2]) == 3
    assert house_robber_ii([1, 2, 3, 1]) == 4
    assert house_robber_ii([1, 3, 1, 3, 100]) == 103
    print("  [PASS] House Robber II")

    # Decode Ways
    assert decode_ways("12") == 2
    assert decode_ways("226") == 3
    assert decode_ways("106") == 1
    assert decode_ways("0") == 0
    print("  [PASS] Decode Ways")

    # LIS
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_binary_search([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence([7, 7, 7, 7]) == 1
    print("  [PASS] LIS (both O(n^2) and O(nlogn))")

    # Maximum Subarray
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([-3, -2, -1, -4]) == -1
    print("  [PASS] Maximum Subarray")

    # Maximum Product Subarray
    assert max_product_subarray([2, 3, -2, 4]) == 6
    assert max_product_subarray([-2, 0, -1]) == 0
    assert max_product_subarray([-2, 3, -4]) == 24
    print("  [PASS] Maximum Product Subarray")

    # Word Break
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print("  [PASS] Word Break")

    # Stock I
    assert max_profit_i([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit_i([7, 6, 4, 3, 1]) == 0
    print("  [PASS] Stock I")

    # Stock II
    assert max_profit_ii([7, 1, 5, 3, 6, 4]) == 7
    assert max_profit_ii([1, 2, 3, 4, 5]) == 4
    print("  [PASS] Stock II")

    # Stock with Cooldown
    assert max_profit_cooldown([1, 2, 3, 0, 2]) == 3
    print("  [PASS] Stock with Cooldown")

    # Jump Game
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    print("  [PASS] Jump Game")

    # Jump Game II
    assert jump_game_ii([2, 3, 1, 1, 4]) == 2
    assert jump_game_ii([2, 3, 0, 1, 4]) == 2
    print("  [PASS] Jump Game II")

    # Coin Change
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1, 3, 4], 6) == 2
    print("  [PASS] Coin Change")

    print("\n  All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
