from tkinter import *
import constants
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3


class employeeClass:
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

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_birth=StringVar()
        self.var_join=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()


        # === SearchFrame ===
        SearchFrame=LabelFrame(self.root,text=constants.search_employee,font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        # === Options ===
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=(constants.generic_select,constants.generic_email,constants.generic_name,constants.generic_contact),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",12),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text=constants.generic_search,command=self.search,font=("goudy old style",12),bg="#4caf50",fg="white").place(x=410,y=10,width=150,height=25)

        # === Title ===
        title=Label(self.root,text=constants.employee_details,font=("goudy old style",12),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        # === Content ========================================================

        # === First Row ===
        lbl_empid=Label(self.root,text=constants.employee_id,font=("goudy old style",12),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text=constants.generic_gender,font=("goudy old style",12),bg="white").place(x=350,y=150)
        lbl_contact=Label(self.root,text=constants.generic_contact,font=("goudy old style",12),bg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",12),bg="lightyellow").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=(constants.generic_select,constants.generic_male,constants.generic_female,constants.generic_other),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",12),bg="lightyellow").place(x=850,y=150,width=180)
       
        # === Second Row ===
        lbl_name=Label(self.root,text=constants.generic_name,font=("goudy old style",12),bg="white").place(x=50,y=190)
        lbl_birth=Label(self.root,text=constants.generic_birth,font=("goudy old style",12),bg="white").place(x=350,y=190)
        lbl_join_date=Label(self.root,text=constants.generic_join_date,font=("goudy old style",12),bg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",12),bg="lightyellow").place(x=150,y=190,width=180)
        txt_birth=Entry(self.root,textvariable=self.var_birth,font=("goudy old style",12),bg="lightyellow").place(x=500,y=190,width=180)
        txt_join_date=Entry(self.root,textvariable=self.var_join,font=("goudy old style",12),bg="lightyellow").place(x=850,y=190,width=180)

        # === Third Row ===
        lbl_email=Label(self.root,text=constants.generic_email,font=("goudy old style",12),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text=constants.generic_password,font=("goudy old style",12),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text=constants.generic_user_type,font=("goudy old style",12),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",12),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",12),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=(constants.generic_admin,constants.generic_employee),state='readonly',justify=CENTER,font=("goudy old style", 12))
        cmb_utype.place(x=850,y=230,width=180) 
        cmb_utype.current(0)

        # === Fourth Row ===
        lbl_address=Label(self.root,text=constants.generic_address,font=("goudy old style",12),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text=constants.generic_salary,font=("goudy old style",12),bg="white").place(x=500,y=270)

        self.txt_address=Text(self.root,font=("goudy old style",12),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",12),bg="lightyellow").place(x=600,y=270,width=180)

        # === Buttons ===
        btn_add=Button(self.root,text=constants.generic_add,command=self.add,font=("goudy old style",12),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text=constants.generic_update,command=self.update,font=("goudy old style",12),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text=constants.generic_delete,command=self.delete,font=("goudy old style",12),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text=constants.generic_clear,command=self.clear,font=("goudy old style",12),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        # === Employees Details ===

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)
        
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=(constants.employee_id,constants.generic_name,constants.generic_email,constants.generic_gender,constants.generic_contact,constants.generic_birth,constants.generic_join_date,constants.generic_password,constants.generic_user_type,constants.generic_address,constants.generic_salary),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)


        self.EmployeeTable.heading(constants.employee_id,text=constants.employee_id)
        self.EmployeeTable.heading(constants.generic_name,text=constants.generic_name)
        self.EmployeeTable.heading(constants.generic_email,text=constants.generic_email)
        self.EmployeeTable.heading(constants.generic_gender,text=constants.generic_gender)
        self.EmployeeTable.heading(constants.generic_contact,text=constants.generic_contact)
        self.EmployeeTable.heading(constants.generic_birth,text=constants.generic_birth)
        self.EmployeeTable.heading(constants.generic_join_date,text=constants.generic_join_date)
        self.EmployeeTable.heading(constants.generic_password,text=constants.generic_password)
        self.EmployeeTable.heading(constants.generic_user_type,text=constants.generic_user_type)
        self.EmployeeTable.heading(constants.generic_address,text=constants.generic_address)
        self.EmployeeTable.heading(constants.generic_salary,text=constants.generic_salary)
        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column(constants.employee_id,width=90)
        self.EmployeeTable.column(constants.generic_name,width=200)
        self.EmployeeTable.column(constants.generic_email,width=100)
        self.EmployeeTable.column(constants.generic_gender,width=100)
        self.EmployeeTable.column(constants.generic_contact,width=100)
        self.EmployeeTable.column(constants.generic_birth,width=100)
        self.EmployeeTable.column(constants.generic_join_date,width=100)
        self.EmployeeTable.column(constants.generic_password,width=100)
        self.EmployeeTable.column(constants.generic_user_type,width=100)
        self.EmployeeTable.column(constants.generic_address,width=100)
        self.EmployeeTable.column(constants.generic_salary,width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
# =================================================================================
    def add(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error",constants.employee_required_id_error,parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE ID=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error",constants.employee_already_exist,parent=self.root)
                else:
                    cur.execute("INSERT INTO Employee (ID,Nombre,Email,Sexo,Contacto,F_Nacimiento,F_Ingreso,Password,T_Usuario,Dirección,Salario) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_birth.get(),
                                        self.var_join.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo(constants.generic_added,constants.employee_added,parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM Employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        # print(row)
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_birth.set(row[5]),
        self.var_join.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0',END),
        self.txt_address.insert(END,row[9]),
        self.var_salary.set(row[10])


    def update(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error",constants.employee_required_id_error,parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE ID=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Employee ID",parent=self.root)
                else:
                    cur.execute("UPDATE Employee SET Nombre=?,Email=?,Sexo=?,Contacto=?,F_Nacimiento=?,F_Ingreso=?,Password=?,T_Usuario=?,Dirección=?,Salario=? WHERE ID=?",(
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_birth.get(),
                                        self.var_join.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_salary.get(),
                                        self.var_emp_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo(constants.generic_updated, constants.employee_updated,parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error",constants.employee_required_id_error,parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE ID=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno(constants.generic_confirm,constants.employee_confirm_delete,parent=self.root)
                    if op==True:
                        cur.execute("DELETE FROM Employee WHERE ID=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo(constants.generic_deleted,constants.employee_deleted,parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_emp_id.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set(constants.generic_select),
        self.var_contact.set(""),
        self.var_birth.set(""),
        self.var_join.set(""),
        self.var_pass.set(""),
        self.var_utype.set(""),
        self.txt_address.delete('1.0',END),
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set(constants.generic_select)
        self.show()

    def search(self):
        con=sqlite3.connect(database='database.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()==constants.generic_select:
                messagebox.showerror("Error",constants.search_by_option_message, parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error",constants.search_input_required, parent=self.root)

            else:
                cur.execute("SELECT * FROM Employee WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", constants.search_no_record_found,parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

        

if __name__=="__main__":

    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
 