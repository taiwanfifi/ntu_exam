# VLSI 教學講義 第八章：低功耗設計與先進技術

> **適用對象**：零基礎入門，電機/電子系大學部至研究所
> **重要度**：低功耗設計是 TSMC/MTK/Qualcomm/Apple 面試**最高頻話題**，業界每天都在面對的核心挑戰

---

## 🔰 本章基礎觀念（零基礎必讀）

### 為什麼低功耗如此重要？

| 應用場景 | 功耗限制原因 |
|---------|------------|
| 手機/穿戴裝置 | 電池壽命 |
| 資料中心 | 電費 + 散熱成本 |
| 物聯網（IoT） | 微小電池或能量採集 |
| 自駕車/AI | 散熱面積有限 |

> **摩爾定律的瓶頸已經從速度轉向功耗。** 現代晶片設計花 **50% 以上的努力** 在管理功耗。

### 功率回顧

```
P_total = P_dynamic + P_short-circuit + P_static
        = α·CL·VDD²·f + Psc + Ileak·VDD
```

---

## 一、低功耗設計技術

### 1.1 電壓縮放（Voltage Scaling）：最有效的省電手段

```
┌───────────────────────────────┐
│  P_dynamic ∝ VDD²             │
│  P_static ∝ VDD              │
│  Delay ∝ VDD / (VDD - Vt)²   │
└───────────────────────────────┘
```

**效果**：VDD 降低 30% → 動態功率降低 51%

```
VDD 從 1.0V → 0.7V：
P_new/P_old = (0.7/1.0)² = 0.49 → 省電 51%
```

**代價**：速度變慢

```
假設 Vt = 0.3V：
Delay_new/Delay_old = [0.7/(0.7-0.3)²] / [1.0/(1.0-0.3)²]
                    = [0.7/0.16] / [1.0/0.49]
                    = 4.375 / 2.04
                    = 2.14 → 慢了 114%
```

> **這就是為什麼需要 DVFS**：在不需要高速時降壓省電，需要時再升壓。

### 1.2 多閾值電壓（Multi-Vth）

同一個晶片上同時使用**不同閾值電壓**的電晶體：

| 類型 | Vt 值 | 速度 | 漏電 | 用途 |
|------|-------|------|------|------|
| **LVT**（Low-Vt） | ~0.25V | **最快** | **最大** | 關鍵路徑（Critical Path） |
| **SVT**（Standard-Vt） | ~0.35V | 中等 | 中等 | 一般邏輯 |
| **HVT**（High-Vt） | ~0.45V | 最慢 | **最小** | 非關鍵路徑 |
| **UHVT**（Ultra-High-Vt） | ~0.55V | 非常慢 | 極小 | 待機電路 |

**設計策略**：

```
         ┌─────────┐     ┌─────────┐     ┌─────────┐
Input ───┤  HVT    ├──→──┤  LVT    ├──→──┤  HVT    ├───→ Output
         │ (省電)  │     │ (加速)  │     │ (省電)  │
         └─────────┘     └─────────┘     └─────────┘
                      ↑ 關鍵路徑上用 LVT
```

**典型比例**（手機 SoC）：
- HVT：60~70%（大部分）
- SVT：20~25%
- LVT：5~15%（只用在最關鍵的路徑）

> **面試常問**：「如何用 Multi-Vth 在不犧牲速度的前提下降低漏電？」
> 答：在關鍵路徑上用 LVT 維持速度，非關鍵路徑用 HVT 降低漏電。

### 1.3 電源閘控（Power Gating）

**核心概念**：完全切斷不使用模組的電源，使漏電降到接近零。

```
      VDD（永遠供電）
       │
    ┌──┴──┐
    │Sleep│ ← Header Switch（大 PMOS，由 Sleep 信號控制）
    │PMOS │
    └──┬──┘
       │
    VVDD（虛擬 VDD，可被切斷）
       │
   ┌───┴───────────┐
   │               │
   │  Logic Block  │  ← 被閘控的邏輯模組
   │               │
   └───┬───────────┘
       │
      GND
```

或者用 Footer Switch（大 NMOS 接在 GND 端）：

```
   ┌───┬───────────┐
   │               │
   │  Logic Block  │
   │               │
   └───┬───────────┘
       │
    VGND（虛擬 GND）
       │
    ┌──┴──┐
    │Sleep│ ← Footer Switch（大 NMOS）
    │NMOS │
    └──┬──┘
       │
      GND
```

**設計考量**：

| 考量 | 說明 |
|------|------|
| Sleep Switch 大小 | 太小 → IR drop 大、速度慢；太大 → 面積浪費 |
| 衝入電流（Inrush Current） | 開啟時電容充電 → 巨大電流脈衝 |
| 保留暫存器（Retention Register） | 休眠前要保存狀態 → 用特殊 FF |
| 喚醒時間 | 從休眠到工作需要時間恢復 VVDD |
| 隔離單元（Isolation Cell） | 防止休眠模組的浮動輸出干擾其他模組 |

**電源閘控的層級**：

```
粗粒度（Coarse-Grain）：關閉整個功能模組
   ↕
細粒度（Fine-Grain）：關閉單個標準元件的行
```

### 1.4 時脈閘控（Clock Gating）

上一章已介紹。補充重點：

```
省電效果：
- 時脈網路通常占動態功率的 30~50%
- 時脈閘控可以在模組不活動時節省這部分功率
- 不需要保存/恢復狀態（比 Power Gating 簡單）
```

**自動時脈閘控（Automatic Clock Gating）**：
- EDA 工具可以自動識別暫存器的使能信號
- 自動插入 ICG（Integrated Clock Gating）單元
- 在 RTL 級別使用 `if (en) Q <= D;` 即可觸發

### 1.5 DVFS（Dynamic Voltage and Frequency Scaling）

**核心概念**：根據工作負載，動態調整 VDD 和頻率。

```
                性能需求高         性能需求低
                ┌─────────┐       ┌─────────┐
VDD：           │  1.0V   │       │  0.7V   │
                └─────────┘       └─────────┘
頻率：          │  2 GHz  │       │  1 GHz  │
                └─────────┘       └─────────┘
動態功率：      │  P₀     │       │ ~0.25P₀ │
                └─────────┘       └─────────┘
```

**計算**：

```
P₁/P₀ = (V₁/V₀)² × (f₁/f₀)
       = (0.7/1.0)² × (1/2)
       = 0.49 × 0.5
       = 0.245 → 省了 75.5% 的動態功率！
```

**DVFS 的實現**：
- 需要片上**電壓調節器（Voltage Regulator）**或**PMU（Power Management Unit）**
- 頻率由 PLL 控制
- 軟體（OS 排程器）決定何時調整
- 切換時需要**先降頻再降壓**（升壓時先升壓再升頻），避免時序違規

### 1.6 體偏壓（Body Biasing）

通過改變電晶體的基體（Body/Bulk）電壓來調整 Vt：

#### (a) 正向體偏壓（Forward Body Biasing, FBB）

```
NMOS：VBS > 0（基體電壓 > 源極電壓）
效果：Vt 降低 → 速度加快 → 漏電增加
```

#### (b) 反向體偏壓（Reverse Body Biasing, RBB）

```
NMOS：VBS < 0（基體電壓 < 源極電壓）
效果：Vt 升高 → 速度變慢 → 漏電降低
```

**體偏壓效應公式**：

```
Vt = Vt0 + γ(√(2φf - VBS) - √(2φf))

其中：
- Vt0：零偏壓閾值電壓
- γ：體效應係數
- φf：費米電位
- VBS：基體-源極電壓
```

**應用場景**：

| 模式 | 體偏壓 | 效果 | 使用時機 |
|------|--------|------|---------|
| 高性能模式 | FBB | Vt↓, 速度↑, 漏電↑ | 需要高速運算 |
| 正常模式 | 零偏壓 | 正常 | 一般操作 |
| 待機模式 | RBB | Vt↑, 速度↓, 漏電↓ | 休眠省電 |

> **注意**：在先進製程（FinFET）中，體偏壓的效果大幅降低，因為通道被鰭片（Fin）包圍，
> 基體對通道的控制力減弱。但在 FD-SOI 製程中，體偏壓仍然非常有效。

---

## 二、變異性（Variability）

### 2.1 PVT 變異：Process, Voltage, Temperature

| 變異來源 | 英文 | 影響 |
|---------|------|------|
| 製程（Process） | P | Vt、L、W、tox 等偏離標稱值 |
| 電壓（Voltage） | V | VDD 波動 |
| 溫度（Temperature） | T | 載子移動率、Vt 等隨溫度變化 |

### 2.2 製程變異的分類

#### (a) 全域變異（Inter-die / Global Variation）

- 不同晶圓、不同晶片之間的差異
- 所有電晶體**同方向偏移**（例如全部偏快或全部偏慢）
- 主要原因：製程參數的批次差異

#### (b) 局部變異（Intra-die / Local Variation）

- 同一晶片上不同位置的差異
- 電晶體之間的**隨機差異**
- 主要原因：摻雜原子的隨機分佈（Random Dopant Fluctuation, RDF）
- **在先進製程中越來越嚴重**

### 2.3 PVT Corner

設計時需要在**多個 PVT 角點**驗證電路：

| Corner | NMOS | PMOS | 特性 |
|--------|------|------|------|
| **SS**（Slow-Slow） | 慢 | 慢 | **最慢**（Setup worst case） |
| **FF**（Fast-Fast） | 快 | 快 | **最快**（Hold worst case） |
| **TT**（Typical-Typical） | 典型 | 典型 | 標稱設計點 |
| **SF**（Slow-Fast） | 慢 | 快 | PMOS 較強（VM 偏高） |
| **FS**（Fast-Slow） | 快 | 慢 | NMOS 較強（VM 偏低） |

**電壓和溫度的 Corner**：

| 條件 | 電壓 | 溫度 | 說明 |
|------|------|------|------|
| Best case speed | VDD + 10% | -40°C | 最快（Setup relaxed） |
| Worst case speed | VDD - 10% | 125°C | 最慢（Setup critical） |
| Worst case leakage | VDD + 10% | 125°C | 漏電最大 |

**完整 PVT 矩陣**：

```
Process: SS, TT, FF, SF, FS  (5 corners)
Voltage: VDD_min, VDD_nom, VDD_max  (3 levels)
Temperature: -40°C, 25°C, 125°C  (3 levels)

理論上：5 × 3 × 3 = 45 個組合
實務上：選擇最重要的 ~10 個組合驗證
```

### 2.4 溫度反轉效應（Temperature Inversion）

在先進低電壓製程中，有一個反直覺的現象：

| 傳統認知（高 VDD） | 先進製程（低 VDD） |
|-------------------|-------------------|
| 高溫 → 移動率↓ → 速度↓ | 高溫 → Vt↓ → **速度可能↑** |
| 低溫 → 速度↑ | 低溫 → Vt↑ → **速度可能↓** |

**原因**：在接近閾值電壓工作時，Vt 的溫度效應（降低）比移動率的溫度效應（降低）更主導。

> 這使得溫度分析更加複雜，不能簡單假設「低溫就是最快」。

---

## 三、可測試性設計（Design for Testability, DFT）

### 3.1 為什麼需要 DFT？

製造出的晶片可能有缺陷（defect），需要測試才能出貨。
但晶片內部有**數十億個電晶體**，外部引腳只有幾百個，如何測試？

> **DFT 的目的**：讓內部節點「可觀察」和「可控制」

### 3.2 掃描鏈（Scan Chain）

**核心概念**：將所有正反器串接成一條移位暫存器。

#### 正常模式

```
            ┌───────────┐
Comb. Logic → D    FF    Q → Comb. Logic → ...
            │   CLK     │
            └───────────┘
```

#### 掃描模式

```
Scan In → MUX → D    FF    Q → MUX → D    FF    Q → ... → Scan Out
          ↑           │           ↑           │
       scan_en     CLK         scan_en     CLK
```

**工作流程**：
1. **Shift-In**：SE = 1，將測試向量從 Scan In 逐位元移入所有 FF
2. **Capture**：SE = 0，施加一個時脈邊緣，正常邏輯運算一次
3. **Shift-Out**：SE = 1，將結果從 Scan Out 逐位元移出，同時移入下一個測試向量

**面積代價**：每個 FF 增加一個 MUX（約增加 10~15% 面積）

### 3.3 ATPG（Automatic Test Pattern Generation）

**自動測試向量產生**：EDA 工具自動生成測試向量，目標是達到高**故障覆蓋率**。

**故障模型**：

| 模型 | 假設 |
|------|------|
| Stuck-at-0 (SA0) | 節點永遠為 0 |
| Stuck-at-1 (SA1) | 節點永遠為 1 |
| Transition Fault | 節點無法完成 0→1 或 1→0 轉態 |
| Path Delay Fault | 路徑延遲超出規格 |
| Bridge Fault | 兩個節點短路 |

**故障覆蓋率**：

```
Fault Coverage = (偵測到的故障數) / (總故障數) × 100%

目標：通常 > 95%，高端產品要求 > 99%
```

### 3.4 BIST（Built-In Self-Test）

**內建自測試**：在晶片內部放置測試電路，不需要外部測試機。

```
┌──────────────────────────────────┐
│  BIST Controller                  │
│  ┌──────┐    ┌──────┐    ┌─────┐│
│  │ PRPG ├───→│ CUT  ├───→│MISR ││
│  │(向量  │    │(被測  │    │(壓縮││
│  │ 產生) │    │ 電路) │    │比較)││
│  └──────┘    └──────┘    └─────┘│
└──────────────────────────────────┘
```

| 元件 | 功能 |
|------|------|
| PRPG（Pseudo-Random Pattern Generator） | 產生偽隨機測試向量 |
| CUT（Circuit Under Test） | 被測試的電路 |
| MISR（Multiple Input Signature Register） | 壓縮輸出結果為「簽章」 |

**BIST 的優點**：
- 不需昂貴的外部測試機
- 可以在系統中隨時自測
- 特別適合**記憶體測試**（Memory BIST）

---

## 四、SoC 設計流程

### 4.1 完整流程

```
  ┌─────────────┐
  │   Spec      │  ← 規格定義：功能、性能、功耗、面積
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │    RTL      │  ← 暫存器轉移層級設計（Verilog/VHDL）
  │  Design     │     功能模擬驗證
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │ Synthesis   │  ← 邏輯合成：RTL → Gate-level Netlist
  │             │     使用標準元件庫（Standard Cell Library）
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │   DFT       │  ← 插入掃描鏈、BIST 等測試結構
  │  Insertion  │
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │  Place &    │  ← 佈局與繞線
  │  Route (P&R)│     Floorplan → Placement → CTS → Routing
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │  Signoff    │  ← 最終驗證
  │ Verification│     STA、IR Drop、EM、DRC/LVS
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │  Tapeout    │  ← 送出 GDS/OASIS 給晶圓廠
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │  Fab &      │  ← 製造、封裝、測試
  │  Packaging  │
  └─────────────┘
```

### 4.2 各步驟詳解

#### (a) Spec（規格定義）
- 功能需求
- 目標製程（如 TSMC 5nm）
- 性能指標（頻率、吞吐量）
- 功耗預算
- 面積限制
- 介面標準（PCIe、DDR、USB 等）

#### (b) RTL Design（RTL 設計）
- 用 Verilog 或 SystemVerilog 編寫
- 功能驗證（Functional Simulation）
- 形式驗證（Formal Verification）
- 可能耗時數月

#### (c) Synthesis（邏輯合成）
- 將 RTL 轉換為閘級網表（Gate-level Netlist）
- 目標：滿足時序（Timing）、面積（Area）、功耗（Power）約束
- 使用 EDA 工具：Synopsys Design Compiler, Cadence Genus 等

#### (d) Place & Route（P&R）
- **Floorplan**：決定模組位置、電源規劃
- **Placement**：放置標準元件
- **CTS（Clock Tree Synthesis）**：建立時脈樹
- **Routing**：金屬連線
- 使用 EDA 工具：Synopsys ICC2, Cadence Innovus 等

#### (e) Signoff（簽核驗證）

| 驗證項目 | 工具 | 內容 |
|---------|------|------|
| STA（靜態時序分析） | PrimeTime | Setup/Hold 檢查 |
| Power Analysis | PrimePower/Voltus | 功耗分析 |
| IR Drop | RedHawk/Voltus | 電源完整性 |
| EM（電遷移） | 同上 | 可靠性 |
| DRC（設計規則檢查） | Calibre/IC Validator | 製程規則 |
| LVS（佈局與電路比對） | Calibre/IC Validator | 一致性 |
| Formal Verification | Formality/Conformal | RTL vs 網表一致性 |

#### (f) Tapeout（送廠）
- 產出 GDS-II 或 OASIS 檔案
- 提交給晶圓廠（如 TSMC）
- 開始光罩製作和製造
- 從 tapeout 到拿到晶片通常需要 **2~3 個月**

---

## 五、關鍵術語表

| 英文 | 中文 | 說明 |
|------|------|------|
| Voltage Scaling | 電壓縮放 | P ∝ VDD² |
| Multi-Vth | 多閾值電壓 | HVT/SVT/LVT 混合使用 |
| Power Gating | 電源閘控 | 切斷不用模組電源 |
| Clock Gating | 時脈閘控 | 關閉不用模組時脈 |
| DVFS | 動態電壓頻率調節 | 根據負載調整 V 和 f |
| Body Biasing | 體偏壓 | FBB 加速/RBB 省電 |
| FBB | 正向體偏壓 | Vt 降低 |
| RBB | 反向體偏壓 | Vt 升高 |
| PVT | 製程/電壓/溫度 | 三大變異來源 |
| Corner | 角點 | SS/TT/FF/SF/FS |
| Inter-die Variation | 全域變異 | 晶片間差異 |
| Intra-die Variation | 局部變異 | 晶片內差異 |
| Temperature Inversion | 溫度反轉 | 低 VDD 時的反直覺效應 |
| Scan Chain | 掃描鏈 | FF 串接成移位暫存器 |
| ATPG | 自動測試向量產生 | EDA 自動產生測試 |
| BIST | 內建自測試 | 晶片自己測自己 |
| Fault Coverage | 故障覆蓋率 | 偵測到的/總故障數 |
| Stuck-at Fault | 黏著故障 | SA0 或 SA1 |
| RTL | 暫存器轉移層級 | Verilog/VHDL |
| Synthesis | 邏輯合成 | RTL → 閘級網表 |
| P&R | 佈局與繞線 | 實體設計 |
| STA | 靜態時序分析 | 不需模擬的時序檢查 |
| Tapeout | 送廠 | 設計完成提交製造 |
| DRC | 設計規則檢查 | 製程限制驗證 |
| LVS | 佈局與電路比對 | 實體 vs 邏輯一致性 |
| Signoff | 簽核 | 最終驗證通過 |
| Retention Register | 保留暫存器 | Power Gating 時保存狀態 |
| Isolation Cell | 隔離單元 | 防止浮動信號 |

---

## 六、數值例題

### 例題 1：DVFS 省電計算

**題目**：一個處理器有三個工作模式：

| 模式 | VDD | 頻率 | 使用比例 |
|------|-----|------|---------|
| 高性能 | 1.0V | 3 GHz | 20% |
| 正常 | 0.8V | 2 GHz | 50% |
| 低功耗 | 0.6V | 1 GHz | 30% |

(a) 計算各模式的相對動態功率
(b) 平均動態功率是固定 1.0V/3GHz 的幾倍？

**解答**：

(a) P ∝ VDD² × f

```
P_high = (1.0)² × 3 = 3.0（基準）
P_norm = (0.8)² × 2 = 1.28
P_low  = (0.6)² × 1 = 0.36
```

(b) 使用 DVFS 的平均功率：
```
P_avg_DVFS = 0.2 × 3.0 + 0.5 × 1.28 + 0.3 × 0.36
           = 0.6 + 0.64 + 0.108
           = 1.348
```

固定 1.0V/3GHz 的功率：
```
P_fixed = 1.0 × 3.0 = 3.0
```

比值：
```
P_avg_DVFS / P_fixed = 1.348 / 3.0 = 0.449
```

**答：使用 DVFS 後，平均動態功率只有固定模式的 44.9%，節省了 55.1%**

---

### 例題 2：Multi-Vth 漏電分析

**題目**：一個模組有 100,000 個電晶體。
- LVT 漏電：100 nA/transistor
- SVT 漏電：10 nA/transistor
- HVT 漏電：1 nA/transistor
- VDD = 0.9V

方案 A：全部用 SVT
方案 B：70% HVT, 25% SVT, 5% LVT
比較兩方案的總漏電功率。

**解答**：

**方案 A**：
```
I_leak_A = 100,000 × 10 nA = 1,000,000 nA = 1 mA
P_leak_A = 1 mA × 0.9V = 0.9 mW
```

**方案 B**：
```
I_HVT = 70,000 × 1 nA = 70,000 nA
I_SVT = 25,000 × 10 nA = 250,000 nA
I_LVT = 5,000 × 100 nA = 500,000 nA
I_total = 820,000 nA = 0.82 mA

P_leak_B = 0.82 mA × 0.9V = 0.738 mW
```

**比較**：
```
P_leak_B / P_leak_A = 0.738 / 0.9 = 0.82
```

**答：方案 B 漏電功率為方案 A 的 82%，節省 18%**

> 注意：雖然 LVT 只佔 5%，但貢獻了 500,000/820,000 = 61% 的漏電！
> 這說明 **LVT 的使用要極其謹慎**。

---

### 例題 3：Power Gating 效益

**題目**：一個 SoC 中，GPU 模組的功耗 = 2W（包含動態 1.5W + 漏電 0.5W）。
GPU 在日常使用中 60% 的時間處於閒置狀態。
使用 Power Gating：
- 閒置時漏電降為 5 mW（sleep switch 漏電）
- 喚醒/休眠各需要 10 μs，功耗等效增加 0.1W
- 切換頻率：每秒平均 100 次

(a) 不用 Power Gating，GPU 平均功耗 = ?
(b) 使用 Power Gating，GPU 平均功耗 = ?

**解答**：

(a) 不使用 PG：
```
P_avg = 0.4 × 2W + 0.6 × 0.5W（閒置時仍有漏電）
      = 0.8 + 0.3
      = 1.1W
```

(b) 使用 PG：
```
活動時功耗 = 2W × 0.4 = 0.8W

閒置時功耗 = 0.005W × 0.6 = 0.003W

切換開銷 = 100 次/秒 × (10+10)μs × 等效功耗
         = 100 × 20×10⁻⁶ × (某平均功耗)
         → 簡化為題目給的等效增加 0.1W 的一部分

但題目說「功耗等效增加 0.1W」：
P_transition ≈ 0.1W × (切換時間佔比)
切換時間佔比 = 100 × 20μs = 2ms/s = 0.002
P_transition = 0.1W × 0.002 = 0.0002W ≈ 可忽略

更簡單的估算：
P_avg_PG = 0.4 × 2W + 0.6 × 0.005W + 小量切換開銷
         = 0.8 + 0.003 + ~0
         ≈ 0.803W
```

**節省**：
```
ΔP = 1.1 - 0.803 = 0.297W
節省比例 = 0.297/1.1 = 27%
```

**答：(a) 1.1W (b) ≈ 0.8W，節省約 27%**

---

### 例題 4：PVT Corner 時序分析

**題目**：一個電路在 TT/0.9V/25°C 下 fmax = 2 GHz。
各 corner 的延遲因子：

| Corner | 延遲因子（相對 TT） |
|--------|-------------------|
| SS/0.81V/125°C | 1.6× |
| FF/0.99V/-40°C | 0.7× |
| TT/0.9V/25°C | 1.0× |

(a) SS corner 的 fmax = ?
(b) 為了在 SS corner 達到 1.5 GHz，需要做什麼？

**解答**：

(a)
```
SS 延遲 = TT 延遲 × 1.6
Tclk_SS = Tclk_TT × 1.6 = (1/2GHz) × 1.6 = 500ps × 1.6 = 800ps

fmax_SS = 1/800ps = 1.25 GHz
```

(b) 要在 SS corner 達到 1.5 GHz：
```
需要 Tclk_SS = 1/1.5GHz = 667 ps
TT 下需要：Tclk_TT = 667/1.6 = 417 ps
TT 下 fmax 需要 = 1/417ps = 2.4 GHz
```

需要將 TT 下的設計從 2 GHz 提升到 2.4 GHz（**提升 20%**），方法包括：
- 最佳化關鍵路徑
- 使用更多 LVT 元件
- 增加管線化（Pipelining）
- 使用更先進的製程

**答：(a) 1.25 GHz (b) 需要在 TT 下達到 2.4 GHz 的設計**

---

### 例題 5：掃描鏈測試時間

**題目**：一個設計有 50,000 個掃描正反器，分成 10 條掃描鏈（每條 5,000 個 FF）。
掃描時脈頻率 = 100 MHz，需要 2,000 個測試向量。
(a) 每個向量的掃描時間
(b) 總測試時間

**解答**：

(a) 每條鏈有 5,000 個 FF，每個時脈移入/移出一個位元：
```
Shift 時間 = 5,000 / 100 MHz = 5,000 × 10 ns = 50 μs
Capture 時間 = 1 個時脈 = 10 ns（可忽略）

每個向量 ≈ 50 μs（shift-in）+ 10 ns（capture）+ 50 μs（shift-out）
但 shift-out 和下一個 shift-in 可以重疊（pipeline），所以：
每個向量 ≈ 50 μs + 10 ns ≈ 50 μs
```

(b) 總測試時間：
```
T_total = 2,000 × 50 μs + 50 μs（最後一個 shift-out）
        ≈ 2,000 × 50 μs
        = 100,000 μs
        = 100 ms = 0.1 秒
```

**答：(a) 每個向量 ≈ 50 μs (b) 總測試時間 ≈ 0.1 秒**

> 如果只有 1 條掃描鏈（50,000 個 FF）：
> 每個向量 = 500 μs → 總測試 = 1 秒
> 10 條鏈將測試時間縮短了 10 倍！

---

## 七、題型鑑別表

| 題目特徵 | 題型 | 方法 |
|---------|------|------|
| VDD 改變，求功率 | 電壓縮放 | P ∝ VDD² |
| 不同 Vth 比例 | Multi-Vth 分析 | 分別計算漏電 |
| 模組使用率和功耗 | Power Gating | 活動/閒置分別計算 |
| VDD 和 f 都變 | DVFS | P ∝ VDD² × f |
| 不同 corner 延遲 | PVT 分析 | 延遲因子乘算 |
| 掃描鏈配置 | DFT 測試時間 | 鏈長/頻率/向量數 |
| SoC 設計步驟 | 流程題 | Spec→RTL→Syn→P&R→Signoff |

---

## ✅ 自我檢測

### Q1：Multi-Vth 設計中，為什麼不全部用 HVT 來最小化漏電？

<details>
<summary>點擊展開答案</summary>

雖然 HVT 漏電最小，但 HVT 的速度也**最慢**。如果全部用 HVT：

1. **關鍵路徑速度不足**：高 Vt 意味著較小的驅動電流，延遲增大，可能無法達到目標頻率。

2. **需要更高的 VDD 來補償**：為了維持速度，可能需要提高 VDD → 動態功率增加（P ∝ VDD²）→ 可能得不償失。

所以最佳策略是**混合使用**：
- 關鍵路徑：LVT（維持速度）
- 非關鍵路徑：HVT（降低漏電）
- 中間路徑：SVT

這樣可以在**不犧牲速度**的前提下，最大程度降低漏電。

EDA 工具在合成和最佳化時會自動進行 Multi-Vth 分配。
</details>

### Q2：DVFS 切換時為什麼要「先降頻再降壓」（降壓時）和「先升壓再升頻」（升壓時）？

<details>
<summary>點擊展開答案</summary>

**降壓過程**（高性能 → 低功耗）：

如果先降壓再降頻：
- VDD 降低 → 電路速度變慢
- 頻率還沒降 → **可能產生 Setup Violation**（時脈太快，邏輯來不及）
- 導致功能錯誤

正確順序：
1. 先降頻（確保時序有餘量）
2. 再降壓（此時頻率已經夠低，不會違規）

**升壓過程**（低功耗 → 高性能）：

如果先升頻再升壓：
- 頻率升高 → 需要更快的速度
- VDD 還沒升 → **速度不夠 → Setup Violation**

正確順序：
1. 先升壓（提供足夠的驅動力）
2. 再升頻（此時速度已經足夠）

**一句話記憶**：永遠確保「電壓足以支撐當前頻率」。
</details>

### Q3：為什麼 SS corner 是 Setup 的最差情況，FF corner 是 Hold 的最差情況？

<details>
<summary>點擊展開答案</summary>

**SS（Slow-Slow）= Setup worst case**：
- 所有電晶體都慢 → 組合邏輯延遲 tlogic 最大
- Setup 約束：Tclk ≥ tcq + tlogic + tsu + tskew
- tlogic 最大 → 最容易違反 Setup → 需要最低的頻率

**FF（Fast-Fast）= Hold worst case**：
- 所有電晶體都快 → tlogic_min 更小
- Hold 約束：tcq + tlogic_min ≥ th + tskew
- tlogic_min 更小 → 左邊更小 → 更容易違反 Hold

所以：
- **STA Setup 分析**在 SS/low-V/high-T corner 進行
- **STA Hold 分析**在 FF/high-V/low-T corner 進行（但溫度反轉時要注意）
</details>

### Q4：掃描鏈為什麼要分成多條？只用一條不行嗎？

<details>
<summary>點擊展開答案</summary>

只用一條掃描鏈技術上可行，但有嚴重問題：

1. **測試時間太長**：如果有 100,000 個 FF，每次 shift 需要 100,000 個時脈週期。
   - 1 條鏈 × 100MHz = 每向量 1ms
   - 10 條鏈 × 100MHz = 每向量 0.1ms
   - **測試時間直接正比於鏈長**

2. **測試成本**：測試時間 = ATE（自動測試設備）使用時間 = 金錢。晶圓廠的 ATE 每小時成本可達數百美元。

3. **功率問題**：太長的鏈在 shift 時可能產生過大的切換功率。

分成 N 條鏈：
- 測試時間縮短 N 倍
- 需要 N 個 Scan-In 和 N 個 Scan-Out 引腳
- 通常分成 10~100 條鏈，平衡引腳數和測試時間

現代設計還使用**壓縮掃描（Compressed Scan）**技術（如 Synopsys DFTMAX），進一步減少測試向量數量和引腳需求。
</details>

### Q5：解釋 SoC 設計流程中 Synthesis 和 P&R 的主要區別。

<details>
<summary>點擊展開答案</summary>

**Synthesis（邏輯合成）**：
- 輸入：RTL（Verilog/VHDL）
- 輸出：Gate-level Netlist（閘級網表）
- 做什麼：將行為描述轉換為邏輯閘的連接
- 關注：邏輯最佳化、時序約束、功耗約束
- 此階段**不知道確切的物理位置**，只用估計的線延遲（Wire Load Model）
- 工具：Synopsys Design Compiler, Cadence Genus

**P&R（Place & Route，佈局與繞線）**：
- 輸入：Gate-level Netlist + 實體約束
- 輸出：GDS-II（含所有幾何圖形的檔案）
- 做什麼：決定每個元件的**物理位置**和**金屬線路徑**
- 關注：面積利用率、繞線壅塞、時脈樹、IR Drop
- 此階段知道**確切的寄生 RC**，可做精確時序分析
- 工具：Synopsys ICC2, Cadence Innovus

**關鍵區別**：Synthesis 是「邏輯世界」（抽象），P&R 是「物理世界」（實際佈局）。
合成後的設計可能在 P&R 後無法達到時序目標（因為實際線延遲比估計的大），需要反覆迭代。
</details>

---

## 八、本系列總結

恭喜你完成了 VLSI 設計的八章教學！以下是核心重點回顧：

| 章節 | 核心觀念 | 面試關鍵詞 |
|------|---------|----------|
| Ch1 CMOS反相器 | VTC、VM、雜訊邊限 | β ratio, NMH/NML |
| Ch2 動態特性 | tp = 0.69RC, P = αCV²f | 延遲、三種功耗 |
| Ch3 組合邏輯 | PDN/PUN互補、NAND優先 | 等效電阻法、Logical Effort |
| Ch4 動態邏輯 | 預充/求值、Domino | 電荷分享、keeper |
| Ch5 時序電路 | Setup/Hold Time | fmax 公式、Hold violation |
| Ch6 互連 | Elmore Delay、Buffer Insertion | 串擾Miller、IR Drop |
| Ch7 記憶體 | 6T SRAM、SNM | CR/PR ratio、讀穩定性 |
| Ch8 低功耗 | DVFS、Multi-Vth | PVT corner、DFT |

> **致讀者**：VLSI 設計涵蓋面極廣，本系列只是入門基礎。建議搭配 Rabaey 的
> 《Digital Integrated Circuits》和 Weste & Harris 的《CMOS VLSI Design》深入學習。
> 祝學習順利，面試成功！
