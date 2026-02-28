"""
白噪音診所 — 若嵐的統計學筆記 #07
相關不代表因果 Correlation ≠ Causation

沈維誠（3年前）與林哲宇（2個月前）的 GPS 軌跡高度重疊
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
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
# 左圖：GPS 軌跡散點圖
# ──────────────────────────────────────────────────
rng = np.random.default_rng(42)

# 台北街道模擬路徑（Z字型城市路徑）
n = 60
t = np.linspace(0, 2 * np.pi, n)

# 基礎路徑：模擬台北信義→大安的路線
base_x = 2.5 * t + 0.8 * np.sin(1.5 * t)
base_y = 1.2 * t + 1.0 * np.cos(2.0 * t) + 0.5 * np.sin(3 * t)

# 沈維誠（3年前）：加入小噪音
noise_w_x = rng.normal(0, 0.25, n)
noise_w_y = rng.normal(0, 0.25, n)
w_x = base_x + noise_w_x
w_y = base_y + noise_w_y

# 林哲宇（2個月前）：高度相關，略微偏移
noise_z_x = rng.normal(0.18, 0.22, n)
noise_z_y = rng.normal(0.12, 0.22, n)
z_x = base_x + noise_z_x
z_y = base_y + noise_z_y

# 計算實際相關係數（用 x 座標）
r = np.corrcoef(w_x, z_x)[0, 1]

# 繪製
ax1.scatter(w_x, w_y, color=BLUE, s=28, alpha=0.72, zorder=4,
            label='沈維誠（3年前）', edgecolors='none')
ax1.scatter(z_x, z_y, color=RED, s=28, alpha=0.72, zorder=4,
            label='林哲宇（2個月前）', edgecolors='none')

# 路徑連線（淡化）
ax1.plot(w_x, w_y, color=BLUE,   alpha=0.22, linewidth=1.0, zorder=2)
ax1.plot(z_x, z_y, color=RED,    alpha=0.22, linewidth=1.0, zorder=2)

# 起點／終點標記
ax1.scatter([w_x[0]], [w_y[0]], color=BLUE,  s=100, marker='D', zorder=6,
            edgecolors=WHITE, linewidth=1.2)
ax1.scatter([z_x[0]], [z_y[0]], color=RED,   s=100, marker='D', zorder=6,
            edgecolors=WHITE, linewidth=1.2)
ax1.scatter([w_x[-1]], [w_y[-1]], color=BLUE, s=120, marker='*', zorder=6,
            edgecolors=WHITE, linewidth=0.8)
ax1.scatter([z_x[-1]], [z_y[-1]], color=RED,  s=120, marker='*', zorder=6,
            edgecolors=WHITE, linewidth=0.8)

ax1.legend(fontsize=9.5, loc='upper left',
           facecolor='#12171f', edgecolor='#2d333b',
           labelcolor=TEXT, markerscale=1.4)

ax1.set_xlabel('東西向座標（相對 km）', fontsize=10.5, labelpad=8)
ax1.set_ylabel('南北向座標（相對 km）', fontsize=10.5, labelpad=8)
ax1.set_title(f'兩條軌跡的重疊  r = {r:.2f}',
              fontsize=13, color=WHITE, fontweight='bold', pad=12)
ax1.grid(True, color=GRID, alpha=0.45, linewidth=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# r 值標注框
ax1.text(0.97, 0.04, f'r ≈ {r:.2f}\n（高度正相關）',
         transform=ax1.transAxes, ha='right', va='bottom',
         fontsize=10, color=AMBER,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1408',
                   edgecolor=AMBER, alpha=0.8, linewidth=0.9))

# ──────────────────────────────────────────────────
# 右圖：因果關係概念圖（三種情境）
# ──────────────────────────────────────────────────
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_facecolor(BG)

# 分隔線
ax2.axhline(6.5, color=GREY, alpha=0.4, linewidth=0.8, xmin=0.05, xmax=0.95)
ax2.axhline(3.2, color=GREY, alpha=0.4, linewidth=0.8, xmin=0.05, xmax=0.95)

# ── 情境 1：A → B（直接因果）
y1 = 8.2
ax2.text(1.5, y1, 'A', fontsize=20, color=BLUE,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1a2e',
                   edgecolor=BLUE, linewidth=1.8))
ax2.text(8.5, y1, 'B', fontsize=20, color=GREEN,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1e0d',
                   edgecolor=GREEN, linewidth=1.8))
ax2.annotate('', xy=(7.8, y1), xytext=(2.2, y1),
             arrowprops=dict(arrowstyle='->', color=WHITE,
                             lw=2.0, mutation_scale=18))
ax2.text(5.0, y1 + 0.55, 'A 導致 B', ha='center', fontsize=11,
         color=WHITE, fontweight='bold')
ax2.text(5.0, y1 - 0.65, '（直接因果）', ha='center', fontsize=9.5,
         color=MUTED, style='italic')

# ── 情境 2：A ← B（反向因果）
y2 = 4.85
ax2.text(1.5, y2, 'A', fontsize=20, color=BLUE,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1a2e',
                   edgecolor=BLUE, linewidth=1.8))
ax2.text(8.5, y2, 'B', fontsize=20, color=GREEN,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1e0d',
                   edgecolor=GREEN, linewidth=1.8))
ax2.annotate('', xy=(2.2, y2), xytext=(7.8, y2),
             arrowprops=dict(arrowstyle='->', color=RED,
                             lw=2.0, mutation_scale=18))
ax2.text(5.0, y2 + 0.55, 'B 導致 A', ha='center', fontsize=11,
         color=RED, fontweight='bold')
ax2.text(5.0, y2 - 0.65, '（反向因果）', ha='center', fontsize=9.5,
         color=MUTED, style='italic')

# ── 情境 3：A ← C → B（干擾變數）
y3 = 1.5
ax2.text(1.5, y3, 'A', fontsize=20, color=BLUE,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1a2e',
                   edgecolor=BLUE, linewidth=1.8))
ax2.text(8.5, y3, 'B', fontsize=20, color=GREEN,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#0d1e0d',
                   edgecolor=GREEN, linewidth=1.8))
ax2.text(5.0, y3 + 1.55, 'C', fontsize=20, color=AMBER,
         fontweight='bold', ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.5', facecolor='#1a1408',
                   edgecolor=AMBER, linewidth=2.2))
ax2.text(5.0, y3 + 2.75, '干擾變數 C', ha='center', fontsize=11,
         color=AMBER, fontweight='bold')
ax2.text(5.0, y3 + 2.2, '（Resonance Analytics）', ha='center', fontsize=9,
         color=AMBER, alpha=0.75, style='italic')

# C → A
ax2.annotate('', xy=(2.1, y3 + 0.25), xytext=(4.4, y3 + 1.3),
             arrowprops=dict(arrowstyle='->', color=AMBER,
                             lw=1.8, mutation_scale=16))
# C → B
ax2.annotate('', xy=(7.9, y3 + 0.25), xytext=(5.6, y3 + 1.3),
             arrowprops=dict(arrowstyle='->', color=AMBER,
                             lw=1.8, mutation_scale=16))

ax2.set_title('相關≠因果：三種可能的關係',
              fontsize=13, color=WHITE, fontweight='bold', pad=12)

# ──────────────────────────────────────────────────
# 底部引文
# ──────────────────────────────────────────────────
fig.text(0.5, 0.01,
         '「他們是被同一個看不見的手推向同一條路的兩個人。」',
         ha='center', fontsize=11.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.55', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

fig.suptitle('相關不代表因果', fontsize=16, color=WHITE,
             fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0.07, 1, 0.94])

SAVE = '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch07_相關不代表因果.png'
plt.savefig(SAVE, dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'✓ 已儲存：{SAVE}')
