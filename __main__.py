import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector as sql
import crud 

# Database connection
connection = sql.connect(
    host="localhost",
    user="root",    
    password="",
    database="expense_tracker"
)

if connection.is_connected():
    print("Connection to database successful!")


dtbcount = crud.readData()

# Main GUI
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1600x900")

frame1 = tk.Frame(root, bg="#454746")
frame1.pack(fill="both", expand=True)

budget = (69696969)
ex = crud.displaySum()


for i in range(6):
    frame1.columnconfigure(i, weight=1)
    frame1.rowconfigure(1, weight=1)  

def refresh_treeview():
    for row in tview.get_children():
        tview.delete(row)
    crud.cursor.execute("SELECT * FROM expenses")
    rows = crud.cursor.fetchall()
    for row in rows:
        tview.insert("", "end", values = row)


def open_new_window_addrecord():
    new_window = tk.Toplevel(root, bg="#454746")
    new_window.title("Add New Record")
    new_window.geometry("300x200")

    def validate_integer_input(int_val_amt):   #this functions allows for strictly integer input
        if int_val_amt == "":
            return True
        return int_val_amt.isdigit()
    
    vcmd = (new_window.register(validate_integer_input), "%P")

    ttk.Label(new_window, text="Enter Details").grid(row=0, padx=10, pady=5, columnspan=2)

    ttk.Label(new_window, text="S.No.: ").grid(row=1, column=0, padx=20, pady=5, sticky="w")
    sno_entry = ttk.Entry(new_window, width=20, validate = "key", validatecommand = vcmd)
    sno_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Date: ").grid(row=2, column=0, padx=20, pady=5, sticky="w")
    date_entry = DateEntry(new_window, width=20)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Category:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
    categories = ["Food", "Travel", "Rent", "Utilities", "Entertainment"]
    category_dropdown = ttk.Combobox(new_window, values=categories, state="readonly", width=18)
    category_dropdown.grid(row=3, column=1, padx=10, pady=5)
    category_dropdown.set("Select a category")


    ttk.Label(new_window, text="Amount:").grid(row=4, column=0, padx=20, pady=5, sticky="w")
    amount_entry = ttk.Entry(new_window, width=20, validate = "key", validatecommand = vcmd)
    amount_entry.grid(row=4, column=1, padx=10, pady=5)

    
    def saveDetails_add():

        expense_data = {
        "exp_id": sno_entry.get(), 
        "date": date_entry.get_date().strftime("%Y-%m-%d"),  
        "category": category_dropdown.get(), 
        "expenses": int(amount_entry.get()) if amount_entry.get().isdigit() else 0  
        }

        if not expense_data["exp_id"]:
            print("Error: S.No. cannot be empty.")
            return
        if not expense_data["category"] or expense_data["category"] == "Select a category":
            print("Error: Please select a valid category.")
            return
        if expense_data["expenses"] <= 0:
            print("Error: Amount must be greater than 0.")
            return

        try:    
            crud.insertQuery(expense_data)  
            print("Record successfully added!")
        except Exception as e:
            print(f"Error while adding record: {e}")

        refresh_treeview()



    ttk.Button(new_window, text="Save", command = lambda: (saveDetails_add(), new_window.destroy())).grid(row=5, column=0, pady=10, padx=10)
    ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=5, column=1, pady=10, padx=10)

def update_budget():
    def save_budget():
        nonlocal new_budget_entry
        try:
            new_budget = int(new_budget_entry.get()) 
            if new_budget <= 0:
                raise ValueError("Budget must be greater than 0")
            global budget
            budget = new_budget 
            lbl_remaining_budget.config(text=f"Remaining Budget: {budget - ex}")
            btn_total_budget.config(text=f"Total Budget: {budget}")
            new_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the budget.")

    new_window = tk.Toplevel(root, bg="#454746")
    new_window.title("Set Budget")
    new_window.geometry("300x150")

    ttk.Label(new_window, text="Enter New Budget:", background="#454746", foreground="white").grid(row=0, column=0, padx=20, pady=20, sticky="w")
    new_budget_entry = ttk.Entry(new_window, width=20)
    new_budget_entry.grid(row=0, column=1, padx=10, pady=20)

    ttk.Button(new_window, text="Save", command=save_budget).grid(row=1, column=0, columnspan=2, pady=10)

def deleteRecord():
    selected_item = tview.focus()
    if not selected_item:
        messagebox.showwarning("Warning!", "No record selected!")
        return
    
    values = tview.item(selected_item, 'values')
    exp_id = values[0] 

    if messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete record ID {exp_id}?"):
        try:
            crud.cursor.execute("DELETE FROM expenses WHERE exp_id = %s", (exp_id,))  
            connection.commit()
            tview.delete(selected_item)  
            refresh_treeview()

            messagebox.showinfo("Success", f"Record ID {exp_id} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")  




def open_new_window_editrecord():
    new_window = tk.Toplevel(root, bg="#454746")
    new_window.title("Edit Existing Record")
    new_window.geometry("300x200")

    def validate_integer_input(int_val_amt):   #this functions allows for strictly integer input
        if int_val_amt == "":
            return True
        return int_val_amt.isdigit()
    
    vcmd = (new_window.register(validate_integer_input), "%P")

    ttk.Label(new_window, text="Enter Details").grid(row=0, padx=10, pady=5, columnspan=2)

    ttk.Label(new_window, text="Date: ").grid(row=2, column=0, padx=20, pady=5, sticky="w")
    date_entry = DateEntry(new_window, width=20)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Category:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
    categories = ["Food", "Travel", "Rent", "Utilities", "Entertainment"]
    category_dropdown = ttk.Combobox(new_window, values=categories, state="readonly", width=18)
    category_dropdown.grid(row=3, column=1, padx=10, pady=5)
    category_dropdown.set("Select a category")


    ttk.Label(new_window, text="Amount:").grid(row=4, column=0, padx=20, pady=5, sticky="w")
    amount_entry = ttk.Entry(new_window, width=20, validate = "key", validatecommand = vcmd)
    amount_entry.grid(row=4, column=1, padx=10, pady=5)



    def updateData():
   
        selected_item = tview.focus()

        if not selected_item:
            print("Error: No record selected!")
            return

         # Get the exp_id from the selected row
        values = tview.item(selected_item, 'values')
        exp_id = values[0]  # Assuming exp_id is at index 0

        # Gather new values from GUI elements
        edit_data = {
            "date": date_entry.get_date().strftime("%Y-%m-%d"),  
            "category": category_dropdown.get(), 
            "expenses": int(amount_entry.get()) if amount_entry.get().isdigit() else 0  
    }

    # Input validation
        if not edit_data["category"] or edit_data["category"] == "Select a category":
            print("Error: Please select a valid category.")
            return
        if edit_data["expenses"] <= 0:
            print("Error: Amount must be greater than 0.")
            return

        try:
            # Update the existing record in the database
            crud.cursor.execute(
                "UPDATE expenses SET date = %s, category = %s, expenses = %s WHERE exp_id = %s",
                (edit_data["date"], edit_data["category"], edit_data["expenses"], exp_id)
            )
            connection.commit()

            # Refresh the Treeview to reflect the changes
            refresh_treeview()

            print(f"Record ID {exp_id} successfully updated!")
        except Exception as e:
            print(f"Error while updating record: {e}")





    
    def saveDetails_edit():

        edit_data = {
        "date": date_entry.get_date().strftime("%Y-%m-%d"),  
        "category": category_dropdown.get(), 
        "expenses": int(amount_entry.get()) if amount_entry.get().isdigit() else 0  
        }

        if not edit_data["category"] or edit_data["category"] == "Select a category":
            print("Error: Please select a valid category.")
            return
        if edit_data["expenses"] <= 0:
            print("Error: Amount must be greater than 0.")
            return

        try:    
            crud.insertQuery(edit_data)  
            print("Record successfully added!")
        except Exception as e:
            print(f"Error while adding record: {e}")

        refresh_treeview()



    ttk.Button(new_window, text="Save", command = lambda: (saveDetails_edit(), new_window.destroy())).grid(row=5, column=0, pady=10, padx=10)
    ttk.Button(new_window, text="Cancel", command=new_window.destroy).grid(row=5, column=1, pady=10, padx=10)
   


btn_total_budget = tk.Button(frame1, text=f"Total Budget: {budget}", command=update_budget, font=("Arial", 14), bd=1, relief="solid", bg="#1f1f1f", fg="white")
btn_total_budget.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lbl_remaining_budget = tk.Label(frame1, text=f"Remaining Budget: {budget-ex}", font=("Arial", 14), bd=1, relief="solid", bg="#1f1f1f", fg="white")
lbl_remaining_budget.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

lbl_total_expense = tk.Label(frame1, text=f"Total Expense: {ex}", font=("Arial", 14), bd=1, relief="solid", bg="#1f1f1f", fg="white")
lbl_total_expense.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

btn_add_record = tk.Button(frame1, text="+", font=("Arial", 14), bg="#1f1f1f", fg="white", command=open_new_window_addrecord)  #add button calls crud.insertQuery()
btn_add_record.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

btn_delete_record = tk.Button(frame1, text="\U0001F5D1", font=("Arial", 14), bg="#1f1f1f", fg="white", command = deleteRecord)   #delete button calls crud.deleteQuery()
btn_delete_record.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

btn_edit_record = tk.Button(frame1, text="Edit", font=("Arial", 14), bg="#1f1f1f", fg="white", command=open_new_window_editrecord)   #edit button in the main gui calls crud.updateQuery()
btn_edit_record.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")

# Treeview
tview = ttk.Treeview(frame1, columns=('id', 'date', 'category', 'amount', 'checkbox'), show='headings')
tview.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)


scrollbar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tview.yview)
scrollbar.grid(row=1, column=6, sticky="ns")
tview.configure(yscrollcommand=scrollbar.set)


tview.heading('id', text='Expense ID')
tview.heading('date', text='Date')
tview.heading('category', text='Category')
tview.heading('amount', text='Amount')
tview.heading('checkbox', text='Select')

tview.column('id', width=100, anchor='center')
tview.column('date', width=100, anchor='center')    
tview.column('category', width=100, anchor='center')
tview.column('amount', width=100, anchor='center')
tview.column('checkbox', width=50, anchor='center') 


for record in dtbcount:
    tview.insert(parent='', index='end', values=(record[0], record[1], record[2], record[3], "☐"))


def toggle_row_selection(event):
    selected_item = tview.focus()
    if not selected_item:
        return
    
    values = list(tview.item(selected_item, 'values'))
    values[4] = "☑" if values[4] == "☐" else "☐"
    tview.item(selected_item, values=values)
    
tview.bind("<Button-1>", toggle_row_selection)



root.mainloop()

input("Press Enter to exit...")