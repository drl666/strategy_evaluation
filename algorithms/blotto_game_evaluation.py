"""
Use alpha-rank and SE to evaluate the blotto game.

Consider a symmetric blotto game with 3 fields and 3 coins for each player.
"""

from open_spiel.python.egt import alpharank

import numpy as np
import matplotlib.pyplot as plt
import random
import argparse
import tikzplotlib
import sys
sys.path.append("../tools")
from find_SCC2 import Graph
from metric import cycle_based_metric


if __name__ == '__main__':
    random.seed(12)

    weight = [0.5, 0.5]
    learning_step = 400  #
    episilon = 0.1  #
    n_SE = 2  #
    payoffs = np.array([[ 0, -4,  2,  1, -1,  0, -1, -1,  0],
                        [ 4,  0, -2,  1, -1,  1, -1,  1,  2],
                        [-2,  2,  0,  4, -1, -1,  2,  1,  1],
                        [-1, -1, -4,  0, -1,  1,  0, -1,  1],
                        [ 1,  1,  1,  1,  0,  1, -1,  1,  1],
                        [ 0, -1,  1, -1, -1,  0,  3, -4,  1],
                        [ 1,  1, -2,  0,  1, -3,  0,  5,  1],
                        [ 1, -1, -1,  1, -1,  4, -5,  0,  4],
                        [ 0, -2, -1, -1, -1, -1, -1, -4,  0]])

    payoff_matrix = [payoffs, payoffs.transpose()]
    SSCC_set = []
    g = []
    label = 0
    n_agent = 2

    g = Graph(np.prod(np.size(payoff_matrix[0])))
    # 根据收益矩阵生成对应的严格最优反应图
    g.generate_graph(payoff_matrix)
    # 输出所有的sink
    SSCC_set = g.SSCC()

    # 判断是否存在non-singleton的sink
    for SSCC in SSCC_set:
        if len(SSCC) >= 1 and len(SSCC_set) >= 2:
            cycle_metric = cycle_based_metric(g, payoff_matrix, weight, SSCC_set)
            metric_set = [data[1] for data in cycle_metric]
            label = 0
            break
    # 计算每个sink的cycle-based metric
    cycle_metric = cycle_based_metric(g, payoff_matrix, weight, SSCC_set)
    metric_set = [data[1] for data in cycle_metric]
    maximum_cycle_metric = max(metric_set)

    print('SSCC_set', SSCC_set)
    print('cycle_metric', cycle_metric)
    payoff_table = [payoff_matrix[0]]
    num_strategy = payoff_matrix[0].shape[0]
    print(payoff_matrix[0])

    alphas = np.arange(1e-1, 10.0, 1e-1)
    alphas = np.exp(np.arange(-4, 1.1, 0.1) * np.log(10))
    pi_s = [[] for _ in range(num_strategy)]

    for alpha in alphas:
        rhos, _, pi, _, _ = alpharank.compute(payoff_table, alpha=alpha)
        for s in range(num_strategy):
            pi_s[s].append(pi[s])

    # _, _, pi, _, _ = alpharank.compute(payoff_table)
    np.savetxt('../figs/pi_s.txt', np.array(pi))
    print('alpha_rank pi', np.array(pi))

    fig, ax = plt.subplots()

    ax.set_xscale('log')
    ax.set_xlim([1e-4, 10.0])
    # # ax.set_ylim([0, 1])

    for s in range(num_strategy):
        ax.plot(alphas, pi_s[s], label=str(s))

    ax.set(xlabel=r'Ranking-intensity $\alpha$',
           ylabel=r'Strategy mass in stationary distribution $\pi$')
    ax.legend()
    plt.tight_layout()

    plt.style.use('seaborn')
    plt.rcParams.update({
        "font.family": "serif",  # use serif/main font for text elements
        "text.usetex": True,  # use inline math for ticks
        "pgf.rcfonts": False,  # don't setup fonts from rc parameters
        # "savefig.dpi": 300
    })


    plt.grid(linestyle='--')
    # tikzplotlib.save('../figs/blotto_alpha_rank.tex', dpi=300, encoding='utf-8')
    plt.savefig('../figs/blotto_alpha_rank.png')
    # plt.savefig('../figs/blotto_alpha_rank.eps', format='eps')
    # plt.show()
