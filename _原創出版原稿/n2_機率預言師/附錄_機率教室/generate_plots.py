"""
《機率預言師》附錄圖表生成器
================================
為小說中出現的所有機率統計概念生成教學用圖表。
執行方式：python generate_plots.py
輸出位置：圖表/ 資料夾
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import gamma as gamma_func
import os

# ── 深色主題設定 ──────────────────────────────────────
plt.style.use('dark_background')
plt.rcParams.update({
    'font.size': 12,
    'figure.dpi': 150,
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#e2e2e2',
    'axes.labelcolor': '#e2e2e2',
    'axes.grid': True,
    'grid.color': '#394867',
    'grid.alpha': 0.4,
    'text.color': '#e2e2e2',
    'xtick.color': '#e2e2e2',
    'ytick.color': '#e2e2e2',
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#1a1a2e',
    'legend.facecolor': '#16213e',
    'legend.edgecolor': '#394867',
})

# 配色方案：冷灰藍底 + 暖橘色/珊瑚色重點
C_ACCENT = '#e07a5f'     # 暖橘 — 關鍵數據
C_WARM = '#f2cc8f'        # 暖黃 — 次要重點
C_COOL1 = '#81b29a'       # 灰綠 — 一般曲線
C_COOL2 = '#3d85c6'       # 藍 — 一般曲線
C_COOL3 = '#9b72cf'       # 紫 — 一般曲線
C_RED = '#e07a5f'         # 同暖橘 — 警示/拒絕
C_TEXT = '#e2e2e2'        # 文字色

OUT = os.path.join(os.path.dirname(__file__), '圖表')
os.makedirs(OUT, exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1：校準 — Beta分布、貝氏更新、似然函數、Poisson
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_beta_distribution():
    """圖1：Beta分布家族 — 不同參數的形狀變化"""
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：各種 Beta 分布
    params = [
        (1, 1, 'Beta(1,1) — Uniform'),
        (2, 5, 'Beta(2,5) — Left-skewed'),
        (5, 2, 'Beta(5,2) — Right-skewed'),
        (6.2, 3.8, r'Beta(6.2, 3.8) — Ch.1 Lens'),
        (5, 5, 'Beta(5,5) — Symmetric'),
    ]
    for a, b, label in params:
        axes[0].plot(x, stats.beta.pdf(x, a, b), lw=2, label=label)
    axes[0].set_xlabel(r'$\theta$')
    axes[0].set_ylabel(r'$f(\theta)$')
    axes[0].set_title(r'Beta Distribution Family: $f(\theta) = \frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha,\beta)}$')
    axes[0].legend(fontsize=9)

    # 右圖：Beta(72, 28) — 小說關鍵數字
    axes[1].plot(x, stats.beta.pdf(x, 72, 28), lw=2.5, color='crimson', label='Beta(72, 28)')
    axes[1].axvline(72/100, color='crimson', ls='--', alpha=0.7, label=f'E[X] = 72/100 = 0.72')
    axes[1].fill_between(x, stats.beta.pdf(x, 72, 28), alpha=0.15, color='crimson')
    axes[1].set_xlabel(r'$\theta$ (Prior modification rate)')
    axes[1].set_ylabel(r'$f(\theta)$')
    axes[1].set_title('Beta(72, 28) — The Hidden Code (Ch.20-21)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '01_beta_distribution.png'))
    plt.close()
    print('  [OK] 01_beta_distribution.png')


def plot_bayesian_update():
    """圖2：貝氏更新過程 — Prior × Likelihood ∝ Posterior"""
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 場景：硬幣是否公正？
    # Prior: Beta(2, 2)
    prior_a, prior_b = 2, 2
    # Data: 7 heads out of 10 flips
    heads, tails = 7, 3
    post_a, post_b = prior_a + heads, prior_b + tails

    prior = stats.beta.pdf(x, prior_a, prior_b)
    likelihood = x**heads * (1-x)**tails
    likelihood = likelihood / likelihood.max() * prior.max()  # scale for viz
    posterior = stats.beta.pdf(x, post_a, post_b)

    titles = ['Prior: Beta(2, 2)', 'Likelihood: 7H, 3T', 'Posterior: Beta(9, 5)']
    curves = [prior, likelihood, posterior]
    colors = ['steelblue', 'orange', 'crimson']

    for ax, y, t, c in zip(axes, curves, titles, colors):
        ax.fill_between(x, y, alpha=0.3, color=c)
        ax.plot(x, y, lw=2.5, color=c)
        ax.set_title(t, fontsize=13)
        ax.set_xlabel(r'$\theta$ (P(Heads))')
        ax.set_ylabel('Density')

    # 公式標註
    fig.suptitle(r'Bayesian Update: $P(\theta|D) \propto P(\theta) \times P(D|\theta)$',
                 fontsize=15, y=1.02, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '02_bayesian_update.png'))
    plt.close()
    print('  [OK] 02_bayesian_update.png')


def plot_sequential_bayesian():
    """圖3：逐步貝氏更新 — 從先驗到後驗的演化"""
    x = np.linspace(0, 1, 500)
    fig, ax = plt.subplots(figsize=(10, 6))

    # 從 Beta(1,1) 開始，每次觀察一個數據點
    observations = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    a, b = 1, 1
    steps = [0, 3, 7, 12, 20]
    colors = plt.cm.viridis(np.linspace(0, 1, len(steps)))

    for i, (step, color) in enumerate(zip(steps, colors)):
        a_s = 1 + sum(observations[:step])
        b_s = 1 + step - sum(observations[:step])
        label = f'n={step}: Beta({a_s}, {b_s}), E={a_s/(a_s+b_s):.2f}'
        ax.plot(x, stats.beta.pdf(x, a_s, b_s), lw=2, color=color, label=label)

    ax.axvline(0.72, color='red', ls=':', alpha=0.5, label=r'True $\theta$ = 0.72')
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$f(\theta | data)$')
    ax.set_title('Sequential Bayesian Update: Prior Converges to Truth')
    ax.legend()
    plt.savefig(os.path.join(OUT, '03_sequential_bayesian.png'))
    plt.close()
    print('  [OK] 03_sequential_bayesian.png')


def plot_likelihood_function():
    """圖4：似然函數 — MLE估計 (Ch.7)"""
    x = np.linspace(0.5, 5, 500)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Poisson likelihood for observed data (simulated)
    data = [3, 2, 4, 1, 3, 2, 3, 4, 2, 3]  # observed counts
    n = len(data)
    sum_x = sum(data)
    mle = sum_x / n  # MLE = x̄ = 2.7

    log_likelihood = np.array([sum_x * np.log(lam) - n * lam for lam in x])
    log_likelihood -= log_likelihood.max()
    likelihood = np.exp(log_likelihood)

    ax.plot(x, likelihood, lw=2.5, color='darkorange')
    ax.axvline(mle, color='red', ls='--', lw=2, label=f'MLE = {mle:.1f}')
    ax.fill_between(x, likelihood, alpha=0.15, color='darkorange')

    # 標記小說中的兩個值
    ax.axvline(2.63, color='green', ls=':', lw=1.5, alpha=0.7, label=r'MLE (Ch.7) = 2.63')
    ax.axvline(1.8, color='blue', ls=':', lw=1.5, alpha=0.7, label=r'Official $\lambda$ = 1.8')

    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$L(\lambda | data)$ (normalized)')
    ax.set_title(r'Likelihood Function for Poisson: $L(\lambda) = \prod \frac{e^{-\lambda} \lambda^{x_i}}{x_i!}$')
    ax.legend()
    plt.savefig(os.path.join(OUT, '04_likelihood_function.png'))
    plt.close()
    print('  [OK] 04_likelihood_function.png')


def plot_poisson_distribution():
    """圖5：Poisson分布 — 不同λ的形狀 (Ch.4-5, Ch.53)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左：不同λ的 Poisson
    for lam, color in [(0.58, 'green'), (1.67, 'blue'), (3.0, 'orange'), (5.0, 'red')]:
        k = np.arange(0, 15)
        pmf = stats.poisson.pmf(k, lam)
        axes[0].bar(k + lam*0.05, pmf, width=0.2, alpha=0.7, color=color,
                   label=f'Poisson({lam})')
    axes[0].set_xlabel('k (events)')
    axes[0].set_ylabel('P(X = k)')
    axes[0].set_title(r'Poisson Distribution: $P(X=k) = \frac{e^{-\lambda}\lambda^k}{k!}$')
    axes[0].legend()

    # 右：Poisson(0.58) — Ch.53 意外事件
    lam = 0.58
    k = np.arange(0, 8)
    pmf = stats.poisson.pmf(k, lam)
    bars = axes[1].bar(k, pmf, color='steelblue', alpha=0.8, edgecolor='navy')
    bars[0].set_color('crimson')
    bars[0].set_alpha(0.9)
    axes[1].set_xlabel('k (Poisson events per hour)')
    axes[1].set_ylabel('P(X = k)')
    axes[1].set_title(r'Ch.53: Poisson($\lambda$=0.58) — P(0)=56%, P($\geq$1)=44%')

    for i, p in enumerate(pmf[:5]):
        axes[1].text(i, p + 0.01, f'{p:.3f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '05_poisson_distribution.png'))
    plt.close()
    print('  [OK] 05_poisson_distribution.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2：雜訊 — 常態分布、中央極限定理、共軛先驗
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_distribution_families():
    """圖6：四大分布家族 (Ch.14)"""
    x = np.linspace(0, 10, 500)
    x_norm = np.linspace(-4, 4, 500)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Normal
    for mu, sigma in [(0, 1), (0, 2), (2, 1)]:
        axes[0, 0].plot(x_norm, stats.norm.pdf(x_norm, mu, sigma), lw=2,
                       label=f'N({mu}, {sigma}²)')
    axes[0, 0].set_title(r'Normal: $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$')
    axes[0, 0].legend()

    # Exponential
    for lam in [0.5, 1.0, 2.0]:
        axes[0, 1].plot(x, stats.expon.pdf(x, scale=1/lam), lw=2,
                       label=f'Exp({lam})')
    axes[0, 1].set_title(r'Exponential: $f(x) = \lambda e^{-\lambda x}$')
    axes[0, 1].legend()

    # Gamma
    for a, b in [(1, 1), (3.2, 1.1), (1.8, 1.4), (5, 1)]:
        axes[1, 0].plot(x, stats.gamma.pdf(x, a, scale=1/b), lw=2,
                       label=f'Gamma({a}, {b})')
    axes[1, 0].set_title(r'Gamma: $f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$')
    axes[1, 0].legend()

    # Beta (on [0,1])
    x01 = np.linspace(0.01, 0.99, 500)
    for a, b in [(2, 5), (5, 2), (5, 5), (72, 28)]:
        label = f'Beta({a},{b})'
        if a == 72:
            axes[1, 1].plot(x01, stats.beta.pdf(x01, a, b), lw=2.5,
                           label=label, color='red')
        else:
            axes[1, 1].plot(x01, stats.beta.pdf(x01, a, b), lw=2, label=label)
    axes[1, 1].set_title(r'Beta: $f(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}$')
    axes[1, 1].legend()

    for ax in axes.flat:
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')

    fig.suptitle('Four Distribution Families', fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '06_distribution_families.png'))
    plt.close()
    print('  [OK] 06_distribution_families.png')


def plot_central_limit_theorem():
    """圖7：中央極限定理視覺化 (Ch.28)"""
    np.random.seed(42)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # 原始分布：Exponential (右偏)
    original = stats.expon(scale=2)
    x = np.linspace(0, 10, 200)
    axes[0, 0].plot(x, original.pdf(x), lw=2, color='steelblue')
    axes[0, 0].fill_between(x, original.pdf(x), alpha=0.3, color='steelblue')
    axes[0, 0].set_title('Original: Exp(0.5)\n(Right-skewed)')

    # 不同 n 的樣本均值分布
    for idx, n in enumerate([2, 5, 30]):
        means = [np.mean(np.random.exponential(2, n)) for _ in range(5000)]
        axes[0, idx].hist(means, bins=50, density=True, alpha=0.7, color='steelblue',
                         edgecolor='white') if idx > 0 else None

        # 理論常態分布
        mu, sigma = 2, 2 / np.sqrt(n)
        x_n = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
        if idx > 0:
            axes[0, idx].plot(x_n, stats.norm.pdf(x_n, mu, sigma), 'r--', lw=2,
                            label=f'N({mu}, {sigma:.2f}²)')
            axes[0, idx].set_title(f'n = {n}')
            axes[0, idx].legend()

    # 下排：更多 n 值
    for idx, n in enumerate([50, 100, 500]):
        means = [np.mean(np.random.exponential(2, n)) for _ in range(5000)]
        axes[1, idx].hist(means, bins=50, density=True, alpha=0.7, color='coral',
                         edgecolor='white')
        mu, sigma = 2, 2 / np.sqrt(n)
        x_n = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
        axes[1, idx].plot(x_n, stats.norm.pdf(x_n, mu, sigma), 'r--', lw=2)
        axes[1, idx].set_title(f'n = {n}')

    fig.suptitle(r'Central Limit Theorem: $\sqrt{n}(\bar{X}_n - \mu)/\sigma \to N(0, 1)$',
                fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '07_central_limit_theorem.png'))
    plt.close()
    print('  [OK] 07_central_limit_theorem.png')


def plot_conjugate_prior():
    """圖8：共軛先驗 — Beta-Binomial (Ch.16)"""
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 三個場景：不同先驗 + 同樣數據 → 不同後驗
    data_k, data_n = 7, 10  # 10 次試驗中 7 次成功

    priors = [
        (1, 1, 'Uniform prior'),
        (5, 5, 'Symmetric prior'),
        (2, 8, 'Skeptical prior'),
    ]

    for ax, (a, b, name) in zip(axes, priors):
        prior = stats.beta.pdf(x, a, b)
        posterior = stats.beta.pdf(x, a + data_k, b + data_n - data_k)

        ax.plot(x, prior, 'b--', lw=2, label=f'Prior: Beta({a},{b})')
        ax.plot(x, posterior, 'r-', lw=2.5,
                label=f'Posterior: Beta({a+data_k},{b+data_n-data_k})')
        ax.fill_between(x, posterior, alpha=0.15, color='red')
        ax.axvline(0.7, color='gray', ls=':', alpha=0.5, label='True p = 0.7')
        ax.set_title(name)
        ax.set_xlabel(r'$\theta$')
        ax.legend(fontsize=9)

    fig.suptitle(r'Conjugate Prior: Beta($\alpha, \beta$) + Binomial(k, n) $\to$ Beta($\alpha$+k, $\beta$+n-k)',
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '08_conjugate_prior.png'))
    plt.close()
    print('  [OK] 08_conjugate_prior.png')


def plot_joint_marginal():
    """圖9：聯合分布與邊際分布 (Ch.22)"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    np.random.seed(42)
    # 生成二維數據
    n = 1000
    x = np.random.beta(5, 2, n)  # modification magnitude
    y = x * 0.6 + np.random.normal(0, 0.15, n)  # correlated timestamp

    # 聯合分布 (scatter)
    axes[0].scatter(x, y, alpha=0.3, s=10, color='steelblue')
    axes[0].set_xlabel('X: Modification Magnitude')
    axes[0].set_ylabel('Y: Timestamp Index')
    axes[0].set_title('Joint Distribution f(x, y)')

    # 邊際 f_X(x)
    axes[1].hist(x, bins=40, density=True, color='coral', alpha=0.7, edgecolor='white')
    xr = np.linspace(0, 1, 200)
    axes[1].plot(xr, stats.beta.pdf(xr, 5, 2), 'r-', lw=2)
    axes[1].set_xlabel('X')
    axes[1].set_title(r'Marginal $f_X(x) = \int f(x,y) dy$')

    # 邊際 f_Y(y)
    axes[2].hist(y, bins=40, density=True, color='lightgreen', alpha=0.7,
                edgecolor='white', orientation='horizontal')
    axes[2].set_ylabel('Y')
    axes[2].set_title(r'Marginal $f_Y(y) = \int f(x,y) dx$')

    fig.suptitle('Joint & Marginal Distributions (Ch.22)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '09_joint_marginal.png'))
    plt.close()
    print('  [OK] 09_joint_marginal.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3：信號 — 期望值、變異數、大數法則、不等式、MGF
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_expected_value():
    """圖10：期望值與 LOTUS (Ch.25-26)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左：離散期望值
    x = np.arange(1, 7)
    fair = np.ones(6) / 6
    loaded = np.array([0.05, 0.05, 0.1, 0.1, 0.2, 0.5])

    w = 0.3
    axes[0].bar(x - w/2, fair, w, color='steelblue', alpha=0.8, label=f'Fair die: E[X]={np.sum(x*fair):.1f}')
    axes[0].bar(x + w/2, loaded, w, color='coral', alpha=0.8, label=f'Loaded die: E[X]={np.sum(x*loaded):.1f}')
    axes[0].set_xlabel('Outcome')
    axes[0].set_ylabel('P(X = x)')
    axes[0].set_title(r'Discrete: $E[X] = \sum x_i \cdot P(x_i)$')
    axes[0].legend()

    # 右：連續期望值 — Beta(72, 28) 的期望值
    t = np.linspace(0, 1, 500)
    pdf = stats.beta.pdf(t, 72, 28)
    ev = 72 / 100
    axes[1].plot(t, pdf, lw=2, color='crimson')
    axes[1].fill_between(t, pdf, alpha=0.2, color='crimson')
    axes[1].axvline(ev, color='black', ls='--', lw=2, label=f'E[X] = {ev:.2f}')
    axes[1].set_xlabel(r'$\theta$')
    axes[1].set_ylabel(r'$f(\theta)$')
    axes[1].set_title(r'Continuous: $E[X] = \int x \cdot f(x) dx$' + f'\nBeta(72,28): E={ev}')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '10_expected_value.png'))
    plt.close()
    print('  [OK] 10_expected_value.png')


def plot_variance():
    """圖11：變異數與標準差 (Ch.27)"""
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(-6, 6, 500)

    for sigma, color, label in [(0.5, 'red', r'$\sigma$=0.5 (tight)'),
                                  (1.0, 'blue', r'$\sigma$=1.0'),
                                  (2.0, 'green', r'$\sigma$=2.0 (spread)')]:
        pdf = stats.norm.pdf(x, 0, sigma)
        ax.plot(x, pdf, lw=2.5, color=color, label=label)
        ax.fill_between(x, pdf, alpha=0.1, color=color)

    # 68-95-99.7 rule for sigma=1
    ax.axvspan(-1, 1, alpha=0.1, color='blue', label='68.3% within 1σ')
    ax.axvspan(-2, -1, alpha=0.05, color='blue')
    ax.axvspan(1, 2, alpha=0.05, color='blue')

    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(r'Variance: $\text{Var}(X) = E[(X-\mu)^2] = \sigma^2$')
    ax.legend()
    plt.savefig(os.path.join(OUT, '11_variance.png'))
    plt.close()
    print('  [OK] 11_variance.png')


def plot_law_of_large_numbers():
    """圖12：大數法則 (Ch.28)"""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(12, 6))

    true_mean = 0.72  # the novel's Beta(72,28) expected value
    ns = np.arange(1, 1001)

    for trial, color in enumerate(['steelblue', 'coral', 'green', 'purple', 'orange']):
        samples = np.random.beta(72, 28, 1000)
        running_mean = np.cumsum(samples) / ns
        ax.plot(ns, running_mean, lw=1, alpha=0.6, color=color,
                label=f'Trial {trial+1}' if trial < 3 else None)

    ax.axhline(true_mean, color='red', ls='--', lw=2.5,
               label=f'True mean E[X] = {true_mean}')

    ax.set_xlabel('n (sample size)')
    ax.set_ylabel(r'$\bar{X}_n$')
    ax.set_title(r'Law of Large Numbers: $\bar{X}_n \to \mu$ as $n \to \infty$')
    ax.legend()
    ax.set_ylim(0.55, 0.90)
    plt.savefig(os.path.join(OUT, '12_law_of_large_numbers.png'))
    plt.close()
    print('  [OK] 12_law_of_large_numbers.png')


def plot_chebyshev_inequality():
    """圖13：Chebyshev不等式 (Ch.29-30)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：Chebyshev bound vs. actual Normal
    ks = np.arange(1, 11)
    chebyshev = 1 / ks**2
    normal_actual = 2 * (1 - stats.norm.cdf(ks))

    axes[0].semilogy(ks, chebyshev, 'ro-', lw=2, markersize=8, label='Chebyshev: 1/k²')
    axes[0].semilogy(ks, normal_actual, 'bs-', lw=2, markersize=8, label='Normal: exact')
    axes[0].set_xlabel('k (standard deviations)')
    axes[0].set_ylabel(r'$P(|X - \mu| \geq k\sigma)$')
    axes[0].set_title(r'Chebyshev: $P(|X-\mu| \geq k\sigma) \leq \frac{1}{k^2}$')
    axes[0].legend()

    # 右圖：5σ honeypot trigger (Ch.33)
    x = np.linspace(-8, 8, 500)
    pdf = stats.norm.pdf(x, 0, 1)
    axes[1].plot(x, pdf, 'b-', lw=2)
    axes[1].fill_between(x, pdf, where=(np.abs(x) >= 5), alpha=0.5, color='red',
                        label=r'Beyond 5$\sigma$: P < 0.00006%')
    axes[1].fill_between(x, pdf, where=(np.abs(x) < 5), alpha=0.2, color='steelblue')
    axes[1].axvline(5.23, color='red', ls='--', lw=2, label='Ch.33: 5.23σ trigger')
    axes[1].set_xlabel(r'Standard deviations ($\sigma$)')
    axes[1].set_title(r'The 5$\sigma$ Honeypot Trigger (Ch.30, 33)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '13_chebyshev_inequality.png'))
    plt.close()
    print('  [OK] 13_chebyshev_inequality.png')


def plot_mgf():
    """圖14：動差生成函數 MGF (Ch.34)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    t = np.linspace(-0.5, 0.9, 200)

    # 左：不同分布的 MGF
    # Normal(0,1): M(t) = exp(t²/2)
    axes[0].plot(t, np.exp(t**2 / 2), lw=2, label=r'N(0,1): $e^{t^2/2}$')
    # Exp(1): M(t) = 1/(1-t) for t < 1
    t_exp = t[t < 0.95]
    axes[0].plot(t_exp, 1 / (1 - t_exp), lw=2, label=r'Exp(1): $\frac{1}{1-t}$')
    # Poisson(2): M(t) = exp(2(e^t - 1))
    axes[0].plot(t, np.exp(2 * (np.exp(t) - 1)), lw=2, label=r'Poisson(2): $e^{2(e^t-1)}$')

    axes[0].set_xlabel('t')
    axes[0].set_ylabel(r'$M_X(t)$')
    axes[0].set_title(r'MGF: $M_X(t) = E[e^{tX}]$')
    axes[0].legend()
    axes[0].set_ylim(0, 10)

    # 右：小說中的 Gamma MGF 對比 (Ch.34)
    t_g = np.linspace(0, 0.9, 100)
    # Gamma(3.2, 1.1): M(t) = (1.1/(1.1-t))^3.2
    M_A = (1.1 / (1.1 - t_g))**3.2
    # Gamma(1.8, 1.4): M(t) = (1.4/(1.4-t))^1.8
    M_B = (1.4 / (1.4 - t_g))**1.8

    axes[1].plot(t_g, M_A, 'b-', lw=2.5, label=r'$M_A(t)$: Gamma(3.2, 1.1) — Original')
    axes[1].plot(t_g, M_B, 'r-', lw=2.5, label=r'$M_B(t)$: Gamma(1.8, 1.4) — Modified')

    # 標記小說中的比較點
    for t_val in [0.1, 0.2, 0.5]:
        ma = (1.1 / (1.1 - t_val))**3.2
        mb = (1.4 / (1.4 - t_val))**1.8
        axes[1].plot(t_val, ma, 'bo', markersize=8)
        axes[1].plot(t_val, mb, 'ro', markersize=8)
        axes[1].annotate(f't={t_val}\n{ma:.3f} vs {mb:.3f}',
                        xy=(t_val, (ma+mb)/2), fontsize=8, ha='center')

    axes[1].set_xlabel('t')
    axes[1].set_ylabel(r'$M(t)$')
    axes[1].set_title('MGF Uniqueness: Different MGF = Different Distribution (Ch.34)')
    axes[1].legend()
    axes[1].set_ylim(0, 8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '14_mgf.png'))
    plt.close()
    print('  [OK] 14_mgf.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 4：檢定 — 假設檢定、p-value、Type I/II Error、卡方
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_hypothesis_testing():
    """圖15：假設檢定視覺化 (Ch.37-40)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    x = np.linspace(-4, 6, 500)
    null = stats.norm.pdf(x, 0, 1)
    alt = stats.norm.pdf(x, 2.5, 1)

    # 左圖：H₀ 與 H₁
    axes[0].plot(x, null, 'b-', lw=2.5, label=r'$H_0$: No modification')
    axes[0].plot(x, alt, 'r-', lw=2.5, label=r'$H_1$: Modified')
    alpha_cutoff = stats.norm.ppf(0.999)  # α = 0.001
    axes[0].axvline(alpha_cutoff, color='green', ls='--', lw=2, label=f'α=0.001 cutoff ({alpha_cutoff:.2f})')
    axes[0].fill_between(x, null, where=(x >= alpha_cutoff), alpha=0.4, color='orange',
                        label='Type I Error (α)')
    axes[0].fill_between(x, alt, where=(x < alpha_cutoff), alpha=0.3, color='purple',
                        label='Type II Error (β)')
    axes[0].set_title('Hypothesis Testing Framework')
    axes[0].legend(fontsize=9)

    # 右圖：p-value 解釋
    test_stat = 4.2
    axes[1].plot(x, null, 'b-', lw=2.5, label=r'Distribution under $H_0$')
    axes[1].fill_between(x, null, where=(x >= test_stat), alpha=0.5, color='red',
                        label=f'p-value: P(X ≥ {test_stat} | H₀)')
    axes[1].axvline(test_stat, color='red', ls='--', lw=2, label=f'Test statistic = {test_stat}')
    p_val = 1 - stats.norm.cdf(test_stat)
    axes[1].set_title(f'p-value = {p_val:.6f} (Ch.38: "10,000 trials, only 3")')
    axes[1].legend(fontsize=9)

    for ax in axes:
        ax.set_xlabel('Test statistic')
        ax.set_ylabel('Density')

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '15_hypothesis_testing.png'))
    plt.close()
    print('  [OK] 15_hypothesis_testing.png')


def plot_type_errors():
    """圖16：Type I & Type II Error 決策矩陣 (Ch.40-41)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：決策矩陣
    ax = axes[0]
    ax.axis('off')
    table_data = [
        ['', 'H₀ is True\n(Innocent)', 'H₁ is True\n(Guilty)'],
        ['Reject H₀\n(Convict)', 'Type I Error\nα = 0.001\n"False Positive"', 'Correct!\nPower = 1-β\n= 0.77'],
        ['Fail to Reject\n(Acquit)', 'Correct!\n1-α = 0.999', 'Type II Error\nβ = 0.23\n"False Negative"'],
    ]

    colors = [['lightgray', 'lightgray', 'lightgray'],
              ['lightgray', '#ffcccc', '#ccffcc'],
              ['lightgray', '#ccffcc', '#ffffcc']]

    table = ax.table(cellText=table_data, cellColours=colors,
                    cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.5)
    ax.set_title('Decision Matrix (Ch.40-41)', fontsize=14, pad=20)

    # 右圖：Power curve
    effect_sizes = np.linspace(0.1, 2.0, 100)
    n = 347  # novel's sample size
    alpha = 0.001

    powers = []
    for d in effect_sizes:
        se = 1 / np.sqrt(n)
        z_alpha = stats.norm.ppf(1 - alpha)
        z_beta = d / se - z_alpha
        power = stats.norm.cdf(z_beta)
        powers.append(power)

    axes[1].plot(effect_sizes, powers, lw=2.5, color='steelblue')
    axes[1].axhline(0.77, color='red', ls='--', alpha=0.7, label='Power = 0.77 (Ch.41)')
    axes[1].axvline(0.42, color='green', ls='--', alpha=0.7, label='d = 0.42 (Ch.41)')
    axes[1].set_xlabel('Effect Size (d)')
    axes[1].set_ylabel('Power (1 - β)')
    axes[1].set_title(f'Power Curve (n={n}, α={alpha})')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '16_type_errors.png'))
    plt.close()
    print('  [OK] 16_type_errors.png')


def plot_chi_square():
    """圖17：卡方檢定 (Ch.44)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：卡方分布，不同自由度
    x = np.linspace(0, 30, 500)
    for df, color in [(2, 'blue'), (4, 'green'), (8, 'red'), (12, 'purple')]:
        axes[0].plot(x, stats.chi2.pdf(x, df), lw=2, color=color,
                    label=f'df = {df}')
    axes[0].set_xlabel(r'$\chi^2$')
    axes[0].set_ylabel(r'$f(\chi^2)$')
    axes[0].set_title(r'$\chi^2$ Distribution Family')
    axes[0].legend()

    # 右圖：Ch.44 的卡方檢定 — χ² = 47.3, df = 8
    x = np.linspace(0, 55, 500)
    pdf = stats.chi2.pdf(x, 8)
    axes[1].plot(x, pdf, 'b-', lw=2.5, label=r'$\chi^2$(df=8)')
    axes[1].fill_between(x, pdf, where=(x >= 47.3), alpha=0.5, color='red',
                        label=r'$\chi^2$ = 47.3: p < 0.00001')

    # 臨界值標記
    for alpha_val, cv, ls in [(0.05, 15.51, ':'), (0.01, 20.09, '-.'), (0.001, 26.12, '--')]:
        axes[1].axvline(cv, color='gray', ls=ls, alpha=0.7,
                       label=f'α={alpha_val}: {cv}')

    axes[1].axvline(47.3, color='red', ls='-', lw=2.5, label=r'Observed $\chi^2$ = 47.3')
    axes[1].set_xlabel(r'$\chi^2$')
    axes[1].set_title(r'Ch.44: $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i} = 47.3$')
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '17_chi_square.png'))
    plt.close()
    print('  [OK] 17_chi_square.png')


def plot_confidence_interval():
    """圖18：信賴區間 (Ch.42-43)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：信賴區間隨 n 變化
    ns = [10, 30, 100, 347, 1000, 6083]
    widths = [1.96 / np.sqrt(n) for n in ns]

    axes[0].barh(range(len(ns)), widths, color='steelblue', alpha=0.8)
    axes[0].set_yticks(range(len(ns)))
    axes[0].set_yticklabels([f'n = {n}' for n in ns])
    axes[0].set_xlabel('95% CI Half-width')
    axes[0].set_title(r'CI Width $\propto \frac{1}{\sqrt{n}}$')

    # 標記小說中的關鍵值
    for i, n in enumerate(ns):
        w = 1.96 / np.sqrt(n)
        marker = ''
        if n == 347:
            marker = ' (Ch.42)'
        elif n == 6083:
            marker = ' (Ch.43)'
        axes[0].text(w + 0.005, i, f'±{w:.4f}{marker}', va='center', fontsize=9)

    # 右圖：多組信賴區間的可視化
    np.random.seed(42)
    true_mu = 0.72
    n = 30
    ax = axes[1]
    captured = 0
    for i in range(20):
        sample = np.random.beta(72, 28, n)
        xbar = np.mean(sample)
        se = np.std(sample, ddof=1) / np.sqrt(n)
        ci_low = xbar - 1.96 * se
        ci_high = xbar + 1.96 * se
        color = 'steelblue' if ci_low <= true_mu <= ci_high else 'red'
        if ci_low <= true_mu <= ci_high:
            captured += 1
        ax.plot([ci_low, ci_high], [i, i], color=color, lw=2)
        ax.plot(xbar, i, 'o', color=color, markersize=5)

    ax.axvline(true_mu, color='red', ls='--', lw=2, label=f'True μ = {true_mu}')
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel('Sample')
    ax.set_title(f'20 Confidence Intervals ({captured}/20 captured μ)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '18_confidence_interval.png'))
    plt.close()
    print('  [OK] 18_confidence_interval.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 5：隨機 — 馬可夫鏈、隨機漫步、Poisson過程
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_markov_chain():
    """圖19：馬可夫鏈與穩態分布 (Ch.49-50)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：3-state Markov chain transition diagram (simplified)
    # 簡化版轉移矩陣
    P = np.array([
        [0.7, 0.2, 0.1],
        [0.15, 0.7, 0.15],
        [0.1, 0.2, 0.7]
    ])

    # 穩態分布收斂
    n_steps = 30
    pi = np.array([1.0, 0.0, 0.0])  # start from state 0
    history = [pi.copy()]

    for _ in range(n_steps):
        pi = pi @ P
        history.append(pi.copy())

    history = np.array(history)
    for i, (label, color) in enumerate(zip(['State A', 'State B', 'State C'],
                                            ['blue', 'red', 'green'])):
        axes[0].plot(history[:, i], lw=2, color=color, label=f'{label}: π={history[-1, i]:.3f}')

    axes[0].set_xlabel('Steps')
    axes[0].set_ylabel(r'$\pi_n(i)$')
    axes[0].set_title(r'Markov Chain Convergence to $\pi = \pi P$')
    axes[0].legend()

    # 右圖：特徵值與收斂速率
    eigenvalues = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]

    # 收斂速率由 |λ₂| 決定
    lam2_values = [0.847, 0.793, 0.761]  # novel's values
    steps = np.arange(1, 50)

    for lam2, label in zip(lam2_values, ['Initial: 0.847', 'Adjusted: 0.793', 'Accelerated: 0.761']):
        convergence = lam2 ** steps
        axes[1].semilogy(steps, convergence, lw=2, label=f'|λ₂| = {label}')

    axes[1].axhline(0.01, color='orange', ls='--', lw=1.5, label='Irreversible threshold: 0.01')
    axes[1].axhline(0.001, color='red', ls='--', lw=1.5, label='Full steady-state: 0.001')
    axes[1].set_xlabel('Steps')
    axes[1].set_ylabel(r'$|\lambda_2|^n$ (convergence distance)')
    axes[1].set_title(r'Convergence Rate: $\|\pi_n - \pi\| \sim |\lambda_2|^n$')
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '19_markov_chain.png'))
    plt.close()
    print('  [OK] 19_markov_chain.png')


def plot_random_walk():
    """圖20：隨機漫步 — 公平與偏幣 (Ch.51-52)"""
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    n_steps = 200

    # 左圖：1D Random Walk
    for trial in range(5):
        steps = np.random.choice([-1, 1], n_steps)
        path = np.cumsum(steps)
        axes[0].plot(path, alpha=0.6, lw=1.5)

    axes[0].axhline(0, color='black', ls='-', lw=0.5)
    axes[0].set_xlabel('Time step')
    axes[0].set_ylabel('Position')
    axes[0].set_title('Fair Coin Random Walk: P(+1) = P(-1) = 0.5')

    # 右圖：Biased Random Walk (55/45)
    for trial in range(5):
        steps = np.random.choice([-1, 1], n_steps, p=[0.45, 0.55])
        path = np.cumsum(steps)
        axes[1].plot(path, alpha=0.6, lw=1.5)

    # 理論漂移
    t = np.arange(n_steps)
    drift = 0.1 * t  # E[step] = 0.55 - 0.45 = 0.1
    axes[1].plot(drift, 'k--', lw=2, label='Expected drift: 0.1t')
    axes[1].axhline(0, color='black', ls='-', lw=0.5)
    axes[1].set_xlabel('Time step')
    axes[1].set_ylabel('Position')
    axes[1].set_title('Biased Coin: P(+1) = 0.55, P(-1) = 0.45 (Ch.51)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '20_random_walk.png'))
    plt.close()
    print('  [OK] 20_random_walk.png')


def plot_2d_random_walk():
    """圖21：二維隨機漫步 — 小說路線 (Ch.52)"""
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    n_steps = 100

    # 左：公平二維漫步
    for _ in range(3):
        dx = np.random.choice([-1, 1], n_steps)
        dy = np.random.choice([-1, 1], n_steps)
        x = np.cumsum(dx)
        y = np.cumsum(dy)
        axes[0].plot(x, y, alpha=0.6, lw=1)
        axes[0].plot(x[0], y[0], 'go', markersize=8)
        axes[0].plot(x[-1], y[-1], 'r^', markersize=8)

    axes[0].set_title('Fair 2D Random Walk')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    axes[0].set_aspect('equal')

    # 右：偏幣二維漫步（模擬小說中的路線）
    target = np.array([50, 30])
    pos = np.array([0.0, 0.0])
    path = [pos.copy()]

    for _ in range(n_steps):
        # 55% towards target, 45% away
        direction = target - pos
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        noise = np.random.randn(2) * 0.5
        step = direction * (np.random.random() < 0.55) + noise
        pos = pos + step
        path.append(pos.copy())

    path = np.array(path)
    axes[1].plot(path[:, 0], path[:, 1], 'b-', alpha=0.7, lw=1.5, label='Biased walk')
    axes[1].plot(0, 0, 'go', markersize=12, label='Start')
    axes[1].plot(target[0], target[1], 'r*', markersize=15, label='Target (Xinyi)')
    axes[1].plot([0, target[0]], [0, target[1]], 'r--', alpha=0.3, label='Direct path')
    axes[1].set_title('Biased 2D Walk: 55/45 Coin (Ch.52)')
    axes[1].set_xlabel('x (km)')
    axes[1].set_ylabel('y (km)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '21_2d_random_walk.png'))
    plt.close()
    print('  [OK] 21_2d_random_walk.png')


def plot_poisson_process():
    """圖22：Poisson過程與指數分布 (Ch.53)"""
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左：Poisson 過程事件時間軸
    lam = 0.58  # events per hour (from novel)
    T = 20  # hours
    n_events = np.random.poisson(lam * T)
    event_times = np.sort(np.random.uniform(0, T, n_events))

    axes[0].eventplot([event_times], lineoffsets=0.5, linelengths=0.5, colors='red')

    # 累積計數
    ax2 = axes[0].twinx()
    counts = np.arange(1, len(event_times) + 1)
    ax2.step(event_times, counts, 'b-', lw=2, where='post')
    ax2.plot([0, T], [0, lam * T], 'g--', lw=1.5, label=f'Expected: λt = {lam}t')
    ax2.set_ylabel('N(t) cumulative count', color='blue')
    ax2.legend()

    axes[0].set_xlabel('Time (hours)')
    axes[0].set_title(f'Poisson Process: λ = {lam} events/hour (Ch.53)')

    # 右：等待時間 — 指數分布
    x = np.linspace(0, 8, 200)
    axes[1].plot(x, stats.expon.pdf(x, scale=1/lam), lw=2.5, color='darkorange',
                label=f'Exp(λ={lam}): E[T] = 1/λ = {1/lam:.2f} hr')

    # 無記憶性示意
    t0 = 2
    axes[1].fill_between(x, stats.expon.pdf(x, scale=1/lam), where=(x >= t0),
                        alpha=0.3, color='red')
    axes[1].axvline(t0, color='red', ls='--', alpha=0.5)
    axes[1].annotate('Memoryless property:\nP(T > t+s | T > t) = P(T > s)',
                    xy=(t0 + 1, 0.2), fontsize=10, color='red',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    axes[1].set_xlabel('Waiting time (hours)')
    axes[1].set_ylabel('f(t)')
    axes[1].set_title(r'Exponential: $f(t) = \lambda e^{-\lambda t}$, Memoryless!')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '22_poisson_process.png'))
    plt.close()
    print('  [OK] 22_poisson_process.png')


def plot_ergodic_theorem():
    """圖23：遍歷性定理 (Ch.50)"""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(12, 6))

    # 4-state Markov chain
    P = np.array([
        [0.5, 0.3, 0.1, 0.1],
        [0.2, 0.4, 0.3, 0.1],
        [0.1, 0.2, 0.5, 0.2],
        [0.15, 0.15, 0.2, 0.5]
    ])

    # Find stationary distribution
    eigenvalues, eigenvectors = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigenvalues - 1))
    pi_stat = np.real(eigenvectors[:, idx])
    pi_stat = pi_stat / pi_stat.sum()

    # Simulate: time-average frequency of visiting state 0
    n_sim = 2000
    state = 0
    visit_counts = np.zeros(4)
    time_avg = []

    for t in range(1, n_sim + 1):
        visit_counts[state] += 1
        time_avg.append(visit_counts[0] / t)
        state = np.random.choice(4, p=P[state])

    ax.plot(time_avg, lw=1.5, color='steelblue', label='Time avg (fraction in state 0)')
    ax.axhline(pi_stat[0], color='red', ls='--', lw=2.5,
               label=f'Stationary π₀ = {pi_stat[0]:.4f}')
    ax.set_xlabel('Time steps')
    ax.set_ylabel('Fraction of time in state 0')
    ax.set_title('Ergodic Theorem: Time Average → Stationary Distribution')
    ax.legend()
    ax.set_ylim(0, 0.6)

    plt.savefig(os.path.join(OUT, '23_ergodic_theorem.png'))
    plt.close()
    print('  [OK] 23_ergodic_theorem.png')


def plot_prior_choice_distribution():
    """圖24：v5.0 選擇分布 — 自由的形狀 (Ch.57)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左圖：選擇分布
    labels = ['Official\nPrior', 'Personal\nPrior', 'No Prior', 'Lens Off', 'Undecided']
    sizes = [33.1, 29.4, 16.8, 9.2, 11.5]
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#95a5a6', '#f39c12']
    explode = (0, 0.05, 0, 0, 0)

    wedges, texts, autotexts = axes[0].pie(sizes, labels=labels, colors=colors,
                                           autopct='%1.1f%%', startangle=90,
                                           explode=explode, pctdistance=0.8)
    axes[0].set_title('v5.0 Prior Choice Distribution\nn = 21,847,203 (Ch.57)')

    # 右圖：時間序列 — 回應率
    times = [0, 8, 12, 17, 20]  # hours
    rates = [12.7, 67, 89, 94.3, 94.3]

    axes[1].plot(times, rates, 'bo-', lw=2.5, markersize=10)
    axes[1].fill_between(times, rates, alpha=0.2, color='steelblue')
    axes[1].set_xlabel('Hours after v5.0 deployment')
    axes[1].set_ylabel('Response rate (%)')
    axes[1].set_title('Response Rate Over Time (Ch.57)')
    axes[1].set_ylim(0, 100)

    for t, r in zip(times, rates):
        axes[1].annotate(f'{r}%', xy=(t, r), xytext=(t + 0.5, r - 5), fontsize=11)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '24_prior_choice.png'))
    plt.close()
    print('  [OK] 24_prior_choice.png')


def plot_likelihood_ratio_test():
    """圖25：似然比檢定 (Ch.9)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 小說中的似然比數據
    districts = ['Daan', 'Xinyi', 'Zhongzheng', 'Neihu', 'Songshan', 'Zhongshan', 'Wanhua']
    lr_values = [4.72, 3.18, 5.01, 4.33, 3.77, 0.04, 0.07]
    p_values = [0.001, 0.005, 0.001, 0.001, 0.001, 0.84, 0.79]
    colors = ['red' if p < 0.05 else 'steelblue' for p in p_values]

    bars = ax.bar(districts, lr_values, color=colors, alpha=0.8, edgecolor='black')
    ax.axhline(3.84, color='orange', ls='--', lw=1.5, label='Critical value (α=0.05): 3.84')
    ax.axhline(1, color='gray', ls=':', alpha=0.5)

    for bar, p in zip(bars, p_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'p={p}', ha='center', fontsize=9)

    ax.set_ylabel('Likelihood Ratio')
    ax.set_title(r'Likelihood Ratio Test by District (Ch.9): $\Lambda = \frac{L(H_0)}{L(H_1)}$')
    ax.legend()

    plt.savefig(os.path.join(OUT, '25_likelihood_ratio.png'))
    plt.close()
    print('  [OK] 25_likelihood_ratio.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == '__main__':
    print('=== Generating plots for《機率預言師》附錄_機率教室 ===\n')

    funcs = [
        plot_beta_distribution,
        plot_bayesian_update,
        plot_sequential_bayesian,
        plot_likelihood_function,
        plot_poisson_distribution,
        plot_distribution_families,
        plot_central_limit_theorem,
        plot_conjugate_prior,
        plot_joint_marginal,
        plot_expected_value,
        plot_variance,
        plot_law_of_large_numbers,
        plot_chebyshev_inequality,
        plot_mgf,
        plot_hypothesis_testing,
        plot_type_errors,
        plot_chi_square,
        plot_confidence_interval,
        plot_markov_chain,
        plot_random_walk,
        plot_2d_random_walk,
        plot_poisson_process,
        plot_ergodic_theorem,
        plot_prior_choice_distribution,
        plot_likelihood_ratio_test,
    ]

    for f in funcs:
        try:
            f()
        except Exception as e:
            print(f'  [FAIL] {f.__name__}: {e}')

    print(f'\n=== Done! {len(funcs)} plots generated in {OUT}/ ===')
