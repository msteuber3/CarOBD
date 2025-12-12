import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from custom_widgets.DisplayMeter import DisplayMeter

class DisplayMeterSerial(Enum):
    CIRCULAR_GAUGE = "circular_gauge"
    PLAIN_TEXT = "plain_text"
    HORIZONTAL_TACHOMETER = "horizontal_tachometer"
    def pretty(self):
        if self == DisplayMeterSerial.CIRCULAR_GAUGE:
            return "Circular Gauge"
        elif self == DisplayMeterSerial.PLAIN_TEXT:
            return "Plain Text"
        elif self == DisplayMeterSerial.HORIZONTAL_TACHOMETER:
            return "Horizontal Tachometer"
        return None

@dataclass
class DataType:
    name: str
    min_value: int
    max_value: int
    default_unit: str
    alternate_units: List[str]
    default_display_type: DisplayMeterSerial # TODO: Come back to this, can I go direct to DisplayMeter? and if i can, do i want to?
    alternate_display_types: List[DisplayMeterSerial]

def load_datatypes_from_json(json_data: str) -> Dict[str, DataType]:
    """
    Parses a JSON string and returns a dictionary of DataType objects.
    """
    parsed_data = json.loads(json_data)
    datatype_objects = {}

    for key, item in parsed_data.items():
        default_display = DisplayMeterSerial(item["default_display_type"])
        alt_displays = [DisplayMeterSerial(dt) for dt in item["alternate_display_types"]]

        dt_obj = DataType(
            name=item["name"],
            min_value=item["min_value"],
            max_value=item["max_value"],
            default_unit=item["default_unit"],
            alternate_units=item["alternate_units"],
            default_display_type=default_display,
            alternate_display_types=alt_displays
        )

        datatype_objects[key] = dt_obj

    return datatype_objects

def serialize_datatypes_to_json(datatypes: Dict[str, DataType]) -> str:
    """
    Serializes a dictionary of DataType objects to a JSON string.
    """
    serialized_data = {}

    for key, datatype in datatypes.items():
        serialized_data[key] = {
            "name": datatype.name,
            "min_value": datatype.min_value,
            "max_value": datatype.max_value,
            "default_unit": datatype.default_unit,
            "alternate_units": datatype.alternate_units,
            "default_display_type": datatype.default_display_type.value,
            "alternate_display_types": [dt.value for dt in datatype.alternate_display_types]
        }

    return json.dumps(serialized_data)