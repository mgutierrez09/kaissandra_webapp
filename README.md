# Kaissandra Webapp :ok_hand:

Server-side for Kaissandra App implemented in python.

## Setup

### Local Setup

 First install packages in requirements.txt with `$pip install -r requirements.txt`. Visual cpp is required too and can be 
downloaded from ___.

Set up DB with `$flask db upgrage`.
 
WARNING! If you are using sqlite, it might give an error due to incompatibilities with posgresql. In this case, back up
the migration folder and create a new db environment by running 

```
$ flask db init
$ flask db migrate -m "message"
$ flask db upgrade
```

Create new username and password by getting into the terminal with $flask shell, and then run:

```python
from app import db
from app.tables_test import User
u = User(username=<username>,  isadmin=True)
u.set_password(<password>)
u.check_password(<password>)
db.session.add(u)
db.session.commit()
```
### Remote Setup with API Calls

1. Create new user remotely:

`http POST http://localhost:5000/api/users/<admin id>/signup username=<username> password=<password> email=<email> "Authorization:Bearer <token admin>"`

2. Get token:

`http --auth <username>:<password> POST http://localhost:5000/api/tokens`

3. Add funds:

`http POST http://localhost:5000/api/users/<user id>/funds funds=<funds> "Authorization:Bearer <token admin>"`

4. Add trader

`http POST http://localhost:5000/api/users/<user id>/traders tradername=<trader name> budget=<budget> poslots=<volune> leverage=<leverage> "Authorization:Bearer <token user>"`

## How to use

Some usuful commands:

- Run debugging mail server:

`$ python -m smtpd -n -c DebuggingServer localhost:8025`

- Post token:

`$ http --auth <username>:<password> POST http://localhost:5000/api/tokens`

- request with token bearer:

`http GET http://localhost:5000/api/users/1 "Authorization:Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"` 

- update open sessions parameters

`http PUT http://localhost:5000/api/traders/sessions/change_params lots=0.05 stoploss=30 "Authorization:Bearer tVGT8/M8ybkJsmUqRQ1z+B2sMYJDt6TV"`

- Enquire updated parameters from session

`http GET http://localhost:5000/api/traders/sessions/269/get_params "Authorization:Bearer tVGT8/M8ybkJsmUqRQ1z+B2sMYJDt6TV"`

- Close sessions

`http PUT http://localhost:5000/api/traders/sessions/close "Authorization:Bearer tVGT8/M8ybkJsmUqRQ1z+B2sMYJDt6TV"`

- Change trading parameters:

`$ http PUT https://kaissandra-webapp.herokuapp.com/api/traders/sessions/change_params stoploss=<value> lots=<value> "Authorization:Bearer <token>"`
 
## Author

Miguel A. Gutierrez-Estevez 

https://www.linkedin.com/in/magutierrezestevez/