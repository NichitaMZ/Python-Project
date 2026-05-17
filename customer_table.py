import mysql.connector
import sys
import tkinter as tk
from my_functions import is_integer
from my_functions import get_mydb_connect
from my_functions import exit_root
from my_functions import is_valid_email
from my_functions import is_numeric
from my_functions import is_string
from tkinter import messagebox
import re




# Main validation function
def validate_fields():
    ###~~~###~~~###~~~###
    code = custid_var.get()
    name = custname_var.get()
    surname = custsurname_var.get()
    locality = custlocality_var.get()
    street = custstreet_var.get()
    house = custhouseno_var.get()
    postcode = custpostcode_var.get()
    mobile = custmob_var.get()
    email = custemail_var.get()
    ###~~~###~~~###~~~###
    
    #Duplicates))
    ###~~~###~~~###~~~###
    cust_id = code.strip()
    cust_name = name.strip()
    cust_surname = surname.strip()
    cust_email = email.strip()
    custhouse_no = house.strip()
    custpost_code = postcode.strip()
    ###~~~###~~~###~~~###
    ###~~~###~~~###~~~###
    error_message = "INVALID: "
    errors = False
    missing_fields = []

    if not cust_id:
        missing_fields.append("Customer ID")
    if not cust_name:
        missing_fields.append("Customer Name")
    if not cust_surname:
        missing_fields.append("Customer Surname")

    if missing_fields:
        messagebox.showerror("Input Error", f"Please fill in the following required fields: {', '.join(missing_fields)}.")
        return False
                     

    ###PROPER NAME###
    if not is_string(cust_name):
        error_message += " \n Name (ex: Donald)"
        errors = True
    ###~~~###~~~###~~~###~~~###
    
    ###PROPER SURNAME###
    if not is_string(cust_surname):
        error_message += " \n Surname (ex: Trump)"
        errors = True
    ###~~~###~~~###~~~###~~~###
        

    ###CUSTOMER EMAIL###
    if cust_email and not is_valid_email(cust_email):
        error_message += " \n E-mail (ex: donaldtrump@yahoo.com)"
        errors = True
    ###~~~###~~~###~~~###~~~###

    ###CUSTOMER LOCALITY###
    
    if locality:
        if not is_valid_locality(locality):
            error_message += " \n Locality format (ex: San Pawl il-Baħar)"
            errors = True

    
    
        #####CUSTOMER ID#####
    if cust_id:
        if not valid_id(cust_id):
            error_message += " \n Customer ID (ex: 0234113A)"
            errors = True
    else:
        error_message += " \n Customer ID is required"
        errors = True
    
    if custhouse_no:
        try:
            custhouse_no = int(custhouse_no)  # Convert to int to check validity
            if custhouse_no <= 0:  # Ensure house number is positive
                error_message += "\n House Number must be a positive integer"
                errors = True
        except ValueError:
            error_message += "\n House Number must be a valid integer"
            errors = True
    
    if errors:
        messagebox.showerror("Input Error", error_message)
        return False   
        
    try:
        my_cursor.execute(chk_customer,(cust_id,))
        recordset = my_cursor.fetchall()
        if len(recordset) > 0:
            messagebox.showerror("ERROR", "The Customer ID exists already")
            return False
                
        response = messagebox.askyesno("CONFIRM","Are you sure you want to save the current data?")
        if (response == True):
            messagebox.showinfo("CONFIRM",f"The {cust_id} ID is saved succesfully")
        else:
            messagebox.showinfo("CONFIRM",f"The {cust_id} ID is not saved")
            return False
                    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error",f"Error checking Customer: {err}")
        return False 
            ###~~~###~~~###~~~###~~~###
    
    try:
        my_cursor.execute(save_data, (code, name, surname, locality, street, house, postcode, mobile, email))
        mydb.commit()  # Make sure to commit the transaction to save changes
    except mysql.connector.Error as db_err:
        messagebox.showerror("Database Error", f"Failed to insert data into database: {db_err}")
        return False
    else:
        messagebox.showinfo("Success", "Customer data saved successfully.")
        return True



#### MAIN FUNCTION ####


def update_customer():
    cust_id = custid_var.get().strip()
    cust_name = custname_var.get().strip()
    cust_surn = custsurname_var.get().strip()
    cust_locality = custlocality_var.get().strip()
    cust_street = custstreet_var.get().strip()
    cust_houseno = custhouseno_var.get().strip()
    cust_post = custpostcode_var.get().strip()
    cust_mob = custmob_var.get().strip()
    cust_email = custemail_var.get().strip()
    
    
    response = messagebox.askyesno("Update","Are you sure you want to update this information")
    
    if(response == True):
        my_cursor.execute(upd_customer,(cust_name,cust_surn,cust_locality,cust_street,cust_houseno,cust_post,cust_mob,cust_email,cust_id,))
        mydb.commit()
        messagebox.showinfo("Update",f"{cust_id} was successfuly updated")
    else:
        messagebox.showinfo("Update","Successfully canceled updation")




def search_button():
    cust_id = custid_var.get().strip()
    
    if not(cust_id):
        messagebox.showerror("ERROR","To search for a Customer please enter a valid Customer ID") 
    else:
        my_cursor.execute(chk_customer,(cust_id,))
        recordset = my_cursor.fetchall()
        
        if (len(recordset) > 0):
            for row in recordset:
                cust_id,cust_name,cust_surname,cust_locality,cust_street,cust_houseno,cust_post,cust_mob,cust_email = row
                
                custid_var.set(cust_id)
                custname_var.set(cust_name)
                custsurname_var.set(cust_surname)
                custlocality_var.set(cust_locality)
                custstreet_var.set(cust_street)
                custhouseno_var.set(cust_houseno)
                custpostcode_var.set(cust_post)
                custmob_var.set(cust_mob)
                custemail_var.set(cust_email)
                update_btn.config(state=tk.NORMAL)

        else:
            update_btn.config(state=tk.DISABLED)
            messagebox.showerror("INVALID","Customer ID was not found")
            clear_fields()
       



def delete_customer():
    cust_id = custid_var.get().strip()
    
    if not cust_id:
        messagebox.showerror("ERROR","Fill in the Customer ID for DELETION")
        return False
    
    if not (valid_id(cust_id)):
        messagebox.showerror("ERROR","Apporpriate Customer ID (ex:0234140A)")
        return False
    
    try:
        my_cursor.execute(chk_customer,(cust_id,))
        cust_record = my_cursor.fetchall()
        if len(cust_record) == 0:
            messagebox.showerror("ERROR","The Customer ID does not exist")
            return False
        
        response = messagebox.askyesno("Confirm Deletion",f"Are you sure you want to delete {cust_id}?")
        if(response == True):
            my_cursor.execute(del_customer,(cust_id,))
            mydb.commit()
            messagebox.showinfo("Success",f"The {cust_id} was successfully deleted")
        else:
            messagebox.showinfo("Aborted","You successfully canceled the deletion")
            
            
    except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error checking customer: {err}")
                return False
        





def valid_id(customer_id):
    id_regex = r"^\d{7,10}[AMLBGHPZ]$" # malta id format (0234140A)
    return bool(re.match(id_regex,customer_id))



def save_customer():
    if(validate_fields() == True ):
        # Save data logic here
        clear_fields()     
        root.destroy()




def exit_root():
    root.destroy()


def clear_fields():
    custid_var.set("")
    custname_var.set("")
    custsurname_var.set("")
    custlocality_var.set("")
    custstreet_var.set("")
    custhouseno_var.set("")
    custpostcode_var.set("")
    custmob_var.set("")
    custemail_var.set("")



def is_numeric(value):
    if not value:
        return 0
    try:
        number = float(value)
        return number
    except ValueError:
        return -1

"""
def postcode_validate(post_code):
    post_code = post_code.upper()
    
    pc_regex = r"^[A-Z]{3}\d{4-6}$"
    
    return  re.match(pc_regex,post_code) is not None
"""


def email_limit(*args):
    cust_email = custemail_var.get().strip()
    custemail_var.set(cust_email)
    
    if len(cust_email) > 35:
        cust_email = cust_email[:35]
    
    custemail_var.set(cust_email)
    


def cust_id_limit(*args):
    cust_id = custid_var.get().strip().upper()
    custid_var.set(cust_id)
    if len(cust_id) > 10:
        cust_id = cust_id[:10]  
    
    custid_var.set(cust_id)


def mobile_limit(*args):
    cust_mob = custmob_var.get().strip()
    custmob_var.set(cust_mob)
    
    if len(cust_mob) > 12:
        cust_mob = cust_mob[:13]
    
    custmob_var.set(cust_mob)



def post_limit(*args):
    cust_post = custpostcode_var.get().strip().upper()
    custpostcode_var.set(cust_post)
    
    if len(cust_post) > 8:
        cust_post = cust_post[:8]
        
    custpostcode_var.set(cust_post)



def house_limit(*args):
    cust_house = custhouseno_var.get().strip()
    custhouseno_var.set(cust_house)
    
    if len(cust_house) > 3:
        cust_house = cust_house[:3]
        
    custhouseno_var.set(cust_house)



def street_limit(*args):
    cust_street = custstreet_var.get()
    custstreet_var.set(cust_street)
    
    if len(cust_street) > 20:
        cust_street = cust_street[:20]
        
    custstreet_var.set(cust_street)


    
def cust_name_limit(*args):
    cust_name = custname_var.get().strip()
    if cust_name:
        cust_name = cust_name[0].upper() + cust_name[1:]
    custname_var.set(cust_name)
    if len(cust_name) > 20:
        cust_name = cust_name[:20]
        
    custname_var.set(cust_name)
    
    

def cust_surn_limit(*args):
    cust_surname = custsurname_var.get().strip()
    if cust_surname:
        cust_surname = cust_surname[0].upper() + cust_surname[1:]
    custsurname_var.set(cust_surname)
    if len(cust_surname) > 20:
        cust_surname = cust_surname[:20]
        
    custsurname_var.set(cust_surname)


def is_valid_locality(value):
    # Check if the locality consists of letters, spaces, and hyphens
    return bool(re.match(r"^[a-zA-Z\s-]+$", value))    


   
def cust_locality_limit(*args):
    cust_locality = custlocality_var.get()
    
    # Limit to 25 characters and remove any invalid characters
    cust_locality = re.sub(r"[^a-zA-Z\s-]", "", cust_locality)
    cust_locality = cust_locality[:25]
    
    # Set the cleaned value back to the entry field
    custlocality_var.set(cust_locality)

#window
root = tk.Tk()
root.geometry("1080x720")
root.resizable(False,False)
root.title("Sport MD")
root.iconbitmap("images\Logo.ico")
#---#---#

# Database connection

mydb = get_mydb_connect()
my_cursor = mydb.cursor()

# SQL statement
upd_customer = "UPDATE customer SET cust_name = %s, cust_surname = %s, cust_locality = %s, cust_street = %s, cust_house_no = %s, cust_postcode = %s, cust_mob = %s, cust_email = %s WHERE cust_id = %s"

del_customer = "DELETE  FROM customer WHERE cust_id = %s"
chk_customer = " SELECT * FROM customer WHERE cust_id = %s" 
save_data = """INSERT INTO customer (cust_id, cust_name, cust_surname, cust_locality, cust_street, 
                cust_house_no, cust_postcode, cust_mob, cust_email)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

#variables
custid_var = tk.StringVar()
custname_var = tk.StringVar()
custsurname_var = tk.StringVar()
custlocality_var = tk.StringVar()
custstreet_var = tk.StringVar()
custhouseno_var = tk.StringVar()
custpostcode_var = tk.StringVar()
custmob_var = tk.StringVar()
custemail_var = tk.StringVar()
#---#---#

#vars with setups
custid_var.trace('w',cust_id_limit)
custname_var.trace('w',cust_name_limit)
custsurname_var.trace('w',cust_surn_limit)
custlocality_var.trace('w', cust_locality_limit)
custstreet_var.trace("w", street_limit)
custhouseno_var.trace("w", house_limit)
custpostcode_var.trace("w", post_limit)
custmob_var.trace("w", mobile_limit)
custemail_var.trace("w", email_limit)

#---#---#

#fonts
title_font = ("Arial",18)
default_font = ("Arial",14)
button_font = ("Courier New",14) 
#---#---#
#labels
screen_title_lbl = tk.Label(root,text="CUSTOMER TABLE",font=title_font,fg="yellow",bg="blue")
custid_lbl = tk.Label(root,text="Customer ID*",font=default_font)
custname_lbl = tk.Label(root,text="Customer Name*",font=default_font)
custsurname_lbl = tk.Label(root,text="Customer Surname*",font=default_font)
custlocality_lbl = tk.Label(root,text="Locality",font=default_font)
custstreet_lbl = tk.Label(root,text="Street",font=default_font)
custhouseno_lbl = tk.Label(root,text="House Number",font=default_font)
custpostcode_lbl = tk.Label(root,text="Post Code",font=default_font)
custmob_lbl = tk.Label(root,text="Mobile",font=default_font)
custemail_lbl = tk.Label(root,text="E-mail",font=default_font)
#---#---#
#entry boxes
custid_txt = tk.Entry(root,textvariable=custid_var,font=default_font)
custname_txt = tk.Entry(root,textvariable=custname_var,font=default_font)
custsurname_txt = tk.Entry(root,textvariable=custsurname_var,font=default_font)
custlocality_txt = tk.Entry(root,textvariable=custlocality_var,font=default_font)
custstreet_txt = tk.Entry(root,textvariable=custstreet_var,font=default_font)
custhouseno_txt = tk.Entry(root,textvariable=custhouseno_var,font=default_font)
custpostcode_txt = tk.Entry(root,textvariable=custpostcode_var,font=default_font)
custmob_txt = tk.Entry(root,textvariable=custmob_var,font=default_font)
custemail_txt = tk.Entry(root,textvariable=custemail_var,font=default_font)
#---#---#

#buttons
save_btn = tk.Button(root,text="Save Details",command=save_customer,font=button_font,fg="white",bg="green")
reset_btn = tk.Button(root,text="Reset Details",command=clear_fields,font=button_font)
exit_btn = tk.Button(root,text="EXIT",command=exit_root,font=button_font,fg="white",bg="red")
del_btn = tk.Button(root,text="Delete Customer Details",command=delete_customer,font=button_font,fg="red")
update_btn = tk.Button(root,text="Update Details",command=update_customer,font=button_font,fg="blue",state='disabled')
search_btn = tk.Button(root,text="SEARCH",command=search_button,font=button_font,bg='green',fg='white')
#---#---#

#binding

#grid layout
root.columnconfigure((0,1,2),weight=1)
root.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
#---#---#


#the grid
screen_title_lbl.grid(row=0,columnspan=3,sticky="we")
custid_lbl.grid(row=1,column=0,sticky="sw",padx=55)
custid_txt.grid(row=2,column=0,sticky="nw",padx=20,pady=10)
custname_lbl.grid(row=1,column=1,sticky="sw",padx=55)
custname_txt.grid(row=2,column=1,sticky="nw",padx=20,pady=10)
custsurname_lbl.grid(row=1,column=2,sticky="sw",padx=55)
custsurname_txt.grid(row=2,column=2,sticky="nw",padx=20,pady=10)
custlocality_lbl.grid(row=3,column=0,sticky="sw",padx=55)
custlocality_txt.grid(row=4,column=0,sticky="nw",padx=20,pady=10)
custstreet_lbl.grid(row=3,column=1,sticky="sw",padx=55)
custstreet_txt.grid(row=4,column=1,sticky="nw",padx=20,pady=10)
custhouseno_lbl.grid(row=3,column=2,sticky="sw",padx=55)
custhouseno_txt.grid(row=4,column=2,sticky="nw",padx=20,pady=10)
custpostcode_lbl.grid(row=5,column=0,sticky="sw",padx=55)
custpostcode_txt.grid(row=6,column=0,sticky="nw",padx=20,pady=10)
custmob_lbl.grid(row=5,column=1,sticky="sw",padx=55)
custmob_txt.grid(row=6,column=1,sticky="nw",padx=20,pady=10)
custemail_lbl.grid(row=5,column=2,sticky="sw",padx=55)
custemail_txt.grid(row=6,column=2,sticky="nw",padx=20,pady=10)
save_btn.grid(row=7, column=0, columnspan=2,sticky="w", pady=20,padx=20)
update_btn.grid(row=7, column=0, columnspan=2, pady=20)
reset_btn.grid(row=7, column=2, columnspan=2,sticky="" ,pady=20)
del_btn.grid(row=7,column=1,columnspan=1,sticky="e",pady=20)
exit_btn.grid(row=7, column=2,sticky="se", columnspan=2, pady=20,padx=20)
search_btn.grid(row=6,column=2,columnspan=1,sticky='s',pady=20,padx=20)

root.mainloop()





