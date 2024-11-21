有言在前：本项目基于视觉识别，相当于机器代替人由于扫雷游戏的特性，并不能保证每次游戏都能成功（所以我写了自动重试），成功概率与人相同，但是速度比人快

如何使用？

一、arbiter官网下载Minesweeper Arbiter版本扫雷游戏，解压，找到其主程序ms_arbiter.exe的路径，填入game_path.py的arbiter_path（很重要，要填对）
例如：![image](https://github.com/user-attachments/assets/47fde55c-32a3-4240-bea4-dcc39d9aea6e)

二、
1.运行UI.py有基础ui界面直接使用（行数和列数很重要，一定要填对）

![image](https://github.com/user-attachments/assets/4a5a0cb5-16f4-4396-9e3d-5a791de8ff9b)


2.main.py有接口Main(row,lin)传入参数为目前扫雷游戏的行格子数和列格子数（很重要，一定要填对）


3.main.py有module_run(_wide, _high, _module)函数可调用，_wide, _high同2中的row,lin，_module为0或其他，分别代表：只尝试一次：尝试多次直到成功

注：以上方法会自动调用game_path.py的arbiter_path打开游戏，也可自行打开

三、注意事项

1.在运行时要保证游戏窗口不被其他窗口阻挡

2.在运行过程中会获取鼠标的操作权限，你仍可以使用鼠标，但是不建议，可能会点到其他地方。在运行过程中可以按下ctrl+e或者把鼠标移动到屏幕右上角以终止程序
<!---
sdy-310400/sdy-310400 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
