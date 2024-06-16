from jinja2 import Environment, FileSystemLoader

def generate_playbook(package_name, give_name_playbook):
    # Загрузка шаблона
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('disable_update.j2')

    # Заполнение шаблона данными
    output = template.render(package_name=package_name)

    # Сохранение сгенерированного плейбука в файл
    with open(f'{give_name_playbook}.yml', 'w') as file:
        file.write(output)

    print(f"Playbook '{give_name_playbook}.yml' generated successfully!")

if __name__ == "__main__":
    # Спросим у пользователя необходимые данные
    give_name_playbook = input('Assign a name to the playbook: ')
    packages_input = input("Enter the package to disable: ")

    generate_playbook(packages_input, give_name_playbook)