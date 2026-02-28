"""
米亞的演算法筆記 #19 — XOR / 位元運算 視覺化
《記憶駭客》第261-263章、第267章〈異或〉
「她只在你用記憶去解碼她的時候存在。」
上半部：XOR 真值表 + 核心性質  下半部：加密/解密流程圖
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

fig = plt.figure(figsize=(16, 11))
fig.suptitle('米亞的演算法筆記 #19 — XOR / 位元運算\n'
             '「她只在你用記憶去解碼她的時候存在。」— 第267章',
             fontsize=15, color=MIA_WARM, fontweight='bold', y=0.97)

# ── 上左：XOR 真值表 ──
ax_t = fig.add_axes([0.05, 0.55, 0.42, 0.35])
ax_t.set_title('XOR 真值表', fontsize=13, color=MIA_BLUE, pad=10)
ax_t.set_xlim(-0.5, 1.5); ax_t.set_ylim(-0.5, 1.5)
ax_t.set_aspect('equal'); ax_t.axis('off')
truth = {(0,0): 0, (0,1): 1, (1,0): 1, (1,1): 0}
for (a, b), r in truth.items():
    clr = MUTED if r == 0 else MIA_WARM
    rect = mpatches.FancyBboxPatch((a-0.4, b-0.4), 0.8, 0.8,
        boxstyle='round,pad=0.05', facecolor=clr+'33', edgecolor=clr, lw=2)
    ax_t.add_patch(rect)
    ax_t.text(a, b+0.1, f'{a} ⊕ {b} = {r}', ha='center', va='center',
              fontsize=13, color=TEXT, fontweight='bold')
    ax_t.text(a, b-0.18, '消失' if r == 0 else '留下', ha='center',
              va='center', fontsize=9, color=clr)
ax_t.text(0.5, -0.48, '一樣 → 消失（0）    不一樣 → 留下（1）',
          ha='center', fontsize=10, color=MIA_BLUE)

# ── 上右：XOR 核心性質 ──
ax_p = fig.add_axes([0.52, 0.55, 0.45, 0.35])
ax_p.axis('off')
ax_p.set_title('XOR 核心性質', fontsize=13, color=MIA_BLUE, pad=10)
props = [
    ('自反性', 'a ⊕ a = 0', '自己消去自己', RED),
    ('恆等性', 'a ⊕ 0 = a', '和零運算不變', GREEN),
    ('可逆性', '(a ⊕ b) ⊕ b = a', '再做一次就還原', MIA_WARM),
    ('交換律', 'a ⊕ b = b ⊕ a', '順序不影響', MIA_BLUE),
    ('結合律', '(a⊕b)⊕c = a⊕(b⊕c)', '分組不影響', TEXT),
]
for i, (name, formula, meaning, clr) in enumerate(props):
    y = 0.85 - i * 0.18
    ax_p.plot(0.02, y, 'o', color=clr, markersize=8, transform=ax_p.transAxes)
    ax_p.text(0.07, y, name, transform=ax_p.transAxes, fontsize=11,
              color=clr, fontweight='bold', va='center')
    ax_p.text(0.28, y, formula, transform=ax_p.transAxes, fontsize=12,
              color=TEXT, fontfamily='monospace', va='center')
    ax_p.text(0.72, y, meaning, transform=ax_p.transAxes, fontsize=9.5,
              color=MUTED, va='center')

# ── 下半部：加密/解密流程圖 ──
ax_f = fig.add_axes([0.05, 0.04, 0.9, 0.44])
ax_f.axis('off'); ax_f.set_xlim(0, 10); ax_f.set_ylim(0, 5)
M, K, C = '10110011', '11001010', '01111001'

def draw_bits(ax, x, y, bits, label, lc, bc):
    ax.text(x, y+0.55, label, ha='center', fontsize=10, color=lc, fontweight='bold')
    w = len(bits) * 0.38
    sx = x - w / 2
    for i, b in enumerate(bits):
        bx = sx + i * 0.38
        fc = bc+'44' if b == '1' else GRID
        ec = bc if b == '1' else MUTED
        rect = mpatches.FancyBboxPatch((bx, y-0.2), 0.32, 0.45,
            boxstyle='round,pad=0.03', facecolor=fc, edgecolor=ec, lw=1.3)
        ax.add_patch(rect)
        ax.text(bx+0.16, y+0.02, b, ha='center', va='center',
                fontsize=11, color=TEXT, fontweight='bold')

# 加密（左側）
ax_f.text(2.5, 4.7, '【加 密】', fontsize=13, color=RED, fontweight='bold', ha='center')
draw_bits(ax_f, 2.5, 3.8, M, '語青的記憶（明文 M）', MIA_BLUE, MIA_BLUE)
draw_bits(ax_f, 2.5, 2.5, K, '維倫的記憶（密鑰 K）', MIA_WARM, MIA_WARM)
ax_f.text(2.5, 3.25, '⊕', fontsize=22, color=RED, ha='center', va='center', fontweight='bold')
ax_f.annotate('', xy=(2.5, 1.8), xytext=(2.5, 2.3),
              arrowprops=dict(arrowstyle='->', color=RED, lw=2.5))
draw_bits(ax_f, 2.5, 1.0, C, '密文 C（不可讀）', RED, RED)
ax_f.text(2.5, 0.35, '任何人拿到都讀不出來', ha='center', fontsize=8.5,
          color=MUTED, style='italic')

# 解密（右側）
ax_f.text(7.5, 4.7, '【解 密】', fontsize=13, color=GREEN, fontweight='bold', ha='center')
draw_bits(ax_f, 7.5, 3.8, C, '密文 C', RED, RED)
draw_bits(ax_f, 7.5, 2.5, K, '維倫的記憶（密鑰 K）', MIA_WARM, MIA_WARM)
ax_f.text(7.5, 3.25, '⊕', fontsize=22, color=GREEN, ha='center', va='center', fontweight='bold')
ax_f.annotate('', xy=(7.5, 1.8), xytext=(7.5, 2.3),
              arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.5))
draw_bits(ax_f, 7.5, 1.0, M, '語青的記憶回來了', GREEN, GREEN)
ax_f.text(7.5, 0.35, '只有記得她的人能解開', ha='center', fontsize=8.5,
          color=MIA_WARM, style='italic')

# 中間傳輸箭頭
ax_f.annotate('', xy=(5.8, 2.0), xytext=(4.2, 2.0),
              arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5,
                              connectionstyle='arc3,rad=0.3'))
ax_f.text(5.0, 1.6, '傳輸', ha='center', fontsize=9, color=MUTED)

fig.text(0.5, 0.005,
    '「兩段記憶疊在一起。隱藏彼此。只有持有密鑰的人——能把原始記憶解開。」',
    ha='center', fontsize=10, color=MIA_WARM, style='italic')

out_path = os.path.join(os.path.dirname(__file__), 'Vol4_19_XOR_位元運算.png')
plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=DARK_BG, edgecolor='none')
plt.close()
print(f'已儲存：{out_path}')
