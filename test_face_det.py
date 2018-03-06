import sys
import dlib
from skimage import io


detector = dlib.get_frontal_face_detector()

img = io.imread('face3.jpg')
dets = detector(img, 1)
print("Number of faces detected: {}".format(len(dets)))
for i, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))
