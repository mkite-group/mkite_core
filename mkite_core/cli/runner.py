import os
import click
import importlib

from mkite_core.models import JobInfo
from mkite_core.plugins import get_recipe
from mkite_core.recipes.settings import EnvSettings


class RunnerCmd:
    def __init__(
        self,
        recipe: str,
        settings_path: os.PathLike,
        info_path: os.PathLike,
    ):
        self.info = self.load_info(info_path)

        if recipe is None:
            recipe = self.info.recipe["name"]

        recipe_cls = get_recipe(recipe).load()
        self.recipe = recipe_cls(self.info, settings_path)

    def load_info(self, info_path: os.PathLike):
        return JobInfo.from_json(info_path)

    def run(self):
        self.recipe.run()


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
    "--info",
    type=str,
    default="./jobinfo.json",
    help="path to the JobInfo file containing all\
            the information about the job to be run.",
)
def run(recipe, settings, info):
    runner = RunnerCmd(recipe, settings, info)
    runner.run()
