import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

FILE_NAME = "contacts.json"


class ContactBook:

    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        # Load existing data
        self.contacts = self.load_contacts()
        self.current_selected_index = None

        # Build interface
        self.setup_ui()
        self.display_contacts(self.contacts)

    def load_contacts(self):
        if not os.path.exists(FILE_NAME):
            return []
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save_contacts(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Contact Management System",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        title_label.pack(fill=tk.X)

        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Side - List & Search
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            search_frame, text="Search:", font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5
        )
        self.search_entry.bind("<KeyRelease>", self.search_contact)

        # Treeview to display contacts
        self.tree = ttk.Treeview(
            left_frame,
            columns=("Name", "Phone"),
            show="headings",
            height=14,
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.column("Name", width=160)
        self.tree.column("Phone", width=130)

        scrollbar = ttk.Scrollbar(
            left_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.select_contact)

        # Right Side - Form Fields
        right_frame = tk.LabelFrame(
            main_frame, text=" Contact Details ", font=("Arial", 10, "bold"), padx=10, pady=10
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(right_frame, text="Name:", anchor="w").pack(fill=tk.X)
        self.name_entry = ttk.Entry(right_frame, width=32)
        self.name_entry.pack(fill=tk.X, pady=(0, 8))

        tk.Label(right_frame, text="Phone Number:", anchor="w").pack(fill=tk.X)
        self.phone_entry = ttk.Entry(right_frame, width=32)
        self.phone_entry.pack(fill=tk.X, pady=(0, 8))

        tk.Label(right_frame, text="Email:", anchor="w").pack(fill=tk.X)
        self.email_entry = ttk.Entry(right_frame, width=32)
        self.email_entry.pack(fill=tk.X, pady=(0, 8))

        tk.Label(right_frame, text="Address:", anchor="w").pack(fill=tk.X)
        self.address_entry = tk.Text(right_frame, width=32, height=4, font=("Arial", 9))
        self.address_entry.pack(fill=tk.X, pady=(0, 12))

        # Action Buttons
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(fill=tk.X)

        tk.Button(
            btn_frame,
            text="Add",
            bg="#27ae60",
            fg="white",
            width=10,
            command=self.add_contact,
        ).grid(row=0, column=0, padx=2, pady=3)
        tk.Button(
            btn_frame,
            text="Update",
            bg="#2980b9",
            fg="white",
            width=10,
            command=self.update_contact,
        ).grid(row=0, column=1, padx=2, pady=3)
        tk.Button(
            btn_frame,
            text="Delete",
            bg="#c0392b",
            fg="white",
            width=10,
            command=self.delete_contact,
        ).grid(row=1, column=0, padx=2, pady=3)
        tk.Button(
            btn_frame,
            text="Clear",
            bg="#7f8c8d",
            fg="white",
            width=10,
            command=self.clear_fields,
        ).grid(row=1, column=1, padx=2, pady=3)

    def display_contacts(self, contact_list):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, contact in enumerate(contact_list):
            self.tree.insert(
                "",
                tk.END,
                iid=idx,
                values=(contact.get("name"), contact.get("phone")),
            )

    def select_contact(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        idx = int(selected[0])
        # Find the correct contact even if filtered
        contact_name = self.tree.item(selected[0], "values")[0]
        contact_phone = self.tree.item(selected[0], "values")[1]

        for i, c in enumerate(self.contacts):
            if c["name"] == contact_name and c["phone"] == contact_phone:
                self.current_selected_index = i
                break

        contact = self.contacts[self.current_selected_index]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact.get("name", ""))

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact.get("phone", ""))

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact.get("email", ""))

        self.address_entry.delete("1.0", tk.END)
        self.address_entry.insert("1.0", contact.get("address", ""))

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", tk.END).strip()

        if not name or not phone:
            messagebox.showwarning("Error", "Name and Phone Number are required!")
            return

        new_contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
        }

        self.contacts.append(new_contact)
        self.save_contacts()
        self.display_contacts(self.contacts)
        self.clear_fields()
        messagebox.showinfo("Success", "Contact added successfully.")

    def update_contact(self):
        if self.current_selected_index is None:
            messagebox.showwarning("Error", "Please select a contact to update.")
            return

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", tk.END).strip()

        if not name or not phone:
            messagebox.showwarning("Error", "Name and Phone Number cannot be blank!")
            return

        self.contacts[self.current_selected_index] = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
        }

        self.save_contacts()
        self.display_contacts(self.contacts)
        self.clear_fields()
        messagebox.showinfo("Success", "Contact updated successfully.")

    def delete_contact(self):
        if self.current_selected_index is None:
            messagebox.showwarning("Error", "Please select a contact to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?")
        if confirm:
            self.contacts.pop(self.current_selected_index)
            self.save_contacts()
            self.display_contacts(self.contacts)
            self.clear_fields()
            messagebox.showinfo("Success", "Contact deleted.")

    def search_contact(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.display_contacts(self.contacts)
            return

        results = [
            c
            for c in self.contacts
            if query in c["name"].lower() or query in c["phone"].lower()
        ]
        self.display_contacts(results)

    def clear_fields(self):
        self.current_selected_index = None
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete("1.0", tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()