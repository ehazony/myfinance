FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements/services/telegram_bot_service.txt requirements.txt
COPY finance_common/ /app/finance_common/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/telegram_bot_service/ /app/

# Set environment variables
ENV PYTHONPATH=/app

# Run telegram bot
CMD ["python", "-m", "telegram_bot.bot"] 