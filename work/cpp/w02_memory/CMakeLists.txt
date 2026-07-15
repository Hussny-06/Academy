cmake_minimum_required(VERSION 3.23)
project(W02_memory)

add_executable(memory_explorer)
target_sources(memory_explorer
    PRIVATE
        memory_explorer.cpp
)