from myredis.client import redis_client
from mykafka.consumer import kafka_consumer
from mykafka.producer import kafka_producer


MSG_NEW_USER = "new user|{name}|{password}|{number}|{department}"
MSG_UPDATE_PASSWORD = "update password|{name}|{is_employee}"


def register(name, password, number=None, department=None):
    """
    注册一个新用户
    :param name: 用户名
    :param password: 密码
    :param number: 如果该用户是员工，number表示工号，否则number为None
    :param department: 如果该用户是员工，department表示部门，否则department为None
    :return: None
    """
    # TODO:将用户信息写入redis
    #      员工和普通用户的信息要分别存储在两个不同数据库

    # TODO:将注册新用户这一事件写入kafka，任务管理系统会从kafka中读取该事件
    #      kafka server应当事先建立一个名为user-task并且只包含一个partition的topic，用于传递用户管理系统和任务管理系统之间的消息
    #      消息格式为MSG_NEW_USER
    #      消息构造示例：MSG_NEW_USER.format(name="alice", password="123456", number="#", department="#")


def login(name, password):
    """
    用户登录
    :param name: 用户名
    :param password: 密码
    :return: 登录成功返回True，失败返回False
    """
    # TODO:去redis中查找该用户密码，验证用户输入的密码是否正确
    #      正确则返回True，否则返回False


def update_password(name, old_passwd, new_passwd):
    """
    更新用户密码
    :param name: 用户名
    :param old_passwd: 旧密码
    :param new_passwd: 新密码
    :return:
    """
    # TODO:去redis中查找该用户密码，验证用户输入的旧密码是否正确
    #      如果旧密码正确，则更新用户的密码为新密码，同时将更新密码这一事件写入kafka，任务管理系统会从kafka中读取该事件
    #      验证密码的过程中，可以知道该用户是普通用户还是员工，更新密码事件需要包含这一信息，从而让任务管理系统更方便地进行查询
    #      kafka server应当事先建立一个名为user-task并且只包含一个partition的topic，用于传递用户管理系统和任务管理系统之间的消息
    #      消息格式为MSG_UPDATE_PASSWORD
    #      消息构造示例：MSG_UPDATE_PASSWORD.format(name="alice", is_employee="yes")
