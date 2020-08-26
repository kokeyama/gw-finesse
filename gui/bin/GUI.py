#!/usr/bin/env python
# coding: utf-8
import PySimpleGUI as sg    
from pykat import finesse
from pykat.commands import * 
import pykat
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import sys
import math
pykat.init_pykat_plotting(dpi=90)

sg.theme('Default1')

def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))


# In[7]:


# isscan = 
# isdemod_once =


# In[8]:


def generate_kat_FPMI(dic_fpmi_ispds, dic_fpmi_advanced_setting):

    ###############################
    ### get variables from GUI ###
    
    ### Optic ###
    laser_power = dic_fpmi_advanced_setting["laser_power"]#source laser power
    
    ### DoF ###
    dof = dic_fpmi_advanced_setting["dof"]#CARM DARM BS
    
    ### scan/demod/double demod ###
    isscan = dic_fpmi_advanced_setting["isscan"]
    isdemod_once = dic_fpmi_advanced_setting["isdemod_once"]
    istransfunc = dic_fpmi_advanced_setting["istransfunc"]
    
    ###
    x_plotscale = dic_fpmi_advanced_setting["x_plotscale"]
    xaxis_range_beg = dic_fpmi_advanced_setting["xaxis_range_beg"]
    xaxis_range_end = dic_fpmi_advanced_setting["xaxis_range_end"]
    y_plotscale = dic_fpmi_advanced_setting["y_plotscale"]
    #yaxis_range_beg = dic_fpmi_advanced_setting["yaxis_range_beg"]
    #yaxis_range_end = dic_fpmi_advanced_setting["yaxis_range_end"]
    samplingnum = dic_fpmi_advanced_setting["samplingnum"]

    ## pd1 advanced setting
    demod_phase_I = str(0+float(dic_fpmi_advanced_setting["demod_phase"]))
    demod_phase_Q = str(90+float(dic_fpmi_advanced_setting["demod_phase"]))
    ## pd2 advanced setting
    #if(istransfunc):
    pd2_mixer1_demodfreq = dic_fpmi_advanced_setting["pd2_mixer1_demodfreq"]
    
    ###############################

    ### INF components ###
    #
    # Prepare common (fixed for KAGRA) setting for kat file 
    # 
    input_finesse = """
### FPMI

const f1_SB 16.881M
const f2_SB 45.0159M

# Input optics
l i1 %s 0 n0
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
m ETMX 0.99995 5e-06 0 nx3 nxtrans

# Y arm
m ITMY 0.996 0.004 90 ny1 ny2
s sy1 3000 ny2 ny3
m ETMY 0.99995 5e-06 90 ny3 nytrans

    """ % (laser_power)

    ### PDs location ###
    
    # demod_num
    # demod_phase #slider?
    pd0s_code = ""
    pd1s_code = ""
    pd2s_code = ""

    for key in dic_fpmi_ispds.keys():
        if dic_fpmi_ispds[key] == True:
            pd0s_code_add = """
pd0 pd0_%s_I %s
pd0 pd0_%s_Q %s
            """% (key,key,
                  key,key,
                  )
            pd0s_code = pd0s_code + pd0s_code_add # input finesse ni tyokusetu tasu
 
            pd1s_code_add = """
pd1 pd1_%s_I1 $f1_SB %s %s
pd1 pd1_%s_Q1 $f1_SB %s %s
pd1 pd1_%s_I2 $f2_SB %s %s
pd1 pd1_%s_Q2 $f2_SB %s %s
            """% (key, demod_phase_I, key,
                  key, demod_phase_Q, key,
                  key, demod_phase_I, key,
                  key, demod_phase_Q, key)
            pd1s_code = pd1s_code + pd1s_code_add
        
            pd2s_code_add ="""
pd2 pd2_%s_I $f1_SB %s 10 %s
put pd2_%s_I f2 $x1
pd2 pd2_%s_Q $f1_SB 0 10 %s
put pd2_%s_Q f2 $x1
            """% (key,pd2_mixer1_demodfreq,key,
                  key,
                  key,key,
                  key)
            pd2s_code = pd2s_code + pd2s_code_add
            
    input_finesse += pd0s_code+pd1s_code+pd2s_code
    
    #+pd2s_code
    
    if(istransfunc==True):
        
        ### DoF ###
        if(dof=="DARM"):
            darm_sweep = """
## DARM ###
fsig sig1 ETMX 10 0
fsig sig1 ETMY 10 180
xaxis sig1 f log %s %s %s
yaxis lin abs:deg
            """ % (xaxis_range_beg, xaxis_range_end, samplingnum)
            input_finesse = input_finesse + darm_sweep

        elif(dof=="CARM"):
            carm_sweep = """
fsig sig1 ETMX 10 0
fsig sig1 ETMY 10 0
xaxis sig1 f log %s %s %s
yaxis lin abs:deg
            """ % (xaxis_range_beg, xaxis_range_end, samplingnum)
            input_finesse = input_finesse + carm_sweep

        elif(dof=="BS"):
            bs_sweep = """
fsig sig1 ETMX 10 0
fsig sig1 ITMX 10 0
fsig sig1 ETMY 10 180
fsig sig1 ITMY 10 180
xaxis sig1 f log %s %s %s
yaxis lin abs
            """ % (xaxis_range_beg, xaxis_range_end, samplingnum)
            input_finesse = input_finesse + bs_sweep
        else:
            pass
    if(istransfunc==False):
      
        ### DoF ###

        if(dof=="DARM"):
            darm_sweep = """
# DARM scan
xaxis ETMX phi lin %s %s %s
put* ETMY phi $mx1
yaxis abs
            """ % (xaxis_range_beg,xaxis_range_end, samplingnum)
            input_finesse = input_finesse + darm_sweep

        elif(dof=="CARM"):
            carm_sweep = """
# CARM scan
#(koyama) xaxis*
#initial
# m ITMX 0.996 0.004 0 nx1 nx2
xaxis ETMX phi lin %s %s %s
put* ETMY phi $x1
yaxis abs
            """ % (xaxis_range_beg,xaxis_range_end, samplingnum)
            input_finesse = input_finesse + carm_sweep

        elif(dof=="BS"):
            bs_sweep = """
# BS scan
#
#(koyama) original vergion og kokeyamasan uses xaxis*
# select xaxis plotscale "log" cause an error with xaxis*
# m ITMX 0.996 0.004 0 nx1 nx2 
# since the config are above, I think it doesnt cause any problem about the correctness of the result
# 

xaxis ITMX phi lin %s %s %s
put* ITMY phi $mx1
put* ETMX phi $x1
put* ETMY phi $mx1
yaxis abs
            """ % (xaxis_range_beg,xaxis_range_end, samplingnum)
            input_finesse = input_finesse + bs_sweep
        else:
            pass

    code = input_finesse
    print(code)
    return code


# In[9]:


##################################    
#section setting pd0/pd1/pd2
##################################
fpmi_section_pd0 = [

            ]

fpmi_section_pd1 = [
            [sg.Text('Which phase to plot?')],
            [sg.Checkbox('I1(in_phase f1)', size=(20, 1), key='plot_in_phase_f1'),
            sg.Checkbox('Q1(quadrature_phase f1)', size=(20, 1), key='plot_quadrature_phase_f1'),
            sg.Checkbox('I2(in_phase f2)', size=(20, 1), key='plot_in_phase_f2'),
            sg.Checkbox('Q2(quadrature_phase f2)', size=(20, 1), key='plot_quadrature_phase_f2')],
            [sg.Text('Demodulation_phase'),sg.Input(key='demod_phase', default_text='0', enable_events=True)],
]

fpmi_section_pd2 = [
                [sg.Text('mixer1 demodulation freq (ex)0, 100, max)')],
                 [sg.Input(key='pd2_mixer1_demodfreq', default_text='0', enable_events=True)]
]
fpmi_section_how_simulate = [
            [sg.Radio('Power(pd0)', "RADIO1", default=True, size=(10,1), key='isscan', enable_events=True),
             sg.Radio('Demod_once(pd1)',"RADIO1", default=False, size=(10,1), key='isdemod_once', enable_events=True)],
            ### pd0_setting_section
            [collapse(fpmi_section_pd0, 'pd0_setting_section')],
            ### pd1_settnig_section
            [collapse(fpmi_section_pd1, 'pd1_setting_section')]
            ]

##################################    
#TAB select FPMI/PRFPMI/DRFPMI
##################################
tab1_layout =  [
                ]
#FPMI_tab
tab2_layout = [
                [sg.Image("./Fabry_Perot_MI_eom_drawing.png", key="imageContainer", size=(800,600))],#size=(800,600)
                ### RADIO BOX pd0/pd1/pd2
                [sg.Radio('Sweep', "HOW_SIMULATE01", default=True, size=(10,1), key='issweep', enable_events=True),
                 sg.Radio('Transfer', "HOW_SIMULATE01", default=False, size=(10,1), key='istransfunc', enable_events=True)],
                ### RADIO BOX pd0/pd1/pd2
                [collapse(fpmi_section_how_simulate, 'fpmi_section_how_simulate')],
                ### pd2_setting_section
                [collapse(fpmi_section_pd2, 'pd2_setting_section')],
                [sg.Text('DoF'),sg.Combo(('DARM', 'CARM', 'BS'),default_value='DARM', size=(20, 1),key='dof')], #RADIOBOXに変える
                ## PDs checkbox
                [sg.Text('check PDs')],
                [sg.Checkbox('REFL', size=(5, 1), default=True, key='n1'),sg.Checkbox('AS', size=(5, 1),default=True, key='n4'),
                sg.Checkbox('nytrans', size=(5, 1), default=True,key='nytrans'),sg.Checkbox('nxtrans', size=(5, 1), default=True, key='nxtrans')],
                [sg.Checkbox('n2', size=(5, 1), key='n2'),sg.Checkbox('n3', size=(5, 1), key='n3'),
                sg.Checkbox('ny1', size=(5, 1), key='ny1'),sg.Checkbox('nx1', size=(5, 1), key='nx1'),
                sg.Checkbox('ny2', size=(5, 1), key='ny2'),sg.Checkbox('nx2', size=(5, 1), key='nx2'),
                sg.Checkbox('ny3', size=(5, 1), key='ny3'),sg.Checkbox('nx3', size=(5, 1), key='nx3'),
                ],
                #other settings
                [sg.Text('laser_power [W]'), sg.Input(key='laser_power', default_text='1')],
                #
                #
                [sg.Button('Plot', button_color=('white', 'black'), key='event_FPMI')],
                ]

layout = [
            [sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('FPMI_TAB', tab2_layout)]])],
            ### xaxis range
            [sg.Text('sweep range'), sg.Input(key='xaxis_range_beg', default_text='-180', enable_events=True),
            sg.Text("to"), sg.Input(key='xaxis_range_end', default_text='180', enable_events=True)],
            [sg.Radio("xaxis lin", "x_plotscale", default=True, size=(10,1), key='xaxis_lin', enable_events=True),
            sg.Radio('xaxis log',"x_plotscale", default=False, size=(10,1), key='xaxis_log', enable_events=True)],
            ### yaxis range
            [sg.Radio("yaxis lin", "y_plotscale", default=True, size=(10,1), key='yaxis_lin', enable_events=True),
            sg.Radio('yaxis log',"y_plotscale", default=False, size=(10,1), key='yaxis_log', enable_events=True)],
            [sg.Text('sampling num'), sg.Input(key='samplingnum', default_text='500', enable_events=True)],
            [sg.Text('Which data you output?')],
            [sg.Checkbox('kat file', size=(5, 1), key='output_kat'), sg.Checkbox('plotdata', size=(5, 1), key='output_plotdata')]
         ] 

window = sg.Window('My window with tabs', layout, default_element_size=(12,1), finalize=True)    

fname_output=""
fname_kat=""
check = False

while True:    
    if(check==False):
        window['fpmi_section_how_simulate'].update(visible=True)
        window['pd0_setting_section'].update(visible=True)
        window['pd1_setting_section'].update(visible=False)
        window['pd2_setting_section'].update(visible=False)
        check = True
    event, values = window.read()

    #print(event,values)
    if event == sg.WIN_CLOSED:     # if all windows were closed
        break
    if event == "Exit":           # always,  always give a way out!   # atode kesu 
        break        
    if event == "xaxis_range_beg" and values["xaxis_range_beg"] and values["xaxis_range_beg"][-1] not in ('0123456789.-'):
        window["xaxis_range_beg"].update(values["xaxis_range_beg"][:-1])
    if event == "xaxis_range_end" and values["xaxis_range_end"] and values["xaxis_range_end"][-1] not in ('0123456789.-'):
        window["xaxis_range_end"].update(values["xaxis_range_end"][:-1])
    """
    if event == "fpmi_pd1_sweep_range_beg" and values["fpmi_pd1_sweep_range_beg"] and values["fpmi_pd1_sweep_range_beg"][-1] not in ('0123456789.-'):
        window["fpmi_pd1_sweep_range_beg"].update(values["fpmi_pd1_sweep_range_beg"][:-1])
    if event == "fpmi_pd1_sweep_range_end" and values["fpmi_pd1_sweep_range_end"] and values["fpmi_pd1_sweep_range_end"][-1] not in ('0123456789.-'):
        window["fpmi_pd1_sweep_range_end"].update(values["fpmi_pd1_sweep_range_end"][:-1])
    """
    ### visible/invisible advanced setting
    if event == 'issweep':
        window['fpmi_section_how_simulate'].update(visible=True)
        window['pd0_setting_section'].update(visible=True)
        window['pd1_setting_section'].update(visible=False)
        window['pd2_setting_section'].update(visible=False)
    if event == "istransfunc":
        window['fpmi_section_how_simulate'].update(visible=False)
        window['pd0_setting_section'].update(visible=False)
        window['pd1_setting_section'].update(visible=False)
        window['pd2_setting_section'].update(visible=True)
    if event == 'isscan':
        window['pd0_setting_section'].update(visible=True)
        window['pd1_setting_section'].update(visible=False)
        window['pd2_setting_section'].update(visible=False)
    if event == 'isdemod_once':
        window['pd0_setting_section'].update(visible=False)
        window['pd1_setting_section'].update(visible=True)
        window['pd2_setting_section'].update(visible=False)
    if event == "event_FPMI":           # FPMI
        ###############################
        ### get variables from GUI ###
        ###############################

        ### Optic ###
        ##laser_power = values['laser_power']#source laser power
    
        ### what INF ###
        ##what_inf = values['what_inf']

        ### PD location ###
        dic_fpmi_ispds = {
            ### PDs
            "REFL":values['n1'],#bool REFL
            "AS":values['n4'],#bool AS
            "nytrans":values['nytrans'],#bool
            "nxtrans":values['nxtrans'],#bool
            "n2":values['n2'],#bool
            "n3":values['n3'],#bool
            "ny1":values['ny1'],#bool
            "nx1":values['nx1'],#bool
            "ny2":values['ny2'],#bool
            "nx2":values['nx2'],#bool
            "ny3":values['ny3'],#bool
            "nx3":values['nx3'],#bool
        }
        #########
        #
        # plot variables
        # 
        xaxis_range_beg = values["xaxis_range_beg"]
        xaxis_range_end = values["xaxis_range_end"]
        #yaxis_range_beg = values["yaxis_range_beg"]
        #yaxis_range_end = values["yaxis_range_end"]
        x_plotscale = "lin"
        if(values["xaxis_log"]):
            x_plotscale = "log"
        y_plotscale = "lin"
        if(values["yaxis_log"]):
            y_plotscale = "log"
        #########
        dic_fpmi_advanced_setting = {
            ### DoF
            "dof":values['dof'],
            ### pd0/pd1/pd2?
            "isscan":values['isscan'],#bool
            "isdemod_once":values['isdemod_once'],#bool
            "istransfunc":values['istransfunc'],#bool
            ### advanced setting
            "laser_power":values['laser_power'],#str
            #
            # plot variables
            # 
            "x_plotscale":x_plotscale,#str
            "xaxis_range_beg":values["xaxis_range_beg"],#str
            "xaxis_range_end":values["xaxis_range_end"],#str
            "y_plotscale":y_plotscale,#str
            #"yaxis_range_beg":values["yaxis_range_beg"],#str
            #"yaxis_range_end":values["yaxis_range_end"],#str
            "demod_phase":values["demod_phase"],
            "samplingnum":values['samplingnum'],#str
            "pd2_mixer1_demodfreq":values["pd2_mixer1_demodfreq"]
        }
        
        kat = finesse.kat()
        code = generate_kat_FPMI(dic_fpmi_ispds, dic_fpmi_advanced_setting)
        kat.parse(code)
        out = kat.run()

        ### scan
        if(values["issweep"] and values['isscan']==True):
            # 
            fig1 = plt.figure(figsize=(20,20))
            fig1.suptitle("abs")
            plotnum = 0
            for key in dic_fpmi_ispds.keys():
                if dic_fpmi_ispds[key] == True:
                    plotnum += 1 #plotnum
            vh_plotnum = math.ceil(math.sqrt(plotnum))
            if(plotnum > 0):
                #for i in range(plotnum):
                i = 0
                for key in dic_fpmi_ispds.keys():
                    if dic_fpmi_ispds[key]==True:
                        plt.subplot(vh_plotnum,vh_plotnum,i+1) #Axes
                        plt.plot(out.x, out["pd0_%s_I" % key])
                        plt.xscale("linear")
                        plt.yscale("linear")
                        ## if selected log, xscale = log
                        if(x_plotscale=="log"):
                            plt.xscale("log")
                        ## yscale select lin/log
                        if(y_plotscale=="log"):
                            plt.yscale("log")
                        #plt.ylabel('%s' % key)
                        #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                        plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                        plt.title('%s abs' % key, fontsize=18)
                        plt.tick_params(labelsize=18)
                        i += 1
            plt.tight_layout()
        ### demod once (pd1)
        if(values["issweep"] and values['isdemod_once']==True):
            # 
            fig1 = plt.figure(figsize=(20,20))
            fig1.suptitle("absolute value")
            plotnum = 0
            for key in dic_fpmi_ispds.keys():
                if dic_fpmi_ispds[key] == True:
                    plotnum += 1 #plotnum
            
            if(plotnum > 0):
                #for i in range(plotnum):
                i = 0
                #
                # get plot num for matplotlib subplot[v_plotnum, h_plotnum, ]
                #
                fpmi_list_demon_phase = ['plot_in_phase_f1', 'plot_quadrature_phase_f1', 'plot_in_phase_f2', 'plot_in_phase_f2']
                fpmi_list_demon_phase_True = [k for k in fpmi_list_demon_phase if values[k] == True]
                j = len(fpmi_list_demon_phase_True)
                if(j==0):
                    values['plot_in_phase_f1'] = True
                    j = 1
                #plotの横の数
                h_plotnum = j
                #plotの縦の数
                v_plotnum = h_plotnum

                for key in dic_fpmi_ispds.keys():
                    if dic_fpmi_ispds[key] == True:
                        k = 1
                        if values['plot_in_phase_f1'] == True:
                            plt.subplot(v_plotnum,h_plotnum,i+k) #Axes
                            plt.plot(out.x, out["pd1_%s_I1" % key])#IorQ? I1orI2?
                            ## xscale select lin/log
                            if(x_plotscale=="log"):
                                plt.xscale("log")
                            ## yscale select lin/log
                            if(y_plotscale=="log"):
                                plt.yscale("log")
                            #plt.ylabel('%s' % key)
                            #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                            plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                            plt.title('%s pd1 I1' % key, fontsize=18)
                            plt.tick_params(labelsize=18)
                            k += 1
                        if values['plot_quadrature_phase_f1'] == True:
                            plt.subplot(v_plotnum,h_plotnum,i+k) #Axes
                            plt.plot(out.x, out["pd1_%s_Q1" % key])#IorQ? I1orI2?
                            ## xscale select lin/log
                            if(x_plotscale=="log"):
                                plt.xscale("log")
                            ## yscale select lin/log
                            if(y_plotscale=="log"):
                                plt.yscale("log")
                            #plt.ylabel('%s' % key)
                            #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                            plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                            plt.title('%s pd1 Q1' % key, fontsize=18)
                            plt.tick_params(labelsize=18)
                            k += 1
                        if values['plot_in_phase_f2'] == True:
                            plt.subplot(v_plotnum,h_plotnum,i+k) #Axes
                            plt.plot(out.x, out["pd1_%s_I2" % key])#IorQ? I1orI2?
                            ## xscale select lin/log
                            if(x_plotscale=="log"):
                                plt.xscale("log")
                            ## yscale select lin/log
                            if(y_plotscale=="log"):
                                plt.yscale("log")
                            #plt.ylabel('%s' % key)
                            #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                            plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                            plt.title('%s pd1 I2' % key, fontsize=18)
                            plt.tick_params(labelsize=18)
                            k += 1
                        if values['plot_quadrature_phase_f2'] == True:
                            plt.subplot(v_plotnum,h_plotnum,i+k) #Axes
                            plt.plot(out.x, out["pd1_%s_Q2" % key])#IorQ? I1orI2?
                            ## xscale select lin/log
                            if(x_plotscale=="log"):
                                plt.xscale("log")
                            ## yscale select lin/log
                            if(y_plotscale=="log"):
                                plt.yscale("log")
                            #plt.ylabel('%s' % key)
                            #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                            plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                            plt.title('%s pd1 Q2' % key, fontsize=18)
                            plt.tick_params(labelsize=18)
                            k += 1
                        i += j
            plt.tight_layout()
        
        ### sensmat(pd2)
        if(values['istransfunc']==True):
            # abs
            fig1 = plt.figure(figsize=(20,20))
            fig1.suptitle("abs")
            plotnum = 0
            for key in dic_fpmi_ispds.keys():
                if dic_fpmi_ispds[key] == True:
                    plotnum += 1 #plotnum
            h_plotnum = math.ceil(math.sqrt(plotnum)) # abs+phase
            v_plotnum = 2*h_plotnum # math.ceil(math.sqrt(2*plotnum))
            if(plotnum > 0):
                #for i in range(plotnum):
                i = 0
                for key in dic_fpmi_ispds.keys():
                    if dic_fpmi_ispds[key] == True:
                        k = math.floor((i/h_plotnum))*2*h_plotnum + i%h_plotnum+1
                        #
                        # abs
                        #
                        plt.subplot(v_plotnum,h_plotnum,k) #Axes
                        plt.plot(out.x, out["pd2_%s_I" % key])
                        ## xscale select lin/log
                        if(x_plotscale=="log"):
                            plt.xscale("log")
                            ## yscale select lin/log
                        if(y_plotscale=="log"):
                            plt.yscale("log")
                        #plt.ylabel('%s' % key)
                        #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                        plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                        plt.title('%s abs' % key, fontsize=18)
                        plt.tick_params(labelsize=18)
                        
                        #
                        # phase
                        #
                        plt.subplot(v_plotnum,h_plotnum,k+h_plotnum) #Axes
                        plt.semilogx(out.x, np.angle(out["pd2_%s_I" % key]), color="R")
                        ## xscale select lin/log
                        if(x_plotscale=="log"):
                            plt.xscale("log")
                        ## yscale select lin/log
                        if(y_plotscale=="log"):
                            plt.yscale("log")
                        #plt.ylabel('%s' % key)
                        #plt.ylabel(out.ylabel.split()[0]+out.ylabel.split()[1])
                        plt.xlabel(out.xlabel.split()[0]+out.xlabel.split()[1], fontsize=18)
                        plt.title('%s phase' % key, fontsize=18)
                        plt.tick_params(labelsize=18)

                        i += 1
            plt.tight_layout()

        plt.show()
        
        if values['output_kat'] == True:
            kat=code
            fname_kat = sg.popup_get_file('Select the output name for kat file?', save_as=True, file_types=(("ALL Files", "*.kat"),))

            try:
                f = open(fname_kat, 'x')
                f.writelines(kat)
                f.close()
            except FileExistsError:
                sg.popup_ok("Error : there is a file %s" % fname_kat)
            except Exception:
                sg.popup_ok("Unexpected error:", sys.exc_info()[0])
            
        if values['output_plotdata'] == True:
            fname_plotdata = sg.popup_get_file('Select the output name for plot data?', save_as=True, file_types=(("ALL Files", "*.txt"),))
            kat = out
            
            
            
            try:
                f = open(fname_plotdata, 'x')
                f.writelines(kat)
                f.close()
            except FileExistsError:
                sg.popup_ok("Error : there is a file %s" % fname_plotdata)
            except Exception:
                sg.popup_ok("Unexpected error:", sys.exc_info()[0])
            
window.close()         


# In[ ]:





# In[ ]:




