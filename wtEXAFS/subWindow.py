# -*- coding:utf-8 -*-

import re
import tkinter

import numpy as np

from wtEXAFS import fileOper, path, showData, tools


# ------------ 次窗体类（文件打开窗口） ------------
class OpenSDataWindow:
    """
    Open a window to import single normalized k-space EXAFS data
    Open_type = 1: single file open mode
    Open_type = 2: multiple column open mode
    """

    # --------- 构造方法里面进行窗体的控制 ---------
    def __init__(self, path_name, open_type: str):
        path.deleteTempFiles()  # 首先删除所有临时文件
        self.data_show = tkinter.Toplevel()
        self.data_show.title("Column selection")
        self.data_show.geometry("700x300")
        self.data_show.resizable(False, False)
        # --------- 加载数据导入模块 ---------
        self.path_name = fileOper.getFileName(path_name)
        self.dataLoadModule(path_name, open_type)

    def __enter__(self):
        return self.path_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    # --------- 数据导入模块 ---------
    def dataLoadModule(self, path_name: str, open_type: str):
        # --------- 包装后面用到的检测正整数的函数 ---------
        testint = self.data_show.register(tools.testInt)
        if open_type == "multipleData":
            testint2 = self.data_show.register(tools.testMulInt)
        else:
            testint2 = self.data_show.register(tools.testInt)
        # --------- 读入txt文件并储存 ---------
        data_content = fileOper.loadText(path_name)
        # --------- 构建frame ---------
        self.load_frame = tkinter.Frame(self.data_show)
        self.load_frame.pack(side="left")
        self.show_frame = tkinter.Frame(self.data_show)
        self.show_frame.pack(side="left")
        self.input_frame1 = tkinter.Frame(self.load_frame)
        self.input_frame2 = tkinter.Frame(self.load_frame)
        self.botton_frame = tkinter.Frame(self.load_frame)
        # --------- 定义本模块中获取的变量 ---------
        self.rowStart = tkinter.StringVar()
        self.kValue = tkinter.StringVar()
        self.chikValue = tkinter.StringVar()
        # --------- 数据导入模块Entry ---------
        self.rowStart_label = tkinter.Label(self.input_frame1, text="Data start from row: ",
                                            height=2, font=("Calibri", 11))
        self.rowStart_entry = tkinter.Entry(self.input_frame1, width=5, font=("Calibri", 11),
                                            textvariable=self.rowStart,
                                            validate="key", vcmd=(testint, '%P', '%v', '%W'))
        self.kValue_label = tkinter.Label(self.input_frame1, text="k value at column: ",
                                          height=2, font=("Calibri", 11))
        self.kValue_entry = tkinter.Entry(self.input_frame1, width=5, font=("Calibri", 11),
                                          textvariable=self.kValue,
                                          validate="key", vcmd=(testint, '%P', '%v', '%W'))
        self.chikValue_label = tkinter.Label(self.input_frame2, text="chik value at column: ",
                                             height=2, font=("Calibri", 11))
        self.chikValue_entry = tkinter.Entry(self.input_frame2, width=25, font=("Calibri", 11),
                                             textvariable=self.chikValue,
                                             validate="key", vcmd=(testint2, '%P', '%v', '%W'))
        # --------- 初始化数据框输入 ---------
        self.rowStart_entry.delete(0, "end")
        self.rowStart_entry.insert("end", "1")
        self.kValue_entry.delete(0, "end")
        self.kValue_entry.insert("end", "1")
        self.chikValue_entry.delete(0, "end")
        self.chikValue_entry.insert("end", "2")
        # --------- 操作响应模块Button ---------
        self.showInBox_button = tkinter.Button(self.botton_frame, text="Confirm and show selected data",
                                               font=("Calibri", 10), command=lambda: refreshBox())
        self.putDataToMain_button = tkinter.Button(self.botton_frame, text="Continue and close this window",
                                                   font=("Calibri", 10), state="disabled",
                                                   command=self.data_show.destroy)
        # --------- 数据展示模块Text ---------
        self.yScrolledBar = tkinter.Scrollbar(self.show_frame)
        self.xScrolledBar = tkinter.Scrollbar(self.show_frame, orient="horizontal")
        self.show_scrolledBox = tkinter.Text(self.show_frame, font=("Times New Roman", 8),
                                             relief="sunken", wrap="none",
                                             yscrollcommand=self.yScrolledBar.set,
                                             xscrollcommand=self.xScrolledBar.set)
        # --------- 布局数据导入框 ---------
        self.input_frame1.pack(side="top")
        self.input_frame2.pack(side="top")
        self.botton_frame.pack(side="bottom")
        self.rowStart_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.rowStart_entry.grid(column=1, row=0, sticky="w")
        self.kValue_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.kValue_entry.grid(column=1, row=1, sticky="w")
        self.chikValue_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.chikValue_entry.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.showInBox_button.grid(column=0, row=0, padx=20, pady=12)
        self.putDataToMain_button.grid(column=0, row=1, padx=20, pady=12)
        self.xScrolledBar.pack(fill="x", expand=1, side="bottom")
        self.yScrolledBar.pack(fill="y", expand=1, side="right")
        self.show_scrolledBox.pack(fill="both", padx=10, pady=10)
        # --------- 滑动条与数据显示框关联 ---------
        self.yScrolledBar.config(command=self.show_scrolledBox.yview)
        self.xScrolledBar.config(command=self.show_scrolledBox.xview)
        # --------- 数据展示事件 ---------
        showData.showTextInBox(self, data_content)

        # --------- 根据输入刷新显示模块 ---------
        def refreshBox():
            col_num = map(int, re.findall(r'\d+', self.chikValue.get()))  # 提取输入中所有的数字
            col_num = list(sorted(set(filter(lambda x: True if x > 0 else False, col_num))))  # 剔除0和重复数字并升序
            # --------- 判断是否输入了超过文件行列数的数值 ---------
            row_limit = len(data_content)
            column_limit = np.loadtxt(path_name, skiprows=0).shape[1]
            if self.rowStart.get() == "" or self.kValue.get() == "" or self.chikValue.get() == "":
                tools.messagesOrError("selectionOut")
            elif int(self.rowStart.get()) > row_limit:
                tools.messagesOrError("selectionOut")
            elif int(self.kValue.get()) > column_limit or col_num[-1] > column_limit:
                tools.messagesOrError("selectionOut")
            else:
                fileOper.createPolishedData(path_name, self.rowStart.get(), self.kValue.get(), col_num)
                showData.showTextInBox(self, fileOper.loadText(path.TempPath.get('k')))
                np.savetxt(path.TempPath.get('col_selection'), col_num, fmt='%d', delimiter=" ")
                self.putDataToMain_button.config(state="normal")
                print("1. Column selection success!")
                print("2. Data import success!")
