"""
《機率預言師》附錄圖表生成器 v2 — 統一配色版
==============================================
所有圖表使用一致的配色方案：
  深藍黑底 + 暖橘重點 + 灰綠/冷藍/薰衣紫一般曲線
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import os

# ── 深色主題 + 統一色盤 ─────────────────────────────────
plt.style.use('dark_background')
plt.rcParams.update({
    'font.size': 12,
    'figure.dpi': 150,
    'figure.facecolor': '#0f0f1a',
    'axes.facecolor': '#141428',
    'axes.edgecolor': '#444466',
    'axes.labelcolor': '#ccccdd',
    'axes.grid': True,
    'axes.prop_cycle': plt.cycler('color', [
        '#e07a5f', '#81b29a', '#3d85c6', '#9b72cf', '#f2cc8f'
    ]),
    'grid.color': '#2a2a44',
    'grid.alpha': 0.5,
    'grid.linewidth': 0.5,
    'text.color': '#ccccdd',
    'xtick.color': '#999aaa',
    'ytick.color': '#999aaa',
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#0f0f1a',
    'legend.facecolor': '#1a1a30',
    'legend.edgecolor': '#333355',
    'legend.fontsize': 10,
    'lines.linewidth': 2.2,
})

# 色盤常數
A = '#e07a5f'   # 暖橘 accent — 最重要的東西
W = '#f2cc8f'   # 暖黃 warm — 次要重點 / 警告線
G = '#81b29a'   # 灰綠 — 一般曲線 A
B = '#3d85c6'   # 冷藍 — 一般曲線 B
P = '#9b72cf'   # 紫 — 一般曲線 C
R = '#e05555'   # 紅 — 拒絕/危險
DIM = '#666688' # 灰 — 輔助線
TXT = '#ccccdd'

OUT = os.path.join(os.path.dirname(__file__), '圖表_v2')
os.makedirs(OUT, exist_ok=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1：校準
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_beta_distribution():
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    params = [
        (1, 1, 'Beta(1,1) — Uniform', DIM),
        (2, 5, 'Beta(2,5) — Left-skewed', G),
        (5, 2, 'Beta(5,2) — Right-skewed', B),
        (6.2, 3.8, 'Beta(6.2, 3.8) — Ch.1 Lens', W),
        (5, 5, 'Beta(5,5) — Symmetric', P),
    ]
    for a, b, label, c in params:
        axes[0].plot(x, stats.beta.pdf(x, a, b), color=c, label=label)
    axes[0].set_xlabel(r'$\theta$')
    axes[0].set_ylabel(r'$f(\theta)$')
    axes[0].set_title(r'Beta Family: $f(\theta) = \frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha,\beta)}$')
    axes[0].legend(fontsize=9)

    axes[1].plot(x, stats.beta.pdf(x, 72, 28), lw=2.5, color=A, label='Beta(72, 28)')
    axes[1].axvline(0.72, color=W, ls='--', alpha=0.8, label='E[X] = 0.72')
    axes[1].fill_between(x, stats.beta.pdf(x, 72, 28), alpha=0.12, color=A)
    axes[1].set_xlabel(r'$\theta$')
    axes[1].set_ylabel(r'$f(\theta)$')
    axes[1].set_title('Beta(72, 28) — The Hidden Code (Ch.20-21)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '01_beta_distribution.png'))
    plt.close()
    print('  [OK] 01_beta_distribution.png')


def plot_bayesian_update():
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    prior_a, prior_b = 2, 2
    heads, tails = 7, 3
    post_a, post_b = prior_a + heads, prior_b + tails

    prior = stats.beta.pdf(x, prior_a, prior_b)
    likelihood = x**heads * (1-x)**tails
    likelihood = likelihood / likelihood.max() * prior.max()
    posterior = stats.beta.pdf(x, post_a, post_b)

    titles = ['Prior: Beta(2, 2)', 'Likelihood: 7H, 3T', 'Posterior: Beta(9, 5)']
    curves = [prior, likelihood, posterior]
    colors = [B, W, A]

    for ax, y, t, c in zip(axes, curves, titles, colors):
        ax.fill_between(x, y, alpha=0.2, color=c)
        ax.plot(x, y, lw=2.5, color=c)
        ax.set_title(t, fontsize=13)
        ax.set_xlabel(r'$\theta$')
        ax.set_ylabel('Density')

    fig.suptitle(r'Bayesian Update: $P(\theta|D) \propto P(\theta) \times P(D|\theta)$',
                 fontsize=15, y=1.02, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '02_bayesian_update.png'))
    plt.close()
    print('  [OK] 02_bayesian_update.png')


def plot_sequential_bayesian():
    x = np.linspace(0, 1, 500)
    fig, ax = plt.subplots(figsize=(10, 6))

    observations = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    steps = [0, 3, 7, 12, 20]
    palette = [DIM, P, B, G, A]

    for step, color in zip(steps, palette):
        a_s = 1 + sum(observations[:step])
        b_s = 1 + step - sum(observations[:step])
        label = f'n={step}: Beta({a_s}, {b_s}), E={a_s/(a_s+b_s):.2f}'
        ax.plot(x, stats.beta.pdf(x, a_s, b_s), color=color, label=label)

    ax.axvline(0.72, color=R, ls=':', alpha=0.6, label=r'True $\theta$ = 0.72')
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel(r'$f(\theta | data)$')
    ax.set_title('Sequential Bayesian Update: Prior Converges to Truth')
    ax.legend()
    plt.savefig(os.path.join(OUT, '03_sequential_bayesian.png'))
    plt.close()
    print('  [OK] 03_sequential_bayesian.png')


def plot_likelihood_function():
    x = np.linspace(0.5, 5, 500)
    fig, ax = plt.subplots(figsize=(10, 6))

    data = [3, 2, 4, 1, 3, 2, 3, 4, 2, 3]
    n = len(data)
    sum_x = sum(data)
    mle = sum_x / n

    log_likelihood = np.array([sum_x * np.log(lam) - n * lam for lam in x])
    log_likelihood -= log_likelihood.max()
    likelihood = np.exp(log_likelihood)

    ax.plot(x, likelihood, color=A, lw=2.5)
    ax.fill_between(x, likelihood, alpha=0.1, color=A)
    ax.axvline(mle, color=A, ls='--', lw=2, label=f'MLE = {mle:.1f}')
    ax.axvline(2.63, color=G, ls=':', lw=2, alpha=0.8, label='MLE (Ch.7) = 2.63')
    ax.axvline(1.8, color=B, ls=':', lw=2, alpha=0.8, label=r'Official $\lambda$ = 1.8')

    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$L(\lambda | data)$')
    ax.set_title(r'Likelihood Function: $L(\lambda) = \prod \frac{e^{-\lambda} \lambda^{x_i}}{x_i!}$')
    ax.legend()
    plt.savefig(os.path.join(OUT, '04_likelihood_function.png'))
    plt.close()
    print('  [OK] 04_likelihood_function.png')


def plot_poisson_distribution():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for lam, color in [(0.58, A), (1.67, B), (3.0, G), (5.0, P)]:
        k = np.arange(0, 15)
        pmf = stats.poisson.pmf(k, lam)
        axes[0].bar(k + lam*0.05, pmf, width=0.2, alpha=0.75, color=color,
                   label=f'Poisson({lam})')
    axes[0].set_xlabel('k')
    axes[0].set_ylabel('P(X = k)')
    axes[0].set_title(r'Poisson: $P(X=k) = \frac{e^{-\lambda}\lambda^k}{k!}$')
    axes[0].legend()

    lam = 0.58
    k = np.arange(0, 8)
    pmf = stats.poisson.pmf(k, lam)
    bar_colors = [R if i == 0 else B for i in range(len(k))]
    axes[1].bar(k, pmf, color=bar_colors, alpha=0.85, edgecolor='#333355')
    axes[1].set_xlabel('k (events/hour)')
    axes[1].set_ylabel('P(X = k)')
    axes[1].set_title(r'Ch.53: Poisson($\lambda$=0.58) — P(0)=56%')
    for i, p in enumerate(pmf[:5]):
        axes[1].text(i, p + 0.01, f'{p:.3f}', ha='center', fontsize=10, color=TXT)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '05_poisson_distribution.png'))
    plt.close()
    print('  [OK] 05_poisson_distribution.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2：雜訊
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_distribution_families():
    x = np.linspace(0, 10, 500)
    x_norm = np.linspace(-4, 4, 500)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for (mu, sigma), c in zip([(0, 1), (0, 2), (2, 1)], [A, B, G]):
        axes[0, 0].plot(x_norm, stats.norm.pdf(x_norm, mu, sigma), color=c,
                       label=f'N({mu}, {sigma}²)')
    axes[0, 0].set_title(r'Normal: $\frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^2}$')
    axes[0, 0].legend()

    for lam, c in zip([0.5, 1.0, 2.0], [A, B, G]):
        axes[0, 1].plot(x, stats.expon.pdf(x, scale=1/lam), color=c, label=f'Exp({lam})')
    axes[0, 1].set_title(r'Exponential: $\lambda e^{-\lambda x}$')
    axes[0, 1].legend()

    for (a, b), c in zip([(1, 1), (3.2, 1.1), (1.8, 1.4), (5, 1)], [DIM, B, R, G]):
        axes[1, 0].plot(x, stats.gamma.pdf(x, a, scale=1/b), color=c,
                       label=f'Gamma({a}, {b})')
    axes[1, 0].set_title(r'Gamma: $\frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$')
    axes[1, 0].legend()

    x01 = np.linspace(0.01, 0.99, 500)
    for (a, b), c in zip([(2, 5), (5, 2), (5, 5), (72, 28)], [G, B, P, A]):
        axes[1, 1].plot(x01, stats.beta.pdf(x01, a, b), color=c,
                       lw=2.5 if a == 72 else 2, label=f'Beta({a},{b})')
    axes[1, 1].set_title(r'Beta: $\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}$')
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
    np.random.seed(42)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    original = stats.expon(scale=2)
    x = np.linspace(0, 10, 200)
    axes[0, 0].plot(x, original.pdf(x), color=B)
    axes[0, 0].fill_between(x, original.pdf(x), alpha=0.2, color=B)
    axes[0, 0].set_title('Original: Exp(0.5)\n(Right-skewed)')

    ns_top = [2, 5, 30]
    ns_bot = [50, 100, 500]

    for idx, n in enumerate(ns_top):
        means = [np.mean(np.random.exponential(2, n)) for _ in range(5000)]
        if idx > 0:
            axes[0, idx].hist(means, bins=50, density=True, alpha=0.6, color=B, edgecolor='#1a1a30')
            mu, sigma = 2, 2 / np.sqrt(n)
            x_n = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
            axes[0, idx].plot(x_n, stats.norm.pdf(x_n, mu, sigma), color=A, ls='--', lw=2,
                            label=f'N(2, {sigma:.2f}²)')
            axes[0, idx].set_title(f'n = {n}')
            axes[0, idx].legend()

    for idx, n in enumerate(ns_bot):
        means = [np.mean(np.random.exponential(2, n)) for _ in range(5000)]
        axes[1, idx].hist(means, bins=50, density=True, alpha=0.6, color=G, edgecolor='#1a1a30')
        mu, sigma = 2, 2 / np.sqrt(n)
        x_n = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
        axes[1, idx].plot(x_n, stats.norm.pdf(x_n, mu, sigma), color=A, ls='--', lw=2)
        axes[1, idx].set_title(f'n = {n}')

    fig.suptitle(r'Central Limit Theorem: $\sqrt{n}(\bar{X}_n - \mu)/\sigma \to N(0, 1)$',
                fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '07_central_limit_theorem.png'))
    plt.close()
    print('  [OK] 07_central_limit_theorem.png')


def plot_conjugate_prior():
    x = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    data_k, data_n = 7, 10

    priors = [(1, 1, 'Uniform prior'), (5, 5, 'Symmetric prior'), (2, 8, 'Skeptical prior')]

    for ax, (a, b, name) in zip(axes, priors):
        prior = stats.beta.pdf(x, a, b)
        posterior = stats.beta.pdf(x, a + data_k, b + data_n - data_k)
        ax.plot(x, prior, color=B, ls='--', label=f'Prior: Beta({a},{b})')
        ax.plot(x, posterior, color=A, lw=2.5, label=f'Post: Beta({a+data_k},{b+data_n-data_k})')
        ax.fill_between(x, posterior, alpha=0.12, color=A)
        ax.axvline(0.7, color=DIM, ls=':', alpha=0.6, label='True p = 0.7')
        ax.set_title(name)
        ax.set_xlabel(r'$\theta$')
        ax.legend(fontsize=9)

    fig.suptitle(r'Conjugate Prior: Beta + Binomial $\to$ Beta', fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '08_conjugate_prior.png'))
    plt.close()
    print('  [OK] 08_conjugate_prior.png')


def plot_joint_marginal():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    np.random.seed(42)
    n = 1000
    x = np.random.beta(5, 2, n)
    y = x * 0.6 + np.random.normal(0, 0.15, n)

    axes[0].scatter(x, y, alpha=0.3, s=10, color=B)
    axes[0].set_xlabel('X: Magnitude')
    axes[0].set_ylabel('Y: Timestamp')
    axes[0].set_title('Joint f(x, y)')

    axes[1].hist(x, bins=40, density=True, color=A, alpha=0.7, edgecolor='#1a1a30')
    xr = np.linspace(0, 1, 200)
    axes[1].plot(xr, stats.beta.pdf(xr, 5, 2), color=W, lw=2)
    axes[1].set_xlabel('X')
    axes[1].set_title(r'Marginal $f_X(x)$')

    axes[2].hist(y, bins=40, density=True, color=G, alpha=0.7, edgecolor='#1a1a30', orientation='horizontal')
    axes[2].set_ylabel('Y')
    axes[2].set_title(r'Marginal $f_Y(y)$')

    fig.suptitle('Joint & Marginal Distributions (Ch.22)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '09_joint_marginal.png'))
    plt.close()
    print('  [OK] 09_joint_marginal.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3：信號
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_expected_value():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x = np.arange(1, 7)
    fair = np.ones(6) / 6
    loaded = np.array([0.05, 0.05, 0.1, 0.1, 0.2, 0.5])
    w = 0.3
    axes[0].bar(x - w/2, fair, w, color=B, alpha=0.85, label=f'Fair: E={np.sum(x*fair):.1f}')
    axes[0].bar(x + w/2, loaded, w, color=A, alpha=0.85, label=f'Loaded: E={np.sum(x*loaded):.1f}')
    axes[0].set_xlabel('Outcome')
    axes[0].set_ylabel('P(X = x)')
    axes[0].set_title(r'Discrete: $E[X] = \sum x_i P(x_i)$')
    axes[0].legend()

    t = np.linspace(0, 1, 500)
    pdf = stats.beta.pdf(t, 72, 28)
    axes[1].plot(t, pdf, color=A, lw=2.5)
    axes[1].fill_between(t, pdf, alpha=0.12, color=A)
    axes[1].axvline(0.72, color=W, ls='--', lw=2, label='E[X] = 0.72')
    axes[1].set_xlabel(r'$\theta$')
    axes[1].set_ylabel(r'$f(\theta)$')
    axes[1].set_title(r'Continuous: $E[X] = \int x f(x) dx$')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '10_expected_value.png'))
    plt.close()
    print('  [OK] 10_expected_value.png')


def plot_variance():
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(-6, 6, 500)

    for sigma, color, label in [(0.5, A, r'$\sigma$=0.5 (tight)'),
                                  (1.0, B, r'$\sigma$=1.0'),
                                  (2.0, G, r'$\sigma$=2.0 (spread)')]:
        pdf = stats.norm.pdf(x, 0, sigma)
        ax.plot(x, pdf, color=color, label=label)
        ax.fill_between(x, pdf, alpha=0.08, color=color)

    ax.axvspan(-1, 1, alpha=0.08, color=B)
    ax.axvspan(-2, 2, alpha=0.04, color=B)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(r'Variance: $\text{Var}(X) = E[(X-\mu)^2] = \sigma^2$')
    ax.legend()
    plt.savefig(os.path.join(OUT, '11_variance.png'))
    plt.close()
    print('  [OK] 11_variance.png')


def plot_law_of_large_numbers():
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(12, 6))
    true_mean = 0.72
    ns = np.arange(1, 1001)
    trail_colors = [B, G, P, W, DIM]

    for trial, color in enumerate(trail_colors):
        samples = np.random.beta(72, 28, 1000)
        running_mean = np.cumsum(samples) / ns
        ax.plot(ns, running_mean, lw=1, alpha=0.6, color=color,
                label=f'Trial {trial+1}' if trial < 3 else None)

    ax.axhline(true_mean, color=A, ls='--', lw=2.5, label=f'True E[X] = {true_mean}')
    ax.set_xlabel('n')
    ax.set_ylabel(r'$\bar{X}_n$')
    ax.set_title(r'Law of Large Numbers: $\bar{X}_n \to \mu$')
    ax.legend()
    ax.set_ylim(0.55, 0.90)
    plt.savefig(os.path.join(OUT, '12_law_of_large_numbers.png'))
    plt.close()
    print('  [OK] 12_law_of_large_numbers.png')


def plot_chebyshev_inequality():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ks = np.arange(1, 11)
    chebyshev = 1 / ks**2
    normal_actual = 2 * (1 - stats.norm.cdf(ks))

    axes[0].semilogy(ks, chebyshev, 'o-', color=A, markersize=8, label='Chebyshev: 1/k²')
    axes[0].semilogy(ks, normal_actual, 's-', color=B, markersize=8, label='Normal: exact')
    axes[0].set_xlabel('k (standard deviations)')
    axes[0].set_ylabel(r'$P(|X - \mu| \geq k\sigma)$')
    axes[0].set_title(r'Chebyshev: $P(|X-\mu| \geq k\sigma) \leq 1/k^2$')
    axes[0].legend()

    x = np.linspace(-8, 8, 500)
    pdf = stats.norm.pdf(x, 0, 1)
    axes[1].plot(x, pdf, color=B, lw=2)
    axes[1].fill_between(x, pdf, where=(np.abs(x) >= 5), alpha=0.5, color=R,
                        label=r'Beyond 5$\sigma$')
    axes[1].fill_between(x, pdf, where=(np.abs(x) < 5), alpha=0.15, color=B)
    axes[1].axvline(5.23, color=A, ls='--', lw=2.5, label='5.23σ trigger (Ch.33)')
    axes[1].set_xlabel(r'$\sigma$')
    axes[1].set_title(r'The 5$\sigma$ Honeypot Trigger')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '13_chebyshev_inequality.png'))
    plt.close()
    print('  [OK] 13_chebyshev_inequality.png')


def plot_mgf():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    t = np.linspace(-0.5, 0.9, 200)

    axes[0].plot(t, np.exp(t**2 / 2), color=A, label=r'N(0,1): $e^{t^2/2}$')
    t_exp = t[t < 0.95]
    axes[0].plot(t_exp, 1 / (1 - t_exp), color=B, label=r'Exp(1): $\frac{1}{1-t}$')
    axes[0].plot(t, np.exp(2 * (np.exp(t) - 1)), color=G, label=r'Poisson(2): $e^{2(e^t-1)}$')
    axes[0].set_xlabel('t')
    axes[0].set_ylabel(r'$M_X(t)$')
    axes[0].set_title(r'MGF: $M_X(t) = E[e^{tX}]$')
    axes[0].legend()
    axes[0].set_ylim(0, 10)

    t_g = np.linspace(0, 0.9, 100)
    M_A = (1.1 / (1.1 - t_g))**3.2
    M_B = (1.4 / (1.4 - t_g))**1.8
    axes[1].plot(t_g, M_A, color=B, lw=2.5, label=r'$M_A$: Gamma(3.2, 1.1) — Original')
    axes[1].plot(t_g, M_B, color=A, lw=2.5, label=r'$M_B$: Gamma(1.8, 1.4) — Modified')

    for t_val in [0.1, 0.2, 0.5]:
        ma = (1.1 / (1.1 - t_val))**3.2
        mb = (1.4 / (1.4 - t_val))**1.8
        axes[1].plot(t_val, ma, 'o', color=B, markersize=8)
        axes[1].plot(t_val, mb, 'o', color=A, markersize=8)
        axes[1].annotate(f'{ma:.2f} vs {mb:.2f}', xy=(t_val, (ma+mb)/2),
                        fontsize=8, ha='center', color=TXT)

    axes[1].set_xlabel('t')
    axes[1].set_ylabel(r'$M(t)$')
    axes[1].set_title('MGF Uniqueness (Ch.34)')
    axes[1].legend()
    axes[1].set_ylim(0, 8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '14_mgf.png'))
    plt.close()
    print('  [OK] 14_mgf.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 4：檢定
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_hypothesis_testing():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x = np.linspace(-4, 6, 500)
    null = stats.norm.pdf(x, 0, 1)
    alt = stats.norm.pdf(x, 2.5, 1)

    axes[0].plot(x, null, color=B, lw=2.5, label=r'$H_0$: No modification')
    axes[0].plot(x, alt, color=A, lw=2.5, label=r'$H_1$: Modified')
    cutoff = stats.norm.ppf(0.999)
    axes[0].axvline(cutoff, color=W, ls='--', lw=2, label=f'α=0.001 ({cutoff:.2f})')
    axes[0].fill_between(x, null, where=(x >= cutoff), alpha=0.4, color=W, label='Type I (α)')
    axes[0].fill_between(x, alt, where=(x < cutoff), alpha=0.2, color=P, label='Type II (β)')
    axes[0].set_title('Hypothesis Testing')
    axes[0].legend(fontsize=9)

    test_stat = 4.2
    axes[1].plot(x, null, color=B, lw=2.5, label=r'Under $H_0$')
    axes[1].fill_between(x, null, where=(x >= test_stat), alpha=0.5, color=R, label=f'p-value')
    axes[1].axvline(test_stat, color=R, ls='--', lw=2, label=f'Stat = {test_stat}')
    p_val = 1 - stats.norm.cdf(test_stat)
    axes[1].set_title(f'p-value = {p_val:.6f}')
    axes[1].legend(fontsize=9)

    for ax in axes:
        ax.set_xlabel('Test statistic')
        ax.set_ylabel('Density')

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '15_hypothesis_testing.png'))
    plt.close()
    print('  [OK] 15_hypothesis_testing.png')


def plot_type_errors():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.axis('off')
    table_data = [
        ['', 'H₀ True\n(Innocent)', 'H₁ True\n(Guilty)'],
        ['Reject H₀\n(Convict)', 'Type I\nα = 0.001', 'Correct!\nPower = 0.77'],
        ['Fail to Reject\n(Acquit)', 'Correct!\n1-α = 0.999', 'Type II\nβ = 0.23'],
    ]
    cell_colors = [['#2a2a44', '#2a2a44', '#2a2a44'],
                   ['#2a2a44', '#4a2233', '#1a3a2a'],
                   ['#2a2a44', '#1a3a2a', '#3a3a1a']]
    table = ax.table(cellText=table_data, cellColours=cell_colors,
                    cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.5)
    for cell in table.get_celld().values():
        cell.set_text_props(color=TXT)
        cell.set_edgecolor('#444466')
    ax.set_title('Decision Matrix (Ch.40-41)', fontsize=14, pad=20)

    effect_sizes = np.linspace(0.1, 2.0, 100)
    n = 347
    alpha = 0.001
    powers = []
    for d in effect_sizes:
        se = 1 / np.sqrt(n)
        z_alpha = stats.norm.ppf(1 - alpha)
        z_beta = d / se - z_alpha
        powers.append(stats.norm.cdf(z_beta))

    axes[1].plot(effect_sizes, powers, color=B, lw=2.5)
    axes[1].axhline(0.77, color=A, ls='--', alpha=0.8, label='Power = 0.77')
    axes[1].axvline(0.42, color=G, ls='--', alpha=0.8, label='d = 0.42')
    axes[1].set_xlabel('Effect Size (d)')
    axes[1].set_ylabel('Power (1 - β)')
    axes[1].set_title(f'Power Curve (n={n}, α={alpha})')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '16_type_errors.png'))
    plt.close()
    print('  [OK] 16_type_errors.png')


def plot_chi_square():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    x = np.linspace(0, 30, 500)
    for df, c in zip([2, 4, 8, 12], [A, B, G, P]):
        axes[0].plot(x, stats.chi2.pdf(x, df), color=c, label=f'df = {df}')
    axes[0].set_xlabel(r'$\chi^2$')
    axes[0].set_ylabel(r'$f(\chi^2)$')
    axes[0].set_title(r'$\chi^2$ Distribution Family')
    axes[0].legend()

    x = np.linspace(0, 55, 500)
    pdf = stats.chi2.pdf(x, 8)
    axes[1].plot(x, pdf, color=B, lw=2.5, label=r'$\chi^2$(df=8)')
    axes[1].fill_between(x, pdf, where=(x >= 47.3), alpha=0.5, color=R, label='p < 0.00001')
    for cv, ls in [(15.51, ':'), (20.09, '-.'), (26.12, '--')]:
        axes[1].axvline(cv, color=DIM, ls=ls, alpha=0.7)
    axes[1].axvline(47.3, color=A, ls='-', lw=2.5, label=r'$\chi^2$ = 47.3')
    axes[1].set_xlabel(r'$\chi^2$')
    axes[1].set_title(r'Ch.44: $\chi^2 = 47.3$, df = 8')
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '17_chi_square.png'))
    plt.close()
    print('  [OK] 17_chi_square.png')


def plot_confidence_interval():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ns = [10, 30, 100, 347, 1000, 6083]
    widths = [1.96 / np.sqrt(n) for n in ns]
    bar_colors = [DIM, DIM, DIM, A, DIM, G]

    axes[0].barh(range(len(ns)), widths, color=bar_colors, alpha=0.85)
    axes[0].set_yticks(range(len(ns)))
    axes[0].set_yticklabels([f'n = {n}' for n in ns])
    axes[0].set_xlabel('95% CI Half-width')
    axes[0].set_title(r'CI Width $\propto 1/\sqrt{n}$')
    for i, n in enumerate(ns):
        w = 1.96 / np.sqrt(n)
        m = ' (Ch.42)' if n == 347 else ' (Ch.43)' if n == 6083 else ''
        axes[0].text(w + 0.003, i, f'±{w:.4f}{m}', va='center', fontsize=9, color=TXT)

    np.random.seed(42)
    true_mu = 0.72
    ax = axes[1]
    captured = 0
    for i in range(20):
        sample = np.random.beta(72, 28, 30)
        xbar = np.mean(sample)
        se = np.std(sample, ddof=1) / np.sqrt(30)
        ci_lo = xbar - 1.96 * se
        ci_hi = xbar + 1.96 * se
        hit = ci_lo <= true_mu <= ci_hi
        if hit: captured += 1
        c = B if hit else R
        ax.plot([ci_lo, ci_hi], [i, i], color=c, lw=2)
        ax.plot(xbar, i, 'o', color=c, markersize=5)

    ax.axvline(true_mu, color=A, ls='--', lw=2.5, label=f'True μ = {true_mu}')
    ax.set_xlabel(r'$\theta$')
    ax.set_ylabel('Sample')
    ax.set_title(f'20 CIs ({captured}/20 captured μ)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '18_confidence_interval.png'))
    plt.close()
    print('  [OK] 18_confidence_interval.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 5：隨機
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def plot_markov_chain():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    P_mat = np.array([[0.7, 0.2, 0.1], [0.15, 0.7, 0.15], [0.1, 0.2, 0.7]])
    n_steps = 30
    pi = np.array([1.0, 0.0, 0.0])
    history = [pi.copy()]
    for _ in range(n_steps):
        pi = pi @ P_mat
        history.append(pi.copy())
    history = np.array(history)

    for i, (label, c) in enumerate(zip(['State A', 'State B', 'State C'], [A, B, G])):
        axes[0].plot(history[:, i], color=c, label=f'{label}: π={history[-1, i]:.3f}')
    axes[0].set_xlabel('Steps')
    axes[0].set_ylabel(r'$\pi_n(i)$')
    axes[0].set_title(r'Convergence to $\pi = \pi P$')
    axes[0].legend()

    steps = np.arange(1, 50)
    for lam2, label, c in zip([0.847, 0.793, 0.761],
                               ['0.847', '0.793', '0.761'], [B, G, A]):
        axes[1].semilogy(steps, lam2**steps, color=c, label=f'|λ₂| = {label}')
    axes[1].axhline(0.01, color=W, ls='--', lw=1.5, label='Irreversible: 0.01')
    axes[1].axhline(0.001, color=R, ls='--', lw=1.5, label='Steady-state: 0.001')
    axes[1].set_xlabel('Steps')
    axes[1].set_ylabel(r'$|\lambda_2|^n$')
    axes[1].set_title(r'Convergence Rate')
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '19_markov_chain.png'))
    plt.close()
    print('  [OK] 19_markov_chain.png')


def plot_random_walk():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    n_steps = 200
    trail = [B, G, P, W, DIM]

    for trial in range(5):
        path = np.cumsum(np.random.choice([-1, 1], n_steps))
        axes[0].plot(path, alpha=0.6, lw=1.5, color=trail[trial])
    axes[0].axhline(0, color=DIM, ls='-', lw=0.5)
    axes[0].set_xlabel('Step')
    axes[0].set_ylabel('Position')
    axes[0].set_title('Fair: P(+1) = P(-1) = 0.5')

    for trial in range(5):
        path = np.cumsum(np.random.choice([-1, 1], n_steps, p=[0.45, 0.55]))
        axes[1].plot(path, alpha=0.6, lw=1.5, color=trail[trial])
    t = np.arange(n_steps)
    axes[1].plot(0.1 * t, color=A, ls='--', lw=2.5, label='Drift: 0.1t')
    axes[1].axhline(0, color=DIM, ls='-', lw=0.5)
    axes[1].set_xlabel('Step')
    axes[1].set_ylabel('Position')
    axes[1].set_title('Biased: P(+1)=0.55 (Ch.51)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '20_random_walk.png'))
    plt.close()
    print('  [OK] 20_random_walk.png')


def plot_2d_random_walk():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    n_steps = 100

    for c in [B, G, P]:
        dx = np.random.choice([-1, 1], n_steps)
        dy = np.random.choice([-1, 1], n_steps)
        x, y = np.cumsum(dx), np.cumsum(dy)
        axes[0].plot(x, y, alpha=0.5, lw=1, color=c)
        axes[0].plot(x[0], y[0], 'o', color=G, markersize=8)
        axes[0].plot(x[-1], y[-1], '^', color=A, markersize=8)
    axes[0].set_title('Fair 2D Walk')
    axes[0].set_aspect('equal')

    target = np.array([50, 30])
    pos = np.array([0.0, 0.0])
    path = [pos.copy()]
    for _ in range(n_steps):
        direction = target - pos
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        step = direction * (np.random.random() < 0.55) + np.random.randn(2) * 0.5
        pos = pos + step
        path.append(pos.copy())
    path = np.array(path)

    axes[1].plot(path[:, 0], path[:, 1], color=B, alpha=0.7, lw=1.5, label='Biased walk')
    axes[1].plot(0, 0, 'o', color=G, markersize=12, label='Start')
    axes[1].plot(target[0], target[1], '*', color=A, markersize=15, label='Target')
    axes[1].plot([0, target[0]], [0, target[1]], color=R, ls='--', alpha=0.3, label='Direct')
    axes[1].set_title('Biased 2D: 55/45 (Ch.52)')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '21_2d_random_walk.png'))
    plt.close()
    print('  [OK] 21_2d_random_walk.png')


def plot_poisson_process():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    lam = 0.58
    T = 20
    n_events = np.random.poisson(lam * T)
    event_times = np.sort(np.random.uniform(0, T, n_events))

    axes[0].eventplot([event_times], lineoffsets=0.5, linelengths=0.5, colors=A)
    ax2 = axes[0].twinx()
    ax2.step(event_times, np.arange(1, len(event_times)+1), color=B, lw=2, where='post')
    ax2.plot([0, T], [0, lam*T], color=G, ls='--', lw=1.5, label=f'E: λt={lam}t')
    ax2.set_ylabel('N(t)', color=B)
    ax2.legend()
    axes[0].set_xlabel('Time (hours)')
    axes[0].set_title(f'Poisson Process: λ = {lam} (Ch.53)')

    x = np.linspace(0, 8, 200)
    axes[1].plot(x, stats.expon.pdf(x, scale=1/lam), color=A, lw=2.5,
                label=f'Exp({lam}): E[T]={1/lam:.2f}hr')
    axes[1].fill_between(x, stats.expon.pdf(x, scale=1/lam), where=(x >= 2),
                        alpha=0.2, color=R)
    axes[1].axvline(2, color=R, ls='--', alpha=0.5)
    axes[1].annotate('Memoryless:\nP(T>t+s|T>t) = P(T>s)',
                    xy=(3, 0.18), fontsize=10, color=W,
                    bbox=dict(boxstyle='round', facecolor='#1a1a30', edgecolor=W, alpha=0.9))
    axes[1].set_xlabel('Wait time (hours)')
    axes[1].set_title(r'Exponential: $\lambda e^{-\lambda t}$')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '22_poisson_process.png'))
    plt.close()
    print('  [OK] 22_poisson_process.png')


def plot_ergodic_theorem():
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(12, 6))
    P_mat = np.array([[0.5, 0.3, 0.1, 0.1], [0.2, 0.4, 0.3, 0.1],
                       [0.1, 0.2, 0.5, 0.2], [0.15, 0.15, 0.2, 0.5]])
    evals, evecs = np.linalg.eig(P_mat.T)
    idx = np.argmin(np.abs(evals - 1))
    pi_stat = np.real(evecs[:, idx])
    pi_stat = pi_stat / pi_stat.sum()

    n_sim = 2000
    state = 0
    visit = np.zeros(4)
    time_avg = []
    for t in range(1, n_sim + 1):
        visit[state] += 1
        time_avg.append(visit[0] / t)
        state = np.random.choice(4, p=P_mat[state])

    ax.plot(time_avg, color=B, lw=1.5, label='Time average')
    ax.axhline(pi_stat[0], color=A, ls='--', lw=2.5, label=f'π₀ = {pi_stat[0]:.4f}')
    ax.set_xlabel('Steps')
    ax.set_ylabel('Fraction in state 0')
    ax.set_title('Ergodic Theorem: Time Avg → π')
    ax.legend()
    ax.set_ylim(0, 0.6)
    plt.savefig(os.path.join(OUT, '23_ergodic_theorem.png'))
    plt.close()
    print('  [OK] 23_ergodic_theorem.png')


def plot_prior_choice_distribution():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    labels = ['Official\nPrior', 'Personal\nPrior', 'No Prior', 'Lens Off', 'Undecided']
    sizes = [33.1, 29.4, 16.8, 9.2, 11.5]
    colors_pie = [B, A, G, DIM, W]

    wedges, texts, autotexts = axes[0].pie(
        sizes, labels=labels, colors=colors_pie,
        autopct='%1.1f%%', startangle=90, explode=(0, 0.05, 0, 0, 0),
        pctdistance=0.8, textprops={'color': TXT})
    for at in autotexts:
        at.set_color('#ffffff')
    axes[0].set_title('v5.0 Choice Distribution (Ch.57)')

    times = [0, 8, 12, 17, 20]
    rates = [12.7, 67, 89, 94.3, 94.3]
    axes[1].plot(times, rates, 'o-', color=A, lw=2.5, markersize=10)
    axes[1].fill_between(times, rates, alpha=0.12, color=A)
    axes[1].set_xlabel('Hours after deployment')
    axes[1].set_ylabel('Response (%)')
    axes[1].set_title('Response Rate (Ch.57)')
    axes[1].set_ylim(0, 100)
    for t, r in zip(times, rates):
        axes[1].annotate(f'{r}%', xy=(t, r), xytext=(t+0.5, r-6), fontsize=11, color=TXT)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '24_prior_choice.png'))
    plt.close()
    print('  [OK] 24_prior_choice.png')


def plot_likelihood_ratio_test():
    fig, ax = plt.subplots(figsize=(10, 6))
    districts = ['Daan', 'Xinyi', 'Zhongzheng', 'Neihu', 'Songshan', 'Zhongshan', 'Wanhua']
    lr_values = [4.72, 3.18, 5.01, 4.33, 3.77, 0.04, 0.07]
    p_values = [0.001, 0.005, 0.001, 0.001, 0.001, 0.84, 0.79]
    bar_colors = [R if p < 0.05 else B for p in p_values]

    bars = ax.bar(districts, lr_values, color=bar_colors, alpha=0.85, edgecolor='#333355')
    ax.axhline(3.84, color=W, ls='--', lw=1.5, label='α=0.05: 3.84')
    ax.axhline(1, color=DIM, ls=':', alpha=0.5)

    for bar, p in zip(bars, p_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.12,
                f'p={p}', ha='center', fontsize=9, color=TXT)

    ax.set_ylabel('Likelihood Ratio')
    ax.set_title('Likelihood Ratio by District (Ch.9)')
    ax.legend()
    plt.savefig(os.path.join(OUT, '25_likelihood_ratio.png'))
    plt.close()
    print('  [OK] 25_likelihood_ratio.png')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    print('=== Generating v2 plots (unified palette) ===\n')
    funcs = [
        plot_beta_distribution, plot_bayesian_update, plot_sequential_bayesian,
        plot_likelihood_function, plot_poisson_distribution, plot_distribution_families,
        plot_central_limit_theorem, plot_conjugate_prior, plot_joint_marginal,
        plot_expected_value, plot_variance, plot_law_of_large_numbers,
        plot_chebyshev_inequality, plot_mgf, plot_hypothesis_testing,
        plot_type_errors, plot_chi_square, plot_confidence_interval,
        plot_markov_chain, plot_random_walk, plot_2d_random_walk,
        plot_poisson_process, plot_ergodic_theorem, plot_prior_choice_distribution,
        plot_likelihood_ratio_test,
    ]
    for f in funcs:
        try:
            f()
        except Exception as e:
            print(f'  [FAIL] {f.__name__}: {e}')
    print(f'\n=== Done! {len(funcs)} plots in {OUT}/ ===')
