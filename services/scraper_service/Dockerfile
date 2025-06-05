FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Chrome for Selenium
RUN apt-get update && apt-get install -y \
    gcc \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements/services/scraper_service.txt requirements.txt
COPY finance_common/ /app/finance_common/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/scraper_service/ /app/

# Set environment variables
ENV PYTHONPATH=/app
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

# Expose port
EXPOSE 8002

# Run scraper service
CMD ["python", "-m", "bank_scraper.api"] 