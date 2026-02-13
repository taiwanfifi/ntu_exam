# EDA 05：邏輯合成與時序分析

> **目標讀者**：零基礎學生、準備 TSMC / 聯發科後段設計工程師面試者
> **預備知識**：基礎數位邏輯（AND, OR, NOT, Flip-Flop 概念）
> **學習時間**：約 120 分鐘

---

## 🔰 本章基礎觀念（零基礎必讀）

### 邏輯合成是什麼？一句話

邏輯合成就是把你寫的 Verilog 程式碼（RTL）**自動轉換**成由真實邏輯閘（AND, OR, FF...）組成的電路。

### STA 是什麼？一句話

STA（靜態時序分析）就是在不跑模擬的情況下，**數學計算**電路中所有路徑的延遲，確認信號是否來得及在時脈邊緣前到達。

### 為什麼這兩個概念超級重要？

- **邏輯合成**是前段設計（RTL）和後段設計（P&R）之間的**橋梁**
- **STA** 是所有後段設計工程師的**每日必用技能**
- 面試問 STA 的機率 > 90%（TSMC、聯發科、Synopsys 都會問）

### 生活比喻

| EDA 概念 | 生活比喻 |
|---------|---------|
| RTL 程式碼 | 用文字描述一棟房子的功能需求 |
| 邏輯合成 | 建築師把需求轉換成具體的建築藍圖 |
| 標準元件庫 | 建材目錄（磚塊、鋼筋、門窗的規格） |
| STA | 計算每條管線的水壓和流速是否足夠 |
| Setup Time | 水龍頭打開後，水要在截止時間前到達 |
| Hold Time | 水龍頭打開後，水流不能太快斷掉 |

---

## 一、邏輯合成（Logic Synthesis）

### 1.1 合成的輸入與輸出

```
         輸入                                輸出
    ┌──────────┐                       ┌──────────────┐
    │ RTL 程式碼 │                       │ Gate-level    │
    │ (Verilog) │───┐                   │ Netlist       │
    └──────────┘   │                   │ (閘級網表)     │
                    │  ┌────────────┐   └──────────────┘
    ┌──────────┐   ├─▶│  邏輯合成   │──▶
    │ 標準元件庫 │───┤  │ (Synthesis)│   ┌──────────────┐
    │ (.lib)   │   │  └────────────┘   │ 時序報告       │
    └──────────┘   │                   │ (Timing Report)│
                    │                   └──────────────┘
    ┌──────────┐   │
    │ 時序約束   │───┘
    │ (.sdc)   │
    └──────────┘
```

### 1.2 合成的三大步驟

```
    RTL
     │
     ▼
 ┌──────────────┐
 │ ① 轉譯       │  RTL → 通用布林方程式
 │ (Translation) │  （還不用真實元件）
 └──────────────┘
     │
     ▼
 ┌──────────────┐
 │ ② 最佳化      │  簡化布林函數
 │(Optimization) │  面積/速度/功耗 取捨
 └──────────────┘
     │
     ▼
 ┌──────────────┐
 │ ③ 技術映射    │  用標準元件庫中的真實閘
 │ (Tech Mapping)│  取代通用邏輯
 └──────────────┘
     │
     ▼
  Gate-level Netlist
```

### 1.3 高階合成（HLS, High-Level Synthesis）簡介

| 比較 | RTL 合成 | 高階合成（HLS） |
|------|---------|----------------|
| 輸入 | Verilog/VHDL | C/C++/SystemC |
| 自動化程度 | 中 | 高 |
| 設計效率 | 低（需手動寫 RTL） | 高 |
| 品質（PPA） | 好 | 中等（但在進步中） |
| 工具 | DC, Genus | Vitis HLS (Xilinx), Catapult (Siemens) |

HLS 讓設計師用高階語言描述演算法，工具自動產生 RTL。適用於複雜演算法的快速原型（如影像處理、機器學習加速器）。

---

## 二、布林函數表示

### 2.1 真值表

最直接的表示法，但大小隨輸入數**指數成長**（$n$ 個輸入 → $2^n$ 行）。

```
  a  b  c │ f
  ────────┼───
  0  0  0 │ 0
  0  0  1 │ 1
  0  1  0 │ 0
  0  1  1 │ 1
  1  0  0 │ 0
  1  0  1 │ 1
  1  1  0 │ 1
  1  1  1 │ 1

  → f = ab + c（SOP 形式）
```

### 2.2 SOP 與 POS

- **SOP（Sum of Products）**：$f = \overline{a}c + bc + ab$
- **POS（Product of Sums）**：$f = (a+c)(b+c)(\overline{a}+b)$

### 2.3 BDD（Binary Decision Diagram）

BDD 是用有向無環圖（DAG）表示布林函數。

```
     BDD 表示 f = ab + c

           a
          / \
         0   1
        /     \
       b       b
      / \     / \
     0   1   0   1
    /   / \ /   / \
   c   c   1   1   1
  / \ / \
 0   1 0  1

 簡化後（合併等價節點）→ ROBDD
```

### 2.4 ROBDD（Reduced Ordered BDD）

ROBDD 是 BDD 的簡化版，有兩個重要性質：

1. **有序（Ordered）**：變數順序固定（例如 $a > b > c$）
2. **簡化（Reduced）**：
   - 合併等價的子圖
   - 消除冗餘節點（兩個子節點相同的節點）

**ROBDD 的關鍵定理**：給定變數順序，ROBDD 是**唯一的**（Canonical）。

這意味著：
- 判斷兩個布林函數是否等價 → 比較 ROBDD 是否相同 → O(1)
- 但不同的變數順序可能產生不同大小的 ROBDD

### 2.5 變數順序的影響 ★

```
  f = a₁b₁ + a₂b₂

  好的順序 (a₁, b₁, a₂, b₂)：       壞的順序 (a₁, a₂, b₁, b₂)：
  節點數 = O(n)                      節點數 = O(2^n)

  ┌─────┐                           ┌─────────────┐
  │ 小圖 │                           │   超大的圖    │
  └─────┘                           └─────────────┘
```

- 找最佳變數順序是 **NP-hard** 問題
- 實務上用啟發式方法（heuristic）找次佳順序

---

## 三、邏輯最佳化

### 3.1 兩階最佳化（Two-Level Optimization）

目標：找到最簡的 SOP 或 POS 表示。

#### Karnaugh Map（卡諾圖）

適用於 ≤ 6 個變數，手動最簡化。

#### Espresso 算法 ★

- 用於自動化兩階邏輯最佳化
- 不保證最佳解，但實際上幾乎都是最佳
- 三個核心操作：EXPAND（擴大）、REDUCE（縮小）、IRREDUNDANT（去冗餘）
- 時間複雜度遠低於窮舉法

### 3.2 多階最佳化（Multi-Level Optimization）

現實 IC 不會只用兩階邏輯（閘數太多、延遲太大）。多階最佳化將邏輯拆成多層：

#### 常見操作

| 操作 | 說明 | 效果 |
|------|------|------|
| **分解（Decomposition）** | 把大函數拆成小函數的組合 | 減少面積 |
| **提取（Extraction）** | 找出共同子表達式 | 減少重複邏輯 |
| **替換（Substitution）** | 用已有的邏輯重組 | 進一步簡化 |
| **消除（Elimination）** | 合併中間節點 | 可能減少延遲 |

### 3.3 技術映射（Technology Mapping）

將通用邏輯閘映射到**標準元件庫（Standard Cell Library）**中的真實元件。

```
  通用邏輯                   標準元件庫
  ─────────                 ─────────
  AND2, OR2,      ──→      NAND2_X1  (面積小，慢)
  INV, XOR...     映射      NAND2_X2  (面積中，中速)
                           NAND2_X4  (面積大，快)
                           NOR2_X1
                           AOI21_X1  (AND-OR-INV)
                           OAI22_X2  (OR-AND-INV)
                           DFF_X1    (正反器)
                           ...
```

映射時需要考慮：
- **面積**：用小元件 → 面積小但可能較慢
- **速度**：用大元件（驅動力強）→ 快但面積大
- **功耗**：速度和面積都影響功耗

工具會根據 SDC 約束自動選擇最合適的元件大小。

---

## 四、靜態時序分析（STA）★面試重點中的重點

### 4.1 什麼是 STA？

STA 分析電路中**所有可能的路徑**延遲，不需要輸入向量（不跑模擬）。

| 比較 | 動態時序分析 | 靜態時序分析（STA） |
|------|------------|-------------------|
| 方法 | 模擬（Simulation） | 數學計算 |
| 需要輸入向量？ | 是 | **否** |
| 覆蓋率 | 取決於測試向量 | **100% 路徑覆蓋** |
| 速度 | 慢 | **快** ★ |
| 工具 | VCS + SDF | PrimeTime, Tempus |

### 4.2 基本時序模型

考慮最簡單的時序電路：兩個正反器（FF）之間有組合邏輯。

```
     Launch FF          組合邏輯           Capture FF
    ┌─────────┐     ┌──────────────┐    ┌─────────┐
    │         │     │              │    │         │
CLK─┤ D    Q  ├────▶│  delay path  ├───▶│ D    Q  ├──▶
    │         │     │              │    │         │
    │   FF1   │     └──────────────┘    │   FF2   │
    └────┬────┘                         └────┬────┘
         │                                    │
         └──────────── CLK ──────────────────┘
                       (可能有 skew)
```

### 4.3 到達時間、要求時間、鬆弛量

| 術語 | 英文 | 定義 |
|------|------|------|
| **到達時間** | Arrival Time (AT) | 信號從源頭到達某節點的**實際時間** |
| **要求時間** | Required Time (RT) | 信號**必須**在此時間前到達才能正常工作 |
| **鬆弛量** | Slack | RT - AT。Slack ≥ 0 → 時序滿足；Slack < 0 → 時序違規 |

### 4.4 Setup Time 檢查 ★★★

**Setup Time ($t_{setup}$)**：資料必須在時脈邊緣**之前**穩定的最小時間。

```
    時序圖（Setup 檢查）
    ====================

CLK  ─────┐         ┌─────────┐         ┌──────
          │         │         │         │
          └─────────┘         └─────────┘
          ←── Tclk ──▶

Data ─────────────────╲
                       ╲───────────────────────
          ← tcq+tlogic ▶← tsetup ▶

          資料必須在 Capture edge 前 tsetup 到達
```

#### Setup Slack 公式

$$\boxed{\text{Setup Slack} = T_{clk} - (t_{cq} + t_{logic} + t_{setup}) - t_{skew_{pessimistic}}}$$

更精確的版本（考慮時脈偏移方向）：

$$\boxed{\text{Setup Slack} = (T_{clk} + t_{skew}) - (t_{cq} + t_{logic} + t_{setup})}$$

其中：
- $T_{clk}$：時脈週期
- $t_{cq}$：Launch FF 的 clock-to-Q 延遲
- $t_{logic}$：組合邏輯延遲（取最長路徑）
- $t_{setup}$：Capture FF 的 setup time
- $t_{skew} = t_{clk2} - t_{clk1}$：時脈偏移（正值表示 Capture CLK 較晚到達）

**Setup Slack ≥ 0 → PASS；Setup Slack < 0 → FAIL（時序違規）**

### 4.5 Hold Time 檢查 ★★★

**Hold Time ($t_{hold}$)**：資料必須在時脈邊緣**之後**繼續穩定的最小時間。

```
    時序圖（Hold 檢查）
    ==================

CLK  ─────┐         ┌──────
          │         │
          └─────────┘

Data ──────╲                    新資料太快到達！
            ╲──────             會覆蓋掉正在被捕捉的舊資料
          ← thold ▶

          資料必須在 Capture edge 後 thold 保持穩定
```

#### Hold Slack 公式

$$\boxed{\text{Hold Slack} = (t_{cq} + t_{logic}) - (t_{hold} + t_{skew})}$$

其中 $t_{skew} = t_{clk2} - t_{clk1}$（與 Setup 定義相同）。

**Hold Slack ≥ 0 → PASS；Hold Slack < 0 → FAIL**

### 4.6 Setup vs Hold 的關鍵差異 ★面試常問

| 比較項目 | Setup 違規 | Hold 違規 |
|---------|-----------|----------|
| 問題 | 資料到得**太慢** | 資料到得**太快** |
| 與時脈頻率的關係 | **有關**（降頻可解） | **無關**（降頻也修不了）★ |
| 修復方法 | 降頻、縮短路徑、用更快元件 | 加 buffer 延長路徑 |
| 嚴重程度 | 可用降頻暫時解決 | **更嚴重**（無法用頻率解決） |

> **記憶口訣**：Setup 靠**減**（減延遲），Hold 靠**加**（加延遲）。Setup 能降頻暫救，Hold 不能。

### 4.7 關鍵路徑（Critical Path）

**定義**：電路中 Slack 最小（最容易違規）的路徑。

- 關鍵路徑決定了晶片的**最高工作頻率**
- $f_{max} = 1 / T_{clk,min}$，其中 $T_{clk,min} = t_{cq} + t_{logic,max} + t_{setup}$

---

### 數值例題 1：Setup Slack 計算

**題目**：一個同步電路，$T_{clk} = 2$ ns, $t_{cq} = 0.2$ ns, $t_{logic} = 1.3$ ns, $t_{setup} = 0.15$ ns, $t_{skew} = 0$。

(a) 計算 Setup Slack
(b) 這個時序是否 meet？
(c) 最大可容忍的 $t_{logic}$ 是多少？

**解答**：

**(a)**
$$\text{Setup Slack} = T_{clk} - (t_{cq} + t_{logic} + t_{setup})$$
$$= 2.0 - (0.2 + 1.3 + 0.15) = 2.0 - 1.65 = \boxed{0.35 \text{ ns}}$$

**(b)** Slack = 0.35 ns > 0 → **PASS**（時序滿足）

**(c)** 令 Slack = 0：
$$0 = T_{clk} - (t_{cq} + t_{logic,max} + t_{setup})$$
$$t_{logic,max} = T_{clk} - t_{cq} - t_{setup} = 2.0 - 0.2 - 0.15 = \boxed{1.65 \text{ ns}}$$

---

### 數值例題 2：Hold Slack 計算

**題目**：承例題 1，$t_{hold} = 0.1$ ns, $t_{cq} = 0.2$ ns。最短組合邏輯延遲 $t_{logic,min} = 0.05$ ns。

(a) 計算 Hold Slack
(b) 是否有 Hold 違規？如何修復？

**解答**：

**(a)**
$$\text{Hold Slack} = (t_{cq} + t_{logic,min}) - t_{hold}$$
$$= (0.2 + 0.05) - 0.1 = 0.25 - 0.1 = \boxed{0.15 \text{ ns}}$$

**(b)** Slack = 0.15 ns > 0 → **PASS**（無 Hold 違規）

如果 $t_{logic,min}$ 更小，例如 0 ns：
$$\text{Hold Slack} = 0.2 - 0.1 = 0.1 \text{ ns（仍 Pass）}$$

如果有 Hold 違規（例如 $t_{cq} = 0.05$, $t_{logic,min} = 0$, $t_{hold} = 0.1$）：
$$\text{Hold Slack} = 0.05 - 0.1 = -0.05 \text{ ns（FAIL!）}$$
修復：在路徑上插入 buffer（增加延遲）。

---

### 數值例題 3：時脈偏移的影響

**題目**：$T_{clk} = 1.5$ ns, $t_{cq} = 0.15$ ns, $t_{logic} = 1.0$ ns, $t_{setup} = 0.12$ ns, $t_{hold} = 0.08$ ns。

情況 A：$t_{skew} = +0.1$ ns（Capture CLK 比 Launch CLK 慢 0.1 ns）
情況 B：$t_{skew} = -0.1$ ns（Capture CLK 比 Launch CLK 快 0.1 ns）

分別計算 Setup Slack 和 Hold Slack。

**解答**：

**情況 A：$t_{skew} = +0.1$ ns**

$$\text{Setup Slack} = (T_{clk} + t_{skew}) - (t_{cq} + t_{logic} + t_{setup})$$
$$= (1.5 + 0.1) - (0.15 + 1.0 + 0.12) = 1.6 - 1.27 = \boxed{+0.33 \text{ ns (PASS)}}$$

$$\text{Hold Slack} = (t_{cq} + t_{logic}) - (t_{hold} + t_{skew})$$
$$= (0.15 + 1.0) - (0.08 + 0.1) = 1.15 - 0.18 = \boxed{+0.97 \text{ ns (PASS)}}$$

> 正 skew（Capture 較晚）→ Setup 受益（多了時間），Hold 有點吃虧（但通常還好）

**情況 B：$t_{skew} = -0.1$ ns**

$$\text{Setup Slack} = (1.5 - 0.1) - (0.15 + 1.0 + 0.12) = 1.4 - 1.27 = \boxed{+0.13 \text{ ns (PASS, 但很緊)}}$$

$$\text{Hold Slack} = (0.15 + 1.0) - (0.08 - 0.1) = 1.15 - (-0.02) = \boxed{+1.17 \text{ ns (PASS)}}$$

> 負 skew（Capture 較早）→ Setup 吃虧，Hold 受益

---

### 數值例題 4：最大工作頻率

**題目**：電路的關鍵路徑：$t_{cq} = 0.25$ ns, $t_{logic,critical} = 2.5$ ns, $t_{setup} = 0.18$ ns, $t_{skew} = 0.05$ ns（worst case）。求最大工作頻率。

**解答**：

最小時脈週期（令 Setup Slack = 0）：

$$T_{clk,min} = t_{cq} + t_{logic,critical} + t_{setup} + t_{skew,worst}$$
$$= 0.25 + 2.5 + 0.18 + 0.05 = 2.98 \text{ ns}$$

$$f_{max} = \frac{1}{T_{clk,min}} = \frac{1}{2.98 \times 10^{-9}} \approx \boxed{335 \text{ MHz}}$$

---

### 數值例題 5：多級路徑 STA

**題目**：下圖電路，計算每個節點的 AT 和關鍵路徑。$T_{clk} = 5$ ns, $t_{setup} = 0.2$ ns。

```
       FF_A ──[2ns]──▶ G1 ──[1ns]──▶ G3 ──[0.5ns]──▶ FF_D
                              ↑
       FF_B ──[1.5ns]─▶ G2 ──┘
                         ↑
       FF_C ──[0.8ns]────┘
```

（FF 的 $t_{cq}$ = 0.3 ns）

**解答**：

計算各節點的到達時間（AT），從 Launch FF 的 Q 端開始（AT = $t_{cq}$ = 0.3 ns）：

**G1 輸出**：
- 從 FF_A：$0.3 + 2.0 = 2.3$ ns

**G2 輸出**：
- 從 FF_B：$0.3 + 1.5 = 1.8$ ns
- 從 FF_C：$0.3 + 0.8 = 1.1$ ns
- **取最大值**：$\max(1.8, 1.1) = 1.8$ ns

**G3 輸入**：
- 從 G1：$2.3 + 1.0 = 3.3$ ns
- 從 G2：$1.8$  ns
- **取最大值**：$3.3$ ns

**FF_D 的 D 端**（AT）：
- $3.3 + 0.5 = 3.8$ ns

**Required Time**：
- $RT = T_{clk} - t_{setup} = 5.0 - 0.2 = 4.8$ ns

**Setup Slack**：
- $Slack = 4.8 - 3.8 = \boxed{1.0 \text{ ns (PASS)}}$

**關鍵路徑**：FF_A → G1 → G3 → FF_D（總延遲最大的路徑）

---

## 五、時序約束（SDC 格式）

### 5.1 什麼是 SDC？

SDC（Synopsys Design Constraints）是描述時序約束的標準格式，用 Tcl 語法寫成。

### 5.2 常見 SDC 指令

```tcl
# 定義時脈
create_clock -name CLK -period 2.0 [get_ports clk]

# 設定輸入延遲（外部電路到達此晶片的延遲）
set_input_delay -clock CLK 0.5 [get_ports data_in]

# 設定輸出延遲（此晶片到外部電路的要求）
set_output_delay -clock CLK 0.3 [get_ports data_out]

# 設定時脈不確定度（包含 jitter + skew margin）
set_clock_uncertainty 0.1 [get_clocks CLK]

# 設定假路徑（不需要做 STA 的路徑）
set_false_path -from [get_clocks CLK_A] -to [get_clocks CLK_B]

# 設定多週期路徑
set_multicycle_path -setup 2 -from [get_cells reg_a] -to [get_cells reg_b]

# 設定最大延遲
set_max_delay 3.0 -from [get_ports a] -to [get_ports b]

# 設定驅動強度
set_driving_cell -lib_cell BUF_X4 [get_ports data_in]

# 設定負載
set_load 0.05 [get_ports data_out]
```

### 5.3 SDC 中的重要概念

| 指令 | 影響 | 用途 |
|------|------|------|
| `create_clock` | 定義時脈頻率和波形 | 所有時序分析的基礎 |
| `set_input_delay` | 設定外部到達時間 | 約束晶片輸入端 |
| `set_output_delay` | 設定外部所需時間 | 約束晶片輸出端 |
| `set_false_path` | 排除某些路徑 | 跨時脈域、靜態信號 |
| `set_multicycle_path` | 允許多個週期 | 慢速資料路徑 |
| `set_clock_uncertainty` | 加入時脈不確定度 | 包含 jitter 和 margin |

---

## 關鍵術語表

| 術語 | 英文全名 | 說明 |
|------|---------|------|
| 邏輯合成 | Logic Synthesis | RTL → Gate-level Netlist |
| HLS | High-Level Synthesis | C/C++ → RTL |
| BDD | Binary Decision Diagram | 布林函數的圖形表示 |
| ROBDD | Reduced Ordered BDD | 簡化有序 BDD（唯一性） |
| SOP | Sum of Products | 積之和（最小項） |
| POS | Product of Sums | 和之積（最大項） |
| Espresso | — | 兩階邏輯最佳化演算法 |
| 技術映射 | Technology Mapping | 通用閘 → 標準元件庫 |
| 標準元件庫 | Standard Cell Library | 真實邏輯閘的集合 |
| STA | Static Timing Analysis | 靜態時序分析 |
| AT | Arrival Time | 到達時間 |
| RT | Required Time | 要求時間 |
| Slack | — | 鬆弛量 = RT - AT |
| Setup Time | — | 資料須在 CLK 前穩定的時間 |
| Hold Time | — | 資料須在 CLK 後保持的時間 |
| $t_{cq}$ | Clock-to-Q Delay | FF 的時脈到輸出延遲 |
| $t_{skew}$ | Clock Skew | 不同 FF 收到時脈的時間差 |
| Critical Path | — | Slack 最小的路徑 |
| SDC | Synopsys Design Constraints | 時序約束格式 |
| False Path | — | 不需分析的路徑 |
| Multicycle Path | — | 允許多週期的路徑 |
| PrimeTime | — | Synopsys 的 STA 工具 |

---

## 題型鑑別

| 看到什麼關鍵字 | 用什麼公式 | 答題方向 |
|---------------|-----------|---------|
| Setup Slack | $T_{clk} + t_{skew} - t_{cq} - t_{logic} - t_{setup}$ | 正值→PASS |
| Hold Slack | $t_{cq} + t_{logic} - t_{hold} - t_{skew}$ | 注意 skew 方向 |
| 最大頻率 | $f = 1/(t_{cq} + t_{logic} + t_{setup})$ | 取關鍵路徑 |
| 關鍵路徑 | 所有路徑的最大延遲 | 從 Launch FF → Capture FF |
| BDD、ROBDD | 圖形表示 | 變數順序影響大小 |
| 合成、映射 | 三步驟 | 轉譯→最佳化→技術映射 |
| SDC、約束 | Tcl 語法 | 記住常見指令 |

---

## ✅ 自我檢測

### 基礎題

<details>
<summary>Q1：邏輯合成的三大步驟是什麼？各步驟的輸入/輸出？</summary>

**答案**：
1. **轉譯（Translation）**：RTL → 通用布林邏輯網路（不依賴任何元件庫）
2. **最佳化（Optimization）**：簡化布林函數，根據面積/速度/功耗目標取捨
3. **技術映射（Technology Mapping）**：用標準元件庫中的真實邏輯閘取代通用邏輯

最終輸出：Gate-level Netlist（閘級網表）
</details>

<details>
<summary>Q2：Setup Time 和 Hold Time 的物理意義是什麼？哪個更嚴重？</summary>

**答案**：
- **Setup Time**：資料必須在時脈有效邊緣**之前**就穩定的最小時間。違反 → 資料太慢到達 → FF 可能抓到錯誤的值
- **Hold Time**：資料必須在時脈有效邊緣**之後**繼續保持穩定的最小時間。違反 → 新資料太快到達 → 覆蓋掉正在被抓取的資料

**Hold 違規更嚴重**：因為 Setup 違規可以靠降頻（增加 $T_{clk}$）暫時解決，但 Hold 違規與時脈頻率無關（公式中沒有 $T_{clk}$），只能靠修改電路（加 buffer）解決
</details>

<details>
<summary>Q3：ROBDD 的兩個重要性質是什麼？為什麼變數順序重要？</summary>

**答案**：
1. **唯一性（Canonical）**：給定變數順序，布林函數的 ROBDD 表示是唯一的 → 可快速判斷兩個函數是否等價
2. **簡化（Reduced）**：合併等價子圖、消除冗餘節點 → 圖最小

**變數順序重要**：不同順序可能導致 ROBDD 大小差異極大（從 O(n) 到 O(2^n)）。例如 $f = a_1b_1 + a_2b_2 + ... + a_nb_n$，若相關變數相鄰（$a_1, b_1, a_2, b_2, ...$）則 O(n)，若分開（$a_1, a_2, ..., b_1, b_2, ...$）則 O(2^n)
</details>

### 計算題

<details>
<summary>Q4：$T_{clk} = 3$ ns, $t_{cq} = 0.2$ ns, $t_{setup} = 0.15$ ns, $t_{hold} = 0.08$ ns, $t_{skew} = 0.05$ ns。關鍵路徑的 $t_{logic} = 2.3$ ns，最短路徑的 $t_{logic,min} = 0.1$ ns。求 Setup Slack 和 Hold Slack。</summary>

**答案**：

Setup Slack：
$$= (T_{clk} + t_{skew}) - (t_{cq} + t_{logic} + t_{setup})$$
$$= (3.0 + 0.05) - (0.2 + 2.3 + 0.15) = 3.05 - 2.65 = +0.40 \text{ ns (PASS)}$$

Hold Slack：
$$= (t_{cq} + t_{logic,min}) - (t_{hold} + t_{skew})$$
$$= (0.2 + 0.1) - (0.08 + 0.05) = 0.3 - 0.13 = +0.17 \text{ ns (PASS)}$$
</details>

<details>
<summary>Q5：某設計的關鍵路徑延遲（$t_{cq} + t_{logic}$）= 4.2 ns, $t_{setup}$ = 0.2 ns, $t_{skew}$ = 0.1 ns（worst case）。(a) 最大工作頻率？(b) 若要跑 300 MHz，有多少 timing margin？</summary>

**答案**：

**(a)** 最小時脈週期：
$$T_{clk,min} = 4.2 + 0.2 + 0.1 = 4.5 \text{ ns}$$
$$f_{max} = 1/4.5 \text{ ns} = 222 \text{ MHz}$$

**(b)** 300 MHz → $T_{clk} = 3.33$ ns

$$\text{Setup Slack} = 3.33 - 4.5 = -1.17 \text{ ns}$$

**Slack 為負！無法跑 300 MHz。** 需要把關鍵路徑縮短至少 1.17 ns。
</details>

<details>
<summary>Q6：為什麼在 SDC 中要設定 false path？給一個常見的例子。</summary>

**答案**：
**False Path** 是在功能上不可能被觸發，或不需要滿足時序要求的路徑。設定 false path 可以：
1. 讓工具不浪費資源優化不存在的路徑
2. 避免假的 timing violation

**常見例子**：
1. **跨時脈域（CDC）**：兩個不同時脈域之間的路徑，時序關係不確定，不能用 STA 分析（需要用同步器處理）
   ```tcl
   set_false_path -from [get_clocks CLK_100M] -to [get_clocks CLK_200M]
   ```
2. **靜態配置信號**：上電後就不再改變的暫存器（如控制暫存器），不需要動態時序約束
3. **測試模式路徑**：正常功能不會走到的 DFT 路徑
</details>

---

> **下一章**：[eda_06_實體設計_佈局與繞線.md](eda_06_實體設計_佈局與繞線.md) —— 把閘級網表「擺」到矽晶片上
