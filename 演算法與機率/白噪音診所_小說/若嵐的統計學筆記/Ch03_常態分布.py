"""
白噪音診所 — 若嵐的統計學筆記 #03
常態分布 Normal Distribution

許芷萱的遲到分布：一座精準的堡壘
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from scipy.stats import norm

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

# ── 參數 ──────────────────────────────────────────
mu = 3.12
sigma = 0.87

# ── 生成曲線 ──────────────────────────────────────
x = np.linspace(mu - 4.5 * sigma, mu + 4.5 * sigma, 1000)
y = norm.pdf(x, mu, sigma)

# ── 99.7% 區域 (3σ) ──────────────────────────────
x_3s = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 800)
y_3s = norm.pdf(x_3s, mu, sigma)
ax.fill_between(x_3s, y_3s, alpha=0.08, color='#1a73e8', label='99.7% (3σ)')

# ── 95% 區域 (2σ) ────────────────────────────────
x_2s = np.linspace(mu - 2 * sigma, mu + 2 * sigma, 600)
y_2s = norm.pdf(x_2s, mu, sigma)
ax.fill_between(x_2s, y_2s, alpha=0.13, color='#42a5f5', label='95% (2σ)')

# ── 68% 區域 (1σ) ────────────────────────────────
x_1s = np.linspace(mu - sigma, mu + sigma, 400)
y_1s = norm.pdf(x_1s, mu, sigma)
ax.fill_between(x_1s, y_1s, alpha=0.22, color=BLUE, label='68% (1σ)')

# ── 主曲線 ────────────────────────────────────────
ax.plot(x, y, color=BLUE, linewidth=2.5, alpha=0.9)

# ── 均值線 ────────────────────────────────────────
ax.axvline(x=mu, color=AMBER, linewidth=1.5, linestyle='--', alpha=0.7)
ax.text(mu + 0.08, max(y) * 1.02, f'μ = {mu}',
        fontsize=12, color=AMBER, fontweight='bold', ha='left')

# ── σ 標記線 ──────────────────────────────────────
for k, label_pct in [(1, '68%'), (2, '95%'), (3, '99.7%')]:
    left = mu - k * sigma
    right = mu + k * sigma
    y_level = -0.012 - k * 0.008
    # 橫向範圍箭頭
    ax.annotate('', xy=(right, y_level), xytext=(left, y_level),
                arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.2))
    ax.text(mu, y_level - 0.005, f'{label_pct}',
            fontsize=9.5, color=MUTED, ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=BG,
                     edgecolor='none', alpha=0.9))

# ── σ 刻度標記 ────────────────────────────────────
for k in range(1, 4):
    for sign, ha in [(-1, 'right'), (1, 'left')]:
        pos = mu + sign * k * sigma
        ax.plot([pos, pos], [0, norm.pdf(pos, mu, sigma)],
                color=MUTED, linewidth=0.8, linestyle=':', alpha=0.5)
        ax.text(pos, -0.005, f'{"+" if sign > 0 else "−"}{k}σ',
                fontsize=8.5, color=MUTED, ha='center')

# ── 紅色核心標注 ──────────────────────────────────
ax.annotate('均值三分鐘。那不是遲到。\n那是一座堡壘的厚度。',
            xy=(mu, max(y)), xytext=(mu + 2.0, max(y) * 0.75),
            fontsize=12, color=RED, fontweight='bold', linespacing=1.5,
            arrowprops=dict(arrowstyle='->', color=RED, alpha=0.6,
                           connectionstyle='arc3,rad=-0.2', lw=1.8),
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#1a0f0f',
                     edgecolor=RED, alpha=0.85, linewidth=1.0))

# ── 參數資訊框 ────────────────────────────────────
info_text = f'μ = {mu} 分鐘\nσ = {sigma} 分鐘\nN = 247 筆紀錄'
ax.text(0.97, 0.95, info_text, transform=ax.transAxes,
        fontsize=10, color=BLUE2, linespacing=1.6,
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                 edgecolor='#2d333b', alpha=0.85, linewidth=0.8))

# ── 軸 ───────────────────────────────────────────
ax.set_xlim(mu - 4.2 * sigma, mu + 4.2 * sigma)
ax.set_ylim(-0.05, max(y) * 1.15)
ax.set_xlabel('遲到分鐘數', fontsize=13, labelpad=12)
ax.set_ylabel('機率密度', fontsize=13, labelpad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='y', color=GRID, alpha=0.4, linewidth=0.5)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.3,
          edgecolor='#2d333b', facecolor='#161b22')

# ── 標題 ──────────────────────────────────────────
fig.suptitle('許芷萱的遲到分布：一座精準的堡壘',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.96)
ax.set_title('「她把時間切成標準差，用精確對抗失控。」',
             fontsize=10.5, color=MUTED, style='italic', pad=14)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.015,
         '一個人把恐懼穿在身上的形狀。',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.93])
plt.savefig('Ch03_常態分布.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch03_常態分布.png")
