from jinja2 import Environment, FileSystemLoader
import os

def get_user_input():
    custom_users = {}
    custom_groups = {}
    command_aliases = {}

    assign_name = input('Name sudoers file: ')
    print("Введите информацию о пользователях:")
    while True:
        user = input("Имя пользователя (или 'done' для завершения): ")
        if user.lower() == 'done':
            break
        privileges = input(f"Привилегии для {user}: ")
        custom_users[user] = privileges

    print("\nВведите информацию о группах:")
    while True:
        group = input("Имя группы (или 'done' для завершения): ")
        if group.lower() == 'done':
            break
        privileges = input(f"Привилегии для группы {group}: ")
        custom_groups[group] = privileges

    print("\nВведите алиасы команд:")
    while True:
        alias = input("Имя алиаса команды (или 'done' для завершения): ")
        if alias.lower() == 'done':
            break
        commands = input(f"Команды для алиаса {alias} (через запятую): ")
        command_aliases[alias] = commands

    return assign_name, custom_users, custom_groups, command_aliases

def generate_sudoers(assign_name, custom_users, custom_groups, command_aliases):
    # Определите путь к шаблону
    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = 'sudoers.j2'

    # Создайте окружение Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # Сгенерируйте sudoers файл
    sudoers_content = template.render(custom_users=custom_users, custom_groups=custom_groups, command_aliases=command_aliases)

    # Запишите сгенерированный контент в файл sudoers
    with open(f'{assign_name}', 'w') as sudoers_file:
        sudoers_file.write(sudoers_content)

    print(f"sudoers файл успешно создан и сохранен как '{assign_name}'")

if __name__ == "__main__":
    assign_name, custom_users, custom_groups, command_aliases = get_user_input()
    generate_sudoers(assign_name, custom_users, custom_groups, command_aliases)
