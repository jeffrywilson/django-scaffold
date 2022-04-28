# Django Scaffold

This is a basic scaffold for Django projects with support to create an API

## Development quickstart guide - Bare Install

### Requirements

The following software is required to build and run Django Scaffold in development mode:

* MacOS / Linux / Windows system
* Python 3.8.9 
* PostgreSQL 12.2

### MacOS setup

If you don't already have PostgreSQL setup, install it via [Postgres.app](https://postgresapp.com/). You'll
also need [Homebrew](https://brew.sh/) to install additional software. Install the following brew packages:

    brew install python3 pipenv

You'll also need [git](https://git-scm.com/download/mac) to fetch and push source code from and to the GitHub
repository.

### Linux setup

Debian 9.3+ or Ubuntu 17.10+ is recommended. These instructions assume a Debian-based system.

Install required software with apt-get:

    apt-get install git postgresql-server python3 python3-dev libpq-dev

### Windows setup

[Download the installer](https://www.postgresql.org/download/windows/) and follow the instructions

### Create database 

Use `psql` to connect to PostgreSQL as an admin user and create the user and database for the project:

    CREATE USER scaffold WITH PASSWORD 'scaffold' CREATEDB;
    CREATE DATABASE scaffold WITH OWNER scaffold ENCODING 'unicode';

### Set up backend

The following commands all need to be done in the `root` directory.

Install Virtual Env  
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa 
sudo apt install python3.8-dev python3.8-venv libpq-dev build-essential libssl-dev zlib1g-dev

Create a new Python environment virtualenv and install required Python packages :

    python3.8 -m venv <env_name> 

Synchronize the required libs using pip tools

    source <venv_path>/bin/activate
    python -m pip install --upgrade pip
    pip install pip-tools
    pip-sync requirements/local.txt

Configure the application by copying `env-template` file to `.env` and modifying it as needed:

    cp project/project/settings/.env-template project/project/settings/.env

Initialize the database by running Django migrations:
    
    python project/manage.py migrate

Then, run server:

    python project/manage.py runserver

### Create superuser

    python project/manage.py createsuperuser

and visit http://127.0.0.1:8000/ to access the site.

