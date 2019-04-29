View this project on [CADLAB.io](https://cadlab.io/project/1601). 

# ECE-477

This project relies on Python 3.5 or above to work properly. Furthermore, DLIB, OpenCV, face_recognition, and several other PIP packages are required for download before this will run properly. Additional packages are required for a Raspberry Pi. For our conventience during initial testing, a discovered wheel build for Tensorflow on a Raspberry Pi was added for easy distrobution among our prototyping devices. It was offered up on a forum that we came across as we tried to build Tensorflow on a Pi from source.

Running application.py should detect whether on a Pi or Ubuntu, and this project isn't promised to work outside of those two environments. This also requires an MSP432 to be flashed with the code in  the msp432 Code Composer Studio project folder, and the EAGLE folder has some of our EAGLE source files, though at the writing of this document it is unknown if they're the latest versions.

This was a project that didn't get finalized to a manufacturing or distrobution setting, so we cannot promise that all of the board population components and project requirements are included in this GitHub.

Lastly, THIS SHOULD NOT BE USED FOR HIGH-SECURITY PURPOSES
Facial recognition has a few ways it can be easily fooled, and the accuracy of this network wasn't fully stress tested on edge cases (twins, close family resemblance, holding a photo up to the camera of a registered user, etc). If you'd like to use this project, it is recommended for personal interest projects at best, as it'd need large additions to become more realistically secure.
