# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all files into container
COPY . /app/

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
