from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

COOKIE_KEY: str = "booking_access_token"


class Settings(BaseSettings):
    """Настройка приложения"""

    MODE: Literal["DEV", "PROD", "TEST"]

    LOG_LEVEL: Literal["INFO", "DEBUG"]

    # данные для базы данных PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # имя тестовой базы данных PostgreSQL
    TEST_DB_NAME: str

    # ключ для хешировани пользовательских паролей
    SECRET_KEY: str

    # алгоритм шифрования для JWT токена
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    # Для telegram бота
    BOT_TOKEN: str
    TG_USER_ID: int

    # Google авторизация
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_SECRET_KEY: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            + f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            + f"{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"
        )

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def TG_SEND_MESSAGE_URL(self):
        return f"https://api.telegram.org/bot{self.BOT_TOKEN}"

    @property
    def google_redirect_url(self) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code"
            f"&client_id={self.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.GOOGLE_REDIRECT_URI}"
            f"&scope=openid%20profile%20email&access_type=offline"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


async def get_settings() -> Settings:
    return Settings()
