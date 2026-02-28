"""
============================================================================
  LeetCode 刷題教學 #03 — HashMap / HashSet 完全攻略
  Target: Google / NVIDIA 面試準備 (Beginner Level)

  觀念：HashMap (dict) 用「鍵→值」做 O(1) 查找/計數/映射
       HashSet (set) 用「鍵存在性」做 O(1) 去重/成員檢查

  本檔可直接執行: python 03_HashMap_HashSet.py
============================================================================
"""
from typing import List, Dict, Optional
from collections import Counter, defaultdict


# ════════════════════════════════════════════════════════════════════════
#  Section 1: 計數型 HashMap (Frequency Counting)
#  核心觀念：用 dict 記錄「元素 → 出現次數 / 索引」
# ════════════════════════════════════════════════════════════════════════

# ── 1-1. Two Sum (LeetCode #1) ─────────────────────────────────────────
# 思路：遍歷時把 num→index 存進 map，查 complement 是否已存在
# Time: O(n)  Space: O(n)
def two_sum(nums: List[int], target: int, verbose: bool = False) -> List[int]:
    """回傳兩數索引，使其和 == target。"""
    lookup: Dict[int, int] = {}  # num → index
    if verbose:
        print(f"  nums={nums}, target={target}")
    for i, num in enumerate(nums):
        complement = target - num
        if verbose:
            found = complement in lookup
            print(f"  Step {i+1}: num={num}, complement={complement}, "
                  f"map={lookup} → {'FOUND!' if found else 'not found'}", end="")
        if complement in lookup:
            result = [lookup[complement], i]
            if verbose:
                print(f" → return {result}")
            return result
        lookup[num] = i
        if verbose:
            print(f" → map={lookup}")
    return []


# ── 1-2. Valid Anagram (LeetCode #242) ─────────────────────────────────
# 思路：統計兩字串各字元出現次數，比較是否相同
# Time: O(n)  Space: O(1) — 最多 26 個字母
def is_anagram(s: str, t: str, verbose: bool = False) -> bool:
    """判斷 t 是否為 s 的 anagram（字母重排）。"""
    if len(s) != len(t):
        if verbose:
            print(f"  長度不同 ({len(s)} vs {len(t)}) → False")
        return False

    count: Dict[str, int] = {}
    if verbose:
        print(f"  s=\"{s}\", t=\"{t}\"")
        print(f"  Phase 1: 掃描 s，建立字頻 map")
    for i, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        if verbose:
            print(f"    Step {i+1}: ch='{ch}' → count={dict(count)}")

    if verbose:
        print(f"  Phase 2: 掃描 t，遞減字頻")
    for i, ch in enumerate(t):
        count[ch] = count.get(ch, 0) - 1
        if verbose:
            print(f"    Step {i+1}: ch='{ch}' → count={dict(count)}")
        if count[ch] < 0:
            if verbose:
                print(f"    '{ch}' 次數 < 0 → False")
            return False

    result = all(v == 0 for v in count.values())
    if verbose:
        print(f"  所有字頻歸零? → {result}")
    return result


# ── 1-3. Top K Frequent Elements (LeetCode #347) ──────────────────────
# 思路：先統計頻率，再用 bucket sort — bucket[freq] = [元素們]
# Time: O(n)  Space: O(n)
def top_k_frequent(nums: List[int], k: int, verbose: bool = False) -> List[int]:
    """回傳出現次數最多的前 k 個元素。"""
    # Step 1: 計數
    freq: Dict[int, int] = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1
    if verbose:
        print(f"  nums={nums}, k={k}")
        print(f"  Step 1 頻率表: {freq}")

    # Step 2: Bucket Sort — index=頻率, value=元素列表
    n = len(nums)
    buckets: List[List[int]] = [[] for _ in range(n + 1)]
    for num, cnt in freq.items():
        buckets[cnt].append(num)
    if verbose:
        print(f"  Step 2 Buckets (index=頻率):")
        for i in range(n, -1, -1):
            if buckets[i]:
                print(f"    bucket[{i}] = {buckets[i]}")

    # Step 3: 從高頻 bucket 往低頻取，取滿 k 個
    result: List[int] = []
    for i in range(n, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                if verbose:
                    print(f"  Step 3 取前 {k} 個: {result}")
                return result
    return result


# ════════════════════════════════════════════════════════════════════════
#  Section 2: 映射型 HashMap (Mapping / Lookup)
#  核心觀念：用 dict 建立「某種 key → 分組 / 對應關係」
# ════════════════════════════════════════════════════════════════════════

# ── 2-1. Group Anagrams (LeetCode #49) ─────────────────────────────────
# 思路：排序後的字串當 key，原字串 append 到對應 list
# Time: O(n * k log k)  Space: O(n * k)  k=最長字串長度
def group_anagrams(strs: List[str], verbose: bool = False) -> List[List[str]]:
    """把 anagram 分到同一組。"""
    groups: Dict[str, List[str]] = defaultdict(list)
    if verbose:
        print(f"  strs={strs}")
    for i, s in enumerate(strs):
        key = "".join(sorted(s))
        groups[key].append(s)
        if verbose:
            print(f"  Step {i+1}: \"{s}\" → sorted key=\"{key}\" → groups={dict(groups)}")
    result = list(groups.values())
    if verbose:
        print(f"  最終分組: {result}")
    return result


# ── 2-2. Isomorphic Strings (LeetCode #205) ───────────────────────────
# 思路：兩個 map 互相映射 s→t 和 t→s，確保一對一
# Time: O(n)  Space: O(n)
def is_isomorphic(s: str, t: str, verbose: bool = False) -> bool:
    """判斷 s 和 t 是否同構（字元可一對一替換）。"""
    if len(s) != len(t):
        return False
    s_to_t: Dict[str, str] = {}
    t_to_s: Dict[str, str] = {}
    if verbose:
        print(f"  s=\"{s}\", t=\"{t}\"")
    for i in range(len(s)):
        sc, tc = s[i], t[i]
        if verbose:
            print(f"  Step {i+1}: s[{i}]='{sc}', t[{i}]='{tc}', "
                  f"s→t={s_to_t}, t→s={t_to_s}", end="")
        # 檢查 s→t 映射一致性
        if sc in s_to_t:
            if s_to_t[sc] != tc:
                if verbose:
                    print(f" → '{sc}'已映射到'{s_to_t[sc]}' != '{tc}' → False")
                return False
        # 檢查 t→s 映射一致性
        if tc in t_to_s:
            if t_to_s[tc] != sc:
                if verbose:
                    print(f" → '{tc}'已被'{t_to_s[tc]}'映射 != '{sc}' → False")
                return False
        s_to_t[sc] = tc
        t_to_s[tc] = sc
        if verbose:
            print(f" → OK, s→t={s_to_t}, t→s={t_to_s}")
    if verbose:
        print(f"  全部配對成功 → True")
    return True


# ── 2-3. Word Pattern (LeetCode #290) ─────────────────────────────────
# 思路：跟 Isomorphic Strings 幾乎一樣，pattern 字元↔單字 一對一映射
# Time: O(n)  Space: O(n)
def word_pattern(pattern: str, s: str, verbose: bool = False) -> bool:
    """判斷字串 s 的單字是否符合 pattern 的對應關係。"""
    words = s.split()
    if len(pattern) != len(words):
        if verbose:
            print(f"  pattern 長度 {len(pattern)} != words 數量 {len(words)} → False")
        return False

    p_to_w: Dict[str, str] = {}
    w_to_p: Dict[str, str] = {}
    if verbose:
        print(f"  pattern=\"{pattern}\", words={words}")
    for i in range(len(pattern)):
        p, w = pattern[i], words[i]
        if verbose:
            print(f"  Step {i+1}: p='{p}', w=\"{w}\", "
                  f"p→w={p_to_w}, w→p={w_to_p}", end="")
        if p in p_to_w and p_to_w[p] != w:
            if verbose:
                print(f" → '{p}'已映射\"{p_to_w[p]}\" != \"{w}\" → False")
            return False
        if w in w_to_p and w_to_p[w] != p:
            if verbose:
                print(f" → \"{w}\"已被'{w_to_p[w]}'映射 != '{p}' → False")
            return False
        p_to_w[p] = w
        w_to_p[w] = p
        if verbose:
            print(f" → OK")
    if verbose:
        print(f"  全部配對成功 → True")
    return True


# ════════════════════════════════════════════════════════════════════════
#  Section 3: HashSet 去重與查找
#  核心觀念：set 只存「有沒有」，O(1) 成員檢查，自動去重
# ════════════════════════════════════════════════════════════════════════

# ── 3-1. Contains Duplicate (LeetCode #217) ────────────────────────────
# 思路：邊掃邊加 set，遇到已存在的就回傳 True
# Time: O(n)  Space: O(n)
def contains_duplicate(nums: List[int], verbose: bool = False) -> bool:
    """判斷陣列中是否有重複元素。"""
    seen: set = set()
    if verbose:
        print(f"  nums={nums}")
    for i, num in enumerate(nums):
        if verbose:
            print(f"  Step {i+1}: num={num}, seen={seen}", end="")
        if num in seen:
            if verbose:
                print(f" → {num} 已存在! → True")
            return True
        seen.add(num)
        if verbose:
            print(f" → add → seen={seen}")
    if verbose:
        print(f"  掃完無重複 → False")
    return False


# ── 3-2. Intersection of Two Arrays (LeetCode #349) ───────────────────
# 思路：set1 & set2 即為交集
# Time: O(n+m)  Space: O(n+m)
def intersection(nums1: List[int], nums2: List[int],
                 verbose: bool = False) -> List[int]:
    """回傳兩陣列的交集（不重複）。"""
    set1 = set(nums1)
    set2 = set(nums2)
    if verbose:
        print(f"  nums1={nums1} → set1={set1}")
        print(f"  nums2={nums2} → set2={set2}")
        print(f"  逐一檢查 set1 中的元素是否在 set2:")
    result: List[int] = []
    for num in set1:
        if verbose:
            print(f"    {num} in set2? → {num in set2}")
        if num in set2:
            result.append(num)
    result.sort()  # 排序讓輸出穩定
    if verbose:
        print(f"  交集結果: {result}")
    return result


# ── 3-3. Longest Consecutive Sequence (LeetCode #128) ─────────────────
# 思路：全部丟 set，找每段連續序列的起點（num-1 不在 set 裡）
#       從起點往上數，記錄最長長度
# Time: O(n)  Space: O(n)
def longest_consecutive(nums: List[int], verbose: bool = False) -> int:
    """找出最長連續整數序列的長度。"""
    if not nums:
        return 0
    num_set = set(nums)
    best = 0
    if verbose:
        print(f"  nums={nums}")
        print(f"  num_set={sorted(num_set)}")
    for num in num_set:
        # 只從序列起點開始數（num-1 不在 set 裡 → num 是起點）
        if num - 1 not in num_set:
            cur = num
            length = 1
            if verbose:
                print(f"  起點 {num}: ", end="")
            while cur + 1 in num_set:
                cur += 1
                length += 1
            if verbose:
                print(f"連續到 {cur}, 長度={length}")
            best = max(best, length)
        else:
            if verbose:
                print(f"  跳過 {num} (因為 {num-1} 在 set 中，非起點)")
    if verbose:
        print(f"  最長連續序列長度: {best}")
    return best


# ════════════════════════════════════════════════════════════════════════
#  Section 4: 前綴和 + HashMap (Prefix Sum + HashMap)
#  核心觀念：prefix_sum[j] - prefix_sum[i] = subarray sum(i..j-1)
#           用 map 記錄「prefix_sum → 出現次數/索引」達 O(n)
# ════════════════════════════════════════════════════════════════════════

# ── 4-1. Subarray Sum Equals K (LeetCode #560) ────────────────────────
# 思路：prefix_sum - k 如果之前出現過，代表中間那段 subarray 和 == k
# Time: O(n)  Space: O(n)
def subarray_sum(nums: List[int], k: int, verbose: bool = False) -> int:
    """回傳和為 k 的連續子陣列個數。"""
    prefix_count: Dict[int, int] = {0: 1}  # prefix_sum=0 出現 1 次（空陣列）
    curr_sum = 0
    result = 0
    if verbose:
        print(f"  nums={nums}, k={k}")
        print(f"  初始 prefix_count={prefix_count}, curr_sum=0, result=0")
    for i, num in enumerate(nums):
        curr_sum += num
        need = curr_sum - k
        if verbose:
            print(f"  Step {i+1}: num={num}, curr_sum={curr_sum}, "
                  f"need={need} (={curr_sum}-{k})", end="")
        if need in prefix_count:
            result += prefix_count[need]
            if verbose:
                print(f" → need 在 map 中出現 {prefix_count[need]} 次, "
                      f"result={result}", end="")
        prefix_count[curr_sum] = prefix_count.get(curr_sum, 0) + 1
        if verbose:
            print(f" → prefix_count={dict(prefix_count)}")
    if verbose:
        print(f"  子陣列個數: {result}")
    return result


# ── 4-2. Continuous Subarray Sum (LeetCode #523) ──────────────────────
# 思路：若 prefix_sum[j] % k == prefix_sum[i] % k 且 j-i >= 2
#       則 subarray(i..j-1) 的和是 k 的倍數
#       用 map 記錄「餘數 → 最早出現的 index」
# Time: O(n)  Space: O(n)
def check_subarray_sum(nums: List[int], k: int,
                       verbose: bool = False) -> bool:
    """判斷是否存在長度 >= 2 的子陣列，其和為 k 的倍數。"""
    # 餘數 0 初始出現在 index=-1（代表空前綴）
    remainder_map: Dict[int, int] = {0: -1}
    curr_sum = 0
    if verbose:
        print(f"  nums={nums}, k={k}")
        print(f"  初始 remainder_map={remainder_map}")
    for i, num in enumerate(nums):
        curr_sum += num
        rem = curr_sum % k if k != 0 else curr_sum
        if verbose:
            print(f"  Step {i+1}: num={num}, curr_sum={curr_sum}, "
                  f"rem={rem} (={curr_sum}%{k})", end="")
        if rem in remainder_map:
            prev_idx = remainder_map[rem]
            length = i - prev_idx
            if verbose:
                print(f" → rem 最早在 index={prev_idx}, 長度={length}", end="")
            if length >= 2:
                if verbose:
                    print(f" >= 2 → True")
                return True
            if verbose:
                print(f" < 2, 不更新 map")
        else:
            remainder_map[rem] = i
            if verbose:
                print(f" → 新餘數, remainder_map={remainder_map}")
    if verbose:
        print(f"  找不到 → False")
    return False


# ════════════════════════════════════════════════════════════════════════
#  Section 5: HashMap vs HashSet vs Array Counter 比較
# ════════════════════════════════════════════════════════════════════════

def comparison_guide():
    """印出 HashMap / HashSet / Array Counter 的使用時機比較表。"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  Section 5: HashMap vs HashSet vs Array Counter 比較               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  ┌──────────────────┬──────────┬──────────┬────────────────────┐   ║
║  │ 工具              │ 查找     │ 插入     │ 適用場景           │   ║
║  ├──────────────────┼──────────┼──────────┼────────────────────┤   ║
║  │ dict (HashMap)   │ O(1) avg │ O(1) avg │ key→value 映射     │   ║
║  │ set  (HashSet)   │ O(1) avg │ O(1) avg │ 去重/成員檢查      │   ║
║  │ list (Counter)   │ O(1)     │ O(1)     │ key 範圍小且已知   │   ║
║  └──────────────────┴──────────┴──────────┴────────────────────┘   ║
║                                                                     ║
║  【Decision Framework 決策框架】                                    ║
║                                                                     ║
║  Q1: 你需要「值」嗎? (不只是存在性)                                ║
║      → YES → 用 dict                                               ║
║      → NO  → Q2                                                    ║
║                                                                     ║
║  Q2: 你只需要判斷「有沒有見過」?                                   ║
║      → YES → 用 set                                                ║
║      → NO  → Q3                                                    ║
║                                                                     ║
║  Q3: key 的範圍是否小且固定? (例如 26 個英文字母 / 0-9 數字)       ║
║      → YES → 用 list[size] 當 counter (最快, cache-friendly)       ║
║      → NO  → 用 dict                                               ║
║                                                                     ║
║  【Performance 效能比較】                                           ║
║                                                                     ║
║  場景: 統計 100 萬個小寫字母的頻率                                  ║
║  ┌──────────────────┬──────────────┬──────────────────────────┐    ║
║  │ 方法              │ 速度 (相對)  │ 備註                     │    ║
║  ├──────────────────┼──────────────┼──────────────────────────┤    ║
║  │ list[26]         │ 1x (最快)    │ 直接 index 存取          │    ║
║  │ dict             │ ~2-3x        │ hash 計算 + 碰撞處理     │    ║
║  │ Counter()        │ ~2-3x        │ 底層是 dict, 方便但稍慢  │    ║
║  │ set              │ N/A          │ 不適合計數, 只能記有/無   │    ║
║  └──────────────────┴──────────────┴──────────────────────────┘    ║
║                                                                     ║
║  【何時用 collections.Counter?】                                    ║
║  - 需要 .most_common(k) 時                                         ║
║  - 需要兩個 Counter 相減時                                          ║
║  - 程式碼簡潔比效能重要時                                           ║
║                                                                     ║
║  【面試小技巧 Interview Tips】                                      ║
║  1. 先跟面試官確認: input 範圍 → 決定用 list 還是 dict             ║
║  2. Two Sum 類型 → 邊掃邊建 map (one-pass)                         ║
║  3. Anagram 類型 → sorted string 當 key, 或用 Counter              ║
║  4. Prefix Sum 類型 → map 存「前綴和→次數」                        ║
║  5. Consecutive 類型 → set + 找起點                                 ║
╚══════════════════════════════════════════════════════════════════════╝
""")


# ════════════════════════════════════════════════════════════════════════
#  Main — 執行所有範例
# ════════════════════════════════════════════════════════════════════════

def run_section_1():
    print("=" * 70)
    print("  Section 1: 計數型 HashMap (Frequency Counting)")
    print("=" * 70)

    # ── Two Sum ──
    print("\n── 1-1. Two Sum (LeetCode #1) ──")
    print("【觀念】遍歷一次，map 存 {數值: 索引}，查 complement = target - num")

    print("\n範例 1: nums=[2,7,11,15], target=9")
    r = two_sum([2, 7, 11, 15], 9, verbose=True)
    print(f"  答案: {r}")
    assert r == [0, 1]

    print("\n範例 2: nums=[3,2,4], target=6")
    r = two_sum([3, 2, 4], 6, verbose=True)
    print(f"  答案: {r}")
    assert r == [1, 2]

    print("\n範例 3: nums=[1,5,3,7,2,8], target=10")
    r = two_sum([1, 5, 3, 7, 2, 8], 10, verbose=True)
    print(f"  答案: {r}")
    assert r == [2, 3]

    # ── Valid Anagram ──
    print("\n── 1-2. Valid Anagram (LeetCode #242) ──")
    print("【觀念】統計字頻，s 加 t 減，全部歸零即 anagram")

    print("\n範例 1: s=\"anagram\", t=\"nagaram\"")
    r = is_anagram("anagram", "nagaram", verbose=True)
    print(f"  答案: {r}")
    assert r is True

    print("\n範例 2: s=\"rat\", t=\"car\"")
    r = is_anagram("rat", "car", verbose=True)
    print(f"  答案: {r}")
    assert r is False

    print("\n範例 3: s=\"listen\", t=\"silent\"")
    r = is_anagram("listen", "silent", verbose=True)
    print(f"  答案: {r}")
    assert r is True

    # ── Top K Frequent ──
    print("\n── 1-3. Top K Frequent Elements (LeetCode #347) ──")
    print("【觀念】先計頻率，再 bucket sort — bucket[freq] = [元素]")

    print("\n範例 1: nums=[1,1,1,2,2,3], k=2")
    r = top_k_frequent([1, 1, 1, 2, 2, 3], 2, verbose=True)
    print(f"  答案: {r}")
    assert set(r) == {1, 2}

    print("\n範例 2: nums=[4,4,4,6,6,6,6,2], k=1")
    r = top_k_frequent([4, 4, 4, 6, 6, 6, 6, 2], 1, verbose=True)
    print(f"  答案: {r}")
    assert r == [6]

    print("\n範例 3: nums=[7,7,8,8,9], k=3")
    r = top_k_frequent([7, 7, 8, 8, 9], 3, verbose=True)
    print(f"  答案: {r}")
    assert len(r) == 3


def run_section_2():
    print("\n" + "=" * 70)
    print("  Section 2: 映射型 HashMap (Mapping / Lookup)")
    print("=" * 70)

    # ── Group Anagrams ──
    print("\n── 2-1. Group Anagrams (LeetCode #49) ──")
    print("【觀念】sorted(word) 當 key，同 key 的字歸為一組")

    print("\n範例 1: [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]")
    r = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"], verbose=True)
    print(f"  答案: {r}")

    print("\n範例 2: [\"\"]")
    r = group_anagrams([""], verbose=True)
    print(f"  答案: {r}")

    print("\n範例 3: [\"abc\",\"bca\",\"xyz\",\"zyx\",\"aaa\"]")
    r = group_anagrams(["abc", "bca", "xyz", "zyx", "aaa"], verbose=True)
    print(f"  答案: {r}")

    # ── Isomorphic Strings ──
    print("\n── 2-2. Isomorphic Strings (LeetCode #205) ──")
    print("【觀念】兩個 map 雙向映射，確保一對一關係")

    print("\n範例 1: s=\"egg\", t=\"add\"")
    r = is_isomorphic("egg", "add", verbose=True)
    print(f"  答案: {r}")
    assert r is True

    print("\n範例 2: s=\"foo\", t=\"bar\"")
    r = is_isomorphic("foo", "bar", verbose=True)
    print(f"  答案: {r}")
    assert r is False

    print("\n範例 3: s=\"paper\", t=\"title\"")
    r = is_isomorphic("paper", "title", verbose=True)
    print(f"  答案: {r}")
    assert r is True

    # ── Word Pattern ──
    print("\n── 2-3. Word Pattern (LeetCode #290) ──")
    print("【觀念】pattern 字元 ↔ 單字 一對一映射，與 Isomorphic 同理")

    print("\n範例 1: pattern=\"abba\", s=\"dog cat cat dog\"")
    r = word_pattern("abba", "dog cat cat dog", verbose=True)
    print(f"  答案: {r}")
    assert r is True

    print("\n範例 2: pattern=\"abba\", s=\"dog cat cat fish\"")
    r = word_pattern("abba", "dog cat cat fish", verbose=True)
    print(f"  答案: {r}")
    assert r is False

    print("\n範例 3: pattern=\"abba\", s=\"dog dog dog dog\"")
    r = word_pattern("abba", "dog dog dog dog", verbose=True)
    print(f"  答案: {r}")
    assert r is False


def run_section_3():
    print("\n" + "=" * 70)
    print("  Section 3: HashSet 去重與查找")
    print("=" * 70)

    # ── Contains Duplicate ──
    print("\n── 3-1. Contains Duplicate (LeetCode #217) ──")
    print("【觀念】邊掃邊加 set，遇到已存在的就是重複")

    print("\n範例 1: nums=[1,2,3,1]")
    r = contains_duplicate([1, 2, 3, 1], verbose=True)
    print(f"  答案: {r}")
    assert r is True

    print("\n範例 2: nums=[1,2,3,4]")
    r = contains_duplicate([1, 2, 3, 4], verbose=True)
    print(f"  答案: {r}")
    assert r is False

    print("\n範例 3: nums=[5,3,5,8,3]")
    r = contains_duplicate([5, 3, 5, 8, 3], verbose=True)
    print(f"  答案: {r}")
    assert r is True

    # ── Intersection of Two Arrays ──
    print("\n── 3-2. Intersection of Two Arrays (LeetCode #349) ──")
    print("【觀念】轉 set 後取交集 O(n+m)")

    print("\n範例 1: nums1=[1,2,2,1], nums2=[2,2]")
    r = intersection([1, 2, 2, 1], [2, 2], verbose=True)
    print(f"  答案: {r}")
    assert r == [2]

    print("\n範例 2: nums1=[4,9,5], nums2=[9,4,9,8,4]")
    r = intersection([4, 9, 5], [9, 4, 9, 8, 4], verbose=True)
    print(f"  答案: {r}")
    assert set(r) == {4, 9}

    print("\n範例 3: nums1=[1,2,3], nums2=[4,5,6]")
    r = intersection([1, 2, 3], [4, 5, 6], verbose=True)
    print(f"  答案: {r}")
    assert r == []

    # ── Longest Consecutive Sequence ──
    print("\n── 3-3. Longest Consecutive Sequence (LeetCode #128) ──")
    print("【觀念】全部丟 set，找起點(num-1 不在 set)，從起點往上數")

    print("\n範例 1: nums=[100,4,200,1,3,2]")
    r = longest_consecutive([100, 4, 200, 1, 3, 2], verbose=True)
    print(f"  答案: {r}")
    assert r == 4

    print("\n範例 2: nums=[0,3,7,2,5,8,4,6,0,1]")
    r = longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], verbose=True)
    print(f"  答案: {r}")
    assert r == 9

    print("\n範例 3: nums=[10,30,20]")
    r = longest_consecutive([10, 30, 20], verbose=True)
    print(f"  答案: {r}")
    assert r == 1


def run_section_4():
    print("\n" + "=" * 70)
    print("  Section 4: 前綴和 + HashMap (Prefix Sum + HashMap)")
    print("=" * 70)

    # ── Subarray Sum Equals K ──
    print("\n── 4-1. Subarray Sum Equals K (LeetCode #560) ──")
    print("【觀念】prefix_sum - k 若之前出現過 → 中間那段和 == k")
    print("        map 存 {prefix_sum: 出現次數}")

    print("\n範例 1: nums=[1,1,1], k=2")
    r = subarray_sum([1, 1, 1], 2, verbose=True)
    print(f"  答案: {r}")
    assert r == 2

    print("\n範例 2: nums=[1,2,3], k=3")
    r = subarray_sum([1, 2, 3], 3, verbose=True)
    print(f"  答案: {r}")
    assert r == 2

    print("\n範例 3: nums=[3,4,7,2,-3,1,4,2], k=7")
    r = subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7, verbose=True)
    print(f"  答案: {r}")
    assert r == 4

    # ── Continuous Subarray Sum ──
    print("\n── 4-2. Continuous Subarray Sum (LeetCode #523) ──")
    print("【觀念】prefix_sum % k 相同 → 中間子陣列和是 k 的倍數")
    print("        map 存 {餘數: 最早出現的 index}，長度 >= 2 才算")

    print("\n範例 1: nums=[23,2,4,6,7], k=6")
    r = check_subarray_sum([23, 2, 4, 6, 7], 6, verbose=True)
    print(f"  答案: {r}")
    assert r is True

    print("\n範例 2: nums=[23,2,6,4,7], k=13 (找不到)")
    r = check_subarray_sum([23, 2, 6, 4, 7], 13, verbose=True)
    print(f"  答案: {r}")
    assert r is False

    print("\n範例 3: nums=[5,0,0,0], k=3")
    r = check_subarray_sum([5, 0, 0, 0], 3, verbose=True)
    print(f"  答案: {r}")
    assert r is True


def main():
    print("╔" + "═" * 68 + "╗")
    print("║  LeetCode 刷題教學 #03 — HashMap / HashSet 完全攻略             ║")
    print("║  Target: Google / NVIDIA | Beginner Level                       ║")
    print("╚" + "═" * 68 + "╝")

    run_section_1()
    run_section_2()
    run_section_3()
    run_section_4()

    # Section 5: 比較表
    print("\n" + "=" * 70)
    comparison_guide()

    print("=" * 70)
    print("  ALL EXAMPLES PASSED — HashMap / HashSet 攻略完成!")
    print("=" * 70)
    print("""
  【本檔重點回顧 Summary】

  1. 計數型 HashMap: Two Sum / Anagram / Top K Frequent
     → map 存 {元素: 次數或索引}

  2. 映射型 HashMap: Group Anagrams / Isomorphic / Word Pattern
     → map 存 {key: 對應值}，注意雙向映射確保一對一

  3. HashSet 去重: Contains Dup / Intersection / Longest Consecutive
     → set 存「有沒有出現過」，O(1) 查找

  4. Prefix Sum + HashMap: Subarray Sum K / Continuous Subarray Sum
     → map 存 {前綴和(或餘數): 次數或最早索引}

  5. 選擇工具:
     - 需要 key→value → dict
     - 只需存在性  → set
     - key 範圍小且固定 → list (最快)

  Time Complexity 總結:
  ┌─────────────────────────────┬────────┬────────┐
  │ 題目                         │ Time   │ Space  │
  ├─────────────────────────────┼────────┼────────┤
  │ Two Sum                     │ O(n)   │ O(n)   │
  │ Valid Anagram               │ O(n)   │ O(1)*  │
  │ Top K Frequent              │ O(n)   │ O(n)   │
  │ Group Anagrams              │O(nklogk)│ O(nk) │
  │ Isomorphic Strings          │ O(n)   │ O(n)   │
  │ Word Pattern                │ O(n)   │ O(n)   │
  │ Contains Duplicate          │ O(n)   │ O(n)   │
  │ Intersection of Two Arrays  │ O(n+m) │ O(n+m) │
  │ Longest Consecutive Seq     │ O(n)   │ O(n)   │
  │ Subarray Sum Equals K       │ O(n)   │ O(n)   │
  │ Continuous Subarray Sum     │ O(n)   │ O(n)   │
  └─────────────────────────────┴────────┴────────┘
  * O(1) 因為最多 26 個字母
""")


if __name__ == "__main__":
    main()
