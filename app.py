from flask import Flask, redirect, render_template, request, request_started, url_for, flash, make_response
from flask.logging import default_handler
from flask_login import LoginManager,login_user,login_required, logout_user
import models
import jwt
import re
import datetime
from urllib.parse import urlparse

app = Flask(__name__)
models.createDB()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
userlogin = ""

app.secret_key = "supersecretKey"


@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return redirect(url_for('login'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = str(request.form['username'])
        password = str(request.form['password'])
        if not validate(str(login)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("registration.html")
        if not validate(str(password)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("registration.html")

        out = models.getUser(login)
        if len(out)== 0:
            models.insertUser(login,password)
            flash("Успешная регистрация")
            return redirect(url_for('login'))
        else:
            flash("Учетная запись занята")
            return render_template('registration.html')
    if request.method == 'GET':
        return render_template('registration.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if not validate(str(username)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("login.html")
        if not validate(str(password)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("login.html")

        row = models.getUser(username)
        arr = []
        if len(row)!=0:
            for i in row[0]:
                arr.append(i)
            if(password!=arr[2]):
                flash("Неверный пароль / логин")
                return render_template("login.html")
            else:
                userlogin = UserLogin().create(arr[1])
                login_user(userlogin)
                flash("Успешный вход")
                content = {}
                content ['username'] = []
                content ['username'] = username
                UserId = models.getUserID(username)
                models.updateOnline(username, datetime.datetime.now())
                response = make_response(render_template("profile.html",context = content,cookies = request.cookies))
                data = {"id": UserId, "user" : username, "password" : password, "role": "user"}
                if username == "admin": 
                    data = {"id": UserId, "user" : username, "password" : password, "role": "admin"}
                token = encodeJWT(data)
                response.set_cookie("jwt", token)
                return response
        else:
            flash("Неверный пароль / логин")
            return render_template("login.html")

    if request.method == 'GET':
        return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    response = make_response(render_template("login.html",cookies = request.cookies))
    response.set_cookie("jwt","")
    flash("Вы вышли из аккаунта","success")
    return redirect(url_for('login')) #render_template("login.html") 

@app.route('/profile',methods=['GET'])
@login_required
def profile():
    if request.method == 'GET':
        content = {}
        content ['username'] = []
        token = request.cookies.get("jwt")
        token_data = decodeJWT(token)
        username = token_data.get('user')
        content ['username'] = username
        UserID = models.getUserID(username)
        UserID = UserID[0]
        row = models.getTasksByUserID(UserID[0])
        flash ("Текущая роль - " + token_data.get('role'))
        if len(row) != 0:
            return (render_template("profile.html",context = content, headings = ("Номер записи","Текст","Автор","Выполнено"), data = row))
        else:
            flash ("Пользователь не имеет задач")
            return (render_template("profile.html",context = content, headings = ("","","",""), data = row))

@app.route('/tasks',methods=['GET','POST'])
@login_required
def tasks():
    content = {}
    content ['username'] = []
    token = request.cookies.get("jwt")
    token_data = decodeJWT(token)
    username = token_data.get('user')
    content ['username'] = username    
    UserID = models.getUserID(username)
    UserID = UserID[0]
    row = models.getTasksByUserID(UserID[0])
    TaskNameArray = []
    
    if token_data.get('role') == 'admin':  
        row = models.getTasks()
    
    
    for name in row:
        TaskNameArray.append(name[1])
    
    AuthorArray = models.getAuthors()
    
    if request.method == 'GET':
        if len(row) != 0:
            return (render_template("tasks.html",AuthorArray = AuthorArray, TaskNameArray = TaskNameArray, context = content, headings = ("Номер записи","Текст","Автор","Выполнено"), data = row))
        else:
            flash ("Пользователь не имеет задач")
            return (render_template("tasks.html", AuthorArray = AuthorArray, TaskNameArray = TaskNameArray, context = content, headings = ("","","",""), data = row))

    if request.method == 'POST':
        if request.form['action'] == 'Добавить задачу':
            taskName = str(request.form['taskNameInput'])
            taskAuthor = request.form.get('taskAuthor')
            authorID = models.getUserID(taskAuthor)
            models.addTask(taskName, authorID[0])
            row = models.getTasksByName(taskAuthor)
            flash("Задача успешно добавлена")
            return (render_template("tasks.html", AuthorArray = AuthorArray, TaskNameArray = TaskNameArray,context = content, headings = ("Номер записи","Текст","Автор","Выполнено"), data = row))
        if request.form['action'] == "Закрыть задачу":
            taskName = request.form.get('taskNameDropDown')
            models.updateTask(taskName)
            row = models.getTasksByName(taskAuthor)
            return (render_template("tasks.html", AuthorArray = AuthorArray, TaskNameArray = TaskNameArray, context = content, headings = ("Номер записи","Текст","Автор","Выполнено"), data = row))
        if request.form['action'] == "Посмотреть задачи":
            taskAuthor = request.form.get('taskAuthorInput')
            row = models.getTasksByName(taskAuthor)
            flash("Отображены задачи пользователя:" + taskAuthor)
            return (render_template("tasks.html", AuthorArray = AuthorArray, TaskNameArray = TaskNameArray, context = content, headings = ("Номер записи","Текст","Автор","Выполнено"), data = row))


@app.route('/online')
#@login_required
def online():
    content = {}
    content ['username'] = []
    token = request.cookies.get("jwt")
    if token!=None:
        token_data = decodeJWT(token)
        username = token_data.get('user')
        content ['username'] = username
        row = models.getOnline()
        flash ("Текущая роль - " + token_data.get('role'))
        flash ("Доступ до страницы только для авторизованных пользователей!")
    else:
        row = models.getOnline()  

    return (render_template("online.html",context = content, headings = ("Пользователь","Последний онлайн"), data = row))


@app.errorhandler(404) 
def not_found(e):   
    return render_template("404.html") 

def encodeJWT(data):
    token = ""
    token = jwt.encode(data, "secret")
    return token.decode('UTF-8')
def decodeJWT(token):
    data = jwt.decode(token, "secret", algorithms=["HS256"], verify=True)
    return data

@login_manager.unauthorized_handler
def unauthorized():
    flash("Войдите в аккаунт")
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(userlogin):
    return UserLogin().fromDB(userlogin)

def validate(s):
    # Регулярное выражение для проверки, содержит ли строка только буквы и цифры
    regex = re.compile(r'^[a-zA-Z0-9]+$')
    ss = str(s)
    a = regex.match(str(s))
    if a !=None:
        return True
    else:
        return False

class UserLogin():
    def fromDB(self,user):  
        self.__user = models.getUserID(user)
        return self
    def create (self,user):
        self.__user=user
        return self
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        out = ""
        id = models.getUserID(self.__user)
        if len(id)!=0:
            for i in id:
                out = i
                break
            return out[0]
        else:
            return NULL

if __name__ == '__main__':
    app.run(debug=True, port = 11000, host='0.0.0.0')