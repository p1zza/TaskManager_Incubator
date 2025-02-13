import requests
import subprocess
import time


PORT = 11000
host = '0.0.0.0'
usernameArray = ['elPiniato','UnicornImagination', 'LongBeardedSheep', 'RomanticGiraffe', 'MrBalalaika', 'LadyFirework', 'GiantDandelion', 'SuperBaby', 'PenguinNutella', 'BatSlipper', 'CatFrankfurter', 'MoonRabbit', 'VirusCompilux', 'BraveRubiksCube', 'PrincessBooger', 'ZombieTomato', 'SantaSteel', 'DoctorPineappleJam']
passwordArray = ['asd34dsa6','3ShGR9JmZ2',          'P7THgcm4bW',     'p6HwW8E7qa',       'hHBFYnrbV8',     'Tc3SZjCn2N', 'ebt2xaFqR8',  'Hx3XrpydsD',   'TFBZnqyNSa',   'pEsktzFKGM',   'WuAsZ29PHF',   'nzgeQJ6vtj',   'bK4FNWJ8CY',   'aCfm2HXUQG',   'hB56MUAVrd',       'tKJ7jGkEDd',       'YKHw3vUfTC','KVRmFPhf7B']


loginurl = f'http://{host}:{PORT}/login'
logouturl =f'http://{host}:{PORT}/logout'
registrationurl = f'http://{host}:{PORT}/registration'
profileurl = f'http://{host}:{PORT}/profile'
tasksurl = f'http://{host}:{PORT}/tasks'
onlineurl = f'http://{host}:{PORT}/online'
mainurl = f'http://{host}:{PORT}/'
i = 0

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
    
        subprocess.run(["gpio -1 mode 3 out"], shell=True)
        subprocess.run(["gpio -1 write 3 1"], shell=True)
        
        if not "200" in str(r):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif not "200" in str(r1):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif  not "200" in str(r2):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif not "200" in str(r3):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif not "200" in str(r4):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif not "200" in str(r5):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        elif not "200" in str(r6):
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 0"], shell=True)
        else:
            subprocess.run(["gpio -1 mode 3 out"], shell=True)
            subprocess.run(["gpio -1 write 3 1"], shell=True)
    except Exception:
        while(i <4):
            subprocess.run(["gpio -1 write 3 0"], shell=True)
            time.sleep(1)
            subprocess.run(["gpio -1 write 3 1"], shell=True)
            i+=1
        

def check():
    try:
        subprocess.run(["gpio -1 mode 5 out"], shell=True)
        subprocess.run(["gpio -1 write 5 1"], shell=True)

        r = requests.post(loginurl, data = {'username': 'user', 'password' : 'password'}, timeout = 50)
        dict_cookies = r.cookies.get_dict()
        dict_cookies["jwt"] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6W1syXV0sInVzZXIiOiJ1c2VyIiwicGFzc3dvcmQiOiJwYXNzd29yZCIsInJvbGUiOiJzdXBlckFkbWluIn0.A5art41ChmL_u1nS6YcIl9xumM-6d49iIwuTeITzwUI"
        r = requests.get(profileurl, cookies=dict_cookies, data = "")
        if "<li>Текущая роль - superAdmin</li>" in r.text:
            None
        else:
            subprocess.run(["gpio -1 write 5 0"], shell=True)
    except Exception:
        while(i <4):
            subprocess.run(["gpio -1 write 5 0"], shell=True)
            time.sleep(1)
            subprocess.run(["gpio -1 write 5 1"], shell=True)
            i+=1

def check_sqlinj():
    try:
        subprocess.run(["gpio -1 mode 7 out"], shell=True)
        subprocess.run(["gpio -1 write 7 1"], shell=True)

        r = requests.post(loginurl, data = {'username': 'user', 'password' : 'password'}, timeout = 50)
        dict_cookies = r.cookies.get_dict()
        r = requests.post(tasksurl, cookies=dict_cookies, data = 
                          {'action':'Посмотреть задачи','taskAuthorInput':'1\' UNION ALL SELECT * from users;--'})
        if "HelloIAmAdmin" in r.text:
            None
        else:
            subprocess.run(["gpio -1 write 7 0"], shell=True)
    except Exception:
        while(i <4):
            subprocess.run(["gpio -1 write 7 0"], shell=True)
            time.sleep(1)
            subprocess.run(["gpio -1 write 7 1"], shell=True)
            i+=1
    
def check_online():
    try:
        subprocess.run(["gpio -1 mode 8 out"], shell=True)
        subprocess.run(["gpio -1 write 8 1"], shell=True)

        r = requests.get(onlineurl, cookies = {}, data = "")
        if "<li>Добро пожаловать: []</li>" in r.text:
            None
        else:
            subprocess.run(["gpio -1 write 8 0"], shell=True)
    except Exception:
        while(i <4):
            subprocess.run(["gpio -1 write 8 0"], shell=True)
            time.sleep(1)
            subprocess.run(["gpio -1 write 8 1"], shell=True)
            i+=1

if __name__ == '__main__':
    ping()
    check()
    check_sqlinj()
    check_online()
