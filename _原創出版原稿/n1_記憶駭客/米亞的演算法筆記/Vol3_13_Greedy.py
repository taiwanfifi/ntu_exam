"""
米亞的演算法筆記 #13 — Greedy 貪心演算法
《記憶駭客》第163-164章：六十秒搶救決策序列

「你有六十秒。不是選最好的——是選來得及的。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Color Palette ──
DARK_BG = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT = '#d0d7de'
MUTED = '#6e7681'
GRID = '#1c2028'
RED = '#ff6b6b'
GREEN = '#7bc87b'

# ── Chinese Font Detection ──
def get_chinese_font():
    for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
        try:
            from matplotlib.font_manager import FontProperties
            fp = FontProperties(family=font)
            if fp.get_name() != font:
                continue
            return font
        except Exception:
            continue
    return 'PingFang TC'

FONT_FAMILY = get_chinese_font()
plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['axes.facecolor'] = DARK_BG
plt.rcParams['figure.facecolor'] = DARK_BG
plt.rcParams['text.color'] = TEXT
plt.rcParams['axes.edgecolor'] = MUTED
plt.rcParams['xtick.color'] = MUTED
plt.rcParams['ytick.color'] = MUTED

# ── Data: 60-second rescue sequence (showing 20 representative seconds) ──
np.random.seed(163)
n_show = 20

labels = [
    '新手媽媽', '老人亡妻', '退役軍人', '鋼琴師', '教師',
    '青年初吻', '漁夫遠洋', '護士夜班', '作家靈感', '廚師味覺',
    '畫家色彩', '工程師', '舞者旋轉', '農夫日出', '歌手高音',
    '男孩母聲', '程式師', '園丁花香', '棋手終局', '攝影師光'
]
values = [97, 94, 89, 88, 82, 76, 63, 71, 68, 59,
          52, 58, 91, 45, 73, 31, 58, 42, 66, 55]

# Rescue outcome: 0=saved, 1=lost, 2=degraded
outcomes = [0, 0, 1, 0, 2, 0, 1, 0, 0, 1,
            1, 0, 1, 2, 0, 0, 0, 1, 0, 2]
# Note: index 15 (男孩母聲, value=31) is saved — Viren's deviation
# Note: index 12 (舞者, value=91) is lost — cost of the 0.8s pause

outcome_colors = {0: MIA_BLUE, 1: RED, 2: MIA_WARM}
outcome_alpha  = {0: 0.9, 1: 0.3, 2: 0.6}

# ── Figure Setup ──
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 1, height_ratios=[3, 1.2, 1], hspace=0.35)

fig.suptitle('Greedy — 六十秒搶救決策序列',
             fontsize=17, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, '「你有六十秒。不是選最好的——是選來得及的。」— 第163章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Panel 1: Timeline with value bars ──
ax1 = fig.add_subplot(gs[0])
bar_width = 0.7

for i in range(n_show):
    c, a = outcome_colors[outcomes[i]], outcome_alpha[outcomes[i]]
    ax1.bar(i, values[i], width=bar_width, color=c, alpha=a, edgecolor=c, lw=0.8)
    ax1.text(i, values[i]+1.5, labels[i], ha='center', va='bottom',
             fontsize=7.5, color=TEXT, rotation=45)
    ax1.text(i, values[i]/2, str(values[i]), ha='center', va='center',
             fontsize=8, color=DARK_BG, fontweight='bold')

# Highlight the deviation at second 16 (index 15)
ax1.annotate('維倫的選擇\n(偏離最優)',
             xy=(15, values[15] + 1), xytext=(15, -15),
             fontsize=9, color=MIA_WARM, fontweight='bold',
             ha='center', va='top',
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=2))

# Highlight the lost dancer at index 12
ax1.annotate('因 0.8 秒延遲\n永久碎裂',
             xy=(12, values[12]), xytext=(12, values[12] + 18),
             fontsize=8, color=RED, ha='center',
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))

ax1.set_xlim(-0.8, n_show - 0.2)
ax1.set_ylim(-20, 120)
ax1.set_ylabel('記憶價值', fontsize=11, color=TEXT)
ax1.set_xlabel('搶救順序（秒）', fontsize=11, color=TEXT)
ax1.set_xticks(range(n_show))
ax1.set_xticklabels([f'{i+1}' for i in range(n_show)], fontsize=8)
ax1.axhline(y=0, color=MUTED, linewidth=0.5)
ax1.set_facecolor(DARK_BG)
ax1.grid(axis='y', color=GRID, linewidth=0.5, alpha=0.5)

# ── Panel 2: Cumulative value curve ──
ax2 = fig.add_subplot(gs[1])
cumulative = np.cumsum(
    [values[i] if outcomes[i] != 1 else 0 for i in range(n_show)]
)
# Theoretical optimal (sorted desc, all saved)
optimal_vals = sorted(values, reverse=True)
cumulative_opt = np.cumsum(optimal_vals)

ax2.fill_between(range(n_show), cumulative_opt, alpha=0.15, color=GREEN)
ax2.plot(range(n_show), cumulative_opt, color=GREEN, linewidth=1.5,
         linestyle='--', label='理論最優', alpha=0.7)
ax2.plot(range(n_show), cumulative, color=MIA_BLUE, linewidth=2.5,
         label='維倫實際', marker='o', markersize=4)

# Mark the deviation point
ax2.plot(15, cumulative[15], 'o', color=MIA_WARM, markersize=10, zorder=5)
ax2.annotate('第47秒偏離',
             xy=(15, cumulative[15]), xytext=(17, cumulative[15] - 80),
             fontsize=9, color=MIA_WARM,
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.5))

ax2.set_ylabel('累計搶救價值', fontsize=10, color=TEXT)
ax2.set_xlabel('搶救順序（秒）', fontsize=10, color=TEXT)
ax2.legend(fontsize=9, loc='upper left', frameon=False, labelcolor=TEXT)
ax2.set_facecolor(DARK_BG)
ax2.grid(color=GRID, linewidth=0.5, alpha=0.5)
ax2.set_xlim(-0.5, n_show - 0.5)

# ── Panel 3: Summary stats ──
ax3 = fig.add_subplot(gs[2])
ax3.axis('off')

sv = sum(1 for o in outcomes if o==0)
lo = sum(1 for o in outcomes if o==1)
dg = sum(1 for o in outcomes if o==2)
sv_val = sum(values[i] for i in range(n_show) if outcomes[i]==0)
stats = (f'搶救成功: {sv}/{n_show} ({sv/n_show*100:.0f}%)    '
         f'永久失去: {lo}/{n_show} ({lo/n_show*100:.0f}%)    '
         f'降級保存: {dg}/{n_show} ({dg/n_show*100:.0f}%)    '
         f'搶救總價值: {sv_val}')
ax3.text(0.5, 0.7, stats, ha='center', va='center',
         fontsize=11, color=TEXT, fontweight='bold', transform=ax3.transAxes)

ax3.text(0.5, 0.2,
         '「不是因為理性。是因為手比大腦快。」— 第164章',
         ha='center', va='center', fontsize=11, color=MIA_WARM,
         style='italic', transform=ax3.transAxes)

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=MIA_BLUE, alpha=0.9, label='搶救成功 (saved)'),
    mpatches.Patch(facecolor=RED, alpha=0.3, label='永久失去 (lost)'),
    mpatches.Patch(facecolor=MIA_WARM, alpha=0.6, label='降級保存 (degraded)'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol3_13_Greedy.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
