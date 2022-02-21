import sqlite3

def create_database():
    con=sqlite3.connect(database=r'database.db')
    cur=con.cursor()

    # == Employee Create ===
    cur.execute("CREATE TABLE IF NOT EXISTS Employee(ID INTEGER PRIMARY KEY AUTOINCREMENT,Nombre text,Email text,Sexo text,Contacto text,F_Nacimiento text,F_Ingreso text,Password text,T_Usuario text,Dirección text,Salario text)")
    con.commit()

    # == Employee Create ===    
    cur.execute("CREATE TABLE IF NOT EXISTS Supplier(Factura INTEGER PRIMARY KEY AUTOINCREMENT,Nombre text,Contacto text,Descripción text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Category(CID INTEGER PRIMARY KEY AUTOINCREMENT,Nombre text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Product(ID INTEGER PRIMARY KEY AUTOINCREMENT,Proveedor text,Categoria text,Nombre text,Precio text,Cantidad text,Estado text)")
    con.commit()

create_database()
