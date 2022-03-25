import sqlite3
from tkinter import *
import constants
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import _sqlite3
import time

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title(constants.app_name)
        self.root.config(bg="white")
        self.cart_list=[]

        # === Title ===
        self.icon_title = PhotoImage(file="images/logo1_small.png")
        title = Label(self.root,text=constants.app_title,image=self.icon_title,compound=LEFT,font=("times new roman", 20, "bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # === Button Logout ===
        btn_logout = Button(self.root,text=constants.button_logout_text,font=("times new roman",14,"bold"),bg="white",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        # === Clock ===
        self.lbl_clock = Label(self.root,text=constants.welcome_date_hour_text_bar,font=("times new roman",12),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # === Product Frame ===
        ProductFrame=Frame(self.root,bd=4,relief=RIDGE)
        ProductFrame.place(x=6,y=110,width=410,height=520)

        pTitle=Label(ProductFrame,text=constants.generic_all_products,font=("goudy old style",12,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        # == Product Search Frame ===
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",12,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text=constants.generic_product,font=("times new roman",12,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",12),bg="lightyellow").place(x=128,y=47,width=150,height=22)

        btn_search=Button(ProductFrame2,text=constants.generic_search,command=self.search,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=280,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text=constants.generic_show_all,command=self.show,font=("goudy old style",10),bg="#083531",fg="white",cursor="hand2").place(x=280,y=10,width=100,height=25)

        # === Frame3 Details ===
        ProductFrame3=Frame(ProductFrame,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=350)
        
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(ProductFrame3,columns=(constants.product_id,constants.generic_name,constants.generic_price,constants.generic_quantity,constants.generic_status),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)


        self.ProductTable.heading(constants.product_id,text=constants.product_id)
        self.ProductTable.heading(constants.generic_name,text=constants.generic_name)
        self.ProductTable.heading(constants.generic_price,text=constants.generic_price)
        self.ProductTable.heading(constants.generic_quantity,text=constants.generic_quantity)
        self.ProductTable.heading(constants.generic_status,text=constants.generic_status)
        self.ProductTable["show"]="headings"
        self.ProductTable.column(constants.product_id,width=40)
        self.ProductTable.column(constants.generic_name,width=170)
        self.ProductTable.column(constants.generic_price,width=50)
        self.ProductTable.column(constants.generic_quantity,width=70)
        self.ProductTable.column(constants.generic_status,width=60)

        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.ProductTable.bind("<Double-Button-1>",self.DoubleClickAdding)
        self.ProductTable.bind("<Return>",self.EnterAdding)
        self.root.bind("<Up>",self.UpDownUpdate)
        self.root.bind("<Down>",self.UpDownUpdate)


        lbl_note=Label(ProductFrame,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        # === Customer Frame ===
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",12),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text=constants.generic_name,font=("times new roman",12,"bold"),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",12),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text=constants.generic_contact,font=("times new roman",12,"bold"),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",12),bg="lightyellow").place(x=380,y=35,width=140)

        # === Cal Cart Frame ===
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=330)


        # === Calculator Frame ===
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=310)

        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly')
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=3,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=3,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=3,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=1,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=3,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=3,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=3,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=1,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=3,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_1=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=3,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=3,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=1,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=3,pady=18,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=3,pady=18,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=3,pady=18,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=1,pady=18,cursor="hand2").grid(row=4,column=3)


        # === Cart Frame ===
        cart_frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_frame.place(x=280,y=8,width=245,height=310)
        self.cartTitle=Label(cart_frame,text="Cart \t Total Product: [0]",font=("goudy old style",12),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
        
        scrolly=Scrollbar(cart_frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_frame,columns=(constants.product_id,constants.generic_name,constants.generic_price,constants.generic_quantity),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading(constants.product_id,text=constants.product_id)
        self.CartTable.heading(constants.generic_name,text=constants.generic_name)
        self.CartTable.heading(constants.generic_price,text=constants.generic_price)
        self.CartTable.heading(constants.generic_quantity,text=constants.generic_quantity)
        self.CartTable["show"]="headings"
        self.CartTable.column(constants.product_id,width=40)
        self.CartTable.column(constants.generic_name,width=100)
        self.CartTable.column(constants.generic_price,width=90)
        self.CartTable.column(constants.generic_quantity,width=80)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)


        # === Add Cart Widget Frame ===
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=520,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",12),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",12),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",12),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",12),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",12),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",12),bg="lightyellow",).place(x=390,y=35,width=120,height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",12),bg="white")
        self.lbl_inStock.place(x=5,y=70)
        btn_clear_cart=Button(Add_CartWidgetsFrame,text=constants.generic_clear,font=("times new roman",12,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",12,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)


        # === Billing Area ===
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=410,height=410)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",12,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # === Billing Buttons ===
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=953,y=520,width=410,height=110)

        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",10,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=2,width=120,height=50)

        self.lbl_discount=Label(billMenuFrame,text='Discount \n[5%]',font=("goudy old style",10,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=2,width=120,height=50)

        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",10,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=2,width=160,height=50)

        btn_print=Button(billMenuFrame,text='Print',cursor='hand2',font=("goudy old style",10,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=56,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text='Clear All',cursor='hand2',font=("goudy old style",10,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=56,width=120,height=50)

        btn_generate=Button(billMenuFrame,text='Generate/Save Bill',command=self.generate_bill,cursor='hand2',font=("goudy old style",10,"bold"),bg="#809688",fg="white")
        btn_generate.place(x=246,y=56,width=160,height=50)


        # # === Footer ===
        footer=Label(self.root,text="MVP Sistema de Ventas e Inventario | Developed By Gluonico\nFor Technical Issue contact: 3003943675",font=("times new roman",11),bg="#4d636d",fg="white",activebackground="#4d636d",activeforeground="white").pack(side=BOTTOM,fill=X)

        self.show()
        # self.bill_top()


# ========================================== All Functions ===============================================================================

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT {},{},{},{},{} FROM Product where {}='{}'".format(constants.product_id,constants.generic_name,constants.generic_price,constants.generic_quantity,constants.generic_status,constants.generic_status,constants.generic_active))
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input shoul be required", parent=self.root)

            else:
                cur.execute(("SELECT {},{},{},{},{} FROM Product WHERE {} LIKE '%"+self.var_search.get()+"%' and {}='{}'").format(constants.product_id,constants.generic_name,constants.generic_price,constants.generic_quantity,constants.generic_status,constants.generic_name,constants.generic_status,constants.generic_active))
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')


    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)

        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            # price_cal=int(self.var_qty.get())*float(self.var_price.get())
            # price_cal=float(price_cal)
            price_cal=self.var_price.get()

            # constants.product_id,constants.generic_name,constants.generic_price,constants.generic_quantity,constants.generic_status
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]

            # === Update Cart ===
            present='no'
            index_=0


            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1

            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update| Remove from the cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal # Price
                        self.cart_list[index_][3]=self.var_qty.get() # Quantity
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()



    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amount(COP)\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay(COP)\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)


    def generate_bill(self):
        """Function that construct the bill"""

        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please add product to the cart",parent=self.root)

        else:
            # *** Bill Top ***
            self.bill_top()
            # *** Bill Middle ***
            self.bill_middle()
            # *** Bill Bottom ***
            self.bill_bottom()


    def bill_top(self):
        """Function that built a text segment and insert it
            in the corresponding bill area"""

        invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\tTexaco 31 - Software de Facturación
\tPhone No. 9872543345, San Pedro-Valle
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
 {str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    
    def bill_middle(self):
        for row in self.cart_list:
            name=row[1]
            qty=row[3]
            price=float(row[2])*int(row[3])
            price=str(price)
            self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+qty+"\tRs."+price) 


    def DoubleClickAdding(self,env):
        """Function to add a product that is called by double clicking"""

        self.get_data
        self.add_update_cart()


    def EnterAdding(self,env):
        """Function that update the cart if var_pid has a value
            If the user press enter, only update the cart if the data is charged
        """
        if self.var_pid.get():
            self.add_update_cart()

    def UpDownUpdate(self,env):
        """Function that updates values when navigate with up/down arrows"""

        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

if __name__=="__main__":

    root = Tk()
    obj = BillClass(root)
    root.mainloop()      