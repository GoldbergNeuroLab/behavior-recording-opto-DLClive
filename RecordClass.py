# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:25:30 2022

@author: kevin
"""
import cv2
import threading
from PIL import Image, ImageTk
from queue import Queue
from datetime import date,datetime
from tkinter import filedialog
import os
import tkinter as tk

class Record(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Record Behavior")
        label.grid(column=0, row=0)

        self.button = tk.Button(self, text="RS",
                            command=lambda: controller.show_frame(controller.RecordAndStim))
        self.button.grid(column=0, row=1)


        self.button2 = tk.Button(self, text="ST",
                            command=lambda: controller.show_frame(controller.StimTest))
        self.button2.grid(column=0, row=2)


        self.orig_lbl = tk.Label(self, text="Directory")
        self.orig_lbl.grid(column=0, row=3)
        
        self.FR_val= tk.Entry(self,width=15)
        self.FR_val.grid(column=2, row=1)
        self.FR_val.insert(0,30)
        
        self.lbl5 = tk.Label(self, text="FRAMERATE (Hz)")
        self.lbl5.grid(column=2, row=0)
        
        self.Time_limit= tk.Entry(self,width=15)
        self.Time_limit.grid(column=3, row=1)
        self.Time_limit.insert(0,15)
        
        self.Cam_Select= tk.Entry(self,width=15)
        self.Cam_Select.grid(column=7, row=1)
        self.Cam_Select.insert(0,0)
        
        self.lbl5 = tk.Label(self, text="Time Limit (Min)")
        self.lbl5.grid(column=3, row=0)
        
        self.orig_lbl = tk.Label(self, text="Select Cam")
        self.orig_lbl.grid(column=8, row=1)
        
        self.video_label = tk.Label(self)
        self.video_label.grid(column=2,row=3,columnspan=7, rowspan=2)
        
        self.experiment = tk.Entry(self,width=15, text = "XXX")
        self.experiment.grid(column=1, row=4)
        
        self.mouse = tk.Entry(self,width=15, text = "XXXX")
        self.mouse.grid(column=1, row=5)
        
        self.fieldn = tk.Entry(self,width=15, text = "XXXXX")
        self.fieldn.grid(column=1, row=6)
        
        
        self.lbl1 = tk.Label(self, text="experiment number")
        self.lbl1.grid(column=0, row=4)
        
        self.lbl2 = tk.Label(self, text="mouse number")
        self.lbl2.grid(column=0, row=5)
        
        self.lbl3 = tk.Label(self, text="Experiment")
        self.lbl3.grid(column=0, row=6)
        
        self.final_lbl = tk.Label(self, text="KGXXXcellmXXXXX")
        self.final_lbl.grid(column=0, row=7)

        #buttons with functions 
        
        self.orig_btn = tk.Button(self, text="Set Directory",command=self.sel_dir)
        self.orig_btn.grid(column=0, row=0)
        
        self.str_btn =tk.Button(self, text='Start Streaming',command=self.start_stream)
        self.str_btn.grid(column=6, row=1)
        
        self.name_file = tk.Button(self, text="Generate name",command=self.gen_name)
        self.name_file.grid(column=0, row=6)
        
        self.rec_btn =tk.Button(self, text='Start Recording',command=self.start_rec)
        self.rec_btn.grid(column=6, row=0)
        
        self.stp_btn =tk.Button(self, text='Stop Recording',command=self.stop_rec)
        self.stp_btn.grid(column=7, row=0)
        
        self.qt_btn =tk.Button(self, text='Quit Application',command=controller.destroy)
        self.qt_btn.grid(column=8, row=0)
        
        
        self.running = False
        self.after_id = None
        self.frame_queue = Queue()
        self.new_file_name = ""
        self.dir_n = ""
        
        
    def gen_name(self):
        
        self.new_file_name = "KG"+self.experiment.get()+"_m"+self.mouse.get()+"_"+self.fieldn.get()
        self.final_lbl.configure(text=self.new_file_name)
        print("Saving data as " + self.new_file_name)
    
        
        
    def start_capture(self):
        
        
        fr=float(self.FR_val.get())
        file_size=float(self.Time_limit.get())
        camindex = int(self.Cam_Select.get())
        
        frame_ct=0
        today=date.today()
        now=datetime.now()
        if not os.path.exists(self.dir_n + '\\'+ today.strftime("%m_%d_%y")):
            os.mkdir(self.dir_n + '\\'+ today.strftime("%m_%d_%y"))
    
        
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
        fname=self.dir_n + '\\' + today.strftime("%m_%d_%y") +'\\' + self.new_file_name + "_" + now.strftime("%m_%d_%y_%H_%M_%S") + '.mp4'
        video_writer = cv2.VideoWriter(fname, fourcc, fr, (640, 480))
        capture = cv2.VideoCapture(camindex)
        while self.running:
            
            rect, frame =  capture.read()
    
            if rect:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                videoImg = Image.fromarray(cv2image)
                # current_frame = ImageTk.PhotoImage(image = videoImg)
                self.frame_queue.put(videoImg)
                video_writer.write(frame)
                frame_ct=frame_ct+1
                
                if frame_ct >= file_size*60*30:
                    print('Successfully saved file as ' + self.new_file_name + "_" + now.strftime("%m_%d_%y_%H_%M_%S") + '.mp4')
                    break 
                
        capture.release()
        video_writer.release()
        if frame_ct < file_size*60*30:
            print('Recording ended early, saved file as ' + self.new_file_name + "_" + now.strftime("%m_%d_%y_%H_%M_%S") + '.mp4')
        
        
    def streaming(self):
    
        camindex = int(self.Cam_Select.get())
    
    
        
        capture = cv2.VideoCapture(camindex)
        while self.running:
        
            rect, frame =  capture.read()
    
            if rect:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                videoImg = Image.fromarray(cv2image)
                # current_frame = ImageTk.PhotoImage(image = videoImg)
                self.frame_queue.put(videoImg)
       
        capture.release()
        print('Stream ended, ready to record')
        

    def stop_rec(self):
        #nonlocal running, after_id
        self.running = False
    
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
            
        with self.frame_queue.mutex:
            self.frame_queue.queue.clear()                    
    
    def start_rec(self):
        # nonlocal running
        self.running = False
        self.stop_rec()
    
        self.running = True
        thread = threading.Thread(target=self.start_capture, daemon=True)
        thread.start()
        self.update_frame()
    
    
    def start_stream(self):
        # nonlocal running
        self.running = False
        self.stop_rec()
    
        self.running = True
        thread = threading.Thread(target=self.streaming, daemon=True)
        thread.start()
        self.update_frame()
    
    def update_frame(self):
        #nonlocal after_id
    
        if not self.frame_queue.empty():
            self.video_label.image_frame = ImageTk.PhotoImage(self.frame_queue.get_nowait())
            self.video_label.config(image=self.video_label.image_frame)
        
        self.after_id = self.after(10, self.update_frame)
        
    # def closeWindow(self):
    #     self.stop_rec()
    #     controller.destroy()
    
    def sel_dir(self):
        #nonlocal dir_n
        self.dir_n=filedialog.askdirectory()
            
  