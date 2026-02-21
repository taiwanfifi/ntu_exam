# EP03 — C++：NVIDIA / GPU 工程師必備語言

> **對象**：熟悉 Python 的開發者，準備跨入 C++ 與 CUDA 領域
> **目標**：用 Python 已知概念，快速建立 C++ 完整知識體系
> **原則**：每個函式皆標註 Input / Process / Output

---

## 目錄

1. [C++ vs Python 基本對照](#1-c-vs-python-基本對照)
2. [基本型別與運算](#2-基本型別與運算)
3. [指標與參考 (Pointers & References)](#3-指標與參考-pointers--references)
4. [函式](#4-函式)
5. [類別 (Classes)](#5-類別-classes)
6. [記憶體管理](#6-記憶體管理)
7. [STL 標準模板庫](#7-stl-標準模板庫)
8. [現代 C++ (C++11/14/17/20)](#8-現代-c-c11141720)
9. [CUDA 入門概念](#9-cuda-入門概念)
10. [編譯與建置](#10-編譯與建置)

---

## 1. C++ vs Python 基本對照

### 1.1 總覽對照表

| 特性 | Python | C++ |
|------|--------|-----|
| 型別系統 | 動態型別 | 靜態型別 |
| 執行方式 | 直譯 (Interpreter) | 編譯 (Compiler) |
| 記憶體管理 | 自動 GC | 手動 / Smart Pointer |
| 進入點 | 直接執行 | `main()` 函式 |
| 匯入模組 | `import` | `#include` |
| 輸出 | `print()` | `std::cout` |
| 速度 | 較慢 | 極快（接近硬體） |
| 分號 | 不需要 | 每行結尾必須 `;` |
| 大括號 | 用縮排 | 用 `{}` |

### 1.2 變數宣告

```python
# Python — 動態型別，不需宣告型別
x = 5
name = "Alice"
pi = 3.14
is_valid = True
```

```cpp
// C++ — 靜態型別，必須宣告型別
int x = 5;
std::string name = "Alice";
double pi = 3.14;
bool is_valid = true;
```

### 1.3 完整 Hello World 與編譯步驟

**Python 版本：**

```python
# hello.py
# Input:  無
# Process: 印出字串
# Output:  "Hello, World!"
print("Hello, World!")
```

```bash
python hello.py          # 直接執行，不需編譯
```

**C++ 版本：**

```cpp
// hello.cpp
// Input:  無
// Process: 透過 std::cout 輸出字串到標準輸出
// Output:  "Hello, World!"

#include <iostream>      // 引入輸入輸出函式庫（類似 import）

int main() {            // 程式進入點，一定要有 main()
    std::cout << "Hello, World!" << std::endl;
    return 0;            // 回傳 0 表示程式正常結束
}
```

```bash
# 編譯步驟
g++ -o hello hello.cpp   # 將 .cpp 編譯為可執行檔 hello
./hello                  # 執行編譯後的二進位檔
# 輸出: Hello, World!
```

### 1.4 #include vs import

```python
# Python
import math              # 匯入整個模組
from os import path      # 匯入特定功能
```

```cpp
// C++
#include <iostream>      // 標準函式庫用角括號 <>
#include <vector>        // STL 容器
#include <string>        // 字串
#include "myheader.h"    // 自己的標頭檔用雙引號 ""
```

### 1.5 std::cout vs print()

```python
# Python
name = "NVIDIA"
year = 2024
print(f"公司: {name}, 成立: {year}")    # f-string 格式化
```

```cpp
// C++
// Input:  字串與整數
// Process: 用 << 串接輸出
// Output:  格式化的字串到終端
#include <iostream>
#include <string>

int main() {
    std::string name = "NVIDIA";
    int year = 2024;
    std::cout << "公司: " << name << ", 成立: " << year << std::endl;
    return 0;
}
```

> **重點**：`<<` 是輸出運算子，可以連續串接不同型別的資料。`std::endl` 等同換行 `\n` 並清空緩衝區。

---

## 2. 基本型別與運算

### 2.1 基本型別對照表

| C++ 型別 | 大小 (bytes) | Python 對應 | 說明 |
|----------|-------------|------------|------|
| `int` | 4 | `int` | 整數 |
| `float` | 4 | `float`（低精度） | 單精度浮點 |
| `double` | 8 | `float` | 雙精度浮點（Python 預設） |
| `char` | 1 | `str`（單字元） | 單一字元 |
| `bool` | 1 | `bool` | 布林值 |
| `std::string` | 動態 | `str` | 字串 |
| `long long` | 8 | `int`（Python 無上限） | 長整數 |

### 2.2 型別範例

```cpp
// Input:  各種型別的值 | Process: 宣告初始化 | Output: 值與大小
#include <iostream>
#include <string>
int main() {
    int age = 30;                      // 4 bytes
    float salary_f = 50000.5f;         // 4 bytes，f 後綴
    double salary_d = 50000.123456;    // 8 bytes，預設浮點
    char grade = 'A';                  // 1 byte，單引號
    bool is_engineer = true;           // 1 byte
    std::string company = "NVIDIA";    // 動態大小，雙引號

    std::cout << "age: " << age << " (" << sizeof(age) << " bytes)" << std::endl;
    std::cout << "salary_d: " << salary_d << " (" << sizeof(salary_d) << " bytes)" << std::endl;
    std::cout << "company: " << company << std::endl;
    return 0;
}
```

### 2.3 auto 自動推斷

```cpp
// C++ 的 auto 讓編譯器自動推斷型別（C++11 起）
// 類似 Python 的動態型別，但型別在編譯時就確定了

auto x = 42;           // 推斷為 int
auto pi = 3.14;        // 推斷為 double
auto name = std::string("CUDA");  // 推斷為 std::string
auto flag = true;      // 推斷為 bool

// 注意：auto 一旦推斷後，型別就固定了
// x = "hello";        // 編譯錯誤！x 已經是 int
```

### 2.4 const vs constexpr

```python
# Python — 沒有真正的 const，只有慣例用全大寫
PI = 3.14159           # 只是慣例，其實可以被改
MAX_SIZE = 100
```

```cpp
// C++ — 編譯器強制保護
const double PI = 3.14159;       // 執行期常數，不可修改
constexpr int MAX_SIZE = 100;    // 編譯期常數，效能更好

// PI = 3.0;           // 編譯錯誤！不可修改 const
// MAX_SIZE = 200;     // 編譯錯誤！

// constexpr 要求值在編譯期就能確定
constexpr int square(int n) { return n * n; }
constexpr int result = square(5);  // 編譯期就算出 25
```

### 2.5 容器對照表

| Python | C++ | 特性 |
|--------|-----|------|
| `list` | `std::vector` | 動態陣列 |
| `tuple` | `std::tuple` / `std::array` | 固定大小 |
| `dict` | `std::map` / `std::unordered_map` | 鍵值對 |
| `set` | `std::set` / `std::unordered_set` | 不重複集合 |

### 2.6 陣列 vs vector vs array

```cpp
// Input:  一組整數
// Process: 用三種方式儲存並存取
// Output:  印出各容器內容

#include <iostream>
#include <vector>
#include <array>

int main() {
    // 1. C 風格陣列 — 固定大小，不安全（盡量別用）
    int c_arr[5] = {1, 2, 3, 4, 5};

    // 2. std::array — 固定大小，安全（C++11）
    std::array<int, 5> safe_arr = {10, 20, 30, 40, 50};

    // 3. std::vector — 動態大小，最常用（等同 Python list）
    std::vector<int> vec = {100, 200, 300};
    vec.push_back(400);       // 等同 Python list.append(400)
    vec.push_back(500);

    // 印出 vector
    std::cout << "vector 內容: ";
    for (int v : vec) {       // range-based for（類似 Python for v in vec）
        std::cout << v << " ";
    }
    std::cout << std::endl;
    std::cout << "vector 大小: " << vec.size() << std::endl;
    std::cout << "第一個元素: " << vec[0] << std::endl;
    std::cout << "最後一個元素: " << vec.back() << std::endl;

    return 0;
}
```

### 2.7 std::map、std::unordered_map、std::set

```cpp
// Input:  GPU 資料 | Process: map/set 操作 | Output: 查詢結果
#include <iostream>
#include <map>
#include <unordered_map>
#include <set>
#include <string>

int main() {
    // std::map — 有序（紅黑樹），O(log n)
    std::map<std::string, int> gpu_mem = {
        {"RTX 4090", 24}, {"A100", 80}, {"H100", 80}
    };
    gpu_mem["RTX 5090"] = 32;                       // 新增 (Python: dict[key] = val)

    for (const auto& [name, mem] : gpu_mem) {       // structured binding (C++17)
        std::cout << name << ": " << mem << " GB" << std::endl;
    }

    if (gpu_mem.count("A100") > 0) {                // 檢查 key 存在
        std::cout << "A100: " << gpu_mem["A100"] << " GB" << std::endl;
    }

    // std::unordered_map — 無序（雜湊表），O(1) 平均，更快
    std::unordered_map<std::string, double> bench = {{"training", 95.5}};

    // std::set — 有序不重複（等同 Python set，但有序）
    std::set<int> ids = {5, 3, 1, 3, 5, 7};   // 自動去重排序: {1, 3, 5, 7}
    ids.insert(2);                              // Python: set.add(2)
    ids.erase(3);                               // Python: set.remove(3)

    if (ids.find(7) != ids.end()) {
        std::cout << "7 存在於 set 中" << std::endl;
    }
    return 0;
}
```

---

## 3. 指標與參考 (Pointers & References)

> **這是 Python 開發者學 C++ 最關鍵的一章。** GPU 程式設計中，你必須直接操作記憶體地址。

### 3.1 記憶體模型圖解

```
Python 的世界:
    x = 42
    ┌──────┐     ┌──────────┐
    │  x   │────>│  42      │  Python 中 x 是「標籤」，指向物件
    └──────┘     │ (object) │  所有變數都是參考，你不知道地址
                 └──────────┘

C++ 的世界:
    int x = 42;
    記憶體地址:  0x7fff1234
    ┌──────────────────┐
    │  x = 42          │  x 直接擁有這塊記憶體
    │  地址: 0x7fff1234│  你可以知道並操作這個地址
    └──────────────────┘

    int* ptr = &x;     // ptr 儲存 x 的地址
    記憶體地址:  0x7fff5678
    ┌──────────────────┐     ┌──────────────────┐
    │  ptr = 0x7fff1234│────>│  x = 42          │
    │  地址: 0x7fff5678│     │  地址: 0x7fff1234│
    └──────────────────┘     └──────────────────┘
```

### 3.2 指標基礎：& 取地址、* 解參考

```cpp
// Input:  一個整數變數
// Process: 用指標存取其記憶體地址與值
// Output:  地址與值

#include <iostream>

int main() {
    int x = 42;

    // & 取地址運算子：取得變數的記憶體地址
    int* ptr = &x;   // ptr 是「指向 int 的指標」，儲存 x 的地址

    std::cout << "x 的值: " << x << std::endl;         // 42
    std::cout << "x 的地址: " << &x << std::endl;      // 0x7fff... (某個地址)
    std::cout << "ptr 的值: " << ptr << std::endl;      // 同上，ptr 儲存的就是 x 的地址
    std::cout << "*ptr 解參考: " << *ptr << std::endl;  // 42，透過地址取得值

    // 透過指標修改原始變數
    *ptr = 100;    // 把 ptr 指向的位置的值改為 100
    std::cout << "修改後 x: " << x << std::endl;  // 100（x 也變了！）

    return 0;
}
```

### 3.3 指標 vs 參考

| 特性 | 指標 `int* ptr = &x;` | 參考 `int& ref = x;` |
|------|----------------------|---------------------|
| 可以為空 | 可以 (`nullptr`) | 不行，必須初始化 |
| 重新綁定 | 可以 (`ptr = &y`) | 不行 |
| 取值語法 | 需要 `*ptr` | 直接用 `ref` |
| 運算 | 可以 (`ptr++`) | 不行 |
| 主要用途 | 動態記憶體、陣列 | 函式參數傳遞 |

```cpp
// Input: 整數 | Process: 指標與參考操作 | Output: 修改結果
#include <iostream>
int main() {
    int x = 10, y = 20;

    int* ptr = &x;  *ptr = 15;    // 透過指標修改 x → 15
    ptr = &y;       *ptr = 25;    // 改指向 y，修改 y → 25

    int& ref = x;   ref = 100;    // ref 是 x 的別名，x → 100
    // int& ref2;                 // 編譯錯誤！必須初始化

    std::cout << "x=" << x << " y=" << y << " ref=" << ref << std::endl;
    // 輸出: x=100 y=25 ref=100
    return 0;
}
```

### 3.4 nullptr

```cpp
// Input: 無 | Process: 空指標安全檢查 | Output: 檢查結果
#include <iostream>
int main() {
    int* ptr = nullptr;          // C++11 空指標（取代舊式 NULL）

    if (ptr != nullptr) {        // 使用前一定要檢查！
        std::cout << *ptr << std::endl;
    } else {
        std::cout << "指標為空，不能解參考！" << std::endl;
    }

    int x = 42;
    ptr = &x;
    if (ptr) {                   // 簡寫：非空即 true
        std::cout << "值: " << *ptr << std::endl;  // 42
    }
    return 0;
}
```

### 3.5 為什麼 Python 不需要指標

```python
# Python 中一切都是物件參考（類似 C++ 的指標，但被語言自動管理）
a = [1, 2, 3]
b = a            # b 和 a 指向同一個 list 物件（類似 C++ 指標）
b.append(4)
print(a)         # [1, 2, 3, 4]  — a 也被改了！

# Python 幫你隱藏了所有記憶體操作
# C++ 把這些操作暴露給你，讓你能精確控制
```

```
為什麼 GPU 程式需要指標？
─────────────────────────
1. GPU 有獨立記憶體（Device Memory），CPU 也有記憶體（Host Memory）
2. 你需要用指標指定：資料在 CPU 還是 GPU 上
3. cudaMalloc(&d_ptr, size) — 在 GPU 上配置記憶體，回傳指標
4. cudaMemcpy(d_ptr, h_ptr, size, ...) — 在 CPU 和 GPU 間複製資料
5. 沒有指標 → 無法進行 GPU 程式設計
```

### 3.6 完整記憶體圖解範例

```cpp
// Input: 多層指標 | Process: 展示記憶體布局 | Output: 各層地址與值
#include <iostream>
int main() {
    int value = 42;
    int* ptr1 = &value;    // 一級指標
    int** ptr2 = &ptr1;    // 二級指標（指標的指標）

    // 記憶體布局: ptr2 → ptr1 → value
    //            (存 ptr1 地址)  (存 value 地址)  (存 42)

    std::cout << "value: " << value << ", 地址: " << &value << std::endl;
    std::cout << "*ptr1: " << *ptr1 << std::endl;    // 42
    std::cout << "**ptr2: " << **ptr2 << std::endl;  // 42
    return 0;
}
```

---

## 4. 函式

### 4.1 值傳遞 vs 參考傳遞 vs 指標傳遞

```cpp
// Input:  一個整數
// Process: 用三種方式傳遞並嘗試修改
// Output:  觀察原始值是否被改變

#include <iostream>

// 方式一：值傳遞（Pass by Value）— 複製一份，原本不受影響
void by_value(int x) {
    x = 999;    // 只修改了複製品
}

// 方式二：參考傳遞（Pass by Reference）— 直接操作原本的變數
void by_reference(int& x) {
    x = 999;    // 直接修改原始變數
}

// 方式三：指標傳遞（Pass by Pointer）— 透過地址操作
void by_pointer(int* x) {
    *x = 999;   // 透過解參考修改原始變數
}

int main() {
    int a = 1, b = 1, c = 1;

    by_value(a);
    std::cout << "值傳遞後 a = " << a << std::endl;     // 1（沒變）

    by_reference(b);
    std::cout << "參考傳遞後 b = " << b << std::endl;   // 999（被改了）

    by_pointer(&c);
    std::cout << "指標傳遞後 c = " << c << std::endl;   // 999（被改了）

    return 0;
}
```

```python
# Python 對比：Python 用的是 "Pass by Object Reference"
def modify(lst):
    lst.append(4)    # 可以修改可變物件（list）

def reassign(x):
    x = 999          # 只是重新綁定本地變數，原始不受影響

my_list = [1, 2, 3]
modify(my_list)
print(my_list)       # [1, 2, 3, 4] — 被改了（類似 C++ 參考傳遞）

val = 42
reassign(val)
print(val)           # 42 — 沒變（int 是不可變物件）
```

### 4.2 函式重載 (Overloading)

```cpp
// Input: 不同型別/數量參數 | Process: 編譯器選版本 | Output: 各版本結果
#include <iostream>
#include <string>

// 同名函式，不同參數 — C++ 支援，Python 不支援
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
std::string add(std::string a, std::string b) { return a + b; }
int add(int a, int b, int c) { return a + b + c; }

int main() {
    std::cout << add(1, 2) << std::endl;          // int 版: 3
    std::cout << add(1.5, 2.5) << std::endl;      // double 版: 4.0
    std::cout << add(1, 2, 3) << std::endl;        // 三參數版: 6
    return 0;
}
// Python 沒有重載，用 *args 模擬: def add(*args): return sum(args)
```

### 4.3 預設參數與 inline

```cpp
// 預設參數（和 Python 相同概念，從右到左）
void connect(std::string host, int port = 8080, std::string proto = "https") {
    std::cout << proto << "://" << host << ":" << port << std::endl;
}
// connect("nvidia.com")           → https://nvidia.com:8080
// connect("nvidia.com", 443)      → https://nvidia.com:443

// inline: 建議編譯器展開函式，避免呼叫開銷（適用於短小函式）
inline int square(int x) { return x * x; }
```

### 4.5 template 函式模板

```cpp
// Input: 任意型別 | Process: 泛型比較 | Output: 較大值
#include <iostream>
#include <string>

template <typename T>                    // 對比 Python 鴨子型別 / Generic
T max_value(T a, T b) { return (a > b) ? a : b; }

template <typename T, typename U>        // 多型別模板
auto multiply(T a, U b) -> decltype(a * b) { return a * b; }

int main() {
    std::cout << max_value(10, 20) << std::endl;      // int: 20
    std::cout << max_value(3.14, 2.71) << std::endl;  // double: 3.14
    std::cout << multiply(3, 4.5) << std::endl;       // 13.5
    return 0;
}
// Python: def max_value(a, b): return a if a > b else b  # 天生支援
```

---

## 5. 類別 (Classes)

### 5.1 class vs struct

```cpp
// C++ 的 class 和 struct 幾乎一樣，唯一差異是預設存取權限
// struct: 預設 public
// class:  預設 private

struct Point {
    double x, y;     // 預設 public
};

class Vector3D {
    double x, y, z;  // 預設 private，外部不能直接存取
public:
    Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}
    double length() const;
};
```

### 5.2 完整的類別範例

```cpp
// Input: GPU 資訊 | Process: 類別操作 | Output: GPU 物件資訊
#include <iostream>
#include <string>

class GPU {
private:                                    // 私有成員
    std::string name_;
    int memory_gb_;
    int cuda_cores_;
public:
    // Constructor 建構子（等同 Python __init__）
    GPU(std::string name, int mem, int cores)
        : name_(name), memory_gb_(mem), cuda_cores_(cores) {   // 初始化列表
        std::cout << "GPU [" << name_ << "] 已建立" << std::endl;
    }
    ~GPU() { std::cout << "GPU [" << name_ << "] 已銷毀" << std::endl; }  // 解構子

    std::string get_name() const { return name_; }   // Getter
    void display() const {
        std::cout << name_ << " | " << memory_gb_ << "GB | "
                  << cuda_cores_ << " cores" << std::endl;
    }
    // this 指標（等同 Python self）
    GPU& upgrade_memory(int gb) { this->memory_gb_ += gb; return *this; }
};

int main() {
    GPU rtx("RTX 4090", 24, 16384);
    rtx.display();
    rtx.upgrade_memory(8).display();    // 鏈式呼叫
    return 0;
}   // 離開 main → 解構子自動呼叫
```

```python
# Python 對比
class GPU:
    def __init__(self, name, memory, cores):  # Constructor
        self.name = name       # Python 用 self，C++ 用 this
        self.memory = memory
    def __del__(self):         # Destructor（不保證何時呼叫）
        print(f"GPU [{self.name}] 已銷毀")
```

### 5.3 繼承與多型

```cpp
// Input: 不同裝置 | Process: 繼承+多型 | Output: 各裝置行為
#include <iostream>
#include <string>
#include <vector>
#include <memory>

class ComputeDevice {                                // 基底類別
protected:
    std::string name_;
    double tflops_;
public:
    ComputeDevice(std::string n, double t) : name_(n), tflops_(t) {}
    virtual ~ComputeDevice() = default;              // 虛擬解構子（重要！）
    virtual void compute() const {                   // virtual: 允許覆寫
        std::cout << name_ << ": 通用計算" << std::endl;
    }
    virtual std::string arch() const = 0;            // 純虛函式 = 0（必須實作）
};

class NvidiaGPU final : public ComputeDevice {       // final: 不可再繼承
    int cores_;
public:
    NvidiaGPU(std::string n, double t, int c) : ComputeDevice(n, t), cores_(c) {}
    void compute() const override {                  // override: 明確標示覆寫
        std::cout << name_ << ": CUDA (" << cores_ << " cores)" << std::endl;
    }
    std::string arch() const override { return "CUDA"; }
};

class AMDGPU : public ComputeDevice {
public:
    AMDGPU(std::string n, double t) : ComputeDevice(n, t) {}
    void compute() const override {
        std::cout << name_ << ": ROCm (" << tflops_ << " TFLOPS)" << std::endl;
    }
    std::string arch() const override { return "RDNA"; }
};

int main() {
    std::vector<std::unique_ptr<ComputeDevice>> devs;
    devs.push_back(std::make_unique<NvidiaGPU>("H100", 989.0, 16896));
    devs.push_back(std::make_unique<AMDGPU>("MI300X", 1307.0));
    for (const auto& d : devs) d->compute();         // 多型：自動選正確版本
    return 0;
}
```

```python
# Python 對比
from abc import ABC, abstractmethod
class ComputeDevice(ABC):
    @abstractmethod          # 等同 C++ 純虛函式 = 0
    def arch(self): pass
    def compute(self):       # 等同 C++ virtual（Python 天生支援覆寫）
        print(f"{self.name}: 通用計算")
```

### 5.4 運算子重載

```cpp
// Input: 兩向量 | Process: 重載 +, ==, << | Output: 運算結果
#include <iostream>
#include <cmath>

class Vec2 {
public:
    double x, y;
    Vec2(double x = 0, double y = 0) : x(x), y(y) {}

    Vec2 operator+(const Vec2& o) const { return {x + o.x, y + o.y}; }    // Python __add__
    bool operator==(const Vec2& o) const { return x == o.x && y == o.y; }  // Python __eq__
    friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {     // Python __repr__
        os << "Vec2(" << v.x << ", " << v.y << ")"; return os;
    }
};

int main() {
    Vec2 a(3, 4), b(1, 2), c = a + b;
    std::cout << a << " + " << b << " = " << c << std::endl;
    return 0;
}
```

```python
# Python 對比
class Vec2:
    def __init__(self, x=0, y=0): self.x, self.y = x, y
    def __add__(self, o): return Vec2(self.x + o.x, self.y + o.y)
    def __eq__(self, o): return self.x == o.x and self.y == o.y
    def __repr__(self): return f"Vec2({self.x}, {self.y})"
```

---

## 6. 記憶體管理

> **NVIDIA 面試高頻考點。** GPU 程式需要在 CPU 和 GPU 間手動管理記憶體。

### 6.1 Stack vs Heap

| 特性 | Stack（堆疊） | Heap（堆積） |
|------|--------------|-------------|
| 管理 | 自動（離開作用域釋放） | 手動（new/delete） |
| 速度 | 快 | 較慢 |
| 大小 | 有限（1-8 MB） | 只受系統記憶體限制 |
| 用途 | 局部變數 | 動態配置的資料 |

```cpp
// Input: 無 | Process: Stack vs Heap 對比 | Output: 變數位置與生命週期
#include <iostream>
int main() {
    int stack_var = 42;                          // Stack — 自動管理
    int* heap_var = new int(100);                // Heap — 手動管理
    int* arr = new int[5]{10, 20, 30, 40, 50};   // Heap 陣列

    std::cout << "Stack: " << stack_var << std::endl;
    std::cout << "Heap:  " << *heap_var << std::endl;

    delete heap_var;     // 釋放單一物件（不 delete = 記憶體洩漏！）
    delete[] arr;        // 釋放陣列（注意 delete[]）
    return 0;
}   // stack_var 在這裡自動釋放
```

### 6.2 Smart Pointers（智慧指標）

```cpp
// Input: 動態物件 | Process: Smart Pointer 管理 | Output: 自動釋放
#include <iostream>
#include <memory>
#include <string>

class GPUBuffer {
    std::string name_;
public:
    GPUBuffer(std::string n) : name_(n) { std::cout << "配置 " << name_ << std::endl; }
    ~GPUBuffer() { std::cout << "釋放 " << name_ << std::endl; }
    void process() const { std::cout << "處理 " << name_ << std::endl; }
};

int main() {
    // 1. unique_ptr — 獨占所有權（最常用，零開銷）
    {
        auto buf1 = std::make_unique<GPUBuffer>("vertex");
        buf1->process();
        // auto copy = buf1;              // 編譯錯誤！不能複製
        auto moved = std::move(buf1);     // 可以移動所有權
    } // moved 離開作用域 → 自動 delete

    // 2. shared_ptr — 共享所有權（引用計數）
    {
        auto buf2 = std::make_shared<GPUBuffer>("texture");
        std::cout << "引用計數: " << buf2.use_count() << std::endl;  // 1
        {
            auto copy = buf2;             // 共享，引用計數 → 2
        }                                 // copy 離開，引用計數 → 1
    } // buf2 離開，引用計數 → 0，自動 delete

    // 3. weak_ptr — 弱參考（不增加引用計數，避免循環參考）
    std::weak_ptr<GPUBuffer> weak;
    {
        auto buf3 = std::make_shared<GPUBuffer>("index");
        weak = buf3;
        if (auto locked = weak.lock()) locked->process();  // 成功
    } // buf3 被釋放
    std::cout << "已過期? " << weak.expired() << std::endl;  // 1 (true)

    return 0;
}
```

### 6.3 Smart Pointer 選擇指南

```
你需要共享所有權嗎？
    ├── 否 → unique_ptr（預設選擇，零開銷）
    └── 是 → shared_ptr
              └── 需要避免循環參考？ → weak_ptr
```

### 6.4 RAII 原則

```
RAII = Resource Acquisition Is Initialization
       資源取得即初始化

核心思想：
  - 在建構子中取得資源（配置記憶體、開啟檔案、取得鎖）
  - 在解構子中釋放資源（釋放記憶體、關閉檔案、釋放鎖）
  - 利用 C++ 的作用域規則，保證資源一定會被釋放

Python 對比：
  - Python 用 context manager (with 語句) 達成類似效果
  - with open('file.txt') as f:  ← 這就是 RAII 精神
```

```cpp
// RAII 範例：建構子取得資源，解構子釋放資源
class FileReader {
    std::ifstream file_;
public:
    FileReader(const std::string& path) : file_(path) {}   // 建構 → 開啟
    ~FileReader() { if (file_.is_open()) file_.close(); }   // 解構 → 關閉
};
// 離開作用域時自動呼叫解構子，保證資源一定被釋放
```

### 6.5 為什麼 GPU 程式需要手動管理記憶體

```
Host (CPU RAM) ◄──── PCIe Bus ────► Device (GPU VRAM)

流程：new → cudaMalloc → cudaMemcpy(H→D) → kernel<<<>>>()
      → cudaMemcpy(D→H) → cudaFree → delete

Python 對比：tensor.to('cuda') 底層就是 cudaMalloc + cudaMemcpy
```

---

## 7. STL 標準模板庫

### 7.1 常用容器速查

| 容器 | 底層結構 | 存取 | 插入/刪除 | Python 對應 |
|------|---------|------|----------|------------|
| `vector` | 動態陣列 | O(1) 隨機 | 尾部 O(1) | `list` |
| `list` | 雙向鏈結串列 | O(n) | 任意 O(1) | `collections.deque` |
| `deque` | 雙端佇列 | O(1) 隨機 | 頭尾 O(1) | `collections.deque` |
| `map` | 紅黑樹 | O(log n) | O(log n) | `dict`（有序） |
| `unordered_map` | 雜湊表 | O(1) 平均 | O(1) 平均 | `dict` |
| `set` | 紅黑樹 | O(log n) | O(log n) | `set`（有序） |

### 7.2 algorithm 常用演算法

```cpp
// Input: 一組數字 | Process: STL algorithm | Output: 處理結果
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int main() {
    std::vector<int> nums = {5, 3, 8, 1, 9, 2, 7, 4, 6};

    // sort（Python: sorted / list.sort）
    std::sort(nums.begin(), nums.end());

    // find（Python: list.index / in）
    auto it = std::find(nums.begin(), nums.end(), 7);
    if (it != nums.end())
        std::cout << "7 在位置: " << std::distance(nums.begin(), it) << std::endl;

    // transform（Python: map）
    std::vector<int> doubled(nums.size());
    std::transform(nums.begin(), nums.end(), doubled.begin(),
                   [](int x) { return x * 2; });

    // accumulate（Python: sum）
    int total = std::accumulate(nums.begin(), nums.end(), 0);

    // count_if（Python: sum(1 for x in lst if cond)）
    int evens = std::count_if(nums.begin(), nums.end(),
                               [](int x) { return x % 2 == 0; });

    // any_of / all_of（Python: any / all）
    bool all_pos = std::all_of(nums.begin(), nums.end(), [](int x) { return x > 0; });

    std::cout << "總和: " << total << " 偶數: " << evens
              << " 全正? " << all_pos << std::endl;
    return 0;
}
```

### 7.3 迭代器 (Iterator) 與 list comprehension 對比

```python
# Python list comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

```cpp
// C++ 沒有 list comprehension，但可以用 STL 組合達成
// Input:  0 到 9 的數字
// Process: 篩選偶數並平方
// Output:  結果 vector

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // 方法：先產生範圍，再用 algorithm 處理
    std::vector<int> range(10);
    std::iota(range.begin(), range.end(), 0);  // 填入 0,1,2,...,9

    std::vector<int> squares;
    for (int x : range) {
        if (x % 2 == 0) {
            squares.push_back(x * x);
        }
    }

    for (int s : squares) {
        std::cout << s << " ";    // 0 4 16 36 64
    }
    std::cout << std::endl;

    return 0;
}
```

---

## 8. 現代 C++ (C++11/14/17/20)

### 8.1 Lambda 表達式

```cpp
// Input: 數字集合 | Process: lambda 操作 | Output: 處理結果
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // 語法: [捕獲列表](參數) -> 回傳型別 { 本體 }
    auto add = [](int a, int b) -> int { return a + b; };
    std::cout << "3+4 = " << add(3, 4) << std::endl;

    // [=] 值捕獲（複製外部變數）
    int multiplier = 3;
    auto times = [=](int x) { return x * multiplier; };

    // [&] 參考捕獲（可修改外部變數）
    int counter = 0;
    auto inc = [&counter]() { counter++; };
    inc(); inc();
    std::cout << "counter = " << counter << std::endl;  // 2

    // 搭配 STL 使用
    std::vector<int> nums = {5, 2, 8, 1, 9, 3};
    std::sort(nums.begin(), nums.end(),
              [](int a, int b) { return a > b; });      // 降冪排序

    std::vector<int> big;
    std::copy_if(nums.begin(), nums.end(), std::back_inserter(big),
                 [](int x) { return x > 5; });          // 篩選 > 5
    return 0;
}
```

```python
# Python 對比（lambda 只能單行，C++ lambda 可以多行）
add = lambda a, b: a + b
sorted_nums = sorted([5,2,8,1,9,3], key=lambda x: -x)
big = list(filter(lambda x: x > 5, [5,2,8,1,9,3]))
```

### 8.2 std::optional 與 std::variant

```cpp
// Input: 查詢 | Process: optional 處理空值 | Output: 安全結果
#include <iostream>
#include <optional>
#include <variant>
#include <string>
#include <map>

// optional — 等同 Python Optional[T]（可能有值也可能是 None）
std::optional<int> find_gpu_mem(const std::string& name) {
    std::map<std::string, int> db = {{"RTX 4090", 24}, {"A100", 80}};
    auto it = db.find(name);
    if (it != db.end()) return it->second;
    return std::nullopt;            // 等同 Python return None
}

int main() {
    auto r = find_gpu_mem("A100");
    if (r.has_value()) std::cout << "A100: " << r.value() << " GB" << std::endl;

    auto m = find_gpu_mem("RTX 9090");
    std::cout << "RTX 9090: " << m.value_or(-1) << " GB" << std::endl;  // -1

    // variant — 類型安全聯合（等同 Python Union[int, str, float]）
    std::variant<int, double, std::string> val;
    val = 42;       std::cout << std::get<int>(val) << std::endl;
    val = 3.14;     std::cout << std::get<double>(val) << std::endl;
    val = std::string("CUDA");

    std::visit([](auto&& arg) { std::cout << arg << std::endl; }, val);
    return 0;
}
```

### 8.3 Structured Bindings（結構化綁定，C++17）

```cpp
// Input: 結構化資料 | Process: 解構 | Output: 個別值
#include <iostream>
#include <map>
#include <tuple>
#include <string>

std::tuple<std::string, int, double> get_gpu_info() {
    return {"H100", 80, 989.5};   // 回傳多個值
}

int main() {
    // 解構 tuple（等同 Python: name, mem, perf = get_gpu_info()）
    auto [name, memory, tflops] = get_gpu_info();
    std::cout << name << ": " << memory << "GB, " << tflops << " TFLOPS" << std::endl;

    // 解構 map 元素
    std::map<std::string, int> prices = {{"RTX 4090", 1599}, {"RTX 4080", 1199}};
    for (const auto& [gpu, price] : prices)
        std::cout << gpu << ": $" << price << std::endl;

    return 0;
}
```

### 8.4 move 語義與右值參考

```cpp
// Input: 大型資料 | Process: move 轉移所有權 | Output: 高效轉移
#include <iostream>
#include <vector>
#include <utility>

int main() {
    std::vector<int> big(1000000, 42);     // 一百萬個元素
    // std::vector<int> copy = big;         // 複製 O(n)，慢！

    std::vector<int> moved = std::move(big); // 移動 O(1)，只轉移指標
    std::cout << "moved: " << moved.size() << std::endl;  // 1000000
    std::cout << "big: " << big.size() << std::endl;      // 0（已清空）
    return 0;
}
```

```
move 核心概念：
- 左值 (lvalue)：有名字有地址（int x = 5 中的 x）
- 右值 (rvalue)：臨時無名（5、x+y 的結果）
- std::move()：「我不再需要這個了，偷走它的資源」
- Python 對比：Python 的 = 只建立新參考，不複製也不移動
```

---

## 9. CUDA 入門概念

> **這一章是 NVIDIA 工程師的核心知識。** 理解 Host/Device 模型是 GPU 程式設計的基礎。

### 9.1 Host vs Device

```
Host (CPU)                          Device (GPU)
┌─────────────────┐  PCIe/NVLink  ┌─────────────────┐
│ 主程式 (C++)     │ ◄──────────► │ Kernel 函式      │
│ 序列執行         │               │ 數千執行緒平行   │
│ 記憶體: RAM      │               │ 記憶體: VRAM     │
└─────────────────┘               └─────────────────┘
```

### 9.2 CUDA 關鍵字

| 關鍵字 | 執行位置 | 呼叫位置 | 說明 |
|--------|---------|---------|------|
| `__global__` | Device (GPU) | Host (CPU) | Kernel 函式，程式入口 |
| `__device__` | Device (GPU) | Device (GPU) | 只能在 GPU 上呼叫的函式 |
| `__host__` | Host (CPU) | Host (CPU) | 一般 CPU 函式（預設） |

### 9.3 Grid, Block, Thread 階層

```
Grid（網格）
├── Block(0)           Block(1)           Block(2)
│   [T0][T1][T2]...   [T0][T1][T2]...   [T0][T1][T2]...

threadIdx.x = 執行緒在 Block 內的索引
blockIdx.x  = Block 在 Grid 內的索引
blockDim.x  = 每個 Block 的執行緒數

全域索引 = blockIdx.x * blockDim.x + threadIdx.x
```

### 9.4 記憶體管理函式

| CUDA API | 對應操作 | 方向 |
|----------|---------|------|
| `cudaMalloc(&ptr, size)` | `new`（在 GPU 上） | - |
| `cudaFree(ptr)` | `delete`（GPU 記憶體） | - |
| `cudaMemcpy(dst, src, size, H2D)` | `memcpy` | CPU → GPU |
| `cudaMemcpy(dst, src, size, D2H)` | `memcpy` | GPU → CPU |

### 9.5 完整向量加法範例

```cuda
// vector_add.cu
// Input:  兩個等長的浮點數向量 A 和 B
// Process: 在 GPU 上平行計算 C[i] = A[i] + B[i]
// Output:  結果向量 C

#include <iostream>
#include <cstdlib>

// Kernel 函式 — 在 GPU 上執行，每個執行緒處理一個元素
__global__ void vector_add(const float* A, const float* B, float* C, int N) {
    // 計算全域執行緒索引
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // 邊界檢查（執行緒數可能超過陣列大小）
    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

int main() {
    const int N = 1000000;                  // 一百萬個元素
    const int SIZE = N * sizeof(float);     // 位元組大小

    // ============ 第一步：在 Host (CPU) 上配置記憶體 ============
    float* h_A = new float[N];    // h_ 前綴表示 host
    float* h_B = new float[N];
    float* h_C = new float[N];

    // 初始化資料
    for (int i = 0; i < N; i++) {
        h_A[i] = static_cast<float>(i);
        h_B[i] = static_cast<float>(i * 2);
    }

    // ============ 第二步：在 Device (GPU) 上配置記憶體 ============
    float* d_A;    // d_ 前綴表示 device
    float* d_B;
    float* d_C;
    cudaMalloc(&d_A, SIZE);
    cudaMalloc(&d_B, SIZE);
    cudaMalloc(&d_C, SIZE);

    // ============ 第三步：將資料從 CPU 複製到 GPU ============
    cudaMemcpy(d_A, h_A, SIZE, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, SIZE, cudaMemcpyHostToDevice);

    // ============ 第四步：啟動 Kernel（GPU 計算） ============
    int threads_per_block = 256;                                  // 每個 Block 256 個執行緒
    int blocks_per_grid = (N + threads_per_block - 1) / threads_per_block;  // 向上取整

    // <<<blocks, threads>>> 是 CUDA 特殊語法
    vector_add<<<blocks_per_grid, threads_per_block>>>(d_A, d_B, d_C, N);

    // 等待 GPU 完成
    cudaDeviceSynchronize();

    // ============ 第五步：將結果從 GPU 複製回 CPU ============
    cudaMemcpy(h_C, d_C, SIZE, cudaMemcpyDeviceToHost);

    // ============ 第六步：驗證結果 ============
    bool correct = true;
    for (int i = 0; i < N; i++) {
        if (h_C[i] != h_A[i] + h_B[i]) {
            correct = false;
            break;
        }
    }
    std::cout << "結果: " << (correct ? "正確" : "錯誤") << std::endl;

    // ============ 第七步：釋放記憶體 ============
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    delete[] h_A;
    delete[] h_B;
    delete[] h_C;

    return 0;
}
```

```python
# Python (PyTorch) 對比 — 底層就是在做上面的事
import torch

A = torch.arange(1000000, dtype=torch.float32)
B = torch.arange(1000000, dtype=torch.float32) * 2

# .to('cuda') 底層 = cudaMalloc + cudaMemcpy H→D
A_gpu = A.to('cuda')
B_gpu = B.to('cuda')

# GPU 計算（底層 = kernel launch）
C_gpu = A_gpu + B_gpu

# .cpu() 底層 = cudaMemcpy D→H
C = C_gpu.cpu()
# 離開作用域後 GPU 記憶體自動回收
```

### 9.6 為什麼 NVIDIA 需要 C++

| 原因 | 說明 |
|------|------|
| 效能 | GPU 驅動、CUDA Runtime 都是 C++，Python 太慢無法寫 kernel |
| 硬體控制 | 需要指標操作記憶體、精確控制執行緒同步 |
| 生態系統 | CUDA Toolkit、cuDNN、TensorRT、PyTorch 核心都是 C++ |
| 職位要求 | GPU Arch / CUDA / DL Framework / Driver 工程師皆需 C++ |

---

## 10. 編譯與建置

### 10.1 g++ 基本編譯

```bash
g++ -o program main.cpp                     # 基本編譯
g++ -std=c++17 -o program main.cpp          # 指定 C++17 標準
g++ -O2 -o program main.cpp                 # 開啟最佳化（O0/O2/O3）
g++ -Wall -Wextra -std=c++17 -o prog main.cpp  # 開啟所有警告
g++ -g -std=c++17 -o program main.cpp       # 除錯資訊（搭配 gdb）
g++ -std=c++17 -o prog main.cpp gpu.cpp     # 多檔案編譯
g++ -std=c++17 -o prog main.cpp -lpthread   # 連結外部函式庫
```

### 10.2 標頭檔 .h vs 實作檔 .cpp

```
project/
├── include/gpu.h        ← 宣告（介面）
├── src/gpu.cpp          ← 實作
├── src/main.cpp         ← 主程式
├── CMakeLists.txt       ← 建置設定
└── build/               ← 編譯輸出
```

```cpp
// include/gpu.h — 標頭檔（宣告介面）
#ifndef GPU_H              // Include Guard：防止重複引入
#define GPU_H
#include <string>
class GPU {
    std::string name_;
    int memory_gb_;
public:
    GPU(std::string name, int memory);
    void display() const;
};
#endif
```

```cpp
// src/gpu.cpp — 實作檔
#include "gpu.h"
#include <iostream>
GPU::GPU(std::string name, int mem) : name_(name), memory_gb_(mem) {}
void GPU::display() const {
    std::cout << name_ << " (" << memory_gb_ << " GB)" << std::endl;
}

// src/main.cpp
// #include "gpu.h"
// int main() { GPU rtx("RTX 4090", 24); rtx.display(); }
// Python 對比：不分標頭檔/實作檔，from gpu import GPU 等同 #include
```

### 10.3 CMakeLists.txt 基礎

```cmake
# CMakeLists.txt
# Input:  專案的原始碼與設定
# Process: 自動產生 Makefile 或其他建置系統的設定
# Output:  可編譯的建置檔

cmake_minimum_required(VERSION 3.18)
project(GPUProject LANGUAGES CXX)

# 設定 C++ 標準
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 新增可執行檔
add_executable(gpu_app
    src/main.cpp
    src/gpu.cpp
)

# 指定標頭檔目錄
target_include_directories(gpu_app PRIVATE include/)

# 開啟警告
target_compile_options(gpu_app PRIVATE -Wall -Wextra)
```

```bash
# 用 CMake 建置
mkdir build && cd build
cmake ..                  # 產生 Makefile
make                      # 編譯
./gpu_app                 # 執行
```

### 10.4 nvcc CUDA 編譯器

```bash
# nvcc 把 GPU 程式碼交給 GPU 編譯器，CPU 程式碼交給 g++
nvcc -o vector_add vector_add.cu                   # 基本編譯
nvcc -arch=sm_89 -o vec vector_add.cu              # RTX 40 系列
nvcc -arch=sm_90 -o vec vector_add.cu              # H100
nvcc -std=c++17 -O2 -o vec vector_add.cu           # C++17 + 最佳化
```

---

## 附錄：C++ 與 Python 完整對照速查表

| 功能 | Python | C++ |
|------|--------|-----|
| 印出 | `print("hi")` | `std::cout << "hi" << std::endl;` |
| 輸入 | `x = input()` | `std::cin >> x;` |
| 字串格式化 | `f"值={x}"` | `std::cout << "值=" << x;` |
| 條件式 | `if x > 0:` | `if (x > 0) {` |
| 迴圈 | `for i in range(n):` | `for (int i = 0; i < n; i++) {` |
| range for | `for x in lst:` | `for (auto& x : lst) {` |
| while | `while cond:` | `while (cond) {` |
| 函式 | `def f(x):` | `int f(int x) {` |
| 類別 | `class C:` | `class C {` |
| 建構子 | `__init__(self)` | `C() {` |
| 繼承 | `class B(A):` | `class B : public A {` |
| 抽象方法 | `@abstractmethod` | `virtual void f() = 0;` |
| 例外 | `try/except` | `try/catch` |
| 空值 | `None` | `nullptr` |
| 列表 | `[1,2,3]` | `std::vector<int>{1,2,3}` |
| 字典 | `{"a":1}` | `std::map<str,int>{{"a",1}}` |
| 集合 | `{1,2,3}` | `std::set<int>{1,2,3}` |
| 排序 | `sorted(lst)` | `std::sort(v.begin(), v.end())` |
| 長度 | `len(lst)` | `v.size()` |
| 新增 | `lst.append(x)` | `v.push_back(x)` |
| Lambda | `lambda x: x*2` | `[](int x){ return x*2; }` |
| 型別提示 | `x: int = 5` | `int x = 5;` |
| 模組 | `import os` | `#include <filesystem>` |
| 套件管理 | `pip` | `vcpkg / conan / CMake` |
| 測試 | `pytest` | `Google Test / Catch2` |

---

> **下一步**：EP04 將深入 CUDA 平行程式設計實戰，涵蓋 Shared Memory、Warp、Stream 等進階主題。
