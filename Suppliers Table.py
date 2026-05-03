import mysql.connector
import sys
import tkinter as tk
from my_functions import get_mydb_connect
from my_functions import exit_root
from my_functions import is_valid_email
from my_functions import is_numeric
from my_functions import is_integer
from my_functions import is_string
from tkinter import messagebox
import re



mydb = get_mydb_connect()
my_cursor = mydb.cursor()

upd_supplier = "UPDATE suppliers SET supplier_name = %s, supplier_country = %s, supplier_email = %s, supplier_contact_no = %s WHERE supplier_id = %s" 
save_supplier = "INSERT INTO suppliers (supplier_id,supplier_name,supplier_country,supplier_email,supplier_contact_no) VALUES(%s,%s,%s,%s,%s)"
chk_supplier = "SELECT * FROM suppliers WHERE supplier_id = %s"
del_supplier = "DELETE FROM suppliers WHERE supplier_id = %s"
chk_prod_supplier = "SELECT * FROM product WHERE supplier_id = %s"

###MAIN FUNCTION###
def field_validation():
    supp_id = supplierid_var.get().strip()
    supp_email = supplieremail_var.get().strip()
    supp_mob = suppliercontact_no_var.get().strip()
    supp_country = suppliercountry_var.get()
    supp_name = suppliername_var.get()

    error_message = "INVALID:"
    errors = False 
    
    missing_fields = []
    
    ###SUPPLIER ID NN###
    if not supp_id:
        missing_fields.append("Supplier ID")
    ###~~~###~~~###~~~###    
    if missing_fields:
        messagebox.showerror("INVALID", f"Please fill in the following required fields: {', '.join(missing_fields)}.")
        return False
    ###~~~###~~~###~~~###
    if supp_name:
        if not is_string(supp_name):
            error_message += " \n Supplier Name"
            errors = True
            
    if supp_id:
        if is_integer(supp_id) == -1:
            error_message += "\n Supplier ID (integer)"
            errors = True
        else:
            try:
                my_cursor.execute(chk_supplier,(supp_id,))
                recordset = my_cursor.fetchall()
                if len(recordset) > 0 :
                    messagebox.showerror("ERROR", "Supplier ID already exists")
                    return False
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",f"Error checking Product: {err}")
                return False
    
    if supp_email:
        if not is_valid_email(supp_email):
            error_message += " \n Supplier Email"
            errors = True
     
    
    
    if errors:
        messagebox.showerror("Input Error", error_message)
        return False
    
    
    


    #MYSQL EXECUTION
    try:
        my_cursor.execute(save_supplier,(supp_id,supp_name,supp_country,supp_email,supp_mob))
        mydb.commit()  # Make sure to commit the transaction to save changes
    except mysql.connector.Error as db_err:
        messagebox.showerror("Database Error", f"Failed to insert data into database: {db_err}")
        return False
    else:
        messagebox.showinfo("Success", "Supplier data saved successfully in the Database.")
    #---#---#---#---#---#
        return True
    
#Functions
def clear_fields():
    supplierid_var.set("")
    suppliercontact_no_var.set("")
    suppliercountry_var.set("")
    supplieremail_var.set("")
    suppliername_var.set("")


def search_supplier():
    supplier_id = supplierid_var.get().strip()
    
    if not supplier_id:
        messagebox.showerror("ERROR","To Search for your Data, Type in the (SUPPLIER ID) the ID")
    else:
        my_cursor.execute(chk_supplier,(supplier_id,))
        recordset = my_cursor.fetchall()
        
        if (len(recordset) > 0):
            for row in recordset:
                supp_id,supp_name,supp_country,supp_email,supp_mob = row
                
                supplierid_var.set(supp_id)
                suppliername_var.set(supp_name)
                suppliercountry_var.set(supp_country)
                supplieremail_var.set(supp_email)
                suppliercontact_no_var.set(supp_mob)
                update_btn.config(state=tk.NORMAL)

        else:
            update_btn.config(state=tk.DISABLED)
            messagebox.showerror("INVALID","Supplier ID was not found")
            clear_fields()


def update_supplier():
    supp_id = supplierid_var.get().strip()
    supp_name = suppliername_var.get().strip()
    supp_country = suppliercountry_var.get().strip()
    supp_email = supplieremail_var.get().strip()
    supp_mob = suppliercontact_no_var.get().strip()
    
    response = messagebox.askyesno("Update","Are you sure you want to update this information")
    if(response == True):
        my_cursor.execute(upd_supplier,(supp_name,supp_country,supp_email,supp_mob,supp_id,))
        mydb.commit()
        messagebox.showinfo("Update",f"The supplier: {supp_id} was successfuly updated")
    else:
        messagebox.showinfo("Update","Successfully canceled updation")



def delete_supplier():
    supplier_id = supplierid_var.get().strip()
    
    if not supplier_id:
        messagebox.showerror("ERROR","To delete a supplier please enter the supplier id")
        return False
    
    if is_integer(supplier_id) == -1:
        messagebox.showerror("ERROR","The Supplier ID must be an integer")
        return False
    try:
        my_cursor.execute(chk_supplier,(supplier_id,))
        supp_record = my_cursor.fetchall()
        if len(supp_record) == 0:
            messagebox.showerror("ERROR","The Supplier ID does not exist")
            return False
        
        my_cursor.execute(chk_prod_supplier,(supplier_id,))
        sales_record = my_cursor.fetchall()
        if len(sales_record) > 0:
            response = messagebox.askyesno("Confirm Deletion",f"This supplier is linked to a product. Are you sure you want to delete {supplier_id}?")
            if(response == True):
                my_cursor.execute(del_supplier,(supplier_id,))
                mydb.commit()
                messagebox.showinfo("Success",f"The {supplier_id} was successfully deleted")
            else:
                messagebox.showinfo("Aborted","You successfully canceled the deletion")
                return False #to stop here 
        
        response = messagebox.askyesno("Confirm Deletion",f"Are you sure you want to delete {supplier_id}?")
        if(response == True):
            my_cursor.execute(del_supplier,(supplier_id,))
            mydb.commit()
            messagebox.showinfo("Success",f"The {supplier_id} was successfully deleted")
        else:
            messagebox.showinfo("Aborted","You successfully canceled the deletion")
    
    except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error checking supplier: {err}")
                return False



def save_detail():
    if field_validation():
        messagebox.showinfo("Success", "Customer information saved successfully!")
        clear_fields()
        root.destroy()




#window
root = tk.Tk()
root.geometry("1080x720")
root.resizable(False,False)
root.title("Sport MD")
root.iconbitmap("images\Logo.ico")
#---#---#







#variables
supplierid_var = tk.StringVar()
suppliername_var = tk.StringVar()
suppliercountry_var = tk.StringVar()
supplieremail_var = tk.StringVar()
suppliercontact_no_var = tk.StringVar()
#---#---#



#fonts
title_font = ("Arial",18)
default_font = ("Arial",14)
button_font = ("Courier New",14) 
#---#---#





#labels
screen_title_lbl = tk.Label(root,text="SUPPLIER TABLE",font=title_font,fg="white",bg="orange")
supplierid_lbl = tk.Label(root,text="Supplier ID*",font=default_font)
suppliername_lbl = tk.Label(root,text="Supplier Name",font=default_font)
suppliercountry_lbl = tk.Label(root,text="Supplier Country",font=default_font)
supplieremail_lbl = tk.Label(root,text="Supplier Email",font=default_font)
suppliercontact_no_lbl = tk.Label(root,text="Supplier's Contact Number",font=default_font)
#---#---#


#entry boxes
supplierid_txt = tk.Entry(root,textvariable=supplierid_var,font=default_font)
suppliername_txt = tk.Entry(root,textvariable=suppliername_var,font=default_font)
suppliercountry_txt = tk.Entry(root,textvariable=suppliercountry_var,font=default_font)
supplieremail_txt = tk.Entry(root,textvariable=supplieremail_var,font=default_font)
suppliercontact_no_txt = tk.Entry(root,textvariable=suppliercontact_no_var,font=default_font)
#---#---#


#buttons
save_btn = tk.Button(root,text="Save Details",command=save_detail,font=button_font,fg="white",bg="green")
reset_btn = tk.Button(root,text="Reset Details",command=clear_fields,font=button_font)
exit_btn = tk.Button(root,text="EXIT",command=exit_root,font=button_font,fg="white",bg="red")
del_btn = tk.Button(root,text="Delete Suppliers Details",command=delete_supplier,font=button_font,fg="red")
update_btn = tk.Button(root,text="Update Details",command=update_supplier,font=button_font,fg="blue",state="disabled")
search_btn = tk.Button(root,text="Search Details",command=search_supplier,font=button_font,bg="light green")
#---#---#

#grid layout
root.columnconfigure((0,2),weight=1)
root.rowconfigure((0,1,2,3,4,5,6),weight=1)
#---#---#

#the grid
screen_title_lbl.grid(row=0,columnspan=3,sticky="we")
supplierid_lbl.grid(row=1,column=0,sticky="sw",padx=20,pady=10)
supplierid_txt.grid(row=2,column=0,sticky="nw",padx=10)
suppliername_lbl.grid(row=1,column=0,sticky="se",padx=20,pady=10)
suppliername_txt.grid(row=2,column=0,sticky="ne",padx=10)
suppliercountry_lbl.grid(row=3,column=0,sticky="sw",padx=20,pady=10)
suppliercountry_txt.grid(row=4,column=0,sticky="nw",padx=10)
suppliercontact_no_lbl.grid(row=3,column=0,sticky="se",padx=20,pady=10)
suppliercontact_no_txt.grid(row=4,column=0,sticky="ne",padx=10)
supplieremail_lbl.grid(row=5,column=0,sticky="s",padx=20)
supplieremail_txt.grid(row=6,column=0,sticky="we",padx=10,pady=30)

save_btn.grid(row=1,column=2,sticky="n")
del_btn.grid(row=2,column=2,sticky="n")
search_btn.grid(row=3,column=2,sticky="s")
update_btn.grid(row=5,column=2,sticky="n")
reset_btn.grid(row=6,column=2,sticky="n")
exit_btn.grid(row=6,column=2,sticky="se",pady=10,padx=10)

root.mainloop()






















