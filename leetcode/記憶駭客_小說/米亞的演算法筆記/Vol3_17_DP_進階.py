"""
米亞的演算法筆記 #17 — DP 進階（多維動態規劃）
《記憶駭客》第189-191章：
  維倫的記憶真偽分析——依賴鏈汙染傳播

「43%。不多。但你的 43% 裡面有她。」
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

# ── Build memory dependency graph ──
from collections import deque

N_NODES = 28
layer_sizes = [3, 5, 6, 6, 5, 3]
layer_labels = ['根源記憶', '童年', '少年', '遇見語青前', '遇見語青後', '現在']
positions, node_layer = [], []
for li, size in enumerate(layer_sizes):
    y, x0 = 5 - li * 1.0, -(size - 1) / 2.0
    for ni in range(size):
        positions.append((x0 + ni * 1.1, y)); node_layer.append(li)

edges_raw = [
    (0,3),(0,4),(1,4),(1,5),(2,6),(2,7),(3,8),(3,9),(4,9),(4,10),
    (5,10),(5,11),(6,12),(7,12),(7,13),(8,14),(9,14),(9,15),(10,15),
    (10,16),(11,17),(11,18),(12,18),(13,19),(14,20),(15,20),(15,21),
    (16,21),(16,22),(17,22),(18,23),(19,23),(20,25),(21,25),(21,26),
    (22,26),(23,27),(24,25),(24,26)]
planted_sources = {0, 2}

# DP contamination propagation
adj, in_deg = [[] for _ in range(N_NODES)], [0] * N_NODES
for u, v in edges_raw:
    adj[u].append(v); in_deg[v] += 1
status = ['PLANTED' if i in planted_sources else 'NATIVE' for i in range(N_NODES)]
queue = deque(i for i in range(N_NODES) if in_deg[i] == 0)
while queue:
    u = queue.popleft()
    for v in adj[u]:
        if status[u] == 'PLANTED': status[v] = 'PLANTED'
        in_deg[v] -= 1
        if in_deg[v] == 0: queue.append(v)
n_native = status.count('NATIVE')
n_planted = status.count('PLANTED')
pct_native = round(100 * n_native / N_NODES)

# ── Figure: two panels ──
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(1, 2, width_ratios=[3, 1.2], wspace=0.08)
ax_graph = fig.add_subplot(gs[0])
ax_stats = fig.add_subplot(gs[1])

fig.suptitle('DP 進階 — 維倫的記憶真偽分析（依賴鏈汙染傳播）',
             fontsize=16, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.935,
         '「43%。聽起來不多。但維倫——你那 43% 裡面有她。」— 第191章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ── Left panel: dependency graph ──
ax_graph.set_xlim(-4.5, 4.5); ax_graph.set_ylim(-1.5, 6.2)
ax_graph.set_aspect('equal'); ax_graph.axis('off')

for u, v in edges_raw:
    x1, y1 = positions[u]; x2, y2 = positions[v]
    planted_e = (status[u] == 'PLANTED' and status[v] == 'PLANTED')
    ax_graph.annotate('', xy=(x2, y2), xytext=(x1, y1),
                      arrowprops=dict(arrowstyle='->', lw=1.5 if planted_e else 0.8,
                                      color=RED if planted_e else MIA_BLUE,
                                      alpha=0.7 if planted_e else 0.35))

for i, (x, y) in enumerate(positions):
    src = i in planted_sources
    planted = status[i] == 'PLANTED'
    nc = RED if planted else MIA_BLUE
    fc = nc + ('55' if src else '22' if planted else '33')
    circle = plt.Circle((x, y), 0.32, facecolor=fc, edgecolor=nc,
                         linewidth=2.5 if src else 1.5, zorder=3)
    ax_graph.add_patch(circle)
    ax_graph.text(x, y, str(i), ha='center', va='center',
                  fontsize=7, color=nc, fontweight='bold', zorder=4)

for li, label in enumerate(layer_labels):
    ax_graph.text(-4.2, 5 - li, label, ha='right', va='center',
                  fontsize=8, color=MUTED, style='italic')
for idx, lbl, c in [(0,'植入源',RED),(2,'植入源',RED),(1,'原生',MIA_BLUE)]:
    ax_graph.text(positions[idx][0], positions[idx][1]+0.55, lbl,
                  ha='center', va='bottom', fontsize=7.5, color=c, fontweight='bold')

# ── Right panel: statistics ──
ax_stats.set_xlim(0, 10); ax_stats.set_ylim(0, 10); ax_stats.axis('off')

theta1, theta2 = 90, 90 + 360 * n_planted / N_NODES
ax_stats.add_patch(mpatches.Wedge((5,6.5), 2.0, theta1, theta2,
                   facecolor=RED+'aa', edgecolor=RED, linewidth=1.5))
ax_stats.add_patch(mpatches.Wedge((5,6.5), 2.0, theta2, theta1+360,
                   facecolor=MIA_BLUE+'aa', edgecolor=MIA_BLUE, linewidth=1.5))
ax_stats.text(5, 6.5, f'{pct_native}%\n原生', ha='center', va='center',
              fontsize=16, color=MIA_WARM, fontweight='bold')
ax_stats.text(5, 3.8, f'植入: {n_planted} 段 ({100-pct_native}%)',
              ha='center', fontsize=10, color=RED, fontweight='bold')
ax_stats.text(5, 3.1, f'原生: {n_native} 段 ({pct_native}%)',
              ha='center', fontsize=10, color=MIA_BLUE, fontweight='bold')
ax_stats.text(5, 1.6, '「原生的部分\n  有她在。」',
              ha='center', va='center', fontsize=11,
              color=MIA_WARM, style='italic', fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.5', facecolor=MIA_WARM+'15',
                        edgecolor=MIA_WARM, linewidth=1.2))
ax_stats.text(5, 0.5, f'汙染擴大倍率: {n_planted}/{len(planted_sources)} = '
              f'{n_planted/len(planted_sources):.1f}x',
              ha='center', fontsize=8.5, color=MUTED)

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=RED + '55', edgecolor=RED, label='植入（已知源 + 汙染傳播）'),
    mpatches.Patch(facecolor=MIA_BLUE + '33', edgecolor=MIA_BLUE, label='原生記憶'),
    mpatches.Patch(facecolor=GRID, edgecolor=MIA_WARM, label='依賴鏈方向 →'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False,
           labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol3_17_DP_進階.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
