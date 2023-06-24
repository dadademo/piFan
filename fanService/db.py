# 导入sqlite3模块
import time
import sqlite3

# 添加数据
# addsql = 'CREATE TABLE fan(id integer primary key autoincrement,time int NOT NULL,fanStatus int NOT NULL,temp int NOT NULL,setTemp int NOT NULL);'


def square(info):
    retObj = {}
    retObj['id'] = info[0]
    retObj['time'] = info[1]
    retObj['fanStatus'] = info[2]
    retObj['temp'] = info[3]
    retObj['setTemp'] = info[4]
    return retObj


def addInfo(fanStatus, temp, setTemp):
    # 连接到数据库
    conn = sqlite3.connect('fan.db')
    # 创建游标对象
    cursor = conn.cursor()
    # 默认当前时间戳
    currentTime = int(round(time.time() * 1000))
    cursor.execute("INSERT INTO fan(time,fanStatus,temp,setTemp) VALUES ({},{},{},{})".format(
        currentTime, fanStatus, temp, setTemp))
    conn.commit()
    conn.close()
    return True

# 获取数据


def getInfo(startTimestamp='', endTimestamp='', pageIndex=1, pageSize=10, all=False):
    # 连接到数据库
    conn = sqlite3.connect('fan.db')
    # 创建游标对象
    cursor = conn.cursor()
    # 默认查询sql
    sqlStr = 'select * from fan'
    # 时间查询
    if startTimestamp and endTimestamp:
        sqlStr = 'select * from fan where time >= {} and time <= {}'.format(
            startTimestamp, endTimestamp)
    if all == False:
        sqlStr += ' limit {},{}'.format((pageIndex - 1) * pageSize, pageSize)
    print(sqlStr)
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    # 序列化数据

    conn.close()
    # 返回新数组
    return list(map(square, result))


# 获取最后一条数据
def getLastData():
    # 连接到数据库
    conn = sqlite3.connect('fan.db')
    # 创建游标对象
    cursor = conn.cursor()
    # 默认查询sql
    sqlStr = 'select * from fan order by id desc limit 1'
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    lastData = list(map(square, result))
    conn.close()
    fanStatus = 0
    setTemp = 0
    if int(len(lastData)) == 0:
        fanStatus = 0
        setTemp = 40
    else:
        fanStatus = lastData[0].get('fanStatus')
        setTemp = lastData[0].get('setTemp')
    return {'fanStatus': fanStatus, 'setTemp': setTemp}


# # 连接到数据库
# conn = sqlite3.connect('fan.db')
# # 创建游标对象
# cursor = conn.cursor()
# # 默认当前时间戳
# currentTime = int(round(time.time() * 1000))
# cursor.execute(addsql)
# conn.commit()
# conn.close()
