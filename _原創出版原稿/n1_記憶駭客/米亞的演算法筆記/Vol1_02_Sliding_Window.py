"""
米亞的演算法筆記 #02 — Sliding Window 滑動窗口
《記憶駭客》第8-9章：小杰母親的假暑假

「噪音裡的信號。雜訊裡的愛。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Color Palette ──
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
DARK_BG = '#0a0e14'
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

# ── Generate signal stream ──
np.random.seed(2089)
n_segments = 200  # Represent 1024 compressed to 200 for viz
noise_base = np.random.uniform(0.05, 0.35, n_segments)

# Inject signal peak around segment 70 (maps to ~347 in story)
peak_center = 70
peak_width = 13  # maps to window size 64
signal = np.zeros(n_segments)
for i in range(n_segments):
    dist = abs(i - peak_center)
    if dist < peak_width:
        signal[i] = 0.7 * np.exp(-0.5 * (dist / (peak_width * 0.4))**2)
    # Small secondary bump (false lead around segment 40)
    dist2 = abs(i - 40)
    if dist2 < 6:
        signal[i] += 0.2 * np.exp(-0.5 * (dist2 / 2.5)**2)

stream = noise_base + signal

# ── Sliding window SNR computation ──
window_k = 13
snr_values = []
for i in range(n_segments - window_k + 1):
    window = stream[i:i + window_k]
    sig_power = np.mean(signal[i:i + window_k])
    noise_power = np.mean(noise_base[i:i + window_k])
    snr = sig_power / max(noise_power, 0.01)
    snr_values.append(snr)

snr_values = np.array(snr_values)
best_pos = np.argmax(snr_values)

# ── Figure ──
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9),
                                gridspec_kw={'height_ratios': [1.3, 1]})

fig.suptitle('Sliding Window — 小杰母親的記憶流訊噪比掃描',
             fontsize=16, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.935, '「噪音裡的信號。雜訊裡的愛。」— 第8章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Top panel: Signal stream ──
x = np.arange(n_segments)

# Background noise fill
ax1.fill_between(x, 0, noise_base, color=MUTED, alpha=0.25, label='噪音')
# Signal on top of noise
ax1.fill_between(x, noise_base, stream, color=MIA_BLUE, alpha=0.35, label='訊號')
# Stream line
ax1.plot(x, stream, color=MIA_BLUE, linewidth=0.8, alpha=0.7)

# Highlight the best window
win_start = best_pos
win_end = best_pos + window_k
ax1.axvspan(win_start, win_end, color=MIA_WARM, alpha=0.2)
ax1.axvline(win_start, color=MIA_WARM, linewidth=1.5, linestyle='--', alpha=0.7)
ax1.axvline(win_end, color=MIA_WARM, linewidth=1.5, linestyle='--', alpha=0.7)

# Window bracket annotation
mid = (win_start + win_end) / 2
ax1.annotate('窗口鎖定：第347段\nSNR = 12.6',
             xy=(mid, stream[int(mid)] + 0.05),
             xytext=(mid + 30, 0.85),
             fontsize=10, color=MIA_WARM, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', fc=DARK_BG, ec=MIA_WARM, alpha=0.9))

# Mark the "mama" moment
ax1.plot(peak_center, stream[peak_center], 'o', color=MIA_WARM,
         markersize=10, zorder=5)
ax1.text(peak_center, stream[peak_center] + 0.08, '「媽媽！」',
         ha='center', fontsize=10, color=MIA_WARM, fontweight='bold')

# False lead annotation
ax1.annotate('微弱訊號\nSNR=2.1', xy=(40, stream[40]),
             xytext=(15, 0.7),
             fontsize=8, color=MUTED,
             arrowprops=dict(arrowstyle='->', color=MUTED, lw=1),
             bbox=dict(boxstyle='round,pad=0.2', fc=DARK_BG, ec=MUTED, alpha=0.8))

ax1.set_ylabel('記憶密度', fontsize=11, color=TEXT)
ax1.set_xlabel('記憶段編號（1024 段壓縮顯示）', fontsize=10, color=MUTED)
ax1.set_xlim(0, n_segments)
ax1.set_ylim(0, 1.1)
ax1.legend(loc='upper right', fontsize=9, frameon=False, labelcolor=TEXT)
ax1.grid(True, color=GRID, linewidth=0.5, alpha=0.5)

# ── Bottom panel: SNR curve ──
snr_x = np.arange(len(snr_values))
ax2.fill_between(snr_x, 0, snr_values, color=MIA_BLUE, alpha=0.2)
ax2.plot(snr_x, snr_values, color=MIA_BLUE, linewidth=1.2)

# Threshold line
threshold = 3.0
ax2.axhline(threshold, color=RED, linewidth=1, linestyle=':', alpha=0.7)
ax2.text(n_segments - 20, threshold + 0.3, f'閾值 SNR={threshold}',
         fontsize=9, color=RED, ha='right')

# Best position
ax2.plot(best_pos, snr_values[best_pos], 'o', color=MIA_WARM,
         markersize=12, zorder=5)
ax2.annotate(f'最高 SNR = {snr_values[best_pos]:.1f}\n位置 = {best_pos}',
             xy=(best_pos, snr_values[best_pos]),
             xytext=(best_pos + 25, snr_values[best_pos] - 1),
             fontsize=10, color=MIA_WARM, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', fc=DARK_BG, ec=MIA_WARM, alpha=0.9))

# Complexity annotation
ax2.text(160, snr_values.max() * 0.85,
         f'窗口大小 k = {window_k}\n滑動步數 = {len(snr_values)}\n複雜度 O(n)',
         fontsize=9, color=MUTED, fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.4', fc=GRID, ec=MUTED, alpha=0.8))

ax2.set_ylabel('SNR（訊噪比）', fontsize=11, color=TEXT)
ax2.set_xlabel('窗口起始位置', fontsize=10, color=MUTED)
ax2.set_xlim(0, len(snr_values))
ax2.set_ylim(0, snr_values.max() * 1.15)
ax2.grid(True, color=GRID, linewidth=0.5, alpha=0.5)

plt.tight_layout(rect=[0.03, 0.02, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol1_02_Sliding_Window.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
