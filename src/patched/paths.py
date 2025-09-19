from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
WEB_DIR = PROJECT_ROOT / "web"
WEB_TEMPLATES_DIR = WEB_DIR / "templates"
WEB_OUTPUTS_DIR = WEB_DIR / "outputs"

__all__ = [
    "PACKAGE_ROOT",
    "PROJECT_ROOT",
    "DATA_DIR",
    "DATA_RAW_DIR",
    "DATA_PROCESSED_DIR",
    "WEB_DIR",
    "WEB_TEMPLATES_DIR",
    "WEB_OUTPUTS_DIR",
]
