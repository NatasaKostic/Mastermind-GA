try:
    from Tkinter import *
except ImportError:
    from tkinter import *

class Mastermind(Frame):
    def say_hi(self):
        print ("hi there, everyone!")

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

        self.colorRed = Button(self, highlightbackground = "red")
        self.colorRed.pack({"side": "left"})
        self.colorRed["command"] = lambda: self.selectCombo("red")

        self.colorPurple = Button(self, highlightbackground = "purple")
        self.colorPurple.pack({"side": "left"})
        self.colorPurple["command"] = lambda: self.selectCombo("purple")

        self.colorGreen = Button(self, highlightbackground = "green")
        self.colorGreen.pack({"side": "left"})
        self.colorGreen["command"] = lambda: self.selectCombo("green")

        self.colorYellow = Button(self, highlightbackground = "yellow")
        self.colorYellow.pack({"side": "left"})
        self.colorYellow["command"] = lambda: self.selectCombo("yellow")

        self.colorBlue = Button(self, highlightbackground = "blue")
        self.colorBlue.pack({"side": "left"})
        self.colorBlue["command"] = lambda: self.selectCombo("blue")

        self.colorMagenta = Button(self, highlightbackground = "magenta")
        self.colorMagenta.pack({"side": "left"})
        self.colorMagenta["command"] = lambda: self.selectCombo("magenta")


    def selectCombo(self, color):
    	self.colorsSelected = self.colorsSelected + 1
    	print ("Red selected '{}'").format(self.colorsSelected)
    	print ("Red selected '{}'").format(color)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.colorsSelected = 0


root = Tk()
# style = Tk.Style()
# style.theme_use('classic')
app = Mastermind(master=root)
app.master.title("My Do-Nothing Application")
app.master.maxsize(1000, 400)
app.master.minsize(width=666, height=666)
app.mainloop()
root.destroy()



