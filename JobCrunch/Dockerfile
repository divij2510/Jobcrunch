FROM python:3.11.12-slim

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # Chrome dependencies
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxshmfence1 \
    libxss1 \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install latest stable Chrome from official repo
RUN apt-get update && apt-get install -y \
    curl jq unzip \
    && curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json > /tmp/versions.json \
    && CHROME_URL=$(jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url' /tmp/versions.json) \
    && wget -q --continue -O /tmp/chrome-linux64.zip "$CHROME_URL" \
    && unzip /tmp/chrome-linux64.zip -d /usr/local/bin/chrome \
    && chmod +x /usr/local/bin/chrome/chrome-linux64/chrome \
    && ln -s /usr/local/bin/chrome/chrome-linux64/chrome /usr/bin/google-chrome \
    && rm -rf /tmp/chrome-linux64.zip /tmp/versions.json

# Set environment variables
ENV CHROME_BIN=/usr/local/bin/chrome/chrome-linux64/chrome
ENV PATH="/usr/local/bin/chrome/chrome-linux64:${PATH}"

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
CMD ["sh", "-c", "python manage.py makemigrations jobscraper && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 300 JobCrunch.wsgi:application"]
