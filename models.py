
import sqlite3
from sqlite3 import Error
from os import path


db_file = path.abspath(path.dirname(__file__))
db_file = path.join(db_file, 'db.db')

sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS "tasks" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "task_text" text NOT NULL,
                            "author" integer,
                            "status" boolean); """

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS "users" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "user" text NOT NULL,
                            "password" text,
                            "online" datetime); """

sql_insert_tasks_table = """INSERT INTO tasks (id, task_text, author, status) VALUES 
                                        ('1', 'Открыть дверь холодильника', '1', 'False'),
                                        ('2', 'Положить в холодильник слона', '1', 'False'),
                                        ('3', 'Закрыть дверь холодильника', '1', 'False');
                                        """

sql_insert_users_table = """INSERT INTO users (id, user, password) VALUES 
                                    ('1', 'admin', 'HelloIAmAdmin'),
                                    ('2','user','password');"""


#sql_update_tasks_table = """UPDATE tasks SET status = 'True' WHERE id = 2;"""

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.fetchall()
    except Error as e:
        print(e)

def insert_data_to_table(conn,expression):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(expression)
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def createDB():
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_tasks_table)
        insert_data_to_table(conn, sql_insert_users_table)
        insert_data_to_table(conn, sql_insert_tasks_table)
         
    if not path.exists(db_file):
        def create_connection(db_file):
            conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

def getTasks():
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * from tasks")
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def getTasksByUserID(userID):
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * from tasks where author = ?;", (userID,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def getOnline():
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT user,online from users;")
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def addTask(taskName, taskAuthor):
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        a = 'INSERT INTO tasks (task_text, author, status) VALUES ("%s", "%s", "False");' %(taskName,taskAuthor[0])
        cur.execute(a)
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def updateTask(taskName):
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('UPDATE "tasks" SET status = True WHERE task_text = \'%s\';' %(taskName))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def getUser(user):
    row = ""
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * from users where user=?",(user,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def getUserID(user):
    row = ""
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT id from users where user=?",(user,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row
   
def getAuthors():
    _out = []
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('SELECT user from "Users";')
        out = cur.fetchall()
        for i in out:
            _out.append(i[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return _out





#Продукты
def getProduct(id):
    conn=create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from products where id=?",(id))
    row = cur.fetchall()
    return row
def getAllProducts():
    conn = ""
    try:
       conn=sqlite3.connect(db_file)
       cur = conn.cursor()
       cur.execute("SELECT * from products")
       row = cur.fetchall()
       return row
    except Error as e:
       print(e)
    finally:
        if conn:
            conn.close()

#Корзина
def getBasket(user):
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from bucket where user=?;",(user,))
    row = cur.fetchall()
    return row
def insertProductsToBasket(user,product):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into bucket (user,product) values (?,?);",(user,product))
        row = cur.fetchall()
        cur.execute("select * from bucket;")
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def deleteProductsFromBasket(user):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DELETE from bucket WHERE user = ?;",(user,))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#Заказы
def insertOrder(user,datetime):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into orders (data, user) values (?,?);",(datetime, user))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def getOrders():
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from orders;")
    row = cur.fetchall()
    return row


#Пользователи
def insertUser(user,password):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into users(user,password) values (?,?);",(user,password))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def updateUser(user,password):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = ? WHERE user = ?;", (password,user))
        row = cur.fetchall()
        conn.commit()
        return conn.total_changes
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def updateOnline(user,datetime):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("UPDATE users SET online = ? WHERE user = ?;", (datetime,user))
        row = cur.fetchall()
        conn.commit()
        return conn.total_changes
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

