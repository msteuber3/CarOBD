import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict
from utils.DataTypes import DataType
from utils.OBDPaths import OBDPaths


@dataclass
class Layout:
    default: bool
    name: str
    source: str
    default_widgets: List[str]
    custom_widgets: List[DataType]
    sequence_map: List[str] = field(default_factory=list)


def serialize_layout(layout: Layout) -> str:
    """
    Converts a Layouts object into a JSON string, merging the separate
    widget lists into a single ordered 'widgets' list for the file.
    """
    ordered_widgets = []

    for key in layout.sequence_map:
        tag, index_str = key.split(':')
        index = int(index_str)

        if tag == 'd':
            widget_id = layout.default_widgets[index]
            ordered_widgets.append({
                "type": "default",
                "data": widget_id
            })
        elif tag == 'c':
            widget_obj = layout.custom_widgets[index]
            ordered_widgets.append({
                "type": "custom",
                "data": asdict(widget_obj)
            })

    layout_dict = {
        "default": layout.default,
        "name": layout.name,
        "source": layout.source,
        "widgets": ordered_widgets
    }

    return json.dumps(layout_dict, indent=4)


def load_layout(json_str: str) -> Layout:
    """
    Parses a JSON string into a Layouts object, splitting the single 'widgets'
    list into default_widgets, custom_widgets, and generating the sequence_map.
    """
    data = json.loads(json_str)

    default_widgets = []
    custom_widgets = []
    sequence_map = []

    for widget in data.get("widgets", []):
        w_type = widget["type"]
        w_data = widget["data"]

        if w_type == "default":
            default_widgets.append(w_data)
            sequence_map.append(f"d:{len(default_widgets) - 1}")

        elif w_type == "custom":
            datatype_obj = DataType(**w_data)
            custom_widgets.append(datatype_obj)
            sequence_map.append(f"c:{len(custom_widgets) - 1}")

    return Layout(
        default=data["default"],
        name=data["name"],
        source=data["source"],
        default_widgets=default_widgets,
        custom_widgets=custom_widgets,
        sequence_map=sequence_map
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
        layouts_dict[f.replace(".json", "")] = load_layout(open(f"{path}/{f}", "r").read())

    return layouts_dict
