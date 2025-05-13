from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import os
import json

app = FastAPI()

# Load books data on startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "part2", "books_with_country.json")

books_data: List[dict] = []

def load_books():
    global books_data
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Không tìm thấy file: {DATA_PATH}")
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        books_data = json.load(f)

def save_books():
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)

@app.on_event("startup")
def startup_event():
    load_books()

@app.get("/books", summary="Lấy danh sách sách", response_description="Danh sách sách")
def get_books(country: Optional[str] = Query(None, description="Lọc theo quốc gia xuất bản")):
    if country:
        filtered = [book for book in books_data if book.get("publisher_country", "").lower() == country.lower()]
        return filtered
    return books_data

@app.post("/books", summary="Thêm sách mới")
def add_book(book: dict):
    if "title" not in book:
        raise HTTPException(status_code=400, detail="Thiếu trường 'title'")
    
    # Kiểm tra trùng
    if any(b['title'].lower() == book['title'].lower() for b in books_data):
        raise HTTPException(status_code=409, detail="Sách đã tồn tại")
    
    books_data.append(book)
    save_books()
    return {"message": "Thêm sách thành công", "book": book}

@app.delete("/books/{title}", summary="Xoá sách theo tiêu đề")
def delete_book(title: str):
    global books_data
    original_count = len(books_data)
    books_data = [book for book in books_data if book['title'].lower() != title.lower()]
    
    if len(books_data) == original_count:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách")

    save_books()
    return {"message": f"Đã xoá sách: {title}"}
