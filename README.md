# About

Dockerized shoutbomb signup form.

# Testing

Start a local debug SMTP server:

```
sudo aiosmtpd -n -d -l 0.0.0.0:25
```

Set environment variables:

```
export SMTP_HOST localhost
export SMTP_USER=test@localhost
export SHOUTBOMB_EMAIL=test@localhost
```

Start the application:

```
cd src
gunicorn --reload -w 4 -b 0.0.0.0:8888 main:app
```
