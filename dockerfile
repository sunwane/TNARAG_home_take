FROM python:3.10-slim

# Không tạo file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# In log ngay lập tức
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]