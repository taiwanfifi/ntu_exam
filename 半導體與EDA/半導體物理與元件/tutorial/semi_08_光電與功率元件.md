# 第八章：光電與功率元件

> **學習目標**：理解太陽能電池、LED、雷射、光偵測器和功率元件的物理原理與設計考量。
> **預備知識**：第四章（產生復合）、第五章（PN 接面）
> **預估時間**：4～5 小時

---

## 🔰 本章基礎觀念（零基礎必讀）

### 光電元件 vs 功率元件

| 類別 | 核心物理 | 代表元件 |
|------|---------|---------|
| 光→電 | 光子吸收 → 產生電子-電洞對 → 收集 | 太陽能電池、光偵測器 |
| 電→光 | 電子-電洞復合 → 釋放光子 | LED、雷射 |
| 功率 | 高電壓/大電流切換 | Power MOSFET、IGBT |

### 一分鐘抓住核心

```
太陽能電池：光 → 載子 → PN接面分離 → 電流
LED：      電流 → 載子注入 → 輻射復合 → 光
雷射：     LED + 增益介質 + 光腔 → 相干光
功率元件： 控制大電壓/大電流，低損耗是關鍵
```

---

## 一、太陽能電池（Solar Cell）

### 1.1 基本原理

太陽能電池就是一個反偏的 PN 接面二極體，只是反偏電流由光照提供：

1. **光子吸收**：能量 > Eg 的光子被半導體吸收，產生電子-電洞對
2. **載子分離**：PN 接面的內建電場將電子掃向 N 側，電洞掃向 P 側
3. **電流輸出**：外部電路中流過電流，做功

```
      光 ↓↓↓↓↓↓
   ┌──────────────┐
   │   n⁺ 射極    │  ← 薄，讓光穿過
   ├──────────────┤
   │   空乏區     │  ← 電場分離載子
   ├──────────────┤
   │              │
   │   p 型基板   │  ← 厚，吸收光
   │              │
   └──────────────┘
        │    │
       (+)  (-)    → 外部負載
```

### 1.2 I-V 特性

$$I = I_L - I_s\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

其中 IL 是**光產生電流（Photo-generated Current）**，正比於光照強度。

```
I ↑
  │ Isc ○─────────────╮
  │                    │
  │                    │
  │           Pmax ─→  ■ (Vm, Im)
  │                    │
  │                    │
  │                    ╰─○ Voc
  └──────────────────────→ V

Isc = 短路電流 ≈ IL
Voc = 開路電壓 = nVT·ln(IL/Is + 1)
```

### 1.3 關鍵參數

**短路電流 Isc**：
$$I_{sc} \approx I_L$$

**開路電壓 Voc**：
$$V_{oc} = nV_T \ln\left(\frac{I_L}{I_s} + 1\right) \approx nV_T \ln\left(\frac{I_L}{I_s}\right)$$

**最大功率點 (Vm, Im)**：
$$P_{max} = V_m \times I_m$$

**填充因子（Fill Factor, FF）**：
$$FF = \frac{V_m \times I_m}{V_{oc} \times I_{sc}} = \frac{P_{max}}{V_{oc} \times I_{sc}}$$

典型值：FF ≈ 0.75 ~ 0.85

**轉換效率 η**：
$$\eta = \frac{P_{max}}{P_{in}} = \frac{V_{oc} \times I_{sc} \times FF}{P_{in}}$$

Pin = 入射光功率，標準測試條件（AM1.5G）：Pin = 100 mW/cm²

### 1.4 效率限制因素

| 損耗機制 | 說明 | 改善方法 |
|---------|------|---------|
| 光子能量 < Eg | 長波長光無法被吸收 | 多接面串疊（Multi-junction） |
| 光子能量 > Eg | 多餘能量變成熱（熱化損耗） | 多接面串疊 |
| 表面反射 | 光被反射回去 | 抗反射層（Anti-reflection coating） |
| 表面復合 | 表面缺陷吃掉載子 | 鈍化（SiO₂, Al₂O₃） |
| 體復合 | 體內 SRH/Auger 復合 | 高品質矽（長 τ） |
| 串聯電阻 | 歐姆損耗 | 優化電極設計 |

### 1.5 Shockley-Queisser 極限

單接面太陽能電池的理論最大效率：

$$\eta_{max} \approx 33.7\% \quad \text{（Eg ≈ 1.34 eV 時最佳）}$$

Si（Eg = 1.12 eV）的 SQ 極限約 **29.4%**。目前實驗室記錄約 26.8%。

---

## 二、LED（發光二極體）

### 2.1 基本原理

LED 是正偏的 PN 接面，電子和電洞在接面附近復合，釋放光子。

1. **正偏注入**：電子注入 P 區，電洞注入 N 區
2. **輻射復合**：在活性層中，電子-電洞對復合，釋放出能量等於 Eg 的光子
3. **出光**：光子從半導體中射出

### 2.2 為什麼需要直接帶隙？

- **直接帶隙**（GaAs, GaN, InGaN）：復合時動量守恆自動滿足，光子發射效率高
- **間接帶隙**（Si, Ge）：需要聲子協助，發光效率極低

### 2.3 波長與能帶隙

$$\lambda = \frac{hc}{E_g} \quad \Rightarrow \quad \lambda(\mu m) = \frac{1.24}{E_g(eV)}$$

| 材料 | Eg (eV) | λ (nm) | 顏色 |
|------|---------|--------|------|
| GaAs | 1.42 | 873 | 紅外 |
| AlGaAs | 1.43~1.9 | 650~870 | 紅~紅外 |
| GaAsP | 1.9~2.2 | 560~650 | 黃~紅 |
| InGaN | 2.0~3.4 | 365~620 | 紫外~綠 |
| GaN | 3.4 | 365 | 紫外 |

### 2.4 量子效率

**內部量子效率（Internal Quantum Efficiency, IQE）**：

$$\eta_{int} = \frac{R_{rad}}{R_{rad} + R_{non-rad}} = \frac{B \cdot np}{B \cdot np + R_{SRH} + R_{Auger}}$$

**外部量子效率（External Quantum Efficiency, EQE）**：

$$\eta_{ext} = \eta_{int} \times \eta_{extraction}$$

光取出效率 ηextraction 受全內反射限制：

$$\eta_{extraction} \approx \frac{1}{4n^2}$$

對 GaN（n ≈ 2.5）：ηextraction ≈ 4%（如果不做特殊處理）。

改善方法：粗化表面、光子晶體、倒裝晶片（Flip-chip）封裝。

### 2.5 雙異質接面 LED（DH LED）

```
     n-AlGaAs    │  GaAs  │  p-AlGaAs
    (寬能隙)      │(窄能隙)│  (寬能隙)
                  │活性層  │
  ──Ec──╲        │  ↕Eg   │       ╱──Ec──
         ╲───────│────────│──────╱
         ╱───────│────────│──────╲
  ──Ev──╱        │        │       ╲──Ev──

  電子→→→→ 被侷限在活性層 ←←←←電洞
  兩側寬能隙材料形成位障
```

優勢：載子被侷限在薄的活性層 → 高載子密度 → 高復合率 → 高亮度。

---

## 三、Laser Diode（半導體雷射）

### 3.1 基本原理

半導體雷射在 LED 的基礎上加入：

1. **增益介質**：注入足夠多的載子，使增益 > 損耗（Population Inversion）
2. **光學共振腔**：兩個鏡面反射光來回，形成駐波
3. **受激輻射（Stimulated Emission）**：光子觸發更多光子 → 相干光

### 3.2 臨界電流密度

$$J_{th} = \frac{qdn_i}{τ_{rad}} \times n_{th}$$

當注入電流超過臨界電流 Jth 時，受激輻射超過自發輻射，開始雷射動作。

### 3.3 LED vs Laser

| 特性 | LED | Laser |
|------|-----|-------|
| 發光機制 | 自發輻射 | 受激輻射 |
| 光譜寬度 | 寬（~30nm） | 窄（< 1nm） |
| 方向性 | 發散 | 高度準直 |
| 相干性 | 非相干 | 相干 |
| 效率 | 中 | 高（超過臨界後） |
| 應用 | 照明、顯示 | 光通訊、光碟、雷射切割 |

### 3.4 雷射的 L-I 特性

```
光功率 P
    ↑
    │           ╱
    │          ╱  受激輻射
    │         ╱   （斜率效率）
    │        ╱
    │   ----╱ ← Ith（臨界電流）
    │ --   自發輻射
    │-
    └──────────────→ 電流 I
         Ith
```

---

## 四、光偵測器（Photodetector）

### 4.1 PIN 光偵測器

```
    p⁺  │    i (本質)    │  n⁺
  ──────┤───────────────┤──────
        │←─ 寬空乏區 ──→│
        │  光吸收在這裡  │
        │  E field 掃出載子│
```

**I 層（本質層）**的優勢：
- 空乏區寬 → 吸收更多光子
- 電場均勻 → 載子快速被收集
- 接面電容小 → 高頻響應好

### 4.2 雪崩光偵測器（APD, Avalanche Photodetector）

利用雪崩倍增效應放大光電流：

$$M = \frac{I_{ph}}{I_{ph,primary}} = \frac{1}{1 - (V/V_{BR})^n}$$

增益 M 可達 10~100 倍，但伴隨超額雜訊。

### 4.3 響應度與量子效率

**響應度（Responsivity）**：

$$\mathcal{R} = \frac{I_{ph}}{P_{opt}} = \frac{\eta_q \lambda}{1.24} \quad \text{(A/W)}$$

其中 ηq 是量子效率（每個光子產生一個電子-電洞對的機率）。

---

## 五、功率元件

### 5.1 功率元件的特殊需求

| 需求 | 原因 | 對應參數 |
|------|------|---------|
| 高崩潰電壓 | 承受數百~數千伏特 | VBR |
| 低導通電阻 | 減少導通損耗 | RDS(on) |
| 快速切換 | 減少切換損耗 | ton, toff |
| 高電流密度 | 推動大負載 | JD |

### 5.2 Power MOSFET

功率 MOSFET 使用**垂直結構**以承受高電壓：

```
      Source     Gate     Source
    ┌──n⁺──┐ ┌──────┐ ┌──n⁺──┐
    │      │ │Oxide │ │      │
    │  p   │ │      │ │  p   │  ← body
    │      └─┤      ├─┘      │
    │        │  n⁻  │        │  ← 漂移區（承受電壓）
    │        │      │        │
    │        │      │        │
    │        │  n⁺  │        │  ← 基板
    └────────┴──────┴────────┘
              Drain

電流垂直流動：Source → channel → n⁻ drift → n⁺ → Drain
```

**漂移區（Drift Region）**：輕摻雜的 n⁻ 層，承受大部分電壓。

**Ron 和 VBR 的矛盾**：

$$R_{on} \propto \frac{W_{drift}}{N_d} \propto V_{BR}^{2.5} \quad \text{（矽的理論限制）}$$

崩潰電壓越高 → 漂移區越厚、摻雜越低 → 導通電阻越大

**SiC 的優勢**：臨界電場是 Si 的 10 倍 → 同樣的 VBR 下，漂移區薄 10 倍、摻雜高 10 倍 → **Ron 降低 ~300 倍**（理論上）。

### 5.3 IGBT（Insulated Gate Bipolar Transistor）

IGBT 結合了 MOSFET 的高輸入阻抗和 BJT 的低飽和電壓：

```
     MOSFET 控制     │  BJT 大電流
     （電壓驅動）    │  （電導調變）
                     │
   ┌──n⁺──┐ ┌──────┐ ┌──n⁺──┐
   │      │ │Oxide │ │      │
   │  p   │ │      │ │  p   │
   │      └─┤      ├─┘      │
   │        │  n⁻  │        │  ← 漂移區
   │        │      │        │
   │        │  p⁺  │        │  ← ← 注意：這裡是 p⁺（不是 n⁺）
   └────────┴──────┴────────┘
             Collector

與 Power MOSFET 唯一的差別：
基板從 n⁺ 換成 p⁺ → 形成 PNP BJT → 電導調變
```

**IGBT 的電導調變（Conductivity Modulation）**：
p⁺ 基板注入電洞到 n⁻ 漂移區 → 漂移區載子濃度大增 → Ron 大幅降低

**IGBT 的缺點**：
- 關斷時需要清除注入的少數載子 → 拖尾電流（Tail Current）→ 切換速度比 MOSFET 慢

### 5.4 安全操作區（SOA, Safe Operating Area）

```
ID (log) ↑
         │╲
         │ ╲ 電流限制
         │  ╲
         │   ╲──── 功率限制 P = VD × ID
         │    │╲
         │    │ ╲
         │    │  ╲── 二次崩潰限制（BJT才有）
         │    │   ╲
         │    │    ╲── 崩潰電壓限制
         └────┴─────┴──→ VDS (log)
                    VBR
```

SOA 定義了元件可以安全操作的 VDS-ID 範圍，超出範圍可能損壞元件。

### 5.5 功率元件材料比較

| 參數 | Si | SiC (4H) | GaN |
|------|-----|---------|------|
| Eg (eV) | 1.12 | 3.26 | 3.4 |
| Ecrit (MV/cm) | 0.3 | 3.0 | 3.3 |
| μn (cm²/V·s) | 1350 | 900 | 1000 |
| vsat (10⁷ cm/s) | 1.0 | 2.0 | 2.5 |
| 熱導率 (W/cm·K) | 1.5 | 4.9 | 1.3 |
| Ron 優勢 (vs Si) | 1× | ~300× | ~500× |

SiC 額外有優異的熱導率 → 散熱容易 → 電動車首選。

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|---------|------|
| 太陽能電池 | Solar Cell | 光→電的PN接面 | Si, GaAs, 鈣鈦礦 |
| 短路電流 | Short-Circuit Current (Isc) | V=0時的最大電流 | ≈ 光產生電流 |
| 開路電壓 | Open-Circuit Voltage (Voc) | I=0時的最大電壓 | Voc = nVT·ln(IL/Is) |
| 填充因子 | Fill Factor (FF) | I-V曲線的「方正度」 | FF ≈ 0.75~0.85 |
| 轉換效率 | Conversion Efficiency (η) | 光→電的轉換比例 | Si: 最高~26.8% |
| LED | Light-Emitting Diode | 電→光的PN接面 | 照明、顯示器 |
| 內部量子效率 | Internal Quantum Efficiency (IQE) | 輻射復合佔總復合的比例 | 直接帶隙材料高 |
| 外部量子效率 | External Quantum Efficiency (EQE) | 實際出光效率 | EQE = IQE × ηextraction |
| 受激輻射 | Stimulated Emission | 光子觸發更多同相位光子 | 雷射原理 |
| 臨界電流 | Threshold Current (Ith) | 雷射開始動作的最低電流 | Ith越低越好 |
| PIN二極體 | PIN Diode | p-i-n結構光偵測器 | 寬空乏區吸收光 |
| APD | Avalanche Photodiode | 雪崩倍增光偵測器 | M ≈ 10~100倍增益 |
| 功率MOSFET | Power MOSFET | 垂直結構功率開關 | 低壓大電流應用 |
| IGBT | Insulated Gate Bipolar Transistor | MOSFET+BJT混合 | 高壓大電流（電動車） |
| 電導調變 | Conductivity Modulation | 注入少數載子降低漂移區電阻 | IGBT的關鍵優勢 |
| 安全操作區 | Safe Operating Area (SOA) | 元件安全工作的V-I範圍 | 超出可能燒毀 |
| 漂移區 | Drift Region | 承受電壓的輕摻雜區 | Power MOSFET的n⁻層 |

---

## 數值例題

### 【例題 1】太陽能電池效率計算

**題目**：Si 太陽能電池，A = 100 cm²，在 AM1.5G（100 mW/cm²）下測得 Isc = 3.5 A，Voc = 0.65 V，FF = 0.80。求效率。

**解答**：

```
Pin = 100 mW/cm² × 100 cm² = 10,000 mW = 10 W

Pmax = Voc × Isc × FF = 0.65 × 3.5 × 0.80 = 1.82 W

η = Pmax/Pin = 1.82/10 = 0.182 = 18.2%

答案：η = 18.2%
```

---

### 【例題 2】太陽能電池的 Voc

**題目**：Si 太陽能電池，Is = 10⁻¹² A，光產生電流 IL = 30 mA，n = 1，T = 300K。求 Voc。

**解答**：

```
Voc = nVT × ln(IL/Is + 1) ≈ nVT × ln(IL/Is)
    = 1 × 0.026 × ln(30×10⁻³/10⁻¹²)
    = 0.026 × ln(3×10¹⁰)
    = 0.026 × 24.12
    = 0.627 V

答案：Voc ≈ 0.63 V
```

**觀察**：Voc < Eg/q = 1.12V。Voc 永遠小於 Eg/q，差異主要來自 Is 的大小。Is 越小 → Voc 越大 → 效率越高。

---

### 【例題 3】LED 波長計算

**題目**：InGaN 量子井的 Eg 被調到 2.75 eV（透過組成調整）。求發光波長和顏色。

**解答**：

```
λ = 1.24 / Eg = 1.24 / 2.75 = 0.451 μm = 451 nm

顏色：藍光（可見光中 450~495nm 為藍色）

這就是藍光 LED 的原理，由 InGaN/GaN 量子井實現。
```

---

### 【例題 4】Power MOSFET 的 Ron vs VBR 權衡

**題目**：Si Power MOSFET，VBR = 600V 時，RDS(on)·A = 150 mΩ·cm²。如果改用 SiC（Ron 改善 ~300 倍），求 SiC 的 RDS(on)·A。

**解答**：

```
SiC 的理論 Ron 改善倍數：
(Ecrit,SiC/Ecrit,Si)³ × (μSi/μSiC) ≈ 10³ × (1350/900)
= 1000 × 1.5 = 1500 倍

但實際改善約 300 倍（受其他損耗限制）：

RDS(on)·A (SiC) = 150 / 300 = 0.5 mΩ·cm²

這意味著相同面積的 SiC 元件，導通損耗只有 Si 的 1/300。
或者說，相同導通電阻下，SiC 晶片面積可以縮小 300 倍。
```

---

### 【例題 5】光偵測器響應度

**題目**：Si PIN 光偵測器，在 λ = 850nm 下量子效率 ηq = 90%。求響應度。

**解答**：

```
R = ηq × λ / 1.24 = 0.90 × 0.85 / 1.24 = 0.617 A/W

如果入射光功率 Popt = 1 mW：
Iph = R × Popt = 0.617 × 10⁻³ = 0.617 mA
```

---

### 【例題 6】IGBT vs Power MOSFET 比較

**題目**：600V 應用場景，負載電流 50A。比較 Si Power MOSFET（RDS(on) = 0.2 Ω）和 IGBT（VCE(sat) = 2V）的導通損耗。

**解答**：

```
Power MOSFET 導通損耗：
P_MOSFET = I² × RDS(on) = 50² × 0.2 = 500 W

IGBT 導通損耗：
P_IGBT = I × VCE(sat) = 50 × 2 = 100 W

IGBT 的導通損耗只有 MOSFET 的 1/5！

原因：IGBT 利用電導調變大幅降低了漂移區電阻。
但 IGBT 的切換速度較慢（拖尾電流），切換損耗較大。

結論：
- 低頻高壓大電流（如工業馬達驅動）→ IGBT 較佳
- 高頻中壓（如DC-DC轉換器）→ Power MOSFET 較佳
- 高壓高頻 → SiC MOSFET 最佳
```

---

## 題型鑑別

| 看到什麼關鍵字 | 用什麼方法 | 對應公式 |
|--------------|----------|---------|
| 太陽能電池、效率 | η = Voc×Isc×FF/Pin | Pin=100mW/cm²(AM1.5) |
| Voc、開路電壓 | Voc公式 | Voc = nVT·ln(IL/Is) |
| LED、波長 | λ = 1.24/Eg | 注意單位 μm 和 eV |
| 量子效率 | IQE和EQE | EQE = IQE × ηextraction |
| 雷射、臨界電流 | L-I特性 | I > Ith 才雷射 |
| 光偵測器、響應度 | R = ηq·λ/1.24 | 單位 A/W |
| 功率MOSFET、Ron | Ron ∝ VBR^2.5 | SiC降低~300倍 |
| IGBT、電導調變 | 導通損耗比較 | P = I×VCE(sat) |
| SOA | V-I安全範圍 | 不能超出 |

---

## ✅ 自我檢測

### 基礎題

**Q1**：太陽能電池的三個關鍵參數（Isc, Voc, FF）分別代表什麼？

<details>
<summary>點擊查看答案</summary>

- **Isc（短路電流）**：V = 0 時的電流，代表「能收集多少光產生的載子」
- **Voc（開路電壓）**：I = 0 時的電壓，代表「PN 接面能建立多大的電位差」
- **FF（填充因子）**：I-V 曲線的「方正度」，FF = Pmax/(Voc×Isc)

三者的乘積（再除以入射功率）就是效率：η = Voc×Isc×FF/Pin

</details>

**Q2**：為什麼 LED 必須用直接帶隙材料？

<details>
<summary>點擊查看答案</summary>

LED 的發光靠**輻射復合**（電子-電洞復合時釋放光子）。

- 直接帶隙：電子從導帶底部跳到價帶頂部，動量自動守恆（兩者在同一個 k 值），可以直接釋放光子 → 高效發光
- 間接帶隙（如 Si）：導帶最低點和價帶最高點的 k 值不同，需要聲子（晶格振動）協助才能完成跳躍，但三者同時滿足的機率極低 → 發光效率極差

所以 LED 用 GaN、InGaN、GaAs 等直接帶隙材料。

</details>

**Q3**：Power MOSFET 和 IGBT 各適合什麼應用場景？

<details>
<summary>點擊查看答案</summary>

| 特性 | Power MOSFET | IGBT |
|------|-------------|------|
| 切換速度 | 快（無少數載子儲存） | 慢（有拖尾電流） |
| 導通損耗（高壓） | 高（Ron ∝ VBR^2.5） | 低（電導調變） |
| 驅動方式 | 電壓驅動（簡單） | 電壓驅動（簡單） |

- **Power MOSFET**：中低壓（< 200V）、高頻（> 100kHz），如 DC-DC converter
- **IGBT**：高壓（> 600V）、低頻（< 20kHz），如工業馬達驅動、電動車逆變器
- **SiC MOSFET**：高壓+高頻，逐漸取代兩者在電動車中的應用

</details>

### 進階題

**Q4**：為什麼太陽能電池的 Voc 永遠小於 Eg/q？

<details>
<summary>點擊查看答案</summary>

Voc = nVT·ln(IL/Is)

Is ∝ ni² ∝ exp(-Eg/kT)，所以 Voc ∝ Eg - kT·ln(terms)

Voc < Eg/q 的原因：
1. **Is 不為零**：即使 IL 很大，Voc 也受限於 ln(IL/Is) 的有限值
2. **復合損耗**：Auger、SRH、表面復合都增加 Is → 降低 Voc
3. **熱力學限制**：太陽能電池在有限溫度下工作，不可能達到 Carnot 效率
4. 實際 Voc 大約是 Eg/q - 0.3~0.5V

例如 Si：Eg = 1.12V，實際 Voc ≈ 0.65~0.75V。

</details>

**Q5**：什麼是全內反射？它怎麼限制 LED 的外部量子效率？

<details>
<summary>點擊查看答案</summary>

當光從高折射率介質（如 GaN，n≈2.5）射向低折射率介質（空氣，n=1）時，入射角大於臨界角的光會被完全反射回去。

臨界角 θc = arcsin(1/n) = arcsin(1/2.5) = 23.6°

只有在錐角 2θc 內的光才能逃出 → 光取出效率：
ηextraction ≈ 1/(4n²) ≈ 1/(4×6.25) = 4%

也就是說，96% 的光被困在 LED 內部！

解決方案：
- 表面粗化：破壞全反射條件
- 光子晶體結構
- 倒裝晶片封裝
- 成形透鏡

現代高效 LED 透過這些技術可以達到 ηextraction > 80%。

</details>

---

## 本章重點整理

```
1. 太陽能電池：I = IL - Is[exp(V/nVT)-1]
2. 效率 η = Voc×Isc×FF/Pin，SQ極限~33.7%
3. Voc = nVT·ln(IL/Is)，降低Is是提高效率的關鍵
4. LED：直接帶隙材料，λ = 1.24/Eg (μm)
5. EQE = IQE × ηextraction，全內反射是主要損失
6. 雷射：受激輻射，I > Ith 才啟動
7. PIN光偵測器：寬空乏區提高吸收和速度
8. Power MOSFET：垂直結構，Ron ∝ VBR^2.5
9. IGBT = MOSFET + BJT：電導調變降低Ron，但切換慢
10. SiC/GaN功率元件：Ron降低100~500倍，電動車/5G關鍵
```

---

> **下一章預告**：[第九章 先進製程與可靠度](semi_09_先進製程與可靠度.md) —— 最後一章，涵蓋 HKMG、應變工程、可靠度，以及 TSMC/Intel/Samsung 的製程競爭。這是面試的加分項。
