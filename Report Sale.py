import tkinter as tk
from my_functions import is_integer #from file import the function
from my_functions import is_numeric
from my_functions import is_empty
from tkinter import messagebox
from my_functions import exit_root
from my_functions import get_mydb_connect
from datetime import date
 
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Spacer
import os


def clear_data():
    global rows
    sale_id.set("")
    sale_date.set("dd/mm/yyyy")
    cust_id.set("")
    cust_name.set("")
    total_sale.set(0.00)
    for row in rows:
        row['prod_code'].set("")
        row['prod_desc'].set("")
        row['prod_price'].set(0.00)
        row['sale_qty'].set(1)
        row['total_unit'].set(0.00)
        # Clear all rows
        for row in rows:
            row['row_frame'].destroy()  # Destroy the frame widget
    rows.clear()  # Clear the list for the new sale

    sale_id_txt.configure(state="normal")
    print_sale_btn.configure(state="disabled")

 
def update_total_unit(item_vars):
    price = item_vars['prod_price'].get()
    qty = item_vars['sale_qty'].get()
    total = price * qty
    item_vars['total_unit'].set(total)
    update_total_sale()
 
 
def update_total_sale():
    global rows
    total = 0.0
    for row in rows:
        total += float(row['total_unit'].get())
    total_sale.set(total)

def find_sale(event):
 
    global rows

    sale = sale_id.get()
    my_cursor.execute(find_sale_no, (sale,))
    recordset = my_cursor.fetchall()
 
    if len(recordset) > 0:
        sale_id_txt.configure(state="disabled")
        print_sale_btn.configure(state="normal")
        #why converting recordset (which is a list of tuples) to a list of dictionaries.
        for row in recordset:
            row_item = tk.Frame(scroll_frame) #a frame is created in each loop
            row_item.pack(fill="x",pady=5)
            rows.append({
                "sale_id": row[0],
                "sale_date": row[1],
                "cust_id": row[2],
                "prod_code": tk.StringVar(value=row[3]),
                "sale_qty": tk.IntVar(value=row[4]),
                "cust_name": row[5],
                "cust_surname": row[6],
                "prod_desc": tk.StringVar(value=row[7]),
                "prod_price": tk.DoubleVar(value=row[8]),
                'total_unit':tk.DoubleVar(),
                'row_frame': row_item #each row will have it's own frame IMP
            })
 
        for i,row in enumerate(rows):
            sale_date.set(row['sale_date'])
            cust_id.set(row['cust_id'])
            cust_name.set(row['cust_name'] + " " + row['cust_surname'])
            #row_item = tk.Frame(scroll_frame)
            #row_item.pack(fill="x",pady=5)
            prod_code_lbl = tk.Label(row['row_frame'],text="Product Code")
            prod_code_lbl.grid(row=0,column=0,padx=2)
            prod_code_txt = tk.Entry(row['row_frame'],textvariable=row['prod_code'],width=10,state="readonly")    
            prod_code_txt.grid(row=1,column=0,padx=2)
            prod_desc_lbl = tk.Label(row['row_frame'],text="Description")
            prod_desc_lbl.grid(row=0,column=1,padx=2)
            prod_desc_txt = tk.Entry(row['row_frame'],textvariable=row['prod_desc'],width=20,state="readonly")
            prod_desc_txt.grid(row=1,column=1,padx=2)
            prod_price_lbl = tk.Label(row['row_frame'],text="Price")
            prod_price_lbl.grid(row=0,column=2,padx=2)
            prod_price_txt = tk.Entry(row['row_frame'],textvariable=row['prod_price'],width=7,state="readonly")
            prod_price_txt.grid(row=1, column=2, padx=2)
            sale_qty_lbl = tk.Label(row['row_frame'],text="Quantity")
            sale_qty_lbl.grid(row=0,column=3,padx=2)
            sale_qty_txt = tk.Entry(row['row_frame'],textvariable=row['sale_qty'],width=4,state="readonly")
            sale_qty_txt.grid(row=1,column=3,padx=2)
            total_unit_lbl = tk.Label(row['row_frame'],text="Total Unit")
            total_unit_lbl.grid(row=0,column=4,padx=2)
            total_unit_txt = tk.Entry(row['row_frame'],textvariable=row['total_unit'], width=7,state="readonly")
            total_unit_txt.grid(row=1,column=4,padx=2)
            row['total_unit'].set(row['prod_price'].get()*row['sale_qty'].get())
            update_total_sale()
    else:
        messagebox.showerror("Sale No Error","Sale number does not exist")
        print_sale_btn.configure(state="disabled")
        clear_data()

 
def print_pdf():
    # initialising the file
    pdf_name = "Sales_Report"+str(sale_id.get())+".pdf" #sale number is added to the file
    doc = SimpleDocTemplate(pdf_name, pagesize=A4)
    elements = []
    # Styles to be used in the report
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
     # **Retrieve Sale Details**
    sale_id_value = sale_id.get()
    sale_date_value = sale_date.get()
    cust_id_value = cust_id.get()
    cust_name_value = cust_name.get()
    #Headings Report
    elements.append(Paragraph(f"Sales Report - Sale No: {sale_id_value}", title_style))
    elements.append(Spacer(1, 10 * mm))  #10mm space
    elements.append(Paragraph(f"Date: <b>{sale_date_value}</b>", normal_style))
    elements.append(Paragraph(f"Customer ID: <b>{cust_id_value}</b>", normal_style))
    elements.append(Paragraph(f"Customer Name: <b>{cust_name_value}</b>",normal_style))
    #elements.append(Paragraph(" ", normal_style))  #space before adding the tabular sale items
    elements.append(Spacer(1, 10 * mm))  # 10mm space before the table

     #Extract Sale Items and set table headers
    table_data_list = [["Product Code", "Description", "Price", "Quantity", "Total Unit"]]
    for row in rows:  # Iterate through your sale items
        prod_code = row['prod_code'].get()
        prod_desc = row['prod_desc'].get()
        prod_price = row['prod_price'].get()
        sale_qty = row['sale_qty'].get()
        total_unit = row['total_unit'].get()
        # Append data to the table
        table_data_list.append([prod_code, prod_desc, f"€{prod_price:.2f}", sale_qty, f"€{total_unit:.2f}"])
         # **Create Table**
    table = Table(table_data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10 * mm))  # 10mm space
    elements.append(Paragraph(f'<para alignment="right">Total Sale: <b>{total_sale.get()}</b></para>', normal_style))
    doc.build(elements)#this is what creates and saves the file
    print("PDF saved at:", os.path.abspath(pdf_name)) #testing the path





#sql
mydb = get_mydb_connect()
my_cursor = mydb.cursor()

 
#SQL
#used to get the last sale no, so that we can increment by 1
find_sale_no = """SELECT s.sale_id,s.sale_date,s.cust_id,s.prod_id,s.sale_qty,c.cust_name,c.cust_surname,p.prod_name,p.prod_sprice 
FROM Sales s
JOIN Customer c ON s.cust_id = c.cust_id
JOIN Product p ON s.prod_id = p.prod_id
WHERE s.sale_id = %s"""
 
 
#window
root = tk.Tk()
root.geometry("800x600")
root.title("SALES REPORT")
root.resizable(False,False)
root.iconbitmap("images\Logo.ico")
 
 
#variables
 
sale_id = tk.IntVar()
sale_id.set("Enter Sale no. here")
sale_date = tk.StringVar()
sale_date.set("dd/mm/yyyy")
 
cust_id = tk.StringVar()
cust_name = tk.StringVar()
total_sale = tk.DoubleVar()
 
#reminder: rows[] is a global variable list
rows = [] #list for the sale items that are going to be displayed on the canvas
#add_item()
 
 
#font styles
default_font = ("Arial",14)
title_font = ("Verdana",18)
button_font = ("Courier New",14)
 
'''
#setting the grid
root.rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
root.columnconfigure((0,1,2),weight=1)
'''
#widgets
 
#scrollable Frame Section
product_section = tk.Frame(root) #creating a frame
canvas = tk.Canvas(product_section,height=150)
product_scroll = tk.Scrollbar(product_section,orient="vertical",command=canvas.yview)
scroll_frame = tk.Frame(canvas)
canvas.create_window((0,0),window=scroll_frame,anchor="nw")
 
 
#labels
title_lbl = tk.Label(root,text="GROCERY SYSTEM - SALE REPORT",font=title_font,bg="#00DD00")
sale_id_lbl = tk.Label(root,text="Sale Id",font=default_font)
sale_date_lbl = tk.Label(root,text="Sale Date",font=default_font)
cust_id_lbl = tk.Label(root,text="Customer ID",font=default_font)
cust_name_lbl = tk.Label(root,text="Customer Name",font=default_font)
total_sale_lbl = tk.Label(root,text="Total Sale",font=default_font)
 
 
#entry boxes
sale_id_txt = tk.Entry(root,textvariable=sale_id,font=default_font)
sale_id_txt.bind("<FocusOut>",find_sale)
sale_id_txt.bind("<FocusIn>",lambda e: e.widget.select_range(0, 'end'))#select all text for easier input of Sale No
sale_date_txt = tk.Entry(root,textvariable=sale_date,font=default_font,state="readonly")
cust_id_txt = tk.Entry(root,textvariable=cust_id,font=default_font,state="readonly")
cust_name_txt = tk.Entry(root,textvariable=cust_name,font=default_font,state="readonly")
total_sale_txt = tk.Entry(root,textvariable=total_sale,font=default_font,state="readonly")
 
#buttons
clear_data_btn = tk.Button(root,text="Clear Data",font=button_font,command=clear_data)
print_sale_btn = tk.Button(root,text="Print (PDF)",font=button_font,command=print_pdf,state='disabled')
exit_btn = tk.Button(root,text="EXIT",font=button_font,command=exit_root)
 
 
#placing the widgets
title_lbl.grid(row=0,columnspan=3,sticky="we")
 
sale_id_lbl.grid(row=1,column=0,padx=40,pady=10,sticky="nw")
sale_id_txt.grid(row=2,column=0,padx=40,sticky="nw")
 
sale_date_lbl.grid(row=1,column=1,padx=10,pady=10,sticky="nw")
sale_date_txt.grid(row=2,column=1,padx=10,pady=10,sticky="nw")
 
cust_id_lbl.grid(row=3,column=0,padx=40,pady=10,sticky="nw")
cust_id_txt.grid(row=4,column=0,padx=40,pady=10,sticky="nw")
 
cust_name_lbl.grid(row=3,column=1,padx=10,pady=10,sticky="nw")
cust_name_txt.grid(row=4,column=1,padx=10,pady=10,sticky="nw")
 
total_sale_lbl.grid(row=6,column=1,padx=10,sticky="ne")
total_sale_txt.grid(row=6,column=2,padx=10,sticky="nw")
 
 
#placing the scroll section on the screen
product_section.grid(row=5,column=0,columnspan=3,padx=10,pady=10)
canvas.pack(side="left",fill="both",expand=True)
product_scroll.pack(side="right",fill="y",padx=15) #actual scrollbar
canvas.configure(yscrollcommand=product_scroll.set)
scroll_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

 
 
clear_data_btn.grid(row=8,columnspan=3,pady=7,sticky="we")
print_sale_btn.grid(row=9,columnspan=3,pady=7,sticky="we")
exit_btn.grid(row=10,columnspan=3,pady=7,sticky="we")
 
 
#main loop - window
root.mainloop()




