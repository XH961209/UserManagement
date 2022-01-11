import time
import threading
from flask import Flask
from flask import request
from flask import abort
from common import MSG_NEW_USER, MSG_UPDATE_DEPARTMENT
from common import MSG_UPDATE_PASSWORD
from common import USER_TASK_TOPIC
from myredis.client import redis_client
from mykafka.consumer import kafka_consumer
from mykafka.producer import kafka_producer


app = Flask(__name__)


def on_send_success(record_metadata, result):
    result['success'] = True
    result['debug_info'] = "Successfully send message to topic {}, partition {}, offset {}".\
        format(record_metadata.topic, record_metadata.partition, record_metadata.offset)


def on_send_fail(e, result):
    result['success'] = False
    result['info'] = "Fail to send message with error {}".format(e)


def register(number, name, department, password):
    """
    注册一个新用户
    :param number: 工号
    :param name: 用户名
    :param department: 部门
    :param password: 密码
    :return: None
    """
    # 将用户信息写入redis
    key = number
    value = {
        "name": name,
        "department": department,
        "password": password
    }
    redis_client.hset(name=key, mapping=value)

    # 将注册新用户这一事件写入kafka，任务管理系统会从kafka中读取该事件
    # kafka server应当事先建立一个名为user-task并且只包含一个partition的topic，用于传递用户管理系统和任务管理系统之间的消息
    result = {
        "success": False,
        "debug_info": ""
    }
    msg_new_user = MSG_NEW_USER.format(number=number, name=name, department=department).encode()
    kafka_producer.send(USER_TASK_TOPIC, msg_new_user).\
        add_callback(on_send_success, result=result).\
        add_errback(on_send_fail, result=result)
    time.sleep(0.1)

    return result


def login_request_is_valid(login_request):
    return ("name" in login_request.json) and ("password" in login_request.json)


@app.route('/user/api/login', methods=['POST'])
def login():
    """
    用户登录
    """
    if not login_request_is_valid(request):
        abort(400)

    # 去redis中查找该用户密码，验证用户输入的密码是否正确
    # 正确则返回True，否则返回False
    name = request.json["name"]
    password = request.json["password"]

    # 若redis中不存在name则直接返回
    if not redis_client.exists(name):
        return "该用户不存在!\n"

    expected_password = redis_client.hget(name=name, key="password").decode()
    if expected_password != password:
        return "密码错误!\n"
    else:
        return "登录成功!\n"


def update_passwd_request_is_valid(update_passwd_request):
    # TODO:新旧密码不能相同
    return ("name" in update_passwd_request.json) and \
           ("old_password" in update_passwd_request.json) and \
           ("new_password" in update_passwd_request.json)


@app.route('/user/api/update_password', methods=['POST'])
def update_password():
    """
    更新用户密码
    """
    if not update_passwd_request_is_valid(request):
        abort(400)
    # 去redis中查找该用户密码，验证用户输入的旧密码是否正确
    #      如果旧密码正确，则更新用户的密码为新密码，同时将更新密码这一事件写入kafka，任务管理系统会从kafka中读取该事件
    #      kafka server应当事先建立一个名为user-task并且只包含一个partition的topic，用于传递用户管理系统和任务管理系统之间的消息
    name = request.json["name"]
    old_password = request.json["old_password"]
    new_password = request.json["new_password"]

    # 若redis中不存在name则直接返回
    if not redis_client.exists(name):
        return "该用户不存在!请检查用户名。\n"

    expected_password = redis_client.hget(name=name, key="password").decode()
    if expected_password != old_password:
        return "密码错误!请输入正确密码。\n"
    else:
        redis_client.hset(name=name, key="password", value=new_password)

        # 将注册新用户这一事件写入kafka，任务管理系统会从kafka中读取该事件
        result = {
            "success": False,
            "debug_info": ""
        }
        msg_update_password = MSG_UPDATE_PASSWORD.format(name=name).encode()
        kafka_producer.send(USER_TASK_TOPIC, msg_update_password).\
            add_callback(on_send_success, result=result).\
            add_errback(on_send_fail, result=result)
        time.sleep(0.1)
        return "密码修改成功!\n"


def reset_department_request_is_valid(update_request):
    return ("name" in update_request.json) and ("password" in update_request.json) and ("department" in update_request.json)


@app.route('/user/api/reset_department', methods=['POST'])
def reset_department():
    """
    更新用户密码
    :param name: 用户名
    :param password: 密码
    :param department: 新部门
    :
    :return:
    """
    # 去redis中查找该用户密码，验证用户输入的旧密码是否正确
    #      如果密码正确，则更换用户的部门为新部门，同时将更换部门这一事件写入kafka，任务管理系统会从kafka中读取该事件同步修改该用户的部门
    #      kafka server应当事先建立一个名为user-task并且只包含一个partition的topic，用于传递用户管理系统和任务管理系统之间的消息
    #      消息格式为MSG_UPDATE_DEPARTMENT
    if not reset_department_request_is_valid(request):
        abort(400)
    
    name = request.json["name"]
    password = request.json["password"]
    department = request.json["department"]

    # 若redis中不存在name则直接返回
    if not redis_client.exists(name):
        return "该用户不存在!请检查用户名。\n"

    expected_password = redis_client.hget(name=name, key="password").decode()
    if expected_password != password:
        return "密码错误!请输入正确密码。\n"
    else:
        redis_client.hset(name=name, key="department", value=department)

        # 将更换部门这一事件写入kafka，任务管理系统会从kafka中读取该事件
        result = {
            "success": False,
            "debug_info": ""
        }
        msg_update_department = MSG_UPDATE_DEPARTMENT.format(name=name, department=department).encode()
        kafka_producer.send(USER_TASK_TOPIC, msg_update_department).\
            add_callback(on_send_success, result=result).\
            add_errback(on_send_fail, result=result)
        time.sleep(0.1)
        return "用户部门修改成功!\n"

def consume_kafka():
    """
    从kafka中消费员工管理系统发来的消息
    :return:
    """
    while True:
        tp_to_records = kafka_consumer.poll()
        kafka_consumer.commit()
        for tp in tp_to_records:
            records = tp_to_records[tp]
            for record in records:
                # print('get message from kafka', record)
                msg = record.value.decode()
                msg_slices = msg.split('|')
                if msg_slices[0] == "new employee":
                    number = msg_slices[1]
                    name = msg_slices[2]
                    department = msg_slices[3]
                    password = msg_slices[4]
                    register(number=number, name=name, department=department, password=password)
        time.sleep(1)


if __name__ == "__main__":
    consume_threading = threading.Thread(target=consume_kafka, name="ConsumeThreading")
    consume_threading.start()
    app.run(host="0.0.0.0")
