# 引入RPi.GPIO库函数命名为GPIO
import RPi.GPIO as GPIO


# 21号脚
pinIndex = 21

# 读取当前温度
def read_cpu_temperature():
    # 打开文件
    file = open("/sys/class/thermal/thermal_zone0/temp")
    # 读取结果，并转换为浮点数
    temp = float(file.read()) / 1000
    # 关闭文件
    file.close()
    return temp

def init_gpio():
    # 电路板编号系统模式
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinIndex, GPIO.OUT)
    GPIO.setwarnings(False)


# 写入风扇状态
def set_fan(status):
    GPIO.output(pinIndex, status)
    print('写入状态{}'.format(status))

# 关闭端口
def quit():
    # 关闭GPIO
    GPIO.cleanup()
    print("关闭GPIO")
    print("press Ctrl+C")






