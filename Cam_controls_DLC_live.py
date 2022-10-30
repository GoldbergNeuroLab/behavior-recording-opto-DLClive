# -*- coding: utf-8 -*-
"""
Cam_controls_DLC_live.py

utilities for controlling openCV cameras with Video_Recording_Gui.py

Created on Tue Oct 25 09:20:29 2022

@author: kevin
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




# def start_capture(Time_limit, Cam_Select, FR_val, new_file_name, dir_n):
    
#     fr=float(FR_val.get())
#     file_size=float(Time_limit.get())
#     camindex = int(Cam_Select.get())
#     frame_ct=0
#     global capture, frame_queue, running

#     # print(camindex)
    
#     frame_ct=0
#     today=date.today()
#     now=datetime.now()
#     if not os.path.exists(dir_n + '\\'+ today.strftime("%m_%d_%y")):
#         os.mkdir(dir_n + '\\'+ today.strftime("%m_%d_%y"))

    
#     fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
#     fname=dir_n + '\\' + today.strftime("%m_%d_%y") +'\\' + new_file_name + "_" + now.strftime("%m_%d_%y_%H_%M_%S") + '.avi'
#     video_writer = cv2.VideoWriter(fname, fourcc, fr, (640, 480))
#     capture = cv2.VideoCapture(camindex)
#     while running:
        
#         rect, frame =  capture.read()

#         if rect:
#             cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#             videoImg = Image.fromarray(cv2image)
#             # current_frame = ImageTk.PhotoImage(image = videoImg)
#             frame_queue.put(videoImg)
#             video_writer.write(frame)
#             frame_ct=frame_ct+1
#             if frame_ct==file_size*60*30:
#                video_writer.release()
#                frame_ct=0
#                today=date.today()
#                now=datetime.now()
              
            
#     capture.release()
#     video_writer.release()



# def start_rec(root, Time_limit, Cam_Select,FR_val, new_file_name, dir_n, after_id, frame_queue):
#     global running

#     stop_rec(root, after_id, frame_queue)

#     running = True
#     thread = threading.Thread(target=start_capture(Time_limit, Cam_Select, FR_val, new_file_name, dir_n), daemon=True)
#     thread.start()
#     update_frame()



def start_stream(root, Cam_Select, after_id):
    global running
    
    stop_rec(root, after_id)

    running = True
    thread = threading.Thread(target=streaming(Cam_Select), daemon=True)
    thread.start()
    update_frame()

def streaming(Cam_Select):

    camindex = int(Cam_Select.get())

    global capture, frame_queue

    frame_queue = Queue()
    capture = cv2.VideoCapture(camindex)
    while running:
    
        rect, frame =  capture.read()

        if rect:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            videoImg = Image.fromarray(cv2image)
            # current_frame = ImageTk.PhotoImage(image = videoImg)
            frame_queue.put(videoImg)
   
    capture.release()


# def start_stream(Cam_Select, FR_val, frame_queue, video_label):
    
#     camindex = int(Cam_Select.get())
#     stop_rec(frame_queue)
#     capture = cv2.VideoCapture(camindex)
    
#     running = True
#     while running:
    
#         rect, frame =  capture.read()

#         if rect:
#             cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#             videoImg = Image.fromarray(cv2image)
#             # current_frame = ImageTk.PhotoImage(image = videoImg)
#             frame_queue.put(videoImg)
            
#             # if not frame_queue.empty():
#             #     video_label.image_frame = ImageTk.PhotoImage(frame_queue.get_nowait())
#             #     video_label.config(image=video_label.image_frame)
                
   
#     capture.release()
    
    
    
def stop_rec(root, after_id, frame_queue):
    global running
    running = False

    if after_id:
        root.after_cancel(after_id)
        after_id = None
        
    with frame_queue.mutex:
        frame_queue.queue.clear()
        
    return after_id, frame_queue   

def closeWindow(root):
    stop_rec()
    root.destroy()

def sel_dir():
    dir_n=filedialog.askdirectory()
    return dir_n

