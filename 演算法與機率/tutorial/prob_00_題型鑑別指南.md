# 機率與統計 題型鑑別指南

> **核心目的**：看到題目的瞬間，知道要用什麼分布、什麼公式、什麼方法。

---

# 第一部分：分布辨識決策樹

## 1. 離散分布：看到什麼 → 用什麼

```
題目描述                                    → 分布
─────────────────────────────────────────────────────
「n 次獨立試驗，每次成功機率 p，           → Binomial(n, p)
  問恰好 k 次成功的機率」

「重複試驗直到第一次成功」                  → Geometric(p)
  （含 memoryless property）                  P(X=k) = (1-p)^{k-1} p

「重複試驗直到第 r 次成功」                 → Negative Binomial(r, p)
                                              P(X=k) = C(k-1,r-1) p^r (1-p)^{k-r}

「一段時間/區域內事件發生次數，             → Poisson(λ)
  平均 λ 次」                                 P(X=k) = e^{-λ} λ^k / k!

「N 個中有 K 個特殊，抽 n 個               → Hypergeometric
  （不放回），問特殊的個數」                  P(X=k) = C(K,k)C(N-K,n-k)/C(N,n)

「n 個等可能結果中選一個」                  → Discrete Uniform(1,n)
                                              P(X=k) = 1/n

「X₁+X₂+...+Xₙ，各 Xᵢ 獨立 Bernoulli」   → Binomial（Bernoulli 之和）

「X₁+X₂+...+Xᵣ，各 Xᵢ 獨立 Geometric」   → Negative Binomial（Geometric 之和）
```

### 關鍵判斷點

| 問自己 | 是 → | 否 → |
|--------|-------|-------|
| 固定次數 n？ | Binomial | 等到某事發生？ |
| 等到第 1 次成功？ | Geometric | 等到第 r 次？ → NegBin |
| 抽樣放回？ | Binomial | 不放回 → Hypergeometric |
| 事件在連續時間中？ | Poisson | 離散次試驗 → Binomial |

### 易混淆：Binomial vs Poisson

| | Binomial | Poisson |
|---|---|---|
| 試驗次數 | **固定** n 次 | 不固定（觀察時間段） |
| 適用情境 | n 不太大 | n 很大, p 很小, np = λ |
| 近似關係 | — | Poisson 是 Binomial 的極限 |
| 典型題目 | "10次中5次" | "每小時平均3次，問5次的機率" |

---

## 2. 連續分布：看到什麼 → 用什麼

```
題目描述                                    → 分布
─────────────────────────────────────────────────────
「在 [a,b] 上均勻分布」                     → Uniform(a, b)
                                              f(x) = 1/(b-a)

「等待時間，memoryless」                    → Exponential(λ)
「兩次 Poisson 事件之間的時間」               f(x) = λe^{-λx}

「n 個獨立 Expo 的和」                      → Gamma(n, λ) / Erlang
「等到第 n 個 Poisson 事件」                  f(x) = λⁿxⁿ⁻¹e^{-λx}/(n-1)!

「自然界鐘形分布」                          → Normal(μ, σ²)
「大量獨立 RV 之和（CLT）」                   f(x) = (2πσ²)^{-1/2} exp(-(x-μ)²/2σ²)

「Uniform(0,1) 取 -ln」                     → Exponential(1)

「Normal² 的和」                            → Chi-squared (χ²)

「Normal/sqrt(χ²/n)」                       → t-distribution

「χ²/χ²」                                  → F-distribution
```

### 關鍵判斷：Exponential vs Geometric

| | Exponential | Geometric |
|---|---|---|
| 空間 | 連續 (x ≥ 0) | 離散 (k = 1,2,...) |
| Memoryless | ✓ P(X>s+t|X>s) = P(X>t) | ✓ P(X>m+n|X>m) = P(X>n) |
| 關聯 | 兩次 Poisson 事件的間隔 | 每次試驗的等待次數 |
| 互為對應 | 連續版的 memoryless | 離散版的 memoryless |

### 關鍵判斷：什麼時候想到 Poisson Process？

- 「事件以固定速率隨機發生」
- 「平均每小時/每天/每分鐘 λ 次」
- 看到「arrival」「occur」「event」

Poisson Process 的三寶：
1. 某時段內事件數 → **Poisson(λt)**
2. 兩事件間的間隔 → **Exponential(λ)**
3. 第 n 個事件到達時間 → **Gamma(n, λ)**

---

# 第二部分：計算方法選擇

## 1. 求機率 P(A)

```
已知條件                              → 方法
────────────────────────────────────────────
直接可以算                            → 直接計算
有條件資訊 P(A|B)                     → 全概率公式 + 貝氏定理
要把事件分解                          → P(A) = Σ P(A|Bᵢ)P(Bᵢ)
互斥事件聯集                          → P(A∪B) = P(A) + P(B)
獨立事件交集                          → P(A∩B) = P(A)·P(B)
至少一個/沒有一個                     → 補事件: P(至少1) = 1 - P(全都不)
複雜的排列組合                        → 計數法 |A|/|S|
```

### 全概率 vs 貝氏 — 什麼時候用哪個？

| 情境 | 方法 |
|------|------|
| 已知原因→結果的機率，求結果的總機率 | **全概率**：P(B) = Σ P(B|Aᵢ)P(Aᵢ) |
| 已知結果，要推原因 | **貝氏**：P(Aᵢ|B) = P(B|Aᵢ)P(Aᵢ)/P(B) |
| 題目說「已知 B 發生了，問 A 的機率」 | **貝氏定理** |
| 題目說「求 B 發生的總機率」 | **全概率公式** |

**記憶口訣**：
- 全概率 = 「因→果」的加總
- 貝氏 = 「果→因」的反推

---

## 2. 求期望值 E[X]

```
情境                                  → 方法
────────────────────────────────────────────
X 有已知分布                          → 直接查表（背公式）
X = g(Y)，Y 的分布已知                → LOTUS: E[g(Y)] = Σ g(y)·P(Y=y)
                                        或 ∫ g(y)·f_Y(y) dy

X 可以拆成指標變數之和                → 指標法: X = Σ Xᵢ, E[X] = Σ E[Xᵢ]
  （「有多少個...」類型）                （不需要獨立！線性期望值）

有 MGF M(t) 可用                      → E[X] = M'(0)

條件期望值                            → E[X] = Σ E[X|Aᵢ]·P(Aᵢ)（全期望值法則）

遞迴結構問題                          → 設 E[X] = ... 建立方程式解
```

### 指標法 (Indicator Method) — 超好用！

**適用情境**：「n 個東西中，有多少個滿足某條件？」

**做法**：令 Xᵢ = 1 if 第 i 個滿足條件，else 0。

E[X] = E[Σ Xᵢ] = Σ E[Xᵢ] = Σ P(第 i 個滿足條件)

**經典例子**：
- 隨機排列的 fixed points 數量：E = Σ 1/n = 1
- n 封信隨機放信封，期望對的數量 = 1
- Coupon collector：E[收集全部] = n·Hₙ = n(1 + 1/2 + ... + 1/n)

### 何時用 MGF？

- 要求 E[X], E[X²], E[X³]... 多個矩 → MGF 一次搞定
- 要證明分布的和 → X+Y 的 MGF = Mₓ(t)·M_Y(t)（獨立時）
- 要證明收斂到 Normal → 證明 MGF 收斂到 Normal 的 MGF

---

## 3. 求變異數 Var(X)

```
方法                                  適用情境
────────────────────────────────────────────
公式法: Var(X) = E[X²] - (E[X])²    → 最常用！先求 E[X²]
已知分布直接查表                      → 背公式
MGF: E[X²] = M''(0)                  → 用 MGF 求二階矩
條件變異數公式                        → Var(X) = E[Var(X|Y)] + Var(E[X|Y])
```

**條件變異數公式**（Eve's Law）：
$$Var(X) = E[Var(X|Y)] + Var(E[X|Y])$$
- 第一項：「給定 Y 時 X 還剩多少不確定」的平均
- 第二項：「Y 造成 X 的期望值變化」的變異數

---

## 4. 求分布 / PDF / CDF

```
已知                                  → 方法
────────────────────────────────────────────
Y = g(X)，X 的分布已知                → CDF法: F_Y(y) = P(Y ≤ y) = P(g(X) ≤ y)
                                        再微分得 f_Y(y)

Y = g(X)，g 單調                      → 變數變換法:
                                        f_Y(y) = f_X(g⁻¹(y)) · |dg⁻¹/dy|

(X,Y) 聯合 → Z = X+Y                 → 摺積: f_Z(z) = ∫ f_X(x)·f_Y(z-x) dx

已知 MGF                              → MGF 唯一對應分布（查表反推）

多變數變換                            → Jacobian 法:
                                        f_{U,V}(u,v) = f_{X,Y}(h₁,h₂) · |J|
```

### CDF 法 vs 變數變換法 — 怎麼選？

| 情境 | 推薦方法 |
|------|----------|
| g 是單調函數 | **變數變換法**（直接套公式，最快） |
| g 不單調（如 Y=X²） | **CDF 法**（分段處理） |
| 不確定 | **CDF 法**（永遠可用，最通用） |
| 多個變數同時變換 | **Jacobian 法** |
| 求和 Z = X+Y | **摺積** 或 **MGF 法** |

---

# 第三部分：分布之間的關係圖

```
Bernoulli(p)
    │
    │ 和（n個獨立的）
    ▼
Binomial(n,p) ──n大p小──→ Poisson(λ=np)
    │                           │
    │ n→∞                       │ 事件間隔
    ▼                           ▼
Normal(np, np(1-p))    Exponential(λ)
    ▲                           │
    │ CLT                       │ 和（n個獨立的）
    │                           ▼
    │                     Gamma(n, λ) / Erlang
任意 iid RV 之和 ─CLT─→ Normal

Geometric(p) ──和（r個）──→ Negative Binomial(r, p)
    │
    │ 連續版本
    ▼
Exponential(λ)

Uniform(0,1) ──(-1/λ)ln(U)──→ Exponential(λ)

Normal² ──和（n個）──→ Chi-squared(n)

Normal ÷ √(χ²/n) ──→ t-distribution(n)

χ²/m ÷ χ²/n ──→ F-distribution(m,n)
```

---

# 第四部分：常見計算套路

## 套路 1：「至少一個」問題
**P(至少一個) = 1 - P(一個都沒有)**

例：丟 10 次骰子，至少一次 6 的機率
= 1 - (5/6)¹⁰

## 套路 2：「最大值/最小值」問題
- P(max(X₁,...,Xₙ) ≤ x) = P(X₁≤x)·...·P(Xₙ≤x) = [F(x)]ⁿ
- P(min(X₁,...,Xₙ) ≤ x) = 1 - [1-F(x)]ⁿ

**應用**：n 個獨立 Expo(λ) 的最小值是 Expo(nλ)

## 套路 3：「條件 + 遞迴」問題
看到「第一步可能是 A 或 B，然後重新開始」→ 設 E[X] 列方程

例：Gambler's Ruin、Random Walk、等待特定 pattern

## 套路 4：全概率 + 遞迴公式
P(事件|起始狀態 i) = Σⱼ P(到狀態 j|i) · P(事件|起始狀態 j)

## 套路 5：MGF 辨認分布
算出 MGF → 對照已知分布的 MGF → 辨識分布

| 分布 | MGF M(t) |
|------|----------|
| Bernoulli(p) | 1-p+pe^t |
| Binomial(n,p) | (1-p+pe^t)ⁿ |
| Poisson(λ) | exp(λ(e^t-1)) |
| Geometric(p) | pe^t/(1-(1-p)e^t) |
| Exponential(λ) | λ/(λ-t) |
| Normal(μ,σ²) | exp(μt + σ²t²/2) |
| Gamma(α,λ) | (λ/(λ-t))^α |

## 套路 6：Memoryless Property 的利用
只有 Exponential（連續）和 Geometric（離散）有。

P(X > s+t | X > s) = P(X > t)

**直覺**：「已經等了 s 時間不影響未來」
**計算技巧**：看到「given X > s」，直接當做重新開始

## 套路 7：Order Statistics
n 個 iid 連續 RV，排序後第 k 小的 X_{(k)}：

$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1} [1-F(x)]^{n-k} f(x)$$

特別地，Uniform(0,1) 的第 k 個 order statistic ~ Beta(k, n-k+1)。

---

# 第五部分：考試速判流程

遇到題目時，按以下順序思考：

### Step 1: 這是什麼類型的問題？
- [ ] 求機率 → Go to 求機率方法
- [ ] 求期望值 → Go to 求期望值方法
- [ ] 求分布/PDF → Go to 求分布方法
- [ ] 證明/推導 → 用定義或已知性質
- [ ] 統計推論 → MLE / MoM / CI / Hypothesis test

### Step 2: 涉及什麼分布？
- [ ] 題目明確告知 → 直接用
- [ ] 需要辨認 → 用第一部分的決策樹
- [ ] 是已知分布的函數 → 需要做變數變換

### Step 3: 有沒有特殊結構可利用？
- [ ] 獨立 → 乘法、MGF 相乘
- [ ] Memoryless → 條件化簡
- [ ] 對稱性 → 直接得答案
- [ ] 指標函數分解 → 線性期望值

### Step 4: 多步驟/複合問題怎麼拆？
- [ ] 先求中間量 → 再組合
- [ ] 全概率展開 → 分案討論
- [ ] 條件期望/變異數 → Eve's Law

---

# 第六部分：常見易錯點

1. **Poisson 近似要求**：n 大、p 小、np ≈ λ。不是所有 Binomial 都能用 Poisson！

2. **CDF 法的邊界**：P(Y ≤ y) 中要注意 y 的範圍，不同區間可能有不同表達式。

3. **獨立 ≠ 不相關**：不相關（Cov=0）不等於獨立。但**聯合 Normal** 時不相關 ⟹ 獨立。

4. **條件 PDF**：f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y)。注意分母是 **marginal PDF**，不是機率。

5. **CLT 的使用**：需要 n 夠大。標準化：Z = (X̄ - μ)/(σ/√n)。記得是 **σ/√n** 不是 σ。

6. **MLE vs MoM**：MLE 取 likelihood 微分 = 0；MoM 令樣本矩 = 理論矩。MLE 通常更有效率但可能更難算。

7. **Geometric 的定義差異**：
   - 「等到成功的試驗數」(含成功那次)：P(X=k) = (1-p)^{k-1}·p，E[X] = 1/p
   - 「成功前失敗的次數」：P(Y=k) = (1-p)^k·p，E[Y] = (1-p)/p

   **考試時看清楚定義！**
