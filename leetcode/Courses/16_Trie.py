#!/usr/bin/env python3
"""
=============================================================================
LeetCode Trie (Prefix Tree) 模式完全攻略
=============================================================================
目標讀者：準備 Google / NVIDIA 面試的初學者
教學風格：每題 3 個範例，每個範例都有完整的 step-by-step 數值追蹤
語言：繁體中文解說 + English technical terms

直接執行：python 16_Trie.py
=============================================================================
"""
from typing import List, Dict, Optional


# ============================================================================
# Section 1: Trie 基礎概念與實作 (Trie Fundamentals)
# ============================================================================
# Trie（字典樹/前綴樹/Prefix Tree）— 高效存取和搜尋字串集合。
# 核心：每個節點=一個字元, is_end 標記單字結尾, 共享前綴節省空間。
#
#  插入 "apple","app","apt":    root → a → p → p* → l → e*
#                                              \→ t*
#  (* = is_end, 完整單字結尾)
#
# Time: insert/search/startsWith 都是 O(L), L=字串長度
# Space: 最差 O(N*L*26)，實際因前綴共享遠小於此
# ============================================================================


# ---------------------------------------------------------------------------
# 1-1. Implement Trie / Prefix Tree (LeetCode 208)
# ---------------------------------------------------------------------------
# 題意：實作一個 Trie，支援以下操作：
#   - insert(word): 插入一個單字
#   - search(word): 搜尋完整單字（必須 is_end=True）
#   - startsWith(prefix): 檢查是否有任何單字以此 prefix 開頭
#
# INSERT 範例:
#   insert("apple"): root→a→p→p→l→e* (全部 create)
#   insert("app"):   root→a(reuse)→p(reuse)→p*(mark end, reuse)
#   insert("apt"):   root→a(reuse)→p(reuse)→t*(create, 分岔)
#   最終: root→a→p→{p*→l→e*, t*}
#
# SEARCH 範例:
#   search("apple")→True  (走完且 is_end=True)
#   search("apx")→False   ('x' 不存在)
#   search("ap")→False    (路徑存在但 is_end=False)
#
# STARTSWITH 範例:
#   startsWith("app")→True  (路徑存在)
#   startsWith("ap")→True   (路徑存在)
#   startsWith("b")→False   ('b' 不在 root.children)

class TrieNode:
    """Trie 的節點。每個節點包含 children dict 和 is_end 標記。"""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Trie:
    """LeetCode 208 - Implement Trie (Prefix Tree)."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, verbose: bool = False) -> None:
        """插入一個單字到 Trie 中。Time: O(L), Space: O(L)"""
        node = self.root
        if verbose:
            print(f"  insert(\"{word}\"):")
        for i, ch in enumerate(word):
            if ch not in node.children:
                node.children[ch] = TrieNode()
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (create node)")
            else:
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (node exists, reuse)")
            node = node.children[ch]
        node.is_end = True
        if verbose:
            print(f"    Mark is_end=True at '{word[-1]}' → \"{word}\" 插入完成")

    def search(self, word: str, verbose: bool = False) -> bool:
        """搜尋完整單字。必須走完所有字元且 is_end=True。"""
        node = self.root
        if verbose:
            print(f"  search(\"{word}\"):")
        for i, ch in enumerate(word):
            if ch not in node.children:
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (NOT found) ✗ → return False")
                return False
            if verbose:
                print(f"    Step {i+1}: → '{ch}' (found)")
            node = node.children[ch]
        if verbose:
            status = "is_end=True ✓" if node.is_end else "is_end=False ✗"
            print(f"    到達結尾: {status} → return {node.is_end}")
        return node.is_end

    def starts_with(self, prefix: str, verbose: bool = False) -> bool:
        """檢查是否有單字以 prefix 開頭。只需路徑存在即可。"""
        node = self.root
        if verbose:
            print(f"  startsWith(\"{prefix}\"):")
        for i, ch in enumerate(prefix):
            if ch not in node.children:
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (NOT found) ✗ → return False")
                return False
            if verbose:
                print(f"    Step {i+1}: → '{ch}' (found)")
            node = node.children[ch]
        if verbose:
            print(f"    路徑完整存在 ✓ → return True")
        return True


def demo_trie_basic():
    """示範 Trie 基本操作。"""
    print("=" * 60)
    print("1-1. Implement Trie (LeetCode 208)")
    print("=" * 60)

    trie = Trie()

    print("\n--- INSERT 範例 ---")
    trie.insert("apple", verbose=True)
    print()
    trie.insert("app", verbose=True)
    print()
    trie.insert("apt", verbose=True)

    print("\n--- SEARCH 範例 ---")
    print(f"\n  結果: search('apple') = {trie.search('apple', verbose=True)}")
    print(f"\n  結果: search('apx') = {trie.search('apx', verbose=True)}")
    print(f"\n  結果: search('ap') = {trie.search('ap', verbose=True)}")

    print("\n--- STARTSWITH 範例 ---")
    print(f"\n  結果: startsWith('app') = {trie.starts_with('app', verbose=True)}")
    print(f"\n  結果: startsWith('ap') = {trie.starts_with('ap', verbose=True)}")
    print(f"\n  結果: startsWith('b') = {trie.starts_with('b', verbose=True)}")
    print()


# ============================================================================
# Section 2: Trie 應用題 (Trie Applications)
# ============================================================================


# ---------------------------------------------------------------------------
# 2-1. Word Search II (LeetCode 212)
# ---------------------------------------------------------------------------
# 題意：給定一個 m×n 字母矩陣 board 和一組單字 words，
#       找出所有能在 board 上用相鄰格子拼出的單字。
# 策略：先把 words 建成 Trie，然後對 board 每個格子做 DFS backtracking。
#       Trie 讓我們能「提前剪枝」— 如果當前路徑不是任何 word 的 prefix，就停。
#
# 範例 1: board=[["o","a","n"],["e","t","h"]], words=["oan","an"]
#   Trie: root→{o→a→n*, a→n*}
#   DFS(0,0)='o'→'a'→'n'(end!)→"oan"; DFS(0,1)='a'→'n'(end!)→"an"
#   結果: ["oan","an"]
#
# 範例 2: board=[["a","b"],["c","d"]], words=["ab","ba","abc"]
#   DFS(0,0)→"ab"found; DFS(0,1)→"ba"found; "abc"不可能(b,c不相鄰)
#
# 範例 3: board=[["a"]], words=["a","b"] → ["a"] (b 不在 board)

def find_words(board: List[List[str]], words: List[str],
               verbose: bool = False) -> List[str]:
    """LeetCode 212 - Word Search II. Trie + DFS backtracking."""
    # Step 1: 建 Trie
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.word = w  # 儲存完整單字方便回收

    if verbose:
        print(f"  Board: {board}")
        print(f"  Words: {words}")
        print(f"  Trie built for {words}")

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r: int, c: int, node: TrieNode, path: str, step: int):
        if node.is_end:
            result.append(node.word)
            if verbose:
                print(f"    {'  ' * step}★ Found \"{node.word}\"!")
            node.is_end = False  # 避免重複加入

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        ch = board[r][c]
        if ch == '#' or ch not in node.children:
            return

        if verbose:
            print(f"    {'  ' * step}Step {step}: ({r},{c})='{ch}', path=\"{path + ch}\"")

        board[r][c] = '#'  # mark visited
        next_node = node.children[ch]
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, next_node, path + ch, step + 1)
        board[r][c] = ch  # backtrack

        # 剪枝優化：若子樹已空，刪除節點
        if not next_node.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root.children:
                if verbose:
                    print(f"  DFS from ({r},{c})='{board[r][c]}':")
                dfs(r, c, root, "", 1)

    if verbose:
        print(f"  結果: {result}")
    return result


def demo_word_search_ii():
    """示範 Word Search II。"""
    print("=" * 60)
    print("2-1. Word Search II (LeetCode 212)")
    print("=" * 60)

    # 範例 1
    print("\n--- 範例 1 ---")
    board1 = [["o", "a", "n"], ["e", "t", "h"]]
    find_words(board1, ["oan", "an"], verbose=True)

    # 範例 2
    print("\n--- 範例 2 ---")
    board2 = [["a", "b"], ["c", "d"]]
    find_words(board2, ["ab", "ba", "abc"], verbose=True)

    # 範例 3
    print("\n--- 範例 3 ---")
    board3 = [["a"]]
    find_words(board3, ["a", "b"], verbose=True)
    print()


# ---------------------------------------------------------------------------
# 2-2. Design Add and Search Words (LeetCode 211)
# ---------------------------------------------------------------------------
# 題意：設計資料結構 WordDictionary，支援：
#   - addWord(word): 新增單字
#   - search(word): 搜尋單字，'.' 可匹配任意一個字母
#
# 關鍵：search 遇到 '.' 時，必須對當前節點的「所有 children」做 DFS。
#
# 範例 1: add("bad"), search("b.d")→True  ('.'匹配'a')
# 範例 2: add("dad"),add("mad"), search(".ad")→True ('.'匹配'd'或'm')
# 範例 3: add("bat"), search("b..")→True ('.'匹配'a'再匹配't')

class WordDictionary:
    """LeetCode 211 - Design Add and Search Words Data Structure."""

    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str, verbose: bool = False) -> None:
        """新增單字。Time: O(L)"""
        node = self.root
        if verbose:
            print(f"  addWord(\"{word}\"):")
        for i, ch in enumerate(word):
            if ch not in node.children:
                node.children[ch] = TrieNode()
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (create)")
            else:
                if verbose:
                    print(f"    Step {i+1}: → '{ch}' (exists)")
            node = node.children[ch]
        node.is_end = True
        if verbose:
            print(f"    Mark is_end=True → \"{word}\" done")

    def search(self, word: str, verbose: bool = False) -> bool:
        """搜尋單字，'.' 可匹配任意字母。Time: worst O(26^L)"""
        if verbose:
            print(f"  search(\"{word}\"):")

        def dfs(idx: int, node: TrieNode, depth: int) -> bool:
            if idx == len(word):
                if verbose:
                    indent = "    " + "  " * depth
                    status = "is_end=True ✓" if node.is_end else "is_end=False ✗"
                    print(f"{indent}到達結尾: {status}")
                return node.is_end

            ch = word[idx]
            indent = "    " + "  " * depth

            if ch == '.':
                if verbose:
                    keys = list(node.children.keys())
                    print(f"{indent}Step {idx+1}: '.' wildcard → "
                          f"try all children: {keys}")
                for key in node.children:
                    if verbose:
                        print(f"{indent}  try '{key}':")
                    if dfs(idx + 1, node.children[key], depth + 1):
                        return True
                if verbose:
                    print(f"{indent}  所有 branch 都失敗 ✗")
                return False
            else:
                if ch not in node.children:
                    if verbose:
                        print(f"{indent}Step {idx+1}: '{ch}' NOT found ✗")
                    return False
                if verbose:
                    print(f"{indent}Step {idx+1}: '{ch}' found")
                return dfs(idx + 1, node.children[ch], depth + 1)

        result = dfs(0, self.root, 0)
        if verbose:
            print(f"    → return {result}")
        return result


def demo_add_search_words():
    """示範 Design Add and Search Words。"""
    print("=" * 60)
    print("2-2. Design Add and Search Words (LeetCode 211)")
    print("=" * 60)

    wd = WordDictionary()

    # 範例 1
    print("\n--- 範例 1 ---")
    wd.add_word("bad", verbose=True)
    print(f"  結果: {wd.search('b.d', verbose=True)}")

    # 範例 2
    print("\n--- 範例 2 ---")
    wd2 = WordDictionary()
    wd2.add_word("dad", verbose=True)
    wd2.add_word("mad", verbose=True)
    print(f"  結果: {wd2.search('.ad', verbose=True)}")

    # 範例 3
    print("\n--- 範例 3 ---")
    wd3 = WordDictionary()
    wd3.add_word("bat", verbose=True)
    print(f"  結果: {wd3.search('b..', verbose=True)}")
    print()


# ---------------------------------------------------------------------------
# 2-3. Replace Words (LeetCode 648)
# ---------------------------------------------------------------------------
# 題意：給定一組 roots（詞根）和一個句子 sentence，
#       將句子中每個單字替換為「最短的詞根」。
#       如果某個單字沒有匹配的詞根，保持原樣。
#
# 策略：把所有 roots 建成 Trie，對句子每個單字在 Trie 中找最短 prefix。
#
# 範例 1: roots=["cat","bat","rat"], "the cattle was rattled by the battery"
#   Trie: root→{c→a→t*, b→a→t*, r→a→t*}
#   cattle→"cat", rattled→"rat", battery→"bat" → "the cat was rat by the bat"
#
# 範例 2: roots=["a","b","c"], "aadsfasf absbd bbab cadsfabd"
#   每個詞根一個字元 → "a a b c"
#
# 範例 3: roots=["catt","cat","bat"], "the cattle battled"
#   cattle→"cat"(最短,不是"catt"), battled→"bat" → "the cat bat"

def replace_words(dictionary: List[str], sentence: str,
                  verbose: bool = False) -> str:
    """LeetCode 648 - Replace Words. 用 Trie 找最短詞根。"""
    # 建 Trie
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    if verbose:
        print(f"  Roots: {dictionary}")
        print(f"  Sentence: \"{sentence}\"")

    def find_root(word: str) -> str:
        """在 Trie 中找 word 的最短詞根。"""
        node = root
        prefix = []
        for ch in word:
            if ch not in node.children:
                break
            node = node.children[ch]
            prefix.append(ch)
            if node.is_end:
                replacement = "".join(prefix)
                if verbose:
                    print(f"    \"{word}\" → {'→'.join(prefix)} "
                          f"(is_end!) → \"{replacement}\"")
                return replacement
        if verbose:
            print(f"    \"{word}\" → no root match → keep \"{word}\"")
        return word

    words = sentence.split()
    result_words = [find_root(w) for w in words]
    result = " ".join(result_words)
    if verbose:
        print(f"  結果: \"{result}\"")
    return result


def demo_replace_words():
    """示範 Replace Words。"""
    print("=" * 60)
    print("2-3. Replace Words (LeetCode 648)")
    print("=" * 60)

    print("\n--- 範例 1 ---")
    replace_words(["cat", "bat", "rat"],
                  "the cattle was rattled by the battery", verbose=True)

    print("\n--- 範例 2 ---")
    replace_words(["a", "b", "c"],
                  "aadsfasf absbd bbab cadsfabd", verbose=True)

    print("\n--- 範例 3 ---")
    replace_words(["catt", "cat", "bat"],
                  "the cattle battled", verbose=True)
    print()


# ============================================================================
# Section 3: Trie 進階 (Advanced Trie)
# ============================================================================


# ---------------------------------------------------------------------------
# 3-1. Longest Common Prefix using Trie
# ---------------------------------------------------------------------------
# 題意：找出一組字串的最長共同前綴 (Longest Common Prefix)。
# 策略：把所有字串插入 Trie，從 root 往下走，只要「只有一個 child 且不是結尾」
#       就繼續，否則停止。
#
# 範例 1: ["flower","flow","flight"] → f→l→分岔(o,i) → "fl"
# 範例 2: ["dog","dot","dove"] → d→o→分岔(g,t,v) → "do"
# 範例 3: ["abc","abc","abc"] → a→b→c*(end) → "abc"

def longest_common_prefix_trie(strs: List[str],
                               verbose: bool = False) -> str:
    """用 Trie 找最長共同前綴。"""
    if not strs:
        return ""

    # 建 Trie
    root = TrieNode()
    for word in strs:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    if verbose:
        print(f"  Strings: {strs}")

    # 從 root 往下走
    prefix = []
    node = root
    step = 0
    while len(node.children) == 1 and not node.is_end:
        ch = list(node.children.keys())[0]
        prefix.append(ch)
        node = node.children[ch]
        step += 1
        if verbose:
            reason = ""
            if node.is_end:
                reason = " (is_end=True, stop after this)"
            print(f"    Step {step}: only child '{ch}' → "
                  f"prefix = \"{''.join(prefix)}\"{reason}")

    if verbose:
        if not node.is_end and len(node.children) != 1:
            print(f"    Stop: {len(node.children)} children at this node")
        print(f"  結果: \"{''.join(prefix)}\"")
    return "".join(prefix)


def demo_longest_common_prefix():
    """示範 Longest Common Prefix using Trie。"""
    print("=" * 60)
    print("3-1. Longest Common Prefix using Trie")
    print("=" * 60)

    print("\n--- 範例 1 ---")
    longest_common_prefix_trie(["flower", "flow", "flight"], verbose=True)

    print("\n--- 範例 2 ---")
    longest_common_prefix_trie(["dog", "dot", "dove"], verbose=True)

    print("\n--- 範例 3 ---")
    longest_common_prefix_trie(["abc", "abc", "abc"], verbose=True)
    print()


# ---------------------------------------------------------------------------
# 3-2. Map Sum Pairs (LeetCode 677)
# ---------------------------------------------------------------------------
# 題意：設計 MapSum 資料結構：
#   - insert(key, val): 插入 key-value pair，若 key 已存在則覆蓋
#   - sum(prefix): 回傳所有以 prefix 開頭的 key 的 value 總和
#
# 每個節點存 prefix_sum（所有經過它的 value 總和）
# 範例 1: insert("apple",3), sum("ap")→3
# 範例 2: insert("apple",3)+insert("app",2), sum("ap")→5
# 範例 3: +insert("apricot",7), sum("ap")→12, sum("app")→5

class MapSumNode:
    """MapSum 的 Trie 節點，額外存 prefix_sum。"""
    def __init__(self):
        self.children: Dict[str, 'MapSumNode'] = {}
        self.prefix_sum: int = 0


class MapSum:
    """LeetCode 677 - Map Sum Pairs."""

    def __init__(self):
        self.root = MapSumNode()
        self.key_vals: Dict[str, int] = {}  # 記錄已存 key 的值（用於覆蓋）

    def insert(self, key: str, val: int, verbose: bool = False) -> None:
        """插入 key-val，並更新路徑上所有節點的 prefix_sum。"""
        # 如果 key 已存在，需要計算差值
        delta = val - self.key_vals.get(key, 0)
        self.key_vals[key] = val

        if verbose:
            print(f"  insert(\"{key}\", {val}): delta={delta}")

        node = self.root
        for i, ch in enumerate(key):
            if ch not in node.children:
                node.children[ch] = MapSumNode()
            node = node.children[ch]
            node.prefix_sum += delta
            if verbose:
                print(f"    Step {i+1}: '{ch}' prefix_sum → {node.prefix_sum}")

    def sum_prefix(self, prefix: str, verbose: bool = False) -> int:
        """回傳所有以 prefix 開頭的 key 的 value 總和。"""
        if verbose:
            print(f"  sum(\"{prefix}\"):")
        node = self.root
        for i, ch in enumerate(prefix):
            if ch not in node.children:
                if verbose:
                    print(f"    Step {i+1}: '{ch}' NOT found → return 0")
                return 0
            node = node.children[ch]
            if verbose:
                print(f"    Step {i+1}: '{ch}' (prefix_sum={node.prefix_sum})")
        if verbose:
            print(f"    結果: {node.prefix_sum}")
        return node.prefix_sum


def demo_map_sum():
    """示範 Map Sum Pairs。"""
    print("=" * 60)
    print("3-2. Map Sum Pairs (LeetCode 677)")
    print("=" * 60)

    # 範例 1
    print("\n--- 範例 1 ---")
    ms1 = MapSum()
    ms1.insert("apple", 3, verbose=True)
    ms1.sum_prefix("ap", verbose=True)

    # 範例 2
    print("\n--- 範例 2 ---")
    ms2 = MapSum()
    ms2.insert("apple", 3, verbose=True)
    ms2.insert("app", 2, verbose=True)
    ms2.sum_prefix("ap", verbose=True)

    # 範例 3
    print("\n--- 範例 3 ---")
    ms3 = MapSum()
    ms3.insert("apple", 3, verbose=True)
    ms3.insert("app", 2, verbose=True)
    ms3.insert("apricot", 7, verbose=True)
    ms3.sum_prefix("ap", verbose=True)
    ms3.sum_prefix("app", verbose=True)
    print()


# ---------------------------------------------------------------------------
# 3-3. Word Break (LeetCode 139) — Trie approach vs DP approach
# ---------------------------------------------------------------------------
# 題意：給定字串 s 和字典 wordDict，判斷 s 是否能被拆分成 wordDict 中的單字。
#
# Trie 思路：把 wordDict 建成 Trie，用 DP + Trie 同時掃描。
#   dp[i] = True 表示 s[0:i] 可以被拆分
#   對每個 dp[i]=True 的位置，從 Trie root 開始匹配 s[i:]
#
# 範例 1: "leetcode", ["leet","code"]
#   i=0: match "leet"→dp[4]=T; i=4: match "code"→dp[8]=T → True
# 範例 2: "catsandog", ["cats","dog","sand","and","cat"]
#   match "cat"→dp[3], "cats"→dp[4], "sand"→dp[7]... but dp[9]=False
# 純 DP 對比: dp[i] = any(dp[j] and s[j:i] in wordSet)
# Trie 版在字典大時更快，能提前剪枝（prefix 不存在就停）。

def word_break_trie(s: str, word_dict: List[str],
                    verbose: bool = False) -> bool:
    """LeetCode 139 - Word Break (Trie + DP approach)."""
    # 建 Trie
    root = TrieNode()
    for w in word_dict:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # 空字串

    if verbose:
        print(f"  s = \"{s}\", wordDict = {word_dict}")
        print(f"  dp 初始: dp[0]=True, 其餘 False")

    for i in range(n):
        if not dp[i]:
            continue
        if verbose:
            print(f"  i={i} (dp[{i}]=True): 從 Trie root 匹配 s[{i}:]=\"{s[i:]}\"")

        node = root
        for j in range(i, n):
            ch = s[j]
            if ch not in node.children:
                if verbose:
                    print(f"    j={j}: '{ch}' NOT in trie → stop")
                break
            node = node.children[ch]
            if node.is_end:
                dp[j + 1] = True
                if verbose:
                    print(f"    j={j}: '{ch}' found (is_end!) "
                          f"→ dp[{j+1}] = True  (matched \"{s[i:j+1]}\")")
            else:
                if verbose:
                    print(f"    j={j}: '{ch}' found (continue)")

    if verbose:
        print(f"  結果: dp[{n}] = {dp[n]}")
    return dp[n]


def word_break_dp(s: str, word_dict: List[str],
                  verbose: bool = False) -> bool:
    """LeetCode 139 - Word Break (純 DP approach 做對比)."""
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    if verbose:
        print(f"  s = \"{s}\", wordDict = {word_dict}")
        print(f"  [DP approach] dp[0]=True")

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                if verbose:
                    print(f"    dp[{i}]=True ← dp[{j}]=True "
                          f"and s[{j}:{i}]=\"{s[j:i]}\" in dict")
                break

    if verbose:
        print(f"  結果: dp[{n}] = {dp[n]}")
    return dp[n]


def demo_word_break():
    """示範 Word Break — Trie vs DP。"""
    print("=" * 60)
    print("3-3. Word Break (LeetCode 139) — Trie vs DP")
    print("=" * 60)

    # 範例 1
    print("\n--- 範例 1: s=\"leetcode\" ---")
    print("[Trie approach]:")
    word_break_trie("leetcode", ["leet", "code"], verbose=True)
    print("[DP approach]:")
    word_break_dp("leetcode", ["leet", "code"], verbose=True)

    # 範例 2
    print("\n--- 範例 2: s=\"catsandog\" ---")
    print("[Trie approach]:")
    word_break_trie("catsandog", ["cats", "dog", "sand", "and", "cat"],
                    verbose=True)
    print("[DP approach]:")
    word_break_dp("catsandog", ["cats", "dog", "sand", "and", "cat"],
                  verbose=True)
    print()


# ============================================================================
# Section 4: Trie vs HashMap vs Set 比較
# ============================================================================
# 精確搜尋: Trie O(L), HashMap O(L), Set O(L) — 都差不多
# 前綴搜尋: Trie O(P) ✓ 最大優勢!  HashMap/Set O(N*L) 需遍歷
# 自動補全: Trie O(P+K) ✓           HashMap/Set O(N*L)
# 空間:     Trie O(N*L*26) 最差但前綴共享   HashMap/Set O(N*L)
# Wildcard: Trie O(26^L) DFS 可行   HashMap/Set 不支援
#
# 用 Trie: prefix search, autocomplete, spell check, wildcard
# 用 HashMap/Set: exact match, 非字串 key, 記憶體有限

def demo_trie_vs_hashmap():
    """實際比較 Trie vs HashMap 做前綴搜尋的差異。"""
    print("=" * 60)
    print("Section 4: Trie vs HashMap vs Set 比較")
    print("=" * 60)

    words = ["apple", "app", "application", "apt", "banana", "band", "ban"]

    # --- HashMap approach: 前綴搜尋 ---
    print("\n--- HashMap approach: 找所有以 'app' 開頭的單字 ---")
    prefix = "app"
    hash_result = [w for w in words if w.startswith(prefix)]
    print(f"  遍歷所有 {len(words)} 個單字，逐一檢查 startswith(\"{prefix}\")")
    for w in words:
        match = w.startswith(prefix)
        print(f"    \"{w}\".startswith(\"{prefix}\") = {match}")
    print(f"  結果: {hash_result}")
    print(f"  Time: O(N * L)，N={len(words)} 個單字都要檢查")

    # --- Trie approach: 前綴搜尋 ---
    print(f"\n--- Trie approach: 找所有以 '{prefix}' 開頭的單字 ---")
    trie = Trie()
    for w in words:
        trie.insert(w)

    # 走到 prefix 節點
    node = trie.root
    print(f"  Step 1: 沿著 Trie 走到 prefix \"{prefix}\" 的節點")
    for ch in prefix:
        node = node.children[ch]
        print(f"    → '{ch}'")
    print(f"  Step 2: 從該節點 DFS 收集所有完整單字")

    # DFS 收集
    trie_result = []

    def collect(n: TrieNode, path: str):
        if n.is_end:
            trie_result.append(path)
        for ch_key in sorted(n.children):
            collect(n.children[ch_key], path + ch_key)

    collect(node, prefix)
    print(f"  結果: {trie_result}")
    print(f"  Time: O(P + K)，P={len(prefix)} 走到節點，K={len(trie_result)} 收集結果")
    print(f"  不需要檢查 'banana', 'band', 'ban' 等無關單字！")

    # --- 總結 ---
    print(f"\n--- 總結 ---")
    print(f"  HashMap: 簡單直覺，精確匹配 O(1)，前綴搜尋 O(N*L)")
    print(f"  Trie:    前綴搜尋 O(P+K)，適合 autocomplete / prefix 相關題目")
    print(f"  Set:     跟 HashMap 類似，適合 membership test")
    print(f"\n  面試口訣: prefix/autocomplete/wildcard → Trie")
    print(f"            exact match / contains → HashMap / Set")
    print()


# ============================================================================
# main — 執行所有示範
# ============================================================================

def main():
    print()
    print("*" * 60)
    print("*  LeetCode Trie (Prefix Tree) 模式完全攻略")
    print("*  適用面試：Google / NVIDIA / Meta / Amazon")
    print("*" * 60)
    print()

    # Section 1
    demo_trie_basic()

    # Section 2
    demo_word_search_ii()
    demo_add_search_words()
    demo_replace_words()

    # Section 3
    demo_longest_common_prefix()
    demo_map_sum()
    demo_word_break()

    # Section 4
    demo_trie_vs_hashmap()

    print("=" * 60)
    print("全部示範完成！面試口訣：")
    print("  prefix / autocomplete / wildcard → Trie")
    print("  exact match / contains → HashMap / Set")
    print("=" * 60)


if __name__ == "__main__":
    main()
