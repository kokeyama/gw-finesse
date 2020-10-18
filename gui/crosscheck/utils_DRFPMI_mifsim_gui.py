#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pykat
from pykat import finesse
import numpy as np

def model_DRFPMI():
    #
    # usage: base = utils_DRFPMI.model_DRFPMI()
    # output is the finesse structure with the DRFPMI configuration
    #
    #
    base = finesse.kat()
    base.verbose=False
    base.parse("""
    
    # ======== Constants ========================
    const fsb1 16881000.0
    const fsb2 45015900.0
    const mfsb1 -16881000.0
    const mfsb2 -45015900.0
    const arbitraryfreq001 0
    const arbitraryfreq002 0
    const a 0.686

    # DRFPMI
    #
    # ======== Input optics =====================
    l i1 1 0 n0
    s s_eo0 0 n0 n_eo1
    mod eom1 $fsb1 0.3 1 pm n_eo1 n_eo2
    s s_eo1 0 n_eo2 n_eo3
    mod eom2 $fsb2 0.3 1 pm n_eo3 n_eo4
    s s_eo2 0 n_eo4 REFL

    ## ======= PRC each mirror loss $prc_loss =======
    # PRC
    m1 PRM 0.1 4.5e-05 0 REFL npr1
    s sLpr1 14.7615 npr1 npr2
    bs1 PR2 0.0005 4.5e-05 0 $a npr3 npr2 POP POP2
    s sLpr2 11.0661 npr3 npr4
    bs1 PR3 5e-05 4.5e-05 0 $a dump dump npr4 npr5
    s sLpr3 15.7638 npr5 npr6

    # ======= Michelson =======
    bs1 MIbs 0.5 0 0 45 npr6 n2 n3 n4
    s lx 26.6649 n3 nx1
    s ly 23.3351 n2 ny1

    # X arm
    m1 ITMX 0.004 0 0 nx1 nx2
    s sx1 3000 nx2 nx3
    m1 ETMX 5e-06 0 0 nx3 nTMSX

    # Y arm
    m1 ITMY 0.004 0 90 ny1 ny2
    s sy1 3000 ny2 ny3
    m1 ETMY 5e-06 0 90 ny3 nTMSY

    # ========= SRC each mirror loss $src_loss =======
    s sLsr3 15.7386 n4 nsr5
    bs1 SR3 5e-05 4.5e-05 0 $a nsr5 nsr4 dump dump
    s sLsr2 11.1115 nsr4 nsr3
    bs1 SR2 0.0005 4.5e-05 0 $a nsr2 nsr3 POS dump
    s sLsr1 14.7412 nsr2 nsr1
    m1 SRM 0.3 4.5e-05 0 nsr1 AS


            

    
    

    ad fsb2_lower_ad_nTMSX $mfsb2 nTMSX
    ad fsb2_upper_ad_POP $fsb2 POP
    ad fsb2_upper_ad_nTMSY $fsb2 nTMSY
    ad fsb1_lower_ad_POS $mfsb1 POS
    ad fsb1_upper_ad_POP $fsb1 POP
    ad fsb2_lower_ad_POS $mfsb2 POS
    ad car_ad_nTMSY 0 nTMSY
    ad fsb1_lower_ad_nTMSX $mfsb1 nTMSX
    ad fsb2_lower_ad_REFL $mfsb2 REFL
    ad fsb2_upper_ad_REFL $fsb2 REFL
    ad fsb2_upper_ad_AS $fsb2 AS
    ad fsb2_lower_ad_AS $mfsb2 AS
    ad car_ad_AS 0 AS
    ad car_ad_REFL 0 REFL
    ad fsb1_upper_ad_nTMSY $fsb1 nTMSY
    ad car_ad_POS 0 POS
    ad fsb1_lower_ad_AS $mfsb1 AS
    ad fsb1_lower_ad_POP $mfsb1 POP
    ad fsb2_lower_ad_POP $mfsb2 POP
    ad fsb2_lower_ad_nTMSY $mfsb2 nTMSY
    ad fsb2_upper_ad_POS $fsb2 POS
    ad car_ad_POP 0 POP
    ad car_ad_nTMSX 0 nTMSX
    ad fsb1_upper_ad_nTMSX $fsb1 nTMSX
    ad fsb1_lower_ad_nTMSY $mfsb1 nTMSY
    ad fsb1_lower_ad_REFL $mfsb1 REFL
    ad fsb1_upper_ad_AS $fsb1 AS
    ad fsb2_upper_ad_nTMSX $fsb2 nTMSX
    ad fsb1_upper_ad_POS $fsb1 POS
    ad fsb1_upper_ad_REFL $fsb1 REFL
    
    """)
    return base



def model_HOM_DRFPMI():
    #
    # usage: base = utils_DRFPMI.model_DRFPMI()
    # output is the finesse structure with the DRFPMI configuration
    #
    #
    base = finesse.kat()
    base.verbose=False
    base.parse("""
    /*
    #ここの関数の中身はifo-modelのまま
    # ======== Constants ========================
    const f1 16.881M
    const f2 45.0159M
    const mf1 -16.881M
    const mf2 -45.0159M
    const a 0.686
    const phi_PRM 90
    const pi 3.1415
    const phi_SRM 90
    
    # ======== Input optics =====================
    l i1 1 0 n0
    s s_eo0 0 n0 n_eo1
    mod eom1 $f1 0.3 1 pm n_eo1 n_eo2
    s s_eo1 0 n_eo2 n_eo3
    mod eom2 $f2 0.3 1 pm n_eo3 n_eo4
    s s_eo2 0 n_eo4 nREFL

    # ======= PRC each mirror loss 45ppm =======
    # PRC
    m1 PRM 0.1 45e-6 $phi_PRM nREFL npr1
    s sLpr1 14.7615 npr1 npr2
    bs1 PR2 500e-6 45e-6 0 $a npr3 npr2 nPOP nPOP2
    s sLpr2 11.0661 npr3 npr4
    bs1 PR3 50e-6 45e-6 0 $a dump dump npr4 npr5
    s sLpr3 15.7638 npr5 npr6

    # ======= Michelson ========================
    bs bs1 0.5 0.5 0 45 npr6 n2 n3 n4
    s lx 26.4018 n3 nx1 #26.6649-thickness*1.754
    s ly 23.072 n2 ny1 #23.3351-thickness*1.754


    # ======== Thick ITMs ======================
    m IXAR 0     1     0 nx1 nx2
    s thick_IX 0.15 1.754 nx2 nx3
    m ITMX 0.996 0.004 0 nx3 nx4

    m IYAR 0     1     0 ny1 ny2
    s thick_IY 0.15 1.754 ny2 ny3
    m ITMY 0.996 0.004 90 ny3 ny4

    # ========== Arm     =======================
    s sx1 3000 nx4 nx5
    m ETMX 0.999995 5e-06 0 nx5 nTMSX

    s sy1 3000 ny4 ny5
    m ETMY 0.999995 5e-06 90 ny5 nTMSY


    # ========= SRC each mirror loss 45ppm =======
    s sLsr3 15.7386 n4 nsr5
    bs1 SR3 50e-6 45e-6 0 $a nsr5 nsr4 dump dump
    s sLsr2 11.1115 nsr4 nsr3
    bs1 SR2 500e-6 45e-6 0 $a nsr2 nsr3 nPOS dump
    s sLsr1 14.7412 nsr2 nsr1
    m1 SRM 0.3 0e-6 $phi_SRM nsr1 nAS

    ad CR_REFL 0 nREFL
    ad SB1p_REFL $f1 nREFL
    ad SB1m_REFL $mf1 nREFL
    ad SB2p_REFL $f2 nREFL
    ad SB2m_REFL $mf2 nREFL
    
    ad CR_POP 0 nPOP
    ad SB1p_POP $f1 nPOP
    ad SB1m_POP $mf1 nPOP
    ad SB2p_POP $f2 nPOP
    ad SB2m_POP $mf2 nPOP

    ad CR_TMSX   0 nTMSX
    ad SB1p_TMSX $f1 nTMSX
    ad SB1m_TMSX $mf1 nTMSX
    ad SB2p_TMSX $f2 nTMSX
    ad SB2m_TMSX $mf2 nTMSX

    ad CR_TMSY   0 nTMSY
    ad SB1p_TMSY $f1 nTMSY
    ad SB1m_TMSY $mf1 nTMSY
    ad SB2p_TMSY $f2 nTMSY
    ad SB2m_TMSY $mf2 nTMSY
    
    ad CR_POS 0 nPOS
    ad SB1p_POS $f1 nPOS
    ad SB1m_POS $mf1 nPOS
    ad SB2p_POS $f2 nPOS
    ad SB2m_POS $mf2 nPOS

    ad CR_AS 0 nAS
    ad SB1p_AS $f1 nAS
    ad SB1m_AS $mf1 nAS
    ad SB2p_AS $f2 nAS
    ad SB2m_AS $mf2 nAS
    
    */
    """)
    return base




def run_sweep(DoF, base):
    #
    # usage: model, out = utils_DRFPMI.run_sweep('CARM',base)
    # out: the computed signals, 
    # model: updated the finesse structire
    # model is with the sweep command, such as 'xaxis mirror phi lin -90 90 5000'
    #
    model = base.deepcopy()
    model.parse("""
    #ここの中身はGUI
    pd1 pd1_Iphase_fsb1_POS $fsb1 0.0 POS
    pd1 pd1_Qphase_fsb1_nTMSY $fsb1 90.0 nTMSY
    pd1 pd1_Iphase_fsb1_REFL $fsb1 0.0 REFL
    pd1 pd1_Iphase_fsb1_POP $fsb1 0.0 POP
    pd1 pd1_Qphase_fsb1_REFL $fsb1 90.0 REFL
    pd1 pd1_Iphase_fsb1_AS $fsb1 0.0 AS
    pd1 pd1_Qphase_fsb1_POS $fsb1 90.0 POS
    pd1 pd1_Iphase_fsb1_nTMSX $fsb1 0.0 nTMSX
    pd1 pd1_Qphase_fsb1_POP $fsb1 90.0 POP
    pd1 pd1_Qphase_fsb1_AS $fsb1 90.0 AS
    pd1 pd1_Iphase_fsb1_nTMSY $fsb1 0.0 nTMSY
    pd1 pd1_Qphase_fsb1_nTMSX $fsb1 90.0 nTMSX

    pd1 pd1_Iphase_fsb2_AS $fsb2 0.0 AS
    pd1 pd1_Qphase_fsb2_nTMSX $fsb2 90.0 nTMSX
    pd1 pd1_Iphase_fsb2_REFL $fsb2 0.0 REFL
    pd1 pd1_Iphase_fsb2_POP $fsb2 0.0 POP
    pd1 pd1_Qphase_fsb2_POP $fsb2 90.0 POP
    pd1 pd1_Iphase_fsb2_nTMSY $fsb2 0.0 nTMSY
    pd1 pd1_Iphase_fsb2_nTMSX $fsb2 0.0 nTMSX
    pd1 pd1_Iphase_fsb2_POS $fsb2 0.0 POS
    pd1 pd1_Qphase_fsb2_AS $fsb2 90.0 AS
    pd1 pd1_Qphase_fsb2_POS $fsb2 90.0 POS
    pd1 pd1_Qphase_fsb2_nTMSY $fsb2 90.0 nTMSY
    pd1 pd1_Qphase_fsb2_REFL $fsb2 90.0 REFL
    
    """)
    
    if DoF == "CARM":
        model.parse("""
        xaxis ETMX phi lin -180 180 5000
        put* ETMY phi $x1
        yaxis abs
        """)
    elif DoF == "DARM":
        model.parse("""
       
        xaxis ETMX phi lin -180 180 5000
        put* ETMY phi $mx1
        yaxis abs
        """)
    elif DoF == "MICH":
        model.parse("""
        var tuning 0
        # BS scan
        xaxis ITMX phi lin -180 180 5000
        put* ITMY phi $mx1
        put* ETMX phi $x1
        put* ETMY phi $mx1
        yaxis abs
        """)
    elif DoF == "PRCL":
        model.parse("""
        var tuning 0
        # PRM scan
        xaxis PRM phi lin -180 180 5000
        yaxis lin abs
        """)
    elif DoF == "SRCL":
        model.parse("""
        var tuning 0
        xaxis tuning phi lin -180 180 5000
        put SRM phi $x1
        """)
        
        
    out = model.run()
    return model, out


def run_fsig(DoF, base):
    model = base.deepcopy()
    model.parse("""
    
    const fsb1 16.881M
    const fsb2 45.0159M

    pd2 ASI1 $fsb1 0 10 nAS
    pd2 ASQ1 $fsb1 90 10 nAS
    pd2 REFLI1 $fsb1 0 10 nREFL
    pd2 REFLQ1 $fsb1 90 10 nREFL
    pd2 POPI1 $fsb1 0 10 nPOP
    pd2 POPQ1 $fsb1 90 10 nPOP
    pd2 POSI1 $fsb1 0 10 nPOS
    pd2 POSQ1 $fsb1 90 10 nPOS

    pd2 ASI2 $fsb2 0 10 nAS
    pd2 ASQ2 $fsb2 90 10 nAS
    pd2 REFLI2 $fsb2 0 10 nREFL
    pd2 REFLQ2 $fsb2 90 10 nREFL
    pd2 POPI2 $fsb2 0 10 nPOP
    pd2 POPQ2 $fsb2 90 10 nPOP
    pd2 POSI2 $fsb2 0 10 nPOS
    pd2 POSQ2 $fsb2 90 10 nPOS

    put ASI1 f2 $x1
    put ASQ1 f2 $x1
    put REFLI1 f2 $x1
    put REFLQ1 f2 $x1
    put POPI1 f2 $x1
    put POPQ1 f2 $x1
    put POSI1 f2 $x1
    put POSQ1 f2 $x1

    put ASI2 f2 $x1
    put ASQ2 f2 $x1
    put REFLI2 f2 $x1
    put REFLQ2 f2 $x1
    put POPI2 f2 $x1
    put POPQ2 f2 $x1
    put POSI2 f2 $x1
    put POSQ2 f2 $x1

    yaxis log abs:deg
    """)

###### choosing DoF ######

    if DoF == "CARM":
        model.parse("""
        const fstart 0.0005
        const fend 500
        fsig sig1 ETMX 10 0
        fsig sig1 ETMY 10 0
        xaxis sig1 f log $fstart $fend 1000
        """)
    elif DoF == "DARM":
        model.parse("""
        const fstart 0.0005
        const fend 500
        fsig sig1 ETMX 10 0
        fsig sig1 ETMY 10 180
        xaxis sig1 f log $fstart $fend 1000
        """)
    elif DoF == "MICH":
        model.parse("""
        const fstart 0.0005
        const fend 500
        fsig sig1 bs1 10 0
        xaxis sig1 f log $fstart $fend 1000
        """)
    elif DoF == "PRCL":
        model.parse("""
        const fstart 0.0005
        const fend 500
        fsig sig1 PRM 10 0
        xaxis sig1 f log $fstart $fend 1000
        """)    
    elif DoF == "SRCL":
        model.parse("""
        const fstart 0.0005
        const fend 500
        fsig sig1 SRM 10 0
        xaxis sig1 f log $fstart $fend 1000
        """)    
    else:
        print("Please specify a valid DoF")
    
    
    out = model.run()
    
    return model, out


def demod_phase(out, port, SB, N):
    #
    # usage: mag, phase = utils_DRFPMI.demod_phase(out, port, SB, N):
    # out: the computed signals from run_fsig
    # port: string, either 'REFL','AS','POP' or 'POS'
    # SB: string, either '1' or '2', indecating f1 or f2 demodulation
    # N: integer related to the frequency. Should be updated.
    #
    #
    sensI = port+"I"+SB
    sensQ = port+"Q"+SB
    I = np.sign(np.sin(np.angle(out[sensI][N])))* np.abs(out[sensI][N])
    Q = np.sign(np.sin(np.angle(out[sensQ][N])))* np.abs(out[sensQ][N])
    demod = np.arctan(Q/I)*180/np.pi
    mag = np.sqrt(I**2 + Q**2)
    
    return mag, demod


# In[ ]:




