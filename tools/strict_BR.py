# 计算严格最优反应


def strict_BR(payoff_matrix, index, agent, multiple_label, all_next):
    # 读取选定作最优反应的agent对应的收益矩阵
    payoff = payoff_matrix[agent]
    payoff_vector = []
    index_list = list(index)
    index_list.pop(agent)
    # 严格最优反应是否存在标志位
    strict_label = 0
    # 当其他agent策略固定时，找到最优反应agent对应的收益向量
    for i in range(payoff_matrix[0].shape[agent]):
        index_list.insert(agent, i)
        index_tuple = tuple(index_list)
        payoff_vector.append(payoff[index_tuple])
        index_list.pop(agent)
    if payoff[index] < max(payoff_vector):
        # 严格最优反应存在标志
        strict_label = 1
    # 基于最优反应agent的收益向量，计算最优反应
    if multiple_label == 1:
        # 返回所有的最优反应
        agent_BR = tuple(i for i, x in enumerate(payoff_vector) if x == max(payoff_vector))
        index_new = []
        for agent_BR_i in agent_BR:
            index_list = list(index)
            index_list.pop(agent)
            index_list.insert(agent, agent_BR_i)
            index_new.append(tuple(index_list))
        index_new = tuple(index_new)
    else:
        agent_BR = payoff_vector.index(max(payoff_vector))
        index_list = list(index)
        index_list.pop(agent)
        index_list.insert(agent, agent_BR)
        index_new = tuple(index_list)
    if all_next == 0:
        return agent_BR, strict_label
    else:
        return index_new, strict_label
