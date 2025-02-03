# Use official Python image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app


# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the application port (8080)
EXPOSE 8080

# Command to run the Flask app
CMD ["python", "app.py"]
