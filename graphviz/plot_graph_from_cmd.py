import sys
import os
pro_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pro_root not in sys.path:
    sys.path.insert(0, pro_root)

import matplotlib.pyplot as plt 
# plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
# plt.rcParams["axes.unicode_minus"]=False   #该语句解决图像中的“-”负号的乱码问题 
import networkx as nx 
import argparse
from utils import ioutil

parser = argparse.ArgumentParser()
parser.add_argument("--template", type=str, default='./template.txt')
args = parser.parse_args()

template_file = args.template

def gen_pos(G, nodes, edges):

    pos = {}
    start = 'X'
    end = 'Y'
    rest_nodes = set(nodes)           # 剩余节点
    bottom_nodes = set([start, end])  # 显示在最底部的节点
    if start in nodes and end in nodes:
        rest_nodes -= bottom_nodes
    else:
        pos = nx.spring_layout(G)  # 用 FR算法排列节点
        return pos
    
    # 统计每个节点的所有出边
    stat_vertex = {}
    for e in edges:
        v1, v2 = e[:2]
        if v1 in stat_vertex:
            stat_vertex[v1].add(v2)
        else:
            stat_vertex[v1] = set([v2])
    
    second_layer = set()
    # 如果指向只有底部节点，则作为第二层节点
    for v, vers in stat_vertex.items():
        if len(vers - bottom_nodes) == 0:
            second_layer.add(v)
            if v in rest_nodes:
                rest_nodes.remove(v)
    
    # 剩余节点放在第三层
    third_layer = rest_nodes  

    max_layer_node_num = 0
    for layer in [bottom_nodes, second_layer, third_layer]:
        max_layer_node_num = max(max_layer_node_num, len(layer))

    max_layer_node_num += 1
    
    # 设置每一层的位置
    bottom_nodes
    pos[start] = (0, 0)
    pos[end] = (max_layer_node_num, 0)

    for i, node in enumerate(second_layer):  # TODO 跨层指向节点时，边应该避免经过其他节点
        pos[node] = (i+1, 1)

    for i, node in enumerate(third_layer):
        pos[node] = (i+1, 2)
    
    return pos



def build_graph(nodes_dic, edges):
    G = nx.DiGraph() 
    G.add_edges_from(edges)
    pos = gen_pos(G, nodes, edges)  # 自定义计算节点位置
    # pos=nx.spring_layout(G)       # 用FR算法排列节点
    nodes_labels = {}
    for node in G:
        nodes_labels[node] = node
        nx.draw_networkx_nodes(G, pos=pos, nodelist=[node],  node_color='white', edgecolors='black',  label="{}:{}".format(node,nodes_dic[node]))
    nx.draw_networkx_edges(G, pos=pos, edgelist=edges)
    nx.draw_networkx_labels(G, pos, labels=nodes_labels)
    plt.legend(numpoints = 1)       # 绘制图例
    plt.savefig('./causal.jpg')
    plt.show()


if __name__ == '__main__':

    # 让用户输入节点和对应的含义
    count = 1
    err_hint = False
    nodes = {}
    while(True):
        if count == 1:     # 首次执行，对命令进行提示
            x = input("Please enter variables, \nInput Format >> Variable:Meaning, \nStop command >> -1 \n")
        elif not err_hint: # 输入正确时，提示再次输入
            x = input("Please enter variables again:\n")
        else:              # 输入错误时，提示按格式输入
            x = input("Please enter the correct format:\n")
            err_hint= False
        count += 1
        if x == '-1':      # 输入 -1 exit 
            break
        vars = x.split(":")
        if len(vars) != 2:
            err_hint = True
            continue
        var, des = vars[:2]
        nodes[var] = des

    print("nodes:", nodes)

    # 让用户输入节点之间的关系
    edges = []
    err_hint = False
    count = 1
    while(True):
        if count == 1:     # 首次执行，对命令进行提示
            x = input("Please enter the relationship between variables, \nInput Format >> Variable1:Variable2, \nStop command >> -1 \n")
        elif not err_hint: # 输入正确时，提示再次输入
            x = input("Please enter Variable1:Variable2 again:\n")
        else:              # 输入错误时，提示按格式输入
            x = input("Please enter the correct format:\n")
            err_hint= False
        count += 1
        if x == '-1':      # 输入 -1 exit 
            break
        vars = x.split(":")
        if len(vars) != 2:
            err_hint = True
            continue
        var1, var2 = vars[:2]
        edges.append((var1, var2))

    # 输入边中包含无效节点，进行过滤
    valid_edges = []
    for edge in edges:
        v1, v2 = edge[:2]
        if v1 in nodes and v2 in nodes:
            valid_edges.append((v1, v2))

    print("valid edges:", valid_edges)

    # nodes = {'X': 'meaning1', 'Y': 'meaning2', 'C': 'meaning3', 'M': 'meaning4'}
    # valid_edges = [('X', 'Y'), ('X', 'M'), ('M', 'Y'),('C', 'X'), ('C', 'M')]
    build_graph(nodes, valid_edges)
