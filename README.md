# Flask Boilerplate
Flask Boilerplate to quickly get started with production grade flask application

## Getting Started
### Prerequisites
* Python 3.8.10 or higher

### Project setup
```
# clone the repo
$ git clone https://github.com/AMuriuki/flask-boilerplate.git

# enter the project directory
$ cd flask-boilerplate
```

### Create & activate virtual environment
```
# included on all recent Python version
$ python3 -m venv venv

# activating the virtual env
$ . venv/bin/activate

# if using Microsoft Windows CMD
$ venv\Scripts\activate
```

### Initialize database
```
# migrate files to db
$ flask db upgrade
```

### Email Support
To enable email support:

1. [Signup for a trial/free Twilio SendGrid account](https://signup.sendgrid.com/)
2. Create an API key to authenticate access to SendGrid services
3. Update env vairables in .flaskenv.example and rename to .flaskenv

```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=<your-api-key>
MAIL_DEFAULT_SENDER=<your-sender-email-address>
```


