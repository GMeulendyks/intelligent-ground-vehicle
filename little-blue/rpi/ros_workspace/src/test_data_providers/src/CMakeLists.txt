set(INCLUDE
    ${CMAKE_CURRENT_SOURCE_DIR}
)
set(LIBS
    ${packager_msgs_TARGETS}
    providers
    nodes
)
add_subdirectory(providers)
add_subdirectory(nodes)

add_executable(Cam0NodeMain Cam0Main.cpp)
target_link_libraries(Cam0NodeMain ${LIBS})
add_executable(Cam1NodeMain Cam1Main.cpp)
target_link_libraries(Cam1NodeMain ${LIBS})
add_executable(ImuNodeMain ImuMain.cpp)
target_link_libraries(ImuNodeMain ${LIBS})
add_executable(LidarNodeMain LidarMain.cpp)
target_link_libraries(LidarNodeMain ${LIBS})
add_executable(MotorControlNodeMain MotorControlMain.cpp)
target_link_libraries(MotorControlNodeMain ${LIBS})

set(NODE_TARGETS
    Cam0NodeMain
    Cam1NodeMain
    ImuNodeMain
    LidarNodeMain
    MotorControlNodeMain
    PARENT_SCOPE
)
