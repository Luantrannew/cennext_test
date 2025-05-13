# bài test

Ứng dụng này bao gồm 3 phần:
- **part1**: Script Python độc lập (`part1/main.py`)
- **part2**: Script Python độc lập (`part2/main.py`) 
- **part3**: API viết bằng FastAPI (`part3.py`) — mặc định sẽ chạy

---

## 🚀 Yêu cầu
- Docker
- Docker Compose

---

## ⚙️ Hướng dẫn sử dụng

### 1. Build và khởi động phần part3 (FastAPI)
```bash
docker-compose up --build part3
```

Sau khi chạy xong, truy cập trình duyệt tại:
```
http://localhost:8000/books
```

### 2. Chạy thêm từng phần khi cần
Các phần `part1` và `part2` **không chạy tự động**, chỉ kích hoạt khi cần.

Chạy `part1`:
```bash
docker-compose up part1
```

Chạy `part2`:
```bash
docker-compose up part2
```

### 3. Dừng một phần cụ thể
```bash
docker-compose stop part1
docker-compose stop part2
docker-compose stop part3
```

### 4. Dừng và xóa toàn bộ container
```bash
docker-compose down
```

## 📁 Cấu trúc thư mục
```
.
├── part1/
│   └── main.py
├── part2/
│   └── main.py
├── part3.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 📌 Ghi chú
* Tất cả các phần dùng chung 1 Docker image (build từ `Dockerfile`)
* Các phần hoạt động độc lập và có thể chạy song song khi cần
