from tkinter import *

def callback(input):
    '''
    this is use for input only numbers
    :param input:
    :return:
    '''
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False

def add():
    '''
    eveluat function
    :return:
    '''
    no1 = e1.get()
    no2 = e2.get()
    op = option.get()
    try:
        sum = eval(no1+op+no2)
    except:
        sum = "error"
    ans.set(sum)

def clear():
    '''
    clear all the value
    :return:
    '''
    n1.set("")
    n2.set("")
    option.set("")
    ans.set("answer")
    e1.focus_set()

if __name__ == '__main__':
    # initialization
    root = Tk()
    root.geometry("500x500")
    root.title("calculator")
    root.wm_iconbitmap("icon.ico")
    n1=StringVar(value=0)
    n2=StringVar(value=0)
    option = StringVar(value="+")
    ans = StringVar(value="answer")
    reg = root.register(callback)

    # main frame
    frame = Frame(root)

    # frame1
    f = Frame(frame, background="gray")
    Label(f,text="Number 1 : ", font="Arial 25").pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
    e1 = Entry(f, textvariable=n1, font="Arial 25")
    e1.pack(padx=10, pady=10, fill=BOTH, expand=YES, side=RIGHT)
    e1.config(validate="key", validatecommand=(reg, "%P"))
    f.pack(fill=BOTH, expand=YES)

    # frame2
    f = Frame(frame, background="gray")
    for i in ['+','-','*','/']:
        Radiobutton(f, text=i, value=i, variable=option, font="Arial 25", indicator=0).pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
    f.pack(fill=BOTH, expand=YES)

    # frame3
    f = Frame(frame, background="gray")
    Label(f,text="Number 2 : ", font="Arial 25").pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
    e2 = Entry(f, textvariable=n2, font="Arial 25")
    e2.pack(padx=10, pady=10, fill=BOTH, expand=YES, side=RIGHT)
    e2.config(validate="key", validatecommand=(reg, "%P"))
    f.pack(fill=BOTH, expand=YES)

    # frame4
    f = Frame(frame, background="gray")
    Button(f, text="=", font="Arial 17", width=13, command=add).pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
    l = Label(f, textvariable=ans, font="Arial 25", width=7).pack(padx=10, pady=10, fill=BOTH, expand=YES, side=RIGHT)
    f.pack(fill=BOTH, expand=YES)

    # frame5
    f = Frame(frame, background="gray")
    Button(f, text="clear", font="Arial 17", width=13, command=clear).pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
    f.pack(fill=BOTH, expand=YES)

    frame.pack(fill=BOTH, expand=YES, padx=50, pady=50)
    root.mainloop()