# 電子學（六）：MOSFET 小信號分析

## 🔰 本章基礎觀念（零基礎必讀）

### 回顧：小信號分析的核心思想

在上一章我們學了 MOSFET 的直流特性。現在，就像 BJT 的小信號分析一樣，我們要在直流工作點附近做**線性化**，分析交流信號的放大行為。

### MOSFET 小信號分析 vs BJT 小信號分析

好消息：**分析方法完全相同！** 只是小信號模型的參數不同。

| 對應關係 | BJT | MOSFET |
|---------|-----|--------|
| 轉導 | gm = IC/VT | gm = 2ID/VOV |
| 輸入電阻 | rπ = β/gm | **無窮大**（IG = 0） |
| 輸出電阻 | ro = VA/IC | ro = 1/(λID) |
| 對應組態 | CE → CS, CB → CG, CC → CD | |

> **最大差異**：MOSFET 的閘極不吸收電流，所以沒有 rπ！輸入阻抗天生就是無窮大。

---

## 一、MOSFET 小信號參數

### 1.1 轉導 gm

$$g_m = \frac{\partial I_D}{\partial V_{GS}} \bigg|_{Q} = \frac{2I_D}{V_{GS} - V_{th}} = \frac{2I_D}{V_{OV}}$$

也可以寫成：

$$g_m = \sqrt{2 \mu_n C_{ox} \frac{W}{L} I_D} = \sqrt{2 k_n' \frac{W}{L} I_D}$$

或者：

$$g_m = k_n' \frac{W}{L} (V_{GS} - V_{th}) = k_n' \frac{W}{L} V_{OV}$$

**三種表達式各有用處**：
- 知道 ID 和 VOV → 用 gm = 2ID/VOV
- 知道 kn'(W/L) 和 ID → 用 gm = √(2kn'(W/L)ID)
- 知道 kn'(W/L) 和 VOV → 用 gm = kn'(W/L)VOV

### 1.2 輸出電阻 ro

$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### 1.3 小信號等效電路

MOSFET 的小信號模型比 BJT 更簡單：

```
    G ──────(open)────── S
              |           |
             vgs          |
              |           |
    D ──── gm·vgs ── ro ── S
```

- 閘極到源極：**斷路**（因為 IG = 0）
- 汲極到源極：受控電流源 gm·vgs 並聯 ro

### 數值例題 6.1：MOSFET 小信號參數

> **題目**：NMOS，kn'(W/L) = 2 mA/V²，ID = 0.5 mA，Vth = 0.8V，λ = 0.02V⁻¹。
> 求 gm、ro、VGS。
>
> **解答**：
> 先求 VGS：
> ID = ½ kn'(W/L)(VGS - Vth)²
> 0.5m = ½ × 2m × (VGS - 0.8)²
> (VGS - 0.8)² = 0.5 → VGS - 0.8 = 0.707 → VGS = 1.507V
> VOV = 0.707V
>
> gm = 2ID/VOV = 2 × 0.5m/0.707 = 1.414 mA/V
> 或 gm = √(2 × 2m × 0.5m) = √(2m²) = 1.414 mA/V ✓
>
> ro = 1/(λID) = 1/(0.02 × 0.5m) = 100 kΩ
>
> **結果**：gm = 1.414 mS，ro = 100 kΩ

---

## 二、共源極放大器（Common Source, CS）

### 2.1 基本 CS 放大器（最常用！）

**電路描述**：
- 輸入從閘極進入
- 輸出從汲極取出
- 源極接地

**小信號分析**：

$$A_v = -g_m (R_D \| R_L \| r_o) \approx -g_m (R_D \| R_L)$$

$$R_{in} = R_1 \| R_2 \quad (\text{因為閘極本身是斷路})$$

$$R_{out} = R_D \| r_o \approx R_D$$

**注意**：輸入阻抗只由偏壓電阻決定，MOSFET 本身不貢獻。

### 數值例題 6.2：基本 CS 放大器

> **題目**：CS 放大器，ID = 1mA，kn'(W/L) = 4mA/V²，Vth = 0.5V，λ = 0.01V⁻¹。
> RD = 5kΩ，R1 = 1MΩ，R2 = 1MΩ，RL = 10kΩ。求 Av、Rin、Rout。
>
> **解答**：
> VOV = √(2ID/[kn'(W/L)]) = √(2×1m/4m) = √0.5 = 0.707V
> gm = 2ID/VOV = 2m/0.707 = 2.83 mS
> ro = 1/(0.01 × 1m) = 100 kΩ
>
> Av = -gm(RD ∥ RL ∥ ro) = -2.83m × (5k ∥ 10k ∥ 100k)
> 5k ∥ 10k = 3.33kΩ，3.33k ∥ 100k = 3.22kΩ
> Av = -2.83m × 3.22k = **-9.11**
>
> Rin = R1 ∥ R2 = 1M ∥ 1M = **500 kΩ**
>
> Rout = RD ∥ ro = 5k ∥ 100k = **4.76 kΩ**
>
> **結果**：Av = -9.11，Rin = 500kΩ（高！），Rout = 4.76kΩ

### 2.2 含源極退化電阻 RS 的 CS 放大器

在源極加上未被旁路的 RS：

$$A_v = \frac{-g_m(R_D \| R_L)}{1 + g_m R_S}$$

當 gmRS >> 1 時：

$$A_v \approx -\frac{R_D \| R_L}{R_S}$$

$$R_{in} = R_1 \| R_2$$

$$R_{out} = R_D \| [r_o(1 + g_m R_S) + R_S] \approx R_D$$

### 數值例題 6.3：含 RS 的 CS 放大器

> **題目**：延續例題 6.2，加上 RS = 500Ω（交流未旁路），RL = ∞。求 Av。
>
> **解答**：
> Av = -gm × RD/(1 + gmRS)
> = -2.83m × 5k/(1 + 2.83m × 500)
> = -14.15/(1 + 1.415)
> = -14.15/2.415 = **-5.86**
>
> 近似值：Av ≈ -RD/RS = -5k/500 = -10
>（近似值差比較多，因為 gmRS = 1.415 不算 >> 1）
>
> 若 RS = 2kΩ：
> Av = -2.83m × 5k/(1 + 2.83m × 2k) = -14.15/6.66 = -2.12
> 近似值：-5k/2k = -2.5（更接近了）

---

## 三、共閘極放大器（Common Gate, CG）

### 3.1 電路描述

- 輸入從源極進入
- 輸出從汲極取出
- 閘極交流接地

### 3.2 小信號分析

$$A_v = g_m(R_D \| R_L \| r_o) \approx g_m(R_D \| R_L)$$

**不反相！**（與 CS 增益大小相同，但符號相反）

$$R_{in} = \frac{1}{g_m} \| r_o \approx \frac{1}{g_m}$$

**非常低的輸入阻抗**

$$R_{out} = R_D \| [r_o(1 + g_m R_S) + R_S]$$

若信號源阻抗 RS → 0：
$$R_{out} = R_D \| r_o \approx R_D$$

若 RS 存在：
$$R_{out} \approx R_D \| (g_m r_o R_S)$$

輸出電阻可以非常高。

### 3.3 CG 的特點

- 電壓增益與 CS 相同量級，但**不反相**
- **輸入阻抗很低**（1/gm，通常幾百歐姆）
- **沒有米勒效應**（閘極接地，Cgd 不會被放大）
- 適合**高頻放大**

### 數值例題 6.4：CG 放大器

> **題目**：CG 放大器，ID = 0.5mA，gm = 2mS，ro = 200kΩ，RD = 10kΩ。求 Av、Rin。
>
> **解答**：
> Av = gm × (RD ∥ ro) = 2m × (10k ∥ 200k) = 2m × 9.52k = **+19.05**
>
> Rin = 1/gm = 1/2m = **500 Ω**
>
> **結果**：增益約 19，不反相；輸入阻抗只有 500Ω

---

## 四、共汲極放大器（Common Drain, CD / Source Follower）

### 4.1 電路描述

- 輸入從閘極進入
- 輸出從源極取出
- 汲極交流接地（接 VDD）

### 4.2 小信號分析

$$A_v = \frac{g_m(R_S \| R_L \| r_o)}{1 + g_m(R_S \| R_L \| r_o)} \approx \frac{g_m R_S}{1 + g_m R_S}$$

**增益 < 1，但接近 1，不反相** → 源極跟隨器（Source Follower）

$$R_{in} = R_1 \| R_2 \quad (\text{MOSFET 閘極本身無窮大})$$

$$R_{out} = R_S \| \frac{1}{g_m} \| r_o \approx R_S \| \frac{1}{g_m}$$

**低輸出阻抗**（由 1/gm 主導）

### 4.3 CD 的用途

與 BJT 的 CC（射極跟隨器）完全相同：
- **緩衝器（Buffer）**
- **電位移位（Level Shifting）**
- **阻抗轉換**

### 數值例題 6.5：CD 放大器（源極跟隨器）

> **題目**：CD 放大器，ID = 1mA，gm = 4mS，RS = 5kΩ，RL = 1kΩ。求 Av、Rout。
>
> **解答**：
> RS ∥ RL = 5k ∥ 1k = 833Ω
> Av = gm × 833/(1 + gm × 833) = 4m × 833/(1 + 3.33) = 3.33/4.33 = **0.770**
>
> Rout = RS ∥ (1/gm) = 5k ∥ 250 = 238Ω
>
> 若只看 MOSFET 本身（不含 RS）：Rout(MOSFET) = 1/gm = **250 Ω**
>
> **結果**：Av = 0.770，Rout = 238Ω

---

## 五、三種組態完整比較

| 特性 | CS（共源極） | CG（共閘極） | CD（共汲極） |
|------|------------|------------|------------|
| 對應 BJT | CE | CB | CC |
| 電壓增益 | **-gm(RD∥RL)**，反相 | +gm(RD∥RL)，同相 | ≈1，同相 |
| 輸入阻抗 | R1∥R2（**高**） | 1/gm（**低**） | R1∥R2（**高**） |
| 輸出阻抗 | RD（中） | 高 | 1/gm（**低**） |
| 電流增益 | 高 | ≈1 | 高 |
| 頻率響應 | 受米勒效應限制 | **最好** | 好 |
| 主要用途 | 一般放大 | 高頻放大 | 緩衝器 |

### 數值例題 6.6：三種組態同條件比較

> **題目**：MOSFET 參數：ID = 1mA，gm = 4mS，ro = 50kΩ。
> 負載 RD = RS_load = 5kΩ，無外部 RL。比較三種組態的 Av。
>
> **解答**：
> CS：Av = -gm(RD∥ro) = -4m × (5k∥50k) = -4m × 4.55k = **-18.2**
> CG：Av = +gm(RD∥ro) = +4m × 4.55k = **+18.2**
> CD：Av = gm(RS∥ro)/(1+gm(RS∥ro)) = 4m×4.55k/(1+4m×4.55k) = 18.2/19.2 = **+0.948**

---

## 六、主動負載（Active Load）放大器

### 6.1 為什麼要用主動負載？

被動電阻做負載時：
$$A_v = -g_m R_D$$

要提高增益就要加大 RD，但 RD 太大會：
1. VDD 不夠大來維持飽和區
2. 浪費面積（IC 裡電阻很占面積）

**解決方案**：用 PMOS 做電流源當負載——它的**小信號等效電阻 ro 很大**，但直流壓降由 VDS 決定，不占太多電壓空間。

### 6.2 NMOS + PMOS 主動負載

NMOS 做放大管（M1），PMOS 做主動負載（M2，二極體連接或電流源連接）。

**PMOS 二極體連接負載**：

$$R_{load} = \frac{1}{g_{m2}} \| r_{o2} \approx \frac{1}{g_{m2}}$$

$$A_v = -g_{m1} \left(\frac{1}{g_{m2}} \| r_{o1}\right) \approx -\frac{g_{m1}}{g_{m2}}$$

增益受限，通常只有 -2 ~ -10 左右。

**PMOS 電流源負載**（閘極接固定偏壓）：

$$R_{load} = r_{o2}$$

$$A_v = -g_{m1}(r_{o1} \| r_{o2})$$

增益大幅提升！

### 數值例題 6.7：主動負載放大器

> **題目**：NMOS + PMOS 電流源負載放大器。
> NMOS：gm1 = 2mS，ro1 = 50kΩ
> PMOS：ro2 = 80kΩ
> 求電壓增益。
>
> **解答**：
> Av = -gm1(ro1 ∥ ro2)
> = -2m × (50k ∥ 80k)
> = -2m × 30.77k
> = **-61.5**
>
> 如果用電阻負載 RD = 5kΩ，增益只有 -2m × 5k = -10。
> 主動負載讓增益提升了 6 倍！

---

## 七、Cascode 放大器

### 7.1 基本概念

Cascode = **CS（共源極）+ CG（共閘極）的串級**

**為什麼增益更高？**

- CS 級提供高轉導 gm
- CG 級提供**極高的輸出電阻**

### 7.2 NMOS Cascode 的輸出電阻

$$R_{out} = g_{m2} r_{o2} r_{o1}$$

比單一 MOSFET 的 ro 高出 gm·ro 倍（通常 20~100 倍）！

### 7.3 Cascode 放大器的增益

搭配主動 Cascode 負載（PMOS Cascode 電流源）：

$$A_v = -g_{m1}(R_{out,n} \| R_{out,p})$$

$$A_v \approx -g_m (g_m r_o^2 \| g_m r_o^2) \approx -\frac{g_m^2 r_o^2}{2}$$

增益可達數千甚至數萬！

### 數值例題 6.8：Cascode 放大器

> **題目**：Cascode 放大器，所有 MOSFET 參數相同：
> gm = 2mS，ro = 50kΩ。NMOS Cascode + PMOS Cascode 負載。
> 求輸出電阻和電壓增益。
>
> **解答**：
> NMOS Cascode 輸出電阻：
> Rout,n = gm × ro × ro = 2m × 50k × 50k = 5 GΩ
>
> 等等，讓我們更仔細：
> Rout,n = gm2·ro2·(ro1∥(1/gm1的影響))
> 簡化：Rout,n ≈ gm·ro·ro = gm·ro² = 2m × (50k)² = 2m × 2.5G = 5 MΩ
>
> 同理 PMOS Cascode：Rout,p ≈ 5 MΩ
>
> Av = -gm1(Rout,n ∥ Rout,p) = -2m × (5M ∥ 5M) = -2m × 2.5M = **-5000**
>
> 對比單一 CS + 電流源負載：|Av| = gm(ro∥ro) = 2m × 25k = 50
> **Cascode 增益提高了 100 倍！**

### 7.4 Cascode 的代價

- **電壓裕度（Voltage Headroom）減少**：堆疊的 MOSFET 每個至少需要 VOV 的 VDS
- **頻寬**：通常更窄（增益頻寬積守恆）

### 數值例題 6.9：Cascode 的電壓裕度

> **題目**：Cascode NMOS，VOV = 0.2V，VDD = 1.8V。
> 每個 MOSFET 至少需要 VDS = VOV 才能在飽和區。
> 求輸出端的可用擺幅。
>
> **解答**：
> NMOS cascode 佔用：VDS1 + VDS2 ≥ 2VOV = 0.4V
> PMOS cascode 佔用：|VSD3| + |VSD4| ≥ 2|VOV| = 0.4V
>
> 輸出擺幅 ≈ VDD - 4VOV = 1.8 - 0.8 = **1.0V（peak-to-peak）**
>
> 對比無 cascode（只用兩個管）：
> 擺幅 = VDD - 2VOV = 1.8 - 0.4 = 1.4V
>
> **Cascode 犧牲了 0.4V 的擺幅**

---

## 八、放大器設計總結與直覺

### 8.1 如何提高電壓增益？

$$A_v = -g_m \times R_{out}$$

1. **增大 gm**：增大 W/L 或增大 ID
2. **增大 Rout**：用主動負載、Cascode
3. **多級串接**

### 8.2 增益的內在限制（Intrinsic Gain）

單一 MOSFET 能達到的最大增益（當負載是自己的 ro 時）：

$$A_0 = g_m r_o = \frac{2}{V_{OV} \lambda}$$

這被稱為 MOSFET 的**內在增益（Intrinsic Gain）**。

### 數值例題 6.10：內在增益

> **題目**：NMOS，VOV = 0.2V，λ = 0.1V⁻¹。求內在增益。
>
> **解答**：
> A0 = gm·ro = 2/(VOV·λ) = 2/(0.2 × 0.1) = **100**
>
> 若 VOV = 0.2V，λ = 0.02V⁻¹：
> A0 = 2/(0.2 × 0.02) = **500**
>
> 長通道（小λ）的 MOSFET 有更高的內在增益。

### 數值例題 6.11：完整 CS 放大器設計

> **題目**：設計一個 CS 放大器，要求 Av = -10，ID = 0.5mA，VDD = 3.3V。
> 製程：kn' = 200μA/V²，Vth = 0.5V，λ = 0.02V⁻¹。
> 使用電阻負載 RD。
>
> **解答**：
> 步驟一：選擇 VOV 和 W/L
> ID = ½kn'(W/L)VOV²
> 選 VOV = 0.3V：
> 0.5m = ½ × 200μ × (W/L) × 0.09
> W/L = 0.5m/(9μ) = 55.6 → 取 **W/L = 56**
>
> 步驟二：求 gm
> gm = 2ID/VOV = 2 × 0.5m/0.3 = 3.33 mS
>
> 步驟三：求 RD
> |Av| = gm × RD → RD = 10/3.33m = 3 kΩ
>
> 步驟四：驗證飽和區
> VD = VDD - IDRD = 3.3 - 0.5m × 3k = 3.3 - 1.5 = 1.8V
> VGS = Vth + VOV = 0.5 + 0.3 = 0.8V
> VDS = VD（假設 VS = 0）= 1.8V > VOV = 0.3V ✓ 飽和區
>
> 步驟五：驗證 ro 的影響
> ro = 1/(0.02 × 0.5m) = 100 kΩ >> RD = 3kΩ ✓ 可忽略
>
> **設計結果**：W/L = 56，RD = 3kΩ，VGS = 0.8V

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|---------|------|
| 共源極 | Common Source (CS) | 源極接地，最常用的放大組態 | 類似 BJT 的 CE |
| 共閘極 | Common Gate (CG) | 閘極交流接地 | 類似 BJT 的 CB |
| 共汲極 | Common Drain (CD) | 汲極交流接地（源極跟隨器） | 類似 BJT 的 CC |
| 源極跟隨器 | Source Follower | CD 的別名，增益≈1 | 緩衝器 |
| 主動負載 | Active Load | 用電晶體代替電阻做負載 | PMOS 電流源 |
| Cascode | Cascode | CS+CG 串級，極高增益 | 高性能 OPA 中 |
| 內在增益 | Intrinsic Gain (A0) | 單一管的最大增益 = gm·ro | 設計的天花板 |
| 源極退化 | Source Degeneration | 源極加電阻穩定增益 | 類似射極退化 |
| 電壓裕度 | Voltage Headroom | 維持飽和區所需的最小 VDS | Cascode 需要更多 |
| 米勒效應 | Miller Effect | Cgd 被增益放大 | CS 的頻寬殺手 |

---

## 題型鑑別

| 看到什麼條件 | 用什麼方法 |
|-------------|-----------|
| 「CS 放大器、求增益」 | Av = -gm(RD∥RL)，注意負號 |
| 「含 RS、未旁路」 | Av = -gm(RD∥RL)/(1+gmRS) |
| 「CG 放大器」 | Av = +gm(RD∥RL)，Rin ≈ 1/gm |
| 「CD / 源極跟隨器」 | Av ≈ 1，Rout ≈ 1/gm |
| 「主動負載」 | 把 PMOS 的 ro 或 1/gm 代入負載 |
| 「Cascode」 | Rout ≈ gm·ro²，增益 ≈ gm·(gm·ro²∥...) |
| 「求內在增益」 | A0 = gm·ro = 2/(VOV·λ) |
| 「設計放大器」 | 由規格反推 gm → W/L → RD |

---

## ✅ 自我檢測

### 概念題

1. MOSFET 小信號模型和 BJT 最大的差別是什麼？
2. CS 放大器是反相還是同相？為什麼？
3. 為什麼主動負載可以提高增益？
4. Cascode 放大器的核心優勢是什麼？代價是什麼？
5. 源極跟隨器的電壓增益接近多少？為什麼還是有用？

<details>
<summary>點擊查看答案</summary>

1. **MOSFET 沒有 rπ。** BJT 有有限的 rπ = β/gm，但 MOSFET 閘極不吸收電流，等效輸入阻抗無窮大。因此 MOSFET 的小信號模型更簡單。

2. **反相。** 因為 VGS 增大 → ID 增大 → VRD = ID·RD 增大 → VO = VDD - ID·RD 減小。輸入增大導致輸出減小。

3. **因為主動負載（如 PMOS 電流源）的小信號等效電阻 ro 遠大於一般的電阻 RD。** 增益 = -gm × Rload，更大的 Rload 就有更大的增益。而且電流源在直流只佔用很小的 VDS 壓降。

4. **優勢：極高的輸出電阻（gm·ro²），因此增益極高。代價：佔用更多電壓裕度（每個堆疊的管至少需要 VOV），限制了輸出擺幅。**

5. **增益接近 1。** 但它非常有用，因為它提供**高輸入阻抗**和**低輸出阻抗**，可以做為緩衝器，在高阻抗源和低阻抗負載之間做阻抗匹配。

</details>

### 計算題

6. NMOS，ID = 2mA，kn'(W/L) = 8mA/V²，λ = 0.05V⁻¹。求 gm 和 ro。
7. CS 放大器，gm = 5mS，RD = 10kΩ，RL = 10kΩ。求 Av。
8. 上題加 RS = 1kΩ（未旁路），求新的 Av。
9. CD 放大器，gm = 3mS，RS = 2kΩ，RL = 500Ω。求 Av 和 Rout。
10. Cascode NMOS，gm = 2mS，ro = 100kΩ。求 Rout。
11. 若用上題的 Cascode 加上相同參數的 PMOS Cascode 負載，求 |Av|。

<details>
<summary>點擊查看答案</summary>

6. VOV = √(2×2m/8m) = √0.5 = 0.707V
   gm = 2×2m/0.707 = 5.66 mS
   ro = 1/(0.05×2m) = 10 kΩ

7. Av = -5m × (10k∥10k) = -5m × 5k = -25

8. Av = -5m×5k/(1+5m×1k) = -25/6 = -4.17

9. RS∥RL = 2k∥500 = 400Ω
   Av = 3m×400/(1+3m×400) = 1.2/2.2 = 0.545
   Rout = RS∥(1/gm) = 2k∥333 = 286Ω

10. Rout = gm·ro² = 2m × (100k)² = 2m × 10¹⁰ = 20 MΩ

11. Rout,p = 20MΩ（相同）
    |Av| = gm × (Rout,n∥Rout,p) = 2m × (20M∥20M) = 2m × 10M = 20,000

</details>

---

> **下一篇**：[electronics_07_差動放大器](electronics_07_差動放大器.md) — 學習現代 OPA 的核心結構！
