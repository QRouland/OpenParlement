FROM python:alpine3.13

# Create a app directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir PyMySQL

# Copy files
COPY ./app /app/app
COPY ./commands /app/commands
COPY ./migrations /app/migrations
COPY ./specs /app/specs
COPY ./LICENSE.md /app/LICENSE.md
COPY ./alembic.ini /app/alembic.ini
COPY ./main.py /app/main.py

# Copy crontab file and script
COPY ./docker/cronjob /etc/crontabs/root
COPY --chmod=755 ./docker/db_update.sh /app/db_update.sh

# Expose ports
EXPOSE 8000

# Run the Gunicorn
COPY --chmod=755 ./docker/start.sh /start.sh
CMD ["/start.sh"]
