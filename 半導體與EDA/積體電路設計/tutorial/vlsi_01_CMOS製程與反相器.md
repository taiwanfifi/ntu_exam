# VLSI 教學講義 第一章：CMOS 製程與反相器

> **適用對象**：零基礎入門，電機/電子系大學部至研究所
> **重要度**：CMOS 反相器是所有 VLSI 設計的基石，TSMC/MTK 面試必考

---

## 🔰 本章基礎觀念（零基礎必讀）

### IC 設計為什麼重要？——從沙子到晶片的旅程

你手上的手機裡藏著一顆小小的晶片，它包含了**數十億個電晶體**。這些電晶體是怎麼來的？

1. **矽（Silicon, Si）** 是地球上第二豐富的元素，主要存在於沙子裡
2. 沙子經過提煉，變成純度高達 99.999999999%（11 個 9）的**單晶矽棒（Ingot）**
3. 矽棒被切成薄薄的**晶圓（Wafer）**，直徑通常是 300mm（12 吋）
4. 在晶圓上，透過**光刻（Lithography）**、**蝕刻（Etching）**、**離子佈植（Ion Implantation）** 等步驟，製造出電晶體
5. 最後切割、封裝，就變成你看到的晶片

> **一句話記憶**：IC 設計 = 用數十億個微小開關（電晶體）組合出能運算的電路

### 為什麼學 CMOS？

| 特性 | CMOS 的優勢 |
|------|------------|
| 靜態功耗 | 幾乎為零（理想情況） |
| 雜訊邊限 | 大（抗干擾能力強） |
| 輸出擺幅 | 完全從 0 到 VDD（Rail-to-Rail） |
| 製程成熟度 | 全世界 95% 以上的晶片都是 CMOS |

---

## 一、CMOS 製程概述

### 1.1 什麼是 CMOS？

**CMOS = Complementary Metal-Oxide-Semiconductor**（互補式金屬氧化物半導體）

「互補」的意思是：同時使用 **NMOS** 和 **PMOS** 兩種電晶體來構成電路。

### 1.2 井（Well）製程

要在同一片矽基板上同時製作 NMOS 和 PMOS，需要用「井」來隔離：

#### (a) N-well 製程
- **基板（Substrate）**：P 型矽
- NMOS 直接做在 P 型基板上
- PMOS 做在 **N-well**（N 型井）裡
- **最常見**的製程方式

```
    PMOS (在 N-well 中)        NMOS (在 P-substrate 上)
   ┌───────────────────┐     ┌───────────────────┐
   │   S    G    D     │     │   S    G    D     │
   │   │    │    │     │     │   │    │    │     │
   │  p+   ║   p+     │     │  n+   ║   n+     │
   │  ╔════╬════╗     │     │  ╔════╬════╗     │
   │  ║ N-well  ║     │     │  ║P-substrate║    │
   └──╚═════════╝─────┘     └──╚═════════╝─────┘
```

#### (b) P-well 製程
- **基板**：N 型矽
- PMOS 直接做在 N 型基板上
- NMOS 做在 **P-well**（P 型井）裡

#### (c) Twin-well（雙井）製程
- 在輕摻雜基板上，**同時**製作 N-well 和 P-well
- 可以分別最佳化 NMOS 和 PMOS 的參數
- **先進製程多採用此方式**

### 1.3 製程步驟簡要流程

```
氧化 → 光阻塗佈 → 曝光 → 顯影 → 蝕刻 → 離子佈植 → 金屬化 → ...
```

每一層都需要一張**光罩（Mask）**，一個完整製程可能需要 30~50 張光罩。

---

## 二、NMOS / PMOS 結構複習

### 2.1 NMOS 電晶體

```
         閘極 (Gate, G)
           │
     ══════╪══════  ← 閘極氧化層 (Gate Oxide)
     ┌─────┴─────┐
  n+ │           │ n+
  源極(S)      汲極(D)
     └───────────┘
      P-type 基板
           │
        基體 (Body, B)
```

**NMOS 開啟條件**：VGS > Vtn（N 通道閾值電壓，通常 Vtn ≈ 0.3~0.7V）

| 區域 | 條件 | 電流 IDS |
|------|------|---------|
| 截止區（Cutoff） | VGS < Vtn | IDS ≈ 0 |
| 線性區（Linear/Triode） | VGS > Vtn 且 VDS < VGS - Vtn | IDS = μnCox(W/L)[(VGS-Vtn)VDS - VDS²/2] |
| 飽和區（Saturation） | VGS > Vtn 且 VDS ≥ VGS - Vtn | IDS = (μnCox/2)(W/L)(VGS-Vtn)² |

### 2.2 PMOS 電晶體

PMOS 和 NMOS **互補**：
- 通道載子：電洞（Hole），移動率較低
- **開啟條件**：VGS < Vtp（Vtp 為負值，通常 Vtp ≈ -0.3~-0.7V）
- 電流方向：從源極流向汲極（源極接 VDD）

> **關鍵差異**：在相同尺寸下，PMOS 的電流驅動能力約為 NMOS 的 **1/2 ~ 1/3**，
> 因為電洞移動率（μp）約為電子移動率（μn）的一半。

### 2.3 電晶體參數速查

| 參數 | 符號 | 典型值（45nm 製程） |
|------|------|-------------------|
| 閾值電壓（NMOS） | Vtn | ~0.4V |
| 閾值電壓（PMOS） | Vtp | ~-0.4V |
| 電子移動率 | μn | ~300 cm²/V·s |
| 電洞移動率 | μp | ~100 cm²/V·s |
| 閘極氧化層電容 | Cox | ~15 fF/μm² |
| 供應電壓 | VDD | ~1.0V |

---

## 三、CMOS 反相器：核心中的核心

### 3.1 電路結構：PMOS 上拉 + NMOS 下拉

```
        VDD
         │
    ┌────┤
    │  ┌─┴─┐
    │  │   │ PMOS (上拉, Pull-Up)
    │  └─┬─┘
    │    │
Vin ─────┤──── Vout
    │    │
    │  ┌─┴─┐
    │  │   │ NMOS (下拉, Pull-Down)
    │  └─┬─┘
    └────┤
         │
        GND
```

**工作原理**（記住這個就夠了！）：

| Vin | NMOS 狀態 | PMOS 狀態 | Vout |
|-----|----------|----------|------|
| 0（Low） | OFF | ON | VDD（High） |
| VDD（High） | ON | OFF | 0（Low） |

> **核心重點**：任何時刻，NMOS 和 PMOS **只有一個導通**，所以：
> - **沒有穩態電流**（靜態功耗 ≈ 0）
> - **輸出完整擺幅**：0 到 VDD

### 3.2 VTC（Voltage Transfer Characteristic）曲線

VTC 是反相器最重要的特性曲線，描述 **Vout 對 Vin 的關係**。

```
Vout
 ^
VDD ┤━━━━━━┓
 │        ┃
 │        ┃    ← 轉態區（Transition Region）
 │        ┃
VDD/2 ┤ · · · ·╋· · · · · ← VM（開關閾值）
 │          ┃
 │          ┃
 │          ┃
 0 ┤          ┗━━━━━━
 └──┬──┬──┬──┬──┬──→ Vin
    0 VIL VM VIH VDD
```

### 3.3 VTC 的五個區域

這是考試重點，必須理解每個區域的電晶體狀態：

| 區域 | Vin 範圍 | NMOS | PMOS | Vout |
|------|---------|------|------|------|
| 1 | 0 ≤ Vin < Vtn | 截止 | 線性 | VDD |
| 2 | Vtn ≤ Vin < VM | 飽和 | 線性 | 高（下降中） |
| 3 | Vin = VM | 飽和 | 飽和 | VM |
| 4 | VM < Vin ≤ VDD+Vtp | 線性 | 飽和 | 低（下降中） |
| 5 | VDD+Vtp < Vin ≤ VDD | 線性 | 截止 | 0 |

> **記憶技巧**：
> - 區域 1 和 5：一個 OFF 一個 ON → 輸出為固定值
> - 區域 2 和 4：一個飽和一個線性 → 轉態中
> - 區域 3：兩個都飽和 → **開關閾值點**

### 3.4 開關閾值 VM 推導

**定義**：VM 是 VTC 曲線上 Vout = Vin 的點。

在 VM 點，NMOS 和 PMOS 都在**飽和區**，令兩者電流相等：

**IDn = IDp**

```
(μnCox/2)(Wn/Ln)(VM - Vtn)² = (μpCox/2)(Wp/Lp)(VDD - VM + Vtp)²
```

其中 Vtp 為負值，所以 VDD - VM + Vtp = VDD - VM - |Vtp|

定義 **β ratio**：

```
r = βp/βn = (μpCox·Wp/Lp) / (μnCox·Wn/Ln) = kp(Wp/Lp) / [kn(Wn/Ln)]
```

假設 |Vtn| = |Vtp| = Vt，解出 VM：

```
        Vtn + √r · (VDD + Vtp)
VM = ─────────────────────────
            1 + √r
```

> **當 r = 1（即 βp = βn）且 |Vtn| = |Vtp| 時**：
> **VM = VDD / 2**（完美對稱的反相器）

### 3.5 雜訊邊限（Noise Margin）

雜訊邊限衡量電路**抵抗雜訊干擾**的能力。

#### 定義四個關鍵電壓

| 符號 | 定義 | 圖形上的位置 |
|------|------|------------|
| VOH | 輸出高電壓（Output High） | VTC 左端平坦處 = VDD |
| VOL | 輸出低電壓（Output Low） | VTC 右端平坦處 = 0 |
| VIH | 輸入高電壓（Input High） | VTC 斜率 = -1 的右側點 |
| VIL | 輸入低電壓（Input Low） | VTC 斜率 = -1 的左側點 |

#### 雜訊邊限公式

```
NMH = VOH - VIH    （高態雜訊邊限）
NML = VIL - VOL    （低態雜訊邊限）
```

```
        VOH ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
            │                                     │ NMH = VOH - VIH
        VIH ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
            │           ←不確定區域→
        VIL ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
            │                                     │ NML = VIL - VOL
        VOL ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

> **理想 CMOS 反相器**（VOH=VDD, VOL=0, 對稱）：NMH = NML = VDD/2

### 3.6 Beta Ratio 設計（使 VM = VDD/2）

**目標**：設計對稱的反相器，使開關閾值在 VDD/2。

因為 μn ≈ 2~3 × μp，所以 PMOS 要比 NMOS **寬**才能補償。

**設計準則**：

```
βp = βn
⟹ μp·Cox·(Wp/Lp) = μn·Cox·(Wn/Ln)
⟹ Wp/Lp = (μn/μp) · (Wn/Ln)
```

若 μn/μp ≈ 2.5，且 Ln = Lp = Lmin：

```
Wp ≈ 2.5 × Wn
```

> **實務上**：TSMC 的 PDK 通常建議 **Wp/Wn ≈ 2~3**

---

## 四、關鍵術語表

| 英文 | 中文 | 說明 |
|------|------|------|
| CMOS | 互補式金屬氧化物半導體 | 同時使用 NMOS + PMOS |
| Inverter | 反相器 | 最基本的邏輯閘 |
| VTC | 電壓轉移特性 | Vout vs Vin 曲線 |
| Switching Threshold (VM) | 開關閾值 | Vout = Vin 的點 |
| Noise Margin | 雜訊邊限 | 抵抗雜訊的能力 |
| NMH | 高態雜訊邊限 | VOH - VIH |
| NML | 低態雜訊邊限 | VIL - VOL |
| N-well | N 型井 | 在 P 基板上做的 N 區域 |
| Threshold Voltage (Vt) | 閾值電壓 | 電晶體開啟的最低 VGS |
| Rail-to-Rail | 全擺幅 | 輸出從 0 到 VDD |
| Pull-Up Network (PUN) | 上拉網路 | PMOS 組成，輸出拉高 |
| Pull-Down Network (PDN) | 下拉網路 | NMOS 組成，輸出拉低 |
| Saturation | 飽和區 | VDS ≥ VGS - Vt |
| Linear/Triode | 線性/三極區 | VDS < VGS - Vt |
| Beta Ratio | Beta 比值 | βp/βn，決定 VM 位置 |

---

## 五、數值例題

### 例題 1：判斷電晶體工作區域

**題目**：一個 NMOS 電晶體，Vtn = 0.5V。若 VGS = 1.8V，VDS = 0.8V，該電晶體在哪個工作區域？

**解答**：
1. 檢查是否導通：VGS = 1.8V > Vtn = 0.5V → **導通**
2. 計算 VGS - Vtn = 1.8 - 0.5 = 1.3V
3. 比較 VDS 與 VGS - Vtn：VDS = 0.8V < 1.3V
4. **結論：線性區（Linear Region）**

---

### 例題 2：CMOS 反相器開關閾值

**題目**：一個 CMOS 反相器，VDD = 1.8V，Vtn = 0.4V，Vtp = -0.4V，μnCox = 200 μA/V²，μpCox = 80 μA/V²，Wn/Ln = 2，Wp/Lp = 5。求 VM。

**解答**：
1. 計算 r = βp/βn = (μpCox · Wp/Lp) / (μnCox · Wn/Ln)
   - βp = 80 × 5 = 400 μA/V²
   - βn = 200 × 2 = 400 μA/V²
   - r = 400/400 = 1

2. 由於 |Vtn| = |Vtp| = 0.4V 且 r = 1：
   ```
   VM = (Vtn + √r · (VDD + Vtp)) / (1 + √r)
      = (0.4 + 1 × (1.8 - 0.4)) / (1 + 1)
      = (0.4 + 1.4) / 2
      = 0.9V = VDD/2 ✓
   ```

3. **答：VM = 0.9V = VDD/2**（完美對稱）

---

### 例題 3：雜訊邊限計算

**題目**：一個 CMOS 反相器，VDD = 3.3V，VOH = 3.3V，VOL = 0V，VIH = 1.8V，VIL = 1.2V。求 NMH 和 NML。

**解答**：
```
NMH = VOH - VIH = 3.3 - 1.8 = 1.5V
NML = VIL - VOL = 1.2 - 0 = 1.2V
```

**答：NMH = 1.5V，NML = 1.2V**

> 分析：NMH > NML，表示此反相器對高態的抗雜訊能力較強。
> NML 較小意味著低態輸入更容易受到干擾。

---

### 例題 4：設計對稱反相器

**題目**：製程參數 μn/μp = 3，Ln = Lp = 90nm，Wn = 270nm。為使 VM = VDD/2，求 Wp。

**解答**：
1. 對稱條件：βp = βn
   ```
   μpCox · (Wp/Lp) = μnCox · (Wn/Ln)
   ```
2. Cox 相消，整理得：
   ```
   Wp/Lp = (μn/μp) · (Wn/Ln)
   Wp/90nm = 3 × (270nm/90nm)
   Wp/90nm = 3 × 3 = 9
   Wp = 810nm
   ```

**答：Wp = 810nm（PMOS 寬度是 NMOS 的 3 倍）**

---

### 例題 5：VTC 區域判斷

**題目**：CMOS 反相器，VDD = 1.0V，Vtn = 0.3V，Vtp = -0.3V。當 Vin = 0.2V 時：
(a) NMOS 和 PMOS 各在什麼狀態？
(b) Vout 是多少？

**解答**：
(a)
- **NMOS**：VGS = Vin = 0.2V < Vtn = 0.3V → **截止（OFF）**
- **PMOS**：VGS = Vin - VDD = 0.2 - 1.0 = -0.8V < Vtp = -0.3V → **導通**
  - VSG = 0.8V > |Vtp| = 0.3V → **ON**
  - VSD = VDD - Vout = 1.0 - Vout
  - 由於 NMOS 截止，無電流通路，Vout 被 PMOS 拉到 VDD

(b) **Vout = VDD = 1.0V**

> 這是 VTC 的**區域 1**（Vin < Vtn）

---

### 例題 6：非對稱反相器的 VM

**題目**：若 Wp/Wn = 1（即 PMOS 和 NMOS 寬度相同），μn/μp = 2，VDD = 1.8V，Vtn = |Vtp| = 0.4V。求 VM。

**解答**：
1. r = βp/βn = (μpCox · Wp/Lp) / (μnCox · Wn/Ln) = μp/μn = 1/2 = 0.5

2. 代入公式：
   ```
   VM = (Vtn + √r · (VDD + Vtp)) / (1 + √r)
      = (0.4 + √0.5 × (1.8 - 0.4)) / (1 + √0.5)
      = (0.4 + 0.707 × 1.4) / (1 + 0.707)
      = (0.4 + 0.99) / 1.707
      = 1.39 / 1.707
      = 0.814V
   ```

3. **答：VM ≈ 0.81V**（小於 VDD/2 = 0.9V）

> 分析：PMOS 太弱（寬度不夠），無法把 VM 拉到中間，VM 偏低。

---

## 六、題型鑑別表

| 題目特徵 | 題型 | 關鍵公式/方法 |
|---------|------|-------------|
| 給 VGS、VDS，問工作區域 | 電晶體區域判斷 | 比較 VDS 與 VGS-Vt |
| 給尺寸、μ，求 VM | 開關閾值計算 | VM 公式（令 IDn = IDp） |
| 給 VOH/VOL/VIH/VIL | 雜訊邊限 | NMH = VOH-VIH, NML = VIL-VOL |
| 求 Wp 使 VM = VDD/2 | 對稱反相器設計 | βp = βn → Wp = (μn/μp)·Wn |
| 給 Vin，問 Vout | VTC 分析 | 判斷五個區域 |
| 比較不同反相器 | 設計權衡 | r 值改變 → VM 移動方向 |

---

## ✅ 自我檢測

### Q1：CMOS 反相器中，為什麼 PMOS 通常比 NMOS 寬？

<details>
<summary>點擊展開答案</summary>

因為電洞移動率（μp）約為電子移動率（μn）的 1/2~1/3。為了使 PMOS 和 NMOS 的驅動能力匹配（βp = βn），需要增加 PMOS 的寬度（W）來補償較低的移動率。

具體來說：Wp/Wn ≈ μn/μp ≈ 2~3

這樣才能使開關閾值 VM = VDD/2，獲得對稱的 VTC 曲線。
</details>

### Q2：CMOS 反相器的靜態功耗為什麼幾乎為零？

<details>
<summary>點擊展開答案</summary>

在穩態時，NMOS 和 PMOS **不會同時導通**：
- 輸入為 High：NMOS ON、PMOS OFF → 無從 VDD 到 GND 的通路
- 輸入為 Low：NMOS OFF、PMOS ON → 無從 VDD 到 GND 的通路

由於沒有穩態電流路徑，所以理想情況下靜態功耗為零。
（實際上有微小的漏電流，尤其在先進製程中漏電功耗不可忽略）
</details>

### Q3：如果將 VM 設計得偏高（VM > VDD/2），對電路有什麼影響？

<details>
<summary>點擊展開答案</summary>

VM > VDD/2 意味著：
- **PMOS 比 NMOS 強**（βp > βn 或 r > 1）
- 影響：
  - **NMH 增大**：高態更不容易被干擾
  - **NML 減小**：低態更容易被干擾
  - **tpLH < tpHL**：上升較快、下降較慢（PMOS 強 → 充電快）

這種設計可能在需要更好高態雜訊邊限的場合有用，但犧牲了對稱性。
</details>

### Q4：請畫出 CMOS 反相器 VTC 的五個區域，標出 VM、VIL、VIH。

<details>
<summary>點擊展開答案</summary>

```
Vout
 ^
VDD ┤━━━━━━┓                 區域1: Vin<Vtn, NMOS截止, Vout=VDD
    │  ①  ┃②                區域2: NMOS飽和, PMOS線性, 轉態中
    │      ┃   ← VIL         區域3: 兩者飽和, Vin=Vout=VM
VM  ┤ · · · ·③· ·            區域4: NMOS線性, PMOS飽和, 轉態中
    │        ┃  ← VIH        區域5: PMOS截止, Vout=0
    │       ④┃
  0 ┤        ┗━━━━━━ ⑤
    └──┬──┬──┬──┬──┬──→ Vin
       0 VIL VM VIH VDD
```

- VIL 和 VIH 是 VTC 斜率 = -1 的兩個點
- VM 是 Vout = Vin 的交叉點
</details>

### Q5：N-well 製程和 Twin-well 製程各有什麼優缺點？

<details>
<summary>點擊展開答案</summary>

**N-well 製程**：
- 優點：製程步驟較少、成本較低
- 缺點：NMOS 和 PMOS 無法分別最佳化（NMOS 直接在基板上）

**Twin-well 製程**：
- 優點：NMOS 和 PMOS 各在自己的井中，可分別最佳化；Latch-up 抗性更好
- 缺點：製程步驟多、成本較高

先進製程（如 TSMC 7nm 以下）幾乎都使用 Twin-well 或更先進的技術。
</details>

---

> **下一章預告**：第二章將深入探討 CMOS 反相器的**動態特性**——傳播延遲和功率消耗，這是 IC 設計中最重要的效能指標。
