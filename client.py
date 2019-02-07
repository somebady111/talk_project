#!/usr/bin/env python
#coding=utf-8
#客户端
'''
udp协议
一级界面:选项功能，登录，注册
功能:登录，注册
二级界面:查询界面,并打印出相关标签
'''

#导入库
from socket import *
import sys
import time
import getpass

#创建主函数
def main():
    print('欢迎使用xxx')

    #创建套接字数据报
    sockfd = socket(AF_INET,SOCK_DGRAM)

    while True:
        time.sleep(1)
        #打印出一级界面,此为提示信息
        print('\n+---------------------------+')
        print('|           请选择          |')
        print('|           1.登录          |')
        print('|           2.注册          |')
        print('|           3.退出          |')
        print('+---------------------------+\n')
        i = input('请输入您的选择:')
        if i in ['1','2','3']:
            if i == '1':
                #用do_login函数实现登录
                do_login(sockfd)

            elif i == '2':
                #用do_register函数实现注册
                do_register(sockfd)

            elif i == '3':
                print('谢谢使用!')
                time.sleep(0.5)
                break

        else:
            print('您的输入不再选项中!')
            continue

#注册功能
def do_register(sockfd):
    while True:
        username = input('请输入用户名>>:')
        password = getpass.getpass()
        password1 = getpass.getpass('again:')
        if (' ' in username) and (' ' in password):
            print('您输入的用户名和密码不能有空格')
            continue
        elif password != password1:
            print('两次输入的密码不一致,请确认后再行输入!')
            continue

        msg = 'R %S %S'%(username,password)
        sockfd.sendto(msg.encode())
        data = s.recvfrom(128).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXIST':
            print('用户已存在!')
        else:
            print('注册失败!')
        return    

#实现登录
def do_login(sockfd):
    username = input('请输入您的用户名>>:')
    password = getpass.getpass()
    msg = "L %s %s"%(username,password)
    sockfd.sento(msg.encode())
    data = sockfd.recvfrom(128)
    if data == 'OK':
        print('登录成功!')
        time.sleep(0.2)
        login(sockfd)
    else:
        print('您的账户不存在或账户密码输入有误,请重新确认后进行输入!')

#登录后进入二级界面
def login(s):
    print('欢迎来到xxx您可在此查询您的需求')
    message = input('请输入您的需求>>:')
    msg = 'S %s'%message
    data = s.sendto(msg.encode())
    if data == 'OK':
        print(data.decode())
    else:
        print('您查找的信息不存在!')

main()