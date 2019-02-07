#!/usr/bin/env python
#coding='utf-8'
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

#创建主函数
def main():
    #创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    #绑定地址
    s.bind('0.0.0.0',8888)
    while True:
        #处理僵尸进程
        signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(s)
            sys.exit(0)
        else:
            s.close()

def do_child(s):
    while True:
        data = s.recvfrom(128).decode()
        

pass
