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
    evaluate = tk.Toplevel()
    evaluate.title('evaluate')
    evaluate.geometry('240x130+580+280')

    var = tk.StringVar()
    laber_evaluate = tk.Label(evaluate, bg='yellow', width=30, text='chose a model')
    laber_evaluate.pack()

    def print_selection():
        laber_evaluate.config(bg='green',text='you choose the "'+var.get()+'" model')

    r1 = tk.Radiobutton(evaluate, text='rate', variable=var, value='rate', command =print_selection)
    r1.place(x = 80, y = 25)
    r2 = tk.Radiobutton(evaluate, text='ztest', variable=var, value='ztest', command =print_selection)
    r2.place(x = 80, y = 45)
    r3 = tk.Radiobutton(evaluate, text='mix', variable=var, value='mix', command =print_selection)
    r3.place(x = 80, y = 65)

    def detail():

        if var.get()=='rate':
            evaluate.withdraw()
            rate_page = tk.Toplevel()
            rate_page.title('rate model')
            rate_page.geometry('240x230+580+250')
            laber_rate = tk.Label(rate_page, bg='yellow', width=30, text='Please select')
            laber_rate.pack()
            def print_tolerate(v):
                if (float)(scale_min.get()) < (float)(scale_max.get()):
                    laber_rate.config(bg='green',text='You chose '+(str)(scale_min.get())+' to '+(str)(scale_max.get()) )
                if (float)(scale_min.get()) >= (float)(scale_max.get()):
                    laber_rate.config(bg='red',text='Certain should less than wrong')

            scale_min = tk.Scale(rate_page, label='Max distance for certain', from_=0, to=50, orient=tk.HORIZONTAL, length=200, showvalue=10,
                             tickinterval=50, resolution=0.1, command=print_tolerate)
            scale_min.pack()

            scale_max = tk.Scale(rate_page, label='Min distance for wrong', from_=0, to=50, orient=tk.HORIZONTAL, length=200, showvalue=10,
                             tickinterval=50, resolution=0.1, command=print_tolerate)
            scale_max.pack()

            def rate_confirm():
                if (float)(scale_min.get()) < (float)(scale_max.get()):
                    # b.showinfo(title='notice', message='The error function is processing, it will take few minutes.')
                    # b.askokcancel(title='notice', message='The error function is processing, it will take few minutes.')
                    laber_rate.config(bg='yellow', text='The error function is processing')
                    eval.show('rate', (float)(scale_min.get()), (float)(scale_max.get()))
                if (float)(scale_min.get()) >= (float)(scale_max.get()):
                    laber_rate.config(bg='red', text='Please select the right number')
            tolerate_confirm = tk.Button(rate_page, text='confirm', width=15, height=2, command=rate_confirm)
            tolerate_confirm.pack()

        elif var.get()=='ztest':

            evaluate.withdraw()
            ztest_page = tk.Toplevel()
            ztest_page.title('ztest model')
            ztest_page.geometry('240x230+580+250')
            laber_ztest = tk.Label(ztest_page, bg='yellow', width=30, text='Please input the mask tolerance')
            laber_ztest.pack()

            mask_tolerance = tk.StringVar()
            mask_tolerance.set('3')
            entry = tk.Entry(ztest_page,width=3,textvariable=mask_tolerance)
            entry.place(x=150,y=40)
            tk.Label(ztest_page, text='Mask tolerance').place(x=50,y=40)
            tk.Label(ztest_page, text='Declear: visibility mask defined as a \nset of pixels where '
                                      'the surface of \nmodel is in front of the scene surface \n'
                                      'or at mose by the tolerance behand').place(x=10, y=90)
            def ztest_confirm():
                if str.isdigit(entry.get()):
                    eval.show('ztest', (float)(entry.get()), 0)
                else:
                    laber_ztest.config( bg='red', text='Please input a number')

            ztest_confirm = tk.Button(ztest_page, text='confirm', width=15, height=1, command=ztest_confirm)
            ztest_confirm.place(x= 50, y=190)

        elif var.get()=='mix':
            evaluate.withdraw()
            mix_page = tk.Toplevel()
            mix_page.title('mix model')
            mix_page.geometry('240x230+580+250')
            laber_mix = tk.Label(mix_page, bg='yellow', width=30, text='Please chose the weight')
            laber_mix.pack()

            weight = tk.Scale(mix_page, label='Weight for ztest', from_=0, to=1, orient=tk.HORIZONTAL,
                                 length=200, showvalue=10,resolution=0.01)
            weight.set(0.50)
            weight.pack()

            tk.Label(mix_page, text='Declear: mix two method together. \n'
                                    'The number reflact the weight of ztest ').place(x=10, y=100)

            def ztest_confirm():
                if str.isdigit(entry.get()):
                    eval.show('ztest', (float)(entry.get()), 0)
                else:
                    laber_ztest.config(bg='red', text='Please input a number')

            def mix_confirm():
                eval.show('mix', weight.get(), 1-weight.get())
            mix_confirm = tk.Button(mix_page, text='Confirm', width=15, height=1, command=mix_confirm)
            mix_confirm.place(x=50, y=170)

        else:
            laber_evaluate.config(bg='red',text='you did not chose any')

    button = tk.Button(evaluate, text='Next Step', width=10, height=1, command = detail)
    button.place(x= 70, y= 90)

    evaluate.mainloop()

def show_data_analysis():
    analysis = tk.Toplevel()
    analysis.title('analysis')
    analysis.geometry('240x230+580+250')

    var = tk.StringVar()
    laber_evaluate = tk.Label(analysis, bg='yellow', width=30, text='chose a model')
    laber_evaluate.pack()

    def print_selection():
        laber_evaluate.config(bg='green',text='the "'+var.get()+'" model')

    r1 = tk.Radiobutton(analysis, text='Average ', variable=var, value='average', command =print_selection)
    r1.place(x = 60, y = 25)
    r2 = tk.Radiobutton(analysis, text='Standard deviation', variable=var, value='standard_deviation', command =print_selection)
    r2.place(x = 60, y = 45)

    degree = tk.Scale(analysis, label='Rotation degree', from_=0, to=360, orient=tk.HORIZONTAL, length=200,
                         showvalue=10,tickinterval=90, resolution=1)
    degree.place(x = 20, y = 75)
    def show_data():
        if var.get()=='average':
            daan.show('average', degree.get())
        elif var.get()=='standard_deviation':
            daan.show('standard_deviation', degree.get())
        else:
            laber_evaluate.config(bg='red', text='Please chose a model')

    analysis_confirm = tk.Button(analysis, text='confirm', width=15, height=1,command=show_data)
    analysis_confirm.place(x =50, y = 180)

menubar = tk.Menu(frame)

filemenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='Tool',menu=filemenu)

filemenu.add_command(label='Data',command=show_data_analysis)
filemenu.add_command(label='Evaluate',command=show_evaluate_page)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=frame.quit)



editmenu = tk.Menu(menubar,tearoff=0)

menubar.add_cascade(label='Help',menu=editmenu)

editmenu.add_command(label='Author')
editmenu.add_command(label='About')


frame.config(menu=menubar)


frame.mainloop()
