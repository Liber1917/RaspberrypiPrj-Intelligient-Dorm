import os

file_path = 'sound/'
num = 0
while True:
    if os.path.exists(file_path + str(num) + ".wav"):
        num += 1
    else:
        break
print("文件数量：", num)
# 检查文件是否存在
for i in range(0, num):
    path = file_path + str(i) + ".wav"
    if os.path.exists(path):
        # 删除文件
        os.remove(path)
        print(f"文件 {path} 已成功删除。")
    else:
        print(f"文件 {path} 不存在。")