# 機率與統計 題型鑑別指南

> **核心目的**：看到題目的瞬間，知道要用什麼分布、什麼公式、什麼方法。
> **本指南特色**：每個公式都帶數字走一遍，讓你真正「會算」，而不只是「看過」。

---

# 第一部分：離散分布辨識 + 數值範例

## 1. Bernoulli(p) — 一次試驗，成功或失敗

**關鍵字**：「一次」「是否」「成功/失敗」

$$P(X = 1) = p, \quad P(X = 0) = 1 - p$$

$$E[X] = p, \quad \text{Var}(X) = p(1-p)$$

> **數值範例**：一個產品不良率 $p = 0.03$。
>
> 隨機取一個，是不良品（ $X=1$ ）的機率 = $0.03$
>
> $E[X] = 0.03$，$\text{Var}(X) = 0.03 \times 0.97 = 0.0291$

---

## 2. Binomial(n, p) — 固定 n 次試驗，數成功幾次

**關鍵字**：「$n$ 次試驗」「成功幾次」「獨立」「放回抽樣」

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

$$E[X] = np, \quad \text{Var}(X) = np(1-p)$$

> **數值範例**：投籃 $n = 10$ 次，命中率 $p = 0.6$，恰好進 7 球的機率？
>
> **Step 1**：確認分布 → $X \sim \text{Binomial}(10, 0.6)$
>
> **Step 2**：帶入公式
>
> $$P(X=7) = \binom{10}{7}(0.6)^7(0.4)^3$$
>
> **Step 3**：算組合數 $\binom{10}{7} = \frac{10!}{7! \cdot 3!} = 120$
>
> **Step 4**：算次方 $(0.6)^7 = 0.02799$，$(0.4)^3 = 0.064$
>
> **Step 5**：相乘 $120 \times 0.02799 \times 0.064 \approx 0.2150$
>
> **答案**：約 21.5%
>
> $E[X] = 10 \times 0.6 = 6$ 球，$\text{Var}(X) = 10 \times 0.6 \times 0.4 = 2.4$

### 台大級延伸

> 某通訊系統傳送 $n = 20$ 個 bit，每個 bit 出錯機率 $p = 0.05$（獨立）。系統可糾正最多 2 個錯誤。求系統無法正常運作的機率。
>
> $X \sim \text{Binomial}(20, 0.05)$，要求 $P(X \geq 3)$
>
> $P(X \geq 3) = 1 - P(X=0) - P(X=1) - P(X=2)$
>
> $P(X=0) = (0.95)^{20} = 0.3585$
>
> $P(X=1) = \binom{20}{1}(0.05)^1(0.95)^{19} = 20 \times 0.05 \times 0.3774 = 0.3774$
>
> $P(X=2) = \binom{20}{2}(0.05)^2(0.95)^{18} = 190 \times 0.0025 \times 0.3972 = 0.1887$
>
> $P(X \geq 3) = 1 - 0.3585 - 0.3774 - 0.1887 = 0.0755$（約 7.6%）

---

## 3. Geometric(p) — 一直做到第一次成功

**關鍵字**：「直到第一次成功」「等到」「第一個」「memoryless」

$$P(X = k) = (1-p)^{k-1} p, \quad k = 1, 2, 3, \ldots$$

$$E[X] = \frac{1}{p}, \quad \text{Var}(X) = \frac{1-p}{p^2}$$

$$P(X \gt k) = (1-p)^k \quad \text{（前 $k$ 次全部失敗）}$$

**無記憶性**：$P(X \gt m+n \mid X \gt m) = P(X \gt n)$

> **數值範例**：每次丟骰子出 6 的機率 $p = 1/6$。平均要丟幾次才出第一個 6？
>
> $X \sim \text{Geometric}(1/6)$
>
> $E[X] = \frac{1}{1/6} = 6$ 次（平均要丟 6 次）
>
> $\text{Var}(X) = \frac{5/6}{(1/6)^2} = \frac{5/6}{1/36} = 30$
>
> 丟超過 10 次才出 6 的機率：$P(X \gt 10) = (5/6)^{10} = 0.1615$（約 16.2%）
>
> **無記憶性範例**：已經丟了 8 次沒出 6，再丟超過 3 次才出 6 的機率？
>
> $P(X \gt 11 \mid X \gt 8) = P(X \gt 3) = (5/6)^3 = 0.5787$
>
> 和「從頭開始丟超過 3 次」的機率一模一樣！

---

## 4. Negative Binomial(r, p) — 做到第 r 次成功

**關鍵字**：「第 $r$ 次成功」「做到成交 $r$ 單」

$$P(X = k) = \binom{k-1}{r-1} p^r (1-p)^{k-r}, \quad k = r, r+1, \ldots$$

$$E[X] = \frac{r}{p}, \quad \text{Var}(X) = \frac{r(1-p)}{p^2}$$

> **數值範例**：業務員每次拜訪成交機率 $p = 0.2$，需要成交 $r = 3$ 單。
>
> $X \sim \text{NB}(3, 0.2)$
>
> $E[X] = \frac{3}{0.2} = 15$（平均要拜訪 15 位客戶）
>
> $\text{Var}(X) = \frac{3 \times 0.8}{0.04} = 60$，$\text{SD}(X) = \sqrt{60} \approx 7.75$
>
> 恰好第 5 次拜訪時成交第 3 單的機率（前 4 次中恰好 2 次成交，第 5 次成交）：
>
> $P(X=5) = \binom{4}{2}(0.2)^3(0.8)^2 = 6 \times 0.008 \times 0.64 = 0.0307$

---

## 5. Poisson(λ) — 固定時間/空間內的事件計數

**關鍵字**：「平均每小時/每天 $\lambda$ 次」「arrival」「事件數」「稀疏」

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots$$

$$E[X] = \lambda, \quad \text{Var}(X) = \lambda \quad \text{（期望值 = 變異數！）}$$

**可加性**：Poisson( $\lambda_1$ ) + Poisson( $\lambda_2$ ) = Poisson( $\lambda_1 + \lambda_2$ )

> **數值範例**：某路口平均每小時 $\lambda = 2$ 起事故。
>
> **(a) 某小時恰好 3 起的機率？**
>
> $P(X=3) = \frac{e^{-2} \times 2^3}{3!} = \frac{0.1353 \times 8}{6} = \frac{1.0824}{6} = 0.1804$（約 18%）
>
> **(b) 某小時沒有事故？**
>
> $P(X=0) = \frac{e^{-2} \times 2^0}{0!} = e^{-2} = 0.1353$（約 13.5%）
>
> **(c) 兩小時內超過 5 起？**（可加性：兩小時 $\lambda = 4$）
>
> $Y \sim \text{Poisson}(4)$
>
> $P(Y \leq 5) = e^{-4}(1 + 4 + 8 + 10.67 + 10.67 + 8.53) = e^{-4} \times 42.87 = 0.0183 \times 42.87 = 0.785$
>
> $P(Y \gt 5) = 1 - 0.785 = 0.215$（約 21.5%）

### Poisson 近似 Binomial

**條件**：$n$ 大（$\geq 20$）、$p$ 小（$\leq 0.05$）、$\lambda = np$ 適中

> **數值範例**：零件不良率 $p = 0.002$，一批 $n = 1000$ 個，不良品超過 3 個的機率？
>
> 精確算需要 $\binom{1000}{k}$，太麻煩。用 Poisson 近似：$\lambda = 1000 \times 0.002 = 2$
>
> $P(X \gt 3) = 1 - P(X \leq 3) = 1 - e^{-2}(1 + 2 + 2 + 4/3) = 1 - 0.1353 \times 6.333 = 1 - 0.857 = 0.143$

---

## 6. Hypergeometric(N, K, n) — 不放回抽樣

**關鍵字**：「不放回」「有限母體」「從 $N$ 個中有 $K$ 個特殊的，抽 $n$ 個」

$$P(X = k) = \frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$$

$$E[X] = n \cdot \frac{K}{N}, \quad \text{Var}(X) = np(1-p) \cdot \frac{N-n}{N-1} \quad \text{（其中 $p = K/N$）}$$

> **數值範例**：52 張撲克牌抽 5 張（不放回），恰好 2 張紅心？
>
> $N = 52$，$K = 13$（紅心），$n = 5$，$k = 2$
>
> $P(X=2) = \frac{\binom{13}{2}\binom{39}{3}}{\binom{52}{5}} = \frac{78 \times 9139}{2598960} = \frac{712842}{2598960} = 0.2743$（約 27.4%）
>
> $E[X] = 5 \times \frac{13}{52} = 1.25$ 張紅心

### Binomial vs Hypergeometric 怎麼選？

| 條件 | 用哪個 | 例子 |
|------|--------|------|
| 放回抽樣（或母體無限大） | **Binomial** | 丟骰子 10 次 |
| 不放回 + 有限母體 | **Hypergeometric** | 52 張牌抽 5 張 |
| 不放回但 $N \gg n$ | **Binomial 近似** | 1 萬人中抽 10 人 |

---

# 第二部分：連續分布辨識 + 數值範例

## 7. Uniform(a, b) — 區間上等可能

**關鍵字**：「均勻分布」「隨機選一點」「等可能」

$$f(x) = \frac{1}{b-a}, \quad a \leq x \leq b$$

$$E[X] = \frac{a+b}{2}, \quad \text{Var}(X) = \frac{(b-a)^2}{12}$$

$$P(c \leq X \leq d) = \frac{d - c}{b - a} \quad \text{（就是長度比例！）}$$

> **數值範例**：公車每 20 分鐘一班，你隨機到站。$X \sim \text{Uniform}(0, 20)$。
>
> 等超過 15 分鐘的機率？$P(X \gt 15) = \frac{20-15}{20-0} = \frac{5}{20} = 0.25$（25%）
>
> 平均等多久？$E[X] = \frac{0+20}{2} = 10$ 分鐘
>
> $\text{Var}(X) = \frac{(20-0)^2}{12} = \frac{400}{12} = 33.33$，$\text{SD} = 5.77$ 分鐘

---

## 8. Exponential(λ) — 等待時間

**關鍵字**：「等待時間」「兩次事件之間」「memoryless」「壽命」

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$

$$E[X] = \frac{1}{\lambda}, \quad \text{Var}(X) = \frac{1}{\lambda^2} \quad \text{（標準差 = 期望值！）}$$

$$P(X \gt t) = e^{-\lambda t} \quad \text{（存活函數，超好用）}$$

**無記憶性**：$P(X \gt s+t \mid X \gt s) = P(X \gt t)$

**和 Poisson 的關係**：事件按 Poisson( $\lambda$ ) 到達 → 等待時間是 Exp( $\lambda$ )

> **數值範例**：客服電話平均每分鐘接 $\lambda = 0.2$ 通（即平均 $1/0.2 = 5$ 分鐘一通）。
>
> **(a) 等超過 10 分鐘的機率？**
>
> $P(X \gt 10) = e^{-0.2 \times 10} = e^{-2} = 0.1353$（約 13.5%）
>
> **(b) 已等了 5 分鐘，再等超過 3 分鐘？**（無記憶性）
>
> $P(X \gt 8 \mid X \gt 5) = P(X \gt 3) = e^{-0.2 \times 3} = e^{-0.6} = 0.5488$（約 54.9%）
>
> **(c) 中位數？**（$F(m) = 0.5$，即 $1 - e^{-\lambda m} = 0.5$）
>
> $e^{-0.2m} = 0.5 \Rightarrow m = \frac{\ln 2}{0.2} = \frac{0.693}{0.2} = 3.47$ 分鐘
>
> 中位數(3.47) < 期望值(5)，Exponential 是右偏分布！

### Exponential 的兩種參數化（考試必注意！）

| 參數化 | PDF | $E[X]$ | 範例 |
|--------|-----|--------|------|
| Rate: $\lambda$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $\lambda = 2$ → 平均 0.5 |
| Mean: $\theta$ | $\frac{1}{\theta}e^{-x/\theta}$ | $\theta$ | $\theta = 0.5$ → 平均 0.5 |

**一定要看清楚題目用哪一種！**

---

## 9. Gamma(α, β) — 多個 Exponential 的和

**關鍵字**：「第 $n$ 個事件到達時間」「 $n$ 個 Exp 之和」「Erlang」

$$f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}, \quad x \gt 0$$

$$E[X] = \frac{\alpha}{\beta}, \quad \text{Var}(X) = \frac{\alpha}{\beta^2}$$

> **數值範例**：服務台每位客人服務時間 $\sim \text{Exp}(\beta = 2)$（平均 0.5 分鐘/人）。服務完 $\alpha = 3$ 位客人的總時間？
>
> $T \sim \text{Gamma}(3, 2)$
>
> $E[T] = \frac{3}{2} = 1.5$ 分鐘
>
> $\text{Var}(T) = \frac{3}{4} = 0.75$，$\text{SD} = 0.866$ 分鐘
>
> $P(T \gt 3) = \sum_{k=0}^{2} \frac{(2 \times 3)^k e^{-6}}{k!} = e^{-6}(1 + 6 + 18) = 25 \times 0.00248 = 0.0620$（約 6.2%）

---

## 10. Normal(μ, σ²) — 鐘型曲線

**關鍵字**：「常態」「鐘型」「CLT」「大量獨立之和」

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**標準化**：$Z = \frac{X - \mu}{\sigma} \sim N(0,1)$，然後查 $\Phi$ 表

**68-95-99.7 法則**：
- $\mu \pm 1\sigma$：68.27%
- $\mu \pm 2\sigma$：95.45%
- $\mu \pm 3\sigma$：99.73%

> **數值範例**：台灣成年男性身高 $X \sim N(172, 36)$，即 $\mu = 172$，$\sigma = 6$。
>
> **身高超過 180 公分的機率？**
>
> Step 1：標準化 $Z = \frac{180 - 172}{6} = \frac{8}{6} = 1.33$
>
> Step 2：查表 $\Phi(1.33) = 0.9082$
>
> Step 3：$P(X \gt 180) = 1 - \Phi(1.33) = 1 - 0.9082 = 0.0918$（約 9.2%）
>
> **身高在 166 到 178 之間的機率？**
>
> $P(166 \leq X \leq 178) = \Phi\left(\frac{178-172}{6}\right) - \Phi\left(\frac{166-172}{6}\right) = \Phi(1) - \Phi(-1) = 0.8413 - 0.1587 = 0.6827$（約 68%，就是 1σ 範圍）

### 常用 Z 值（背起來）

| $z$ | $\Phi(z)$ | 意義 |
|-----|-----------|------|
| 1.645 | 0.95 | 單尾 5% |
| 1.96 | 0.975 | 雙尾 5%（95% CI） |
| 2.326 | 0.99 | 單尾 1% |
| 2.576 | 0.995 | 雙尾 1%（99% CI） |

---

## 11. Chi-squared χ²(n)、t(n)、F(m,n)

| 分布 | 定義 | $E$ | $\text{Var}$ | 用途 |
|------|------|-----|------|------|
| $\chi^2(n)$ | $Z_1^2 + \cdots + Z_n^2$ | $n$ | $2n$ | 變異數檢定、適合度檢定 |
| $t(n)$ | $Z / \sqrt{V/n}$，$V \sim \chi^2(n)$ | $0$ | $\frac{n}{n-2}$ | 小樣本均值推論 |
| $F(m,n)$ | $(U/m)/(V/n)$ | $\frac{n}{n-2}$ | 複雜 | ANOVA、迴歸 F-test |

> **數值範例（χ²）**：$Z_1, Z_2, Z_3 \stackrel{iid}{\sim} N(0,1)$，$Q = Z_1^2 + Z_2^2 + Z_3^2 \sim \chi^2(3)$。
>
> $E[Q] = 3$，$\text{Var}(Q) = 6$
>
> $P(Q \gt 7.815) = 0.05$（查 $\chi^2$ 表，df=3 的 5% 臨界值 = 7.815）

---

# 第三部分：Poisson Process 三寶

**情境**：事件以固定速率 $\lambda$ 隨機發生。

| 問什麼 | 分布 | 公式 |
|--------|------|------|
| 某段時間內事件數 | Poisson( $\lambda t$ ) | $P(N=k) = \frac{(\lambda t)^k e^{-\lambda t}}{k!}$ |
| 兩事件之間的間隔 | Exp( $\lambda$ ) | $P(T \gt t) = e^{-\lambda t}$ |
| 第 $n$ 個事件到達時間 | Gamma( $n, \lambda$ ) | $E = n/\lambda$ |

> **完整數值範例**：餐廳顧客到達率 $\lambda = 6$ 人/小時。
>
> **Q1**：一小時內來了恰好 4 組？→ $X \sim \text{Poisson}(6)$
>
> $P(X=4) = \frac{e^{-6} \times 6^4}{4!} = \frac{0.00248 \times 1296}{24} = \frac{3.215}{24} = 0.1339$（約 13.4%）
>
> **Q2**：下一位客人多久會到？→ $T \sim \text{Exp}(6)$
>
> $E[T] = 1/6$ 小時 $= 10$ 分鐘
>
> 等超過 20 分鐘 = 1/3 小時的機率：$P(T \gt 1/3) = e^{-6 \times 1/3} = e^{-2} = 0.135$
>
> **Q3**：第 3 位客人什麼時候到？→ $S_3 \sim \text{Gamma}(3, 6)$
>
> $E[S_3] = 3/6 = 0.5$ 小時 $= 30$ 分鐘

---

# 第四部分：計算方法 + 數值範例

## 方法 1：全概率公式 — 「因→果」的加總

$$P(B) = \sum_i P(B \mid A_i) \cdot P(A_i)$$

> **數值範例**：工廠 A 佔產量 60%（不良率 2%），工廠 B 佔產量 40%（不良率 5%）。隨機取一產品，不良的機率？
>
> $P(\text{不良}) = P(\text{不良} \mid A) \cdot P(A) + P(\text{不良} \mid B) \cdot P(B)$
>
> $= 0.02 \times 0.6 + 0.05 \times 0.4 = 0.012 + 0.020 = 0.032$（3.2%）

---

## 方法 2：貝氏定理 — 「果→因」的反推

$$P(A_i \mid B) = \frac{P(B \mid A_i) \cdot P(A_i)}{P(B)}$$

> **延續上例**：已知某產品是不良品，它來自工廠 A 的機率？
>
> $P(A \mid \text{不良}) = \frac{P(\text{不良} \mid A) \cdot P(A)}{P(\text{不良})} = \frac{0.02 \times 0.6}{0.032} = \frac{0.012}{0.032} = 0.375$（37.5%）
>
> 雖然 A 廠佔 60% 產量，但不良品中只有 37.5% 來自 A 廠（因為 A 的品質比較好）。

### 台大級延伸：連續用貝氏

> 醫學檢測：某病盛行率 $P(D) = 0.001$（千分之一）。
>
> 檢測靈敏度 $P(+ \mid D) = 0.99$（有病測出陽性 99%）
>
> 偽陽性率 $P(+ \mid D^c) = 0.05$（沒病但測陽性 5%）
>
> **你檢測陽性了，你真的有病的機率是多少？**
>
> $P(D \mid +) = \frac{P(+ \mid D) \cdot P(D)}{P(+)}$
>
> $P(+) = P(+ \mid D) \cdot P(D) + P(+ \mid D^c) \cdot P(D^c) = 0.99 \times 0.001 + 0.05 \times 0.999 = 0.00099 + 0.04995 = 0.05094$
>
> $P(D \mid +) = \frac{0.00099}{0.05094} = 0.0194$
>
> **只有 1.94%！** 即使測到陽性，真正有病的機率不到 2%。
>
> 這就是 **base rate fallacy** — 當盛行率很低時，偽陽性數量遠大於真陽性。

---

## 方法 3：指標法（Indicator Method） — 「有多少個滿足條件？」

$$X = \sum_{i=1}^{n} X_i, \quad E[X] = \sum_{i=1}^{n} P(\text{第 } i \text{ 個滿足條件})$$

> **數值範例（錯排）**：5 封信隨機放入 5 個信封，期望放對幾封？
>
> 令 $X_i = 1$ 若第 $i$ 封放對。$P(X_i = 1) = 1/5$
>
> $E[X] = \sum_{i=1}^{5} E[X_i] = 5 \times \frac{1}{5} = 1$
>
> 不管 $n$ 多大，期望放對的信件數永遠是 1！

### 台大級延伸：Coupon Collector

> 便利商店集 $n = 6$ 款公仔，每次隨機送一款。期望要買幾次才能集齊？
>
> 第 1 款：一定是新的，期望 $\frac{6}{6} = 1$ 次
>
> 第 2 款（已有 1 款）：每次拿到新款的機率 $5/6$，期望 $\frac{6}{5} = 1.2$ 次
>
> 第 3 款：機率 $4/6$，期望 $\frac{6}{4} = 1.5$ 次
>
> 第 4 款：期望 $\frac{6}{3} = 2$ 次
>
> 第 5 款：期望 $\frac{6}{2} = 3$ 次
>
> 第 6 款：期望 $\frac{6}{1} = 6$ 次
>
> 總期望 $= 6 \times (1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \frac{1}{6}) = 6 \times 2.45 = 14.7$ 次
>
> **一般公式**：$E = n \cdot H_n = n(1 + 1/2 + 1/3 + \cdots + 1/n) \approx n \ln n$

---

## 方法 4：MGF 辨認分布 — 算出 MGF → 查表 → 辨識

| 分布 | MGF $M(t)$ |
|------|-----------|
| Bernoulli( $p$ ) | $q + pe^t$ |
| Binomial( $n,p$ ) | $(q+pe^t)^n$ |
| Poisson( $\lambda$ ) | $e^{\lambda(e^t-1)}$ |
| Geometric( $p$ ) | $\frac{pe^t}{1-qe^t}$ |
| Exponential( $\lambda$ ) | $\frac{\lambda}{\lambda-t}$ |
| Normal( $\mu,\sigma^2$ ) | $e^{\mu t + \sigma^2 t^2/2}$ |
| Gamma( $\alpha,\beta$ ) | $\left(\frac{\beta}{\beta-t}\right)^\alpha$ |

> **數值範例**：某隨機變數 $X$ 的 MGF 為 $M(t) = e^{3(e^t - 1)}$。
>
> 比對表格：這是 Poisson 的形式 $e^{\lambda(e^t - 1)}$，其中 $\lambda = 3$。
>
> 所以 $X \sim \text{Poisson}(3)$，$E[X] = 3$，$\text{Var}(X) = 3$。
>
> **驗證**：$M'(t) = 3e^t \cdot e^{3(e^t-1)}$，$M'(0) = 3 \times 1 = 3 = E[X]$ ✓

---

## 方法 5：條件變異數公式（Eve's Law）

$$\text{Var}(X) = E[\text{Var}(X \mid Y)] + \text{Var}(E[X \mid Y])$$

> **數值範例**：隨機選一個箱子（箱子 A 機率 0.6，箱子 B 機率 0.4）。箱子 A 中的球重量 $X \mid A \sim N(10, 4)$，箱子 B 中 $X \mid B \sim N(15, 9)$。
>
> **Step 1**：$E[X \mid Y]$ 的值
> - 選 A：$E[X \mid A] = 10$
> - 選 B：$E[X \mid B] = 15$
>
> **Step 2**：$E[X] = 10 \times 0.6 + 15 \times 0.4 = 6 + 6 = 12$
>
> **Step 3**：$\text{Var}(E[X \mid Y]) = E[(E[X \mid Y])^2] - (E[X])^2 = (100 \times 0.6 + 225 \times 0.4) - 144 = (60 + 90) - 144 = 6$
>
> **Step 4**：$E[\text{Var}(X \mid Y)] = 4 \times 0.6 + 9 \times 0.4 = 2.4 + 3.6 = 6$
>
> **Step 5**：$\text{Var}(X) = 6 + 6 = 12$

---

# 第五部分：常見計算套路 + 數值範例

## 套路 1：「至少一個」→ 補集法

$$P(\text{至少一個}) = 1 - P(\text{一個都沒有})$$

> **數值範例**：丟 10 次骰子，至少出現一次 6？
>
> $P = 1 - (5/6)^{10} = 1 - 0.1615 = 0.8385$（約 83.9%）

---

## 套路 2：最大值 / 最小值

$$P(\max(X_1, \ldots, X_n) \leq x) = [F(x)]^n$$

$$P(\min(X_1, \ldots, X_n) \leq x) = 1 - [1 - F(x)]^n$$

**重要結論**：$n$ 個獨立 $\text{Exp}(\lambda)$ 的最小值 $\sim \text{Exp}(n\lambda)$

> **數值範例**：5 台機器壽命各自獨立 $\sim \text{Exp}(0.01)$（平均壽命 100 小時）。系統在「任一台壞掉」就停機。
>
> 系統壽命 $= \min(X_1, \ldots, X_5) \sim \text{Exp}(5 \times 0.01) = \text{Exp}(0.05)$
>
> 系統平均壽命 $= 1/0.05 = 20$ 小時（從 100 小時驟降到 20 小時！）
>
> $P(\text{系統撐過 30 小時}) = e^{-0.05 \times 30} = e^{-1.5} = 0.2231$

---

## 套路 3：遞迴 / 條件化期望值

**看到「第一步可能 A 或 B，然後重新開始」→ 設 $E[X]$ 列方程式**

> **數值範例（Gambler's Ruin 簡化版）**：
>
> 你有 3 元，每次丟公平硬幣（$p = 0.5$），正面贏 1 元，反面輸 1 元。目標 5 元（到 5 元贏，到 0 元輸）。你贏的機率？
>
> 設 $P_i$ = 從 $i$ 元開始贏的機率。邊界條件：$P_0 = 0$，$P_5 = 1$。
>
> 遞迴：$P_i = 0.5 \cdot P_{i+1} + 0.5 \cdot P_{i-1}$
>
> 公平硬幣（$p = 0.5$）的解：$P_i = i/5$（線性解）
>
> 所以 $P_3 = 3/5 = 0.6$（60%）

### 台大級延伸：不公平 Gambler's Ruin

> 若 $p = 0.4$（輸多贏少），從 3 元開始，目標 5 元。
>
> 一般公式：$P_i = \frac{1 - (q/p)^i}{1 - (q/p)^N}$，其中 $q/p = 0.6/0.4 = 1.5$
>
> $P_3 = \frac{1 - 1.5^3}{1 - 1.5^5} = \frac{1 - 3.375}{1 - 7.594} = \frac{-2.375}{-6.594} = 0.3602$
>
> 只有 36%！（公平時是 60%，不公平使贏的機率幾乎砍半）

---

## 套路 4：變數變換（CDF 法）

**已知 $X$ 的分布，求 $Y = g(X)$ 的分布**

> **數值範例**：$X \sim \text{Uniform}(0, 1)$，求 $Y = -\frac{1}{\lambda}\ln(X)$ 的分布。
>
> **CDF 法**：
>
> $F_Y(y) = P(Y \leq y) = P\left(-\frac{1}{\lambda}\ln X \leq y\right) = P(\ln X \geq -\lambda y) = P(X \geq e^{-\lambda y})$
>
> $= 1 - e^{-\lambda y}, \quad y \geq 0$
>
> 這就是 $\text{Exp}(\lambda)$ 的 CDF！
>
> **應用**：這是模擬 Exponential 隨機變數的標準方法（反轉換法）。

---

## 套路 5：Order Statistics

$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1} [1-F(x)]^{n-k} f(x)$$

> **數值範例**：$X_1, X_2, X_3 \stackrel{iid}{\sim} \text{Uniform}(0, 1)$。求最大值 $X_{(3)}$ 的期望值。
>
> $f_{X_{(3)}}(x) = \frac{3!}{2! \cdot 0!} [x]^2 [1-x]^0 \cdot 1 = 3x^2, \quad 0 \leq x \leq 1$
>
> $E[X_{(3)}] = \int_0^1 x \cdot 3x^2 \, dx = 3 \int_0^1 x^3 \, dx = 3 \times \frac{1}{4} = \frac{3}{4}$
>
> **一般結論**：$n$ 個 $\text{Uniform}(0,1)$ 的第 $k$ 小的期望值 $= \frac{k}{n+1}$

---

# 第六部分：分布之間的關係圖

```
Bernoulli(p)
    │
    │ n 次獨立的和
    ▼
Binomial(n,p) ──n大p小，λ=np──→ Poisson(λ)
    │                                 │
    │ n→∞ (CLT)                       │ 事件間隔
    ▼                                 ▼
Normal(np, npq)                Exponential(λ)
    ▲                                 │
    │ CLT                             │ n 個獨立的和
    │                                 ▼
任意 iid 之和 ─CLT─→ Normal    Gamma(n, λ) = Erlang

Geometric(p) ──r 次的和──→ Negative Binomial(r, p)
    │
    │ 連續版本（memoryless）
    ▼
Exponential(λ)

Hypergeometric(N,K,n) ──N→∞, K/N→p──→ Binomial(n, p)

Normal² ──n個之和──→ Chi-squared(n) = Gamma(n/2, 1/2)

Normal / √(χ²/n) ──→ t(n)

χ²/m ÷ χ²/n ──→ F(m,n)

Uniform(0,1) ── -ln(U)/λ ──→ Exponential(λ)
```

---

# 第七部分：考試速判流程

```
看到題目
  │
  ├─「求機率 P(...)」
  │    ├─ 有條件資訊 → 全概率 / 貝氏
  │    ├─ 至少一個 → 補集法
  │    ├─ 可用已知分布 → 直接帶 PMF/PDF
  │    └─ 計數問題 → 排列組合 + 古典機率
  │
  ├─「求期望值 E[X]」
  │    ├─ 已知分布 → 查表公式
  │    ├─ X = 指標之和 → 線性期望值
  │    ├─ 條件結構 → E[X] = Σ E[X|Aᵢ]P(Aᵢ)
  │    └─ 遞迴結構 → 列方程式解
  │
  ├─「求變異數 Var(X)」
  │    ├─ 已知分布 → 查表
  │    ├─ 用 Var = E[X²] - (E[X])² → 先求 E[X²]
  │    └─ 條件結構 → Eve's Law
  │
  └─「求分布 / PDF / CDF」
       ├─ Y = g(X)，g 單調 → 變數變換法
       ├─ Y = g(X)，g 非單調 → CDF 法
       ├─ Z = X + Y → 摺積或 MGF
       └─ 算出 MGF → 查表辨識
```

---

# 第八部分：台大考試級綜合練習

### 練習 1：Poisson + Bayes（★★★）

某郵局有兩種包裹：國內包裹（佔 70%）和國際包裹（佔 30%）。國內包裹每天到達數 $\sim \text{Poisson}(5)$，國際包裹每天到達數 $\sim \text{Poisson}(2)$。

(a) 某天總共到達恰好 8 個包裹的機率。

(b) 已知某天到了 8 個包裹，其中恰好 3 個是國際包裹的機率。

<details>
<summary>解答</summary>

**(a)** 國內 $X \sim \text{Poi}(5)$，國際 $Y \sim \text{Poi}(2)$，獨立。

$X + Y \sim \text{Poi}(7)$

$P(X+Y = 8) = \frac{e^{-7} \times 7^8}{8!} = \frac{0.000912 \times 5764801}{40320} = \frac{5257.6}{40320} = 0.1304$

**(b)** 給定總共 8 個包裹，國際包裹數服從 Binomial。

原理：給定 $X + Y = n$ 時，$Y \mid (X+Y=n) \sim \text{Binomial}\left(n, \frac{\lambda_Y}{\lambda_X + \lambda_Y}\right)$

$Y \mid (X+Y=8) \sim \text{Binomial}\left(8, \frac{2}{7}\right)$

$P(Y = 3) = \binom{8}{3}\left(\frac{2}{7}\right)^3\left(\frac{5}{7}\right)^5 = 56 \times \frac{8}{343} \times \frac{3125}{16807} = 56 \times 0.02332 \times 0.18593 = 0.2428$

</details>

---

### 練習 2：Exponential + 條件機率（★★★）

兩台機器 $A$、$B$ 的壽命分別為 $X_A \sim \text{Exp}(1)$、$X_B \sim \text{Exp}(2)$（獨立）。

(a) 求 $P(X_A \lt X_B)$（A 先壞的機率）

(b) 求 $\min(X_A, X_B)$ 的分布

(c) 已知 A 先壞了，求從系統啟動到 A 壞掉的期望時間。

<details>
<summary>解答</summary>

**(a)** $P(X_A \lt X_B) = \int_0^\infty P(X_B \gt t) \cdot f_{X_A}(t) \, dt$

$= \int_0^\infty e^{-2t} \cdot e^{-t} \, dt = \int_0^\infty e^{-3t} \, dt = \frac{1}{3}$

A 先壞的機率 = $1/3$（更短命的 B 反而 2/3 機率先壞，因為 rate 更高）

**(b)** $P(\min \gt t) = P(X_A \gt t) \cdot P(X_B \gt t) = e^{-t} \cdot e^{-2t} = e^{-3t}$

所以 $\min(X_A, X_B) \sim \text{Exp}(3)$。$E[\min] = 1/3$

**(c)** 已知 A 先壞，$E[X_A \mid X_A \lt X_B]$。

$E[\min(X_A, X_B) \mid A \text{先壞}] = E[X_A \mid X_A \lt X_B]$

由於 $\min \sim \text{Exp}(3)$，且 A 先壞的機率 = 1/3：

$E[X_A \mid X_A \lt X_B] = E[\min \mid \min = X_A] = \frac{1}{3}$

（因為給定哪台先壞，最小值仍然是 $\text{Exp}(\lambda_A + \lambda_B)$，與誰先壞獨立。）

</details>

---

### 練習 3：Normal + CLT（★★★★）

某保險公司有 10000 位保戶。每位保戶每年出險的機率為 0.01（獨立），出險時理賠金額 $Y \sim \text{Exp}(1/5000)$（平均 5000 元）。

(a) 某年出險人數的期望值和標準差。

(b) 某年總理賠金額超過 60 萬元的機率（用 CLT 近似）。

<details>
<summary>解答</summary>

**(a)** 出險人數 $N \sim \text{Binomial}(10000, 0.01)$

$E[N] = 10000 \times 0.01 = 100$

$\text{Var}(N) = 10000 \times 0.01 \times 0.99 = 99$

$\text{SD}(N) = \sqrt{99} \approx 9.95$

也可以用 Poisson 近似：$N \approx \text{Poisson}(100)$

**(b)** 設 $S = \sum_{i=1}^{N} Y_i$ 為總理賠金額。用全期望值：

$E[S] = E[N] \cdot E[Y] = 100 \times 5000 = 500000$ 元

$\text{Var}(S) = E[N] \cdot \text{Var}(Y) + \text{Var}(N) \cdot (E[Y])^2$（Eve's Law）

$= 100 \times 5000^2 + 99 \times 5000^2 = 199 \times 25000000 = 4.975 \times 10^9$

$\text{SD}(S) = \sqrt{4.975 \times 10^9} \approx 70534$

由 CLT：$S \approx N(500000, 70534^2)$

$P(S \gt 600000) = P\left(Z \gt \frac{600000 - 500000}{70534}\right) = P(Z \gt 1.418)$

$= 1 - \Phi(1.42) = 1 - 0.9222 = 0.0778$（約 7.8%）

</details>

---

### 練習 4：容斥原理深度題（★★★★）

$n$ 個人隨機排成一列。若第 $i$ 個人排在第 $i$ 位稱為「fixed point」。

(a) 至少有一個 fixed point 的機率（用容斥原理）。

(b) 恰好有 $k$ 個 fixed point 的機率。

(c) 當 $n = 5$ 時，帶入具體數字驗算 (a) 和 (b)。

<details>
<summary>解答</summary>

**(a)** 令 $A_i$ = 第 $i$ 人在第 $i$ 位。

$P(A_i) = \frac{(n-1)!}{n!} = \frac{1}{n}$

$P(A_i \cap A_j) = \frac{(n-2)!}{n!} = \frac{1}{n(n-1)}$

一般地：$P(A_{i_1} \cap \cdots \cap A_{i_k}) = \frac{(n-k)!}{n!}$

有 $\binom{n}{k}$ 項，每項相同，所以第 $k$ 層的總和：

$\binom{n}{k} \cdot \frac{(n-k)!}{n!} = \frac{1}{k!}$

容斥：$P(\text{至少一個}) = 1 - \frac{1}{2!} + \frac{1}{3!} - \cdots + (-1)^{n+1}\frac{1}{n!}$

$P(\text{全部錯排}) = 1 - P(\text{至少一個}) = \sum_{k=0}^{n} \frac{(-1)^k}{k!} \approx e^{-1} \approx 0.3679$

**(b)** 恰好 $k$ 個 fixed point：先選哪 $k$ 個是 fixed，剩下 $n-k$ 個全部錯排。

$P(\text{恰好 } k \text{ 個}) = \binom{n}{k} \cdot \frac{D_{n-k}}{n!} = \frac{1}{k!} \cdot \sum_{j=0}^{n-k} \frac{(-1)^j}{j!}$

其中 $D_m = m! \sum_{j=0}^{m} \frac{(-1)^j}{j!}$ 是 $m$ 個元素的錯排數。

**(c)** $n = 5$：

$D_5 = 5!(1 - 1 + 1/2 - 1/6 + 1/24 - 1/120) = 120 \times 0.3667 = 44$

$P(\text{至少一個 fixed point}) = 1 - 1/2 + 1/6 - 1/24 + 1/120 = 0.6333$

$P(\text{恰好 0 個}) = D_5 / 5! = 44/120 = 0.3667$

$P(\text{恰好 1 個}) = \binom{5}{1} \cdot D_4 / 5! = 5 \times 9 / 120 = 45/120 = 0.375$

$P(\text{恰好 2 個}) = \binom{5}{2} \cdot D_3 / 5! = 10 \times 2 / 120 = 20/120 = 0.1667$

$P(\text{恰好 3 個}) = \binom{5}{3} \cdot D_2 / 5! = 10 \times 1 / 120 = 10/120 = 0.0833$

$P(\text{恰好 4 個}) = 0$（不可能恰好 4 個對，因為 4 個對了第 5 個也一定對）

$P(\text{恰好 5 個}) = 1/5! = 1/120 = 0.0083$

驗證：$0.3667 + 0.375 + 0.1667 + 0.0833 + 0 + 0.0083 = 1$ ✓

</details>

---

### 練習 5：變數變換 + Jacobian（★★★★★）

$X, Y$ 獨立，$X \sim \text{Exp}(1)$，$Y \sim \text{Exp}(1)$。令 $U = X + Y$，$V = X / (X + Y)$。

(a) 求 $(U, V)$ 的聯合 PDF。

(b) 證明 $U$ 和 $V$ 獨立。

(c) 分別求 $U$ 和 $V$ 的邊際分布。

<details>
<summary>解答</summary>

**(a)** 原始聯合 PDF：$f_{X,Y}(x,y) = e^{-x} \cdot e^{-y} = e^{-(x+y)}, \quad x,y \gt 0$

反解：$X = UV$，$Y = U(1-V)$

Jacobian：

$$J = \begin{vmatrix} \frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ \frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} \end{vmatrix} = \begin{vmatrix} v & u \\ 1-v & -u \end{vmatrix} = -uv - u(1-v) = -u$$

$|J| = u$

$f_{U,V}(u,v) = f_{X,Y}(uv, u(1-v)) \cdot |J| = e^{-u} \cdot u, \quad u \gt 0, \, 0 \lt v \lt 1$

**(b)** $f_{U,V}(u,v) = \underbrace{u \cdot e^{-u}}_{g(u)} \cdot \underbrace{1}_{h(v)}$

可以分離成只和 $u$ 有關的函數乘以只和 $v$ 有關的函數 → $U$ 和 $V$ 獨立！

**(c)** $f_U(u) = u \cdot e^{-u}, \quad u \gt 0$

這是 $\text{Gamma}(2, 1)$ 的 PDF。驗證：$E[U] = E[X+Y] = 1 + 1 = 2 = \alpha/\beta$ ✓

$f_V(v) = 1, \quad 0 \lt v \lt 1$

這是 $\text{Uniform}(0, 1)$！

**結論**：$X + Y \sim \text{Gamma}(2,1)$，$\frac{X}{X+Y} \sim \text{Uniform}(0,1)$，且兩者獨立。

</details>

---

# 第九部分：常見易錯點

1. **Poisson 近似條件**：$n$ 大、$p$ 小、$\lambda = np$ 適中。不是所有 Binomial 都能用 Poisson！

2. **獨立 ≠ 不相關**：$\text{Cov} = 0$ 不等於獨立。但**聯合 Normal** 時，不相關 $\Rightarrow$ 獨立。

3. **Geometric 的兩種定義**：
   - 「試驗次數」：$k = 1, 2, \ldots$，$E = 1/p$
   - 「失敗次數」：$k = 0, 1, 2, \ldots$，$E = (1-p)/p$
   - **考試第一件事：確認定義！**

4. **Exponential 的兩種參數化**：rate $\lambda$ vs. mean $\theta = 1/\lambda$。

5. **Normal 的第二個參數是 $\sigma^2$（變異數）**，不是 $\sigma$（標準差）。

6. **CLT 的標準化**：$Z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}}$，分母是 $\sigma / \sqrt{n}$ 不是 $\sigma$。

7. **$P(X = a) = 0$ 對連續型**：所以 $P(X \leq a) = P(X \lt a)$。但離散型兩者不同！

8. **PDF 可以大於 1**：$f(x)$ 是密度不是機率。$\text{Uniform}(0, 0.1)$ 的 $f(x) = 10$。

9. **Max/Min 的獨立性**：$\max$ 和 $\min$ 通常不獨立（即使原始 RV 獨立）。

10. **Hypergeometric 的有限母體修正**：不放回的變異數 $\leq$ 放回的變異數（乘以 $\frac{N-n}{N-1} \leq 1$）。

---

# 第十部分：分布速查總表

## 離散分布

| 分布 | PMF | $E[X]$ | $\text{Var}(X)$ | MGF |
|------|-----|--------|-----------------|-----|
| Bernoulli( $p$ ) | $p^k q^{1-k}$ | $p$ | $pq$ | $q+pe^t$ |
| Binomial( $n,p$ ) | $\binom{n}{k}p^k q^{n-k}$ | $np$ | $npq$ | $(q+pe^t)^n$ |
| Geometric( $p$ ) | $q^{k-1}p$ | $1/p$ | $q/p^2$ | $\frac{pe^t}{1-qe^t}$ |
| NegBin( $r,p$ ) | $\binom{k-1}{r-1}p^r q^{k-r}$ | $r/p$ | $rq/p^2$ | $\left(\frac{pe^t}{1-qe^t}\right)^r$ |
| Poisson( $\lambda$ ) | $\frac{e^{-\lambda}\lambda^k}{k!}$ | $\lambda$ | $\lambda$ | $e^{\lambda(e^t-1)}$ |
| HyperGeo | $\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$ | $\frac{nK}{N}$ | $npq\frac{N-n}{N-1}$ | — |

## 連續分布

| 分布 | PDF | $E[X]$ | $\text{Var}(X)$ | MGF |
|------|-----|--------|-----------------|-----|
| Uniform( $a,b$ ) | $\frac{1}{b-a}$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ | $\frac{e^{tb}-e^{ta}}{t(b-a)}$ |
| Exp( $\lambda$ ) | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ | $\frac{\lambda}{\lambda-t}$ |
| Gamma( $\alpha,\beta$ ) | $\frac{\beta^\alpha}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x}$ | $\alpha/\beta$ | $\alpha/\beta^2$ | $\left(\frac{\beta}{\beta-t}\right)^\alpha$ |
| Normal( $\mu,\sigma^2$ ) | $\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ | $e^{\mu t+\sigma^2 t^2/2}$ |
| $\chi^2(n)$ | Gamma( $n/2, 1/2$ ) | $n$ | $2n$ | $(1-2t)^{-n/2}$ |

其中 $q = 1 - p$。

---

> **使用建議**：先用「速判流程」判斷類型 → 查「分布辨識」確認分布 → 帶入「數值範例」的模式一步步算 → 用「易錯點」自我檢查。
>
> 各分布的完整推導請參考 prob_01 ~ prob_09。
