from itertools import product
from tkinter import *
import constants
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

# Inventory Management System


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title(constants.app_name)
        self.root.config(bg="white")

        # === Title ===
        self.icon_title = PhotoImage(file="images/logo1_small.png")
        title = Label(
            self.root,
            text=constants.app_title,
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 20, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20).place(
            x=0,
            y=0,
            relwidth=1,
            height=70)

        # === Button Logout ===
        btn_logout = Button(
            self.root,
            text=constants.button_logout_text,
            font=(
                "times new roman",
                14,
                "bold"),
            bg="white",
            cursor="hand2").place(
            x=1150,
            y=10,
            height=50,
            width=150)

        # === Clock ===
        self.lbl_clock = Label(
            self.root,
            text=constants.welcome_date_hour_text_bar,
            font=(
                "times new roman",
                12),
            bg="#4d636d",
            fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # === Left Menu ===
        self.MenuLogo=Image.open("images/IMS_logo.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side = PhotoImage(file="images/right_arrow2.png")
        lbl_menu = Label(LeftMenu,text=constants.generic_menu,font=("times new roman",15),bg="#009688").pack(side=TOP,fill=X)

        # === Menu Buttons ===
        btn_employee = Button(LeftMenu,text=constants.generic_employees,command=self.employee,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu,text=constants.generic_suppliers,command=self.supplier,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu,text=constants.generic_categories,command=self.category,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product = Button(LeftMenu,text=constants.generic_product,command=self.product,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu,text=constants.generic_sales,command=self.sales,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu,text=constants.generic_exit,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        # === Content ===
        self.lbl_employee=Label(self.root,text=constants.generic_total_employee + "\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",15,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text=constants.generic_total_supplier + "\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",15,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text=constants.generic_total_category + "\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",15,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text=constants.generic_total_product + "\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",15,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text=constants.generic_total_sales + "\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",15,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        # === Footer ===
        self.lbl_clock = Label(
            self.root,
            text=constants.footer_text,
            font=(
                "times new roman",
                12),
            bg="#4d636d",
            fg="white").pack(side=BOTTOM,fill=X)

# ==============================================================

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)


if __name__=="__main__":

    root = Tk()
    obj = IMS(root)
    root.mainloop()
