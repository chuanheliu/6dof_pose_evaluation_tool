import Tkinter as tk
import eval_rotating_cup as eval
import tkMessageBox as b
import data_analysis as daan


frame = tk.Tk()
frame.title('evaluation tool')
frame.geometry('380x260+500+200')

canvas = tk.Canvas(frame)

image_file = tk.PhotoImage(file='timg.gif')
image = canvas.create_image(0,0,anchor='nw',image=image_file)
canvas.pack()

def show_evaluate_page():
    '''
    the evaluate button call this method to show the evaluation page

    '''
    evaluate = tk.Toplevel()
    evaluate.title('evaluate')
    evaluate.geometry('240x130+580+280')
    # the laber in the top
    var = tk.StringVar()
    laber_evaluate = tk.Label(evaluate, bg='yellow', width=30, text='chose a model')
    laber_evaluate.pack()

    # change the laber after chose a model
    def print_selection():
        laber_evaluate.config(bg='green',text='you choose the "'+var.get()+'" model')

    # the 3 Radiobuttons
    r1 = tk.Radiobutton(evaluate, text='CPR', variable=var, value='cpr', command =print_selection)
    r1.place(x = 80, y = 25)
    r2 = tk.Radiobutton(evaluate, text='ZDD', variable=var, value='zdd', command =print_selection)
    r2.place(x = 80, y = 45)
    r3 = tk.Radiobutton(evaluate, text='WIVM', variable=var, value='wivm', command =print_selection)
    r3.place(x = 80, y = 65)

    # goes to different page
    def detail():

        # CRP model
        if var.get()=='cpr':

            # CRP window
            evaluate.withdraw() #close the previous window
            cpr_page = tk.Toplevel()
            cpr_page.title('CPR model')
            cpr_page.geometry('240x230+580+250')
            laber_cpr = tk.Label(cpr_page, bg='yellow', width=30, text='Please select')
            laber_cpr.pack()

            # print the tolerate that have chosen
            def print_tolerate(v):
                # the min number should less than max number
                if (float)(scale_min.get()) < (float)(scale_max.get()):
                    laber_cpr.config(bg='green',text='You chose '+(str)(scale_min.get())+' to '+(str)(scale_max.get()) )
                if (float)(scale_min.get()) >= (float)(scale_max.get()):
                    laber_cpr.config(bg='red',text='Certain should less than wrong')

            # the scale from 0 to 50 to chose the right tolerate
            scale_min = tk.Scale(cpr_page, label='Max distance for certain', from_=0, to=50, orient=tk.HORIZONTAL, length=200, showvalue=10,
                             tickinterval=50, resolution=0.1, command=print_tolerate)
            scale_min.pack()
            # the scale from 0 to 50 to chose the wrong tolerate
            scale_max = tk.Scale(cpr_page, label='Min distance for wrong', from_=0, to=50, orient=tk.HORIZONTAL, length=200, showvalue=10,
                             tickinterval=50, resolution=0.1, command=print_tolerate)
            scale_max.pack()

            # confirm the tolerates and execut the error function
            def cpr_confirm():
                if (float)(scale_min.get()) < (float)(scale_max.get()):
                    # b.showinfo(title='notice', message='The error function is processing, it will take few minutes.')
                    # b.askokcancel(title='notice', message='The error function is processing, it will take few minutes.')
                    laber_cpr.config(bg='yellow', text='The error function is processing')
                    eval.show('cpr', (float)(scale_min.get()), (float)(scale_max.get()))
                if (float)(scale_min.get()) >= (float)(scale_max.get()):
                    laber_cpr.config(bg='red', text='Please select the right number')
            tolerate_confirm = tk.Button(cpr_page, text='confirm', width=15, height=2, command=cpr_confirm)
            tolerate_confirm.pack()

        # ZDD model
        elif var.get()=='zdd':

            # ZDD window
            evaluate.withdraw() #close the previous window
            zdd_page = tk.Toplevel()
            zdd_page.title('zdd model')
            zdd_page.geometry('240x230+580+250')
            laber_zdd = tk.Label(zdd_page, bg='yellow', width=30, text='Please input the mask tolerance')
            laber_zdd.pack()

            mask_tolerance = tk.StringVar()
            # default
            mask_tolerance.set('3')
            entry = tk.Entry(zdd_page,width=3,textvariable=mask_tolerance)
            entry.place(x=150,y=40)
            tk.Label(zdd_page, text='Mask tolerance').place(x=50,y=40)
            tk.Label(zdd_page, text='Declear: visibility mask defined as a \nset of pixels where '
                                      'the surface of \nmodel is in front of the scene surface \n'
                                      'or at mose by the tolerance behand').place(x=10, y=90)
            # the confirm button to execute ZDD error function
            def zdd_confirm():
                # judge the mask tolerate is number
                if str.isdigit(entry.get()):
                    # execute
                    eval.show('zdd', (float)(entry.get()), 0)
                else:
                    # change laber
                    laber_zdd.config( bg='red', text='Please input a number')

            # confirm button
            tk.Button(zdd_page, text='confirm', width=15, height=1, command=zdd_confirm).place(x= 50, y=190)

        # WIVM model
        elif var.get()=='wivm':

            # WIVM window
            evaluate.withdraw()#close the previous window
            wivm_page = tk.Toplevel()
            wivm_page.title('WIVM model')
            wivm_page.geometry('240x230+580+250')
            laber_wivm = tk.Label(wivm_page, bg='yellow', width=30, text='Please chose the weight')
            laber_wivm.pack()

            # a scale from 0 to 1 to chose the weight
            weight = tk.Scale(wivm_page, label='Weight for Inner Visibility Mask', from_=0, to=1, orient=tk.HORIZONTAL,
                                 length=200, showvalue=10,resolution=0.01)
            # default = 0.5
            weight.set(0.50)
            weight.pack()

            # label for declear
            tk.Label(wivm_page, text='Declear: consider both inner and \nunion part. '
                                    'The number reflact the \nweight for inner part ').place(x=10, y=100)

            # confirm to execute the WIVM error function
            def wivm_confirm():
                eval.show('wivm', weight.get(), 1-weight.get())
            mix_confirm = tk.Button(wivm_page, text='Confirm', width=15, height=1, command=wivm_confirm)
            mix_confirm.place(x=50, y=170)
        # if user does chose any model but wants to go to next step
        else:
            laber_evaluate.config(bg='red',text='you did not chose any')

    button = tk.Button(evaluate, text='Next Step', width=10, height=1, command = detail)
    button.place(x= 70, y= 90)

    evaluate.mainloop()

def show_data_analysis():
    '''
    the data analysis button call this method to show the data

    '''
    analysis = tk.Toplevel()
    analysis.title('analysis')
    analysis.geometry('240x230+580+250')

    var = tk.StringVar()
    laber_evaluate = tk.Label(analysis, bg='yellow', width=30, text='chose a model')
    laber_evaluate.pack()

    # print the model user select
    def print_selection():
        laber_evaluate.config(bg='green',text='the "'+var.get()+'" model')

    # radiobuttn to select model "average" or "standard deviation"
    r1 = tk.Radiobutton(analysis, text='Average ', variable=var, value='average', command =print_selection)
    r1.place(x = 60, y = 25)
    r2 = tk.Radiobutton(analysis, text='Standard deviation', variable=var, value='standard_deviation', command =print_selection)
    r2.place(x = 60, y = 45)

    #  a scale that from 0 -360 to chose the degree of data user want to show
    degree = tk.Scale(analysis, label='Rotation degree', from_=0, to=360, orient=tk.HORIZONTAL, length=200,
                         showvalue=10,tickinterval=90, resolution=1)
    degree.place(x = 20, y = 75)

    # different model to show different data format
    def show_data():
        if var.get()=='average':
            daan.show('average', degree.get())
        elif var.get()=='standard_deviation':
            daan.show('standard_deviation', degree.get())
        else:
            laber_evaluate.config(bg='red', text='Please chose a model')

    analysis_confirm = tk.Button(analysis, text='confirm', width=15, height=1,command=show_data)
    analysis_confirm.place(x =50, y = 180)


# add the menubar to the top of the window
menubar = tk.Menu(frame)

# file menu
filemenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='Tool',menu=filemenu)

filemenu.add_command(label='Data',command=show_data_analysis)
filemenu.add_command(label='Evaluate',command=show_evaluate_page)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=frame.quit)


# edit menu
editmenu = tk.Menu(menubar,tearoff=0)

menubar.add_cascade(label='Help',menu=editmenu)

editmenu.add_command(label='Author')
editmenu.add_command(label='About')


frame.config(menu=menubar)


frame.mainloop()
