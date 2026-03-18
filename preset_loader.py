import json

def load_presets(path="data/preset_registry.json"):
    with open(path, "r") as file:
        return json.load(file)

def get_constraints(presets, family, level):
    return presets[family]["levels"][str(level)]