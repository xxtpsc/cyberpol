import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, SINGLE, END

def list_playbooks(directory):
    """Returns a list of playbooks in the given directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []

def run_ansible_playbook(playbook_path, host):
    """Runs the given Ansible playbook on the specified host."""
    try:
        result = subprocess.run(['ansible-playbook', playbook_path, '-i', host], capture_output=True, text=True)
        messagebox.showinfo("Playbook Output", f"Output:\n{result.stdout}")
        if result.stderr:
            messagebox.showwarning("Playbook Errors", f"Errors:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"Failed to run playbook: {e}")

def select_category():
    category = category_var.get()
    if category == "Выход":
        root.quit()
    else:
        playbook_dir = categories[category]
        playbooks = list_playbooks(playbook_dir)
        if not playbooks:
            messagebox.showinfo("No Playbooks", f"No playbooks found in the directory: {playbook_dir}")
            return
        update_playbook_list(playbooks)

def update_playbook_list(playbooks):
    playbook_listbox.delete(0, END)
    for playbook in playbooks:
        playbook_listbox.insert(END, playbook)
    playbook_listbox.insert(END, "Назад")

def on_playbook_select(event):
    selected = playbook_listbox.get(playbook_listbox.curselection())
    if selected == "Назад":
        category_var.set("")
        playbook_listbox.delete(0, END)
    else:
        playbook_dir = categories[category_var.get()]
        playbook_path = os.path.join(playbook_dir, selected)
        host = host_var.get()
        if not host:
            messagebox.showwarning("No Host Selected", "Please select a host before running the playbook.")
            return
        run_ansible_playbook(playbook_path, host)

root = tk.Tk()
root.title("Ansible Playbook Runner")

categories = {
    'CVE': 'playbooks/cve',
    'Ошибки администрирования': 'playbooks/admin_errors',
    'Сценарии на основе MITRE': 'playbooks/mitre',
    'Создание своего плейбука': 'playbooks/create'
}

category_var = tk.StringVar()
category_label = tk.Label(root, text="Выберите категорию:")
category_label.pack()

category_menu = tk.OptionMenu(root, category_var, *list(categories.keys()) + ["Выход"], command=lambda _: select_category())
category_menu.pack()

playbook_listbox = Listbox(root, selectmode=SINGLE)
playbook_listbox.pack()
playbook_listbox.bind('<<ListboxSelect>>', on_playbook_select)

host_var = tk.StringVar()
host_label = tk.Label(root, text="Введите хост (inventory file или IP):")
host_label.pack()

host_entry = tk.Entry(root, textvariable=host_var)
host_entry.pack()

root.mainloop()
