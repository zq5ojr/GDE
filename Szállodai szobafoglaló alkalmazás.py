from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def informacio(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, tipus):
        super().__init__(szobaszam, 10000)
        self.tipus = tipus

    def informacio(self):
        return f"Szobaszám: {self.szobaszam}. Egyágyas szoba {self.tipus} - {self.ar} Ft/éjszaka"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, tipus):
        super().__init__(szobaszam, 20000)
        self.tipus = tipus

    def informacio(self):
        return f"Szobaszám: {self.szobaszam}. Kétágyas szoba {self.tipus} - {self.ar} Ft/éjszaka"

class Szalloda:
    def __init__(self):
        self.szobak = {
            1: EgyagyasSzoba(1, "Egyágyas szoba erkéllyel"),
            2: EgyagyasSzoba(2, "Egyágyas apartman szoba"),
            3: EgyagyasSzoba(3, "Egyágyas szoba jakuzzival"),
            4: KetagyasSzoba(4, "Kétágyas szoba erkéllyel"),
            5: KetagyasSzoba(5, "Kétágyas apartman szoba"),
            6: KetagyasSzoba(6, "Kétágyas szoba jakuzzival")
        }

class Foglalas:
    def __init__(self, szobaszam, kezdo_datum, befejezo_datum):
        self.szobaszam = szobaszam
        self.kezdo_datum = kezdo_datum
        self.befejezo_datum = befejezo_datum

szalloda = Szalloda()
foglalasok = []
foglalasok.append(Foglalas(1, datetime(2024, 5, 1), datetime(2024, 5, 5)))
foglalasok.append(Foglalas(4, datetime(2024, 5, 10), datetime(2024, 5, 15)))
foglalasok.append(Foglalas(6, datetime(2024, 5, 20), datetime(2024, 5, 25)))
foglalasok.append(Foglalas(2, datetime(2024, 6, 1), datetime(2024, 6, 5)))
foglalasok.append(Foglalas(5, datetime(2024, 6, 10), datetime(2024, 6, 15)))
def foglalas_osszeg(szoba, kezdo_datum, befejezo_datum):
    napok_szama = (befejezo_datum - kezdo_datum).days
    return szoba.ar * napok_szama

def kiiras_foglalasok():
    if foglalasok:
        print("Az eddig foglalt szobák:")
        for foglalas in foglalasok:
            print(f"Szobaszám: {foglalas.szobaszam}, Kezdő dátum: {foglalas.kezdo_datum}, Befejező dátum: {foglalas.befejezo_datum}")
    else:
        print("Nincs foglalás rögzítve.")

def foglalas():
    print("Választható szobák:")
    print("1. Egyágyas szoba")
    print("2. Kétágyas szoba")
    
    szobatipus = input("Kérlek válassz szobatípust (1 vagy 2): ")
    if szobatipus == "1":
        for szobaszam, szoba in szalloda.szobak.items():
            if isinstance(szoba, EgyagyasSzoba):
                print(szoba.informacio())
    elif szobatipus == "2":
        for szobaszam, szoba in szalloda.szobak.items():
            if isinstance(szoba, KetagyasSzoba):
                print(szoba.informacio())
    else:
        print("Hibás választás.")
        return
    
    szobaszam = int(input("Kérlek válassz szobaszámot: "))
    if szobatipus == "1" and szobaszam not in [1, 2, 3]:
        print("Hibás szobaszám.")
        return
    elif szobatipus == "2" and szobaszam not in [4, 5, 6]:
        print("Hibás szobaszám.")
        return
    kezdo_datum = input("Kérlek add meg a kezdő dátumot (YYYY-MM-DD formátumban): ")
    befejezo_datum = input("Kérlek add meg a befejező dátumot (YYYY-MM-DD formátumban): ")
    
    try:
        datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
        if datum < datetime.now():
            print("A megadott dátum a múltban van. Kérlek adj meg egy jövőbeli dátumot.")
            return
        kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
        befejezo_datum = datetime.strptime(befejezo_datum, "%Y-%m-%d")
    except ValueError:
        print("Hibás dátum formátum. Kérlek használj 'YYYY-MM-DD' formátumot.")
        return
    
    if befejezo_datum <= kezdo_datum:
        print("A befejező dátumnak későbbinek kell lennie, mint a kezdő dátum.")
        return
    
    for foglalas in foglalasok:
        if (foglalas.szobaszam == szobaszam and
            ((kezdo_datum >= foglalas.kezdo_datum and kezdo_datum < foglalas.befejezo_datum) or
             (befejezo_datum > foglalas.kezdo_datum and befejezo_datum <= foglalas.befejezo_datum))):
            print("Erre az időszakra már van foglalás!")
            return
    
    szoba = szalloda.szobak.get(szobaszam)
    if szoba:
        fizetendo = foglalas_osszeg(szoba, kezdo_datum, befejezo_datum)
        foglalasok.append(Foglalas(szobaszam, kezdo_datum, befejezo_datum))
        print(f"A foglalás sikeres. Fizetendő összeg: {fizetendo} Ft.")
    else:
        print("Nem létezik ilyen szoba.")

def lemondas():
    if foglalasok:
        szobaszam = int(input("Kérlek add meg a lemondani kívánt szobaszámot: "))
        kezdo_datum = input("Kérlek add meg a foglalás kezdő dátumát (YYYY-MM-DD formátumban): ")
        befejezo_datum = input("Kérlek add meg a foglalás befejező dátumát (YYYY-MM-DD formátumban): ")
        
        try:
            kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
            befejezo_datum = datetime.strptime(befejezo_datum, "%Y-%m-%d")
        except ValueError:
            print("Hibás dátum formátum. Kérlek használj 'YYYY-MM-DD' formátumot.")
            return
        
        for foglalas in foglalasok:
            if (foglalas.szobaszam == szobaszam and
                foglalas.kezdo_datum == kezdo_datum and
                foglalas.befejezo_datum == befejezo_datum):
                foglalasok.remove(foglalas)
                print("A foglalás sikeresen törölve.")
                return
        
        print("Nincs ilyen foglalás.")
    else:
        print("Nincs foglalás rögzítve.")

while True:
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")
    valasztas = input("Válassz egy műveletet: ")
    
    if valasztas == "1":
        foglalas()
    elif valasztas == "2":
        lemondas()
    elif valasztas == "3":
        kiiras_foglalasok()
    elif valasztas == "4":
        print("Kilépés...")
        break
    else:
        print("Hibás választás. Kérlek, válassz az elérhető műveletek közül.")