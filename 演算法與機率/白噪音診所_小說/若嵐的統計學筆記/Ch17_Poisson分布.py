"""
白噪音診所 — 若嵐的統計學筆記 #17
Poisson 分布

每一滴雨是獨立的。但雨量是被控制的。
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson
from scipy.stats import norm

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

# ── LEFT PANEL: Poisson PMF comparison ──────────────────────────────────
lambda0 = 0.95
lambda1 = 2.25
k_vals = np.arange(0, 10)

pmf0 = poisson.pmf(k_vals, lambda0)
pmf1 = poisson.pmf(k_vals, lambda1)

width = 0.38
offsets = [-width / 2, width / 2]

bars0 = ax_left.bar(k_vals + offsets[0], pmf0, width=width, color=BLUE,
                    alpha=0.8, label=f'λ₀ = {lambda0}（基準 / 正常）',
                    edgecolor='#0c1018', linewidth=0.6)
bars1 = ax_left.bar(k_vals + offsets[1], pmf1, width=width, color=RED,
                    alpha=0.8, label=f'λ₁ = {lambda1}（觀測 / 異常）',
                    edgecolor='#0c1018', linewidth=0.6)

# Arrow showing the shift
ax_left.annotate('',
                 xy=(lambda1, 0.30), xytext=(lambda0, 0.30),
                 arrowprops=dict(arrowstyle='->', color=AMBER, lw=2.0))
ax_left.text((lambda0 + lambda1) / 2, 0.32, 'λ 被調高了',
             ha='center', fontsize=9.5, color=AMBER)

# Mu markers
ax_left.axvline(x=lambda0, color=BLUE, linewidth=1.0, linestyle=':', alpha=0.5)
ax_left.axvline(x=lambda1, color=RED, linewidth=1.0, linestyle=':', alpha=0.5)

ax_left.set_xticks(k_vals)
ax_left.set_xticklabels([f'k={k}' for k in k_vals], fontsize=8.5, rotation=30)
ax_left.set_xlabel('事件次數 k', fontsize=11, labelpad=10)
ax_left.set_ylabel('P(X = k)', fontsize=11, labelpad=10)
ax_left.set_title('Poisson 分布：λ 被調高了', fontsize=14, color=WHITE, pad=14)
ax_left.legend(fontsize=9.5, facecolor='#12181f', edgecolor=GREY, labelcolor=WHITE)
ax_left.set_xlim(-0.7, 9.5)
ax_left.set_ylim(0, 0.42)
ax_left.spines['top'].set_visible(False)
ax_left.spines['right'].set_visible(False)
ax_left.spines['left'].set_color(GREY)
ax_left.spines['bottom'].set_color(GREY)
ax_left.grid(True, axis='y', color='#1c2028', alpha=0.5, linewidth=0.5)
ax_left.tick_params(colors=GREY)

# Insight text
ax_left.text(5.0, 0.36,
             f'P(k≥3 | λ₀={lambda0}) = {1 - poisson.cdf(2, lambda0):.3f}\n'
             f'P(k≥3 | λ₁={lambda1}) = {1 - poisson.cdf(2, lambda1):.3f}',
             fontsize=9, color=GREY, linespacing=1.6,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#12181f',
                       edgecolor=GREY, alpha=0.7))

# ── RIGHT PANEL: Treatment effect — shift in mean ────────────────────────
ax_right.set_facecolor(BG)
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
ax_right.spines['left'].set_color(GREY)
ax_right.spines['bottom'].set_color(GREY)

x = np.linspace(-8, 8, 600)

# 治療前: N(+3.12, 0.87^2) — "遲到的堡壘"
mu_before, sigma_before = 3.12, 0.87
y_before = norm.pdf(x, mu_before, sigma_before)

# 治療後: N(-2.17, 1.03^2) — "提早的堡壘"
mu_after, sigma_after = -2.17, 1.03
y_after = norm.pdf(x, mu_after, sigma_after)

ax_right.fill_between(x, y_before, alpha=0.15, color=BLUE)
ax_right.plot(x, y_before, color=BLUE, linewidth=2.2,
              label=f'治療前  N({mu_before}, {sigma_before}²)  遲到的堡壘')

ax_right.fill_between(x, y_after, alpha=0.15, color=GREEN)
ax_right.plot(x, y_after, color=GREEN, linewidth=2.2,
              label=f'治療後  N({mu_after}, {sigma_after}²)  提早的堡壘')

# x=0 vertical line (準時)
ax_right.axvline(x=0, color=WHITE, linewidth=1.5, linestyle='--', alpha=0.5)
ax_right.text(0.15, 0.40, '準時\n(x = 0)', fontsize=8.5, color=WHITE, va='center')

# Mu markers
ax_right.axvline(x=mu_before, color=BLUE, linewidth=1.0, linestyle=':', alpha=0.5)
ax_right.text(mu_before + 0.1, 0.46, f'μ = {mu_before}', fontsize=8.5, color=BLUE)

ax_right.axvline(x=mu_after, color=GREEN, linewidth=1.0, linestyle=':', alpha=0.5)
ax_right.text(mu_after - 1.5, 0.40, f'μ = {mu_after}', fontsize=8.5, color=GREEN)

# Shift arrow
ax_right.annotate('',
                 xy=(mu_after, 0.28), xytext=(mu_before, 0.28),
                 arrowprops=dict(arrowstyle='<->', color=AMBER, lw=2.0))
delta_mu = round(mu_after - mu_before, 2)
ax_right.text((mu_before + mu_after) / 2, 0.30,
              f'Δμ = {delta_mu}', ha='center', fontsize=9.5, color=AMBER)

# Insight annotation
ax_right.annotate('均值移了。\n標準差沒變。',
                  xy=(-1.0, 0.15), xytext=(2.5, 0.25),
                  fontsize=11, color=AMBER, fontweight='bold',
                  arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.3),
                  bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1408',
                            edgecolor=AMBER, alpha=0.85))

ax_right.set_xlabel('相對準時的偏移（分鐘）', fontsize=11, labelpad=10)
ax_right.set_ylabel('機率密度', fontsize=11, labelpad=10)
ax_right.set_title('均值 vs 標準差', fontsize=14, color=WHITE, pad=14)
ax_right.legend(fontsize=9, facecolor='#12181f', edgecolor=GREY, labelcolor=WHITE,
                loc='upper right')
ax_right.set_xlim(-7, 7.5)
ax_right.set_ylim(0, 0.55)
ax_right.tick_params(colors=GREY)

# ── Title and quote ──────────────────────────────────────────────────────
fig.suptitle('Poisson 分布  泊松過程',
             fontsize=18, color=WHITE, fontweight='bold', y=0.97)

fig.text(0.5, 0.02,
         '「每一滴雨是獨立的。但雨量是被控制的。」',
         ha='center', fontsize=12, color=PURPLE, style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#14101e',
                   edgecolor=PURPLE, alpha=0.45, linewidth=0.8))

plt.tight_layout(rect=[0, 0.07, 1, 0.95])
plt.savefig(
    '/Users/william/Downloads/phd_exam/演算法與機率/白噪音診所_小說/若嵐的統計學筆記/Ch17_Poisson分布.png',
    dpi=200, bbox_inches='tight', facecolor=BG, edgecolor='none'
)
print("saved Ch17_Poisson分布.png")
