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


class JunoJumpOffline(Processor):
    def __init__(self, lik_thresh=0.5, baudrate=int(9600), **kwargs):

        super().__init__()
        self.lik_thresh = lik_thresh
        self.led_times = []
        self.last_light = 0
        self.led_status = False
        self.ser = serial.Serial(kwargs["com"], kwargs["baudrate"])
        # make sure this matches serial port of arduino

    def switch_led(self, val, frame_time):

        if self.led_status != val:
            ctime = frame_time
            if ctime - self.last_light > 0.5:#check every 500ms
                self.led_status = val
                if val:
                    self.turn_stim_on
                else
                    self.turn_stim_off

                self.last_light = ctime
                self.led_times.append((val, frame_time, ctime))

    def close_serial(self):
        self.ser.close()

    def turn_stim_on(self):
        # command to activate arduino which runs code with desired stim parameters
        # H will turn on, will run until receives L
        self.ser.write(b'H')

    def turn_stim_off(self):
        self.ser.write(b"L")



    def process(self, pose, **kwargs):

        ### bodyparts
        # 0. nose
        # 1. L-eye
        # 2. R-eye
        # 3. L-ear
        # 4. R-ear
        # 5. Throat
        # 6. Withers
        # 7. Tailset
        # 8. L-front-paw
        # 9. R-front-paw
        # 10. L-front-wrist
        # 11. R-front-wrist
        # 12. L-front-elbow
        # 13. R-front-elbow
        # ...

        l_elbow = pose[12, 1] if pose[12, 2] > self.lik_thresh else None
        r_elbow = pose[13, 1] if pose[13, 2] > self.lik_thresh else None
        elbows = [l_elbow, r_elbow]
        this_elbow = (
            min([e for e in elbows if e is not None])
            if any([e is not None for e in elbows])
            else None
        )

        withers = pose[6, 1] if pose[6, 2] > self.lik_thresh else None

        if kwargs["record"]:
            if withers is not None and this_elbow is not None:
                if this_elbow < withers:
                    self.switch_led(True, kwargs["frame_time"])
                else:
                    self.switch_led(False, kwargs["frame_time"])

        return pose

    def save(self, filename):

        ### save stim on and stim off times

        if filename[-4:] != ".npy":
            filename += ".npy"
        arr = np.array(self.led_times, dtype=float)
        try:
            np.save(filename, arr)
            filename -= ".npy"
            np.savetxt(filename + ".csv", arr, delimiter=',', fmt='%f')
            save_code = True
        except Exception:
            save_code = False
            print("Could not save processor file")
        return save_code
