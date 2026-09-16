from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import json
from typing import List

class Settings(BaseSettings):
    bot_token: str = Field(alias='BOT_TOKEN')
    admin_ids: str = Field(alias='ADMIN_IDS')
    gemini_api_key: str = Field(alias='GEMINI_API_KEY', default="")

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @property
    def admins(self) -> List[int]:
        try:
            return json.loads(self.admin_ids)
        except:
            return []

config = Settings()
