# VLSI 教學講義 第五章：時序電路 CMOS 實現

> **適用對象**：零基礎入門，電機/電子系大學部至研究所
> **重要度**：Setup/Hold Time 分析是 TSMC/MTK/聯發科面試的**最高頻考題**

---

## 🔰 本章基礎觀念（零基礎必讀）

### 組合邏輯 vs 時序邏輯

| 類型 | 特性 | 例子 |
|------|------|------|
| 組合邏輯 | 輸出只取決於**當前輸入** | 加法器、多工器 |
| 時序邏輯 | 輸出取決於**當前輸入 + 過去狀態** | 暫存器、計數器 |

時序邏輯需要**記憶元件**來儲存狀態，最基本的就是**鎖存器（Latch）**和**正反器（Flip-Flop）**。

> **一句話記住**：
> - Latch = 電平觸發（Level-Sensitive）：時脈為高（或低）時透明
> - Flip-Flop = 邊緣觸發（Edge-Triggered）：只在時脈邊緣取樣

---

## 一、靜態鎖存器與正反器的 CMOS 實現

### 1.1 傳輸閘鎖存器（Transmission Gate Latch）

這是最基本也最常用的 CMOS 鎖存器。

```
         TG1                    TG2
D ──┤╦╗├──┬──[>o]──┬──┤╦╗├──┬──→ Q
    CLK    │   INV1 │  CLK_bar│
    CLK_bar│        │  CLK    │
           │        │         │
           └──[>o]──┘         │
              INV2             │
           (回饋反相器)         │
                               │
                          [>o] INV3（可選，輸出緩衝）
```

**更詳細的結構**：

```
      CLK
       │
  ┌────┴────┐     ┌──────┐
  │  NMOS   │     │      │
D─┤         ├──┬──┤ INV1 ├──┬──→ Q
  │  PMOS   │  │  │      │  │
  └────┬────┘  │  └──────┘  │
       │       │             │
    CLK_bar    │  ┌──────┐   │
               │  │      │   │
               └──┤ INV2 ├───┘
                  │      │
                  └──────┘
                 (回饋，維持資料)
```

#### 工作原理

| CLK | TG1 | TG2 | 狀態 |
|-----|-----|-----|------|
| 1（High） | ON | OFF | **透明**：D 通過 TG1 → INV1 → Q |
| 0（Low） | OFF | ON | **保持**：回饋迴路（INV1 → INV2 → INV1）維持 Q |

**正位準鎖存器**（CLK = 1 時透明）的時序行為：

```
CLK  ────┐     ┌─────┐     ┌────
         │     │     │     │
         └─────┘     └─────┘

D    ──┬──┬──────────┬──────────
       │1 │   0      │  1
       └──┘          │

Q    ──┬──┬──────────┬──────────
       │1 │   0      │  1
       └──┘(CLK高時   │(CLK高時
           跟隨D)      跟隨D)
              ↑                ↑
         CLK=0時，Q保持    CLK=0時，Q保持
```

### 1.2 主從式 D 正反器（Master-Slave D Flip-Flop）

**核心概念**：兩個鎖存器串接，用互補時脈控制。

```
                Master Latch          Slave Latch
               (CLK_bar 透明)         (CLK 透明)
           ┌──────────────────┐  ┌──────────────────┐
           │   TG    INV      │  │   TG    INV      │
D ─────────┤──╦╗──┬──[>o]──┬─┤──┤──╦╗──┬──[>o]──┬─┤──→ Q
           │CLK_bar│  │     │ │  │ CLK │  │     │ │
           │ CLK   │  │     │ │  │CLK_bar│ │     │ │
           │       └[>o]────┘ │  │      └[>o]────┘ │
           │      (回饋)       │  │     (回饋)       │
           └──────────────────┘  └──────────────────┘
```

#### 工作原理

| CLK | Master | Slave | 行為 |
|-----|--------|-------|------|
| 0（Low） | **透明**（取樣 D） | **保持** | D 值進入 Master |
| 0→1（上升沿） | 關閉 | 打開 | Master 的值傳到 Slave → Q 更新 |
| 1（High） | **保持** | **透明** | Q = Master 鎖住的值 |
| 1→0（下降沿） | 打開 | 關閉 | Slave 鎖住 Q |

> **關鍵**：Q 只在**時脈上升沿**更新一次，這就是「邊緣觸發」。

### 1.3 C²MOS 鎖存器（Clocked CMOS）

```
        VDD
         │
    ┌────┤
    │  ┌─┴─┐
  D─┤  │ P1│
    │  └─┬─┘
    │  ┌─┴─┐
CLK_bar┤ P2│    ← 時脈控制的 PMOS
    │  └─┬─┘
    │    │
    │    ├──── Q
    │    │
    │  ┌─┴─┐
 CLK──┤ N2│    ← 時脈控制的 NMOS
    │  └─┬─┘
    │  ┌─┴─┐
  D─┤  │ N1│
    │  └─┬─┘
    └────┤
         │
        GND
```

**優點**：
- 不需要傳輸閘
- 無通路從 VDD 到 GND（低功耗）
- 佈局緊湊

**缺點**：
- 需要互補時脈
- 時脈負載較大（控制兩個電晶體）

---

## 二、動態正反器

### 2.1 TSPC（True Single Phase Clock）正反器

**最大優點**：只需要**單一相位時脈**（不需 CLK_bar）。

#### TSPC 正沿觸發 D 正反器

```
Stage 1 (P-type)    Stage 2 (N-type)    Stage 3 (P-type)
    VDD                  VDD                 VDD
     │                    │                   │
   ┌─┴─┐              ┌─┴─┐               ┌─┴─┐
 D─┤ P1│           ┌──┤ P3│            ┌──┤ P5│
   └─┬─┘           │  └─┬─┘            │  └─┬─┘
   ┌─┴─┐           │  ┌─┴─┐            │  ┌─┴─┐
CLK┤ P2│           │  │ N3├──CLK       │  │ N5├─CLK_internal
   └─┬─┘           │  └─┬─┘            │  └─┬─┘
     │──→ node1 ───│    │──→ node2 ────│    │──→ Q
   ┌─┴─┐           │  ┌─┴─┐            │  ┌─┴─┐
 D─┤ N1│           └──┤ N4│            └──┤ N6│
   └─┬─┘              └─┬─┘               └─┬─┘
   ┌─┴─┐                │                    │
CLK┤ N2│              GND                  GND
   └─┬─┘
     │
    GND
```

**TSPC 的優缺點**：

| 優點 | 缺點 |
|------|------|
| 單一時脈（無需 CLK_bar） | 對時脈佔空比敏感 |
| 電晶體數適中 | 動態節點有漏電問題 |
| 時脈負載小 | 需注意時脈速度下限 |
| 適合高速設計 | |

---

## 三、時序參數分析（面試核心重點）

### 3.1 三個關鍵時序參數

```
        ┌─────────────┐
  D ───→│             │───→ Q
        │  Flip-Flop  │
  CLK──→│             │
        └─────────────┘
```

#### (a) Setup Time (tsu) — 建立時間

**定義**：資料 D 必須在時脈邊緣**之前**穩定的最短時間。

```
              tsu
         ←────────→
D    ────┬─────────┬─────
         │ D 必須  │
         │ 穩定    │
         └─────────┘
                    ↑
CLK  ───────────────┤──────
                    │↑ 上升沿
                    └──────
```

> 如果 D 在 tsu 之內改變 → **Setup Violation** → 正反器可能進入亞穩態（Metastability）

#### (b) Hold Time (th) — 保持時間

**定義**：資料 D 必須在時脈邊緣**之後**繼續穩定的最短時間。

```
                    th
                ←────────→
D    ────────────┬─────────┬────
                 │ D 必須  │
                 │ 穩定    │
                 └─────────┘
                 ↑
CLK  ────────────┤──────────
                 │↑ 上升沿
                 └──────────
```

> 如果 D 在 th 之內改變 → **Hold Violation** → 同樣可能進入亞穩態

#### (c) Clock-to-Q (tcq) — 時脈到輸出延遲

**定義**：時脈邊緣到輸出 Q 穩定的時間。

```
CLK  ────────────┤──────────
                 │↑
                 └──────────
                     tcq
                 ←────────→
Q    ────────────────┬──────
                     │ Q 穩定
                     └──────
```

### 3.2 最大操作頻率分析

考慮兩個串接的正反器和之間的組合邏輯：

```
       FF1                    Combinational               FF2
  ┌──────────┐                  Logic                ┌──────────┐
  │          │───→ tlogic ───→                  ───→│          │
D─│   tcq    │                                       │          │→ Q
  │          │                                       │   tsu    │
  └────┬─────┘                                       └────┬─────┘
       │                                                   │
  CLK──┴───────────────────────────────────────────────────┘
              ← Tclk (一個完整時脈週期) →
```

**時序約束**：

```
┌──────────────────────────────────────────────────────────┐
│  Tclk_min = tcq + tlogic_max + tsu + tskew              │
│                                                          │
│  最大操作頻率：fmax = 1 / Tclk_min                        │
└──────────────────────────────────────────────────────────┘
```

**分解**：
- tcq：FF1 的時脈到輸出延遲
- tlogic_max：組合邏輯的**最大延遲**（最長路徑）
- tsu：FF2 的建立時間
- tskew：時脈偏移（FF2 的時脈比 FF1 早到的情況更嚴格）

### 3.3 Hold Time 約束

Hold violation 比 Setup violation **更危險**，因為它**不能靠降低頻率修復**。

```
┌──────────────────────────────────────────────────────────┐
│  tcq + tlogic_min ≥ th + tskew                           │
│                                                          │
│  即：資料的最快到達時間 ≥ Hold time + 時脈偏移              │
└──────────────────────────────────────────────────────────┘
```

如果違反：
- 新資料太快到達 FF2 → FF2 抓到錯誤的資料
- **無法靠調頻修復**，必須在路徑上**插入延遲**（buffer insertion）

### 3.4 完整時序圖

```
CLK1 ──┤      ┌──── (FF1 的時脈)
        │      │
CLK2 ──┤ tskew├──── (FF2 的時脈，可能有偏移)
        │←────→│

        tcq    tlogic    tsu
  FF1 ──┤←──→├──┤←────→├──┤←──→├── FF2
        │      │  │        │  │      │
        └──────┘  └────────┘  └──────┘

約束：tcq + tlogic + tsu ≤ Tclk - tskew  (Setup)
     tcq + tlogic_min ≥ th + tskew       (Hold)
```

---

## 四、時脈偏移（Clock Skew）

### 4.1 定義

**時脈偏移（Clock Skew）**：同一個時脈信號到達不同正反器的**時間差**。

```
tskew = tCLK_arrival(FF2) - tCLK_arrival(FF1)
```

### 4.2 正偏移 vs 負偏移

| 類型 | 條件 | 對 Setup 的影響 | 對 Hold 的影響 |
|------|------|----------------|---------------|
| 正偏移（Positive Skew） | FF2 時脈較晚到 | **有利**（多了時間） | **不利**（Hold 更嚴格） |
| 負偏移（Negative Skew） | FF2 時脈較早到 | **不利**（少了時間） | **有利**（Hold 更寬鬆） |

### 4.3 零偏移設計目標

理想情況下 tskew = 0，但實際上不可能。設計目標是**最小化偏移**。

---

## 五、時脈抖動（Clock Jitter）

### 5.1 定義

**時脈抖動（Clock Jitter）**：時脈邊緣的**隨機變化**，每個週期的實際時長略有不同。

```
理想時脈：  ┌──┐  ┌──┐  ┌──┐  ┌──┐
            │  │  │  │  │  │  │  │
          ──┘  └──┘  └──┘  └──┘  └──

實際時脈：  ┌──┐   ┌──┐ ┌──┐   ┌──┐
            │  │   │  │ │  │   │  │
          ──┘  └───┘  └─┘  └───┘  └──
                ↑        ↑
              偏晚      偏早（抖動）
```

### 5.2 對時序的影響

抖動會使有效時脈週期**縮短**，Setup 約束變為：

```
Tclk_min = tcq + tlogic_max + tsu + tskew + tjitter
```

### 5.3 來源

| 來源 | 說明 |
|------|------|
| PLL/DLL 內部雜訊 | 鎖相迴路的相位雜訊 |
| 電源雜訊 | VDD 波動影響時脈緩衝器延遲 |
| 溫度變化 | 影響電晶體特性 |
| 串擾 | 耦合雜訊 |

---

## 六、時脈分佈（Clock Distribution）

### 6.1 目標

將時脈信號從一個源頭（通常是 PLL 輸出）**均勻分佈到晶片上數百萬個正反器**，且偏移最小。

### 6.2 H-tree（H 型樹）

```
                    ┌─────┐
                    │ PLL │
                    └──┬──┘
                       │
              ┌────────┼────────┐
              │        │        │
         ┌────┼────┐   │   ┌───┼────┐
         │    │    │       │   │    │
        FF   FF   FF      FF  FF   FF
```

**特點**：
- 每條路徑長度**完全相同** → 理論上零偏移
- 結構對稱
- **缺點**：佈線面積大、不易配合不規則的晶片佈局

### 6.3 Clock Mesh（時脈網格）

```
    ══════╦══════╦══════╦══════
          ║      ║      ║
    ══════╬══════╬══════╬══════
          ║      ║      ║
    ══════╬══════╬══════╬══════
          ║      ║      ║
    ══════╩══════╩══════╩══════
```

**特點**：
- 在晶片上鋪設金屬網格
- 多條路徑到達同一點 → **冗餘降低偏移**
- **缺點**：短路電流大、功耗高

### 6.4 Clock Spine（時脈脊柱）

```
          PLL
           │
    ═══════╪═══════  ← 主幹（Spine）
    │      │      │
    ├──FF  ├──FF  ├──FF   ← 分支
    │      │      │
    ├──FF  ├──FF  ├──FF
```

**特點**：
- 一條粗金屬主幹 + 分支
- 介於 H-tree 和 Mesh 之間
- 適合長條型佈局

### 6.5 比較

| 方法 | 偏移 | 功耗 | 佈線面積 | 適用場景 |
|------|------|------|---------|---------|
| H-tree | 極低 | 中 | 大 | 高速處理器 |
| Clock Mesh | 低 | **高** | 大 | 高性能 SoC |
| Clock Spine | 中 | 低 | 小 | 一般 SoC |
| Buffered Tree | 中 | 中 | 中 | 最常見 |

---

## 七、時脈閘控（Clock Gating）

### 7.1 動機

時脈網路消耗晶片 **30%~50%** 的動態功率（因為 α = 1）。

如果某個模組暫時不工作，可以**關閉它的時脈**來省電。

### 7.2 基本結構

#### (a) 簡單 AND 閘控

```
CLK ──┐
      │ AND ──→ GCLK（閘控時脈）
EN ───┘
```

**問題**：如果 EN 在 CLK = 1 時改變 → 產生 glitch（毛刺）！

#### (b) Latch-based 閘控（正確做法）

```
          ┌──────┐
EN ───────┤Latch ├──┐
          │(CLK低 │  │ AND ──→ GCLK
CLK ──┬───┤時透明)│  │
      │   └──────┘  │
      │              │
      └──────────────┘
```

**工作原理**：
1. CLK = 0 時，Latch 透明 → EN 通過 Latch
2. CLK = 1 時，Latch 鎖住 → EN 的變化不影響 GCLK
3. **確保 GCLK 沒有 glitch**

### 7.3 省電效果

```
原始功率：Pclk = Cclk × VDD² × f
閘控後：  Pclk' = α_gate × Cclk × VDD² × f

省電比例 = 1 - α_gate
```

如果一個模組 50% 的時間不工作 → 節省該模組 50% 的時脈功率。

---

## 八、關鍵術語表

| 英文 | 中文 | 說明 |
|------|------|------|
| Latch | 鎖存器 | 電平觸發的記憶元件 |
| Flip-Flop (FF) | 正反器 | 邊緣觸發的記憶元件 |
| Master-Slave | 主從式 | 兩個鎖存器串接 |
| Setup Time (tsu) | 建立時間 | D 在 CLK 沿前需穩定的時間 |
| Hold Time (th) | 保持時間 | D 在 CLK 沿後需穩定的時間 |
| Clock-to-Q (tcq) | 時脈到輸出延遲 | CLK 沿到 Q 穩定的時間 |
| Clock Skew (tskew) | 時脈偏移 | 時脈到達不同 FF 的時間差 |
| Clock Jitter (tjitter) | 時脈抖動 | 時脈邊緣的隨機偏移 |
| Metastability | 亞穩態 | FF 在非穩定狀態振盪 |
| Transmission Gate (TG) | 傳輸閘 | NMOS+PMOS 並聯開關 |
| C²MOS | 時脈 CMOS | 用時脈控制的 CMOS 閘 |
| TSPC | 真單相時脈 | 只需一個時脈相位 |
| H-tree | H 型樹 | 對稱時脈分佈結構 |
| Clock Mesh | 時脈網格 | 網格式時脈分佈 |
| Clock Gating | 時脈閘控 | 關閉不用模組的時脈 |
| Setup Violation | 建立時間違規 | D 太晚穩定 |
| Hold Violation | 保持時間違規 | D 太早改變 |
| Critical Path | 關鍵路徑 | 決定 fmax 的最長路徑 |

---

## 九、數值例題

### 例題 1：最大操作頻率計算

**題目**：一個同步數位系統，tcq = 50 ps，tsu = 40 ps，最長組合邏輯延遲 tlogic = 300 ps，時脈偏移 tskew = 20 ps。
(a) 求最小時脈週期 Tclk_min
(b) 求最大操作頻率 fmax

**解答**：

```
(a) Tclk_min = tcq + tlogic + tsu + tskew
             = 50 + 300 + 40 + 20
             = 410 ps

(b) fmax = 1 / Tclk_min
         = 1 / (410 × 10⁻¹²)
         = 2.44 × 10⁹ Hz
         = 2.44 GHz
```

**答：Tclk_min = 410 ps，fmax ≈ 2.44 GHz**

---

### 例題 2：Hold Time 檢查

**題目**：續例題 1，th = 30 ps，最短組合邏輯延遲 tlogic_min = 15 ps。
檢查是否有 Hold Violation。

**解答**：

```
Hold 約束：tcq + tlogic_min ≥ th + tskew

左邊 = 50 + 15 = 65 ps
右邊 = 30 + 20 = 50 ps

65 ps ≥ 50 ps ✓ → 無 Hold Violation
```

**答：65 ps > 50 ps，Hold 約束滿足。安全邊限 = 65 - 50 = 15 ps**

---

### 例題 3：Hold Violation 修復

**題目**：另一條路徑，tcq = 40 ps，tlogic_min = 5 ps，th = 35 ps，tskew = 25 ps。
(a) 是否有 Hold Violation？
(b) 如果有，需要插入多少延遲？

**解答**：

(a)
```
tcq + tlogic_min = 40 + 5 = 45 ps
th + tskew = 35 + 25 = 60 ps

45 ps < 60 ps → Hold Violation！
```

(b)
```
需要額外延遲 = (th + tskew) - (tcq + tlogic_min)
              = 60 - 45
              = 15 ps
```

需要在路徑上插入至少 15 ps 的延遲（通常用 buffer 或 delay cell）。

**答：(a) 有 Hold Violation (b) 需插入至少 15 ps 延遲**

> **重要**：Hold Violation 不能靠降頻修復！必須改電路。
> Setup Violation 可以靠降頻修復（增加 Tclk）。

---

### 例題 4：時脈偏移的影響

**題目**：tcq = 60 ps，tlogic = 200 ps，tsu = 50 ps。
(a) 若 tskew = 0，fmax = ?
(b) 若 tskew = 30 ps（FF2 時脈較早到，負偏移），fmax = ?
(c) 若 tskew = -30 ps（FF2 時脈較晚到，正偏移），fmax = ?

**解答**：

注意：我們定義 tskew > 0 表示 FF2 時脈較晚到（正偏移，對 Setup 有利）。

但在很多教科書中，Setup 約束寫為：
```
Tclk ≥ tcq + tlogic + tsu - tskew（正偏移時 tskew 為正，效果是放寬）
```

或更保守地考慮最差情況：
```
Tclk ≥ tcq + tlogic + tsu + |tskew|（取絕對值，最保守）
```

讓我們用標準定義：**tskew = t_CLK2 - t_CLK1**

Setup 約束：Tclk + tskew ≥ tcq + tlogic + tsu
即：Tclk ≥ tcq + tlogic + tsu - tskew

(a) tskew = 0：
```
Tclk_min = 60 + 200 + 50 - 0 = 310 ps
fmax = 1/310ps = 3.23 GHz
```

(b) tskew = -30 ps（FF2 早到 30 ps）：
```
Tclk_min = 60 + 200 + 50 - (-30) = 340 ps
fmax = 1/340ps = 2.94 GHz（變慢了！）
```

(c) tskew = +30 ps（FF2 晚到 30 ps）：
```
Tclk_min = 60 + 200 + 50 - 30 = 280 ps
fmax = 1/280ps = 3.57 GHz（變快了！）
```

> 但注意：(c) 的正偏移雖然幫了 Setup，卻讓 Hold 約束更嚴格。
> Hold 約束：tcq + tlogic_min ≥ th + tskew
> 如果 tskew = 30 ps，Hold 右邊增加 30 ps，更容易違規。

**答：(a) 3.23 GHz (b) 2.94 GHz (c) 3.57 GHz**

---

### 例題 5：時脈閘控省電

**題目**：一個 SoC 的時脈網路功率 Pclk = 500 mW，佔總動態功率的 40%。
其中有一個 DSP 模組佔時脈功率的 25%，在語音通話模式下 80% 的時間不使用。
(a) 不使用時脈閘控，DSP 時脈功率 = ?
(b) 使用時脈閘控後，DSP 時脈功率 = ?
(c) 總功率節省多少？

**解答**：

(a)
```
P_DSP_clk = 25% × 500 mW = 125 mW
```

(b) 使用閘控後，80% 的時間時脈被關閉：
```
P_DSP_clk_gated = 125 × (1 - 0.8) = 125 × 0.2 = 25 mW
```

(c)
```
節省的功率 = 125 - 25 = 100 mW
總動態功率 = 500/0.4 = 1250 mW
節省比例 = 100/1250 = 8%
```

**答：(a) 125 mW (b) 25 mW (c) 總功率節省 8%（100 mW）**

---

### 例題 6：含抖動的時序分析

**題目**：tcq = 45 ps，tlogic = 250 ps，tsu = 35 ps，tskew = 15 ps，tjitter = 10 ps。
求 fmax。

**解答**：

```
Tclk_min = tcq + tlogic + tsu + tskew + tjitter
         = 45 + 250 + 35 + 15 + 10
         = 355 ps

fmax = 1 / 355 ps = 2.82 GHz
```

如果不考慮抖動和偏移：
```
Tclk_min = 45 + 250 + 35 = 330 ps → fmax = 3.03 GHz
```

抖動和偏移使 fmax 降低了 7%。

**答：fmax = 2.82 GHz（抖動和偏移造成 7% 的頻率損失）**

---

## 十、題型鑑別表

| 題目特徵 | 題型 | 關鍵公式 |
|---------|------|---------|
| 給 tcq, tlogic, tsu | 求 fmax | Tclk = tcq + tlogic + tsu + tskew |
| 給 tlogic_min, th | Hold 檢查 | tcq + tlogic_min ≥ th + tskew |
| 問插入延遲量 | Hold 修復 | Δt = (th+tskew) - (tcq+tlogic_min) |
| 比較偏移影響 | Skew 分析 | 正偏移幫 Setup 害 Hold |
| 時脈功率 | 閘控省電 | P_saved = α_inactive × P_clk_module |
| 畫 Latch/FF | 電路辨識 | TG Latch, Master-Slave DFF |

---

## ✅ 自我檢測

### Q1：Latch 和 Flip-Flop 有什麼區別？

<details>
<summary>點擊展開答案</summary>

| 特性 | Latch（鎖存器） | Flip-Flop（正反器） |
|------|-----------------|-------------------|
| 觸發方式 | **電平觸發**（Level-Sensitive） | **邊緣觸發**（Edge-Triggered） |
| 透明期間 | CLK = 1（或 0）的整個期間 | 只在 CLK 邊緣的瞬間 |
| 結構 | 一個 TG + 回饋 | 兩個 Latch 串接（Master-Slave） |
| 時序分析 | 較複雜（time borrowing） | 較簡單（離散取樣） |
| 應用 | 高速設計、時序最佳化 | **絕大多數同步設計** |

Flip-Flop 是由兩個互補的 Latch（Master + Slave）組成的。
</details>

### Q2：為什麼 Hold Violation 比 Setup Violation 更危險？

<details>
<summary>點擊展開答案</summary>

**Setup Violation**：
- 原因：tlogic 太大（路徑太長），或頻率太高
- 修復方法：**降低頻率**（增加 Tclk）即可
- 也可以做邏輯最佳化、管線化（Pipelining）

**Hold Violation**：
- 原因：tlogic_min 太小（路徑太短），或 tskew 太大
- **不能靠降頻修復**！因為 Hold 約束與 Tclk 無關
- 必須**修改電路**：插入延遲（buffer）、調整佈局
- 如果在 tapeout 後才發現 → 可能需要重新流片（Respin），代價極大

所以在設計流程中，Hold 修復的優先級通常**高於** Setup 修復。
</details>

### Q3：為什麼時脈閘控要用 Latch-based 而非簡單 AND 閘？

<details>
<summary>點擊展開答案</summary>

**簡單 AND 閘的問題**：
```
GCLK = CLK AND EN
```
如果 EN 在 CLK = 1 時從 1→0 或 0→1，GCLK 會產生**毛刺（Glitch）**：

```
CLK   ──┐  ┌────
        │  │
        └──┘
EN    ────┐
          │  ← EN 在 CLK=1 時改變
          └────
GCLK  ──┐┃┌────  ← 毛刺！
        │┃│
        └┃┘
```

這個毛刺可能被下游的 FF 誤觸發。

**Latch-based 解決方案**：
1. EN 先通過一個負位準 Latch（CLK=0 時透明）
2. EN 的改變只在 CLK=0 時傳遞 → CLK=1 時 EN 被鎖住
3. 所以 GCLK = CLK AND Latch_Q 不會有毛刺
</details>

### Q4：一個系統 tcq=30ps, tlogic=180ps, tsu=25ps, th=20ps, tskew=15ps。
(a) fmax=? (b) 最短路徑至少要多長才不會 Hold Violation？

<details>
<summary>點擊展開答案</summary>

(a) Setup 分析：
```
Tclk_min = tcq + tlogic + tsu + tskew
         = 30 + 180 + 25 + 15
         = 250 ps

fmax = 1/250ps = 4.0 GHz
```

(b) Hold 分析：
```
tcq + tlogic_min ≥ th + tskew
30 + tlogic_min ≥ 20 + 15
tlogic_min ≥ 5 ps
```

最短路徑的組合邏輯延遲至少要 **5 ps**。

如果有路徑的 tlogic < 5 ps（例如直連），需要插入至少 5 - tlogic 的延遲。
</details>

### Q5：請比較 H-tree、Clock Mesh、Clock Spine 三種時脈分佈方法。

<details>
<summary>點擊展開答案</summary>

| 特性 | H-tree | Clock Mesh | Clock Spine |
|------|--------|------------|-------------|
| **偏移** | 極低（路徑等長） | 低（冗餘路徑） | 中等 |
| **功耗** | 中等 | **高**（短路電流） | 低 |
| **面積** | 大（對稱結構） | 大（金屬網格） | 小 |
| **設計難度** | 中（需對稱佈局） | 高 | 低 |
| **適用場景** | 高速處理器 | 高性能 SoC | 一般 SoC |
| **PVT 敏感度** | 中 | **低**（冗餘） | 高 |
| **典型使用者** | Intel, AMD | Apple, Qualcomm | 各家 |

現代高性能晶片通常混合使用多種方法：上層用 Mesh 或 Spine，下層用 Buffered Tree。
</details>

---

> **下一章預告**：第六章將學習**互連與信號完整性**——金屬連線的電阻、電容建模，
> 以及串擾、IR Drop、電遷移等實際問題。
