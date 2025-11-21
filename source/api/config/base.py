import re
from dotenv import dotenv_values
from pydantic.v1 import BaseSettings, Field
from dotenv import load_dotenv
from loguru import logger
import os
from typing import Literal, Optional

logger.debug("Status load env {e}", e=load_dotenv(".env", override=True))

class BaseSetting(BaseSettings):
    # API
    LLM_API_KEY : str
    LLM_BASE_URL : str
    EMBEDDING_BASE_URL : str

    # DB
    VECTOR_DB : str

    # AI
    MODEL_NAME : str
    EMBEDING_MODEL : str
    EMBEDDING_SIZE : str

    ACTIVE_ROUTERS : str
    PROJECT_SERVICE_PORT : str

    # PG
    BASE_POSTGRESQL_URL: str
    POSTGRESQL_TABLE_DOCUMENT : str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_DB: str

    COPYRIGHT: str = Field(default="Copyright (c) 2023 eBdesk Teknologi. All Rights Reserved.")

    class Config:
        env_file = ".env"


class Setting:
    instance = None

    def __new__(cls, *args, **kwargs):
        global settings
        if cls.instance is None:
            if kwargs.get("file"):
                env_values = dotenv_values(kwargs["file"])
                current_env = BaseSetting().dict()
                env_values = {_key: os.getenv(_key, '') for _key in env_values.keys() if _key in current_env}

                if kwargs.get("update_env"):
                    new_env = {}
                    for env in kwargs.get("update_env").split(" "):
                        if env.split("=")[0] in env_values:
                            new_env[env.split("=")[0]] = env.split("=")[1]
                    env_values.update(new_env)

                # if kwargs.get("routers"):
                #     env_values["ACTIVE_ROUTERS"] = build_routers(kwargs.get("routers"))
            else:
                # env_values["ACTIVE_ROUTERS"] = ""
                cls.instance = BaseSetting()
            settings = cls.instance
        return cls.instance


settings = Setting()
