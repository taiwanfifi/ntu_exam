# 聯合分布與變數轉換

> 台大機率統計教學講義 — 從聯合分布到 Jacobian，多變數的世界

---

## 本章基礎觀念（零基礎必讀）

### 為什麼需要學聯合分布與變數轉換？

想像你同時丟兩顆骰子，你想知道「兩顆骰子點數的和」是多少。這時候你不能只看一顆骰子——你需要同時考慮兩顆骰子的結果。這就是**聯合分布**的核心想法：同時描述多個隨機變數的行為。

再進一步，如果你知道骰子的點數分布，想推出「點數的平方」或「兩顆骰子之和」的分布，這就是**變數轉換**——從已知分布推出新變數的分布。

這兩個工具在統計學和機器學習中無處不在。例如：投資組合需要考慮多支股票的聯合報酬率；醫學研究需要分析身高和體重的聯合關係。

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 聯合分布 | Joint Distribution | 同時描述兩個（或多個）隨機變數的分布 | 兩顆骰子同時丟，(X,Y) 的所有可能組合及其機率 |
| 聯合 PMF | Joint PMF | 離散情形下，(X,Y) 同時取特定值的機率 | P(骰子1=3, 骰子2=5) = 1/36 |
| 聯合 PDF | Joint PDF | 連續情形下，(X,Y) 的機率密度函數 | f(x,y) = 6(1-y)，在三角形區域上 |
| 邊際分布 | Marginal Distribution | 從聯合分布「積掉」另一個變數，得到單一變數的分布 | 知道 (X,Y) 的聯合分布後，只看 X 自己的分布 |
| 條件分布 | Conditional Distribution | 知道 Y=y 後，X 的分布如何變化 | 知道體重=70kg 後，身高的分布 |
| Jacobian 行列式 | Jacobian Determinant | 多變數變換時，用來修正「面積扭曲」的因子 | 直角座標轉極座標時的 r |
| 摺積 | Convolution | 求兩個獨立隨機變數之和的分布的方法 | X+Y 的 PDF = X 和 Y 的 PDF 做摺積 |
| 順序統計量 | Order Statistics | 把 n 個樣本從小到大排列後的第 k 個值 | 5 個考試成績排序後的中位數 |
| 支撐（區域） | Support | 隨機變數（或密度函數）不為零的範圍 | Uniform(0,1) 的支撐是 [0,1] |

### 前置知識

你需要先讀完以下章節：
- **prob_01 ~ prob_03**：知道什麼是隨機變數、PMF、PDF、CDF
- **prob_04**：熟悉常見分布（Uniform、Exponential、Normal 等）

關鍵公式複習：
- CDF 和 PDF 的關係：$F(x) = \int_{-\infty}^x f(t)\,dt$，$f(x) = F'(x)$
- Uniform(a,b) 的 PDF：$f(x) = \frac{1}{b-a}$，$a \le x \le b$
- Normal 的 PDF：$f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/(2\sigma^2)}$

---

## 一、聯合分布的基本概念

### 1.1 為什麼需要聯合分布？

前面我們討論的都是「一個」隨機變數。但現實中很多問題涉及**多個隨機變數之間的關係**。例如：

- 身高 $X$ 和體重 $Y$ 的關係
- 投資組合中兩支股票報酬率 $(R_1, R_2)$ 的關聯
- 一個人的學習時間 $X$ 和考試成績 $Y$

這時候我們需要「聯合分布」來描述多個隨機變數**同時**的行為。

### 1.2 聯合 PMF（離散情形）

**定義**：若 $(X, Y)$ 是離散隨機向量，其聯合 PMF 為

$$p_{X,Y}(x, y) = P(X = x, Y = y)$$

> **數值範例：兩顆骰子同時丟**
>
> 設 $X$ = 第一顆骰子點數，$Y$ = 第二顆骰子點數，兩顆獨立公平骰子。
>
> 聯合 PMF：$p_{X,Y}(x,y) = \frac{1}{36}$，對所有 $x \in \{1,...,6\}$，$y \in \{1,...,6\}$
>
> 例如：$P(X=2, Y=5) = \frac{1}{36}$
>
> 驗證總和：共 $6 \times 6 = 36$ 個組合，每個機率 $\frac{1}{36}$，總和 $= 36 \times \frac{1}{36} = 1$ ✓
>
> 如果我們想知道 $P(X+Y=7)$，需要把所有使 $x+y=7$ 的組合加起來：
> $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$，共 6 個，所以 $P(X+Y=7) = \frac{6}{36} = \frac{1}{6}$

**性質**：

1. $p_{X,Y}(x, y) \ge 0$
2. $\sum_x \sum_y p_{X,Y}(x, y) = 1$

### 1.3 聯合 PDF（連續情形）

**定義**：若 $(X, Y)$ 是連續隨機向量，其聯合 PDF $f_{X,Y}(x, y)$ 滿足

$$P((X,Y) \in A) = \iint_A f_{X,Y}(x, y)\,dx\,dy$$

**性質**：

1. $f_{X,Y}(x, y) \ge 0$
2. $\int_{-\infty}^{\infty}\int_{-\infty}^{\infty} f_{X,Y}(x, y)\,dx\,dy = 1$
3. $f_{X,Y}(x, y)$ 是密度，不是機率，可以大於 1

> **數值範例：三角形區域上的聯合 PDF**
>
> 設 $f_{X,Y}(x,y) = 2$，在三角形區域 $0 \le x \le 1,\; 0 \le y \le x$ 上；其他地方為 0。
>
> **驗證是合法的 PDF**：
> $$\int_0^1 \int_0^x 2\,dy\,dx = \int_0^1 2x\,dx = \left[x^2\right]_0^1 = 1 \quad \checkmark$$
>
> **求 $P(X \le 0.5)$**：
> $$P(X \le 0.5) = \int_0^{0.5}\int_0^x 2\,dy\,dx = \int_0^{0.5} 2x\,dx = \left[x^2\right]_0^{0.5} = 0.25$$

### 1.4 聯合 CDF

$$F_{X,Y}(x, y) = P(X \le x, Y \le y) = \int_{-\infty}^{x}\int_{-\infty}^{y} f_{X,Y}(s, t)\,dt\,ds$$

$$f_{X,Y}(x, y) = \frac{\partial^2 F_{X,Y}(x,y)}{\partial x \,\partial y}$$

---

## 二、邊際分布（Marginal Distribution）

### 2.1 概念

如果我們知道 $(X, Y)$ 的聯合分布，但只想知道 $X$ 自己的分布，就要把 $Y$ 的影響「積掉」（或「加掉」）。

### 2.2 連續型：積分消去

$$f_X(x) = \int_{-\infty}^{\infty} f_{X,Y}(x, y)\,dy$$

$$f_Y(y) = \int_{-\infty}^{\infty} f_{X,Y}(x, y)\,dx$$

> **直覺**：把聯合密度在 $y$ 方向「壓扁」，就得到 $X$ 的邊際密度。

### 2.3 離散型：求和消去

$$p_X(x) = \sum_y p_{X,Y}(x, y)$$

### 2.4 範例

**例題**：設 $(X, Y)$ 的聯合 PDF 為

$$f_{X,Y}(x, y) = \begin{cases} 6(1-y), & 0 \le x \le y \le 1 \\ 0, & \text{otherwise} \end{cases}$$

求邊際 PDF $f_X(x)$ 和 $f_Y(y)$。

**解**：

先畫出支撐區域：$0 \le x \le y \le 1$，這是 $x$-$y$ 平面上的一個三角形（$y = x$ 到 $y = 1$，$x$ 從 0 到 1）。

**求 $f_X(x)$**：固定 $x$，$y$ 的範圍是 $x \le y \le 1$。

$$f_X(x) = \int_x^1 6(1-y)\,dy = 6\left[y - \frac{y^2}{2}\right]_x^1 = 6\left[\left(1-\frac{1}{2}\right) - \left(x - \frac{x^2}{2}\right)\right]$$

$$= 6\left[\frac{1}{2} - x + \frac{x^2}{2}\right] = 6 \cdot \frac{(1-x)^2}{2} = 3(1-x)^2, \quad 0 \le x \le 1$$

**驗證**：$\int_0^1 3(1-x)^2\,dx = 3 \cdot \frac{(1-x)^3}{-3}\Big|_0^1 = -(0-1) = 1$ ✓

**求 $f_Y(y)$**：固定 $y$，$x$ 的範圍是 $0 \le x \le y$。

$$f_Y(y) = \int_0^y 6(1-y)\,dx = 6(1-y) \cdot y = 6y(1-y), \quad 0 \le y \le 1$$

這是 Beta(2, 2) 分布！

**驗證**：$\int_0^1 6y(1-y)\,dy = 6\left[\frac{y^2}{2} - \frac{y^3}{3}\right]_0^1 = 6\left(\frac{1}{2} - \frac{1}{3}\right) = 6 \cdot \frac{1}{6} = 1$ ✓

> **數值範例：用具體數字體會「積掉」的過程**
>
> 繼續上面的例子，$f_{X,Y}(x,y) = 6(1-y)$，$0 \le x \le y \le 1$。
>
> **求 $f_X(0.3)$**（固定 $x = 0.3$，把 $y$ 積掉）：
>
> $y$ 的範圍：$0.3 \le y \le 1$
>
> $$f_X(0.3) = \int_{0.3}^{1} 6(1-y)\,dy = 6\left[y - \frac{y^2}{2}\right]_{0.3}^{1}$$
> $$= 6\left[\left(1 - 0.5\right) - \left(0.3 - 0.045\right)\right] = 6\left[0.5 - 0.255\right] = 6 \times 0.245 = 1.47$$
>
> 用公式驗證：$f_X(x) = 3(1-x)^2$，$f_X(0.3) = 3(0.7)^2 = 3 \times 0.49 = 1.47$ ✓
>
> **求 $f_Y(0.6)$**（固定 $y = 0.6$，把 $x$ 積掉）：
>
> $x$ 的範圍：$0 \le x \le 0.6$
>
> $$f_Y(0.6) = \int_0^{0.6} 6(1-0.6)\,dx = 6 \times 0.4 \times 0.6 = 1.44$$
>
> 用公式驗證：$f_Y(y) = 6y(1-y)$，$f_Y(0.6) = 6 \times 0.6 \times 0.4 = 1.44$ ✓
>
> **重點**：注意 $f_X(0.3) = 1.47 > 1$，這是合法的！PDF 的值可以大於 1，因為它是密度，不是機率。

---

## 三、條件分布

### 3.1 定義

**連續型**：

$$f_{X|Y}(x|y) = \frac{f_{X,Y}(x,y)}{f_Y(y)}, \quad \text{當 } f_Y(y) > 0$$

**離散型**：

$$p_{X|Y}(x|y) = \frac{p_{X,Y}(x,y)}{p_Y(y)}, \quad \text{當 } p_Y(y) > 0$$

> **直覺**：知道 $Y = y$ 之後，$X$ 的分布「更新」了。就像 Bayes 定理的函數版。

### 3.2 範例（續前題）

**例題**：用上一節的聯合 PDF，求 $f_{X|Y}(x|y)$。

**解**：

$$f_{X|Y}(x|y) = \frac{f_{X,Y}(x,y)}{f_Y(y)} = \frac{6(1-y)}{6y(1-y)} = \frac{1}{y}, \quad 0 \le x \le y$$

這是 $\text{Uniform}(0, y)$！知道 $Y = y$ 之後，$X$ 在 $[0, y]$ 上均勻分布。

---

## 四、獨立性判斷

### 4.1 定義

$X$ 和 $Y$ **獨立** $\iff$ $f_{X,Y}(x, y) = f_X(x) \cdot f_Y(y)$ 對所有 $(x, y)$ 成立。

### 4.2 實用判斷技巧

**技巧 1：可分離性**。如果 $f_{X,Y}(x, y) = g(x) \cdot h(y)$（可以拆成一個只跟 $x$ 有關的函數乘以一個只跟 $y$ 有關的函數），**且支撐區域是矩形**，那就獨立。

**技巧 2：支撐區域**。如果支撐區域不是矩形（例如上面的三角形 $0 \le x \le y \le 1$），那一定**不獨立**。因為 $x$ 的範圍依賴 $y$ 的值。

### 4.3 範例

**例題**：判斷以下聯合 PDF 的 $X$ 和 $Y$ 是否獨立。

(a) $f(x,y) = 2e^{-x}e^{-2y}$，$x > 0, y > 0$

(b) $f(x,y) = 24xy$，$0 < x < 1, 0 < y < 1, x+y < 1$

**解**：

(a) $f(x,y) = (2e^{-2y}) \cdot (e^{-x})$ = $h(y) \cdot g(x)$。支撐區域 $\{x>0, y>0\}$ 是矩形（第一象限）。
但要驗證常數是否正確：$f_X(x) = e^{-x}$（Exp(1)），$f_Y(y) = 2e^{-2y}$（Exp(2)）。
$f_X(x) \cdot f_Y(y) = 2e^{-x}e^{-2y} = f(x,y)$。**獨立** ✓

(b) 支撐區域 $\{0<x<1, 0<y<1, x+y<1\}$ 是一個三角形，**不是矩形**。
所以 $X$ 和 $Y$ **不獨立**。

具體驗證：$f_X(x) = \int_0^{1-x} 24xy\,dy = 24x \cdot \frac{(1-x)^2}{2} = 12x(1-x)^2$

$f_Y(y) = \int_0^{1-y} 24xy\,dx = 12y(1-y)^2$

$f_X(x) \cdot f_Y(y) = 144xy(1-x)^2(1-y)^2 \neq 24xy = f(x,y)$。確認不獨立。

---

## 五、變數變換三大方法

這是機率課中最核心的技巧之一。已知 $X$ 的分布，求 $Y = g(X)$ 的分布。

### 5.1 方法一：CDF 法（最通用）

**核心思路**：先求 CDF，再微分得 PDF。

$$F_Y(y) = P(Y \le y) = P(g(X) \le y) = P(X \in \{x : g(x) \le y\})$$

**步驟**：

1. 寫出 $P(Y \le y) = P(g(X) \le y)$
2. 將不等式 $g(X) \le y$ 化簡成 $X$ 的不等式（注意方向！）
3. 用 $X$ 的 CDF 或 PDF 積分求出 $F_Y(y)$
4. 微分 $f_Y(y) = F_Y'(y)$
5. 檢查 $y$ 的範圍

> **優點**：萬用，不管 $g$ 是不是單調、是不是一對一都能用。
> **缺點**：有時候要分段討論。

#### 範例 0：CDF 法入門 — Y = X²，X~Uniform(0,1)

> **數值範例：從最簡單的例子開始**
>
> **題目**：$X \sim \text{Uniform}(0,1)$，求 $Y = X^2$ 的 PDF。
>
> **Step 1**：確定 $Y$ 的範圍。$X \in [0,1]$，所以 $Y = X^2 \in [0,1]$。
>
> **Step 2**：求 CDF。對 $0 \le y \le 1$：
>
> $$F_Y(y) = P(Y \le y) = P(X^2 \le y) = P(X \le \sqrt{y})$$
>
> 因為 $X \ge 0$，所以 $X^2 \le y \iff X \le \sqrt{y}$（不用考慮負的）。
>
> $$F_Y(y) = P(X \le \sqrt{y}) = \sqrt{y} \quad \text{（因為 } X \sim \text{Uniform}(0,1) \text{，CDF 就是 } x \text{）}$$
>
> **Step 3**：微分得 PDF。
>
> $$f_Y(y) = F_Y'(y) = \frac{d}{dy}\sqrt{y} = \frac{1}{2\sqrt{y}}, \quad 0 < y \le 1$$
>
> **Step 4**：驗證。
>
> $$\int_0^1 \frac{1}{2\sqrt{y}}\,dy = \left[\sqrt{y}\right]_0^1 = 1 \quad \checkmark$$
>
> **用具體數字檢查**：$P(Y \le 0.25) = P(X^2 \le 0.25) = P(X \le 0.5) = 0.5$。
> 用 CDF 公式：$F_Y(0.25) = \sqrt{0.25} = 0.5$ ✓
>
> **觀察**：$f_Y(y) = \frac{1}{2\sqrt{y}}$ 在 $y$ 接近 0 時趨於無窮大！這是因為 $X$ 在接近 0 的地方，平方後「壓縮」了，密度變高。

#### 範例 1：求 Y = X² 的 PDF（CDF 法）

**題目**：$X \sim N(0, 1)$，求 $Y = X^2$ 的 PDF。

**解**：

**Step 1**：$Y = X^2 \ge 0$，所以 $y < 0$ 時 $F_Y(y) = 0$。

**Step 2**：對 $y > 0$：

$$F_Y(y) = P(X^2 \le y) = P(-\sqrt{y} \le X \le \sqrt{y})$$

$$= \Phi(\sqrt{y}) - \Phi(-\sqrt{y}) = 2\Phi(\sqrt{y}) - 1$$

**Step 3**：微分（用鏈式法則）：

$$f_Y(y) = F_Y'(y) = 2\phi(\sqrt{y}) \cdot \frac{1}{2\sqrt{y}}$$

其中 $\phi(z) = \frac{1}{\sqrt{2\pi}}e^{-z^2/2}$。

$$f_Y(y) = \frac{1}{\sqrt{y}} \cdot \frac{1}{\sqrt{2\pi}} e^{-y/2} = \frac{1}{\sqrt{2\pi}} y^{-1/2} e^{-y/2}, \quad y > 0$$

這就是 $\chi^2(1)$ 分布！

> **為什麼用 CDF 法？** 因為 $g(x) = x^2$ 不是一對一函數（$x$ 和 $-x$ 都映射到同一個 $y$），所以不能直接用變數變換公式。CDF 法自動處理了這個問題。

### 5.2 方法二：變數變換公式法（單調函數）

**條件**：$g$ 在 $X$ 的支撐上是**嚴格單調**的（嚴格遞增或嚴格遞減），且 $g$ 可微。

**公式**：

$$f_Y(y) = f_X(g^{-1}(y)) \cdot \left|\frac{d}{dy}g^{-1}(y)\right|$$

也可以寫成（令 $x = g^{-1}(y)$）：

$$f_Y(y) = f_X(x) \cdot \left|\frac{dx}{dy}\right|$$

**推導**：

假設 $g$ 嚴格遞增（遞減的情形類似）：

$$F_Y(y) = P(g(X) \le y) = P(X \le g^{-1}(y)) = F_X(g^{-1}(y))$$

微分（鏈式法則）：

$$f_Y(y) = f_X(g^{-1}(y)) \cdot \frac{d}{dy}g^{-1}(y)$$

如果 $g$ 嚴格遞減，則 $P(g(X) \le y) = P(X \ge g^{-1}(y))$，微分後多一個負號。

取絕對值統一處理：

$$\boxed{f_Y(y) = f_X(g^{-1}(y)) \cdot \left|\frac{d}{dy}g^{-1}(y)\right|}$$

#### 範例 2：求 Y = e^X 的 PDF（變數變換法）

**題目**：$X \sim N(\mu, \sigma^2)$，求 $Y = e^X$ 的 PDF。

**解**：

**Step 1**：確認 $g(x) = e^x$ 嚴格遞增。✓

**Step 2**：求反函數 $x = g^{-1}(y) = \ln y$，$y > 0$。

**Step 3**：求導數 $\frac{dx}{dy} = \frac{1}{y}$。

**Step 4**：代入公式

$$f_Y(y) = f_X(\ln y) \cdot \left|\frac{1}{y}\right| = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(\ln y - \mu)^2}{2\sigma^2}\right) \cdot \frac{1}{y}$$

$$= \frac{1}{y\sigma\sqrt{2\pi}} \exp\left(-\frac{(\ln y - \mu)^2}{2\sigma^2}\right), \quad y > 0$$

這就是**對數常態分布（Log-Normal）**！$Y \sim \text{LogNormal}(\mu, \sigma^2)$。

**Step 5**：驗證 $y$ 的範圍：$X \in (-\infty, \infty)$，$Y = e^X \in (0, \infty)$。✓

### 5.3 方法三：多變數 Jacobian 法

> **什麼是 Jacobian？白話解釋**
>
> 當你把座標從 $(x,y)$ 變成 $(u,v)$ 時，空間會被「扭曲」。原本 $(x,y)$ 空間裡一個小正方形，到了 $(u,v)$ 空間可能變成平行四邊形，面積也變了。
>
> **Jacobian 行列式就是衡量這個面積變化的倍率**。
>
> 舉個最直覺的例子：直角座標 $(x,y)$ 轉極座標 $(r,\theta)$ 時，Jacobian = $r$。這就是為什麼極座標的面積元素是 $r\,dr\,d\theta$ 而不是 $dr\,d\theta$——因為離原點越遠，同樣的 $dr\,d\theta$ 對應的實際面積越大。
>
> **什麼是行列式？2x2 矩陣的行列式很簡單**：
>
> $$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$
>
> 幾何意義：以矩陣兩行（或兩列）為邊的平行四邊形面積（帶正負號）。

**情境**：有 $(X, Y)$ 的聯合 PDF，想求 $(U, V) = (g_1(X,Y), g_2(X,Y))$ 的聯合 PDF。

**公式**：

$$f_{U,V}(u, v) = f_{X,Y}(x(u,v),\; y(u,v)) \cdot |J|$$

其中 $J$ 是 **Jacobian 行列式**：

$$J = \det\begin{pmatrix} \frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ \frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} \end{pmatrix} = \frac{\partial x}{\partial u}\frac{\partial y}{\partial v} - \frac{\partial x}{\partial v}\frac{\partial y}{\partial u}$$

> **數值範例：簡單的線性變換**
>
> 設 $(X,Y)$ 的聯合 PDF 為 $f_{X,Y}(x,y) = 1$，在正方形 $0 \le x \le 1,\; 0 \le y \le 1$ 上。
>
> 令 $U = X + Y$，$V = X - Y$。求 $(U,V)$ 的聯合 PDF。
>
> **Step 1**：求反變換。
> 由 $U = X+Y$，$V = X-Y$，解出 $X = \frac{U+V}{2}$，$Y = \frac{U-V}{2}$。
>
> **Step 2**：計算 Jacobian。
> $$J = \det\begin{pmatrix} \frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ \frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} \end{pmatrix} = \det\begin{pmatrix} 1/2 & 1/2 \\ 1/2 & -1/2 \end{pmatrix} = \frac{1}{2} \times (-\frac{1}{2}) - \frac{1}{2} \times \frac{1}{2} = -\frac{1}{2}$$
>
> 所以 $|J| = \frac{1}{2}$。
>
> **Step 3**：代入公式。
> $$f_{U,V}(u,v) = f_{X,Y}\left(\frac{u+v}{2}, \frac{u-v}{2}\right) \cdot \frac{1}{2} = 1 \times \frac{1}{2} = \frac{1}{2}$$
>
> （在新的支撐區域上。原來的正方形 $0 \le x \le 1, 0 \le y \le 1$ 在新座標下變成菱形。）

> **注意**：這裡的 Jacobian 是**反變換**（從 $(u,v)$ 回到 $(x,y)$）的 Jacobian。

**推導**：

想像 $(u,v)$ 空間中一個小矩形 $du \times dv$。它在 $(x,y)$ 空間中對應的面積約為 $|J| \cdot du \cdot dv$。

機率不變原理：$f_{U,V}(u,v)\,du\,dv = f_{X,Y}(x,y)\,dx\,dy$

所以 $f_{U,V}(u,v) = f_{X,Y}(x,y) \cdot \left|\frac{\partial(x,y)}{\partial(u,v)}\right| = f_{X,Y}(x,y) \cdot |J|$。

#### 範例 3：極座標變換推導（經典！）

**題目**：$X, Y$ i.i.d. $\sim N(0,1)$。令 $R = \sqrt{X^2 + Y^2}$，$\Theta = \arctan(Y/X)$。求 $(R, \Theta)$ 的聯合 PDF。

**解**：

**Step 1**：聯合 PDF

$$f_{X,Y}(x,y) = \frac{1}{2\pi}e^{-(x^2+y^2)/2}$$

**Step 2**：反變換 $x = r\cos\theta$，$y = r\sin\theta$

**Step 3**：計算 Jacobian

$$J = \det\begin{pmatrix} \frac{\partial x}{\partial r} & \frac{\partial x}{\partial \theta} \\ \frac{\partial y}{\partial r} & \frac{\partial y}{\partial \theta} \end{pmatrix} = \det\begin{pmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{pmatrix}$$

$$= r\cos^2\theta + r\sin^2\theta = r$$

所以 $|J| = r$（$r > 0$）。

**Step 4**：代入

$$f_{R,\Theta}(r, \theta) = \frac{1}{2\pi}e^{-r^2/2} \cdot r = \frac{r}{2\pi} e^{-r^2/2}, \quad r > 0,\; 0 \le \theta < 2\pi$$

**Step 5**：觀察！這可以分解為

$$f_{R,\Theta}(r, \theta) = \underbrace{r e^{-r^2/2}}_{f_R(r)} \cdot \underbrace{\frac{1}{2\pi}}_{f_\Theta(\theta)}$$

所以 $R$ 和 $\Theta$ **獨立**！

- $\Theta \sim \text{Uniform}(0, 2\pi)$
- $R$ 的 PDF 是 $f_R(r) = r e^{-r^2/2}$（$r > 0$），這是 **Rayleigh 分布**

> 這個結果非常優美：二維標準常態分布在極座標下，角度和半徑是獨立的。

### 5.4 三種方法的比較

| 特性 | CDF 法 | 變數變換公式法 | Jacobian 法 |
|------|--------|--------------|-------------|
| 適用情形 | 任何 $g$ | 嚴格單調函數 | 多變數變換 |
| 步驟 | 寫 CDF → 微分 | 直接套公式 | 計算 Jacobian |
| 優點 | 最通用 | 最快（單調時） | 處理多變數 |
| 缺點 | 可能要分段 | 不能處理非單調 | 要引入輔助變數 |
| 典型應用 | $Y = X^2$ | $Y = e^X$ | 極座標變換 |

**選擇建議**：

- 單變數、單調函數 → 變數變換公式（最快）
- 單變數、非單調函數 → CDF 法
- 多變數 → Jacobian 法
- 不確定 → CDF 法（萬用）

---

## 六、摺積（Convolution）：Z = X + Y 的分布

### 6.1 推導

設 $X$ 和 $Y$ 獨立，聯合 PDF 為 $f_{X,Y}(x,y) = f_X(x) f_Y(y)$。

要求 $Z = X + Y$ 的 PDF。

**方法**：令 $Z = X + Y$，$W = Y$（輔助變數）。

反變換：$X = Z - W$，$Y = W$。

Jacobian：
$$J = \det\begin{pmatrix} \frac{\partial x}{\partial z} & \frac{\partial x}{\partial w} \\ \frac{\partial y}{\partial z} & \frac{\partial y}{\partial w} \end{pmatrix} = \det\begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix} = 1$$

$$f_{Z,W}(z, w) = f_X(z - w) f_Y(w) \cdot 1$$

邊際化（積掉 $W$）：

$$\boxed{f_Z(z) = \int_{-\infty}^{\infty} f_X(z - w) f_Y(w)\,dw = (f_X * f_Y)(z)}$$

這就是**摺積公式（convolution formula）**。

等價地：

$$f_Z(z) = \int_{-\infty}^{\infty} f_X(x) f_Y(z - x)\,dx$$

### 6.2 直覺

摺積的意思是：$Z = z$ 的方式有無限多種（$X = x$，$Y = z - x$，對所有可能的 $x$）。把所有這些方式的「機率密度」加起來，就是 $f_Z(z)$。

### 6.3 範例：兩個獨立 Uniform 之和

**題目**：$X, Y$ i.i.d. $\sim \text{Uniform}(0, 1)$，求 $Z = X + Y$ 的 PDF。

**解**：

$$f_Z(z) = \int_{-\infty}^{\infty} f_X(z-y) f_Y(y)\,dy = \int_{-\infty}^{\infty} f_X(z-y) \cdot \mathbf{1}_{0 \le y \le 1}\,dy$$

$f_X(z-y) = 1$ 當 $0 \le z-y \le 1$，即 $z-1 \le y \le z$。

所以要同時滿足 $0 \le y \le 1$ 和 $z-1 \le y \le z$。

**分段討論**：

**情形一**：$0 \le z \le 1$

$y$ 的範圍：$\max(0, z-1) = 0$ 到 $\min(1, z) = z$

$$f_Z(z) = \int_0^z 1\,dy = z$$

**情形二**：$1 < z \le 2$

$y$ 的範圍：$\max(0, z-1) = z-1$ 到 $\min(1, z) = 1$

$$f_Z(z) = \int_{z-1}^1 1\,dy = 1 - (z-1) = 2 - z$$

**結果**：

$$f_Z(z) = \begin{cases} z, & 0 \le z \le 1 \\ 2-z, & 1 < z \le 2 \\ 0, & \text{otherwise} \end{cases}$$

這是一個三角形分布！峰值在 $z = 1$。

**驗證**：$\int_0^1 z\,dz + \int_1^2 (2-z)\,dz = 1/2 + 1/2 = 1$ ✓

### 6.4 摺積的 MGF 捷徑

如果你只是想知道 $Z = X + Y$ 服從什麼分布（而不需要 PDF 的具體形式），用 MGF 往往更快：

$$M_Z(t) = M_X(t) \cdot M_Y(t) \quad (\text{當 } X, Y \text{ 獨立})$$

辨認 $M_Z(t)$ 屬於哪個分布即可。

---

## 七、Order Statistics（順序統計量）

### 7.1 定義

設 $X_1, X_2, \ldots, X_n$ i.i.d.，令

$$X_{(1)} \le X_{(2)} \le \cdots \le X_{(n)}$$

為排序後的值。$X_{(k)}$ 稱為第 $k$ 個順序統計量。

- $X_{(1)} = \min(X_1, \ldots, X_n)$
- $X_{(n)} = \max(X_1, \ldots, X_n)$

### 7.2 $X_{(k)}$ 的 PDF 推導

**定理**：若 $X_i$ i.i.d. 有 PDF $f$ 和 CDF $F$，則

$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1} [1-F(x)]^{n-k} f(x)$$

**推導思路**：

$X_{(k)}$ 在 $x$ 附近意味著：
- 有 $k-1$ 個觀測值 $< x$（機率各為 $F(x)$）
- 有 1 個觀測值 $\approx x$（密度 $f(x)\,dx$）
- 有 $n-k$ 個觀測值 $> x$（機率各為 $1-F(x)$）

選法有 $\frac{n!}{(k-1)! \cdot 1! \cdot (n-k)!}$ 種（多項式係數）。

因此：

$$P(x < X_{(k)} < x + dx) \approx \frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1} f(x)\,dx \,[1-F(x)]^{n-k}$$

### 7.3 特殊情形

**最小值** $X_{(1)}$（$k=1$）：

$$f_{X_{(1)}}(x) = n[1-F(x)]^{n-1} f(x)$$

$$P(X_{(1)} > x) = [1-F(x)]^n = [P(X_1 > x)]^n$$

> **直覺**：最小值 $> x$ $\iff$ 全部都 $> x$。

**最大值** $X_{(n)}$（$k=n$）：

$$f_{X_{(n)}}(x) = n[F(x)]^{n-1} f(x)$$

$$P(X_{(n)} \le x) = [F(x)]^n$$

> **直覺**：最大值 $\le x$ $\iff$ 全部都 $\le x$。

### 7.4 範例

**例題**：$X_1, X_2, X_3$ i.i.d. $\sim \text{Uniform}(0, 1)$。求中位數 $X_{(2)}$ 的 PDF 和期望值。

**解**：$n = 3$，$k = 2$，$F(x) = x$，$f(x) = 1$（$0 \le x \le 1$）。

$$f_{X_{(2)}}(x) = \frac{3!}{1! \cdot 1!} x^1 (1-x)^1 \cdot 1 = 6x(1-x), \quad 0 \le x \le 1$$

這是 $\text{Beta}(2, 2)$！

$$E[X_{(2)}] = \int_0^1 x \cdot 6x(1-x)\,dx = 6\int_0^1 (x^2 - x^3)\,dx = 6\left[\frac{1}{3} - \frac{1}{4}\right] = 6 \cdot \frac{1}{12} = \frac{1}{2}$$

> 一般規律：$U_{(1)}, \ldots, U_{(n)}$ 來自 $\text{Uniform}(0,1)$ 時，$U_{(k)} \sim \text{Beta}(k, n-k+1)$，$E[U_{(k)}] = \frac{k}{n+1}$。

---

## 八、更多完整範例

### 範例 4：Jacobian 法 — Box-Muller 變換

**題目**：$U_1, U_2$ i.i.d. $\sim \text{Uniform}(0, 1)$。令

$$Z_1 = \sqrt{-2\ln U_1}\cos(2\pi U_2), \quad Z_2 = \sqrt{-2\ln U_1}\sin(2\pi U_2)$$

證明 $Z_1, Z_2$ i.i.d. $\sim N(0, 1)$。

**解**：

反過來比較容易。設 $Z_1, Z_2$ i.i.d. $N(0,1)$，轉極座標 $R, \Theta$。

我們在範例 3 已經推導了：$R$ 和 $\Theta$ 獨立，$\Theta \sim \text{Uniform}(0, 2\pi)$，$R$ 的 PDF 是 $re^{-r^2/2}$。

令 $U_1 = e^{-R^2/2}$，$U_2 = \Theta/(2\pi)$。

反過來 $R = \sqrt{-2\ln U_1}$，$\Theta = 2\pi U_2$。

$$J = \det\begin{pmatrix} \frac{\partial R}{\partial U_1} & \frac{\partial R}{\partial U_2} \\ \frac{\partial \Theta}{\partial U_1} & \frac{\partial \Theta}{\partial U_2} \end{pmatrix} = \det\begin{pmatrix} \frac{-1}{U_1\sqrt{-2\ln U_1}} & 0 \\ 0 & 2\pi \end{pmatrix} = \frac{-2\pi}{U_1 R}$$

$f_{U_1,U_2}(u_1,u_2) = f_{R,\Theta}(r,\theta) \cdot |J|^{-1}$

但更直接的方式：$U_1 = e^{-R^2/2}$ 是 $R^2/2$ 的遞減函數，$R^2/2 \sim \text{Exp}(1)$。

$P(U_1 \le u) = P(e^{-R^2/2} \le u) = P(R^2/2 \ge -\ln u) = e^{\ln u} = u$，所以 $U_1 \sim \text{Uniform}(0,1)$。

$U_2 = \Theta/(2\pi) \sim \text{Uniform}(0,1)$，且和 $U_1$ 獨立。

因此 Box-Muller 的逆變換成立：從 $U_1, U_2 \sim \text{Uniform}(0,1)$ 可以生成 $Z_1, Z_2 \sim N(0,1)$。

### 範例 5：CDF 法的分段討論

**題目**：$X \sim \text{Uniform}(-1, 2)$，求 $Y = |X|$ 的 PDF。

**解**：

$Y = |X| \ge 0$。$Y$ 的範圍：因為 $X \in [-1, 2]$，所以 $Y = |X| \in [0, 2]$。

**Step 1**：求 CDF

$$F_Y(y) = P(|X| \le y) = P(-y \le X \le y)$$

**分段**：

**當 $0 \le y < 1$**：$X \in [-y, y] \cap [-1, 2] = [-y, y]$
$$F_Y(y) = P(-y \le X \le y) = \frac{y - (-y)}{2 - (-1)} = \frac{2y}{3}$$

**當 $1 \le y \le 2$**：$X \in [-y, y] \cap [-1, 2] = [-1, y]$
$$F_Y(y) = P(-1 \le X \le y) = \frac{y - (-1)}{3} = \frac{y+1}{3}$$

**Step 2**：微分得 PDF

$$f_Y(y) = \begin{cases} \frac{2}{3}, & 0 \le y < 1 \\ \frac{1}{3}, & 1 \le y \le 2 \\ 0, & \text{otherwise} \end{cases}$$

**驗證**：$\int_0^1 \frac{2}{3}\,dy + \int_1^2 \frac{1}{3}\,dy = \frac{2}{3} + \frac{1}{3} = 1$ ✓

> **重點**：CDF 法在 $y = 1$ 處需要分段，因為 $|X| \le y$ 的解集形狀在 $y = 1$ 改變了（左邊界從 $-y$ 變成 $-1$）。

### 範例 6：最小值的分布

**題目**：$X_1, \ldots, X_5$ i.i.d. $\sim \text{Exp}(3)$。令 $M = \min(X_1, \ldots, X_5)$。
求 $M$ 的分布和 $E[M]$。

**解**：

$$P(M > t) = P(X_1 > t, \ldots, X_5 > t) = [P(X_1 > t)]^5 = (e^{-3t})^5 = e^{-15t}$$

所以 $M \sim \text{Exp}(15)$。

$$E[M] = \frac{1}{15}$$

> 一般規律：$n$ 個 i.i.d. $\text{Exp}(\lambda)$ 的最小值 $\sim \text{Exp}(n\lambda)$。

---

## 九、常見陷阱

### 陷阱 1：忘記 Jacobian 的絕對值

Jacobian 行列式可以是負數（例如反轉座標），但 PDF 必須非負，所以一定要取**絕對值**。

### 陷阱 2：CDF 法忘記分段

當 $g$ 不是單調函數時（如 $|X|$、$X^2$），CDF 法幾乎一定要分段討論。

分段的「斷點」通常出現在：
- $g(x)$ 改變單調性的地方
- 支撐的邊界

### 陷阱 3：忘記轉換支撐範圍

做變數變換後，$Y$ 的支撐不一定和 $X$ 一樣。例如：
- $X \in (-\infty, \infty)$，$Y = e^X \in (0, \infty)$
- $X \in (0, 1)$，$Y = -\ln X \in (0, \infty)$
- $X \in (-1, 2)$，$Y = X^2 \in (0, 4)$

### 陷阱 4：Jacobian 的方向

Jacobian 是**反變換**的 Jacobian。如果你定義了正變換 $(u, v) = (g_1(x,y), g_2(x,y))$，那麼 Jacobian 要用反變換 $(x, y) = (h_1(u,v), h_2(u,v))$ 來算。

或者你可以算正變換的 Jacobian 再取倒數：

$$\left|\frac{\partial(x,y)}{\partial(u,v)}\right| = \frac{1}{\left|\frac{\partial(u,v)}{\partial(x,y)}\right|}$$

### 陷阱 5：摺積的積分上下限

做摺積 $f_Z(z) = \int f_X(z-y)f_Y(y)\,dy$ 時，積分上下限要由兩個 PDF 的支撐**同時**決定。

例如 $X, Y \in [0, 1]$，則需要 $0 \le y \le 1$ 且 $0 \le z - y \le 1$（即 $z-1 \le y \le z$）。

兩個範圍的交集隨 $z$ 的值而變，所以通常需要分段。

### 陷阱 6：獨立性和支撐區域

即使 $f_{X,Y}(x,y)$ 在形式上可以寫成 $g(x)h(y)$，如果支撐區域不是矩形（例如 $x + y < 1$），$X$ 和 $Y$ 仍然**不獨立**。

### 陷阱 7：多變數 Jacobian 中輔助變數的選擇

做 Jacobian 法時，如果只有一個目標變數（如 $Z = X + Y$），需要引入一個輔助變數（如 $W = Y$）。輔助變數的選擇通常不影響最終結果，但選得好可以簡化計算。常見選擇：$W = X$ 或 $W = Y$。

---

## 十、概念比較

### 邊際 vs. 條件 vs. 聯合

| | 聯合 | 邊際 | 條件 |
|---|------|------|------|
| 符號 | $f_{X,Y}(x,y)$ | $f_X(x)$, $f_Y(y)$ | $f_{X|Y}(x|y)$ |
| 描述 | $X$ 和 $Y$ 同時的行為 | $X$（或 $Y$）單獨的行為 | 知道 $Y=y$ 後 $X$ 的行為 |
| 從聯合求 | — | 積掉另一個變數 | 除以邊際 |
| 關係 | $f_{X,Y} = f_{X|Y} \cdot f_Y$ | $f_X = \int f_{X,Y}\,dy$ | $f_{X|Y} = f_{X,Y}/f_Y$ |

### CDF 法 vs. 變數變換法 vs. MGF 法（求和的分布）

| 方法 | 步驟 | 得到什麼 | 限制 |
|------|------|---------|------|
| CDF 法 | 寫 CDF → 微分 | 完整 PDF | 無 |
| 變數變換 | 反函數 + Jacobian | 完整 PDF | 需單調 / 多變數 |
| 摺積 | $\int f_X(z-y)f_Y(y)\,dy$ | $Z=X+Y$ 的 PDF | 只限求和 |
| MGF | $M_Z = M_X \cdot M_Y$ | 辨認分布 | 要能辨認 MGF |

---

### 自我檢測

1. **基礎題**：設 $(X,Y)$ 的聯合 PDF 為 $f(x,y) = 4xy$，$0 < x < 1$，$0 < y < 1$。判斷 $X$ 和 $Y$ 是否獨立？求 $f_X(x)$。

2. **計算題**：$X \sim \text{Uniform}(0,2)$，用 CDF 法求 $Y = 3X + 1$ 的 PDF。

3. **Jacobian 題**：設 $X,Y$ 獨立，都服從 $\text{Exp}(1)$。令 $U = X + Y$，$V = X/(X+Y)$。求 $(U,V)$ 的聯合 PDF，並證明 $U$ 和 $V$ 獨立。

4. **邊際分布題**：設 $f(x,y) = e^{-y}$，$0 < x < y < \infty$。求 $f_X(x)$ 和 $f_Y(y)$。

<details><summary>參考答案</summary>

**1.** $f_X(x) = \int_0^1 4xy\,dy = 4x \cdot \frac{1}{2} = 2x$。$f_Y(y) = \int_0^1 4xy\,dx = 2y$。
$f_X(x) \cdot f_Y(y) = 4xy = f(x,y)$，且支撐區域 $(0,1) \times (0,1)$ 是矩形。所以 **$X$ 和 $Y$ 獨立**。

**2.** $F_Y(y) = P(3X+1 \le y) = P(X \le \frac{y-1}{3})$。
$X \sim \text{Uniform}(0,2)$，所以 $F_X(x) = x/2$。
$F_Y(y) = \frac{(y-1)/3}{2} = \frac{y-1}{6}$，$y \in [1, 7]$。
微分：$f_Y(y) = \frac{1}{6}$，$1 \le y \le 7$。所以 $Y \sim \text{Uniform}(1,7)$。

**3.** 反變換：$X = UV$，$Y = U(1-V)$。
Jacobian：$J = \det\begin{pmatrix} V & U \\ 1-V & -U \end{pmatrix} = -UV - U(1-V) = -U$，$|J| = U$。
$f_{U,V}(u,v) = e^{-uv} \cdot e^{-u(1-v)} \cdot u = u e^{-u}$，$u > 0$，$0 < v < 1$。
這可以拆成 $f_U(u) = u e^{-u}$（Gamma(2,1) 的 PDF）和 $f_V(v) = 1$（Uniform(0,1)）。所以 $U$ 和 $V$ 獨立。

**4.** $f_X(x) = \int_x^\infty e^{-y}\,dy = e^{-x}$，$x > 0$。
$f_Y(y) = \int_0^y e^{-y}\,dx = ye^{-y}$，$y > 0$。

</details>

---

*下一講：期望值、變異數與 MGF*
