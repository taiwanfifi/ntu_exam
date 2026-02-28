"""
米亞的演算法筆記 #16 — Trie 前綴樹
《記憶駭客》第182-184, 194-195章：
  周明哲的記憶碎片前綴編碼 / 黑市記憶池搜尋阿嬤的豆漿

「正確的前綴，能在一百萬段記憶裡找到一碗豆漿。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# ── Trie structure for visualization (black-market memory pool) ──
# Highlighted path: JX-2079-10-28-003 (阿嬤的記憶)
def N(label, children=None, leaf=None, hit=False):
    """Shorthand node constructor."""
    d = {'label': label, 'hit': hit}
    if children: d['children'] = children
    if leaf: d['leaf'] = leaf
    return d

TREE = N('ROOT', hit=True, children=[
    N('J', hit=True, children=[
        N('X', hit=True, children=[
            N('-20', hit=True, children=[
                N('79-', hit=True, children=[
                    N('10-', hit=True, children=[
                        N('28-', hit=True, children=[
                            N('001', leaf='記憶碎片 #1'),
                            N('003', leaf='阿嬤的豆漿', hit=True),
                            N('017', leaf='記憶碎片 #17')]),
                        N('31-', children=[N('009', leaf='其他記憶')])]),
                    N('11-', children=[
                        N('02-', children=[N('044', leaf='其他記憶')])])]),
                N('80-', children=[
                    N('03-', children=[
                        N('12-', children=[N('556', leaf='其他記憶')])])])])])]),
    N('K', children=[
        N('M', children=[
            N('-20', children=[
                N('81-', children=[N('...', leaf='其他區段')])])])])])

# ── Layout: compute (x, y) for each node ──
positions = []   # (x, y, label, is_hit, leaf_text_or_None)
edges_draw = []  # (x1, y1, x2, y2, is_hit)

def layout(node, depth, x_left, x_right):
    x, y = (x_left + x_right) / 2, -depth * 1.15
    hit, leaf = node.get('hit', False), node.get('leaf', None)
    positions.append((x, y, node['label'], hit, leaf))
    for i, child in enumerate(node.get('children', [])):
        w = (x_right - x_left) / len(node['children'])
        ci = len(positions)
        layout(child, depth + 1, x_left + i * w, x_left + (i + 1) * w)
        edges_draw.append((x, y, positions[ci][0], positions[ci][1],
                           hit and child.get('hit', False)))

layout(TREE, 0, 0, 16)

# ── Figure ──
fig, ax = plt.subplots(figsize=(15, 10))
fig.suptitle('Trie（前綴樹）— 黑市記憶池搜尋路徑',
             fontsize=17, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.935,
         '「在百萬人的記憶裡找一碗三十年前的豆漿——你需要的不是運氣。是正確的開頭。」',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# Draw edges
for x1, y1, x2, y2, hit in edges_draw:
    color = MIA_WARM if hit else MUTED
    lw = 2.8 if hit else 1.0
    alpha = 1.0 if hit else 0.4
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, alpha=alpha, zorder=1)

# Draw nodes
for x, y, label, hit, leaf in positions:
    if hit:
        nc = MIA_BLUE if not leaf else (MIA_WARM if leaf == '阿嬤的豆漿' else MIA_BLUE)
        fc = nc + '33'
        ec = nc
        text_c = nc
    else:
        fc = GRID
        ec = MUTED
        text_c = MUTED

    radius = 0.38 if leaf is None else 0.42
    circle = plt.Circle((x, y), radius, facecolor=fc, edgecolor=ec,
                         linewidth=2.0 if hit else 1.0, zorder=2)
    ax.add_patch(circle)
    fontsize = 8.5 if len(label) <= 3 else 7.0
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fontsize, color=text_c, fontweight='bold', zorder=3)

    # Leaf annotation
    if leaf:
        if leaf == '阿嬤的豆漿':
            ax.annotate(f'{leaf}\nJX-2079-10-28-003',
                        xy=(x, y - radius), xytext=(x + 0.8, y - 1.1),
                        fontsize=9, color=MIA_WARM, fontweight='bold',
                        ha='center', va='top',
                        arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.8),
                        zorder=4,
                        bbox=dict(boxstyle='round,pad=0.3',
                                  facecolor=MIA_WARM + '22', edgecolor=MIA_WARM))
        else:
            ax.text(x, y - radius - 0.25, leaf, ha='center', va='top',
                    fontsize=6.5, color=MUTED, style='italic', zorder=3)

# ── Search path annotation ──
ax.text(0.3, 0.5, '搜尋前綴：JX-2079-10-28-003',
        fontsize=10, color=MIA_WARM, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor=GRID, edgecolor=MIA_WARM))
ax.text(0.3, -0.35, '每一步只走匹配的分支\n18 步 → 1 段記憶',
        fontsize=8.5, color=TEXT, va='top')

# Axes
ax.set_xlim(-0.5, 16.5)
ax.set_ylim(-9.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=MIA_WARM + '55', edgecolor=MIA_WARM,
                   label='匹配路徑（前綴命中）'),
    mpatches.Patch(facecolor=MIA_BLUE + '33', edgecolor=MIA_BLUE,
                   label='路徑上的節點'),
    mpatches.Patch(facecolor=GRID, edgecolor=MUTED,
                   label='未匹配分支'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol3_16_Trie.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
