#Образ Foodgram
![Cat](https://github.com/x038xx77/foodgram-project/workflows/Foodgram/badge.svg)
## Краткое описание проекта

Эти инструкции позволят вам получить копию проекта foodgram — продуктовый помошник
http://llgall.ga
www.llgall.ga
130.193.43.183
на базе python, Django, PostgresQL, Gunicorn и запустить его на
вашем сервере. Примечания по развертыванию проекта в системе
см. В разделе развертывание.

### Необходимые компоненты
Docker-compose - подробнее о версиях можно прочесть в документации:
https://docs.docker.com/compose/compose-file/compose-versioning/


### Подготовка к запуску на локальном компьютере (Python 3, Linux)
Клонируйте репозиторий foodgram-project
```
https://github.com/x038xx77/foodgram-project.git
```
```
Создайте виртуальное окружение python3 -m venv venv
Активируйте виртуальное окружение source venv/bin/activate
Создайте файл .env командой touch .env и добавьте в него переменные окружения:
SECRET_KEY = #секретный ключ Django
DEBUG=0
Сгенерировать SECRET_KEY вы можете, например, по этой статье https://tech.serhatteker.com/post/2020-01/django-create-secret-key/

- Установите зависимости pip install -r requirements.txt
- Создайте все необходимые таблицы в базе данных - выполните команду python manage.py migrate
- Импортируйте в базу теги и ингридиенты из файла tags.json и ingredients.json соответственно  - выполните команду python manage.py load_fixtures
- Создайте администратора сайта python manage.py createsuperuser
- Чтобы запустить проект на локальной машине - ./manage.py runserver
```

### Подготовка к запуску на удаленном сервере
Для запуска проекта на удаленном сервере необходимо:
- установите docker и docker-compose см. Необходимые компоненты
- в файле `.env` поменять настройки `DEBUG=0`
- скопировать на сервер файлы `docker-compose.yaml`, `.env`, `nginx.conf` командами:
```
scp /home/{user}/foodgram-project/ docker-compose.yaml  {user}@{server-ip}:
scp /home/{user}/foodgram-project/ .env {user}@{server-ip}:
scp /home/{user}/foodgram-project/ nginx.conf {user}@{server-ip}:
```
- запустить на сервере контейнеры командой `sudo docker-compose up`

## Развертывание
На вашем сервере в папке /foodgram-project при необходимости отредактируйте ранее выше загруженный файл .env проверьте DEBUG=0 и укажите ваши логины, пароли (все необходимые 
параметры указаны в setting.py настройки DATABASE ) для работы с базой данных PostgresQL ниже:

```  
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=<название вашей базы данных>
POSTGRES_USER=<пользователь базы данных>
POSTGRES_PASSWORD=<пароль базы данных>
DB_HOST=db
DB_PORT=5432
```
В директории /foodgram-project запустите c правами root docker-compose командой 
docker-compose pull && docker-compose down && docker-compose up
. У вас развернется проект, запущенный с базой данных postgres.

После, для создания базы данных в директории foodgram-project запустите команду:

```  
docker-compose run web python manage.py migrate
```

Для создания суперпользователя в директории foodgram-project запустите команду:

```  
docker-compose run web python manage.py createsuperuser
```
далее следуйте инструкции в терминале.

- Импортируйте в базу теги и ингридиенты выполнив команду docker-compose run web python manage.py load_fixtures

```

Для заполнения базы, вашими данными, скопируйте в директорию foodgram-project файл вашей базы в формате json 
и выполните команду:
```     
docker-compose run web python manage.py python loaddata <your_basa_postgresql>.json
``` 
Подробнее https://postgrespro.ru/docs/postgresql/9.6/sql-load

## Authors

* **Pavel Lavrentev** - *Initial work* - [Lavrentev](https://github.com/x038xx77)

# License Templates

These files are designed to be used by `lice`, a command-line license generator
for software projects. 

## Format/Structure

The template uses variables as placeholders to substitute values specified by
`lice`.

* `{{ 2021 }}`: the year of the software's copyright.
* `{{ x038xx77 }}`: the name of the organization or individual who holds
the copyright to the software.
* `{{ foodgram-progect }}`: the name of the software project.

## Copyright

All licenses in this repository are copyrighted by their respective authors.
Everything else is released under CC0. See `LICENSE` for details.