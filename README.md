#Образ Foodgram
![Cat](https://github.com/x038xx77/foodgram-project/workflows/Foodgram/badge.svg)
## Краткое описание проекта Foodgram-prod Test

Эти инструкции позволят вам получить копию проекта foodgram — продуктовый помошник
http://llgall.ga
www.llgall.ga
178.154.194.78
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
- Создайте администратора сайта python manage.py createsuperuser
- Чтобы запустить проект на локальной машине - ./manage.py runserver
```
### Импорт (восстановление) с loaddata
Команда loaddata позволяет загрузить фикстуры (экспортированные с помощью dumpdata данные). Синтаксис так же крайне прост:
```
./manage.py loaddata db.json
```
Восстановление всей базы данных
Если вы попробуете сделать экспортировать данные на одном ПК, и восстановить на другом, то у вас ничего не выйдет. В процессе будет "выброшено" исключение IntegrityError. При этом на том же ПК, на котором был сделан экспорт - все будет импортироваться прекрасно. Чтобы избежать этой проблемы, из экспорта необходимо исключить таблицы contenttypes и auth.permissions:
```
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```
После этого импорт должен пройти без проблем:
```
./manage.py loaddata db.json
```
### Настройка почтового сервера yandex
https://django.fun/tutorials/nastrojka-pochty-v-django/
https://searchengines.guru/ru/forum/1037543

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
sudo docker-compose run web python manage.py migrate
```

Для создания суперпользователя в директории foodgram-project запустите команду:

```  
sudo docker-compose run web python manage.py createsuperuser
```
далее следуйте инструкции в терминале.


```

Для заполнения базы, вашими данными, скопируйте в директорию foodgram-project файл вашей базы в формате json 
и выполните команду:
```     
docker-compose run web python manage.py python loaddata <your_basa_postgresql>.json

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
