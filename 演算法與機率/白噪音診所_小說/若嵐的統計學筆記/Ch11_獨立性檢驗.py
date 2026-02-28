"""
白噪音診所 — 若嵐的統計學筆記 #11
獨立性檢驗 Chi-Square Test of Independence

p = 0.000000134 → 拒絕獨立假設
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from scipy import stats

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
# 左圖：觀察值 vs 期望值（分組條形圖）
# ──────────────────────────────────────────────────
# 2×2 列聯表
#              出事  未出事
# Resonance:   52    28     (80 total)
# 非Resonance: 18   302    (320 total)
# Total:       70   330     400

observed = np.array([[52, 28],
                      [18, 302]])

row_sum  = observed.sum(axis=1)   # [80, 320]
col_sum  = observed.sum(axis=0)   # [70, 330]
total    = observed.sum()          # 400

expected = np.outer(row_sum, col_sum) / total
# expected ≈ [[14.0, 66.0], [56.0, 264.0]]

cell_labels = [
    'Resonance\n× 出事',
    'Resonance\n× 未出事',
    '非Resonance\n× 出事',
    '非Resonance\n× 未出事',
]
obs_flat = observed.flatten()
exp_flat = expected.flatten()

x = np.arange(4)
width = 0.35

bars_o = ax1.bar(x - width / 2, obs_flat, width, color=RED,
                 alpha=0.82, label='觀察值 O', zorder=3,
                 edgecolor='#0c1018', linewidth=0.6)
bars_e = ax1.bar(x + width / 2, exp_flat, width, color=BLUE,
                 alpha=0.82, label='期望值 E', zorder=3,
                 edgecolor='#0c1018', linewidth=0.6)

# 數值標注
for rect, val in zip(bars_o, obs_flat):
    ax1.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 3,
             f'{val:.0f}', ha='center', va='bottom', fontsize=9.5,
             color=RED, fontweight='bold')
for rect, val in zip(bars_e, exp_flat):
    ax1.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 3,
             f'{val:.1f}', ha='center', va='bottom', fontsize=9.5,
             color=BLUE, fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(cell_labels, fontsize=9.0)
ax1.set_ylabel('頻次', fontsize=11, labelpad=8)
ax1.set_title('觀察值 vs 期望值', fontsize=13, color=WHITE,
              fontweight='bold', pad=12)
ax1.legend(fontsize=10, facecolor='#12171f', edgecolor='#2d333b',
           labelcolor=TEXT)
ax1.grid(True, axis='y', color=GRID, alpha=0.5, linewidth=0.5, zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_ylim(0, 360)

# χ² 公式提示
chi2_val = np.sum((obs_flat - exp_flat) ** 2 / exp_flat)
ax1.text(0.97, 0.97,
         f'χ² = Σ(O−E)²/E\n= {chi2_val:.1f}',
         transform=ax1.transAxes, ha='right', va='top',
         fontsize=10, color=AMBER,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1408',
                   edgecolor=AMBER, alpha=0.8, linewidth=0.9))

# ──────────────────────────────────────────────────
# 右圖：χ²(df=1) 分布曲線 + 拒絕域
# ──────────────────────────────────────────────────
x_curve = np.linspace(0.01, 20, 800)
df = 1
y_curve = stats.chi2.pdf(x_curve, df)

ax2.plot(x_curve, y_curve, color=BLUE, linewidth=2.2, zorder=4)

# 拒絕域：α = 0.01，臨界值 6.63
crit_001 = stats.chi2.ppf(0.99, df)   # ≈ 6.635
chi2_obs = 9.9                          # 觀測到的 χ²

x_reject = np.linspace(crit_001, 20, 400)
y_reject = stats.chi2.pdf(x_reject, df)
ax2.fill_between(x_reject, 0, y_reject, color=RED, alpha=0.30,
                 zorder=2, label=f'拒絕域 (α=0.01)')

# 臨界值虛線
ax2.axvline(crit_001, color=AMBER, linewidth=1.6, linestyle='--', zorder=5,
            alpha=0.85)
ax2.text(crit_001 + 0.15, stats.chi2.pdf(crit_001, df) * 1.5,
         f'臨界值\n{crit_001:.2f}', fontsize=9, color=AMBER,
         va='bottom', style='italic')

# 觀測值紅線
ax2.axvline(chi2_obs, color=RED, linewidth=2.2, zorder=6)
ax2.text(chi2_obs + 0.15, stats.chi2.pdf(chi2_obs, df) + 0.012,
         f'χ² = {chi2_obs}\n（觀測值）',
         fontsize=9.5, color=RED, fontweight='bold', va='bottom',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a0a0a',
                   edgecolor=RED, alpha=0.82, linewidth=0.9))

# p 值標注
p_val_str = 'p < 0.01\n（實際 p = 1.34×10⁻⁷）'
ax2.text(12, 0.25, p_val_str, ha='center', fontsize=10.5,
         color=RED, fontweight='bold', linespacing=1.5,
         bbox=dict(boxstyle='round,pad=0.55', facecolor='#1a0a0a',
                   edgecolor=RED, alpha=0.85, linewidth=1.0))

ax2.legend(fontsize=9.5, facecolor='#12171f', edgecolor='#2d333b',
           labelcolor=TEXT, loc='upper right')
ax2.set_xlabel('χ² 值', fontsize=11, labelpad=8)
ax2.set_ylabel('機率密度', fontsize=11, labelpad=8)
ax2.set_title('χ² 檢驗：拒絕獨立假設', fontsize=13, color=WHITE,
              fontweight='bold', pad=12)
ax2.set_xlim(0, 18)
ax2.set_ylim(0, 0.45)
ax2.grid(True, axis='y', color=GRID, alpha=0.45, linewidth=0.5, zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# df 標注
ax2.text(0.03, 0.95, 'df = 1', transform=ax2.transAxes,
         fontsize=10, color=MUTED, style='italic')

# ──────────────────────────────────────────────────
# 底部引文
# ──────────────────────────────────────────────────
fig.text(0.5, 0.01,
         '「p = 0.000000134。他們不是獨立的。」',
         ha='center', fontsize=11.5, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.55', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

fig.suptitle('獨立性檢驗：χ² 統計量', fontsize=16, color=WHITE,
             fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0.07, 1, 0.94])

SAVE = '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch11_獨立性檢驗.png'
plt.savefig(SAVE, dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'✓ 已儲存：{SAVE}')
