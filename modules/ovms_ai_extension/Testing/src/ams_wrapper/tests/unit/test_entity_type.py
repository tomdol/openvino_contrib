#
# Copyright (c) 2020-2023 Intel Corporation
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

from src.api.types import Tag, Rectangle, SingleEntity, Entity, Detection


def test_single_entity():
    expected_dict = {
        "tag": {
            "value": "car",
            "confidence": 0.97
        },
        "box": {"l": 1.0, "t": 2.0, "w": 3.0, "h": 4.0}
    }

    tag = Tag("car", 0.97)
    box = Rectangle(1.0, 2.0, 3.0, 4.0)
    single_entity = SingleEntity(tag, box)
    assert expected_dict == single_entity.as_dict()


def test_entity():
    detections = []
    entities = []
    expected_dict = {
        'inferences': [
            {
                'type': 'entity',
                'subtype': 'vehicleDetection',
                'entity': {
                    'tag': {'value': 'car', 'confidence': 0.97},
                    'box': {'l': 1.0, 't': 2.0, 'w': 3.0, 'h': 4.0}
                    }
            },
            {
                'type': 'entity',
                'subtype': 'vehicleDetection',
                'entity': {
                    'tag': {'value': 'bike', 'confidence': 0.94},
                    'box': {'l': 0.0, 't': 0.0, 'w': 0.0, 'h': 0.0}
                    }
            }
        ]
    }
    detections = [
        SingleEntity(Tag("car", 0.97), Rectangle(1.0, 2.0, 3.0, 4.0)),
        SingleEntity(Tag("bike", 0.94), Rectangle(0.0, 0.0, 0.0, 0.0)),
    ]
    for detection in detections:
        entity = Entity(subtype_name="vehicleDetection", entity=detection)
        entities.append(entity)
    model_detection = Detection(entities=entities)
    print(model_detection.as_dict())
    assert expected_dict == model_detection.as_dict()
