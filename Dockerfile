# Start from the official Python base image.
FROM python:3.9.4-slim

# Set the current working directory to /code.
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the file with the requirements to the root directory.
COPY requirements.txt .

# Install the package dependencies in the requirements file.
RUN pip install -r requirements.txt

# Copy the directory
COPY . .

# Set the command to run the uvicorn server.
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80"]

