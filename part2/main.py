import requests
import json
import os
import random
from typing import List, Dict, Any

def get_countries() -> List[str]:
    url = "https://restcountries.com/v3.1/all?fields=name"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"API gọi thất bại với mã lỗi: {response.status_code}")
    
    countries_data = response.json()
    country_names = [country["name"]["common"] for country in countries_data]
    return country_names


def read_books_data(file_path: str) -> List[Dict[str, Any]]:
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        print("File không phải định dạng JSON")

def assign_random_countries(books: List[Dict[str, Any]], countries: List[str]) -> List[Dict[str, Any]]:
    updated_books = []
    
    for book in books:
        updated_book = book.copy()
        updated_book["publisher_country"] = random.choice(countries)
        updated_books.append(updated_book)
    return updated_books

def save_to_json(data: List[Dict[str, Any]], output_file: str) -> None:
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"Dữ liệu đã được lưu vào {output_file}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "..", "data", "part1", "books.json")
    output_file = os.path.join(base_dir, "..", "data", "part2", "books_with_country.json")

    if not os.path.exists(output_file):
         os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        print("Đang lấy danh sách quốc gia...")
        countries = get_countries()
        print(f"Đã lấy {len(countries)} quốc gia")
        
        # Đọc dữ liệu sách
        print(f"Đang đọc dữ liệu sách từ {input_file}...")
        books = read_books_data(input_file)
        print(f"Đã đọc {len(books)} cuốn sách")
        
        # Gán quốc gia ngẫu nhiên cho mỗi cuốn sách
        print("Đang gán quốc gia ngẫu nhiên cho mỗi cuốn sách...")
        updated_books = assign_random_countries(books, countries)
        
        # Lưu dữ liệu đã cập nhật
        print(f"Đang lưu dữ liệu đã cập nhật vào {output_file}...")
        save_to_json(updated_books, output_file)
        
        print("Hoàn thành!")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()