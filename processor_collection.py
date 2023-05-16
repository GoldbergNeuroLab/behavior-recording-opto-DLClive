"""
DeepLabCut Toolbox (deeplabcut.org)
© A. & M. Mathis Labs

Licensed under GNU Lesser General Public License v3.0
"""
import struct
import time
import numpy as np
import serial

from dlclive.processor import Processor, KalmanFilterPredictor


class TC_proc(Processor):
    def __init__(self, lik_thresh=0.85, baudrate=int(9600), **kwargs):

        super().__init__()
        self.lik_thresh = lik_thresh
        self.led_times = []
        self.last_light = 0
        self.led_status = False
        try:
            self.ser = serial.Serial(kwargs["com"], baudrate)
        except:
            print("Unable to connect to COM")

        time.sleep(2)
        print("Using" + kwargs["com"])
        # make sure this matches serial port of arduino

    def switch_led(self, val, ctime):

        if self.led_status != val:
            if ctime - self.last_light > 30:#check every 1s - 30 frames
                #print(val)
            #for testing, trigger every 1s

                self.led_status = val
                if val>0:
                    self.turn_stim_on()
                else:
                    self.turn_stim_off()

                self.last_light = ctime
                self.led_times.append((val, ctime))

    def close_serial(self):
        self.ser.close()

    def turn_stim_on(self):
        # command to activate arduino which runs code with desired stim parameters
        # H will turn on, will run until receives L
        self.ser.write(b'H')
        print("sent H")

    def turn_stim_off(self):
        self.ser.write(b"L")
        print("sent L")


    def process(self, pose, **kwargs):

        ### bodyparts
        #0 Mouse nose
        #1 Mouse neck
        #2 Mouse tail base
        #3 Mouse tail tip
        #4 empty cage front
        #5 empty cage top
        #6 empty cage bottom
        #7 empty cage back
        #8 mouse cage front
        #9 mouse cage top
        #10 mouse cage bottom
        #11 mouse cage back
        #12 empty chamber top
        #13 empty chamber bottom
        #14 mouse chamber top
        #15 mouse chamber bottom
        if kwargs['frame_time'] > 9000 and kwargs['frame_time'] < 18001:#only start stimulating during 5-10min

            nose = pose[0, 0:2] if pose[0, 2] > self.lik_thresh else None
            neck = pose[1, 0:2] if pose[1, 2] > self.lik_thresh else None
            front_of_mcage = pose[8, 0:2] if pose[8, 2] > self.lik_thresh else None
            front_of_empty = pose[4, 0:2] if pose[4, 2] > self.lik_thresh else None

            if nose is not None and neck is not None and kwargs['frame_time'] is not None and front_of_empty is not None and front_of_mcage is not None:
                head = (nose + neck) / 2
                distance_to_novel_mouse = sum((head-front_of_mcage)**2)**0.5
                distance_to_empty_cage = sum((head-front_of_empty)**2)**0.5

                if distance_to_novel_mouse < 110: #quick math, width of tank =  /~620 pixels. radius to front of cage = 3cm/110 pixels
                    self.switch_led(val = True, ctime = kwargs['frame_time'])

                else:
                    self.switch_led(val = False, ctime = kwargs['frame_time'])

        if kwargs['frame_time'] == 18100:
            self.switch_led(val = False, ctime = kwargs['frame_time'])

        return pose

    def save(self, filename):

        ### save stim on and stim off times

        if filename[-4:] != ".csv":
            filename += ".csv"
        arr = np.array(self.led_times, dtype=float)
        #np.save(filename, arr)

        #print(arr)
        np.savetxt(filename, arr, delimiter=',', fmt ='%f')
        save_code = True

        return save_code

class OF_proc(Processor):

    def __init__(self, lik_thresh=0.85, baudrate=int(9600), **kwargs):

        super().__init__()
        self.lik_thresh = lik_thresh
        self.led_times = []
        self.last_light = 0
        self.led_status = False
        try:
            self.ser = serial.Serial(kwargs["com"], baudrate)
        except:
            print("Unable to connect to COM")

        time.sleep(2)
        print("Using" + kwargs["com"])
        # make sure this matches serial port of arduino

    def switch_led(self, val, ctime):

        if self.led_status != val:
            if ctime - self.last_light > 30:#check every 500ms - 15 frames
                #print(val)
            #for testing, trigger every 1s

                self.led_status = val
                if val>0:
                    self.turn_stim_on()
                else:
                    self.turn_stim_off()

                self.last_light = ctime
                self.led_times.append((val, ctime))

    def close_serial(self):
        self.ser.close()

    def turn_stim_on(self):
        # command to activate arduino which runs code with desired stim parameters
        # H will turn on, will run until receives L
        self.ser.write(b'H')
        print("sent H")

    def turn_stim_off(self):
        self.ser.write(b"L")
        print("sent L")


    def process(self, pose, **kwargs):

        #0 TL
        #1 TR
        #2 BL
        #3 BR
        #4 s4
        #5 s3
        #6 s2
        #7 s1
        #8 nose
        #9 L ear
        #10 R ear
        #11 neck
        #12 tail base
        #13 tail tip
        #14 object left
        #15 object right

        if kwargs['frame_time'] > 12600: #12600:#only start stimulating after 7 min
            nose = pose[8, 0:2] if pose[8, 2] > self.lik_thresh else None
            neck = pose[11, 0:2] if pose[11, 2] > self.lik_thresh else None
            topleft = pose[0, 0:2] if pose[0, 2] > self.lik_thresh else None
            s3 = pose[5, 0:2] if pose[5, 2] > self.lik_thresh else None
            #top left and s3 demarkate 3cm square corner of cage

            if nose is not None and neck is not None and topleft is not None and s3 is not None:
                head = (nose + neck) / 2

                if head[0] < s3[0] and head[1] < s3[1]: #head is in top left corner
                    self.switch_led(val = True, ctime = kwargs['frame_time'])
                else:
                    self.switch_led(val = False, ctime = kwargs['frame_time'])

        return pose

    def save(self, filename):

        ### save stim on and stim off times

        if filename[-4:] != ".csv":
            filename += ".csv"
        arr = np.array(self.led_times, dtype=float)
        #np.save(filename, arr)

        #print(arr)
        np.savetxt(filename, arr, delimiter=',', fmt ='%f')
        save_code = True

        return save_code

class TC_proc_short(Processor):
    def __init__(self, lik_thresh=0.85, baudrate=int(9600), **kwargs):

        super().__init__()
        self.lik_thresh = lik_thresh
        self.led_times = []
        self.last_light = 0
        self.led_status = False
        try:
            self.ser = serial.Serial(kwargs["com"], baudrate)
        except:
            print("Unable to connect to COM")

        time.sleep(2)
        print("Using" + kwargs["com"])
        # make sure this matches serial port of arduino

    def switch_led(self, val, ctime):

        if self.led_status != val:
            if ctime - self.last_light > 30:#check every 1s - 30 frames
                #print(val)
            #for testing, trigger every 1s

                self.led_status = val
                if val>0:
                    self.turn_stim_on()
                else:
                    self.turn_stim_off()

                self.last_light = ctime
                self.led_times.append((val, ctime))

    def close_serial(self):
        self.ser.close()

    def turn_stim_on(self):
        # command to activate arduino which runs code with desired stim parameters
        # H will turn on, will run until receives L
        self.ser.write(b'H')
        print("sent H")

    def turn_stim_off(self):
        self.ser.write(b"L")
        print("sent L")


    def process(self, pose, **kwargs):

        ### bodyparts
        #0 Mouse nose
        #1 Mouse neck
        #2 Mouse tail base
        #3 Mouse tail tip
        #4 empty cage front
        #5 empty cage top
        #6 empty cage bottom
        #7 empty cage back
        #8 mouse cage front
        #9 mouse cage top
        #10 mouse cage bottom
        #11 mouse cage back
        #12 empty chamber top
        #13 empty chamber bottom
        #14 mouse chamber top
        #15 mouse chamber bottom
        if kwargs['frame_time'] < 9000:#only start stimulating during 0-5min

            nose = pose[0, 0:2] if pose[0, 2] > self.lik_thresh else None
            neck = pose[1, 0:2] if pose[1, 2] > self.lik_thresh else None
            front_of_mcage = pose[8, 0:2] if pose[8, 2] > self.lik_thresh else None
            front_of_empty = pose[4, 0:2] if pose[4, 2] > self.lik_thresh else None

            if nose is not None and neck is not None and kwargs['frame_time'] is not None and front_of_empty is not None and front_of_mcage is not None:
                head = (nose + neck) / 2
                distance_to_novel_mouse = sum((head-front_of_mcage)**2)**0.5
                distance_to_empty_cage = sum((head-front_of_empty)**2)**0.5

                if distance_to_novel_mouse < 110: #quick math, width of tank =  /~620 pixels. radius to front of cage = 3cm/110 pixels
                    self.switch_led(val = True, ctime = kwargs['frame_time'])

                else:
                    self.switch_led(val = False, ctime = kwargs['frame_time'])

        if kwargs['frame_time'] == 9100:
            self.switch_led(val = False, ctime = kwargs['frame_time'])

        return pose

    def save(self, filename):

        ### save stim on and stim off times

        if filename[-4:] != ".csv":
            filename += ".csv"
        arr = np.array(self.led_times, dtype=float)
        #np.save(filename, arr)

        #print(arr)
        np.savetxt(filename, arr, delimiter=',', fmt ='%f')
        save_code = True

        return save_code

class OF_proc_short(Processor):

    def __init__(self, lik_thresh=0.85, baudrate=int(9600), **kwargs):

        super().__init__()
        self.lik_thresh = lik_thresh
        self.led_times = []
        self.last_light = 0
        self.led_status = False
        try:
            self.ser = serial.Serial(kwargs["com"], baudrate)
        except:
            print("Unable to connect to COM")

        time.sleep(2)
        print("Using" + kwargs["com"])
        # make sure this matches serial port of arduino

    def switch_led(self, val, ctime):

        if self.led_status != val:
            if ctime - self.last_light > 30:#check every 500ms - 15 frames
                #print(val)
            #for testing, trigger every 1s

                self.led_status = val
                if val>0:
                    self.turn_stim_on()
                else:
                    self.turn_stim_off()

                self.last_light = ctime
                self.led_times.append((val, ctime))

    def close_serial(self):
        self.ser.close()

    def turn_stim_on(self):
        # command to activate arduino which runs code with desired stim parameters
        # H will turn on, will run until receives L
        self.ser.write(b'H')
        print("sent H")

    def turn_stim_off(self):
        self.ser.write(b"L")
        print("sent L")


    def process(self, pose, **kwargs):

        #0 TL
        #1 TR
        #2 BL
        #3 BR
        #4 s4
        #5 s3
        #6 s2
        #7 s1
        #8 nose
        #9 L ear
        #10 R ear
        #11 neck
        #12 tail base
        #13 tail tip
        #14 object left
        #15 object right

        #no time restrictions
        nose = pose[8, 0:2] if pose[8, 2] > self.lik_thresh else None
        neck = pose[11, 0:2] if pose[11, 2] > self.lik_thresh else None
        topleft = pose[0, 0:2] if pose[0, 2] > self.lik_thresh else None
        s3 = pose[5, 0:2] if pose[5, 2] > self.lik_thresh else None
        #top left and s3 demarkate 3cm square corner of cage

        if nose is not None and neck is not None and topleft is not None and s3 is not None:
            head = (nose + neck) / 2

            if head[0] < s3[0] and head[1] < s3[1]: #head is in top left corner
                self.switch_led(val = True, ctime = kwargs['frame_time'])
            else:
                self.switch_led(val = False, ctime = kwargs['frame_time'])

        return pose

    def save(self, filename):

        ### save stim on and stim off times

        if filename[-4:] != ".csv":
            filename += ".csv"
        arr = np.array(self.led_times, dtype=float)
        #np.save(filename, arr)

        #print(arr)
        np.savetxt(filename, arr, delimiter=',', fmt ='%f')
        save_code = True

        return save_code
