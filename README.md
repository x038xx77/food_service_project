#Образ Foodgram
![Cat](https://github.com/x038xx77/foodgram-project/workflows/Foodgram/badge.svg)
## Краткое описание проекта

Эти инструкции позволят вам получить копию проекта foodgram — продуктовый помошник http://llgall.ga www.llgall.ga 130.193.43.183 на базе python, Django, PostgresQL, Gunicorn и запустить его на вашем сервере. Примечания по развертыванию проекта в системе см. В разделе развертывание.

### Необходимые компоненты
Docker-compose - подробнее о версиях можно прочесть в документации:
https://docs.docker.com/compose/compose-file/compose-versioning/


### Подготовка к запуску на локальном компьютере (Python 3, Linux)
Клонируйте репозиторий foodgram-project
```
https://github.com/x038xx77/foodgram-project.git
Создайте виртуальное окружение python3 -m venv venv
Активируйте виртуальное окружение source venv/bin/activate
Создайте файл .env командой touch .env и добавьте в него переменные окружения:
SECRET_KEY = #секретный ключ Django
DEBUG=1
Сгенерировать SECRET_KEY вы можете, например, по этой статье https://tech.serhatteker.com/post/2020-01/django-create-secret-key/

- Установите зависимости pip install -r requirements.txt
- Создайте все необходимые таблицы в базе данных - выполните команду ./manage.py migrate
- Импортируйте в базу теги и ингридиенты из файла tags.json и ingredients.json соответственно  - выполните команду python manage.py load_fixtures
- Создайте администратора сайта ./manage.py createsuperuser
- Чтобы запустить проект на локальной машине - ./manage.py runserver
```
### Подготовка к запуску на сервере
```
Для запуска проекта на удаленном сервере необходимо:

установить docker и docker-compose

скопировать на сервер файлы docker-compose.yaml, .env, config.nginx командами:
scp docker-compose.yaml  {user}@{server-ip}:
scp .env {user}@{server-ip}:
scp config.nginx {user}@{server-ip}:
в файле .env установить настройки DEBUG=0
Примечания по .env и развертыванию проекта в системе см. В разделе развертывание.
запустить на сервере контейнеры командой sudo docker-compose up
```
## Развертывание
На вашем сервере в папке /foodgram-project создайте файл .env и укажите ваши логины, пароли (все необходимые 
параметры указаны в setting.py настройки DATABASE ) для работы с базой данных PostgresQL.

```  
в файле .env должно быть
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=<название вашей базы данных>
POSTGRES_USER=<пользователь базы данных>
POSTGRES_PASSWORD=<пароль базы данных>
DB_HOST=db
DB_PORT=5432
```
```
после команды docker-compose up У вас развернется проект, запущенный с базой данных postgres.

Для создания базы данных в директории foodgram-project:
  
- запустите миграции docker-compose exec web python manage.py migrate
- Соберите статику командой sudo docker-compose exec web python manage.py collectstatic --no-input
```
Для создания суперпользователя в директории запустите команду:

```  
docker-compose run web python manage.py createsuperuser
```
далее следуйте инструкции в терминале.
Импортируйте в базу теги и ингридиенты из файла tags.json и ingredients.json соответственно  - выполните команду docker-compose run web python manage.py load_fixtures

Для заполнения базы, вашими данными, скопируйте в директорию foodgram-project файл вашей базы в формате json 
и выполните команду:
```     
docker-compose run web python manage.py python loaddata <your_basa_postgresql>.json
``` 
Подробнее https://postgrespro.ru/docs/postgresql/9.6/sql-load