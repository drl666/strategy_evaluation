import numpy as np

from collections import defaultdict
from strict_BR import strict_BR

class Graph:

    def __init__(self, vertex):
        self.V = vertex
        self.graph = defaultdict(list)
        self.SCC = []

    # Add edge into the graph
    def add_edge(self, s, d):
        self.graph[s].append(d)

    # dfs
    def dfs(self, d, visited_vertex):
        visited_vertex[d] = True
        # print(d, end='')
        self.SCC.append(d)
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex)
            # new


    def fill_order(self, d, visited_vertex, stack):
        visited_vertex[d] = True
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)
        stack = stack.append(d)

    # transpose the matrix
    def transpose(self):
        g = Graph(self.V)

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    # Print stongly connected components
    def print_scc(self):
        stack = []
        visited_vertex = [False] * (self.V)

        for i in range(self.V):
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        gr = self.transpose()

        visited_vertex = [False] * (self.V)
        SCC_set = []
        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                gr.dfs(i, visited_vertex)
                # 记录所有的SCC
                SCC_set.append(gr.SCC)
                gr.SCC = []
                # print("")
        return SCC_set

    # 计算sink SCC
    def SSCC(self):
        SCC_set = self.print_scc()
        SSCC_set = []
        for SCC in SCC_set:
            label = 1
            for i in SCC:
                for j in self.graph[i]:
                    if j not in SCC:
                        label = 0
                        break
                if label == 0:
                    break
            if label == 1:
                SSCC_set.append(SCC)
        return SSCC_set

    # 根据收益矩阵生成对应的严格最优反应图
    def generate_graph(self, payoff_matrix):
        index_set = list(np.ndindex(payoff_matrix[0].shape))
        for num in range(self.V):
            index = index_set[num]
            # 针对每个agent，计算严格最优反应点
            multiple_label = 1
            all_next = 1
            for agent in range(len(payoff_matrix)):
                index_new, strict_label = strict_BR(payoff_matrix, index, agent, multiple_label, all_next)
                if strict_label == 1:
                    # 如果为严格最优反应，则加入此边
                    for sample in index_new:
                        next_num = index_set.index(sample)
                        self.add_edge(num, next_num)


# g = Graph(8)
# g.add_edge(0, 1)
# g.add_edge(1, 2)
# g.add_edge(2, 3)
# # g.add_edge(2, 4)
# g.add_edge(3, 0)
# g.add_edge(4, 5)
# g.add_edge(5, 6)
# g.add_edge(6, 4)
# g.add_edge(6, 7)
#
# print("Strongly Connected Components:")
# SCC_set_output = g.print_scc()
# SSCC_set_output = g.SSCC(SCC_set_output)
# tt = 1