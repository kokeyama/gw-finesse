
import pykat
from pykat import finesse
import numpy as np

def model_base(configuration):
    #
    # usage: base = utils_DRFPMI.model_DRFPMI()(修正)
    # output is the finesse structure with the DRFPMI configuration(修正)
    #
    #
    base = finesse.kat()
    base.verbose=True
    base.parse("""
    const fsb1 16.881M
    const fsb2 45.0159M
    const mfsb1 -16.881M
    const mfsb2 -45.0159M
    const a 0.686
    const pi 3.1415

    l i1 1.0 0.0 0.0 n0
    s s_eo0 0.0 n0 n_eo1
    mod eom1 16881000.0 0.3 3 pm 0.0 n_eo1 n_eo2
    s s_eo1 0.0 n_eo2 n_eo3
    mod eom2 45015900.0 0.3 3 pm 0.0 n_eo3 n_eo4
    s s_eo2 0.0 n_eo4 REFL
    

    ad car_ad_REFL 0 REFL
    ad fsb1_upper_ad_REFL 16881000.0 REFL
    ad fsb1_lower_ad_REFL -16881000.0 REFL
    ad fsb2_upper_ad_REFL 45015900.0 REFL
    ad fsb2_lower_ad_REFL -45015900.0 REFL
    ad car_ad_AS 0 AS
    ad fsb1_upper_ad_AS 16881000.0 AS
    ad fsb1_lower_ad_AS -16881000.0 AS
    ad fsb2_upper_ad_AS 45015900.0 AS
    ad fsb2_lower_ad_AS -45015900.0 AS
    ad car_ad_TMSX 0 TMSX
    ad fsb1_upper_ad_TMSX 16881000.0 TMSX
    ad fsb1_lower_ad_TMSX -16881000.0 TMSX
    ad fsb2_upper_ad_TMSX 45015900.0 TMSX
    ad fsb2_lower_ad_TMSX -45015900.0 TMSX
    ad car_ad_TMSY 0 TMSY
    ad fsb1_upper_ad_TMSY 16881000.0 TMSY
    ad fsb1_lower_ad_TMSY -16881000.0 TMSY
    ad fsb2_upper_ad_TMSY 45015900.0 TMSY
    ad fsb2_lower_ad_TMSY -45015900.0 TMSY
    ad car_ad_POP 0 POP
    ad fsb1_upper_ad_POP 16881000.0 POP
    ad fsb1_lower_ad_POP -16881000.0 POP
    ad fsb2_upper_ad_POP 45015900.0 POP
    ad fsb2_lower_ad_POP -45015900.0 POP
    ad car_ad_POS 0 POS
    ad fsb1_upper_ad_POS 16881000.0 POS
    ad fsb1_lower_ad_POS -16881000.0 POS
    ad fsb2_upper_ad_POS 45015900.0 POS
    ad fsb2_lower_ad_POS -45015900.0 POS
    
    """)
    if configuration == "MI":
        base.parse("""
        m PRM 0.0 1.0 0.0 REFL npr1
        s sLpr1 0.0 npr1 npr2
        bs PR2 1.0 0.0 0.0 0.686 npr3 npr2 POP POP2
        s sLpr2 0.0 npr3 npr4
        bs PR3 1.0 0.0 0.0 0.686 dump dump npr4 npr5
        s sLpr3 0.0 npr5 npr6
        bs bs1 0.5 0.5 0.0 45.0 npr6 n2 n3 n4
        s lx 26.6649 n3 nx1
        s ly 23.3351 n2 ny1
        m ITMX 0.995955 0.004 0.0 nx1 nx2
        s sx1 3000.0 nx2 nx3
        m ETMX 0.0 0.0 0.0 nx3 TMSX
        m ITMY 0.995955 0.004 90.0 ny1 ny2
        s sy1 3000.0 ny2 ny3
        m ETMY 0.0 0.0 90.0 ny3 TMSY
        s sLsr3 0.0 n4 nsr5
        bs SR3 1.0 0.0 0.0 0.686 nsr5 nsr4 dump dump
        s sLsr2 0.0 nsr4 nsr3
        bs SR2 1.0 0.0 0.0 0.686 nsr2 nsr3 POS dump
        s sLsr1 0.0 nsr2 nsr1
        m SRM 0.0 1.0 0.0 nsr1 AS
        """)
    elif configuration == "FPMI":
        base.parse("""
        m PRM 0.0 1.0 0.0 REFL npr1
        s sLpr1 0.0 npr1 npr2
        bs PR2 1.0 0.0 0.0 0.686 npr3 npr2 POP POP2
        s sLpr2 0.0 npr3 npr4
        bs PR3 1.0 0.0 0.0 0.686 dump dump npr4 npr5
        s sLpr3 0.0 npr5 npr6
        bs bs1 0.5 0.5 0.0 45.0 npr6 n2 n3 n4
        s lx 26.6649 n3 nx1
        s ly 23.3351 n2 ny1
        m ITMX 0.995955 0.004 0.0 nx1 nx2
        s sx1 3000.0 nx2 nx3
        m ETMX 0.99995 5e-06 0.0 nx3 TMSX
        m ITMY 0.995955 0.004 90.0 ny1 ny2
        s sy1 3000.0 ny2 ny3
        m ETMY 0.99995 5e-06 90.0 ny3 TMSY
        s sLsr3 0.0 n4 nsr5
        bs SR3 1.0 0.0 0.0 0.686 nsr5 nsr4 dump dump
        s sLsr2 0.0 nsr4 nsr3
        bs SR2 1.0 0.0 0.0 0.686 nsr2 nsr3 POS dump
        s sLsr1 0.0 nsr2 nsr1
        m SRM 0.0 1.0 0.0 nsr1 AS
        
        """)
    elif configuration == "PRFPMI":
        base.parse("""
        m PRM 0.8999550000000001 0.1 0.0 REFL npr1
        s sLpr1 14.7615 npr1 npr2
        bs PR2 0.9994550000000001 0.0005 0.0 0.686 npr3 npr2 POP POP2
        s sLpr2 11.0661 npr3 npr4
        bs PR3 0.999905 5e-05 0.0 0.686 dump dump npr4 npr5
        s sLpr3 15.7638 npr5 npr6
        bs bs1 0.5 0.5 0.0 45.0 npr6 n2 n3 n4
        s lx 26.6649 n3 nx1
        s ly 23.3351 n2 ny1
        m ITMX 0.995955 0.004 0.0 nx1 nx2
        s sx1 3000.0 nx2 nx3
        m ETMX 0.99995 5e-06 0.0 nx3 TMSX
        m ITMY 0.995955 0.004 90.0 ny1 ny2
        s sy1 3000.0 ny2 ny3
        m ETMY 0.99995 5e-06 90.0 ny3 TMSY
        s sLsr3 0.0 n4 nsr5
        bs SR3 1.0 0.0 0.0 0.686 nsr5 nsr4 dump dump
        s sLsr2 0.0 nsr4 nsr3
        bs SR2 1.0 0.0 0.0 0.686 nsr2 nsr3 POS dump
        s sLsr1 0.0 nsr2 nsr1
        m SRM 0.0 1.0 0.0 nsr1 AS
        
        """)
    elif configuration == "DRFPMI":
        base.parse("""
        m PRM 0.8999550000000001 0.1 0.0 REFL npr1
        s sLpr1 14.7615 npr1 npr2
        bs PR2 0.9994550000000001 0.0005 0.0 0.686 npr3 npr2 POP POP2
        s sLpr2 11.0661 npr3 npr4
        bs PR3 0.999905 5e-05 0.0 0.686 dump dump npr4 npr5
        s sLpr3 15.7638 npr5 npr6
        bs bs1 0.5 0.5 0.0 45.0 npr6 n2 n3 n4
        s lx 26.6649 n3 nx1
        s ly 23.3351 n2 ny1
        m ITMX 0.995955 0.004 0.0 nx1 nx2
        s sx1 3000.0 nx2 nx3
        m ETMX 0.99995 5e-06 0.0 nx3 TMSX
        m ITMY 0.995955 0.004 90.0 ny1 ny2
        s sy1 3000.0 ny2 ny3
        m ETMY 0.99995 5e-06 90.0 ny3 TMSY
        s sLsr3 14.7412 n4 nsr5
        bs SR3 0.999905 5e-05 0.0 0.686 nsr5 nsr4 dump dump
        s sLsr2 11.1115 nsr4 nsr3
        bs SR2 0.9994550000000001 0.0005 0.0 0.686 nsr2 nsr3 POS dump
        s sLsr1 15.7386 nsr2 nsr1
        m SRM 0.8463550000000001 0.1536 0.0 nsr1 AS
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
    not made script
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
    
    #=====I phase=====
    pd1 pd1_fsb1_0_REFL 16881000.0 0.0 REFL
    pd1 pd1_fsb1_0_AS 16881000.0 0.0 AS
    pd1 pd1_fsb1_0_TMSX 16881000.0 0.0 TMSX
    pd1 pd1_fsb1_0_TMSY 16881000.0 0.0 TMSY
    pd1 pd1_fsb1_0_POP 16881000.0 0.0 POP
    pd1 pd1_fsb2_0_REFL 45015900.0 0.0 REFL
    pd1 pd1_fsb2_0_AS 45015900.0 0.0 AS
    pd1 pd1_fsb2_0_TMSX 45015900.0 0.0 TMSX
    pd1 pd1_fsb2_0_TMSY 45015900.0 0.0 TMSY
    pd1 pd1_fsb2_0_POP 45015900.0 0.0 POP
    
    #=====Q phase=====
    pd1 pd1_fsb1_90_REFL 16881000.0 90.0 REFL
    pd1 pd1_fsb1_90_AS 16881000.0 90.0 AS
    pd1 pd1_fsb1_90_TMSX 16881000.0 90.0 TMSX
    pd1 pd1_fsb1_90_TMSY 16881000.0 90.0 TMSY
    pd1 pd1_fsb1_90_POP 16881000.0 90.0 POP
    pd1 pd1_fsb2_90_REFL 45015900.0 90.0 REFL
    pd1 pd1_fsb2_90_AS 45015900.0 90.0 AS
    pd1 pd1_fsb2_90_TMSX 45015900.0 90.0 TMSX
    pd1 pd1_fsb2_90_TMSY 45015900.0 90.0 TMSY
    pd1 pd1_fsb2_90_POP 45015900.0 90.0 POP
    yaxis abs
    """)
    
    if DoF == "CARM":
        model.parse("""
        xaxis ETMX phi lin -180 180 1000
        put* ETMY phi $x1
        """)
    elif DoF == "DARM":
        model.parse("""
        xaxis ETMX phi lin -180 180 1000
        put* ETMY phi $mx1
        
        """)
    elif DoF == "MICH":
        model.parse("""
        xaxis ITMX phi lin -180 180 1000
        put* ETMX phi $x1
        put* ITMY phi $mx1
        put* ETMY phi $mx1
        """)
    elif DoF == "PRCL":
        model.parse("""
        xaxis PRM phi lin -180 180 1000
        """)
    elif DoF == "SRCL":
        model.parse("""
        var tuning 0.0
        xaxis tuning phi lin -180 180 1000
        put SRM phi $x1
        """)
    
 
        
        
    out = model.run()
    return model, out


def run_fsig(DoF, base):
    model = base.deepcopy()
    model.parse("""
    
    # ======== Constants ========================
    const f1 16881000.0
    const f2 45015900.0S
    
    put pd2_fsb1_0_REFL f2 $x1
    put pd2_fsb1_90_REFL f2 $x1
    put pd2_fsb2_0_REFL f2 $x1
    put pd2_fsb2_90_REFL f2 $x1
    
    put pd2_fsb1_0_AS f2 $x1
    put pd2_fsb1_90_AS f2 $x1
    put pd2_fsb2_0_AS f2 $x1
    put pd2_fsb2_90_AS f2 $x1
    
    put pd2_fsb1_0_TMSX f2 $x1
    put pd2_fsb1_90_TMSX f2 $x1
    put pd2_fsb2_0_TMSX f2 $x1
    put pd2_fsb2_90_TMSX f2 $x1
    
    put pd2_fsb1_0_TMSY f2 $x1
    put pd2_fsb1_90_TMSY f2 $x1
    put pd2_fsb2_0_TMSY f2 $x1
    put pd2_fsb2_90_TMSY f2 $x1

    put pd2_fsb1_0_POP f2 $x1
    put pd2_fsb1_90_POP f2 $x1
    put pd2_fsb2_0_POP f2 $x1
    put pd2_fsb2_90_POP f2 $x1

    put pd2_fsb1_0_POS f2 $x1
    put pd2_fsb1_90_POS f2 $x1
    put pd2_fsb2_0_POS f2 $x1
    put pd2_fsb2_90_POS f2 $x1

    pd2 pd2_fsb1_0_REFL 16881000.0 0.0 10.0 REFL
    pd2 pd2_fsb1_90_REFL 16881000.0 90.0 10.0 REFL
    pd2 pd2_fsb2_0_REFL 45015900.0 0.0 10.0 REFL
    pd2 pd2_fsb2_90_REFL 45015900.0 90.0 10.0 REFL
    
    pd2 pd2_fsb1_0_AS 16881000.0 0.0 10.0 AS
    pd2 pd2_fsb1_90_AS 16881000.0 90.0 10.0 AS
    pd2 pd2_fsb2_0_AS 45015900.0 0.0 10.0 AS
    pd2 pd2_fsb2_90_AS 45015900.0 90.0 10.0 AS
    pd2 pd2_fsb1_0_TMSX 16881000.0 0.0 10.0 TMSX
    pd2 pd2_fsb1_90_TMSX 16881000.0 90.0 10.0 TMSX
    pd2 pd2_fsb2_0_TMSX 45015900.0 0.0 10.0 TMSX
    pd2 pd2_fsb2_90_TMSX 45015900.0 90.0 10.0 TMSX
    pd2 pd2_fsb1_0_TMSY 16881000.0 0.0 10.0 TMSY
    pd2 pd2_fsb1_90_TMSY 16881000.0 90.0 10.0 TMSY
    pd2 pd2_fsb2_0_TMSY 45015900.0 0.0 10.0 TMSY
    pd2 pd2_fsb2_90_TMSY 45015900.0 90.0 10.0 TMSY
    pd2 pd2_fsb1_0_POP 16881000.0 0.0 10.0 POP
    pd2 pd2_fsb1_90_POP 16881000.0 90.0 10.0 POP
    pd2 pd2_fsb2_0_POP 45015900.0 0.0 10.0 POP
    pd2 pd2_fsb2_90_POP 45015900.0 90.0 10.0 POP

 
    pd2 pd2_fsb1_0_POS 16881000.0 0.0 10.0 POS
    pd2 pd2_fsb1_90_POS 16881000.0 90.0 10.0 POS
    pd2 pd2_fsb2_0_POS 45015900.0 0.0 10.0 POS
    pd2 pd2_fsb2_90_POS 45015900.0 90.0 10.0 POS

    yaxis log abs:deg
    """)

###### choosing DoF ######

    if DoF == "CARM":
        model.parse("""
        fsig sig1 ETMX phase 10.0 0.0 
        fsig sig1 ETMY phase 10.0 0.0 
        xaxis sig1 f lin -180 180 1000
        """)
    elif DoF == "DARM":
        model.parse("""
        xaxis sig1 f lin -180 180 1000
        fsig sig1 ETMX phase 10.0 0.0 
        fsig sig1 ETMY phase 10.0 180.0 
        """)
    elif DoF == "MICH":
        model.parse("""
        xaxis sig1 f lin -180 180 1000
        fsig sig1 ETMX phase 10.0 0.0 
        fsig sig1 ITMX phase 10.0 0.0 
        fsig sig1 ETMY phase 10.0 180.0 
        fsig sig1 ITMY phase 10.0 180.0 
        """)
    elif DoF == "PRCL":
        model.parse("""
        xaxis sig1 f lin -180 180 1000
        fsig sig1 PRM phase 1.0 0.0 
        """)
    elif DoF == "SRCL":
        model.parse("""
        xaxis sig1 f lin -180 180 1000
        fsig sig1 SRM phase 1.0 0.0 
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





# %%
