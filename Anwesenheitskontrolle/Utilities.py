import sys
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pickle

def get_selected_path():
    tk.Tk().withdraw() # prevents an empty tkinter window from appearing
    return filedialog.askdirectory()

def copy_all_files(src, dest):
    src_files = os.listdir(src)
    count = len(src_files)
    if (dialog_yes_no("Copy files", "Es wurden " + str(count) + " dateien gefunden. Sollen diese kopiert werden?")):
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest)

def dialog_yes_no(title, question):
    return messagebox.askquestion(title, question, icon='warning') == 'yes'

def WriteFile(content, filename, path):
    with open(os.path.join(path, filename), 'wb') as fp :
        pickle.dump(content, fp)

def ReadFile(filename, path):
    file = os.path.join(path, filename)
    with open(file, mode='rb') as fp: # b is important -> binary
        encodeListKnown = pickle.load(fp)
    return encodeListKnown

#def console_query_yes_no(question, default="yes"):
#    """Ask a yes/no question via raw_input() and return their answer.
#    "question" is a string that is presented to the user.
#    "default" is the presumed answer if the user just hits <Enter>.
#            It must be "yes" (the default), "no" or None (meaning
#            an answer is required of the user).
#    The "answer" return value is True for "yes" or False for "no".
#    """
#    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
#    if default is None:
#        prompt = " [y/n] "
#    elif default == "yes":
#        prompt = " [Y/n] "
#    elif default == "no":
#        prompt = " [y/N] "
#    else:
#        raise ValueError("invalid default answer: '%s'" % default)
#    while True:
#        sys.stdout.write(question + prompt)
#        choice = input().lower()
#        if default is not None and choice == "":
#            return valid[default]
#        elif choice in valid:
#            return valid[choice]
#        else:
#            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")