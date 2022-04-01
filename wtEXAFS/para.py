# -*- coding:utf-8 -*-

# ----------- 输入参数 -----------
class Parameters:
    file_name = ""
    kmin = 0.00  # kmin (wave number) in dataset
    kmax = 10.00  # kmax in dataset
    dk = 0.05  # step size of k in dataset
    bmin = 0.00  # when user change the kmin/kmax/dk, they actually change bmin/bmax/db
    bmax = 10.00
    db = 0.05
    Rmin = 0.50  # Rmin (R of FT EXAFS)
    Rmax = 4.00  # Rmax
    dR = 0.05  # step size of R (user-defined)
    sigma = 1.0  # the half-width of Gaussian envelope for morlet wavelet
    eta = 10.0  # the frequency of the sine and cosine functions for morlet wavelet
    n = 100  # Cauthy wavelet parameter
    wavelet_coef = 1


# ----------- 参数字典 -----------
def ParaDict():
    para_dict = {
        'kmin:': Parameters.bmin, 'kmax:': Parameters.bmax, 'dk:': Parameters.db,
        'Rmin:': Parameters.Rmin, 'Rmax:': Parameters.Rmax, 'dR:': Parameters.dR,
        'sigma:': Parameters.sigma, 'eta:': Parameters.eta, 'n_order:': Parameters.n,
        'kmin_in_data:': Parameters.kmin, 'kmax_in_data:': Parameters.kmax,
        'deltak_in_data:': Parameters.dk
    }
    return para_dict
