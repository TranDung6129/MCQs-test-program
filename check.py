from tkinter import *
from tkinter import ttk
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

question_set = pandas.read_csv("./tests/testform50.csv")
questions = question_set.question.to_list()
choices = question_set.choices.to_list()
answer = question_set.answer.to_list()
final_qs_set = []

for i in range(len(question_set)):

    to_add = {"question": questions[i], "choices": choices[i].split('| '), "answer": answer[i].split("| ")}
    final_qs_set.append(to_add)

print(final_qs_set)