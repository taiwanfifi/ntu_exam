"""
白噪音診所 — 若嵐的統計學筆記 #01
期望值 Expected Value

林哲宇死前七天的行為投資時間軸
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
BG = '#0c1018'
PANEL = '#0c1018'
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
    'axes.facecolor': PANEL,
    'text.color': TEXT,
    'axes.labelcolor': TEXT,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'axes.edgecolor': '#2d333b',
    'font.size': 11,
})

fig, ax = plt.subplots(figsize=(14, 7.5))

# ── 背景區域 ──────────────────────────────────────
# 紅色零線區域（自殺意圖 E=0）
ax.axhline(y=0, color=RED, linewidth=1.8, linestyle='--', alpha=0.5)
ax.fill_between([-8.5, 1.5], -1200, 0, color=RED, alpha=0.025)
ax.text(-8.2, -800, 'E[X] = 0　自殺計畫者的行為期望值',
        fontsize=9, color=RED, alpha=0.6, style='italic')

# ── 數據點 ────────────────────────────────────────
events = [
    (-7,  12000, BLUE,   '半年健身房會員\n$12,000',  '→ 6 個月後兌現',  (-5.2, 12800)),
    (-3,  5000,  BLUE2,  '兩張演唱會門票\n$5,000',   '→ 2 個月後兌現',  (-1.1, 6200)),
    (-0.5, 800,  PURPLE, '凍乾貓糧（給 Bug）\n$800', '→ 明天兌現',      (0.6, 2200)),
]

for day, val, color, label, sub, text_pos in events:
    # 垂直連線
    ax.plot([day, day], [0, val], color=color, linewidth=1.2, alpha=0.35, linestyle=':')
    # 散點
    ax.scatter(day, val, s=180, color=color, zorder=5,
               edgecolors='white', linewidth=1.5)
    # 標注
    ax.annotate(f'{label}\n{sub}',
                xy=(day, val), xytext=text_pos,
                fontsize=9.5, color=color, linespacing=1.4,
                arrowprops=dict(arrowstyle='->', color=color, alpha=0.5,
                               connectionstyle='arc3,rad=0.15'),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                         edgecolor=color, alpha=0.85, linewidth=0.8))

# ── 死亡線 ────────────────────────────────────────
ax.axvline(x=0, color=RED, linewidth=2.5, alpha=0.75)
ax.annotate('06:47\n數據歸零',
            xy=(0, 10000), xytext=(0.7, 10500),
            fontsize=12, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0f0f',
                     edgecolor=RED, alpha=0.85))

# ── 趨勢：用虛線連接三個點，暗示方向 ──────────────
trend_x = [-7, -3, -0.5]
trend_y = [12000, 5000, 800]
ax.plot(trend_x, trend_y, color=AMBER, linewidth=1.5, linestyle='--',
        alpha=0.25, zorder=1)
ax.text(-6.5, 8500, '行為投資的方向：全部指向未來 →',
        fontsize=9.5, color=AMBER, alpha=0.5, style='italic',
        rotation=-18)

# ── 軸 ───────────────────────────────────────────
ax.set_xlim(-8.5, 2.2)
ax.set_ylim(-1500, 15000)
ax.set_xlabel('距離死亡的天數', fontsize=12, labelpad=12)
ax.set_ylabel('行為投資金額（新台幣）', fontsize=12, labelpad=12)
ax.set_xticks([-7, -6, -5, -4, -3, -2, -1, 0])
ax.set_xticklabels(['Day -7', '', '', '', 'Day -3', '', '', 'Day 0'],
                    fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='y', color=GRID, alpha=0.4, linewidth=0.5)

# ── 標題 ──────────────────────────────────────────
fig.suptitle('林哲宇死前七天的行為期望值',
             fontsize=17, color='#e6edf3', fontweight='bold', y=0.96)
ax.set_title('「一個人的行為投資，就是他真實意圖的影子。」',
             fontsize=10.5, color=MUTED, style='italic', pad=14)

# ── 底部引文 ──────────────────────────────────────
fig.text(0.5, 0.015,
         '如果 E[未來投資] > 0，他不是在計畫死亡。\n'
         '「這不是自殺。這是謀殺。只是凶器不是刀，是機率。」',
         ha='center', fontsize=10.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#14101e',
                  edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.08, 1, 0.93])
plt.savefig('Ch01_期望值.png', dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.show()
print("✓ Ch01_期望值.png")
