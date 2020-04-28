import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif']=['SimHei']
def figure(list_data,list_name,title):

    plt.figure()
    plt.bar(list_name, list_data)
    plt.title(title)
    plt.show()



# 生成数据
