## 生成数据库
在db.py文件中定义了创建数据库的脚本
``` python
# addsql = 'CREATE TABLE fan(id integer primary key autoincrement,time int NOT NULL,fanStatus int NOT NULL,temp int NOT NULL,setTemp int NOT NULL);'

# # 连接到数据库
# conn = sqlite3.connect('fan.db')
# # 创建游标对象
# cursor = conn.cursor()
# # 默认当前时间戳
# currentTime = int(round(time.time() * 1000))
# cursor.execute(addsql)
# conn.commit()
# conn.close()
```
需要先执行一下，然后就继续注释就完了
 
## 执行一下脚本确认一下缺少的依赖
``` shell
python3 index.py
python3 processRequest.py
# 确认一下库有没有缺失
pip install 缺少的依赖
# 安装对应的依赖，这个不缺的话不需要执行
```

### 配置一下systemctl 开机自启
> /etc/systemd/system 增加对应的文件   

fanServer.service
``` service
[Unit]
Description=test deamon
After=rc-local.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=文件的路径
ExecStart=nohup python3 -u processRequest.py > service.log 2>&1 &
Restart=always

[Install]
WantedBy=multi-user.target
```
fan.service 
``` service
[Unit]
Description=test deamon
After=rc-local.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=文件所在的路径
ExecStart=nohup python3 -u index.py > fan.log 2>&1 &
Restart=always

[Install]
WantedBy=multi-user.target
```
### 确认了可以正常运行，那就启动吧
启动
``` shell
sudo systemctl start  fan.service
sudo systemctl start  fanServer.service
```
添加到开机自启
``` shell
sudo systemctl enable fan.service
sudo systemctl enable fanServer.service
```

### ui发布 
> 1. 下载以后npm install 
> 2. npm run build
> 3. 将dist放到远程，配置一下nginx服务就完了

nginx配置文件
``` conf
location / {
   root /路径/dist;
   index index.html;
}
location /api/{
    proxy_pass http://127.0.0.1:3001/;
}
```

