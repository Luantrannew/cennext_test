FROM python:3.11-slim

# Cài Chrome và ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    chromium \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/chrome-data && chmod 777 /tmp/chrome-data

# Cài đặt thư viện Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Mặc định chạy phần API (part3)
CMD ["uvicorn", "part3:app", "--host", "0.0.0.0", "--port", "8000"]
