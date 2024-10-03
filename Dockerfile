# Use Python as base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir -r app/requirements.txt

# Expose port 80 for the app
EXPOSE 80

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
