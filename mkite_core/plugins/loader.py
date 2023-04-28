from typing import List, Dict
from importlib import metadata


def get_entry_points(name: str) -> List[metadata.EntryPoint]:
    entry_points = metadata.entry_points()
    if name not in entry_points:
        return []

    return list(set(entry_points[name]))


def get_recipes() -> Dict[str, metadata.EntryPoint]:
    entries = get_entry_points("mkite.recipes")
    return {entry.name: entry for entry in entries}


def get_recipe(name: str) -> metadata.EntryPoint:
    recipes = get_recipes()
    return recipes[name]
