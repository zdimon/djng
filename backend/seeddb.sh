#!/bin/sh
# wait-for-seeddb.sh
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing seed"
cd /app
python manage.py migrate
python manage.py load_settings
python manage.py load_users
python manage.py load_administration
python manage.py load_media
python manage.py load_feed
python manage.py load_subscription
python manage.py load_payment_types
python manage.py load_payment
python manage.py load_props
python manage.py load_stickers
#python manage.py load_messages
#python manage.py load_agency
#python manage.py load_webmaster
#python manage.py load_category
#python manage.py load_product
#python manage.py load_menu

>&2 echo "Postgres is up - executing command"
exec $cmd
