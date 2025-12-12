import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict
from utils.DataTypes import DataType, serialize_datatypes_to_json, load_datatypes_from_json, DisplayMeterSerial
from utils.OBDPaths import OBDPaths


@dataclass
class Layout:
    default: bool
    name: str
    source: str
    widgets: Dict[str, DataType]


def serialize_layout(layout: Layout) -> str:
    """
    Converts a Layouts object into a JSON string, merging the separate
    widget lists into a single ordered 'widgets' list for the file.
    """
    layout_dict = {
        "default": layout.default,
        "name": layout.name,
        "source": layout.source,
        "widgets": serialize_datatypes_to_json(layout.widgets)
    }

    return json.dumps(layout_dict)


def load_layout(json_str: str) -> Layout:
    """
    Parses a JSON string into a Layouts object, splitting the single 'widgets'
    list into default_widgets, custom_widgets, and generating the sequence_map.
    """
    data = json.loads(json_str)
    datatypes_dict = {}
    for key, item in data["widgets"].items():
        default_display = DisplayMeterSerial(item["default_display_type"])
        alt_displays = [DisplayMeterSerial(dt) for dt in item["alternate_display_types"]]
        datatypes_dict[key] = DataType(
            name=item["name"],
            min_value=item["min_value"],
            max_value=item["max_value"],
            default_unit=item["default_unit"],
            alternate_units=item["alternate_units"],
            default_display_type=default_display,
            alternate_display_types=alt_displays
        )

    return Layout(
        default=data["default"],
        name=data["name"],
        source=data["source"],
        widgets=datatypes_dict,
    )


def load_default_layout() -> Layout | None:
    layouts_dict = load_all_layouts()
    for layout in layouts_dict.values():
        if layout.default:
            return layout
    return None


def load_all_layouts(path=OBDPaths.Layouts) -> Dict[str, Layout]:
    layouts_dict = {}
    for f in os.listdir(path):
        with open(path / f, encoding='utf-8') as json_file:
            loaded_layout = load_layout(json_file.read())
            layouts_dict[f] = loaded_layout

    return layouts_dict
