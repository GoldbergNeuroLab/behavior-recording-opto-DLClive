# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:56:23 2022

@author: kevin
"""
import tkinter as tk

class RecordAndStim(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Record with Stim")
        label.grid(column=0, row=0)

        button1 = tk.Button(self, text="R",
                            command=lambda: controller.show_frame(controller.Record))
        button1.grid(column=0, row=1)


        button2 = tk.Button(self, text="ST",
                            command=lambda: controller.show_frame(controller.StimTest))
        button2.grid(column=0, row=2)