"""
米亞的演算法筆記 #08 — DFS / BFS 視覺化
左側：DFS 深度優先路徑（記憶迷宮）  右側：BFS 漣漪式擴展（母親記憶）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import deque
import os

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

# ── 建樹（4 層，分岔 2）─────────────────────────────
def build_tree():
    adj, pos = {0: []}, {0: (0, 0)}
    nid, layers = 1, [[0]]
    for d in range(1, 4):
        layer = []
        span = 2 ** (3 - d)
        for p in layers[d - 1]:
            for c in range(2):
                adj.setdefault(p, []).append(nid); adj[nid] = []
                px, py = pos[p]
                pos[nid] = (px + (c - 0.5) * span * 0.8, -d * 1.4)
                layer.append(nid); nid += 1
        layers.append(layer)
    return adj, pos, layers

def dfs_order(adj):
    vis, order, stack = set(), [], [0]
    while stack:
        v = stack.pop()
        if v in vis: continue
        vis.add(v); order.append(v)
        for u in reversed(adj.get(v, [])):
            if u not in vis: stack.append(u)
    return order

def bfs_levels(adj):
    vis, q, levels = {0}, deque([0]), []
    while q:
        lv = []
        for _ in range(len(q)):
            v = q.popleft(); lv.append(v)
            for u in adj.get(v, []):
                if u not in vis: vis.add(u); q.append(u)
        levels.append(lv)
    return levels

# ── 繪圖 ──────────────────────────────────────────
fig, (ax_d, ax_b) = plt.subplots(1, 2, figsize=(16, 8.5))
adj, pos, tree_layers = build_tree()

def draw_edges(ax, adj, pos):
    for v, nb in adj.items():
        for u in nb:
            ax.plot([pos[v][0], pos[u][0]], [pos[v][1], pos[u][1]],
                    color=GRID, lw=1.2, zorder=1)

def setup_ax(ax, title, color):
    ax.set_title(title, fontsize=16, color=color, pad=14)
    ax.set_xlim(-5, 5); ax.set_ylim(-5.5, 1.2)
    ax.set_aspect("equal"); ax.axis("off")

# ── 左：DFS ───────────────────────────────────────
setup_ax(ax_d, "DFS — 一口氣潛到底", MIA_BLUE)
draw_edges(ax_d, adj, pos)
dfs_p = dfs_order(adj)
deep4 = dfs_p[:4]
for i in range(len(deep4) - 1):
    a, b = deep4[i], deep4[i + 1]
    ax_d.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
              color=MIA_BLUE, lw=3.5, zorder=2, alpha=0.9)
for v, (x, y) in pos.items():
    c, s = (MIA_BLUE, 420) if v in deep4 else (MUTED, 200)
    ax_d.scatter(x, y, s=s, c=c, zorder=5, edgecolors="none", alpha=0.85)
for idx, nd in enumerate(dfs_p[:7]):
    x, y = pos[nd]
    ax_d.text(x, y + 0.45, str(idx + 1), ha="center", va="center",
              fontsize=8, color=MIA_WARM, fontweight="bold")
# 防禦體
ex, ey = pos[deep4[-1]]
ax_d.scatter(ex, ey, s=700, c=RED, zorder=6, alpha=0.5)
ax_d.text(ex, ey - 0.6, "防禦體", ha="center", fontsize=9, color=RED)
# 回溯箭頭
px2, py2 = pos[deep4[-2]]
ax_d.annotate("", xy=(px2 + 0.2, py2), xytext=(ex + 0.2, ey + 0.15),
              arrowprops=dict(arrowstyle="->", color=MIA_WARM, lw=2, ls="--"))
ax_d.text(px2 + 0.9, (ey + py2) / 2, "回溯", fontsize=9,
          color=MIA_WARM, style="italic")
ax_d.text(0, -5.0, "「碰壁就退一步。退一步不是失敗。」",
          ha="center", fontsize=10, color=MUTED, style="italic")

# ── 右：BFS ───────────────────────────────────────
setup_ax(ax_b, "BFS — 漣漪式擴展", MIA_WARM)
draw_edges(ax_b, adj, pos)
levels = bfs_levels(adj)
lv_colors = [MIA_WARM, GREEN, MIA_BLUE, RED]
for li, lv in enumerate(levels):
    c = lv_colors[li % 4]
    for nd in lv:
        ax_b.scatter(*pos[nd], s=350, c=c, zorder=5, edgecolors="none", alpha=0.8)
    if li > 0:
        r = 2 ** (3 - li) * 0.8 + 0.6
        circle = plt.Circle((0, -li * 1.4), r, fill=False,
                             edgecolor=c, lw=1.5, ls="--", alpha=0.35)
        ax_b.add_patch(circle)
        ax_b.text(r + 0.4, -li * 1.4, f"第{li}圈", fontsize=9,
                  color=c, va="center")
flat = [n for l in levels for n in l]
for idx, nd in enumerate(flat[:8]):
    x, y = pos[nd]
    ax_b.text(x, y + 0.45, str(idx + 1), ha="center", va="center",
              fontsize=8, color=DARK_BG, fontweight="bold")
ax_b.text(0, -5.0, "「先看清楚周圍，再往外走一步。」",
          ha="center", fontsize=10, color=MUTED, style="italic")

# ── 輸出 ──────────────────────────────────────────
fig.suptitle("米亞的演算法筆記 #08 — DFS 深潛 vs BFS 漣漪",
             fontsize=13, color=TEXT, y=0.97)
fig.text(0.5, 0.01, "Vol 2 · ch86-87, ch90, ch103 · 記憶駭客",
         ha="center", fontsize=9, color=MUTED)
plt.tight_layout(rect=[0, 0.03, 1, 0.94])
out = os.path.join(os.path.dirname(__file__), "Vol2_08_DFS_BFS.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=DARK_BG)
plt.close(fig)
print(f"[done] {out}")
