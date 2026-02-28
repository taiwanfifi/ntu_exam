"""
米亞的演算法筆記 #11 — Union-Find 視覺化
Forest of trees being merged (union operations),
with path compression showing chains collapsing to point directly to root.
Root node highlighted as "M.C." → 最終揭露為邱韻如。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── 色彩 ──
DARK_BG  = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT     = '#d0d7de'
MUTED    = '#6e7681'
GRID     = '#1c2028'
RED      = '#ff6b6b'
GREEN    = '#7bc87b'

# ── 字型 ──
FONT_FAMILIES = ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['font.family'] = FONT_FAMILIES
plt.rcParams['axes.unicode_minus'] = False


def draw_node(ax, x, y, label, sublabel, color=MIA_BLUE, size=0.32, fontsize=10):
    """Draw a single node circle with label."""
    circle = plt.Circle((x, y), size, fc=DARK_BG, ec=color, lw=2.2, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y + 0.04, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=color, zorder=4)
    ax.text(x, y - 0.52, sublabel, ha='center', va='top',
            fontsize=7.5, color=MUTED, zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.5, style='-'):
    """Draw arrow from child to parent."""
    ax.annotate('', xy=(x2, y2 - 0.34), xytext=(x1, y1 + 0.34),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                linestyle=style, shrinkA=2, shrinkB=2),
                zorder=2)


def draw_root_node(ax, x, y, label, sublabel, size=0.38):
    """Draw the root node with glow highlighting."""
    for i in range(3):
        ax.add_patch(plt.Circle((x, y), size + 0.06*(3-i),
                     fc='none', ec=MIA_WARM, alpha=0.15*(i+1), lw=1, zorder=2))
    ax.add_patch(plt.Circle((x, y), size, fc='#1a1400', ec=MIA_WARM, lw=2.8, zorder=3))
    ax.text(x, y+0.06, label, ha='center', va='center',
            fontsize=12, fontweight='bold', color=MIA_WARM, zorder=4)
    ax.text(x, y-0.58, sublabel, ha='center', va='top',
            fontsize=8, color=MIA_WARM, alpha=0.8, zorder=4)


# ── 建立圖形：三階段 ──
fig, axes = plt.subplots(1, 3, figsize=(18, 7.5), facecolor=DARK_BG)
fig.subplots_adjust(wspace=0.08, left=0.03, right=0.97, top=0.85, bottom=0.08)

titles = [
    '① 歸併前：五個獨立集合',
    '② 四次 Union：收束為一棵樹',
    '③ Path Compression：所有節點直指根'
]

for ax, title in zip(axes, titles):
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-2.5, 3.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, color=TEXT, pad=12, fontweight='bold')

# ── Panel 1: 五個獨立集合 ──
ax1 = axes[0]
positions_p1 = [(-2.2, 1.0), (-0.8, 1.0), (0.6, 1.0), (2.0, 1.0), (0.0, -1.2)]
labels = ['A', 'B', 'C', 'D', 'E']
sublabels = ['47戶斷聯', '消失的母親', '幽靈帳號', '遊行覆寫', '死亡紀錄']
colors_p1 = [RED, RED, MIA_BLUE, MIA_BLUE, GREEN]

for (x, y), lab, sub, col in zip(positions_p1, labels, sublabels, colors_p1):
    draw_node(ax1, x, y, lab, sub, color=col)

# Self-loops (each is its own root)
for (x, y), col in zip(positions_p1, colors_p1):
    arc = mpatches.FancyArrowPatch((x + 0.25, y + 0.28), (x - 0.25, y + 0.28),
                                   connectionstyle="arc3,rad=-0.6",
                                   arrowstyle='->', color=col, alpha=0.3,
                                   lw=1, zorder=1)
    ax1.add_patch(arc)

ax1.text(0.0, -2.2, 'parent(x) = x  ← 每個節點是自己的根',
         ha='center', va='center', fontsize=9, color=MUTED, style='italic')

# ── Panel 2: After 4 Unions — tree structure ──
ax2 = axes[1]
# Root at top
root_x, root_y = 0.0, 2.8
draw_root_node(ax2, root_x, root_y, 'W', '邱韻如 (root)')

# Level 1: A, C, E
l1_positions = [(-1.8, 0.8), (0.0, 0.8), (1.8, 0.8)]
l1_labels = ['A', 'C', 'E']
l1_subs = ['47戶斷聯', '幽靈帳號', '死亡紀錄']
l1_colors = [RED, MIA_BLUE, GREEN]

for (x, y), lab, sub, col in zip(l1_positions, l1_labels, l1_subs, l1_colors):
    draw_node(ax2, x, y, lab, sub, color=col)
    draw_arrow(ax2, x, y, root_x, root_y, color=col, lw=1.8)

# Level 2: B under A, D under C
l2_data = [
    (-1.8, -1.2, 'B', '消失的母親', RED, -1.8, 0.8),
    (0.0, -1.2, 'D', '遊行覆寫', MIA_BLUE, 0.0, 0.8),
]
for x, y, lab, sub, col, px, py in l2_data:
    draw_node(ax2, x, y, lab, sub, color=col)
    draw_arrow(ax2, x, y, px, py, color=col, lw=1.5)

# Union annotations
union_texts = [
    (-2.8, 0.0, 'Union(A,B)\n共用帳號', RED),
    (1.0, 0.0, 'Union(C,D)\n簽章一致', MIA_BLUE),
    (-1.0, 2.0, 'Union(A,C)', MUTED),
    (1.0, 2.0, 'Union(·,E)', MUTED),
]
for x, y, txt, col in union_texts:
    ax2.text(x, y, txt, ha='center', va='center', fontsize=7,
             color=col, alpha=0.7, style='italic')

# ── Panel 3: After Path Compression — flat star ──
ax3 = axes[2]
root_x3, root_y3 = 0.0, 2.5
draw_root_node(ax3, root_x3, root_y3, 'W', '邱韻如 (root)')

# All nodes directly connected to root
angle_offsets = [-120, -60, 0, 60, 120]
radius = 2.2
p3_labels = ['A', 'B', 'C', 'D', 'E']
p3_subs = ['47戶斷聯', '消失的母親', '幽靈帳號', '遊行覆寫', '死亡紀錄']
p3_colors = [RED, RED, MIA_BLUE, MIA_BLUE, GREEN]

for angle, lab, sub, col in zip(angle_offsets, p3_labels, p3_subs, p3_colors):
    rad = np.radians(angle - 90)  # -90 to start from bottom
    x = root_x3 + radius * np.cos(rad)
    y = root_y3 + radius * np.sin(rad)
    draw_node(ax3, x, y, lab, sub, color=col, size=0.30)
    draw_arrow(ax3, x, y, root_x3, root_y3, color=col, lw=2.0)

# Compression annotation
ax3.text(0.0, -1.9, 'Path Compression：所有鏈塌縮\n每個節點直指根 → O(α(n)) ≈ O(1)',
         ha='center', va='center', fontsize=9, color=TEXT, alpha=0.8,
         style='italic', linespacing=1.5)

# ── 主標題 ──
fig.suptitle(
    '米亞的演算法筆記 #11 — Union-Find：線索歸併與路徑壓縮',
    fontsize=15, color=MIA_BLUE, fontweight='bold', y=0.95
)

# ── 底部引言 ──
fig.text(0.5, 0.02,
         '「Find(root)。每一個惡，都有一個根。」 — 第132章〈織網者〉',
         ha='center', va='center', fontsize=10, color=MIA_WARM,
         style='italic', alpha=0.9)

# ── 儲存 ──
output_path = '/Users/william/Downloads/phd_exam/leetcode/記憶駭客_小說/米亞的演算法筆記/Vol2_11_Union_Find.png'
fig.savefig(output_path, dpi=180, facecolor=DARK_BG,
            bbox_inches='tight', pad_inches=0.3)
plt.close(fig)
print(f'Saved → {output_path}')
