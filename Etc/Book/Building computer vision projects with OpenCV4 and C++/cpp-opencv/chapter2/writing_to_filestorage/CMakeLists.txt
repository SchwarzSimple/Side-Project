cmake_minimum_required (VERSION 3.0)
PROJECT(Chapter2)
# Requires OpenCV
FIND_PACKAGE( OpenCV  REQUIRED )
# Show a message with the opencv version detected
MESSAGE("OpenCV version : ${OpenCV_VERSION}")
# Add the paths to the include directories/to the header files
include_directories(${OpenCV_INCLUDE_DIRS})
# Add the paths to the compiled libraries/objects
link_directories(${OpenCV_LIB_DIR})
# Create a variable called SRC
SET(SRC main.cpp)
# Create our executable
ADD_EXECUTABLE(${PROJECT_NAME} ${SRC})
# Link our library
TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${OpenCV_LIBS})
