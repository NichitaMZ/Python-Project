import mysql.connector
import sys
import tkinter as tk
from my_functions import is_integer
from my_functions import is_empty
from my_functions import get_mydb_connect
from my_functions import exit_root
from my_functions import is_numeric
from my_functions import is_string
from tkinter import messagebox
import re
from datetime import date


mydb = get_mydb_connect()
my_cursor = mydb.cursor()






def clear_sale_vars():
    sale_id.set(0)
    custid_var.set("")
    custname_var.set("")
    totalsale_var.set(0.00)


def remove_sale_items():
    global rows
    
    for row in rows:
        row['prod_id'].set("")
        row['prod_name'].set("")
        row['prod_sprice'].set(0.00)
        row['sale_qty'].set(1)
        row['total_unit'].set(0.00)
        
        for row in rows:
            row['row_frame'].destroy() #removes the row frame widget
             
    rows.clear()



def save_sale():
    if len(rows) > 0 and not(is_empty(custid_var.get())): #checks if there is something in the canvas and the custid is not empty
        try:
            for row in rows:
                sal_id = new_sale_id.get()
                sdate = sale_date.get()
                customer = custid_var.get()
                prod_id = row['prod_id'].get()
                qty = int(row['sale_qty'].get())
                
                my_cursor.execute(save_sql,(sal_id,sdate,customer,prod_id,qty)) # inserts the data from table to sql
                
                my_cursor.execute(update_qty_sql, (qty,prod_id)) #changes the prod_qty
                
            mydb.commit()
            messagebox.showinfo("Success","Sale was saved successfully!!")
            new_sale_id.set("#")
            sale_date.set("")
            custid_var.set("")
            custid_txt.configure(state='readonly')
            custname_var.set("")
            totalsale_var.set(0.00)
            remove_sale_items()
        except Exception as e:
            mydb.rollback()
            messagebox.showerror("Error",f"An error occured: {str(e)}")
    else:
        messagebox.showerror("SAVE ERROR","Check The Sale Details Requirments")
        


def prod_id_focusout(event,item_vars):
    prod_id = item_vars['prod_id'].get()
    if(is_empty(prod_id) == False ):
        if not(current_item.get() == item_vars['prod_id'].get()): # to match the old with new id 
            if prod_exists(item_vars) == True:# if it is valid
                items_in_sale.discard(current_item.get()) #removes the old code from the set
                if(prod_already_in_sale(item_vars) == False ):#  the code is valid and it is not in the sale
                    items_in_sale.add(prod_id)
                    rows.append(item_vars) # connects the rows with the dict. vars
                    update_total_unit(item_vars)
                else:#if the id exists in sales
                    messagebox.showerror("ERORR","Product ID already has a Sale")
                    item_vars['row_frame'].destroy()
                    update_total_unit(item_vars)
            else:
                messagebox.showerror("ERORR","The Product ID doesn't exists")
                item_vars['row_frame'].destroy()
                update_total_unit(item_vars)
    else:
        item_vars['row_frame'].destroy()

    


def update_total_sale():
    global rows
    
    total = 0.0
    
    for row in rows:
        total += float(row['total_unit'].get())
    
    totalsale_var.set(total)



def update_total_unit(item_vars):
    
    price = item_vars['prod_sprice'].get()
    qty = item_vars['sale_qty'].get()
    total = price * qty
    
    item_vars['total_unit'].set(total)
    
    update_total_sale()
    


def chk_qty_level(prod_entered,sale_qty_entered):
    
    my_cursor.execute(chk_stock_level,(prod_entered,)) #checks the quantity in prod table
    recordset = my_cursor.fetchall()
    get_record_qty = recordset[0]
    qty_in_stock = get_record_qty[0]
    
    if(qty_in_stock < sale_qty_entered):
        messagebox.showerror("ERROR","Insufficient stock level")
        return True #the sale qty exceeded
    else:
        return False
    







def sale_qty_changed(event,item_vars):
    prod_id = item_vars['prod_id'].get()
    
    try:
        qty = item_vars['sale_qty'].get()
    except (tk.TclError,ValueError): # to get both possibles errors
        qty = 0
    
    if not(qty <=0 ):
        low_chk = chk_qty_level(prod_id,qty)
        
        if(low_chk == True):
            item_vars['sale_qty'].set(1)
            update_total_unit(item_vars)
        else:
            #item_vars['sale_qty'].set(1)  # if sale_qty = 0
            update_total_unit(item_vars)
    

def custid_changed(event): #detects the cursor moving out of the entry box
    cust_exists(custid_var.get())


def prod_id_click(event,item_vars):# to detect the data that was typed in
    prod_id = item_vars['prod_id'].get()
    if(is_empty(prod_id) == False):
        response = messagebox.askyesno("Changes Applied","Do you want to update the Product ID?")
        if response == True:
            current_item.set(prod_id)
        else:
            return True




def prod_exists(item_vars):
    prod_entered = item_vars['prod_id'].get() #prod_id is a key
    
    my_cursor.execute(chk_prod,(prod_entered,))
    recordset = my_cursor.fetchall()
    
    if len(recordset) > 0 :
        get_record = recordset[0]
        item_vars['prod_name'].set(get_record[1]) #gets the [1] second record in mysql the prod_name
        item_vars['prod_sprice'].set(get_record[2]) #get the [2] third record from mysql
        
        update_total_unit(item_vars)
        
        return True
    
    else:
        
        return False


def prod_already_in_sale(item_vars):
    if(item_vars['prod_id'].get() in items_in_sale): #using lists for no dublicates
        return True
    else:
        return False 




def configure_canvas(event):
    #adjust the scroll frame to match internal area of the scrollable frame
    canvas.configure(scrollregion=canvas.bbox("all"))



def cust_exists(cust_entered):
    if(not(is_empty(cust_entered))):
        my_cursor.execute(chk_customer,(cust_entered,))
        recordset = my_cursor.fetchall()
        
        if len(recordset) > 0 :
            get_record = recordset[0]
            
            name = get_record[1] #the name of field 0 = id, 1 = name and 2 = surname
            
            surname = get_record[2]
            
            custname_var.set(name + " " + surname)
            
        else:
            custid_var.set("Generic")
            custname_var.set("N/A")
    else:
        custid_var.set("Generic")
        custname_var.set("N/A")
 
 

 
 
def new_sale():
    global rows
    
    clear_sale_vars() # clears the variables data
    items_in_sale.clear() #removes all the items in the set
    custid_txt.configure(state="normal")
    my_cursor.execute(get_last_sale)
    recordset = my_cursor.fetchall()
    
    if (recordset == 0):   # if no records
        remove_sale_items()
        new_sale_id.set(1)
        add_item_btn.configure(state='normal')
        save_sale_btn.configure(state='normal')
    else:                                           # if there is get the last sale and add 1
        remove_sale_items()
        get_record = recordset[0]
        sale_id = get_record[0]
        new_sale_id.set(sale_id+1)
        sale_date.set(today)
    
        add_item_btn.configure(state="normal")
        save_sale_btn.configure(state="normal")




def add_item(): # will show the prod fields to add items in the canvas frame
    row_item = tk.Frame(scroll_frame)
    row_item.pack(fill="x",pady=5)
    
    item_vars ={
        'prod_id':tk.StringVar(),
        'prod_name':tk.StringVar(),
        'prod_sprice':tk.DoubleVar(),
        'sale_qty':tk.IntVar(),
        'total_unit':tk.DoubleVar(),
        'row_frame':row_item #for easy removal
    }
    
    item_vars['sale_qty'].set(1)  #sale default value
    
    prod_id_lbl = tk.Label(row_item,text="Product ID")
    prod_id_lbl.grid(row=0,column=0,padx=2)
    
    prod_id_txt = tk.Entry(row_item,textvariable=item_vars['prod_id'],width=10,)
    prod_id_txt.bind("<FocusOut>",lambda e:prod_id_focusout(e,item_vars))
    prod_id_txt.bind("<Button-1>",lambda e:prod_id_click(e,item_vars))
    prod_id_txt.grid(row=1,column=0,padx=2)
    
    prod_name_lbl = tk.Label(row_item,text="Product Name")
    prod_name_lbl.grid(row=0,column=1,padx=2)
    
    prod_name_txt = tk.Entry(row_item,textvariable=item_vars['prod_name'],width=10,state='readonly')
    prod_name_txt.grid(row=1,column=1,padx=2)
    
    prod_sprice_lbl = tk.Label(row_item,text="Product Price")
    prod_sprice_lbl.grid(row=0,column=2,padx=2)
    
    prod_sprice_txt = tk.Entry(row_item,textvariable=item_vars['prod_sprice'],width=10,state='readonly')
    prod_sprice_txt.grid(row=1,column=2,padx=2)
    
    sale_qty_lbl = tk.Label(row_item,text="Quantity")
    sale_qty_lbl.grid(row=0,column=3,padx=2)
    
    sale_qty_txt = tk.Entry(row_item,textvariable=item_vars['sale_qty'],width=3)
    sale_qty_txt.grid(row=1,column=3,padx=2)
    sale_qty_txt.bind("<FocusOut>",lambda e:sale_qty_changed(e,item_vars))
    
    total_unit_lbl = tk.Label(row_item,text="Total Unit")
    total_unit_lbl.grid(row=0,column=4,padx=2)
    
    total_unit_txt = tk.Entry(row_item,textvariable=item_vars['total_unit'],width=7,state='readonly')
    total_unit_txt.grid(row=1,column=4,padx=2)
    
    




root = tk.Tk()
root.geometry("700x600")
root.resizable(False,False)
root.title("Sport MD")
root.iconbitmap("images\Logo.ico")



#sql
get_last_sale = "SELECT * FROM sales ORDER BY sale_id DESC LIMIT 1"
chk_customer = "SELECT cust_id,cust_name,cust_surname FROM customer WHERE cust_id = %s"
chk_prod = "SELECT prod_id,prod_name,prod_sprice FROM  product WHERE prod_id = %s"
chk_stock_level = "SELECT prod_qty FROM product WHERE prod_id = %s"
save_sql = "INSERT INTO sales(sale_id,sale_date,cust_id,prod_id,sale_qty) VALUES(%s,%s,%s,%s,%s)"

#deletes the prod_qty after a sale is saved
update_qty_sql = "UPDATE product SET prod_qty = prod_qty - %s WHERE prod_id = %s"

#fonts
title_font = ("Arial",18)
default_font = ("Arial",14)
button_font = ("Courier New",14)     



#variable
current_item = tk.StringVar() #to store the old id before changing it
items_in_sale = set()
new_sale_id = tk.IntVar()
new_sale_id.set("#")
today = date.today()
sale_date = tk.StringVar()
sale_date.set(today)


sale_id = tk.IntVar()
custid_var = tk.StringVar()
custname_var = tk.StringVar()
totalsale_var = tk.DoubleVar()


prod_sec = tk.Frame(root) #Create frame
canvas = tk.Canvas(prod_sec,height=150)
prod_scroll = tk.Scrollbar(prod_sec,orient='vertical',command=canvas.yview)
scroll_frame = tk.Frame(canvas)
canvas.create_window((0,0),window=scroll_frame,anchor="nw")

# reminder: rows[] is a global variable list
rows = [] #il lists for items on the canvas


#labels
title_lbl = tk.Label(root,text="SPORTMD SALES SCREEN",font=title_font,bg="#FFFF3F")
custid_lbl = tk.Label(root,text="Customer ID",font=default_font)
custname_lbl = tk.Label(root,text="Customer Name",font=default_font)
saledate_lbl = tk.Label(root,text="Sale Date",font=default_font)
saleid_lbl = tk.Label(root,text="Sale ID",font=default_font)
totalsale_lbl = tk.Label(root,text="Total Sale",font=default_font)


#entry boxes
custid_txt = tk.Entry(root,textvariable=custid_var,width=20,state='readonly')
custid_txt.bind("<FocusOut>",custid_changed)
custname_txt = tk.Entry(root,textvariable=custname_var,width=20,state='readonly')
saleid_txt = tk.Entry(root,textvariable=new_sale_id,width=20,state='readonly')
saledate_txt = tk.Entry(root,textvariable=sale_date,width=20,state='readonly')
totalsale_txt = tk.Entry(root,textvariable=totalsale_var,width=20,state='readonly')

#buttons

new_salebtn = tk.Button(root,text="New Sale",font=button_font,command=new_sale)
exit_btn = tk.Button(root,text="Exit",font=button_font,command=exit_root)
add_item_btn = tk.Button(root,text="Add item",font=button_font,command=add_item,state='disabled')
save_sale_btn = tk.Button(root,text="Save Sale",font=button_font,command=save_sale,state='disabled')

#grid

title_lbl.grid(row=0,columnspan=3,padx=180,)
saleid_lbl.grid(row=1,column=0,sticky="sw")
saleid_txt.grid(row=2,column=0,sticky="nw")
saledate_lbl.grid(row=1,column=1,sticky="sw")
saledate_txt.grid(row=2,column=1,sticky="nw")
custid_lbl.grid(row=3,column=0,sticky="sw")
custid_txt.grid(row=4,column=0,sticky="nw")
custname_lbl.grid(row=3,column=1,sticky="sw")
custname_txt.grid(row=4,column=1,sticky="nw")
totalsale_lbl.grid(row=6,column=2,sticky="sw")
totalsale_txt.grid(row=7,column=2,sticky="nw")

new_salebtn.grid(row=7,column=0,sticky="sw")
exit_btn.grid(row=9,column=1,sticky="sw")
add_item_btn.grid(row=8,column=0,sticky="sw")
save_sale_btn.grid(row=7,column=1,sticky="nw")

#placing the scroll section
prod_sec.grid(row=5,column=0,columnspan=3,padx=10,pady=10)
canvas.pack(side="left",fill="both",expand=True)
prod_scroll.pack(side="right",fill="y")
canvas.configure(yscrollcommand=prod_scroll.set)
scroll_frame.bind("<Configure>",configure_canvas)


root.mainloop()











