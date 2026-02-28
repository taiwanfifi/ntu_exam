"""
米亞的演算法筆記 #01 — Two Pointers 雙指標
《記憶駭客》第1-2章：老陳的婚禮記憶碎片排列

「把東西排好，是哀悼的第一步。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Color Palette ──
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
DARK_BG = '#0a0e14'
TEXT = '#d0d7de'
MUTED = '#6e7681'
GRID = '#1c2028'
RED = '#ff6b6b'
GREEN = '#7bc87b'

# ── Chinese Font Detection ──
def get_chinese_font():
    for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
        try:
            from matplotlib.font_manager import FontProperties
            fp = FontProperties(family=font)
            if fp.get_name() != font:
                continue
            return font
        except Exception:
            continue
    return 'PingFang TC'

FONT_FAMILY = get_chinese_font()
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['axes.facecolor'] = DARK_BG
plt.rcParams['figure.facecolor'] = DARK_BG
plt.rcParams['text.color'] = TEXT
plt.rcParams['axes.edgecolor'] = MUTED
plt.rcParams['xtick.color'] = MUTED
plt.rcParams['ytick.color'] = MUTED

# ── Data: Memory fragments (timestamps as minutes from start) ──
np.random.seed(42)
n_fragments = 12
sorted_times = np.sort(np.random.uniform(0, 720, n_fragments)).astype(int)
labels_zh = [
    '到場', '簽名', '入座', '開場', '敬酒',
    '致詞', '切蛋糕', '擁抱', '合照', '跳舞',
    '送客', '微笑'
]

# ── Figure Setup ──
fig, axes = plt.subplots(4, 1, figsize=(14, 11),
                         gridspec_kw={'height_ratios': [1.2, 1.2, 1.2, 1.2]})
fig.suptitle('Two Pointers — 老陳的婚禮記憶碎片排列',
             fontsize=16, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.935, '「把東西排好，是哀悼的第一步。」— 第1章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Helper: draw array ──
def draw_array(ax, arr, labels, L, R, step_label, highlight_sorted=None):
    ax.set_xlim(-0.8, len(arr) - 0.2)
    ax.set_ylim(-1.2, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')

    # Step label
    ax.text(-0.7, 1.6, step_label, fontsize=12, color=TEXT, fontweight='bold',
            va='center')

    box_w = 0.8
    for i, (val, lab) in enumerate(zip(arr, labels)):
        # Box color
        if highlight_sorted is not None and i in highlight_sorted:
            fc = GREEN + '33'
            ec = GREEN
        elif i == L or i == R:
            fc = MIA_BLUE + '33'
            ec = MIA_BLUE
        else:
            fc = GRID
            ec = MUTED

        rect = mpatches.FancyBboxPatch(
            (i - box_w/2, -0.1), box_w, 0.9,
            boxstyle='round,pad=0.05', facecolor=fc, edgecolor=ec, linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(i, 0.35, lab, ha='center', va='center',
                fontsize=8, color=TEXT, fontweight='bold')
        ax.text(i, -0.35, f'{val}m', ha='center', va='center',
                fontsize=7, color=MUTED)

    # Pointer arrows
    if L is not None and L < len(arr):
        ax.annotate('L', xy=(L, -0.15), xytext=(L, -0.9),
                    fontsize=11, color=RED, fontweight='bold',
                    ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', color=RED, lw=2))
    if R is not None and R < len(arr):
        ax.annotate('R', xy=(R, -0.15), xytext=(R, -0.9),
                    fontsize=11, color=MIA_WARM, fontweight='bold',
                    ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=2))

# ── Scrambled order ──
scramble_idx = [3, 7, 0, 10, 5, 1, 11, 8, 2, 6, 4, 9]
scrambled_times = sorted_times[scramble_idx]
scrambled_labels = [labels_zh[i] for i in scramble_idx]

# Step 0: Initial scrambled state
draw_array(axes[0], scrambled_times, scrambled_labels,
           0, 11, '初始狀態：碎片打亂', highlight_sorted=None)

# Step 1: After first pass — L=1, R=10, ends placed
step1_idx = [0, 7, 3, 10, 5, 1, 8, 2, 6, 4, 9, 11]
step1_times = sorted_times[step1_idx]
step1_labels = [labels_zh[i] for i in step1_idx]
draw_array(axes[1], step1_times, step1_labels,
           1, 10, '步驟1-2：兩端歸位', highlight_sorted={0, 11})

# Step 2: Midway — L=4, R=7
step2_idx = [0, 1, 2, 3, 5, 7, 8, 10, 6, 9, 4, 11]
step2_times = sorted_times[step2_idx]
step2_labels = [labels_zh[i] for i in step2_idx]
draw_array(axes[2], step2_times, step2_labels,
           4, 7, '步驟5-6：向中間收攏', highlight_sorted={0, 1, 2, 3, 11, 10, 9, 8})

# Step 3: Final sorted state
draw_array(axes[3], sorted_times, labels_zh,
           None, None, '完成：47段歸位（示意12段）',
           highlight_sorted=set(range(12)))

# Highlight the last fragment (smile)
axes[3].text(11, 1.5, '← 最後歸位：妻子的微笑',
             fontsize=10, color=MIA_WARM, style='italic', va='center')

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=RED + '55', edgecolor=RED, label='L 指標（左端）'),
    mpatches.Patch(facecolor=MIA_WARM + '55', edgecolor=MIA_WARM, label='R 指標（右端）'),
    mpatches.Patch(facecolor=GREEN + '33', edgecolor=GREEN, label='已歸位'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol1_01_Array_雙指標.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
