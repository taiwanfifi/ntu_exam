#!/usr/bin/env python3
"""
LeetCode Linked List Patterns -- 鏈結串列模式完整教學
=====================================================
Target: Google / NVIDIA interview prep (beginner level)
Style : step-by-step numerical traces with pointer states

Sections
--------
1. 基礎操作 (Basic Operations)
   - Reverse Linked List (反轉鏈結串列)
   - Merge Two Sorted Lists (合併兩個排序鏈結串列)
   - Remove Nth Node From End (移除倒數第 N 個節點)
2. 快慢指針 (Fast-Slow Pointers)
   - Middle of Linked List (鏈結串列的中間節點)
   - Linked List Cycle Detection (環形偵測)
   - Linked List Cycle II (環形入口)
3. 進階操作 (Advanced Operations)
   - Palindrome Linked List (回文鏈結串列)
   - Reorder List (重新排列鏈結串列)
   - Sort List (排序鏈結串列 - Merge Sort)
4. Dummy Node 技巧
   - Add Two Numbers (兩數相加)
   - Partition List (分隔鏈結串列)
"""

from typing import Optional, List, Tuple


# ============================================================
# ListNode 定義 & 輔助工具 (Helper Utilities)
# ============================================================
class ListNode:
    """標準 LeetCode 鏈結串列節點"""
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def build_list(vals: list) -> Optional[ListNode]:
    """從 Python list 建立 linked list"""
    if not vals:
        return None
    head = ListNode(vals[0])
    curr = head
    for v in vals[1:]:
        curr.next = ListNode(v)
        curr = curr.next
    return head


def to_list(head: Optional[ListNode]) -> list:
    """將 linked list 轉回 Python list"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def list_to_str(head: Optional[ListNode]) -> str:
    """視覺化: 1 -> 2 -> 3 -> None"""
    parts = []
    while head:
        parts.append(str(head.val))
        head = head.next
    return " -> ".join(parts) + " -> None" if parts else "None"


def build_cycle_list(vals: list, pos: int) -> Optional[ListNode]:
    """建立帶環的 linked list, pos 是 tail 連回的 index (-1 表示無環)"""
    if not vals:
        return None
    head = ListNode(vals[0])
    curr = head
    nodes = [head]
    for v in vals[1:]:
        curr.next = ListNode(v)
        curr = curr.next
        nodes.append(curr)
    if pos >= 0:
        curr.next = nodes[pos]  # tail 指向 pos 位置的節點
    return head


# ============================================================
# Section 1: 基礎操作 (Basic Operations)
# ============================================================

# --------------------------------------------------
# 1-1. Reverse Linked List 反轉鏈結串列 (LC 206)
# --------------------------------------------------
# 核心觀念 (Core Idea):
#   用三個指針 prev/curr/nxt, 逐步把每個節點的 next 指向前一個
#   Time: O(n), Space: O(1)

def reverse_list_iterative(head: Optional[ListNode],
                           verbose: bool = False) -> Optional[ListNode]:
    """Iterative 反轉 -- 最常考的寫法"""
    prev, curr = None, head
    step = 0
    while curr:
        nxt = curr.next          # 暫存下一個
        if verbose:
            step += 1
            print(f"  Step {step}: prev={prev.val if prev else 'None'}, "
                  f"curr={curr.val}, nxt={nxt.val if nxt else 'None'}")
            print(f"    curr.next = prev  =>  {curr.val} -> "
                  f"{prev.val if prev else 'None'}")
        curr.next = prev         # 反轉指向
        prev = curr              # prev 前進
        curr = nxt               # curr 前進
        if verbose:
            print(f"    now prev={prev.val}, curr={curr.val if curr else 'None'}")
    return prev


def reverse_list_recursive(head: Optional[ListNode],
                           verbose: bool = False, depth: int = 0) -> Optional[ListNode]:
    """Recursive 反轉 -- 面試常問你能不能寫遞迴版"""
    if not head or not head.next:
        if verbose:
            print(f"  {'  ' * depth}Base case: head={head.val if head else 'None'}")
        return head
    if verbose:
        print(f"  {'  ' * depth}Recurse on {head.next.val} (head={head.val})")
    new_head = reverse_list_recursive(head.next, verbose, depth + 1)
    if verbose:
        print(f"  {'  ' * depth}Back at head={head.val}: "
              f"head.next.next = head => {head.next.val}.next = {head.val}")
    head.next.next = head    # 讓下一個節點指回自己
    head.next = None         # 斷開原本的 next
    return new_head


def demo_reverse():
    print("=" * 60)
    print("1-1. Reverse Linked List 反轉鏈結串列")
    print("=" * 60)

    # --- Iterative examples ---
    cases_iter = [
        [1, 2, 3, 4, 5],
        [1, 2],
        [7],
    ]
    print("\n【Iterative 迭代法】")
    for vals in cases_iter:
        head = build_list(vals)
        print(f"\n  Input:  {list_to_str(head)}")
        result = reverse_list_iterative(head, verbose=True)
        print(f"  Output: {list_to_str(result)}")

    # --- Recursive examples ---
    cases_rec = [
        [10, 20, 30],
        [5, 3, 8, 1],
        [99],
    ]
    print("\n【Recursive 遞迴法】")
    for vals in cases_rec:
        head = build_list(vals)
        print(f"\n  Input:  {list_to_str(head)}")
        result = reverse_list_recursive(head, verbose=True)
        print(f"  Output: {list_to_str(result)}")


# --------------------------------------------------
# 1-2. Merge Two Sorted Lists 合併排序串列 (LC 21)
# --------------------------------------------------
# 核心觀念: 使用 dummy node, 逐步比較兩串列頭部, 較小的接上去
# Time: O(n+m), Space: O(1) (不含 output)

def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode],
                    verbose: bool = False) -> Optional[ListNode]:
    dummy = ListNode(-1)
    tail = dummy
    step = 0
    while l1 and l2:
        step += 1
        if l1.val <= l2.val:
            if verbose:
                print(f"  Step {step}: compare {l1.val} <= {l2.val}, pick {l1.val}")
            tail.next = l1
            l1 = l1.next
        else:
            if verbose:
                print(f"  Step {step}: compare {l1.val} > {l2.val}, pick {l2.val}")
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    remaining = l1 if l1 else l2
    if verbose and remaining:
        print(f"  Append remaining: {list_to_str(remaining)}")
    tail.next = remaining
    return dummy.next


def demo_merge():
    print("\n" + "=" * 60)
    print("1-2. Merge Two Sorted Lists 合併排序串列")
    print("=" * 60)
    cases = [
        ([1, 2, 4], [1, 3, 4]),
        ([5, 10, 15], [2, 6, 20]),
        ([], [0]),
    ]
    for a, b in cases:
        l1, l2 = build_list(a), build_list(b)
        print(f"\n  L1: {list_to_str(l1)}")
        print(f"  L2: {list_to_str(l2)}")
        result = merge_two_lists(l1, l2, verbose=True)
        print(f"  Merged: {list_to_str(result)}")


# --------------------------------------------------
# 1-3. Remove Nth Node From End 移除倒數第N個 (LC 19)
# --------------------------------------------------
# Two-pass: 先算長度, 再走到 (len - n) 位置
# One-pass:  fast 先走 n 步, 然後 fast/slow 一起走

def remove_nth_from_end_two_pass(head: Optional[ListNode], n: int,
                                 verbose: bool = False) -> Optional[ListNode]:
    """Two-pass 解法"""
    # Pass 1: 計算長度
    length = 0
    curr = head
    while curr:
        length += 1
        curr = curr.next
    if verbose:
        print(f"  Pass 1: total length = {length}")

    # 特殊情況: 移除頭節點
    if n == length:
        if verbose:
            print(f"  Remove head node ({head.val})")
        return head.next

    # Pass 2: 走到 (length - n - 1)
    curr = head
    for i in range(length - n - 1):
        curr = curr.next
        if verbose:
            print(f"  Pass 2 step {i + 1}: move to {curr.val}")
    if verbose:
        print(f"  Remove node {curr.next.val} (curr={curr.val}, skip next)")
    curr.next = curr.next.next
    return head


def remove_nth_from_end_one_pass(head: Optional[ListNode], n: int,
                                 verbose: bool = False) -> Optional[ListNode]:
    """One-pass 解法 (使用 dummy node + 快慢指針)"""
    dummy = ListNode(0, head)
    fast = slow = dummy

    # fast 先走 n+1 步
    for i in range(n + 1):
        if verbose:
            print(f"  Fast advance {i + 1}: fast={fast.next.val if fast.next else 'None'}")
        fast = fast.next

    # fast 和 slow 一起走
    step = 0
    while fast:
        step += 1
        fast = fast.next
        slow = slow.next
        if verbose:
            print(f"  Together step {step}: slow={slow.val}, "
                  f"fast={fast.val if fast else 'None'}")

    if verbose:
        print(f"  Remove node {slow.next.val} after slow={slow.val}")
    slow.next = slow.next.next
    return dummy.next


def demo_remove_nth():
    print("\n" + "=" * 60)
    print("1-3. Remove Nth Node From End 移除倒數第N個")
    print("=" * 60)
    cases = [
        ([1, 2, 3, 4, 5], 2),
        ([1, 2, 3], 3),
        ([1], 1),
    ]
    print("\n【Two-pass 兩次遍歷】")
    for vals, n in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}, n={n}")
        result = remove_nth_from_end_two_pass(head, n, verbose=True)
        print(f"  Output: {list_to_str(result)}")

    print("\n【One-pass 一次遍歷 (快慢指針)】")
    for vals, n in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}, n={n}")
        result = remove_nth_from_end_one_pass(head, n, verbose=True)
        print(f"  Output: {list_to_str(result)}")


# ============================================================
# Section 2: 快慢指針 (Fast-Slow Pointers)
# ============================================================

# --------------------------------------------------
# 2-1. Middle of Linked List 中間節點 (LC 876)
# --------------------------------------------------
# 核心觀念: slow 走一步, fast 走兩步, fast 到底時 slow 在中間
# Time: O(n), Space: O(1)

def middle_of_linked_list(head: Optional[ListNode],
                          verbose: bool = False) -> Optional[ListNode]:
    slow = fast = head
    step = 0
    while fast and fast.next:
        step += 1
        slow = slow.next
        fast = fast.next.next
        if verbose:
            print(f"  Step {step}: slow={slow.val}, "
                  f"fast={fast.val if fast else 'end'}")
    if verbose:
        print(f"  Middle node = {slow.val}")
    return slow


def demo_middle():
    print("\n" + "=" * 60)
    print("2-1. Middle of Linked List 中間節點")
    print("=" * 60)
    cases = [
        [1, 2, 3, 4, 5],       # 奇數: middle = 3
        [1, 2, 3, 4, 5, 6],    # 偶數: second middle = 4
        [1, 2],                 # 兩個: middle = 2
    ]
    for vals in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}")
        result = middle_of_linked_list(head, verbose=True)
        print(f"  Result: middle = {result.val}")


# --------------------------------------------------
# 2-2. Linked List Cycle Detection 環形偵測 (LC 141)
# --------------------------------------------------
# Floyd's Tortoise & Hare: 快慢指針, 若有環必相遇
# Time: O(n), Space: O(1)

def has_cycle(head: Optional[ListNode],
              verbose: bool = False) -> bool:
    slow = fast = head
    step = 0
    while fast and fast.next:
        step += 1
        slow = slow.next
        fast = fast.next.next
        if verbose:
            print(f"  Step {step}: slow={slow.val}, "
                  f"fast={fast.val if fast else 'None'}")
        if slow is fast:
            if verbose:
                print(f"  Cycle detected! slow == fast == {slow.val}")
            return True
    if verbose:
        print(f"  No cycle (fast reached end)")
    return False


def demo_cycle_detection():
    print("\n" + "=" * 60)
    print("2-2. Linked List Cycle Detection 環形偵測 (Floyd)")
    print("=" * 60)

    # Example 1: [3,2,0,-4] cycle at pos=1 (node val=2)
    print("\n  Example 1: [3,2,0,-4], tail connects to index 1 (val=2)")
    head1 = build_cycle_list([3, 2, 0, -4], pos=1)
    has_cycle(head1, verbose=True)

    # Example 2: [1,2] cycle at pos=0
    print("\n  Example 2: [1,2], tail connects to index 0 (val=1)")
    head2 = build_cycle_list([1, 2], pos=0)
    has_cycle(head2, verbose=True)

    # Example 3: [1,2,3,4] no cycle
    print("\n  Example 3: [1,2,3,4], no cycle")
    head3 = build_list([1, 2, 3, 4])
    has_cycle(head3, verbose=True)


# --------------------------------------------------
# 2-3. Linked List Cycle II -- 找入口 (LC 142)
# --------------------------------------------------
# 數學推導 (Math Derivation):
#   設 head 到入口距離 = a, 入口到相遇點 = b, 環長 = c
#   slow 走了 a+b, fast 走了 a+b+k*c (k >= 1)
#   2(a+b) = a+b+k*c  =>  a+b = k*c  =>  a = k*c - b
#   所以從 head 和相遇點同時走, 會在入口相遇!

def detect_cycle_entry(head: Optional[ListNode],
                       verbose: bool = False) -> Optional[ListNode]:
    slow = fast = head
    # Phase 1: 找相遇點
    step = 0
    while fast and fast.next:
        step += 1
        slow = slow.next
        fast = fast.next.next
        if verbose:
            print(f"  Phase1 step {step}: slow={slow.val}, fast={fast.val}")
        if slow is fast:
            if verbose:
                print(f"  Met at node {slow.val}!")
            break
    else:
        if verbose:
            print(f"  No cycle found")
        return None

    # Phase 2: head 和相遇點同時走, 相遇即入口
    ptr = head
    step2 = 0
    while ptr is not slow:
        step2 += 1
        if verbose:
            print(f"  Phase2 step {step2}: ptr={ptr.val}, slow={slow.val}")
        ptr = ptr.next
        slow = slow.next
    if verbose:
        print(f"  Cycle entry = {ptr.val}")
    return ptr


def demo_cycle_entry():
    print("\n" + "=" * 60)
    print("2-3. Linked List Cycle II 環形入口")
    print("=" * 60)
    print("  數學: a = k*c - b, 從 head 和相遇點同時走 => 在入口相遇\n")

    # Example 1: [3,2,0,-4] pos=1 => entry=2
    print("  Example 1: [3,2,0,-4], cycle at index 1")
    h1 = build_cycle_list([3, 2, 0, -4], pos=1)
    entry1 = detect_cycle_entry(h1, verbose=True)
    print(f"  Entry node val = {entry1.val}\n")

    # Example 2: [1,2,3,4,5] pos=2 => entry=3
    print("  Example 2: [1,2,3,4,5], cycle at index 2")
    h2 = build_cycle_list([1, 2, 3, 4, 5], pos=2)
    entry2 = detect_cycle_entry(h2, verbose=True)
    print(f"  Entry node val = {entry2.val}\n")

    # Example 3: [1] pos=0 => entry=1 (self loop)
    print("  Example 3: [1], self-loop at index 0")
    h3 = build_cycle_list([1], pos=0)
    entry3 = detect_cycle_entry(h3, verbose=True)
    print(f"  Entry node val = {entry3.val}")


# ============================================================
# Section 3: 進階操作 (Advanced Operations)
# ============================================================

# --------------------------------------------------
# 3-1. Palindrome Linked List 回文鏈結串列 (LC 234)
# --------------------------------------------------
# 策略: 1) 找中點  2) 反轉後半  3) 逐一比較
# Time: O(n), Space: O(1)

def is_palindrome(head: Optional[ListNode],
                  verbose: bool = False) -> bool:
    if not head or not head.next:
        return True

    # Step 1: 找中點 (slow 停在前半末尾)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    if verbose:
        print(f"  Step 1: mid-point, slow stops at {slow.val}")

    # Step 2: 反轉後半
    second_half = slow.next
    slow.next = None  # 斷開
    prev = None
    curr = second_half
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    reversed_half = prev
    if verbose:
        print(f"  Step 2: reversed second half = {list_to_str(reversed_half)}")
        print(f"          first half           = {list_to_str(head)}")

    # Step 3: 比較
    p1, p2 = head, reversed_half
    is_palin = True
    step = 0
    while p2:
        step += 1
        if verbose:
            match = "==" if p1.val == p2.val else "!="
            print(f"  Step 3.{step}: {p1.val} {match} {p2.val}")
        if p1.val != p2.val:
            is_palin = False
        p1 = p1.next
        p2 = p2.next
    return is_palin


def demo_palindrome():
    print("\n" + "=" * 60)
    print("3-1. Palindrome Linked List 回文鏈結串列")
    print("=" * 60)
    cases = [
        [1, 2, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 2, 3],
    ]
    for vals in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}")
        result = is_palindrome(head, verbose=True)
        print(f"  Is palindrome? {result}")


# --------------------------------------------------
# 3-2. Reorder List 重新排列 (LC 143)
# --------------------------------------------------
# 策略: 1) 找中點  2) 反轉後半  3) 交替合併
# L0 -> L1 -> ... -> Ln  =>  L0 -> Ln -> L1 -> Ln-1 -> ...

def reorder_list(head: Optional[ListNode],
                 verbose: bool = False) -> None:
    if not head or not head.next:
        return

    # Step 1: 找中點
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    if verbose:
        print(f"  Step 1: split at slow={slow.val}")

    # Step 2: 反轉後半
    second = slow.next
    slow.next = None
    prev = None
    curr = second
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev
    if verbose:
        print(f"  Step 2: first  = {list_to_str(head)}")
        print(f"          second = {list_to_str(second)}")

    # Step 3: 交替合併 (interleave)
    first = head
    step = 0
    while second:
        step += 1
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        if verbose:
            print(f"  Step 3.{step}: insert {second.val} after {first.val}")
        first = tmp1
        second = tmp2
    if verbose:
        # 回到 head 印出結果
        print(f"  Result: {list_to_str(head)}")


def demo_reorder():
    print("\n" + "=" * 60)
    print("3-2. Reorder List 重新排列")
    print("=" * 60)
    cases = [
        [1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6],
    ]
    for vals in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}")
        reorder_list(head, verbose=True)
        print(f"  Output: {list_to_str(head)}")


# --------------------------------------------------
# 3-3. Sort List 排序鏈結串列 - Merge Sort (LC 148)
# --------------------------------------------------
# 核心觀念: 鏈結串列上的 merge sort
#   1) 快慢指針找中點, 分成兩半
#   2) 遞迴排序左右
#   3) 合併兩個已排序串列
# Time: O(n log n), Space: O(log n) recursion stack

def sort_list(head: Optional[ListNode],
              verbose: bool = False, depth: int = 0) -> Optional[ListNode]:
    indent = "  " + "  " * depth
    if not head or not head.next:
        if verbose and head:
            print(f"{indent}Base: [{head.val}]")
        return head

    if verbose:
        print(f"{indent}Sort: {list_to_str(head)}")

    # 找中點 & 切半
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None

    if verbose:
        print(f"{indent}Split -> left={list_to_str(head)}, right={list_to_str(mid)}")

    left = sort_list(head, verbose, depth + 1)
    right = sort_list(mid, verbose, depth + 1)

    # 合併 (不用 verbose 避免太冗長, 用 merge_two_lists 邏輯)
    dummy = ListNode(0)
    tail = dummy
    while left and right:
        if left.val <= right.val:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next
        tail = tail.next
    tail.next = left if left else right

    if verbose:
        print(f"{indent}Merged => {list_to_str(dummy.next)}")
    return dummy.next


def demo_sort():
    print("\n" + "=" * 60)
    print("3-3. Sort List 排序鏈結串列 (Merge Sort)")
    print("=" * 60)
    cases = [
        [4, 2, 1, 3],
        [-1, 5, 3, 4, 0],
        [3, 1],
    ]
    for vals in cases:
        head = build_list(vals)
        print(f"\n  Input:  {list_to_str(head)}")
        result = sort_list(head, verbose=True)
        print(f"  Output: {list_to_str(result)}")


# ============================================================
# Section 4: Dummy Node 技巧
# ============================================================
# 何時使用 Dummy Node? (When to use?)
#   1. head 可能被修改或刪除時 (e.g., remove, partition)
#   2. 需要從空串列開始建構結果時 (e.g., merge, add)
#   3. 簡化邊界條件 (edge cases), 不用特判 head == None

# --------------------------------------------------
# 4-1. Add Two Numbers 兩數相加 (LC 2)
# --------------------------------------------------
# 數字以反向 linked list 儲存: 342 = 2->4->3
# Time: O(max(m,n)), Space: O(max(m,n))

def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode],
                    verbose: bool = False) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    step = 0
    while l1 or l2 or carry:
        step += 1
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        old_carry = carry
        carry = total // 10
        digit = total % 10
        if verbose:
            print(f"  Step {step}: {v1} + {v2} + carry={old_carry} "
                  f"= {total} => digit={digit}, new carry={carry}")
        curr.next = ListNode(digit)
        curr = curr.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


def demo_add_two():
    print("\n" + "=" * 60)
    print("4-1. Add Two Numbers 兩數相加 (Dummy Node)")
    print("=" * 60)
    print("  數字以反序存放: 342 => 2->4->3")
    cases = [
        ([2, 4, 3], [5, 6, 4]),       # 342 + 465 = 807
        ([9, 9, 9], [1]),              # 999 + 1 = 1000
        ([0], [0]),                    # 0 + 0 = 0
    ]
    for a, b in cases:
        l1, l2 = build_list(a), build_list(b)
        num_a = int("".join(str(x) for x in reversed(a)))
        num_b = int("".join(str(x) for x in reversed(b)))
        print(f"\n  {num_a} + {num_b} = {num_a + num_b}")
        print(f"  L1: {list_to_str(l1)}")
        print(f"  L2: {list_to_str(l2)}")
        result = add_two_numbers(l1, l2, verbose=True)
        print(f"  Result: {list_to_str(result)}")


# --------------------------------------------------
# 4-2. Partition List 分隔鏈結串列 (LC 86)
# --------------------------------------------------
# 給定 x, 把 < x 的放前面, >= x 的放後面, 保持相對順序
# 用兩個 dummy node: before_head 和 after_head
# Time: O(n), Space: O(1)

def partition_list(head: Optional[ListNode], x: int,
                   verbose: bool = False) -> Optional[ListNode]:
    before = before_head = ListNode(0)
    after = after_head = ListNode(0)
    step = 0
    while head:
        step += 1
        if head.val < x:
            if verbose:
                print(f"  Step {step}: {head.val} < {x}, goes to 'before' list")
            before.next = head
            before = before.next
        else:
            if verbose:
                print(f"  Step {step}: {head.val} >= {x}, goes to 'after' list")
            after.next = head
            after = after.next
        head = head.next
    after.next = None           # 斷尾 (避免形成環)
    before.next = after_head.next  # before 接上 after
    if verbose:
        print(f"  Before list: {list_to_str(before_head.next)}")
        # rebuild after for display
        print(f"  Connected: before -> after")
    return before_head.next


def demo_partition():
    print("\n" + "=" * 60)
    print("4-2. Partition List 分隔鏈結串列 (Dummy Node)")
    print("=" * 60)
    cases = [
        ([1, 4, 3, 2, 5, 2], 3),
        ([2, 1], 2),
        ([1, 1, 1, 3, 5, 2, 4], 3),
    ]
    for vals, x in cases:
        head = build_list(vals)
        print(f"\n  Input: {list_to_str(head)}, x={x}")
        result = partition_list(head, x, verbose=True)
        print(f"  Output: {list_to_str(result)}")


# ============================================================
# 速查表 (Quick Reference Cheat Sheet)
# ============================================================
def print_cheat_sheet():
    print("\n" + "=" * 60)
    print("Linked List 解題速查表 (Cheat Sheet)")
    print("=" * 60)
    sheet = """
  Pattern              | When to use                    | Time  | Space
  ---------------------+--------------------------------+-------+------
  Reverse iterative    | 反轉整條/部分串列              | O(n)  | O(1)
  Reverse recursive    | 面試要求遞迴版本               | O(n)  | O(n)
  Merge two sorted     | 合併已排序串列                 | O(n+m)| O(1)
  Remove Nth from end  | 刪除倒數第 k 個                | O(n)  | O(1)
  Fast-slow (middle)   | 找中點                         | O(n)  | O(1)
  Floyd's cycle detect | 判斷有無環                     | O(n)  | O(1)
  Floyd's cycle entry  | 找環的入口                     | O(n)  | O(1)
  Palindrome check     | 回文判斷 (reverse 2nd half)    | O(n)  | O(1)
  Reorder list         | L0->Ln->L1->Ln-1 重排          | O(n)  | O(1)
  Merge sort on list   | 排序鏈結串列                   | O(nlogn)| O(logn)
  Add two numbers      | 兩數相加 (反序存放)            | O(n)  | O(n)
  Partition list       | 依值分隔 (保持順序)            | O(n)  | O(1)

  關鍵技巧:
  1. Dummy Node -- head 可能改變時, 用 dummy 簡化邊界條件
  2. prev/curr/nxt -- 反轉時的三指針標配
  3. 快慢指針 -- 找中點、偵測環
  4. 斷開 + 合併 -- 很多題都是「拆成兩半 -> 操作 -> 合併」
"""
    print(sheet)


# ============================================================
# Main -- 執行全部範例
# ============================================================
def main():
    print("LeetCode Linked List Patterns -- 鏈結串列完整教學")
    print("Target: Google / NVIDIA | Beginner Level")
    print("每題都有 step-by-step pointer trace\n")

    # Section 1
    demo_reverse()
    demo_merge()
    demo_remove_nth()

    # Section 2
    demo_middle()
    demo_cycle_detection()
    demo_cycle_entry()

    # Section 3
    demo_palindrome()
    demo_reorder()
    demo_sort()

    # Section 4
    demo_add_two()
    demo_partition()

    # Cheat sheet
    print_cheat_sheet()

    print("\n" + "=" * 60)
    print("All demos completed! 所有範例執行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
