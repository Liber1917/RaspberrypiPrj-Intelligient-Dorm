try:
    import pyttsx3
except ImportError:
    print("pyttsx3未安装")
try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Selenium未安装")
try:
    from datetime import datetime
    import time
except ImportError:
    print("datetime未安装")
try:
    import re
except ImportError:
    print("re未安装")


time_table = [["星期", "上课时间", "课程名称", "地点", "上课周数"]]


def split_title(sub_id, subtitle, sub_rowspan):
    id_match = re.findall(r'(\d+)_', sub_id)
    course_name_match = re.findall(r'^(.*?)\(', subtitle)
    time_match = re.findall(r'\(([-|\d|\s]+),', subtitle)
    if len(time_match) != 0:
        print("time_match:", time_match[0])
        week_count = re.findall(r'(\d+-\d+)', time_match[0])
        week_count_2 = re.findall(r'(?<!\S)\d+(?!\S)', time_match[0])
        if len(week_count) != 0:
            for week in week_count:
                week_split = week.split('-')
                for i in range(int(week_split[0]), int(week_split[1])+1):
                    week_count_2.append(str(i))
        week_schedule = [int(x) for x in week_count_2]
        week_schedule = sorted(week_schedule)
    else:
        week_schedule = 0
        week_count = 0
    location_match = re.findall(r',(\w+)\*', subtitle)
    if not location_match:
        location_match.append("未知")
    print("课程名称：", course_name_match, "上课周数", time_match, "地点：", location_match, "ID：", id_match, "Week", week_count, week_schedule)
    date = int(int(id_match[0]) / 12 + 1)
    class_num = int(int(id_match[0]) % 12 + 1)

    last_time = "第"+str(class_num)+"到"+str((class_num - 1) + int(sub_rowspan))+"节课"
    print(last_time)
    time_table.append([int(date), last_time, course_name_match[0], location_match[0], week_schedule])


def login(switch):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Edge(options=chrome_options)  # 启动浏览器 options=options

    print("start")
    start_time = time.time()  # Start timing

    if switch == '1':
        driver.get("https://pass.neu.edu.cn/tpass/login")  # 信息门户
    elif switch == '2':
        driver.get("https://portal.neu.edu.cn/desktop/#/dashboard")  # 统一门户
    elif switch == '3':
        driver.get("https://portal.neu.edu.cn/desktop/#/microapp")  # 应用
    elif switch == '4':
        driver.get("http://219.216.96.4/eams/homeExt.action")  # 教务系统
    elif switch == '5':
        driver.get("http://ipgw.neu.edu.cn/srun_portal_pc?ac_id=1&theme=pro")  # IP网关
    else:
        print("无效的选择")

    # 指定密钥文件路径，文件第一行放账号，第二行放密码
    file_path = './Lginconf.txt'

    with open(file_path, 'r') as file:
        KEY = file.read().split("\n")

    # 密钥内容
    print(KEY)
    text_person = driver.find_element(By.ID, "un")
    text_person.send_keys(KEY[0])
    text_password = driver.find_element(By.ID, "pd")
    text_password.send_keys(KEY[1])
    log_in_btn = driver.find_element(By.ID, "index_login_btn")
    log_in_btn.click()

    end_time = time.time()  # End timing
    print("请求耗时：", end_time - start_time, "s")

    button = driver.find_element(By.XPATH, '//a[@href="/eams/courseTableForStd.action"]')
    button.click()

    wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.infoTitle')))
    # sele = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#startWeek')))
    # select = Select(sele)
    # select.select_by_value('14')

    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.infoTitle')))
    for element in elements:
        id = element.get_attribute('id')
        print("ID:", id)
        rowspan = element.get_attribute('rowspan')
        print("Rowspan:", rowspan)
        titles = element.get_attribute('title')
        print("Titles:", titles)
        split_list = titles.split(';')
        if split_list[1] == '':
            title = split_list[0]+split_list[3]
            print("Title:", title)
            split_title(id, title, rowspan)
        else:
            title = split_list[0]+split_list[1]
            print("Title:", title)
            split_title(id, title, rowspan)
            title = split_list[2]+split_list[3]
            print("Title:", title)
            split_title(id, title, rowspan)

    print("HTML 内容已保存为 source.html 文件")

    # 获取当前会话的所有Cookie
    cookies = driver.get_cookies()
    # print("cookie:",cookies)

    # 遍历cookie列表，查找JSESSIONID对应的value值
    for cookie_dict in cookies:
        if cookie_dict['name'] == 'JSESSIONID':
            jsessionid_value = cookie_dict['value']
            # JSESSIONID对应的value值
            # print(jsessionid_value)
            return jsessionid_value


def main():
    # options = Options()
    # options.add_experimental_option("detach", True)  # 防止浏览器自动关闭

    print('''
    选择你要登录的网址：
    1. 信息门户
    2. 统一门户
    3. 应用
    4. 教务系统
    5. IP网关
    ''')
    # login(input(), options)
    login('4')

if __name__ == "__main__":
    main()
    date = datetime.now().weekday()+1
    print(date)

    print(time_table[0])
    time.sleep(1)
    time_table = sorted(time_table[1:], key=lambda x: x[0])
    for schedule in time_table:
        print(schedule)
        if schedule[0] == date:
            engine = pyttsx3.init()
            engine.say("从"+schedule[1]+"在"+schedule[3]+"上"+schedule[2])
            engine.runAndWait()
