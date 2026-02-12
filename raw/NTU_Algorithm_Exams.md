# NTU 演算法歷屆考古題完整彙整

---

## 考試 1: 109-1 陳和麟 演算法 期中考

- 學期: 109-1
- 教授: 陳和麟
- 考試類型: 期中考
- 考試日期: 109.11.09
- 考試時限: 180 分鐘
- 課程性質: 電子所核心二選一必修、電信電機生醫電資所選修
- 備註: Closed book，可帶一張雙面手寫A4筆記

### 試題

**Problem 1.** Let all functions be positive functions. Prove or disprove the following three statements. You may only use the definitions of asymptotic notations. Any other property of asymptotic notations must be proved before using. Answering true/false without any explanation will not receive any credit.

1. (4%) log_2 n ∈ O(log_{10} n).
2. (8%) If f(n) ∈ Ω(g(n)), then either f(n) ∈ ω(g(n)) or f(n) ∈ Θ(g(n)).
3. (8%) If f(n) ∈ Ω(h(n)) and g(n) ∈ o(h(n)), then f(n)-g(n) ∈ Ω(h(n)).

**Problem 2.**
1. (5%) Solve T(n) = 4T(n/2) + n²ln{n}, T(1) = 1. You only need to obtain the asymptotic solution (in Θ() notation). If you use the master theorem, you must specify all parameters and briefly verify all conditions.
2. (10%) Let T(n) = 4T(⌊n/2⌋ + 1) + n, for all n ≥ 8. T(5) = T(6) = T(7) = 1. Prove that T(n) ∈ O(n²) using substitution method.

**Problem 3.** (15%) Given n distinct real numbers a_1, a_2, ..., a_n (not sorted), a_1 = 0 and a_2 = n. Your goal is to find a pair of numbers a_i and a_j such that |a_i - a_j| > 1, but there is no other a_k with value in between. Design an O(n)-time algorithm which finds one such pair. Briefly justify the correctness and the running time of the algorithm. (For example, if the input is 0, 4, 4.2, 1.3, the algorithm may output either (0,1.3) or (1.3,4)). You may assume that n is a power of 2.

**Problem 4.** (15%) Given k sorted arrays of n/k elements each. An algorithm A merges all k arrays into a single sorted array of n elements using only pairwise comparisons. Formally prove that the time complexity of algorithm A is Ω(n log k).

**Problem 5.** In this problem, Prof. Chen tries to maximize the number of meetings he can attend (meetings M_1, M_2, ..., M_n with start time s_i and end time t_i). Analyze one of the following greedy algorithms (choose one between 5-1 and 5-2):

1. (15%) Assume that the optimal solution chooses k meetings. Consider the greedy algorithm which always selects the meeting with the least number of conflicts. Prove that this algorithm always chooses at least ⌈k/2⌉ meetings or provide a counter example.
2. (10%) Assume that the optimal solution chooses k meetings. Consider the greedy algorithm which always selects the shortest meeting. Prove that this algorithm always chooses at least ⌈k/2⌉ meetings or provide a counter example.

**Problem 6.** Prof. Chen wants to maximize the total meeting time (instead of the number of meetings). Assume t_1 ≤ t_2 ≤ ... ≤ t_n.

1. (10%) Given an additional assumption that Prof. Chen must attend at least k meetings. Design an algorithm to find the optimal set of meetings (which maximizes the total meeting time). The running time must be polynomial in nk. Briefly justify correctness and analyze running time.
2. (10%) Given an additional assumption: For every i, M_i and M_{i+2} cannot both be attended, even if the meeting time does not conflict each other. Design an algorithm to find the maximum total meeting time (you do not need to find the optimal set of meetings). The running time must be polynomial in n. Briefly justify correctness and analyze running time.

---

## 考試 2: 109-1 陳和麟 演算法 期末考

- 學期: 109-1
- 教授: 陳和麟
- 考試類型: 期末考
- 考試日期: 110.1.11
- 考試時限: 180 分鐘
- 課程性質: 電機所選修
- 備註: Closed book，可帶一張雙面手寫A4筆記

### 試題

**Problem 1.** (15%) Given a connected undirected graph G. A bridge is an edge whose removal disconnects the graph.

1. (5%) Given a connected undirected graph G and an edge {u,v} in G, design an O(V+E)-time algorithm to determine whether {u,v} is a bridge.
2. (10%) Given a connected undirected graph G, design an O(V(V+E))-time algorithm to find all bridges. (hint: spanning trees of the graph must have exactly |V|-1 edges.)

**Problem 2.** (10%) There are n visitors v_1, v_2, ..., v_n and m hotels h_1, h_2, ..., h_m eligible for quarantine. Each visitor has exactly 3 hotels that he/she is willing to stay in. Given the capacity (maximum number of visitors allowed) of every hotel. Design a polynomial-time algorithm that assigns visitors to hotels or reports that no such assignment is possible. (Each visitor must be assigned to one of the 3 hotels that he/she is willing to stay in.) Briefly justify the correctness and analyze the running time.

**Problem 3.** (15%) Assume that hotels have no capacity limits. You must choose a set of hotels such that every visitor has a hotel that he/she is willing to stay in. The goal is to minimize the number of hotels chosen. Design a 3-approximation algorithm for this problem. Briefly justify the correctness and analyze the running time.

**Problem 4.** (15%) Given an undirected graph G in which all edge costs are distinct. Let C be any simple cycle in G. Prove the following statements or give counterexamples.

1. (8%) The most expensive edge in C does not belong to the minimum spanning tree.
2. (7%) The cheapest edge in C must belong to the minimum spanning tree.

**Problem 5.** (15%) Given an undirected graph G. Each edge has a (possibly negative) edge cost. The problem is to determine whether the graph G has a simple cycle of total cost 0.

(You must either: 1. design a polynomial-time algorithm, or 2. prove that the problem is NP-complete. Hint: One possible reduction is similar to the reduction from HAM. PATH to HAM. CYCLE described in class.)

**Problem 6.** (15%) Given a directed acyclic graph G. The problem is to determine whether the graph G has a Hamiltonian path.

(Same requirements as Problem 5.)

**Problem 7.** (15%) Given a graph G=(V,E). Each edge e has a length a_e ≥ 0 and a loading b_e ≥ 0. Given two nodes s and t in G. For any path P from s to t, define the length of the path to be the sum of lengths Σ_{e in P} a_e and the loading of the path to be the minimum loading min_{e in P} b_e. Design an O(E+V log V) algorithm to find a path from s to t, which minimizes (loading of the path × length of the path). Briefly justify the correctness and analyze the running time. (Partial credit: find the path which minimizes loading + length.)

---

## 考試 3: 103-1 蕭旭君 演算法設計與分析 期中考

- 學期: 103-1
- 教授: 蕭旭君
- 考試類型: 期中考
- 考試日期: 2014/11/14
- 考試時限: 180 分鐘
- 課程性質: 資訊系必修
- 備註: Closed book, 7 題共 100 分 + 30 分加分題，最高 100 分。空白答案可得該題 1/5 分數，完全錯誤得 0 分。

### 試題

**Problem 1: Short Answer Question (30 points)**

(a) (3 points) True or False: To prove the correctness of a greedy algorithm, we must prove that **every optimal solution contains our greedy choice**.

(b) (3 points) True or False: When items have **non-integer weights**, it may be extremely inefficient to solve the 0/1 Knapsack Problem using dynamic programming because of **lack of overlapping subproblems**.

(c) (3 points) True or False: (m_1,w_3),(m_2,w_2),(m_3,w_1) is one stable matching in the following preference lists:

| | 1st | 2nd | 3rd | | | 1st | 2nd | 3rd |
|---|---|---|---|---|---|---|---|---|
| m_1 | w_3 | w_2 | w_1 | | w_1 | m_1 | m_2 | m_3 |
| m_2 | w_2 | w_1 | w_3 | | w_2 | m_1 | m_2 | m_3 |
| m_3 | w_3 | w_2 | w_1 | | w_3 | m_2 | m_1 | m_3 |

(d) (3 points) True or False: If f(n) is O(g(n)), then 2^{f(n)} is O(2^{g(n)}).

(e) (3 points) Given the recurrence relation A(i,j) = F(A(i,j-1), A(i-1,j-1), A(i-1,j+1)), provide a valid traversal order to fill the DP table or justify why no valid traversal exists.

(f) (3 points) Given the recurrence relation A(i,j) = F(A(i-1,j-1), A(i+1,j+1)), provide a valid traversal order to fill the DP table or justify why no valid traversal exists.

(g) (3 points) Suppose you have designed a Divide and Conquer algorithm whose running time T(n) can be expressed by T(n) = aT(n/b)+f(n). Briefly explain what a, b, and f(n) represent in your algorithm.

(h) (3 points) Solve the following recurrence by giving a tight Θ-notation bound:
   T(n) = 2T(n/2) + n² log n

(i) (6 points) Describe a real-world problem that you have solved or have thought about solving using techniques learned in the class. Make an educated guess about how fast your algorithm might be, and how much time it would take to solve the same problem using a brute-force approach instead.

**Problem 2: nth Smallest in Two Databases (15 points)**

You're given two databases D_1 and D_2, each containing n numbers. These 2n numbers are all distinct. For each database, you can query for the kth smallest number for any 1 ≤ k ≤ n. You want to find the nth smallest number among these 2n numbers.

(a) (10 points) Please design a Divide-and-Conquer algorithm to find the nth smallest number among these 2n numbers in O(log n) queries.
   Hint: Let m = ⌊n/2⌋ and let v_{1,m} and v_{2,m} be the mth smallest number in database D_1 and D_2, respectively. Let x be the nth smallest number among these 2n numbers. Consider where x is in three cases: v_{1,m} > v_{2,m}, v_{1,m} = v_{2,m}, v_{1,m} < v_{2,m}.

(b) (5 points) Briefly justify the running time of your algorithm is indeed O(log n) queries.

**Problem 3: Longest Path (20 points)**

(a) (3 points) Briefly explain what optimal substructure is.

(b) (5 points) Consider a graph G = (V,E), a start node s ∈ V, end node t ∈ V, and weight w_e of each edge e ∈ E. The Longest Path Problem is to find a longest simple path going from s to t on this graph. Please construct a counterexample to show that the Longest Path Problem has no optimal substructure.

(c) Your friend made an interesting observation that the Longest Path Problem on certain types of graphs does exhibit optimal substructure. Consider a n-by-n grid-like directed graph with edges going downward and rightward only.

   1. (3 points) Find one longest path in the 4-by-4 grid graph in Figure 1 (with labeled edge weights).
   2. (6 points) Consider a n-by-n grid. Define your subproblems and represent the value of the optimal solution using a recurrence.
   3. (3 points) What's special about this type of graphs? Please explain why the Longest Path Problem has no optimal substructure in general but has optimal substructure in this special type of graphs.

   Figure 1 的 4x4 grid 邊權重:
   - 第一行橫向: 3, 4, 5
   - 第一列縱向: 8, 3, 7
   - 第二行橫向: 8, 7, 3
   - 第二列縱向: 5, 6, 5
   - 第三行橫向: 3, 9, 7
   - 第三列縱向: 5, 5, 3
   - 第四行橫向: 3, 1, 4
   - 第四列縱向: 8, 4, 1

**Problem 4: The Rise of the Planet of the Apes (15 points)**

Caesar is learning a sign language. The sign language should be prefix-free. Word frequencies:

| Word | food | sleep | play | drink | open | who | come |
|---|---|---|---|---|---|---|---|
| Frequency | 0.25 | 0.15 | 0.12 | 0.19 | 0.07 | 0.14 | 0.08 |

(a) (5 points) Caesar can do two gestures: UP and DOWN. Please create a prefix-free binary sign language to minimize the average number of gestures per word (Huffman coding).

(b) (5 points) Caesar now can do three gestures: UP, DOWN, and WAVE. Please create a prefix-free ternary sign language to minimize the average number of gestures per word.

(c) (5 points) Following (a), the UP gesture consumes three times the energy of the DOWN gesture. Will's greedy heuristic: first draw a binary prefix tree minimizing average gestures, then re-label edges so that the lighter-frequency subtree gets UP (costlier gesture). Show that this greedy algorithm is incorrect (provide a counterexample).

**Problem 5: Counting Inversions (10 points + 10 bonus points)**

(a) (10 points) Given a sequence of unique numbers B = b_1, b_2, ..., b_n, an inversion is a pair (b_i, b_j) such that i < j and b_i > b_j. Design an O(n log n) algorithm to count inversions.

(b) (10 bonus points) A significant inversion is a pair (b_i, b_j) such that i < j and b_i > 2b_j. Modify your algorithm from (a) to count significant inversions in O(n log n) time.

**Problem 6: Finding Closest Pair of Points (10 points + 10 bonus points)**

(a) (10 points) n points in 2D space. Distance defined as d(i,j) = min{|x_i - x_j|, |y_i - y_j|}. Given sorted arrays X_n and Y_n, design a greedy algorithm to find the closest pair in O(n) time.
   Hint: first consider a 1D case.

(b) (10 bonus points) Distance defined as d(i,j) = max{|x_i - x_j|, |y_i - y_j|}. Design an O(n log n) algorithm to find the closest pair.

**Problem 7: Fair Division of Christmas Gifts (10 bonus points)**

Divide n gifts into two groups such that the weight difference is minimized. Each gift has a positive integer weight. Design an algorithm in O(nS) time where S is the total weight. Find the minimal weight difference and the groupings.
   Hint: Convert into making one set as close to S/2 as possible.

**附錄: Master Theorem**
T(n) = aT(n/b) + f(n)
1. If f(n) = O(n^{log_b a - ε}), then T(n) = Θ(n^{log_b a}).
2. If f(n) = Θ(n^{log_b a}), then T(n) = Θ(n^{log_b a} log n).
3. If f(n) = Ω(n^{log_b a + ε}) and af(n/b) ≤ cf(n), then T(n) = Θ(f(n)).

---

## 考試 4: 103下 林軒田 資料結構與演算法 期中考+解答

- 學期: 103 下
- 教授: 林軒田
- 考試類型: 期中考（含解答）
- 考試日期: 2015.04.21
- 考試時限: 120 分鐘
- 課程性質: 資工系必修
- 備註: Open-book exam，可使用任何紙本資料。共 5 大題，每題 40 分，滿分 200 分。9 個子題，3 題 * (簡單)，4 題 ** (一般)，2 題 *** (困難)。

### 試題

**1. C and C++**

(a) (20%, *) Give a concrete example in C/C++ to explain in your own words how memory leak could happen.

(b) (20%, *) Suppose we use the following class to represent homework scores:
```cpp
class myScore {
public:
    myScore(int n = 10){ size = n; hwScore = new int[size]; }
    ~myScore(){ delete[] hwScore; }
    string name;
    int *hwScore;
};
```
Draw the memory layout after running:
```cpp
myScore a(6);
a.name = "John"; a.hwScore[0] = 85; a.hwScore[1] = 90;
myScore b = a;
b.name = "Mary"; b.hwScore[0] = 70;
```
Explain potential hazards/problems.

**2. Arrays and Linked Lists**

(a) (20%, **) Given a vector of N integers between 1 and M, write pseudo code of an O(N)-time O(M)-space algorithm to determine whether all integers are distinct.

(b) (20%, *) Given a singly linked list:
```cpp
class node {
public:
    string data;
    node *next;
};
```
Write a C/C++ function invert(node *head) that inverts the list without dynamic memory allocation.

**3. Stacks and Queues**

(a) (20%, **) Show how a stack evaluates the postfix expression step by step:
   `9 8 7 2 3 * - / - 5 2 - * 3 /`
Draw the stack status after each step.

(b) (20%, **) Given a deque D storing N elements (d_0, d_1, ..., d_{N-1}) and an initially empty queue Q, give pseudo-code to reverse the elements in D using only D and Q.

**4. The Evil Complexity**

Definition: f(n) = O(g(n)) iff ∃ n_0 ≥ 1 and c > 0 such that ∀ n ≥ n_0, f(n) ≤ c·g(n). Functions are from N to R⁺ ∪ {0}.

(a) (20%, **) Prove or disprove: If f(n) = O(g(n)), then (f(n))² = O((g(n))²).

(b) (20%, ***) Prove or disprove: If |f(n) - g(n)| = O(1), then 2^{f(n)} = O(2^{g(n)}).

**5. (40%, ***) Binary Search**

Given a sorted vector a with N distinct integers where a[0] < a[1] < ... < a[N-1], defining N+1 non-overlapping ranges (-∞, a[0]], (a[0], a[1]], ..., (a[N-1], ∞). Given a value x (different from all elements in a), write pseudo code of a O(log N)-time algorithm to determine which range x falls in.

---

## 考試 5: 101上 蔡欣穆 演算法設計與分析 期末考

- 學期: 101 上
- 教授: 蔡欣穆
- 考試類型: 期末考
- 考試日期: 102/1/10 (2013年1月10日)
- 考試時限: 180 分鐘
- 總分: 130 分
- 課程性質: 資訊工程學系必修

### 試題

**Problem 1.** True or False (每題 1 分判斷 + 3 分解釋，共 16 分)

1. If NPC = P, then P = NP.
2. If L_1, L_2 ⊂ {0,1}* are languages such that L_1 ≤_p L_2. If L_1 ∈ NPC, then L_2 ∈ NPC.
3. The complexity class NP represents the problems which cannot be decided within polynomial time.
4. When performing an amortized analysis, we usually require the total amortized cost to be a lower bound of the total actual cost.

**Problem 2.** Short answer questions (38 points)

1. (8 points) Please derive the work T_1(A∪B∪C∪D) and the span T_∞(A∪B∪C∪D) of the multithread algorithm shown in Figure 1 in terms of T_1(s) and T_∞(s), s = {A,B,C,D}.
   (Figure 1: Block diagram with A→B, A→C, A→D, B→C, C→D 的多執行緒演算法)

2. (4 points) When the estimated completion time for the software product does not meet the original planned product ship date, why is it not a good idea to hire more software engineers to complete the job? What should be done instead to solve this problem?

3. (6 points) Suppose for each software engineer in your company, you have collected a historic list of ratios of the estimated time to complete a programming task and the actual time to complete it. Explain briefly how to use evidence-based scheduling to utilize the lists to estimate the time to complete a future task.

4. (4 points) In the form of pseudo code, give an example of an algorithm that will result in race condition(s). (不可使用課堂上的 RACE-EXAMPLE)

5. (8 points) Dynamic tables: contract a table by multiplying its size by 2/3 when α drops below 1/3. Use potential function Φ(T) = |2T.num - T.size| to show amortized cost of table delete is bounded above by a constant. (8 points)

**Problem 3.** P-Square-Matrix-Multiply (24 points)

Given:
```
P-Square-Matrix-Multiply(a,b)
    n = a.rows
    let c be a new n x n matrix
    parallel for i = 1 to n
        parallel for j = 1 to n
            c[i][j] = 0
            for k = 1 to n
                c[i][j] = c[i][j] + a[i][k]*b[k][j]
    return c
```

1. (6 points) Draw the computation dag for 2x2 matrices. Label vertices corresponding to strands. Spawn/call edges point downward, continuation edges point right, return edges point upward.
2. (6 points) Analyze the work, span, and parallelism.
3. (8 points) Modify to have a span of O(log n). (Cannot just use "parallel for k=1 to n" since iterations share c[i][j]. Use spawn and sync, define a new function for recursive calls.)
4. (4 points) Show your modified algorithm has span O(log n).

**Problem 4.** Machine Task Scheduling (26 points)

One machine, n tasks a_1, ..., a_n. Machine accessible between time 0 and D. Task a_j requires t_j time units, yields profit p_j, ready at time s_j. Machine processes one task at a time without interruption. Maximize total profit.

1. (2 points) State this problem as a decision problem.
2. (8 points) Show the decision problem is NP-complete. (Reduce from 0-1 knapsack.)
3. (8 points) Assuming processing times and ready times are integers from 1 to n, show optimal substructure (define subproblem).
4. (8 points) Give a polynomial-time dynamic programming algorithm (assuming integer times from 1 to n).

**Problem 5.** α-balanced Binary Search Tree (28 points)

A node x is α-balanced if x.left.size ≤ α · x.size and x.right.size ≤ α · x.size. Define Δ(x) = |x.left.size - x.right.size| and Φ(T) = c Σ_{x∈T: Δ(x)≥2} Δ(x).

1. (6 points) Show how to rebuild a subtree rooted at x to become (1/2)-balanced in O(x.size) time and space.
2. (4 points) Show that searching in an n-node α-balanced BST takes O(log n) worst-case time.
3. (4 points) Argue any BST has nonnegative potential and a (1/2)-balanced tree has potential 0.
4. (8 points) Suppose m units of potential can pay for rebuilding an m-node subtree. How large must c be in terms of α for O(1) amortized rebuilding time?
5. (6 points) Show inserting/deleting in an n-node α-balanced tree costs O(log n) amortized time.

**Problem 6.** (6 points) What would you do, if you were the instructor of the ADA course, to improve the atmosphere in the classroom?

---

## 考試 6: 99下 蔡益坤 演算法 期末考

- 學期: 99 下
- 教授: 蔡益坤
- 考試類型: 期末考
- 考試日期: 2011/06/20
- 考試時限: 180 分鐘
- 課程性質: 資訊管理學系必修
- 備註: Closed-book exam，每題 10 分

### 試題

**Problem 1.** For each of the following pairs of functions, determine whether f(n) = O(g(n)) and/or f(n) = Ω(g(n)). Justify your answers.

|  | f(n) | g(n) |
|---|---|---|
| (a) | (log n)^{log n} | n / (log n) |
| (b) | n³ × 2^n | 3^n |

**Problem 2.** Consider rearranging the following array into a max heap using the bottom-up approach.

```
Index:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
Value:  2   8   3   5   1  14   6   7  11   4  10  12  13  15   9
```

Please show the result after a new element is added to the current collection of heaps (at the bottom) until the entire array has become a heap.

**Problem 3.** Prove that the sum of the heights of all nodes in a complete binary tree with n nodes is at most n-1. You may assume it is known that the sum of the heights of all nodes in a full binary tree of height h is 2^{h+1} - h - 2. (Note: a single-node tree has height 0.)

**Problem 4.** Compute the next table as in the KMP algorithm for string B[1..11] = abaabababaa. Please show how next[7] and next[11] are computed from using preceding entries in the table.

**Problem 5.** Given a connected undirected graph G, a spanning tree T of G, and a vertex v, design an algorithm to determine whether T is a valid DFS tree of G rooted at v. Present your algorithm in pseudo code. Explain why the algorithm is correct and analyze its time complexity.

**Problem 6.** What is wrong with the following algorithm for computing the minimum-cost spanning tree?

"If the input is just a single-node graph, return the single node. Otherwise, divide the graph into two subgraphs, recursively compute their minimum-cost spanning trees, and then connect the two spanning trees with an edge between the two subgraphs that has the minimum weight."

**Problem 7.** Let G = (V,E) be a connected weighted undirected graph and T be a minimum-cost spanning tree (MCST) of G. Suppose that the cost of one edge {u,v} in G is increased; {u,v} may or may not belong to T. Design an algorithm either to find a new MCST or to determine that T is still an MCST. Explain correctness and analyze time complexity.

**Problem 8.** Let G = (V,E) be a directed graph, and let T be a DFS tree of G. Prove that the intersection of the edges of T with the edges of any strongly connected component of G form a subtree (rather than two or more separate subtrees) of T.

**Problem 9.** Single-source shortest path using dynamic programming:

D^L(u) = min{ D^{L-1}(u), min_{(u',u)∈E} {D^{L-1}(u') + length(u',u)} }, 2 ≤ L ≤ n-1

Please explain why the solution allows edges with a negative weight (as long as there is no cycle with a negative weight). How is this different from Dijkstra's algorithm?

**Problem 10.** The subgraph isomorphism problem: Given two graphs G1 = (V1,E1) and G2 = (V2,E2), does G1 have a subgraph isomorphic to G2? Prove that the subgraph isomorphism problem is NP-complete.
   Hint: reduce from Hamiltonian Cycle problem, setting G1 = G and G2 = a ring of |V1| nodes.

**附錄:**
The Hamiltonian cycle problem: given an undirected graph G, does G have a Hamiltonian cycle? (NP-complete)

---

## 考試 7: 107-1 陳健輝 演算法設計方法論 期末考

- 狀態: **該文章已被刪除 (PTT 返回 404)**
- 原始連結: https://www.ptt.cc/bbs/NTU-Exam/M.1547467773.A.B4E.html

---

## 考試 8: 105上 蕭旭君 演算法設計與分析 期末考

- 學期: 104上 (105上依原始標題)
- 教授: 蕭旭君
- 考試類型: 期末考
- 考試日期: 2016.01.12
- 考試時限: 180 分鐘
- 課程性質: 資工系必修
- 備註: Closed book, 6 題共 100 分 + 35 分加分題，最高 100 分

### 試題

**Problem 1: Short Answer Questions (25 points)**

(a) (3 points) True or False: If P ≠ NP, then there is no polynomial-time algorithm to solve any NP-complete problem.

(b) (3 points) True or False: If A can be reduced to B in O(n²) time and there is an O(n³) algorithm for B, then there is an O(n³) algorithm for A.

(c) (3 points) True or False: Every computational problem is decidable.

(d) (3 points) True or False: It is more efficient to represent a sparse graph using an adjacency matrix than using adjacency lists.

(e) (3 points) True or False: If the amortized cost for every operation on a data structure is O(1), the running time for performing a sequence of n operations is O(n) in the worst case. (Assuming the data structure is empty at the beginning.)

(f) (3 points) True or False: If there is a randomized algorithm that solves a decision problem in time t and outputs the correct answer with probability 0.5, then there is a randomized algorithm for the problem that runs in time Θ(t) and outputs the correct answer with probability at least 0.99.

(g) (3 points) Provide a counterexample to show that the following divide-and-conquer algorithm may not correctly find a MST:
   - Divide: Given a graph G, partition G into two parts by using a cut.
   - Conquer: Find a MST for each part.
   - Combine: Combine the two MSTs using the minimum edge of the cut.

(h) (4 points) Please write down up to three of your peers who help you most for the ADA class. Anything else you would like to say to your instructor or suggestions?

**Problem 2: Basic Graph Problems (25 points)**

(a) (5 points) Given pre-order traversal {A, B, D, E, F, C} and post-order traversal {D, F, E, B, C, A}, reconstruct a legal binary tree.

(b) (5 points) Given BFS traversal {A, B, C, E, D, F} and DFS traversal {A, B, C, F, D, E}, reconstruct a legal undirected connected graph.

(c) (5 points) Consider the graph in Figure 1 (with negative edges). What is the shortest path distance from s to t computed by Dijkstra's algorithm? What is the actual shortest path distance from s to t?

   Graph 結構:
   - s→b: -1 (雙向), s→a: 10
   - b→d: 5 (雙向), b→c: 3 (向上)
   - d→f: 6 (雙向), d←b: 6 (斜向)
   - f→t: 2, f→b: -5
   - e→c: 3, e→f: 3, e↔t: 4
   - a→c: 8, c→t: 1

(d) (10 points) Given the path relaxation property, explain why Bellman-Ford algorithm correctly computes shortest path distance when there is no negative cycle.

**Problem 3: Approximation Algorithms (20 points)**

(a) (10 points) The MAX-k-CNF-SAT problem aims to maximize satisfied clauses. Design a randomized (2^k/(2^k - 1))-approximation algorithm for k-CNF-SAT (k > 3). Your algorithm should run in polynomial time. Assume no clause contains both a variable and its negation.

(b) (10 points) Ada claims she can design a (2^k/(2^k - 1))-approximation algorithm for MAX-3-CNF-SAT by first converting 3-CNF to k-CNF then solving MAX-k-CNF-SAT. Do you agree? Justify.

**Problem 4: Independent Set (20 points)**

An independent set of G = (V,E) is V' ⊆ V such that no two vertices in V' are joined by an edge. IND-SET: given G and k, determine whether there is an independent set of size k.

Reduction from 3-CNF-SAT to IND-SET:
1. For each clause C_r = (l^r_1 ∨ l^r_2 ∨ l^r_3), introduce triple of vertices (v^r_1, v^r_2, v^r_3).
2. Build edges between vertices in same triple (r = s) and between vertices in different triples whose literals are negations of each other.

(a) (10 points) Given ψ = (x1 ∨ ¬x2 ∨ ¬x3) ∧ (¬x1 ∨ x2 ∨ x3) ∧ (x1 ∨ x2 ∨ x3), draw the IND-SET instance.

(b) (10 points) Justify correctness: ψ is satisfiable iff G has an independent set of size k.

**Problem 5: Election Day (10 points + 15 bonus points)**

(a) (10 points) Binary Counter displaying vote count. If it costs 2^d to flip the d-th bit, justify amortized cost per increment is O(log n) and total amortized cost is O(n log n) for n votes.

(b) (5 bonus) Ada uses Bloom filter to check citizen IDs. Give one advantage and one disadvantage.

(c) (5 bonus) Ada publishes H(winner, r) before election and reveals winner and r after. Explain why Ada cannot cheat.

(d) (5 bonus) The election uses plurality rule. Construct an example demonstrating plurality is not strategyproof with more than two candidates.

**Problem 6: More Independent Set (20 bonus points)**

Maximum weighted independent set on a line graph G with n vertices V = {v_0, v_1, ..., v_n} and edges E = {(v_0,v_1), (v_1,v_2), ..., (v_{n-1},v_n)}, weight w_i for v_i.

(a) (5 points) Provide a counterexample showing the heaviest-first greedy algorithm fails:
```
Algorithm 1: The heaviest-first greedy algorithm
1: V' ← ∅, S ← V
2: while S ≠ ∅ do
3:   Pick v_i of maximum weight in S
4:   Add v_i to V'
5:   Remove v_i and its neighbors from S
6: end while
7: Return V'
```

(b) (15 points) Design a polynomial-time algorithm to find maximum weighted independent set. (O(n²) for at most 10 points, O(n) for 15 points.)

**附錄:**
- Dijkstra's algorithm pseudo code
- Bellman-Ford algorithm pseudo code

---

## 考試 9: 104上 蕭旭君 演算法設計與分析 期末考

- 狀態: **該文章已被刪除 (PTT 返回 404)**
- 原始連結: https://www.ptt.cc/bbs/NTU-Exam/M.1453876482.A.1BC.html

---

## 考試 10: 103-1 蔡欣穆 演算法設計與分析 期末考

- 學期: 103-1
- 教授: 蔡欣穆
- 考試類型: 期末考
- 考試日期: 2015/01/15
- 考試時限: 180 分鐘
- 總分: 132 分
- 課程性質: 資工系大二必修

### 試題

**Problem 1.** True or False (每題 1 分判斷 + 3 分解釋，共 40 分)

1. If L ∈ NPC and L ∈ P, then P = NP.
2. If L ∈ NP then L̄ ∈ NP.
3. If L̄ ∈ P then L ∈ P.
4. If P = NP then NP = co-NP.
5. NPC ⊆ NP.
6. NP ⊇ P.

(以下 4 題請參考 DFS(G) 和 DFS-VISIT(G,v) 虛擬碼)

7. There is no back edge in terms of the depth-first forest produced by a DFS on an undirected graph.
8. There is no cross edge in terms of the depth-first forest produced by a DFS on an undirected graph.
9. There is no back edge in terms of the depth-first forest produced by a DFS on a directed acyclic graph.
10. In DFS, when we visit an edge e = (u,v), if v's color is BLACK and u.d < v.d, then e is a cross edge.

DFS(G):
```
1  for each vertex u ∈ G.V
2      u.color = WHITE
3      u.π = NIL
4  time = 0
5  for each vertex u ∈ G.V
6      if u.color == WHITE
7          DFS-VISIT(G,u)
```

DFS-VISIT(G,u):
```
1  time = time + 1
2  u.d = time
3  u.color = GRAY
4  for each v ∈ G.Adj[u]
5      if v.color == WHITE
6          v.π = u
7          DFS-VISIT(G,v)
8  u.color = BLACK
9  time = time + 1
10 u.f = time
```

**Problem 2.** (6 points) Briefly explain in evidence-based scheduling how you can "simulate the future" -- use the past history to estimate the time required to complete a task.

**Problem 3.** Minimum Cost Spanning Tree (24 points)

1. (4 points) Write pseudo code of Kruskal's algorithm.
2. (4 points) Show Kruskal's runs in O(|E| log |E|). (Given: m operations of MAKE-SET, FIND-SET, UNION take O(mα(n)) time.)
3. (4 points) If all edge weights are integers in range 1 to |V|, give a modified Kruskal's that runs in O(|E|α|V|).
4. (4 points) Write pseudo code of Prim's algorithm.
5. (4 points) Show Prim's runs in O(|E| log |V|).
6. (4 points) If all edge weights are integers in range 1 to some constant W, give a modified Prim's that runs in O(|E|).

**Problem 4.** Dynamic Table (16 points)

TABLE-INSERT: if full, double table size and move all data.
TABLE-DELETE: if less than 25% full, halve table size and move all data.

Using potential function:
```
            ⎧ 2 × T.num - T.size     if T.num/T.size ≥ 1/2
Φ(T) =     ⎨
            ⎩ T.size/2 - T.num       if T.num/T.size < 1/2
```

Show that amortized cost of both operations is bounded above by a constant. Discuss cases with and without table expansion/contraction.

**Problem 5.** Shortest Path (16 points)

Refer to a directed graph G (Figure 2 -- http://imgur.com/i47tCKL).

1. (6 points) Use Dijkstra Algorithm to determine shortest path costs from vertex 1 to all other vertices. Fill in Table 1 showing each iteration.
2. (6 points) Use Bellman-Ford Algorithm to determine shortest path costs from vertex 1 to all other vertices. Fill in Table 2 showing each iteration.
3. (4 points) Explain why Dijkstra Algorithm cannot handle edges with negative weights.

**Problem 6.** NODE-COVER NP-completeness (20 points)

Given graph G = (V,E), N ⊆ V is a node cover if every edge in E has at least one end in N. NODE-COVER: given G and budget k, does G have a node cover of k or fewer nodes?

1. (4 points) Show NODE-COVER ∈ NP.
2. Reduction from 3-CNF-SAT to NODE-COVER:
   (a) For each clause (x∨y∨z), construct a "column" of three nodes, all connected by vertical edges. Add horizontal edges between nodes representing a variable and its negation.
   (b) Budget k = twice the number of clauses.

   Example: (x∨y∨z)∧(¬x∨¬y∨¬z)∧(x∨¬y∨z)∧(¬x∨y∨¬z) is reduced to G (Figure 1 -- http://imgur.com/dXvJvUF) with k = 8.

   (12 points) Show x ∈ 3-CNF-SAT iff f(x) ∈ NODE-COVER.
   (4 points) Explain why the reduction runs in polynomial time.

**Problem 7.** (10 points) Out of all the lectures this semester, which one do you enjoy the most and which one do you want to skip the most? Why? And give constructive suggestions to the style and content of the homework assignments.
