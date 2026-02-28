"""
米亞的演算法筆記 #06 — Binary Search 視覺化
「每折一次，離真相更近一步。」

在 2^20 = 1,048,576 段記憶中，用 Binary Search 找到「茉莉花」。
左圖：搜尋空間逐步減半的過程。
右圖：完整的 binary search tree 路徑，標記茉莉花為目標。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── 色彩 ──
DARK_BG  = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT     = '#d0d7de'
MUTED   = '#6e7681'
GRID    = '#1c2028'
RED     = '#ff6b6b'
GREEN   = '#7bc87b'

# ── 中文字體 ──
for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.family'] = font
        break
    except Exception:
        continue

plt.rcParams.update({
    'text.color': TEXT,
    'axes.labelcolor': TEXT,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'figure.facecolor': DARK_BG,
    'axes.facecolor': DARK_BG,
})

# ─────────────────────────────────────────────
# 左圖資料：ch35 茉莉花搜尋步驟
# ─────────────────────────────────────────────
steps = [
    ("全部感官記憶",   1_048_576, None),
    ("嗅覺最強",       524_288,   "視覺/聽覺 排除"),
    ("花香類",         262_144,   "食物/化學品 排除"),
    ("茉莉花科",       131_072,   "玫瑰/桂花 排除"),
    ("特定茉莉",        65_536,   "繼續縮小"),
    ("精確片段",        32_768,   "..."),
    ("...",             16_384,   "..."),
    ("...",              8_192,   "..."),
    ("定位區域",         4_096,   "..."),
    ("逼近",             2_048,   "..."),
    ("鎖定",             1_024,   "..."),
    ("*心率 150*",           1,   "* 茉莉花"),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9),
                                gridspec_kw={'width_ratios': [1, 1.2]})

# ── 左圖：搜尋空間遞減瀑布圖 ──
n = len(steps)
y_pos = np.arange(n)[::-1]
sizes = [s[1] for s in steps]
labels = [s[0] for s in steps]
log_sizes = [np.log2(max(s, 1)) for s in sizes]

colors = []
for i, s in enumerate(steps):
    if i == n - 1:
        colors.append(MIA_WARM)
    elif i <= 2:
        colors.append(MIA_BLUE)
    else:
        colors.append(MUTED)

bars = ax1.barh(y_pos, log_sizes, height=0.6, color=colors, edgecolor=DARK_BG)

for i, (bar, label, size) in enumerate(zip(bars, labels, sizes)):
    w = bar.get_width()
    c = MIA_WARM if i == n - 1 else TEXT
    ax1.text(w + 0.3, bar.get_y() + bar.get_height() / 2,
             f"{label}  ({size:,})",
             va='center', ha='left', fontsize=8.5, color=c)

# 連接箭頭（每步之間）
for i in range(n - 1):
    ax1.annotate('', xy=(log_sizes[i + 1], y_pos[i + 1]),
                 xytext=(log_sizes[i], y_pos[i]),
                 arrowprops=dict(arrowstyle='->', color=MUTED,
                                 lw=0.8, connectionstyle='arc3,rad=0.15'))

ax1.set_xlim(0, 24)
ax1.set_yticks([])
ax1.set_xlabel('log2(搜尋空間大小)', fontsize=10)
ax1.set_title('ch35 茉莉花：搜尋空間遞減\n2^20 = 1,048,576 -> 1',
              fontsize=13, color=MIA_BLUE, pad=15)
ax1.axvline(x=0, color=GRID, lw=0.5)

# 底部標註
ax1.text(12, -1.5, '「每折一次，離真相更近一步。」',
         ha='center', va='center', fontsize=10, color=MIA_WARM,
         style='italic')

# ─────────────────────────────────────────────
# 右圖：四次 Binary Search 情感遞進
# ─────────────────────────────────────────────
chapters = ['ch33\n記憶庫', 'ch35\n茉莉花', 'ch45\n三千份報告', 'ch53\n冰原碎片']
emotions = ['真相', '愛', '恐懼', '希望']
weights  = [1, 3, 2, 4]  # 情感重量
ch_colors = [MIA_BLUE, MIA_WARM, RED, GREEN]

x_ch = np.arange(len(chapters))

# 情感重量柱狀
bar2 = ax2.bar(x_ch, weights, width=0.5, color=ch_colors, edgecolor=DARK_BG,
               alpha=0.85)

for i, (b, emo) in enumerate(zip(bar2, emotions)):
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15,
             emo, ha='center', va='bottom', fontsize=12,
             color=ch_colors[i], fontweight='bold')

# 教學遞進曲線
teach_level = [1, 2, 3, 4]
teach_labels = ['概念建立', '變體理解', '內化', '直覺']
ax2b = ax2.twinx()
ax2b.plot(x_ch, teach_level, 'o--', color=TEXT, markersize=8,
          markerfacecolor=TEXT, lw=1.5, alpha=0.7)
for i, tl in enumerate(teach_labels):
    ax2b.text(x_ch[i] + 0.12, teach_level[i] + 0.12, tl,
              fontsize=8.5, color=MUTED, ha='left')

ax2b.set_ylabel('讀者理解度', fontsize=10, color=MUTED)
ax2b.set_ylim(0, 5.5)
ax2b.tick_params(colors=MUTED)
ax2b.spines['right'].set_color(MUTED)

ax2.set_xticks(x_ch)
ax2.set_xticklabels(chapters, fontsize=10)
ax2.set_ylabel('情感重量', fontsize=10)
ax2.set_ylim(0, 5.5)
ax2.set_title('Binary Search 四次使用：情感遞進 × 教學遞進',
              fontsize=13, color=MIA_BLUE, pad=15)

# 虛線標記：ch35 = 全卷最佳 AB 線融合
ax2.annotate('★ 全卷最佳 AB 線融合',
             xy=(1, 3), xytext=(1.8, 4.5),
             fontsize=9, color=MIA_WARM,
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.2))

# 虛線標記：ch53 = 讀者跑在角色前面
ax2.annotate('讀者跑在角色前面',
             xy=(3, 4), xytext=(2.2, 5.0),
             fontsize=9, color=GREEN,
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

# ── 全域標題 ──
fig.suptitle('米亞的演算法筆記 #06 — Binary Search\n「對折再對折，在百萬段記憶中找到她」',
             fontsize=15, color=MIA_WARM, y=0.98, fontweight='bold')

plt.tight_layout(rect=[0, 0.02, 1, 0.93])

out_path = os.path.join(os.path.dirname(__file__), 'Vol1_06_Binary_Search.png')
plt.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close()
print(f"已儲存：{out_path}")
