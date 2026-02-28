"""
米亞的演算法筆記 #09 — Graph / 連通分量 視覺化
記憶網絡碎裂：連通分量作為孤立島嶼，被剪斷的邊以紅色虛線呈現
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np, os

# ── 色票與字型 ─────────────────────────────────────
DARK_BG = "#0a0e14"; MIA_BLUE = "#4fc1e9"; MIA_WARM = "#f5c542"
TEXT = "#d0d7de"; MUTED = "#6e7681"; GRID = "#1c2028"
RED = "#ff6b6b"; GREEN = "#7bc87b"

def _font():
    from matplotlib.font_manager import FontProperties
    for n in ["PingFang TC", "Heiti TC", "Arial Unicode MS"]:
        try:
            if FontProperties(family=n).get_name() == n: return n
        except Exception: pass
    return "sans-serif"

plt.rcParams.update({"font.family": _font(), "axes.facecolor": DARK_BG,
    "figure.facecolor": DARK_BG, "text.color": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED})

# ── 簇定義（5 個連通分量，模擬 123 座島的縮影）──────────
np.random.seed(42)
clusters = [
    {"c": (-3.5,  2.5), "n": 14, "r": 1.6, "lbl": "島嶼 A\n4,200 人"},
    {"c": ( 3.0,  2.8), "n": 10, "r": 1.3, "lbl": "島嶼 B\n2,800 人"},
    {"c": (-3.0, -2.0), "n":  7, "r": 1.1, "lbl": "島嶼 C\n890 人"},
    {"c": ( 3.5, -1.5), "n":  5, "r": 0.9, "lbl": "島嶼 D\n12 人"},
    {"c": ( 0.0,  0.0), "n":  2, "r": 0.4, "lbl": "孤立者"},
]
CC = [MIA_BLUE, GREEN, MIA_WARM, "#c792ea", MUTED]

pos, cid, ranges = [], [], []
off = 0
for ci, cl in enumerate(clusters):
    cx, cy = cl["c"]; n = cl["n"]
    ang = np.linspace(0, 2*np.pi, n, endpoint=False) + np.random.uniform(0, .3, n)
    rad = cl["r"] * np.sqrt(np.random.uniform(.15, .95, n))
    for a, r in zip(ang, rad):
        pos.append((cx + r*np.cos(a), cy + r*np.sin(a)))
        cid.append(ci)
    ranges.append((off, off + n)); off += n

# 簇內邊
intra = []
for s, e in ranges:
    for i in range(s, e):
        for j in range(i+1, e):
            d = np.hypot(pos[i][0]-pos[j][0], pos[i][1]-pos[j][1])
            if d < 1.2 and np.random.random() < 0.6:
                intra.append((i, j))

# 被剪斷的跨簇邊
cut = []
for ca, cb in [(0,1),(0,2),(1,3),(2,3),(0,4),(1,4)]:
    sa, ea = ranges[ca]; sb, eb = ranges[cb]
    cut.append((np.random.randint(sa,ea), np.random.randint(sb,eb)))
    if np.random.random() < .4:
        cut.append((np.random.randint(sa,ea), np.random.randint(sb,eb)))

# ── 繪圖 ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(-6.5, 6.5); ax.set_ylim(-4.5, 5.5)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("米亞的演算法筆記 #09 — 記憶網絡連通分量",
             fontsize=15, color=TEXT, pad=16)

# 被剪斷的邊
for a, b in cut:
    xa, ya = pos[a]; xb, yb = pos[b]
    ax.plot([xa,xb],[ya,yb], color=RED, lw=1.5, ls="--", alpha=.55, zorder=1)
    ax.scatter((xa+xb)/2, (ya+yb)/2, marker="x", s=60, c=RED, zorder=6, alpha=.7)

# 簇內邊
for a, b in intra:
    ax.plot([pos[a][0],pos[b][0]], [pos[a][1],pos[b][1]],
            color=GRID, lw=.9, alpha=.7, zorder=2)

# 島嶼背景圈 + 標籤
for ci, cl in enumerate(clusters):
    cx, cy = cl["c"]
    circle = plt.Circle((cx,cy), cl["r"]+.4, fill=True,
        facecolor=CC[ci], alpha=.06, edgecolor=CC[ci], lw=1.2, zorder=0)
    ax.add_patch(circle)
    ax.text(cx, cy - cl["r"] - .55, cl["lbl"], ha="center", va="top",
            fontsize=9, color=CC[ci], fontweight="bold")

# 節點
for i, (x, y) in enumerate(pos):
    iso = (cid[i] == 4)
    ax.scatter(x, y, s=80 if iso else 30, c=CC[cid[i]], zorder=5,
               edgecolors=RED if iso else "none", linewidths=1.2 if iso else 0,
               alpha=1.0 if iso else .85)

# 孤立者標籤
ax.text(0, .7, "度數 = 0", ha="center", fontsize=8, color=RED, style="italic")

# 統計面板
stats = ("ch120-121 數據\n━━━━━━━━━━━━━\n節點：23,000 人\n"
         "連通分量：123\n最大島：4,200\n最小島：12\n孤立者：17")
ax.text(-6.0, 4.8, stats, fontsize=8, color=TEXT, family="monospace", va="top",
        bbox=dict(boxstyle="round,pad=0.5", fc=GRID, ec=MUTED, alpha=.8))

# 圖例
handles = [
    mpatches.Patch(fc=GRID, ec=GRID, label="存活的邊"),
    plt.Line2D([0],[0], color=RED, ls="--", lw=1.5, label="被剪斷的邊"),
    plt.Line2D([0],[0], marker="o", color="none", mfc=MIA_BLUE, ms=6, label="島嶼內節點"),
    plt.Line2D([0],[0], marker="o", color="none", mfc=MUTED, mec=RED, ms=6, label="孤立節點"),
]
ax.legend(handles=handles, loc="upper right", fontsize=9,
          facecolor=DARK_BG, edgecolor=MUTED, labelcolor=TEXT, framealpha=.8)

fig.text(0.5, 0.02, "「人是節點。記憶是邊。有人在剪邊。」— 第120章〈斷裂〉",
         ha="center", fontsize=10, color=MUTED, style="italic")
plt.tight_layout(rect=[0, .05, 1, .95])
out = os.path.join(os.path.dirname(__file__), "Vol2_09_Graph_連通分量.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=DARK_BG)
plt.close(fig)
print(f"[done] {out}")
