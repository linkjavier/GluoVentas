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

        # *** Variables ***
        self.SearchByVar=StringVar()
        self.SearchTxtVar=StringVar()
        self.ProductIdVar=StringVar()
        self.CategoryVar=StringVar()
        self.SupplierVar=StringVar()
        self.CategoryList=[]
        self.SupplierList = []
        self.fetch_cat_sup()
        self.NameVar=StringVar()
        self.PriceVar=StringVar()
        self.QuantityVar=StringVar()
        self.StatusVar=StringVar()



        # ** Product Frame **
        ProductFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        ProductFrame.place(x=10,y=10,width=450,height=480)

        # *** Title ***
        TitleLabel=Label(ProductFrame,text=constants.product_details,font=("goudy old style",12),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
 
        # *** Column 1 ***
        Categorylabel=Label(ProductFrame,text=constants.generic_category,font=("goudy old style",12),bg="white").place(x=30,y=60)
        SupplierLabel=Label(ProductFrame,text=constants.generic_supplier,font=("goudy old style",12),bg="white").place(x=30,y=110)
        NameLabel=Label(ProductFrame,text=constants.generic_name,font=("goudy old style",12),bg="white").place(x=30,y=160)
        PriceLabel=Label(ProductFrame,text=constants.generic_price,font=("goudy old style",12),bg="white").place(x=30,y=210)
        QuantityLabel=Label(ProductFrame,text=constants.generic_quantity,font=("goudy old style",12),bg="white").place(x=30,y=260)
        StatusLabel=Label(ProductFrame,text=constants.generic_status,font=("goudy old style",12),bg="white").place(x=30,y=310)

        
        # *** Column 2 ***
        ComboBoxCategory=ttk.Combobox(ProductFrame,textvariable=self.CategoryVar,values=(self.CategoryList),state='readonly',justify=CENTER,font=("goudy old style", 12))
        ComboBoxCategory.place(x=150,y=60,width=200)
        ComboBoxCategory.current(0)

        ComboBoxSupplier=ttk.Combobox(ProductFrame,textvariable=self.SupplierVar,values=(self.SupplierList),state='readonly',justify=CENTER,font=("goudy old style", 12))
        ComboBoxSupplier.place(x=150,y=110,width=200)
        ComboBoxSupplier.current(0)

        txt_name=Entry(ProductFrame,textvariable=self.NameVar,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=160,width=200)
        txt_price=Entry(ProductFrame,textvariable=self.PriceVar,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=210,width=200)
        txt_qty=Entry(ProductFrame,textvariable=self.QuantityVar,font=("goudy old style", 12),bg='lightyellow').place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(ProductFrame,textvariable=self.StatusVar,values=(constants.generic_active,constants.generic_inactive),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        # *** Buttons ***
        btn_add=Button(ProductFrame,text=constants.generic_add,command=self.add,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(ProductFrame,text=constants.generic_update,command=self.update,font=("goudy old style",12),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(ProductFrame,text=constants.generic_delete,command=self.delete,font=("goudy old style",12),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(ProductFrame,text=constants.generic_clear,command=self.clear,font=("goudy old style",12),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)


        # *** SearchFrame ***
        SearchFrame=LabelFrame(self.root,text=constants.search_product,font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        # *** Options ***
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.SearchByVar,values=(constants.generic_select,constants.generic_category,constants.generic_supplier,constants.generic_name),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.SearchTxtVar,font=("goudy old style",12),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text=constants.generic_search,command=self.search,font=("goudy old style",12),bg="#4caf50",fg="white").place(x=410,y=10,width=150,height=25)

        # *** Product Details ***

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

# *********************************************************************************

    def fetch_cat_sup(self):
        self.CategoryList.append(constants.generic_empty)
        self.SupplierList.append(constants.generic_empty)
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT Nombre FROM Category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.CategoryList[:]
                self.CategoryList.append(constants.generic_select)
                for i in cat:
                    self.CategoryList.append(i[0])

            cur.execute(("SELECT {} FROM Supplier").format(constants.generic_name))
            sup=cur.fetchall()
            if len(sup)>0:
                del self.SupplierList[:]
                self.SupplierList.append(constants.generic_select)
                for i in sup:
                    self.SupplierList.append(i[0])


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)



    def add(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.CategoryVar.get()==constants.generic_select or self.CategoryVar.get()==constants.generic_empty or self.SupplierVar.get()==constants.generic_select or self.NameVar.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE Nombre=?",(self.NameVar.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Product already exist, try different",parent=self.root)
                else:
                    cur.execute("INSERT INTO Product(Categoria,Proveedor,Nombre,Precio,Cantidad,Estado) values(?,?,?,?,?,?)",(
                                        self.CategoryVar.get(),
                                        self.SupplierVar.get(),
                                        self.NameVar.get(),
                                        self.PriceVar.get(),
                                        self.QuantityVar.get(),
                                        self.StatusVar.get(),
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
        self.ProductIdVar.set(row[0]),
        self.SupplierVar.set(row[1]),
        self.CategoryVar.set(row[2]),
        self.NameVar.set(row[3]),
        self.PriceVar.set(row[4]),
        self.QuantityVar.set(row[5]),
        self.StatusVar.set(row[6]),

    def update(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.ProductIdVar.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE ID=?",(self.ProductIdVar.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("UPDATE Product SET Categoria=?,Proveedor=?,Nombre=?,Precio=?,Cantidad=?,Estado=? WHERE ID=?",(
                                        self.CategoryVar.get(),
                                        self.SupplierVar.get(),
                                        self.NameVar.get(),
                                        self.PriceVar.get(),
                                        self.QuantityVar.get(),
                                        self.StatusVar.get(),
                                        self.ProductIdVar.get()
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
            if self.ProductIdVar.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE ID=?",(self.ProductIdVar.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete",parent=self.root)
                    if op==True:
                        cur.execute("DELETE FROM Product WHERE ID=?",(self.ProductIdVar.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.CategoryVar.set(constants.generic_select),
        self.SupplierVar.set(constants.generic_select),
        self.NameVar.set(""),
        self.PriceVar.set(""),
        self.QuantityVar.set(""),
        self.StatusVar.set(""),
        self.ProductIdVar.set("")
        self.SearchTxtVar.set("")
        self.SearchByVar.set(constants.generic_select)
        self.show()

    def search(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.SearchByVar.get()==constants.generic_select:
                messagebox.showerror("Error","Select Search By Option", parent=self.root)
            elif self.SearchTxtVar.get()=="":
                messagebox.showerror("Error","Search input shoul be required", parent=self.root)

            else:
                cur.execute("SELECT * FROM Product WHERE "+self.SearchByVar.get()+" LIKE '%"+self.SearchTxtVar.get()+"%'")
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
