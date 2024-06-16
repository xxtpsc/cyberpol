from ansible.playbook.play import Play
import os
import sys 
from ansible.module_utils.common.collections import ImmutableDict
from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.task_queue_manager import TaskQueueManager
import subprocess
# def run_externa_playbook(playbook_path, inventory_path, extra_vars=None):

#     runner_config = ansible_runner.RunnerConfig(
#         private_data_dir='.',  # Adjust if needed
#         playbook=playbook_path,
#         inventory=inventory_path,
#         extravars=extra_vars
#     )

#     runner = ansible_runner.Runner(config=runner_config)
#     results = runner.run()

#     if results.status_code == 0:
#         print("Playbook execution successful!")
#     else:
#         print("Playbook execution failed. See output for details.")

#     return results


def select_file_from_directory(directory):

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return None

    files = os.listdir(directory)

    if not files:
        print(f"Directory '{directory}' is empty.")
        return None

    print("Select CVE:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")


    while True: # Select file 
        try:
            file_index = int(input("Enter the number of the file you want to select: "))
            if 1 <= file_index <= len(files):
                selected_file = os.path.join(directory, files[file_index - 1])
                return selected_file
            else:
                print("Invalid file number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# def run_external_playbook(selected_file):
    
#     host_list = ['inventory.yml']

#     context.CLIARGS = ImmutableDict(connection='smart', module_path=['/to/mymodules', '/usr/share/ansible'], forks=10, become=True,
#                                     become_method='sudo', become_user=None, check=False, diff=False, verbosity=0)
    
#     sources = ','.join(host_list)

#     loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    
#     passwords = dict(vault_pass='secret')

#     # results_callback = ResultsCollectorJSONCallback()
 
#     inventory = InventoryManager(loader=loader, sources=sources)

#     variable_manager = VariableManager(loader=loader, inventory=inventory)


#     tqm = TaskQueueManager(
#         inventory=inventory,
#         variable_manager=variable_manager,
#         loader=loader,
#         passwords=passwords,
#         stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
#     )

#     play = Play().load(selected_file, variable_manager=variable_manager, loader=loader)

#     try:
#         result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
#     finally:
#         # we always need to cleanup child procs and the structures we use to communicate with them
#         tqm.cleanup()
#         if loader:
#             loader.cleanup_all_tmp_files()

#     # Remove ansible tmpdir
#     shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

#     print("UP ***********")
#     for host, result in results_callback.host_ok.items():
#         print('{0} >>> {1}'.format(host, result._result['stdout']))
        

#     print("FAILED *******")
#     for host, result in results_callback.host_failed.items():
#         print('{0} >>> {1}'.format(host, result._result['msg']))

#     print("DOWN *********")
#     for host, result in results_callback.host_unreachable.items():
#         print('{0} >>> {1}'.format(host, result._result['msg']))
def run_externa_playbook(selected_file):

    command = [f"ansible-playbook", selected_file, "-i", "inventory.yml"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode == 0:
        print("Ansible playbook executed successfully:")
        print(output.decode())  # Decode if necessary
    else:
        print("Ansible playbook execution failed:")
        print(error.decode())  # Decode if necessary

if __name__ == "__main__":
    current_file_path, *_ = sys.argv # Никто не пользуется, надо переделеать.
    current_directory = os.path.dirname(current_file_path)
    directory = f"{current_directory}/CVE_base"  # Replace with the actual directory path
    selected_file = select_file_from_directory(directory)

    if selected_file:
        print(f"Selected file: {selected_file}")
    else:
        print("No file selected.")

    run_externa_playbook(selected_file)
    
# tasks=[
#             #  dict(action=dict(module='shell', args='ls'), register='shell_out'),
#              #dict(name='Install Neofetch', action=dict(module='apt', args=dict(name='neofetch', state='present'))),
#              #dict(name='Ping Pong', action=dict(module='ping_pong',args=dict(hosts='all', register='ping_result'))),
#              #dict(name='Удалить Neofetch',action=dict(module='package',args=dict(name='neofetch',state='absent'))),
#             # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
#             # dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime'))),
#             dict(action=dict(module='package',name='{{ item }}',state='present'),with_items=['wget','make','build-essential'] ),
#         ]