"""
米亞的演算法筆記 #14 — Heap / Priority Queue
《記憶駭客》第165, 169, 176-177章：碎片拾荒者歸還系統

「三千七百二十一。Heap 不懂等待。人懂。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# ── Color Palette ──
DARK_BG = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
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

# ── Heap Data: priority values for the tree ──
# Max-Heap: parent >= children
heap_vals = [99.7, 98.3, 97.1, 96.8, 96.2, 94.5, 93.1,
             91.4, 88.7, 85.3, 82.6, 79.8, 76.1, 72.9, 68.4]
heap_labels = [
    '亡夫的信', '女兒第一步', '戰友的臉', '兒子笑聲',
    '畢業典禮', '初戀的歌', '母親的手',
    '婚禮舞曲', '日出記憶', '雨天散步', '生日蛋糕',
    '畢業旅行', '第一份薪', '搬家那天', '廚房味道'
]

# ── Tree Layout: positions for a complete binary tree (15 nodes) ──
def tree_positions(n):
    """Compute (x, y) for each node in a complete binary tree."""
    import math
    depth = int(math.log2(n)) + 1
    pos = {}
    for i in range(n):
        d = int(math.log2(i + 1))
        idx_d = i - (2 ** d - 1)
        sp = 14.0 / (2 ** d + 1)
        pos[i] = (-7 + sp * (idx_d + 1), (depth - 1 - d) * 2.2)
    return pos

# ── Figure ──
fig, (ax_tree, ax_wait) = plt.subplots(
    2, 1, figsize=(16, 13),
    gridspec_kw={'height_ratios': [3, 1.2]})

fig.suptitle('Heap / Priority Queue — 碎片拾荒者歸還系統',
             fontsize=17, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.94,
         '「三千七百二十一。Heap 不懂等待。人懂。」— 第177章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Panel 1: Heap tree structure ──
pos = tree_positions(len(heap_vals))

# Draw edges
for i in range(len(heap_vals)):
    for ch in [2*i+1, 2*i+2]:
        if ch < len(heap_vals):
            ax_tree.plot([pos[i][0], pos[ch][0]], [pos[i][1], pos[ch][1]],
                         color=MUTED, linewidth=1.5, zorder=1)

# Draw nodes
for i in range(len(heap_vals)):
    x, y = pos[i]
    if i == 0:     nc, na, ec = MIA_BLUE, 0.9, MIA_BLUE
    elif i == 14:  nc, na, ec = MIA_WARM, 0.8, MIA_WARM  # boy's mother #3721
    else:          nc, na, ec = GRID, 0.8, MUTED
    ax_tree.add_patch(plt.Circle((x, y), 0.65, facecolor=nc,
                      edgecolor=ec, linewidth=2, alpha=na, zorder=3))
    ax_tree.text(x, y+0.12, f'{heap_vals[i]:.1f}', ha='center', va='center',
                 fontsize=8, color=TEXT if i>0 else DARK_BG, fontweight='bold', zorder=4)
    ax_tree.text(x, y-1.0, heap_labels[i], ha='center', va='center',
                 fontsize=7, color=MUTED, zorder=4)

# Arrow showing extract-max
ax_tree.annotate('extract-max\nO(log n)',
                 xy=(pos[0][0], pos[0][1] + 0.7),
                 xytext=(pos[0][0] + 3.5, pos[0][1] + 2.0),
                 fontsize=10, color=MIA_BLUE, fontweight='bold',
                 ha='center',
                 arrowprops=dict(arrowstyle='->', color=MIA_BLUE, lw=2))

# Arrow pointing to node 14 (bottom right) — 3721
ax_tree.annotate('排第 3721 位\n男孩在門口等了一天',
                 xy=(pos[14][0], pos[14][1] - 0.7),
                 xytext=(pos[14][0] + 1.5, pos[14][1] - 2.5),
                 fontsize=9, color=MIA_WARM, fontweight='bold',
                 ha='center',
                 arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=2))

# Small figure of waiting boy (stick figure)
bx, by = pos[14][0] + 4.0, pos[14][1] - 2.5
ax_tree.plot(bx, by+0.3, 'o', color=MIA_WARM, markersize=6)       # head
ax_tree.plot([bx, bx], [by-0.3, by+0.15], color=MIA_WARM, lw=1.5) # body
ax_tree.plot([bx-0.2, bx+0.2], [by-0.05, by+0.05], color=MIA_WARM, lw=1.5)
ax_tree.plot([bx, bx-0.15], [by-0.3, by-0.6], color=MIA_WARM, lw=1.5)
ax_tree.plot([bx, bx+0.15], [by-0.3, by-0.6], color=MIA_WARM, lw=1.5)

ax_tree.set_xlim(-9, 9)
ax_tree.set_ylim(-4.5, 10)
ax_tree.set_aspect('equal')
ax_tree.axis('off')

# ── Panel 2: Insert + sift-up animation (conceptual) ──
ax_wait.set_xlim(0, 10)
ax_wait.set_ylim(0, 2)
ax_wait.axis('off')

# Show the sift-up path for a new high-priority insert
steps_text = (
    'insert(胎動觸感, 優先級 87.5)  →  '
    'sift-up: [14]→[6]→[2]→[0]  →  '
    '3 次交換  →  升至堆頂  →  O(log n) = O(4)'
)
ax_wait.text(5, 1.4, 'ch169 孕婦案：重新加權後的 sift-up 路徑',
             ha='center', va='center', fontsize=12,
             color=MIA_BLUE, fontweight='bold')
ax_wait.text(5, 0.8, steps_text,
             ha='center', va='center', fontsize=10, color=TEXT)
ax_wait.text(5, 0.2,
             '有些東西的優先級不是算出來的。是感受出來的。— ch169',
             ha='center', va='center', fontsize=10,
             color=MIA_WARM, style='italic')

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=MIA_BLUE, alpha=0.9, label='堆頂 (extract-max)'),
    mpatches.Patch(facecolor=GRID, edgecolor=MUTED, label='一般節點'),
    mpatches.Patch(facecolor=MIA_WARM, alpha=0.8, label='#3721 (男孩的母親)'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol3_14_Heap_Priority_Queue.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
