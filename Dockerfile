FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations before starting the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 3 --bind 0.0.0.0:8000 codeverse.wsgi:application"]
