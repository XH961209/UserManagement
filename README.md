# UserManagement
## 环境
python3.8
## 怎样运行系统并通过rest api进行调用？
### 1 下载、安装、运行redis和kafka
#### redis
redis下载链接:  
https://download.redis.io/releases/redis-6.2.6.tar.gz  
下载后，运行以下命令解压:  
`tar -zxvf redis-6.2.6.tar.gz`  
解压后进入redis-6.2.6目录，执行以下命令编译:  
`make`  
编译完成后，执行以下命令验证编译是否成功:  
`make test`  
验证成功后，执行以下命令运行redis:  
`./src/redis-server ./redis.conf`  
#### kafka
kafka下载链接:  
https://www.apache.org/dyn/closer.cgi?path=/kafka/3.0.0/kafka_2.13-3.0.0.tgz  
下载后，运行以下命令解压:  
`tar -zxvf kafka_2.13-3.0.0.tgz`  
解压后进入kafka_2.13-3.0.0目录，先运行zookeeper:  
`./bin/zookeeper-server-start.sh`  
再启动kafka server:  
`./bin/kafka-server-start.sh`
### 2 运行用户管理系统
#### 创建kafka topic
用户管理系统会将注册的用户信息写入redis数据集，然后将这一事件发送到kafka，之后任务管理系统会从kafka中读取这一事件来新建任务以及修改任务状态
我们需要为用户管理系统创建一个专门的topic(user-task)用于用户管理系统和任务管理系统之间的消息传递  
进入kafka根目录，执行以下命令以创建该topic:  
`./bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic user-task --partitions 1 --replication-factor 1`  
#### 运行员工管理系统
拉下员工管理系统的代码之后，执行以下命令以运行系统:  
`python user.py`  
#### 通过rest api调用用户管理系统的登录功能
`curl -i -H "Content-Type: application/json" -X POST -d '{"name":"000000", "password":"7SFGjsn6i4"}' http://127.0.0.1:5001/user/api/login`

该api调用会在用户管理系统下登录用户ID为`000000`，密码为`7SFGjsn6i4`的用户。

若用户不存在，会提示`该用户不存在！`；若密码错误，会提示`密码错误！`；登录成功会提示`登录成功！`。
#### 通过rest api调用用户管理系统的修改密码功能
`curl -i -H "Content-Type: application/json" -X POST -d '{"name":"000000", "old_password":"7SFGjsn6i4", "new_password":"123"}' http://127.0.0.1:5001/user/api/update_password`

该api调用会在用户管理系统下将登录用户ID为`000000`的原密码为`7SFGjsn6i4`修改为`123`。

若用户不存在，会提示`该用户不存在！请检查用户名。`；若密码错误，会提示`密码错误！请输入正确密码。`；修改成功会提示`密码修改成功！`。
#### 通过rest api调用用户管理系统的修改用户部门功能
`curl -i -H "Content-Type: application/json" -X POST -d '{"name":"000000", "password": "123", "department":"Financial"}' http://127.0.0.1:5001/user/api/reset_department`

该api调用会在用户管理系统下将登录用户ID为`000000`的部门修改为`Financial`，任务管理系统下登录用户ID`000000`对应的部门同样会被修改。

若用户不存在，会提示`该用户不存在！请检查用户名。`；若密码错误，会提示`密码错误！请输入正确密码。`；修改成功会提示`用户部门修改成功！`。
