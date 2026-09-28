import csv
import os

produkte = {"Water": 2.0, "Oat milk": 2.5, "Coffee": 3.0, "Latte": 5.0, "Espresso": 3.0, "Cappucino": 4.5}
ressourcen = {"Water": 2000, "Oat milk": 1000, "Coffee": 500}
ingredienten = {
    "Water": {"Water": 200},
    "Oat milk": {"Oat milk": 100},
    "Coffee": {"Coffee": 50},
    "Latte": {"Water": 100, "Oat milk": 250, "Coffee": 25},
    "Espresso": {"Water": 50, "Coffee": 20},
    "Cappucino": {"Water": 250, "Oat milk": 100, "Coffee": 25}
}
muenzfach = {"0.1": 10, "0.2": 10, "0.5": 10, "1.0": 10, "2.0": 10}  # Anzahl der Münzen im Fach
muenzen = [0.1, 0.2, 0.5, 1.0, 2.0]  # Akzeptierte Münzen in Euro
strom = True
umsatz = 0.0
erfolg = True

while strom:
    einwurf=0;
    gezahlteMuenzen = []
    ausgezahltesWechselgeld = []

    print("Willkommen bei der Kaffeemaschine!")

    print("Liste der Getränke:")
    for produkt, preis in produkte.items():
        print(f"- {produkt}: {preis} Euro")

    auswahl = input("Geben Sie den Namen des gewünschten Getränks ein: ")
    if auswahl in produkte:
        print(f"Sie haben {auswahl} gewählt.")
        print("Überprüfe die Ressourcen...")

        for zutat, menge in ingredienten[auswahl].items():
            if ressourcen[zutat] < menge:
                print(f"Entschuldigung, es gibt nicht genug {zutat}.")
                erfolg = False
                break

        if erfolg:
            preis = produkte[auswahl]
            print(f"Der Preis für {auswahl} beträgt {preis} Euro.")

            while einwurf < preis:
                muenze = float(input("Geben Sie den Wert der Münze ein (z.B. 0.1, 0.2, 0.5, 1.0, 2.0) oder '0' zum Abbrechen: "))

                if muenze in muenzen:
                    einwurf += muenze
                    gezahlteMuenzen.append(muenze)
                    print(f"Sie haben insgesamt {einwurf} Euro eingeworfen.")
                elif muenze == 0:
                    print("Zahlung abgebrochen.")
                    erfolg = False
                    break
                else:
                    print("Ungültige Münze. Bitte geben Sie eine gültige Münze ein.")

            if einwurf >= preis:
                wechselgeld = einwurf - preis
                umsatz += preis

                for muenze in gezahlteMuenzen:
                    muenzfach[str(muenze)] += 1

                if wechselgeld > 0:
                    for muenze in sorted(muenzen, reverse=True):
                        while wechselgeld >= muenze and muenzfach[str(muenze)] > 0:
                            wechselgeld -= muenze
                            ausgezahltesWechselgeld.append(muenze)

                    if wechselgeld == sum(ausgezahltesWechselgeld):
                        for muenze in ausgezahltesWechselgeld:
                            muenzfach[str(muenze)] -= 1
                        print(f"Hier ist Ihr Wechselgeld: {wechselgeld} Euro.")
                    else:
                        print("Entschuldigung, es gibt nicht genug Wechselgeld. Bitte wenden Sie sich an den Betreiber.")
                        erfolg = False

        if erfolg:
            for zutat, menge in ingredienten[auswahl].items():
                ressourcen[zutat] -= menge

            print(f"Hier ist Ihr {auswahl}. Guten Appetit!")
    elif auswahl.lower() == "report":
        with open("report.csv", "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerows([["Zutat", "Menge"]] + [[zutat, menge] for zutat, menge in ressourcen.items()])
            writer.writerows([[muenze, muenzfach[muenze]] for muenze in muenzfach])
            writer.writerow(["Umsatz", umsatz])

        print("Ressourcenbericht:")
        for zutat, menge in ressourcen.items():
            print(f"- {zutat}: {menge}")
        print(f"Umsatz: {umsatz} Euro")
    elif auswahl.lower() == "off":
        print("Kaffeemaschine wird ausgeschaltet.")
        strom = False
    else:
        print("Ungültige Auswahl. Bitte wählen Sie ein Getränk aus der Liste.")
        erfolg = True
