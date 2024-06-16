from jinja2 import Environment, FileSystemLoader

def generate_playbook(give_name_playbook,user_name,group_name):
    # Загрузка шаблона
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('addtogroup.j2')

    # Заполнение шаблона данными
    output = template.render( user_name=user_name, group_name=group_name )

    # Сохранение сгенерированного плейбука в файл
    with open(f'{give_name_playbook}.yml', 'w') as file:
        file.write(output)

    print("Playbook generated successfully!")


if __name__ == "__main__":
    # Спросим у пользователя необходимые данные
    give_name_playbook = input('Assign a name: ')
    user_name = input("Enter username to add group: ")
    group_name = input('Enter groupname for user: ')

    generate_playbook(give_name_playbook,user_name,group_name)