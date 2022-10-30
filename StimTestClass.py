# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:25:29 2022

@author: kevin
"""
import tkinter as tk

class StimTest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Test Stimulation")
        label.grid(column=0, row=0)

        button1 = tk.Button(self, text="R",
                            command=lambda: controller.show_frame(controller.Record))
        button1.grid(column=0, row=1)


        button2 = tk.Button(self, text="RS",
                            command=lambda: controller.show_frame(controller.RecordAndStim))
        button2.grid(column=0, row=2)


    