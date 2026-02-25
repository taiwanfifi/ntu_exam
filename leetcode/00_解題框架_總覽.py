#!/usr/bin/env python3
"""
=============================================================================
  LeetCode 解題框架總覽 — Master Decision Tree
  適用對象：準備 Google / NVIDIA 面試的初學者
  執行方式：python 00_解題框架_總覽.py
=============================================================================

本檔案包含：
  1. 算法分類表（AlgorithmCatalog）
  2. 時間/空間複雜度速查表
  3. 「看到什麼關鍵字 → 用什麼算法」完整對照
  4. 20+ 種常見 Pattern 辨識範例
  5. Decision Tree 函數
  6. 可執行的 main()，印出完整框架
"""


# =============================================================================
# Section 1: 算法分類表 (Algorithm Catalog)
# =============================================================================

ALGORITHM_CATALOG = {
    "Array / String": {
        "Two Pointers": {
            "description": "用兩個指標從不同位置出發，向彼此靠近或同方向移動",
            "subtypes": ["反向雙指標 (opposite)", "同向雙指標 (same direction)", "快慢指標 (fast-slow)"],
            "time": "O(n)",
            "space": "O(1)",
            "use_when": "sorted array, 找 pair, 原地修改, 判斷 palindrome",
            "classic": ["Two Sum II", "3Sum", "Container With Most Water", "Trapping Rain Water"],
        },
        "Sliding Window": {
            "description": "維護一個連續的子陣列/子字串視窗，動態調整左右邊界",
            "subtypes": ["固定長度視窗", "可變長度視窗"],
            "time": "O(n)",
            "space": "O(k) 或 O(字元集大小)",
            "use_when": "連續子陣列/子字串, 最長/最短滿足條件的區間",
            "classic": ["Max Average Subarray", "Longest Substring Without Repeating", "Minimum Window Substring"],
        },
        "Prefix Sum": {
            "description": "預計算前綴和，用 prefix[j] - prefix[i] 快速求區間和",
            "subtypes": ["一維前綴和", "二維前綴和"],
            "time": "O(n) 預處理, O(1) 查詢",
            "space": "O(n)",
            "use_when": "多次查詢子陣列的和, subarray sum equals k",
            "classic": ["Subarray Sum Equals K", "Range Sum Query", "Product of Array Except Self"],
        },
    },
    "Hash": {
        "HashMap": {
            "description": "用 key-value 對存儲資料，O(1) 查找",
            "subtypes": ["counting", "grouping", "lookup", "two-pass/one-pass"],
            "time": "O(n)",
            "space": "O(n)",
            "use_when": "需要快速查找, counting 出現次數, grouping by some key",
            "classic": ["Two Sum", "Group Anagrams", "Longest Consecutive Sequence"],
        },
        "HashSet": {
            "description": "只存 key（不需 value），O(1) 判斷是否存在",
            "subtypes": ["去重", "存在性檢查", "集合操作"],
            "time": "O(n)",
            "space": "O(n)",
            "use_when": "判斷是否出現過, 去除重複, 集合交集/差集",
            "classic": ["Contains Duplicate", "Happy Number", "Intersection of Two Arrays"],
        },
    },
    "Stack / Queue": {
        "Stack": {
            "description": "Last-In-First-Out (LIFO)",
            "subtypes": ["括號匹配", "表達式求值", "單調棧 (Monotonic Stack)"],
            "time": "O(n)",
            "space": "O(n)",
            "use_when": "括號匹配, 表達式計算, 找下一個更大/更小元素",
            "classic": ["Valid Parentheses", "Daily Temperatures", "Largest Rectangle in Histogram"],
        },
        "Queue / Deque": {
            "description": "First-In-First-Out (FIFO) / Double-ended Queue",
            "subtypes": ["BFS 用 Queue", "Sliding Window Maximum 用 Deque"],
            "time": "O(n)",
            "space": "O(n)",
            "use_when": "BFS, 滑動視窗最大值, 設計題 (LRU Cache)",
            "classic": ["Sliding Window Maximum", "Implement Queue using Stacks"],
        },
    },
    "Linked List": {
        "Linked List": {
            "description": "節點串聯的線性結構，擅長 O(1) 插入/刪除",
            "subtypes": ["反轉", "合併", "快慢指標", "Dummy Head 技巧"],
            "time": "O(n)",
            "space": "O(1) 通常原地操作",
            "use_when": "反轉/合併 linked list, 找中點/環, 刪除節點",
            "classic": ["Reverse Linked List", "Merge Two Sorted Lists", "Linked List Cycle"],
        },
    },
    "Binary Search": {
        "Binary Search": {
            "description": "每次排除一半的搜索空間，O(log n) 找目標",
            "subtypes": ["標準搜尋", "Lower/Upper Bound", "Search on Answer", "Rotated Array"],
            "time": "O(log n)",
            "space": "O(1)",
            "use_when": "sorted array 搜尋, 最小化最大值, 找分界點, rotated array",
            "classic": ["Binary Search", "Search in Rotated Sorted Array", "Koko Eating Bananas"],
        },
    },
    "Tree": {
        "DFS (Depth-First Search)": {
            "description": "深度優先：先走到底再回頭",
            "subtypes": ["Preorder (前序)", "Inorder (中序)", "Postorder (後序)", "Recursive / Iterative"],
            "time": "O(n)",
            "space": "O(h) 其中 h = 樹高",
            "use_when": "遍歷所有節點, 求高度/深度, 路徑和, LCA",
            "classic": ["Max Depth", "Path Sum", "Lowest Common Ancestor", "Diameter of Binary Tree"],
        },
        "BFS (Breadth-First Search)": {
            "description": "廣度優先：一層一層走",
            "subtypes": ["Level Order Traversal", "Zigzag Traversal"],
            "time": "O(n)",
            "space": "O(w) 其中 w = 最寬層的寬度",
            "use_when": "層序遍歷, 找最淺的某節點, 序列化/反序列化",
            "classic": ["Binary Tree Level Order Traversal", "Binary Tree Right Side View"],
        },
        "BST (Binary Search Tree)": {
            "description": "左 < 根 < 右 的性質 → Inorder 是排序的",
            "subtypes": ["搜尋/插入/刪除", "驗證 BST", "Inorder 遍歷"],
            "time": "O(h) 平均 O(log n)",
            "space": "O(h)",
            "use_when": "需要排序性質, 找第 K 小, 驗證 BST",
            "classic": ["Validate BST", "Kth Smallest Element in BST", "Convert Sorted Array to BST"],
        },
    },
    "Graph": {
        "Graph DFS": {
            "description": "在 graph 上做深度優先搜索",
            "subtypes": ["遞迴 DFS", "Iterative DFS (Stack)"],
            "time": "O(V + E)",
            "space": "O(V)",
            "use_when": "找 connected components, 走遍所有路徑, cycle detection",
            "classic": ["Number of Islands", "Clone Graph", "Pacific Atlantic Water Flow"],
        },
        "Graph BFS": {
            "description": "在 graph 上做廣度優先搜索（找最短路徑）",
            "subtypes": ["單源 BFS", "多源 BFS", "Bidirectional BFS"],
            "time": "O(V + E)",
            "space": "O(V)",
            "use_when": "無權重圖的最短路徑, 層級擴散",
            "classic": ["Word Ladder", "Rotting Oranges", "Shortest Path in Binary Matrix"],
        },
        "Topological Sort": {
            "description": "有向無環圖 (DAG) 的線性排序",
            "subtypes": ["Kahn's (BFS-based)", "DFS-based"],
            "time": "O(V + E)",
            "space": "O(V)",
            "use_when": "任務依賴排序, 課程先修, 判斷 DAG",
            "classic": ["Course Schedule", "Course Schedule II", "Alien Dictionary"],
        },
        "Union-Find": {
            "description": "用於動態連通性問題",
            "subtypes": ["Path Compression", "Union by Rank"],
            "time": "O(α(n)) ≈ O(1) per operation",
            "space": "O(n)",
            "use_when": "動態判斷連通, 合併集合, 找環",
            "classic": ["Number of Connected Components", "Redundant Connection", "Accounts Merge"],
        },
        "Shortest Path": {
            "description": "有權重圖的最短路徑",
            "subtypes": ["Dijkstra (非負)", "Bellman-Ford (可負)", "Floyd-Warshall (全對)"],
            "time": "Dijkstra: O(E log V)",
            "space": "O(V + E)",
            "use_when": "有權重的最短路徑, 網路延遲, 最少花費",
            "classic": ["Network Delay Time", "Cheapest Flights Within K Stops"],
        },
    },
    "Dynamic Programming": {
        "DP 1D": {
            "description": "一維狀態轉移：dp[i] 只依賴之前的值",
            "subtypes": ["爬樓梯型", "搶劫型", "最長遞增子序列 (LIS)"],
            "time": "O(n) 或 O(n²)",
            "space": "O(n) 可優化到 O(1)",
            "use_when": "求方法數/最大值/最小值，且有重疊子問題",
            "classic": ["Climbing Stairs", "House Robber", "Coin Change", "Word Break"],
        },
        "DP 2D": {
            "description": "二維狀態轉移：dp[i][j] 依賴相鄰格子",
            "subtypes": ["Grid DP", "LCS", "Edit Distance"],
            "time": "O(m × n)",
            "space": "O(m × n) 可優化到 O(n)",
            "use_when": "二維棋盤/字串比對/子序列問題",
            "classic": ["Unique Paths", "Longest Common Subsequence", "Edit Distance"],
        },
        "Knapsack": {
            "description": "背包問題：有容量限制下的最佳選擇",
            "subtypes": ["0/1 Knapsack", "Unbounded Knapsack", "Subset Sum"],
            "time": "O(n × W)",
            "space": "O(W) 一維優化",
            "use_when": "選/不選決策, 容量限制, 子集和",
            "classic": ["Partition Equal Subset Sum", "Coin Change", "Target Sum"],
        },
    },
    "Backtracking": {
        "Backtracking": {
            "description": "嘗試所有可能 + 遇到不合法就回頭（DFS + 剪枝）",
            "subtypes": ["排列 (Permutation)", "組合 (Combination)", "子集 (Subset)", "棋盤問題"],
            "time": "O(2^n) 或 O(n!)",
            "space": "O(n)",
            "use_when": "列舉所有可能, 排列組合, N-Queens, Sudoku",
            "classic": ["Subsets", "Permutations", "Combination Sum", "N-Queens", "Word Search"],
        },
    },
    "Greedy": {
        "Greedy": {
            "description": "每步做局部最優選擇，期望得到全域最優",
            "subtypes": ["排序後貪心", "區間貪心", "Jump Game 系列"],
            "time": "通常 O(n log n) (排序) 或 O(n)",
            "space": "O(1) 或 O(n)",
            "use_when": "局部最優 → 全域最優, 區間排程, 最少操作次數",
            "classic": ["Jump Game", "Merge Intervals", "Non-overlapping Intervals", "Task Scheduler"],
        },
    },
    "Heap / Priority Queue": {
        "Heap": {
            "description": "維護動態最大/最小值，O(log n) 插入/刪除",
            "subtypes": ["Min-Heap", "Max-Heap", "Top K", "Merge K Sorted"],
            "time": "O(n log k) 通常",
            "space": "O(k)",
            "use_when": "Top K 問題, 動態中位數, 合併 K 個排序結構",
            "classic": ["Kth Largest Element", "Top K Frequent Elements", "Merge K Sorted Lists"],
        },
    },
    "Trie": {
        "Trie": {
            "description": "前綴樹：用樹結構存儲字串集合",
            "subtypes": ["Insert", "Search", "StartsWith", "Word Search II"],
            "time": "O(L) 每次操作，L = 字串長度",
            "space": "O(Σ所有字串長度)",
            "use_when": "前綴查詢, 自動補全, 多字串搜尋",
            "classic": ["Implement Trie", "Word Search II", "Design Add and Search Words"],
        },
    },
    "Sorting / Bit": {
        "Sorting": {
            "description": "排序演算法",
            "subtypes": ["Quick Sort O(n log n)", "Merge Sort O(n log n)", "Counting Sort O(n+k)"],
            "time": "O(n log n)",
            "space": "O(n) Merge Sort / O(1) Quick Sort",
            "use_when": "需要排序, 合併區間, 找第 K 大",
            "classic": ["Sort Colors", "Merge Intervals", "Kth Largest Element"],
        },
        "Bit Manipulation": {
            "description": "用位元運算解決問題",
            "subtypes": ["XOR 找唯一", "AND/OR 性質", "移位操作"],
            "time": "O(n) 或 O(1)",
            "space": "O(1)",
            "use_when": "找唯一/缺失數字, 判斷 2 的冪, 計算 1 的位元數",
            "classic": ["Single Number", "Counting Bits", "Reverse Bits", "Power of Two"],
        },
    },
}


# =============================================================================
# Section 2: 時間/空間複雜度速查表
# =============================================================================

COMPLEXITY_TABLE = [
    # (算法, Time Complexity, Space Complexity, 備註)
    ("Two Pointers",        "O(n)",         "O(1)",         "需要 sorted 或可原地操作"),
    ("Sliding Window",      "O(n)",         "O(k)",         "k = 視窗大小或字元集大小"),
    ("Prefix Sum",          "O(n)",         "O(n)",         "預處理 O(n), 查詢 O(1)"),
    ("HashMap / HashSet",   "O(n)",         "O(n)",         "平均情況, worst case O(n²)"),
    ("Stack / Queue",       "O(n)",         "O(n)",         "每個元素最多進出各一次"),
    ("Monotonic Stack",     "O(n)",         "O(n)",         "每個元素最多進出 stack 各一次"),
    ("Linked List",         "O(n)",         "O(1)",         "通常原地操作"),
    ("Binary Search",       "O(log n)",     "O(1)",         "Iterative 版本"),
    ("Tree DFS",            "O(n)",         "O(h)",         "h = 樹高, worst O(n)"),
    ("Tree BFS",            "O(n)",         "O(w)",         "w = 最寬層的寬度"),
    ("Graph DFS / BFS",     "O(V + E)",     "O(V)",         "V = vertices, E = edges"),
    ("Topological Sort",    "O(V + E)",     "O(V)",         "只適用 DAG"),
    ("Union-Find",          "O(α(n)) ≈ O(1)", "O(n)",      "with Path Compression + Union by Rank"),
    ("Dijkstra",            "O(E log V)",   "O(V + E)",     "用 Min-Heap 實作"),
    ("Bellman-Ford",        "O(V × E)",     "O(V)",         "可處理負權重"),
    ("Floyd-Warshall",      "O(V³)",        "O(V²)",        "所有點對最短路徑"),
    ("DP 1D",               "O(n)",         "O(n) → O(1)", "可滾動陣列優化"),
    ("DP 2D",               "O(m × n)",     "O(m × n) → O(n)", "可滾動陣列優化"),
    ("Knapsack",            "O(n × W)",     "O(W)",         "一維優化版本"),
    ("Backtracking",        "O(2^n) / O(n!)", "O(n)",       "看問題而定"),
    ("Greedy",              "O(n log n)",   "O(1)",         "排序後通常 O(n)"),
    ("Heap (Top K)",        "O(n log k)",   "O(k)",         "k = 要找的前 K 個"),
    ("Merge Sort",          "O(n log n)",   "O(n)",         "穩定排序"),
    ("Quick Sort",          "O(n log n)",   "O(log n)",     "平均情況, worst O(n²)"),
    ("Trie",                "O(L)",         "O(ΣL)",        "L = 字串長度"),
    ("Bit Manipulation",    "O(n) / O(1)",  "O(1)",         "位元運算常數時間"),
]


# =============================================================================
# Section 3: 關鍵字 → 算法 對照表
# =============================================================================

KEYWORD_TO_ALGORITHM = {
    # ── Array / String 相關 ──
    "sorted array + 找某組合": "Two Pointers (反向)",
    "原地 remove / deduplicate": "Two Pointers (同向: 快慢指標)",
    "palindrome 判斷": "Two Pointers (反向: 從兩端向中間)",
    "連續子陣列 (contiguous subarray)": "Sliding Window 或 Prefix Sum",
    "最長/最短 substring 滿足某條件": "Sliding Window (可變長度)",
    "固定長度 k 的子陣列": "Sliding Window (固定長度)",
    "subarray sum = k": "Prefix Sum + HashMap",
    "求區間和 (range sum query)": "Prefix Sum",

    # ── Hash 相關 ──
    "O(1) 查找是否存在": "HashSet",
    "counting 出現次數": "HashMap (Counter)",
    "分組 (group by)": "HashMap (key = 分組依據, value = list)",
    "anagram 相關": "HashMap (sorted string 或 char count 為 key)",
    "two sum 系列": "HashMap (存 complement)",

    # ── Stack / Queue 相關 ──
    "括號匹配 / 嵌套結構": "Stack",
    "下一個更大/更小元素": "Monotonic Stack",
    "表達式求值 (calculator)": "Stack (運算符 + 數字兩個 stack)",
    "BFS / 層序遍歷": "Queue",
    "滑動視窗最大值": "Deque (Monotonic Deque)",
    "設計 LRU Cache": "HashMap + Doubly Linked List (或 OrderedDict)",

    # ── Linked List 相關 ──
    "反轉 linked list": "Iterative (prev, curr, next) 或 Recursive",
    "找中點 / 判斷環": "快慢指標 (Floyd's Cycle Detection)",
    "合併兩個/K個 sorted list": "Two Pointers / Heap",
    "刪除倒數第 N 個節點": "快慢指標 (fast 先走 N 步)",

    # ── Binary Search 相關 ──
    "sorted array 找目標": "Binary Search",
    "找最小的滿足條件的值": "Binary Search (Lower Bound)",
    "找最大的滿足條件的值": "Binary Search (Upper Bound)",
    "最小化最大值 / 最大化最小值": "Binary Search on Answer",
    "rotated sorted array": "Binary Search (判斷哪半邊有序)",
    "Koko eating bananas / 分配類": "Binary Search on Answer",

    # ── Tree 相關 ──
    "tree 的高度/深度": "DFS (後序)",
    "tree 的路徑和": "DFS (前序或後序)",
    "LCA (最低共同祖先)": "DFS (後序 + 左右回傳)",
    "層序遍歷 (level order)": "BFS (用 Queue)",
    "BST 找第 K 小": "Inorder Traversal (中序 = 排序)",
    "驗證 BST": "Inorder (檢查遞增) 或 DFS (帶範圍)",
    "serialize / deserialize tree": "BFS 或 Preorder DFS",

    # ── Graph 相關 ──
    "島嶼問題 / 連通區域": "Graph DFS 或 BFS (flood fill)",
    "任務依賴 / 課程先修": "Topological Sort",
    "動態連通性 / 合併集合": "Union-Find",
    "無權重最短路徑": "BFS",
    "有權重最短路徑 (非負)": "Dijkstra",
    "有權重最短路徑 (可負)": "Bellman-Ford",
    "所有點對最短路徑": "Floyd-Warshall",
    "判斷 DAG / 有向圖有環": "Topological Sort (Kahn's) 或 DFS (三色標記)",
    "判斷無向圖有環": "Union-Find 或 DFS",

    # ── DP 相關 ──
    "爬樓梯 / Fibonacci 型": "DP 1D (dp[i] = dp[i-1] + dp[i-2])",
    "搶劫問題 (不能相鄰)": "DP 1D (dp[i] = max(dp[i-1], dp[i-2] + val))",
    "硬幣兌換 / 最少操作次數": "DP 1D (Unbounded Knapsack)",
    "最長遞增子序列 (LIS)": "DP O(n²) 或 Binary Search O(n log n)",
    "Word Break": "DP 1D + HashSet",
    "棋盤路徑 (unique paths)": "DP 2D",
    "字串比對 (LCS / Edit Distance)": "DP 2D",
    "子集和 / partition": "0/1 Knapsack (DP)",

    # ── Backtracking 相關 ──
    "列舉所有排列": "Backtracking (swap 或 used[] 標記)",
    "列舉所有組合": "Backtracking (start index 避免重複)",
    "列舉所有子集": "Backtracking (選或不選)",
    "N-Queens / Sudoku": "Backtracking + 剪枝",
    "Word Search (在棋盤上找字)": "Backtracking + DFS",

    # ── Greedy 相關 ──
    "區間排程 / 不重疊區間": "Greedy (按結束時間排序)",
    "合併區間": "Greedy (按開始時間排序)",
    "Jump Game": "Greedy (追蹤最遠可達)",
    "分配問題 (assign cookies)": "Greedy (排序後匹配)",

    # ── Heap 相關 ──
    "Top K / Kth largest": "Heap (Min-Heap of size K)",
    "動態中位數": "Two Heaps (Max-Heap + Min-Heap)",
    "合併 K 個 sorted list": "Heap (Min-Heap)",

    # ── Trie 相關 ──
    "前綴搜尋 / autocomplete": "Trie",
    "多字串同時搜尋": "Trie + DFS/BFS",

    # ── Bit 相關 ──
    "找唯一出現一次的數字": "XOR (a ^ a = 0)",
    "判斷 2 的冪": "n & (n - 1) == 0",
    "計算二進位中 1 的個數": "n & (n - 1) 逐步消除",
}


# =============================================================================
# Section 4: Pattern Recognition — 20+ 種常見 Pattern
# =============================================================================

PATTERNS = [
    {
        "id": 1,
        "name": "Two Pointers — 反向夾擊",
        "signal": "sorted array + 找兩數之和",
        "example": "Two Sum II: nums=[2,7,11,15], target=9 → left=0, right=3 → 2+15=17>9 → right-- → 2+11=13>9 → right-- → 2+7=9 ✓",
        "template": "left, right = 0, len(nums)-1; while left < right: 比較 sum 與 target",
    },
    {
        "id": 2,
        "name": "Two Pointers — 快慢指標",
        "signal": "原地刪除/去重，或 linked list 找環/中點",
        "example": "Remove Duplicates: [1,1,2,3,3] → slow=0, fast 掃描 → 遇到新值就 slow++ 寫入 → [1,2,3,_,_], return 3",
        "template": "slow = 0; for fast in range(n): if nums[fast] != nums[slow]: slow += 1; nums[slow] = nums[fast]",
    },
    {
        "id": 3,
        "name": "Sliding Window — 可變長度",
        "signal": "最長/最短的連續子陣列/子字串滿足某條件",
        "example": "Longest Substring Without Repeating: 'abcabcbb' → 視窗 [a]→[ab]→[abc]→ 遇到重複 a → 縮左 → [bca]→... → 答案 3",
        "template": "left = 0; for right in range(n): 加入 right; while 不滿足條件: 移除 left, left += 1; 更新答案",
    },
    {
        "id": 4,
        "name": "Sliding Window — 固定長度",
        "signal": "固定大小 k 的子陣列的最大/最小/平均",
        "example": "Max Average Subarray k=3: [1,12,-5,-6,50,3] → 視窗 [1,12,-5]=8 → [12,-5,-6]=1 → [-5,-6,50]=39 → [-6,50,3]=47 → 答案 47/3",
        "template": "window_sum = sum(nums[:k]); for i in range(k, n): window_sum += nums[i] - nums[i-k]; 更新答案",
    },
    {
        "id": 5,
        "name": "HashMap — One-Pass Lookup",
        "signal": "找配對 (complement), O(1) 查找",
        "example": "Two Sum: nums=[2,7,11,15], target=9 → 看到 2, 存 {2:0} → 看到 7, 查 9-7=2 存在! → return [0,1]",
        "template": "seen = {}; for i, num in enumerate(nums): comp = target - num; if comp in seen: return [seen[comp], i]; seen[num] = i",
    },
    {
        "id": 6,
        "name": "Prefix Sum + HashMap",
        "signal": "子陣列和 = 目標值 的個數",
        "example": "Subarray Sum=K: [1,2,3], k=3 → prefix=[0,1,3,6] → 每步查 prefix-k 是否在 map → prefix=3, 3-3=0 在! → count++",
        "template": "prefix = 0; count_map = {0: 1}; for num: prefix += num; count += count_map.get(prefix - k, 0); count_map[prefix] += 1",
    },
    {
        "id": 7,
        "name": "Monotonic Stack — 下一個更大元素",
        "signal": "對每個元素找右邊第一個比它大的",
        "example": "Daily Temperatures: [73,74,75,71,69,72,76,73] → stack 存 index → 73 入 → 74>73 出算差 1 → ... → 答案 [1,1,4,2,1,1,0,0]",
        "template": "stack = []; result = [0]*n; for i in range(n): while stack and nums[i] > nums[stack[-1]]: j = stack.pop(); result[j] = i - j; stack.append(i)",
    },
    {
        "id": 8,
        "name": "Binary Search — 標準模板",
        "signal": "sorted array 找目標值",
        "example": "nums=[1,3,5,7,9], target=5 → lo=0,hi=4 → mid=2, nums[2]=5 ✓ → return 2",
        "template": "lo, hi = 0, len(nums)-1; while lo <= hi: mid = (lo+hi)//2; if nums[mid]==target: return mid; elif nums[mid]<target: lo=mid+1; else: hi=mid-1",
    },
    {
        "id": 9,
        "name": "Binary Search on Answer",
        "signal": "最小化最大值 / 答案有單調性",
        "example": "Koko Eating Bananas: piles=[3,6,7,11], h=8 → 答案在 [1,11] → 試 mid=6: 需 1+1+2+2=6 天 ≤ 8 ✓ → 試更小 → ... → 答案 4",
        "template": "lo, hi = min_possible, max_possible; while lo < hi: mid = (lo+hi)//2; if feasible(mid): hi = mid; else: lo = mid + 1; return lo",
    },
    {
        "id": 10,
        "name": "Tree DFS — 遞迴求高度",
        "signal": "求 tree 的高度/深度/直徑",
        "example": "Max Depth: root=[3,9,20,null,null,15,7] → 左子樹高度 1(只有9) → 右子樹高度 2(20→15或7) → max(1,2)+1 = 3",
        "template": "def dfs(node): if not node: return 0; return 1 + max(dfs(node.left), dfs(node.right))",
    },
    {
        "id": 11,
        "name": "Tree BFS — Level Order",
        "signal": "一層一層遍歷 tree",
        "example": "Level Order: root=[3,9,20,null,null,15,7] → queue=[3] → 取出 3, 加入 [9,20] → 取出 9,20, 加入 [15,7] → [[3],[9,20],[15,7]]",
        "template": "queue = deque([root]); while queue: level = []; for _ in range(len(queue)): node = queue.popleft(); level.append(node.val); 加入左右子",
    },
    {
        "id": 12,
        "name": "Graph BFS — 最短路徑 (無權重)",
        "signal": "在 grid/graph 上找最少步數",
        "example": "Number of Islands: grid 裡遇到 '1' → BFS 把整座島標記為 '0' → 計數 ++ → 繼續掃描",
        "template": "visited + queue; 從起點出發; while queue: 取出節點; for 四個方向: if 合法且未訪問: 加入 queue",
    },
    {
        "id": 13,
        "name": "Topological Sort — Kahn's Algorithm",
        "signal": "任務依賴排序 / 判斷是否存在環",
        "example": "Course Schedule: n=4, prereqs=[[1,0],[2,0],[3,1],[3,2]] → in-degree: [0,1,1,2] → queue=[0] → 0→1,2 → 1→3, 2→3 → order=[0,1,2,3]",
        "template": "計算 in-degree → queue = [所有 in-degree=0 的節點] → while queue: 取出 u, 對 u 的鄰居 v: in_degree[v]-=1, 若 =0 加入 queue",
    },
    {
        "id": 14,
        "name": "Union-Find — 動態連通",
        "signal": "動態合併集合 + 判斷連通",
        "example": "Number of Components: n=5, edges=[[0,1],[1,2],[3,4]] → union(0,1) → union(1,2) → union(3,4) → 2 個 component",
        "template": "parent = list(range(n)); def find(x): 路徑壓縮; def union(x,y): 合併; connected = n; 每次 union 成功: connected -= 1",
    },
    {
        "id": 15,
        "name": "DP 1D — 爬樓梯型",
        "signal": "第 i 步依賴前 1~2 步",
        "example": "Climbing Stairs n=5: dp[1]=1, dp[2]=2, dp[3]=3, dp[4]=5, dp[5]=8 → 答案 8",
        "template": "dp[0]=base; dp[1]=base; for i in range(2, n+1): dp[i] = dp[i-1] + dp[i-2]",
    },
    {
        "id": 16,
        "name": "DP 1D — Coin Change 型",
        "signal": "用最少硬幣湊出目標值",
        "example": "Coin Change: coins=[1,2,5], amount=11 → dp[0]=0, dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=2, dp[5]=1, ..., dp[11]=3 (5+5+1)",
        "template": "dp = [inf]*(amount+1); dp[0]=0; for i in range(1, amount+1): for coin in coins: if i>=coin: dp[i] = min(dp[i], dp[i-coin]+1)",
    },
    {
        "id": 17,
        "name": "DP 2D — LCS (最長共同子序列)",
        "signal": "兩字串的最長共同子序列",
        "example": "LCS('abcde','ace') → 填表: a-a=1, c-c=2, e-e=3 → 答案 3",
        "template": "dp[i][j] = dp[i-1][j-1]+1 if s1[i]==s2[j] else max(dp[i-1][j], dp[i][j-1])",
    },
    {
        "id": 18,
        "name": "Backtracking — 子集列舉",
        "signal": "列舉所有子集/組合",
        "example": "Subsets [1,2,3] → []→[1]→[1,2]→[1,2,3]→[1,3]→[2]→[2,3]→[3] → 共 8 個",
        "template": "def backtrack(start, path): result.append(path[:]); for i in range(start, n): path.append(nums[i]); backtrack(i+1, path); path.pop()",
    },
    {
        "id": 19,
        "name": "Greedy — 區間排程",
        "signal": "最多不重疊區間 / 最少移除讓不重疊",
        "example": "Non-overlapping Intervals: [[1,2],[2,3],[3,4],[1,3]] → 按結束時間排序 → [1,2],[2,3],[3,4] → 移除 1 個 [1,3]",
        "template": "按結束時間排序; end = intervals[0][1]; count = 1; for 每個 interval: if start >= end: count += 1; end = 此 interval 的結束",
    },
    {
        "id": 20,
        "name": "Heap — Top K",
        "signal": "找第 K 大/小 或 前 K 個高頻",
        "example": "Kth Largest k=2: [3,2,1,5,6,4] → Min-Heap 維護 size 2 → 最後 heap[0] = 5",
        "template": "import heapq; heap = []; for num in nums: heapq.heappush(heap, num); if len(heap) > k: heapq.heappop(heap); return heap[0]",
    },
    {
        "id": 21,
        "name": "Dijkstra — 有權重最短路徑",
        "signal": "有正權重的 graph 最短路徑",
        "example": "Network Delay Time: n=4, [[2,1,1],[2,3,1],[3,4,1]], src=2 → dist=[inf,1,0,1,2] → 最大 = 2",
        "template": "dist = [inf]*n; dist[src]=0; heap = [(0, src)]; while heap: d, u = heappop(heap); for v, w in graph[u]: if d+w < dist[v]: dist[v]=d+w; heappush(heap, (d+w, v))",
    },
    {
        "id": 22,
        "name": "Trie — 前綴樹",
        "signal": "大量字串的前綴查詢",
        "example": "insert('apple'), insert('app') → search('app')=True, startsWith('app')=True, search('ap')=False",
        "template": "class TrieNode: children = {}; is_end = False; insert: 逐字元建節點; search: 逐字元走, 檢查 is_end",
    },
    {
        "id": 23,
        "name": "Bit — XOR 找唯一",
        "signal": "陣列中只有一個數字出現一次，其他出現兩次",
        "example": "Single Number: [4,1,2,1,2] → 4^1^2^1^2 = 4^(1^1)^(2^2) = 4^0^0 = 4",
        "template": "result = 0; for num in nums: result ^= num; return result",
    },
]


# =============================================================================
# Section 5: Decision Tree Function
# =============================================================================

def decide_algorithm(
    data_structure: str = "",
    sorted_input: bool = False,
    keywords: list = None,
    need_all_solutions: bool = False,
    optimization_type: str = "",
    graph_type: str = "",
) -> list:
    """
    Decision Tree：輸入題目特徵，回傳建議的演算法清單。

    Parameters
    ----------
    data_structure : str
        輸入的資料結構，例如 "array", "string", "tree", "graph", "linked_list", "matrix"
    sorted_input : bool
        輸入是否已排序
    keywords : list
        題目中出現的關鍵字，例如 ["subarray", "sum", "target"]
    need_all_solutions : bool
        是否要求列舉所有可能解
    optimization_type : str
        最佳化類型："max", "min", "count", "exists", ""
    graph_type : str
        如果是 Graph 問題："unweighted", "weighted_positive", "weighted_negative", "dag"

    Returns
    -------
    list of str
        建議的演算法列表，按推薦程度排序
    """
    if keywords is None:
        keywords = []
    keywords_set = set(k.lower() for k in keywords)
    suggestions = []

    # ── Array / String 分支 ──
    if data_structure in ("array", "string"):
        if sorted_input:
            suggestions.append("Two Pointers (反向)")
            suggestions.append("Binary Search")
        if "subarray" in keywords_set or "contiguous" in keywords_set:
            if "sum" in keywords_set:
                suggestions.append("Prefix Sum + HashMap")
            suggestions.append("Sliding Window")
        if "substring" in keywords_set:
            suggestions.append("Sliding Window")
            suggestions.append("Two Pointers")
        if "palindrome" in keywords_set:
            suggestions.append("Two Pointers (反向: 從兩端)")
            suggestions.append("DP 2D (區間 DP)")
        if "anagram" in keywords_set:
            suggestions.append("HashMap (字元計數)")
            suggestions.append("Sliding Window + HashMap")
        if "pair" in keywords_set or "two sum" in keywords_set:
            suggestions.append("HashMap (One-Pass Lookup)")
        if "duplicate" in keywords_set:
            suggestions.append("HashSet")
            suggestions.append("Two Pointers (如果 sorted)")
        if "interval" in keywords_set or "merge" in keywords_set:
            suggestions.append("Greedy (排序後合併)")
        if "k-th" in keywords_set or "top k" in keywords_set:
            suggestions.append("Heap (Min-Heap of size K)")
            suggestions.append("Quick Select O(n)")
        if "permutation" in keywords_set:
            suggestions.append("Backtracking")
        if "next greater" in keywords_set or "next smaller" in keywords_set:
            suggestions.append("Monotonic Stack")
        if not suggestions:
            suggestions.append("HashMap / HashSet (先想 O(n) 解法)")
            suggestions.append("Two Pointers (如果可以排序)")

    # ── Tree 分支 ──
    elif data_structure == "tree":
        if "level order" in keywords_set or "bfs" in keywords_set:
            suggestions.append("BFS (Queue)")
        if "depth" in keywords_set or "height" in keywords_set:
            suggestions.append("DFS (後序)")
        if "path sum" in keywords_set or "path" in keywords_set:
            suggestions.append("DFS (前序或後序)")
        if "lca" in keywords_set or "ancestor" in keywords_set:
            suggestions.append("DFS (後序, 左右回傳)")
        if "bst" in keywords_set:
            suggestions.append("Inorder Traversal (中序 = 排序)")
            suggestions.append("DFS with Range [lo, hi]")
        if "serialize" in keywords_set:
            suggestions.append("BFS 或 Preorder DFS")
        if not suggestions:
            suggestions.append("DFS (Recursive)")
            suggestions.append("BFS (如果需要層序)")

    # ── Graph 分支 ──
    elif data_structure == "graph":
        if graph_type == "dag" or "dependency" in keywords_set or "prerequisite" in keywords_set:
            suggestions.append("Topological Sort (Kahn's BFS)")
        if "connected" in keywords_set or "component" in keywords_set:
            suggestions.append("Union-Find")
            suggestions.append("DFS / BFS")
        if "shortest path" in keywords_set or "minimum steps" in keywords_set:
            if graph_type == "unweighted":
                suggestions.append("BFS")
            elif graph_type == "weighted_positive":
                suggestions.append("Dijkstra (Min-Heap)")
            elif graph_type == "weighted_negative":
                suggestions.append("Bellman-Ford")
            else:
                suggestions.append("BFS (無權重) 或 Dijkstra (有權重)")
        if "cycle" in keywords_set:
            suggestions.append("Topological Sort (有向圖)")
            suggestions.append("Union-Find (無向圖)")
            suggestions.append("DFS 三色標記 (有向圖)")
        if "island" in keywords_set or "grid" in keywords_set:
            suggestions.append("DFS / BFS (Flood Fill)")
        if not suggestions:
            suggestions.append("DFS / BFS")

    # ── Linked List 分支 ──
    elif data_structure == "linked_list":
        if "reverse" in keywords_set:
            suggestions.append("Iterative (prev, curr, next)")
        if "cycle" in keywords_set or "middle" in keywords_set:
            suggestions.append("快慢指標 (Floyd's)")
        if "merge" in keywords_set:
            suggestions.append("Two Pointers / Heap")
        if "remove" in keywords_set:
            suggestions.append("Dummy Head + Two Pointers")
        if not suggestions:
            suggestions.append("Dummy Head 技巧")
            suggestions.append("快慢指標")

    # ── Matrix 分支 ──
    elif data_structure == "matrix":
        if "shortest path" in keywords_set:
            suggestions.append("BFS")
        if "path" in keywords_set and optimization_type in ("count", "max", "min"):
            suggestions.append("DP 2D")
        if "island" in keywords_set or "connected" in keywords_set:
            suggestions.append("DFS / BFS (Flood Fill)")
        if "rotate" in keywords_set or "spiral" in keywords_set:
            suggestions.append("模擬 (Simulation) with 邊界追蹤")
        if not suggestions:
            suggestions.append("DFS / BFS 或 DP 2D")

    # ── 列舉型問題 ──
    if need_all_solutions:
        suggestions.insert(0, "Backtracking (DFS + 剪枝)")

    # ── 最佳化問題 (如果還沒有建議) ──
    if optimization_type in ("max", "min", "count") and not suggestions:
        suggestions.append("Dynamic Programming")
        suggestions.append("Greedy (如果局部最優 = 全域最優)")

    return suggestions if suggestions else ["先嘗試 Brute Force，再看能否用 HashMap 優化到 O(n)"]


# =============================================================================
# Section 6: Print Functions (Beautiful Formatted Output)
# =============================================================================

def print_separator(char="=", width=78):
    print(char * width)


def print_title(title):
    print()
    print_separator("=")
    print(f"  {title}")
    print_separator("=")
    print()


def print_subtitle(title):
    print()
    print(f"  --- {title} ---")
    print()


def print_complexity_table():
    """印出完整的複雜度速查表。"""
    print_title("時間/空間複雜度速查表 (Complexity Cheat Sheet)")

    header = f"  {'算法':<24} {'Time':<22} {'Space':<18} {'備註'}"
    print(header)
    print("  " + "-" * 74)

    for algo, time_c, space_c, note in COMPLEXITY_TABLE:
        print(f"  {algo:<24} {time_c:<22} {space_c:<18} {note}")


def print_keyword_table():
    """印出「關鍵字 → 算法」對照表。"""
    print_title("看到什麼關鍵字 → 用什麼算法 (Keyword → Algorithm)")

    max_key_len = 40
    for keyword, algo in KEYWORD_TO_ALGORITHM.items():
        # 截斷過長的 keyword 以維持排版
        key_display = keyword[:max_key_len].ljust(max_key_len)
        print(f"  {key_display} → {algo}")


def print_pattern_list():
    """印出所有 Pattern 辨識範例。"""
    print_title("常見 Pattern 辨識 (20+ Patterns)")

    for p in PATTERNS:
        print(f"  [{p['id']:>2}] {p['name']}")
        print(f"       辨識信號: {p['signal']}")
        print(f"       範例: {p['example'][:90]}{'...' if len(p['example']) > 90 else ''}")
        print()


def print_algorithm_catalog():
    """印出完整的算法分類表。"""
    print_title("算法分類表 (Algorithm Catalog)")

    for category, algorithms in ALGORITHM_CATALOG.items():
        print(f"  [{category}]")
        for algo_name, info in algorithms.items():
            print(f"    ▸ {algo_name}")
            print(f"      說明: {info['description']}")
            print(f"      子類: {', '.join(info['subtypes'])}")
            print(f"      Time: {info['time']}  |  Space: {info['space']}")
            print(f"      使用時機: {info['use_when']}")
            print(f"      經典題: {', '.join(info['classic'][:3])}")
            print()


def print_decision_tree_visual():
    """印出 Decision Tree 的視覺化版本。"""
    print_title("Decision Tree — 解題思路流程圖")

    tree = """
  收到題目
  │
  ├── 題目給的是什麼資料結構？
  │   │
  │   ├── Array / String
  │   │   ├── Input 已 sorted？
  │   │   │   ├── Yes → Two Pointers / Binary Search
  │   │   │   └── No  → 可以排序嗎？
  │   │   │       ├── Yes → 排序後 Two Pointers
  │   │   │       └── No  → HashMap / Sliding Window
  │   │   │
  │   │   ├── 要找「連續子陣列/子字串」？
  │   │   │   ├── 和/積 相關 → Prefix Sum + HashMap
  │   │   │   ├── 最長/最短滿足條件 → Sliding Window
  │   │   │   └── 固定長度 k → Sliding Window (固定)
  │   │   │
  │   │   ├── 要找配對 (pair)？ → HashMap (one-pass)
  │   │   ├── 要去重/判斷存在？ → HashSet
  │   │   ├── 找下一個更大/更小？ → Monotonic Stack
  │   │   └── 區間合併/排程？ → Greedy (排序後)
  │   │
  │   ├── Linked List
  │   │   ├── 反轉 → Iterative (prev/curr/next)
  │   │   ├── 找中點/環 → 快慢指標
  │   │   ├── 合併 sorted → Two Pointers / Heap
  │   │   └── 刪除節點 → Dummy Head + 快慢指標
  │   │
  │   ├── Tree
  │   │   ├── 需要層序 (level-by-level)？ → BFS (Queue)
  │   │   ├── 需要深度/高度/路徑？ → DFS (Recursive)
  │   │   ├── BST 相關？ → Inorder = 排序
  │   │   └── Serialize / Clone？ → BFS 或 Preorder DFS
  │   │
  │   ├── Graph
  │   │   ├── 有向 + 依賴關係？ → Topological Sort
  │   │   ├── 連通性 / 動態合併？ → Union-Find
  │   │   ├── 最短路徑？
  │   │   │   ├── 無權重 → BFS
  │   │   │   ├── 有正權重 → Dijkstra
  │   │   │   └── 有負權重 → Bellman-Ford
  │   │   ├── 島嶼/flood fill？ → DFS / BFS
  │   │   └── 偵測環？ → Topo Sort (有向) / Union-Find (無向)
  │   │
  │   └── Matrix (二維陣列)
  │       ├── 路徑計數/最值 → DP 2D
  │       ├── 最短路徑 → BFS
  │       ├── 連通區域 → DFS / BFS
  │       └── 旋轉/螺旋 → Simulation
  │
  ├── 問題要求什麼？
  │   │
  │   ├── 列舉「所有」排列/組合/子集 → Backtracking
  │   ├── 求「最值」(最大/最小/最長/最短)
  │   │   ├── 有重疊子問題？ → Dynamic Programming
  │   │   └── 局部最優 = 全域最優？ → Greedy
  │   ├── 求「個數/方法數」 → Dynamic Programming
  │   ├── Top K / Kth largest → Heap (Min-Heap size K)
  │   ├── 前綴搜尋 → Trie
  │   └── 位元操作 → Bit Manipulation
  │
  └── 還是想不到？ → 先寫 Brute Force，再看怎麼優化
      ├── O(n²) → 能否用 HashMap 降到 O(n)？
      ├── O(n²) → 能否排序後用 Two Pointers？
      ├── O(2^n) → 能否用 DP memoization？
      └── 逐步優化，面試官會引導你
"""
    print(tree)


def print_interview_tips():
    """印出面試小提醒。"""
    print_title("面試解題流程 (Interview Framework)")

    tips = """
  Step 1: Clarify（問清楚）— 2 分鐘
  ────────────────────────────────────
  • Input 的範圍？ (n 最大多少？值域？)
  • 有沒有 duplicate？ 是否 sorted？
  • Return 什麼？ (index, value, boolean, list?)
  • Edge cases：空陣列？ 一個元素？ 負數？

  Step 2: Approach（想解法）— 5 分鐘
  ────────────────────────────────────
  • 先說 Brute Force：「最直覺的方式是 ... O(n²)」
  • 再優化：「我們可以用 ... 把它降到 O(n)」
  • 用 Decision Tree 辨識 Pattern
  • 說出 Time / Space Complexity

  Step 3: Code（寫程式）— 15~20 分鐘
  ────────────────────────────────────
  • 先寫 function signature
  • 邊寫邊解釋每一步
  • 變數命名有意義 (left, right, count, NOT i, j, k)
  • 不要怕寫 helper function

  Step 4: Test（測試）— 5 分鐘
  ────────────────────────────────────
  • 用一個小 example 手動 trace（最重要！）
  • 想 edge cases 並測試
  • 發現 bug → 冷靜修復，解釋原因
"""
    print(tips)


def print_quick_cheatsheet():
    """印出一頁式速查表（最精華摘要）。"""
    print_title("一頁速查表 (One-Page Cheat Sheet)")

    cheat = """
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    看到什麼 → 用什麼（精華版）                        │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  sorted array + 找配對        → Two Pointers (反向)                 │
  │  連續子陣列/子字串的最值      → Sliding Window                       │
  │  子陣列和 = K                 → Prefix Sum + HashMap                │
  │  O(1) 查找/去重              → HashMap / HashSet                    │
  │  括號匹配/嵌套               → Stack                                │
  │  下一個更大元素               → Monotonic Stack                      │
  │  sorted array 找值            → Binary Search                       │
  │  最小化最大值                 → Binary Search on Answer              │
  │  Tree 深度/路徑               → DFS (Recursive)                     │
  │  Tree 層序                    → BFS (Queue)                         │
  │  BST 第 K 小                  → Inorder Traversal                   │
  │  Graph 最短路 (無權)          → BFS                                  │
  │  Graph 最短路 (有權)          → Dijkstra                             │
  │  任務依賴排序                 → Topological Sort                     │
  │  動態連通性                   → Union-Find                           │
  │  求最值 + 重疊子問題          → Dynamic Programming                  │
  │  列舉所有排列/組合            → Backtracking                         │
  │  局部最優 = 全域最優          → Greedy                               │
  │  Top K / 動態最值             → Heap (Priority Queue)               │
  │  前綴搜尋                     → Trie                                 │
  │  找唯一/位元操作              → Bit Manipulation (XOR)              │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │                 常見複雜度速記                                        │
  ├─────────────────────────────────────────────────────────────────────┤
  │  O(1)       → HashMap lookup, Bit operation                        │
  │  O(log n)   → Binary Search                                        │
  │  O(n)       → Two Pointers, Sliding Window, HashMap, 一次遍歷      │
  │  O(n log n) → Sorting, Heap (n 個元素各 log n)                     │
  │  O(n²)      → 雙重迴圈, 暴力配對                                   │
  │  O(2^n)     → Backtracking (子集), 未優化的遞迴                    │
  │  O(n!)      → Backtracking (排列)                                  │
  └─────────────────────────────────────────────────────────────────────┘
"""
    print(cheat)


# =============================================================================
# Section 7: Interactive Demo — Decision Tree 使用範例
# =============================================================================

def demo_decision_tree():
    """用幾個範例展示 Decision Tree 的使用方式。"""
    print_title("Decision Tree 使用範例 (Demo)")

    demos = [
        {
            "problem": "Two Sum: 給一個 array 和 target，找兩個數加起來 = target",
            "params": {"data_structure": "array", "keywords": ["pair", "two sum"]},
        },
        {
            "problem": "Longest Substring Without Repeating Characters",
            "params": {"data_structure": "string", "keywords": ["substring", "longest"]},
        },
        {
            "problem": "Binary Tree Level Order Traversal",
            "params": {"data_structure": "tree", "keywords": ["level order", "bfs"]},
        },
        {
            "problem": "Course Schedule: 判斷能否修完所有課（有先修課限制）",
            "params": {"data_structure": "graph", "keywords": ["dependency", "cycle"], "graph_type": "dag"},
        },
        {
            "problem": "Coin Change: 用最少硬幣湊出目標金額",
            "params": {"data_structure": "array", "keywords": ["minimum"], "optimization_type": "min"},
        },
        {
            "problem": "Subsets: 列舉所有子集",
            "params": {"data_structure": "array", "keywords": ["subset"], "need_all_solutions": True},
        },
        {
            "problem": "Kth Largest Element in an Array",
            "params": {"data_structure": "array", "keywords": ["k-th", "top k"]},
        },
        {
            "problem": "Number of Islands: 在 grid 裡找島嶼數量",
            "params": {"data_structure": "graph", "keywords": ["island", "grid", "connected"]},
        },
    ]

    for i, demo in enumerate(demos, 1):
        print(f"  範例 {i}: {demo['problem']}")
        result = decide_algorithm(**demo["params"])
        print(f"  建議演算法:")
        for r in result:
            print(f"    ▸ {r}")
        print()


# =============================================================================
# Main
# =============================================================================

def main():
    """主程式：印出完整的 LeetCode 解題框架。"""

    print()
    print_separator("*")
    print("  LeetCode 解題框架總覽 — Master Decision Tree")
    print("  適用對象：準備 Google / NVIDIA 面試的初學者")
    print("  執行方式：python 00_解題框架_總覽.py")
    print_separator("*")

    # 1. 一頁速查表（最精華，放最前面）
    print_quick_cheatsheet()

    # 2. Decision Tree 視覺化
    print_decision_tree_visual()

    # 3. 關鍵字 → 算法 對照表
    print_keyword_table()

    # 4. 複雜度速查表
    print_complexity_table()

    # 5. 常見 Pattern 辨識
    print_pattern_list()

    # 6. 完整算法分類表
    print_algorithm_catalog()

    # 7. Decision Tree 使用範例
    demo_decision_tree()

    # 8. 面試小提醒
    print_interview_tips()

    # 結尾
    print_separator("=")
    print("  框架總覽結束。建議把這份輸出印出來，解題時隨時對照！")
    print("  接下來請按順序學習 01 ~ 18 各主題的 .py 檔案。")
    print_separator("=")
    print()


if __name__ == "__main__":
    main()
