FROM python:3.7

COPY . /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt

ARG username=joris
ARG first_name=Joris
ARG last_name=Gutjahr
ARG password
ARG id

RUN python register.py $username $first_name $last_name $id $password

ENV DATABASE demnet.db


EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]
