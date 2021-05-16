import firebase_admin
from firebase_admin import credentials
from pathlib import Path
from firebase_admin import db
from datetime import datetime

def DBconnect():
    databaseUrl = "your-url"
    path = Path("credential-file.json")
    cred = credentials.Certificate(path)
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': databaseUrl})
    #print(default_app.name)  # "[DEFAULT]"

def calculateAvgRating(voti):
    votilist = voti.split(";")
    #print(votilist)
    media = i = 0
    for val in votilist:
        media += float(val)
        i += 1
    if i == 0:
        return 0
    return float("{:.1f}".format(media/i))


def translate():
    ref = db.reference("/tabellone")
    data = dict(ref.get())
    ratingsGroupped = {} #{string:string}
    for k in data:
        voto = data[k]["attr1"]
        voto = str(voto)
        numero = data[k]["attr2"]
        if(numero in ratingsGroupped.keys()):
            voto = ";"+str(voto)
            ratingsGroupped[numero] += voto
        else:
            ratingsGroupped[numero] = voto
    #print(ratingsGroupped)

    ratingsAVG = {} #id ->AVG
    for k in ratingsGroupped:
        voti = ratingsGroupped[k]
        media = calculateAvgRating(voti)
        ratingsAVG[k]=media
    #print(ratingsAVG)

    #PUSH DEI DATI SUL DB
    ref = db.reference("/tabellaRiassuntiva")

    for k in ratingsAVG:
        ref.child(k).set(ratingsAVG[k])

    ref = db.reference("/lastUpdate")
    now = datetime.now()
    #print("Today's date:", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    ref.set(dt_string)
    print("OK - " + dt_string)

if __name__ == '__main__':
    DBconnect()
    translate()
