from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str               # Токен для доступа к телеграм-боту


@dataclass
class SteamProfiles:
    profile_urls: list[str]  # Ссылки на профили, откуда собираем статистику игровых часов


@dataclass
class Config:
    tg_bot: TgBot
    steam_profiles: SteamProfiles


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        steam_profiles=list(
            map(str, env.list('STEAM_PROFILES'))
        ),
    )