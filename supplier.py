from tkinter import *
import constants
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title(constants.app_name)
        self.root.config(bg="white")
        self.root.focus_force()

        # ==================================================================

        # === All Variables ===
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()

        # === Options ===
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style", 12))
        lbl_search.place(x=700,y=80)

        txt_search=Entry(root,textvariable=self.var_searchtxt,font=("goudy old style",12),bg="lightyellow").place(x=800,y=80,width=160)
        btn_search=Button(root,text=constants.generic_search,command=self.search,font=("goudy old style",12),bg="#4caf50",fg="white").place(x=980,y=79,width=100,height=28)

        # === Title ===
        title=Label(self.root,text=constants.supplier_details,font=("goudy old style",12,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        # === Content ========================================================

        # === First Row ===
        lbl_supplier_invoice=Label(self.root,text=constants.invoice_number,font=("goudy old style",12),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",12),bg="lightyellow").place(x=180,y=80,width=180)
      
        # === Second Row ===
        lbl_name=Label(self.root,text=constants.generic_name,font=("goudy old style",12),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",12),bg="lightyellow").place(x=180,y=120,width=180)
        
        # === Third Row ===
        lbl_contact=Label(self.root,text=constants.generic_contact,font=("goudy old style",12),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",12),bg="lightyellow").place(x=180,y=160,width=180)
  
        # === Fourth Row ===
        lbl_address=Label(self.root,text=constants.generic_description,font=("goudy old style",12),bg="white").place(x=50,y=200)

        self.txt_desc=Text(self.root,font=("goudy old style",12),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)

        # === Buttons ===
        btn_add=Button(self.root,text=constants.generic_add,command=self.add,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=28)
        btn_update=Button(self.root,text=constants.generic_update,command=self.update,font=("goudy old style",12),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=28)
        btn_delete=Button(self.root,text=constants.generic_delete,command=self.delete,font=("goudy old style",12),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=28)
        btn_clear=Button(self.root,text=constants.generic_clear,command=self.clear,font=("goudy old style",12),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=28)

        # === Suppliers Details ===

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)
        
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(emp_frame,columns=(constants.generic_invoice,constants.generic_name,constants.generic_contact,constants.generic_description),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)


        self.SupplierTable.heading(constants.generic_invoice,text=constants.generic_invoice)
        self.SupplierTable.heading(constants.generic_name,text=constants.generic_name)
        self.SupplierTable.heading(constants.generic_contact,text=constants.generic_contact)
        self.SupplierTable.heading(constants.generic_description,text=constants.generic_description)
        self.SupplierTable["show"]="headings"

        self.SupplierTable.column(constants.generic_invoice,width=90)
        self.SupplierTable.column(constants.generic_name,width=200)
        self.SupplierTable.column(constants.generic_contact,width=100)
        self.SupplierTable.column(constants.generic_description,width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
# =================================================================================
    def add(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM Supplier WHERE Factura=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice No. already assigned, try different",parent=self.root)
                else:
                    cur.execute("INSERT INTO Supplier (Factura,Nombre,Contacto,Descripci??n) values(?,?,?,?)",(
                                        self.var_sup_invoice.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Succes", "Supplier Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM Supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        # print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),

    def update(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Must be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM Supplier WHERE Factura=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Invoide No.",parent=self.root)
                else:
                    cur.execute("UPDATE Supplier SET Nombre=?,Contacto=?,Descripci??n=? WHERE Factura=?",(
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Succes", "Supplier Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No.Must be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM Supplier WHERE Factura=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Invoide No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete",parent=self.root)
                    if op==True:
                        cur.execute("DELETE FROM Supplier WHERE Factura=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. should be required", parent=self.root)

            else:
                cur.execute("SELECT * FROM Supplier WHERE Factura=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

        

if __name__=="__main__":

    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
 