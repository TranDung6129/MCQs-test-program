from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
import sqlite3
from PIL import Image, ImageTk
import time
import random
from tkinter import filedialog as fd
import pandas
import math

timer = None


class MainScreen(Tk):

    def __init__(self):
        super().__init__()

        self.title("Lựa chọn")
        self.geometry("800x600")

        # Canvas
        canvas = Canvas(self, width=800, height=600)
        self.start_image = Image.open("Images/image_1.png")
        self.start_image = self.start_image.resize((800, 600), Image.ANTIALIAS)
        self.start_image = ImageTk.PhotoImage(self.start_image)
        canvas.create_image(-400, 0, anchor=NW, image=self.start_image)
        canvas.config(highlightthickness=0)
        canvas.create_text(150, 90, text="Chương trình\nlàm bài thi \ntrắc nghiệm",
                           font=('Oswald', 32, "bold"),
                           fill="#26603A")
        canvas.create_text(705, 585, text="Trần Mạnh Dũng - 20206129", font=("Oswald", 10))
        canvas.grid(column=0, row=0, rowspan=2, columnspan=2)

        welcome = Label(self, text="WELCOME", font=('Oswald', 32, "bold"), fg="#1E9052")
        welcome.place(x=480, y=45)

        notif_1 = Label(self, text="Import or create your own test", font=('Oswald', 10))
        notif_1.place(x=510, y=100)

        import_mode_but = Button(self, text="IMPORT", bg="#E7F492", width=20, height=1,
                                 font=('Oswald', 15, "bold"),
                                 fg="#451111", command=self.import_mode)
        import_mode_but.place(x=472, y=160)

        create_mode_but = Button(self, text="CREATE", bg="#99CCFF", width=20, height=1,
                                 font=('Oswald', 15, "bold"),
                                 fg="#451111", command=self.create_mode)
        create_mode_but.place(x=472, y=220)

        username = Entry(self, bg="#99D7AE", font=('Oswald', 15))
        username.place(x=472, y=300, width=250, height=25)

    def import_mode(self):
        import_window = ImportFile(self)
        import_window.grab_set()

    def create_mode(self):
        create_window = CreateFile(self)
        create_window.grab_set()


class ImportFile(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Nhập đề")
        self.geometry("800x600")

        self.display_label()
        self.display_timerbox()
        self.display_checkbox()
        self.display_button()

    # input csv file
    def choose_file(self):
        filetypes = (
            ('csv files', "*.csv"),
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.filepath_box.insert(END, filename)

    def display_label(self):
        self.filepath_label = Label(self, text="Path: ", font=("Oswald", 15))
        self.filepath_label.place(x=90, y=102)
        self.filepath_box = Entry(self, font=("Oswald", 15))

        self.label_subject = Label(self, text="Test name: ", font=("Oswald", 15))
        self.label_subject.place(x=90, y=302)
        self.entry_subject = Entry(self, font=("Oswald", 15))
        self.entry_subject.insert(END, "Bài thi thử")
        self.entry_subject.place(x=400, y=302)

    def display_timerbox(self):
        # Timer box
        self.timer_label = Label(self, text="Set time: ", font=("Oswald", 15))
        self.timer_label.place(x=90, y=162)

        self.timer_hour_label = Label(self, text="Hours", font=("Oswald", 15))
        self.timer_hour_label.place(x=310, y=162)
        self.timer_box_hour = Entry(self, font=("Oswald", 15), justify="right")
        self.timer_box_hour.place(x=200, y=162, width=100, height=30)
        self.timer_box_hour.insert(END, "0")

        self.timer_minute_label = Label(self, text="Minutes", font=("Oswald", 15))
        self.timer_minute_label.place(x=310, y=202)
        self.timer_box_minute = Entry(self, font=("Oswald", 15), justify="right")
        self.timer_box_minute.insert(END, "45")
        self.timer_box_minute.place(x=200, y=202, width=100, height=30)

        self.timer_second_label = Label(self, text="Seconds", font=("Oswald", 15))
        self.timer_second_label.place(x=310, y=242)
        self.timer_box_second = Entry(self, font=("Oswald", 15), justify="right")
        self.timer_box_second.place(x=200, y=242, width=100, height=30)
        self.timer_box_second.insert(END, "0")

    def display_button(self):
        self.choose_file_but = Button(self, text="Import", font=("Oswald", 15), command=self.choose_file)
        self.choose_file_but.place(x=680, y=100, height=35, width=80)
        self.filepath_box.place(x=200, y=100, width=470, height=34)

        self.back_button = Button(self, text="Back", bg="white", font=('Oswald', 15), command=self.destroy)
        self.back_button.place(x=550, y=530, width=100, height=30)

        self.next_button = Button(self, text="Next", bg="white", font=('Oswald', 15), command=self.start_test)
        self.next_button.place(x=660, y=530, width=100, height=30)

    def display_checkbox(self):
        self.turn_back_var = IntVar()
        self.turn_back_var.set(2)

        self.label_turn_back = Label(self, text="Allow back to previous quesion: ", font=("Oswald", 15))
        self.label_turn_back.place(x=90, y=362)
        self.turn_back_check_box_yes = Checkbutton(self, variable=self.turn_back_var, onvalue=1, offvalue=2,
                                                   text="Yes")
        self.turn_back_check_box_yes.place(x=400, y=360)
        self.turn_back_check_box_no = Checkbutton(self, variable=self.turn_back_var, onvalue=2, offvalue=1,
                                                  text="No")
        self.turn_back_check_box_no.place(x=500, y=360)

        self.random_qs_var = IntVar()
        self.random_qs_var.set(2)

        self.label_random_ques = Label(self, text="Suffle question: ", font=("Oswald", 15))
        self.label_random_ques.place(x=90, y=422)
        self.random_check_box_yes = Checkbutton(self, variable=self.random_qs_var, onvalue=1, offvalue=2,
                                                text="Yes")
        self.random_check_box_yes.place(x=400, y=420)
        self.random_check_box_no = Checkbutton(self, variable=self.random_qs_var, onvalue=2, offvalue=1, text="No")
        self.random_check_box_no.place(x=500, y=420)

        self.hard_mode_var = IntVar()
        self.hard_mode_var.set(2)

        self.label_mode = Label(self, text="Hard mode: ", font=("Oswald", 15))
        self.label_mode.place(x=90, y=482)
        self.mode_check_box_yes = Checkbutton(self, variable=self.hard_mode_var, onvalue=1, offvalue=2, text="Yes")
        self.mode_check_box_yes.place(x=400, y=480)
        self.mode_check_box_box_no = Checkbutton(self, variable=self.hard_mode_var, onvalue=2, offvalue=1,
                                                 text="No")
        self.mode_check_box_box_no.place(x=500, y=480)

    def get_time(self):
        hours = int(self.timer_box_hour.get())
        minutes = int(self.timer_box_minute.get())
        second = int(self.timer_box_second.get())

        test_time = hours * 3600 + minutes * 60 + second

        return test_time

    def get_user_choice(self, var):
        return var.get()

    def start_test(self):
        try:
            filepath = self.filepath_box.get()
            pandas.read_csv(filepath)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File do not exist or you haven't provide file path!")
        else:
            test_screen = TestOn(self, filepath=filepath,
                                 turn_back=self.get_user_choice(self.turn_back_var),
                                 suffle=self.get_user_choice(self.random_qs_var),
                                 hard=self.get_user_choice(self.hard_mode_var),
                                 test_name=self.entry_subject.get(),
                                 test_time=self.get_time())
            test_screen.grab_set()
            # program.destroy()


class CreateFile(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Tạo đề")
        self.geometry("800x600")


class TestOn(Toplevel):

    def __init__(self, parent, filepath, turn_back, suffle, hard, test_name, test_time):
        super().__init__(parent)

        self.title("Làm bài")
        self.geometry("800x600")

        self.cur_pos = 0
        self.mark = 0
        self.radio_but = []
        self.check_but = []

        # Checkbox Answers
        self.one_choice_but = IntVar()
        self.one_choice_but.set(0)

        # Read Question file
        self.question_set = pandas.read_csv(filepath)
        self.questions = self.question_set.question.to_list()
        if suffle == 1:
            random.shuffle(self.questions)

        self.display_question()
        self.display_choices()

        self.display_time(test_time)
        self.display_test_name(test_name)
        self.display_question_num()
        self.display_button(turn_back)

        # random.shuffle(self.questions)

    def display_question(self):

        self.question_box = Text(self, font=("Oswald", 15), height=5, width=72)
        self.question_box.grid(column=0, row=2, columnspan=3, sticky=S)

        self.cur_question = self.questions[self.cur_pos]
        self.question_box.delete("1.0", END)
        self.question_box.insert(END, self.cur_question)

    def display_time(self, test_time):

        # Timer
        self.timer_label = Label(self, text=f"00:00:00", font=("Oswald", 15))
        self.timer_label.grid(column=2, row=0, sticky=E)
        self.timer_countdown(test_time)

    def display_question_num(self):

        # Question number
        self.question_num = Label(self, text=f"Question {self.cur_pos + 1}/{len(self.questions)}", font=("Oswald", 15))
        self.question_num.grid(column=0, row=1, sticky=W)

    def display_test_name(self, test_name):
        # Subject
        self.subj_name = Label(self, text=f"{test_name}", font=("Oswald", 15))
        self.subj_name.grid(column=0, row=0, sticky=W)

    def display_button(self, turn_back):

        # Next Qus
        self.next_button = Button(self, text="Next", font=("Oswald", 15), width=14, command=self.next_qus)
        self.next_button.grid(column=2, row=7, sticky=E)

        if turn_back == 1:
            # Previous Qus
            self.previous_button = Button(self, text="Previous", font=("Oswald", 15), width=14,
                                          command=self.previous_qus)
            self.previous_button.grid(column=2, row=7, sticky=W)

        # Submit
        self.submit_question = Button(self, text="Submit", font=("Oswald", 15), width=10)
        self.submit_question.grid(column=0, row=7, sticky=W)

    def display_one_choice_answer(self):

        for value, radio_button in enumerate(self.radio_but, 0):
            radio_button.config(
                text=f"{self.question_set[self.question_set.question == self.cur_question].choices.item().split(', ')[value]}")

    def display_mul_choices_answer(self):

        for value, check_button in enumerate(self.check_but, 0):
            check_button.config(
                text=f"{self.question_set[self.question_set.question == self.cur_question].choices.item().split(', ')[value]}")

    def display_choices(self):

        if self.num_of_answer() == 1:
            self.one_choice()
            self.display_one_choice_answer()
        else:
            self.mul_choice()
            self.display_mul_choices_answer()

    def num_of_answer(self):
        return len(self.question_set[self.question_set.question == self.cur_question].answer.item().split(", "))

    def get_qs_choice(self):
        return self.question_set[self.question_set.question == self.cur_question].choices.item().split(", ")

    def num_of_question(self):
        return len(self.questions)

    def one_choice(self):

        self.radio_but = []
        self.one_choice_but.set(0)

        for value, choice in enumerate(
                self.question_set[self.question_set.question == self.cur_question].choices.item().split(", "), 1):
            radio_button = Radiobutton(self, text="", variable=self.one_choice_but, value=value)
            radio_button.grid(column=0, row=2 + value, sticky=W)
            self.radio_but.append(radio_button)

    def mul_choice(self):

        self.check_but = []

        for value, choice in enumerate(
                self.question_set[self.question_set.question == self.cur_question].choices.item().split(", "), 1):
            check_button = Checkbutton(self, text="", onvalue=value, offvalue=0)
            check_button.grid(column=0, row=value + 2, sticky=W)
            self.check_but.append(check_button)

        for value, check_button in enumerate(self.check_but, 0):
            self.check_but[value].deselect()

    def check_answer(self):

        if self.num_of_answer() == 1:
            if self.question_set[self.question_set.question == self.cur_question].choices.item().split(", ")[
                      self.one_choice_but.get() - 1] == self.question_set[self.question_set.question == self.cur_question].answer.item():
                return True
        if self.num_of_answer() > 1:
            pass
        
    def timer_countdown(self, test_time):

        count_hour = math.floor(test_time / 3600)
        count_min = math.floor((test_time % 3600) / 60)
        count_sec = test_time % 60

        if count_sec < 10:
            count_sec = f"0{count_sec}"

        if count_min < 10:
            count_min = f"0{count_min}"

        if count_hour < 10:
            count_hour = f"0{count_hour}"

        self.timer_label.config(text=f"{count_hour}:{count_min}:{count_sec}")
        if test_time > 0:
            global timer
            timer = self.after(1000, self.timer_countdown, test_time - 1)
        else:
            messagebox.showinfo("Time is up!")

    def next_qus(self):

        if self.check_answer():
            self.mark += 1

        self.cur_pos += 1

        if self.cur_pos == self.num_of_question():

            messagebox.showinfo(title="Complete!",
                                message=f"You complete all question\nYour mark is {self.mark}/{self.num_of_question()}")
            self.destroy()
        else:

            for radio_button in self.radio_but:
                radio_button.grid_remove()

            for check_button in self.check_but:
                check_button.grid_remove()

            self.display_question()
            self.display_choices()

            self.question_num.config(text=f"Question {self.cur_pos + 1}/{len(self.questions)}")

    def previous_qus(self):

        self.cur_pos -= 1

    def submit(self):

        if self.cur_pos < self.num_of_question():
            messagebox.askyesnocancel(title="Test hasn't complete", message="You haven't complete the test, are you "
                                                                            "sure to submit?")


if __name__ == "__main__":
    program = MainScreen()
    program.mainloop()