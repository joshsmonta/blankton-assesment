FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Create a non-root user and set permissions
# RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
# USER appuser  # Switch to the non-root user

# Run the Celery worker under the new user
# RUN celery -A dashboard_service worker --loglevel=info
# Copy the superuser creation script
COPY create_superuser.py /app/create_superuser.py

# Run migrations and create superuser
RUN python manage.py migrate && \
    python manage.py shell < create_superuser.py

CMD ["sh", "-c", "python3 manage.py test && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8001"]
