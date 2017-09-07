import os
lines=os.popen('ps | grep python').read()
lines=lines.split(' ')
id=lines[1]
os.popen('kill -s 9 %s'%id)
