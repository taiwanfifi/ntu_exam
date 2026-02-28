# 米亞的演算法筆記 #05
## 鏈結串列與 Floyd 判圈法 Linked List / Floyd's Cycle Detection
> 出現於：第27-29章〈蘇曉晴的無盡星期三——記憶被困在循環中〉

---

### ◈ 這個概念在故事裡是什麼

蘇曉晴每天早上醒來，都是星期三。

不是「感覺像星期三」。是她的記憶鏈結串列在第 37 個節點形成了一個環——從那天起，每一天的記憶都指向同一個「星期三早晨」的起點。她的日子不是往前走的。她的日子是一個圓。而最恐怖的部分是：**她不知道自己在重複。**

每個星期三，她都覺得是第一次。去同一家早餐店，點同一碗豆漿，對老闆說「今天天氣不錯」。老闆已經聽了 37 次了。但蘇曉晴每次都覺得是第一次說。

我用 Floyd 的龜兔演算法去偵測她的記憶循環。慢指標是「現在的蘇曉晴」，快指標是「加速回放的蘇曉晴」。當兩個版本的她在同一個記憶節點重合——我就找到了環。但找到環不是結局。**切斷環才是。** 切斷的代價：37 天份的真實記憶會在一瞬間全部湧回——包括她父親的葬禮。

---

### ◈ 正式定義

**Linked List（鏈結串列）：**

$$
\text{Node} = \{ \text{val}, \text{next} \} \qquad \text{next} \in \{\text{Node}, \text{NULL}\}
$$

每個節點存一個值，並指向下一個節點。若 `next` 指回先前的節點——就形成了**環（cycle）**。

**Floyd's Cycle Detection（龜兔判圈法）：**

$$
\text{slow} \leftarrow \text{slow.next} \;(\text{每次 1 步}) \qquad \text{fast} \leftarrow \text{fast.next.next} \;(\text{每次 2 步})
$$
$$
\text{若存在環} \Rightarrow \exists\, t : \text{slow}_t = \text{fast}_t
$$

**找環入口：** 相遇後，將一指標移回 head，兩者改為每次 1 步，再次相遇即為環入口。

$$
\text{設 } a = \text{head→入口距離},\; b = \text{入口→相遇點},\; c = \text{環長}
$$
$$
2(a+b) = a + b + nc \;\Rightarrow\; a = (n-1)c + (c-b)
$$

白話：從 head 走 $a$ 步到入口 = 從相遇點走 $c - b$ 步到入口。同速前進，必在入口相遇。

---

### ◈ 推導

**為什麼快慢指標一定會相遇？**

1. **前提：** 環存在，環長為 $c$。
2. **進入環後：** slow 和 fast 都在環內，相對距離 $d \leq c$。
3. **每走一步：** 相對距離縮小 1（fast 比 slow 快 1 步）。
4. **$d$ 步後：** 距離歸零 → 相遇。

$$
T(\text{detection}) = O(a + c) = O(n) \qquad S = O(1)
$$

**關鍵優雅之處：** 不用 HashSet 記錄走過的節點。只用兩個指標，$O(n)$ 時間、$O(1)$ 空間。

---

### ◈ 帶入數字算算看：蘇曉晴的 37 天循環

```
Day1 → Day2 → ... → Day15 → Day16 → Day17 → ... → Day52 → ─┐
                       ↑                                       │
                       └───────────────────────────────────────┘
                       環入口 = Day 16，環長 c = 37 天
```

- 非環部分：$a = 15$，環長：$c = 37$

**Floyd 偵測過程：**

| 步數 | slow 位置 | fast 位置 | 相遇？ |
|------|-----------|-----------|--------|
| 0 | Day1 | Day1 | - |
| 15 | Day16（入口）| Day31 | 否 |
| 30 | Day31 | Day46 | 否 |
| 52 | Day16 | Day16 | **相遇！** |

驗算：slow 走 52 步 = 15 + 37 → 回到 Day16。fast 走 104 步 = 15 + 37×2 + 15 → 也在 Day16。

**找入口：** fast 移回 Day1，同速前進 15 步 → 兩者在 **Day 16** 相遇——第一個「星期三」。

---

### ◈ 更深一層：不知道自己在重複

蘇曉晴教會我——最恐怖的迴圈不是「出不去」，是「不知道自己在裡面」。

程式的無窮迴圈會讓 CPU 飆到 100%，系統當機，人會注意到。但蘇曉晴的迴圈不會當機。她微笑、工作、吃飯、睡覺。沒有 error log。一切正常——除了她永遠停在星期三。

人類有多少迴圈是自己看不見的？重複同樣的爭吵模式，重複同樣的自我否定，重複同樣的選擇然後說「這次不一樣」。

Floyd 的龜兔演算法有效，是因為**它從外部觀察**。你不能從迴圈內部偵測迴圈——你需要一個跑得比你快的參照點。蘇曉晴需要的不是演算法，是一個**跑得比她快的人**，從外面告訴她：「你在重複。」

而切斷環的代價——37 天記憶同時湧回——她父親的葬禮在第 23 天。她不在場。她在點豆漿。

---

### ◈ 跨卷連結

| 連結 | 說明 |
|------|------|
| **#01 Array** → **#05 Linked List** | Array 是靜態排列；Linked List 是動態連結。記憶是一個接一個指向下去的。 |
| **#04 Stack** → **#05 Linked List** | Stack 是「剝開」，Linked List 是「追蹤」。張國棟遇到空，蘇曉晴遇到環。 |
| **#05 Floyd** → **#09 Graph/CC** | Floyd 偵測線性結構中的環。第二卷發現——環跨越了整個記憶網絡。 |
| **#05 切斷環** → **#15 Backtracking** | 切斷是「強制中斷」。Backtracking 是「有選擇地回退」。回退的路上有你愛的人。 |

---

### 練習題

**Q1.** 用 HashSet 偵測環 vs Floyd，蘇曉晴的 52 節點鏈，時間與空間複雜度各是多少？

<details><summary>答案</summary>

**HashSet：** 時間 $O(52)$，空間 $O(52)$。**Floyd：** 時間 $O(52)$，空間 $O(1)$。
差異：Floyd 不需額外記憶體。蘇曉晴的記憶系統已被佔滿——Floyd 是唯一選擇。
</details>

**Q2.** 如果環長是 1（節點 next 指向自己），Floyd 還能偵測嗎？

<details><summary>答案</summary>

**可以。** slow 和 fast 進入該節點後，下一步都在原地 → 立即相遇。這是最極端的迴圈——蘇曉晴連「以為在前進」的幻覺都被剝奪了。
</details>

**Q3.** 設計修復函式：讓 Day52 指向 Day53 而非回到 Day16。

<details><summary>答案</summary>

```python
def repair_cycle(head):
    # Floyd 找環入口
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast: break
    slow = head
    while slow != fast:
        slow, fast = slow.next, fast.next
    entry = slow  # Day16
    # 找環尾（next == entry 的節點）
    cur = entry
    while cur.next != entry:
        cur = cur.next
    # 修復：尾巴指向新節點
    cur.next = Node("Day53_真實記憶")
    cur.next.next = None  # 鏈結恢復終止
    return head  # 代價：37 天記憶同時湧回
```
</details>

---

> *「她不知道自己在重複。那是最壞的迴圈——不是因為出不去，而是因為裡面太舒服了。豆漿是熱的，老闆會笑，天氣永遠不錯。誰會想離開一個完美的星期三？」* — 第29章〈蘇曉晴的無盡星期三〉
