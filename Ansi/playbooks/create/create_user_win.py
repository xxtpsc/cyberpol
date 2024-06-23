import os
from jinja2 import Environment, FileSystemLoader

# Определяем директорию с шаблоном
template_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(template_dir))

# Загружаем шаблон
template = env.get_template('create_user_win.j2')

# Запрашиваем у пользователя данные
playbook_name = input("ВВедите имя плейбука: ")
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")
groups = input("Введите группы (через запятую): ").split(',')

# Данные для шаблона
data = {
    'username': username,
    'password': password,
    'groups': [group.strip() for group in groups]
}

# Рендерим шаблон с данными
output = template.render(data)

# Сохраняем результат в файл
with open(f'{playbook_name}.yml', 'w', encoding='utf-8') as f:
    f.write(output)

print("Playbook создан и сохранен")