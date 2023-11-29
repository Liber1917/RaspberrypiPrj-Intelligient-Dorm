/*
    读取4*4键盘矩阵的键值 
    
*/

#include <wiringPi.h>
#include <stdio.h>

#define R1 24   //键盘矩阵(row1)     行1     wiringPi编号24（BCM 19）
#define R2 26   //键盘矩阵(row2)     行2     wiringPi编号26（BCM 12）
#define R3 23   //键盘矩阵(row3)     行3     wiringPi编号23（BCM 13） 
#define R4 27   //键盘矩阵(row4)     行4     wiringPi编号27（BCM 16）
#define C1 28   //键盘矩阵(column1)  列1     wiringPi编号28（BCM 20）
#define C2 25   //键盘矩阵(column2)  列2     wiringPi编号25（BCM 26）
#define C3 6    //键盘矩阵(column3)  列3     wiringPi编号6 （BCM 25）
#define C4 5    //键盘矩阵(column4)  列4     wiringPi编号5 （BCM 24）

int key[4][4] = {{1,2,3,4}, {5,6,7,8}, {9,10,11,12}, {13,14,15,16}};



int get_row()
{
    //设置列 C1~C4 输出高电平
    pinMode(C1, OUTPUT);
    digitalWrite(C1, HIGH);
    pinMode(C2, OUTPUT);
    digitalWrite(C2, HIGH);
    pinMode(C3, OUTPUT);
    digitalWrite(C3, HIGH);
    pinMode(C4, OUTPUT);
    digitalWrite(C4, HIGH);

    //设置行 R1~R4 为下拉输入
    pinMode(R1, INPUT);
    pullUpDnControl(R1, PUD_DOWN);
    pinMode(R2, INPUT);
    pullUpDnControl(R2, PUD_DOWN);
    pinMode(R3, INPUT);
    pullUpDnControl(R3, PUD_DOWN);
    pinMode(R4, INPUT);
    pullUpDnControl(R4, PUD_DOWN);

    //哪一行检测到高电平就返回哪一行的行号
    if (digitalRead(R1) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(R1) == HIGH)
        {
            return 1;
        }
        
    }
    if (digitalRead(R2) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(R2) == HIGH)
        {
            return 2;
        }
        
    }
    if (digitalRead(R3) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(R3) == HIGH)
        {
            return 3;
        }
        
    }
    if (digitalRead(R4) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(R4) == HIGH)
        {
            return 4;
        }
        
    }

    //所有行都没有检测到高电平就返回-1
    return -1;
}

int get_column()
{
    //设置行 R1~R4 输出高电平
    pinMode(R1, OUTPUT);
    digitalWrite(R1, HIGH);
    pinMode(R2, OUTPUT);
    digitalWrite(R2, HIGH);
    pinMode(R3, OUTPUT);
    digitalWrite(R3, HIGH);
    pinMode(R4, OUTPUT);
    digitalWrite(R4, HIGH);

    //设置列 C1~C4 为下拉输入
    pinMode(C1, INPUT);
    pullUpDnControl(C1, PUD_DOWN);
    pinMode(C2, INPUT);
    pullUpDnControl(C2, PUD_DOWN);
    pinMode(C3, INPUT);
    pullUpDnControl(C3, PUD_DOWN);
    pinMode(C4, INPUT);
    pullUpDnControl(C4, PUD_DOWN);

    //哪一列检测到高电平就返回哪一列的列号
    if (digitalRead(C1) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(C1) == HIGH)
        {
            return 1;
        }
        
    }
    if (digitalRead(C2) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(C2) == HIGH)
        {
            return 2;
        }
        
    }
    if (digitalRead(C3) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(C3) == HIGH)
        {
            return 3;
        }
        
    }
    if (digitalRead(C4) == HIGH)
    {
        delay(10);      //延时去抖动
        if (digitalRead(C4) == HIGH)
        {
            return 4;
        }
        
    }

    //所有列都没有检测到高电平就返回-1
    return -1;
}

int main(void)
{
	//初始化连接失败时，将消息打印到屏幕
	if(wiringPiSetup() == -1){ 
		printf("setup wiringPi failed !");
		return 1; 
	}
    
    while (1)
    {
        int row, column;
        if ((row = get_row()) > 0)
        {
            if ((column = get_column()) > 0)
            {
                do
                {
                    ;   //等待按键弹起
                } while (get_row() > 0);
                
                printf("(%d,%d)\n",row, column);
            }
            
        }
        
    }
    

	return 0;
}

