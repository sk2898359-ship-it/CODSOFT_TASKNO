from datetime import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = "todo_list.json"


class TodoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("720x560")
        self.root.minsize(620, 440)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview.Heading", font=("Helvetica", 10, "bold")
        )
        self.style.configure("Treeview", rowheight=26, font=("Helvetica", 10))

        self.tasks = self.load_tasks()

        self._create_widgets()
        self.refresh_table()

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, indent=4)
        except IOError as err:
            messagebox.showerror(
                "Save Error", f"Unable to save task file: {err}"
            )

    def _create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", height=50)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame,
            text="To-Do List Dashboard",
            font=("Helvetica", 16, "bold"),
            fg="#ffffff",
            bg="#1e293b",
            pady=12,
        )
        header_label.pack()

        input_frame = tk.Frame(self.root, pady=12, padx=16)
        input_frame.pack(fill=tk.X)

        self.task_entry = ttk.Entry(input_frame, font=("Helvetica", 11))
        self.task_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4
        )
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        add_btn = tk.Button(
            input_frame,
            text="+ Add Task",
            command=self.add_task,
            bg="#0284c7",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=14,
            pady=4,
            cursor="hand2",
        )
        add_btn.pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.root, padx=16)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "title", "status", "created_at")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("id", text="#")
        self.tree.heading("title", text="Task Description")
        self.tree.heading("status", text="Status")
        self.tree.heading("created_at", text="Created At")

        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("title", width=340, anchor=tk.W)
        self.tree.column("status", width=110, anchor=tk.CENTER)
        self.tree.column("created_at", width=140, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = tk.Frame(self.root, pady=14, padx=16)
        btn_frame.pack(fill=tk.X)

        toggle_btn = tk.Button(
            btn_frame,
            text="Toggle Status",
            command=self.toggle_task_status,
            bg="#16a34a",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=5,
            relief="flat",
            cursor="hand2",
        )
        toggle_btn.pack(side=tk.LEFT, padx=(0, 6))

        edit_btn = tk.Button(
            btn_frame,
            text="Edit",
            command=self.edit_task_description,
            bg="#eab308",
            fg="black",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=5,
            relief="flat",
            cursor="hand2",
        )
        edit_btn.pack(side=tk.LEFT, padx=6)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete",
            command=self.delete_task,
            bg="#dc2626",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=5,
            relief="flat",
            cursor="hand2",
        )
        delete_btn.pack(side=tk.LEFT, padx=6)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            command=self.clear_all_tasks,
            bg="#64748b",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=5,
            relief="flat",
            cursor="hand2",
        )
        clear_btn.pack(side=tk.RIGHT)

        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10,
            pady=4,
            font=("Helvetica", 9),
            bg="#f1f5f9",
            fg="#475569",
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        completed_count = 0
        for index, task in enumerate(self.tasks, start=1):
            status_text = "Completed" if task.get("completed") else "Pending"
            if task.get("completed"):
                completed_count += 1

            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    task.get("title", ""),
                    status_text,
                    task.get("created_at", "N/A"),
                ),
            )

        self.status_var.set(
            f"Total Tasks: {len(self.tasks)} | Completed: {completed_count} | Pending: {len(self.tasks) - completed_count}"
        )

    def _get_selected_index(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a task from the list first."
            )
            return None
        item_values = self.tree.item(selected[0], "values")
        return int(item_values[0]) - 1

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning(
                "Blank Field", "Task description cannot be empty."
            )
            return

        new_task = {
            "title": title,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_table()
        self.task_entry.delete(0, tk.END)

    def toggle_task_status(self):
        index = self._get_selected_index()
        if index is None:
            return

        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.refresh_table()

    def edit_task_description(self):
        index = self._get_selected_index()
        if index is None:
            return

        current_desc = self.tasks[index]["title"]
        updated_desc = simpledialog.askstring(
            "Edit Task", "Update task description:", initialvalue=current_desc
        )

        if updated_desc is not None:
            updated_desc = updated_desc.strip()
            if updated_desc:
                self.tasks[index]["title"] = updated_desc
                self.save_tasks()
                self.refresh_table()
            else:
                messagebox.showwarning(
                    "Blank Input", "Task description cannot be empty."
                )

    def delete_task(self):
        index = self._get_selected_index()
        if index is None:
            return

        task_title = self.tasks[index]["title"]
        confirm = messagebox.askyesno(
            "Confirm Deletion", f"Are you sure you want to delete '{task_title}'?"
        )
        if confirm:
            self.tasks.pop(index)
            self.save_tasks()
            self.refresh_table()

    def clear_all_tasks(self):
        if not self.tasks:
            messagebox.showinfo("List Empty", "There are no tasks to clear.")
            return

        confirm = messagebox.askyesno(
            "Clear Everything", "Delete all tasks permanently?"
        )
        if confirm:
            self.tasks.clear()
            self.save_tasks()
            self.refresh_table()


if __name__ == "__main__":
    app_window = tk.Tk()
    app = TodoApp(app_window)
    app_window.mainloop()