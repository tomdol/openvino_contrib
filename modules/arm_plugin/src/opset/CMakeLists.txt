# Copyright (C) 2020-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

set(TARGET_NAME "openvino_arm_cpu_opset")

file(GLOB_RECURSE SOURCES_TRANSFORMATIONS
        ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)

add_library(${TARGET_NAME} STATIC ${SOURCES_TRANSFORMATIONS})


target_include_directories(${TARGET_NAME} PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}"
        "${IE_MAIN_ARM_PLUGIN_SOURCE_DIR}/src/")

target_link_libraries(${TARGET_NAME} PRIVATE
        arm_compute::arm_compute
        arm_compute::half
        openvino::ngraph_reference
        openvino::itt
        openvino::runtime::dev)

ov_install_static_lib(${TARGET_NAME} cpu)
