# -------------------------------
# Minimal Dockerfile (with migrate)
# -------------------------------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app /app

# Expose your app port
EXPOSE 8000

# Run migrations and start the app
CMD ["sh", "-c", "python3 manage.py migrate && uvicorn main:app --host 0.0.0.0 --port 8000"]
