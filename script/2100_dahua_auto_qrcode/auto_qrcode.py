'''
Author: 胡益华

Creation Date: 2024-04-21

Updated Date: 2024-09-06

Usage: python auto_qrcode.py

Description:
(1) 脚本用于 ssh 模式下，大华设备后台登录自动扫码
(2) 通过 ../config/auto_qr_user.ini 文件配置一些参数

Notice:
(1) 脚本仅支持 Windows 上运行
(2) 脚本通过 secureCRT 的日志记录功能实现扫码，故不支持 secureCRT 之外的仿真终端。
    secureCRT 的日志记录快捷键默认为 `alt + f + l`
(3) 脚本运行时，输入法必须为小写英文状态
(4) 脚本对 /C/Users/%USERNAME%/AppData/Local/Temp 目录需有写权限
(5) 会话终端的编码格式为 utf8
(6) 脚本运行时不能有其它影响字符串自动输入的操作，如切换窗口、手动输入字符串等
'''

import time
import ssl
import urllib.request
import sys
import os
import re
import pyautogui
import cv2
import configparser
from pyzbar.pyzbar import decode
from PIL import Image, ImageFont, ImageDraw

import fileModule

# 模拟按下Alt + F + L，打开secureCRT日志按钮，输入文件名
def qr_log_open(file_path):
    pyautogui.press("alt")
    pyautogui.press("f")
    pyautogui.press("l")
    time.sleep(0.1)
    pyautogui.write(f"{file_path}")
    pyautogui.press("enter")

# 通过pyzbar识别二维码中保存的信息，返回网址信息
def qrcode_checkurl(image_path):
    qr_url      = ""
    qr_image    = cv2.imread(image_path)
    qr_info     = decode(qr_image)
    if qr_info:
        qr_url  = qr_info[0].data.decode("utf-8")
        return qr_url
    return False

# 在终端打印出二维码
def get_qr_info(user_username):
    pyautogui.write("shell")
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.write(user_username)
    pyautogui.press("enter")
    time.sleep(0.2)

# 串口模式下，二维码出现速度极慢，这里做校验，若二维码不完全，则继续等待
def qr_txt_check(qr_txt_path):
    time.sleep(0.1)
    with open(qr_txt_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.find("██████████████") != -1:
                time.sleep(1)
                return True

# 将日志文件中的字符串转化成png图片格式，并扫描二维码得到网址
def qr_string_to_url(tmp_pre, qr_txt_path):
    qr_width, qr_height, elem_height, elem_width, type_size = (800, 800, 16, 8, 12)
    x, y        = 10, 10
    qr_url      = ""
    qr_img_path = f"{tmp_pre}\\qrcode.png"
    qr_img_path = fileModule.FMcreateUniqueFileName(qr_img_path)
    if not qr_img_path:
        return False
    image       = Image.new("RGB", (qr_width, qr_height), color="black")
    draw        = ImageDraw.Draw(image)
    font        = ImageFont.truetype(fileModule.FMgetAbsolutePath(".\\typeface\\arial.ttf"), type_size)

    with open(qr_txt_path, "r", encoding="utf-8") as file:
        for char in file.read():
            if char == "\n":
                x = 10
                y += elem_height
            elif char == " ":
                draw.text((x, y), "█", fill = "black", font = font)
                x += elem_width
            else:
                draw.text((x, y), char, fill = "white", font = font)
                x += elem_width

    image.save(qr_img_path)
    time.sleep(0.1)
    qr_url = qrcode_checkurl(qr_img_path)
    os.remove(qr_img_path)
    if qr_url:
        return qr_url
    return False

# 通过网址获取ssh登录的密码
def checkurl_checkcode(checkurl, user_password):
    password    = user_password
    items       = re.findall(r"(\w)=([^&]*)", checkurl)
    user        = ""
    ver         = ""
    txt         = ""
    for item in items:
        if item[0] == "v":
            ver = item[1]
        elif item[0] == "u":
            user = item[1]
        elif item[0] == "t":
            txt = item[1]
    url         = "https://svsh.dahuatech.com/cgi-bin/psh/svsh.cgi"
    data        = "user=%s&pwd=%s&ver=%s&txt=%s" % (user, password, ver, txt)
    checkcode   = None

    for _ in range(3):
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, data=data.encode(), timeout=15, context=context) as response:
                checkcode = response.read().decode()
                if len(re.sub("\r|\n", "", checkcode)) == 8:
                    return checkcode
                time.sleep(0.5)
        except:
            time.sleep(0.5)
    else:
        return False

# 资源释放
def resource_release(tmp_pre, exit_code=0):
    pyautogui.press("alt")
    pyautogui.press("f")
    pyautogui.press("l")

    # 删除可能遗留的所有qrcode*.tmp文件，某些情况下，历史遗留的二维码日志文件可能没有被删除
    # 此时用户已可以做其它操作，不必担心此模块影响扫码速度
    qr_files = os.listdir(tmp_pre)
    for file in qr_files:
        if file.lower().startswith("qrcode") and file.lower().endswith(".tmp"):
            file_path = os.path.join(tmp_pre, file)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass

    sys.exit(exit_code)

if __name__ == "__main__":
    username    = os.environ.get("USERNAME")
    tmp_pre     = f"C:\\Users\\{username}\\AppData\\Local\\Temp"
    qr_txt_path = f"{tmp_pre}\\qrcode.tmp"
    qr_txt_path = fileModule.FMcreateUniqueFileName(qr_txt_path)
    if not qr_txt_path:
        sys.exit(1)
    qr_log_open(qr_txt_path)

    config                      = configparser.ConfigParser()
    config_file                 = fileModule.FMgetAbsolutePath(".\\config\\auto_qr_user.ini")
    config.read(config_file, encoding="utf-8")
    user_username               = config.get("section_user_data", "username") or "411634"
    user_password               = config.get("section_user_data", "password") or "112211m,"
    user_log_file_save_internal = config.getint("section_delay_time", "log_file_save_internal") or 26

    # 若二维码日志文件不存在，证明secureCRT的日志功能是开启的，上面被关闭了，所以再打开一次
    # 尝试两次，两次后直接关闭进程
    # 延时是为了等待secureCRT创建文件，经测试，时间为1.6秒左右，这里循环user_log_file_save_internal次，每次间隔0.1秒
    # 延迟后没有发现扫码日志文件则判定为日志功能是用户自己开启的，然后当前被关闭了，所以再次开启
    for i in range(0, 3):
        file_exists_flag = False
        for _ in range(0, user_log_file_save_internal):
            time.sleep(0.1)
            if os.path.exists(qr_txt_path):
                file_exists_flag = True
                break

        if file_exists_flag:
            break
        elif 2 == i and not file_exists_flag:
            resource_release(tmp_pre, 1)
        else:
            qr_log_open(qr_txt_path)

    get_qr_info(user_username)

    qr_url = qr_string_to_url(tmp_pre, qr_txt_path)
    if not qr_url:
        for _ in range(0, 4):
            if qr_txt_check(qr_txt_path):
                qr_url = qr_string_to_url(tmp_pre, qr_txt_path)
                if qr_url:
                    break
        else:
            resource_release(tmp_pre, 1)
    qr_url = qr_url.replace("\n", "")

    check_code = checkurl_checkcode(qr_url, user_password)
    if not check_code:
        pyautogui.write("Nothing in this qrcode")
        pyautogui.press("enter")
        resource_release(tmp_pre, 1)

    pyautogui.write(check_code)
    pyautogui.press("enter")

    resource_release(tmp_pre, 0)
