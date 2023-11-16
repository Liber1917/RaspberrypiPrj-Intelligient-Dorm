import time
import RPi.GPIO as GPIO
import sys,os

class keypad(object):
  KEYPAD=[
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']]

  ROW    =[19,12,13,16]#行
  COLUMN =[20,26,25,24]#列

#初始化函数
def __init__():
  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)
  print("init done\n")
#取得键盘数函数
def getkey():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
#设置列输出低
  for i in range(len(keypad.COLUMN)):
    GPIO.setup(keypad.COLUMN[i],GPIO.OUT)
    GPIO.output(keypad.COLUMN[i],GPIO.LOW)
#设置行为输入、上拉
  for j in range(len(keypad.ROW)):
    GPIO.setup(keypad.ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)

#检测行是否有键按下，有则读取行值
  RowVal=-1
  for i in range(len(keypad.ROW)):
    RowStatus=GPIO.input(keypad.ROW[i])
    if RowStatus==GPIO.LOW:
      RowVal=i
      print('RowVal=%s' % RowVal)
#若无键按下,则退出，准备下一次扫描
  if RowVal<0 or RowVal>3:
    exit()
    return

#若第RowVal行有键按下，跳过退出函数，对掉输入输出模式
#第RowVal行输出高电平，
  GPIO.setup(keypad.ROW[RowVal],GPIO.OUT)
  GPIO.output(keypad.ROW[RowVal],GPIO.HIGH)
#列为下拉输入
  for j in range(len(keypad.COLUMN)):
    GPIO.setup(keypad.COLUMN[j],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#读取按键所在列值
  ColumnVal=-1
  for i in range(len(keypad.COLUMN)):
    ColumnStatus=GPIO.input(keypad.COLUMN[i])
    if ColumnStatus==GPIO.HIGH:
      ColumnVal=i
#等待按键松开
      while GPIO.input(keypad.COLUMN[i])==GPIO.HIGH:
        time.sleep(0.05)
        print ('ColumnVal=%s' % ColumnVal)
#若无键按下，返回
  if ColumnVal<0 or ColumnVal>3:
    exit()
    return

  exit()
  return keypad.KEYPAD[RowVal][ColumnVal]


def exit():
  #print("exit\n")
  import RPi.GPIO as GPIO
  for i in range(len(keypad.ROW)):
    GPIO.setup( keypad.ROW[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
  for j in range(len( keypad.COLUMN)):
    GPIO.setup( keypad.COLUMN[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)


#key=None

# 检查文件是否可以写入
if os.access('output.txt', os.W_OK):
  with open('output.txt', 'w') as f:
    while True:
      key = getkey()
      try:
        if not key==None:
          data = 'You enter the key: ' + key + '\n'
          print(data,end='')
          print("input success\n")
          f.write(data)
          #f.flush()  # 立即将数据写入文件
          #f.close()
      except KeyboardInterrupt:
        GPIO.cleanup()
        break  # 退出循环

  f.close()

else:
  print('文件不可写入')
