"""
米亞的演算法筆記 #15 — Backtracking 回溯法
《記憶駭客》第215-216章：語青意識碎片追蹤

「你不能剪掉那條記得你第一次牽手的路。」
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
PRUNED = '#3a3f47'

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

# ── Tree: (x, y, type, label) — type: R=root E=explored P=pruned D=dead F=fragment H=highlight
_E, _P, _D, _F, _H, _R = 'explored', 'pruned', 'dead', 'fragment', 'highlight', 'root'
nodes = {
    0: (0,10,_R,'ROOT'),
    1: (-6,8,_E,''),    2: (-1.5,8,_E,''),  3: (3,8,_P,''),     4: (6.5,8,_E,''),
    5: (-7.5,6,_D,''),  6: (-5.5,6,_E,''),  7: (-4,6,_P,''),
    8: (-2.5,6,_E,''),  9: (-0.5,6,_D,''),
    10:(2,6,_P,''),     11:(4,6,_P,''),
    12:(5.5,6,_E,''),   13:(7.5,6,_D,''),
    14:(-6.5,4,_D,''),  15:(-4.5,4,_F,'咖啡半匙糖'),
    16:(-3.5,4,_E,''),  17:(-1.5,4,_F,'星星偏 0.3°'),
    18:(4.5,4,_E,''),   19:(6.5,4,_D,''),
    20:(-4.5,2,_D,''),  21:(-2.5,2,_F,'畢業典禮的淚'),
    22:(3.5,2,_D,''),   23:(5.5,2,_H,''),
    24:(4.5,0,_D,''),   25:(6.5,0,_F,'第一次牽手\n36.2°C'),
}
edges = [(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,7),(2,8),(2,9),(3,10),(3,11),
         (4,12),(4,13),(6,14),(6,15),(8,16),(8,17),(12,18),(12,19),
         (16,20),(16,21),(18,22),(18,23),(23,24),(23,25)]
highlight_path = {(0,4),(4,12),(12,18),(18,23),(23,25)}

# Type → (facecolor, edgecolor, alpha)
type_styles = {
    _R: (MIA_BLUE, MIA_BLUE, 0.9), _E: (GRID, MUTED, 0.7),
    _P: (PRUNED, PRUNED, 0.3),     _D: (RED, RED, 0.2),
    _F: (MIA_BLUE, MIA_BLUE, 0.85),_H: (MIA_WARM, MIA_WARM, 0.7),
}

# ── Figure ──
fig, ax = plt.subplots(figsize=(16, 13))

fig.suptitle('Backtracking — 語青意識碎片追蹤搜尋樹',
             fontsize=17, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.94,
         '「你不能剪掉那條記得你第一次牽手的路。」— 第215章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Draw edges ──
for p, c in edges:
    px, py = nodes[p][0], nodes[p][1]
    cx, cy = nodes[c][0], nodes[c][1]
    if (p, c) in highlight_path:    col, lw, al = MIA_WARM, 3.0, 0.9
    elif nodes[c][2] == _P:         col, lw, al = PRUNED, 1.0, 0.3
    elif nodes[c][2] == _D:         col, lw, al = RED, 1.0, 0.25
    else:                           col, lw, al = MUTED, 1.5, 0.6
    ax.plot([px, cx], [py, cy], color=col, linewidth=lw, alpha=al, zorder=1)

# ── Draw nodes ──
for nid, (x, y, ntype, label) in nodes.items():
    fc, ec, al = type_styles[ntype]
    r = 0.45 if ntype == _F else 0.35
    if ntype == _F:  # glowing effect
        ax.add_patch(plt.Circle((x,y), r+0.15, fc=MIA_BLUE, alpha=0.15, ec='none', zorder=2))
        ax.add_patch(plt.Circle((x,y), r+0.08, fc=MIA_BLUE, alpha=0.25, ec='none', zorder=2))
    ax.add_patch(plt.Circle((x,y), r, fc=fc, ec=ec,
                 lw=1.5 if ntype!=_P else 0.8, alpha=al, zorder=3))
    if ntype == _D:
        ax.text(x, y, 'X', ha='center', va='center', fontsize=7,
                color=RED, fontweight='bold', alpha=0.5, zorder=4)
    if label and ntype in (_F, _R):
        yo = -1.0 if nid==25 else (-0.85 if ntype==_F else 0.65)
        co = MIA_WARM if nid==25 else (MIA_BLUE if ntype==_F else TEXT)
        ax.text(x, y+yo, label, ha='center', va='center',
                fontsize=9, color=co, fontweight='bold', zorder=4)

# ── Pruned subtree annotation ──
ax.annotate('剪枝 (pruned)\n碎片概率 < 1%',
            xy=(3.0, 7.5), xytext=(0.5, 11.0),
            fontsize=9, color=PRUNED, ha='center',
            arrowprops=dict(arrowstyle='->', color=PRUNED, lw=1.5))

# ── Refused-to-prune annotation ──
ax.annotate('維倫拒絕剪枝\n碎片概率 3.2%\n「你不能剪掉\n　那條路。」',
            xy=(5.5, 2.0), xytext=(8.5, 3.5),
            fontsize=10, color=MIA_WARM, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=2.5))

# ── Fragment count annotation ──
ax.text(-7.5, 0.5,
        '碎片搜索結果\n'
        '━━━━━━━━━━━\n'
        '總節點: 847\n'
        '已探索: 2,587\n'
        '已剪枝: ~28,000\n'
        '找到碎片: 23/23\n'
        '拒絕剪枝: 2 條路\n'
        '額外成本: +2 分鐘',
        fontsize=9, color=TEXT, va='top',
        family='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=GRID,
                  edgecolor=MUTED, alpha=0.8))

# ── Highlighted path label ──
ax.text(8.0, 0.0,
        '完整搜索路徑\nroot→4→12→18→23→碎片',
        fontsize=9, color=MIA_WARM, ha='center',
        style='italic')

# ── Bottom quote ──
ax.text(0.0, -1.5,
        '「一個都不想放棄。追的不是路——是她。」',
        ha='center', va='center', fontsize=12,
        color=MIA_WARM, style='italic')

ax.set_xlim(-9.5, 10)
ax.set_ylim(-2.5, 11.5)
ax.set_aspect('equal')
ax.axis('off')

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=MIA_BLUE, alpha=0.85, label='碎片 (fragment)'),
    mpatches.Patch(facecolor=GRID, edgecolor=MUTED, label='已探索 (explored)'),
    mpatches.Patch(facecolor=PRUNED, alpha=0.3, label='已剪枝 (pruned)'),
    mpatches.Patch(facecolor=RED, alpha=0.2, label='死路 (dead end)'),
    mpatches.Patch(facecolor=MIA_WARM, alpha=0.9, label='拒絕剪枝的路徑'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=5,
           fontsize=9, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol3_15_Backtracking.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
