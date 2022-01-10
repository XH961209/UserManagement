import smtplib
from email.mime.text import MIMEText
'''
发送邮件函数，默认使用163smtp
:param mail_host: 邮箱服务器，16邮箱host: smtp.163.com
:param port: 端口号,163邮箱的默认端口是 25
:param username: 邮箱账号 xx@163.com
:param passwd: 邮箱密码(不是邮箱的登录密码，是邮箱的授权码)
:param usermail: 邮箱接收人地址
:param title: 邮件标题
:param content: 邮件内容
:return:
'''
 

def send_mail(usermail, content, username="18621830838@163.com", passwd="UZXDSBRURPAVUXTO", title="初始密码", mail_host='smtp.163.com', port=25):
  msg = MIMEText(content)  # 邮件内容
  msg['Subject'] = title   # 邮件主题
  msg['From'] = username   # 发送者账号
  msg['To'] = usermail      # 接收者账号
  smtp = smtplib.SMTP(mail_host, port=port)   # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
  smtp.login(username, passwd)          # 登录发送者的邮箱账号，密码
  # 参数分别是 发送者，接收者，第三个是把上面的发送邮件的 内容变成字符串
  smtp.sendmail(username, usermail, msg.as_string())
  smtp.quit() # 发送完毕后退出smtp
  print('email send success.')

if __name__ == '__main__':
  userMail = '123@qq.com'
  content = '随机数字'
  send_mail( userMail, content)
