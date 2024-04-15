from datetime import datetime
from abc import ABC, abstractmethod


class Szoba(ABC):
    def __init__(self, ar: int, szobaszam: int):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def get_description(self):
        pass
    
    def get_szobaszam(self):
        return self.szobaszam


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=9900):  # Egyágyas szoba alapára: 9900 Ft
        super().__init__(ar, szobaszam)
        self.ar = ar

    def get_description(self):
        return f"Egyágyas szoba #{self.szobaszam}, Ár: {self.ar}"


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=14900):  # Kétágyas szoba alapára: 14900 Ft
        super().__init__(ar, szobaszam)
        self.ar = ar

    def get_description(self):
        return f"Kétágyas szoba #{self.szobaszam}, Ár: {self.ar}"


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def get_szobak(self):
        return self.szobak

    def get_nev(self):
        return self.nev

    def foglalas(self, szobaszam, datum, auto=False):
        # Ellenőrizzük, hogy a dátum jövőbeli-e
        today = datetime.now().date()
        if datum <= today:
            print("A foglalás dátuma csak a jövőben lehet!")
            return None
        # ellenőrizzük hogy a szoba szabad-e
        for foglalas in self.foglalasok:
            if foglalas.get_szoba().szobaszam == szobaszam and foglalas.get_datum() == datum:
                print("Ez a szoba már foglalt!")
                return None

        # ellenőrizzük hogy van-e ilyen szobaszám
        for szoba in self.szobak:
            if szoba.get_szobaszam() == szobaszam:
                if auto != True:
                    confirm = input(
                        f"Folglalni kívánt szoba: {szobaszam} Dátum: {datum} Ár:{szoba.ar}. Biztosan folytatja? (y/n)")
                    if confirm.lower() == 'n':
                        print("Foglalás megszakítva!")
                        return None
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)

                return foglalas

        return None  # Ha nincs ilyen szoba

    def lemondas(self, szobaszam, datum):
        # ellenőrizzük hogy a szoba foglalt-e
        for id, foglalas in enumerate(self.foglalasok):
            if foglalas.get_szoba().szobaszam == szobaszam and foglalas.get_datum() == datum:
                confirm = input(
                    f"Töröli kívánt foglalás: {szobaszam} Dátum: {datum} Ár:{foglalas.get_szoba().ar}. Biztosan folytatja? (y/n)")
                if confirm.lower() == 'n':
                    print("Foglalás megszakítva!")
                    return None
                del self.foglalasok[id]
                return True

        print("Ez a szoba nincs lefoglalva!")
        return False

    def get_ar(self, szobaszam):
        for szoba in self.szobak:
            if szoba.get_szobaszam() == szobaszam:
                return szoba.get_ar()

        return None  # Ha nincs ilyen szoba

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
            return

        print("Foglalások:")
        for i, foglalas in enumerate(self.foglalasok, start=1):
            print(f"{i}. Foglalás:")
            print("Szoba:", foglalas.get_szoba().get_description())
            print("Dátum:", foglalas.get_datum_as_string())


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum
        self.foglalasok = []

    def get_szoba(self):
        return self.szoba

    def get_datum_as_string(self):
        return self.datum.strftime("%Y-%m-%d")  # Konvertáljuk a dátumot stringgé

    def get_datum(self):
        return self.datum


def print_menu():
    print("\nVálassz egy műveletet:")
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")


if __name__ == "__main__":
    szalloda = Szalloda("Beadandó Hotel and Spa")

    egyagyas_szoba = EgyagyasSzoba(szobaszam=101)
    elso_ketagyas_szoba = KetagyasSzoba(szobaszam=201)
    masodik_ketagyas_szoba = KetagyasSzoba(szobaszam=202)

    szalloda.add_szoba(egyagyas_szoba)
    szalloda.add_szoba(elso_ketagyas_szoba)
    szalloda.add_szoba(masodik_ketagyas_szoba)

    szalloda.foglalas(101, datetime.strptime("2024-06-01", "%Y-%m-%d").date(), auto=True)
    szalloda.foglalas(201, datetime.strptime("2024-06-01", "%Y-%m-%d").date(), auto=True)
    szalloda.foglalas(202, datetime.strptime("2024-06-01", "%Y-%m-%d").date(), auto=True)
    szalloda.foglalas(201, datetime.strptime("2024-06-05", "%Y-%m-%d").date(), auto=True)
    szalloda.foglalas(202, datetime.strptime("2024-06-05", "%Y-%m-%d").date(), auto=True)

    while True:
        print_menu()

        try:
            valasztas = int(input("Választás: "))

            if valasztas == 1:
                print(f"A {szalloda.get_nev()} foglalható szoba típusai:")
                szobak = szalloda.get_szobak()
                for szoba in szobak:
                    print(szoba.get_description())
                szobaszam = int(input("Add meg a foglalni kívánt szoba számát (kettőskereszt nélkül): "))
                datum_str = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                foglalas = szalloda.foglalas(szobaszam, datum)
                if foglalas:
                    print("Sikeres foglalás!")
                else:
                    print("Foglalás sikertelen!")
            elif valasztas == 2:
                szobaszam = int(input("Add meg a lemondani kívánt szoba számát: "))
                datum_str = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                lemondas = szalloda.lemondas(szobaszam, datum)
                if lemondas:
                    print("Sikeres lemondás!")
                else:
                    print("Lemondás sikertelen!")
            elif valasztas == 3:
                szalloda.listaz_foglalasok()
            elif valasztas == 4:
                print("Kilépés...")
                break
            else:
                print("Nincs ilyen művelet.")

        except ValueError as err:
            print(f"Kérem adjon meg egy számot! {err}")
