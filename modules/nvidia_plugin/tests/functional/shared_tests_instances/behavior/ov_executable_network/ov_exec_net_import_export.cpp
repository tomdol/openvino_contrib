// Copyright (C) 2018-2023 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//
#include <common_test_utils/test_constants.hpp>
#include <cuda_test_constants.hpp>

#include "behavior/ov_executable_network/exec_graph_info.hpp"
#include "ie_plugin_config.hpp"

using namespace ov::test::behavior;
namespace {
const std::vector<ov::element::Type_t> netPrecisions = {
    ov::element::f16, ov::element::f32, ov::element::i8,
    // TODO: Add additional network precisions
};
const std::vector<ov::AnyMap> configs = {
    {},
};
const std::vector<ov::AnyMap> multiConfigs = {{ov::device::priorities(CommonTestUtils::DEVICE_NVIDIA)}};

const std::vector<ov::AnyMap> heteroConfigs = {{ov::device::priorities(CommonTestUtils::DEVICE_NVIDIA)}};

INSTANTIATE_TEST_SUITE_P(smoke_BehaviorTests,
                         OVExecGraphImportExportTest,
                         ::testing::Combine(::testing::ValuesIn(netPrecisions),
                                            ::testing::Values(CommonTestUtils::DEVICE_NVIDIA),
                                            ::testing::ValuesIn(configs)),
                         OVExecGraphImportExportTest::getTestCaseName);

INSTANTIATE_TEST_SUITE_P(smoke_Auto_BehaviorTests,
                         OVExecGraphImportExportTest,
                         ::testing::Combine(::testing::ValuesIn(netPrecisions),
                                            ::testing::Values(CommonTestUtils::DEVICE_AUTO),
                                            ::testing::ValuesIn(multiConfigs)),
                         OVExecGraphImportExportTest::getTestCaseName);

INSTANTIATE_TEST_SUITE_P(smoke_Hetero_BehaviorTests,
                         OVExecGraphImportExportTest,
                         ::testing::Combine(::testing::ValuesIn(netPrecisions),
                                            ::testing::Values(CommonTestUtils::DEVICE_HETERO),
                                            ::testing::ValuesIn(heteroConfigs)),
                         OVExecGraphImportExportTest::getTestCaseName);

}  // namespace