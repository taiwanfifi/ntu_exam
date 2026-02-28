"""
白噪音診所 — 若嵐的統計學筆記 #04
幾何分布 Geometric Distribution

柏宇：連續30天的高頻事件，條件一變就歸零
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.patches import FancyBboxPatch

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
# 左圖：幾何分布 PMF，p = 0.3
# ──────────────────────────────────────────────────
p = 0.3
k = np.arange(1, 16)
pmf = (1 - p) ** (k - 1) * p

bars = ax1.bar(k, pmf, color=BLUE, alpha=0.82, width=0.65, zorder=3,
               edgecolor='#0c1018', linewidth=0.6)

# 標記每根 bar 的數值（前幾根）
for i, (ki, pi) in enumerate(zip(k[:5], pmf[:5])):
    ax1.text(ki, pi + 0.004, f'{pi:.3f}', ha='center', va='bottom',
             fontsize=8.5, color=BLUE, alpha=0.85)

# 文字框說明 P(X≥30)
prob_ge30 = (1 - p) ** 29
box_text = (f'P(X ≥ 30) = (0.7)²⁹\n'
            f'≈ {prob_ge30:.4f}\n'
            f'柏宇：連續 30 天無間斷')
ax1.text(8.5, 0.22,
         box_text,
         fontsize=9.5, color=RED, linespacing=1.55,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#1a0a0a',
                   edgecolor=RED, alpha=0.88, linewidth=1.0))

# 標示「30天」的虛線（映射到圖內的 k=15 邊界右側提示箭頭）
ax1.annotate('', xy=(15, 0.005), xytext=(13.5, 0.04),
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.3, alpha=0.7))
ax1.text(9.2, 0.05, '→ k=30 已在圖外', fontsize=8.5, color=RED, alpha=0.65)

ax1.set_xlim(0.2, 15.8)
ax1.set_ylim(0, 0.33)
ax1.set_xlabel('k（第幾次才首次成功）', fontsize=11, labelpad=8)
ax1.set_ylabel('P(X = k)', fontsize=11, labelpad=8)
ax1.set_xticks(k)
ax1.set_title('幾何分布 P(X=k), p = 0.3', fontsize=13, color=WHITE,
              fontweight='bold', pad=12)
ax1.grid(True, axis='y', color=GRID, alpha=0.5, linewidth=0.5, zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# p 標注
ax1.text(0.55, 0.29, 'p = 0.3', fontsize=11, color=AMBER,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1408',
                   edgecolor=AMBER, alpha=0.75, linewidth=0.8))

# ──────────────────────────────────────────────────
# 右圖：條件改變前後的事件頻率對比
# ──────────────────────────────────────────────────
labels   = ['改變條件前\n(47件 / 30天)', '改變條件後\n(2件 / 7天)']
rates    = [47 / 30, 2 / 7]       # ~1.57, ~0.29
colors   = [RED, GREEN]
x_pos    = [0, 1]

bars2 = ax2.bar(x_pos, rates, color=colors, alpha=0.82, width=0.45, zorder=3,
                edgecolor='#0c1018', linewidth=0.6)

# 數值標注
for xi, ri, ci in zip(x_pos, rates, colors):
    ax2.text(xi, ri + 0.02, f'{ri:.2f} 件/天',
             ha='center', va='bottom', fontsize=11.5, color=ci, fontweight='bold')

# 降幅標注
reduction = (rates[0] - rates[1]) / rates[0] * 100
ax2.annotate('', xy=(1, rates[1]), xytext=(0, rates[0]),
             arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5,
                             connectionstyle='arc3,rad=-0.3'))
ax2.text(0.5, 0.85, f'↓ {reduction:.0f}%', ha='center', fontsize=12,
         color=AMBER, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1408',
                   edgecolor=AMBER, alpha=0.75, linewidth=0.8))

ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, fontsize=10.5)
ax2.set_ylim(0, 2.1)
ax2.set_ylabel('每日事件頻率（件/天）', fontsize=11, labelpad=8)
ax2.set_title('條件改變後的事件頻率', fontsize=13, color=WHITE,
              fontweight='bold', pad=12)
ax2.grid(True, axis='y', color=GRID, alpha=0.5, linewidth=0.5, zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# 小說場景標注
ax2.text(0, 1.62, '柏宇\n跟蹤紀錄', ha='center', fontsize=8.5,
         color=RED, alpha=0.75)
ax2.text(1, 0.38, '若嵐\n介入後', ha='center', fontsize=8.5,
         color=GREEN, alpha=0.75)

# ──────────────────────────────────────────────────
# 底部引文
# ──────────────────────────────────────────────────
fig.text(0.5, 0.01,
         '「條件一變，自相關歸零。骰子終於重新擲了。」',
         ha='center', fontsize=11.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.55', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

# 大標題
fig.suptitle('幾何分布：等待第一次成功', fontsize=16, color=WHITE,
             fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0.07, 1, 0.94])

SAVE = '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch04_幾何分布.png'
plt.savefig(SAVE, dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'✓ 已儲存：{SAVE}')
