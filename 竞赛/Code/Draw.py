import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys

def loadData(road_path, cross_path, car_path):
    roadList = []  # 保存道路信息：道路id，道路长度，最高限速，车道数目，起始点id，终点id，是否双向（1：双向；0：单向）
    # 路口信息数据向量中的道路id，以路口为中心，其所连接的道路id按顺时针方向编排
    crossList = []  # 保存路口信息：路口id,道路id,道路id,道路id,道路id
    carList = []  # 保存车辆信息：车辆id，始发地、目的地、最高速度、出发时间

    # 读取数据
    with open(road_path, "r") as f1:
        lines1 = f1.readlines()
        for line in lines1:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                row = [int(str) for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(",")]
                roadList.append(row)

    with open(cross_path, "r") as f2:
        lines2 = f2.readlines()
        for line in lines2:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                row = [int(str) for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(",")]
                crossList.append(row)

    with open(car_path, "r") as f3:
        lines3 = f3.readlines()
        for line in lines3:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                row = [int(str) for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(",")]
                carList.append(row)
    return roadList, crossList, carList


#画道路图
def draw(roadList, crossList, save=False):
    g = nx.DiGraph()
    g.clear()  # 将图上元素清空
    #1.添加路口节点
    g.add_nodes_from(range(1, len(crossList)+1))
    #2.添加边
    for road in roadList:
        g.add_edge(road[4], road[5], attr_dict={'road_id':road[0], 'road_length':road[1], 'max_speed':road[2], 'lanes_number':road[3]})
        if(road[6]==1):
            g.add_edge(road[5], road[4], attr_dict={'road_id':road[0], 'road_length':road[1], 'max_speed':road[2], 'lanes_number':road[3]})

    pos = nx.spring_layout(g)
    #print(g[1][2]['attr_dict']['road_id'])
    nx.draw(g, pos = pos, with_labels = True, font_size =18, nodecolor='r', edge_color='b')
    # specifiy edge labels explicitly
    edge_labels = dict([((u, v,), d['attr_dict']['road_id']) for u, v, d in g.edges(data=True)])
    nx.draw_networkx_edge_labels(g, pos = pos, edge_labels=edge_labels, font_size=5)
    if(save==True):
        plt.savefig("map.png")
    plt.show()
    return

roadList, crossList, carList = loadData("./Data/road.txt", "./Data/cross.txt", "./Data/car.txt")
draw(roadList, crossList, save=True)



