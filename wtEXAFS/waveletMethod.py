# -*- coding:utf-8 -*-
# Construct wavelet and wavelet transformation

import numpy as np
from cmath import exp
from cmath import log
from cmath import sqrt
from math import pi


def energyCoef(r: float, omega: float):
    energy_normalized = (2 * r / omega) ** 0.5  # 引入能量归一化参数
    return energy_normalized


def morletC(r: float, b: float, sigma: float, eta: float, k_value: float):
    i = complex(0, 1)
    t = 2 * r * (k_value - b) / eta
    C = 1.0 / (sqrt(2.0 * pi) * sigma)
    morleti = C * exp(i * eta * t) * exp(-(t * t) / (2.0 * sigma * sigma))
    return morleti


def cauchyC(r: float, b: float, n: float, k_value: float):
    i = complex(0, 1)
    t = 2 * r * (k_value - b) / n
    cauchyi = pow(exp(log(i / (i + t))), (n + 1))
    return cauchyi


def cWT(wavelet, chi, energy_coef, dk: float):
    """
    将chi序列与小波基中的每一行（代表不同尺度的小波，r越大，小波的频率越高）进行卷积运算
    :param wavelet: r行（根据用户输入的Rmin / Rmax / dR）k+列的小波基
    :param chi: 经过一维线性插值的chi序列，间距为dk
    :param dk: 数据间隔
    :param energy_coef: 能量的归一化常数
    :return: 一维的小波变换结果，先是k变化，然后是r变化
    """
    w_abs = np.array([])
    w_complex = np.array([])
    row_limit = len(wavelet)
    for i in range(row_limit):
        psi = np.array(wavelet[i])
        wt = np.convolve(chi, psi, "same") * dk * energy_coef[i]
        w_abs = np.append(w_abs, abs(wt))
        w_complex = np.append(w_complex, wt)
    return w_abs, w_complex


def iWT(w_matrix, energy_coef, wavelet_coef, dr):
    # 目前仍不清楚为什么这个算法能生效，这个算法与实际公式并不一致
    row_limit = len(w_matrix)
    for i in range(row_limit):
        '''
        w_matrix[i] = 4 * w_matrix[i] * dr / energy_coef[i]
        '''
        w_matrix[i] = w_matrix[i] / energy_coef[i]
    iw = np.sum((w_matrix / wavelet_coef), axis=0).real
    return iw


def fftWavelet(wavelet, k_list):
    wavelet = np.array(wavelet).real
    '''
    fft_amp = abs(np.fft.fft(wavelet))
    fft_freq = np.fft.fftfreq(len(wavelet), d=(k_list[1] - k_list[0]) / (2 * pi))
    wavelet_coef = np.trapz(fft_amp, dx=(fft_freq[1] - fft_freq[0])) * (k_list[1] - k_list[0])
    return fft_freq, fft_amp, wavelet_coef
    '''
    chiR = fft(wavelet, k_list)[1]
    wavelet_coef = 2 * np.sqrt(np.pi) * np.trapz(chiR)
    return wavelet_coef


def windowFunction(k_list, up, down, halfw):
    k_len = len(k_list)
    delta_k = k_list[1] - k_list[0]
    # 定义上升或下降区间的数据个数
    halfw_count = int(halfw / delta_k)
    halfw_range = np.arange(2 * halfw_count + 1)
    # 获得上升和下降区间的中心值索引
    up_index = int((up - k_list[0]) / delta_k)
    down_index = int((down - k_list[0]) / delta_k)
    # 获得上升和下降区间的窗函数
    window = np.kaiser(len(halfw_range) * 2 - 1, 8)
    # 索引锚点，共四个
    anchor_a = up_index - halfw_count
    anchor_b = up_index + halfw_count + 1
    anchor_c = down_index - halfw_count
    anchor_d = down_index + halfw_count + 1
    # 上升前空间索引序列
    region_a = np.arange(0, anchor_a)
    # 上升空间索引序列
    refion_b = np.arange(anchor_a, anchor_b)
    # 恒定空间索引序列
    refion_c = np.arange(anchor_b, anchor_c)
    # 下降区间索引序列
    region_d = np.arange(anchor_c, anchor_d)
    # 合并所有区间
    window_final = []
    adp = window_final.append
    j = 0
    for i in np.arange(k_len):
        if i in region_a:
            adp(0.0)
        elif i in refion_b:
            adp(window[j])
            j += 1
        elif i in refion_c:
            adp(1.0)
        elif i in region_d:
            adp(window[j])
            j -= 1
        else:
            adp(0.0)
    return window_final


def waveFunction(omega):
    i = complex(0, 1)
    wave_func = exp(i * omega)
    return wave_func


def fft(wave, k_list):
    # 根据k序列的间隔和长度构建r序列，注意在EXAFS中，omega(k)=2*k*(R + phase_shift)，对于k的实际频率为2R，但为了方便傅里叶变换后只显示为R，
    k_range = k_list[-1] - k_list[0]
    delta_k = k_list[1] - k_list[0]
    r_range = np.pi / (2 * delta_k)
    delta_r = np.pi / k_range
    r_list = np.arange(0, r_range, delta_r)
    # 构建用于傅里叶变换的核
    coef_energy = delta_k / np.sqrt(np.pi)
    base = np.array([[waveFunction(2 * k * r) for k in k_list] for r in r_list])
    # 傅里叶变换
    fft_result = []
    adp = fft_result.append
    for i in np.arange(len(r_list)):
        adp(abs(coef_energy * sum(wave * base[i])))
    return r_list, fft_result
