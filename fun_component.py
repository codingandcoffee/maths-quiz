from tkinter import *
from functools import partial
import re
import random


class Quiz:
    def __init__(self):

        self.menu_frame = Frame(width=300, pady=10)
        self.menu_frame.grid()

        self.main_menu_label = Label(self.menu_frame, text="Main Maths Menu", justify=CENTER, font="Helvetica 16", padx=10, pady=10)
        self.main_menu_label.grid(row=0)

        self.question_number = 0

        self.quiz_number = 0

        self.quiz_history = []

        self.results_string = ""

        self.quiz_list = []

        self.quiz_string = ""

        self.show_history = ""

        self.correct_number = 0

        self.question_list = []

        self.correct_answers = []

        self.answers = []

        self.overall_score = 0

        self.score = 0

        self.selection_label = Label(self.menu_frame, text="Select Quiz", justify=CENTER)
        self.selection_label.grid(row=1)

        self.operations_frame = Frame()
        self.operations_frame.grid()

        self.addition_button = Button(self.operations_frame, text="Addition +", command=lambda: self.generate_questions("Addition"), padx=10)
        self.addition_button.grid(row=4, column=1)

        self.subtraction_button = Button(self.operations_frame, text="Subtraction -", command=lambda: self.generate_questions("Subtraction"), padx=10)
        self.subtraction_button.grid(row=4, column=2)

        self.multiplication_button = Button(self.operations_frame, text="Multiplication x", command=lambda: self.generate_questions("Multiplication"), padx=10)
        self.multiplication_button.grid(row=4, column=3)

        self.division_button = Button(self.operations_frame, text="Division /", command=lambda: self.generate_questions("Division"), padx=10)
        self.division_button.grid(row=4, column=4)

        self.quiz_frame = Frame()
        self.quiz_frame.grid()

        self.operation_label = Label(self.quiz_frame, text="", justify=CENTER)
        self.operation_label.grid(row=1, column=0)

        self.start_button = Button(self.quiz_frame, text="Start", command=lambda: self.display_question(), state=DISABLED, justify=CENTER)
        self.start_button.grid(row=2, column=0)

        self.question_label = Label(self.quiz_frame, text="Questions will appear here.", justify=CENTER)
        self.question_label.grid(row=3, column=0)

        self.answer_entry = Entry(self.quiz_frame, state=DISABLED, justify=CENTER)
        self.answer_entry.grid(row=4, column=0)

        self.result_label = Label(self.quiz_frame, text="", justify=CENTER)
        self.result_label.grid(row=5, column=0)

        self.buttons_frame = Frame()
        self.buttons_frame.grid()

        self.check_button = Button(self.buttons_frame, text="Check", state=DISABLED, command=lambda: self.check())
        self.check_button.grid(row=0, column=0)

        self.next_button = Button(self.buttons_frame, text="Next", state=DISABLED, command=lambda: self.next())
        self.next_button.grid(row=0, column=1)

        self.quit_button = Button(self.buttons_frame, text="Quit", state=DISABLED, command=self.close_quiz)
        self.quit_button.grid(row=0, column=2)

        self.history_button = Button(self.buttons_frame, state=DISABLED, text="View History", command=lambda: self.show_results(self.quiz_history))
        self.history_button.grid(row=0, column=3)

        self.export_frame = Frame()
        self.export_frame.grid()

        self.show_export_button = Button(self.export_frame, text="Export", justify=CENTER, state=DISABLED, command=lambda: self.export(self.quiz_history))
        self.show_export_button.grid(row=2, column=1)

        self.fun_zone_button = Button(self.export_frame, text="Fun Zone", justify=CENTER, state=DISABLED, command=self.fun)
        self.fun_zone_button.grid(row=2, column=2)

        self.help_button = Button(self.export_frame, text="Help", justify=CENTER)
        self.help_button.grid(row=2, column=3)

    def export(self, quiz_history):
        Export(self, quiz_history)

    def fun(self):
        Fun(self)

    def generate_questions(self, operation):

        for i in range(2):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)

            if operation == "Addition":
                question = "{} + {} = ?".format(num1, num2)
                correct_answer = num1 + num2

            elif operation == "Subtraction":
                question = "{} - {} = ?".format(num1, num2)
                correct_answer = num1 - num2

            elif operation == "Multiplication":
                question = "{} x {} = ?".format(num1, num2)
                correct_answer = num1 * num2

            else:
                while num1 % num2 != 0:
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                question = "{} / {} = ?".format(num1, num2)
                correct_answer = num1 / num2

            self.question_list.append(question)
            self.correct_answers.append(correct_answer)
            self.start_button.config(state=NORMAL)

        self.addition_button.config(state=DISABLED)
        self.subtraction_button.config(state=DISABLED)
        self.multiplication_button.config(state=DISABLED)
        self.division_button.config(state=DISABLED)

    def display_question(self):
        self.answer_entry.config(state=NORMAL)
        self.quit_button.config(state=NORMAL)
        self.question_label.configure(text=self.question_list[self.question_number])
        self.check_button.config(state=NORMAL)
        self.history_button.config(state=DISABLED)

    def check(self):
        self.check_button.config(state=DISABLED)
        answer = self.answer_entry.get()
        try:

            if int(answer) == self.correct_answers[self.question_number]:
                self.correct_number += 1
                self.result_label.configure(text="Correct!")
            else:
                self.result_label.configure(text="Incorrect!")

            self.answers.append(answer)
            self.next_button.config(state=NORMAL)

        except ValueError:
            # Forces the user to add valid input i.e. a number or integer, no blanks or strings
            self.result_label.configure(text="Enter a number!")
            self.answer_entry.configure(bg="red")

    def next(self):
        self.check_button.config(state=NORMAL)
        self.question_number += 1
        self.result_label.configure(text="")
        self.answer_entry.delete(0, END)
        if self.question_number == len(self.question_list):
            self.show_export_button.config(state=NORMAL)
            self.next_button.config(state=DISABLED)
            self.question_label.configure(text="")
            self.start_button.config(state=DISABLED)
            self.addition_button.config(state=NORMAL)
            self.subtraction_button.config(state=NORMAL)
            self.multiplication_button.config(state=NORMAL)
            self.division_button.config(state=NORMAL)
            self.answer_entry.delete(0, END)
            self.answer_entry.config(state=DISABLED)
            self.result_label.configure(text="")
            self.quit_button.config(state=DISABLED)
            self.check_button.config(state=DISABLED)
            self.score += self.correct_number / self.question_number * 100
            self.question_label.configure(text="Score: {}%".format(self.score))
            self.overall_score += self.score / 100
            if self.score == 100:
                self.fun_zone_button.config(state=NORMAL)
            self.quiz_number += 1

            for question in self.question_list:
                index = self.question_list.index(question)
                self.quiz_string += question + "    " + str(self.correct_answers[index]) + "     " + "You entered: " + str(self.answers[index])

            self.quiz_history.append(["Quiz no. ", str(self.quiz_number), "Score: ", str(self.score), "\n", self.quiz_string, "\n"])

            self.history_button.config(state=NORMAL)

            self.quit_button.config(state=DISABLED)



        else:
            # shows the next question
            self.display_question()
            self.next_button.config(state=DISABLED)

    def close_quiz(self):
        self.question_list.clear()
        self.answers.clear()
        self.correct_answers.clear()
        self.question_label.configure(text="")
        self.addition_button.config(state=NORMAL)
        self.subtraction_button.config(state=NORMAL)
        self.multiplication_button.config(state=NORMAL)
        self.division_button.config(state=NORMAL)
        self.answer_entry.delete(0, END)
        self.answer_entry.config(state=DISABLED)
        self.result_label.configure(text="")
        self.quit_button.config(state=DISABLED)
        self.next_button.config(state=DISABLED)
        self.check_button.config(state=DISABLED)
        self.start_button.config(state=DISABLED)


    def show_results(self, quiz_history):
        Results(self, quiz_history)


class Results:
    def __init__(self, partner, quiz_history):

        self.results_box = Toplevel()
        self.results_box.protocol('WM_DELETE_WINDOW', partial(self.close_results, partner))

        self.results_frame = Frame(self.results_box, width=300, padx=10, pady=10)
        self.results_frame.grid()

        self.response_label = Label(self.results_frame, text="Response", justify=CENTER, pady=10, font="Helvetica 12")
        self.response_label.grid(row=0)

        self.heading_label = Label(self.results_frame, text="Questions, Correct Answers, Your Answers", justify=CENTER, pady=10)
        self.heading_label.grid(row=1)

        history_string = ""
        # The following code ensures that only up to the 7 most recent past calculations are shown on the History window
        if len(quiz_history) >= 2:
            for item in range(0, 2):
                history_string += str(quiz_history[len(quiz_history) - item - 1]) + "\n"
        else:
            for item in quiz_history:
                history_string += (str(quiz_history[len(quiz_history) - quiz_history.index(item) - 1]) + "\n")

        self.quiz = Label(self.results_frame, text=history_string, justify=CENTER)
        self.quiz.grid(row=2)

        self.back_button = Button(self.results_frame, text="Back", command=partial(self.close_results, partner))
        self.back_button.grid()

    def close_results(self, partner):
        self.results_box.destroy()


class Fun:
    def __init__(self, partner):

        self.fun_box = Toplevel()
        self.fun_box.protocol('WM_DELETE_WINDOW', partial(self.close_fun, partner))

        self.fun_frame = Frame(self.fun_box, width=300, padx=10, pady=10)
        self.fun_frame.grid()

        self.fun_list = ["Why was six scared of seven? \n Because seven eight nine!", "You don't know maths until you do maths.", "The number 2 is the only even prime number.", "Mathematicians like maths not because they are good at it, but because they like to take on challenges.", "Practice makes perfect!", "Why was the geometry adorable? \n Because it had acute angles!", "All the internal angles in a triangle add to 180 degrees.", "Parallel lines have so much in common...it's a shame they will never meet!", "Which tables do you not have to learn? Dinner tables!", "Why did the teacher get upset when the student called her average? \n Because it was a 'mean' thing to say!"]

        self.response_label = Label(self.fun_frame, text="Fun Zone", justify=CENTER, pady=10, font="Helvetica 12")
        self.response_label.grid(row=0)

        self.fun_fact = random.choice(self.fun_list)

        self.fun = Label(self.fun_frame, text=self.fun_fact, justify=CENTER)
        self.fun.grid(row=2)

        self.back_button = Button(self.fun_frame, text="Back", command=partial(self.close_fun, partner))
        self.back_button.grid()

        partner.fun_zone_button.config(state=DISABLED)

    def close_fun(self, partner):
        self.fun_box.destroy()


class Export:
    def __init__(self, partner, quiz_history):
        background = "white"
        partner.show_export_button.config(state=DISABLED)
        self.export_box = Toplevel()
        # Headings, buttons and labels outlined below
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        self.export_frame = Frame(self.export_box, width=300, bg=background)
        self.export_frame.grid()
        self.how_heading = Label(self.export_frame, text="Export", bg=background, font="Helvetica 12")
        self.how_heading.grid(row=0)
        self.export_text = Label(self.export_frame, text="Save your results to a text file.", justify=LEFT, width=40, bg=background)
        self.export_text.grid(row=1)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, its content will be replaced with your calculation history.", justify=LEFT, bg="#ffafaf", fg="maroon", font="Arial 10 italic", padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)
        # The user enters a filename below
        self.filename_entry = Entry(self.export_frame, width=20, justify=LEFT)
        self.filename_entry.grid(row=3, pady=10)
        self.save_error_label = Label(self.export_frame, text="", fg="red", bg=background)
        self.save_error_label.grid(row=4)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)
        # The save history function is called when the save button is clicked - to confirm the validity of the filename
        self.save_button = Button(self.save_cancel_frame, text="Save", command=partial(lambda: self.save_quiz(partner, quiz_history)))
        self.save_button.grid(row=5, column=0)
        # The window closes should the user choose to click Cancel
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=5, column=1)

        # Close export function called to close the Export window if user cancels
    def close_export(self, partner):
        partner.show_export_button.config(state=NORMAL)
        self.export_box.destroy()
        # The save history function that confirms the validity of the filename before successfully exporting it

    def save_quiz(self, partner, quiz_history):
        valid_char = "[A-Za-z0-9_]" # Common way out outlining filename conditions
        has_error = "no"
        # User enters filename here
        filename = self.filename_entry.get()
        print(filename)
    # Checks filename to rule out blank spaces and apostrophes - forces the user to enter a valid filename
        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "(no spaces allowed)"
            else:
                problem = ("(no {}'s allowed)".format(letter))
            has_error = "yes"
            break


        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

# If there are errors, the type of error is displayed
        if has_error == "yes":
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            self.filename_entry.config(bg="pink")
            print()
        else: # Otherwise, the file is successfully exported
            filename = filename + ".txt"
            f = open(filename, "w+")
            for item in quiz_history:
                f.write(item + "\n")
            f.close()

            self.close_export(partner) # Export window closes after operation is successfully complete


# main routine
max_quiz_number = 4
if __name__ == "__main__":
    root = Tk()
    root.title("Maths Quiz")
    something = Quiz()
    root.mainloop()
