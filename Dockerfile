FROM python:3

WORKDIR /usr/src/app

RUN pip install Django channels daphne psycopg2 djangorestframework
RUN pip install django-cors-headers

COPY ./runserver.sh /usr/bin/
RUN chmod +x /usr/bin/runserver.sh

EXPOSE 8080

CMD [ "/usr/bin/runserver.sh" ]
