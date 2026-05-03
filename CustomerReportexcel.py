import tkinter as tk
from tkinter import messagebox
from my_functions import exit_root
from my_functions import get_mydb_connect
import pandas as pd

def print_all_customers():
    print("HELLO WORLD")


def print_count_by_locality():
    print("HELLO WORLD")


def print_by_surname():
    surname = cust_surname.get()
    my_cursor.execute(customers_by_surname_report,(surname,))
    cust_by_surname = my_cursor.fetchall()
    #the fetchall returns a list of tuples
    #each row/record is a tuple
    
    if(len(cust_by_surname) > 0):
        columns = [desc[0] for desc in my_cursor.description]
        #getting into lists
        cust_surname_frame = pd.DataFrame(cust_by_surname,columns=columns)
        print(cust_by_surname)
        
        cust_surname_frame.to_excel(f"Customers_{surname}.xlsx",index=False)
        messagebox.showinfo("REPORT","Report was generated successfuly")
        cust_surname.set("")
        label1.set(f"Print Customers by:")
    else:
        messagebox.showerror("REPORT ERROR","No customers were found")

#function that detects what user inputs
def surname_changed(event):
    surname = cust_surname.get()
    label1.set(f"Print Customers by : {surname}")

#db connection

mydb = get_mydb_connect()
my_cursor = mydb.cursor()
 
#sql statements
customers_by_surname_report = "SELECT * FROM customer WHERE cust_surname = %s ORDER BY cust_surname"
all_customers = "SELECT * FROM customer ORDER BY cust_surname"
count_by_locality = "SELECT COUNT(cust_id), cust_locality FROM customer GROUP BY cust_locality"


root = tk.Tk()
root.geometry("500x400")
root.title("SPORTMD-CUSTOMERS REPORTS")
root.resizable(False,False)
root.iconbitmap("images/logo.ico")


#variables

cust_surname = tk.StringVar()

label1 = tk.StringVar()

label1.set(f"Print Customers by:")
 
#font styles

default_font = ("Arial",14)

title_font = ("Verdana",14)

button_font = ("Courier New",14)


#widgets
#labels
title_lbl = tk.Label(root,text="SPORT MD - CUSTOMER DETAILS REPORT",font=title_font,bg="#DD8833")
cust_lbl1 = tk.Label(root,textvariable=label1,font=default_font)
space_lbl = tk.Label(root,text="-----------------------------------------------",font=default_font)
 
#entry boxes
cust_surname_txt = tk.Entry(root,textvariable=cust_surname,width=20,font=default_font)
cust_surname_txt.bind("<KeyRelease>",surname_changed)
 
#buttons
print_surname_btn = tk.Button(root,text="Create Report",font=button_font,command=print_by_surname)
print_all_customers_btn = tk.Button(root,text="Print ALL customers",font=button_font,command=print_all_customers)
print_by_locality_btn = tk.Button(root,text="Count by locality",font=button_font,command=print_count_by_locality)
exit_btn = tk.Button(root,text="EXIT",font=button_font,width=20)


#placing the widgets
title_lbl.grid(row=0,columnspan=2,sticky="we")
cust_lbl1.grid(row=1,column=0,padx=20,sticky="sw")
cust_surname_txt.grid(row=2,column=0,padx=20,sticky="nw")
print_surname_btn.grid(row=3,column=0,padx=20,sticky="nw")
space_lbl.grid(row=4,columnspan=2,sticky="nwe")
print_all_customers_btn.grid(row=5,column=0,padx=20,sticky="nw")
print_by_locality_btn.grid(row=5,column=1,padx=20,sticky="nw")
exit_btn.grid(row=6,columnspan=2,sticky="we")

#setting the grid

root.rowconfigure((0,1,2,3,4,5,6),weight=1)

root.columnconfigure((0,1),weight=1)
 
root.mainloop()