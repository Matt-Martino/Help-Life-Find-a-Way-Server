rm db.sqlite3
rm -rf ./helplifeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations helplifeapi
python3 manage.py migrate helplifeapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata plant_type
python3 manage.py loaddata care_tip
python3 manage.py loaddata plant
