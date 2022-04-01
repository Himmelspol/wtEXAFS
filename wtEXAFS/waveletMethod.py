# -*- coding:utf-8 -*-
# Construct wavelet and wavelet transformation

from cmath import exp
from cmath import log
from cmath import sqrt
from math import pi

import numpy as np
from numba import jit


@jit(nopython=True, fastmath=True)
def energyCoef(r: float, omega: float):
    energy_normalized = (2 * r / omega) ** 0.5  # 引入能量归一化参数
    return energy_normalized


@jit(nopython=True, fastmath=True)
def morletC(r: float, b: float, sigma: float, eta: float, k_value: float):
    i = complex(0, 1)
    t = 2 * r * (k_value - b) / eta
    C = 1.0 / (sqrt(2.0 * pi) * sigma)
    morleti = C * exp(i * eta * t) * exp(-(t * t) / (2.0 * sigma * sigma))
    return morleti


@jit(nopython=True, fastmath=True)
def cauthyC(r: float, b: float, n: float, k_value: float):
    i = complex(0, 1)
    t = 2 * r * (k_value - b) / n
    cauthyi = pow(exp(log(i / (i + t))), (n + 1))
    return cauthyi


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


@jit(nopython=True, fastmath=True)
def iWT(w_matrix, energy_coef, wavelet_coef, dr):
    # 目前仍不清楚为什么这个算法能生效，这个算法与实际公式并不一致
    row_limit = len(w_matrix)
    for i in range(row_limit):
        w_matrix[i] = 4 * w_matrix[i] * dr / energy_coef[i]
    iw = np.sum((w_matrix / wavelet_coef), axis=0).real
    return iw


def fftWavelet(wavelet, k_list):
    wavelet = np.array(wavelet)
    fft_amp = abs(np.fft.fft(wavelet))
    fft_freq = np.fft.fftfreq(len(wavelet), d=(k_list[1] - k_list[0]) / (2 * pi))
    wavelet_coef = np.trapz(fft_amp, dx=(fft_freq[1] - fft_freq[0])) * (k_list[1] - k_list[0])
    return fft_freq, fft_amp, wavelet_coef
