from typing import List
from pydantic import BaseModel, ValidationError
import yaml

CONFIG_PATH = "src/config.yaml"


class Config(BaseModel):
    lastfm_api_key: str
    filename_format: str
    tags: List[str]


def save_config(config: Config) -> None:
    # will create the file if one does not exist, no need to handle
    with open(CONFIG_PATH, "w") as file:
        file.truncate(0)
        yaml.safe_dump(config.model_dump(), file)


def load_config() -> Config:
    # use try so we can catch if the file does not exist
    try:
        with open(CONFIG_PATH, "r") as file:
            data = yaml.safe_load(file)
            return Config(**data)
    except FileNotFoundError as _:
        # use the default values and save a new config file
        config = Config(lastfm_api_key="", filename_format="", tags=[])
        save_config(config)
        return config
    except ValidationError as validation_error:
        # TODO: i would like to have a toast message that warns the user about this
        # use the default config but do NOT overwrite the existing one
        return Config(lastfm_api_key="", filename_format="", tags=[])
