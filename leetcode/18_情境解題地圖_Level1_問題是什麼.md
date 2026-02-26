# 情境解題地圖 Level 1：問題是什麼？

> **核心理念**：不要問「這題該用什麼算法」，要問「這題到底在問什麼」。
> 當你識別出**問題情境**，算法就自動浮現。
> **本檔案不解釋算法原理**（參見 01–17 教學檔），只做 **情境 → 算法** 的映射。

---

## 第一層：宏觀問題分類 — 八大問題本質

每一道 LeetCode 題目，剝掉包裝之後，本質上只在問八件事：

| 代號 | 本質 | 一句話 | 英文對應 |
|------|------|--------|----------|
| **找** | Find | 找到某個特定東西 | Find / Search / Locate |
| **數** | Count | 數有幾個、幾種 | Count / Number of |
| **最** | Optimize | 求最大/最小/最長/最短 | Maximum / Minimum / Longest / Shortest |
| **排** | Arrange | 排列、排序、重組 | Sort / Arrange / Reorder |
| **建** | Build | 建造、轉換資料結構 | Construct / Convert / Design |
| **驗** | Validate | 驗證某個性質是否成立 | Valid / Check / Is... / Can... |
| **列** | Enumerate | 列出所有可能 | All / Generate / List |
| **連** | Connect | 連通性、關係、分群 | Connected / Union / Components |

> **使用方式**：看到題目 → 判斷屬於哪個宏觀類 → 進入該類的微觀情境表 → 鎖定算法

---

## 一、找 (Find) — 找到某個東西

> **特徵詞**：find, search, locate, return the element, look up, get

### 情境 1.1：在未排序集合中找特定元素或配對

```
📋 看到什麼：unsorted array + 「find two numbers that sum to target」
🎯 本質問題：快速查找某值是否存在（O(1) lookup）
🔧 算法家族：HashMap (One-pass / Two-pass)
💡 關鍵信號：unsorted + target + pair/triplet
📌 代表：LC 1 Two Sum, LC 217 Contains Duplicate
⚡ 為什麼不用暴力？HashMap 把 O(n²) 變 O(n)
```

### 情境 1.2：在已排序集合中找特定元素

```
📋 看到什麼：sorted array + 「find target」/ 「search for」
🎯 本質問題：有序 → 可以每次排除一半
🔧 算法家族：Binary Search
💡 關鍵信號：sorted + search + O(log n) 要求
📌 代表：LC 704 Binary Search, LC 35 Search Insert Position
⚡ 經典 left, right, mid 框架，注意邊界條件
```

### 情境 1.3：在已排序集合中找一對/多個元素滿足條件

```
📋 看到什麼：sorted array + 「find pair / two numbers that...」
🎯 本質問題：在有序空間中搜尋，每次可以排除一端
🔧 算法家族：對向雙指針 (Two Pointers - Opposite Direction)
💡 關鍵信號：sorted + pair + target sum/difference
📌 代表：LC 167 Two Sum II, LC 15 3Sum
⚡ 為什麼不用 HashMap？sorted 提供了更好的結構，雙指針 O(1) space
```

### 情境 1.4：在旋轉/變形的排序資料中找元素

```
📋 看到什麼：「rotated sorted array」+ search
🎯 本質問題：局部有序 → 修改版 binary search
🔧 算法家族：Modified Binary Search
💡 關鍵信號：rotated + sorted + search
📌 代表：LC 33 Search in Rotated Sorted Array, LC 153 Find Minimum in Rotated Sorted Array
⚡ 關鍵：先判斷哪半邊是有序的，再決定往哪邊走
```

### 情境 1.5：在矩陣中找元素

```
📋 看到什麼：2D matrix + search / find target
🎯 本質問題：將 2D 映射到 1D 或利用排序性質
🔧 算法家族：Binary Search (flatten) 或 Staircase Search (右上角出發)
💡 關鍵信號：matrix + sorted rows/columns + search
📌 代表：LC 74 Search a 2D Matrix, LC 240 Search a 2D Matrix II
⚡ 74 用 flatten + binary search；240 用右上角 staircase
```

### 情境 1.6：找連續子陣列/子字串中滿足條件的區段

```
📋 看到什麼：「substring」/「subarray」+ 某種條件（不重複、包含所有字元...）
🎯 本質問題：維護一個動態視窗，擴展右端、收縮左端
🔧 算法家族：Sliding Window
💡 關鍵信號：contiguous / substring / subarray + 條件限制
📌 代表：LC 3 Longest Substring Without Repeating, LC 76 Minimum Window Substring
⚡ 可變長度視窗：右指針擴展，左指針收縮直到條件不滿足
```

### 情境 1.7：找樹中的某個節點或路徑

```
📋 看到什麼：binary tree + find node / path / ancestor
🎯 本質問題：遍歷樹結構，遞迴探索
🔧 算法家族：DFS (preorder/inorder/postorder) 或 BFS
💡 關鍵信號：tree + path + node + sum
📌 代表：LC 112 Path Sum, LC 236 Lowest Common Ancestor
⚡ 找路徑用 DFS；找最近的用 BFS；找祖先用 postorder DFS
```

### 情境 1.8：找圖中兩點之間的路徑

```
📋 看到什麼：graph + path from A to B / reachable
🎯 本質問題：圖的遍歷，找是否可達或最短路
🔧 算法家族：BFS (最短路) 或 DFS (任意路徑)
💡 關鍵信號：graph + path + shortest + connected
📌 代表：LC 127 Word Ladder, LC 797 All Paths From Source to Target
⚡ 要最短路用 BFS；要所有路徑用 DFS
```

### 情境 1.9：找第 K 大 / 第 K 小的元素

```
📋 看到什麼：「kth largest」/「kth smallest」
🎯 本質問題：部分排序，只需要知道第 K 個
🔧 算法家族：Min/Max Heap (size K) 或 QuickSelect
💡 關鍵信號：kth + largest/smallest/frequent
📌 代表：LC 215 Kth Largest Element, LC 347 Top K Frequent Elements
⚡ Heap: O(n log k)；QuickSelect: 平均 O(n)
```

### 情境 1.10：找下一個更大/更小的元素

```
📋 看到什麼：「next greater element」/「daily temperatures」
🎯 本質問題：對每個元素，找右邊第一個比它大/小的
🔧 算法家族：Monotonic Stack（單調遞減棧找 next greater）
💡 關鍵信號：next greater / next smaller / days until warmer
📌 代表：LC 496 Next Greater Element I, LC 739 Daily Temperatures
⚡ 從右往左掃，維護遞減棧
```

### 情境 1.11：找重複元素（陣列值當索引）

```
📋 看到什麼：n+1 numbers in range [1, n] + find duplicate + O(1) space
🎯 本質問題：值域 = 索引域 → 可以當成鏈表找環
🔧 算法家族：Floyd's Cycle Detection（快慢指針）
💡 關鍵信號：array as linked list + duplicate + constant space
📌 代表：LC 287 Find the Duplicate Number
⚡ 不能排序、不能用額外空間 → Floyd's
```

### 情境 1.12：找缺失/唯一的元素

```
📋 看到什麼：「missing number」/「single number」/ 所有數都出現兩次只有一個出現一次
🎯 本質問題：利用數學性質或位運算消去配對
🔧 算法家族：XOR (Bit Manipulation) 或 Math (等差和)
💡 關鍵信號：missing + range [0, n] / single + appears once
📌 代表：LC 268 Missing Number, LC 136 Single Number, LC 41 First Missing Positive
⚡ XOR: a ⊕ a = 0；Math: expected sum - actual sum
```

### 情境 1.13：找所有符合前綴的字串

```
📋 看到什麼：「prefix match」/「autocomplete」/「word search with wildcard」
🎯 本質問題：前綴樹結構，共享前綴快速查找
🔧 算法家族：Trie (Prefix Tree)
💡 關鍵信號：prefix + search + dictionary + word
📌 代表：LC 208 Implement Trie, LC 211 Design Add and Search Words
⚡ HashMap 也可以但 Trie 在前綴查詢上更高效
```

### 情境 1.14：找最低公共祖先 (LCA)

```
📋 看到什麼：binary tree + lowest common ancestor of two nodes
🎯 本質問題：後序遍歷，從下往上匯報是否找到目標
🔧 算法家族：DFS (postorder)；若是 BST 則利用大小性質
💡 關鍵信號：LCA / lowest common ancestor / tree
📌 代表：LC 236 LCA of Binary Tree, LC 235 LCA of BST
⚡ BST 版本只需比較值的大小，O(h)
```

### 情境 1.15：找鏈表環的入口

```
📋 看到什麼：linked list + detect cycle + return cycle start node
🎯 本質問題：快慢指針相遇後，重置一個到頭部同步走
🔧 算法家族：Floyd's Cycle Detection (phase 2)
💡 關鍵信號：linked list + cycle + entry point
📌 代表：LC 142 Linked List Cycle II
⚡ Phase 1: 快慢相遇；Phase 2: 頭部 + 相遇點同步走
```

### 情境 1.16：找峰值元素（局部極值）

```
📋 看到什麼：「find peak element」/ 相鄰不相等 + O(log n)
🎯 本質問題：局部上升方向必有峰值 → binary search 變形
🔧 算法家族：Binary Search (gradient ascent)
💡 關鍵信號：peak + O(log n) + adjacent elements differ
📌 代表：LC 162 Find Peak Element, LC 852 Peak Index in Mountain Array
⚡ 比較 mid 和 mid+1，往大的方向走
```

### 情境 1.17：找中位數（動態資料流）

```
📋 看到什麼：data stream + find median + addNum / findMedian
🎯 本質問題：維護兩個 heap 讓中間值隨時可取
🔧 算法家族：Two Heaps (Max-Heap + Min-Heap)
💡 關鍵信號：median + stream + dynamic insert
📌 代表：LC 295 Find Median from Data Stream
⚡ Max-heap 存小的一半，Min-heap 存大的一半
```

---

## 二、數 (Count) — 數有幾個/幾種

> **特徵詞**：count, number of, how many, total ways

### 情境 2.1：數子陣列和等於 K 的個數

```
📋 看到什麼：subarray + sum equals k + count
🎯 本質問題：prefix[j] - prefix[i] = k → 找有幾個 i
🔧 算法家族：Prefix Sum + HashMap
💡 關鍵信號：subarray sum + equals k + count
📌 代表：LC 560 Subarray Sum Equals K, LC 930 Binary Subarrays With Sum
⚡ HashMap 存 prefix sum 出現次數，一邊算一邊查
```

### 情境 2.2：數網格中從左上到右下的路徑數

```
📋 看到什麼：m × n grid + count paths + 只能往右/下走
🎯 本質問題：每格的路徑數 = 上格 + 左格
🔧 算法家族：2D DP
💡 關鍵信號：grid + paths + right/down only
📌 代表：LC 62 Unique Paths, LC 63 Unique Paths II (with obstacles)
⚡ dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### 情境 2.3：數解碼/拆分的方式數

```
📋 看到什麼：string of digits + how many ways to decode/split
🎯 本質問題：每個位置可以選取 1 位或 2 位 → 類似爬樓梯
🔧 算法家族：1D DP
💡 關鍵信號：decode ways + string + count
📌 代表：LC 91 Decode Ways, LC 139 Word Break (count variant)
⚡ dp[i] = dp[i-1] (取一位) + dp[i-2] (取兩位，若合法)
```

### 情境 2.4：數連通分量的個數

```
📋 看到什麼：graph / grid + count connected components / number of islands
🎯 本質問題：每找到一個未訪問的節點就是新的分量
🔧 算法家族：DFS / BFS / Union-Find
💡 關鍵信號：connected components + number of + islands
📌 代表：LC 200 Number of Islands, LC 323 Number of Connected Components
⚡ DFS/BFS 從每個未訪問節點出發；Union-Find 合併後數根
```

### 情境 2.5：數島嶼/封閉區域的數量

```
📋 看到什麼：grid of 0/1 + count distinct regions
🎯 本質問題：Flood fill — 找到 1 就把整個島標記已訪問
🔧 算法家族：Grid DFS / BFS
💡 關鍵信號：grid + 1s and 0s + count islands/regions
📌 代表：LC 200 Number of Islands, LC 695 Max Area of Island
⚡ 遍歷每格，遇到 1 就 DFS 把相連的都標記
```

### 情境 2.6：數視窗內的不同字元/元素數

```
📋 看到什麼：sliding window + count unique / distinct characters
🎯 本質問題：維護 window 內的 frequency map
🔧 算法家族：Sliding Window + HashMap
💡 關鍵信號：window + unique + at most K distinct
📌 代表：LC 340 Longest Substring with At Most K Distinct, LC 992 Subarrays with K Different Integers
⚡ 「恰好 K 個」= 「至多 K 個」−「至多 K-1 個」
```

### 情境 2.7：數反轉對/逆序對的數量

```
📋 看到什麼：count inversions + i < j but a[i] > a[j]
🎯 本質問題：merge sort 合併時順便計數
🔧 算法家族：Merge Sort (modified) 或 BIT/Fenwick Tree
💡 關鍵信號：inversions + count pairs + i < j, a[i] > a[j]
📌 代表：LC 315 Count of Smaller Numbers After Self, LC 493 Reverse Pairs
⚡ Merge sort 合併時，左半邊元素 > 右半邊時計數
```

### 情境 2.8：數位元中 1 的個數

```
📋 看到什麼：count bits / number of 1s / hamming weight
🎯 本質問題：位運算消去最低位的 1
🔧 算法家族：Bit Manipulation (n & (n-1))
💡 關鍵信號：bits + count 1s + binary representation
📌 代表：LC 191 Number of 1 Bits, LC 338 Counting Bits
⚡ n & (n-1) 消去最低位的 1，數幾次變 0
```

### 情境 2.9：數爬樓梯/跳格子的方式數

```
📋 看到什麼：stairs + each time 1 or 2 steps + how many ways
🎯 本質問題：Fibonacci 變形
🔧 算法家族：1D DP
💡 關鍵信號：stairs / steps + ways + 1 or 2 at a time
📌 代表：LC 70 Climbing Stairs, LC 746 Min Cost Climbing Stairs
⚡ dp[i] = dp[i-1] + dp[i-2]，經典入門 DP
```

### 情境 2.10：數組合和/硬幣湊法的方式數

```
📋 看到什麼：coins + amount + how many combinations
🎯 本質問題：完全背包問題（每個硬幣可用多次）
🔧 算法家族：DP (Unbounded Knapsack)
💡 關鍵信號：coins / denominations + amount + count ways
📌 代表：LC 518 Coin Change II, LC 377 Combination Sum IV
⚡ 518 是組合（順序不重要）；377 是排列（順序重要）
```

### 情境 2.11：數字串中的回文子串數量

```
📋 看到什麼：count palindromic substrings
🎯 本質問題：以每個位置為中心向外擴展
🔧 算法家族：中心擴展法 或 DP
💡 關鍵信號：palindrome + count + substring
📌 代表：LC 647 Palindromic Substrings, LC 5 Longest Palindromic Substring
⚡ 以每個 (i, i) 和 (i, i+1) 為中心擴展
```

### 情境 2.12：數樹中符合條件的路徑數

```
📋 看到什麼：tree + count paths + path sum equals target
🎯 本質問題：DFS + Prefix Sum（樹上版本）
🔧 算法家族：DFS + HashMap (prefix sum on tree)
💡 關鍵信號：tree path + count + sum equals
📌 代表：LC 437 Path Sum III, LC 124 Binary Tree Maximum Path Sum
⚡ 把 prefix sum 技巧搬到樹上，DFS 時維護 HashMap
```

### 情境 2.13：數矩陣中的正方形/矩形數量

```
📋 看到什麼：matrix of 0/1 + count squares / maximal square
🎯 本質問題：dp[i][j] = 以 (i,j) 為右下角的最大正方形邊長
🔧 算法家族：2D DP
💡 關鍵信號：matrix + square + count / maximal
📌 代表：LC 221 Maximal Square, LC 1277 Count Square Submatrices
⚡ dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
```

---

## 三、最 (Optimize) — 最大/最小/最短/最長

> **特徵詞**：maximum, minimum, longest, shortest, largest, smallest, most, least, optimal

### 情境 3.1：最大連續子陣列和

```
📋 看到什麼：contiguous subarray + maximum sum
🎯 本質問題：每個位置二選一：繼續累加 or 從頭開始
🔧 算法家族：Kadane's Algorithm (DP 思維)
💡 關鍵信號：maximum subarray sum + contiguous
📌 代表：LC 53 Maximum Subarray, LC 918 Maximum Sum Circular Subarray
⚡ dp[i] = max(nums[i], dp[i-1] + nums[i])
```

### 情境 3.2：最大路徑和（樹）

```
📋 看到什麼：binary tree + maximum path sum (path 不一定過 root)
🎯 本質問題：後序遍歷，每個節點回報「以我為端點的最長臂」
🔧 算法家族：DFS (postorder) + global max
💡 關鍵信號：tree + path sum + maximum + any node to any node
📌 代表：LC 124 Binary Tree Maximum Path Sum
⚡ 每個節點：max_path = node.val + max(0, left) + max(0, right)
```

### 情境 3.3：最小視窗包含所有目標字元

```
📋 看到什麼：string + minimum window containing all characters of T
🎯 本質問題：可變長度 sliding window，擴展直到滿足 → 收縮到不滿足
🔧 算法家族：Sliding Window (variable length)
💡 關鍵信號：minimum window + contains all + substring
📌 代表：LC 76 Minimum Window Substring
⚡ 用 need/have counter，擴展右端直到 have == need，再縮左端
```

### 情境 3.4：最短路（無權圖）

```
📋 看到什麼：graph + shortest path + unweighted (or all edges = 1)
🎯 本質問題：BFS 天然找最短路（每層距離 +1）
🔧 算法家族：BFS
💡 關鍵信號：shortest path + unweighted + fewest steps / moves
📌 代表：LC 127 Word Ladder, LC 994 Rotting Oranges, LC 1091 Shortest Path in Binary Matrix
⚡ BFS 的層數就是最短距離
```

### 情境 3.5：最短路（加權圖，非負權）

```
📋 看到什麼：weighted graph + shortest path + non-negative weights
🎯 本質問題：貪心擴展最近未訪問節點
🔧 算法家族：Dijkstra's Algorithm (Min-Heap)
💡 關鍵信號：weighted + shortest path + non-negative
📌 代表：LC 743 Network Delay Time, LC 787 Cheapest Flights Within K Stops
⚡ Priority queue + relaxation
```

### 情境 3.6：最少硬幣湊出金額

```
📋 看到什麼：coins + minimum number to make amount
🎯 本質問題：完全背包的最小化版本
🔧 算法家族：DP (Bottom-up)
💡 關鍵信號：minimum coins + amount + denominations
📌 代表：LC 322 Coin Change
⚡ dp[amount] = min(dp[amount - coin] + 1) for each coin
```

### 情境 3.7：最長遞增子序列 (LIS)

```
📋 看到什麼：longest increasing subsequence (不要求連續)
🎯 本質問題：DP 每個位置記錄以它結尾的 LIS 長度；或用 Patience Sort
🔧 算法家族：DP O(n²) 或 DP + Binary Search O(n log n)
💡 關鍵信號：longest increasing subsequence + not contiguous
📌 代表：LC 300 Longest Increasing Subsequence, LC 354 Russian Doll Envelopes
⚡ O(n log n)：維護 tails 陣列 + bisect
```

### 情境 3.8：最大矩形面積

```
📋 看到什麼：histogram + largest rectangle / maximal rectangle in matrix
🎯 本質問題：對每個 bar 找左右第一個更矮的 → 寬度確定
🔧 算法家族：Monotonic Stack
💡 關鍵信號：histogram + largest rectangle + area
📌 代表：LC 84 Largest Rectangle in Histogram, LC 85 Maximal Rectangle
⚡ 單調遞增棧，遇到更矮的就 pop 並計算面積
```

### 情境 3.9：最大盛水容器

```
📋 看到什麼：array of heights + maximize area = min(h[i], h[j]) × (j-i)
🎯 本質問題：短板決定水位，移動短的那邊才有可能變大
🔧 算法家族：Two Pointers (Opposite Direction)
💡 關鍵信號：container + water + maximize area + heights
📌 代表：LC 11 Container With Most Water, LC 42 Trapping Rain Water
⚡ 11 用對向雙指針；42 用單調棧或雙指針
```

### 情境 3.10：最長公共子序列 (LCS)

```
📋 看到什麼：two strings/arrays + longest common subsequence
🎯 本質問題：經典 2D DP，兩個序列的對齊問題
🔧 算法家族：2D DP
💡 關鍵信號：two sequences + common + subsequence + longest
📌 代表：LC 1143 Longest Common Subsequence, LC 72 Edit Distance
⚡ dp[i][j] = dp[i-1][j-1]+1 (match) or max(dp[i-1][j], dp[i][j-1])
```

### 情境 3.11：最大利潤（買賣股票）

```
📋 看到什麼：stock prices + maximize profit + buy/sell
🎯 本質問題：追蹤最低價，每天算「今天賣的話利潤多少」
🔧 算法家族：Greedy (one pass) 或 State Machine DP (多次交易)
💡 關鍵信號：stock + buy + sell + profit + maximum
📌 代表：LC 121 Best Time to Buy and Sell Stock, LC 122 (多次), LC 188 (k次)
⚡ 一次交易用 Greedy；k 次交易用 DP
```

### 情境 3.12：最長回文子串

```
📋 看到什麼：string + longest palindromic substring
🎯 本質問題：每個位置當中心向外擴展
🔧 算法家族：中心擴展 O(n²) 或 Manacher O(n)
💡 關鍵信號：palindrome + longest + substring (contiguous)
📌 代表：LC 5 Longest Palindromic Substring, LC 516 Longest Palindromic Subsequence
⚡ 5 是 substring (中心擴展)；516 是 subsequence (DP)
```

### 情境 3.13：背包問題 — 容量限制下的最大價值

```
📋 看到什麼：items with weight/value + capacity + maximize
🎯 本質問題：每個物品選或不選 → 0/1 Knapsack
🔧 算法家族：DP (0/1 Knapsack 或 Unbounded Knapsack)
💡 關鍵信號：capacity + weight + value + maximize / can achieve
📌 代表：LC 416 Partition Equal Subset Sum, LC 494 Target Sum
⚡ 0/1: dp[j] = max(dp[j], dp[j-w]+v)；完全: 內循環正向
```

### 情境 3.14：最少操作次數（字串轉換）

```
📋 看到什麼：transform string A to B + minimum operations (insert/delete/replace)
🎯 本質問題：經典 Edit Distance — 2D DP
🔧 算法家族：2D DP
💡 關鍵信號：edit distance + minimum operations + insert/delete/replace
📌 代表：LC 72 Edit Distance, LC 583 Delete Operation for Two Strings
⚡ dp[i][j] = 考慮 word1[0..i-1] 和 word2[0..j-1] 的最少操作
```

### 情境 3.15：最大 subarray product

```
📋 看到什麼：contiguous subarray + maximum product
🎯 本質問題：負數翻轉 → 同時追蹤最大和最小
🔧 算法家族：DP (track max and min simultaneously)
💡 關鍵信號：maximum product + subarray + 可能有負數
📌 代表：LC 152 Maximum Product Subarray
⚡ max_so_far, min_so_far 每步更新（負數會讓 min 變 max）
```

### 情境 3.16：最大正方形（矩陣中）

```
📋 看到什麼：matrix of 0/1 + largest square containing only 1s
🎯 本質問題：dp[i][j] = 以 (i,j) 為右下角的最大正方形邊長
🔧 算法家族：2D DP
💡 關鍵信號：matrix + largest square + all 1s
📌 代表：LC 221 Maximal Square
⚡ dp[i][j] = min(左, 上, 左上) + 1
```

---

## 四、排 (Arrange) — 排列/排序/重組

> **特徵詞**：sort, reorder, arrange, merge, partition, next, reorganize

### 情境 4.1：特殊排序（只有 0/1/2 或有限類別）

```
📋 看到什麼：sort array of 0s, 1s, 2s / sort colors
🎯 本質問題：有限類別 → counting sort 或 Dutch National Flag
🔧 算法家族：Dutch National Flag (三指針) 或 Counting Sort
💡 關鍵信號：sort + only 2-3 distinct values + in-place
📌 代表：LC 75 Sort Colors
⚡ 三指針：low, mid, high 各管一個顏色
```

### 情境 4.2：合併多個已排序的序列

```
📋 看到什麼：merge k sorted lists/arrays
🎯 本質問題：每次取最小的那個 → Min-Heap
🔧 算法家族：Min-Heap (Priority Queue) 或 Divide-and-Conquer Merge
💡 關鍵信號：merge + k sorted + lists/arrays
📌 代表：LC 23 Merge k Sorted Lists, LC 88 Merge Sorted Array
⚡ k=2 用雙指針；k>2 用 Heap 或兩兩合併
```

### 情境 4.3：重組字串/陣列使相鄰不重複

```
📋 看到什麼：reorganize string so no adjacent are same
🎯 本質問題：每次放頻率最高的（但不能和上一個相同）
🔧 算法家族：Max-Heap + Greedy
💡 關鍵信號：reorganize + no adjacent duplicates + rearrange
📌 代表：LC 767 Reorganize String, LC 621 Task Scheduler
⚡ 每次從 heap 取最大頻率，放完後放回（cooldown 機制）
```

### 情境 4.4：拓撲排序（依賴關係排序）

```
📋 看到什麼：prerequisites + order of courses / tasks
🎯 本質問題：DAG 的線性排序 → BFS (Kahn's) 或 DFS
🔧 算法家族：Topological Sort (Kahn's BFS with in-degree)
💡 關鍵信號：prerequisites + order + dependency + DAG
📌 代表：LC 207 Course Schedule, LC 210 Course Schedule II
⚡ 入度為 0 的先處理，處理後鄰居入度 -1
```

### 情境 4.5：下一個排列

```
📋 看到什麼：next permutation / next greater number with same digits
🎯 本質問題：固定的數學模式 — 從右找下降點
🔧 算法家族：Math Pattern (specific algorithm)
💡 關鍵信號：next permutation + lexicographically + next greater
📌 代表：LC 31 Next Permutation, LC 556 Next Greater Element III
⚡ ① 從右找第一個下降 a[i] < a[i+1] ② 找右邊最小的大於 a[i] ③ 交換 ④ 反轉 i+1 之後
```

### 情境 4.6：按照特定規則排序（自定義 comparator）

```
📋 看到什麼：sort intervals by start time / sort by custom rule
🎯 本質問題：自定義比較函數 + 排序後處理
🔧 算法家族：Sort + Greedy / Sort + Stack
💡 關鍵信號：intervals + sort + merge / custom ordering
📌 代表：LC 56 Merge Intervals, LC 179 Largest Number
⚡ 排序是前置操作，排完後用 greedy 或 stack 處理
```

### 情境 4.7：原地分割（partition）

```
📋 看到什麼：move all X to left, Y to right + in-place
🎯 本質問題：同向雙指針或對向雙指針分割
🔧 算法家族：Two Pointers (same direction / opposite)
💡 關鍵信號：partition + in-place + move zeros / odd-even
📌 代表：LC 283 Move Zeroes, LC 905 Sort Array By Parity
⚡ 一個指針掃描，一個指針記錄放置位置
```

### 情境 4.8：合併區間

```
📋 看到什麼：list of intervals + merge overlapping
🎯 本質問題：按起點排序後，逐一判斷是否重疊
🔧 算法家族：Sort + Greedy (Linear Scan)
💡 關鍵信號：intervals + merge + overlapping
📌 代表：LC 56 Merge Intervals, LC 57 Insert Interval
⚡ 排序後：if current.start <= last.end → merge
```

---

## 五、建 (Build) — 建造/轉換資料結構

> **特徵詞**：construct, build, convert, flatten, serialize, deserialize, design, implement

### 情境 5.1：從遍歷序列建構二叉樹

```
📋 看到什麼：construct tree from preorder + inorder / postorder + inorder
🎯 本質問題：preorder 第一個是 root → inorder 中找到 root → 左右分割遞迴
🔧 算法家族：DFS (Divide and Conquer) + HashMap
💡 關鍵信號：construct + binary tree + preorder/inorder/postorder
📌 代表：LC 105 from Preorder and Inorder, LC 106 from Inorder and Postorder
⚡ HashMap 存 inorder 中每個值的 index，O(1) 查找 root 位置
```

### 情境 5.2：展平樹結構為鏈表/陣列

```
📋 看到什麼：flatten binary tree to linked list / nested list
🎯 本質問題：DFS 前序遍歷 → 依序連結
🔧 算法家族：DFS (preorder, reverse-postorder) 或 Morris Traversal
💡 關鍵信號：flatten + tree + linked list + in-place
📌 代表：LC 114 Flatten Binary Tree to Linked List, LC 341 Flatten Nested List Iterator
⚡ 反向後序：right → left → root，每次接到 prev
```

### 情境 5.3：複製/克隆圖結構

```
📋 看到什麼：deep copy / clone graph or linked list with random pointer
🎯 本質問題：DFS/BFS + HashMap 記錄 old → new 的映射
🔧 算法家族：DFS + HashMap 或 BFS + HashMap
💡 關鍵信號：clone + deep copy + graph / random pointer
📌 代表：LC 133 Clone Graph, LC 138 Copy List with Random Pointer
⚡ HashMap: {old_node: new_node} 避免重複克隆
```

### 情境 5.4：序列化/反序列化

```
📋 看到什麼：serialize tree/graph to string + deserialize back
🎯 本質問題：BFS 或 preorder DFS 轉字串，null 用特殊符號
🔧 算法家族：BFS (level-order) 或 DFS (preorder)
💡 關鍵信號：serialize + deserialize + string ↔ tree
📌 代表：LC 297 Serialize and Deserialize Binary Tree, LC 449 Serialize BST
⚡ Preorder + 「null」標記 → 反序列化用 queue 消費
```

### 情境 5.5：設計資料結構（LRU / LFU / Stack + Min）

```
📋 看到什麼：design a data structure with O(1) for get/put/push/getMin
🎯 本質問題：組合多個基礎結構達到 O(1)
🔧 算法家族：HashMap + Doubly Linked List (LRU) / HashMap + Stack / etc.
💡 關鍵信號：design + implement + O(1) + get + put
📌 代表：LC 146 LRU Cache, LC 155 Min Stack, LC 460 LFU Cache
⚡ LRU: HashMap (key→node) + DLL (order)；MinStack: 兩個 stack
```

### 情境 5.6：將資料結構轉換為另一種形式

```
📋 看到什麼：convert BST to sorted linked list / sorted array to BST
🎯 本質問題：利用 BST 的 inorder = sorted 性質
🔧 算法家族：DFS (inorder) 或 Divide and Conquer
💡 關鍵信號：convert + BST + sorted + linked list / array
📌 代表：LC 108 Convert Sorted Array to BST, LC 426 Convert BST to Sorted DLL
⚡ 108: 取中間為 root → 遞迴左右
```

### 情境 5.7：建構字串/數值的表達式求值器

```
📋 看到什麼：evaluate expression / basic calculator + parentheses
🎯 本質問題：遇到 '(' 壓棧，遇到 ')' 彈出並計算
🔧 算法家族：Stack (recursive descent)
💡 關鍵信號：evaluate + expression + calculator + parentheses + operators
📌 代表：LC 224 Basic Calculator, LC 227 Basic Calculator II
⚡ 用 stack 處理優先級和括號
```

### 情境 5.8：Implement Iterator / 將複雜遍歷封裝

```
📋 看到什麼：implement next() / hasNext() for tree / nested list
🎯 本質問題：用 stack 模擬遞迴遍歷的暫停和恢復
🔧 算法家族：Stack-based Iterator
💡 關鍵信號：implement + iterator + next + hasNext
📌 代表：LC 173 BST Iterator, LC 284 Peeking Iterator, LC 341 Flatten Nested List
⚡ Stack 存右邊的節點，每次 next() pop 出來並推入左邊
```

---

## 六、驗 (Validate) — 驗證/檢查性質

> **特徵詞**：valid, is..., can..., check, verify, determine if

### 情境 6.1：驗證括號是否合法

```
📋 看到什麼：string of brackets + valid / balanced
🎯 本質問題：左括號壓棧，右括號彈棧匹配
🔧 算法家族：Stack
💡 關鍵信號：parentheses + valid + balanced + brackets
📌 代表：LC 20 Valid Parentheses, LC 32 Longest Valid Parentheses
⚡ 遇到左括號 push，右括號 pop 並檢查匹配
```

### 情境 6.2：驗證是否為合法 BST

```
📋 看到什麼：binary tree + is valid BST
🎯 本質問題：每個節點必須在 (min, max) 範圍內
🔧 算法家族：DFS with valid range 或 Inorder 檢查遞增
💡 關鍵信號：valid BST + binary search tree
📌 代表：LC 98 Validate Binary Search Tree
⚡ DFS(node, min_val, max_val)：左走更新 max，右走更新 min
```

### 情境 6.3：驗證是否為回文

```
📋 看到什麼：palindrome + string / number / linked list
🎯 本質問題：兩端往中間比較是否對稱
🔧 算法家族：Two Pointers (Opposite Direction)
💡 關鍵信號：palindrome + check + valid
📌 代表：LC 125 Valid Palindrome, LC 234 Palindrome Linked List
⚡ 字串用雙指針；鏈表用快慢找中 + 反轉後半段
```

### 情境 6.4：判斷能否到達終點

```
📋 看到什麼：array of jump lengths + can reach last index
🎯 本質問題：Greedy — 追蹤能到達的最遠位置
🔧 算法家族：Greedy 或 DP
💡 關鍵信號：jump + reach + can / possible
📌 代表：LC 55 Jump Game, LC 45 Jump Game II
⚡ 55: max_reach = max(max_reach, i + nums[i])；45: BFS 層次
```

### 情境 6.5：圖中是否有環

```
📋 看到什麼：directed/undirected graph + detect cycle
🎯 本質問題：DFS 三色標記（白/灰/黑）或 Union-Find
🔧 算法家族：DFS (coloring) / Topological Sort (if DAG) / Union-Find
💡 關鍵信號：cycle + detect + graph + directed/undirected
📌 代表：LC 207 Course Schedule, LC 261 Graph Valid Tree
⚡ 有向圖：DFS 灰色遇灰色 = 環；無向圖：Union-Find
```

### 情境 6.6：圖是否為二分圖

```
📋 看到什麼：graph + bipartite + two-colorable
🎯 本質問題：BFS/DFS 染色，鄰居必須不同色
🔧 算法家族：BFS / DFS Coloring
💡 關鍵信號：bipartite + two colors + graph coloring
📌 代表：LC 785 Is Graph Bipartite
⚡ BFS 染色：當前紅 → 鄰居藍；遇到同色 = 非二分
```

### 情境 6.7：判斷字串能否被字典分割

```
📋 看到什麼：string + dictionary + can be segmented into words
🎯 本質問題：dp[i] = 前 i 個字元能否被分割
🔧 算法家族：DP (1D) 或 BFS/DFS + Memo
💡 關鍵信號：word break + dictionary + segment
📌 代表：LC 139 Word Break
⚡ dp[i] = any(dp[j] and s[j:i] in dict) for j < i
```

### 情境 6.8：驗證序列是否為合法的前序/後序遍歷

```
📋 看到什麼：verify preorder/postorder sequence of BST
🎯 本質問題：用 stack 模擬遍歷過程
🔧 算法家族：Stack 或 Recursion
💡 關鍵信號：verify + preorder/postorder + BST
📌 代表：LC 255 Verify Preorder Sequence in BST, LC 946 Validate Stack Sequences
⚡ 單調遞減棧 + 追蹤下界
```

### 情境 6.9：判斷兩個字串是否同構 / 異位詞

```
📋 看到什麼：isomorphic + anagram + pattern matching
🎯 本質問題：字元映射是否一致 / 字元頻率是否相同
🔧 算法家族：HashMap (frequency count / bijection)
💡 關鍵信號：isomorphic + anagram + same frequency + pattern
📌 代表：LC 242 Valid Anagram, LC 205 Isomorphic Strings, LC 290 Word Pattern
⚡ Anagram: 頻率表相同；Isomorphic: 雙向映射
```

### 情境 6.10：判斷子樹/子結構關係

```
📋 看到什麼：is subtree / is same tree / symmetric tree
🎯 本質問題：遞迴比較結構和值
🔧 算法家族：DFS (recursive comparison)
💡 關鍵信號：subtree + same tree + symmetric + mirror
📌 代表：LC 100 Same Tree, LC 101 Symmetric Tree, LC 572 Subtree of Another Tree
⚡ isSame(p, q) → p.val == q.val and isSame(left) and isSame(right)
```

---

## 七、列 (Enumerate) — 列出所有可能

> **特徵詞**：all, generate, list, enumerate, every possible, combinations, permutations, subsets

### 情境 7.1：列出所有子集

```
📋 看到什麼：return all subsets / power set
🎯 本質問題：每個元素「選」或「不選」→ 二叉決策樹
🔧 算法家族：Backtracking (include/exclude at each step)
💡 關鍵信號：all subsets + power set
📌 代表：LC 78 Subsets, LC 90 Subsets II (with duplicates)
⚡ 有重複時：先排序，跳過相同元素避免重複
```

### 情境 7.2：列出所有排列

```
📋 看到什麼：return all permutations
🎯 本質問題：每個位置從「剩餘可用」中選一個
🔧 算法家族：Backtracking + used[] 陣列
💡 關鍵信號：all permutations + arrange all elements
📌 代表：LC 46 Permutations, LC 47 Permutations II (with duplicates)
⚡ used[] 記錄誰已經用過；有重複時 sort + 跳過
```

### 情境 7.3：列出所有組合（選 k 個）

```
📋 看到什麼：all combinations of k elements / combination sum
🎯 本質問題：Backtracking + start index 避免重複選
🔧 算法家族：Backtracking + start index
💡 關鍵信號：combinations + choose k + combination sum
📌 代表：LC 77 Combinations, LC 39 Combination Sum, LC 40 Combination Sum II
⚡ 39: 可重複用 → start 不動；40: 不可重複 → start+1 + 跳重複
```

### 情境 7.4：生成所有合法括號

```
📋 看到什麼：generate all valid parentheses with n pairs
🎯 本質問題：Backtracking + 約束：open < n 可加 '('，close < open 可加 ')'
🔧 算法家族：Backtracking with constraints
💡 關鍵信號：generate parentheses + n pairs + all valid
📌 代表：LC 22 Generate Parentheses
⚡ 兩個計數器 open/close 控制合法性
```

### 情境 7.5：列出圖中所有路徑

```
📋 看到什麼：all paths from source to target in DAG
🎯 本質問題：DFS + 路徑記錄 + 回溯
🔧 算法家族：DFS + Backtracking
💡 關鍵信號：all paths + source to target + DAG
📌 代表：LC 797 All Paths From Source to Target
⚡ DAG 不需要 visited（無環保證終止）
```

### 情境 7.6：N-Queens / Sudoku Solver

```
📋 看到什麼：place N queens / solve sudoku + no conflicts
🎯 本質問題：Backtracking + 多維約束檢查
🔧 算法家族：Backtracking + Constraint Checking
💡 關鍵信號：N-Queens + sudoku + place + no attack / conflict
📌 代表：LC 51 N-Queens, LC 37 Sudoku Solver
⚡ 用 set 記錄被佔用的列/對角線，O(1) 檢查衝突
```

### 情境 7.7：字串的所有分割方式

```
📋 看到什麼：partition string into palindromes / valid IPs / sentences
🎯 本質問題：Backtracking 切割 — 每個位置選擇切多長
🔧 算法家族：Backtracking (partition)
💡 關鍵信號：partition + all ways + palindrome / valid parts
📌 代表：LC 131 Palindrome Partitioning, LC 93 Restore IP Addresses
⚡ 從 start 開始，嘗試切 1/2/3/... 長度，驗證後遞迴
```

### 情境 7.8：所有可能的表達式結果

```
📋 看到什麼：add operators / different ways to add parentheses
🎯 本質問題：分治 — 以每個運算符為分割點
🔧 算法家族：Divide and Conquer / Backtracking
💡 關鍵信號：different ways + expressions + operators + all results
📌 代表：LC 241 Different Ways to Add Parentheses, LC 282 Expression Add Operators
⚡ 241: 遇到 op → 左右分治；282: backtracking + 大數處理
```

### 情境 7.9：字母組合（電話鍵盤）

```
📋 看到什麼：phone number + letter combinations
🎯 本質問題：每個數字對應幾個字母 → 多路分支 backtracking
🔧 算法家族：Backtracking (multi-way branching)
💡 關鍵信號：phone + letter combinations + digits
📌 代表：LC 17 Letter Combinations of a Phone Number
⚡ 每個 digit → 3-4 個選擇，遞迴到下一個 digit
```

### 情境 7.10：列出所有單詞搜索路徑（矩陣）

```
📋 看到什麼：board of characters + find all words from dictionary
🎯 本質問題：Trie 存字典 + DFS backtracking 在 board 上搜
🔧 算法家族：Trie + DFS Backtracking
💡 關鍵信號：word search + board + dictionary + find all
📌 代表：LC 79 Word Search, LC 212 Word Search II
⚡ 79: 純 DFS backtracking；212: Trie 優化多詞搜索
```

---

## 八、連 (Connect) — 連通性/關係/分群

> **特徵詞**：connected, union, component, group, cluster, reach, redundant, spanning

### 情境 8.1：判斷兩點是否連通

```
📋 看到什麼：are nodes A and B connected? / same component?
🎯 本質問題：動態連通性查詢
🔧 算法家族：Union-Find (最優) 或 BFS/DFS
💡 關鍵信號：connected + query + dynamic + union
📌 代表：LC 547 Number of Provinces, LC 684 Redundant Connection
⚡ Union-Find 的 find(a) == find(b) 即同一連通分量
```

### 情境 8.2：數連通分量的數量

```
📋 看到什麼：number of connected components / provinces / islands
🎯 本質問題：遍歷所有節點，每個新起點就是新分量
🔧 算法家族：Union-Find / DFS / BFS
💡 關鍵信號：number of + components / islands / groups
📌 代表：LC 200 Number of Islands, LC 323 Number of Connected Components, LC 547 Provinces
⚡ Union-Find: 最終有幾個不同的 root = 幾個分量
```

### 情境 8.3：判斷課程是否能全部修完（環偵測 + 排序）

```
📋 看到什麼：courses + prerequisites + can finish all?
🎯 本質問題：DAG 判定 — 有環就不行
🔧 算法家族：Topological Sort (Kahn's BFS)
💡 關鍵信號：prerequisites + can finish + course schedule + order
📌 代表：LC 207 Course Schedule, LC 210 Course Schedule II
⚡ 如果排完的節點數 < 總數 → 有環 → 無法完成
```

### 情境 8.4：找多餘的邊（使圖變成樹）

```
📋 看到什麼：graph + redundant edge + remove to make tree
🎯 本質問題：加邊時若兩端已連通 → 該邊多餘
🔧 算法家族：Union-Find
💡 關鍵信號：redundant connection + tree + extra edge
📌 代表：LC 684 Redundant Connection, LC 685 Redundant Connection II
⚡ 依序加邊，find(u) == find(v) 時該邊就是答案
```

### 情境 8.5：最小生成樹

```
📋 看到什麼：connect all points/cities + minimum cost
🎯 本質問題：所有點連通且總權最小
🔧 算法家族：Kruskal's (Sort edges + Union-Find) 或 Prim's (Min-Heap)
💡 關鍵信號：minimum spanning tree + connect all + minimum cost
📌 代表：LC 1584 Min Cost to Connect All Points, LC 1135 Connecting Cities
⚡ Kruskal: 邊排序後 Union-Find 依序加邊；Prim: Min-Heap BFS
```

### 情境 8.6：帳戶合併 / 等價類分群

```
📋 看到什麼：accounts with shared emails → merge
🎯 本質問題：共享元素的集合要合併 → Union-Find
🔧 算法家族：Union-Find + HashMap
💡 關鍵信號：merge accounts + shared + group by equivalence
📌 代表：LC 721 Accounts Merge, LC 399 Evaluate Division
⚡ 每個 email 指向一個 owner → union 相同 owner 的 email
```

### 情境 8.7：圖是否為有效的樹

```
📋 看到什麼：n nodes + edges + is valid tree?
🎯 本質問題：無環 + 連通 + 邊數 = n-1
🔧 算法家族：Union-Find 或 DFS
💡 關鍵信號：valid tree + n nodes + n-1 edges + no cycle + connected
📌 代表：LC 261 Graph Valid Tree
⚡ 邊數 = n-1 且 Union-Find 加邊不產生環
```

### 情境 8.8：被包圍的區域 / 邊界連通

```
📋 看到什麼：board + capture surrounded regions (not connected to border)
🎯 本質問題：從邊界出發 DFS/BFS 標記，剩下的就是被包圍的
🔧 算法家族：DFS/BFS from boundary 或 Union-Find
💡 關鍵信號：surrounded regions + border + capture + flip
📌 代表：LC 130 Surrounded Regions, LC 1020 Number of Enclaves
⚡ 反向思維：先標記與邊界連通的，剩下的翻轉
```

### 情境 8.9：判斷字串轉換關係（圖建模）

```
📋 看到什麼：word transformation + change one letter at a time
🎯 本質問題：每個單詞是節點，差一個字母的連邊 → BFS 最短路
🔧 算法家族：BFS + HashMap (wildcard pattern)
💡 關鍵信號：word ladder + transformation + one change + shortest
📌 代表：LC 127 Word Ladder, LC 433 Minimum Genetic Mutation
⚡ 用 h*t 這種 wildcard pattern 建鄰接表
```

### 情境 8.10：網路延遲 / 訊息傳播

```
📋 看到什麼：network + time to reach all nodes + signal
🎯 本質問題：從一個源出發的最短路（到所有點）→ 答案是最大的最短路
🔧 算法家族：Dijkstra's Algorithm
💡 關鍵信號：network delay + signal + reach all + time
📌 代表：LC 743 Network Delay Time
⚡ Dijkstra 找到所有最短路，取 max
```

---

## 跨類型進階情境

> 有些題目橫跨多個類別，或偽裝成一個類別但本質是另一個。

### 情境 X.1：接雨水 (Trapping Rain Water)

```
📋 看到什麼：elevation map + how much water can be trapped
🎯 本質問題：每個位置的水量 = min(左邊最高, 右邊最高) - 自己高度
🔧 算法家族：Two Pointers 或 Monotonic Stack 或 DP (prefix max)
💡 關鍵信號：elevation + trap + water + rain
📌 代表：LC 42 Trapping Rain Water
⚡ Two Pointers: O(n) time O(1) space 最優
```

### 情境 X.2：區間調度 / 會議室問題

```
📋 看到什麼：intervals + minimum meeting rooms / max non-overlapping
🎯 本質問題：排序後用 heap 追蹤結束時間，或 Greedy 選結束早的
🔧 算法家族：Sort + Greedy / Sort + Min-Heap
💡 關鍵信號：intervals + meeting rooms + non-overlapping + minimum rooms
📌 代表：LC 252 Meeting Rooms, LC 253 Meeting Rooms II, LC 435 Non-overlapping Intervals
⚡ 252: 排序檢查重疊；253: heap 追蹤結束時間；435: greedy 選最早結束
```

### 情境 X.3：前綴和的各種偽裝

```
📋 看到什麼：subarray sum divisible by K / range sum query / product except self
🎯 本質問題：預計算累加值，區間查詢 O(1)
🔧 算法家族：Prefix Sum / Prefix Product
💡 關鍵信號：subarray sum + range + query + divisible
📌 代表：LC 303 Range Sum Query, LC 238 Product of Array Except Self, LC 974 Subarray Sums Divisible by K
⚡ 974: prefix_sum % K 相同 → 兩個位置之間的和可被 K 整除
```

### 情境 X.4：Matrix as Graph（矩陣當圖遍歷）

```
📋 看到什麼：grid + 上下左右移動 + 最短路 / 可達性
🎯 本質問題：每個格子是節點，四方向是邊
🔧 算法家族：BFS (最短) / DFS (可達) / Dijkstra (加權格)
💡 關鍵信號：grid + 4-directional + shortest path / reachable
📌 代表：LC 994 Rotting Oranges, LC 1091 Shortest Path in Binary Matrix, LC 417 Pacific Atlantic Water Flow
⚡ BFS 從多源同時出發（multi-source BFS）
```

### 情境 X.5：Interval + DP 混合

```
📋 看到什麼：burst balloons / merge stones / matrix chain multiplication
🎯 本質問題：區間 DP — dp[i][j] 代表處理區間 [i, j] 的最優解
🔧 算法家族：Interval DP
💡 關鍵信號：burst + merge + chain + cost of combining range
📌 代表：LC 312 Burst Balloons, LC 1000 Minimum Cost to Merge Stones
⚡ 枚舉分割點 k：dp[i][j] = max/min(dp[i][k] + dp[k][j] + cost)
```

### 情境 X.6：Trie + Backtracking 複合

```
📋 看到什麼：word search II — 在 grid 中找字典裡所有出現的單詞
🎯 本質問題：Trie 存字典 + DFS 在 grid 上走
🔧 算法家族：Trie + DFS Backtracking
💡 關鍵信號：board + word list + find all words
📌 代表：LC 212 Word Search II
⚡ 比逐詞搜索高效：Trie 讓多個詞共享搜索路徑
```

### 情境 X.7：Monotonic Deque — 滑動視窗最大值

```
📋 看到什麼：sliding window + maximum/minimum in each window
🎯 本質問題：Deque 維護遞減（找 max）或遞增（找 min）序列
🔧 算法家族：Monotonic Deque
💡 關鍵信號：sliding window + maximum/minimum + fixed size k
📌 代表：LC 239 Sliding Window Maximum
⚡ Deque 前端 = 當前 max；從後端移除比新元素小的
```

### 情境 X.8：State Machine DP

```
📋 看到什麼：buy/sell stock with cooldown / with fee / at most k transactions
🎯 本質問題：每天有多種狀態（持有/不持有/冷凍期）→ 狀態轉移
🔧 算法家族：DP (State Machine)
💡 關鍵信號：stock + cooldown + fee + k transactions + multiple states
📌 代表：LC 309 Best Time with Cooldown, LC 714 with Transaction Fee, LC 188 with K Transactions
⚡ 定義 hold/sold/rest 三種狀態，寫出轉移方程
```

### 情境 X.9：Bit Manipulation 進階

```
📋 看到什麼：single number appearing once while others appear 3 times / power of 2
🎯 本質問題：位元運算的數學性質
🔧 算法家族：Bit Manipulation
💡 關鍵信號：appears once + others appear K times / power of two / bit count
📌 代表：LC 137 Single Number II, LC 260 Single Number III, LC 231 Power of Two
⚡ 137: 逐位統計 mod 3；260: XOR 全部 → 分組
```

### 情境 X.10：Reservoir Sampling / 隨機抽樣

```
📋 看到什麼：random pick / linked list random node / shuffle
🎯 本質問題：無法預知總量時的等概率抽樣
🔧 算法家族：Reservoir Sampling / Fisher-Yates Shuffle
💡 關鍵信號：random + equal probability + stream + shuffle
📌 代表：LC 382 Linked List Random Node, LC 384 Shuffle an Array, LC 398 Random Pick Index
⚡ Reservoir: 第 i 個元素以 1/i 概率替換當前選擇
```

---

## 總結：情境速查表 (120+ Scenarios)

> 用法：看到題目 → 在下表中找到最接近的情境描述 → 直接套用算法

| # | 情境 | 算法 | 代表題 |
|---|------|------|--------|
| **找 (Find)** | | | |
| 1.1 | 未排序找配對/元素 | HashMap | LC 1, 217 |
| 1.2 | 已排序找元素 | Binary Search | LC 704, 35 |
| 1.3 | 已排序找配對 | Two Pointers (opposite) | LC 167, 15 |
| 1.4 | 旋轉排序找元素 | Modified Binary Search | LC 33, 153 |
| 1.5 | 矩陣找元素 | Binary Search / Staircase | LC 74, 240 |
| 1.6 | 找符合條件的連續子段 | Sliding Window | LC 3, 76 |
| 1.7 | 樹中找節點/路徑 | DFS / BFS | LC 112, 236 |
| 1.8 | 圖中找路徑 | BFS / DFS | LC 127, 797 |
| 1.9 | 找第 K 大/小 | Heap / QuickSelect | LC 215, 347 |
| 1.10 | 找下一個更大/小元素 | Monotonic Stack | LC 496, 739 |
| 1.11 | 陣列值當索引找重複 | Floyd's Cycle | LC 287 |
| 1.12 | 找缺失/唯一元素 | XOR / Math | LC 268, 136 |
| 1.13 | 前綴匹配找字串 | Trie | LC 208, 211 |
| 1.14 | 找最低公共祖先 | DFS postorder / BST | LC 236, 235 |
| 1.15 | 鏈表找環入口 | Floyd's Phase 2 | LC 142 |
| 1.16 | 找峰值 | Binary Search (gradient) | LC 162, 852 |
| 1.17 | 動態資料找中位數 | Two Heaps | LC 295 |
| **數 (Count)** | | | |
| 2.1 | 子陣列和 = K 的個數 | Prefix Sum + HashMap | LC 560 |
| 2.2 | 網格路徑數 | 2D DP | LC 62, 63 |
| 2.3 | 解碼方式數 | 1D DP | LC 91 |
| 2.4 | 連通分量數 | DFS / BFS / Union-Find | LC 200, 323 |
| 2.5 | 島嶼/區域數 | Grid DFS / BFS | LC 200, 695 |
| 2.6 | 視窗內不同元素數 | Sliding Window + HashMap | LC 340, 992 |
| 2.7 | 逆序對數 | Merge Sort / BIT | LC 315, 493 |
| 2.8 | 位元 1 的個數 | Bit Manipulation | LC 191, 338 |
| 2.9 | 爬樓梯方式數 | 1D DP (Fibonacci) | LC 70, 746 |
| 2.10 | 組合和方式數 | DP (Knapsack) | LC 518, 377 |
| 2.11 | 回文子串數 | 中心擴展 / DP | LC 647 |
| 2.12 | 樹路徑和計數 | DFS + Prefix Sum | LC 437 |
| 2.13 | 矩陣中正方形數 | 2D DP | LC 221, 1277 |
| **最 (Optimize)** | | | |
| 3.1 | 最大連續子陣列和 | Kadane's | LC 53 |
| 3.2 | 最大路徑和（樹） | DFS postorder | LC 124 |
| 3.3 | 最小視窗含所有字元 | Sliding Window | LC 76 |
| 3.4 | 最短路（無權） | BFS | LC 127, 994 |
| 3.5 | 最短路（加權非負） | Dijkstra | LC 743, 787 |
| 3.6 | 最少硬幣湊金額 | DP (Knapsack) | LC 322 |
| 3.7 | 最長遞增子序列 | DP + Binary Search | LC 300 |
| 3.8 | 最大矩形面積 | Monotonic Stack | LC 84, 85 |
| 3.9 | 最大盛水容器 | Two Pointers | LC 11, 42 |
| 3.10 | 最長公共子序列 | 2D DP | LC 1143, 72 |
| 3.11 | 最大股票利潤 | Greedy / State DP | LC 121, 122 |
| 3.12 | 最長回文子串 | 中心擴展 / DP | LC 5, 516 |
| 3.13 | 背包最大價值 | DP (0/1 / Unbounded) | LC 416, 494 |
| 3.14 | 最少字串操作 | 2D DP (Edit Distance) | LC 72 |
| 3.15 | 最大子陣列乘積 | DP (track max + min) | LC 152 |
| 3.16 | 最大正方形 | 2D DP | LC 221 |
| **排 (Arrange)** | | | |
| 4.1 | 有限類別排序 | Dutch National Flag | LC 75 |
| 4.2 | 合併多個排序序列 | Min-Heap / Merge | LC 23, 88 |
| 4.3 | 重組使相鄰不重複 | Max-Heap + Greedy | LC 767, 621 |
| 4.4 | 依賴關係排序 | Topological Sort | LC 207, 210 |
| 4.5 | 下一個排列 | Math Pattern | LC 31 |
| 4.6 | 自定義排序 | Sort + Custom Comparator | LC 56, 179 |
| 4.7 | 原地分割 | Two Pointers | LC 283, 905 |
| 4.8 | 合併重疊區間 | Sort + Greedy | LC 56, 57 |
| **建 (Build)** | | | |
| 5.1 | 從遍歷建樹 | DFS + HashMap | LC 105, 106 |
| 5.2 | 展平樹為鏈表 | DFS / Morris | LC 114, 341 |
| 5.3 | 克隆圖/鏈表 | DFS/BFS + HashMap | LC 133, 138 |
| 5.4 | 序列化/反序列化 | BFS / DFS | LC 297, 449 |
| 5.5 | 設計資料結構 | 複合結構 (HashMap + DLL) | LC 146, 155 |
| 5.6 | 結構轉換 (BST ↔ List) | DFS / Divide and Conquer | LC 108, 426 |
| 5.7 | 表達式求值 | Stack (recursive) | LC 224, 227 |
| 5.8 | 實作 Iterator | Stack-based Iterator | LC 173, 284 |
| **驗 (Validate)** | | | |
| 6.1 | 括號合法性 | Stack | LC 20, 32 |
| 6.2 | 合法 BST | DFS with range | LC 98 |
| 6.3 | 回文驗證 | Two Pointers | LC 125, 234 |
| 6.4 | 能否到達終點 | Greedy / DP | LC 55, 45 |
| 6.5 | 圖有環嗎 | DFS coloring / Union-Find | LC 207, 261 |
| 6.6 | 二分圖判定 | BFS/DFS Coloring | LC 785 |
| 6.7 | 字串能否分割 | 1D DP | LC 139 |
| 6.8 | 驗證遍歷序列 | Stack | LC 255, 946 |
| 6.9 | 異位詞/同構判定 | HashMap (frequency) | LC 242, 205 |
| 6.10 | 子樹/對稱判定 | DFS (recursive compare) | LC 100, 101, 572 |
| **列 (Enumerate)** | | | |
| 7.1 | 所有子集 | Backtracking | LC 78, 90 |
| 7.2 | 所有排列 | Backtracking + used[] | LC 46, 47 |
| 7.3 | 所有組合 | Backtracking + start | LC 77, 39, 40 |
| 7.4 | 所有合法括號 | Backtracking + constraint | LC 22 |
| 7.5 | 圖中所有路徑 | DFS + Backtracking | LC 797 |
| 7.6 | N-Queens / Sudoku | Backtracking + check | LC 51, 37 |
| 7.7 | 字串所有分割方式 | Backtracking (partition) | LC 131, 93 |
| 7.8 | 所有表達式結果 | Divide and Conquer | LC 241, 282 |
| 7.9 | 電話鍵盤字母組合 | Backtracking (multi-way) | LC 17 |
| 7.10 | 矩陣中找所有單詞 | Trie + DFS | LC 79, 212 |
| **連 (Connect)** | | | |
| 8.1 | 兩點是否連通 | Union-Find / BFS | LC 547, 684 |
| 8.2 | 連通分量數 | Union-Find / DFS | LC 200, 323 |
| 8.3 | 課程能否修完 | Topological Sort | LC 207, 210 |
| 8.4 | 找多餘的邊 | Union-Find | LC 684, 685 |
| 8.5 | 最小生成樹 | Kruskal's / Prim's | LC 1584 |
| 8.6 | 帳戶合併 / 等價類 | Union-Find + HashMap | LC 721 |
| 8.7 | 圖是否為有效樹 | Union-Find / DFS | LC 261 |
| 8.8 | 被包圍區域 | Boundary DFS/BFS | LC 130, 1020 |
| 8.9 | 字串轉換路徑 | BFS + Wildcard | LC 127, 433 |
| 8.10 | 網路延遲傳播 | Dijkstra | LC 743 |
| **跨類型 (Cross)** | | | |
| X.1 | 接雨水 | Two Pointers / Stack | LC 42 |
| X.2 | 區間調度/會議室 | Sort + Heap / Greedy | LC 253, 435 |
| X.3 | 前綴和偽裝 | Prefix Sum + HashMap | LC 303, 238, 974 |
| X.4 | 矩陣當圖 | BFS / DFS / Dijkstra | LC 994, 1091, 417 |
| X.5 | 區間 DP | Interval DP | LC 312, 1000 |
| X.6 | Trie + Backtracking | Trie + DFS | LC 212 |
| X.7 | 滑動視窗最大值 | Monotonic Deque | LC 239 |
| X.8 | 狀態機 DP | State Machine DP | LC 309, 714, 188 |
| X.9 | Bit 進階 | Bit Manipulation | LC 137, 260 |
| X.10 | 隨機抽樣 | Reservoir Sampling | LC 382, 384 |

---

## 解題 SOP：三步定位法

```
看到題目
  │
  ▼
Step 1：這題在問什麼？ ─────────────────────────── 八大類之一
  │    找/數/最/排/建/驗/列/連
  ▼
Step 2：具體情境是什麼？ ─────────────────────────── 微觀情境 (1.1 ~ X.10)
  │    對照上方 120+ 情境描述
  │    看題目關鍵字：sorted? graph? substring? all possible?
  ▼
Step 3：算法家族確認 ───────────────────────────── 直接套用
  │    從情境直接對應算法
  │    去 01-17 教學檔看具體實作
  ▼
寫 code
```

### 快速分流的關鍵字對照表

| 看到這些關鍵字 | 直接想到 |
|--------------|---------|
| sorted + search | Binary Search |
| sorted + pair + target | Two Pointers (opposite) |
| substring / subarray + condition | Sliding Window |
| unsorted + find/count + O(n) | HashMap |
| next greater / next smaller | Monotonic Stack |
| shortest path (unweighted) | BFS |
| shortest path (weighted) | Dijkstra |
| all subsets / permutations / combinations | Backtracking |
| can finish / prerequisites / dependency | Topological Sort |
| connected / components / union | Union-Find |
| maximum subarray sum | Kadane's |
| longest subsequence (not contiguous) | DP |
| longest substring (contiguous) | Sliding Window |
| tree + path + sum | DFS |
| grid + regions / islands | Grid DFS/BFS |
| kth largest / smallest | Heap / QuickSelect |
| parentheses + valid | Stack |
| buy/sell stock | Greedy / State Machine DP |
| coins / capacity / weight | DP (Knapsack) |
| matrix + search | Binary Search / Staircase |
| two strings + common + subsequence | 2D DP |
| word + dictionary + prefix | Trie |
| detect cycle (graph) | DFS coloring / Union-Find |
| detect cycle (linked list) | Floyd's fast-slow |
| clone / deep copy | DFS + HashMap |
| serialize / deserialize | BFS or DFS |
| intervals + overlap | Sort + Greedy/Heap |
| histogram + area | Monotonic Stack |
| sliding window + max/min | Monotonic Deque |
| appears once / missing | XOR / Bit Manipulation |
| random + equal probability | Reservoir Sampling |

---

> **下一步**：確認情境後，回到對應的教學檔（01–17）學習具體實作和模板。
> 本檔只負責 **「問題是什麼 → 該用什麼」** 的映射，不負責 **「怎麼用」**。
