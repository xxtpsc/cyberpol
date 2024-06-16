from jinja2 import Environment, FileSystemLoader

def generate_playbook(name_package, src_path, dest_path, name_service):
    # Загрузка шаблона
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('distrget.j2')

    # Заполнение шаблона данными
    output = template.render(name_package=name_package, src_path=src_path, dest_path=dest_path, name_service=name_service)

    # Сохранение сгенерированного плейбука в файл
    with open('installsambaftp.yml', 'w') as file:
        file.write(output)

    print("Playbook generated successfully!")

# Пример использования
name_package = 'samba'
src_path = '/home/kali/Ansi/playbooks/cfgs/smb.cfg'
dest_path = '/etc/samba/smb.conf'
name_service = 'smbd'

generate_playbook(name_package, src_path, dest_path, name_service)
