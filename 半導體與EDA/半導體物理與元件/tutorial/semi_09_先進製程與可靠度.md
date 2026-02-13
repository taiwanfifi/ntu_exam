# 第九章：先進製程與可靠度

> **學習目標**：掌握先進邏輯製程的演進趨勢、HKMG 技術、應變工程和可靠度議題。這是 TSMC 面試的加分重點。
> **預備知識**：第六章（MOSFET 元件物理）、第七章（FinFET/GAA 結構）
> **預估時間**：4～5 小時

---

## 🔰 本章基礎觀念（零基礎必讀）

### 為什麼要了解先進製程？

半導體產業的核心驅動力是**摩爾定律（Moore's Law）**：每 ~2 年，單位面積的電晶體數量翻倍。要做到這一點，需要持續縮小元件尺寸，同時解決各種物理和工程挑戰。

面試時，了解這些「挑戰與解決方案」能展現你對產業趨勢的掌握。

### 一分鐘抓住核心

```
製程演進路線圖：

Planar MOSFET → FinFET → GAA/Nanosheet → CFET
  (~45nm)       (22nm)     (3nm~)        (未來)

每一代要解決的核心問題：
1. 短通道效應 → FinFET/GAA（多面閘極）
2. 閘極漏電 → High-k/Metal Gate（HKMG）
3. 遷移率下降 → 應變工程（Strain Engineering）
4. 可靠度退化 → NBTI/HCI/TDDB 管理
```

---

## 一、先進邏輯製程演進

### 1.1 製程節點的演進

| 時期 | 節點 | 結構 | 關鍵技術 |
|------|------|------|---------|
| 2007-2011 | 45nm~32nm | Planar | HKMG (45nm Intel), 應變工程 |
| 2012-2017 | 22nm~10nm | FinFET | 三面閘極, Self-aligned |
| 2018-2022 | 7nm~5nm | FinFET | EUV微影, COAG |
| 2023-2025 | 3nm~2nm | GAA/Nanosheet | Nanosheet, Backside PDN |
| 2026+ | 1.4nm~ | GAA/CFET | CFET, 2D materials |

### 1.2 各節點特徵比較表

| 參數 | 7nm | 5nm | 3nm | 2nm |
|------|-----|-----|-----|-----|
| 結構 | FinFET | FinFET | FinFET/GAA | GAA |
| Fin Pitch (nm) | 30 | 25-30 | 23-26 | ~22 |
| Gate Pitch (nm) | 54 | 48 | 44-48 | ~40 |
| M1 Pitch (nm) | 36 | 28-30 | 22-24 | ~20 |
| 密度 (MTr/mm²) | ~90 | ~170 | ~290 | ~450 |
| 微影 | DUV+多重曝光/EUV | EUV | EUV+多重曝光 | High-NA EUV |
| 代表公司 | TSMC N7 | TSMC N5 | TSMC N3/Samsung 3GAE | TSMC N2/Intel 20A |

### 1.3 「製程節點」名稱的演變

**重要觀念**：現代製程節點名稱（如「3nm」）並不代表任何物理尺寸是 3nm！

```
早期（~90nm以前）：節點名稱 ≈ 閘極長度
後來（45nm~）：節點名稱成為行銷名稱
現在（7nm~）：節點名稱與實際尺寸關聯度低

實際衡量指標：
- Logic Density (MTr/mm²)：每平方毫米的電晶體數量
- SRAM Cell Size (μm²)
- Gate Pitch、Fin/Track Pitch
```

### 1.4 微影技術（Lithography）演進

| 技術 | 波長 | 節點 | 說明 |
|------|------|------|------|
| DUV (ArF) | 193nm | ~7nm | 配合多重曝光（SADP, SAQP） |
| EUV | 13.5nm | 7nm~3nm | 單次曝光取代多次 DUV |
| High-NA EUV | 13.5nm (NA=0.55) | 2nm~ | 更高解析度，Intel 率先導入 |

---

## 二、High-k / Metal Gate（HKMG）

### 2.1 為什麼需要 High-k？

傳統 MOSFET 使用 SiO₂ 作為閘極介電質。隨著尺寸縮小，需要增加 Cox = εox/tox 來維持閘極控制力。

**問題**：tox 薄到 ~1.2nm（僅 4-5 個原子層）時，**閘極直接穿隧漏電**急劇增加。

```
閘極漏電流 JG

(log) ↑
      │            ╱  SiO₂ 直接穿隧
      │           ╱
      │          ╱     ← 太薄了！
      │         ╱
      │        ╱
      │───────╱─── 可接受的漏電限制
      │      ╱
      │     ╱
      └────╱────────→ 1/tox
            ↑
          tox~1.2nm
```

### 2.2 High-k 的解決方案

用高介電常數材料取代 SiO₂：

$$C_{ox} = \frac{\varepsilon_0 \varepsilon_r}{t_{phys}}$$

如果 εr 更大，可以用更厚的物理厚度達到同樣的電容：

| 材料 | εr | 說明 |
|------|-----|------|
| SiO₂ | 3.9 | 傳統材料 |
| Si₃N₄ | 7.5 | 早期替代 |
| Al₂O₃ | 9 | 過渡方案 |
| HfO₂ | 25 | 業界主流 High-k |
| ZrO₂ | 25 | 用於 DRAM |
| La₂O₃ | 30 | 研究中 |

### 2.3 等效氧化層厚度（EOT）

$$EOT = \frac{\varepsilon_{SiO_2}}{\varepsilon_{HK}} \times t_{HK} = \frac{3.9}{\varepsilon_{HK}} \times t_{HK}$$

**範例**：
- HfO₂（εr = 25），物理厚度 tHK = 5nm
- EOT = (3.9/25) × 5 = **0.78nm**

物理厚度 5nm（穿隧漏電小），但電氣效果等於 0.78nm 的 SiO₂。

### 2.4 為什麼需要 Metal Gate？

傳統使用多晶矽（poly-Si）閘極有兩個問題：

1. **多晶矽空乏效應（Poly Depletion）**：
   - 多晶矽不是真正的金屬，靠近氧化層的區域會空乏
   - 等效增加了 ~0.3-0.5nm 的電介質厚度
   - 抵銷了 High-k 的部分好處

2. **功函數控制困難**：
   - NMOS 和 PMOS 需要不同的功函數來設定合適的 Vth
   - 多晶矽的功函數調整範圍有限

**解決方案**：使用金屬閘極（如 TiN、TaN、TiAl 等），可以精確控制功函數，且無空乏效應。

### 2.5 CET vs EOT

$$CET = EOT + \text{量子效應修正} + \text{其他寄生}$$

CET（Capacitance Equivalent Thickness）是從實際 C-V 測量得到的等效厚度，比 EOT 大約 0.3~0.5nm（因為反轉層的量子力學效應）。

### 2.6 Gate-First vs Gate-Last

| 方法 | 說明 | 優缺點 |
|------|------|--------|
| Gate-First | High-k/MG 先沉積，再做 S/D 退火 | 高溫可能損壞 High-k |
| Gate-Last (RMG) | 先用假閘極（Dummy Gate），最後替換 | 主流方法，避免高溫損壞 |

Intel 在 45nm 首次量產 HKMG（Gate-Last），TSMC 在 28nm 跟進。

---

## 三、應變工程（Strain Engineering）

### 3.1 為什麼需要應變？

隨著節點縮小，供電電壓降低，需要提高遷移率來維持驅動電流。應變（Strain）可以改變能帶結構，提升載子遷移率。

### 3.2 應變對遷移率的影響

**拉伸應變（Tensile Strain）→ 提升 NMOS 電子遷移率**

- 機制：改變 Si 導帶的谷結構，降低有效質量和散射率
- 遷移率提升：可達 50~100%

**壓縮應變（Compressive Strain）→ 提升 PMOS 電洞遷移率**

- 機制：改變價帶的重電洞/輕電洞能帶分裂
- 遷移率提升：可達 50~100%

```
NMOS 需要拉伸應變：
←─ 拉伸 ──→ 通道 ←── 拉伸 ──→

PMOS 需要壓縮應變：
──→ 壓縮 ←── 通道 ──→ 壓縮 ←──
```

### 3.3 實現應變的方法

#### (a) CESL（Contact Etch Stop Liner）

在元件上方沉積高應力的氮化矽薄膜：
- 拉伸 SiN → NMOS
- 壓縮 SiN → PMOS

#### (b) eSiGe（Embedded SiGe）源極/汲極

在 PMOS 的 S/D 區域嵌入 SiGe：
- SiGe 的晶格常數 > Si → 對通道施加壓縮應變
- 提升 PMOS 電洞遷移率
- Intel 在 90nm 首次使用，至今仍是標準技術

```
         Gate
    ┌────┴────┐
    │ Oxide  │
════╪════════╪════  ← Si 通道（被壓縮）
SiGe│        │SiGe  ← 嵌入式 SiGe S/D
    │  ←→←→  │      ← 壓縮應變
════╧════════╧════
```

#### (c) 拉伸應變 Si 通道

在 SiGe 虛擬基板上成長 Si 薄膜：
- Si 的晶格被 SiGe 拉伸
- 適合 NMOS

#### (d) 在 FinFET 和 GAA 中的應變

- FinFET：S/D 的 SiGe（PMOS）或 SiC（NMOS）對 Fin 施加應變
- Nanosheet：通過 S/D epitaxy 和 inner spacer 控制應變
- 隨著節點縮小，維持應變越來越困難

---

## 四、可靠度（Reliability）

### 4.1 概述

可靠度是半導體產業的核心議題：晶片必須在 10 年以上的使用壽命內維持性能。主要的退化機制有四大類。

### 4.2 NBTI（Negative Bias Temperature Instability）

**負偏壓溫度不穩定性**——PMOS 的主要退化機制。

**發生條件**：PMOS 在 ON 狀態（VGS < 0，反轉），溫度升高時：

```
      Gate (V < 0)
   ┌──────────┐
   │  Oxide   │ ← Si-H 鍵被打斷
   ├──────────┤     → 產生介面態 (Dit)
   │ channel  │     → Vth 負移（|Vth| 增加）
   │ (反轉)   │
```

**機制**：
1. Si/SiO₂ 介面的 Si-H 鍵在電場和溫度作用下斷裂
2. 氫原子擴散進入氧化層
3. 留下的懸掛鍵形成介面態（Dit）
4. Dit 增加 → |Vth| 增加 → 驅動電流 ID 下降

**NBTI 模型（Reaction-Diffusion Model）**：

$$\Delta V_{th} \propto t^n \quad (n \approx 0.16 \sim 0.25)$$

**NBTI 的特點**：
- 有部分**恢復效應（Recovery）**：移除偏壓後 Vth 會部分回復
- 所以測量時要注意「on-the-fly」測量，避免低估退化
- 在 High-k 材料中，PBTI（Positive BTI）也變得重要（影響 NMOS）

### 4.3 HCI（Hot Carrier Injection）

**熱載子注入**——短通道效應的可靠度後果。

**發生條件**：NMOS 在飽和區（高 VDS），汲極端電場最高。

```
      Gate
   ┌──────┐
   │Oxide │ ←── 熱電子被注入氧化層
   ╪══════╪═══
   │ →→→→ │→⚡  ← 汲極端電場最高
   Source   Drain     高能電子在此產生
```

**機制**：
1. 通道電場在汲極端最大
2. 電子獲得足夠能量（「熱」電子）
3. 部分熱電子被注入閘極氧化層
4. 產生氧化層電荷（Not）和介面態（Dit）
5. Vth 漂移、gm 退化

**HCI 退化模型**：

$$\Delta V_{th} \propto t^n \quad (n \approx 0.5)$$

**最惡劣偏壓條件**：VGS ≈ VDS/2（基板電流最大的點）

**解決方案**：
- LDD（Lightly Doped Drain）降低汲極電場
- 降低 VDD
- 使用氮化處理改善氧化層品質

### 4.4 TDDB（Time-Dependent Dielectric Breakdown）

**時間相依介電崩潰**——閘極氧化層的最終失效模式。

**發生條件**：閘極氧化層長期處於電場下。

**機制**：
1. 氧化層中的弱鍵被電場打斷
2. 隨時間累積缺陷（Defect generation）
3. 當缺陷密度達到臨界值，形成導電路徑
4. **氧化層永久崩潰** → 閘極和通道短路

**TDDB 壽命模型（Power-law model）**：

$$t_{BD} = A \cdot V_G^{-\gamma} \cdot \exp\left(\frac{E_a}{kT}\right)$$

或（1/E model）：

$$t_{BD} \propto \exp\left(\frac{G}{E_{ox}}\right)$$

**重要參數**：
- tBD 隨 VG 增加急劇下降
- 溫度越高，tBD 越短
- High-k 材料的 TDDB 行為與 SiO₂ 不同，需要新的模型

### 4.5 電遷移（Electromigration, EM）

**電遷移**——金屬互連線的失效模式。

**發生條件**：高電流密度流過金屬線。

```
電子流 →→→→→→→→→→→→→→→
      ═══════════════════
金屬原子 ○ ○ ○ ○ → ○ ○ ○ ○  ← 動量轉移使原子移動
      ═══════════════════
      空洞(Void)          堆積(Hillock)
      ← 電阻增加、斷線     → 可能短路
```

**Black 方程**：

$$MTTF = A \cdot J^{-n} \cdot \exp\left(\frac{E_a}{kT}\right)$$

其中：
- MTTF：平均失效時間（Mean Time To Failure）
- J：電流密度
- n：電流密度指數（通常 n ≈ 1~2）
- Ea：活化能（Cu 的 EM 約 0.8~1.0 eV）

**互連材料的演變**：

| 材料 | 電阻率 (μΩ·cm) | EM 抗性 | 使用年代 |
|------|---------------|--------|---------|
| Al | 2.7 | 較差 | ~180nm 以前 |
| Cu (Damascene) | 1.7 | 好 | 130nm~ |
| Co (Via) | 6.2 | 更好 | 10nm~ 局部互連 |
| Ru | 7.1 | 極好 | 研究/未來 |

**注意**：隨著線寬縮小，金屬線的實際電阻率因表面散射和晶界散射而大幅增加（遠高於塊材值）。

### 4.6 可靠度測試方法

| 退化機制 | 加速測試條件 | 外推方法 |
|---------|------------|---------|
| NBTI | 高溫 + 高 |VGS| | 時間冪律外推 |
| HCI | 高 VDS + 高 VGS | 時間冪律外推 |
| TDDB | 高 VG + 高溫 | 威布爾分佈 + 電壓加速 |
| EM | 高電流密度 + 高溫 | Black 方程 + 對數常態分佈 |

### 4.7 可靠度退化的影響

```
元件壽命內的退化趨勢：

參數退化
    ↑
    │            ╱ NBTI (PMOS)
    │           ╱
    │          ╱
    │         ╱   ╱ HCI (NMOS)
    │        ╱   ╱
    │       ╱   ╱
    │      ╱   ╱
    │     ╱   ╱
    │    ╱   ╱
    └───╱───╱──────────→ 時間 (log)

NBTI：∝ t^0.2 → 持續緩慢退化
HCI：∝ t^0.5 → 前期退化較快
TDDB：突然失效（不是漸進退化）
EM：在 MTTF 附近集中失效
```

---

## 五、TSMC vs Intel vs Samsung 製程比較

### 5.1 競爭格局（截至 2025 年）

| 指標 | TSMC | Intel | Samsung |
|------|------|-------|---------|
| 最先進量產 | N3E (3nm FinFET) | Intel 4 (FinFET) | 3nm GAA (3GAE) |
| 下一代 | N2 (GAA, 2025) | Intel 18A (GAA, 2025) | 2nm GAA (2GAP) |
| 市佔率(先進) | ~60% | ~15% | ~15% |
| 主要客戶 | Apple, AMD, NVIDIA, Qualcomm | Intel 自用 + 外部代工 | Qualcomm, Samsung |
| EUV 層數(3nm) | ~20 | ~20 | ~20 |

### 5.2 各家技術特色

**TSMC**：
- 製造良率業界最高
- 最完整的 IP 生態系
- N3B 是 FinFET 最後一代，N2 轉向 Nanosheet GAA
- TSMC N2 導入 Backside Power Delivery Network (BSPDN)

**Intel**：
- RibbonFET（Intel 版的 Nanosheet GAA）
- PowerVia（背面供電）：Intel 18A
- Intel 20A 首次在量產中同時導入 GAA + 背面供電
- 積極追趕，但良率仍需證明

**Samsung**：
- 全球最早量產 GAA（3nm GAE，2022）
- 但良率低、客戶少
- 正在努力改善 2nm 世代的良率

### 5.3 背面供電（Backside Power Delivery Network, BSPDN）

```
傳統架構：                    背面供電架構：
信號線 + 電源線都在正面        信號線在正面，電源線在背面

   ┌─ 信號 ─┐  ┌─ 電源 ─┐     ┌─ 只有信號線 ─┐
   │ M10    │  │ M10    │     │ M10         │
   │  ...   │  │  ...   │     │  ...        │
   │ M1     │  │ M1     │     │ M1          │ ← 正面
   ╪════════╪══╪════════╪     ╪═════════════╪
   │ 電晶體 │  │ 電晶體 │     │  電晶體     │
   ╧════════╧══╧════════╧     ╪═════════════╪
   │ 基板   │                 │ 電源線      │ ← 背面
                              │ 粗大、低電阻 │

優勢：
1. 正面金屬層減少 → 信號延遲降低
2. 電源線不受 pitch 限制 → IR drop 降低
3. 標準邏輯單元面積可以縮小 → 密度提升
```

### 5.4 未來技術方向

| 技術 | 時程 | 說明 |
|------|------|------|
| CFET | 2028~ | NMOS/PMOS 垂直堆疊 |
| 2D 通道材料 | 研究中 | MoS₂, WS₂ 等取代 Si |
| 3D 堆疊 | 漸進導入 | Chiplet, 3D IC |
| 碳奈米管 FET | 研究中 | 極高遷移率 |
| 光互連 | 研究中 | 解決互連延遲瓶頸 |

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|---------|------|
| 高介電常數 | High-k | 介電常數大於SiO₂的材料 | HfO₂ (εr≈25) |
| 等效氧化層厚度 | EOT | 換算成SiO₂的等效厚度 | EOT=(3.9/εHK)×tHK |
| 金屬閘極 | Metal Gate | 取代多晶矽的金屬閘極 | TiN, TaN |
| 多晶矽空乏 | Poly Depletion | poly-Si靠近氧化層的空乏效應 | 等效增厚~0.3nm |
| 替換閘極 | Replacement Metal Gate (RMG) | Gate-Last製程 | 先假閘，後替換 |
| 應變工程 | Strain Engineering | 用應變提升遷移率 | eSiGe, CESL |
| 拉伸應變 | Tensile Strain | 拉伸Si晶格→NMOS μn↑ | 應變Si on SiGe |
| 壓縮應變 | Compressive Strain | 壓縮Si晶格→PMOS μp↑ | eSiGe in S/D |
| NBTI | Negative BTI | PMOS Vth隨時間退化 | ΔVth ∝ t^0.2 |
| HCI | Hot Carrier Injection | 熱電子注入氧化層 | 汲極端電場最高 |
| TDDB | Time-Dependent Dielectric BD | 氧化層隨時間崩潰 | tBD隨VG指數下降 |
| 電遷移 | Electromigration (EM) | 金屬原子被電子推動 | Black方程 |
| MTTF | Mean Time To Failure | 平均失效時間 | MTTF ∝ J⁻²·exp(Ea/kT) |
| EUV | Extreme Ultraviolet | 極紫外光微影（13.5nm） | 7nm~ 使用 |
| 背面供電 | BSPDN | 電源線移到晶片背面 | Intel PowerVia |
| CFET | Complementary FET | N/P垂直堆疊 | 未來 |

---

## 數值例題

### 【例題 1】EOT 計算

**題目**：閘極介電層為 3nm HfO₂（εr = 25）加上 0.5nm 介面層 SiO₂（εr = 3.9）。求總 EOT 和總 Cox。

**解答**：

```
HfO₂ 的 EOT = (3.9/25) × 3 = 0.468 nm
SiO₂ IL 的 EOT = 0.5 nm（它本身就是 SiO₂）

總 EOT = 0.468 + 0.5 = 0.968 nm ≈ 1.0 nm

Cox = εSiO₂/EOT = 3.9 × 8.854×10⁻¹⁴ / (0.968×10⁻⁷)
    = 3.453×10⁻¹³ / 9.68×10⁻⁸
    = 3.57×10⁻⁶ F/cm² = 3.57 μF/cm²
```

**比較**：如果全用 SiO₂ 做到 EOT = 1.0nm，物理厚度只有 1.0nm → 穿隧漏電巨大。用 HfO₂ + IL，物理厚度 3.5nm → 穿隧漏電可控。

---

### 【例題 2】NBTI 壽命預測

**題目**：PMOS 在加速條件（T = 125°C，|VGS| = 1.5V）下測試，10000 秒後 ΔVth = 30 mV。假設 ΔVth ∝ t⁰·²，且 10 年壽命需要 ΔVth < 50 mV。問：此元件是否通過壽命規格？

**解答**：

```
10 年 = 10 × 365 × 24 × 3600 = 3.156×10⁸ 秒

ΔVth(10年) = ΔVth(10000s) × (t₂/t₁)^0.2
           = 30 × (3.156×10⁸/10⁴)^0.2
           = 30 × (3.156×10⁴)^0.2
           = 30 × (31560)^0.2

(31560)^0.2 = 10^(0.2×log10(31560)) = 10^(0.2×4.499) = 10^0.9 = 7.94

ΔVth(10年) = 30 × 7.94 = 238 mV >> 50 mV

答案：不通過！
```

**但注意**：這是在加速條件下的結果。實際使用條件的溫度和電壓更低，需要用活化能外推到實際條件。如果 Ea = 0.5 eV：

```
加速因子(溫度) = exp(Ea/k × (1/T_use - 1/T_stress))
              = exp(0.5/8.617e-5 × (1/358 - 1/398))
              ≈ exp(5803 × 2.81×10⁻⁴)
              = exp(1.63) = 5.1

加速因子(電壓) ≈ (Vstress/Vuse)^γ ≈ (1.5/0.8)^5 ≈ 22.7

總加速因子 = 5.1 × 22.7 = 115.8

在實際使用條件下：
ΔVth(10年, 使用) ≈ 238 / 115.8^0.2 ...

（實際外推需要更精確的模型，這裡僅示意）
```

---

### 【例題 3】電遷移壽命（Black 方程）

**題目**：Cu 互連線在 J = 2 MA/cm²、T = 300°C 下測試，MTTF = 100 小時。已知 n = 2，Ea = 0.9 eV。求在 J = 0.5 MA/cm²、T = 100°C 下的預期壽命。

**解答**：

```
Black 方程：MTTF = A × J⁻ⁿ × exp(Ea/kT)

MTTF₂/MTTF₁ = (J₁/J₂)ⁿ × exp(Ea/k × (1/T₂ - 1/T₁))

電流密度加速因子：
(J₁/J₂)² = (2/0.5)² = 4² = 16

溫度加速因子：
T₁ = 300°C = 573K, T₂ = 100°C = 373K
Ea/k = 0.9/(8.617×10⁻⁵) = 10444 K

exp(10444 × (1/373 - 1/573))
= exp(10444 × (0.002681 - 0.001745))
= exp(10444 × 9.36×10⁻⁴)
= exp(9.78)
= 17,687

總加速因子 = 16 × 17,687 = 283,000

MTTF（使用條件）= 100 × 283,000 = 2.83×10⁷ 小時
                = 3,230 年

答案：在使用條件下預期壽命約 3,230 年 >> 10 年 ✓
```

---

### 【例題 4】應變對遷移率的影響

**題目**：未加應變的 Si PMOS μp = 100 cm²/V·s。使用 eSiGe（30% Ge）後，壓縮應變使 μp 提升 80%。求應變後的 gm 改善（假設其他參數不變）。

**解答**：

```
μp(strained) = 100 × 1.80 = 180 cm²/V·s

gm ∝ μp × Cox × (W/L) × (VGS - Vth)

其他參數不變，所以：
gm 改善 = 180/100 = 1.80 = 80% 提升

這等效於驅動電流 ID 也提升 80%（飽和區 ID ∝ μ）。

或者可以反過來看：不需要增加 W 就得到 80% 更多電流。
如果原來需要 W = 1μm，現在只需要 W = 1/1.8 = 0.56μm
→ 面積縮小 44%！
```

---

## 題型鑑別

| 看到什麼關鍵字 | 用什麼方法 | 對應公式/概念 |
|--------------|----------|-------------|
| EOT、High-k | 等效厚度計算 | EOT = (3.9/εHK)×tHK |
| 閘極漏電、穿隧 | High-k解決方案 | 物理厚度↑，Cox不變 |
| 功函數、Vth調整 | Metal Gate | Gate-Last/RMG |
| 遷移率提升、應變 | 判斷拉伸/壓縮 | NMOS拉伸, PMOS壓縮 |
| NBTI、Vth退化 | 時間冪律 | ΔVth ∝ t^0.2 |
| HCI、熱載子 | 汲極電場分析 | LDD降低電場 |
| TDDB、氧化層崩潰 | 壽命模型 | tBD ∝ VG^(-γ)·exp(Ea/kT) |
| 電遷移、互連失效 | Black方程 | MTTF = A·J⁻ⁿ·exp(Ea/kT) |
| FinFET vs GAA | 閘極控制力比較 | 三面 vs 四面 |
| TSMC vs Intel | 製程節點對比 | 密度、良率、客戶 |

---

## ✅ 自我檢測

### 基礎題

**Q1**：什麼是 EOT？為什麼要用 High-k 材料？

<details>
<summary>點擊查看答案</summary>

**EOT（Equivalent Oxide Thickness）**：把 High-k 閘極介電質換算成等效 SiO₂ 厚度。

EOT = (εSiO₂/εHK) × tHK = (3.9/εHK) × tHK

**為什麼用 High-k**：
- 繼續縮小 MOSFET 需要更大的 Cox = ε/t
- SiO₂ 的 tox 不能小於 ~1.2nm（穿隧漏電）
- High-k 材料（如 HfO₂，εr=25）可以用更厚的物理厚度達到同樣的 Cox
- 物理厚度厚 → 穿隧漏電小 → 閘極漏電問題解決

</details>

**Q2**：NBTI 和 HCI 分別影響哪種元件？在什麼偏壓條件下最嚴重？

<details>
<summary>點擊查看答案</summary>

**NBTI**：
- 影響 **PMOS**
- 最嚴重條件：PMOS **ON 狀態**（VGS = -VDD），高溫
- 機制：Si-H 鍵斷裂 → 介面態 → |Vth| 增加
- ΔVth ∝ t^0.2

**HCI**：
- 影響 **NMOS**（也可影響 PMOS，但 NMOS 更嚴重）
- 最嚴重條件：**飽和區**（高 VDS），VGS ≈ VDS/2（基板電流最大點）
- 機制：熱電子注入氧化層 → Vth 漂移
- ΔVth ∝ t^0.5

</details>

**Q3**：應變工程中，NMOS 和 PMOS 分別需要什麼類型的應變？

<details>
<summary>點擊查看答案</summary>

- **NMOS**：需要**拉伸應變（Tensile Strain）**→ 提升電子遷移率
  - 實現方法：拉伸 CESL、SiC S/D、應變 Si on SiGe

- **PMOS**：需要**壓縮應變（Compressive Strain）**→ 提升電洞遷移率
  - 實現方法：壓縮 CESL、eSiGe S/D（最常用）

記憶口訣：**NMOS 拉（Tensile），PMOS 壓（Compressive）**

</details>

### 進階題

**Q4**：TSMC 面試題：解釋 Gate-Last（RMG）製程的流程和優勢。

<details>
<summary>點擊查看答案</summary>

**Gate-Last（Replacement Metal Gate, RMG）流程**：

1. 沉積假閘極（Dummy Gate）：用多晶矽
2. 完成 S/D 製程（離子佈植、活化退火 ~1000°C）
3. 沉積 ILD（層間介電質）並平坦化（CMP）
4. 移除假閘極（選擇性蝕刻）
5. 沉積 High-k 介電質（HfO₂ ~2nm）
6. 沉積金屬閘極（TiN/TaN + 功函數金屬 + 填充金屬）

**優勢**：
1. High-k 和金屬閘極不需要經歷 S/D 退火的高溫（~1000°C）→ 避免 High-k 結晶化和介面品質退化
2. 可以分別為 NMOS 和 PMOS 沉積不同功函數的金屬 → 精確控制 Vth
3. 金屬閘極無多晶矽空乏效應 → CET 更小

**主要挑戰**：
- 需要在高深寬比的溝槽中均勻沉積 → 對 ALD 技術要求高
- 金屬填充品質影響 Vth 均勻性

</details>

**Q5**：用 Black 方程解釋為什麼 Cu 互連線有最大允許電流密度的規格。

<details>
<summary>點擊查看答案</summary>

Black 方程：MTTF = A × J⁻ⁿ × exp(Ea/kT)

因為 n ≈ 2（Cu），壽命與電流密度的平方成反比：

- J 增加 2 倍 → MTTF 縮短 4 倍
- J 增加 10 倍 → MTTF 縮短 100 倍

所以設計規則中會規定**最大允許電流密度 Jmax**，確保在使用溫度下 MTTF > 10 年。

典型值：Cu 互連線的 Jmax ≈ 1~2 MA/cm²

隨著線寬縮小（面積減小），在相同電流下 J 增加 → EM 風險增加。這是先進製程互連的主要挑戰之一。

解決方案：
- 使用抗 EM 更好的 barrier/liner（如 Co、Ru）
- 冗餘設計（Redundant vias）
- 降低局部溫度

</details>

**Q6**：比較 TSMC N3 和 Intel 18A 的技術方案差異。

<details>
<summary>點擊查看答案</summary>

| 特性 | TSMC N3 (N3B/N3E) | Intel 18A |
|------|-------------------|-----------|
| 結構 | FinFET | GAA (RibbonFET) |
| 背面供電 | 無（N2才導入） | 有（PowerVia） |
| 閘極控制 | 三面 | 四面（更好） |
| 密度 | ~290 MTr/mm² | ~250 MTr/mm²（估計） |
| 量產時間 | 2022-2023（已量產） | 2025（預計） |
| 良率 | 高（已成熟） | 待驗證 |
| 主要客戶 | Apple、AMD、NVIDIA | Intel 自用 + 外部代工 |

**TSMC 策略**：FinFET 延用到 N3，穩健過渡，N2 才轉 GAA
**Intel 策略**：18A 一次導入 GAA + 背面供電，技術風險高但潛力大

在先進製程的競爭中，**良率**往往比技術先進性更重要。TSMC 的優勢在於良率和客戶生態系，Intel 的挑戰在於證明新技術的量產能力。

</details>

---

## 本章重點整理

```
1. 製程演進：Planar→FinFET(22nm)→GAA(3nm)→CFET(未來)
2. High-k：用HfO₂(εr=25)取代SiO₂(3.9)，降低閘極漏電
3. EOT = (3.9/εHK) × tHK，EOT~1nm但物理厚度~3-5nm
4. Metal Gate：消除poly depletion，精確控制功函數
5. Gate-Last(RMG)：先做S/D退火，再沉積HK/MG
6. 應變工程：NMOS拉伸、PMOS壓縮，提升遷移率50-100%
7. NBTI：PMOS ON狀態退化，ΔVth ∝ t^0.2
8. HCI：NMOS飽和區退化，ΔVth ∝ t^0.5
9. TDDB：閘極氧化層的最終失效
10. 電遷移：MTTF = A·J⁻ⁿ·exp(Ea/kT)（Black方程）
11. BSPDN（背面供電）：降低IR drop，提高密度
12. 良率是先進製程競爭的核心
```

---

## 全系列回顧

恭喜你完成了「半導體物理與元件」的完整學習旅程！讓我們回顧九章的脈絡：

```
第1章 材料與結構 ──→ 半導體是什麼？用什麼材料？
第2章 能帶與載子 ──→ 裡面有多少可以導電的載子？
第3章 傳輸機制   ──→ 載子怎麼移動？（漂移+擴散）
第4章 產生復合   ──→ 載子怎麼被創造和消滅？
第5章 PN接面     ──→ 最基本的元件結構
第6章 MOSFET     ──→ 最重要的元件（邏輯晶片的基礎）
第7章 BJT與先進  ──→ BJT物理 + FinFET/GAA先進結構
第8章 光電功率   ──→ 太陽能電池、LED、功率元件
第9章 先進製程   ──→ HKMG、應變、可靠度、產業趨勢
```

每一章都是後面章節的基礎，建議按順序學習。祝學習順利，面試成功！
