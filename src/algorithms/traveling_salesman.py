import numpy as np

def dist(vector1, vector2, cosine):
    if cosine == 0:
        return np.linalg.norm(vector1 - vector2)
    else:
        return sum(vector1 * vector2) / (np.sqrt(sum(vector1*vector1)) * np.sqrt(sum(vector2 * vector2)))

def cost(vector_list):
    cost = 0
    for i in range(1, len(vector_list)):
        cost += dist(vector_list[i-1], vector_list[i], 1)
    return cost

def permutations(my_list):
    if len(my_list) <= 1:
        return [my_list]
    else:
        new_list = []
        for i in range(len(my_list)):
            sub_list = my_list[:i]+my_list[i+1:]
            for p in permutations(sub_list):
                new_list.append([my_list[i]] + p)
        return new_list

def order(sentence_tuples):
    #use brute force search
    best_cost = 1.0
    best_order = sentence_tuples.copy()
    for p in permutations(sentence_tuples):
        c = cost(np.array([i[0] for i in p]))
        if c < best_cost:
            best_cost = c
            best_order = p.copy()
    return best_order
