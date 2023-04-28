import os
import yaml
import json
from pathlib import Path


def expand_file(filename: os.PathLike) -> dict:
    """Loads a YAML file and expands its environmental variables.
    A custom variable is the `${_self_}`, which is replaced by the
    folder where the given file is found.
    """
    path = Path(filename)
    with open(path, "r") as f:
        txt = f.read()

    root = str(path.parent.absolute())
    txt = os.path.expandvars(txt)
    txt = txt.replace("${_self_}", root)

    return txt


def load_config(filename: os.PathLike, expand=True):
    if expand:
        txt = expand_file(filename)
    else:
        with open(filename, "r") as f:
            txt = f.read()

    path = Path(filename)
    extension = path.suffix.strip(".")

    if extension in ["yaml", "yml"]:
        return yaml.safe_load(txt)

    if extension == "json":
        return json.loads(txt)

    raise ValueError(f"File {filename} has unrecognized extension {extension}")
