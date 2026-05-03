import mysql.connector
import sys
import tkinter as tk
from my_functions import get_mydb_connect
from my_functions import exit_root
from my_functions import is_numeric
from my_functions import is_integer
from my_functions import is_string
from tkinter import messagebox
import re


#Functions
mydb = get_mydb_connect()


#the data transfer

my_cursor = mydb.cursor()

#number of fields must match the  >>>                                      # Values

upd_product = "UPDATE product SET prod_name = %s, prod_colour = %s, prod_size = %s, prod_qty = %s, prod_sprice =%s WHERE prod_id = %s" 
save_product = "INSERT INTO product(prod_id,supplier_id,prod_name,prod_colour,prod_size,prod_qty,prod_sprice) VALUES(%s,%s,%s,%s,%s,%s,%s)"
del_product = "DELETE FROM product WHERE prod_id = %s"
chk_product = "SELECT * FROM product WHERE prod_id = %s"
chk_supplier = "SELECT * FROM suppliers WHERE supplier_id = %s "
chk_prod_sales = "SELECT * FROM sales WHERE prod_id = %s"



def field_validation():
    prod_id = prodid_var.get().strip()
    supplier_id = supplierid_var.get().strip()
    prod_name = prodname_var.get().strip()
    prod_col = prodcol_var.get().strip()
    prod_size = prodsize_var.get().strip()
    prod_qty = prodqty_var.get().strip()
    prod_s_price = prodsprice_var.get().strip()

    
    error_message = " INVALID: "
    errors = False

    #Not Null#
    missing_field = []
    if not prod_id:
        missing_field.append("Product ID")
    elif not supplier_id:
        missing_field.append("Supplier ID")
    
    if missing_field:
        missing_field_str = ", ".join(missing_field)
        messagebox.showerror("Input Error", f"Please fill in the: {missing_field_str} (Compulsory)")
        return False
    #---#---#---#---#---#
    
    #Proper Name#
    if (prod_name) and (is_string(prod_name) == 0):
        error_message = error_message + " \n Product Name "
        errors = True
        
    #---#---#---#---#---#
        
    #Integer
    if not prod_qty:
        prod_qty = 1  # Default to 1 if empty or invalid
        prodqty_var.set(str(prod_qty))  # Update the field in the form
    
    if is_integer(prod_qty) == -1:
        messagebox.showerror("ERROR", "Product Quantity must be integer")
        errors = True 

        
    #---#---#---#---#---#
        
    #Float
    if prod_s_price:
        if is_numeric(prod_s_price) == -1:
            messagebox.showerror("ERROR", "Product Selling Price")
            errors = True 
            prod_s_price = 0.0
            prodsprice_var.set(f"{prod_s_price:.2f}")
        else:
            default2_price = float(prod_s_price)
             
    else:
        prod_s_price = 0.0
        prodsprice_var.set(f"{prod_s_price:.2f}")
     
    ###Prod Id###
    if prod_id:
        if is_integer(prod_id) == -1:
            error_message += " \n Product ID must be an integer"
            errors = True
        else:
            try:
                my_cursor.execute(chk_product,(prod_id,))
                recordest = my_cursor.fetchall()
                if len(recordest) > 0:
                    messagebox.showerror("ERROR", "The Product ID exists already")
                    return False
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error",f"Error checking Product: {err}")
                return False
    else:
        error_message += " \n Product ID is required"
        errors = True 
    #---#---#---#---#---#
    #Supplier Id
    if supplier_id:
        if is_integer(supplier_id) == -1:
            error_message += " \n Supplier ID must be an integer"
            errors = True
        else:
            try:
                my_cursor.execute(chk_supplier, (supplier_id,))
                recordset = my_cursor.fetchall()
                if len(recordset) == 0:
                    messagebox.showerror("ERROR", "Supplier does not exist")
                    return False
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error checking supplier: {err}")
                return False
    else:
        error_message += " \n Supplier ID is required"
        errors = True

            
    #---#---#---#---#---#   
    #---#---#---#---#---#
        
    if errors:
        messagebox.showerror("Input Error", error_message)
        return False
    #---#---#---#---#---#
    
    #MYSQL EXECUTION
    try:
        my_cursor.execute(save_product,(prod_id,supplier_id,prod_name,prod_col,prod_size,prod_qty,prod_s_price))
        mydb.commit()  
    except mysql.connector.Error as db_err:
        messagebox.showerror("Database Error", f"Failed to insert data into database: {db_err}")
        return False
    else:
        messagebox.showinfo("Success", "Product data saved successfully in the Database.")
    #---#---#---#---#---#
        return True

###~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######~~~######    
    
    
    



def clear_fields():
    prodid_var.set("")
    supplierid_var.set("")
    prodname_var.set("")
    prodcol_var.set("")
    prodsize_var.set("")
    prodqty_var.set("")
    prodsprice_var.set("")
    


def search_product():
    prod_id = prodid_var.get().strip()
    
    if not prod_id:
        messagebox.showerror("ERROR","To Search for your Data, Type in the (PRODUCT ID) the ID")
    else:
        my_cursor.execute(chk_product,(prod_id,))
        recordset = my_cursor.fetchall()
        
        if (len(recordset) > 0):
            for row in recordset:
                prod_id,supplier,prod_name,prod_colour,prod_size,prod_qty,prod_sprice = row
                
                supplierid_var.set(supplier)
                prodname_var.set(prod_name)
                prodcol_var.set(prod_colour)
                prodsize_var.set(prod_size)
                prodqty_var.set(prod_qty)
                prodsprice_var.set(prod_sprice)
                update_btn.config(state=tk.NORMAL)

        else:
            update_btn.config(state=tk.DISABLED)
            messagebox.showerror("INVALID","Product ID was not found")
            clear_fields()
       

        
        
    
def prod_id_changed(event):
    update_btn.config(state=tk.DISABLED)



def update_product():
    prod_id = prodid_var.get().strip()
    prod_name = prodname_var.get().strip()
    prod_col = prodcol_var.get().strip()
    prod_size = prodsize_var.get().strip()
    prod_qty = prodqty_var.get().strip()
    prod_s_price = prodsprice_var.get().strip()
    
    response = messagebox.askyesno("Update","Are you sure you want to update this information")
    if(response == True):
        my_cursor.execute(upd_product,(prod_name,prod_col,prod_size,prod_qty,prod_s_price,prod_id,))
        mydb.commit()
        messagebox.showinfo("Update",f"{prod_id} was successfuly updated")
    else:
        messagebox.showinfo("Update","Successfully canceled updation")
    



def delete_product():
    prod_id = prodid_var.get().strip()
    
    if not prod_id:
        messagebox.showerror("ERROR","To delete a product please enter the product id")
        return False
    
    if is_integer(prod_id) == -1:
        messagebox.showerror("ERROR","The Product ID must be an integer")
        return False
    try:
        my_cursor.execute(chk_product,(prod_id,))
        prod_record = my_cursor.fetchall()
        if len(prod_record) == 0:
            messagebox.showerror("ERROR","The Product ID does not exist")
            return False
        
        my_cursor.execute(chk_prod_sales,(prod_id,))
        sales_record = my_cursor.fetchall()
        if len(sales_record) > 0:
            messagebox.showerror("ERROR","The Product ID Exists in the Sales table")
            return False 
        
        response = messagebox.askyesno("Confirm Deletion",f"Are you sure you want to delete {prod_id}?")
        if(response == True):
            my_cursor.execute(del_product,(prod_id,))
            mydb.commit()
            messagebox.showinfo("Success",f"The {prod_id} was successfully deleted")
        else:
            messagebox.showinfo("Aborted","You successfully canceled the deletion")
            
            
    except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error checking product: {err}")
                return False



def save_detail():
    if field_validation():
        clear_fields()
        root.destroy()


##### ----- VARS LIMITS ----- #####


def prod_size_limit_uppercase(*args):
    size_input = prodsize_var.get().strip().upper()
    prodsize_var.set(size_input)
    
    if len(size_input) > 3:
        size_input = size_input[:3]  
    
    prodsize_var.set(size_input)


def prod_id_limit(*args):
    prod_id = prodid_var.get().strip()
    prodid_var.set(prod_id)
    
    if len(prod_id) > 10:
        prod_id = prod_id[:10]
    
    prodid_var.set(prod_id)


def supplier_limit(*args):
    supplier_id = supplierid_var.get().strip()
    supplierid_var.set(supplier_id)
    
    if len(supplier_id) > 10:
        supplier_id = supplier_id[:10]
    
    supplierid_var.set(supplier_id)
  
  
    
def prod_name_limit(*args):
    prod_name = prodname_var.get()
    prodname_var.set(prod_name)
    
    if len(prod_name) > 25:
        prod_name = prod_name[:25]
        
    prodname_var.set(prod_name)
    
    
    
def prod_colour_limit(*args):
    prod_colour = prodcol_var.get()
    prodcol_var.set(prod_colour)
    
    if len(prod_colour) > 15:
        prod_colour = prod_colour[:15]
        
    prodcol_var.set(prod_colour)
    
        

##### ----- ----- #####
    



#window
root = tk.Tk()
root.geometry("1080x720")
root.resizable(False,False)
root.title("Sport MD")
root.iconbitmap("images\Logo.ico")
#---#---#







#variables
prodid_var = tk.StringVar()
supplierid_var = tk.StringVar()
prodname_var = tk.StringVar()
prodcol_var = tk.StringVar()
prodsize_var = tk.StringVar()
prodqty_var = tk.StringVar()
prodqty_var.set(1)
prodsprice_var = tk.StringVar()
prodsprice_var.set(0.00)
#---#---#
#vars with setup
prodsize_var.trace("w" , prod_size_limit_uppercase)
prodid_var.trace("w", prod_id_limit)
supplierid_var.trace("w", supplier_limit)
prodname_var.trace("w", prod_name_limit)
prodcol_var.trace("w", prod_colour_limit)




#---#---#

#fonts
title_font = ("Arial",18)
default_font = ("Arial",14)
button_font = ("Courier New",14) 
#---#---#





#labels
screen_title_lbl = tk.Label(root,text="PRODUCT TABLE",font=title_font,fg="#FFFFFF",bg="#666699")
prodid_lbl = tk.Label(root,text="Product ID*",font=default_font)
supplierid_lbl = tk.Label(root,text="Supplier ID*",font=default_font)
prodname_lbl = tk.Label(root,text="Product Name",font=default_font)
prodcol_lbl = tk.Label(root,text="Product Color",font=default_font)
prodsize_lbl = tk.Label(root,text="Product Size",font=default_font)
prodqty_lbl = tk.Label(root,text="Product Quantity",font=default_font)
prodsprice_lbl = tk.Label(root,text="Product Selling Price",font=default_font)
#---#---#


#entry boxes
prodid_txt = tk.Entry(root,textvariable=prodid_var,font=default_font)
prodid_txt.bind("<KeyRelease>",prod_id_changed)
supplierid_txt = tk.Entry(root,textvariable=supplierid_var,font=default_font)
prodname_txt = tk.Entry(root,textvariable=prodname_var,font=default_font)
prodcol_txt = tk.Entry(root,textvariable=prodcol_var,font=default_font)
prodsize_txt = tk.Entry(root,textvariable=prodsize_var,font=default_font)
prodqty_txt = tk.Entry(root,textvariable=prodqty_var,font=default_font)
prodsprice_txt = tk.Entry(root,textvariable=prodsprice_var,font=default_font)
#---#---#


#buttons
save_btn = tk.Button(root,text="Save Details",command=save_detail,font=button_font,fg="white",bg="green")
reset_btn = tk.Button(root,text="Reset Details",command=clear_fields,font=button_font)
exit_btn = tk.Button(root,text="EXIT",command=exit_root,font=button_font,fg="white",bg="red")
del_btn = tk.Button(root,text="Delete Product Details",command=delete_product,font=button_font,fg="red")
update_btn = tk.Button(root,text="Update Details",command=update_product,font=button_font,fg="blue")
update_btn.config(state=tk.DISABLED)
search_btn = tk.Button(root,text="Search (ID)",command=search_product,font=button_font,fg="green")
#---#---#

#grid layout
root.columnconfigure((0,2),weight=1)
root.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
#---#---#

#the grid

screen_title_lbl.grid(row=0,columnspan=3,sticky="we")
prodid_lbl.grid(row=1,column=0,sticky="sw",padx=55)
prodid_txt.grid(row=2,column=0,sticky="nw",padx=20,pady=10)
supplierid_lbl.grid(row=1,column=1,sticky="sw",padx=55)
supplierid_txt.grid(row=2,column=1,sticky="nw",padx=20,pady=10)
prodname_lbl.grid(row=1,column=2,sticky="sw",padx=55)
prodname_txt.grid(row=2,column=2,sticky="nw",padx=20,pady=10)
prodcol_lbl.grid(row=3,column=0,sticky="sw",padx=55)
prodcol_txt.grid(row=4,column=0,sticky="nw",padx=20,pady=10)
prodsize_lbl.grid(row=3,column=2,sticky="sw",padx=55)
prodsize_txt.grid(row=4,column=2,sticky="nw",padx=20,pady=10)
prodqty_lbl.grid(row=5,column=0,sticky="sw",padx=55)
prodqty_txt.grid(row=6,column=0,sticky="nw",padx=20,pady=10)
prodsprice_lbl.grid(row=5,column=2,sticky="sw",padx=55)
prodsprice_txt.grid(row=6,column=2,sticky="nw",padx=20,pady=10)
save_btn.grid(row=7, column=0, columnspan=1, pady=20)
reset_btn.grid(row=7, column=2, columnspan=1, pady=20)
update_btn.grid(row=7, column=1, columnspan=1, pady=20)
search_btn.grid(row=4,column=1,pady=20)
del_btn.grid(row=6,column=1,columnspan=1,pady=20,padx=20)
exit_btn.grid(row=7, column=2,sticky="se", columnspan=2, pady=20,padx=20)






root.mainloop()











