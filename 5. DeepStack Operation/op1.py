# Import modules needed for frame grabbing and prediction.

# basic image processing
import imutils
from imutils.video import VideoStream
# arguments parsing
import argparse
# frame grabbing
import cv2
# for sending http requests and getting response objects
import requests
# modules for text to speech. NB: pyttsx3 performs woefully on linux systems, gtts is a viable replacement but it needs internet connection and you'll need the playsound module to play the mp3 file. These extra processes are liable to cause extra lagging
# from gtts import gTTS, gTTSError
# from playsound import playsound
import pyttsx3
# for input/output operations and memory optimization
from io import BytesIO

import os
import time

# confuguring the python text to sppech module
converter = pyttsx3.init()
converter.setProperty('rate', 150) # tts speed
converter.setProperty('volume', 1) # tts volume
# changing the property to voices[1] will give a female voice output
# voices = engine.getProperty('voices') 
# converter.setProperty('voice', voices[0].id) 

sourceImages = []

# python function for predicting sign language
def predict_sign(frame, url):
    s = time.time()
    response = requests.post(url, files={"image": frame}).json()
    e = time.time()
    # prints time taken for each predicted output
    print(f"Inference took: {(e - s)} seconds")
    print(response)
    if "success" in response and response['success'] == True and len(response['predictions']) > 0:
        prediction = response['predictions'][0]
        for object in response["predictions"]:
            # prints out the predicted sign
            print(object["label"])
    else:
        prediction = None

    return prediction

    
if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    # default = deepstack url
    ap = argparse.ArgumentParser()
    ap.add_argument("--deepstack-url", type=str,
                    default="http://localhost:80/v1/vision/custom/SignLanguage",
                    help="url to running deepstack image")
    args = vars(ap.parse_args())

    deepstack_url = args['deepstack_url']

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    # Green color. Change the values to give other shades of color
    color = (0, 255, 0)

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        # isTrue, frame = vs.read()
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        success, encoded_image = cv2.imencode('.jpg', frame)
        source_image = content2 = encoded_image.tobytes()
        sourceImages.append(source_image)

        print("\n\nPrediction: \n")
        # sourceImages[-1] - the latest frame in the list
        prediction = predict_sign(sourceImages[-1], deepstack_url)

        if prediction is not None:
            confidence = prediction['confidence']
            label = prediction['label']
            y_min = prediction['y_min']
            x_min = prediction['x_min']
            y_max = prediction['y_max']
            x_max = prediction['x_max']

            # Text to Speech

            # accents can be changed by manipulating the lang and tld arguments.
            # try:
            #     voice = BytesIO()
            #     tts = gTTS(label, lang='en', slow=False, tld='com.uk')
            #     tts.save('output.mp3')
            #     playsound('output.mp3')
            #     os.remove('output.mp3')
            # except gTTSError:
            #     print('Prediction could not be voiced out due to a data connection failure.......')

            converter.say(label)
            converter.runAndWait()

            # display the label and bounding box rectangle on the output frame
            cv2.putText(frame, f"{label} {confidence}", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
             
            # did this part twice to improve the user experience, if you have a
            # a good machine, you can cut this out.
            converter.say(label)
            converter.runAndWait()

        cv2.imshow("Sign Language", frame)
        # press 'q' to break out of the video stream. NB: 'Q' won't do the trick
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
