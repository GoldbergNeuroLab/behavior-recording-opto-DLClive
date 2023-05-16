"""
adapted from test-dlc-live using model zoo dog and videos of my dog!

"""
import os
import sys
import shutil
import warnings
import urllib.request
import argparse
from pathlib import Path
import tarfile

def urllib_pbar(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    outstr = f"{round(percent)}%"
    sys.stdout.write(outstr)
    sys.stdout.write("\b"*len(outstr))
    sys.stdout.flush()


class export_model():
    """download exported dog model from DeepLabCut Model Zoo"""

    def __init__(self, dir="C:/Users/kevin/local Python Scripts/dlc live model for three chamber"):

        self.directory = Path(dir)

    def makdir(self):
        # make temporary directory,
        print("\nCreating  directory...\n")
        self.directory.mkdir(mode=0o775,exist_ok=True)

    def downloadmodel(self):

        #video_file = str(self.directory / 'dog_clip.avi')
        model_tarball = self.directory / 'DLC_KG230_3ch_mobilenet_v2_1.0_iteration-0_shuffle-1.tar.gz'
        model_dir = model_tarball.with_suffix('').with_suffix('') # remove two suffixes (tar.gz)

        if Path(model_tarball).exists():
            print('Tarball already downloaded, using cached version')
        else:
            print("Could not find model")

        print('Untarring compressed model')
        model_file = tarfile.open(str(model_tarball))
        model_file.extractall(str(model_dir.parent))
        model_file.close()





em = export_model()
em.makdir()
em.downloadmodel()
print(em.directory)
