cmake_minimum_required(VERSION 3.12)

project(xmlrpc-epi C)

find_package(EXPAT REQUIRED)

file(GLOB HEADERS "src/*.h")
file(GLOB SOURCES "src/*.c")

add_library(xmlrpc-epi ${SOURCES} ${HEADERS})

target_include_directories(xmlrpc-epi PUBLIC include)

set(LINK_LIBRARIES expat::expat)
if (WIN32)
    find_package(ICONV REQUIRED)
    list(APPEND LINK_LIBRARIES Iconv::Iconv)
endif (WIN32)

target_link_libraries(xmlrpc-epi ${LINK_LIBRARIES})

install(TARGETS xmlrpc-epi
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES ${HEADERS} DESTINATION include)
