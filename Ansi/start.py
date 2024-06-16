import os
import subprocess
import inquirer

def list_playbooks(directory):
    """Returns a list of playbooks in the given directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []

def run_ansible_playbook(playbook_path):
    """Runs the given Ansible playbook."""
    try:
        result = subprocess.run(['ansible-playbook', playbook_path], capture_output=True, text=True)
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"Failed to run playbook: {e}")

def select_option(options, message):
    """Prompts the user to select an option from the list."""
    question = [inquirer.List('option', message=message, choices=options)]
    answer = inquirer.prompt(question)
    return answer['option']

def main():
    categories = {
        'CVE': 'playbooks/cve',
        'Ошибки администрирования': 'playbooks/admin_errors',
        'Сценарии на основе MITRE': 'playbooks/mitre'
    }

    category = select_option(list(categories.keys()), "Выберите категорию плейбука:")
    playbook_dir = categories[category]

    playbooks = list_playbooks(playbook_dir)
    if not playbooks:
        print(f"No playbooks found in the directory: {playbook_dir}")
        return

    playbook = select_option(playbooks, "Выберите плейбук для запуска:")
    playbook_path = os.path.join(playbook_dir, playbook)
    
    print(f"Running playbook: {playbook_path}")
    run_ansible_playbook(playbook_path)

if __name__ == "__main__":
    main()
