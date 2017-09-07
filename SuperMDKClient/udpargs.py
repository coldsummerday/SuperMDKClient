#!/usr/bin/python
import os
import serial
import threading
import gc
import socket
import sys
def serialinit(port,HZ,timeouts):
    ser=serial.Serial(port,HZ,timeout=timeouts)
    return ser
def sockinit(ip,port):
    socket_handle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_handle.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_handle.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return socket_handle
def udplink(socket_handle,addr,serial_handles):
    count=0
    while True:
        try:
            data=serialtodict(serial_handles)
            if socket_handle.sendto(data,addr):
                count+=1
                print(data)
                
            if count==600:
                gc.collect()
                count=0
                for serial in serial_handles:
                    serial.flushInput()
        except Exception,e:
	    print(str(e.message))
            break
    socket_handle.close()
def serialrecv(serial_handle):
    while True:
        data=serial_handle.readline()
        if data=='' or len(data)!=53:
            serial_handle.flush()
            continue
        else:
            break
    data=data[:len(data)-1]
    return data
def Pack(data):
    length=len(data)
    data=data.decode()
    order=0
    if data[0]=='S' and data[length-1]=='E':
        data=data[1:length-1]
        order,datas=data.split('!')
        mpudatas=datas.split('#')
        mpudatas.remove("")
        order=int(order)
    line={}
    line[order]=mpudatas
    return line
def datatosend(boxline):
    '''
    for i in range(1,5):
        if  i not in boxline:
            boxline[i]=["_Error_","_Error_","_Error_","_Error_","_Error_","_Error_"]
    '''
    strtosend="<%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s>" % (boxline[1][0],boxline[1][1],boxline[1][2],boxline[1][3],boxline[1][4],boxline[1][5],
    boxline[2][0],boxline[2][1],boxline[2][2],boxline[2][3],boxline[2][4],boxline[2][5],
    boxline[3][0],boxline[3][1],boxline[3][2],boxline[3][3],boxline[3][4],boxline[3][5],
    boxline[4][0],boxline[4][1],boxline[4][2])
    return strtosend
def serialtodict(serial_handles):
    dic={}
    for serial_handle in serial_handles:
        dic.update(Pack(serialrecv(serial_handle)))
    return datatosend(dic)
def serials_handleinit(serial1,serial2,serial3,serial4):
    serial_handles=[]
    serial_handle1=serialinit(serial1,115200,0.5)
    serial_handles.append(serial_handle1)
    serial_handle2=serialinit(serial2,115200,0.5)
    serial_handles.append(serial_handle2)
    serial_handle3=serialinit(serial3,115200,0.5)
    serial_handles.append(serial_handle3)
    serial_handle4=serialinit(serial4,115200,0.5)
    serial_handles.append(serial_handle4)
    return serial_handles
if __name__=='__main__':
    socket=sockinit('1',8887)
    serial_handles=serials_handleinit(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    addr=('<broadcast>',8887)
    thread_handle=threading.Thread(target=udplink,args=(socket,addr,serial_handles))
    thread_handle.start()
