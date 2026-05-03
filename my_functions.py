import sys
import mysql.connector
import re
from tkinter import messagebox

mydb = None

def is_numeric(value):
    if not value:
        return 0
    try:
        number = float(value)
        return number
    except ValueError:
        return -1 


def is_valid_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"  #for proper email validation format
    return re.match(email_regex, email) is not None

 
    
def is_string(value):
#to check for strings onlyy
    if not value:
        return False  # Reject empty input
    return all(char.isalpha() or char in [' ', '-'] for char in value)  
 
 

def is_empty(box_entry):
    if(not(box_entry)):
        return True
    else:
        return False

    
    
def is_integer(value):
    if not value:
        return 0
    try:
        number = int(value)
        return number
    except ValueError:
        return -1



def exit_root():
    sys.exit()



def exit_all():
    messagebox.showinfo("Exit","Sport MD system is closing")
    sys.exit()

"""
def valid_id(product_id):
    pattern = r'^\d{8,10}$'
    return bool(re.match(pattern,product_id))
"""



def get_mydb_connect():
    
    global mydb
    
    if mydb is None:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="costumesdb"
        )
        
    return mydb













