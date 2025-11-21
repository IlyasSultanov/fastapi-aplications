echo "Start migrations"

exec alembic upgrade head

echo "Finish migrations"