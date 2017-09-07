#!usr/bin/python
import serial
from time import sleep
import sys
def serialinit(port,Hz,timeouts):
    serial_handle=serial.Serial(port,Hz,timeout=timeouts)
    return serial_handle
def recv(serial_handle):
    while True:
        data=serial_handle.readline()
        if data=='' or len(data)!=53:
            continue
        else:
            break
    data=data[:len(data)-1]
    return data
def formatline(data):
    length=len(data)
    data=data.decode()
    if data[0]=='S' and data[length-1]=='E':
        data=data[1:length-1]
        order,datas=data.split('!')
        mpudatas=datas.split('#')
        mpudatas.remove("")
        mpudatas.append(order)
    return mpudatas
def Pack(line):
    order=line[6]
    line.remove(order)
    order=int(order)
    boxline={}
    boxline[order]=line
    return boxline
def send(boxline):
    for i in range(1,5):
        if  i not in boxline.keys():
            boxline[i]=["_Error_","_Error_","_Error_","_Error_","_Error_","_Error_"]
    strtosend="<%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s!%s|%s|%s>" % (boxline[1][0],boxline[1][1],boxline[1][2],boxline[1][3],boxline[1][4],boxline[1][5],
    boxline[2][0],boxline[2][1],boxline[2][2],boxline[2][3],boxline[2][4],boxline[2][5],
    boxline[3][0],boxline[3][1],boxline[3][2],boxline[3][3],boxline[3][4],boxline[3][5],
    boxline[4][0],boxline[4][1],boxline[4][2],boxline[4][3],boxline[4][4],boxline[4][5])
    print(strtosend)
def datatosend(serial_handles):
    dic={}
    for serial_handle in serial_handles:
        data=recv(serial_handle)
        dic.update(Pack(formatline(data)))
    return send(dic)
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
    

if  __name__=="__main__":
    serial_handles=serials_handleinit(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    count=0
    while True:
        count+=1
        datatosend(serial_handles)
        if count ==30:
            for serial in serial_handles:
                serial.flushInput()

        
        
   
            
