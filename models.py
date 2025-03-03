
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
                            "online" text); """

sql_insert_tasks_table = """INSERT INTO tasks (id, task_text, author, status) VALUES 
                                        ('1', 'Открыть дверь холодильника', 'admin', 'False'),
                                        ('2', 'Положить в холодильник слона', 'admin', 'False'),
                                        ('3', 'Закрыть дверь холодильника', 'admin', 'False');
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
        cur.execute("SELECT * from tasks where author = ?", (userID,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row

def getTasksByName(username):
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        a = str("SELECT * from tasks where author = '" + username + "';")
        cur.execute(a)
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
        
def updateOnline(username, datetime):
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('UPDATE "users" SET online = %s WHERE user = %s' %(datetime,username))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def addTask(taskName, taskAuthor):
    row = ""
    try:
        conn=sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (task_text, author, status) VALUES (?,?,?)",(taskName,taskAuthor,False))
        conn.commit()
        #row = cur.fetchall()
        res = cur.execute("SELECT task_text FROM tasks ")
        out = res.fetchall()
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
        cur.execute("SELECT * FROM users WHERE user = ?",(user,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row
        
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

def getUserID(user):
    row = ""
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT id from users where user= ? ",(user,))
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
