# 给定任意的sink集合以及严格最优反应图，计算对应的cycle-based metric

import numpy as np
from collections import defaultdict


def cycle_based_metric(g, payoff_matrix, weight, SSCC_set):
    index_set = list(np.ndindex(payoff_matrix[0].shape))
    cycle_metric = []
    for SSCC in SSCC_set:
        if len(SSCC) == 1:
            # 如果为PNE
            index = index_set[SSCC[0]]
            payoff_vector = [data[index] for data in payoff_matrix]
            cycle_metric_SSCC = np.dot(payoff_vector, weight)
            cycle_metric.append((SSCC, cycle_metric_SSCC))
        else:
            # 对于非singleton的sink
            # 首先只保留该sink相关的节点和边
            subg = subgraph(g.graph, SSCC)
            # 计算所有的cycle
            cycles = [[node] + path for node in subg for path in dfs(subg, node, node)]
            # 剔除重复的cycle(计算cycle-based metric时，只要节点集相同，则metric是相同的)
            cycles_simplified = []
            temp = []
            for cycle in cycles:
                if set(cycle) not in temp:
                    temp.append(set(cycle))
                    cycles_simplified.append(cycle)
            for cycle in cycles_simplified:
                cycle.pop()
            # 计算所有cycle中拥有最小metric的cycle
            cycle_metric_SSCC= 1000000
            for cycle in cycles_simplified:
                cycle_performance = path_performance(payoff_matrix, cycle, weight)
                if cycle_performance < cycle_metric_SSCC:
                    cycle_metric_SSCC = cycle_performance
            cycle_metric.append((SSCC, cycle_metric_SSCC))
    return cycle_metric



# 输入图和一个节点集，输出为一个子图，其中只包含该节点集和相关的边
def subgraph(graph, node_set):
    subg = defaultdict(list)
    for node in node_set:
        for next_node in graph[node]:
            if next_node in node_set:
                subg[node].append(next_node)
    return subg

def dfs(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))


# 输入一条严格最优反应路径，输出对应的performance
def path_performance(payoff_matrix, path, weight):
    index_set = list(np.ndindex(payoff_matrix[0].shape))
    performance = 0
    for node in path:
        index = index_set[node]
        payoff_vector = [data[index] for data in payoff_matrix]
        performance += np.dot(payoff_vector, weight)
    return performance / len(path)