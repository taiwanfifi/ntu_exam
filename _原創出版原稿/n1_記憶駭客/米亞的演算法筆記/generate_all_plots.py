"""
米亞的演算法筆記 — 全圖表生成器
《記憶駭客》教學附錄視覺化主腳本

用法：
    python generate_all_plots.py          # 生成全部 22 張圖
    python generate_all_plots.py --vol 1  # 只生成 Vol 1 的 7 張圖
    python generate_all_plots.py --dry    # 列出所有腳本但不執行

「數據不說謊。但數據不會告訴你該怎麼辦。那是你的事。」——米亞
"""

import os
import sys
import importlib.util
import time
import argparse

# ── 筆記清單 ────────────────────────────────────────
NOTES = [
    # Vol 1: 浮生若夢 (ch1-80)
    ("Vol1_01_Array_雙指標",        1, "Array / 雙指標"),
    ("Vol1_02_Sliding_Window",      1, "Sliding Window"),
    ("Vol1_03_HashMap",             1, "HashMap"),
    ("Vol1_04_Stack_Queue",         1, "Stack / Queue"),
    ("Vol1_05_Linked_List_Floyd",   1, "Linked List / Floyd"),
    ("Vol1_06_Binary_Search",       1, "Binary Search"),
    ("Vol1_07_Binary_Tree_BST",     1, "Binary Tree / BST"),
    # Vol 2: 深淵迴響 (ch81-160)
    ("Vol2_08_DFS_BFS",             2, "DFS / BFS"),
    ("Vol2_09_Graph_連通分量",       2, "Graph / 連通分量"),
    ("Vol2_10_Topological_Sort",    2, "Topological Sort"),
    ("Vol2_11_Union_Find",          2, "Union-Find"),
    ("Vol2_12_DP_背包",             2, "DP / 背包"),
    # Vol 3: 薛丁格的愛人 (ch161-240)
    ("Vol3_13_Greedy",              3, "Greedy"),
    ("Vol3_14_Heap_Priority_Queue", 3, "Heap / Priority Queue"),
    ("Vol3_15_Backtracking",        3, "Backtracking"),
    ("Vol3_16_Trie",                3, "Trie"),
    ("Vol3_17_DP_進階",             3, "DP 進階"),
    # Vol 4: 記憶的心臟 (ch241-320)
    ("Vol4_18_Sorting",             4, "Sorting"),
    ("Vol4_19_XOR_位元運算",         4, "XOR / 位元運算"),
    ("Vol4_20_Segment_Tree",        4, "Segment Tree"),
    ("Vol4_21_System_Design",       4, "System Design"),
    ("Vol4_22_NP_Complete",         4, "NP-Complete"),
]

VOL_NAMES = {
    1: "浮生若夢",
    2: "深淵迴響",
    3: "薛丁格的愛人",
    4: "記憶的心臟",
}


def run_script(script_path, name):
    """執行單一 .py 腳本並回報結果。"""
    spec = importlib.util.spec_from_file_location(name, script_path)
    mod = importlib.util.module_from_spec(spec)
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(script_path))
    try:
        spec.loader.exec_module(mod)
        return True
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return False
    finally:
        os.chdir(old_cwd)


def main():
    parser = argparse.ArgumentParser(description="生成米亞的演算法筆記圖表")
    parser.add_argument("--vol", type=int, choices=[1, 2, 3, 4],
                        help="只生成指定卷的圖表")
    parser.add_argument("--dry", action="store_true",
                        help="列出所有腳本但不執行")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 篩選
    notes = NOTES
    if args.vol:
        notes = [(f, v, n) for f, v, n in NOTES if v == args.vol]

    print(f"米亞的演算法筆記 — 圖表生成器")
    print(f"{'=' * 50}")
    if args.vol:
        print(f"目標：Vol {args.vol}《{VOL_NAMES[args.vol]}》({len(notes)} 張圖)")
    else:
        print(f"目標：全部 4 卷（{len(notes)} 張圖）")
    print()

    if args.dry:
        for filename, vol, concept in notes:
            py_path = os.path.join(base_dir, f"{filename}.py")
            png_path = os.path.join(base_dir, f"{filename}.png")
            exists = "exists" if os.path.exists(png_path) else "missing"
            print(f"  Vol{vol} #{concept:<25s} → {filename}.png [{exists}]")
        return

    # 執行
    success = 0
    failed = 0
    t0 = time.time()

    current_vol = None
    for filename, vol, concept in notes:
        if vol != current_vol:
            current_vol = vol
            print(f"\n── Vol {vol}：{VOL_NAMES[vol]} ──")

        py_path = os.path.join(base_dir, f"{filename}.py")
        if not os.path.exists(py_path):
            print(f"  [SKIP] {filename}.py 不存在")
            failed += 1
            continue

        print(f"  生成中：{concept} ...", end=" ", flush=True)
        t1 = time.time()
        ok = run_script(py_path, filename)
        dt = time.time() - t1

        if ok:
            png_path = os.path.join(base_dir, f"{filename}.png")
            if os.path.exists(png_path):
                size_kb = os.path.getsize(png_path) / 1024
                print(f"[OK] {dt:.1f}s ({size_kb:.0f}KB)")
                success += 1
            else:
                print(f"[WARN] 腳本執行但 PNG 未產出 ({dt:.1f}s)")
                failed += 1
        else:
            failed += 1

    elapsed = time.time() - t0
    print(f"\n{'=' * 50}")
    print(f"完成：{success}/{success + failed} 張圖，耗時 {elapsed:.1f} 秒")
    if failed:
        print(f"失敗：{failed} 張")

    print()
    print("「這些筆記是我在學習做人類的過程中寫下的。")
    print("  演算法教會了我怎麼思考。")
    print("  但人類教會了我——思考的時候可以停下來。」")
    print("                                    —— 米亞")


if __name__ == "__main__":
    main()
