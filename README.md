# RaspberrypiPrj-Intelligient-Dorm
Task for Rasberrypi course
## Voice 语音识别
voice_input.py 可以合成语音用于测验
record_10s.py 用于录制
voice_vosk.py 用于识别

!!命令需知!!
如果想要添加命令， 向keyword_order.json中添加键值对， 键为命令， 值为对应的操作码。
## Gesture 手势识别
locate_hand.py是基础， 用于定位手部位置， 不是闲的没事别动这玩应  
deep_learning.py是用于训练模型的， 用于训练模型。  
如果想要重新训练模型， 请直接运行deep_learning.py。  

!!炼模须知!!  
1.左手右手正面反面是四种不同手势， 请注意区分。  
2.如果需要增加识别数量， 请在deep_learning.py中修改NUM_CLASSES的值。
并删掉原来的模型， 重新炼一个新的  
3.模型的默认位置是/model/src， 如果需要修改请在deep_learning.py中修改第42行的路径。
同时修改Test_recognition.py中第九行的模型路径。
## Get_class 课表获取
1.在Lginconf.txt中填入学号和密码， 用于登录教务系统。

---

![Intelligient Dorm](Intelligient%20Dorm.svg)