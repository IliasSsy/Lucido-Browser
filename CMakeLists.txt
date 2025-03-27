cmake_minimum_required(VERSION 3.1)

project(Lucido-browser)  # Corrected project name declaration

find_package(Boost REQUIRED COMPONENTS system filesystem)  # Ensure Boost is found
include_directories(${Boost_INCLUDE_DIRS})  # Include Boost headers

add_executable(${PROJECT_NAME} launch.cpp)  # Corrected variable syntax

target_link_libraries(${PROJECT_NAME} Boost::system Boost::filesystem)  # Link Boost libraries
