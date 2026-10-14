# upscale-cli
A lightweight, script that utilizes OpenCV's DNN super res module to upscale images. It runs entirely local on your machine and will max out lower end hardware with complex models.
___
For running the script, you need python 3.6+ installed on your machine.
It relies on the OpenCV, specifically including the contrib/DNN super resolution modules.

To install these packages, you can either use the pip package manager or your own desired option:
```pip install opencv-python opencv-contrib-python```
___
Your directory strcuture should look like this:

upscale/
  models/
   ESPCN_x2.pb
   ESPCN_x4.pb

 upscale.py
 README.md
___
To run the script, you can open the cloned direcotry and in it's root, you will see a file named as 'upscale.py'. While being in that same direcotry with the file, run:
```python3 upscale.py```
And then follow the prompts for entering the image path and model selection.

NOTE: You can even take your own models and place them inside the 'models' sub direcotry in the cloned one. The script will detect those automatically.
