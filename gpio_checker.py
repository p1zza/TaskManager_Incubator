import requests
from checklib import *
import re
import subprocess


PORT = 11000
host = '0.0.0.0'
usernameArray = ['elPiniato','UnicornImagination', 'LongBeardedSheep', 'RomanticGiraffe', 'MrBalalaika', 'LadyFirework', 'GiantDandelion', 'SuperBaby', 'PenguinNutella', 'BatSlipper', 'CatFrankfurter', 'MoonRabbit', 'VirusCompilux', 'BraveRubiksCube', 'PrincessBooger', 'ZombieTomato', 'SantaSteel', 'DoctorPineappleJam']
passwordArray = ['asd34dsa6','3ShGR9JmZ2',          'P7THgcm4bW',     'p6HwW8E7qa',       'hHBFYnrbV8',     'Tc3SZjCn2N', 'ebt2xaFqR8',  'Hx3XrpydsD',   'TFBZnqyNSa',   'pEsktzFKGM',   'WuAsZ29PHF',   'nzgeQJ6vtj',   'bK4FNWJ8CY',   'aCfm2HXUQG',   'hB56MUAVrd',       'tKJ7jGkEDd',       'YKHw3vUfTC','KVRmFPhf7B']


def ping():
    r = requests.get(f'http://{host}:{PORT}/', timeout=3)
    r1 = requests.get(f'http://{host}:{PORT}/logout', timeout=3)
    r2 = requests.get(f'http://{host}:{PORT}/registration', timeout=3)
    r3 = requests.get(f'http://{host}:{PORT}/login', timeout=3)
    r4 = requests.get(f'http://{host}:{PORT}/online', timeout=3)
    r5 = requests.get(f'http://{host}:{PORT}/tasks', timeout=3)
    r6 = requests.get(f'http://{host}:{PORT}/profile', timeout=3)

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

def check():
    loginurl = f'http://{host}:{PORT}/login'
    profileurl = f'http://{host}:{PORT}/profile'

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

    




'''
def check(self):
    try:



def put_flag(self, flag_id, flag,vuln):
    host_id = str(self.checker.host)
    octets = host_id.split('.')
    host_id = octets[2]
    host_id = int(host_id)
    if int(host_id) > 17:
        host_id = 4

    rdata = {"id":flag_id, "value":flag}
    registerurl = f'http://{self.checker.host}:{PORT}/registration'
    loginurl = f'http://{self.checker.host}:{PORT}/login'
    cargogurl = f'http://{self.checker.host}:{PORT}/cargo'
    stationurl = f'http://{self.checker.host}:{PORT}/station'
    try:
        r = requests.post(registerurl, data= {'username': usernameArray[host_id], 'password' : passwordArray[host_id]}, timeout=50)
        self.checker.check_response(r, 'Could not put flag')
        if "<li>Учетная запись занята</li>" in r.text:
            r = requests.post(loginurl, data = {'username': usernameArray[host_id], 'password' : passwordArray[host_id]}, timeout = 50)
            jwt = r.cookies.get("jwt")
            cookies = {'jwt': jwt}
            r = requests.get(stationurl, timeout=3)
            r = requests.post(stationurl, cookies=cookies, data = {'AddCargoButton':'AddCargoButton', 'AddedCargoTypeArrayDropdown':'Наука', 'AddedCargoName':flag_id, 'AddedCargoAmount': '1', 'AddedCommentCargoSteal': flag})
        if "<li>Успешная регистрация</li>" in r.text:
            r = requests.post(loginurl, data = {'username': 'Alex', 'password' : '53967b964ff4e8844b1'}, timeout = 50)
            jwt = r.cookies.get("jwt")
            cookies = {'jwt': jwt}
            r = requests.get(stationurl, timeout=3)
            r = requests.post(stationurl, cookies=cookies, data = {'AddCargoButton':'AddCargoButton', 'AddedCargoTypeArrayDropdown':'Наука', 'AddedCargoName':flag_id, 'AddedCargoAmount': '1', 'AddedCommentCargoSteal': flag})
        return flag_id
    except Exception as e:
        print(str(e))
        self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in put_flag')

    def get_flag(self, flag_id,vuln):
        registerurl = f'http://{self.checker.host}:{PORT}/registration'
        loginurl = f'http://{self.checker.host}:{PORT}/login'
        cargogurl = f'http://{self.checker.host}:{PORT}/cargo'
        stationurl = f'http://{self.checker.host}:{PORT}/station'
        try:
            host_id = str(self.checker.host)
            octets = host_id.split('.')
            host_id = octets[2]
            host_id = int(host_id)
            if int(host_id) > 17:
                 host_id = 4
            r = requests.post(loginurl, data = {'username': usernameArray[host_id], 'password' : passwordArray[host_id]}, timeout = 50)
            jwt = r.cookies.get("jwt")
            cookies = {'jwt': jwt}
            r = requests.get(cargogurl, timeout=3)
            match = re.search(r"\<pre\>(.*?3)\: (\d+)",r.text)
            passw = match.group(2)
            r = requests.post(stationurl, cookies=cookies, data = {'passScienceSteal':passw, 'ScienceSteal':'ScienceSteal','cargoScienceName':flag_id})
            match = re.search(r"<li>(?!<a>)(.*?)<\/li>",r.text)
            return match.group(1)
            #return flag.text[18:-1].split(",")[2].split(":")[1][3:-2]
        except Exception as e:
            self.checker.cquit(Status.MUMBLE, 'Services not working correctly', 'Services not working correctly in get_flag')
            print(e)
'''

if __name__ == '__main__':
    ping()
    check()
