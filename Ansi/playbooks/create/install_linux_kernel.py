from jinja2 import Environment, FileSystemLoader
import os 

def generate_playbook(url_to_source_code, package_source_name,output_file, package_source_only_name):
    # Установим директорию, где находится наш шаблон
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Загрузим шаблон
    template = env.get_template('install_linux_kernel.j2')
    
    # Сгенерируем содержимое плейбука
    playbook_content = template.render(
        url_to_source_code=url_to_source_code,
        package_source_name=package_source_name,
        package_source_only_name=package_source_only_name
    )
    
    # Запишем сгенерированный плейбук в файл
    with open(output_file, 'w') as f:
        f.write(playbook_content)
    print(f"Playbook '{output_file}' has been generated successfully.")

if __name__ == "__main__":
    # Спросим у пользователя необходимые данные
    give_name_playbook = input('Assign a name: ')
    url_to_source_code = input("Enter the URL to the source code: ").strip()
    package_source_name = url_to_source_code.rsplit('/', 1)[-1]
    package_source_only_name = package_source_name[:-7]

    #     # Имя выходного файла для плейбука
    output_file_name = f'{give_name_playbook}.yml'
        
        # Генерация плейбука
    generate_playbook( 
        url_to_source_code, 
        package_source_name,   
        output_file_name,
        package_source_only_name
    )
