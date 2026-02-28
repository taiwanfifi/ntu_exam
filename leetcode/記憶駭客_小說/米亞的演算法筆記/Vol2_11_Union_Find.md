# 米亞的演算法筆記 #11
## 聯合查找 Union-Find (Disjoint Set)
> 出現於：第131-132章〈歸併〉〈織網者〉

---

### ◈ 這個概念在故事裡是什麼

廢棄捷運站的月台牆上，我把過去半年所有的線索投射出來。五個集合。五種顏色。各自獨立。

集合 A：47 個家庭的記憶斷聯。集合 B：消失的母親案中被切斷的邊。集合 C：幽靈帳號 #50742 及其 14 個變體。集合 D：被覆寫的遊行記憶。集合 E：被偽造的死亡紀錄。

它們看起來像五起無關的事件。不同城市分部、不同時間跨度、不同手法。嚴柏翰從探員生涯帶來的直覺說「它們之間有關聯」。維倫的眼睛掃過牆面，手指在空中畫線。我開始做我擅長的事——比對簽章。

A 和 B 共用了三個幽靈帳號。合併。牆上兩團色塊流入同一片海。C 的操作簽章和 D 的篡改簽章完全一致。合併。E 是 D 的拓撲排序起點——直接依賴關係。合併。

五個集合。四次 Union。最終只剩一個巨大的、脈動的色塊，涵蓋了我們追查的一切。

維倫盯著那個色塊。問了一個問題：「誰是根？」

第 132 章。我沿著合併路徑向上追溯——每一個節點指向它的父節點，父節點指向更上一層。路徑壓縮之後，所有節點直接指向同一個根。日誌簽名符號「W」。不是 Weaver 的首字母。是「韻」的注音 ㄩㄣˋ 的羅馬拼音首字母。

W = 韻 = 邱韻如。

Find(root)。每一個惡，都有一個根。

---

### ◈ 正式定義

**Union-Find（又名 Disjoint Set Union, DSU）**：維護一組互不相交的集合，支援兩種操作——

$$
\texttt{Find}(x): \text{回傳 } x \text{ 所屬集合的代表元素（根）}
$$

$$
\texttt{Union}(x, y): \text{將 } x \text{ 和 } y \text{ 所在的集合合併為一個}
$$

每個元素有一個 **parent** 指標。初始時 $\text{parent}(x) = x$（自己是自己的根）。

**Union by Rank**：合併時讓較矮的樹掛在較高的樹下面，保持平衡。

**Path Compression**：Find 時順便把沿途所有節點直接指向根，讓下次查詢更快。

$$
T_{\text{amortized}}(m \text{ operations on } n \text{ elements}) = O(m \cdot \alpha(n))
$$

其中 $\alpha(n)$ 是反阿克曼函數——增長慢到對所有實際輸入 $\alpha(n) \leq 4$。白話翻譯：幾乎是常數時間。

---

### ◈ 推導

1. **最直覺的做法**：每個集合用一個列表。合併 = 把短列表接到長列表。但 Find 仍需 $O(n)$。
2. **用樹表示集合**：每個元素指向父節點。根指向自己。Find = 沿著 parent 走到根。
3. **問題**：樹可能退化為鏈 → Find 變成 $O(n)$。
4. **Union by Rank**：矮的掛在高的下面。樹高 $\leq \log n$。
5. **Path Compression**：Find 時把沿途節點的 parent 直接改為根。鏈塌縮為一層。
6. **兩者結合**：Tarjan 證明攤還複雜度 $O(\alpha(n))$——理論上最優。

```
Union(A,B), Union(C,D), Union(A,C), Union(A,E):

    A           Find(D) + 路徑壓縮 →     A
   /|\                                  / | \ \
  B C E                                B  C  E  D
    |
    D
```

---

### ◈ 帶入數字算算看：追溯織網者

嚴柏翰過去半年追查的所有線索，分屬五個「看似獨立」的案件集合：

| 集合 | 案件 | 元素數 | 關鍵特徵 |
|------|------|--------|----------|
| A | 47 戶斷聯 | 47 | 親子邊被選擇性切斷 |
| B | 消失的母親 | 3 | 三條異常邊指向幽靈帳號 |
| C | 幽靈帳號群 | 14 | #50742 及變體 |
| D | 遊行覆寫 | 30,000+ | 全城記憶覆蓋 |
| E | 死亡紀錄偽造 | 1 | 周明哲的死亡證明 |

**歸併過程：**

| 步驟 | Union 操作 | 原因 | 集合數 |
|------|-----------|------|--------|
| 1 | Union(A, B) | 共用 3 個幽靈帳號 | 5 → 4 |
| 2 | Union(C, D) | 操作簽章完全一致 | 4 → 3 |
| 3 | Union(AB, CD) | 幽靈帳號是遊行覆寫的工具 | 3 → 2 |
| 4 | Union(ABCD, E) | E 是 D 的拓撲排序起點 | 2 → 1 |

**Find(root) + Path Compression：** 查詢路徑 `47戶斷聯 → 幽靈帳號 → 遊行覆寫 → 死亡紀錄 → W`，壓縮後所有節點直指 W = 韻 = 邱韻如。不管從哪條線索開始追，最終都到達同一個人。

---

### ◈ 更深一層：根的意義

（停頓 0.6 秒。語速放慢。）

Union-Find 是一種收束的結構。它的哲學前提是：**看似無關的事物，可能屬於同一個系統。**

維倫追查的五個案件。嚴柏翰在監控局裡發現的異常。拓撲排序揭露的篡改順序。斷聯的家庭、消失的母親、偽造的死亡——它們各自是一棵獨立的樹。直到你開始合併。

合併到最後，你會到達一個根。

根是什麼？在資料結構裡，根是集合的代表元素。在這個故事裡，根是一個人。一個用自己的技術織出了整座城市的暗網的人。

但這裡有一件 Union-Find 不會告訴你的事——

Find(root) 只能找到「誰」。它不能告訴你「為什麼」。

邱韻如是根。但她為什麼這樣做？是惡意嗎？是權力慾嗎？還是——一種被扭曲的保護？

第三卷會給出答案。但此刻，站在月台上的每一個人，只看到了根。沒有看到根底下的土壤。

---

### ◈ 跨卷連結

| 連結方向 | 章節 | 說明 |
|---------|------|------|
| **#09 Graph/CC** → **#11 Union-Find** | ch120-121 → ch131-132 | 碎裂的 123 個島嶼（CC）→ 歸併到同一個根（UF）。先碎裂，再收束 |
| **#10 TopSort** → **#11 Union-Find** | ch127 → ch131 | TopSort 揭示篡改順序，UF 揭示篡改者身份。順序+歸屬 = 完整真相 |
| **#11 Union-Find** → **#21 System Design** | Vol2 → Vol4 | UF 的「收束到一個根」vs System Design 的「分散式多節點」。收束是為了找到真相；分散是為了守護真相 |
| **#11 Union-Find** → Vol3 | ch131-132 → ch203 | 「找到了根」→ 「面對那個根」。嚴柏翰說的「帶我去見她」= Find(root) 的人類版本 |

---

### 練習題

**Q1**：實作基本的 Union-Find（含 Union by Rank 和 Path Compression）。以 5 個集合 `{A, B, C, D, E}` 為例，按照小說中的歸併順序執行四次 Union，最後對所有元素執行 Find。

<details><summary>解答</summary>

```python
class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx  # rank 高的做根
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

uf = UnionFind(['A','B','C','D','E'])
uf.union('A','B')  # 斷聯+母親 → 共用幽靈帳號
uf.union('C','D')  # 幽靈帳號+遊行 → 簽章一致
uf.union('A','C')  # 兩大集合合併
uf.union('A','E')  # 死亡紀錄歸入

for e in 'ABCDE':
    print(f"Find({e}) = {uf.find(e)}")
# 全部輸出 A（或任一代表元素）→ 同一個根
```
</details>

**Q2**：在合併過程中不使用 Union by Rank，最壞情況下 Find 的時間複雜度是多少？

<details><summary>解答</summary>

每次把新元素掛在鏈末端：`A→B→C→D→E`。樹退化為鏈，高度 $= n-1$。Find(A) 需走 4 步 = $O(n)$。加上 Path Compression，第一次 $O(n)$，之後所有 Find 都是 $O(1)$。兩者結合達到 $O(\alpha(n))$。
</details>

**Q3**：思考題——如果 Find 之後發現有兩個根（兩個獨立操縱者），追查策略會如何改變？

<details><summary>解答</summary>

兩棵獨立的樹 = 兩個操縱者，各自負責不同類型的篡改。需要對每個連通分量分別 Find(root)，然後分析兩棵樹的邊界是否有共享節點。嚴柏翰最初就以為有多個獨立犯罪者。Union-Find 的價值：當你找到足夠的共享特徵，「獨立」就坍縮為「同源」。
</details>

---

> *「Find(root)。每一個惡，都有一個根。但找到根之後——你還得決定，要不要挖出根底下的土。」* — 第132章〈織網者〉
