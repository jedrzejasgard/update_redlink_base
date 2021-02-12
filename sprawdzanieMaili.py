
import csv
from vendoasg.vendoasg import Vendo
from seleniumUpdate import updateRedlink
import configparser

config = configparser.ConfigParser()
config.read('setings.ini')

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))


def polaczListy(lis):
    l = []
    for elem in lis:
        #print('laczenie', elem)
        for item in elem:
            l.append(item)
    return l

def polaczAdresy(adr):
    l = []
    for item in adr:
        l.append(item)
    return l

def jakiJezyk(item):
    #jaki jezyk klienta
    for j in item['WartosciDowolne']:
        if(j.get('Nazwa'))=='wersja_jezykowa':
            if j.get('Wartosci'):
                return j.get('Wartosci')[0]
            else:
                pass


def listaOsobaID(item):
    listaKlientow = []
    for i in item['LudzieKlienta']:
        if i['CzyAktywna'] == True:
            for l in i["Powiazania"]:
                listaKlientow.append(l.get("OsobaKlientaID"))
        else:
            pass
    #print(listaKlientow)
    return listaKlientow


def wartoscProm(resp_prom):
    for i in resp_prom[0]['Wartosci']:
        if i.get('Nazwa') == 'Promocje_ludzie_klienta':
            return i.get('Wartosci')[0].lower()

def nazwaOpiekuna(opiekun):
    if opiekun == 10:
        return 'AgnieszkaSitek'
    elif opiekun == 27:
        return 'MagdalenaMikolajczyk'
    elif opiekun == 8:
        return 'MarlenaKluszczynska'
    elif opiekun == 7:
        return 'IwonaRosinska'
    elif opiekun == 13:
        return 'CezaryIdziak'
    elif opiekun == 9:
        return  'TomaszPiszczola'
    elif opiekun == 48:
        return  'JakubNieglos'
    elif opiekun == 83:
        return  'AleksandraBiegajlo'
    elif opiekun == 94:
        return  'MonikaBujakowska'
    elif opiekun == 131:
        return  'MariannaPrange'
    elif opiekun == 187:
        return  'PawelStrzelecki'
    elif opiekun == 194:
        return  'LukaszUrbanczyk'
    elif opiekun == 260:
        return  'MalgorzataSobaszek'
    elif opiekun == 62:
        return  'AdriannaTrafna'

def mail(item,dane):
    try:
        #print('ID osoby na TAK', item)
        for i in dane:
            for it in i['LudzieKlienta']:
                if item == it['ID']:
                    try:
                        for v in (it['Emaile']):
                            #print(v.get('Adres'))
                            return(v.get('Adres'))
                    except:
                        print('Nie znalazlem maila dla--', item )
    except IndexError:
        pass

def bibjson(data):
    added = []
    for item in data:
        added.append(item)
    return(added)

def downloadMails():
    
    listaOpiekunow = [9,27,8,7,13,10,48,83,94,131,187,194,260,62]
    #listaOpiekunow = [62]
    for opiekun in listaOpiekunow:
        opiek = nazwaOpiekuna(opiekun)
        print(opiek)

        listaPL = []
        listaDE =[]
        listaFR = []
        listaENG = []
        listaCZ = []

        mailePL = ['Email']
        maileENG = ['Email']
        maileDE = ['Email']
        maileFR = ['Email']
        maileCZ = ['Email']

        dataRepoALL = []
    # 1 LOOP
        ilosc_rekordow = 0
        response_data = vendoApi.getJson ('/json/reply/CRM_Klienci_KlientRozszerzony', {"Token":vendoApi.USER_TOKEN,"Model":{"ZwrocLudziKlienta":True, "ZwrocWartosciDowolne":True,"OpiekunID": opiekun,"Cursor":True, "Aktywnosci":["Aktywny", "Potencjalny"], "Funkcje":["Odbiorca"], "Strona":{"Indeks":0,"LiczbaRekordow":1000}}})
        repo_data = response_data['Wynik']['Rekordy']
        ilosc_rekordow = response_data['Wynik']['Strona']['LiczbaRekordow']
        dataRepoALL.append(bibjson(repo_data))
        if ilosc_rekordow >=1000:
            cursorresp = response_data["Wynik"]["Cursor"]["Nazwa"]
        else:
            pass
        
        for item in repo_data:
            slownik = jakiJezyk(item)
            if slownik == '344':
                listaPL.append(listaOsobaID(item))
            elif slownik == '342':
                listaENG.append(listaOsobaID(item))
            elif slownik == '837':
                listaCZ.append(listaOsobaID(item))
            elif slownik == '732':
                listaFR.append(listaOsobaID(item))
            elif slownik == '343':
                listaDE.append(listaOsobaID(item))

    #2 LOOP
        if ilosc_rekordow >=1000:
            response_data = vendoApi.getJson ('/json/reply/CRM_Klienci_KlientRozszerzony', {"Token":vendoApi.USER_TOKEN,"Model":{"ZwrocLudziKlienta":True, "ZwrocWartosciDowolne":True, "OpiekunID":opiekun, "Cursor":True, "Aktywnosci":["Aktywny", "Potencjalny"],"Funkcje":["Odbiorca"], "CursorNazwa": cursorresp, "Strona":{"Indeks":1000,"LiczbaRekordow":1000}}})
            ilosc_rekordow += response_data['Wynik']['Strona']['LiczbaRekordow']
        
            repo_data = response_data['Wynik']['Rekordy']
            print('----------------------------------------- 2 -------------------------------------------')

            dataRepoALL.append(bibjson(repo_data))

            for item in repo_data:
                slownik = jakiJezyk(item)
                if slownik == '344':
                    listaPL.append(listaOsobaID(item))
                elif slownik == '342':
                    listaENG.append(listaOsobaID(item))
                elif slownik == '837':
                    listaCZ.append(listaOsobaID(item))
                elif slownik == '732':
                    listaFR.append(listaOsobaID(item))
                elif slownik == '343':
                    listaDE.append(listaOsobaID(item))
        else:
            pass
        

    # 3 LOOP
        if ilosc_rekordow >=1000:
            response_data = vendoApi.getJson ('/json/reply/CRM_Klienci_KlientRozszerzony', {"Token":vendoApi.USER_TOKEN,"Model":{"ZwrocLudziKlienta":True, "ZwrocWartosciDowolne":True, "OpiekunID":opiekun, "Cursor":True, "Aktywnosci":["Aktywny", "Potencjalny"],"Funkcje":["Odbiorca"], "CursorNazwa": cursorresp, "Strona":{"Indeks":2000,"LiczbaRekordow":1000}}})
            ilosc_rekordow += response_data['Wynik']['Strona']['LiczbaRekordow']
        
            repo_data = response_data['Wynik']['Rekordy']
            print('----------------------------------------- 2 -------------------------------------------')

            dataRepoALL.append(bibjson(repo_data))

            for item in repo_data:
                slownik = jakiJezyk(item)
                if slownik == '344':
                    listaPL.append(listaOsobaID(item))
                elif slownik == '342':
                    listaENG.append(listaOsobaID(item))
                elif slownik == '837':
                    listaCZ.append(listaOsobaID(item))
                elif slownik == '732':
                    listaFR.append(listaOsobaID(item))
                elif slownik == '343':
                    listaDE.append(listaOsobaID(item))
        else:
            pass

    # Czy osoba ma promocje na TAK 

        CalaListaPL = polaczListy(listaPL)
        CalaListaDE = polaczListy(listaDE)
        CalaListaFR = polaczListy(listaFR)
        CalaListaENG = polaczListy(listaENG)
        CalaListaCZ = polaczListy(listaCZ)

        print('Ilość znalezionych ludzi klienta (aktywnych/potencjalnych) PL: ',len(CalaListaPL))
        print('Ilość znalezionych ludzi klienta (aktywnych/potencjalnych) DE: ',len(CalaListaDE))
        print('Ilość znalezionych ludzi klienta (aktywnych/potencjalnych) FR: ',len(CalaListaFR))
        print('Ilość znalezionych ludzi klienta (aktywnych/potencjalnych) ENG: ',len(CalaListaENG))
        print('Ilość znalezionych ludzi klienta (aktywnych/potencjalnych) CZ: ',len(CalaListaCZ))

        osobyTAKPL = []
        osobyTAKDE = []
        osobyTAKFR = []
        osobyTAKENG = []
        osobyTAKCZ = []

        for item in CalaListaPL:
            prom = vendoApi.getJson ('/json/reply/DB_WartosciDowolne', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"CzlowiekKlienta","ObiektyID":item,"Nazwy":["Promocje_ludzie_klienta"], "ZwrocPusteWartosci":True,}})
            resp_prom = prom['Wynik']['Rekordy']
            if wartoscProm(resp_prom) == 'tak':
                osobyTAKPL.append(item)
        print('---------------------PL Ilosc osob na tak :',len(osobyTAKPL))

        for item in CalaListaDE:
            prom = vendoApi.getJson ('/json/reply/DB_WartosciDowolne', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"CzlowiekKlienta","ObiektyID":item,"Nazwy":["Promocje_ludzie_klienta"], "ZwrocPusteWartosci":True,}})
            resp_prom = prom['Wynik']['Rekordy']
            if wartoscProm(resp_prom) == 'tak':
                osobyTAKDE.append(item)
        print('---------------------DE Ilosc osob na tak :',len(osobyTAKDE))

        for item in CalaListaFR:
            prom = vendoApi.getJson ('/json/reply/DB_WartosciDowolne', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"CzlowiekKlienta","ObiektyID":item,"Nazwy":["Promocje_ludzie_klienta"], "ZwrocPusteWartosci":True,}})
            resp_prom = prom['Wynik']['Rekordy']
            if wartoscProm(resp_prom) == 'tak':
                osobyTAKFR.append(item)
        print('---------------------FR Ilosc osob na tak :',len(osobyTAKFR))

        for item in CalaListaENG:
            prom = vendoApi.getJson ('/json/reply/DB_WartosciDowolne', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"CzlowiekKlienta","ObiektyID":item,"Nazwy":["Promocje_ludzie_klienta"], "ZwrocPusteWartosci":True,}})
            resp_prom = prom['Wynik']['Rekordy']
            if wartoscProm(resp_prom) == 'tak':
                osobyTAKENG.append(item)
        print('---------------------ENG Ilosc osob na tak :',len(osobyTAKENG))

        for item in CalaListaCZ:
            prom = vendoApi.getJson ('/json/reply/DB_WartosciDowolne', {"Token":vendoApi.USER_TOKEN,"Model":{"ObiektTypDanych":"CzlowiekKlienta","ObiektyID":item,"Nazwy":["Promocje_ludzie_klienta"], "ZwrocPusteWartosci":True,}})
            resp_prom = prom['Wynik']['Rekordy']
            if wartoscProm(resp_prom) == 'tak':
                osobyTAKCZ.append(item)
        print('---------------------CZ Ilosc osob na tak :',len(osobyTAKCZ))

    #dodawanie maili ludzi klienta z promocja na TAK 
        dataRepoALL = polaczListy(dataRepoALL)
        d = dataRepoALL

        for osoba in osobyTAKPL:
            mailePL.append(mail(osoba,d))

        for osoba in osobyTAKDE:
            maileDE.append(mail(osoba,d))

        for osoba in osobyTAKFR:
            maileFR.append(mail(osoba,d))

        for osoba in osobyTAKENG:
            maileENG.append(mail(osoba,d))

        for osoba in osobyTAKCZ:
            maileCZ.append(mail(osoba,d))

        #len(mailePL)-1 odejmuje pierwszy rekord któym jest wartość'email' potrzebna do wgrania listy na redlink
        print('Ilosc znalezionych maili PL: ',len(mailePL)-1)
        print('Ilosc znalezionych maili DE: ',len(maileDE)-1)
        print('Ilosc znalezionych maili FR: ',len(maileFR)-1)
        print('Ilosc znalezionych maili ENG: ',len(maileENG)-1)
        print('Ilosc znalezionych maili CZ: ',len(maileCZ)-1)

    #zapisywanie do plików
        mypath = r'.\\listymailingowe'
        if len(maileENG) > 5:
            with open(mypath+'\\'+str(opiek)+'_EN.csv' ,'w', encoding='utf-8', newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in maileENG:
                    if item:
                        try:
                            writer.writerow([item])
                        except:
                            print('niezapisałem ENG')
                            pass
        if len(maileFR) > 5:
            with open(mypath+'\\'+str(opiek)+'_FR.csv' ,'w', encoding='utf-8', newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in maileFR:
                    if item:
                        try:
                            writer.writerow([item])
                        except:
                            print('niezapisałem FR')
                            pass
        if len(maileDE) > 5:
            with open(mypath+'\\'+str(opiek)+'_DE.csv' ,'w', encoding='utf-8', newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in maileDE:
                    if item:
                        try: 
                            writer.writerow([item])
                        except:
                            print('niezapisałem DE')
                            pass
        if len(maileCZ) > 5:
            with open(mypath+'\\'+str(opiek)+'_CZ.csv' ,'w', encoding='utf-8', newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in maileCZ:
                    if item:
                        try:
                            writer.writerow([item])
                        except:
                            print('niezapisałem CZ')
                            pass
        if len(mailePL) > 5:
            with open(mypath+'\\'+str(opiek)+'_PL.csv' ,'w', encoding='utf-8', newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in mailePL:
                    if item:
                        try:
                            writer.writerow([item])
                        except:
                            pass
                    
if __name__ == "__main__":
    downloadMails()
    updateRedlink()