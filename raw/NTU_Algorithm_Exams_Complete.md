# NTU 演算法考古題完整彙整

---

## 考試 1：100上 蔡欣穆 演算法設計與分析 期中考

- 學期：100上 (Fall 2011)
- 教授：蔡欣穆
- 考試類型：期中考
- 日期：2011/11/18
- 時限：180 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1321630989.A.A2C.html

### 試題

**Problem 1.** In each of the following question, please specify if the statement is true or false. If the statement is true, explain why it is true. If it is false, explain what the correct answer is and why. (20 points. For each question, 1 point for true/false answer and 3 points for the explanations.)

1. The person who should close the bug report is the one who fixes the bug.
2. nlogn is polynomially larger than n.
3. nlogn is polynomially smaller than n^1.001.
4. Master theorem sometimes cannot be applied even if the recurrence is in the form of T(n)=aT(n/b)+f(n).
5. In all cases, using a top-down approach when using dynamic programming to solve a problem is slower than using a bottom-up approach since former would usually involve the overhead of recursively calls (setting up stack and local variables).

**Problem 2.** "Short answer" questions: (32 points)

1. Describe two benefits of using paper prototype instead of the regular software prototype. (4 points)
2. What are the 3 things required in every bug report? (6 points)
3. Explain why a binary tree cannot correspond to an optimal prefix code if it is not full (no internal node has only one children). (4 points)
4. Show how you would use an adjacency matrix to represent directed graph G in Figure 1. (3 points)
5. Show how you would use an adjacency list to represent directed graph G in Figure 1. (3 points)
6. Draw a breadth-first tree of directed graph G in Figure 1. Assume that we start the breadth-first search on vertex 2. (4 points)
7. Draw a depth-first tree of directed graph G in Figure 1. Assume that we start the depth-first search on vertex 2. (4 points)
8. Following the previous question, after the depth-first search you performed on G, mark the type of each edge in the original graph G. The types of the edges include tree edges, forward edges, back edges, cross edges. (4 points)

Figure 1 為一有向圖，節點 1-8，邊如下：
```
                       -->
               1<---2<--3
              ^ <\  />\< /
              |   4     5
              |/>\     \<\
               6 <- 7<---8
```

**Problem 3.** Determine the cost and the structure of an optimal binary search tree for a set of n=7 distinct keys with the probabilities in Table 1.

Table 1:
| i  | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    |
|----|------|------|------|------|------|------|------|------|
| pi |      | 0.04 | 0.06 | 0.08 | 0.02 | 0.10 | 0.12 | 0.14 |
| qi | 0.06 | 0.06 | 0.06 | 0.06 | 0.05 | 0.05 | 0.05 | 0.05 |

(10 points)

**Problem 4.** Use a recursion tree to determine a good asymptotic upper bound on the recurrence T(n) = T(n/2) + n^2. Use the substitution method to verify your answer. (10 points, 5 points for the recursion tree and 5 points for substitution method)

**Problem 5.** Given an unweighted directed graph G=(V,E), we need to find the shortest path from u to v, where u,v in V. Show that the problem of finding the shortest path from u to v exhibits the optimal substructure property. (Hint: prove that the shortest path between u and v contains the shortest paths from u to another vertex w and from w to v) (5 points)

**Problem 6.** Suppose you are given an array A[1...n] of sorted integers that has been circularly shifted k positions to the right. For example, [35,42,5,15,27,29] is a sorted array that has been circularly shifted k=2 positions, while [27,29,35,42,5,15] has been shifted k=4 positions. We can obviously find the largest element in A in O(n) time. Describe an O(logn) algorithm based on the divide-and-conquer strategy to find the largest element in A. (You need to show that your algorithm's time complexity is O(logn)) (10 points)

**Problem 7.** There is a river which flows horizontally through a country. There are N cities on the north side of the river are n1, n2..., nN, and the X coordinates of the N cities on the south side of the river are s1, s2,...sN. Assume that we can only build bridges between cities with the same number; that is, we can only build bridges between cities with coordinates ni and si, where 1 <= i <= N. In this problem, we ask you to determine the maximum number of bridges we can build without any bridges crossing with each other. Note that n1 through nN and s1 through sN are both not sorted.

1. Describe your definition of a subproblem. Use that definition, prove that this problem exhibits optimal substructure. (5 points)
2. Describe a dynamic-programming algorithm to solve the problem. (10 points)
3. What is the time complexity of your algorithm? (3 points)

**Problem 8.** Modern computers use a cache to store a small amount of data in a fast memory. Even though a program may access large amounts of data, by storing a small subset of the main memory in the cache - a small but fast memory - overall access time can greatly decrease. When a computer program executes, it makes a sequence <r1,r2,...,rn> of n memory requests, where each request is for a particular data element. [...] We can solve this off-line problem by a greedy strategy called furthest-in-future, which chooses to evict the item in the cache whose next access in the request sequence comes furthest in the future.

1. Write pseudocode for a cache management that uses the furthest-in-future strategy. The input should be a sequence <r1,r2,...,rn> of requests and a cache size k, and the output should be a sequence of decisions about which data element (if any) to evict upon each request. What is the running time of your algorithm? (10 points)
2. Show that the off-line caching problem exhibits optimal substructure. (5 points)
3. Prove that furthest-in-future produces the minimum possible number of cache misses (prove that this greedy choice is correct). (5 points)

**Problem 9.** Please write down 3 things you like about this course and 3 things that you would like to see some changes (and your suggestion about how we should change them). (10 points)

---

## 考試 2：100上 蔡欣穆 演算法設計與分析 期末考

- 學期：100上 (Fall 2011)
- 教授：蔡欣穆
- 考試類型：期末考
- 日期：2012/1/13
- 時限：180 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1326554879.A.6E0.html

### 試題

**Problem 1.** In each of the following question, please specify if the statement is true or false. If the statement is true, explain why it is true. If it is false, explain what the correct answer is and why. (8 points. 1 point for true/false and 3 points for the explanation for each question)

1. The complexity class NP represents the problems which cannot be solved in polynomial time.
2. When the parallelism of a multi-thread algorithm, rho = Omega(n), adding more processors to the system which runs the algorithm would always make the algorithm run faster.

**Problem 2.** "Short answer" questions: (36 points)

1. Why is it hard to discover bugs caused by race conditions? (4 points)
2. Fill in blanks (a) through (d) in Figure 1 using T1(A), T1(B), T_inf(A), and T_inf(B). (8 points)
   - 串聯 (serial): Work: T1(A U B) = (a), Span: T_inf(A U B) = (b)
   - 並聯 (parallel): Work: T1(A U B) = (c), Span: T_inf(A U B) = (d)
3. What are the two conditions that a language L subset {0,1}* is NP-complete? (4 points)
4. Explain why Dijkstra's algorithm does not work when the edges in the graph can be negative. (4 points)
5. Explain when using Evidence-Based Scheduling, how we predict the time to complete a task. (4 points)
6. List two advantages of writing the functional specification before start implementing the software. (4 points)
7. Let T_inf, Tp, T1 be the running time of multi-threaded algorithm A when having inf, P, 1 processors in the system, respectively. Write down the formulas for (1) the work law; and (2) the span law; using these 3 variables. (8 points)

**Problem 3.** Please answer the following questions about circuit satisfiability and formula satisfiability problems: (22 points)

1. Use the reduction algorithm we talked about in the lecture to reduce the circuit in Figure 2 to a general boolean formula. (4 points)
2. Use the reduction algorithm we talked about in the lecture to reduce a general boolean formula (~X1 ^ X2) V X3 to the 3-CNF form. (8 points)
3. 2-CNF-SAT: Let 2-CNF-SAT be the set of satisfiable boolean formulas in CNF with exactly 2 literals per clause. Show that 2-CNF-SAT is in P. Make your algorithm as efficient as possible. (Hint: Observe that x V y is equivalent to ~x -> y. Reduce 2-CNF-SAT to an efficiently solvable problem on a directed graph.) (10 points)

**Problem 4.** Consider an ordinary binary min-heap data structure with n elements supporting the instructions INSERT and EXTRACT-MIN in O(log n) worst-case time. Give a potential function Phi such that the amortized cost of INSERT is O(log n) and the amortized cost of EXTRACT-MIN is O(1), and show that it works. (20 points)

1. Define your potential function Phi. Prove that it always satisfies Phi(Di) >= Phi(D0), for all i, where Di is the data structure after performing the i-th operation. (4 points)
2. Show that the amortized cost of INSERT is O(log n). (8 points)
3. Show that the amortized cost of EXTRACT-MIN is O(1). (8 points)

**Problem 5.** Answer the following questions about the complexity class co-NP. (12 points)

1. Use the language HAM-CYCLE = {<G>: G is a hamiltonian graph} as an example to explain what co-NP means; on what condition HAM-CYCLE in NP? (4 points)
2. Prove that P subset co-NP. (8 points)

**Problem 6.** Answer the following questions about graph. (20 points)

1. Use Prim's algorithm to obtain the minimum spanning tree of the graph in Figure 3. Please mark the order of adding the edge to the spanning tree on the figure. (4 points)
2. Please use the Bellman-Ford algorithm to determine the costs of the shortest paths from vertex 1 to all other vertices in the graph in Figure 3. Use table 1 to show how the algorithm is executed in each iterations. (8 points)
3. Please use the Dijkstra's algorithm to determine the costs of the shortest path from vertex 1 to all other vertices in the graph in Figure 3. Use Table 2 to show how the algorithm is executed in each iteration. (8 points)

Figure 3 為一圖，節點 1-7，邊權重如下：
- 1-5: 2, 1-6: 20, 1-7: 9
- 5-2: 4, 2-7: 9, 7-4: 1
- 4-2: 3, 7-2: 5, 2-3: 3
- 6-3: 2, 6-7: 10, 4-3: 5

**Problem 7.** Out of all topics we covered in the classes this semester, which one do you like the most? Which one do you dislike the most? Why? Please give some constructive suggestions. (2 points)

---

## 考試 3：100上 蘇雅韻 演算法設計與分析 期末考

- 學期：100上 (Fall 2011)
- 教授：蘇雅韻
- 考試類型：期末考
- 日期：2012/1/13
- 時限：170 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1327853701.A.932.html

### 試題

**Problem 1. Minimum spanning tree** [20 points, 3 points each for (a)-(c), 11 points for (d) and (e)]

For parts (a), (b), and (c), consider a weighted graph with 9 vertices (A-I) and 14 edges with distinct integer weights between 1 and 14.

(a) Complete the sequences of edges added to a MST in the order that Kruskal's algorithm includes them.

(b) Suppose edge (E, F) of weight w is added to the graph. How would you assign the value of w so that edge (E, F) is included in a MST?

(c) Complete the sequences of edges to a MST in the order that Prim's algorithm includes them. Start Prim's algorithm from vertex A.

(d) Suppose you know the MST of a weighted graph G. Now, a new edge (u, v) of weight w is inserted into G to form a weighted graph G'. Design an O(V) time algorithm to determine if the MST in G is also an MST in G'. You may assume all edge weights are distinct.

(e) Explain briefly why your algorithm takes O(V) time.

**Problem 2. Short answer questions** [8 points, 4 points each]

1. Circle the choice that describes a use of the following code:
```
for i = 1 to |G.V|-1
  for u = 1 to |G.V|-1
    for v in G.adj(u)
      if v.d > u.d + w(u,v)
        v.d = u.d + w(u,v)
```
(a) To find the longest path in a weighted graph
(b) To compute the MST of a weighted graph
(c) To topologically sort a digraph
(d) To find shortest path in a weighted graph
(e) To implement DFS in a weighted graph

2. Given the weighted graph and the initial distance matrix below, what is the value d_35 in matrix D^(2)?
(a) 5   (b) 11   (c) inf   (d) 3   (e) None of the above

**Problem 3. True or False and Justify.** [12 points, 3 points each]

1. T F  Dijkstra's algorithm can be implemented with binary-heap or Fibonacci-heap. Given a sparse graph where |E| = Theta(|V|), the Fibonacci-heap implementation is asymptotically faster than the binary-heap implementation.

2. T F  Let G = (V,E) be a weighted graph and let T be a minimum spanning tree of G. Then, for any pair of vertices s and t, the path in T must be a shortest path in G.

3. T F  Given a graph G = (V,E) with distinct weight on edges and a subset of vertices S <= V. Let edge (u, v) be the minimum cost edge between any vertex in S and any vertex in V-S. Then, the minimum spanning tree of G must include the edge (u, v).

4. T F  Let G = (V,E) be a directed graph with negative-weight edges, but no negative-weight cycles. Then, one can compute all shortest paths from a source vertex s in V to all vertices v in V faster than Bellman-Ford using the technique of reweighting.

**Problem 4. Maximum-flow** [20 points]

1. (10 points) The figure describes a flow assignment in a flow network. (1) Briefly state the Max-flow min-cut theorem. (2) Draw the minimum cut in the figure. (3) Explain whether the flow assignment in the figure is maximum flow using the Max-flow min-cut theorem.

2. (10 points) Suppose you have an algorithm A to solve the maximum flow problem. Given N persons, the capacity of M places, and an N*M matrix K (K_ij = 1 if person P_i is willing to go to place j), please (1) give an algorithm that can determine the maximum number of people that can go outside and (2) explain why your algorithm is correct.

**Problem 5. Shortest paths** [15 points]

1. Given a DAG, please describe how to use topological sort to find shortest paths. (6 points)
2. We know that topological sort may output results of more than one kind of ordering. Please explain why this does not affect the results of finding shortest paths? (9 points)

**Problem 6.** [10 points]

An edge disjoint path is that any two paths with no sharing edges. Given a directed graph, a source s and destination t, please (1) find k edge disjoint paths from s to t, and (2) briefly explain why your algorithm is correct.

**Problem 7. NP-completeness** [20 points, 4, 6, and 10 points for 1, 2, and 3 respectively]

1. A problem A has a polynomial reduction to a problem B, and B has a polynomial reduction to a problem C. Suppose B is in NP-complete.
   (1) What can you say about A? (a) Nothing (b) It's in P (c) It's in NP (d) It's NP-complete (e) It's NP-hard
   (2) What can you say about C? (a) Nothing (b) It's in P (c) It's in NP (d) It's NP-complete (e) It's NP-hard

2. SAT is the decision problem that takes as input a Boolean formula and returns YES if the formula can be satisfied, NO if it cannot.
   (1) What can you say about SAT?
   (2) Assume P = NP, What can you say about SAT?
   (3) Assume P != NP, What can you say about SAT?

3. Assume there is an algorithm SOLVE_SAT to solve SAT that takes time T(n) where n is the number of variables. Write in pseudocode an algorithm that utilizes SOLVE_SAT to return an assignment of the formula (when it exists) that takes time O(nT(n)).

**Problem 8. Feedback** [10 points]

Please tell us what you think about this class! Please write down (1) things you like about this class and (2) things you would like to see we do that can help you learn better.

---

## 考試 4：100上 蘇雅韻 演算法設計與分析 期中考

- 學期：100上 (Fall 2011)
- 教授：蘇雅韻
- 考試類型：期中考
- 日期：2011/11/18
- 時限：170 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1326781218.A.4F9.html

### 試題

**Problem 1. Substitution method** [10 points, 3 points for (a) and 7 points for (b)]

For the recurrence of T(n) = T(n/2) + T(n/4) + n
(1) Draw a recursion tree to derive a guess for its upper bound
(2) Use substitution method to prove the upper bound you derived from (1)

**Problem 2. True or False, and Justify** [30 points total, 3 points each]

(1) Asymptotic notations (prove using definition):
  a. T F  If g(n) = O(f(n)), and g(n) = Omega(f(n)), then g(n) = Theta(f(n))
  b. T F  If g(n) = o(f(n)), it is possible that g(n) = Omega(f(n))
  c. T F  If g(n) = omega(f(n)), then g(n) = Omega(f(n))
  d. T F  If g(n) = O(f(n)), then g(n) = o(f(n))
  e. T F  If g(n) = Theta(nlogn), then g(n) = omega(n)
  f. T F  If g(n) = Theta(nlogn), then g(n) = o(n^2)

(2) T F  We covered a selection algorithm that can find the i-th smallest element in an array of n elements in linear time. In the algorithm, the input elements are divided into groups of 5. If the input elements are divided into groups of 7, the total running time will still be linear.

(3) T F  The solution to the recurrence for T(n) = 3T(n/3) + O(nlgn) is T(n) = Theta(nlgn)

(4) T F  If we need to be able to quickly determine if an edge connects two vertices, adjacency list is the preferred way to represent a graph.

(5) T F  Given a file with 31 characters and the following frequencies:
| Character | a  | b | c | d | e |
|-----------|----|---|---|---|---|
| Frequency | 16 | 8 | 4 | 2 | 1 |

Using Huffman encoding, we need a total of 56 bits to encode this file. (Please show the codeword for each character to receive full credits.)

**Problem 3. Graph** [20 points, 5 points each]

The diameter of a tree (sometimes called the width) is the number of nodes on the longest path between two leaves in the tree.

(1) Please describe a brute-force algorithm for finding the diameter of a binary tree based on BFS, and state your running time.
(2) Given a node V, which is on the longest path of the two leaves, describe an algorithm which can determine the diameter of a binary tree in O(n) time?
(3) Describe an algorithm that finds the diameter of a binary tree in O(n) running time.
(4) Prove the correctness of your algorithm.

**Problem 4. Dynamic Programming** [20%, 10 points for (1) and 5 points for (2) and (3) each]

A divide-and-conquer algorithm is presented to solve the maximum subarray problem in class. You are given the same input: an array A of daily stock prices, {P_1, P_2, ..., P_n}.

(1) Design an algorithm that can determine (a) the maximum profit and (b) print out which day to buy and which day to sell the stock to maximize your profit based on dynamic programming strategy.
(2) Analyze the time complexity of your algorithm.
(3) Prove the optimal substructure of your algorithm. That is, prove that the solution to maximum subarray of array A[1...n] utilizes the solution to maximum subarray of A[1...n-1].

**Problem 5. Greedy algorithm** [15%, 5 points each]

You are given an array of elements, n elements in the array are marked, and a number m. The index of marked elements is given to you as a sequence of <i_1, i_2, ..., i_n>. You need to find m subarrays to cover all marked elements. Please design an algorithm such that the total length of the m subarrays is minimal.

(1) Given the example above, what is the minimal total length if m = 3.
(2) Describe your greedy algorithm.
(3) Prove that your greedy choice is correct for your algorithm.

**Problem 6. Graph** [20 points, 5 points each]

(1) Given the graph (A-G directed graph), please mark the finishing time of the DFS algorithm starting from A (assume vertices are explored in lexicographical order).

(2) Show G^T of the graph from (1).

(3) Describe how you would find strongly-connected-components using the information you derived from (1) and (2). Then, write down the strongly-connected-components you found.

(4) Run BFS on the undirected version of G starting from A. Assume vertices in adjacency list are sorted in lexicographical order. List the vertices in the order in which the vertices are enqueued on the FIFO queue during the exploration.

---

## 考試 5：98上 張耀文 演算法 期中考

- 學期：98上 (Fall 2009)
- 教授：張耀文
- 考試類型：期中考
- 日期：2009/11/05
- 時限：150 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1257495443.A.43E.html

### 試題

**Problem 1.** (15 pts total)
For each of the following recurrence relations, give the asymptotic growth rate of the solution using the Theta notation. Assume for each case that T(n) is Theta(1) for n <= 8.

(a) (5 pts) T(n) = 3T(n/2) + n.
(b) (5 pts) T(n) = 2T(n/4) + nlgn.
(c) (5 pts) T(n) = 4T(sqrt(n)) + (lgn)^2.

**Problem 2.** (32 pts total)
Please give a brief answer for each of the following questions.

Q1. For the following three functions, rank them from the slowest (with the lowest complexity) to the fastest growing: (lgn)!, n^(1/lgn), (sqrt(n))^lgn.

Q2. Let f(n) and g(n) be asymptotically positive, is max(f(n),g(n)) = O(f(n)+g(n))? Why?

Q3. Is it true that any comparison sort of 5 elements requires at least 7 comparisons in the worst case? Why?

Q4. Consider a variant of QUICKSORT, such that each time PARTITION is called, the median of the partitioned array is found (by using the SELECT algorithm) and used as a pivot. What is the running time of this algorithm? Why?

Q5. Is it true that counting sort will always sort an array of n integers from {1, 2, ..., m} in O(n) time? Why?

Q6. Can we put the numbers 1, 2, ..., 7 in a tree such that it is both a valid max-heap and binary search tree at the same time? Why?

Q7. We typically need extra time to maintain the information for red-black trees, why are they still useful as compared to standard binary search trees?

Q8. Consider the following algorithm for computing the square root of a number:
```
SQUARE-ROOT(x)
for i=1, ..., x/2
  if i^2 = x then output i.
```
Is it true that this algorithm runs in polynomial time? Why?

**Problem 3.** (10 pts total)
Let X[1..n] and Y[1..n] be two arrays, each containing n numbers already in sorted order. Give an algorithm to find the median of all 2n elements in arrays X and Y. (Partial credits will be given for an algorithm with higher time complexity.)

**Problem 4.** (14 pts total)
Elephants and Lions baseball teams are competing for the 2009 CPBL Championship. Both teams play a series of games until one of the teams wins n games. Assume that the probability of the Elephants winning a game is p and the probability of losing is q = 1-p. Let P(i,j) be the probability of Elephants winning the series if Elephants need i more games to win and Lions needs j more games to win.

(a) (6 pts) Find the optimal substructure (a recurrence relation for P(i,j)).
(b) (3 pts) The probability of winning a game is only 0.4. Find the probability of the Elephants team winning a 3-game series (3 戰 2 勝制).
(c) (5 pts) Give a dynamic programming algorithm for solving the problem. What are the time and space complexity of your algorithm?

**Problem 5.** (14 pts total)
Suppose you are given three strings of characters: X = x1x2...xm, Y = y1y2...yn, and Z = z1z2...z(m+n). Z is said to be a shuffle of X and Y if Z can be formed by interspersing the characters from X and Y in a way that maintains the left-to-right ordering of the characters from each string.

(a) (7 pts) Find the optimal substructure (i.e., derive the recurrence for a problem and its subproblems).
(b) (7 pts) Design a dynamic programming algorithm Is_Shuffle that takes as inputs X, Y, Z, m, and n, and determines whether Z is a shuffle of X and Y. What is the running time of your algorithm?

**Problem 6.** (18 points total)
Search trees. (pseudocode 見課本)

(a) (4 pts) Give the binary search tree that results from successively inserting the keys 7,8,2,1,4,3,5,9 into an initially empty tree.
(b) (4 pts) Label each node in the tree with R or B denoting the respective colors RED and BLACK so that the tree is a legal red-black tree.
(c) (5 pts) Give the red-black tree that results from inserting the key 6 into the tree of (b).
(d) (5 pts) Give the red-black tree that results from deleting the key 1 from the tree of (b) (notice that it is (b), not (c)).

**Problem 7.** (4 pts total)
Please give two of your opinion(s)/comment(s) on this course (e.g., strengths and weaknesses)?

---

## 考試 6：97上 張耀文 演算法 期中考

- 學期：97上 (Fall 2008)
- 教授：張耀文
- 考試類型：期中考
- 日期：2008/11/12
- 時限：150 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1226672709.A.A19.html

### 試題

**Problem 1.** (16 pts total)
For each of the following recurrence relations, give the asymptotic growth rate of the solution using the Theta notation. Assume in each case that T(n) is Theta(1) for n <= 10.

(a) (5 pts) T(n) = 5T(n/2) + (n^3)(lg n).
(b) (5 pts) T(n) = T(sqrt(n)) + lglg n.
(c) (6 pts) T(n) = T(pn) + T(qn) + n, where p + q = 1.

**Problem 2.** (20 pts total)
Please give a brief answer for each of the following questions.

Q1. If f(n) is asymptotically positive, is f(n) + o(f(n)) = O(f(n))? Why?

Q2. Can we have a priority queue in the comparison sorting model with both the properties: (1) EXTRACT-MIN runs in O(lglg n) time, and (2) BUILD-MAX-HEAP runs in O(n) time? Why?

Q3. Suppose that an array contains n numbers, each of which is 0, 1, or 2. Then, can this array be sorted in linear time in the worst case? How to do it if it can, or why it is not possible?

Q4. Can we put the numbers 1, 2, ..., 10 in a tree such that it is both a valid max-heap and binary search tree at the same time? Why?

**Problem 3.** (12 pts total)
Let A0 be a numerical array of length n, originally sorted into ascending order. Assume that k entries of A0 are overwritten with new values, producing an array A. Furthermore assume you have an array B containing n values (0 or 1), where B[i] is true if A[i] is one of the k values that was overwritten, and false otherwise.

(a) (9 pts) Give a fast algorithm to sort A into ascending order, with time complexity better than O(nk). (Hint: Separate out A into two lists.)
(b) (3 pts) Give the time complexity of your algorithm in big-O notation, as a function of n and k (the tighter, the better).

**Problem 4.** (16 pts total)
Search trees.

(a) (5 pts) Give the binary search tree that results from successively inserting the keys 9, 10, 2, 1, 7, 6, 8 into an initially empty tree.
(b) (5 pts) Label each node in the tree with R or B denoting the respective colors RED and BLACK so that the tree is a legal red-black tree.
(c) (6 pts) Give the red-black tree that results from inserting the key 3 into the tree of (b). (Hint: The pseudocode for inserting a node in a red-black tree is given.)

**Problem 5.** (16 pts total)
You are asked to determine the cost and structure of an optimal binary search tree for a set K = <k1,k2,k3,k4> of n=4 keys with the following probabilities:

| i  | 0    | 1    | 2    | 3    | 4    |
|----|------|------|------|------|------|
| pi | -    | 0.10 | 0.10 | 0.20 | 0.05 |
| qi | 0.05 | 0.10 | 0.20 | 0.10 | 0.10 |

(a) (12 pts) Fill every field in the e, w, and root tables.
(b) (4 pts) Find an optimal binary search tree of the given probabilities and give the expected search cost of the tree.

**Problem 6.** (12 pts total)
Professor Chang plans to drive a car from Taipei to Tainan along the Formosa highway (Highway #3). His car's gas tank, when full, holds enough gas to travel n kilometers, and his map gives the distances between gas stations on his route. He wishes to make as few gas stops as possible along the way. Give an efficient algorithm to determine at which gas stations he should stop and prove the optimality of your algorithm.

**Problem 7.** (18 pts total)
Given a log of wood of length k, Woody the woodcutter will cut it once, in any place you choose, for the price of k dollars. Suppose you have a log of length L, marked to be cut in n different locations labeled 1,2,...,n. Let the distance of mark i from the left end of the log be di, and assume that 0 = d0 < d1 < d2 < ... < dn < d(n+1) = L.

(a) (4 pts) Give an example illustrating that two different sequences of cuts to the same marked log can result in two different costs.
(b) (8 pts) Let c(i,j) be the minimum cost of cutting a log with left endpoint i and right endpoint j at all its marked locations. Suppose the log is cut at position m, somewhere between i and j. Define the recurrence of c(i,j) in terms of i, m, j, di and dj.
(c) (6 pts) Using part (b), give an efficient algorithm to solve the wood-cutting problem. Use a table C of size (n+1) x (n+1). What is the running time of your algorithm?

**Problem 8.** (4 pts total)
Please give two of your opinion(s)/comment(s) on this course (e.g., strengths and weaknesses)?

---

## 考試 7：97上 張耀文 演算法 期末考

- 學期：97上 (Fall 2008)
- 教授：張耀文
- 考試類型：期末考
- 日期：2009/01/14
- 時限：150 分鐘
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1231954768.A.B41.html

### 試題

**Problem 1.** (40 pts total)
Please give a brief answer for each of the following questions.

(a) Professor Chang reduces a job assignment problem into the maximum-flow problem. The reduction and the maximum-flow solving take O(VE sqrt(lgC)) time. He claims this job-assignment algorithm to be polynomial-time solvable. Argue if his claim is correct.

(b) Does either Prim's or Kruskal's minimum-spanning-tree algorithm work if there are negative edge weights? Why?

(c) Let P be a shortest path from some vertex s to some other vertex t in a graph. If the weight of each edge in the graph is increased by one, will P still be a shortest path from s to t? Why?

(d) Let G = (V,E) be a weighted directed graph. The capacity of a path is defined as the minimum edge weight among all the edges on the path. Suppose that we want to find a maximum capacity path between each pair of vertices. Show how to modify Floyd-Warshall's all-pair shortest-path algorithm to solve this problem in O(V^3) time.

(e) Let G = (V,E) be a weighted directed graph with edge weights w: E -> R. Define another edge-weight function w'(u,v) = w(u,v) - outdegree(u) + outdegree(v). Then, G contains a negative-weight cycle under w if and only if G contains a negative-weight cycle under w'. Prove or disprove.

(f) Given a maximum flow f on a flow network G = (V,E) with source s and sink t, can a minimum cut separating s from t be found in O(V+E) time? Why?

(g) Professor Chang claims the apparent paradox between statements S1 and S2. Give two possible reasons for this phenomenon.
- S1: P != NP.
- S2: There exists a transformation from some particular instance of the NP-complete HP problem to a shortest path problem solvable by Dijkstra's algorithm.

(h) Consider the Degree-Constrained Spanning-Tree problem (DCST):
- Instance: G = (V,E), a positive integer K <= |V|.
- Question: Is there a spanning tree for G in which no vertex has degree larger than K?
We know that the Hamiltonian path (HP) problem is NP-complete. Is DCST NP-hard? Why?

**Problem 2.** (12 pts total)
Consider a chessboard with some shaded (blocked) squares. We wish to determine a shortest path from square s to square t.

(a) (7 pts) Formulate this problem on an appropriately defined graph. Give an efficient algorithm. What is the time complexity?
(b) (5 pts) Suppose that each boundary of two squares models the penalty or profit for passing through it (cost could be positive or negative). Give an efficient algorithm.

**Problem 3.** (12 pts total) (Acyclic graphs)

(a) (4 pts) Suppose that the constraint graph G = (V,E) corresponding to a linear-programming system of difference constraints is acyclic. Give a linear-time algorithm for finding a solution.
(b) (8 pts) A longest path is a directed path from node s to node t with the maximum length. Give a linear-time algorithm for determining a longest path in an acyclic graph with nonnegative edge lengths.

**Problem 4.** (12 pts total)
A Chinese delegate stays at the Grand Hotel (node s). He would like to meet the Taiwanese president at the Taipei Hall (node t). The chief-of-police needs to deploy minimum police officers on roads to remove protesters.

(a) (9 pts) Apply a polynomial-time algorithm to solve the problem step by step. What is the minimum number of police officers?
(b) (3 pts) Explain why the final result is maximum.

**Problem 5.** (12 pts total)
A realtor needs to maximize the number of apartments sold. She has p apartments, q potential customers, and m salesmen. Each salesman i can sell at most bi apartments. Construct the flow network for the underlying problem and show how to find the maximum number of apartments that can be sold.

**Problem 6.** (18 pts total)
An independent set of a graph G = (V,E) is a subset V' of V such that each edge in E is incident on at most one vertex in V'. The Independent-Set Problem (ISP) is to find a maximum-size independent set in G.

(a) (6 pts) Give an efficient algorithm to solve the ISP when G is bipartite. Justify the correctness.
(b) (2 pts) Formally describe the decision problem of ISP. Let it be ISPD.
(c) (10 pts) Prove that ISPD is NP-complete by using the reduction from 3SAT.

**Problem 7.** (bonus) Please list the corrections to the class notes and lectures you made in this semester, if any.

---

## 考試 8：101上 蔡欣穆 演算法設計與分析 期中考

- 學期：101上 (Fall 2012)
- 教授：蔡欣穆
- 考試類型：期中考
- 日期：2012/11/8
- 時限：180 分鐘
- 總分：128 分
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1352517091.A.26C.html

### 試題

**Problem 1.** In each of the following question, please specify if the statement is true or false. (20 points. 1 point for the true/false answer and 3 points for the explanations.)

1. nlogn is asymptotically larger than n.
2. sqrt(n) * sqrt(logn) is polynomially larger than sqrt(n).
3. The specification should be written by a group of people, as the result of teamwork.
4. We can initialize a heap with only O(n) time.
5. Usually the bottom-up approach is less efficient than the top-down approach when implementing a dynamic programming algorithm.

**Problem 2.** "Short answer" questions: (38 points)

1. Derive a Huffman code for the following frequencies of characters: {a:100, b:300, c:300, d:400, e:600, f:700}. Draw the decoding tree. (6 points)
2. Explain when the master theorem cannot be applied to solve the recurrences. (4 points)
3. Explain what a paper prototype is. Give two advantages of using a paper prototype. (6 points)
4. Write down the recurrences that represent the running time of the quick sort algorithm in the worst case, and solve the recurrences. (6 points)
5. Write down the recurrences that represent the running time of the quick sort algorithm in the best case, and solve the recurrences. (6 points)
6. Explain the difference between functional specifications and technical specifications. (4 points)
7. Recall the divide-and-conquer algorithm that we introduce to solve the closest pair of points in 2D space problem. Explain why it only takes O(n) time to combine the solutions. (6 points)

**Problem 3.** A palindrome is a string which is not changed when it is reversed. Derive an algorithm which will convert a given string to a palindrome with a minimum number of insertions. (22 points)

Examples:
- abcd -> 3 insertions, abcdcba
- abababaabababa -> 0 insertions
- abcdbnmzabcd -> 7 insertions, abcdcbanzmznabcdcba

1. Write down recurrences which represent the cost of converting the string to a palindrome. (6 points)
2. Prove that this problem exhibits the optimal substructure property. (6 points)
3. Write down the algorithm which uses dynamic programming to solve this problem. What is the time complexity? (10 points)

**Problem 4.** n people wish to cross a bridge at night. A group of at most two people may cross at any time, and each group must have a flashlight. Only one flashlight is available. The time for two people to cross is determined by the slower of the two. (22 points)

1. Show that this problem exhibits the optimal substructure property and how you define a subproblem. (6 points)
2. Derive the cost function using the recurrences. (6 points)
3. If you use dynamic programming to solve this problem, what would be the time complexity? (4 points)
4. Show a greedy strategy and prove that it exists in the optimal solution. (6 points)

**Problem 5.** Use a recursion tree to give an asymptotically tight solution to the recurrence T(n) = T(alpha*n) + T((1-alpha)*n) + cn, where alpha is a constant in the range 0 < alpha < 1 and c > 0 is also a constant. Then, use the substitution method to prove the solution. (10 points)

**Problem 6.** Assume you have an array A[1..n] of n elements. A majority element of A is any element occurring in more than n/2 positions. Assume that elements cannot be ordered or sorted, but can be compared for equality. (10 points)

1. Design an efficient divide-and-conquer algorithm to determine whether a majority element exists. (6 points)
2. Determine the time complexity of your algorithm. (4 points)

**Problem 7.** Please write down 3 things you like about this course and 3 things that you would like to see some changes. (6 points)

---

## 考試 9：102上 蔡欣穆 演算法設計與分析 期中考

- 學期：102上 (Fall 2013)
- 教授：蔡欣穆
- 考試類型：期中考
- 日期：2013/11/7
- 時限：180 分鐘
- 總分：132 分
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1389531579.A.F4F.html

### 試題

**Problem 1.** True or false. (16 points. 1 point for true/false and 2 points for explanations)

1. The bug report is usually closed by the person who fixes the bug.
2. The class of NP is the class of languages that cannot be accepted in polynomial time.
3. Different encodings would cause different time complexity for the same algorithm.
4. "A language L is accepted by an algorithm A" means that, for some x not in L, A would reject x.

**Problem 2.** "Short answer" questions: (21 points, 3 points each except 2.6)

1. Why is it necessary for the software tester to minimize the number of steps to generate a bug?
2. What are the 3 things that need to be in a bug report in a bug tracking system?
3. Explain what "polynomially larger" means.
4. Give an example of recurrences that is in the form of T(n) = aT(n/b) + f(n), but cannot be solved with Master theorem.
5. Explain what would happen if a dynamic programming algorithm is designed to solve a problem that does not have overlapping sub-problems.
6. Derive a ternary Huffman code for the following frequencies of characters: {a:100, b:500, c:500, d:600, e:800, f:1000, g:1700, h:1800}. Ternary codes use ternary bits, i.e. {0,1,2}, instead of binary bits. Draw the decoding tree. (6 points)

**Problem 3.** Making changes (8 points)

Assume n kinds of available coins with denominations 1 = a_1 < a_2 < ... < a_n.

1. Describe a greedy algorithm to make change when n = 4 and denominations are 1, 5, 10, 50. Prove that your algorithm always yields an optimal solution. (4 points)
2. Give a set of denominations for which the greedy algorithm does not yield an optimal solution to some m. Give an example. (4 points)

**Problem 4.** Copying Books (26 points)

You have m books (numbered 1,2,...,m) with different numbers of pages (p_1,p_2,...,p_m) and you want to make one copy of each. Divide these books among k scribes, k <= m. Each book can be assigned to a single scriber only, and every scriber must get a continuous sequence of books. The goal is to minimize the maximum number of pages assigned to a single scriber.

1. Define the sub-problem for dynamic programming. (3 points)
2. Write down the recurrences and boundary condition(s). (5 points)
3. Write the pseudo code in O(mk)-time. (5 points)
4. Analyze the time complexity. (3 points)
5. Prove this problem exhibits optimal substructure. (10 points)

**Problem 5.** Revisiting the Problem of Finding the Closest Pair of Points in 2D Space (15 points)

Comparison of original algorithm vs. modified divide step.

1. What is the maximum time complexity that the combine step can have? (3 points)
2. What is the value of N_0 (number of points to check in original algorithm)? Explain. (4 points)
3. What is the value of N_m (number of points to check in new algorithm)? Explain. (4 points)
4. Which algorithm would run faster in reality? Compare. (4 points)

**Problem 6.** Solving the recurrences (20 points)

T(n) = sqrt(n) * T(sqrt(n)) + n. Solution needs to be in Theta-notation.

1. Draw the recurrence tree and estimate the solution. (8 points)
2. Use the substitution method to prove the upper bound O(f(n)). (6 points)
3. Use the substitution method to prove the lower bound Omega(f(n)). (6 points)

**Problem 7.** Maximum Sub-array, the Dynamic Programming Way (20 points)

Given a sequence of n numbers {a_1, a_2, ..., a_n}. Find the sum of the maximum sub-array. Sub-problem S_i is defined as finding the maximum sub-array that starts from anywhere but ends on a_i.

1. Prove optimal substructure. (4 points)
2. Give the cost function recurrences and boundary cases. (6 points)
3. Fill out the cost function table for array {1,-4,3,2,-1,3,5,-4}. (4 points)
4. Write pseudo code to output the starting and ending indices of the maximum sub-array. (6 points)

**Problem 8.** Please write down 3 things you like about this course and 3 things that you would like to see some changes. (6 points)

---

## 考試 10：101上 蔡欣穆 演算法設計與分析 期末考

- 學期：101上 (Fall 2012)
- 教授：蔡欣穆
- 考試類型：期末考
- 日期：2013/1/10
- 時限：180 分鐘
- 總分：130 分
- 來源：https://www.ptt.cc/bbs/NTU-Exam/M.1357919211.A.0A0.html

### 試題

**Problem 1.** True or false. (16 points. 1 point for true/false and 3 points for explanations.)

1. If NPC = P, then P = NP.
2. If L_1, L_2 subset {0,1}* are languages such that L_1 <=p L_2. If L_1 in NPC, then L_2 in NPC.
3. The complexity class NP represents the problems which cannot be decided within polynomial time.
4. When performing an amortized analysis, we usually require the total amortized cost to be a lower bound of the total actual cost.

**Problem 2.** "Short answer" questions: (38 points)

1. Please derive the work T_1(A U B U C U D) and the span T_inf(A U B U C U D) of the multithread algorithm shown in Figure 1. (8 points)
   [Figure 1: Block diagram with blocks A, B, C, D connected in a specific parallel/serial pattern]
2. When the estimated complete time does not meet the original planned ship date, why is it not a good idea to hire more software engineers? What should be done instead? (4 points)
3. Explain briefly how to use evidence-based scheduling to estimate the time to complete a future task. (6 points)
4. In the form of pseudo code, give an example of an algorithm that will result in race condition(s). (4 points)
5. Dynamic tables: Suppose contraction occurs when alpha drops below 1/3, table size is multiplied by 2/3. Use the potential function Phi(T) = |2T.num - T.size| to show that the amortized cost of a table delete function is bounded above by a constant. (8 points)

**Problem 3.** P-Square-Matrix-Multiply (24 points)
```
P-Square-Matrix-Multiply(a,b)
n = a.rows
let c be a new n x n matrix
parallel for i = 1 to n
  parallel for j = 1 to n
    c[i][j] = 0
    for k = 1 to n
      c[i][j] = c[i][j] + a[i][k] * b[k][j]
return c
```

1. Draw the computation DAG for 2x2 matrices. (6 points)
2. Analyze the work, span, and parallelism. (6 points)
3. Modify to have a span of O(logn). (8 points)
4. Show that your modified algorithm indeed has a span of O(logn). (4 points)

**Problem 4.** Task scheduling optimization. (26 points)

One machine, n tasks a_1,...,a_n. Machine available between time 0 and D. Each task a_j requires t_j time, yields profit p_j, ready at time s_j.

1. State this problem as a decision problem. (2 points)
2. Show that the decision problem is NP-complete (reduce from 0-1 knapsack). (8 points)
3. Assuming all processing times and ready times are integers from 1 to n, show optimal substructure. (8 points)
4. Give a polynomial-time dynamic programming algorithm for the decision problem. (8 points)

**Problem 5.** Alpha-balanced binary search trees. (28 points)

A node x is alpha-balanced if x.left.size <= alpha * x.size and x.right.size <= alpha * x.size.

1. Show how to rebuild a subtree rooted at x to become (1/2)-balanced in O(x.size) time. (6 points)
2. Show that searching in an n-node alpha-balanced BST takes O(logn) worst-case time. (4 points)
3. Argue that any BST has nonnegative potential and a (1/2)-balanced tree has potential 0. (4 points)
4. How large must c be in terms of alpha for O(1) amortized rebuild time? (8 points)
   Using potential: Phi(T) = c * sum over {x in T: Delta(x) >= 2} Delta(x), where Delta(x) = |x.left.size - x.right.size|
5. Show that inserting/deleting a node costs O(logn) amortized time. (6 points)

**Problem 6.** What would you do, if you were the instructor, to improve the atmosphere in the classroom? (6 points)
