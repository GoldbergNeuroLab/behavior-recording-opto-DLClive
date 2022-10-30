# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:35:15 2022

@author: somarowtha and goffk
"""
import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk
from queue import Queue
from datetime import date,datetime
from tkinter import filedialog
import os
import sys

    
def gen_name():
    global new_file_name
    new_file_name = "KG"+experiment.get()+"_m"+mouse.get()+"_"+fieldn.get()
    final_lbl.configure(text=new_file_name)
    print("Saving data as " + new_file_name)


def update_frame():
    global after_id

    if not frame_queue.empty():
        video_label.image_frame = ImageTk.PhotoImage(frame_queue.get_nowait())
        video_label.config(image=video_label.image_frame)
    
    after_id = root.after(10, update_frame)
    
    
def start_capture():
    
    fr=float(FR_val.get())
    file_size=float(Time_limit.get())
    camindex = int(Cam_Select.get())
    frame_ct=0
    global capture

    # print(camindex)
    
    frame_ct=0
    today=date.today()
    now=datetime.now()
    if not os.path.exists(dir_n + '\\'+ today.strftime("%m_%d_%y")):
        os.mkdir(dir_n + '\\'+ today.strftime("%m_%d_%y"))

    
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    fname=dir_n + '\\' + today.strftime("%m_%d_%y") +'\\' + new_file_name + "_" + now.strftime("%m_%d_%y_%H_%M_%S") + '.mp4'
    video_writer = cv2.VideoWriter(fname, fourcc, fr, (640, 480))
    capture = cv2.VideoCapture(camindex)
    while running:
        
        rect, frame =  capture.read()

        if rect:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            videoImg = Image.fromarray(cv2image)
            # current_frame = ImageTk.PhotoImage(image = videoImg)
            frame_queue.put(videoImg)
            video_writer.write(frame)
            frame_ct=frame_ct+1
            
            if frame_ct >= file_size*60*30:
                video_writer.release()
                frame_ct=0
                today=date.today()
                now=datetime.now()
                capture.release()
            
    capture.release()
    video_writer.release()



def start_rec():
    global running

    stop_rec()

    running = True
    thread = threading.Thread(target=start_capture, daemon=True)
    thread.start()
    update_frame()


def start_stream():
    global running
    
    stop_rec()

    running = True
    thread = threading.Thread(target=streaming, daemon=True)
    thread.start()
    update_frame()

def streaming():

    camindex = int(Cam_Select.get())

    global capture

    
    capture = cv2.VideoCapture(camindex)
    while running:
    
        rect, frame =  capture.read()

        if rect:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            videoImg = Image.fromarray(cv2image)
            # current_frame = ImageTk.PhotoImage(image = videoImg)
            frame_queue.put(videoImg)
   
    capture.release()

    
    
def stop_rec():
    global running, after_id
    running = False

    if after_id:
        root.after_cancel(after_id)
        after_id = None
        
    with frame_queue.mutex:
        frame_queue.queue.clear()
        
    
def closeWindow(root):
    stop_rec()
    root.destroy()

def sel_dir():
    global dir_n
    dir_n=filedialog.askdirectory()
    

    
running = False
after_id = None
frame_queue = Queue()

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", closeWindow)
root.title("Video Recording")

orig_lbl = tk.Label(root, text="Directory")
orig_lbl.grid(column=0, row=1)

FR_val= tk.Entry(root,width=15)
FR_val.grid(column=2, row=1)
FR_val.insert(0,30)

lbl5 = tk.Label(root, text="FRAMERATE (Hz)")
lbl5.grid(column=2, row=0)

Time_limit= tk.Entry(root,width=15)
Time_limit.grid(column=3, row=1)
Time_limit.insert(0,15)

Cam_Select= tk.Entry(root,width=15)
Cam_Select.grid(column=7, row=1)
Cam_Select.insert(0,0)

lbl5 = tk.Label(root, text="Time Limit (Min)")
lbl5.grid(column=3, row=0)

orig_lbl = tk.Label(root, text="Select Cam")
orig_lbl.grid(column=8, row=1)

video_label = tk.Label(root)
video_label.grid(column=2,row=3,columnspan=7, rowspan=2)

experiment = tk.Entry(root,width=15, text = "XXX")
experiment.grid(column=1, row=3)

mouse = tk.Entry(root,width=15, text = "XXXX")
mouse.grid(column=1, row=4)

fieldn = tk.Entry(root,width=15, text = "XXXXX")
fieldn.grid(column=1, row=5)


lbl1 = tk.Label(root, text="experiment number")
lbl1.grid(column=0, row=3)

lbl2 = tk.Label(root, text="mouse number")
lbl2.grid(column=0, row=4)

lbl3 = tk.Label(root, text="Experiment")
lbl3.grid(column=0, row=5)

final_lbl = tk.Label(root, text="KGXXXcellmXXXXX")
final_lbl.grid(column=1, row=6)


#buttons with functions 

orig_btn = tk.Button(root, text="Set Directory",command=sel_dir)
orig_btn.grid(column=0, row=0)

str_btn =tk.Button(root, text='Start Streaming',command=start_stream)
str_btn.grid(column=6, row=1)

name_file = tk.Button(root, text="Generate name",command=gen_name)
name_file.grid(column=0, row=6)

rec_btn =tk.Button(root, text='Start Recording',command=start_rec)
rec_btn.grid(column=6, row=0)

stp_btn =tk.Button(root, text='Stop Recording',command=stop_rec)
stp_btn.grid(column=7, row=0)

qt_btn =tk.Button(root, text='Quit Application',command=root.destroy)
qt_btn.grid(column=8, row=0)




root.mainloop()

