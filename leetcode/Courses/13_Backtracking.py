"""
==============================================================================
  LeetCode 刷題教學：Backtracking（回溯法）
  目標公司：Google / NVIDIA
  難度定位：Beginner → Intermediate
  教學語言：Traditional Chinese + English technical terms
==============================================================================

回溯法 (Backtracking) 是一種「系統性窮舉」的搜尋策略。
核心思想：像走迷宮一樣，每到一個岔路就選一條走，走不通就「退回上一步」換另一條。

物理類比 (Physical Analogy):
  想像你在一座迷宮裡找出口：
  1. 你走到一個岔路口 → 選一個方向走 (make choice)
  2. 走到死路 → 退回岔路口 (backtrack / undo choice)
  3. 換另一個方向走 → 繼續探索 (try next choice)
  4. 找到出口 → 記錄這條路徑 (add to result)

  回溯 = DFS (深度優先搜尋) + 撤銷操作

萬用模板 (Universal Template):
  def backtrack(path, choices):
      if 滿足結束條件 (base case):
          result.append(path[:])   # 加入結果（注意要複製！）
          return
      for choice in choices:
          path.append(choice)       # 做選擇
          backtrack(path, 剩餘選擇) # 遞迴探索
          path.pop()                # 撤銷選擇（回溯！）

六大類型：
  1. 子集型 (Subsets)：選或不選，順序無關 → 用 start index
  2. 排列型 (Permutations)：順序有關，全部都要用 → 用 used[] 陣列
  3. 組合型 (Combinations)：選 k 個，順序無關 → 用 start index + 計數
  4. 棋盤型 (Board)：在格子上放東西 → 逐行/逐格嘗試
  5. 分割型 (Partition)：把字串切成合法子串 → 用 start index 切割
  6. 圖型 (Graph)：在圖/矩陣上找路徑 → visited 陣列

本檔案所有程式碼皆可直接執行 (python3 13_Backtracking.py)
"""

from typing import List, Optional
from copy import deepcopy


# ============================================================================
# Section 1: 回溯核心概念 (Backtracking Core Template)
# ============================================================================
# 最簡單的回溯範例：生成所有二進位字串 (Binary Strings)
#
# 思路：每個位置有兩個選擇 (0 或 1)，嘗試所有組合。
#
# Decision Tree for n=3:
#                        ""
#                   /          \
#                 "0"           "1"
#               /    \        /    \
#            "00"   "01"   "10"    "11"
#            / \    / \    / \     / \
#         "000""001""010""011""100""101""110""111"
#
# 模板拆解：
#   1. path = 目前走過的路徑
#   2. choices = 在這一步可以做的選擇
#   3. base case = 路徑夠長了，收集結果
#   4. backtrack = pop 掉最後的選擇，試下一個

def generate_binary_strings(n: int, verbose: bool = False) -> List[str]:
    """生成所有長度為 n 的二進位字串"""
    result = []

    def backtrack(path: list):
        # Base case: 路徑長度達到 n
        if len(path) == n:
            result.append("".join(path))
            if verbose:
                print(f"    -> 找到結果: {''.join(path)}")
            return

        # 兩個選擇: 0 或 1
        for choice in ["0", "1"]:
            path.append(choice)             # 做選擇
            if verbose:
                print(f"  {'  ' * len(path)}選擇 {choice}: path={path}")
            backtrack(path)                 # 遞迴
            path.pop()                      # 撤銷選擇 (backtrack!)
            if verbose:
                print(f"  {'  ' * (len(path)+1)}撤銷 {choice}: path={path}")

    backtrack([])
    return result


# ============================================================================
# Section 2: 子集型 (Subsets)
# ============================================================================
# 核心：對每個元素，選 or 不選，產生所有可能的子集合。
# 重點：用 start index 確保不重複（不走回頭路）。
#
# 模板：
#   def backtrack(start, path):
#       result.append(path[:])       # 每個節點都是合法子集
#       for i in range(start, n):    # 只看 start 之後的元素
#           path.append(nums[i])
#           backtrack(i + 1, path)   # 下一次從 i+1 開始
#           path.pop()

# --------------------------------------------------------------------------
# 2.1 Subsets (LeetCode 78)
# --------------------------------------------------------------------------
# 題目：給定不含重複元素的陣列，返回所有子集。
# Time: O(n * 2^n), Space: O(n) 遞迴深度

def subsets(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """返回 nums 的所有子集（無重複元素）"""
    result = []
    n = len(nums)

    def backtrack(start: int, path: list):
        result.append(path[:])  # 每個節點都是子集
        if verbose:
            print(f"  {'  ' * len(path)}收集子集: {path}")

        for i in range(start, n):
            path.append(nums[i])
            if verbose:
                print(f"  {'  ' * len(path)}選擇 nums[{i}]={nums[i]}: path={path}")
            backtrack(i + 1, path)
            path.pop()
            if verbose:
                print(f"  {'  ' * (len(path)+1)}撤銷 nums[{i}]={nums[i]}: path={path}")

    backtrack(0, [])
    return result


# --------------------------------------------------------------------------
# 2.2 Subsets II (LeetCode 90) - 含重複元素
# --------------------------------------------------------------------------
# 題目：含重複元素的陣列，返回所有不重複的子集。
# 關鍵：先排序，同一層遇到相同元素就跳過！
#
# Skip Logic:
#   nums = [1,2,2] (已排序)
#   當 i > start 且 nums[i] == nums[i-1] 時跳過
#   → 避免同一層選了兩次相同的值

def subsets_with_dup(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """返回 nums 的所有不重複子集（含重複元素）"""
    nums.sort()  # 必須先排序！
    result = []
    n = len(nums)

    def backtrack(start: int, path: list):
        result.append(path[:])
        if verbose:
            print(f"  {'  ' * len(path)}收集子集: {path}")

        for i in range(start, n):
            # 關鍵跳過邏輯：同一層不選重複元素
            if i > start and nums[i] == nums[i - 1]:
                if verbose:
                    print(f"  {'  ' * (len(path)+1)}跳過 nums[{i}]={nums[i]} "
                          f"(與 nums[{i-1}] 重複)")
                continue

            path.append(nums[i])
            if verbose:
                print(f"  {'  ' * len(path)}選擇 nums[{i}]={nums[i]}: path={path}")
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


# ============================================================================
# Section 3: 排列型 (Permutations)
# ============================================================================
# 核心：順序有關！[1,2] 和 [2,1] 是不同排列。
# 重點：用 used[] 布林陣列記錄哪些元素已使用。
#
# 模板：
#   def backtrack(path):
#       if len(path) == n: result.append(path[:])
#       for i in range(n):            # 每次都從 0 開始看！
#           if used[i]: continue       # 已用過就跳過
#           used[i] = True
#           path.append(nums[i])
#           backtrack(path)
#           path.pop()
#           used[i] = False

# --------------------------------------------------------------------------
# 3.1 Permutations (LeetCode 46)
# --------------------------------------------------------------------------
# 題目：給定不含重複元素的陣列，返回所有排列。
# Time: O(n * n!), Space: O(n)

def permutations(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """返回 nums 的所有排列（無重複元素）"""
    result = []
    n = len(nums)
    used = [False] * n

    def backtrack(path: list):
        if len(path) == n:
            result.append(path[:])
            if verbose:
                print(f"    -> 找到排列: {path}")
            return

        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            if verbose:
                indent = "  " * (len(path) + 1)
                print(f"  {indent}選擇 nums[{i}]={nums[i]}: "
                      f"path={path}, used={used}")
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


# --------------------------------------------------------------------------
# 3.2 Permutations II (LeetCode 47) - 含重複元素
# --------------------------------------------------------------------------
# 題目：含重複元素的陣列，返回所有不重複的排列。
# 關鍵：排序 + 同一層相同值且前一個沒用過 → 跳過
#
# 剪枝條件：
#   if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
#       continue
#   意義：相同的數字，必須按順序使用（第一個用了才能用第二個）

def permutations_unique(nums: List[int], verbose: bool = False) -> List[List[int]]:
    """返回 nums 的所有不重複排列（含重複元素）"""
    nums.sort()  # 必須先排序！
    result = []
    n = len(nums)
    used = [False] * n

    def backtrack(path: list):
        if len(path) == n:
            result.append(path[:])
            if verbose:
                print(f"    -> 找到排列: {path}")
            return

        for i in range(n):
            if used[i]:
                continue
            # 剪枝：同值元素，前一個沒用就不用這個（避免重複）
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                if verbose:
                    print(f"    {'  ' * len(path)}跳過 nums[{i}]={nums[i]} "
                          f"(前一個相同值未使用)")
                continue

            used[i] = True
            path.append(nums[i])
            if verbose:
                print(f"    {'  ' * len(path)}選擇 nums[{i}]={nums[i]}: "
                      f"path={path}")
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


# --------------------------------------------------------------------------
# 3.3 Next Permutation (LeetCode 31) - 非回溯，但重要！
# --------------------------------------------------------------------------
# 題目：找出下一個字典序更大的排列。如果已是最大，返回最小排列。
# 思路（三步驟）：
#   1. 從右往左找第一個下降位 i（nums[i] < nums[i+1]）
#   2. 從右往左找第一個比 nums[i] 大的位 j，交換 i,j
#   3. 反轉 i+1 到末尾
#
# 範例: [1,2,3] -> 找 i=1(2<3), j=2(3>2), swap -> [1,3,2], reverse 空 -> [1,3,2]

def next_permutation(nums: List[int], verbose: bool = False) -> None:
    """原地修改 nums 為下一個排列"""
    n = len(nums)
    if verbose:
        print(f"  原始: {nums}")

    # Step 1: 從右往左找第一個下降位 i
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if verbose:
        print(f"  Step 1: 從右找第一個下降位 → i={i}" +
              (f" (nums[{i}]={nums[i]})" if i >= 0 else " (已是最大排列)"))

    if i >= 0:
        # Step 2: 從右往左找第一個比 nums[i] 大的位 j
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        if verbose:
            print(f"  Step 2: 從右找第一個 > nums[{i}]={nums[i]} "
                  f"→ j={j} (nums[{j}]={nums[j]})")

        # 交換 i, j
        nums[i], nums[j] = nums[j], nums[i]
        if verbose:
            print(f"  Step 2: 交換 nums[{i}] 和 nums[{j}] → {nums}")

    # Step 3: 反轉 i+1 到末尾
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    if verbose:
        print(f"  Step 3: 反轉 index {i+1} 到末尾 → {nums}")


# ============================================================================
# Section 4: 組合型 (Combinations)
# ============================================================================
# 核心：從 n 個中選 k 個，順序無關 → C(n,k)
# 重點：用 start index + 計數（path 長度 == k 時收集）
#
# 模板：
#   def backtrack(start, path):
#       if len(path) == k:
#           result.append(path[:])
#           return
#       for i in range(start, n+1):   # 剪枝：可限制上界
#           path.append(i)
#           backtrack(i + 1, path)
#           path.pop()

# --------------------------------------------------------------------------
# 4.1 Combinations (LeetCode 77)
# --------------------------------------------------------------------------
# 題目：給定 n 和 k，返回 1~n 中所有大小為 k 的組合。
# Time: O(k * C(n,k)), Space: O(k)

def combine(n: int, k: int, verbose: bool = False) -> List[List[int]]:
    """返回 1~n 中所有大小為 k 的組合"""
    result = []

    def backtrack(start: int, path: list):
        if len(path) == k:
            result.append(path[:])
            if verbose:
                print(f"    -> 找到組合: {path}")
            return

        # 剪枝: 剩餘數量不夠填滿 k 個就不用繼續了
        # need = k - len(path), 至少需要 need 個數，所以 i 最大到 n - need + 1
        remaining_needed = k - len(path)
        for i in range(start, n - remaining_needed + 2):
            path.append(i)
            if verbose:
                print(f"    {'  ' * len(path)}選擇 {i}: path={path}")
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result


# --------------------------------------------------------------------------
# 4.2 Combination Sum (LeetCode 39) - 可重複使用
# --------------------------------------------------------------------------
# 題目：candidates 中的數字可無限次使用，找出所有和為 target 的組合。
# 關鍵：遞迴時 start 不加 1（同一個數可以再選）！
# Time: O(n^(T/M)) where T=target, M=min(candidates)

def combination_sum(candidates: List[int], target: int,
                    verbose: bool = False) -> List[List[int]]:
    """找出所有和為 target 的組合（元素可重複使用）"""
    candidates.sort()
    result = []

    def backtrack(start: int, path: list, remaining: int):
        if remaining == 0:
            result.append(path[:])
            if verbose:
                print(f"    -> 找到組合: {path}, sum={target}")
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            # 剪枝: 後面的數更大，不可能湊到了
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            if verbose:
                curr_sum = target - remaining + candidates[i]
                print(f"    {'  ' * len(path)}選擇 {candidates[i]}: "
                      f"path={path}, sum={curr_sum}, "
                      f"remaining={remaining - candidates[i]}")
            backtrack(i, path, remaining - candidates[i])  # i 不加 1！
            path.pop()

    backtrack(0, [], target)
    return result


# --------------------------------------------------------------------------
# 4.3 Combination Sum II (LeetCode 40) - 不可重複，含重複元素
# --------------------------------------------------------------------------
# 題目：candidates 有重複，每個數只能用一次，找和為 target 的所有不重複組合。
# 關鍵：排序 + 同層跳過重複（和 Subsets II 一樣的邏輯）

def combination_sum2(candidates: List[int], target: int,
                     verbose: bool = False) -> List[List[int]]:
    """找出和為 target 的所有不重複組合（每個數只能用一次）"""
    candidates.sort()
    result = []

    def backtrack(start: int, path: list, remaining: int):
        if remaining == 0:
            result.append(path[:])
            if verbose:
                print(f"    -> 找到組合: {path}, sum={target}")
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            # 同層跳過重複
            if i > start and candidates[i] == candidates[i - 1]:
                if verbose:
                    print(f"    {'  ' * len(path)}  跳過重複 "
                          f"candidates[{i}]={candidates[i]}")
                continue

            path.append(candidates[i])
            if verbose:
                curr_sum = target - remaining + candidates[i]
                print(f"    {'  ' * len(path)}選擇 {candidates[i]}: "
                      f"path={path}, sum={curr_sum}")
            backtrack(i + 1, path, remaining - candidates[i])  # i+1！
            path.pop()

    backtrack(0, [], target)
    return result


# --------------------------------------------------------------------------
# 4.4 Letter Combinations of Phone Number (LeetCode 17)
# --------------------------------------------------------------------------
# 題目：給定手機按鍵數字字串，返回所有可能的字母組合。
# 思路：每個數字對應幾個字母，逐層展開。

PHONE_MAP = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
}

def letter_combinations(digits: str, verbose: bool = False) -> List[str]:
    """返回手機按鍵數字字串的所有字母組合"""
    if not digits:
        return []
    result = []

    def backtrack(index: int, path: list):
        if index == len(digits):
            result.append("".join(path))
            if verbose:
                print(f"    -> 找到組合: {''.join(path)}")
            return

        letters = PHONE_MAP[digits[index]]
        for letter in letters:
            path.append(letter)
            if verbose:
                print(f"    {'  ' * index}digit='{digits[index]}' "
                      f"選擇 '{letter}': path={path}")
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return result


# ============================================================================
# Section 5: 棋盤型 (Board / Grid Backtracking)
# ============================================================================
# 核心：在二維格子上放置/搜尋，需要維護棋盤狀態。

# --------------------------------------------------------------------------
# 5.1 N-Queens (LeetCode 51)
# --------------------------------------------------------------------------
# 題目：在 n x n 棋盤上放 n 個皇后，使得彼此不能攻擊。
# 皇后攻擊：同行、同列、同對角線。
# 思路：逐行放置，用集合記錄已佔用的列和對角線。
#
# 對角線技巧：
#   主對角線 (\): row - col 相同
#   副對角線 (/): row + col 相同

def solve_n_queens(n: int, verbose: bool = False) -> List[List[str]]:
    """解 N 皇后問題，返回所有合法棋盤"""
    result = []
    queens = []  # queens[i] = 第 i 行皇后放在第幾列
    cols = set()
    diag1 = set()  # row - col (主對角線 \)
    diag2 = set()  # row + col (副對角線 /)

    def backtrack(row: int):
        if row == n:
            # 建構棋盤字串
            board = []
            for r in range(n):
                line = "." * queens[r] + "Q" + "." * (n - queens[r] - 1)
                board.append(line)
            result.append(board)
            if verbose:
                print(f"    -> 找到解! 皇后位置: {queens}")
                for line in board:
                    print(f"       {line}")
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                if verbose and n <= 5:
                    reasons = []
                    if col in cols:
                        reasons.append("同列衝突")
                    if (row - col) in diag1:
                        reasons.append("主對角線衝突")
                    if (row + col) in diag2:
                        reasons.append("副對角線衝突")
                    print(f"    row={row}, col={col}: "
                          f"{'、'.join(reasons)} → 跳過")
                continue

            queens.append(col)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            if verbose:
                print(f"    row={row}, col={col}: 放置皇后 → "
                      f"queens={queens}")
            backtrack(row + 1)
            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


# --------------------------------------------------------------------------
# 5.2 Sudoku Solver (LeetCode 37)
# --------------------------------------------------------------------------
# 題目：填完一個 9x9 數獨。
# 思路：找空格 → 嘗試 1-9 → 檢查合法性 → 遞迴 → 回溯
#
# 合法性檢查：同行、同列、同 3x3 宮格不能有重複數字。
# box index = (row // 3) * 3 + (col // 3)

def solve_sudoku(board: List[List[str]], verbose: bool = False) -> bool:
    """原地求解數獨，回傳是否有解"""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    # 初始化已有的數字
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                num = board[r][c]
                rows[r].add(num)
                cols[c].add(num)
                boxes[(r // 3) * 3 + (c // 3)].add(num)

    def backtrack(pos: int) -> bool:
        # 找下一個空格
        while pos < 81:
            r, c = pos // 9, pos % 9
            if board[r][c] == ".":
                break
            pos += 1
        if pos == 81:
            return True  # 填完了

        r, c = pos // 9, pos % 9
        box_id = (r // 3) * 3 + (c // 3)

        for num_int in range(1, 10):
            num = str(num_int)
            if num in rows[r] or num in cols[c] or num in boxes[box_id]:
                continue

            board[r][c] = num
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_id].add(num)
            if verbose:
                print(f"    ({r},{c}) 嘗試 {num}")

            if backtrack(pos + 1):
                return True

            board[r][c] = "."
            rows[r].remove(num)
            cols[c].remove(num)
            boxes[box_id].remove(num)
            if verbose:
                print(f"    ({r},{c}) 回溯，撤銷 {num}")

        return False

    return backtrack(0)


# --------------------------------------------------------------------------
# 5.3 Word Search (LeetCode 79)
# --------------------------------------------------------------------------
# 題目：在 m x n 格子中搜尋單字，可上下左右走，每格只能用一次。
# 思路：DFS + 標記已訪問 → 回溯時取消標記

def word_search(board: List[List[str]], word: str,
                verbose: bool = False) -> bool:
    """在格子中搜尋是否存在 word"""
    if not board or not board[0]:
        return False
    m, n = len(board), len(board[0])

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True

        if r < 0 or r >= m or c < 0 or c >= n:
            return False
        if board[r][c] != word[idx]:
            return False

        # 標記已訪問（用 # 暫時替換）
        original = board[r][c]
        board[r][c] = "#"
        if verbose:
            print(f"    ({r},{c})='{original}' 匹配 word[{idx}]='{word[idx]}'")

        # 四個方向
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = original  # 恢復
                return True

        board[r][c] = original  # 回溯：恢復原值
        if verbose:
            print(f"    ({r},{c}) 四方向都走不通，回溯")
        return False

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0]:
                if verbose:
                    print(f"  起點 ({i},{j})='{board[i][j]}':")
                if backtrack(i, j, 0):
                    return True
    return False


# ============================================================================
# Section 6: 子集 vs 排列 vs 組合 比較 (Comparison)
# ============================================================================
# 這是面試最常被問的：三者有什麼不同？模板差在哪？
#
# ┌──────────────┬──────────────────┬──────────────────┬──────────────────┐
# │              │ Subsets 子集     │ Permutations 排列│ Combinations 組合│
# ├──────────────┼──────────────────┼──────────────────┼──────────────────┤
# │ 順序重要？   │ 否               │ 是               │ 否               │
# │ 選幾個？     │ 任意個 (0~n)     │ 全部 n 個        │ 恰好 k 個        │
# │ 避免重複方式 │ start index      │ used[] 陣列      │ start index      │
# │ 迴圈起點     │ for i in         │ for i in         │ for i in         │
# │              │   range(start,n) │   range(0, n)    │   range(start,n) │
# │ 收集時機     │ 每個節點         │ path長度==n      │ path長度==k      │
# │ 典型題       │ LeetCode 78, 90  │ LeetCode 46, 47  │ LeetCode 77, 39  │
# │ 結果數量     │ 2^n              │ n!               │ C(n,k)           │
# └──────────────┴──────────────────┴──────────────────┴──────────────────┘
#
# 去重邏輯（含重複元素時）：
#   Subsets II / Combination Sum II:
#     排序 + if i > start and nums[i] == nums[i-1]: continue
#   Permutations II:
#     排序 + if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
#
# 決策流程：
#   1. 順序重要嗎？ → 是: Permutation → 否: 下一步
#   2. 選幾個？
#      → 任意個: Subset
#      → 固定 k 個: Combination
#      → 和為 target: Combination Sum


# ============================================================================
# main() - 完整測試與範例展示
# ============================================================================

def main():
    # ==================================================================
    # Section 1: 回溯核心概念
    # ==================================================================
    print("=" * 70)
    print(" Section 1: 回溯核心概念 (Backtracking Core Template)")
    print("=" * 70)

    print("\n--- 生成二進位字串 (Binary Strings) ---")

    # 範例 1: n=2
    print("\n範例 1: n=2")
    # Decision Tree:
    #          ""
    #        /    \
    #      "0"    "1"
    #      / \    / \
    #   "00""01""10""11"
    print("  Decision Tree:")
    print('           ""')
    print("         /    \\")
    print('       \"0\"    \"1\"')
    print("       / \\    / \\")
    print('    \"00\"\"01\"\"10\"\"11\"')
    result = generate_binary_strings(2, verbose=True)
    print(f"  結果: {result}")
    assert result == ["00", "01", "10", "11"]

    # 範例 2: n=3
    print("\n範例 2: n=3")
    result = generate_binary_strings(3)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 8

    # 範例 3: n=1
    print("\n範例 3: n=1")
    result = generate_binary_strings(1)
    print(f"  結果: {result}")
    assert result == ["0", "1"]

    # ==================================================================
    # Section 2: 子集型 (Subsets)
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 2: 子集型 (Subsets)")
    print("=" * 70)

    # ---------- 2.1 Subsets ----------
    print("\n--- 2.1 Subsets (LeetCode 78) ---")

    # 範例 1: nums = [1,2,3]
    print("\n範例 1: nums = [1,2,3]")
    print("""
  Decision Tree (start index 控制，每個節點都收集):
                         []
                  /       |       \\
               [1]       [2]      [3]
              /   \\       |
          [1,2]  [1,3]  [2,3]
            |
        [1,2,3]

  Trace: []->[1]->[1,2]->[1,2,3]->撤銷3->[1,2]->撤銷2->
         [1,3]->撤銷3->[1]->撤銷1->[2]->[2,3]->撤銷3->
         [2]->撤銷2->[3]->撤銷3->[]
  收集順序: [],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3] (共 8=2^3)
""")
    result = subsets([1, 2, 3], verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 8  # 2^3

    # 範例 2: nums = [0]
    print("\n範例 2: nums = [0]")
    print("""
  Decision Tree:
       []
       |
      [0]
""")
    result = subsets([0])
    print(f"  結果: {result}")
    assert result == [[], [0]]

    # 範例 3: nums = [1,2]
    print("\n範例 3: nums = [1,2]")
    print("""
  Decision Tree:
          []
        /    \\
      [1]    [2]
       |
     [1,2]
  結果: [], [1], [1,2], [2]  (共 2^2=4 個)
""")
    result = subsets([1, 2])
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 4

    # ---------- 2.2 Subsets II ----------
    print("\n--- 2.2 Subsets II with duplicates (LeetCode 90) ---")

    # 範例 1: nums = [1,2,2]
    print("\n範例 1: nums = [1,2,2]")
    print("""
  排序後: [1,2,2]
  Decision Tree (同層重複跳過):
          []
       /    |     \\
    [1]    [2]   [2]←跳過(i>start且==前一個)
    / \\     |
  [1,2][1,2] [2,2]
    |   ↑跳過
  [1,2,2]
  Trace: []->[1]->[1,2]->[1,2,2]->跳過第二個2->[2]->[2,2]->跳過
  結果: [],[1],[1,2],[1,2,2],[2],[2,2] (6 個)
""")
    result = subsets_with_dup([1, 2, 2], verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 6

    # 範例 2: nums = [1,1,1]
    print("\n範例 2: nums = [1,1,1] → 同層只選第一個 1")
    result = subsets_with_dup([1, 1, 1])
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 4

    # 範例 3: nums = [4,4,1,4]
    print("\n範例 3: nums = [4,4,1,4] → 排序後 [1,4,4,4]")
    result = subsets_with_dup([4, 4, 1, 4])
    print(f"  結果 ({len(result)} 個): {result}")
    # [],[1],[1,4],[1,4,4],[1,4,4,4],[4],[4,4],[4,4,4]
    assert len(result) == 8

    # ---------- Include/Exclude 比較 ----------
    print("\n--- Include/Exclude 方法 vs Iteration 方法比較 ---")
    print("""
  方法一: Include/Exclude（二元分支：選它 or 不選它）
    def backtrack(i, path):
        if i == n: result.append(path[:]); return
        backtrack(i+1, path)            # 不選
        path.append(nums[i])            # 選
        backtrack(i+1, path); path.pop()

  方法二: Iteration（for 迴圈選下一個）← 本文使用
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, n):
            path.append(nums[i]); backtrack(i+1, path); path.pop()

  兩者結果相同，樹形不同。nums=[1,2]:
  Include/Exclude: [],[2],[1],[1,2]  Iteration: [],[1],[1,2],[2]
""")
    r1 = subsets([1, 2])
    print(f"  比較範例 1: nums=[1,2] → {r1}")
    r2 = subsets([1, 2, 3])
    print(f"  比較範例 2: nums=[1,2,3] → {len(r2)} 個子集")
    assert len(r2) == 8
    r3 = subsets([])
    print(f"  比較範例 3: nums=[] → {r3}")
    assert r3 == [[]]

    # ==================================================================
    # Section 3: 排列型 (Permutations)
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 3: 排列型 (Permutations)")
    print("=" * 70)

    # ---------- 3.1 Permutations ----------
    print("\n--- 3.1 Permutations (LeetCode 46) ---")

    # 範例 1: nums = [1,2,3]
    print("\n範例 1: nums = [1,2,3]")
    print("""
  Decision Tree (used[] 陣列控制):
                          []
                 /         |         \\
              [1]         [2]        [3]
             / \\        /   \\       / \\
          [1,2][1,3]  [2,1][2,3] [3,1][3,2]
           |    |      |    |     |    |
        [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

  Trace:
  path=[], used=[F,F,F]
    i=0: 選 1, path=[1], used=[T,F,F]
      i=0: used → skip
      i=1: 選 2, path=[1,2], used=[T,T,F]
        i=0,1: used → skip
        i=2: 選 3, path=[1,2,3] → 收集!
        撤銷 3
      撤銷 2
      i=2: 選 3, path=[1,3], used=[T,F,T]
        i=1: 選 2, path=[1,3,2] → 收集!
        撤銷 2
      撤銷 3
    撤銷 1
    (i=1, i=2 類似...)
""")
    result = permutations([1, 2, 3], verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 6  # 3!

    # 範例 2: nums = [0,1]
    print("\n範例 2: nums = [0,1]")
    print("""
  Decision Tree:
       []
      /   \\
    [0]   [1]
     |     |
   [0,1] [1,0]
""")
    result = permutations([0, 1])
    print(f"  結果: {result}")
    assert len(result) == 2

    # 範例 3: nums = [1]
    print("\n範例 3: nums = [1]")
    result = permutations([1])
    print(f"  結果: {result}")
    assert result == [[1]]

    # ---------- 3.2 Permutations II ----------
    print("\n--- 3.2 Permutations II with duplicates (LeetCode 47) ---")

    # 範例 1: nums = [1,1,2]
    print("\n範例 1: nums = [1,1,2]")
    print("""
  排序後: [1,1,2]
  Decision Tree (剪枝: 相同值前一個沒用就跳過):
                          []
                 /         |          \\
              [1]         [1]←跳過    [2]
             / \\                     /
          [1,1] [1,2]             [2,1]
           |      |                 |
        [1,1,2] [1,2,1]         [2,1,1]

  剪枝邏輯:
  - 第一層 i=1: nums[1]=1==nums[0]=1, used[0]=False → 跳過!
  - 在 [2] 分支下 i=1: nums[1]=1==nums[0]=1, used[0]=False → 跳過!
    所以 [2,1,...] 只會走 i=0 的 1
  結果只有 3 個 (而不是 6 個)
""")
    result = permutations_unique([1, 1, 2], verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 3

    # 範例 2: nums = [1,2,2]
    print("\n範例 2: nums = [1,2,2]")
    result = permutations_unique([1, 2, 2])
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 3

    # 範例 3: nums = [2,2,2]
    print("\n範例 3: nums = [2,2,2]")
    result = permutations_unique([2, 2, 2])
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 1  # 只有 [2,2,2]
    assert result == [[2, 2, 2]]

    # ---------- 3.3 Next Permutation ----------
    print("\n--- 3.3 Next Permutation (LeetCode 31) ---")

    # 範例 1: [1,2,3] → [1,3,2]
    print("\n範例 1: [1,2,3] → ?")
    print("""
  Step-by-step:
  原始: [1,2,3]
  Step 1: 從右找下降位 → i=1 (nums[1]=2 < nums[2]=3)
  Step 2: 從右找第一個 > 2 的 → j=2 (nums[2]=3)
          交換 nums[1],nums[2] → [1,3,2]
  Step 3: 反轉 index 2 到末尾 → [1,3,2] (只有一個元素，不變)
  結果: [1,3,2]
""")
    nums = [1, 2, 3]
    next_permutation(nums, verbose=True)
    print(f"  結果: {nums}")
    assert nums == [1, 3, 2]

    # 範例 2: [3,2,1] → [1,2,3] (最大 → 最小)
    print("\n範例 2: [3,2,1] → ? (已是最大排列)")
    print("""
  Step-by-step:
  原始: [3,2,1]
  Step 1: 從右找下降位 → i=-1 (完全遞減，無下降位)
  Step 2: 跳過 (i<0)
  Step 3: 反轉整個陣列 → [1,2,3]
  結果: [1,2,3] (回到最小排列)
""")
    nums = [3, 2, 1]
    next_permutation(nums, verbose=True)
    print(f"  結果: {nums}")
    assert nums == [1, 2, 3]

    # 範例 3: [1,5,8,4,7,6,5,3,1] → [1,5,8,5,1,3,4,6,7]
    print("\n範例 3: [1,5,8,4,7,6,5,3,1]")
    print("""
  Step-by-step:
  原始: [1,5,8,4,7,6,5,3,1]
  Step 1: 從右找下降位 → i=3 (nums[3]=4 < nums[4]=7)
  Step 2: 從右找 >4 → j=6 (nums[6]=5), 交換 → [1,5,8,5,7,6,4,3,1]
  Step 3: 反轉 index 4~8 → [1,5,8,5,1,3,4,6,7]
""")
    nums = [1, 5, 8, 4, 7, 6, 5, 3, 1]
    next_permutation(nums, verbose=True)
    print(f"  結果: {nums}")
    assert nums == [1, 5, 8, 5, 1, 3, 4, 6, 7]

    # ==================================================================
    # Section 4: 組合型 (Combinations)
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 4: 組合型 (Combinations)")
    print("=" * 70)

    # ---------- 4.1 Combinations ----------
    print("\n--- 4.1 Combinations C(n,k) (LeetCode 77) ---")

    # 範例 1: n=4, k=2
    print("\n範例 1: n=4, k=2 → C(4,2)=6")
    print("""
  Decision Tree (start index 遞增):
                      []
              /      /     \\     \\
            [1]    [2]     [3]   [4]←剪枝(剩0個不夠)
           / | \\    | \\     |
       [1,2][1,3][1,4][2,3][2,4] [3,4]

  Trace:
  path=[], start=1
    選 1: path=[1], start=2
      選 2: path=[1,2] → 收集! 撤銷 2
      選 3: path=[1,3] → 收集! 撤銷 3
      選 4: path=[1,4] → 收集! 撤銷 4
    撤銷 1
    選 2: path=[2], start=3
      選 3: path=[2,3] → 收集! 撤銷 3
      選 4: path=[2,4] → 收集! 撤銷 4
    撤銷 2
    選 3: path=[3], start=4
      選 4: path=[3,4] → 收集! 撤銷 4
    撤銷 3
    選 4: path=[4] → 剪枝! 還需 1 個但沒有更多了
""")
    result = combine(4, 2, verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 6

    # 範例 2: n=5, k=3
    print("\n範例 2: n=5, k=3 → C(5,3)=10")
    result = combine(5, 3)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 10

    # 範例 3: n=3, k=1
    print("\n範例 3: n=3, k=1 → C(3,1)=3")
    result = combine(3, 1)
    print(f"  結果: {result}")
    assert result == [[1], [2], [3]]

    # ---------- 4.2 Combination Sum ----------
    print("\n--- 4.2 Combination Sum (LeetCode 39) - 可重複使用 ---")

    # 範例 1: candidates=[2,3,6,7], target=7
    print("\n範例 1: candidates=[2,3,6,7], target=7")
    print("""
  Decision Tree (元素可重複使用):
                           [], remain=7
                   /        |       |      \\
              [2],r=5   [3],r=4  [6],r=1  [7],r=0 ✓
             /   |  \\     |  \\
        [2,2],r=3 [2,3],r=2 ...  [3,3],r=1
          / \\       |              (>1,停)
    [2,2,2],r=1 [2,2,3],r=0 ✓  [2,3,?]...
       |
  [2,2,2,?]  (2>1,不行; 3>1,不行)  停

  結果: [2,2,3], [7]
""")
    result = combination_sum([2, 3, 6, 7], 7, verbose=True)
    print(f"  結果: {result}")
    assert sorted([sorted(x) for x in result]) == [[2, 2, 3], [7]]

    # 範例 2: candidates=[2,3,5], target=8
    print("\n範例 2: candidates=[2,3,5], target=8")
    print("""
  Trace 重點:
  [2,2,2,2] sum=8 ✓
  [2,3,3]   sum=8 ✓
  [3,5]     sum=8 ✓
""")
    result = combination_sum([2, 3, 5], 8, verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 3

    # 範例 3: candidates=[2], target=1
    print("\n範例 3: candidates=[2], target=1 → 無解")
    result = combination_sum([2], 1)
    print(f"  結果: {result}")
    assert result == []

    # ---------- 4.3 Combination Sum II ----------
    print("\n--- 4.3 Combination Sum II (LeetCode 40) - 不可重複 + 有重複元素 ---")

    # 範例 1: candidates=[10,1,2,7,6,1,5], target=8
    print("\n範例 1: candidates=[10,1,2,7,6,1,5], target=8")
    print("  排序後: [1,1,2,5,6,7,10]")
    print("""
  Decision Tree (關鍵: 同層跳過重複):
  path=[], remain=8
    選 1(idx=0): path=[1], r=7
      選 1(idx=1): path=[1,1], r=6
        選 2: path=[1,1,2], r=4 → 選 5: [1,1,2,5]?? r=-1 超過
                                   但 r=4: 選 5 → r=-1 停
        但實際: [1,1,6] sum=8 ✓
      選 2(idx=2): path=[1,2], r=5 → [1,2,5] sum=8 ✓
      選 7(idx=5): path=[1,7] sum=8 ✓
    選 1(idx=1): 跳過! (同層重複)
    選 2(idx=2): path=[2], r=6 → [2,6] sum=8 ✓
""")
    result = combination_sum2([10, 1, 2, 7, 6, 1, 5], 8, verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 4

    # 範例 2: candidates=[2,5,2,1,2], target=5
    print("\n範例 2: candidates=[2,5,2,1,2], target=5")
    print("  排序後: [1,2,2,2,5]")
    result = combination_sum2([2, 5, 2, 1, 2], 5)
    print(f"  結果: {result}")
    # [1,2,2], [5]
    assert len(result) == 2

    # 範例 3: candidates=[1,1,1,1], target=2
    print("\n範例 3: candidates=[1,1,1,1], target=2")
    result = combination_sum2([1, 1, 1, 1], 2)
    print(f"  結果: {result}")
    assert result == [[1, 1]]

    # ---------- 4.4 Letter Combinations ----------
    print("\n--- 4.4 Letter Combinations of Phone Number (LeetCode 17) ---")

    # 範例 1: digits="23"
    print('\n範例 1: digits="23"')
    print("""
  2 → "abc", 3 → "def"
  Decision Tree:
                   ""
              /    |    \\
            "a"   "b"   "c"
           / | \\  / | \\  / | \\
         ad ae af bd be bf cd ce cf

  Trace:
  idx=0, digit='2', letters='abc'
    選 'a': path=['a'], idx=1, digit='3', letters='def'
      選 'd': path=['a','d'] → "ad" ✓
      選 'e': → "ae" ✓
      選 'f': → "af" ✓
    選 'b': ...
    選 'c': ...
""")
    result = letter_combinations("23", verbose=True)
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 9  # 3 * 3

    # 範例 2: digits="7"
    print('\n範例 2: digits="7"')
    print('  7 → "pqrs" (4 個字母)')
    result = letter_combinations("7")
    print(f"  結果: {result}")
    assert result == ["p", "q", "r", "s"]

    # 範例 3: digits="29"
    print('\n範例 3: digits="29"')
    print('  2 → "abc", 9 → "wxyz" → 3*4=12 組合')
    result = letter_combinations("29")
    print(f"  結果 ({len(result)} 個): {result}")
    assert len(result) == 12

    # ==================================================================
    # Section 5: 棋盤型 (Board / Grid Backtracking)
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 5: 棋盤型 (Board / Grid Backtracking)")
    print("=" * 70)

    # ---------- 5.1 N-Queens ----------
    print("\n--- 5.1 N-Queens (LeetCode 51) ---")

    # 範例 1: n=4
    print("\n範例 1: n=4 (4-Queens)")
    print("""
  棋盤 (解 1):            棋盤 (解 2):
    0 1 2 3                 0 1 2 3
  0 . Q . .  queens=[1,3,0,2]  0 . . Q .  queens=[2,0,3,1]
  1 . . . Q               1 Q . . .
  2 Q . . .               2 . . . Q
  3 . . Q .               3 . Q . .

  Trace (找第一個解):
  row=0 col=0 → row=1 全部衝突 → 回溯
  row=0 col=1 → row=1 col=3 → row=2 col=0 → row=3 col=2 → 找到!
""")
    result = solve_n_queens(4, verbose=True)
    print(f"  找到 {len(result)} 個解")
    for idx, board in enumerate(result):
        print(f"  解 {idx + 1}:")
        for row in board:
            print(f"    {row}")
    assert len(result) == 2

    # 範例 2: n=1
    print("\n範例 2: n=1")
    result = solve_n_queens(1)
    print(f"  結果: {result}")
    assert result == [["Q"]]

    # 範例 3: n=5
    print("\n範例 3: n=5")
    result = solve_n_queens(5)
    print(f"  找到 {len(result)} 個解")
    for idx, board in enumerate(result):
        print(f"  解 {idx + 1}: {[''.join([str(c) for c, ch in enumerate(row) if ch == 'Q']) for row in board]}")
    assert len(result) == 10

    # ---------- 5.2 Sudoku Solver ----------
    print("\n--- 5.2 Sudoku Solver (LeetCode 37) ---")

    print("\n範例: 經典數獨")
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    print("  題目:")
    for r in board:
        print(f"    {' '.join(r)}")

    solved = solve_sudoku(board, verbose=False)  # verbose=True 輸出太多
    print(f"\n  已解: {solved}")
    print("  答案:")
    for r in board:
        print(f"    {' '.join(r)}")
    assert solved
    # 驗證每行都有 1-9
    for r in board:
        assert set(r) == set(str(i) for i in range(1, 10))

    # ---------- 5.3 Word Search ----------
    print("\n--- 5.3 Word Search (LeetCode 79) ---")

    # 範例 1: 找 "ABCCED"
    print('\n範例 1: 找 "ABCCED"')
    grid = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    print("  Board:")
    for row in grid:
        print(f"    {row}")
    print("""
  Trace:
  起點 (0,0)='A' 匹配 word[0]
    → (0,1)='B' 匹配 word[1]
      → (0,2)='C' 匹配 word[2]
        → (1,2)='C' 匹配 word[3]
          → (2,2)='E' 匹配 word[4]
            → (2,1)='D' 匹配 word[5] → 找到!
""")
    result = word_search(
        [row[:] for row in grid], "ABCCED", verbose=True)
    print(f"  結果: {result}")
    assert result is True

    # 範例 2: 找 "SEE"
    print('\n範例 2: 找 "SEE"')
    grid2 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    print("""
  Trace:
  起點 (1,3)='S' 匹配 word[0]
    → (2,3)='E' 匹配 word[1]
      → (2,2)='E' 匹配 word[2] → 找到!
""")
    result = word_search(
        [row[:] for row in grid2], "SEE", verbose=True)
    print(f"  結果: {result}")
    assert result is True

    # 範例 3: 找 "ABCB" (不存在，因為不能重複使用同一格)
    print('\n範例 3: 找 "ABCB" (需要重複使用 B → False)')
    grid3 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    result = word_search(
        [row[:] for row in grid3], "ABCB", verbose=True)
    print(f"  結果: {result}")
    assert result is False

    # ==================================================================
    # Section 6: 子集 vs 排列 vs 組合 總比較
    # ==================================================================
    print("\n" + "=" * 70)
    print(" Section 6: 子集 vs 排列 vs 組合 比較總結")
    print("=" * 70)
    print("""
  ┌──────────────┬──────────────────┬──────────────────┬──────────────────┐
  │              │ Subsets 子集     │ Permutations 排列│ Combinations 組合│
  ├──────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ 順序重要？   │ 否               │ 是               │ 否               │
  │ 選幾個？     │ 任意 (0~n)       │ 全部 n 個        │ 恰好 k 個        │
  │ 避免重複     │ start index      │ used[] 陣列      │ start index      │
  │ 迴圈起點     │ range(start, n)  │ range(0, n)      │ range(start, n)  │
  │ 收集時機     │ 每個節點         │ len(path) == n   │ len(path) == k   │
  │ 結果數量     │ 2^n              │ n!               │ C(n,k)           │
  └──────────────┴──────────────────┴──────────────────┴──────────────────┘

  模板對比（以 nums = [1,2,3] 為例）:

  # Subsets 子集                   # Permutations 排列
  def backtrack(start, path):      def backtrack(path):
      result.append(path[:])           if len(path) == n:
      for i in range(start, n):            result.append(path[:])
          path.append(nums[i])             return
          backtrack(i+1, path)         for i in range(n):
          path.pop()                       if used[i]: continue
                                           used[i] = True
                                           path.append(nums[i])
  # Combinations 組合                      backtrack(path)
  def backtrack(start, path):              path.pop()
      if len(path) == k:                   used[i] = False
          result.append(path[:])
          return
      for i in range(start, n):
          path.append(nums[i])
          backtrack(i+1, path)
          path.pop()

  去重邏輯比較:
  ┌─────────────────────────────────────────────────────────────────┐
  │ Subsets II / Combination Sum II:                                │
  │   nums.sort()                                                   │
  │   if i > start and nums[i] == nums[i-1]: continue              │
  │   意義: 同一層不選相同值                                        │
  ├─────────────────────────────────────────────────────────────────┤
  │ Permutations II:                                                │
  │   nums.sort()                                                   │
  │   if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue│
  │   意義: 相同值必須按順序使用（前一個沒用就不用後面的）          │
  └─────────────────────────────────────────────────────────────────┘

  面試決策流程:
  ┌──────────────────────────────┐
  │ 題目要「所有可能的...」？    │
  │          ↓ 是               │
  │ 順序重要嗎？                │
  │   ├─ 是 → Permutation       │
  │   └─ 否                     │
  │       ├─ 選幾個？            │
  │       │  ├─ 任意 → Subset    │
  │       │  ├─ k 個 → Combination│
  │       │  └─ 和=target → CombSum│
  │       └─ 有重複元素？        │
  │          ├─ 有 → 排序+跳過   │
  │          └─ 無 → 直接套模板  │
  └──────────────────────────────┘
""")

    print("=" * 70)
    print(" 全部測試通過！All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
