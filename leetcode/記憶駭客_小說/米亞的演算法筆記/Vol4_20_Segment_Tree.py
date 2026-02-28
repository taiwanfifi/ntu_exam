"""
米亞的演算法筆記 #20 — Segment Tree 視覺化
《記憶駭客》第256章、第305-309章
「線段樹能管理區間。但它填不滿空的那些。」
上半部：線段樹結構（8天健康度，含空白區間 + 查詢路徑高亮）
下半部：原始資料條形圖
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── 色彩 ──
DARK_BG = '#0a0e14'; MIA_BLUE = '#4fc1e9'; MIA_WARM = '#f5c542'
TEXT = '#d0d7de'; MUTED = '#6e7681'; GRID = '#1c2028'
RED = '#ff6b6b'; GREEN = '#7bc87b'

for font in ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.family'] = font; break
    except Exception: continue
plt.rcParams.update({'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG})

fig = plt.figure(figsize=(17, 11))
fig.suptitle('米亞的演算法筆記 #20 — Segment Tree（線段樹）\n'
             '「線段樹能管理區間。但它填不滿空的那些。」— 第309章',
             fontsize=15, color=MIA_WARM, fontweight='bold', y=0.97)

# ── 資料與建樹 ──
data = [72, 85, 63, 91, 0, 0, 78, 88]
days = ['Day1','Day2','Day3','Day4','Day5','Day6','Day7','Day8']
tree = [0] * 16

def build(p, l, r):
    if l == r: tree[p] = data[l]; return
    m = (l+r)//2; build(2*p, l, m); build(2*p+1, m+1, r)
    tree[p] = tree[2*p] + tree[2*p+1]
build(1, 0, 7)

# 查詢 [2,5] 標記路徑
ql, qr = 2, 5
q_hits, q_path = set(), set()
def mark(p, l, r):
    q_path.add(p)
    if ql <= l and r <= qr: q_hits.add(p); return
    if l > qr or r < ql: return
    m = (l+r)//2; mark(2*p, l, m); mark(2*p+1, m+1, r)
mark(1, 0, 7)

# ── 上半部：線段樹 ──
ax = fig.add_axes([0.03, 0.28, 0.94, 0.62])
ax.set_xlim(-1, 17); ax.set_ylim(-0.5, 8.5); ax.axis('off')
ax.set_title('全城記憶健康度 — 線段樹結構（8天簡化）', fontsize=13, color=MIA_BLUE, pad=5)

pos = {}
def calc(p, l, r, d, xl, xr):
    pos[p] = ((xl+xr)/2, 7.5-d*1.8, l, r)
    if l == r: return
    m = (l+r)//2; calc(2*p, l, m, d+1, xl, (xl+xr)/2); calc(2*p+1, m+1, r, d+1, (xl+xr)/2, xr)
calc(1, 0, 7, 0, 0.5, 15.5)

# 畫邊
for p in pos:
    for ch in [2*p, 2*p+1]:
        if ch in pos:
            x1, y1 = pos[p][0], pos[p][1]
            x2, y2 = pos[ch][0], pos[ch][1]
            ec = MIA_BLUE if (p in q_path and ch in q_path) else GRID
            ax.plot([x1, x2], [y1-0.35, y2+0.35], color=ec, lw=1.8 if ec==MIA_BLUE else 0.8)

# 畫節點
for p, (x, y, l, r) in pos.items():
    v = tree[p]; empty = (v==0); hit = p in q_hits; vis = p in q_path
    if hit: fc, ec, lw = GREEN+'55', GREEN, 2.5
    elif empty and l==r: fc, ec, lw = RED+'22', RED, 1.8
    elif vis: fc, ec, lw = MIA_BLUE+'33', MIA_BLUE, 1.8
    else: fc, ec, lw = GRID, MUTED, 1
    nw = max(0.8, (r-l+1)*0.25)
    rect = mpatches.FancyBboxPatch((x-nw/2, y-0.3), nw, 0.6,
        boxstyle='round,pad=0.06', facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x, y+0.05, str(v), ha='center', va='center',
            fontsize=10 if l==r else 11, color=TEXT, fontweight='bold')
    ilbl = f'[{l},{r}]' if l != r else days[l]
    ic = RED if (empty and l==r) else (GREEN if hit else MUTED)
    ax.text(x, y-0.45, ilbl, ha='center', va='top', fontsize=7.5, color=ic)
    if empty and l == r:
        ax.text(x, y+0.5, '空白', ha='center', fontsize=7, color=RED, style='italic')

# 圖例
ax.text(14, 7.5, f'查詢：Day{ql+1}~Day{qr+1}', fontsize=11, color=GREEN, fontweight='bold')
ax.text(14, 6.9, f'結果：{tree[5]}+{tree[6]}={tree[5]+tree[6]}', fontsize=10, color=GREEN)
for i, (t, c) in enumerate([('綠色=命中',GREEN),('藍色=路徑',MIA_BLUE),('紅色=空白',RED)]):
    ax.text(14, 6.3-i*0.5, t, fontsize=8.5, color=c)

# ── 下半部：條形圖 ──
ax2 = fig.add_axes([0.08, 0.04, 0.84, 0.2])
ax2.set_title('原始資料：8天記憶健康度', fontsize=11, color=MIA_BLUE, pad=5)
bc = [RED+'aa' if v==0 else (GREEN+'cc' if ql<=i<=qr else MIA_BLUE+'88') for i,v in enumerate(data)]
bars = ax2.bar(range(8), data, color=bc, edgecolor=DARK_BG, width=0.7)
for i, (bar, v) in enumerate(zip(bars, data)):
    lbl = f'{v}' if v > 0 else '空白'
    ax2.text(bar.get_x()+bar.get_width()/2, max(v,5)+3, lbl,
             ha='center', va='bottom', fontsize=9, color=TEXT if v>0 else RED, fontweight='bold')
ax2.annotate('', xy=(ql-0.3, -12), xytext=(qr+0.3, -12),
             arrowprops=dict(arrowstyle='<->', color=GREEN, lw=2))
ax2.text((ql+qr)/2, -18, f'查詢區間 [{ql},{qr}]', ha='center', fontsize=9,
         color=GREEN, fontweight='bold')
ax2.set_xticks(range(8)); ax2.set_xticklabels(days, fontsize=9)
ax2.set_ylabel('健康度', fontsize=9); ax2.set_ylim(-22, 105)
for s in ['top','right']: ax2.spines[s].set_visible(False)
for s in ['bottom','left']: ax2.spines[s].set_color(MUTED)
ax2.set_facecolor(DARK_BG); ax2.grid(axis='y', color=GRID, lw=0.5, alpha=0.5)

out_path = os.path.join(os.path.dirname(__file__), 'Vol4_20_Segment_Tree.png')
plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=DARK_BG, edgecolor='none')
plt.close()
print(f'已儲存：{out_path}')
