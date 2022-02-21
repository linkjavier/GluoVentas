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



        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=10,y=10,width=450,height=480)

        # === Title ===
        title=Label(product_frame,text=constants.product_details,font=("goudy old style",12),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
 
        lbl_category=Label(product_frame,text=constants.generic_category,font=("goudy old style",12),bg="white").place(x=30,y=60)
        lbl_suppliery=Label(product_frame,text=constants.generic_supplier,font=("goudy old style",12),bg="white").place(x=30,y=110)
        lbl_name=Label(product_frame,text=constants.generic_name,font=("goudy old style",12),bg="white").place(x=30,y=160)
        lbl_price=Label(product_frame,text=constants.generic_price,font=("goudy old style",12),bg="white").place(x=30,y=210)
        lbl_quantity=Label(product_frame,text=constants.generic_quantity,font=("goudy old style",12),bg="white").place(x=30,y=260)
        lbl_status=Label(product_frame,text=constants.generic_status,font=("goudy old style",12),bg="white").place(x=30,y=310)





if __name__=="__main__":

    root = Tk()
    obj = productClass(root)
    root.mainloop()