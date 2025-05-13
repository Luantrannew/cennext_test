📚 CENNEXT Multi-Service App
Ứng dụng được tách thành 3 phần riêng biệt, mỗi phần chạy dưới dạng một Docker service:

part1: Chạy script part1/main.py
part2: Chạy script part2/main.py
part3: API viết bằng FastAPI (part3.py) — mặc định sẽ chạy


🔧 Yêu cầu

Docker
Docker Compose


🚀 Cách sử dụng
1. Build & chạy phần part3 (FastAPI)
bashdocker-compose up --build api
2. Build & chạy phần part1 / part2
Chạy part1:
bashdocker-compose up part1
Chạy part2:
bashdocker-compose up part2
3. Dừng một phần cụ thể
bashdocker-compose stop part1
docker-compose stop part2
docker-compose stop part3
4. Dừng hệ thống
bashdocker-compose down
