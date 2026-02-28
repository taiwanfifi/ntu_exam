"""
米亞的演算法筆記 #03 — HashMap 雜湊表
《記憶駭客》第14-15章：許薇陳昊的記憶指紋交叉比對

「Hash 碰撞：兩段記憶指向同一個人。」
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Color Palette ──
MIA_BLUE, MIA_WARM = '#4fc1e9', '#f5c542'
DARK_BG, TEXT, MUTED = '#0a0e14', '#d0d7de', '#6e7681'
GRID, RED, GREEN = '#1c2028', '#ff6b6b', '#7bc87b'

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

plt.rcParams.update({
    'font.family': get_chinese_font(), 'axes.facecolor': DARK_BG,
    'figure.facecolor': DARK_BG, 'text.color': TEXT,
    'axes.edgecolor': MUTED, 'xtick.color': MUTED, 'ytick.color': MUTED
})

# ── Hash table data: (name, hash_val, bucket, source P=許薇 C=陳昊) ──
n_buckets = 8
entries = [
    ('早餐＋咖啡', 0x7A3F, 7, 'P'), ('捷運偶遇', 0x1B02, 2, 'P'),
    ('淡水碼頭', 0xB2E1, 1, 'P'), ('雨天書店', 0x4C8D, 5, 'P'),
    ('深夜通話', 0xD1F6, 6, 'P'), ('公園散步', 0x38A4, 4, 'P'),
    ('早餐＋咖啡', 0x2E10, 0, 'C'), ('淡水碼頭', 0xB2E1, 1, 'C'),
    ('電影院', 0x5D73, 3, 'C'), ('雨天書店', 0x4C8D, 5, 'C'),
    ('最後訊息', 0x9AB8, 0, 'C'), ('車站道別', 0x6F21, 1, 'C'),
]

# ── Figure ──
fig = plt.figure(figsize=(14, 11))
fig.suptitle('HashMap — 許薇與陳昊的記憶指紋交叉比對',
             fontsize=16, color=MIA_BLUE, fontweight='bold', y=0.97)
fig.text(0.5, 0.935, '「Hash 碰撞：兩段記憶指向同一個人。」— 第14章',
         ha='center', fontsize=11, color=MIA_WARM, style='italic')

ax = fig.add_axes([0.05, 0.12, 0.90, 0.78])
ax.set_xlim(-1, 16)
ax.set_ylim(-1, n_buckets + 0.5)
ax.axis('off')

bucket_w, bucket_h = 2.0, 0.65
chain_start_x = bucket_w + 1.8

for b in range(n_buckets):
    y = n_buckets - 1 - b
    rect = mpatches.FancyBboxPatch(
        (0, y - bucket_h/2), bucket_w, bucket_h,
        boxstyle='round,pad=0.08', facecolor=GRID, edgecolor=MUTED, linewidth=1.2)
    ax.add_patch(rect)
    ax.text(bucket_w / 2, y, f'[{b}]', ha='center', va='center',
            fontsize=10, color=MUTED, fontweight='bold')
    bucket_entries = [(e[0], e[1], e[3]) for e in entries if e[2] == b]
    sources = set(e[2] for e in bucket_entries)
    has_collision = 'P' in sources and 'C' in sources
    for j, (name, hval, src) in enumerate(bucket_entries):
        node_x = chain_start_x + j * 3.2
        node_w, node_h = 2.6, 0.58
        nc = MIA_BLUE if src == 'P' else MIA_WARM
        lbl = '許薇' if src == 'P' else '陳昊'
        ec = RED if has_collision else nc
        lw = 2.2 if has_collision else 1.5
        node_rect = mpatches.FancyBboxPatch(
            (node_x - node_w/2, y - node_h/2), node_w, node_h,
            boxstyle='round,pad=0.08', facecolor=nc + '22', edgecolor=ec, linewidth=lw)
        ax.add_patch(node_rect)
        ax.text(node_x, y + 0.08, name, ha='center', va='center',
                fontsize=8, color=TEXT, fontweight='bold')
        ax.text(node_x, y - 0.18, f'{lbl} | 0x{hval:04X}',
                ha='center', va='center', fontsize=6.5, color=MUTED)
        asx = bucket_w + 0.1 if j == 0 else chain_start_x + (j-1)*3.2 + node_w/2 + 0.1
        ax.annotate('', xy=(node_x - node_w/2 - 0.1, y), xytext=(asx, y),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2))
        if has_collision and j == len(bucket_entries) - 1:
            ax.text(node_x + node_w/2 + 0.3, y, '碰撞!', fontsize=9,
                    color=RED, fontweight='bold', va='center',
                    bbox=dict(boxstyle='round,pad=0.15', fc=RED+'22', ec=RED, alpha=0.9))

# ── Info boxes ──
ax.text(10.5, -0.5, '碰撞統計\n─────────\n許薇：3,847 段\n陳昊：4,112 段\n'
        '碰撞：127 段（3.09%）\n─────────\n最大碰撞：淡水碼頭\n同一夕陽·同一碗魚丸湯',
        fontsize=8.5, color=TEXT, fontfamily='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc=GRID, ec=MIA_BLUE, alpha=0.9))

ax.text(0.2, -0.5, '複雜度比較\n─────────────\n暴力法：O(n×m)\n= 15,819,264 次\n\n'
        'HashMap：O(n+m)\n= 7,959 次\n\n加速：1,988×',
        fontsize=8.5, color=TEXT, fontfamily='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc=GRID, ec=GREEN, alpha=0.9))

# ── Hash function label ──
ax.text(0, n_buckets + 0.2, 'h(記憶) = fingerprint(溫度, 亮度, 音量, 氣味, 地點) mod 8',
        fontsize=9, color=MUTED, fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.3', fc=GRID, ec=MUTED, alpha=0.7))

# ── Legend ──
legend_elements = [
    mpatches.Patch(facecolor=MIA_BLUE+'44', edgecolor=MIA_BLUE, label='許薇的記憶'),
    mpatches.Patch(facecolor=MIA_WARM+'44', edgecolor=MIA_WARM, label='陳昊的記憶'),
    mpatches.Patch(facecolor=RED+'22', edgecolor=RED, label='碰撞（同一場景）'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, frameon=False, labelcolor=TEXT, bbox_to_anchor=(0.5, 0.01))

fig.text(0.95, 0.04, '「三天不夠讓人愛上。\n  但夠讓人決定相信。」',
         ha='right', va='bottom', fontsize=10, color=MIA_WARM,
         style='italic', fontweight='bold')

# ── Save ──
out_path = os.path.join(os.path.dirname(__file__), 'Vol1_03_HashMap.png')
fig.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=DARK_BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {out_path}')
