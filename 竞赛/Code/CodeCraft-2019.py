import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

#l为距离矩阵 n为点的个数
def floyd(l, n):
    d = l[:]

    routes =  [[[] for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if d[i][j][0]<sys.maxsize:
                routes[i][j] = [i+1, j+1]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j][0] > d[i][k][0] + d[k][j][0]:
                    d[i][j][0] = d[i][k][0] + d[k][j][0]
                    routes[i][j] = routes[i][k] + routes[k][j][1:]

    return d, routes

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

def saveFile(file_path, result):
    with open(file_path, "w") as f:
        for res in result:
            f.write("("+str(res)[1:-1]+")"+"\n")




def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))


    # to read input file
    #----------------------------------------------------------------------------------------
    #对于多车道的道路，相对于行驶方向，车道编号从左至右依次增大

    road_labels = ['road_id', 'road_length', 'max_speed', 'lanes_number', 'start_id', 'end_id', 'is_two_way']#道路列名
    cross_labels = ['node_id', 'road1_id', 'road2_id', 'road3_id', 'road4_id']#路口列名
    car_labels = ['car_id','start_node_id', 'end_node_id', 'max_speed', 'departure_time']#车辆列名

    #载入数据
    roadList, crossList, carList = loadData(road_path, cross_path, car_path)
    n = len(crossList)
    #----------------------------------------------------------------------------------------
    # process
    #----------------------------------------------------------------------------------------
    #创建矩阵
    #l[][][0]:路长 l[][][1]:限速 l[][][2]:道路id
    l = [[[sys.maxsize] for i in range(n)] for j in range(n)]
    for i in range(n):
        l[i][i][0] = 0
    for road in roadList:
        l[road[4]-1][road[5]-1][0] = road[1]
        l[road[4]-1][road[5]-1].append(road[2])
        l[road[4]-1][road[5]-1].append(road[0])
        if (road[6] == 1):
            l[road[5]-1][road[4]-1][0] = road[1]
            l[road[5]-1][road[4]-1].append(road[2])
            l[road[5]-1][road[4]-1].append(road[0])

    #计算每两个点之间的最小距离
    d, routes = floyd(l, n)
    result = []
    time = 0
    for car in carList:
        route = routes[car[1]-1][car[2]-1]
        m = len(route)
        v1 = 0
        s1 = 0
        res = []
        for i in range(m-1):
            len_road = l[route[i]-1][route[i + 1]-1][0]
            v_road = l[route[i]-1][route[i + 1]-1][1]
            id_road = l[route[i]-1][route[i + 1]-1][2]
            v2 = min(car[3], v_road)
            if(s1==0):
                time += len_road//v2
                s1 = len_road%v2
                v1 = v2
            else:
                if(v2>s1):
                    s2 = v2-s1
                else:
                    s2 = 0
                len_road -= s2
                time += 1
                time += len_road // v2
                s1 = len_road % v2
                v1 = v2
            res.append(id_road)
        res.insert(0, car[0])
        res.insert(1, time)
        result.append(res)
    #----------------------------------------------------------------------------------------
    # to write output file
    #----------------------------------------------------------------------------------------
    saveFile(answer_path, result)
    #np.savetxt("result.txt", np.array(result), fmt="%d", delimiter=',')
    #----------------------------------------------------------------------------------------



if __name__ == "__main__":
    main()