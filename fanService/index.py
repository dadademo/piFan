
# 使用内建的signal库捕获Ctrl+C
import signal
# 风扇模块
import controlFan
# 退出程序
import sys
# 引用db模块
import db
import time


# 开始时间
beginTimeHour = 7
# 结束时间
endTimeHour = 20

# 每隔5分钟判断一次温度
timeOut = 60*5



# 程序停止
def stop():
    # 停止gpio操作
    controlFan.quit()
    # 退出程序
    sys.exit()

controlFan.init_gpio()

# 监听Ctr+C
signal.signal(signal.SIGINT, stop)
while True:
    # 0/1 当前风扇状态
    fanStatus = 0
    # 设定状态，默认40度
    setTemp = 0
    # 获取状态
    lastData = db.getLastData()
    fanStatus =  lastData.get('fanStatus')
    setTemp = lastData.get('setTemp')

    # 获取当前温度
    currentTemp = controlFan.read_cpu_temperature()
    # 时间
    currentTime = time.localtime()
    dt = time.strftime('%Y:%m:%d %H:%M:%S', currentTime)
    print(dt)
    # 当前温度大于设定温度
    ctrlVal = currentTemp > setTemp
    # 判断逻辑
    if ctrlVal:
        fanStatus = 1
    else:
        fanStatus = 0
    # 初始化后追加状态
    db.addInfo(fanStatus, currentTemp, setTemp)
    if ctrlVal:
        # 夜间模式
        if currentTime.tm_hour < beginTimeHour and currentTime.tm_hour > endTimeHour:
            controlFan.set_fan(False)
        else:
            controlFan.set_fan(True)
    else:
        controlFan.set_fan(False)
    time.sleep(timeOut)


