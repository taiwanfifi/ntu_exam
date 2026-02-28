"""
白噪音診所 — 若嵐的統計學筆記 #39
蒙地卡羅 Monte Carlo Simulation

在黑暗裡投一百萬次骰子
左：虛無假設下的交叉相關分布 vs 觀測值
右：蒙地卡羅估計圓周率
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

np.random.seed(2024)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5),
                                gridspec_kw={'width_ratios': [5, 4]})

# ══════════════════════════════════════════════════
# 左圖：虛無假設下的交叉相關分布
# ══════════════════════════════════════════════════

n_sim = 100_000
null_dist = np.random.normal(0.02, 0.06, n_sim)
observed = 0.847

# 直方圖
counts, bins, patches = ax1.hist(null_dist, bins=120, range=(-0.25, 0.35),
                                  color=BLUE, alpha=0.7, edgecolor='none',
                                  density=True)

# 為直方圖的 bin 上色（越接近邊緣越暗）
for patch, b in zip(patches, bins[:-1]):
    if b > 0.25:
        patch.set_alpha(0.3)

# 觀測值紅線（需要把 xlim 擴大才看得到）
ax1.axvline(x=observed, color=RED, linewidth=2.5, linestyle='-', alpha=0.9,
            zorder=5)

# 觀測值標注
ax1.annotate(f'觀測值 = {observed}',
            xy=(observed, 0.5), xytext=(0.62, 5.0),
            fontsize=12, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=RED, alpha=0.7, lw=2,
                           connectionstyle='arc3,rad=-0.1'),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0f0f',
                     edgecolor=RED, alpha=0.85, linewidth=1.0))

ax1.text(0.62, 4.0, '一百萬次模擬\n沒有一次超過 0.35',
         fontsize=9.5, color=AMBER, style='italic', linespacing=1.4,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#161b22',
                  edgecolor=AMBER, alpha=0.7, linewidth=0.6))

# 虛無假設標注
ax1.text(0.02, 6.5, r'$H_0$ 分布' + '\nμ=0.02, σ=0.06',
         fontsize=10, color=BLUE2, ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#161b22',
                  edgecolor='#2d333b', alpha=0.85))

# p 值標注
ax1.text(0.05, 0.88, 'p < 0.000001',
         transform=ax1.transAxes, fontsize=11, color=RED,
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a0f0f',
                  edgecolor=RED, alpha=0.7, linewidth=0.8))

ax1.set_xlim(-0.25, 0.95)
ax1.set_xlabel('交叉相關係數', fontsize=12, labelpad=10)
ax1.set_ylabel('機率密度', fontsize=12, labelpad=10)
ax1.set_title('虛無假設下的模擬分布', fontsize=13, color=TEXT, pad=12)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, axis='y', color=GRID, alpha=0.4, linewidth=0.5)

# ══════════════════════════════════════════════════
# 右圖：蒙地卡羅估計 π
# ══════════════════════════════════════════════════

n_points = 8000
x_pts = np.random.uniform(0, 1, n_points)
y_pts = np.random.uniform(0, 1, n_points)
dist = x_pts ** 2 + y_pts ** 2
inside = dist <= 1.0

# 圈內點（藍色）
ax2.scatter(x_pts[inside], y_pts[inside], s=1.5, color=BLUE,
            alpha=0.4, edgecolors='none')
# 圈外點（紅色）
ax2.scatter(x_pts[~inside], y_pts[~inside], s=1.5, color=RED,
            alpha=0.25, edgecolors='none')

# 四分之一圓弧
theta = np.linspace(0, np.pi / 2, 200)
ax2.plot(np.cos(theta), np.sin(theta), color=AMBER, linewidth=2, alpha=0.8)

# 估計值
pi_est = 4 * np.sum(inside) / n_points
ax2.text(0.5, 0.5, f'π ≈ {pi_est:.4f}',
         transform=ax2.transAxes, fontsize=16, color=AMBER,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                  edgecolor=AMBER, alpha=0.85, linewidth=1.0))

ax2.text(0.5, 0.38, f'n = {n_points:,} 個隨機點',
         transform=ax2.transAxes, fontsize=9.5, color=MUTED,
         ha='center', style='italic')

# 圖例
ax2.scatter([], [], s=25, color=BLUE, label='圈內（距離 ≤ 1）')
ax2.scatter([], [], s=25, color=RED, label='圈外（距離 > 1）')
ax2.legend(loc='upper right', fontsize=9, framealpha=0.3,
           edgecolor='#2d333b', facecolor='#161b22')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect('equal')
ax2.set_xlabel('x', fontsize=12, labelpad=10)
ax2.set_ylabel('y', fontsize=12, labelpad=10)
ax2.set_title('蒙地卡羅估計 π', fontsize=13, color=TEXT, pad=12)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(True, color=GRID, alpha=0.3, linewidth=0.5)

# ── 標題 ──────────────────────────────────────────
fig.suptitle('蒙地卡羅：在黑暗裡投一百萬次骰子',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.97)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.008,
         '如果世界是公平的，會發生這樣的事嗎？不會。',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
plt.savefig('Ch39_蒙地卡羅.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch39_蒙地卡羅.png")
