# 第三章：離散分布大全

> 台大機率統計教學講義
> 本章目標：完整推導所有重要離散分布的 PMF、期望值、變異數、MGF，並建立分布之間的關係網路。

---

## 🔰 本章基礎觀念（零基礎必讀）

### 什麼是「分布」？（用生活化語言解釋）

「分布」就是告訴你一個隨機事件的「所有可能結果」以及「每個結果出現的機率」。

想像你丟一顆骰子，可能的結果是 1 到 6，每個結果的機率都是 1/6。把這個資訊整理成一張表，就是一個「分布」：

| 點數 | 1 | 2 | 3 | 4 | 5 | 6 |
|------|---|---|---|---|---|---|
| 機率 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |

「離散分布」是指結果可以一個一個列出來的（比如 0, 1, 2, 3, ...）。相對地，「連續分布」的結果是一段連續的範圍（比如身高可以是 170.1, 170.123... 任何數字），連續分布會在下一章介紹。

### 你需要知道的數學基礎

1. **PMF（機率質量函數，Probability Mass Function）**：就是「每個結果對應的機率」，寫成 $P(X = k)$。所有 PMF 加起來一定等於 1。

2. **期望值 $E[X]$（Expected Value）**：就是「平均值」的概念。把每個結果乘以它的機率，再全部加起來。
   - 例如：骰子的期望值 = $1 \times \frac{1}{6} + 2 \times \frac{1}{6} + \cdots + 6 \times \frac{1}{6} = 3.5$
   - 白話：如果你丟非常非常多次骰子，平均點數會趨近 3.5

3. **變異數 $\text{Var}(X)$（Variance）**：衡量「結果離平均值有多分散」。變異數越大，結果越不確定。
   - 公式：$\text{Var}(X) = E[X^2] - (E[X])^2$
   - 白話：把每個結果和平均值的差距取平方，再求平均

4. **$\sum$ 求和符號**：$\sum_{k=0}^{n} f(k)$ 就是把 $f(0) + f(1) + f(2) + \cdots + f(n)$ 加起來

5. **i.i.d.（Independent and Identically Distributed）**：「獨立且相同分布」。白話：每次實驗的條件完全一樣，而且每次的結果不會互相影響。例如連續丟 10 次硬幣，每次都是獨立的，而且每次正面機率都是 0.5。

6. **MGF（動差生成函數，Moment Generating Function）**：一個數學工具，可以用它來快速計算期望值和變異數。初學者可以先跳過 MGF 的推導，專注理解 PMF、期望值和變異數即可。

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 分布 | Distribution | 所有可能結果及其機率的完整描述 | 骰子的 1~6 各 1/6 |
| PMF | Probability Mass Function | 每個結果的機率值 | $P(X=3) = 1/6$ |
| 期望值 | Expected Value / Mean | 長期平均的結果 | 骰子的期望值 = 3.5 |
| 變異數 | Variance | 結果的分散程度 | 變異數大 = 結果很不確定 |
| 標準差 | Standard Deviation | 變異數開根號，和原始單位相同 | $\text{SD} = \sqrt{\text{Var}}$ |
| i.i.d. | Independent & Identically Distributed | 每次實驗獨立且條件相同 | 連續丟硬幣 |
| MGF | Moment Generating Function | 求期望值/變異數的數學工具 | 進階工具，初學可先跳過 |
| Support | 支撐 / 值域 | 隨機變數可能取到的值的範圍 | 骰子的支撐是 {1,2,3,4,5,6} |
| 動差 / Moment | Moment | $E[X^n]$ 叫做第 $n$ 階動差 | $E[X]$ 是第一階動差 |

---

## 0. 預備知識：期望值、變異數、動差生成函數

在進入各分布之前，先複習基本定義。

### 期望值 E[X]

$$E[X] = \sum_{x} x \cdot P(X = x)$$

**性質：**
- 線性：$E[aX + b] = aE[X] + b$
- 對任何函數 $g$：$E[g(X)] = \sum_x g(x) \cdot P(X = x)$（LOTUS 公式）

### 變異數 Var(X)

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

**性質：**
- $\text{Var}(aX + b) = a^2 \text{Var}(X)$
- $\text{Var}(X) \geq 0$，等號成立若且唯若 $X$ 是常數

### 動差生成函數 MGF：$M_X(t)$

$$M_X(t) = E[e^{tX}] = \sum_{x} e^{tx} \cdot P(X = x)$$

**為什麼要 MGF？**
1. 可以用微分求動差：$E[X^n] = M_X^{(n)}(0)$（在 $t = 0$ 處的第 $n$ 階導數）
2. MGF 唯一決定分布（如果 MGF 在 $t = 0$ 的鄰域存在）
3. 獨立隨機變數之和的 MGF = 各自 MGF 之積

---

## 1. Bernoulli 分布 $\text{Bernoulli}(p)$

### 1.1 定義與情境

最簡單的隨機變數。一次試驗，只有「成功」(1) 或「失敗」(0)。

> **🔰 白話定義**：丟一次硬幣——結果要嘛是正面（成功=1），要嘛是反面（失敗=0），就這樣！
>
> **什麼時候會用到？** 任何只有「是/否」兩種結果的單次實驗：
> - 丟一枚硬幣（正面/反面）
> - 一個產品是否為不良品（是/否）
> - 一次投籃是否命中（進/不進）
> - 一位顧客是否購買（買/不買）

$$X = \begin{cases} 1 & \text{with probability } p \\ 0 & \text{with probability } 1 - p \end{cases}$$

其中 $0 \leq p \leq 1$，令 $q = 1 - p$。

### 1.2 PMF

$$P(X = k) = p^k (1-p)^{1-k}, \quad k = 0, 1$$

**驗證加總為 1：** $P(X=0) + P(X=1) = (1-p) + p = 1$ ✓

### 1.3 E[X] 推導

$$E[X] = 0 \cdot P(X=0) + 1 \cdot P(X=1) = 0 \cdot q + 1 \cdot p = p$$

### 1.4 Var(X) 推導

先求 $E[X^2]$：
$$E[X^2] = 0^2 \cdot q + 1^2 \cdot p = p$$

$$\text{Var}(X) = E[X^2] - (E[X])^2 = p - p^2 = p(1-p) = pq$$

**有趣的觀察：** 變異數 $pq$ 在 $p = 1/2$ 時最大（= 1/4），在 $p = 0$ 或 $p = 1$（確定事件）時為 0。

### 1.5 MGF 推導

$$M_X(t) = E[e^{tX}] = e^{t \cdot 0} \cdot q + e^{t \cdot 1} \cdot p = q + pe^t$$

$$\boxed{M_X(t) = q + pe^t}$$

**驗證 E[X]：** $M_X'(t) = pe^t$，$M_X'(0) = p$ ✓

**驗證 E[X^2]：** $M_X''(t) = pe^t$，$M_X''(0) = p$ ✓，$\text{Var} = p - p^2 = pq$ ✓

### 1.6 範例

**問題：** 某工廠產品的不良率是 3%。隨機取一個產品，令 $X$ = 1 若為不良品，$X$ = 0 若為良品。

$$X \sim \text{Bernoulli}(0.03)$$
$$E[X] = 0.03, \quad \text{Var}(X) = 0.03 \times 0.97 = 0.0291$$

> **📝 數值範例（丟硬幣）**：丟一枚公平硬幣，正面 = 1、反面 = 0，$p = 0.5$。
>
> $P(X = 1) = 0.5$，$P(X = 0) = 0.5$
> $E[X] = p = 0.5$（平均而言，丟非常多次後，正面的比例趨近 0.5）
> $\text{Var}(X) = 0.5 \times 0.5 = 0.25$（不確定性最大的情況！）

---

## 2. 二項分布 $\text{Binomial}(n, p)$

### 2.1 定義與情境

$n$ 次獨立的 Bernoulli 試驗中，成功的總次數。

> **🔰 白話定義**：把 Bernoulli 做很多次（$n$ 次），然後數「成功了幾次」。
>
> **什麼時候會用到？**
> - 考試有 20 題選擇題，每題隨機猜答對的機率是 1/4，猜對幾題？→ Binomial(20, 0.25)
> - 投籃 10 次，每次命中率 60%，進了幾球？→ Binomial(10, 0.6)
> - 生產 100 個零件，每個不良率 3%，有幾個不良品？→ Binomial(100, 0.03)
>
> **和 Bernoulli 的關係**：Bernoulli 是「做 1 次」，Binomial 是「做 $n$ 次再數成功幾次」。$n$ 次 Bernoulli 加起來 = 1 個 Binomial。

如果 $X_1, X_2, \ldots, X_n$ 是 i.i.d. $\text{Bernoulli}(p)$，則：
$$X = X_1 + X_2 + \cdots + X_n \sim \text{Binomial}(n, p)$$

### 2.2 PMF 推導

$X = k$ 表示 $n$ 次中恰好 $k$ 次成功。

- 選哪 $k$ 次成功：$\binom{n}{k}$ 種方式
- 那 $k$ 次成功的機率：$p^k$
- 其餘 $n - k$ 次失敗的機率：$(1-p)^{n-k}$
- 因為各次獨立，所以每種排列的機率相乘

$$\boxed{P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n}$$

**驗證加總為 1：** 由二項式定理：
$$\sum_{k=0}^{n} \binom{n}{k} p^k (1-p)^{n-k} = [p + (1-p)]^n = 1^n = 1 \quad \checkmark$$

### 2.3 E[X] 推導

**方法 1：利用 Bernoulli 的線性性**

$$E[X] = E[X_1 + X_2 + \cdots + X_n] = \sum_{i=1}^{n} E[X_i] = np$$

這個方法最簡潔！

**方法 2：直接從定義計算（練習用）**

$$E[X] = \sum_{k=0}^{n} k \binom{n}{k} p^k q^{n-k}$$

$k = 0$ 那項是 0，所以從 $k = 1$ 開始：
$$= \sum_{k=1}^{n} k \cdot \frac{n!}{k!(n-k)!} p^k q^{n-k}$$
$$= \sum_{k=1}^{n} \frac{n!}{(k-1)!(n-k)!} p^k q^{n-k}$$
$$= np \sum_{k=1}^{n} \frac{(n-1)!}{(k-1)!(n-k)!} p^{k-1} q^{n-k}$$

令 $j = k - 1$，$m = n - 1$：
$$= np \sum_{j=0}^{m} \binom{m}{j} p^j q^{m-j} = np \cdot (p + q)^m = np \cdot 1 = np \quad \checkmark$$

### 2.4 Var(X) 推導

**方法 1：利用獨立性**

因為 $X_1, \ldots, X_n$ 獨立：
$$\text{Var}(X) = \sum_{i=1}^{n} \text{Var}(X_i) = n \cdot pq = npq$$

**方法 2：先求 $E[X(X-1)]$（常用技巧）**

$$E[X(X-1)] = \sum_{k=0}^{n} k(k-1) \binom{n}{k} p^k q^{n-k}$$

$k = 0, 1$ 的項都是 0，從 $k = 2$ 開始：
$$= \sum_{k=2}^{n} k(k-1) \frac{n!}{k!(n-k)!} p^k q^{n-k}$$
$$= \sum_{k=2}^{n} \frac{n!}{(k-2)!(n-k)!} p^k q^{n-k}$$
$$= n(n-1)p^2 \sum_{k=2}^{n} \frac{(n-2)!}{(k-2)!(n-k)!} p^{k-2} q^{n-k}$$

令 $j = k - 2$，$m = n - 2$：
$$= n(n-1)p^2 \sum_{j=0}^{m} \binom{m}{j} p^j q^{m-j} = n(n-1)p^2$$

因此：
$$E[X^2] = E[X(X-1)] + E[X] = n(n-1)p^2 + np$$
$$\text{Var}(X) = E[X^2] - (E[X])^2 = n(n-1)p^2 + np - n^2p^2$$
$$= n^2p^2 - np^2 + np - n^2p^2 = np - np^2 = np(1-p) = npq \quad \checkmark$$

### 2.5 MGF 推導

$$M_X(t) = E[e^{tX}] = \sum_{k=0}^{n} e^{tk} \binom{n}{k} p^k q^{n-k}$$
$$= \sum_{k=0}^{n} \binom{n}{k} (pe^t)^k q^{n-k} = (pe^t + q)^n$$

$$\boxed{M_X(t) = (pe^t + q)^n}$$

**另一種推導（利用獨立性）：**
$$M_X(t) = M_{X_1}(t) \cdot M_{X_2}(t) \cdots M_{X_n}(t) = (q + pe^t)^n \quad \checkmark$$

### 2.6 範例

**問題：** 投籃命中率 60%，投 10 球，恰好進 7 球的機率？

$$X \sim \text{Binomial}(10, 0.6)$$

$$P(X = 7) = \binom{10}{7} (0.6)^7 (0.4)^3 = 120 \times 0.0279936 \times 0.064 = 120 \times 0.001791590 \approx 0.2150$$

$$E[X] = 10 \times 0.6 = 6, \quad \text{Var}(X) = 10 \times 0.6 \times 0.4 = 2.4$$

> **📝 數值範例（考試猜題）**：選擇題考試有 5 題，每題 4 個選項隨機猜，$p = 1/4 = 0.25$，$X$ = 猜對的題數。
>
> $X \sim \text{Binomial}(5, 0.25)$
>
> 全部猜錯（$k=0$）：$P(X=0) = \binom{5}{0}(0.25)^0(0.75)^5 = 1 \times 1 \times 0.2373 = 0.2373$
> 猜對 1 題（$k=1$）：$P(X=1) = \binom{5}{1}(0.25)^1(0.75)^4 = 5 \times 0.25 \times 0.3164 = 0.3955$
> 猜對 2 題（$k=2$）：$P(X=2) = \binom{5}{2}(0.25)^2(0.75)^3 = 10 \times 0.0625 \times 0.4219 = 0.2637$
>
> 期望猜對題數：$E[X] = 5 \times 0.25 = 1.25$ 題
>
> **驗證 n 次 Bernoulli = Binomial**：每一題猜對/猜錯就是一次 Bernoulli(0.25)，5 題的「猜對總數」就是 Binomial(5, 0.25)。

---

## 3. 幾何分布 $\text{Geometric}(p)$

### 3.1 定義與情境

一直做獨立 Bernoulli 試驗，直到第一次成功。$X$ = 需要的試驗次數。

> **🔰 白話定義**：一直重複做某件事，直到第一次成功為止。$X$ 記錄「你做了幾次才成功」。
>
> **什麼時候會用到？**
> - 一直丟骰子，直到第一次出現 6 為止，丟了幾次？→ Geometric(1/6)
> - 打電話給客服，每次接通機率 30%，打了幾通才接通？→ Geometric(0.3)
> - 面試多家公司，每家錄取機率 10%，面試了幾家才拿到 offer？→ Geometric(0.1)

### 3.2 兩種定義的比較

| | 定義 1（試驗次數） | 定義 2（失敗次數） |
|---|---|---|
| $X$ 代表 | 第一次成功的試驗編號 | 第一次成功前的失敗次數 |
| 值域 | $\{1, 2, 3, \ldots\}$ | $\{0, 1, 2, \ldots\}$ |
| PMF | $P(X=k) = q^{k-1}p$ | $P(Y=k) = q^k p$ |
| $E[X]$ | $1/p$ | $q/p$ |
| $\text{Var}(X)$ | $q/p^2$ | $q/p^2$ |
| 關係 | $X = Y + 1$ | $Y = X - 1$ |

**本講義主要使用定義 1（試驗次數）。考試時請確認題目用哪個定義！**

### 3.3 PMF 推導（定義 1）

$X = k$ 表示：前 $k - 1$ 次失敗，第 $k$ 次成功。

$$\boxed{P(X = k) = (1-p)^{k-1} p = q^{k-1} p, \quad k = 1, 2, 3, \ldots}$$

**驗證加總為 1：**
$$\sum_{k=1}^{\infty} q^{k-1} p = p \sum_{k=0}^{\infty} q^k = p \cdot \frac{1}{1-q} = p \cdot \frac{1}{p} = 1 \quad \checkmark$$

（用了等比級數 $\sum_{k=0}^{\infty} r^k = \frac{1}{1-r}$，$|r| < 1$）

### 3.4 E[X] 推導

$$E[X] = \sum_{k=1}^{\infty} k \cdot q^{k-1} p = p \sum_{k=1}^{\infty} k q^{k-1}$$

利用公式 $\sum_{k=1}^{\infty} k r^{k-1} = \frac{1}{(1-r)^2}$（$|r| < 1$，這是 $\frac{d}{dr}\frac{1}{1-r}$ 的結果）：

$$E[X] = p \cdot \frac{1}{(1-q)^2} = p \cdot \frac{1}{p^2} = \frac{1}{p}$$

$$\boxed{E[X] = \frac{1}{p}}$$

**直觀：** 如果每次成功的機率是 $p = 0.1$，平均需要 $1/0.1 = 10$ 次才會第一次成功。合理！

### 3.5 Var(X) 推導

先求 $E[X(X-1)]$：
$$E[X(X-1)] = \sum_{k=1}^{\infty} k(k-1) q^{k-1} p = pq \sum_{k=2}^{\infty} k(k-1) q^{k-2}$$

利用 $\sum_{k=2}^{\infty} k(k-1) r^{k-2} = \frac{2}{(1-r)^3}$（$\frac{d^2}{dr^2}\frac{1}{1-r}$ 的結果）：

$$E[X(X-1)] = pq \cdot \frac{2}{(1-q)^3} = pq \cdot \frac{2}{p^3} = \frac{2q}{p^2}$$

$$E[X^2] = E[X(X-1)] + E[X] = \frac{2q}{p^2} + \frac{1}{p} = \frac{2q + p}{p^2} = \frac{q + 1}{p^2}$$

（因為 $2q + p = q + (q + p) = q + 1$）

$$\text{Var}(X) = E[X^2] - (E[X])^2 = \frac{q + 1}{p^2} - \frac{1}{p^2} = \frac{q}{p^2}$$

$$\boxed{\text{Var}(X) = \frac{q}{p^2} = \frac{1-p}{p^2}}$$

### 3.6 MGF 推導

$$M_X(t) = E[e^{tX}] = \sum_{k=1}^{\infty} e^{tk} q^{k-1} p = \frac{p}{q} \sum_{k=1}^{\infty} (qe^t)^k$$

$$= \frac{p}{q} \cdot \frac{qe^t}{1 - qe^t} = \frac{pe^t}{1 - qe^t}$$

（需要 $qe^t < 1$，即 $t < -\ln q = \ln(1/q)$）

$$\boxed{M_X(t) = \frac{pe^t}{1 - qe^t}, \quad t < \ln\frac{1}{q}}$$

### 3.7 無記憶性（Memoryless Property）

幾何分布是唯一具有無記憶性的離散分布：

$$P(X > m + n \mid X > m) = P(X > n), \quad \forall m, n \geq 0$$

**推導：**

先算 $P(X > k) = \sum_{j=k+1}^{\infty} q^{j-1} p = q^k$（前 $k$ 次都失敗的機率）。

$$P(X > m + n | X > m) = \frac{P(X > m + n \cap X > m)}{P(X > m)} = \frac{P(X > m + n)}{P(X > m)} = \frac{q^{m+n}}{q^m} = q^n = P(X > n) \quad \blacksquare$$

**口語：** 已經失敗了 $m$ 次，還需要再等多久和從頭開始一樣。之前的失敗不影響未來。

### 3.8 範例

**問題：** 投籃命中率 30%。求第一次進球所需投籃次數的期望值和變異數。求投超過 5 次才進第一球的機率。

$$X \sim \text{Geometric}(0.3)$$

$$E[X] = \frac{1}{0.3} = \frac{10}{3} \approx 3.33$$

$$\text{Var}(X) = \frac{0.7}{0.09} = \frac{70}{9} \approx 7.78$$

$$P(X > 5) = q^5 = 0.7^5 = 0.16807$$

大約 16.8% 的機率要投超過 5 次。

> **📝 數值範例（一直丟骰子直到出 6）**：每次出 6 的機率 $p = 1/6$，$X$ = 丟到第一次出 6 時的次數。
>
> $X \sim \text{Geometric}(1/6)$
>
> $P(X = 1) = 1/6 \approx 0.167$（第一次就出 6）
> $P(X = 2) = (5/6)^1 \times (1/6) = 5/36 \approx 0.139$（第一次不是 6，第二次是 6）
> $P(X = 3) = (5/6)^2 \times (1/6) = 25/216 \approx 0.116$
>
> 期望要丟幾次？$E[X] = 1/p = 6$ 次（平均要丟 6 次才會出第一個 6，直覺上很合理！）
>
> **無記憶性的生活解釋**：假設你已經丟了 10 次都沒有出 6。你可能會想「我已經丟了這麼多次，下一次應該更容易出 6 了吧？」但無記憶性告訴你：不會！從現在開始，你還需要平均再丟 6 次才會出 6，就像你剛開始丟一樣。過去的失敗完全不影響未來。

---

## 4. 負二項分布 $\text{Negative Binomial}(r, p)$

### 4.1 定義與情境

一直做獨立 Bernoulli 試驗，直到第 $r$ 次成功。$X$ = 需要的總試驗次數。

> **🔰 白話定義**：Geometric 是「做到第 1 次成功」，Negative Binomial 是「做到第 $r$ 次成功」。就是 Geometric 的進階版！
>
> **什麼時候會用到？**
> - 打電話做問卷調查，需要 10 個人接受，每次成功率 30%，打幾通才夠？→ NB(10, 0.3)
> - 棒球打者要打出 3 支安打，每次打擊率 25%，需要幾個打席？→ NB(3, 0.25)

**和幾何分布的關係：** Geometric$(p)$ = Negative Binomial$(1, p)$。

### 4.2 PMF 推導

$X = k$ 表示：第 $k$ 次試驗是第 $r$ 次成功。這意味著：
- 前 $k - 1$ 次中恰好有 $r - 1$ 次成功（和 $k - r$ 次失敗）
- 第 $k$ 次是成功

$$P(X = k) = \binom{k-1}{r-1} p^{r-1} q^{k-r} \cdot p = \binom{k-1}{r-1} p^r q^{k-r}$$

$$\boxed{P(X = k) = \binom{k-1}{r-1} p^r (1-p)^{k-r}, \quad k = r, r+1, r+2, \ldots}$$

**解釋 $\binom{k-1}{r-1}$：** 前 $k-1$ 次中選哪 $r-1$ 次成功。最後一次一定是成功（第 $r$ 次成功），所以不在組合裡。

### 4.3 從 Geometric 累加推導

令 $X_1, X_2, \ldots, X_r$ 為獨立的隨機變數，其中 $X_i$ 代表「第 $i-1$ 次成功到第 $i$ 次成功之間需要的試驗次數」。

由無記憶性，每次「重新開始等待」的過程都像一個新的幾何分布：
$$X_i \sim \text{Geometric}(p), \quad \text{i.i.d.}$$

則總試驗次數：
$$X = X_1 + X_2 + \cdots + X_r \sim \text{Negative Binomial}(r, p)$$

### 4.4 E[X] 推導

利用 Geometric 的累加：
$$E[X] = E[X_1] + E[X_2] + \cdots + E[X_r] = r \cdot \frac{1}{p} = \frac{r}{p}$$

$$\boxed{E[X] = \frac{r}{p}}$$

### 4.5 Var(X) 推導

因為 $X_1, \ldots, X_r$ 獨立：
$$\text{Var}(X) = r \cdot \text{Var}(X_1) = r \cdot \frac{q}{p^2} = \frac{rq}{p^2}$$

$$\boxed{\text{Var}(X) = \frac{rq}{p^2} = \frac{r(1-p)}{p^2}}$$

### 4.6 MGF 推導

利用獨立性：
$$M_X(t) = [M_{X_1}(t)]^r = \left(\frac{pe^t}{1 - qe^t}\right)^r$$

$$\boxed{M_X(t) = \left(\frac{pe^t}{1 - qe^t}\right)^r, \quad t < \ln\frac{1}{q}}$$

### 4.7 範例

**問題：** 某銷售員每次拜訪客戶成交的機率是 20%。他需要成交 3 單才能完成月度目標。求他需要拜訪的客戶數的期望值和標準差。

$$X \sim \text{Negative Binomial}(3, 0.2)$$

$$E[X] = \frac{3}{0.2} = 15$$

$$\text{Var}(X) = \frac{3 \times 0.8}{0.04} = \frac{2.4}{0.04} = 60$$

$$\text{SD}(X) = \sqrt{60} \approx 7.75$$

平均需要拜訪 15 位客戶。

$$P(X = 3) = \binom{2}{2} (0.2)^3 (0.8)^0 = 1 \times 0.008 = 0.008$$

連續三次成交的機率只有 0.8%。

---

## 5. Poisson 分布 $\text{Poisson}(\lambda)$

### 5.1 定義與情境

用來描述「在固定時間/空間中，某事件發生的次數」。

> **🔰 白話定義**：在一段固定的時間（或空間）裡，數某件事發生了幾次。$\lambda$ 就是「平均次數」。
>
> **什麼時候會用到？** 只要是「在固定範圍內計數稀疏的事件」，都可以考慮 Poisson：
> - 一小時內便利商店來了幾個客人（平均 5 個 → $\lambda = 5$）
> - 一頁論文裡有幾個錯字（平均 0.3 個 → $\lambda = 0.3$）
> - 一天內某路口發生幾起車禍（平均 1.2 起 → $\lambda = 1.2$）
> - 一平方公尺的草地上有幾隻蟲（平均 8 隻 → $\lambda = 8$）
>
> **Poisson 的超酷特色**：期望值和變異數都等於 $\lambda$！如果你算出來的平均值和變異數差很多，就不太適合用 Poisson。

典型例子：
- 一小時內到達櫃台的顧客數
- 一頁文件中的錯字數
- 一天中收到的電話數
- 一平方公尺地面上的細菌數

### 5.2 PMF

$$\boxed{P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots}$$

**驗證加總為 1：**
$$\sum_{k=0}^{\infty} \frac{e^{-\lambda} \lambda^k}{k!} = e^{-\lambda} \sum_{k=0}^{\infty} \frac{\lambda^k}{k!} = e^{-\lambda} \cdot e^{\lambda} = 1 \quad \checkmark$$

（用了 Taylor 展開 $e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!}$）

### 5.3 從 Binomial 極限推導 Poisson

**定理：** 如果 $X_n \sim \text{Binomial}(n, p_n)$，且 $n \to \infty$，$p_n \to 0$，$np_n \to \lambda$（常數），則：

$$P(X_n = k) \to \frac{e^{-\lambda} \lambda^k}{k!}$$

**推導：**

令 $\lambda = np$，即 $p = \lambda/n$。

$$P(X_n = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

$$= \frac{n!}{k!(n-k)!} \left(\frac{\lambda}{n}\right)^k \left(1 - \frac{\lambda}{n}\right)^{n-k}$$

$$= \frac{n(n-1)(n-2)\cdots(n-k+1)}{n^k} \cdot \frac{\lambda^k}{k!} \cdot \left(1 - \frac{\lambda}{n}\right)^n \cdot \left(1 - \frac{\lambda}{n}\right)^{-k}$$

當 $n \to \infty$（$k$ 固定）：

- $\frac{n(n-1)\cdots(n-k+1)}{n^k} = 1 \cdot (1 - 1/n) \cdot (1 - 2/n) \cdots (1 - (k-1)/n) \to 1$

- $\left(1 - \frac{\lambda}{n}\right)^n \to e^{-\lambda}$（這是 $e$ 的定義之一）

- $\left(1 - \frac{\lambda}{n}\right)^{-k} \to 1$

因此：
$$P(X_n = k) \to 1 \cdot \frac{\lambda^k}{k!} \cdot e^{-\lambda} \cdot 1 = \frac{e^{-\lambda}\lambda^k}{k!} \quad \blacksquare$$

### 5.4 E[X] 推導

$$E[X] = \sum_{k=0}^{\infty} k \cdot \frac{e^{-\lambda}\lambda^k}{k!} = \sum_{k=1}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-1)!}$$

令 $j = k - 1$：
$$= e^{-\lambda} \lambda \sum_{j=0}^{\infty} \frac{\lambda^j}{j!} = e^{-\lambda} \lambda \cdot e^{\lambda} = \lambda$$

$$\boxed{E[X] = \lambda}$$

### 5.5 Var(X) 推導

先求 $E[X(X-1)]$：
$$E[X(X-1)] = \sum_{k=2}^{\infty} k(k-1) \frac{e^{-\lambda}\lambda^k}{k!} = \sum_{k=2}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-2)!}$$

令 $j = k - 2$：
$$= e^{-\lambda}\lambda^2 \sum_{j=0}^{\infty} \frac{\lambda^j}{j!} = e^{-\lambda}\lambda^2 e^{\lambda} = \lambda^2$$

$$E[X^2] = E[X(X-1)] + E[X] = \lambda^2 + \lambda$$

$$\text{Var}(X) = E[X^2] - (E[X])^2 = \lambda^2 + \lambda - \lambda^2 = \lambda$$

$$\boxed{\text{Var}(X) = \lambda}$$

**Poisson 分布的一大特色：期望值 = 變異數 = $\lambda$！**

如果實際資料的平均值和變異數差很多，就不太適合用 Poisson 模型。

### 5.6 MGF 推導

$$M_X(t) = E[e^{tX}] = \sum_{k=0}^{\infty} e^{tk} \frac{e^{-\lambda}\lambda^k}{k!} = e^{-\lambda} \sum_{k=0}^{\infty} \frac{(\lambda e^t)^k}{k!} = e^{-\lambda} \cdot e^{\lambda e^t} = e^{\lambda(e^t - 1)}$$

$$\boxed{M_X(t) = e^{\lambda(e^t - 1)}}$$

**驗證 E[X]：** $M_X'(t) = \lambda e^t \cdot e^{\lambda(e^t-1)}$，$M_X'(0) = \lambda \cdot 1 = \lambda$ ✓

### 5.7 Poisson 的可加性

如果 $X \sim \text{Poisson}(\lambda_1)$，$Y \sim \text{Poisson}(\lambda_2)$，且 $X, Y$ 獨立，則：
$$X + Y \sim \text{Poisson}(\lambda_1 + \lambda_2)$$

**用 MGF 證明：**
$$M_{X+Y}(t) = M_X(t) \cdot M_Y(t) = e^{\lambda_1(e^t-1)} \cdot e^{\lambda_2(e^t-1)} = e^{(\lambda_1+\lambda_2)(e^t-1)}$$

這就是 $\text{Poisson}(\lambda_1 + \lambda_2)$ 的 MGF！由 MGF 唯一性，得證。$\blacksquare$

### 5.8 範例

**問題：** 某路口平均每小時發生 2 起交通事故。

(a) 某小時恰好發生 3 起的機率？
(b) 某小時沒有事故的機率？
(c) 兩小時內發生超過 5 起的機率？

$$X \sim \text{Poisson}(2)$$

**(a)**
$$P(X = 3) = \frac{e^{-2} \cdot 2^3}{3!} = \frac{e^{-2} \cdot 8}{6} = \frac{4e^{-2}}{3} \approx \frac{4 \times 0.1353}{3} \approx 0.1804$$

**(b)**
$$P(X = 0) = \frac{e^{-2} \cdot 2^0}{0!} = e^{-2} \approx 0.1353$$

**(c)** 兩小時內，$Y \sim \text{Poisson}(4)$（Poisson 可加性）。

$$P(Y > 5) = 1 - P(Y \leq 5) = 1 - \sum_{k=0}^{5} \frac{e^{-4} \cdot 4^k}{k!}$$

$$= 1 - e^{-4}\left(1 + 4 + 8 + \frac{32}{3} + \frac{32}{3} + \frac{128}{15}\right)$$
$$= 1 - e^{-4}\left(1 + 4 + 8 + 10.667 + 10.667 + 8.533\right)$$
$$= 1 - e^{-4} \times 42.867$$
$$= 1 - 0.01832 \times 42.867$$
$$\approx 1 - 0.7851 = 0.2149$$

大約 21.5%。

> **📝 數值範例（一小時內來幾個客人）**：便利商店平均每小時來 3 個客人，$X \sim \text{Poisson}(3)$。
>
> 一小時內剛好沒有客人：$P(X=0) = \frac{e^{-3} \times 3^0}{0!} = e^{-3} \approx 0.0498$（約 5%）
> 一小時內來 1 個客人：$P(X=1) = \frac{e^{-3} \times 3^1}{1!} = 3e^{-3} \approx 0.1494$（約 15%）
> 一小時內來 2 個客人：$P(X=2) = \frac{e^{-3} \times 3^2}{2!} = \frac{9e^{-3}}{2} \approx 0.2240$（約 22%）
> 一小時內來 3 個客人：$P(X=3) = \frac{e^{-3} \times 3^3}{3!} = \frac{27e^{-3}}{6} \approx 0.2240$（約 22%）
>
> $E[X] = 3$（平均 3 個客人），$\text{Var}(X) = 3$（變異數也是 3）
>
> 兩小時內呢？用可加性：$Y \sim \text{Poisson}(6)$，$E[Y] = 6$

---

## 6. Poisson 近似 Binomial

### 6.1 適用條件

當 $\text{Binomial}(n, p)$ 的 $n$ 很大、$p$ 很小，使得 $\lambda = np$ 適中時，可以用 $\text{Poisson}(\lambda)$ 近似。

**經驗法則：** $n \geq 20$ 且 $p \leq 0.05$ 時，近似效果不錯。或者更寬鬆地，$n \geq 100$ 且 $np \leq 10$。

### 6.2 近似範例

**問題：** 某零件的不良率是 0.002。一批有 1000 個零件。不良品超過 3 個的機率？

精確計算：$X \sim \text{Binomial}(1000, 0.002)$

$$P(X > 3) = 1 - \sum_{k=0}^{3} \binom{1000}{k} (0.002)^k (0.998)^{1000-k}$$

這個計算涉及 $\binom{1000}{k}$ 這種大數，不方便手算。

**Poisson 近似：** $\lambda = np = 1000 \times 0.002 = 2$

$$P(X > 3) \approx 1 - \sum_{k=0}^{3} \frac{e^{-2} \cdot 2^k}{k!}$$
$$= 1 - e^{-2}\left(1 + 2 + 2 + \frac{4}{3}\right)$$
$$= 1 - e^{-2} \times \frac{19}{3}$$
$$= 1 - 0.1353 \times 6.333$$
$$\approx 1 - 0.8571 = 0.1429$$

精確答案大約是 0.1428，近似非常好！

### 6.3 近似誤差

近似的總變差距離（total variation distance）大約是 $p$（和 $n$ 無關！），所以 $p$ 越小近似越好。

---

## 7. 超幾何分布（Hypergeometric Distribution）

### 7.1 定義與情境

> **🔰 白話定義**：和 Binomial 很像，都是「數成功幾次」。差別在於 Hypergeometric 是「不放回」抽樣（從有限母體中一個一個拿出來），而 Binomial 是「有放回」（或無限母體）。
>
> **什麼時候會用到？**
> - 52 張撲克牌抽 5 張，有幾張紅心？→ Hypergeometric(52, 13, 5)
> - 一箱 100 個零件有 5 個不良品，抽檢 10 個，有幾個不良品？→ Hypergeometric(100, 5, 10)
> - 彩券開獎：從 49 個號碼中開出 6 個，你選的 6 個中了幾個？→ Hypergeometric
>
> **和 Binomial 的簡單比較**：放回 → Binomial，不放回 → Hypergeometric。當母體很大時，兩者幾乎一樣。

從一個有 $N$ 個物品的母體（其中 $K$ 個是「成功」、$N-K$ 個是「失敗」）中，**不放回**地抽 $n$ 個。$X$ = 抽到的成功品數。

$$X \sim \text{Hypergeometric}(N, K, n)$$

### 7.2 PMF 推導

$$P(X = k) = \frac{\text{從 K 個成功品中選 k 個} \times \text{從 N-K 個失敗品中選 n-k 個}}{\text{從 N 個中選 n 個}}$$

$$\boxed{P(X = k) = \frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}}$$

其中 $k$ 的範圍是 $\max(0, n-N+K) \leq k \leq \min(n, K)$。

### 7.3 E[X] 推導

$$E[X] = \sum_{k} k \cdot \frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$$

**技巧：** 用 $k\binom{K}{k} = K\binom{K-1}{k-1}$。

$$E[X] = \frac{K}{\binom{N}{n}} \sum_{k=1}^{\min(n,K)} \binom{K-1}{k-1}\binom{N-K}{n-k}$$

令 $j = k - 1$：
$$= \frac{K}{\binom{N}{n}} \sum_{j=0}^{\min(n-1,K-1)} \binom{K-1}{j}\binom{N-K}{(n-1)-j}$$

由 Vandermonde 恆等式：$\sum_j \binom{K-1}{j}\binom{N-K}{n-1-j} = \binom{N-1}{n-1}$。

$$E[X] = \frac{K \cdot \binom{N-1}{n-1}}{\binom{N}{n}} = K \cdot \frac{(N-1)!/(n-1)!(N-n)!}{N!/n!(N-n)!} = K \cdot \frac{n}{N} = \frac{nK}{N}$$

$$\boxed{E[X] = \frac{nK}{N} = n \cdot \frac{K}{N}}$$

**直觀：** 就是 $n$ 乘以每個物品是成功品的機率 $K/N$，和 Binomial 的 $np$ 形式一樣！（令 $p = K/N$）

### 7.4 Var(X) 推導

$$\boxed{\text{Var}(X) = n \cdot \frac{K}{N} \cdot \frac{N-K}{N} \cdot \frac{N-n}{N-1} = npq \cdot \frac{N-n}{N-1}}$$

其中 $p = K/N$，$q = 1 - p = (N-K)/N$。

比較 Binomial 的 $\text{Var} = npq$，Hypergeometric 多了一個修正因子 $\frac{N-n}{N-1}$，稱為**有限母體修正因子**（finite population correction, FPC）。

- 當 $N \gg n$ 時，$\frac{N-n}{N-1} \approx 1$，Hypergeometric $\approx$ Binomial
- 當 $n = N$ 時，$\frac{N-n}{N-1} = 0$，變異數為 0（全部都抽了，沒有隨機性）
- FPC 永遠 $\leq 1$，所以不放回的變異數 $\leq$ 放回的變異數

### 7.5 與 Binomial 的比較

| | Hypergeometric | Binomial |
|---|---|---|
| 抽樣方式 | 不放回 | 有放回 |
| 試驗獨立？ | 否 | 是 |
| 母體大小 | 有限 $N$ | 無限（或有放回） |
| $E[X]$ | $nK/N$ | $np$ |
| $\text{Var}(X)$ | $npq \cdot \frac{N-n}{N-1}$ | $npq$ |
| 近似關係 | 當 $N \to \infty$ 且 $K/N \to p$ 時 → Binomial | — |

### 7.6 MGF

超幾何分布的 MGF 沒有簡潔的封閉形式，考試中通常不會要求推導。形式上是：

$$M_X(t) = \frac{\binom{N-K}{n}}{\binom{N}{n}} \cdot {}_2F_1(-n, -K; N-K-n+1; e^t)$$

其中 ${}_2F_1$ 是超幾何函數。這太複雜了，實務上不需要記。

### 7.7 範例

**問題：** 一副 52 張撲克牌，抽 5 張（不放回），恰好有 2 張紅心的機率？

$$N = 52, \quad K = 13 \text{（紅心數）}, \quad n = 5$$
$$X \sim \text{Hypergeometric}(52, 13, 5)$$

$$P(X = 2) = \frac{\binom{13}{2}\binom{39}{3}}{\binom{52}{5}}$$

計算：
- $\binom{13}{2} = 78$
- $\binom{39}{3} = \frac{39 \times 38 \times 37}{6} = 9139$
- $\binom{52}{5} = 2598960$

$$P(X = 2) = \frac{78 \times 9139}{2598960} = \frac{712842}{2598960} \approx 0.2743$$

$$E[X] = 5 \times \frac{13}{52} = 5 \times 0.25 = 1.25$$

---

## 8. 離散均勻分布（Discrete Uniform Distribution）

### 8.1 定義

$X$ 在 $\{a, a+1, a+2, \ldots, b\}$ 上均勻分布，每個值的機率相等。

記為 $X \sim \text{DUnif}(a, b)$。令 $n = b - a + 1$（值的個數）。

### 8.2 PMF

$$\boxed{P(X = k) = \frac{1}{n} = \frac{1}{b-a+1}, \quad k = a, a+1, \ldots, b}$$

### 8.3 E[X] 推導

$$E[X] = \frac{1}{n}\sum_{k=a}^{b} k = \frac{1}{n} \cdot \frac{(a + b) \cdot n}{2} = \frac{a + b}{2}$$

（用了等差數列求和公式）

$$\boxed{E[X] = \frac{a + b}{2}}$$

### 8.4 Var(X) 推導

先令 $Y = X - a$，則 $Y \sim \text{DUnif}(0, n-1)$，$\text{Var}(X) = \text{Var}(Y)$。

$$E[Y] = \frac{n-1}{2}$$

$$E[Y^2] = \frac{1}{n}\sum_{k=0}^{n-1} k^2 = \frac{1}{n} \cdot \frac{(n-1)n(2n-1)}{6} = \frac{(n-1)(2n-1)}{6}$$

$$\text{Var}(Y) = E[Y^2] - (E[Y])^2 = \frac{(n-1)(2n-1)}{6} - \frac{(n-1)^2}{4}$$

$$= (n-1)\left[\frac{2n-1}{6} - \frac{n-1}{4}\right] = (n-1) \cdot \frac{2(2n-1) - 3(n-1)}{12}$$

$$= (n-1) \cdot \frac{4n - 2 - 3n + 3}{12} = (n-1) \cdot \frac{n + 1}{12} = \frac{(n-1)(n+1)}{12} = \frac{n^2 - 1}{12}$$

$$\boxed{\text{Var}(X) = \frac{(b-a+1)^2 - 1}{12} = \frac{n^2 - 1}{12}}$$

其中 $n = b - a + 1$。

**特例：公平骰子** $X \sim \text{DUnif}(1, 6)$，$n = 6$。
$$E[X] = \frac{1+6}{2} = 3.5, \quad \text{Var}(X) = \frac{36-1}{12} = \frac{35}{12} \approx 2.917$$

### 8.5 MGF 推導

$$M_X(t) = \frac{1}{n}\sum_{k=a}^{b} e^{tk} = \frac{e^{ta}}{n} \sum_{j=0}^{n-1} e^{tj} = \frac{e^{ta}}{n} \cdot \frac{e^{tn} - 1}{e^t - 1} = \frac{e^{ta}(e^{tn} - 1)}{n(e^t - 1)}$$

$$\boxed{M_X(t) = \frac{e^{ta}(e^{tn} - 1)}{n(e^t - 1)}, \quad t \neq 0}$$

（$t = 0$ 時，$M_X(0) = 1$，要用 L'Hopital 法則驗證連續性）

### 8.6 範例

**問題：** 擲一顆公平骰子，求點數的期望值和標準差。

$$X \sim \text{DUnif}(1, 6)$$

$$E[X] = \frac{1 + 6}{2} = 3.5$$

$$\text{Var}(X) = \frac{6^2 - 1}{12} = \frac{35}{12} \approx 2.917$$

$$\text{SD}(X) = \sqrt{35/12} \approx 1.708$$

---

## 9. 分布之間的關係

### 9.1 關係圖

```
                    Bernoulli(p)
                    /          \
             n 次累加         極限 (p→0)
                  /              \
          Binomial(n,p)     Poisson(λ)
              |                  |
         p→0, np→λ        可加性
              \                 |
               → Poisson(λ) ←──┘

          Geometric(p) ──r次累加──→ Negative Binomial(r,p)
               |
           Geo = NB(1,p)

      Hypergeometric(N,K,n) ──N→∞──→ Binomial(n, K/N)
```

### 9.2 重要關係推導

**關係 1：Bernoulli 的和 = Binomial**

若 $X_1, \ldots, X_n \stackrel{iid}{\sim} \text{Bernoulli}(p)$，則 $\sum X_i \sim \text{Binomial}(n, p)$。

（前面已在 Binomial 的 MGF 用獨立性推導過。）

> **📝 用數值驗證**：丟 3 次公平硬幣（$p = 0.5$），令 $X_i = 1$ 若第 $i$ 次是正面，$X_i \sim \text{Bernoulli}(0.5)$。
> 正面總數 $S = X_1 + X_2 + X_3 \sim \text{Binomial}(3, 0.5)$。
>
> 用 Binomial 公式算：
> $P(S = 0) = \binom{3}{0}(0.5)^3 = 0.125$
> $P(S = 1) = \binom{3}{1}(0.5)^3 = 0.375$
> $P(S = 2) = \binom{3}{2}(0.5)^3 = 0.375$
> $P(S = 3) = \binom{3}{3}(0.5)^3 = 0.125$
>
> 直接列舉驗證（8 個等可能結果：HHH, HHT, HTH, HTT, THH, THT, TTH, TTT）：
> 0 個正面：TTT → 1/8 = 0.125 ✓
> 1 個正面：HTT, THT, TTH → 3/8 = 0.375 ✓
> 2 個正面：HHT, HTH, THH → 3/8 = 0.375 ✓
> 3 個正面：HHH → 1/8 = 0.125 ✓

**關係 2：Geometric 的和 = Negative Binomial**

若 $X_1, \ldots, X_r \stackrel{iid}{\sim} \text{Geometric}(p)$，則 $\sum X_i \sim \text{NB}(r, p)$。

（用 MGF：$M_{\sum X_i}(t) = \left(\frac{pe^t}{1-qe^t}\right)^r$ = NB 的 MGF。）

**關係 3：Binomial → Poisson（極限）**

$\text{Binomial}(n, \lambda/n) \xrightarrow{n \to \infty} \text{Poisson}(\lambda)$

（前面第 5.3 節已完整推導。）

**關係 4：Hypergeometric → Binomial（極限）**

$\text{Hypergeometric}(N, K, n) \xrightarrow{N \to \infty, K/N \to p} \text{Binomial}(n, p)$

直觀：母體很大時，不放回和放回的差別消失。

**關係 5：Poisson 的和 = Poisson**

若 $X \sim \text{Poisson}(\lambda_1)$，$Y \sim \text{Poisson}(\lambda_2)$，獨立，則 $X + Y \sim \text{Poisson}(\lambda_1 + \lambda_2)$。

**關係 6：Binomial 的和 = Binomial**

若 $X \sim \text{Bin}(n_1, p)$，$Y \sim \text{Bin}(n_2, p)$，獨立（同一個 $p$！），則 $X + Y \sim \text{Bin}(n_1 + n_2, p)$。

用 MGF：$(pe^t + q)^{n_1} \cdot (pe^t + q)^{n_2} = (pe^t + q)^{n_1 + n_2}$。

**注意：** $p$ 必須相同！如果 $p$ 不同，和就不是 Binomial。

---

## 10. 離散分布總覽比較表

| 分布 | 參數 | PMF $P(X=k)$ | $E[X]$ | $\text{Var}(X)$ | MGF $M_X(t)$ |
|------|------|-------------|--------|----------------|---------------|
| Bernoulli$(p)$ | $p$ | $p^k q^{1-k}$, $k=0,1$ | $p$ | $pq$ | $q + pe^t$ |
| Binomial$(n,p)$ | $n, p$ | $\binom{n}{k}p^k q^{n-k}$, $k=0,\ldots,n$ | $np$ | $npq$ | $(q+pe^t)^n$ |
| Geometric$(p)$ | $p$ | $q^{k-1}p$, $k=1,2,\ldots$ | $\frac{1}{p}$ | $\frac{q}{p^2}$ | $\frac{pe^t}{1-qe^t}$ |
| NegBin$(r,p)$ | $r, p$ | $\binom{k-1}{r-1}p^r q^{k-r}$, $k=r,r+1,\ldots$ | $\frac{r}{p}$ | $\frac{rq}{p^2}$ | $\left(\frac{pe^t}{1-qe^t}\right)^r$ |
| Poisson$(\lambda)$ | $\lambda$ | $\frac{e^{-\lambda}\lambda^k}{k!}$, $k=0,1,\ldots$ | $\lambda$ | $\lambda$ | $e^{\lambda(e^t-1)}$ |
| Hypergeometric | $N,K,n$ | $\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$ | $\frac{nK}{N}$ | $npq\frac{N-n}{N-1}$ | （無簡潔形式） |
| DUnif$(a,b)$ | $a, b$ | $\frac{1}{b-a+1}$, $k=a,\ldots,b$ | $\frac{a+b}{2}$ | $\frac{n^2-1}{12}$ | $\frac{e^{ta}(e^{tn}-1)}{n(e^t-1)}$ |

其中 $q = 1-p$，$n = b-a+1$（在 DUnif 中）。

---

## 11. 「何時用哪個分布」決策指南

### 決策流程

```
問題開始
  │
  ├─ 每次試驗只有成功/失敗兩種結果？
  │    │
  │    ├─ 是 → 只有一次試驗？
  │    │         ├─ 是 → Bernoulli(p)
  │    │         └─ 否 → 固定次數 n 次？
  │    │                   ├─ 是 → 放回/獨立？
  │    │                   │        ├─ 是 → Binomial(n,p)
  │    │                   │        └─ 否（不放回，有限母體）→ Hypergeometric(N,K,n)
  │    │                   └─ 否 → 試驗到第 r 次成功為止？
  │    │                             ├─ r=1 → Geometric(p)
  │    │                             └─ r>1 → Negative Binomial(r,p)
  │    │
  │    └─ 否 → 計數「次數」在連續時間/空間中？
  │              ├─ 是 → Poisson(λ)
  │              └─ 否 → 每個值等機率？
  │                        ├─ 是 → Discrete Uniform(a,b)
  │                        └─ 否 → 其他分布（考慮連續分布等）
```

### 關鍵問題清單

| 問自己的問題 | 答案對應的分布 |
|---|---|
| 只做一次，成功或失敗？ | Bernoulli |
| 固定做 $n$ 次，數成功幾次？（獨立） | Binomial |
| 固定做 $n$ 次，數成功幾次？（不放回） | Hypergeometric |
| 做到第一次成功為止？ | Geometric |
| 做到第 $r$ 次成功為止？ | Negative Binomial |
| 計算某段時間/空間中的事件數？ | Poisson |
| $n$ 很大，$p$ 很小，$np$ 適中？ | 用 Poisson 近似 Binomial |
| 每個結果等機率？ | Discrete Uniform |

### 常見陷阱

1. **Binomial vs Hypergeometric：** 問自己「是放回還是不放回？」放回 → Binomial，不放回 → Hypergeometric。但如果母體遠大於樣本（$N \gg n$），可以用 Binomial 近似。

2. **Geometric vs Negative Binomial：** Geometric 是 NB 的特殊情況（$r = 1$）。

3. **Binomial vs Poisson：** Binomial 有固定的 $n$，Poisson 沒有上限。當 $n$ 大 $p$ 小時 Binomial 可用 Poisson 近似。

4. **Geometric 的兩種定義：** 一定要確認是「試驗次數」（從 1 開始）還是「失敗次數」（從 0 開始）。

5. **負二項的值域：** 從 $r$ 開始（因為至少需要 $r$ 次試驗才能有 $r$ 次成功）。

---

## 12. 綜合範例

### 範例：哪個分布？

**問題 1：** 一箱 100 個零件中有 5 個不良品。隨機抽 10 個檢查（不放回），不良品數的分布是？

→ 不放回 + 有限母體 → **Hypergeometric**(100, 5, 10)

**問題 2：** 同上，但改為有放回抽樣。

→ 有放回 + 每次成功/失敗 → **Binomial**(10, 0.05)

**問題 3：** 一條生產線的不良率是 0.05，持續生產直到出現第 3 個不良品。總共生產的產品數？

→ 做到第 $r = 3$ 次「成功」（這裡成功 = 出現不良品） → **Negative Binomial**(3, 0.05)

$E[X] = 3/0.05 = 60$，平均要生產 60 個才會出現第 3 個不良品。

**問題 4：** 同問題 3，但只是問第一個不良品出現時的產品數。

→ $r = 1$ → **Geometric**(0.05)

$E[X] = 1/0.05 = 20$

**問題 5：** 某服務台平均每分鐘接到 3 通電話。5 分鐘內接到超過 20 通的機率？

→ 固定時間內的事件計數 → **Poisson**(15)（$\lambda = 3 \times 5 = 15$）

$P(X > 20) = 1 - P(X \leq 20) = 1 - \sum_{k=0}^{20} \frac{e^{-15} \cdot 15^k}{k!}$

（此值需查表或用軟體計算，大約 0.083）

---

## 13. 附錄：常用求和公式

推導分布性質時常用到以下公式：

| 公式 | 結果 |
|------|------|
| $\sum_{k=0}^{\infty} r^k$ ($\|r\|<1$) | $\frac{1}{1-r}$ |
| $\sum_{k=1}^{\infty} kr^{k-1}$ | $\frac{1}{(1-r)^2}$ |
| $\sum_{k=2}^{\infty} k(k-1)r^{k-2}$ | $\frac{2}{(1-r)^3}$ |
| $\sum_{k=0}^{\infty} \frac{x^k}{k!}$ | $e^x$ |
| $\sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$ | $(x+y)^n$ |
| $\sum_{j=0}^{k} \binom{m}{j}\binom{n}{k-j}$ | $\binom{m+n}{k}$ (Vandermonde) |
| $\sum_{k=1}^{n} k$ | $\frac{n(n+1)}{2}$ |
| $\sum_{k=1}^{n} k^2$ | $\frac{n(n+1)(2n+1)}{6}$ |

---

### ✅ 自我檢測

1. **（觀念題）** 以下每個情境該用哪個分布？
   (a) 擲一枚硬幣，看是否正面 → ?
   (b) 擲 10 枚硬幣，數正面的個數 → ?
   (c) 一直擲硬幣直到第一次正面，數擲的次數 → ?
   (d) 一小時內收到的 email 數（平均 4 封） → ?
   (e) 50 張牌中有 10 張紅牌，不放回抽 5 張，數紅牌數 → ?

2. **（計算題）** 某餐廳平均每小時有 6 組客人到達，假設服從 Poisson 分布。
   (a) 某小時恰好來 4 組客人的機率是多少？
   (b) 某小時沒有客人的機率是多少？（提示：$e^{-6} \approx 0.00248$）

3. **（進階應用）** 一位業務員每次拜訪客戶成功簽約的機率是 20%。
   (a) 他至少要拜訪幾位客戶，才能讓「至少簽到 1 單」的機率超過 90%？（提示：用幾何分布的 $P(X > k) = q^k$，找最小的 $k$ 使得 $1 - 0.8^k > 0.9$）
   (b) 他拜訪了 10 位客戶，恰好簽到 3 單的機率是多少？（提示：用 Binomial）

<details>
<summary>參考答案</summary>

1. (a) Bernoulli(0.5)
   (b) Binomial(10, 0.5)
   (c) Geometric(0.5)
   (d) Poisson(4)
   (e) Hypergeometric(50, 10, 5)

2. $X \sim \text{Poisson}(6)$

   (a) $P(X=4) = \frac{e^{-6} \times 6^4}{4!} = \frac{e^{-6} \times 1296}{24} = 54 \times e^{-6} \approx 54 \times 0.00248 \approx 0.1339$

   (b) $P(X=0) = e^{-6} \approx 0.00248$，非常低！約 0.25%。

3. (a) 需要 $1 - 0.8^k > 0.9$，即 $0.8^k < 0.1$。
   $k = 10$：$0.8^{10} = 0.1074 > 0.1$（不夠）
   $k = 11$：$0.8^{11} = 0.0859 < 0.1$（夠了！）
   答案：至少要拜訪 11 位客戶。

   (b) $X \sim \text{Binomial}(10, 0.2)$
   $P(X=3) = \binom{10}{3}(0.2)^3(0.8)^7 = 120 \times 0.008 \times 0.2097 \approx 0.2013$，約 20.1%。

</details>

---

> 這三章的內容構成了機率論的基礎。掌握了這些，就有足夠的功力去處理連續分布、大數法則、中央極限定理等進階主題。
