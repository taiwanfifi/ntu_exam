"""
==============================================================================
  LeetCode 教學筆記 #04 — Stack, Queue & Monotonic Stack
  （堆疊、佇列與單調堆疊）

  Target: Google / NVIDIA 面試準備
  Level : Beginner → Intermediate（從零開始，逐步進階）
  Style : 每題 3 組 step-by-step 數值追蹤，看懂 stack/queue 每一步的變化

  Usage : python 04_Stack_Queue_Monotonic.py
==============================================================================
"""

from collections import deque
from typing import List, Optional


# ============================================================================
#  SECTION 1: 基礎 Stack（Basic Stack）
# ============================================================================

# ----------------------------------------------------------------------------
#  1-1  Valid Parentheses（有效括號）— LeetCode 20
#
#  觀念：遇到左括號 push，遇到右括號 pop 並比對。
#        最後 stack 為空 → 合法。
#
#  Time: O(n)   Space: O(n)
# ----------------------------------------------------------------------------

def is_valid_parentheses(s: str, verbose: bool = False) -> bool:
    """
    判斷括號字串是否合法。
    mapping: 右括號 → 對應的左括號
    """
    mapping = {')': '(', '}': '{', ']': '['}
    stack = []

    for i, char in enumerate(s):
        if char in mapping:                       # 右括號
            top = stack.pop() if stack else '#'   # stack 空就用哨兵
            if top != mapping[char]:
                if verbose:
                    print(f"  Step {i+1}: char='{char}' → top='{top}' 不匹配 → return False")
                return False
            if verbose:
                print(f"  Step {i+1}: char='{char}' → matches '{top}' → pop → stack={stack}")
        else:                                     # 左括號
            stack.append(char)
            if verbose:
                print(f"  Step {i+1}: char='{char}' → push → stack={stack}")

    result = len(stack) == 0
    if verbose:
        print(f"  Final: stack={stack} → {'Valid' if result else 'Invalid'}")
    return result


def demo_valid_parentheses():
    print("=" * 70)
    print("1-1  Valid Parentheses（有效括號）— LeetCode 20")
    print("=" * 70)

    # 範例 1: s = "({[]})"
    # Step 1: char='(' → push → stack=['(']
    # Step 2: char='{' → push → stack=['(', '{']
    # Step 3: char='[' → push → stack=['(', '{', '[']
    # Step 4: char=']' → matches '[' → pop → stack=['(', '{']
    # Step 5: char='}' → matches '{' → pop → stack=['(']
    # Step 6: char=')' → matches '(' → pop → stack=[]
    # Result: stack is empty → Valid
    print("\n範例 1: s = '({[]})'")
    assert is_valid_parentheses("({[]})", verbose=True) == True

    # 範例 2: s = "(]"
    # Step 1: char='(' → push → stack=['(']
    # Step 2: char=']' → top='(' 不匹配 ']' 需要 '[' → Invalid
    print("\n範例 2: s = '(]'")
    assert is_valid_parentheses("(]", verbose=True) == False

    # 範例 3: s = "{[]}{}"
    # 六步：push { → push [ → pop [ → pop { → push { → pop { → empty → Valid
    print("\n範例 3: s = '{[]}{}'")
    assert is_valid_parentheses("{[]}{}", verbose=True) == True
    print()


# ----------------------------------------------------------------------------
#  1-2  Min Stack（最小堆疊）— LeetCode 155
#
#  觀念：用一個輔助 stack (min_stack) 同步記錄「到目前為止的最小值」。
#        push/pop/top/getMin 全部 O(1)。
# ----------------------------------------------------------------------------

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []       # 輔助 stack：紀錄各層最小值

    def push(self, val: int) -> None:
        self.stack.append(val)
        # 若 min_stack 為空 或 val <= 當前最小 → push 進 min_stack
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

    def __repr__(self):
        return f"stack={self.stack}, min_stack={self.min_stack}"


def demo_min_stack():
    print("=" * 70)
    print("1-2  Min Stack（最小堆疊）— LeetCode 155")
    print("=" * 70)

    # 範例 1: push(-2), push(0), push(-3) → getMin=-3, pop, getMin=-2
    print("\n範例 1: push -2, 0, -3 → getMin → pop → getMin")
    ms = MinStack()
    for val in [-2, 0, -3]:
        ms.push(val)
        print(f"  push({val}) → {ms}")
    print(f"  getMin() = {ms.getMin()}")       # -3
    assert ms.getMin() == -3
    ms.pop()
    print(f"  pop()    → {ms}")
    print(f"  getMin() = {ms.getMin()}")       # -2
    assert ms.getMin() == -2

    # 範例 2: push(1), push(1), push(2) → getMin=1, pop, getMin=1
    print("\n範例 2: push 1, 1, 2 → 重複最小值處理")
    ms2 = MinStack()
    for val in [1, 1, 2]:
        ms2.push(val)
        print(f"  push({val}) → {ms2}")
    print(f"  getMin() = {ms2.getMin()}")      # 1
    assert ms2.getMin() == 1
    ms2.pop()
    print(f"  pop()    → {ms2}")
    print(f"  getMin() = {ms2.getMin()}")      # 1 (還有一個 1)
    assert ms2.getMin() == 1

    # 範例 3: push(5), push(3), push(7), pop, pop → getMin=5
    print("\n範例 3: push 5, 3, 7 → pop 兩次")
    ms3 = MinStack()
    for val in [5, 3, 7]:
        ms3.push(val)
        print(f"  push({val}) → {ms3}")
    ms3.pop(); print(f"  pop()    → {ms3}")  # 移除 7
    ms3.pop(); print(f"  pop()    → {ms3}")  # 移除 3
    print(f"  getMin() = {ms3.getMin()}")     # 5
    assert ms3.getMin() == 5
    print()


# ----------------------------------------------------------------------------
#  1-3  Evaluate Reverse Polish Notation（逆波蘭表示法）— LeetCode 150
#
#  觀念：遇到數字 push；遇到運算子 pop 兩個數，計算後 push 結果。
#  注意：除法向零取整（Python 需用 int(a/b) 而非 a//b）。
#
#  Time: O(n)   Space: O(n)
# ----------------------------------------------------------------------------

def eval_rpn(tokens: List[str], verbose: bool = False) -> int:
    stack = []
    ops = {'+', '-', '*', '/'}

    for i, t in enumerate(tokens):
        if t in ops:
            b = stack.pop()           # 注意順序：b 先 pop
            a = stack.pop()
            if   t == '+': res = a + b
            elif t == '-': res = a - b
            elif t == '*': res = a * b
            else:          res = int(a / b)   # 向零取整
            stack.append(res)
            if verbose:
                print(f"  Step {i+1}: token='{t}' → {a} {t} {b} = {res} → stack={stack}")
        else:
            stack.append(int(t))
            if verbose:
                print(f"  Step {i+1}: token='{t}' → push {int(t)} → stack={stack}")

    return stack[0]


def demo_eval_rpn():
    print("=" * 70)
    print("1-3  Evaluate Reverse Polish Notation — LeetCode 150")
    print("=" * 70)

    # 範例 1: ["2","1","+","3","*"] → (2+1)*3 = 9
    print('\n範例 1: ["2","1","+","3","*"] → (2+1)*3 = 9')
    r1 = eval_rpn(["2", "1", "+", "3", "*"], verbose=True)
    print(f"  Result = {r1}")
    assert r1 == 9

    # 範例 2: ["4","13","5","/","+"] → 4+(13/5)=4+2=6
    print('\n範例 2: ["4","13","5","/","+"] → 4+(13/5) = 6')
    r2 = eval_rpn(["4", "13", "5", "/", "+"], verbose=True)
    print(f"  Result = {r2}")
    assert r2 == 6

    # 範例 3: ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    # = ((10*(6/((9+3)*-11)))+17)+5 = 22
    print('\n範例 3: 較長的表達式 → 22')
    r3 = eval_rpn(["10","6","9","3","+","-11","*","/","*","17","+","5","+"], verbose=True)
    print(f"  Result = {r3}")
    assert r3 == 22
    print()


# ============================================================================
#  SECTION 2: 單調 Stack（Monotonic Stack）
# ============================================================================

# ----------------------------------------------------------------------------
#  2-1  Next Greater Element I — LeetCode 496
#
#  觀念：從右往左掃描 nums2，維護一個「單調遞減 stack」（bottom→top 遞減）。
#        對每個元素，把 stack 裡比它小的都 pop 掉，stack 頂就是 next greater。
#
#  Time: O(n+m)   Space: O(n)
# ----------------------------------------------------------------------------

def next_greater_element(nums1: List[int], nums2: List[int],
                         verbose: bool = False) -> List[int]:
    stack = []
    nge = {}  # num → next greater element

    # 從右到左掃描 nums2
    for i in range(len(nums2) - 1, -1, -1):
        val = nums2[i]
        # 把 stack 裡 <= val 的都 pop 掉
        while stack and stack[-1] <= val:
            stack.pop()
        nge[val] = stack[-1] if stack else -1
        stack.append(val)
        if verbose:
            print(f"  i={i}, val={val} → nge[{val}]={nge[val]}, stack={stack}")

    result = [nge[x] for x in nums1]
    return result


def demo_next_greater_element():
    print("=" * 70)
    print("2-1  Next Greater Element I（下一個更大元素）— LeetCode 496")
    print("=" * 70)

    # 範例 1: nums1=[4,1,2], nums2=[1,3,4,2]
    # 從右到左掃 nums2：
    #   i=3, val=2 → stack=[] → nge[2]=-1, stack=[2]
    #   i=2, val=4 → pop 2 → stack=[] → nge[4]=-1, stack=[4]
    #   i=1, val=3 → stack=[4], 4>3 → nge[3]=4, stack=[4,3]
    #   i=0, val=1 → stack=[4,3], 3>1 → nge[1]=3, stack=[4,3,1]
    # nums1=[4,1,2] → [-1, 3, -1]
    print("\n範例 1: nums1=[4,1,2], nums2=[1,3,4,2]")
    r1 = next_greater_element([4,1,2], [1,3,4,2], verbose=True)
    print(f"  Result = {r1}")
    assert r1 == [-1, 3, -1]

    # 範例 2: nums1=[2,4], nums2=[1,2,3,4]
    print("\n範例 2: nums1=[2,4], nums2=[1,2,3,4]")
    r2 = next_greater_element([2,4], [1,2,3,4], verbose=True)
    print(f"  Result = {r2}")
    assert r2 == [3, -1]

    # 範例 3: nums1=[1,3,5], nums2=[6,5,4,3,2,1,7]
    print("\n範例 3: nums1=[1,3,5], nums2=[6,5,4,3,2,1,7]")
    r3 = next_greater_element([1,3,5], [6,5,4,3,2,1,7], verbose=True)
    print(f"  Result = {r3}")
    assert r3 == [7, 7, 7]
    print()


# ----------------------------------------------------------------------------
#  2-2  Daily Temperatures（每日溫度）— LeetCode 739
#
#  觀念：stack 存 index，維持「單調遞減」（溫度從 bottom→top 遞減）。
#        遇到更高溫度時，pop 出那些「等待更高溫」的 index，算天數差。
#
#  為什麼用 Monotonic Stack？
#  → 暴力法 O(n^2)：每天往後找第一個更高溫。
#  → Monotonic Stack O(n)：每個元素最多 push/pop 各一次。
#
#  Time: O(n)   Space: O(n)
# ----------------------------------------------------------------------------

def daily_temperatures(temperatures: List[int],
                       verbose: bool = False) -> List[int]:
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存 index，stack 內溫度遞減

    for i in range(n):
        # 當前溫度 > stack 頂的溫度 → 找到答案
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
            if verbose:
                print(f"    pop idx={prev_idx}(temp={temperatures[prev_idx]}): "
                      f"answer={i}-{prev_idx}={i - prev_idx}")
        stack.append(i)
        if verbose:
            stack_temps = [temperatures[j] for j in stack]
            print(f"  Day {i}: temp={temperatures[i]} → push idx={i} → "
                  f"stack(idx)={stack} stack(temp)={stack_temps}")

    return result


def demo_daily_temperatures():
    print("=" * 70)
    print("2-2  Daily Temperatures（每日溫度）— LeetCode 739")
    print("=" * 70)

    # 範例 1: [73,74,75,71,69,72,76,73]
    print("\n範例 1: temperatures = [73,74,75,71,69,72,76,73]")
    r1 = daily_temperatures([73,74,75,71,69,72,76,73], verbose=True)
    print(f"  Result = {r1}")
    assert r1 == [1,1,4,2,1,1,0,0]

    # 範例 2: [30,40,50,60]  — 持續上升
    print("\n範例 2: temperatures = [30,40,50,60] (持續上升)")
    r2 = daily_temperatures([30,40,50,60], verbose=True)
    print(f"  Result = {r2}")
    assert r2 == [1,1,1,0]

    # 範例 3: [60,50,40,30] — 持續下降
    print("\n範例 3: temperatures = [60,50,40,30] (持續下降)")
    r3 = daily_temperatures([60,50,40,30], verbose=True)
    print(f"  Result = {r3}")
    assert r3 == [0,0,0,0]
    print()


# ----------------------------------------------------------------------------
#  2-3  Largest Rectangle in Histogram（柱狀圖最大矩形）— LeetCode 84
#
#  觀念：維護「單調遞增 stack」（bottom→top 高度遞增）。
#        當遇到較矮的柱子時，pop 出較高的柱子並計算面積。
#        pop 出的柱子高度 h，寬度 = 左邊界（新 stack 頂+1）到右邊界（i-1）。
#
#  關鍵公式：width = i - stack[-1] - 1  (stack 非空時)
#            width = i                    (stack 為空時)
#
#  Time: O(n)   Space: O(n)
#
#  Google 面試高頻題！
# ----------------------------------------------------------------------------

def largest_rectangle_histogram(heights: List[int],
                                verbose: bool = False) -> int:
    stack = []       # 存 index，高度單調遞增
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        # 用 0 作為哨兵，確保最後所有柱子都會被 pop
        cur_h = heights[i] if i < n else 0

        while stack and cur_h < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            area = h * w
            max_area = max(max_area, area)
            if verbose:
                print(f"    pop: h={h}, w={w}, area={area}, max_area={max_area}")

        stack.append(i)
        if verbose:
            stack_h = [heights[j] if j < n else 0 for j in stack]
            print(f"  i={i}, cur_h={cur_h} → stack(idx)={stack} "
                  f"stack(h)={stack_h}")

    return max_area


def demo_largest_rectangle():
    print("=" * 70)
    print("2-3  Largest Rectangle in Histogram — LeetCode 84")
    print("    （Google 面試高頻！）")
    print("=" * 70)

    # 範例 1: [2,1,5,6,2,3] → 最大矩形面積 10 (高5,寬2 在 index 2-3)
    print("\n範例 1: heights = [2,1,5,6,2,3] → 10")
    r1 = largest_rectangle_histogram([2,1,5,6,2,3], verbose=True)
    print(f"  Max Area = {r1}")
    assert r1 == 10

    # 範例 2: [2,4] → 最大面積 4 (高2,寬2 或 高4,寬1)
    print("\n範例 2: heights = [2,4] → 4")
    r2 = largest_rectangle_histogram([2,4], verbose=True)
    print(f"  Max Area = {r2}")
    assert r2 == 4

    # 範例 3: [1,2,3,4,5] → 遞增序列 → 最大面積 9 (高3,寬3)
    print("\n範例 3: heights = [1,2,3,4,5] → 9")
    r3 = largest_rectangle_histogram([1,2,3,4,5], verbose=True)
    print(f"  Max Area = {r3}")
    assert r3 == 9
    print()


# ============================================================================
#  SECTION 3: Stack 模擬型（Stack-Based Simulation）
# ============================================================================

# ----------------------------------------------------------------------------
#  3-1  Decode String（解碼字串）— LeetCode 394
#
#  觀念：遇到 '[' → 把目前的字串和數字 push 進 stack
#        遇到 ']' → pop 出來組合
#        用兩個資訊：(之前的字串, 重複次數)
#
#  Time: O(output length)   Space: O(n)
# ----------------------------------------------------------------------------

def decode_string(s: str, verbose: bool = False) -> str:
    stack = []           # 存 (prev_string, repeat_count)
    current_str = ""
    current_num = 0

    for i, ch in enumerate(s):
        if ch.isdigit():
            current_num = current_num * 10 + int(ch)
            if verbose:
                print(f"  Step {i+1}: ch='{ch}' (digit) → current_num={current_num}")
        elif ch == '[':
            # 把目前狀態存進 stack
            stack.append((current_str, current_num))
            current_str = ""
            current_num = 0
            if verbose:
                print(f"  Step {i+1}: ch='[' → push ('{stack[-1][0]}', {stack[-1][1]}) "
                      f"→ reset → stack={stack}")
        elif ch == ']':
            # pop 出來組合
            prev_str, num = stack.pop()
            current_str = prev_str + current_str * num
            if verbose:
                print(f"  Step {i+1}: ch=']' → pop ('{prev_str}', {num}) "
                      f"→ current_str='{current_str}'")
        else:
            current_str += ch
            if verbose:
                print(f"  Step {i+1}: ch='{ch}' (letter) → current_str='{current_str}'")

    return current_str


def demo_decode_string():
    print("=" * 70)
    print("3-1  Decode String（解碼字串）— LeetCode 394")
    print("=" * 70)

    # 範例 1: "3[a]2[bc]" → "aaabcbc"
    print('\n範例 1: s = "3[a]2[bc]" → "aaabcbc"')
    r1 = decode_string("3[a]2[bc]", verbose=True)
    print(f"  Result = '{r1}'")
    assert r1 == "aaabcbc"

    # 範例 2: "3[a2[c]]" → "accaccacc" (巢狀 nested)
    # 追蹤：
    #   3 → num=3
    #   [ → push("", 3), reset
    #   a → str="a"
    #   2 → num=2
    #   [ → push("a", 2), reset
    #   c → str="c"
    #   ] → pop("a",2) → str = "a" + "c"*2 = "acc"
    #   ] → pop("",3) → str = "" + "acc"*3 = "accaccacc"
    print('\n範例 2: s = "3[a2[c]]" → "accaccacc" (巢狀結構)')
    r2 = decode_string("3[a2[c]]", verbose=True)
    print(f"  Result = '{r2}'")
    assert r2 == "accaccacc"

    # 範例 3: "2[ab3[d]]ef" → "abdddabdddef"
    print('\n範例 3: s = "2[ab3[d]]ef" → "abdddabdddef"')
    r3 = decode_string("2[ab3[d]]ef", verbose=True)
    print(f"  Result = '{r3}'")
    assert r3 == "abdddabdddef"
    print()


# ----------------------------------------------------------------------------
#  3-2  Basic Calculator II — LeetCode 227
#
#  觀念：stack 存數字。遇到 +/- → 直接 push（帶正負號）。
#        遇到 * / → 先 pop 出來算完再 push。最後 sum(stack)。
#        這樣自然處理了「先乘除後加減」。
#
#  Time: O(n)   Space: O(n)
# ----------------------------------------------------------------------------

def basic_calculator_ii(s: str, verbose: bool = False) -> int:
    stack = []
    num = 0
    op = '+'          # 前一個運算子（初始為 +）

    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)

        # 遇到運算子或到尾巴 → 根據「前一個運算子」處理
        if ch in '+-*/' or i == len(s) - 1:
            if   op == '+': stack.append(num)
            elif op == '-': stack.append(-num)
            elif op == '*': stack.append(stack.pop() * num)
            elif op == '/': stack.append(int(stack.pop() / num))

            if verbose:
                print(f"  i={i}: op='{op}', num={num} → stack={stack}")

            op = ch
            num = 0

    result = sum(stack)
    if verbose:
        print(f"  sum(stack) = sum({stack}) = {result}")
    return result


def demo_basic_calculator_ii():
    print("=" * 70)
    print("3-2  Basic Calculator II — LeetCode 227")
    print("=" * 70)

    # 範例 1: "3+2*2" → 7
    # op='+', num=3 → stack=[3]
    # op='+', num=2 → stack=[3,2]  → 遇到 * → 暫不處理
    # op='*', num=2 → stack=[3, 2*2=4] → sum=7
    print('\n範例 1: s = "3+2*2" → 7')
    r1 = basic_calculator_ii("3+2*2", verbose=True)
    print(f"  Result = {r1}")
    assert r1 == 7

    # 範例 2: " 3/2 " → 1
    print('\n範例 2: s = " 3/2 " → 1')
    r2 = basic_calculator_ii(" 3/2 ", verbose=True)
    print(f"  Result = {r2}")
    assert r2 == 1

    # 範例 3: "14-3*2+11" → 14-6+11 = 19
    # 但按照程式邏輯：op='+' push 14, op='-' push -3, 但等等遇到 * 才處理
    # 重新追蹤 → 最終 sum = 19
    print('\n範例 3: s = "14-3*2+11" → 19')
    r3 = basic_calculator_ii("14-3*2+11", verbose=True)
    print(f"  Result = {r3}")
    assert r3 == 19
    print()


# ----------------------------------------------------------------------------
#  3-3  Asteroid Collision（小行星碰撞）— LeetCode 735
#
#  觀念：正數向右飛，負數向左飛。
#        只有「stack 頂 > 0 且新來的 < 0」才會碰撞。
#        碰撞結果：大的活，小的爆，一樣大兩個都爆。
#
#  Time: O(n)   Space: O(n)
# ----------------------------------------------------------------------------

def asteroid_collision(asteroids: List[int],
                       verbose: bool = False) -> List[int]:
    stack = []

    for i, ast in enumerate(asteroids):
        alive = True
        # 碰撞條件：stack 頂正（右飛）且新來的負（左飛）
        while alive and stack and ast < 0 < stack[-1]:
            if stack[-1] < abs(ast):
                if verbose:
                    print(f"  Step {i+1}: ast={ast} vs stack_top={stack[-1]} → "
                          f"{stack[-1]} explodes")
                stack.pop()
            elif stack[-1] == abs(ast):
                if verbose:
                    print(f"  Step {i+1}: ast={ast} vs stack_top={stack[-1]} → "
                          f"both explode")
                stack.pop()
                alive = False
            else:
                if verbose:
                    print(f"  Step {i+1}: ast={ast} vs stack_top={stack[-1]} → "
                          f"{ast} explodes")
                alive = False

        if alive:
            stack.append(ast)
            if verbose:
                print(f"  Step {i+1}: ast={ast} survives → stack={stack}")

    return stack


def demo_asteroid_collision():
    print("=" * 70)
    print("3-3  Asteroid Collision（小行星碰撞）— LeetCode 735")
    print("=" * 70)

    # 範例 1: [5, 10, -5] → [5, 10]
    # 5 push, 10 push, -5 來了 vs 10 → 10>5 → -5 explodes
    print("\n範例 1: asteroids = [5, 10, -5] → [5, 10]")
    r1 = asteroid_collision([5, 10, -5], verbose=True)
    print(f"  Result = {r1}")
    assert r1 == [5, 10]

    # 範例 2: [8, -8] → []  (同大小，都爆)
    print("\n範例 2: asteroids = [8, -8] → []")
    r2 = asteroid_collision([8, -8], verbose=True)
    print(f"  Result = {r2}")
    assert r2 == []

    # 範例 3: [10, 2, -5] → [10]
    # 10 push, 2 push, -5 來了 vs 2 → 2<5 → 2 explodes
    #                         -5 vs 10 → 10>5 → -5 explodes
    print("\n範例 3: asteroids = [10, 2, -5] → [10]")
    r3 = asteroid_collision([10, 2, -5], verbose=True)
    print(f"  Result = {r3}")
    assert r3 == [10]
    print()


# ============================================================================
#  SECTION 4: Queue / Deque（佇列 / 雙端佇列）
# ============================================================================

# ----------------------------------------------------------------------------
#  4-1  Sliding Window Maximum（滑動視窗最大值）— LeetCode 239
#
#  觀念：使用「單調遞減 Deque」（front→back 遞減）。
#        Deque 存 index。
#        1) 移除超出視窗的 front
#        2) 從 back pop 掉比新元素小的（它們永遠不會是最大值了）
#        3) push 新 index 到 back
#        4) 當視窗形成（i >= k-1）→ front 就是最大值的 index
#
#  Time: O(n)   Space: O(k)
# ----------------------------------------------------------------------------

def max_sliding_window(nums: List[int], k: int,
                       verbose: bool = False) -> List[int]:
    dq = deque()   # 存 index，保持 nums[dq[0]] >= nums[dq[1]] >= ...
    result = []

    for i in range(len(nums)):
        # 1) 移除超出視窗的 front
        if dq and dq[0] < i - k + 1:
            removed = dq.popleft()
            if verbose:
                print(f"    remove front idx={removed} (out of window)")

        # 2) 從 back pop 掉比 nums[i] 小的
        while dq and nums[dq[-1]] <= nums[i]:
            popped = dq.pop()
            if verbose:
                print(f"    pop back idx={popped}(val={nums[popped]}) < {nums[i]}")

        # 3) push 新 index
        dq.append(i)

        # 4) 視窗形成時紀錄答案
        if i >= k - 1:
            result.append(nums[dq[0]])

        if verbose:
            dq_vals = [nums[j] for j in dq]
            window = nums[max(0, i-k+1):i+1]
            print(f"  i={i}, val={nums[i]} → deque(idx)={list(dq)} "
                  f"deque(val)={dq_vals} | window={window}"
                  + (f" → max={nums[dq[0]]}" if i >= k-1 else ""))

    return result


def demo_sliding_window_max():
    print("=" * 70)
    print("4-1  Sliding Window Maximum（滑動視窗最大值）— LeetCode 239")
    print("=" * 70)

    # 範例 1: nums=[1,3,-1,-3,5,3,6,7], k=3
    print("\n範例 1: nums=[1,3,-1,-3,5,3,6,7], k=3")
    r1 = max_sliding_window([1,3,-1,-3,5,3,6,7], 3, verbose=True)
    print(f"  Result = {r1}")
    assert r1 == [3,3,5,5,6,7]

    # 範例 2: nums=[1], k=1
    print("\n範例 2: nums=[1], k=1")
    r2 = max_sliding_window([1], 1, verbose=True)
    print(f"  Result = {r2}")
    assert r2 == [1]

    # 範例 3: nums=[7,6,5,4,3,2,1], k=3 (遞減)
    print("\n範例 3: nums=[7,6,5,4,3,2,1], k=3 (遞減序列)")
    r3 = max_sliding_window([7,6,5,4,3,2,1], 3, verbose=True)
    print(f"  Result = {r3}")
    assert r3 == [7,6,5,4,3]
    print()


# ----------------------------------------------------------------------------
#  4-2  Design Circular Queue（設計環形佇列）— LeetCode 622
#
#  觀念：用固定大小的 list，front 和 rear 指標取餘數循環。
#        count 紀錄目前元素數量（判斷 full/empty 更直覺）。
# ----------------------------------------------------------------------------

class MyCircularQueue:
    def __init__(self, k: int):
        self.data = [0] * k
        self.size = k
        self.front = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        rear = (self.front + self.count) % self.size
        self.data[rear] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.data[self.front]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        rear = (self.front + self.count - 1) % self.size
        return self.data[rear]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.size

    def __repr__(self):
        if self.isEmpty():
            return "CircularQueue(empty)"
        items = []
        for i in range(self.count):
            items.append(self.data[(self.front + i) % self.size])
        return (f"CircularQueue(data={items}, front_ptr={self.front}, "
                f"count={self.count}/{self.size})")


def demo_circular_queue():
    print("=" * 70)
    print("4-2  Design Circular Queue（環形佇列）— LeetCode 622")
    print("=" * 70)

    # 範例 1: 基本 enQueue / deQueue
    print("\n範例 1: 基本操作 (size=3)")
    cq = MyCircularQueue(3)
    ops = [
        ("enQueue(1)", lambda: cq.enQueue(1)),
        ("enQueue(2)", lambda: cq.enQueue(2)),
        ("enQueue(3)", lambda: cq.enQueue(3)),
        ("enQueue(4)", lambda: cq.enQueue(4)),   # Full → False
        ("Rear()",     lambda: cq.Rear()),        # 3
        ("isFull()",   lambda: cq.isFull()),      # True
        ("deQueue()",  lambda: cq.deQueue()),     # True
        ("enQueue(4)", lambda: cq.enQueue(4)),    # 現在有空位 → True
        ("Rear()",     lambda: cq.Rear()),        # 4
    ]
    for name, fn in ops:
        result = fn()
        print(f"  {name:15s} → {str(result):6s} | {cq}")

    # 範例 2: 環繞 (wrap-around) 展示
    print("\n範例 2: 環繞 wrap-around (size=3)")
    cq2 = MyCircularQueue(3)
    trace = [
        ("enQueue(10)", lambda: cq2.enQueue(10)),
        ("enQueue(20)", lambda: cq2.enQueue(20)),
        ("deQueue()",   lambda: cq2.deQueue()),     # 移除 10
        ("enQueue(30)", lambda: cq2.enQueue(30)),
        ("enQueue(40)", lambda: cq2.enQueue(40)),   # wrap around!
        ("Front()",     lambda: cq2.Front()),        # 20
        ("Rear()",      lambda: cq2.Rear()),         # 40
    ]
    for name, fn in trace:
        result = fn()
        print(f"  {name:15s} → {str(result):6s} | {cq2}")

    # 範例 3: 空佇列操作
    print("\n範例 3: 邊界測試 (size=2)")
    cq3 = MyCircularQueue(2)
    trace3 = [
        ("isEmpty()",   lambda: cq3.isEmpty()),     # True
        ("deQueue()",   lambda: cq3.deQueue()),     # False (空的)
        ("Front()",     lambda: cq3.Front()),       # -1
        ("enQueue(7)",  lambda: cq3.enQueue(7)),
        ("enQueue(8)",  lambda: cq3.enQueue(8)),
        ("Front()",     lambda: cq3.Front()),       # 7
        ("deQueue()",   lambda: cq3.deQueue()),
        ("deQueue()",   lambda: cq3.deQueue()),
        ("isEmpty()",   lambda: cq3.isEmpty()),     # True
    ]
    for name, fn in trace3:
        result = fn()
        print(f"  {name:15s} → {str(result):6s} | {cq3}")
    print()


# ============================================================================
#  SECTION 5: Stack vs Queue vs Monotonic Stack 比較總結
# ============================================================================

def print_comparison():
    print("=" * 70)
    print("SECTION 5: Stack vs Queue vs Monotonic Stack 比較總結")
    print("=" * 70)

    print("""
+---------------------+-------------------+-----------------------------------+
| 資料結構            | 使用時機           | 經典題型                           |
| (Data Structure)    | (When to Use)      | (Classic Problems)                |
+---------------------+-------------------+-----------------------------------+
| Stack               | 配對匹配           | Valid Parentheses                 |
| (堆疊 LIFO)        | 巢狀結構           | Decode String                     |
|                     | 後進先出邏輯       | Evaluate RPN                      |
|                     | 遞迴模擬           | Basic Calculator                  |
+---------------------+-------------------+-----------------------------------+
| Monotonic Stack     | "下一個更大/更小"  | Next Greater Element              |
| (單調堆疊)         | "左/右邊界"        | Daily Temperatures                |
|                     | "柱狀圖面積"       | Largest Rectangle in Histogram    |
|                     |                    | Trapping Rain Water               |
+---------------------+-------------------+-----------------------------------+
| Queue / Deque       | FIFO 順序處理      | BFS (Level-order Traversal)       |
| (佇列 / 雙端佇列)  | 滑動視窗最大/最小  | Sliding Window Maximum            |
|                     | 環形緩衝區         | Design Circular Queue             |
+---------------------+-------------------+-----------------------------------+

### 關鍵模式辨識 (Pattern Recognition)：

  1. 看到 "next greater / next smaller element"
     → 用 Monotonic Stack（單調堆疊）
     → 從右往左掃，維護遞減 stack

  2. 看到 "matching pairs" / "nested structure"
     → 用 Stack（一般堆疊）
     → 括號匹配、巢狀解碼、表達式求值

  3. 看到 "sliding window maximum / minimum"
     → 用 Monotonic Deque（單調雙端佇列）
     → deque 存 index，front 是答案

  4. 看到 "碰撞 / 消除"
     → 用 Stack（模擬碰撞過程）

### Monotonic Stack 兩種方向：

  (A) 找 Next Greater → 從右到左掃描，維護遞減 stack
      while stack and stack[-1] <= val: stack.pop()

  (B) 找 Previous Smaller → 從左到右掃描，維護遞增 stack
      while stack and stack[-1] >= val: stack.pop()

### 時間複雜度提醒：

  - 看起來像 O(n^2)（while loop 在 for loop 內），
    但每個元素最多 push 一次、pop 一次 → 攤銷 O(n)！
  - 這是面試中常被問到的 follow-up：
    "Why is this O(n) and not O(n^2)?"
""")


# ============================================================================
#  main() — 執行所有範例
# ============================================================================

def main():
    print()
    print("*" * 70)
    print("  LeetCode 教學 #04: Stack, Queue & Monotonic Stack")
    print("  堆疊、佇列與單調堆疊 — 完整教學與數值追蹤")
    print("*" * 70)
    print()

    # Section 1: 基礎 Stack
    demo_valid_parentheses()
    demo_min_stack()
    demo_eval_rpn()

    # Section 2: 單調 Stack
    demo_next_greater_element()
    demo_daily_temperatures()
    demo_largest_rectangle()

    # Section 3: Stack 模擬型
    demo_decode_string()
    demo_basic_calculator_ii()
    demo_asteroid_collision()

    # Section 4: Queue / Deque
    demo_sliding_window_max()
    demo_circular_queue()

    # Section 5: 比較總結
    print_comparison()

    print("=" * 70)
    print("  ALL EXAMPLES PASSED — 全部範例通過！")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
