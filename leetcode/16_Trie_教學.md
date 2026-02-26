# LeetCode 教學 #16：Trie (Prefix Tree) 完全攻略

> **適用對象**：LeetCode 初學者，準備 Google 面試
> **前置知識**：Python 基礎（dict 語法）、Big-O 概念、Tree 基本觀念
> **配套程式**：`16_Trie.py`（可直接執行看 step-by-step trace）

---

## 第一章：Trie 是什麼？ -- 從零開始

### 1.1 問題：如何高效搜尋前綴？

假設你有一個字典，裡面存了 100 萬個英文單字。現在使用者打了 `"app"`，你要找出所有以 `"app"` 開頭的單字（像 Google 搜尋的自動補全）。

**方法一：HashMap / List 暴力搜尋**

```
words = ["apple", "app", "apt", "bat", "bad", ...]  # 100 萬個

# 逐一檢查每個單字是否以 "app" 開頭
for word in words:
    if word.startswith("app"):   # 每次比較 O(m)，m = prefix 長度
        results.append(word)

# 總時間：O(n * m)，n = 單字總數，m = prefix 長度
# 100 萬個單字 × 3 字元 = 300 萬次比較... 太慢了！
```

**方法二：Trie（前綴樹）**

把所有單字的共同前綴「合併」成一棵樹。搜尋時只要沿著前綴路徑走下去，不需要掃描所有單字。

```
搜尋 "app" 的路徑：root → a → p → p    只走了 3 步！
然後從這個節點往下收集所有完整單字      O(m + k)，k = 結果數
```

| 操作 | HashMap / List | Trie |
|------|---------------|------|
| 插入一個單字 | O(1) / O(m) | O(m) |
| 精確搜尋 | O(1) / O(n) | O(m) |
| **前綴搜尋** | **O(n * m)** | **O(m + k)** |
| 自動補全 | O(n * m) | O(m + k) |

其中 m = 單字長度，n = 單字總數，k = 匹配的結果數。

---

### 1.2 Trie 長什麼樣子？

我們把 `["apple", "app", "apt", "bat", "bad"]` 這五個單字存進 Trie：

```
                    root
                   /    \
                  a      b
                  |      |
                  p      a
                 / \    / \
                p   t* d*  t*
                |
                l
                |
                e*

    (* 表示 is_end = True，代表這裡是一個完整單字的結尾)
```

**觀察重點**：

1. **共享前綴 (shared prefix)**：`"apple"`, `"app"`, `"apt"` 共享前綴 `"ap"`，在 Trie 中只存一次
2. **分岔點 (branching point)**：`"app"` 和 `"apt"` 在第三個字元分岔（`p` vs `t`）
3. **結尾標記 (is_end)**：`"app"` 的第二個 `p` 和 `"apt"` 的 `t` 都標記為 `is_end = True`
4. **每條邊代表一個字元**：從 root 到任何 `is_end` 節點的路徑 = 一個完整單字

---

### 1.3 TrieNode 的結構

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # dict: char -> TrieNode
        self.is_end = False     # 是否為完整單字的結尾
```

就這麼簡單！一個節點只有兩樣東西：

| 欄位 | 型態 | 說明 |
|------|------|------|
| `children` | `Dict[str, TrieNode]` | 存放子節點。key = 字元，value = 下一個 TrieNode |
| `is_end` | `bool` | 標記到這個節點為止是否形成一個完整單字 |

**為什麼用 dict 而不是固定大小的 array？**

- Array 版本：`self.children = [None] * 26`，用 `ord(ch) - ord('a')` 索引。固定 O(1) 存取，但每個節點固定占 26 格空間。
- Dict 版本：`self.children = {}`，只存有用的 child。更省空間，程式碼更直覺。

面試時兩種都可以，dict 版本更好寫、更不容易出錯。

---

### 1.4 為什麼叫 Trie？

Trie 這個名字來自 re**TRIE**val（檢索）。由 Edward Fredkin 在 1960 年命名。

- 發音有爭議：有人念 "tree"（和 Tree 同音），有人念 "try"（為了區別）
- 面試時說 "prefix tree" 最安全，面試官一定聽得懂
- 中文常見翻譯：**字典樹**、**前綴樹**

---

## 第二章：Trie 基礎操作 -- Implement Trie (LC 208)

### 2.1 Insert（插入）

**核心邏輯**：從 root 開始，逐字元往下走。如果 child 不存在就建立新節點，已存在就重複利用。走完所有字元後，標記 `is_end = True`。

#### Example 1：Insert "apple"（全部建立新節點）

```
初始狀態：只有 root（空的 Trie）

Step 1: ch='a'  → root 沒有 child 'a' → 建立新節點
        root ─a─> (a)

Step 2: ch='p'  → (a) 沒有 child 'p' → 建立新節點
        root ─a─> (a) ─p─> (p)

Step 3: ch='p'  → (p) 沒有 child 'p' → 建立新節點
        root ─a─> (a) ─p─> (p) ─p─> (p)

Step 4: ch='l'  → (p) 沒有 child 'l' → 建立新節點
        root ─a─> (a) ─p─> (p) ─p─> (p) ─l─> (l)

Step 5: ch='e'  → (l) 沒有 child 'e' → 建立新節點
        root ─a─> (a) ─p─> (p) ─p─> (p) ─l─> (l) ─e─> (e)

最後：標記 (e) 的 is_end = True

完成後的 Trie：
        root
         |
         a
         |
         p
         |
         p
         |
         l
         |
         e*        (* = is_end)
```

#### Example 2：Insert "app"（重複利用已有節點）

```
目前的 Trie（已經有 "apple"）：
        root ─a─> (a) ─p─> (p) ─p─> (p) ─l─> (l) ─e─> (e*)

Step 1: ch='a'  → root 已有 child 'a' → 重複利用！不建新節點
Step 2: ch='p'  → (a) 已有 child 'p'  → 重複利用！
Step 3: ch='p'  → (p) 已有 child 'p'  → 重複利用！

最後：標記第二個 (p) 的 is_end = True

完成後的 Trie：
        root
         |
         a
         |
         p
         |
         p*  ← is_end=True（"app" 在這裡結束）
         |
         l
         |
         e*  ← is_end=True（"apple" 在這裡結束）

關鍵：insert "app" 沒有建立任何新節點！只是在已有路徑上標記了 is_end。
```

---

### 2.2 Search（搜尋完整單字）

**核心邏輯**：從 root 開始逐字元往下走。如果某個字元的 child 不存在，回傳 False。走完所有字元後，檢查 `is_end` 是否為 True。

目前的 Trie 存有 `"apple"` 和 `"app"`：

```
        root
         |
         a
         |
         p
         |
         p*         ← is_end=True
         |
         l
         |
         e*         ← is_end=True
```

#### Example 1：search("apple") --> True

```
Step 1: ch='a'  → root 有 child 'a'  → 往下走
Step 2: ch='p'  → (a) 有 child 'p'   → 往下走
Step 3: ch='p'  → (p) 有 child 'p'   → 往下走
Step 4: ch='l'  → (p*) 有 child 'l'  → 往下走
Step 5: ch='e'  → (l) 有 child 'e'   → 到達 (e*)

檢查：is_end = True → return True ✓
路徑完整存在，且結尾是完整單字。
```

#### Example 2：search("app") --> True

```
Step 1: ch='a'  → root 有 child 'a'  → 往下走
Step 2: ch='p'  → (a) 有 child 'p'   → 往下走
Step 3: ch='p'  → (p) 有 child 'p'   → 到達 (p*)

檢查：is_end = True → return True ✓
雖然下面還有 "le" 兩個節點，但 "app" 本身就是一個完整單字。
```

#### Example 3：search("ap") --> False

```
Step 1: ch='a'  → root 有 child 'a'  → 往下走
Step 2: ch='p'  → (a) 有 child 'p'   → 到達第一個 (p)

檢查：is_end = False → return False ✗
路徑存在，但 "ap" 不是一個完整單字（沒有被 insert 過）。
```

#### Example 4：search("orange") --> False

```
Step 1: ch='o'  → root 沒有 child 'o' → return False ✗
在第一步就失敗了！root 底下只有 'a'，根本沒有 'o'。
```

---

### 2.3 StartsWith（前綴搜尋）

**核心邏輯**：和 Search 幾乎一樣，唯一的差別是**不需要檢查 is_end**。只要路徑存在就回傳 True。

#### Example 1：startsWith("ap") --> True

```
Step 1: ch='a'  → root 有 child 'a'  → 往下走
Step 2: ch='p'  → (a) 有 child 'p'   → 到達

路徑完整存在 → return True ✓

對比 search("ap") → False！
差異：startsWith 不檢查 is_end，只要路徑存在就好。
```

#### Example 2：startsWith("bat") --> False

```
Step 1: ch='b'  → root 沒有 child 'b' → return False ✗
目前 Trie 裡只有 a 開頭的字，沒有 b 開頭的。
```

---

### 2.4 完整程式碼（附逐行解說）

```python
class TrieNode:
    def __init__(self):
        self.children = {}       # char -> TrieNode
        self.is_end = False      # 到這裡是否為完整單字

class Trie:
    def __init__(self):
        self.root = TrieNode()   # Trie 永遠有一個空的 root

    # ─── INSERT ───
    def insert(self, word: str) -> None:
        node = self.root                     # 從 root 出發
        for ch in word:                      # 逐字元走
            if ch not in node.children:      #   這個字元的路不存在？
                node.children[ch] = TrieNode()  #   建新路
            node = node.children[ch]         #   往下走
        node.is_end = True                   # 標記：這裡是一個完整單字

    # ─── SEARCH ───
    def search(self, word: str) -> bool:
        node = self.root                     # 從 root 出發
        for ch in word:                      # 逐字元走
            if ch not in node.children:      #   路斷了？
                return False                 #   單字不存在
            node = node.children[ch]         #   往下走
        return node.is_end                   # 走完了，檢查是不是完整單字

    # ─── STARTS WITH ───
    def startsWith(self, prefix: str) -> bool:
        node = self.root                     # 從 root 出發
        for ch in prefix:                    # 逐字元走
            if ch not in node.children:      #   路斷了？
                return False                 #   前綴不存在
            node = node.children[ch]         #   往下走
        return True                          # 走完了，路徑存在就好（不管 is_end）
```

**注意 search 和 startsWith 的唯一差異**：

```
search:      return node.is_end    # 必須是完整單字
startsWith:  return True           # 路徑存在就好
```

### 2.5 複雜度分析

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| insert(word) | O(m) | O(m)，最差情況新建 m 個節點 |
| search(word) | O(m) | O(1)，不建新節點 |
| startsWith(prefix) | O(m) | O(1)，不建新節點 |

其中 m = 輸入字串的長度。

**整棵 Trie 的空間複雜度**：O(N * M)，N = 單字數，M = 平均長度。但因為共享前綴，實際空間遠小於此。

---

## 第三章：Trie 應用題

### 3.1 Word Search II (LC 212) -- Google Hard

**題意**：給定一個 m x n 的字母矩陣 `board` 和一組單字 `words`，找出所有能在 board 上用相鄰格子（上下左右）拼出的單字。每個格子在同一個單字中只能用一次。

**策略**：Trie + DFS Backtracking

1. 把所有 `words` 建成 Trie
2. 對 board 每個格子啟動 DFS
3. DFS 過程中，同步在 Trie 中走。如果當前路徑不是任何 word 的 prefix，**立即剪枝**

為什麼不能單純用 DFS？因為如果有 1000 個 word，每個 word 都要跑一遍 DFS，太慢了。
Trie 讓我們**一次 DFS 就能同時搜尋所有 word**！

#### Example 1：找到 "oan" 和 "an"

```
Board:                    Words: ["oan", "an"]
  +---+---+---+
  | o | a | n |           Step 1: 建 Trie
  +---+---+---+                    root
  | e | t | h |                   /    \
  +---+---+---+                  o      a
                                 |      |
                                 a      n*
                                 |
                                 n*
```

**DFS 追蹤**：

```
從 (0,0)='o' 開始：
  root 有 child 'o' → 進入
    (0,0)='o' → Trie 走到 (o)
    往右 (0,1)='a' → Trie: (o) 有 child 'a' → 進入
      (0,1)='a' → Trie 走到 (o→a)
      往右 (0,2)='n' → Trie: (o→a) 有 child 'n' → 進入
        (0,2)='n' → Trie 走到 (o→a→n*)
        is_end = True → 找到 "oan" !!
        繼續探索鄰居，但 Trie 在 n* 下面沒有 child → 全部剪枝
      回溯
    回溯
  回溯

從 (0,1)='a' 開始：
  root 有 child 'a' → 進入
    (0,1)='a' → Trie 走到 (a)
    往右 (0,2)='n' → Trie: (a) 有 child 'n' → 進入
      (0,2)='n' → Trie 走到 (a→n*)
      is_end = True → 找到 "an" !!
    回溯
  回溯

結果：["oan", "an"]
```

#### Example 2：部分匹配

```
Board:                    Words: ["ab", "ba", "abc"]
  +---+---+
  | a | b |               Trie:
  +---+---+                      root
  | c | d |                     /    \
  +---+---+                    a      b
                               |      |
                               b*     a*
                               |
                               c*
```

**DFS 追蹤**：

```
從 (0,0)='a' 開始：
  Trie: root → a
    往右 (0,1)='b' → Trie: a → b*
      is_end = True → 找到 "ab"!
      往下 (1,1)='d' → Trie: b* 沒有 child 'd' → 剪枝
      往下 (1,0)='c' → Trie: b* 有 child 'c' → 進入
        (1,0)='c' → Trie 走到 b*→c*
        is_end = True → 找到 "abc"!
        （注意：a(0,0) → b(0,1) → c(1,0) 是合法路徑，b 和 c 相鄰）
    往下 (1,0)='c' → Trie: a 沒有 child 'c' → 剪枝

從 (0,1)='b' 開始：
  Trie: root → b
    往左 (0,0)='a' → Trie: b → a*
      is_end = True → 找到 "ba"!

結果：["ab", "abc", "ba"]
```

#### 完整程式碼

```python
def findWords(board, words):
    # Step 1: 建 Trie
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.word = w          # 存完整單字，方便找到時直接取用

    rows, cols = len(board), len(board[0])
    result = []

    # Step 2: 對每個格子啟動 DFS
    def dfs(r, c, node):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        ch = board[r][c]
        if ch == '#' or ch not in node.children:   # 已訪問 或 Trie 中沒路
            return

        next_node = node.children[ch]

        if next_node.is_end:                 # 找到一個完整單字！
            result.append(next_node.word)
            next_node.is_end = False         # 防止重複加入

        board[r][c] = '#'                    # 標記已訪問
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc, next_node)
        board[r][c] = ch                     # 回溯

        # 剪枝優化：如果子節點已空，刪掉省未來搜尋
        if not next_node.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root.children:
                dfs(r, c, root)

    return result
```

**關鍵優化**：
- `next_node.is_end = False`：找到後取消標記，避免同一個字被加入多次
- `del node.children[ch]`：子樹已空時刪除節點，減少未來搜尋的分支

**複雜度**：
- 時間：O(M * N * 4^L)，M*N 個起點，每個最多探索 4^L 條路徑（L = 最長單字長度）
- 空間：O(W * L)，Trie 的空間，W = 單字數

---

### 3.2 Design Add and Search Words (LC 211)

**題意**：設計一個資料結構 `WordDictionary`，支援：
- `addWord(word)`：新增單字
- `search(word)`：搜尋單字。`'.'` 可以匹配**任意一個字母**

**關鍵**：遇到 `'.'` 時，必須對當前節點的**所有 children** 進行 DFS。這就是為什麼 Trie 比 HashMap 更適合這題 -- HashMap 碰到 wildcard 只能暴力掃描。

#### Example 1：search("b.d") matches "bad"

```
Trie（存了 "bad", "dad", "mad"）：

        root
       / | \
      b  d  m
      |  |  |
      a  a  a
      |  |  |
      d* d* d*

search("b.d") 的過程：

  Step 1: ch='b' → root 有 child 'b' → 走到 (b)
  Step 2: ch='.' → wildcard! 必須嘗試 (b) 的所有 children
    (b) 的 children = {'a': ...}
    嘗試 'a'：走到 (b→a)
      Step 3: ch='d' → (a) 有 child 'd' → 走到 (b→a→d*)
      is_end = True → return True ✓

路徑：b → . matches 'a' → d → 找到 "bad"！
```

#### Example 2：search("...") matches any 3-letter word

```
search("...") 的過程：

  Step 1: ch='.' → root 的所有 children = {'b', 'd', 'm'}
    嘗試 'b'：走到 (b)
      Step 2: ch='.' → (b) 的所有 children = {'a'}
        嘗試 'a'：走到 (b→a)
          Step 3: ch='.' → (a) 的所有 children = {'d'}
            嘗試 'd'：走到 (b→a→d*)
            is_end = True → return True ✓

第一條路徑就成功了！實際上 "bad", "dad", "mad" 都匹配 "..."。
```

#### 完整程式碼

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True          # 和普通 Trie insert 完全一樣

    def search(self, word: str) -> bool:
        def dfs(idx, node):
            if idx == len(word):             # 走完所有字元
                return node.is_end           # 檢查是否為完整單字

            ch = word[idx]

            if ch == '.':                    # wildcard：嘗試所有 children
                for child in node.children.values():
                    if dfs(idx + 1, child):  # 只要有一條路成功就好
                        return True
                return False                 # 所有路都失敗
            else:                            # 普通字元
                if ch not in node.children:
                    return False
                return dfs(idx + 1, node.children[ch])

        return dfs(0, self.root)
```

**複雜度**：
- `addWord`：O(m)，m = 單字長度
- `search` 無 wildcard：O(m)
- `search` 有 wildcard：最差 O(26^m)，但實際上 Trie 分支有限，遠小於此

---

### 3.3 Replace Words (LC 648)

**題意**：給定一組詞根 (roots) 和一個句子。把句子中每個單字替換成**最短的匹配詞根**。如果沒有匹配的詞根，保持原樣。

**策略**：把所有 roots 建成 Trie。對句子中每個單字，在 Trie 中走，碰到第一個 `is_end = True` 就停（最短前綴）。

#### Example 1：基本替換

```
roots = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"

Trie:
        root
       / | \
      c  b  r
      |  |  |
      a  a  a
      |  |  |
      t* t* t*

逐一處理句子中的單字：
  "the"     → 走 t → root 沒有 child 't'?
              等等，root 有 c, b, r... 沒有 t → 保持原樣 "the"
  "cattle"  → 走 c→a→t* → is_end! 最短詞根 = "cat" → 替換
  "was"     → root 沒有 child 'w' → 保持原樣 "was"
  "rattled" → 走 r→a→t* → is_end! 最短詞根 = "rat" → 替換
  "by"      → root 沒有 child 'b'? 有! → 走 b→... 等等
              走 b→... 但 "by" 的第二個字元是 'y'
              (b) 的 child 只有 'a'，沒有 'y' → 保持原樣 "by"
  "the"     → 保持原樣 "the"
  "battery" → 走 b→a→t* → is_end! 最短詞根 = "bat" → 替換

結果："the cat was rat by the bat"
```

#### Example 2：多個長度的詞根，取最短

```
roots = ["catt", "cat", "bat"]
sentence = "the cattle battled"

Trie:
        root
       / \
      c   b
      |   |
      a   a
      |   |
      t*  t*
      |
      t*

逐一處理：
  "the"     → root 沒有 child 't' (只有 c, b) → 保持 "the"
  "cattle"  → 走 c→a→t* → is_end! 停！最短詞根 = "cat"
              （不會繼續走到 "catt"，因為 "cat" 更短且已經 is_end）
  "battled" → 走 b→a→t* → is_end! 最短詞根 = "bat"

結果："the cat bat"
```

#### 完整程式碼

```python
def replaceWords(dictionary, sentence):
    # 建 Trie
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def find_root(word):
        """找 word 的最短詞根。"""
        node = root
        prefix = []
        for ch in word:
            if ch not in node.children:   # 路斷了，沒有匹配的詞根
                break
            node = node.children[ch]
            prefix.append(ch)
            if node.is_end:               # 找到最短詞根！
                return "".join(prefix)
        return word                       # 沒找到詞根，保持原樣

    return " ".join(find_root(w) for w in sentence.split())
```

**複雜度**：
- 建 Trie：O(D)，D = 所有詞根的總字元數
- 替換句子：O(S)，S = 句子總字元數
- 總時間：O(D + S)

---

## 第四章：Trie 進階應用

### 4.1 Autocomplete System（自動補全系統）

Google 搜尋框的自動補全功能，背後就是 Trie 的概念！

**核心思路**：Trie + 每個節點儲存該前綴的「熱門搜尋」（按頻率排序）。

```
用戶輸入 "app"，系統要回傳最熱門的建議：

Trie 結構（每個節點附帶 top-3 熱門結果）：

        root
         |
         a     [apple(100), amazon(90), app(50)]
         |
         p     [apple(100), app(50), application(30)]
         |
         p     [apple(100), app(50), application(30)]
        / \
       l   *   (* = "app" is_end, freq=50)
       |
       e
       |
       *       (* = "apple" is_end, freq=100)

用戶輸入 "app" → 走到第二個 p → 回傳 ["apple", "app", "application"]
```

#### Example 1：基本自動補全

```
存入的搜尋歷史（word: frequency）：
  "apple": 100
  "app": 50
  "application": 30
  "banana": 80

用戶輸入 "app" → 自動補全結果：
  1. apple (100)       ← 頻率最高
  2. app (50)
  3. application (30)
```

#### Example 2：邊輸入邊更新

```
用戶輸入 "a" → 結果：["apple(100)", "app(50)", "application(30)"]
用戶輸入 "ap" → 結果：["apple(100)", "app(50)", "application(30)"]
用戶輸入 "app" → 結果：["apple(100)", "app(50)", "application(30)"]
用戶輸入 "appl" → 結果：["apple(100)", "application(30)"]
用戶選擇 "apple" → 更新頻率 "apple": 101
```

#### 核心程式邏輯

```python
def search_prefix(self, prefix):
    # Step 1: 走到 prefix 對應的節點
    node = self.root
    for ch in prefix:
        if ch not in node.children:
            return []
        node = node.children[ch]

    # Step 2: DFS 收集子樹中所有完整單字
    results = []
    def dfs(n, path):
        if n.is_end:
            results.append((path, n.freq))
        for ch, child in n.children.items():
            dfs(child, path + ch)
    dfs(node, prefix)

    # Step 3: 按頻率排序，回傳 top-3
    results.sort(key=lambda x: -x[1])
    return [word for word, freq in results[:3]]
```

---

### 4.2 Longest Common Prefix with Trie

**題意**：找出一組字串的最長共同前綴 (Longest Common Prefix)。

**策略**：把所有字串插入 Trie，從 root 往下走。只要**只有一個 child 且不是結尾**就繼續，否則停止。

- 遇到**分岔**（多個 children）→ 停，因為字串在這裡開始不同
- 遇到 **is_end = True** → 停，因為某個字串在這裡結束了，更長的前綴不是所有字串共有的

#### Example 1：["flower", "flow", "flight"]

```
Trie:
        root
         |
         f
         |
         l
        / \
       o   i          ← 分岔！
       |   |
       w*  g
       |   |
       e   h
       |   |
       r*  t*

從 root 往下走：
  Step 1: root 只有一個 child 'f'，is_end=False → 繼續 → prefix = "f"
  Step 2: (f) 只有一個 child 'l'，is_end=False → 繼續 → prefix = "fl"
  Step 3: (l) 有兩個 children {'o', 'i'} → 停！

結果："fl"
```

#### Example 2：["dog", "dot", "dove"]

```
Trie:
        root
         |
         d
         |
         o
        / | \
       g* t* v         ← 三個 children，分岔！
             |
             e*

從 root 往下走：
  Step 1: root 只有一個 child 'd'，is_end=False → 繼續 → prefix = "d"
  Step 2: (d) 只有一個 child 'o'，is_end=False → 繼續 → prefix = "do"
  Step 3: (o) 有三個 children {'g', 't', 'v'} → 停！

結果："do"
```

#### Example 3：["abc", "abc", "abc"]（全部相同）

```
Trie（三個相同字串插入，路徑完全重疊）：
        root
         |
         a
         |
         b
         |
         c*

從 root 往下走：
  Step 1: root 只有一個 child 'a'，is_end=False → 繼續 → prefix = "a"
  Step 2: (a) 只有一個 child 'b'，is_end=False → 繼續 → prefix = "ab"
  Step 3: (b) 只有一個 child 'c'，但 is_end=True → 繼續並加入 → prefix = "abc"
  Step 4: (c*) is_end=True → 停！

結果："abc"
```

#### 程式碼

```python
def longestCommonPrefix(strs):
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

    # 從 root 往下走，直到分岔或結尾
    prefix = []
    node = root
    while len(node.children) == 1 and not node.is_end:
        ch = list(node.children.keys())[0]
        prefix.append(ch)
        node = node.children[ch]

    return "".join(prefix)
```

> **注意**：這題用 Trie 是 O(S) 其中 S = 所有字串的總字元數。其實直接逐位比較也是 O(S)，效率一樣。但 Trie 的好處是：如果你之後要動態加入新字串，Trie 結構已經建好，不用重新比較。

---

## 第五章：Trie vs HashMap vs Set 比較

### 5.1 三種資料結構的特性比較

```
+------------------+-----------+-----------+-----------+
|       操作       |   Trie    |  HashMap  |    Set    |
+------------------+-----------+-----------+-----------+
| 插入             | O(m)      | O(m)*     | O(m)*     |
| 精確搜尋         | O(m)      | O(1)**    | O(1)**    |
| 前綴搜尋         | O(m+k)   | O(n*m)    | O(n*m)    |
| 自動補全 (top-k) | O(m+k)   | O(n*m)    | --        |
| Wildcard 搜尋    | O(26^m)  | O(n*m)    | --        |
| 刪除             | O(m)      | O(1)**    | O(1)**    |
| 空間             | O(N*M*C) | O(N*M)    | O(N*M)    |
+------------------+-----------+-----------+-----------+

m = 輸入字串長度
n = 儲存的字串總數
k = 搜尋結果數量
N = 字串總數, M = 平均長度, C = 字元集大小（英文=26）

*  HashMap/Set 的 insert 和 lookup 是「平均 O(1)」，
   但 hash 計算本身需要 O(m)（m = key 長度），嚴格來說是 O(m)
** 同上，精確搜尋的 O(1) 是假設 hash 是 O(1)
```

### 5.2 什麼時候用 Trie？

```
面試決策流程：

  題目涉及字串操作？
    |
    ├─ 需要「前綴」相關操作？ → Trie
    |   - 前綴搜尋 (startsWith)
    |   - 自動補全 (autocomplete)
    |   - 找最短/最長前綴
    |   - 所有前綴匹配
    |
    ├─ 需要 wildcard / 模糊匹配？ → Trie
    |   - '.' 匹配任意字元
    |   - regex-like 搜尋
    |
    ├─ 需要精確匹配 / 計數？ → HashMap
    |   - word frequency counting
    |   - 兩數之和 (Two Sum)
    |   - 去重
    |
    └─ 只需要判斷存在與否？ → Set
        - membership test
        - 去重
```

### 5.3 Trie 的優缺點

```
優點：
  ✓ 前綴搜尋效率極高 — O(prefix_len) 不受字典大小影響
  ✓ 字串集合有大量共同前綴時，空間效率高
  ✓ 可以按字典序遍歷所有字串（DFS 自然產生排序結果）
  ✓ 支援 wildcard 搜尋
  ✓ 增量式匹配（一邊輸入一邊搜尋）

缺點：
  ✗ 空間開銷比 HashMap 大（每個節點都有 children dict）
  ✗ 實作比 HashMap 複雜
  ✗ Cache locality 差（節點分散在記憶體中）
  ✗ 如果字串集合沒有共同前綴，退化成很多獨立的鏈
```

### 5.4 面試常見 Trie 題型速查表

```
+------+-----------------------------+--------+-------------------+
| 題號 | 題目                         | 難度   | 核心技巧           |
+------+-----------------------------+--------+-------------------+
| 208  | Implement Trie              | Medium | Trie 基本實作      |
| 211  | Add and Search Words        | Medium | Trie + DFS ('.')   |
| 212  | Word Search II              | Hard   | Trie + Backtrack   |
| 648  | Replace Words               | Medium | Trie 找最短前綴    |
| 677  | Map Sum Pairs               | Medium | Trie + prefix sum  |
| 139  | Word Break                  | Medium | Trie + DP          |
| 720  | Longest Word in Dictionary  | Medium | Trie + DFS/BFS     |
| 1268 | Search Suggestions System   | Medium | Trie + 排序        |
+------+-----------------------------+--------+-------------------+

Google 面試最愛考：208（基本功）、212（Hard 綜合題）、211（wildcard）
```

---

## 總結：Trie 心法

```
1. Trie 的本質 = 用「樹」的結構來存「字串的共同前綴」
   - 每個節點 = 一個字元
   - 每條路徑 = 一個字串（或字串的前綴）
   - is_end 區分「完整單字」和「只是前綴」

2. 三個基本操作的共同模式：
   node = root
   for ch in word:
       if ch not in node.children:
           # insert: 建立新節點
           # search/startsWith: return False
       node = node.children[ch]
   # insert: node.is_end = True
   # search: return node.is_end
   # startsWith: return True

3. 進階應用的核心組合：
   - Trie + DFS/Backtracking → Word Search II (212)
   - Trie + DFS (wildcard)   → Add and Search Words (211)
   - Trie + Greedy           → Replace Words (648)
   - Trie + DP               → Word Break (139)
   - Trie + Frequency        → Autocomplete System

4. 面試口訣：
   看到 "prefix" / "autocomplete" / "wildcard" → 想 Trie
   看到 "exact match" / "counting" → 想 HashMap
```
