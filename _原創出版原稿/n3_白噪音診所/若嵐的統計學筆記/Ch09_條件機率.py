"""
白噪音診所 — 若嵐的統計學筆記 #09
條件機率 Conditional Probability

翔宇科技（哲宇）∩ 博雅國際（維誠）→ Resonance Analytics 客戶
P(出事 | Resonance) >> P(出事 | 非 Resonance)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import numpy as np

# ── 字體 ──────────────────────────────────────────
for font_name in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'STHeiti']:
    try:
        fm.findfont(font_name, fallback_to_default=False)
        plt.rcParams['font.family'] = font_name
        break
    except:
        continue

# ── 全域風格 ────────────────────────────────────
BG     = '#0c1018'
TEXT   = '#d0d7de'
MUTED  = '#6e7681'
GRID   = '#1c2028'
RED    = '#ff6b6b'
BLUE   = '#64b5f6'
PURPLE = '#ce93d8'
AMBER  = '#ffb74d'
GREEN  = '#81c784'
WHITE  = '#e0e0e0'
GREY   = '#555555'

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor':   BG,
    'text.color':       TEXT,
    'axes.labelcolor':  TEXT,
    'xtick.color':      MUTED,
    'ytick.color':      MUTED,
    'axes.edgecolor':   '#2d333b',
    'font.size':        11,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))
fig.patch.set_facecolor(BG)

# ──────────────────────────────────────────────────
# 左圖：手繪 Venn 圖
# ──────────────────────────────────────────────────
ax1.set_xlim(-1, 11)
ax1.set_ylim(-1, 9)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_facecolor(BG)

# 左圓：翔宇科技（哲宇）
cA = plt.Circle((3.5, 4.3), 2.8, color=BLUE, alpha=0.18, zorder=2)
cA_edge = plt.Circle((3.5, 4.3), 2.8, fill=False, edgecolor=BLUE,
                      linewidth=2.0, alpha=0.75, zorder=3)
ax1.add_patch(cA)
ax1.add_patch(cA_edge)

# 右圓：博雅國際（維誠）
cB = plt.Circle((6.5, 4.3), 2.8, color=RED, alpha=0.18, zorder=2)
cB_edge = plt.Circle((6.5, 4.3), 2.8, fill=False, edgecolor=RED,
                      linewidth=2.0, alpha=0.75, zorder=3)
ax1.add_patch(cB)
ax1.add_patch(cB_edge)

# 標籤
ax1.text(2.0, 7.5, '翔宇科技\n（哲宇）', ha='center', fontsize=10.5,
         color=BLUE, fontweight='bold', linespacing=1.4)
ax1.text(8.0, 7.5, '博雅國際\n（維誠）', ha='center', fontsize=10.5,
         color=RED, fontweight='bold', linespacing=1.4)

# 交集標籤
ax1.text(5.0, 4.3, 'Resonance\nAnalytics\n客戶',
         ha='center', va='center', fontsize=9.5,
         color=AMBER, fontweight='bold', linespacing=1.4,
         zorder=5)

# 非交集區域文字
ax1.text(2.4, 3.5, '獨立客戶\n（低風險）', ha='center', fontsize=8.5,
         color=BLUE, alpha=0.65, linespacing=1.4)
ax1.text(7.6, 3.5, '獨立客戶\n（低風險）', ha='center', fontsize=8.5,
         color=RED, alpha=0.65, linespacing=1.4)

# 條件機率標注
prob_box = ('P(出事 | Resonance) ≈ 0.0025\n'
            'P(出事 | 非 Resonance) ≈ 10^(-10)\n\n'
            '差了 500 萬倍')
ax1.text(5.0, 1.1, prob_box,
         ha='center', fontsize=9.5, color=AMBER, linespacing=1.6,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#1a1408',
                   edgecolor=AMBER, alpha=0.82, linewidth=1.0))

# 連接箭頭（交集 → 機率框）
ax1.annotate('', xy=(5.0, 1.85), xytext=(5.0, 3.0),
             arrowprops=dict(arrowstyle='->', color=AMBER,
                             lw=1.4, alpha=0.7))

ax1.set_title('條件機率與交集事件', fontsize=13, color=WHITE,
              fontweight='bold', pad=8)

# ──────────────────────────────────────────────────
# 右圖：對數尺度條形圖（條件 vs 無條件）
# ──────────────────────────────────────────────────
labels = ['P(A∩B)\n無條件', 'P(A∩B | Resonance)\n給定條件']
vals   = [1e-10, 0.0025]
colors_bar = [RED, AMBER]
x_pos  = [0, 1]

ax2.bar(x_pos, vals, color=colors_bar, alpha=0.82, width=0.45, zorder=3,
        edgecolor='#0c1018', linewidth=0.6)

# 數值標注
ax2.text(0, vals[0] * 3.5, '≈ 10^(-10)', ha='center', va='bottom',
         fontsize=10.5, color=RED, fontweight='bold')
ax2.text(1, vals[1] * 1.8, f'≈ 0.0025', ha='center', va='bottom',
         fontsize=10.5, color=AMBER, fontweight='bold')

ax2.set_yscale('log')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, fontsize=10.5)
ax2.set_ylim(1e-12, 0.1)
ax2.set_ylabel('機率值（對數尺度）', fontsize=11, labelpad=8)
ax2.set_title('條件如何改變機率', fontsize=13, color=WHITE,
              fontweight='bold', pad=12)
ax2.grid(True, axis='y', color=GRID, alpha=0.5, linewidth=0.5, zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# 「差了 500 萬倍」標注
ax2.annotate('', xy=(1, 0.002), xytext=(0, 5e-11),
             arrowprops=dict(arrowstyle='->', color=GREEN,
                             lw=1.4, connectionstyle='arc3,rad=-0.35'))
ax2.text(0.5, 5e-5, '差了\n500 萬倍', ha='center', fontsize=11,
         color=GREEN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#0d1e0d',
                   edgecolor=GREEN, alpha=0.8, linewidth=0.9))

# log 軸刻度顏色修正
ax2.yaxis.set_tick_params(which='both', color=MUTED, labelcolor=MUTED)

# ──────────────────────────────────────────────────
# 底部引文
# ──────────────────────────────────────────────────
fig.text(0.5, 0.01,
         '「你以為你在調查。但也許，你只是別人的條件變數裡的一個事件。」',
         ha='center', fontsize=11.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.55', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

fig.suptitle('條件機率：已知條件下的機率更新', fontsize=16, color=WHITE,
             fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0.07, 1, 0.94])

SAVE = '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch09_條件機率.png'
plt.savefig(SAVE, dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'✓ 已儲存：{SAVE}')
