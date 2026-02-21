# EP06 — Rust：安全系統程式語言

> **對象**：有 Python 經驗的開發者，想學習 Rust
> **核心觀念**：所有權 (Ownership)、借用 (Borrowing)、零成本抽象 (Zero-Cost Abstraction)

---

## 目錄

| 章 | 主題 | 重點 |
|----|------|------|
| 1 | Rust vs Python 基本對照 | 語法映射、Cargo 工具鏈 |
| 2 | 所有權系統 | move / copy / borrow / lifetime |
| 3 | 基本型別 | 標量、String vs &str、Option、Result |
| 4 | 函式與閉包 | fn、closure、Fn trait |
| 5 | Struct 與 Enum | 資料建模、模式匹配 |
| 6 | Trait | 核心抽象機制 |
| 7 | 錯誤處理 | Result、? 運算子、自定義錯誤 |
| 8 | 集合與迭代器 | Vec、HashMap、鏈式迭代 |
| 9 | 並發 | thread、Arc、Mutex、channel |
| 10 | Cargo 與專案管理 | 模組、可見性、依賴 |
| 11 | 巨集入門 | macro_rules!、derive |
| 12 | 完整迷你專案 | CLI 任務管理器 |

---

## 1. Rust vs Python 基本對照

### 1.1 Hello World 完整對照

```python
# Python — 直接執行: python hello.py
print("Hello, World!")
```

```rust
// Rust — src/main.rs
// Input:  無 | Process: 呼叫 println! 巨集 | Output: 終端印出文字
fn main() {
    println!("Hello, World!");
}
```

| 項目 | Python | Rust |
|------|--------|------|
| 進入點 | 整個檔案由上而下 | 必須有 `fn main()` |
| 執行 | 直譯 `python file.py` | 編譯 `cargo run` |
| 分號 | 不需要 | 每行結尾需要 `;` |
| 印出 | `print()` 函式 | `println!()` 巨集（注意 `!`） |
| 型別 | 動態型別 | 靜態型別，編譯期檢查 |

### 1.2 變數宣告：let vs let mut

```rust
// Input: 無 | Process: 示範不可變與可變變數 | Output: 印出變數值
fn main() {
    // 不可變綁定（預設）
    let x = 5;
    // x = 10;  // 編譯錯誤！不可變

    // 可變綁定
    let mut y = 5;
    println!("y 原始值: {}", y);  // 5
    y = 10;
    println!("y 修改後: {}", y);  // 10

    // 變數遮蔽 (shadowing)
    let z = 5;
    let z = z + 1;
    let z = z * 2;
    println!("z = {}", z);  // 12

    // 型別標注
    let a: i32 = 42;
    let b: f64 = 3.14;
    let c: bool = true;
    let d: char = '中';  // Rust char 是 Unicode，4 bytes
    println!("a={}, b={}, c={}, d={}", a, b, c, d);
}
```

### 1.3 Cargo 工具鏈

```bash
cargo new my_project     # 建立新專案
cargo build              # Debug 編譯
cargo build --release    # Release 編譯（最佳化）
cargo run                # 編譯並執行
cargo test               # 執行測試
cargo check              # 檢查語法（不產生執行檔）
```

**Cargo.toml**（等同 `requirements.txt` + `pyproject.toml`）：

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
```

| Python 工具 | Rust 對應 |
|-------------|-----------|
| `pip install` | `cargo add` 或編輯 `Cargo.toml` |
| `requirements.txt` | `Cargo.toml` |
| `venv` | Rust 天生隔離，無此需求 |
| `PyPI` | `crates.io` |
| `pytest` | `cargo test` |

### 1.4 println! 格式化

```rust
// Input: 無 | Process: 各種格式化輸出 | Output: 格式化字串
fn main() {
    let name = "Rust";
    let version = 2021;
    println!("Hello, {}!", name);                          // 基本插值
    println!("{lang} v{ver}", lang=name, ver=version);     // 具名參數

    let nums = vec![1, 2, 3];
    println!("{:?}", nums);     // Debug 輸出: [1, 2, 3]
    println!("{:#?}", nums);    // 美化印出

    println!("{:>10}", 42);     // 靠右對齊，寬度 10
    println!("{:0>5}", 42);     // 補零: 00042
    println!("{:.2}", 3.14159); // 小數兩位: 3.14
    println!("{:b}", 255);      // 二進位: 11111111
    println!("{:x}", 255);      // 十六進位: ff
}
```

---

## 2. 所有權系統 — Rust 最重要的概念

### 2.1 所有權三大規則

```
規則 1: Rust 中每個值都有一個「擁有者」(owner)
規則 2: 同一時間只能有一個擁有者
規則 3: 當擁有者離開作用域 (scope)，值會被丟棄 (drop)
```

```rust
// Input: 無 | Process: 示範所有權與作用域 | Output: 印出作用域內的值
fn main() {
    {
        let s = String::from("hello");
        println!("{}", s);
    } // s 離開作用域 → 記憶體自動釋放（呼叫 drop）
    // println!("{}", s);  // 編譯錯誤！s 已不存在
}
```

### 2.2 移動 (Move) vs 複製 (Copy)

```
Move（堆上資料，如 String）:        Copy（棧上資料，如 i32）:
┌──────────┐    ┌────────┐        ┌──────┐
│ s1       │    │ heap   │        │ x =5 │ ← 棧 stack
│ ptr ─────┼──→ │"hello" │        └──────┘
│ len: 5   │    └────────┘        let y = x; (Copy)
└──────────┘                      ┌──────┐  ┌──────┐
let s2 = s1; (Move)              │ x =5 │  │ y =5 │
s1 失效！s2 接管指標              └──────┘  └──────┘
```

```rust
// Input: 無 | Process: 示範 Move 和 Copy 差異 | Output: 印出變數值
fn main() {
    // Move 語義（堆上資料）
    let s1 = String::from("hello");
    let s2 = s1;            // s1 所有權移動到 s2
    // println!("{}", s1);  // 編譯錯誤！
    println!("{}", s2);

    // Copy 語義（棧上資料）
    let x = 5;
    let y = x;              // i32 實作 Copy trait，複製
    println!("x={}, y={}", x, y);  // 都能用

    // 明確 clone（深拷貝）
    let s3 = String::from("world");
    let s4 = s3.clone();
    println!("s3={}, s4={}", s3, s4);  // 都有效

    // 函式呼叫時的 Move
    let s5 = String::from("rust");
    takes_ownership(s5);     // s5 所有權移入函式
    // println!("{}", s5);  // 編譯錯誤！

    let n = 42;
    makes_copy(n);           // i32 是 Copy，n 仍可用
    println!("n 仍可用: {}", n);
}

// Input: some_string: String（取得所有權）
// Process: 印出字串 | Output: 函式結束時 drop
fn takes_ownership(some_string: String) {
    println!("取得所有權: {}", some_string);
}

// Input: some_integer: i32（複製）
// Process: 印出數字 | Output: 原始值不受影響
fn makes_copy(some_integer: i32) {
    println!("複製的值: {}", some_integer);
}
```

**Python 對照**：Python 一切都是參考（reference），有 GC 自動回收，不需考慮 Move/Copy。

### 2.3 借用 (Borrow)：&T 與 &mut T

```
借用規則：
1. 任意時刻，要嘛「一個可變借用」，要嘛「多個不可變借用」
2. 借用必須總是有效的（不能 dangling reference）
```

```rust
// Input: 無 | Process: 示範借用 | Output: 印出借用的值
fn main() {
    // 不可變借用 &T
    let s1 = String::from("hello");
    let len = calculate_length(&s1);  // 借出，不轉移所有權
    println!("'{}' 長度 {}", s1, len);  // s1 仍可用！

    // 多個不可變借用 — 合法
    let s2 = String::from("world");
    let r1 = &s2;
    let r2 = &s2;
    println!("r1={}, r2={}", r1, r2);

    // 可變借用 &mut T
    let mut s3 = String::from("hello");
    change(&mut s3);
    println!("修改後: {}", s3);  // hello, world

    // 不能同時有可變和不可變借用
    let mut s4 = String::from("test");
    let r3 = &s4;
    println!("{}", r3);   // r3 最後一次使用（NLL 結束借用）
    let r4 = &mut s4;     // 現在可以了
    r4.push_str("!");
    println!("{}", r4);
}

// Input: s: &String（不可變借用）| Process: 計算長度 | Output: usize
fn calculate_length(s: &String) -> usize {
    s.len()
}

// Input: s: &mut String（可變借用）| Process: 追加內容 | Output: 修改原始字串
fn change(s: &mut String) {
    s.push_str(", world");
}
```

### 2.4 生命週期 (Lifetime) 入門

```rust
// Input: x, y: &str | Process: 回傳較長的 | Output: &str（生命週期 = 較短的輸入）
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let string1 = String::from("long string");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
        println!("較長的是: {}", result);
    }
    // 編譯器透過 'a 在編譯期就能抓到懸空參考錯誤
}
```

| 語言 | 記憶體管理 | 優點 | 缺點 |
|------|-----------|------|------|
| Python | GC | 開發者不用管 | 效能開銷 |
| C/C++ | 手動 malloc/free | 完全控制 | 記憶體洩漏 |
| Rust | 所有權系統 | 零成本、編譯期安全 | 學習曲線陡 |

---

## 3. 基本型別

### 3.1 標量型別

```rust
// Input: 無 | Process: 展示標量型別 | Output: 印出各型別的值
fn main() {
    let a: i8 = -128;            // 8 位元有號
    let b: u8 = 255;             // 8 位元無號
    let c: i32 = 2_147_483_647;  // 預設整數型別
    let d: i64 = 9_000_000_000;
    let e: usize = 100;          // 平台相關（用於索引）
    let f: f64 = 3.14159;        // 預設浮點型別
    let g: bool = true;
    let h: char = '中';          // 4 bytes，Unicode
    println!("i8={}, u8={}, i32={}, i64={}", a, b, c, d);
    println!("usize={}, f64={}, bool={}, char={}", e, f, g, h);
    println!("i32: {} bytes, char: {} bytes",
        std::mem::size_of::<i32>(), std::mem::size_of::<char>());
}
```

### 3.2 &str vs String — 最常見困惑

```
&str（字串切片，借用，不可變）    String（擁有所有權，可變，堆上）
┌──────────┐                    ┌──────────┐    ┌───────────┐
│ ptr ─────┼→ "hello" (唯讀)    │ ptr ─────┼──→ │ h e l l o │ heap
│ len: 5   │                    │ len: 5   │    └───────────┘
└──────────┘                    │ cap: 8   │
                                └──────────┘
```

```rust
// Input: 無 | Process: 示範 &str 和 String 差異與轉換 | Output: 操作結果
fn main() {
    let s1: &str = "hello";               // 字串字面值（二進位中）
    let mut s2: String = String::from("hello");
    s2.push_str(", world");
    s2.push('!');
    println!("{}", s2);  // hello, world!

    // 轉換
    let s3: String = s1.to_string();       // &str → String
    let s4: String = "world".into();       // &str → String（Into trait）
    let s5: &str = &s3;                    // String → &str（自動解引用）
    let s6: &str = s3.as_str();            // String → &str（明確）
    println!("s3={}, s4={}, s5={}, s6={}", s3, s4, s5, s6);

    // 字串切片與串接
    let full = String::from("Hello, Rust!");
    let hello: &str = &full[0..5];
    let rust: &str = &full[7..11];
    println!("{}", format!("{} {}!", hello, rust));
}

// 函式參數建議用 &str — 更通用
// Input: name: &str | Process: 格式化問候語 | Output: String
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

### 3.3 Vec<T> — 對比 Python list

```rust
// Input: 無 | Process: 示範 Vec 操作 | Output: 印出向量內容
fn main() {
    let mut nums: Vec<i32> = Vec::new();
    nums.push(1);
    nums.push(2);
    nums.push(3);

    let nums2 = vec![1, 2, 3, 4, 5];   // vec! 巨集

    let first = nums[0];                // 直接索引（越界 panic）
    let second = nums.get(1);           // 回傳 Option<&i32>（安全）
    println!("first={}, second={:?}", first, second);

    for n in &nums { print!("{} ", n); }
    println!();

    println!("長度: {}, 含2: {}", nums.len(), nums.contains(&2));

    nums.push(4);
    nums.pop();             // 移除最後一個
    nums.insert(0, 0);      // 在索引 0 插入
    nums.remove(0);         // 移除索引 0

    let mut v = vec![3, 1, 4, 1, 5, 9];
    v.sort();
    println!("排序後: {:?}", v);

    let slice: &[i32] = &nums2[1..4];
    println!("切片: {:?}", slice);  // [2, 3, 4]
}
```

### 3.4 HashMap<K, V> — 對比 Python dict

```rust
use std::collections::HashMap;

// Input: 無 | Process: 示範 HashMap 操作 | Output: 印出內容
fn main() {
    let mut scores: HashMap<String, i32> = HashMap::new();
    scores.insert(String::from("Alice"), 95);
    scores.insert(String::from("Bob"), 87);

    match scores.get("Alice") {
        Some(score) => println!("Alice: {}", score),
        None => println!("找不到"),
    }

    for (name, score) in &scores {
        println!("{}: {}", name, score);
    }

    // 只在 key 不存在時插入
    scores.entry(String::from("Carol")).or_insert(92);

    // 更新值
    let count = scores.entry(String::from("Alice")).or_insert(0);
    *count += 5;

    // 字數統計 — 對比 Python Counter
    let text = "hello world hello rust hello";
    let mut word_count: HashMap<&str, i32> = HashMap::new();
    for word in text.split_whitespace() {
        let count = word_count.entry(word).or_insert(0);
        *count += 1;
    }
    println!("字數統計: {:?}", word_count);
}
```

### 3.5 Option<T> — 對比 Python Optional / None

```rust
// Input: 無 | Process: 示範 Option 用法 | Output: 安全處理可能為空的值
fn main() {
    let some_number: Option<i32> = Some(42);
    let no_number: Option<i32> = None;

    // match（最安全）
    match some_number {
        Some(n) => println!("得到: {}", n),
        None => println!("沒有值"),
    }

    // if let — 只關心 Some
    if let Some(n) = some_number { println!("數字: {}", n); }

    // unwrap / unwrap_or
    let v1 = some_number.unwrap();          // None 會 panic
    let v2 = no_number.unwrap_or(0);        // 預設值
    println!("v1={}, v2={}", v1, v2);

    // map
    let doubled = some_number.map(|n| n * 2);
    println!("doubled: {:?}", doubled);  // Some(84)

    // 安全陣列存取
    let names = vec!["Alice", "Bob"];
    println!("{:?}, {:?}", names.get(0), names.get(9));  // Some, None
}

// Input: items: &[i32] | Process: 尋找第一個偶數 | Output: Option<i32>
fn find_first_even(items: &[i32]) -> Option<i32> {
    for &item in items {
        if item % 2 == 0 { return Some(item); }
    }
    None
}
```

### 3.6 Result<T, E> — 對比 Python try/except

```rust
use std::num::ParseIntError;

// Input: 無 | Process: 示範 Result 用法 | Output: 處理可能失敗的操作
fn main() {
    let good: Result<i32, ParseIntError> = "42".parse();
    let bad: Result<i32, ParseIntError> = "abc".parse();

    match good {
        Ok(n) => println!("解析成功: {}", n),
        Err(e) => println!("失敗: {}", e),
    }
    match bad {
        Ok(n) => println!("成功: {}", n),
        Err(e) => println!("失敗: {}", e),  // 走這裡
    }

    let num = "not_a_number".parse::<i32>().unwrap_or(0);
    let result = "42".parse::<i32>().map(|n| n * 2).unwrap_or(0);
    println!("預設: {}, 鏈式: {}", num, result);
}
```

---

## 4. 函式與閉包

### 4.1 函式定義

```rust
// Input: a, b: i32 | Process: 相加 | Output: i32
fn add(a: i32, b: i32) -> i32 {
    a + b  // 最後表達式 = 回傳值（無分號）
}

// Input: n: u32 | Process: 判斷奇偶 | Output: &str
fn is_even(n: u32) -> &'static str {
    if n % 2 == 0 { "偶數" } else { "奇數" }
}

// Input: numbers: &[i32] | Process: 計算平均 | Output: f64
fn average(numbers: &[i32]) -> f64 {
    if numbers.is_empty() { return 0.0; }
    let sum: i32 = numbers.iter().sum();
    sum as f64 / numbers.len() as f64
}

// Input: numbers: &[i32] | Process: 找最小最大 | Output: (i32, i32) 元組
fn min_max(numbers: &[i32]) -> (i32, i32) {
    let mut min = numbers[0];
    let mut max = numbers[0];
    for &n in numbers {
        if n < min { min = n; }
        if n > max { max = n; }
    }
    (min, max)
}

fn main() {
    println!("add(3,4) = {}", add(3, 4));
    println!("10 是{}", is_even(10));
    println!("平均: {}", average(&[1, 2, 3, 4, 5]));
    let (min, max) = min_max(&[3, 1, 4, 1, 5, 9]);
    println!("最小={}, 最大={}", min, max);
}
```

### 4.2 閉包 (Closure)

```rust
// Input: 無 | Process: 示範閉包用法 | Output: 閉包執行結果
fn main() {
    // 基本閉包 — 對比 Python lambda x: x + 1
    let add_one = |x: i32| -> i32 { x + 1 };
    let add_one_short = |x| x + 1;
    println!("{}, {}", add_one(5), add_one_short(5_i32));

    // 捕獲環境變數
    let multiplier = 3;
    let multiply = |x: i32| x * multiplier;
    println!("multiply(5) = {}", multiply(5));  // 15

    // 可變捕獲
    let mut count = 0;
    let mut increment = || { count += 1; count };
    println!("{}, {}", increment(), increment());  // 1, 2

    // 閉包作為參數 — 對比 Python: map(lambda x: x*2, list)
    let numbers = vec![1, 2, 3, 4, 5];
    let doubled: Vec<i32> = numbers.iter().map(|&x| x * 2).collect();
    let evens: Vec<&i32> = numbers.iter().filter(|&&x| x % 2 == 0).collect();
    println!("doubled: {:?}, evens: {:?}", doubled, evens);

    // 閉包作為回傳值
    let adder = make_adder(10);
    println!("adder(5) = {}", adder(5));  // 15
}

// Input: x: i32 | Process: 建立加法閉包 | Output: impl Fn(i32) -> i32
fn make_adder(x: i32) -> impl Fn(i32) -> i32 {
    move |y| x + y  // move 取得 x 的所有權
}

// Fn:     以 &self 借用捕獲變數（可多次呼叫，不修改）
// FnMut:  以 &mut self 借用（可多次呼叫，會修改）
// FnOnce: 取得所有權（只能呼叫一次）

// Input: f: F, x: i32 | Process: 呼叫 f 兩次求和 | Output: i32
fn apply_twice<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 {
    f(x) + f(x)
}
```

---

## 5. Struct 與 Enum

### 5.1 Struct — 對比 Python dataclass

```rust
#[derive(Debug, Clone)]
struct User {
    name: String,
    email: String,
    age: u32,
    active: bool,
}

impl User {
    // Input: name, email, age | Process: 建立 User | Output: User
    fn new(name: &str, email: &str, age: u32) -> Self {
        User { name: name.to_string(), email: email.to_string(), age, active: true }
    }

    // Input: &self | Process: 格式化問候語 | Output: String
    fn greet(&self) -> String {
        format!("Hi, I'm {} ({})", self.name, self.age)
    }

    // Input: &mut self | Process: 停用帳號 | Output: 無
    fn deactivate(&mut self) { self.active = false; }

    // Input: self, new_email | Process: 消耗自身建立新 User | Output: User
    fn with_email(self, new_email: &str) -> User {
        User { email: new_email.to_string(), ..self }
    }
}

fn main() {
    let mut user = User::new("Alice", "alice@ex.com", 30);
    println!("{}", user.greet());
    user.deactivate();
    let user2 = user.with_email("new@ex.com");
    println!("{:?}", user2);

    // 元組結構
    struct Point(f64, f64);
    let p = Point(1.0, 2.0);
    println!("Point({}, {})", p.0, p.1);
}
```

### 5.2 Enum — 比 Python enum 強大很多

```rust
// Rust enum 可攜帶資料（代數資料型別 ADT）
#[derive(Debug)]
enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle { base: f64, height: f64 },
}

impl Shape {
    // Input: &self | Process: 計算面積 | Output: f64
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => std::f64::consts::PI * r * r,
            Shape::Rectangle(w, h) => w * h,
            Shape::Triangle { base, height } => 0.5 * base * height,
        }
    }

    // Input: &self | Process: 回傳名稱 | Output: &str
    fn name(&self) -> &str {
        match self {
            Shape::Circle(_) => "圓形",
            Shape::Rectangle(_, _) => "長方形",
            Shape::Triangle { .. } => "三角形",
        }
    }
}

#[derive(Debug)]
enum Command {
    Quit,
    Echo(String),
    Move { x: i32, y: i32 },
    ChangeColor(u8, u8, u8),
}

// Input: cmd: &Command | Process: 執行指令 | Output: 印出結果
fn execute(cmd: &Command) {
    match cmd {
        Command::Quit => println!("退出"),
        Command::Echo(msg) => println!("回音: {}", msg),
        Command::Move { x, y } => println!("移動到 ({}, {})", x, y),
        Command::ChangeColor(r, g, b) => println!("RGB({},{},{})", r, g, b),
    }
}

fn main() {
    let shapes = vec![
        Shape::Circle(5.0), Shape::Rectangle(4.0, 6.0),
        Shape::Triangle { base: 3.0, height: 8.0 },
    ];
    for s in &shapes { println!("{} = {:.2}", s.name(), s.area()); }

    let cmds = vec![
        Command::Echo(String::from("Hello")),
        Command::Move { x: 10, y: 20 },
        Command::Quit,
    ];
    for cmd in &cmds { execute(cmd); }
}
```

### 5.3 模式匹配 match

```rust
// Input: 無 | Process: 展示 match 強大用法 | Output: 匹配結果
fn main() {
    let number = 13;
    match number {
        1 => println!("一"),
        2 | 3 | 5 | 7 | 11 | 13 => println!("質數"),
        14..=19 => println!("十幾"),
        _ => println!("其他"),
    }

    // 解構 tuple + 守衛
    let point = (3, -5);
    match point {
        (0, 0) => println!("原點"),
        (x, 0) => println!("x 軸, x={}", x),
        (0, y) => println!("y 軸, y={}", y),
        (x, y) if x > 0 && y > 0 => println!("第一象限"),
        (x, y) => println!("({}, {})", x, y),
    }

    // Option 匹配
    let maybe: Option<i32> = Some(42);
    match maybe {
        Some(n) if n > 0 => println!("正數: {}", n),
        Some(n) => println!("非正: {}", n),
        None => println!("無值"),
    }

    // if let（簡化 match）
    if let Some(v) = maybe { println!("if let: {}", v); }

    // while let
    let mut stack = vec![1, 2, 3];
    while let Some(top) = stack.pop() { println!("彈出: {}", top); }
}
```

---

## 6. Trait — Rust 的核心抽象

### 6.1 定義與實作 Trait

```rust
use std::fmt;

// Trait — 對比 Python ABC 或 Go interface
trait Drawable {
    fn draw(&self) -> String;                    // 必須實作
    fn description(&self) -> String {            // 預設實作
        format!("可繪製物件: {}", self.draw())
    }
}

#[derive(Debug)]
struct Circle { radius: f64 }

#[derive(Debug)]
struct Square { side: f64 }

impl Drawable for Circle {
    fn draw(&self) -> String { format!("圓形 (r={})", self.radius) }
}

impl Drawable for Square {
    fn draw(&self) -> String { format!("正方形 (s={})", self.side) }
    fn description(&self) -> String {  // 覆寫預設
        format!("正方形，邊長 {}，面積 {}", self.side, self.side * self.side)
    }
}

// Trait Bound 三種寫法
// Input: item: &T | Process: 呼叫 draw | Output: 印出結果
fn print_drawing<T: Drawable>(item: &T) {
    println!("{}", item.draw());
}
fn print_desc(item: &impl Drawable) {  // impl Trait 語法
    println!("{}", item.description());
}
fn print_debug<T>(item: &T) where T: Drawable + fmt::Debug {  // where 子句
    println!("{:?} → {}", item, item.draw());
}

// 回傳 impl Trait
fn default_shape() -> impl Drawable { Circle { radius: 1.0 } }

fn main() {
    let c = Circle { radius: 5.0 };
    let s = Square { side: 3.0 };
    print_drawing(&c);
    print_desc(&s);
    print_debug(&c);

    // 動態分派（trait object）— 不同型別存同一容器
    let shapes: Vec<Box<dyn Drawable>> = vec![
        Box::new(Circle { radius: 2.0 }),
        Box::new(Square { side: 4.0 }),
    ];
    for shape in &shapes { println!("{}", shape.draw()); }
}
```

### 6.2 derive 巨集與常見 Trait

```rust
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Student { name: String, grade: u32 }

impl fmt::Display for Student {
    // Input: &self, f | Process: 格式化 | Output: fmt::Result
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}（{}年級）", self.name, self.grade)
    }
}

fn main() {
    let s1 = Student { name: String::from("Alice"), grade: 3 };
    let s2 = s1.clone();
    println!("{:?}", s1);              // Debug
    println!("{}", s1);                // Display
    println!("相等: {}", s1 == s2);    // PartialEq
}
```

**常見 Trait 速查表**：

| Trait | 功能 | Python 對照 |
|-------|------|------------|
| `Debug` | `{:?}` 格式化 | `__repr__` |
| `Display` | `{}` 格式化 | `__str__` |
| `Clone` | `.clone()` 深拷貝 | `copy.deepcopy()` |
| `Copy` | 隱式複製（棧上小型別） | 無對應 |
| `PartialEq`/`Eq` | `==` 比較 | `__eq__` |
| `PartialOrd`/`Ord` | 排序 | `__lt__`/`__gt__` |
| `Hash` | 雜湊（可作 key） | `__hash__` |
| `Default` | 預設值 | 無參 `__init__` |
| `Iterator` | 迭代 | `__iter__`/`__next__` |
| `From`/`Into` | 型別轉換 | 自訂轉換 |
| `Drop` | 析構清理 | `__del__` |

---

## 7. 錯誤處理

### 7.1 Result<T, E> 與 ? 運算子

```rust
use std::fs;

// Input: filename | Process: 讀檔→解析數字 | Output: Result<i32, String>
fn read_number_v1(filename: &str) -> Result<i32, String> {
    let content = match fs::read_to_string(filename) {
        Ok(c) => c,
        Err(e) => return Err(format!("讀檔失敗: {}", e)),
    };
    match content.trim().parse::<i32>() {
        Ok(n) => Ok(n),
        Err(e) => Err(format!("解析失敗: {}", e)),
    }
}

// 同功能，用 ? 運算子（優雅很多）
// Input: filename | Process: 讀檔+解析，? 自動傳播錯誤 | Output: Result
fn read_number_v2(filename: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(filename)?;  // 失敗提早回傳
    let number = content.trim().parse::<i32>()?;
    Ok(number)
}

fn main() {
    match read_number_v1("number.txt") {
        Ok(n) => println!("讀到: {}", n),
        Err(e) => println!("錯誤: {}", e),
    }

    let value = read_number_v1("missing.txt").unwrap_or_else(|e| {
        println!("警告: {}，用預設值", e);
        0
    });
    println!("最終值: {}", value);
}
```

### 7.2 自定義錯誤型別

```rust
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    IoError(std::io::Error),
    ParseError(ParseIntError),
    ValidationError(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::IoError(e) => write!(f, "IO: {}", e),
            AppError::ParseError(e) => write!(f, "解析: {}", e),
            AppError::ValidationError(msg) => write!(f, "驗證: {}", msg),
        }
    }
}

// 實作 From — 讓 ? 自動轉換錯誤型別
impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::IoError(e) }
}
impl From<ParseIntError> for AppError {
    fn from(e: ParseIntError) -> Self { AppError::ParseError(e) }
}

// Input: filename, min, max | Process: 讀檔+解析+驗證 | Output: Result<i32, AppError>
fn read_and_validate(filename: &str, min: i32, max: i32) -> Result<i32, AppError> {
    let content = std::fs::read_to_string(filename)?;
    let number: i32 = content.trim().parse()?;
    if number < min || number > max {
        return Err(AppError::ValidationError(
            format!("{} 不在 {}~{} 範圍", number, min, max)));
    }
    Ok(number)
}

fn main() {
    match read_and_validate("config.txt", 1, 100) {
        Ok(n) => println!("設定值: {}", n),
        Err(AppError::IoError(e)) => println!("檔案: {}", e),
        Err(AppError::ParseError(e)) => println!("格式: {}", e),
        Err(AppError::ValidationError(msg)) => println!("驗證: {}", msg),
    }
}
```

### 7.3 第三方 crate

```rust
// thiserror（函式庫用）— Cargo.toml: thiserror = "1.0"
// use thiserror::Error;
// #[derive(Error, Debug)]
// enum AppError {
//     #[error("IO: {0}")]
//     Io(#[from] std::io::Error),
//     #[error("解析: {0}")]
//     Parse(#[from] std::num::ParseIntError),
// }

// anyhow（應用程式用）— Cargo.toml: anyhow = "1.0"
// use anyhow::{Context, Result};
// fn read_config() -> Result<i32> {
//     let content = std::fs::read_to_string("config.txt")
//         .context("無法讀取設定檔")?;
//     Ok(content.trim().parse().context("不是有效數字")?)
// }
```

| Python | Rust |
|--------|------|
| `try/except` | `match Ok/Err` 或 `?` |
| `raise ValueError` | `return Err(...)` |
| 例外自動冒泡 | `?` 明確傳播 |

---

## 8. 集合與迭代器

### 8.1 集合型別

```rust
use std::collections::{HashMap, HashSet, BTreeMap, VecDeque};

// Input: 無 | Process: 示範集合型別 | Output: 印出操作結果
fn main() {
    // VecDeque — 對比 Python collections.deque
    let mut deque: VecDeque<i32> = VecDeque::new();
    deque.push_back(1);
    deque.push_front(0);
    println!("VecDeque: {:?}", deque);

    // HashSet — 對比 Python set
    let set_a: HashSet<i32> = [1, 2, 3, 4].iter().cloned().collect();
    let set_b: HashSet<i32> = [3, 4, 5, 6].iter().cloned().collect();
    let union: HashSet<&i32> = set_a.union(&set_b).collect();
    let inter: HashSet<&i32> = set_a.intersection(&set_b).collect();
    println!("聯集: {:?}, 交集: {:?}", union, inter);

    // BTreeMap — 有序映射（key 自動排序）
    let mut bt: BTreeMap<String, i32> = BTreeMap::new();
    bt.insert("cherry".into(), 3);
    bt.insert("apple".into(), 1);
    bt.insert("banana".into(), 2);
    for (k, v) in &bt { println!("{}: {}", k, v); }  // apple, banana, cherry
}
```

### 8.2 迭代器鏈 — 對比 Python list comprehension

```rust
// Input: 無 | Process: 迭代器鏈式操作 | Output: 轉換結果
fn main() {
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // 對比 Python: [x*2 for x in numbers if x%2==0]
    let result: Vec<i32> = numbers.iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * 2)
        .collect();
    println!("偶數加倍: {:?}", result);  // [4, 8, 12, 16, 20]

    // 對比 Python: sum(x**2 for x in numbers)
    let sum_sq: i32 = numbers.iter().map(|&x| x * x).sum();
    println!("平方和: {}", sum_sq);

    // any / all
    println!("有>5: {}", numbers.iter().any(|&x| x > 5));
    println!("全>0: {}", numbers.iter().all(|&x| x > 0));

    // enumerate — 對比 Python enumerate()
    let fruits = vec!["apple", "banana", "cherry"];
    for (i, f) in fruits.iter().enumerate() { println!("{}. {}", i+1, f); }

    // zip — 對比 Python zip()
    let names = vec!["Alice", "Bob"];
    let scores = vec![95, 87];
    let paired: Vec<_> = names.iter().zip(scores.iter()).collect();
    println!("配對: {:?}", paired);

    // fold — 對比 Python functools.reduce()
    let product: i32 = vec![1,2,3,4,5].iter().fold(1, |acc, &x| acc * x);
    println!("連乘: {}", product);  // 120

    // take / skip
    let first3: Vec<&i32> = numbers.iter().take(3).collect();
    let skip5: Vec<&i32> = numbers.iter().skip(5).collect();
    println!("前三: {:?}, 跳五: {:?}", first3, skip5);

    // flat_map — 攤平
    let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
    let flat: Vec<&i32> = nested.iter().flat_map(|v| v.iter()).collect();
    println!("攤平: {:?}", flat);
}
```

### 8.3 自訂迭代器

```rust
struct Counter { current: u32, max: u32 }

impl Counter {
    fn new(max: u32) -> Self { Counter { current: 0, max } }
}

impl Iterator for Counter {
    type Item = u32;
    // Input: &mut self | Process: 產生下一個值 | Output: Option<u32>
    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            self.current += 1;
            Some(self.current)
        } else { None }
    }
}

fn main() {
    let sum: u32 = Counter::new(5).sum();
    println!("1+2+3+4+5 = {}", sum);

    let evens_sq: Vec<u32> = Counter::new(10)
        .filter(|&x| x % 2 == 0)
        .map(|x| x * x)
        .collect();
    println!("偶數平方: {:?}", evens_sq);  // [4, 16, 36, 64, 100]
}
```

---

## 9. 並發

### 9.1 執行緒 (Thread)

```rust
use std::thread;
use std::time::Duration;

// Input: 無 | Process: 建立執行緒 | Output: 執行緒計算結果
fn main() {
    // 基本執行緒 — 對比 Python threading.Thread
    let handle = thread::spawn(|| {
        for i in 1..=5 {
            println!("子執行緒: {}", i);
            thread::sleep(Duration::from_millis(100));
        }
        42
    });

    for i in 1..=3 {
        println!("主執行緒: {}", i);
        thread::sleep(Duration::from_millis(150));
    }

    let result = handle.join().unwrap();
    println!("子執行緒回傳: {}", result);

    // move 閉包 — 將所有權移入執行緒
    let data = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("資料: {:?}", data);
        data.iter().sum::<i32>()
    });
    println!("總和: {}", handle.join().unwrap());

    // 多個執行緒
    let mut handles = vec![];
    for i in 0..5 {
        handles.push(thread::spawn(move || i * i));
    }
    let results: Vec<i32> = handles.into_iter().map(|h| h.join().unwrap()).collect();
    println!("結果: {:?}", results);
}
```

### 9.2 共享狀態：Arc<Mutex<T>>

```rust
use std::sync::{Arc, Mutex};
use std::thread;

// Input: 無 | Process: 多執行緒安全共享資料 | Output: 最終計數值
fn main() {
    // Arc = 執行緒安全參考計數 | Mutex = 互斥鎖
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter_clone = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter_clone.lock().unwrap();
            *num += 1;
            // MutexGuard 離開作用域自動解鎖
        }));
    }

    for h in handles { h.join().unwrap(); }
    println!("最終計數: {}", *counter.lock().unwrap());  // 10

    // 共享 Vec
    let shared_vec = Arc::new(Mutex::new(Vec::new()));
    let mut handles = vec![];
    for i in 0..5 {
        let vc = Arc::clone(&shared_vec);
        handles.push(thread::spawn(move || {
            vc.lock().unwrap().push(i * 10);
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("共享 Vec: {:?}", *shared_vec.lock().unwrap());
}
```

### 9.3 通道 (Channel)：mpsc

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

// Input: 無 | Process: 通道傳遞訊息 | Output: 接收到的訊息
fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        for msg in vec!["你好", "來自", "子執行緒"] {
            tx.send(msg.to_string()).unwrap();
            thread::sleep(Duration::from_millis(200));
        }
    });

    for received in rx { println!("收到: {}", received); }

    // 多個生產者
    let (tx, rx) = mpsc::channel();
    for i in 0..3 {
        let tx_clone = tx.clone();
        thread::spawn(move || {
            tx_clone.send(format!("來自執行緒 {}", i)).unwrap();
        });
    }
    drop(tx);
    for msg in rx { println!("{}", msg); }
}
```

### 9.4 Send 和 Sync trait

```
Send: 可在執行緒間傳送所有權  |  Sync: 可被多執行緒同時引用
幾乎所有基本型別都是 Send + Sync
例外: Rc<T> 不是 Send（改用 Arc<T>）

Python: GIL → 不擔心（但無法真正平行）
Go:     goroutine → 執行期檢查
Rust:   Send/Sync → 編譯期保證，資料競爭不可能
```

---

## 10. Cargo 與專案管理

### 10.1 專案結構

```
my_project/
├── Cargo.toml       ← 專案設定 + 依賴
├── Cargo.lock       ← 鎖定版本
├── src/
│   ├── main.rs      ← 二進位 crate 進入點
│   ├── lib.rs       ← 函式庫 crate 進入點
│   ├── config.rs    ← 模組檔案
│   └── models/
│       ├── mod.rs   ← 模組宣告
│       ├── user.rs
│       └── task.rs
├── tests/           ← 整合測試
├── benches/         ← 效能基準
└── examples/        ← 範例程式
```

### 10.2 模組系統 (mod)

```rust
// === src/lib.rs ===
pub mod config;
pub mod models;

// === src/config.rs ===
pub struct AppConfig {
    pub port: u16,
    pub host: String,
    debug: bool,       // 未標 pub → 私有
}
impl AppConfig {
    pub fn new() -> Self {
        AppConfig { port: 8080, host: "localhost".into(), debug: false }
    }
    pub fn is_debug(&self) -> bool { self.debug }
}

// === src/models/mod.rs ===
pub mod user;
pub mod task;
pub use user::User;    // 重新匯出
pub use task::Task;

// === src/models/user.rs ===
#[derive(Debug)]
pub struct User { pub name: String, pub email: String }
impl User {
    pub fn new(name: &str, email: &str) -> Self {
        User { name: name.into(), email: email.into() }
    }
}
```

### 10.3 可見性規則

```
pub        — 公開            │ Python name   → Rust pub name
pub(crate) — crate 內部公開  │ Python _name  → Rust name（私有）
pub(super) — 父模組可存取    │ Python 私有是慣例，Rust 私有是編譯器強制
（無標注）  — 私有
```

### 10.4 Cargo 常用指令

```bash
cargo new my_app           # 二進位專案
cargo new my_lib --lib     # 函式庫專案
cargo build --release      # Release 編譯
cargo run -- arg1 arg2     # 傳入命令列參數
cargo test -- --nocapture  # 測試顯示 println
cargo add serde            # 加入依賴
cargo doc --open           # 生成文件
cargo fmt                  # 格式化（類似 black）
cargo clippy               # 靜態分析（類似 pylint）
```

---

## 11. 巨集 (Macros) 入門

### 11.1 常用內建巨集

```rust
fn main() {
    println!("Hello, {}!", "world");     // 格式化印出
    let v = vec![1, 2, 3];              // 建立 Vec
    let s = format!("數字: {}", 42);    // 格式化字串（不印出）
    let x = 5;
    dbg!(x * 2);                        // 除錯: [src/main.rs:5] x * 2 = 10
    // todo!("還沒實作");               // 標記未實作（panic）
    assert_eq!(2 + 2, 4);              // 斷言
    assert_ne!(2 + 2, 5);
    if cfg!(target_os = "windows") { println!("Win"); }
    println!("{:?}, {}", v, s);
}
```

### 11.2 宣告式巨集 macro_rules!

```rust
// Input: key => value 對 | Process: 建立 HashMap | Output: HashMap
macro_rules! hashmap {
    ($($key:expr => $value:expr),* $(,)?) => {{
        let mut map = std::collections::HashMap::new();
        $(map.insert($key, $value);)*
        map
    }};
}

macro_rules! say_hello {
    () => { println!("Hello!"); };
    ($name:expr) => { println!("Hello, {}!", $name); };
}

macro_rules! max_of {
    ($x:expr) => ($x);
    ($x:expr, $($rest:expr),+) => {
        std::cmp::max($x, max_of!($($rest),+))
    };
}

fn main() {
    let scores = hashmap! { "Alice" => 95, "Bob" => 87 };
    println!("{:?}", scores);
    say_hello!();
    say_hello!("Rust");
    println!("最大: {}", max_of!(1, 5, 3, 9, 2));  // 9
}
```

### 11.3 derive 巨集

```rust
#[derive(Debug, Clone, PartialEq, Default)]
struct Config { name: String, value: i32, enabled: bool }

fn main() {
    let c1 = Config { name: "test".into(), value: 42, enabled: true };
    let c2 = c1.clone();
    println!("{:?}", c1);
    println!("相等: {}", c1 == c2);
    println!("預設: {:?}", Config::default());  // { name: "", value: 0, enabled: false }
}
```

| Rust | Python | 說明 |
|------|--------|------|
| `macro_rules!` | 無直接對應 | 編譯期程式碼生成 |
| `#[derive(...)]` | `@dataclass` | 自動生成方法 |
| `#[test]` | `@pytest.mark` | 標記測試 |
| `#[allow(unused)]` | `# noqa` | 忽略警告 |

---

## 12. 完整迷你專案：CLI 任務管理器

```rust
// ============================================================
// CLI 任務管理器 — src/main.rs
// 編譯執行: cargo run
// 整合: struct, enum, impl, match, Vec, Result, 閉包, I/O
// ============================================================

use std::io::{self, Write};

/// 任務狀態
#[derive(Debug, Clone, PartialEq)]
enum Status { Pending, Done }

/// 單一任務
#[derive(Debug, Clone)]
struct Task { id: u32, title: String, status: Status }

impl Task {
    /// Input: id, title | Process: 建立任務 | Output: Task
    fn new(id: u32, title: &str) -> Self {
        Task { id, title: title.to_string(), status: Status::Pending }
    }

    /// Input: &mut self | Process: 標記完成 | Output: 無
    fn complete(&mut self) { self.status = Status::Done; }

    /// Input: &self | Process: 格式化顯示 | Output: String
    fn display(&self) -> String {
        let icon = match self.status {
            Status::Pending => "[ ]",
            Status::Done => "[x]",
        };
        format!("{} #{}: {}", icon, self.id, self.title)
    }
}

/// 任務管理器
struct TaskManager { tasks: Vec<Task>, next_id: u32 }

impl TaskManager {
    /// Input: 無 | Process: 建立空管理器 | Output: TaskManager
    fn new() -> Self { TaskManager { tasks: Vec::new(), next_id: 1 } }

    /// Input: &mut self, title | Process: 新增任務 | Output: 新 ID
    fn add(&mut self, title: &str) -> u32 {
        let id = self.next_id;
        self.tasks.push(Task::new(id, title));
        self.next_id += 1;
        id
    }

    /// Input: &mut self, id | Process: 標記完成 | Output: Result
    fn complete(&mut self, id: u32) -> Result<(), String> {
        match self.tasks.iter_mut().find(|t| t.id == id) {
            Some(task) => { task.complete(); Ok(()) }
            None => Err(format!("找不到任務 #{}", id)),
        }
    }

    /// Input: &mut self, id | Process: 刪除任務 | Output: Result
    fn remove(&mut self, id: u32) -> Result<String, String> {
        match self.tasks.iter().position(|t| t.id == id) {
            Some(i) => { let t = self.tasks.remove(i); Ok(format!("已刪除: {}", t.title)) }
            None => Err(format!("找不到任務 #{}", id)),
        }
    }

    /// Input: &self | Process: 列出所有任務 | Output: 印出
    fn list(&self) {
        if self.tasks.is_empty() { println!("  (沒有任務)"); return; }
        for task in &self.tasks { println!("  {}", task.display()); }
        let done = self.tasks.iter().filter(|t| t.status == Status::Done).count();
        println!("  --- 共 {} 個，完成 {} 個 ---", self.tasks.len(), done);
    }
}

/// Input: prompt | Process: 讀取標準輸入 | Output: String
fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().to_string()
}

/// Input: 無 | Process: 主迴圈 | Output: 無
fn main() {
    let mut mgr = TaskManager::new();
    println!("=== Rust 任務管理器 ===");
    println!("指令: add <標題> | done <ID> | rm <ID> | list | quit\n");

    loop {
        let input = read_input("> ");
        let parts: Vec<&str> = input.splitn(2, ' ').collect();

        match parts[0] {
            "add" => {
                if parts.len() < 2 || parts[1].is_empty() {
                    println!("  用法: add <標題>"); continue;
                }
                let id = mgr.add(parts[1]);
                println!("  已新增 #{}: {}", id, parts[1]);
            }
            "done" => {
                if parts.len() < 2 { println!("  用法: done <ID>"); continue; }
                match parts[1].parse::<u32>() {
                    Ok(id) => match mgr.complete(id) {
                        Ok(()) => println!("  #{} 已完成!", id),
                        Err(e) => println!("  錯誤: {}", e),
                    },
                    Err(_) => println!("  請輸入有效數字"),
                }
            }
            "rm" => {
                if parts.len() < 2 { println!("  用法: rm <ID>"); continue; }
                match parts[1].parse::<u32>() {
                    Ok(id) => match mgr.remove(id) {
                        Ok(msg) => println!("  {}", msg),
                        Err(e) => println!("  錯誤: {}", e),
                    },
                    Err(_) => println!("  請輸入有效數字"),
                }
            }
            "list" => mgr.list(),
            "quit" | "exit" | "q" => { println!("  再見!"); break; }
            "" => continue,
            other => {
                println!("  未知: '{}' | 可用: add | done | rm | list | quit", other);
            }
        }
    }
}
```

### 執行範例

```
=== Rust 任務管理器 ===
指令: add <標題> | done <ID> | rm <ID> | list | quit

> add 學習 Rust 所有權系統
  已新增 #1: 學習 Rust 所有權系統
> add 完成迭代器練習
  已新增 #2: 完成迭代器練習
> list
  [ ] #1: 學習 Rust 所有權系統
  [ ] #2: 完成迭代器練習
  --- 共 2 個，完成 0 個 ---
> done 1
  #1 已完成!
> rm 2
  已刪除: 完成迭代器練習
> list
  [x] #1: 學習 Rust 所有權系統
  --- 共 1 個，完成 1 個 ---
> quit
  再見!
```

---

## 附錄：Python 轉 Rust 速查表

| 情境 | Python | Rust |
|------|--------|------|
| 變數 | `x = 5` | `let x = 5;` |
| 可變 | `x = 5; x = 10` | `let mut x = 5; x = 10;` |
| 字串 | `s = "hello"` | `let s = String::from("hello");` |
| 字面值 | `s = "hello"` | `let s: &str = "hello";` |
| 陣列 | `[1, 2, 3]` | `vec![1, 2, 3]` |
| 字典 | `{"a": 1}` | `HashMap::from([("a", 1)])` |
| 函式 | `def f(x): return x+1` | `fn f(x: i32) -> i32 { x + 1 }` |
| Lambda | `lambda x: x+1` | `\|x\| x + 1` |
| None | `None` | `Option::None` |
| 類別 | `class Foo:` | `struct Foo {}` + `impl Foo {}` |
| 繼承 | `class B(A):` | 無繼承，用 trait + 組合 |
| 介面 | `ABC` | `trait` |
| 例外 | `try/except` | `match Ok/Err` 或 `?` |
| 迭代 | `for x in list:` | `for x in &list {}` |
| 推導 | `[x*2 for x in l]` | `l.iter().map(\|&x\| x*2).collect()` |
| 印出 | `print(f"{x}")` | `println!("{}", x);` |
| 匯入 | `import os` | `use std::fs;` |
| 套件 | `pip install` | `cargo add` |
| 測試 | `pytest` | `cargo test` |
| 格式化 | `black` | `cargo fmt` |
| Lint | `ruff` | `cargo clippy` |

---

## 學習路線建議

```
第 1 週: 基本語法 + 所有權概念（第 1~2 章）→ 理解 move/borrow
第 2 週: 型別 + 函式 + 閉包（第 3~4 章）→ String vs &str, Option/Result
第 3 週: Struct + Enum + Trait（第 5~6 章）→ 實作資料模型
第 4 週: 錯誤處理 + 迭代器（第 7~8 章）→ ? 運算子，鏈式迭代
第 5 週: 並發 + 專案管理（第 9~10 章）→ 多執行緒程式
第 6 週: 完整專案（第 12 章）→ 從零建構 CLI 工具

推薦資源:
- The Rust Programming Language: https://doc.rust-lang.org/book/
- Rustlings 練習: https://github.com/rust-lang/rustlings
- Rust By Example: https://doc.rust-lang.org/rust-by-example/
```
