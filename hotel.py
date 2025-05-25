import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x400")
        self.rooms = {f"Room {i}": None for i in range(1, 11)}  # 10 rooms
        self.create_widgets()

    def create_widgets(self):
        self.room_label = tk.Label(self.root, text="Select Room:")
        self.room_label.grid(row=0, column=0)
        self.room_var = tk.StringVar(value=list(self.rooms.keys())[0])
        self.room_menu = tk.OptionMenu(self.root, self.room_var, *self.rooms.keys())
        self.room_menu.grid(row=0, column=1)

        self.guest_name_label = tk.Label(self.root, text="Guest Name:")
        self.guest_name_label.grid(row=1, column=0)
        self.guest_name_entry = tk.Entry(self.root)
        self.guest_name_entry.grid(row=1, column=1)

        self.check_in_button = tk.Button(self.root, text="Check In", command=self.check_in)
        self.check_in_button.grid(row=2, column=0)

        self.check_out_button = tk.Button(self.root, text="Check Out", command=self.check_out)
        self.check_out_button.grid(row=2, column=1)

        self.bill_button = tk.Button(self.root, text="Generate Bill", command=self.generate_bill)
        self.bill_button.grid(row=3, column=0, columnspan=2)

    def check_in(self):
        room = self.room_var.get()
        guest_name = self.guest_name_entry.get()
        if not guest_name:
            messagebox.showwarning("Input Error", "Please enter guest name.")
            return
        if self.rooms[room]:
            messagebox.showwarning("Room Occupied", f"{room} is already occupied.")
        else:
            self.rooms[room] = {"guest_name": guest_name, "check_in": datetime.now()}
            messagebox.showinfo("Check In", f"Checked in {guest_name} to {room}.")

    def check_out(self):
        room = self.room_var.get()
        if not self.rooms[room]:
            messagebox.showwarning("No Guest", f"No guest in {room}.")
        else:
            guest_name = self.rooms[room]["guest_name"]
            self.rooms[room] = None
            messagebox.showinfo("Check Out", f"Checked out {guest_name} from {room}.")

    def generate_bill(self):
        room = self.room_var.get()
        if not self.rooms[room]:
            messagebox.showwarning("No Guest", f"No guest in {room}.")
        else:
            guest_name = self.rooms[room]["guest_name"]
            check_in_time = self.rooms[room]["check_in"]
            stay_duration = (datetime.now() - check_in_time).days
            bill_amount = stay_duration * 100  # Assuming $100 per day
            messagebox.showinfo("Bill", f"Guest: {guest_name}\nStay Duration: {stay_duration} days\nTotal Bill: ${bill_amount}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()

