
# Use the official lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender-dev \
    libxext6 \
    libopencv-dev

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8080 to allow communication to/from server
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
