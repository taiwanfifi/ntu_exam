# 機率極限定理與不等式

> 本章是機率論的「大結局」——我們終於要回答一個根本問題：**當樣本數 n 很大時，到底會發生什麼事？**
>
> 這章的內容從「粗略的估計工具」（Markov、Chebyshev）到「精確的極限結果」（大數法則、CLT），是考試的重中之重。

---

## 本章基礎觀念（零基礎必讀）

### 為什麼需要學極限定理與不等式？

假設你完全不知道某個隨機變數服從什麼分布，只知道它的平均值和變異數。你能不能說些關於它的機率的事情？

答案是：可以！**機率不等式**（Markov、Chebyshev）就是這樣的工具——不需要知道分布的具體形狀，就能給出機率的上界或下界。

再進一步，如果你做很多次實驗取平均，結果會怎樣？**大數法則（LLN）**告訴你：平均值會穩定下來。**中央極限定理（CLT）**更厲害：不管原始分布長什麼樣，足夠多次的平均值都近似常態分布！

這些結果是整個統計學的地基——信賴區間、假設檢定、抽樣調查，全都建立在它們之上。

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| Markov 不等式 | Markov's Inequality | 只用期望值就能估計尾機率的上界 | 平均月薪 5 萬，月薪超過 50 萬的人最多 10% |
| Chebyshev 不等式 | Chebyshev's Inequality | 用期望值和變異數估計「偏離平均」的機率 | 考試平均 70 分、標準差 10 分，偏離 20 分以上的人最多 25% |
| 大數法則 | Law of Large Numbers (LLN) | 樣本平均值會趨近母體平均值 | 丟硬幣越多次，正面比例越接近 0.5 |
| 中央極限定理 | Central Limit Theorem (CLT) | n 夠大時，樣本平均近似常態分布 | 100 個骰子的點數和近似 Normal |
| 依機率收斂 | Convergence in Probability | 「偏離的機率趨近 0」 | WLLN 的結論 |
| 依分布收斂 | Convergence in Distribution | CDF 收斂 | CLT 的結論 |
| 連續性修正 | Continuity Correction | 用連續分布近似離散分布時的 ±0.5 修正 | Normal 近似 Binomial 時使用 |
| Chernoff Bound | Chernoff Bound | 用 MGF 得到指數級的尾機率估計 | 比 Chebyshev 精確得多的上界 |

### 前置知識

你需要先讀完：
- **prob_06**：熟悉期望值 $E[X]$、變異數 $\text{Var}(X)$、MGF $M(t) = E[e^{tX}]$
- **prob_04**：熟悉 Binomial、Normal 等常見分布

關鍵公式複習：
- $\text{Var}(X) = E[X^2] - (E[X])^2$
- $\text{Var}(\bar{X}_n) = \sigma^2/n$（i.i.d. 樣本平均的變異數）
- 標準常態 CDF：$\Phi(z) = P(Z \le z)$，$Z \sim N(0,1)$

---

## 1. Markov 不等式（Markov's Inequality）

### 1.1 陳述

設 X 是非負隨機變數（X ≥ 0），E[X] 存在，則對任意 a > 0：

$$
P(X \geq a) \leq \frac{E[X]}{a}
$$

### 1.2 從期望值定義推導

這個證明非常漂亮，從期望值的定義出發：

**Step 1**：因為 X ≥ 0，我們可以把期望值拆開：

$$
E[X] = \int_0^\infty x \, f_X(x) \, dx = \int_0^a x \, f_X(x) \, dx + \int_a^\infty x \, f_X(x) \, dx
$$

**Step 2**：因為 x ≥ 0，第一個積分 ≥ 0，所以：

$$
E[X] \geq \int_a^\infty x \, f_X(x) \, dx
$$

**Step 3**：在第二個積分的範圍裡，x ≥ a，所以 x 可以用 a 來下界：

$$
E[X] \geq \int_a^\infty a \, f_X(x) \, dx = a \int_a^\infty f_X(x) \, dx = a \cdot P(X \geq a)
$$

**Step 4**：整理得：

$$
P(X \geq a) \leq \frac{E[X]}{a} \qquad \blacksquare
$$

> **直覺理解**：如果一個非負隨機變數的平均值是 μ，那它「跑到」10μ 以上的機率最多是 1/10。平均薪水 5 萬的話，薪水超過 50 萬的人最多 10%。

> **數值範例：薪水的例子**
>
> 某公司員工的平均月薪 $E[X] = 5$ 萬元（月薪一定是非負的）。不知道薪水的分布。
>
> **問題 1**：月薪超過 20 萬的人最多佔多少比例？
>
> $$P(X \ge 20) \le \frac{E[X]}{20} = \frac{5}{20} = 0.25 = 25\%$$
>
> **問題 2**：月薪超過 50 萬的人最多佔多少比例？
>
> $$P(X \ge 50) \le \frac{5}{50} = 0.1 = 10\%$$
>
> **問題 3**：月薪超過 100 萬的人最多佔多少比例？
>
> $$P(X \ge 100) \le \frac{5}{100} = 0.05 = 5\%$$
>
> 注意：這些都是**上界**，實際比例可能更低。Markov 不等式的好處是完全不需要知道分布的形狀！

### 1.3 使用時機與限制

**使用時機**：
- 只知道 E[X]，不知道 Var(X) 時
- 需要一個快速、粗略的尾機率上界
- 作為推導其他不等式的基石（如 Chebyshev）

**限制**：
- 需要 X ≥ 0（非負）
- 給出的 bound 通常很鬆
- 不使用任何關於分布形狀的資訊

---

## 2. Chebyshev 不等式（Chebyshev's Inequality）

### 2.1 陳述

設 X 是隨機變數，E[X] = μ，Var(X) = σ² < ∞，則對任意 k > 0：

$$
P(|X - \mu| \geq k) \leq \frac{\sigma^2}{k^2}
$$

等價形式（令 k = tσ）：

$$
P(|X - \mu| \geq t\sigma) \leq \frac{1}{t^2}
$$

### 2.2 從 Markov 不等式推導

這是一個非常優雅的推導——把 Chebyshev 歸約到 Markov：

**Step 1**：注意到 |X - μ| ≥ k 等價於 (X - μ)² ≥ k²：

$$
P(|X - \mu| \geq k) = P\big((X - \mu)^2 \geq k^2\big)
$$

**Step 2**：Y = (X - μ)² 是非負隨機變數，直接套 Markov：

$$
P\big((X - \mu)^2 \geq k^2\big) \leq \frac{E[(X - \mu)^2]}{k^2} = \frac{\sigma^2}{k^2}
$$

就這麼簡單！ $\blacksquare$

### 2.3 使用時機

- 知道均值 μ 和變異數 σ² 但不知道具體分布
- 需要估計「距離均值多遠」的機率
- 推導弱大數法則（WLLN）

> **數值範例：考試成績的例子**
>
> 某考試的平均分數 $\mu = 70$，標準差 $\sigma = 10$（即 $\sigma^2 = 100$）。不知道成績的分布。
>
> **問題 1**：成績和平均值相差 20 分以上（即低於 50 或高於 90）的學生最多佔多少？
>
> $$P(|X - 70| \ge 20) \le \frac{\sigma^2}{20^2} = \frac{100}{400} = 0.25 = 25\%$$
>
> 或者用 $k\sigma$ 的形式：$20 = 2\sigma$，所以 $P(|X-\mu| \ge 2\sigma) \le \frac{1}{4} = 25\%$
>
> **問題 2**：成績在 40 到 100 之間的學生至少佔多少？
>
> $|X - 70| < 30 = 3\sigma$
>
> $$P(|X - 70| \ge 30) \le \frac{1}{9} \approx 11.1\%$$
>
> 所以 $P(40 \le X \le 100) \ge 1 - \frac{1}{9} = \frac{8}{9} \approx 88.9\%$
>
> **和常態分布比較**：如果成績服從 $N(70, 100)$，$P(|X-70| \ge 20)$ 的真實值只有約 4.55%，遠小於 Chebyshev 給的 25%。Chebyshev 的上界很寬鬆，但它的優勢是**不需要假設分布**。

### 2.4 Chebyshev 告訴我們什麼

用 k = tσ 的版本：

| 距離均值 | 機率上界 |
|----------|----------|
| |X - μ| ≥ σ | ≤ 1 (沒用) |
| |X - μ| ≥ 2σ | ≤ 1/4 = 25% |
| |X - μ| ≥ 3σ | ≤ 1/9 ≈ 11.1% |
| |X - μ| ≥ 4σ | ≤ 1/16 = 6.25% |
| |X - μ| ≥ 10σ | ≤ 1/100 = 1% |

對比 Normal 分布：P(|Z| ≥ 2) ≈ 4.55%，P(|Z| ≥ 3) ≈ 0.27%。可見 Chebyshev 給的 bound 很寬鬆，但勝在**不需要知道分布**。

---

## 3. Chernoff Bound

### 3.1 想法

Markov 和 Chebyshev 用的是 1 階和 2 階動差。Chernoff bound 更聰明——它利用**動差生成函數（MGF）**來得到指數級的尾機率估計。

### 3.2 推導

對任意 t > 0：

**Step 1**：把事件轉換成指數形式：

$$
P(X \geq a) = P(e^{tX} \geq e^{ta}) \quad (\text{因為 } e^{t \cdot} \text{ 是遞增函數})
$$

**Step 2**：對 $Y = e^{tX}$（非負）套 Markov 不等式：

$$
P(e^{tX} \geq e^{ta}) \leq \frac{E[e^{tX}]}{e^{ta}} = \frac{M_X(t)}{e^{ta}} = e^{-ta} M_X(t)
$$

**Step 3**：因為對所有 t > 0 都成立，我們取最緊的那個：

$$
\boxed{P(X \geq a) \leq \min_{t > 0} e^{-ta} M_X(t)}
$$

這就是 **Chernoff bound**。

同理，對左尾（t < 0）：

$$
P(X \leq a) \leq \min_{t < 0} e^{-ta} M_X(t)
$$

### 3.3 為什麼 Chernoff bound 比較緊

Chebyshev 給的是 **多項式衰減**（~1/k²），而 Chernoff 給的是**指數衰減**（~e^{-ct}）。當 a 很大時，指數衰減遠快於多項式衰減，所以 Chernoff bound 通常緊得多。

---

## 4. 弱大數法則（Weak Law of Large Numbers, WLLN）

### 4.1 陳述

設 X₁, X₂, ..., Xₙ 是 i.i.d. 隨機變數，E[Xᵢ] = μ，Var(Xᵢ) = σ² < ∞。

令樣本均值 $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$，則對任意 ε > 0：

$$
\lim_{n \to \infty} P\big(|\bar{X}_n - \mu| \geq \varepsilon\big) = 0
$$

用符號寫就是 $\bar{X}_n \xrightarrow{P} \mu$（依機率收斂到 μ）。

### 4.2 用 Chebyshev 推導

**Step 1**：計算 $\bar{X}_n$ 的均值和變異數：

$$
E[\bar{X}_n] = \frac{1}{n}\sum_{i=1}^n E[X_i] = \frac{1}{n} \cdot n\mu = \mu
$$

$$
\text{Var}(\bar{X}_n) = \frac{1}{n^2}\sum_{i=1}^n \text{Var}(X_i) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}
$$

（用到了 X₁, ..., Xₙ 獨立所以變異數可加。）

**Step 2**：對 $\bar{X}_n$ 套 Chebyshev：

$$
P\big(|\bar{X}_n - \mu| \geq \varepsilon\big) \leq \frac{\text{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2}
$$

**Step 3**：當 n → ∞：

$$
\frac{\sigma^2}{n\varepsilon^2} \to 0
$$

因此 $P(|\bar{X}_n - \mu| \geq \varepsilon) \to 0$。$\blacksquare$

> **白話解讀**：丟銅板丟越多次，正面比例就越接近 1/2。這不是「一定等於」，而是「偏離的機率趨近 0」。

> **數值範例：丟硬幣看大數法則**
>
> 公平硬幣（$p = 0.5$），丟 $n$ 次，正面比例 $\hat{p} = \bar{X}_n$。
>
> 問：正面比例偏離 0.5 超過 0.05 的機率上界是多少？
>
> 由 Chebyshev：$P(|\hat{p} - 0.5| \ge 0.05) \le \frac{\text{Var}(\hat{p})}{0.05^2} = \frac{p(1-p)/n}{0.0025} = \frac{0.25/n}{0.0025} = \frac{100}{n}$
>
> | 丟 $n$ 次 | $P(\|\hat{p} - 0.5\| \ge 0.05) \le$ | 直覺 |
> |-----------|--------------------------------------|------|
> | n = 100 | 100/100 = 100%（無用） | 丟太少次，什麼都不保證 |
> | n = 1,000 | 100/1000 = 10% | 開始有用了 |
> | n = 10,000 | 100/10000 = 1% | 很有把握了 |
> | n = 100,000 | 100/100000 = 0.1% | 幾乎確定 |
>
> 可以看到，隨著 $n$ 增大，上界趨近 0。這就是大數法則！

---

## 5. 強大數法則（Strong Law of Large Numbers, SLLN）

### 5.1 陳述

設 X₁, X₂, ..., Xₙ 是 i.i.d. 隨機變數，E[|Xᵢ|] < ∞（只需要一階動差有限！），E[Xᵢ] = μ，則：

$$
P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1
$$

用符號寫就是 $\bar{X}_n \xrightarrow{a.s.} \mu$（幾乎必然收斂到 μ）。

### 5.2 WLLN vs SLLN 的區別

| | WLLN | SLLN |
|---|---|---|
| 結論 | 依機率收斂 | 幾乎必然收斂 |
| 條件 | 需要 Var 有限 (在 Chebyshev 證法中) | 只需要 E[\|X\|] < ∞ |
| 直覺 | 對每個固定 ε，「偏離 ε 以上」的機率 → 0 | 整條路徑最終都會穩定在 μ 附近 |
| 嚴格性 | 較弱 | 較強（SLLN ⟹ WLLN，反之不然）|

> **直覺**：WLLN 說的是「在任何一個時間點看，偏離的機率很小」。SLLN 說的是「跑了無窮久之後，這條路幾乎一定穩定了」。SLLN 排除了那些「偶爾還會大幅偏離」的樣本路徑。

### 5.3 嚴格證明概述（不需要背）

完整證明需要用到 Borel-Cantelli lemma 和截斷（truncation）技巧。核心想法：
1. 用四階動差 E[(X - μ)⁴] 來做更精細的估計
2. 證明 $\sum_n P(|\bar{X}_n - \mu| > \varepsilon) < \infty$
3. 由 Borel-Cantelli 第一引理得到 a.s. 收斂

---

## 6. 中央極限定理（Central Limit Theorem, CLT）

### 6.1 精確陳述（Lindeberg-Lévy CLT）

設 X₁, X₂, ..., Xₙ 是 i.i.d. 隨機變數，E[Xᵢ] = μ，Var(Xᵢ) = σ² ∈ (0, ∞)，則：

$$
Z_n = \frac{\sum_{i=1}^n X_i - n\mu}{\sigma\sqrt{n}} = \frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0, 1)
$$

也就是：

$$
\lim_{n \to \infty} P\left(\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \leq z\right) = \Phi(z)
$$

其中 Φ(z) 是標準常態的 CDF。

> **白話**：不管原始分布長什麼樣（只要均值和變異數有限），n 個 i.i.d. 隨機變數的和，標準化之後都會趨近 Normal！

> **數值範例：n 個骰子的和，如何趨近常態**
>
> 公平骰子：$\mu = 3.5$，$\sigma^2 = 35/12 \approx 2.917$
>
> 丟 $n$ 顆骰子，總和 $S_n = X_1 + \cdots + X_n$。
>
> | $n$ | $E[S_n]$ | $\text{SD}(S_n)$ | 分布形狀 |
> |-----|----------|------------------|----------|
> | 1 | 3.5 | 1.71 | 均勻（每個值等機率），完全不像 Normal |
> | 2 | 7 | 2.42 | 三角形分布（7 最多），開始有點像 |
> | 10 | 35 | 5.40 | 已經很像 Normal（肉眼看幾乎對稱的鐘形） |
> | 100 | 350 | 17.08 | 幾乎完美的 Normal |
>
> **具體計算（n = 100）**：
>
> 問：$P(S_{100} \ge 370)$ = ？
>
> $E[S_{100}] = 350$，$\text{SD}(S_{100}) = \sqrt{100 \times 35/12} = \sqrt{291.67} \approx 17.08$
>
> $$Z = \frac{370 - 350}{17.08} \approx 1.17$$
>
> $$P(S_{100} \ge 370) \approx 1 - \Phi(1.17) \approx 1 - 0.879 = 0.121$$
>
> 也就是說，100 顆骰子的點數和超過 370 的機率大約是 12.1%。注意我們完全沒有去算 Binomial 或其他複雜的精確分布——CLT 讓我們直接用常態分布近似！

### 6.2 標準化步驟（重要！）

這是考試最常用到的。設 Sₙ = X₁ + X₂ + ... + Xₙ，則：

- E[Sₙ] = nμ
- Var(Sₙ) = nσ²
- SD(Sₙ) = σ√n

標準化：

$$
Z_n = \frac{S_n - E[S_n]}{\sqrt{\text{Var}(S_n)}} = \frac{S_n - n\mu}{\sigma\sqrt{n}}
$$

等價地（用 $\bar{X}_n = S_n / n$）：

$$
Z_n = \frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}}
$$

所以 CLT 告訴我們：

$$
\bar{X}_n \stackrel{\text{approx}}{\sim} N\left(\mu, \frac{\sigma^2}{n}\right)
$$

$$
S_n \stackrel{\text{approx}}{\sim} N(n\mu, n\sigma^2)
$$

### 6.3 用 MGF 推導 CLT（sketch）

這個推導的核心想法是：如果 $Z_n$ 的 MGF 收斂到 $N(0,1)$ 的 MGF $e^{t^2/2}$，就能得到分布收斂。

**Step 1**：令 $Y_i = \frac{X_i - \mu}{\sigma}$（標準化），則 E[Yᵢ] = 0，Var(Yᵢ) = 1。

$$
Z_n = \frac{1}{\sqrt{n}} \sum_{i=1}^n Y_i
$$

**Step 2**：計算 $Z_n$ 的 MGF：

$$
M_{Z_n}(t) = E\left[e^{tZ_n}\right] = E\left[e^{\frac{t}{\sqrt{n}}\sum Y_i}\right] = \prod_{i=1}^n E\left[e^{\frac{t}{\sqrt{n}}Y_i}\right] = \left[M_Y\left(\frac{t}{\sqrt{n}}\right)\right]^n
$$

**Step 3**：Taylor 展開 $M_Y(s)$，其中 s = t/√n → 0：

$$
M_Y(s) = E[e^{sY}] = 1 + sE[Y] + \frac{s^2}{2}E[Y^2] + O(s^3)
$$

因為 E[Y] = 0，E[Y²] = 1：

$$
M_Y(s) = 1 + \frac{s^2}{2} + O(s^3) = 1 + \frac{t^2}{2n} + O\left(\frac{1}{n^{3/2}}\right)
$$

**Step 4**：取 n 次方：

$$
M_{Z_n}(t) = \left[1 + \frac{t^2}{2n} + O\left(\frac{1}{n^{3/2}}\right)\right]^n
$$

回憶 $(1 + a/n)^n \to e^a$，所以：

$$
M_{Z_n}(t) \to e^{t^2/2}
$$

這正是 N(0,1) 的 MGF！由 MGF 收斂定理（若 MGF 在 0 的鄰域收斂，則分布收斂），我們得到 $Z_n \xrightarrow{d} N(0,1)$。$\blacksquare$

### 6.4 何時可以用 CLT

**Rule of thumb**：
- 一般分布：**n ≥ 30** 就可以用 CLT 做近似
- 對稱分布（如 Uniform）：n ≥ 12 就已經很好
- 嚴重偏斜的分布（如 Exponential、Poisson with small λ）：可能需要 n ≥ 50 或更多
- Bernoulli(p)：當 np ≥ 5 且 n(1-p) ≥ 5 時可以用

**重要**：CLT 需要 σ² < ∞。如果分布的變異數不存在（如 Cauchy 分布），**CLT 不適用**！

### 6.5 CLT 的各種應用場景

1. **近似 Binomial**：Bin(n, p) 是 n 個 Bernoulli(p) 的和，可用 N(np, np(1-p)) 近似
2. **近似 Poisson**：Poisson(λ) 可以看成 n 個 Poisson(λ/n) 的和（當 λ 大時）用 N(λ, λ) 近似
3. **樣本均值的分布**：$\bar{X}_n \approx N(\mu, \sigma^2/n)$，這是統計推論的基礎
4. **信賴區間**：大樣本下的 CI 都是基於 CLT
5. **假設檢定**：大樣本 Z-test 就是靠 CLT

---

## 7. Normal 近似 Binomial + Continuity Correction

### 7.1 近似公式

若 X ~ Bin(n, p)，則當 np ≥ 5 且 n(1-p) ≥ 5 時：

$$
X \stackrel{\text{approx}}{\sim} N(np, \, np(1-p))
$$

$$
P(X \leq k) \approx \Phi\left(\frac{k - np}{\sqrt{np(1-p)}}\right)
$$

### 7.2 Continuity Correction（連續性修正）

**問題**：Binomial 是離散分布，Normal 是連續分布。直接近似會有系統性誤差。

**解決**：做 **±0.5 的修正**。

**原理推導**：離散隨機變數 X 取整數值 k 的機率 P(X = k) 對應的「面積」應該是從 k - 0.5 到 k + 0.5 的區間，所以：

$$
P(X = k) \approx \Phi\left(\frac{k + 0.5 - np}{\sqrt{np(1-p)}}\right) - \Phi\left(\frac{k - 0.5 - np}{\sqrt{np(1-p)}}\right)
$$

**常用修正規則**：

| 原始表達 | 修正後 |
|----------|--------|
| P(X ≤ k) | P(Y ≤ k + 0.5) |
| P(X < k) | P(Y ≤ k - 0.5) |
| P(X ≥ k) | P(Y ≥ k - 0.5) |
| P(X > k) | P(Y ≥ k + 0.5) |
| P(X = k) | P(k - 0.5 ≤ Y ≤ k + 0.5) |

其中 Y ~ N(np, np(1-p))。

> **記憶訣竅**：≤ k 的修正是 k + 0.5（往右推一點，把 k 完整包進去）；≥ k 的修正是 k - 0.5（往左推一點，把 k 完整包進去）。

> **數值範例：Normal 近似 Binomial 完整計算（n=100, p=0.5）**
>
> $X \sim \text{Bin}(100, 0.5)$。$\mu = np = 50$，$\sigma = \sqrt{np(1-p)} = \sqrt{25} = 5$。
>
> **問題 1**：$P(X = 55)$ = ？
>
> 用連續校正：$P(X = 55) \approx P(54.5 \le Y \le 55.5)$，$Y \sim N(50, 25)$。
>
> $$= \Phi\left(\frac{55.5-50}{5}\right) - \Phi\left(\frac{54.5-50}{5}\right) = \Phi(1.1) - \Phi(0.9)$$
> $$= 0.8643 - 0.8159 = 0.0484$$
>
> 精確值：$\binom{100}{55}(0.5)^{100} \approx 0.0485$。非常接近！
>
> **問題 2**：$P(X \ge 60)$ = ？
>
> 用連續校正：$P(X \ge 60) \approx P(Y \ge 59.5)$。
>
> $$= 1 - \Phi\left(\frac{59.5-50}{5}\right) = 1 - \Phi(1.9) = 1 - 0.9713 = 0.0287$$
>
> 不做連續校正：$P(Y \ge 60) = 1 - \Phi(2.0) = 1 - 0.9772 = 0.0228$。
>
> 精確值：$\approx 0.0284$。做了連續校正（0.0287）比沒做（0.0228）接近得多！
>
> **問題 3**：$P(45 \le X \le 55)$ = ？
>
> 用連續校正：$P(44.5 \le Y \le 55.5) = \Phi(1.1) - \Phi(-1.1) = 2 \times 0.8643 - 1 = 0.7286$
>
> 精確值：$\approx 0.7288$。驚人地準確！

---

## 8. 收斂的四種形式

### 8.1 四種收斂的定義

設 {Xₙ} 是一列隨機變數，X 是一個隨機變數：

**(1) 幾乎必然收斂（Almost Sure Convergence, a.s.）**

$$
X_n \xrightarrow{a.s.} X \iff P\left(\lim_{n \to \infty} X_n = X\right) = 1
$$

直覺：除了一個機率為 0 的集合之外，每條樣本路徑 Xₙ(ω) 都收斂到 X(ω)。

**(2) 依機率收斂（Convergence in Probability）**

$$
X_n \xrightarrow{P} X \iff \forall \varepsilon > 0, \; \lim_{n \to \infty} P(|X_n - X| > \varepsilon) = 0
$$

直覺：「跳出 ε 範圍的機率」趨近 0，但不保證路徑最終穩定。

**(3) 依分布收斂（Convergence in Distribution）**

$$
X_n \xrightarrow{d} X \iff \lim_{n \to \infty} F_{X_n}(x) = F_X(x) \;\; \text{at all continuity points of } F_X
$$

直覺：CDF 收斂。只要求「整體分布形狀」像，不要求逐點。

**(4) r 階動差收斂（Convergence in rth Mean / Lʳ Convergence）**

$$
X_n \xrightarrow{L^r} X \iff \lim_{n \to \infty} E[|X_n - X|^r] = 0
$$

最常見的是 r = 2（均方收斂，mean square convergence）：$E[(X_n - X)^2] \to 0$。

### 8.2 關係圖

```
                    a.s. convergence
                    ↓
L^r convergence → convergence in probability → convergence in distribution
```

精確地說：

1. **a.s. ⟹ in probability**（但反之不然）
2. **L^r ⟹ in probability**（但反之不然）
3. **in probability ⟹ in distribution**（但反之不然）
4. **a.s. 和 L^r 之間沒有一般的蘊含關係**

**特殊情況**：
- 如果 Xₙ →ᵈ c（常數），則 Xₙ →ᴾ c（分布收斂到常數等價於機率收斂到常數）
- 如果 Xₙ →ᴾ X 且 |Xₙ| ≤ Y（某個可積的 Y），則 Xₙ →^{L¹} X（Dominated Convergence）

### 8.3 反例（為什麼不能反推）

**in probability 不能推 a.s.**：

經典例子：在 [0,1] 上定義 Xₙ，讓它在越來越小但不斷移動的區間上等於 1。每個時間點 Xₙ = 1 的機率 → 0（in probability 收斂到 0），但對任何 ω，Xₙ(ω) 會無限多次等於 1（不 a.s. 收斂）。

**in distribution 不能推 in probability**：

Xₙ ~ N(0,1) for all n，X ~ N(0,1) 且 X 與所有 Xₙ 獨立。
那 Xₙ →ᵈ X（因為分布都一樣），但 Xₙ - X ~ N(0,2) 不趨近 0，所以不 in probability 收斂。

---

## 9. 完整計算範例

### 範例 1：用 Chebyshev 估計尾機率

**問題**：X 是一個隨機變數，E[X] = 10，Var(X) = 4。求 P(|X - 10| ≥ 6) 的上界。

**解答**：

直接套 Chebyshev：

$$
P(|X - 10| \geq 6) \leq \frac{\text{Var}(X)}{6^2} = \frac{4}{36} = \frac{1}{9} \approx 0.111
$$

所以 P(|X - 10| ≥ 6) ≤ 1/9。

**進一步**：也就是 P(X ≤ 4 或 X ≥ 16) ≤ 1/9。

**注意**：如果只問單邊，例如 P(X ≥ 16)，Chebyshev 給的是雙邊的 bound，所以最多能說 P(X ≥ 16) ≤ 1/9（不能直接除以 2，因為 Chebyshev 不假設對稱性）。

但如果額外知道分布對稱於 μ，則可以說 P(X ≥ 16) ≤ 1/18。

---

### 範例 2：用 CLT 求 Binomial 的近似機率

**問題**：擲一個公正硬幣 100 次，求正面次數在 45 到 55 之間（含）的機率。

**解答**：

設 X ~ Bin(100, 0.5)。

**Step 1**：計算均值和標準差。
- μ = np = 100 × 0.5 = 50
- σ² = np(1-p) = 100 × 0.5 × 0.5 = 25
- σ = 5

**Step 2**：用 CLT + continuity correction：

$$
P(45 \leq X \leq 55) = P(44.5 \leq Y \leq 55.5)
$$

其中 Y ~ N(50, 25)。

**Step 3**：標準化：

$$
P\left(\frac{44.5 - 50}{5} \leq Z \leq \frac{55.5 - 50}{5}\right) = P(-1.1 \leq Z \leq 1.1)
$$

**Step 4**：查表：

$$
P(-1.1 \leq Z \leq 1.1) = 2\Phi(1.1) - 1 = 2(0.8643) - 1 = 0.7286
$$

**不做 continuity correction 的話**：

$$
P\left(\frac{45 - 50}{5} \leq Z \leq \frac{55 - 50}{5}\right) = P(-1 \leq Z \leq 1) = 0.6827
$$

精確值（用電腦算）約為 0.7288。可以看到做了 continuity correction 之後，近似值 0.7286 非常接近精確值！

---

### 範例 3：用 CLT 求樣本平均值的分布

**問題**：某工廠生產的零件重量 X ~ 某分布（不知道是什麼分布），已知 μ = 50g，σ = 2g。隨機抽 64 個零件，求樣本平均重量 $\bar{X}$ 超過 50.5g 的機率。

**解答**：

**Step 1**：n = 64 ≥ 30，可以用 CLT。

$$
\bar{X} \stackrel{\text{approx}}{\sim} N\left(\mu, \frac{\sigma^2}{n}\right) = N\left(50, \frac{4}{64}\right) = N(50, 0.0625)
$$

所以 $\bar{X}$ 的標準差 = σ/√n = 2/8 = 0.25。

**Step 2**：

$$
P(\bar{X} > 50.5) = P\left(Z > \frac{50.5 - 50}{0.25}\right) = P(Z > 2) = 1 - \Phi(2) = 1 - 0.9772 = 0.0228
$$

**答**：約 2.28%。

> **注意**：這裡我們完全不知道原始分布是什麼！但因為 n = 64 夠大，CLT 保證 $\bar{X}$ 近似 Normal。這就是 CLT 的強大之處。

---

### 範例 4：用 Chernoff Bound 做更緊的估計

**問題**：X₁, ..., Xₙ i.i.d. ~ Bernoulli(1/2)。用 Chernoff bound 估計 P(Sₙ ≥ 3n/4)，其中 Sₙ = X₁ + ... + Xₙ。

**解答**：

**Step 1**：先求 Bernoulli(1/2) 的 MGF：

$$
M_X(t) = E[e^{tX}] = \frac{1}{2}e^0 + \frac{1}{2}e^t = \frac{1 + e^t}{2}
$$

**Step 2**：$S_n$ 的 MGF：

$$
M_{S_n}(t) = \left(\frac{1 + e^t}{2}\right)^n
$$

**Step 3**：套 Chernoff bound（取 a = 3n/4）：

$$
P(S_n \geq 3n/4) \leq \min_{t > 0} e^{-t \cdot 3n/4} \left(\frac{1 + e^t}{2}\right)^n = \min_{t > 0} \left[\frac{(1 + e^t) \cdot e^{-3t/4}}{2}\right]^n
$$

**Step 4**：令 f(t) = (1 + eᵗ) · e^{-3t/4} / 2，對 t 微分求最小值。

$$
f(t) = \frac{e^{-3t/4} + e^{t/4}}{2}
$$

$$
f'(t) = \frac{-\frac{3}{4}e^{-3t/4} + \frac{1}{4}e^{t/4}}{2} = 0
$$

$$
\frac{1}{4}e^{t/4} = \frac{3}{4}e^{-3t/4} \implies e^t = 3 \implies t^* = \ln 3
$$

**Step 5**：代入 t* = ln 3：

$$
f(\ln 3) = \frac{e^{-3\ln 3/4} + e^{\ln 3/4}}{2} = \frac{3^{-3/4} + 3^{1/4}}{2}
$$

計算：
- $3^{1/4} \approx 1.3161$
- $3^{-3/4} = 1/3^{3/4} \approx 1/2.2795 \approx 0.4387$
- $f(\ln 3) = (0.4387 + 1.3161)/2 = 1.7548/2 = 0.8774$

因此：

$$
P(S_n \geq 3n/4) \leq (0.8774)^n
$$

**比較**：

- **Chebyshev**：$P(S_n \geq 3n/4) = P(S_n - n/2 \geq n/4) \leq P(|S_n - n/2| \geq n/4) \leq \frac{n/4}{(n/4)^2} = \frac{4}{n}$

  這是 O(1/n) 的衰減。

- **Chernoff**：$(0.8774)^n$ 是指數衰減，遠遠快於 1/n。

例如 n = 100：
- Chebyshev：≤ 4/100 = 0.04
- Chernoff：≤ (0.8774)^100 ≈ 2.1 × 10⁻⁶

Chernoff 緊了將近 **四個數量級**！

---

### 範例 5（bonus）：WLLN 的直接應用

**問題**：用隨機模擬估計 π。在單位正方形 [0,1]² 中均勻撒 n 個點，令 X 為落在以 (0,0) 為圓心、半徑 1 的四分之一圓內的點數。證明 4X/n 依機率收斂到 π。

**解答**：

設 Yᵢ = 1 如果第 i 個點落在四分之一圓內，否則 Yᵢ = 0。

則 Yᵢ ~ Bernoulli(p)，其中 p = 四分之一圓面積 / 正方形面積 = π/4。

X = Y₁ + Y₂ + ... + Yₙ，且 Y₁, ..., Yₙ i.i.d.。

由 WLLN：

$$
\frac{X}{n} = \bar{Y}_n \xrightarrow{P} E[Y_1] = p = \frac{\pi}{4}
$$

因此：

$$
\frac{4X}{n} \xrightarrow{P} 4 \cdot \frac{\pi}{4} = \pi \qquad \blacksquare
$$

---

## 10. 比較：Chebyshev vs CLT vs Chernoff

### 什麼時候用什麼

| 情境 | 推薦方法 | 原因 |
|------|----------|------|
| 只知道 μ 和 σ²，不知道分布 | Chebyshev | 不需要分布資訊 |
| n 夠大，要算具體的近似機率 | CLT | 給出精確的近似值，不只是 bound |
| 需要指數級的尾機率 bound | Chernoff | 比 Chebyshev 緊得多 |
| n 很小（< 30） | 精確計算或 Chebyshev | CLT 近似可能不準 |
| 要用在證明中 | 看需求 | Chebyshev 適合簡單的機率 bound，CLT 適合漸近分析 |

### 精確度比較

假設 X₁, ..., X₁₀₀ i.i.d. ~ Bernoulli(0.5)，S₁₀₀ = ΣXᵢ。

估計 P(S₁₀₀ ≥ 75)：

| 方法 | 估計值 | 說明 |
|------|--------|------|
| 精確值 | ≈ 5.96 × 10⁻⁷ | 用 Binomial CDF 精確計算 |
| Chebyshev | ≤ 0.04 | P(\|S - 50\| ≥ 25) ≤ 25/625 = 1/25 |
| CLT | ≈ 2.87 × 10⁻⁷ | Φ(-(75 - 50)/5) = Φ(-5) |
| Chernoff | ≈ 1.5 × 10⁻⁶ | 指數 bound |

觀察：
- Chebyshev 差了 5 個數量級
- CLT 非常接近精確值
- Chernoff 雖然是 upper bound，但只比精確值大約 2.5 倍

### 使用原則

1. **如果能用 CLT（n 夠大），優先用 CLT**——它給的是近似值，不是 bound，最有用
2. **如果需要嚴格的上界（如在證明中），用 Chernoff**——指數級的 bound
3. **如果什麼都不知道，只有均值和變異數，用 Chebyshev**——最通用但最鬆
4. **如果連變異數都不知道，只有均值且非負，用 Markov**——最後的手段

---

## 11. 常見陷阱

### 陷阱 1：CLT 的前提條件

CLT 要求 **σ² < ∞**。如果分布的變異數不存在（如 Cauchy 分布），CLT 不適用。

**Cauchy 是經典反例**：i.i.d. Cauchy 的樣本均值仍然是 Cauchy（不會「收斂到 Normal」），因為 Cauchy 的均值都不存在。

### 陷阱 2：CLT 給的是分布收斂，不是精確結果

$$
\bar{X}_n \sim N(\mu, \sigma^2/n) \quad \text{(錯！這是近似，不是精確)}
$$

$$
\bar{X}_n \stackrel{\text{approx}}{\sim} N(\mu, \sigma^2/n) \quad \text{(對！)}
$$

除非 Xᵢ 本身就是 Normal 的（此時 $\bar{X}_n$ 精確地是 Normal）。

### 陷阱 3：Chebyshev 是雙邊的

P(X ≥ μ + k) 和 P(X ≤ μ - k) 分別只是 P(|X - μ| ≥ k) 的一部分。Chebyshev 只能 bound 雙邊的尾，不能直接 bound 單邊。

如果用 Chebyshev bound 單邊，結果和 bound 雙邊一樣：P(X ≥ μ + k) ≤ P(|X - μ| ≥ k) ≤ σ²/k²。

（但有一個加強版 **Cantelli's inequality** 可以做單邊 bound：$P(X - \mu \geq k) \leq \frac{\sigma^2}{\sigma^2 + k^2}$，有些考試會考。）

### 陷阱 4：Continuity correction 的方向

P(X ≥ 10) 修正成 P(Y ≥ 9.5)，不是 10.5！

因為 X ≥ 10 包含 X = 10，而 X = 10 對應的區間是 [9.5, 10.5]，要整個包進去。

### 陷阱 5：收斂形式的蘊含方向

常見錯誤：「依分布收斂可以推出依機率收斂」——**錯**！

只有在收斂到**常數**時，依分布收斂才等價於依機率收斂。

### 陷阱 6：Chernoff bound 的 t 要取對方向

- 估計右尾 P(X ≥ a)：t > 0
- 估計左尾 P(X ≤ a)：t < 0

如果取錯方向，bound 會大於 1，毫無用處。

---

## 12. 章節總結

| 工具 | 需要知道 | 結果類型 | 精度 | 適用場景 |
|------|----------|----------|------|----------|
| Markov | E[X], X ≥ 0 | 上界 | 很鬆 | 最後手段 |
| Chebyshev | E[X], Var(X) | 上界 | 鬆 | 不知道分布 |
| Chernoff | MGF | 上界 | 緊（指數級）| 需要精確 bound |
| WLLN | μ, σ² | 收斂結論 | — | 理論保證 |
| SLLN | μ | 收斂結論 | — | 理論保證（更強）|
| CLT | μ, σ² | 近似分布 | 很好 | n 大時的實際計算 |

> **考試建議**：CLT 的計算是必考題，一定要熟練標準化步驟和 continuity correction。Chebyshev 的推導也常考。Chernoff bound 較進階，但理解推導思路很重要。四種收斂的關係是選擇題的最愛。

---

### 自我檢測

1. **Markov 基礎題**：某班學生每週花在社群媒體上的平均時間是 14 小時（$E[X] = 14$），求每週花超過 42 小時的學生最多佔多少比例？

2. **Chebyshev 計算題**：某零件長度 $\mu = 10$ cm，$\sigma = 0.5$ cm。不知道分布。求 $P(9 \le X \le 11)$ 的下界。

3. **CLT 計算題**：一台自動販賣機每罐飲料重量 $\mu = 350$ ml，$\sigma = 10$ ml。隨機抽 25 罐，求樣本平均重量低於 347 ml 的機率。

4. **Normal 近似 Binomial**：某藥物有效率 $p = 0.6$，對 200 位病人使用。求至少 130 人有效的機率（用連續性修正）。

<details><summary>參考答案</summary>

**1.** $P(X \ge 42) \le \frac{14}{42} = \frac{1}{3} \approx 33.3\%$

**2.** $|X - 10| < 1 = 2\sigma$。$P(|X-10| \ge 1) \le \frac{0.25}{1} = 0.25$。
所以 $P(9 \le X \le 11) \ge 1 - 0.25 = 0.75 = 75\%$。

**3.** $\bar{X} \sim N(350, 100/25) = N(350, 4)$ 近似。$\text{SD}(\bar{X}) = 2$。
$Z = \frac{347-350}{2} = -1.5$。$P(\bar{X} < 347) = \Phi(-1.5) = 0.0668 \approx 6.7\%$

**4.** $X \sim \text{Bin}(200, 0.6)$。$\mu = 120$，$\sigma = \sqrt{200 \times 0.6 \times 0.4} = \sqrt{48} \approx 6.928$。
$P(X \ge 130) \approx P(Y \ge 129.5)$（連續校正）。
$Z = \frac{129.5 - 120}{6.928} = \frac{9.5}{6.928} \approx 1.371$。
$P(Z \ge 1.371) = 1 - \Phi(1.371) \approx 1 - 0.9149 = 0.0851 \approx 8.5\%$

</details>
