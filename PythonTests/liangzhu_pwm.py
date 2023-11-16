import RPi.GPIO as GPIO
import time

Buzzer = 11 #蜂鸣器接在第11管脚上

# 定义低中高频率
CL = [0, 262, 294, 330, 349, 392, 440, 494]		# Frequency of Low C notes

CM = [0, 523, 587, 659, 698, 784, 880, 988]		# Frequency of Middle C notes

CH = [0, 1046, 1175, 1318, 1397, 1568, 1760, 1976]		# Frequency of High C notes

# 第一首歌谱子频率
song_1 = [	CL[3], CL[5], CL[6], CM[1], CM[2], CL[6], CM[1], CL[5], # Notes of song1
		CM[5], CH[1], CM[6], CM[5], CM[3], CM[5], CM[2], CM[2], 
		CM[2], CM[3], CL[7], CL[6], CL[5], CL[6], CM[1], CM[2],
		CL[5], CL[6], CM[1], CM[2], CL[3], CM[1], CL[6], CL[5],
		CL[5], CM[1], CL[5]]
# 节奏
beat_1 = [	4, 3, 1, 3, 1, 1, 1, 2, 			# Beats of song 1, 1 means 1/8 beats
		3, 1, 1, 1, 1, 1, 4, 4, 
		3, 1, 2, 2, 3, 1, 2, 2, 
		3, 1, 2, 2, 2, 2, 1, 1, 
		1, 1, 8	]

song_2 = [	CM[3], CM[3], CM[5], CM[6], CH[1], CH[1], CM[6], CM[5], # Notes of song2
		CM[5], CM[6], CM[5], CM[5], CM[3], CM[3], CM[5], CM[6], 
		CH[1], CH[1], CM[6], CM[5], CM[5], CM[6], CM[5], CM[5], 
		CM[3], CM[5], CM[6], CM[5], CM[3], CM[2], CM[3], CM[5],
		CM[3], CM[2], CM[1], CM[2], CM[1], CM[3], CM[2], CM[1],
		CM[3], CM[2], CM[3], CM[5], CM[6], CH[1], CM[5], CM[2],
		CM[3], CM[5], CM[2], CM[3], CM[1], CL[6], CL[5], CL[6],
		CM[1], CM[2], CM[3], CM[1], CM[2], CM[1], CL[6], CL[5]	]

beat_2 = [	2, 1, 1, 1, 1, 1, 1, 2, 			# Beats of song 2, 1 means 1/8 beats
		1, 1, 2, 2, 2, 1, 1, 1, 
		1, 1, 1, 2, 1, 1, 4, 6, 
		1, 1, 4, 4, 2, 1, 1, 2,
		1, 1, 3, 1, 4, 1, 1, 1,
		1, 3, 1, 2, 1, 1, 4, 2,
		1, 1, 1, 1, 1, 1, 4, 2,
		2, 3, 1, 1, 1, 1, 1, 6 ]

# 一些初始化操作
def setup():
    GPIO.setwarnings(False)         # 先关掉警告，因为操作io口会有警告
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location 树莓派有很多编码模式，这里采用GPIO编码模式
    GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output Buzzer = 11 #蜂鸣器接在第11管脚上
    global Buzz						# Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.440HZ初试频率
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration 

def loop():
	while True:
		print( '\n    Playing song 1...')
		for i in range(1, len(song_1)):		# Play song 1
			Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
			time.sleep(beat_1[i] * 0.25)		# delay a note for beat * 0.5s 
		time.sleep(1)						# Wait a second for next song.

		print( '\n\n    Playing song 2...')
		for i in range(1, len(song_2)):     # Play song 1
			Buzz.ChangeFrequency(song_2[i]) # Change the frequency along the song note
			time.sleep(beat_2[i] * 0.25)     # delay a note for beat * 0.5s

# 释放资源
def destory():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		# Set Buzzer pin to High
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
