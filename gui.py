try:
    from Tkinter import *
except ImportError:
    from tkinter import *

class Mastermind(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

        self.colorRed = Button(self, text = "Red button", background = "black")
        self.colorRed.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
# style = Tk.Style()
# style.theme_use('classic')
app = Mastermind(master=root)
app.master.title("My Do-Nothing Application")
app.master.maxsize(1000, 400)
app.master.minsize(width=666, height=666)
app.mainloop()
root.destroy()