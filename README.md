# Air Food API

Этот проект представляет собой RESTful API для получения информации о меню авиакомпаний на основе различных параметров, таких как длительность полета, класс обслуживания и выбранная авиакомпания.

## Установка

1. Клонируйте данный репозиторий на свой локальный компьютер:

```
git clone https://github.com/12mativ/air_food.git
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv venv
source venv/bin/activate  

# Для Windows используйте 
'venv\Scripts\activate'
```

3. Установите зависимости проекта:

```
pip install -r .\requirements.txt
```

4. Укажите параметры для подключения к базе данных в файле `.env`. Пример `.env`:

```
DB_URL=db_url
```

5. Запустите приложение:

```
python .\api.py
```

После этого ваше приложение будет доступно по адресу http://localhost:8000/.

## Использование

Вы можете использовать это API для получения меню авиакомпаний на основе различных параметров. Вот некоторые из доступных эндпоинтов:

- `POST /menu`: Получить меню на основе параметров, переданных в теле запроса.
- `GET /airlines`: Получить список доступных авиакомпаний.

Для более подробных инструкций по использованию API, смотрите Swagger UI, который доступен по URL `/`. 

## Технологии

Проект создан с использованием следующих технологий:

- Python 3
- Flask: Фреймворк для создания веб-приложений на Python.
- Flask-RESTX: Расширение для Flask, упрощающее создание RESTful API.
- PostgreSQL: Система управления базами данных.

## Лицензия

Этот проект лицензируется в соответствии с [Лицензией MIT](LICENSE).

Для полной информации о проекте и его использовании обратитесь к [документации API](http://localhost:8000/).