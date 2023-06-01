# behavior-recording-dlc-live
closed loop reccording of behavior with opencv - DLC live - tkinter GUI
Used in Goff et al Cell Reports 2023, live recording of mouse behavior with closed loop optogenetic stimulation given via a arduino driving laser.
DLC_env.yaml is the environment file used during data acquisition on a laptop with RTX2080 nvidia graphics card. exact environment may differ when using different generation of video card. see DLC documentation for appropriate installation of CUDA, cudnn, microsoft visual studio, etc.

TTL_20Hz_5ms.ino files provided were used with the arduino IDE to drive TTL pulses from arduino.
Run_GUI.py is the main file, running will generate a tkinter UI for controlling laser and recording with opencv.
The various pages of the ui are imported from RecordClass, RecordAndStimClass, and StimTestClass.
The processor_collection.py file includes classes for several 'processors' used by DLC live, including for three chamber task (TC_proc) and open field (OF_proc). These use the DLC models found in the folder 'DLC models'. Briefly, TC_proc will send an 'on' signal to the arduino whenever the mouse is within ~2cm from the social cage, with a refresh rate of 1s (ie can not turn on/off more frequently than once per second) there is no timout period. OF_proc does the same but when the mouse is in a single corner of the open field.  there are short and long versions of each processor that record for different lengths and with the stimulation either on during the first 5 minutes, or minutes 5-10 

additional processors can be added to the file "processor_collection.py" and additional models to the DLC models folder. currently the GUI interface will have you select a DLC model, then uses a numeric input (1,2,3,4) to select the processor. this will need to be changed to add additional processors (line 309-320 in RecordClass.py)

Additional DLC models can be trained and exported with DLClive : https://github.com/DeepLabCut/DeepLabCut-live
Download arduino IDE here: https://www.arduino.cc/en/software

 
