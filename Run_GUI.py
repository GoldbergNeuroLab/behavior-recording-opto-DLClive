# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:47:09 2022
from conda consol:
conda activate dlc-live
cd to Directory
python Video_Recording_Behavior.py
@author: kevin
"""
import tkinter as tk
from RecordAndStimClass import RecordAndStim
from RecordClass import Record
from StimTestClass import StimTest


class BehaviorRecorder(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        self.RecordAndStim = RecordAndStim
        self.Record = Record
        self.StimTest = StimTest

        for F in (self.Record, self.RecordAndStim, self.StimTest):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.Record)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



def main():
    app = BehaviorRecorder()

    app.mainloop()
    #print(dir(app.frames))

if __name__ == "__main__":
    main()
