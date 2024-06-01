FROM python:3
MAINTAINER Chelsea Kendrick "ckendri5@uoregon.edu"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]