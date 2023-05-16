"""takes a numpy array (frame) and (pose) and returns a labelled image in both img and array format
will also pass image from array if no pose is given
Create the image with DeepLabCut labels
Parameters
-----------
frame :class:`numpy.ndarray`
    an image as a numpy array
pose :class:`numpy.ndarray`
    the pose estimated by DeepLabCut for the image
optional arguments are
radius - size of points
cmap  - color map string for colorcet
pcutoff - probability cutoff for labelling

"""
import cv2
from PIL import Image, ImageDraw
import colorcet as cc

def create_label_frame(frame, pose = None, cmap = "bmy", radius=15, pcutoff=0.5):

    im_size = (frame.shape[1], frame.shape[0])

    if pose is not None:

        all_colors = getattr(cc, cmap)
        colors = all_colors[:: int(len(all_colors) / pose.shape[0])]
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        draw = ImageDraw.Draw(img)

        for i in range(pose.shape[0]):
            if pose[i, 2] > pcutoff:
                try:
                    x0 = (
                        pose[i, 0] - radius
                        if pose[i, 0] - radius > 0
                        else 0
                    )
                    x1 = (
                        pose[i, 0] + radius
                        if pose[i, 0] + radius < im_size[0]
                        else im_size[1]
                    )
                    y0 = (
                        pose[i, 1] - radius
                        if pose[i, 1] - radius > 0
                        else 0
                    )
                    y1 = (
                        pose[i, 1] + radius
                        if pose[i, 1] + radius < im_size[1]
                        else im_size[0]
                    )
                    coords = [x0, y0, x1, y1]
                    draw.ellipse(
                        coords, fill=colors[i], outline=colors[i]
                    )
                except Exception as e:
                    print(e)

    else:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)

    return img
