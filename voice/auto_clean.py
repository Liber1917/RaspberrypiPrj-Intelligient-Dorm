import os


def clean_cache(start, end):
    file_path = '../sound/'
    num = start

    for i in range(num, end):
        path = file_path + str(i) + ".wav"
        if os.path.exists(path):
            # 删除文件
            os.remove(path)
            print(f"文件 {path} 已成功删除。")
        else:
            print(f"文件 {path} 不存在。")


if __name__ == '__main__':
    clean_cache(0, 230)