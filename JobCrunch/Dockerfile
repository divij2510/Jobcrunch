FROM python:3.11.12-slim

# Install dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    jq \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install specific Chrome version (135.0.7049.114)
RUN CHROME_VERSION="135.0.7049.114" \
    && CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
    && wget -q --continue -O /tmp/chrome-linux64.zip "$CHROME_URL" \
    && unzip /tmp/chrome-linux64.zip -d /opt/chrome \
    && chmod +x /opt/chrome/chrome-linux64/chrome \
    && rm -rf /tmp/chrome-linux64.zip

# Set Chrome binary location
ENV CHROME_BIN=/opt/chrome/chrome-linux64/chrome

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["sh", "-c", "python manage.py makemigrations jobscraper && python manage.py migrate && gunicorn --bind 0.0.0.0:8000  --workers 3 --timeout 300 JobCrunch.wsgi:application"]
