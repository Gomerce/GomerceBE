# Gomerce Backend Service

This is the backend for and open source ALX-T Udacity full-stack developer graduate project.
It is the backend API for a B2B2C e-commerce web application

# Collaboration

Our Pledge
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

We appreciate your time and effort made to support this project and so we have set out some guidelines to make this community effort worthwhile.

Informations on how best to contribute to this initiative can be found at the [CONTRIBUTING.md](./CONTRIBUTING.md)

# Requirements

```
Python 3.9 or higher
PostgreSQL 13.* or higher - recommended
```

# Setup

## Development Environment

Install this extension `Python` from Microsoft on your code editor (VS Code) or it's equivalent for the editor you use, to allow you to use the same coding style with everyone.

Setup your linter to follow `pycodestyle` and your formatter to follow `autopep8`

## Virtual environment

How to setup a python virtual environment

- Create the virtual environment,

  ```
  python -m venv .venv
  ```

- Activate the virtual environment
  - for windows
  ```
  .venv\Scripts\activate
  ```
  - for Linux / macOS
  ```
  source .venv/bin/activate
  ```
- Deactivate the virtual environment when you need to,

  ```
  deactivate
  ```

## Install requirements

For local development

```
pip install -r requirements.txt
```

For production

```
pip install -r requirements-prod.txt
```

## Set environment variables

- Make a copy of the `example.env` file, and rename it to `.env`

- Update the values of the variables in the `.env` file to suite your system environment.

- Create a folder named `logs` in the root directory, if it does not exist

- Create and accout on [Mailjet](https://www.mailjet.com) to get your `API_KEY` and `API_SECRET` for development process.
  make sure to validate your `EMAIL_SENDER_EMAIL` on mailjet first

## Integrating Google OAuth

### Create client_secret.json

### Note python 3.9.\* is required for google Oauth incorporation

1. visit <a href="https://www.google.co.in/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwj5ouHdnPD0AhXksFYBHbw3CfMQFnoECAkQAQ&url=https%3A%2F%2Fconsole.developers.google.com%2F&usg=AOvVaw39ieEDI7pzBj4NtuzqS57M"> Google CLoud Platform</a>
2. on the sidebar click on the credentials menu
3. To the top below the Navigation bar click on create credentials
4. select oauth_client
5. select web application
6. Fill the respective fields
7. Add a redirect url http://127.0.0.1:5000/callback
8. download the client_secretXXXXX.json file
9. Rename client_secretXXXXXX.json to client_secret.json
10. move to project root directory

### install google auth requirements

```
pip install -r requirements_google.txt
```

## Datebase setup

### Create databases

Create a Postgres database with the name matching what you have on the `.env` file for `DB_NAME` and `TEST_DB_NAME`. For example:

```
createdb gomerce
createdb gomerce-test
```

### Export your flask app

In order to run your migrations and app using the `flask` command, expose your flask app:

- for Linux / macOS

```
export FLASK_APP=src/server.py
```

- for windows
  - On CMD
  ```
  SET FLASK_APP="src/server.py"
  ```
  - On BASH
  ```
  export FLASK_APP="src/server.py"
  ```
  - On POWERSHELL
  ```
  $env:FLASK_APP="src/server.py"
  ```

### **Create database tables from migrations**

To add the existing database schema and dummy data to your datebase, run:

```
flask db upgrade
```

Make your database changes accessible to others using migrations

```
flask db migrate
```

### **Run server application**

From the root folder, run

```
python src/server.py
```

The application will run at the specified port `APPLICATION_PORT` in `.env` file

The local URL to access the API should be `http://localhost:3303/`

You can visit the Products URL to test the application at `http://localhost:3303/products`

The API Swagger documentation should be accessible at `http://localhost:3303/apidocs`



## docker run

```
# running cerbort
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org

# 
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org

# renew cert
docker compose run --rm certbot renew
```