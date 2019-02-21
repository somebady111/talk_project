#!/usr/bin/env python
#_*_coding_*_='utf-8'
#服务端
'''
tcp传输协议
处理客户端发送来的请求进行处理
多进程

'''

#导入库
from socket import *
import sys 
import os
import signal
import pymysql

#定义局部变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

#创建主函数
def main():
    #创建数据库链接
    db = pymysql.connect('localhost','root','123456','project')
    
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定地址
    s.bind(ADDR)
    s.listen(3)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    print("connect form port 8888")
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue 
        
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c,db) #子进程函数
            sys.exit(0)
        else:
            c.close()

#处理子进程
def do_child(c,db):
    #此处存在客户端接受问题
    while True:
        data = c.recv(128).decode()
        if data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'S':
            do_search(c,db,data)
        
def do_register(c,db,data):
    name = data.split(' ')[1]
    password = data.split(' ')[2]

    cursor = db.cursor()
    #创建游标和sql语句
    sql = "select * from user where username = '%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    
    #如果查找的r不为空，返回一个exist，如果为空，则插入语句
    if r != None:
        c.send(b'EXIST')
        return

    sql = "insert into user(username,password) values('%s','%s')"%(name,password)
    try:
        #执行sql语句
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'False')
def do_login(c,db,data):
    while True:
        name = data.split(' ')[1]
        password = data.split(' ')[2]

        #创建游标对象
        cursor = db.cursor()
        #编写sql语句
        sql = "select * from user where username = '%s'"%name
        r = cursor.fetchone()

        if r != None:
            c.send(b'OK')
        else:
            c.send(b'fault')


main()
