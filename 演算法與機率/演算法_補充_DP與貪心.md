# 演算法補充題庫：動態規劃與貪心演算法

> 補充自 NTU_Algorithm_Exams.md 與 NTU_Algorithm_Exams_Complete.md

---

## 題目 B1（陳和麟 109-1 期中 P6）

Prof. Chen wants to maximize total meeting time. Meetings M₁,...,Mₙ with start time sᵢ and end time tᵢ (t₁ ≤ t₂ ≤ ... ≤ tₙ).

(1) Must attend at least k meetings. Design algorithm to maximize total meeting time. Polynomial in nk.
(2) Additional constraint: for every i, Mᵢ and Mᵢ₊₂ cannot both be attended. Maximize total meeting time. Polynomial in n.

### 詳解

**(1) DP with constraint "at least k meetings"**

**子問題定義**：dp[i][j] = 前 i 個 meeting 中恰好參加 j 個的最大總時間，且不衝突。

先按 tᵢ 排序（已給定）。對每個 i，定義 prev(i) = 最大的 j < i 使得 tⱼ ≤ sᵢ（即不衝突的最近前一個 meeting）。可用 binary search 在 O(log n) 求得。

**遞迴式**：

$$dp[i][j] = \max \begin{cases} dp[i-1][j] & \text{（不參加 } M_i\text{）} \\ dp[prev(i)][j-1] + (t_i - s_i) & \text{（參加 } M_i\text{）} \end{cases}$$

邊界：dp[0][0] = 0, dp[i][j] = -∞ 當 j > i 或 j < 0。

答案 = max{dp[n][j] : j ≥ k}

**時間複雜度**：O(nk) 狀態 × O(1) 轉移（prev 預處理 O(n log n)）。

$$\boxed{O(nk) \text{ — DP: dp[i][j] = 前 i 個 meeting 參加 j 個的最大時間}}$$

**(2) Constraint: Mᵢ and Mᵢ₊₂ cannot both be attended**

這個額外限制是基於**索引**（不只是時間衝突），Mᵢ 和 Mᵢ₊₂ 不能同時選。

**子問題定義**：dp[i] = 前 i 個 meeting 的最大總時間（考慮時間衝突 + 索引約束）。

但注意還要考慮原始的時間不衝突條件。

更精確地，令 dp[i][0] = 前 i 個 meeting 中不選 Mᵢ 的最大時間，dp[i][1] = 前 i 個 meeting 中選 Mᵢ 的最大時間。

$$dp[i][0] = \max(dp[i-1][0], dp[i-1][1])$$

$$dp[i][1] = \max(dp[i-1][0], dp[i-2][0], dp[i-2][1] \text{ if } M_{i-2} \text{不與} M_i \text{時間衝突}) + (t_i - s_i)$$

但由於 "Mᵢ 和 Mᵢ₊₂ 不能同時" 的限制，**如果選了 Mᵢ，則 Mᵢ₋₂ 不能選**。

重新定義：dp[i][1] 選 Mᵢ 時，Mᵢ₋₁ 可以選或不選，但 Mᵢ₋₂ 不能選。

$$dp[i][1] = dp[i-1][0] + (t_i - s_i) \quad \text{(若 } M_{i-1} \text{ 和 } M_i \text{ 不時間衝突)}$$

$$dp[i][1] = \max(dp[i-1][0], dp[i-2][0]) + (t_i - s_i) \quad \text{(general case)}$$

更簡潔的做法：三狀態

- 定義 dp[i] = 考慮到第 i 個 meeting 的最大時間
- 不選 i：dp[i] = dp[i-1]
- 選 i：需要 i-2 不被選（索引限制），且不與前一個被選的衝突

$$\boxed{O(n) \text{ — 類似 weighted interval scheduling 但加入索引間距約束}}$$

---

## 題目 B2（蔡欣穆 100-1 期中 P3）

Determine the cost and structure of an optimal binary search tree for n=7 keys with given probabilities pᵢ and qᵢ.

### 詳解

**Optimal BST 的 DP 公式**（CLRS Chapter 15）：

定義 e[i,j] = 搜索 kᵢ 到 kⱼ 的最小期望搜索代價（含虛擬鍵 dᵢ₋₁ 到 dⱼ）。

$$w[i,j] = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l$$

$$e[i,j] = \min_{i \leq r \leq j} \{ e[i, r-1] + e[r+1, j] + w[i,j] \}$$

**邊界**：e[i, i-1] = qᵢ₋₁

**演算法**：Bottom-up 填表，按照 j-i（子問題長度）從 0 到 n 填。

**時間複雜度**：O(n³)（Knuth 優化可到 O(n²)）

對於給定的 7 個 key，p = {0.04, 0.06, 0.08, 0.02, 0.10, 0.12, 0.14}, q = {0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05}：

需要填 8×8 的 e 和 w 表。最終 e[1,7] 即為最小期望代價。

$$\boxed{O(n^3) \text{ — DP: } e[i,j] = \min_r\{e[i,r-1] + e[r+1,j] + w[i,j]\}}$$

**關鍵觀念**：選擇根節點 r 時，左右子樹深度各加 1，期望代價增加 w[i,j]。

---

## 題目 B3（蔡欣穆 100-1 期中 P7）

N cities on north bank (n₁,...,nₙ) and south bank (s₁,...,sₙ). Bridge between nᵢ and sᵢ. Maximize bridges without crossing.

### 詳解

**轉化為 LIS（Longest Increasing Subsequence）**：

1. 將城市按北岸座標排序：得到 (n_{π(1)}, s_{π(1)}), (n_{π(2)}, s_{π(2)}), ..., (n_{π(N)}, s_{π(N)})
   其中 n_{π(1)} < n_{π(2)} < ... < n_{π(N)}

2. 兩座橋 (nᵢ, sᵢ) 和 (nⱼ, sⱼ) 不交叉 ⟺ nᵢ < nⱼ 且 sᵢ < sⱼ（或反向）

3. 北岸已排序後，不交叉等價於南岸座標也遞增。

4. 問題化為：在序列 s_{π(1)}, s_{π(2)}, ..., s_{π(N)} 中找 **LIS**。

**LIS DP**：

$$dp[i] = \max_{j < i, s_{\pi(j)} < s_{\pi(i)}} dp[j] + 1$$

邊界：dp[i] = 1（只選自己）

答案 = max{dp[i]}

**時間複雜度**：
- 排序：O(N log N)
- DP（naive）：O(N²)
- DP + Binary Search（patience sorting）：**O(N log N)**

$$\boxed{O(N \log N) \text{ — 按北岸排序後，找南岸序列的 LIS}}$$

---

## 題目 B4（蔡欣穆 100-1 期中 P8）

Cache management: furthest-in-future strategy. Cache size k, request sequence r₁,...,rₙ.

(1) Write pseudocode and analyze running time.
(2) Show optimal substructure.
(3) Prove furthest-in-future produces minimum cache misses.

### 詳解

**(1) Pseudocode**：

```
FurthestInFuture(r[1..n], k):
  cache = ∅
  misses = 0
  for i = 1 to n:
    if r[i] ∈ cache:
      continue     // cache hit
    misses++
    if |cache| < k:
      cache.add(r[i])
    else:
      // Find item in cache used furthest in future
      victim = argmax_{x ∈ cache} NextUse(x, i, r)
      // NextUse(x, i, r) = min{j > i : r[j] = x}, or ∞ if none
      cache.remove(victim)
      cache.add(r[i])
  return misses
```

**時間**：O(nk) per eviction（找最遠使用的 item），總共 O(n²k) 最壞。可用 priority queue 優化到 O(n log k)。

**(2) Optimal substructure**：

令 OPT(i, C) = 從第 i 個請求開始，cache 狀態為 C 時的最少 miss 數。

$$OPT(i, C) = \begin{cases} OPT(i+1, C) & \text{if } r_i \in C \\ 1 + \min_{x \in C} OPT(i+1, C \setminus \{x\} \cup \{r_i\}) & \text{if } r_i \notin C, |C|=k \end{cases}$$

**(3) 正確性證明**（Exchange Argument）：

設 S* 是最優解，S 是 furthest-in-future 的解。若 S ≠ S*，找到第一次它們不同的 eviction。S 驅逐了 x（最遠未來使用），S* 驅逐了 y（y 的下次使用比 x 早）。

可以修改 S* 使其在此步也驅逐 x，且不增加 miss 數：在 x 下次被需要之前，y 一定先被需要（因為 y 的下次使用更早）。交換驅逐決策不會增加 miss。

歸納地，可以把 S* 逐步轉化為 S 而不增加 miss，故 S 也是最優。

$$\boxed{\text{Furthest-in-future: 驅逐未來最晚使用的元素，Exchange Argument 證明最優}}$$

---

## 題目 B5（蔡欣穆 101-1 期中 P3）

Convert a string to a palindrome with minimum number of insertions.

Example: "abcd" → 3 insertions → "abcdcba"

(1) Write recurrences.
(2) Prove optimal substructure.
(3) DP algorithm and time complexity.

### 詳解

**(1) 遞迴式**：

令 dp[i][j] = 將 S[i..j] 變成回文的最少插入次數。

$$dp[i][j] = \begin{cases} 0 & \text{if } i \geq j \\ dp[i+1][j-1] & \text{if } S[i] = S[j] \\ \min(dp[i+1][j], dp[i][j-1]) + 1 & \text{if } S[i] \neq S[j] \end{cases}$$

- S[i] = S[j]：首尾相同，自然配對，處理內部
- S[i] ≠ S[j]：
  - 在右邊插入 S[i]：匹配左端 → dp[i+1][j] + 1
  - 在左邊插入 S[j]：匹配右端 → dp[i][j-1] + 1

**(2) Optimal Substructure 證明**：

設 S[i..j] 的最優解需要 k 次插入，產生回文 P。

- 若 S[i] = S[j]：P 的首尾都是 S[i]，去掉首尾後 P' 是 S[i+1..j-1] 的回文，P' 需要 k 次插入。若存在更少插入的方案 k' < k 把 S[i+1..j-1] 變回文，則加上 S[i] 的配對就得到 k' 次的方案，矛盾。
- 若 S[i] ≠ S[j]：P 的首字元和尾字元相同，必有一端是插入的。

**(3) DP 演算法**：

Bottom-up：按照 j-i（子字串長度）從小到大填表。

**時間**：O(n²) 狀態，O(1) 轉移 = **O(n²)**

**空間**：O(n²)，可優化到 O(n)

$$\boxed{dp[i][j] = \begin{cases} dp[i+1][j-1] & S[i]=S[j] \\ \min(dp[i+1][j], dp[i][j-1])+1 & S[i] \neq S[j] \end{cases}, \quad O(n^2)}$$

---

## 題目 B6（蔡欣穆 101-1 期中 P4）

n people cross a bridge at night. At most 2 people at a time, need flashlight (only one). Time = max of the two. Minimize total time.

### 詳解

**經典問題**：令 a₁ ≤ a₂ ≤ ... ≤ aₙ 為排序後的過橋時間。

**Greedy 策略**（n ≥ 4 時交替使用）：

每次送兩個最慢的過橋，有兩種策略：

**策略 A**（最快帶最慢）：a₁ 帶 aₙ 過去，a₁ 回來，a₁ 帶 aₙ₋₁ 過去，a₁ 回來
- Cost = aₙ + a₁ + aₙ₋₁ + a₁

**策略 B**（最快帶次快，次快帶兩慢）：a₁ 和 a₂ 先過，a₁ 回來，aₙ₋₁ 和 aₙ 過，a₂ 回來
- Cost = a₂ + a₁ + aₙ + a₂

每次送走兩個最慢的（n, n-1），選 A 和 B 中較小的。

**DP 定義**：dp[i] = 送走最慢的 n-i 人（剩 i 人在起點）的最小時間。

$$dp[i] = dp[i+2] + \min \begin{cases} 2a_1 + a_i + a_{i+1} & \text{（策略 A）} \\ a_1 + 2a_2 + a_{i+1} & \text{（策略 B）} \end{cases}$$

邊界：dp[n] = 0, dp[n-1] = aₙ₋₁（1人直接過）, dp[n-2] = aₙ₋₂ + ...

**答案**：dp[2]（送到剩 2 人）+ a₂（最後兩人一起過）

$$\boxed{O(n \log n) \text{ (排序) + } O(n) \text{ (DP) — 每次比較策略 A vs B}}$$

---

## 題目 B7（蔡欣穆 102-1 期中 P3）

Making change with denominations 1, 5, 10, 50.

(1) Describe greedy algorithm and prove optimality for n=4, denominations {1,5,10,50}.
(2) Give denominations where greedy fails.

### 詳解

**(1) Greedy**：每次選最大面額的硬幣。

```
MakeChange(m, denominations = [50, 10, 5, 1]):
  coins = 0
  for d in denominations (descending):
    coins += m // d
    m = m % d
  return coins
```

**證明最優性**（對 {1, 5, 10, 50}）：

觀察最優解中的限制：
- 1 元硬幣最多 4 個（5 個 = 1 個 5 元）
- 5 元硬幣最多 1 個（2 個 = 1 個 10 元）
- 10 元硬幣最多 4 個（5 個 = 1 個 50 元）

因此在最優解中，非 50 元硬幣總值 < 50 + 10 + 5 = 65 < 100。

Greedy 先用盡量多的 50，剩下的 < 50，再用 10，剩下 < 10，再用 5，剩下 < 5，用 1。在每一層都不會超過上述限制，所以和最優解一致。

**(2) 反例**：denominations = {1, 3, 4}

找零 m = 6：
- Greedy: 4 + 1 + 1 = 3 枚
- Optimal: 3 + 3 = **2 枚**

$$\boxed{\text{Greedy 對 \{1,5,10,50\} 最優；反例：\{1,3,4\} 找零 6 元}}$$

---

## 題目 B8（蔡欣穆 102-1 期中 P4）

Copying Books: m books with pages p₁,...,pₘ, k scribes. Each scriber gets consecutive books. Minimize maximum pages assigned.

### 詳解

**子問題定義**：dp[i][j] = 前 i 本書由 j 個抄寫員處理的最小最大頁數。

**遞迴式**：

$$dp[i][j] = \min_{j-1 \leq l < i} \max\left(dp[l][j-1], \sum_{t=l+1}^{i} p_t\right)$$

第 j 個抄寫員負責書 l+1 到 i，前 l 本由 j-1 個人處理。

**邊界**：
- dp[i][1] = Σ_{t=1}^{i} pₜ（一個人抄所有）
- dp[0][j] = 0

**前綴和加速**：令 S[i] = Σ_{t=1}^{i} pₜ，則 Σ_{t=l+1}^{i} = S[i] - S[l]。

**時間複雜度**：O(m²k)（m 個 i，k 個 j，每次嘗試 m 個分割點）

**進一步優化**：可用 Binary Search + Greedy 做到 O(m log S)：

Binary Search 猜最大頁數 T，Greedy 驗證是否能用 k 個人完成（逐書分配直到超過 T 就開新人）。

$$\boxed{dp[i][j] = \min_{l} \max(dp[l][j-1], S[i]-S[l]), \quad O(m^2 k)}$$

---

## 題目 B9（蘇雅韻 100-1 期中 P4）

Stock trading: Given daily prices P₁,...,Pₙ. Find maximum profit (buy low, sell high).

(1) Design DP algorithm for max profit + which days.
(2) Time complexity.
(3) Prove optimal substructure.

### 詳解

**子問題**：S[i] = 結尾在第 i 天的最大子陣列和（等同 Kadane's Algorithm）。

定義 diff[i] = Pᵢ - Pᵢ₋₁（每日價差），問題轉化為找 diff 陣列的**最大子陣列和**。

**DP 遞迴式**：

$$S[i] = \max(S[i-1] + diff[i], \; diff[i]) = \max(S[i-1], 0) + diff[i]$$

邊界：S[1] = 0（或 diff[1] 不存在）

最大利潤 = max{S[i] : 1 ≤ i ≤ n}

**追蹤買賣日**：記錄每個 S[i] 的起始索引。當 S[i-1] < 0 時重新開始（buy = i-1），否則繼承。

**時間複雜度**：O(n)

**Optimal Substructure 證明**：

S[n] = max subarray ending at n。若最優子陣列為 diff[j..n]，則 diff[j..n-1] 也是結尾在 n-1 的最優（否則可替換得更好的 S[n]，矛盾）。

$$\boxed{S[i] = \max(S[i-1], 0) + diff[i], \quad O(n)}$$

---

## 題目 B10（張耀文 98-1 期中 P4）

Elephants and Lions play baseball series: first to win n games wins. P(Elephants win single game) = p. P(i,j) = prob Elephants win when they need i more wins and Lions need j more.

(1) Recurrence for P(i,j).
(2) P(Elephants win 3-game series) with p=0.4.
(3) DP algorithm.

### 詳解

**(1) 遞迴式**：

$$P(i, j) = \begin{cases} 1 & \text{if } i = 0 \text{ (Elephants already won)} \\ 0 & \text{if } j = 0 \text{ (Lions already won)} \\ p \cdot P(i-1, j) + q \cdot P(i, j-1) & \text{otherwise} \end{cases}$$

**(2)** 3 戰 2 勝制：需要 n = 2 勝。P(2, 2) with p = 0.4, q = 0.6。

$$P(1,1) = p \cdot P(0,1) + q \cdot P(1,0) = 0.4 \cdot 1 + 0.6 \cdot 0 = 0.4$$

$$P(1,2) = p \cdot P(0,2) + q \cdot P(1,1) = 0.4 \cdot 1 + 0.6 \cdot 0.4 = 0.64$$

$$P(2,1) = p \cdot P(1,1) + q \cdot P(2,0) = 0.4 \cdot 0.4 + 0.6 \cdot 0 = 0.16$$

$$P(2,2) = p \cdot P(1,2) + q \cdot P(2,1) = 0.4 \cdot 0.64 + 0.6 \cdot 0.16 = 0.352$$

$$\boxed{P(2,2) = 0.352}$$

**(3) DP 演算法**：

Bottom-up 填表，i 從 0 到 n，j 從 0 到 n。

**時間**：O(n²)，**空間**：O(n²)（可優化到 O(n)）

---

## 題目 B11（張耀文 98-1 期中 P5）

String shuffle: Z is a shuffle of X and Y if it interleaves characters maintaining left-to-right order.

(1) Recurrence.
(2) DP algorithm.

### 詳解

**(1) 遞迴式**：

dp[i][j] = True iff Z[1..i+j] is a shuffle of X[1..i] and Y[1..j]。

$$dp[i][j] = (dp[i-1][j] \land X[i] = Z[i+j]) \lor (dp[i][j-1] \land Y[j] = Z[i+j])$$

邊界：dp[0][0] = True

**(2) DP 演算法**：

Bottom-up 填 (m+1) × (n+1) 表。

```
Is_Shuffle(X, Y, Z, m, n):
  if len(Z) ≠ m + n: return False
  dp[0][0] = True
  for i = 1 to m: dp[i][0] = dp[i-1][0] AND (X[i] == Z[i])
  for j = 1 to n: dp[0][j] = dp[0][j-1] AND (Y[j] == Z[j])
  for i = 1 to m:
    for j = 1 to n:
      dp[i][j] = (dp[i-1][j] AND X[i]==Z[i+j]) OR
                 (dp[i][j-1] AND Y[j]==Z[i+j])
  return dp[m][n]
```

**時間**：O(mn)，**空間**：O(mn)

$$\boxed{dp[i][j] = (dp[i-1][j] \land X_i=Z_{i+j}) \lor (dp[i][j-1] \land Y_j=Z_{i+j}), \quad O(mn)}$$

---

## 題目 B12（張耀文 97-1 期中 P7）

Wood-cutting: log of length L, n marks at d₁,...,dₙ. Cost of one cut at position in a log of length k is k dollars. Minimize total cost.

(1) Show different cut orders give different costs.
(2) Recurrence for c(i,j).
(3) Algorithm and time complexity.

### 詳解

**(1) 例子**：L = 10, marks at 2, 5.

- 先切 2：cost = 10（切 10 長木頭）+ 8（切 [2,10] 在 5 處）= 18
- 先切 5：cost = 10 + 5（切 [0,5] 在 2 處）= 15

**(2) 遞迴式**：

c(i, j) = 最小成本切 d_i 到 d_j 之間所有標記。

$$c(i, j) = \begin{cases} 0 & \text{if } j = i+1 \text{ (no marks between)} \\ \min_{i < m < j} \{c(i, m) + c(m, j)\} + (d_j - d_i) & \text{otherwise} \end{cases}$$

每次在位置 m 切，cost = 木頭長度 dⱼ - dᵢ，再分別處理兩段。

**(3) 演算法**：

用 d₀ = 0, d_{n+1} = L 作為邊界。

Bottom-up：按照 j-i（區間長度）從 2 到 n+1 填表。

**時間**：O(n³)（n+2 個端點，每個區間嘗試 O(n) 個切割位置）

$$\boxed{c(i,j) = \min_{i<m<j}\{c(i,m)+c(m,j)\} + (d_j - d_i), \quad O(n^3)}$$

---

## 題目 B13（蕭旭君 103-1 期中 P3）

Longest Path on DAG (grid graph): n×n grid with edges going down and right only. Has optimal substructure (unlike general longest path).

### 詳解

**一般圖中 Longest Path 沒有 optimal substructure**：

反例：考慮 s → a → b → t 和 s → b → a → t。s 到 t 的最長路經 s-a-b-t 時，s 到 b 走了 s-a-b。但 s 到 b 的最長路可能是 s-b（如果有直接邊且 s-b > s-a-b）。因為「簡單路徑」約束，選了 a 後就不能再用 a。

**Grid DAG 有 optimal substructure**：

子問題：dp[i][j] = 從 (1,1) 到 (i,j) 的最長路徑長。

$$dp[i][j] = \max \begin{cases} dp[i-1][j] + w((i-1,j) \to (i,j)) & \text{(from above)} \\ dp[i][j-1] + w((i,j-1) \to (i,j)) & \text{(from left)} \end{cases}$$

**為什麼 grid DAG 有而一般圖沒有？**

因為 grid DAG 中所有邊都往下或往右，所以**不可能有環**。任何從 (1,1) 到 (i,j) 的路徑都是簡單路徑（因為不可能回頭）。因此沒有「已使用節點」的約束衝突。

$$\boxed{\text{DAG 無環 → 所有路徑自然簡單 → optimal substructure 成立}}$$

---

## 題目 B14（蕭旭君 103-1 期中 P7）

Fair Division: Divide n gifts into two groups minimizing weight difference. Weights are positive integers. O(nS) time where S = total weight.

### 詳解

**轉化為 Subset Sum**：找一個子集使其和最接近 S/2。

**DP**：dp[j] = True iff 存在子集使得重量和為 j。

```
FairDivision(w[1..n], S):
  dp[0] = True
  dp[1..S] = False
  for i = 1 to n:
    for j = S down to w[i]:    // 倒序避免重複使用
      dp[j] = dp[j] OR dp[j - w[i]]
  // Find j closest to S/2 where dp[j] = True
  best = argmin_{j: dp[j]=True} |S - 2j|
  return |S - 2*best|
```

**時間**：O(nS)，**空間**：O(S)

**追蹤分組**：用額外陣列記錄每個 j 最後加入了哪個物品，回溯找出子集。

$$\boxed{O(nS) \text{ — Subset Sum DP，找最接近 S/2 的子集和}}$$

---

## 題目 B15（蘇雅韻 100-1 期中 P5）

Given array with n marked elements and number m. Find m subarrays to cover all marked elements with minimum total length.

### 詳解

**Greedy 策略**：

1. 找出所有標記元素的位置 i₁ < i₂ < ... < iₙ
2. 先用一個子陣列 [i₁, iₙ] 覆蓋所有元素（長度 = iₙ - i₁ + 1）
3. 在標記元素之間找 m-1 個**最大間隔**，切開

**具體做法**：

1. 計算相鄰標記元素間的間隔：gap[j] = i_{j+1} - i_j，j = 1,...,n-1
2. 排序所有 gap，取最大的 m-1 個間隔作為切割點
3. 在這些間隔處切斷，得到 m 段
4. 總長度 = (iₙ - i₁ + 1) - (m-1 個最大間隔之和) + (m-1)（因為每段首尾各含一個元素）

更精確地：
- 總長度 = Σ 每段長度 = Σ(段末 - 段首 + 1)
- = (iₙ - i₁ + n) - Σ(被切斷的 gap)

**時間**：O(n log n)（排序 gap）

**正確性**：切最大的 gap 節省最多長度。Exchange argument：若不切某個大 gap 而切小 gap，交換後總長度更小。

$$\boxed{O(n \log n) \text{ — 計算間隔後貪心切最大的 m-1 個 gap}}$$
