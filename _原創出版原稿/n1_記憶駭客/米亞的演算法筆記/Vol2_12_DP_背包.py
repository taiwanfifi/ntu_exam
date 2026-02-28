"""
米亞的演算法筆記 #12 — DP / 背包問題 視覺化
Knapsack DP table + 記憶卡片 + 三樣東西最終選擇。
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── 色彩與字型 ──
DARK_BG  = '#0a0e14'
MIA_BLUE = '#4fc1e9'
MIA_WARM = '#f5c542'
TEXT     = '#d0d7de'
MUTED    = '#6e7681'
GRID     = '#1c2028'
RED      = '#ff6b6b'
GREEN    = '#7bc87b'
plt.rcParams['font.family'] = ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ── 記憶物品 ──
MEMORIES = [
    {'name': '榮譽獎章',   'w': 12, 'v': 2,  'keep': False},
    {'name': '破案紀錄',   'w': 18, 'v': 4,  'keep': False},
    {'name': '方法論',     'w': 3,  'v': 8,  'keep': True},
    {'name': '同事情誼',   'w': 8,  'v': 5,  'keep': False},
    {'name': '維倫的友誼', 'w': 8,  'v': 10, 'keep': True},
    {'name': '茉莉花',     'w': 1,  'v': 99, 'keep': True},
]
CAP = 66  # 可保留容量 (100 - 34)
n = len(MEMORIES)
weights = [m['w'] for m in MEMORIES]
values  = [m['v'] for m in MEMORIES]

# ── DP 計算 ──
dp = np.zeros((n + 1, CAP + 1), dtype=int)
for i in range(1, n + 1):
    for w in range(CAP + 1):
        dp[i][w] = dp[i-1][w]
        if w >= weights[i-1]:
            dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])

# ── 建立圖形 ──
fig = plt.figure(figsize=(18, 9), facecolor=DARK_BG)
gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1], hspace=0.35, wspace=0.25,
                      left=0.06, right=0.94, top=0.88, bottom=0.08)

# ── Panel 1: 記憶卡片 ──
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(DARK_BG); ax1.axis('off')
ax1.set_xlim(-0.5, 6.5); ax1.set_ylim(-1.0, 2.5)
ax1.set_title('嚴柏翰的記憶清單', fontsize=13, color=TEXT, fontweight='bold', pad=10)

for idx, m in enumerate(MEMORIES):
    x, kept = idx, m['keep']
    ec = GREEN if kept else RED
    fc = '#0d1a0d' if kept else '#1a0d0d'
    a = 1.0 if kept else 0.5
    ax1.add_patch(mpatches.FancyBboxPatch((x-0.4, -0.5), 0.8, 2.4,
        boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=2 if kept else 1, alpha=a, zorder=2))
    ax1.text(x, 1.55, m['name'], ha='center', va='center',
             fontsize=8.5, color=ec, fontweight='bold', alpha=a, zorder=3)
    # Weight bar
    bw = min(m['w']/20, 0.7) * 0.7
    ax1.add_patch(mpatches.FancyBboxPatch((x-bw/2, 0.7), bw, 0.22,
        boxstyle="round,pad=0.02", fc=RED, alpha=0.4*a, zorder=3))
    ax1.text(x, 0.81, f"w={m['w']}%", ha='center', va='center',
             fontsize=7, color=RED, alpha=a, zorder=4)
    # Value bar
    bv = min(m['v']/20, 0.7) * 0.7
    ax1.add_patch(mpatches.FancyBboxPatch((x-bv/2, 0.2), bv, 0.22,
        boxstyle="round,pad=0.02", fc=MIA_WARM, alpha=0.4*a, zorder=3))
    vs = f"v={m['v']}" if m['v'] < 50 else "v=inf"
    ax1.text(x, 0.31, vs, ha='center', va='center',
             fontsize=7, color=MIA_WARM, alpha=a, zorder=4)
    dec = "* keep" if kept else "x drop"
    ax1.text(x, -0.2, dec, ha='center', va='center',
             fontsize=8, color=ec, fontweight='bold', alpha=a, zorder=3)
ax1.text(3.0, -0.8, 'drop = release    keep = define yourself',
         ha='center', fontsize=9, color=MUTED, style='italic')

# ── Panel 2: DP 表格 ──
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(DARK_BG)
ax2.set_title('DP table (sampled columns)', fontsize=13, color=TEXT,
              fontweight='bold', pad=10)
w_samp = [0, 3, 8, 11, 16, 19, 27, 35, 50, 66]
row_labels = ['--'] + [m['name'][:3] for m in MEMORIES]
max_val = dp[n][CAP]
n_rows, n_cols = n + 1, len(w_samp)

for i in range(n_rows):
    for j in range(n_cols):
        val = dp[i][w_samp[j]]
        intensity = val / max(max_val, 1)
        if val == max_val and i == n_rows - 1:
            fc, tc, a = MIA_WARM, DARK_BG, 1.0
        elif val > 0:
            fc, tc = MIA_BLUE, (DARK_BG if intensity > 0.5 else TEXT)
            a = 0.15 + 0.6 * intensity
        else:
            fc, tc, a = GRID, MUTED, 0.5
        ax2.add_patch(mpatches.FancyBboxPatch(
            (j-0.45, n_rows-1-i-0.4), 0.9, 0.8,
            boxstyle="round,pad=0.03", fc=fc, alpha=a, ec=MUTED, lw=0.5, zorder=2))
        ax2.text(j, n_rows-1-i, str(val), ha='center', va='center',
                 fontsize=7.5, color=tc, fontweight='bold', zorder=3)

for j, ws in enumerate(w_samp):
    ax2.text(j, n_rows-0.2, f'w={ws}', ha='center', fontsize=7, color=MUTED)
for i, rl in enumerate(row_labels):
    ax2.text(-0.8, n_rows-1-i, rl, ha='right', fontsize=8, color=TEXT)
ax2.set_xlim(-1.2, n_cols-0.3); ax2.set_ylim(-0.8, n_rows+0.5); ax2.axis('off')
ax2.annotate(f'optimal = {max_val}', xy=(n_cols-1, 0), xytext=(n_cols-1.5, -0.6),
             fontsize=9, color=MIA_WARM, fontweight='bold', ha='center',
             arrowprops=dict(arrowstyle='->', color=MIA_WARM, lw=1.5))

# ── Panel 3: 三樣東西 ──
ax3 = fig.add_subplot(gs[1, :])
ax3.set_facecolor(DARK_BG); ax3.axis('off')
ax3.set_xlim(-5, 5); ax3.set_ylim(-1.5, 2.5)
ax3.set_title('三樣東西——嚴柏翰最終的選擇', fontsize=14, color=MIA_WARM,
              fontweight='bold', pad=12)

three = [
    ('方法論', '工具可以帶走\n身份會變，能力不會', '3%', GREEN, '承諾'),
    ('維倫的友誼', '你是這十年裡\n唯一真的東西', '8%', MIA_BLUE, '名字'),
    ('茉莉花', '手不肯放開\n沒有畫面，只有味道', '0.1%', MIA_WARM, '一段音樂'),
]
for x, (name, desc, wt, col, meta) in zip([-3, 0, 3], three):
    for r in [1.15, 1.05]:
        ax3.add_patch(plt.Circle((x, 0.8), r, fc='none', ec=col, alpha=0.1, lw=1))
    ax3.add_patch(plt.Circle((x, 0.8), 0.95, fc=DARK_BG, ec=col, lw=2.5, zorder=2))
    ax3.text(x, 1.2, name, ha='center', fontsize=12, color=col,
             fontweight='bold', zorder=3)
    ax3.text(x, 0.55, desc, ha='center', fontsize=8, color=TEXT,
             alpha=0.8, zorder=3, linespacing=1.4)
    ax3.text(x, -0.3, f'[{wt}]', ha='center', fontsize=9, color=MUTED, zorder=3)
    ax3.text(x, -0.7, meta, ha='center', fontsize=10, color=col,
             alpha=0.6, style='italic', zorder=3)

ax3.plot([-1.8, 1.8], [-1.1, -1.1], color=MUTED, lw=0.8, alpha=0.4)
ax3.text(0, -1.3, 'dp[n][W] = max(...)? No. His hand chose for him.',
         ha='center', fontsize=10, color=MUTED, style='italic')

# ── 標題與引言 ──
fig.suptitle('米亞的演算法筆記 #12 — DP / 0-1 背包：記憶的取捨',
             fontsize=16, color=MIA_BLUE, fontweight='bold', y=0.96)
fig.text(0.5, 0.02,
    '「你的大腦是一個背包。只裝得下這麼多。你留什麼？」 — 第149章〈三樣東西〉',
    ha='center', fontsize=10, color=MIA_WARM, style='italic', alpha=0.9)

# ── 儲存 ──
out = '/Users/william/Downloads/phd_exam/leetcode/記憶駭客_小說/米亞的演算法筆記/Vol2_12_DP_背包.png'
fig.savefig(out, dpi=180, facecolor=DARK_BG, bbox_inches='tight', pad_inches=0.3)
plt.close(fig)
print(f'Saved -> {out}')
