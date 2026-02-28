"""
白噪音診所 — 若嵐的統計學筆記 #16
辛普森悖論 Simpson's Paradox

每一天看起來都正常。但加總起來不正常。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Style constants
BG = '#0c1018'
RED = '#ff6b6b'
BLUE = '#64b5f6'
PURPLE = '#ce93d8'
AMBER = '#ffb74d'
GREEN = '#81c784'
WHITE = '#e0e0e0'
GREY = '#555555'

plt.rcParams.update({
    'font.family': ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'STHeiti'],
    'axes.facecolor': BG,
    'figure.facecolor': BG,
    'text.color': WHITE,
    'axes.labelcolor': WHITE,
    'xtick.color': WHITE,
    'ytick.color': WHITE,
    'font.size': 11,
})

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 7.5))
fig.patch.set_facecolor(BG)

# ── LEFT PANEL: Daily bar chart ──────────────────────────────────────────
counts = [2, 2, 3, 2, 2, 2, 2, 1, 3, 2, 5, 1]
days = list(range(1, 13))
lambda0 = 0.95  # baseline

bar_colors = []
for c in counts:
    if c <= 2:
        bar_colors.append(GREEN)
    elif c == 3:
        bar_colors.append(AMBER)
    else:
        bar_colors.append(RED)

bars = ax_left.bar(days, counts, color=bar_colors, edgecolor='#0c1018',
                   linewidth=0.8, width=0.7, zorder=3)

# Baseline dashed line
ax_left.axhline(y=lambda0, color=BLUE, linewidth=1.8, linestyle='--', alpha=0.8, zorder=4)
ax_left.text(12.35, lambda0 + 0.05, f'λ₀ = {lambda0}', fontsize=9, color=BLUE, va='bottom')

# Value labels on bars
for bar, c in zip(bars, counts):
    if c > 0:
        ax_left.text(bar.get_x() + bar.get_width() / 2, c + 0.08,
                     str(c), ha='center', va='bottom', fontsize=9,
                     color=WHITE, fontweight='bold')

ax_left.set_xlim(0.3, 13.5)
ax_left.set_ylim(0, 6.5)
ax_left.set_xticks(days)
ax_left.set_xticklabels([f'Day\n{d}' for d in days], fontsize=8.5)
ax_left.set_xlabel('日期', fontsize=11, labelpad=10)
ax_left.set_ylabel('事件次數', fontsize=11, labelpad=10)
ax_left.set_title('每一天看起來都正常', fontsize=14, color=WHITE, pad=14)
ax_left.spines['top'].set_visible(False)
ax_left.spines['right'].set_visible(False)
ax_left.spines['left'].set_color(GREY)
ax_left.spines['bottom'].set_color(GREY)
ax_left.grid(True, axis='y', color='#1c2028', alpha=0.5, linewidth=0.5, zorder=1)
ax_left.tick_params(colors=GREY)

# Legend
green_p = mpatches.Patch(color=GREEN, label='正常 (≤2)')
amber_p = mpatches.Patch(color=AMBER, label='略高 (=3)')
red_p = mpatches.Patch(color=RED, label='異常 (≥4)')
baseline_line = mpatches.Patch(color=BLUE, label=f'基準線 λ₀ = {lambda0}')
ax_left.legend(handles=[green_p, amber_p, red_p, baseline_line],
               fontsize=8.5, facecolor='#12181f', edgecolor=GREY, labelcolor=WHITE,
               loc='upper left')

# Annotation for Day 11
ax_left.annotate('Day 11\n單日爆增',
                 xy=(11, 5), xytext=(9.2, 5.8),
                 fontsize=8.5, color=RED,
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1.3),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a0a0a',
                           edgecolor=RED, alpha=0.8))

# ── Connecting arrow between panels ─────────────────────────────────────
fig.text(0.505, 0.52, '→', fontsize=28, color=AMBER, ha='center', va='center',
         fontweight='bold')

# ── RIGHT PANEL: Aggregate comparison ────────────────────────────────────
ax_right.set_facecolor(BG)
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
ax_right.spines['left'].set_color(GREY)
ax_right.spines['bottom'].set_color(GREY)

baseline_total = round(lambda0 * 12, 1)  # 11.4
actual_total = sum(counts)              # 22

categories = ['基準期望值\n(λ₀ × 12天)', '實際觀測值\n(∑ 12天)']
values = [baseline_total, actual_total]
colors = [BLUE, RED]

bars2 = ax_right.barh(categories, values, color=colors, height=0.45,
                      edgecolor='#0c1018', linewidth=0.8)

# Value labels inside bars
for bar, val, col in zip(bars2, values, colors):
    ax_right.text(val + 0.4, bar.get_y() + bar.get_height() / 2,
                  f'{val}', va='center', fontsize=16, color=col, fontweight='bold')

ax_right.set_xlim(0, 32)
ax_right.set_xlabel('事件總數', fontsize=11, labelpad=10)
ax_right.set_title('但加總起來不正常', fontsize=14, color=WHITE, pad=14)
ax_right.tick_params(colors=GREY)
ax_right.grid(True, axis='x', color='#1c2028', alpha=0.5, linewidth=0.5, zorder=1)

# Z and p annotation
ax_right.text(16, 0.55,
              'Z = 4.62\np < 0.00002',
              fontsize=16, color=AMBER, fontweight='bold',
              va='center', ha='left',
              bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1408',
                        edgecolor=AMBER, alpha=0.85))

# Extra annotation
ax_right.annotate('超出基準\n+' + str(actual_total - baseline_total) + ' 件',
                  xy=(actual_total, 0.0), xytext=(24.5, -0.4),
                  fontsize=10, color=RED,
                  arrowprops=dict(arrowstyle='->', color=RED, lw=1.3),
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a0a0a',
                            edgecolor=RED, alpha=0.85))

# Insight text
ax_right.text(1, -0.68,
              '個別看：每天正常。\n整體看：統計顯著異常。\n這就是辛普森悖論的反面——\n細看無事，總覽驚心。',
              fontsize=9.5, color=GREY, linespacing=1.6,
              bbox=dict(boxstyle='round,pad=0.5', facecolor='#12181f',
                        edgecolor=GREY, alpha=0.6))

ax_right.set_ylim(-1.1, 1.2)

# ── Title and quote ──────────────────────────────────────────────────────
fig.suptitle('辛普森悖論  Simpson\'s Paradox',
             fontsize=18, color=WHITE, fontweight='bold', y=0.97)

fig.text(0.5, 0.02,
         '「每一天：正常。十二天：Z = 4.62。」',
         ha='center', fontsize=12, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.95])
plt.savefig(
    '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch16_辛普森悖論.png',
    dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none'
)
print("saved Ch16_辛普森悖論.png")
