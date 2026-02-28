"""
米亞的演算法筆記 #10 — Topological Sort 視覺化
篡改事件 DAG：死亡證明為源頭（紅色），沿拓撲序展開到全城覆寫
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np, os
from collections import deque

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

# ── DAG（ch126-127 篡改事件鏈）────────────────────────
nodes = ["偽造\n死亡紀錄", "刪除\n遊行紀錄", "清除\n目擊者記憶",
         "銷毀\n物證", "覆蓋\n新聞報導", "篡改\n監控局檔案",
         "修改\n醫療紀錄", "全城\n記憶覆寫"]
edges = [(0,1),(0,2),(0,6),(1,3),(1,4),(2,4),(2,5),(3,7),(4,7),(5,7),(6,5)]
N = len(nodes)

# Kahn's algorithm
adj = {i: [] for i in range(N)}
ind = [0] * N
for u, v in edges:
    adj[u].append(v); ind[v] += 1
q, topo = deque(i for i in range(N) if ind[i] == 0), []
while q:
    v = q.popleft(); topo.append(v)
    for u in adj[v]:
        ind[u] -= 1
        if ind[u] == 0: q.append(u)

# ── 佈局（按拓撲層）──────────────────────────────────
layer_map = {0:0, 1:1, 2:1, 6:1, 3:2, 4:2, 5:2, 7:3}
layer_y = {0: 3.5, 1: 1.5, 2: -0.5, 3: -2.8}
layer_nodes = {}
for nid, ly in layer_map.items():
    layer_nodes.setdefault(ly, []).append(nid)

pos = {}
for ly, nids in layer_nodes.items():
    y = layer_y[ly]; xspan = (len(nids) - 1) * 2.8
    for i, nid in enumerate(sorted(nids)):
        pos[nid] = (-xspan/2 + i*2.8, y)

# ── 繪圖 ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(-6, 6); ax.set_ylim(-4.5, 5.5)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("米亞的演算法筆記 #10 — 篡改事件拓撲排序",
             fontsize=15, color=TEXT, pad=16)

# 主鏈高亮集合
main = {(0,1),(0,2),(1,4),(2,4),(4,7)}

# 有向邊
for u, v in edges:
    xu, yu = pos[u]; xv, yv = pos[v]
    is_m = (u,v) in main
    c, lw = (MIA_BLUE, 2.2) if is_m else (MUTED, 1.2)
    dx, dy = xv-xu, yv-yu
    d = np.hypot(dx, dy); sh = 0.55
    sx, sy = xu + dx*sh/d*.8, yu + dy*sh/d*.8
    ex, ey = xv - dx*sh/d*.8, yv - dy*sh/d*.8
    ax.annotate("", xy=(ex,ey), xytext=(sx,sy),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                mutation_scale=16), zorder=2)

# 節點顏色
ncol = [RED if i==0 else MIA_WARM if i==7 else MIA_BLUE for i in range(N)]

# 節點（圓角矩形 + 序號）
for i in range(N):
    x, y = pos[i]; c = ncol[i]
    a = .9 if i in (0,7) else .7
    ax.text(x, y, nodes[i], ha="center", va="center", fontsize=10,
            color=c, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=c, ec=c, alpha=a*.25),
            zorder=5)
    ax.text(x+1.1, y+.4, f"#{topo.index(i)+1}", ha="center",
            fontsize=8, color=MUTED, zorder=5)

# 源頭光暈
sx, sy = pos[0]
ax.add_patch(plt.Circle((sx,sy), 1.2, fc=RED, alpha=.08, ec="none", zorder=0))
ax.text(sx, sy+1.1, "入度 = 0  ← 起點", ha="center",
        fontsize=9, color=RED, fontweight="bold")

# 終點標記
ex, ey = pos[7]
ax.text(ex, ey-.9, "出度 = 0  ← 終點", ha="center",
        fontsize=9, color=MIA_WARM, fontweight="bold")

# 層級標籤
for ly, y in layer_y.items():
    lbl = ["第 1 步","第 2 步","第 3 步","最終步"][ly]
    ax.text(-5.5, y, lbl, ha="center", fontsize=9, color=MUTED,
            bbox=dict(boxstyle="round,pad=0.3", fc=GRID, ec=MUTED, alpha=.6))

# 統計面板
panel = (f"Kahn's Algorithm\n━━━━━━━━━━━━━━━\n"
         f"節點數：{N}\n邊數：{len(edges)}\n"
         f"拓撲序：{'→'.join(str(i) for i in topo)}\n源頭：死亡紀錄")
ax.text(4.5, 4.8, panel, fontsize=7.5, color=TEXT, family="monospace", va="top",
        bbox=dict(boxstyle="round,pad=0.5", fc=GRID, ec=MUTED, alpha=.8))

# 圖例
handles = [
    mpatches.Patch(fc=RED, alpha=.6, label="源頭：偽造死亡紀錄"),
    mpatches.Patch(fc=MIA_BLUE, alpha=.6, label="中間事件"),
    mpatches.Patch(fc=MIA_WARM, alpha=.6, label="終點：全城覆寫"),
    plt.Line2D([0],[0], color=MIA_BLUE, lw=2, label="主依賴鏈"),
    plt.Line2D([0],[0], color=MUTED, lw=1, label="次要依賴"),
]
ax.legend(handles=handles, loc="lower left", fontsize=8,
          facecolor=DARK_BG, edgecolor=MUTED, labelcolor=TEXT, framealpha=.8)

fig.text(0.5, 0.015,
         "「他們最先偽造的，是死亡證明。」— 第127章〈篡改的順序〉",
         ha="center", fontsize=10, color=MUTED, style="italic")
plt.tight_layout(rect=[0, .04, 1, .95])
out = os.path.join(os.path.dirname(__file__), "Vol2_10_Topological_Sort.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=DARK_BG)
plt.close(fig)
print(f"[done] {out}")
