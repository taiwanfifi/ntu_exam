# EP01 — Python 從入門到專案級別

> **系列定位**：你已經會在 Colab 上跑程式、知道 function / import / 基本繼承，
> 但想寫出「NVIDIA 等級」的 production code。本篇把 Python 核心語法拉到專案水準。

---

## 目錄

1. [變數與型別](#1-變數與型別-variables--types)
2. [函式進階](#2-函式進階-advanced-functions)
3. [類別完整攻略](#3-類別完整攻略-classes-complete-guide)
4. [dataclass 完整教學](#4-dataclass-完整教學)
5. [Type Hints 型別提示](#5-type-hints-型別提示)
6. [`__slots__` 記憶體優化](#6-__slots__-記憶體優化)
7. [生成器與迭代器](#7-生成器與迭代器-generator--iterator)
8. [上下文管理器](#8-上下文管理器-context-manager)
9. [例外處理](#9-例外處理-exception-handling)
10. [模組與套件](#10-模組與套件-modules--packages)
11. [設計模式實踐](#11-設計模式實踐)

---

## 1. 變數與型別 (Variables & Types)

Python 是**動態型別**語言：變數本身不帶型別，值才帶型別。

### 1.1 八大基本型別一覽

```python
# === 數值型別 ===
整數 = 42                     # int — 任意精度整數
浮點數 = 3.14                 # float — 64-bit 雙精度
布林值 = True                 # bool — 其實是 int 的子類別

# === 文字型別 ===
文字 = "你好世界"              # str — 不可變的 Unicode 序列

# === 容器型別 ===
串列 = [1, 2, 3]              # list — 可變、有序
元組 = (1, 2, 3)              # tuple — 不可變、有序
集合 = {1, 2, 3}              # set — 可變、無序、不重複
字典 = {"a": 1, "b": 2}      # dict — 可變、鍵值對

# 印出每個變數的型別
所有變數 = [整數, 浮點數, 布林值, 文字, 串列, 元組, 集合, 字典]
for 變數 in 所有變數:
    print(f"值={變數!r:20s}  型別={type(變數).__name__}")
```

輸出：
```
值=42                    型別=int
值=3.14                  型別=float
值=True                  型別=bool
值='你好世界'             型別=str
值=[1, 2, 3]             型別=list
值=(1, 2, 3)             型別=tuple
值={1, 2, 3}             型別=set
值={'a': 1, 'b': 2}      型別=dict
```

### 1.2 type() vs isinstance()

```python
# --- type() 做「精確」比較 ---
print(type(42) == int)        # True
print(type(True) == int)      # True  ← 注意！bool 是 int 子類別
print(type(True) == bool)     # True

# --- isinstance() 做「含繼承」比較（推薦用法）---
print(isinstance(True, int))  # True  ← bool 繼承自 int
print(isinstance(True, bool)) # True
print(isinstance(42, bool))   # False ← int 不是 bool

# 實務建議：判斷型別時優先用 isinstance()
def 安全除法(a, b):
    """
    輸入：a, b — 任意值
    處理：檢查型別後執行除法
    輸出：浮點數結果 或 拋出 TypeError
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError(f"需要數值，收到 {type(a).__name__} 和 {type(b).__name__}")
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b

print(安全除法(10, 3))   # 3.3333...
print(安全除法(10.5, 2)) # 5.25
```

### 1.3 型別轉換

```python
# --- 明確轉換 ---
數字字串 = "123"
轉成整數 = int(數字字串)        # 123
轉成浮點 = float(數字字串)      # 123.0
轉回字串 = str(轉成整數)        # "123"

# --- 容器之間互轉 ---
原始列表 = [1, 2, 2, 3, 3, 3]
轉成集合 = set(原始列表)        # {1, 2, 3} — 去重
轉成元組 = tuple(原始列表)      # (1, 2, 2, 3, 3, 3)
排序後列表 = sorted(轉成集合)   # [1, 2, 3] — sorted 回傳 list

# --- 字典相關轉換 ---
鍵值對列表 = [("x", 1), ("y", 2), ("z", 3)]
轉成字典 = dict(鍵值對列表)     # {'x': 1, 'y': 2, 'z': 3}
取出鍵 = list(轉成字典.keys())  # ['x', 'y', 'z']
取出值 = list(轉成字典.values())# [1, 2, 3]

print(f"集合: {轉成集合}")
print(f"字典: {轉成字典}")
print(f"鍵:   {取出鍵}")
```

---

## 2. 函式進階 (Advanced Functions)

### 2.1 *args 與 **kwargs

```python
def 彈性函式(*args, **kwargs):
    """
    輸入：任意數量的位置參數與關鍵字參數
    處理：分別印出 args (tuple) 和 kwargs (dict)
    輸出：無（純列印）
    """
    print(f"位置參數 args   = {args}")
    print(f"關鍵字參數 kwargs = {kwargs}")

# 呼叫範例
彈性函式(1, 2, 3, name="Alice", age=30)
# 位置參數 args   = (1, 2, 3)
# 關鍵字參數 kwargs = {'name': 'Alice', 'age': 30}
```

```python
def 建立設定檔(專案名稱, *額外標籤, **覆蓋設定):
    """
    輸入：專案名稱(str), 額外標籤(*args), 覆蓋設定(**kwargs)
    處理：合併成一個設定字典
    輸出：dict — 完整的設定檔
    """
    設定 = {
        "project": 專案名稱,
        "tags": list(額外標籤),
        "debug": False,
        "version": "1.0.0",
    }
    設定.update(覆蓋設定)  # kwargs 覆蓋預設值
    return 設定

結果 = 建立設定檔("VisionDSL", "cv", "edge", debug=True, version="2.1.0")
print(結果)
# {'project': 'VisionDSL', 'tags': ['cv', 'edge'], 'debug': True, 'version': '2.1.0'}
```

```python
# --- 拆解（unpack）傳入 ---
def 加總三數(a, b, c):
    """
    輸入：a, b, c — 三個數值
    處理：相加
    輸出：int — 總和
    """
    return a + b + c

數列 = [10, 20, 30]
print(加總三數(*數列))   # 60  ← 用 * 拆解 list

參數字典 = {"a": 100, "b": 200, "c": 300}
print(加總三數(**參數字典)) # 600  ← 用 ** 拆解 dict
```

### 2.2 lambda, map, filter, reduce

```python
# --- lambda：匿名函式 ---
平方 = lambda x: x ** 2
print(平方(5))  # 25

# --- map：對每個元素套用函式 ---
# 輸入：函式 + 可迭代物件
# 處理：逐一套用函式
# 輸出：map 物件（惰性求值），通常轉成 list
數列 = [1, 2, 3, 4, 5]
平方結果 = list(map(lambda x: x ** 2, 數列))
print(f"map 平方: {平方結果}")  # [1, 4, 9, 16, 25]

# --- filter：過濾元素 ---
# 輸入：判斷函式 + 可迭代物件
# 處理：保留回傳 True 的元素
# 輸出：filter 物件，通常轉成 list
偶數 = list(filter(lambda x: x % 2 == 0, 數列))
print(f"filter 偶數: {偶數}")  # [2, 4]

# --- reduce：累積運算 ---
from functools import reduce
# 輸入：二元函式 + 可迭代物件
# 處理：從左至右累積 (((1+2)+3)+4)+5
# 輸出：單一累積值
總和 = reduce(lambda 累積, 當前: 累積 + 當前, 數列)
print(f"reduce 總和: {總和}")  # 15

# 實務範例：用 reduce 組合字典
片段列表 = [
    {"model": "yolov8"},
    {"confidence": 0.85},
    {"device": "cuda:0"},
]
合併字典 = reduce(lambda 累積, 片段: {**累積, **片段}, 片段列表, {})
print(f"合併: {合併字典}")
# {'model': 'yolov8', 'confidence': 0.85, 'device': 'cuda:0'}
```

### 2.3 閉包 (Closure)

```python
def 建立計數器(起始值=0):
    """
    輸入：起始值 (int)
    處理：建立一個閉包，內部函式記住並修改外部變數
    輸出：function — 每次呼叫回傳遞增後的值
    """
    計數 = [起始值]  # 用 list 包裝，讓內部函式可修改

    def 遞增():
        計數[0] += 1
        return 計數[0]

    return 遞增

計數器A = 建立計數器(0)
計數器B = 建立計數器(100)

print(計數器A())  # 1
print(計數器A())  # 2
print(計數器B())  # 101  ← 兩個計數器互不干擾
print(計數器A())  # 3
```

```python
# 用 nonlocal 的閉包寫法（Python 3+）
def 建立累加器(起始值=0):
    """
    輸入：起始值 (int)
    處理：用 nonlocal 讓內部函式修改外部變數
    輸出：function — 每次呼叫加上指定量並回傳
    """
    總和 = 起始值

    def 加上(數值):
        nonlocal 總和
        總和 += 數值
        return 總和

    return 加上

累加 = 建立累加器(0)
print(累加(10))   # 10
print(累加(20))   # 30
print(累加(5))    # 35
```

### 2.4 裝飾器 (Decorator) — 從零推導

**第一層：函式可以被當成參數傳遞**

```python
def 大聲說(文字):
    """輸入：str → 處理：轉大寫 → 輸出：str"""
    return 文字.upper()

def 小聲說(文字):
    """輸入：str → 處理：轉小寫 → 輸出：str"""
    return 文字.lower()

def 用某種方式說(說話函式, 文字):
    """
    輸入：說話函式(function), 文字(str)
    處理：呼叫傳入的函式
    輸出：str
    """
    return 說話函式(文字)

print(用某種方式說(大聲說, "Hello World"))  # HELLO WORLD
print(用某種方式說(小聲說, "Hello World"))  # hello world
```

**第二層：函式可以回傳函式（手動包裝）**

```python
def 計時包裝(原始函式):
    """
    輸入：原始函式 (function)
    處理：建立一個新函式，在前後加上計時邏輯
    輸出：function — 包裝後的新函式
    """
    import time

    def 包裝後(*args, **kwargs):
        開始 = time.time()
        結果 = 原始函式(*args, **kwargs)
        耗時 = time.time() - 開始
        print(f"[計時] {原始函式.__name__} 耗時 {耗時:.4f} 秒")
        return 結果

    return 包裝後

def 慢速加法(a, b):
    """輸入：a, b (int) → 處理：模擬耗時 → 輸出：int"""
    import time
    time.sleep(0.1)
    return a + b

# 手動包裝
計時版加法 = 計時包裝(慢速加法)
print(計時版加法(3, 4))
# [計時] 慢速加法 耗時 0.10xx 秒
# 7
```

**第三層：用 @ 語法糖（真正的裝飾器）**

```python
import time
from functools import wraps

def 計時器(函式):
    """
    輸入：函式 (function)
    處理：用 @wraps 保留原始函式的 metadata，加上計時邏輯
    輸出：function — 裝飾後的函式
    """
    @wraps(函式)  # 保留 __name__, __doc__ 等屬性
    def 包裝(*args, **kwargs):
        開始 = time.time()
        結果 = 函式(*args, **kwargs)
        耗時 = time.time() - 開始
        print(f"[計時] {函式.__name__} 耗時 {耗時:.6f} 秒")
        return 結果
    return 包裝

@計時器
def 費波那契(n):
    """
    輸入：n (int) — 第幾個費波那契數
    處理：遞迴計算
    輸出：int — 費波那契數
    """
    if n <= 1:
        return n
    return 費波那契(n - 1) + 費波那契(n - 2)

# @計時器 等同於：費波那契 = 計時器(費波那契)
print(費波那契(20))
# [計時] 費波那契 耗時 0.00xxxx 秒  （遞迴會多次觸發）
# 6765

# 驗證 @wraps 的效果
print(費波那契.__name__)  # "費波那契"（不是 "包裝"）
print(費波那契.__doc__)   # 原始 docstring 保留
```

```python
# --- 帶參數的裝飾器（三層巢狀）---
from functools import wraps

def 重試(最大次數=3, 例外類型=Exception):
    """
    輸入：最大次數(int), 例外類型(type)
    處理：建立裝飾器，在函式失敗時自動重試
    輸出：decorator function
    """
    def 裝飾器(函式):
        @wraps(函式)
        def 包裝(*args, **kwargs):
            最後例外 = None
            for 第幾次 in range(1, 最大次數 + 1):
                try:
                    return 函式(*args, **kwargs)
                except 例外類型 as e:
                    最後例外 = e
                    print(f"[重試] {函式.__name__} 第 {第幾次} 次失敗: {e}")
            raise 最後例外
        return 包裝
    return 裝飾器

import random

@重試(最大次數=5, 例外類型=ValueError)
def 不穩定的API呼叫():
    """
    輸入：無
    處理：模擬 70% 失敗率的 API
    輸出：str — 成功訊息
    """
    if random.random() < 0.7:
        raise ValueError("伺服器忙碌")
    return "成功取得資料"

結果 = 不穩定的API呼叫()
print(結果)
```

---

## 3. 類別完整攻略 (Classes Complete Guide)

### 3.1 魔術方法 (Dunder Methods)

```python
class 向量:
    """二維向量類別，示範常見魔術方法"""

    def __init__(self, x, y):
        """
        輸入：x (float), y (float)
        處理：儲存為實例屬性
        輸出：無（初始化用）
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """
        輸入：無
        處理：產生「可重建物件」的字串（給開發者看）
        輸出：str
        """
        return f"向量({self.x}, {self.y})"

    def __str__(self):
        """
        輸入：無
        處理：產生「人類易讀」的字串（給使用者看）
        輸出：str
        """
        return f"({self.x}, {self.y})"

    def __len__(self):
        """
        輸入：無
        處理：回傳維度數（固定 2）
        輸出：int
        """
        return 2

    def __getitem__(self, 索引):
        """
        輸入：索引 (int) — 0 或 1
        處理：回傳對應分量
        輸出：float
        """
        if 索引 == 0:
            return self.x
        elif 索引 == 1:
            return self.y
        else:
            raise IndexError(f"向量只有 2 個分量，索引 {索引} 超出範圍")

    def __add__(self, 其他):
        """
        輸入：其他 (向量)
        處理：分量相加
        輸出：向量 — 新的向量物件
        """
        return 向量(self.x + 其他.x, self.y + 其他.y)

    def __eq__(self, 其他):
        """
        輸入：其他 (向量)
        處理：比較兩個向量是否相等
        輸出：bool
        """
        return self.x == 其他.x and self.y == 其他.y

# 使用範例
v1 = 向量(3, 4)
v2 = 向量(1, 2)

print(repr(v1))       # 向量(3, 4)  ← __repr__
print(str(v1))        # (3, 4)      ← __str__
print(len(v1))        # 2           ← __len__
print(v1[0])          # 3           ← __getitem__
print(v1 + v2)        # (4, 6)      ← __add__ → __str__
print(v1 == 向量(3,4)) # True       ← __eq__
```

### 3.2 @property, @staticmethod, @classmethod

```python
class 溫度:
    """溫度轉換類別，示範三種方法裝飾器"""

    def __init__(self, 攝氏度):
        """
        輸入：攝氏度 (float)
        處理：儲存攝氏溫度（內部用 _攝氏 表示「受保護」）
        輸出：無
        """
        self._攝氏 = 攝氏度

    @property
    def 攝氏(self):
        """
        輸入：無
        處理：回傳攝氏溫度
        輸出：float — 讓外部像讀取屬性一樣取值
        """
        return self._攝氏

    @攝氏.setter
    def 攝氏(self, 值):
        """
        輸入：值 (float) — 新的攝氏溫度
        處理：驗證不低於絕對零度後設定
        輸出：無
        """
        if 值 < -273.15:
            raise ValueError("溫度不能低於絕對零度 (-273.15°C)")
        self._攝氏 = 值

    @property
    def 華氏(self):
        """
        輸入：無
        處理：攝氏轉華氏
        輸出：float
        """
        return self._攝氏 * 9 / 5 + 32

    @staticmethod
    def 是否沸騰(攝氏溫度):
        """
        輸入：攝氏溫度 (float)
        處理：判斷是否達到水的沸點（不需要 self）
        輸出：bool
        """
        return 攝氏溫度 >= 100.0

    @classmethod
    def 從華氏建立(cls, 華氏度):
        """
        輸入：華氏度 (float)
        處理：華氏轉攝氏後建立新實例
        輸出：溫度 — 新的溫度物件
        """
        攝氏度 = (華氏度 - 32) * 5 / 9
        return cls(攝氏度)

# 使用範例
t1 = 溫度(100)
print(f"攝氏: {t1.攝氏}°C")   # 100°C
print(f"華氏: {t1.華氏}°F")   # 212.0°F

t2 = 溫度.從華氏建立(72)       # classmethod 建立
print(f"72°F = {t2.攝氏:.1f}°C")  # 22.2°C

print(溫度.是否沸騰(100))       # True  ← staticmethod
print(溫度.是否沸騰(99))        # False

t1.攝氏 = 50                   # setter 驗證通過
# t1.攝氏 = -300              # ValueError!
```

### 3.3 繼承與 super()

```python
class 動物:
    """基礎動物類別"""

    def __init__(self, 名字, 年齡):
        """
        輸入：名字(str), 年齡(int)
        處理：儲存基本屬性
        輸出：無
        """
        self.名字 = 名字
        self.年齡 = 年齡

    def 說話(self):
        """
        輸入：無
        處理：基礎類別的預設行為
        輸出：str
        """
        return f"{self.名字}發出聲音"

    def __repr__(self):
        return f"{type(self).__name__}({self.名字!r}, {self.年齡})"


class 狗(動物):
    """狗 — 單一繼承範例"""

    def __init__(self, 名字, 年齡, 品種):
        """
        輸入：名字(str), 年齡(int), 品種(str)
        處理：呼叫父類別 __init__ 後加上品種
        輸出：無
        """
        super().__init__(名字, 年齡)  # 呼叫 動物.__init__
        self.品種 = 品種

    def 說話(self):
        """輸入：無 → 處理：覆寫父類別 → 輸出：str"""
        return f"{self.名字}：汪汪！"


class 導盲犬(狗):
    """導盲犬 — 多層繼承"""

    def __init__(self, 名字, 年齡, 品種, 主人):
        """
        輸入：名字(str), 年齡(int), 品種(str), 主人(str)
        處理：逐層呼叫 super()
        輸出：無
        """
        super().__init__(名字, 年齡, 品種)
        self.主人 = 主人

    def 帶路(self):
        """輸入：無 → 處理：描述帶路行為 → 輸出：str"""
        return f"{self.名字}正在為{self.主人}帶路"


小白 = 導盲犬("小白", 3, "拉布拉多", "王先生")
print(小白.說話())   # 小白：汪汪！（繼承自 狗）
print(小白.帶路())   # 小白正在為王先生帶路
print(repr(小白))    # 導盲犬('小白', 3)（繼承自 動物）
```

### 3.4 多重繼承與 MRO

```python
class 可飛行:
    """混入類別 (Mixin) — 飛行能力"""

    def 飛(self):
        """輸入：無 → 處理：描述飛行 → 輸出：str"""
        return f"{self.名字}在天空飛翔"


class 可游泳:
    """混入類別 (Mixin) — 游泳能力"""

    def 游(self):
        """輸入：無 → 處理：描述游泳 → 輸出：str"""
        return f"{self.名字}在水中游泳"


class 鴨子(可飛行, 可游泳, 動物):
    """鴨子 — 多重繼承"""

    def __init__(self, 名字, 年齡):
        """
        輸入：名字(str), 年齡(int)
        處理：呼叫 super() 沿 MRO 鏈傳遞
        輸出：無
        """
        super().__init__(名字, 年齡)

    def 說話(self):
        """輸入：無 → 處理：覆寫 → 輸出：str"""
        return f"{self.名字}：嘎嘎！"


唐老鴨 = 鴨子("唐老鴨", 5)
print(唐老鴨.說話())  # 唐老鴨：嘎嘎！
print(唐老鴨.飛())    # 唐老鴨在天空飛翔
print(唐老鴨.游())    # 唐老鴨在水中游泳

# 查看 MRO（方法解析順序）
print("MRO:", [cls.__name__ for cls in 鴨子.__mro__])
# MRO: ['鴨子', '可飛行', '可游泳', '動物', 'object']
# Python 使用 C3 線性化演算法決定搜尋順序
```

### 3.5 抽象類別 ABC

```python
from abc import ABC, abstractmethod

class 模型基礎(ABC):
    """
    抽象基礎類別 — 定義所有 ML 模型必須實作的介面
    不能直接實例化
    """

    def __init__(self, 模型名稱):
        """
        輸入：模型名稱 (str)
        處理：儲存名稱
        輸出：無
        """
        self.模型名稱 = 模型名稱

    @abstractmethod
    def 訓練(self, 資料):
        """
        輸入：資料 — 訓練資料
        處理：子類別必須實作訓練邏輯
        輸出：由子類別定義
        """
        pass

    @abstractmethod
    def 預測(self, 輸入):
        """
        輸入：輸入 — 要預測的資料
        處理：子類別必須實作預測邏輯
        輸出：由子類別定義
        """
        pass

    def 摘要(self):
        """
        輸入：無
        處理：回傳模型摘要（共用方法，不需覆寫）
        輸出：str
        """
        return f"模型: {self.模型名稱} ({type(self).__name__})"


class 線性回歸(模型基礎):
    """具體實作 — 線性回歸"""

    def __init__(self):
        super().__init__("線性回歸")
        self.權重 = None

    def 訓練(self, 資料):
        """
        輸入：資料 (list[tuple]) — [(x, y), ...]
        處理：用最小平方法擬合
        輸出：str — 訓練完成訊息
        """
        n = len(資料)
        sum_x = sum(d[0] for d in 資料)
        sum_y = sum(d[1] for d in 資料)
        sum_xy = sum(d[0] * d[1] for d in 資料)
        sum_x2 = sum(d[0] ** 2 for d in 資料)

        self.權重 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        self.偏差 = (sum_y - self.權重 * sum_x) / n
        return f"訓練完成: y = {self.權重:.2f}x + {self.偏差:.2f}"

    def 預測(self, 輸入):
        """
        輸入：輸入 (float) — x 值
        處理：代入線性公式
        輸出：float — 預測的 y 值
        """
        return self.權重 * 輸入 + self.偏差


# 使用範例
# m = 模型基礎("test")  # TypeError: 不能實例化抽象類別

模型 = 線性回歸()
訓練資料 = [(1, 2), (2, 4), (3, 6), (4, 8)]
print(模型.訓練(訓練資料))  # 訓練完成: y = 2.00x + 0.00
print(模型.預測(10))        # 20.0
print(模型.摘要())          # 模型: 線性回歸 (線性回歸)
```

---

## 4. dataclass 完整教學

### 4.1 基本用法

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class 偵測結果:
    """
    來自 VisionDSL 專案的真實模式
    dataclass 自動產生 __init__, __repr__, __eq__
    """
    id: str                                          # 必填欄位
    類型: str                                        # 必填欄位
    邊界框: List[float]                              # 必填欄位
    信心度: float = 1.0                              # 有預設值
    屬性: Dict[str, Any] = field(default_factory=dict)  # 可變預設值

# 使用範例
d1 = 偵測結果(
    id="det_001",
    類型="person",
    邊界框=[100.0, 200.0, 300.0, 400.0],
    信心度=0.95,
    屬性={"age": "adult", "wearing_hat": True}
)
d2 = 偵測結果(id="det_002", 類型="car", 邊界框=[50.0, 50.0, 200.0, 150.0])

print(d1)
# 偵測結果(id='det_001', 類型='person', 邊界框=[100.0, 200.0, 300.0, 400.0],
#          信心度=0.95, 屬性={'age': 'adult', 'wearing_hat': True})
print(d2.信心度)   # 1.0（使用預設值）
print(d2.屬性)     # {}（使用 default_factory 產生的新空字典）
```

### 4.2 field(default_factory=...) 為什麼需要

```python
# ❌ 錯誤寫法 — 所有實例會共用同一個 list 物件！
# @dataclass
# class 錯誤範例:
#     標籤: List[str] = []  # 這會引發 ValueError

# ✅ 正確寫法 — 每個實例都得到自己的新 list
@dataclass
class 正確範例:
    標籤: List[str] = field(default_factory=list)

a = 正確範例()
b = 正確範例()
a.標籤.append("已標記")

print(a.標籤)  # ['已標記']
print(b.標籤)  # [] ← 互不干擾，因為各自有獨立的 list

# field() 的其他實用參數
@dataclass
class 進階欄位示範:
    """
    輸入：各欄位值
    處理：field() 可控制每個欄位的行為
    輸出：dataclass 實例
    """
    名字: str
    密碼: str = field(repr=False)           # repr 不顯示
    建立時間: float = field(default_factory=lambda: __import__('time').time())
    標籤: List[str] = field(default_factory=list)
    _內部快取: dict = field(default_factory=dict, repr=False, compare=False)

使用者 = 進階欄位示範(名字="Alice", 密碼="secret123")
print(使用者)
# 進階欄位示範(名字='Alice', 建立時間=1700000000.0, 標籤=[])
# 注意：密碼和 _內部快取 不會出現在 repr 中
```

### 4.3 frozen=True 不可變

```python
@dataclass(frozen=True)
class 座標:
    """
    frozen=True 讓實例建立後不可修改（類似 tuple）
    同時自動產生 __hash__，可以放進 set 或當 dict 的 key
    """
    x: float
    y: float

p1 = 座標(1.0, 2.0)
p2 = 座標(1.0, 2.0)
p3 = 座標(3.0, 4.0)

print(p1 == p2)          # True（自動產生的 __eq__）
print(hash(p1) == hash(p2))  # True

# p1.x = 5.0  # FrozenInstanceError! 不能修改

# 因為可 hash，能放進 set
座標集合 = {p1, p2, p3}
print(f"不重複座標數: {len(座標集合)}")  # 2（p1 和 p2 相同）

# 也能當字典的 key
距離表 = {p1: 0.0, p3: 5.0}
print(距離表[座標(1.0, 2.0)])  # 0.0
```

### 4.4 __post_init__

```python
from dataclasses import dataclass, field
from typing import List
import math

@dataclass
class 三角形:
    """
    __post_init__ 在 __init__ 之後自動執行
    用於驗證、計算衍生屬性
    """
    邊a: float
    邊b: float
    邊c: float
    面積: float = field(init=False)    # init=False 表示不從建構子傳入
    是否有效: bool = field(init=False)

    def __post_init__(self):
        """
        輸入：無（使用已設定的 邊a, 邊b, 邊c）
        處理：驗證三角不等式 + 計算面積
        輸出：無（設定 面積 和 是否有效 屬性）
        """
        # 三角不等式驗證
        self.是否有效 = (
            self.邊a + self.邊b > self.邊c and
            self.邊b + self.邊c > self.邊a and
            self.邊a + self.邊c > self.邊b
        )

        if self.是否有效:
            # 海龍公式計算面積
            s = (self.邊a + self.邊b + self.邊c) / 2
            self.面積 = math.sqrt(s * (s - self.邊a) * (s - self.邊b) * (s - self.邊c))
        else:
            self.面積 = 0.0

t1 = 三角形(3, 4, 5)
print(t1)
# 三角形(邊a=3, 邊b=4, 邊c=5, 面積=6.0, 是否有效=True)

t2 = 三角形(1, 1, 10)
print(t2.是否有效)  # False
print(t2.面積)      # 0.0
```

---

## 5. Type Hints 型別提示

Python 的型別提示不會影響執行，但能讓 IDE 和靜態分析工具（mypy）幫你抓錯。

### 5.1 基本型別與容器型別

```python
from typing import List, Dict, Tuple, Set, Optional, Union, Any

# --- 基本型別 ---
名字: str = "Alice"
年齡: int = 25
身高: float = 165.5
是否活躍: bool = True

# --- 容器型別（Python 3.9+ 可直接用 list[int]，但 typing 版本更通用）---
分數列表: List[int] = [85, 90, 78, 92]
學生成績: Dict[str, float] = {"Alice": 95.0, "Bob": 87.5}
座標: Tuple[float, float] = (3.14, 2.72)
不定長元組: Tuple[int, ...] = (1, 2, 3, 4, 5)  # ... 表示任意長度
唯一標籤: Set[str] = {"person", "car", "dog"}

# --- 函式型別標註 ---
def 計算平均(分數: List[float]) -> float:
    """
    輸入：分數 (List[float]) — 分數列表
    處理：計算平均值
    輸出：float — 平均分數
    """
    return sum(分數) / len(分數) if 分數 else 0.0

結果: float = 計算平均([85.0, 90.0, 78.0])
print(f"平均: {結果:.1f}")  # 平均: 84.3
```

### 5.2 Optional, Union

```python
from typing import Optional, Union

def 查詢使用者(使用者ID: int) -> Optional[Dict[str, Any]]:
    """
    輸入：使用者ID (int)
    處理：模擬資料庫查詢
    輸出：Optional[Dict] — 找到回傳字典，找不到回傳 None
          等同於 Union[Dict[str, Any], None]
    """
    資料庫 = {
        1: {"name": "Alice", "age": 25},
        2: {"name": "Bob", "age": 30},
    }
    return 資料庫.get(使用者ID)  # 找不到回傳 None

def 格式化數值(值: Union[int, float, str]) -> str:
    """
    輸入：值 — 可以是 int, float 或 str
    處理：統一轉成格式化字串
    輸出：str
    """
    if isinstance(值, float):
        return f"{值:.2f}"
    return str(值)

使用者 = 查詢使用者(1)
print(使用者)            # {'name': 'Alice', 'age': 25}
print(查詢使用者(999))   # None

print(格式化數值(42))      # "42"
print(格式化數值(3.14159)) # "3.14"
print(格式化數值("hello")) # "hello"
```

### 5.3 Callable

```python
from typing import Callable, List

def 套用函式到列表(
    函式: Callable[[int], int],
    列表: List[int]
) -> List[int]:
    """
    輸入：函式 — 接受 int 回傳 int 的函式
          列表 — int 的列表
    處理：對每個元素套用函式
    輸出：List[int] — 結果列表
    """
    return [函式(x) for x in 列表]

# Callable[[參數型別...], 回傳型別]
print(套用函式到列表(lambda x: x ** 2, [1, 2, 3, 4]))  # [1, 4, 9, 16]
print(套用函式到列表(lambda x: x + 10, [1, 2, 3, 4]))  # [11, 12, 13, 14]


def 建立驗證器(最小值: float, 最大值: float) -> Callable[[float], bool]:
    """
    輸入：最小值(float), 最大值(float) — 有效範圍
    處理：建立閉包函式
    輸出：Callable[[float], bool] — 驗證函式
    """
    def 驗證(值: float) -> bool:
        return 最小值 <= 值 <= 最大值
    return 驗證

信心度驗證 = 建立驗證器(0.0, 1.0)
print(信心度驗證(0.85))  # True
print(信心度驗證(1.5))   # False
```

### 5.4 TypeVar 與 Generic

```python
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')  # 宣告一個型別變數

class 堆疊(Generic[T]):
    """
    泛型堆疊 — T 可以是任何型別
    使用時指定：堆疊[int](), 堆疊[str]()
    """

    def __init__(self):
        """
        輸入：無
        處理：初始化空堆疊
        輸出：無
        """
        self._資料: List[T] = []

    def 推入(self, 元素: T) -> None:
        """
        輸入：元素 (T) — 要推入的元素
        處理：加到堆疊頂端
        輸出：無
        """
        self._資料.append(元素)

    def 彈出(self) -> T:
        """
        輸入：無
        處理：移除並回傳堆疊頂端元素
        輸出：T — 頂端元素
        """
        if not self._資料:
            raise IndexError("堆疊為空")
        return self._資料.pop()

    def 頂端(self) -> Optional[T]:
        """
        輸入：無
        處理：查看頂端但不移除
        輸出：Optional[T]
        """
        return self._資料[-1] if self._資料 else None

    def __len__(self) -> int:
        return len(self._資料)

    def __repr__(self) -> str:
        return f"堆疊({self._資料})"

# 整數堆疊
整數堆疊: 堆疊[int] = 堆疊()
整數堆疊.推入(10)
整數堆疊.推入(20)
整數堆疊.推入(30)
print(整數堆疊)           # 堆疊([10, 20, 30])
print(整數堆疊.彈出())    # 30
print(整數堆疊.頂端())    # 20

# 字串堆疊
字串堆疊: 堆疊[str] = 堆疊()
字串堆疊.推入("hello")
字串堆疊.推入("world")
print(字串堆疊.彈出())    # "world"
```

---

## 6. `__slots__` 記憶體優化

### 6.1 為什麼用 `__slots__`

一般 Python 物件用 `__dict__` 儲存屬性（一個字典），每個實例約耗 200+ bytes 的字典開銷。
`__slots__` 讓屬性以更緊湊的方式儲存，適合需要建立大量實例的場景。

```python
# 來自 VisionDSL 專案的真實模式
class Detection:
    """使用 __slots__ 的偵測結果類別"""
    __slots__ = ('id', 'class_name', 'bbox_xyxy', 'confidence', 'attributes')

    def __init__(self, id, class_name, bbox_xyxy, confidence, attributes=None):
        """
        輸入：id(str), class_name(str), bbox_xyxy(tuple),
              confidence(float), attributes(dict|None)
        處理：儲存到固定的 slot 中（不使用 __dict__）
        輸出：無
        """
        self.id = id
        self.class_name = class_name
        self.bbox_xyxy = bbox_xyxy
        self.confidence = confidence
        self.attributes = attributes or {}

    def __repr__(self):
        return (f"Detection(id={self.id!r}, class={self.class_name!r}, "
                f"conf={self.confidence:.2f})")


class DetectionNoSlots:
    """不使用 __slots__ 的對照組"""

    def __init__(self, id, class_name, bbox_xyxy, confidence, attributes=None):
        self.id = id
        self.class_name = class_name
        self.bbox_xyxy = bbox_xyxy
        self.confidence = confidence
        self.attributes = attributes or {}


# 使用範例
d = Detection("det_001", "person", (100, 200, 300, 400), 0.95)
print(d)  # Detection(id='det_001', class='person', conf=0.95)

# 嘗試新增不存在的屬性
# d.color = "red"  # AttributeError! __slots__ 禁止動態新增屬性
```

### 6.2 記憶體比較

```python
import sys

class 有Slots:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class 無Slots:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

有slots實例 = 有Slots(1, 2, 3)
無slots實例 = 無Slots(1, 2, 3)

# sys.getsizeof 測量物件本身大小
大小_有slots = sys.getsizeof(有slots實例)
大小_無slots = sys.getsizeof(無slots實例) + sys.getsizeof(無slots實例.__dict__)

print(f"有 __slots__: {大小_有slots} bytes")
print(f"無 __slots__: {大小_無slots} bytes（物件 + __dict__）")
print(f"節省: {大小_無slots - 大小_有slots} bytes/實例")

# 大量實例時的差異
print("\n--- 建立 100,000 個實例 ---")
import tracemalloc
tracemalloc.start()

有slots列表 = [有Slots(i, i+1, i+2) for i in range(100_000)]
快照1 = tracemalloc.take_snapshot()
有slots記憶體 = sum(stat.size for stat in 快照1.statistics('filename'))

tracemalloc.stop()
tracemalloc.start()

無slots列表 = [無Slots(i, i+1, i+2) for i in range(100_000)]
快照2 = tracemalloc.take_snapshot()
無slots記憶體 = sum(stat.size for stat in 快照2.statistics('filename'))

tracemalloc.stop()

print(f"有 __slots__: {有slots記憶體 / 1024 / 1024:.1f} MB")
print(f"無 __slots__: {無slots記憶體 / 1024 / 1024:.1f} MB")
# 一般來說可以省下 30-50% 記憶體
```

---

## 7. 生成器與迭代器 (Generator & Iterator)

### 7.1 yield 基礎

```python
def 費波那契生成器(上限):
    """
    輸入：上限 (int) — 產生多少個數
    處理：每次 yield 暫停函式、回傳值，下次呼叫從暫停處繼續
    輸出：generator — 惰性產生費波那契數列
    """
    a, b = 0, 1
    已產生 = 0
    while 已產生 < 上限:
        yield a          # 暫停，回傳 a
        a, b = b, a + b  # 下次呼叫才執行這行
        已產生 += 1

# 使用 for 迴圈消費生成器
for 數 in 費波那契生成器(10):
    print(數, end=" ")
print()  # 0 1 1 2 3 5 8 13 21 34

# 手動消費
生成器 = 費波那契生成器(5)
print(next(生成器))  # 0
print(next(生成器))  # 1
print(next(生成器))  # 1
print(list(生成器))  # [2, 3] — 剩餘的全部取出
```

### 7.2 生成器表達式

```python
# 列表推導式 — 一次產生所有元素（佔記憶體）
列表版 = [x ** 2 for x in range(1_000_000)]

# 生成器表達式 — 惰性產生（省記憶體）
生成器版 = (x ** 2 for x in range(1_000_000))

import sys
print(f"列表佔用: {sys.getsizeof(列表版):,} bytes")       # ~8,000,000+ bytes
print(f"生成器佔用: {sys.getsizeof(生成器版):,} bytes")    # ~200 bytes

# 實務用法：處理大量資料時用生成器節省記憶體
def 讀取大檔案行(檔案路徑):
    """
    輸入：檔案路徑 (str)
    處理：逐行讀取，不載入整個檔案
    輸出：generator[str] — 每次 yield 一行
    """
    with open(檔案路徑, 'r', encoding='utf-8') as f:
        for 行 in f:
            yield 行.strip()

# 鏈式生成器處理管線
數字列表 = range(1, 101)
偶數 = (x for x in 數字列表 if x % 2 == 0)
平方 = (x ** 2 for x in 偶數)
前五個 = []
for i, 值 in enumerate(平方):
    前五個.append(值)
    if i >= 4:
        break
print(f"前五個偶數的平方: {前五個}")  # [4, 16, 36, 64, 100]
```

### 7.3 自訂迭代器

```python
class 倒數計時:
    """
    自訂迭代器 — 實作 __iter__ 和 __next__
    """

    def __init__(self, 起始值):
        """
        輸入：起始值 (int)
        處理：記錄起始值
        輸出：無
        """
        self.當前值 = 起始值

    def __iter__(self):
        """
        輸入：無
        處理：回傳自己（迭代器本身就是可迭代物件）
        輸出：self
        """
        return self

    def __next__(self):
        """
        輸入：無
        處理：每次呼叫減 1，到 0 時停止
        輸出：int — 當前值
        """
        if self.當前值 <= 0:
            raise StopIteration  # 告訴 for 迴圈「結束了」
        結果 = self.當前值
        self.當前值 -= 1
        return 結果

for 秒 in 倒數計時(5):
    print(f"倒數: {秒}")
# 倒數: 5
# 倒數: 4
# 倒數: 3
# 倒數: 2
# 倒數: 1
```

### 7.4 itertools 常用工具

```python
import itertools

# --- chain：串接多個可迭代物件 ---
列表A = [1, 2, 3]
列表B = [4, 5, 6]
列表C = [7, 8, 9]
串接結果 = list(itertools.chain(列表A, 列表B, 列表C))
print(f"chain: {串接結果}")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# --- islice：對迭代器做切片 ---
無限計數 = itertools.count(start=0, step=5)
前六個 = list(itertools.islice(無限計數, 6))
print(f"islice: {前六個}")  # [0, 5, 10, 15, 20, 25]

# --- groupby：分組（資料需先排序！）---
資料 = [
    {"類型": "水果", "名稱": "蘋果"},
    {"類型": "水果", "名稱": "香蕉"},
    {"類型": "蔬菜", "名稱": "紅蘿蔔"},
    {"類型": "蔬菜", "名稱": "白菜"},
    {"類型": "肉類", "名稱": "雞肉"},
]
# 資料已按 "類型" 排序
for 鍵, 組 in itertools.groupby(資料, key=lambda x: x["類型"]):
    組列表 = [item["名稱"] for item in 組]
    print(f"  {鍵}: {組列表}")
# 水果: ['蘋果', '香蕉']
# 蔬菜: ['紅蘿蔔', '白菜']
# 肉類: ['雞肉']

# --- product：笛卡兒積（取代巢狀 for）---
顏色 = ["紅", "綠"]
尺寸 = ["S", "M", "L"]
所有組合 = list(itertools.product(顏色, 尺寸))
print(f"product: {所有組合}")
# [('紅', 'S'), ('紅', 'M'), ('紅', 'L'), ('綠', 'S'), ('綠', 'M'), ('綠', 'L')]

# --- zip_longest：不同長度也能配對 ---
名字列表 = ["Alice", "Bob", "Charlie"]
分數列表 = [90, 85]
配對結果 = list(itertools.zip_longest(名字列表, 分數列表, fillvalue=0))
print(f"zip_longest: {配對結果}")
# [('Alice', 90), ('Bob', 85), ('Charlie', 0)]
```

---

## 8. 上下文管理器 (Context Manager)

### 8.1 with 語法基本概念

```python
# 最常見的用法：檔案操作
# with 確保離開區塊時一定會關閉檔案，即使發生例外

# 不用 with（危險 — 例外時可能不會關閉）
# f = open("test.txt", "w")
# f.write("hello")
# f.close()  # 如果前一行出錯，這行不會執行

# 用 with（安全）
# with open("test.txt", "w", encoding="utf-8") as f:
#     f.write("hello")  # 即使這裡出錯，檔案也會被正確關閉
```

### 8.2 自訂上下文管理器（class 方式）

```python
import time

class 計時器:
    """
    用 class 實作上下文管理器
    需要 __enter__ 和 __exit__ 兩個方法
    """

    def __init__(self, 標籤=""):
        """
        輸入：標籤 (str) — 標記這段計時的名稱
        處理：儲存標籤
        輸出：無
        """
        self.標籤 = 標籤
        self.開始時間 = None
        self.耗時 = None

    def __enter__(self):
        """
        輸入：無
        處理：記錄開始時間
        輸出：self — as 子句綁定的物件
        """
        self.開始時間 = time.time()
        print(f"[{self.標籤}] 開始計時...")
        return self  # 這就是 `as timer` 中的 timer

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        輸入：exc_type — 例外類型（無例外時為 None）
              exc_val  — 例外值
              exc_tb   — 追蹤資訊
        處理：計算耗時、處理例外
        輸出：bool — True 表示「吞掉例外」，False 表示「繼續拋出」
        """
        self.耗時 = time.time() - self.開始時間
        if exc_type is not None:
            print(f"[{self.標籤}] 發生例外: {exc_val}")
        print(f"[{self.標籤}] 耗時: {self.耗時:.4f} 秒")
        return False  # 不吞掉例外

# 使用範例
with 計時器("排序測試") as t:
    資料 = list(range(100_000, 0, -1))
    資料.sort()

print(f"排序耗時: {t.耗時:.4f} 秒")
```

```python
class 資料庫連線:
    """模擬資料庫連線的上下文管理器"""

    def __init__(self, 連線字串):
        """
        輸入：連線字串 (str) — 資料庫位址
        處理：儲存連線資訊
        輸出：無
        """
        self.連線字串 = 連線字串
        self.已連線 = False

    def __enter__(self):
        """
        輸入：無
        處理：建立連線
        輸出：self
        """
        print(f"連線到 {self.連線字串}...")
        self.已連線 = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        輸入：例外資訊
        處理：確保連線被關閉（即使出錯）
        輸出：False（不吞例外）
        """
        print(f"關閉連線 {self.連線字串}")
        self.已連線 = False
        return False

    def 查詢(self, sql):
        """
        輸入：sql (str)
        處理：模擬查詢
        輸出：list — 查詢結果
        """
        if not self.已連線:
            raise RuntimeError("尚未連線")
        print(f"執行: {sql}")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


with 資料庫連線("postgresql://localhost:5432/mydb") as db:
    結果 = db.查詢("SELECT * FROM users")
    print(f"查到 {len(結果)} 筆資料")
# 離開 with 後自動關閉，即使中間出錯
```

### 8.3 contextlib.contextmanager

```python
from contextlib import contextmanager

@contextmanager
def 暫時切換目錄(目標目錄):
    """
    輸入：目標目錄 (str) — 要切換到的目錄
    處理：yield 前 = __enter__，yield 後 = __exit__
    輸出：generator（由 contextmanager 裝飾器轉成上下文管理器）
    """
    import os
    原始目錄 = os.getcwd()
    try:
        os.chdir(目標目錄)
        print(f"切換到: {目標目錄}")
        yield 目標目錄  # 這就是 as 子句綁定的值
    finally:
        os.chdir(原始目錄)
        print(f"切回: {原始目錄}")

# 使用範例
import os
print(f"目前: {os.getcwd()}")
# with 暫時切換目錄("/tmp") as 路徑:
#     print(f"在 with 中: {os.getcwd()}")
# print(f"離開後: {os.getcwd()}")  # 回到原始目錄
```

```python
from contextlib import contextmanager

@contextmanager
def 抑制例外(*例外類型):
    """
    輸入：例外類型 — 要抑制的例外
    處理：捕捉指定的例外並忽略
    輸出：無
    """
    try:
        yield
    except 例外類型 as e:
        print(f"[已抑制] {type(e).__name__}: {e}")

# 使用範例
with 抑制例外(ZeroDivisionError, ValueError):
    結果 = 10 / 0  # 不會拋出例外
print("程式繼續執行")  # 這行會執行

with 抑制例外(KeyError):
    字典 = {"a": 1}
    值 = 字典["b"]  # KeyError 被抑制
print("程式繼續執行")  # 這行也會執行
```

---

## 9. 例外處理 (Exception Handling)

### 9.1 try / except / else / finally

```python
def 安全讀取設定(檔案路徑):
    """
    輸入：檔案路徑 (str)
    處理：嘗試讀取 JSON 設定檔，完整展示四個區塊的用途
    輸出：dict 或 None
    """
    import json

    try:
        # try 區塊：放可能出錯的程式碼
        with open(檔案路徑, 'r', encoding='utf-8') as f:
            設定 = json.load(f)
    except FileNotFoundError:
        # except：捕捉特定例外
        print(f"檔案不存在: {檔案路徑}")
        return None
    except json.JSONDecodeError as e:
        # 可以有多個 except，各捕捉不同例外
        print(f"JSON 解析錯誤: {e}")
        return None
    except Exception as e:
        # 最後捕捉所有其他例外（注意順序：子類別放前面）
        print(f"未預期的錯誤: {type(e).__name__}: {e}")
        return None
    else:
        # else：只有完全沒有例外時才執行
        print(f"成功載入設定: {list(設定.keys())}")
        return 設定
    finally:
        # finally：不管有沒有例外都會執行（清理用）
        print("設定檔讀取流程結束")

# 模擬呼叫
結果 = 安全讀取設定("不存在的檔案.json")
print(f"結果: {結果}")
# 檔案不存在: 不存在的檔案.json
# 設定檔讀取流程結束
# 結果: None
```

### 9.2 自定義例外

```python
class 應用程式錯誤(Exception):
    """所有自定義例外的基礎類別"""
    pass

class 驗證錯誤(應用程式錯誤):
    """資料驗證失敗"""

    def __init__(self, 欄位名稱, 錯誤值, 訊息="驗證失敗"):
        """
        輸入：欄位名稱(str), 錯誤值(Any), 訊息(str)
        處理：儲存錯誤資訊
        輸出：無
        """
        self.欄位名稱 = 欄位名稱
        self.錯誤值 = 錯誤值
        self.訊息 = 訊息
        super().__init__(f"{訊息}: {欄位名稱}={錯誤值!r}")

class 信心度錯誤(驗證錯誤):
    """信心度超出 [0, 1] 範圍"""

    def __init__(self, 值):
        super().__init__(
            欄位名稱="confidence",
            錯誤值=值,
            訊息="信心度必須在 0 到 1 之間"
        )

class 權限不足(應用程式錯誤):
    """使用者無權執行此操作"""
    pass


def 建立偵測(信心度):
    """
    輸入：信心度 (float)
    處理：驗證信心度範圍
    輸出：dict — 偵測結果
    """
    if not isinstance(信心度, (int, float)):
        raise 驗證錯誤("confidence", 信心度, "必須是數值")
    if not 0 <= 信心度 <= 1:
        raise 信心度錯誤(信心度)
    return {"type": "detection", "confidence": 信心度}


# 使用自定義例外
try:
    結果 = 建立偵測(1.5)
except 信心度錯誤 as e:
    print(f"信心度錯誤: {e}")
    print(f"  欄位: {e.欄位名稱}")
    print(f"  錯誤值: {e.錯誤值}")
except 驗證錯誤 as e:
    print(f"驗證錯誤: {e}")
except 應用程式錯誤 as e:
    print(f"應用程式錯誤: {e}")

# 輸出：
# 信心度錯誤: 信心度必須在 0 到 1 之間: confidence=1.5
#   欄位: confidence
#   錯誤值: 1.5
```

### 9.3 raise from（例外鏈）

```python
class 設定載入錯誤(Exception):
    """設定檔載入失敗"""
    pass

def 載入模型設定(設定路徑):
    """
    輸入：設定路徑 (str)
    處理：嘗試載入設定，用 raise...from 保留原始例外
    輸出：dict
    """
    import json

    try:
        with open(設定路徑, 'r') as f:
            原始資料 = f.read()
    except FileNotFoundError as e:
        # raise X from Y：Y 是原始原因，X 是新的更高層例外
        raise 設定載入錯誤(
            f"找不到設定檔: {設定路徑}"
        ) from e

    try:
        設定 = json.loads(原始資料)
    except json.JSONDecodeError as e:
        raise 設定載入錯誤(
            f"設定檔格式錯誤: {設定路徑}, 行 {e.lineno}"
        ) from e

    return 設定

# 使用範例
try:
    設定 = 載入模型設定("model_config.json")
except 設定載入錯誤 as e:
    print(f"載入失敗: {e}")
    print(f"原始原因: {e.__cause__}")
    # 載入失敗: 找不到設定檔: model_config.json
    # 原始原因: [Errno 2] No such file or directory: 'model_config.json'
```

---

## 10. 模組與套件 (Modules & Packages)

### 10.1 `__init__.py` 的角色

```
專案結構：
my_package/
    __init__.py       # 讓目錄成為 Python 套件
    core.py
    utils.py
    models/
        __init__.py   # 子套件
        yolo.py
        sam.py
```

```python
# === my_package/__init__.py ===
# 這個檔案在 import my_package 時自動執行

# 方式一：直接匯入子模組的東西，讓外部使用更方便
from .core import 核心引擎
from .utils import 格式化輸出

# 方式二：定義版本資訊
__version__ = "1.0.0"

# 使用者可以這樣用：
# from my_package import 核心引擎  （不需要知道在 core.py 裡）
```

### 10.2 `__all__` 控制 public API

```python
# === my_package/utils.py ===

# __all__ 定義「from module import *」時匯出哪些名稱
__all__ = ['格式化輸出', '安全除法']

def 格式化輸出(資料):
    """
    輸入：資料 (Any)
    處理：格式化為易讀字串
    輸出：str
    """
    return f"[OUTPUT] {資料}"

def 安全除法(a, b):
    """
    輸入：a (float), b (float)
    處理：安全除法
    輸出：float 或 None
    """
    return a / b if b != 0 else None

def _內部輔助函式():
    """以底線開頭表示「不建議外部使用」"""
    pass

# from my_package.utils import *
# 只會匯入 格式化輸出 和 安全除法
# _內部輔助函式 不會被 * 匯入（但仍可明確匯入）
```

### 10.3 相對匯入 vs 絕對匯入

```python
# === my_package/models/yolo.py ===

# --- 絕對匯入（推薦用於大型專案）---
from my_package.core import 核心引擎
from my_package.utils import 格式化輸出

# --- 相對匯入（在套件內部使用）---
from ..core import 核心引擎        # .. 表示上一層套件
from ..utils import 格式化輸出     # .. = my_package
from .sam import SAM模型           # .  = 同一層（models/）

# 相對匯入的規則：
# .   = 當前套件（同層目錄）
# ..  = 上一層套件
# ... = 上兩層套件（盡量不要用到這麼深）

class YOLO偵測器:
    """
    輸入：模型路徑 (str)
    處理：載入 YOLO 模型
    輸出：偵測器實例
    """
    def __init__(self, 模型路徑):
        self.模型路徑 = 模型路徑
        # self.引擎 = 核心引擎(模型路徑)  # 使用絕對匯入的模組

    def 偵測(self, 圖片):
        """
        輸入：圖片 — 影像資料
        處理：執行物件偵測
        輸出：list[dict] — 偵測結果
        """
        return [{"class": "person", "confidence": 0.95}]
```

### 10.4 延遲匯入 (Lazy Import)

```python
# === 來自 VisionDSL 專案的真實模式 ===
# 為什麼需要延遲匯入？
# 1. 某些套件（如 torch）import 很慢，不一定每次都用到
# 2. 避免循環匯入
# 3. 可選依賴 — 使用者沒安裝也不會在 import 時就報錯

# --- 模式一：函式級延遲匯入 ---
def 建立SAM3管線(*args, **kwargs):
    """
    輸入：任意參數（透傳給真正的 Adapter）
    處理：只在真正呼叫時才 import 重量級模組
    輸出：SAM3PipelineAdapter 實例
    """
    from .sam3_pipeline import SAM3PipelineAdapter as _Adapter
    return _Adapter(*args, **kwargs)


# --- 模式二：__getattr__ 模組級延遲匯入（Python 3.7+）---
# 放在 __init__.py 中

def __getattr__(名稱):
    """
    輸入：名稱 (str) — 被存取的屬性名稱
    處理：只在存取時才匯入對應模組
    輸出：被請求的模組或物件
    """
    if 名稱 == "YOLO偵測器":
        from .models.yolo import YOLO偵測器
        return YOLO偵測器
    elif 名稱 == "SAM模型":
        from .models.sam import SAM模型
        return SAM模型
    raise AttributeError(f"module {__name__!r} has no attribute {名稱!r}")


# --- 模式三：try/except 處理可選依賴 ---
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # 讓型別提示不報錯

def 建立張量(資料):
    """
    輸入：資料 (list) — 數值列表
    處理：如果有 torch 就建立張量，沒有就用原始列表
    輸出：torch.Tensor 或 list
    """
    if HAS_TORCH:
        return torch.tensor(資料)
    else:
        print("警告: PyTorch 未安裝，回傳原始列表")
        return 資料

# 使用者體驗：
# import my_package          # 快速（不載入 torch）
# det = my_package.YOLO偵測器("model.pt")  # 此時才載入 yolo 模組
```

---

## 11. 設計模式實踐

### 11.1 Registry Pattern（註冊表模式）

```python
# 來自 VisionDSL logic.py 的真實模式
# 用字典映射取代大量 if-elif，方便擴充

import math

# --- 基本版：函式註冊表 ---
def op_touch(物件A, 物件B):
    """
    輸入：物件A(dict), 物件B(dict) — 各含 bbox 欄位
    處理：判斷兩個邊界框是否接觸
    輸出：bool
    """
    ax1, ay1, ax2, ay2 = 物件A["bbox"]
    bx1, by1, bx2, by2 = 物件B["bbox"]
    水平重疊 = ax1 <= bx2 and bx1 <= ax2
    垂直重疊 = ay1 <= by2 and by1 <= ay2
    return 水平重疊 and 垂直重疊

def op_inside(物件A, 物件B):
    """
    輸入：物件A(dict), 物件B(dict)
    處理：判斷 A 是否完全在 B 裡面
    輸出：bool
    """
    ax1, ay1, ax2, ay2 = 物件A["bbox"]
    bx1, by1, bx2, by2 = 物件B["bbox"]
    return ax1 >= bx1 and ay1 >= by1 and ax2 <= bx2 and ay2 <= by2

def op_distance(物件A, 物件B):
    """
    輸入：物件A(dict), 物件B(dict)
    處理：計算兩個邊界框中心的距離
    輸出：float
    """
    ax1, ay1, ax2, ay2 = 物件A["bbox"]
    bx1, by1, bx2, by2 = 物件B["bbox"]
    中心A = ((ax1 + ax2) / 2, (ay1 + ay2) / 2)
    中心B = ((bx1 + bx2) / 2, (by1 + by2) / 2)
    return math.sqrt((中心A[0] - 中心B[0])**2 + (中心A[1] - 中心B[1])**2)

# 註冊表：字串 → 函式
ops_map = {
    'TOUCH': op_touch,
    'INSIDE': op_inside,
    'DISTANCE': op_distance,
}

def 執行空間操作(操作名稱, 物件A, 物件B):
    """
    輸入：操作名稱(str), 物件A(dict), 物件B(dict)
    處理：從註冊表查找並執行對應函式
    輸出：取決於操作（bool 或 float）
    """
    if 操作名稱 not in ops_map:
        raise ValueError(f"未知操作: {操作名稱}，可用: {list(ops_map.keys())}")
    函式 = ops_map[操作名稱]
    return 函式(物件A, 物件B)

# 使用範例
人 = {"bbox": [100, 100, 200, 300]}
車 = {"bbox": [150, 150, 400, 500]}

print(執行空間操作("TOUCH", 人, 車))     # True
print(執行空間操作("INSIDE", 人, 車))    # False
print(執行空間操作("DISTANCE", 人, 車))  # 距離值
```

```python
# --- 進階版：裝飾器自動註冊 ---

class 操作註冊表:
    """
    用裝飾器自動收集函式，無需手動維護 dict
    """

    def __init__(self):
        """
        輸入：無
        處理：初始化空註冊表
        輸出：無
        """
        self._函式表 = {}

    def 註冊(self, 名稱):
        """
        輸入：名稱 (str) — 操作名稱
        處理：回傳裝飾器，將函式加入註冊表
        輸出：decorator function
        """
        def 裝飾器(函式):
            self._函式表[名稱] = 函式
            return 函式
        return 裝飾器

    def 執行(self, 名稱, *args, **kwargs):
        """
        輸入：名稱(str), 其餘參數
        處理：查表並呼叫
        輸出：函式回傳值
        """
        if 名稱 not in self._函式表:
            raise KeyError(f"未註冊: {名稱}，可用: {list(self._函式表.keys())}")
        return self._函式表[名稱](*args, **kwargs)

    def 列出所有(self):
        """
        輸入：無
        處理：回傳所有已註冊的操作名稱
        輸出：list[str]
        """
        return list(self._函式表.keys())


# 建立全域註冊表
啟動函式表 = 操作註冊表()

@啟動函式表.註冊("relu")
def relu(x):
    """輸入：x(float) → 處理：max(0, x) → 輸出：float"""
    return max(0.0, x)

@啟動函式表.註冊("sigmoid")
def sigmoid(x):
    """輸入：x(float) → 處理：1/(1+e^(-x)) → 輸出：float"""
    return 1.0 / (1.0 + math.exp(-x))

@啟動函式表.註冊("tanh")
def tanh(x):
    """輸入：x(float) → 處理：tanh(x) → 輸出：float"""
    return math.tanh(x)

# 使用
print(f"可用啟動函式: {啟動函式表.列出所有()}")
print(f"relu(-3)    = {啟動函式表.執行('relu', -3)}")       # 0.0
print(f"relu(5)     = {啟動函式表.執行('relu', 5)}")        # 5.0
print(f"sigmoid(0)  = {啟動函式表.執行('sigmoid', 0)}")     # 0.5
print(f"tanh(1)     = {啟動函式表.執行('tanh', 1):.4f}")    # 0.7616
```

### 11.2 觀察者模式 (Observer Pattern)

```python
from typing import Callable, List, Dict, Any

class 事件系統:
    """
    觀察者模式 — 發布/訂閱架構
    常用於 GUI、訓練回呼、日誌系統
    """

    def __init__(self):
        """
        輸入：無
        處理：初始化事件 → 處理函式的映射表
        輸出：無
        """
        self._訂閱者: Dict[str, List[Callable]] = {}

    def 訂閱(self, 事件名稱: str, 處理函式: Callable) -> None:
        """
        輸入：事件名稱(str), 處理函式(Callable)
        處理：將處理函式加入對應事件的訂閱者列表
        輸出：無
        """
        if 事件名稱 not in self._訂閱者:
            self._訂閱者[事件名稱] = []
        self._訂閱者[事件名稱].append(處理函式)

    def 發布(self, 事件名稱: str, **資料) -> None:
        """
        輸入：事件名稱(str), 資料(**kwargs)
        處理：通知所有訂閱該事件的函式
        輸出：無
        """
        if 事件名稱 in self._訂閱者:
            for 處理函式 in self._訂閱者[事件名稱]:
                處理函式(**資料)

    def 取消訂閱(self, 事件名稱: str, 處理函式: Callable) -> None:
        """
        輸入：事件名稱(str), 處理函式(Callable)
        處理：從訂閱列表中移除
        輸出：無
        """
        if 事件名稱 in self._訂閱者:
            self._訂閱者[事件名稱].remove(處理函式)


# --- 模擬 ML 訓練的回呼系統 ---
訓練事件 = 事件系統()

def 紀錄損失(epoch, loss, **kwargs):
    """輸入：epoch, loss → 處理：印出日誌 → 輸出：無"""
    print(f"  [日誌] Epoch {epoch}: loss = {loss:.4f}")

def 儲存檢查點(epoch, loss, **kwargs):
    """輸入：epoch, loss → 處理：模擬儲存模型 → 輸出：無"""
    if loss < 0.1:
        print(f"  [儲存] Epoch {epoch}: 損失夠低，儲存檢查點")

def 提前停止(epoch, loss, **kwargs):
    """輸入：epoch, loss → 處理：模擬提前停止判斷 → 輸出：無"""
    if loss < 0.05:
        print(f"  [停止] Epoch {epoch}: 達到目標，建議停止訓練")

# 訂閱事件
訓練事件.訂閱("epoch_end", 紀錄損失)
訓練事件.訂閱("epoch_end", 儲存檢查點)
訓練事件.訂閱("epoch_end", 提前停止)

# 模擬訓練
模擬損失 = [0.5, 0.3, 0.15, 0.08, 0.03]
for i, loss in enumerate(模擬損失):
    print(f"--- Epoch {i+1} ---")
    訓練事件.發布("epoch_end", epoch=i+1, loss=loss)
```

### 11.3 工廠模式 (Factory Pattern)

```python
from abc import ABC, abstractmethod
from typing import Dict, Type

# --- 抽象基礎類別 ---
class 偵測器(ABC):
    """所有偵測器的介面"""

    @abstractmethod
    def 偵測(self, 圖片路徑: str) -> list:
        """
        輸入：圖片路徑 (str)
        處理：執行偵測
        輸出：list[dict] — 偵測結果
        """
        pass

    @abstractmethod
    def 模型名稱(self) -> str:
        """
        輸入：無
        處理：回傳模型名稱
        輸出：str
        """
        pass


# --- 具體實作 ---
class YOLO偵測器(偵測器):
    def __init__(self, 版本: str = "v8"):
        self.版本 = 版本

    def 偵測(self, 圖片路徑: str) -> list:
        """
        輸入：圖片路徑 (str)
        處理：模擬 YOLO 偵測
        輸出：list[dict]
        """
        print(f"YOLO{self.版本} 正在偵測: {圖片路徑}")
        return [{"class": "person", "confidence": 0.95, "bbox": [10, 20, 100, 200]}]

    def 模型名稱(self) -> str:
        return f"YOLO{self.版本}"


class SSD偵測器(偵測器):
    def __init__(self, 骨幹網路: str = "mobilenet"):
        self.骨幹網路 = 骨幹網路

    def 偵測(self, 圖片路徑: str) -> list:
        """
        輸入：圖片路徑 (str)
        處理：模擬 SSD 偵測
        輸出：list[dict]
        """
        print(f"SSD ({self.骨幹網路}) 正在偵測: {圖片路徑}")
        return [{"class": "car", "confidence": 0.88, "bbox": [50, 50, 300, 200]}]

    def 模型名稱(self) -> str:
        return f"SSD-{self.骨幹網路}"


class DETR偵測器(偵測器):
    def __init__(self, 編碼器層數: int = 6):
        self.編碼器層數 = 編碼器層數

    def 偵測(self, 圖片路徑: str) -> list:
        """
        輸入：圖片路徑 (str)
        處理：模擬 DETR 偵測
        輸出：list[dict]
        """
        print(f"DETR (layers={self.編碼器層數}) 正在偵測: {圖片路徑}")
        return [{"class": "dog", "confidence": 0.92, "bbox": [200, 100, 350, 280]}]

    def 模型名稱(self) -> str:
        return f"DETR-L{self.編碼器層數}"


# --- 工廠 ---
class 偵測器工廠:
    """
    工廠模式 — 根據名稱建立對應的偵測器
    結合 Registry Pattern，新增偵測器只需 register + 實作類別
    """

    _偵測器表: Dict[str, Type[偵測器]] = {}

    @classmethod
    def 註冊(cls, 名稱: str, 偵測器類別: Type[偵測器]) -> None:
        """
        輸入：名稱(str), 偵測器類別(Type)
        處理：加入註冊表
        輸出：無
        """
        cls._偵測器表[名稱] = 偵測器類別

    @classmethod
    def 建立(cls, 名稱: str, **kwargs) -> 偵測器:
        """
        輸入：名稱(str), 建構參數(**kwargs)
        處理：從註冊表找到類別並實例化
        輸出：偵測器 — 對應的偵測器實例
        """
        if 名稱 not in cls._偵測器表:
            raise ValueError(
                f"未知偵測器: {名稱}，"
                f"可用: {list(cls._偵測器表.keys())}"
            )
        return cls._偵測器表[名稱](**kwargs)

    @classmethod
    def 列出所有(cls) -> list:
        """
        輸入：無
        處理：列出所有已註冊的偵測器
        輸出：list[str]
        """
        return list(cls._偵測器表.keys())

# 註冊偵測器
偵測器工廠.註冊("yolo", YOLO偵測器)
偵測器工廠.註冊("ssd", SSD偵測器)
偵測器工廠.註冊("detr", DETR偵測器)

# 使用工廠建立偵測器（使用者不需要知道具體類別）
print(f"可用偵測器: {偵測器工廠.列出所有()}")

模型 = 偵測器工廠.建立("yolo", 版本="v8")
結果 = 模型.偵測("photo.jpg")
print(f"模型: {模型.模型名稱()}, 結果: {結果}")

模型2 = 偵測器工廠.建立("detr", 編碼器層數=12)
結果2 = 模型2.偵測("photo.jpg")
print(f"模型: {模型2.模型名稱()}, 結果: {結果2}")

# 設定檔驅動建立（常見於生產系統）
設定 = {
    "detector": "ssd",
    "params": {"骨幹網路": "resnet50"}
}
模型3 = 偵測器工廠.建立(設定["detector"], **設定["params"])
print(f"從設定檔建立: {模型3.模型名稱()}")
```

---

## 總結對照表

| 主題 | Colab 等級 | 專案等級 |
|------|-----------|---------|
| 函式 | `def f(x):` | `*args`, `**kwargs`, 裝飾器, 閉包 |
| 類別 | `__init__` | 魔術方法, ABC, MRO, `__slots__` |
| 資料 | `class + __init__` | `@dataclass`, `frozen`, `__post_init__` |
| 型別 | 無標註 | `Type Hints` + `Generic` + `TypeVar` |
| 迭代 | `for x in list` | 生成器, `yield`, `itertools` |
| 資源 | `open()` / `close()` | `with` + 上下文管理器 |
| 錯誤 | `try/except` | 自定義例外層級, `raise from` |
| 模組 | `import x` | `__all__`, 延遲匯入, `__getattr__` |
| 架構 | 直接寫邏輯 | Registry, Observer, Factory 模式 |

> **下一集預告**：EP02 將深入 Python 的並行與非同步 —
> threading, multiprocessing, asyncio，以及 GPU 加速的前置知識。

---

*EP01 完 — Python 從入門到專案級別*
