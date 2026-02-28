"""
白噪音診所 — 若嵐的統計學筆記 #12
倖存者偏差 Survivorship Bias

你看到的飛機，是飛回來的飛機。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# Style constants
BG = '#0c1018'
RED = '#ff6b6b'
BLUE = '#64b5f6'
PURPLE = '#ce93d8'
AMBER = '#ffb74d'
GREEN = '#81c784'
WHITE = '#e0e0e0'
GREY = '#555555'

plt.rcParams.update({
    'font.family': ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'STHeiti'],
    'axes.facecolor': BG,
    'figure.facecolor': BG,
    'text.color': WHITE,
    'axes.labelcolor': WHITE,
    'xtick.color': WHITE,
    'ytick.color': WHITE,
    'font.size': 11,
})

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor(BG)

# ── LEFT PANEL: Airplane grid with bullet holes ─────────────────────────
ax_left.set_facecolor(BG)
ax_left.set_xlim(0, 4)
ax_left.set_ylim(0, 3)
ax_left.set_aspect('equal')
ax_left.axis('off')

# Draw airplane sections as a grid (4 columns x 3 rows)
# Layout:
#   Row 2 (top):    [0,2]=機頭/cockpit  [1,2]=左翼前  [2,2]=右翼前  [3,2]=尾翼
#   Row 1 (mid):    [0,1]=機身左        [1,1]=引擎左   [2,1]=引擎右  [3,1]=機身右
#   Row 0 (bot):    [0,0]=機腹左        [1,0]=左翼後  [2,0]=右翼後  [3,0]=機尾

section_labels = [
    ['機腹左', '左翼後', '右翼後', '機尾'],
    ['機身左', '引擎左', '引擎右', '機身右'],
    ['機頭', '左翼前', '右翼前', '尾翼'],
]

# Sections that are critical (no bullet holes should be here - if hit, plane doesn't return)
critical_sections = {(0, 2), (1, 1), (2, 1)}  # 機頭, 引擎左, 引擎右

# Bullet hole counts per section (row, col)
bullet_counts = {
    (0, 0): 3, (0, 1): 5, (0, 2): 4, (0, 3): 2,
    (1, 0): 4, (1, 1): 0, (1, 2): 0, (1, 3): 3,
    (2, 0): 0, (2, 1): 3, (2, 2): 3, (2, 3): 2,
}

rng = np.random.default_rng(42)

for row in range(3):
    for col in range(4):
        x0, y0 = col, row
        is_critical = (col, row) in critical_sections
        edge_color = AMBER if is_critical else GREY
        lw = 2.0 if is_critical else 0.8
        rect = mpatches.FancyBboxPatch(
            (x0 + 0.05, y0 + 0.05), 0.9, 0.9,
            boxstyle='round,pad=0.05',
            facecolor='#12181f' if not is_critical else '#1a1408',
            edgecolor=edge_color, linewidth=lw
        )
        ax_left.add_patch(rect)

        # Label
        label = section_labels[row][col]
        ax_left.text(x0 + 0.5, y0 + 0.82, label,
                     ha='center', va='center', fontsize=8,
                     color=AMBER if is_critical else '#666666')

        # Bullet holes
        n_holes = bullet_counts.get((col, row), 0)
        if n_holes > 0:
            xs = rng.uniform(x0 + 0.15, x0 + 0.85, n_holes)
            ys = rng.uniform(y0 + 0.15, y0 + 0.65, n_holes)
            ax_left.scatter(xs, ys, s=40, color=RED, zorder=5,
                            edgecolors='#ff000077', linewidth=0.5)

# Amber annotation arrows for critical sections
# Arrow to 機頭 (col=0, row=2) -> center at (0.5, 2.5)
ax_left.annotate('加固這裡\n被擊中的\n飛不回來',
                 xy=(0.5, 2.5), xytext=(-0.05, 3.25),
                 fontsize=8.5, color=AMBER, ha='center',
                 arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1408',
                           edgecolor=AMBER, alpha=0.85))

# Arrow to 引擎左 (col=1, row=1) -> center at (1.5, 1.5)
ax_left.annotate('加固這裡',
                 xy=(1.5, 1.5), xytext=(1.5, -0.4),
                 fontsize=8.5, color=AMBER, ha='center',
                 arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1408',
                           edgecolor=AMBER, alpha=0.85))

# Arrow to 引擎右 (col=2, row=1) -> center at (2.5, 1.5)
ax_left.annotate('加固這裡',
                 xy=(2.5, 1.5), xytext=(2.5, -0.4),
                 fontsize=8.5, color=AMBER, ha='center',
                 arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1408',
                           edgecolor=AMBER, alpha=0.85))

ax_left.set_title('你看到的是飛回來的飛機', fontsize=14, color=WHITE, pad=18)

# Legend
red_dot = mpatches.Patch(color=RED, label='彈孔（倖存飛機）')
amber_box = mpatches.Patch(color=AMBER, label='空白 = 致命區域（從未歸來）')
ax_left.legend(handles=[red_dot, amber_box], loc='lower center',
               fontsize=8.5, facecolor='#12181f', edgecolor=GREY,
               labelcolor=WHITE, bbox_to_anchor=(2.0, -0.15))

# ── RIGHT PANEL: Survivorship bias in sampling ───────────────────────────
ax_right.set_facecolor(BG)
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
ax_right.spines['left'].set_color(GREY)
ax_right.spines['bottom'].set_color(GREY)

x = np.linspace(-4, 6, 500)

# Full male population: N(2.5, 1.2)
mu_all, sigma_all = 2.5, 1.2
y_all = (1 / (sigma_all * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_all) / sigma_all) ** 2)

# High-social-scene visible: N(0.5, 1.4) — shifted left (less loyal)
mu_vis, sigma_vis = 0.5, 1.4
y_vis = (1 / (sigma_vis * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_vis) / sigma_vis) ** 2)

ax_right.fill_between(x, y_all, alpha=0.15, color=BLUE)
ax_right.plot(x, y_all, color=BLUE, linewidth=2.0, label='全體男性 忠誠度分布')

ax_right.fill_between(x, y_vis, alpha=0.15, color=RED)
ax_right.plot(x, y_vis, color=RED, linewidth=2.0, label='高社交場景可見者 忠誠度分布')

# Threshold line (方靜宜's threshold)
threshold = 1.2
ax_right.axvline(x=threshold, color=PURPLE, linewidth=1.5, linestyle='--', alpha=0.8)
ax_right.text(threshold + 0.1, 0.28, '方靜宜的\n判斷閾值',
              fontsize=9, color=PURPLE, va='center')

# Mu markers
ax_right.axvline(x=mu_all, color=BLUE, linewidth=1.0, linestyle=':', alpha=0.6)
ax_right.text(mu_all + 0.1, 0.34, f'μ = {mu_all}', fontsize=8.5, color=BLUE)

ax_right.axvline(x=mu_vis, color=RED, linewidth=1.0, linestyle=':', alpha=0.6)
ax_right.text(mu_vis - 0.9, 0.30, f'μ = {mu_vis}', fontsize=8.5, color=RED)

# Annotation
ax_right.annotate('取樣偏差：\n她只看到紅色的',
                  xy=(mu_vis, 0.20), xytext=(3.2, 0.25),
                  fontsize=9.5, color=AMBER,
                  arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.3),
                  bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1408',
                            edgecolor=AMBER, alpha=0.85))

ax_right.set_xlabel('忠誠度指數', fontsize=11, labelpad=10)
ax_right.set_ylabel('機率密度', fontsize=11, labelpad=10)
ax_right.set_title('樣本空間的偏差', fontsize=14, color=WHITE, pad=14)
ax_right.legend(fontsize=9, facecolor='#12181f', edgecolor=GREY, labelcolor=WHITE,
                loc='upper right')
ax_right.set_xlim(-4, 6)
ax_right.set_ylim(0, 0.42)
ax_right.tick_params(colors=GREY)

# ── Title and quote ──────────────────────────────────────────────────────
fig.suptitle('倖存者偏差  Survivorship Bias',
             fontsize=18, color=WHITE, fontweight='bold', y=0.97)

fig.text(0.5, 0.02,
         '「你看到的飛機，是飛回來的飛機。」',
         ha='center', fontsize=12, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.95])
plt.savefig(
    '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch12_倖存者偏差.png',
    dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none'
)
print("saved Ch12_倖存者偏差.png")
