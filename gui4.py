from tkinter import *                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from combinatorics import all_colours



class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ComboSelection, PlayGame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Welcome! Let's play Mastermind!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Select your color code",
                            command=lambda: controller.show_frame("ComboSelection"))
        button1.pack()


class ComboSelection(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Select 4 colors for your combination and click OK", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        buttonRed = Button(self, text="Red", command=lambda: self.selectCombo(0))
        buttonBlue = Button(self, text="Blue", command=lambda: self.selectCombo(1))
        buttonMagenta = Button(self, text="Magenta", command=lambda: self.selectCombo(2))
        buttonGreen = Button(self, text="Green", command=lambda: self.selectCombo(3))
        buttonPurple = Button(self, text="Purple", command=lambda: self.selectCombo(4))
        buttonYellow = Button(self, text="Yellow", command=lambda: self.selectCombo(5))
        
        ### figure out how to pass the combo from one frame to the next ###   from controller??
        buttonOK = Button(self, text="OK", command=lambda: self.getCombo())
        buttonPlay = Button(self, text="Let's play!", command=lambda: controller.show_frame("PlayGame"))

        button.pack()
        buttonRed.pack()
        buttonBlue.pack()
        buttonMagenta.pack()
        buttonGreen.pack()
        buttonPurple.pack()
        buttonYellow.pack()
        buttonOK.pack()
        buttonPlay.pack()
        
        self.colorsSelected = 0
        self.combo = []

yellow, red blue, green

    def selectCombo(self, color):
      self.colorsSelected = self.colorsSelected + 1
      if self.colorsSelected <= 4:
          self.combo.append(color)
      else:
          pass
          # tkMessageBox.showwarning("Oops!", "Looks like you have already selected a combination!")

    def getCombo(self):
        print (("Your combo is '{}'").format(self.combo))
        return self.combo


class PlayGame(Frame):

    def inconsistent(p, guesses):
        for guess in guesses:
          res = check(guess[0], p)
          (rightly_positioned, permutated) = guess[1]
        if res != [rightly_positioned, permutated]:
         return True # inconsistent
        return False # i.e. consistent


    def reasonable(right, color):
        return not ((right + color > 4) or (right + color < 2) or (right == 3 and color == 1))


    def get_evaluation():
        rightly_positioned = int(entryWidget_both.get())
        permutated = int(entryWidget_only_colours.get())
        return (rightly_positioned, permutated)

    def new_evaluation(self, current_colour_choices):
        rightly_positioned, permutated = get_evaluation()
        if rightly_positioned == number_of_positions:
            return(current_colour_choices, (rightly_positioned, permutated))
  
        if not reasonable(rightly_positioned, permutated):
            print("Input Error: Sorry, the input makes no sense")
            return(current_colour_choices, (-1, permutated))
        guesses.append((current_colour_choices, (rightly_positioned, permutated)))
        view_guesses()
  
        current_colour_choices = create_new_guess() 
        self.show_current_guess(current_colour_choices)
        if not current_colour_choices:
            return(current_colour_choices, (-1, permutated))
        return(current_colour_choices, (rightly_positioned, permutated))

    def check(p1, p2):
        blacks = 0
        whites = 0
        for i in range(len(p1)):
            if p1[i] == p2[i]:
                blacks += 1
            else:
                if p1[i] in p2:
                    whites += 1
        return [blacks, whites] 


    def create_new_guess():
        next_choice = next(permutation_iterator) 
        while inconsistent(next_choice, guesses):
          try:
             next_choice = next(permutation_iterator)
          except StopIteration:
             print("Error: Your answers were inconsistent!")
             return ()
        return next_choice


    def new_evaluation_tk():
        global current_colour_choices
        res = new_evaluation(current_colour_choices)
        current_colour_choices = res[0]


    def show_current_guess(self, new_guess):
        row = 1 
        Label(self, text="   New Guess:   ").grid(row=row, column=0, columnspan=4)
        row +=1
        col_count = 0
        for c in new_guess:
            print(c)
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1


    def view_guesses():
        row = 3
        Label(self, text="Old Guesses").grid(row=row, column=0, columnspan=4)
        Label(self, text="c&p").grid(row=row, padx=5, column=number_of_positions + 1)
        Label(self, text="p").grid(row=row, padx=5, column=number_of_positions + 2)
        
        # dummy label for distance:
        Label(self, text="         ").grid(row=row, column=number_of_positions + 3)


        row += 1
        # vertical dummy label for distance:
        Label(self, text="             ").grid(row=row, column=0, columnspan=5)

        for guess in guesses:
            guessed_colours = guess[0]
            col_count = 0
            row += 1
            for c in guessed_colours:
                print(guessed_colours[col_count])
                l = Label(self, text="    ", bg=guessed_colours[col_count])
                l.grid(row=row,column=col_count,  sticky=W, padx=2)
                col_count += 1
          # evaluation:
            for i in (0,1):
                l = Label(self, text=str(guess[1][i]))
                l.grid(row=row,column=col_count + i + 1, padx=2)


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Select 4 colors for your combination and click OK", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


        colours = ["red","green","blue","yellow","orange","pink"]
        guesses = []       
        number_of_positions = 4

        permutation_iterator = all_colours(colours, number_of_positions)
        current_colour_choices = next(permutation_iterator)

        new_guess = (current_colour_choices, (0,0))

        row_offset = 1
        # root = Tk()
        # root.title("Mastermind")
        # root["padx"] = 30
        # root["pady"] = 20   

        entryLabel = Label(self)
        entryLabel["text"] = "Completely Correct:"
        entryLabel.grid(row=row_offset, sticky=E, padx=5, column=number_of_positions + 4)
        entryWidget_both = Entry(self)
        entryWidget_both["width"] = 5
        entryWidget_both.grid(row=row_offset, column=number_of_positions + 5)

        entryLabel = Label(self)
        entryLabel["text"] = "Wrong Position:"
        entryLabel.grid(row=row_offset+1, sticky=E, padx=5, column= number_of_positions + 4)
        entryWidget_only_colours = Entry(self)
        entryWidget_only_colours["width"] = 5
        entryWidget_only_colours.grid(row=row_offset+1, column=number_of_positions + 5)

        submit_button = Button(self, text="Submit", command= lambda: self.new_evaluation_tk)
        submit_button.grid(row=4,column=number_of_positions + 4)

        # quit_button = Button(self, text="Quit", command=self.quit)
        # quit_button.grid(row=4,column=number_of_positions + 5)
        self.show_current_guess(current_colour_choices)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()









