# QRkot_spreadseets
# Описание проекта
Благотворительный проект для помощи котикам(им ничо не угрожает, да и нужна ли им помощь непонятно).
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

# Технологии
- Python 3.9.10
- FastApi 0.78.0
- Alembic 1.7.7
- Google Cloud Platform
- Google Sheets Api
- Googla Drive Api

# Авторы
- YandexPracticum
- BlopFlop(ArturYoungBlood)

# Документация

Генерируется автоматически [Redoc](http://127.0.0.1:8000/redoc)

# Описание .env файла

- QRK_APP_TITLE - Название приложения; 
- QRK_DESCRIPTION - Описание приложения; 
- QRK_DATABASE_URL - Урл базы данных; 
- QRK_SECRET - Секретный ключ; 
- QRK_FIRST_SUPERUSER_EMAIL - Почта суперюзера; 
- QRK_FIRST_SUPERUSER_PASSWORD - Пароль суперюзера;

- QRK_TYPE - Поле type из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_PROJECT_ID - Поле project id из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_PRIVATE_KEY_ID - Поле private key id из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_PRIVATE_KEY - Поле private key из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_CLIENT_EMAIL - Поле client email из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_CLIENT_ID - Поле client id из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_AUTH_URI - Поле auth url из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_TOKEN_URI - Поле token url из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_AUTH_PROVIDER_X509_CERT_URL - Поле auth provider x509 cert url из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_CLIENT_X509_CERT_URL - Поле client x509 cert url из сгенерированного файла creeds.json из гугл сервисов; 
- QRK_EMAIL - Почта пользователя которому будет открыт доступ на гугл таблицы.

# Инструкция:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:BlopFlop/QRkot_spreadseets.git
```

```
cd QRkot_spreadseets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
или для пользователей Windows

```
source env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Применение миграции:
```
alembic upgrade head
```

Запустить проект (* - создание суперпользователя происходит автоматически):

```
uvicorn app.main:app -reload
```