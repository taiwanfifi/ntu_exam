#!/usr/bin/env python3
"""
=============================================================================
LeetCode Greedy 貪心演算法完全攻略
=============================================================================
目標讀者：準備 Google / NVIDIA 面試的初學者
教學風格：每題 3 個範例，每個範例都有完整的 step-by-step 數值追蹤
語言：繁體中文解說 + English technical terms

直接執行：python 14_Greedy.py
=============================================================================
"""
from typing import List
import heapq
from collections import Counter


# ============================================================================
# Section 1: Greedy 核心概念
# ============================================================================
# 什麼是 Greedy（貪心）？
#   每一步都選擇「當下最好」的選項，不回頭，最終得到全域最佳解。
#
# Greedy 成立的兩大條件：
#   1. Greedy Choice Property（貪心選擇性質）
#      → 局部最佳選擇可以導出全域最佳解
#   2. Optimal Substructure（最佳子結構）
#      → 做完一個選擇後，剩下的子問題仍然有最佳子結構
#
# Greedy vs DP：
#   - Greedy：每步只看當下，不回頭 → O(n) 或 O(n log n)
#   - DP：考慮所有可能組合，記憶子問題 → 通常 O(n^2) 或更高
#   - 如果能證明貪心選擇性質成立 → 用 Greedy（更快）
#   - 如果貪心會漏掉最佳解 → 必須用 DP
#
# 三個經典例子：Greedy 成功 vs 失敗
#
# [成功] 找零錢（硬幣面額: 1, 5, 10, 25）
#   目標: 41 cents → 25+10+5+1 = 4 枚（最佳！）
#   每次拿最大面額 → 保證最少硬幣數
#
# [成功] 活動選擇（按結束時間排序，選不衝突的最多活動）
#   每次選最早結束的 → 留最多空間給後面 → 保證最多活動數
#
# [失敗] 找零錢（硬幣面額: 1, 3, 4）目標: 6
#   Greedy: 4+1+1 = 3 枚
#   最佳:   3+3   = 2 枚  ← Greedy 失敗！需要 DP
#   原因：面額不是標準的倍數關係，貪心選擇性質不成立
# ============================================================================


# ============================================================================
# Section 2: 區間問題 (Interval Problems) - Google 最愛
# ============================================================================
# 區間問題是 Greedy 的經典應用場景。
# 核心技巧：先排序（by start 或 by end），然後逐一掃描決策。
# ============================================================================


# ---------------------------------------------------------------------------
# 2-1. Merge Intervals (LeetCode 56)
# ---------------------------------------------------------------------------
# 題意：給定一組區間 intervals，合併所有重疊的區間。
#
# 策略：按照 start 排序後，逐一比較 → 重疊就合併，不重疊就加入。
# Greedy 選擇：排序後，每次盡可能延伸當前區間的 end。
#
# 範例 1: intervals = [[1,3],[2,6],[8,10],[15,18]]
# 先排序（已排序）: [[1,3],[2,6],[8,10],[15,18]]
#
# Step 1: merged = [[1,3]], next=[2,6]
#   2 <= 3 (overlapping!) → merge → [1, max(3,6)] = [1,6]
#   merged = [[1,6]]
# Step 2: next=[8,10]
#   8 > 6 (no overlap) → add new
#   merged = [[1,6],[8,10]]
# Step 3: next=[15,18]
#   15 > 10 (no overlap) → add new
#   merged = [[1,6],[8,10],[15,18]]
# 結果: [[1,6],[8,10],[15,18]]
#
# 範例 2: intervals = [[1,4],[0,4]]
# 排序: [[0,4],[1,4]]
#
# Step 1: merged = [[0,4]], next=[1,4]
#   1 <= 4 (overlapping!) → merge → [0, max(4,4)] = [0,4]
#   merged = [[0,4]]
# 結果: [[0,4]]
#
# 範例 3: intervals = [[1,4],[2,3],[5,7],[6,9]]
# 排序: [[1,4],[2,3],[5,7],[6,9]]
#
# Step 1: merged = [[1,4]], next=[2,3]
#   2 <= 4 (overlapping!) → merge → [1, max(4,3)] = [1,4]
#   merged = [[1,4]]
# Step 2: next=[5,7]
#   5 > 4 (no overlap) → add new
#   merged = [[1,4],[5,7]]
# Step 3: next=[6,9]
#   6 <= 7 (overlapping!) → merge → [5, max(7,9)] = [5,9]
#   merged = [[1,4],[5,9]]
# 結果: [[1,4],[5,9]]

def merge_intervals(intervals: List[List[int]], verbose: bool = False) -> List[List[int]]:
    """Merge Intervals - 合併重疊區間。Time: O(n log n), Space: O(n)"""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    if verbose:
        print(f"  排序後: {intervals}")

    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        curr = intervals[i]
        last = merged[-1]

        if curr[0] <= last[1]:  # overlapping
            merged[-1][1] = max(last[1], curr[1])
            if verbose:
                print(f"  Step {i}: next={curr}, {curr[0]} <= {last[1]} "
                      f"(overlap!) → merge → {merged[-1]}")
        else:  # no overlap
            merged.append(curr)
            if verbose:
                print(f"  Step {i}: next={curr}, {curr[0]} > {last[1]} "
                      f"(no overlap) → add new")

    if verbose:
        print(f"  結果: {merged}")
    return merged


# ---------------------------------------------------------------------------
# 2-2. Non-overlapping Intervals (LeetCode 435)
# ---------------------------------------------------------------------------
# 題意：給定一組區間，找出「最少要移除幾個」才能使剩餘區間不重疊。
#
# 策略：按 end 排序 → 每次選結束最早的，若下一個的 start < 當前 end → 移除。
# Greedy 直覺：保留結束越早的，留給後面越多空間。
#
# 範例 1: intervals = [[1,2],[2,3],[3,4],[1,3]]
# 按 end 排序: [[1,2],[2,3],[1,3],[3,4]]
#
# Step 1: keep [1,2], end=2
# Step 2: next=[2,3], 2 >= 2 (no overlap) → keep, end=3
# Step 3: next=[1,3], 1 < 3 (overlap!) → remove, count=1
# Step 4: next=[3,4], 3 >= 3 (no overlap) → keep, end=4
# 結果: remove 1 個
#
# 範例 2: intervals = [[1,2],[1,2],[1,2]]
# 按 end 排序: [[1,2],[1,2],[1,2]]
#
# Step 1: keep [1,2], end=2
# Step 2: next=[1,2], 1 < 2 (overlap!) → remove, count=1
# Step 3: next=[1,2], 1 < 2 (overlap!) → remove, count=2
# 結果: remove 2 個
#
# 範例 3: intervals = [[1,100],[11,22],[1,11],[2,12]]
# 按 end 排序: [[1,11],[11,22],[2,12],[1,100]]
#
# Step 1: keep [1,11], end=11
# Step 2: next=[11,22], 11 >= 11 (no overlap) → keep, end=22
# Step 3: next=[2,12], 2 < 22 (overlap!) → remove, count=1
# Step 4: next=[1,100], 1 < 22 (overlap!) → remove, count=2
# 結果: remove 2 個

def erase_overlap_intervals(intervals: List[List[int]], verbose: bool = False) -> int:
    """Non-overlapping Intervals - 最少移除幾個區間。Time: O(n log n), Space: O(1)"""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])  # sort by end
    if verbose:
        print(f"  按 end 排序: {intervals}")

    count = 0
    end = intervals[0][1]
    if verbose:
        print(f"  Step 1: keep {intervals[0]}, end={end}")

    for i in range(1, len(intervals)):
        curr = intervals[i]
        if curr[0] < end:  # overlap
            count += 1
            if verbose:
                print(f"  Step {i+1}: next={curr}, {curr[0]} < {end} "
                      f"(overlap!) → remove, count={count}")
        else:
            end = curr[1]
            if verbose:
                print(f"  Step {i+1}: next={curr}, {curr[0]} >= {end - (curr[1]-end)} "
                      f"(no overlap) → keep, end={end}")

    if verbose:
        print(f"  結果: remove {count} 個")
    return count


# ---------------------------------------------------------------------------
# 2-3. Insert Interval (LeetCode 57)
# ---------------------------------------------------------------------------
# 題意：給定已排序且不重疊的區間 list，插入新區間並合併。
#
# 策略：分三段 → (1) 完全在左邊的直接加 (2) 重疊的合併 (3) 完全在右邊的直接加
#
# 範例 1: intervals = [[1,3],[6,9]], newInterval = [2,5]
#
# Step 1: [1,3] end=3 >= new start=2 → 可能重疊，進入合併
#   合併: new = [min(1,2), max(3,5)] = [1,5]
# Step 2: [6,9] start=6 > new end=5 → 不重疊，加入右邊
# 結果: [[1,5],[6,9]]
#
# 範例 2: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
#
# Step 1: [1,2] end=2 < new start=4 → 完全在左邊，直接加
# Step 2: [3,5] end=5 >= new start=4 → 重疊!
#   合併: new = [min(3,4), max(5,8)] = [3,8]
# Step 3: [6,7] start=6 <= new end=8 → 重疊!
#   合併: new = [min(3,6), max(8,7)] = [3,8]
# Step 4: [8,10] start=8 <= new end=8 → 重疊!
#   合併: new = [min(3,8), max(8,10)] = [3,10]
# Step 5: [12,16] start=12 > new end=10 → 右邊
# 結果: [[1,2],[3,10],[12,16]]
#
# 範例 3: intervals = [[1,5]], newInterval = [0,0]
#
# Step 1: [1,5] start=1 > new end=0 → new 完全在左邊!
# 結果: [[0,0],[1,5]]

def insert_interval(intervals: List[List[int]], newInterval: List[int],
                    verbose: bool = False) -> List[List[int]]:
    """Insert Interval - 插入並合併區間。Time: O(n), Space: O(n)"""
    result = []
    i = 0
    n = len(intervals)

    # Part 1: 完全在 newInterval 左邊的
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        if verbose:
            print(f"  左邊不重疊: {intervals[i]}")
        i += 1

    # Part 2: 與 newInterval 重疊的 → 合併
    while i < n and intervals[i][0] <= newInterval[1]:
        old_new = newInterval[:]
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        if verbose:
            print(f"  重疊合併: {intervals[i]} → new = [{newInterval[0]},{newInterval[1]}]")
        i += 1

    result.append(newInterval)
    if verbose:
        print(f"  插入合併後的區間: {newInterval}")

    # Part 3: 完全在 newInterval 右邊的
    while i < n:
        result.append(intervals[i])
        if verbose:
            print(f"  右邊不重疊: {intervals[i]}")
        i += 1

    if verbose:
        print(f"  結果: {result}")
    return result


# ---------------------------------------------------------------------------
# 2-4. Meeting Rooms II (LeetCode 253)
# ---------------------------------------------------------------------------
# 題意：給定會議時間區間，求最少需要幾間會議室。
#
# 策略：用 min-heap 追蹤每間會議室的結束時間。
#   新會議開始時，如果最早結束的會議室已空 → 複用，否則新開一間。
#
# 範例 1: intervals = [[0,30],[5,10],[15,20]]
# 排序: [[0,30],[5,10],[15,20]]
#
# Step 1: [0,30] → heap 為空，開新房 → heap=[30]  (1 間)
# Step 2: [5,10] → heap top=30, 5 < 30 → 衝突! 開新房 → heap=[10,30]  (2 間)
# Step 3: [15,20] → heap top=10, 15 >= 10 → 可複用! pop 10, push 20 → heap=[20,30]  (2 間)
# 結果: 2 間會議室
#
# 範例 2: intervals = [[7,10],[2,4]]
# 排序: [[2,4],[7,10]]
#
# Step 1: [2,4] → 開新房 → heap=[4]  (1 間)
# Step 2: [7,10] → heap top=4, 7 >= 4 → 可複用! → heap=[10]  (1 間)
# 結果: 1 間會議室
#
# 範例 3: intervals = [[0,5],[1,6],[2,7],[3,8]]
# 排序: [[0,5],[1,6],[2,7],[3,8]]
#
# Step 1: [0,5] → 開新房 → heap=[5]  (1 間)
# Step 2: [1,6] → top=5, 1 < 5 → 衝突! → heap=[5,6]  (2 間)
# Step 3: [2,7] → top=5, 2 < 5 → 衝突! → heap=[5,6,7]  (3 間)
# Step 4: [3,8] → top=5, 3 < 5 → 衝突! → heap=[5,6,7,8]  (4 間)
# 結果: 4 間（全部衝突，每個都需要獨立的房間）

def min_meeting_rooms(intervals: List[List[int]], verbose: bool = False) -> int:
    """Meeting Rooms II - 最少會議室數量。Time: O(n log n), Space: O(n)"""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    if verbose:
        print(f"  排序後: {intervals}")

    heap = []  # min-heap of end times

    for i, (start, end) in enumerate(intervals):
        if heap and heap[0] <= start:
            old_end = heapq.heappop(heap)
            heapq.heappush(heap, end)
            if verbose:
                print(f"  Step {i+1}: [{start},{end}] → top={old_end}, "
                      f"{start} >= {old_end} → 可複用! → heap={sorted(heap)} "
                      f"({len(heap)} 間)")
        else:
            heapq.heappush(heap, end)
            if verbose:
                if i == 0:
                    print(f"  Step {i+1}: [{start},{end}] → 開新房 → "
                          f"heap={sorted(heap)} ({len(heap)} 間)")
                else:
                    print(f"  Step {i+1}: [{start},{end}] → top={heap[0] if len(heap)==1 else min(heap)}, "
                          f"{start} < {sorted(heap)[0] if len(heap)>1 else heap[0]} → 衝突! → "
                          f"heap={sorted(heap)} ({len(heap)} 間)")

    if verbose:
        print(f"  結果: {len(heap)} 間會議室")
    return len(heap)


# ============================================================================
# Section 3: 跳躍/貪心選擇 (Jump / Greedy Choice)
# ============================================================================
# 這類問題的共同點：在每一步都做出最有利的選擇，往前推進。
# ============================================================================


# ---------------------------------------------------------------------------
# 3-1. Jump Game (LeetCode 55)
# ---------------------------------------------------------------------------
# 題意：陣列每個元素代表「最多能跳幾步」，問能否到達最後一個位置。
#
# 策略：維護 farthest（目前能到的最遠位置），逐步更新。
# Greedy 選擇：每一步都盡量跳最遠。
#
# 範例 1: nums = [2,3,1,1,4]
#
# Step 0: i=0, farthest = max(0, 0+2) = 2
#   目前能到 index 2
# Step 1: i=1, 1 <= 2 (可到達), farthest = max(2, 1+3) = 4
#   目前能到 index 4 >= 4 (last index) → 提前結束!
# 結果: True（可以到達）
#
# 範例 2: nums = [3,2,1,0,4]
#
# Step 0: i=0, farthest = max(0, 0+3) = 3
# Step 1: i=1, 1 <= 3, farthest = max(3, 1+2) = 3
# Step 2: i=2, 2 <= 3, farthest = max(3, 2+1) = 3
# Step 3: i=3, 3 <= 3, farthest = max(3, 3+0) = 3
#   遍歷結束, farthest=3 < 4 (last index)
# 結果: False（被 0 卡住了）
#
# 範例 3: nums = [1,1,1,1]
#
# Step 0: i=0, farthest = max(0, 0+1) = 1
# Step 1: i=1, farthest = max(1, 1+1) = 2
# Step 2: i=2, farthest = max(2, 2+1) = 3 >= 3 → True
# 結果: True

def can_jump(nums: List[int], verbose: bool = False) -> bool:
    """Jump Game - 能否到達終點。Time: O(n), Space: O(1)"""
    farthest = 0
    last = len(nums) - 1

    for i in range(len(nums)):
        if i > farthest:
            if verbose:
                print(f"  Step {i}: i={i} > farthest={farthest} → 無法到達!")
            return False

        farthest = max(farthest, i + nums[i])
        if verbose:
            print(f"  Step {i}: i={i}, farthest = max({farthest - max(0, i+nums[i]-farthest)}, "
                  f"{i}+{nums[i]}) = {farthest}")

        if farthest >= last:
            if verbose:
                print(f"  farthest={farthest} >= last={last} → True!")
            return True

    if verbose:
        print(f"  結果: farthest={farthest}, last={last}")
    return farthest >= last


# ---------------------------------------------------------------------------
# 3-2. Jump Game II (LeetCode 45)
# ---------------------------------------------------------------------------
# 題意：保證能到終點，求最少跳幾次。
#
# 策略：BFS 思維 — 每一「層」是當前跳能到的範圍。
#   在當前範圍內找最遠的下一步，到達範圍邊界時 jumps++。
#
# 範例 1: nums = [2,3,1,1,4]
#
# 初始: jumps=0, curEnd=0, farthest=0
# i=0: farthest = max(0, 0+2)=2, i==curEnd(0) → jumps=1, curEnd=2
# i=1: farthest = max(2, 1+3)=4, 4 >= 4 → 可提前結束
# i=2: i==curEnd(2) → jumps=2, curEnd=4
# 結果: 2 jumps (0→1→4)
#
# 範例 2: nums = [2,3,0,1,4]
#
# i=0: farthest = max(0,0+2)=2, i==curEnd → jumps=1, curEnd=2
# i=1: farthest = max(2,1+3)=4
# i=2: farthest = max(4,2+0)=4, i==curEnd → jumps=2, curEnd=4
# 結果: 2 jumps
#
# 範例 3: nums = [1,2,3]
#
# i=0: farthest = max(0,0+1)=1, i==curEnd → jumps=1, curEnd=1
# i=1: farthest = max(1,1+2)=3, 3 >= 2 → 到達!
#      i==curEnd → jumps=2, curEnd=3
# 結果: 2 jumps (0→1→2)

def jump_game_ii(nums: List[int], verbose: bool = False) -> int:
    """Jump Game II - 最少跳躍次數。Time: O(n), Space: O(1)"""
    if len(nums) <= 1:
        return 0

    jumps = 0
    cur_end = 0
    farthest = 0
    last = len(nums) - 1

    if verbose:
        print(f"  初始: jumps=0, curEnd=0, farthest=0, target={last}")

    for i in range(len(nums) - 1):  # don't need to jump from last
        farthest = max(farthest, i + nums[i])
        if verbose:
            print(f"  i={i}: farthest = max(_, {i}+{nums[i]})={farthest}", end="")

        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if verbose:
                print(f", i==curEnd → jumps={jumps}, curEnd={cur_end}")
            if cur_end >= last:
                break
        else:
            if verbose:
                print()

    if verbose:
        print(f"  結果: {jumps} jumps")
    return jumps


# ---------------------------------------------------------------------------
# 3-3. Gas Station (LeetCode 134)
# ---------------------------------------------------------------------------
# 題意：環形路線 n 個加油站，gas[i] 加油量，cost[i] 到下一站的耗油量。
#       找出能繞一圈的起始站，保證唯一解或無解。
#
# 策略：如果 total gas >= total cost → 一定有解。
#   Greedy：追蹤 tank，如果 tank < 0 → 從下一站重新開始。
#
# 範例 1: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
# net = gas-cost = [-2,-2,-2,3,3], total = 0 → 有解
#
# i=0: tank = 0+(-2) = -2 < 0 → reset! start=1, tank=0
# i=1: tank = 0+(-2) = -2 < 0 → reset! start=2, tank=0
# i=2: tank = 0+(-2) = -2 < 0 → reset! start=3, tank=0
# i=3: tank = 0+3 = 3 >= 0 ✓
# i=4: tank = 3+3 = 6 >= 0 ✓
# 結果: start = 3
#
# 範例 2: gas = [2,3,4], cost = [3,4,3]
# net = [-1,-1,1], total = -1 < 0 → 無解
# 結果: -1
#
# 範例 3: gas = [5,1,2,3,4], cost = [4,4,1,5,1]
# net = [1,-3,1,-2,3], total = 0 → 有解
#
# i=0: tank = 0+1 = 1 >= 0 ✓
# i=1: tank = 1+(-3) = -2 < 0 → reset! start=2, tank=0
# i=2: tank = 0+1 = 1 >= 0 ✓
# i=3: tank = 1+(-2) = -1 < 0 → reset! start=4, tank=0
# i=4: tank = 0+3 = 3 >= 0 ✓
# 結果: start = 4

def can_complete_circuit(gas: List[int], cost: List[int],
                         verbose: bool = False) -> int:
    """Gas Station - 能繞一圈的起點。Time: O(n), Space: O(1)"""
    total_tank = 0
    curr_tank = 0
    start = 0

    if verbose:
        net = [g - c for g, c in zip(gas, cost)]
        print(f"  net = gas-cost = {net}, total = {sum(net)}")

    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        curr_tank += diff

        if verbose:
            print(f"  i={i}: tank = {curr_tank}", end="")

        if curr_tank < 0:
            start = i + 1
            curr_tank = 0
            if verbose:
                print(f" < 0 → reset! start={start}, tank=0")
        else:
            if verbose:
                print(f" >= 0 ✓")

    result = start if total_tank >= 0 else -1
    if verbose:
        print(f"  結果: {'start = ' + str(start) if total_tank >= 0 else '無解 (-1)'}")
    return result


# ---------------------------------------------------------------------------
# 3-4. Task Scheduler (LeetCode 621)
# ---------------------------------------------------------------------------
# 題意：有 tasks 和冷卻時間 n，同一個 task 之間至少隔 n 個間隔。
#       求最少需要多少時間單位完成所有 tasks。
#
# 策略：最高頻的 task 決定框架，idle slots 被其他 tasks 填滿。
#   公式：框架 = (maxFreq - 1) * (n + 1) + countOfMax
#   答案 = max(框架, len(tasks))  ← 當 tasks 很多時不需要 idle
#
# 範例 1: tasks = ["A","A","A","B","B","B"], n = 2
# 頻率: A=3, B=3, maxFreq=3, countOfMax=2
#
# 框架: (3-1) * (2+1) + 2 = 2 * 3 + 2 = 8
# 排列: A B _ | A B _ | A B
#       ^^^     ^^^     ^^
#       slot1   slot2   tail(countOfMax=2)
# len(tasks)=6, max(8, 6) = 8
# 結果: 8
#
# 範例 2: tasks = ["A","A","A","B","B","B"], n = 0
# 頻率: A=3, B=3, maxFreq=3, countOfMax=2
#
# 框架: (3-1) * (0+1) + 2 = 2 * 1 + 2 = 4
# 但 len(tasks)=6 > 4 → 不需要任何 idle!
# 結果: max(4, 6) = 6
#
# 範例 3: tasks = ["A","A","A","A","B","C","D","E"], n = 2
# 頻率: A=4, B=1, C=1, D=1, E=1, maxFreq=4, countOfMax=1
#
# 框架: (4-1) * (2+1) + 1 = 3 * 3 + 1 = 10
# 排列: A B C | A D E | A _ _ | A
#       slot1   slot2   slot3   tail
# idle slots = 10 - 8 = 2 個 idle
# 結果: max(10, 8) = 10

def least_interval(tasks: List[str], n: int, verbose: bool = False) -> int:
    """Task Scheduler - 最少時間完成所有 tasks。Time: O(m), Space: O(1)"""
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_of_max = sum(1 for v in freq.values() if v == max_freq)

    if verbose:
        print(f"  頻率: {dict(freq)}")
        print(f"  maxFreq={max_freq}, countOfMax={count_of_max}")

    frame = (max_freq - 1) * (n + 1) + count_of_max
    result = max(frame, len(tasks))

    if verbose:
        print(f"  框架: ({max_freq}-1) * ({n}+1) + {count_of_max} "
              f"= {max_freq-1} * {n+1} + {count_of_max} = {frame}")
        print(f"  len(tasks)={len(tasks)}, max({frame}, {len(tasks)}) = {result}")

    return result


# ============================================================================
# Section 4: 分配型 Greedy (Assignment / Distribution)
# ============================================================================
# 共同模式：排序後，用雙指針或 two-end 策略做最佳配對。
# ============================================================================


# ---------------------------------------------------------------------------
# 4-1. Assign Cookies (LeetCode 455)
# ---------------------------------------------------------------------------
# 題意：每個小孩有 greed factor g[i]，每塊餅乾有 size s[j]。
#       s[j] >= g[i] 才能滿足小孩 i。求最多能滿足幾個小孩。
#
# 策略：排序後，貪心地把最小能滿足的餅乾分給最不貪心的小孩。
#
# 範例 1: g = [1,2,3], s = [1,1]
# 排序: g=[1,2,3], s=[1,1]
#
# i=0, j=0: s[0]=1 >= g[0]=1 ✓ → 滿足! i=1, j=1, count=1
# i=1, j=1: s[1]=1 < g[1]=2 → 餅乾太小, j=2
# j=2 超出範圍 → 結束
# 結果: 1 個小孩被滿足
#
# 範例 2: g = [1,2], s = [1,2,3]
# 排序: g=[1,2], s=[1,2,3]
#
# i=0, j=0: s[0]=1 >= g[0]=1 ✓ → count=1, i=1, j=1
# i=1, j=1: s[1]=2 >= g[1]=2 ✓ → count=2, i=2, j=2
# i=2 超出 → 結束
# 結果: 2 個小孩被滿足
#
# 範例 3: g = [10,9,8,7], s = [5,6,7,8]
# 排序: g=[7,8,9,10], s=[5,6,7,8]
#
# i=0, j=0: s[0]=5 < g[0]=7 → j=1
# i=0, j=1: s[1]=6 < g[0]=7 → j=2
# i=0, j=2: s[2]=7 >= g[0]=7 ✓ → count=1, i=1, j=3
# i=1, j=3: s[3]=8 >= g[1]=8 ✓ → count=2, i=2, j=4
# j=4 超出 → 結束
# 結果: 2 個小孩被滿足

def find_content_children(g: List[int], s: List[int],
                          verbose: bool = False) -> int:
    """Assign Cookies - 最多滿足幾個小孩。Time: O(n log n), Space: O(1)"""
    g.sort()
    s.sort()
    if verbose:
        print(f"  排序: g={g}, s={s}")

    child = 0
    cookie = 0

    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            if verbose:
                print(f"  i={child}, j={cookie}: s[{cookie}]={s[cookie]} >= "
                      f"g[{child}]={g[child]} ✓ → count={child+1}")
            child += 1
        else:
            if verbose:
                print(f"  i={child}, j={cookie}: s[{cookie}]={s[cookie]} < "
                      f"g[{child}]={g[child]} → 餅乾太小, skip")
        cookie += 1

    if verbose:
        print(f"  結果: {child} 個小孩被滿足")
    return child


# ---------------------------------------------------------------------------
# 4-2. Boats to Save People (LeetCode 881)
# ---------------------------------------------------------------------------
# 題意：每艘船最多載 2 人，重量限制 limit。求最少幾艘船。
#
# 策略：排序後，最輕配最重（雙指針）。能配就配，不能就重的獨坐。
#
# 範例 1: people = [1,2], limit = 3
# 排序: [1,2]
#
# left=0, right=1: 1+2=3 <= 3 → 配對! boats=1, left=1, right=0
# 結束
# 結果: 1 艘船
#
# 範例 2: people = [3,2,2,1], limit = 3
# 排序: [1,2,2,3]
#
# left=0, right=3: 1+3=4 > 3 → 3 獨坐, boats=1, right=2
# left=0, right=2: 1+2=3 <= 3 → 配對! boats=2, left=1, right=1
# left > right → 結束
# 結果: 2 艘船
#
# 範例 3: people = [3,5,3,4], limit = 5
# 排序: [3,3,4,5]
#
# left=0, right=3: 3+5=8 > 5 → 5 獨坐, boats=1, right=2
# left=0, right=2: 3+4=7 > 5 → 4 獨坐, boats=2, right=1
# left=0, right=1: 3+3=6 > 5 → 3 獨坐, boats=3, right=0
# left=0, right=0: 一個人 → 獨坐, boats=4
# 結果: 4 艘船

def num_rescue_boats(people: List[int], limit: int,
                     verbose: bool = False) -> int:
    """Boats to Save People - 最少船數。Time: O(n log n), Space: O(1)"""
    people.sort()
    if verbose:
        print(f"  排序: {people}, limit={limit}")

    left, right = 0, len(people) - 1
    boats = 0

    while left <= right:
        if left == right:
            boats += 1
            if verbose:
                print(f"  left={left}==right → {people[left]} 獨坐, boats={boats}")
            break

        if people[left] + people[right] <= limit:
            if verbose:
                print(f"  left={left}, right={right}: {people[left]}+{people[right]}"
                      f"={people[left]+people[right]} <= {limit} → 配對! ", end="")
            left += 1
            right -= 1
            boats += 1
            if verbose:
                print(f"boats={boats}")
        else:
            if verbose:
                print(f"  left={left}, right={right}: {people[left]}+{people[right]}"
                      f"={people[left]+people[right]} > {limit} → "
                      f"{people[right]} 獨坐, ", end="")
            right -= 1
            boats += 1
            if verbose:
                print(f"boats={boats}")

    if verbose:
        print(f"  結果: {boats} 艘船")
    return boats


# ---------------------------------------------------------------------------
# 4-3. Partition Labels (LeetCode 763)
# ---------------------------------------------------------------------------
# 題意：將字串分成盡可能多的部分，使得每個字母只出現在一個部分中。
#
# 策略：先記錄每個字母最後出現的位置 (last occurrence)。
#   掃描字串，擴展當前 partition 的右邊界到所有字母的最後出現位置。
#
# 範例 1: s = "ababcbacadefegdehijhklij"
# last occurrence: a→8, b→5, c→7, d→14, e→15, f→11, g→13, h→19, i→22, j→23, k→20, l→21
#
# i=0 'a': end = max(0,8)=8
# i=1 'b': end = max(8,5)=8
# i=2 'a': end = max(8,8)=8
# ...
# i=8 'a': end=8, i==end → 切! partition size=9
# i=9 'd': end=14
# ...
# i=15 'e': end=15, i==end → 切! partition size=7
# i=16 'h': end=19
# ...
# i=23 'j': end=23, i==end → 切! partition size=8
# 結果: [9, 7, 8]
#
# 範例 2: s = "eccbbbbdec"
# last: e→8, c→9, b→6, d→7
#
# i=0 'e': end=8
# i=1 'c': end=max(8,9)=9
# ... 所有字母的 last 都 <= 9
# i=9 'c': end=9, i==end → 切! size=10
# 結果: [10] (整個字串一個 partition)
#
# 範例 3: s = "abcabc"
# last: a→3, b→4, c→5
#
# i=0 'a': end=3
# i=1 'b': end=max(3,4)=4
# i=2 'c': end=max(4,5)=5
# i=3 'a': end=max(5,3)=5
# i=4 'b': end=max(5,4)=5
# i=5 'c': end=5, i==end → 切! size=6
# 結果: [6]

def partition_labels(s: str, verbose: bool = False) -> List[int]:
    """Partition Labels - 分割字串使字母只出現在一個部分。Time: O(n), Space: O(1)"""
    last = {}
    for i, ch in enumerate(s):
        last[ch] = i

    if verbose:
        print(f"  last occurrence: {last}")

    result = []
    start = 0
    end = 0

    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if verbose:
            print(f"  i={i} '{ch}': end=max(_, {last[ch]})={end}", end="")

        if i == end:
            result.append(end - start + 1)
            if verbose:
                print(f", i==end → 切! size={end - start + 1}")
            start = end + 1
        else:
            if verbose:
                print()

    if verbose:
        print(f"  結果: {result}")
    return result


# ============================================================================
# Section 5: 數字/字串型 Greedy (Number / String Greedy)
# ============================================================================
# 這類問題需要在字串或數字上做出最佳的逐步選擇。
# ============================================================================


# ---------------------------------------------------------------------------
# 5-1. Remove K Digits (LeetCode 402)
# ---------------------------------------------------------------------------
# 題意：從數字字串中移除 k 位數，使剩餘數字最小。
#
# 策略：Monotonic Stack + Greedy。
#   從左到右掃，如果當前數字 < stack top → pop (移除大的)，直到用完 k 次。
#   直覺：在高位保留小的數字 → 整體數值最小。
#
# 範例 1: num = "1432219", k = 3
#
# Step 1: '1' → stack=[1]
# Step 2: '4' → 4>=1, push → stack=[1,4]
# Step 3: '3' → 3<4, pop 4 (k=2) → stack=[1,3]
# Step 4: '2' → 2<3, pop 3 (k=1) → stack=[1,2]
# Step 5: '2' → 2>=2, push → stack=[1,2,2]
# Step 6: '1' → 1<2, pop 2 (k=0) → stack=[1,2,1]
# Step 7: '9' → k=0, push → stack=[1,2,1,9]
# 去除前導零 → "1219"
# 結果: "1219"
#
# 範例 2: num = "10200", k = 1
#
# Step 1: '1' → stack=[1]
# Step 2: '0' → 0<1, pop 1 (k=0) → stack=[0]
# Step 3: '2' → push → stack=[0,2]
# Step 4: '0' → k=0, push → stack=[0,2,0]
# Step 5: '0' → k=0, push → stack=[0,2,0,0]
# 去除前導零 → "200"
# 結果: "200"
#
# 範例 3: num = "9876", k = 2
#
# Step 1: '9' → stack=[9]
# Step 2: '8' → 8<9, pop 9 (k=1) → stack=[8]
# Step 3: '7' → 7<8, pop 8 (k=0) → stack=[7]
# Step 4: '6' → k=0, push → stack=[7,6]
# 結果: "76"

def remove_k_digits(num: str, k: int, verbose: bool = False) -> str:
    """Remove K Digits - 移除 k 位使數字最小。Time: O(n), Space: O(n)"""
    stack = []

    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            popped = stack.pop()
            k -= 1
            if verbose:
                print(f"  '{digit}' < '{popped}', pop (k={k}) → stack={''.join(stack)}")

        stack.append(digit)
        if verbose:
            print(f"  push '{digit}' → stack={''.join(stack)}")

    # If k still > 0, remove from end (the remaining are in ascending order)
    if k > 0:
        if verbose:
            print(f"  還剩 k={k}，從尾部移除: {''.join(stack)} → {''.join(stack[:-k])}")
        stack = stack[:-k]

    result = ''.join(stack).lstrip('0') or '0'
    if verbose:
        print(f"  去除前導零 → \"{result}\"")
    return result


# ---------------------------------------------------------------------------
# 5-2. Reorganize String (LeetCode 767)
# ---------------------------------------------------------------------------
# 題意：重新排列字串，使得相鄰字母不同。不可能則回傳 ""。
#
# 策略：每次從 max-heap 取出頻率最高的字母放入結果，然後輪換。
#   如果最高頻 > (len+1)//2 → 不可能。
#
# 範例 1: s = "aab"
# 頻率: a=2, b=1
# 最高頻 2 <= (3+1)//2 = 2 → 可行
#
# heap = [(-2,'a'), (-1,'b')]
# Step 1: pop (-2,'a') → result="a", push back (-1,'a')
#   heap = [(-1,'a'), (-1,'b')]  (先取前次放回的以外的)
# Step 2: pop (-1,'b') → result="ab", push back (0 不推)
#   heap = [(-1,'a')]
# Step 3: pop (-1,'a') → result="aba"
# 結果: "aba"
#
# 範例 2: s = "aaab"
# 頻率: a=3, b=1
# 最高頻 3 > (4+1)//2 = 2 → 不可能!
# 結果: ""
#
# 範例 3: s = "aabbcc"
# 頻率: a=2, b=2, c=2
# 最高頻 2 <= (6+1)//2 = 3 → 可行
#
# 一種合法排列: "abcabc" 或 "abacbc" 等
# 結果: (任何合法排列皆可)

def reorganize_string(s: str, verbose: bool = False) -> str:
    """Reorganize String - 相鄰不重複排列。Time: O(n log k), Space: O(k)"""
    freq = Counter(s)
    max_freq = max(freq.values())

    if verbose:
        print(f"  頻率: {dict(freq)}")
        print(f"  最高頻={max_freq}, 上限={(len(s)+1)//2}")

    if max_freq > (len(s) + 1) // 2:
        if verbose:
            print(f"  {max_freq} > {(len(s)+1)//2} → 不可能!")
        return ""

    # Max heap (negate for max behavior)
    heap = [(-cnt, ch) for ch, cnt in freq.items()]
    heapq.heapify(heap)

    result = []
    prev = None  # (count, char) of the previously placed character

    step = 0
    while heap or prev:
        if not heap and prev:
            # prev is the only one left but can't place → impossible
            if verbose:
                print(f"  heap 空但 prev='{prev[1]}' 還剩 → 不可能")
            return ""

        step += 1
        neg_cnt, ch = heapq.heappop(heap)
        result.append(ch)
        cnt = -neg_cnt

        if verbose:
            print(f"  Step {step}: pop '{ch}'(freq={cnt}) → result=\"{''.join(result)}\"")

        # Push back the previously held character
        if prev:
            heapq.heappush(heap, prev)
            if verbose:
                print(f"    push back prev '{prev[1]}'(freq={-prev[0]})")
            prev = None

        # Hold current char if still has remaining count
        if cnt - 1 > 0:
            prev = (-(cnt - 1), ch)

    result_str = ''.join(result)
    if verbose:
        print(f"  結果: \"{result_str}\"")
    return result_str


# ---------------------------------------------------------------------------
# 5-3. Queue Reconstruction by Height (LeetCode 406)
# ---------------------------------------------------------------------------
# 題意：people[i] = [h, k]，h 是身高，k 是前面有幾個人 >= h。
#       重建隊列。
#
# 策略：先按身高 降序 排列（同高則按 k 升序），然後依 k 值插入。
# Greedy 直覺：先安排高的人，矮的人插入不影響高的人的 k 值。
#
# 範例 1: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
# 排序（h 降序, k 升序）: [[7,0],[7,1],[6,1],[5,0],[5,2],[4,4]]
#
# Step 1: insert [7,0] at index 0 → [[7,0]]
# Step 2: insert [7,1] at index 1 → [[7,0],[7,1]]
# Step 3: insert [6,1] at index 1 → [[7,0],[6,1],[7,1]]
# Step 4: insert [5,0] at index 0 → [[5,0],[7,0],[6,1],[7,1]]
# Step 5: insert [5,2] at index 2 → [[5,0],[7,0],[5,2],[6,1],[7,1]]
# Step 6: insert [4,4] at index 4 → [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
# 結果: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
#
# 範例 2: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
# 排序: [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
#
# Step 1: insert [6,0] at 0 → [[6,0]]
# Step 2: insert [5,0] at 0 → [[5,0],[6,0]]
# Step 3: insert [4,0] at 0 → [[4,0],[5,0],[6,0]]
# Step 4: insert [3,2] at 2 → [[4,0],[5,0],[3,2],[6,0]]
# Step 5: insert [2,2] at 2 → [[4,0],[5,0],[2,2],[3,2],[6,0]]
# Step 6: insert [1,4] at 4 → [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
# 結果: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
#
# 範例 3: people = [[9,0],[7,0],[1,9],[3,0],[2,7],[5,3],[6,0],[3,4],[6,2],[5,2]]
# 排序: [[9,0],[7,0],[6,0],[6,2],[5,2],[5,3],[3,0],[3,4],[2,7],[1,9]]
#
# Step 1: insert [9,0] at 0 → [[9,0]]
# Step 2: insert [7,0] at 0 → [[7,0],[9,0]]
# Step 3: insert [6,0] at 0 → [[6,0],[7,0],[9,0]]
# Step 4: insert [6,2] at 2 → [[6,0],[7,0],[6,2],[9,0]]
# Step 5: insert [5,2] at 2 → [[6,0],[7,0],[5,2],[6,2],[9,0]]
# Step 6: insert [5,3] at 3 → [[6,0],[7,0],[5,2],[5,3],[6,2],[9,0]]
# Step 7: insert [3,0] at 0 → [[3,0],[6,0],[7,0],[5,2],[5,3],[6,2],[9,0]]
# Step 8: insert [3,4] at 4 → [[3,0],[6,0],[7,0],[5,2],[3,4],[5,3],[6,2],[9,0]]
# Step 9: insert [2,7] at 7 → [[3,0],[6,0],[7,0],[5,2],[3,4],[5,3],[6,2],[2,7],[9,0]]
# Step 10: insert [1,9] at 9 → [[3,0],[6,0],[7,0],[5,2],[3,4],[5,3],[6,2],[2,7],[9,0],[1,9]]
# 結果: [[3,0],[6,0],[7,0],[5,2],[3,4],[5,3],[6,2],[2,7],[9,0],[1,9]]

def reconstruct_queue(people: List[List[int]], verbose: bool = False) -> List[List[int]]:
    """Queue Reconstruction by Height。Time: O(n^2), Space: O(n)"""
    # Sort: height descending, then k ascending
    people.sort(key=lambda x: (-x[0], x[1]))
    if verbose:
        print(f"  排序（h降序, k升序）: {people}")

    queue = []
    for i, person in enumerate(people):
        queue.insert(person[1], person)
        if verbose:
            print(f"  Step {i+1}: insert {person} at index {person[1]} → {queue}")

    if verbose:
        print(f"  結果: {queue}")
    return queue


# ============================================================================
# Section 6: Greedy vs DP 完整比較
# ============================================================================
# 什麼時候 Greedy 有效？什麼時候必須用 DP？
#
# ----- Greedy 正確的條件 -----
# 1. Greedy Choice Property（貪心選擇性質）
#    → 做出局部最佳選擇後，不需要回頭修改
#    → 證明方法：Exchange Argument（交換論證）
#      假設最佳解 OPT 和 Greedy 解 G 不同，
#      證明把 OPT 中的某個選擇「交換」成 G 的選擇後，
#      結果不會變差 → G 也是最佳解。
#
# 2. Optimal Substructure（最佳子結構）
#    → 子問題的最佳解可以組成全域最佳解
#
# ----- Red Flags: Greedy 會失敗的信號 -----
# 1. 問題要求「所有可能的組合」或「方案數」→ 用 DP/backtracking
# 2. 當前選擇會影響未來所有子問題的結構 → 用 DP
# 3. 問題有「重疊子問題」但沒有 greedy choice property → 用 DP
# 4. 小測試 case 可以找到 greedy 反例 → 一定不能用 greedy
#
# ----- 經典對比 -----
# | 問題              | Greedy | DP  | 原因                          |
# |-------------------|--------|-----|-------------------------------|
# | Activity Selection | ✓      |     | 選最早結束的，exchange arg 成立  |
# | Coin Change       |        | ✓   | 非標準面額時 greedy 失敗        |
# | Jump Game         | ✓      |     | farthest reach 是單調的        |
# | 0/1 Knapsack      |        | ✓   | 物品不可分割，greedy 漏最佳組合  |
# | Fractional Knapsack| ✓     |     | 物品可分割，按 CP 值排序即可     |
# | Huffman Coding    | ✓      |     | 合併最小頻率，exchange arg 成立  |
# | LIS (最長遞增子序列) |      | ✓   | 需要考慮所有可能的子序列          |
# | Merge Intervals   | ✓      |     | 排序後逐一合併，不需回頭         |
# ============================================================================


# ---------------------------------------------------------------------------
# 6-1. 同一問題的 Greedy vs DP 比較: Jump Game
# ---------------------------------------------------------------------------
# Greedy 解法已在 Section 3 (can_jump)，這裡展示 DP 解法做對比。

def can_jump_dp(nums: List[int], verbose: bool = False) -> bool:
    """Jump Game - DP 版本（對比用）。Time: O(n^2), Space: O(n)"""
    n = len(nums)
    dp = [False] * n
    dp[0] = True

    if verbose:
        print(f"  DP 初始: dp[0]=True, 其餘 False")

    for i in range(1, n):
        for j in range(i):
            if dp[j] and j + nums[j] >= i:
                dp[i] = True
                if verbose:
                    print(f"  dp[{i}]=True (from dp[{j}]=True, {j}+{nums[j]}={j+nums[j]} >= {i})")
                break
        if verbose and not dp[i]:
            print(f"  dp[{i}]=False (no valid predecessor)")

    if verbose:
        print(f"  DP 結果: {dp[-1]} (Greedy 只要 O(n)，DP 卻要 O(n^2)!)")
    return dp[-1]


# ---------------------------------------------------------------------------
# 6-2. Greedy 失敗的案例：Coin Change
# ---------------------------------------------------------------------------
# 用 Greedy（每次拿最大面額）vs DP 的對比。

def coin_change_greedy(coins: List[int], amount: int,
                       verbose: bool = False) -> int:
    """Coin Change - Greedy 版本（可能錯誤！僅做對比）"""
    coins.sort(reverse=True)
    count = 0

    if verbose:
        print(f"  硬幣（降序）: {coins}, 目標: {amount}")

    remaining = amount
    for coin in coins:
        if remaining <= 0:
            break
        num = remaining // coin
        if num > 0:
            count += num
            if verbose:
                print(f"  用 {num} 個 {coin} 元 → 剩餘 {remaining} - {num*coin} = {remaining - num*coin}")
            remaining -= num * coin

    if remaining != 0:
        if verbose:
            print(f"  Greedy 失敗! 剩餘 {remaining} 無法湊齊")
        return -1

    if verbose:
        print(f"  Greedy 答案: {count} 枚")
    return count


def coin_change_dp(coins: List[int], amount: int,
                   verbose: bool = False) -> int:
    """Coin Change - DP 版本（正確解法）。Time: O(n*amount), Space: O(amount)"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    result = dp[amount] if dp[amount] != float('inf') else -1
    if verbose:
        # Show key states
        print(f"  DP 表格（部分）:")
        show = [0] + list(range(1, min(amount + 1, 8))) + ([amount] if amount >= 8 else [])
        for idx in show:
            val = dp[idx] if dp[idx] != float('inf') else "INF"
            print(f"    dp[{idx}] = {val}")
        print(f"  DP 答案: {result} 枚")
    return result


# ============================================================================
# Main - 完整測試所有函式
# ============================================================================

def main():
    print("=" * 70)
    print("LeetCode Greedy 貪心演算法完全攻略")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Section 2: 區間問題
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Section 2: 區間問題 (Interval Problems)")
    print("=" * 70)

    print("\n--- 2-1. Merge Intervals (LC 56) ---")
    for i, intervals in enumerate([
        [[1, 3], [2, 6], [8, 10], [15, 18]],
        [[1, 4], [0, 4]],
        [[1, 4], [2, 3], [5, 7], [6, 9]],
    ], 1):
        print(f"\n範例 {i}: intervals = {intervals}")
        result = merge_intervals([iv[:] for iv in intervals], verbose=True)
        print(f"答案: {result}")

    print("\n--- 2-2. Non-overlapping Intervals (LC 435) ---")
    for i, intervals in enumerate([
        [[1, 2], [2, 3], [3, 4], [1, 3]],
        [[1, 2], [1, 2], [1, 2]],
        [[1, 100], [11, 22], [1, 11], [2, 12]],
    ], 1):
        print(f"\n範例 {i}: intervals = {intervals}")
        result = erase_overlap_intervals([iv[:] for iv in intervals], verbose=True)
        print(f"答案: {result}")

    print("\n--- 2-3. Insert Interval (LC 57) ---")
    for i, (intervals, new) in enumerate([
        ([[1, 3], [6, 9]], [2, 5]),
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
        ([[1, 5]], [0, 0]),
    ], 1):
        print(f"\n範例 {i}: intervals = {intervals}, newInterval = {new}")
        result = insert_interval([iv[:] for iv in intervals], new[:], verbose=True)
        print(f"答案: {result}")

    print("\n--- 2-4. Meeting Rooms II (LC 253) ---")
    for i, intervals in enumerate([
        [[0, 30], [5, 10], [15, 20]],
        [[7, 10], [2, 4]],
        [[0, 5], [1, 6], [2, 7], [3, 8]],
    ], 1):
        print(f"\n範例 {i}: intervals = {intervals}")
        result = min_meeting_rooms([iv[:] for iv in intervals], verbose=True)
        print(f"答案: {result} 間")

    # ------------------------------------------------------------------
    # Section 3: 跳躍/貪心選擇
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Section 3: 跳躍/貪心選擇 (Jump / Greedy Choice)")
    print("=" * 70)

    print("\n--- 3-1. Jump Game (LC 55) ---")
    for i, nums in enumerate([
        [2, 3, 1, 1, 4],
        [3, 2, 1, 0, 4],
        [1, 1, 1, 1],
    ], 1):
        print(f"\n範例 {i}: nums = {nums}")
        result = can_jump(nums, verbose=True)
        print(f"答案: {result}")

    print("\n--- 3-2. Jump Game II (LC 45) ---")
    for i, nums in enumerate([
        [2, 3, 1, 1, 4],
        [2, 3, 0, 1, 4],
        [1, 2, 3],
    ], 1):
        print(f"\n範例 {i}: nums = {nums}")
        result = jump_game_ii(nums, verbose=True)
        print(f"答案: {result} jumps")

    print("\n--- 3-3. Gas Station (LC 134) ---")
    for i, (gas, cost) in enumerate([
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]),
        ([2, 3, 4], [3, 4, 3]),
        ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]),
    ], 1):
        print(f"\n範例 {i}: gas = {gas}, cost = {cost}")
        result = can_complete_circuit(gas, cost, verbose=True)
        print(f"答案: {result}")

    print("\n--- 3-4. Task Scheduler (LC 621) ---")
    for i, (tasks, n) in enumerate([
        (["A", "A", "A", "B", "B", "B"], 2),
        (["A", "A", "A", "B", "B", "B"], 0),
        (["A", "A", "A", "A", "B", "C", "D", "E"], 2),
    ], 1):
        print(f"\n範例 {i}: tasks = {tasks}, n = {n}")
        result = least_interval(tasks, n, verbose=True)
        print(f"答案: {result}")

    # ------------------------------------------------------------------
    # Section 4: 分配型 Greedy
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Section 4: 分配型 Greedy (Assignment / Distribution)")
    print("=" * 70)

    print("\n--- 4-1. Assign Cookies (LC 455) ---")
    for i, (g, s) in enumerate([
        ([1, 2, 3], [1, 1]),
        ([1, 2], [1, 2, 3]),
        ([10, 9, 8, 7], [5, 6, 7, 8]),
    ], 1):
        print(f"\n範例 {i}: g = {g}, s = {s}")
        result = find_content_children(g[:], s[:], verbose=True)
        print(f"答案: {result}")

    print("\n--- 4-2. Boats to Save People (LC 881) ---")
    for i, (people, limit) in enumerate([
        ([1, 2], 3),
        ([3, 2, 2, 1], 3),
        ([3, 5, 3, 4], 5),
    ], 1):
        print(f"\n範例 {i}: people = {people}, limit = {limit}")
        result = num_rescue_boats(people[:], limit, verbose=True)
        print(f"答案: {result}")

    print("\n--- 4-3. Partition Labels (LC 763) ---")
    for i, s in enumerate([
        "ababcbacadefegdehijhklij",
        "eccbbbbdec",
        "abcabc",
    ], 1):
        print(f"\n範例 {i}: s = \"{s}\"")
        result = partition_labels(s, verbose=True)
        print(f"答案: {result}")

    # ------------------------------------------------------------------
    # Section 5: 數字/字串型 Greedy
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Section 5: 數字/字串型 Greedy (Number / String)")
    print("=" * 70)

    print("\n--- 5-1. Remove K Digits (LC 402) ---")
    for i, (num, k) in enumerate([
        ("1432219", 3),
        ("10200", 1),
        ("9876", 2),
    ], 1):
        print(f"\n範例 {i}: num = \"{num}\", k = {k}")
        result = remove_k_digits(num, k, verbose=True)
        print(f"答案: \"{result}\"")

    print("\n--- 5-2. Reorganize String (LC 767) ---")
    for i, s in enumerate(["aab", "aaab", "aabbcc"], 1):
        print(f"\n範例 {i}: s = \"{s}\"")
        result = reorganize_string(s, verbose=True)
        print(f"答案: \"{result}\"")

    print("\n--- 5-3. Queue Reconstruction by Height (LC 406) ---")
    for i, people in enumerate([
        [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]],
        [[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]],
        [[9, 0], [7, 0], [1, 9], [3, 0], [2, 7], [5, 3],
         [6, 0], [3, 4], [6, 2], [5, 2]],
    ], 1):
        print(f"\n範例 {i}: people = {people}")
        result = reconstruct_queue([p[:] for p in people], verbose=True)
        print(f"答案: {result}")

    # ------------------------------------------------------------------
    # Section 6: Greedy vs DP 比較
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Section 6: Greedy vs DP 完整比較")
    print("=" * 70)

    print("\n--- 6-1. Jump Game: Greedy O(n) vs DP O(n^2) ---")
    nums = [2, 3, 1, 1, 4]
    print(f"\nnums = {nums}")
    print("\n[Greedy 解法]")
    can_jump(nums, verbose=True)
    print("\n[DP 解法] (同樣結果，但慢很多)")
    can_jump_dp(nums, verbose=True)

    print("\n--- 6-2. Coin Change: Greedy 失敗 vs DP 正確 ---")
    print("\n案例 A: coins=[1,5,10,25], amount=41（Greedy 成功）")
    print("[Greedy]")
    coin_change_greedy([1, 5, 10, 25], 41, verbose=True)
    print("[DP]")
    coin_change_dp([1, 5, 10, 25], 41, verbose=True)

    print("\n案例 B: coins=[1,3,4], amount=6（Greedy 失敗!）")
    print("[Greedy] → 會選 4+1+1 = 3 枚")
    coin_change_greedy([1, 3, 4], 6, verbose=True)
    print("[DP] → 正確答案 3+3 = 2 枚")
    coin_change_dp([1, 3, 4], 6, verbose=True)

    print("\n案例 C: coins=[1,7,10], amount=14（Greedy 失敗!）")
    print("[Greedy] → 會選 10+1+1+1+1 = 5 枚")
    coin_change_greedy([1, 7, 10], 14, verbose=True)
    print("[DP] → 正確答案 7+7 = 2 枚")
    coin_change_dp([1, 7, 10], 14, verbose=True)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Greedy 面試重點整理")
    print("=" * 70)
    print("""
    1. 區間問題（排序是關鍵！）
       - Merge Intervals: sort by start, 逐一合併
       - Non-overlapping: sort by END, 貪心保留結束早的
       - Meeting Rooms II: sort by start + min-heap

    2. 跳躍/選擇問題
       - Jump Game: 追蹤 farthest reach
       - Gas Station: total >= 0 保證有解, tank < 0 就 reset

    3. 分配問題（排序 + 雙指針）
       - Assign Cookies: 小餅乾配不貪心的小孩
       - Boats: 最輕配最重
       - Partition Labels: last occurrence 決定邊界

    4. 字串/數字（Monotonic Stack + Greedy）
       - Remove K Digits: 保持單調遞增
       - Reorganize String: max-heap 輪換

    5. Greedy vs DP 判斷
       - 能找到反例 → DP
       - Exchange Argument 成立 → Greedy
       - 問「方案數」→ DP
       - 問「最佳值」且有 Greedy Choice Property → Greedy
    """)


if __name__ == "__main__":
    main()
