"""
白噪音診所 — 若嵐的統計學筆記 #42
隨機漫步 Random Walk

一維隨機漫步：每一條路都會回來
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

# ── 五條隨機漫步 ──────────────────────────────────
n_steps = 500
walk_colors = [BLUE, AMBER, RED, PURPLE, '#66bb6a']
walk_labels = ['路徑 α', '路徑 β', '路徑 γ', '路徑 δ', '路徑 ε']

for i, (color, label) in enumerate(zip(walk_colors, walk_labels)):
    steps = np.random.choice([-1, 1], size=n_steps)
    walk = np.cumsum(steps)
    walk = np.insert(walk, 0, 0)  # 從原點開始
    t = np.arange(len(walk))

    ax.plot(t, walk, color=color, linewidth=1.2, alpha=0.65, label=label)

    # 找出回到零點的位置
    zero_crossings = np.where(walk == 0)[0]
    if len(zero_crossings) > 1:
        # 排除起點，只標後續回零點
        zc = zero_crossings[1:]
        ax.scatter(zc, np.zeros(len(zc)), s=18, color=color,
                   alpha=0.7, zorder=4, edgecolors='none')

# ── 原點水平線 ────────────────────────────────────
ax.axhline(y=0, color=TEXT, linewidth=1.2, linestyle='--', alpha=0.3)
ax.text(n_steps * 0.98, 1.5, 'y = 0（原點）',
        fontsize=9, color=MUTED, ha='right', style='italic')

# ── 數學定理標注 ──────────────────────────────────
ax.annotate('P(回到原點) = 1',
            xy=(250, 0), xytext=(350, 22),
            fontsize=14, color=AMBER, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=AMBER, alpha=0.5,
                           connectionstyle='arc3,rad=0.2', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                     edgecolor=AMBER, alpha=0.85, linewidth=1.0))

ax.text(355, 17, '（一維對稱隨機漫步的遞迴性）',
        fontsize=8.5, color=MUTED, style='italic')

# ── 文學標注 ──────────────────────────────────────
ax.text(0.03, 0.92, '迷路的人終將回家',
        transform=ax.transAxes, fontsize=13, color=RED,
        fontweight='bold', style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0f0f',
                 edgecolor=RED, alpha=0.7, linewidth=0.8))

# ── 零穿越標記說明 ────────────────────────────────
ax.text(0.03, 0.05, '小圓點 = 回到原點的瞬間',
        transform=ax.transAxes, fontsize=9, color=MUTED,
        style='italic')

# ── 軸 ───────────────────────────────────────────
ax.set_xlim(0, n_steps)
ax.set_xlabel('步數 (t)', fontsize=13, labelpad=12)
ax.set_ylabel('位置', fontsize=13, labelpad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='both', color=GRID, alpha=0.4, linewidth=0.5)
ax.legend(loc='upper right', fontsize=9, framealpha=0.3,
          edgecolor='#2d333b', facecolor='#161b22', ncol=1)

# ── 標題 ──────────────────────────────────────────
fig.suptitle('一維隨機漫步：每一條路都會回來',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.96)
ax.set_title('「漫步不是迷路。是尋找。」',
             fontsize=10.5, color=MUTED, style='italic', pad=14)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.015,
         '87% 是軌道。10% 是自由意志。',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.93])
plt.savefig('Ch42_隨機漫步.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch42_隨機漫步.png")
