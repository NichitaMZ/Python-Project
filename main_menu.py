import mysql.connector
from tkinter import Menu
import sys
import tkinter as tk
from my_functions import is_integer
from my_functions import is_string
from my_functions import exit_all 
from tkinter import messagebox
import re #to provide proper pattern how it should be entered
import subprocess



def open_customer():
    subprocess.Popen(["python","customer_table.py"])


def open_product():
    subprocess.Popen(["python","product_table.py"])


def open_sales():
    subprocess.Popen(["python","sale_table.py"])


def open_suppliers():
    subprocess.Popen(["python","suppliers_table.py"])

def open_cust_reports():
    subprocess.Popen(["python","CustomerReportexcel.py"])

def open_sales_reports():
    subprocess.Popen(["python","report_sale.py"])

root = tk.Tk()
root.title("SPORTMD MAIN MENU")
root.geometry("800x600")
root.resizable(False,False)
root.iconbitmap("images/Logo.ico")


menu_bar = Menu(root)


file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Customers", command=open_customer)  # Customers menu option
file_menu.add_command(label="Products", command=open_product)  # Products menu option
file_menu.add_command(label="Suppliers", command=open_suppliers)  # Suppliers menu option
file_menu.add_command(label="Sales", command=open_sales)  # Sales menu option

file_menu.add_separator()

file_menu.add_command(label="Exit",command=exit_all)


# Create a Report menu
report_menu = Menu(menu_bar, tearoff=0)
report_menu.add_command(label="Customer Report")#, command=open_report_customer)  # Customers menu option
report_menu.add_command(label="Products Report")#, command=open_report_product)  # Products menu option
report_menu.add_command(label="Suppliers Report")#, command=open_report_suppliers)  # Suppliers menu option
report_menu.add_command(label="Sales Report",command=open_sales_reports)#, command=open_report_sales)

# Add File menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Report", menu=report_menu)
 
# Display the menu bar
root.config(menu=menu_bar)

try:
    image = tk.PhotoImage(file="Images\kudim3.png")  # Load the image. Suggested to use png, otherwise different code is needed
    label_image = tk.Label(root, image=image)  # Create a Label to display the image:It is needed.
    label_image.pack(pady=20)  # packing = place the image on the window
except tk.TclError:
    # Handle error if the image file is not found or format is unsupported
    label_image = tk.Label(root, text="Image could not be loaded", font=("Arial", 14))
    label_image.pack(pady=20)









root.mainloop()
