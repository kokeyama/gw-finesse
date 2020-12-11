
from pykat import finesse
import numpy as np

def get_all_port_list():
    """
    all_port_list = ["REFL", "AS", "TMSX", "TMSY",
                        "POP",
                        "POS",
                        "npr1","npr2","npr3","npr4","npr5","npr6",
                        "nsr1","nsr2","nsr3","nsr4","nsr5",
                        "n2", "n3", # n1=REFL, n4=AS
                        "nx1", "nx2", "nx3",
                        "ny1", "ny2", "ny3",
                        "n0", "n_eo1", "n_eo2", "n_eo3", "n_eo4"]
    """
    all_port_list = ["REFL", "AS", "TMSX", "TMSY",
                        "POP",
                        "POS",
                        "npr1","npr2","npr3","npr4","npr5","npr6",
                        "nsr1","nsr2","nsr3","nsr4","nsr5",
                        "n2", "n3", # n1=REFL, n4=AS
                        "nx1", "nx2", "nx3",
                        "ny1", "ny2", "ny3",
                        "n0", "n_eo1", "n_eo2", "n_eo3", "n_eo4"]
    return all_port_list

def get_all_parameter_names():
    all_parameter_key_names = []
    # laser
    key = "k_inf_c_laser_power"
    all_parameter_key_names.append(key)
    # mirror
    mirror_names = ["mibs", "itmx", "itmy", "etmx", "etmy", "prm", "srm", "pr2", "pr3", "sr2", "sr3"]
    mirror_paras = ["transmittance", "loss"]
    for mirror in mirror_names:
        for param in mirror_paras:
            key = "k_inf_c_%s_mirror_%s"%(mirror, param)
            all_parameter_key_names.append(key)
    # length
    length_names = ["prm_pr2", "pr2_pr3", "pr3_bs",
                    "srm_sr2", "sr2_sr3", "sr3_bs",
                    "bs_itmx", "bs_itmy", "itmx_etmx", "itmy_etmy"]
    for length in length_names:
        key = "k_inf_c_length_%s"%length
        all_parameter_key_names.append(key)
    # eom
    eom_names = ["f1", "f2"]
    eom_params = ["mod_frequency", "mod_index"]
    for eom in eom_names:
        for param in eom_params:
            key = "k_inf_c_%s_%s"%(eom, param)
            all_parameter_key_names.append(key)
    return all_parameter_key_names

def get_optimal_demod_phase(out, I_pdname, Q_pdname, N):
    #
    # usage: mag, phase = utils_DRFPMI.demod_phase(out, port, SB, N):
    # out: the computed signals from run_fsig
    # N: integer related to the frequency. Should be updated.
    #
    #
    #jupyter notebook script
    
    tot = out[I_pdname] + 1j*out[Q_pdname]
    #print(type(out[I_pdname]))
    #print(type(out[Q_pdname]))
    #mag=1
    phase = np.angle(tot)*180/np.pi
    # kokeyamasan script
    #I = np.sign(np.sin(np.angle(out[I_pdname][N])))* np.abs(out[I_pdname][N])
    #print("out_I = ")
    #print(I) #0.0になる
    #Q = np.sign(np.sin(np.angle(out[Q_pdname][N])))* np.abs(out[Q_pdname][N])
    #print("out_Q = ")
    #print(Q) #0.0になる
    #phase = np.arctan(Q/I)*180/np.pi
    #print("optimalphase = ")
    #print(phase) #nanになる
    #mag = np.sqrt(I**2 + Q**2)
    #print("mag = ")
    #print(mag)
    return phase

def get_model(values, inteferometer_config_list):
    
    input_finesse   = (
        """
        # ======== Constants ========================
        const fsb1 16.881M
        const fsb2 45.0159M
        const mfsb1 -16.881M
        const mfsb2 -45.0159M
        const a 0.686
        const pi 3.1415

        # ======== Input optics =====================
        l i1 1 0 n0
        s s_eo0 0 n0 n_eo1
        mod eom1 $fsb1 0.3 1 pm n_eo1 n_eo2
        s s_eo1 0 n_eo2 n_eo3
        mod eom2 $fsb2 0.3 1 pm n_eo3 n_eo4
        s s_eo2 0 n_eo4 REFL

        ## ======= PRC each mirror loss 45ppm =======
        # PRC

        m1 PRM 0.1 45e-6 0 REFL npr1
        s sLpr1 14.7615 npr1 npr2
        bs1 PR2 500e-6 45e-6 0 $a npr3 npr2 POP POP2
        s sLpr2 11.0661 npr3 npr4
        bs1 PR3 50e-6 45e-6 0 $a dump dump npr4 npr5
        s sLpr3 15.7638 npr5 npr6

        # Michelson
        bs bs1 0.5 0.5 0 45 npr6 n2 n3 n4
        s lx 26.6649 n3 nx1
        s ly 23.3351 n2 ny1

        # X arm
        m ITMX 0.996 0.004 0 nx1 nx2
        s sx1 3000 nx2 nx3
        m ETMX 0.999995 5e-06 0 nx3 TMSX

        # Y arm
        m ITMY 0.996 0.004 90 ny1 ny2
        s sy1 3000 ny2 ny3
        m ETMY 0.999995 5e-06 90 ny3 TMSY


        # ========= SRC each mirror loss 45ppm =======
        s sLsr3 15.7386 n4 nsr5
        bs1 SR3 50e-6 45e-6 0 $a nsr5 nsr4 dump dump
        s sLsr2 11.1115 nsr4 nsr3
        bs1 SR2 500e-6 45e-6 0 $a nsr2 nsr3 POS dump
        s sLsr1 14.7412 nsr2 nsr1
        m1 SRM 0.3 0e-6 0 nsr1 AS
        
        """
        )
    
    interferometer = inteferometer_config_list[0]
    type_of_pd_signal = inteferometer_config_list[1]
    
    # base
    drfpmi_model = finesse.kat()
    drfpmi_model.parse(input_finesse)
    print("drfpmi = \n")
    print(drfpmi_model)
    # model
    model = create_base_by_setting_param(values, drfpmi_model, interferometer)
        # use HOM
    if values["k_inf_c_laser_use_hom"]:
        model = hom_extention(values, model)
    # add xaxis command
    model = add_dofcommand_to_model(model, values, type_of_pd_signal)
    # add PDs
    model = add_pds_to_model(model, values, type_of_pd_signal, add_dofcommand_to_model)
    return model

def disable_FP_param(window, values):
    """

    """
    window["k_inf_c_itmx_mirror_transmittance"].update(value="1")
    window["k_inf_c_itmx_mirror_loss"].update(value="0")
    window["k_inf_c_itmy_mirror_transmittance"].update(value="1")
    window["k_inf_c_itmy_mirror_loss"].update(value="0")
    window["k_inf_c_length_itmx_etmx"].update(value="0")
    window["k_inf_c_length_itmy_etmy"].update(value="0")
    
    #window["k_inf_c_etmx_mirror_transmittance"].update(value="1")
    #window["k_inf_c_etmx_mirror_loss"].update(value="0")
    #window["k_inf_c_etmy_mirror_transmittance"].update(value="1")
    #window["k_inf_c_etmy_mirror_loss"].update(value="0")

def disable_PRC_param(window, values):
    window["k_inf_c_prm_mirror_transmittance"].update(value="1")
    window["k_inf_c_prm_mirror_loss"].update(value="0")
    window["k_inf_c_pr2_mirror_transmittance"].update(value="0")
    window["k_inf_c_pr2_mirror_loss"].update(value="0")
    window["k_inf_c_pr3_mirror_transmittance"].update(value="0")
    window["k_inf_c_pr3_mirror_loss"].update(value="0")
    #model.PRM.setRTL(0,1,0)
    #model.PR2.setRTL(1,0,0)
    #model.PR3.setRTL(1,0,0)
    window["k_inf_c_length_prm_pr2"].update(value="0")
    window["k_inf_c_length_pr2_pr3"].update(value="0")
    window["k_inf_c_length_pr3_bs"].update(value="0")
    #model.sLpr1.L = 0
    #model.sLpr2.L = 0
    #model.sLpr3.L = 0

def disable_SRC_param(window, values):
    window["k_inf_c_srm_mirror_transmittance"].update(value="1")
    window["k_inf_c_srm_mirror_loss"].update(value="0")
    window["k_inf_c_sr2_mirror_transmittance"].update(value="0")
    window["k_inf_c_sr2_mirror_loss"].update(value="0")
    window["k_inf_c_sr3_mirror_transmittance"].update(value="0")
    window["k_inf_c_sr3_mirror_loss"].update(value="0")
    #model.SRM.setRTL(0,1,0)
    #model.SR2.setRTL(1,0,0)
    #model.SR3.setRTL(1,0,0)
    window["k_inf_c_length_srm_sr2"].update(value="0")
    window["k_inf_c_length_sr2_sr3"].update(value="0")
    window["k_inf_c_length_sr3_bs"].update(value="0")
    #model.sLsr1.L = 0
    #model.sLsr2.L = 0
    #model.sLsr3.L = 0

def change_interferometer(window, values, interferometer):
    if interferometer=="MI":
        disable_SRC_param(window, values)
        disable_PRC_param(window, values)
        disable_FP_param(window,  values)
    elif interferometer=="FPMI":
        disable_SRC_param(window, values)
        disable_PRC_param(window, values)
    elif interferometer=="PRFPMI":
        disable_SRC_param(window, values)
    elif interferometer=="DRFPMI":
        pass

def change_default_optical_parameter(values, window, name):
    def set_parameter(window, default_dict):
        keys = list(default_dict.keys())
        for key in keys:
            window[key].update(value=str(default_dict[key]))
        for paranamekey in get_all_parameter_names():
            window[paranamekey].update(background_color="#d3d7dd")
    # kagra parameter
    if name == "kagra":
        default_value = {
        # laser
        "k_inf_c_laser_power"               : 1,
        # mirror
            # transmittance
        "k_inf_c_mibs_mirror_transmittance" : 0.5,
        "k_inf_c_itmx_mirror_transmittance" : 0.004,
        "k_inf_c_itmy_mirror_transmittance" : 0.004,
        "k_inf_c_etmx_mirror_transmittance" : 5e-6,
        "k_inf_c_etmy_mirror_transmittance" : 5e-6,
        "k_inf_c_prm_mirror_transmittance"  : 0.1,
        "k_inf_c_pr2_mirror_transmittance"  : 500e-6,
        "k_inf_c_pr3_mirror_transmittance"  : 50e-6,
        "k_inf_c_srm_mirror_transmittance"  : 0.1536,
        "k_inf_c_sr2_mirror_transmittance"  : 500e-6,
        "k_inf_c_sr3_mirror_transmittance"  : 50e-6,
            # loss
        "k_inf_c_mibs_mirror_loss"          : 0,
        "k_inf_c_itmx_mirror_loss"          : 45e-6,
        "k_inf_c_itmy_mirror_loss"          : 45e-6,
        "k_inf_c_etmx_mirror_loss"          : 45e-6,
        "k_inf_c_etmy_mirror_loss"          : 45e-6,
        "k_inf_c_prm_mirror_loss"           : 45e-6,
        "k_inf_c_pr2_mirror_loss"           : 45e-6,
        "k_inf_c_pr3_mirror_loss"           : 45e-6,
        "k_inf_c_srm_mirror_loss"           : 45e-6,
        "k_inf_c_sr2_mirror_loss"           : 45e-6,
        "k_inf_c_sr3_mirror_loss"           : 45e-6,
        # length
        "k_inf_c_length_prm_pr2"            : 14.7615,#slpr1
        "k_inf_c_length_pr2_pr3"            : 11.0661,#slpr2
        "k_inf_c_length_pr3_bs"             : 15.7638,#slpr3
        "k_inf_c_length_bs_itmx"            : 26.6649,#lx
        "k_inf_c_length_itmx_etmx"          : 3000,#sx1
        "k_inf_c_length_bs_itmy"            : 23.3351,#ly
        "k_inf_c_length_itmy_etmy"          : 3000,#sy1
        "k_inf_c_length_srm_sr2"            : 15.7386,#slsr1
        "k_inf_c_length_sr2_sr3"            : 11.1115,#slsr2
        "k_inf_c_length_sr3_bs"             : 14.7412,#slsr3
        # EOM
        "k_inf_c_f1_mod_frequency"          : 16.881e6,
        "k_inf_c_f1_mod_index"              : 0.3,
        "k_inf_c_f2_mod_frequency"          : 45.0159e6,
        "k_inf_c_f2_mod_index"              : 0.3,
        "k_inf_c_num_of_sidebands"          : 3
        }
        set_parameter(window, default_value)

def change_nums_unit_str_to_float(str_num):
    """
    str_numに含まれる省略した単位を数値に変換して,str_numをfloat型の数字に変換して計算した結果を返す

    Parameters
    ----------
    str_num    : str
        str型の数字

    Returns
    -------
    str_num : float
        計算した結果のfloat型の数字
    """
    str_num = str_num.replace('ppm','*10**(-6)')#pより先に置かないとpが置き換わってしまう
    str_num = str_num.replace('p',  '*10**(-12)')
    str_num = str_num.replace('n',  '*10**(-9)')
    str_num = str_num.replace('k',  '*10**3')
    str_num = str_num.replace('m',  '*10**(-3)')
    str_num = str_num.replace('M',  '*10**6')
    str_num = str_num.replace('G',  '*10**9')
    if str_num=="":
        pass
    else:
        str_num = eval(str_num)
    return str_num

def verify_input_chr_foramt_is_correct(input_str):
    """
    input_strに値が入っているか、入っている値はchange_nums_unit_str_to_floatで計算できるのかを調べる
    GUIのinputboxで入力した値をkatファイルのパラメータに代入できるかを調べるために作った
    """
    if input_str=="":
        return False
    else:
        try:
            a = change_nums_unit_str_to_float(input_str)
            a = a
            return True
        except:
            return False

def get_layout_drawing_path(base,interferometer,drawingsize):
    path=""
    if base=="kagra":
        if interferometer=="MI":
            if drawingsize=="normalsize":
                path = "../fig/MI_picture_normal.png"
            if drawingsize=="largesize":
                path = "../fig/MI_picture_large.png"
        if interferometer=="FPMI":
            if drawingsize=="normalsize":
                path = "../fig/FPMI_picture_normal.png"
            if drawingsize=="largesize":
                path = "../fig/FPMI_picture_large.png"
        if interferometer=="PRFPMI":
            if drawingsize=="normalsize":
                path = "../fig/PRFPMI_picture_normal.png"
            if drawingsize=="largesize":
                path = "../fig/PRFPMI_picture_large.png"
        if interferometer=="DRFPMI":
            if drawingsize=="normalsize":
                path = "../fig/DRFPMI_picture_normal.png"
            if drawingsize=="largesize":
                path = "../fig/DRFPMI_picture_large.png"
    else:
        pass
    return path

def layout_drawing_change(window, path):
    window["layout_drawing_key"].update
    window["layout_drawing_key"].update(filename=path)
    window["para_drawing_key"].update
    window["para_drawing_key"].update(filename=path)

def calculate_plot_fontsize(plotnum, v_plotnum, h_plotnum):
    """
    legendのfontsizeをplotする数によって変更する
    """
    fontsize = 18
    if   1<=plotnum and plotnum<=4:
        fontsize = 18
    elif 5<=plotnum and plotnum<=9:
        fontsize = 9
    elif 10<=plotnum and plotnum<=16:
        fontsize = 6
    else:
        # plotnumが大量にある時はfontsize=6くらいだと図が隠れるけど、逆にs大体形がわかればいいと思った
        fontsize = 6

    return fontsize

def run_func_by_boolean(boolean, func1, func2):
    """
    if boolean==True, run func1
    else, run func2
    """
    if boolean==True:
        func1()
    else:
        func2()

def hom_extention(values, base):
    model = base.deepcopy()
    # HOM parse
    model.lx.L = 26.4018 #26.6649-thickness*1.754
    model.ly.L = 23.072 #23.3351-thickness*1.754
    model.nodes.createNode("nitx1")
    model.nodes.createNode("nitx2")
    model.nodes.createNode("netx1")
    model.nodes.createNode("netx2")

    model.nodes.createNode("nity1")
    model.nodes.createNode("nity2")
    model.nodes.createNode("nety1")
    model.nodes.createNode("nety2")

    model.nodes.replaceNode(model.lx, "nx1", "nitx1")
    model.nodes.replaceNode(model.ly, "ny1", "nity1")

    model.nodes.replaceNode(model.ETMX, "TMSX", "netx1")
    model.nodes.replaceNode(model.ETMY, "TMSY", "nety1")

    hom_code = """

    # ======== Thick ITMs ======================
    m IXAR 0     1     0 nitx1 nitx2
    s thick_IX 0.15 1.754 nitx2 nx1

    m IYAR 0     1     0 nity1 nity2
    s thick_IY 0.15 1.754 nity2 ny1

    # ======== Thick ETMs ======================
    s thick_EX 0.15 1.754 netx1 netx2
    m EXAR 0     1     0  netx2 TMSX

    s thick_EY 0.15 1.754 nety1 nety2
    m EYAR 0     1     0  nety2 TMSY

    """
    model.parse(hom_code)

    hom_extention = """
    # =========  HOM Expansion =======
    attr PRM Rc -458.1285
    attr PR2 Rc -3.0764
    attr PR3 Rc -24.9165
    attr bs1 Rc 0
    attr ITMX Rc -1900.   # measured -1904.6
    attr ETMX Rc 1900.    # measured  1908.24
    attr ITMY Rc -1900    # measured -1904.4
    attr ETMY Rc 1900.    # measured  1905.55
    attr SRM Rc 458.1285
    attr SR2 Rc -2.9872
    attr SR3 Rc 24.9165
    attr IXAR Rc 0
    attr IYAR Rc 0

    cav XARM ITMX nx2 ETMX nx3
    cav YARM ITMY ny2 ETMY ny3
    cav PRX PRM npr1 ITMX nx1
    cav PRY PRM npr1 ITMY ny1
    cav SRX SRM nsr1 ITMX nx1
    cav SRY SRM nsr1 ITMY ny1
    maxtem off
    """
    model.parse(hom_extention)
    model.maxtem = change_nums_unit_str_to_float(values["k_inf_c_num_of_hom_order"])
    #print(model)
    return model

def create_base_by_setting_param(values, base, interferometer):
    changed_model = base.deepcopy()
    gui_param_to_model_param(values, changed_model)
    if interferometer=="MI":
        #FP
        changed_model = disable_FP_by_param(changed_model)
        #PRC
        changed_model = disable_PRC_by_param(changed_model)
        #SRC
        changed_model = disable_SRC_by_param(changed_model)
        return changed_model
    elif interferometer=="FPMI":
        #PRC
        changed_model = disable_PRC_by_param(changed_model)
        #SRC
        changed_model = disable_SRC_by_param(changed_model)
        return changed_model
    elif interferometer=="PRFPMI":
        #SRC
        changed_model = disable_SRC_by_param(changed_model)
        return changed_model
    else:
        return changed_model

def gui_param_to_model_param(values, model):
    #print(model)
    # laser power
    model.i1.P = values["k_inf_c_laser_power"]
    # transmittance
    model.bs1.T  = values["k_inf_c_mibs_mirror_transmittance"]
    model.ITMX.T = values["k_inf_c_itmx_mirror_transmittance"]
    model.ITMY.T = values["k_inf_c_itmy_mirror_transmittance"]
    model.ETMX.T = values["k_inf_c_etmx_mirror_transmittance"]
    model.ETMY.T = values["k_inf_c_etmy_mirror_transmittance"]
    model.PRM.T  = values["k_inf_c_prm_mirror_transmittance"]
    model.SRM.T  = values["k_inf_c_srm_mirror_transmittance"]
    model.PR2.T  = values["k_inf_c_pr2_mirror_transmittance"]
    model.PR3.T  = values["k_inf_c_pr3_mirror_transmittance"]
    model.SR2.T  = values["k_inf_c_sr2_mirror_transmittance"]
    model.SR3.T  = values["k_inf_c_sr3_mirror_transmittance"]
    # loss
    model.bs1.L  = values["k_inf_c_mibs_mirror_loss"]
    model.ITMX.L = values["k_inf_c_itmx_mirror_loss"]
    model.ITMY.L = values["k_inf_c_itmy_mirror_loss"]
    model.ETMX.L = values["k_inf_c_etmx_mirror_loss"]
    model.ETMY.L = values["k_inf_c_etmy_mirror_loss"]
    model.PRM.L  = values["k_inf_c_prm_mirror_loss"]
    model.SRM.L  = values["k_inf_c_srm_mirror_loss"]
    model.PR2.L  = values["k_inf_c_pr2_mirror_loss"]
    model.PR3.L  = values["k_inf_c_pr3_mirror_loss"]
    model.SR2.L  = values["k_inf_c_sr2_mirror_loss"]
    model.SR3.L  = values["k_inf_c_sr3_mirror_loss"]
    # reflectance
    model.bs1.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_mibs_mirror_loss"]) - change_nums_unit_str_to_float(values["k_inf_c_mibs_mirror_transmittance"])
    model.ITMX.R = 1 - change_nums_unit_str_to_float(values["k_inf_c_itmx_mirror_loss"]) - change_nums_unit_str_to_float(values["k_inf_c_itmx_mirror_transmittance"])
    model.ITMY.R = 1 - change_nums_unit_str_to_float(values["k_inf_c_itmy_mirror_loss"]) - change_nums_unit_str_to_float(values["k_inf_c_itmy_mirror_transmittance"])
    model.ETMX.R = 1 - change_nums_unit_str_to_float(values["k_inf_c_etmx_mirror_loss"]) - change_nums_unit_str_to_float(values["k_inf_c_etmx_mirror_transmittance"])
    model.ETMY.R = 1 - change_nums_unit_str_to_float(values["k_inf_c_etmy_mirror_loss"]) - change_nums_unit_str_to_float(values["k_inf_c_etmy_mirror_transmittance"])
    model.PRM.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_prm_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_prm_mirror_transmittance"])
    model.SRM.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_srm_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_srm_mirror_transmittance"])
    model.PR2.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_pr2_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_pr2_mirror_transmittance"])
    model.PR3.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_pr3_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_pr3_mirror_transmittance"])
    model.SR2.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_sr2_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_sr2_mirror_transmittance"])
    model.SR3.R  = 1 - change_nums_unit_str_to_float(values["k_inf_c_sr3_mirror_loss"])  - change_nums_unit_str_to_float(values["k_inf_c_sr3_mirror_transmittance"])
    # Length
    model.sLpr1.L = values["k_inf_c_length_prm_pr2"]
    model.sLpr2.L = values["k_inf_c_length_pr2_pr3"]
    model.sLpr3.L = values["k_inf_c_length_pr3_bs"]

    model.lx.L    = values["k_inf_c_length_bs_itmx"]
    model.ly.L    = values["k_inf_c_length_bs_itmy"]

    model.sx1.L   = values["k_inf_c_length_itmx_etmx"]
    model.sy1.L   = values["k_inf_c_length_itmy_etmy"]

    model.sLsr1.L = values["k_inf_c_length_srm_sr2"]
    model.sLsr2.L = values["k_inf_c_length_sr2_sr3"]
    model.sLsr3.L = values["k_inf_c_length_sr3_bs"]
    # EOM
    model.eom1.f     = values["k_inf_c_f1_mod_frequency"]
    model.eom1.midx  = values["k_inf_c_f1_mod_index"]
    model.eom1.order = values["k_inf_c_num_of_sidebands"]
    model.eom2.f     = values["k_inf_c_f2_mod_frequency"]
    model.eom2.midx  = values["k_inf_c_f2_mod_index"]
    model.eom2.order = values["k_inf_c_num_of_sidebands"]
    
def disable_FP_by_param(model):
    model.ITMX.setRTL(0,1,0)
    model.ITMY.setRTL(0,1,0)
    model.sx1.L   = 0
    model.sy1.L   = 0
    #model.ETMX.setRTL(0,0,1)
    #model.ETMY.setRTL(0,0,1)
    return model

def disable_PRC_by_param(model):
    model.PRM.setRTL(0,1,0)
    model.PR2.setRTL(1,0,0)
    model.PR3.setRTL(1,0,0)
    model.sLpr1.L = 0
    model.sLpr2.L = 0
    model.sLpr3.L = 0
    return model

def disable_SRC_by_param(model):
    model.SRM.setRTL(0,1,0)
    model.SR2.setRTL(1,0,0)
    model.SR3.setRTL(1,0,0)
    model.sLsr1.L = 0
    model.sLsr2.L = 0
    model.sLsr3.L = 0
    return model

def add_dofcommand_to_model(base, values, type_of_pd_signal):
    model = base.deepcopy()
    dof = values["kifo_dof"]
    xaxis_range_beg = change_nums_unit_str_to_float(values['k_inf_c_xaxis_range_beg'])
    xaxis_range_end = change_nums_unit_str_to_float(values['k_inf_c_xaxis_range_end'])
    samplingnum     = change_nums_unit_str_to_float(values['k_inf_c_samplingnum'])
    plotscale = "lin"
    if values["k_inf_c_xaxis_log"]:
        plotscale = "log"
    if values["kifo_dof_selection"]:
        if dof=="BS":
            if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1" or type_of_pd_signal=="sw_amptd"):
                model.parse(
                    """
                    xaxis ITMX phi lin -180 180 1000
                    put* ITMY phi $mx1
                    put* ETMX phi $x1
                    put* ETMY phi $mx1
                    """)
            if(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2" or type_of_pd_signal=="tf_amptd"):
                model.parse("""
                    fsig sig1 ETMX 10 0
                    fsig sig1 ITMX 10 0
                    fsig sig1 ETMY 10 180
                    fsig sig1 ITMY 10 180
                    xaxis sig1 f log 10 100 1000
                    yaxis lin abs:deg
                    """)
            elif(type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 lx 1 0
                    fsig sig1 ly 1 180
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis log abs
                    """)
        elif dof=="DARM":
            if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1" or type_of_pd_signal=="sw_amptd"):
                model.parse("""
                    xaxis ETMX phi lin -180 180 1000
                    put* ETMY phi $mx1
                    """)
            elif(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2" or type_of_pd_signal=="tf_amptd"):
                model.parse("""
                    fsig sig1 ETMX 10 0
                    fsig sig1 ETMY 10 180
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis lin abs:deg
                    """)
            elif(type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 sx1 1 0
                    fsig sig1 sy1 1 180
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis log abs
                    """)
        elif dof=="CARM":
            if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1" or type_of_pd_signal=="sw_amptd"):
                model.parse(
                    """
                    xaxis ETMX phi lin -180 180 1000
                    put* ETMY phi $x1
                    """)
            if(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2" or type_of_pd_signal=="tf_amptd" or type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 ETMX 10 0
                    fsig sig1 ETMY 10 0
                    xaxis sig1 f log 10 100 1000
                    yaxis lin abs:deg
                                """)
            elif(type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 sx1 1 0
                    fsig sig1 sy1 1 0
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis log abs
                    """)
        elif dof=="PRCL":
            if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1" or type_of_pd_signal=="sw_amptd"):
                model.parse(
                    """
                    xaxis PRM phi lin -180 180 1000
                    """)
            if(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2" or type_of_pd_signal=="tf_amptd" or type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 PRM 1 0
                    xaxis sig1 f log 10 100 1000
                    yaxis lin abs:deg
                                """)
            elif(type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 sLpr1 1 0
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis log abs
                    """)
        elif dof=="SRCL":
            if(type_of_pd_signal=="sw_power" or type_of_pd_signal=="sw_dmod1" or type_of_pd_signal=="sw_amptd"):
                model.parse(
                    """
                    var tuning 0.0
                    xaxis tuning phi lin -180 180 1000
                    put SRM phi $x1
                    """)
            if(type_of_pd_signal=="tf_power" or type_of_pd_signal=="tf_dmod2" or type_of_pd_signal=="tf_amptd" or type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 SRM 1 0
                    xaxis sig1 f log 10 100 1000
                    yaxis lin abs:deg
                                """)
            elif(type_of_pd_signal=="st_type1"):
                model.parse("""
                    fsig sig1 sLsr1 1 0
                    xaxis sig1 f log 0.01 1000 1000
                    yaxis log abs
                    """)
    elif values["kifo_sweep_phase_mirror_selection"]:
        if values["kifo_phase_sweep_mirror"]=="SRM":
            model.parse("""
                xaxis SRM phi lin -90 90 1000
                yaxis lin abs:deg
                            """)
        if values["kifo_phase_sweep_mirror"]=="PRM":
            model.parse("""
                xaxis PRM phi lin -90 90 1000
                yaxis lin abs:deg
                            """)
    model.xaxis.scale  = plotscale
    model.xaxis.limits = [xaxis_range_beg, xaxis_range_end]
    model.xaxis.steps  = samplingnum
    return model

def replace_chr(tmp, values):
    list1 = ["2fsb1","2fsb2", "3fsb1","3fsb2", "fsb1","fsb2"]
    f1_2  = change_nums_unit_str_to_float("2*%s"%values["k_inf_c_f1_mod_frequency"])
    f1_3  = change_nums_unit_str_to_float("3*%s"%values["k_inf_c_f1_mod_frequency"])
    f2_2  = change_nums_unit_str_to_float("2*%s"%values["k_inf_c_f2_mod_frequency"])
    f2_3  = change_nums_unit_str_to_float("3*%s"%values["k_inf_c_f2_mod_frequency"])
    list2 = [str(f1_2), str(f2_2), str(f1_3), str(f2_3), values["k_inf_c_f1_mod_frequency"], values["k_inf_c_f2_mod_frequency"]]
    #print(list2)
    for i in range(len(list1)):
        tmp = tmp.replace(list1[i], list2[i])
    return tmp

def parse_sw_dmod1_kat(values, model, port, freq, phase):
    if freq=="DC":            
        model.parse("pd0 pd0_DC_%s %s" % (port, port))
        return model
    else:
        if phase=="optimal":
            optimal_phase = get_first_mixer_optimal_phase(model, values, port, freq)
            phase = optimal_phase
            tmp = "pd1 pd1_insert_freqs_later_optimal%s_%s %s %s %s" % (optimal_phase, port, freq, optimal_phase, port)
            """
            tmp = replace_chr(tmp, values)
            tmp = tmp.replace('insert_freqs_later', freq)
            tmp = tmp.replace('Iphase', '0' )
            tmp = tmp.replace('Qphase', '90')
            model.parse(tmp)
            """
        else:
            tmp = "pd1 pd1_insert_freqs_later_%s_%s %s %s %s" % (phase, port, freq, phase, port)
            print(tmp)
        tmp = replace_chr(tmp, values)
        tmp = tmp.replace('insert_freqs_later', freq)
        tmp = tmp.replace('Iphase', '0' )
        tmp = tmp.replace('Qphase', '90')
        model.parse(tmp)
        return model
        ## def end

def get_first_mixer_optimal_phase(model, values, port, freq):
    # calculate first mixer optimal phase
    tmp_model = model.deepcopy()
    tmp1         = "pd1 pd1_insert_freqs_later_0_%s %s 0 %s" % (port, freq, port)
    tmp1         = replace_chr(tmp1, values)
    tmp2         = "pd1 pd1_insert_freqs_later_90_%s %s 90 %s" % (port, freq, port)
    tmp2         = replace_chr(tmp2, values)
    I_pdname     = "pd1_insert_freqs_later_0_%s"%(port)
    I_pdname     = replace_chr(I_pdname, values)
    Q_pdname     = "pd1_insert_freqs_later_90_%s"%(port)
    Q_pdname     = replace_chr(Q_pdname, values)
    tmp_model.parse(tmp1)
    tmp_model.parse(tmp2)
    tmp_model.xaxis.remove()
    tmp_model = add_dofcommand_to_model(tmp_model, values, "tf_dmod2")# sw_dmod1の項目だけど、ここで渡すのは"tf_dmod2"で合ってる
    tmp_model.xaxis.scale = "log"
    tmp_model.xaxis.limits = (1e-30, 1000)
    #print("now calculating optimalphase")
    #print(tmp_model)
    out = tmp_model.run()
    optimal_phase = get_optimal_demod_phase(out, I_pdname, Q_pdname, 0)[0]
    print("calculated optimal phase = %s"%optimal_phase)
    return optimal_phase

def parse_sw_dmod2_kat_not_optimal(values, model, port, freq, phase):
    tmp = "pd2 pd2_insert_freqs_later_%s_%s %s %s 10 %s"%(phase, port, freq, phase, port)
    tmp = tmp.replace('fsb1',values["k_inf_c_f1_mod_frequency"])
    tmp = tmp.replace('fsb2',values["k_inf_c_f2_mod_frequency"])
    tmp = tmp.replace('insert_freqs_later', freq)
    tmp = tmp.replace('Iphase', '0' )
    tmp = tmp.replace('Qphase', '90')
    model.parse(tmp)
    return model

def parse_sw_dmod2_kat_optimal(values, model, port, freq, phase):
    # calculate dmod1 optimal
    optimal_phase1 = get_first_mixer_optimal_phase(model, values, port, freq)
    """
    tmp_model = model.deepcopy()
    tmp1         = "pd1 pd1_insert_freqs_later_0_%s %s 0 %s" % (port, freq, port)
    tmp1         = replace_chr(tmp1, values)
    tmp2         = "pd1 pd1_insert_freqs_later_90_%s %s 90 %s" % (port, freq, port)
    tmp2         = replace_chr(tmp2, values)
    I_pdname     = "pd1_insert_freqs_later_0_%s"%(port)
    I_pdname     = replace_chr(I_pdname, values)
    Q_pdname     = "pd1_insert_freqs_later_90_%s"%(port)
    Q_pdname     = replace_chr(Q_pdname, values)
    tmp_model.parse(tmp1)
    tmp_model.parse(tmp2)
    tmp_model.xaxis.remove()
    tmp_model = add_dofcommand_to_model(tmp_model, values, "tf_dmod2")
    print("now calculating optimalphase")
    print(tmp_model)
    out = tmp_model.run()
    optimal_phase1 = get_optimal_demod_phase(out, I_pdname, Q_pdname, 0)[0]
    print("optimal phase1 = ")
    print(optimal_phase1)
    """

    # calculate dmod2 optimal
    tmp_model = model.deepcopy()
    tmp3         = "pd2 pd2_insert_freqs_later_0_%s %s %s 10 0 %s"%(port, freq, optimal_phase1, port)
    tmp3         = replace_chr(tmp3, values)
    tmp4         = "pd2 pd2_insert_freqs_later_90_%s %s %s 10 90 %s"%(port, freq, optimal_phase1, port)
    tmp4         = replace_chr(tmp4, values)
    I_pdname     = "pd2_insert_freqs_later_0_%s"%(port)
    I_pdname     = replace_chr(I_pdname, values)
    Q_pdname     = "pd2_insert_freqs_later_90_%s"%(port)
    Q_pdname     = replace_chr(Q_pdname, values)
    tmp_model.parse(tmp3)
    tmp_model.parse(tmp4)
    tmp_model.xaxis.remove()
    tmp_model = add_dofcommand_to_model(tmp_model, values, "tf_dmod2")# sw_dmod1の項目だけど、ここで渡すのは"tf_dmod2"で合ってる
    print("now calculating optimalphase")
    print(tmp_model)
    out = tmp_model.run()
    optimal_phase2 = get_optimal_demod_phase(out, I_pdname, Q_pdname, 0)[0]
    print("optimal phase2 = ")
    print(optimal_phase2)

    # put PD
    tmp5 = "pd2 pd2_insert_freqs_later_optimal%s_%s_%s %s %s 10 %s %s"%(optimal_phase1, optimal_phase2, port, freq, optimal_phase1, optimal_phase2, port)
    tmp5 = replace_chr(tmp5, values)
    tmp5 = tmp5.replace('insert_freqs_later', freq)
    tmp5 = tmp5.replace('Iphase', '0' )
    tmp5 = tmp5.replace('Qphase', '90')
    model.parse(tmp5)
    #model.parse(tmp4)
    print("now added optimal pd2")
    print(model)
    return model

def parse_sw_amptd_kat(model, values, port):
    # default value
    fsb1 = values["k_inf_c_f1_mod_frequency"]
    mfsb1 = "-"+values["k_inf_c_f1_mod_frequency"]
    fsb2 = values["k_inf_c_f2_mod_frequency"]
    mfsb2 = "-"+values["k_inf_c_f2_mod_frequency"]
    #model.parse("ad car_ad_REFL 0 REFL")
    if values["kifo_put_car_sw_amptd_flag"]:# or kifo_put_car_tf_amptd_flag:
        model.parse("ad car_ad_%s 0 %s" % (port, port))
    if values["kifo_put_f1u_sw_amptd_flag"]:# or kifo_put_f1u_tf_amptd_flag:
        model.parse("ad fsb1_upper_ad_%s %s %s" % (port, fsb1, port))
    if values["kifo_put_f1l_sw_amptd_flag"]:# or kifo_put_f1l_tf_amptd_flag:
        model.parse("ad fsb1_lower_ad_%s %s %s" % (port, mfsb1, port))
    if values["kifo_put_f2u_sw_amptd_flag"]:# or kifo_put_f2u_tf_amptd_flag:
        model.parse("ad fsb2_upper_ad_%s %s %s" % (port, fsb2, port))
    if values["kifo_put_f2l_sw_amptd_flag"]:# or kifo_put_f2l_tf_amptd_flag:
        model.parse("ad fsb2_lower_ad_%s %s %s" % (port, mfsb2, port))
    return model

def add_pds_to_model(base, values, type_of_pd_signal, add_dofcommand_to_model):
    model = base.deepcopy()
    #model = make_kat_pd(model, type_of_pd_signal, values)
    if type_of_pd_signal  =="sw_power":
        for port in get_all_port_list():
            if values["kifo_sw_power_%s"%port]:
                model.parse("pd0 pd0_DC_%s %s" % (port, port))
    elif type_of_pd_signal=="sw_amptd":
        # run
        for port in get_all_port_list():
            if values["kifo_sw_amptd_%s"%port]:
                model = parse_sw_amptd_kat(model, values, port)
    elif type_of_pd_signal=="sw_dmod1":
        for i in range(values["kgui_sw_dmod1_plotnum"]):
            num = i+1
            freq  = values["kifo_sw_dmod1_freq_combo%s"%(str(num))]
            phase = values["kifo_sw_dmod1_phase_combo%s"%(str(num))]
            port  = values["kifo_sw_dmod1_port_combo%s"%(str(num))]
            model = parse_sw_dmod1_kat(values, model, port, freq, phase)
    elif type_of_pd_signal=="tf_power":
        model.parse("pd0 pd0_DC_%s %s" % (port, port))
    elif type_of_pd_signal=="tf_amptd":
        model.parse("pd0 pd0_DC_%s %s" % (port, port))
    elif type_of_pd_signal=="tf_dmod2":
        #####
        for i in range(values["kgui_tf_dmod2_plotnum"]):
            i = i+1
            freq  = values["kifo_tf_dmod2_freq_combo%s"%(str(i))]
            phase = values["kifo_tf_dmod2_phase_combo%s"%(str(i))]
            port  = values["kifo_tf_dmod2_port_combo%s"%(str(i))]
            if phase =="optimal":
                model = parse_sw_dmod2_kat_optimal(values, model, port, freq, phase)
            else:
                model = parse_sw_dmod2_kat_not_optimal(values, model, port, freq, phase)
        #####
        # pd2を置く時にputのコマンドも一緒にparseすると重複した時にエラーが出る
        # pdは重複したものを勝手に消してくれるからいいが、
        # putの行をどうやってpykatのコマンドを使ってどう消すのかわからないので後から付け加えることにした
        print("now adding put")
        print(model.detectors.keys())
        for pdname in model.detectors.keys():
            model.parse("put %s f2 $x1"%pdname)
    elif type_of_pd_signal=="st_type1":
        freq = values["k_inf_c_f1_mod_frequency"]
        for port in get_all_port_list():
            if values["kifo_st_type1_%s"%port]:
                tmp = "qnoisedS qnoisedS_insert_freqs_later_%s 2 %s max $fs %s"%(port, freq, port)
                tmp = tmp.replace('fsb1',values["k_inf_c_f1_mod_frequency"])
                tmp = tmp.replace('fsb2',values["k_inf_c_f2_mod_frequency"])
                tmp = tmp.replace('insert_freqs_later', freq)
                model.parse(tmp)
        pass
    print("now added PDs")
    return model
    
def make_plot_f_title(base_name, interferometer, dof, type_of_pd_signal):
    plot_title = base_name+"_"+interferometer+"_"+dof+"_"+type_of_pd_signal
    return plot_title