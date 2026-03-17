import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class TaskNode:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.status = "Pending"
        self.next = None


class TaskList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def add_first(self, title, description):
        node = TaskNode(title, description)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node

    def add_last(self, title, description):
        node = TaskNode(title, description)
        if self.is_empty():
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def search(self, title):
        current = self.head
        while current is not None:
            if current.title.lower() == title.lower():
                return current
            current = current.next
        return None

    def mark_completed(self, title):
        task = self.search(title)
        if task is not None:
            task.status = "Completed"
            return True
        return False

    def count(self):
        total = 0
        current = self.head
        while current is not None:
            total = total + 1
            current = current.next
        return total

    def show_tasks(self, status=None):
        if self.is_empty():
            return "The task list is empty."

        text = ""
        current = self.head
        number = 1

        while current is not None:
            if status is None or current.status == status:
                text += f"Task {number}\n"
                text += f"Title: {current.title}\n"
                text += f"Description: {current.description}\n"
                text += f"Status: {current.status}\n"
                text += "-" * 35 + "\n"
            current = current.next
            number = number + 1

        return text if text else "No tasks found."

    def first_task(self):
        return self.head

    def last_task(self):
        return self.tail


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x600")
        self.root.config(bg="#0f172a")
        self.tasks = TaskList()
        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#e2e8f0")
        style.configure("TLabel", background="#e2e8f0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#1e293b")

        card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        card.place(relx=0.5, rely=0.5, anchor="center", width=820, height=540)

        ttk.Label(card, text="Task Manager with Singly Linked List", style="Title.TLabel").pack(pady=(0, 20))

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x", pady=5)

        ttk.Label(form, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(form, width=35)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Description").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(form, width=35)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        buttons = ttk.Frame(card, style="Card.TFrame")
        buttons.pack(pady=15)

        actions = [
            ("Add First", self.add_first),
            ("Add Last", self.add_last),
            ("Show All", self.show_all),
            ("Search", self.search_task),
            ("Mark Completed", self.complete_task),
            ("Count", self.count_tasks),
            ("Pending", lambda: self.show_by_status("Pending")),
            ("Completed", lambda: self.show_by_status("Completed")),
            ("First Task", self.show_first),
            ("Last Task", self.show_last)
        ]

        row = col = 0
        for text, command in actions:
            ttk.Button(buttons, text=text, command=command).grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            col = col + 1
            if col == 5:
                col = 0
                row = row + 1

        self.output = ScrolledText(card, font=("Consolas", 10), height=16, bg="#f8fafc", fg="#0f172a")
        self.output.pack(fill="both", expand=True, pady=10)

    def data(self):
        return self.title_entry.get().strip(), self.description_entry.get().strip()

    def clear(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def write(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def validate(self, need_description=True):
        title, description = self.data()
        if title == "" or (need_description and description == ""):
            messagebox.showwarning("Warning", "Please complete the required fields.")
            return None, None
        return title, description

    def add_first(self):
        title, description = self.validate()
        if title:
            self.tasks.add_first(title, description)
            self.write("Task added at the beginning.")
            self.clear()

    def add_last(self):
        title, description = self.validate()
        if title:
            self.tasks.add_last(title, description)
            self.write("Task added at the end.")
            self.clear()

    def show_all(self):
        self.write(self.tasks.show_tasks())

    def search_task(self):
        title, _ = self.validate(False)
        if title:
            task = self.tasks.search(title)
            if task is None:
                self.write("Task not found.")
            else:
                self.write(
                    f"Task found\nTitle: {task.title}\nDescription: {task.description}\nStatus: {task.status}"
                )

    def complete_task(self):
        title, _ = self.validate(False)
        if title:
            self.write("Task marked as completed." if self.tasks.mark_completed(title) else "Task not found.")

    def count_tasks(self):
        self.write(f"Total tasks: {self.tasks.count()}")

    def show_by_status(self, status):
        self.write(self.tasks.show_tasks(status))

    def show_first(self):
        task = self.tasks.first_task()
        self.write("The task list is empty." if task is None else
                   f"First task\nTitle: {task.title}\nDescription: {task.description}\nStatus: {task.status}")

    def show_last(self):
        task = self.tasks.last_task()
        self.write("The task list is empty." if task is None else
                   f"Last task\nTitle: {task.title}\nDescription: {task.description}\nStatus: {task.status}")


root = tk.Tk()
app = TaskManagerGUI(root)
root.mainloop()