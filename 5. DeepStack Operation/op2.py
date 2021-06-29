import requests
import time

image_data = open('1. Data Collection/train/black power.a7af3f36-cf5c-11eb-96f5-54ab3a020c27.png',"rb").read()

s = time.time()
response = requests.post("http://localhost:80/v1/vision/custom/SignLanguage", files={"image":image_data}).json()
e = time.time()

for object in response["predictions"]:
    print(object["label"])

print(f'[INFERENCE] took {e-s} secs...')
print(response)

if "success" in response and response['success'] == True and len(response['predictions']) > 0:
    prediction = response['predictions'][0]
    for object in response["predictions"]:
        # prints out the predicted sign
        print(object["label"])

else:
    print('None')

