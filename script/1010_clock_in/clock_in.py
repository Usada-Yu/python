'''
Author: 胡益华

Creation Date: 2024-08-26

Updated Date: 2024-08-26

Usage: python clock_in.py

Description:
(1) 此脚本运行后会打开一个窗口，用于定时挪动鼠标到相应的坐标位置并点击一次
(2) 点击 `Get Mouse Position` 按钮，在2秒内将鼠标移动到需要点击的位置，窗口会显示鼠标坐标
(3) 将鼠标的坐标填入 `X coordinate` 和 `Y coordinate` 中(负数坐标同样支持，如双屏幕时 x 坐标可能为负)
(4) 在 `Time` 栏中，设置需要挪动鼠标的时间，时间以24小时制
    格式样例：08:58 20:43
(4) 点击 `Confirm` 按钮启动即可
(5) 若需要更改时间或坐标，直接更改即可，无需重复点击 `Confirm`；
    不过需要更改的话建议优先点击 `Cancel` 按钮，重新配置后再次点击 `Confirm`；
    重复点击 `Confirm` 无实际效果

Notice:
(1) 脚本仅支持 Windows 上运行
(2) 脚本仅支持配置24小时制，故脚本仅一天内有作用
'''

import pyautogui
import time
import threading
import tkinter as tk

class MouseMover:
    def __init__(self, window):
        self.thread_state       = False
        self.thread_stop_flag   = False

        self.window = window
        self.window.title("Clock In")
        self.window.geometry("500x480")
        self.window.resizable(width=False, height=False)

        self.get_position_button = tk.Button(window, text="Get Mouse Position", command=self.get_mouse_position)
        self.get_position_button.pack(pady=10)

        self.position_label = tk.Label(window)
        self.position_label.pack()

        self.x_label = tk.Label(window, text="X coordinate")
        self.x_label.pack()
        self.x_entry = tk.Entry(window)
        self.x_entry.pack()

        self.y_label = tk.Label(window, text="Y coordinate")
        self.y_label.pack()
        self.y_entry = tk.Entry(window)
        self.y_entry.pack()

        self.time_label = tk.Label(window, text="Time (24-hour ex. 08:00)")
        self.time_label.pack()
        self.time_entry = tk.Entry(window)
        self.time_entry.pack()

        self.confirm_button = tk.Button(window, text="Confirm", command=self.timer_start)
        self.confirm_button.pack(pady=10)

        self.timer_label = tk.Label(window)
        self.timer_label.pack()

        self.cancel_button = tk.Button(window, text="Cancel", command=self.timer_cancel)
        self.cancel_button.pack(pady=10)

    def get_mouse_position(self):
        mouse_x, mouse_y = pyautogui.position()
        self.position_label.config(text=f"Current mouse coordinates: ({mouse_x}, {mouse_y})", fg="green")

    def move_mouse_to_position(self):
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def check_time(self):
        self.thread_stop_flag = False

        while True:
            if self.thread_stop_flag:
                break

            current_time = time.strftime("%H:%M")
            if current_time == self.time_entry.get():
                self.move_mouse_to_position()
                break
            time.sleep(1)

        self.thread_state = False

    def timer_start(self):
        if not self.thread_state:
            self.thread_state   = True
            self.timer_thread   = threading.Thread(target=self.check_time)
            self.timer_thread.start()
        else:
            self.timer_label.config(text="Please click the cancel button first", fg="red")
            self.timer_label.after(800, lambda: self.timer_label.config(text="", fg="black"))

    def timer_cancel(self):
        if self.thread_state:
            self.thread_stop_flag = True

if __name__ == "__main__":
    window  = tk.Tk()
    app     = MouseMover(window)
    window.mainloop()
