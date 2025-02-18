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

frame1 = tk.Frame(root, bg="#1E1E2E")
frame1.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("TButton", background="#1E1E2E", foreground="#98FF98", font=("Segoe UI", 14, "bold"))

budget = crud.displaySum_budget()
ex = crud.displaySum_expenses()


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

    global budget, ex
    budget = crud.displaySum_budget()
    ex = crud.displaySum_expenses()

    lbl_remaining_budget.config(text=f"Remaining Budget: {budget - ex}")
    lbl_total_expense.config(text=f"Total Expense: {ex}")
    btn_total_budget.config(text=f"Total Budget: {budget}")


def open_new_window_addrecord():
    new_window = tk.Toplevel(root, bg="#1E1E2E")
    new_window.title("Add New Record")
    new_window.geometry("350x250")

    def validate_integer_input(int_val_amt):   #this functions allows for strictly integer input
        if int_val_amt == "":
            return True
        return int_val_amt.isdigit()
    
    vcmd = (new_window.register(validate_integer_input), "%P")

    ttk.Label(new_window, text="Enter Details", font=("Segoe UI", 14, "bold"), background="#1E1E2E", foreground="#98FF98").grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(new_window, text="S.No.:", background="#1E1E2E", foreground="#98FF98").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    sno_entry = ttk.Entry(new_window, width=22, validate="key", validatecommand=vcmd)
    sno_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    ttk.Label(new_window, text="Date:", background="#1E1E2E", foreground="#98FF98").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    date_entry = DateEntry(new_window, width=19)
    date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    ttk.Label(new_window, text="Category:", background="#1E1E2E", foreground="#98FF98").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    categories = ["Food", "Travel", "Rent", "Utilities", "Entertainment"]
    category_dropdown = ttk.Combobox(new_window, values=categories, state="readonly", width=20)
    category_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    category_dropdown.set("Select a category")

    ttk.Label(new_window, text="Amount:", background="#1E1E2E", foreground="#98FF98").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    amount_entry = ttk.Entry(new_window, width=22, validate="key", validatecommand=vcmd)
    amount_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    
    def saveDetails_add():

        expense_data = {
        "exp_id": sno_entry.get(), 
        "date": date_entry.get_date().strftime("%Y-%m-%d"),  
        "category": category_dropdown.get(), 
        "expenses": int(amount_entry.get()) if amount_entry.get().isdigit() else 0  
        }

        if not expense_data["exp_id"]:
            messagebox.showerror("Error", "S.No. cannot be empty.")
            print("Error: S.No. cannot be empty.")
            return
        if not expense_data["category"] or expense_data["category"] == "Select a category":
            messagebox.showerror("Error", "Please select a valid category.")
            print("Error: Please select a valid category.")
            return
        if expense_data["expenses"] <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            print("Error: Amount must be greater than 0.")
            return
        
        existing_ids = [record[0] for record in crud.readData_id()]
        if expense_data["exp_id"] in existing_ids:
            messagebox.showerror("Error", "S.No. already exists.")
            print("Error: S.No. already exists.")


        try:    
            crud.insertQuery(expense_data)  
            refresh_treeview()
            print("Record successfully added!")
            messagebox.showinfo("Success", "Record successfully added!")
        except Exception as e:
            print(f"Error while adding record: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

        refresh_treeview()
    
    
    ttk.Button(new_window, text="Save", command = lambda: (saveDetails_add(), new_window.destroy()), style="TButton").grid(row=5, column=0, pady=10, padx=10)
    ttk.Button(new_window, text="Cancel", command=new_window.destroy, style="TButton").grid(row=5, column=1, pady=10, padx=10)

def update_budget():

    def save_budget():
        
        nonlocal new_budget_entry
        try:
            new_budget = int(new_budget_entry.get()) 
            if new_budget <= 0:
                raise ValueError("Budget must be greater than 0")
            global budget
            budget = new_budget 

            try:
                query = "UPDATE expenses SET budget = %s WHERE exp_id = 1"
                crud.cursor.execute(query, (budget,))
                crud.connection.commit()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update budget: {e}")
                return


            refresh_treeview()
            new_window_budget.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the budget.")
    

    new_window_budget = tk.Toplevel(root, bg="#1E1E2E")
    new_window_budget.title("Set Budget")
    new_window_budget.geometry("300x100")

    ttk.Label(new_window_budget, text="Enter New Budget:", background="#1E1E2E", foreground="#98FF98", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    new_budget_entry = ttk.Entry(new_window_budget, width=10)
    new_budget_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(new_window_budget, text="Save", command=save_budget, style="TButton").grid(row=1, column=0, pady=5, padx=5)


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
    new_window = tk.Toplevel(root, bg="#1E1E2E")
    new_window.title("Edit Existing Record")
    new_window.geometry("300x250")

    def validate_integer_input(int_val_amt):   #this functions allows for strictly integer input
        if int_val_amt == "":
            return True
        return int_val_amt.isdigit()
    
    vcmd = (new_window.register(validate_integer_input), "%P")

    ttk.Label(new_window, text="Enter Details", font=("Segoe UI", 12, "bold"), background="#1E1E2E", foreground="#FFFFFF").grid(row=0, column=0, columnspan=2, pady=15)

    ttk.Label(new_window, text="Date:", background="#1E1E2E", foreground="#FFFFFF").grid(row=1, column=0, padx=20, pady=10, sticky="e")
    date_entry = DateEntry(new_window, width=20, background="#3EB489", foreground="#000000")
    date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    ttk.Label(new_window, text="Category:", background="#1E1E2E", foreground="#FFFFFF").grid(row=2, column=0, padx=20, pady=10, sticky="e")
    categories = ["Food", "Travel", "Rent", "Utilities", "Entertainment"]
    category_dropdown = ttk.Combobox(new_window, values=categories, state="readonly", width=18)
    category_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    category_dropdown.set("Select a category")

    ttk.Label(new_window, text="Amount:", background="#1E1E2E", foreground="#FFFFFF").grid(row=3, column=0, padx=20, pady=10, sticky="e")
    amount_entry = ttk.Entry(new_window, width=20, validate="key", validatecommand=vcmd)
    amount_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    ttk.Button(new_window, text="Submit", command = lambda: (updateData(), new_window.destroy())).grid(row=4, column=0, columnspan=2, pady=20)
    


    def updateData():
   
        selected_item = tview.focus()
      
        if not selected_item:
            print("Error: No record selected!")
            messagebox.showwarning("Warning!", "No record selected!")
            return

        values = tview.item(selected_item, 'values')
        exp_id = values[0]  

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
            crud.cursor.execute(
                "UPDATE expenses SET date = %s, category = %s, expenses = %s WHERE exp_id = %s",
                (edit_data["date"], edit_data["category"], edit_data["expenses"], exp_id)
            )
            connection.commit()
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



   


btn_total_budget = tk.Button(frame1, text=f"Total Budget: {budget}", command=update_budget, font=("Segoe UI", 14, "bold"), bd=1, relief="solid", bg="#1E1E2E", fg="#98FF98")
btn_total_budget.grid(row=0, column=0, sticky="nsew")

lbl_remaining_budget = tk.Label(frame1, text=f"Remaining Money: {budget - ex}", font=("Segoe UI", 14, "bold"), bd=1, relief="solid", bg="#1E1E2E", fg="#98FF98")
lbl_remaining_budget.grid(row=0, column=1, sticky="nsew")

lbl_total_expense = tk.Label(frame1, text=f"Total Expense: {ex}", font=("Segoe UI", 14, "bold"), bd=1, relief="solid", bg="#1E1E2E", fg="#98FF98")
lbl_total_expense.grid(row=0, column=2, sticky="nsew")

btn_add_record = tk.Button(frame1, text="+", font=("Segoe UI", 14, "bold"), bg="#1E1E2E", fg="#3EB489", command=open_new_window_addrecord)  #add button calls crud.insertQuery()
btn_add_record.grid(row=0, column=3, sticky="nsew")

btn_delete_record = tk.Button(frame1, text="\U0001F5D1", font=("Segoe UI", 14, "bold"), bg="#1E1E2E", fg="#3EB489", command = deleteRecord)   #delete button calls crud.deleteQuery()
btn_delete_record.grid(row=0, column=4, sticky="nsew")

btn_edit_record = tk.Button(frame1, text="Edit", font=("Segoe UI", 14, "bold"), bg="#1E1E2E", fg="#3EB489", command=open_new_window_editrecord)   #edit button in the main gui calls crud.updateQuery()
btn_edit_record.grid(row=0, column=5, sticky="nsew")

# Treeview
tview = ttk.Treeview(frame1, columns=('I.D.', 'Date', 'Category', 'Amount'), show='headings')
tview.grid(row=1, column=0, columnspan=6, sticky="nsew")


scrollbar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tview.yview)
scrollbar.grid(row=1, column=6, sticky="ns")
tview.configure(yscrollcommand=scrollbar.set)


tview.heading('I.D.', text='Expense ID')
tview.heading('Date', text='Date')
tview.heading('Category', text='Category')
tview.heading('Amount', text='Amount')


tview.column('I.D.', width=50, anchor='center')
tview.column('Date', width=100, anchor='center')    
tview.column('Category', width=100, anchor='center')
tview.column('Amount', width=200, anchor='center')



for record in dtbcount:
    tview.insert(parent='', index='end', values=(record[0], record[1], record[2], record[3], "☐"))





root.mainloop()

input("Press Enter to exit...")