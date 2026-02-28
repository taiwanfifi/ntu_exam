"""
米亞的演算法筆記 #22 — NP-Complete 視覺化
《記憶駭客》第259章、第312-316章：終局

「差別不是聰明。是接受不完美。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

# ── Color Palette ──
DARK_BG  = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT     = '#d0d7de'
MUTED    = '#6e7681'
GRID     = '#1c2028'
RED      = '#ff6b6b'
GREEN    = '#7bc87b'

# ── Chinese Font ──
for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.family'] = font
        break
    except Exception:
        continue

plt.rcParams.update({
    'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG,
    'axes.edgecolor': MUTED,
})

# ── Layout ──
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.25,
                      left=0.05, right=0.96, top=0.86, bottom=0.08)
ax_venn = fig.add_subplot(gs[0, 0])   # left: P/NP/NP-Hard/NPC Euler diagram
ax_approx = fig.add_subplot(gs[0, 1]) # right: 95% approximation curve

fig.suptitle('米亞的演算法筆記 #22 — NP-Complete\n「完美解不存在。但足夠好存在。」',
             fontsize=15, color=MIA_BLUE, fontweight='bold', y=0.96)
fig.text(0.5, 0.895, '「差別不是聰明。是接受不完美。」— 第316章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ═══ LEFT: P/NP/NP-Hard/NPC Euler diagram ═══
ax_venn.set_xlim(-4, 5.5); ax_venn.set_ylim(-3.5, 4); ax_venn.axis('off')
ax_venn.set_title('P, NP, NP-Hard, NP-Complete 關係圖', fontsize=12, color=TEXT, pad=10)

# Ellipses: NP-Hard, NP, P, NPC
for params in [((1.8, 0.3), 6.5, 6.0, -5, RED+'15', RED, '--'),
               ((-0.3, 0), 5.5, 5.5, 0, MIA_BLUE+'15', MIA_BLUE, '-'),
               ((-1.2, -0.5), 2.8, 2.5, 0, GREEN+'25', GREEN, '-'),
               ((1.5, 0.1), 2.0, 2.2, 10, MIA_WARM+'35', MIA_WARM, '-')]:
    ctr, w, h, ang, fc, ec, ls = params
    lw = 2.5 if ec == MIA_WARM else 2
    ax_venn.add_patch(mpatches.Ellipse(ctr, w, h, angle=ang,
                      fc=fc, ec=ec, lw=lw, ls=ls))

ax_venn.text(4.2, 2.8, 'NP-Hard', fontsize=12, color=RED, fontweight='bold', ha='center')
ax_venn.text(-2.3, 2.2, 'NP', fontsize=13, color=MIA_BLUE, fontweight='bold', ha='center')
ax_venn.text(-2.3, 1.6, '能快速驗證', fontsize=8, color=MIA_BLUE, ha='center')
ax_venn.text(-1.2, -0.2, 'P', fontsize=14, color=GREEN, fontweight='bold', ha='center')
ax_venn.text(-1.2, -0.8, '能快速解決', fontsize=8, color=GREEN, ha='center')
ax_venn.text(1.5, 0.4, 'NPC', fontsize=14, color=MIA_WARM, fontweight='bold', ha='center')
ax_venn.text(1.5, -0.2, 'NP ∩ NP-Hard', fontsize=8, color=MIA_WARM, ha='center')

examples = [
    (-1.5, -1.5, '排序\nBinary Search', GREEN, 8),
    (-0.3, 1.0, '圖著色驗證', MIA_BLUE, 7),
    (1.2, -0.7, 'SAT\nTSP\n記憶修復', MIA_WARM, 7),
    (3.8, -0.8, '停機問題', RED, 7),
    (4.0, 0.5, 'NP-Hard\n但不在 NP', RED, 7),
]
for ex, ey, etxt, ecol, esz in examples:
    ax_venn.text(ex, ey, etxt, fontsize=esz, color=ecol, ha='center',
                 va='center', style='italic',
                 bbox=dict(boxstyle='round,pad=0.2', fc=DARK_BG + 'cc',
                           ec=ecol + '44', lw=0.5))
ax_venn.annotate('P =? NP\n千禧年難題', xy=(-0.5, 0.8), xytext=(-3.3, 3.2),
                 fontsize=9, color=MUTED, ha='center',
                 arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, ls='--'))
ax_venn.text(0.5, -3.3,
             '如果 P = NP，黃色區域坍縮進綠色\n'
             '如果 P ≠ NP，完美解永遠不可快速求得',
             ha='center', fontsize=8, color=MUTED, style='italic')

# ═══ RIGHT: Approximation curve — 95% vs 100% ═══
ax_approx.set_title('選項 C：近似解 vs 完美解', fontsize=12, color=TEXT, pad=10)
x_time = np.linspace(0, 10, 300)
approx_curve = 95 * (1 - np.exp(-0.6 * x_time))  # Greedy: plateau at 95%
ax_approx.fill_between(x_time, 0, approx_curve, alpha=0.15, color=MIA_BLUE)
ax_approx.plot(x_time, approx_curve, color=MIA_BLUE, lw=2.5,
               label='近似解（Greedy）')
# 95% and 100% reference lines
ax_approx.axhline(y=95, color=MIA_WARM, lw=1.5, ls='--', alpha=0.7)
ax_approx.text(10.2, 95, '95%', fontsize=11, color=MIA_WARM, fontweight='bold', va='center')
ax_approx.text(6.5, 96.5, '「足夠好」', fontsize=10, color=MIA_WARM, style='italic')
ax_approx.axhline(y=100, color=RED, lw=2, ls=':', alpha=0.5)
ax_approx.text(10.2, 100, '100%', fontsize=11, color=RED, fontweight='bold', va='center')
ax_approx.text(6.5, 101.5, '完美（不可達）', fontsize=10, color=RED, style='italic')
ax_approx.fill_between([0, 10], 95, 100, alpha=0.08, color=RED)
ax_approx.text(5, 97.5, '5% 的不完美', fontsize=9, color=RED, ha='center', alpha=0.8)
# Time markers
ax_approx.axvline(x=6.5, color=GREEN, lw=1, ls='--', alpha=0.5)
ax_approx.text(6.5, -5, '67 小時\n2400 節點並行', fontsize=8, color=GREEN, ha='center')
ax_approx.annotate('精確解所需時間\n→ 宇宙熱寂之後',
                   xy=(9.5, 100), xytext=(8, 108),
                   fontsize=9, color=RED, ha='center',
                   arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

ax_approx.set_xlabel('計算時間', fontsize=10)
ax_approx.set_ylabel('記憶修復覆蓋率 (%)', fontsize=10)
ax_approx.set_xlim(0, 10.5); ax_approx.set_ylim(-18, 112)
ax_approx.set_xticks([]); ax_approx.set_yticks([0, 20, 40, 60, 80, 95, 100])
ax_approx.tick_params(colors=MUTED); ax_approx.grid(True, color=GRID, lw=0.5, alpha=0.5)

stats_text = ('選項 C 統計\n───────────\n570 萬人  完全修復\n'
              ' 28.5 萬人  輕微模糊\n  1.5 萬人  顯著缺口\n'
              '───────────\n「夠了。」— 語青')
ax_approx.text(1.8, 75, stats_text, fontsize=9, color=TEXT,
               va='top', bbox=dict(boxstyle='round,pad=0.5', fc=GRID, ec=MIA_WARM,
                                   lw=1.5, alpha=0.9))
# Novel journey at bottom
vol_labels = [(0.8, -12, 'Vol1\nP 的世界\n排好就好', GREEN),
              (3.5, -12, 'Vol2\nNP 的世界\n能驗證真相', MIA_BLUE),
              (6.2, -12, 'Vol3\n建造堡壘\n系統設計', '#c49cde'),
              (9.0, -12, 'Vol4\nNPC\n接受不完美', MIA_WARM)]
for vx, vy, vtxt, vc in vol_labels:
    ax_approx.text(vx, vy, vtxt, fontsize=7.5, color=vc, ha='center', va='top', fontweight='bold')
for i in range(3):
    ax_approx.annotate('', xy=(vol_labels[i+1][0]-0.8, -12), xytext=(vol_labels[i][0]+0.8, -12),
                       arrowprops=dict(arrowstyle='->', color=MUTED, lw=1))

legend_elements = [mpatches.Patch(fc=MIA_BLUE+'55', ec=MIA_BLUE, label='近似解覆蓋率'),
                   mpatches.Patch(fc=RED+'33', ec=RED, label='不可達的完美'),
                   mpatches.Patch(fc=MIA_WARM+'55', ec=MIA_WARM, label='95%「足夠好」')]
ax_approx.legend(handles=legend_elements, loc='upper left', fontsize=8,
                 frameon=True, facecolor=DARK_BG, edgecolor=MUTED, labelcolor=TEXT)

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol4_22_NP_Complete.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
