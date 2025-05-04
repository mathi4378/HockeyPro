***This is my Masterthesis***

+ The environment can be used with the given requirements file


**Progress:**

First a depth map was used to detect the hit. This can be seen in the 2 plots below:

![Hit detection using the depth map](https://github.com/mathi4378/Masterarbeit/blob/main/Images_readme/image_9-1.png)
![Hit detection using the depth map](https://github.com/mathi4378/Masterarbeit/blob/main/Images_readme/image_9-2.png)

As seen in the right image there is some noice, which gets a lot more in videos and therefore the accuracy and reliability is not given. Therefore a new approach
using the yolo models can be seen below.


<p align="center">
    <img src="https://github.com/mathi4378/Masterarbeit/blob/main/Images_readme/Test_3.jpg" alt="Hit detection with yolo" width="300">
    <img src="https://github.com/mathi4378/Masterarbeit/blob/main/Images_readme/Test_4.jpg" alt="Hit detection with yolo" width="300">
</p>


Below it is shown how the position of the hit can be seen:

<p align="center">
    <img src="https://github.com/mathi4378/Masterarbeit/blob/main/Pictures/Test_position/Results/Test_2.jpg" alt="Hit number 1" width="300">
    <img src="https://github.com/mathi4378/Masterarbeit/blob/main/Pictures/Test_position/Results/Test_3.jpg" alt="Hit number 2" width="300">
</p>

Here are the results of the yolo11n model and the measurements made my hand (very inaccurate, only to prove that the code works):

| Hit |   Höhe-gemessen |   Höhe-Yolo |   Breite-gemessen |   Breite-Yolo |   Höhe-Differenz |   Breite-Differenz |
|----:|----------------:|------------:|------------------:|--------------:|-----------------:|-------------------:|
|   1 |              84 |          76 |                85 |            89 |                8 |                 -4 |
|   2 |              20 |          13 |                20 |            25 |                7 |                 -5 |




