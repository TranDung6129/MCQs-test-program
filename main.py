from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import time
import random
from tkinter import filedialog as fd
import pandas
import math
import sympy as sp
import numpy
import os.path
from functools import partial

timer = None


# Main Screen
class MainScreen(Tk):
    """Main screen of the software, including buttons for users to choose depending on the purpose of use,
    the username box for users to enter a name to distinguish it from other users of other software on the same
    computer. """

    def __init__(self):
        super().__init__()

        self.title("Lựa chọn")
        self.geometry("800x600")
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)

        self.display_canvas()
        self.display_label()
        self.display_button()
        self.display_register_system()

    def display_canvas(self):
        # Canvas
        self.canvas = Canvas(self, width=800, height=600)
        self.start_image = Image.open("images/image_1.png")
        self.start_image = self.start_image.resize((800, 600), Image.ANTIALIAS)
        self.start_image = ImageTk.PhotoImage(self.start_image)
        self.canvas.create_image(-400, 0, anchor=NW, image=self.start_image)
        self.canvas.config(highlightthickness=0)
        self.canvas.create_text(150, 90, text="Chương trình\nlàm bài thi \ntrắc nghiệm",
                                font=('Oswald', 32, "bold"),
                                fill="#26603A")
        self.canvas.create_text(705, 585, text="Trần Mạnh Dũng - 20206129", font=("Oswald", 10))
        self.canvas.grid(column=0, row=0, rowspan=2, columnspan=2)

    def display_label(self):
        self.welcome = Label(self, text="WELCOME", font=('Oswald', 32, "bold"), fg="#1E9052")
        self.welcome.place(x=480, y=45)

        self.notif_1 = Label(self, text="Import or create your own test", font=('Oswald', 10))
        self.notif_1.place(x=510, y=100)

    def display_button(self):
        self.import_mode_but = Button(self, text="IMPORT", bg="#E7F492", width=20, height=1,
                                      font=('Oswald', 15, "bold"),
                                      fg="#451111", command=self.import_mode)
        self.import_mode_but.place(x=472, y=160)

        self.create_mode_but = Button(self, text="CREATE", bg="#99CCFF", width=20, height=1,
                                      font=('Oswald', 15, "bold"),
                                      fg="#451111", command=self.create_mode)
        self.create_mode_but.place(x=472, y=220)

        self.test_history_but = Button(self, text="HISTORY", width=20, height=1, font=("Oswald", 15, "bold"),
                                       command=self.history_mode)
        self.test_history_but.place(x=472, y=280)

    def display_register_system(self):
        self.username_box = Entry(self, bg="#99D7AE", font=('Oswald', 15))
        self.username_box.place(x=472, y=360, width=250, height=25)

        self.username_label = Label(self, text="USERNAME:", font=('Oswald', 10))
        self.username_label.place(x=470, y=335)

    def check_register(self):

        res = ""
        username = self.username_box.get()
        self.isExist = os.path.exists(f"./userdata/{username}")

        if username == "":
            res = messagebox.askyesno(title="Enter your username",
                                      message="Please enter your user name, if you don't have "
                                              "one, click 'Yes' to create new")
            if res:
                self.check_to_add_username()
            else:
                return False

        elif not self.isExist:
            res = messagebox.askyesno(title="User not found",
                                      message="Check your username again or click 'Yes' button to create new")
            if res:
                self.check_to_add_username()
            else:
                return False

        else:

            messagebox.showinfo(title="Success", message="Login successfully")
            return True

    def check_to_add_username(self):

        self.new_username = simpledialog.askstring(title="Add username", prompt="Enter new username: ")

        if self.new_username == None or self.new_username == "":
            messagebox.showerror(title="Error", message="Please enter your new username")
        elif self.isExist:
            messagebox.showerror(title="Error",
                                 message=f"Username \"{self.new_username}\" already exist, please choose another")
        else:
            print(self.new_username)
            os.makedirs(f"./userdata/{self.new_username}")
            messagebox.showinfo(title="Success", message="Create new user successfully")

    def import_mode(self):
        if self.check_register():
            self.import_window = ImportFile(self)
            self.import_window.grab_set()

    def create_mode(self):
        if self.check_register():
            self.create_window = CreateFile(self)
            self.create_window.grab_set()

    def history_mode(self):
        if self.check_register():
            self.history_window = CheckHistory(self)
            self.history_window.grab_set()


class ImportFile(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Nhập đề")
        self.geometry("800x600")
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)

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

        self.instruction_label = Label(self, text="IMPORT FILE", font=("Oswald", 40, "bold"))
        self.instruction_label.place(x=235, y=20)

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
        self.timer_box_minute.insert(END, "0")
        self.timer_box_minute.place(x=200, y=202, width=100, height=30)

        self.timer_second_label = Label(self, text="Seconds", font=("Oswald", 15))
        self.timer_second_label.place(x=310, y=242)
        self.timer_box_second = Entry(self, font=("Oswald", 15), justify="right")
        self.timer_box_second.place(x=200, y=242, width=100, height=30)
        self.timer_box_second.insert(END, "30")

    def display_button(self):
        self.choose_file_but = Button(self, text="Import", font=("Oswald", 15), command=self.choose_file)
        self.choose_file_but.place(x=680, y=100, height=35, width=80)
        self.filepath_box.place(x=200, y=100, width=470, height=34)

        self.back_button = Button(self, text="Back", bg="white", font=('Oswald', 15), command=self.destroy)
        self.back_button.place(x=550, y=530, width=100, height=30)

        self.next_button = Button(self, text="Next", bg="white", font=('Oswald', 15), command=self.start_test)
        self.next_button.place(x=660, y=530, width=100, height=30)

        self.instruction_button = Button(self, text="I", font=("Oswald", 10, "bold"), command=self.display_instruction)
        self.instruction_button.place(x=580, y=38, width=30, height=30)

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

        self.label_random_ques = Label(self, text="Shuffle question: ", font=("Oswald", 15))
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

    def display_instruction(self):

        with open("files/instruction_import.txt") as instruction:
            self.instruction_content = messagebox.showinfo(title="Instruction", message=instruction.read())

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


class CreateFile(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Tạo đề")
        self.geometry("680x600")
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)
        self.menubar = Menu(self)

        self.display_label()
        self.display_button()
        self.display_entry()
        self.display_menu()

        self.filename = ""
        self.import_filepath = ""
        self.new_test_name = ""

        self.cur_adding = 0

        self.questions = []
        self.choices = []
        self.answer = []
        self.questions_dict = {"question": self.questions,
                               "choices": self.choices,
                               "answer": self.answer}

        self.temp_question = []

        self.config(menu=self.menubar)

    def choose_file(self):
        filetypes = (
            ('csv files', "*.csv"),
        )
        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

    def display_label(self):

        self.create_label = Label(self, text="CREATE TEST", font=("Oswald", 30, "bold"))
        self.create_label.grid(column=0, row=0, columnspan=2)

        self.question_label = Label(self, text="Question: ", font=("Oswald", 15))
        self.question_label.grid(column=0, row=1, padx=10, sticky=W)

        self.choice_label = Label(self, text="Choices: ", font=("Oswald", 15))
        self.choice_label.grid(column=0, row=4, padx=10, sticky=W)

        self.answer_label = Label(self, text="Answer: ", font=("Oswald", 15))
        self.answer_label.grid(column=0, row=7, padx=10, sticky=W)

    def display_button(self):

        self.create_button = Button(self, text="Create", font=("Oswald", 15), width=8, command=self.create_question)
        self.create_button.grid(column=0, row=10, pady=10, sticky=E)

    def display_entry(self):

        self.question_entry = Text(self, font=("Oswald", 15), width=60, height=5)
        self.question_entry.grid(column=0, row=2, padx=10, rowspan=2, columnspan=2)

        self.choice_entry = Text(self, font=("Oswald", 15), width=60, height=5)
        self.choice_entry.grid(column=0, row=5, padx=10, rowspan=2, columnspan=2)

        self.answer_entry = Text(self, font=("Oswald", 15), width=60, height=5)
        self.answer_entry.grid(column=0, row=8, padx=10, rowspan=2, columnspan=2)

    def display_menu(self):

        file = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file)
        file.add_command(label="Open...", command=self.import_exist_file)
        file.add_command(label="Save", command=self.export_file)
        file.add_separator()
        file.add_command(label="Exit", command=self.exit_button)

        edit = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=edit)
        edit.add_command(label="Change...", command=self.adjust_test)

        help_ = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_)
        help_.add_command(label="Instruction", command=self.instruction_create_test)

    def clear_question(self):

        self.question_entry.delete("1.0", END)

    def clear_answer(self):

        self.answer_entry.delete("1.0", END)

    def clear_choices(self):

        self.choice_entry.delete("1.0", END)

    def create_question(self):

        self.temp_question = []
        question = self.question_entry.get("1.0", "end-1c")
        choices = self.choice_entry.get("1.0", "end-1c")
        answer = self.answer_entry.get("1.0", "end-1c")

        self.temp_question.append(question)
        self.temp_question.append(choices)
        self.temp_question.append(answer)

        if len(self.temp_question) < 3:
            for value, content in enumerate(self.temp_question, 0):
                if self.temp_question[value] == "":
                    messagebox.showerror(title="Error", message="Some field haven't enter, please fill it and try "
                                                                "again!")
                break
        else:
            for value, content in enumerate(self.temp_question, 0):
                if self.temp_question[value] == "":
                    messagebox.showerror(title="Error", message="Some field haven't enter, please fill it and try "
                                                                "again!")
                break
            self.questions_dict["question"].append(question)
            self.questions_dict["choices"].append(choices)
            self.questions_dict["answer"].append(answer)

            self.clear_question()
            self.clear_choices()
            self.clear_answer()

    def export_file(self):

        file_exist = False
        self.new_test_name = simpledialog.askstring(title="Add file", prompt="New test file name: ")
        try:
            os.path.exists(f"./tests/{self.new_test_name}.csv")

        except TypeError:
            messagebox.showerror(title="Invalid file name", message="Please enter file name")
        else:
            file_exist = os.path.exists(f"./tests/{self.new_test_name}.csv")

        res = ""
        nos = ""

        if file_exist:
            nos = messagebox.askyesnocancel(title="File already exist", message="This file already exist, do you want "
                                                                                "to replace this file?")
            if nos:
                self.check_to_add_file()

        else:
            self.check_to_add_file()

    def check_to_add_file(self):

        if self.new_test_name is None or self.new_test_name == "":
            messagebox.showerror(title="Invalid file name", message="Please enter file name")

        else:

            if len(self.questions_dict["question"]) == 0:
                messagebox.showerror(title="Nothing exist in test",
                                     message="Look like you didn't add anything to test, please add at least one "
                                             "question to save test")
            else:
                res = messagebox.askyesno(title="Export File", message="Are you sure to export file?")
                if res:
                    question_file = pandas.DataFrame.from_dict(self.questions_dict)
                    question_file.to_csv(f"./tests/{self.new_test_name}.csv", index=False)
                messagebox.showinfo(title="Success", message="File export successfully")

    def check_to_ask_question(self):
        pass

    def exit_button(self):
        is_back = messagebox.askokcancel(title="Warning", message="Are you sure to exit, all progress will lost")
        if is_back:
            self.destroy()

    def adjust_test(self):
        adjust_test_screen = AdjustTest(self)
        adjust_test_screen.grab_set()

    def instruction_create_test(self):

        with open("files/instruction_export.txt") as instruction:
            self.instruction_content = messagebox.showinfo(title="Instruction", message=instruction.read())

    def import_exist_file(self):
        try:
            self.choose_file()
            filepath = self.filename
            pandas.read_csv(filepath)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File no exist or you haven't provide file path!")
        else:
            messagebox.showinfo(title="Success", message="File import successfully")

            self.import_filepath = self.filename
            questions_df = pandas.read_csv(self.import_filepath)

            self.questions = questions_df["question"].to_list()
            self.choices = questions_df["choices"].to_list()
            self.answer = questions_df["answer"].to_list()

            self.questions_dict = {"question": self.questions,
                                   "choices": self.choices,
                                   "answer": self.answer}

            if len(self.questions) == 0:
                self.cur_adding = 0
            else:
                self.cur_adding = len(self.questions)

            # self.questions_dict.index = np.arange(1, len(self.questions_dict) + 1)
            # self.questions_dict = self.questions_dict.to_dict()


class AdjustTest(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Làm bài")
        self.geometry("800x600")
        self.display_sorry()
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)

    def display_sorry(self):
        self.sorry = Label(self, text="This function is under development, sorry about the inconvenience",
                           font=("Oswald", 15, "bold"))
        self.sorry.grid(column=0, row=1)

        self.back = Button(self, text="OK", font=("Oswald", 15), command=self.destroy)
        self.back.grid(column=0, row=2)


class CheckHistory(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Lịch sử")
        self.geometry("800x600")
        self.display_label()
        self.display_button()
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)

    def display_label(self):
        self.sorry = Label(self, text="This function is under development, sorry about the inconvenience",
                           font=("Oswald", 15, "bold"))
        self.sorry.grid(column=0, row=1)

    def display_button(self):
        self.back = Button(self, text="OK", font=("Oswald", 15), command=self.destroy)
        self.back.grid(column=0, row=2)

    def check_history(self):
        pass


class TestOn(Toplevel):

    def __init__(self, parent, filepath, turn_back, suffle, hard, test_name, test_time):
        super().__init__(parent)

        self.title("Làm bài")
        self.geometry("1100x600")
        icon = PhotoImage(file="./images/hust_logo.png")
        self.iconphoto(False, icon)

        self.cur_pos = 0
        self.mark = 0
        self.radio_but = []
        self.check_but = []

        self.check_but_state = []
        self.your_mul_choice = []
        self.mul_answers = []

        self.qs_button_list = {}

        self.show_page = IntVar()
        self.show_page.set(1)

        self.question_bar_page = {}

        # Radiobut Answer
        self.one_choice_but = StringVar()
        self.one_choice_but.set("off")

        # Read Question file
        self.question_set = pandas.read_csv(filepath)
        self.questions = self.question_set.question.to_list()
        self.choices = self.question_set.choices.to_list()
        self.answer = self.question_set.answer.to_list()
        self.final_qs_set = []

        self.input_question_file()

        if suffle == 1:
            random.shuffle(self.final_qs_set)

        if hard == 1:
            messagebox.showinfo(title="Sorry", message="Hard mode is under development, sorry for the inconvenience")

        if turn_back == 1:
            self.display_question_choose_bar()
            self.display_spinbox()

        self.display_question()
        self.display_choices()
        self.display_divider()

        self.display_time(test_time)
        self.display_test_name(test_name, turn_back)
        self.display_question_num()
        self.display_button(turn_back)

        self.manipulate_qs_bar()
        print(self.question_bar_page)

    def input_question_file(self):

        for i in range(self.num_of_question()):
            to_add = {"question": self.questions[i], "choices": self.choices[i].split('| '),
                      "answer": self.answer[i].split("| ")}
            self.final_qs_set.append(to_add)

    def display_question_choose_bar(self):
        for i in range(1, self.num_of_question() + 1):
            self.qs_button_list[i] = Button(self, text=i, height=2, width=4,
                                            command=partial(self.get_user_click, but=i))
            if 25 * (self.show_page.get() - 1) + i <= 9:
                self.qs_button_list[i].config(text=f"0{25 * (self.show_page.get() - 1) + i}")
                self.qs_button_list[i].place(x=820 + 50 * ((i - 1) % 5), y=60 + 50 * ((i - 1) // 5))
            else:
                self.qs_button_list[i].place(x=820 + 50 * ((i - 1) % 5), y=60 + 50 * ((i - 1) // 5))

    def manipulate_qs_bar(self):

        for page in range(1, self.num_of_question() // 25 + 1 + 1):
            self.question_bar_page[page] = []

        for i in self.qs_button_list:
            if i % 25 == 0:
                self.question_bar_page[i / 25].append(self.qs_button_list[i])
            else:
                self.question_bar_page[i // 25 + 1].append(self.qs_button_list[i])

    def display_spinbox(self):

        label = Label(self, text="Page: ", font=("Oswald", 15))
        label.place(x=820, y=360)
        if self.num_of_question() % 25 == 0:
            spin_qs_box = Spinbox(self, from_=1, to=self.num_of_question() / 25, textvariable=self.show_page,
                                  command=self.display_question_choose_bar)
        else:
            spin_qs_box = Spinbox(self, from_=1, to=self.num_of_question() // 25 + 1, textvariable=self.show_page,
                                  command=self.display_question_choose_bar)

        spin_qs_box.place(width=80, height=30, x=880, y=360)

    def get_user_click(self, but):
        print(self.qs_button_list[but].cget("text"))

    def go_to_qs(self):
        """Trả về câu hỏi ở vị trí đúng với số hiển thị trên nút, cùng với đó là hiển thị các lựa chọn không có sự thay đổi gì nếu
        như người dùng đã chọn phương án trả lời cho câu hỏi đó"""
        self.question_box.delete("1.0", END)

    def display_question(self):
        """Những câu hỏi đã trả lời được đổi màu trên thanh lựa chọn câu hỏi sang màu khác."""
        self.question_box = Text(self, font=("Oswald", 15), height=5, width=72)
        self.question_box.grid(column=0, row=2, columnspan=3, sticky=W)

        self.question_box.delete("1.0", END)
        self.question_box.insert(END, self.final_qs_set[self.cur_pos]["question"])
        self.question_box.config(state=DISABLED)

    def display_time(self, test_time):

        # Timer
        self.timer_label = Label(self, text=f"00:00:00", font=("Oswald", 15))
        self.timer_label.grid(column=2, row=0, sticky=E)
        self.timer_countdown(test_time)

    def display_question_num(self):

        # Question number
        self.question_num = Label(self, text=f"Question {self.cur_pos + 1}/{len(self.questions)}", font=("Oswald", 15))
        self.question_num.grid(column=0, row=1, sticky=W)

    def display_divider(self):

        divider = ttk.Separator(self, orient=VERTICAL, style="TSeparator", takefocus=1, cursor="man")
        divider.grid(column=3, row=0, rowspan=8, pady=10, padx=10, ipady=200)

    def display_test_name(self, test_name, turn_back):
        # Subject
        self.subj_name = Label(self, text=f"{test_name}", font=("Oswald", 15))
        self.subj_name.grid(column=0, row=0, sticky=W)

        if turn_back == 1:
            self.question_nof = Label(self, text="Questions", font=("Oswald", 15))
            self.question_nof.grid(column=4, row=0, columnspan=5, sticky=S)

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
        self.submit_question = Button(self, text="Submit", font=("Oswald", 15), width=10, command=self.submit)
        self.submit_question.grid(column=0, row=7, sticky=W)

    def display_one_choice_answer(self):

        for value, radio_button in enumerate(self.radio_but, 0):
            radio_button.config(
                text=f"{self.final_qs_set[self.cur_pos]['choices'][value]}")

    def display_mul_choices_answer(self):

        for value, check_button in enumerate(self.check_but, 0):
            check_button.config(
                text=f"{self.final_qs_set[self.cur_pos]['choices'][value]}")

    def display_choices(self):

        if self.num_of_answer() == 1:
            self.one_choice()
            self.display_one_choice_answer()
        else:
            self.mul_choice()
            self.display_mul_choices_answer()

    def num_of_answer(self):
        return len(self.final_qs_set[self.cur_pos]["answer"])

    def num_of_question(self):
        return len(self.questions)

    def one_choice(self):

        self.radio_but = []
        self.one_choice_but.set("off")

        for value, choice in enumerate(self.final_qs_set[self.cur_pos]["choices"], 1):
            radio_button = WrappingRadiobutton(self, text="", variable=self.one_choice_but,
                                               value=self.final_qs_set[self.cur_pos]["choices"][value - 1],
                                               justify="left")
            radio_button.grid(column=0, row=2 + value, columnspan=3, sticky=W)

            self.radio_but.append(radio_button)

    def mul_choice(self):

        self.check_but = []
        self.check_but_state = []

        for value, choice in enumerate(self.final_qs_set[self.cur_pos]["choices"], 1):
            self.mul_choice_but = StringVar()
            self.mul_choice_but.set("off")

            check_button = WrappingCheckbutton(self,
                                               text="",
                                               variable=self.mul_choice_but,
                                               onvalue=f"{self.final_qs_set[self.cur_pos]['choices'][value - 1]}",
                                               offvalue="off",
                                               justify="left")
            check_button.grid(column=0, row=value + 2, columnspan=3, sticky=W)

            self.check_but_state.append(self.mul_choice_but)
            self.check_but.append(check_button)

        # for value, check_button in enumerate(self.check_but, 0):
        #     self.check_but[value].deselect()

    def check_answer(self):

        if self.num_of_answer() == 1:

            if not self.one_choice_but.get() == "off":
                if self.one_choice_but.get() == self.final_qs_set[self.cur_pos]["answer"][0]:
                    return True

        self.your_mul_choice = []

        if self.num_of_answer() > 1:

            for value, choice in enumerate(self.check_but_state, 0):
                if not choice.get() == "off":
                    self.your_mul_choice.append(choice.get())

            self.mul_answers = self.final_qs_set[self.cur_pos]["answer"]
            self.mul_answers.sort()
            self.your_mul_choice.sort()

            if self.mul_answers == self.your_mul_choice:
                return True

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
            messagebox.showinfo(title=f"Time is up!", message=f"Your result is {self.mark}/{self.num_of_question()}")
            self.destroy()

    def next_qus(self):

        if self.check_answer():
            self.mark += 1

        self.cur_pos += 1

        if self.cur_pos == self.num_of_question():

            messagebox.showinfo(title="Complete!",
                                message=f"You complete all question\nYour result is {self.mark}/{self.num_of_question()}")
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
            res = messagebox.askyesno(title="Test hasn't complete",
                                      message="You haven't complete the test, are you "
                                              "sure to submit?")
            if res == True:
                messagebox.showinfo(title="Complete",
                                    message=f"You complete your test with result {self.mark}/{self.num_of_question()}")
                self.destroy()


class WrappingCheckbutton(Checkbutton):
    """a type of Checkbutton that automatically adjusts the wrap to the size"""

    def __init__(self, master, **kwargs):
        Checkbutton.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=master.winfo_width() - 40))


class WrappingRadiobutton(Radiobutton):
    """a type of Radiobutton that automatically adjusts the wrap to the size"""

    def __init__(self, master=None, **kwargs):
        Radiobutton.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=master.winfo_width() - 40))


if __name__ == "__main__":
    program = MainScreen()
    program.mainloop()
