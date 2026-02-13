# EDA 07：先進製程技術

> **目標讀者**：零基礎學生、準備 TSMC / Intel / Samsung 面試者
> **預備知識**：基礎 MOSFET 概念（閘極、源極、汲極）
> **學習時間**：約 120 分鐘
> **面試重要度**：★★★★★（本章幾乎每題都是 TSMC 面試熱門考點）

---

## 🔰 本章基礎觀念（零基礎必讀）

### 電晶體為什麼要一直縮小？

| 縮小帶來的好處 | 說明 |
|--------------|------|
| 更快 | 通道短 → 載子跑得快 → 切換快 |
| 更省電 | 面積小 → 電容小 → 充放電少 → 功耗低 |
| 更多功能 | 同樣面積塞更多電晶體 → 功能更強 |
| 更便宜 | 同一片晶圓產出更多晶片 |

### 縮小遇到什麼問題？

當 Planar MOSFET（平面電晶體）的閘極長度縮到約 20nm 以下時，閘極對通道的控制力不足，產生**短通道效應**：
- 漏電流暴增
- 閘極失去「開關」能力
- DIBL（Drain Induced Barrier Lowering）
- 亞閾值擺幅（Subthreshold Swing）劣化

### 解法：讓閘極從更多方向包住通道

```
    Planar → FinFET → GAA/Nanosheet → CFET

    閘極包覆通道的面數：1面 → 3面 → 4面 → 4面（堆疊）
    閘極控制力：             弱 → 強 → 更強 → 最強
```

---

## 一、FinFET ★TSMC 面試必問

### 1.1 結構

FinFET（Fin Field-Effect Transistor，鰭式場效電晶體）的核心改變：把通道從平面變成**立體的鰭片（Fin）**，閘極從三面包覆。

```
    Planar MOSFET（平面）          FinFET（立體）
    =====================          =============

        閘極                        閘極
    ┌──────────┐                ┌──┤    ├──┐
    │Gate      │                │  │Gate│  │  ← 閘極包三面
    ├──────────┤                │  ├────┤  │
    │Channel   │  ← 只有上方    │  │ Fin│  │  ← 鰭片就是通道
    ├──────────┤     一面控制    │  │(Ch)│  │
    │Substrate │                │  │    │  │
    └──────────┘                └──┴────┴──┘
                                   │    │
                                  Substrate

    閘極接觸通道：1面              閘極接觸通道：3面
```

**3D 示意圖**（正面觀察）：

```
                    Gate（閘極）
               ┌─────────────────┐
               │    ┌───────┐    │
               │    │       │    │
               │    │  Fin  │    │  ← Wfin（鰭片寬度）
               │    │(通道) │    │
               │    │       │    │  ← Hfin（鰭片高度）
               │    └───┬───┘    │
               └────────┼────────┘
               ═════════╧═════════
                    BOX / STI

    有效通道寬度 Weff = 2 × Hfin + Wfin
```

### 1.2 有效通道寬度 ★

$$\boxed{W_{eff} = 2 \times H_{fin} + W_{fin}}$$

- $H_{fin}$：鰭片高度（典型 40～50 nm）
- $W_{fin}$：鰭片寬度/厚度（典型 5～7 nm）

多個鰭片並聯時：

$$\boxed{W_{eff,total} = N_{fin} \times (2 \times H_{fin} + W_{fin})}$$

### 1.3 量化效應 ★★面試重點

**FinFET 只能用整數個 fin！** 你不能用 1.5 個 fin。

```
    1 fin          2 fins         3 fins
    ┌──┐          ┌──┐ ┌──┐      ┌──┐ ┌──┐ ┌──┐
    │  │          │  │ │  │      │  │ │  │ │  │
    │  │          │  │ │  │      │  │ │  │ │  │
    └──┘          └──┘ └──┘      └──┘ └──┘ └──┘

    Weff = 1×(2H+W)   2×(2H+W)    3×(2H+W)
```

這意味著：
- 驅動力只能是**離散值**（不像 Planar 可以任意調 W）
- 設計上需要仔細選擇 fin 數量
- 數位邏輯中，通常 NMOS 用 1～3 fins，PMOS 用 1～4 fins

### 1.4 FinFET vs Planar MOSFET 比較

| 特性 | Planar | FinFET |
|------|--------|--------|
| 閘極包覆 | 1 面 | **3 面** |
| 短通道效應 | 嚴重（≤ 22nm） | 大幅改善 |
| 漏電流 | 高 | **低** |
| 亞閾值擺幅 | ~90 mV/dec | **~65 mV/dec**（更接近理想 60） |
| 通道寬度 | 連續可調 | **離散量化** |
| 製程複雜度 | 低 | 高（3D 結構） |
| 製程節點 | > 22nm | **22nm ～ 3nm** |
| 代表 | 傳統 CMOS | TSMC N16/N7/N5/N3 |

### 1.5 TSMC FinFET 製程演進

| 製程 | 年份 | Fin Pitch | Metal Pitch | 邏輯密度 |
|------|------|-----------|-------------|---------|
| N16 | 2015 | ~48 nm | ~64 nm | ~30 MTr/mm² |
| N7 | 2018 | ~30 nm | ~40 nm | ~91 MTr/mm² |
| N5 | 2020 | ~25 nm | ~28 nm | ~173 MTr/mm² |
| N3 | 2022 | ~23 nm | ~23 nm | ~292 MTr/mm² |

（MTr/mm² = 百萬電晶體/平方毫米）

---

## 二、GAA / Nanosheet ★3nm 以下主流

### 2.1 為什麼需要 GAA？

FinFET 在 3nm 以下也遇到極限：
- Fin 越做越窄 → 量子效應、變異增加
- 3 面包覆不夠 → 需要 **4 面完全包覆**

### 2.2 GAA（Gate-All-Around）結構

```
    FinFET（3面包覆）             GAA Nanosheet（4面包覆）
    ┌──────────────┐             ┌──────────────┐
    │ G ┌────┐ G  │             │ G ┌────────┐G│
    │   │ Fin│    │             │   │Nanosheet│ │  ← 閘極完全包圍
    │   │    │    │             │ G └────────┘G│
    │   │    │    │             │ G ┌────────┐G│  ← 可以堆疊多層
    │   └────┘    │             │   │Nanosheet│ │
    │      ↑      │             │ G └────────┘G│
    │    底部沒有   │             │ G ┌────────┐G│
    │    閘極控制   │             │   │Nanosheet│ │
    └──────────────┘             │ G └────────┘G│
                                 └──────────────┘
    3面控制                       4面完全控制 ★
```

### 2.3 GAA 的優勢

| 特性 | 說明 |
|------|------|
| 閘極控制 | **4 面完全包覆** → 最佳閘極控制力 |
| 短通道效應 | 進一步抑制（比 FinFET 好） |
| 驅動力調整 | 調整 nanosheet 的**寬度**（而非 fin 數量）→ 更靈活 |
| 堆疊增加驅動力 | 堆疊 3～4 層 nanosheet → 增大有效寬度 |
| 面積效率 | 比 FinFET 更好的 PPA（Performance, Power, Area） |

### 2.4 有效通道寬度（GAA）

$$\boxed{W_{eff} = N_{sheets} \times 2 \times (W_{sheet} + T_{sheet})}$$

- $N_{sheets}$：堆疊的 nanosheet 層數（典型 3～4 層）
- $W_{sheet}$：每片 nanosheet 的寬度（可調，如 15～50 nm）
- $T_{sheet}$：每片 nanosheet 的厚度（典型 5～7 nm）

### 2.5 各廠 GAA 製程

| 公司 | 製程名稱 | 預計量產 | 說明 |
|------|---------|---------|------|
| Samsung | 3nm GAA | 2022 | 業界首個量產 GAA |
| TSMC | N2 (2nm) | 2025 | TSMC 首個 GAA（稱為 Nanosheet） |
| Intel | Intel 20A | 2024 | 稱為 RibbonFET |

---

## 三、CFET（Complementary FET）

### 3.1 概念

CFET 把 NMOS 和 PMOS **垂直堆疊**，而非水平並排：

```
    傳統 CMOS                    CFET
    (NMOS 和 PMOS 並排)          (NMOS 在 PMOS 上方)

    ┌──────┐  ┌──────┐          ┌──────┐
    │ PMOS │  │ NMOS │          │ NMOS │  ← 上方
    └──────┘  └──────┘          ├──────┤
                                │ PMOS │  ← 下方
    水平佈局 → 佔面積大           └──────┘

                                垂直堆疊 → 面積減半！
```

### 3.2 CFET 的優勢與挑戰

| 優勢 | 挑戰 |
|------|------|
| 面積大幅減少（理論減半） | 製程極為複雜 |
| 互連更短 → RC delay 降低 | 散熱問題（下層 PMOS 被上層包住） |
| 有利於繼續微縮 | 對準精度要求極高 |

### 3.3 電晶體架構演進路線圖

```
    時間軸 →
    ══════════════════════════════════════════════▶

    Planar     FinFET        GAA/Nanosheet    CFET
    ──────     ──────        ─────────────    ────
    > 22nm     22nm～3nm     2nm～下一代       未來

    1面         3面           4面              4面
    包覆        包覆          包覆             (堆疊)

    │          │             │                │
    ▼          ▼             ▼                ▼
   簡單       成熟主流       逐步量產          研發中
```

---

## 四、先進微影

### 4.1 多重圖案化（Multi-Patterning）

當目標圖案的間距（pitch）小於光學微影的單次解析度極限時，需要多次曝光。

#### LELE（Litho-Etch-Litho-Etch）

```
    第一次曝光 + 蝕刻               第二次曝光 + 蝕刻
    ┌──┐    ┌──┐    ┌──┐          ┌──┐ ┌┐┌──┐ ┌┐┌──┐
    │  │    │  │    │  │    →     │  │ │││  │ │││  │
    └──┘    └──┘    └──┘          └──┘ └┘└──┘ └┘└──┘
    ← pitch →                     ← pitch/2 →

    間距 = 原始 pitch               間距 = pitch/2（更密）
```

問題：兩次曝光的**對準誤差（Overlay）**會直接影響最終圖案精度。

#### SADP（Self-Aligned Double Patterning）★

**自對準**：不需要兩次獨立的曝光對準，而是利用薄膜沉積的自然對稱性。

```
    步驟 1：光阻圖案
    ┌──┐        ┌──┐
    │  │        │  │
    └──┘        └──┘

    步驟 2：沉積間隔物（Spacer）
    ┌┤  ├┐      ┌┤  ├┐     ← 間隔物（保形沉積）
    │└──┘│      │└──┘│
    └────┘      └────┘

    步驟 3：去除光阻芯（Mandrel）
     ┌┐  ┌┐     ┌┐  ┌┐     ← 只剩間隔物
     └┘  └┘     └┘  └┘

    間距從 P 變成 P/2！且自對準 → 不需要額外曝光對準
```

#### SAQP（Self-Aligned Quadruple Patterning）

做兩次 SADP → 間距變成 **P/4**。

### 4.2 EUV 單次 vs 多次曝光

| 方案 | 曝光次數 | 適用節點 | 說明 |
|------|---------|---------|------|
| ArF + SADP | 2～3 次 | 7nm | 成本高、步驟多 |
| EUV 單次曝光 | **1 次** | 7～5nm | 取代多重圖案化 ★ |
| EUV + SADP | 1 + 1 | 3nm 以下 | EUV 也需要多重圖案化了 |
| High-NA EUV | 1 次 | ≤ 2nm | NA 從 0.33 → 0.55 |

### 4.3 High-NA EUV

| 參數 | 現行 EUV | High-NA EUV |
|------|---------|-------------|
| NA | 0.33 | **0.55** |
| 解析度 | ~14 nm | **~8 nm** |
| 設備供應商 | ASML（獨家） | ASML（獨家） |
| 價格 | ~$1.5 億 | **> $3 億** |
| 首台交付 | — | 2024（Intel） |

---

## 五、先進封裝 ★業界熱門

### 5.1 為什麼先進封裝突然變重要？

| 驅動力 | 說明 |
|--------|------|
| 摩爾定律放緩 | 電晶體微縮越來越困難和昂貴 |
| Chiplet 趨勢 | 把大 SoC 拆成小晶片再封裝組合 |
| 異質整合 | 不同製程/材料/功能的晶片整合在一起 |
| HBM 記憶體 | 高頻寬記憶體需要先進封裝互連 |

### 5.2 封裝技術演進

```
    傳統                        先進
    ─────────────────────────────────────────▶
    Wire Bond → Flip Chip → 2.5D → 3D → Chiplet

    QFP        BGA          CoWoS    TSV   UCIe
    (腳多)     (球陣列)     (矽中介) (矽通孔) (標準介面)
```

### 5.3 2.5D 封裝

#### CoWoS（Chip on Wafer on Substrate）★TSMC 招牌

```
    ┌───────┐  ┌───────┐  ┌───────┐
    │  GPU  │  │ HBM   │  │ HBM   │   ← 多顆晶片
    │       │  │       │  │       │
    └───┬───┘  └───┬───┘  └───┬───┘
        │          │          │
    ════╪══════════╪══════════╪════
    │   ▼          ▼          ▼   │   ← 矽中介層（Silicon Interposer）
    │   ┌──────────────────────┐  │     含高密度繞線
    │   │  RDL（重佈線層）      │  │
    │   └──────────────────────┘  │
    ══════════════════════════════
              │
    ┌─────────┴─────────┐
    │    有機基板         │            ← Substrate
    │   (Organic Substrate)│
    └─────────┬─────────┘
              │
         ┌────┴────┐
         │  PCB    │                  ← 印刷電路板
         └─────────┘
```

特點：
- 用矽中介層（Si Interposer）提供晶片間的高密度連接
- 主要用於 **GPU + HBM**（如 NVIDIA A100, H100）
- 線寬/線距可達 ~0.4 μm（比有機基板密得多）

#### EMIB（Embedded Multi-die Interconnect Bridge）—— Intel

```
    ┌───────┐           ┌───────┐
    │ Die A │           │ Die B │
    └───┬───┘           └───┬───┘
        │                   │
    ────┼───────────────────┼────
    │   ▼    ┌────────┐    ▼   │   ← 有機基板
    │        │ EMIB   │        │     （中間嵌入矽橋）
    │        │(矽橋片)│        │
    │        └────────┘        │
    ────────────────────────────
```

比 CoWoS 便宜（不需要整片矽中介層），但密度稍低。

### 5.4 3D IC：TSV（Through-Silicon Via，矽通孔）

```
    ┌──────────────┐
    │   Die 2      │     ← 上層晶片
    │  ┌──┐  ┌──┐  │
    │  │  │  │  │  │     ← TSV（矽通孔）
    └──┤  ├──┤  ├──┘        穿透矽基板的垂直連接
    ┌──┤  ├──┤  ├──┐
    │  │  │  │  │  │
    │  └──┘  └──┘  │
    │   Die 1      │     ← 下層晶片
    └──────────────┘

    TSV 直徑：~5-10 μm
    TSV 高度：~50-100 μm
```

3D 堆疊的好處：
- **超短互連** → 低延遲、低功耗
- **面積效率** → 垂直堆疊節省平面面積
- 挑戰：**散熱**（被包住的晶片散熱困難）、**測試**（堆疊前測試 → Known Good Die, KGD）

### 5.5 Chiplet 架構 ★

#### 為什麼要用小晶片（Chiplet）？

| 問題 | Monolithic（單晶片） | Chiplet（小晶片組合） |
|------|---------------------|---------------------|
| 良率 | 面積大 → 良率低 | 面積小 → 良率高 ★ |
| 成本 | 全部用最先進製程 | 只有關鍵部分用先進製程 ★ |
| 設計彈性 | 一體設計 | 模組化、可重複使用 ★ |
| 上市時間 | 長（重新設計全部） | 短（混搭已驗證的 chiplet） |

#### 良率計算範例

假設缺陷密度 $D_0 = 0.1$ /cm²：
- 大晶片（500 mm²）：$Y = e^{-5 \times 0.1} = e^{-0.5} = 60.7\%$
- 小 Chiplet（100 mm² × 5）：$Y_{each} = e^{-1 \times 0.1} = e^{-0.1} = 90.5\%$
- 5 顆都好的機率：$0.905^5 = 60.6\%$

等等 —— 看起來差不多？但 Chiplet 的優勢在於：
- 可以分別測試，壞的丟掉 → 只用好的組裝
- 不同 Chiplet 可以用不同製程（CPU 用 3nm, I/O 用 12nm）→ 大幅降低成本

#### 業界範例

| 產品 | 架構 | 封裝 |
|------|------|------|
| AMD EPYC | CPU Chiplets + I/O Die | 有機基板 |
| AMD MI300 | GPU + CPU + HBM Chiplets | 3D + 2.5D |
| Apple M1 Ultra | 2 × M1 Max | UltraFusion（矽中介） |
| Intel Meteor Lake | CPU + GPU + SoC + I/O Tiles | Foveros 3D |

### 5.6 InFO（Integrated Fan-Out）★TSMC

```
    傳統封裝                     InFO

    ┌─────────┐                 ┌──────────────┐
    │   Die   │                 │  Die + RDL   │
    └────┬────┘                 │  (重佈線層)   │
         │                      └──────┬───────┘
    ┌────┴────┐                        │
    │ 基板    │                   不需要基板！
    │(Substrate)│                  直接扇出
    └─────────┘

    需要基板 → 貴               免基板 → 薄、便宜、性能好
```

InFO 特點：
- 不需要傳統的有機基板
- 封裝更薄、更輕
- 第一個大規模應用：Apple A10 處理器（iPhone 7）
- 衍生：InFO-PoP（Package on Package，用於手機）

---

## 六、TSMC / Intel / Samsung 製程路線圖

```
    年份    TSMC              Intel              Samsung
    ════    ════              ═════              ═══════
    2020    N5 (FinFET)       Intel 7            5nm (FinFET)
    2022    N3 (FinFET)       Intel 4            3nm (GAA) ★首個
    2024    N3E, N3P          Intel 20A(RibbonFET) 2nm (GAA)
    2025    N2 (GAA) ★        Intel 18A          SF2 (GAA)
    2026    N2P               Intel 18A+         SF1.4
    2027    A14 (1.4nm)       —                  —
    2028+   A10 (1nm)         —                  —
            ↓
          CFET 研發中
```

### 命名注意

- 製程名稱的「nm」數字**不代表任何實際物理尺寸**
- 只是商業命名（Marketing Name）
- 真正的指標是**邏輯密度**（MTr/mm²）和**PPA**（Performance, Power, Area）

---

## 關鍵術語表

| 術語 | 英文全名 | 說明 |
|------|---------|------|
| FinFET | Fin Field-Effect Transistor | 鰭式場效電晶體（3 面閘極） |
| GAA | Gate-All-Around | 全繞式閘極（4 面） |
| Nanosheet | — | 奈米片（GAA 的通道形狀） |
| CFET | Complementary FET | 互補 FET（NMOS/PMOS 垂直堆疊） |
| Hfin | — | 鰭片高度 |
| Wfin | — | 鰭片寬度 |
| Weff | Effective Width | 有效通道寬度 |
| SCE | Short Channel Effect | 短通道效應 |
| DIBL | Drain-Induced Barrier Lowering | 汲極引發位障降低 |
| SADP | Self-Aligned Double Patterning | 自對準雙重圖案化 |
| SAQP | Self-Aligned Quadruple Patterning | 自對準四重圖案化 |
| LELE | Litho-Etch-Litho-Etch | 微影蝕刻微影蝕刻 |
| High-NA | — | 高數值孔徑 EUV |
| CoWoS | Chip on Wafer on Substrate | TSMC 2.5D 封裝技術 |
| EMIB | Embedded Multi-die Interconnect Bridge | Intel 2.5D 封裝 |
| TSV | Through-Silicon Via | 矽通孔（3D 封裝互連） |
| Chiplet | — | 小晶片（模組化設計） |
| InFO | Integrated Fan-Out | 整合型扇出封裝（TSMC） |
| HBM | High Bandwidth Memory | 高頻寬記憶體 |
| KGD | Known Good Die | 已知良品晶粒 |
| RDL | Redistribution Layer | 重佈線層 |
| PPA | Performance, Power, Area | 效能、功耗、面積 |
| UCIe | Universal Chiplet Interconnect Express | Chiplet 標準介面 |

---

## 題型鑑別

| 看到什麼關鍵字 | 對應技術 | 答題方向 |
|---------------|---------|---------|
| 鰭片、3面包覆 | FinFET | Weff 計算、量化效應 |
| 全繞式、4面、Nanosheet | GAA | 與 FinFET 比較、堆疊層數 |
| NMOS/PMOS 堆疊 | CFET | 面積優勢、散熱挑戰 |
| 多重圖案化、SADP | 先進微影 | 自對準 vs LELE |
| CoWoS、矽中介 | 2.5D 封裝 | GPU + HBM 互連 |
| TSV、3D 堆疊 | 3D IC | 散熱、KGD 測試 |
| 小晶片、Chiplet | 模組化設計 | 良率、成本、混合製程 |
| InFO、扇出 | TSMC 封裝 | 免基板、手機應用 |

---

## ✅ 自我檢測

### 基礎題

<details>
<summary>Q1：FinFET 相比 Planar MOSFET 的核心改進是什麼？量化效應指什麼？</summary>

**答案**：
**核心改進**：通道從平面變成立體鰭片（Fin），閘極從 1 面包覆變成 **3 面包覆** → 大幅改善對通道的控制力 → 抑制短通道效應和漏電流。

**量化效應**：FinFET 的通道寬度 $W_{eff} = N_{fin} \times (2H_{fin} + W_{fin})$。由於 $N_{fin}$ 只能是**整數**（不能用半個 fin），所以驅動力只能是離散值。例如：
- 1 fin → Weff = 95 nm
- 2 fins → Weff = 190 nm
- 不能得到 150 nm 的 Weff

這與 Planar MOSFET 可以任意調整寬度 W 不同。
</details>

<details>
<summary>Q2：GAA/Nanosheet 比 FinFET 好在哪裡？為什麼要從 FinFET 轉向 GAA？</summary>

**答案**：

**GAA 的優勢**：
1. **4 面完全包覆**（vs FinFET 的 3 面）→ 更強的閘極控制力
2. **通道寬度可調**：調整 nanosheet 的寬度（連續值），比 FinFET 只能加減 fin 更靈活
3. **更好的 PPA**：在相同面積下提供更大的有效通道寬度

**為什麼要轉向**：
- FinFET 的 fin 要繼續縮小 → 寬度已接近量子極限（< 5nm），量子效應和製程變異太大
- 3 面包覆在通道極短時仍有漏電 → 需要 4 面完全包覆
- TSMC N2、Intel 20A、Samsung 3nm 都已轉向 GAA 架構
</details>

<details>
<summary>Q3：CoWoS 和 InFO 是什麼？各自的典型應用？</summary>

**答案**：

**CoWoS（Chip on Wafer on Substrate）**：
- TSMC 的 2.5D 封裝技術
- 用**矽中介層（Si Interposer）**連接多顆晶片
- 典型應用：**GPU + HBM**（如 NVIDIA H100、AMD MI300）
- 優勢：晶片間互連密度極高

**InFO（Integrated Fan-Out）**：
- TSMC 的免基板扇出型封裝
- 不需要傳統有機基板 → 更薄、更便宜
- 典型應用：**手機處理器**（Apple A 系列）
- 優勢：薄型化、低成本、良好的電氣性能
</details>

<details>
<summary>Q4：SADP（自對準雙重圖案化）的「自對準」指什麼？為什麼比 LELE 好？</summary>

**答案**：

**「自對準」的含義**：
SADP 中，間隔物（Spacer）是通過保形沉積（ALD/CVD）自然生長在光阻芯（Mandrel）的兩側。間距由薄膜厚度決定，不需要第二次曝光對準 → 自對準。

**比 LELE 好的原因**：
1. **對準精度高**：LELE 需要兩次獨立曝光，有對準誤差（Overlay error ~2nm）。SADP 由薄膜厚度決定，精度更高
2. **成本較低**：雖然步驟多，但不需要第二次完整的微影（只需一次曝光 + 薄膜沉積 + 蝕刻）
3. **線距均勻性好**：薄膜沉積的均勻性 > 兩次曝光的對準精度
</details>

<details>
<summary>Q5：Chiplet 架構的三個主要優勢？用 AMD EPYC 為例說明。</summary>

**答案**：

1. **良率優勢**：小 Chiplet 面積小 → 個別良率高 → 壞的丟掉只浪費小面積。AMD EPYC 用多顆 CPU Chiplet (~74mm² 每顆) 而非一顆大 die (~500mm²)，大幅提高良率

2. **成本優勢**：
   - CPU Chiplet 用 5nm（需要高性能）
   - I/O Die 用 14nm（不需最先進製程）
   - 混合製程大幅降低成本（14nm 的晶圓成本遠低於 5nm）

3. **設計彈性**：
   - 同一個 CPU Chiplet 可以用在不同產品（4 顆組成 32 核，8 顆組成 64 核）
   - 模組化設計，上市時間短
   - 可以獨立升級某個 Chiplet（如只換 CPU，保留 I/O）
</details>

<details>
<summary>Q6：FinFET 有效寬度計算：Hfin = 42 nm, Wfin = 7 nm。一個 NMOS 用 2 fins，一個 PMOS 用 3 fins。各自的 Weff？</summary>

**答案**：

每個 fin 的 Weff = $2 \times 42 + 7 = 91$ nm

NMOS（2 fins）：$W_{eff} = 2 \times 91 = \boxed{182 \text{ nm}}$

PMOS（3 fins）：$W_{eff} = 3 \times 91 = \boxed{273 \text{ nm}}$

注意：如果設計需要 Weff = 200 nm → 無法精確實現（只能選 182 nm 或 273 nm），這就是量化效應。
</details>

<details>
<summary>Q7：為什麼製程節點的「nm」數字不代表實際物理尺寸？用什麼指標才有意義？</summary>

**答案**：
- 早期（> 100nm），製程名稱確實對應閘極長度
- 但從 22nm 左右開始，命名變成**商業行銷名稱**，與任何實際尺寸脫節
- 例如：TSMC N7 的 fin pitch ~30nm，metal pitch ~40nm，沒有任何尺寸是 7nm

**有意義的指標**：
1. **邏輯密度**（MTr/mm²）：每平方毫米的電晶體數量
2. **PPA**（Performance, Power, Area）：相同功能的效能/功耗/面積三者的綜合表現
3. **Contacted Poly Pitch（CPP）**：電晶體的水平間距
4. **Metal Pitch**：最底層金屬的線距

例如：TSMC N5 的密度 ~173 MTr/mm²，N3 ~292 MTr/mm²，這才能真正比較。
</details>

---

> **下一章**：[eda_08_DFT測試與良率.md](eda_08_DFT測試與良率.md) —— 晶片做好了，怎麼確保它是好的？
