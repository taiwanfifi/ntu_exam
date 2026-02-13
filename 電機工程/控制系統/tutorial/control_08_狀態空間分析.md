# 控制系統（八）：狀態空間分析

## 🔰 本章基礎觀念（零基礎必讀）

> 前七章我們都用**轉移函數** G(s) 來描述系統，這是「經典控制」的方法。但轉移函數有個限制：它只能描述**一個輸入一個輸出（SISO）**的系統，而且隱藏了系統內部的資訊。**狀態空間（State Space）**是「現代控制」的語言，它用矩陣和向量來描述系統，可以處理**多輸入多輸出（MIMO）**系統，並且完整揭露系統的內部狀態。可以把轉移函數想像成只看房子的外觀，狀態空間則是看到了房子的設計藍圖。

---

## 一、狀態空間表示法

### 1.1 基本概念

- **狀態（State）**：完全描述系統在某時刻行為所需的最少變數組。知道了所有狀態變數和未來的輸入，就能完全預測未來的輸出。
- **狀態變數 x(t)**：一組描述系統內部的變數（通常選為各積分器的輸出）
- **狀態向量**：$\mathbf{x}(t) = [x_1(t), x_2(t), \ldots, x_n(t)]^T$

### 1.2 狀態方程與輸出方程

$$\boxed{\dot{\mathbf{x}}(t) = A\mathbf{x}(t) + B\mathbf{u}(t)} \quad \text{（狀態方程）}$$

$$\boxed{\mathbf{y}(t) = C\mathbf{x}(t) + D\mathbf{u}(t)} \quad \text{（輸出方程）}$$

其中：
- $\mathbf{x}(t)$：n×1 狀態向量
- $\mathbf{u}(t)$：m×1 輸入向量
- $\mathbf{y}(t)$：p×1 輸出向量
- $A$：n×n 系統矩陣（State Matrix）
- $B$：n×m 輸入矩陣（Input Matrix）
- $C$：p×n 輸出矩陣（Output Matrix）
- $D$：p×m 直接傳遞矩陣（Feedthrough Matrix，通常 D=0）

### 1.3 從微分方程到狀態空間

**n 階微分方程**：
$$y^{(n)} + a_{n-1}y^{(n-1)} + \cdots + a_1\dot{y} + a_0 y = b_0 u$$

選取狀態變數：$x_1 = y, \; x_2 = \dot{y}, \; \ldots, \; x_n = y^{(n-1)}$

$$\begin{cases}
\dot{x}_1 = x_2 \\
\dot{x}_2 = x_3 \\
\vdots \\
\dot{x}_{n-1} = x_n \\
\dot{x}_n = -a_0 x_1 - a_1 x_2 - \cdots - a_{n-1} x_n + b_0 u
\end{cases}$$

**【例題 1】二階系統轉狀態空間**

$$\ddot{y} + 3\dot{y} + 2y = 5u$$

令 $x_1 = y$，$x_2 = \dot{y}$：

$$\dot{x}_1 = x_2$$
$$\dot{x}_2 = -2x_1 - 3x_2 + 5u$$
$$y = x_1$$

矩陣形式：

$$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 5 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = 0$$

---

## 二、轉移函數與狀態空間的關係

### 2.1 從狀態空間求轉移函數

$$\boxed{G(s) = C(sI - A)^{-1}B + D}$$

**推導**：
取拉普拉斯轉換（零初始條件）：
$$sX(s) = AX(s) + BU(s) \Rightarrow X(s) = (sI-A)^{-1}BU(s)$$
$$Y(s) = CX(s) + DU(s) = [C(sI-A)^{-1}B + D]U(s)$$

**【例題 2】狀態空間轉轉移函數**

承例題 1：$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$，$B = \begin{bmatrix} 0 \\ 5 \end{bmatrix}$，$C = \begin{bmatrix} 1 & 0 \end{bmatrix}$

$$sI - A = \begin{bmatrix} s & -1 \\ 2 & s+3 \end{bmatrix}$$

$$(sI-A)^{-1} = \frac{1}{s(s+3)+2} \begin{bmatrix} s+3 & 1 \\ -2 & s \end{bmatrix} = \frac{1}{s^2+3s+2} \begin{bmatrix} s+3 & 1 \\ -2 & s \end{bmatrix}$$

$$G(s) = C(sI-A)^{-1}B = \begin{bmatrix} 1 & 0 \end{bmatrix} \frac{1}{s^2+3s+2} \begin{bmatrix} s+3 & 1 \\ -2 & s \end{bmatrix} \begin{bmatrix} 0 \\ 5 \end{bmatrix}$$

$$= \frac{1}{s^2+3s+2} \begin{bmatrix} s+3 & 1 \end{bmatrix} \begin{bmatrix} 0 \\ 5 \end{bmatrix} = \frac{5}{s^2+3s+2} = \frac{5}{(s+1)(s+2)}$$

驗算：原方程 $\ddot{y}+3\dot{y}+2y = 5u$，G(s) = 5/(s²+3s+2) ✓

### 2.2 特徵值與極點的關係

$$\det(sI - A) = 0 \quad \Leftrightarrow \quad \text{特徵方程式}$$

**A 矩陣的特徵值 = 轉移函數的極點（在最小實現時）**

例題 2：$\det(sI-A) = s^2+3s+2 = (s+1)(s+2) = 0$

特徵值：λ₁ = -1, λ₂ = -2 → 就是極點。

---

## 三、標準式

### 3.1 可控標準式（Controllable Canonical Form）

對於 $G(s) = \frac{b_{n-1}s^{n-1}+\cdots+b_1s+b_0}{s^n+a_{n-1}s^{n-1}+\cdots+a_1s+a_0}$

$$A_c = \begin{bmatrix} 0 & 1 & 0 & \cdots & 0 \\ 0 & 0 & 1 & \cdots & 0 \\ \vdots & & & \ddots & \vdots \\ 0 & 0 & 0 & \cdots & 1 \\ -a_0 & -a_1 & -a_2 & \cdots & -a_{n-1} \end{bmatrix}, \quad B_c = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}$$

$$C_c = \begin{bmatrix} b_0 & b_1 & \cdots & b_{n-1} \end{bmatrix}, \quad D = 0$$

**【例題 3】寫出可控標準式**

$G(s) = \frac{2s+3}{s^3+4s^2+5s+6}$

$a_0=6, a_1=5, a_2=4$；$b_0=3, b_1=2, b_2=0$

$$A_c = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -6 & -5 & -4 \end{bmatrix}, \quad B_c = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}, \quad C_c = \begin{bmatrix} 3 & 2 & 0 \end{bmatrix}$$

### 3.2 可觀測標準式（Observable Canonical Form）

$$A_o = A_c^T, \quad B_o = C_c^T, \quad C_o = B_c^T$$

即可控標準式的**轉置**。

承例題 3：

$$A_o = \begin{bmatrix} 0 & 0 & -6 \\ 1 & 0 & -5 \\ 0 & 1 & -4 \end{bmatrix}, \quad B_o = \begin{bmatrix} 3 \\ 2 \\ 0 \end{bmatrix}, \quad C_o = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$$

### 3.3 對角標準式（Diagonal Form / Modal Form）

當 A 有 n 個不同的特徵值 λ₁, λ₂, ..., λₙ 時：

$$A_d = \begin{bmatrix} \lambda_1 & 0 & \cdots & 0 \\ 0 & \lambda_2 & \cdots & 0 \\ \vdots & & \ddots & \vdots \\ 0 & 0 & \cdots & \lambda_n \end{bmatrix}$$

此時 $A_d = P^{-1}AP$，其中 P 是特徵向量矩陣。

---

## 四、狀態轉移矩陣

### 4.1 定義

齊次方程 $\dot{\mathbf{x}} = A\mathbf{x}$ 的解為：

$$\mathbf{x}(t) = e^{At}\mathbf{x}(0) = \Phi(t)\mathbf{x}(0)$$

$$\boxed{\Phi(t) = e^{At} \text{：狀態轉移矩陣（State Transition Matrix）}}$$

完整解（含輸入）：
$$\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^t e^{A(t-\tau)}B\mathbf{u}(\tau)d\tau$$

### 4.2 性質

- $\Phi(0) = I$（單位矩陣）
- $\Phi^{-1}(t) = \Phi(-t) = e^{-At}$
- $\Phi(t_1+t_2) = \Phi(t_1)\Phi(t_2)$

### 4.3 求法一：拉普拉斯反轉換

$$\boxed{e^{At} = \mathcal{L}^{-1}\{(sI-A)^{-1}\}}$$

**【例題 4】求狀態轉移矩陣**

$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$

$$sI - A = \begin{bmatrix} s & -1 \\ 2 & s+3 \end{bmatrix}$$

$$(sI-A)^{-1} = \frac{1}{(s+1)(s+2)} \begin{bmatrix} s+3 & 1 \\ -2 & s \end{bmatrix}$$

部分分式展開每個元素：

$(1,1)$：$\frac{s+3}{(s+1)(s+2)} = \frac{2}{s+1} - \frac{1}{s+2}$

$(1,2)$：$\frac{1}{(s+1)(s+2)} = \frac{1}{s+1} - \frac{1}{s+2}$

$(2,1)$：$\frac{-2}{(s+1)(s+2)} = \frac{-2}{s+1} + \frac{2}{s+2}$

$(2,2)$：$\frac{s}{(s+1)(s+2)} = \frac{-1}{s+1} + \frac{2}{s+2}$

$$e^{At} = \begin{bmatrix} 2e^{-t}-e^{-2t} & e^{-t}-e^{-2t} \\ -2e^{-t}+2e^{-2t} & -e^{-t}+2e^{-2t} \end{bmatrix}$$

驗算：t=0 → $\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I$ ✓

### 4.4 求法二：Cayley-Hamilton 定理

> **Cayley-Hamilton 定理**：每個方陣都滿足自己的特徵方程式。

若特徵方程為 $\lambda^2 + 3\lambda + 2 = 0$（如上例），則：

$$A^2 + 3A + 2I = 0$$

因此 $e^{At}$ 可以表示為 A 的有限多項式：

$$e^{At} = \alpha_0(t)I + \alpha_1(t)A \quad \text{（2×2 矩陣只需到 A¹）}$$

其中 $\alpha_0, \alpha_1$ 由以下方程組決定：

$$e^{\lambda_1 t} = \alpha_0 + \alpha_1 \lambda_1$$
$$e^{\lambda_2 t} = \alpha_0 + \alpha_1 \lambda_2$$

$\lambda_1=-1, \lambda_2=-2$：

$$e^{-t} = \alpha_0 - \alpha_1$$
$$e^{-2t} = \alpha_0 - 2\alpha_1$$

相減：$e^{-t}-e^{-2t} = \alpha_1$

$\alpha_0 = e^{-t} + (e^{-t}-e^{-2t}) = 2e^{-t}-e^{-2t}$

$$e^{At} = (2e^{-t}-e^{-2t})I + (e^{-t}-e^{-2t})A$$

$$= (2e^{-t}-e^{-2t})\begin{bmatrix}1&0\\0&1\end{bmatrix} + (e^{-t}-e^{-2t})\begin{bmatrix}0&1\\-2&-3\end{bmatrix}$$

$$= \begin{bmatrix} 2e^{-t}-e^{-2t} & e^{-t}-e^{-2t} \\ -2(e^{-t}-e^{-2t}) & (2e^{-t}-e^{-2t})-3(e^{-t}-e^{-2t}) \end{bmatrix}$$

$$= \begin{bmatrix} 2e^{-t}-e^{-2t} & e^{-t}-e^{-2t} \\ -2e^{-t}+2e^{-2t} & -e^{-t}+2e^{-2t} \end{bmatrix}$$

與拉普拉斯法結果一致 ✓

---

## 五、可控性（Controllability）

### 5.1 定義

系統 (A, B) 是**完全可控的（Completely Controllable）**，若對任意初始狀態 $\mathbf{x}(0)$ 和任意目標狀態，都存在一個有限時間的輸入 $\mathbf{u}(t)$ 能將系統從 $\mathbf{x}(0)$ 驅動到目標狀態。

### 5.2 可控性矩陣

$$\boxed{\mathcal{C} = \begin{bmatrix} B & AB & A^2B & \cdots & A^{n-1}B \end{bmatrix}}$$

$$\text{完全可控} \Leftrightarrow \text{rank}(\mathcal{C}) = n$$

**【例題 5】判斷可控性**

$A = \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix}, \quad B = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$

$$AB = \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$

$$\mathcal{C} = \begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix}$$

$\text{rank}(\mathcal{C}) = 1 \neq 2$ → **不完全可控**

直覺：狀態 $x_2$ 的方程是 $\dot{x}_2 = 2x_2$，不受輸入 u 影響 → 無法控制 $x_2$。

**【例題 6】可控系統**

$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

$$AB = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}\begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \\ -3 \end{bmatrix}$$

$$\mathcal{C} = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$$

$\det(\mathcal{C}) = 0\times(-3) - 1\times1 = -1 \neq 0$ → rank = 2 → **完全可控** ✓

---

## 六、可觀測性（Observability）

### 6.1 定義

系統 (A, C) 是**完全可觀測的（Completely Observable）**，若由輸出 $\mathbf{y}(t)$ 和輸入 $\mathbf{u}(t)$ 在有限時間內能唯一確定初始狀態 $\mathbf{x}(0)$。

### 6.2 可觀測性矩陣

$$\boxed{\mathcal{O} = \begin{bmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{bmatrix}}$$

$$\text{完全可觀測} \Leftrightarrow \text{rank}(\mathcal{O}) = n$$

**【例題 7】判斷可觀測性**

$A = \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}$

$$CA = \begin{bmatrix} 1 & 0 \end{bmatrix}\begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 1 & 1 \end{bmatrix}$$

$$\mathcal{O} = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$$

$\det(\mathcal{O}) = 1 \neq 0$ → rank = 2 → **完全可觀測** ✓

> 有趣的對比：同一個 A 和 B=[[1],[0]]，系統不可控但可觀測。同一個 A 和 C=[1, 0]，系統可觀測但不可控。可控性和可觀測性是**獨立的概念**！

### 6.3 對偶性

系統 (A, B, C) 的可控性 ⟺ 對偶系統 $(A^T, C^T, B^T)$ 的可觀測性

---

## 七、狀態回授與極點配置

### 7.1 狀態回授

假設所有狀態都可量測，使用控制律：

$$\mathbf{u} = -K\mathbf{x} + r$$

其中 K 是 1×n 的增益向量，r 是參考輸入。

閉迴路：$\dot{\mathbf{x}} = (A-BK)\mathbf{x} + Br$

閉迴路的特徵值 = $A - BK$ 的特徵值。

### 7.2 極點配置定理

> **若且唯若系統 (A, B) 完全可控，則可以通過狀態回授 u = -Kx 將閉迴路極點配置在任意位置。**

### 7.3 設計步驟（Ackermann 公式）

1. 確定期望的特徵方程：$\alpha_d(s) = (s-s_1)(s-s_2)\cdots(s-s_n) = s^n + \hat{a}_{n-1}s^{n-1}+\cdots+\hat{a}_0$
2. 計算 $\alpha_d(A) = A^n + \hat{a}_{n-1}A^{n-1}+\cdots+\hat{a}_0 I$
3. Ackermann 公式：

$$K = \begin{bmatrix} 0 & 0 & \cdots & 0 & 1 \end{bmatrix} \mathcal{C}^{-1} \alpha_d(A)$$

**【例題 8】極點配置**

$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

期望極點：s = -5, -5（雙重極點）

期望特徵方程：$(s+5)^2 = s^2+10s+25$

**方法一（直接比較法）**：
$$\det(sI - (A-BK)) = \det\begin{bmatrix} s & -1 \\ 2+k_1 & s+3+k_2 \end{bmatrix}$$
$$= s(s+3+k_2) + (2+k_1) = s^2 + (3+k_2)s + (2+k_1)$$

比較：
- $3+k_2 = 10 \Rightarrow k_2 = 7$
- $2+k_1 = 25 \Rightarrow k_1 = 23$

$$K = \begin{bmatrix} 23 & 7 \end{bmatrix}$$

**驗算**：
$$A - BK = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix} - \begin{bmatrix} 0 \\ 1 \end{bmatrix}\begin{bmatrix} 23 & 7 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -25 & -10 \end{bmatrix}$$

特徵方程：$s^2+10s+25 = (s+5)^2 = 0$ ✓

---

## 八、觀測器（Observer）設計

### 8.1 為什麼需要觀測器？

狀態回授 u = -Kx 假設所有狀態可量測，但實際上很多狀態無法直接量測。觀測器用**已知的輸入和輸出**來**估計**狀態。

### 8.2 全狀態觀測器（Full-State Observer / Luenberger Observer）

$$\boxed{\dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + B\mathbf{u} + L(\mathbf{y} - C\hat{\mathbf{x}})}$$

其中 $\hat{\mathbf{x}}$ 是狀態估計值，$L$ 是 n×1 觀測器增益向量。

誤差 $\mathbf{e} = \mathbf{x} - \hat{\mathbf{x}}$ 滿足：

$$\dot{\mathbf{e}} = (A - LC)\mathbf{e}$$

- 若 $(A-LC)$ 的所有特徵值在 LHP → 誤差收斂到零 → 觀測器有效
- **選擇 L 使觀測器極點在期望位置**（類似極點配置！）

### 8.3 觀測器極點配置定理

> **若且唯若系統 (A, C) 完全可觀測，則可以通過選擇 L 將觀測器極點配置在任意位置。**

### 8.4 設計原則

觀測器的極點應該比控制器的極點（閉迴路極點）**快 3~5 倍**，使觀測器的估計誤差快速收斂。

**【例題 9】觀測器設計**

$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}$

期望觀測器極點：s = -20, -20

$$A - LC = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix} - \begin{bmatrix} l_1 \\ l_2 \end{bmatrix}\begin{bmatrix} 1 & 0 \end{bmatrix} = \begin{bmatrix} -l_1 & 1 \\ -2-l_2 & -3 \end{bmatrix}$$

特徵方程：
$$\det(sI-(A-LC)) = s^2 + (l_1+3)s + (3l_1+2+l_2) = (s+20)^2 = s^2+40s+400$$

比較：
- $l_1+3 = 40 \Rightarrow l_1 = 37$
- $3\times37+2+l_2 = 400 \Rightarrow l_2 = 287$

$$L = \begin{bmatrix} 37 \\ 287 \end{bmatrix}$$

### 8.5 分離定理（Separation Principle）

> 狀態回授控制器和觀測器可以**分開設計**。閉迴路系統的極點 = 控制器極點（A-BK 的特徵值）∪ 觀測器極點（A-LC 的特徵值）。

---

## 九、關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 狀態變數 | State Variable | 描述系統內部的最少變數 | 位移 x 和速度 ẋ |
| 系統矩陣 | System/State Matrix (A) | 描述系統動態的核心矩陣 | A 的特徵值=極點 |
| 狀態轉移矩陣 | State Transition Matrix | e^(At)，描述自由響應 | Φ(t) |
| 可控性 | Controllability | 輸入能否驅動所有狀態 | rank(C)=n |
| 可觀測性 | Observability | 能否從輸出推知所有狀態 | rank(O)=n |
| 可控標準式 | Controllable Canonical Form | 特定形式的 A, B, C | 最後一行是-aᵢ |
| 可觀測標準式 | Observable Canonical Form | 可控標準式的轉置 | Aₒ=Ac^T |
| 狀態回授 | State Feedback | u = -Kx + r | 極點配置 |
| 觀測器 | Observer (Luenberger) | 用 y 和 u 估計 x | 全狀態觀測器 |
| 分離定理 | Separation Principle | 控制器和觀測器可分開設計 | 極點集合=控制∪觀測 |
| 極點配置 | Pole Placement | 透過回授設定閉迴路極點 | 需要完全可控 |
| Cayley-Hamilton | Cayley-Hamilton Theorem | 矩陣滿足自己的特徵方程 | A²+3A+2I=0 |

---

## 十、題型鑑別表

| 題目特徵 | 解題方法 |
|----------|----------|
| 微分方程→狀態空間 | 選狀態變數 xᵢ = y^(i-1)，寫 A,B,C,D |
| 轉移函數→狀態空間 | 寫成可控或可觀測標準式 |
| 狀態空間→轉移函數 | G(s) = C(sI-A)⁻¹B + D |
| 求 e^(At) | 拉普拉斯反轉換 L⁻¹{(sI-A)⁻¹} 或 Cayley-Hamilton |
| 判斷可控性 | 建可控性矩陣 [B AB ... A^(n-1)B]，看 rank |
| 判斷可觀測性 | 建可觀測性矩陣 [C; CA; ...; CA^(n-1)]，看 rank |
| 極點配置設計 K | 直接比較法或 Ackermann 公式 |
| 觀測器設計 L | 類似極點配置，但用 (A-LC) |
| 求系統極點 | det(sI-A)=0 或 A 的特徵值 |
| 判斷穩定性 | A 的所有特徵值實部<0 → 穩定 |

---

## 十一、額外例題

**【例題 10】完整的狀態空間分析**

一個系統的狀態空間為：

$$A = \begin{bmatrix} -1 & 0 \\ 1 & -2 \end{bmatrix}, \quad B = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad C = \begin{bmatrix} 0 & 1 \end{bmatrix}, \quad D = 0$$

(a) 求轉移函數
(b) 判斷可控性和可觀測性
(c) 求 e^(At)

**解**：

**(a)**

$$sI-A = \begin{bmatrix} s+1 & 0 \\ -1 & s+2 \end{bmatrix}$$

$$(sI-A)^{-1} = \frac{1}{(s+1)(s+2)} \begin{bmatrix} s+2 & 0 \\ 1 & s+1 \end{bmatrix}$$

$$G(s) = C(sI-A)^{-1}B = \begin{bmatrix} 0 & 1 \end{bmatrix} \frac{1}{(s+1)(s+2)} \begin{bmatrix} s+2 & 0 \\ 1 & s+1 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$

$$= \frac{1}{(s+1)(s+2)} \begin{bmatrix} 1 & s+1 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{1}{(s+1)(s+2)}$$

**(b) 可控性**：
$$AB = \begin{bmatrix} -1 & 0 \\ 1 & -2 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

$$\mathcal{C} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}, \quad \det = 1 \neq 0 \quad \Rightarrow \text{完全可控 ✓}$$

**可觀測性**：
$$CA = \begin{bmatrix} 0 & 1 \end{bmatrix}\begin{bmatrix} -1 & 0 \\ 1 & -2 \end{bmatrix} = \begin{bmatrix} 1 & -2 \end{bmatrix}$$

$$\mathcal{O} = \begin{bmatrix} 0 & 1 \\ 1 & -2 \end{bmatrix}, \quad \det = -1 \neq 0 \quad \Rightarrow \text{完全可觀測 ✓}$$

**(c)** 因為 A 是下三角矩陣，特徵值直接是對角線元素：λ₁=-1, λ₂=-2。

$(sI-A)^{-1}$ 已在 (a) 中求出。取拉普拉斯反轉換：

$(1,1)$：$\frac{s+2}{(s+1)(s+2)} = \frac{1}{s+1}$ → $e^{-t}$

$(1,2)$：$\frac{0}{(s+1)(s+2)} = 0$ → $0$

$(2,1)$：$\frac{1}{(s+1)(s+2)} = \frac{1}{s+1}-\frac{1}{s+2}$ → $e^{-t}-e^{-2t}$

$(2,2)$：$\frac{s+1}{(s+1)(s+2)} = \frac{1}{s+2}$ → $e^{-2t}$

$$e^{At} = \begin{bmatrix} e^{-t} & 0 \\ e^{-t}-e^{-2t} & e^{-2t} \end{bmatrix}$$

驗算：$e^{A\cdot0} = \begin{bmatrix}1&0\\0&1\end{bmatrix} = I$ ✓

---

## ✅ 自我檢測

<details>
<summary><strong>Q1：狀態空間表示法相較於轉移函數的優勢是什麼？</strong></summary>

**答**：(1) 可處理多輸入多輸出（MIMO）系統；(2) 可處理非零初始條件；(3) 揭露系統內部結構（可控性、可觀測性）；(4) 容易推廣到非線性和時變系統。
</details>

<details>
<summary><strong>Q2：A 矩陣的特徵值和轉移函數的極點有什麼關係？</strong></summary>

**答**：A 的特徵值包含轉移函數的極點。但如果系統不是最小實現（有可控/可觀測的抵消），A 可能有額外的特徵值不出現在轉移函數中。在最小實現時，特徵值 = 極點。
</details>

<details>
<summary><strong>Q3：可控性矩陣的 rank < n 代表什麼物理意義？</strong></summary>

**答**：有些狀態變數不受輸入影響（無法控制）。這些「不可控」的狀態只能自由演化，無法透過輸入來改變。例如：隔離的子系統。
</details>

<details>
<summary><strong>Q4：觀測器的極點為什麼要比控制器極點快 3~5 倍？</strong></summary>

**答**：觀測器需要在控制器開始大幅動作之前就提供準確的狀態估計。如果觀測器太慢，狀態估計不準確，控制器就會根據錯誤的資訊做出不當的控制動作。
</details>

<details>
<summary><strong>Q5：系統完全可控但不完全可觀測，會有什麼問題？</strong></summary>

**答**：雖然理論上可以把極點配置在任意位置，但因為無法觀測所有狀態，就無法設計有效的觀測器，也就無法實現狀態回授控制。除非改用輸出回授或其他方法。
</details>

<details>
<summary><strong>Q6：分離定理的實際意義是什麼？</strong></summary>

**答**：你可以先獨立設計控制器增益 K（假設所有狀態可量測），再獨立設計觀測器增益 L（使狀態估計收斂），最後組合使用 u = -Kx̂。組合後的閉迴路極點就是控制器極點和觀測器極點的聯集，兩者互不影響。這大大簡化了設計流程。
</details>

---

> **本系列總結**：恭喜你完成控制系統全部八章！從建模到狀態空間，你已經掌握了自動控制的核心知識體系。接下來的學習方向可以是：數位控制（z轉換）、非線性控制（Lyapunov 穩定性）、最優控制（LQR/LQG）、或強健控制（H∞）。加油！
