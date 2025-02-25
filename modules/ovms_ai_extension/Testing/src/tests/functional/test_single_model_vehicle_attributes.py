# Copyright (c) 2018-2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import cv2
import os
import json
import numpy as np

from constants import PREDICTION_SERVICE, ERROR_SHAPE
from utils.grpc import infer


class TestVehicleAttributes():

    def load_image(self, file_path, width, height):
        img = cv2.imread(file_path)  # BGR color format, shape HWC
        img = cv2.resize(img, (width, height))
        img = img.transpose(2, 0, 1).reshape(1, 3, height, width)
        # change shape to NCHW
        img = img.astype(np.float32)
        return img

    def test_run_inference(self, vehicle_attributes_model_downloader,
                           vehicle_attributes_data_downloader,
                           start_server_single_vehicle_attrib_model,
                           create_grpc_channel):
        """
        <b>Description</b>
        Submit request to gRPC interface serving a single vehicle model

        <b>input data</b>
        - directory with the model in IR format
        - docker image with ie-serving-py service

        <b>fixtures used</b>
        - model downloader
        - service launching

        <b>Expected results</b>
        - response contains proper numpy shape

        """

        _, ports = start_server_single_vehicle_attrib_model

        # Connect to grpc service
        stub = create_grpc_channel('localhost:{}'.format(ports["grpc_port"]),
                                   PREDICTION_SERVICE)

        imgs_v1_384 = np.ones((1, 3, 72, 72), dtype=np.float32)
        in_name = 'input'
        out_color = 'color'
        out_type = 'type'
        output = infer(imgs_v1_384, input_tensor=in_name, grpc_stub=stub,
                       model_spec_name='vehicle-attributes',
                       model_spec_version=None,
                       output_tensors=[out_color, out_type])

        print("output color shape", output[out_color].shape)
        assert output[out_color].shape == (1, 7, 1, 1), ERROR_SHAPE

    def test_run_inference_img(self, vehicle_attributes_model_downloader,
                               vehicle_attributes_data_downloader,
                               start_server_single_vehicle_attrib_model,
                               create_grpc_channel):
        """
        <b>Description</b>
        Submit request to gRPC interface serving a single vehicle model

        <b>input data</b>
        - directory with the model in IR format
        - docker image with ie-serving-py service

        <b>fixtures used</b>
        - model downloader
        - service launching

        <b>Expected results</b>
        - response contains proper numpy shape

        """

        _, ports = start_server_single_vehicle_attrib_model
        imgs_path = os.path.join(vehicle_attributes_data_downloader, "images")

        print("imgs_path" + imgs_path)

        input_img = self.load_image(os.path.join(
            imgs_path, "021471_004.png"), 72, 72)

        # Connect to grpc service
        stub = create_grpc_channel('localhost:{}'.format(ports["grpc_port"]),
                                   PREDICTION_SERVICE)

        in_name = 'input'
        out_color = 'color'
        out_type = 'type'
        output = infer(input_img, input_tensor=in_name, grpc_stub=stub,
                       model_spec_name='vehicle-attributes',
                       model_spec_version=None,
                       output_tensors=[out_color, out_type])

        result = output[out_color]
        print("colors:" + str(result))

        result = output[out_type]
        print("types:" + str(result))

        color_prob_sum = 0.0
        type_prob_sum = 0.0

        epsilon = 0.0000001

        for i in range(7):
            color_prob_sum += output[out_color][0, i, 0, 0].item()

        print("color probability sum", str(color_prob_sum))
        assert color_prob_sum + epsilon >= 1.0

        print("output type shape", output[out_type].shape)
        assert output[out_type].shape == (1, 4, 1, 1), ERROR_SHAPE

        for i in range(4):
            type_prob_sum += output[out_type][0, i, 0, 0].item()

        print("color probability sum", str(color_prob_sum))
        assert type_prob_sum + epsilon >= 1.0
        assert type_prob_sum <= 1.0 + epsilon

        # [car, bus, truck, van]
        expected_type_index = 2
        highest_prob = 0.0
        type_index = -1
        for i in range(4):
            type_prob = output[out_type][0, i, 0, 0].item()
            print("type_prob " + str(type_prob))
            if type_prob > highest_prob:
                print("update " + str(type_prob) + ">" + str(highest_prob))
                highest_prob = type_prob
                type_index = i

        print("type_index= " + str(type_index))
        assert type_index == expected_type_index

        # [white, gray, yellow, red, green, blue, black]
        expected_color_index = 3
        highest_prob = 0.0
        color_index = -1
        for i in range(7):
            color_prob = output[out_color][0, i, 0, 0].item()
            print("color_prob " + str(color_prob))
            if color_prob > highest_prob:
                print("update " + str(color_prob) + ">" + str(highest_prob))
                highest_prob = color_prob
                color_index = i

        print("color_index= " + str(color_index))
        assert color_index == expected_color_index

    def test_run_inference_postprocess(self, vehicle_attributes_model_downloader,
                                       vehicle_attributes_data_downloader,
                                       start_server_single_vehicle_attrib_model,
                                       create_grpc_channel):
        """
        <b>Description</b>
        Submit request to gRPC interface serving a single vehicle model

        <b>input data</b>
        - directory with the model in IR format
        - docker image with ie-serving-py service

        <b>fixtures used</b>
        - model downloader
        - service launching

        <b>Expected results</b>
        - response contains proper numpy shape

        """

        _, ports = start_server_single_vehicle_attrib_model
        imgs_path = os.path.join(vehicle_attributes_data_downloader, "images")

        imgs = np.zeros((0, 3, 72, 72), np.dtype('<f'))
        input_img = self.load_image(os.path.join(
            imgs_path, "021471_004.png"), 72, 72)
        imgs = np.append(imgs, input_img, axis=0)

        # Connect to grpc service
        stub = create_grpc_channel('localhost:{}'.format(ports["grpc_port"]),
                                   PREDICTION_SERVICE)

        in_name = 'input'
        out_color = 'color'
        out_type = 'type'
        output = infer(input_img, input_tensor=in_name, grpc_stub=stub,
                       model_spec_name='vehicle-attributes',
                       model_spec_version=None,
                       output_tensors=[out_color, out_type])

        sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),
                                                     '../../../ams_wrapper/')))
        from src.api.models.model_builder import ModelBuilder

        config_path = os.path.abspath(os.path.join(os.path.realpath(__file__),
                                                   '../../../ams_models/vehicle_attributes_model.json'))
        model_attrib = ModelBuilder.build_model(config_path, 4000)

        json_response = model_attrib.postprocess_inference_output(output)
        print("json_response=  " + str(json_response))

        class_count = str(json_response).count("color")

        print("detected types:" + str(class_count))
        assert class_count == 1

        class_count = str(json_response).count('"subtype": "type"')

        print("detected types:" + str(class_count))
        assert class_count == 1

        try:
            format_check = json.loads(json_response)
        except Exception as e:
            print("json loads exception:" + str(e))
            assert False

        print("format_check:" + str(format_check))
        assert format_check["inferences"][0]["subtype"] == "color"

        print("format_check:" + str(format_check))
        assert format_check["inferences"][1]["subtype"] == "type"

        first_color = (format_check["inferences"][0]["classification"]["tag"]["value"])
        print("first color:" + first_color)
        assert first_color == "red"

        first_type = (format_check["inferences"][1]["classification"]["tag"]["value"])
        print("first type:" + first_type)
        assert first_type == "truck"
