# 進階隨機過程

> 這章進入「動態」的機率世界——隨機變數不再是孤立的，而是隨著時間演化的**隨機過程（Stochastic Process）**。Poisson Process 和 Markov Chain 是考試中出現頻率最高的兩類隨機過程。

---

## 1. Poisson Process

### 1.1 定義（三個條件）

一個計數過程 {N(t), t ≥ 0} 稱為**速率 λ 的 Poisson Process**，如果滿足：

1. **N(0) = 0**
2. **獨立增量（Independent Increments）**：不重疊的時間區間的計數彼此獨立。即若 s₁ < t₁ ≤ s₂ < t₂，則 N(t₁) - N(s₁) 和 N(t₂) - N(s₂) 獨立。
3. **平穩增量（Stationary Increments）且為 Poisson 分布**：N(t+s) - N(s) ~ Poisson(λt)，只和時間長度 t 有關，和起始時間 s 無關。

> **白話**：事件以固定平均速率 λ 發生，不同時段的事件互不影響，而且「什麼時候開始觀察」不重要。

### 1.2 基本性質

#### 計數分布

$$
P(N(t) = k) = \frac{(\lambda t)^k e^{-\lambda t}}{k!}, \quad k = 0, 1, 2, ...
$$

- E[N(t)] = λt
- Var(N(t)) = λt

#### 間隔分布（Inter-arrival Times）

設 Tₖ 是第 k-1 次和第 k 次事件之間的時間間隔。

**定理**：T₁, T₂, T₃, ... i.i.d. ~ Exp(λ)。

**推導**：

$$
P(T_1 > t) = P(N(t) = 0) = e^{-\lambda t}
$$

所以 T₁ 的 CDF 是 F(t) = 1 - e^{-λt}，即 T₁ ~ Exp(λ)。

由 memoryless property 和獨立增量，所有 Tₖ 都是 i.i.d. Exp(λ)。

#### 到達時間（Arrival Times / Waiting Times）

第 n 次事件的到達時間 Sₙ = T₁ + T₂ + ... + Tₙ。

因為 Tᵢ i.i.d. Exp(λ)，所以：

$$
S_n \sim \text{Gamma}(n, \lambda)
$$

$$
f_{S_n}(t) = \frac{\lambda^n t^{n-1} e^{-\lambda t}}{(n-1)!}, \quad t > 0
$$

- E[Sₙ] = n/λ
- Var(Sₙ) = n/λ²

### 1.3 合併與分拆（Merging and Splitting）

#### 合併（Superposition）

若 {N₁(t)} 和 {N₂(t)} 是獨立的 Poisson Process，速率分別為 λ₁ 和 λ₂，則：

$$
N(t) = N_1(t) + N_2(t) \text{ 是速率 } \lambda_1 + \lambda_2 \text{ 的 Poisson Process}
$$

**直覺**：兩個獨立的 Poisson 水龍頭的水滴合在一起，速率相加。

#### 分拆（Thinning / Splitting）

若 {N(t)} 是速率 λ 的 Poisson Process，每個事件以機率 p 被歸類為 Type 1、機率 1-p 歸為 Type 2（獨立分類），則：

- Type 1 的計數 {N₁(t)} 是速率 λp 的 Poisson Process
- Type 2 的計數 {N₂(t)} 是速率 λ(1-p) 的 Poisson Process
- **N₁(t) 和 N₂(t) 獨立**

### 1.4 條件分布：Order Statistics Property

**定理**：給定 N(t) = n，這 n 個事件的到達時間 S₁, S₂, ..., Sₙ 的條件分布等同於 n 個 i.i.d. Uniform(0, t) 的 **order statistics**。

也就是說：

$$
(S_1, S_2, ..., S_n) \mid N(t) = n \stackrel{d}{=} (U_{(1)}, U_{(2)}, ..., U_{(n)})
$$

其中 U₁, ..., Uₙ i.i.d. ~ Uniform(0, t)，U₍₁₎ ≤ U₍₂₎ ≤ ... ≤ U₍ₙ₎ 是排序後的值。

**推導素描**：

考慮 $P(S_1 \in ds_1, ..., S_n \in ds_n \mid N(t) = n)$。

利用 Poisson 過程的獨立平穩增量：

$$
= \frac{P(\text{分別在 } ds_1, ..., ds_n \text{ 各有一次事件，其餘無事件})}{P(N(t) = n)}
$$

分子 = $(\lambda ds_1)(\lambda ds_2) \cdots (\lambda ds_n) \cdot e^{-\lambda t}$

分母 = $e^{-\lambda t} (\lambda t)^n / n!$

$$
= \frac{\lambda^n \, ds_1 \cdots ds_n \cdot e^{-\lambda t}}{e^{-\lambda t}(\lambda t)^n / n!} = \frac{n!}{t^n} \, ds_1 \cdots ds_n
$$

這正是 n 個 Uniform(0, t) 的 order statistics 的聯合密度！

**應用**：知道 [0, t] 內有 n 次事件後，每次事件「均勻散佈」在 [0, t] 上（但要排序）。

### 1.5 計算範例

#### 範例 1：合併和分拆

**問題**：某咖啡店，男生顧客以 Poisson process 到達，速率 3 人/hr；女生顧客以獨立的 Poisson process 到達，速率 5 人/hr。

(a) 在 2 小時內恰好有 10 位顧客的機率。
(b) 已知第一位到達的顧客是女生的機率。
(c) 在 1 小時內男生多於 5 人的機率。

**解答**：

**(a)** 合併後總速率 λ = 3 + 5 = 8 人/hr。
2 小時內總人數 N(2) ~ Poisson(8 × 2) = Poisson(16)。

$$
P(N(2) = 10) = \frac{16^{10} e^{-16}}{10!} = \frac{16^{10}}{10!} e^{-16}
$$

計算：16¹⁰ = 1.0995 × 10¹², 10! = 3628800

$$
= \frac{1.0995 \times 10^{12}}{3.6288 \times 10^6} \times e^{-16} = 3.030 \times 10^5 \times 1.125 \times 10^{-7} \approx 0.0341
$$

**(b)** 設 T_M 和 T_F 分別是第一位男生和女生到達的時間。

T_M ~ Exp(3)，T_F ~ Exp(5)，獨立。

$$
P(\text{第一位是女生}) = P(T_F < T_M) = \frac{\lambda_F}{\lambda_M + \lambda_F} = \frac{5}{3 + 5} = \frac{5}{8}
$$

（這是 Exponential 的競爭性質：min(Exp(λ₁), Exp(λ₂)) 中，Exp(λᵢ) 勝出的機率是 λᵢ/(λ₁+λ₂)。）

**(c)** 男生在 1 小時的人數 ~ Poisson(3)。

$$
P(N_M(1) > 5) = 1 - \sum_{k=0}^{5} \frac{3^k e^{-3}}{k!}
$$

$$
= 1 - e^{-3}\left(1 + 3 + \frac{9}{2} + \frac{27}{6} + \frac{81}{24} + \frac{243}{120}\right)
$$

$$
= 1 - e^{-3}(1 + 3 + 4.5 + 4.5 + 3.375 + 2.025)
$$

$$
= 1 - e^{-3} \times 18.4 = 1 - 0.04979 \times 18.4 = 1 - 0.9161 = 0.0839
$$

---

#### 範例 2：條件分布

**問題**：顧客以 Poisson(λ = 4/hr) 到達商店。已知上午 9:00 到 11:00 之間恰好有 3 位顧客到達，求第二位到達的顧客在 9:30 之前到達的機率。

**解答**：

令 t = 2（小時）。Given N(2) = 3，三個到達時間的條件分布等同於 3 個 Uniform(0, 2) 的 order statistics。

設 U₁, U₂, U₃ i.i.d. ~ Uniform(0, 2)，我們要求 P(U₍₂₎ ≤ 0.5)。

U₍₂₎ ≤ 0.5 意味著至少 2 個 Uᵢ ≤ 0.5。

每個 Uᵢ ≤ 0.5 的機率是 p = 0.5/2 = 0.25。

令 K = #{Uᵢ ≤ 0.5}，K ~ Bin(3, 0.25)。

$$
P(U_{(2)} \leq 0.5) = P(K \geq 2) = \binom{3}{2}(0.25)^2(0.75)^1 + \binom{3}{3}(0.25)^3
$$

$$
= 3 \times 0.0625 \times 0.75 + 1 \times 0.015625
$$

$$
= 0.140625 + 0.015625 = 0.15625 = \frac{5}{32}
$$

---

## 2. Markov Chain

### 2.1 定義和 Markov Property

**定義**：{Xₙ, n = 0, 1, 2, ...} 是一個離散時間 Markov Chain（DTMC），如果對所有 n ≥ 0 和所有狀態 i₀, i₁, ..., iₙ, j：

$$
P(X_{n+1} = j \mid X_n = i_n, X_{n-1} = i_{n-1}, ..., X_0 = i_0) = P(X_{n+1} = j \mid X_n = i_n)
$$

這就是 **Markov Property（無記憶性）**：給定現在，未來和過去獨立。

> **白話**：「未來只和現在有關，和過去無關。」知道你現在在哪裡，就足夠預測下一步了。

### 2.2 轉移矩陣（Transition Matrix）

如果 Markov Chain 是**時齊（time-homogeneous）**的：

$$
p_{ij} = P(X_{n+1} = j \mid X_n = i) \quad \text{（不依賴 n）}
$$

轉移矩陣 $\mathbf{P}$：

$$
\mathbf{P} = \begin{pmatrix} p_{11} & p_{12} & \cdots \\ p_{21} & p_{22} & \cdots \\ \vdots & \vdots & \ddots \end{pmatrix}
$$

**性質**：
- 每個元素 pᵢⱼ ≥ 0
- 每一列（row）的和 = 1：$\sum_j p_{ij} = 1$（每一列代表「從狀態 i 出發」的所有可能）

### 2.3 n 步轉移機率

$$
p_{ij}^{(n)} = P(X_{m+n} = j \mid X_m = i)
$$

**Chapman-Kolmogorov 方程式**：

$$
p_{ij}^{(m+n)} = \sum_k p_{ik}^{(m)} \cdot p_{kj}^{(n)}
$$

矩陣形式：**P^(m+n) = P^(m) · P^(n)**。

特別地：**n 步轉移矩陣就是 P 的 n 次方 Pⁿ**。

$$
p_{ij}^{(n)} = (\mathbf{P}^n)_{ij}
$$

### 2.4 穩態分布（Stationary Distribution）

**定義**：機率向量 π = (π₁, π₂, ...) 稱為穩態分布，如果：

$$
\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi} \quad \text{且} \quad \sum_i \pi_i = 1, \; \pi_i \geq 0
$$

**直覺**：如果系統處於穩態分布 π，則經過一步轉移後，分布仍然是 π。系統達到「平衡」。

**求法步驟**：

1. 列方程式 πP = π（展開成每個狀態的等式）
2. 加上正規化條件 $\sum \pi_i = 1$
3. 解聯立方程組

> **技巧**：πP = π 意味著 π(P - I) = 0，但這組方程式的秩是 n-1（不滿秩），所以需要額外的正規化條件。

**存在性和唯一性**：如果 Markov Chain 是 **irreducible**（不可約）且 **positive recurrent**（正常返），則穩態分布存在且唯一。如果還是 **aperiodic**（非週期），則不管初始分布是什麼，長期分布都會收斂到 π。

### 2.5 狀態分類

#### Recurrent vs Transient

- **Recurrent（常返）**：從 i 出發，最終一定會回到 i（回訪機率 = 1）
- **Transient（暫態）**：從 i 出發，有正機率永遠不回到 i（回訪機率 < 1）

**判斷**：
- 有限狀態的 irreducible chain → 所有狀態都是 recurrent
- 如果 $\sum_{n=1}^\infty p_{ii}^{(n)} = \infty$ 則 i 是 recurrent
- 如果 $\sum_{n=1}^\infty p_{ii}^{(n)} < \infty$ 則 i 是 transient

#### Positive Recurrent vs Null Recurrent

- **Positive Recurrent（正常返）**：回訪的期望時間有限
- **Null Recurrent（零常返）**：一定會回來，但期望時間無限

有限狀態空間中，recurrent 等同 positive recurrent（不存在 null recurrent）。

#### Periodic vs Aperiodic

- **週期 d**：$d = \gcd\{n \geq 1 : p_{ii}^{(n)} > 0\}$
- **Aperiodic（非週期）**：d = 1
- **Periodic（週期的）**：d > 1

**例子**：在二部圖（bipartite graph）上的隨機遊走是週期 2 的（只能在奇數步和偶數步交替訪問兩組狀態）。

**判斷技巧**：如果某個狀態有 self-loop（pᵢᵢ > 0），則它是 aperiodic。

#### Ergodic

**Ergodic = Irreducible + Positive Recurrent + Aperiodic**

Ergodic chain 有唯一的穩態分布 π，且從任何初始狀態出發，長期平均都收斂到 π：

$$
\lim_{n \to \infty} p_{ij}^{(n)} = \pi_j \quad \forall i
$$

### 2.6 吸收態（Absorbing State）

**定義**：狀態 i 是吸收態，如果 pᵢᵢ = 1（進去就出不來）。

**吸收鏈（Absorbing Chain）**：一個 Markov Chain 如果
(1) 至少有一個吸收態
(2) 從任何非吸收態出發，都有正機率（可能經過多步）到達某個吸收態

#### 求吸收機率

設非吸收態集合為 {1, 2, ..., t}，吸收態集合為 {t+1, ..., s}。

令 aᵢ = P(被吸收態 j 吸收 | 起始於狀態 i)。

利用 first-step analysis：

$$
a_i = \sum_k p_{ik} \cdot a_k
$$

配合邊界條件（吸收態 j 的 aⱼ = 1，其他吸收態的 a = 0），解聯立方程式。

#### 求吸收時間

令 mᵢ = E[被吸收的步數 | 起始於狀態 i]。

$$
m_i = 1 + \sum_{k \in \text{non-absorbing}} p_{ik} \cdot m_k
$$

邊界條件：吸收態的 m = 0。

### 2.7 計算範例

#### 範例 1：求穩態分布

**問題**：天氣有三種狀態：晴(S)、陰(C)、雨(R)，轉移矩陣為：

$$
\mathbf{P} = \begin{pmatrix} 0.7 & 0.2 & 0.1 \\ 0.3 & 0.4 & 0.3 \\ 0.2 & 0.3 & 0.5 \end{pmatrix}
$$

（行：S, C, R；列：S, C, R）

求穩態分布 π = (π_S, π_C, π_R)。

**解答**：

列方程式 πP = π：

$$
\pi_S = 0.7\pi_S + 0.3\pi_C + 0.2\pi_R \quad \cdots (1)
$$
$$
\pi_C = 0.2\pi_S + 0.4\pi_C + 0.3\pi_R \quad \cdots (2)
$$
$$
\pi_R = 0.1\pi_S + 0.3\pi_C + 0.5\pi_R \quad \cdots (3)
$$
$$
\pi_S + \pi_C + \pi_R = 1 \quad \cdots (4)
$$

**整理 (1)**：$0.3\pi_S = 0.3\pi_C + 0.2\pi_R$，即 $3\pi_S = 3\pi_C + 2\pi_R \quad \cdots (1')$

**整理 (2)**：$0.6\pi_C = 0.2\pi_S + 0.3\pi_R$，即 $6\pi_C = 2\pi_S + 3\pi_R \quad \cdots (2')$

**從 (1')**：$\pi_R = \frac{3(\pi_S - \pi_C)}{2}$

**代入 (2')**：$6\pi_C = 2\pi_S + \frac{9(\pi_S - \pi_C)}{2}$

$$
12\pi_C = 4\pi_S + 9\pi_S - 9\pi_C
$$

$$
21\pi_C = 13\pi_S \implies \pi_C = \frac{13}{21}\pi_S
$$

$$
\pi_R = \frac{3(\pi_S - \frac{13}{21}\pi_S)}{2} = \frac{3 \cdot \frac{8}{21}\pi_S}{2} = \frac{24}{42}\pi_S = \frac{4}{7}\pi_S
$$

**代入 (4)**：

$$
\pi_S + \frac{13}{21}\pi_S + \frac{4}{7}\pi_S = 1
$$

$$
\pi_S\left(1 + \frac{13}{21} + \frac{12}{21}\right) = 1
$$

$$
\pi_S \cdot \frac{21 + 13 + 12}{21} = 1
$$

$$
\pi_S \cdot \frac{46}{21} = 1 \implies \pi_S = \frac{21}{46}
$$

$$
\pi_C = \frac{13}{21} \times \frac{21}{46} = \frac{13}{46}
$$

$$
\pi_R = \frac{4}{7} \times \frac{21}{46} = \frac{12}{46} = \frac{6}{23}
$$

**驗證**：$\frac{21}{46} + \frac{13}{46} + \frac{12}{46} = \frac{46}{46} = 1$ ✓

$$
\boxed{\boldsymbol{\pi} = \left(\frac{21}{46}, \frac{13}{46}, \frac{12}{46}\right) \approx (0.457, 0.283, 0.261)}
$$

**解讀**：長期來看，約 45.7% 的天數是晴天，28.3% 陰天，26.1% 雨天。

---

#### 範例 2：Gambler's Ruin

**問題**：賭徒有 i 元，每次賭注 1 元，贏的機率 p，輸的機率 q = 1-p。到達 N 元（贏光對方）或 0 元（破產）就停止。求破產機率。

（這是一個有兩個吸收態的 Markov Chain：0 和 N 是吸收態。）

**設定**：令 rᵢ = P(破產 | 起始資金 i)，i = 0, 1, ..., N。

邊界條件：r₀ = 1（已經破產），rₙ = 0（已經贏了）。

**First-step analysis**：

$$
r_i = p \cdot r_{i+1} + q \cdot r_{i-1}, \quad i = 1, 2, ..., N-1
$$

**求解**：

這是一個二階線性遞迴。重排為：

$$
p \cdot r_{i+1} - r_i + q \cdot r_{i-1} = 0
$$

因為 p + q = 1，可以寫成：

$$
p(r_{i+1} - r_i) = q(r_i - r_{i-1})
$$

令 $d_i = r_i - r_{i-1}$，則 $d_{i+1} = \frac{q}{p} d_i$，得到 $d_i = (q/p)^{i-1} d_1$。

**Case 1：p ≠ q（即 p ≠ 1/2）**

$$
r_i - r_0 = \sum_{k=1}^i d_k = d_1 \sum_{k=0}^{i-1} \left(\frac{q}{p}\right)^k = d_1 \cdot \frac{1 - (q/p)^i}{1 - q/p}
$$

因為 r₀ = 1：

$$
r_i = 1 + d_1 \cdot \frac{1 - (q/p)^i}{1 - q/p}
$$

用 rₙ = 0 求 d₁：

$$
0 = 1 + d_1 \cdot \frac{1 - (q/p)^N}{1 - q/p}
$$

$$
d_1 = -\frac{1 - q/p}{1 - (q/p)^N}
$$

代回：

$$
r_i = 1 - \frac{1 - (q/p)^i}{1 - (q/p)^N}
$$

$$
\boxed{r_i = \frac{(q/p)^i - (q/p)^N}{1 - (q/p)^N}} \quad (p \neq q)
$$

**Case 2：p = q = 1/2**

此時 q/p = 1，公比等於 1，$d_i = d_1$ for all i。

$$
r_i = 1 + i \cdot d_1
$$

由 rₙ = 0：$0 = 1 + N d_1$，得 $d_1 = -1/N$。

$$
\boxed{r_i = 1 - \frac{i}{N} = \frac{N - i}{N}} \quad (p = q = 1/2)
$$

**數值例子**：p = 0.4, q = 0.6, i = 5, N = 10。

q/p = 3/2 = 1.5

$$
r_5 = \frac{1.5^5 - 1.5^{10}}{1 - 1.5^{10}} = \frac{7.594 - 57.665}{1 - 57.665} = \frac{-50.071}{-56.665} \approx 0.884
$$

即使只差一半的錢（5 vs 10），只要 p < 0.5，破產機率就高達 88.4%！

**公平遊戲（p = 0.5）**：$r_5 = (10-5)/10 = 0.5$。一半一半。

---

## 3. Random Walk

### 3.1 一維簡單隨機遊走（Simple Random Walk）

**定義**：$S_n = X_1 + X_2 + ... + X_n$，其中 Xᵢ i.i.d.，P(Xᵢ = +1) = p，P(Xᵢ = -1) = q = 1-p。

$S_0 = 0$，Sₙ 是 n 步後的位置。

**基本性質**：
- E[Sₙ] = n(p - q) = n(2p - 1)
- Var(Sₙ) = 4npq
- p > 1/2：向右漂移（drift to +∞）
- p < 1/2：向左漂移（drift to -∞）
- p = 1/2：**對稱隨機遊走（symmetric random walk）**，E[Sₙ] = 0

### 3.2 對稱隨機遊走的性質（p = 1/2）

1. **Recurrent**：P(回到原點) = 1（一定會回來！）
2. **Null recurrent**：E[回到原點的時間] = ∞（但回來的期望時間是無限的！）
3. **回到原點的機率**：$P(S_{2n} = 0) = \binom{2n}{n} \left(\frac{1}{2}\right)^{2n} \sim \frac{1}{\sqrt{\pi n}}$（by Stirling）

> 這是一個很反直覺的結果：你一定會回到起點，但平均要花無限長時間才能回來。

### 3.3 Gambler's Ruin Problem（已在 Markov Chain 中推導）

見上一節範例 2。

### 3.4 期望遊戲時間

在 Gambler's Ruin 中，令 Dᵢ = E[遊戲結束的步數 | 起始資金 i]。

**遞推方程**：

$$
D_i = 1 + p \cdot D_{i+1} + q \cdot D_{i-1}, \quad i = 1, ..., N-1
$$

邊界：D₀ = Dₙ = 0。

**Case 1：p ≠ q**

$$
\boxed{D_i = \frac{i}{q - p} - \frac{N}{q - p} \cdot \frac{1 - (q/p)^i}{1 - (q/p)^N}}
$$

**推導**：

重排遞推式：$p \cdot D_{i+1} - D_i + q \cdot D_{i-1} = -1$

這是一個帶非齊次項的二階線性遞迴。

齊次解和 Gambler's Ruin 一樣。特解猜 Dᵢ = ci：

$$
p \cdot c(i+1) - ci + q \cdot c(i-1) = -1
$$
$$
ci(p + q) + c(p - q) - ci = -1
$$
$$
c(p - q) = -1 \implies c = \frac{1}{q - p}
$$

（需要 p ≠ q。）

所以通解 $D_i = \frac{i}{q-p} + A + B(q/p)^i$。

由 D₀ = 0：$A + B = 0$，即 B = -A。
由 Dₙ = 0：$\frac{N}{q-p} + A - A(q/p)^N = 0$。

$$
A = \frac{N/(q-p)}{(q/p)^N - 1}
$$

代回即得結果。

**Case 2：p = q = 1/2**

$$
\boxed{D_i = i(N - i)}
$$

**推導**：

當 p = q = 1/2 時，遞推式變成：

$$
\frac{1}{2}D_{i+1} - D_i + \frac{1}{2}D_{i-1} = -1
$$

即 $D_{i+1} - 2D_i + D_{i-1} = -2$（二階差分 = -2）。

這等價於 D 是一個開口向下的二次函數，邊界 D₀ = Dₙ = 0。

猜 Dᵢ = ai² + bi + c：

$(i+1)^2 - 2i^2 + (i-1)^2 = 2$，所以 a 的二階差分是 2a = -2，a = -1。

$D_i = -i^2 + bi$，D₀ = 0 ✓，Dₙ = -N² + bN = 0 ⟹ b = N。

$$
D_i = -i^2 + Ni = i(N - i)
$$

**數值例子**：p = 1/2, i = 5, N = 10。
D₅ = 5 × 5 = 25 步。

---

## 4. 資訊理論基礎

### 4.1 熵（Entropy）

**定義**：離散隨機變數 X 的熵：

$$
H(X) = -\sum_{x} p(x) \log p(x) = E[-\log p(X)]
$$

（convention：0 log 0 = 0。對數底通常用 2 或 e；用 2 時單位是 bits，用 e 時單位是 nats。）

**直覺**：H(X) 衡量 X 的「不確定性」或「資訊量」。

**性質**：
1. H(X) ≥ 0
2. 若 X 取 n 個值，H(X) ≤ log n（均勻分布時等號成立）
3. H(X) = 0 ⟺ X 是確定性的（某個值機率為 1）

**例子**：X ~ Bernoulli(p)

$$
H(X) = -p\log p - (1-p)\log(1-p)
$$

- p = 0 或 p = 1：H = 0（完全確定）
- p = 1/2：H = log 2 = 1 bit（最不確定）

### 4.2 聯合熵和條件熵

**聯合熵**：

$$
H(X, Y) = -\sum_{x,y} p(x,y) \log p(x,y)
$$

**條件熵**：

$$
H(Y|X) = -\sum_{x,y} p(x,y) \log p(y|x) = E[-\log p(Y|X)]
$$

**Chain rule**：

$$
H(X, Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)
$$

### 4.3 互資訊（Mutual Information）

**定義**：

$$
I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)
$$

**直覺**：I(X; Y) 衡量 X 和 Y 之間共享的資訊量。

**性質**：
1. I(X; Y) ≥ 0（非負性）
2. I(X; Y) = 0 ⟺ X ⊥ Y（獨立）
3. I(X; Y) = I(Y; X)（對稱性）
4. I(X; X) = H(X)

### 4.4 KL 散度（Kullback-Leibler Divergence）

**定義**：

$$
D_{KL}(p \| q) = \sum_x p(x) \log \frac{p(x)}{q(x)} = E_p\left[\log \frac{p(X)}{q(X)}\right]
$$

**性質**：
1. $D_{KL}(p \| q) \geq 0$（**Gibbs' inequality**）
2. $D_{KL}(p \| q) = 0 \iff p = q$
3. $D_{KL}(p \| q) \neq D_{KL}(q \| p)$（**不對稱！**不是距離）

**直覺**：KL 散度衡量用 q 來近似 p 時「損失了多少資訊」。

**與互資訊的關係**：

$$
I(X; Y) = D_{KL}(p(x,y) \| p(x)p(y))
$$

互資訊就是聯合分布和邊際乘積之間的 KL 散度。

**Gibbs' inequality 的推導**：

$$
D_{KL}(p \| q) = -\sum_x p(x) \log \frac{q(x)}{p(x)} \geq -\log\left(\sum_x p(x) \cdot \frac{q(x)}{p(x)}\right) = -\log\left(\sum_x q(x)\right) = -\log 1 = 0
$$

（用了 Jensen's inequality：因為 -log 是凸函數。）

### 4.5 H(g(X)) ≤ H(X) 的推導（Data Processing Inequality 的特例）

**定理**：如果 Y = g(X) 是 X 的函數，則 H(Y) ≤ H(X)，等號成立當且僅當 g 是一對一函數。

**推導**：

**Step 1**：因為 Y = g(X)，知道 X 就知道 Y，所以 H(Y|X) = 0。

**Step 2**：由 chain rule：

$$
H(X, Y) = H(X) + H(Y|X) = H(X) + 0 = H(X)
$$

**Step 3**：同時：

$$
H(X, Y) = H(Y) + H(X|Y)
$$

**Step 4**：因為 H(X|Y) ≥ 0：

$$
H(X) = H(Y) + H(X|Y) \geq H(Y)
$$

$$
\boxed{H(g(X)) = H(Y) \leq H(X)} \qquad \blacksquare
$$

**等號條件**：H(X|Y) = 0，即知道 Y 就能確定 X，也就是 g 是一對一的。

> **白話**：處理資料只會損失（或維持）資訊，不會增加資訊。你不可能靠「加工」讓資料變得更有資訊量。

---

## 5. 常見陷阱和比較

### 5.1 Poisson Process 的陷阱

**陷阱 1：非齊次 Poisson Process**

如果到達率 λ(t) 隨時間變化（如尖峰時段較高），就不是（齊次的）Poisson Process。此時 N(t₁, t₂) ~ Poisson(∫_{t₁}^{t₂} λ(s) ds)。

**陷阱 2：間隔不是 Exp 就不是 Poisson Process**

有些計數過程的間隔分布不是 Exponential（如 renewal process），此時不是 Poisson Process，不能套那些漂亮的性質。

**陷阱 3：合併時要求獨立**

兩個 Poisson Process 合併成 Poisson Process 需要它們**獨立**。如果不獨立，合併後不一定是 Poisson。

### 5.2 Markov Chain 的陷阱

**陷阱 1：穩態分布不代表收斂**

如果 chain 是 periodic 的（如週期 2），則 $P^n$ 不收斂，但穩態分布仍然存在！穩態分布是「時間平均」的意義，不一定是「極限分布」。只有 ergodic chain 才保證 P^n → π。

**陷阱 2：πP = π 的解不唯一（如果 chain 不是 irreducible）**

如果有多個 communicating class，每個 recurrent class 都有自己的穩態分布，整體的穩態分布是它們的凸組合（不唯一）。

**陷阱 3：轉移矩陣的方向**

有些教科書用「行向量 × 矩陣」（πP = π），有些用「矩陣 × 列向量」（Pᵀπ = π）。要注意自己用的是哪個 convention。

**本教材使用行向量 convention（πP = π）**，這也是台大最常見的用法。

### 5.3 Random Walk 的陷阱

**陷阱：一維對稱隨機遊走是 recurrent，但三維不是！**

- 一維（d=1）：recurrent ✓
- 二維（d=2）：recurrent ✓（Pólya 定理）
- 三維及以上（d≥3）：transient ✗

"A drunk man will find his way home, but a drunk bird may get lost forever."

### 5.4 資訊理論的陷阱

**陷阱 1：KL 散度不是距離**

$D_{KL}(p \| q) \neq D_{KL}(q \| p)$，也不滿足三角不等式。不要把它當作距離函數。

**陷阱 2：H(X) 只對離散隨機變數有「絕對」的意義**

連續型的 differential entropy h(X) = -∫ f(x) log f(x) dx 可以是負的，而且依賴坐標系的選擇。

### 5.5 各種隨機過程的比較

| | Poisson Process | Markov Chain | Random Walk |
|---|---|---|---|
| 時間 | 連續 | 離散 | 離散 |
| 狀態 | 離散（計數） | 離散（有限或可數） | 離散（整數格點） |
| 關鍵性質 | 獨立平穩增量 | Markov property | 獨立增量 |
| 間隔/步長分布 | Exp(λ) | 由轉移矩陣決定 | Bernoulli(±1) |
| 和 Markov Chain 的關係 | Poisson Process 是連續時間 Markov Chain 的特例 | — | Random Walk 是 Markov Chain 的特例 |

---

## 6. 額外範例：Markov Chain 的 First-Step Analysis

### 範例：兩步達到吸收態

**問題**：考慮以下四狀態的 Markov Chain：

- 狀態 1, 2 是暫態（transient）
- 狀態 3, 4 是吸收態

轉移矩陣：

$$
\mathbf{P} = \begin{pmatrix}
0 & 0.5 & 0.25 & 0.25 \\
0.5 & 0 & 0.25 & 0.25 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

(a) 從狀態 1 出發，最終被狀態 3 吸收的機率。
(b) 從狀態 1 出發，期望吸收步數。

**解答**：

**(a)** 令 a₁ = P(被狀態3吸收 | X₀ = 1)，a₂ = P(被狀態3吸收 | X₀ = 2)。

First-step analysis：

$$
a_1 = 0 \cdot a_1 + 0.5 \cdot a_2 + 0.25 \cdot 1 + 0.25 \cdot 0 = 0.5a_2 + 0.25
$$

$$
a_2 = 0.5 \cdot a_1 + 0 \cdot a_2 + 0.25 \cdot 1 + 0.25 \cdot 0 = 0.5a_1 + 0.25
$$

從第一式：$a_1 = 0.5a_2 + 0.25$

代入第二式：$a_2 = 0.5(0.5a_2 + 0.25) + 0.25 = 0.25a_2 + 0.125 + 0.25$

$0.75a_2 = 0.375$，$a_2 = 0.5$

$a_1 = 0.5 \times 0.5 + 0.25 = 0.5$

**答**：P(被狀態3吸收 | 起始於1) = 0.5。

由對稱性，被狀態4吸收的機率也是 0.5。✓

**(b)** 令 m₁, m₂ 為期望吸收步數。

$$
m_1 = 1 + 0 \cdot m_1 + 0.5 \cdot m_2 + 0.25 \cdot 0 + 0.25 \cdot 0 = 1 + 0.5m_2
$$

$$
m_2 = 1 + 0.5 \cdot m_1 + 0 \cdot m_2 + 0.25 \cdot 0 + 0.25 \cdot 0 = 1 + 0.5m_1
$$

從第一式：$m_1 = 1 + 0.5m_2$

代入第二式：$m_2 = 1 + 0.5(1 + 0.5m_2) = 1.5 + 0.25m_2$

$0.75m_2 = 1.5$，$m_2 = 2$

$m_1 = 1 + 0.5 \times 2 = 2$

**答**：E[吸收步數 | 起始於1] = 2 步。

---

## 7. 章節總結

| 主題 | 核心概念 | 常考題型 |
|------|----------|----------|
| Poisson Process | 三條件定義、間隔 Exp、合併分拆 | 計算到達機率、條件分布 |
| Markov Chain | 轉移矩陣、穩態分布、狀態分類 | 求 πP=π、吸收機率 |
| Random Walk | Gambler's Ruin | 破產機率公式推導 |
| 資訊理論 | H(X)、I(X;Y)、KL 散度 | 定義、性質、不等式 |

> **考試建議**：Poisson Process 的性質（合併、分拆、條件分布是 Uniform order statistics）是常考的觀念題。Markov Chain 求穩態分布和吸收機率是必備的計算技能。Gambler's Ruin 的公式推導雖然長，但思路固定，練幾次就熟了。資訊理論如果有出，通常是定義和基本不等式。
