"""
米亞的演算法筆記 #04 — Stack / Queue 視覺化
張國棟的七層記憶：逐層 pop，第七層是空的
生成檔案：Vol1_04_Stack_Queue.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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

# ── 七層記憶資料 ──
layers = [
    (0, RED, "NULL—空"), (11, MUTED, "模糊光影"), (23, MUTED, "孤兒院"),
    (41, MIA_WARM, "虛構婚姻"), (65, MIA_WARM, "留學歸國"),
    (78, MIA_BLUE, "車禍倖存"), (92, GREEN, "退休教授"),
]

fig = plt.figure(figsize=(14, 9)); fig.patch.set_facecolor(DARK_BG)

# ── 左半：Stack 逐層 pop ──
ax_s = fig.add_axes([0.04, 0.08, 0.44, 0.78])
ax_s.set_facecolor(DARK_BG); ax_s.set_xlim(-0.5, 6.5); ax_s.set_ylim(-1, 8.5)
ax_s.axis("off")
ax_s.set_title("Stack：張國棟的七層記憶", fontsize=15, color=MIA_BLUE,
               pad=12, fontweight="bold")

bw, bh = 1.05, 0.64
stages = [7, 5, 3, 0]
for si, rem in enumerate(stages):
    xo = si * 1.55 - 0.3
    for i in range(7):
        y = i * (bh + 0.08)
        active = i < rem
        fc = layers[i][1] if active else MUTED
        rect = FancyBboxPatch((xo, y), bw, bh, boxstyle="round,pad=0.03",
                              facecolor=fc, edgecolor=TEXT,
                              alpha=0.85 if active else 0.12, linewidth=0.8)
        ax_s.add_patch(rect)
        if active:
            ax_s.text(xo + bw/2, y + bh/2, f"{layers[i][0]}%",
                      ha="center", va="center", fontsize=6.5,
                      color=DARK_BG, fontweight="bold")
        elif i == rem and rem < 7:
            ax_s.text(xo + bw/2, y + bh/2, "pop\u2191", ha="center",
                      va="center", fontsize=6, color=RED, fontweight="bold")
    popped = 7 - rem
    lbl = "初始" if rem == 7 else ("全部 pop\n\u2192 NULL" if rem == 0
                                   else f"pop \u00d7{popped}")
    ax_s.text(xo + bw/2, -0.6, lbl, ha="center", va="center", fontsize=7,
              color=MIA_WARM if rem == 0 else TEXT)

for i in range(3):
    x1 = -0.3 + i * 1.55 + bw + 0.08; x2 = -0.3 + (i+1) * 1.55 - 0.08
    ax_s.annotate("", xy=(x2, 3.5), xytext=(x1, 3.5),
                  arrowprops=dict(arrowstyle="->", color=RED, lw=1.5, alpha=0.7))

ax_s.text(3.0, 8.0, "LIFO：最後疊上的記憶，最先被剝開",
          ha="center", fontsize=9, color=MUTED, style="italic")

# ── 右半：Queue 修復排程 ──
ax_q = fig.add_axes([0.54, 0.08, 0.44, 0.78])
ax_q.set_facecolor(DARK_BG); ax_q.set_xlim(-0.5, 7.5); ax_q.set_ylim(-1.5, 8.5)
ax_q.axis("off")
ax_q.set_title("Queue：安全修復排程", fontsize=15, color=MIA_WARM,
               pad=12, fontweight="bold")

repairs = [("L2", "錨點建立", 3, GREEN), ("L4", "衝突移除", 8, RED),
           ("L6", "重新校準", 2, MIA_BLUE), ("L7", "表層維持", 1, MIA_BLUE)]
qy, sw, sh = 5.5, 1.5, 2.2

for idx, (layer, action, risk, clr) in enumerate(repairs):
    x = idx * (sw + 0.3) + 0.3
    ax_q.add_patch(FancyBboxPatch((x, qy - sh/2), sw, sh,
                   boxstyle="round,pad=0.08", facecolor=clr,
                   edgecolor=TEXT, alpha=0.3, linewidth=1.2))
    ax_q.text(x + sw/2, qy + 0.5, layer, ha="center", va="center",
              fontsize=13, color=clr, fontweight="bold")
    ax_q.text(x + sw/2, qy - 0.05, action, ha="center", va="center",
              fontsize=8, color=TEXT)
    ax_q.text(x + sw/2, qy - 0.55, f"風險: {risk}", ha="center",
              va="center", fontsize=7.5, color=MUTED)
    ax_q.text(x + sw/2, qy + 1.35, f"#{idx+1}", ha="center", va="center",
              fontsize=10, color=MIA_WARM, fontweight="bold")
    if idx < len(repairs) - 1:
        ax_q.annotate("", xy=(x + sw + 0.15, qy), xytext=(x + sw + 0.02, qy),
                      arrowprops=dict(arrowstyle="->", color=MIA_WARM, lw=1.5))

ax_q.text(6.8, qy + 1.6, "enqueue \u2190", fontsize=9, color=GREEN,
          ha="right", va="center")
ax_q.text(0.3, qy + 1.6, "\u2192 dequeue", fontsize=9, color=RED,
          ha="left", va="center")

# 靈魂句
ax_q.text(3.75, 1.8, "\u300c彈出。彈出。彈出。空的。\u300d",
          ha="center", fontsize=13, color=RED, fontweight="bold",
          alpha=0.9, style="italic")
ax_q.text(3.75, 1.0,
          "那是最可怕的數據點——\n不是因為沒有資料，是因為從來就沒有過。",
          ha="center", fontsize=9, color=MUTED, style="italic", linespacing=1.6)

# ── 主標題 ──
fig.text(0.5, 0.96, "米亞的演算法筆記 #04 — Stack / Queue",
         ha="center", fontsize=17, color=TEXT, fontweight="bold")
fig.text(0.5, 0.925, "ch19-20 張國棟的七層記憶：每一層都是善意的謊言",
         ha="center", fontsize=10, color=MUTED)

# ── 輸出 ──
out = "/Users/william/Downloads/phd_exam/leetcode/記憶駭客_小說/米亞的演算法筆記/Vol1_04_Stack_Queue.png"
fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=DARK_BG, edgecolor="none")
plt.close(fig)
print(f"OK {out}")
