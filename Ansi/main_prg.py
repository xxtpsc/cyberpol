import os
import subprocess
import inquirer
import configparser
from tqdm import tqdm
import time

def list_playbooks(directory):
    """Returns a list of playbooks in the given directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []

def read_inventory(inventory_file):
    """Reads the inventory file and returns a dictionary of hosts by group."""
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(inventory_file)
    hosts = {}
    for section in config.sections():
        hosts[section] = list(config[section].keys())
    return hosts

def select_option(options, message, multiple=False):
    """Prompts the user to select an option from the list."""
    if multiple:
        question = [inquirer.Checkbox('options', message=message, choices=options)]
        answer = inquirer.prompt(question)
        return answer['options']
    else:
        question = [inquirer.List('option', message=message, choices=options)]
        answer = inquirer.prompt(question)
        return answer['option']

def run_ansible_playbook(playbook_path, host, inventory_file):
    """Runs the given Ansible playbook on the specified host with a progress bar."""
    try:
        command = ['ansible-playbook', '-i', inventory_file, '-l', host, playbook_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


        with tqdm(total=100, desc="Running Playbook", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed}') as pbar:
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    pbar.update(1)  


        stderr = process.stderr.read()
        if stderr:
            print("Errors:\n", stderr)
    except Exception as e:
        print(f"Failed to run playbook: {e}")

def run_python_script(script_path):
    """Runs the given Python script and prompts the user for input."""
    try:
        command = ['python3', script_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())

                if 'Enter' in output or 'enter' in output:
                    user_input = input("Введите данные: ")
                    process.stdin.write(user_input + '\n')
                    process.stdin.flush()
            if process.poll() is not None:
                break

        # Check for errors
        stderr = process.stderr.read()
        if stderr:
            print("Errors:\n", stderr)
    except Exception as e:
        print(f"Failed to run script: {e}")

def main():
    while True:
        os_types = ['Windows', 'Linux']
        os_type = select_option(os_types + ["Выход"], "Выберите тип операционной системы:")

        if os_type == "Выход":
            print("Выход из программы.")
            break

        categories = {
            'CVE': 'playbooks/cve',
            'Ошибки администрирования': 'playbooks/admin_errors',
            'Настройка ОС': 'playbooks/mitre',
            'Создание своего плейбука': 'playbooks/create'
        }

        category = select_option(list(categories.keys()) + ["Назад"], "Выберите категорию:")

        if category == "Назад":
            continue

        playbook_dir = categories[category]

        if category == 'Создание своего плейбука':
            while True:
                scripts = list_playbooks(playbook_dir)
                if not scripts:
                    print(f"No scripts found in the directory: {playbook_dir}")
                    break

                script = select_option(scripts + ["Назад"], "Выберите скрипт для запуска:")

                if script == "Назад":
                    break

                script_path = os.path.join(playbook_dir, script)
                print(f"Running script: {script_path}")
                run_python_script(script_path)

        else:
            while True:
                playbooks = list_playbooks(playbook_dir)
                if not playbooks:
                    print(f"No playbooks found in the directory: {playbook_dir}")
                    break

                selected_playbooks = select_option(playbooks + ["Назад"], "Выберите плейбуки для запуска:", multiple=True)

                if "Назад" in selected_playbooks:
                    break

                # Read inventory file and select host group
                inventory_file = "inventory.yml"  # Path to your inventory file
                hosts = read_inventory(inventory_file)

                if not hosts:
                    print("No hosts found in the inventory file.")
                    break

                group_prefix = "windows" if os_type == "Windows" else "linux"
                groups = [group for group in hosts.keys() if group.startswith(group_prefix)]

                if not groups:
                    print(f"No {os_type} groups found in the inventory file.")
                    break

                selected_group = select_option(groups + ["Назад"], "Выберите группу хостов:")
                
                if selected_group == "Назад":
                    break

                selected_host = select_option(hosts[selected_group] + ["Назад"], "Выберите хост:")
                
                if selected_host == "Назад":
                    break

                for playbook in selected_playbooks:
                    playbook_path = os.path.join(playbook_dir, playbook)
                    print(f"Running playbook: {playbook_path} on host: {selected_host}")
                    run_ansible_playbook(playbook_path, selected_host, inventory_file)

if __name__ == "__main__":
    main()
