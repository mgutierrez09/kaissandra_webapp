# Kaissandra Webapp

* This is the readme.

## How to use

### Setup
 First install packages in requirements.txt with $pip install -r requirements.txt. Visual cpp is required too and can be 
downloaded from ___.

Set up DB with $flask db upgrage. 
WARNING! If you are using sqlite, it might give an error due to incompatibilities with posgresql. In this case, back up
the migration folder and create a new db environment by running 
$flask db init
$flask db migrate -m "<message>"
$flask db upgrade

Create new username and password by getting into the terminal with $flask shell, and the run:

> from app import db

> from app.tables_test import User

> u = User(username=<username>,  isadmin=True)

> u.set_password(<password>)

> u.check_password(<password>)

> db.session.add(u)

> db.session.commit()
 
## Authors

[Miguel A. Gutierrez-Estevez] (https://www.linkedin.com/in/magutierrezestevez/)