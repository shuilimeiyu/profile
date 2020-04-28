import random
# !/usr/bin/python3

import pymysql
#
# 打开数据库连接
list_ = ['A', 'B', 'C', 'D']
list_name = ['陈小狗', '张小饭', '李偶', '李贤', '张小凡']
list_color = ['红色', '橙色', '黄色', '绿色', '青色', '蓝色', '紫色', '灰色', '粉色', '黑色', '白色', '棕色']
Vehicle_type1 = ['途锐', 'T-Roc', '途观', '途观L', '途昂', 'POLO', '桑塔纳', '朗逸', '朗行', '朗境', '凌渡', '帕萨特', '辉昂']
def car(car_number, car_name, car_color, Vehicle_type,car_Price,total_views,car_Region_id,car_hide):
    db = pymysql.connect("localhost", "root", "", "tuiwenbang")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = f"INSERT INTO car(car_number, car_name, car_color, Vehicle_type,car_Price,total_views,car_Region_id,car_hide) VALUES ('{car_number}', '{car_name}', '{car_color}', '{Vehicle_type}','{car_Price}','{total_views}','{car_Region_id}','{car_hide}')"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("sor")

for x in range(40):

    car(car_number=f'琼{random.sample(list_,1)[0][0]}{random.randint(10000,99999)}',car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}', Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=1,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=3,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=6,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=7,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=10,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=11,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=13,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=14,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=15,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=16,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=17,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=18,car_hide=0)
    car(car_number=f'琼{random.sample(list_,1)[0]}{random.randint(10000, 99999)}',
        car_name=f'{random.sample(list_name,1)[0]}', car_color=f'{random.sample(list_color,1)[0]}',
        Vehicle_type=f'{random.sample(Vehicle_type1,1)[0]}', car_Price=f'{random.randint(100, 200)}', total_views=f'{random.randint(18, 999)}', car_Region_id=24,car_hide=0)

    #
