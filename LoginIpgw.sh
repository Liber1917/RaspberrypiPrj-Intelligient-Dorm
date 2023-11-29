#!/bin/bash

# 获取sudo密码
password="tdt"

# 调用sudo命令并自动填充密码
echo "$password" | sudo -S ipgw i
