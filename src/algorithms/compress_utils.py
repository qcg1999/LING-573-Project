from nltk import tree
from nltk.corpus import stopwords
import numpy as np

DELETE = 0
KEEP = 1
PARTIAL = 1

def get_pos_tags(t):
    tags = []
    if type(t) == tree.Tree:
        tags.append(t.label())
        for child in t:
            tags += get_pos_tags(child)
    return tags

def count_nodes(t):
    if type(t) == tree.Tree:
        count = 1
        for subtree in t:
            count += count_nodes(subtree)
    else:
        count = 0
    return count

def get_features_recursive(t, tokens, parent=None, grandparent=None, depth=0):
    if not type(t) == tree.Tree:
        return []

    tag_list = ['ROOT', 'S', 'NP', 'VP', '-LRB-', '-RRB-',
            'ADJP', 'ADVP', 'CC', 'CD', 'CONJP', 'DT', 'EX', 'FW',
            'FRAG', 'IN', 'INTJ', 'JJ', 'JJR', 'JJS', 'LS', 'MD',
            'NN', 'NNS', 'NNP', 'NNPS', 'NX', 'QP', 'PP', 'PDT',
            'PRN', 'PRT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS',
            'RP', 'SBAR', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG',
            'VBN', 'VBP', 'VBZ', 'WDT', 'WHADVP', 'WHNP', 'WP', 'WP$',
            'WRB', '.', ',', ':', "''", '``', '"', '?']
    vector = np.zeros((18+len(tag_list)*5))

    #basic features (see Wang et al 2013)
    if all(x in tokens[:3] for x in t.leaves()):
        vector[0] = 1.0
    if all(x in tokens[-3:] for x in t.leaves()):
        vector[1] = 1.0
    if all(x in t.leaves() for x in tokens[:3]):
        vector[2] = 1.0
    if all(x in t.leaves() for x in tokens[-3:]):
        vector[3] = 1.0
    for leaf in t.leaves():
        if len(leaf) > 10:
            vector[4] += 1.0
    if len(t.leaves()) == 1:
        vector[5] = 1.0
    if all(x in t.leaves() for x in tokens):
        vector[6] = 1.0
    for leaf in t.leaves():
        if leaf.isupper():
            vector[8] = 1.0
        elif leaf[0].isupper():
            vector[7] = 1.0
    if "not" in t.leaves() or "n't" in t.leaves():
        vector[9] = 1.0
    if any(x in stopwords.words('english') for x in t.leaves()):
        vector[10] = 1.0

    #rule-based features

    #parenthetical
    if '(' in tokens and ')' in tokens:
        leaves = t.leaves()
        for i in range(tokens.find(')'), tokens.find('(')-len(leaves)):
            if tokens[i:i+len(leaves)] == leaves:
                vector[11] = 1.0
                break
    #lead adverbial
    if t.label() == 'ADVP' and t.leaves()[0] == tokens[0]:
        vector[12] = 1.0
    #relative clause
    t_pos_tags = get_pos_tags(t)
    if len(t_pos_tags) > 1 and t_pos_tags[1] == 'WHNP':
        vector[13] = 1.0
    #lead prepositional clause
    if t.label() == 'PP' and t.leaves()[0] == tokens[0]:
        vector[14] = 1.0

    #tree features
    vector[15] = depth
    if parent:
        index = parent.index(t)
        if index == 0:
            vector[16] = 1.0
        if index == 1:
            vector[17] = 1.0

        #sister lables
        if index > 0:
            if parent[index-1].label() in tag_list:
                vector[18+tag_list.index(parent[index-1].label())] = 1.0
        if index < len(parent)-1:
            if parent[index+1].label() in tag_list:
                vector[18+len(tag_list)+tag_list
                        .index(parent[index+1].label())] = 1.0

        if grandparent:
            #aunt labels
            index = grandparent.index(parent)
            if index > 0:
                if grandparent[index-1].label() in tag_list:
                    vector[18+len(tag_list)*2+tag_list
                            .index(grandparent[index-1].label())] = 1.0
            if index < len(grandparent)-1:
                if grandparent[index+1].label() in tag_list:
                    vector[18+len(tag_list)*3+tag_list
                            .index(grandparent[index+1].label())] = 1.0

    #semantic features
    if t.label() in tag_list:
        vector[18+len(tag_list)*4+tag_list.index(t.label())] = 1.0


    features = [vector]
    for children in t:
        features += get_features_recursive(children, tokens, t, parent, depth+1)
    return features

def get_labels_recursive(original, compressed):
    #stopping condition
    if not type(original) == tree.Tree:
        return []
    
    labels = []
    idx1 = idx2 = 0
    while idx1 < len(original):
        subtree1 = original[idx1]

        if idx2 >= len(compressed):
            labels = labels + [DELETE for node in range(count_nodes(subtree1))]
            idx1 += 1
            continue

        subtree2 = compressed[idx2]
        if subtree1 == subtree2: #keep all
            labels = labels + [KEEP for node in range(count_nodes(subtree1))]
            idx1 += 1
            idx2 += 1
        elif (subtree1.label() == subtree2.label() and 
                all((x in subtree1.leaves()) for x in subtree2.leaves())):
            labels = labels + get_labels_recursive(subtree1, subtree2)
            idx1 += 1
            idx2 += 1
        else: #delete all
            labels = labels + [DELETE for node in range(count_nodes(subtree1))]
            idx1 += 1
    if KEEP in labels:
        if DELETE in labels:
            labels = [PARTIAL] + labels
        else:
            labels = [KEEP] + labels
    else:
        labels = [DELETE] + labels

    return labels

