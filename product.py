from itertools import product
from tkinter import *
import constants
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title(constants.app_name)
        self.root.config(bg="white")
        self.root.focus_force()

        # === Variables ===
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()



        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=10,y=10,width=450,height=480)

        # === Title ===
        title=Label(product_frame,text=constants.product_details,font=("goudy old style",12),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
 
        # === Column 1 ===
        lbl_category=Label(product_frame,text=constants.generic_category,font=("goudy old style",12),bg="white").place(x=30,y=60)
        lbl_suppliery=Label(product_frame,text=constants.generic_supplier,font=("goudy old style",12),bg="white").place(x=30,y=110)
        lbl_name=Label(product_frame,text=constants.generic_name,font=("goudy old style",12),bg="white").place(x=30,y=160)
        lbl_price=Label(product_frame,text=constants.generic_price,font=("goudy old style",12),bg="white").place(x=30,y=210)
        lbl_quantity=Label(product_frame,text=constants.generic_quantity,font=("goudy old style",12),bg="white").place(x=30,y=260)
        lbl_status=Label(product_frame,text=constants.generic_status,font=("goudy old style",12),bg="white").place(x=30,y=310)

        
        # === Column 2 ===
        cmb_cat=ttk.Combobox(product_frame,textvariable=self.var_cat,values=(self.cat_list),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_frame,textvariable=self.var_sup,values=(self.sup_list),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_frame,textvariable=self.var_name,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=160,width=200)
        txt_price=Entry(product_frame,textvariable=self.var_price,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=210,width=200)
        txt_qty=Entry(product_frame,textvariable=self.var_qty,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_frame,textvariable=self.var_status,values=(constants.generic_active,constants.generic_inactive),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        # === Buttons ===
        btn_add=Button(product_frame,text=constants.generic_add,command=self.add,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_frame,text=constants.generic_update,command=self.update,font=("goudy old style",12),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_frame,text=constants.generic_delete,command=self.delete,font=("goudy old style",12),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_frame,text=constants.generic_clear,command=self.clear,font=("goudy old style",12),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)


        # === SearchFrame ===
        SearchFrame=LabelFrame(self.root,text=constants.search_product,font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        # === Options ===
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=(constants.generic_select,constants.generic_category,constants.generic_supplier,constants.generic_name),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",12),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text=constants.generic_search,command=self.search,font=("goudy old style",12),bg="#4caf50",fg="white").place(x=410,y=10,width=150,height=25)

        # === Product Details ===

        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)
        
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(p_frame,columns=(constants.product_id,constants.generic_supplier,constants.generic_category,constants.generic_name,constants.generic_price,constants.generic_quantity,constants.generic_status),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)


        self.ProductTable.heading(constants.product_id,text=constants.product_id)
        self.ProductTable.heading(constants.generic_category,text=constants.generic_category)
        self.ProductTable.heading(constants.generic_supplier,text=constants.generic_supplier)
        self.ProductTable.heading(constants.generic_name,text=constants.generic_name)
        self.ProductTable.heading(constants.generic_price,text=constants.generic_price)
        self.ProductTable.heading(constants.generic_quantity,text=constants.generic_quantity)
        self.ProductTable.heading(constants.generic_status,text=constants.generic_status)

        self.ProductTable["show"]="headings"

        self.ProductTable.column(constants.product_id,width=90)
        self.ProductTable.column(constants.generic_category,width=200)
        self.ProductTable.column(constants.generic_supplier,width=100)
        self.ProductTable.column(constants.generic_name,width=100)
        self.ProductTable.column(constants.generic_price,width=100)
        self.ProductTable.column(constants.generic_quantity,width=100)
        self.ProductTable.column(constants.generic_status,width=100)

        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

# =================================================================================

    def fetch_cat_sup(self):
        self.cat_list.append(constants.generic_empty)
        self.sup_list.append(constants.generic_empty)
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT Nombre FROM Category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append(constants.generic_select)
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute(("SELECT {} FROM Supplier").format(constants.generic_name))
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append(constants.generic_select)
                for i in sup:
                    self.sup_list.append(i[0])


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)



    def add(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()==constants.generic_select or self.var_cat.get()==constants.generic_empty or self.var_sup.get()==constants.generic_select or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE Nombre=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Product already exist, try different",parent=self.root)
                else:
                    cur.execute("INSERT INTO Product(Categoria,Proveedor,Nombre,Precio,Cantidad,Estado) values(?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Succes", "Product Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM Product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_sup.set(row[1]),
        self.var_cat.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),

    def update(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE ID=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("UPDATE Product SET Categoria=?,Proveedor=?,Nombre=?,Precio=?,Cantidad=?,Estado=? WHERE ID=?",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Succes", "Product Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE ID=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete",parent=self.root)
                    if op==True:
                        cur.execute("DELETE FROM Product WHERE ID=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_cat.set(constants.generic_select),
        self.var_sup.set(constants.generic_select),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set(""),
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set(constants.generic_select)
        self.show()

    def search(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()==constants.generic_select:
                messagebox.showerror("Error","Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input shoul be required", parent=self.root)

            else:
                cur.execute("SELECT * FROM Product WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)


if __name__=="__main__":

    root = Tk()
    obj = productClass(root)
    root.mainloop()