FROM python:3.7-alpine

RUN adduser -D flaskr_user

WORKDIR /home/flaskr_user

COPY requirements.txt requirements.txt
# Workaround the error during PyMySQL dependency 'cryptography' installation
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc
RUN pip install -r requirements.txt
COPY flaskr flaskr
COPY migrations migrations
COPY run.sh config.py .env ./
RUN chmod +x run.sh

ENV FLASK_APP=flaskr

RUN chown -R flaskr_user ./
USER flaskr_user

EXPOSE 5000
ENTRYPOINT ["./run.sh"]