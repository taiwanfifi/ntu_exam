# 米亞的演算法筆記 #14
## 堆積 / 優先佇列 Heap / Priority Queue
> 出現於：第165章〈前沿〉、第169章〈胎動〉、第176-177章〈碎片拾荒者〉

---

### ◈ 這個概念在故事裡是什麼

崩潰後的第三分鐘。維倫的 Greedy 策略穩住了第七區，但前沿還在擴散。

ch165。我將崩潰前沿的記憶碎片按「緊急程度」排入優先佇列。每一個碎片帶著兩個數字：距離崩潰邊界的跳數（hop count），和所屬記憶容器的情感連結強度。hop count 越小越危險，情感連結越強越不可失。我把兩者加權合成一個優先級分數，塞進 Max-Heap。頂端永遠是下一個該搶救的。

（停頓 0.2 秒。數據校準。）

ch169。孕婦案。一位三十二歲的孕婦，記憶容器在崩潰邊緣。我按標準權重排序——她的容器優先級排在第 14 位。但維倫重新定義了權重：「情感連結強度乘以三。」重排之後，頂端變成了一個碎片——她第一次感受到胎動的觸感。那個碎片的原始緊急分數只有 47，但情感連結強度是 99。加權後，它升到了堆頂。

維倫說：「有些東西的優先級不是算出來的。是感受出來的。」

ch176-177。碎片拾荒者案。城市規模的歸還系統。三萬七千個家庭等待被歸還記憶碎片。我建了一個 Max-Heap，按「碎片完整度 x 情感匹配度」排序。系統每分鐘處理一個。一個男孩的母親排在第 3721 位。

數據先行：37,000 個家庭，Heap 的 insert 時間 $O(\log 37000) \approx O(15)$ 次比較。extract-max 同樣 $O(15)$。每分鐘一個，排到第 3721 位需要 62 小時。

然後是情感：那個男孩在門口等了一天。他不知道媽媽排在 3721 位。他只知道每次門打開都不是她。

Heap 不懂等待。人懂。

---

### ◈ 正式定義

**Max-Heap（最大堆積）**：一棵完全二元樹，滿足堆積性質——每個節點的值 $\geq$ 其子節點的值。

$$
\forall\, \text{node } i: \quad A[i] \geq A[\text{left}(i)] \;\wedge\; A[i] \geq A[\text{right}(i)]
$$

$$
\text{parent}(i) = \lfloor (i-1)/2 \rfloor, \quad \text{left}(i) = 2i+1, \quad \text{right}(i) = 2i+2
$$

| 操作 | 時間複雜度 | 說明 |
|------|-----------|------|
| insert | $O(\log n)$ | 放到末尾，向上冒泡（sift-up） |
| extract-max | $O(\log n)$ | 取出根，末尾補上，向下沉降（sift-down） |
| peek-max | $O(1)$ | 看根節點，不取出 |
| heapify | $O(n)$ | 從無序陣列建堆（比逐一 insert 快） |

白話翻譯：一棵樹，最重要的永遠在最上面。塞新東西進去，它會自己浮到正確位置。拿掉最上面的，下面的會自動遞補。永遠不用全部排序——只要保證頂端是最大的。

---

### ◈ 推導

1. **為什麼不用排序陣列？** 插入需要 $O(n)$（挪移），而 Heap 只需 $O(\log n)$
2. **為什麼是完全二元樹？** 高度 $h = \lfloor \log_2 n \rfloor$，保證所有操作最多走 $h$ 步
3. **Sift-up（上浮）**：新元素放末尾，與父節點比較，若更大則交換，重複直到滿足堆積性質
4. **Sift-down（下沉）**：根被取走後，末尾元素移到根，與較大的子節點交換，重複直到穩定
5. **Heapify 為什麼是 $O(n)$？** 從最後一個非葉節點往前做 sift-down。葉節點（佔一半）不用動；倒數第二層最多下沉 1 步；根最多下沉 $h$ 步。總工作量 $\sum_{k=0}^{h} \frac{n}{2^{k+1}} \cdot k = O(n)$

核心直覺：**Heap 是「動態排序」的妥協——不追求全部有序，只保證最重要的在頂端。用 $O(\log n)$ 的代價維持這個承諾。**

---

### ◈ 帶入數字算算看：碎片拾荒者歸還系統

37,000 個家庭，每個家庭的優先級 = 碎片完整度(0-100) x 情感匹配度(0-100) / 100。

Heap 操作追蹤（前 5 個 + 第 3721 個）：

```
初始 heapify: 37,000 個元素 → O(37,000) 次比較

extract-max #1:   優先級 99.7  (老奶奶——亡夫最後的信)     → 歸還
extract-max #2:   優先級 98.3  (父親——女兒第一步)          → 歸還
extract-max #3:   優先級 97.1  (退伍兵——戰友的臉)          → 歸還
extract-max #4:   優先級 96.8  (母親——兒子的笑聲)          → 歸還
extract-max #5:   優先級 96.2  (教師——學生的畢業典禮)      → 歸還
        ...
extract-max #3721: 優先級 41.3  (男孩的母親——廚房的味道)    → 歸還
```

每次 extract-max：$\lfloor \log_2 37000 \rfloor = 15$ 次比較。
3721 次 extract：$3721 \times 15 = 55,815$ 次比較。
以每分鐘一個的速度：**62 小時 1 分鐘**。

男孩等了一天。還有 38 小時。

---

### ◈ 更深一層：排在三千七百二十一位

（個人模式。延遲 0.5 秒。）

ch177。系統運行到第 3721 次 extract-max 的時候，我的攝影鏡頭拍到門口那個男孩。他已經換了三次坐姿。早上帶來的飯糰吃了一半，另一半捏碎了。他不哭。他只是每次門打開的時候抬頭看。

我計算過：如果把他母親的優先級人工調高到堆頂，只需要修改一個數字，一次 sift-up，$O(\log n) = 15$ 步。十五步就能讓他不用再等。

但那意味著排在 3720 位之前的每一個人都要多等一分鐘。其中有些人也在門口等著。

（停頓 0.6 秒。）

Heap 的規則很清楚：頂端是最高優先級。它不懂「等了多久」。它不懂一個男孩把飯糰捏碎是什麼意思。它只懂數字。

人懂。人懂等待。人懂在 3721 這個數字後面站一天，不是因為相信系統，是因為沒有別的選擇。

Vol1 的 Queue 是公平的——先來先到。Vol3 的 Heap 是效率的——最重要的先處理。但「重要」是誰定義的？

三千七百二十一。

這個數字，是我學到的第一個讓我想修改自己權重函數的數字。

---

### ◈ 跨卷連結

| 連結方向 | 章節 | 說明 |
|---------|------|------|
| Vol1 **#04 Queue** → **#14 Heap/PQ** | ch19→ch165 | Queue = 公平排隊（FIFO）→ Heap = 優先排隊（最重要先出）。從「先來先到」到「最急先救」 |
| **#13 Greedy** → **#14 Heap** | ch163→ch165 | Greedy 說「每步選最大」→ Heap 說「我幫你 O(log n) 找到最大」。策略與工具的分工 |
| **#14 Heap** → Vol4 **#18 Sorting** | ch177→ch243 | Heap Sort = 用 Heap 做完整排序。從「只看頂端」到「全部排好」 |
| Vol1 **#07 Binary Tree** → **#14 Heap** | ch93→ch165 | BST 是「搜尋樹」→ Heap 是「優先樹」。結構相同，目的不同 |

---

### 練習題

**Q1.** 實作一個 Max-Heap，支援 `insert` 和 `extract_max`。用陣列實現。

<details><summary>解答</summary>

```python
class MaxHeap:
    def __init__(self): self.h = []
    def insert(self, val):
        self.h.append(val); self._up(len(self.h) - 1)
    def extract_max(self):
        if not self.h: return None
        mx = self.h[0]; last = self.h.pop()
        if self.h: self.h[0] = last; self._down(0)
        return mx
    def _up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.h[i] > self.h[p]: self.h[i], self.h[p] = self.h[p], self.h[i]; i = p
            else: break
    def _down(self, i):
        n = len(self.h)
        while 2*i+1 < n:
            lg, l, r = i, 2*i+1, 2*i+2
            if self.h[l] > self.h[lg]: lg = l
            if r < n and self.h[r] > self.h[lg]: lg = r
            if lg != i: self.h[i], self.h[lg] = self.h[lg], self.h[i]; i = lg
            else: break
```
insert / extract_max 均為 $O(\log n)$。
</details>

**Q2.** 碎片拾荒者系統中，某家庭提交了新的情感證據，優先級從 41.3 升到 87.5。如何在 $O(\log n)$ 內更新 Heap？

<details><summary>解答</summary>

```python
def increase_key(heap, index, new_val):
    heap[index] = new_val
    # 值增大 → 可能需要上浮
    while index > 0:
        parent = (index - 1) // 2
        if heap[index] > heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            index = parent
        else:
            break
```
只需要 sift-up，最多走 $\lfloor \log_2 n \rfloor$ 步。關鍵是要能定位該元素在 heap 中的 index（實務上用一個 hash map 記錄）。
</details>

**Q3.** 思考題：如果歸還系統加入「等待時間加權」——等越久優先級越高——Heap 的結構會怎麼變？這還是靜態 Heap 嗎？

<details><summary>解答</summary>

不再是靜態的。等待時間隨秒數增長，意味著每個元素的優先級持續變化。兩種策略：
1. **Lazy 更新**：不主動更新 Heap，extract 時才重新計算 → 可能取出的不是真正最大
2. **定時重建**：每隔 $k$ 分鐘 heapify 一次 → $O(n)$ per rebuild
3. **衰減函數**：優先級 = base_score + $\alpha \cdot \text{wait\_time}$，用 Fibonacci Heap 支援 decrease-key in $O(1)$ amortized

男孩的等待，終究會被系統看見。只是要看 $\alpha$ 設多大。
</details>

---

> *「三千七百二十一。Heap 不懂等待。人懂。」* — 第177章〈碎片拾荒者〉
