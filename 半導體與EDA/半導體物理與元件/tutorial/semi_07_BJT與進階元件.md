# 第七章：BJT 與進階元件

> **學習目標**：深入理解 BJT 的元件物理（電流增益的推導），並掌握 SOI、FinFET、GAA 等先進元件結構。
> **預備知識**：第五章（PN 接面）、第六章（MOSFET 基礎）
> **預估時間**：4～5 小時

---

## 🔰 本章基礎觀念（零基礎必讀）

### BJT 與 MOSFET 的差異

| 特性 | BJT | MOSFET |
|------|-----|--------|
| 全名 | Bipolar Junction Transistor | Metal-Oxide-Semiconductor FET |
| 控制方式 | 電流控制（基極電流IB） | 電壓控制（閘極電壓VGS） |
| 載子類型 | 雙極性（電子+電洞都參與） | 單極性（只有一種載子） |
| 輸入阻抗 | 低（基極有電流） | 極高（閘極絕緣） |
| 跨導 gm | 高（gm = IC/VT） | 較低 |
| 主要應用 | 類比放大器、RF、功率 | 數位邏輯、記憶體 |

### 一分鐘抓住核心

```
NPN BJT 結構：

  Emitter    Base    Collector
   n⁺    │  p  │     n
  ──────┤──────┤──────────
  重摻雜  薄+輕   輕摻雜

工作原理：
1. BE 接面正偏 → 電子從 E 注入 B
2. B 區很薄 → 大部分電子穿越 B 到達 C
3. BC 接面反偏 → 電子被 C 收集
4. 結果：IC ≈ IE，IB 很小 → β = IC/IB >> 1
```

---

## 一、BJT 元件物理（深入版）

### 1.1 少數載子在各區域的分佈

在正常主動模式（Normal Active Mode：BE 正偏，BC 反偏）：

```
載子濃度 (少數載子)
     ↑
     │  np(0)
     │  ╱╲
     │ ╱  ╲        pn(0)
     │╱    ╲      ╱
  np0│      ╲    ╱
     │       ╲  ╱
  ───│────────╲╱───────── 平衡值
     │  E(n⁺)  B(p)    C(n)
     └──────────────────→ x
         │←WB→│

E區（射極）：少數電洞 pE 從 BE 接面注入
B區（基極）：少數電子 nB 線性下降（薄基極近似）
C區（集極）：少數電洞被反偏接面掃走
```

### 1.2 基極中的少數載子分佈

在薄基極（WB << Ln）近似下，B 區的少數電子濃度近似線性分佈：

$$n_p(x) = n_{p0}\left[\exp\left(\frac{V_{BE}}{V_T}\right)\left(1 - \frac{x}{W_B}\right) + \frac{x}{W_B}\right]$$

斜率決定了擴散電流（即集極電流 IC）。

### 1.3 射極注入效率（Emitter Injection Efficiency, γ）

$$\gamma = \frac{J_{nE}}{J_{nE} + J_{pE}} = \frac{1}{1 + \frac{D_p N_{aB} W_B}{D_n N_{dE} L_p}}$$

**白話**：從射極注入基極的電子電流，佔總 BE 接面電流的比例。

要讓 γ → 1：
- **NdE >> NaB**：射極重摻雜（所以射極用 n⁺）
- **WB 薄**
- **Dn 大**

### 1.4 基極傳輸因子（Base Transport Factor, αT）

$$\alpha_T = \frac{I_{Cn}}{I_{En}} = 1 - \frac{W_B^2}{2L_n^2} \approx 1 - \frac{1}{2}\left(\frac{W_B}{L_n}\right)^2$$

**白話**：注入基極的電子中，有多少能成功穿越基極到達集極？

要讓 αT → 1：
- **WB << Ln**：基極必須很薄（遠小於擴散長度）

### 1.5 電流增益

**共基極電流增益**：

$$\alpha = \gamma \cdot \alpha_T$$

$$I_C = \alpha I_E$$

**共射極電流增益**：

$$\beta = \frac{\alpha}{1 - \alpha} = \frac{I_C}{I_B}$$

由於 α 接近 1（典型 0.99），β 很大（典型 100~300）。

**範例**：如果 γ = 0.998，αT = 0.995
- α = 0.998 × 0.995 = 0.993
- β = 0.993 / (1 - 0.993) = 0.993 / 0.007 = 142

### 1.6 Gummel Number

Gummel Number 是影響 β 的關鍵物理量：

$$G_B = \int_0^{W_B} \frac{p(x)}{D_n(x)} dx \approx \frac{N_{aB} W_B}{D_n} \quad \text{（均勻摻雜近似）}$$

$$\beta \approx \frac{G_E}{G_B}$$

其中 GE 是射極的 Gummel Number。

**設計原則**：要讓 β 大，必須讓基極的 Gummel Number 小 → 基極薄 + 輕摻雜。

### 1.7 集極電流與 Gummel Plot

$$I_C = \frac{qA D_n n_i^2}{G_B}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right]$$

**Gummel Plot**：在 log(IC) 和 log(IB) vs VBE 圖中：

```
log(I) ↑
       │      ╱╱  IC
       │     ╱╱
       │    ╱╱   ← 理想斜率 = q/kT (n=1)
       │   ╱╱
       │  ╱╱    IB
       │ ╱╱
       │╱╱   ← 低VBE時IB斜率 = q/2kT (n=2, 復合)
       └───────────→ VBE
```

IC 和 IB 之間的距離就是 β。

---

## 二、BJT 的非理想效應

### 2.1 Early 效應（Early Effect）

隨著 VCE 增加，BC 空乏區變寬，有效基極寬度 WB 變窄 → IC 微增。

$$I_C = I_{C0}\left(1 + \frac{V_{CE}}{V_A}\right)$$

VA 是 **Early 電壓**（通常 50~200V），可從 IC-VCE 曲線的外推交點求得。

```
IC ↑
   │     ╱─── IB3
   │    ╱╱─── IB2
   │   ╱╱╱─── IB1
   │  ╱╱╱
   │ ╱╱╱
   ╱╱╱
──╱─┼──────────→ VCE
-VA  0
```

### 2.2 Kirk 效應（Base Pushout / Kirk Effect）

在大電流操作下：

1. 集極中注入的電子濃度 > Nd（集極摻雜）
2. 集極的淨電荷從正變負
3. BC 空乏區向集極推移
4. 等效基極寬度 WB 增加
5. β 急劇下降

$$J_{Kirk} = qN_d v_{sat}$$

Kirk 效應限制了 BJT 的最大工作電流。

### 2.3 高頻特性：fT

截止頻率（Unity Gain Frequency）：

$$f_T = \frac{g_m}{2\pi(C_\pi + C_\mu)} \approx \frac{1}{2\pi \tau_{EC}}$$

$$\tau_{EC} = \tau_E + \tau_B + \tau_C + \tau_{RC}$$

基極渡越時間：τB = WB²/(2Dn)

WB 越薄、Dn 越大 → fT 越高。

---

## 三、SOI MOSFET（矽絕緣體上）

### 3.1 結構

```
     Gate
   ┌──────┐
   │ Oxide│
═══╪══════╪═══ ← Si 薄膜（通道）
n⁺ │      │ n⁺
───┴──────┴───
   Buried Oxide (BOX)  ← 埋入氧化層
═══════════════
   Si Substrate (Handle wafer)
```

### 3.2 SOI 的優勢

| 優勢 | 原因 |
|------|------|
| 無 Latch-up | SOI 隔離消除了寄生 PNPN |
| 接面電容小 | S/D 和基板之間有 BOX 隔離 |
| 短通道控制好 | 薄 Si 薄膜限制了電場穿透 |
| 軟錯誤抗性 | BOX 擋住基板的電荷收集 |

### 3.3 全空乏 SOI（FD-SOI）vs 部分空乏 SOI（PD-SOI）

- **FD-SOI**：Si 薄膜很薄（< ~10nm），整個通道被空乏 → 無浮體效應 → 現代製程主流（如 GlobalFoundries 22FDX）
- **PD-SOI**：Si 薄膜較厚，中性區存在 → 有浮體效應（kink effect）→ 較少使用

### 3.4 FD-SOI 的獨特優勢

- **背閘極偏壓（Back-gate Bias）**：可以透過基板電壓調整 Vth，不需要額外製程步驟
- 這種「體偏壓」（Body Bias）可以動態調整：高效能模式降低 Vth，低功耗模式提高 Vth

---

## 四、FinFET

### 4.1 為什麼需要 FinFET？

從 22nm 節點開始，平面 MOSFET 的短通道效應已經難以控制（DIBL、Vth roll-off 太嚴重）。FinFET 用**3D 結構**解決了這個問題。

### 4.2 結構

```
          Gate Gate
           │   │
     ┌─────┤   ├─────┐
     │     │   │     │
     │ Gate│Fin│Gate │  ← 閘極從三面包覆 Fin
     │     │   │     │
     └─────┤   ├─────┘
           │   │
    ═══════╧═══╧═══════ ← Oxide/BOX
         Substrate

俯視圖：
     G─────G
     │ Fin │  Hfin = Fin 高度
     │     │  Wfin = Fin 寬度
     G─────G
     （三面閘極包覆）
```

### 4.3 有效通道寬度

$$W_{eff} = 2 \times H_{fin} + W_{fin}$$

其中：
- Hfin：Fin 的高度（通常 ~40-50nm）
- Wfin：Fin 的寬度（通常 ~5-7nm）

如果 Hfin = 42nm，Wfin = 7nm：
Weff = 2×42 + 7 = **91 nm**（每個 Fin）

### 4.4 量化效應

FinFET 的 Weff 只能是**整數個 Fin** 的倍數，無法連續調整：

| Fin 數量 | Weff (nm) | 說明 |
|---------|----------|------|
| 1 | 91 | 最小寬度 |
| 2 | 182 | |
| 3 | 273 | |
| N | N × 91 | 只能是整數倍 |

這與平面 MOSFET 的連續 W 不同，對類比電路設計是一個挑戰。

### 4.5 FinFET 的優勢

1. **優異的閘極控制**：三面包覆 → DIBL < 50 mV/V
2. **更好的 SS**：接近 60 mV/dec
3. **更高的 ION/IOFF**
4. **更小的面積**：利用垂直方向增加 Weff

### 4.6 各代 FinFET 比較

| 公司 | 節點 | Fin Pitch (nm) | Hfin (nm) | Wfin (nm) |
|------|------|---------------|-----------|-----------|
| Intel | 22nm | 60 | 34 | 8 |
| TSMC | 16nm | 48 | 37 | 7 |
| TSMC | 7nm | 30 | 42 | 6 |
| TSMC | 5nm | 25-30 | 48 | 5 |

---

## 五、GAA / Nanosheet

### 5.1 為什麼從 FinFET 到 GAA？

FinFET 的 Fin 寬度持續縮小，但低於 ~5nm 時會遇到：
- 量子侷限效應嚴重
- 載子遷移率急劇下降
- 製程困難

**GAA（Gate-All-Around）**：閘極從**四面**完全包覆通道。

### 5.2 Nanosheet 結構

```
     ┌────────────────────┐
     │       Gate         │
     ├────────────────────┤
     │  ┌──────────────┐  │
     │  │   Nanosheet  │  │  ← Si 通道薄片
     │  │   (channel)  │  │     Wsheet × Tsheet
     │  └──────────────┘  │
     │       Gate         │
     ├────────────────────┤
     │  ┌──────────────┐  │
     │  │   Nanosheet  │  │  ← 可以堆疊多層
     │  └──────────────┘  │
     │       Gate         │
     ├────────────────────┤
     │  ┌──────────────┐  │
     │  │   Nanosheet  │  │
     │  └──────────────┘  │
     │       Gate         │
     └────────────────────┘
```

### 5.3 Nanosheet 的優勢

1. **四面閘極包覆** → 比 FinFET 更好的短通道控制
2. **Weff 可以透過調整 Nanosheet 寬度**連續調整 → 解決 FinFET 的量化問題
3. **可以堆疊多層** → 增加驅動力
4. **靈活性**：寬 sheet 給大電流，窄 sheet 給小漏電

### 5.4 從 FinFET 到 GAA 的演進

```
Planar MOSFET  →  FinFET      →  GAA/Nanosheet  →  CFET
(~45nm)           (22nm~)        (3nm~)            (future)

  ═══════           ║             ═══
  │Gate│           ║║║            │G│
  ═══════          ║║║            ═══
  一面控制         三面控制        四面控制         NMOS+PMOS
                                                堆疊
```

### 5.5 CFET（Complementary FET）

未來的方向：將 NMOS 和 PMOS **垂直堆疊**，大幅縮小 CMOS 面積。

```
     ┌──────────┐
     │  PMOS    │  ← 上層
     ├──────────┤
     │  NMOS    │  ← 下層
     └──────────┘

面積縮小約 50%！但製程極其複雜。
```

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|---------|------|
| 射極注入效率 | Emitter Injection Efficiency (γ) | 射極電流中電子佔的比例 | γ → 1 需要 NdE >> NaB |
| 基極傳輸因子 | Base Transport Factor (αT) | 穿越基極的電子比例 | αT ≈ 1 - WB²/2Ln² |
| 共基極增益 | Common-Base Gain (α) | IC/IE = γ·αT | α ≈ 0.99 |
| 共射極增益 | Common-Emitter Gain (β) | IC/IB = α/(1-α) | β ≈ 100~300 |
| Gummel Number | Gummel Number | 基極摻雜的積分量 | GB = NaB·WB/Dn |
| Early效應 | Early Effect | VCE↑→WB↓→IC↑ | VA: Early 電壓 |
| Kirk效應 | Kirk Effect / Base Pushout | 大電流下基極有效變寬 | β 急降 |
| SOI | Silicon-On-Insulator | 矽薄膜在氧化層上 | FD-SOI, PD-SOI |
| FinFET | Fin Field-Effect Transistor | 鰭式3D電晶體 | 22nm~5nm 主流 |
| Weff | Effective Channel Width | 有效通道寬度 | 2Hfin + Wfin |
| GAA | Gate-All-Around | 閘極四面包覆 | 3nm 及以下 |
| Nanosheet | Nanosheet | 薄片狀通道 | GAA的一種形式 |
| CFET | Complementary FET | NMOS+PMOS垂直堆疊 | 未來技術 |
| fT | Unity Gain Frequency | 電流增益為1的頻率 | fT ∝ 1/WB² |
| 浮體效應 | Floating Body Effect | SOI中body電位浮動 | PD-SOI的問題 |

---

## 數值例題

### 【例題 1】BJT 電流增益計算

**題目**：NPN BJT，NdE = 10¹⁹ cm⁻³，NaB = 10¹⁷ cm⁻³，WB = 0.5 μm。Dn(B) = 20 cm²/s，Dp(E) = 5 cm²/s，Ln = 50 μm，Lp = 5 μm。求 γ、αT 和 β。

**解答**：

```
步驟 1：射極注入效率 γ
γ = 1 / (1 + Dp·NaB·WB / (Dn·NdE·Lp))
  = 1 / (1 + 5×10¹⁷×0.5×10⁻⁴ / (20×10¹⁹×5×10⁻⁴))
  = 1 / (1 + 2.5×10¹³ / 10¹⁶)
  = 1 / (1 + 0.0025)
  = 1 / 1.0025
  = 0.9975

步驟 2：基極傳輸因子 αT
αT = 1 - WB²/(2Ln²)
   = 1 - (0.5×10⁻⁴)²/(2×(50×10⁻⁴)²)
   = 1 - 2.5×10⁻⁹/(2×2.5×10⁻⁵)
   = 1 - 2.5×10⁻⁹/5×10⁻⁵
   = 1 - 5×10⁻⁵
   = 0.99995

步驟 3：α 和 β
α = γ × αT = 0.9975 × 0.99995 = 0.9975

β = α/(1-α) = 0.9975/0.0025 = 399

答案：β ≈ 400
```

**觀察**：αT 幾乎等於 1（WB << Ln），所以 β 主要由 γ 決定（射極注入效率）。

---

### 【例題 2】Early 效應

**題目**：BJT 在 VCE = 2V 時 IC = 1 mA，VA = 100V。求 VCE = 5V 時的 IC 和輸出電阻 ro。

**解答**：

```
IC(VCE=2V) = IC0(1 + 2/100) → IC0 = 1/(1.02) = 0.980 mA

IC(VCE=5V) = 0.980 × (1 + 5/100) = 0.980 × 1.05 = 1.029 mA

輸出電阻：
ro = VA/IC ≈ 100/10⁻³ = 100 kΩ

（更精確：ro = (VA + VCE)/IC = 102/10⁻³ = 102 kΩ）
```

---

### 【例題 3】FinFET 的 Weff 計算

**題目**：TSMC 5nm FinFET，Hfin = 48 nm，Wfin = 5 nm。一個 NMOS 元件使用 4 個 Fin。求 Weff。如果需要 Weff ≈ 500nm，最少需要幾個 Fin？

**解答**：

```
每個 Fin 的 Weff = 2×Hfin + Wfin = 2×48 + 5 = 101 nm

4 個 Fin：Weff = 4 × 101 = 404 nm

需要 Weff ≈ 500nm：
N = 500/101 = 4.95 → 需要 5 個 Fin

5 Fin 的 Weff = 5 × 101 = 505 nm ✓

注意：不能用 4.95 個 Fin！只能是整數。
如果需要精確的 500nm，FinFET 做不到。
但 Nanosheet 可以（調整 sheet 寬度）。
```

---

### 【例題 4】Kirk 效應的臨界電流

**題目**：NPN BJT，Nd(C) = 10¹⁶ cm⁻³，vsat = 10⁷ cm/s，A = 10⁻⁶ cm²。求 Kirk 效應的臨界電流密度和臨界電流。

**解答**：

```
JKirk = qNd·vsat
      = 1.6×10⁻¹⁹ × 10¹⁶ × 10⁷
      = 1.6×10⁴ A/cm²
      = 16 kA/cm²

IKirk = JKirk × A = 1.6×10⁴ × 10⁻⁶
      = 1.6×10⁻² A = 16 mA

當 IC > 16 mA 時，Kirk 效應開始顯著，β 急劇下降。
```

---

## 題型鑑別

| 看到什麼關鍵字 | 用什麼方法 | 對應公式 |
|--------------|----------|---------|
| β、電流增益 | γ × αT | β = α/(1-α) |
| 射極注入效率 | γ 公式 | 需要 NdE >> NaB |
| 基極寬度、穿越 | αT 公式 | αT ≈ 1 - WB²/2Ln² |
| VCE↑、IC微增 | Early效應 | IC = IC0(1+VCE/VA) |
| 大電流、β下降 | Kirk效應 | JKirk = qNd·vsat |
| FinFET、Weff | 計算公式 | Weff = 2Hfin + Wfin |
| Fin數量 | 取整數 | 只能整數個Fin |
| SOI、浮體 | FD vs PD | FD-SOI消除浮體效應 |
| GAA、Nanosheet | 閘極控制力比較 | 四面 > 三面 > 一面 |

---

## ✅ 自我檢測

### 基礎題

**Q1**：BJT 的 β 高需要什麼條件？

<details>
<summary>點擊查看答案</summary>

β 高需要 α → 1，即 γ 和 αT 都要接近 1：

1. **γ → 1**：射極注入效率高
   - NdE >> NaB（射極重摻雜，基極輕摻雜）
2. **αT → 1**：基極傳輸因子高
   - WB << Ln（基極寬度遠小於擴散長度）

簡言之：**射極重、基極薄且輕**。

</details>

**Q2**：FinFET 的有效通道寬度怎麼算？為什麼 Weff 只能是離散值？

<details>
<summary>點擊查看答案</summary>

Weff = 2×Hfin + Wfin（每個 Fin 的三面展開寬度）

由於 FinFET 的 Fin 是固定尺寸的 3D 結構，只能以整數個 Fin 為單位增加寬度。你不能做「半個 Fin」。

所以 Weff 只能是：1×91nm, 2×91nm, 3×91nm, ... （假設每 Fin 91nm）

這對類比電路設計是個挑戰，因為類比電路常需要精確的寬度比。

</details>

**Q3**：什麼是 Early 效應？它怎麼影響電路？

<details>
<summary>點擊查看答案</summary>

Early 效應：VCE 增加 → BC 空乏區變寬 → 有效基極寬度 WB 減小 → IC 微增。

IC = IC0(1 + VCE/VA)

電路影響：
- 理想 BJT 在飽和區 IC 應不隨 VCE 變化 → 無窮大輸出電阻
- Early 效應使輸出電阻有限：ro = VA/IC
- 這限制了放大器的電壓增益：Av = -gm × ro

VA 越大（典型 50~200V），元件越接近理想。

</details>

### 進階題

**Q4**：GAA/Nanosheet 相比 FinFET 的技術優勢有哪些？

<details>
<summary>點擊查看答案</summary>

1. **閘極控制力更強**：四面包覆 vs 三面包覆 → SS 更接近理想，DIBL 更小
2. **通道寬度可連續調整**：調整 nanosheet 的寬度即可，不受 Fin 量化限制
3. **更好的 ION/IOFF**
4. **可以堆疊多層** sheet 增加驅動力
5. **在極小節點（2nm 以下）仍可繼續縮放**

挑戰：
- 製程複雜度大幅增加（inner spacer、selective etch）
- 寄生電容控制困難
- sheet 之間的間距需要精確控制

</details>

**Q5**：比較平面 MOSFET、FinFET、GAA、CFET 的閘極控制力和面積效率。

<details>
<summary>點擊查看答案</summary>

| 結構 | 閘極包覆面數 | 閘極控制力 | 面積效率 | 製程世代 |
|------|------------|----------|---------|---------|
| Planar | 1 面 | 最弱 | 低 | ~45nm 以上 |
| FinFET | 3 面 | 強 | 中 | 22nm~5nm |
| GAA/Nanosheet | 4 面 | 最強 | 中高 | 3nm~ |
| CFET | 4 面 + 堆疊 | 最強 | 最高 | 未來 |

趨勢：從一維（平面）→ 二維（FinFET 垂直 Fin）→ 三維（GAA 堆疊 + CFET N/P 堆疊）

每一代的目標都是在更小面積內放更多電晶體，同時維持良好的電氣特性。

</details>

---

## 本章重點整理

```
1. BJT：γ = 射極注入效率，αT = 基極傳輸因子
2. α = γ·αT ≈ 0.99，β = α/(1-α) ≈ 100~300
3. β高的條件：NdE >> NaB（射極重），WB << Ln（基極薄）
4. Gummel Number GB = NaB·WB/Dn，β ≈ GE/GB
5. Early效應：VCE↑→IC↑，ro = VA/IC
6. Kirk效應：大電流→WB有效增加→β急降
7. SOI：埋入氧化層隔離，FD-SOI消除浮體效應
8. FinFET：Weff = 2Hfin + Wfin，三面閘極，22nm~5nm主流
9. FinFET量化：Weff只能是整數個Fin的倍數
10. GAA/Nanosheet：四面閘極，3nm及以下
11. CFET：N/P堆疊，面積縮小50%，是未來方向
```

---

> **下一章預告**：[第八章 光電與功率元件](semi_08_光電與功率元件.md) —— 探索太陽能電池、LED、雷射、光偵測器和功率元件的物理原理。
