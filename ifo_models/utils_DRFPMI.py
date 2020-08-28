import pykat
from pykat import finesse
import numpy as np

def model_DRFPMI():
    
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
    s sLsr3 15.7396 n4 nsr5
    bs1 SR3 50e-6 45e-6 0 $a nsr5 nsr4 dump dump
    s sLsr2 11.1115 nsr4 nsr3
    bs1 SR2 500e-6 45e-6 0 $a nsr2 nsr3 nPOS dump
    s sLsr1 14.7412 nsr2 nsr1
    m1 SRM 0.3 0e-6 0 nsr1 nAS

    ## ===== amplitude detectors =====

    ad CR_POP 0 nPOP
    ad SB1p_POP $f1 nPOP
    ad SB1m_POP $mf1 nPOP
    ad SB2p_POP $f2 nPOP
    ad SB2m_POP $mf2 nPOP

    ad CR_TMSX 0_TMSX nTMSX
    ad SB1p_TMSX $f1 nTMSX
    ad SB1m_TMSX $mf1 nTMSX
    ad SB2p_TMSX $f2 nTMSX
    ad SB2m_TMSX $mf2 nTMSX
    
    ad CR_POS 0 nPOS
    ad SB1p_POS $f1 nPOS
    ad SB1m_POS $mf1 nPOS
    ad SB2p_POS $f2 nPOS
    ad SB2m_POS $mf2 nPOS
    
    """)
    return base



def run_sweep(DoF, base):

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
        put bs1 phi $x1
        yaxis lin abs
        """)
    elif DoF == "PRCL":
        model.parse("""
        var tuning 0
        xaxis tuning phi lin -90 90 5000
        put PRM phi $x1
        yaxis lin abs
        """)
    elif DoF == "SRCL":
        model.parse("""
        var tuning 0
        xaxis tuning phi lin -90 90 5000
        put SRM phi $x1
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
    # Deriving the signal angle simply by arctan(Qsig/Isig) of a port
    #
    # port and SB should be string
    # SB is 1 or 2 for f1 or f2
    # out is the output of model.run()
    # N indicate a frequency, but currently it's just a number.
    #   should be properly treated in a near future
    #
    #
    sensI = port+"I"+SB
    sensQ = port+"Q"+SB
    I = np.sign(np.sin(np.angle(out[sensI][N])))* np.abs(out[sensI][N])
    Q = np.sign(np.sin(np.angle(out[sensQ][N])))* np.abs(out[sensQ][N])
    demod = np.arctan(Q/I)*180/np.pi
    mag = np.sqrt(I**2 + Q**2)
    
    return mag, demod
