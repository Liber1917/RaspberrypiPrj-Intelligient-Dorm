import speech_recognition as sr

def select_microphone():
    # 获取可用的麦克风设备
    microphones = sr.Microphone.list_microphone_names()

    if not microphones:
        print("未找到麦克风设备")
        return None

    # 打印可用的麦克风设备列表
    print("可用的麦克风设备：")
    for i, microphone in enumerate(microphones):
        print(f"{i+1}. {microphone}")

    # 让用户选择麦克风设备
    selected_index = int(input("请选择麦克风设备的编号：")) - 1

    if selected_index < 0 or selected_index >= len(microphones):
        print("选择的麦克风设备无效")
        return None

    # 返回用户选择的麦克风设备
    return selected_index


microphone_index = select_microphone()
print(microphone_index)