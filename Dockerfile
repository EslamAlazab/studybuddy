FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=studybud.settings \
    PYTHONPATH=/app

CMD ["sh", "-c", "python manage.py migrate && gunicorn studybud.wsgi:application --bind 0.0.0.0:8000"]
