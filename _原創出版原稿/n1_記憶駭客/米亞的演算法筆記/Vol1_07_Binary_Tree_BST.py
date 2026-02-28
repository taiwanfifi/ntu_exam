"""
米亞的演算法筆記 #07 — Binary Tree / BST 視覺化
「根不是技能。根是『為什麼』。」
左圖：鋼琴師李曼筠的記憶之樹，標記被切斷的連結。
右圖：三種走訪順序（Preorder / Inorder / Postorder）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

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

# ── 鋼琴師的記憶之樹 (depth 3, 15 nodes) ──
nodes = {
    'root': ('為什麼\n彈琴', 0.5, 0.92), 'L1': ('音階\n感覺', 0.25, 0.72),
    'R1': ('節拍\n感覺', 0.75, 0.72), 'L1L': ('和弦', 0.13, 0.52),
    'L1R': ('踏板', 0.37, 0.52), 'R1L': ('指法', 0.63, 0.52),
    'R1R': ('呼吸', 0.87, 0.52), 'L1LL': ('蕭邦', 0.07, 0.32),
    'L1LR': ('貝多芬', 0.19, 0.32), 'L1RL': ('德布西', 0.31, 0.32),
    'L1RR': ('比賽', 0.43, 0.32), 'R1LL': ('音樂會', 0.57, 0.32),
    'R1LR': ('練習室', 0.69, 0.32), 'R1RL': ('祖母', 0.81, 0.32),
    'R1RR': ('掌聲', 0.93, 0.32),
}
edges = [('root','L1',True), ('root','R1',False),   # True = 被切斷
    ('L1','L1L',False), ('L1','L1R',False), ('R1','R1L',False), ('R1','R1R',False),
    ('L1L','L1LL',False), ('L1L','L1LR',False), ('L1R','L1RL',False),
    ('L1R','L1RR',False), ('R1L','R1LL',False), ('R1L','R1LR',False),
    ('R1R','R1RL',False), ('R1R','R1RR',False)]
depth_labels = {0.92: '核心動機', 0.72: '基礎技能',
                0.52: '進階技能', 0.32: '曲目/經歷/情感'}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 9.5),
                                gridspec_kw={'width_ratios': [1.3, 1]})
# ═══ 左圖：記憶之樹 ═══
ax1.set_xlim(-0.02, 1.02); ax1.set_ylim(0.2, 1.02); ax1.axis('off')

for pk, ck, cut in edges:
    px, py = nodes[pk][1], nodes[pk][2]
    cx, cy = nodes[ck][1], nodes[ck][2]
    if cut:
        ax1.plot([px,cx], [py,cy], '--', color=RED, lw=2.5, alpha=0.8)
        mx, my = (px+cx)/2, (py+cy)/2
        ax1.plot(mx, my, 'x', color=RED, markersize=14, markeredgewidth=3)
        ax1.text(mx-0.06, my+0.01, '切斷', fontsize=8, color=RED, fontweight='bold')
    else:
        ec = MIA_BLUE if ck.startswith('L') else MIA_WARM
        ax1.plot([px,cx], [py,cy], '-', color=ec, lw=1.5, alpha=0.5)

for key, (label, x, y) in nodes.items():
    if key == 'root':
        nc, fc, ec, lw = MIA_WARM, DARK_BG, MIA_WARM, 2.5
    elif key == 'L1':
        nc, fc, ec, lw = RED, '#1a0505', RED, 2
    elif key.startswith('L'):
        nc, fc, ec, lw = MIA_BLUE, '#0a1520', MIA_BLUE, 1.2
    else:
        nc, fc, ec, lw = MIA_WARM, '#1a1505', MIA_WARM, 1.2
    ax1.add_patch(plt.Circle((x,y), 0.035, facecolor=fc, edgecolor=ec,
                              linewidth=lw, zorder=5))
    fs = 6.5 if '\n' in label else 7.5
    ax1.text(x, y, label, ha='center', va='center',
             fontsize=fs, color=nc, fontweight='bold', zorder=6)

for yv, dl in depth_labels.items():
    ax1.text(-0.01, yv, dl, ha='right', va='center', fontsize=8,
             color=MUTED, style='italic')

ax1.legend(handles=[
    mpatches.Patch(facecolor='none', edgecolor=RED, linestyle='--',
                   linewidth=2, label='被切斷（技能之根）'),
    mpatches.Patch(facecolor=MIA_BLUE, alpha=0.6, label='技能側（左子樹）'),
    mpatches.Patch(facecolor=MIA_WARM, alpha=0.6, label='情感側（右子樹）')],
    loc='lower left', fontsize=8, framealpha=0.3,
    facecolor=DARK_BG, edgecolor=MUTED)
ax1.set_title('ch93-94 鋼琴師李曼筠的記憶之樹\n「根斷了。但枝葉還在風中搖晃。」',
              fontsize=13, color=MIA_BLUE, pad=12)

# ═══ 右圖：三種走訪 ═══
#       4
#      / \
#     2   6
#    / \ / \
#   1  3 5  7
stree = {4:(0.5,0.88), 2:(0.28,0.65), 6:(0.72,0.65),
         1:(0.14,0.42), 3:(0.42,0.42), 5:(0.58,0.42), 7:(0.86,0.42)}
sedges = [(4,2),(4,6),(2,1),(2,3),(6,5),(6,7)]
travs = [
    ('Preorder\n(根左右)', '4 → 2 → 1 → 3 → 6 → 5 → 7', 0.28, MIA_BLUE,
     '維倫的方式：\n先問「為什麼」'),
    ('Inorder\n(左根右)',  '1 → 2 → 3 → 4 → 5 → 6 → 7', 0.17, GREEN,
     'BST 排序結果：\n一個人的時間線'),
    ('Postorder\n(左右根)', '1 → 3 → 2 → 5 → 7 → 6 → 4', 0.06, MIA_WARM,
     '篡改者的手法：\n最後才碰根'),
]

ax2.set_xlim(-0.02, 1.02); ax2.set_ylim(-0.05, 1.02); ax2.axis('off')

for p, c in sedges:
    ax2.plot([stree[p][0], stree[c][0]], [stree[p][1], stree[c][1]],
             '-', color=MUTED, lw=1.2, alpha=0.4)
for v, (x, y) in stree.items():
    ax2.add_patch(plt.Circle((x,y), 0.032, facecolor=DARK_BG,
                              edgecolor=MIA_BLUE, linewidth=1.5, zorder=5))
    ax2.text(x, y, str(v), ha='center', va='center',
             fontsize=11, color=TEXT, fontweight='bold', zorder=6)

ax2.text(0.5, 0.95, 'BST 性質：左 < 根 < 右',
         ha='center', fontsize=10, color=MIA_BLUE, fontweight='bold')

for name, seq, yb, color, meaning in travs:
    ax2.text(0.02, yb+0.04, name, ha='left', va='center',
             fontsize=9, color=color, fontweight='bold')
    ax2.text(0.22, yb+0.04, seq, ha='left', va='center',
             fontsize=9.5, color=TEXT)
    ax2.text(0.72, yb+0.04, meaning, ha='left', va='center',
             fontsize=7.5, color=MUTED, style='italic')

ax2.text(0.02, -0.02, 'BST 搜尋 target=5：', fontsize=9, color=RED)
ax2.text(0.35, -0.02, '4 → 6 (左轉) → 5 (找到!)', fontsize=9, color=RED)
ax2.set_title('三種走訪 = 三種理解一個人的方式',
              fontsize=13, color=MIA_WARM, pad=12)

fig.suptitle('米亞的演算法筆記 #07 — Binary Tree / BST\n'
             '「根不是技能。根是為什麼。」',
             fontsize=15, color=MIA_WARM, y=0.99, fontweight='bold')
plt.tight_layout(rect=[0, 0.01, 1, 0.93])
out_path = os.path.join(os.path.dirname(__file__), 'Vol1_07_Binary_Tree_BST.png')
plt.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
plt.close()
print(f"已儲存：{out_path}")
