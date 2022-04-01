# -*- coding:utf-8 -*-

from wtEXAFS import mainWindow
from wtEXAFS import path

# --------------------- 主程序 ---------------------
if __name__ == "__main__":
    # --------- 实例化主窗体类 ---------
    mainWindow.MainWindow()
    # --------- 删除临时文件 ---------
    path.deleteTempFiles()
