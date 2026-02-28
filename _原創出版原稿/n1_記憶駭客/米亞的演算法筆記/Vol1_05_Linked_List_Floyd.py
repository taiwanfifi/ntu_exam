"""
米亞的演算法筆記 #05 — Linked List / Floyd 判圈法視覺化
蘇曉晴的無盡星期三：記憶被困在循環中
生成檔案：Vol1_05_Linked_List_Floyd.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import numpy as np

# ── 色彩系統 ──
MIA_BLUE, MIA_WARM, DARK_BG = "#4fc1e9", "#f5c542", "#0a0e14"
TEXT, MUTED, GRID = "#d0d7de", "#6e7681", "#1c2028"
RED, GREEN = "#ff6b6b", "#7bc87b"

# ── 中文字型 ──
def get_cjk():
    from matplotlib.font_manager import FontProperties
    for f in ["PingFang TC", "Heiti TC", "Arial Unicode MS"]:
        try:
            if FontProperties(family=f).get_name() == f: return f
        except Exception: pass
    return "Arial Unicode MS"

plt.rcParams.update({
    "font.family": get_cjk(), "text.color": TEXT,
    "axes.labelcolor": TEXT, "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": DARK_BG, "axes.facecolor": DARK_BG,
})

fig = plt.figure(figsize=(14, 9)); fig.patch.set_facecolor(DARK_BG)
ax = fig.add_axes([0.05, 0.12, 0.90, 0.75])
ax.set_facecolor(DARK_BG); ax.set_xlim(-2, 16); ax.set_ylim(-5.5, 5.5)
ax.axis("off")

# ── 非環段：Day 1-15 ──
lin_x = [i * 1.8 for i in range(6)]
lin_y, lin_lbl = 3.5, ["1", "4", "7", "10", "13", "15"]

for idx, (x, lbl) in enumerate(zip(lin_x, lin_lbl)):
    ax.add_patch(Circle((x, lin_y), 0.38, fc=GRID, ec=MIA_BLUE, lw=1.5, alpha=0.85))
    ax.text(x, lin_y, lbl, ha="center", va="center", fontsize=7,
            color=MIA_BLUE, fontweight="bold")
    ax.text(x, lin_y - 0.65, f"Day {lbl}", ha="center", va="top",
            fontsize=5.5, color=MUTED)
    if idx < 5:
        ax.annotate("", xy=(lin_x[idx+1] - 0.42, lin_y),
                    xytext=(x + 0.42, lin_y),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))

# ── 環段：Day 16-52 ──
cx, cy, cr = 10.5, 0.0, 3.0
n_nodes = 12
days = [16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 52]
cnodes = []
for i in range(n_nodes):
    ang = np.pi/2 - i * 2 * np.pi / n_nodes
    cnodes.append((cx + cr * np.cos(ang), cy + cr * np.sin(ang)))

# 直線段 → 環入口
ax.annotate("", xy=(cnodes[0][0] - 0.42, cnodes[0][1] + 0.15),
            xytext=(lin_x[-1] + 0.42, lin_y),
            arrowprops=dict(arrowstyle="-|>", color=MIA_WARM, lw=2.0,
                            connectionstyle="arc3,rad=-0.3"))
mx = (lin_x[-1] + cnodes[0][0]) / 2 + 0.5
my = (lin_y + cnodes[0][1]) / 2 + 0.8
ax.text(mx, my, "進入環", fontsize=8, color=MIA_WARM, ha="center",
        fontweight="bold")

# 繪製環節點
for idx, ((x, y), day) in enumerate(zip(cnodes, days)):
    is_entry, is_funeral = (day == 16), (day == 37)
    if is_entry:
        ec, fc, al = MIA_WARM, MIA_WARM, 0.35
    elif is_funeral:
        ec, fc, al = RED, RED, 0.35
    else:
        ec, fc, al = MUTED, GRID, 0.7
    ax.add_patch(Circle((x, y), 0.38, fc=fc, ec=ec,
                        lw=1.8 if is_entry else 1.2, alpha=al))
    ax.text(x, y, str(day), ha="center", va="center", fontsize=7,
            color=MIA_WARM if is_entry else TEXT, fontweight="bold")
    if is_entry:
        ax.text(x, y + 0.65, "環入口", ha="center", va="bottom",
                fontsize=7, color=MIA_WARM, fontweight="bold")
        ax.text(x, y + 1.05, "第一個星期三", ha="center", va="bottom",
                fontsize=6, color=MIA_WARM, alpha=0.7)
    if is_funeral:
        ax.text(x, y - 0.65, "父親葬禮", ha="center", va="top",
                fontsize=6.5, color=RED, fontweight="bold")
    # 環內箭頭
    nx, ny = cnodes[(idx + 1) % n_nodes]
    dx, dy = nx - x, ny - y
    d = np.hypot(dx, dy)
    if d > 0:
        ux, uy = dx/d, dy/d
        is_close = (idx == n_nodes - 1)
        ax.annotate("", xy=(nx - ux*0.42, ny - uy*0.42),
                    xytext=(x + ux*0.42, y + uy*0.42),
                    arrowprops=dict(arrowstyle="-|>",
                                   color=RED if is_close else MUTED,
                                   lw=1.8 if is_close else 1.0,
                                   alpha=0.9 if is_close else 0.6))

ax.text(cx, cy, "c = 37 天\n永恆的星期三", ha="center", va="center",
        fontsize=10, color=TEXT, alpha=0.6, style="italic", linespacing=1.5)

# ── 龜兔指標 ──
tx, ty = cnodes[4]  # Day 28
ax.annotate("slow（龜）", xy=(tx, ty - 0.5), xytext=(tx - 1.8, ty - 1.8),
            fontsize=9, color=GREEN, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
ax.text(tx - 1.8, ty - 2.3, "每次 1 步", ha="center", fontsize=7,
        color=GREEN, alpha=0.7)

hx, hy = cnodes[8]  # Day 40
ax.annotate("fast（兔）", xy=(hx + 0.4, hy - 0.3),
            xytext=(hx + 2.0, hy - 1.5), fontsize=9, color=RED,
            fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
ax.text(hx + 2.0, hy - 2.0, "每次 2 步", ha="center", fontsize=7,
        color=RED, alpha=0.7)

# ── 說明文字 ──
ax.text(7.5, -4.8,
        "Floyd 判圈法：slow 走 a+b 步，fast 走 2(a+b) 步 → 環內相遇",
        ha="center", fontsize=9, color=MUTED)
ax.text(7.5, -5.3,
        "a=15, c=37 → 相遇後一指標移回 head，同速前進 → Day 16 相遇 = 環入口",
        ha="center", fontsize=7.5, color=MUTED, alpha=0.7)

# ── 靈魂句 ──
fig.text(0.5, 0.04,
         "「她不知道自己在重複。那是最壞的迴圈——\n"
         "不是因為出不去，而是因為裡面太舒服了。」",
         ha="center", fontsize=12, color=RED, style="italic",
         alpha=0.85, linespacing=1.6)

# ── 標題 ──
fig.text(0.5, 0.96, "米亞的演算法筆記 #05 — Linked List / Floyd 判圈法",
         ha="center", fontsize=17, color=TEXT, fontweight="bold")
fig.text(0.5, 0.925, "ch27-29 蘇曉晴的無盡星期三：記憶被困在循環中",
         ha="center", fontsize=10, color=MUTED)

# ── 圖例 ──
ax.legend(handles=[
    mpatches.Patch(fc=MIA_WARM, ec=MIA_WARM, alpha=0.5, label="環入口 (Day 16)"),
    mpatches.Patch(fc=RED, ec=RED, alpha=0.4, label="父親葬禮 (Day 37)"),
    mpatches.Patch(fc=GREEN, ec=GREEN, alpha=0.5, label="slow 指標（龜）"),
    mpatches.Patch(fc=RED, ec=RED, alpha=0.7, label="fast 指標（兔）"),
], loc="upper left", fontsize=8, facecolor=DARK_BG, edgecolor=MUTED,
   labelcolor=TEXT, framealpha=0.8)

# ── 輸出 ──
out = "/Users/william/Downloads/phd_exam/leetcode/記憶駭客_小說/米亞的演算法筆記/Vol1_05_Linked_List_Floyd.png"
fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=DARK_BG, edgecolor="none")
plt.close(fig)
print(f"OK {out}")
