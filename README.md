
# Getting started

## Alvarado ISD Workshop

### Install Dependencies

1. Install global dependencies

        sudo easy_install virtualenv

1. Run setup script

        ./setup

### Run

1. Activate virtualenv

        source activate-workshop

1. Run django

        python manage.py syncdb (to create your local database)
        python manage.py createsuperuser (to create your admin user)
        python manage.py runserver

1. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) for Django.
