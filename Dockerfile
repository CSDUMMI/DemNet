FROM python:3.7

COPY . /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt

ENV DATABASE demnet.db

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
