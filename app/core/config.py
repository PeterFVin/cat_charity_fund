from typing import Optional

from pydantic import BaseSettings, EmailStr


APP_TITTLE = 'Благотворительный фонд поддержки котиков'


class Settings(BaseSettings):
    app_title: str = APP_TITTLE
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
