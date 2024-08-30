from pydantic import Field, DirectoryPath, FilePath
from mkite_core.external import load_config
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    """Wraps and obtains all settings for the environmental variables"""

    SCRATCH_DIR: DirectoryPath = Field(
        ".",
        description="Root directory for all temporary files and calculations",
    )

    @classmethod
    def from_file(cls, filename: FilePath):
        data = load_config(filename)
        return cls(**data)
