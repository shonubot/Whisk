import glob
import os
import configparser
from rapidfuzz import fuzz

def get_applications():
    desktop_dirs = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
    apps = []

    for directory in desktop_dirs:
        for filepath in glob.glob(os.path.join(directory, "*.desktop")):
            config = configparser.ConfigParser()
            try:
                config.read(filepath)
                name = config.get("Desktop Entry", "Name")
                icon = config.get("Desktop Entry", "Icon", fallback="")
                apps.append((name, os.path.basename(filepath), icon))
            except Exception:
                continue

    return apps

def fuzzy_search(apps, query):
    if not query:
        return []
    return sorted(
        [(name, path, icon) for name, path, icon in apps if fuzz.partial_ratio(query.lower(), name.lower()) > 50],
        key=lambda x: fuzz.partial_ratio(query.lower(), x[0].lower()),
        reverse=True
    )
