cmake_minimum_required(VERSION 3.16)
project(PyOpenROAD)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/OpenROAD/src/cmake")

option(USE_SYSTEM_BOOST "Use system shared Boost libraries" ON)

add_subdirectory(OpenROAD)

set(PYMODULE_SOURCE
    src/PyModule.cc
    OpenROAD/src/Design.cc
    OpenROAD/src/Timing.cc
    OpenROAD/src/Tech.cc
    OpenROAD/src/OpenRoad.cc
)

add_library(pymodule_openroad MODULE ${PYMODULE_SOURCE})

set_target_properties(pymodule_openroad PROPERTIES
PREFIX ""
OUTPUT_NAME "openroadpy"
LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/python
)
  
target_compile_options(pymodule_openroad
PRIVATE
    -Wextra -pedantic -Wcast-qual
)

target_link_libraries(pymodule_openroad
    openroad
)

target_include_directories(pymodule_openroad
    PRIVATE
    ${CMAKE_SOURCE_DIR}/OpenROAD/include
)

target_compile_definitions(pymodule_openroad PRIVATE GPU)
target_compile_definitions(pymodule_openroad PRIVATE BUILD_PYTHON)
target_compile_definitions(pymodule_openroad PRIVATE BUILD_GUI)
target_compile_definitions(pymodule_openroad PRIVATE ENABLE_CHARTS)