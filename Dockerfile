FROM python:3.8.5
LABEL author='plavrentev' version=1.1.1
WORKDIR /code
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
