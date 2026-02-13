# VLSI 教學講義 第三章：CMOS 組合邏輯設計

> **適用對象**：零基礎入門，電機/電子系大學部至研究所
> **重要度**：CMOS 邏輯閘設計是數位 IC 設計的基礎，面試必考

---

## 🔰 本章基礎觀念（零基礎必讀）

### 從反相器到邏輯閘

上兩章我們學了 CMOS 反相器（NOT 閘），但計算需要更多邏輯功能：AND、OR、NAND、NOR……

**核心觀念**：CMOS 邏輯閘都遵循同一個架構：

```
         VDD
          │
    ┌─────┤
    │   PUN (PMOS 上拉網路)
    │     │
    │─────┤──── Vout
    │     │
    │   PDN (NMOS 下拉網路)
    │     │
    └─────┤
          │
         GND
```

- **PDN（Pull-Down Network）**：用 NMOS 組成，實現邏輯函數 F
- **PUN（Pull-Up Network）**：用 PMOS 組成，實現 F 的互補（$\overline{F}$）
- 任何時刻，**只有 PUN 或 PDN 導通**（不會同時導通）

---

## 一、CMOS 邏輯設計原則

### 1.1 NMOS 和 PMOS 的邏輯對應

這是最核心的概念，必須牢記：

#### NMOS（下拉網路 PDN）：

| 連接方式 | 邏輯功能 | 記憶口訣 |
|---------|---------|---------|
| **串聯（Series）** | **AND** | 串＝全通才通 |
| **並聯（Parallel）** | **OR** | 並＝有一個通就通 |

#### PMOS（上拉網路 PUN）：

PMOS 實現的是 **PDN 的互補函數**，根據 DeMorgan 定律：

| PDN 連接 | PUN 連接 | 原因（DeMorgan） |
|---------|---------|----------------|
| NMOS 串聯（AND） | PMOS **並聯** | $\overline{A \cdot B} = \overline{A} + \overline{B}$ |
| NMOS 並聯（OR） | PMOS **串聯** | $\overline{A + B} = \overline{A} \cdot \overline{B}$ |

> **黃金法則**：PDN 和 PUN 互為**拓撲互補**（Topological Complement）
> - PDN 串聯 ↔ PUN 並聯
> - PDN 並聯 ↔ PUN 串聯

### 1.2 為什麼 CMOS 邏輯只能直接實現反相函數？

注意到 PUN 是 PDN 的互補，所以：
- 當 PDN 導通（F = 1），PUN 不導通 → Vout = 0（Low）
- 當 PDN 不導通（F = 0），PUN 導通 → Vout = VDD（High）

**輸出 = NOT(F) = $\overline{F}$**

所以 CMOS 只能直接實現 **NAND、NOR、AOI、OAI** 等**反相（Inverting）函數**。
要實現 AND、OR，需要額外加一個反相器。

---

## 二、基本閘設計

### 2.1 NAND 閘（NMOS 串聯 + PMOS 並聯）

**功能**：Y = $\overline{A \cdot B}$ = NAND(A, B)

```
        VDD          VDD
         │            │
    ┌────┤       ┌────┤
    │  ┌─┴─┐    │  ┌─┴─┐
  A─┤  │ P1│  B─┤  │ P2│     PMOS 並聯
    │  └─┬─┘    │  └─┬─┘     → 任一輸入為 0，輸出拉高
    │    │       │    │
    └────┴───┬───┴────┘
             │
             ├──── Y (Output)
             │
           ┌─┴─┐
         A─┤ N1│                NMOS 串聯
           └─┬─┘                → 兩個輸入都為 1，輸出拉低
           ┌─┴─┐
         B─┤ N2│
           └─┬─┘
             │
            GND
```

**真值表**：

| A | B | N1 | N2 | PDN | PUN | Y |
|---|---|----|----|-----|-----|---|
| 0 | 0 | OFF | OFF | OFF | ON | 1 |
| 0 | 1 | OFF | ON | OFF | ON | 1 |
| 1 | 0 | ON | OFF | OFF | ON | 1 |
| 1 | 1 | ON | ON | ON | OFF | 0 |

### 2.2 NOR 閘（NMOS 並聯 + PMOS 串聯）

**功能**：Y = $\overline{A + B}$ = NOR(A, B)

```
        VDD
         │
    ┌────┤
    │  ┌─┴─┐
  A─┤  │ P1│     PMOS 串聯
    │  └─┬─┘     → 兩個輸入都為 0，輸出拉高
    │  ┌─┴─┐
  B─┤  │ P2│
    │  └─┬─┘
    │    │
    └────┤──── Y (Output)
         │
    ┌────┴────┐
  ┌─┴─┐    ┌─┴─┐
A─┤ N1│  B─┤ N2│    NMOS 並聯
  └─┬─┘    └─┬─┘    → 任一輸入為 1，輸出拉低
    └────┬────┘
         │
        GND
```

**真值表**：

| A | B | PDN | PUN | Y |
|---|---|-----|-----|---|
| 0 | 0 | OFF | ON | 1 |
| 0 | 1 | ON | OFF | 0 |
| 1 | 0 | ON | OFF | 0 |
| 1 | 1 | ON | OFF | 0 |

### 2.3 NAND vs NOR 比較

| 特性 | NAND | NOR |
|------|------|-----|
| NMOS 連接 | 串聯 | 並聯 |
| PMOS 連接 | 並聯 | 串聯 |
| 速度（相同尺寸） | **較快** | 較慢 |
| 面積（相同驅動力） | **較小** | 較大 |
| 偏好 | **NAND 是首選** | 盡量避免多輸入 NOR |

> **為什麼 NAND 比 NOR 好？**
> - NAND 的串聯在 NMOS（速度快的那邊），並聯在 PMOS
> - NOR 的串聯在 PMOS（速度慢的那邊），要補償需要更大的 PMOS
> - 所以實務上，**NAND 閘是 CMOS 的基本建構單元**

---

## 三、複雜閘：AOI 和 OAI

### 3.1 AOI（AND-OR-Invert）

**功能**：Y = $\overline{A \cdot B + C \cdot D}$

**PDN（NMOS）**：

```
    ┌───────┬───────┐
  ┌─┴─┐  ┌─┴─┐
A─┤ N1│C─┤ N3│      兩組串聯（AND），再並聯（OR）
  └─┬─┘  └─┬─┘
  ┌─┴─┐  ┌─┴─┐
B─┤ N2│D─┤ N4│
  └─┬─┘  └─┬─┘
    └───────┴───────→ GND
```

**PUN（PMOS）**：拓撲互補

```
VDD
 │
┌┴──────────────┐
│  P1(A)  P3(C) │     兩組並聯（OR的互補），再串聯（AND的互補）
│  P2(B)  P4(D) │
└┬──────────────┘
 │
 ├──→ Y
```

更明確地說：
- (P1 並聯 P2) **串聯** (P3 並聯 P4)
- P1 接 A，P2 接 B，P3 接 C，P4 接 D

### 3.2 OAI（OR-AND-Invert）

**功能**：Y = $\overline{(A + B) \cdot (C + D)}$

**PDN（NMOS）**：兩組並聯（OR），再串聯（AND）

```
    ┌───┬───┐
  ┌─┴─┐ ┌─┴─┐
A─┤N1 │B┤N2 │    並聯（OR）
  └─┬─┘ └─┬─┘
    └──┬───┘
    ┌──┴───┐
  ┌─┴─┐ ┌─┴─┐
C─┤N3 │D┤N4 │    並聯（OR）
  └─┬─┘ └─┬─┘
    └──┬───┘
       │
      GND
```

**PUN（PMOS）**：拓撲互補
- (P1 串聯 P2) **並聯** (P3 串聯 P4)

### 3.3 AOI/OAI 的優點

| 優點 | 說明 |
|------|------|
| 電晶體少 | 一個 AOI22 只需 8 個電晶體（vs 用基本閘要更多） |
| 速度快 | 只有一級延遲（vs 多級串接） |
| 面積小 | 適合標準元件庫 |

---

## 四、電晶體尺寸設計：等效電阻法

### 4.1 問題描述

串聯的電晶體，等效電阻會**疊加**，導致延遲增大。如何調整尺寸使延遲合理？

### 4.2 串聯電阻疊加

假設最小 NMOS（W/L = 1）的等效電阻為 R：

| 連接方式 | 等效電阻 |
|---------|---------|
| 單一 NMOS (W/L = 1) | R |
| 2 個 NMOS 串聯 (W/L = 1) | 2R |
| N 個 NMOS 串聯 (W/L = 1) | NR |
| 2 個 NMOS 並聯 (W/L = 1) | R/2 |

### 4.3 尺寸設計原則

**目標**：使每個閘的**最差路徑等效電阻**等於反相器的等效電阻。

#### 2-input NAND 閘：

PDN 有 2 個 NMOS 串聯：最差電阻 = 2Rn

**解法**：將每個 NMOS 的 W/L 加倍（W = 2Wmin），使等效電阻回到 Rn。

PUN 有 2 個 PMOS 並聯：最差電阻 = Rp（單一 PMOS 即可）

```
2-input NAND 尺寸：
- NMOS: W = 2 × Wn_min（串聯補償）
- PMOS: W = Wp_min（並聯不需補償）
```

#### 2-input NOR 閘：

PDN 有 2 個 NMOS 並聯：不需補償

PUN 有 2 個 PMOS 串聯：每個 PMOS 的 W 要加倍

```
2-input NOR 尺寸：
- NMOS: W = Wn_min
- PMOS: W = 2 × Wp_min（串聯補償）
```

> **這就是 NOR 閘面積更大的原因**：PMOS 本來就比 NMOS 大，還要加倍！

### 4.4 N-input 閘的尺寸

| 閘型 | NMOS 寬度 | PMOS 寬度 | 電晶體數 |
|------|----------|----------|---------|
| N-input NAND | N × Wn | Wp | 2N |
| N-input NOR | Wn | N × Wp | 2N |
| 反相器 | Wn | Wp | 2 |

---

## 五、扇入（Fan-in）對延遲的影響

### 5.1 什麼是扇入？

**扇入（Fan-in）** = 一個邏輯閘的**輸入數目**。

### 5.2 扇入增加的影響

以 N-input NAND 為例：

```
延遲增加來源：
1. 串聯電阻增加：N 個 NMOS 串聯 → 等效電阻 ∝ N
2. 寄生電容增加：每個電晶體都有擴散電容
3. 即使加寬電晶體補償電阻，面積和電容也增大
```

**經驗法則**：
- 扇入 ≤ 4：延遲增加可接受
- 扇入 > 4：應該分解成多級

```
例：8-input NAND
方案 A（直接實現）：8 個 NMOS 串聯 → 非常慢
方案 B（分解）：2 級 × 4-input NAND + 1 個 NAND → 快得多
```

### 5.3 延遲與扇入的關係

對於 N-input NAND（經過尺寸補償後）：

```
tpd(N-input NAND) ≈ tpd(INV) × N × (1 + N/4)
```

> **實務建議**：高扇入閘應拆解成**多級低扇入閘**的組合

---

## 六、邏輯效能（Logical Effort）方法簡介

### 6.1 動機

我們需要一個**系統化方法**來最佳化多級邏輯電路的延遲。

### 6.2 基本定義

**邏輯效能（Logical Effort, g）**：衡量一個閘相比反相器，**實現同樣驅動能力需要多大的輸入電容**。

```
g = (閘的輸入電容) / (等效反相器的輸入電容)
    （在提供相同輸出電流的前提下）
```

| 閘型 | 邏輯效能 g |
|------|----------|
| 反相器（Inverter） | 1 |
| 2-input NAND | 4/3 ≈ 1.33 |
| 3-input NAND | 5/3 ≈ 1.67 |
| 2-input NOR | 5/3 ≈ 1.67 |
| 3-input NOR | 7/3 ≈ 2.33 |

> **g 越大，這個閘越「笨重」**，需要更大的輸入電容才能達到和反相器相同的速度。

### 6.3 電氣效能（Electrical Effort, h）

```
h = Cout / Cin = 扇出的電容 / 閘的輸入電容
```

### 6.4 級效能（Stage Effort, f）

```
f = g × h（每一級的效能）
```

### 6.5 路徑效能與最佳化

對於 N 級串接的路徑：

```
路徑效能 F = G × B × H

其中：
G = g₁ × g₂ × ... × gN    （路徑邏輯效能）
B = 分支因子的乘積         （Branching Effort）
H = Cout_path / Cin_path    （路徑電氣效能）
```

**最佳化定理**：當每一級的 f 相等時，總延遲最小：

```
f_opt = F^(1/N)
最小延遲 = N × (F^(1/N)) + P（寄生延遲）
```

**最佳級數**：

```
N_opt ≈ ln(F) / ln(ρ)    其中 ρ ≈ 3.6（經驗值）
```

---

## 七、其他邏輯族

### 7.1 偽 NMOS（Pseudo-NMOS）

```
      VDD
       │
     ┌─┴─┐
     │   │ PMOS (Gate 接 GND, 永遠 ON)
     └─┬─┘
       │
       ├──── Vout
       │
     PDN (NMOS 下拉網路)
       │
      GND
```

**特點**：
- 用一個**永遠導通的 PMOS** 取代整個 PUN
- **優點**：電晶體數量少（N+1 vs 2N）、佈局簡單
- **缺點**：
  - **有穩態電流**（當 PDN 導通時，VDD→PMOS→NMOS→GND）
  - VOL ≠ 0（被 PMOS 拉住，Vout 不能完全到 0）
  - **靜態功耗大**
  - 雜訊邊限差

**VOL 計算**：
令 PMOS 電流 = NMOS 電流，解出 VOL > 0

**應用**：ROM、PLA 等面積敏感的電路

### 7.2 傳輸閘（Transmission Gate, TG）

```
       ┌─────┐
  A ───┤ NMOS├─── Y
       └──┬──┘
          │ CLK
       ┌──┴──┐
  A ───┤ PMOS├─── Y
       └─────┘
          CLK_bar
```

**原理**：
- NMOS 傳遞 0 很好（VGS = VDD），但傳遞 1 會損失一個 Vtn（VGS 不夠）
- PMOS 傳遞 1 很好，但傳遞 0 會損失一個 |Vtp|
- **並聯後**：NMOS 和 PMOS 互補，**可以傳遞完整的 0 到 VDD**

**等效電阻**：

```
RTG = Rn ∥ Rp = (Rn · Rp) / (Rn + Rp)
```

隨輸入電壓變化，RTG 的特性：

| Vin | NMOS Req | PMOS Req | RTG |
|-----|---------|---------|-----|
| 0 | 低 | 高 | 中 |
| VDD/2 | 中 | 中 | 中 |
| VDD | 高 | 低 | 中 |

> **傳輸閘的等效電阻幾乎恆定**，這是它的重要優點！

**應用**：多工器（MUX）、鎖存器、XOR 閘

### 7.3 通過電晶體邏輯（Pass Transistor Logic）

只用 **NMOS** 來傳遞信號：

```
          B
          │
       ┌──┴──┐
  A ───┤ NMOS├─── Y = A·B（當 B=1，Y=A；當 B=0，Y=浮接）
       └─────┘
```

**優點**：
- 電晶體數量極少
- 適合實現 XOR、MUX 等

**缺點**：
- **閾值損失**：NMOS 傳遞 High 時，最多只能到 VDD - Vtn
- 需要**位準恢復電路（Level Restorer）**
- **串接級數受限**：每級損失更多電壓

#### CPL（Complementary Pass-Transistor Logic）

使用互補信號對（A 和 A_bar）來避免閾值損失問題，但電晶體數量增加。

---

## 八、關鍵術語表

| 英文 | 中文 | 說明 |
|------|------|------|
| PDN (Pull-Down Network) | 下拉網路 | NMOS 組成，實現 F |
| PUN (Pull-Up Network) | 上拉網路 | PMOS 組成，實現 F 互補 |
| NAND | 反及閘 | NMOS 串聯 + PMOS 並聯 |
| NOR | 反或閘 | NMOS 並聯 + PMOS 串聯 |
| AOI (AND-OR-Invert) | 與或反閘 | 複雜閘的一種 |
| OAI (OR-AND-Invert) | 或與反閘 | 複雜閘的一種 |
| Fan-in | 扇入 | 閘的輸入數目 |
| Fan-out | 扇出 | 閘驅動的下一級數目 |
| Logical Effort | 邏輯效能 | 閘的「笨重程度」 |
| Electrical Effort | 電氣效能 | Cout/Cin |
| Pseudo-NMOS | 偽 NMOS | 用固定 PMOS 做上拉 |
| Transmission Gate | 傳輸閘 | NMOS + PMOS 並聯傳遞 |
| Pass Transistor | 通過電晶體 | 只用 NMOS 傳遞 |
| DeMorgan's Law | 迪摩根定律 | PUN/PDN 互補的依據 |
| Topological Complement | 拓撲互補 | 串聯↔並聯 |
| Level Restorer | 位準恢復 | 補償閾值損失 |
| CPL | 互補式通過電晶體邏輯 | 使用互補信號對 |
| Equivalent Resistance | 等效電阻 | 串聯=加、並聯=除 |

---

## 九、數值例題

### 例題 1：NAND 閘電晶體尺寸設計

**題目**：設計一個 2-input NAND 閘，使其最差路徑延遲等於一個對稱反相器。
已知：反相器 Wn = 1μm，Wp = 2.5μm（μn/μp = 2.5），L = 90nm。

**解答**：

**步驟 1：分析 PDN（NMOS 串聯）**
- 2 個 NMOS 串聯，等效電阻 = 2Rn（最差情況）
- 要使等效電阻 = 反相器的 Rn → 每個 NMOS 的 W 加倍
- **NMOS: Wn = 2 × 1 = 2μm**

**步驟 2：分析 PUN（PMOS 並聯）**
- 2 個 PMOS 並聯，最差電阻 = 單一 PMOS 的 Rp
- 不需要補償
- **PMOS: Wp = 2.5μm**

**答：NMOS: Wn = 2μm，PMOS: Wp = 2.5μm，L = 90nm**

| 元件 | W | L |
|------|---|---|
| N1 | 2μm | 90nm |
| N2 | 2μm | 90nm |
| P1 | 2.5μm | 90nm |
| P2 | 2.5μm | 90nm |

> 總共 4 個電晶體，比反相器的 2 個多一倍。

---

### 例題 2：3-input NOR 閘尺寸設計

**題目**：設計一個 3-input NOR 閘，等效於參考反相器（Wn = 0.5μm，Wp = 1.25μm）。

**解答**：

**PDN（3 個 NMOS 並聯）**：
- 並聯不增加電阻，不需補償
- NMOS: Wn = 0.5μm

**PUN（3 個 PMOS 串聯）**：
- 3 個串聯，等效電阻 = 3Rp
- 每個 PMOS 的 W 要 ×3
- PMOS: Wp = 3 × 1.25 = 3.75μm

**答：**

| 元件 | W | 說明 |
|------|---|------|
| N1, N2, N3 | 0.5μm | 並聯，不需補償 |
| P1, P2, P3 | 3.75μm | 串聯，每個 ×3 |

> 注意 PMOS 每個都是 3.75μm，非常大！這就是為什麼避免高扇入 NOR 閘。

---

### 例題 3：邏輯效能計算

**題目**：一個 2-input NAND 閘驅動 4 個相同的 2-input NAND 閘。
已知 NAND2 的輸入電容 Cin = 5 fF/input（假設每個輸入相同）。
求電氣效能 h。

**解答**：

```
Cout = 4 個 NAND2 的總輸入電容
     = 4 × 5 fF = 20 fF（假設驅動每個閘的一個輸入）

h = Cout / Cin = 20 / 5 = 4
```

**答：h = 4（扇出為 4）**

級效能 f = g × h = (4/3) × 4 = 16/3 ≈ 5.33

---

### 例題 4：AOI22 電晶體數計算與真值表

**題目**：設計 AOI22 閘（Y = $\overline{A \cdot B + C \cdot D}$），列出電晶體連接方式和真值表。

**解答**：

**PDN（NMOS）**：
- A·B：N1(A) 串聯 N2(B)
- C·D：N3(C) 串聯 N4(D)
- 兩組並聯
- **4 個 NMOS**

**PUN（PMOS）**：（拓撲互補）
- P1(A) 並聯 P2(B)（對應 AB 串聯的互補）
- P3(C) 並聯 P4(D)（對應 CD 串聯的互補）
- 兩組串聯
- **4 個 PMOS**

**總共 8 個電晶體**

部分真值表：

| A | B | C | D | A·B | C·D | A·B+C·D | Y |
|---|---|---|---|-----|-----|---------|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |

---

### 例題 5：Pseudo-NMOS 的 VOL 計算

**題目**：一個 Pseudo-NMOS 反相器，PMOS 永遠導通（Gate 接 GND），
kp(Wp/Lp) = 10 μA/V²，kn(Wn/Ln) = 100 μA/V²，VDD = 1.8V，Vtn = 0.4V，Vtp = -0.4V。
當 Vin = VDD 時，求 VOL。

**解答**：

當 Vin = VDD：
- NMOS 導通，VGS_n = 1.8V
- PMOS 永遠導通，VGS_p = 0 - VDD = -1.8V
- 假設 NMOS 在線性區，PMOS 在飽和區（因為 VOL 很小）

PMOS 飽和電流：
```
Ip = (kp/2)(Wp/Lp)(VDD - |Vtp|)²
   = (10/2)(1.8 - 0.4)²
   = 5 × 1.96
   = 9.8 μA
```

NMOS 線性電流（VDS = VOL 很小）：
```
In = kn(Wn/Ln)[(VGS - Vtn)·VDS - VDS²/2]
   ≈ kn(Wn/Ln)(VGS - Vtn)·VOL    （VOL << VGS-Vtn）
   = 100 × (1.8 - 0.4) × VOL
   = 140 × VOL μA
```

令 Ip = In：
```
9.8 = 140 × VOL
VOL = 9.8 / 140 = 0.07V
```

**答：VOL ≈ 0.07V**（不是 0！這是 Pseudo-NMOS 的缺點）

穩態電流 = 9.8 μA → 靜態功率 = 9.8μA × 1.8V = 17.6 μW（每個閘！）

---

### 例題 6：最佳級數估算

**題目**：用邏輯效能方法，路徑效能 F = 100。求最佳級數 N_opt。

**解答**：
```
N_opt ≈ ln(F) / ln(ρ)
      = ln(100) / ln(3.6)
      = 4.605 / 1.281
      ≈ 3.6
```

取整數：**N_opt = 4 級**

每級的最佳效能：f_opt = F^(1/N) = 100^(1/4) = 3.16

**答：最佳為 4 級，每級效能 ≈ 3.16**

---

## 十、題型鑑別表

| 題目特徵 | 題型 | 方法 |
|---------|------|------|
| 給布林函數，畫電路 | PDN/PUN 設計 | NMOS 串=AND/並=OR + 拓撲互補 |
| 求電晶體尺寸 | 等效電阻法 | 串聯×N 補償寬度 |
| 比較閘的速度 | 延遲分析 | 考慮串聯電阻和電容 |
| 多級最佳化 | 邏輯效能 | F = G×B×H, f_opt = F^(1/N) |
| Pseudo-NMOS 的 VOL | 靜態分析 | 令 Ip = In 解方程 |
| 傳輸閘應用 | 功能分析 | NMOS+PMOS 互補傳遞 |

---

## ✅ 自我檢測

### Q1：為什麼 CMOS 只能直接實現反相函數（NAND、NOR），不能直接實現 AND、OR？

<details>
<summary>點擊展開答案</summary>

因為 CMOS 的架構是 PUN（上拉到 VDD）+ PDN（下拉到 GND）：

- 當 PDN 導通（邏輯函數 F = 1）→ 輸出被拉低到 GND → Vout = 0
- 當 PUN 導通（F = 0）→ 輸出被拉高到 VDD → Vout = VDD

所以 Vout = NOT(F)，輸出天然就是 F 的反相。

要得到非反相函數（AND、OR），需要再加一個反相器（Inverter），即：
- AND = NAND + INV
- OR = NOR + INV
</details>

### Q2：設計一個實現 Y = $\overline{A \cdot (B + C)}$ 的 CMOS 閘，畫出 PDN 和 PUN。

<details>
<summary>點擊展開答案</summary>

**函數分析**：F = A · (B + C)，Y = $\overline{F}$

**PDN（NMOS，實現 F）**：
- B + C → NMOS B 和 C **並聯**
- A · (B+C) → NMOS A 與上述並聯組**串聯**

```
PDN:
      ┌─── N_B ───┐
A ─── N_A ──┤            ├─── GND
      └─── N_C ───┘
```

**PUN（PMOS，拓撲互補）**：
- PDN 串聯 → PUN **並聯**
- PDN 並聯 → PUN **串聯**

```
PUN:
VDD ──── P_A ───┤
                 ├──── Y
VDD ── P_B ── P_C ──┤
```

即 P_A 與 (P_B 串聯 P_C) **並聯**。

總共 6 個電晶體（3 NMOS + 3 PMOS）。
</details>

### Q3：為什麼高扇入 NOR 閘比高扇入 NAND 閘差？

<details>
<summary>點擊展開答案</summary>

以 4-input 閘為例：

**4-input NAND**：
- PDN：4 個 NMOS 串聯 → 每個 W 要 ×4（但 NMOS 本身就小）
- PUN：4 個 PMOS 並聯 → 不需補償

**4-input NOR**：
- PDN：4 個 NMOS 並聯 → 不需補償
- PUN：4 個 PMOS **串聯** → 每個 W 要 ×4

問題在於 PMOS 本身就比 NMOS 大 2~3 倍，再乘以 4，變成反相器 PMOS 的 8~12 倍！
- 面積劇增
- 輸入電容劇增
- 驅動前一級的負擔增加

所以實務上盡量用 NAND 為主，避免高扇入 NOR。
</details>

### Q4：傳輸閘為什麼能傳遞完整的 0 到 VDD？

<details>
<summary>點擊展開答案</summary>

- **NMOS** 傳遞 0 很好（VGS = VDD - 0 = VDD >> Vtn），但傳遞 VDD 時 VGS = VDD - VDD = 0 < Vtn → 截止，實際只能傳到 VDD - Vtn。

- **PMOS** 傳遞 VDD 很好（|VGS| = VDD >> |Vtp|），但傳遞 0 時 |VGS| = 0 < |Vtp| → 截止，實際只能傳到 |Vtp|。

- **並聯後**：
  - 傳遞 0：NMOS 負責（OK）
  - 傳遞 VDD：PMOS 負責（OK）
  - 中間值：兩者一起負責

所以傳輸閘能傳遞完整的 0 到 VDD 範圍。
</details>

### Q5：如果要實現 Y = A XOR B，用通過電晶體邏輯需要幾個電晶體？

<details>
<summary>點擊展開答案</summary>

XOR: Y = A ⊕ B = A·$\overline{B}$ + $\overline{A}$·B

用通過電晶體邏輯（假設有互補信號 B 和 $\overline{B}$）：
- 當 B = 1：Y = A（通過 A）
- 當 B = 0：Y = $\overline{A}$（通過 $\overline{A}$）

如果用**傳輸閘（TG）**實現 2:1 MUX：
- 需要 2 個 TG = 4 個電晶體
- 加上產生 $\overline{A}$ 的反相器 = 2 個電晶體
- **總共 6 個電晶體**

如果用**純 NMOS Pass Transistor**：
- 2 個 NMOS + 1 個 level restorer
- 更少電晶體，但有閾值損失問題

比 CMOS 全靜態實現（通常需要 12~16 個電晶體）少很多！
</details>

---

> **下一章預告**：第四章將學習**動態邏輯**——利用時脈來減少電晶體數量、提升速度，
> 包括 Domino Logic、NP-CMOS 等進階技術。
