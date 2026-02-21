# EP04 — JavaScript / TypeScript 全端開發

> **對象讀者**：具備 Python 基礎的開發者，想跨足前後端（Full-Stack）開發。
> 本篇以 Python 為對照，系統性帶入 JavaScript（ES2024）與 TypeScript 5.x 的核心知識。

---

## 目錄

1. [JavaScript vs Python 基本對照](#1-javascript-vs-python-基本對照)
2. [函式三種寫法](#2-函式三種寫法)
3. [非同步程式設計](#3-非同步程式設計--js-最大特色)
4. [陣列操作 (Array Methods)](#4-陣列操作-array-methods)
5. [物件與類別](#5-物件與類別)
6. [模組系統](#6-模組系統)
7. [TypeScript 完整入門](#7-typescript-完整入門)
8. [TypeScript 進階](#8-typescript-進階)
9. [Node.js 基礎](#9-nodejs-基礎)
10. [前端框架概覽](#10-前端框架概覽)
11. [實用工具鏈](#11-實用工具鏈)

---

## 1. JavaScript vs Python 基本對照

### 1.1 變數宣告：let / const / var

```javascript
// ─── JavaScript ───
// const: 不可重新賦值（類似 Python 的常數慣例 ALL_CAPS，但 JS 是語法層級保證）
const PI = 3.14159;
// PI = 3;  // TypeError: Assignment to constant variable.

// let: 可重新賦值，區塊作用域 (block scope)
let counter = 0;
counter = 1;  // OK

// var: 舊式宣告，函式作用域 (function scope)，有 hoisting 問題，現代程式碼應避免
var oldStyle = "deprecated";

// ─── 作用域差異示範 ───
if (true) {
    let blockScoped = "只在 if 內可見";
    var functionScoped = "整個函式都可見";
}
// console.log(blockScoped);    // ReferenceError
console.log(functionScoped);    // "整個函式都可見"  <-- var 的陷阱
```

```python
# ─── Python 對照 ───
PI = 3.14159        # 慣例大寫，但 Python 無法阻止重新賦值
counter = 0
counter = 1         # Python 變數永遠可重新賦值
```

**重點整理**：
| 特性 | `const` | `let` | `var` |
|------|---------|-------|-------|
| 可重新賦值 | 否 | 是 | 是 |
| 作用域 | 區塊 | 區塊 | 函式 |
| Hoisting | 有 (TDZ) | 有 (TDZ) | 有 (初始化為 undefined) |
| 建議使用 | 優先 | 需要時 | 避免 |

### 1.2 七種原始型別 + Object

```javascript
// ─── JavaScript 的 8 種資料型別 ───

// 7 種原始型別 (Primitive)
const num = 42;                  // number（整數浮點數都是 number）
const str = "Hello";             // string
const bool = true;               // boolean
const nothing = null;            // null（刻意設定為空）
const notDefined = undefined;    // undefined（尚未賦值）
const bigNum = 9007199254740993n; // bigint（超大整數）
const id = Symbol("unique");     // symbol（唯一識別符）

// 1 種參考型別 (Reference)
const obj = { name: "Alice" };   // object（含陣列、函式、日期等）

// 型別檢查
console.log(typeof num);         // "number"
console.log(typeof str);         // "string"
console.log(typeof bool);        // "boolean"
console.log(typeof nothing);     // "object"  <-- 歷史遺留 bug！
console.log(typeof notDefined);  // "undefined"
console.log(typeof bigNum);      // "bigint"
console.log(typeof id);          // "symbol"
console.log(typeof obj);         // "object"
```

```python
# ─── Python 對照 ───
num = 42              # int
flt = 3.14            # float（JS 沒有分 int/float）
s = "Hello"           # str
b = True              # bool
nothing = None        # NoneType
# Python 沒有 undefined、symbol、bigint 原始型別
```

### 1.3 console.log vs print

```javascript
// ─── JavaScript 輸出 ───
console.log("一般訊息");          // 標準輸出
console.error("錯誤訊息");        // 標準錯誤（紅色）
console.warn("警告訊息");         // 警告（黃色）
console.table([                   // 表格形式顯示
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 }
]);
console.time("計時器");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("計時器");         // 計時器: 3.456ms
```

```python
# ─── Python 對照 ───
print("一般訊息")
import sys
print("錯誤訊息", file=sys.stderr)
# Python 沒有內建的 console.table / console.time
```

### 1.4 嚴格比較 === vs 寬鬆比較 ==

```javascript
// ─── 嚴格比較 ===：型別 + 值 都要相同 ───
console.log(1 === 1);        // true
console.log(1 === "1");      // false（型別不同）
console.log(null === undefined); // false

// ─── 寬鬆比較 ==：會自動型別轉換（type coercion）───
console.log(1 == "1");       // true  <-- 危險！"1" 被轉為數字
console.log(0 == false);     // true  <-- 危險！
console.log(null == undefined); // true
console.log("" == false);    // true  <-- 危險！

// 結論：永遠使用 ===，除非你非常清楚自己在做什麼
```

```python
# ─── Python 對照 ───
# Python 的 == 比較接近 JS 的 ===（不會自動轉型）
print(1 == "1")    # False
print(0 == False)  # True（Python 中 bool 是 int 的子類別）
# Python 用 is 比較身份（類似 JS 的 Object.is）
```

### 1.5 真值 (Truthy) 與假值 (Falsy)

```javascript
// ─── JavaScript 的 falsy 值（只有這 8 個）───
// false, 0, -0, 0n, "", null, undefined, NaN

// 其餘全部為 truthy（包括空陣列 [] 和空物件 {}！）
if ([]) console.log("空陣列是 truthy！");  // 會印出
if ({}) console.log("空物件是 truthy！");  // 會印出

// 常見陷阱對照
console.log(Boolean(0));          // false
console.log(Boolean(""));         // false
console.log(Boolean("0"));        // true  <-- 非空字串
console.log(Boolean([]));         // true  <-- Python 中 [] 是 falsy！
console.log(Boolean({}));         // true  <-- Python 中 {} 是 falsy！
console.log(Boolean(null));       // false
console.log(Boolean(undefined));  // false
```

```python
# ─── Python 對照 ───
# Python 的 falsy: False, 0, 0.0, "", [], {}, set(), None, 0j
print(bool([]))   # False  <-- 與 JS 不同！
print(bool({}))   # False  <-- 與 JS 不同！
print(bool("0"))  # True（非空字串，與 JS 相同）
```

### 1.6 Template Literals vs f-string

```javascript
// ─── JavaScript Template Literals（反引號 ` ）───
const name = "Alice";
const age = 30;

// 字串插值
const greeting = `你好，我是 ${name}，今年 ${age} 歲`;

// 多行字串（不需要 \n）
const multiLine = `
  第一行
  第二行
  第三行
`;

// 嵌入表達式
const result = `1 + 2 = ${1 + 2}`;  // "1 + 2 = 3"

// Tagged Template Literals（進階）
function highlight(strings, ...values) {
    let result = "";
    strings.forEach((str, i) => {
        result += str;
        if (i < values.length) {
            result += `【${values[i]}】`;
        }
    });
    return result;
}
const output = highlight`姓名: ${name}, 年齡: ${age}`;
// "姓名: 【Alice】, 年齡: 【30】"
console.log(output);
```

```python
# ─── Python 對照 ───
name = "Alice"
age = 30
greeting = f"你好，我是 {name}，今年 {age} 歲"
multi_line = """
  第一行
  第二行
"""
```

---

## 2. 函式三種寫法

### 2.1 Function Declaration（函式宣告）

```javascript
// Input:  兩個數字 a, b
// Process: 將 a 與 b 相加
// Output:  回傳相加結果 (number)
function add(a, b) {
    return a + b;
}
console.log(add(3, 5));  // 8

// 特點：有 hoisting，可以在宣告前呼叫
console.log(multiply(3, 4));  // 12（不會報錯）
function multiply(a, b) {
    return a * b;
}
```

### 2.2 Function Expression（函式表達式）

```javascript
// Input:  兩個數字 a, b
// Process: 將 a 減去 b
// Output:  回傳相減結果 (number)
const subtract = function(a, b) {
    return a - b;
};
console.log(subtract(10, 3));  // 7

// 沒有 hoisting，不能在宣告前呼叫
// console.log(divide(10, 2));  // ReferenceError
const divide = function(a, b) {
    if (b === 0) throw new Error("除數不能為零");
    return a / b;
};
```

### 2.3 Arrow Function（箭頭函式）

```javascript
// ─── 完整寫法 ───
// Input:  兩個數字 a, b
// Process: 計算 a 的 b 次方
// Output:  回傳計算結果 (number)
const power = (a, b) => {
    return Math.pow(a, b);
};

// ─── 簡寫：單一表達式可省略 {} 和 return ───
const square = (x) => x * x;

// ─── 單一參數可省略括號 ───
const double = x => x * 2;

// ─── 無參數必須保留括號 ───
const getTimestamp = () => Date.now();

// ─── 回傳物件字面值需要用括號包裹 ───
const createUser = (name, age) => ({ name: name, age: age });

console.log(power(2, 10));        // 1024
console.log(square(9));           // 81
console.log(double(21));          // 42
console.log(getTimestamp());      // 1708500000000
console.log(createUser("A", 25)); // { name: "A", age: 25 }
```

### 2.4 對比 Python: def vs lambda

```javascript
// ─── JavaScript ───
const greet = (name) => `Hello, ${name}!`;
const nums = [1, 2, 3, 4, 5];
const doubled = nums.map(x => x * 2);  // [2, 4, 6, 8, 10]
```

```python
# ─── Python 對照 ───
greet = lambda name: f"Hello, {name}!"
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))  # [2, 4, 6, 8, 10]
# 或用 list comprehension
doubled = [x * 2 for x in nums]
```

### 2.5 預設參數與 Rest Parameters

```javascript
// ─── 預設參數 ───
// Input:  name(string), greeting(string, 預設 "Hello")
// Process: 組合問候語
// Output:  回傳問候字串 (string)
function greetUser(name, greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
console.log(greetUser("Alice"));           // "Hello, Alice!"
console.log(greetUser("Alice", "Hi"));     // "Hi, Alice!"

// ─── Rest Parameters（收集剩餘參數為陣列）───
// Input:  第一個數字 first, 其餘數字 ...rest
// Process: 計算總和
// Output:  回傳總和 (number)
function sum(first, ...rest) {
    console.log(`第一個: ${first}`);
    console.log(`其餘: [${rest}]`);
    return first + rest.reduce((acc, val) => acc + val, 0);
}
console.log(sum(1, 2, 3, 4, 5));  // 15
```

```python
# ─── Python 對照 ───
def greet_user(name, greeting="Hello"):
    return f"{greeting}, {name}!"

def sum_all(first, *rest):    # *args 類似 ...rest
    return first + sum(rest)
```

### 2.6 解構賦值 (Destructuring)

```javascript
// ─── 陣列解構 ───
const [a, b, c] = [1, 2, 3];
console.log(a, b, c);  // 1 2 3

// 跳過元素
const [first, , third] = [10, 20, 30];
console.log(first, third);  // 10 30

// 搭配 rest
const [head, ...tail] = [1, 2, 3, 4, 5];
console.log(head);  // 1
console.log(tail);  // [2, 3, 4, 5]

// ─── 物件解構 ───
const user = { name: "Alice", age: 30, city: "Taipei" };
const { name, age, city } = user;
console.log(name, age, city);  // "Alice" 30 "Taipei"

// 重新命名
const { name: userName, age: userAge } = user;
console.log(userName);  // "Alice"

// 預設值
const { name: n, country = "Taiwan" } = user;
console.log(country);  // "Taiwan"（user 沒有 country 屬性）

// ─── 函式參數解構 ───
// Input:  一個使用者物件 { name, age, role }
// Process: 格式化使用者資訊
// Output:  回傳格式化字串 (string)
function formatUser({ name, age, role = "member" }) {
    return `${name} (${age}) - ${role}`;
}
console.log(formatUser({ name: "Bob", age: 25 }));
// "Bob (25) - member"
```

```python
# ─── Python 對照 ───
a, b, c = [1, 2, 3]
head, *tail = [1, 2, 3, 4, 5]
# Python 沒有物件解構，但有字典取值
user = {"name": "Alice", "age": 30}
name = user["name"]
```

---

## 3. 非同步程式設計 — JS 最大特色

### 3.1 Event Loop 圖解

```
 ┌──────────────────────────────────────────────────┐
 │                    Call Stack                     │
 │  （同步程式碼在此執行，一次只能執行一個任務）        │
 └──────────────┬───────────────────────────────────┘
                │ 遇到非同步任務時，
                │ 交給 Web API / Node API 處理
                ▼
 ┌──────────────────────────────────────────────────┐
 │              Web APIs / Node APIs                 │
 │  setTimeout, fetch, fs.readFile, DOM events ...   │
 └──────────────┬───────────────────────────────────┘
                │ 任務完成後，
                │ callback 進入任務佇列
                ▼
 ┌──────────────────────────────────────────────────┐
 │          Task Queue (Macro / Micro)               │
 │  Microtask: Promise.then, queueMicrotask          │
 │  Macrotask: setTimeout, setInterval, I/O          │
 └──────────────┬───────────────────────────────────┘
                │ Event Loop 持續檢查：
                │ Call Stack 空了嗎？
                │ → 是 → 從 Queue 取出下一個任務
                ▼
        ┌───────────────┐
        │  Event Loop   │ ← 不斷循環
        └───────────────┘
```

**執行順序規則**：
1. 同步程式碼優先執行
2. Microtask（Promise.then）次之
3. Macrotask（setTimeout）最後

```javascript
// ─── 經典面試題：執行順序是？ ───
console.log("1 - 同步");

setTimeout(() => {
    console.log("2 - setTimeout (macrotask)");
}, 0);

Promise.resolve().then(() => {
    console.log("3 - Promise.then (microtask)");
});

console.log("4 - 同步");

// 輸出順序：
// 1 - 同步
// 4 - 同步
// 3 - Promise.then (microtask)
// 2 - setTimeout (macrotask)
```

### 3.2 Callback（回呼函式）

```javascript
// ─── Callback 風格（最早期的非同步模式）───
// Input:  userId (number), callback (function)
// Process: 模擬從資料庫讀取使用者（延遲 1 秒）
// Output:  透過 callback 回傳使用者物件或錯誤
function getUserCallback(userId, callback) {
    setTimeout(() => {
        if (userId <= 0) {
            callback(new Error("無效的使用者 ID"), null);
            return;
        }
        const user = { id: userId, name: "Alice", email: "alice@example.com" };
        callback(null, user);
    }, 1000);
}

// 使用方式
getUserCallback(1, (error, user) => {
    if (error) {
        console.error("錯誤:", error.message);
        return;
    }
    console.log("使用者:", user);
});

// ─── Callback Hell（回呼地獄）───
// 當多個非同步操作相依時，程式碼會不斷向右縮排
getUserCallback(1, (err, user) => {
    if (err) return console.error(err);
    getUserCallback(2, (err, friend) => {
        if (err) return console.error(err);
        getUserCallback(3, (err, anotherFriend) => {
            if (err) return console.error(err);
            console.log("所有使用者:", user, friend, anotherFriend);
            // 繼續嵌套下去... 可讀性極差
        });
    });
});
```

### 3.3 Promise

```javascript
// ─── Promise 基本結構 ───
// Input:  userId (number)
// Process: 模擬非同步查詢使用者
// Output:  回傳 Promise<User>，resolve 時帶使用者物件，reject 時帶錯誤
function getUser(userId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (userId <= 0) {
                reject(new Error("無效的使用者 ID"));
                return;
            }
            resolve({ id: userId, name: "Alice", email: "alice@example.com" });
        }, 1000);
    });
}

// ─── .then / .catch 鏈式呼叫 ───
getUser(1)
    .then(user => {
        console.log("使用者:", user);
        return getUser(2);  // 回傳另一個 Promise，形成鏈
    })
    .then(user2 => {
        console.log("使用者2:", user2);
    })
    .catch(error => {
        console.error("發生錯誤:", error.message);
    })
    .finally(() => {
        console.log("無論成功或失敗都會執行");
    });

// ─── Promise 靜態方法 ───
// Promise.all: 全部成功才成功，一個失敗就失敗
// Input:  Promise 陣列
// Output: 回傳所有結果的陣列
const p1 = getUser(1);
const p2 = getUser(2);
const p3 = getUser(3);

Promise.all([p1, p2, p3])
    .then(users => {
        console.log("全部使用者:", users);
    })
    .catch(error => {
        console.error("其中一個失敗:", error.message);
    });

// Promise.allSettled: 等全部完成，不論成敗
Promise.allSettled([getUser(1), getUser(-1)])
    .then(results => {
        results.forEach(result => {
            if (result.status === "fulfilled") {
                console.log("成功:", result.value);
            } else {
                console.log("失敗:", result.reason.message);
            }
        });
    });

// Promise.race: 取最快完成的那一個
// Promise.any:  取最快成功的那一個（忽略失敗）
```

### 3.4 async / await

```javascript
// ─── async/await：Promise 的語法糖，讓非同步看起來像同步 ───

// Input:  userId (number)
// Process: 模擬非同步查詢使用者（回傳 Promise）
// Output:  Promise<{ id, name, email }>
function fetchUser(userId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (userId <= 0) {
                reject(new Error(`使用者 ${userId} 不存在`));
                return;
            }
            resolve({ id: userId, name: `User_${userId}`, email: `user${userId}@test.com` });
        }, 500);
    });
}

// Input:  無
// Process: 依序取得三個使用者資料
// Output:  印出使用者資訊（無回傳值）
async function loadUsers() {
    try {
        const user1 = await fetchUser(1);   // 等待 Promise resolve
        console.log("使用者1:", user1);

        const user2 = await fetchUser(2);
        console.log("使用者2:", user2);

        const user3 = await fetchUser(3);
        console.log("使用者3:", user3);
    } catch (error) {
        console.error("載入失敗:", error.message);
    } finally {
        console.log("載入流程結束");
    }
}

loadUsers();

// ─── 平行執行（效能優化）───
// Input:  無
// Process: 同時發出三個請求，等全部完成
// Output:  印出所有使用者
async function loadUsersParallel() {
    try {
        const [u1, u2, u3] = await Promise.all([
            fetchUser(1),
            fetchUser(2),
            fetchUser(3)
        ]);
        console.log("平行結果:", u1, u2, u3);
    } catch (error) {
        console.error("平行載入失敗:", error.message);
    }
}
```

### 3.5 對比 Python asyncio

```javascript
// ─── JavaScript async/await ───
async function fetchData() {
    const response = await fetch("https://api.example.com/data");
    const data = await response.json();
    return data;
}
fetchData().then(data => console.log(data));
```

```python
# ─── Python asyncio 對照 ───
import asyncio
import aiohttp

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/data") as response:
            data = await response.json()
            return data

# Python 必須用 asyncio.run() 啟動事件循環
asyncio.run(fetch_data())

# 關鍵差異：
# - JS: 天生單執行緒 + Event Loop，async 是「預設模式」
# - Python: 預設同步，asyncio 是「額外引入」的機制
# - JS: 任何地方都能用 await（top-level await 在 ESM 模組中可用）
# - Python: 必須在 async def 內才能用 await
```

### 3.6 fetch API 範例

```javascript
// ─── 使用 fetch 發送 HTTP 請求 ───

// GET 請求
// Input:  API URL (string)
// Process: 發送 GET 請求，解析 JSON
// Output:  回傳 Promise<object> 解析後的資料
async function getPost(postId) {
    const url = `https://jsonplaceholder.typicode.com/posts/${postId}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
}

// POST 請求
// Input:  title (string), body (string), userId (number)
// Process: 發送 POST 請求建立新文章
// Output:  回傳 Promise<object> 新建的文章物件
async function createPost(title, body, userId) {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, body, userId })
    });

    if (!response.ok) {
        throw new Error(`建立失敗: ${response.status}`);
    }

    const newPost = await response.json();
    return newPost;
}
```

### 3.7 完整範例：連續呼叫 3 個 API

```javascript
// Input:  無
// Process: 連續呼叫三個 API，每一步依賴前一步的結果
// Output:  印出最終整合的資料
async function fetchChainedData() {
    try {
        // 步驟 1：取得使用者
        console.log("步驟 1: 取得使用者...");
        const userResponse = await fetch("https://jsonplaceholder.typicode.com/users/1");
        if (!userResponse.ok) throw new Error("取得使用者失敗");
        const user = await userResponse.json();
        console.log(`使用者: ${user.name}`);

        // 步驟 2：用使用者 ID 取得該使用者的文章
        console.log("步驟 2: 取得文章...");
        const postsResponse = await fetch(
            `https://jsonplaceholder.typicode.com/posts?userId=${user.id}`
        );
        if (!postsResponse.ok) throw new Error("取得文章失敗");
        const posts = await postsResponse.json();
        console.log(`文章數量: ${posts.length}`);

        // 步驟 3：取得第一篇文章的留言
        const firstPost = posts[0];
        console.log("步驟 3: 取得留言...");
        const commentsResponse = await fetch(
            `https://jsonplaceholder.typicode.com/comments?postId=${firstPost.id}`
        );
        if (!commentsResponse.ok) throw new Error("取得留言失敗");
        const comments = await commentsResponse.json();
        console.log(`留言數量: ${comments.length}`);

        // 整合結果
        const result = {
            userName: user.name,
            postTitle: firstPost.title,
            commentCount: comments.length,
            firstComment: comments[0].body
        };

        console.log("最終結果:", JSON.stringify(result, null, 2));
        return result;
    } catch (error) {
        console.error("API 鏈呼叫失敗:", error.message);
        throw error;
    }
}

fetchChainedData();
```

---

## 4. 陣列操作 (Array Methods)

### 4.1 map / filter / reduce / forEach

```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// ─── map：轉換每個元素，回傳新陣列 ───
// Input:  陣列 + 轉換函式
// Process: 對每個元素套用函式
// Output:  新陣列（長度不變）
const doubled = numbers.map(n => n * 2);
console.log(doubled);  // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// ─── filter：篩選元素，回傳符合條件的新陣列 ───
// Input:  陣列 + 判斷函式
// Process: 保留回傳 true 的元素
// Output:  新陣列（長度 <= 原陣列）
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens);  // [2, 4, 6, 8, 10]

// ─── reduce：累積計算，歸納為單一值 ───
// Input:  陣列 + 累積函式 + 初始值
// Process: 依序將每個元素與累積值結合
// Output:  單一值
const sum = numbers.reduce((accumulator, current) => accumulator + current, 0);
console.log(sum);  // 55

// reduce 實用範例：分組統計
const fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"];
const fruitCount = fruits.reduce((counts, fruit) => {
    counts[fruit] = (counts[fruit] || 0) + 1;
    return counts;
}, {});
console.log(fruitCount);  // { apple: 3, banana: 2, cherry: 1 }

// ─── forEach：遍歷（無回傳值，純副作用）───
// Input:  陣列 + 副作用函式
// Process: 對每個元素執行操作
// Output:  undefined（不回傳新陣列）
numbers.forEach((n, index) => {
    console.log(`index ${index}: ${n}`);
});
```

### 4.2 find / some / every

```javascript
const users = [
    { id: 1, name: "Alice", age: 30, active: true },
    { id: 2, name: "Bob", age: 25, active: false },
    { id: 3, name: "Charlie", age: 35, active: true },
    { id: 4, name: "Diana", age: 28, active: true }
];

// ─── find：找到第一個符合條件的元素 ───
// Input:  陣列 + 判斷函式
// Process: 從頭遍歷，找到第一個回傳 true 的
// Output:  該元素或 undefined
const bob = users.find(u => u.name === "Bob");
console.log(bob);  // { id: 2, name: "Bob", age: 25, active: false }

const notFound = users.find(u => u.name === "Eve");
console.log(notFound);  // undefined

// ─── findIndex：找到第一個符合條件的索引 ───
const bobIndex = users.findIndex(u => u.name === "Bob");
console.log(bobIndex);  // 1

// ─── some：是否「至少有一個」元素符合條件 ───
// Input:  陣列 + 判斷函式
// Process: 找到一個 true 就停止
// Output:  boolean
const hasInactive = users.some(u => !u.active);
console.log(hasInactive);  // true

// ─── every：是否「所有」元素都符合條件 ───
// Input:  陣列 + 判斷函式
// Process: 找到一個 false 就停止
// Output:  boolean
const allAdults = users.every(u => u.age >= 18);
console.log(allAdults);  // true
```

### 4.3 展開運算子與對比 Python

```javascript
// ─── 展開運算子 Spread (...) ───
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// 合併陣列
const merged = [...arr1, ...arr2];
console.log(merged);  // [1, 2, 3, 4, 5, 6]

// 複製陣列（淺拷貝）
const copy = [...arr1];

// 展開物件
const defaults = { theme: "dark", lang: "zh-TW", fontSize: 14 };
const userPrefs = { lang: "en", fontSize: 16 };
const settings = { ...defaults, ...userPrefs };
console.log(settings);  // { theme: "dark", lang: "en", fontSize: 16 }
```

```python
# ─── Python 對照 ───
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
merged = [*arr1, *arr2]           # 類似 JS 的 spread

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubled = [n * 2 for n in numbers]              # list comprehension 取代 map
evens = [n for n in numbers if n % 2 == 0]      # list comprehension 取代 filter
total = sum(numbers)                             # 內建 sum 取代 reduce
# Python 的 map/filter 回傳 iterator，需要 list() 包裹
doubled_map = list(map(lambda n: n * 2, numbers))
evens_filter = list(filter(lambda n: n % 2 == 0, numbers))
```

---

## 5. 物件與類別

### 5.1 Object Literal

```javascript
// ─── 物件字面值 ───
const person = {
    firstName: "Alice",
    lastName: "Wang",
    age: 30,

    // 方法簡寫
    getFullName() {
        return `${this.firstName} ${this.lastName}`;
    },

    // 計算屬性名稱
    ["is" + "Adult"]() {
        return this.age >= 18;
    }
};

console.log(person.getFullName());  // "Alice Wang"
console.log(person.isAdult());     // true
console.log(person["age"]);        // 30（中括號存取）

// ─── 屬性簡寫 ───
const name = "Bob";
const age = 25;
const user = { name, age };  // 等同 { name: name, age: age }

// ─── Optional Chaining (?.) ───
const company = {
    name: "TechCorp",
    address: {
        city: "Taipei"
    }
};
console.log(company.address?.city);     // "Taipei"
console.log(company.address?.zipCode);  // undefined（不會報錯）
console.log(company.ceo?.name);         // undefined（不會報錯）

// ─── Nullish Coalescing (??) ───
const config = {
    timeout: 0,        // 0 是有效值
    retries: null       // null 代表未設定
};
const timeout = config.timeout ?? 3000;  // 0（?? 只在 null/undefined 時取預設值）
const retries = config.retries ?? 3;     // 3
// 對比 ||：const timeout = config.timeout || 3000;  // 3000（0 是 falsy！）
```

### 5.2 Class 完整範例

```javascript
// ─── 基礎類別 ───
class Animal {
    // Private field（外部無法存取）
    #sound;

    // Static 屬性
    static kingdom = "Animalia";

    // 建構函式
    // Input:  name (string), sound (string)
    // Process: 初始化實例屬性
    constructor(name, sound) {
        this.name = name;    // 公開屬性
        this.#sound = sound; // 私有屬性
    }

    // Getter
    get info() {
        return `${this.name} says ${this.#sound}`;
    }

    // Setter
    set nickname(value) {
        if (typeof value !== "string" || value.length === 0) {
            throw new Error("暱稱必須是非空字串");
        }
        this._nickname = value;
    }

    get nickname() {
        return this._nickname || this.name;
    }

    // 一般方法
    // Input:  無
    // Process: 組合叫聲字串
    // Output:  回傳字串 (string)
    speak() {
        return `${this.name}: ${this.#sound}!`;
    }

    // 靜態方法（透過類別呼叫，非實例）
    // Input:  Animal 實例陣列
    // Process: 比較名稱長度
    // Output:  回傳名稱最長的 Animal
    static findLongestName(animals) {
        return animals.reduce((longest, current) =>
            current.name.length > longest.name.length ? current : longest
        );
    }
}

// ─── 繼承 ───
class Dog extends Animal {
    #tricks;

    // Input:  name (string)
    // Process: 呼叫父類別建構式，初始化技能陣列
    constructor(name) {
        super(name, "Woof");  // 呼叫父類別的 constructor
        this.#tricks = [];
    }

    // Input:  trick (string)
    // Process: 新增一個技能到技能清單
    // Output:  無
    learnTrick(trick) {
        this.#tricks.push(trick);
    }

    // Input:  無
    // Process: 取得所有技能
    // Output:  回傳技能陣列的副本 (string[])
    getTricks() {
        return [...this.#tricks];
    }

    // 覆寫父類別方法
    speak() {
        return `${this.name}: Woof Woof! (我會 ${this.#tricks.length} 個技能)`;
    }
}

// 使用
const dog = new Dog("Buddy");
dog.learnTrick("坐下");
dog.learnTrick("握手");
console.log(dog.speak());       // "Buddy: Woof Woof! (我會 2 個技能)"
console.log(dog.info);          // "Buddy says Woof"（getter，繼承自 Animal）
console.log(dog.getTricks());   // ["坐下", "握手"]
console.log(Animal.kingdom);    // "Animalia"（靜態屬性）
// console.log(dog.#sound);     // SyntaxError（私有欄位無法從外部存取）
```

### 5.3 對比 Python class

```python
# ─── Python 對照 ───
class Animal:
    kingdom = "Animalia"  # 類別變數（類似 static）

    def __init__(self, name, sound):
        self.name = name        # 公開屬性
        self.__sound = sound    # 名稱修飾（name mangling），非真正私有

    @property
    def info(self):             # 類似 JS getter
        return f"{self.name} says {self.__sound}"

    def speak(self):
        return f"{self.name}: {self.__sound}!"

    @staticmethod
    def find_longest_name(animals):
        return max(animals, key=lambda a: len(a.name))


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")
        self.__tricks = []

    def learn_trick(self, trick):
        self.__tricks.append(trick)

    def speak(self):  # 覆寫
        return f"{self.name}: Woof Woof! (我會 {len(self.__tricks)} 個技能)"
```

---

## 6. 模組系統

### 6.1 ES Modules（現代標準）

```javascript
// ─── math-utils.js（匯出模組）───

// Named Export（具名匯出）
export function add(a, b) {
    return a + b;
}

export function subtract(a, b) {
    return a - b;
}

export const PI = 3.14159;

// Default Export（預設匯出，每個模組只能有一個）
export default class Calculator {
    constructor() {
        this.history = [];
    }

    calculate(a, op, b) {
        let result;
        switch (op) {
            case "+": result = a + b; break;
            case "-": result = a - b; break;
            case "*": result = a * b; break;
            case "/": result = b !== 0 ? a / b : NaN; break;
            default: throw new Error(`不支援的運算子: ${op}`);
        }
        this.history.push({ a, op, b, result });
        return result;
    }
}
```

```javascript
// ─── app.js（匯入模組）───

// 匯入 default export
import Calculator from "./math-utils.js";

// 匯入 named exports
import { add, subtract, PI } from "./math-utils.js";

// 重新命名匯入
import { add as addition } from "./math-utils.js";

// 匯入全部為命名空間
import * as MathUtils from "./math-utils.js";

console.log(add(1, 2));             // 3
console.log(PI);                    // 3.14159
console.log(MathUtils.subtract(5, 3)); // 2

const calc = new Calculator();
console.log(calc.calculate(10, "+", 5)); // 15
```

### 6.2 CommonJS（Node.js 傳統格式）

```javascript
// ─── utils.js（匯出）───
function formatDate(date) {
    return date.toISOString().split("T")[0];
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

module.exports = {
    formatDate,
    capitalize
};

// 或者單一匯出
// module.exports = formatDate;
```

```javascript
// ─── app.js（匯入）───
const { formatDate, capitalize } = require("./utils");

console.log(formatDate(new Date()));  // "2026-02-21"
console.log(capitalize("hello"));    // "Hello"
```

### 6.3 對比 Python import

| JS (ES Modules) | Python | 說明 |
|---|---|---|
| `import X from "./mod"` | `from mod import X` | 預設匯入 |
| `import { a, b } from "./mod"` | `from mod import a, b` | 具名匯入 |
| `import * as M from "./mod"` | `import mod as M` | 命名空間匯入 |
| `export default class X {}` | （無對應，Python 不區分 default） | 預設匯出 |
| `export function f() {}` | 任何頂層定義自動可匯入 | 具名匯出 |

---

## 7. TypeScript 完整入門

### 7.1 為什麼需要 TypeScript

```javascript
// ─── 純 JavaScript 的問題 ───
function processOrder(order) {
    // order 是什麼結構？有哪些屬性？
    // 呼叫者可能傳入任何東西，只有 runtime 才會發現錯誤
    return order.items.map(item => item.price * item.quantity);
}

// 這些呼叫都不會在編譯時報錯：
processOrder(null);                    // Runtime Error!
processOrder({ items: "not array" }); // Runtime Error!
processOrder({ products: [] });       // Runtime Error!（屬性名稱錯誤）
```

```typescript
// ─── TypeScript 解決方案 ───
interface OrderItem {
    name: string;
    price: number;
    quantity: number;
}

interface Order {
    id: string;
    items: OrderItem[];
    createdAt: Date;
}

// Input:  order (Order)
// Process: 計算每個品項的小計
// Output:  回傳小計陣列 (number[])
function processOrder(order: Order): number[] {
    return order.items.map(item => item.price * item.quantity);
}

// 編譯時就會報錯：
// processOrder(null);                     // Error: 型別 'null' 不能指定給 'Order'
// processOrder({ items: "not array" });   // Error: 型別不符
```

### 7.2 基本型別標注

```typescript
// ─── 變數型別標注 ───
const name: string = "Alice";
const age: number = 30;
const isActive: boolean = true;
const scores: number[] = [95, 87, 92];
const pair: [string, number] = ["Alice", 30]; // Tuple（元組）

// ─── 函式型別標注 ───
// Input:  a (number), b (number)
// Process: 相加
// Output:  number
function add(a: number, b: number): number {
    return a + b;
}

// 箭頭函式
const multiply = (a: number, b: number): number => a * b;

// 可選參數（加 ?）
// Input:  name (string), greeting (string, 可選)
// Process: 組合問候語
// Output:  string
function greet(name: string, greeting?: string): string {
    return `${greeting || "Hello"}, ${name}!`;
}

// void：函式不回傳值
function logMessage(msg: string): void {
    console.log(msg);
}

// never：函式永遠不會正常結束
function throwError(message: string): never {
    throw new Error(message);
}
```

### 7.3 interface vs type

```typescript
// ─── interface：定義物件結構的契約 ───
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;             // 可選屬性
    readonly createdAt: Date; // 唯讀屬性
}

// interface 可以被擴展（extends）
interface Admin extends User {
    role: "admin" | "superadmin";
    permissions: string[];
}

// interface 可以被合併宣告（Declaration Merging）
interface User {
    phone?: string;  // 自動與前面的 User 合併
}

// ─── type：型別別名，更靈活 ───
type ID = string | number;  // Union Type

type Point = {
    x: number;
    y: number;
};

// type 可以用交叉型別 (&) 組合
type Timestamped = {
    createdAt: Date;
    updatedAt: Date;
};

type TimestampedPoint = Point & Timestamped;

// type 可以定義 primitive、union、tuple 等
type Status = "pending" | "active" | "inactive";  // 字面值型別
type Coordinate = [number, number];                // Tuple
type Callback = (data: string) => void;            // 函式型別

// ─── 使用範例 ───
const admin: Admin = {
    id: 1,
    name: "Alice",
    email: "alice@admin.com",
    createdAt: new Date(),
    role: "admin",
    permissions: ["read", "write", "delete"]
};

const status: Status = "active";
// const bad: Status = "unknown"; // Error: 型別 '"unknown"' 不能指定給型別 'Status'
```

**何時用 interface？何時用 type？**
| 場景 | 推薦 | 原因 |
|------|------|------|
| 物件結構定義 | `interface` | 可擴展、可合併 |
| Union / Intersection | `type` | interface 不支援 |
| 函式型別 | `type` | 語法更清晰 |
| React Props | `interface` | 社群慣例 |
| 通用選擇 | 都可以 | 團隊統一即可 |

### 7.4 泛型 (Generics)

```typescript
// ─── 問題：沒有泛型時，要嘛失去型別資訊，要嘛重複寫很多版本 ───
function identityAny(value: any): any {
    return value;  // 回傳 any，型別資訊丟失
}

// ─── 泛型解決方案：用 <T> 佔位符 ───
// Input:  value (T) — 任意型別
// Process: 直接回傳（身份函式）
// Output:  T — 與輸入相同的型別
function identity<T>(value: T): T {
    return value;
}

const str = identity<string>("hello");  // 型別: string
const num = identity<number>(42);       // 型別: number
const auto = identity("world");         // 自動推斷為 string

// ─── 泛型用於容器 ───
// Input:  items (T[])
// Process: 隨機選取一個元素
// Output:  T
function randomPick<T>(items: T[]): T {
    const index = Math.floor(Math.random() * items.length);
    return items[index];
}

const fruit = randomPick(["apple", "banana", "cherry"]);  // 型別: string
const score = randomPick([95, 87, 92]);                    // 型別: number

// ─── 泛型約束 (Constraints) ───
interface HasLength {
    length: number;
}

// Input:  value (T extends HasLength) — 必須有 length 屬性
// Process: 檢查長度並回傳描述
// Output:  string
function describeLength<T extends HasLength>(value: T): string {
    return `長度為 ${value.length}`;
}

console.log(describeLength("hello"));     // "長度為 5"
console.log(describeLength([1, 2, 3]));   // "長度為 3"
// describeLength(42);  // Error: number 沒有 length 屬性

// ─── 多個泛型參數 ───
// Input:  key (K), value (V)
// Process: 建立鍵值對物件
// Output:  { key: K, value: V }
function makePair<K, V>(key: K, value: V): { key: K; value: V } {
    return { key, value };
}

const pair = makePair("name", "Alice");  // { key: string, value: string }
const pair2 = makePair(1, true);         // { key: number, value: boolean }

// ─── 泛型 interface ───
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
    timestamp: Date;
}

interface UserData {
    id: number;
    name: string;
}

const userResponse: ApiResponse<UserData> = {
    data: { id: 1, name: "Alice" },
    status: 200,
    message: "OK",
    timestamp: new Date()
};
```

### 7.5 enum 列舉

```typescript
// ─── 數值列舉 ───
enum Direction {
    Up = 0,
    Down = 1,
    Left = 2,
    Right = 3
}

// 也可以不指定值，會自動從 0 開始遞增
enum Color {
    Red,    // 0
    Green,  // 1
    Blue    // 2
}

// ─── 字串列舉（推薦，更安全可讀）───
enum HttpMethod {
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    DELETE = "DELETE",
    PATCH = "PATCH"
}

enum OrderStatus {
    Pending = "PENDING",
    Processing = "PROCESSING",
    Shipped = "SHIPPED",
    Delivered = "DELIVERED",
    Cancelled = "CANCELLED"
}

// 使用
function handleRequest(method: HttpMethod, url: string): void {
    console.log(`${method} ${url}`);
}

handleRequest(HttpMethod.GET, "/api/users");
// handleRequest("GET", "/api/users"); // Error: 型別 '"GET"' 不能指定給 'HttpMethod'

// ─── const enum（編譯時會被內聯，效能更好）───
const enum Sizes {
    Small = "S",
    Medium = "M",
    Large = "L"
}

const mySize = Sizes.Medium; // 編譯後直接變成 "M"
```

### 7.6 Union Types 與 Type Guards

```typescript
// ─── Union Types：多種型別的聯合 ───
type StringOrNumber = string | number;

// Input:  value (string | number)
// Process: 根據型別不同做不同處理
// Output:  string
function formatValue(value: string | number): string {
    // Type Guard：使用 typeof 縮小型別範圍
    if (typeof value === "string") {
        return value.toUpperCase();   // 這裡 TS 知道 value 是 string
    } else {
        return value.toFixed(2);      // 這裡 TS 知道 value 是 number
    }
}

console.log(formatValue("hello"));  // "HELLO"
console.log(formatValue(3.14159));  // "3.14"

// ─── Discriminated Union（可區分聯合型別）───
interface Circle {
    kind: "circle";
    radius: number;
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}

interface Triangle {
    kind: "triangle";
    base: number;
    height: number;
}

type Shape = Circle | Rectangle | Triangle;

// Input:  shape (Shape)
// Process: 根據 kind 屬性計算面積
// Output:  number
function calculateArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rectangle":
            return shape.width * shape.height;
        case "triangle":
            return 0.5 * shape.base * shape.height;
    }
}

console.log(calculateArea({ kind: "circle", radius: 5 }));              // 78.54
console.log(calculateArea({ kind: "rectangle", width: 4, height: 6 })); // 24
console.log(calculateArea({ kind: "triangle", base: 3, height: 8 }));   // 12
```

### 7.7 Utility Types

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    age: number;
    role: string;
}

// ─── Partial<T>：所有屬性變為可選 ───
type PartialUser = Partial<User>;
// 等同: { id?: number; name?: string; email?: string; age?: number; role?: string; }

// 實用場景：更新函式只需傳部分欄位
// Input:  id (number), updates (Partial<User>)
// Process: 合併更新資料
// Output:  User
function updateUser(id: number, updates: Partial<User>): User {
    const existing: User = { id, name: "Alice", email: "a@b.com", age: 30, role: "user" };
    return { ...existing, ...updates };
}
const updated = updateUser(1, { name: "Bob" });  // 只更新 name

// ─── Required<T>：所有屬性變為必要 ───
type RequiredUser = Required<User>;

// ─── Pick<T, K>：挑選部分屬性 ───
type UserPreview = Pick<User, "id" | "name">;
// 等同: { id: number; name: string; }

// ─── Omit<T, K>：排除部分屬性 ───
type UserWithoutId = Omit<User, "id">;
// 等同: { name: string; email: string; age: number; role: string; }

// ─── Record<K, V>：建立鍵值對映射 ───
type UserRoles = Record<string, string[]>;
const rolePermissions: UserRoles = {
    admin: ["read", "write", "delete"],
    editor: ["read", "write"],
    viewer: ["read"]
};

// ─── Readonly<T>：所有屬性變為唯讀 ───
type ReadonlyUser = Readonly<User>;
const frozenUser: ReadonlyUser = { id: 1, name: "A", email: "a@b", age: 1, role: "u" };
// frozenUser.name = "B";  // Error: 無法指定給 'name'，因為它是唯讀屬性

// ─── Extract / Exclude：從 Union 中提取或排除 ───
type AllStatus = "active" | "inactive" | "pending" | "deleted";
type ActiveStatus = Extract<AllStatus, "active" | "pending">;   // "active" | "pending"
type ArchivedStatus = Exclude<AllStatus, "active" | "pending">; // "inactive" | "deleted"
```

### 7.8 對比 Python type hints

```typescript
// ─── TypeScript ───
function greet(name: string, age: number): string {
    return `Hello ${name}, you are ${age}`;
}

interface Config {
    host: string;
    port: number;
    debug?: boolean;
}
```

```python
# ─── Python 對照 ───
from typing import Optional, TypedDict

def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age}"

class Config(TypedDict):
    host: str
    port: int
    debug: NotRequired[bool]   # Python 3.11+

# 關鍵差異：
# - TS: 編譯時強制型別檢查（tsc 會報錯）
# - Python: type hints 只是「註解」，不強制（需 mypy 等工具）
# - TS: 泛型語法 <T> vs Python: Generic[T]
# - TS: interface 可合併 vs Python: Protocol（結構子型別）
```

---

## 8. TypeScript 進階

### 8.1 裝飾器 (Decorators)

```typescript
// ─── 注意：需在 tsconfig.json 中啟用 experimentalDecorators ───

// 方法裝飾器：記錄函式呼叫時間
// Input:  target (物件原型), propertyKey (方法名), descriptor (屬性描述符)
// Process: 包裝原始方法，加上計時邏輯
// Output:  修改後的描述符
function LogExecutionTime(
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
): PropertyDescriptor {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
        const start = performance.now();
        const result = originalMethod.apply(this, args);
        const end = performance.now();
        console.log(`${propertyKey} 執行時間: ${(end - start).toFixed(2)}ms`);
        return result;
    };

    return descriptor;
}

// 類別裝飾器：自動加上 toString 方法
// Input:  constructor (類別建構函式)
// Process: 在原型上加入 toString
// Output:  無（直接修改類別）
function AutoToString(constructor: Function): void {
    constructor.prototype.toString = function () {
        const props = Object.keys(this)
            .map(key => `${key}=${this[key]}`)
            .join(", ");
        return `${constructor.name}(${props})`;
    };
}

// 屬性裝飾器：驗證數值範圍
// Input:  min (number), max (number)
// Process: 建立 setter 驗證邏輯
// Output:  裝飾器函式
function Range(min: number, max: number) {
    return function (target: any, propertyKey: string): void {
        let value: number;
        Object.defineProperty(target, propertyKey, {
            get() {
                return value;
            },
            set(newValue: number) {
                if (newValue < min || newValue > max) {
                    throw new Error(`${propertyKey} 必須在 ${min} 到 ${max} 之間，收到 ${newValue}`);
                }
                value = newValue;
            }
        });
    };
}

@AutoToString
class Product {
    name: string;

    @Range(0, 99999)
    price: number;

    constructor(name: string, price: number) {
        this.name = name;
        this.price = price;
    }

    @LogExecutionTime
    calculateTax(rate: number): number {
        let sum = 0;
        for (let i = 0; i < 1000000; i++) {
            sum += this.price * rate;
        }
        return this.price * rate;
    }
}

const product = new Product("Laptop", 1500);
console.log(product.toString());       // "Product(name=Laptop, price=1500)"
product.calculateTax(0.05);            // "calculateTax 執行時間: 2.34ms"
// product.price = -100;               // Error: price 必須在 0 到 99999 之間
```

### 8.2 條件型別 (Conditional Types)

```typescript
// ─── 條件型別語法：T extends U ? X : Y ───

// 基礎範例
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;   // "yes"
type B = IsString<number>;   // "no"
type C = IsString<"hello">;  // "yes"

// ─── 實用範例：根據型別提取不同部分 ───
type Flatten<T> = T extends Array<infer U> ? U : T;

type Str = Flatten<string[]>;    // string
type Num = Flatten<number[]>;    // number
type Bool = Flatten<boolean>;    // boolean（非陣列，原樣回傳）

// ─── 函式回傳型別提取 ───
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

type R1 = ReturnOf<() => string>;             // string
type R2 = ReturnOf<(x: number) => boolean>;   // boolean

// ─── 實戰：API 回應型別轉換 ───
type ApiEndpoint = "users" | "posts" | "comments";

type ApiResponseType<T extends ApiEndpoint> =
    T extends "users" ? { id: number; name: string } :
    T extends "posts" ? { id: number; title: string; body: string } :
    T extends "comments" ? { id: number; postId: number; text: string } :
    never;

// Input:  endpoint (T extends ApiEndpoint)
// Process: 發送 API 請求
// Output:  Promise<ApiResponseType<T>>
async function fetchApi<T extends ApiEndpoint>(
    endpoint: T
): Promise<ApiResponseType<T>> {
    const response = await fetch(`/api/${endpoint}`);
    return response.json();
}

// 使用時，回傳型別自動推斷
// const user = await fetchApi("users");     // 型別: { id: number; name: string }
// const post = await fetchApi("posts");     // 型別: { id: number; title: string; body: string }
```

### 8.3 映射型別 (Mapped Types)

```typescript
// ─── 映射型別：遍歷型別的每個屬性進行轉換 ───

// 基礎：將所有屬性變為可選
type MyPartial<T> = {
    [K in keyof T]?: T[K];
};

// 基礎：將所有屬性變為唯讀
type MyReadonly<T> = {
    readonly [K in keyof T]: T[K];
};

// ─── 進階：將所有屬性值包裹為 Promise ───
type Promisify<T> = {
    [K in keyof T]: Promise<T[K]>;
};

interface SyncData {
    name: string;
    age: number;
    active: boolean;
}

type AsyncData = Promisify<SyncData>;
// 等同: { name: Promise<string>; age: Promise<number>; active: Promise<boolean>; }

// ─── 進階：為每個屬性自動生成 getter 方法名 ───
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<{ name: string; age: number }>;
// 等同: { getName: () => string; getAge: () => number; }

// ─── 進階：過濾特定型別的屬性 ───
type OnlyStrings<T> = {
    [K in keyof T as T[K] extends string ? K : never]: T[K];
};

interface MixedData {
    id: number;
    name: string;
    email: string;
    age: number;
}

type StringFields = OnlyStrings<MixedData>;
// 等同: { name: string; email: string; }
```

### 8.4 完整範例：API Response 型別系統

```typescript
// ─── 建構一個完整的、型別安全的 API Response 系統 ───

// 基礎型別定義
type HttpStatusCode = 200 | 201 | 400 | 401 | 403 | 404 | 500;

interface PaginationMeta {
    currentPage: number;
    totalPages: number;
    pageSize: number;
    totalItems: number;
}

// 成功回應
interface SuccessResponse<T> {
    success: true;
    data: T;
    meta?: PaginationMeta;
    timestamp: string;
}

// 錯誤回應
interface ErrorResponse {
    success: false;
    error: {
        code: HttpStatusCode;
        message: string;
        details?: Record<string, string[]>;
    };
    timestamp: string;
}

// 聯合型別：API 回應一定是成功或失敗
type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

// 資料模型
interface User {
    id: number;
    name: string;
    email: string;
    role: "admin" | "user" | "guest";
}

interface Post {
    id: number;
    title: string;
    content: string;
    authorId: number;
    tags: string[];
}

// 路由對映射型別
interface ApiEndpoints {
    "GET /users": ApiResponse<User[]>;
    "GET /users/:id": ApiResponse<User>;
    "POST /users": ApiResponse<User>;
    "PUT /users/:id": ApiResponse<User>;
    "DELETE /users/:id": ApiResponse<{ deleted: boolean }>;
    "GET /posts": ApiResponse<Post[]>;
    "GET /posts/:id": ApiResponse<Post>;
}

// 型別安全的 API 客戶端
// Input:  endpoint (E), 請求設定 (RequestInit)
// Process: 發送請求並解析回應
// Output:  Promise<ApiEndpoints[E]>
async function apiClient<E extends keyof ApiEndpoints>(
    endpoint: E,
    config?: RequestInit
): Promise<ApiEndpoints[E]> {
    const [method, path] = (endpoint as string).split(" ");
    const response = await fetch(path, { method, ...config });
    const json = await response.json();
    return json as ApiEndpoints[E];
}

// Type Guard：檢查回應是否成功
// Input:  response (ApiResponse<T>)
// Process: 檢查 success 欄位
// Output:  boolean（並縮小型別範圍）
function isSuccess<T>(response: ApiResponse<T>): response is SuccessResponse<T> {
    return response.success === true;
}

// 使用範例
async function demo(): Promise<void> {
    const response = await apiClient("GET /users");

    if (isSuccess(response)) {
        // TypeScript 知道 response.data 是 User[]
        response.data.forEach(user => {
            console.log(`${user.name} (${user.role})`);
        });
    } else {
        // TypeScript 知道 response.error 存在
        console.error(`錯誤 ${response.error.code}: ${response.error.message}`);
    }
}
```

---

## 9. Node.js 基礎

### 9.1 專案初始化

```bash
# 建立專案目錄並初始化
mkdir my-api && cd my-api
npm init -y                    # 產生 package.json（-y 使用預設值）

# 安裝相依套件
npm install express cors       # 安裝到 dependencies
npm install -D typescript @types/express @types/cors ts-node nodemon
#          -D = --save-dev（開發依賴）

# TypeScript 初始化
npx tsc --init                 # 產生 tsconfig.json
```

### 9.2 package.json 結構

```json
{
    "name": "my-api",
    "version": "1.0.0",
    "description": "我的第一個 Node.js API",
    "main": "dist/index.js",
    "scripts": {
        "dev": "nodemon --exec ts-node src/index.ts",
        "build": "tsc",
        "start": "node dist/index.js",
        "test": "jest"
    },
    "dependencies": {
        "express": "^4.18.2",
        "cors": "^2.8.5"
    },
    "devDependencies": {
        "typescript": "^5.3.0",
        "@types/express": "^4.17.21",
        "@types/cors": "^2.8.17",
        "ts-node": "^10.9.2",
        "nodemon": "^3.0.2"
    }
}
```

### 9.3 內建模組：fs, path, http

```javascript
// ─── fs（檔案系統）───
const fs = require("fs");
const fsPromises = require("fs").promises;

// 同步讀取
// Input:  檔案路徑 (string)
// Process: 讀取檔案內容
// Output:  檔案內容 (string)
const content = fs.readFileSync("./data.txt", "utf-8");
console.log(content);

// 非同步讀取（Promise 版本，推薦）
// Input:  檔案路徑 (string)
// Process: 非同步讀取檔案
// Output:  Promise<string>
async function readFile(filePath) {
    try {
        const data = await fsPromises.readFile(filePath, "utf-8");
        return data;
    } catch (error) {
        console.error("讀取失敗:", error.message);
        throw error;
    }
}

// 寫入檔案
// Input:  filePath (string), content (string)
// Process: 將內容寫入檔案
// Output:  Promise<void>
async function writeFile(filePath, content) {
    await fsPromises.writeFile(filePath, content, "utf-8");
    console.log(`已寫入 ${filePath}`);
}

// ─── path（路徑處理）───
const path = require("path");

console.log(path.join("/users", "alice", "documents", "file.txt"));
// "/users/alice/documents/file.txt"

console.log(path.resolve(".", "src", "index.ts"));
// "/absolute/path/to/src/index.ts"

console.log(path.extname("photo.jpg"));     // ".jpg"
console.log(path.basename("/a/b/c.txt"));   // "c.txt"
console.log(path.dirname("/a/b/c.txt"));    // "/a/b"

// ─── http（原生 HTTP 伺服器）───
const http = require("http");

// Input:  無
// Process: 建立 HTTP 伺服器，處理請求
// Output:  監聽指定 port
const server = http.createServer((req, res) => {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: "Hello from Node.js!" }));
});

server.listen(3000, () => {
    console.log("伺服器啟動: http://localhost:3000");
});
```

### 9.4 Express.js 最小 REST API

```javascript
const express = require("express");
const cors = require("cors");

const app = express();

// 中介軟體 (Middleware)
app.use(cors());                         // 允許跨域請求
app.use(express.json());                 // 解析 JSON body

// Input:  GET /api/hello
// Process: 回傳歡迎訊息
// Output:  JSON { message: string }
app.get("/api/hello", (req, res) => {
    res.json({ message: "Hello, World!" });
});

// Input:  GET /api/hello/:name
// Process: 用 URL 參數組合歡迎訊息
// Output:  JSON { message: string }
app.get("/api/hello/:name", (req, res) => {
    const { name } = req.params;
    res.json({ message: `Hello, ${name}!` });
});

app.listen(3000, () => {
    console.log("API 啟動: http://localhost:3000");
});
```

### 9.5 完整 CRUD API 範例

```javascript
const express = require("express");
const app = express();
app.use(express.json());

// 模擬資料庫（記憶體中的陣列）
let todos = [
    { id: 1, title: "學習 JavaScript", completed: false },
    { id: 2, title: "學習 TypeScript", completed: false }
];
let nextId = 3;

// CREATE - 新增待辦事項
// Input:  POST /api/todos, body: { title: string }
// Process: 建立新的待辦事項並加入陣列
// Output:  201 + 新建的待辦事項物件
app.post("/api/todos", (req, res) => {
    const { title } = req.body;
    if (!title || typeof title !== "string") {
        return res.status(400).json({ error: "title 為必填字串" });
    }
    const newTodo = { id: nextId++, title: title.trim(), completed: false };
    todos.push(newTodo);
    res.status(201).json(newTodo);
});

// READ ALL - 取得所有待辦事項
// Input:  GET /api/todos?completed=true|false（可選篩選）
// Process: 回傳全部或篩選後的待辦事項
// Output:  200 + 待辦事項陣列
app.get("/api/todos", (req, res) => {
    const { completed } = req.query;
    let result = todos;
    if (completed !== undefined) {
        const isCompleted = completed === "true";
        result = todos.filter(t => t.completed === isCompleted);
    }
    res.json(result);
});

// READ ONE - 取得單一待辦事項
// Input:  GET /api/todos/:id
// Process: 依 ID 查找待辦事項
// Output:  200 + 待辦事項物件，或 404
app.get("/api/todos/:id", (req, res) => {
    const id = parseInt(req.params.id, 10);
    const todo = todos.find(t => t.id === id);
    if (!todo) {
        return res.status(404).json({ error: `找不到 ID 為 ${id} 的待辦事項` });
    }
    res.json(todo);
});

// UPDATE - 更新待辦事項
// Input:  PUT /api/todos/:id, body: { title?: string, completed?: boolean }
// Process: 依 ID 查找並更新
// Output:  200 + 更新後的物件，或 404
app.put("/api/todos/:id", (req, res) => {
    const id = parseInt(req.params.id, 10);
    const todo = todos.find(t => t.id === id);
    if (!todo) {
        return res.status(404).json({ error: `找不到 ID 為 ${id} 的待辦事項` });
    }
    const { title, completed } = req.body;
    if (title !== undefined) todo.title = title;
    if (completed !== undefined) todo.completed = completed;
    res.json(todo);
});

// DELETE - 刪除待辦事項
// Input:  DELETE /api/todos/:id
// Process: 依 ID 查找並從陣列移除
// Output:  200 + 確認訊息，或 404
app.delete("/api/todos/:id", (req, res) => {
    const id = parseInt(req.params.id, 10);
    const index = todos.findIndex(t => t.id === id);
    if (index === -1) {
        return res.status(404).json({ error: `找不到 ID 為 ${id} 的待辦事項` });
    }
    const deleted = todos.splice(index, 1)[0];
    res.json({ message: `已刪除: ${deleted.title}`, deleted });
});

app.listen(3000, () => {
    console.log("CRUD API 啟動: http://localhost:3000/api/todos");
});
```

---

## 10. 前端框架概覽

### 10.1 React 基本概念

```
React 核心觀念（對照 Python 思維）：

┌────────────┬──────────────────────────────────┬────────────────────────┐
│ React 概念  │ 說明                             │ Python 類比             │
├────────────┼──────────────────────────────────┼────────────────────────┤
│ Component  │ UI 的基本單元（函式回傳 JSX）       │ 一個 class / function   │
│ Props      │ 外部傳入的參數（唯讀）              │ 函式參數               │
│ State      │ 元件內部的狀態（可變）              │ 實例變數               │
│ Hook       │ 在函式元件中使用狀態/副作用         │ 裝飾器 / mixin          │
│ JSX        │ JavaScript + HTML 混合語法        │ Jinja2 模板             │
│ Virtual DOM│ 記憶體中的 DOM 樹，差異更新         │ 無直接對應              │
└────────────┴──────────────────────────────────┴────────────────────────┘
```

### 10.2 完整 React Component 範例

```tsx
// ─── TodoApp.tsx：完整的待辦事項元件 ───

import React, { useState, useEffect } from "react";

// Props 介面定義
interface TodoItem {
    id: number;
    title: string;
    completed: boolean;
}

interface TodoListProps {
    initialTodos?: TodoItem[];
    apiUrl?: string;
}

// Input:  props: { initialTodos?, apiUrl? }
// Process: 管理待辦事項的 CRUD 操作
// Output:  渲染待辦事項清單 UI
function TodoApp({ initialTodos = [], apiUrl = "/api/todos" }: TodoListProps) {
    // ─── State（狀態）───
    const [todos, setTodos] = useState<TodoItem[]>(initialTodos);
    const [inputValue, setInputValue] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

    // ─── useEffect：副作用處理（類似 Python 的 __init__ 中啟動非同步任務）───
    // 元件載入時從 API 取得資料
    useEffect(() => {
        async function fetchTodos() {
            setIsLoading(true);
            setError(null);
            try {
                const response = await fetch(apiUrl);
                if (!response.ok) throw new Error("載入失敗");
                const data: TodoItem[] = await response.json();
                setTodos(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : "未知錯誤");
            } finally {
                setIsLoading(false);
            }
        }

        if (initialTodos.length === 0) {
            fetchTodos();
        }
    }, [apiUrl, initialTodos.length]);
    // ↑ 依賴陣列：只在 apiUrl 或 initialTodos.length 改變時重新執行

    // ─── 事件處理函式 ───
    // Input:  無（使用元件內的 inputValue state）
    // Process: 新增一筆待辦事項到 todos 陣列
    // Output:  更新 todos state
    function handleAddTodo(): void {
        const trimmed = inputValue.trim();
        if (trimmed === "") return;

        const newTodo: TodoItem = {
            id: Date.now(),
            title: trimmed,
            completed: false
        };
        setTodos(prev => [...prev, newTodo]);
        setInputValue("");
    }

    // Input:  id (number)
    // Process: 切換指定待辦事項的完成狀態
    // Output:  更新 todos state
    function handleToggle(id: number): void {
        setTodos(prev =>
            prev.map(todo =>
                todo.id === id ? { ...todo, completed: !todo.completed } : todo
            )
        );
    }

    // Input:  id (number)
    // Process: 從 todos 中移除指定的待辦事項
    // Output:  更新 todos state
    function handleDelete(id: number): void {
        setTodos(prev => prev.filter(todo => todo.id !== id));
    }

    // ─── 計算衍生資料 ───
    const filteredTodos = todos.filter(todo => {
        if (filter === "active") return !todo.completed;
        if (filter === "completed") return todo.completed;
        return true;
    });

    const completedCount = todos.filter(t => t.completed).length;
    const totalCount = todos.length;

    // ─── JSX 渲染 ───
    return (
        <div style={{ maxWidth: "500px", margin: "0 auto", padding: "20px" }}>
            <h1>待辦事項清單</h1>

            {error && <p style={{ color: "red" }}>錯誤: {error}</p>}

            {/* 新增區域 */}
            <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAddTodo()}
                    placeholder="新增待辦事項..."
                    style={{ flex: 1, padding: "8px" }}
                />
                <button onClick={handleAddTodo}>新增</button>
            </div>

            {/* 篩選按鈕 */}
            <div style={{ marginBottom: "16px" }}>
                {(["all", "active", "completed"] as const).map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        style={{
                            marginRight: "8px",
                            fontWeight: filter === f ? "bold" : "normal"
                        }}
                    >
                        {f === "all" ? "全部" : f === "active" ? "未完成" : "已完成"}
                    </button>
                ))}
            </div>

            {/* 待辦清單 */}
            {isLoading ? (
                <p>載入中...</p>
            ) : (
                <ul style={{ listStyle: "none", padding: 0 }}>
                    {filteredTodos.map(todo => (
                        <li
                            key={todo.id}
                            style={{
                                display: "flex",
                                alignItems: "center",
                                padding: "8px",
                                borderBottom: "1px solid #eee"
                            }}
                        >
                            <input
                                type="checkbox"
                                checked={todo.completed}
                                onChange={() => handleToggle(todo.id)}
                            />
                            <span
                                style={{
                                    flex: 1,
                                    marginLeft: "8px",
                                    textDecoration: todo.completed ? "line-through" : "none",
                                    color: todo.completed ? "#999" : "#333"
                                }}
                            >
                                {todo.title}
                            </span>
                            <button onClick={() => handleDelete(todo.id)}>刪除</button>
                        </li>
                    ))}
                </ul>
            )}

            {/* 統計 */}
            <p style={{ marginTop: "16px", color: "#666" }}>
                已完成 {completedCount} / {totalCount} 項
            </p>
        </div>
    );
}

export default TodoApp;
```

### 10.3 Next.js 概念

```
Next.js 是基於 React 的全端框架：

┌─────────────────────────┬──────────────────────────────────────┐
│ 功能                     │ 說明                                 │
├─────────────────────────┼──────────────────────────────────────┤
│ Server-Side Rendering   │ 伺服器端渲染，有利 SEO                │
│ Static Site Generation  │ 建置時預先產生靜態頁面                 │
│ App Router              │ 基於檔案系統的路由（資料夾 = 路由）     │
│ API Routes              │ 在同一專案中寫後端 API                 │
│ Server Components       │ 預設在伺服器端渲染的元件               │
│ Server Actions          │ 直接在元件中呼叫伺服器端函式           │
└─────────────────────────┴──────────────────────────────────────┘

檔案結構範例：
app/
├── layout.tsx        # 全域版面（類似 Django base.html）
├── page.tsx          # 首頁 /
├── about/
│   └── page.tsx      # /about 頁面
├── blog/
│   ├── page.tsx      # /blog 列表頁
│   └── [slug]/
│       └── page.tsx  # /blog/:slug 動態路由
└── api/
    └── users/
        └── route.ts  # API: /api/users
```

### 10.4 對比 Python Flask / Django

```
┌──────────────┬──────────────────┬──────────────────┬─────────────────┐
│ 概念          │ Express.js       │ Flask            │ Django           │
├──────────────┼──────────────────┼──────────────────┼─────────────────┤
│ 路由定義      │ app.get("/path") │ @app.route("/")  │ urlpatterns      │
│ 中介軟體      │ app.use(fn)      │ @app.before_req  │ MIDDLEWARE       │
│ 模板引擎      │ EJS / Pug        │ Jinja2           │ Django Template  │
│ ORM          │ Prisma/Sequelize │ SQLAlchemy        │ Django ORM       │
│ 套件管理      │ npm              │ pip              │ pip              │
│ 設定檔        │ package.json     │ config.py        │ settings.py      │
│ 哲學          │ 極簡（自己組裝）  │ 微框架           │ 全功能（內建齊全）│
└──────────────┴──────────────────┴──────────────────┴─────────────────┘
```

---

## 11. 實用工具鏈

### 11.1 package.json 結構詳解

```json
{
    "name": "my-fullstack-app",
    "version": "1.0.0",
    "description": "全端應用程式",
    "type": "module",
    "main": "dist/index.js",
    "types": "dist/index.d.ts",

    "scripts": {
        "dev": "vite",
        "build": "tsc && vite build",
        "preview": "vite preview",
        "lint": "eslint src/ --ext .ts,.tsx",
        "format": "prettier --write 'src/**/*.{ts,tsx,css}'",
        "test": "vitest",
        "test:coverage": "vitest --coverage",
        "typecheck": "tsc --noEmit"
    },

    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },

    "devDependencies": {
        "typescript": "^5.3.0",
        "vite": "^5.0.0",
        "@types/react": "^18.2.0",
        "eslint": "^8.56.0",
        "prettier": "^3.2.0",
        "vitest": "^1.2.0"
    },

    "engines": {
        "node": ">=18.0.0"
    }
}
```

```
版本號語意 (Semver)：
  "express": "^4.18.2"
                │ │  │
                │ │  └─ Patch（修 bug）
                │ └────  Minor（新功能，向下相容）
                └──────  Major（破壞性變更）

  ^4.18.2 → 允許 >=4.18.2 且 <5.0.0（鎖定 Major）
  ~4.18.2 → 允許 >=4.18.2 且 <4.19.0（鎖定 Minor）
   4.18.2 → 精確鎖定版本
```

### 11.2 tsconfig.json 設定

```json
{
    "compilerOptions": {
        // ─── 基本設定 ───
        "target": "ES2022",
        "module": "ESNext",
        "lib": ["ES2022", "DOM", "DOM.Iterable"],
        "moduleResolution": "bundler",

        // ─── 輸出設定 ───
        "outDir": "./dist",
        "rootDir": "./src",
        "declaration": true,
        "declarationMap": true,
        "sourceMap": true,

        // ─── 嚴格模式（全部建議開啟）───
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,

        // ─── 模組互通 ───
        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "isolatedModules": true,

        // ─── JSX（React 專案）───
        "jsx": "react-jsx",

        // ─── 路徑別名 ───
        "baseUrl": ".",
        "paths": {
            "@/*": ["./src/*"],
            "@components/*": ["./src/components/*"],
            "@utils/*": ["./src/utils/*"]
        },

        // ─── 裝飾器 ───
        "experimentalDecorators": true,
        "emitDecoratorMetadata": true,

        // ─── 跳過型別檢查（加速建置）───
        "skipLibCheck": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

```
重要選項對照（Python 開發者快速理解）：

  target        → 編譯成哪個版本的 JS（類似 Python 指定 3.8+ 語法）
  strict        → 開啟所有嚴格檢查（類似 mypy --strict）
  outDir        → 編譯輸出目錄（類似 Python 的 build/）
  paths         → 路徑別名（類似 Python 的 sys.path 或 pyproject.toml 的 packages）
  declaration   → 產生 .d.ts 型別定義檔（類似 Python 的 .pyi stub 檔案）
```

### 11.3 ESLint 與 Prettier

```javascript
// ─── .eslintrc.cjs（程式碼品質檢查）───
module.exports = {
    root: true,
    env: {
        browser: true,
        es2022: true,
        node: true
    },
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:react/recommended",
        "plugin:react-hooks/recommended",
        "prettier"  // 放最後，關閉與 Prettier 衝突的規則
    ],
    parser: "@typescript-eslint/parser",
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: {
            jsx: true
        }
    },
    plugins: ["@typescript-eslint", "react"],
    rules: {
        "no-console": "warn",
        "no-unused-vars": "off",
        "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
        "@typescript-eslint/explicit-function-return-type": "warn",
        "react/react-in-jsx-scope": "off"
    },
    settings: {
        react: {
            version: "detect"
        }
    }
};
```

```json
// ─── .prettierrc（程式碼格式化）───
{
    "semi": true,
    "trailingComma": "none",
    "singleQuote": false,
    "printWidth": 100,
    "tabWidth": 4,
    "useTabs": false,
    "bracketSpacing": true,
    "arrowParens": "avoid",
    "endOfLine": "lf"
}
```

```
ESLint vs Prettier 分工：

  ESLint   → 程式碼品質（找 bug、強制風格）  → 類似 Python 的 pylint / flake8
  Prettier → 程式碼格式（排版美化）          → 類似 Python 的 black / autopep8

  兩者搭配使用：ESLint 負責邏輯，Prettier 負責美觀，互不衝突。
```

### 11.4 Webpack vs Vite

```
┌────────────┬────────────────────────────┬────────────────────────────┐
│            │ Webpack                    │ Vite                       │
├────────────┼────────────────────────────┼────────────────────────────┤
│ 開發模式    │ 打包後啟動（慢）            │ 原生 ESM（極快）            │
│ 熱更新      │ 整個模組重新打包            │ 只更新修改的模組            │
│ 設定複雜度  │ 高（webpack.config.js）     │ 低（vite.config.ts）       │
│ 生態系      │ 成熟龐大                   │ 快速成長                   │
│ 建置工具    │ 自身                       │ 底層用 Rollup / esbuild    │
│ 適用場景    │ 大型舊專案                  │ 新專案首選                 │
│ 類比 Python │ 類似手動配置 setuptools     │ 類似 Poetry 一鍵設定       │
└────────────┴────────────────────────────┴────────────────────────────┘
```

```typescript
// ─── vite.config.ts（Vite 設定範例）───
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
            "@components": path.resolve(__dirname, "./src/components"),
            "@utils": path.resolve(__dirname, "./src/utils")
        }
    },
    server: {
        port: 5173,
        proxy: {
            "/api": {
                target: "http://localhost:3000",
                changeOrigin: true
            }
        }
    },
    build: {
        outDir: "dist",
        sourcemap: true,
        minify: "esbuild"
    }
});
```

---

## 總結速查表

```
Python 開發者轉 JS/TS 的五個關鍵心態轉換：

1. 非同步是預設 ─── Python 用 asyncio 是「引入」，JS 的 async 是「天性」
2. 型別是可選的 ─── Python type hints 是註解，TS 型別是編譯時強制
3. 函式是一等公民 ── Python 也是，但 JS 更激進（callback 無所不在）
4. 原型 vs 類別 ─── JS 的 class 是語法糖，底層是原型鏈（prototype chain）
5. 生態系碎片化 ── Python 有 Django「全家桶」，JS 要自己組裝工具鏈

常用命令速查：
  npm init -y              # 初始化專案（類似 poetry init）
  npm install <pkg>        # 安裝套件（類似 pip install）
  npm install -D <pkg>     # 安裝開發依賴（類似 pip install 到 dev group）
  npx tsc --init           # 初始化 TypeScript
  npx tsc                  # 編譯 TypeScript
  npm run dev              # 啟動開發伺服器
  npm run build            # 建置生產版本
  npm test                 # 執行測試
```

---

> **下一步學習建議**：
> - 完成本篇後，建議動手用 Express + TypeScript 寫一個完整的 REST API
> - 接著用 React + TypeScript 做一個前端介面串接該 API
> - 最後嘗試 Next.js 整合前後端，體驗真正的全端開發流程
