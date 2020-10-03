import pykat
from pykat import finesse
import numpy as np

def model_DRMI():
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
    mod eom1 $f1 0.3 3 pm n_eo1 n_eo2
    s s_eo1 0 n_eo2 n_eo3
    mod eom2 $f2 0.3 3 pm n_eo3 n_eo4
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
    m ETMX 0 5e-06 0 nx3 nTMSX

    # Y arm
    m ITMY 0.996 0.004 90 ny1 ny2
    s sy1 3000 ny2 ny3
    m ETMY 0 5e-06 90 ny3 nTMSY


    # ========= SRC each mirror loss 45ppm =======
    s sLsr3 15.7396 n4 nsr5
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



