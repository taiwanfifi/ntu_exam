"""
白噪音診所 — 若嵐的統計學筆記 #28
共變異數 Covariance

從藍到紅：Echo 的指紋
三個時間點的共變異數矩陣熱力圖
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

np.random.seed(42)

# ── 生成三組共變異數矩陣 ──────────────────────────
n = 12
dim_labels = [f'D{i+1}' for i in range(n)]

# Day -30：低共變異數，大部分接近零，對角線有值
base_30 = np.random.uniform(-0.05, 0.12, (n, n))
base_30 = (base_30 + base_30.T) / 2  # 對稱
np.fill_diagonal(base_30, np.random.uniform(0.15, 0.35, n))
# 加入少量稀疏暖點
base_30[2, 5] = base_30[5, 2] = 0.22
base_30[8, 9] = base_30[9, 8] = 0.18

# Day -7：中等共變異數，從對角線向外擴散
base_7 = np.random.uniform(0.05, 0.35, (n, n))
base_7 = (base_7 + base_7.T) / 2
np.fill_diagonal(base_7, np.random.uniform(0.55, 0.75, n))
# 對角線附近加強
for i in range(n):
    for j in range(n):
        dist = abs(i - j)
        if dist <= 2:
            base_7[i, j] += 0.2
        elif dist <= 4:
            base_7[i, j] += 0.08
base_7 = np.clip(base_7, 0, 1)

# Day 0：幾乎全紅，所有維度高度相關
base_0 = np.random.uniform(0.7, 0.95, (n, n))
base_0 = (base_0 + base_0.T) / 2
np.fill_diagonal(base_0, 1.0)
# 確保最低值也不低
base_0 = np.clip(base_0, 0.65, 1.0)

matrices = [base_30, base_7, base_0]
titles = ['崩潰前 30 天', '崩潰前 7 天', '崩潰當天']
subtitle_texts = ['稀疏．獨立', '擴散．耦合', '全面同步']
border_colors = [BLUE, AMBER, RED]

fig, axes = plt.subplots(1, 3, figsize=(18, 6.5),
                          gridspec_kw={'wspace': 0.25})

for idx, (ax, mat, title, sub, bc) in enumerate(
        zip(axes, matrices, titles, subtitle_texts, border_colors)):
    im = ax.imshow(mat, cmap='RdYlBu_r', aspect='equal',
                   vmin=-0.1, vmax=1.0, interpolation='nearest')

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(dim_labels, fontsize=7, rotation=45)
    ax.set_yticklabels(dim_labels, fontsize=7)

    ax.set_title(f'{title}\n{sub}', fontsize=13, color=bc,
                 fontweight='bold', pad=10, linespacing=1.5)

    # 邊框顏色
    for spine in ax.spines.values():
        spine.set_edgecolor(bc)
        spine.set_linewidth(1.5)

    # 在格子裡標數字（只對 Day 0 標部分高值）
    if idx == 2:
        for i in range(0, n, 3):
            for j in range(0, n, 3):
                val = mat[i, j]
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=6.5, color='white', fontweight='bold')

# ── 共用色條 ──────────────────────────────────────
cbar_ax = fig.add_axes([0.93, 0.18, 0.015, 0.62])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('共變異數', fontsize=11, color=TEXT, labelpad=10)
cbar.ax.tick_params(colors=MUTED, labelsize=9)
cbar.outline.set_edgecolor('#2d333b')

# ── 演化箭頭 ──────────────────────────────────────
fig.text(0.365, 0.06, '→', fontsize=28, color=AMBER, ha='center',
         fontweight='bold', alpha=0.6)
fig.text(0.655, 0.06, '→', fontsize=28, color=RED, ha='center',
         fontweight='bold', alpha=0.6)

# ── 標題 ──────────────────────────────────────────
fig.suptitle('從藍到紅：Echo 的指紋',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.97)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.46, 0.008,
         '所有維度同步崩潰。這就是人為操控的痕跡。',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.08, 0.91, 0.93])
plt.savefig('Ch28_共變異數.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch28_共變異數.png")
