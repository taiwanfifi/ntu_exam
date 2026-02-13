# 信號與系統 第四章：傅立葉轉換

---

## 🔰 本章基礎觀念（零基礎必讀）

### 從傅立葉級數到傅立葉轉換

上一章我們學了**傅立葉級數**：把**週期信號**拆成離散頻率的諧波。

但現實中很多信號不是週期的——一個語音詞句、一個短脈衝、一張照片的掃描線。這些非週期信號怎麼做頻率分析？

核心想法：

> **把非週期信號當成「週期趨向無限大」的週期信號。**

當 T → ∞：
- 基本頻率 ω₀ = 2π/T → 0（頻率間隔趨近於零）
- 離散頻率 kω₀ → 連續頻率 ω
- 求和 Σ → 積分 ∫
- 傅立葉係數 aₖ → 連續的頻譜密度函數 X(jω)

> **傅立葉轉換就是傅立葉級數的「連續頻率版本」。**

### 傅立葉轉換告訴我們什麼？

X(jω) 是一個**複數函數**，它告訴你：
- |X(jω)|：頻率 ω 的分量**有多強**（振幅譜）
- ∠X(jω)：頻率 ω 的分量**相位是多少**（相位譜）

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 傅立葉轉換 | Fourier Transform (FT) | 把時域信號轉到頻域的工具 | x(t) → X(jω) |
| 反傅立葉轉換 | Inverse FT | 把頻域轉回時域 | X(jω) → x(t) |
| 頻譜 | Spectrum | 信號的頻率組成 | |
| sinc 函數 | sinc function | sin(πx)/(πx) | 矩形脈衝的頻譜 |
| 頻率響應 | Frequency response H(jω) | LTI 系統對不同頻率的增益和相移 | 等化器的頻率曲線 |
| 卷積定理 | Convolution theorem | 時域卷積 ↔ 頻域相乘 | 最重要的性質之一 |
| 對偶性 | Duality | 時域頻域的對稱關係 | |
| 低通濾波器 | Low-pass filter (LPF) | 只讓低頻通過的系統 | 音響的 Bass 旋鈕 |
| 高通濾波器 | High-pass filter (HPF) | 只讓高頻通過的系統 | 去除直流偏移 |
| 帶通濾波器 | Band-pass filter (BPF) | 只讓某頻段通過的系統 | 收音機選台 |
| 帶寬 | Bandwidth | 信號或系統佔據的頻率範圍 | |

---

## 一、連續時間傅立葉轉換（CTFT）

### 1.1 正轉換（Forward Transform）

$$X(j\omega) = \int_{-\infty}^{\infty} x(t) \, e^{-j\omega t} \, dt$$

記號：x(t) ↔ X(jω)，或 X(jω) = F{x(t)}

### 1.2 反轉換（Inverse Transform）

$$x(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} X(j\omega) \, e^{j\omega t} \, d\omega$$

> 正轉換和反轉換的差異：指數的正負號不同，反轉換多了 1/(2π) 的係數。

### 1.3 存在條件

x(t) 的傅立葉轉換存在的充分條件：

$$\int_{-\infty}^{\infty} |x(t)| \, dt < \infty$$

> 有些信號（如 u(t)、cos(t)）不滿足此條件，但可以用**廣義傅立葉轉換**（含 δ 函數）來處理。

---

## 二、常見傅立葉轉換對

### 2.1 矩形脈衝 ↔ sinc 函數

$$\text{rect}(t/\tau) = \begin{cases} 1, & |t| < \tau/2 \\ 0, & |t| > \tau/2 \end{cases}$$

$$\text{rect}(t/\tau) \longleftrightarrow \tau \cdot \text{sinc}\left(\frac{\omega\tau}{2\pi}\right) = \tau \cdot \frac{\sin(\omega\tau/2)}{\omega\tau/2}$$

> **白話**：越窄的脈衝（時域越短），頻譜越寬（包含的頻率越多）。

### 數值例題 2.1：矩形脈衝的頻譜

> **問題**：x(t) 是寬度為 2、高度為 1 的矩形脈衝（在 [-1, 1] 為 1），求 X(jω)。

**解答**：

$$X(j\omega) = \int_{-1}^{1} e^{-j\omega t} dt = \left[\frac{e^{-j\omega t}}{-j\omega}\right]_{-1}^{1}$$

$$= \frac{e^{-j\omega} - e^{j\omega}}{-j\omega} = \frac{-2j\sin(\omega)}{-j\omega} = \frac{2\sin(\omega)}{\omega}$$

**答：X(jω) = 2sin(ω)/ω = 2sinc(ω/π)**

驗證：在 ω = 0 時，X(0) = 2（等於矩形面積）✓

### 2.2 三角脈衝 ↔ sinc² 函數

$$\Lambda(t/\tau) \longleftrightarrow \tau \cdot \text{sinc}^2\left(\frac{\omega\tau}{2\pi}\right)$$

> 三角脈衝比矩形「平滑」，所以頻譜衰減更快（sinc² 比 sinc 衰減快）。

### 2.3 高斯脈衝 ↔ 高斯

$$e^{-at^2} \longleftrightarrow \sqrt{\frac{\pi}{a}} \, e^{-\omega^2/(4a)}$$

> **高斯函數的傅立葉轉換還是高斯！** 這是唯一一個「自身是自身轉換」的函數形狀。

### 2.4 脈衝函數

$$\delta(t) \longleftrightarrow 1$$

> δ(t) 包含**所有頻率**，且各頻率等量。（一記瞬間的打擊激發所有頻率。）

$$1 \longleftrightarrow 2\pi\delta(\omega)$$

> 常數（直流信號）只有零頻率分量。

### 2.5 複指數 / 正弦

$$e^{j\omega_0 t} \longleftrightarrow 2\pi\delta(\omega - \omega_0)$$

$$\cos(\omega_0 t) \longleftrightarrow \pi[\delta(\omega - \omega_0) + \delta(\omega + \omega_0)]$$

$$\sin(\omega_0 t) \longleftrightarrow \frac{\pi}{j}[\delta(\omega - \omega_0) - \delta(\omega + \omega_0)]$$

> 純正弦波的頻譜是兩根「針」，分別在 ±ω₀ 處。

### 2.6 指數衰減

$$e^{-at}u(t) \longleftrightarrow \frac{1}{a + j\omega}, \quad a > 0$$

### 2.7 雙邊指數

$$e^{-a|t|} \longleftrightarrow \frac{2a}{a^2 + \omega^2}, \quad a > 0$$

### 常見轉換對速查表

| x(t) | X(jω) | 備註 |
|-------|--------|------|
| δ(t) | 1 | 脈衝 → 全頻 |
| 1 | 2πδ(ω) | 直流 → 零頻 |
| e^(jω₀t) | 2πδ(ω-ω₀) | |
| cos(ω₀t) | π[δ(ω-ω₀)+δ(ω+ω₀)] | |
| u(t) | πδ(ω) + 1/(jω) | |
| e^(-at)u(t), a>0 | 1/(a+jω) | |
| e^(-a\|t\|), a>0 | 2a/(a²+ω²) | |
| rect(t/τ) | τ·sinc(ωτ/2π) | |
| e^(-at²) | √(π/a)·e^(-ω²/4a) | |
| sgn(t) | 2/(jω) | |

---

## 三、傅立葉轉換的重要性質

### 3.1 線性（Linearity）

$$ax_1(t) + bx_2(t) \longleftrightarrow aX_1(j\omega) + bX_2(j\omega)$$

### 3.2 時移（Time Shift）

$$x(t - t_0) \longleftrightarrow X(j\omega) \cdot e^{-j\omega t_0}$$

> **時移不改變振幅譜，只加一個線性相位。**

### 3.3 頻移（Frequency Shift / Modulation）

$$x(t) \cdot e^{j\omega_0 t} \longleftrightarrow X(j(\omega - \omega_0))$$

> 乘以複指數 = 把頻譜搬移 ω₀。這是**調變**的基礎！

### 3.4 尺度變換（Time Scaling）

$$x(at) \longleftrightarrow \frac{1}{|a|} X\left(\frac{j\omega}{a}\right)$$

> **壓縮時間 → 展開頻率，反之亦然。**
> 直覺：一個很短的脈衝需要很寬的頻帶來表達。

### 數值例題 3.1：尺度變換

> **問題**：已知 rect(t) ↔ sinc(ω/2π)，求 rect(t/4) 的傅立葉轉換。

**解答**：

rect(t/4) = rect(at)，其中 a = 1/4。

$$F\{\text{rect}(t/4)\} = \frac{1}{|1/4|} \cdot \text{sinc}\left(\frac{\omega/4}{2\pi}\right) \cdot \text{(correction needed)}$$

更直觀的方法：rect(t/4) 是寬度 4 的矩形脈衝。

$$X(j\omega) = \int_{-2}^{2} e^{-j\omega t} dt = \frac{2\sin(2\omega)}{\omega} = 4 \cdot \frac{\sin(2\omega)}{2\omega}$$

**答：X(jω) = 4·sin(2ω)/(2ω) = 4sinc(2ω/π)**

> 寬度從 1 變成 4（展開 4 倍），主瓣寬度從 2π 變成 π/2（壓縮 4 倍）。

### 3.5 時域微分

$$\frac{d}{dt}x(t) \longleftrightarrow j\omega \cdot X(j\omega)$$

> 微分 = 乘以 jω（增強高頻）。

### 3.6 時域積分

$$\int_{-\infty}^{t} x(\tau)d\tau \longleftrightarrow \frac{X(j\omega)}{j\omega} + \pi X(0)\delta(\omega)$$

### 3.7 卷積定理（最重要！）

**時域卷積 ↔ 頻域乘積**：

$$x(t) * h(t) \longleftrightarrow X(j\omega) \cdot H(j\omega)$$

**時域乘積 ↔ 頻域卷積**：

$$x(t) \cdot w(t) \longleftrightarrow \frac{1}{2\pi} X(j\omega) * W(j\omega)$$

> **卷積定理的威力**：在時域做卷積很複雜（要積分），但在頻域只是簡單的乘法！
> 這就是為什麼「轉到頻域再處理」常常更有效率。

### 數值例題 3.2：卷積定理應用

> **問題**：x(t) = e^(-t)u(t)，h(t) = e^(-2t)u(t)，用卷積定理求 y(t) = x(t)*h(t)。

**解答**：

**步驟 1：求各自的傅立葉轉換**
- X(jω) = 1/(1+jω)
- H(jω) = 1/(2+jω)

**步驟 2：頻域相乘**
$$Y(j\omega) = X(j\omega) \cdot H(j\omega) = \frac{1}{(1+j\omega)(2+j\omega)}$$

**步驟 3：部分分式展開**
$$Y(j\omega) = \frac{1}{1+j\omega} - \frac{1}{2+j\omega}$$

**步驟 4：反轉換**
$$y(t) = (e^{-t} - e^{-2t})u(t)$$

> 和第二章用時域卷積算的結果一模一樣！但頻域方法明顯更簡潔。

### 3.8 對偶性（Duality）

如果 x(t) ↔ X(jω)，那麼：

$$X(jt) \longleftrightarrow 2\pi \, x(-\omega)$$

> **白話**：把時域的函數形狀拿到頻域當頻譜，反過來也成立（差一個 2π 和反褶）。

### 數值例題 3.3：對偶性

> **問題**：已知 e^(-a|t|) ↔ 2a/(a²+ω²)，利用對偶性求 2a/(a²+t²) 的傅立葉轉換。

**解答**：

由對偶性，如果 x(t) ↔ X(jω)，則 X(jt) ↔ 2πx(-ω)。

令 x(t) = e^(-a|t|)，X(jω) = 2a/(a²+ω²)。

則 X(jt) = 2a/(a²+t²) 的傅立葉轉換為：

$$F\left\{\frac{2a}{a^2+t^2}\right\} = 2\pi \cdot e^{-a|-\omega|} = 2\pi e^{-a|\omega|}$$

### 3.9 Parseval 定理

$$\int_{-\infty}^{\infty} |x(t)|^2 \, dt = \frac{1}{2\pi} \int_{-\infty}^{\infty} |X(j\omega)|^2 \, d\omega$$

> **能量守恆**：時域算的總能量 = 頻域算的總能量。

|X(jω)|² 稱為**能量頻譜密度（Energy Spectral Density）**。

### 性質速查表

| 性質 | 時域 | 頻域 |
|------|------|------|
| 線性 | ax₁+bx₂ | aX₁+bX₂ |
| 時移 | x(t-t₀) | X(jω)e^(-jωt₀) |
| 頻移 | x(t)e^(jω₀t) | X(j(ω-ω₀)) |
| 尺度 | x(at) | (1/\|a\|)X(jω/a) |
| 微分 | dx/dt | jωX(jω) |
| 卷積 | x*h | X·H |
| 乘積 | x·w | (1/2π)(X*W) |
| 對偶 | X(jt) | 2πx(-ω) |
| 共軛 | x*(t) | X*(-jω) |

---

## 四、頻率響應

### 4.1 定義

對 LTI 系統，**頻率響應**就是脈衝響應的傅立葉轉換：

$$H(j\omega) = \int_{-\infty}^{\infty} h(t) e^{-j\omega t} dt$$

由卷積定理：

$$Y(j\omega) = H(j\omega) \cdot X(j\omega)$$

$$\Rightarrow H(j\omega) = \frac{Y(j\omega)}{X(j\omega)}$$

### 4.2 物理意義

如果輸入是 x(t) = e^(jω₀t)（複指數），那麼 LTI 系統的輸出是：

$$y(t) = H(j\omega_0) \cdot e^{j\omega_0 t}$$

> **LTI 系統對複指數只做「放大+移相」，不改變頻率！**
> 這就是為什麼複指數（正弦波）是 LTI 系統的**特徵函數（Eigenfunction）**。

- |H(jω₀)| = 增益（這個頻率被放大或衰減多少倍）
- ∠H(jω₀) = 相位偏移

### 數值例題 4.1：頻率響應計算

> **問題**：h(t) = e^(-3t)u(t)，求頻率響應，並計算輸入 x(t) = cos(2t) 的穩態輸出。

**解答**：

**步驟 1：求 H(jω)**
$$H(j\omega) = \frac{1}{3 + j\omega}$$

**步驟 2：在 ω = 2 處求值**
$$H(j2) = \frac{1}{3 + j2} = \frac{3-j2}{9+4} = \frac{3-j2}{13}$$

$$|H(j2)| = \frac{1}{\sqrt{9+4}} = \frac{1}{\sqrt{13}} \approx 0.277$$

$$\angle H(j2) = -\arctan(2/3) \approx -33.7°$$

**步驟 3：輸出**
$$y(t) = |H(j2)| \cdot \cos(2t + \angle H(j2)) = \frac{1}{\sqrt{13}} \cos(2t - 33.7°)$$

> cos 的振幅從 1 變成 1/√13 ≈ 0.277，相位落後約 33.7°。

---

## 五、理想濾波器

### 5.1 理想低通濾波器（Ideal LPF）

$$H(j\omega) = \begin{cases} 1, & |\omega| < \omega_c \\ 0, & |\omega| > \omega_c \end{cases}$$

只讓頻率低於 ωc（截止頻率）的分量通過。

脈衝響應：h(t) = (ωc/π) sinc(ωct/π)

> **注意**：理想低通的 h(t) 是 sinc 函數，在 t < 0 也有值 → **非因果**！
> 所以理想低通濾波器在物理上**不可實現**。

### 5.2 理想高通濾波器（Ideal HPF）

$$H_{HP}(j\omega) = 1 - H_{LP}(j\omega)$$

讓高頻通過，擋住低頻。

### 5.3 理想帶通濾波器（Ideal BPF）

$$H(j\omega) = \begin{cases} 1, & \omega_1 < |\omega| < \omega_2 \\ 0, & \text{otherwise} \end{cases}$$

只讓 [ω₁, ω₂] 頻段通過。

### 數值例題 5.1：濾波效果

> **問題**：x(t) = 2 + 3cos(5t) + cos(20t) 通過截止頻率 ωc = 10 的理想低通濾波器，輸出是什麼？

**解答**：

分析各分量的頻率：
- 直流分量（ω=0）：2 → 通過 ✓
- cos(5t)（ω=5）：5 < 10 → 通過 ✓
- cos(20t)（ω=20）：20 > 10 → 被擋住 ✗

**答：y(t) = 2 + 3cos(5t)**

> 20 rad/s 的分量被完全濾除。

---

## 六、數值例題補充

### 數值例題 6.1：反傅立葉轉換

> **問題**：X(jω) = 2/(3+jω) + 5/(4+jω)，求 x(t)（假設 x(t) 因果）。

**解答**：

利用轉換對 e^(-at)u(t) ↔ 1/(a+jω)：

$$x(t) = 2e^{-3t}u(t) + 5e^{-4t}u(t)$$

### 數值例題 6.2：利用性質組合求解

> **問題**：求 x(t) = te^(-2t)u(t) 的傅立葉轉換。

**解答**：

已知 e^(-2t)u(t) ↔ 1/(2+jω)。

利用**時域乘以 t** 的性質：若 x(t) ↔ X(jω)，則 tx(t) ↔ j(dX/dω)。

$$F\{te^{-2t}u(t)\} = j \cdot \frac{d}{d\omega}\left[\frac{1}{2+j\omega}\right]$$

$$= j \cdot \frac{-j}{(2+j\omega)^2} = \frac{1}{(2+j\omega)^2}$$

**答：X(jω) = 1/(2+jω)²**

---

## 七、題型鑑別

| 看到什麼 | 用什麼方法 |
|----------|-----------|
| 「求 X(jω)」 | 查轉換對表 + 利用性質（時移、尺度...）|
| 「求反轉換 x(t)」 | 部分分式展開 → 查表反轉 |
| 「求 y(t)=x(t)*h(t)」 | 卷積定理：Y=X·H 再反轉 |
| 「輸入 cos(ωt) 的穩態輸出」 | 代入 H(jω)：y = \|H\|cos(ωt+∠H) |
| 「通過理想濾波器」 | 看各頻率分量是否在通帶內 |
| 「壓縮/拉伸後的頻譜」 | 尺度變換性質 |
| 「乘以 cos(ω₀t) 的頻譜」 | 頻移性質（頻譜搬移 ±ω₀）|
| 「tx(t) 的轉換」 | jdX/dω |
| 「求能量」 | Parseval：E = (1/2π)∫\|X\|²dω |

---

## ✅ 自我檢測

### 問題 1
δ(t-3) 的傅立葉轉換是什麼？

<details>
<summary>點擊查看答案</summary>

利用時移性質：δ(t) ↔ 1，所以

$$\delta(t-3) \longleftrightarrow 1 \cdot e^{-j3\omega} = e^{-j3\omega}$$

振幅譜 |X(jω)| = 1（全頻等幅），相位譜 ∠X(jω) = -3ω（線性相位）。

</details>

### 問題 2
利用卷積定理，說明為什麼理想低通濾波器的脈衝響應是 sinc 函數。

<details>
<summary>點擊查看答案</summary>

理想低通的頻率響應是矩形函數 H(jω) = rect(ω/2ωc)。

h(t) = 反傅立葉轉換{H(jω)}。

由對偶性（或直接計算）：矩形函數的反轉換是 sinc 函數。

$$h(t) = \frac{1}{2\pi}\int_{-\omega_c}^{\omega_c} e^{j\omega t} d\omega = \frac{\omega_c}{\pi} \cdot \frac{\sin(\omega_c t)}{\omega_c t} = \frac{\omega_c}{\pi}\text{sinc}(\omega_c t/\pi)$$

</details>

### 問題 3
x(t) = e^(-2|t|) 的能量是多少？用 Parseval 定理在頻域計算。

<details>
<summary>點擊查看答案</summary>

X(jω) = 4/(4+ω²)

$$E = \frac{1}{2\pi}\int_{-\infty}^{\infty} \frac{16}{(4+\omega^2)^2} d\omega$$

利用公式 ∫₋∞^∞ 1/(a²+ω²)² dω = π/(2a³)，其中 a² = 4 → a = 2：

$$E = \frac{16}{2\pi} \cdot \frac{\pi}{2 \cdot 8} = \frac{16}{2\pi} \cdot \frac{\pi}{16} = \frac{1}{2}$$

驗證（時域）：∫₋∞^∞ e^(-4|t|) dt = 2·(1/4) = 1/2 ✓

</details>

### 問題 4
如果 x(t) 是實偶函數，X(jω) 有什麼特殊性質？

<details>
<summary>點擊查看答案</summary>

- x(t) 是**實數** → X(-jω) = X*(jω)
- x(t) 是**偶函數** → X(jω) = X(-jω)（時域偶 → 頻域偶）

合併：X(jω) = X*(jω) → **X(jω) 是實數！**

而且是偶函數（實偶）。

例如：e^(-a|t|) 是實偶函數 → X(jω) = 2a/(a²+ω²) 確實是實數且偶函數 ✓

</details>

### 問題 5
x(t) = cos(10t)·e^(-t²)，這個信號的頻譜長什麼樣？（定性描述即可）

<details>
<summary>點擊查看答案</summary>

e^(-t²) 的頻譜是高斯函數（centered at ω=0）。

乘以 cos(10t) = [e^(j10t)+e^(-j10t)]/2，由頻移性質：

頻譜 = 把高斯函數搬到 ω=+10 和 ω=-10，各乘 1/2。

所以 X(jω) 是兩個高斯峰，分別在 **ω = ±10** 處。

這就是 **AM 調變** 的基本原理！

</details>

---

> **下一章預告**：傅立葉轉換有一個限制——信號必須「夠乖」（絕對可積）。但很多重要的信號（如增長的指數）不滿足此條件。**拉普拉斯轉換**將突破這個限制，成為分析連續時間系統的終極工具。
