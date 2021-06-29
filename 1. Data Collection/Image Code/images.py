# Import modules needed for image collection
# cv2 for getting frames from a video stream, uuid for giving images unique ids 

import os
import cv2
import time
import uuid

# Root folder for the images. NB:   change train to test while collecting the test images
imgPath = '1. Data Collection/train'

# Sign language images to be collected
labels = ['call me', 'married', 'divorced', 'open relationship', 'tea time', 'dad', 'mom', 'thank you', 'more', 'black power', 'bed', 'go to hell']

# Number of images collected per label. NB: change to 5 for the test images
numImgs = 50

for label in labels:
  # Creates a folder for each label in the image root folder. NB: change train to test for the test images
  os.mkdir('1. Data Collection/train//'+label)
  # cv2 starts a video stream using the systems's webcam (0). Other connected webcams can  be used by changing the cam address (e.g 1, 2, 3....)
  cam = cv2.VideoCapture(0)
  print('Collecting Images for {}'.format(label))
  time.sleep(5)
  for numImg in range(numImgs):
    # cv2 collects frames
    ret, frame = cam.read()
    imagename = os.path.join(imgPath, label, label + '.' + '{}.png'.format(str(uuid.uuid1())))
    # The collected frames are saved
    cv2.imwrite(imagename, frame)
    cv2.imshow('frame', frame)
    time.sleep(2)
    # Click on 'q' to break out of the video stream. NB: 'Q' won't do the trick..
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  cam.release()


