import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')

    @classmethod
    def validate(cls):
        """Проверка обязательных параметров конфигурации."""
        missing = [attr for attr in ['JWT_SECRET', 'JWT_ALGORITHM', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_HOST'] if getattr(cls, attr) is None]
        if missing:
            raise EnvironmentError(f"Следующие ENV отсутствуют: {', '.join(missing)}")


Config.validate()
