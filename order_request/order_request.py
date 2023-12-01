from get_class import p_id
from voice.list_keywords import listed

def order_react(order_queue):
    while True:
        if order_queue.empty():
            continue
        order = order_queue.get()
        if order == 'voice3':
            p_id.main()
        elif order == 'voice0':
            print("开灯")
        elif order == 'voice_introduce':
            listed()
        else:
            print("无法识别的指令")
