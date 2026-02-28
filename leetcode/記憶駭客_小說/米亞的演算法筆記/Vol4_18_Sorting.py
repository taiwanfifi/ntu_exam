"""
米亞的演算法筆記 #18 — Sorting 視覺化
《記憶駭客》第243-245章：集體潛意識海洋中分類記憶碎片
「Quick Sort = 直覺。Merge Sort = 耐心。你需要兩個。」
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np, os

# ── 色彩 ──
DARK_BG = '#0a0e14'; MIA_BLUE = '#4fc1e9'; MIA_WARM = '#f5c542'
TEXT = '#d0d7de'; MUTED = '#6e7681'; GRID = '#1c2028'
RED = '#ff6b6b'; GREEN = '#7bc87b'

for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.family'] = font; break
    except Exception: continue
plt.rcParams.update({'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG})

fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.35,
                      left=0.05, right=0.97, top=0.88, bottom=0.06)
fig.suptitle('米亞的演算法筆記 #18 — Sorting\n'
             '「Quick Sort = 直覺。Merge Sort = 耐心。你需要兩個。」',
             fontsize=15, color=MIA_WARM, fontweight='bold', y=0.96)

# ── 左面板：Quick Sort partition ──
ax_qs = fig.add_subplot(gs[:, 0])
ax_qs.set_title('Quick Sort — 直覺式粗分', fontsize=12, color=MIA_BLUE, pad=10)
ax_qs.axis('off')
data_orig = [38, 72, 15, 91, 53, 27, 64, 45]
labels_qs = ['恐懼', '喜悅', '平靜', '狂喜', '懷念', '哀傷', '愛', '倦怠']
rows_data = [
    ("原始", data_orig, None, None),
    ("pivot=53", data_orig, 4, None),
    ("partition", [15, 27, 38, 45, 53, 91, 72, 64], 4, {0, 1, 2, 3}),
]
for row_i, (label, arr, piv, left_set) in enumerate(rows_data):
    y_base = 0.85 - row_i * 0.35
    ax_qs.text(0.02, y_base + 0.08, label, transform=ax_qs.transAxes,
               fontsize=10, color=MIA_WARM, fontweight='bold', va='center')
    for i in range(len(arr)):
        x = 0.05 + i * 0.115
        if piv is not None and i == piv: fc, ec = MIA_WARM+'aa', MIA_WARM
        elif left_set and i in left_set: fc, ec = GREEN+'44', GREEN
        elif left_set and i not in left_set and i != piv: fc, ec = RED+'33', RED
        else: fc, ec = GRID, MUTED
        rect = mpatches.FancyBboxPatch((x, y_base-0.08), 0.1, 0.12,
            transform=ax_qs.transAxes, boxstyle='round,pad=0.01',
            facecolor=fc, edgecolor=ec, lw=1.5)
        ax_qs.add_patch(rect)
        ax_qs.text(x+0.05, y_base-0.02, str(arr[i]), transform=ax_qs.transAxes,
                   ha='center', va='center', fontsize=8.5, color=TEXT, fontweight='bold')
        if row_i == 0:
            ax_qs.text(x+0.05, y_base-0.12, labels_qs[i], transform=ax_qs.transAxes,
                       ha='center', va='center', fontsize=6.5, color=MUTED)
for row_i in range(2):
    ya = 0.85 - row_i*0.35 - 0.18
    ax_qs.annotate('', xy=(0.45, ya-0.02), xytext=(0.45, ya+0.04),
        xycoords='axes fraction', textcoords='axes fraction',
        arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))
ax_qs.text(0.5, 0.05, '< pivot（綠） | pivot（金） | > pivot（紅）',
           transform=ax_qs.transAxes, ha='center', fontsize=8, color=MUTED)

# ── 中面板：Merge Sort divide-and-merge ──
ax_ms = fig.add_subplot(gs[:, 1])
ax_ms.set_title('Merge Sort — 耐心精分', fontsize=12, color=MIA_BLUE, pad=10)
ax_ms.axis('off')
levels = [
    [([38,72,15,91,53,27,64,45], '')],
    [([38,72,15,91], ''), ([53,27,64,45], '')],
    [([38,72], ''), ([15,91], ''), ([53,27], ''), ([64,45], '')],
    [([38], ''), ([72], ''), ([15], ''), ([91], ''),
     ([27], ''), ([53], ''), ([45], ''), ([64], '')],
    [([38,72], ''), ([15,91], ''), ([27,53], ''), ([45,64], '')],
    [([15,38,72,91], ''), ([27,45,53,64], '')],
    [([15,27,38,45,53,64,72,91], '')],
]
level_labels = ['原始', '分割', '分割', '最小', '合併', '合併', '完成']
for lv, groups in enumerate(levels):
    y = 0.92 - lv * 0.125
    x_cursor = 0.5 - sum(len(g[0]) for g in groups) * 0.04
    clr = GREEN if lv >= 4 else (MIA_WARM if lv == 3 else MIA_BLUE)
    ax_ms.text(0.01, y, level_labels[lv], transform=ax_ms.transAxes,
               fontsize=7, color=clr, va='center', fontweight='bold')
    for arr, _ in groups:
        for i, v in enumerate(arr):
            x = x_cursor + i * 0.075
            fc = GREEN+'44' if lv >= 4 else (MIA_WARM+'55' if lv == 3 else GRID)
            ec = GREEN if lv >= 4 else (MIA_WARM if lv == 3 else MUTED)
            rect = mpatches.FancyBboxPatch((x, y-0.03), 0.06, 0.055,
                transform=ax_ms.transAxes, boxstyle='round,pad=0.005',
                facecolor=fc, edgecolor=ec, lw=1)
            ax_ms.add_patch(rect)
            ax_ms.text(x+0.03, y, str(v), transform=ax_ms.transAxes,
                       ha='center', va='center', fontsize=7, color=TEXT)
        x_cursor += len(arr)*0.075 + 0.04
ax_ms.axhline(y=0.92-3.5*0.125, color=MIA_WARM, lw=0.8, ls='--', xmin=0.05, xmax=0.95)
ax_ms.text(0.5, 0.92-3.5*0.125+0.015, '--- 分到最小，開始合併 ---',
           transform=ax_ms.transAxes, ha='center', fontsize=7.5, color=MIA_WARM)

# ── 右上：時間複雜度比較圖 ──
ax_cmp = fig.add_subplot(gs[0, 2])
ax_cmp.set_title('三種排序比較', fontsize=12, color=MIA_BLUE, pad=8)
n_vals = np.logspace(1, 6, 50)
ax_cmp.loglog(n_vals, n_vals*np.log2(n_vals), '-', color=RED, lw=2, label='Quick Sort (avg)')
ax_cmp.loglog(n_vals, n_vals**2, ':', color=RED, lw=1.2, alpha=0.5, label='Quick Sort (worst)')
ax_cmp.loglog(n_vals, n_vals*np.log2(n_vals)*1.5, '-', color=GREEN, lw=2, label='Merge Sort')
ax_cmp.loglog(n_vals, n_vals*np.log2(n_vals)*2, '-', color=MIA_BLUE, lw=2, label='Heap Sort')
ax_cmp.set_xlabel('n（記憶碎片數）', fontsize=9)
ax_cmp.set_ylabel('比較次數', fontsize=9)
ax_cmp.legend(fontsize=7.5, loc='upper left', frameon=False, labelcolor=TEXT)
ax_cmp.grid(True, color=GRID, lw=0.5, alpha=0.5)

# ── 右下：特性比較表 ──
ax_tbl = fig.add_subplot(gs[1, 2])
ax_tbl.axis('off')
ax_tbl.set_title('特性總覽', fontsize=12, color=MIA_BLUE, pad=8)
rows = [
    ['', 'Quick Sort', 'Merge Sort', 'Heap Sort'],
    ['平均', 'O(n log n)', 'O(n log n)', 'O(n log n)'],
    ['最壞', 'O(n²)', 'O(n log n)', 'O(n log n)'],
    ['空間', 'O(log n)', 'O(n)', 'O(1)'],
    ['穩定', '否', '是(穩定)', '否'],
    ['小說', '直覺', '耐心', '紀律'],
    ['章節', 'ch243', 'ch244', 'ch245'],
]
for ri, row in enumerate(rows):
    for ci, cell in enumerate(row):
        c = MIA_WARM if ri == 0 else (MIA_BLUE if ci == 0 else TEXT)
        fw = 'bold' if ri == 0 or ci == 0 else 'normal'
        ax_tbl.text(0.02+ci*0.25, 0.88-ri*0.125, cell, transform=ax_tbl.transAxes,
                    fontsize=8.5, color=c, fontweight=fw, va='center')

fig.text(0.5, 0.01, '「排序是把混亂變成秩序。但秩序不等於意義——你還得選擇用什麼標準排。」— 第245章',
         ha='center', fontsize=10, color=MIA_WARM, style='italic')

out_path = os.path.join(os.path.dirname(__file__), 'Vol4_18_Sorting.png')
plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=DARK_BG, edgecolor='none')
plt.close()
print(f'已儲存：{out_path}')
