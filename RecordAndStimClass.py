# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:56:23 2022

@author: kevin
"""
import tkinter as tk
from RecordClass import Record
class RecordAndStim(Record):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Record with Stim")
        label.grid(column=1, row=7)

        self.button  = tk.Button(self, text="Record",
                            command=lambda: controller.show_frame(controller.Record))
        self.button .grid(column=0, row=1)


        self.button2 = tk.Button(self, text="Stim Test",
                            command=lambda: controller.show_frame(controller.StimTest))
        self.button2.grid(column=0, row=2)
