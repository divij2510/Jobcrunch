FROM python:3.11.12-slim

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Install latest stable Chrome from official repo
RUN apt-get update && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get install -y firefox-esr \
    && apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["sh", "-c", "python manage.py makemigrations jobscraper && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 300 JobCrunch.wsgi:application"]
