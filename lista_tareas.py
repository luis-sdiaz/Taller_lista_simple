import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class TaskNode:
    def __init__(self, task):
        self.task = task
        self.next = None


class TaskList:
    def __init__(self):
        self.first_node = None
        self.last_node = None

    def add_task(self, task):
        new_node = TaskNode(task)

        if self.first_node is None:
            self.first_node = new_node
            self.last_node = new_node
        else:
            self.last_node.next = new_node
            self.last_node = new_node

    def get_tasks(self):
        if self.first_node is None:
            return "No hay tareas registradas."

        text = ""
        current_node = self.first_node
        number = 1

        while current_node is not None:
            text += f"Tarea {number}: {current_node.task}\n"
            current_node = current_node.next
            number += 1

        return text


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas Pendientes")
        self.root.geometry("760x520")
        self.root.configure(bg="#0f172a")

        self.task_list = TaskList()
        self.build_interface()

    def build_interface(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#e2e8f0")
        style.configure("Card.TFrame", background="#f8fafc")
        style.configure("Title.TLabel", background="#f8fafc", foreground="#0f172a",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Text.TLabel", background="#f8fafc", foreground="#334155",
                        font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)

        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding=20)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=680, height=430)

        card_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=25)
        card_frame.pack(fill="both", expand=True)

        ttk.Label(
            card_frame,
            text="Lista de Tareas Pendientes",
            style="Title.TLabel"
        ).pack(pady=(0, 10))

        ttk.Label(
            card_frame,
            text="Ingrese una tarea para almacenarla en la lista simple",
            style="Text.TLabel"
        ).pack(pady=(0, 18))

        self.task_entry = ttk.Entry(card_frame, font=("Segoe UI", 11), width=50)
        self.task_entry.pack(ipady=6, pady=(0, 18), fill="x")

        button_frame = ttk.Frame(card_frame, style="Card.TFrame")
        button_frame.pack(pady=(0, 18))

        ttk.Button(
            button_frame,
            text="Agregar tarea",
            command=self.add_task
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            button_frame,
            text="Mostrar tareas",
            command=self.show_tasks
        ).grid(row=0, column=1, padx=10)

        self.output = ScrolledText(
            card_frame,
            height=12,
            font=("Consolas", 11),
            bg="#ffffff",
            fg="#0f172a",
            relief="flat",
            bd=0
        )
        self.output.pack(fill="both", expand=True)

    def add_task(self):
        task = self.task_entry.get().strip()

        if task == "":
            messagebox.showwarning("Advertencia", "Por favor ingrese una tarea.")
            return

        self.task_list.add_task(task)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Tarea agregada correctamente.")
        self.task_entry.delete(0, tk.END)

    def show_tasks(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.task_list.get_tasks())


root = tk.Tk()
app = TaskManagerGUI(root)
root.mainloop()