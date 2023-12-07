Данный проект выполнен как тестоввое задание по django

для запуска проекта следует:
- скачать проект
- перейти в папку проекта и прописать следующие команды
- docker-compose up
- docker-compose run app python Test/manage.py migrate
- docker-compose run app python Test/manage.py createsuperuser

После этого необходимо зайти в админку джанги и добавить записи в таблицы бд Roles и UserStatus
В ролес необходимо добавить роль User, а в UserStatus - enabled

В проекте присутсвует свагер:
    localhost:8000/api/v1

Так же в проекте можно запусть тесты командой:
- docker-compose run app python Test/manage.py test MainApp.tests.MyTestApi

<h1>Описания существующих api(все находятся по адресу localhost:8000/api/{адрес api})</h1>

    
- registration/ --> апи принимает пост запрос с полями: email, name,surname,password
- login/ --> принимает пост запрос с полями: email, password. Возвращает json объект {token: "Token {сам токен}"}

<h3>Для следующих запросов требуется в headers пслыать поле Authorization со значение: "Token {сам токен}</h3>
- upload_file/ --> пост запрос с полями: file(сам файл), file_name
- get_file/ --> get запрос, можно без полей (тогда вернет json объект {files:[{file_name: "имя файла", file:"сам файл"}]})  либо с полем file_name(тогда вернет json {files:{file: "сам файл"})
- update_file/ --> put запрос, принимает поля file_name(обязательный) и 2 или 1 на выбор: file_name_new и file
- delete_file/ --> delete запрос, принимает поле file_name


- Так же впроекте существует фоновая задачка get_pokemon_stats которая подключается к внешней апи  и раз в 10 часов сохраняет в файл json статы покемона, запускается задача при старте приложения