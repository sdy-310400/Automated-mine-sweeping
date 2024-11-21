如何使用？

一、arbiter官网下载Minesweeper Arbiter版本扫雷游戏，解压，找到其主程序ms_arbiter.exe的路径，填入game_path.py的arbiter_path（很重要，要填对）
例如：![image](https://github.com/user-attachments/assets/47fde55c-32a3-4240-bea4-dcc39d9aea6e)

二、
1.运行UI.py有基础ui界面直接使用（行数和列数很重要，一定要填对）
2.main.py有接口Main(row,lin)传入参数为目前扫雷游戏的行格子数和列格子数（很重要，一定要填对）
3.main.py有module_run(_wide, _high, _module)函数可调用，_wide, _high同2中的row,lin，_module为0或其他，分别代表：只尝试一次：尝试多次直到成功
注：以上方法会自动调用game_path.py的arbiter_path打开游戏，也可
<!---
sdy-310400/sdy-310400 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
