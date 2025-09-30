# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY rq.txt .
RUN pip install --no-cache-dir -r rq.txt

# Copy project files into container
COPY . .

# Default command (can be overridden by cron)
CMD ["python3", "scripts/daily_script.py"]
