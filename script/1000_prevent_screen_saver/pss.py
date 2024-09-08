'''
Author: 胡益华

Creation Date: 2024-08-25

Updated Date: 2024-08-25

Usage: python pss.py

Description:
(1) 企业计算机设置为自动睡眠，且不可显示设置取消，那么运行此脚本，电脑将不再自动睡眠
(2) 若需要终止该脚本，打开任务管理器，结束 pss 进程即可

Notice:
(1) 脚本仅支持 Windows 上运行
'''

import ctypes
import time

def prevent_screen_saver():
    while True:
        # 防止息屏
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        time.sleep(35)

if __name__ == "__main__":
    prevent_screen_saver()
