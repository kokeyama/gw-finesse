# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import PySimpleGUI as sg
from pykat import finesse
from pykat.commands import *
import pykat
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import sys
import math
import datetime

sg.theme('LightGrey2')

def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))

# %%
all_interferometers = ["FPMI", "PRFPMI", "DRFPMI", "MI"]

all_ports = ["REFL", "AS", "nTMSX", "nTMSY",
             "POP","POP2",
             "POS",
             "npr1","npr2","npr3","npr4","npr5","npr6",
             "nsr1","nsr2","nsr3","nsr4","nsr5","nsr6",
             "n2", "n3", # n1=REFL, n4=AS
             "nx1", "nx2", "nx3",
             "ny1", "ny2", "ny3",
             "n0", "n_eo1", "n_eo2", "n_eo3", "n_eo4"]
all_important_ports = ["REFL", "AS", "nTMSX", "nTMSY",
                       "POP","POP2",
                       "POS",
             ]
all_gui_section_keys = []
for interferometer in all_interferometers:
    # すべてのsectionのkeyをここで設定
    all_gui_section_keys += ["k%s_sec_sw_setting"%interferometer,
                             "k%s_sec_tf_setting"%interferometer,
                             "k%s_sec_sw_power_setting"%interferometer,
                             "k%s_sec_sw_dmod1_setting"%interferometer,
                             "k%s_sec_tf_power_setting"%interferometer,
                             "k%s_sec_tf_dmod2_setting"%interferometer]
all_radiobox_keys = []
for interferometer in all_interferometers:
    # すべてのRADIOBOXのkeyをここで設定
    all_radiobox_keys += ["k%s_issw"%interferometer,
                          "k%s_istf"%interferometer,
                          "k%s_issw_power"%interferometer,
                          "k%s_issw_dmod1"%interferometer,
                          "k%s_istf_power"%interferometer,
                          "k%s_istf_dmod2"%interferometer]

all_demod_phases = ["Iphase", "Qphase"]
all_demod_freqs  = ["fsb1", "fsb2"]
all_pdname_heads = ["pd0", "pd1", "pd2"]

all_pdname_tails_i, all_pdname_tails_q = [], []

for freq in all_demod_freqs:
    all_pdname_tails_i.append("Iphase_%s"%freq)
for freq in all_demod_freqs:
    all_pdname_tails_q.append("Qphase_%s"%freq)


# %%
def generate_kat(pds_for_kat, dic_advanced_setting, selected_interferometer):
    """
    GUIで選択した設定のfinesseのkatテキストを作成する
    この関数で作成したkatファイルをfinesseで読み込んでシミュレーションを行う

    Parameters
    ----------
    pds_for_kat             : list of str
        関数make_pd_kat_for_finesseで作成した
        finesseで使うkatのテキストに追加するPdの部分をリストにしたもの
    dic_advanced_setting    : dictionary
        GUIで選択されたvaluesの値から干渉計の設定に関する値を取り出してまとめた辞書
    selected_interferometer : str
        GUIで選択されている干渉計構成の名前 MI/FPMI/PRFPMI/DRFPMI

    Returns
    -------
    code : dictionary
        finesseに送ったりplotを行うために必要な変数をまとめた辞書
    """
    
    ##############################
    ### get variables from GUI ###
    ##############################
    
    dof               = dic_advanced_setting["dof"]# pick up DoF (CARM / DARM / BS) from GUI
    type_of_pd_signal = dic_advanced_setting["type_of_pd_signal"]# sw_power/sw_dmod1/tf_power/tf_dmod2
    
    ### xaxis/yaxis setting ###
    x_plotscale       = dic_advanced_setting["x_plotscale"]# linear or log
    xaxis_range_beg   = dic_advanced_setting["xaxis_range_beg"]#plotしたときのx軸の最小値
    xaxis_range_end   = dic_advanced_setting["xaxis_range_end"]#plotしたときのx軸の最大値
    y_plotscale       = dic_advanced_setting["y_plotscale"]#str

    if x_plotscale=='linear':
        x_plotscale = 'lin'
    if y_plotscale=='linear':
        y_plotscale = 'lin'

    samplingnum       = dic_advanced_setting["samplingnum"]# サンプリング数
    
    ######################
    ### INF components ###
    ######################

    input_finesse = create_input_finesse(dic_advanced_setting, selected_interferometer)

    ## pds ##
    input_finesse += """
## PDs ##
"""
    for pd in pds_for_kat:
        input_finesse += """%s""" % pd

    ### DoF ###

    ### sweep ###
    if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1"):
        if(dof=="DARM"):
            input_finesse += """
            
# DARM scan
xaxis ETMX phi %s %s %s %s
put* ETMY phi $mx1
yaxis abs
            """ % (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)

        elif(dof=="CARM"):
            input_finesse += """
            
# CARM scan
#(koyama) xaxis*
#initial
# m ITMX 0.996 0.004 0 nx1 nx2
xaxis ETMX phi %s %s %s %s
put* ETMY phi $x1
yaxis abs
            """ % (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)

        elif(dof=="BS" and selected_interferometer!="MI"):
            input_finesse += """
            
# BS scan
#
#(koyama) original vergion log kokeyamasan uses xaxis*
# select xaxis plotscale "log" cause an error with xaxis*
# m ITMX 0.996 0.004 0 nx1 nx2
# since the config are above, I think it doesnt cause any problem about the correctness of the result
#

xaxis ITMX phi %s %s %s %s
put* ITMY phi $mx1
put* ETMX phi $x1
put* ETMY phi $mx1
yaxis abs
            """ % (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)
        elif(dof=="BS" and selected_interferometer=="MI"):
            input_finesse += """
            
# BS scan
#
#(koyama) original vergion log kokeyamasan uses xaxis*
# select xaxis plotscale "log" cause an error with xaxis*
# m ITMX 0.996 0.004 0 nx1 nx2
# since the config are above, I think it doesnt cause any problem about the correctness of the result
#

xaxis ITMX phi %s %s %s %s
put* ITMY phi $mx1
yaxis abs
            """ % (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)
        elif(dof=="PRCL"):
            input_finesse += """
            
# PRM scan
xaxis PRM phi %s %s %s %s
yaxis lin abs
            """% (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)
        elif(dof=="SRCL"):
            input_finesse += """
            
# SRM scan
var tuning 0.0
xaxis tuning phi %s %s %s %s
put SRM phi $x1
            """% (x_plotscale, xaxis_range_beg,xaxis_range_end, samplingnum)
        else:
            pass

    ### transfer function ###
    if(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2"):
        
        if(dof=="DARM"):
            input_finesse += """
            
### DARM ###
fsig sig1 ETMX 10 0
fsig sig1 ETMY 10 180
xaxis sig1 f %s %s %s %s
yaxis lin abs:deg
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        elif(dof=="CARM"):
            input_finesse += """
            
### CARM ###
fsig sig1 ETMX 10 0
fsig sig1 ETMY 10 0
xaxis sig1 f %s %s %s %s
yaxis lin abs:deg
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        elif(dof=="BS"and selected_interferometer!="MI"):
            input_finesse += """
            
### BS ###
fsig sig1 ETMX 10 0
fsig sig1 ITMX 10 0
fsig sig1 ETMY 10 180
fsig sig1 ITMY 10 180
xaxis sig1 f %s %s %s %s
yaxis lin abs
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        elif(dof=="BS"and selected_interferometer=="MI"):
            input_finesse += """

### BS ###
fsig sig1 ITMX 10 0
fsig sig1 ITMY 10 180
xaxis sig1 f %s %s %s %s
yaxis lin abs
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        elif(dof=="PRCL"):
            input_finesse += """

### PRCL ###
fsig sig1 PRM 1 0
xaxis sig1 f %s %s %s %s
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        elif(dof=="SRCL"):
            input_finesse += """
            
### SRCL ###
fsig sig1 SRM 1 0
xaxis sig1 f %s %s %s %s
            """ % (x_plotscale, xaxis_range_beg, xaxis_range_end, samplingnum)
        else:
            pass

    code = input_finesse
    print(code)
    return code
# %%
# make_dof_sentence_for_finesse


# %%
def create_input_finesse(dic_advanced_setting, selected_interferometer):# make_interferometer_sentence_for_finesse
    """
    選択した干渉計をfinesseでシミュレーションするためのkatテキストを、GUIのOPTIONタブで設定した例外的な設定などを加えて作成する

    Parameters
    ----------
    dic_advanced_setting    : dictionary
        GUIで選択されたvaluesの値から干渉計の設定に関する値を取り出してまとめた辞書
    selected_interferometer : str
        GUIで選択されている干渉計構成の名前 MI/FPMI/PRFPMI/DRFPMI

    Returns
    -------
    input_finesse : dictionary
        finesseに送ったりplotを行うために必要な変数をまとめた辞書
    """

    laser_power     = dic_advanced_setting["laser_power"]
    prc_mirror_loss = dic_advanced_setting["prc_mirror_loss"]
    src_mirror_loss = dic_advanced_setting["src_mirror_loss"]

    if selected_interferometer=="MI":
        input_finesse = """

### MI

const fsb1 16.881M
const fsb2 45.0159M

# Input optics
l I_fsb1 %s 0 n0
s s_eo0 0 n0 n_eo1
mod eom1 16.881M 0.3 1 pm n_eo1 n_eo2
s s_eo1 0 n_eo2 n_eo3
mod eom2 45.0159M 0.3 1 pm n_eo3 n_eo4
s s_eo2 0 n_eo4 REFL

# Michelson
bs bs1 0.5 0.5 0 45 REFL n2 n3 AS
s lx 26.6649 n3 nx1
s ly 23.3351 n2 ny1

# X arm
m ITMX 0.996 0.004 0 nx1 nx2

# Y arm
m ITMY 0.996 0.004 90 ny1 ny2

        """ % (laser_power)
    elif selected_interferometer=="FPMI":
        input_finesse = """

### FPMI

const fsb1 16.881M
const fsb2 45.0159M

# Input optics
l I_fsb1 %s 0 n0
s s_eo0 0 n0 n_eo1
mod eom1 16.881M 0.3 1 pm n_eo1 n_eo2
s s_eo1 0 n_eo2 n_eo3
mod eom2 45.0159M 0.3 1 pm n_eo3 n_eo4
s s_eo2 0 n_eo4 REFL

# Michelson
bs bs1 0.5 0.5 0 45 REFL n2 n3 AS
s lx 26.6649 n3 nx1
s ly 23.3351 n2 ny1


# X arm
m ITMX 0.996 0.004 0 nx1 nx2
s sx1 3000 nx2 nx3
m ETMX 0.99995 5e-06 0 nx3 nTMSX

# Y arm
m ITMY 0.996 0.004 90 ny1 ny2
s sy1 3000 ny2 ny3
m ETMY 0.99995 5e-06 90 ny3 nTMSY

        """ % (laser_power)
        
    elif selected_interferometer=="PRFPMI":
        input_finesse = """
# PRFPMI
# 
# ======== Constants ========================
const fsb1 16.881M
const fsb2 45.0159M
const mfsb1 -16.881M
const mfsb2 -45.0159M
const a 0.686
const prc_loss %s

# ======== Input optics =====================
l i1 %s 0 n0
s s_eo0 0 n0 n_eo1
mod eom1 $fsb1 0.3 1 pm n_eo1 n_eo2
s s_eo1 0 n_eo2 n_eo3
mod eom2 $fsb2 0.3 1 pm n_eo3 n_eo4
s s_eo2 0 n_eo4 REFL

## ======= PRC each mirror loss $prc_loss =======
# PRC
#m1 PRM 1 0e-6 0 REFL npr1
m1 PRM 0.1 $prc_loss 0 REFL npr1
s sLpr1 14.7615 npr1 npr2
bs1 PR2 500e-6 $prc_loss 0 $a npr3 npr2 POP POP2
s sLpr2 11.0661 npr3 npr4
bs1 PR3 50e-6 $prc_loss 0 $a dump dump npr4 npr5
s sLpr3 15.7638 npr5 npr6

# Michelson
bs bs1 0.5 0.5 0 45 npr6 n2 n3 AS
s lx 26.6649 n3 nx1
s ly 23.3351 n2 ny1

# X arm
m ITMX 0.996 0.004 0 nx1 nx2
s sx1 3000 nx2 nx3
m ETMX 0.999995 5e-06 0 nx3 nTMSX

# Y arm
m ITMY 0.996 0.004 90 ny1 ny2
s sy1 3000 ny2 ny3
m ETMY 0.999995 5e-06 90 ny3 nTMSY
        """%(prc_mirror_loss, laser_power)

    elif selected_interferometer=="DRFPMI":
        input_finesse = """
# DRFPMI
#
# ======== Constants ========================
const fsb1 16.881M
const fsb2 45.0159M
const mfsb1 -16.881M
const mfsb2 -45.0159M
const a 0.686
const prc_loss %s
const src_loss %s

# ======== Input optics =====================
l i1 %s 0 n0
s s_eo0 0 n0 n_eo1
mod eom1 $fsb1 0.3 1 pm n_eo1 n_eo2
s s_eo1 0 n_eo2 n_eo3
mod eom2 $fsb2 0.3 1 pm n_eo3 n_eo4
s s_eo2 0 n_eo4 REFL

## ======= PRC each mirror loss $prc_loss =======
# PRC
#m1 PRM 1 0e-6 0 REFL npr1
m1 PRM 0.1 $prc_loss 0 REFL npr1
s sLpr1 14.7615 npr1 npr2
bs1 PR2 500e-6 $prc_loss 0 $a npr3 npr2 POP POP2
s sLpr2 11.0661 npr3 npr4
bs1 PR3 50e-6 $prc_loss 0 $a dump dump npr4 npr5
s sLpr3 15.7638 npr5 npr6

# Michelson
bs bs1 0.5 0.5 0 45 npr6 n2 n3 n4
s lx 26.6649 n3 nx1
s ly 23.3351 n2 ny1

# X arm
m ITMX 0.996 0.004 0 nx1 nx2
s sx1 3000 nx2 nx3
m ETMX 0.999995 5e-06 0 nx3 nTMSX

# Y arm
m ITMY 0.996 0.004 90 ny1 ny2
s sy1 3000 ny2 ny3
m ETMY 0.999995 5e-06 90 ny3 nTMSY

# ========= SRC each mirror loss 45ppm =======
s sLsr3 15.7396 n4 nsr5
bs1 SR3 50e-6 $src_loss 0 $a nsr5 nsr4 dump dump
s sLsr2 11.1115 nsr4 nsr3
bs1 SR2 500e-6 $src_loss 0 $a nsr2 nsr3 POS dump
s sLsr1 14.7412 nsr2 nsr1
m1 SRM 0.3 $src_loss 0 nsr1 AS
        """%(prc_mirror_loss, src_mirror_loss, laser_power)


    
    return input_finesse


# %%
def make_dic_selected_setting_from_gui(values, selected_tab, type_of_pd_signal):
    """
    GUIで選択した設定とそれを加工して作った変数を辞書でまとめて返す。

    Parameters
    ----------
    values            : dictionary
        pysimpleGUIで選択した値の辞書
    selected_tab      : str
        GUIで選択されている干渉計構成の名前 MI/FPMI/PRFPMI/DRFPMI
    type_of_pd_signal : str
        GUIで選択されているPdの信号の検出の方法 sw_power/sw_dmod1/tf_power/tf_dmod2

    Returns
    -------
    dic_selected_setting_from_gui : dictionary
        finesseに送ったりplotを行うために必要な変数をまとめた辞書
    
    See Also
    --------
    all_ports        : list of str
        GUIで用意しているすべてのportのリスト
    all_pdname_heads : list of str
        GUIで用意しているすべてのpdの種類のリスト
    all_demod_freqs  : list of str
        GUIで用意しているすべての復調（変調）周波数のリスト
    all_demod_phases : list of str
        GUIで用意しているすべての復調位相のリスト（Iphase/Qphase）
    """
    
    port_trues   = []
    pdname_tails = []

    interferometer = selected_tab
        
    # port_true
    for port in all_ports:
        port_name = "%s_%s" % (interferometer, port)
        if "k"+port_name in values:# valueにはGUIのチェックボックスのkFPMI_REFLなどが入っている
            if(values["k"+port_name]):
                port_trues.append(port)
        
    # pdname_heads
    if type_of_pd_signal  =="sw_power" or type_of_pd_signal=="tf_power":
        pdname_head = "pd0"
    elif type_of_pd_signal=="sw_dmod1":
        pdname_head = "pd1"
    elif type_of_pd_signal=="tf_dmod2":
        pdname_head = "pd2"
        
    # pdname_tails
    for freq in all_demod_freqs:
        for phase in all_demod_phases:
            tail = "%s_%s"%(phase, freq)
            key  = "k%s_%s_%s"%(interferometer, pdname_head, tail)
            if key in values:
                if values[key]:
                    pdname_tails.append(tail)
            
    # demod_phase
    demod_phase = values["k%s_pd1_demod_phase"%selected_tab]
    if(type_of_pd_signal=="tf_dmod2"):
        demod_phase  = values["k%s_pd2_demod_phase"%selected_tab]
    
    dic_selected_setting_from_gui = {
            'type_of_pd_signal': type_of_pd_signal,
            'interferometer'   : interferometer,
            'port_trues'       : port_trues,
            'pdname_head'      : pdname_head,
            'pdname_tails'     : pdname_tails,
            'demod_phase'      : demod_phase,
            'put_cr_amp_detecter_flag'  : values['k_inf_c_put_cr_amp_detecter_flag'],
            'put_f1_amp_detecter_flag'  : values['k_inf_c_put_f1_amp_detecter_flag'],
            'put_f2_amp_detecter_flag'  : values['k_inf_c_put_f2_amp_detecter_flag']
            }
    
    return dic_selected_setting_from_gui
# %%
#def make_pdname():


# %%
def make_pd_kat_for_finesse(dic_selected_setting_from_gui):# make_pd_sentence_for _finesse
    """
    関数 make_dic_selected_setting_from_gui で作成した辞書を使って、finesseでノードに置くpdのテキストを作る

    Parameters
    ----------
    dic_selected_setting_from_gui : dictionary
        make_dic_selected_setting_from_guiで作成した辞書
    Returns
    -------
    pds_for_kat        : list of str
        finesseで使うkatのテキストに追加するPdの部分をリストにしたもの

    See Also
    --------
    all_pdname_tails_i : list of str
        Pdの名前の頭につける時にIphaseになるtailのリスト
    all_pdname_tails_q : list of str
        Pdの名前の頭につける時にQphaseになるtailのリスト
    """

    interferometer           = dic_selected_setting_from_gui["interferometer"]
    type_of_pd_signal        = dic_selected_setting_from_gui["type_of_pd_signal"]
    port_trues               = dic_selected_setting_from_gui["port_trues"]
    pdname_head              = dic_selected_setting_from_gui["pdname_head"]
    pdname_tails             = dic_selected_setting_from_gui["pdname_tails"]
    demod_phase              = dic_selected_setting_from_gui["demod_phase"]
    put_cr_amp_detecter_flag = dic_selected_setting_from_gui["put_f1_amp_detecter_flag"]
    put_f1_amp_detecter_flag = dic_selected_setting_from_gui["put_f1_amp_detecter_flag"]
    put_f2_amp_detecter_flag = dic_selected_setting_from_gui["put_f2_amp_detecter_flag"]
    pds_for_kat              = []
    
    if type_of_pd_signal=="sw_power" or type_of_pd_signal=="tf_power":
        for port in port_trues:
            pds_for_kat.append("""
pd0 %s_%s %s""" % (pdname_head, port, port)
            )
            if put_cr_amp_detecter_flag:
                pds_for_kat.append("""
ad cr_%s_%s 0 %s""" % (pdname_head, port, port)
                )
            if put_f1_amp_detecter_flag:
                pds_for_kat.append("""
ad fsb1_%s_%s $fsb1 %s""" % (pdname_head, port, port)
                )
            if put_f2_amp_detecter_flag:
                pds_for_kat.append("""
ad fsb2_%s_%s $fsb2 %s""" % (pdname_head, port, port)
                )
    else:
        for port in port_trues:
            for pdname_tail in pdname_tails:
                pdname = "%s_%s_%s"%(pdname_head, pdname_tail, port)
                freq = pdname_tail.split("_")[1]
                if   pdname_tail in all_pdname_tails_i:
                    phase = str(0+float(demod_phase))
                elif pdname_tail in all_pdname_tails_q:
                    phase = str(90+float(demod_phase))
                
                if   type_of_pd_signal=="sw_dmod1":
                    pds_for_kat.append("""
pd1 %s $%s %s %s"""%  (pdname, freq, phase, port))
                    # 周波数ごと(CR, f1 f2)に見る場合
                    if put_cr_amp_detecter_flag:
                        pds_for_kat.append("""
ad cr_%s_%s 0 %s""" % (pdname_head, port, port)
                )
                    if put_f1_amp_detecter_flag:
                        pds_for_kat.append("""
ad fsb1_%s_%s $fsb1 %s""" % (pdname_head, port, port)
                )
                    if put_f2_amp_detecter_flag:
                        pds_for_kat.append("""
ad fsb2_%s_%s $fsb2 %s""" % (pdname_head, port, port)
                )
                elif type_of_pd_signal=="tf_dmod2":
                    pds_for_kat.append("""
pd2 %s $%s %s 10 %s
put %s f2 $x1"""%     (pdname, freq, phase, port, pdname))
                    # 周波数ごと(CR, f1 f2)に見る場合
                    if put_cr_amp_detecter_flag:
                        pds_for_kat.append("""
ad cr_%s_%s 0 %s""" % (pdname_head, port, port)
                )
                    if put_f1_amp_detecter_flag:
                        pds_for_kat.append("""
ad fsb1_%s_%s $fsb1 %s""" % (pdname_head, port, port)
                )
                    if put_f2_amp_detecter_flag:
                        pds_for_kat.append("""
ad fsb2_%s_%s $fsb2 %s""" % (pdname_head, port, port)
                )
                else:
                    pass
                                           
    # 重複するとfinesseのエラーが出るから重複はなくす
    pds_for_kat = set(pds_for_kat)
    
    return pds_for_kat


# %%
def set_gui_window_visible(target_section_keys, should_be_visible, window):
    """
    第一引数で渡した名前のセクションを第二引数がTrueなら開く、Falseなら閉じる

    Parameters
    ----------
    target_section_keys : dictionary
        開閉するGUIのオブジェクトのkeyの名前のリスト
    should_be_visible   : bool
        Trueなら開き、Falseなら閉じる
    window 　　　　　　　　: PySimpleGUI.PySimpleGUI.Window
        pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    See Also
    --------
    pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    """

    for key in target_section_keys:
        window[key].update(visible=should_be_visible)

def set_gui_window_bool(target_keys, should_be_enabled, window):
    """
    第一引数で渡した名前のGUIオブジェクトを第二引数の真偽値の値にする

    Parameters
    ----------
    target_keys       : list of str
        真偽値を変更するGUIのオブジェクトのkeyの名前のリスト
    should_be_enabled : bool
        変更する真偽値
    window            : PySimpleGUI.PySimpleGUI.Window
        pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    See Also
    --------
    pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    """

    for key in target_keys:
        window[key].update(should_be_enabled)

def set_gui_port_bool(values, selected_tab, target_ports, port_flag, window):
    """
    引数で渡されたGUIで選択するポート target_ports の値を port_flag(True/False) の値にする

    Parameters
    ----------
    values         : dictionary
        make_dic_selected_setting_from_guiで作成した辞書
    selected_tab   : str
        GUIで選択されている干渉計構成の名前 MI/FPMI/PRFPMI/DRFPMI
    target_ports   : list of str
        真偽値を変更するポートのkeyのリスト
    port_flag      : bool
        ポートの真偽値をこの値に変更する
    window         : PySimpleGUI.PySimpleGUI.Window
        pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    See Also
    --------
    pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    """

    for i in target_ports:
        key = "k%s_%s"%(selected_tab, i)
        if key in values:
            window[key].update(port_flag)


# %%
def change_GUI_plotscale(axis_plotscales, should_set_default_value, window):
    """
    GUIのplotscaleを第一引数で渡されたscaleにしてxaxisの範囲に入力できる値を制限する、第二引数がTrueならxaxisの範囲にdefaultの値を代入する

    Parameters
    ----------
    axis_plotscales          : list of str
        プロットするときのx軸とy軸のスケールをlistの要素の値に変更する
        lin/log 以外の値が含まれている場合には何もしない
        axis_plotscales[0]がx軸でaxis_plotscales[1]がy軸
    should_set_default_value : bool
        x軸の範囲にデフォルトの値を入力するかどうか
    window                   : PySimpleGUI.PySimpleGUI.Window
    
        pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    See Also
    --------
    pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    """

    xaxis_plotscale = axis_plotscales[0]
    yaxis_plotscale = axis_plotscales[1]

    if xaxis_plotscale=="lin":
        window["k_inf_c_xaxis_lin"].update(True)
        value_beg = "-180"
        value_end = "180"
    elif xaxis_plotscale=="log":
        window["k_inf_c_xaxis_log"].update(True)
        value_beg = "0.01"
        value_end = "1000"
    else:
        pass
    if yaxis_plotscale=="lin":
        window["k_inf_c_yaxis_lin"].update(True)
    elif yaxis_plotscale=="log":
        window["k_inf_c_yaxis_log"].update(True)
    else:
        pass

    if should_set_default_value:
        window['k_inf_c_xaxis_range_beg'].update(value_beg)
        window['k_inf_c_xaxis_range_end'].update(value_end)


# %%
def set_drawing_size_enlarge(selected_tab, enlarge_flag, window):
    """
    第一引数で指定されたタブの図のサイズを第二引数がTrueなら拡大し、Falseなら通常に戻す

    Parameters
    ----------
    selected_tab : str
        GUIで選択されている干渉計構成の名前 MI/FPMI/PRFPMI/DRFPMI
    enlarge_flag : bool
        図のサイズを大きくするか通常のサイズにするか
    window       : PySimpleGUI.PySimpleGUI.Window
        pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    See Also
    --------
    pysimpleGUIのオブジェクトの値を変えるにはwindowも渡さないといけないらしくないと実行できない
    Notes
    -----
    enlarge_flag の値がFalseの場合には、GUIの図の大きさはnormalサイズにする
    """

    for interferometer in all_interferometers:
        window["k%s_drawing_normalsize"%interferometer].update(visible=False)
        window["k%s_drawing_largesize" %interferometer].update(visible=False)
    if enlarge_flag == False:
        window["k%s_drawing_normalsize"%selected_tab].update(visible= True)
        window["k%s_drawing_largesize" %interferometer].update(visible=False)
    elif enlarge_flag == True:
        window["k%s_drawing_normalsize"%interferometer].update(visible=False)
        window["k%s_drawing_largesize" %selected_tab].update(visible= True)


