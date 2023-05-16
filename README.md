# behavior-recording-dlc-live
 closed loop reccording of behavior with opencv - DLC live - tkinter GUI

Used in Goff et al Cell Reports 2023, live recording of mouse behavior with closed loop optogenetic stimulation given via a arduino driving laser.

DLC_env.yaml is the environment file used during data acquisition on a laptop with RTX2080 nvidia graphics card. exact environment may differ when using different generation of video card.
see DLC documentation for appropriate installation of CUDA, cudnn, microsoft visual studio, etc. 

TTL_20Hz_5ms.ino files provided were used with the arduino IDE to drive TTL pulses from arduino. 

Run_GUI.py is the main  file, running will generate a tkinter UI for controlling laser and recording with opencv. 

The various pages of the ui are imported from RecordClass, RecordAndStimClass, and StimTestClass. 

The processor_collection.py file includes classes for several 'processors' used by DLC live, including for three chamber task (TC_proc) and open field (OF_proc).

These use the DLC models found in the folder 'DLC models'.


 
