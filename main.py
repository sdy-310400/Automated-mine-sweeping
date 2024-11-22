"""作者：@sdy-310400
本模块为程序核心模块2：逻辑判断与操作模块"""
import keyboard
import take_data
import pyautogui


class Main:
    def __init__(self, wide_count, high_count):
        self.exit = False
        self.number_set = None  # 储存现在需要访问的数字格子
        self.running = True  # 运行控制器
        self.CB = take_data.CheckerBoard(wide_count, high_count)  # 实例化数据获取类

    def fun_1(self):
        """逻辑函数1，用于点击数字格子周围的一个随机格子
        无参
        返回：点击的格子"""
        mine_possibilities = {}
        for data in self.number_set:
            around_data = self.CB.find_around(data.row, data.lin)
            none_count = len(around_data.none)
            sign_count = len(around_data.sign)

            if none_count != 0:
                possibility = (int(data.name) - sign_count) / none_count
            else:
                continue
            for none_i in around_data.none:
                if (none_i.row, none_i.lin) not in mine_possibilities:
                    mine_possibilities.update({(none_i.row, none_i.lin): possibility})
                else:
                    mine_possibilities[(none_i.row, none_i.lin)] += possibility

        d_order = sorted(mine_possibilities.items(), key=lambda x: x[1], reverse=False)

        try:
            dat = d_order[0]
            item = self.CB.get_data(dat[0][0], dat[0][1])
            print("\033[1;35m随机点击 (%d,%d)\033[0m" % (dat[0][0], dat[0][1]))
            pyautogui.click(item.lo_x, item.lo_y)
            return item
        except IndexError:
            pass
        except pyautogui.FailSafeException:
            pass

    def fun_2(self):
        """逻辑函数2，用于计算哪些格子是安全的或者雷
        无参
        返回：[take_data.CheckerBoard.Data](找到可用格子) | [](未找到可用格子)"""
        for number_1 in self.number_set:
            around_number_1 = self.CB.find_around(number_1.row, number_1.lin)
            for number_2 in around_number_1.number:
                if number_2.row == number_1.row or number_2.lin == number_1.lin:
                    around_number_2 = self.CB.find_around(number_2.row, number_2.lin)
                    count_1 = int(number_1.name) - len(around_number_1.sign)
                    count_2 = int(number_2.name) - len(around_number_2.sign)

                    around_number_1_none = set(around_number_1.none)
                    around_number_2_none = set(around_number_2.none)

                    all_in = all(i in around_number_2_none for i in around_number_1_none)
                    chink = {i for i in around_number_2_none if i not in around_number_1_none}

                    if all_in and len(chink) > 0:
                        if count_2 - count_1 == 0:
                            for chinked in chink:
                                print("\033[1;36m计算为sign(%d,%d)\033[0m" % (chinked.row, chinked.lin))
                                pyautogui.click(chinked.lo_x, chinked.lo_y)
                            return chink
                        elif count_2 - count_1 == len(chink):
                            for chinked in chink:
                                print("\033[1;36m计算为safe(%d,%d)\033[0m" % (chinked.row, chinked.lin))
                                self.CB.write_data("sign", chinked.lo_x, chinked.lo_y, chinked.row, chinked.lin)
                            return chink
        return False

    def manual_end(self):
        """结束所有进程
        无参
        无返回"""
        self.running = False
        self.CB.running = False
        self.CB.scanning_pic.running = False
        self.exit = True

    def new_game(self):
        """新建游戏"""
        self.CB.clear_data()
        pyautogui.click(self.CB.left + self.CB.face[0], self.CB.top + 100)

    def run(self):
        keyboard.add_hotkey('ctrl+e', self.manual_end)
        self.new_game()
        try:
            pyautogui.click(self.CB.begin[0], self.CB.begin[1] + 80)
        except pyautogui.FailSafeException:
            pass
        no_number_flag = 0

        while self.running:
            if self.CB.scanning(self):
                return False
            self.CB.print_board()
            have_chink = False
            have_none = None
            self.number_set = set()
            safe_set = set()

            for row, lin in self.CB.interator:
                data = self.CB.get_data(row, lin)
                if data.ok:
                    continue
                elif data.name == "none":
                    have_none = data
                    continue

                if data.name in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                    self.number_set.add(data)
                    around_none_list = self.CB.find_around(row, lin).none
                    around_sign_list = self.CB.find_around(row, lin).sign

                    if len(around_sign_list) == int(data.name) and len(around_none_list) != 0:
                        for around_none in around_none_list:
                            have_chink = True
                            if around_none not in safe_set:
                                print("\033[1;32m标记为safe(%d,%d)\033[0m" % (around_none.row, around_none.lin))
                                safe_set.add(around_none)
                    elif len(around_none_list) + len(around_sign_list) == int(data.name):
                        for around_none in around_none_list:
                            have_chink = True
                            print("\033[1;31m标记为sign(%d,%d)\033[0m" % (around_none.row, around_none.lin))
                            self.CB.write_data("sign", around_none.lo_x, around_none.lo_y,
                                               around_none.row, around_none.lin)

            if not self.number_set:
                no_number_flag += 1

            try:
                if no_number_flag == 3:
                    if have_none is not None:
                        pyautogui.click(have_none.lo_x, have_none.lo_y)
                    print("========游戏成功=========")
                    self.manual_end()
                    return True

                for safe_item in safe_set:
                    pyautogui.click(safe_item.lo_x, safe_item.lo_y)
            except pyautogui.FailSafeException:
                self.manual_end()
                return True

            if not have_chink:
                if not self.fun_2():
                    self.fun_1()

            self.CB.scanning_step += 1


def module_run(_wide, _high, _module):
    if _module == 0:
        _main = Main(wide_count=_wide, high_count=_high)
        _main.run()
    else:
        while True:
            _main = Main(wide_count=_wide, high_count=_high)
            if _main.run():
                break
            if _main.exit:
                break


if __name__ == '__main__':
    module_run(30, 16, 1)
