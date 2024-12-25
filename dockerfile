# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "system_traiteur.wsgi:application", "--bind", "0.0.0.0:8000"]
