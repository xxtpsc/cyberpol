from jinja2 import Environment, FileSystemLoader

def generate_playbook(path_to_share, src_to_cfg, path_to_cfg, src_to_script, path_to_share_script):
    # Загрузка шаблона
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('sambaOPEN.j2')

    # Заполнение шаблона данными
    output = template.render(path_to_share=path_to_share, src_to_cfg=src_to_cfg, path_to_cfg=path_to_cfg, src_to_script=src_to_script, path_to_share_script=path_to_share_script)

    # Сохранение сгенерированного плейбука в файл
    with open(f'{give_name_playbook}.yml', 'w') as file:
        file.write(output)

    print("Playbook generated successfully!")

# Пример использования
# give_name_playbook = input('Assign a name: ')
# path_to_share = input("Path to share:" )
# src_to_cfg = input('src path to cfg: ')
# path_to_cfg = input('dest path to cfg: ')
# src_to_script = input('src to script: ')
# path_to_share_scrpit = input('dest to script: ') 

give_name_playbook = 'openSMB'
path_to_share = '/srv/samba/share'
src_to_cfg = '/home/kali/Ansi/playbooks/cfgs/opensmb.conf'
path_to_cfg = '/etc/samba/smb.conf'
src_to_script = '/home/kali/Ansi/playbooks/scripts/opensmb.sh'
path_to_share_scrpit = "/srv/samba/share/opensmb.sh"




generate_playbook(path_to_share, src_to_cfg, path_to_cfg, src_to_script, path_to_share_scrpit)
