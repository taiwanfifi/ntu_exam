"""
白噪音診所 — 若嵐的統計學筆記 #43
中央極限定理 Central Limit Theorem

保護自由，就是拒絕被平均。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

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

rng = np.random.default_rng(2025)
N = 100_000

# Simulate die rolls (uniform on 1..6)
single_die = rng.integers(1, 7, size=(N,))
avg_5     = rng.integers(1, 7, size=(N, 5)).mean(axis=1)
avg_30    = rng.integers(1, 7, size=(N, 30)).mean(axis=1)

datasets = [
    (single_die, 'n = 1　骰子單擲', 1.0, 6.0),
    (avg_5,      'n = 5　平均值',    1.0, 6.0),
    (avg_30,     'n = 30　平均值',   2.5, 4.5),
]

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(BG)

for ax, (data, title, x_lo, x_hi) in zip(axes, datasets):
    ax.set_facecolor(BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GREY)
    ax.spines['bottom'].set_color(GREY)
    ax.tick_params(colors=GREY)

    # Histogram
    n_bins = 30 if title.startswith('n = 1') else 50
    counts, bin_edges, patches = ax.hist(
        data, bins=n_bins, range=(x_lo, x_hi),
        density=True, color=BLUE, alpha=0.75,
        edgecolor='#0c1018', linewidth=0.4
    )

    # Fitted normal curve overlay
    mu_fit = data.mean()
    sigma_fit = data.std()
    x_fit = np.linspace(x_lo, x_hi, 400)
    y_fit = norm.pdf(x_fit, mu_fit, sigma_fit)
    ax.plot(x_fit, y_fit, color=AMBER, linewidth=2.0, zorder=5,
            label=f'正態擬合\nμ={mu_fit:.2f}, σ={sigma_fit:.2f}')

    # Mu vertical line
    ax.axvline(x=mu_fit, color=AMBER, linewidth=1.2, linestyle='--', alpha=0.6)

    ax.set_title(title, fontsize=13, color=WHITE, pad=12)
    ax.set_xlabel('平均值', fontsize=10, labelpad=8)
    ax.set_ylabel('機率密度', fontsize=10, labelpad=8)
    ax.set_xlim(x_lo, x_hi)
    ax.legend(fontsize=8.5, facecolor='#12181f', edgecolor=GREY, labelcolor=WHITE,
              loc='upper right' if title.startswith('n = 1') else 'upper center')
    ax.grid(True, axis='y', color='#1c2028', alpha=0.4, linewidth=0.5)

# Additional annotation on right panel
ax3 = axes[2]
sigma_expected = round(np.sqrt(35 / 12) / np.sqrt(30), 3)
ax3.text(2.55, ax3.get_ylim()[1] * 0.55,
         f'σ/√n = {sigma_expected}\n幾乎完美正態',
         fontsize=9, color=GREEN, linespacing=1.6,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#0e1f0e',
                   edgecolor=GREEN, alpha=0.75))

# ── Title and quote ──────────────────────────────────────────────────────
fig.suptitle('中央極限定理  Central Limit Theorem\n樣本數越大，平均值越趨向常態分布',
             fontsize=16, color=WHITE, fontweight='bold', y=0.97)

fig.text(0.5, 0.02,
         '「保護自由，就是拒絕被平均。」',
         ha='center', fontsize=12, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.94])
plt.savefig(
    '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch43_中央極限定理.png',
    dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none'
)
print("saved Ch43_中央極限定理.png")
