# Use the official Python image
FROM python:3.11.4

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

ARG SECRET_KEY
ARG EMAIL_HOST_PASSWORD
ARG DATABASE_URL

# Set environment variables
ENV SECRET_KEY=${SECRET_KEY}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV DATABASE_URL=${DATABASE_URL}

# Collect static files (if required for deployment)
RUN python manage.py collectstatic --noinput

# Expose the port used by the application
EXPOSE 8000

# Command to start the application
CMD ["gunicorn", "JWTAUth.wsgi:application", "--bind", "0.0.0.0:8000"]
