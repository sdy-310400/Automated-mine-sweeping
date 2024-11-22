import ctypes
import json
import os
import time
from threading import Thread
from tkinter.messagebox import showerror

import main
import tkinter as tk


class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename

    def write(self, auto_restart, width, height):
        """将设置保存到JSON文件中"""
        settings = {
            'auto_restart': auto_restart,
            'width': width,
            'height': height
        }
        with open(self.filename, 'w') as json_file:
            json.dump(settings, json_file)

    def get(self):
        """从JSON文件中读取设置"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as json_file:
                settings = json.load(json_file)
                return settings['auto_restart'], settings['width'], settings['height']
        else:
            # 如果文件不存在，返回默认值
            return False, 30, 16  # 默认复选框值和宽高值


class GUI:
    def __init__(self):
        self._main = None
        self.running = None
        self.attempts_label = None
        self.duration_label = None
        self.auto_restart_var = None
        self.height_entry = None
        self.width_entry = None
        self.root = tk.Tk()
        self.manager = SettingsManager()  # 创建 SettingsManager 实例
        self.initialize_gui()
        self.initialize_settings()
        self.root.mainloop()

    def initialize_gui(self):
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)  # 调用api获得当前的缩放因子
        self.root.title("自动扫雷程序")
        self.root.tk.call('tk', 'scaling', scale_factor / 75)  # 设置缩放因子
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        label = tk.Label(self.root, text="按下ctrl+e暂停")
        label.pack(pady=10)

        # 创建一个框架用于输入框
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        def on_entry_click(event, enter):
            event.widget.focus_set()
            enter.configure(fg='black')

        # 宽输入框
        width_label = tk.Label(input_frame, text="宽:")
        width_label.pack(side=tk.LEFT, padx=5)
        self.width_entry = tk.Entry(input_frame, width=10, fg="grey")
        self.width_entry.insert(0, "0")
        self.width_entry.bind("<FocusIn>", lambda event: on_entry_click(event, self.width_entry))

        self.width_entry.pack(side=tk.LEFT, padx=5)

        # 高输入框
        height_label = tk.Label(input_frame, text="高:")
        height_label.pack(side=tk.LEFT, padx=5)
        self.height_entry = tk.Entry(input_frame, width=10, fg="grey")
        self.height_entry.pack(side=tk.LEFT, padx=5)
        self.height_entry.insert(0, "0")
        self.height_entry.bind("<FocusIn>", lambda event: on_entry_click(event, self.height_entry))

        # 创建一个框架用于复选框和按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        # 按钮
        start_button = tk.Button(control_frame, text="开始", command=self.start_action)
        start_button.pack(side=tk.RIGHT, padx=5)

        reset_button = tk.Button(control_frame, text="重置", command=self.reset_action)
        reset_button.pack(side=tk.RIGHT, padx=5)

        # 复选框
        self.auto_restart_var = tk.BooleanVar()
        auto_restart_check = tk.Checkbutton(control_frame, variable=self.auto_restart_var)
        auto_restart_check.pack(side=tk.RIGHT, padx=5)  # 复选框在左侧
        auto_restart_label = tk.Label(control_frame, text="自动重试")
        auto_restart_label.pack(side=tk.LEFT)  # 文本在复选框右侧

        # 创建分隔框架
        separator_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        separator_frame.pack(pady=10, padx=10, fill='x')

        # 用时时长展示
        self.duration_label = tk.Label(separator_frame, text="用时时长: 00:00:00")
        self.duration_label.pack(pady=5)

        # 尝试次数展示
        self.attempts_label = tk.Label(separator_frame, text="尝试次数: 0次")
        self.attempts_label.pack(pady=5)

    def start_action(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            showerror("错误", "输入宽高必须是大于0的整数")
            return

        if width > 0 and height > 0:
            time.sleep(1)
            self.running = True

            def game_thread():
                self.step = 0
                if self.auto_restart_var.get() == 0:
                    self._main = main.Main(wide_count=width, high_count=height)
                    self._main.run()
                    self.running = False
                else:
                    while self.running:
                        print("game_thread")
                        self._main = main.Main(wide_count=width, high_count=height)
                        if self._main.run() or self._main.exit:
                            self.running = False
                            break
                        self.step += 1
                        self.attempts_label.configure(text="尝试次数%d" % self.step)

            def time_thread():
                self._time = 0
                while self.running:
                    self.duration_label.configure(text="用时时长: " +
                                                       str(time.strftime("%H:%M:%S", time.gmtime(self._time))))
                    self._time += 1
                    print("time_thread")
                    time.sleep(1)

            thread_1_game = Thread(target=game_thread)
            thread_2_time = Thread(target=time_thread)
            thread_1_game.start()
            thread_2_time.start()
        else:
            showerror("错误", "输入宽高必须是大于0的整数")

    def reset_action(self):
        _main = main.Main(0, 0)
        _main.new_game()
        _main.manual_end()
        self.running = False
        self.attempts_label.configure(text="尝试次数0")
        self.duration_label.configure(text="用时时长: 00:00:00")

    def on_closing(self):
        self.manager.write(self.auto_restart_var.get(), self.width_entry.get(), self.height_entry.get())
        self.running = False
        try:
            self._main.manual_end()
        except AttributeError:
            pass
        self.root.destroy()

    def initialize_settings(self):
        auto_restart, width, height = self.manager.get()  # 获取设置
        # 设置窗口的宽度和高度
        self.width_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.width_entry.insert(0, width)
        self.height_entry.insert(0, height)
        # 创建复选框，设置初始值
        self.auto_restart_var.set(auto_restart)


if __name__ == '__main__':
    gui = GUI()
