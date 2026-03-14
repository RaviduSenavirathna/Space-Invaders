import json
import os

# Path to config file in project root (same folder as main.py)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

# Default configuration values (easy to read and expand later)
DEFAULT_CONFIG = {
    "window": {
        "width": 800,
        "height": 600
    },
    "music_volume": 70,  # percent 0-100
    "controls": {
        "move_left": "K_LEFT",
        "move_right": "K_RIGHT",
        "shoot": "K_SPACE",
        "pause": "K_ESCAPE",
        "restart": "K_r"
    }
}


def _write_default_config(path=CONFIG_PATH):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)


def get_config():
    """Load configuration from disk, create default if missing or invalid."""
    if not os.path.exists(CONFIG_PATH):
        _write_default_config()

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
    except (json.JSONDecodeError, OSError):
        # Recreate config file if it is malformed
        _write_default_config()
        loaded = DEFAULT_CONFIG.copy()

    # Merge defaults with loaded values for missing keys
    merged = DEFAULT_CONFIG.copy()
    if isinstance(loaded, dict):
        merged.update({k: v for k, v in loaded.items() if v is not None})
        if isinstance(loaded.get('window'), dict):
            merged['window'].update(loaded['window'])
        if isinstance(loaded.get('controls'), dict):
            merged['controls'].update(loaded['controls'])
        if 'music_volume' in loaded:
            merged['music_volume'] = loaded.get('music_volume', merged['music_volume'])

    return merged
