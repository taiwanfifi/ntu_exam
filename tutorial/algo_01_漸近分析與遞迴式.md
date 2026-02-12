# 演算法教學 01：漸近分析與遞迴式

> 台大演算法課教學講義
> 本篇是整個演算法課程的基石。如果你不能精確地分析一個演算法的時間複雜度，那後面的一切都是空談。

---

## 本章基礎觀念（零基礎必讀）

### 為什麼需要學漸近分析與遞迴式？

想像你寫了一支程式來搜尋一個名單裡的電話號碼。名單有 100 筆時跑得飛快，但名單變成 100 萬筆時卻要等好幾分鐘。你想知道：**隨著資料量變大，我的程式到底會變多慢？**

這就是「漸近分析」要回答的問題。它給你一套數學工具，讓你不用真的跑程式，光看程式碼結構就能預測效能。

舉個最簡單的例子：

```python
# 程式 A：找到名單中某個人
for i in range(n):        # 跑 n 次
    if names[i] == target:
        return i
# → 最多跑 n 次，我們說它是 O(n)

# 程式 B：比較名單中所有人的配對
for i in range(n):        # 跑 n 次
    for j in range(n):    # 每次又跑 n 次
        compare(i, j)
# → 跑 n × n = n² 次，我們說它是 O(n²)
```

當 n = 1000 時，程式 A 做 1,000 次運算，程式 B 做 1,000,000 次運算。差距很明顯吧？**漸近分析就是幫你判斷「這支程式的效率等級是什麼」**。

而「遞迴式」則是分析遞迴程式效能的工具。很多高效演算法（如快速排序、合併排序）都是遞迴的，你需要解遞迴式才能知道它們多快。

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 漸近記號 | Asymptotic Notation | 描述函數在 n 很大時成長速度的符號 | $O(n)$、$\Theta(n^2)$ |
| Big-O | Big-O | 「最多這麼慢」（上界） | $3n+5 = O(n)$ |
| Big-Omega | Big-Omega ($\Omega$) | 「至少這麼慢」（下界） | $3n+5 = \Omega(n)$ |
| Big-Theta | Big-Theta ($\Theta$) | 「剛好這麼快」（精確等級） | $3n+5 = \Theta(n)$ |
| 遞迴式 | Recurrence Relation | 把 T(n) 用 T(更小的 n) 來表示 | $T(n) = 2T(n/2) + n$ |
| Master Theorem | Master Theorem | 一個公式，直接解特定形式的遞迴式 | 見 3.2 節 |
| 遞迴樹 | Recursion Tree | 把遞迴展開成樹狀圖，每層算工作量再加總 | 見第 4 節 |
| 代入法 | Substitution Method | 先猜答案，再用數學歸納法驗證 | 見第 5 節 |
| 數學歸納法 | Mathematical Induction | 先證最小的情況成立，再證「如果 k 成立則 k+1 也成立」 | 見 5.2 節 |
| 幾何級數 | Geometric Series | 每項是前一項乘以固定比值 r 的數列之和 | $1 + r + r^2 + \cdots$ |

### 前置知識

- **程式基礎**：理解 for 迴圈、巢狀迴圈、遞迴函數的概念
- **基礎數學**：對數（$\log$）的意義（$\log_2 8 = 3$ 代表 2 要乘自己 3 次才會等於 8）、指數運算、基本不等式
- **如果你不熟 $\log$**：記住一個直覺——$\log_2 n$ 大約是「把 n 一直除以 2，要除幾次才會到 1」。例如 $\log_2 1024 = 10$（1024 除以 2 要除 10 次）

---

## 1. 漸近記號完整教學

### 1.1 為什麼需要漸近記號？

我們分析演算法的效率時，不關心常數倍差異（畢竟換台電腦就差好幾倍），也不關心小輸入的表現。我們真正關心的是：**當輸入夠大的時候，這個演算法的成長速度像什麼函數？**

漸近記號就是用來精確描述這個「成長速度」的數學工具。

---

### 1.2 五個漸近記號的正式定義

#### Big-O：O(g(n)) — 漸近上界

**正式定義：**
$$
f(n) = O(g(n)) \iff \exists\, c > 0,\; \exists\, n_0 > 0,\; \forall\, n \geq n_0:\; 0 \leq f(n) \leq c \cdot g(n)
$$

**直覺解釋：** f(n) 的成長速度「不超過」g(n)。也就是說，當 n 夠大之後，f(n) 一定被 c·g(n) 壓在下面。你可以想成「f(n) ≤ g(n)」的漸近版本。

**白話：** 「f 最多跟 g 一樣快。」

> **具體直覺範例**：假設一支程式的確切執行次數是 $f(n) = 3n + 10$。
> - 當 $n = 100$ 時，$f(100) = 310$
> - 當 $n = 1000$ 時，$f(1000) = 3010$
> - 當 $n = 10000$ 時，$f(10000) = 30010$
>
> 你會發現 $f(n)$ 的成長速度跟 $n$ 差不多（那個 +10 越來越不重要，常數 3 也不影響「等級」）。
> 所以 $3n + 10 = O(n)$，意思是「這支程式最多就是線性等級」。
>
> **常見程式碼對應**：
> | 程式碼結構 | 執行次數 | Big-O |
> |-----------|---------|-------|
> | 一個 for 迴圈跑 n 次 | $n$ | $O(n)$ |
> | 兩層巢狀 for 迴圈，各跑 n 次 | $n^2$ | $O(n^2)$ |
> | 每次砍一半的迴圈（如二分搜尋） | $\log n$ | $O(\log n)$ |
> | 先排序再掃描一次 | $n\log n + n$ | $O(n \log n)$ |

#### Big-Omega：Ω(g(n)) — 漸近下界

**正式定義：**
$$
f(n) = \Omega(g(n)) \iff \exists\, c > 0,\; \exists\, n_0 > 0,\; \forall\, n \geq n_0:\; 0 \leq c \cdot g(n) \leq f(n)
$$

**直覺解釋：** f(n) 的成長速度「至少是」g(n)。你可以想成「f(n) ≥ g(n)」的漸近版本。

**白話：** 「f 至少跟 g 一樣快（或更快）。」

#### Big-Theta：Θ(g(n)) — 漸近緊界

**正式定義：**
$$
f(n) = \Theta(g(n)) \iff \exists\, c_1 > 0,\; c_2 > 0,\; \exists\, n_0 > 0,\; \forall\, n \geq n_0:\; 0 \leq c_1 \cdot g(n) \leq f(n) \leq c_2 \cdot g(n)
$$

**等價條件：** f(n) = O(g(n)) **且** f(n) = Ω(g(n))。

**直覺解釋：** f(n) 的成長速度「剛好就是」g(n) 的等級。被上下兩條線夾住。

**白話：** 「f 跟 g 一樣快。」

#### Little-o：o(g(n)) — 嚴格漸近上界（非緊的）

**正式定義：**
$$
f(n) = o(g(n)) \iff \forall\, c > 0,\; \exists\, n_0 > 0,\; \forall\, n \geq n_0:\; 0 \leq f(n) < c \cdot g(n)
$$

**等價條件：** $\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$

**注意跟 Big-O 的差別：** Big-O 只要「存在某個 c」就好，little-o 要求「對所有 c 都成立」。

**直覺解釋：** f(n) 比 g(n) 嚴格地慢。你可以想成「f(n) < g(n)」的漸近版本（嚴格小於）。

**白話：** 「f 嚴格比 g 慢。」

#### Little-omega：ω(g(n)) — 嚴格漸近下界（非緊的）

**正式定義：**
$$
f(n) = \omega(g(n)) \iff \forall\, c > 0,\; \exists\, n_0 > 0,\; \forall\, n \geq n_0:\; 0 \leq c \cdot g(n) < f(n)
$$

**等價條件：** $\lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty$

**直覺解釋：** f(n) 比 g(n) 嚴格地快。你可以想成「f(n) > g(n)」的漸近版本（嚴格大於）。

**白話：** 「f 嚴格比 g 快。」

---

### 1.3 五個記號的類比對照表

| 漸近記號 | 類比實數關係 | 意思 |
|----------|------------|------|
| f = O(g) | f ≤ g | f 不比 g 快 |
| f = Ω(g) | f ≥ g | f 不比 g 慢 |
| f = Θ(g) | f = g | f 跟 g 同級 |
| f = o(g) | f < g | f 嚴格比 g 慢 |
| f = ω(g) | f > g | f 嚴格比 g 快 |

**重要提醒：** 這個類比不是完美的！實數任意兩個都可以比大小，但函數不一定。例如 f(n) = n^{1+sin n} 跟 g(n) = n 就無法用漸近記號比較（因為 f 不斷震盪）。

---

### 1.4 重要性質

#### 遞移性 (Transitivity) — 全部五個記號都有

- 若 f = O(g) 且 g = O(h)，則 f = O(h)
- 若 f = Ω(g) 且 g = Ω(h)，則 f = Ω(h)
- 若 f = Θ(g) 且 g = Θ(h)，則 f = Θ(h)
- 若 f = o(g) 且 g = o(h)，則 f = o(h)
- 若 f = ω(g) 且 g = ω(h)，則 f = ω(h)

#### 自反性 (Reflexivity) — 只有 O, Ω, Θ

- f = O(f) ✓
- f = Ω(f) ✓
- f = Θ(f) ✓
- f = o(f) ✗（因為 f 不會嚴格小於自己）
- f = ω(f) ✗

#### 對稱性 (Symmetry) — 只有 Θ

- f = Θ(g) ⟺ g = Θ(f) ✓

#### 轉置對稱性 (Transpose Symmetry)

- f = O(g) ⟺ g = Ω(f)
- f = o(g) ⟺ g = ω(f)

**這個性質超好用！** 要證 f = Ω(g) 覺得很煩的話，可以反過來證 g = O(f)。

---

### 1.5 常見函數的成長速度排序

從慢到快：

$$
1 \prec \log\log n \prec \log n \prec \sqrt{n} \prec n \prec n\log n \prec n^2 \prec n^3 \prec 2^n \prec n! \prec n^n
$$

更精細的排序：

$$
1 \prec \log\log n \prec \sqrt{\log n} \prec \log n \prec (\log n)^2 \prec \sqrt{n} \prec n^{2/3} \prec n \prec n\log n \prec n^{3/2} \prec n^2 \prec n^2 \log n \prec n^3 \prec 2^n \prec 3^n \prec n! \prec n^n
$$

其中 $\prec$ 代表嚴格漸近小於（little-o 關係）。

**重要的比較結果：**

1. **任何多項式都打贏任何多對數 (polylog)：** $(\log n)^k = o(n^\epsilon)$ 對所有 $k > 0, \epsilon > 0$
2. **任何指數都打贏任何多項式：** $n^k = o(c^n)$ 對所有 $k > 0, c > 1$
3. **Stirling 近似：** $n! \approx \sqrt{2\pi n} \cdot (n/e)^n$，所以 $\log(n!) = \Theta(n \log n)$

---

### 1.6 實用技巧：用極限判斷漸近關係

$$
L = \lim_{n \to \infty} \frac{f(n)}{g(n)}
$$

| L 的值 | 結論 |
|--------|------|
| L = 0 | f = o(g)，當然也是 f = O(g) |
| L = ∞ | f = ω(g)，當然也是 f = Ω(g) |
| 0 < L < ∞ | f = Θ(g) |
| 極限不存在 | 不能直接下結論，要回到定義 |

---

## 2. 常見的證明與反證範例

### 範例 2.1：證明 3n² + 7n + 2 = O(n²)

**目標：** 找到 c > 0 和 n₀ > 0，使得對所有 n ≥ n₀，3n² + 7n + 2 ≤ cn²。

**推導：**

對 n ≥ 1：
- 7n ≤ 7n²（因為 n ≤ n²）
- 2 ≤ 2n²（因為 1 ≤ n²）

所以：
$$
3n^2 + 7n + 2 \leq 3n^2 + 7n^2 + 2n^2 = 12n^2
$$

取 c = 12, n₀ = 1，則對所有 n ≥ 1：
$$
3n^2 + 7n + 2 \leq 12n^2
$$

因此 3n² + 7n + 2 = O(n²)。 ∎

---

### 範例 2.2：證明 3n² + 7n + 2 = Ω(n²)

**目標：** 找到 c > 0 和 n₀ > 0，使得對所有 n ≥ n₀，3n² + 7n + 2 ≥ cn²。

**推導：** 這個比較簡單，因為 3n² + 7n + 2 ≥ 3n² 對所有 n ≥ 0。

取 c = 3, n₀ = 0（或 1），即可。 ∎

結合 2.1 和 2.2：3n² + 7n + 2 = Θ(n²)。

---

### 範例 2.3：反證 n³ ≠ O(n²)

**目標：** 證明不存在 c, n₀ 使得 n³ ≤ cn² 對所有 n ≥ n₀ 成立。

**反證法：** 假設存在 c > 0, n₀ > 0 使得對所有 n ≥ n₀：n³ ≤ cn²。

兩邊除以 n²（n ≥ 1 時合法）：n ≤ c。

這表示 n 被常數 c 限制住了，但 n 可以取到任意大，取 n = ⌈c⌉ + 1 > c，矛盾。

因此 n³ ≠ O(n²)。 ∎

---

### 範例 2.4（經典考古題）：If f(n) = O(g(n)), then 2^{f(n)} = O(2^{g(n)})?

**答案：False!**

**反例：** 取 f(n) = 2n，g(n) = n。

顯然 2n = O(n)（取 c = 2 即可）。

但 2^{f(n)} = 2^{2n} = 4^n，而 2^{g(n)} = 2^n。

若 4^n = O(2^n)，則存在 c, n₀ 使得 4^n ≤ c · 2^n，也就是 (4/2)^n = 2^n ≤ c。

但 2^n 可以任意大，所以不可能被常數 c bound 住。矛盾！

**核心原因：** 指數函數把「常數倍差異」放大成「指數倍差異」。f(n) = 2n 跟 g(n) = n 只差一個常數倍，但 2^{2n} 跟 2^n 差了指數倍。

**教訓：** Big-O 不能直接「搬進指數」裡面！

---

### 範例 2.5（經典考古題）：If |f(n) - g(n)| = O(1), then 2^{f(n)} = O(2^{g(n)})?

**答案：True!**

**推導：**

|f(n) - g(n)| = O(1) 意思是：存在常數 d > 0，使得 |f(n) - g(n)| ≤ d 對所有夠大的 n。

因此 f(n) - g(n) ≤ d，也就是 f(n) ≤ g(n) + d。

所以：
$$
2^{f(n)} \leq 2^{g(n) + d} = 2^d \cdot 2^{g(n)}
$$

取 c = 2^d（這是一個正常數），就得到 2^{f(n)} ≤ c · 2^{g(n)}。

因此 2^{f(n)} = O(2^{g(n)})。 ∎

**兩題的對比：** 只有當兩個函數差一個「常數」（而非「常數倍」）時，才能安全地搬進指數裡。

---

### 範例 2.6：証明 log(n!) = Θ(n log n)

**上界 O(n log n)：**

$n! = 1 \cdot 2 \cdot 3 \cdots n \leq n \cdot n \cdot n \cdots n = n^n$

所以 $\log(n!) \leq \log(n^n) = n \log n$，故 $\log(n!) = O(n \log n)$。

**下界 Ω(n log n)：**

$n! = 1 \cdot 2 \cdots n \geq (n/2)^{n/2}$（後半的 n/2 個數字每個都 ≥ n/2）

所以 $\log(n!) \geq \frac{n}{2} \log \frac{n}{2} = \frac{n}{2}(\log n - 1) = \Omega(n \log n)$。

合起來：$\log(n!) = \Theta(n \log n)$。 ∎

---

## 3. Master Theorem 完整教學

### 3.1 基本形式

Master Theorem 適用於以下形式的遞迴式：

$$
T(n) = a \cdot T\!\left(\frac{n}{b}\right) + f(n)
$$

其中 a ≥ 1, b > 1 為常數，f(n) 為漸近正函數。

**關鍵值：** $n^{\log_b a}$（我們把它叫做「分水嶺函數」watershed function）。

---

### 3.2 用遞迴樹直覺理解三個 Case

先畫遞迴樹：

```
層級 0:           f(n)                    → 工作量 f(n)
               /  |  \
層級 1:    f(n/b) ... f(n/b)   (a 個)     → 工作量 a · f(n/b)
            / | \     / | \
層級 2:   .....................  (a² 個)   → 工作量 a² · f(n/b²)
            ⋮
層級 k:   (aᵏ 個節點，問題大小 n/bᵏ)      → 工作量 aᵏ · f(n/bᵏ)
            ⋮
層級 log_b(n): (a^{log_b n} = n^{log_b a} 個葉子)  → 工作量 Θ(n^{log_b a})
```

**樹的高度：** $\log_b n$

**葉子數量：** $a^{\log_b n} = n^{\log_b a}$（這是一個恆等式，推導：$a^{\log_b n} = a^{\frac{\ln n}{\ln b}} = n^{\frac{\ln a}{\ln b}} = n^{\log_b a}$）

**總工作量 =** 所有層級的工作量之和：

$$
T(n) = \sum_{k=0}^{\log_b n} a^k \cdot f\!\left(\frac{n}{b^k}\right) + \Theta(n^{\log_b a})
$$

（最後一項是葉子的工作量。）

現在問題變成：**這個和被誰主導？**

想像你把每層的工作量列出來，看它是遞增、遞減、還是持平：

- **Case 1（葉子主導）：** 每層工作量越往下越多，最後一層（葉子）的工作量最大，佔了總量的大部分。此時 $T(n) = \Theta(n^{\log_b a})$。

- **Case 2（平均分攤）：** 每層工作量差不多，總共 $\log_b n$ 層，所以乘上層數。此時 $T(n) = \Theta(n^{\log_b a} \log n)$。

- **Case 3（根主導）：** 每層工作量越往上越多，第一層（根）的工作量最大。此時 $T(n) = \Theta(f(n))$。

---

### 3.3 三個 Case 的精確陳述

令 $c_{\text{crit}} = \log_b a$（critical exponent）。

#### Case 1：f(n) 比 $n^{c_{\text{crit}}}$ 多項式地慢

若 $f(n) = O(n^{c_{\text{crit}} - \epsilon})$，其中 $\epsilon > 0$ 是某個常數，則：

$$
T(n) = \Theta(n^{c_{\text{crit}}}) = \Theta(n^{\log_b a})
$$

**白話：** 如果 f(n) 遠比 $n^{\log_b a}$ 小（差一個多項式因子），那麼葉子的工作量佔主導。

#### Case 2：f(n) 跟 $n^{c_{\text{crit}}}$ 同級

若 $f(n) = \Theta(n^{c_{\text{crit}}})$，也就是 $f(n) = \Theta(n^{\log_b a})$，則：

$$
T(n) = \Theta(n^{\log_b a} \cdot \log n)
$$

**白話：** 如果 f(n) 跟 $n^{\log_b a}$ 一樣大，那每層工作量差不多，乘上層數 $\log n$。

#### Case 3：f(n) 比 $n^{c_{\text{crit}}}$ 多項式地快

若 $f(n) = \Omega(n^{c_{\text{crit}} + \epsilon})$，其中 $\epsilon > 0$，**而且** $a \cdot f(n/b) \leq c \cdot f(n)$ 對某個 $c < 1$（正則條件 regularity condition），則：

$$
T(n) = \Theta(f(n))
$$

**白話：** 如果 f(n) 遠比 $n^{\log_b a}$ 大（差一個多項式因子），而且滿足正則條件，那根的工作量佔主導。

**為什麼 Case 3 需要正則條件？** 因為我們不只要 f(n) 長得快，還要它「行為正常」——具體來說，遞迴拆出的子問題工作量 a·f(n/b) 確實比 f(n) 小一個常數比例。大部分正常的函數（多項式、n log n 等）都自動滿足這個條件。

---

### 3.4 Extended Case 2（常考！）

如果 $f(n) = \Theta(n^{\log_b a} \cdot (\log n)^k)$，其中 $k \geq 0$，則：

$$
T(n) = \Theta(n^{\log_b a} \cdot (\log n)^{k+1})
$$

**這是 Case 2 的推廣版。** 原本的 Case 2 就是 k = 0 的特例。

**直覺：** 每層的工作量是 $\Theta(n^{\log_b a} \cdot (\log n)^k)$ 的某個版本，加上 $\log_b n$ 層，積分起來就多了一個 $\log$ 因子。

**範例：** $T(n) = 2T(n/2) + n\log n$

這裡 a = 2, b = 2，$n^{\log_b a} = n^1 = n$。而 f(n) = n log n = $n \cdot (\log n)^1$，所以 k = 1。

$$
T(n) = \Theta(n \cdot (\log n)^2)
$$

---

### 3.5 Master Theorem 手把手教學範例

> **給零基礎同學的使用步驟**：遇到 $T(n) = aT(n/b) + f(n)$ 的遞迴式時，照著以下步驟做：
>
> 1. **辨識 a, b, f(n)**：a 是遞迴呼叫幾次、b 是問題每次縮小幾倍、f(n) 是遞迴以外的工作量
> 2. **算分水嶺**：計算 $n^{\log_b a}$
> 3. **比較 f(n) 和分水嶺**：看 f(n) 比分水嶺小、一樣大、還是大
> 4. **套用對應的 Case**
>
> **完整數值代入範例**：$T(n) = 2T(n/2) + n$
>
> | 步驟 | 操作 | 結果 |
> |------|------|------|
> | 1. 辨識參數 | 遞迴呼叫 2 次，問題縮小 2 倍，額外工作 n | $a=2, b=2, f(n)=n$ |
> | 2. 算分水嶺 | $n^{\log_b a} = n^{\log_2 2} = n^1 = n$ | 分水嶺 = $n$ |
> | 3. 比較 | $f(n) = n$ 跟分水嶺 $n$ **一樣大** | $f(n) = \Theta(n^{\log_b a})$ |
> | 4. 套用 Case 2 | 每層工作量差不多，乘以層數 | $T(n) = \Theta(n \log n)$ |
>
> 這就是 Merge Sort 的時間複雜度！

### 3.6 Master Theorem 的使用範例

#### 範例 3.6.1：T(n) = 9T(n/3) + n

- a = 9, b = 3
- $n^{\log_b a} = n^{\log_3 9} = n^2$
- f(n) = n
- 比較：$n = O(n^{2-1}) = O(n^1)$，是 Case 1（$\epsilon = 1$）
- **答：** $T(n) = \Theta(n^2)$

#### 範例 3.6.2：T(n) = T(2n/3) + 1

- a = 1, b = 3/2
- $n^{\log_b a} = n^{\log_{3/2} 1} = n^0 = 1$
- f(n) = 1
- 比較：$f(n) = \Theta(1) = \Theta(n^{\log_b a})$，是 Case 2
- **答：** $T(n) = \Theta(\log n)$

#### 範例 3.6.3：T(n) = 3T(n/4) + n log n

- a = 3, b = 4
- $n^{\log_b a} = n^{\log_4 3} \approx n^{0.793}$
- f(n) = n log n
- 比較：$n \log n = \Omega(n^{0.793 + \epsilon})$，取 $\epsilon \approx 0.2$，是 Case 3
- 正則條件：$3 \cdot (n/4)\log(n/4) = \frac{3}{4} n \log(n/4) \leq \frac{3}{4} n \log n = \frac{3}{4} f(n)$，取 $c = 3/4 < 1$ ✓
- **答：** $T(n) = \Theta(n \log n)$

#### 範例 3.6.4：T(n) = 2T(n/2) + n log n

- a = 2, b = 2
- $n^{\log_b a} = n^1 = n$
- f(n) = n log n = $\Theta(n \cdot (\log n)^1)$
- 這是 Extended Case 2，k = 1
- **答：** $T(n) = \Theta(n (\log n)^2)$

---

### 3.6 Master Theorem 什麼時候不能用？

**情況 1：f(n) 落在 Case 1 和 Case 2 之間的「間隙」**

例：$T(n) = 2T(n/2) + \frac{n}{\log n}$

- $n^{\log_b a} = n$
- $f(n) = n / \log n$
- 要用 Case 1，需要 $f(n) = O(n^{1-\epsilon})$，但 $n/\log n$ 不是 $O(n^{1-\epsilon})$ 對任何 $\epsilon > 0$（因為 $n/\log n$ 只比 n 小一個 log 因子，不是多項式因子）。
- 要用 Case 2，需要 $f(n) = \Theta(n)$，但 $n/\log n \neq \Theta(n)$。

→ **Master Theorem 不適用。** 要用其他方法（如遞迴樹或 Akra-Bazzi）。

**情況 2：a < 1 或 b ≤ 1**

Master Theorem 要求 a ≥ 1, b > 1。

**情況 3：子問題大小不一致**

例：$T(n) = T(n/3) + T(2n/3) + n$

兩個子問題大小不同，不是 $T(n) = aT(n/b) + f(n)$ 的形式。

**情況 4：非多項式差距但不滿足正則條件（罕見）**

---

## 4. 遞迴樹法

### 4.1 基本步驟

1. **展開遞迴式** ─ 把 T(n) 寫成一棵樹
2. **計算每層的工作量**
3. **計算樹的高度（層數）**
4. **加總所有層** ─ 通常會得到一個幾何級數或等差級數
5. **化簡** ─ 得到漸近結果

### 4.2 遞迴樹的小規模具體範例：T(n) = 2T(n/2) + n，n = 8

> **給初學者**：遞迴樹就是「把遞迴一層一層展開，看每層做多少工作」。我們用 n = 8 來實際算。

```
層 0:                    8                        工作量 = 8
                       /   \
層 1:                 4     4                      工作量 = 4 + 4 = 8
                    / \   / \
層 2:              2   2 2   2                     工作量 = 2+2+2+2 = 8
                  /\ /\ /\ /\
層 3 (base):     1 1 1 1 1 1 1 1                  工作量 = 8 個 base case
```

| 層級 | 節點數 | 每個節點工作量 | 該層總工作量 |
|------|--------|---------------|-------------|
| 0 | 1 | 8 | 8 |
| 1 | 2 | 4 | 8 |
| 2 | 4 | 2 | 8 |
| 3 (base) | 8 | 1 | 8 |
| **合計** | | | **8 + 8 + 8 + 8 = 32** |

樹的高度 = $\log_2 8 = 3$ 層（加上 base case 共 4 層）。

每層工作量都是 8 = n，共 $\log_2 n + 1$ 層，所以總工作量 $\approx n \times (\log_2 n + 1) = \Theta(n \log n)$。

和 Master Theorem 的結果一致！

---

### 4.3 範例 1：T(n) = 3T(n/4) + cn²

**Step 1：畫出遞迴樹**

```
層 0:                     cn²
                       /   |   \
層 1:           c(n/4)²  c(n/4)²  c(n/4)²
               / | \     / | \    / | \
層 2:       c(n/16)² ... (共 9 個)
                ⋮
```

**Step 2：每層的工作量**

- 層 0：$cn^2$（1 個節點）
- 層 1：$3 \cdot c(n/4)^2 = 3 \cdot cn^2/16 = \frac{3}{16} cn^2$
- 層 2：$9 \cdot c(n/16)^2 = 9 \cdot cn^2/256 = \frac{9}{256} cn^2 = \left(\frac{3}{16}\right)^2 cn^2$
- 層 k：$\left(\frac{3}{16}\right)^k cn^2$

**Step 3：樹的高度**

問題大小每次除以 4，到 1 時：$n/4^h = 1 \Rightarrow h = \log_4 n$。

**Step 4：加總**

$$
T(n) = cn^2 \sum_{k=0}^{\log_4 n} \left(\frac{3}{16}\right)^k + \Theta(n^{\log_4 3})
$$

（最後一項是葉子層的貢獻：$3^{\log_4 n} = n^{\log_4 3}$ 個葉子。）

幾何級數的比值 $r = 3/16 < 1$，所以無窮級數收斂：

$$
\sum_{k=0}^{\infty} \left(\frac{3}{16}\right)^k = \frac{1}{1 - 3/16} = \frac{16}{13}
$$

因此：

$$
T(n) = \Theta(cn^2 \cdot \frac{16}{13}) + \Theta(n^{\log_4 3}) = \Theta(n^2)
$$

（因為 $n^{\log_4 3} \approx n^{0.793} = o(n^2)$，被 $n^2$ 主導。）

**答：** $T(n) = \Theta(n^2)$。

---

### 4.3 範例 2：T(n) = T(n/3) + T(2n/3) + cn

這是 Master Theorem 不能用的情況（子問題大小不一致）。

**Step 1：畫出遞迴樹**

```
層 0:                    cn
                       /     \
層 1:           c(n/3)      c(2n/3)
               /   \        /    \
層 2:     c(n/9) c(2n/9) c(2n/9) c(4n/9)
```

**Step 2：每層的工作量**

- 層 0：$cn$
- 層 1：$c(n/3) + c(2n/3) = cn$
- 層 2：$c(n/9) + c(2n/9) + c(2n/9) + c(4n/9) = cn$

**發現：每層的工作量都是 cn！**

**Step 3：樹的高度**

最短路徑（一直走 n/3）：$\log_3 n$
最長路徑（一直走 2n/3）：$\log_{3/2} n$

所以樹不是完全平衡的，高度介於 $\log_3 n$ 和 $\log_{3/2} n$ 之間。

但由於每層完整的話工作量都是 cn，我們可以得到：

$$
T(n) \geq cn \cdot \log_3 n = \Omega(n \log n)
$$
$$
T(n) \leq cn \cdot \log_{3/2} n = O(n \log n)
$$

**答：** $T(n) = \Theta(n \log n)$。

---

## 5. 代入法 (Substitution Method)

### 5.1 基本步驟

1. **猜測**答案（通常先用遞迴樹或 Master Theorem 猜一個形式）
2. **用數學歸納法驗證**猜測
3. **找到適當的常數 c**（和可能的低階修正項）

### 5.2 範例 1：T(n) = 2T(n/2) + n

**Step 1：猜測** T(n) = O(n log n)，也就是猜 T(n) ≤ cn log n 對某個 c > 0。

**Step 2：歸納假設**

假設對所有 m < n，$T(m) \leq cm \log m$。特別是 $T(n/2) \leq c(n/2)\log(n/2)$。

**Step 3：代入遞迴式**

$$
T(n) = 2T(n/2) + n \leq 2 \cdot c\frac{n}{2}\log\frac{n}{2} + n = cn\log\frac{n}{2} + n
$$
$$
= cn(\log n - \log 2) + n = cn\log n - cn\log 2 + n = cn\log n - cn + n
$$

（這裡我們用 $\log_2$，所以 $\log 2 = 1$。）

$$
= cn\log n + n(1 - c)
$$

要讓這 $\leq cn\log n$，需要 $n(1-c) \leq 0$，也就是 $c \geq 1$。

取 c = 1（或任何 ≥ 1 的常數），歸納成立。

**Base case：** T(1) = Θ(1) ≤ c · 1 · log 1 = 0？這有問題！log 1 = 0！

**修正：** 我們把 base case 設在 n = 2（或更大），然後選 c 夠大使得 T(2) ≤ c·2·log 2 = 2c。只要 c 夠大就可以搞定。

**答：** $T(n) = O(n \log n)$。 ∎

---

### 5.3 範例 2（需要減低階項）：T(n) = T(n/2) + T(n/4) + n

**Step 1：猜測** $T(n) = O(n)$，也就是猜 $T(n) \leq cn$。

**Step 2：代入**

$$
T(n) = T(n/2) + T(n/4) + n \leq c\frac{n}{2} + c\frac{n}{4} + n = \frac{3cn}{4} + n = n\left(\frac{3c}{4} + 1\right)
$$

要讓這 $\leq cn$，需要 $\frac{3c}{4} + 1 \leq c$，也就是 $1 \leq \frac{c}{4}$，$c \geq 4$。

取 c = 4，$T(n) \leq 4n$。歸納成立。 ✓

**等等！** 這個例子其實直接就成功了。讓我示範一個「真正需要減低階項」的例子。

---

### 5.4 範例 3（真正需要減低階項）：T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + 1

**Step 1：猜測** $T(n) = O(n)$，也就是猜 $T(n) \leq cn$。

**Step 2：代入**（為簡化先忽略上下取整）

$$
T(n) = T(n/2) + T(n/2) + 1 \leq cn/2 + cn/2 + 1 = cn + 1
$$

我們得到 $T(n) \leq cn + 1$，但目標是 $T(n) \leq cn$。多了一個 +1，歸納**失敗**！

**Step 3：修正猜測 ─ 減低階項**

改猜 $T(n) \leq cn - d$，其中 d 是某個常數。

$$
T(n) \leq c(n/2) - d + c(n/2) - d + 1 = cn - 2d + 1
$$

要讓這 $\leq cn - d$，需要 $-2d + 1 \leq -d$，也就是 $d \geq 1$。

取 d = 1，得到 $T(n) \leq cn - 1$，歸納成立！

**教訓：** 當直接猜 $cn$ 歸納差一個常數不夠的時候，減一個低階項 $-d$ 可以「吸收」掉多出來的常數。這是代入法最重要的技巧之一。

---

### 5.5 代入法的常見陷阱

**陷阱 1：猜太鬆**

T(n) = 2T(n/2) + n，如果你猜 T(n) = O(n²)，歸納當然能成功，但你得到的是一個不夠緊的上界。要盡量猜到最緊的 bound。

**陷阱 2：忘記驗 base case**

歸納法一定要驗 base case！有時候 base case 會讓你的常數 c 需要更大。

**陷阱 3：多了低階項卻以為成功了**

「$T(n) \leq cn + 1$，差不多就是 cn 嘛！」——不行！數學歸納法要**精確**，差一點都不行。這時候就要用減低階項的技巧。

**陷阱 4：不當使用漸近記號**

不能寫 $T(n) \leq cn\log n + O(n)$，然後說「O(n) 反正比 n log n 小所以不管它」。歸納法的每一步都必須嚴謹。

---

## 6. 特殊遞迴式

### 6.1 變數替換法：T(n) = T(√n) + c

**這個遞迴式的特色：** 子問題大小不是除以常數 b，而是開根號。

**技巧：令 m = log₂ n**（也就是 n = 2^m）

則 $\sqrt{n} = 2^{m/2}$，令 $S(m) = T(2^m) = T(n)$。

代入遞迴式：
$$
S(m) = T(2^m) = T(\sqrt{2^m}) + c = T(2^{m/2}) + c = S(m/2) + c
$$

現在 $S(m) = S(m/2) + c$ 是我們熟悉的形式！

用 Master Theorem：a=1, b=2, f(m) = c = Θ(1) = Θ(m^0)。

$m^{\log_2 1} = m^0 = 1$，$f(m) = \Theta(1)$，Case 2。

$$S(m) = \Theta(\log m)$$

代回 m = log n：

$$T(n) = S(\log n) = \Theta(\log \log n)$$

**答：** $T(n) = \Theta(\log \log n)$。

---

### 6.2 T(n) = √n · T(√n) + n

**Step 1：令 m = log₂ n，S(m) = T(2^m)。**

$T(n) = \sqrt{n} \cdot T(\sqrt{n}) + n$

$T(2^m) = 2^{m/2} \cdot T(2^{m/2}) + 2^m$

$S(m) = 2^{m/2} \cdot S(m/2) + 2^m$

**Step 2：兩邊除以 $2^m$，令 $R(m) = S(m)/2^m$。**

$$
R(m) = \frac{S(m)}{2^m} = \frac{2^{m/2} \cdot S(m/2) + 2^m}{2^m} = \frac{S(m/2)}{2^{m/2}} + 1 = R(m/2) + 1
$$

所以 $R(m) = R(m/2) + 1$，這是跟上面一樣的遞迴！

$R(m) = \Theta(\log m)$

因此：
$$
S(m) = 2^m \cdot R(m) = 2^m \cdot \Theta(\log m)
$$

代回 n：
$$
T(n) = n \cdot \Theta(\log \log n)
$$

**答：** $T(n) = \Theta(n \log \log n)$。

---

### 6.3 T(n) = T(n/2) + T(n/4) + n

這個遞迴式有不同大小的子問題，Master Theorem 不能直接用。

**方法 1：代入法**

猜 $T(n) = \Theta(n)$，猜 $T(n) \leq cn$。

$T(n) = T(n/2) + T(n/4) + n \leq cn/2 + cn/4 + n = (3c/4 + 1)n$

要 $(3c/4 + 1)n \leq cn$，即 $3c/4 + 1 \leq c$，$c \geq 4$。

取 c = 4，歸納成立。✓

猜 $T(n) \geq dn$。

$T(n) = T(n/2) + T(n/4) + n \geq dn/2 + dn/4 + n = (3d/4 + 1)n$

要 $(3d/4 + 1)n \geq dn$，即 $3d/4 + 1 \geq d$，$d \leq 4$。

取 d = 4（或任何 ≤ 4 的正數），歸納成立。✓

**答：** $T(n) = \Theta(n)$。

**方法 2：遞迴樹（驗證直覺）**

```
層 0:               n
               /       \
層 1:       n/2        n/4         → 工作量 n/2 + n/4 = 3n/4
           /   \      /   \
層 2:   n/4  n/8   n/8  n/16      → 工作量 n/4 + n/8 + n/8 + n/16 = 9n/16 = (3/4)²n
```

每層的工作量是前一層的 3/4，形成比值 3/4 的遞減幾何級數。

$$
T(n) = n \sum_{k=0}^{\infty} (3/4)^k = n \cdot \frac{1}{1-3/4} = 4n = \Theta(n)
$$

---

### 6.4 總結：遇到遞迴式怎麼辦？

```
遞迴式 T(n) = ...
    │
    ├── 形如 aT(n/b) + f(n)？
    │       → 試 Master Theorem
    │       → 如果落在 gap 裡，用遞迴樹或 Akra-Bazzi
    │
    ├── 子問題大小不一致？（如 T(n/2) + T(n/4)）
    │       → 遞迴樹 + 代入法驗證
    │
    ├── 子問題大小是 √n？
    │       → 變數替換 m = log n
    │
    └── 其他奇怪的遞迴？
            → 遞迴樹先猜，然後代入法驗證
```

---

## 附錄：常用公式速查

### 幾何級數
$$\sum_{k=0}^{n} r^k = \frac{r^{n+1}-1}{r-1} \quad (r \neq 1)$$

- r < 1：$\sum_{k=0}^{\infty} r^k = \frac{1}{1-r}$
- r > 1：$\sum_{k=0}^{n} r^k = \Theta(r^n)$（最後一項主導）
- r = 1：$\sum_{k=0}^{n} 1 = n+1$

### 調和級數
$$\sum_{k=1}^{n} \frac{1}{k} = \ln n + O(1) = \Theta(\log n)$$

### 對數恆等式
- $a^{\log_b c} = c^{\log_b a}$（超常用！）
- $\log_b a = \frac{\log a}{\log b}$
- $a^{\log_b n} = n^{\log_b a}$

### Stirling 近似
$$n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n$$
$$\log(n!) = \Theta(n \log n)$$

---

## 自我檢測題

完成本章後，試著回答以下問題來確認自己的理解程度。

### 觀念題

1. **用自己的話解釋**：Big-O、Big-Omega、Big-Theta 之間的差別是什麼？各自代表「上界」「下界」還是「精確等級」？

2. **判斷對錯**：以下各敘述是 True 還是 False？
   - (a) $5n^2 + 3n = O(n^2)$
   - (b) $5n^2 + 3n = O(n^3)$
   - (c) $5n^2 + 3n = \Theta(n^3)$
   - (d) $n \log n = O(n^2)$
   - (e) $2^{n+1} = O(2^n)$

3. **排序**：把以下函數從成長最慢到最快排列：$n^2$、$\log n$、$2^n$、$n \log n$、$n$、$1$

### 計算題

4. **證明練習**：用 Big-O 的定義證明 $7n + 12 = O(n)$。（提示：找到具體的 $c$ 和 $n_0$）

5. **Master Theorem 練習**：用 Master Theorem 解以下遞迴式：
   - (a) $T(n) = 4T(n/2) + n$
   - (b) $T(n) = 2T(n/4) + \sqrt{n}$
   - (c) $T(n) = T(n/2) + 1$

6. **遞迴樹練習**：畫出 $T(n) = 2T(n/2) + n^2$ 在 n = 8 時的遞迴樹，算出每層的工作量，並求出 $T(n)$ 的漸近結果。

7. **代入法練習**：用代入法驗證 $T(n) = 2T(n/2) + n$ 的解為 $T(n) = O(n \log n)$。（提示：猜 $T(n) \leq cn\log n$，然後代入遞迴式做歸納）

### 參考答案提示

- 第 2 題：(a) True (b) True (c) False (d) True (e) True（因為 $2^{n+1} = 2 \cdot 2^n$，取 $c = 2$ 即可）
- 第 3 題：$1 \prec \log n \prec n \prec n\log n \prec n^2 \prec 2^n$
- 第 5(a) 題：$a=4, b=2, n^{\log_2 4} = n^2$，$f(n) = n = O(n^{2-1})$，Case 1，$T(n) = \Theta(n^2)$
- 第 5(c) 題：$a=1, b=2, n^{\log_2 1} = n^0 = 1$，$f(n) = 1 = \Theta(1)$，Case 2，$T(n) = \Theta(\log n)$
