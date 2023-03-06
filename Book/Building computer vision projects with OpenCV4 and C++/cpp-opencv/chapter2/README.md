# About
- How to read and wirte an image using c++ and OpenCV

# Steps
- Create a "build" folder
- Create a CMakeLists.txt
- Copy lena.jpg from "https://github.com/TrainingByPackt/Building-Computer-Vision-Projects-with-OpenCV-4-and-CPP/blob/master/Chapter%2002/lena.jpg"
- Create a main.cpp
- Inside the build folder, execute command "cmake .."
- Inside the build folder, execute command "make"
- Execute "Chapter2"

# Error
- "Could not find module FindOpenCV.cmake or a configuration file for package OpenCV", excute command "sudo apt-get install libopencv-dev"
- 'CV_LOAD_IMAGE_GRAYSCALE' is not defined -> change "CV_LOAD_IMAGE_GRAYSCALE" to "IMREAD_GRAYSCALE"
