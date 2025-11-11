import logging
from typing import List
from pydantic import BaseModel, ValidationError
from textual.app import App
from textual.logging import TextualHandler
import yaml

CONFIG_PATH = "src/config.yaml"

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)

class Config(BaseModel):
    lastfm_api_key: str
    filename_format: str
    tags: List[str]


def save_config(config: Config) -> None:
    # will create the file if one does not exist, no need to handle
    with open(CONFIG_PATH, "w") as file:
        file.truncate(0)
        yaml.safe_dump(config.model_dump(), file)


def load_config(app: App) -> Config:
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
        app.notify(
                "Your config.yaml is not formatted correctly! Using a default config instead.",
                severity="error",
            )
        logging.error("Malformed config.yaml:", validation_error)
        # return a default blank config and do not overwrite the existing config.yaml
        return Config(lastfm_api_key="", filename_format="", tags=[])
