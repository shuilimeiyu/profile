import pymysql
from random import randint
def input(age,sex,autograph,city,iocn,phone):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "tuiwenbang")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句 bt,ctid,image_path,bt,'三亚市','100','三亚市'
    sql = f" INSERT INTO user_information(age,sex,autograph,city,iocn,phone) VALUES ('{age}','{sex}','{autograph}','{city}','{iocn}','{phone}')"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print("出错")

for x in range(60):
    input(age=randint(18,60),sex='男',autograph="我看到了挖矿的健康是",city="三亚",iocn='dwajdhwjhjdwhda',phone='18689681779')
for x in range(60):
    input(age=randint(18,60),sex='女',autograph="我看到了挖矿的健康是",city="三亚",iocn='dwajdhwjhjdwhda',phone='18689681779')