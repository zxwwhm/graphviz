import sys
import os
pro_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if pro_root not in sys.path:
    sys.path.insert(0, pro_root)

import matplotlib.pyplot as plt  
import networkx as nx 
import argparse
from utils import ioutil

parser = argparse.ArgumentParser()
parser.add_argument("--template", type=str, default='./template.txt')
args = parser.parse_args()

template_file = args.template

def build_graph():
    G2 = nx.DiGraph() 
    # edge_list = [('X', 'Y'), ('X', 'M'), ('M' 'Y'), ('C', 'X'), ('C', 'M')]
    # pos = {'X':(0,0), 'Y':(2,0), 'M':(1, 1), 'C':(1,2)}  # 具体制定位置
    edge_list = ioutil.read_txt(template_file, sep=' ')  
    G2.add_edges_from(edge_list)

    pos = nx.spring_layout(G2)  # 用 FR算法排列节点
    nx.draw(G2, pos, with_labels=True, alpha=0.5)
    nx.draw_networkx(G2, pos)
    plt.savefig('./causal.jpg')
    plt.show()

build_graph()