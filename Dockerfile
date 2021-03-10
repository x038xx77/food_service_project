FROM python:3.8.5
LABEL author='plavrentev' version=1.1.1
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
