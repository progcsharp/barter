# Инструкция по запуску Django-проекта и тестов

## 🔧 Запуск проекта

### Windows (через .bat файл)

1. Убедитесь, что установлен Python и pip.
2. Дважды кликните по файлу `start.bat` в корне проекта.
3. Скрипт создаст виртуальное окружение, установит зависимости, выполнит миграции и запустит сервер разработки.
4. После запуска проект будет доступен по адресу: `http://127.0.0.1:8000/`.

> **Примечание:** Убедитесь, что файл `start.bat` находится в корне проекта рядом с `manage.py`.

---

### Linux (установка с нуля)

Полная инструкция по развертыванию проекта на Linux.

#### 1. Установка необходимых пакетов

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

Проверьте версии Python и pip:

```bash
python3 --version
pip3 --version
```

#### 2. Клонирование проекта

```bash
git clone https://github.com/your-username/your-django-project.git
cd your-django-project
```

#### 3. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Выполнение миграций

```bash
python manage.py migrate
```

#### 6. Создание суперпользователя (по желанию)

```bash
python manage.py createsuperuser
```

Введите имя, email и пароль.

#### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере:

```
http://127.0.0.1:8000/
```

---

## 🧪 Запуск тестов

1. Активируйте виртуальное окружение проекта.
2. Выполните команду для запуска всех тестов:
   - `python manage.py test ads`
---
