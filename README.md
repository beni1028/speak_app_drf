# BackEnd for an APP to check weather using Django-Rest-Framework
Mini Project for SpeakAPP

## How to setup?
1. Clone the project
2. Open a console in the same directory as manage.py file in the clned repo
3. Create a virtual environment using the command: python -m venv venv (For linux use python3 -m venv venv)
4. Activate the environemnt: .\venv\Scripts.activate (For Lniux: source venv/bin/activate)
5. Intall requirements: pip install -r requirements.txt
6. Make Migrations: python manage.py makemigraions
7. Migrate: python manage.py migrate
8. Create Super User: python manage.py createsuperuser
9. Run server: python manage.py runserver
10. IF using Celery and Redis
    * In settings, set USE_CELERY = True (default will be False)
    * use command: celery -A weather_app worker -P gevent -l INFO


## APIs
1. /ap1/v1/signup/
2. /ap1/v1/login/
3. /ap1/v1/logout/
4. /ap1/v1/verify_account/?aid=
5. /ap1/v1/resend_verifiction/
6. /ap1/v1/get_weather_data/
