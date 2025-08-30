from pydantic import BaseModel, HttpUrl
from datetime import datetime

# Схема для создания новой короткой ссылки
class URLBase(BaseModel):
    original_url: HttpUrl  # Pydantic автоматически валидирует URL

# Схема, возвращаемая после создания ссылки
class URLCreate(URLBase):
    pass

# Схема, возвращаемая при запросе информации о ссылке
class URLInfo(URLBase):
    short_code: str
    created_at: datetime
    click_count: int

    class Config:
        from_attributes = True  # Работа с ORM (ранее orm_mode)

# Схема для ответа, содержащая короткую ссылку
class URLInfoResponse(URLInfo):
    admin_url: str  # URL для просмотра статистики