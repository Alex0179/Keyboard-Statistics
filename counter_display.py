from tkinter import *
from tkinter import messagebox
from pynput.mouse import Listener as MouseListener
import json
import time
import collections

tk = Tk()
txt = StringVar()
current_time = time.strftime("%H:%M:%S", time.localtime())
f = open('key_counts.json')
counts = json.load(f)
#print(counts)
print("---")
#sort_counts = collections.OrderedDict(sorted(counts["key"].items(), key=lambda x: x[1], reverse=True))
#for i in sort_counts:
#	print(i[0], i[1])
#print(sort_counts)

tk.title("Keyboard Statistics")
tk.geometry("800x600")
tk.resizable(True, True)
tk.configure(background="#043d69")

tk.iconbitmap('icon.ico')
infobutton=PhotoImage(file="info.gif")
keyboard=PhotoImage(file="keyboard.gif")
dynamic="yes"

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def on_click(x, y, button, pressed):
    if pressed:
        print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

pos_1 = "a"
count_1 = "1"
pos_2 = "b"
count_2 = "2"
pos_3 = "c"
count_3 = "3"
pos_4 = "d"
count_4 = "4"
pos_5 = "e"
count_5 = "5"

def infobox():
    infobox=messagebox.showinfo("Keyboard Statistics Quick Info", "Quick Info\n"
                                "\nTop 5 used keys:\n"
                                "    1: "+pos_1+", used "+count_1+" times\n"
                                "    2: "+pos_2+", used "+count_2+" times\n"
                                "    3: "+pos_3+", used "+count_3+" times\n"
                                "    4: "+pos_4+", used "+count_4+" times\n"
                                "    5: "+pos_5+", used "+count_5+" times\n")

header=Label(tk, text="Keyboard Statistics Display", bg="#043d69", fg="gold", font=("futura", "20"))
header.place(x=230, y=20)

keyboarddisp=Label(tk, image=keyboard)
keyboarddisp.image = keyboard
keyboarddisp.place(x=56, y=90)

keyesc = Button(tk, text="", width=4, height=1, bg="#064E86", relief=FLAT)
keyesc.place(x=86, y=122)

keyf1 = Button(tk, text="", width=4, height=1, bg="#064E86", relief=FLAT)
keyf1.place(x=86, y=207)

keytidle = Button(tk, text="", width=3, height=1, bg="#064E86", relief=FLAT)
keytidle.place(x=86, y=172)
    
info=Button(tk, text="asd", image=infobutton, bg="#043d69", relief=FLAT, fg="white", command=infobox)
info.image = infobutton
info.place(x=740, y=540)

CreateToolTip(keyesc, text =("Times Escape key pressed: "+str(counts["key"]["esc"])))
CreateToolTip(keytidle, text =("Times Tidle key pressed: "+str(counts["key"]["`"]+counts["key"]["Â¬"])))

listener = MouseListener(on_click=on_click)
listener.start()

tk.mainloop()
