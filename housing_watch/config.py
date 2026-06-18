import json
from pathlib import Path


DEFAULT_CONFIG = Path("config/sources.json")


def load_config(path=None):
    config_path = Path(path or DEFAULT_CONFIG)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    config["_path"] = str(config_path)
    return config


def enabled_sources(config, source_id=None):
    sources = config.get("sources", [])
    if source_id:
        return [source for source in sources if source.get("id") == source_id]
    return [source for source in sources if source.get("enabled", False)]


def scoped_regions(config):
    return config.get("interest", {}).get("regions", [])


def database_path(config):
    return Path(config.get("project", {}).get("database_path", "data/housing_watch.sqlite"))
