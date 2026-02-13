# EDA 01：IC 設計流程總覽

> **目標讀者**：零基礎學生、準備 TSMC / 聯發科面試者
> **預備知識**：無（本章為入門起點）
> **學習時間**：約 90 分鐘

---

## 🔰 本章基礎觀念（零基礎必讀）

### 什麼是 IC？

IC（Integrated Circuit，積體電路）就是把數以億計的電晶體（transistor）「做」在一小片矽晶片上。你手上的手機 SoC（如 Apple A17、聯發科天璣 9300）就是一顆 IC。

### 什麼是 EDA？

EDA（Electronic Design Automation，電子設計自動化）是設計 IC 所需的軟體工具。沒有 EDA，工程師不可能用人力畫出數十億個電晶體的電路。

### 一個比喻

把 IC 設計想像成蓋一棟超大型摩天樓：

| 蓋大樓 | IC 設計 |
|--------|---------|
| 建築師畫設計圖 | 電路設計工程師寫 RTL |
| 結構計算 | 時序分析（STA） |
| 施工藍圖 | 光罩（Mask） |
| 營造廠施工 | 晶圓代工廠（Fab）製造 |
| 驗收檢查 | 晶片測試（Test） |

---

## 一、從想法到晶片：IC 設計全流程

IC 設計是一個長鏈條，從最初的「想法」到最終的「可用晶片」，一般需要 **1～3 年**，花費 **數千萬至數十億美元**。

### 1.1 完整流程圖

```
                         IC 設計全流程
                         ============

 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │ 系統規格  │───▶│ 架構設計  │───▶│ RTL 設計  │───▶│ 功能驗證  │
 │  (Spec)  │    │  (Arch)  │    │ (Verilog) │    │(Simulation│
 └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                       │
       ┌───────────────────────────────────────────────┘
       ▼
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │ 邏輯合成  │───▶│ 實體設計  │───▶│ 時序簽核  │───▶│  光罩    │
 │(Synthesis)│   │  (P&R)   │    │ (Signoff) │    │(Tapeout) │
 └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                       │
       ┌───────────────────────────────────────────────┘
       ▼
 ┌──────────┐    ┌──────────┐    ┌──────────┐
 │  製造    │───▶│  封裝    │───▶│  測試    │
 │  (Fab)   │    │(Package) │    │  (Test)  │
 └──────────┘    └──────────┘    └──────────┘
```

### 1.2 各階段詳細說明

#### 階段 1：系統規格（System Specification）

- **做什麼**：定義晶片要實現的功能、性能指標、功耗預算、面積限制
- **產出**：規格書（Spec Document）
- **範例**：「設計一顆 5G 基頻晶片，支援 Sub-6GHz + mmWave，下行速率 10Gbps，功耗 < 5W」

#### 階段 2：架構設計（Architecture Design）

- **做什麼**：決定晶片內部模組劃分、匯流排架構、記憶體階層
- **工具**：SystemC、MATLAB、Python 模型
- **產出**：架構文件、功能模型（Functional Model）
- **關鍵決策**：硬體/軟體分割（HW/SW Partitioning）

#### 階段 3：RTL 設計（RTL Design）

- **做什麼**：用 HDL（Hardware Description Language）描述電路的暫存器傳輸層行為
- **語言**：Verilog / SystemVerilog / VHDL
- **產出**：RTL 程式碼
- **比喻**：這就像用程式語言「寫」出硬體電路

```verilog
// 簡單的 RTL 範例：4-bit 加法器
module adder4 (
    input  [3:0] a, b,
    input        cin,
    output [3:0] sum,
    output       cout
);
    assign {cout, sum} = a + b + cin;
endmodule
```

#### 階段 4：功能驗證（Functional Verification）

- **做什麼**：確認 RTL 行為正確，沒有邏輯 bug
- **方法**：
  - 模擬（Simulation）：用 testbench 測試
  - 形式驗證（Formal Verification）：數學證明
  - 硬體加速（Emulation）：用 FPGA 加速驗證
- **工具**：VCS (Synopsys)、Xcelium (Cadence)、Questa (Siemens EDA)
- **現實**：驗證消耗整個設計流程 **60～70%** 的工時

#### 階段 5：邏輯合成（Logic Synthesis）

- **做什麼**：把 RTL 轉換成由標準元件（Standard Cell）組成的閘級網表（Gate-level Netlist）
- **工具**：Design Compiler (Synopsys)、Genus (Cadence)
- **輸入**：RTL + 標準元件庫（Standard Cell Library）+ 時序約束（SDC）
- **產出**：Gate-level Netlist

```
RTL 程式碼 ──→ [邏輯合成] ──→ 由 AND、OR、FF 等閘組成的網表
              ↑
         標準元件庫 + 時序約束
```

#### 階段 6：實體設計（Physical Design / Place & Route, P&R）

- **做什麼**：把閘級網表中的元件「擺」在晶片上，並「拉」線連接
- **子步驟**：
  1. 晶片規劃（Floorplanning）
  2. 佈局（Placement）
  3. 時脈樹合成（Clock Tree Synthesis, CTS）
  4. 繞線（Routing）
- **工具**：IC Compiler II (Synopsys)、Innovus (Cadence)

#### 階段 7：時序簽核（Signoff）

- **做什麼**：最終確認設計滿足時序、功耗、可靠性等所有要求
- **檢查項目**：
  - STA（Static Timing Analysis）：時序是否 meet？
  - DRC（Design Rule Check）：佈局是否符合製程規則？
  - LVS（Layout vs. Schematic）：佈局是否與電路一致？
  - IR Drop：電源供應是否穩定？
  - EM（Electromigration）：電流密度是否安全？

#### 階段 8：光罩（Tapeout）

- **做什麼**：把最終設計資料（GDS/OASIS 格式）送到光罩廠製作光罩
- **重要性**：Tapeout 後就不能改了，錯了就要重新製作光罩（每組光罩數百萬至上千萬美元）
- **術語由來**：早期設計資料存在磁帶（tape）上送出去，所以叫 tape-out

#### 階段 9：製造（Fabrication）

- **做什麼**：晶圓代工廠用光罩把電路「印」到矽晶圓上
- **主要廠商**：TSMC（台積電）、Samsung、Intel Foundry
- **週期**：約 2～3 個月

#### 階段 10：封裝（Packaging）

- **做什麼**：把晶粒（Die）裝進封裝體，引出腳位
- **類型**：Wire Bond、Flip-Chip、2.5D/3D、CoWoS、InFO

#### 階段 11：測試（Testing）

- **做什麼**：用 ATE（Automatic Test Equipment）測試每顆晶片是否正常
- **階段**：晶圓測試（CP）→ 封裝後測試（FT）

---

## 二、前段（Front-end）vs 後段（Back-end）設計

IC 設計分成兩大團隊，職責截然不同：

| 比較項目 | 前段（Front-end） | 後段（Back-end） |
|---------|-------------------|-----------------|
| **工作內容** | RTL 設計 + 功能驗證 | 邏輯合成 + 實體設計 + 簽核 |
| **核心技能** | Verilog / SystemVerilog | STA / P&R / DRC / LVS |
| **輸出** | RTL 程式碼 | GDS/OASIS 檔案 |
| **思維方式** | 像軟體工程師 | 像土木工程師 |
| **工具** | VCS, Verdi | ICC2, Innovus, PrimeTime |
| **面試重點** | 數位邏輯、FSM、時序電路 | STA、P&R flow、製程知識 |

### 前段工程師的一天

1. 早上：Review RTL code，修 bug
2. 下午：跑模擬（Simulation），分析波形
3. 晚上：等 Regression test 結果

### 後段工程師的一天

1. 早上：跑合成（Synthesis），調整時序約束
2. 下午：分析 timing violation，修 critical path
3. 晚上：跑 P&R，等 DRC/LVS clean

---

## 三、EDA 工具生態

### 3.1 三大 EDA 公司

```
        EDA 產業三巨頭
        ===============

  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Synopsys   │  │   Cadence   │  │ Siemens EDA │
  │  (新思科技)   │  │  (益華電腦)  │  │(原 Mentor)  │
  │  市佔 ~32%   │  │  市佔 ~28%  │  │  市佔 ~15%  │
  └─────────────┘  └─────────────┘  └─────────────┘
```

### 3.2 各階段主要 EDA 工具

| 設計階段 | Synopsys | Cadence | Siemens EDA |
|---------|----------|---------|-------------|
| RTL 模擬 | VCS | Xcelium | Questa |
| 邏輯合成 | Design Compiler (DC) | Genus | — |
| 形式驗證 | Formality | Conformal | — |
| STA | PrimeTime (PT) | Tempus | — |
| P&R | IC Compiler II (ICC2) | Innovus | — |
| DRC/LVS | IC Validator | Pegasus | Calibre ★ |
| 功耗分析 | PrimePower | Voltus | — |
| 寄生萃取 | StarRC | Quantus | — |
| SPICE 模擬 | HSPICE | Spectre | — |
| PCB 設計 | — | Allegro | HyperLynx |
| DFT | DFT Compiler | Modus | Tessent ★ |

> **★** 表示該領域的業界標準工具

### 3.3 EDA 工具鏈（Tool Chain）

一個典型的後段設計流程（以 Synopsys 為例）：

```
Verilog RTL
    │
    ▼
┌──────────────────┐
│ Design Compiler  │ ← 邏輯合成
│ (DC)             │
└──────────────────┘
    │  Gate-level Netlist
    ▼
┌──────────────────┐
│ IC Compiler II   │ ← 實體設計 (P&R)
│ (ICC2)           │
└──────────────────┘
    │  Layout (DEF)
    ▼
┌──────────────────┐
│ StarRC           │ ← 寄生萃取
└──────────────────┘
    │  SPEF
    ▼
┌──────────────────┐
│ PrimeTime (PT)   │ ← 靜態時序分析
└──────────────────┘
    │  Timing Report
    ▼
┌──────────────────┐
│ IC Validator     │ ← DRC / LVS
└──────────────────┘
    │  Clean? → Tapeout!
```

---

## 四、設計抽象層次

IC 設計有多個抽象層次，從最高層到最低層：

```
高
▲   ┌──────────────────────────────────┐
│   │ 系統層（System Level）             │  "晶片要做什麼？"
│   │ 工具：SystemC, MATLAB             │
│   ├──────────────────────────────────┤
│   │ 行為層（Behavioral Level）         │  "演算法怎麼跑？"
│   │ 工具：C/C++ Model                 │
│   ├──────────────────────────────────┤
│   │ RTL層（Register Transfer Level）   │  "暫存器間怎麼傳？"
│   │ 工具：Verilog, VHDL               │
│   ├──────────────────────────────────┤
│   │ 閘層（Gate Level）                 │  "用哪些邏輯閘？"
│   │ 工具：Design Compiler              │
│   ├──────────────────────────────────┤
│   │ 電晶體層（Transistor Level）       │  "幾個電晶體？"
│   │ 工具：HSPICE, Spectre              │
│   ├──────────────────────────────────┤
│   │ 佈局層（Layout / Physical Level）  │  "擺哪裡？怎麼連？"
│   │ 工具：ICC2, Innovus                │
低  └──────────────────────────────────┘
```

### 各層的資訊量對照

| 抽象層次 | 設計單元 | 數量級（以手機 SoC 為例） |
|---------|---------|--------------------------|
| 系統層 | 功能模組 | ~10 個 |
| RTL 層 | 暫存器、MUX、ALU | ~百萬 |
| 閘層 | AND, OR, FF | ~十億 |
| 電晶體層 | NMOS, PMOS | ~百億 |
| 佈局層 | 幾何形狀（polygon） | ~千億 |

### 為什麼需要抽象？

因為人腦無法直接處理百億個電晶體。每一層只關心自己該處理的細節，上層交給自動化工具去展開。

---

## 五、Gajski-Kuhn Y-Chart（設計三域圖）

Y-Chart 是理解 IC 設計的經典框架，將設計空間分為三個域：

```
              行為域
             (Behavioral)
               /\
              /  \
             /    \
            /      \
           /        \
          /    IC    \
         /   設計    \
        /    空間     \
       /              \
      /________________\
  結構域              實體域
(Structural)      (Physical)
```

| 域 | 描述 | 範例 |
|---|------|------|
| 行為域 | 電路「做什麼」 | 演算法、真值表、布林方程式 |
| 結構域 | 電路「由什麼組成」 | 模組、閘、電晶體 |
| 實體域 | 電路「長什麼樣」 | 晶片佈局、繞線 |

---

## 六、設計流程中的重要檔案格式

| 檔案格式 | 全名 | 用途 |
|---------|------|------|
| `.v` / `.sv` | Verilog / SystemVerilog | RTL 原始碼 |
| `.vhd` | VHDL | RTL 原始碼（歐洲常用） |
| `.sdc` | Synopsys Design Constraints | 時序約束 |
| `.lib` | Liberty | 標準元件庫時序/功耗 |
| `.lef` | Library Exchange Format | 元件庫實體資訊 |
| `.def` | Design Exchange Format | 設計實體資訊（佈局結果） |
| `.spef` | Standard Parasitic Exchange Format | 寄生參數 |
| `.gds` / `.oas` | GDS II / OASIS | 光罩資料（最終產出） |
| `.sdf` | Standard Delay Format | 延遲資訊（用於 gate-level simulation） |

---

## 七、IC 設計的現實面

### 7.1 設計成本

| 製程節點 | 一次光罩費用 | 完整設計成本（含人力） |
|---------|------------|---------------------|
| 28nm | ~$500萬 | ~$5,000萬 |
| 7nm | ~$3,000萬 | ~$3億 |
| 5nm | ~$5,000萬 | ~$5億 |
| 3nm | ~$7,000萬+ | ~$7億+ |

### 7.2 設計時程（典型數位 SoC）

| 階段 | 時間 |
|------|------|
| 架構設計 + RTL | 6～12 個月 |
| 驗證 | 6～18 個月 |
| 後段設計 | 3～6 個月 |
| 製造 + 封測 | 3～4 個月 |
| **合計** | **18～40 個月** |

### 7.3 為什麼不能出錯？

- 一組 3nm 光罩成本超過 **7,000 萬美元**
- 如果 Tapeout 後發現 bug → 必須做 Metal ECO 或完全重來
- Metal ECO：只改金屬層光罩（改 1～2 層），成本較低但受限
- Full Re-spin：全部光罩重做 → 數千萬美元 + 數月延誤

---

## 關鍵術語表

| 術語 | 英文全名 | 說明 |
|------|---------|------|
| IC | Integrated Circuit | 積體電路 |
| EDA | Electronic Design Automation | 電子設計自動化 |
| SoC | System on Chip | 系統單晶片 |
| RTL | Register Transfer Level | 暫存器傳輸層 |
| HDL | Hardware Description Language | 硬體描述語言 |
| STA | Static Timing Analysis | 靜態時序分析 |
| P&R | Place and Route | 佈局與繞線 |
| DRC | Design Rule Check | 設計規則檢查 |
| LVS | Layout vs. Schematic | 佈局對電路驗證 |
| GDS | Graphic Data System | 光罩資料格式 |
| SDC | Synopsys Design Constraints | 時序約束格式 |
| CTS | Clock Tree Synthesis | 時脈樹合成 |
| ECO | Engineering Change Order | 工程變更命令 |
| Fab | Fabrication | 晶圓製造廠 |
| Tapeout | — | 設計資料送出製造 |
| Die | — | 晶粒（切割前的晶片） |
| Wafer | — | 矽晶圓 |
| ATE | Automatic Test Equipment | 自動測試設備 |
| DFT | Design for Testability | 可測試性設計 |
| IP | Intellectual Property | 矽智財（可重複使用的設計模組） |

---

## 題型鑑別

| 看到什麼關鍵字 | 屬於哪個階段 | 答題方向 |
|---------------|------------|---------|
| RTL、Verilog、FSM | 前段設計 | 寫程式碼、畫狀態圖 |
| Synthesis、Netlist | 邏輯合成 | 標準元件、最佳化 |
| STA、Setup、Hold | 時序分析 | 計算 Slack |
| Placement、Routing | 實體設計 | 演算法、HPWL |
| DRC、LVS | 簽核 | 規則違規分析 |
| Tapeout、GDS | 光罩製作 | 檔案格式 |
| Yield、Test、DFT | 測試 | 故障模型、覆蓋率 |

---

## ✅ 自我檢測

### 基礎題

<details>
<summary>Q1：IC 設計流程中，「邏輯合成」的輸入和輸出分別是什麼？</summary>

**答案**：
- **輸入**：RTL 程式碼（Verilog/VHDL）、標準元件庫（Liberty .lib）、時序約束（SDC）
- **輸出**：閘級網表（Gate-level Netlist），由標準元件（AND, OR, FF 等）組成
</details>

<details>
<summary>Q2：前段（Front-end）工程師和後段（Back-end）工程師的主要工作差異是什麼？</summary>

**答案**：
- **前段**：RTL 設計 + 功能驗證，核心技能是 Verilog/SystemVerilog，像軟體工程師
- **後段**：邏輯合成 + 實體設計（P&R）+ 時序簽核，核心技能是 STA、P&R flow，像土木工程師
</details>

<details>
<summary>Q3：為什麼功能驗證會消耗整個 IC 設計流程 60～70% 的工時？</summary>

**答案**：
1. 現代 SoC 功能極為複雜，包含數十個子系統
2. 需要驗證所有可能的輸入組合（狀態空間巨大）
3. 需要覆蓋邊界條件、例外情況
4. Bug 如果到 Tapeout 後才發現，修復成本極高（數千萬美元）
5. 因此寧可在驗證階段多花時間，也不要帶 bug 進製造
</details>

<details>
<summary>Q4：列舉三大 EDA 公司及各自的招牌工具</summary>

**答案**：
1. **Synopsys**（新思科技）：VCS（模擬）、Design Compiler（合成）、PrimeTime（STA）、ICC2（P&R）
2. **Cadence**（益華電腦）：Xcelium（模擬）、Genus（合成）、Tempus（STA）、Innovus（P&R）
3. **Siemens EDA**（原 Mentor）：Questa（模擬）、Calibre（DRC/LVS，業界標準）、Tessent（DFT）
</details>

### 進階題

<details>
<summary>Q5：什麼是 Metal ECO？和 Full Re-spin 的差異？</summary>

**答案**：
- **Metal ECO**（Engineering Change Order）：只修改金屬層（上層幾層），不動電晶體層。只需重做少數幾張光罩，成本約為完整光罩組的 10～20%。但功能修改受限於已有的電晶體
- **Full Re-spin**：所有光罩全部重做，可以修改任何部分，但成本極高（3nm 光罩組 > 7,000 萬美元）且需額外等待 2～3 個月製造時間
</details>

<details>
<summary>Q6：Y-Chart 的三個域分別代表什麼？</summary>

**答案**：
1. **行為域（Behavioral）**：描述電路「做什麼」→ 演算法、真值表、傳輸函數
2. **結構域（Structural）**：描述電路「由什麼組成」→ 模組、閘、電晶體
3. **實體域（Physical）**：描述電路「長什麼樣」→ 晶片佈局、繞線幾何

每個域都有不同的抽象層次（系統→RTL→閘→電晶體）
</details>

<details>
<summary>Q7：為什麼先進製程（如 3nm）的設計成本遠高於成熟製程（如 28nm）？</summary>

**答案**：
1. **光罩成本暴增**：先進製程需要 EUV 光罩，成本遠高於 DUV
2. **設計複雜度**：更多設計規則（DRC rules 數量從 28nm 的 ~500 條增加到 3nm 的 ~5000 條）
3. **更多金屬層**：先進製程可能有 15+ 層金屬，繞線更複雜
4. **驗證難度**：更多寄生效應需要考慮
5. **人力成本**：需要更多工程師、更長開發時間
6. **EDA 工具授權費**：先進節點的工具更貴
</details>

<details>
<summary>Q8：請按正確順序排列：CTS → DRC → Placement → Floorplanning → Routing → LVS</summary>

**答案**：
正確順序：
1. **Floorplanning**（晶片規劃）
2. **Placement**（元件佈局）
3. **CTS**（時脈樹合成）
4. **Routing**（繞線）
5. **DRC**（設計規則檢查）
6. **LVS**（佈局對電路驗證）
</details>

---

> **下一章**：[eda_02_IC製程基礎_氧化擴散佈植.md](eda_02_IC製程基礎_氧化擴散佈植.md) —— 進入晶圓製造的物理世界
