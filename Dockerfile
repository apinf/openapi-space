FROM python:3-stretch

RUN pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 80
	
ENTRYPOINT ["uwsgi", "--ini", "/app/uwsgi.ini"]
