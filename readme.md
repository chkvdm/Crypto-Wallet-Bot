# Crypto Sandbox API

Backend code for telegram bot 'crypto-sandbox-api'. Allows the user to simulate a crypto wallet with a start balance.  
Based on real exchange rates, buy and sell cryptocurrencies. View your activity data and monitor your balance.

## Technologies used

* **[Python3](https://www.python.org/downloads/)** - A programming language.
* **[PostgreSQL](https://www.postgresql.org/download/)** – Powerful, open source object-relational database system that uses and extends the SQL language.
* **[Flask](https://flask.palletsprojects.com/en/2.2.x/installation/)** - A microframework for Python based on WSGI, Werkzeug and Jinja 2.
* **[Flask-marshmallow](https://www.sqlalchemy.org/download.html)** - Flask-Marshmallow is a thin integration layer for Flask and marshmallow that adds additional features to marshmallow.
* **[SQLAlchemy](https://www.sqlalchemy.org/download.html)** - Python SQL toolkit and Object Relational Mapper.  
* And other requirements which are in the pipfile.

## Local development

The project comes with a basic configuration for build from sources or [Docker](https://www.docker.com/).

Build from sources:

```bash
$ git clone https://github.com/chkvdm/crypto-sandbox-api.git
$ cd crypto-sandbox-api
$
$ # activate the Pipenv shell
$ pipenv shell
$
$ # Install requirements
$ pipenv install
$
$ # start postgres and create database with docker-compose.yaml
$ docker-compose up
$
$ # run the flask run.py
$ flask --app run run
```

Start the app using Docker:

```bash
$ # Get the code
$ git clone https://github.com/chkvdm/crypto-sandbox-api.git
$ cd crypto-sandbox-api
$
$ # Start the app in Docker
$ ###################
```

## Testing

The project includes a complete postman collection of HTTP requests to all API endpoints. You can imported collection [from](./postman).  

<img width="900" alt="postman-screenshoot" src="https://user-images.githubusercontent.com/107465582/210433192-823e0391-8956-4af1-8b70-8d3b53b302a5.png">

## Authors

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRr0qq7pHt2RAjrMGGKJ_-460bOO8Mpb038TQ&usqp=CAU" height="16"/>  [Vadim Chaiko](https://www.linkedin.com/in/vadim-chaiko-712279127/)

## License

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)