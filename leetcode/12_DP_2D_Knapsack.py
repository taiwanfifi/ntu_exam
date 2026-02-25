"""
============================================================
  12. 二維 DP 與背包問題 (2D DP & Knapsack Patterns)
  LeetCode 教學：Google / NVIDIA 面試準備
============================================================

涵蓋主題 (Topics Covered):
  S1: 二維 DP 基礎 — Unique Paths, Obstacles, Min Path Sum
  S2: 字串型 2D DP — LCS, Edit Distance, Longest Palindromic Substring
  S3: 0/1 背包 — Classic Knapsack, Partition Equal Subset, Target Sum
  S4: 完全背包 — Coin Change, Coin Change 2, 迴圈順序差異
  S5: 區間 DP — Palindrome Partitioning II, Burst Balloons
  S6: 背包 vs 區間 DP 比較總整理

核心觀念：
  - 二維 DP 用 dp[i][j] 表格儲存子問題答案
  - 背包問題 = 「有限資源下的最佳選擇」
  - 每題都附 完整表格填充過程 + 3 組數值追蹤
"""

# ============================================================
# Section 1: 二維 DP 基礎 (2D DP Basics)
# ============================================================

def unique_paths(m: int, n: int, verbose=False) -> int:
    """
    LeetCode 62 - Unique Paths
    從左上走到右下，只能往右或往下，共幾條路？
    dp[i][j] = dp[i-1][j] + dp[i][j-1]  (上方 + 左方)
    Time: O(m*n) | Space: O(m*n)
    """
    dp = [[1]*n for _ in range(m)]  # 第一列/第一行都是 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    if verbose:
        print(f"\n=== Unique Paths ({m}x{n}) ===")
        for i in range(m):
            print("  " + "  ".join(f"{dp[i][j]:3d}" for j in range(n)))
        print(f"  答案 = {dp[m-1][n-1]}")
    return dp[m-1][n-1]


def unique_paths_with_obstacles(grid: list, verbose=False) -> int:
    """
    LeetCode 63 - Unique Paths II (有障礙物)
    obstacle=1 的格子 dp=0，其餘同 Unique Paths。
    """
    m, n = len(grid), len(grid[0])
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = 0 if grid[0][0] == 1 else 1
    for j in range(1, n):
        dp[0][j] = 0 if grid[0][j] == 1 else dp[0][j-1]
    for i in range(1, m):
        dp[i][0] = 0 if grid[i][0] == 1 else dp[i-1][0]
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    if verbose:
        print(f"\n=== Unique Paths II (with obstacles) ===")
        print("  Grid (1=obstacle):")
        for row in grid:
            print("    " + str(row))
        print("  DP table:")
        for i in range(m):
            print("    " + "  ".join(f"{dp[i][j]:3d}" for j in range(n)))
        print(f"  答案 = {dp[m-1][n-1]}")
    return dp[m-1][n-1]


def min_path_sum(grid: list, verbose=False) -> int:
    """
    LeetCode 64 - Minimum Path Sum
    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    """
    m, n = len(grid), len(grid[0])
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    if verbose:
        print(f"\n=== Minimum Path Sum ===")
        print("  Grid values:")
        for row in grid:
            print("    " + "  ".join(f"{v:3d}" for v in row))
        print("  DP table (cumulative min cost):")
        for i in range(m):
            print("    " + "  ".join(f"{dp[i][j]:3d}" for j in range(n)))
        print(f"  最小路徑和 = {dp[m-1][n-1]}")
    return dp[m-1][n-1]


# ============================================================
# Section 2: 字串型 2D DP (String DP)
# ============================================================

def longest_common_subsequence(text1: str, text2: str, verbose=False) -> int:
    """
    LeetCode 1143 - Longest Common Subsequence (LCS)
    dp[i][j] = LCS of text1[:i] and text2[:j]
      若 text1[i-1]==text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
      否則: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    Time: O(m*n) | Space: O(m*n)

    範例追蹤 text1="abcde", text2="ace":
          ""  a  c  e
      ""   0  0  0  0
      a    0  1  1  1   ← 'a'=='a' → dp[0][0]+1=1
      b    0  1  1  1   ← 'b'!='a' → max(1,0)=1
      c    0  1  2  2   ← 'c'=='c' → dp[1][1]+1=2
      d    0  1  2  2
      e    0  1  2  3   ← 'e'=='e' → dp[3][2]+1=3
    """
    m, n = len(text1), len(text2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    if verbose:
        print(f"\n=== LCS: \"{text1}\" vs \"{text2}\" ===")
        header = '     ""  ' + "  ".join(f"{c:>2}" for c in text2)
        print(header)
        for i in range(m+1):
            label = f'  "{text1[i-1]}"' if i > 0 else '   ""'
            row = "  ".join(f"{dp[i][j]:2d}" for j in range(n+1))
            reason = ""
            if i > 0:
                for j in range(1, n+1):
                    if text1[i-1] == text2[j-1]:
                        reason = (f"  ← dp[{i}][{j}]: '{text1[i-1]}'=="
                                  f"'{text2[j-1]}' → dp[{i-1}][{j-1}]+1={dp[i][j]}")
                        break
            print(f"  {label}  {row}{reason}")
        print(f"  LCS 長度 = {dp[m][n]}")
    return dp[m][n]


def edit_distance(word1: str, word2: str, verbose=False) -> int:
    """
    LeetCode 72 - Edit Distance (Google 經典題!)
    dp[i][j] = min operations to convert word1[:i] → word2[:j]
      相同字元: dp[i][j] = dp[i-1][j-1]        (不動)
      不同字元: dp[i][j] = 1 + min(
          dp[i-1][j],    ← delete (刪除 word1[i-1])
          dp[i][j-1],    ← insert (插入 word2[j-1])
          dp[i-1][j-1]   ← replace (替換)
      )
    """
    m, n = len(word1), len(word2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    ops = [[""]*( n+1) for _ in range(m+1)]  # 記錄操作
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                ops[i][j] = "keep"
            else:
                del_cost = dp[i-1][j]
                ins_cost = dp[i][j-1]
                rep_cost = dp[i-1][j-1]
                dp[i][j] = 1 + min(del_cost, ins_cost, rep_cost)
                if dp[i][j] == 1 + del_cost:
                    ops[i][j] = "del"
                elif dp[i][j] == 1 + ins_cost:
                    ops[i][j] = "ins"
                else:
                    ops[i][j] = "rep"
    if verbose:
        print(f'\n=== Edit Distance: "{word1}" → "{word2}" ===')
        header = '     ""  ' + "  ".join(f"{c:>2}" for c in word2)
        print(header)
        for i in range(m+1):
            label = f'  "{word1[i-1]}"' if i > 0 else '   ""'
            row = "  ".join(f"{dp[i][j]:2d}" for j in range(n+1))
            print(f"  {label}  {row}")
        print(f"  最少操作次數 = {dp[m][n]}")
        # 回溯路徑
        i, j, path = m, n, []
        while i > 0 or j > 0:
            if i > 0 and j > 0 and ops[i][j] == "keep":
                i, j = i-1, j-1
            elif i > 0 and j > 0 and ops[i][j] == "rep":
                path.append(f"replace '{word1[i-1]}' → '{word2[j-1]}'")
                i, j = i-1, j-1
            elif i > 0 and (j == 0 or ops[i][j] == "del"):
                path.append(f"delete '{word1[i-1]}'")
                i -= 1
            else:
                path.append(f"insert '{word2[j-1]}'")
                j -= 1
        for step in reversed(path):
            print(f"    操作: {step}")
    return dp[m][n]


def longest_palindromic_substring(s: str, verbose=False) -> str:
    """
    LeetCode 5 - Longest Palindromic Substring
    dp[i][j] = True if s[i..j] is palindrome
      - 長度1: dp[i][i] = True
      - 長度2: dp[i][i+1] = (s[i]==s[i+1])
      - 長度>=3: dp[i][j] = dp[i+1][j-1] and s[i]==s[j]
    """
    n = len(s)
    if n <= 1:
        return s
    dp = [[False]*n for _ in range(n)]
    start, max_len = 0, 1
    for i in range(n):
        dp[i][i] = True
    for i in range(n-1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start, max_len = i, 2
    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length
    result = s[start:start+max_len]
    if verbose:
        print(f'\n=== Longest Palindromic Substring: "{s}" ===')
        print(f"  DP table (T=palindrome):")
        header = "       " + "  ".join(f"{c:>2}" for c in s)
        print(header)
        for i in range(n):
            row = "  ".join(f"{'T':>2}" if dp[i][j] else f"{'·':>2}"
                           for j in range(n))
            print(f'    {s[i]:>2}  {row}')
        print(f'  最長回文子字串 = "{result}" (長度 {max_len})')
    return result


# ============================================================
# Section 3: 0/1 背包 (0/1 Knapsack)
# ============================================================
# 現實比喻：你有一個背包，容量有限。每個物品只能拿或不拿（0 或 1）。
# 目標：在不超重的情況下，讓背包內物品總價值最大。
#
# dp[i][w] = 考慮前 i 個物品、背包容量 w 時的最大價值
#   不拿第 i 個: dp[i][w] = dp[i-1][w]
#   拿第 i 個:   dp[i][w] = dp[i-1][w - weight[i]] + value[i]
#   dp[i][w] = max(不拿, 拿)

def knapsack_01(weights: list, values: list, capacity: int, verbose=False) -> int:
    """
    Classic 0/1 Knapsack — 2D 版本 + 1D 空間優化
    """
    n = len(weights)
    # --- 2D 版本 ---
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        w, v = weights[i-1], values[i-1]
        for c in range(capacity+1):
            dp[i][c] = dp[i-1][c]  # 不拿
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i-1][c-w] + v)  # 拿
    if verbose:
        print(f"\n=== 0/1 Knapsack (2D) ===")
        print(f"  物品: weights={weights}, values={values}, capacity={capacity}")
        header = "  容量 w:  " + "  ".join(f"{w:3d}" for w in range(capacity+1))
        print(header)
        for i in range(n+1):
            label = f"  item{i}   " if i > 0 else "  none    "
            row = "  ".join(f"{dp[i][c]:3d}" for c in range(capacity+1))
            extra = ""
            if i > 0:
                extra = f"  (w={weights[i-1]}, v={values[i-1]})"
            print(f"{label}{row}{extra}")
        print(f"  最大價值 = {dp[n][capacity]}")

    # --- 1D 空間優化 ---
    # 關鍵：內層迴圈 **倒序** 走，避免同一輪重複使用物品
    dp1d = [0] * (capacity + 1)
    if verbose:
        print(f"\n  === 1D 空間優化版 ===")
        print(f"  初始:  {dp1d}")
    for i in range(n):
        w, v = weights[i], values[i]
        for c in range(capacity, w - 1, -1):   # 倒序!
            dp1d[c] = max(dp1d[c], dp1d[c - w] + v)
        if verbose:
            print(f"  item{i+1} (w={w},v={v}): {dp1d}")
    if verbose:
        print(f"  1D 最大價值 = {dp1d[capacity]}")
    return dp[n][capacity]


def partition_equal_subset_sum(nums: list, verbose=False) -> bool:
    """
    LeetCode 416 - Partition Equal Subset Sum
    轉化為 0/1 背包：能否從 nums 中選出子集，和恰好 = total/2？
    dp[i][s] = 考慮前 i 個數字，能否湊出和 s
    """
    total = sum(nums)
    if total % 2 != 0:
        if verbose:
            print(f"\n=== Partition Equal Subset Sum ===")
            print(f"  nums={nums}, sum={total} (奇數，不可能均分)")
        return False
    target = total // 2
    n = len(nums)
    dp = [[False]*(target+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = True  # 和=0 永遠可以（不選任何）
    for i in range(1, n+1):
        for s in range(1, target+1):
            dp[i][s] = dp[i-1][s]  # 不選 nums[i-1]
            if s >= nums[i-1]:
                dp[i][s] = dp[i][s] or dp[i-1][s - nums[i-1]]
    if verbose:
        print(f"\n=== Partition Equal Subset Sum ===")
        print(f"  nums={nums}, total={total}, target={target}")
        header = "  sum:     " + " ".join(f"{s:>2}" for s in range(target+1))
        print(header)
        for i in range(n+1):
            label = f"  +{nums[i-1]:>2}     " if i > 0 else "  init     "
            row = " ".join(f"{'T':>2}" if dp[i][s] else f"{'·':>2}"
                          for s in range(target+1))
            print(f"{label}{row}")
        print(f"  能否均分? {dp[n][target]}")
    return dp[n][target]


def target_sum(nums: list, target: int, verbose=False) -> int:
    """
    LeetCode 494 - Target Sum
    每個數字前面放 + 或 -，使總和 = target。求方法數。
    轉化: 設正數子集和=P, 負數子集和=N
      P - N = target, P + N = total
      → P = (target + total) / 2
    變成 0/1 背包: 從 nums 中選子集，和 = P 的方法數
    """
    total = sum(nums)
    if (target + total) % 2 != 0 or abs(target) > total:
        if verbose:
            print(f"\n=== Target Sum: nums={nums}, target={target} ===")
            print(f"  (target+total)={target+total} 為奇數 或 |target|>total → 0 種")
        return 0
    bag = (target + total) // 2
    n = len(nums)
    dp = [[0]*(bag+1) for _ in range(n+1)]
    dp[0][0] = 1
    for i in range(1, n+1):
        for s in range(bag+1):
            dp[i][s] = dp[i-1][s]
            if s >= nums[i-1]:
                dp[i][s] += dp[i-1][s - nums[i-1]]
    if verbose:
        print(f"\n=== Target Sum: nums={nums}, target={target} ===")
        print(f"  轉化: bag capacity = (target+total)/2 = ({target}+{total})/2 = {bag}")
        header = "  sum:   " + " ".join(f"{s:>3}" for s in range(bag+1))
        print(header)
        for i in range(n+1):
            label = f"  +{nums[i-1]:>2}   " if i > 0 else "  init   "
            row = " ".join(f"{dp[i][s]:>3}" for s in range(bag+1))
            print(f"{label}{row}")
        print(f"  方法數 = {dp[n][bag]}")
    return dp[n][bag]


# ============================================================
# Section 4: 完全背包 (Unbounded Knapsack)
# ============================================================
# 與 0/1 背包的差異：每個物品可以 **無限次** 使用。
# 關鍵差異在迴圈順序：
#   0/1 背包 (1D): 內層倒序 for c in range(capacity, w-1, -1)
#   完全背包 (1D): 內層正序 for c in range(w, capacity+1)
# 正序 → dp[c-w] 可能已包含本輪物品 → 重複選取 → 完全背包!

def coin_change(coins: list, amount: int, verbose=False) -> int:
    """
    LeetCode 322 - Coin Change (最少硬幣數)
    完全背包：每種硬幣可用無限次。求湊出 amount 的最少硬幣數。
    dp[i][a] = 用前 i 種硬幣湊出金額 a 的最少硬幣數
      不用 coin[i]: dp[i][a] = dp[i-1][a]
      用 coin[i]:   dp[i][a] = dp[i][a - coin] + 1   ← 注意是 dp[i] 不是 dp[i-1]!
    """
    n = len(coins)
    INF = float('inf')
    dp = [[INF]*(amount+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = 0
    for i in range(1, n+1):
        c = coins[i-1]
        for a in range(amount+1):
            dp[i][a] = dp[i-1][a]  # 不用這種硬幣
            if a >= c and dp[i][a - c] != INF:
                dp[i][a] = min(dp[i][a], dp[i][a - c] + 1)
    if verbose:
        print(f"\n=== Coin Change: coins={coins}, amount={amount} ===")
        header = "  金額:  " + " ".join(f"{a:>3}" for a in range(amount+1))
        print(header)
        for i in range(n+1):
            label = f"  +{coins[i-1]:>2}   " if i > 0 else "  init   "
            row = " ".join(f"{'  X' if dp[i][a]==INF else f'{dp[i][a]:>3}'}"
                          for a in range(amount+1))
            print(f"{label}{row}")
        ans = dp[n][amount] if dp[n][amount] != INF else -1
        print(f"  最少硬幣數 = {ans}")
    return dp[n][amount] if dp[n][amount] != INF else -1


def coin_change_2(coins: list, amount: int, verbose=False) -> int:
    """
    LeetCode 518 - Coin Change 2 (組合數)
    完全背包：計算湊出 amount 的組合數（順序不同算同一種）。
    dp[i][a] = 用前 i 種硬幣湊出 a 的組合數
      dp[i][a] = dp[i-1][a] + dp[i][a - coin]
    """
    n = len(coins)
    dp = [[0]*(amount+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = 1
    for i in range(1, n+1):
        c = coins[i-1]
        for a in range(amount+1):
            dp[i][a] = dp[i-1][a]
            if a >= c:
                dp[i][a] += dp[i][a - c]  # dp[i] 不是 dp[i-1] → 可重複用
    if verbose:
        print(f"\n=== Coin Change 2 (組合數): coins={coins}, amount={amount} ===")
        header = "  金額:  " + " ".join(f"{a:>3}" for a in range(amount+1))
        print(header)
        for i in range(n+1):
            label = f"  +{coins[i-1]:>2}   " if i > 0 else "  init   "
            row = " ".join(f"{dp[i][a]:>3}" for a in range(amount+1))
            print(f"{label}{row}")
        print(f"  組合數 = {dp[n][amount]}")
    return dp[n][amount]


# ============================================================
# Section 5: 區間 DP (Interval DP)
# ============================================================

def palindrome_partitioning_ii(s: str, verbose=False) -> int:
    """
    LeetCode 132 - Palindrome Partitioning II
    最少切幾刀使每段都是回文？
    Step 1: 預處理 is_pal[i][j] = s[i..j] 是否回文
    Step 2: dp[i] = s[0..i] 最少切幾刀
      若 s[0..i] 本身回文 → dp[i] = 0
      否則: dp[i] = min(dp[j-1] + 1) for all j where is_pal[j][i]
    """
    n = len(s)
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n-1):
        is_pal[i][i+1] = (s[i] == s[i+1])
    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i+1][j-1]
    dp = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = i  # 最多切 i 刀
            for j in range(1, i+1):
                if is_pal[j][i]:
                    dp[i] = min(dp[i], dp[j-1] + 1)
    if verbose:
        print(f'\n=== Palindrome Partitioning II: "{s}" ===')
        print(f"  回文表 is_pal[i][j] (T=palindrome):")
        print("       " + "  ".join(f"{c:>2}" for c in s))
        for i in range(n):
            row = "  ".join(f"{'T':>2}" if is_pal[i][j] else f"{'·':>2}"
                           for j in range(n))
            print(f"    {s[i]:>2}  {row}")
        print(f"  dp (最少切幾刀): {dp}")
        print(f"  最少切 {dp[n-1]} 刀")
    return dp[n-1]


def burst_balloons(nums: list, verbose=False) -> int:
    """
    LeetCode 312 - Burst Balloons (Google 經典困難題!)
    戳破所有氣球獲得最多金幣。戳破 i 得 nums[left]*nums[i]*nums[right]。

    關鍵想法：不要想「先戳哪個」，而是想「最後戳哪個」。
    加邊界 [1] + nums + [1]，dp[i][j] = 戳破 (i, j) 之間所有氣球的最大金幣。
    dp[i][j] = max(dp[i][k] + dp[k][j] + arr[i]*arr[k]*arr[j]) for k in (i+1..j-1)
    k 是「最後一個被戳的氣球」。
    """
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0]*n for _ in range(n)]
    # 從短區間到長區間
    for length in range(2, n):  # length = j - i
        for i in range(n - length):
            j = i + length
            for k in range(i+1, j):
                val = dp[i][k] + dp[k][j] + arr[i] * arr[k] * arr[j]
                dp[i][j] = max(dp[i][j], val)
    if verbose:
        print(f"\n=== Burst Balloons: {nums} ===")
        print(f"  加邊界後: {arr}")
        print(f"  DP table dp[i][j] (i=row, j=col):")
        header = "     " + "  ".join(f"{v:>4}" for v in arr)
        print(header)
        for i in range(n):
            row = "  ".join(f"{dp[i][j]:>4}" for j in range(n))
            print(f"  {arr[i]:>2}  {row}")
        print(f"  最大金幣 = {dp[0][n-1]}")
    return dp[0][n-1]


# ============================================================
# Section 6: 比較總整理 (Pattern Comparison)
# ============================================================

def print_comparison():
    """
    列印 0/1背包 vs 完全背包 vs 區間DP 的比較表
    """
    print("""
============================================================
  Section 6: 0/1背包 vs 完全背包 vs 區間DP 比較
============================================================

┌─────────────┬───────────────────┬───────────────────┬──────────────────┐
│             │  0/1 背包          │  完全背包          │  區間 DP          │
├─────────────┼───────────────────┼───────────────────┼──────────────────┤
│ 物品使用     │ 每個只能用一次     │ 每個可用無限次     │ N/A              │
│ 狀態定義     │ dp[i][w]          │ dp[i][w]          │ dp[i][j]         │
│             │ 前i個物品,容量w    │ 前i種,容量w       │ 區間[i,j]的最佳解 │
│ 轉移來源     │ dp[i-1][...]      │ dp[i][...]        │ 列舉分割點k      │
│ 1D迴圈順序   │ 內層倒序 ←←←      │ 內層正序 →→→      │ 枚舉區間長度     │
│ 經典題目     │ 416 Partition     │ 322 Coin Change   │ 312 Burst Balloon│
│             │ 494 Target Sum    │ 518 Coin Change 2 │ 132 Palindrome   │
├─────────────┴───────────────────┴───────────────────┴──────────────────┤
│ 如何判斷用哪種？                                                       │
│  1. 「每個元素只選一次」→ 0/1 背包                                      │
│  2. 「每個元素可重複選」→ 完全背包                                      │
│  3. 「合併/分割區間」   → 區間 DP                                      │
│  4. 「兩個字串比對」    → 字串 2D DP (LCS / Edit Distance)             │
│  5. 「網格走路」        → 網格 2D DP                                   │
└────────────────────────────────────────────────────────────────────────┘

迴圈順序差異 (最重要的觀念!):

  # 0/1 背包 — 1D 倒序
  for i in range(n):
      for c in range(capacity, w[i]-1, -1):  # ← 倒序: 每個物品最多用一次
          dp[c] = max(dp[c], dp[c-w[i]] + v[i])

  # 完全背包 — 1D 正序
  for i in range(n):
      for c in range(w[i], capacity+1):       # → 正序: 允許重複使用
          dp[c] = max(dp[c], dp[c-w[i]] + v[i])

  為什麼倒序 = 0/1？
    倒序時 dp[c-w] 還是「上一輪(不含物品i)」的值 → 不會重複選。
  為什麼正序 = 完全？
    正序時 dp[c-w] 可能「本輪已更新過」→ 物品i可被重複選取。
""")


# ============================================================
# main() — 每個問題 3 組測試範例，完整數值追蹤
# ============================================================

def main():
    print("=" * 60)
    print("  Section 1: 二維 DP 基礎 (2D DP Basics)")
    print("=" * 60)

    # --- Unique Paths: 3 examples ---
    # Ex1: 3x3 grid
    # dp:  1  1  1
    #      1  2  3
    #      1  3  6  → 答案 6
    unique_paths(3, 3, verbose=True)

    # Ex2: 3x7
    unique_paths(3, 7, verbose=True)

    # Ex3: 2x4
    unique_paths(2, 4, verbose=True)

    # --- Unique Paths II: 3 examples ---
    # Ex1: obstacle at center
    unique_paths_with_obstacles(
        [[0,0,0],[0,1,0],[0,0,0]], verbose=True)
    # Ex2: obstacle blocking first row
    unique_paths_with_obstacles(
        [[0,1,0],[0,0,0],[0,0,0]], verbose=True)
    # Ex3: start is blocked
    unique_paths_with_obstacles(
        [[1,0],[0,0]], verbose=True)

    # --- Minimum Path Sum: 3 examples ---
    min_path_sum([[1,3,1],[1,5,1],[4,2,1]], verbose=True)
    min_path_sum([[1,2,3],[4,5,6]], verbose=True)
    min_path_sum([[1,2],[5,1],[2,1]], verbose=True)

    print("\n" + "=" * 60)
    print("  Section 2: 字串型 2D DP (String DP)")
    print("=" * 60)

    # --- LCS: 3 examples ---
    longest_common_subsequence("abcde", "ace", verbose=True)
    longest_common_subsequence("abc", "abc", verbose=True)
    longest_common_subsequence("abc", "def", verbose=True)

    # --- Edit Distance: 3 examples ---
    edit_distance("horse", "ros", verbose=True)
    edit_distance("intention", "execution", verbose=True)
    edit_distance("abc", "abc", verbose=True)

    # --- Longest Palindromic Substring: 3 examples ---
    longest_palindromic_substring("babad", verbose=True)
    longest_palindromic_substring("cbbd", verbose=True)
    longest_palindromic_substring("aacabdkacaa", verbose=True)

    print("\n" + "=" * 60)
    print("  Section 3: 0/1 背包 (0/1 Knapsack)")
    print("=" * 60)

    print("""
  0/1 背包概念 — 現實比喻:
  你要去露營，背包最多裝 W 公斤。
  有 n 件物品，每件有「重量」和「價值」。
  每件只能帶或不帶 (0 或 1)，求最大總價值。
    """)

    # --- Classic 0/1 Knapsack: 3 examples ---
    knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7, verbose=True)
    knapsack_01([2, 3, 4], [3, 4, 5], 5, verbose=True)
    knapsack_01([1, 2, 3], [6, 10, 12], 5, verbose=True)

    # --- Partition Equal Subset Sum: 3 examples ---
    partition_equal_subset_sum([1, 5, 11, 5], verbose=True)
    partition_equal_subset_sum([1, 2, 3, 5], verbose=True)
    partition_equal_subset_sum([3, 3, 3, 4, 5], verbose=True)

    # --- Target Sum: 3 examples ---
    target_sum([1, 1, 1, 1, 1], 3, verbose=True)
    target_sum([1, 2, 3], 0, verbose=True)
    target_sum([2, 1], 1, verbose=True)

    print("\n" + "=" * 60)
    print("  Section 4: 完全背包 (Unbounded Knapsack)")
    print("=" * 60)

    # --- Coin Change: 3 examples ---
    coin_change([1, 2, 5], 11, verbose=True)
    coin_change([2], 3, verbose=True)
    coin_change([1, 3, 4], 6, verbose=True)

    # --- Coin Change 2: 3 examples ---
    coin_change_2([1, 2, 5], 5, verbose=True)
    coin_change_2([2], 3, verbose=True)
    coin_change_2([1, 2, 3], 4, verbose=True)

    print("""
  *** 0/1 vs 完全背包 — 迴圈順序差異 ***
  0/1 背包 1D: 內層 倒序 (capacity → 0)   → 每個物品最多用一次
  完全背包 1D: 內層 正序 (0 → capacity)   → 每個物品可重複用
  只差一個方向，效果完全不同! 面試常考!
    """)

    print("\n" + "=" * 60)
    print("  Section 5: 區間 DP (Interval DP)")
    print("=" * 60)

    # --- Palindrome Partitioning II: 2 examples ---
    palindrome_partitioning_ii("aab", verbose=True)
    palindrome_partitioning_ii("abacbc", verbose=True)

    # --- Burst Balloons: 2 examples ---
    burst_balloons([3, 1, 5, 8], verbose=True)
    burst_balloons([1, 5], verbose=True)

    print("\n" + "=" * 60)
    print("  Section 6: 背包 vs 區間 DP 比較總整理")
    print("=" * 60)
    print_comparison()

    print("\n全部執行完畢! 所有 DP 表格皆已追蹤完成。")


if __name__ == "__main__":
    main()
