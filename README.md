[![Foodgram workflow](https://github.com/GideonRavenor1/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](https://github.com/GideonRavenor1/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
# Foodgram - Продуктовый помощник

Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей,
подписываться на интересных авторов, добавлять лучшие рецепты в избранное,
а также создавать список покупок и загружать его в pdf формате.

>Технологии, используемые на проекте:

>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
>>4. PostgresSQL ![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
>>5. pgAdmin ![pgAdmin](https://img.shields.io/badge/PG-pgAdmin-blue?style=flat-square&logo=pgAdmin)
>>6. Nginx ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat-square&logo=nginx&logoColor=white)
>>7. Swagger ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=flat-square&logo=swagger&logoColor=white)
>>8. Celery ![Celery](https://img.shields.io/badge/-Celery-%2300C7B7?style=flat-square&logo=Celery)
>>9. Flower ![Flower](https://img.shields.io/badge/F-Flower-green?style=flat-square&logo=Celery)
>>10. Redis ![Redis](https://img.shields.io/badge/-Redis-FCA121?style=flat-square&logo=Redis)
>>11. React ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
# Как запустить проект:

В папку ***infra*** расположить .env файл со следующими параметрами:
1. DOCKER_USERNAME=***Логин от docker hub***
2. IMAGE_TAG=***Версия образов***
3. POSTGRES_USER=***ВАШЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ОТ БД***
4. POSTGRES_PASSWORD=***ВАШ ПАРОЛЬ ОТ БД***
5. POSTGRES_DB=***ИМЯ БАЗЫ ДАННЫХ***
6. POSTGRES_HOST=***ХОСТ, УКАЗАТЬ СЛУЖБУ БД,В НАШЕМ СЛУЧАЕ postgresql_db***
7. PGADMIN_DEFAULT_EMAIL=***ВАША ПОЧТА***
8. PGADMIN_DEFAULT_PASSWORD=***ВАШ ПАРОЛЬ***
9. SPOONACULAR_API_KEY=***Ключ от апи для автоматической загрузки рецептов***https://spoonacular.com/food-api/pricing

Скачать docker: 
1. Для [windows](https://docs.docker.com/desktop/windows/install/)
2. Для [macOS](https://docs.docker.com/desktop/mac/install/)
3. Для дистрибутивов [Linux](https://docs.docker.com/desktop/linux/#uninstall)

После установки проверьте конфигурацию переменных окружений 
командой:
```
docker-compose config
```
Если всё успешно, все переменные на местах, запустить командой:
```
docker-compose -f docker-compose.dev.yml up --build -d
```

Что бы создать суперпользователя, 
необходимо войти в контейнер командой:
```
docker exec -it drf_backend bash
```
Применить миграции:
```
python manage.py migrate
```
Собрать статику:
```
python manage.py collectstatic
```
После ввести команду:
```
python manage.py createsuperuser
```
и следовать дальнейшим инструкциям.

Для выхода введите:
```
exit
```
Следующие сервисы будут доступны по адресам:

## API
1. http://localhost:8000/api/swagger/
2. http://localhost:8000/api/redoc/

## UI панель базы данный PostgeSQL
1. http://localhost:5050


## Развернутый экземпляр приложения доступен по адресу:
## API
1. http://51.250.110.97/api/swagger/
2. http://51.250.110.97/api/redoc/


## UI панель базы данный PostgeSQL
1. http://51.250.110.97/api/pgadmin4/


## UI панель celery
1. http://51.250.110.97/api/flower/

## Фронт
1. http://51.250.110.97/
