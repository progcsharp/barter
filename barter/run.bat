@echo off
REM ==============================================
REM БАТНИК ДЛЯ ЗАПУСКА DJANGO НА WINDOWS
REM ==============================================

set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%venv
set MANAGE_PY=%PROJECT_DIR%manage.py
set DJANGO_SETTINGS_MODULE=barter.settings

REM Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен или не добавлен в PATH
    echo Установите Python 3.8+ и отметьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

REM Создание виртуального окружения
if not exist "%VENV_DIR%" (
    echo Создание виртуального окружения...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo ОШИБКА: Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
)

REM Активация venv
echo Активация виртуального окружения...
call "%VENV_DIR%\Scripts\activate.bat"

REM Обновление pip
echo Обновление pip...
python -m pip install --upgrade pip

REM Установка зависимостей
if exist "%PROJECT_DIR%requirements.txt" (
    echo Установка зависимостей...
    pip install -r "%PROJECT_DIR%requirements.txt"
) else (
    echo Файл requirements.txt не найден, устанавливаю только Django
    pip install django
)

REM Проверка manage.py
if not exist "%MANAGE_PY%" (
    echo ОШИБКА: Файл manage.py не найден!
    pause
    exit /b 1
)

REM Применение миграций
echo Применение миграций...
python "%MANAGE_PY%" migrate

REM Запуск сервера
echo Запуск сервера разработки...
echo Для остановки сервера нажмите CTRL+C
python "%MANAGE_PY%" runserver

pause