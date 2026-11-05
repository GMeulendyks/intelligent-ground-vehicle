add_subdirectory(img)
add_subdirectory(imu)
add_subdirectory(lidar)

add_library(IGVCPackager Common.cpp)
target_include_directories(IGVCPackager PUBLIC ${PROJECT_INCLUDE})
target_link_libraries(IGVCPackager PUBLIC imu lidar img)

