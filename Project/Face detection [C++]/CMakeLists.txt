cmake_minimum_required (VERSION 3.0) 

PROJECT(DeepLearning_Face_Detection)

set (CMAKE_CXX_STANDARD 11)

IF(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
ENDIF()

# Requires OpenCV v4.0 or later
FIND_PACKAGE( OpenCV 4 REQUIRED )
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})

ADD_EXECUTABLE( ${PROJECT_NAME}_face resnet_ssd_face_detection.cpp )
TARGET_LINK_LIBRARIES( ${PROJECT_NAME}_face  ${CONAN_LIBRARIES} ${OpenCV_LIBRARIES} )
