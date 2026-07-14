cmake_minimum_required(VERSION 3.23)
project(W01_cmake)

# Show which build type we're using
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Create the library target
add_library(utils_lib)

# Tell it which source files to build, and expose the header
target_sources(utils_lib
  PRIVATE
    src/utils.cpp
  PUBLIC
    FILE_SET HEADERS
    BASE_DIRS src
    FILES
      src/utils.h
)

# Create the executable target
add_executable(my_project)

# Tell it which source file to build
target_sources(my_project
  PRIVATE
    src/main.cpp
)

# Link the library to the executable
target_link_libraries(my_project
  PRIVATE
    utils_lib
)

# Enable testing
enable_testing()

# Find Google Test
find_package(GTest REQUIRED)

# Create test executable
add_executable(run_tests)
target_sources(run_tests
  PRIVATE
    tests/test_utils.cpp
)
target_link_libraries(run_tests
  PRIVATE
    utils_lib
    GTest::GTest
    GTest::Main
)

# Register with CTest
add_test(NAME utils_tests COMMAND run_tests)
