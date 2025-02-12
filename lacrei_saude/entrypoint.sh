#!/bin/sh
DB_TABLES_COUNT=$(python manage.py shell -c "from django.db import connection; print(len(connection.introspection.table_names()))")

if [ "$DB_TABLES_COUNT" -eq 0 ]; then
    echo "Running database migrations..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput

    echo "Initializing database..."
    python manage.py init_db
fi

exec "$@"