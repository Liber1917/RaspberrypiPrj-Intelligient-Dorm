> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [blog.csdn.net](https://blog.csdn.net/wanggao_1990/article/details/103702563?ops_request_misc=&request_id=&biz_id=102&utm_term=%E6%A0%91%E8%8E%93%E6%B4%BE%E4%B8%B2%E5%8F%A3%E9%80%9A%E4%BF%A1&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-103702563.142^v96^pc_search_result_base5&spm=1018.2226.3001.4187)

使用[树莓派](https://so.csdn.net/so/search?q=%E6%A0%91%E8%8E%93%E6%B4%BE&spm=1001.2101.3001.7020) 3B+/4B 测试 gpio，配置硬件串口，测试串口通信。  

#### 文章目录

*   [1、GPIO 扩展口定义、DB9 接口定义](#1GPIODB9_3)
*   [2、串口设置](#2_14)
*   *   [2.1 开启 GPIO 串口功能，并使用硬件串口](#21_09GPIO_30)
    *   [2.2 禁用串口的控制台功能](#22__47)
    *   [2.3 测试验证串口通信功能](#23__56)
    *   *   [2.3.1 c 语言实现](#231_c_64)
        *   [2.3.2 python 实现](#232_python_92)
        *   [2.3.3 minicom 命令函实现](#233__minicom_122)
    *   [2.4 wiringPi 库 c 语言完整串口通信代码](#24_wiringPic_134)
*   [3、GPIO 编程](#3GPIO__207)
*   *   [3.1 gpio 命令行](#31_gpio_212)
    *   [3.2 Python 库 RPi.GPIO 编程](#32__Python__RPiGPIO_225)
    *   [3.3 c/c++ 使用 wiringPI 库](#33__ccwiringPI_253)

1、GPIO 扩展口定义、DB9 接口定义
---------------------

这里的板子上 40pin 引脚有 3 中编码方式：  
1、Board 编码：对应实际的物理插槽  
2、BCM 编码：基本和 GPIO 的名字对应  
2、wiringPi 编码：wiringPi 库使用的引脚编码方式  
![](https://img-blog.csdnimg.cn/20191225171057561.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)  
DB9 公头接口定义  
![](https://img-blog.csdnimg.cn/20191225171134513.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)

在进行[串口通信](https://so.csdn.net/so/search?q=%E4%B8%B2%E5%8F%A3%E9%80%9A%E4%BF%A1&spm=1001.2101.3001.7020)，两个设备间进行双向通信时，**两个设备的 RXD、TXD 要交错连接**。

2、串口设置
------

树莓派包含两个串口（树莓派 3 及以前版本）  
1. **硬件串口**（**/dev/ttyAMA0**）, 硬件串口由硬件实现，有单独的波特率时钟源，性能高，可靠。一般优先选择这个使用。  
2.**mini 串口**（**/dev/ttyS0**），mini 串口时钟源是由 CPU 内核时钟提供，波特率受到内核时钟的影响，不稳定。

> 树莓派 3 及以前版本仅 2 个串口，4 和 400 有 4 个串口，cm 系列有 6 个串口，详见 [树莓派官网 Configuring UARTs](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-uarts)）  
> ,  
> 树莓派 4 开启 ttyAMA1，可以直接配置 dtoverlay=uart2 即可（其他 ttyAMA2 -> uart3, ttyAMA3 -> uart4, ttyAMA4 -> uart5，具体引脚配置可以通过 dtoverlay -h uartN 查看）。  
> ，  
> 注意 CM4 使用双相机的 dtb 配置（ [树莓派计算模块 CM4 eMMC 系统烧写、配置、相机连接](https://blog.csdn.net/wanggao_1990/article/details/121398020)）时，ttyAMA1 会失效。

想要通过树莓派的 GPIO 引脚进行稳定的串口通信，需要修改串口的映射关系。  
serial0 是 GPIO 引脚对应的串口，serial1 是蓝牙对应的串口，默认未启用 serial0。使用`ls -l /dev/serial*`查看当前的映射关系：  
![](https://img-blog.csdnimg.cn/20191225172309500.png)  
可以看到这里是，蓝牙串口 serial1 使用硬件串口 ttyAMA0。

### 2.1 开启 GPIO 串口功能，并使用硬件串口

使用`sudo raspi-config` 进入图形界面  
选择菜单 Interfacing Options -> P6 Serial,  
第一个选项（would you like a login shell to be accessible over serial?）选择 NO，  
第二个选项（would you like the serial port hardware to be enabled?）选择 YES

保存后重启，查看映射关系  
![](https://img-blog.csdnimg.cn/20191226121115159.png)  
比之前多了一个 gpio 的串口 serial0，并且使用的 ttyS0。这里已经是开启了 GPIO 串口功能，但是使用的 cpu 实现的软件串口。

**如果想使用稳定可靠的硬件串口，就要将树莓派 3b + 的硬件串口与 mini 串口默认映射对换**（先禁用蓝牙 `sudo systemctl disable hciuart`）。

在 / boot/config.txt 文件末尾添加一行代码 `dtoverlay=pi3-miniuart-bt` （树莓派 4B 也使用这个命令）。 还可以直接配置禁用 bluetooth，代码为 `dtoverlay=disable-bt`，见参考链接 [【树莓派 功能配置（含网络）不定期更新】](https://blog.csdn.net/wanggao_1990/article/details/114927334)。

保存后重启再查看设备对用关系，发现已经调换成功。  
![](https://img-blog.csdnimg.cn/20191226121650842.png)

### 2.2 禁用串口的控制台功能

前面步骤已经交换了硬件串口与 mini 串口的映射关系，但是，现在还不能使用树莓派串口模块与电脑进行通信，因为，[树莓派 gpio](https://so.csdn.net/so/search?q=%E6%A0%91%E8%8E%93%E6%B4%BEgpio&spm=1001.2101.3001.7020) 口引出串口默认是用来做控制台使用的，即是为了用串口控制树莓派，而不是通信。所以我们要禁用此默认设置。  
首先执行命令如下：  
`sudo systemctl stop serial-getty@ttyAMA0.service`  
`sudo systemctl disable serial-getty@ttyAMA0.service`  
然后执行命令行修改文件：  
`sudo nano /boot/cmdline.txt`  
并删除语句`console=serial0,115200`（没有的话就不需要此步骤）

### 2.3 测试验证串口通信功能

这里使用三种方式进行测试验证， c 语言下使用 wiringPi 库， python 语言下使用 serial 包，最后命令行使用 minicom 工具。  
先安装以上开发工具  
`sudo apt-get install wiringpi`  
`sudo apt-get install python-serial`  
`sudo apt-get install minicom`

将 usb 转 ttl 模块引脚的 GND、TX、RX 分别与树莓派的 GND、RX、TX 连接；电脑端启用串口调试助手，波特率设置一致。

#### 2.3.1 c 语言实现

编写 test.c 测试代码，

```
#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>
  
int main()
{
    int fd;
    if(wiringPiSetup()<0) {
        return 1;
    }

    //if((fd=serialOpen("/dev/ttyS0",115200))<0) { // gpio 使用mini串口
    if((fd=serialOpen("/dev/ttyAMA0",115200))<0) { // gpio 使用硬件串口
        return 1;
    }
 
    printf("serial test output ...\n");
    serialPrintf(fd,"1234567890abcdef");
 
    serialClose(fd);
    return 0;
}
```

编译 `gcc test.c -o test -lwiringPi`，运行 `sudo ./test`  
![](https://img-blog.csdnimg.cn/20191226145342535.png)![](https://img-blog.csdnimg.cn/20191226145501375.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)

#### 2.3.2 python 实现

```
# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial("/dev/ttyAMA0",115200)

if not ser.isOpen():
    print("open failed")
else:
    print("open success: ")
    print(ser)

try:
    while True:
        count = ser.inWaiting()
        if count > 0:
            recv = ser.read(count)
            print("recv: " + recv)
        	ser.write(recv)
        sleep(0.05) 
except KeyboardInterrupt:
    if ser != None:
        ser.close()
```

运行 python 代码，并在串口调试助手中发送字符串，树莓派收到数据后打印、在回发给串口助手，截图如下。  
![](https://img-blog.csdnimg.cn/20191226150241617.png)  
![](https://img-blog.csdnimg.cn/20191226150328220.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)

#### 2.3.3 minicom 命令函实现

使用`minicom -b 115200 -D /dev/ttyAMA0`进入串口调试界面，这里将一直等待接收，直到用户手动退出。退出时 ctrl+A，再按键 X 退出。  
minicom 调试界面默认是不显示用户输入，使用 cttl+A，再按 E 即可开启（**会捕获换行**）。

串口助手和 minicom 界面的交互如下:  
串口助手发送 “1234567890abcdef”，  
minicom 发送 "\n”，“1”，“\n”，“3”，“4”，“\n”  
串口助手发送 “1234567890abcdef”，

界面截图如下：  
![](https://img-blog.csdnimg.cn/20191226151101632.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)  
![](https://img-blog.csdnimg.cn/20191226151203120.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)

### 2.4 wiringPi 库 c 语言完整串口通信代码

使用 wiringPI 库进行发送和持续接收的示例代码，如下

```
#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>

#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

int running = 1;

void sig_handle(int sig)
{
   if(sig == SIGINT)   running = 0;
}

int main()
{    
    signal(SIGINT, sig_handle);    

    int fd;
    if(wiringPiSetup() < 0){
        printf("wiringPi setup failed.\n");
        return 1;
    }

    int baudrate = 115200;

    //if((fd = serialOpen("/dev/ttyS0", baudrate)) < 0){  
    if((fd = serialOpen("/dev/ttyAMA0",baudrate)) < 0){
        printf("serial open failed.\n");
        return 1;
    }

    printf("serial test output ...\n"); 
    serialPrintf(fd, "0123456789abcdef");  //发送

    while(running)
    {
       int sz = serialDataAvail(fd); // 等待介绍的数据个数
       
       if(sz > 0)
       {
         printf("size %d, ", sz);
         char *buff =(char*)malloc(sz);
         printf("recv: ");
         for(int i = 0; i < sz; i++){
              int c = serialGetchar(fd);  //接收一个字符
              //if(c != -1)
                  buff[i] = c;  
         }
         printf("%s\n", buff);
         free(buff);

         serialPrintf(fd, buff);//回显
       }
       else{
         usleep(50000); // 必要的延时50ms
       }
    }

    serialClose(fd);
    printf("close serial.\n");

    return 0;
}
```

> tip: 延时的作用：1、匹配串口读写速度，使得下一次读时，设备已经完成写操作; 2、减小资源占用;  
> 若不延时，CPU 占用高，并且最多一次读取一个字符。

3、GPIO 编程
---------

这里演示 BCM_gpio 22 输出控制，串接一个 220 欧姆、led 灯珠到 GND，进行亮、灭灯控制。  
![](https://img-blog.csdnimg.cn/20191226152456436.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)  
这里涉及引脚连线、编程中确定口线，需要熟悉引脚编码。先以 gpio 命令行工具说明编码、并进行测试，再使用 python、c 语言实现。

### 3.1 gpio 命令行

使用`gpio -v`查看版本  
![](https://img-blog.csdnimg.cn/20191226152943898.png)  
使用`gpio readall`查看引脚编码  
![](https://img-blog.csdnimg.cn/20191226155140748.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbmdnYW9fMTk5MA==,size_16,color_FFFFFF,t_70)  
**这里我们选择的名称为 "BCM_GPIO.22"，对应的是 BCM 编码 "22"，wPi 编码 "3"，而实际的物理插槽 BOARD 编码是 "15"。** 因此实际接线应该使用插槽编码为 15 的口线。

gpio 工具使用的是 BCM 编码。设置 BCM_GPIO.22 口为输出模式， 写”1” 灯亮，写”0” 灯灭。

```
gpio -g mode 22 out
gpio -g write 22 1
gpio -g write 22 0
```

### 3.2 Python 库 RPi.GPIO 编程

这里的操作结果同上，使用 RPi.GPIO 库。若无该库，先进行安装 `sudo pip install RPi.GPIO`  
先使用 python idle 进行简单控制

```
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)   ## 编号默认BCM
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)
GPIO.output(22, LOW)
GPIO.output(22, 1)
GPIO.output(22, 0)
```

在利用脚本让其间隔一秒钟亮灭

```
# -*- coding: utf-8 -*-                 
import RPi.GPIO as GPIO               #引入RPi.GPIO库函数命名为GPIO
import time                           #引入计时time函数
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)              #将GPIO编程方式设置为BOARD模式
# 输出模式
GPIO.setup(15, GPIO.OUT)              #将Board 15引脚（BCM 22）设置为输出引脚

while True:                            #条件为真，下面程序一直循环执行
    GPIO.output(15, GPIO.HIGH)         #将15引脚电压置高，点亮LED灯
    time.sleep(1)                      #延时1秒
    GPIO.output(15, GPIO.LOW)          #将15引脚电压置低，熄灭LED灯
    time.sleep(1)                      #延时1秒
```

### 3.3 c/c++ 使用 wiringPI 库

重复上面引用内容： **这里我们选择的名称为 "BCM_GPIO.22"，对应的是 BCM 编码 "22"，wPi 编码 "3"，而实际的物理插槽 BOARD 编码是 "15"。**

使用 wiringPI 库时，IO 口为 wPi 编码，为保证和前面的实列对应相同，使用编号为 **3**。

编写以下 test.c 代码  
编译 `gcc test.c -o test -lwiringPi`，运行 `./test`

```
#include <stdio.h>
#include <wiringPi.h>

// LED Pin - wiringPi pin 3 is BCM_GPIO 22.(pyscial 15)
#define  LED  3

int main (void)
{
  if(wiringPiSetup() < 0){
      printf("wiringPi setup failed.\n");
      return 1;
  }

  pinMode(LED, OUTPUT);  // 设置输出模式

  for (;;)
  {
    digitalWrite(LED, HIGH) ;	// On
    delay(500) ;		        // mS
    digitalWrite(LED, LOW) ;	// Off
    delay(500) ;
  }
  return 0 ;
}
```