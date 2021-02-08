#Образ YaMDb
![Cat](https://github.com/x038xx77/foodgram-project/workflows/foodgram/badge.svg)
## Краткое описание проекта

Эти инструкции позволят вам получить копию проекта foodgram — продуктовый помошник
на базе python, Django, PostgresQL, Gunicorn и запустить его на
вашем сервере. Примечания по развертыванию проекта в системе
см. В разделе развертывание.

### Необходимые компоненты
Docker-compose - подробнее о версиях можно прочесть в документации:
https://docs.docker.com/compose/compose-file/compose-versioning/

### Подготовка к запуску на сервере
Клонируйте репозиторий foodgram-project
```
https://github.com/x038xx77/foodgram-project.git
```

## Развертывание
На вашем сервере в папке /foodgram-project создайте файл .env и укажите ваши логины, пароли (все необходимые 
параметры указаны в setting.py настройки DATABASE ) для работы с базой данных PostgresQL.

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

Для заполнения базы, вашими данными, скопируйте в директорию foodgram-project файл вашей базы в формате json 
и выполните команду:
```     
docker-compose run web python manage.py python loaddata <your_basa_postgresql>.json
``` 
Подробнее https://postgrespro.ru/docs/postgresql/9.6/sql-load