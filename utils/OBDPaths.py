from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

class OBDPaths:
    """Central path routing repo"""

    UserDataTypes = PROJECT_ROOT / "config" / "user_datatype_config.json"
    Layouts = PROJECT_ROOT / "config" / "layouts"
    Data = PROJECT_ROOT / "data"