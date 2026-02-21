# EP05 — Go 語言：高效並發程式設計

> **對象讀者**：有 Python 經驗的開發者，想快速掌握 Go 語言
> **核心定位**：從 Python 思維無縫切換到 Go 思維，重點掌握並發模型
> **Go 版本**：1.21+（含泛型語法）

---

## 目錄

1. [Go vs Python 基本對照](#1-go-vs-python-基本對照)
2. [基本型別與資料結構](#2-基本型別與資料結構)
3. [函式](#3-函式)
4. [Struct 與方法](#4-struct-與方法)
5. [Interface — Go 最重要概念](#5-interface--go-最重要概念)
6. [並發程式設計 — Go 殺手級特色](#6-並發程式設計--go-殺手級特色)
7. [錯誤處理](#7-錯誤處理)
8. [套件管理](#8-套件管理)
9. [常用標準庫](#9-常用標準庫)
10. [泛型 (Go 1.18+)](#10-泛型-go-118)
11. [完整迷你專案：REST API](#11-完整迷你專案rest-api)

---

## 1. Go vs Python 基本對照

### 1.1 第一支程式：Hello World

**Python 版本：**

```python
# hello.py — 直接執行即可
print("Hello, World!")
```

**Go 版本：**

```go
// hello.go — 必須宣告 package 與 main 函式
package main          // 每個 Go 檔案必須屬於一個 package；可執行程式用 main

import "fmt"          // 匯入標準庫的 fmt（格式化輸出）

func main() {         // 程式進入點，不接受參數，不回傳值
    fmt.Println("Hello, World!")   // 印出並換行
}
```

**執行方式：**

```bash
# 方式一：直接執行（編譯 + 執行合一）
go run hello.go

# 方式二：先編譯再執行（產生二進位檔）
go build -o hello hello.go
./hello
```

> **關鍵差異**：Go 是編譯型語言，產出的二進位檔不需要 runtime 環境。Python 是直譯型，需要 Python 直譯器。

### 1.2 變數宣告

```go
package main

import "fmt"

func main() {
    // --- 方式一：完整宣告 ---
    var x int = 5            // Python: x = 5（Python 不需要宣告型別）
    var name string = "Go"   // Python: name = "Go"
    var pi float64 = 3.14    // Python: pi = 3.14
    var active bool = true   // Python: active = True

    // --- 方式二：型別推斷 ---
    var y = 10               // 編譯器自動推斷 y 為 int

    // --- 方式三：短變數宣告（最常用，只能在函式內） ---
    z := 20                  // 等同 var z int = 20
    greeting := "你好"       // 等同 var greeting string = "你好"

    // --- 多重宣告 ---
    var a, b, c int = 1, 2, 3
    d, e := "hello", 42

    fmt.Println(x, name, pi, active)  // 5 Go 3.14 true
    fmt.Println(y, z, greeting)       // 10 20 你好
    fmt.Println(a, b, c)              // 1 2 3
    fmt.Println(d, e)                 // hello 42
}
```

### 1.3 常數與 iota

```go
package main

import "fmt"

// 常數：編譯期確定，不可修改
const Pi = 3.14159
const AppName = "MyApp"

// iota：自動遞增的常數產生器（Python 沒有對應功能）
type Weekday int

const (
    Sunday    Weekday = iota  // 0
    Monday                    // 1（自動遞增）
    Tuesday                   // 2
    Wednesday                 // 3
    Thursday                  // 4
    Friday                    // 5
    Saturday                  // 6
)

func main() {
    fmt.Println(Pi)        // 3.14159
    fmt.Println(Monday)    // 1
    fmt.Println(Friday)    // 5
}
```

### 1.4 控制流程

```go
package main

import "fmt"

func main() {
    // --- if/else（不需要括號） ---
    score := 85
    if score >= 90 {           // Python: if score >= 90:
        fmt.Println("優秀")
    } else if score >= 70 {    // Python: elif score >= 70:
        fmt.Println("良好")
    } else {
        fmt.Println("加油")
    }

    // --- if 帶初始化語句（Go 獨有） ---
    if x := 10 * 2; x > 15 {
        fmt.Println("x 大於 15, x =", x)  // x 只在此 if 區塊可見
    }

    // --- for 迴圈（Go 只有 for，沒有 while） ---
    // 傳統 for
    for i := 0; i < 5; i++ {          // Python: for i in range(5):
        fmt.Println(i)
    }

    // while 風格
    count := 0
    for count < 3 {                    // Python: while count < 3:
        fmt.Println(count)
        count++
    }

    // 無限迴圈
    // for {                           // Python: while True:
    //     break
    // }

    // range 迭代
    fruits := []string{"蘋果", "香蕉", "芒果"}
    for index, fruit := range fruits { // Python: for i, fruit in enumerate(fruits):
        fmt.Printf("  %d: %s\n", index, fruit)
    }

    // --- switch（比 Python 的 match/case 更早存在） ---
    day := "Monday"
    switch day {
    case "Monday":
        fmt.Println("星期一，加油！")
    case "Friday":
        fmt.Println("星期五，快放假了！")
    default:
        fmt.Println("普通的一天")
    }
}
```

### 1.5 對照總覽表

| 概念 | Python | Go |
|------|--------|----|
| 進入點 | 直接執行 / `if __name__ == "__main__"` | `func main()` |
| 變數宣告 | `x = 5` | `x := 5` 或 `var x int = 5` |
| 印出 | `print()` | `fmt.Println()` |
| 型別 | 動態型別 | 靜態型別 |
| 分號 | 不需要 | 不需要（編譯器自動插入） |
| 大括號 | 用縮排 | 用 `{}` |
| 套件匯入 | `import os` | `import "os"` |
| 未使用的變數 | 警告 | **編譯錯誤** |
| 未使用的匯入 | 警告 | **編譯錯誤** |

---

## 2. 基本型別與資料結構

### 2.1 基本型別

```go
package main

import "fmt"

func main() {
    // --- 整數型別 ---
    var a int = 42          // 平台相關（32 或 64 位元）
    var b int8 = 127        // -128 ~ 127
    var c int64 = 9999999   // 64 位元整數
    var d uint = 100        // 無號整數（>= 0）

    // --- 浮點數 ---
    var pi float64 = 3.14159   // Python 的 float 等同 Go 的 float64
    var e float32 = 2.71       // 32 位元浮點數

    // --- 字串 ---
    var name string = "Go 語言"       // 字串是不可變的（同 Python）
    char := name[0]                    // byte 型別，不是 rune！

    // --- bool ---
    var active bool = true    // Python: True（首字母大寫）

    // --- byte 與 rune ---
    var letter byte = 'A'    // byte = uint8，ASCII 字元
    var emoji rune = '🚀'    // rune = int32，Unicode 碼點（類似 Python 的 chr/ord）

    fmt.Println(a, b, c, d)
    fmt.Println(pi, e)
    fmt.Println(name, char)  // char 會印出數字（byte 值）
    fmt.Println(active)
    fmt.Println(letter, emoji)
    fmt.Printf("letter=%c, emoji=%c\n", letter, emoji)  // %c 印出字元

    // --- 零值（zero value）：Go 不需要初始化 ---
    var zeroInt int       // 0
    var zeroStr string    // ""（空字串）
    var zeroBool bool     // false
    fmt.Println(zeroInt, zeroStr, zeroBool)
}
```

### 2.2 Array 與 Slice

```go
package main

import "fmt"

func main() {
    // === Array（固定長度，很少直接使用） ===
    // Input: 宣告固定大小陣列
    // Process: 存取元素
    // Output: 印出陣列內容
    var arr [3]int = [3]int{10, 20, 30}  // Python 沒有固定長度 array
    fmt.Println("Array:", arr)
    fmt.Println("長度:", len(arr))        // 3
    arr[0] = 99
    fmt.Println("修改後:", arr)           // [99 20 30]

    // === Slice（動態長度，最常用，對應 Python list） ===
    // Input: 建立 slice
    // Process: append 新增元素
    // Output: 印出 slice 與其容量

    // 方式一：字面值
    fruits := []string{"蘋果", "香蕉", "芒果"}  // Python: fruits = ["蘋果", "香蕉", "芒果"]

    // 方式二：make 建立（預分配容量）
    scores := make([]int, 0, 10)  // 長度 0，容量 10

    // append 新增元素
    fruits = append(fruits, "西瓜")            // Python: fruits.append("西瓜")
    scores = append(scores, 95, 88, 72)        // 一次加多個

    fmt.Println("fruits:", fruits)              // [蘋果 香蕉 芒果 西瓜]
    fmt.Println("scores:", scores)              // [95 88 72]
    fmt.Println("len:", len(scores))            // 3
    fmt.Println("cap:", cap(scores))            // 10（預分配的容量）

    // --- 切片操作（與 Python 幾乎相同） ---
    nums := []int{0, 1, 2, 3, 4, 5}
    fmt.Println(nums[1:4])   // [1 2 3]   Python: nums[1:4]
    fmt.Println(nums[:3])    // [0 1 2]   Python: nums[:3]
    fmt.Println(nums[3:])    // [3 4 5]   Python: nums[3:]
    // 注意：Go 沒有負數索引！nums[-1] 會編譯錯誤

    // --- 遍歷 ---
    for i, v := range fruits {
        fmt.Printf("  [%d] %s\n", i, v)
    }

    // 只需要值，忽略索引
    for _, v := range fruits {
        fmt.Println(" ", v)
    }
}
```

### 2.3 Map（對應 Python dict）

```go
package main

import "fmt"

func main() {
    // === 建立 Map ===
    // Input: 鍵值對資料
    // Process: CRUD 操作
    // Output: 印出 map 內容

    // 方式一：字面值
    ages := map[string]int{      // Python: ages = {"Alice": 30, "Bob": 25}
        "Alice": 30,
        "Bob":   25,
    }

    // 方式二：make
    scores := make(map[string]float64)

    // --- 新增 / 修改 ---
    ages["Charlie"] = 35         // Python: ages["Charlie"] = 35
    scores["數學"] = 95.5

    // --- 讀取 ---
    aliceAge := ages["Alice"]    // 30
    fmt.Println("Alice:", aliceAge)

    // --- 檢查 key 是否存在（Go 獨有的 comma ok 慣用法） ---
    value, exists := ages["Dave"]   // Python: ages.get("Dave", None)
    if exists {
        fmt.Println("Dave:", value)
    } else {
        fmt.Println("Dave 不存在")  // 會印出這行
    }

    // --- 刪除 ---
    delete(ages, "Bob")             // Python: del ages["Bob"]

    // --- 遍歷 ---
    for key, val := range ages {    // Python: for key, val in ages.items():
        fmt.Printf("  %s: %d\n", key, val)
    }

    fmt.Println("Map 長度:", len(ages))  // Python: len(ages)
}
```

### 2.4 Struct（對應 Python class / dataclass）

```go
package main

import "fmt"

// === 定義 Struct ===
// Python 等價：
// @dataclass
// class Person:
//     name: str
//     age: int
//     email: str

type Person struct {
    Name  string   // 首字母大寫 = 公開（exported）
    Age   int
    Email string
}

func main() {
    // --- 建立實例 ---
    // Input: 欄位值
    // Process: 初始化 struct
    // Output: Person 實例

    // 方式一：具名欄位
    p1 := Person{
        Name:  "Alice",
        Age:   30,
        Email: "alice@example.com",
    }

    // 方式二：按順序
    p2 := Person{"Bob", 25, "bob@example.com"}

    // 方式三：零值初始化
    var p3 Person  // Name="", Age=0, Email=""

    // --- 存取欄位 ---
    fmt.Println(p1.Name)    // Alice     Python: p1.name
    p3.Name = "Charlie"
    p3.Age = 35

    fmt.Println(p1)  // {Alice 30 alice@example.com}
    fmt.Println(p2)  // {Bob 25 bob@example.com}
    fmt.Println(p3)  // {Charlie 35 }

    // --- 指標 ---
    ptr := &p1                  // 取得 p1 的指標
    fmt.Println(ptr.Name)       // Alice（Go 自動解引用）
    ptr.Age = 31                // 修改原始值
    fmt.Println(p1.Age)         // 31
}
```

---

## 3. 函式

### 3.1 基本函式與多回傳值

```go
package main

import (
    "fmt"
    "math"
)

// --- 基本函式 ---
// Input: a, b 兩個整數
// Process: 相加
// Output: 回傳整數總和
func add(a int, b int) int {   // Python: def add(a, b): return a + b
    return a + b
}

// --- 多回傳值（Go 的招牌特色） ---
// Input: a, b 兩個整數
// Process: 同時計算商和餘數
// Output: 回傳商（int）與餘數（int）
func divide(a, b int) (int, int) {  // Python: def divide(a, b): return a // b, a % b
    return a / b, a % b
}

// --- 具名回傳值（named return） ---
// Input: 半徑 r
// Process: 計算圓面積與周長
// Output: area（面積）、circumference（周長）
func circleInfo(r float64) (area float64, circumference float64) {
    area = math.Pi * r * r
    circumference = 2 * math.Pi * r
    return  // 裸 return，自動回傳具名變數
}

func main() {
    sum := add(3, 5)
    fmt.Println("3 + 5 =", sum)  // 8

    quotient, remainder := divide(17, 5)
    fmt.Println("17 / 5 =", quotient, "餘", remainder)  // 3 餘 2

    area, circ := circleInfo(5.0)
    fmt.Printf("半徑 5 的圓：面積=%.2f, 周長=%.2f\n", area, circ)
}
```

### 3.2 錯誤處理模式：error 型別

```go
package main

import (
    "errors"
    "fmt"
    "strconv"
)

// --- 回傳 error（Go 的核心慣用法） ---
// Input: 被除數 a、除數 b
// Process: 檢查除數是否為零，計算商
// Output: 計算結果或錯誤
func safeDivide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("除數不能為零")  // Python: raise ValueError("...")
    }
    return a / b, nil  // nil = Python 的 None
}

func main() {
    // --- 基本錯誤處理 ---
    result, err := safeDivide(10, 3)
    if err != nil {                         // Go 的核心模式：if err != nil
        fmt.Println("錯誤:", err)
    } else {
        fmt.Printf("10 / 3 = %.2f\n", result)  // 3.33
    }

    // 除以零的情況
    result, err = safeDivide(10, 0)
    if err != nil {
        fmt.Println("錯誤:", err)           // 錯誤: 除數不能為零
    }

    // --- 標準庫的錯誤處理範例 ---
    num, err := strconv.Atoi("abc")         // 字串轉整數
    if err != nil {
        fmt.Println("轉換失敗:", err)       // 轉換失敗: strconv.Atoi: parsing "abc": invalid syntax
    }
    fmt.Println(num)  // 0（錯誤時的零值）
}
```

### 3.3 defer, panic, recover

```go
package main

import "fmt"

// --- defer：延遲執行，函式結束前才執行（LIFO 順序） ---
// Input: 無
// Process: 示範 defer 的執行順序
// Output: 印出執行順序
func demoDefer() {
    fmt.Println("開始")
    defer fmt.Println("defer 1")  // 最後執行（第二個 defer 之後）
    defer fmt.Println("defer 2")  // 倒數第二執行
    fmt.Println("結束")
    // 輸出順序：開始 → 結束 → defer 2 → defer 1
}

// --- panic + recover：類似 Python 的 raise + try/except ---
// Input: 無
// Process: 觸發 panic 並用 recover 捕捉
// Output: 捕捉到的錯誤訊息
func safePanic() {
    defer func() {
        if r := recover(); r != nil {        // recover() 捕捉 panic
            fmt.Println("捕捉到 panic:", r)  // Python: except Exception as e:
        }
    }()

    fmt.Println("即將 panic...")
    panic("出大事了！")                       // Python: raise Exception("出大事了！")
    // 這行不會執行
}

func main() {
    demoDefer()
    fmt.Println("---")
    safePanic()
    fmt.Println("程式繼續執行")  // panic 被 recover 捕捉，不會中斷
}
```

### 3.4 函式作為參數與閉包

```go
package main

import "fmt"

// --- 函式作為參數（First-class functions） ---
// Input: slice、過濾函式
// Process: 遍歷 slice，用 fn 過濾
// Output: 符合條件的新 slice
func filter(nums []int, fn func(int) bool) []int {
    // Python 等價：list(filter(fn, nums))
    result := []int{}
    for _, n := range nums {
        if fn(n) {
            result = append(result, n)
        }
    }
    return result
}

// --- 閉包（Closure） ---
// Input: 初始值
// Process: 回傳一個函式，每次呼叫累加
// Output: 累加器函式
func makeCounter(start int) func() int {
    // Python 等價：
    // def make_counter(start):
    //     count = start
    //     def counter():
    //         nonlocal count
    //         count += 1
    //         return count
    //     return counter
    count := start
    return func() int {
        count++
        return count
    }
}

// --- map 操作 ---
// Input: int slice、轉換函式
// Process: 對每個元素套用轉換
// Output: 轉換後的新 slice
func mapSlice(nums []int, fn func(int) int) []int {
    result := make([]int, len(nums))
    for i, n := range nums {
        result[i] = fn(n)
    }
    return result
}

func main() {
    nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    // 過濾偶數
    evens := filter(nums, func(n int) bool {
        return n%2 == 0
    })
    fmt.Println("偶數:", evens)  // [2 4 6 8 10]

    // 每個元素平方
    squared := mapSlice(nums, func(n int) int {
        return n * n
    })
    fmt.Println("平方:", squared)  // [1 4 9 16 25 36 49 64 81 100]

    // 閉包計數器
    counter := makeCounter(0)
    fmt.Println(counter())  // 1
    fmt.Println(counter())  // 2
    fmt.Println(counter())  // 3
}
```

---

## 4. Struct 與方法

### 4.1 方法定義：值接收器 vs 指標接收器

```go
package main

import "fmt"

type Rectangle struct {
    Width  float64
    Height float64
}

// --- 值接收器（value receiver）：不修改原始值 ---
// Input: Rectangle 的副本
// Process: 計算面積
// Output: 面積 float64
func (r Rectangle) Area() float64 {
    // Python 等價：def area(self): return self.width * self.height
    return r.Width * r.Height
}

// --- 值接收器：回傳描述字串 ---
// Input: Rectangle 的副本
// Process: 格式化字串
// Output: 描述字串
func (r Rectangle) String() string {
    return fmt.Sprintf("Rectangle(%.1f x %.1f)", r.Width, r.Height)
}

// --- 指標接收器（pointer receiver）：修改原始值 ---
// Input: Rectangle 的指標
// Process: 按比例縮放寬高
// Output: 修改原始 struct（無回傳值）
func (r *Rectangle) Scale(factor float64) {
    // Python 等價：def scale(self, factor): self.width *= factor
    r.Width *= factor
    r.Height *= factor
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}

    fmt.Println(rect.String())      // Rectangle(10.0 x 5.0)
    fmt.Println("面積:", rect.Area()) // 50

    rect.Scale(2)                    // 寬高都乘以 2
    fmt.Println(rect.String())      // Rectangle(20.0 x 10.0)
    fmt.Println("面積:", rect.Area()) // 200
}
```

> **何時用指標接收器？**
> 1. 需要修改原始 struct
> 2. struct 很大（避免複製開銷）
> 3. 一致性：如果任一方法用指標，全部都用指標

### 4.2 組合取代繼承（Composition over Inheritance）

```go
package main

import "fmt"

// === Python 風格：繼承 ===
// class Animal:
//     def __init__(self, name): self.name = name
//     def speak(self): pass
// class Dog(Animal):
//     def speak(self): return "汪汪"

// === Go 風格：組合（Composition） ===

type Animal struct {
    Name string
}

// Input: Animal 的副本
// Process: 格式化介紹
// Output: 介紹字串
func (a Animal) Introduce() string {
    return fmt.Sprintf("我是 %s", a.Name)
}

type Dog struct {
    Animal           // 嵌入（embedding）— 類似繼承但不是繼承
    Breed  string
}

// Input: Dog 的副本
// Process: 回傳叫聲
// Output: 叫聲字串
func (d Dog) Speak() string {
    return "汪汪！"
}

type Cat struct {
    Animal
    Indoor bool
}

// Input: Cat 的副本
// Process: 回傳叫聲
// Output: 叫聲字串
func (c Cat) Speak() string {
    return "喵喵～"
}

func main() {
    dog := Dog{
        Animal: Animal{Name: "小白"},
        Breed:  "柴犬",
    }
    cat := Cat{
        Animal: Animal{Name: "小花"},
        Indoor: true,
    }

    // 嵌入的方法可以直接呼叫（promoted methods）
    fmt.Println(dog.Introduce())  // 我是 小白（來自 Animal）
    fmt.Println(dog.Speak())      // 汪汪！（Dog 自己的方法）
    fmt.Println(dog.Name)         // 小白（直接存取嵌入的欄位）

    fmt.Println(cat.Introduce())  // 我是 小花
    fmt.Println(cat.Speak())      // 喵喵～
}
```

### 4.3 更實際的組合範例

```go
package main

import (
    "fmt"
    "time"
)

// --- 基礎元件 ---
type Logger struct{}

// Input: 日誌訊息
// Process: 加上時間戳印出
// Output: 格式化日誌到標準輸出
func (l Logger) Log(msg string) {
    fmt.Printf("[%s] %s\n", time.Now().Format("15:04:05"), msg)
}

type Validator struct{}

// Input: email 字串
// Process: 基本格式檢查
// Output: 是否合法
func (v Validator) IsValidEmail(email string) bool {
    for _, ch := range email {
        if ch == '@' {
            return true
        }
    }
    return false
}

// --- 組合多個元件 ---
type UserService struct {
    Logger              // 嵌入 Logger
    Validator           // 嵌入 Validator
    users map[string]string
}

// Input: 使用者名稱與 email
// Process: 驗證 email、記錄日誌、新增使用者
// Output: 錯誤（如果有）
func (s *UserService) AddUser(name, email string) error {
    if !s.IsValidEmail(email) {     // 直接呼叫 Validator 的方法
        s.Log("無效的 email: " + email)  // 直接呼叫 Logger 的方法
        return fmt.Errorf("無效的 email: %s", email)
    }
    s.users[name] = email
    s.Log("新增使用者: " + name)
    return nil
}

func main() {
    svc := &UserService{
        users: make(map[string]string),
    }
    svc.AddUser("Alice", "alice@example.com")  // 成功
    svc.AddUser("Bob", "invalid-email")         // 失敗
}
```

---

## 5. Interface — Go 最重要概念

### 5.1 隱式實作（Implicit Implementation）

```go
package main

import (
    "fmt"
    "math"
)

// === 定義 Interface ===
// Python 等價：
// from abc import ABC, abstractmethod
// class Shape(ABC):
//     @abstractmethod
//     def area(self) -> float: pass
//     @abstractmethod
//     def perimeter(self) -> float: pass

type Shape interface {
    Area() float64
    Perimeter() float64
}

// === Circle 實作 Shape（不需要宣告 "implements"） ===
type Circle struct {
    Radius float64
}

// Input: Circle 副本
// Process: 計算圓面積
// Output: 面積
func (c Circle) Area() float64 {
    return math.Pi * c.Radius * c.Radius
}

// Input: Circle 副本
// Process: 計算圓周長
// Output: 周長
func (c Circle) Perimeter() float64 {
    return 2 * math.Pi * c.Radius
}

// === Square 實作 Shape ===
type Square struct {
    Side float64
}

func (s Square) Area() float64 {
    return s.Side * s.Side
}

func (s Square) Perimeter() float64 {
    return 4 * s.Side
}

// --- 接受 interface 的函式 ---
// Input: 任何實作 Shape 的型別
// Process: 印出面積與周長
// Output: 格式化資訊到標準輸出
func printShapeInfo(s Shape) {
    fmt.Printf("  面積: %.2f\n", s.Area())
    fmt.Printf("  周長: %.2f\n", s.Perimeter())
}

func main() {
    shapes := []Shape{        // 多型！不同型別放在同一個 slice
        Circle{Radius: 5},
        Square{Side: 4},
    }

    for _, s := range shapes {
        fmt.Printf("圖形: %T\n", s)   // %T 印出型別名稱
        printShapeInfo(s)
    }
}
```

> **關鍵差異**：Python 用 duck typing（有方法就行），Go 也是 duck typing 但在**編譯期**檢查。不需要寫 `implements` 關鍵字。

### 5.2 空介面與型別斷言

```go
package main

import "fmt"

// --- 空介面 interface{} 或 any（Go 1.18+） ---
// 可以持有任何型別的值（類似 Python 的動態型別）

// Input: 任何型別的值
// Process: 用 type switch 判斷型別
// Output: 型別描述字串
func describe(val any) string {
    // Python 等價：
    // if isinstance(val, int): ...
    // elif isinstance(val, str): ...

    switch v := val.(type) {    // type switch
    case int:
        return fmt.Sprintf("整數: %d", v)
    case float64:
        return fmt.Sprintf("浮點數: %.2f", v)
    case string:
        return fmt.Sprintf("字串: %q（長度 %d）", v, len(v))
    case bool:
        return fmt.Sprintf("布林: %t", v)
    case []int:
        return fmt.Sprintf("整數切片: %v（長度 %d）", v, len(v))
    default:
        return fmt.Sprintf("未知型別: %T", v)
    }
}

func main() {
    // --- type switch ---
    fmt.Println(describe(42))
    fmt.Println(describe(3.14))
    fmt.Println(describe("Go 語言"))
    fmt.Println(describe(true))
    fmt.Println(describe([]int{1, 2, 3}))

    fmt.Println("---")

    // --- 型別斷言（Type Assertion） ---
    var val any = "Hello, Go!"

    // 安全的型別斷言（comma ok 模式）
    str, ok := val.(string)
    if ok {
        fmt.Println("是字串:", str)
    }

    // 不安全的型別斷言（失敗會 panic）
    // num := val.(int)  // panic: interface conversion

    // 安全做法
    num, ok := val.(int)
    if !ok {
        fmt.Println("不是整數！零值:", num)  // num = 0
    }
}
```

### 5.3 io.Reader 與 io.Writer：Go 介面設計的經典

```go
package main

import (
    "fmt"
    "io"
    "os"
    "strings"
)

// io.Reader 介面定義（標準庫）：
// type Reader interface {
//     Read(p []byte) (n int, err error)
// }

// io.Writer 介面定義（標準庫）：
// type Writer interface {
//     Write(p []byte) (n int, err error)
// }

// --- 自定義 Writer ---
type UpperWriter struct {
    Writer io.Writer
}

// Input: 位元組切片
// Process: 轉大寫後寫入底層 Writer
// Output: 寫入的位元組數與錯誤
func (uw UpperWriter) Write(p []byte) (int, error) {
    upper := strings.ToUpper(string(p))
    return uw.Writer.Write([]byte(upper))
}

func main() {
    // strings.NewReader 實作了 io.Reader
    reader := strings.NewReader("Hello, Go 語言！")

    // 從 reader 讀取到 stdout
    // io.Copy 接受 (Writer, Reader)，展示介面的威力
    fmt.Println("--- 正常輸出 ---")
    io.Copy(os.Stdout, reader)
    fmt.Println()

    // 使用自定義 UpperWriter
    fmt.Println("--- 大寫輸出 ---")
    reader2 := strings.NewReader("Hello, Go interface!\n")
    upperOut := UpperWriter{Writer: os.Stdout}
    io.Copy(upperOut, reader2)
}
```

---

## 6. 並發程式設計 — Go 殺手級特色

### 6.1 Goroutine 基礎

```go
package main

import (
    "fmt"
    "time"
)

// Input: 任務 ID、執行次數
// Process: 模擬工作（sleep）
// Output: 印出進度到標準輸出
func worker(id int, count int) {
    for i := 0; i < count; i++ {
        fmt.Printf("Worker %d: 第 %d 次工作\n", id, i+1)
        time.Sleep(100 * time.Millisecond)
    }
    fmt.Printf("Worker %d: 完成！\n", id)
}

func main() {
    // Python 等價（threading）：
    // import threading
    // t = threading.Thread(target=worker, args=(1, 3))
    // t.start()

    // Go：只需要加 go 關鍵字！
    go worker(1, 3)   // 啟動 goroutine 1
    go worker(2, 3)   // 啟動 goroutine 2
    go worker(3, 3)   // 啟動 goroutine 3

    // 主程式等待（暫時用 Sleep，後面會用 WaitGroup）
    time.Sleep(1 * time.Second)
    fmt.Println("全部完成")
}
```

> **Goroutine vs Thread**：一個 goroutine 只佔約 2KB 記憶體（thread 約 1MB）。可以輕鬆開啟百萬個 goroutine。

### 6.2 Channel：Goroutine 間的通訊

```go
package main

import "fmt"

func main() {
    // === Unbuffered Channel（無緩衝） ===
    // 發送與接收必須同時準備好（同步通訊）

    // Input: 建立 channel
    // Process: 一個 goroutine 發送，主程式接收
    // Output: 接收到的值

    ch := make(chan string)    // Python 沒有直接對應，類似 queue.Queue

    go func() {
        ch <- "Hello from goroutine!"  // 發送到 channel
    }()

    msg := <-ch                         // 從 channel 接收（阻塞直到有資料）
    fmt.Println(msg)                    // Hello from goroutine!

    // === Buffered Channel（有緩衝） ===
    // 緩衝區滿之前，發送不會阻塞

    // Input: 建立容量為 3 的緩衝 channel
    // Process: 連續發送多個值
    // Output: 依序接收

    buffered := make(chan int, 3)  // 緩衝容量 3
    buffered <- 10
    buffered <- 20
    buffered <- 30
    // buffered <- 40  // 這會阻塞！因為緩衝已滿

    fmt.Println(<-buffered)  // 10（FIFO）
    fmt.Println(<-buffered)  // 20
    fmt.Println(<-buffered)  // 30

    // === Channel 搭配 range ===
    // Input: 整數 channel
    // Process: goroutine 發送後關閉，主程式用 range 接收
    // Output: 所有值

    numbers := make(chan int)
    go func() {
        for i := 1; i <= 5; i++ {
            numbers <- i
        }
        close(numbers)  // 關閉 channel，range 才會結束
    }()

    for n := range numbers {  // 持續接收直到 channel 關閉
        fmt.Println("收到:", n)
    }
}
```

### 6.3 Select：多路 Channel 選擇

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // === select：同時等待多個 channel ===
    // Python 等價：asyncio.wait + FIRST_COMPLETED

    // Input: 兩個不同速度的 channel
    // Process: select 等待第一個就緒的 channel
    // Output: 先完成的結果

    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(200 * time.Millisecond)
        ch1 <- "來自 ch1"
    }()

    go func() {
        time.Sleep(100 * time.Millisecond)
        ch2 <- "來自 ch2"
    }()

    // select 會執行第一個就緒的 case
    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-ch1:
            fmt.Println("ch1:", msg1)
        case msg2 := <-ch2:
            fmt.Println("ch2:", msg2)
        }
    }

    // === select + timeout ===
    // Input: 可能很慢的操作
    // Process: 設定超時
    // Output: 結果或超時訊息

    slowCh := make(chan string)
    go func() {
        time.Sleep(2 * time.Second)
        slowCh <- "慢操作完成"
    }()

    select {
    case result := <-slowCh:
        fmt.Println(result)
    case <-time.After(500 * time.Millisecond):
        fmt.Println("超時！操作花太久了")
    }
}
```

### 6.4 sync.WaitGroup：等待所有 Goroutine 完成

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Input: 任務 ID、WaitGroup 指標
// Process: 模擬工作後通知完成
// Output: 印出進度
func downloadFile(id int, wg *sync.WaitGroup) {
    defer wg.Done()  // 函式結束時通知 WaitGroup（計數器 -1）

    fmt.Printf("下載檔案 %d...\n", id)
    time.Sleep(time.Duration(id*100) * time.Millisecond)  // 模擬下載
    fmt.Printf("檔案 %d 下載完成！\n", id)
}

func main() {
    // Python 等價：
    // with concurrent.futures.ThreadPoolExecutor() as executor:
    //     futures = [executor.submit(download, i) for i in range(5)]
    //     concurrent.futures.wait(futures)

    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1)              // 計數器 +1
        go downloadFile(i, &wg)
    }

    wg.Wait()                  // 阻塞直到計數器歸零
    fmt.Println("所有檔案下載完成！")
}
```

### 6.5 sync.Mutex：互斥鎖

```go
package main

import (
    "fmt"
    "sync"
)

// --- 安全的計數器 ---
type SafeCounter struct {
    mu    sync.Mutex       // 互斥鎖
    count map[string]int
}

// Input: key 字串
// Process: 加鎖、遞增、解鎖
// Output: 無（修改內部狀態）
func (c *SafeCounter) Increment(key string) {
    c.mu.Lock()            // Python: with lock:
    defer c.mu.Unlock()    //     ... (自動解鎖)
    c.count[key]++
}

// Input: key 字串
// Process: 加鎖、讀取、解鎖
// Output: 計數值
func (c *SafeCounter) Get(key string) int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count[key]
}

func main() {
    counter := SafeCounter{count: make(map[string]int)}
    var wg sync.WaitGroup

    // 1000 個 goroutine 同時遞增
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment("visits")
        }()
    }

    wg.Wait()
    fmt.Println("最終計數:", counter.Get("visits"))  // 一定是 1000
}
```

### 6.6 完整範例：並行下載器

```go
package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

// DownloadResult 儲存下載結果
type DownloadResult struct {
    URL      string
    Size     int
    Duration time.Duration
    Err      error
}

// Input: URL 字串、結果 channel
// Process: 模擬 HTTP 下載（隨機耗時與大小）
// Output: 結果送入 channel
func download(url string, results chan<- DownloadResult) {
    start := time.Now()

    // 模擬下載（實際場景用 net/http）
    sleepMs := rand.Intn(500) + 100
    time.Sleep(time.Duration(sleepMs) * time.Millisecond)

    size := rand.Intn(10000) + 1000

    results <- DownloadResult{
        URL:      url,
        Size:     size,
        Duration: time.Since(start),
        Err:      nil,
    }
}

// Input: URL 列表、最大並行數
// Process: 用 goroutine pool 並行下載
// Output: 所有下載結果
func parallelDownload(urls []string, maxConcurrency int) []DownloadResult {
    results := make(chan DownloadResult, len(urls))
    semaphore := make(chan struct{}, maxConcurrency)  // 控制並行數
    var wg sync.WaitGroup

    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            semaphore <- struct{}{}        // 取得信號量（佔一個位置）
            download(u, results)
            <-semaphore                    // 釋放信號量
        }(url)
    }

    // 等待所有下載完成後關閉 channel
    go func() {
        wg.Wait()
        close(results)
    }()

    // 收集結果
    var allResults []DownloadResult
    for r := range results {
        allResults = append(allResults, r)
    }
    return allResults
}

func main() {
    urls := []string{
        "https://example.com/file1.zip",
        "https://example.com/file2.zip",
        "https://example.com/file3.zip",
        "https://example.com/file4.zip",
        "https://example.com/file5.zip",
        "https://example.com/file6.zip",
        "https://example.com/file7.zip",
        "https://example.com/file8.zip",
    }

    fmt.Printf("開始下載 %d 個檔案（最多 3 個並行）...\n", len(urls))
    start := time.Now()

    results := parallelDownload(urls, 3)

    totalSize := 0
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("  [失敗] %s: %v\n", r.URL, r.Err)
        } else {
            fmt.Printf("  [完成] %s — %d bytes, %v\n", r.URL, r.Size, r.Duration)
            totalSize += r.Size
        }
    }
    fmt.Printf("全部完成！總大小: %d bytes, 總耗時: %v\n", totalSize, time.Since(start))
}
```

### 6.7 Go 並發 vs Python 並發對照表

| 概念 | Go | Python |
|------|-----|--------|
| 輕量執行緒 | `go func()` (goroutine) | `threading.Thread` / `asyncio.create_task` |
| 通訊 | `chan` (channel) | `queue.Queue` / `asyncio.Queue` |
| 等待全部完成 | `sync.WaitGroup` | `concurrent.futures.wait()` |
| 互斥鎖 | `sync.Mutex` | `threading.Lock` |
| 多路選擇 | `select` | `asyncio.wait(FIRST_COMPLETED)` |
| 並行數控制 | buffered channel (semaphore) | `asyncio.Semaphore` |
| 記憶體模型 | 「不要用共享記憶體通訊；用通訊來共享記憶體」 | GIL 限制真正的平行 |

---

## 7. 錯誤處理

### 7.1 error interface 與自定義錯誤

```go
package main

import (
    "errors"
    "fmt"
)

// error 介面的定義（標準庫）：
// type error interface {
//     Error() string
// }

// === 自定義錯誤型別 ===
// Python 等價：
// class ValidationError(Exception):
//     def __init__(self, field, message):
//         self.field = field
//         self.message = message

type ValidationError struct {
    Field   string
    Message string
}

// 實作 error 介面
func (e *ValidationError) Error() string {
    return fmt.Sprintf("驗證錯誤 [%s]: %s", e.Field, e.Message)
}

// === 哨兵錯誤（Sentinel Errors） ===
var (
    ErrNotFound     = errors.New("找不到資源")
    ErrUnauthorized = errors.New("未授權")
    ErrInternal     = errors.New("內部錯誤")
)

// Input: 使用者 ID
// Process: 模擬資料庫查詢
// Output: 使用者名稱或錯誤
func findUser(id int) (string, error) {
    switch id {
    case 1:
        return "Alice", nil
    case 2:
        return "Bob", nil
    case -1:
        return "", &ValidationError{Field: "id", Message: "ID 不能為負數"}
    default:
        return "", fmt.Errorf("使用者 %d: %w", id, ErrNotFound)  // %w 包裝錯誤
    }
}

func main() {
    // --- 基本錯誤處理 ---
    name, err := findUser(1)
    if err != nil {
        fmt.Println("錯誤:", err)
    } else {
        fmt.Println("找到:", name)  // 找到: Alice
    }

    // --- errors.Is：檢查錯誤鏈中是否包含特定錯誤 ---
    // Python 等價：except NotFoundError:
    _, err = findUser(99)
    if errors.Is(err, ErrNotFound) {
        fmt.Println("使用者不存在")  // 使用者不存在
    }

    // --- errors.As：提取特定型別的錯誤 ---
    // Python 等價：except ValidationError as e:
    _, err = findUser(-1)
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Println("欄位:", valErr.Field)      // 欄位: id
        fmt.Println("訊息:", valErr.Message)     // 訊息: ID 不能為負數
    }
}
```

### 7.2 錯誤包裝與解包

```go
package main

import (
    "errors"
    "fmt"
    "os"
)

// Input: 檔案路徑
// Process: 開啟檔案、讀取內容
// Output: 內容位元組或包裝後的錯誤
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // %w 動詞：包裝原始錯誤（保留錯誤鏈）
        return nil, fmt.Errorf("讀取設定檔 %s 失敗: %w", path, err)
    }
    return data, nil
}

// Input: 無
// Process: 讀取設定、初始化應用
// Output: 包裝後的錯誤
func initApp() error {
    _, err := readConfig("/nonexistent/config.yaml")
    if err != nil {
        return fmt.Errorf("應用初始化失敗: %w", err)
    }
    return nil
}

func main() {
    err := initApp()
    if err != nil {
        fmt.Println("錯誤:", err)
        // 錯誤: 應用初始化失敗: 讀取設定檔 /nonexistent/config.yaml 失敗: open ...

        // 用 errors.Is 檢查底層錯誤
        if errors.Is(err, os.ErrNotExist) {
            fmt.Println("→ 原因：檔案不存在")
        }

        // 用 errors.Unwrap 逐層解包
        unwrapped := errors.Unwrap(err)
        fmt.Println("解包一層:", unwrapped)
    }
}
```

### 7.3 Go vs Python 錯誤處理對照

```
┌─────────────────────────────────────────────────────────┐
│  Python                    │  Go                        │
├────────────────────────────┼────────────────────────────┤
│  try:                      │  result, err := doSth()    │
│      result = do_sth()     │  if err != nil {           │
│  except ValueError as e:   │      // 處理錯誤           │
│      # 處理錯誤            │  }                         │
│  except Exception as e:    │                            │
│      # 處理其他錯誤        │                            │
│  finally:                  │  defer cleanup()           │
│      cleanup()             │                            │
├────────────────────────────┼────────────────────────────┤
│  raise ValueError("msg")   │  return errors.New("msg")  │
│  raise from original_err   │  fmt.Errorf("...: %w",err) │
│  isinstance(e, TypeError)  │  errors.As(err, &target)   │
└─────────────────────────────────────────────────────────┘
```

---

## 8. 套件管理

### 8.1 Go Modules 基礎

```bash
# === 初始化專案（對應 Python: pip init / poetry init） ===
mkdir myproject
cd myproject
go mod init github.com/yourname/myproject

# 產生的 go.mod 檔案：
# module github.com/yourname/myproject
# go 1.21

# === 安裝第三方套件（對應 Python: pip install） ===
go get github.com/gin-gonic/gin            # 安裝 Gin web framework
go get github.com/go-sql-driver/mysql       # MySQL 驅動

# === 整理依賴（移除未使用的） ===
go mod tidy                                 # 對應 Python: pip freeze > requirements.txt

# === 執行 ===
go run .        # 執行當前目錄的 main package
go build .      # 編譯當前目錄
go test ./...   # 執行所有測試
```

### 8.2 專案目錄結構

```
myproject/
├── go.mod                  # Python: requirements.txt / pyproject.toml
├── go.sum                  # Python: pip freeze 的 hash 版（自動產生）
├── main.go                 # 進入點
├── internal/               # 私有套件（外部專案不能匯入）
│   ├── auth/
│   │   └── auth.go
│   └── database/
│       └── db.go
├── pkg/                    # 公開套件（可被外部匯入）
│   └── utils/
│       └── helpers.go
├── handlers/               # HTTP 處理器
│   └── user.go
└── models/                 # 資料模型
    └── user.go
```

### 8.3 套件匯入與可見性

```go
package main

import (
    // 標準庫
    "fmt"
    "strings"

    // 第三方套件
    // "github.com/gin-gonic/gin"

    // 專案內部套件
    // "github.com/yourname/myproject/internal/auth"
    // "github.com/yourname/myproject/models"
)

// 大寫開頭 = 公開（exported）— Python: 不加底線
// 小寫開頭 = 私有（unexported）— Python: 加底線 _private

type User struct {
    Name  string  // 公開：其他套件可存取
    email string  // 私有：只有同套件可存取
}

func main() {
    s := strings.ToUpper("hello")
    fmt.Println(s)
}
```

### 8.4 Go vs Python 套件管理對照

| 功能 | Go | Python |
|------|-----|--------|
| 初始化 | `go mod init` | `pip init` / `poetry init` |
| 依賴檔 | `go.mod` | `requirements.txt` / `pyproject.toml` |
| 鎖定檔 | `go.sum`（自動） | `poetry.lock` / `pip freeze` |
| 安裝套件 | `go get` | `pip install` |
| 虛擬環境 | 不需要（每專案獨立） | `python -m venv` |
| 私有模組 | `internal/` 目錄 | `_` 前綴慣例 |
| 執行 | `go run .` | `python main.py` |

---

## 9. 常用標準庫

### 9.1 fmt / strings / strconv

```go
package main

import (
    "fmt"
    "strconv"
    "strings"
)

func main() {
    // === fmt：格式化輸出 ===
    name := "Go"
    version := 1.21
    fmt.Println("Hello", name)                          // Hello Go
    fmt.Printf("版本: %.1f\n", version)                 // 版本: 1.2
    formatted := fmt.Sprintf("%s v%.1f", name, version) // 不印出，回傳字串
    fmt.Println(formatted)                               // Go v1.2

    // === strings：字串操作（對應 Python str 方法） ===
    s := "Hello, Go 語言!"
    fmt.Println(strings.Contains(s, "Go"))      // true   Python: "Go" in s
    fmt.Println(strings.HasPrefix(s, "Hello"))   // true   Python: s.startswith("Hello")
    fmt.Println(strings.HasSuffix(s, "!"))       // true   Python: s.endswith("!")
    fmt.Println(strings.ToUpper(s))              // HELLO, GO 語言!
    fmt.Println(strings.Replace(s, "Go", "Golang", 1))  // Python: s.replace(...)
    fmt.Println(strings.Split("a,b,c", ","))     // [a b c]  Python: "a,b,c".split(",")
    fmt.Println(strings.Join([]string{"a","b","c"}, "-")) // a-b-c  Python: "-".join([...])
    fmt.Println(strings.TrimSpace("  hello  "))  // hello   Python: "  hello  ".strip()

    // === strconv：型別轉換（Python: int(), str(), float()） ===
    numStr := "42"
    num, err := strconv.Atoi(numStr)       // 字串 → 整數  Python: int("42")
    if err == nil {
        fmt.Println("數字:", num)
    }
    backToStr := strconv.Itoa(num)          // 整數 → 字串  Python: str(42)
    fmt.Println("字串:", backToStr)

    pi, _ := strconv.ParseFloat("3.14", 64)  // Python: float("3.14")
    fmt.Println("Pi:", pi)
}
```

### 9.2 os / io / bufio

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func main() {
    // === os：作業系統操作 ===
    // 環境變數
    home := os.Getenv("HOME")           // Python: os.environ.get("HOME")
    fmt.Println("HOME:", home)

    // 命令列參數
    fmt.Println("參數:", os.Args)       // Python: sys.argv

    // === 檔案寫入 ===
    // Input: 字串內容
    // Process: 建立檔案並寫入
    // Output: 檔案
    content := []byte("Hello, Go!\n第二行\n")
    err := os.WriteFile("/tmp/go_test.txt", content, 0644)  // Python: open().write()
    if err != nil {
        fmt.Println("寫入失敗:", err)
        return
    }

    // === 檔案讀取 ===
    // Input: 檔案路徑
    // Process: 讀取全部內容
    // Output: 位元組陣列
    data, err := os.ReadFile("/tmp/go_test.txt")  // Python: open().read()
    if err != nil {
        fmt.Println("讀取失敗:", err)
        return
    }
    fmt.Println("檔案內容:", string(data))

    // === bufio：逐行讀取 ===
    // Input: 字串模擬的 Reader
    // Process: 逐行掃描
    // Output: 每行內容
    reader := strings.NewReader("第一行\n第二行\n第三行\n")
    scanner := bufio.NewScanner(reader)

    lineNum := 1
    for scanner.Scan() {                  // Python: for line in file:
        fmt.Printf("  行 %d: %s\n", lineNum, scanner.Text())
        lineNum++
    }

    // 清理測試檔案
    os.Remove("/tmp/go_test.txt")
}
```

### 9.3 net/http：完整 HTTP Server

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
)

// Python Flask 等價：
// from flask import Flask, jsonify
// app = Flask(__name__)
// @app.route("/")
// def home(): return "Hello!"

// Input: HTTP Request
// Process: 回傳歡迎訊息
// Output: HTTP Response
func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "歡迎來到 Go HTTP Server！\n")
}

// Input: HTTP Request
// Process: 取得當前時間，回傳 JSON
// Output: JSON Response
func timeHandler(w http.ResponseWriter, r *http.Request) {
    data := map[string]string{
        "time":    time.Now().Format("2006-01-02 15:04:05"),
        "message": "目前時間",
    }
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    json.NewEncoder(w).Encode(data)
}

// Input: HTTP POST Request（JSON body）
// Process: 解析 JSON、處理資料
// Output: JSON Response
func echoHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "只接受 POST", http.StatusMethodNotAllowed)
        return
    }

    var body map[string]any
    err := json.NewDecoder(r.Body).Decode(&body)
    if err != nil {
        http.Error(w, "無效的 JSON", http.StatusBadRequest)
        return
    }

    response := map[string]any{
        "received": body,
        "status":   "ok",
    }
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/time", timeHandler)
    http.HandleFunc("/echo", echoHandler)

    addr := ":8080"
    fmt.Printf("伺服器啟動於 http://localhost%s\n", addr)
    log.Fatal(http.ListenAndServe(addr, nil))
}

// 測試：
// curl http://localhost:8080/
// curl http://localhost:8080/time
// curl -X POST http://localhost:8080/echo -d '{"name":"Go"}'
```

### 9.4 encoding/json

```go
package main

import (
    "encoding/json"
    "fmt"
)

// struct tag 控制 JSON 欄位名稱
type User struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Email    string `json:"email"`
    Password string `json:"-"`           // "-" 表示不序列化
    Age      int    `json:"age,omitempty"` // omitempty: 零值時省略
}

func main() {
    // === Marshal：Go struct → JSON ===
    // Input: User struct
    // Process: 序列化為 JSON
    // Output: JSON 字串
    // Python 等價：json.dumps(user_dict)

    user := User{
        ID:       1,
        Name:     "Alice",
        Email:    "alice@example.com",
        Password: "secret123",
        Age:      30,
    }

    jsonBytes, err := json.Marshal(user)
    if err != nil {
        fmt.Println("序列化失敗:", err)
        return
    }
    fmt.Println("JSON:", string(jsonBytes))
    // {"id":1,"name":"Alice","email":"alice@example.com","age":30}
    // 注意：Password 被排除了，因為 tag 是 "-"

    // 美化輸出
    prettyJSON, _ := json.MarshalIndent(user, "", "  ")
    fmt.Println("美化 JSON:")
    fmt.Println(string(prettyJSON))

    // === Unmarshal：JSON → Go struct ===
    // Input: JSON 字串
    // Process: 反序列化為 struct
    // Output: User struct
    // Python 等價：json.loads(json_str)

    jsonStr := `{"id":2,"name":"Bob","email":"bob@example.com","age":25}`
    var user2 User
    err = json.Unmarshal([]byte(jsonStr), &user2)
    if err != nil {
        fmt.Println("反序列化失敗:", err)
        return
    }
    fmt.Printf("解析結果: %+v\n", user2)

    // === 動態 JSON（不知道結構時） ===
    // Python 等價：data = json.loads(s)  # 直接得到 dict
    dynamicJSON := `{"key": "value", "numbers": [1, 2, 3], "nested": {"a": true}}`
    var result map[string]any
    json.Unmarshal([]byte(dynamicJSON), &result)
    fmt.Println("動態解析:", result)
    fmt.Println("key =", result["key"])
}
```

---

## 10. 泛型 (Go 1.18+)

### 10.1 基本泛型函式

```go
package main

import "fmt"

// === 沒有泛型時：需要為每個型別寫一個函式 ===
// func maxInt(a, b int) int { ... }
// func maxFloat(a, b float64) float64 { ... }

// === 有泛型：一個函式搞定 ===
// Python 等價：
// from typing import TypeVar
// T = TypeVar('T', int, float, str)
// def max_val(a: T, b: T) -> T: ...

// type constraint（型別約束）
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~float32 | ~float64 | ~string
}

// Input: 兩個相同型別的值
// Process: 比較大小
// Output: 較大的值
func Max[T Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Input: 任意型別的 slice
// Process: 檢查是否包含目標值
// Output: bool
func Contains[T comparable](slice []T, target T) bool {
    for _, v := range slice {
        if v == target {
            return true
        }
    }
    return false
}

// Input: slice 和轉換函式
// Process: 對每個元素套用轉換
// Output: 轉換後的新 slice
func Map[T any, U any](slice []T, fn func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = fn(v)
    }
    return result
}

// Input: slice、初始值、累加函式
// Process: 依序累加
// Output: 最終累加值
func Reduce[T any, U any](slice []T, initial U, fn func(U, T) U) U {
    result := initial
    for _, v := range slice {
        result = fn(result, v)
    }
    return result
}

func main() {
    // Max 用於不同型別
    fmt.Println(Max(3, 7))          // 7
    fmt.Println(Max(3.14, 2.71))    // 3.14
    fmt.Println(Max("apple", "banana"))  // banana

    // Contains
    nums := []int{1, 2, 3, 4, 5}
    fmt.Println(Contains(nums, 3))    // true
    fmt.Println(Contains(nums, 99))   // false

    names := []string{"Alice", "Bob"}
    fmt.Println(Contains(names, "Bob"))  // true

    // Map
    doubled := Map(nums, func(n int) int { return n * 2 })
    fmt.Println("加倍:", doubled)  // [2 4 6 8 10]

    strs := Map(nums, func(n int) string {
        return fmt.Sprintf("#%d", n)
    })
    fmt.Println("字串化:", strs)  // [#1 #2 #3 #4 #5]

    // Reduce
    sum := Reduce(nums, 0, func(acc, n int) int { return acc + n })
    fmt.Println("總和:", sum)  // 15
}
```

### 10.2 泛型 Stack（完整資料結構）

```go
package main

import (
    "errors"
    "fmt"
)

// === 泛型 Stack ===
// Python 等價：
// class Stack(Generic[T]):
//     def __init__(self): self._items: list[T] = []
//     def push(self, item: T): self._items.append(item)
//     def pop(self) -> T: return self._items.pop()

type Stack[T any] struct {
    items []T
}

// Input: 新元素
// Process: 加到頂端
// Output: 無
func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

// Input: 無
// Process: 移除並回傳頂端元素
// Output: 頂端元素或錯誤
func (s *Stack[T]) Pop() (T, error) {
    var zero T
    if len(s.items) == 0 {
        return zero, errors.New("stack 為空")
    }
    top := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return top, nil
}

// Input: 無
// Process: 查看頂端元素（不移除）
// Output: 頂端元素或錯誤
func (s *Stack[T]) Peek() (T, error) {
    var zero T
    if len(s.items) == 0 {
        return zero, errors.New("stack 為空")
    }
    return s.items[len(s.items)-1], nil
}

// Input: 無
// Process: 回傳元素數量
// Output: 長度
func (s *Stack[T]) Len() int {
    return len(s.items)
}

// Input: 無
// Process: 檢查是否為空
// Output: bool
func (s *Stack[T]) IsEmpty() bool {
    return len(s.items) == 0
}

func main() {
    // 整數 Stack
    intStack := &Stack[int]{}
    intStack.Push(10)
    intStack.Push(20)
    intStack.Push(30)

    fmt.Println("長度:", intStack.Len())   // 3

    top, _ := intStack.Peek()
    fmt.Println("頂端:", top)              // 30

    val, _ := intStack.Pop()
    fmt.Println("Pop:", val)               // 30
    fmt.Println("Pop 後長度:", intStack.Len()) // 2

    // 字串 Stack
    strStack := &Stack[string]{}
    strStack.Push("Hello")
    strStack.Push("World")

    word, _ := strStack.Pop()
    fmt.Println("字串 Pop:", word)  // World

    // 空 Stack 錯誤處理
    emptyStack := &Stack[float64]{}
    _, err := emptyStack.Pop()
    if err != nil {
        fmt.Println("錯誤:", err)  // 錯誤: stack 為空
    }
}
```

---

## 11. 完整迷你專案：REST API

> 以下是一個完整的待辦事項 REST API，展示 Go 的 struct、interface、goroutine、JSON、HTTP 等核心概念。

### 專案結構

```
todo-api/
├── main.go          # 進入點、路由設定
├── models/
│   └── todo.go      # 資料模型
└── handlers/
    └── todo.go      # HTTP 處理器
```

### models/todo.go

```go
package models

import (
    "errors"
    "sync"
    "time"
)

// Todo 資料模型
type Todo struct {
    ID        int       `json:"id"`
    Title     string    `json:"title"`
    Completed bool      `json:"completed"`
    CreatedAt time.Time `json:"created_at"`
}

// TodoStore 線程安全的記憶體儲存
type TodoStore struct {
    mu     sync.RWMutex
    todos  map[int]Todo
    nextID int
}

// NewTodoStore 建立新的儲存
// Input: 無
// Process: 初始化 map 與 ID 計數器
// Output: TodoStore 指標
func NewTodoStore() *TodoStore {
    return &TodoStore{
        todos:  make(map[int]Todo),
        nextID: 1,
    }
}

// Create 新增待辦事項
// Input: 標題字串
// Process: 建立 Todo、遞增 ID
// Output: 新建的 Todo
func (s *TodoStore) Create(title string) Todo {
    s.mu.Lock()
    defer s.mu.Unlock()

    todo := Todo{
        ID:        s.nextID,
        Title:     title,
        Completed: false,
        CreatedAt: time.Now(),
    }
    s.todos[s.nextID] = todo
    s.nextID++
    return todo
}

// GetAll 取得所有待辦事項
// Input: 無
// Process: 遍歷 map
// Output: Todo slice
func (s *TodoStore) GetAll() []Todo {
    s.mu.RLock()
    defer s.mu.RUnlock()

    result := make([]Todo, 0, len(s.todos))
    for _, t := range s.todos {
        result = append(result, t)
    }
    return result
}

// GetByID 根據 ID 取得
// Input: ID
// Process: 查詢 map
// Output: Todo 與是否存在
func (s *TodoStore) GetByID(id int) (Todo, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    todo, exists := s.todos[id]
    return todo, exists
}

// ToggleComplete 切換完成狀態
// Input: ID
// Process: 翻轉 Completed 欄位
// Output: 更新後的 Todo 或錯誤
func (s *TodoStore) ToggleComplete(id int) (Todo, error) {
    s.mu.Lock()
    defer s.mu.Unlock()

    todo, exists := s.todos[id]
    if !exists {
        return Todo{}, errors.New("找不到該待辦事項")
    }
    todo.Completed = !todo.Completed
    s.todos[id] = todo
    return todo, nil
}

// Delete 刪除待辦事項
// Input: ID
// Process: 從 map 移除
// Output: 錯誤（如果不存在）
func (s *TodoStore) Delete(id int) error {
    s.mu.Lock()
    defer s.mu.Unlock()

    if _, exists := s.todos[id]; !exists {
        return errors.New("找不到該待辦事項")
    }
    delete(s.todos, id)
    return nil
}
```

### handlers/todo.go

```go
package handlers

import (
    "encoding/json"
    "net/http"
    "strconv"
    "strings"

    "todo-api/models"
)

// TodoHandler 處理所有 Todo 相關的 HTTP 請求
type TodoHandler struct {
    Store *models.TodoStore
}

// NewTodoHandler 建立處理器
// Input: TodoStore 指標
// Process: 初始化 handler
// Output: TodoHandler 指標
func NewTodoHandler(store *models.TodoStore) *TodoHandler {
    return &TodoHandler{Store: store}
}

// ServeHTTP 路由分派（實作 http.Handler 介面）
// Input: HTTP Request
// Process: 根據 Method 和 Path 分派到對應處理函式
// Output: HTTP Response
func (h *TodoHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json; charset=utf-8")

    path := strings.TrimPrefix(r.URL.Path, "/todos")
    path = strings.TrimPrefix(path, "/")

    switch {
    case r.Method == http.MethodGet && path == "":
        h.handleList(w, r)
    case r.Method == http.MethodPost && path == "":
        h.handleCreate(w, r)
    case r.Method == http.MethodPatch && path != "":
        h.handleToggle(w, r, path)
    case r.Method == http.MethodDelete && path != "":
        h.handleDelete(w, r, path)
    default:
        writeJSON(w, http.StatusNotFound, map[string]string{"error": "路由不存在"})
    }
}

// Input: HTTP Request
// Process: 取得所有待辦事項
// Output: JSON 陣列
func (h *TodoHandler) handleList(w http.ResponseWriter, r *http.Request) {
    todos := h.Store.GetAll()
    writeJSON(w, http.StatusOK, todos)
}

// Input: HTTP Request（JSON body 含 title）
// Process: 解析 JSON、建立待辦事項
// Output: 新建的 Todo JSON
func (h *TodoHandler) handleCreate(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Title string `json:"title"`
    }
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{"error": "無效的 JSON"})
        return
    }
    if input.Title == "" {
        writeJSON(w, http.StatusBadRequest, map[string]string{"error": "title 不能為空"})
        return
    }
    todo := h.Store.Create(input.Title)
    writeJSON(w, http.StatusCreated, todo)
}

// Input: HTTP Request、路徑中的 ID
// Process: 切換完成狀態
// Output: 更新後的 Todo JSON
func (h *TodoHandler) handleToggle(w http.ResponseWriter, r *http.Request, idStr string) {
    id, err := strconv.Atoi(idStr)
    if err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{"error": "無效的 ID"})
        return
    }
    todo, err := h.Store.ToggleComplete(id)
    if err != nil {
        writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
        return
    }
    writeJSON(w, http.StatusOK, todo)
}

// Input: HTTP Request、路徑中的 ID
// Process: 刪除待辦事項
// Output: 成功訊息或錯誤
func (h *TodoHandler) handleDelete(w http.ResponseWriter, r *http.Request, idStr string) {
    id, err := strconv.Atoi(idStr)
    if err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{"error": "無效的 ID"})
        return
    }
    if err := h.Store.Delete(id); err != nil {
        writeJSON(w, http.StatusNotFound, map[string]string{"error": err.Error()})
        return
    }
    writeJSON(w, http.StatusOK, map[string]string{"message": "已刪除"})
}

// writeJSON 輔助函式：寫入 JSON 回應
func writeJSON(w http.ResponseWriter, status int, data any) {
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}
```

### main.go

```go
package main

import (
    "fmt"
    "log"
    "net/http"

    "todo-api/handlers"
    "todo-api/models"
)

func main() {
    // 初始化儲存與處理器
    store := models.NewTodoStore()
    todoHandler := handlers.NewTodoHandler(store)

    // 預設幾筆資料
    store.Create("學習 Go 基礎語法")
    store.Create("完成並發程式設計章節")
    store.Create("建立第一個 REST API")

    // 路由設定
    http.Handle("/todos", todoHandler)
    http.Handle("/todos/", todoHandler)

    // 首頁
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Todo API — 請使用 /todos 端點\n")
    })

    // 啟動伺服器
    addr := ":8080"
    fmt.Printf("Todo API 伺服器啟動於 http://localhost%s\n", addr)
    fmt.Println("API 端點：")
    fmt.Println("  GET    /todos       — 列出所有待辦事項")
    fmt.Println("  POST   /todos       — 新增待辦事項")
    fmt.Println("  PATCH  /todos/{id}  — 切換完成狀態")
    fmt.Println("  DELETE /todos/{id}  — 刪除待辦事項")
    log.Fatal(http.ListenAndServe(addr, nil))
}

// === 測試指令 ===
// 列出所有：     curl http://localhost:8080/todos
// 新增：         curl -X POST http://localhost:8080/todos -d '{"title":"買牛奶"}'
// 切換完成：     curl -X PATCH http://localhost:8080/todos/1
// 刪除：         curl -X DELETE http://localhost:8080/todos/3
```

---

## 快速參考卡

```
┌─────────────────────────────────────────────────────────────────┐
│                    Go 語言快速參考                                │
├──────────────┬──────────────────────────────────────────────────┤
│ 變數宣告      │ x := 5  /  var x int = 5                        │
│ 常數          │ const Pi = 3.14                                  │
│ 函式          │ func name(a int) (int, error) { }               │
│ 多回傳值      │ val, err := someFunc()                           │
│ 錯誤處理      │ if err != nil { return err }                     │
│ Struct        │ type User struct { Name string }                 │
│ 方法          │ func (u *User) Save() error { }                  │
│ Interface     │ type Reader interface { Read([]byte)(int,error) }│
│ Goroutine     │ go doSomething()                                 │
│ Channel       │ ch := make(chan int)  /  ch <- 42  /  val := <-ch│
│ Select        │ select { case v := <-ch1:  case <-time.After(): }│
│ WaitGroup     │ wg.Add(1)  /  defer wg.Done()  /  wg.Wait()     │
│ Mutex         │ mu.Lock()  /  defer mu.Unlock()                  │
│ 泛型          │ func Max[T Ordered](a, b T) T { }               │
│ JSON 序列化    │ json.Marshal(v)  /  json.Unmarshal(data, &v)     │
│ HTTP Server   │ http.HandleFunc("/", handler)                    │
│ Defer         │ defer file.Close()                               │
│ 套件管理      │ go mod init / go get / go mod tidy               │
└──────────────┴──────────────────────────────────────────────────┘
```

---

## Python → Go 心智轉換清單

1. **沒有 class** → 用 `struct` + 方法，組合取代繼承
2. **沒有 try/except** → 回傳 `error`，`if err != nil` 是日常
3. **沒有 while** → `for` 統一所有迴圈
4. **沒有 pip** → `go mod` 內建套件管理
5. **沒有 GIL** → goroutine 是真正的並行，用 channel 通訊
6. **沒有動態型別** → 靜態型別 + 泛型解決通用需求
7. **未使用的變數/匯入** → 編譯錯誤，不是警告
8. **大寫開頭** → 公開（exported），小寫開頭 → 私有
9. **`nil`** → 不是 `None`，是指標/interface/slice/map/channel 的零值
10. **`defer`** → 取代 `finally`，確保資源釋放

---

> **下一步建議**：安裝 Go（https://go.dev），用 `go run` 逐一執行本教材的範例，親手修改參數觀察變化。並發程式設計的部分建議搭配 `go race detector`（`go run -race main.go`）來檢測資料競爭。
