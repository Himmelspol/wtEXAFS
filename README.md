# wtEXAFS

#### Version: 0.1.1

#### Last update: 2022/04/03

wtEXAFS is an Windows GUI for wavelet transformation of EXAFS

## Prerequisites

It is highly recommended to create a new environment in `PyCharm` to run wtEXAFS.

- Windows10 x64
- Python >= 3.7
- matplotlib == 3.5.1
- numpy == 1.21.5
- pywin32 == 303

## How to start

It is noted that wtEXAFS needs to run on **Windows 10 (x64)**.

### For python users

- If `git` is existed, simply clone the repository:

      git clone https://github.com/Himmelspol/wtEXAFS.git

- Otherwise, download the ZIP file of the repository and unzip it.

#### 1. Start from Python

- Download Python (64-bit) from https://www.python.org/downloads/
- Select "Add Python 3.X to PATH" and install Python with "Customize installation" mode
- On "Advanced Options" page, choose "Install for all users" and install
- After successful installation, press Win + R and open command line window (cmd), then change directory to where "
  wtEXAFS" resides, for example:

       D：
       cd D:\test\wtEXAFS

- Install requirements in cmd as following:

       pip install -r requirements.txt

- Run "main.py" in cmd as following:

       python main.py  

#### 2. Start from PyCharm

- Open the project "wtEXAFS"
- Set python interpreter (python version: >= 3.7.9)
- Install requirements if necessary
- Run "main.py" in the root directory to use the GUI

### 2. Start from Windows executable file (.exe):

- Download the packaged files from (one of the three):
  1. Google drive: https://drive.google.com/drive/folders/1wctfzMaA-KoCo6_diqWzBwc80WCeka35?usp=sharing
  2. MEGA: https://mega.nz/folder/wMgnRCAD#Jv1gsYz5vHrjq1Nprh6VJA
  3. Baidu cloud: https://pan.baidu.com/s/1tvUyJV1Vec3nzR2bw19wLw  code:m8o4
- There are two types of file on the cloud:
  1. Download wtEXAFS-XXX.zip, unzip it, find wtEXAFS.exe in the folder and double-click to run
  2. Download wtEXAFS-XXX.exe, double-click to run (relatively slow)

## How to use

See guide_for_wtEXAFS.pdf for more details.

### 1. Import chi(k) data

#### 1.1 Single file mode:

- Open *.txt/.chi file containing at least two column, one column is k, the other column is chi(k):

      #-------------------------------------
      #  k   chi 
         0   0.0001
         0.5 0.0002
- *.chi file (.chi/.chi1/.chi2/.chi3) is a kind of EXAFS output file extracted from
  ATHENA (https://bruceravel.github.io/demeter/documents/Athena/index.html)
- In this mode, the user can specify in the input box the **row** where the data starts and the **column** where k, chi(
  k) resides
- Select `Confirm and show selected data` to refresh content display box
- Select `Continue and close this window`

#### 1.2 Multiple column mode

- **Only** open *.chi file containing at least two column, one column is k, the other columns are different chi(k)
- In this mode, the user can specify in the input box the **row** where the data starts and the **column** where k, chi(
  k) resides. For chi(k) column, enter `SPACE` to separate different column:

      # The numbers below represent different columns
      3 4 5 6 7 8 9
- Other operations are the same as Single file mode

### 2. k-weight selection

- If the imported data itself is k-weighted (e.g., k^3chi(k)), select `k-weight` to 0
- If the imported data is not k-weighted, select `k-weight` from 1, 2, and 3
- Click `Accept k-weight` and then the user can `Show k-weighted data`
- Click `Next step` for next step

### 3. Custom wavelet transform parameters

- Enter _kmin/kmax/dk_, _Rmin/Rmax/dR_ in the input box
- Enter _Sigma/Eta_ in Morlet wavelet input box and then `Accept` it
- Or Enter _n_ in Cauchy wavelet input box and then `Accept` it
- Then the user can `Show wavelet`
  #### NOTICE:
    - _kmin_ and _kmax_ must be within the data range
    - _Rmin_ must be > 0
    - _Sigma_ and _Eta_ must be > 0
    - _n_ must be > 1
    - if not sure, default value is ok
    - If the input _dK_ does not match the imported data, interpolation will be automatically performed

### 4. Start wavelet transformation

- Click `Start WT` to start calculation (usually takes 3 to 5s)
- Then the user can `Show WT result` or `Save WT result`
- The output file is a TXT file, with internal structure as following:

      # k_value R_value wavelet_coef(column3) wavelet_coef(column4) ...# This line will not display in the *.txt
        0.00000 0.50000 0.013305 0.012805
        0.05000 0.50000 0.013314 0.012963
        0.10000 0.50000 0.013400 0.013002

- If needed, Click `Start inverse WT` to reconstruct EXAFS spectra according to wavelet type and WT result
  #### NOTICE:
    - If multi-column mode was usd, only one spectral result can be displayed at a time. And the user can choose which
      one to display

## About author

Hi everyone, I am a beginner of XAFS and Python. Under the guidance of Prof. Peng Liu, I first came into contact with
EXAFS in 2019. Currently, I am a master's student at China University of Geosciences (Wuhan), majoring in Environmental
Science and Engineering.

I noticed that there are not many GUI for EXAFS wavelet transformation yet. Thus, with the purpose of learning, I wrote
this GUI and hope it can help others :)

EXAFS is a powerful technique for detecting the local structure of different materials. Actually, EXAFS is a composite
signal of electron waves, which is well suited for analysis using wavelet transform. Although it is difficult to gain
quantitative results from wavelet transformation of EXAFS signal, wavelet transformation can still give more information
to help us carry out k-space LCF, EXAFS modeling and so on.

## References

1. Ravel B. and Newville M. (2005) ATHENA, ARTEMIS, HEPHAESTUS: Data analysis for X-ray absorption spectroscopy using
   IFEFFIT. J. Synchrotron Radiat. 12, 537–541.
2. Munoz M., Argoul P. and Farges F. (2003) Continuous cauchy wavelet transform analyses of EXAFS spectra: A qualitative
   approach. Am. Mineral. 88, 694–700.
3. Funke H., Scheinost A. C. and Chukalina M. (2005) Wavelet analysis of extended x-ray absorption fine structure data.
   Phys. Rev. B - Condens. Matter Mater. Phys. 71, 1–7.
4. Funke H., Chukalina M. and Scheinost A. C. (2007) A new FEFF-based wavelet for EXAFS data analysis. J. Synchrotron
   Radiat. 14, 426–432.
5. Timoshenko J. and Kuzmin A. (2009) Wavelet data analysis of EXAFS spectra. Comput. Phys. Commun. 180, 920–925.
6. Xia Z., Zhang H., Shen K., Qu Y. and Jiang Z. (2018) Wavelet analysis of extended X-ray absorption fine structure
   data: Theory, application. Phys. B Condens. Matter 542, 12–19.
7. Arts L. P. A. and van den Broek E. L. (2022) The fast continuous wavelet transformation (fCWT) for real-time,
   high-quality, noise-resistant time–frequency analysis. Nat. Comput. Sci. 2, 47–58.
8. https://www.esrf.fr/UsersAndScience/Experiments/CRG/BM20/Software/Wavelets
9. http://perso.u-pem.fr/farges/wav/
10. https://github.com/hellozhaoming/wtexfas
11. https://github.com/wangmiaoX/wavelet-transform-exafs
12. http://en.volupedia.org/wiki/Convolution


