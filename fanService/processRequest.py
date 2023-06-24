# 导入http.server模块
import http.server
import socketserver

# json对象
import json

# 参数解析
from urllib.parse import urlparse, parse_qs, parse_qsl

import db
import controlFan

# 定义端口号
HTTP_PORT = 3001

# 获取query信息并转为obj


def getQureyData(url):
    retObj = {}
    currentQuery = parse_qs(urlparse(url).query)
    for key in currentQuery:
        if len(currentQuery[key]) == 1:
            retObj[key] = currentQuery[key][0]
        else:
            retObj[key] = currentQuery[key]
    return retObj


# 处理相应
class httpResponse(http.server.SimpleHTTPRequestHandler):
    # 处理get请求
    def do_GET(self):
        # 当前访问的链接决定
        currentUrl = urlparse(self.path).path
        print(currentUrl)
        if currentUrl == '/getFan':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 读取信息
            query = getQureyData(self.path)
            jsonInfo = db.getInfo(
                query.get('startTimestamp'), query.get('endTimestamp'), query.get('pageIndex'), query.get('pageSize'), query.get('all'))

            retStr = json.dumps(jsonInfo)
            self.wfile.write(bytes(retStr, "utf8"))

        if currentUrl == '/getLast':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            jsonInfo = db.getLastData()
            retStr = json.dumps(jsonInfo)
            self.wfile.write(bytes(retStr, "utf8"))
        return

    # 处理post请求
    def do_POST(self):
        # 获取POST请求的数据
        currentUrl = urlparse(self.path).path
        if currentUrl == '/setFan':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 当前信息
            query = getQureyData(self.path)
            # 获取最后的信息
            lastData = db.getLastData()
            fanStatus = int(query.get('fanStatus')
                            or lastData.get('fanStatus'))
            setTemp = int(query.get('setTemp') or lastData.get('setTemp'))
            print(fanStatus, fanStatus == 1)
            # 写入状态
            db.addInfo(fanStatus, controlFan.read_cpu_temperature(), setTemp)

            if fanStatus == 1:
                controlFan.set_fan(True)
            else:
                controlFan.set_fan(False)

            self.wfile.write(bytes("{status:200}", "utf8"))
        return


# 启动http服务
def beginServer():
    with socketserver.TCPServer(("", HTTP_PORT), httpResponse) as httpd:
        print("serving at port", HTTP_PORT)
        httpd.serve_forever()

controlFan.init_gpio()
# 开启服务
beginServer()


