# Program — 多語言程式設計教學系列

> 從 Colab 等級到 NVIDIA 生產級開發者的完整學習路徑

## 目標

- 掌握 **Python / C++ / JavaScript / TypeScript / Go / Rust** 六大語言
- 理解大型專案架構（以 VisionDSL 電腦視覺專案為案例）
- 熟悉 Docker、DevOps、前後端開發等現代開發工具鏈
- 看到任何語言的程式碼都能產生**熟悉感**，快速理解語法與邏輯

## 教學特色

- **跨語言對照**：同一個問題用多種語言解決，建立語感
- **完整程式碼**：所有範例可直接執行，絕不省略
- **Input / Process / Output**：每個函式都標明輸入、處理、輸出
- **從簡單到複雜**：Colab 程度 → 函式 → 類別 → 專案 → 架構 → 生產部署
- **大量範例**：每個概念至少 2-3 個完整範例

---

## 目錄

| EP | 檔案 | 主題 | 行數 | 重點 |
|----|------|------|------|------|
| 01 | [EP01_Python從入門到專案級別.md](EP01_Python從入門到專案級別.md) | Python 完全攻略 | 2,271 | dataclass、裝飾器、`__init__`、`__slots__`、型別提示、設計模式 |
| 02 | [EP02_Python專案架構_從Colab到生產級.md](EP02_Python專案架構_從Colab到生產級.md) | Python 專案架構 | 3,252 | `__init__.py`、分層架構、設定管理、pytest、完整迷你專案 |
| 03 | [EP03_CPP_NVIDIA必備語言.md](EP03_CPP_NVIDIA必備語言.md) | C++ (NVIDIA 必備) | 1,391 | 指標、記憶體管理、Smart Pointer、STL、CUDA 入門 |
| 04 | [EP04_JavaScript_TypeScript全端開發.md](EP04_JavaScript_TypeScript全端開發.md) | JS / TS 全端 | 2,655 | async/await、TypeScript 型別系統、React、Node.js |
| 05 | [EP05_Go語言_高效並發程式設計.md](EP05_Go語言_高效並發程式設計.md) | Go 語言 | 2,456 | goroutine、channel、interface、泛型、REST API |
| 06 | [EP06_Rust_安全系統程式語言.md](EP06_Rust_安全系統程式語言.md) | Rust 語言 | 1,571 | 所有權、借用、trait、Result/Option、模式匹配 |
| 07 | [EP07_跨語言對照_同問題六種解法.md](EP07_跨語言對照_同問題六種解法.md) | 跨語言對照 | 3,065 | 12 道題目 × 5 種語言、語法速查表 |
| 08 | [EP08_Docker與DevOps實戰.md](EP08_Docker與DevOps實戰.md) | Docker / DevOps | 2,821 | Dockerfile、Compose、Git、CI/CD、Linux 指令 |
| 09 | [EP09_前後端開發實戰.md](EP09_前後端開發實戰.md) | 前後端開發 | 2,696 | Flask、FastAPI、React、TypeScript、JWT、部署 |
| 10 | [EP10_設計模式與進階架構.md](EP10_設計模式與進階架構.md) | 設計模式與架構 | 2,966 | SOLID、GoF 模式、系統設計、演算法、學習路線圖 |

**總計：10 集，25,144 行**

---

## 建議學習順序

```
第一週：EP01 → EP02（Python 基礎打穩）
第二週：EP03（C++ 理解底層）→ EP07 前半（跨語言對照）
第三週：EP04（JS/TS 全端）→ EP09（前後端實戰）
第四週：EP05（Go）→ EP06（Rust）→ EP07 後半
第五週：EP08（Docker/DevOps）→ EP10（設計模式與架構）
```

## NVIDIA 特化路線

```
EP01 Python → EP02 專案架構 → EP03 C++/CUDA → EP10 §12 NVIDIA 路線圖
         ↓
     EP07 跨語言對照（重點看 C++ 和 Rust 欄）
         ↓
     EP08 Docker（GPU Container）
```

## 語言覆蓋矩陣

| 概念 | Python | C++ | JS/TS | Go | Rust |
|------|--------|-----|-------|-----|------|
| 變數與型別 | EP01 | EP03 | EP04 | EP05 | EP06 |
| 函式 | EP01 | EP03 | EP04 | EP05 | EP06 |
| 類別/Struct | EP01 | EP03 | EP04 | EP05 | EP06 |
| 繼承/介面/Trait | EP01 | EP03 | EP04 | EP05 | EP06 |
| 錯誤處理 | EP01 | EP03 | EP04 | EP05 | EP06 |
| 並發/非同步 | EP10 | EP03 | EP04 | EP05 | EP06 |
| 專案架構 | EP02 | EP03 | EP04 | EP05 | EP06 |
| 跨語言對照 | EP07 | EP07 | EP07 | EP07 | EP07 |
| Docker | EP08 | EP08 | EP08 | EP08 | — |
| 前後端 | EP09 | — | EP09 | — | — |
| 設計模式 | EP10 | — | EP10 | EP10 | EP10 |

---

> 本系列以 [VisionDSL](https://github.com/taiwanfifi/VisionDSL) 專案為 Python 進階案例參考，
> 涵蓋 dataclass、type hints、`__slots__`、Registry Pattern、Lazy Import 等生產級技巧。
