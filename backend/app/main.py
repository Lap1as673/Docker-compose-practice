from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware  # Импортируем middleware
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener microservice",
    version="1.0.0"
)

# Настройка CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)


@app.post("/shorten/", response_model=schemas.URLInfoResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):   

    db_url = crud.create_url_mapping(db, url.original_url)
    
    # Формируем полный URL для статистики
    base_url = "http://localhost:8000"  # В проде заменить на домен
    admin_url = f"{base_url}/stats/{db_url.short_code}"
    
    return schemas.URLInfoResponse(
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        created_at=db_url.created_at,
        click_count=db_url.click_count,
        admin_url=admin_url
    )

@app.get("/{short_code}")
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):    
    db_url = crud.get_url_mapping_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    
    # Обновляем счетчик кликов
    crud.increment_click_count(db, db_url)
    
    return RedirectResponse(url=db_url.original_url)

@app.get("/stats/{short_code}", response_model=schemas.URLInfo)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):    
    db_url = crud.get_url_info(db, short_code)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    return db_url

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API"}

# Эндпоинт для проверки здоровья (полезно для Docker)
@app.get("/health")
def health_check():
    return {"status": "healthy"}