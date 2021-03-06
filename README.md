# Система классов для приложения "Автосалон"

## Автор

- [@SkonSfc44](https://github.com/SkonSfc44)

## Условия выполнения программы
### Технологический стек
#### ПО
1.	Устройство, стабильно работающее на поддерживаемых ОС Windows.
2.	Python версии 3.10 и выше.

#### Библиотеки
- [PyQt5] - Набор расширений графического фреймворка Qt для языка программирования Python.
- [sys] - Работа с аргументами командной строки (PyQt).
- [sqlalchemy] - Работа с БД при помощи языка SQL. Реализует ORM.
- [itertools] - Полезные итераторы.
- [os] - Работа с ОС.
- [openpyxl] - библиотека для работы исключительно с Excel-файлами.
- [json] - эффективное средство взаимодействия с JavaScript Object Notation.

## Сборка программы
Сборка подразумевает, что исходный код проекта уже присутствует в рабочей папке.
1. Создаем виртуальное окружение:
``` bash
python -m venv venv
```
2. Активируем виртуальное окружение
``` bash
venv\Scripts\activate
```
> ![venv_activate](https://user-images.githubusercontent.com/75139331/174867662-3e41c1ec-aaf1-4f8e-8ba5-6df1cd6d1c39.png)
3. Установим зависимости
``` bash
pip install -r requirements.txt
```
4. Запустим приложение
``` bash
python main.py
```

