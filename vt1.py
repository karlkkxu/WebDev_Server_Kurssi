#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import urllib as url
import simplejson as json

# Palauttaa aakkosjärjestyksessä kaikkien tietorakenteesta löytyvien joukkueiden nimet (STRINGINÄ)
def jarjestaJoukkueet(data):
    joukkueLista = []

    for sarja in data["sarjat"]:
        for joukkue in sarja["joukkueet"]:
            joukkueLista.append(joukkue["nimi"])

    joukkueLista.sort(key=str.casefold)
    #print(joukkueLista)
    joukkueetString = ""
    for joukkue in joukkueLista:
        joukkueetString += joukkue
        joukkueetString += "\n"

    #print(joukkueetString)
    return joukkueetString

# Lisää joukkueen pyydettyyn sarjaan
def lisaaJoukkue(data, sarja, joukkue):

    #Tarkista sarja - identtinen johonkin jo olemassaolevaan
    loytyyDatasta = False
    for sarjat in data["sarjat"]:
        if (sarja == sarjat):
            loytyyDatasta = True
            break
    if loytyyDatasta == False:
        print("Annettu sarja ei ole validi (ei löydy datasta)")
        return

    #Tarkista joukkuedictin eheys
    try:
        for avain in data["sarjat"][0]["joukkueet"][0]:
            if type(data["sarjat"][0]["joukkueet"][0][avain]) != type(joukkue[avain]):
                print("Joukkue ei validi")
    except:
        print("Joukkue ei validi")

    #uusi uniikki ID
    IDt = set()
    for sarjat in data["sarjat"]:
        for joukkueet in sarjat["joukkueet"]:
            IDt.add(joukkueet["id"])

    joukkue["id"] = max(IDt) + 1
    #print(joukkue["id"])
    sarja["joukkueet"].append(joukkue)

#Palauttaa YHDEN MERKKIJONON jossa kaikki kokonaisluvulla alkavien rastien koodit puolipisteellä eroteltuina
def kokonaisLukuRastit(data):
    rastitString = ""
    for rasti in data["rastit"]:
        if rasti["koodi"][0].isdigit():
            rastitString += rasti["koodi"] + ';'

    rastitString = rastitString[:-1]
    #print(rastitString)
    return rastitString

#Tallentaa tietorakenteen .json tiedostoon
def dumpFile(data):
    with open('./mysite/data.json', 'w') as file:
        json.dump(data, file)

#Poistaa nimen ja sarjan perusteella joukkueen tietorakenteesta
def poistaJoukkue(data, sarja, nimi):

    #Tarkista sarja - identtinen johonkin jo olemassaolevaan
    loytyyDatasta = False
    for sarjat in data["sarjat"]:
        if (sarja == sarjat):
            loytyyDatasta = True
            oikeaSarja = sarjat
            break
    if loytyyDatasta == False:
        print("Annettu sarja ei ole validi (ei löydy datasta)")

    #Etsitään sarjasta samanniminen joukkue (oletetaan että nimet uniikkeja)
    for joukkueet in oikeaSarja["joukkueet"]:
        #Oletetaan myös että missään joukkueen nimessä ei ole kirjainta jotka rikkovat .lower() vertailun
        if (joukkueet["nimi"].lower() == nimi.lower()):
            oikeaSarja["joukkueet"].remove(joukkueet)
            return
    
    #print("Joukkuetta ei löytynyt")

#Apufunktio; palauttaa tietorakenteesta viittauksen koko sarjaan sarjan nimen perusteella tai None jos annetun nimistä sarjaa ei ole
def etsiSarjaNimella(data, sarjanNimi):
    for sarja in data["sarjat"]:
        if (sarja["nimi"] == sarjanNimi):
            return sarja
    return None

#Apufunktio; luo oikeanmallisen joukkuedictin annetuilla tiedoilla
def luoJoukkue(joukkueenNimi, jasentenNimet):
    joukkueLisa = {
    "nimi": joukkueenNimi,
    "jasenet": [],
    "id": 1234,
    "leimaustapa": [],
    "rastit": []
    }
    for jasen in jasentenNimet:
        joukkueLisa["jasenet"].append(jasen)
    return joukkueLisa

#TÄMÄ JÄI KESKEN
#Palauttaa stringinä joukkueet jäsenineen pisteiden mukaan järjestettynä
def jarjestaJoukkueetPisteineen(data):
    joukkueetJaPisteet = []
    lahtoRastiID = 0
    maaliRastiID = 0

    #Haetaan valmiiksi tärkeimpien rastien IDt
    for rasti in data["rastit"]:
        if rasti["koodi"] == "MAALI":
            maaliRastiID = rasti["id"]
        if rasti["koodi"] == "LAHTO":
            lahtoRastiID = rasti["id"]

    #Tässä lasketaan jokaiselle joukkueelle rastien mukaiset pisteet.
    #Ei toimi kunnolla, mutta dedis puskee päälle
    for sarja in data["sarjat"]:
        for joukkue in sarja["joukkueet"]:
            #Yhdelle joukkueelle
            lastLahtoRasti = 0
            pisteSumma = 0
            for i in range(len(joukkue["rastit"])):
                if joukkue["rastit"][i]["rasti"] == lahtoRastiID:
                    lastLahtoRasti = i
            rastiLista = []
            for i in range(lastLahtoRasti, (len(joukkue["rastit"]))):
                if joukkue["rastit"][i]["rasti"] == maaliRastiID:
                    break
                rastiLista.append(joukkue["rastit"][i]["rasti"])
            uniikitRastit = set(rastiLista)
            for rasti in uniikitRastit:
                for rastiOG in data["rastit"]:
                    if rasti == rastiOG["id"]:
                        if rastiOG["koodi"][0].isdigit():
                            pisteSumma += int(rastiOG["koodi"][0])
                        break
            joukkueetJaPisteet.append((joukkue, pisteSumma))
                    #Etsitään viimeisin lähtöleimaus
                    #listataan kaikki rastit viimeisimmän lähdön jälkeen kunnes tulee loppuleimaus
                    #Kutistetaan lista rasteista niin että duplikaatit poistuvat
                    #Iteroidaan uniikki lista ja etsitään jokaista rastia vastaava koodi rastirakenteesta (jos ei löydy vastinetta niin 0p) - lisätään suoraan sitä vastaava pistemäärä summaan
    
    palautusString = ""
    joukkueetJaPisteetSorted = sorted(joukkueetJaPisteet, key = lambda tup: tup[1], reverse=True)
    for joukkue in joukkueetJaPisteetSorted:
        palautusString += joukkue[0]["nimi"] + ' (' + str(joukkue[1]) + ' p)\n  '
        for jasen in joukkue[0]["jasenet"]:
            palautusString += jasen + '\n  '
        palautusString = palautusString[:-2]
    return palautusString
        

#--------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/vt1')
def t_rasa():

    #Haetaan kaikki mahdolliset kiinnostavat parametrit muuttujiin
    joukkueenNimi = request.args.get("nimi")
    jasentenNimet = request.args.getlist("jasen")
    sarjanNimi    = request.args.get("sarja")
    
    resetQuery = request.args.get("reset")
    stateQuery = request.args.get("tila")

    #Ensin tarkistetaan resetoidaanko tiedosto vai ei
    #Asetetaan oletusarvoksi lokaali datatiedosto (Paitsi jos sellaista ei ole)
    try:
        with open('./mysite/data.json') as jFile:
            data = json.load(jFile)
    except: #Tapahtuu ensimmäisellä ajokerralla uudessa lokaatiossa, tai jos tiedosto on poistettu
        data = json.load(url.request.urlopen('http://hazor.eu.pythonanywhere.com/2021/data.json'))
    
    #Sitten testataan jos halutaan resetoida tiedosto - helpompi tehdä tässä järjestyksessä
    try:
        if int(resetQuery) == 1: #Resetoinnin query on validi syöte luottevina ykköseksi - tämä on ainoa vaihtoehto jolla datan arvoksi asetetaan alkuperäisestä lähteestä haettu tiedosto
            data = json.load(url.request.urlopen('http://hazor.eu.pythonanywhere.com/2021/data.json')) 
    except:
        print("ResetQueryn vertailu epäonnistui") 

    #Kun tiedetään mitä dataa käsitellään, tarkistetaan poistetaanko vai lisätäänkö
    try:
        if (stateQuery == "delete"): #Ainoa vaihtoehto tiedon poistamiseksi
            #Muiden querysyötteiden eheys tarkastetaan poistofunktiossa
            poistaJoukkue(data, etsiSarjaNimella(data, sarjanNimi), joukkueenNimi)
        
        else: #Jos statequery on olemassa, mutta ei ole "delete" - lisätään
            #lisaaJoukkue tarkistaa syötteen eheyden
            lisaaJoukkue(data, etsiSarjaNimella(data, sarjanNimi), luoJoukkue(joukkueenNimi, jasentenNimet))
    except: #Jos statequeryn vertailussa on ongelmia - oletetaan että sitä ei ole määritelty joten lisätään
        lisaaJoukkue(data, etsiSarjaNimella(data, sarjanNimi), luoJoukkue(joukkueenNimi, jasentenNimet))
        print("Poistotilaa ei tunnistettu - yritettiin lisätä")

    dumpFile(data)
    return Response((
        jarjestaJoukkueet(data) + "\n\n" + kokonaisLukuRastit(data) # Ykköstason tulosteet
        + "\n\n------------------------------------------------------\nKolmostason tulosteet:\n\n" +
        jarjestaJoukkueetPisteineen(data)
        ), mimetype="text/plain")


@app.route('/data.json')
def getData():
    with open('./mysite/data.json', 'r') as file:
        jsonData = file.read()
    return Response(jsonData, mimetype="text/plain")

