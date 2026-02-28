"""
白噪音診所 — 若嵐的統計學筆記 #08
貝氏更新 Bayesian Updating

左：後驗機率隨證據累積的曲線（0.01 → 0.9997）
右：每條證據的似然比柱狀圖
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

# ── 色彩 ──────────────────────────────────────────
BG = '#0c1018'
TEXT = '#d0d7de'
MUTED = '#6e7681'
GRID = '#1c2028'
RED = '#ff6b6b'
BLUE = '#64b5f6'
AMBER = '#ffb74d'
PURPLE = '#ce93d8'

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5),
                                gridspec_kw={'width_ratios': [5, 3]})

# ══════════════════════════════════════════════════
# 左圖：貝氏更新曲線
# ══════════════════════════════════════════════════

evidence_short = [
    '初始信念',
    '14件事件\n符合行為導引',
    '陳默\n消失了',
    '倫理\n委員會調查',
    '三位患者\n同步異常',
    '87%論文',
    '若晴的名字',
]

# 似然比迭代
prior = 0.01
likelihood_ratios = [None, 950, 3.5, 3.0, 3.5, 3.0, 8.0]
posteriors = [prior]
odds = prior / (1 - prior)
for lr in likelihood_ratios[1:]:
    odds *= lr
    posteriors.append(odds / (1 + odds))

x = np.arange(len(posteriors))

# 平滑曲線
x_smooth = np.linspace(0, len(posteriors)-1, 300)
posteriors_smooth = np.interp(x_smooth, x, posteriors)

# 漸變填充
ax1.fill_between(x_smooth, 0, posteriors_smooth, alpha=0.06, color=BLUE)
ax1.plot(x_smooth, posteriors_smooth, color=BLUE, linewidth=2.5, alpha=0.85)

# 「不敢再算」的門檻線
ax1.axhline(y=0.95, color=RED, linewidth=0.8, linestyle=':', alpha=0.35)
ax1.text(6.4, 0.935, '「不敢再算了」', fontsize=8.5, color=RED,
         alpha=0.55, ha='right', style='italic')

# 顏色漸變：從冷藍到紅
point_colors = ['#64b5f6', '#ffb74d', '#ffa726', '#ff8a65',
                '#ef5350', '#e53935', '#c62828']

# 數據點與標注
for i, (xi, yi, label, c) in enumerate(zip(x, posteriors, evidence_short, point_colors)):
    ax1.scatter(xi, yi, s=140, color=c, zorder=5,
               edgecolors='white', linewidth=1.5)

    if i == 0:
        ax1.annotate(f'{label}\nP = {yi:.2f}',
                    xy=(xi, yi), xytext=(xi + 0.4, yi + 0.10),
                    fontsize=8.5, color=BLUE, linespacing=1.3,
                    arrowprops=dict(arrowstyle='->', color=BLUE, alpha=0.4),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                             edgecolor='#2d333b', alpha=0.85))
    elif i == 1:
        ax1.annotate(f'{label}\nP = {yi:.3f}',
                    xy=(xi, yi), xytext=(xi + 0.35, yi - 0.18),
                    fontsize=8.5, color=AMBER, linespacing=1.3,
                    arrowprops=dict(arrowstyle='->', color=AMBER, alpha=0.4),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                             edgecolor='#2d333b', alpha=0.85))
    elif i == len(posteriors) - 1:
        ax1.annotate(f'{label}\nP = {yi:.4f}',
                    xy=(xi, yi), xytext=(xi - 1.8, yi - 0.15),
                    fontsize=9, color=RED, fontweight='bold', linespacing=1.3,
                    arrowprops=dict(arrowstyle='->', color=RED, alpha=0.5,
                                   connectionstyle='arc3,rad=-0.2'),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a0f0f',
                             edgecolor=RED, alpha=0.85))
    else:
        # 簡化：只標數字，交替上下
        offset = 0.035 if i % 2 == 0 else -0.055
        ax1.text(xi, yi + offset, f'{yi:.3f}',
                fontsize=8, color=MUTED, ha='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor=BG,
                         edgecolor='none', alpha=0.8))

ax1.set_xlim(-0.5, 6.8)
ax1.set_ylim(-0.05, 1.12)
ax1.set_xlabel('累積證據', fontsize=12, labelpad=10)
ax1.set_ylabel('後驗機率 P(陳默涉入 | 所有證據)', fontsize=11.5, labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels([f'#{i}' for i in range(len(posteriors))], fontsize=9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, axis='y', color=GRID, alpha=0.4, linewidth=0.5)

# ══════════════════════════════════════════════════
# 右圖：似然比（每條證據的「說服力」）
# ══════════════════════════════════════════════════

lr_labels = [
    '14件事件\n模式吻合',
    '他消失了',
    '倫理委員會\n調查',
    '三位患者\n同步異常',
    '87% 準確率\n預測論文',
    '若晴的名字\n在致謝頁',
]
lr_values = likelihood_ratios[1:]
lr_colors = [AMBER, BLUE, BLUE, AMBER, BLUE, RED]

bars = ax2.barh(range(len(lr_values)), lr_values, color=lr_colors,
                edgecolor='white', linewidth=0.5, alpha=0.8, height=0.55)

for i, (bar, val, c) in enumerate(zip(bars, lr_values, lr_colors)):
    if val > 100:
        ax2.text(bar.get_width() - 50, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f}x', va='center', ha='right',
                 fontsize=13, color='white', fontweight='bold')
    else:
        ax2.text(bar.get_width() + 12, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}x', va='center', fontsize=10.5,
                 color=c, fontweight='bold')

ax2.set_yticks(range(len(lr_labels)))
ax2.set_yticklabels(lr_labels, fontsize=9.5)
ax2.set_xlabel('似然比 Likelihood Ratio', fontsize=11, labelpad=10)
ax2.set_title('每條證據的說服力', fontsize=13, color=TEXT, pad=12)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.invert_yaxis()
ax2.set_xlim(0, 1150)

# 第一條證據的標注
ax2.annotate('一條證據，翻轉 950 倍',
            xy=(950, 0), xytext=(600, 1.8),
            fontsize=9, color=AMBER, style='italic',
            arrowprops=dict(arrowstyle='->', color=AMBER, alpha=0.5))

# ── 標題 ──────────────────────────────────────────
fig.suptitle('若嵐的貝氏更新：信念如何被證據改變',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.97)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.008,
         '「貝氏定理的核心不是公式。是勇氣。'
         '是你願不願意承認，你原本相信的事，可能是錯的。」—— 白若嵐',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
plt.savefig('Ch08_貝氏更新.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch08_貝氏更新.png")
