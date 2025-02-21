# Base image with Python
FROM python:3.10-slim

# Install system packages and compilers
RUN apt update && apt install -y \
    g++ \
    gcc \
    make \
    libpq-dev \
    && apt clean

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for Django
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 3 --bind 0.0.0.0:8000 codeverse.wsgi:application"]
