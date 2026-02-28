"""
白噪音診所 — 若嵐的統計學筆記 #46
大數法則 Law of Large Numbers

當 n → ∞，真相浮現
公平骰子的累積平均收斂到 3.5
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
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
BG = '#0c1018'
TEXT = '#d0d7de'
MUTED = '#6e7681'
GRID = '#1c2028'
RED = '#ff6b6b'
BLUE = '#64b5f6'
BLUE2 = '#90caf9'
PURPLE = '#ce93d8'
AMBER = '#ffb74d'

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': BG,
    'text.color': TEXT,
    'axes.labelcolor': TEXT,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'axes.edgecolor': '#2d333b',
    'font.size': 11,
})

fig, ax = plt.subplots(figsize=(14, 7.5))

np.random.seed(2024)

n_max = 5000
true_mean = 3.5

# ── 收斂包絡線 (±1/√n) ───────────────────────────
n_range = np.arange(1, n_max + 1)
envelope_upper = true_mean + 1.0 / np.sqrt(n_range)
envelope_lower = true_mean - 1.0 / np.sqrt(n_range)

ax.fill_between(n_range, envelope_lower, envelope_upper,
                color=BLUE, alpha=0.06, label='收斂帶 (±1/√n)')

# 包絡線邊緣
ax.plot(n_range, envelope_upper, color=BLUE, linewidth=0.8,
        linestyle=':', alpha=0.3)
ax.plot(n_range, envelope_lower, color=BLUE, linewidth=0.8,
        linestyle=':', alpha=0.3)

# ── 五條模擬路徑 ──────────────────────────────────
path_colors = [BLUE, AMBER, RED, PURPLE, '#66bb6a']
path_labels = ['路徑 1', '路徑 2', '路徑 3', '路徑 4', '路徑 5']

for color, label in zip(path_colors, path_labels):
    rolls = np.random.randint(1, 7, size=n_max)
    running_mean = np.cumsum(rolls) / n_range
    ax.plot(n_range, running_mean, color=color, linewidth=1.0,
            alpha=0.6, label=label)

# ── 真實均值線 ────────────────────────────────────
ax.axhline(y=true_mean, color=AMBER, linewidth=2, linestyle='--', alpha=0.7)
ax.text(n_max * 0.98, true_mean + 0.04, f'E[X] = {true_mean}',
        fontsize=12, color=AMBER, fontweight='bold', ha='right',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                 edgecolor=AMBER, alpha=0.85, linewidth=0.8))

# ── 區域標籤 ──────────────────────────────────────
# 左側：個體是隨機的
ax.text(150, 4.8, '個體是隨機的',
        fontsize=14, color=RED, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0f0f',
                 edgecolor=RED, alpha=0.6, linewidth=0.8))
ax.annotate('', xy=(50, 4.6), xytext=(250, 4.6),
            arrowprops=dict(arrowstyle='<->', color=RED, alpha=0.4, lw=1.2))

# 右側：群體是確定的
ax.text(4200, 3.58, '群體是確定的',
        fontsize=14, color=BLUE2, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0d1520',
                 edgecolor=BLUE2, alpha=0.6, linewidth=0.8))
ax.annotate('', xy=(3500, 3.55), xytext=(4900, 3.55),
            arrowprops=dict(arrowstyle='<->', color=BLUE2, alpha=0.4, lw=1.2))

# ── 公式標注 ──────────────────────────────────────
formula = r'$\bar{X}_n \rightarrow \mu$  as  $n \to \infty$'
ax.text(0.97, 0.88, formula,
        transform=ax.transAxes, fontsize=14, color=MUTED,
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                 edgecolor='#2d333b', alpha=0.85, linewidth=0.8))

# ── 軸 ───────────────────────────────────────────
ax.set_xlim(1, n_max)
ax.set_ylim(1.5, 5.5)
ax.set_xlabel('樣本數 n', fontsize=13, labelpad=12)
ax.set_ylabel('累積平均', fontsize=13, labelpad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='both', color=GRID, alpha=0.4, linewidth=0.5)
ax.legend(loc='lower right', fontsize=9, framealpha=0.3, ncol=2,
          edgecolor='#2d333b', facecolor='#161b22')

# ── 標題 ──────────────────────────────────────────
fig.suptitle('大數法則：當 n → ∞，真相浮現',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.96)
ax.set_title('「公平骰子的六面，終將收斂於 3.5。」',
             fontsize=10.5, color=MUTED, style='italic', pad=14)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.015,
         '你不需要是均值。你只需要是樣本裡的一個點。',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.93])
plt.savefig('Ch46_大數法則.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch46_大數法則.png")
