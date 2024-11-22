"""作者：@sdy-310400
本模块为程序核心模块1：获取屏幕上的数据的模块"""

import subprocess
from threading import Thread
import win32gui
import pyautogui
import game_path


class CheckerBoard:
    class Data:
        """储存每个格子的数据"""
        def __init__(self, name: str, lo_x: int, lo_y: int, row: int, lin: int, color=None, is_ok=False):
            self.name = name
            self.row = row
            self.lin = lin
            self.lo_x = lo_x
            self.lo_y = lo_y
            self.color = color
            self.ok = is_ok

    class ScanningPic:
        """扫描屏幕的线程 location:屏幕的top，left，wide，height"""
        def __init__(self, location: (int, int, int, int)):
            self.running = True
            self.pic = None

            def get_pic():
                while self.running:
                    self.pic = pyautogui.screenshot(region=location)

            get_pic_thread = Thread(target=get_pic)
            get_pic_thread.start()  # 状态检测开始

    def __init__(self, wide_count, high_count):
        self.running = True
        self.wide_count = wide_count
        self.high_count = high_count

        self.interator = set((i // wide_count, i % wide_count) for i in range(wide_count * high_count))
        self.checkerboard = None
        self.count = 24
        self.scanning_step = 1
        self.clear_data()

        hwnd = win32gui.FindWindow("TMain", "Minesweeper Arbiter ")
        if hwnd == 0:
            subprocess.Popen(game_path.arbiter_path)
        while hwnd == 0:
            hwnd = win32gui.FindWindow("TMain", "Minesweeper Arbiter ")
        #win32gui.SetWindowPos(hwnd, None, 101, 101, 0, 0, win32con.SWP_NOSIZE)
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(hwnd)
        print(self.left, self.top, self.right, self.bottom)
        self.begin = (self.left + 47 - 12, self.top + 175 - 12)
        self.face = (47 - 12 + 100, 175 - 12 - 55)
        self.color_to_type = {
            (0, 0, 255): "1",
            (255, 0, 0): "3",
            (0, 0, 128): "4",
            (128, 0, 0): "5",
            (0, 128, 128): "6"
        }
        self.scanning_pic = self.ScanningPic(
            (int(self.begin[0] - 12), int(self.begin[1]) - 12, 24 * self.wide_count, 24 * self.high_count))

    def clear_data(self):
        self.checkerboard = [
            [CheckerBoard.Data("none", 0, 0, row, lin, None, False)
             for row in range(self.wide_count)]
            for lin in range(self.high_count)]

    def write_data(self, name, lo_x, lo_y, row, lin, color=None, is_ok=False):
        data = self.checkerboard[row][lin]
        data.name = name
        data.lo_x = lo_x
        data.lo_y = lo_y
        data.row = row
        data.lin = lin
        data.color = color
        data.ok = is_ok

    def get_data(self, row, lin):
        """获取数据"""
        return self.checkerboard[row][lin]

    def print_board(self):
        """打印棋盘"""
        print("=====print_board: step-%d=====" % self.scanning_step)
        print("   ", end="")
        for i in range(self.wide_count):
            print("{0: ^5}".format(i), end='')
        print("")
        for i in range(self.wide_count * self.high_count):
            row, lin = (i // self.wide_count, i % self.wide_count)
            if row != 0 and lin == 0:
                print("")
                print("{0: ^3}".format(row), end='')
            elif row == 0 and lin == 0:
                print("{0: ^3}".format(row), end='')
            print("{0: ^5}".format(self.get_data(row, lin).name), end='')
        print("\n=====print_over=====")

    def find_around(self, row: int, lin: int):
        """获取某格子周围的格子
        :param row:
        :param lin:
        return Around_Type"""

        class AroundType:
            none = set()
            sign = set()
            number = set()
            all = set()

        row_list = {row - 1, row, row + 1}
        lin_list = {lin - 1, lin, lin + 1}
        _return = AroundType()
        for row_i in row_list:
            for lin_i in lin_list:
                if row_i < 0 or lin_i < 0:
                    continue
                if (row_i, lin_i) == (row, lin):
                    continue

                try:
                    data = self.get_data(row_i, lin_i)
                    _return.all.add(data)

                    value = data.name
                    if value in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                        _return.number.add(data)
                    elif value == "none":
                        _return.none.add(data)
                    elif value == "sign":
                        _return.sign.add(data)
                except IndexError:
                    continue
        return _return

    def get_type(self, _color, _row, _lin, _x, _y):
        if _color in self.color_to_type:
            return self.color_to_type[_color]

        if _color[1] > 120 and _color[0] <= 100 and _color[2] <= 100:
            return "2"
        self.running = False
        self.scanning_pic.running = False
        print("========游戏失败(color-%s;row-%d,lin-%d)========" % (str(_color), _row, _lin))
        # pyautogui.moveTo(_x, _y)
        return False

    def scanning(self, _super):
        pic = self.scanning_pic.pic
        remove = set()
        for row, lin in self.interator:
            data = self.get_data(row, lin)
            if data.name == "sign":
                continue

            x, y = 12 + lin * self.count, 12 + row * self.count
            color = pic.getpixel((x, y))
            if color == (192, 192, 192):
                test = pic.getpixel((x, y + 10))
                name = "null" if test == (192, 192, 192) else "none"
            else:
                name = self.get_type(color, row, lin, x, y)
                if not isinstance(name, str):
                    _super.running = False
                    return False

            around_none = self.find_around(row, lin).none
            if len(around_none) == 0 and data.name != "none":
                if name != "sign":
                    self.write_data("ok", None, None, row, lin, None, True)

                else:
                    self.write_data("sign", None, None, row, lin, None, True)
                remove.add((row, lin))
                continue

            x = int(self.begin[0] + lin * self.count)
            y = int(self.begin[1] + row * self.count)
            self.write_data(name, x, y, row, lin, color)
        for remove_i in remove:
            self.interator.remove(remove_i)
