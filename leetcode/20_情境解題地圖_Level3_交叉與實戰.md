# 情境解題地圖 Level 3：交叉組合與實戰模擬

> **定位**：本系列最高階 — 訓練「複合型問題拆解」與「相似情境鑑別」能力
> **適用對象**：已刷 100+ 題、準備 Google / NVIDIA 面試最後衝刺
> **語言**：繁體中文解說 + English technical terms
> **前置要求**：熟悉 01-17 所有基礎教學檔案

---

## Part A：交叉情境 — 一題多算法的組合拳

> Google 最難的題目幾乎都不是「純粹的某一種算法」。它們把 2-3 種算法
> 交織在一起，考的是你能不能把大問題拆成可辨識的子結構。

### 識別口訣

```
當你發現一種算法解不掉整個問題，問自己：
  「哪一個步驟可以用另一種算法加速？」
  「哪一個前處理能讓後面的算法生效？」
```

---

### 組合 1：Sort + Two Pointers

| 項目 | 說明 |
|------|------|
| 情境 | 在未排序陣列中找兩數/三數/四數之和等於 target |
| 為什麼要組合 | Sort 讓陣列有序 → Two Pointers 可以 O(n) 掃描；否則得用 O(n^2) brute force |
| 關鍵洞察 | 排序成本 O(n log n) 遠低於暴力 O(n^2) 或 O(n^3)，所以排序是「划算的前處理」 |
| 代表題 | LC 15 3Sum, LC 18 4Sum, LC 16 3Sum Closest |

### 組合 2：Trie + DFS/Backtracking

| 項目 | 說明 |
|------|------|
| 情境 | 在字母矩陣中搜尋字典裡的所有單詞 |
| 為什麼要組合 | DFS 探索 grid 的所有路徑 + Trie 做前綴剪枝避免無效搜索 |
| 關鍵洞察 | 純 DFS 對每個單詞都要跑一次整個 grid；Trie 讓你同時搜索所有前綴匹配的單詞 |
| 代表題 | LC 212 Word Search II |

### 組合 3：Binary Search + Greedy (Binary Search on Answer)

| 項目 | 說明 |
|------|------|
| 情境 | 「最小化最大值」或「最大化最小值」的優化問題 |
| 為什麼要組合 | Binary Search 猜答案 + Greedy/模擬函式驗證「這個答案是否可行」 |
| 關鍵洞察 | 答案空間單調：如果 x 可行則 x+1 也可行（或反之），形成二分搜尋前提 |
| 代表題 | LC 410 Split Array Largest Sum, LC 875 Koko Eating Bananas, LC 1011 Capacity to Ship Packages |

### 組合 4：DP + Binary Search

| 項目 | 說明 |
|------|------|
| 情境 | LIS (Longest Increasing Subsequence) 的 O(n log n) 最佳解 |
| 為什麼要組合 | 維護一個 tails 陣列（有序），用 Binary Search 找插入位置 |
| 關鍵洞察 | 純 DP 是 O(n^2)；Binary Search 把每次查詢從 O(n) 降到 O(log n) |
| 代表題 | LC 300 Longest Increasing Subsequence, LC 354 Russian Doll Envelopes |

### 組合 5：Graph + DP (DAG 上的 DP)

| 項目 | 說明 |
|------|------|
| 情境 | 有向無環圖 (DAG) 上的最優路徑 / 限制步數的最短路 |
| 為什麼要組合 | Graph 建模問題結構 + DP 記錄到達每個節點的最優值 |
| 關鍵洞察 | DAG 保證沒有環 → 拓撲序就是 DP 的計算順序 |
| 代表題 | LC 787 Cheapest Flights Within K Stops, LC 1928 Minimum Cost to Reach City With Discounts |

### 組合 6：Stack + HashMap

| 項目 | 說明 |
|------|------|
| 情境 | Next Greater Element with index mapping / 跨陣列的對應關係 |
| 為什麼要組合 | Monotonic Stack 計算 next greater + HashMap 做元素位置映射 |
| 關鍵洞察 | Stack 處理「下一個更大」邏輯，HashMap 處理「在哪裡」邏輯，各司其職 |
| 代表題 | LC 496 Next Greater Element I, LC 503 Next Greater Element II (circular) |

### 組合 7：Two Heaps (Max-Heap + Min-Heap)

| 項目 | 說明 |
|------|------|
| 情境 | 動態資料流中維護中位數 |
| 為什麼要組合 | Max-Heap 存較小的一半，Min-Heap 存較大的一半，中位數在兩堆頂端 |
| 關鍵洞察 | 單一 Heap 無法同時追蹤左右兩半的邊界；兩個 Heap 把 O(n) 排序變成 O(log n) 插入 |
| 代表題 | LC 295 Find Median from Data Stream, LC 480 Sliding Window Median |

### 組合 8：Union-Find + Sort

| 項目 | 說明 |
|------|------|
| 情境 | 按特定順序或條件合併元素群組 |
| 為什麼要組合 | Sort 決定處理順序（如邊的權重） + Union-Find 維護連通性 |
| 關鍵洞察 | Kruskal MST 就是這個組合：排序邊 → 依序 union → 避免成環 |
| 代表題 | LC 721 Accounts Merge, LC 1202 Smallest String With Swaps, LC 1584 Min Cost to Connect All Points |

### 組合 9：Monotonic Stack + DP

| 項目 | 說明 |
|------|------|
| 情境 | 最大矩形面積 / 柱狀圖最大矩形 |
| 為什麼要組合 | DP 逐行計算柱高 + Monotonic Stack 在每行上求最大矩形 |
| 關鍵洞察 | LC 85 把 2D 問題分解成「每一行都跑一次 LC 84」 |
| 代表題 | LC 84 Largest Rectangle in Histogram, LC 85 Maximal Rectangle |

### 組合 10：BFS + Bitmask (State BFS)

| 項目 | 說明 |
|------|------|
| 情境 | 狀態空間搜索 — 需要記錄「已經訪問了哪些節點」 |
| 為什麼要組合 | BFS 做最短路徑 + Bitmask 壓縮已訪問集合為整數 |
| 關鍵洞察 | visited set 用 bitmask 表示讓狀態可以被 hash，避免重複搜索 |
| 代表題 | LC 847 Shortest Path Visiting All Nodes, LC 864 Shortest Path to Get All Keys |

### 組合 11：Sliding Window + HashMap (Counter)

| 項目 | 說明 |
|------|------|
| 情境 | 找包含特定字元/條件的最短/最長子字串 |
| 為什麼要組合 | Sliding Window 控制範圍 + HashMap 記錄窗口內字元頻率 |
| 關鍵洞察 | Window 的 expand/shrink 搭配 Counter 的 increment/decrement，實現 O(n) |
| 代表題 | LC 76 Minimum Window Substring, LC 438 Find All Anagrams, LC 567 Permutation in String |

### 組合 12：DFS + Memoization (Top-Down DP)

| 項目 | 說明 |
|------|------|
| 情境 | 遞迴結構 + 重疊子問題（直接 DFS 會 TLE） |
| 為什麼要組合 | DFS 定義遞迴框架 + Memo dict 避免重複計算 |
| 關鍵洞察 | 跟 Bottom-Up DP 等價，但 DFS 的思考方式更直覺；適合樹形/圖形結構 |
| 代表題 | LC 329 Longest Increasing Path in a Matrix, LC 1192 Critical Connections |

### 組合 13：Prefix Sum + HashMap

| 項目 | 說明 |
|------|------|
| 情境 | 子陣列和等於 k / 子陣列和是 k 的倍數（含負數） |
| 為什麼要組合 | Prefix Sum 把區間和轉成差值 + HashMap 快速查找歷史前綴和 |
| 關鍵洞察 | sum(i..j) = prefix[j] - prefix[i-1]，所以找 sum = k 等價於找 prefix[j] - k 是否出現過 |
| 代表題 | LC 560 Subarray Sum Equals K, LC 523 Continuous Subarray Sum, LC 974 Subarray Sums Divisible by K |

### 組合 14：Heap + BFS/Dijkstra

| 項目 | 說明 |
|------|------|
| 情境 | 加權圖最短路 / 矩陣中找最小代價路徑 |
| 為什麼要組合 | BFS 的結構 + Min-Heap 取代普通 Queue 來保證每次取出最小代價 |
| 關鍵洞察 | 無權圖用 BFS；加權圖用 Heap-based BFS = Dijkstra |
| 代表題 | LC 743 Network Delay Time, LC 1631 Path With Minimum Effort, LC 778 Swim in Rising Water |

### 組合 15：Backtracking + Pruning (剪枝策略)

| 項目 | 說明 |
|------|------|
| 情境 | 排列/組合問題中有額外約束（如 target sum） |
| 為什麼要組合 | Backtracking 枚舉所有可能 + 剪枝砍掉不可能達到目標的分支 |
| 關鍵洞察 | 排序是最常見的剪枝前處理：sorted 後一旦超過 target，後面更大的都不用看 |
| 代表題 | LC 39 Combination Sum, LC 40 Combination Sum II, LC 51 N-Queens |

### 組合 16：Graph BFS + Topological Sort

| 項目 | 說明 |
|------|------|
| 情境 | 課程排序 / 任務依賴 / 編譯順序 |
| 為什麼要組合 | TopSort 用 BFS (Kahn's) 實現：維護 in-degree + BFS 層層剝除 |
| 關鍵洞察 | 如果最終處理的節點數 < 總節點數，代表有環 → 無法完成 |
| 代表題 | LC 207 Course Schedule, LC 210 Course Schedule II, LC 269 Alien Dictionary |

### 組合 17：Two Pointers + Binary Search

| 項目 | 說明 |
|------|------|
| 情境 | 在有序矩陣中搜索 / 在合併排序結構中找第 k 小 |
| 為什麼要組合 | Two Pointers 走矩陣對角線 + Binary Search 做值域搜索 |
| 關鍵洞察 | 矩陣行列都有序時，從右上角開始走就像 BST 搜索 |
| 代表題 | LC 240 Search a 2D Matrix II, LC 378 Kth Smallest Element in a Sorted Matrix |

### 組合 18：DP + Bitmask (狀壓 DP)

| 項目 | 說明 |
|------|------|
| 情境 | 小規模集合的最優分配 / TSP / 任務分配 |
| 為什麼要組合 | DP 記錄最優值 + Bitmask 壓縮「哪些元素已被選」為狀態 |
| 關鍵洞察 | n <= 20 時可用（2^20 = 1M 狀態），暴力 n! 則會爆 |
| 代表題 | LC 1986 Minimum Number of Work Sessions, LC 698 Partition to K Equal Sum Subsets |

### 組合 19：Segment Tree + Coordinate Compression

| 項目 | 說明 |
|------|------|
| 情境 | 區間查詢 + 更新，但座標範圍極大 |
| 為什麼要組合 | 座標壓縮把稀疏值映射到連續 index + Segment Tree 做 range query |
| 關鍵洞察 | 值域 10^9 但實際只有 n 個值 → 壓縮到 [0, n-1] |
| 代表題 | LC 315 Count of Smaller Numbers After Self, LC 327 Count of Range Sum |

### 組合 20：HashMap + Doubly Linked List (Design)

| 項目 | 說明 |
|------|------|
| 情境 | O(1) 的 get + put + eviction（LRU/LFU Cache） |
| 為什麼要組合 | HashMap O(1) 查找 + Doubly Linked List O(1) 移動/刪除節點 |
| 關鍵洞察 | HashMap 指向 linked list node → 查到就能直接移動到最前面 |
| 代表題 | LC 146 LRU Cache, LC 460 LFU Cache |

### 組合 21：Graph + Binary Search (二分搜尋 + 圖檢查)

| 項目 | 說明 |
|------|------|
| 情境 | 找瓶頸路徑 — 最大化路徑上的最小邊權 |
| 為什麼要組合 | Binary Search 猜瓶頸值 + BFS/DFS 檢查只用 >= 該值的邊能否連通 |
| 關鍵洞察 | 答案具有單調性：閾值越高越難連通 |
| 代表題 | LC 1631 Path With Minimum Effort, LC 778 Swim in Rising Water |

### 組合 22：Deque (Monotonic Deque) + Sliding Window

| 項目 | 說明 |
|------|------|
| 情境 | 固定大小窗口中的最大值/最小值 |
| 為什麼要組合 | Sliding Window 控制範圍 + Monotonic Deque O(1) 追蹤極值 |
| 關鍵洞察 | Deque 前端永遠是當前窗口最大值；新元素從後端清除所有比它小的 |
| 代表題 | LC 239 Sliding Window Maximum |

### 組合 23：Math + Greedy (數學性質驅動的貪心)

| 項目 | 說明 |
|------|------|
| 情境 | 數字拆分最大乘積 / 最優策略問題 |
| 為什麼要組合 | 數學推導最優因子 + Greedy 持續拆分 |
| 關鍵洞察 | 拆成 3 的乘積最大（AM-GM 不等式推導） |
| 代表題 | LC 343 Integer Break, LC 1689 Partitioning Into Minimum Number Of Deci-Binary Numbers |

### 組合 24：Divide and Conquer + Merge Sort 應用

| 項目 | 說明 |
|------|------|
| 情境 | 計算逆序對 / 跨區間統計 |
| 為什麼要組合 | Merge Sort 在合併時順便統計跨越左右半的答案 |
| 關鍵洞察 | 合併時左右都已排序 → 可以用 Two Pointers O(n) 統計 |
| 代表題 | LC 315 Count of Smaller Numbers After Self, LC 493 Reverse Pairs |

### 組合 25：Union-Find + Graph Traversal

| 項目 | 說明 |
|------|------|
| 情境 | 動態連通性 + 需要查詢連通分量資訊 |
| 為什麼要組合 | Union-Find 維護連通性 + DFS/BFS 在需要時走訪整個分量 |
| 關鍵洞察 | Union-Find 判連通 O(α(n))，但要列舉分量內元素還是得遍歷 |
| 代表題 | LC 305 Number of Islands II, LC 547 Number of Provinces |

### 組合 26：Trie + Bitmask (XOR 最大值)

| 項目 | 說明 |
|------|------|
| 情境 | 找兩個數字 XOR 的最大值 |
| 為什麼要組合 | 把數字存入 binary Trie + 從高位貪心地走相反分支 |
| 關鍵洞察 | 高位決定 XOR 大小 → 從 MSB 開始，每一位盡量選不同 |
| 代表題 | LC 421 Maximum XOR of Two Numbers in an Array |

### 組合 27：DP + Monotonic Deque (滑動窗口最值 DP)

| 項目 | 說明 |
|------|------|
| 情境 | DP 轉移來自前 k 個狀態的最大/最小值 |
| 為什麼要組合 | DP 定義轉移 + Monotonic Deque 把轉移的 max/min 查詢降到 O(1) |
| 關鍵洞察 | dp[i] = max(dp[j]) + cost, j in [i-k, i-1] → Deque 維護窗口最值 |
| 代表題 | LC 1425 Constrained Subsequence Sum, LC 239 (非 DP 但同理) |

### 組合 28：Recursion + Iterative Conversion (Stack 模擬)

| 項目 | 說明 |
|------|------|
| 情境 | 面試要求不用遞迴實現 Tree traversal / Backtracking |
| 為什麼要組合 | 理解遞迴本質 + 用 explicit stack 模擬 call stack |
| 關鍵洞察 | 任何遞迴都能轉成迭代：function call = push stack, return = pop stack |
| 代表題 | LC 94 Inorder Traversal (iterative), LC 144 Preorder (iterative) |

### 組合 29：Multi-Source BFS + Grid

| 項目 | 說明 |
|------|------|
| 情境 | 從多個起點同時擴散 / 找最近的特定格子 |
| 為什麼要組合 | 把所有起點同時放入 Queue + BFS 層層擴散 |
| 關鍵洞察 | 比「對每個目標點都跑一次 BFS」快 n 倍 — O(m*n) vs O(k*m*n) |
| 代表題 | LC 286 Walls and Gates, LC 994 Rotting Oranges, LC 1162 As Far from Land as Possible |

### 組合 30：String Hashing + Sliding Window (Rabin-Karp)

| 項目 | 說明 |
|------|------|
| 情境 | 字串匹配 / 找重複子字串 |
| 為什麼要組合 | Sliding Window 滑過文本 + Rolling Hash O(1) 更新 hash 值 |
| 關鍵洞察 | Hash 碰撞需要二次驗證，但平均 O(n) 遠快於暴力 O(n*m) |
| 代表題 | LC 187 Repeated DNA Sequences, LC 1044 Longest Duplicate Substring |

---

## Part B：相似情境鑑別 — 長得像但解法不同

> **這是本檔案最有價值的段落。** Google 面試最狠的一招不是出難題，
> 而是出一題「看起來」像 X 但其實要用 Y 的題目。辨識錯誤 = 浪費 15 分鐘走錯路。

---

### 鑑別組 1：「子陣列之和」系列

| 題目特徵 | 你會直覺想用 | 真正該用 | 關鍵差異 |
|----------|-------------|---------|---------|
| 正數陣列，子陣列和 >= target | Sliding Window | Sliding Window | 全正 → 加元素和必增、縮窗和必減 → 單調 |
| 含負數，子陣列和 = k | Sliding Window? | Prefix Sum + HashMap | 有負數 → 窗口不單調，滑窗失效 |
| 子陣列和是 k 的倍數 | Prefix Sum? | Prefix Sum + HashMap (mod) | (prefix[j] - prefix[i]) % k == 0 等價於 prefix[j] % k == prefix[i] % k |
| 最大子陣列和 | 2D DP? | Kadane's Algorithm | 只需 O(1) 空間：current_max = max(num, current_max + num) |
| 子陣列乘積最大 | Kadane's? | 修改版 Kadane's (追蹤 min) | 負負得正 → 必須同時追蹤最小乘積 |
| 和為 k 的最長子陣列 | HashMap? | Prefix Sum + HashMap (存最早出現位置) | 要最長 → HashMap 只存第一次出現的 index |
| 和為 k 的最短子陣列（含負數） | Prefix Sum? | Monotonic Deque + Prefix Sum | 要最短 + 有負數 → Deque 維護單調前綴和 |

**記憶口訣**：全正用滑窗、有負用前綴、要乘積追蹤最小值。

---

### 鑑別組 2：「最短路徑」系列

| 情境 | 用什麼 | 為什麼 | 複雜度 |
|------|--------|--------|--------|
| Grid 中最短路（每步 cost = 1） | BFS | 無權圖 = BFS 天下 | O(V + E) |
| Grid 中最短路（cost 0 或 1） | 0-1 BFS (Deque) | cost 0 放 deque 前端、cost 1 放後端 | O(V + E) |
| 加權圖正權最短路 | Dijkstra (Min-Heap) | 正權 + 需要 relaxation | O(E log V) |
| 含負權（無負環）最短路 | Bellman-Ford | 能處理負權 | O(VE) |
| 所有點對最短路 | Floyd-Warshall | 三層迴圈，概念最簡單 | O(V^3) |
| 限制最多 K 步的最短路 | Modified Bellman-Ford / DP | 需要記錄步數維度 | O(KE) |
| 字串變換最短步數 | BFS (Implicit Graph) | 每次變一個字母 = 一步 = 無權 | O(26 * L * N) |
| DAG 最短路 | TopSort + DP | 拓撲序保證前驅都已計算 | O(V + E) |

**記憶口訣**：無權 BFS、正權 Dijkstra、負權 Bellman-Ford、限步數加維度。

---

### 鑑別組 3：「是否可達/可行」系列

| 問題 | 看起來像 | 真正用什麼 | 為什麼 |
|------|---------|-----------|--------|
| 能否跳到陣列末端 | DP? | Greedy (追蹤 maxReach) | 只要判斷 yes/no，不需要路徑 → Greedy O(n) |
| 能否修完所有課程 | Graph DFS? | TopSort (偵測有向圖是否有環) | 有環 = 有循環依賴 = 修不完 |
| 能否將陣列分成和相等的兩組 | Greedy? | DP (0/1 Knapsack) | 子集和問題 → Greedy 失敗（反例很容易構造） |
| 能否用字典拼出字串 | Backtracking? | DP (Word Break) | 有大量重疊子問題 → memo/DP |
| 能否用兩色塗圖 | DFS? | BFS/DFS (Bipartite Check) | 兩色 = 二分圖 = 相鄰不同色 |
| 能否重新排列成回文 | Sort? | HashMap (Count Characters) | 最多一個字元出現奇數次 → O(n) counting |
| 能否從左上走到右下 | BFS? | DP (Unique Paths) 或 BFS | 無障礙 = 數學公式；有障礙 = DP |

---

### 鑑別組 4：「找環」系列

| 情境 | 用什麼算法 | 為什麼不是其他的 |
|------|-----------|----------------|
| 陣列中找重複數字（不能改陣列） | Floyd's Cycle Detection | 把 arr[i] 當 next pointer → 轉成鏈表找環 |
| 鏈表中偵測環 | Floyd's Fast-Slow Pointers | 經典快慢指標：快追上慢 = 有環 |
| 有向圖中偵測環 | DFS Three-Color Marking | 白→灰→黑：灰色遇到灰色 = back edge = 環 |
| 無向圖中找多餘的邊 | Union-Find | 加邊時如果兩端已連通 → 這條就是多餘邊 |
| 課程能否全修完 | Topological Sort (Kahn's) | 最終 count < 總課程數 → 有環 |
| 函數呼叫是否有無限遞迴 | DFS + visited set | 同有向圖偵測環 |

**記憶口訣**：鏈表用快慢、有向用三色、無向用 Union-Find。

---

### 鑑別組 5：「連通性」判斷

| 情境 | BFS/DFS | Union-Find | 怎麼選 |
|------|---------|-----------|--------|
| 計算島嶼數量 | 掃到陸地就 DFS 標記 | 也可以，但 DFS 更直覺 | DFS 較常見 |
| 動態新增陸地後的島嶼數 | 每次都重跑？太慢 | Union-Find + 動態合併 | Union-Find 完勝 |
| 判斷整張圖是否連通 | 從一點 BFS 看能否到所有點 | 全部 union 後看 root 數 | 都行，Union-Find 略快 |
| 最小生成樹 | 不適用 | Kruskal (Sort + UF) | Union-Find 是核心 |
| 找所有連通分量的大小 | DFS 每個分量計數 | Union-Find + size 陣列 | 都行 |
| 判斷加邊後是否仍是樹 | DFS 太慢 | UF：加邊前已連通 = 成環 | Union-Find |

**決策規則**：靜態用 DFS/BFS、動態增刪用 Union-Find。

---

### 鑑別組 6：「Top K」系列

| 情境 | Sort | Heap | QuickSelect | 怎麼選 |
|------|------|------|-------------|--------|
| 找第 K 大的元素 | O(n log n) | O(n log k) Min-Heap | O(n) 平均 | 面試首選 Heap 或 QuickSelect |
| 找前 K 個高頻元素 | Sort by freq | Min-Heap size k | Bucket Sort O(n) | Bucket Sort 最優但少見 |
| 合併 K 個排序鏈表 | 不適用 | Min-Heap 存 k 個頭 | 不適用 | Heap 是唯一優解 |
| 找最接近原點的 K 個點 | Sort by distance | Max-Heap size k | QuickSelect | 都可，Heap 最穩 |
| 資料流中第 K 大 | 每次重排？太慢 | 固定 size k 的 Min-Heap | 不適用（資料流） | Heap 唯一選擇 |

**記憶口訣**：一次性 → QuickSelect/Sort；資料流 → Heap；合併多路 → Heap。

---

### 鑑別組 7：「子集/排列/組合」鑑別

| 類型 | 模板差異 | 元素可重用？ | 順序重要？ | 代表題 |
|------|---------|------------|-----------|--------|
| 子集 (Subset) | 每元素選或不選 | 否 | 否 | LC 78 |
| 含重複元素的子集 | 排序 + 跳過相鄰重複 | 否 | 否 | LC 90 |
| 組合 (Combination) | 限定大小 k 的子集 | 否 | 否 | LC 77 |
| 組合總和（可重用） | start 不 +1，可重複選 | 是 | 否 | LC 39 |
| 組合總和（不可重用） | 排序 + 跳重複 + start+1 | 否 | 否 | LC 40 |
| 排列 (Permutation) | 每層都從 0 開始但跳過 used | 否 | 是 | LC 46 |
| 含重複元素的排列 | 排序 + 同層跳重複 | 否 | 是 | LC 47 |

```
關鍵判斷流程：
  順序重要嗎？
    ├── 是 → 排列（每層 for 從 0 開始，用 used 陣列）
    └── 否 → 子集/組合（每層 for 從 start 開始，避免回頭）
              ├── 元素可重用？
              │   ├── 是 → for 從 i 開始（不 +1）
              │   └── 否 → for 從 i+1 開始
              └── 有重複元素？
                  ├── 是 → 排序 + if i > start and nums[i] == nums[i-1]: continue
                  └── 否 → 不需特殊處理
```

---

### 鑑別組 8：「Greedy 成功 vs 失敗」

| 問題 | Greedy 行嗎 | 正確做法 | 為什麼 Greedy 失敗 |
|------|------------|---------|-------------------|
| Jump Game I (能否到終點) | 可以 | Greedy maxReach | 只要判斷可達性，不需最優 |
| Jump Game II (最少跳幾次) | 可以 | Greedy (BFS 思維) | 每層能到的最遠 = 一跳 |
| Coin Change (最少硬幣) | 看面額 | DP | 面額非倍數關係時 Greedy 反例存在 |
| Activity Selection (最多活動) | 可以 | Greedy (按結束時間排) | 經典可證明：Exchange Argument |
| 0/1 Knapsack | 不行 | DP | 按價值/重量比貪心的反例很容易構造 |
| Fractional Knapsack | 可以 | Greedy (按 value/weight 排) | 物品可切割 → 局部最優 = 全域最優 |
| Huffman Coding | 可以 | Greedy (每次合併最小兩個) | 可用 Exchange Argument 證明 |
| Task Scheduler | 可以 | Greedy (最多的任務先排) | 高頻任務決定框架，低頻填空 |

**判斷法則**：
1. 能找到反例 → 不能 Greedy → 用 DP
2. 找不到反例 + 有 Exchange Argument → 可以 Greedy
3. 不確定 → 先寫 DP（面試中更安全）

---

### 鑑別組 9：「區間問題」系列

| 問題 | 排序依據 | 算法 | 代表題 |
|------|---------|------|--------|
| 合併重疊區間 | 按起點排 | Greedy merge | LC 56 Merge Intervals |
| 最多不重疊區間 | 按終點排 | Greedy (Activity Selection) | LC 435 Non-overlapping Intervals |
| 插入新區間 | 已排序 | 分三段處理 | LC 57 Insert Interval |
| 最少箭射氣球 | 按終點排 | Greedy (= Activity Selection 變形) | LC 452 Minimum Number of Arrows |
| 會議室能否不衝突 | 按起點排 | Sort + 掃描 | LC 252 Meeting Rooms |
| 最少需要幾間會議室 | 按起點排 | Min-Heap (追蹤結束時間) | LC 253 Meeting Rooms II |
| 安排員工工作時段 | 按起/終點 | Sweep Line (掃描線) | 各種 interval scheduling |

**記憶口訣**：合併按起點、選最多按終點、要幾間用 Heap。

---

### 鑑別組 10：「DP 的狀態定義」容易搞混

| 問題 | dp[i] 定義 | 常見錯誤定義 | 為什麼錯 |
|------|-----------|-------------|---------|
| LIS (最長遞增子序列) | 以 nums[i] 結尾的 LIS 長度 | 前 i 個的 LIS 長度 | 必須結尾在 i 才能正確轉移 |
| House Robber | 到第 i 間時的最大收益 | 搶第 i 間的最大收益 | 需要包含「不搶」的可能 |
| Word Break | s[0..i-1] 是否可拆 | s[i..n-1] 是否可拆 | 前向定義更自然、避免邊界錯誤 |
| Edit Distance | s1[0..i-1] 到 s2[0..j-1] 的編輯距離 | 第 i 步的操作 | DP 記的是狀態不是步驟 |
| Coin Change | 湊出金額 i 的最少硬幣 | 用了第 i 種硬幣的最少數量 | 金額是狀態，不是硬幣選擇 |

---

### 鑑別組 11：「BFS vs DFS」選擇

| 情境 | 用 BFS | 用 DFS | 為什麼 |
|------|--------|--------|--------|
| 最短路（無權） | BFS | 不行 | BFS 保證第一次到達就是最短 |
| 判斷連通性 | 都可以 | 都可以 | 只要能走完就行 |
| 拓撲排序 | Kahn's (BFS) | DFS 後序反轉 | 都是正解，BFS 更直覺 |
| 二分圖判斷 | BFS 塗色 | DFS 塗色 | 都行 |
| 找所有路徑 | 不適合 | DFS + Backtracking | BFS 不方便回溯 |
| 字母矩陣找單詞 | 不適合 | DFS + Backtracking | 需要回溯標記 |
| 層序遍歷 | BFS | 不適合 | BFS 天然分層 |
| 序列化/反序列化 Tree | 都可以 | 前序 DFS 最常見 | DFS 的序列化更緊湊 |

---

### 鑑別組 12：「Sliding Window 可以用 vs 不可以用」

| 條件 | 能用 Sliding Window? | 替代方案 | 原因 |
|------|---------------------|---------|------|
| 全正數，求和 >= target 的最短子陣列 | 可以 | — | 加元素和↑，移除元素和↓ → 單調 |
| 含負數，求和 = k | 不行 | Prefix Sum + HashMap | 加元素和可能↓ → 不知道該縮還是擴 |
| 字串中最長不重複字元子串 | 可以 | — | 加入重複字元時收縮窗口是確定的 |
| 字串中包含所有字元的最短子串 | 可以 | — | 滿足條件後收縮，收縮方向確定 |
| 子陣列中最多 K 個不同元素 | 可以 | — | 超過 K 個就收縮，方向確定 |
| 子陣列乘積 < K（全正） | 可以 | — | 全正 → 乘積隨窗口單調 |
| 子陣列乘積 < K（含負/零） | 不行 | 分情況討論 | 乘負數方向反轉 |

**Sliding Window 核心前提**：窗口的 expand/shrink 與目標函數之間必須有**單調關係**。

---

### 鑑別組 13：「Binary Search 的邊界處理」

| 情境 | left 初始值 | right 初始值 | while 條件 | 回傳 |
|------|------------|-------------|------------|------|
| 標準搜索（找 target） | 0 | n-1 | left <= right | mid (找到) 或 -1 |
| 左邊界 (first occurrence) | 0 | n-1 | left <= right | left (跳出迴圈後) |
| 右邊界 (last occurrence) | 0 | n-1 | left <= right | right (跳出迴圈後) |
| Search on Answer (最小可行值) | answer_min | answer_max | left <= right | left |
| Search on Answer (最大可行值) | answer_min | answer_max | left <= right | right |

```
最小可行值 vs 最大可行值：

  最小可行值：feasible(mid) → right = mid - 1（往左擠）→ 回傳 left
  最大可行值：feasible(mid) → left = mid + 1（往右擠）→ 回傳 right
```

---

### 鑑別組 14：「Tree 問題的遍歷選擇」

| 情境 | 用什麼遍歷 | 為什麼 |
|------|-----------|--------|
| 計算高度/深度 | 後序 DFS (Post-order) | 需要先知道子樹結果 |
| 驗證 BST | 中序 DFS (In-order) | BST 中序 = 排序序列 |
| 序列化 Tree | 前序 DFS (Pre-order) | 根在前面，容易反序列化 |
| 層序遍歷/找最淺節點 | BFS | 天然分層 |
| 路徑和（根到葉） | 前序 DFS | 從上往下傳遞累積和 |
| Diameter / 最長路徑 | 後序 DFS | 需要先算左右子樹深度 |
| LCA (最低共同祖先) | 後序 DFS | 先查左右子樹再判斷 |

---

### 鑑別組 15：「字串匹配」系列

| 情境 | 用什麼 | 為什麼不用其他 |
|------|--------|--------------|
| 簡單 pattern matching | KMP / Built-in | O(n+m) |
| 萬用字元 (? 和 *) | DP | 狀態轉移隨 * 展開 |
| 正則表達式 (. 和 *) | DP | * 代表前一字元的重複 |
| 找所有 anagram 位置 | Sliding Window + Counter | 固定窗口大小 = pattern 長度 |
| 最短包含子串 | Sliding Window + Counter | 可變窗口，先擴後縮 |
| 編輯距離 | DP (2D) | 三種操作：插入、刪除、替換 |
| 子序列判斷 | Two Pointers | O(n) 即可，不需 DP |

---

### 鑑別組 16：「Matrix 問題」路線選擇

| 情境 | 用什麼 | 為什麼 |
|------|--------|--------|
| 計算路徑數（從左上到右下） | DP | 每格 = 上方 + 左方 |
| 最短路（每步 cost=1） | BFS | 無權最短路 |
| 最短路（不同 cost） | Dijkstra / DP | 加權最短路 |
| 搜索特定值（行列有序） | Two Pointers (右上角開始) | O(m+n) |
| 旋轉/翻轉矩陣 | 數學（轉置 + 反轉行） | in-place 操作 |
| 找島嶼數量 | DFS/BFS flood fill | 連通分量 |
| Spiral Order 輸出 | 模擬（四個邊界指標） | 無需特殊算法 |

---

## Part C：Google / NVIDIA 面試模擬情境

> 以下模擬真實面試場景。每題包含：
> - 面試官的口述問題（自然語言）
> - 你該如何識別 pattern
> - 最佳解法
> - 面試官常見的 follow-up 追問

---

### 模擬 1：城市導航

**面試官說**：「給你一個城市道路網，每條路有不同的長度。找從你家到公司的最短路線。」

- **識別**：加權圖 + 最短路徑 → 正權 → Dijkstra
- **算法**：Dijkstra with Min-Heap
- **複雜度**：O(E log V)
- **Follow-up 1**：「如果有些路是單行道？」→ 有向圖，Dijkstra 仍適用
- **Follow-up 2**：「如果要限制轉彎次數 <= K？」→ 狀態 BFS：state = (node, turns_left)
- **Follow-up 3**：「如果有些路段會塞車（動態權重）？」→ A* search with heuristic

---

### 模擬 2：自動補全系統

**面試官說**：「你有一本字典。給一個前綴，回傳所有以此前綴開頭的單詞。」

- **識別**：前綴搜尋 → Trie
- **算法**：Build Trie + DFS from prefix node
- **複雜度**：Build O(sum of word lengths), Query O(prefix + results)
- **Follow-up 1**：「如果要按頻率排序？」→ Trie 節點加 count + 搜尋結果用 Heap
- **Follow-up 2**：「如果打字有錯字容錯？」→ Trie + DFS with edit distance <= 1
- **Follow-up 3**：「如果字典有百萬個詞怎麼省記憶體？」→ Compressed Trie (Patricia Trie)

---

### 模擬 3：社群網路好友推薦

**面試官說**：「Facebook 想推薦新朋友。找出跟你有最多共同好友的人。」

- **識別**：圖的鄰居交集 → BFS 2 層 + counting
- **算法**：BFS depth 2 from user → count second-hop neighbors by frequency
- **複雜度**：O(d^2) where d = average degree
- **Follow-up 1**：「如果社群很大怎麼辦？」→ 分散式 MapReduce
- **Follow-up 2**：「如果要即時更新？」→ 增量計算 + Cache

---

### 模擬 4：任務排程

**面試官說**：「有一堆任務有先後依賴。給出一個合法的執行順序。」

- **識別**：依賴關係 = 有向圖 → 拓撲排序
- **算法**：Kahn's Algorithm (BFS TopSort)
- **複雜度**：O(V + E)
- **Follow-up 1**：「如果有循環依賴怎麼辦？」→ TopSort 無法完成 → 回報有環
- **Follow-up 2**：「如果有多個 CPU 可以平行執行？」→ BFS 層級 = 平行批次
- **Follow-up 3**：「如果每個任務有不同執行時間？」→ Critical Path Method (DP on DAG)

---

### 模擬 5：即時通訊已讀回條

**面試官說**：「設計一個像 WhatsApp 的已讀回條。需要 O(1) 查詢最新已讀訊息。」

- **識別**：key-value 快速存取 + 順序維護 → HashMap + 有序結構
- **算法**：HashMap<userId, lastReadMessageId>
- **Follow-up 1**：「如果要知道群組中有多少人已讀某則訊息？」→ Binary Search on sorted read pointers
- **Follow-up 2**：「如果要 LRU eviction？」→ HashMap + Doubly Linked List = LC 146

---

### 模擬 6：檔案系統搜尋

**面試官說**：「實作一個函式 find(root, pattern)，支援 * 和 ? 萬用字元。」

- **識別**：萬用字元匹配 → DP
- **算法**：2D DP — dp[i][j] = pattern[0..i-1] matches text[0..j-1]
- **複雜度**：O(m * n)
- **Follow-up 1**：「如果只需要判斷前綴？」→ Trie 更適合
- **Follow-up 2**：「如果檔案系統是分散式的？」→ 分散式 Trie / B-Tree index

---

### 模擬 7：GPU 任務分配 (NVIDIA)

**面試官說**：「有 N 個運算任務要分配到 K 個 GPU。每個任務有不同的運算量。目標是最小化最慢的 GPU 完成時間。」

- **識別**：最小化最大值 → Binary Search on Answer
- **算法**：Binary Search on max_time + Greedy 驗證「能否在 max_time 內分完」
- **複雜度**：O(N log(sum of tasks))
- **Follow-up 1**：「如果任務之間有依賴關係？」→ TopSort + DP
- **Follow-up 2**：「如果要精確最佳解？」→ DP + Bitmask（N 小時）

---

### 模擬 8：串流資料中位數

**面試官說**：「資料不斷進來，隨時可能被問『目前的中位數是多少？』」

- **識別**：動態資料流 + 中位數 → Two Heaps
- **算法**：Max-Heap (左半) + Min-Heap (右半)
- **複雜度**：Insert O(log n), Query O(1)
- **Follow-up 1**：「如果要找第 K 大的呢？」→ Fixed-size Min-Heap of size K
- **Follow-up 2**：「如果資料會過期（Sliding Window Median）？」→ Heap + Lazy Deletion or Balanced BST

---

### 模擬 9：網頁爬蟲

**面試官說**：「給你一個起始 URL，爬取同 domain 下所有可到達的頁面。」

- **識別**：從起點擴散 → BFS on implicit graph
- **算法**：BFS + HashSet (visited URLs)
- **Follow-up 1**：「如果要限制深度？」→ BFS 天然分層，加 depth counter
- **Follow-up 2**：「如果要多執行緒加速？」→ Concurrent BFS with thread-safe queue
- **Follow-up 3**：「如果要優先爬重要頁面？」→ Priority Queue (Heap) 替代普通 Queue

---

### 模擬 10：電路板布線 (NVIDIA)

**面試官說**：「在一塊 m x n 的電路板上，找從晶片 A 到晶片 B 的最短走線，有些格子有障礙。」

- **識別**：Grid + 障礙 + 最短路（每步 cost=1） → BFS
- **算法**：BFS from A to B, skipping obstacles
- **複雜度**：O(m * n)
- **Follow-up 1**：「如果走線有不同的信號延遲？」→ Dijkstra
- **Follow-up 2**：「如果要讓多條走線互不交叉？」→ NP-hard (Maximum Disjoint Paths)
- **Follow-up 3**：「如果可以穿越某些障礙但有額外成本？」→ 0-1 BFS 或 Dijkstra

---

### 模擬 11：基因序列比對

**面試官說**：「比較兩段 DNA 序列的相似度。可以插入空格(gap)來對齊。」

- **識別**：兩個序列的最佳對齊 → Edit Distance / LCS 的變形
- **算法**：2D DP (Sequence Alignment)
- **複雜度**：O(m * n)
- **Follow-up 1**：「如果序列很長（百萬級）？」→ 空間優化到 O(min(m,n)) (滾動陣列)
- **Follow-up 2**：「如果要找局部最佳對齊而非全域？」→ Smith-Waterman Algorithm

---

### 模擬 12：股票交易策略

**面試官說**：「給你每天的股價，最多買賣 K 次，求最大利潤。」

- **識別**：多次交易 + 限制次數 → DP (狀態機)
- **算法**：dp[day][transactions][holding] — 三維狀態
- **複雜度**：O(n * k)，空間可壓縮
- **Follow-up 1**：「不限次數？」→ Greedy（所有上漲段都賺）= LC 122
- **Follow-up 2**：「有冷卻期？」→ 狀態多一種「cooldown」= LC 309
- **Follow-up 3**：「有手續費？」→ 賣出時扣費 = LC 714

---

### 模擬 13：地圖上最近的加油站

**面試官說**：「你在一個 2D 地圖上，找離你最近的 K 個加油站。」

- **識別**：K Nearest Points → Max-Heap of size K
- **算法**：遍歷所有加油站，維護 size=K 的 Max-Heap
- **複雜度**：O(n log k)
- **Follow-up 1**：「如果加油站會動態新增/關閉？」→ KD-Tree
- **Follow-up 2**：「如果要考慮道路距離而非直線距離？」→ Dijkstra from current position

---

### 模擬 14：版本控制合併衝突

**面試官說**：「兩個開發者同時修改了同一個文件。找出他們修改的差異區段。」

- **識別**：兩個序列找公共部分 → LCS (Longest Common Subsequence)
- **算法**：2D DP for LCS → diff = not in LCS
- **複雜度**：O(m * n)
- **Follow-up**：「如果是三方合併 (3-way merge)？」→ LCS of three sequences

---

### 模擬 15：智慧停車場

**面試官說**：「設計一個停車場系統。車子進來時分配最近的空位，離開時釋放。」

- **識別**：動態取最小值 + 釋放後再放回 → Min-Heap
- **算法**：Min-Heap of available spots
- **複雜度**：Park O(log n), Leave O(log n)
- **Follow-up 1**：「如果有不同大小的車位？」→ 多個 Heap（小/中/大）
- **Follow-up 2**：「如果要找最近的特定樓層車位？」→ TreeMap per floor

---

### 模擬 16：視訊串流封包重組

**面試官說**：「視訊封包亂序到達，每個封包有序號。找出目前可以播放到哪裡（最長連續序號起始於 1）。」

- **識別**：找從 1 開始的最長連續序列 → HashSet + linear scan
- **算法**：HashSet 存所有已收到的序號，從 1 開始往上找
- **Follow-up 1**：「如果封包量很大怎麼優化？」→ 區間合併 (Merge Intervals) + TreeMap
- **Follow-up 2**：「如果要支持 buffer 大小限制？」→ Sliding Window on sequence numbers

---

### 模擬 17：推薦系統排名

**面試官說**：「有一個商品推薦列表不斷更新。要隨時回傳 Top K 推薦商品。」

- **識別**：動態 Top K → Heap
- **算法**：Min-Heap of size K（最小的元素在頂端，新元素大於頂端就替換）
- **複雜度**：每次更新 O(log K)
- **Follow-up**：「如果商品分數會隨時間衰減？」→ Lazy evaluation + 定期 rebuild

---

### 模擬 18：平行編譯依賴 (NVIDIA)

**面試官說**：「有 N 個 CUDA kernel 要編譯，有些要等前面的完成。用 P 個 processor，算最短總時間。」

- **識別**：DAG + 排程 → TopSort + Greedy/DP
- **算法**：TopSort 求 Critical Path Length（最長路徑 = 下界），再用 Greedy 分配
- **複雜度**：O(V + E)
- **Follow-up**：「如果 processor 有不同速度？」→ 這是 NP-hard 的 job scheduling 問題，用 approximation

---

### 模擬 19：文字編輯器 Undo/Redo

**面試官說**：「實作一個支持 type, delete, undo, redo 的文字編輯器。」

- **識別**：操作歷史 = 兩個 Stack（undo stack + redo stack）
- **算法**：type/delete → push to undo stack, clear redo; undo → pop undo push redo; redo → pop redo push undo
- **Follow-up 1**：「如果要支持 undo 到任意歷史點？」→ Persistent Data Structure 或 Command Pattern + 版本號
- **Follow-up 2**：「如果多人同時編輯？」→ CRDT / Operational Transformation

---

### 模擬 20：晶片缺陷偵測 (NVIDIA)

**面試官說**：「一張晶圓照片用 0/1 矩陣表示（1=缺陷）。找出所有缺陷區域的面積和形狀。」

- **識別**：Connected Components in Grid → DFS/BFS flood fill
- **算法**：遍歷 grid，遇到 1 就 DFS 計算面積並標記 visited
- **複雜度**：O(m * n)
- **Follow-up 1**：「如何分類缺陷形狀（點/線/面）？」→ 記錄 bounding box 長寬比
- **Follow-up 2**：「如果缺陷圖會動態更新？」→ Union-Find (動態合併)
- **Follow-up 3**：「如果要找最大的缺陷區域？」→ 在 DFS 中追蹤 max_area

---

## Part D：終極速查表

### D.1 情境 → 算法 快速對照

```
┌─────────────────────────────────────┬──────────────────────────────────┐
│ 你聽到的關鍵字                        │ 你該想到的算法                      │
├─────────────────────────────────────┼──────────────────────────────────┤
│ 「排序陣列中找...」                    │ Binary Search                    │
│ 「未排序陣列找兩數之和」                │ HashMap (Two Sum pattern)        │
│ 「未排序找三數之和」                   │ Sort + Two Pointers              │
│ 「連續子陣列」+ 全正數                 │ Sliding Window                   │
│ 「連續子陣列」+ 有負數 + 和=k          │ Prefix Sum + HashMap             │
│ 「最長/最短子字串」                    │ Sliding Window + HashMap         │
│ 「最大子陣列和」                       │ Kadane's Algorithm               │
│ 「前 K 個...」                        │ Heap (size K)                    │
│ 「第 K 大/小」                        │ QuickSelect 或 Heap              │
│ 「下一個更大元素」                     │ Monotonic Stack                  │
│ 「括號匹配/巢狀結構」                  │ Stack                            │
│ 「前綴搜尋/自動補全」                  │ Trie                             │
│ 「樹的最深/最淺」                     │ DFS (深) / BFS (淺)              │
│ 「樹的層序」                          │ BFS                              │
│ 「圖的連通分量」                       │ DFS/BFS 或 Union-Find            │
│ 「圖的最短路（無權）」                 │ BFS                              │
│ 「圖的最短路（加權）」                 │ Dijkstra                         │
│ 「有向圖有沒有環」                     │ DFS Three-Color 或 TopSort       │
│ 「任務依賴排序」                       │ Topological Sort (Kahn's)        │
│ 「最小生成樹」                        │ Kruskal (Sort + UF) 或 Prim      │
│ 「能不能做到 → Yes/No」               │ 看情境：Greedy / DP / Graph      │
│ 「最少步數/最少操作」                  │ BFS (狀態圖) 或 DP               │
│ 「所有可能的組合/排列」                │ Backtracking                     │
│ 「最大化最小值」                       │ Binary Search on Answer          │
│ 「最小化最大值」                       │ Binary Search on Answer          │
│ 「區間合併/重疊」                      │ Sort + Greedy                    │
│ 「設計 O(1) 的 get/put」             │ HashMap + Doubly Linked List     │
│ 「動態中位數」                        │ Two Heaps                        │
│ 「重新排列/放置元素」                  │ Greedy + Heap                    │
│ 「最長遞增子序列」                     │ DP O(n^2) 或 BS O(n log n)       │
│ 「兩個字串的距離/相似度」              │ DP (Edit Distance / LCS)         │
│ 「字母矩陣找單詞」                     │ Trie + DFS                       │
│ 「資料流」                            │ Heap 或 特殊資料結構              │
└─────────────────────────────────────┴──────────────────────────────────┘
```

### D.2 複雜度速查

```
算法                          時間            空間         備註
───────────────────────────────────────────────────────────────────
Binary Search                O(log n)        O(1)         前提：有序
Two Pointers                 O(n)            O(1)         前提：有序或特定結構
Sliding Window               O(n)            O(k)         k = window size 或字元種類
HashMap lookup               O(1) avg        O(n)
Prefix Sum build             O(n)            O(n)
Prefix Sum query             O(1)            —
Kadane's                     O(n)            O(1)
Stack (Monotonic)            O(n)            O(n)
Heap push/pop                O(log n)        O(n)
Heap build (heapify)         O(n)            O(n)
QuickSelect                  O(n) avg        O(1)         最差 O(n^2)
Merge Sort                   O(n log n)      O(n)
Quick Sort                   O(n log n) avg  O(log n)     最差 O(n^2)
DFS (graph)                  O(V + E)        O(V)
BFS (graph)                  O(V + E)        O(V)
Dijkstra (heap)              O(E log V)      O(V)
Bellman-Ford                 O(VE)           O(V)
Floyd-Warshall               O(V^3)          O(V^2)
TopSort (Kahn's)             O(V + E)        O(V)
Union-Find (optimized)       O(α(n)) ≈ O(1)  O(n)
Trie insert/search           O(L)            O(Σ * L * n)  L=word length
DP 1D                        O(n) ~ O(n^2)   O(n)
DP 2D                        O(m * n)        O(m * n)      可滾動壓縮
Backtracking                 O(k^n) worst    O(n)          剪枝降低常數
Bitmask DP                   O(2^n * n)      O(2^n)        n ≤ 20
Segment Tree query/update    O(log n)        O(n)
```

### D.3 「什麼時候用什麼」決策樹

```
開始
  │
  ├── 問「找最短路嗎？」
  │     ├── 是 → 有權重嗎？
  │     │         ├── 無權 → BFS
  │     │         ├── 正權 → Dijkstra
  │     │         ├── 負權 → Bellman-Ford
  │     │         └── 限步數 → Modified BF / DP
  │     └── 否 ↓
  │
  ├── 問「在排序陣列/答案空間上搜索嗎？」
  │     ├── 是 → Binary Search
  │     └── 否 ↓
  │
  ├── 問「處理連續子陣列/子字串嗎？」
  │     ├── 是 → 全正數？
  │     │         ├── 是 → Sliding Window
  │     │         └── 否 → Prefix Sum + HashMap
  │     └── 否 ↓
  │
  ├── 問「要列舉所有可能嗎？」
  │     ├── 是 → Backtracking（+ 剪枝）
  │     └── 否 ↓
  │
  ├── 問「有重疊子問題嗎？」
  │     ├── 是 → DP
  │     └── 否 ↓
  │
  ├── 問「處理圖/樹的結構嗎？」
  │     ├── 樹 → DFS (大多) 或 BFS (層序)
  │     ├── 圖 → 看問題：連通(UF/DFS) / 排序(TopSort) / 最短路(上面)
  │     └── 否 ↓
  │
  ├── 問「需要 O(1) 查找/計數嗎？」
  │     ├── 是 → HashMap / HashSet
  │     └── 否 ↓
  │
  ├── 問「需要維護極值/Top K？」
  │     ├── 是 → Heap
  │     └── 否 ↓
  │
  ├── 問「有單調性可利用嗎？」
  │     ├── 是 → Monotonic Stack/Deque
  │     └── 否 ↓
  │
  └── 考慮 Greedy / Math / Simulation
```

### D.4 面試 30 秒辨識 Cheat Sheet

| 聽到這個 | 立刻想到 | 確認條件 |
|---------|---------|---------|
| 「給你一個排序陣列...」 | Binary Search | 找什麼？target / boundary / answer |
| 「子字串/子陣列中滿足...」 | Sliding Window | 確認是否有單調性 |
| 「出現次數 / 存不存在」 | HashMap / HashSet | O(1) lookup |
| 「下一個更大 / 溫度升高」 | Monotonic Stack | 從右往左或從左往右 |
| 「最短距離 / 最少步驟」 | BFS（無權）或 Dijkstra（有權） | 確認有無權重 |
| 「課程/任務順序」 | Topological Sort | 建圖 → 算 in-degree → BFS |
| 「島嶼/連通區域」 | DFS flood fill 或 Union-Find | 靜態 DFS、動態 UF |
| 「所有組合/排列/子集」 | Backtracking | 看順序重不重要 |
| 「最大/最小...在滿足...」 | Binary Search on Answer | 確認答案空間單調 |
| 「兩個序列的相似度」 | DP (LCS / Edit Distance) | 2D 表格 |
| 「前 K 個 / 第 K 大」 | Heap | size K 的 Min/Max Heap |
| 「前綴匹配 / 字典搜尋」 | Trie | 多次查詢時效益最大 |
| 「設計一個 Cache」 | HashMap + Linked List | LRU = 最近最少使用 |
| 「即時 Median」 | Two Heaps | Max-Heap 左 + Min-Heap 右 |
| 「能不能分成兩組等和」 | DP (0/1 Knapsack) | target = total_sum / 2 |
| 「區間合併」 | Sort by start + Greedy | 比較 current.end vs next.start |

---

## 附錄：交叉組合練習清單

> 以下列出每種組合技的練習題，標註 LC 編號與難度。

| 組合技 | 練習題 (Easy → Hard) |
|-------|---------------------|
| Sort + Two Pointers | LC 167 (E), LC 15 (M), LC 18 (M), LC 16 (M) |
| Trie + DFS | LC 208 (M), LC 211 (M), LC 212 (H) |
| BS + Greedy | LC 875 (M), LC 1011 (M), LC 410 (H), LC 774 (H) |
| DP + BS | LC 300 (M), LC 354 (H), LC 1964 (H) |
| Graph + DP | LC 787 (M), LC 1129 (M), LC 1334 (H) |
| Stack + HashMap | LC 496 (E), LC 503 (M), LC 901 (M) |
| Two Heaps | LC 295 (H), LC 480 (H), LC 502 (H) |
| UF + Sort | LC 721 (M), LC 1202 (M), LC 1584 (M) |
| Mono Stack + DP | LC 84 (H), LC 85 (H), LC 907 (M) |
| BFS + Bitmask | LC 847 (H), LC 864 (H), LC 1494 (H) |
| SW + HashMap | LC 3 (M), LC 76 (H), LC 438 (M), LC 567 (M) |
| DFS + Memo | LC 329 (H), LC 1335 (H), LC 576 (M) |
| Prefix Sum + HashMap | LC 560 (M), LC 523 (M), LC 974 (M) |
| Heap + Dijkstra | LC 743 (M), LC 1631 (M), LC 778 (H) |
| Backtracking + Pruning | LC 39 (M), LC 40 (M), LC 51 (H) |
| BFS TopSort | LC 207 (M), LC 210 (M), LC 269 (H) |
| TP + BS (Matrix) | LC 240 (M), LC 378 (M), LC 668 (H) |
| DP + Bitmask | LC 698 (M), LC 1986 (M), LC 943 (H) |
| Segment Tree | LC 315 (H), LC 327 (H), LC 307 (M) |
| HashMap + DLL | LC 146 (M), LC 460 (H), LC 432 (H) |

---

> **使用建議**：
> 1. Part B「相似情境鑑別」優先讀 — 這是投資報酬率最高的段落
> 2. Part C「模擬情境」大聲唸出來練習 — 模擬真實面試的口述解題
> 3. Part D「速查表」印出來貼在螢幕旁 — 刷題時隨時比對
> 4. 每做完一題就回來這份地圖定位 — 「這題用了哪些組合技？歸類到哪個鑑別組？」
