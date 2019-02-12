#!/usr/bin/env python
#_*_coding_*_='utf-8'
#服务端
'''
udp协议
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
    s = socket(AF_INET,SOCK_DGRAM)
    #绑定地址
    s.bind(ADDR)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        data,addr = s.recvfrom(1024)
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(s,db)
            sys.exit(0)
        else:
            s.close()

#处理子进程
def do_child(s,db):
    while True:
        data = s.recvfrom(128).decode()
        if data[0] == 'L':
            do_login(s,db,data)
        elif data[0] == 'R':
            do_register(s,db,data)
        elif data[0] == 'S':
            do_search(s,db,data)
        
def do_register(s,db,data):
    name = data.split(' ')[1]
    password = data.split(' ')[2]
    #创建游标和sql语句
    cursor = db.cursor()
    sql = 'select keyword from 关键词 = %s'%name
    #执行sql语句
    cursor.execute(sql)
    r = cursor.fetchone()
    #如果查找的r不为空，返回一个exist，如果为空，则插入语句
    if r != None:
        s.sendto(b'exist')
        return
    sql = "insert into user(username,password) values('%s','%s')"%(name,password)
    try:
        #执行sql语句
        cursor.execute(sql)
        db.commit()
        s.sendto(b'OK')
    except Exception:
        db.rollback()
        s.send(b'False')

main()
