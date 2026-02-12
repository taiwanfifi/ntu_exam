# 統計推論：MLE、假設檢定與信賴區間

> 從這章開始，我們從「已知分布求機率」轉向「從資料推回分布」。這就是**統計推論**的核心精神：**用樣本來了解母體**。

---

## 本章基礎觀念（零基礎必讀）

### 為什麼需要學統計推論？

前幾章我們學的都是「已知分布求機率」——例如，知道硬幣正面機率是 0.5，求丟 10 次出現 7 次正面的機率。

但現實中我們不知道正面機率是多少！我們只能丟很多次硬幣，觀察結果，然後**猜**正面機率是多少。這個「從數據反推參數」的過程，就是**統計推論**。

具體來說：
- **MLE（最大概似估計）**：「哪個參數值最可能產生我看到的這些數據？」
- **信賴區間**：「參數大概在什麼範圍內？」
- **假設檢定**：「這個新藥真的比舊藥好嗎？還是只是運氣？」

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 母體 | Population | 你感興趣的整體 | 全台灣人的身高 |
| 樣本 | Sample | 你實際收集到的數據 | 隨機抽 100 人量身高 |
| 統計量 | Statistic | 樣本的函數（不含未知參數） | 樣本平均身高 $\bar{X}$ |
| 估計量 | Estimator | 用來估計未知參數的統計量 | 用 $\bar{X}$ 來估計 $\mu$ |
| 概似函數 | Likelihood Function | 給定參數值，觀察到這組數據的機率（密度） | $L(p) = p^7(1-p)^3$ |
| MLE | Maximum Likelihood Estimator | 使概似函數最大的參數值 | 丟 10 次得 7 正 3 反，$\hat{p} = 0.7$ |
| 不偏估計 | Unbiased Estimator | 估計量的期望值等於真值 | $E[\bar{X}] = \mu$ |
| 信賴區間 | Confidence Interval | 用樣本構造的、有一定機率包含真值的區間 | $\bar{X} \pm 1.96\sigma/\sqrt{n}$ |
| 顯著水準 | Significance Level (α) | 「冤枉好人」的最大容許機率 | α = 0.05 表示最多 5% 機率犯錯 |
| p 值 | p-value | 「如果 H₀ 為真，觀察到這麼極端結果的機率」 | p = 0.03 < 0.05，拒絕 H₀ |
| Type I Error | Type I Error | 真的對卻說錯（冤枉好人） | 藥無效但判定有效 |
| Type II Error | Type II Error | 真的錯卻說對（放走壞人） | 藥有效但判定無效 |
| 檢定力 | Power | 正確拒絕錯誤 H₀ 的機率 | Power = 1 - β |

### 前置知識

你需要先讀完：
- **prob_01 ~ prob_06**：熟悉常見分布和期望值、變異數的計算
- **prob_07**：了解 CLT（中央極限定理），因為信賴區間和假設檢定大量使用

關鍵公式複習：
- 常態分布標準化：$Z = \frac{X - \mu}{\sigma} \sim N(0,1)$
- CLT：$\bar{X}_n \stackrel{\text{approx}}{\sim} N(\mu, \sigma^2/n)$（$n$ 夠大時）
- 常用 z 值：$z_{0.025} = 1.96$（95% CI），$z_{0.005} = 2.576$（99% CI）

---

## 1. 統計推論概述

### 1.1 基本架構

```
母體（Population）
  ↓  抽樣
樣本（Sample）：X₁, X₂, ..., Xₙ（i.i.d.）
  ↓  計算
統計量（Statistic）：T = g(X₁, ..., Xₙ)
  ↓  推論
對母體參數 θ 做結論
```

**關鍵定義**：

- **母體**：我們感興趣的整體，通常用一個分布 F(x; θ) 來描述
- **樣本**：從母體中隨機抽取的觀測值 X₁, ..., Xₙ，假設 i.i.d.
- **統計量**：樣本的函數 T(X₁, ..., Xₙ)，**不能含有未知參數 θ**
- **估計量（Estimator）**：用來估計 θ 的統計量，記為 $\hat{\theta}$

> **注意**：$\bar{X}$ 是統計量（只和樣本有關），但 $\bar{X} - \mu$ 不是統計量（因為 μ 是未知參數）。

### 1.2 統計推論的三大任務

1. **點估計（Point Estimation）**：給出 θ 的一個最佳猜測值 $\hat{\theta}$
2. **區間估計（Interval Estimation）**：給出 θ 的一個可信範圍 [L, U]
3. **假設檢定（Hypothesis Testing）**：判斷 θ 是否滿足某個條件

---

## 2. 點估計方法

### 2.1 動差法（Method of Moments, MoM）

#### 原理

把**母體動差**等於**樣本動差**，解出參數。

- 母體的第 k 階動差：$\mu_k' = E[X^k]$（是 θ 的函數）
- 樣本的第 k 階動差：$m_k' = \frac{1}{n}\sum_{i=1}^n X_i^k$

如果有 p 個未知參數，就列 p 個方程式：

$$
\mu_k'(\theta_1, ..., \theta_p) = m_k', \quad k = 1, 2, ..., p
$$

然後解出 $\hat{\theta}_1, ..., \hat{\theta}_p$。

#### 步驟

1. 計算 E[X], E[X²], ... 表示成參數的函數
2. 令 E[X] = $\bar{X}$，E[X²] = $\frac{1}{n}\sum X_i^2$，...
3. 解聯立方程式

#### 優缺點

**優點**：
- 概念簡單，計算通常不難
- 幾乎總是有解（只要動差存在）
- 得到的估計量通常是 consistent 的

**缺點**：
- 不一定是最有效的估計量
- 有時候估計值可能落在參數空間之外（如估計出負的變異數）
- 沒有利用完整的 likelihood 資訊

### 2.2 最大概似估計（Maximum Likelihood Estimation, MLE）

#### 原理

找到使「觀測到這組樣本的機率最大」的參數值。

**概似函數（Likelihood Function）**：

$$
L(\theta) = L(\theta \mid x_1, ..., x_n) = \prod_{i=1}^n f(x_i; \theta)
$$

其中 f 是 PDF（連續型）或 PMF（離散型）。

**MLE** 就是使 $L(\theta)$ 最大的 $\theta$：

$$
\hat{\theta}_{MLE} = \arg\max_\theta L(\theta)
$$

> **數值範例：丟硬幣的 MLE（最直覺的例子）**
>
> **場景**：你拿到一枚硬幣，不知道它的正面機率 $p$。你丟了 10 次，得到 **7 次正面、3 次反面**。$p$ 的 MLE 是什麼？
>
> **Step 1：寫出概似函數**。每次丟硬幣是獨立的 Bernoulli(p)。
>
> $$L(p) = p^7 (1-p)^3$$
>
> 這個函數告訴你：對於不同的 $p$ 值，觀察到「7 正 3 反」的可能性有多大。
>
> **Step 2：取 log**。
>
> $$\ell(p) = 7\ln p + 3\ln(1-p)$$
>
> **Step 3：微分 = 0**。
>
> $$\frac{d\ell}{dp} = \frac{7}{p} - \frac{3}{1-p} = 0$$
>
> $$\frac{7}{p} = \frac{3}{1-p} \implies 7(1-p) = 3p \implies 7 - 7p = 3p \implies 7 = 10p$$
>
> $$\hat{p}_{MLE} = \frac{7}{10} = 0.7$$
>
> **Step 4：確認是最大值**。
>
> $$\frac{d^2\ell}{dp^2} = -\frac{7}{p^2} - \frac{3}{(1-p)^2} < 0 \quad \checkmark$$
>
> **結論**：$\hat{p} = 0.7$。直覺上也很合理：10 次中有 7 次正面，最合理的猜測就是 $p = 7/10$。
>
> **一般結論**：$n$ 次中 $k$ 次正面，Bernoulli(p) 的 MLE 就是 $\hat{p} = k/n$（樣本比例）。

#### 完整步驟教學

**Step 1：寫出 Likelihood**

$$
L(\theta) = \prod_{i=1}^n f(x_i; \theta)
$$

**Step 2：取 log（得到 Log-likelihood）**

$$
\ell(\theta) = \ln L(\theta) = \sum_{i=1}^n \ln f(x_i; \theta)
$$

> 為什麼取 log？因為 (1) 把乘積變成求和，計算方便很多；(2) ln 是嚴格遞增函數，不改變最大值的位置。

**Step 3：微分 = 0（Score equation）**

$$
\frac{d\ell}{d\theta} = 0
$$

如果有多個參數，就對每個參數偏微分 = 0。

**Step 4：解方程式**

解出 $\hat{\theta}$，並確認這是**最大值**（二階微分 < 0，或用其他方法確認）。

**重要警告**：MLE 不一定在微分 = 0 的點！如果 likelihood 在參數空間的邊界達到最大值，微分可能不等於 0。（見範例 3：Uniform(0, θ)）

#### 優缺點

**優點**：
- **漸近有效（Asymptotically Efficient）**：大樣本下，MLE 的變異數達到 Cramér-Rao lower bound
- **漸近常態**：$\hat{\theta}_{MLE} \stackrel{\text{approx}}{\sim} N(\theta, I(\theta)^{-1}/n)$，其中 I(θ) 是 Fisher information
- **不變性（Invariance）**：如果 $\hat{\theta}$ 是 θ 的 MLE，則 g($\hat{\theta}$) 是 g(θ) 的 MLE
- 通常是 consistent 和 sufficient 的

**缺點**：
- 有時候計算困難（需要數值方法）
- 小樣本時可能有偏（biased）
- 需要假設正確的分布形式

### 2.3 MoM 和 MLE 的比較

| | MoM | MLE |
|---|---|---|
| 原理 | 母體動差 = 樣本動差 | 最大化 likelihood |
| 計算難度 | 通常較簡單 | 可能需要數值解 |
| 效率 | 不一定有效 | 漸近有效 |
| 不偏性 | 不一定 | 不一定（但漸近不偏）|
| 利用資訊量 | 只用到前幾階動差 | 用到完整的 likelihood |

**什麼時候結果一樣？**

- Normal(μ, σ²)：MoM 和 MLE 的 $\hat{\mu}$ 都是 $\bar{X}$
- Exponential(λ)：MoM 和 MLE 的 $\hat{\lambda}$ 都是 $1/\bar{X}$
- Poisson(λ)：MoM 和 MLE 的 $\hat{\lambda}$ 都是 $\bar{X}$
- Bernoulli(p)：MoM 和 MLE 的 $\hat{p}$ 都是 $\bar{X}$

**什麼時候結果不一樣？**

- Uniform(0, θ)：MoM 給 $\hat{\theta} = 2\bar{X}$，MLE 給 $\hat{\theta} = X_{(n)}$（最大值），完全不同！
- 一般來說，當 likelihood 不是 exponential family 的形式時，兩者容易不同。

---

## 3. 估計量的性質

### 3.1 不偏性（Unbiasedness）

**定義**：若 $E[\hat{\theta}] = \theta$，則稱 $\hat{\theta}$ 是 θ 的**不偏估計量（unbiased estimator）**。

**偏差**：$\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$

**常見例子**：
- $\bar{X}$ 是 μ 的不偏估計量：$E[\bar{X}] = \mu$ ✓
- $S^2 = \frac{1}{n-1}\sum(X_i - \bar{X})^2$ 是 σ² 的不偏估計量 ✓
- $\hat{\sigma}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2$ 是有偏的：$E[\hat{\sigma}^2] = \frac{n-1}{n}\sigma^2 \neq \sigma^2$ ✗

> **為什麼除以 n-1？** 因為用 $\bar{X}$ 代替 μ 時損失了一個自由度。$\sum(X_i - \bar{X})^2$ 的期望值是 (n-1)σ²，所以要除以 n-1 才是不偏的。

### 3.2 一致性（Consistency）

**定義**：若 $\hat{\theta}_n \xrightarrow{P} \theta$（依機率收斂），則 $\hat{\theta}_n$ 是 θ 的**一致估計量（consistent estimator）**。

**充分條件**（常用）：若 $E[\hat{\theta}_n] \to \theta$ 且 $\text{Var}(\hat{\theta}_n) \to 0$，則 $\hat{\theta}_n$ 是 consistent 的。

（這可以用 Chebyshev 不等式來證。）

### 3.3 有效性（Efficiency）

**Cramér-Rao Lower Bound (CRLB)**：

對任何不偏估計量 $\hat{\theta}$：

$$
\text{Var}(\hat{\theta}) \geq \frac{1}{nI(\theta)}
$$

其中 **Fisher Information**：

$$
I(\theta) = E\left[-\frac{\partial^2}{\partial\theta^2} \ln f(X; \theta)\right] = E\left[\left(\frac{\partial}{\partial\theta} \ln f(X; \theta)\right)^2\right]
$$

如果某個不偏估計量的變異數恰好等於 CRLB，就稱它是 **UMVUE（Uniformly Minimum Variance Unbiased Estimator）**，也就是最有效的不偏估計量。

### 3.4 均方誤差（MSE）

$$
\text{MSE}(\hat{\theta}) = E[(\hat{\theta} - \theta)^2] = \text{Var}(\hat{\theta}) + [\text{Bias}(\hat{\theta})]^2
$$

MSE 同時考慮了變異數和偏差。有時候一個有偏但低變異數的估計量，其 MSE 反而比不偏估計量小。

---

## 4. 信賴區間（Confidence Interval）

### 4.1 定義和直覺

**定義**：一個 100(1-α)% 信賴區間 [L, U] 是滿足以下條件的隨機區間：

$$
P(L \leq \theta \leq U) = 1 - \alpha
$$

其中 L 和 U 是樣本的函數（統計量），θ 是固定的未知參數。

**正確解讀（非常重要）**：

❌「θ 在 [L, U] 內的機率是 95%」——**錯！** θ 是固定的常數，不是隨機變數，它要嘛在區間裡，要嘛不在，沒有「機率」。

✅「如果我們用同樣的方法重複抽樣很多次，構造出很多個信賴區間，其中大約 95% 的區間會包含真正的 θ。」

> **直覺**：信賴區間描述的是**方法的可靠度**，不是某一次結果的不確定性。

### 4.2 正態母體的信賴區間

#### Case 1：σ² 已知

X₁, ..., Xₙ i.i.d. ~ N(μ, σ²)，σ² 已知，求 μ 的 CI。

**推導**：

$$
\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right) \implies Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0,1)
$$

$$
P\left(-z_{\alpha/2} \leq \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \leq z_{\alpha/2}\right) = 1 - \alpha
$$

整理（解出 μ 的不等式）：

$$
P\left(\bar{X} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \leq \mu \leq \bar{X} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right) = 1 - \alpha
$$

所以 **μ 的 100(1-α)% CI**：

$$
\boxed{\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}}
$$

常用值：z₀.₀₂₅ = 1.96（95% CI），z₀.₀₀₅ = 2.576（99% CI）。

#### Case 2：σ² 未知

用 S 代替 σ，但分布變成 t 分布：

$$
T = \frac{\bar{X} - \mu}{S/\sqrt{n}} \sim t_{n-1}
$$

其中 $S^2 = \frac{1}{n-1}\sum(X_i - \bar{X})^2$。

**μ 的 100(1-α)% CI**：

$$
\boxed{\bar{X} \pm t_{\alpha/2, n-1} \cdot \frac{S}{\sqrt{n}}}
$$

> 當 n 很大時（n ≥ 30），t 分布接近 N(0,1)，所以 $t_{\alpha/2, n-1} \approx z_{\alpha/2}$。

### 4.3 大樣本的信賴區間（用 CLT）

當 n 夠大時，**不管母體分布是什麼**，由 CLT：

$$
\frac{\bar{X} - \mu}{S/\sqrt{n}} \stackrel{\text{approx}}{\sim} N(0,1)
$$

所以大樣本下 μ 的近似 95% CI：

$$
\bar{X} \pm 1.96 \cdot \frac{S}{\sqrt{n}}
$$

---

## 5. 假設檢定（Hypothesis Testing）

### 5.1 基本概念

> **假設檢定的完整流程：用「藥物效果測試」的例子**
>
> **場景**：某舊藥治癒率為 60%。新藥宣稱治癒率更高。你對 100 位病人使用新藥，結果 70 人治癒。新藥真的比舊藥好嗎？
>
> **Step 1：設定假設**
> - $H_0: p = 0.6$（新藥和舊藥一樣，沒有改善）
> - $H_1: p > 0.6$（新藥比舊藥好，右尾檢定）
>
> **Step 2：選擇統計量**
> $\hat{p} = 70/100 = 0.7$。在 $H_0$ 下，$\hat{p} \approx N(0.6, \frac{0.6 \times 0.4}{100}) = N(0.6, 0.0024)$
> $Z = \frac{0.7 - 0.6}{\sqrt{0.0024}} = \frac{0.1}{0.04899} = 2.041$
>
> **Step 3：算 p-value**
> $\text{p-value} = P(Z \ge 2.041) = 1 - \Phi(2.041) \approx 1 - 0.9793 = 0.0207$
>
> **Step 4：做結論**
> p-value = 0.0207 < α = 0.05，**拒絕 $H_0$**。
> 結論：有足夠的統計證據顯示新藥治癒率高於 60%。
>
> **注意**：這不代表「新藥一定比舊藥好」。它只是說「如果新藥和舊藥一樣（p=0.6），觀察到 70% 或更高治癒率的機率只有 2%，這太不尋常了」。

> **Type I Error 和 Type II Error：法院判決的比喻**
>
> 想像假設檢定是一場審判：
> - **$H_0$**（虛無假設）= 被告無罪
> - **$H_1$**（對立假設）= 被告有罪
>
> | | 被告真的無罪 | 被告真的有罪 |
> |---|---|---|
> | **判無罪（不拒絕 $H_0$）** | 正確 ✓ | **Type II Error（放走壞人）β** |
> | **判有罪（拒絕 $H_0$）** | **Type I Error（冤枉好人）α** | 正確 ✓（Power = 1-β） |
>
> - **Type I Error（冤枉好人）**：藥其實無效，但我們錯誤地宣稱它有效。機率 = α（我們控制的，通常設 0.05）
> - **Type II Error（放走壞人）**：藥其實有效，但我們沒發現。機率 = β（通常無法直接控制，要靠增加樣本量來降低）
>
> 法律界寧可「放走壞人」也不要「冤枉好人」（寧縱勿枉）。統計學中也是：我們設定小的 α（如 0.05），優先控制「冤枉好人」的機率。

> **信賴區間的正確直覺**
>
> 常見的錯誤說法：「真值有 95% 的機率在這個區間裡」。
>
> **正確理解**：真值 $\theta$ 是一個固定的數（不是隨機的），它要嘛在區間裡，要嘛不在，沒有「95% 的機率」。
>
> 正確的解讀是：**如果我們用同樣的方法重複做 100 次實驗，每次都構造一個 95% 信賴區間，那麼大約有 95 個區間會包含真值，5 個不會。**
>
> 打個比方：信賴區間像是用套環遊戲套目標。你的「方法」（95% CI 公式）有 95% 的命中率。每次丟出去的圈圈（區間）不一定套中，但長期來看 95% 會套中。

**虛無假設 H₀**：我們想要挑戰的「現狀」（通常含等號）
**對立假設 H₁（或 Hₐ）**：我們想要證明的「新主張」

例如：
- H₀: μ = 100 vs H₁: μ ≠ 100（雙尾檢定）
- H₀: μ ≤ 100 vs H₁: μ > 100（右尾檢定）
- H₀: μ ≥ 100 vs H₁: μ < 100（左尾檢定）

### 5.2 兩類錯誤

| | H₀ 為真 | H₀ 為偽 |
|---|---|---|
| **不拒絕 H₀** | 正確（1-α） | Type II Error（β）|
| **拒絕 H₀** | Type I Error（α）| 正確（1-β，即 Power）|

- **α = P(拒絕 H₀ | H₀ 為真)**：顯著水準，由研究者事先設定（常用 0.05, 0.01）
- **β = P(不拒絕 H₀ | H₀ 為偽)**：和 H₁ 中的具體參數值有關
- **Power = 1 - β**：檢定力，越大越好

> **直覺**：α 是「冤枉好人」的機率，β 是「放走壞人」的機率。在司法上，α 對應「判無辜者有罪」，β 對應「判有罪者無罪」。

### 5.3 p-value

**定義**：在 H₀ 為真的假設下，觀察到「至少和實際觀察結果一樣極端」的結果的機率。

$$
\text{p-value} = P(\text{test statistic at least as extreme as observed} \mid H_0 \text{ true})
$$

**使用規則**：
- p-value ≤ α → 拒絕 H₀
- p-value > α → 不拒絕 H₀

> p-value 越小，反對 H₀ 的證據越強。但 p-value **不是** "H₀ 為真的機率"！

> **數值範例：p-value 的完整計算**
>
> **場景**：某燈泡工廠宣稱產品平均壽命 $\mu = 1000$ 小時，$\sigma = 100$ 小時（已知）。消費者團體抽了 $n = 36$ 個燈泡，測得 $\bar{x} = 975$ 小時。燈泡真的沒有 1000 小時嗎？
>
> $H_0: \mu = 1000$，$H_1: \mu < 1000$（左尾檢定，因為消費者懷疑壽命「不夠長」）
>
> **算 Z 值**：
> $$Z = \frac{975 - 1000}{100/\sqrt{36}} = \frac{-25}{16.67} = -1.5$$
>
> **算 p-value**（左尾）：
> $$\text{p-value} = P(Z \le -1.5) = \Phi(-1.5) = 0.0668$$
>
> **結論**：
> - 若 α = 0.05：p-value = 0.0668 > 0.05，**不拒絕 $H_0$**。證據不足以判定壽命低於 1000 小時。
> - 若 α = 0.10：p-value = 0.0668 < 0.10，**拒絕 $H_0$**。
>
> 可見，結論取決於你選的顯著水準 α！p-value 本身只是「證據強度」的量化指標。

### 5.4 假設檢定的完整步驟

1. **設定假設**：寫出 H₀ 和 H₁
2. **選擇檢定統計量**：根據問題特性選（Z, t, χ², F, ...）
3. **決定拒絕域**：根據顯著水準 α 和 H₁ 的方向
4. **計算統計量的值**：帶入樣本數據
5. **做出結論**：統計量落在拒絕域 → 拒絕 H₀；否則不拒絕

### 5.5 範例：Z-test

**問題**：已知某產品重量 σ = 2g。抽 25 個樣本，$\bar{x}$ = 50.8g。在 α = 0.05 下檢定 H₀: μ = 50 vs H₁: μ ≠ 50。

**Step 1**：H₀: μ = 50，H₁: μ ≠ 50（雙尾）

**Step 2**：檢定統計量：$Z = \frac{\bar{X} - \mu_0}{\sigma/\sqrt{n}}$

**Step 3**：拒絕域：|Z| > z₀.₀₂₅ = 1.96

**Step 4**：$Z = \frac{50.8 - 50}{2/\sqrt{25}} = \frac{0.8}{0.4} = 2.0$

**Step 5**：|Z| = 2.0 > 1.96，落在拒絕域，**拒絕 H₀**。

p-value = 2P(Z > 2.0) = 2(1 - 0.9772) = 2(0.0228) = 0.0456 < 0.05，同樣的結論。

---

## 6. 常見檢定的比較

| 檢定 | 適用情境 | 統計量 | 前提 |
|------|----------|--------|------|
| **Z-test** | σ 已知或大樣本 | $Z = \frac{\bar{X} - \mu_0}{\sigma/\sqrt{n}}$ | Normal 母體或 n 大（CLT）|
| **t-test** | σ 未知，小樣本 | $T = \frac{\bar{X} - \mu_0}{S/\sqrt{n}} \sim t_{n-1}$ | Normal 母體 |
| **χ²-test（變異數）** | 檢定 σ² | $\chi^2 = \frac{(n-1)S^2}{\sigma_0^2} \sim \chi^2_{n-1}$ | Normal 母體 |
| **χ²-test（適合度）** | 分布是否一致 | $\chi^2 = \sum\frac{(O_i - E_i)^2}{E_i}$ | 每個 Eᵢ ≥ 5 |
| **F-test** | 比較兩組變異數 | $F = S_1^2/S_2^2$ | 兩組都 Normal |

**選擇流程**：

1. 知道 σ 嗎？
   - 知道 → Z-test
   - 不知道 → 看 n 大不大
     - n ≥ 30 → Z-test（用 S 代替 σ）
     - n < 30 → t-test（需要假設 Normal）

2. 檢定的是什麼？
   - 均值 → Z or t
   - 變異數 → χ²
   - 兩組變異數比 → F
   - 分布形狀 → χ² 適合度

---

## 7. 完整計算範例

### 範例 1：Exponential 的 MLE

**問題**：X₁, ..., Xₙ i.i.d. ~ Exp(λ)，f(x; λ) = λe^{-λx}，x ≥ 0。求 λ 的 MLE。

**Step 1：Likelihood**

$$
L(\lambda) = \prod_{i=1}^n \lambda e^{-\lambda x_i} = \lambda^n \exp\left(-\lambda \sum_{i=1}^n x_i\right)
$$

**Step 2：Log-likelihood**

$$
\ell(\lambda) = n\ln\lambda - \lambda\sum_{i=1}^n x_i
$$

**Step 3：微分 = 0**

$$
\frac{d\ell}{d\lambda} = \frac{n}{\lambda} - \sum_{i=1}^n x_i = 0
$$

**Step 4：解出 λ**

$$
\frac{n}{\lambda} = \sum_{i=1}^n x_i \implies \hat{\lambda}_{MLE} = \frac{n}{\sum x_i} = \frac{1}{\bar{X}}
$$

**驗證是最大值**：

$$
\frac{d^2\ell}{d\lambda^2} = -\frac{n}{\lambda^2} < 0 \quad \checkmark
$$

**同場加映——MoM**：

E[X] = 1/λ，令 1/$\hat{\lambda}$ = $\bar{X}$，得 $\hat{\lambda}_{MoM} = 1/\bar{X}$。

**結論：MoM = MLE = 1/$\bar{X}$**，兩者一致。

---

### 範例 2：Normal 的 MoM 和 MLE

**問題**：X₁, ..., Xₙ i.i.d. ~ N(μ, σ²)，求 μ 和 σ² 的 MoM 和 MLE。

#### MoM

**一階動差**：$E[X] = \mu$，令 $\mu = \bar{X}$，得 $\hat{\mu}_{MoM} = \bar{X}$。

**二階動差**：$E[X^2] = \mu^2 + \sigma^2$，令 $\mu^2 + \sigma^2 = \frac{1}{n}\sum X_i^2$。

$$
\hat{\sigma}^2_{MoM} = \frac{1}{n}\sum X_i^2 - \bar{X}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2
$$

#### MLE

**Step 1：Likelihood**

$$
L(\mu, \sigma^2) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)
$$

**Step 2：Log-likelihood**

$$
\ell(\mu, \sigma^2) = -\frac{n}{2}\ln(2\pi) - \frac{n}{2}\ln\sigma^2 - \frac{1}{2\sigma^2}\sum(x_i - \mu)^2
$$

**Step 3：對 μ 微分 = 0**

$$
\frac{\partial\ell}{\partial\mu} = \frac{1}{\sigma^2}\sum(x_i - \mu) = 0 \implies \hat{\mu} = \bar{X}
$$

**Step 4：對 σ² 微分 = 0**（令 τ = σ²）

$$
\frac{\partial\ell}{\partial\tau} = -\frac{n}{2\tau} + \frac{1}{2\tau^2}\sum(x_i - \mu)^2 = 0
$$

$$
\frac{n}{2\tau} = \frac{\sum(x_i - \bar{x})^2}{2\tau^2} \implies \hat{\tau} = \hat{\sigma}^2 = \frac{1}{n}\sum(x_i - \bar{x})^2
$$

#### 比較

| | MoM | MLE |
|---|---|---|
| $\hat{\mu}$ | $\bar{X}$ | $\bar{X}$ |
| $\hat{\sigma}^2$ | $\frac{1}{n}\sum(X_i - \bar{X})^2$ | $\frac{1}{n}\sum(X_i - \bar{X})^2$ |

**結果完全一樣！** 但注意，兩者的 $\hat{\sigma}^2$ 都除以 n（不是 n-1），所以**都是有偏的**。

不偏版本是 $S^2 = \frac{1}{n-1}\sum(X_i - \bar{X})^2$。

---

### 範例 3：Uniform(0, θ) 的 MLE（重要！邊界解）

**問題**：X₁, ..., Xₙ i.i.d. ~ Uniform(0, θ)，f(x; θ) = 1/θ for 0 ≤ x ≤ θ。求 θ 的 MLE。

**Step 1：Likelihood**

$$
L(\theta) = \prod_{i=1}^n \frac{1}{\theta} \cdot I(0 \leq x_i \leq \theta) = \frac{1}{\theta^n} \cdot I(X_{(n)} \leq \theta)
$$

其中 $X_{(n)} = \max(X_1, ..., X_n)$ 是最大的觀測值，$I(\cdot)$ 是指示函數。

**Step 2：分析 L(θ) 的形狀**

- 如果 θ < X₍ₙ₎：L(θ) = 0（因為有觀測值超出 [0, θ]）
- 如果 θ ≥ X₍ₙ₎：L(θ) = 1/θⁿ，這是 θ 的遞減函數

所以 L(θ) 在 θ ≥ X₍ₙ₎ 的範圍內是遞減的，**最大值在 θ = X₍ₙ₎ 處取到**。

$$
\boxed{\hat{\theta}_{MLE} = X_{(n)} = \max(X_1, ..., X_n)}
$$

**注意**：這裡 dℓ/dθ = -n/θ < 0（在 θ > X₍ₙ₎ 時），微分永遠不等於 0！MLE 在**邊界**取到，不是在微分 = 0 的點。

**MoM 的結果**：

E[X] = θ/2，令 θ/2 = $\bar{X}$，得 $\hat{\theta}_{MoM} = 2\bar{X}$。

**比較**：

| | MLE | MoM |
|---|---|---|
| 估計值 | X₍ₙ₎ = max | 2$\bar{X}$ |
| 不偏？ | $E[X_{(n)}] = \frac{n}{n+1}\theta \neq \theta$，有偏 | $E[2\bar{X}] = 2 \cdot \theta/2 = \theta$，不偏 |
| MSE | $\frac{2\theta^2}{(n+1)(n+2)}$ | $\frac{\theta^2}{3n}$ |

當 n 夠大時，MLE 的 MSE 小得多（O(1/n²) vs O(1/n)），所以 **MLE 雖然有偏但更精確**。

若要不偏版的 MLE：$\frac{n+1}{n} X_{(n)}$ 是 θ 的不偏估計量。

---

### 範例 4：信賴區間和假設檢定

**問題**：某大學生的考試成績假設為 Normal。隨機抽 16 人，樣本均值 $\bar{x}$ = 72，樣本標準差 s = 8。

(a) 求 μ 的 95% 信賴區間。
(b) 在 α = 0.05 下檢定 H₀: μ = 75 vs H₁: μ ≠ 75。

**(a) 信賴區間**

σ 未知，n = 16 < 30，用 t 分布。

自由度 = n - 1 = 15，$t_{0.025, 15} = 2.131$。

$$
\bar{x} \pm t_{0.025, 15} \cdot \frac{s}{\sqrt{n}} = 72 \pm 2.131 \times \frac{8}{\sqrt{16}} = 72 \pm 2.131 \times 2 = 72 \pm 4.262
$$

**95% CI = [67.738, 76.262]**

**(b) 假設檢定**

**Step 1**：H₀: μ = 75，H₁: μ ≠ 75

**Step 2**：$T = \frac{\bar{X} - \mu_0}{S/\sqrt{n}} = \frac{72 - 75}{8/4} = \frac{-3}{2} = -1.5$

**Step 3**：拒絕域：|T| > t₀.₀₂₅,₁₅ = 2.131

**Step 4**：|T| = 1.5 < 2.131

**Step 5**：**不拒絕 H₀**。在 α = 0.05 下，沒有足夠證據顯示 μ ≠ 75。

**用 CI 驗證**：75 ∈ [67.738, 76.262]，μ₀ = 75 在 CI 內，所以不拒絕 H₀。✓

> **重要觀察**：信賴區間和假設檢定是一體兩面！μ₀ 在 95% CI 內 ⟺ 在 α = 0.05 下不拒絕 H₀。

---

### 範例 5：Poisson 的 MLE

**問題**：X₁, ..., Xₙ i.i.d. ~ Poisson(λ)，P(X = k) = e^{-λ}λᵏ/k!。求 λ 的 MLE。

**Step 1：Likelihood**

$$
L(\lambda) = \prod_{i=1}^n \frac{e^{-\lambda}\lambda^{x_i}}{x_i!} = \frac{e^{-n\lambda}\lambda^{\sum x_i}}{\prod x_i!}
$$

**Step 2：Log-likelihood**

$$
\ell(\lambda) = -n\lambda + \left(\sum x_i\right)\ln\lambda - \sum\ln(x_i!)
$$

**Step 3：微分 = 0**

$$
\frac{d\ell}{d\lambda} = -n + \frac{\sum x_i}{\lambda} = 0
$$

**Step 4：解出 λ**

$$
\hat{\lambda}_{MLE} = \frac{\sum x_i}{n} = \bar{X}
$$

**二階導數確認**：$d^2\ell/d\lambda^2 = -\sum x_i / \lambda^2 < 0$ ✓

---

## 8. 充分統計量（Sufficient Statistic）

### 8.1 定義

統計量 T = T(X₁, ..., Xₙ) 稱為 θ 的**充分統計量**，如果：

給定 T 的值之後，樣本的條件分布不依賴 θ。

也就是：$P(X_1, ..., X_n | T = t)$ 和 θ 無關。

**直覺**：T 把樣本中所有關於 θ 的資訊都「壓縮」進去了。知道 T 之後，不需要看原始樣本就能做和 θ 有關的所有推論。

### 8.2 Fisher-Neyman 分解定理

**定理**：T(X) 是 θ 的充分統計量，當且僅當 likelihood 可以分解為：

$$
L(\theta; x_1, ..., x_n) = g(T(x_1, ..., x_n); \theta) \cdot h(x_1, ..., x_n)
$$

其中：
- g 只透過 T 和 θ 有關
- h 和 θ 完全無關

**例子**：

(1) **Normal(μ, σ² known)**：

$$
L(\mu) = \left(\frac{1}{\sqrt{2\pi}\sigma}\right)^n \exp\left(-\frac{\sum(x_i - \mu)^2}{2\sigma^2}\right)
$$

展開 $\sum(x_i - \mu)^2 = \sum x_i^2 - 2\mu\sum x_i + n\mu^2$：

$$
L(\mu) = \underbrace{\exp\left(-\frac{-2\mu \cdot n\bar{x} + n\mu^2}{2\sigma^2}\right)}_{g(\bar{x}; \mu)} \cdot \underbrace{\left(\frac{1}{\sqrt{2\pi}\sigma}\right)^n \exp\left(-\frac{\sum x_i^2}{2\sigma^2}\right)}_{h(x_1, ..., x_n)}
$$

所以 $\bar{X}$ 是 μ 的充分統計量。

(2) **Uniform(0, θ)**：

$$
L(\theta) = \frac{1}{\theta^n} I(X_{(n)} \leq \theta) \cdot I(X_{(1)} \geq 0)
$$

$$
= \underbrace{\frac{1}{\theta^n} I(X_{(n)} \leq \theta)}_{g(X_{(n)}; \theta)} \cdot \underbrace{I(X_{(1)} \geq 0)}_{h(x_1, ..., x_n)}
$$

所以 $X_{(n)} = \max(X_i)$ 是 θ 的充分統計量。

---

## 9. 常見陷阱

### 陷阱 1：MLE 不一定在微分 = 0 處

Uniform(0, θ) 就是經典例子。在求 MLE 時，一定要先看看 likelihood 的定義域和形狀，不能無腦微分 = 0。

**什麼時候要小心**：
- 參數出現在分布的**支撐集（support）**中（如 Uniform 的端點）
- Likelihood 在邊界可能有最大值
- 指示函數（indicator function）使得 likelihood 不可微

### 陷阱 2：信賴區間的解讀

❌「我有 95% 的信心 μ 在 [67.7, 76.3] 內」——嚴格來說，這是 Bayesian 的語言。Frequentist 的正確說法是「如果重複抽樣，95% 的區間會包含 μ」。

但在考試和實務中，這個錯誤通常不扣分。不過台大的題目如果特別問「信賴區間的正確解讀」，就一定要寫正確版本。

### 陷阱 3：MLE 的不偏性

MLE 不一定是不偏的！例如：
- Normal 的 $\hat{\sigma}^2_{MLE} = \frac{1}{n}\sum(X_i - \bar{X})^2$，其 $E[\hat{\sigma}^2] = \frac{n-1}{n}\sigma^2 \neq \sigma^2$
- Uniform(0,θ) 的 $\hat{\theta}_{MLE} = X_{(n)}$，其 $E[X_{(n)}] = \frac{n}{n+1}\theta \neq \theta$

不過 MLE 在大樣本下是**漸近不偏**的（bias → 0 as n → ∞）。

### 陷阱 4：t-test 需要 Normal 假設

當 n 小的時候，t-test 的有效性依賴於母體是 Normal 分布。如果母體明顯非 Normal（如嚴重偏斜），小樣本的 t-test 可能不可靠。

### 陷阱 5：「不拒絕 H₀」不等於「接受 H₀」

正確的表述是「沒有足夠的證據拒絕 H₀」，不是「H₀ 是對的」。

類比：法庭上「無罪釋放」不是說「被告是清白的」，而是「證據不足以定罪」。

### 陷阱 6：p-value 不是 H₀ 為真的機率

p-value = P(data at least this extreme | H₀ true)
≠ P(H₀ true | observed data)

後者是 Bayesian 的後驗機率，需要先驗分布才能算。

### 陷阱 7：MoM 和 MLE 的 σ² 估計

兩者都給出除以 n 的版本。考試如果問「不偏估計量」，記得要除以 n-1。

---

## 10. 章節總結

| 主題 | 核心公式 | 常考點 |
|------|----------|--------|
| MoM | 令 E[Xᵏ] = (1/n)ΣXᵢᵏ | 步驟、和 MLE 比較 |
| MLE | maxₐ L(θ) = maxₐ Πf(xᵢ; θ) | 完整推導、邊界解 |
| 不偏估計 | E[$\hat{\theta}$] = θ | S² vs (1/n)Σ(Xᵢ-X̄)² |
| CI | $\bar{X} \pm z_{\alpha/2} \cdot \sigma/\sqrt{n}$ | 正確解讀、σ 未知用 t |
| 假設檢定 | 五步驟 | Type I/II error、p-value |
| 充分統計量 | Fisher-Neyman 分解 | 判斷 + 例子 |

> **考試建議**：MLE 推導幾乎每年必考。一定要會做 Exp、Normal、Uniform、Poisson、Bernoulli 這幾個經典分布的 MLE。Uniform(0, θ) 的邊界解更是重中之重。信賴區間和假設檢定常出在應用題，要熟悉完整流程。

---

### 自我檢測

1. **MLE 基礎題**：丟一枚硬幣 20 次，得到 12 次正面。求正面機率 $p$ 的 MLE。

2. **MLE 計算題**：$X_1, X_2, \ldots, X_5$ i.i.d. $\sim \text{Poisson}(\lambda)$，觀測值為 3, 1, 4, 2, 5。求 $\lambda$ 的 MLE。

3. **信賴區間題**：某考試成績假設 Normal，$\sigma = 15$（已知）。抽 25 人，$\bar{x} = 68$。求 $\mu$ 的 95% 信賴區間。

4. **假設檢定題**：藥廠宣稱退燒藥平均 30 分鐘退燒（$\sigma = 8$ 分鐘已知）。醫生抽 16 位病人測試，得 $\bar{x} = 34$ 分鐘。在 $\alpha = 0.05$ 下，藥效是否如宣稱？（雙尾檢定）

5. **概念題**：下列哪個是 p-value 的正確解讀？
   (a) H₀ 為真的機率
   (b) 在 H₀ 為真的條件下，觀察到和實際結果一樣極端（或更極端）的機率
   (c) H₁ 為真的機率

<details><summary>參考答案</summary>

**1.** $\hat{p} = 12/20 = 0.6$

**2.** Poisson 的 MLE 是 $\hat{\lambda} = \bar{X} = (3+1+4+2+5)/5 = 15/5 = 3$

**3.** $\bar{x} \pm z_{0.025} \cdot \frac{\sigma}{\sqrt{n}} = 68 \pm 1.96 \times \frac{15}{\sqrt{25}} = 68 \pm 1.96 \times 3 = 68 \pm 5.88$
95% CI = **[62.12, 73.88]**

**4.** $Z = \frac{34 - 30}{8/\sqrt{16}} = \frac{4}{2} = 2.0$
$|Z| = 2.0 > z_{0.025} = 1.96$，落在拒絕域。**拒絕 $H_0$**。
p-value $= 2P(Z > 2) = 2 \times 0.0228 = 0.0456 < 0.05$。
結論：有統計證據顯示退燒時間和宣稱的 30 分鐘有顯著差異。

**5.** 答案是 **(b)**。p-value 不是 H₀ 為真的機率，也不是 H₁ 為真的機率。

</details>
