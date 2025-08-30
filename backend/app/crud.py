from sqlalchemy.orm import Session
import secrets
import string
from models import URLMapping

# Функция для генерации случайного короткого кода
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Создание новой записи в БД
def create_url_mapping(db: Session, original_url: str) -> URLMapping:
    # Генерируем код до тех пор, пока не найдем уникальный
    while True:
        short_code = generate_short_code()
        if not get_url_mapping_by_short_code(db, short_code):
            break

    db_url = URLMapping(original_url=original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

# Поиск оригинального URL по короткому коду
def get_url_mapping_by_short_code(db: Session, short_code: str) -> URLMapping:
    return db.query(URLMapping).filter(URLMapping.short_code == short_code).first()

# Обновление счетчика кликов
def increment_click_count(db: Session, db_url: URLMapping) -> URLMapping:
    db_url.click_count += 1
    db.commit()
    db.refresh(db_url)
    return db_url

# Получение информации о ссылке по коду (для статистики)
def get_url_info(db: Session, short_code: str) -> URLMapping:
    return db.query(URLMapping).filter(URLMapping.short_code == short_code).first()