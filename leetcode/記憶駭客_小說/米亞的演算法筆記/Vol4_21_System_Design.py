"""
米亞的演算法筆記 #21 — System Design 系統設計
《記憶駭客》第220-234章：語青的堡壘 / 第265-281章：全城選項C

「分散式架構？我是說——家。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import os

# ── Color Palette ──
DARK_BG  = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT     = '#d0d7de'
MUTED    = '#6e7681'
GRID     = '#1c2028'
RED      = '#ff6b6b'
GREEN    = '#7bc87b'

# ── Chinese Font ──
for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.family'] = font
        break
    except Exception:
        continue

plt.rcParams.update({
    'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG,
    'axes.edgecolor': MUTED,
})

np.random.seed(221)

# ── Layout: 2 rows ──
fig = plt.figure(figsize=(16, 11))
gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1], hspace=0.32, wspace=0.28,
                      left=0.06, right=0.96, top=0.88, bottom=0.06)
ax_arch = fig.add_subplot(gs[0, :])   # top: full-width architecture
ax_cap  = fig.add_subplot(gs[1, 0])   # bottom-left: CAP triangle
ax_ft   = fig.add_subplot(gs[1, 1])   # bottom-right: fault tolerance

fig.suptitle('米亞的演算法筆記 #21 — System Design\n語青的堡壘：2400 個碎片的分散式架構',
             fontsize=15, color=MIA_BLUE, fontweight='bold', y=0.96)
fig.text(0.5, 0.905, '「分散式架構？我是說——家。」— 第220章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

# ═══ TOP: Distributed architecture diagram ═══
ax_arch.set_xlim(-1, 17); ax_arch.set_ylim(-1.5, 5.5); ax_arch.axis('off')
ax_arch.set_title('堡壘架構：分片 × 複製 × 負載平衡', fontsize=13, color=TEXT, pad=8)

lb_x, lb_y = 8, 4.8  # Load Balancer
ax_arch.add_patch(mpatches.FancyBboxPatch(
    (lb_x - 1.5, lb_y - 0.35), 3, 0.7,
    boxstyle='round,pad=0.12', fc=MIA_WARM + '33', ec=MIA_WARM, lw=2))
ax_arch.text(lb_x, lb_y, 'Load Balancer', ha='center', va='center',
             fontsize=10, color=MIA_WARM, fontweight='bold')
shard_labels = ['Shard A\n「笑容」', 'Shard B\n「聲音」', 'Shard C\n「觸感」', 'Shard D\n「記憶核心」']
shard_colors = [MIA_BLUE, GREEN, '#c49cde', RED]
shard_x_centers = [2, 6.5, 10.5, 15]

for si, (sx, label, sc) in enumerate(zip(shard_x_centers, shard_labels, shard_colors)):
    # Connection from LB to shard group
    ax_arch.annotate('', xy=(sx, 3.2), xytext=(lb_x, lb_y - 0.35),
                     arrowprops=dict(arrowstyle='->', color=MUTED, lw=1, ls='--'))
    for ri in range(3):  # 3 replicas per shard
        rx, ry = sx - 1.0 + ri * 1.0, 2.5 - ri * 0.9
        alpha = '88' if ri == 0 else '55' if ri == 1 else '33'
        ax_arch.add_patch(mpatches.FancyBboxPatch(
            (rx - 0.55, ry - 0.35), 1.1, 0.7,
            boxstyle='round,pad=0.08', fc=sc + alpha, ec=sc, lw=1.5))
        ax_arch.text(rx, ry, f'R{ri+1}', ha='center', va='center',
                     fontsize=8, color=TEXT, fontweight='bold')
        if ri < 2:  # consensus arrows
            nx, ny = sx - 1.0 + (ri + 1) * 1.0, 2.5 - (ri + 1) * 0.9
            ax_arch.annotate('', xy=(nx + 0.1, ny + 0.35), xytext=(rx + 0.1, ry - 0.35),
                             arrowprops=dict(arrowstyle='<->', color=sc, lw=0.8, alpha=0.5))
    ax_arch.text(sx, 3.35, label, ha='center', va='bottom',
                 fontsize=9, color=sc, fontweight='bold')

fx, fy = shard_x_centers[2] + 1.0 - 0.55, 2.5 - 2 * 0.9  # fault marker
ax_arch.text(fx + 0.55, fy, 'X', ha='center', va='center',
             fontsize=16, color=RED, fontweight='bold',
             path_effects=[pe.withStroke(linewidth=3, foreground=DARK_BG)])
ax_arch.annotate('節點故障\n其餘副本接手', xy=(fx + 0.55, fy - 0.35),
                 xytext=(fx + 0.55, fy - 1.1),
                 fontsize=8, color=RED, ha='center',
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1))

ax_arch.text(8, -1.2,
             '48 節點 · 2400 碎片 · 副本因子 3 · 總儲存 7200 份\n'
             '「三份。如果世界毀了兩次，她還在。」',
             ha='center', fontsize=9, color=MUTED, style='italic')

# ═══ BOTTOM-LEFT: CAP Theorem triangle ═══
ax_cap.set_xlim(-0.5, 4.5); ax_cap.set_ylim(-0.8, 4.2); ax_cap.axis('off')
ax_cap.set_title('CAP 定理：Pick 2', fontsize=12, color=TEXT, pad=6)

# Triangle vertices
C_pos = (2, 3.6)
A_pos = (0.3, 0.3)
P_pos = (3.7, 0.3)
tri = plt.Polygon([C_pos, A_pos, P_pos], fill=False, ec=MUTED, lw=1.5, ls='--')
ax_cap.add_patch(tri)

for pos, label, col in [(C_pos, 'C\n一致性', MIA_BLUE),
                         (A_pos, 'A\n可用性', GREEN),
                         (P_pos, 'P\n分區容忍', MIA_WARM)]:
    ax_cap.text(pos[0], pos[1], label, ha='center', va='center',
                fontsize=11, color=col, fontweight='bold')

# Highlight CP edge
cp_mid = ((C_pos[0] + P_pos[0]) / 2 + 0.3, (C_pos[1] + P_pos[1]) / 2)
ax_cap.plot([C_pos[0], P_pos[0]], [C_pos[1], P_pos[1]],
            color=MIA_BLUE, lw=3, alpha=0.7)
ax_cap.text(cp_mid[0], cp_mid[1], '維倫的選擇\nCP',
            ha='center', va='center', fontsize=10, color=MIA_BLUE,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc=DARK_BG, ec=MIA_BLUE, alpha=0.9))

ax_cap.text((C_pos[0]+A_pos[0])/2 - 0.4, (C_pos[1]+A_pos[1])/2,
            'CA', ha='center', fontsize=9, color=MUTED)
ax_cap.text((A_pos[0]+P_pos[0])/2, (A_pos[1]+P_pos[1])/2 - 0.45,
            'AP', ha='center', fontsize=9, color=MUTED)
ax_cap.text(2, -0.6, '「語青只有一個自己。」', ha='center',
            fontsize=9, color=MIA_WARM, style='italic')

# ═══ BOTTOM-RIGHT: Fault tolerance results ═══
ax_ft.set_title('容錯測試：47 種故障場景', fontsize=12, color=TEXT, pad=6)

categories = ['單節點故障', '網路分區', '級聯故障', '數據損壞', '多節點故障',
              '全斷電', '2/3損毀', '她選擇離開']
results    = [10, 10, 10, 10, 4, 0, 0, 0]
max_vals   = [10, 10, 10, 10, 4, 1, 1, 1]
colors_bar = [GREEN]*5 + [RED]*3

y_pos = np.arange(len(categories))[::-1]
bars = ax_ft.barh(y_pos, results, height=0.6, color=[c + '88' for c in colors_bar],
                  edgecolor=colors_bar, linewidth=1.5)
# Background bars
ax_ft.barh(y_pos, max_vals, height=0.6, color=GRID, edgecolor=MUTED,
           linewidth=0.5, zorder=0)

for i, (cat, res, mx) in enumerate(zip(categories, results, max_vals)):
    lbl = f'{res}/{mx} 通過' if res > 0 else '失敗'
    c = GREEN if res > 0 else RED
    ax_ft.text(max(res, 0.3) + 0.3, y_pos[i], f'{cat}  {lbl}',
               va='center', fontsize=9, color=c)

ax_ft.set_xlim(0, 13); ax_ft.set_yticks([]); ax_ft.set_xlabel('通過數', fontsize=9)
ax_ft.text(7, y_pos[-1] - 0.1,
           '← 場景 47\n   不是工程問題',
           fontsize=8, color=RED, style='italic', va='center')
ax_ft.text(10, y_pos[2], '44/47\n93.6%', ha='center', va='center',
           fontsize=16, color=MIA_WARM, fontweight='bold')

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol4_21_System_Design.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
