FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
