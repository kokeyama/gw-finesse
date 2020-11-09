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
    const f1 16.881M
    const f2 45.0159M
    const mf1 -16.881M
    const mf2 -45.0159M
    const a 0.686
    const pi 3.1415
    
    # ======== Input optics =====================
    l i1 1 0 n0
    s s_eo0 0 n0 n_eo1
    mod eom1 $f1 0.3 1 pm n_eo1 n_eo2
    s s_eo1 0 n_eo2 n_eo3
    mod eom2 $f2 0.3 1 pm n_eo3 n_eo4
    s s_eo2 0 n_eo4 nREFL

    ## ======= PRC each mirror loss 45ppm =======
    # PRC

    m1 PRM 0.1 45e-6 0 nREFL npr1
    s sLpr1 14.7615 npr1 npr2
    bs1 PR2 500e-6 45e-6 0 $a npr3 npr2 nPOP nPOP2
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
    m ETMX 0.999995 5e-06 0 nx3 nTMSX

    # Y arm
    m ITMY 0.996 0.004 90 ny1 ny2
    s sy1 3000 ny2 ny3
    m ETMY 0.999995 5e-06 90 ny3 nTMSY


    # ========= SRC each mirror loss 45ppm =======
    s sLsr3 15.7386 n4 nsr5
    bs1 SR3 50e-6 45e-6 0 $a nsr5 nsr4 dump dump
    s sLsr2 11.1115 nsr4 nsr3
    bs1 SR2 500e-6 45e-6 0 $a nsr2 nsr3 nPOS dump
    s sLsr1 14.7412 nsr2 nsr1
    m1 SRM 0.3 0e-6 0 nsr1 nAS

    ## ===== amplitude detectors =====
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

    ad CR_TMSX 0 nTMSX
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
    s lx 26.4018 n3 nx1		#26.6649-thickness*1.754
    s ly 23.072 n2 ny1		#23.3351-thickness*1.754


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

    cav XARM ITMX nx4 ETMX nx5
    cav YARM ITMY ny4 ETMY ny5
    cav PRX PRM npr1 ITMX nx3
    cav PRY PRM npr1 ITMY ny3
    cav SRX SRM nsr1 ITMX nx3
    cav SRY SRM nsr1 ITMY ny3
    
    # ===== amplitude detectors =====
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
    
    
    
    map ITMX ITMXhr.txt
    knm ITMX ITMXhr2
    conf ITMX save_knm_binary 1
    conf ITMX interpolation_method 2
    conf ITMX integration_method 1

    map ETMX ETMXhr.txt
    knm ETMX ETMXhr2
    conf ETMX save_knm_binary 1
    conf ETMX interpolation_method 2
    conf ETMX integration_method 1

    map ITMY ITMYhr.txt
    knm ITMY ITMYhr2
    conf ITMY save_knm_binary 1
    conf ITMY interpolation_method 2
    conf ITMY integration_method 1

    map ETMY ETMYhr.txt
    knm ETMY ETMYhr2
    conf ETMY save_knm_binary 1
    conf ETMY interpolation_method 2
    conf ETMY integration_method 1
    
    
    #===Apperture===
    map ITMX Apperture.txt
    knm ITMX ITMXabs2
    conf ITMX save_knm_binary 1
    conf ITMX interpolation_method 2
    conf ITMX integration_method 1
    
    

    map ETMX Apperture.txt
    knm ETMX ETMXabs2
    conf ETMX save_knm_binary 1
    conf ETMX interpolation_method 2
    conf ETMX integration_method 1
    
    map ITMY Apperture.txt
    knm ITMY ITMYabs2
    conf ITMY save_knm_binary 1
    conf ITMY interpolation_method 2
    conf ITMY integration_method 1

    map ETMY Apperture.txt
    knm ETMY ETMYabs2
    conf ETMY save_knm_binary 1
    conf ETMY interpolation_method 2
    conf ETMY integration_method 1

    
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
    const fsb1 16.881M
    const fsb2 45.0159M

    pd1 ASI1 $fsb1 0 nAS
    pd1 ASQ1 $fsb1 90 nAS
    pd1 REFLI1 $fsb1 0 nREFL
    pd1 REFLQ1 $fsb1 90 nREFL
    pd1 POPI1 $fsb1 0 nPOP
    pd1 POPQ1 $fsb1 90 nPOP
    pd1 POSI1 $fsb1 0 nPOS
    pd1 POSQ1 $fsb1 90 nPOS

    pd1 ASI2 $fsb2 0 nAS
    pd1 ASQ2 $fsb2 90 nAS
    pd1 REFLI2 $fsb2 0 nREFL
    pd1 REFLQ2 $fsb2 90 nREFL
    pd1 POPI2 $fsb2 0 nPOP
    pd1 POPQ2 $fsb2 90 nPOP
    pd1 POSI2 $fsb2 0 nPOS
    pd1 POSQ2 $fsb2 90 nPOS
    """)
    
    if DoF == "CARM":
        model.parse("""
        xaxis ETMX phi lin -90 90 5000
        put* ETMY phi $x1
        yaxis lin abs
        """)
    elif DoF == "DARM":
        model.parse("""
        xaxis ETMX phi lin -90 90 5000
        put* ETMY phi $mx1
        yaxis lin abs
        """)
    elif DoF == "MICH":
        model.parse("""
        var tuning 0
        xaxis tuning phi lin -90 90 5000
        put* ITMX phi $x1
        put* ETMX phi $x1
        put* ITMY phi $mx1
        put* ETMY phi $mx1
        yaxis lin abs
        """)
    elif DoF == "PRCL":
        model.parse("""
        var tuning 0
        xaxis* tuning phi lin -90 90 5000
        put* PRM phi $x1
        yaxis lin abs
        """)
    elif DoF == "SRCL":
        model.parse("""
        var tuning 0
        xaxis* tuning phi lin -90 90 5000
        put* SRM phi $x1
        yaxis lin abs
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
    pd2 TMSXI1 $fsb1 0 10 nTMSX
    pd2 TMSXQ1 $fsb1 90 10 nTMSX
    pd2 TMSYI1 $fsb1 0 10 nTMSY
    pd2 TMSYQ1 $fsb1 90 10 nTMSY
    pd2 TMSXI2 $fsb2 0 10 nTMSX
    pd2 TMSXQ2 $fsb2 90 10 nTMSX
    pd2 TMSYI2 $fsb2 0 10 nTMSY
    pd2 TMSYQ2 $fsb2 90 10 nTMSY

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
    put TMSXQ1 f2 $x1
    put TMSXI1 f2 $x1
    put TMSYQ1 f2 $x1
    put TMSYI1 f2 $x1
    put TMSXQ2 f2 $x1
    put TMSXI2 f2 $x1
    put TMSYQ2 f2 $x1
    put TMSYI2 f2 $x1

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
        fsig sig1 ETMX 10 0
        fsig sig1 ITMX 10 0
        fsig sig1 ETMY 10 180
        fsig sig1 ITMY 10 180
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
