from tkinter import *
from functools import partial
import re
import random


class Menu:
    def __init__(self):

        self.menu_frame = Frame()
        self.menu_frame.grid()

        self.main_menu_label = Label(text="Main Maths Menu")
        self.main_menu_label.grid()

        self.selection_label = Label(text="Select Quiz:")
        self.selection_label.grid()

        self.addition_button = Button(text="+", command=lambda: self.generate_questions("Addition"))
        self.addition_button.grid()

        self.subtraction_button = Button(text="-", command=lambda: self.generate_questions("Subtraction"))
        self.subtraction_button.grid()

        self.multiplication_button = Button(text="x", command=lambda: self.generate_questions("Multiplication"))
        self.multiplication_button.grid()

        self.division_button = Button(text="/", command=lambda: self.generate_questions("Division"))
        self.division_button.grid()

        self.show_statistics_button = Button(text="Statistics")
        self.show_statistics_button.grid()

    def generate_questions(self, operation):
        question_list = []
        correct_answers = []
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

            question_list.append(question)
            correct_answers.append(correct_answer)

        Quiz(self, operation, question_list, correct_answers)


class Quiz:
    def __init__(self, partner, operation, question_list, correct_answers):

        partner.addition_button.config(state=DISABLED)
        partner.subtraction_button.config(state=DISABLED)
        partner.multiplication_button.config(state=DISABLED)
        partner.division_button.config(state=DISABLED)

        self.quiz_box = Toplevel()
        self.quiz_box.protocol('WM_DELETE_WINDOW', partial(self.close_quiz, partner))

        self.quiz_frame = Frame(self.quiz_box)
        self.quiz_frame.grid()

        self.question_number = 0

        self.correct_number = 0

        self.answers = []

        self.operation_label = Label(self.quiz_frame, text="{} Quiz".format(operation))
        self.operation_label.grid()

        self.start_button = Button(self.quiz_frame, text="Start", command=lambda: self.display_question(question_list, correct_answers))
        self.start_button.grid()

        self.question_label = Label(self.quiz_frame, text="Question will appear here.")
        self.question_label.grid()

        self.answer_entry = Entry(self.quiz_frame, state=DISABLED)
        self.answer_entry.grid()

        self.result_label = Label(self.quiz_frame)
        self.result_label.grid()

        self.check_button = Button(self.quiz_frame, text="Check", state=DISABLED, command=lambda: self.check(correct_answers))
        self.check_button.grid()

        self.next_button = Button(self.quiz_frame, text="Next", state=DISABLED, command=lambda: self.next(question_list, correct_answers))
        self.next_button.grid()

        self.quit_button = Button(self.quiz_frame, text="Quit", command=partial(self.close_quiz, partner))
        self.quit_button.grid()

    # The close_history function closes the History window when "dismissed" and the export function is also called below.

    def display_question(self, question_list, correct_answers):
        self.answer_entry.config(state=NORMAL)
        self.question_label.configure(text=question_list[self.question_number])
        self.check_button.config(state=NORMAL)

    def check(self, correct_answers):
        self.check_button.config(state=DISABLED)
        answer = self.answer_entry.get()
        if int(answer) == correct_answers[self.question_number]:
            self.correct_number += 1
            self.result_label.configure(text="Correct!")
        else:
            self.result_label.configure(text="Incorrect!")
        self.answers.append(answer)
        self.next_button.config(state=NORMAL)


    def next(self, question_list, correct_answers):
        self.check_button.config(state=NORMAL)
        self.question_number += 1
        self.result_label.configure(text="")
        quiz_string = ""
        self.answer_entry.delete(0, END)
        if self.question_number == len(question_list):
            self.check_button.config(state=DISABLED)
            self.next_button.config(state=DISABLED)
            self.question_label.configure(text="Score: {} out of {}".format(self.correct_number, self.question_number))
            for question in question_list:
                index = question_list.index(question)

                quiz_string += question + str(self.answers[index]) + "  " + str(correct_answers[index]) + "\n"
            self.next_button.configure(text="View Response", command=lambda: self.show_results(quiz_string))
            self.next_button.config(state=NORMAL)
            self.quit_button.configure(text="Menu", command=self.close_quiz)
        else:
            # shows the next question
            self.display_question(question_list, correct_answers)
            self.next_button.config(state=DISABLED)

    def close_quiz(self, partner):
        partner.addition_button.config(state=NORMAL)
        partner.subtraction_button.config(state=NORMAL)
        partner.multiplication_button.config(state=NORMAL)
        partner.division_button.config(state=NORMAL)
        self.quiz_box.destroy()

    def show_results(self, quiz_string):
        Results(self, quiz_string)


class Results:
    def __init__(self, partner, quiz_string):

        self.results_box = Toplevel()
        self.results_box.protocol('WM_DELETE_WINDOW', partial(self.close_results, partner))

        self.results_frame = Frame(self.results_box)
        self.results_frame.grid()

        self.heading_label = Label(self.results_frame, text="Questions, Answers, Correct Answers")

        self.quiz = Label(self.results_frame, text="")
        self.quiz.grid(row=0)
        # Holds all previous calculations



        # Historical calculations are shown here
        self.quiz.configure(text=quiz_string)
        # The Export and Dismiss buttons are outlined below

        self.back_button = Button(self.results_frame, text="Back", command=partial(self.close_results, partner))
        self.back_button.grid()

        self.export_button = Button(self.results_frame, text="Export", command=lambda: self.export(quiz_string))
        self.export_button.grid()





    def close_results(self, partner):
        self.results_box.destroy()


    def export(self, quiz_string):
        Export(self, quiz_string)

# The Export window


class Export:
    def __init__(self, partner, quiz_string):
        #print(calc_history)
        background = "white"
        partner.export_button.config(state=DISABLED)
        self.export_box = Toplevel()
        # Headings, buttons and labels outlined below
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        self.export_frame = Frame(self.export_box, width=300, bg=background)
        self.export_frame.grid()
        self.how_heading = Label(self.export_frame, text="Export", bg=background)
        self.how_heading.grid(row=0)
        self.export_text = Label(self.export_frame, text="Save your results to a text file.", justify=LEFT, width=40, bg=background)
        self.export_text.grid(row=1)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, its content will be replaced with your calculation history.", justify=LEFT, bg="#ffafaf", fg="maroon", font="Arial 10 italic", padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)
        # The user enters a filename below
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold", justify=LEFT)
        self.filename_entry.grid(row=3, pady=10)
        self.save_error_label = Label(self.export_frame, text="", fg="red", bg=background)
        self.save_error_label.grid(row=4)
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)
        # The save history function is called when the save button is clicked - to confirm the validity of the filename
        self.save_button = Button(self.save_cancel_frame, text="Save", command=partial(lambda: self.save_quiz(partner, quiz_string)))
        self.save_button.grid(row=5, column=0)
        # The window closes should the user choose to click Cancel
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=5, column=1)

        # Close export function called to close the Export window if user cancels
    def close_export(self, partner):
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()
        # The save history function that confirms the validity of the filename before successfully exporting it

    def save_quiz(self, partner, quiz_string):
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
            for item in quiz_string:
                f.write(item + "\n")
            f.close()

            self.close_export(partner) # Export window closes after operation is successfully complete




# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Maths Quiz")
    something = Menu()
    root.mainloop()
