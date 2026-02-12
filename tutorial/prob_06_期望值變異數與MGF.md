# 期望值、變異數與 MGF

> 台大機率統計教學講義 — 從期望值到動差生成函數，計算工具大全

---

## 一、期望值 E[X] 的定義與性質

### 1.1 定義

**離散型**：

$$E[X] = \sum_x x \cdot p_X(x)$$

**連續型**：

$$E[X] = \int_{-\infty}^{\infty} x \cdot f_X(x)\,dx$$

**直覺**：期望值是隨機變數的「加權平均」，權重就是機率（密度）。如果你做這個實驗無限多次，把結果平均起來，就會趨近期望值。

### 1.2 期望值的線性性（完整推導）

**定理**：$E[aX + bY + c] = aE[X] + bE[Y] + c$

這個性質**不需要獨立性**！即使 $X$ 和 $Y$ 高度相關，線性性都成立。

**推導**（連續型，離散型類似）：

$$E[aX + bY + c] = \int\int (ax + by + c) f_{X,Y}(x,y)\,dx\,dy$$

$$= a\int\int x \cdot f_{X,Y}(x,y)\,dx\,dy + b\int\int y \cdot f_{X,Y}(x,y)\,dx\,dy + c\int\int f_{X,Y}(x,y)\,dx\,dy$$

第一項：$\int\int x \cdot f_{X,Y}(x,y)\,dx\,dy = \int x \left[\int f_{X,Y}(x,y)\,dy\right]dx = \int x \cdot f_X(x)\,dx = E[X]$

第二項同理 $= E[Y]$。第三項 $= c \cdot 1 = c$。

所以 $E[aX + bY + c] = aE[X] + bE[Y] + c$。$\blacksquare$

**推廣**：

$$E\left[\sum_{i=1}^n a_i X_i\right] = \sum_{i=1}^n a_i E[X_i]$$

不管 $X_i$ 之間是否獨立！

### 1.3 期望值的其他性質

1. **非負隨機變數**：若 $X \ge 0$，則 $E[X] \ge 0$
2. **保序性**：若 $X \le Y$（幾乎確定），則 $E[X] \le E[Y]$
3. **乘積**：若 $X, Y$ **獨立**，則 $E[XY] = E[X] \cdot E[Y]$（注意：需要獨立！）
4. **三角不等式**：$|E[X]| \le E[|X|]$

**乘積期望值推導**（獨立時）：

$$E[XY] = \int\int xy \cdot f_{X,Y}(x,y)\,dx\,dy = \int\int xy \cdot f_X(x)f_Y(y)\,dx\,dy$$

$$= \left[\int x f_X(x)\,dx\right]\left[\int y f_Y(y)\,dy\right] = E[X] \cdot E[Y] \quad \blacksquare$$

---

## 二、LOTUS（Law of the Unconscious Statistician）

### 2.1 定理

**不需要先求 $Y = g(X)$ 的分布**，就能直接算 $E[g(X)]$：

**離散型**：

$$E[g(X)] = \sum_x g(x) \cdot p_X(x)$$

**連續型**：

$$E[g(X)] = \int_{-\infty}^{\infty} g(x) \cdot f_X(x)\,dx$$

### 2.2 為什麼叫「無意識統計學家法則」？

因為你不需要知道 $g(X)$ 的分布，只需要知道 $X$ 的分布就行。就好像「無意識」地把 $g(x)$ 丟進去乘 $f_X(x)$ 積分。

### 2.3 為什麼成立？（推導）

令 $Y = g(X)$。我們知道 $Y$ 有自己的 PDF $f_Y(y)$，所以

$$E[Y] = \int_{-\infty}^{\infty} y \cdot f_Y(y)\,dy$$

我們要證明這等於 $\int g(x) f_X(x)\,dx$。

用 CDF 法的精神：$f_Y(y)\,dy$ 對應的 $x$ 值使得 $g(x) = y$。在變數變換 $y = g(x)$ 下：

$$\int y \cdot f_Y(y)\,dy = \int g(x) \cdot f_X(x)\,dx$$

（嚴格的證明需要測度論，但直覺上是成立的。）

### 2.4 LOTUS 的威力 — 範例

**例題**：$X \sim \text{Exp}(1)$，求 $E[\sqrt{X}]$。

**不用 LOTUS**：先求 $Y = \sqrt{X}$ 的 PDF（用 CDF 法或變數變換），再算 $E[Y] = \int y f_Y(y)\,dy$。

**用 LOTUS**（直接算！）：

$$E[\sqrt{X}] = \int_0^\infty \sqrt{x} \cdot e^{-x}\,dx = \int_0^\infty x^{1/2} e^{-x}\,dx = \Gamma(3/2) = \frac{1}{2}\Gamma(1/2) = \frac{\sqrt{\pi}}{2}$$

（利用了 $\Gamma(\alpha) = \int_0^\infty x^{\alpha-1}e^{-x}\,dx$ 和 $\Gamma(3/2) = \frac{1}{2}\Gamma(1/2) = \frac{\sqrt{\pi}}{2}$）

### 2.5 二維 LOTUS

$$E[g(X,Y)] = \int\int g(x,y) f_{X,Y}(x,y)\,dx\,dy$$

特別常用：$E[XY]$, $E[(X-\mu_X)(Y-\mu_Y)]$ 等。

---

## 三、變異數 Var(X)

### 3.1 定義

$$\text{Var}(X) = E[(X - E[X])^2] = E[(X - \mu)^2]$$

**直覺**：衡量 $X$ 偏離期望值的「平均程度」。

### 3.2 計算公式推導

$$\text{Var}(X) = E[(X-\mu)^2] = E[X^2 - 2\mu X + \mu^2]$$

$$= E[X^2] - 2\mu E[X] + \mu^2 = E[X^2] - 2\mu^2 + \mu^2$$

$$\boxed{\text{Var}(X) = E[X^2] - (E[X])^2}$$

> **口訣**：「平方的期望 減 期望的平方」。

### 3.3 性質

1. $\text{Var}(X) \ge 0$（$= 0$ $\iff$ $X$ 是常數）
2. $\text{Var}(aX + b) = a^2 \text{Var}(X)$
3. **$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$**
4. 若 $X, Y$ **獨立**，$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$

**性質 2 的推導**：

$$\text{Var}(aX + b) = E[(aX+b)^2] - (E[aX+b])^2$$

$$= E[a^2X^2 + 2abX + b^2] - (aE[X]+b)^2$$

$$= a^2E[X^2] + 2abE[X] + b^2 - a^2(E[X])^2 - 2abE[X] - b^2$$

$$= a^2(E[X^2] - (E[X])^2) = a^2\text{Var}(X) \quad \blacksquare$$

> **常見陷阱**：$\text{Var}(X - Y) = \text{Var}(X) + \text{Var}(Y)$（獨立時），是**加**不是**減**！因為 $(-1)^2 = 1$。

### 3.4 範例

**例題**：$X \sim \text{Binomial}(n, p)$。用定義推導 $\text{Var}(X)$。

**解**：$X = \sum_{i=1}^n X_i$，其中 $X_i \sim \text{Bernoulli}(p)$ 獨立。

$$E[X_i^2] = 0^2 \cdot (1-p) + 1^2 \cdot p = p$$

$$\text{Var}(X_i) = E[X_i^2] - (E[X_i])^2 = p - p^2 = p(1-p)$$

因為 $X_i$ 獨立：

$$\text{Var}(X) = \sum_{i=1}^n \text{Var}(X_i) = np(1-p)$$

---

## 四、Covariance 和 Correlation

### 4.1 Covariance 定義

$$\text{Cov}(X, Y) = E[(X - E[X])(Y - E[Y])]$$

**計算公式**：

$$\text{Cov}(X, Y) = E[XY] - E[X]E[Y]$$

**推導**：

$$\text{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)] = E[XY - \mu_X Y - X\mu_Y + \mu_X\mu_Y]$$

$$= E[XY] - \mu_X E[Y] - E[X]\mu_Y + \mu_X\mu_Y = E[XY] - \mu_X\mu_Y$$

### 4.2 Covariance 的性質

1. $\text{Cov}(X, X) = \text{Var}(X)$
2. $\text{Cov}(X, Y) = \text{Cov}(Y, X)$（對稱）
3. $\text{Cov}(aX, bY) = ab\,\text{Cov}(X, Y)$
4. $\text{Cov}(X + Y, Z) = \text{Cov}(X, Z) + \text{Cov}(Y, Z)$（**雙線性性**）
5. 獨立 $\Rightarrow$ $\text{Cov}(X, Y) = 0$（反之不一定！）
6. $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$

**性質 6 的推導**：

$$\text{Var}(X+Y) = E[(X+Y-\mu_X-\mu_Y)^2] = E[((X-\mu_X)+(Y-\mu_Y))^2]$$

$$= E[(X-\mu_X)^2] + 2E[(X-\mu_X)(Y-\mu_Y)] + E[(Y-\mu_Y)^2]$$

$$= \text{Var}(X) + 2\text{Cov}(X,Y) + \text{Var}(Y) \quad \blacksquare$$

**推廣**：

$$\text{Var}\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2\sum_{i<j} \text{Cov}(X_i, X_j)$$

### 4.3 Correlation（相關係數）

$$\rho(X, Y) = \text{Corr}(X, Y) = \frac{\text{Cov}(X, Y)}{\sqrt{\text{Var}(X)\text{Var}(Y)}} = \frac{\text{Cov}(X,Y)}{\text{SD}(X)\text{SD}(Y)}$$

**性質**：

1. $-1 \le \rho \le 1$
2. $|\rho| = 1$ $\iff$ $Y = aX + b$（完美線性關係）
3. $\rho = 0$ 稱為**不相關（uncorrelated）**
4. 獨立 $\Rightarrow$ 不相關，但不相關 $\not\Rightarrow$ 獨立

**$|\rho| \le 1$ 的推導（用 Cauchy-Schwarz 不等式）**：

Cauchy-Schwarz：$(E[UV])^2 \le E[U^2]E[V^2]$

令 $U = X - \mu_X$，$V = Y - \mu_Y$：

$$(E[(X-\mu_X)(Y-\mu_Y)])^2 \le E[(X-\mu_X)^2]E[(Y-\mu_Y)^2]$$

$$\text{Cov}(X,Y)^2 \le \text{Var}(X)\text{Var}(Y)$$

$$\rho^2 \le 1 \quad \Rightarrow \quad |\rho| \le 1 \quad \blacksquare$$

### 4.4 不相關但不獨立的經典例子

令 $X \sim N(0,1)$，$Y = X^2$。

$$\text{Cov}(X, Y) = E[XY] - E[X]E[Y] = E[X^3] - 0 \cdot E[X^2] = 0$$

（因為 $X^3$ 是奇函數，$X$ 對稱於 0，所以 $E[X^3] = 0$）

所以 $\rho = 0$，$X$ 和 $Y$ 不相關。但 $Y = X^2$ 完全由 $X$ 決定，當然**不獨立**！

> **教訓**：不相關只表示「沒有線性關係」，不代表「沒有任何關係」。

### 4.5 範例

**例題**：公平骰子擲一次，$X$ = 點數，$Y = (X-3.5)^2$。求 $\text{Cov}(X, Y)$ 和 $\rho(X, Y)$。

**解**：

$E[X] = 3.5$

$E[X^2] = \frac{1}{6}(1+4+9+16+25+36) = \frac{91}{6}$

$\text{Var}(X) = \frac{91}{6} - 3.5^2 = \frac{91}{6} - \frac{49}{4} = \frac{182-147}{12} = \frac{35}{12}$

$Y = (X-3.5)^2$，所以 $XY = X(X-3.5)^2$。

$E[XY] = E[X(X-3.5)^2] = E[X^3 - 7X^2 + 12.25X]$

$E[X^3] = \frac{1}{6}(1+8+27+64+125+216) = \frac{441}{6} = 73.5$

$E[XY] = 73.5 - 7 \times \frac{91}{6} + 12.25 \times 3.5 = 73.5 - \frac{637}{6} + 42.875$

$= 73.5 - 106.1\overline{6} + 42.875 = 10.208\overline{3}$

$E[Y] = E[(X-3.5)^2] = \text{Var}(X) = \frac{35}{12}$

$\text{Cov}(X, Y) = E[XY] - E[X]E[Y] = 10.208\overline{3} - 3.5 \times \frac{35}{12} = 10.208\overline{3} - 10.208\overline{3} = 0$

所以 $\text{Cov}(X,Y) = 0$，$\rho(X,Y) = 0$。

> 又一個不相關但不獨立的例子！$Y$ 完全由 $X$ 決定，但線性相關為零。原因是 $Y = (X-\mu)^2$ 對 $X-\mu$ 是偶函數，而 $X-\mu$ 的分布對稱於零。

---

## 五、條件期望值

### 5.1 定義

**離散型**：

$$E[X | Y=y] = \sum_x x \cdot p_{X|Y}(x|y)$$

**連續型**：

$$E[X | Y=y] = \int_{-\infty}^{\infty} x \cdot f_{X|Y}(x|y)\,dx$$

$E[X|Y]$（不寫 $=y$）是一個**隨機變數**，它是 $Y$ 的函數。

### 5.2 全期望值法則（Law of Total Expectation / Adam's Law）

$$\boxed{E[X] = E[E[X|Y]]}$$

**推導**（連續型）：

$$E[E[X|Y]] = \int E[X|Y=y] \cdot f_Y(y)\,dy$$

$$= \int \left[\int x \cdot f_{X|Y}(x|y)\,dx\right] f_Y(y)\,dy$$

$$= \int\int x \cdot f_{X|Y}(x|y) f_Y(y)\,dx\,dy$$

$$= \int\int x \cdot f_{X,Y}(x,y)\,dx\,dy$$

$$= \int x \left[\int f_{X,Y}(x,y)\,dy\right]dx = \int x \cdot f_X(x)\,dx = E[X] \quad \blacksquare$$

### 5.3 全期望值法則的應用

**例題**：一個工廠有兩條生產線。生產線 A 佔 60% 的產量，不良率 2%；生產線 B 佔 40%，不良率 5%。隨機抽一個產品，求期望不良品數（0 或 1）。

**解**：令 $X = 1$ 表示不良品，$Y$ = 生產線（A 或 B）。

$$E[X] = E[E[X|Y]] = E[X|Y=A] \cdot P(Y=A) + E[X|Y=B] \cdot P(Y=B)$$

$$= 0.02 \times 0.6 + 0.05 \times 0.4 = 0.012 + 0.02 = 0.032$$

### 5.4 更深入的範例

**例題**：擲一個公平骰子得到 $N$，然後擲 $N$ 枚公平硬幣。令 $X$ = 正面次數。求 $E[X]$ 和 $\text{Var}(X)$。

**解**：

**求 $E[X]$**（用全期望值法則）：

$$E[X|N=n] = n \cdot \frac{1}{2} = \frac{n}{2}$$

$$E[X] = E[E[X|N]] = E\left[\frac{N}{2}\right] = \frac{E[N]}{2} = \frac{3.5}{2} = 1.75$$

（$\text{Var}(X)$ 的計算見下一節 Eve's Law。）

---

## 六、條件變異數公式（Eve's Law）

### 6.1 公式

$$\boxed{\text{Var}(X) = E[\text{Var}(X|Y)] + \text{Var}(E[X|Y])}$$

名稱由來：**E**xpected **V**alue of **V**ariance + **V**ariance of **E**xpected value → **EVVE** → Eve。

也有人記成 **Adam and Eve's Law**（全期望值 = Adam's Law，全變異數 = Eve's Law）。

### 6.2 推導

**Step 1**：定義。令 $\mu(y) = E[X|Y=y]$，$v(y) = \text{Var}(X|Y=y) = E[X^2|Y=y] - (E[X|Y=y])^2$。

**Step 2**：全期望值法則給出

$$E[X] = E[\mu(Y)]$$

$$E[X^2] = E[E[X^2|Y]]$$

**Step 3**：

$$E[\text{Var}(X|Y)] = E[E[X^2|Y] - (\mu(Y))^2] = E[E[X^2|Y]] - E[(\mu(Y))^2]$$

$$= E[X^2] - E[\mu(Y)^2]$$

$$\text{Var}(E[X|Y]) = \text{Var}(\mu(Y)) = E[\mu(Y)^2] - (E[\mu(Y)])^2 = E[\mu(Y)^2] - (E[X])^2$$

**Step 4**：相加

$$E[\text{Var}(X|Y)] + \text{Var}(E[X|Y]) = E[X^2] - E[\mu(Y)^2] + E[\mu(Y)^2] - (E[X])^2$$

$$= E[X^2] - (E[X])^2 = \text{Var}(X) \quad \blacksquare$$

### 6.3 直覺

$$\text{Var}(X) = \underbrace{E[\text{Var}(X|Y)]}_{\text{組內變異}} + \underbrace{\text{Var}(E[X|Y])}_{\text{組間變異}}$$

- **組內變異**：在每個 $Y = y$ 的條件下，$X$ 還有多少隨機性？取平均。
- **組間變異**：不同的 $Y$ 值導致 $E[X|Y]$ 不同，這種「均值的波動」有多大？

> **ANOVA 的精神**：總變異 = 組內變異 + 組間變異。

### 6.4 範例（續）

**例題**（續上一節）：擲骰子得 $N$，擲 $N$ 枚硬幣得正面數 $X$。求 $\text{Var}(X)$。

**解**：

$$E[X|N] = \frac{N}{2}, \quad \text{Var}(X|N) = N \cdot \frac{1}{2} \cdot \frac{1}{2} = \frac{N}{4}$$

**組內變異**：

$$E[\text{Var}(X|N)] = E\left[\frac{N}{4}\right] = \frac{E[N]}{4} = \frac{3.5}{4} = 0.875$$

**組間變異**：

$$\text{Var}(E[X|N]) = \text{Var}\left(\frac{N}{2}\right) = \frac{1}{4}\text{Var}(N) = \frac{1}{4} \cdot \frac{35}{12} = \frac{35}{48} \approx 0.7292$$

**總變異**：

$$\text{Var}(X) = 0.875 + 0.7292 = \frac{42}{48} + \frac{35}{48} = \frac{77}{48} \approx 1.6042$$

---

## 七、MGF（動差生成函數）完整教學

### 7.1 定義

$$M_X(t) = E[e^{tX}]$$

**離散型**：$M_X(t) = \sum_x e^{tx} p_X(x)$

**連續型**：$M_X(t) = \int_{-\infty}^{\infty} e^{tx} f_X(x)\,dx$

> **為什麼叫「動差生成函數」？** 因為它可以「生成」所有動差（moments）。

### 7.2 為什麼 M^(k)(0) = E[X^k]（推導）

$$M_X(t) = E[e^{tX}] = E\left[\sum_{k=0}^{\infty} \frac{(tX)^k}{k!}\right] = \sum_{k=0}^{\infty} \frac{t^k}{k!} E[X^k]$$

（交換求和和期望值，在 MGF 存在的條件下合法）

這是 $M_X(t)$ 在 $t = 0$ 的 Taylor 展開！所以

$$M_X^{(k)}(0) = E[X^k]$$

**具體驗證**：

$$M'(t) = E[Xe^{tX}] \quad \Rightarrow \quad M'(0) = E[X]$$

$$M''(t) = E[X^2 e^{tX}] \quad \Rightarrow \quad M''(0) = E[X^2]$$

所以 $\text{Var}(X) = M''(0) - (M'(0))^2$。

### 7.3 範例：用 MGF 求動差

**例題**：$X \sim \text{Exp}(\lambda)$，$M_X(t) = \frac{\lambda}{\lambda - t}$。求 $E[X]$ 和 $E[X^2]$。

$$M'(t) = \frac{\lambda}{(\lambda-t)^2} \quad \Rightarrow \quad M'(0) = \frac{\lambda}{\lambda^2} = \frac{1}{\lambda} = E[X] \checkmark$$

$$M''(t) = \frac{2\lambda}{(\lambda-t)^3} \quad \Rightarrow \quad M''(0) = \frac{2\lambda}{\lambda^3} = \frac{2}{\lambda^2} = E[X^2] \checkmark$$

$$\text{Var}(X) = \frac{2}{\lambda^2} - \frac{1}{\lambda^2} = \frac{1}{\lambda^2} \checkmark$$

### 7.4 MGF 的唯一性定理

**定理**：如果兩個隨機變數 $X$ 和 $Y$ 的 MGF 在 $t = 0$ 的某個鄰域 $(-h, h)$ 上相等，即

$$M_X(t) = M_Y(t), \quad \forall t \in (-h, h)$$

則 $X$ 和 $Y$ 有相同的分布。

> **用途**：如果你算出某個隨機變數的 MGF，發現它跟某個已知分布的 MGF 長得一樣，就可以直接辨認分布！不需要反推 PDF。

### 7.5 獨立 RV 之和的 MGF = 各 MGF 之積（推導）

**定理**：若 $X$ 和 $Y$ **獨立**，則

$$M_{X+Y}(t) = M_X(t) \cdot M_Y(t)$$

**推導**：

$$M_{X+Y}(t) = E[e^{t(X+Y)}] = E[e^{tX} \cdot e^{tY}]$$

因為 $X, Y$ 獨立，$e^{tX}$ 和 $e^{tY}$ 也獨立（獨立的函數仍獨立）：

$$= E[e^{tX}] \cdot E[e^{tY}] = M_X(t) \cdot M_Y(t) \quad \blacksquare$$

**推廣**：若 $X_1, \ldots, X_n$ 獨立，

$$M_{X_1 + \cdots + X_n}(t) = \prod_{i=1}^n M_{X_i}(t)$$

### 7.6 用 MGF 辨識分布的範例

**例題**：$X_1, X_2$ i.i.d. $\sim \text{Poisson}(\lambda)$。求 $S = X_1 + X_2$ 的分布。

**解**：

$$M_{X_i}(t) = e^{\lambda(e^t - 1)}$$

$$M_S(t) = M_{X_1}(t) \cdot M_{X_2}(t) = e^{\lambda(e^t-1)} \cdot e^{\lambda(e^t-1)} = e^{2\lambda(e^t-1)}$$

這是 $\text{Poisson}(2\lambda)$ 的 MGF！所以 $S \sim \text{Poisson}(2\lambda)$。

**例題**：$X \sim \text{Gamma}(3, 2)$，$Y \sim \text{Gamma}(5, 2)$，獨立。求 $X + Y$ 的分布。

$$M_{X+Y}(t) = \left(\frac{2}{2-t}\right)^3 \cdot \left(\frac{2}{2-t}\right)^5 = \left(\frac{2}{2-t}\right)^8$$

這是 $\text{Gamma}(8, 2)$ 的 MGF。所以 $X + Y \sim \text{Gamma}(8, 2)$。

> **注意**：Gamma 的可加性要求 rate 參數相同！$\text{Gamma}(\alpha_1, \beta) + \text{Gamma}(\alpha_2, \beta) = \text{Gamma}(\alpha_1 + \alpha_2, \beta)$。如果 $\beta$ 不同就不行。

### 7.7 MGF 不存在的情形

不是所有分布都有 MGF。例如 Cauchy 分布和 Log-Normal 分布的 MGF 不存在（$E[e^{tX}] = \infty$）。

這時候可以用**特徵函數（characteristic function）** $\varphi_X(t) = E[e^{itX}]$，它對所有分布都存在。

---

## 八、指標變數法（Indicator Method）

### 8.1 概念

**指標隨機變數（Indicator RV）**的定義：

$$I_A = \begin{cases} 1, & \text{事件 } A \text{ 發生} \\ 0, & \text{事件 } A \text{ 不發生} \end{cases}$$

$I_A \sim \text{Bernoulli}(P(A))$，所以 $E[I_A] = P(A)$。

### 8.2 核心思想

把一個複雜的隨機變數拆成指標變數之和：

$$X = \sum_{i} I_{A_i}$$

然後利用期望值的線性性：

$$E[X] = \sum_{i} E[I_{A_i}] = \sum_{i} P(A_i)$$

**這裡完全不需要 $I_{A_i}$ 之間獨立！**

### 8.3 範例 1：Fixed Points（錯排問題）

**題目**：$n$ 個人隨機排列，$X$ = 回到原位的人數（fixed points）。求 $E[X]$。

**解**：

令 $I_i = \mathbf{1}[\text{第 } i \text{ 個人回到原位}]$，$i = 1, \ldots, n$。

$$X = \sum_{i=1}^n I_i$$

$$E[I_i] = P(\text{第 } i \text{ 個人回到原位}) = \frac{(n-1)!}{n!} = \frac{1}{n}$$

$$E[X] = \sum_{i=1}^n \frac{1}{n} = 1$$

> 不管 $n$ 多大，平均 fixed point 數恆為 1！

**進階**：求 $\text{Var}(X)$。

$$\text{Var}(X) = \text{Var}\left(\sum I_i\right) = \sum \text{Var}(I_i) + 2\sum_{i<j}\text{Cov}(I_i, I_j)$$

$\text{Var}(I_i) = \frac{1}{n}(1-\frac{1}{n}) = \frac{n-1}{n^2}$

$\text{Cov}(I_i, I_j) = E[I_i I_j] - E[I_i]E[I_j]$

$E[I_i I_j] = P(\text{第 } i \text{ 和第 } j \text{ 都回到原位}) = \frac{(n-2)!}{n!} = \frac{1}{n(n-1)}$

$\text{Cov}(I_i, I_j) = \frac{1}{n(n-1)} - \frac{1}{n^2} = \frac{n - (n-1)}{n^2(n-1)} = \frac{1}{n^2(n-1)}$

$$\text{Var}(X) = n \cdot \frac{n-1}{n^2} + 2\binom{n}{2} \cdot \frac{1}{n^2(n-1)}$$

$$= \frac{n-1}{n} + \frac{n(n-1)}{1} \cdot \frac{1}{n^2(n-1)} = \frac{n-1}{n} + \frac{1}{n} = 1$$

所以 $\text{Var}(X) = 1$，也是跟 $n$ 無關！（事實上 $X$ 近似 $\text{Poisson}(1)$。）

### 8.4 範例 2：Coupon Collector Problem

**題目**：有 $n$ 種優惠券，每次隨機得到一種（等機率）。求集齊所有 $n$ 種需要的次數的期望值 $E[T]$。

**解**：

令 $T_i$ = 已經收集了 $i-1$ 種後，得到第 $i$ 種新券需要的次數。

當已有 $i-1$ 種時，得到新券的機率 = $\frac{n-(i-1)}{n} = \frac{n-i+1}{n}$。

所以 $T_i \sim \text{Geometric}\left(\frac{n-i+1}{n}\right)$，$E[T_i] = \frac{n}{n-i+1}$。

$$T = T_1 + T_2 + \cdots + T_n$$

$$E[T] = \sum_{i=1}^n \frac{n}{n-i+1} = n\sum_{k=1}^n \frac{1}{k} = nH_n$$

其中 $H_n = 1 + \frac{1}{2} + \frac{1}{3} + \cdots + \frac{1}{n}$ 是第 $n$ 個調和數。

**數值例子**：$n = 50$ 種寶可夢卡：

$$E[T] = 50 \times H_{50} \approx 50 \times 4.499 \approx 225$$

平均要買 225 包才能集齊！

> 嚴格來說這題用的是 Geometric 之和，不完全是指標變數法。但核心精神一樣：把複雜問題拆成簡單的獨立部分。

### 8.5 範例 3：Birthday Problem 變形

**題目**：$k$ 個人中，「至少有一對同生日」的期望對數是多少？（$n = 365$ 天）

**解**：

令 $I_{ij} = \mathbf{1}[\text{第 } i \text{ 和第 } j \text{ 同生日}]$，$1 \le i < j \le k$。

「同生日的對數」$= X = \sum_{i<j} I_{ij}$。

$$E[I_{ij}] = P(\text{同生日}) = \frac{1}{365}$$

$$E[X] = \binom{k}{2} \cdot \frac{1}{365} = \frac{k(k-1)}{730}$$

若 $k = 23$：$E[X] = \frac{23 \times 22}{730} = \frac{506}{730} \approx 0.693$

若 $k = 50$：$E[X] = \frac{50 \times 49}{730} \approx 3.356$

> 注意：$E[X] \ge 1$ 不代表「一定有同生日」（期望值 $\ge 1$ 不等於機率 = 1）。但結合 Birthday Problem 的經典結論（23 人時機率 $\approx 50.7\%$），這個期望值是合理的。

---

## 九、Markov 不等式和 Chebyshev 不等式

### 9.1 Markov 不等式

**定理**：若 $X \ge 0$，$a > 0$，則

$$P(X \ge a) \le \frac{E[X]}{a}$$

**推導**：

$$E[X] = \int_0^\infty x f(x)\,dx \ge \int_a^\infty x f(x)\,dx \ge \int_a^\infty a f(x)\,dx = a \cdot P(X \ge a)$$

$$\Rightarrow P(X \ge a) \le \frac{E[X]}{a} \quad \blacksquare$$

> **直覺**：如果一個非負隨機變數的平均值很小，那麼它很少會取到很大的值。

**範例**：某班平均成績 70 分，求「成績 $\ge 90$ 分」的人數上界。

$$P(X \ge 90) \le \frac{70}{90} = \frac{7}{9} \approx 77.8\%$$

這個上界很鬆！Markov 不等式的威力在於它幾乎不需要任何假設。

### 9.2 Chebyshev 不等式

**定理**：對任何隨機變數 $X$（有有限的前兩階動差），

$$P(|X - \mu| \ge k\sigma) \le \frac{1}{k^2}$$

等價地：$P(|X - \mu| \ge c) \le \frac{\sigma^2}{c^2}$

**推導**（從 Markov 推導）：

令 $Y = (X - \mu)^2 \ge 0$。套 Markov 不等式：

$$P(Y \ge c^2) \le \frac{E[Y]}{c^2} = \frac{\sigma^2}{c^2}$$

但 $P(Y \ge c^2) = P((X-\mu)^2 \ge c^2) = P(|X-\mu| \ge c)$。

令 $c = k\sigma$：

$$P(|X-\mu| \ge k\sigma) \le \frac{\sigma^2}{k^2\sigma^2} = \frac{1}{k^2} \quad \blacksquare$$

### 9.3 Chebyshev 的應用

| $k$ | $P(\|X-\mu\| \ge k\sigma) \le$ | 對 Normal 的真實值 |
|-----|-------------------------------|-------------------|
| 1 | 100%（無意義） | 31.73% |
| 2 | 25% | 4.55% |
| 3 | 11.1% | 0.27% |
| 4 | 6.25% | 0.0063% |

Chebyshev 給的是**不管什麼分布都成立**的上界，所以比較鬆。但它的優點是**完全不需要知道分布的形狀**。

### 9.4 範例

**例題**：一台機器每小時產出的合格品數 $X$ 有 $\mu = 100$，$\sigma = 5$。不知道分布，求 $P(85 \le X \le 115)$ 的下界。

**解**：

$$P(|X - 100| \ge 15) \le \frac{25}{225} = \frac{1}{9}$$

所以

$$P(85 \le X \le 115) = P(|X-100| < 15) \ge 1 - \frac{1}{9} = \frac{8}{9} \approx 88.9\%$$

### 9.5 弱大數法則（Chebyshev 的重要應用）

**定理**：$X_1, X_2, \ldots$ i.i.d.，$E[X_i] = \mu$，$\text{Var}(X_i) = \sigma^2 < \infty$。令 $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$。

則對任意 $\epsilon > 0$：

$$P(|\bar{X}_n - \mu| \ge \epsilon) \to 0, \quad n \to \infty$$

**推導**：

$$E[\bar{X}_n] = \mu, \quad \text{Var}(\bar{X}_n) = \frac{\sigma^2}{n}$$

由 Chebyshev：

$$P(|\bar{X}_n - \mu| \ge \epsilon) \le \frac{\text{Var}(\bar{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2} \to 0 \quad \blacksquare$$

---

## 十、更多完整計算範例

### 範例 1：全期望值法則 + 條件推理

**題目**：盒子裡有 3 紅球 2 白球。隨機取出一球，如果是紅球就再放回 1 紅球 1 白球；如果是白球就不改變。然後從（可能改變了的）盒子中再取一球。令 $X$ = 第二次取出紅球數（0 或 1）。求 $E[X]$。

**解**：

令 $Y$ = 第一次取出的球色。

$P(Y = \text{紅}) = 3/5$，$P(Y = \text{白}) = 2/5$

**若 $Y = \text{紅}$**：盒子變成 4 紅 3 白（共 7 球）。$E[X|Y=\text{紅}] = P(\text{第二次紅}|Y=\text{紅}) = 4/7$

**若 $Y = \text{白}$**：盒子不變，仍然 3 紅 2 白（但第一次取出的球沒有說放回，需要釐清題意。這裡假設第一次取出不放回）。

重新看題目：假設第一次取出的球不放回（只是根據顏色決定是否加球）。

**若 $Y = \text{紅}$**：取出 1 紅，剩 2 紅 2 白，然後加入 1 紅 1 白 → 3 紅 3 白（6 球）。$E[X|Y=\text{紅}] = 3/6 = 1/2$

**若 $Y = \text{白}$**：取出 1 白，剩 3 紅 1 白（4 球），不改變。$E[X|Y=\text{白}] = 3/4$

$$E[X] = E[X|Y=\text{紅}] \cdot P(Y=\text{紅}) + E[X|Y=\text{白}] \cdot P(Y=\text{白})$$

$$= \frac{1}{2} \times \frac{3}{5} + \frac{3}{4} \times \frac{2}{5} = \frac{3}{10} + \frac{6}{20} = \frac{3}{10} + \frac{3}{10} = \frac{6}{10} = \frac{3}{5}$$

### 範例 2：用 LOTUS 和 Gamma 函數

**題目**：$X \sim \text{Exp}(2)$，求 $E[X^3]$。

**解**：用 LOTUS：

$$E[X^3] = \int_0^\infty x^3 \cdot 2e^{-2x}\,dx$$

令 $u = 2x$，$du = 2dx$，$x = u/2$：

$$= \int_0^\infty \frac{u^3}{8} \cdot e^{-u} \cdot \frac{du}{2} \cdot 2 = \frac{1}{8}\int_0^\infty u^3 e^{-u}\,du = \frac{\Gamma(4)}{8} = \frac{3!}{8} = \frac{6}{8} = \frac{3}{4}$$

**或者用 MGF**：

$M(t) = \frac{2}{2-t}$

$M'''(t) = \frac{2 \cdot 3!}{(2-t)^4} = \frac{12}{(2-t)^4}$

$E[X^3] = M'''(0) = \frac{12}{16} = \frac{3}{4}$ ✓

### 範例 3：Chebyshev 不等式的應用

**題目**：一家保險公司有 10000 位保戶，每位保戶年理賠額 $X_i$ 獨立，$E[X_i] = 500$ 元，$\text{SD}(X_i) = 800$ 元。公司收的總保費為 520 萬元。用 Chebyshev 估計 $P(\text{理賠總額} > \text{總保費})$。

**解**：

$S = \sum_{i=1}^{10000} X_i$

$E[S] = 10000 \times 500 = 5{,}000{,}000$（500 萬）

$\text{Var}(S) = 10000 \times 800^2 = 6{,}400{,}000{,}000$

$\text{SD}(S) = \sqrt{6.4 \times 10^9} = 80{,}000$

$P(S > 5{,}200{,}000) = P(S - 5{,}000{,}000 > 200{,}000)$

$\le P(|S - 5{,}000{,}000| > 200{,}000) \le \frac{6{,}400{,}000{,}000}{(200{,}000)^2} = \frac{6.4 \times 10^9}{4 \times 10^{10}} = 0.16$

所以虧損的機率 $\le 16\%$。

（如果用 Normal 近似：$Z = \frac{200000}{80000} = 2.5$，$P(Z > 2.5) = 0.0062$，只有 0.62%。Chebyshev 確實比較鬆。）

### 範例 4：Eve's Law 的進階應用

**題目**：$N \sim \text{Poisson}(\lambda)$，給定 $N = n$，$X_1, \ldots, X_n$ i.i.d. $\sim \text{Exp}(\mu)$。令 $S = \sum_{i=1}^N X_i$（若 $N=0$ 則 $S=0$）。求 $E[S]$ 和 $\text{Var}(S)$。

**解**：

**$E[S]$**（全期望值法則）：

$$E[S|N=n] = n \cdot E[X_1] = \frac{n}{\mu}$$

$$E[S|N] = \frac{N}{\mu}$$

$$E[S] = E\left[\frac{N}{\mu}\right] = \frac{\lambda}{\mu}$$

**$\text{Var}(S)$**（Eve's Law）：

$$\text{Var}(S|N=n) = n \cdot \text{Var}(X_1) = \frac{n}{\mu^2}$$

$$E[\text{Var}(S|N)] = E\left[\frac{N}{\mu^2}\right] = \frac{\lambda}{\mu^2}$$

$$\text{Var}(E[S|N]) = \text{Var}\left(\frac{N}{\mu}\right) = \frac{1}{\mu^2}\text{Var}(N) = \frac{\lambda}{\mu^2}$$

$$\text{Var}(S) = \frac{\lambda}{\mu^2} + \frac{\lambda}{\mu^2} = \frac{2\lambda}{\mu^2}$$

> 這是「隨機求和」（compound Poisson process）的經典結果。保險數學中非常常用！

### 範例 5：指標變數法求期望值和變異數

**題目**：$n$ 對夫妻隨機坐成一排（共 $2n$ 人）。令 $X$ = 坐在相鄰位置的夫妻對數。求 $E[X]$。

**解**：

令 $I_i = \mathbf{1}[\text{第 } i \text{ 對夫妻坐在相鄰位置}]$，$i = 1, \ldots, n$。

$$X = \sum_{i=1}^n I_i$$

$$E[I_i] = P(\text{第 } i \text{ 對夫妻坐相鄰})$$

共 $2n$ 個位子，$(2n)!$ 種排法。

第 $i$ 對夫妻坐相鄰：把他們綁在一起視為一個「超級人」，共 $2n-1$ 個位子的排列，且夫妻內部可以交換 → $(2n-1)! \times 2$ 種。

$$P(\text{第 } i \text{ 對相鄰}) = \frac{2 \times (2n-1)!}{(2n)!} = \frac{2}{2n} = \frac{1}{n}$$

$$E[X] = n \times \frac{1}{n} = 1$$

> 不管 $n$ 多大，平均恰好有 1 對夫妻相鄰！

---

## 十一、概念比較與常見混淆

### 期望值 vs. 中位數 vs. 眾數

| | 期望值（Mean） | 中位數（Median） | 眾數（Mode） |
|--|---------------|----------------|------------|
| 定義 | $E[X]$ | $P(X \le m) = 0.5$ | $f(x)$ 最大的 $x$ |
| 對稱分布 | 三者相等 | 三者相等 | 三者相等 |
| 右偏分布 | Mean > Median > Mode | | |
| 對極端值 | 敏感 | 穩健 | 穩健 |

### E[g(X)] vs. g(E[X])

一般而言 $E[g(X)] \neq g(E[X])$！除非 $g$ 是線性（仿射）函數。

**Jensen 不等式**：若 $g$ 是凸函數，則 $E[g(X)] \ge g(E[X])$。

例：$E[X^2] \ge (E[X])^2$（因為 $x^2$ 是凸函數），等價於 $\text{Var}(X) \ge 0$。

### Cov = 0 vs. 獨立

| | $\text{Cov}(X,Y) = 0$ | $X, Y$ 獨立 |
|--|----------------------|------------|
| 含義 | 沒有線性關係 | 沒有任何關係 |
| 獨立 → ? | ✓ 一定不相關 | — |
| 不相關 → ? | — | ✗ 不一定獨立 |
| 例外 | $X \sim N(0,1)$, $Y=X^2$ | |
| Normal 情形 | ✓ 若聯合 Normal 且不相關 → 獨立 | |

### MGF vs. PGF vs. CF

| | MGF $M(t)$ | PGF $G(z)$ | CF $\varphi(t)$ |
|--|-----------|-----------|---------------|
| 定義 | $E[e^{tX}]$ | $E[z^X]$ | $E[e^{itX}]$ |
| 適用 | 大多數分布 | 非負整數值 | 所有分布 |
| 是否一定存在 | 不一定 | 離散型 | 一定 |
| 求動差 | $M^{(k)}(0)$ | 複雜 | $(-i)^k\varphi^{(k)}(0)$ |
| 唯一性 | ✓ | ✓ | ✓ |

---

## 十二、公式速查表

### 期望值公式

| 公式 | 條件 |
|------|------|
| $E[aX+b] = aE[X]+b$ | 無 |
| $E[X+Y] = E[X]+E[Y]$ | 無（不需獨立） |
| $E[XY] = E[X]E[Y]$ | 需要獨立 |
| $E[g(X)] = \int g(x)f(x)\,dx$ | LOTUS |
| $E[X] = E[E[X\|Y]]$ | 全期望值法則 |

### 變異數公式

| 公式 | 條件 |
|------|------|
| $\text{Var}(X) = E[X^2]-(E[X])^2$ | 無 |
| $\text{Var}(aX+b) = a^2\text{Var}(X)$ | 無 |
| $\text{Var}(X+Y) = \text{Var}(X)+\text{Var}(Y)+2\text{Cov}(X,Y)$ | 無 |
| $\text{Var}(X+Y) = \text{Var}(X)+\text{Var}(Y)$ | 需要獨立（或不相關） |
| $\text{Var}(X) = E[\text{Var}(X\|Y)]+\text{Var}(E[X\|Y])$ | Eve's Law |

### 不等式

| 不等式 | 條件 | 公式 |
|--------|------|------|
| Markov | $X \ge 0$ | $P(X \ge a) \le E[X]/a$ |
| Chebyshev | 有限變異數 | $P(\|X-\mu\| \ge k\sigma) \le 1/k^2$ |
| Jensen | $g$ 凸 | $E[g(X)] \ge g(E[X])$ |
| Cauchy-Schwarz | — | $(E[XY])^2 \le E[X^2]E[Y^2]$ |

---

*這三講（連續分布、聯合分布與變數轉換、期望值變異數與 MGF）涵蓋了機率論的核心計算工具。熟練掌握這些，博士班考試的計算題就有堅實的基礎了。*
