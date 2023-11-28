cmake_minimum_required(VERSION 3.15)
project(PackageTest C)

find_package(xmlrpc-epi CONFIG REQUIRED)

add_executable(testapp src/main.c)
target_link_libraries(testapp xmlrpc-epi::xmlrpc-epi)
