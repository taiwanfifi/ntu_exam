# 演算法教學 09：NP 完全性（NP-Completeness）

> 這是整門演算法課中最「哲學」也最容易混淆的章節。我們不再問「怎麼解這個問題」，
> 而是問「這個問題到底能不能被有效率地解？」。如果你覺得這章很抽象，這是正常的——
> 但只要把定義搞清楚、把歸約的方向記對，考試其實就是那幾個固定套路。

---

## 🔰 本章基礎觀念（零基礎必讀）

### 為什麼需要學 NP 完全性？

**場景：** 你是一個程式設計師，老闆要你寫一個程式解決以下問題：「給定 50 個城市和它們之間的距離，找出一條經過每個城市恰好一次、總距離最短的旅行路線。」你試了各種演算法，都跑了好幾個小時甚至好幾天。你開始懷疑：是不是自己太笨了？是不是有什麼更聰明的方法？

**答案：不是你笨。** 這個問題（旅行推銷員問題 TSP）是 **NP-Complete** 的，意思是——在目前人類所知的範圍內，**沒有人找到快速解法**，而且幾十年來全世界最聰明的人都沒找到。如果你找到了，你就解決了價值 100 萬美元的千禧年大獎問題！

**學 NP 完全性的實用意義：**
1. **知道何時放棄找精確解。** 如果你的問題是 NPC，別再浪費時間找多項式演算法了。
2. **知道該怎麼辦。** 改用近似演算法、啟發式演算法、或限制輸入規模。
3. **考試必考。** NPC 的定義、歸約方向、True/False 判斷是經典考點。

### 本章關鍵術語表

| 術語 | 英文 | 白話解釋 | 例子 |
|------|------|----------|------|
| P 類 | P (Polynomial time) | 能在多項式時間內「解決」的問題 | 排序 $O(n \log n)$、最短路 $O(V^2)$ |
| NP 類 | NP (Nondeterministic Polynomial time) | 如果有人給你一個答案，你能在多項式時間內「驗證」它是否正確 | 數獨：填完的答案很容易驗證對不對 |
| NP-Complete | NPC | NP 中「最難的」那批問題，而且它們之間可以互相轉換 | SAT、TSP、背包問題 |
| NP-hard | NP-hard | 至少跟 NP 中最難的問題一樣難（但不一定在 NP 中） | 停機問題（不可判定，比 NPC 更難） |
| 歸約 | Reduction ($\leq_p$) | 把問題 A 轉換成問題 B——如果 B 能解，A 就能解 | 把「找最大團」轉成「找 SAT 的解」 |
| 判定問題 | Decision Problem | 答案只有 Yes/No 的問題 | 「是否存在長度 $\leq$ k 的路徑？」 |
| Certificate | Certificate（證書/憑證） | 用來「證明答案是 Yes」的簡短證據 | 數獨的一個完整填法就是 certificate |
| Verifier | Verifier（驗證器） | 檢查 certificate 是否正確的快速程式 | 檢查數獨填法是否合法的程式 |

### 前置知識

- **基本複雜度概念**（algo_01）：$O, \Theta, \Omega$ 符號，多項式時間
- **圖論基礎**（algo_01~02）：了解 Clique、Independent Set 等圖問題
- **SAT / 布林邏輯**：知道 AND ($\wedge$)、OR ($\vee$)、NOT ($\neg$) 和 CNF 公式
- **SCC（強連通分量）**（algo_02）：2-SAT 的解法需要用到

### P vs NP 的直覺解釋

> **🔰 用「數獨」來理解 P 和 NP：**
>
> 想像一個超大的數獨（$n \times n$），有百萬格：
>
> - **解數獨（找答案）：** 非常難！你可能需要嘗試指數多種填法。目前沒有已知的快速方法。
> - **驗證數獨（檢查別人給你的答案）：** 非常簡單！只要逐行、逐列、逐區塊檢查有沒有重複數字。
>
> **NP 就是這類問題：** 解起來可能很慢，但驗證答案很快。
> **P 就是這類問題：** 不只驗證快，連解都很快。
>
> **P vs NP 問題問的是：** 「所有容易驗證的問題，是不是也都容易解？」如果 P = NP，那每個容易驗證的問題都有快速解法——但大多數人相信 P ≠ NP。
>
> **為什麼這是最重要的未解問題？** 因為如果 P = NP：
> - 所有加密系統都會崩潰（破解密碼和驗證密碼一樣快）
> - 很多被認為「不可能快速解決」的問題瞬間都有解了
> - 整個計算機科學的基礎假設都要改寫

### Reduction（歸約）的直覺

> **白話版：** 假設你不會做微積分（問題 A），但你很會做代數（問題 B）。如果有一個公式能把任何微積分問題**自動轉換**成代數問題，那你就能間接解微積分了——先轉成代數，再用代數的方法解。
>
> 這就是歸約 A $\leq_p$ B 的意思：「A 可以被轉成 B 來解。」
>
> **⚠️ 關鍵方向：** A $\leq_p$ B 意思是「**B 至少和 A 一樣難**」（不是 A 比 B 難！）。因為你需要 B 的解法才能間接解 A。如果 A 已知很難，那 B 只會更難。
>
> **記憶口訣：** 「箭頭指向的那個問題更難」。$A \leq_p B$ 裡箭頭指向 $B$，所以 $B$ 更難（至少一樣難）。

### 如何證明一個問題是 NP-Complete？（模板化步驟）

```
【NPC 證明模板】

目標：證明問題 L 是 NP-Complete

Step 1：證明 L ∈ NP
  (a) 描述 certificate（一個多項式長度的「答案證據」）
  (b) 描述 verifier（一個多項式時間的「驗證程式」）
  (c) 論證：x ∈ L ⟺ 存在合法 certificate 使 verifier accept

Step 2：證明 L 是 NP-hard（用歸約）
  (a) 選一個「已知是 NPC」的問題 L'（通常選 3-SAT）
  (b) 構造歸約函數 f：把 L' 的任意 instance 轉成 L 的 instance
  (c) 證明正確性（雙向！）：
      • x ∈ L' ⟹ f(x) ∈ L
      • f(x) ∈ L ⟹ x ∈ L'  （兩個方向都要證！）
  (d) 證明 f 是多項式時間

結論：L ∈ NP 且 L 是 NP-hard，所以 L 是 NP-Complete。 ∎
```

---

## 一、計算複雜度基礎

### 1.1 Decision Problem vs Optimization Problem

在複雜度理論中，我們統一把問題轉成 **判定問題（Decision Problem）**，也就是答案只有 Yes/No 的問題。

| 問題類型 | 最短路徑（Optimization）| 最短路徑（Decision）|
|---------|----------------------|-------------------|
| 問法 | 從 s 到 t 的最短距離是多少？ | 從 s 到 t 是否存在長度 ≤ k 的路徑？ |
| 答案 | 一個數字（如 42） | Yes 或 No |

**為什麼要這樣做？** 因為判定問題更容易形式化，而且：
- 如果判定版本就已經很難了，最佳化版本只會更難（或一樣難）。
- 透過二分搜尋，通常可以用判定版本的 oracle 來解最佳化版本。

**例子：**
- CLIQUE（Optimization）：圖 G 中最大完全子圖的大小是多少？
- CLIQUE（Decision）：圖 G 中是否存在大小 ≥ k 的完全子圖？
- TSP（Optimization）：訪問所有城市的最短迴路長度？
- TSP（Decision）：是否存在訪問所有城市且總長度 ≤ k 的迴路？

### 1.2 Language 和 Encoding

在複雜度理論中，一個判定問題等價於一個 **語言（Language）**：

```
L = { x ∈ {0,1}* : x 是一個 Yes-instance 的編碼 }
```

所謂「解決」一個語言 L，就是：給定輸入 x，判斷 x ∈ L 還是 x ∉ L。

**Encoding（編碼）很重要！** 同一個問題，用不同編碼，複雜度可能不同：
- 整數 n 用二進位編碼：長度 = O(log n)
- 整數 n 用一進位（unary）編碼：長度 = O(n)

這就是為什麼 Subset Sum 用一般編碼是 NP-complete，但用 unary 編碼就變成 P（因為 DP 的 O(nW) 在 unary 下變成多項式）。這種問題叫 **weakly NP-complete**。

---

## 二、P, NP, co-NP, NP-hard, NP-complete 的精確定義

### 2.1 P 類

**定義：** P 是所有可以在 **多項式時間內「解決」** 的判定問題的集合。

更精確地說：
```
L ∈ P  ⟺  存在一個確定性圖靈機 M 和多項式 p(n)，使得：
           對所有輸入 x（|x| = n），M 在 p(n) 步內停機，
           且 M(x) = 1 ⟺ x ∈ L
```

白話說：**有一個「快速」（polynomial time）演算法可以正確判斷 Yes/No。**

**例子：** 排序、最短路徑、最大流、2-SAT、匹配。

### 2.2 NP 類

> **超級重要：NP 不是 "Non-Polynomial" 的縮寫！**
> NP = **Nondeterministic Polynomial time**

**定義（驗證版，最好理解）：**
```
L ∈ NP  ⟺  存在一個多項式時間的驗證器 V 和多項式 p(n)，使得：
           x ∈ L  ⟺  存在一個 certificate c（|c| ≤ p(|x|)），使 V(x, c) = 1
```

白話說：**如果答案是 Yes，那麼存在一個「簡短的證據」（certificate），讓我可以「快速驗證」。**

**拆解：**
- **Certificate（證書/憑證）：** 一個多項式長度的字串，代表「證據」
- **Verifier（驗證器）：** 一個多項式時間的演算法，檢查證據是否有效

**例子：**
| 問題 | Certificate | 驗證方式 |
|------|------------|---------|
| CLIQUE(G, k) | k 個頂點的集合 S | 檢查 S 中每對頂點都有邊，且 \|S\| ≥ k |
| HAM-CYCLE(G) | 一個頂點排列 | 檢查是否形成合法的 Hamiltonian Cycle |
| SAT(φ) | 一組 truth assignment | 代入檢查 φ 是否為 True |
| COMPOSITE(n) | 一個因數 d | 檢查 1 < d < n 且 d \| n |

**關鍵觀念：**
- NP 的「N」是 Nondeterministic，不是 Non-！
- P ⊆ NP（如果你能快速「解決」，當然也能快速「驗證」——直接忽略 certificate，自己算就好）
- NP 問題不一定很難！它只是說「Yes 答案可以快速驗證」

### 2.3 co-NP 類

**定義：**
```
L ∈ co-NP  ⟺  L̄ ∈ NP
             （L 的補語言在 NP 中）
```

也就是說：**如果答案是 No，那麼存在一個簡短的證據可以快速驗證「不是」。**

**例子：**
- TAUTOLOGY（重言式）：給定布林公式 φ，是否所有 assignment 都讓 φ = True？
  - 這在 co-NP 中：如果 φ 不是 tautology，certificate 就是一組讓 φ = False 的 assignment
  - 但我們不知道 TAUTOLOGY 是否在 NP 中（如果 φ 是 tautology，有什麼簡短證據？）
- PRIMES（判斷是否為質數）：已知 P 中（AKS 2002），所以同時在 NP 和 co-NP 中

**P 和 co-NP 的關係：** P ⊆ co-NP（因為 P 對補封閉）

### 2.4 NP-hard

**定義：**
```
L 是 NP-hard  ⟺  對所有 L' ∈ NP，都有 L' ≤_p L
```

白話說：**NP 中的每一個問題都可以多項式歸約到 L，所以 L 至少和 NP 中最難的問題一樣難。**

注意：NP-hard 的問題 **不一定在 NP 中**！
- 停機問題（Halting Problem）是 NP-hard，但不在 NP 中（甚至不可判定）
- 某些最佳化問題是 NP-hard，但不是判定問題，所以不在 NP 中

### 2.5 NP-complete（NPC）

**定義：**
```
L ∈ NPC  ⟺  (1) L ∈ NP，且
              (2) L 是 NP-hard
即 NPC = NP ∩ NP-hard
```

白話說：**NPC 問題是 NP 中「最難的」那批問題。**

**例子：** SAT, 3-SAT, CLIQUE, VERTEX-COVER, INDEPENDENT-SET, HAMILTONIAN-CYCLE, SUBSET-SUM, 3-COLORING, TSP（判定版）

---

## 三、關係圖

```
┌─────────────────────────────────────────────┐
│                  NP-hard                     │
│                                              │
│    ┌────────────────────┐                    │
│    │        NP          │                    │
│    │                    │                    │
│    │    ┌──────────┐    │                    │
│    │    │   NPC    │    │  ← NPC = NP ∩ NP-hard
│    │    │          │    │                    │
│    │    └──────────┘    │                    │
│    │                    │                    │
│    │   ┌──────┐         │                    │
│    │   │  P   │         │                    │
│    │   └──────┘         │                    │
│    └────────────────────┘                    │
│                                              │
│   停機問題等（NP-hard 但不在 NP 中）           │
└─────────────────────────────────────────────┘

同時：
         ┌──────┐
         │  P   │
         └──┬───┘
            │
     ┌──────┴──────┐
     ▼              ▼
  ┌──────┐     ┌────────┐
  │  NP  │     │ co-NP  │
  └──────┘     └────────┘
```

**已知的包含關係：**
- P ⊆ NP
- P ⊆ co-NP
- NPC ⊆ NP
- 如果 P = NP，則 NP = co-NP（後面會證）

**未解問題（千禧年大問題！）：**
- P =? NP
- NP =? co-NP

---

## 四、Polynomial-time Reduction (≤_p)

### 4.1 定義

**定義：** A ≤_p B（「A 多項式歸約到 B」）表示：
```
存在一個多項式時間可計算的函數 f: {0,1}* → {0,1}*，使得
對所有 x：x ∈ A ⟺ f(x) ∈ B
```

圖示：
```
問題 A 的 instance x  ──f（多項式時間）──→  問題 B 的 instance f(x)
     x ∈ A            ⟺                    f(x) ∈ B
```

### 4.2 直覺理解

**A ≤_p B 的意思是：「B 至少和 A 一樣難」**

> 注意方向！這是最容易記反的地方！

邏輯是這樣的：
- 如果我有一個解決 B 的快速演算法，那我就可以解決 A（先把 A 的 instance 轉成 B 的 instance，再用 B 的演算法解）
- 所以 B 的能力 ≥ A 的能力，即 B 至少和 A 一樣難

**反過來想也可以：**
- 如果 A 很難（比如 NPC），而 A ≤_p B，那 B 也至少一樣難

### 4.3 歸約的方向（超級重要！考試最常錯的地方！）

**要證明問題 L 是 NP-complete，歸約的方向是：**
```
已知 NPC 問題 L' ≤_p 要證的問題 L
```

也就是：**從已知的 hard 問題歸約「到」你要證的問題！**

> **記法：** 箭頭指向「要證的那個」。
> 把已知困難的問題「塞進」要證的問題裡，說明要證的問題至少一樣難。

**千萬不要記反了：**
- 正確：3-SAT ≤_p CLIQUE（要證 CLIQUE 是 NPC，從 3-SAT 歸約到 CLIQUE）
- 錯誤方向：CLIQUE ≤_p 3-SAT（這只能說明 3-SAT 至少和 CLIQUE 一樣難，但你本來就知道 3-SAT 是 NPC 了）

### 4.4 歸約的傳遞性

如果 A ≤_p B 且 B ≤_p C，則 A ≤_p C。

這很重要！因為我們可以建立「歸約鏈」：
```
SAT ≤_p 3-SAT ≤_p CLIQUE ≤_p ...
```
只要鏈的起點是 NPC，終點也是 NP-hard。

---

## 五、證明 NP-complete 的標準流程

要證明問題 L 是 NP-complete，需要兩步：

### Step 1：證明 L ∈ NP

**怎麼做：** 給出 certificate 和 verifier。

模板：
```
Certificate: [描述一個多項式長度的證據]
Verifier:    [描述一個多項式時間的驗證演算法]
正確性:      x ∈ L ⟺ 存在合法的 certificate 使 verifier accept
```

**例子（CLIQUE）：**
- Certificate：一個頂點子集 S ⊆ V，|S| = k
- Verifier：
  1. 檢查 |S| ≥ k → O(1)
  2. 對 S 中每對頂點 (u,v)，檢查 (u,v) ∈ E → O(k²) ⊆ O(n²)
- Certificate 長度 O(n)，驗證時間 O(n²)，都是多項式。所以 CLIQUE ∈ NP。

### Step 2：證明 L 是 NP-hard

**怎麼做：** 從一個已知的 NPC 問題 L' 歸約到 L。

具體步驟：

**(2a) 選擇已知 NPC 問題 L'**

通常選擇和 L 結構最相似的 NPC 問題。常見的起點：
- 圖問題 → 從 3-SAT、CLIQUE、Independent Set、Vertex Cover 出發
- 數值問題 → 從 Subset Sum 出發
- 路徑問題 → 從 Hamiltonian Cycle 出發

**(2b) 構造多項式時間的歸約函數 f**

給定 L' 的任意 instance x，構造 L 的 instance f(x)。

**(2c) 證明正確性（雙向！）**

必須證明 **雙向**：
```
(⟹) 如果 x ∈ L'，則 f(x) ∈ L
(⟸) 如果 f(x) ∈ L，則 x ∈ L'  （等價地：若 x ∉ L' 則 f(x) ∉ L）
```

> **常見陷阱：只證了一個方向！** 兩個方向都要證，缺一不可。

**(2d) 證明 f 是多項式時間**

說明 f 的構造時間是 input size 的多項式。

---

## 六、常用歸約鏈

以下是 NP-complete 證明的「族譜」。Cook-Levin 定理是一切的起點。

### 6.1 Cook-Levin 定理：Circuit-SAT 是 NP-complete

**定理（Cook-Levin, 1971）：** SAT 是 NP-complete。

**核心思想：** 任何 NP 問題 L 都有一個多項式時間的 verifier V。把 V 的計算過程「攤開」成一個布林電路（或 CNF 公式），使得公式可滿足 ⟺ 存在讓 V accept 的 certificate。

這個定理的證明非常技術性（要模擬圖靈機的 tableau），考試通常不考完整證明，但要知道：
- 這是 **唯一一個**「從頭證 NP-hard」的定理
- 之後所有 NPC 證明都是通過歸約鏈

### 6.2 Circuit-SAT → SAT → 3-SAT

**SAT（Satisfiability）：** 給定 CNF 公式 φ，是否存在 satisfying assignment？

**Circuit-SAT → SAT：** 把電路中每個 gate 的輸出用一個新變數表示，然後把每個 gate 的功能寫成 CNF 子句。

**SAT → 3-SAT：**

把每個子句拆成多個 3-literal 的子句：
- 如果子句有 1 個 literal (ℓ₁)：引入 2 個新變數 y₁, y₂，替換為
  (ℓ₁ ∨ y₁ ∨ y₂)(ℓ₁ ∨ y₁ ∨ ȳ₂)(ℓ₁ ∨ ȳ₁ ∨ y₂)(ℓ₁ ∨ ȳ₁ ∨ ȳ₂)
- 如果子句有 2 個 literals (ℓ₁ ∨ ℓ₂)：引入 1 個新變數 y，替換為
  (ℓ₁ ∨ ℓ₂ ∨ y)(ℓ₁ ∨ ℓ₂ ∨ ȳ)
- 如果子句有 3 個 literals：不動
- 如果子句有 k > 3 個 literals (ℓ₁ ∨ ℓ₂ ∨ ... ∨ ℓ_k)：引入 k-3 個新變數 y₁,...,y_{k-3}，替換為
  (ℓ₁ ∨ ℓ₂ ∨ y₁)(ȳ₁ ∨ ℓ₃ ∨ y₂)(ȳ₂ ∨ ℓ₄ ∨ y₃)...(ȳ_{k-3} ∨ ℓ_{k-1} ∨ ℓ_k)

### 6.3 3-SAT → CLIQUE

**CLIQUE：** 圖 G 中是否存在大小 ≥ k 的完全子圖？

**歸約構造：**
給定 3-SAT instance φ = C₁ ∧ C₂ ∧ ... ∧ C_m（每個 C_i 有 3 個 literals）：
1. 對每個子句 C_i 的每個 literal，建一個頂點 → 共 3m 個頂點
2. 兩個頂點 (ℓ_i, C_i) 和 (ℓ_j, C_j) 之間加邊，當且僅當：
   - i ≠ j（來自不同子句），且
   - ℓ_i ≠ ¬ℓ_j（不互相矛盾）
3. 設 k = m

直覺：CLIQUE 中選 k 個互不矛盾的 literals（每個子句選一個），就對應一個 satisfying assignment。

### 6.4 3-SAT → Independent Set

**Independent Set：** 圖 G 中是否存在大小 ≥ k 的獨立集（沒有邊相連的頂點集合）？

（下面第七節有完整的 step-by-step 範例。）

### 6.5 Independent Set ↔ Vertex Cover ↔ Clique

這三個問題可以非常簡單地互相歸約：

**Independent Set ↔ Vertex Cover：**
- S 是 G 的 independent set ⟺ V \ S 是 G 的 vertex cover
- 所以：G 有大小 ≥ k 的 IS ⟺ G 有大小 ≤ n-k 的 VC
- 歸約：(G, k) ↦ (G, n-k)，同一張圖！

**Independent Set ↔ Clique：**
- S 是 G 的 independent set ⟺ S 是 Ḡ（補圖）的 clique
- 歸約：(G, k) ↦ (Ḡ, k)

### 6.6 3-SAT → Subset Sum

**Subset Sum：** 給定一組正整數 S = {s₁,...,sₙ} 和目標值 t，是否存在子集和恰好等於 t？

**歸約思路：** 用一個精巧的十進位數字編碼。對每個變數 xᵢ 造兩個數（對應 xᵢ = True 和 xᵢ = False），對每個子句 Cⱼ 造兩個 slack 數。每個數的十進位表示中，某些位數對應變數、某些位數對應子句。選擇 assignment 對應選擇數字子集，子句被滿足對應位數加起來等於目標值。

### 6.7 3-SAT → Hamiltonian Cycle

**Hamiltonian Cycle：** 圖 G 中是否存在經過每個頂點恰好一次的環？

**歸約思路：** 對每個變數建一條「蛇形路徑」（由許多節點組成），對每個子句建一個特殊節點。蛇形路徑的走法（左到右或右到左）代表變數的 True/False。子句節點透過「旁路」連接到對應的蛇形路徑。

### 6.8 Hamiltonian Cycle → Hamiltonian Path → TSP

**Ham Cycle → Ham Path：**
- 給定 Ham Cycle instance G，選一個頂點 v，把 v 拆成兩個 v_in, v_out，加一個新頂點 s 只連 v_in，一個新頂點 t 只連 v_out。G 有 Ham Cycle ⟺ 新圖有從 s 到 t 的 Ham Path。

**Ham Cycle → TSP（Decision）：**
- 給定圖 G = (V, E)，構造完全圖 K_n，邊權為：
  - w(u,v) = 1 如果 (u,v) ∈ E
  - w(u,v) = 2 如果 (u,v) ∉ E
- 設 k = n（頂點數）
- G 有 Ham Cycle ⟺ K_n 有總權重 ≤ n 的 TSP tour

### 6.9 Hamiltonian Path → Degree-Constrained Spanning Tree (K=2)

**Degree-Constrained Spanning Tree (DCST)：** 圖 G 是否存在一棵生成樹，使得每個頂點的 degree ≤ K？

**歸約（K=2）：**
- 注意：degree ≤ 2 的生成樹就是 Hamiltonian Path！
- 因為生成樹有 n-1 條邊、連通、無環，且每個頂點 degree ≤ 2 → 只能是一條路徑
- 所以 Ham Path ≤_p DCST(K=2) 是 trivial reduction：直接 (G) ↦ (G, K=2)

### 6.10 Hamiltonian Cycle → Subgraph Isomorphism

**Subgraph Isomorphism：** 給定圖 G 和 H，H 是否是 G 的子圖（同構意義下）？

**歸約：**
- 給定 Ham Cycle instance G（n 個頂點），令 H = Cₙ（n 個頂點的環）
- G 有 Hamiltonian Cycle ⟺ Cₙ 是 G 的子圖
- 歸約：G ↦ (G, Cₙ)

---

## 七、完整歸約範例

### 7.1 完整範例：3-SAT ≤_p Independent Set

**目標：** 證明 Independent Set 是 NP-complete。

#### Step 1：Independent Set ∈ NP

- **Certificate：** 一個頂點子集 S ⊆ V
- **Verifier：**
  1. 檢查 |S| ≥ k → O(1)
  2. 對 S 中每對頂點 (u,v)，檢查 (u,v) ∉ E → O(k²) ⊆ O(n²)
- 時間 O(n²)，certificate 長度 O(n)，都是多項式。

**結論：Independent Set ∈ NP。** ✓

#### Step 2：3-SAT ≤_p Independent Set

**(2a) 選擇已知 NPC 問題：** 3-SAT

**(2b) 構造歸約函數 f：**

給定 3-SAT instance：
```
φ = C₁ ∧ C₂ ∧ ... ∧ C_m
其中每個 Cⱼ = (ℓⱼ₁ ∨ ℓⱼ₂ ∨ ℓⱼ₃)
```

構造圖 G = (V, E) 和整數 k 如下：

**頂點：** 對每個子句 Cⱼ 的每個 literal，建一個頂點。
```
V = { vⱼᵢ : j = 1,...,m 且 i = 1,2,3 }
|V| = 3m
```

**邊：** 兩種情況加邊：
1. **同一子句內的 literals 互連（Clause edges）：** 對每個 j，vⱼ₁, vⱼ₂, vⱼ₃ 兩兩連邊（形成三角形）
2. **矛盾的 literals 互連（Contradiction edges）：** 如果 ℓⱼᵢ = ¬ℓⱼ'ᵢ'（一個是 x，另一個是 ¬x），則 vⱼᵢ 和 vⱼ'ᵢ' 連邊

**設 k = m（子句數）。**

**(2c) 正確性證明——完整的雙向證明：**

**（⟹ 方向）φ 可滿足 ⟹ G 有大小 ≥ m 的 independent set**

假設 τ 是 φ 的一個 satisfying assignment。
- 對每個子句 Cⱼ，至少有一個 literal 為 True。從中選一個，設為 ℓⱼᵢⱼ。
- 令 S = { vⱼ,ᵢⱼ : j = 1,...,m }。|S| = m = k。
- S 是 independent set 嗎？
  - Clause edges：每個子句只選了一個頂點，所以同子句的頂點不會同時在 S 中。✓
  - Contradiction edges：S 中的 literals 都是 True，不可能有 x 和 ¬x 同時為 True，所以不會有矛盾邊。✓
- 所以 S 是大小 m 的 independent set。

**（⟸ 方向）G 有大小 ≥ m 的 independent set ⟹ φ 可滿足**

假設 S 是 G 的大小 ≥ m 的 independent set。
- 因為每個子句內三個頂點兩兩相連（三角形），S 最多從每個子句選 1 個頂點。
- 共 m 個子句，|S| ≥ m，所以 S 恰好從每個子句選 1 個。
- 因為沒有 contradiction edges 在 S 中，S 中的 literals 不互相矛盾。
- 構造 assignment τ：
  - 對 S 中的 literal ℓ，如果 ℓ = xᵢ，設 τ(xᵢ) = True
  - 如果 ℓ = ¬xᵢ，設 τ(xᵢ) = False
  - 其餘變數任意設定
- 因為每個子句都有一個被選中的 True literal，φ 被滿足。

**(2d) f 是多項式時間：**
- 建 3m 個頂點 → O(m)
- 建 clause edges：每個子句 3 條 → O(m)
- 建 contradiction edges：對每對頂點檢查是否矛盾 → O(m²)
- 總共 O(m²) = poly(input size)。✓

**結論：Independent Set 是 NP-complete。** ∎

#### 具體範例

考慮 3-SAT instance：
```
φ = (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ ¬x₃)
```

m = 3 個子句，所以 k = 3。

**頂點（9 個）：**
```
C₁: v₁₁(x₁),  v₁₂(¬x₂), v₁₃(x₃)
C₂: v₂₁(¬x₁), v₂₂(x₂),  v₂₃(x₃)
C₃: v₃₁(x₁),  v₃₂(x₂),  v₃₃(¬x₃)
```

**Clause edges（同子句三角形，9 條）：**
```
{v₁₁,v₁₂}, {v₁₁,v₁₃}, {v₁₂,v₁₃}
{v₂₁,v₂₂}, {v₂₁,v₂₃}, {v₂₂,v₂₃}
{v₃₁,v₃₂}, {v₃₁,v₃₃}, {v₃₂,v₃₃}
```

**Contradiction edges：**
```
v₁₁(x₁) — v₂₁(¬x₁)    （x₁ 和 ¬x₁ 矛盾）
v₁₂(¬x₂) — v₂₂(x₂)    （¬x₂ 和 x₂ 矛盾）
v₁₂(¬x₂) — v₃₂(x₂)    （¬x₂ 和 x₂ 矛盾）
v₁₃(x₃) — v₃₃(¬x₃)    （x₃ 和 ¬x₃ 矛盾）
v₂₃(x₃) — v₃₃(¬x₃)    （x₃ 和 ¬x₃ 矛盾）
```

**驗證一個解：** 設 x₁ = T, x₂ = T, x₃ = T。
- C₁ 中 x₁ = T → 選 v₁₁
- C₂ 中 x₂ = T → 選 v₂₂
- C₃ 中 x₁ = T → 選 v₃₁
- S = {v₁₁, v₂₂, v₃₁}，|S| = 3 = k
- 檢查：v₁₁ 和 v₂₂ 之間？不同子句，x₁ ≠ ¬x₂，無邊。✓
- v₁₁ 和 v₃₁ 之間？不同子句，x₁ = x₁ 但不互矛盾，但它們是相同 literal 所以也沒有 contradiction edge。✓
- v₂₂ 和 v₃₁ 之間？不同子句，x₂ ≠ ¬x₁，無邊。✓
- S 是 independent set！✓

### 7.2 完整構造：3-SAT ≤_p Vertex Cover

**Vertex Cover：** 圖 G 中是否存在大小 ≤ k 的頂點集 S，使得每條邊至少有一個端點在 S 中？

#### 方法一：透過 Independent Set 間接歸約

因為我們已經證明了 3-SAT ≤_p Independent Set，且 Independent Set 和 Vertex Cover 有簡單的互補關係：

```
S 是大小 ≥ k 的 independent set of G
⟺ V \ S 是大小 ≤ n-k 的 vertex cover of G
```

所以：
- 先把 3-SAT instance 轉成 Independent Set instance (G, k = m)
- 再轉成 Vertex Cover instance (G, k' = 3m - m = 2m)

#### 方法二：直接歸約（更清楚地展現 Vertex Cover 的構造）

給定 3-SAT instance φ = C₁ ∧ ... ∧ C_m，變數 x₁,...,xₙ。

**構造圖 G：**

**Variable gadgets：** 對每個變數 xᵢ，建一條邊 (aᵢ, bᵢ)，其中 aᵢ 代表 xᵢ，bᵢ 代表 ¬xᵢ。

**Clause gadgets：** 對每個子句 Cⱼ = (ℓⱼ₁ ∨ ℓⱼ₂ ∨ ℓⱼ₃)，建一個三角形 (dⱼ₁, dⱼ₂, dⱼ₃)。

**連接：** 對每個子句 Cⱼ 的第 i 個 literal ℓⱼᵢ：
- 如果 ℓⱼᵢ = xₜ，加邊 (dⱼᵢ, aₜ)
- 如果 ℓⱼᵢ = ¬xₜ，加邊 (dⱼᵢ, bₜ)

**設 k = n + 2m。**

**正確性：**
- variable gadget 的邊 (aᵢ, bᵢ) 至少要選一個端點 → 對應選 xᵢ = T 或 F
- clause gadget 的三角形至少要選 2 個頂點
- 如果子句被滿足，至少一個連接邊已被 variable gadget 覆蓋，三角形選 2 個就夠
- 如果子句不被滿足，三個連接邊都沒被覆蓋，三角形要選 3 個（超出預算）
- 所以：φ 可滿足 ⟺ G 有大小 ≤ n + 2m 的 vertex cover

---

## 八、特殊情況下的多項式解

> 雖然 SAT、Hamiltonian Path 等都是 NPC，但某些特殊版本卻有多項式演算法。
> 這告訴我們：NPC 是針對「最一般的情形」，限制條件可能讓問題變簡單。

### 8.1 2-SAT ∈ P

**2-SAT：** 每個子句恰好有 2 個 literals 的 SAT 問題。

**核心觀察：** 子句 (a ∨ b) 等價於兩個蘊含（implication）：
```
(a ∨ b) ⟺ (¬a → b) ∧ (¬b → a)
```

**Implication Graph 構造：**
1. 對每個變數 xᵢ，建兩個節點：xᵢ 和 ¬xᵢ
2. 對每個子句 (a ∨ b)，加兩條有向邊：¬a → b 和 ¬b → a

**演算法：**
1. 建 Implication Graph
2. 找 SCC（Strongly Connected Components）
3. 如果存在某個 xᵢ 使得 xᵢ 和 ¬xᵢ 在同一個 SCC 中 → 不可滿足
4. 否則 → 可滿足，且可以用拓撲排序給出解

**為什麼這是對的？**

**不可滿足的充分必要條件：** φ 不可滿足 ⟺ 存在變數 x 使得 x 和 ¬x 在同一個 SCC 中。

- （⟹）如果 x 和 ¬x 在同一個 SCC 中，表示 x → ... → ¬x 且 ¬x → ... → x。
  - 如果 x = True，推出 ¬x = True，矛盾。
  - 如果 x = False，即 ¬x = True，推出 x = True，矛盾。
  - 所以不可滿足。

- （⟸）如果沒有這種情況，可以構造解：
  - 把 SCC 縮點，得到 DAG
  - 做反向拓撲排序
  - 對每個未賦值的變數 x：如果 x 的 SCC 在 ¬x 的 SCC 的拓撲序之後，設 x = True

**時間複雜度：** SCC（Tarjan 或 Kosaraju）是 O(V + E) = O(n + m)。所以 **2-SAT ∈ P**。

> **🔰 2-SAT 為什麼在 P？直覺解釋**
>
> 3-SAT 是 NPC，但 2-SAT（每個子句只有 2 個 literal）卻在 P！差別只是每個子句少了 1 個 literal，為什麼難度差這麼多？
>
> **關鍵在於 implication 的結構。** 2-SAT 的每個子句 $(a \vee b)$ 可以改寫成「如果 $\neg a$ 就必須 $b$」和「如果 $\neg b$ 就必須 $a$」。這些 implication 形成一個有向圖——**Implication Graph**。
>
> 在這個圖上，如果 $x$ 和 $\neg x$ 在同一個 SCC（強連通分量）中，代表 $x$ 能推出 $\neg x$、$\neg x$ 也能推出 $x$，邏輯矛盾 → 不可滿足。否則就一定有解。
>
> **為什麼 3-SAT 不能這樣做？** 因為 $(a \vee b \vee c)$ 不能簡單寫成二元 implication。$\neg a$ 不能直接推出 $b$ 或 $c$ 中的哪一個——選擇太多了，無法用有向圖的 SCC 結構處理。
>
> **白話總結：** 2-SAT 的「選擇」很簡單（二選一），可以用圖論快速解決。3-SAT 的「選擇」太複雜（三選一以上），沒有已知的快速方法。

**完整範例：**

φ = (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₃) ∧ (¬x₂ ∨ ¬x₃) ∧ (x₁ ∨ ¬x₃)

Implication Graph 的邊：
```
(x₁ ∨ x₂):    ¬x₁ → x₂,   ¬x₂ → x₁
(¬x₁ ∨ x₃):   x₁ → x₃,    ¬x₃ → ¬x₁
(¬x₂ ∨ ¬x₃):  x₂ → ¬x₃,   x₃ → ¬x₂
(x₁ ∨ ¬x₃):   ¬x₁ → ¬x₃,  x₃ → x₁
```

所有邊：
```
¬x₁ → x₂, ¬x₂ → x₁, x₁ → x₃, ¬x₃ → ¬x₁,
x₂ → ¬x₃, x₃ → ¬x₂, ¬x₁ → ¬x₃, x₃ → x₁
```

SCC 分析：
- x₃ → x₁ → x₃（透過 x₁ → x₃ 和 x₃ → x₁）→ {x₁, x₃} 在同一 SCC
- ¬x₁ → ¬x₃（直接邊）和 ¬x₃ → ¬x₁（直接邊）→ {¬x₁, ¬x₃} 在同一 SCC
- 檢查：沒有 xᵢ 和 ¬xᵢ 在同一 SCC → 可滿足！

構造解：SCC 縮點後的 DAG 中，{x₁, x₃} 的拓撲序在 {¬x₁, ¬x₃} 之後 → x₁ = True, x₃ = True。
¬x₂ → x₁ 和 x₂ → ¬x₃，{x₂} 和 {¬x₂} 分析後 → x₂ = False 或 True 皆可，取 x₂ = False。

驗證：x₁=T, x₂=F, x₃=T
- (T ∨ F) = T ✓
- (F ∨ T) = T ✓
- (T ∨ F) = T ✓ （¬x₂=T, ¬x₃=F → T ∨ F = T）
- (T ∨ F) = T ✓

### 8.2 DAG 上的 Hamiltonian Path ∈ P

一般圖上的 Hamiltonian Path 是 NPC，但如果圖是 DAG（有向無環圖）：

**演算法：**
1. 做拓撲排序，得到序列 v₁, v₂, ..., vₙ
2. 檢查對每個 i，是否 (vᵢ, vᵢ₊₁) ∈ E
3. 如果全部都有邊 → Hamiltonian Path = v₁ → v₂ → ... → vₙ
4. 否則 → 不存在 Hamiltonian Path

**正確性：** 在 DAG 中，Hamiltonian Path 必須和拓撲排序一致（因為所有邊都「往前走」）。如果拓撲排序唯一（相鄰頂點都有邊），那就是 Ham Path；如果拓撲排序不唯一（某處 vᵢ → vᵢ₊₁ 沒有邊），那不可能有 Ham Path（因為任何 Ham Path 都必須是某種拓撲序，而在那個斷點處無法前進）。

**時間複雜度：** O(V + E)。

### 8.3 二部圖最大獨立集 ∈ P

一般圖上的最大獨立集是 NPC，但在二部圖上：

**König's Theorem：** 在二部圖中，
```
最大匹配數 = 最小頂點覆蓋數
```

又因為：
```
最大獨立集 = n - 最小頂點覆蓋 = n - 最大匹配
```

**演算法：**
1. 用 Hopcroft-Karp 或 Hungarian 演算法找最大匹配 M
2. 最大獨立集大小 = n - |M|
3. 要找出具體的獨立集，可以透過最小頂點覆蓋的構造

**時間複雜度：** O(E√V)（Hopcroft-Karp）。

---

## 九、常考的 True/False 題目和詳解

### 9.1 "If L ∈ NPC and L ∈ P, then P = NP" → **True**

**推導：**
1. L ∈ NPC 表示對所有 L' ∈ NP，L' ≤_p L
2. L ∈ P 表示 L 有多項式時間演算法 A
3. 對任意 L' ∈ NP：
   - 因為 L' ≤_p L，存在多項式歸約 f
   - 要判斷 x ∈ L'，先算 f(x)（多項式時間），再用 A 判斷 f(x) ∈ L（多項式時間）
   - 多項式 + 多項式 = 多項式
   - 所以 L' ∈ P
4. 所以 NP ⊆ P，又 P ⊆ NP，故 P = NP。∎

**白話：** 如果一個 NPC 問題有了快速解法，所有 NP 問題都可以透過歸約得到快速解法。NPC 問題是 NP 的「代表」，一個塌了全部塌。

### 9.2 "If L ∈ NP then L̄ ∈ NP" → **False（open question）**

**解釋：**
- L̄ ∈ NP 等價於 L ∈ co-NP
- 所以這個命題等價於「NP ⊆ co-NP」，即「NP = co-NP」
- 這是一個未解的 open question！
- 多數複雜度理論學家猜測 NP ≠ co-NP

**為什麼不能直接說 True？**
- NP 的 certificate 證明「x ∈ L」（Yes 答案有短證據）
- 但不代表「x ∉ L」也有短證據
- 例如：SAT ∈ NP（有 satisfying assignment 當 certificate），但 UNSAT（¬SAT）不知道是否在 NP 中——怎麼用短證據證明一個公式完全不可滿足？

### 9.3 "NP means not polynomial" → **False!**

**正確定義：** NP = Nondeterministic Polynomial time

**解釋：**
- "N" 是 Nondeterministic，不是 Not！
- NP 包含 P（P ⊆ NP），P 中的問題顯然是 polynomial time 的
- 如果 NP 真的是 "not polynomial"，那 P ∩ NP 就是空集，但我們知道 P ⊆ NP
- 這是初學者最常犯的錯誤

### 9.4 "If P = NP then NP = co-NP" → **True**

**推導：**
1. 假設 P = NP
2. P 對補封閉：L ∈ P ⟹ L̄ ∈ P（確定性 TM 直接把 accept/reject 翻轉）
3. 所以 P = co-P
4. 因此：
   ```
   NP = P = co-P = co-NP
   ```
5. 所以 NP = co-NP。∎

**另一個推導方式：**
1. 假設 P = NP
2. 要證 co-NP ⊆ NP：取 L ∈ co-NP，則 L̄ ∈ NP = P，所以 L̄ ∈ P，所以 L ∈ P = NP。✓
3. 要證 NP ⊆ co-NP：取 L ∈ NP = P，則 L̄ ∈ P ⊆ NP，所以 L ∈ co-NP。✓
4. 所以 NP = co-NP。∎

### 9.5 更多常考命題

**"If A ≤_p B and B ∈ P, then A ∈ P"** → **True**
- 歸約 f 是 poly-time，B 的演算法是 poly-time，組合起來是 poly-time。

**"If A ≤_p B and A ∈ NPC, then B ∈ NPC"** → **False**（B 是 NP-hard，但不一定在 NP 中）
- 正確的是：B 是 NP-hard。如果額外知道 B ∈ NP，才能說 B ∈ NPC。

**"If A ≤_p B and B ≤_p A, then A and B have the same complexity"** → **True**（在多項式時間等價的意義下）
- A ∈ P ⟺ B ∈ P。

**"Every problem in NP can be solved in exponential time"** → **True**
- NP 問題可以暴力枚舉所有 certificate（指數多個），每個用多項式時間驗證。
- 所以 NP ⊆ EXP。

**"If L is NP-hard and L ∈ P, then P = NP"** → **True**
- 和 9.1 的證明一模一樣。NP-hard 就夠了，不需要 L ∈ NP。

---

## 十、近似演算法的概念

> 既然 NPC 問題（在 P ≠ NP 的假設下）沒有多項式精確解，我們退而求其次：
> 能不能在多項式時間內找到「差不多好」的解？

### 10.1 ρ-approximation 的定義

對最小化問題：

一個演算法 A 是 **ρ-approximation**，如果對所有 instance I：
```
A(I) ≤ ρ · OPT(I)
```
其中 A(I) 是演算法的解，OPT(I) 是最佳解。ρ ≥ 1（越接近 1 越好）。

對最大化問題：
```
A(I) ≥ (1/ρ) · OPT(I)
```
或者有些教科書定義 approximation ratio 為 OPT/A ≤ ρ。

### 10.2 Vertex Cover 2-approximation

**演算法 APPROX-VERTEX-COVER(G)：**
```
C = ∅
E' = E
while E' ≠ ∅:
    取任意邊 (u, v) ∈ E'
    C = C ∪ {u, v}
    從 E' 中移除所有和 u 或 v 相關的邊
return C
```

**分析：**
- 設演算法選了 t 條邊（互不相鄰，因為選完就刪了相關的邊）。
- |C| = 2t。
- OPT 至少要選 t 個頂點（這 t 條邊互不相鄰，每條至少要覆蓋一端）。
- 所以 |C| = 2t ≤ 2 · OPT。

**結論：** 這是一個 2-approximation。

**例子：**
```
圖：1—2—3—4—5
選邊 (1,2)：C = {1,2}，刪除和 1,2 相關的邊
剩下：3—4—5
選邊 (3,4)：C = {1,2,3,4}，刪除和 3,4 相關的邊
剩下：5（無邊）
C = {1,2,3,4}，|C| = 4
OPT = {2,4}，|OPT| = 2
確實 4 ≤ 2 × 2 ✓
```

### 10.3 MAX-SAT 隨機近似

**MAX-SAT：** 給定 CNF 公式，找一個 assignment 使被滿足的子句數最多。

**隨機演算法：** 每個變數獨立地以 1/2 的機率設為 True。

**分析：**
- 一個有 k 個 literals 的子句不被滿足的機率 = (1/2)^k
- 被滿足的機率 = 1 - (1/2)^k ≥ 1/2（當 k ≥ 1）
- 如果每個子句至少有 k 個 literals：
  - 期望被滿足的子句數 ≥ (1 - (1/2)^k) · m ≥ m/2
- 對 3-SAT（k = 3）：期望滿足 7/8 · m 個子句

**結論：**
- MAX-SAT 的隨機 1/2-approximation（白話：期望至少滿足一半的子句）
- MAX-3-SAT 的隨機 7/8-approximation
- 而且 7/8 是 tight 的（除非 P = NP，不可能做到更好，by Hastad's result）

---

## 附錄：歸約方向速查表

| 要證的問題 L | 從哪個已知 NPC 歸約 | 歸約方向 |
|-------------|-------------------|---------|
| SAT | 所有 NP（Cook-Levin） | ∀L' ∈ NP, L' ≤_p SAT |
| 3-SAT | SAT | SAT ≤_p 3-SAT |
| CLIQUE | 3-SAT | 3-SAT ≤_p CLIQUE |
| Independent Set | 3-SAT | 3-SAT ≤_p IS |
| Vertex Cover | Independent Set | IS ≤_p VC |
| Subset Sum | 3-SAT | 3-SAT ≤_p SUBSET-SUM |
| Ham Cycle | 3-SAT | 3-SAT ≤_p HAM-CYCLE |
| Ham Path | Ham Cycle | HAM-CYCLE ≤_p HAM-PATH |
| TSP | Ham Cycle | HAM-CYCLE ≤_p TSP |
| DCST(K=2) | Ham Path | HAM-PATH ≤_p DCST |
| Subgraph Iso | Ham Cycle | HAM-CYCLE ≤_p SUB-ISO |
| 3-COLORING | 3-SAT | 3-SAT ≤_p 3-COL |

**記住歸約方向的口訣：**
> **「從已知的難題歸約到要證的問題」**
> 箭頭指向要證的問題。已知 Hard →_p 要證 Hard。

---

## 附錄：常見陷阱彙整

1. **歸約方向搞反：** A ≤_p B 是「B 至少和 A 一樣難」，不是 A 比 B 難！
2. **只證一個方向：** 正確性必須證 x ∈ L' ⟺ f(x) ∈ L，雙向都要！
3. **忘記證 L ∈ NP：** NPC 需要兩步，很多人只做歸約忘了給 certificate + verifier。
4. **把 NP 當成 "Not Polynomial"：** NP = Nondeterministic Polynomial，P ⊆ NP！
5. **混淆 NP-hard 和 NPC：** NP-hard 不一定在 NP 中！NPC = NP ∩ NP-hard。
6. **以為 NP 問題都很難：** P ⊆ NP，排序也在 NP 中。
7. **以為 NPC 證明是證「不能解」：** NPC 是在 P ≠ NP 的假設下才沒有多項式解。
8. **Encoding 的影響：** Subset Sum 是 weakly NPC（unary 編碼下有 poly 解），注意 pseudopolynomial。
9. **co-NP 的理解：** L ∈ co-NP 不是 L ∉ NP，而是 L̄ ∈ NP。
10. **特殊情況的遺忘：** 2-SAT ∈ P, DAG 上 Ham Path ∈ P, 二部圖 IS ∈ P — 考試很愛考。

---

## 🔰 3-SAT → Independent Set 歸約的完整數值範例（每一步都畫出來）

為了幫助理解歸約，我們用一個最小的具體例子，一步一步完成整個歸約過程。

### 給定的 3-SAT instance

$$\varphi = (x_1 \vee \neg x_2 \vee x_3) \wedge (\neg x_1 \vee x_2 \vee x_3)$$

- 2 個子句（$m = 2$），所以我們要找大小 $\geq k = 2$ 的 Independent Set。
- 3 個變數：$x_1, x_2, x_3$。

### Step 1：建頂點（每個子句的每個 literal 一個頂點）

```
子句 C₁ = (x₁ ∨ ¬x₂ ∨ x₃)   →  頂點 v₁₁(x₁),  v₁₂(¬x₂),  v₁₃(x₃)
子句 C₂ = (¬x₁ ∨ x₂ ∨ x₃)   →  頂點 v₂₁(¬x₁), v₂₂(x₂),   v₂₃(x₃)
```

共 6 個頂點。

### Step 2：加 Clause Edges（同一子句內的三角形）

```
C₁ 內部：v₁₁—v₁₂, v₁₁—v₁₃, v₁₂—v₁₃  （三角形）
C₂ 內部：v₂₁—v₂₂, v₂₁—v₂₃, v₂₂—v₂₃  （三角形）
```

**意義：** 同一子句最多只能選一個頂點進入 Independent Set。

### Step 3：加 Contradiction Edges（互相矛盾的 literal 連邊）

```
v₁₁(x₁) — v₂₁(¬x₁)    ← x₁ 和 ¬x₁ 矛盾
v₁₂(¬x₂) — v₂₂(x₂)    ← ¬x₂ 和 x₂ 矛盾
```

（$v_{13}(x_3)$ 和 $v_{23}(x_3)$ 不矛盾——它們是同一個 literal，不需要連邊。）

### Step 4：畫出完整的圖

```
    C₁ 三角形                    C₂ 三角形
    v₁₁(x₁) ---- v₁₂(¬x₂)      v₂₁(¬x₁) ---- v₂₂(x₂)
       \         /                   \         /
        \       /                     \       /
        v₁₃(x₃)                      v₂₃(x₃)

    跨子句 contradiction edges:
    v₁₁(x₁) ———————————— v₂₁(¬x₁)
    v₁₂(¬x₂) ——————————— v₂₂(x₂)
```

### Step 5：找大小為 k=2 的 Independent Set

嘗試 $x_1 = T, x_2 = F, x_3 = T$：
- $C_1$ 中 $x_1 = T$ → 選 $v_{11}$
- $C_2$ 中 $x_3 = T$ → 選 $v_{23}$
- $S = \{v_{11}, v_{23}\}$，$|S| = 2 = k$

**檢查 Independent Set：**
- $v_{11}$ 和 $v_{23}$ 之間有邊嗎？不同子句 + $x_1 \neq \neg x_3$ → **無邊** → 合法！

反向驗證：從 $S = \{v_{11}(x_1), v_{23}(x_3)\}$ 構造 assignment：$x_1 = T, x_3 = T$，$x_2$ 任意（取 $F$）。
- $C_1 = (T \vee T \vee T) = T$ ✓
- $C_2 = (F \vee F \vee T) = T$ ✓

**歸約成功！** 3-SAT 的解 ⟺ Independent Set 的解。

---

## 🔰 自我檢測

完成本章後，試著回答以下問題。如果有任何一題答不上來，建議回去重讀對應段落。

### 觀念題

1. **NP 是 "Non-Polynomial" 的縮寫嗎？** NP 的正確含義是什麼？P 和 NP 的包含關係是什麼？

2. **用自己的話解釋 certificate 和 verifier。** 以 CLIQUE 問題為例，certificate 是什麼？verifier 做什麼？

3. **A $\leq_p$ B 是什麼意思？** 哪個問題比較難？歸約的方向為什麼容易記反？

4. **證明 NPC 的兩個步驟分別是什麼？** 如果只做了其中一步，能得到什麼結論？

5. **2-SAT 為什麼在 P，而 3-SAT 是 NPC？** 用 Implication Graph 的角度解釋。

### 計算題

6. 對以下 3-SAT instance，執行 3-SAT → Independent Set 的歸約，畫出圖，並找到一個大小為 $k$ 的 Independent Set。
   ```
   φ = (x₁ ∨ x₂ ∨ ¬x₃) ∧ (¬x₁ ∨ ¬x₂ ∨ x₃)
   ```

7. 對以下 2-SAT instance，畫出 Implication Graph，找 SCC，判斷是否可滿足，並給出一組解。
   ```
   φ = (x₁ ∨ x₂) ∧ (¬x₁ ∨ x₂) ∧ (x₁ ∨ ¬x₂)
   ```

### 判斷題（True/False，並說明理由）

8. 「如果 L ∈ NPC 且 L ∈ P，則 P = NP。」

9. 「如果 A ≤_p B 且 A ∈ NPC，則 B ∈ NPC。」

10. 「NP 中所有問題都很難。」

11. 「如果 P = NP，則 NP = co-NP。」

12. 「Subset Sum 用動態規劃可以在 O(nW) 時間解決，所以它不是 NP-Complete。」

### 參考答案提示

- 第 1 題：NP = Nondeterministic Polynomial time，不是 Not Polynomial。P $\subseteq$ NP。
- 第 8 題：True。NPC 問題是 NP 的「代表」，一個有快解，所有 NP 問題都能透過歸約得到快解。
- 第 9 題：False。只能說 B 是 NP-hard。B 不一定在 NP 中，所以不一定是 NPC。
- 第 10 題：False。P $\subseteq$ NP，排序也在 NP 中。NP 中有很多容易的問題。
- 第 12 題：False。$O(nW)$ 是 **偽多項式時間**（pseudo-polynomial），因為 $W$ 的輸入大小是 $\log W$，不是 $W$。Subset Sum 是 weakly NP-Complete。
