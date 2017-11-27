<<<<<<< HEAD
import Tkinter as tk 
import tkMessageBox
import tkFont as tkfont


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ComboSelection):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome! Let's play Mastermind!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Select Your Combination",
                            command=lambda: controller.show_frame("ComboSelection"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        # button2.pack()


class ComboSelection(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        # self.colorRed = tk.Button(self, highlightbackground = "red")
        # self.colorRed.pack({"side": "left"})
        # self.colorRed["command"] = lambda: self.selectCombo(0)

        # self.colorPurple = tk.Button(self, highlightbackground = "purple")
        # self.colorPurple.pack({"side": "left"})
        # self.colorPurple["command"] = lambda: self.selectCombo(1)

        # self.colorGreen = tk.Button(self, highlightbackground = "green")
        # self.colorGreen.pack({"side": "left"})
        # self.colorGreen["command"] = lambda: self.selectCombo(2)

        # self.colorYellow = tk.Button(self, highlightbackground = "yellow")
        # self.colorYellow.pack({"side": "left"})
        # self.colorYellow["command"] = lambda: self.selectCombo(3)

        # self.colorBlue = tk.Button(self, highlightbackground = "blue")
        # self.colorBlue.pack({"side": "left"})
        # self.colorBlue["command"] = lambda: self.selectCombo(4)

        # self.colorMagenta = tk.Button(self, highlightbackground = "magenta")
        # self.colorMagenta.pack({"side": "left"})
        # self.colorMagenta["command"] = lambda: self.selectCombo(5)

        # self.finishedCombo = tk.Button(self)
        # self.finishedCombo["text"] = "OK"
        # self.finishedCombo["command"] =  self.quit

        # self.finishedCombo.pack({"side": "left"})

        # # self.pack()
        # self.colorsSelected = 0
        # self.combo = []

	# def selectCombo(self, color):
	# 	self.colorsSelected = self.colorsSelected + 1
 #    	# print ("Red selected '{}'").format(self.colorsSelected)
 #    	# print ("Red selected '{}'").format(color)
 #    	if self.colorsSelected <= 4:
 #    		self.combo.append(color)
 #    	else:
	# 		tkMessageBox.showwarning("Oops!", "Looks like you have already selected a combination!")
    # def __init__(self, parent, controller):
    #     tk.Frame.__init__(self, parent)
    #     self.controller = controller
    #     label = tk.Label(self, text="This is page 1", font=controller.title_font)
    #     label.pack(side="top", fill="x", pady=10)
    #     button = tk.Button(self, text="Go to the start page",
    #                        command=lambda: controller.show_frame("StartPage"))
    #     button.pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()




# class Mastermind(tk.Tk):

# 	def __init__(self, *args, **kwargs):
# 		tk.Tk.__init__(self, *args, **kwargs)

#         # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         # container.grid_rowconfigure(0, weight=1)
#         # container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
        
#         for F in (StartPage):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#             # frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame("StartPage")

# 	def show_frame(self, page_name):
# 		frame = self.frames[page_name]
#         frame.tkraise()

# class StartPage(tk.Frame):
# 	# def say_hi(self):
# 	# 	print ("hi there, everyone!")
	
# 	# def createWidgets(self):
# 	# 	self.QUIT = Button(self)
#  #        self.QUIT["text"] = "QUIT"
#  #        self.QUIT["fg"]   = "red"
#  #        self.QUIT["command"] =  self.quit

#  #        self.QUIT.pack({"side": "left"})

#  #        self.hi_there = Button(self)
#  #        self.hi_there["text"] = "Hello",
#  #        self.hi_there["command"] = self.say_hi

#  #        self.hi_there.pack({"side": "left"})

#  #        self.colorRed = Button(self, highlightbackground = "red")
#  #        self.colorRed.pack({"side": "left"})
#  #        self.colorRed["command"] = lambda: self.selectCombo(0)

#  #        self.colorPurple = Button(self, highlightbackground = "purple")
#  #        self.colorPurple.pack({"side": "left"})
#  #        self.colorPurple["command"] = lambda: self.selectCombo(1)

#  #        self.colorGreen = Button(self, highlightbackground = "green")
#  #        self.colorGreen.pack({"side": "left"})
#  #        self.colorGreen["command"] = lambda: self.selectCombo(2)

#  #        self.colorYellow = Button(self, highlightbackground = "yellow")
#  #        self.colorYellow.pack({"side": "left"})
#  #        self.colorYellow["command"] = lambda: self.selectCombo(3)

#  #        self.colorBlue = Button(self, highlightbackground = "blue")
#  #        self.colorBlue.pack({"side": "left"})
#  #        self.colorBlue["command"] = lambda: self.selectCombo(4)

#  #        self.colorMagenta = Button(self, highlightbackground = "magenta")
#  #        self.colorMagenta.pack({"side": "left"})
#  #        self.colorMagenta["command"] = lambda: self.selectCombo(5)

#  #        self.finishedCombo = Button(self)
#  #        self.finishedCombo["text"] = "OK"
#  #        self.finishedCombo["command"] =  self.quit

#  #        self.finishedCombo.pack({"side": "left"})


# 	# def selectCombo(self, color):
# 	# 	self.colorsSelected = self.colorsSelected + 1
#  #    	print ("Red selected '{}'").format(self.colorsSelected)
#  #    	print ("Red selected '{}'").format(color)
#  #    	if self.colorsSelected <= 4:
#  #    		self.combo.append(color)
#  #    	else:
# 	# 		tkMessageBox.showwarning("Oops!", "Looks like you have already selected a combination!")

# 	def __init__(self, parent, controller):
# 		tk.Frame.__init__(self, parent)
#         self.controller = controller
#         # self.pack()
#         # self.createWidgets()
#         self.colorsSelected = 0
#         self.combo = []

#     # def __init__(self, parent, controller):
#     #     tk.Frame.__init__(self, parent)
#     #     self.controller = controller
#     #     label = tk.Label(self, text="This is the start page", font=controller.title_font)
#     #     label.pack(side="top", fill="x", pady=10)

#     #     button1 = tk.Button(self, text="Go to Page One",
#     #                         command=lambda: controller.show_frame("PageOne"))
#     #     button2 = tk.Button(self, text="Go to Page Two",
#     #                         command=lambda: controller.show_frame("PageTwo"))
#     #     button1.pack()
#     #     button2.pack()


# # root = Tk()
# # # style = Tk.Style()
# # # style.theme_use('classic')
# # app = Mastermind(master=root)
# # app.master.title("My Do-Nothing Application")
# # app.master.maxsize(1000, 400)
# # app.master.minsize(width=666, height=666)
# # app.mainloop()
# # root.destroy()

# if __name__ == "__main__":
# 	app = Mastermind()
# 	app.mainloop()
# 	# app.master.maxsize(1000, 400)
# 	# app.master.minsize(width=666, height=666)
#     # app.mainloop()










=======
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


>>>>>>> 2c8f62959181de4a78f90fffaa30d6a5123ccf36
