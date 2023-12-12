from get_class import p_id
from voice.list_keywords import listed
from light_control import light_control

def order_react(order_queue):
    light_status = 0  # 0 for close, 1 for open
    while True:
        if order_queue.empty():
            continue
        order = order_queue.get()
        if order == 'voice3':
            p_id.main()
        elif order == 'voice0':
            print("switching light")
            if light_status == 0:
                light_control.light_opening()
                light_status = 1
            else:
                light_status = 0
                light_control.light_close()
        elif order == 'voice_introduce':
            listed()
        else:
            print("无法识别的指令")
