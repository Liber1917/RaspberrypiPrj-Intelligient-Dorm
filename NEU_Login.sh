###################################################################
# author: wangbin(gkwangbin@126.com)                              #
# date: 2017-06-02                                                #
###################################################################
#!/bin/bash

ip=`ifconfig wlp2s0 |grep "inet addr"| cut -f 2 -d ":"|cut -f 1 -d " "`
#echo $ip
option="${1}"
username=账号
passwd=密码

echo "账户名称: ${username}";
# --login  登录
# --logoff 注销
# --logout 断开
# --info   信息

case $option in
    --login) curl -s -H "ipgw.neu.edu.cn" --data "action=login&ac_id=1&user_ip=&nas_ip=&user_mac=&url=/include/auth_action.php&username=${username}&password=${passwd}&save_me=0" 'https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1' | grep -o -E "已经在线了|网络已连接"
    ;;
    --logoff) curl -s -H "ipgw.neu.edu.cn" --data "action=auto_logout&user_ip=${ip}" 'https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1' | grep -o -E "网络已断开|您似乎未曾连接到网络"
        ;;
    --logout) curl -s -H "ipgw.neu.edu.cn" --data "action=logout&username=${username}&password=${passwd}&ajax=1" 'https://ipgw.neu.edu.cn/include/auth_action.php'
        echo
        ;;
    --info) curl -s -H "ipgw.neu.edu.cn" --data "action=get_online_info" 'https://ipgw.neu.edu.cn/include/auth_action.php' | awk 'BEGIN{FS=","} {if($1=="not_online"){status="not online" } else {status="online"; total=$1/1073741824; time=$2/3600}} END{printf "账号状态: %-s\n", status; printf "已用流量: %-8.2f GB\n", total; printf "已用时长: %-8.2f hours\n", time;printf "账户余额: %-8s Yuan\n", $3; printf  "ip  地址: %-s", $6;}'
        echo
        ;;
    --help) echo "--login 登录"
        echo "--logoff 注销"
        echo "--logout 全部断开"
        echo "--info 上网信息"
        ;;
    *) echo "please input operation command, command --help"
    ;;
esac
