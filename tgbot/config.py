import os
from dataclasses import dataclass


@dataclass
class DbConfig:
    password: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None) -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv("TOKEN", "token"),
        ),
        db=DbConfig(
            password=os.getenv("DB_PASSWORD", 'password'),
        ),
    )
