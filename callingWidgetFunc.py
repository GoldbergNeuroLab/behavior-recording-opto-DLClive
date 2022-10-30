# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:53:48 2022

@author: kevin
"""

import tkinter as tk

class Widgets(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.initUI()

    def initUI(self):

        # Lots of other different tkinter widgets go here

        self.button = tk.Button(text='hello', command=self.parent.get_details)
        self.button.pack()

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.initUI()

    def get_details(self):

        self.widgets.button.config(text='goodbye')

    def initUI(self):

        self.parent.title("My Application")

        self.pack()

        self.widgets = Widgets(self)
        self.widgets.pack(side="top", anchor="center", fill="both", expand=True)

if __name__ == "__main__":

    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.resizable(0,0)
    root.mainloop()