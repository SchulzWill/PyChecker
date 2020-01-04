
FROM python:3.7-alpine

WORKDIR /docker-flask

COPY . .

RUN pip install -r requirements.txt

CMD python app.py