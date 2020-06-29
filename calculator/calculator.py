from tkinter import *

def set_val(text,label):
    '''
    set the calculator
    :param text:
    :param label:
    :return:
    '''
    text_bar.set(text)
    label_var.set(label)

def eq(label):
    '''
    calculat function
    :param label:
    :return:
    '''
    try:
        label = eval(label)
        text = label
    except:
        label = "0"
        text = "0"
    set_val(text,label)

def init(text):
    '''
    set null value
    :param text:
    :return:
    '''
    if text == '0':
        text = ""
    return text

def enter(event):
    '''
    menege keyboard inputs
    :param event:
    :return:
    '''
    key = event.char
    text = text_bar.get()
    label = label_var.get()
    list1 = ['+', '-', '*', '/', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    if key in list1:
        text=init(text)
        label = init(label)

        label += key
        if key in ['+', '-', '*', '/']:
            text = ''
        else:
            text += key
        set_val(text,label)
    elif key == "\x08":
        clear(0)
    elif key == '\r':
        eq(label)

def cleck(event):
    '''
    menege button cleck events
    :param event:
    :return:
    '''
    option = ['+','-','*','/']
    text = text_bar.get()
    label = label_var.get()

    text = init(text)
    label = init(label)

    if event.widget.cget("text") == '=':
        eq(label)
    else:
        if event.widget.cget("text") in option:
            text = ''
        else:
            text = text + event.widget.cget("text")
        label += event.widget.cget("text")
        set_val(text,label)

def clear(event):
    '''
    clear the entry box and set as a 0
    :param event:
    :return:
    '''
    set_val(0,0)

if __name__ == '__main__':

    # initialization
    root = Tk()
    root.geometry("600x600")
    root.title("calculator")
    root.wm_iconbitmap("icon.ico")
    text_bar = StringVar(value='0')
    label_var = StringVar(value='0')
    number = [['9','8','7','+'],['6','5','4','-'],['3','2','1','*'],['0','.','=','/']]

    # main frame
    frame = Frame(root, background="gray", borderwidth=5, relief=SOLID)

    # frame for entry box and clear button
    f1 = Frame(frame, background="light gray")
    e = Entry(f1, textvariable=text_bar, font="Arial 20")
    l = Label(e, textvariable=label_var, font="Arial 20")
    l.pack(anchor="ne")
    e.pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)

    b = Button(f1, text='C', font="Arial 20", width=5)
    b.pack(padx=10, pady=10, fill=BOTH, expand=YES)
    b.bind("<Button-1>", clear)
    f1.pack(padx=10, pady=10, fill=BOTH, expand=YES)

    # all buttons pake in frame 3
    f3 = Frame(frame)
    for j in number:
        f2 = Frame(f3, background="light gray")
        for i in j:
            b = Button(f2, text=i, font="Arial 20")
            b.pack(padx=10, pady=10, fill=BOTH, expand=YES, side=LEFT)
            b.bind("<Button-1>", cleck)
        f2.pack(fill=BOTH, expand=YES)
    f3.pack(padx=10, pady=10, fill=BOTH, expand=YES)

    frame.pack(padx=10, pady=10, fill=BOTH, expand=YES)
    root.bind("<Key>", enter)
    root.mainloop()
