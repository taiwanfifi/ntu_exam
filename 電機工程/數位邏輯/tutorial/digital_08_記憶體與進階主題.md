# 數位邏輯教學講義 第八章：記憶體與進階主題

---

## 🔰 **本章基礎觀念（零基礎必讀）**

前七章涵蓋了數位邏輯的核心：數字系統、布林代數、組合邏輯、循序邏輯、FSM。
這最後一章要把視角拉高，看看數位系統設計的全貌：
記憶體怎麼存資料？可程式邏輯是什麼？晶片怎麼從設計到製造？

這些主題在業界面試中經常出現，尤其是 FPGA vs ASIC 比較、
時脈相關議題（Clock Skew, CDC, Metastability）、以及管線化設計。

> **學完本章，你應該能做到：**
> 1. 分辨 SRAM, DRAM, ROM, Flash 等記憶體的結構與用途
> 2. 理解 PLA, PAL, CPLD, FPGA 的差異
> 3. 解釋 Clock Skew 和 Metastability 的成因與解法
> 4. 理解管線化 (Pipelining) 如何提升 throughput
> 5. 知道 Booth 乘法器的基本原理
> 6. 描述 RTL 到 GDSII 的完整設計流程

---

## 關鍵術語表

| 中文 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| 靜態隨機存取記憶體 | SRAM | 用 6 個電晶體存 1 bit，快但貴 | CPU Cache |
| 動態隨機存取記憶體 | DRAM | 用 1 電晶體+1 電容存 1 bit，慢但便宜 | 主記憶體 DDR |
| 唯讀記憶體 | ROM | 資料寫入後不能（或很難）修改 | BIOS |
| 快閃記憶體 | Flash Memory | 可電子抹除的 ROM，非揮發性 | SSD, USB隨身碟 |
| 可程式邏輯陣列 | PLA | AND 和 OR 陣列都可程式化 | 早期邏輯實現 |
| 現場可程式閘陣列 | FPGA | 出廠後可反覆程式化的邏輯晶片 | 原型驗證 |
| 特定應用積體電路 | ASIC | 為特定用途量身設計的晶片 | 量產的手機晶片 |
| 時脈偏移 | Clock Skew | 時脈到不同 FF 的時間差 | 可能導致時序違規 |
| 跨時脈域 | CDC (Clock Domain Crossing) | 資料從一個時脈域傳到另一個 | 需要同步器 |
| 管線化 | Pipelining | 把長運算切成多段，提高吞吐量 | CPU 指令管線 |
| 暫存器傳輸層 | RTL (Register Transfer Level) | 用硬體描述語言寫的設計抽象層 | Verilog/VHDL |

---

## 一、記憶體分類

### 總覽

```
記憶體
├── 揮發性 (Volatile)：斷電就丟失
│   ├── SRAM（靜態）
│   └── DRAM（動態）
│
└── 非揮發性 (Non-Volatile)：斷電保持
    ├── ROM（唯讀）
    ├── PROM（可程式化一次）
    ├── EPROM（紫外線擦除）
    ├── EEPROM（電子擦除，按 Byte）
    └── Flash（電子擦除，按 Block）
```

### 1.1 SRAM (Static RAM)

**結構**：6 個電晶體 (6T Cell)

```
        WL (Word Line)
         │         │
    ┌────┤         ├────┐
    │    M5        M6    │
    │                     │
BL ─┤  ┌───┐   ┌───┐   ├─ BL'
    │  │INV1├───┤INV2│   │
    │  └───┘   └───┘   │
    │  (交叉耦合反相器)   │
    └─────────────────────┘
```

**讀取**：預充電 BL 和 BL'，開啟 WL，看 BL 和 BL' 的電壓差
**寫入**：驅動 BL 和 BL' 到目標值，開啟 WL

| 特性 | 說明 |
|------|------|
| 速度 | **非常快**（ns 等級） |
| 密度 | 低（6T = 面積大） |
| 功耗 | 靜態功耗低，但漏電流 |
| 不需要刷新 | 只要有電就保持 |
| 用途 | **CPU Cache (L1/L2/L3)**, 暫存器檔 |

### 1.2 DRAM (Dynamic RAM)

**結構**：1 個電晶體 + 1 個電容 (1T1C Cell)

```
    WL (Word Line)
     │
┌────┤
│    M1
│    │
BL ──┤
     │
    ═══ C (電容：存 1 = 充電，存 0 = 放電)
     │
    GND
```

**讀取**：預充電 BL，開啟 WL，電容與 BL 分享電荷，用感測放大器判讀
**寫入**：驅動 BL，開啟 WL，對電容充電/放電

| 特性 | 說明 |
|------|------|
| 速度 | 比 SRAM 慢 |
| 密度 | **非常高**（1T1C = 面積小） |
| 需要刷新 | 電容會漏電，需要定期(~64ms)刷新 |
| 讀取是破壞性的 | 讀完要寫回 |
| 用途 | **主記憶體 (DDR4/DDR5/LPDDR)** |

### SRAM vs DRAM 比較

| | SRAM | DRAM |
|--|------|------|
| 單元結構 | 6T | 1T1C |
| 速度 | 快 (< 1ns) | 慢 (~10ns) |
| 密度 | 低 | **高** |
| 成本/bit | 高 | **低** |
| 刷新 | 不需要 | 需要 |
| 功耗 | 低（靜態） | 高（刷新） |
| 典型用途 | Cache | 主記憶體 |

### 1.3 ROM 家族

| 類型 | 可寫次數 | 擦除方式 | 特點 |
|------|---------|---------|------|
| ROM | 0（製造時寫入） | 不能擦除 | 最便宜，量產用 |
| PROM | 1（使用者寫一次） | 不能擦除 | 用保險絲燒斷 |
| EPROM | 多次 | 紫外線（整顆） | 有石英窗 |
| EEPROM | 多次 | 電子（按 Byte） | 慢但靈活 |
| Flash | 多次 | 電子（按 Block） | **SSD、USB、手機儲存** |

> **Flash 分兩種**：
> - NOR Flash：可隨機存取，適合儲存程式碼(execute in place)
> - NAND Flash：循序存取，密度高，適合大量資料儲存(SSD)

---

## 二、可程式邏輯 (Programmable Logic)

### 2.1 PLA (Programmable Logic Array)

```
輸入 → [可程式 AND 陣列] → [可程式 OR 陣列] → 輸出
```

AND 和 OR 陣列都可以程式化 → 最靈活但最貴

### 2.2 PAL (Programmable Array Logic)

```
輸入 → [可程式 AND 陣列] → [固定 OR 陣列] → 輸出
```

只有 AND 陣列可程式化 → 比 PLA 便宜，夠用

### 2.3 CPLD (Complex PLD)

多個 PAL-like 的邏輯塊 + 可程式互連網路

### 2.4 FPGA (Field Programmable Gate Array)

```
┌─────────────────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ CLB │ │ CLB │ │ CLB │ │ CLB │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ CLB │ │ CLB │ │ CLB │ │ CLB │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│         可程式互連網路               │
│  ┌───┐ ┌───┐ ┌───┐                 │
│  │IOB│ │IOB│ │IOB│ ... (I/O Block) │
│  └───┘ └───┘ └───┘                 │
└─────────────────────────────────────┘

CLB = Configurable Logic Block
    = LUT (Look-Up Table) + FF + MUX
```

**LUT (查找表)**：本質上是一個小的 SRAM，實現任意 n 輸入布林函數。
例如 4-input LUT = 16-bit SRAM，可以實現任何 4 變數函數。

### FPGA vs ASIC 比較

| | FPGA | ASIC |
|--|------|------|
| 可重新程式化 | **是** | 否（製造後固定） |
| 開發時間 | **短**（數週到數月） | 長（數月到數年） |
| 開發成本 (NRE) | **低** | 非常高（光罩費用） |
| 單位成本 | 高 | **低**（量產後） |
| 性能 | 中等 | **高** |
| 功耗 | 高 | **低** |
| 適用場景 | 原型驗證、少量產品、需要更新 | 大量生產、高效能需求 |

> **經驗法則**：
> - 產量 < 10 萬：FPGA 可能更划算
> - 產量 > 100 萬：ASIC 一定更划算
> - 需要常更新：FPGA（如通訊基站）
> - 追求極致效能/功耗：ASIC（如手機 SoC）

---

## 三、時脈相關議題

### 3.1 時脈偏移 (Clock Skew)

**定義**：時脈信號到達不同 FF 的時間差。

```
CLK 源 ─────┬──── 長路徑 ────→ FF_A (CLK 到達較晚)
            │
            └──── 短路徑 ────→ FF_B (CLK 到達較早)

Skew = t_CLK_A - t_CLK_B
```

**影響**：

**正 Skew** (發送端 CLK 較早)：
- Setup time 約束變鬆（等效增加了可用時間）
- Hold time 約束變緊（可能違反！）

**負 Skew** (發送端 CLK 較晚)：
- Setup time 約束變緊（可能違反！）
- Hold time 約束變鬆

**考慮 Skew 的時序約束**：
```
Setup: tcq + tcomb + tsu ≤ T + t_skew    (正skew有利)
Hold:  tcq + tcomb ≥ th + t_skew          (正skew不利)
```

### 3.2 亞穩態 (Metastability)

（第五章已介紹基本概念，這裡深入討論解決方案）

**核心問題**：當非同步信號進入同步系統時，可能違反 setup/hold time。

**解決方案：兩級 FF 同步器 (Two-Flop Synchronizer)**

```
非同步信號 ─→ [D FF₁] ─→ [D FF₂] ─→ 同步後的信號
               ↑ CLK       ↑ CLK
```

**原理**：
1. FF₁ 可能進入亞穩態
2. 但一個時脈週期的時間通常足夠讓 FF₁ 解析(resolve)到 0 或 1
3. FF₂ 取樣到的就是穩定的值

**失敗機率** (MTBF, Mean Time Between Failures)：
```
MTBF = e^(t_resolve / τ) / (f_CLK × f_data × T₀)

t_resolve = 留給亞穩態解析的時間 = T - tsu - tcq
τ = FF 的亞穩態時間常數（由製程決定）
```

> **MTBF 隨 t_resolve 指數增長**，所以降低時脈頻率或使用三級 FF 可以大幅提升可靠性。

### 3.3 跨時脈域 (CDC, Clock Domain Crossing)

**問題**：當資料從時脈域 A（CLK_A）傳到時脈域 B（CLK_B）時，
CLK_A 和 CLK_B 沒有同步關係，接收端可能在任何時刻取樣。

**單 bit 信號**：用兩級 FF 同步器

**多 bit 信號**：
- **不能**對每個 bit 分別用同步器（不同 bit 可能在不同 CLK 邊緣被取樣）
- 解法1：**格雷碼計數器** + 同步器（FIFO 的讀寫指標）
- 解法2：**握手協議 (Handshake Protocol)**
- 解法3：**非同步 FIFO (Async FIFO)**

**非同步 FIFO 的關鍵設計**：
```
寫入時脈域：格雷碼寫指標 ──→ [2-FF同步器] ──→ 讀取時脈域
讀取時脈域：格雷碼讀指標 ──→ [2-FF同步器] ──→ 寫入時脈域

為什麼用格雷碼？
因為格雷碼每次只變 1 bit，即使同步有 1 cycle 延遲，
最多就是指標慢一個值（看起來 FIFO 比實際多一個/少一個），
不會出現完全錯誤的指標值。
```

---

## 四、管線化 (Pipelining)

### 4.1 基本概念

把一個長的組合邏輯路徑切成多段，每段之間插入暫存器(FF)。

```
無管線：
Input ──→ [Stage 1 + Stage 2 + Stage 3] ──→ Output
            ← ─ ─ ─ 30ns ─ ─ ─ →
            T = 30ns, f = 33MHz

有管線（3 段）：
Input → [Stage1] → FF → [Stage2] → FF → [Stage3] → Output
         10ns            10ns            10ns
         T = 10ns + overhead, f ≈ 100MHz
```

### 4.2 管線化的效果

| | 無管線 | 3 段管線 |
|--|--------|---------|
| 時脈週期 | 30ns | ~10ns + FF overhead |
| 時脈頻率 | 33 MHz | ~90 MHz |
| 延遲 (Latency) | 30ns (1 cycle) | ~30ns (3 cycles) |
| 吞吐量 (Throughput) | 33M ops/sec | ~90M ops/sec |

> **關鍵洞察**：
> - **Latency 不會改善**（甚至略增，因為 FF 有 overhead）
> - **Throughput 大幅提升**（因為多個資料同時在不同段處理）

### 4.3 管線冒險 (Pipeline Hazard)

在 CPU 的指令管線中會遇到三種 hazard：

1. **結構冒險 (Structural Hazard)**：硬體資源衝突（兩個指令同時需要同一個元件）
2. **資料冒險 (Data Hazard)**：後面的指令需要前面還沒算完的結果
3. **控制冒險 (Control Hazard)**：分支指令使得後續指令不確定

> 這些在計算機結構課程會深入探討。

---

## 五、算術電路

### 5.1 Booth 乘法器演算法

**問題**：二進位乘法需要很多次加法和移位，能不能減少？

**Booth 的想法**：利用 2's complement 的特性，把連續的 1 轉成減法。

```
例：A × 14
14 = 01110₂

普通乘法：A×01110 = A×(2³+2²+2¹) = 需要 3 次加法

Booth 觀察：01110 = 10000 - 00010 = 2⁴ - 2¹
A×01110 = A×(2⁴ - 2¹) = 只需要 1 次減法 + 1 次加法！
```

**Booth 演算法步驟**（Radix-2）：

1. 在乘數最右邊加一個 0（Q₋₁ = 0）
2. 從 LSB 開始，看每對相鄰位元 (Qᵢ, Qᵢ₋₁)：
   - (0,0) → 不做事，移位
   - (1,1) → 不做事，移位
   - (0,1) → **加** 被乘數，移位
   - (1,0) → **減** 被乘數，移位
3. 重複 n 次

**【例題 1】用 Booth 演算法計算 7 × 3**

```
被乘數 M = 7 = 0111
乘數 Q = 3 = 0011，Q₋₁ = 0

初始：A=0000, Q=0011, Q₋₁=0

Step 1：看 Q₀Q₋₁ = 10 → A = A - M = 0000 - 0111 = 1001
        算術右移：A=1100, Q=1001, Q₋₁=1

Step 2：看 Q₀Q₋₁ = 11 → 不做事
        算術右移：A=1110, Q=0100, Q₋₁=1

Step 3：看 Q₀Q₋₁ = 01 → A = A + M = 1110 + 0111 = 0101
        算術右移：A=0010, Q=1010, Q₋₁=0

Step 4：看 Q₀Q₋₁ = 00 → 不做事
        算術右移：A=0001, Q=0101, Q₋₁=0

結果：AQ = 00010101 = 21 ✓ (7×3=21)
```

### 5.2 Wallace Tree 乘法器

**概念**：用**進位儲存加法器 (Carry Save Adder, CSA)** 的樹狀結構，
平行壓縮部分積，減少加法層數。

```
普通陣列乘法器：  O(n) 層延遲
Wallace Tree：     O(log n) 層延遲
```

**核心技巧**：CSA 把三個數加在一起，產生兩個數（Sum 和 Carry），
而不是等進位傳播。這樣三個數變兩個數，反覆壓縮直到只剩兩個數，
最後用一個快速加法器（如 CLA）得到最終結果。

---

## 六、設計流程：RTL → 合成 → 佈局佈線

### 完整 IC 設計流程

```
1. 規格定義 (Specification)
     ↓
2. 架構設計 (Architecture Design)
     ↓
3. RTL 設計 (Register Transfer Level)
   用 Verilog 或 VHDL 撰寫
     ↓
4. 功能驗證 (Functional Verification)
   模擬(Simulation)、形式驗證(Formal Verification)
     ↓
5. 邏輯合成 (Logic Synthesis)
   RTL → 閘級網表 (Gate-level Netlist)
   工具：Synopsys Design Compiler
     ↓
6. 靜態時序分析 (STA, Static Timing Analysis)
   檢查所有路徑是否滿足時序約束
   工具：Synopsys PrimeTime
     ↓
7. 佈局 (Placement)
   決定每個邏輯閘的物理位置
     ↓
8. 繞線 (Routing)
   連接邏輯閘之間的金屬線
     ↓
9. 實體驗證 (Physical Verification)
   DRC (設計規則檢查), LVS (佈局vs電路圖比對)
     ↓
10. 產生 GDSII 檔案 → 送去晶圓廠製造
```

### 關鍵名詞解釋

**RTL (Register Transfer Level)**：
用硬體描述語言描述資料在暫存器之間的傳輸和運算。
這是工程師實際在寫的東西。

```verilog
// Verilog RTL 範例：D FF
always @(posedge clk) begin
    if (reset)
        q <= 0;
    else
        q <= d;
end
```

**邏輯合成 (Synthesis)**：
把 RTL 轉換成特定製程的邏輯閘。
合成工具會自動做布林化簡、映射到標準元件庫。

**STA (Static Timing Analysis)**：
不需要模擬輸入向量，直接分析所有路徑的延遲。
找出**最長路徑 (Critical Path)** 來確定最高時脈頻率。

---

## 七、題型鑑別表

| 題目關鍵字 | 該用什麼方法 |
|-----------|-------------|
| 「SRAM vs DRAM」 | 6T vs 1T1C，速度 vs 密度 |
| 「FPGA vs ASIC」 | 可重程式 vs 效能高，NRE 高低 |
| 「Clock Skew 影響」 | 修正 setup/hold 約束公式 |
| 「CDC 設計」 | 兩級 FF 同步器(單bit)，格雷碼(多bit) |
| 「Metastability MTBF」 | 指數公式，增加 resolve time |
| 「管線化效益」 | Throughput 提升，Latency 不變或略增 |
| 「Booth 演算法」 | 相鄰位元 00/11 不做事，01 加，10 減 |
| 「IC 設計流程」 | RTL → 合成 → STA → 佈局佈線 → GDSII |

---

## ✅ 自我檢測

### Q1：SRAM 和 DRAM 各用什麼結構？各適合什麼用途？

<details>
<summary>點擊查看答案</summary>

**SRAM**：
- 結構：6 個電晶體 (6T Cell) — 交叉耦合反相器 + 存取電晶體
- 不需要刷新
- 速度快，密度低，成本高
- 用途：**CPU Cache (L1/L2/L3)**

**DRAM**：
- 結構：1 個電晶體 + 1 個電容 (1T1C Cell)
- 需要定期刷新（電容漏電）
- 速度較慢，密度高，成本低
- 用途：**主記憶體 (DDR4/DDR5)**
</details>

### Q2：FPGA 和 ASIC 各適合什麼場景？列出至少3個比較面向。

<details>
<summary>點擊查看答案</summary>

| 面向 | FPGA | ASIC |
|------|------|------|
| 可重程式化 | 是 | 否 |
| 開發時間 | 短（數週） | 長（數月~年） |
| NRE 成本 | 低 | 非常高 |
| 單位成本 | 高 | 低（大量生產時） |
| 效能 | 中等 | 高 |
| 功耗 | 高 | 低 |

**FPGA 適合**：原型驗證、少量產品(< 10萬)、需要更新的產品
**ASIC 適合**：大量生產(> 100萬)、追求效能/功耗的產品（手機晶片）
</details>

### Q3：什麼是 Clock Skew？正 Skew 對 setup 和 hold 各有什麼影響？

<details>
<summary>點擊查看答案</summary>

**Clock Skew**：時脈信號到達不同 FF 的時間差。

**正 Skew**（發送端 CLK 先到，接收端 CLK 後到）：
- **Setup time 約束變鬆**：接收端 CLK 晚到，等於給了資料更多時間到達
  - 公式：tcq + tcomb + tsu ≤ T + t_skew
- **Hold time 約束變緊**：接收端 CLK 晚到，前一個資料存在的時間可能不夠
  - 公式：tcq_min + tcomb_min ≥ th + t_skew

> Hold violation 比 setup violation 更危險，因為無法靠降低時脈頻率來修正。
</details>

### Q4：為什麼跨時脈域(CDC)的多 bit 信號不能各自用獨立的同步器？該怎麼做？

<details>
<summary>點擊查看答案</summary>

**為什麼不行**：
各個 bit 的同步器可能在不同的時脈邊緣才穩定，導致接收端看到的多 bit 值
在某些時刻是「部分新值、部分舊值」的混合體。

例：計數器從 011→100，如果高位元先更新、低位元慢一拍，
接收端可能看到 000 或 111 這種根本不存在的值。

**正確做法**：
1. **格雷碼**：每次只變 1 bit，同步器最多延遲一個值，不會出現完全錯誤的值
   用途：非同步 FIFO 的讀寫指標
2. **握手協議**：用 request/acknowledge 信號確保雙方同意後才傳送
3. **非同步 FIFO**：結合格雷碼指標和兩級 FF 同步器
</details>

### Q5：管線化 (Pipelining) 如何提升效能？Latency 和 Throughput 各有什麼變化？

<details>
<summary>點擊查看答案</summary>

**原理**：把長的組合邏輯切成 k 段，每段之間插入 FF。
多筆資料可以同時在不同段被處理。

**Throughput（吞吐量）**：
- 無管線：f = 1/T_total
- k 段管線：f ≈ k/T_total（理想情況提升 k 倍）
- 實際提升比 k 小，因為 FF 有 overhead (tcq + tsu)

**Latency（延遲）**：
- 無管線：T_total
- k 段管線：k × (T_total/k + FF_overhead) ≈ T_total + k × FF_overhead
- **Latency 不會改善，通常略微增加**

> 管線化是用 Latency 的微小犧牲換取 Throughput 的大幅提升。
</details>

### Q6：Booth 演算法中，乘數相鄰位元 (Qᵢ, Qᵢ₋₁) = (1,0) 時要做什麼操作？

<details>
<summary>點擊查看答案</summary>

**(1,0) → 減去被乘數 (Subtract)**

完整規則：
| Qᵢ | Qᵢ₋₁ | 操作 |
|-----|-------|------|
| 0 | 0 | 不做事（移位） |
| 0 | 1 | **加**被乘數 |
| 1 | 0 | **減**被乘數 |
| 1 | 1 | 不做事（移位） |

直覺理解：
- (0,1) 表示一串 1 的結束（從 ...01 的角度看，這是正值的起點）
- (1,0) 表示一串 1 的開始（從 ...10 的角度看，這是需要減去的地方）

例如 0111₂ = 1000₂ - 0001₂，
在 bit 0 看到 (1,0) → 減，
在 bit 3 看到 (0,1) → 加。
</details>

---

## 八、本系列總結

恭喜你完成了數位邏輯的完整學習之旅！讓我們回顧一下八章的架構：

```
第1章：數字系統與編碼        → 數位世界的「語言」
第2章：布林代數與邏輯閘      → 數位世界的「文法」
第3章：卡諾圖化簡            → 優化表達的「技巧」
第4章：組合邏輯電路          → 「沒有記憶」的電路
第5章：正反器與循序邏輯基礎  → 「有記憶」的元件
第6章：同步循序電路設計      → 系統化的設計流程
第7章：有限狀態機應用        → 實戰應用
第8章：記憶體與進階主題      → 工程實務全貌
```

> **這些知識是所有數位 IC 設計的基礎。**
> 無論你未來做的是 CPU 設計、SoC 設計、FPGA 開發、還是嵌入式系統，
> 這些觀念都是你的根基。繼續加油！
