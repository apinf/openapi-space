FROM python:3-stretch

RUN pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
COPY requirements/ /app/requirements
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 80
	
ENTRYPOINT ["uwsgi", "--ini", "/app/uwsgi.ini"]
