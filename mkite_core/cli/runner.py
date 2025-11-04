import os
import click
import importlib

from ase.io import read
from mkite_core.models import JobInfo, CrystalInfo, ConformerInfo
from mkite_core.plugins import get_recipe
from mkite_core.recipes.settings import EnvSettings


class RunnerCmd:
    def __init__(
        self,
        info: JobInfo,
        recipe: str,
        settings_path: os.PathLike,
    ):
        self.info = info

        if recipe is None:
            recipe = self.info.recipe["name"]

        recipe_cls = get_recipe(recipe).load()
        self.recipe = recipe_cls(self.info, settings_path)

    @staticmethod
    def load_info(info_path: os.PathLike):
        return JobInfo.from_json(info_path)

    def run(self):
        self.recipe.run()

    @classmethod
    def from_json(cls, info_path: str, recipe: str, settings_path: str):
        info = cls.load_info(info_path)
        return cls(info, recipe, settings_path)

    @classmethod
    def from_input(cls, inp_path: str, recipe: str, settings_path: str):
        if not os.path.exists(inp_path):
            raise FileNotFoundError(f"Input file {inp_path} not found")

        atoms = read(inp_path)
        if not all(atoms.pbc):
            raise NotImplementedError("Support for non-crystals not yet implemented")

        info = CrystalInfo.from_ase(atoms)

        jinfo = JobInfo(job={}, options={}, recipe={"name": recipe}, inputs=[info])
        jinfo.job["uuid"] = jinfo.create_uuid()

        return cls(jinfo, recipe, settings_path)


@click.command("run")
@click.option(
    "-r",
    "--recipe",
    type=str,
    default=None,
    help="name of the recipe that will be run. If not given, the name\
            is extracted from the jobinfo.json file.",
)
@click.option(
    "-s",
    "--settings",
    type=str,
    default=None,
    help="path to the settings.yaml file configuring the mkite runner",
)
@click.option(
    "-i",
    "--input_file",
    type=str,
    default="./jobinfo.json",
    help="path to the JobInfo file containing all\
            the information about the job to be run, \
            or to the structure file used as an input.",
)
def run(recipe, settings, input_file):
    if input_file.endswith(".json"):
        runner = RunnerCmd.from_json(input_file, recipe, settings)
    else:
        runner = RunnerCmd.from_input(input_file, recipe, settings)
    runner.run()
