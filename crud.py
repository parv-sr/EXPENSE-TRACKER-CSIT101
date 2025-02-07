import mysql.connector as sql
from tkinter import messagebox
import __main__ as m



connection = sql.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "expense_tracker"
)


if connection.is_connected():
    print("Connection to database succesful!")


cursor = connection.cursor()

def insertQuery(expense_data):
   
    insert_query = """
        INSERT INTO expenses (exp_id, date, category, expenses)
        VALUES (%(exp_id)s, %(date)s, %(category)s, %(expenses)s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, expense_data)
        connection.commit()
        print("Expense successfully added!")
    except sql.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()


def readData():
    select_query = "SELECT * FROM expenses"
    cursor.execute(select_query)
    records = cursor.fetchall()
    
    return records


def updateData():

    def updateData_setCategory():
        update_query = "UPDATE expenses set expenses = %s WHERE category = %s"
        id = int(input("Enter the serial number of entry: "))
        new_exp = int(input("Enter the correct expense: "))

        cursor.execute(update_query, (new_exp, id))
        connection.commit()
        print(f"{id}th expense changed to {new_exp}.")

    def updateData_setDate():
        update_query = "UPDATE expenses set expenses = %s WHERE date = %s"
        id = int(input("Enter the serial number of entry: "))
        new_exp = int(input("Enter the correct expense: "))

        cursor.execute(update_query, (new_exp, id))
        connection.commit()
        print(f"{id}th expense changed to {new_exp}.")

    def updateData_setid():
        update_query = "UPDATE expenses set expenses = %s WHERE exp_id = %s"
        id = int(input("Enter the serial number of entry: "))
        new_exp = int(input("Enter the correct expense: "))

        cursor.execute(update_query, (new_exp, id))
        connection.commit()
        print(f"{id}th expense changed to {new_exp}.")



def deleteQuery():
    delete_query = "DELETE FROM expenses WHERE exp_id = %s"
    remve = int(input("Enter the serial number of entry: "))

    cursor.execute(delete_query, (remve))
    connection.commit()
    print("Deletion Succesful.")





def displaySum():
    dis_sum = "SELECT SUM(expenses) FROM expenses;"
    cursor.execute(dis_sum)
    result = cursor.fetchone()
    return int(result[0]) if result[0] is not None else 0

def displayCount():
    dis_count = "SELECT COUNT(expenses) from expenses;"
    cursor.execute(dis_count)
    result = cursor.fetchone()
    return int(result[0]) if result[0] is not None else 0