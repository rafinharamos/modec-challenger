# modec-challenge

Application to modec challenge.

## Documentation

You can find a postman collection for the API and do some tests at the root of the project (colections_modec_api)

You can also have access to the complete system running on heroku at the address (https://modec-rafinharamos.herokuapp.com/)

Through this link you can access the administrative panel for testing. Just put **admin** at the end of the address (https://modec-rafinharamos.herokuapp.com/admin)

Username and password are in the challenge response email

Note: *Note that the first request may take a while because it is a free service, so it goes to sleep mode when is not being used.*

## Requirements

* Python 3

## Instalation

In the linux terminal, create a virtual environment:

`$ Python -m venv .modec` 

Activate the virtual environment:

`$ source .modec/bin/activate`

After downloading the project, at the root of it run the following command to install the dependencies:

`$ pip install -r requirements.txt`

Note: Make sure that python (3.x) is installed

Now run the command to run the server in an approval environment:

`$ python manage.py runserver`

Now, you have an running API on your localhost on the port 8000.

In the local environment it is possible to create a superuser to use the administrative environment:

`$ python manage.py createsuperuser`

You can use the provided credentials to access the administrative environment on `https://localhost:8000/admin/`.




