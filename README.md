# Sign-Language-to-Speech

Sign Language to Speech in 5 Steps:

1. Data Collection
2. Data Annotation
3. Model Training
4. Trained Model
5. DeepStack Operation



1. Data Collection
Python script path - '1. Data Collection/Image Code/images.py'

Run the python script to collect as many images as you can containing the sign language you want to detect (Yeah, pose for your webcam). For this experiment, 50 images for the training set and 5 images for the test set were collected per label (sign language). Earlier experiments with fewer images produced less than desirable result, so collect as much as possible. Alternatively, you can source images from the web.

Organize your dataset by creating a root folder and creating a train and test folder inside it. You can replicate the folder organization used in this project. Running this python script will create several subfolders in the train and test folders depending on the number of labels you intend collecting.

Empty the datasets in the train subfolders into the root train folder and delete the empty subfolders. Repeat the same step for the test images.



2. Data Annotation

This project uses LabelImg for graphical image annotion. Alternatively, you can use Labelme.

Create a folder, cd (change directory) into it via command prompt and run <git clone https://github.com/tzutalin/labelImg.git> (ofcourse you know those braces are not part of the command). cd into the cloned project and run <python labelImg.py>. If you get a module not found error, run <pip install LabelImg>. Unless there's any other error, you'll see the LabelImg interface come up.

Click on the 'Open Dir' to cd into your data folders. Click on 'PascalVOC' to change it to 'YOLO' format. Press 'w' to bring up the rect box. Use your mouse pad to expand the rect box around the sign language in the image. Type in the label into the interface that'll be brought up, click on save and a txt file of YOLO format will be saved in the same folder as your image with same name. A file named "classes.txt" is saved to that folder too. "classes.txt" defines the list of class names that your YOLO label refers to. Click on 'd' to move to the next image, 'a' to the previous image.

NB: If yours is not a windows system, go to https://github.com/tzutalin/labelImg and check out the installation process peculiar to your system.

  
  
  
3. Model Training
Jupyter notebook path - '3. Model Training/deepstack.ipynb'

Unless you have a gpu powered system, it's better you make use of google colab. Upload the folder containing the datasets to your google drive (you have the option of zipping). Mount your google drive on google colab. Run the commands in the notebook. You can also adjust the parameters as stated in the notebook.

At the end of the training, on the deepstack folder that would have appeared the moment you start running the commands in the notebook, go through 'train-runs/my-dataset/exp/weights'. Download the best weight file. Hey, for no reason should you download any model file before the preset number of epochs elapses. Your deepstack model won't predict anything if you go against this warning (I tried it as well).

  
  
  
4. Trained Model

You can rename the downloaded file e.g SignLanguage.pt (you can as well leave it as best.pt). Create a folder for the model (optional) and move the trained model into it.

  
  
  
5. DeepStack Operation
Python script path - '5. DeepStack Operation/op1.py'

Visit https://docs.deepstack.cc/index.html#installation-guide-for-cpu-version for instructions on how to set up deepstack as peculiar to the type of system you have.

Start command prompt and run <deepstack --MODELSTORE-DETECTION "C:/path-to-trained-sign-language-model-folder" --PORT 80> (the port number can be adjusted if 80 is been used for other things). Deepstack server will give an address corresponding to your what you named your model. Replace the http extension on the python scripts with this address.

On your IDE, run the python script and test out the accuracy of your model.

NB: Visit https://docs.deepstack.cc/custom-models/deployment/ for deployment commands peculiar to systems apart from windows.
If you get a JSON decode error, check your http address in the deepstack operation python scripts.

For this step, I modified Patrick Ryan's original code to fit this pecular project.
Patrick's code - https://gist.github.com/youngsoul/2e6a64dabbf9303103bc48b8b2ab3617





Real Time? Real Battle!!

As stated in the deepstack documentation, a gpu system will power through this project 5x - 20x faster than a cpu system. A cpu system was used in this project and thus bringing this project to the realms of real time was impossible (hey, I tried my best, unless you can do any better, my claim still stands). But in my valiant attempt to turn things around, I tried:

Threading - I separated, threaded and queued the Deepstack Operation python script, so that the script responsible for frame grabbing differed from the script running deepstack. I also threaded the deepstack server to client i.e I started several deepstack servers and threaded their connections to my python script.

Cloud - Considered hosting my deepstack server on cloud services like digital ocean (thought of the cost and backed out, moreso, there's no gpu support). 

Running and also threading the op2 DeepStack Operation script ('5. DeepStack Operation/op1.py') as found at https://docs.deepstack.cc/custom-models/deployment/ made me realize the real cause of the bottleneck is the time taken for deepstack server to process each image. Threading the server to client connection made things worse as deepstack did not process requests on different servers simultaneously but rather one after the other.

At the end, I increased the number of images gathered per label from 15 to 50 for the training set. Used the 'yolo5s' model rather than the default 'yolov5m' model. Left the epochs at 300 (increasing it had no effect on the accuracy).

The resultant effect was that I beat down the deepstack processing time per image from 2.5 secs on average to 1.2 secs on average.

So yeah, this project went from crawling to walking...maybe you'll make it fly, who knows......

Hmm, I used ScreenRec to record the result of this project and it added more lag to this project. So yeah, from crawling to walking and back to CRAWLING....


Final NB: I included my dataset (the test part) in this project, I'm still debating it's relevance: low quality pics, advisable to get better ones for your project but atleast you'll have a better idea of what the dataset is all about.
