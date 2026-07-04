cmake_minimum_required(VERSION 3.23)
project(W01_cmake)

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
