from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
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


class QuestionChooseBox(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Choose question")
        self.geometry("200x600")

    def display_button(self):

        pass


question_choose = Tk()
question_choose.title("Qs")
question_choose.geometry("300x600")
question_nums = 50
for i in range(question_nums):
    button = Button(text=f"{i + 1}", height=1, width=2)
    if i < 9:
        button.config(text=f"0{i + 1}")
        button.grid(column=i % 5, row=i // 5, padx=2, pady=2)
    else:
        button.grid(column=i % 5, row=i // 5, padx=2, pady=2)

question_choose.mainloop()
