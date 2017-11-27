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

        button1 = tk.Button(self, text="Select your color code",
                            command=lambda: controller.show_frame("ComboSelection"))
        button1.pack()

class ComboSelection(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select 4 colors for your combination and click OK", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        buttonRed = tk.Button(self, text="Red", command=lambda: self.selectCombo(0))
        buttonBlue = tk.Button(self, text="Blue", command=lambda: self.selectCombo(1))
        buttonMagenta = tk.Button(self, text="Magenta", command=lambda: self.selectCombo(2))
        buttonGreen = tk.Button(self, text="Green", command=lambda: self.selectCombo(3))
        buttonPurple = tk.Button(self, text="Purple", command=lambda: self.selectCombo(4))
        buttonYellow = tk.Button(self, text="Yellow", command=lambda: self.selectCombo(5))
        buttonOK = tk.Button(self, text="OK", command=lambda: self.getCombo())

        button.pack()
        buttonRed.pack()
        buttonBlue.pack()
        buttonMagenta.pack()
        buttonGreen.pack()
        buttonPurple.pack()
        buttonYellow.pack()
        buttonOK.pack()
        
        self.colorsSelected = 0
        self.combo = []

    def selectCombo(self, color):
      self.colorsSelected = self.colorsSelected + 1
      if self.colorsSelected <= 4:
          self.combo.append(color)
      else:
          tkMessageBox.showwarning("Oops!", "Looks like you have already selected a combination!")

    def getCombo(self):
        print ("Your combo is '{}'").format(self.combo)
        return self.combo


class playGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome! Let's play Mastermind!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Select your color code",
                            command=lambda: controller.show_frame("ComboSelection"))
        button1.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



