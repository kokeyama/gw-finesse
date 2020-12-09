import pykat
from pykat import finesse
import numpy as np

def model_base():
    #
    # usage: base = utils_DRFPMI.model_DRFPMI()
    # output is the finesse structure with the DRFPMI configuration
    #
    #
    base = finesse.kat()
    base.verbose=True
    base.parse("""
        

    # ======== Constants ========================
    const f1 16.881M
    const f2 45.0159M
    const mf1 -16.881M
    const mf2 -45.0159M
    const a 0.686
    const pi 3.1415
    const fsb1 16.881M
    const fsb2 45.0159M



    # ======== Input optics =====================
    l i1 1 0 n0
    s s_eo0 0 n0 n_eo1
    mod eom1 $f1 0.3 1 pm n_eo1 n_eo2
    s s_eo1 0 n_eo2 n_eo3
    mod eom2 $f2 0.3 1 pm n_eo3 n_eo4
    s s_eo2 0 n_eo4 nREFL

    # Michelson
    bs bs1 0.5 0.5 0 45 nREFL n2 n3 nAS
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
    #### ===== amplitude detectors =====

    ad CR_REFL 0 nREFL
    ad SB1p_REFL $f1 nREFL
    ad SB1m_REFL $mf1 nREFL
    ad SB2p_REFL $f2 nREFL
    ad SB2m_REFL $mf2 nREFL

    ad CR_AS 0 nAS
    ad SB1p_AS $f1 nAS
    ad SB1m_AS $mf1 nAS
    ad SB2p_AS $f2 nAS
    ad SB2m_AS $mf2 nAS


    ad CR_TMSX 0 nTMSX
    ad SB1p_TMSX $f1 nTMSX
    ad SB1m_TMSX $mf1 nTMSX
    ad SB2p_TMSX $f2 nTMSX
    ad SB2m_TMSX $mf2 nTMSX

    ad CR_TMSY 0 nTMSY
    ad SB1p_TMSY $f1 nTMSY
    ad SB1m_TMSY $mf1 nTMSY
    ad SB2p_TMSY $f2 nTMSY
    ad SB2m_TMSY $mf2 nTMSY


    #### ===== dumodulated signal =====
    pd1 pd1_ASI1 $f1 0 nAS
    pd1 pd1_ASQ1 $f1 90 nAS
    pd1 pd1_REFLI1 $f1 0 nREFL
    pd1 pd1_REFLQ1 $f1 90 nREFL
    pd1 pd1_TMSXI1 $f1 0 nTMSX
    pd1 pd1_TMSXQ1 $f1 90 nTMSX
    pd1 pd1_TMSYI1 $f1 0 nTMSY
    pd1 pd1_TMSYQ1 $f1 90 nTMSY
    pd1 pd1_ASI2 $f2 0 nAS
    pd1 pd1_ASQ2 $f2 90 nAS
    pd1 pd1_REFLI2 $f2 0 nREFL
    pd1 pd1_REFLQ2 $f2 90 nREFL
    pd1 pd1_TMSXI2 $f2 0 nTMSX
    pd1 pd1_TMSXQ2 $f2 90 nTMSX
    pd1 pd1_TMSYI2 $f2 0 nTMSY
    pd1 pd1_TMSYQ2 $f2 90 nTMSY


    #### ===== transfer function  =====


    pd2 pd1_ASI1 $fsb1 0 10 nAS
    pd2 pd2_ASQ1 $fsb1 90 10 nAS
    pd2 pd2_REFLI1 $fsb1 0 10 nREFL
    pd2 pd2_REFLQ1 $fsb1 90 10 nREFL
    pd2 pd2_ASI2 $fsb2 0 10 nAS
    pd2 pd2_ASQ2 $fsb2 90 10 nAS
    pd2 pd2_REFLI2 $fsb2 0 10 nREFL
    pd2 pd2_REFLQ2 $fsb2 90 10 nREFL

    pd2 pd2_TMSXI1 $fsb1 0 10 nTMSX
    pd2 pd2_TMSXQ1 $fsb1 90 10 nTMSX
    pd2 pd2_TMSYI1 $fsb1 0 10 nTMSY
    pd2 pd2_TMSYQ1 $fsb1 90 10 nTMSY
    pd2 pd2_TMSXI2 $fsb2 0 10 nTMSX
    pd2 pd2_TMSXQ2 $fsb2 90 10 nTMSX
    pd2 pd2_TMSYI2 $fsb2 0 10 nTMSY
    pd2 pd2_TMSYQ2 $fsb2 90 10 nTMSY

    put pd2_ASI1 f2 $x1
    put pd2_ASQ1 f2 $x1
    put pd2_REFLI1 f2 $x1
    put pd2_REFLQ1 f2 $x1

    put pd2_ASI2 f2 $x1
    put pd2_ASQ2 f2 $x1
    put pd2_REFLI2 f2 $x1
    put pd2_REFLQ2 f2 $x1

    put pd2_TMSXQ1 f2 $x1
    put pd2_TMSXI1 f2 $x1
    put pd2_TMSYQ1 f2 $x1
    put pd2_TMSYI1 f2 $x1

    put pd2_TMSXQ2 f2 $x1
    put pd2_TMSXI2 f2 $x1

    put pd2_TMSYQ2 f2 $x1
    put pd2_TMSYI2 f2 $x1



    """)

 
    return base



def model_HOM_PRFPMI():
    #
    # usage: base = utils_DRFPMI.model_DRFPMI()
    # output is the finesse structure with the DRFPMI configuration
    #
    #
    base = finesse.kat()
    base.verbose=False
    base.parse("""
    
    # not made script
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

    yaxis lin abs
    """)
    
    if DoF == "CARM":
        model.parse("""
        xaxis* ETMX phi lin -180 180 5000
        put* ETMY phi $x1
        """)
    elif DoF == "DARM":
        model.parse("""
        xaxis ETMX phi lin -180 180 5000
        put* ETMY phi $mx1
        """)
    elif DoF == "MICH":
        model.parse("""
        var tuning 0
        xaxis* tuning phi lin -180 180 5000
        put* ITMX phi $x1
        put* ITMY phi $mx1
        put* ETMX phi $x1
        put* ETMY phi $mx1
        """)
    else:
        print("Please specify a valid DoF")
        
        
    out = model.run()
    return model, out


def run_fsig(DoF, base):
    model = base.deepcopy()
    model.parse("""
    const fstart -180
    const fend 180
    yaxis log abs:deg
    """)

###### choosing DoF ######

    if DoF == "CARM":
        model.parse("""
        fsig sig1 ETMX 10 0
        fsig sig1 ETMY 10 0
        xaxis sig1 f log $fstart $fend 1000
        """)
    elif DoF == "DARM":
        model.parse("""
        fsig sig1 ETMX 10 0
        fsig sig1 ETMY 10 180
        xaxis sig1 f log $fstart $fend 1000
        """)
    elif DoF == "MICH":
        model.parse("""
        fsig sig1 ETMX 10 0
        fsig sig2 ITMX 10 0
        fsig sig3 ETMY 10 180
        fsig sig4 ITMY 10 180
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
