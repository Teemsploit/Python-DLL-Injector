import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append((proc.info['pid'], proc.info['name']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

class ProcessSelector(tk.Toplevel):
    def __init__(self, parent, processes):
        super().__init__(parent)
        self.title('Select a Process')
        self.geometry('300x300')
        self.resizable(width=False, height=False)
        self.parent = parent

        self.process_listbox = tk.Listbox(self)
        for pid, name in processes:
            self.process_listbox.insert(tk.END, f'{pid}: {name}')

        select_button = ttk.Button(self, text='Select', command=self.select_process)

        self.process_listbox.pack(fill=tk.BOTH, expand=True)
        select_button.pack(pady=5)

    def select_process(self):
        selection = self.process_listbox.get(self.process_listbox.curselection())
        pid = int(selection.split(':')[0])
        name = selection.split(':')[1].strip()
        self.parent.selected_process = (pid, name)
        self.destroy()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('DLL Injector')
        self.geometry('400x200')
        self.resizable(width=False, height=False)

        self.selected_process = None
        self.dll_path = tk.StringVar()

        process_label = ttk.Label(self, text='Select a process:')
        self.process_button = ttk.Button(self, text='...', command=self.select_process)
        dll_label = ttk.Label(self, text='DLL path:')
        dll_entry = ttk.Entry(self, textvariable=self.dll_path)
        inject_button = ttk.Button(self, text='Inject', command=self.inject_dll)

        process_label.pack(pady=5)
        self.process_button.pack(pady=5)
        dll_label.pack(pady=5)
        dll_entry.pack(fill=tk.X, padx=5, pady=5)
        inject_button.pack(pady=10)

    def select_process(self):
        processes = get_processes()
        selector = ProcessSelector(self, processes)
        self.wait_window(selector)
        if self.selected_process is not None:
            self.process_button.configure(text=f'{self.selected_process[0]}: {self.selected_process[1]}')

    def inject_dll(self):
        if self.selected_process is None:
            tk.messagebox.showerror('Error', 'Please select a process.')
            return
        if not self.dll_path.get():
            tk.messagebox.showerror('Error', 'Please enter a DLL path.')
            return
        # will be implimented soon
        print('injected')

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
