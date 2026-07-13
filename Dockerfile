FROM python:3.12-slim

WORKDIR /app

# Dependencies install karo
COPY requirements.txt .
RUN pip install -r requirements.txt

# Code copy karo
COPY . .

# Static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "school_mgmt.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]