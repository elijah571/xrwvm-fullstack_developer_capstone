# Base image with Python and Node (for React build)
FROM python:3.12.0-slim-bookworm

# Install Node.js (for building frontend) and other dependencies
RUN apt-get update && apt-get install -y curl build-essential git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP=/app
WORKDIR $APP

# Copy Python dependencies and install
COPY requirements.txt $APP/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . $APP/

# Build React frontend
WORKDIR $APP/frontend
RUN npm install && npm run build

# Move back to app root
WORKDIR $APP

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Entrypoint and default command
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "djangoproj.wsgi:application"]
