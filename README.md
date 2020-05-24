# UpSalary
*Django REST API for salary payments*<br>

### Get Started

* Clone this repository using either SSH or HTTP on https://github.com/claytonrm/upsalary-django-project
* Install requirements
* Setup project

### Requirements
- [Python 3.8](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)
- [virtualenv](https://pypi.org/project/virtualenv/)
- [Docker](https://www.docker.com) and [docker-compose](https://docs.docker.com/compose/install/)

### Setup

* After download and clone project, inside your project folder:

```shell
cd app
virtualenv -p python3.8 env
source env/bin/activate

pip install -r requirements.txt

```

### Running App

On project root folder, run:

```shell
docker-compose up -d --build
docker-compose exec salaries python manage.py makemigrations
docker-compose exec salaries python manage.py migrate
```
Also, if you want to check some existing data, just run:
```shell
docker-compose exec salaries python manage.py loaddata salaries.json
```
* Now you can check the URL `http://localhost:8000/swagger-docs/`

#### Available operations
* You can try it out each of operations available in above URL or via [Postman](https://www.getpostman.com/)

### Running Tests
```shell
docker-compose exec salaries pytest -s -p no:warnings --cov=.
```
