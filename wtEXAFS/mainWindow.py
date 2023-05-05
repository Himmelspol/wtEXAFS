# -*- coding:utf-8 -*-

import numpy as np
import os
import tkinter  # 导入相关窗体模块
import tkinter.messagebox
from shutil import copy
from tkinter.ttk import Notebook

# ------------ 自定义模块 ------------
from wtEXAFS import fileOper, para, path, showData, subWindow, tools


# ------------ 主窗体类 ------------
class MainWindow:
    # A window that guide users to make wavelet transformation of normalized EXAFS data step by step.

    # --------- 构造方法里面进行窗体的控制 ---------
    def __init__(self):
        LOGO_PATH = path.getResourcePath(os.path.join("resources", "logo.ico"))  # LOGO的文件路径
        path.deleteTempFiles()
        self.root = tkinter.Tk()  # 创建一个窗体
        self.root.title("wtEXAFS")  # 设置标题
        self.root.iconbitmap(LOGO_PATH)  # 设置LOGO资源
        self.root.geometry("480x480+500+100")  # 设置初始化窗体尺寸
        self.root.resizable(False, False)  # 锁定窗体尺寸
        self.root["background"] = "LightGray"  # 设置背景颜色
        # --------------------- 设置menu ---------------------
        self.createMenu()
        # --------------------- 设置frame ---------------------
        self.root_frame = tkinter.Frame(self.root, width=480, bg="#897956")
        self.root_frame.pack(fill="x", side="top")
        # --------------------- 主窗体模块导入（导入时处于未响应状态） ---------------------
        self.showDataMoudle()
        self.showMotherWaveletMoudle()
        self.WaveletTransMoudle()
        # --------------------- 窗体关闭事件 ---------------------
        self.root.protocol("WM_DELETE_WINDOW", self.closeHandle)
        # --------------------- 窗口显示 ---------------------
        self.root.mainloop()

    # --------- 菜单的创建与布局 ---------
    def createMenu(self):
        self.menu = tkinter.Menu(self.root)  # 创建菜单组件
        # --------------------- 添加menu中的Single File及其子菜单 ---------------------
        self.singleFile_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=" Singel File ", menu=self.singleFile_menu)
        self.singleFile_menu.add_command(label="Open k-space EXAFS data", command=self.openData)
        self.singleFile_menu.add_command(label="Open k-space model EXAFS data", command=self.openModelData)
        self.singleFile_menu.add_separator()
        self.singleFile_menu.add_command(label="Open mother wavelet config", command=self.reflashParaconfig,
                                         state="disabled")
        self.singleFile_menu.add_command(label="Save mother wavelet config", command=self.saveParaconfig,
                                         state="disabled")
        self.singleFile_menu.add_separator()
        self.singleFile_menu.add_command(label="Save Wavelet Transformation result as txt",
                                         command=self.saveWaveletResult, state="disabled")
        # --------------------- 添加menu中的Mutiple File及其子菜单 ---------------------
        self.multipleFile_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=" Multiple Column Import ", menu=self.multipleFile_menu)
        self.multipleFile_menu.add_command(label="Open multiple column chi(k) data Set (ATHENA file)",
                                           command=self.openMultipleColumn)
        # --------------------- 添加menu中的Help及其子菜单 ---------------------
        self.Help_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=" Help ", menu=self.Help_menu)
        self.Help_menu.add_command(label="Tips", command=self.helpTips)
        self.Help_menu.add_command(label="About", command=self.helpAbout)
        # --------------------- 添加menu中的Quit及其子菜单 ---------------------
        self.Quit_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label=" Quit ", command=self.closeHandle)  # 退出程序
        # --------------------- 构建菜单 ---------------------
        self.root.config(menu=self.menu)

    # --------- 主窗口中数据载入模块的布局 ---------
    def showDataMoudle(self):
        # --------- 在主窗口建立frame ---------
        self.root_dataFrame = tkinter.Frame(self.root_frame, width=480, height=160,
                                            relief="sunken", borderwidth=2)
        self.root_dataFrame.pack(fill="x", side="top")
        self.data_name = tkinter.Frame(self.root_dataFrame, width=480, height=40)
        self.data_name.pack(fill="x", side="top")
        self.data_kWeight = tkinter.Frame(self.root_dataFrame, width=480, height=40)
        self.data_kWeight.pack(fill="x", side="top")
        self.data_buttonA1 = tkinter.Frame(self.root_dataFrame, width=480, height=40, )
        self.data_buttonA1.pack(fill="x", side="top")
        self.data_buttonA2 = tkinter.Frame(self.root_dataFrame, width=480, height=40)
        self.data_buttonA2.pack(fill="x", side="top")
        # --------- Data Name的显示 ---------
        para.Parameters.file_name = tkinter.StringVar()
        self.name_label = tkinter.Label(self.data_name, text="File name:", font=("Calibri", 11))
        self.name_box = tkinter.Entry(self.data_name, textvariable=para.Parameters.file_name, justify="left",
                                      width=50, font=("Calibri", 11), state="disabled", bg="white")
        self.name_label.pack(side="left", padx=5, pady=5)
        self.name_box.pack(side="left", pady=5)
        # --------- k weight的选择 ---------
        self.kWeight = [("0", 0), ("1", 1), ("2", 2), ("3", 3)]
        self.kWeight_var = tkinter.IntVar()
        self.kWeight_label = tkinter.Label(self.data_kWeight, text="k-weight:", font=("Calibri", 11))
        self.kWeight_label.grid(column=0, row=0, padx=10)
        for text, num in self.kWeight:
            self.kWeight_radio = tkinter.Radiobutton(self.data_kWeight, variable=self.kWeight_var,
                                                     text=text, value=num, font=("Calibri", 11))
            self.kWeight_radio.grid(column=num + 1, row=0, padx=5)
        # --------- buttonA1组件（accept/show/next） ---------
        self.buttonA1_accept = tkinter.Button(self.data_buttonA1, text="Accept k-weight", state="disabled", width=15,
                                              font=("Calibri", 11), command=lambda: kWeightAccept())
        self.buttonA1_show = tkinter.Button(self.data_buttonA1, text="Show k-weighted data", state="disabled", width=18,
                                            font=("Calibri", 11), command=lambda: showData.showKWeighted())
        self.buttonA1_next = tkinter.Button(self.data_buttonA1, text="Next step", state="disabled", width=12,
                                            font=("Calibri", 11), command=lambda: nextStepForMW())
        self.buttonA1_accept.grid(column=0, row=0, padx=15, pady=5)
        self.buttonA1_show.grid(column=1, row=0, padx=15, pady=5)
        self.buttonA1_next.grid(column=2, row=0, padx=15, pady=5)
        # --------- buttonA2组件（open/replace） ---------
        self.buttonA2_open = tkinter.Button(self.data_buttonA2, text="Open k-space data",
                                            state="normal", command=self.openData,
                                            font=("Calibri", 11), width=20)
        self.buttonA2_replace = tkinter.Button(self.data_buttonA2, text="Replace k-space data",
                                               state="disabled", command=self.openData,
                                               font=("Calibri", 11), width=20)
        self.buttonA2_open.pack(side="left", expand=1, padx=5, pady=8)
        self.buttonA2_replace.pack(side="right", expand=1, padx=5, pady=8)

        # --------- 本模块按钮组方法定义（buttonA1) ---------
        # --------- k Weight数据接收与文件刷新 ---------
        def kWeightAccept():
            if os.path.exists(path.TempPath.get("k")):
                print("3. k-weight value accepted!")
                fileOper.createkWData(self.kWeight_var.get())
                self.bottonSet("kWeightAccept")
            else:
                tools.messagesOrError("data import failed")
                self.buttonA1_accept.config(state="disabled")
                self.buttonA2_open.config(state="normal")
                self.buttonA2_replace.config(state="disabled")

        # --------- 进入小波配置的下一步 ---------
        def nextStepForMW():
            # --------- 读取kW文件中的默认参数 ---------
            kW_path = path.TempPath.get('kW')
            para.Parameters.kmin = tools.colFirstLastInter(kW_path)[0]
            para.Parameters.kmax = tools.colFirstLastInter(kW_path)[1]
            para.Parameters.dk = tools.colFirstLastInter(kW_path)[2]
            para.Parameters.dR = round(np.pi / (2 * (20 + (para.Parameters.kmax - para.Parameters.kmin))), 3) + 0.001
            # Nyquist frequency according to k-range, dR = pi/(2*k-range)
            para.Parameters.bmin = para.Parameters.kmin
            para.Parameters.bmax = para.Parameters.kmax
            para.Parameters.db = para.Parameters.dk
            # --------- 刷新参数 ---------
            self.showPara()
            # --------- 按钮组的响应 - --------
            self.bottonSet("nextStepForMW")
            print("4. Now you can type in parameters!")

    # --------- 主窗口中母小波构建模块的布局 ---------
    def showMotherWaveletMoudle(self):
        # --------- 包装后面用到的检测浮点数的函数 ---------
        testfloat = self.root_frame.register(tools.testFloat)
        # --------- 需要获得的参数 ---------
        self.kmin = tkinter.DoubleVar()
        self.kmax = tkinter.DoubleVar()
        self.dk = tkinter.DoubleVar()
        self.Rmin = tkinter.DoubleVar()
        self.Rmax = tkinter.DoubleVar()
        self.dR = tkinter.DoubleVar()
        self.sigma = tkinter.DoubleVar()
        self.eta = tkinter.DoubleVar()
        self.n = tkinter.DoubleVar()
        # --------- 在主窗口建立frame ---------
        self.root_motherWaveletFrame = tkinter.Frame(self.root_frame, width=480, height=200,
                                                     relief="sunken", borderwidth=2)
        self.root_motherWaveletFrame.pack(fill="both", side="top")
        # --------- 小波frame的建立 ---------
        self.entry = tkinter.Frame(self.root_motherWaveletFrame, width=320, height=140,
                                   relief="sunken", borderwidth=2)
        self.entry.pack(side="left", padx=1, pady=1)
        self.bottonB = tkinter.Frame(self.root_motherWaveletFrame, width=160, height=200,
                                     relief="sunken", borderwidth=2)
        self.bottonB.pack(side="right", padx=2, pady=2)
        self.k_user = tkinter.Frame(self.entry, width=320, height=45)
        self.k_user.pack(fill="x", side="top")
        self.R_user = tkinter.Frame(self.entry, width=320, height=45)
        self.R_user.pack(fill="x", side="top")
        # --------- 小波选项卡的建立 ---------
        self.mother_wavelet_choice = Notebook(self.entry)
        self.morlet_choice = tkinter.Frame(self.mother_wavelet_choice, width=320, height=45)
        self.cauchy_choice = tkinter.Frame(self.mother_wavelet_choice, width=320, height=45)
        self.mother_wavelet_choice.add(self.morlet_choice, text="Morlet Wavelet")
        self.mother_wavelet_choice.add(self.cauchy_choice, text="Cauchy Wavelet (in test)")
        self.mother_wavelet_choice.pack(side="top")
        # --------- 小波界面设置（k） ---------
        self.kmin_label = tkinter.Label(self.k_user, text="kmin:", font=("Calibri", 11))
        self.kmin_input = tkinter.Entry(self.k_user, textvariable=self.kmin, width=6,
                                        justify="left", font=("Calibri", 11),
                                        validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.kmax_label = tkinter.Label(self.k_user, text="kmax:", font=("Calibri", 11))
        self.kmax_input = tkinter.Entry(self.k_user, textvariable=self.kmax, width=6,
                                        justify="left", font=("Calibri", 11),
                                        validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.dk_label = tkinter.Label(self.k_user, text="dk:", font=("Calibri", 11))
        self.dk_input = tkinter.Entry(self.k_user, textvariable=self.dk, width=6,
                                      justify="left", font=("Calibri", 11),
                                      validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.kmin_label.grid(column=0, row=0, padx=10, pady=12)
        self.kmin_input.grid(column=1, row=0, pady=12)
        self.kmax_label.grid(column=2, row=0, padx=10, pady=12)
        self.kmax_input.grid(column=3, row=0, pady=12)
        self.dk_label.grid(column=4, row=0, padx=10, pady=12)
        self.dk_input.grid(column=5, row=0, pady=12)
        # --------- 小波界面设置（R） ---------
        self.Rmin_label = tkinter.Label(self.R_user, text="Rmin:", font=("Calibri", 11))
        self.Rmin_input = tkinter.Entry(self.R_user, textvariable=self.Rmin, width=6,
                                        justify="left", font=("Calibri", 11),
                                        validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.Rmax_label = tkinter.Label(self.R_user, text="Rmax:", font=("Calibri", 11))
        self.Rmax_input = tkinter.Entry(self.R_user, textvariable=self.Rmax, width=6,
                                        justify="left", font=("Calibri", 11),
                                        validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.dR_label = tkinter.Label(self.R_user, text="dR:", font=("Calibri", 11))
        self.dR_input = tkinter.Entry(self.R_user, textvariable=self.dR, width=6,
                                      justify="left", font=("Calibri", 11),
                                      validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.Rmin_label.grid(column=0, row=0, padx=10, pady=12)
        self.Rmin_input.grid(column=1, row=0, pady=12)
        self.Rmax_label.grid(column=2, row=0, padx=10, pady=12)
        self.Rmax_input.grid(column=3, row=0, pady=12)
        self.dR_label.grid(column=4, row=0, padx=9, pady=12)
        self.dR_input.grid(column=5, row=0, pady=12)
        # --------- Morlet小波界面设置（sigma/eta） ---------
        self.sigma_label = tkinter.Label(self.morlet_choice, text="Sigma:", font=("Calibri", 11))
        self.sigma_input = tkinter.Entry(self.morlet_choice, textvariable=self.sigma, width=6,
                                         justify="left", font=("Calibri", 11),
                                         validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.eta_label = tkinter.Label(self.morlet_choice, text="Eta:", font=("Calibri", 11))
        self.eta_input = tkinter.Entry(self.morlet_choice, textvariable=self.eta, width=6,
                                       justify="left", font=("Calibri", 11),
                                       validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.get_mPara = tkinter.Button(self.morlet_choice, text="Accept", width=10,
                                        state="disabled", font=("Calibri", 10), command=lambda: acceptMW("morlet"))
        self.sigma_label.pack(side="left", padx=10, pady=8)
        self.sigma_input.pack(side="left", pady=8)
        self.eta_label.pack(side="left", padx=10, pady=8)
        self.eta_input.pack(side="left", pady=8)
        self.get_mPara.pack(side="right", padx=10, pady=5)
        # --------- Cauthy小波界面设置（n） ---------
        self.n_label = tkinter.Label(self.cauchy_choice, text="n order:", font=("Calibri", 11))
        self.n_input = tkinter.Entry(self.cauchy_choice, textvariable=self.n, width=6,
                                     justify="left", font=("Calibri", 11),
                                     validate="key", vcmd=(testfloat, '%P', '%v', '%W'))
        self.get_cPara = tkinter.Button(self.cauchy_choice, text="Accept", width=10,
                                        state="disabled", font=("Calibri", 10), command=lambda: acceptMW("cauchy"))
        self.n_label.pack(side="left", padx=10, pady=8)
        self.n_input.pack(side="left", pady=8)
        self.get_cPara.pack(side="right", padx=10, pady=5)
        # --------- 按钮组布局 ---------
        self.openMW_config = tkinter.Button(self.bottonB, text="Open config", width=15,
                                            state="disabled", font=("Calibri", 11),
                                            command=self.reflashParaconfig)
        self.saveMW_config = tkinter.Button(self.bottonB, text="Save config", width=15,
                                            state="disabled", font=("Calibri", 11),
                                            command=self.saveParaconfig)
        self.showkR = tkinter.Button(self.bottonB, text="Show k & R", width=15,
                                     state="disabled", font=("Calibri", 11),
                                     command=lambda: showData.showKR())
        self.showMW = tkinter.Button(self.bottonB, text="Show wavelet", width=15,
                                     state="disabled", font=("Calibri", 11),
                                     command=lambda: showData.showMotherWavelet())
        self.openMW_config.pack(side="top", padx=10, pady=5)
        self.saveMW_config.pack(side="top", padx=10, pady=5)
        self.showkR.pack(side="top", padx=10, pady=5)
        self.showMW.pack(side="top", padx=10, pady=5)

        # --------- 小波配置的接受与临时保存 ---------
        def acceptMW(type_name: str):
            kmin = self.kmin.get()
            kmax = self.kmax.get()
            deltak = self.dk.get()
            rmin = self.Rmin.get()
            rmax = self.Rmax.get()
            # deltar = round(np.pi / (2 * (20 + (kmax - kmin))), 3) + 0.001
            deltar = self.dR.get()
            sigma = self.sigma.get()
            eta = self.eta.get()
            norder = self.n.get()
            # --------- 判断输入是否合理 ---------
            if tools.testKRInput(kmin, kmax, deltak, rmin, rmax, deltar, sigma, eta, norder):
                print("5. Parameters accepted!")
                # --------- 重新刷新dR ---------
                self.dR_input.config(state="normal")
                self.dR_input.delete(0, "end")
                self.dR_input.insert("end", para.Parameters.dR)
                self.dR_input.config(state="normal")
                # --------- 保存config临时文件 ---------
                fileOper.saveConfig()
                # --------- 创建用户定义的临时数据集 ---------
                fileOper.createkWforWT()
                # --------- 根据用户需求创建小波基 ---------
                fileOper.mwConstruct(type_name)
                # --------- 按钮组状态更新 ---------
                print("6. Wavelet transformation is available!")
                self.bottonSet("acceptMotherW")
                # --------- 弹出窗口 ---------
                tools.messagesOrError("configAccepted")
            else:
                tools.messagesOrError("inputOut")

    # --------- 主窗口中小波变换模块的布局 ---------
    def WaveletTransMoudle(self):
        # --------- 在主窗口空间中建立frame ---------
        self.root_WTFrame = tkinter.Frame(self.root_frame, width=480, height=120,
                                          relief="sunken", borderwidth=2)
        self.root_WTFrame.pack(fill="x", side="top")
        self.wt_process = tkinter.Frame(self.root_WTFrame, width=480, height=40,
                                        relief="sunken", borderwidth=1)
        self.wt_process.pack(fill="x", side="top", padx=5, pady=5)
        self.iwt_process = tkinter.Frame(self.root_WTFrame, width=480, height=40,
                                         relief="sunken", borderwidth=1)
        self.iwt_process.pack(fill="x", side="top", padx=5, pady=5)
        # --------- 小波变换的执行按钮组 ---------
        self.wt_start = tkinter.Button(self.wt_process, text="Start WT",
                                       width=18, state="disabled", font=("Calibri", 10),
                                       command=lambda: wtStart())
        self.wt_show = tkinter.Button(self.wt_process, text="Show WT result", width=18,
                                      state="disabled", font=("Calibri", 10),
                                      command=lambda: showData.showWaveletResult())
        self.wt_save = tkinter.Button(self.wt_process, text="Save WT result",
                                      width=18, state="disabled", font=("Calibri", 10),
                                      command=self.saveWaveletResult)
        self.wt_start.pack(side="left", padx=7, pady=10)
        self.wt_show.pack(side="left", padx=7, pady=10)
        self.wt_save.pack(side="right", padx=7, pady=10)
        # --------- 逆小波变换的执行按钮组 ---------
        self.iwt_start = tkinter.Button(self.iwt_process, text="Start inverse WT (in test)",
                                        width=20, state="disabled", font=("Calibri", 10),
                                        command=lambda: iwtStart())
        self.iwt_show = tkinter.Button(self.iwt_process, text="Show inverse WT result",
                                       width=18, state="disabled", font=("Calibri", 10),
                                       command=lambda: showData.showInverseWaveletResult())
        self.iwt_save = tkinter.Button(self.iwt_process, text="Save inverse WT result",
                                       width=18, state="disabled", font=("Calibri", 10),
                                       command=self.saveInverseWaveletResult)
        self.iwt_start.pack(side="left", padx=7, pady=10)
        self.iwt_show.pack(side="left", padx=7, pady=10)
        self.iwt_save.pack(side="right", padx=7, pady=10)

        # --------- 本模块按钮组方法定义（wt_process/iwt_process) ---------
        # --------- 开始morlet小波变换并创建临时txt文件 ---------
        def wtStart():
            self.wt_start.config(state="disabled")
            fileOper.waveleTransformation()
            tools.messagesOrError("calculationDone")
            # --------- 按钮组更新 ---------
            print("7. Wavelet transformation completed!")
            self.bottonSet("wtStart")

        # --------- 开始小波的逆变换并创建临时txt文件 ---------
        def iwtStart():
            self.iwt_start.config(state="disabled")
            fileOper.inverseWaveleTransformation()
            tools.messagesOrError("calculationDone")
            # --------- 按钮组更新 ---------
            self.bottonSet("iwtStart")
            print("Optional: Inverse wavelet transformation completed.")

    # --------- 按钮组刷新设置 ---------
    def bottonSet(self, note: str):
        if note == "openData":
            self.singleFile_menu.entryconfig("Open mother wavelet config", state="disabled")
            self.buttonA1_show.config(state="disabled")
            self.buttonA1_next.config(state="disabled")
            self.name_box.config(state="normal")
            self.name_box.delete(0, "end")
            self.name_box.insert("end", para.Parameters.file_name)
            self.name_box.config(state="readonly")
            self.buttonA1_accept.config(state="normal")
            self.buttonA2_open.config(state="disabled")
            self.buttonA2_replace.config(state="normal")
            self.singleFile_menu.entryconfig("Save mother wavelet config", state="disabled")
            self.singleFile_menu.entryconfig("Save Wavelet Transformation result as txt", state="disabled")
            self.saveMW_config.config(state="disabled")
            self.showkR.config(state="disabled")
            self.showMW.config(state="disabled")
            self.get_mPara.config(state="disabled")
            self.get_cPara.config(state="disabled")
            self.wt_start.config(state="disabled")
            self.wt_show.config(state="disabled")
            self.wt_save.config(state="disabled")
            self.iwt_start.config(state="disabled")
            self.iwt_show.config(state="disabled")
            self.iwt_save.config(state="disabled")
        elif note == "kWeightAccept":
            self.buttonA1_show.config(state="normal")
            self.buttonA1_next.config(state="normal")
            self.singleFile_menu.entryconfig("Save mother wavelet config", state="disabled")
            self.singleFile_menu.entryconfig("Save Wavelet Transformation result as txt", state="disabled")
            self.saveMW_config.config(state="disabled")
            self.showkR.config(state="disabled")
            self.showMW.config(state="disabled")
            self.get_mPara.config(state="disabled")
            self.get_cPara.config(state="disabled")
            self.wt_start.config(state="disabled")
            self.wt_show.config(state="disabled")
            self.wt_save.config(state="disabled")
            self.iwt_start.config(state="disabled")
            self.iwt_show.config(state="disabled")
            self.iwt_save.config(state="disabled")
        elif note == "nextStepForMW":
            self.buttonA1_next.config(state="disabled")
            self.singleFile_menu.entryconfig("Open k-space EXAFS data", state="disabled")
            self.singleFile_menu.entryconfig("Open k-space model EXAFS data", state="disabled")
            self.singleFile_menu.entryconfig("Open mother wavelet config", state="normal")
            self.multipleFile_menu.entryconfig("Open multiple column chi(k) data Set (ATHENA file)", state="disabled")
            self.buttonA1_accept.config(state="disabled")
            self.buttonA2_replace.config(state="disabled")
            self.get_mPara.config(state="normal")
            self.get_cPara.config(state="normal")
            self.openMW_config.config(state="normal")
        elif note == "acceptMotherW":
            self.singleFile_menu.entryconfig("Open mother wavelet config", state="disabled")
            self.singleFile_menu.entryconfig("Save mother wavelet config", state="normal")
            self.openMW_config.config(state="disabled")
            self.saveMW_config.config(state="normal")
            self.get_mPara.config(state="disabled")
            self.get_cPara.config(state="disabled")
            self.showkR.config(state="normal")
            self.showMW.config(state="normal")
            self.wt_start.config(state="normal")
            self.wt_show.config(state="disabled")
            self.wt_save.config(state="disabled")
            self.iwt_start.config(state="disabled")
            self.iwt_show.config(state="disabled")
            self.iwt_save.config(state="disabled")
        elif note == "wtStart":
            self.singleFile_menu.entryconfig("Open k-space EXAFS data", state="normal")
            self.singleFile_menu.entryconfig("Open k-space model EXAFS data", state="normal")
            self.multipleFile_menu.entryconfig("Open multiple column chi(k) data Set (ATHENA file)", state="normal")
            self.singleFile_menu.entryconfig("Save Wavelet Transformation result as txt", state="normal")
            self.buttonA1_accept.config(state="normal")
            self.buttonA2_replace.config(state="normal")
            self.get_mPara.config(state="normal")
            self.get_cPara.config(state="normal")
            self.wt_show.config(state="normal")
            self.wt_save.config(state="normal")
            self.iwt_start.config(state="normal")
            self.iwt_show.config(state="disabled")
            self.iwt_save.config(state="disabled")
        elif note == "iwtStart":
            self.iwt_show.config(state="normal")
            self.iwt_save.config(state="normal")

    # --------- 主窗口刷新用户配制文件参数 ---------
    def showPara(self):
        # --------- 展示参数 ---------
        self.kmin_input.delete(0, "end")
        self.kmin_input.insert("end", para.Parameters.bmin)
        self.kmax_input.delete(0, "end")
        self.kmax_input.insert("end", para.Parameters.bmax)
        self.dk_input.delete(0, "end")
        self.dk_input.insert("end", para.Parameters.db)
        self.Rmin_input.delete(0, "end")
        self.Rmin_input.insert("end", para.Parameters.Rmin)
        self.Rmax_input.delete(0, "end")
        self.Rmax_input.insert("end", para.Parameters.Rmax)
        self.dR_input.delete(0, "end")
        self.dR_input.insert("end", para.Parameters.dR)
        # self.dR_input.config(state="readonly")
        self.sigma_input.delete(0, "end")
        self.sigma_input.insert("end", para.Parameters.sigma)
        self.eta_input.delete(0, "end")
        self.eta_input.insert("end", para.Parameters.eta)
        self.n_input.delete(0, "end")
        self.n_input.insert("end", para.Parameters.n)

    # --------- 打开数据文件 ---------
    def openData(self):
        PATH = path.getPath("singleData")
        with subWindow.OpenSDataWindow(PATH, "singleData") as file_name:
            para.Parameters.file_name = file_name
            self.bottonSet("openData")

    # --------- 打开预设数据文件 ---------
    def openModelData(self):
        PATH = path.getResourcePath(os.path.join("resources", "model.txt"))
        with subWindow.OpenSDataWindow(PATH, "singleData") as file_name:
            para.Parameters.file_name = file_name
            self.bottonSet("openData")

    # --------- 打开并选择多列数据文件 ---------
    def openMultipleColumn(self):
        PATH = path.getPath("multipleData")
        with subWindow.OpenSDataWindow(PATH, "multipleData") as file_name:
            para.Parameters.file_name = file_name + "_MULTIPLE"
            self.bottonSet("openData")

    # --------- 打开parameter配置文件并刷新输入框 ---------
    def reflashParaconfig(self):
        para_load = np.loadtxt(path.getPath("config"), comments="#", delimiter=' ', usecols=1)
        # --------- 重新读入参数 ---------
        para.Parameters.bmin = para_load[0]
        para.Parameters.bmax = para_load[1]
        para.Parameters.db = para_load[2]
        para.Parameters.Rmin = para_load[3]
        para.Parameters.Rmax = para_load[4]
        para.Parameters.dR = para_load[5]
        para.Parameters.sigma = para_load[6]
        para.Parameters.eta = para_load[7]
        para.Parameters.n = para_load[8]
        para.Parameters.kmin = para_load[9]
        para.Parameters.kmax = para_load[10]
        para.Parameters.dk = para_load[11]
        # --------- 展示读入的参数 ---------
        self.showPara()
        tools.messagesOrError("config import")

    # --------- 保存parameter配置文件 ---------
    def saveParaconfig(self):
        copy(path.TempPath.get('para_profile'), path.savePath("parameter.txt"))
        print("Note: Save config file.")

    # --------- 保存小波变换结果文件 ---------
    def saveWaveletResult(self):
        copy(path.TempPath.get('WT'), path.savePath("wt_" + para.Parameters.file_name + ".txt"))
        print("Note: Save wavelet transformation results file.")

    # --------- 保存逆小波变换结果文件 ---------
    def saveInverseWaveletResult(self):
        copy(path.TempPath.get('iWT'), path.savePath("iwt_" + para.Parameters.file_name + ".txt"))
        print("Note: Save inverse wavelet transformation results file.")

    # --------- 帮助文件 ---------
    def helpTips(self):
        self.tips = tkinter.Toplevel()
        self.tips.title("Tips for using")
        self.tips.geometry("720x480")
        self.tips_text = tkinter.Text(self.tips, font=("Arial", 10), fg="#000000",
                                      relief="sunken", width=50, )
        self.tips_text.pack(fill="both", expand=1, padx=5, pady=5)
        # --------- tips读入 ---------
        tips = fileOper.loadText(path.getResourcePath(os.path.join("resources", "tips.txt")))
        for line in tips:
            self.tips_text.insert("end", line)
        # --------- 窗口显示 ---------
        self.tips_text.config(state="disabled")

    # --------- 声明 ---------
    def helpAbout(self):
        tools.messagesOrError("about")

    # --------- 窗口关闭操作 ---------
    def closeHandle(self):
        if tkinter.messagebox.askyesnocancel("Close caution", "Do you want to close this window?"):
            # --------- 窗口关闭 ---------
            self.root.destroy()
            showData.closeFig()
