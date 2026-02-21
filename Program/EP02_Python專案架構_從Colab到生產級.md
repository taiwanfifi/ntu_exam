# EP02 — Python 專案架構：從 Colab 到生產級

> **系列**：工程師自學程式・第二集
> **前置**：EP01（Python 基礎語法）
> **目標讀者**：習慣在 Colab 寫完整段程式、但從沒自己開過專案的人
> **教學案例**：VisionDSL — 一套即時影像 DSL 引擎（真實生產專案）

---

## 目錄

| 章 | 主題 | 重點 |
|----|------|------|
| 1 | 從單一腳本到專案 | 重構思維 |
| 2 | 套件結構詳解 | `__init__.py` 深潛 |
| 3 | 分層架構 | core / logic / pipeline / run |
| 4 | 設定管理 | JSON + argparse + 環境變數 |
| 5 | 錯誤處理策略 | 自訂 Exception + logging |
| 6 | 依賴管理 | requirements / pyproject / venv |
| 7 | 測試 | pytest 完整教學 |
| 8 | 完整迷你專案 | MiniVision 全檔案 |
| 9 | 常見反模式 | 踩雷清單 |

---

## 1. 從單一腳本到專案

### 1-1 典型 Colab 寫法（反面教材）

在 Colab 裡，我們經常把所有東西塞進同一個 cell：

```python
# bad_colab_script.py  ← 全部寫在一個檔案裡
import cv2
import json
import numpy as np
from dataclasses import dataclass

# ---- 設定 ----
CONFIG = {
    "model_path": "yolov8n.pt",
    "confidence": 0.5,
    "max_objects": 100,
    "output_dir": "./results",
}

# ---- 資料結構 ----
@dataclass
class Detection:
    label: str
    confidence: float
    x: int
    y: int
    w: int
    h: int

# ---- 偵測邏輯 ----
def detect_objects(frame, conf_threshold):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = []
    # 簡化示範：用 threshold 模擬偵測
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 500:
            score = min(1.0, (w * h) / 10000)
            if score >= conf_threshold:
                detections.append(Detection("object", score, x, y, w, h))
    return detections[:CONFIG["max_objects"]]

# ---- 繪圖 ----
def draw_boxes(frame, detections):
    for det in detections:
        color = (0, 255, 0)
        cv2.rectangle(frame, (det.x, det.y), (det.x + det.w, det.y + det.h), color, 2)
        text = f"{det.label} {det.confidence:.2f}"
        cv2.putText(frame, text, (det.x, det.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

# ---- 主程式 ----
def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        dets = detect_objects(frame, CONFIG["confidence"])
        result = draw_boxes(frame, dets)
        print(f"偵測到 {len(dets)} 個物件")
        # cv2.imshow("result", result)  # Colab 裡不能用
        break  # 示範只跑一幀
    cap.release()

main()
```

**問題在哪？**

| 問題 | 說明 |
|------|------|
| 設定寫死在程式裡 | 改一個門檻值要翻整份程式碼 |
| 資料結構、邏輯、呈現混在一起 | 改偵測邏輯可能不小心弄壞繪圖 |
| 無法測試 | `detect_objects` 綁定了 OpenCV，不能單獨跑 |
| 無法重用 | 別人要用你的偵測函式，得複製整份檔案 |
| 沒有錯誤處理 | 攝影機打不開？直接崩潰 |

### 1-2 重構第一步：拆檔案

先不動任何邏輯，純粹「搬家」：

```
my_detector/
├── core.py          # Detection dataclass
├── detector.py      # detect_objects()
├── visualize.py     # draw_boxes()
├── config.json      # 設定抽出
└── run.py           # main()
```

**core.py** — 只放資料結構：

```python
# core.py
from dataclasses import dataclass


@dataclass
class Detection:
    """一個偵測結果的資料容器。"""
    label: str
    confidence: float
    x: int
    y: int
    w: int
    h: int

    @property
    def area(self) -> int:
        return self.w * self.h

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "confidence": round(self.confidence, 4),
            "bbox": [self.x, self.y, self.w, self.h],
        }
```

**detector.py** — 只放偵測邏輯：

```python
# detector.py
import cv2
import numpy as np
from core import Detection


def detect_objects(
    frame: np.ndarray,
    conf_threshold: float = 0.5,
    max_objects: int = 100,
) -> list[Detection]:
    """
    對單幀影像執行物件偵測。

    Parameters
    ----------
    frame : np.ndarray
        BGR 格式的影像陣列。
    conf_threshold : float
        信心度門檻，低於此值的偵測會被丟棄。
    max_objects : int
        最多回傳幾個偵測結果。

    Returns
    -------
    list[Detection]
        排序後的偵測結果（信心度由高到低）。
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 500:
            score = min(1.0, (w * h) / 10000)
            if score >= conf_threshold:
                detections.append(Detection("object", score, x, y, w, h))

    detections.sort(key=lambda d: d.confidence, reverse=True)
    return detections[:max_objects]
```

**visualize.py** — 只放繪圖：

```python
# visualize.py
import cv2
import numpy as np
from core import Detection


def draw_boxes(frame: np.ndarray, detections: list[Detection]) -> np.ndarray:
    """在影像上畫出偵測框與標籤。回傳新影像，不修改原圖。"""
    output = frame.copy()
    color = (0, 255, 0)
    for det in detections:
        cv2.rectangle(output, (det.x, det.y), (det.x + det.w, det.y + det.h), color, 2)
        text = f"{det.label} {det.confidence:.2f}"
        cv2.putText(output, text, (det.x, det.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return output
```

**config.json** — 設定獨立出來：

```json
{
    "model_path": "yolov8n.pt",
    "confidence": 0.5,
    "max_objects": 100,
    "output_dir": "./results"
}
```

**run.py** — 入口點：

```python
# run.py
import json
import cv2
from detector import detect_objects
from visualize import draw_boxes


def load_config(path: str = "config.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config()
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    if not ret:
        print("錯誤：無法讀取攝影機")
        cap.release()
        return

    dets = detect_objects(frame, config["confidence"], config["max_objects"])
    result = draw_boxes(frame, dets)
    print(f"偵測到 {len(dets)} 個物件")

    cap.release()


if __name__ == "__main__":
    main()
```

### 1-3 重構帶來的好處

| 面向 | 改善 |
|------|------|
| 可讀性 | 每個檔案 < 50 行，職責一目瞭然 |
| 可測試 | `detect_objects` 可以餵假資料單獨測 |
| 可重用 | 別人只要 `from detector import detect_objects` |
| 可維護 | 改設定不必碰程式碼 |

> **VisionDSL 對照**：VisionDSL 正是這樣分的——`core.py` 放 `Entity`、`Session`、`FrameContext`；`logic.py` 放運算邏輯（1,220 行）；`pipeline.py` 做協調（353 行）；`run.py` 是 CLI 入口。

---

## 2. 套件結構詳解（`__init__.py` 深潛）

### 2-1 什麼是 Python 套件？

一個「含有 `__init__.py` 的資料夾」就是一個套件（package）。

```
mypackage/
├── __init__.py    ← 有這個檔案，Python 才認得這是套件
├── module_a.py
└── module_b.py
```

### 2-2 空的 `__init__.py`

最簡形式：檔案存在但內容為空。

```python
# mypackage/__init__.py
# （空檔案）
```

效果：你可以這樣引入：

```python
from mypackage import module_a
from mypackage.module_b import some_function
```

但不能直接 `from mypackage import some_function`，因為 `__init__.py` 什麼都沒匯出。

### 2-3 有內容的 `__init__.py`：定義公開 API

VisionDSL 的 `dsl/__init__.py` 長這樣：

```python
# dsl/__init__.py
"""VisionDSL 核心套件 — 公開 API 定義。"""

from dsl.core import Entity, Session, FrameContext
from dsl.logic import LogicEngine, Operator
from dsl.pipeline import VisionPipeline
from dsl.tracker import SessionManager

__all__ = [
    "Entity",
    "Session",
    "FrameContext",
    "LogicEngine",
    "Operator",
    "VisionPipeline",
    "SessionManager",
]

__version__ = "1.2.0"
```

這樣使用者可以寫：

```python
# 使用者的程式碼
from dsl import Entity, VisionPipeline  # 乾淨！不用知道內部檔案結構
```

### 2-4 `__all__` 的作用

`__all__` 控制兩件事：

1. **`from package import *` 會匯入哪些名稱**
2. **文件工具**（如 Sphinx）知道哪些是公開 API

完整範例：

```python
# demo_package/__init__.py
"""示範 __all__ 的效果。"""

from demo_package.public_stuff import useful_function, UsefulClass
from demo_package.internal_stuff import _helper  # 底線開頭 = 內部用

__all__ = [
    "useful_function",
    "UsefulClass",
    # 注意：_helper 不在 __all__ 裡
]
```

```python
# 使用者端
from demo_package import *

useful_function()   # OK
UsefulClass()       # OK
_helper()           # NameError — 沒有被匯出
```

### 2-5 完整範例：從零建立套件

```bash
# 終端指令
mkdir -p myproject/myproject
touch myproject/myproject/__init__.py
touch myproject/myproject/core.py
touch myproject/myproject/utils.py
```

**myproject/myproject/core.py**：

```python
# myproject/myproject/core.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """使用者資料模型。"""
    user_id: int
    name: str
    email: str
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

    def deactivate(self) -> None:
        self.is_active = False

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)


@dataclass
class Order:
    """訂單資料模型。"""
    order_id: int
    user_id: int
    items: list[str] = field(default_factory=list)
    total: float = 0.0
    status: str = "pending"
```

**myproject/myproject/utils.py**：

```python
# myproject/myproject/utils.py
import re


def validate_email(email: str) -> bool:
    """驗證 email 格式是否正確。"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def sanitize_name(name: str) -> str:
    """清理使用者名稱：去頭尾空白、統一小寫。"""
    return name.strip().lower()
```

**myproject/myproject/\_\_init\_\_.py**：

```python
# myproject/myproject/__init__.py
"""myproject — 使用者與訂單管理套件。"""

from myproject.core import User, Order
from myproject.utils import validate_email, sanitize_name

__all__ = [
    "User",
    "Order",
    "validate_email",
    "sanitize_name",
]

__version__ = "0.1.0"
```

現在使用者可以這樣用：

```python
from myproject import User, validate_email

if validate_email("alice@example.com"):
    user = User(user_id=1, name="Alice", email="alice@example.com")
    user.add_tag("vip")
    print(user)
```

### 2-6 子套件（Sub-packages）

VisionDSL 的 `backends/` 就是子套件：

```
dsl/
├── __init__.py
├── core.py
└── backends/           ← 子套件
    ├── __init__.py
    └── sam3_pipeline.py
```

子套件的 `__init__.py` 可以做「懶載入」（lazy import），避免一開始就載入沉重的相依套件：

```python
# dsl/backends/__init__.py
"""後端模組 — 使用懶載入避免啟動時載入重型依賴。"""


def get_sam3_pipeline():
    """需要時才載入 SAM3Pipeline，避免在不使用時引入 torch 等大型套件。"""
    from dsl.backends.sam3_pipeline import SAM3Pipeline
    return SAM3Pipeline


def get_tensorrt_backend():
    """需要時才載入 TensorRT 後端。"""
    from dsl.backends.tensorrt_backend import TensorRTBackend
    return TensorRTBackend
```

使用方式：

```python
# 只有真正呼叫時才會 import torch
SAM3Pipeline = get_sam3_pipeline()
pipeline = SAM3Pipeline(model_path="sam3.pt")
```

---

## 3. 分層架構（Layered Architecture）

### 3-1 VisionDSL 的四層架構

```
┌─────────────────────────────────────────┐
│  入口層 (Entry Point)     run.py        │  ← 接收 CLI 參數、啟動程式
├─────────────────────────────────────────┤
│  協調層 (Orchestration)   pipeline.py   │  ← 串接各模組、控制流程
├─────────────────────────────────────────┤
│  邏輯層 (Business Logic)  logic.py      │  ← 核心演算法、規則引擎
│                            tracker.py   │
│                            kalman.py    │
├─────────────────────────────────────────┤
│  資料層 (Data Layer)      core.py       │  ← dataclass、型別定義
└─────────────────────────────────────────┘
```

**依賴方向**：上層可以引用下層，下層**絕不**引用上層。

```
run.py → pipeline.py → logic.py → core.py
                      → tracker.py → core.py
```

### 3-2 為什麼要分層？

| 原則 | 說明 |
|------|------|
| 單一職責 | 每個檔案只做一件事 |
| 依賴方向單一 | 避免循環引用 |
| 可替換 | 換偵測模型？只改邏輯層，入口層不動 |
| 可測試 | 測邏輯層不需要啟動整個 pipeline |

### 3-3 實作：簡化版三層架構

我們用一個「文字分析器」來示範分層。三個檔案，每個都完整可執行。

**analyzer/core.py** — 資料層：

```python
# analyzer/core.py
"""資料層：只定義資料結構，不含任何邏輯。"""

from dataclasses import dataclass, field


@dataclass
class WordStats:
    """單字統計結果。"""
    word: str
    count: int
    frequency: float = 0.0

    def __post_init__(self):
        self.word = self.word.lower()


@dataclass
class AnalysisResult:
    """一次分析的完整結果。"""
    source: str
    total_words: int
    unique_words: int
    top_words: list[WordStats] = field(default_factory=list)
    avg_word_length: float = 0.0

    def summary(self) -> str:
        lines = [
            f"來源: {self.source}",
            f"總字數: {self.total_words}",
            f"不重複字數: {self.unique_words}",
            f"平均字長: {self.avg_word_length:.1f}",
            "前五高頻字:",
        ]
        for ws in self.top_words[:5]:
            lines.append(f"  {ws.word}: {ws.count} 次 ({ws.frequency:.1%})")
        return "\n".join(lines)
```

**analyzer/logic.py** — 邏輯層：

```python
# analyzer/logic.py
"""邏輯層：核心演算法，只依賴 core.py。"""

import re
from collections import Counter
from analyzer.core import WordStats, AnalysisResult


# 英文停用詞表
STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "shall",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "it", "this", "that", "and", "or", "but", "not", "no", "if",
    "i", "you", "he", "she", "we", "they", "me", "him", "her",
    "us", "them", "my", "your", "his", "its", "our", "their",
})


def tokenize(text: str) -> list[str]:
    """將文字拆成單字列表（小寫、去標點）。"""
    text = text.lower()
    words = re.findall(r"[a-z]+", text)
    return words


def remove_stop_words(words: list[str]) -> list[str]:
    """移除停用詞。"""
    return [w for w in words if w not in STOP_WORDS]


def compute_stats(words: list[str], top_n: int = 10) -> list[WordStats]:
    """計算字頻統計。"""
    total = len(words)
    if total == 0:
        return []

    counter = Counter(words)
    result = []
    for word, count in counter.most_common(top_n):
        freq = count / total
        result.append(WordStats(word=word, count=count, frequency=freq))
    return result


def analyze_text(text: str, source: str = "unknown") -> AnalysisResult:
    """
    對一段文字執行完整分析。

    Parameters
    ----------
    text : str
        要分析的文字。
    source : str
        文字來源標記。

    Returns
    -------
    AnalysisResult
        分析結果。
    """
    all_words = tokenize(text)
    filtered = remove_stop_words(all_words)

    total = len(filtered)
    unique = len(set(filtered))
    top = compute_stats(filtered, top_n=10)

    avg_len = 0.0
    if filtered:
        avg_len = sum(len(w) for w in filtered) / len(filtered)

    return AnalysisResult(
        source=source,
        total_words=total,
        unique_words=unique,
        top_words=top,
        avg_word_length=avg_len,
    )
```

**analyzer/pipeline.py** — 協調層 + 入口：

```python
# analyzer/pipeline.py
"""協調層：串接讀檔 → 分析 → 輸出，處理 I/O 與錯誤。"""

import json
import sys
from pathlib import Path
from analyzer.logic import analyze_text
from analyzer.core import AnalysisResult


def read_file(path: str) -> str:
    """讀取文字檔，處理編碼問題。"""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"檔案不存在: {path}")
    return file_path.read_text(encoding="utf-8")


def save_result(result: AnalysisResult, output_path: str) -> None:
    """將分析結果存成 JSON。"""
    data = {
        "source": result.source,
        "total_words": result.total_words,
        "unique_words": result.unique_words,
        "avg_word_length": result.avg_word_length,
        "top_words": [
            {"word": ws.word, "count": ws.count, "frequency": round(ws.frequency, 4)}
            for ws in result.top_words
        ],
    }
    Path(output_path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def run_pipeline(input_path: str, output_path: str) -> AnalysisResult:
    """完整流程：讀檔 → 分析 → 存檔 → 回傳。"""
    text = read_file(input_path)
    result = analyze_text(text, source=input_path)
    save_result(result, output_path)
    return result


def main():
    """CLI 入口。"""
    if len(sys.argv) < 2:
        print("用法: python -m analyzer.pipeline <input_file> [output_file]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "result.json"

    try:
        result = run_pipeline(input_path, output_path)
        print(result.summary())
        print(f"\n結果已存至: {output_path}")
    except FileNotFoundError as e:
        print(f"錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 3-4 層次之間的呼叫關係

```
main()                          ← pipeline.py（協調層）
  ├── read_file()               ← pipeline.py（I/O）
  ├── analyze_text()            ← logic.py（邏輯層）
  │     ├── tokenize()          ← logic.py
  │     ├── remove_stop_words() ← logic.py
  │     └── compute_stats()     ← logic.py
  │           └── WordStats()   ← core.py（資料層）
  └── save_result()             ← pipeline.py（I/O）
```

核心觀念：**core.py 不 import 任何專案內的模組**，它是最底層。

---

## 4. 設定管理（Configuration Management）

### 4-1 JSON 設定檔

VisionDSL 用 `configs/` 目錄放 JSON 設定：

```json
{
    "model": {
        "path": "weights/yolov8n.engine",
        "input_size": [640, 640],
        "confidence_threshold": 0.5,
        "nms_threshold": 0.45
    },
    "tracker": {
        "max_age": 30,
        "min_hits": 3,
        "iou_threshold": 0.3
    },
    "output": {
        "directory": "./results",
        "save_video": true,
        "save_json": true
    }
}
```

讀取設定的完整程式碼：

```python
# config_loader.py
"""設定載入器：支援 JSON 檔 + 預設值合併。"""

import json
from pathlib import Path
from typing import Any


# 預設設定 — 所有選項都必須有預設值
DEFAULT_CONFIG = {
    "model": {
        "path": "weights/yolov8n.engine",
        "input_size": [640, 640],
        "confidence_threshold": 0.5,
        "nms_threshold": 0.45,
    },
    "tracker": {
        "max_age": 30,
        "min_hits": 3,
        "iou_threshold": 0.3,
    },
    "output": {
        "directory": "./results",
        "save_video": True,
        "save_json": True,
    },
}


def deep_merge(base: dict, override: dict) -> dict:
    """
    深層合併兩個字典。override 的值會覆蓋 base。

    >>> deep_merge({"a": {"b": 1, "c": 2}}, {"a": {"b": 99}})
    {'a': {'b': 99, 'c': 2}}
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str = "configs/default.json") -> dict:
    """
    載入設定檔並與預設值合併。

    - 如果檔案不存在，使用純預設值。
    - 如果檔案存在，使用者的設定會覆蓋對應的預設值。
    - 使用者沒指定的欄位保留預設值。
    """
    path = Path(config_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        return deep_merge(DEFAULT_CONFIG, user_config)
    else:
        print(f"警告: 設定檔 {config_path} 不存在，使用預設值")
        return DEFAULT_CONFIG.copy()


def get_nested(config: dict, dotted_key: str, default: Any = None) -> Any:
    """
    用點分隔的 key 取巢狀字典的值。

    >>> cfg = {"model": {"confidence_threshold": 0.5}}
    >>> get_nested(cfg, "model.confidence_threshold")
    0.5
    >>> get_nested(cfg, "model.missing_key", 42)
    42
    """
    keys = dotted_key.split(".")
    current = config
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    return current
```

### 4-2 argparse CLI 參數

```python
# cli.py
"""命令列參數解析器。"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """建立 CLI 參數解析器。"""
    parser = argparse.ArgumentParser(
        description="VisionDSL 影像分析引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python run.py --config configs/custom.json
  python run.py --source video.mp4 --confidence 0.7
  python run.py --source 0 --no-save-video
        """,
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default="configs/default.json",
        help="設定檔路徑 (預設: configs/default.json)",
    )
    parser.add_argument(
        "--source", "-s",
        type=str,
        default="0",
        help="影像來源：檔案路徑或攝影機編號 (預設: 0)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=None,
        help="覆蓋設定檔中的信心度門檻",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="覆蓋設定檔中的輸出目錄",
    )
    parser.add_argument(
        "--no-save-video",
        action="store_true",
        help="不儲存影片結果",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="顯示詳細日誌",
    )

    return parser


def parse_args(argv: list[str] = None) -> argparse.Namespace:
    """解析命令列參數。"""
    parser = build_parser()
    return parser.parse_args(argv)
```

### 4-3 環境變數

```python
# env_config.py
"""從環境變數讀取敏感設定（API key 等不該寫進設定檔的東西）。"""

import os


def get_env(key: str, default: str = None, required: bool = False) -> str:
    """
    讀取環境變數。

    Parameters
    ----------
    key : str
        環境變數名稱。
    default : str, optional
        預設值。
    required : bool
        若為 True 且環境變數不存在，拋出例外。

    Returns
    -------
    str
        環境變數的值。
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise EnvironmentError(
            f"必要的環境變數 {key} 未設定。"
            f"\n請執行: export {key}=<value>"
        )
    return value


# 使用範例
API_KEY = get_env("VISION_API_KEY", required=False)
MODEL_CACHE_DIR = get_env("MODEL_CACHE_DIR", default="/tmp/models")
DEBUG_MODE = get_env("DEBUG", default="false").lower() == "true"
```

### 4-4 三者整合

```python
# run.py — 把 JSON 設定、CLI 參數、環境變數合在一起
"""入口點：整合所有設定來源。"""

from config_loader import load_config
from cli import parse_args
from env_config import get_env


def build_final_config() -> dict:
    """
    設定優先順序（後者覆蓋前者）：
    1. 程式內建預設值
    2. JSON 設定檔
    3. 環境變數
    4. CLI 參數（最高優先）
    """
    # 步驟 1+2：載入設定檔（已含預設值合併）
    args = parse_args()
    config = load_config(args.config)

    # 步驟 3：環境變數覆蓋
    env_confidence = get_env("VISION_CONFIDENCE")
    if env_confidence is not None:
        config["model"]["confidence_threshold"] = float(env_confidence)

    # 步驟 4：CLI 參數覆蓋（只覆蓋使用者明確指定的）
    if args.confidence is not None:
        config["model"]["confidence_threshold"] = args.confidence
    if args.output_dir is not None:
        config["output"]["directory"] = args.output_dir
    if args.no_save_video:
        config["output"]["save_video"] = False

    # 附加 CLI 專屬設定
    config["source"] = args.source
    config["verbose"] = args.verbose

    return config


if __name__ == "__main__":
    config = build_final_config()
    print("最終設定:")
    import json
    print(json.dumps(config, indent=2, ensure_ascii=False))
```

---

## 5. 錯誤處理策略（Error Handling Strategy）

### 5-1 自定義 Exception 類別

```python
# exceptions.py
"""專案自訂例外類別。

階層設計：
    VisionError               ← 所有專案例外的基底類別
    ├── ConfigError           ← 設定相關錯誤
    │   ├── ConfigNotFound
    │   └── ConfigInvalid
    ├── ModelError            ← 模型相關錯誤
    │   ├── ModelNotFound
    │   └── ModelLoadFailed
    ├── PipelineError         ← 管線執行錯誤
    │   ├── SourceNotAvailable
    │   └── ProcessingFailed
    └── DetectionError        ← 偵測邏輯錯誤
"""


class VisionError(Exception):
    """所有 VisionDSL 例外的基底類別。"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = details or {}


# --- 設定類錯誤 ---

class ConfigError(VisionError):
    """設定相關錯誤的基底。"""
    pass


class ConfigNotFound(ConfigError):
    """設定檔不存在。"""

    def __init__(self, path: str):
        super().__init__(
            f"設定檔不存在: {path}",
            details={"path": path},
        )


class ConfigInvalid(ConfigError):
    """設定內容不合法。"""

    def __init__(self, path: str, reason: str):
        super().__init__(
            f"設定檔格式錯誤 ({path}): {reason}",
            details={"path": path, "reason": reason},
        )


# --- 模型類錯誤 ---

class ModelError(VisionError):
    """模型相關錯誤的基底。"""
    pass


class ModelNotFound(ModelError):
    """模型檔不存在。"""

    def __init__(self, path: str):
        super().__init__(
            f"模型檔不存在: {path}",
            details={"path": path},
        )


class ModelLoadFailed(ModelError):
    """模型載入失敗。"""

    def __init__(self, path: str, reason: str):
        super().__init__(
            f"無法載入模型 {path}: {reason}",
            details={"path": path, "reason": reason},
        )


# --- 管線類錯誤 ---

class PipelineError(VisionError):
    """管線執行錯誤的基底。"""
    pass


class SourceNotAvailable(PipelineError):
    """影像來源無法開啟。"""

    def __init__(self, source: str):
        super().__init__(
            f"無法開啟影像來源: {source}",
            details={"source": source},
        )


class ProcessingFailed(PipelineError):
    """影像處理中發生錯誤。"""

    def __init__(self, frame_id: int, reason: str):
        super().__init__(
            f"第 {frame_id} 幀處理失敗: {reason}",
            details={"frame_id": frame_id, "reason": reason},
        )
```

### 5-2 在哪一層處理什麼錯誤

```
┌──────────────────────────────────────────────────────────────┐
│ 入口層 (run.py)                                              │
│   捕捉: VisionError (所有專案例外)                             │
│   動作: 印出使用者友善訊息、設定 exit code                      │
├──────────────────────────────────────────────────────────────┤
│ 協調層 (pipeline.py)                                         │
│   捕捉: 特定可恢復的錯誤 (如單幀失敗)                          │
│   動作: 記 log、跳過該幀、繼續執行                              │
│   拋出: PipelineError (無法恢復的錯誤往上丟)                    │
├──────────────────────────────────────────────────────────────┤
│ 邏輯層 (logic.py)                                            │
│   捕捉: 通常不捕捉 — 讓錯誤自然浮上去                          │
│   拋出: DetectionError, ValueError                            │
├──────────────────────────────────────────────────────────────┤
│ 資料層 (core.py)                                             │
│   捕捉: 無                                                    │
│   拋出: 只用 __post_init__ 做基本驗證                          │
└──────────────────────────────────────────────────────────────┘
```

實際範例：

```python
# pipeline.py 中的錯誤處理
import logging
from exceptions import SourceNotAvailable, ProcessingFailed

logger = logging.getLogger(__name__)


def process_video(source: str, config: dict) -> None:
    """處理影片的主迴圈 — 示範各層錯誤處理。"""
    import cv2

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SourceNotAvailable(source)  # 無法恢復 → 往上丟

    frame_id = 0
    error_count = 0
    max_errors = config.get("max_consecutive_errors", 10)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.info("影像來源結束，共處理 %d 幀", frame_id)
                break

            try:
                # 這裡呼叫邏輯層
                result = detect_and_track(frame, config)
                error_count = 0  # 成功 → 重設連續錯誤計數
                frame_id += 1
            except Exception as e:
                # 單幀失敗是可恢復的 → 記 log、跳過
                error_count += 1
                logger.warning("第 %d 幀處理失敗: %s", frame_id, e)
                frame_id += 1

                if error_count >= max_errors:
                    raise ProcessingFailed(
                        frame_id,
                        f"連續 {max_errors} 幀失敗，中止處理",
                    )
    finally:
        cap.release()  # 無論如何都要釋放資源
        logger.info("攝影機資源已釋放")
```

### 5-3 logging 模組完整教學

```python
# log_setup.py
"""日誌設定模組 — 完整的 logging 教學。"""

import logging
import logging.handlers
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> None:
    """
    設定全域日誌系統。

    Parameters
    ----------
    level : str
        日誌等級: DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_file : str, optional
        日誌檔路徑。None 表示只輸出到終端。
    max_bytes : int
        單一日誌檔最大大小（bytes），超過會自動輪替。
    backup_count : int
        保留幾份舊日誌檔。
    """
    # 取得根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # 清除舊的 handler（避免重複設定）
    root_logger.handlers.clear()

    # 格式器
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: 終端輸出（stderr）
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler 2: 檔案輸出（可選）
    if log_file is not None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # 降低第三方套件的日誌等級
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)


# ---- 使用範例 ----

def demo_logging():
    """示範各等級的日誌用法。"""
    setup_logging(level="DEBUG", log_file="logs/app.log")

    # 每個模組用自己的 logger
    logger = logging.getLogger(__name__)

    logger.debug("除錯訊息：變數 x = %d", 42)
    logger.info("系統啟動完成")
    logger.warning("記憶體使用率達 85%%")
    logger.error("無法連線到資料庫: %s", "timeout")

    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("計算過程發生例外")
        # .exception() 會自動附上 traceback


if __name__ == "__main__":
    demo_logging()
```

輸出結果類似：

```
2026-02-21 10:30:00 | DEBUG    | __main__             | 除錯訊息：變數 x = 42
2026-02-21 10:30:00 | INFO     | __main__             | 系統啟動完成
2026-02-21 10:30:00 | WARNING  | __main__             | 記憶體使用率達 85%
2026-02-21 10:30:00 | ERROR    | __main__             | 無法連線到資料庫: timeout
2026-02-21 10:30:00 | ERROR    | __main__             | 計算過程發生例外
Traceback (most recent call last):
  File "log_setup.py", line 82, in demo_logging
    result = 1 / 0
ZeroDivisionError: division by zero
```

### 5-4 logging 等級選擇指南

| 等級 | 用途 | 範例 |
|------|------|------|
| `DEBUG` | 開發階段的詳細資訊 | 變數值、函式進出 |
| `INFO` | 正常運作的重要事件 | 「模型載入完成」、「處理了 100 幀」 |
| `WARNING` | 值得注意但還沒壞 | 「使用了預設值」、「接近記憶體上限」 |
| `ERROR` | 出錯了但程式還能跑 | 「單幀處理失敗，跳過」 |
| `CRITICAL` | 嚴重錯誤，程式可能要停 | 「模型載入失敗」、「磁碟空間不足」 |

---

## 6. 依賴管理

### 6-1 requirements.txt

最基本的依賴記錄方式：

```
# requirements.txt
# 格式: 套件名==版本號

# 核心依賴
numpy==1.26.4
opencv-python==4.9.0.80
Pillow==10.2.0

# 機器學習
torch==2.2.1
ultralytics==8.1.0

# 工具
tqdm==4.66.2
pyyaml==6.0.1

# 開發工具（可另存為 requirements-dev.txt）
# pytest==8.0.2
# black==24.2.0
# mypy==1.8.0
```

安裝指令：

```bash
pip install -r requirements.txt
```

建議做法——把開發依賴分開：

```
# requirements-dev.txt
-r requirements.txt     # 先安裝正式依賴

# 測試
pytest==8.0.2
pytest-cov==4.1.0

# 程式碼品質
black==24.2.0
ruff==0.3.0
mypy==1.8.0
```

### 6-2 pyproject.toml（現代標準）

Python 社群正在從 `setup.py` 遷移到 `pyproject.toml`。這是現在推薦的方式：

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "vision-dsl"
version = "1.2.0"
description = "即時影像分析的領域特定語言引擎"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Vision Team", email = "team@example.com"},
]

# 正式依賴
dependencies = [
    "numpy>=1.24,<2.0",
    "opencv-python>=4.8",
    "Pillow>=10.0",
    "tqdm>=4.65",
]

# 可選依賴群組
[project.optional-dependencies]
gpu = [
    "torch>=2.1",
    "tensorrt>=8.6",
]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "black>=24.0",
    "ruff>=0.3",
    "mypy>=1.8",
]
all = ["vision-dsl[gpu,dev]"]

# CLI 入口點
[project.scripts]
vision-dsl = "dsl.run:main"

[tool.setuptools.packages.find]
include = ["dsl*"]

# 工具設定也可以放這裡
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
```

安裝指令：

```bash
# 安裝正式版
pip install .

# 安裝含 GPU 支援
pip install ".[gpu]"

# 安裝含開發工具
pip install ".[dev]"

# 安裝全部
pip install ".[all]"
```

### 6-3 setup.py（傳統方式，仍常見）

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="vision-dsl",
    version="1.2.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
        "opencv-python>=4.8",
        "Pillow>=10.0",
        "tqdm>=4.65",
    ],
    extras_require={
        "dev": ["pytest>=8.0", "black>=24.0"],
    },
    entry_points={
        "console_scripts": [
            "vision-dsl=dsl.run:main",
        ],
    },
)
```

### 6-4 虛擬環境（venv）

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動（macOS / Linux）
source .venv/bin/activate

# 啟動（Windows）
.venv\Scripts\activate

# 確認是在虛擬環境裡
which python
# 應該顯示 .venv/bin/python

# 安裝依賴
pip install -r requirements.txt

# 退出虛擬環境
deactivate
```

### 6-5 pip install -e .（可編輯模式）

這是專案開發最重要的指令之一：

```bash
# 在專案根目錄執行
pip install -e .

# 如果有 dev 依賴
pip install -e ".[dev]"
```

**做了什麼？** 不是複製你的程式碼到 site-packages，而是建立一個指向你專案目錄的連結。

**效果**：

```python
# 安裝前：必須用相對路徑
from dsl.core import Entity    # 只有在專案目錄裡才能跑

# 安裝後 (-e .)：任何地方都能引用
from dsl.core import Entity    # 在任何目錄、任何腳本都能用
```

**為什麼叫「可編輯」？** 因為你改了原始碼，效果立即反映，不需要重新安裝。

---

## 7. 測試（Testing）

### 7-1 pytest 基本用法

pytest 是 Python 最流行的測試框架。安裝：

```bash
pip install pytest
```

最簡單的測試：

```python
# test_basic.py
"""pytest 最基本的範例。"""


def add(a: int, b: int) -> int:
    return a + b


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 0) == 0
```

執行：

```bash
pytest test_basic.py -v
```

### 7-2 測試目錄結構

```
project/
├── my_package/
│   ├── __init__.py
│   ├── core.py
│   └── logic.py
├── tests/
│   ├── __init__.py        ← 可以是空的
│   ├── conftest.py        ← 共用 fixture 放這裡
│   ├── test_core.py       ← 對應 core.py
│   └── test_logic.py      ← 對應 logic.py
└── pyproject.toml
```

命名規則：
- 測試檔案：`test_*.py` 或 `*_test.py`
- 測試函式：`test_*`
- 測試類別：`Test*`

### 7-3 fixture（測試夾具）

fixture 用來準備測試需要的資料或物件。

```python
# tests/conftest.py
"""共用的 test fixtures。"""

import json
import pytest
from pathlib import Path


@pytest.fixture
def sample_config():
    """提供一份標準測試設定。"""
    return {
        "model": {
            "path": "test_model.pt",
            "confidence_threshold": 0.5,
        },
        "tracker": {
            "max_age": 30,
            "iou_threshold": 0.3,
        },
    }


@pytest.fixture
def config_file(tmp_path, sample_config):
    """在臨時目錄建立設定檔，測試結束自動清除。"""
    config_path = tmp_path / "test_config.json"
    config_path.write_text(
        json.dumps(sample_config, indent=2),
        encoding="utf-8",
    )
    return str(config_path)


@pytest.fixture
def sample_text():
    """提供一段測試用文字。"""
    return (
        "The quick brown fox jumps over the lazy dog. "
        "The dog barked at the fox. The fox ran away quickly."
    )
```

### 7-4 mock（模擬）

```python
# tests/test_with_mock.py
"""示範 mock 的用法 — 模擬外部依賴。"""

from unittest.mock import Mock, patch, MagicMock
import pytest


# ---- 被測程式 ----

class DatabaseClient:
    def query(self, sql: str) -> list[dict]:
        raise NotImplementedError("需要真實資料庫連線")


class UserService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_active_users(self) -> list[str]:
        rows = self.db.query("SELECT name FROM users WHERE active = 1")
        return [row["name"] for row in rows]

    def count_users(self) -> int:
        rows = self.db.query("SELECT COUNT(*) as cnt FROM users")
        return rows[0]["cnt"]


# ---- 測試 ----

def test_get_active_users_with_mock():
    """用 Mock 物件替換資料庫，不需要真實連線。"""
    mock_db = Mock(spec=DatabaseClient)
    mock_db.query.return_value = [
        {"name": "Alice"},
        {"name": "Bob"},
    ]

    service = UserService(db=mock_db)
    result = service.get_active_users()

    assert result == ["Alice", "Bob"]
    mock_db.query.assert_called_once_with(
        "SELECT name FROM users WHERE active = 1"
    )


def test_count_users_with_mock():
    """另一個 Mock 範例。"""
    mock_db = Mock(spec=DatabaseClient)
    mock_db.query.return_value = [{"cnt": 42}]

    service = UserService(db=mock_db)
    assert service.count_users() == 42


def test_get_active_users_empty():
    """測試空結果的情況。"""
    mock_db = Mock(spec=DatabaseClient)
    mock_db.query.return_value = []

    service = UserService(db=mock_db)
    result = service.get_active_users()

    assert result == []
```

### 7-5 parametrize（參數化測試）

```python
# tests/test_parametrize.py
"""示範 parametrize — 一個測試函式跑多組資料。"""

import pytest


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """計算 BMI。"""
    if height_m <= 0:
        raise ValueError("身高必須大於零")
    if weight_kg <= 0:
        raise ValueError("體重必須大於零")
    return round(weight_kg / (height_m ** 2), 1)


def classify_bmi(bmi: float) -> str:
    """BMI 分類。"""
    if bmi < 18.5:
        return "過輕"
    elif bmi < 24.0:
        return "正常"
    elif bmi < 27.0:
        return "過重"
    else:
        return "肥胖"


@pytest.mark.parametrize("weight, height, expected_bmi", [
    (70.0, 1.75, 22.9),
    (50.0, 1.60, 19.5),
    (90.0, 1.80, 27.8),
    (45.0, 1.55, 18.7),
    (120.0, 1.70, 41.5),
])
def test_calculate_bmi(weight, height, expected_bmi):
    """五組資料，自動跑五次測試。"""
    assert calculate_bmi(weight, height) == expected_bmi


@pytest.mark.parametrize("bmi, expected_class", [
    (16.0, "過輕"),
    (18.4, "過輕"),
    (18.5, "正常"),
    (22.0, "正常"),
    (24.0, "過重"),
    (26.9, "過重"),
    (27.0, "肥胖"),
    (35.0, "肥胖"),
])
def test_classify_bmi(bmi, expected_class):
    """八組資料，自動跑八次。"""
    assert classify_bmi(bmi) == expected_class


@pytest.mark.parametrize("weight, height", [
    (70.0, 0.0),
    (70.0, -1.5),
    (0.0, 1.75),
    (-10.0, 1.75),
])
def test_calculate_bmi_invalid_input(weight, height):
    """測試非法輸入應該拋出 ValueError。"""
    with pytest.raises(ValueError):
        calculate_bmi(weight, height)
```

### 7-6 三個完整測試函式（搭配 analyzer 專案）

```python
# tests/test_analyzer.py
"""analyzer 專案的測試。"""

import pytest
from analyzer.core import WordStats, AnalysisResult
from analyzer.logic import tokenize, remove_stop_words, analyze_text


def test_tokenize_basic():
    """測試基本斷詞功能。"""
    text = "Hello, World! This is a TEST."
    result = tokenize(text)
    assert result == ["hello", "world", "this", "is", "a", "test"]


def test_remove_stop_words():
    """測試停用詞移除。"""
    words = ["the", "quick", "brown", "fox", "is", "running"]
    result = remove_stop_words(words)
    # "the" 和 "is" 是停用詞，應被移除
    assert "the" not in result
    assert "is" not in result
    assert "quick" in result
    assert "fox" in result


def test_analyze_text_full():
    """測試完整分析流程。"""
    text = "python python python java java go"
    result = analyze_text(text, source="test")

    assert isinstance(result, AnalysisResult)
    assert result.source == "test"
    assert result.total_words == 6  # 沒有停用詞，全保留
    assert result.unique_words == 3
    assert result.top_words[0].word == "python"
    assert result.top_words[0].count == 3
```

---

## 8. 完整迷你專案（MiniVision）

以下是一個完整的迷你影像偵測專案，每個檔案都有完整內容。

### 目錄結構

```
mini_vision/
├── mini_vision/
│   ├── __init__.py       # 套件公開 API
│   ├── core.py           # 資料層：Entity dataclass
│   ├── detector.py       # 邏輯層：偵測演算法
│   └── pipeline.py       # 協調層：串接流程
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py  # 完整測試
├── configs/
│   └── default.json      # 預設設定
├── run.py                # CLI 入口
└── requirements.txt      # 依賴清單
```

### mini_vision/mini_vision/\_\_init\_\_.py

```python
# mini_vision/mini_vision/__init__.py
"""MiniVision — 輕量影像偵測框架。

Usage:
    from mini_vision import Entity, Detector, Pipeline

Public API:
    Entity    - 偵測結果的資料容器
    Detector  - 偵測邏輯引擎
    Pipeline  - 協調讀取、偵測、輸出的完整流程
"""

from mini_vision.core import Entity
from mini_vision.detector import Detector
from mini_vision.pipeline import Pipeline

__all__ = [
    "Entity",
    "Detector",
    "Pipeline",
]

__version__ = "0.1.0"
```

### mini_vision/mini_vision/core.py

```python
# mini_vision/mini_vision/core.py
"""資料層：只放資料結構定義，不含任何業務邏輯。

這個檔案是最底層，不 import 任何專案內的其他模組。
其他所有模組都可以安全地 import core.py，不會造成循環引用。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BoundingBox:
    """邊界框座標（左上角 + 寬高）。"""
    x: int
    y: int
    width: int
    height: int

    @property
    def area(self) -> int:
        """計算面積。"""
        return self.width * self.height

    @property
    def center(self) -> tuple[float, float]:
        """計算中心點座標。"""
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        return (cx, cy)

    def to_xyxy(self) -> tuple[int, int, int, int]:
        """轉換成 (x1, y1, x2, y2) 格式。"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def iou(self, other: "BoundingBox") -> float:
        """計算兩個框的 IoU (Intersection over Union)。"""
        x1 = max(self.x, other.x)
        y1 = max(self.y, other.y)
        x2 = min(self.x + self.width, other.x + other.width)
        y2 = min(self.y + self.height, other.y + other.height)

        if x2 <= x1 or y2 <= y1:
            return 0.0

        intersection = (x2 - x1) * (y2 - y1)
        union = self.area + other.area - intersection
        if union == 0:
            return 0.0
        return intersection / union


@dataclass
class Entity:
    """一個偵測到的物件實體。

    Attributes
    ----------
    entity_id : int
        唯一識別碼。
    label : str
        類別標籤（如 "person", "car"）。
    confidence : float
        偵測信心度 (0.0 ~ 1.0)。
    bbox : BoundingBox
        邊界框。
    metadata : dict
        額外資訊（追蹤 ID、速度等）。
    """
    entity_id: int
    label: str
    confidence: float
    bbox: BoundingBox
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """建立後驗證。"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"confidence 必須在 0.0 到 1.0 之間，收到: {self.confidence}"
            )

    def to_dict(self) -> dict:
        """轉成字典，方便 JSON 序列化。"""
        return {
            "entity_id": self.entity_id,
            "label": self.label,
            "confidence": round(self.confidence, 4),
            "bbox": {
                "x": self.bbox.x,
                "y": self.bbox.y,
                "width": self.bbox.width,
                "height": self.bbox.height,
            },
            "metadata": self.metadata,
        }


@dataclass
class FrameResult:
    """單幀的處理結果。"""
    frame_id: int
    entities: list[Entity] = field(default_factory=list)
    processing_time_ms: float = 0.0

    @property
    def count(self) -> int:
        """偵測到的物件數量。"""
        return len(self.entities)

    def filter_by_label(self, label: str) -> list[Entity]:
        """篩選特定類別的物件。"""
        return [e for e in self.entities if e.label == label]

    def filter_by_confidence(self, threshold: float) -> list[Entity]:
        """篩選信心度高於門檻的物件。"""
        return [e for e in self.entities if e.confidence >= threshold]
```

### mini_vision/mini_vision/detector.py

```python
# mini_vision/mini_vision/detector.py
"""邏輯層：偵測演算法。

只依賴 core.py。不處理 I/O、不讀設定檔、不做 logging。
純粹接收資料、執行演算法、回傳結果。
"""

import math
from mini_vision.core import BoundingBox, Entity, FrameResult


class Detector:
    """物件偵測器。

    在真實專案中這裡會包裝 YOLO / SSD 等模型。
    這個教學版使用簡化的輪廓偵測邏輯。

    Parameters
    ----------
    confidence_threshold : float
        信心度門檻，低於此值的偵測結果會被丟棄。
    min_area : int
        最小物件面積（像素），太小的會被忽略。
    max_detections : int
        單幀最多回傳幾個偵測結果。
    """

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        min_area: int = 500,
        max_detections: int = 100,
    ):
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError(
                f"confidence_threshold 必須在 0~1 之間，收到: {confidence_threshold}"
            )
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.max_detections = max_detections
        self._next_id = 0

    def _generate_id(self) -> int:
        """產生遞增的唯一 ID。"""
        current = self._next_id
        self._next_id += 1
        return current

    def _estimate_confidence(self, area: int, frame_area: int) -> float:
        """根據物件面積佔比估算信心度（簡化版）。"""
        if frame_area == 0:
            return 0.0
        ratio = area / frame_area
        # 使用 sigmoid 函式模擬信心度曲線
        score = 1.0 / (1.0 + math.exp(-10 * (ratio - 0.05)))
        return round(min(1.0, max(0.0, score)), 4)

    def detect_from_regions(
        self,
        regions: list[tuple[int, int, int, int]],
        frame_width: int,
        frame_height: int,
        frame_id: int = 0,
    ) -> FrameResult:
        """
        從候選區域列表產生偵測結果。

        Parameters
        ----------
        regions : list[tuple[int, int, int, int]]
            候選區域列表，每個元素為 (x, y, width, height)。
        frame_width : int
            影像寬度。
        frame_height : int
            影像高度。
        frame_id : int
            幀序號。

        Returns
        -------
        FrameResult
            包含所有通過門檻的偵測結果。
        """
        frame_area = frame_width * frame_height
        entities = []

        for x, y, w, h in regions:
            area = w * h
            if area < self.min_area:
                continue

            confidence = self._estimate_confidence(area, frame_area)
            if confidence < self.confidence_threshold:
                continue

            bbox = BoundingBox(x=x, y=y, width=w, height=h)
            entity = Entity(
                entity_id=self._generate_id(),
                label="object",
                confidence=confidence,
                bbox=bbox,
            )
            entities.append(entity)

        # 依信心度排序，取前 N 個
        entities.sort(key=lambda e: e.confidence, reverse=True)
        entities = entities[:self.max_detections]

        return FrameResult(frame_id=frame_id, entities=entities)

    def detect_from_pixel_data(
        self,
        pixel_data: list[list[int]],
        frame_id: int = 0,
    ) -> FrameResult:
        """
        從像素資料偵測物件（簡化版：找非零區塊）。

        Parameters
        ----------
        pixel_data : list[list[int]]
            二維灰階像素陣列 (height x width)，值為 0~255。
        frame_id : int
            幀序號。

        Returns
        -------
        FrameResult
            偵測結果。
        """
        if not pixel_data or not pixel_data[0]:
            return FrameResult(frame_id=frame_id)

        height = len(pixel_data)
        width = len(pixel_data[0])
        threshold = 128

        # 簡化版連通元件偵測：掃描非零區塊的邊界框
        visited = [[False] * width for _ in range(height)]
        regions = []

        for row in range(height):
            for col in range(width):
                if pixel_data[row][col] >= threshold and not visited[row][col]:
                    # BFS 找連通區塊
                    min_r, max_r = row, row
                    min_c, max_c = col, col
                    queue = [(row, col)]
                    visited[row][col] = True

                    while queue:
                        r, c = queue.pop(0)
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < height and 0 <= nc < width
                                    and not visited[nr][nc]
                                    and pixel_data[nr][nc] >= threshold):
                                visited[nr][nc] = True
                                queue.append((nr, nc))
                                min_r = min(min_r, nr)
                                max_r = max(max_r, nr)
                                min_c = min(min_c, nc)
                                max_c = max(max_c, nc)

                    box_w = max_c - min_c + 1
                    box_h = max_r - min_r + 1
                    regions.append((min_c, min_r, box_w, box_h))

        return self.detect_from_regions(regions, width, height, frame_id)

    def reset(self) -> None:
        """重設偵測器狀態（ID 計數器歸零）。"""
        self._next_id = 0
```

### mini_vision/mini_vision/pipeline.py

```python
# mini_vision/mini_vision/pipeline.py
"""協調層：串接讀取、偵測、輸出的完整流程。

這一層負責：
1. 讀取設定
2. 初始化各元件
3. 控制資料流
4. 錯誤處理與日誌
5. 輸出結果
"""

import json
import logging
import time
from pathlib import Path
from mini_vision.core import Entity, FrameResult
from mini_vision.detector import Detector

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """設定相關錯誤。"""
    pass


class Pipeline:
    """MiniVision 主管線。

    Parameters
    ----------
    config_path : str
        JSON 設定檔路徑。
    """

    # 預設設定
    DEFAULT_CONFIG = {
        "detector": {
            "confidence_threshold": 0.5,
            "min_area": 500,
            "max_detections": 100,
        },
        "output": {
            "directory": "./output",
            "save_json": True,
        },
        "processing": {
            "max_frames": 0,
            "log_interval": 10,
        },
    }

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.detector = self._build_detector()
        self.results: list[FrameResult] = []
        logger.info("Pipeline 初始化完成")

    def _load_config(self, config_path: str = None) -> dict:
        """載入設定檔並與預設值合併。"""
        if config_path is None:
            logger.info("未指定設定檔，使用預設值")
            return self.DEFAULT_CONFIG.copy()

        path = Path(config_path)
        if not path.exists():
            raise ConfigError(f"設定檔不存在: {config_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"設定檔 JSON 格式錯誤: {e}")

        # 深層合併
        merged = self.DEFAULT_CONFIG.copy()
        for section, values in user_config.items():
            if section in merged and isinstance(values, dict):
                merged[section] = {**merged[section], **values}
            else:
                merged[section] = values

        logger.info("設定檔已載入: %s", config_path)
        return merged

    def _build_detector(self) -> Detector:
        """根據設定建立偵測器。"""
        det_config = self.config.get("detector", {})
        return Detector(
            confidence_threshold=det_config.get("confidence_threshold", 0.5),
            min_area=det_config.get("min_area", 500),
            max_detections=det_config.get("max_detections", 100),
        )

    def process_frame(
        self,
        regions: list[tuple[int, int, int, int]],
        frame_width: int,
        frame_height: int,
    ) -> FrameResult:
        """
        處理單幀資料。

        Parameters
        ----------
        regions : list[tuple[int, int, int, int]]
            候選區域列表。
        frame_width : int
            影像寬度。
        frame_height : int
            影像高度。

        Returns
        -------
        FrameResult
            該幀的偵測結果。
        """
        frame_id = len(self.results)
        start_time = time.perf_counter()

        result = self.detector.detect_from_regions(
            regions, frame_width, frame_height, frame_id
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        result.processing_time_ms = round(elapsed_ms, 2)

        self.results.append(result)

        log_interval = self.config["processing"].get("log_interval", 10)
        if frame_id % log_interval == 0:
            logger.info(
                "幀 %d: 偵測到 %d 個物件 (%.1f ms)",
                frame_id, result.count, result.processing_time_ms,
            )

        return result

    def process_batch(
        self,
        frames_data: list[dict],
    ) -> list[FrameResult]:
        """
        批次處理多幀。

        Parameters
        ----------
        frames_data : list[dict]
            每個 dict 包含 "regions", "width", "height"。

        Returns
        -------
        list[FrameResult]
            所有幀的偵測結果。
        """
        max_frames = self.config["processing"].get("max_frames", 0)
        batch_results = []

        for i, frame in enumerate(frames_data):
            if max_frames > 0 and i >= max_frames:
                logger.info("達到最大幀數限制 (%d)，停止處理", max_frames)
                break

            try:
                result = self.process_frame(
                    regions=frame["regions"],
                    frame_width=frame["width"],
                    frame_height=frame["height"],
                )
                batch_results.append(result)
            except Exception as e:
                logger.error("幀 %d 處理失敗: %s", i, e)
                # 插入空結果，保持幀序號連續
                empty_result = FrameResult(frame_id=len(self.results))
                self.results.append(empty_result)
                batch_results.append(empty_result)

        return batch_results

    def save_results(self, output_path: str = None) -> str:
        """
        將所有結果存成 JSON。

        Returns
        -------
        str
            輸出檔案的路徑。
        """
        if output_path is None:
            out_dir = self.config["output"].get("directory", "./output")
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            output_path = str(Path(out_dir) / "results.json")

        data = {
            "total_frames": len(self.results),
            "total_entities": sum(r.count for r in self.results),
            "frames": [
                {
                    "frame_id": r.frame_id,
                    "entity_count": r.count,
                    "processing_time_ms": r.processing_time_ms,
                    "entities": [e.to_dict() for e in r.entities],
                }
                for r in self.results
            ],
        }

        Path(output_path).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info("結果已儲存至: %s", output_path)
        return output_path

    def get_summary(self) -> dict:
        """取得處理摘要。"""
        total_entities = sum(r.count for r in self.results)
        total_time = sum(r.processing_time_ms for r in self.results)
        avg_time = total_time / len(self.results) if self.results else 0

        return {
            "total_frames": len(self.results),
            "total_entities": total_entities,
            "total_time_ms": round(total_time, 2),
            "avg_time_per_frame_ms": round(avg_time, 2),
        }

    def reset(self) -> None:
        """重設管線狀態。"""
        self.results.clear()
        self.detector.reset()
        logger.info("Pipeline 已重設")
```

### mini_vision/tests/\_\_init\_\_.py

```python
# mini_vision/tests/__init__.py
# 空檔案 — 讓 Python 認得 tests 是套件
```

### mini_vision/tests/test_pipeline.py

```python
# mini_vision/tests/test_pipeline.py
"""MiniVision 完整測試套件。"""

import json
import pytest
from mini_vision.core import BoundingBox, Entity, FrameResult
from mini_vision.detector import Detector
from mini_vision.pipeline import Pipeline, ConfigError


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def default_detector():
    """預設偵測器。"""
    return Detector(confidence_threshold=0.3, min_area=100, max_detections=50)


@pytest.fixture
def sample_regions():
    """模擬候選區域：三個不同大小的方塊。"""
    return [
        (10, 10, 200, 200),   # 大物件
        (300, 300, 50, 50),   # 中物件
        (500, 500, 5, 5),     # 太小，會被過濾
    ]


@pytest.fixture
def config_file(tmp_path):
    """在臨時目錄建立測試設定檔。"""
    config = {
        "detector": {
            "confidence_threshold": 0.3,
            "min_area": 100,
            "max_detections": 50,
        },
        "output": {
            "directory": str(tmp_path / "output"),
            "save_json": True,
        },
        "processing": {
            "max_frames": 5,
            "log_interval": 1,
        },
    }
    config_path = tmp_path / "test_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return str(config_path)


@pytest.fixture
def pipeline_with_config(config_file):
    """使用測試設定檔的 Pipeline。"""
    return Pipeline(config_path=config_file)


# ============================================================
# 資料層測試 (core.py)
# ============================================================

class TestBoundingBox:
    """BoundingBox 相關測試。"""

    def test_area(self):
        bbox = BoundingBox(x=0, y=0, width=100, height=50)
        assert bbox.area == 5000

    def test_center(self):
        bbox = BoundingBox(x=10, y=20, width=100, height=60)
        cx, cy = bbox.center
        assert cx == 60.0
        assert cy == 50.0

    def test_to_xyxy(self):
        bbox = BoundingBox(x=10, y=20, width=30, height=40)
        assert bbox.to_xyxy() == (10, 20, 40, 60)

    def test_iou_no_overlap(self):
        a = BoundingBox(x=0, y=0, width=10, height=10)
        b = BoundingBox(x=100, y=100, width=10, height=10)
        assert a.iou(b) == 0.0

    def test_iou_perfect_overlap(self):
        a = BoundingBox(x=0, y=0, width=10, height=10)
        b = BoundingBox(x=0, y=0, width=10, height=10)
        assert a.iou(b) == 1.0

    def test_iou_partial_overlap(self):
        a = BoundingBox(x=0, y=0, width=10, height=10)
        b = BoundingBox(x=5, y=5, width=10, height=10)
        iou = a.iou(b)
        assert 0.0 < iou < 1.0
        # 交集 = 5*5 = 25, 聯集 = 100+100-25 = 175
        assert abs(iou - 25 / 175) < 0.001


class TestEntity:
    """Entity 相關測試。"""

    def test_valid_entity(self):
        bbox = BoundingBox(x=0, y=0, width=50, height=50)
        entity = Entity(entity_id=1, label="person", confidence=0.95, bbox=bbox)
        assert entity.label == "person"
        assert entity.confidence == 0.95

    def test_invalid_confidence(self):
        bbox = BoundingBox(x=0, y=0, width=50, height=50)
        with pytest.raises(ValueError, match="confidence"):
            Entity(entity_id=1, label="test", confidence=1.5, bbox=bbox)

    def test_to_dict(self):
        bbox = BoundingBox(x=10, y=20, width=30, height=40)
        entity = Entity(entity_id=7, label="car", confidence=0.88, bbox=bbox)
        d = entity.to_dict()
        assert d["entity_id"] == 7
        assert d["label"] == "car"
        assert d["bbox"]["width"] == 30


class TestFrameResult:
    """FrameResult 相關測試。"""

    def test_filter_by_label(self):
        bbox = BoundingBox(x=0, y=0, width=50, height=50)
        entities = [
            Entity(1, "person", 0.9, bbox),
            Entity(2, "car", 0.8, bbox),
            Entity(3, "person", 0.7, bbox),
        ]
        result = FrameResult(frame_id=0, entities=entities)
        persons = result.filter_by_label("person")
        assert len(persons) == 2

    def test_filter_by_confidence(self):
        bbox = BoundingBox(x=0, y=0, width=50, height=50)
        entities = [
            Entity(1, "a", 0.9, bbox),
            Entity(2, "b", 0.5, bbox),
            Entity(3, "c", 0.3, bbox),
        ]
        result = FrameResult(frame_id=0, entities=entities)
        high_conf = result.filter_by_confidence(0.6)
        assert len(high_conf) == 1
        assert high_conf[0].entity_id == 1


# ============================================================
# 邏輯層測試 (detector.py)
# ============================================================

class TestDetector:
    """Detector 相關測試。"""

    def test_invalid_threshold(self):
        with pytest.raises(ValueError):
            Detector(confidence_threshold=2.0)

    def test_filter_small_regions(self, default_detector, sample_regions):
        result = default_detector.detect_from_regions(
            sample_regions, frame_width=640, frame_height=480
        )
        # (5, 5) 的物件面積 = 25 < min_area(100)，應被過濾
        for entity in result.entities:
            assert entity.bbox.area >= 100

    def test_max_detections_limit(self):
        detector = Detector(confidence_threshold=0.0, min_area=1, max_detections=2)
        regions = [(i * 10, 0, 50, 50) for i in range(10)]
        result = detector.detect_from_regions(regions, 640, 480)
        assert len(result.entities) <= 2

    def test_reset(self, default_detector, sample_regions):
        default_detector.detect_from_regions(sample_regions, 640, 480)
        old_id = default_detector._next_id
        assert old_id > 0

        default_detector.reset()
        assert default_detector._next_id == 0

    def test_detect_from_pixel_data(self):
        detector = Detector(confidence_threshold=0.0, min_area=1, max_detections=100)
        # 建立一個 20x20 的測試影像，左上角有一塊亮區
        pixel_data = [[0] * 20 for _ in range(20)]
        for r in range(5, 10):
            for c in range(5, 10):
                pixel_data[r][c] = 200
        result = detector.detect_from_pixel_data(pixel_data, frame_id=0)
        assert result.count >= 1


# ============================================================
# 協調層測試 (pipeline.py)
# ============================================================

class TestPipeline:
    """Pipeline 相關測試。"""

    def test_default_config(self):
        pipeline = Pipeline()
        assert "detector" in pipeline.config
        assert "output" in pipeline.config

    def test_load_custom_config(self, config_file):
        pipeline = Pipeline(config_path=config_file)
        assert pipeline.config["detector"]["confidence_threshold"] == 0.3

    def test_invalid_config_path(self):
        with pytest.raises(ConfigError, match="不存在"):
            Pipeline(config_path="/nonexistent/config.json")

    def test_invalid_json(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ invalid json }", encoding="utf-8")
        with pytest.raises(ConfigError, match="JSON"):
            Pipeline(config_path=str(bad_file))

    def test_process_single_frame(self, pipeline_with_config, sample_regions):
        result = pipeline_with_config.process_frame(
            regions=sample_regions,
            frame_width=640,
            frame_height=480,
        )
        assert isinstance(result, FrameResult)
        assert result.frame_id == 0
        assert result.processing_time_ms >= 0

    def test_process_batch(self, pipeline_with_config):
        frames = [
            {"regions": [(10, 10, 100, 100)], "width": 640, "height": 480},
            {"regions": [(20, 20, 150, 150)], "width": 640, "height": 480},
            {"regions": [], "width": 640, "height": 480},
        ]
        results = pipeline_with_config.process_batch(frames)
        assert len(results) == 3

    def test_max_frames_limit(self, pipeline_with_config):
        frames = [
            {"regions": [(10, 10, 100, 100)], "width": 640, "height": 480}
            for _ in range(20)
        ]
        results = pipeline_with_config.process_batch(frames)
        # 設定檔限制 max_frames = 5
        assert len(results) == 5

    def test_save_results(self, pipeline_with_config, sample_regions, tmp_path):
        pipeline_with_config.process_frame(sample_regions, 640, 480)
        output_path = str(tmp_path / "test_results.json")
        saved_path = pipeline_with_config.save_results(output_path)

        assert saved_path == output_path
        with open(saved_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["total_frames"] == 1
        assert "frames" in data

    def test_get_summary(self, pipeline_with_config, sample_regions):
        for _ in range(3):
            pipeline_with_config.process_frame(sample_regions, 640, 480)
        summary = pipeline_with_config.get_summary()
        assert summary["total_frames"] == 3
        assert summary["total_time_ms"] >= 0

    def test_reset(self, pipeline_with_config, sample_regions):
        pipeline_with_config.process_frame(sample_regions, 640, 480)
        assert len(pipeline_with_config.results) == 1

        pipeline_with_config.reset()
        assert len(pipeline_with_config.results) == 0
```

### mini_vision/configs/default.json

```json
{
    "detector": {
        "confidence_threshold": 0.5,
        "min_area": 500,
        "max_detections": 100
    },
    "output": {
        "directory": "./output",
        "save_json": true
    },
    "processing": {
        "max_frames": 0,
        "log_interval": 10
    }
}
```

### mini_vision/run.py

```python
#!/usr/bin/env python3
# mini_vision/run.py
"""MiniVision CLI 入口點。

用法:
    python run.py
    python run.py --config configs/custom.json
    python run.py --confidence 0.7 --verbose
"""

import argparse
import logging
import sys
import json
from mini_vision.pipeline import Pipeline, ConfigError


def setup_logging(verbose: bool = False) -> None:
    """設定日誌系統。"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args(argv: list[str] = None) -> argparse.Namespace:
    """解析命令列參數。"""
    parser = argparse.ArgumentParser(
        description="MiniVision — 輕量影像偵測框架",
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="configs/default.json",
        help="設定檔路徑 (預設: configs/default.json)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=None,
        help="覆蓋設定檔中的信心度門檻",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="顯示詳細日誌",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="執行內建示範（不需要影像來源）",
    )
    return parser.parse_args(argv)


def run_demo(pipeline: Pipeline) -> None:
    """執行內建示範：用假資料跑一遍完整流程。"""
    logger = logging.getLogger(__name__)
    logger.info("=== MiniVision Demo 開始 ===")

    # 模擬 5 幀的資料
    demo_frames = [
        {
            "regions": [(50, 50, 200, 200), (300, 100, 80, 80)],
            "width": 640,
            "height": 480,
        },
        {
            "regions": [(55, 48, 198, 205), (305, 102, 82, 78)],
            "width": 640,
            "height": 480,
        },
        {
            "regions": [(60, 45, 195, 210)],
            "width": 640,
            "height": 480,
        },
        {
            "regions": [],
            "width": 640,
            "height": 480,
        },
        {
            "regions": [(100, 100, 300, 300), (10, 10, 50, 50), (400, 400, 150, 150)],
            "width": 640,
            "height": 480,
        },
    ]

    results = pipeline.process_batch(demo_frames)

    for r in results:
        logger.info(
            "  幀 %d: %d 個物件 (%.1f ms)",
            r.frame_id, r.count, r.processing_time_ms,
        )

    summary = pipeline.get_summary()
    logger.info("=== 處理摘要 ===")
    logger.info("  總幀數: %d", summary["total_frames"])
    logger.info("  總物件數: %d", summary["total_entities"])
    logger.info("  總耗時: %.1f ms", summary["total_time_ms"])
    logger.info("  平均每幀: %.1f ms", summary["avg_time_per_frame_ms"])

    output_path = pipeline.save_results()
    logger.info("結果已儲存至: %s", output_path)
    logger.info("=== Demo 結束 ===")


def main(argv: list[str] = None) -> int:
    """主函式。回傳 exit code (0=成功, 1=錯誤)。"""
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)

    try:
        pipeline = Pipeline(config_path=args.config)

        # CLI 參數覆蓋
        if args.confidence is not None:
            pipeline.config["detector"]["confidence_threshold"] = args.confidence
            pipeline.detector.confidence_threshold = args.confidence
            logger.info("信心度門檻已覆蓋為: %.2f", args.confidence)

        if args.demo:
            run_demo(pipeline)
        else:
            logger.info("MiniVision 已就緒。使用 --demo 執行示範。")

    except ConfigError as e:
        logger.error("設定錯誤: %s", e)
        return 1
    except KeyboardInterrupt:
        logger.info("使用者中斷")
        return 0
    except Exception as e:
        logger.exception("非預期的錯誤: %s", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### mini_vision/requirements.txt

```
# requirements.txt
# MiniVision 核心依賴（本教學版無外部依賴，純 Python 標準庫即可執行）

# 如果要擴展成真實專案，取消下方註解：
# numpy>=1.24
# opencv-python>=4.8
# Pillow>=10.0
# torch>=2.1

# 開發工具
pytest>=8.0
```

### 執行方式

```bash
# 1. 進入專案目錄
cd mini_vision

# 2. 建立虛擬環境
python -m venv .venv
source .venv/bin/activate

# 3. 安裝（可編輯模式）
pip install -e .

# 4. 跑測試
pytest tests/ -v

# 5. 執行示範
python run.py --demo --verbose
```

---

## 9. 常見反模式（Anti-patterns）

### 9-1 循環引用（Circular Import）

**症狀**：`ImportError: cannot import name 'X' from partially initialized module`

**錯誤範例**：

```python
# ---- 檔案 a.py ----
from b import B  # a 載入 b

class A:
    def method(self):
        return B()


# ---- 檔案 b.py ----
from a import A  # b 載入 a → 但 a 還沒載入完！

class B:
    def method(self):
        return A()
```

Python 執行 `a.py` 時：
1. 開始載入 a.py
2. 遇到 `from b import B` → 跳去載入 b.py
3. b.py 遇到 `from a import A` → 但 a.py 還沒載入完，`A` 還不存在
4. 爆炸

**解法一：延遲引入（Lazy Import）**

```python
# ---- 修正後的 b.py ----

class B:
    def method(self):
        from a import A  # 在函式內引入，此時 a.py 已經載入完畢
        return A()
```

**解法二：抽出共用模組**

```python
# ---- common.py（新檔案）----

class Base:
    pass


# ---- a.py ----
from common import Base

class A(Base):
    def method(self):
        from b import B
        return B()


# ---- b.py ----
from common import Base

class B(Base):
    def method(self):
        from a import A
        return A()
```

**解法三：TYPE_CHECKING（僅用於型別提示）**

```python
# ---- b.py ----
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 這個區塊只在型別檢查工具（mypy）執行時才會生效
    # 實際跑程式時不會執行，所以不會循環引入
    from a import A


class B:
    def method(self) -> "A":
        from a import A  # 實際使用時才引入
        return A()
```

**VisionDSL 的作法**：嚴格遵守分層，`core.py` 絕不引入其他專案模組，依賴方向單一（上層 → 下層），自然不會有循環引用。

### 9-2 上帝類別 / 上帝檔案（God Class / God File）

**症狀**：一個類別或檔案超過 1000 行，什麼都做。

**錯誤範例**：

```python
# god_class.py — 千萬別這樣寫
class VisionSystem:
    """什麼都做的上帝類別。"""

    def __init__(self):
        self.model = None
        self.tracker = None
        self.config = {}
        self.results = []
        self.logger = None
        self.db_connection = None
        self.web_server = None

    def load_model(self): pass
    def detect_objects(self): pass
    def track_objects(self): pass
    def draw_boxes(self): pass
    def save_video(self): pass
    def load_config(self): pass
    def save_config(self): pass
    def start_web_server(self): pass
    def handle_api_request(self): pass
    def connect_database(self): pass
    def save_to_database(self): pass
    def send_notification(self): pass
    def generate_report(self): pass
    # ... 繼續無限膨脹 ...
```

**解法：按職責拆分**

```python
# detector.py
class Detector:
    """只負責偵測。"""
    def load_model(self): pass
    def detect(self, frame): pass


# tracker.py
class Tracker:
    """只負責追蹤。"""
    def update(self, detections): pass
    def get_tracks(self): pass


# storage.py
class ResultStorage:
    """只負責儲存。"""
    def save(self, results): pass
    def load(self, path): pass


# pipeline.py
class Pipeline:
    """協調各元件，自己不實作邏輯。"""
    def __init__(self, detector, tracker, storage):
        self.detector = detector
        self.tracker = tracker
        self.storage = storage

    def run(self, frame):
        dets = self.detector.detect(frame)
        tracks = self.tracker.update(dets)
        self.storage.save(tracks)
        return tracks
```

**經驗法則**：

| 指標 | 警戒值 |
|------|--------|
| 檔案行數 | > 500 行就該考慮拆分 |
| 類別方法數 | > 10 個就該檢視職責 |
| `__init__` 參數數 | > 5 個就該用設定物件 |
| import 行數 | > 15 行就代表職責太雜 |

### 9-3 全域狀態（Global State）

**症狀**：模組層級的可變變數，任何人都能改。

**錯誤範例**：

```python
# globals_bad.py — 危險的全域狀態

# 全域可變狀態
current_user = None
detection_count = 0
all_results = []
is_running = False


def start_detection():
    global is_running, detection_count
    is_running = True
    detection_count = 0


def add_result(result):
    global detection_count
    all_results.append(result)
    detection_count += 1


def stop_detection():
    global is_running
    is_running = False
```

**問題**：

1. **不可預測**：任何模組都能改 `current_user`，你不知道誰改了它
2. **無法測試**：測試之間狀態會互相污染
3. **無法併行**：多執行緒同時改 `detection_count` 會出錯

**解法：用類別封裝狀態**

```python
# globals_fixed.py — 用類別管理狀態

class DetectionSession:
    """封裝偵測階段的狀態。每次偵測建立新的 session。"""

    def __init__(self, user: str):
        self.user = user
        self.detection_count = 0
        self.results = []
        self.is_running = False

    def start(self) -> None:
        self.is_running = True
        self.detection_count = 0
        self.results.clear()

    def add_result(self, result: dict) -> None:
        if not self.is_running:
            raise RuntimeError("偵測尚未開始，請先呼叫 start()")
        self.results.append(result)
        self.detection_count += 1

    def stop(self) -> dict:
        self.is_running = False
        return {
            "user": self.user,
            "total": self.detection_count,
            "results": self.results.copy(),
        }


# 使用方式：
session_a = DetectionSession(user="Alice")
session_b = DetectionSession(user="Bob")
# 兩個 session 完全獨立，不會互相干擾
```

**允許的「全域」**：

```python
# 這些是安全的全域定義
import logging

# 常數（不可變）— OK
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0
SUPPORTED_FORMATS = frozenset({"jpg", "png", "bmp"})

# Logger — OK（logging 模組本身是執行緒安全的）
logger = logging.getLogger(__name__)

# 型別別名 — OK
BBoxType = tuple[int, int, int, int]
```

### 9-4 反模式檢查清單

拿這張表對照你的專案，看看有沒有中招：

| 反模式 | 症狀 | 解法 |
|--------|------|------|
| 循環引用 | ImportError | 分層 + 延遲引入 |
| 上帝檔案 | 單檔 > 500 行 | 按職責拆分 |
| 全域可變狀態 | `global` 關鍵字 | 用類別封裝 |
| 硬編碼路徑 | `"/home/user/data"` | 用設定檔或參數傳入 |
| 裸 except | `except:` 不寫型別 | 明確捕捉特定例外 |
| print 除錯 | 到處 `print(x)` | 用 `logging` 模組 |
| import * | `from module import *` | 明確列出要引入的名稱 |
| 深層巢狀 | 5 層以上的 if/for | 提早 return、抽函式 |

---

## 總結：從 Colab 到生產級的完整路徑

```
Level 0: Colab 單一腳本
         ↓  拆檔案
Level 1: 多個 .py 檔案
         ↓  加 __init__.py
Level 2: Python 套件
         ↓  分層架構
Level 3: core / logic / pipeline / run
         ↓  設定管理
Level 4: JSON config + argparse + 環境變數
         ↓  錯誤處理
Level 5: 自訂例外 + logging
         ↓  依賴管理
Level 6: pyproject.toml + venv + editable install
         ↓  測試
Level 7: pytest + fixture + mock + CI
         ↓
    🏁 生產級 Python 專案
```

**VisionDSL 就是 Level 7 的實例**：

```
VisionDSL/
├── dsl/                    # Level 2: 套件
│   ├── __init__.py         # Level 2: 公開 API
│   ├── core.py             # Level 3: 資料層
│   ├── logic.py            # Level 3: 邏輯層（1,220 行）
│   ├── tracker.py          # Level 3: 邏輯層（942 行）
│   ├── pipeline.py         # Level 3: 協調層
│   ├── kalman.py           # Level 3: 邏輯層
│   ├── bodyparts.py        # Level 3: 邏輯層
│   ├── contacts.py         # Level 3: 邏輯層
│   ├── geometry.py         # Level 3: 邏輯層
│   └── matching.py         # Level 3: 邏輯層
├── backends/               # Level 2: 子套件（懶載入）
├── config_ui/              # Level 4: 設定 UI
├── configs/                # Level 4: 設定檔
├── inference.py            # Level 3: 推論包裝
├── run.py                  # Level 3: CLI 入口
├── requirements.txt        # Level 6: 依賴管理
└── tests/                  # Level 7: 測試
```

你不需要一步到位。從 Level 0 開始，每次多做一步，專案自然會成長到正確的形狀。

> **下一集預告**：EP03 將深入 Python 的型別系統——`dataclass`、`TypedDict`、`Protocol`，以及如何用 `mypy` 在執行前就抓到型別錯誤。
