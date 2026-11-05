
add_library(img OBJECT Image.cpp)

target_include_directories(img PRIVATE ${PROJECT_INCLUDE} ${OpenCV_INCLUDE_DIRS})
target_link_libraries(img PUBLIC ${OpenCV_LIBS})
