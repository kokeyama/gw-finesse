import PySimpleGUI as sg      

layout = [[sg.Text('My one-shot window.')],      
                [sg.Image("./Dual_Recycled_FPMI_drawing.png", key="imageContainer", size=(800,600))],
                 [sg.InputText(key='-IN-')],      
                 [sg.Submit(), sg.Cancel()]]

window = sg.Window('Window Title', layout)    

event, values = window.read()    
window.close()

text_input = values['-IN-']    
sg.popup('You entered', text_input)

