# 連續分布大全

> 台大機率統計教學講義 — 從 Uniform 到 F-distribution，一次搞懂所有連續分布

---

## 一、連續隨機變數的基本觀念

### 1.1 離散 vs. 連續：最根本的差異

離散隨機變數可以「列舉」所有可能值（0, 1, 2, ...），每個值都有正的機率。
連續隨機變數的值域是一段區間（甚至整個實數線），**任何單一點的機率都是零**。

> **直覺**：想像一個飛鏢射向 [0,1] 的數線。精確射中 0.5 的機率是多少？是零。但射中 [0.4, 0.6] 這個「區間」的機率不是零。

所以連續隨機變數不用 PMF，而是用 **PDF（機率密度函數）** 來描述「密度」。

### 1.2 CDF（累積分布函數）

**定義**：

$$F_X(x) = P(X \le x), \quad -\infty < x < \infty$$

**性質**（不管離散或連續都成立）：

1. $F(-\infty) = 0$，$F(\infty) = 1$
2. $F$ 是非遞減函數：若 $a < b$，則 $F(a) \le F(b)$
3. $F$ 是右連續的
4. $P(a < X \le b) = F(b) - F(a)$

### 1.3 PDF（機率密度函數）

**定義**：若 $F_X(x)$ 可微分，則

$$f_X(x) = F_X'(x) = \frac{dF_X(x)}{dx}$$

**反過來**：

$$F_X(x) = \int_{-\infty}^{x} f_X(t)\,dt$$

**關鍵性質**：

1. $f_X(x) \ge 0$（但可以大於 1！密度不是機率）
2. $\int_{-\infty}^{\infty} f_X(x)\,dx = 1$
3. $P(a \le X \le b) = \int_a^b f_X(x)\,dx$
4. **$P(X = a) = 0$**（對連續型來說，等號不影響）

> **常見陷阱**：很多同學把 $f(x)$ 當成機率。不對！$f(x)$ 是「密度」，可以超過 1。
> 例如 $X \sim \text{Uniform}(0, 0.5)$，則 $f(x) = 2$，大於 1，完全合法。

### 1.4 CDF 和 PDF 的關係圖

```
f(x)  （PDF）
 │    ┌──────┐
 │    │      │         P(a≤X≤b) = 陰影面積
 │    │██████│                  = ∫_a^b f(x)dx
 │    │██████│                  = F(b) - F(a)
 └────┴──a──b┴──── x

F(x)  （CDF）
 1 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╱─────
 │                     ╱
 │                   ╱
 │                 ╱    ← F'(x) = f(x)
 │              ╱
 0 ──────────╱──────────── x
```

---

## 二、Uniform 分布 Uniform(a, b)

### 2.1 定義與直覺

**情境**：在區間 $[a, b]$ 上「等可能」地隨機取一個數。

**PDF**：

$$f(x) = \begin{cases} \frac{1}{b-a}, & a \le x \le b \\ 0, & \text{otherwise} \end{cases}$$

**驗證**：$\int_a^b \frac{1}{b-a}\,dx = \frac{b-a}{b-a} = 1$ ✓

### 2.2 CDF 推導

$$F(x) = \int_{-\infty}^x f(t)\,dt = \begin{cases} 0, & x < a \\ \frac{x-a}{b-a}, & a \le x \le b \\ 1, & x > b \end{cases}$$

### 2.3 E[X] 推導

$$E[X] = \int_a^b x \cdot \frac{1}{b-a}\,dx = \frac{1}{b-a} \cdot \frac{x^2}{2}\Bigg|_a^b = \frac{1}{b-a} \cdot \frac{b^2 - a^2}{2} = \frac{(b+a)(b-a)}{2(b-a)} = \frac{a+b}{2}$$

> **直覺**：均勻分布的期望值就是中點，完全合理。

### 2.4 E[X^2] 推導

$$E[X^2] = \int_a^b x^2 \cdot \frac{1}{b-a}\,dx = \frac{1}{b-a} \cdot \frac{x^3}{3}\Bigg|_a^b = \frac{b^3 - a^3}{3(b-a)} = \frac{b^2 + ab + a^2}{3}$$

（用了因式分解 $b^3 - a^3 = (b-a)(b^2 + ab + a^2)$）

### 2.5 Var(X) 推導

$$\text{Var}(X) = E[X^2] - (E[X])^2 = \frac{b^2 + ab + a^2}{3} - \left(\frac{a+b}{2}\right)^2$$

$$= \frac{b^2 + ab + a^2}{3} - \frac{a^2 + 2ab + b^2}{4}$$

通分（分母取 12）：

$$= \frac{4(b^2 + ab + a^2) - 3(a^2 + 2ab + b^2)}{12} = \frac{4b^2 + 4ab + 4a^2 - 3a^2 - 6ab - 3b^2}{12}$$

$$= \frac{b^2 - 2ab + a^2}{12} = \frac{(b-a)^2}{12}$$

### 2.6 MGF 推導

$$M(t) = E[e^{tX}] = \int_a^b e^{tx} \cdot \frac{1}{b-a}\,dx = \frac{1}{b-a} \cdot \frac{e^{tx}}{t}\Bigg|_a^b = \frac{e^{tb} - e^{ta}}{t(b-a)}, \quad t \neq 0$$

當 $t = 0$ 時，$M(0) = 1$。

### 2.7 計算範例

**例題**：設 $X \sim \text{Uniform}(2, 8)$。求 $P(3 \le X \le 5)$ 和 $E[X^3]$。

**解**：

$$P(3 \le X \le 5) = \int_3^5 \frac{1}{8-2}\,dx = \frac{1}{6} \cdot (5-3) = \frac{2}{6} = \frac{1}{3}$$

$$E[X^3] = \int_2^8 x^3 \cdot \frac{1}{6}\,dx = \frac{1}{6} \cdot \frac{x^4}{4}\Bigg|_2^8 = \frac{1}{24}(8^4 - 2^4) = \frac{4096 - 16}{24} = \frac{4080}{24} = 170$$

---

## 三、Exponential 分布 Exponential(λ)

### 3.1 定義與直覺

**情境**：Poisson 過程中，等待「第一個事件」發生所需的時間。

如果事件平均每單位時間發生 $\lambda$ 次（Poisson rate = λ），那麼等到第一個事件的時間 $T$ 就是 $\text{Exp}(\lambda)$。

**PDF**：

$$f(x) = \lambda e^{-\lambda x}, \quad x \ge 0$$

**驗證**：$\int_0^\infty \lambda e^{-\lambda x}\,dx = \lambda \cdot \frac{1}{\lambda} = 1$ ✓

### 3.2 CDF 推導

$$F(x) = \int_0^x \lambda e^{-\lambda t}\,dt = -e^{-\lambda t}\Big|_0^x = 1 - e^{-\lambda x}, \quad x \ge 0$$

因此 $P(X > x) = 1 - F(x) = e^{-\lambda x}$，這個存活函數形式很常用。

### 3.3 和 Poisson 過程的關係

設事件按照 rate = λ 的 Poisson 過程到達。令 $T$ = 第一個事件的到達時間。

$$P(T > t) = P(\text{在} [0,t] \text{內沒有事件發生}) = P(N(t) = 0) = \frac{(\lambda t)^0 e^{-\lambda t}}{0!} = e^{-\lambda t}$$

因此 $F_T(t) = 1 - e^{-\lambda t}$，這正是 Exp(λ) 的 CDF！

### 3.4 E[X] 推導

$$E[X] = \int_0^\infty x \cdot \lambda e^{-\lambda x}\,dx$$

用分部積分：令 $u = x$，$dv = \lambda e^{-\lambda x}\,dx$，則 $du = dx$，$v = -e^{-\lambda x}$。

$$= \left[-x e^{-\lambda x}\right]_0^\infty + \int_0^\infty e^{-\lambda x}\,dx = 0 + \frac{1}{\lambda} = \frac{1}{\lambda}$$

> **直覺**：如果每小時平均來 3 個客人（λ=3），那平均等第一個客人要 1/3 小時。

### 3.5 E[X^2] 推導

$$E[X^2] = \int_0^\infty x^2 \cdot \lambda e^{-\lambda x}\,dx$$

用分部積分兩次（或利用 Gamma 積分 $\int_0^\infty x^n e^{-\lambda x}\,dx = \frac{n!}{\lambda^{n+1}}$）：

$$E[X^2] = \frac{2}{\lambda^2}$$

### 3.6 Var(X) 推導

$$\text{Var}(X) = E[X^2] - (E[X])^2 = \frac{2}{\lambda^2} - \frac{1}{\lambda^2} = \frac{1}{\lambda^2}$$

所以 $\text{SD}(X) = 1/\lambda = E[X]$。Exponential 分布的標準差等於期望值！

### 3.7 MGF 推導

$$M(t) = E[e^{tX}] = \int_0^\infty e^{tx} \cdot \lambda e^{-\lambda x}\,dx = \lambda \int_0^\infty e^{-(\lambda - t)x}\,dx = \frac{\lambda}{\lambda - t}, \quad t < \lambda$$

### 3.8 Memoryless Property（無記憶性）完整推導

**定理**：若 $X \sim \text{Exp}(\lambda)$，則

$$P(X > s + t \mid X > s) = P(X > t), \quad \forall s, t > 0$$

**推導**：

$$P(X > s + t \mid X > s) = \frac{P(X > s + t \text{ 且 } X > s)}{P(X > s)}$$

因為 $\{X > s+t\} \subset \{X > s\}$，所以分子就是 $P(X > s+t)$：

$$= \frac{P(X > s+t)}{P(X > s)} = \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P(X > t) \quad \blacksquare$$

**直覺**：你已經等了 $s$ 分鐘公車沒來。Memoryless 告訴你：從現在開始，還要再等多久的分布，跟你剛到站時完全一樣。過去等的時間「白等了」，不會影響未來。

**重要事實**：Exponential 是**唯一**具有無記憶性的連續分布。（離散版本是 Geometric。）

**反向推導（Memoryless → Exponential）**：

設連續非負隨機變數 $X$ 滿足 $P(X > s+t) = P(X > s) \cdot P(X > t)$。

令 $G(t) = P(X > t)$，則 $G(s+t) = G(s) \cdot G(t)$。

這是 Cauchy 函數方程式，在 $G$ 連續且 $G(0)=1$ 的條件下，解為 $G(t) = e^{-\lambda t}$。

這恰好是 Exponential(λ) 的存活函數。

### 3.9 計算範例

**例題**：客服電話的等待時間 $X \sim \text{Exp}(0.2)$（單位：分鐘）。

(a) 求 $P(X > 10)$
(b) 已知等了 5 分鐘，求再等超過 3 分鐘的機率
(c) 求中位數

**解**：

(a) $P(X > 10) = e^{-0.2 \times 10} = e^{-2} \approx 0.1353$

(b) 由 Memoryless property：
$$P(X > 8 \mid X > 5) = P(X > 3) = e^{-0.2 \times 3} = e^{-0.6} \approx 0.5488$$

(c) 中位數 $m$ 滿足 $F(m) = 0.5$：
$$1 - e^{-0.2m} = 0.5 \implies e^{-0.2m} = 0.5 \implies m = \frac{\ln 2}{0.2} = 5\ln 2 \approx 3.466 \text{ 分鐘}$$

注意：中位數 $\approx 3.47$ < 期望值 $= 1/0.2 = 5$。Exponential 是右偏分布。

---

## 四、Gamma 分布 Gamma(α, β)

### 4.1 Gamma 函數

在定義 Gamma 分布之前，先介紹 Gamma 函數：

$$\Gamma(\alpha) = \int_0^\infty x^{\alpha-1} e^{-x}\,dx, \quad \alpha > 0$$

**關鍵性質**：

1. $\Gamma(\alpha) = (\alpha - 1)\Gamma(\alpha - 1)$（分部積分可得）
2. $\Gamma(n) = (n-1)!$（對正整數 $n$）
3. $\Gamma(1) = 1$
4. $\Gamma(1/2) = \sqrt{\pi}$

**$\Gamma(1/2) = \sqrt{\pi}$ 的推導**：

$$\Gamma(1/2) = \int_0^\infty x^{-1/2} e^{-x}\,dx$$

令 $x = u^2/2$，$dx = u\,du$：

$$= \int_0^\infty \frac{e^{-u^2/2}}{u/\sqrt{2}} \cdot u\,du = \sqrt{2}\int_0^\infty e^{-u^2/2}\,du = \sqrt{2} \cdot \frac{\sqrt{2\pi}}{2} = \sqrt{\pi}$$

（其中用了 Gauss 積分 $\int_0^\infty e^{-u^2/2}\,du = \sqrt{\pi/2}$。）

### 4.2 Gamma 分布的定義

> **注意符號**：不同教科書的參數化不同。這裡用 shape-rate 參數化：$\alpha$ = shape，$\beta$ = rate。

**PDF**：

$$f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}, \quad x > 0$$

有些教科書用 $\theta = 1/\beta$（scale parameter），則 PDF 寫成 $f(x) = \frac{x^{\alpha-1}e^{-x/\theta}}{\theta^\alpha \Gamma(\alpha)}$。**考試時務必確認用哪套參數！**

### 4.3 從 Exponential 之和推導（Erlang 分布）

**定理**：若 $X_1, X_2, \ldots, X_n$ 是 i.i.d. $\text{Exp}(\lambda)$，則 $S_n = X_1 + X_2 + \cdots + X_n \sim \text{Gamma}(n, \lambda)$。

**推導（用 MGF）**：

$$M_{X_i}(t) = \frac{\lambda}{\lambda - t}$$

因為獨立，所以

$$M_{S_n}(t) = \prod_{i=1}^n M_{X_i}(t) = \left(\frac{\lambda}{\lambda - t}\right)^n$$

這正是 $\text{Gamma}(n, \lambda)$ 的 MGF！由 MGF 的唯一性，$S_n \sim \text{Gamma}(n, \lambda)$。

> **直覺**：Poisson 過程中，第 $n$ 個事件的到達時間 = $n$ 個指數等待時間之和 = Gamma 分布。

當 $\alpha$ 是正整數時，Gamma 分布也叫做 **Erlang 分布**。

### 4.4 E[X] 推導

$$E[X] = \int_0^\infty x \cdot \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}\,dx = \frac{\beta^\alpha}{\Gamma(\alpha)} \int_0^\infty x^\alpha e^{-\beta x}\,dx$$

令 $u = \beta x$：

$$= \frac{\beta^\alpha}{\Gamma(\alpha)} \cdot \frac{1}{\beta^{\alpha+1}} \int_0^\infty u^\alpha e^{-u}\,du = \frac{1}{\beta \cdot \Gamma(\alpha)} \cdot \Gamma(\alpha+1) = \frac{\alpha\,\Gamma(\alpha)}{\beta\,\Gamma(\alpha)} = \frac{\alpha}{\beta}$$

### 4.5 Var(X) 推導

類似地，$E[X^2] = \frac{\alpha(\alpha+1)}{\beta^2}$，所以

$$\text{Var}(X) = \frac{\alpha(\alpha+1)}{\beta^2} - \left(\frac{\alpha}{\beta}\right)^2 = \frac{\alpha}{\beta^2}$$

### 4.6 MGF 推導

$$M(t) = E[e^{tX}] = \int_0^\infty e^{tx} \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}\,dx = \frac{\beta^\alpha}{\Gamma(\alpha)} \int_0^\infty x^{\alpha-1} e^{-(\beta-t)x}\,dx$$

令 $u = (\beta - t)x$：

$$= \frac{\beta^\alpha}{\Gamma(\alpha)} \cdot \frac{\Gamma(\alpha)}{(\beta-t)^\alpha} = \left(\frac{\beta}{\beta-t}\right)^\alpha, \quad t < \beta$$

### 4.7 CDF

一般情況下沒有封閉形式。當 $\alpha$ 為正整數 $n$ 時（Erlang）：

$$F(x) = 1 - \sum_{k=0}^{n-1} \frac{(\beta x)^k e^{-\beta x}}{k!}$$

這其實就是 Poisson CDF 的互補（和 Poisson 過程的關聯）。

### 4.8 計算範例

**例題**：某服務台每位客人的服務時間 $\sim \text{Exp}(2)$（rate=2，單位：分鐘/人）。求服務完 3 位客人的總時間 $T$ 的期望值、變異數和 $P(T > 3)$。

**解**：$T = X_1 + X_2 + X_3 \sim \text{Gamma}(3, 2)$

$$E[T] = \frac{\alpha}{\beta} = \frac{3}{2} = 1.5 \text{ 分鐘}$$

$$\text{Var}(T) = \frac{\alpha}{\beta^2} = \frac{3}{4} = 0.75$$

$$P(T > 3) = \sum_{k=0}^{2} \frac{(2 \times 3)^k e^{-6}}{k!} = e^{-6}\left(1 + 6 + 18\right) = 25 e^{-6} \approx 0.0620$$

---

## 五、Normal 分布 Normal(μ, σ²)

### 5.1 定義

**PDF**：

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right), \quad -\infty < x < \infty$$

**$\int_{-\infty}^{\infty} f(x)\,dx = 1$ 的驗證**（Gauss 積分）：

令 $I = \int_{-\infty}^{\infty} e^{-x^2/2}\,dx$。計算 $I^2$：

$$I^2 = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} e^{-(x^2+y^2)/2}\,dx\,dy$$

轉極座標 $x = r\cos\theta$，$y = r\sin\theta$，$dx\,dy = r\,dr\,d\theta$：

$$= \int_0^{2\pi}\int_0^\infty e^{-r^2/2} \cdot r\,dr\,d\theta = 2\pi \cdot \left[-e^{-r^2/2}\right]_0^\infty = 2\pi$$

所以 $I = \sqrt{2\pi}$。因此 $\frac{1}{\sigma\sqrt{2\pi}}\int_{-\infty}^{\infty} e^{-(x-\mu)^2/(2\sigma^2)}\,dx = 1$。✓

### 5.2 標準化

**定義**：若 $X \sim N(\mu, \sigma^2)$，令 $Z = \frac{X - \mu}{\sigma}$，則 $Z \sim N(0, 1)$。

**推導**（用變數變換）：

$z = g(x) = \frac{x-\mu}{\sigma}$，所以 $x = \sigma z + \mu$，$\frac{dx}{dz} = \sigma$。

$$f_Z(z) = f_X(\sigma z + \mu) \cdot \left|\frac{dx}{dz}\right| = \frac{1}{\sigma\sqrt{2\pi}} e^{-z^2/2} \cdot \sigma = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$$

這是標準常態的 PDF。✓

**實用公式**：

$$P(X \le x) = P\left(Z \le \frac{x-\mu}{\sigma}\right) = \Phi\left(\frac{x-\mu}{\sigma}\right)$$

其中 $\Phi$ 是標準常態的 CDF（查表值）。

### 5.3 E[X] 推導

$$E[X] = \int_{-\infty}^{\infty} x \cdot \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}\,dx$$

令 $u = x - \mu$：

$$= \int_{-\infty}^{\infty} (u+\mu) \cdot \frac{1}{\sigma\sqrt{2\pi}} e^{-u^2/(2\sigma^2)}\,du$$

$$= \underbrace{\int_{-\infty}^{\infty} \frac{u}{\sigma\sqrt{2\pi}} e^{-u^2/(2\sigma^2)}\,du}_{= 0 \text{（奇函數）}} + \mu \underbrace{\int_{-\infty}^{\infty} \frac{1}{\sigma\sqrt{2\pi}} e^{-u^2/(2\sigma^2)}\,du}_{= 1} = \mu$$

### 5.4 Var(X) 推導

$$\text{Var}(X) = E[(X-\mu)^2] = \int_{-\infty}^{\infty} (x-\mu)^2 \cdot \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}\,dx$$

令 $u = (x-\mu)/\sigma$，$dx = \sigma\,du$：

$$= \int_{-\infty}^{\infty} \sigma^2 u^2 \cdot \frac{1}{\sigma\sqrt{2\pi}} e^{-u^2/2} \cdot \sigma\,du = \sigma^2 \int_{-\infty}^{\infty} \frac{u^2}{\sqrt{2\pi}} e^{-u^2/2}\,du$$

計算 $\int_{-\infty}^{\infty} u^2 e^{-u^2/2}\,du$（分部積分，令 $w = u$，$dv = u e^{-u^2/2}\,du$）：

$$= \left[-u e^{-u^2/2}\right]_{-\infty}^{\infty} + \int_{-\infty}^{\infty} e^{-u^2/2}\,du = 0 + \sqrt{2\pi}$$

所以 $\text{Var}(X) = \sigma^2 \cdot \frac{\sqrt{2\pi}}{\sqrt{2\pi}} = \sigma^2$。

### 5.5 MGF 推導

$$M(t) = E[e^{tX}] = \int_{-\infty}^{\infty} e^{tx} \cdot \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}\,dx$$

合併指數：

$$tx - \frac{(x-\mu)^2}{2\sigma^2} = -\frac{1}{2\sigma^2}\left[(x-\mu)^2 - 2\sigma^2 tx\right]$$

配方：

$$= -\frac{1}{2\sigma^2}\left[x^2 - 2(\mu + \sigma^2 t)x + \mu^2\right] = -\frac{(x - (\mu+\sigma^2 t))^2}{2\sigma^2} + \mu t + \frac{\sigma^2 t^2}{2}$$

因此：

$$M(t) = e^{\mu t + \sigma^2 t^2/2} \cdot \underbrace{\int_{-\infty}^{\infty} \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-(\mu+\sigma^2 t))^2/(2\sigma^2)}\,dx}_{=1 \text{（常態 PDF 積分為 1）}}$$

$$\boxed{M(t) = e^{\mu t + \sigma^2 t^2/2}}$$

### 5.6 68-95-99.7 法則

| 範圍 | 機率 |
|------|------|
| $\mu \pm 1\sigma$ | $\approx 68.27\%$ |
| $\mu \pm 2\sigma$ | $\approx 95.45\%$ |
| $\mu \pm 3\sigma$ | $\approx 99.73\%$ |

**用 Z-table 驗證**：
$$P(\mu - 2\sigma \le X \le \mu + 2\sigma) = P(-2 \le Z \le 2) = \Phi(2) - \Phi(-2)$$
$$= 0.9772 - 0.0228 = 0.9544 \approx 95.45\% \checkmark$$

### 5.7 Z-table 使用方法

Z-table 給的是 $\Phi(z) = P(Z \le z)$。

**常用技巧**：

1. 對稱性：$\Phi(-z) = 1 - \Phi(z)$
2. 中間機率：$P(-a \le Z \le b) = \Phi(b) - \Phi(-a) = \Phi(b) + \Phi(a) - 1$
3. 尾端機率：$P(Z > z) = 1 - \Phi(z)$

**常用 Z 值**：

| 信賴水準 | $z_{\alpha/2}$ |
|----------|---------------|
| 90% | 1.645 |
| 95% | 1.960 |
| 99% | 2.576 |

### 5.8 Normal 的線性組合

**定理**：若 $X \sim N(\mu_X, \sigma_X^2)$ 和 $Y \sim N(\mu_Y, \sigma_Y^2)$ **獨立**，則

$$aX + bY \sim N(a\mu_X + b\mu_Y,\; a^2\sigma_X^2 + b^2\sigma_Y^2)$$

**用 MGF 推導**：

$$M_{aX+bY}(t) = M_X(at) \cdot M_Y(bt) \quad (\text{獨立})$$

$$= e^{\mu_X(at) + \sigma_X^2(at)^2/2} \cdot e^{\mu_Y(bt) + \sigma_Y^2(bt)^2/2}$$

$$= e^{(a\mu_X + b\mu_Y)t + (a^2\sigma_X^2 + b^2\sigma_Y^2)t^2/2}$$

這是 $N(a\mu_X + b\mu_Y, a^2\sigma_X^2 + b^2\sigma_Y^2)$ 的 MGF。✓

> **常見陷阱**：$X - Y$ 的變異數是 $\sigma_X^2 + \sigma_Y^2$，**不是**減！因為 $(-1)^2 = 1$。

### 5.9 計算範例

**例題**：某工廠生產螺絲，直徑 $X \sim N(10, 0.04)$（單位：mm）。規格要求直徑在 $[9.7, 10.3]$ 之間。

(a) 求合格率
(b) 求使合格率 $\ge 99\%$ 的最大允許 $\sigma$

**解**：

(a) $\sigma = \sqrt{0.04} = 0.2$

$$P(9.7 \le X \le 10.3) = P\left(\frac{9.7-10}{0.2} \le Z \le \frac{10.3-10}{0.2}\right) = P(-1.5 \le Z \le 1.5)$$

$$= \Phi(1.5) - \Phi(-1.5) = 0.9332 - 0.0668 = 0.8664 \approx 86.64\%$$

(b) 需要 $P(-0.3/\sigma \le Z \le 0.3/\sigma) \ge 0.99$

即 $2\Phi(0.3/\sigma) - 1 \ge 0.99$，所以 $\Phi(0.3/\sigma) \ge 0.995$

查表 $\Phi(2.576) = 0.995$，所以 $0.3/\sigma \ge 2.576$

$$\sigma \le \frac{0.3}{2.576} \approx 0.1165 \text{ mm}$$

---

## 六、Chi-squared 分布 χ²(n)

### 6.1 定義與推導

**定義**：若 $Z_1, Z_2, \ldots, Z_n$ 是 i.i.d. $N(0,1)$，則

$$Q = Z_1^2 + Z_2^2 + \cdots + Z_n^2 \sim \chi^2(n)$$

**$\chi^2(1)$ 的推導**：

先求 $Y = Z^2$ 的 PDF，其中 $Z \sim N(0,1)$。

用 CDF 法：
$$F_Y(y) = P(Z^2 \le y) = P(-\sqrt{y} \le Z \le \sqrt{y}) = 2\Phi(\sqrt{y}) - 1, \quad y > 0$$

微分：
$$f_Y(y) = 2\phi(\sqrt{y}) \cdot \frac{1}{2\sqrt{y}} = \frac{1}{\sqrt{y}} \cdot \frac{1}{\sqrt{2\pi}} e^{-y/2}$$

$$= \frac{1}{\sqrt{2\pi}} y^{1/2 - 1} e^{-y/2} = \frac{(1/2)^{1/2}}{\Gamma(1/2)} y^{1/2-1} e^{-y/2}$$

（因為 $\Gamma(1/2) = \sqrt{\pi}$，$\frac{1}{\sqrt{2\pi}} = \frac{(1/2)^{1/2}}{\sqrt{\pi}} = \frac{(1/2)^{1/2}}{\Gamma(1/2)}$）

這是 $\text{Gamma}(1/2, 1/2)$ 的 PDF！

### 6.2 Chi-squared 就是 Gamma

$$\chi^2(n) = \text{Gamma}(n/2, 1/2)$$

**推導**：$Q = Z_1^2 + \cdots + Z_n^2$，每個 $Z_i^2 \sim \text{Gamma}(1/2, 1/2)$。

獨立 Gamma 之和（相同 rate）：Gamma(α₁, β) + Gamma(α₂, β) = Gamma(α₁+α₂, β)

所以 $Q \sim \text{Gamma}(n/2, 1/2)$。

### 6.3 性質

$$E[\chi^2(n)] = \frac{\alpha}{\beta} = \frac{n/2}{1/2} = n$$

$$\text{Var}(\chi^2(n)) = \frac{\alpha}{\beta^2} = \frac{n/2}{1/4} = 2n$$

$$M(t) = \left(\frac{1/2}{1/2-t}\right)^{n/2} = (1-2t)^{-n/2}, \quad t < 1/2$$

### 6.4 可加性

若 $Q_1 \sim \chi^2(m)$ 且 $Q_2 \sim \chi^2(n)$ 獨立，則 $Q_1 + Q_2 \sim \chi^2(m+n)$。

### 6.5 計算範例

**例題**：$Z_1, Z_2, Z_3$ 是 i.i.d. $N(0,1)$。令 $Q = Z_1^2 + Z_2^2 + Z_3^2$。
(a) 求 $E[Q]$ 和 $\text{Var}(Q)$
(b) 求 $P(Q > 7.815)$

**解**：$Q \sim \chi^2(3)$

(a) $E[Q] = 3$，$\text{Var}(Q) = 2 \times 3 = 6$

(b) 查 $\chi^2$ 表，$\chi^2_{0.05}(3) = 7.815$，所以 $P(Q > 7.815) = 0.05$。

---

## 七、t-分布與 F-分布（簡要介紹）

### 7.1 t-分布

**定義**：若 $Z \sim N(0,1)$，$V \sim \chi^2(n)$，且 $Z$ 和 $V$ 獨立，則

$$T = \frac{Z}{\sqrt{V/n}} \sim t(n)$$

**性質**：

- $E[T] = 0$（$n > 1$）
- $\text{Var}(T) = \frac{n}{n-2}$（$n > 2$），比 1 大！t-分布比標準常態更「胖尾」
- $n \to \infty$ 時，$t(n) \to N(0,1)$
- 對稱於 0

**用途**：小樣本推論、信賴區間、假設檢定。

### 7.2 F-分布

**定義**：若 $U \sim \chi^2(m)$，$V \sim \chi^2(n)$，且獨立，則

$$F = \frac{U/m}{V/n} \sim F(m, n)$$

**性質**：

- $E[F] = \frac{n}{n-2}$（$n > 2$）
- 若 $T \sim t(n)$，則 $T^2 \sim F(1, n)$
- 若 $F \sim F(m,n)$，則 $1/F \sim F(n,m)$

**用途**：ANOVA、迴歸分析中的 F-test。

### 7.3 重要關係

$$t(n)^2 = F(1, n)$$

$$\chi^2(n)/n \xrightarrow{n\to\infty} 1$$

$$t(n) \xrightarrow{n\to\infty} N(0,1)$$

$$F(m, n) \text{ 當 } n \to \infty \text{ 時，} mF(m,n) \to \chi^2(m)$$

---

## 八、分布間的關係圖

```
                    Uniform(0,1)
                         │
                         │ X = -ln(U)/λ （反轉換法）
                         ▼
                    Exponential(λ)  ←─── Poisson 過程中第一個事件的等待時間
                         │
                         │ X₁+X₂+...+Xₙ（i.i.d. 之和）
                         ▼
                   Gamma(n, λ)     ←─── Poisson 過程中第 n 個事件的等待時間
                    （Erlang）
                         │
                  α=n/2, β=1/2    │ 當 α → ∞ 適當標準化
                         │        ▼
                    Chi-squared(n)    Normal(μ, σ²)
                         │              │
                    Z/√(V/n)           Z²
                         ▼              │
                      t(n)              ▼
                                   Chi-squared(1)
                                        │
                         ┌──────────────┘
                         ▼
                  (U/m)/(V/n) → F(m,n)
```

**關鍵推導鏈**：

1. **Uniform → Exponential**（反轉換法）：
   若 $U \sim \text{Uniform}(0,1)$，令 $X = -\frac{1}{\lambda}\ln(U)$，則 $X \sim \text{Exp}(\lambda)$。

   **推導**：$P(X \le x) = P(-\frac{1}{\lambda}\ln U \le x) = P(\ln U \ge -\lambda x) = P(U \ge e^{-\lambda x}) = 1 - e^{-\lambda x}$ ✓

2. **Exponential → Gamma**：i.i.d. Exp 之和 = Gamma（前面已推導）

3. **Normal² → Chi-squared**：$Z^2 \sim \chi^2(1) = \text{Gamma}(1/2, 1/2)$

4. **Gamma 和 Normal 的連結**：
   - $\chi^2(n) = \text{Gamma}(n/2, 1/2)$
   - 中央極限定理：適當標準化的 Gamma → Normal

---

## 九、常見陷阱整理

### 陷阱 1：Exponential 的參數混淆

- **Rate 參數化**：$f(x) = \lambda e^{-\lambda x}$，$E[X] = 1/\lambda$
- **Mean 參數化**：$f(x) = \frac{1}{\theta}e^{-x/\theta}$，$E[X] = \theta$

考試時一定要看清楚題目用哪個！

### 陷阱 2：Normal 的參數

$N(\mu, \sigma^2)$ 裡面第二個參數是**變異數**，不是標準差！

### 陷阱 3：PDF 可以大於 1

$f(x)$ 是密度，不是機率。$\text{Uniform}(0, 0.1)$ 的 PDF = 10，完全合法。

### 陷阱 4：連續型 P(X = a) = 0

所以 $P(X \le a) = P(X < a)$，等號加不加無所謂。但在離散型中就有差別！

### 陷阱 5：Gamma 的參數化

不同教科書用不同參數化。有的用 (shape, rate)，有的用 (shape, scale)。
- $\text{Gamma}(\alpha, \beta)$ 其中 $\beta$ 是 rate → $E[X] = \alpha/\beta$
- $\text{Gamma}(\alpha, \theta)$ 其中 $\theta$ 是 scale → $E[X] = \alpha\theta$

### 陷阱 6：線性組合 vs. 混合

$aX + bY$ 是線性組合（一個結果）。
$0.5 f_X + 0.5 f_Y$ 是混合分布（先抽硬幣再取值）。
兩者完全不同！

---

## 十、連續分布比較總表

| 分布 | 符號 | $E[X]$ | $\text{Var}(X)$ | MGF $M(t)$ | 支撐 |
|------|------|--------|-----------------|-------------|------|
| Uniform | $U(a,b)$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ | $\frac{e^{tb}-e^{ta}}{t(b-a)}$ | $[a,b]$ |
| Exponential | $\text{Exp}(\lambda)$ | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ | $\frac{\lambda}{\lambda-t}$ | $[0,\infty)$ |
| Gamma | $\text{Ga}(\alpha,\beta)$ | $\frac{\alpha}{\beta}$ | $\frac{\alpha}{\beta^2}$ | $\left(\frac{\beta}{\beta-t}\right)^\alpha$ | $[0,\infty)$ |
| Normal | $N(\mu,\sigma^2)$ | $\mu$ | $\sigma^2$ | $e^{\mu t+\sigma^2 t^2/2}$ | $(-\infty,\infty)$ |
| Chi-squared | $\chi^2(n)$ | $n$ | $2n$ | $(1-2t)^{-n/2}$ | $[0,\infty)$ |
| t-分布 | $t(n)$ | $0$ | $\frac{n}{n-2}$ | 無封閉形式 | $(-\infty,\infty)$ |
| F-分布 | $F(m,n)$ | $\frac{n}{n-2}$ | 複雜 | 無封閉形式 | $[0,\infty)$ |

**分布特殊關係速查**：

| 關係 | 說明 |
|------|------|
| $\text{Exp}(\lambda) = \text{Gamma}(1, \lambda)$ | Exponential 是 Gamma 的特例 |
| $\chi^2(n) = \text{Gamma}(n/2, 1/2)$ | Chi-squared 是 Gamma 的特例 |
| $\chi^2(2) = \text{Exp}(1/2)$ | $n=2$ 的 Chi-squared 等於 Exponential |
| $\sum_{i=1}^n \text{Exp}(\lambda) = \text{Gamma}(n,\lambda)$ | i.i.d. Exp 之和 |
| $Z^2 = \chi^2(1)$ | 標準常態的平方 |
| $t(n)^2 = F(1,n)$ | t 的平方是 F |

---

## 十一、補充範例：綜合應用

**例題**：令 $X_1, X_2, \ldots, X_{25}$ 為 i.i.d. $N(50, 16)$。令 $\bar{X} = \frac{1}{25}\sum X_i$。

(a) 求 $\bar{X}$ 的分布
(b) 求 $P(\bar{X} > 51.5)$
(c) 求 $P(48 < \bar{X} < 52)$

**解**：

(a) 因為 Normal 的線性組合仍是 Normal：
$$\bar{X} = \frac{1}{25}\sum_{i=1}^{25} X_i \sim N\left(50, \frac{16}{25}\right) = N(50, 0.64)$$

$E[\bar{X}] = 50$，$\text{Var}(\bar{X}) = 16/25 = 0.64$，$\text{SD}(\bar{X}) = 0.8$

(b)
$$P(\bar{X} > 51.5) = P\left(Z > \frac{51.5 - 50}{0.8}\right) = P(Z > 1.875) = 1 - \Phi(1.875)$$

查表（內插）：$\Phi(1.87) = 0.9693$，$\Phi(1.88) = 0.9699$

$\Phi(1.875) \approx 0.9696$

$$P(\bar{X} > 51.5) \approx 1 - 0.9696 = 0.0304$$

(c)
$$P(48 < \bar{X} < 52) = P\left(\frac{48-50}{0.8} < Z < \frac{52-50}{0.8}\right) = P(-2.5 < Z < 2.5)$$

$$= \Phi(2.5) - \Phi(-2.5) = 0.9938 - 0.0062 = 0.9876$$

---

*下一講：聯合分布與變數轉換*
