import os, glob, sys
sys.path.append('/home/zhouyj/software/data_prep')
from obspy import read, UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.lines as mlines
from signal_lib import preprocess, calc_dist_km, calc_azm_deg
from reader import read_fpha, dtime2str, get_yb_data
import warnings
warnings.filterwarnings("ignore")

# i/o paths
fpha = 'input/yb_large-all.pha'
evid, ot = 2, '20210521212125'
chn_idx, chn = 2, 'Z'
data_dir = '/data4/YangBi_Fan'
get_data_dict = get_yb_data
data_dict = get_data_dict(UTCDateTime(ot), data_dir)
# sig proc
win_len = [10,100]
samp_rate = 100
npts = int(samp_rate * sum(win_len))
time = -win_len[0] + np.arange(npts) / samp_rate
freq_band = [[1,20],[0.1,5],[0.5,5]][0]
num_sta = 20
fout = 'output/yb_large-waveform_F-%s_%s-%sHz.pdf'%(chn,freq_band[0],freq_band[1])
#title = '%s Channel Waveform: %s %s-%sHz'%(chn, ot,freq_band[0],freq_band[1])
title = '(a) Waveform of F1 F2 & F3: %s Channel %s-%sHz'%(chn, freq_band[0],freq_band[1])
# fig config
fig_size = (12,9)
fsize_label = 14
fsize_title = 18
line_wid = 1.
alpha = 0.8

# read fpha
pick_dict = read_fpha(fpha)[evid][1]
dtype = [('sta','O'),('tp','O')]
picks = [(sta,tp) for sta, [tp,ts] in pick_dict.items()]
picks = np.array(picks, dtype=dtype)
picks = np.sort(picks, order='tp')[0:num_sta]

def plot_label(xlabel=None, ylabel=None, title=None):
    if xlabel: plt.xlabel(xlabel, fontsize=fsize_label)
    if ylabel: plt.ylabel(ylabel, fontsize=fsize_label)
    if title: plt.title(title, fontsize=fsize_title)
    plt.setp(plt.gca().xaxis.get_majorticklabels(), fontsize=fsize_label)
    plt.setp(plt.gca().yaxis.get_majorticklabels(), fontsize=fsize_label)

plt.figure(figsize=fig_size)
for ii,[sta,tp] in enumerate(picks):
    data_path = data_dict[sta][chn_idx]
    st = read(data_path)
    st = preprocess(st.slice(tp-win_len[0], tp+win_len[1]), samp_rate, freq_band)
    st_data = st.normalize()[0].data[0:npts] + ii*2
    color = 'gray' if ii>11 else 'k'
    plt.plot(time, st_data, color=color, lw=line_wid)
plt.vlines(0, -1, 2*ii+1, 'r', zorder=0)
plt.yticks(np.arange(len(picks))*2, picks['sta'], fontsize=fsize_label)
plot_label('Time (s)',None,title)
plt.tight_layout()
plt.savefig(fout)
