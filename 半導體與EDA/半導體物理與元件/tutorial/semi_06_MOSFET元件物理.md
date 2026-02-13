# 第六章：MOSFET 元件物理

> **學習目標**：完整掌握 MOS 電容器、MOSFET I-V 特性推導、短通道效應與亞閾值特性。這是 TSMC/聯發科面試的絕對核心。
> **預備知識**：第二章（載子濃度）、第五章（PN 接面）
> **預估時間**：6～8 小時（本章是重中之重，請多花時間）

---

## 🔰 本章基礎觀念（零基礎必讀）

### MOSFET 為什麼是最重要的元件？

MOSFET（Metal-Oxide-Semiconductor Field-Effect Transistor，金氧半場效電晶體）是現代積體電路的基石。一顆先進處理器中有超過 **100 億個** MOSFET。

**MOSFET 的核心功能**：用電壓控制電流 → 開關 → 邏輯 0/1 → 所有運算

### 一分鐘抓住核心

```
MOSFET 結構：

     Gate（閘極）
   ┌──────────┐  ← 金屬閘極
   │  Oxide   │  ← 氧化層（SiO₂ 或 High-k）
═══╪══════════╪═══ ← 半導體表面
   │ Source   │ Drain    ← 源極/汲極（重摻雜）
   │  n⁺     │  n⁺      （以 NMOS 為例）
───┴──────────┴───
     p-type substrate    ← P型基板

VGS < Vth → 通道關（OFF）→ 無電流
VGS > Vth → 通道開（ON）→ 電流流動

Vth（閾值電壓）= 切換的關鍵電壓
```

---

## 一、MOS 電容器（MOS Capacitor）

### 1.1 結構

MOS 電容器是 MOSFET 的核心結構：

```
    金屬(Metal)     ← 閘極（現代用多晶矽或金屬）
    ─────────────
    氧化層(Oxide)   ← SiO₂, tox 厚度
    ─────────────
    半導體(Semiconductor) ← Si (P 型為例)
```

### 1.2 三種工作狀態（P 型基板 NMOS）

#### (a) 累積（Accumulation）：VG < VFB

閘極施加負電壓 → 吸引電洞到表面 → 表面電洞濃度增加

```
      Gate ⊖⊖⊖⊖
      ═══════════
      ⊕⊕⊕⊕⊕⊕⊕⊕⊕  ← 電洞被吸引到表面（累積）
      p-Si
```

#### (b) 空乏（Depletion）：VFB < VG < Vth

閘極施加小正電壓 → 排斥表面電洞 → 表面形成空乏區

```
      Gate ⊕⊕⊕⊕
      ═══════════
      ┌─────────┐  ← 空乏區（沒有自由載子）
      │ Na⁻ Na⁻ │
      └─────────┘
      p-Si（正常）
```

#### (c) 反轉（Inversion）：VG > Vth

閘極施加大正電壓 → 表面電子濃度超過電洞濃度 → 表面變成「N 型」

```
      Gate ⊕⊕⊕⊕⊕
      ═══════════
      ⊖⊖⊖⊖⊖⊖⊖⊖⊖  ← 反轉層（電子通道！）
      ┌─────────┐  ← 空乏區
      │ Na⁻ Na⁻ │
      └─────────┘
      p-Si（正常）
```

**關鍵概念**：反轉發生在**表面電位 φs = 2φF** 時。

其中 φF = (kT/q)·ln(Na/ni)（費米電位）

### 1.3 能帶圖分析

**平帶（Flatband）**：VG = VFB 時，能帶是平的

```
     Metal  Oxide  Semiconductor
      │      │
  Ef ─│──────│──── Ec
      │      │     Ei ── Ef 在 Ei 下方（P型）
      │      │──── Ev
```

**反轉**：VG > Vth 時

```
     Metal  Oxide  Semiconductor
      │      │         ╱── Ec
  Ef ─│──────│────── Ei
      │      │    ╱
      │      │──╱─── Ev    ← 表面 Ei 跑到 Ef 下方
                              表面 n > p → 反轉！
```

反轉條件：表面的 Ei 跑到 Ef 以下的距離 = φF → 總彎曲 = **2φF**

### 1.4 閾值電壓推導

$$V_{th} = V_{FB} + 2\phi_F + \frac{Q_{dep}}{C_{ox}}$$

各項的意義：

| 項 | 公式 | 意義 |
|---|------|------|
| VFB | φms - Qf/Cox | 讓能帶變平的電壓 |
| 2φF | 2(kT/q)ln(Na/ni) | 讓表面到達強反轉的電位 |
| Qdep/Cox | √(2qεsNa·2φF)/Cox | 支撐空乏區電荷所需的電壓 |

其中：

$$V_{FB} = \phi_{ms} - \frac{Q_f}{C_{ox}}$$

- φms = φm - φs：金屬和半導體的功函數差
- Qf：氧化層中的固定電荷（C/cm²）
- Cox = εox/tox：氧化層單位面積電容

$$Q_{dep} = -qN_a W_{dep} = -\sqrt{2q\varepsilon_s N_a \cdot 2\phi_F}$$

### 1.5 C-V 特性曲線

```
C/Cox ↑
  1.0 │══════╗                    ╔══════  ← 低頻
      │      ║                    ║
      │      ║                    ║
      │      ╚════════════════════╝
      │       ╲                  ╱
      │        ╲                ╱
  Cmin│─────────╲══════════════╱─── ← 高頻
      │
      └──────────┼──────────────→ VG
              VFB           Vth
      累積       空乏        反轉
```

- **累積**：C = Cox（氧化層電容，最大值）
- **空乏**：C = Cox·Cdep/(Cox+Cdep)（串聯電容，C 下降）
- **反轉（低頻）**：C 回到 Cox（少數載子跟得上交流信號）
- **反轉（高頻）**：C 維持在 Cmin（少數載子跟不上）

---

## 二、MOSFET I-V 特性推導

### 2.1 MOSFET 結構回顧

```
        VG
        │
   ┌────┴────┐
   │  Gate   │
   ├─────────┤ tox
===╪═════════╪===  ← 通道長度 L
n⁺ │ channel │ n⁺
Source      Drain
VS=0        VD

W = 通道寬度（垂直紙面）
L = 通道長度（Source到Drain的距離）
```

### 2.2 漸變通道近似（Gradual Channel Approximation, GCA）

假設通道中的電場主要是垂直方向（閘極控制），水平方向（S→D）的電場變化緩慢。

在通道中某一點 x（距源極的距離），通道電壓為 V(x)：

$$Q_{inv}(x) = -C_{ox}[V_{GS} - V(x) - V_{th}]$$

### 2.3 線性區（Triode Region / Linear Region）

VGS > Vth 且 VDS < VGS - Vth（通道未夾斷）：

$$I_D = \mu_n C_{ox} \frac{W}{L}\left[(V_{GS} - V_{th})V_{DS} - \frac{V_{DS}^2}{2}\right]$$

當 VDS << VGS - Vth 時，簡化為：

$$I_D \approx \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_{th})V_{DS}$$

此時 MOSFET 等效為一個電阻，阻值由 VGS 控制。

### 2.4 飽和區（Saturation Region）

VDS ≥ VGS - Vth（通道在汲極端夾斷）：

$$I_{D,sat} = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS} - V_{th})^2$$

**夾斷（Pinch-off）**：當 VDS = VGS - Vth 時，汲極端的通道電荷降為零，電流不再隨 VDS 增加。

### 2.5 通道長度調變（Channel Length Modulation, CLM）

實際上，VDS 增加時，夾斷點會向源極方向移動，有效通道長度縮短：

$$I_{D,sat} = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS} - V_{th})^2(1 + \lambda V_{DS})$$

其中 **λ = 通道長度調變參數**，L 越小 λ 越大。

### 2.6 I-V 特性圖

```
ID ↑
   │           VGS3 > VGS2 > VGS1
   │     ╱─────────────────── VGS3
   │    ╱
   │   ╱  ╱────────────────── VGS2
   │  ╱  ╱
   │ ╱  ╱  ╱─────────────── VGS1
   │╱  ╱  ╱
   │  ╱  ╱
   │ ╱  ╱
   └╱──╱──────────────────→ VDS
   0   VDS,sat = VGS - Vth
     線性區│     飽和區
```

### 2.7 跨導（Transconductance, gm）

$$g_m = \frac{\partial I_D}{\partial V_{GS}}\bigg|_{V_{DS}} = \mu_n C_{ox}\frac{W}{L}(V_{GS} - V_{th}) = \sqrt{2\mu_n C_{ox}\frac{W}{L}I_D}$$

gm 衡量閘極電壓對電流的控制能力，是類比電路設計的核心參數。

### 2.8 重要參數定義

$$\beta = \mu_n C_{ox}\frac{W}{L} \quad \text{（增益因子）}$$

$$k'_n = \mu_n C_{ox} \quad \text{（製程跨導參數，process transconductance parameter）}$$

$$C_{ox} = \frac{\varepsilon_{ox}}{t_{ox}} = \frac{3.9 \times 8.854 \times 10^{-14}}{t_{ox}} \quad \text{(F/cm²)}$$

---

## 三、短通道效應（Short Channel Effects, SCE）

### 3.1 概述

當通道長度 L 縮小到與空乏區寬度可比擬時，長通道模型的假設不再成立，出現一系列「短通道效應」。

### 3.2 Vth Roll-off

在短通道元件中，源極和汲極的 PN 接面空乏區佔據了通道下方部分的電荷。閘極不需要控制全部的空乏區電荷 → Vth 降低。

$$\Delta V_{th} \propto -\frac{x_j}{L}\sqrt{\frac{2\varepsilon_s(V_{bi}+V_{DS})}{qN_a}}$$

L 越小，Vth 下降越多。

### 3.3 DIBL（Drain-Induced Barrier Lowering）

汲極電壓增加時，汲極端的電場會「拉低」源極端的能障 → Vth 隨 VDS 增加而降低。

$$V_{th}(V_{DS}) = V_{th,long} - \eta \cdot V_{DS}$$

其中 η 是 DIBL 係數，典型值 ~20-100 mV/V。

**DIBL 的問題**：在 OFF 狀態下（VGS = 0），VDS 增加會使 Vth 降低 → 漏電流增加。

### 3.4 速度飽和（Velocity Saturation）

在短通道中，橫向電場 E = VDS/L 很大，載子速度飽和：

$$v_d = \frac{\mu E}{1 + \mu E / v_{sat}} \approx v_{sat} \quad \text{（E 很大時）}$$

速度飽和下的飽和電流：

$$I_{D,sat} = W C_{ox}(V_{GS} - V_{th})v_{sat}$$

**注意**：從 (VGS-Vth)² 變成 (VGS-Vth)¹ → 電流與過驅電壓成**線性**而非二次。

### 3.5 熱載子效應（Hot Carrier Injection, HCI）

通道中的高能（「熱」）載子可能：
1. 注入閘極氧化層 → 改變 Vth → 元件退化
2. 在汲極端造成碰撞游離 → 基板電流 ISUB
3. 嚴重時導致閘極電流 IG

**解決方案**：
- LDD（Lightly Doped Drain）結構降低汲極電場
- 降低 VDD

### 3.6 短通道效應的總結

```
長通道 MOSFET              短通道 MOSFET
─────────────              ─────────────
ID,sat ∝ (VGS-Vth)²        ID,sat ∝ (VGS-Vth)¹ （速度飽和）
Vth 與 L 無關              Vth 隨 L 縮小而降低（roll-off）
Vth 與 VDS 無關            Vth 隨 VDS 增加而降低（DIBL）
gm ∝ (VGS-Vth)             gm ≈ WCox·vsat（與 VGS 無關）
```

---

## 四、亞閾值特性（Subthreshold Characteristics）

### 4.1 亞閾值區（Subthreshold Region）

VGS < Vth 時，MOSFET 並非完全關閉。表面處於弱反轉（Weak Inversion），電流由擴散主導：

$$I_{D,sub} = I_0 \exp\left(\frac{V_{GS} - V_{th}}{nV_T}\right)\left[1 - \exp\left(-\frac{V_{DS}}{V_T}\right)\right]$$

其中 n = 1 + Cdep/Cox > 1（亞閾值斜率因子，body effect factor）。

### 4.2 亞閾值擺幅（Subthreshold Swing, SS）

$$SS = \frac{dV_{GS}}{d(\log_{10} I_D)} = \frac{kT}{q} \ln(10) \times n = 2.3 \times nV_T$$

**理想值**（n = 1，T = 300K）：

$$SS_{ideal} = \frac{kT}{q}\ln(10) = 0.026 \times 2.303 = 60 \text{ mV/dec}$$

**意義**：SS 表示每減少一個十倍（decade）的電流，需要改變多少閘極電壓。

```
log(ID) ↑
        │        ╱
        │       ╱
        │      ╱  ← 斜率 = 1/SS
        │     ╱     SS 越小，OFF更乾淨
        │    ╱
        │   ╱
        │  ╱
        │ ╱
        └─┼────────→ VGS
         Vth

每 60mV 電流變化 10 倍（理想值）
```

### 4.3 SS 的重要性

- SS 決定了 MOSFET 的「開關比」（Ion/Ioff）
- SS 越小 → 在相同 Ioff 下可以降低 Vth → 可以降低 VDD → 降低功耗
- 60 mV/dec 是**傳統 MOSFET 的理論極限**（Boltzmann tyranny）
- 突破 60 mV/dec 需要新機制：穿隧 FET（TFET）、負電容 FET（NC-FET）

### 4.4 IOFF 和 ION 的定義

- **IOFF**：VGS = 0，VDS = VDD 時的漏電流
- **ION**：VGS = VDS = VDD 時的驅動電流

```
Ion/Ioff 比值越大越好（通常要求 > 10⁶ ~ 10⁷）
```

---

## 五、MOSFET 尺度縮小定律（Scaling）

### 5.1 Dennard 等比例縮小（Constant-Field Scaling）

所有尺寸和電壓同時按 1/κ 縮小（κ > 1）：

| 參數 | 縮小比例 | 說明 |
|------|---------|------|
| L, W, tox | 1/κ | 物理尺寸 |
| VDD, Vth | 1/κ | 電壓 |
| Na | κ | 摻雜增加 |
| 電場 E | 1 | 保持不變！ |
| ID | 1/κ | 電流 |
| 延遲 CV/I | 1/κ | 速度提升 |
| 功耗 P=VI | 1/κ² | 大幅降低 |
| 功耗密度 P/A | 1 | 保持不變 |

### 5.2 為什麼 Dennard Scaling 不再有效？

從 ~90nm 節點開始，Dennard Scaling 遇到瓶頸：

1. **Vth 不能無限降低**：否則 IOFF 太大（SS ≥ 60 mV/dec 的限制）
2. **VDD 不能無限降低**：Vth 不降，VDD-Vth 太小，ION 不夠
3. **tox 不能無限薄**：否則閘極漏電（量子穿隧）
4. **功耗密度不再恆定**→ 功耗牆（Power Wall）

**解決方案**：
- High-k 閘極介電質（增加 Cox 而不減少物理厚度）
- Metal Gate（降低多晶矽空乏效應）
- FinFET（增加閘極對通道的控制力）
- 多核心設計（降低頻率但增加並行度）

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|---------|------|
| MOS電容器 | MOS Capacitor | Metal-Oxide-Semiconductor結構 | MOSFET的核心 |
| 累積 | Accumulation | 多數載子被吸引到表面 | VG < VFB |
| 空乏 | Depletion | 表面載子被排斥，形成空乏區 | VFB < VG < Vth |
| 反轉 | Inversion | 表面少數載子超過多數載子 | VG > Vth |
| 閾值電壓 | Threshold Voltage (Vth) | 開始形成導電通道的電壓 | NMOS典型 ~0.3-0.7V |
| 平帶電壓 | Flatband Voltage (VFB) | 讓能帶變平的閘極電壓 | VFB = φms - Qf/Cox |
| 氧化層電容 | Oxide Capacitance (Cox) | εox/tox | Cox ↑ → 控制力 ↑ |
| 漸變通道近似 | GCA | 假設通道電場緩慢變化 | I-V推導的基礎 |
| 通道長度調變 | CLM (λ) | 飽和區電流隨VDS微增 | λ: CLM參數 |
| 跨導 | Transconductance (gm) | ∂ID/∂VGS，閘極控制力 | gm = β(VGS-Vth) |
| DIBL | Drain-Induced Barrier Lowering | VDS↑ → Vth↓ | 短通道效應 |
| Vth Roll-off | Vth下降 | L↓ → Vth↓ | 短通道效應 |
| 速度飽和 | Velocity Saturation | 高電場下v→vsat | ID∝(VGS-Vth)¹ |
| 亞閾值擺幅 | Subthreshold Swing (SS) | 每decade電流需要的VGS變化 | 理想: 60mV/dec |
| 熱載子注入 | Hot Carrier Injection (HCI) | 高能載子注入氧化層 | 可靠度問題 |
| Dennard Scaling | 等比例縮小 | 所有尺寸和電壓同時縮小 | ~90nm後失效 |
| LDD | Lightly Doped Drain | 汲極輕摻雜降低電場 | 解決HCI |

---

## 數值例題

### 【例題 1】氧化層電容與閾值電壓

**題目**：NMOS，P 型基板 Na = 10¹⁷ cm⁻³，tox = 2 nm（SiO₂），φms = -0.9V，Qf = 5×10¹⁰ q C/cm²，T = 300K。求 Cox、VFB 和 Vth。

**解答**：

```
步驟 1：Cox
Cox = εox/tox = 3.9 × 8.854×10⁻¹⁴ / (2×10⁻⁷)
    = 3.453×10⁻¹³ / 2×10⁻⁷
    = 1.727×10⁻⁶ F/cm² = 1.727 μF/cm²

步驟 2：φF
φF = VT × ln(Na/ni) = 0.026 × ln(10¹⁷/1.5×10¹⁰)
   = 0.026 × 15.71 = 0.409 V

步驟 3：VFB
Qf = 5×10¹⁰ × 1.6×10⁻¹⁹ = 8×10⁻⁹ C/cm²
VFB = φms - Qf/Cox = -0.9 - 8×10⁻⁹/1.727×10⁻⁶
    = -0.9 - 0.0046 = -0.905 V

步驟 4：Qdep
|Qdep| = √(2qεsNa × 2φF)
       = √(2 × 1.6×10⁻¹⁹ × 1.036×10⁻¹² × 10¹⁷ × 2 × 0.409)
       = √(2 × 1.6×10⁻¹⁹ × 1.036×10⁻¹² × 10¹⁷ × 0.818)
       = √(2.714×10⁻¹⁴)
       = 1.648×10⁻⁷ C/cm²

步驟 5：Vth
Vth = VFB + 2φF + |Qdep|/Cox
    = -0.905 + 0.818 + 1.648×10⁻⁷/1.727×10⁻⁶
    = -0.905 + 0.818 + 0.095
    = 0.008 V ≈ 8 mV
```

**觀察**：tox = 2nm 時，Cox 非常大，所以 Qdep/Cox 很小。現代製程的 Vth 主要由功函數工程調整。

---

### 【例題 2】MOSFET 電流計算（線性區與飽和區）

**題目**：NMOS，μn = 400 cm²/V·s，Cox = 1.5×10⁻⁶ F/cm²，W = 1 μm，L = 50 nm，Vth = 0.3V。求 VGS = 0.8V 時，VDS = 0.1V 和 VDS = 0.8V 的 ID。

**解答**：

```
VGS - Vth = 0.8 - 0.3 = 0.5 V
VDS,sat = VGS - Vth = 0.5 V

k'n = μnCox = 400 × 1.5×10⁻⁶ = 6×10⁻⁴ A/V²

(a) VDS = 0.1V < 0.5V → 線性區
ID = k'n(W/L)[(VGS-Vth)VDS - VDS²/2]
   = 6×10⁻⁴ × (10⁻⁴/5×10⁻⁶) × [0.5×0.1 - 0.01/2]
   = 6×10⁻⁴ × 20 × [0.05 - 0.005]
   = 0.012 × 0.045
   = 5.4×10⁻⁴ A = 0.54 mA

(b) VDS = 0.8V > 0.5V → 飽和區
ID = (1/2)k'n(W/L)(VGS-Vth)²
   = 0.5 × 6×10⁻⁴ × 20 × 0.5²
   = 0.5 × 0.012 × 0.25
   = 1.5×10⁻³ A = 1.5 mA
```

---

### 【例題 3】跨導計算

**題目**：承上題，VDS = 0.8V（飽和區），求 gm 和 gm/ID。

**解答**：

```
gm = k'n(W/L)(VGS - Vth)
   = 6×10⁻⁴ × 20 × 0.5
   = 6×10⁻³ A/V = 6 mS

或者：gm = 2ID/(VGS-Vth) = 2×1.5×10⁻³/0.5 = 6×10⁻³ ✓

gm/ID = 2/(VGS-Vth) = 2/0.5 = 4 V⁻¹

（在亞閾值區 gm/ID → q/nkT ≈ 1/0.026 ≈ 38.5 V⁻¹，是最大值）
```

---

### 【例題 4】短通道效應——速度飽和

**題目**：上題的 NMOS（L = 50nm），vsat = 10⁷ cm/s。比較長通道模型和速度飽和模型的飽和電流。

**解答**：

```
長通道模型（已算）：
ID,sat = 1.5 mA

速度飽和模型：
ID,sat = WCox(VGS - Vth)vsat
       = 10⁻⁴ × 1.5×10⁻⁶ × 0.5 × 10⁷
       = 7.5×10⁻⁴ A = 0.75 mA

速度飽和模型 / 長通道模型 = 0.75/1.5 = 0.5

速度飽和使得實際電流比長通道模型預測的低 50%。
在 L = 50nm 這種超短通道中，速度飽和是絕對主導的效應。
```

---

### 【例題 5】亞閾值擺幅

**題目**：MOSFET 的 n = 1.3（body factor），T = 300K。求 SS。如果 Vth = 0.3V、VDD = 0.8V，求 ION/IOFF（忽略 DIBL）。

**解答**：

```
SS = n × VT × ln(10) = 1.3 × 0.026 × 2.303
   = 0.0778 V/dec = 77.8 mV/dec

ION/IOFF 估算：
在 OFF 狀態（VGS=0），電流相對 Vth 偏移了 Vth/SS 個 decade

log(ION/IOFF) ≈ Vth/SS = 0.3/0.0778 = 3.86 decades

ION/IOFF ≈ 10^3.86 ≈ 7200

這個比值偏低（通常需要 > 10⁶）。所以 Vth 不能太低。
如果 Vth = 0.5V：ION/IOFF ≈ 10^(0.5/0.078) = 10^6.4 ≈ 2.5×10⁶ ✓
```

---

### 【例題 6】DIBL 的影響

**題目**：長通道 Vth = 0.4V，DIBL 係數 η = 80 mV/V，VDD = 0.8V。求實際 Vth 和 DIBL 造成的 IOFF 變化。

**解答**：

```
Vth(VDS=VDD) = Vth,long - η×VDD
             = 0.4 - 0.08×0.8
             = 0.4 - 0.064
             = 0.336 V

Vth 降低了 64 mV。

IOFF 的變化（假設 SS = 70 mV/dec）：
ΔVth = 64 mV
IOFF 增加倍數 = 10^(ΔVth/SS) = 10^(64/70) = 10^0.914 = 8.2 倍

DIBL 使 OFF 漏電流增加了約 8 倍。
```

---

## 題型鑑別

| 看到什麼關鍵字 | 用什麼方法 | 對應公式 |
|--------------|----------|---------|
| Vth、閾值電壓 | 公式推導 | Vth = VFB + 2φF + Qdep/Cox |
| C-V特性 | 三區域分析 | 累積/空乏/反轉 |
| 線性區/三極區 | VDS < VGS-Vth | ID = k'(W/L)[(VGS-Vth)VDS-VDS²/2] |
| 飽和區 | VDS ≥ VGS-Vth | ID = (1/2)k'(W/L)(VGS-Vth)² |
| 跨導 gm | 對VGS微分 | gm = k'(W/L)(VGS-Vth) |
| 短通道、L很小 | 速度飽和 | ID = WCox(VGS-Vth)vsat |
| SS、亞閾值 | 60mV/dec基準 | SS = n×VT×ln10 |
| DIBL | Vth隨VDS變化 | Vth(VDS) = Vth0 - η×VDS |
| CLM、λ | 飽和區斜率 | ID(1+λVDS) |
| ION/IOFF | SS和Vth | log(ION/IOFF) ≈ Vth/SS |

---

## ✅ 自我檢測

### 基礎題

**Q1**：MOS 電容器的三種工作狀態是什麼？分別對應什麼閘極電壓？

<details>
<summary>點擊查看答案</summary>

以 P 型基板 NMOS 為例：

1. **累積（Accumulation）**：VG < VFB → 電洞被吸引到表面
2. **空乏（Depletion）**：VFB < VG < Vth → 表面電洞被排斥，形成空乏區
3. **反轉（Inversion）**：VG > Vth → 表面電子多於電洞，形成導電通道

</details>

**Q2**：為什麼 SS ≥ 60 mV/dec 被稱為「Boltzmann 暴政」？

<details>
<summary>點擊查看答案</summary>

SS 的理想值 = (kT/q)·ln(10) = 60 mV/dec @300K。

這個極限來自載子的玻茲曼能量分佈（指數尾巴），是任何基於熱離子發射（Thermionic Emission）機制的 MOSFET 的物理極限。

它限制了：
- Vth 不能太低（否則 IOFF 太大）
- VDD 不能太低（否則 ION 太小）
- 功耗不能無限降低

這被稱為「Boltzmann 暴政」（Boltzmann Tyranny），是推動研究 TFET、NC-FET 等次 60mV/dec 元件的動力。

</details>

**Q3**：MOSFET 飽和區的電流公式是什麼？VDS,sat 是多少？

<details>
<summary>點擊查看答案</summary>

$$I_{D,sat} = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS} - V_{th})^2$$

VDS,sat = VGS - Vth（夾斷條件）

飽和區的電流（理想上）不隨 VDS 變化（實際上有 CLM 微增）。

</details>

### 進階題

**Q4**：為什麼短通道 MOSFET 的飽和電流從 (VGS-Vth)² 變成 (VGS-Vth)¹？

<details>
<summary>點擊查看答案</summary>

在短通道中，通道電場很高（E ≈ VDS/L），載子速度飽和（v → vsat）。

此時電流不再由 μE 決定，而是由 vsat 決定：

$$I_{D,sat} = W C_{ox}(V_{GS} - V_{th})v_{sat}$$

過驅電壓的指數從 2 降為 1，因為速度不再隨電場線性增加。

這對電路設計的影響：
- gm = WCox·vsat（與 VGS 無關）
- gm/ID 比長通道低
- 增加 W 是提高電流的主要方式

</details>

**Q5**：TSMC 面試題：解釋為什麼 tox 不能無限減薄？High-k 如何解決這個問題？

<details>
<summary>點擊查看答案</summary>

**tox 不能太薄的原因**：
- SiO₂ 厚度小於 ~1.5nm 時，閘極漏電流急劇增加（量子穿隧）
- 穿隧電流 ∝ exp(-tox)，極其敏感

**High-k 的解決方案**：
用高介電常數材料（如 HfO₂，εr ≈ 25）取代 SiO₂（εr = 3.9）：

Cox = ε/t → 用更厚的 High-k 得到等效甚至更大的 Cox

等效氧化層厚度 EOT = (εSiO₂/εHK) × tHK
例如：tHK = 5nm HfO₂ → EOT = (3.9/25)×5 = 0.78nm

物理厚度 5nm 夠厚，穿隧漏電小；但電氣效果等於 0.78nm 的 SiO₂。

</details>

**Q6**：為什麼 FinFET 比平面 MOSFET 能更好地控制短通道效應？

<details>
<summary>點擊查看答案</summary>

FinFET 的閘極從三面包覆通道（Fin 的左、右、頂），而平面 MOSFET 只從上方一面控制。

多面閘極控制的優勢：
1. 閘極對通道的電場穿透更強 → 更好的閘極控制力
2. 源極/汲極對通道的影響被閘極屏蔽 → **DIBL 降低**
3. 等效的 Vth roll-off 更小 → 可以做更短的 L
4. SS 更接近理想 60 mV/dec

定量地說，「自然長度」（Natural Length）λ 越小，短通道效應越弱：
- 平面：λ ∝ √(tox × tbody)
- FinFET：λ 更小（因為多面閘極等效地減薄了 tbody）

</details>

---

## 本章重點整理

```
1. MOS三態：累積(VG<VFB)→空乏→反轉(VG>Vth)
2. Vth = VFB + 2φF + Qdep/Cox
3. 線性區：ID = k'(W/L)[(VGS-Vth)VDS - VDS²/2]
4. 飽和區：ID = (1/2)k'(W/L)(VGS-Vth)²
5. 跨導：gm = k'(W/L)(VGS-Vth) = 2ID/(VGS-Vth)
6. CLM：ID,sat(1+λVDS)，λ ∝ 1/L
7. 短通道效應：Vth roll-off, DIBL, 速度飽和, HCI
8. 速度飽和：ID = WCox(VGS-Vth)vsat → ∝(VGS-Vth)¹
9. SS = n×VT×ln10 ≥ 60mV/dec（300K理想值）
10. Scaling：L↓ → 速度↑ 功耗↓，但受SS和漏電限制
11. High-k/Metal Gate 解決閘極漏電問題
12. FinFET 多面閘極解決短通道效應
```

---

> **下一章預告**：[第七章 BJT 與進階元件](semi_07_BJT與進階元件.md) —— 深入 BJT 的物理，並介紹 SOI、FinFET、GAA 等先進元件結構。
