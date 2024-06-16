from jinja2 import Environment, FileSystemLoader
import os
#import inventory_generate_new 

def generate_playbook(packages, url_to_source_code, package_source_name, command_to_install, output_file):
    # Установим директорию, где находится наш шаблон
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Загрузим шаблон
    template = env.get_template('cve.j2')
    
    # Сгенерируем содержимое плейбука
    playbook_content = template.render(
        packages=packages,
        url_to_source_code=url_to_source_code,
        package_source_name=package_source_name,
        command_to_install=command_to_install,
        #path_to_start_program=path_to_start_program,
        src_path=src_path,
        start_service_command=start_service_command,
        dest_path=dest_path,
        package_source_only_name=package_source_only_name
    )
    
    # Запишем сгенерированный плейбук в файл
    with open(output_file, 'w') as f:
        f.write(playbook_content)
    print(f"Playbook '{output_file}' has been generated successfully.")

if __name__ == "__main__":
    # Спросим у пользователя необходимые данные
    give_name_playbook = input('Assign a name: ')
    packages_input = input("Enter the packages to install, separated by spaces: ")
    packages_to_install = [pkg.strip() for pkg in packages_input.split() if pkg.strip()]

    url_to_source_code = input("Enter the URL to the source code: ").strip()
    #package_source_name = input("Enter the name of the source code package: ").strip()
    package_source_name = url_to_source_code.rsplit('/', 1)[-1]
    package_source_only_name = package_source_name[:-7]
    command_to_install = input("Enter the command to compile and install the package: ").strip()
    src_path = input("Src path to cfg file: ").strip()
    dest_path = input("Dest path to cfg file: ").strip()
    start_service_command = input("Path to start service: ").strip()
    #path_to_start_program = input("Enter the path to start the program: ")
    #inventory_generate_new.PrintIpsInfo()


    if not packages_to_install or not url_to_source_code or not package_source_name or not command_to_install:
        print("All fields are required. Exiting.")
    else:
        # Имя выходного файла для плейбука
        output_file_name = f'{give_name_playbook}.yml'
        
        # Генерация плейбука
        generate_playbook(
            packages_to_install, 
            url_to_source_code, 
            package_source_name, 
            command_to_install,  
            output_file_name
        )
