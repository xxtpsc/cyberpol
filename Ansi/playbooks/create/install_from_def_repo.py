from jinja2 import Environment, FileSystemLoader

def generate_playbook(packages, give_name_playbook):
    # Загрузка шаблона
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('install_from_def_repo.j2')

    # Заполнение шаблона данными
    output = template.render(packages=packages)

    # Сохранение сгенерированного плейбука в файл
    with open(f'{give_name_playbook}.yml', 'w') as file:
        file.write(output)

    print(f"Playbook '{give_name_playbook}.yml' generated successfully!")

if __name__ == "__main__":
    # Спросим у пользователя необходимые данные
    give_name_playbook = input('Assign a name to the playbook: ')
    packages_input = input("Enter the packages to install, separated by spaces: ")
    packages_to_install = [pkg.strip() for pkg in packages_input.split() if pkg.strip()]

    generate_playbook(packages_to_install, give_name_playbook)
