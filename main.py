import csv

ressourcen = {
    "Water": 2000,
    "Oat milk": 1000,
    "Coffee": 500
}

ingredienten = {
    "Water": {"Water": 200},
    "Oat milk": {"Oat milk": 100},
    "Coffee": {"Coffee": 50},
    "Latte": {"Water": 100, "Oat milk": 250, "Coffee": 25},
    "Espresso": {"Water": 50, "Coffee": 20},
    "Cappucino": {"Water": 250, "Oat milk": 100, "Coffee": 25}
}

muenzfach = {  # Anzahl der Münzen im Fach
    "0.1": 10,
    "0.2": 10,
    "0.5": 10,
    "1.0": 10,
    "2.0": 10
} 

muenzen = [0.1, 0.2, 0.5, 1.0, 2.0]  # Akzeptierte Münzen in Euro

strom = True
erfolg = True

umsatz = 0.0
produkte = {}

with open("prices.csv", "r", newline="", encoding="utf-8") as datei:
    reader = csv.reader(datei)
    next(reader)  # Überspringe die Kopfzeile
    for row in reader:
        produkt, preis = row
        produkte[produkt.strip()] = float(preis) # Entferne führende und nachfolgende Leerzeichen und konvertiere den Preis in einen float

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
        # Erstelle eine CSV-Datei mit den aktuellen Ressourcen, Münzen und Umsatz
        with open("report.csv", "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerow(["Zutat", "Menge"])
            for zutat, menge in ressourcen.items():
                writer.writerow([zutat, menge])

            writer.writerow(["Münze", "Anzahl"])
            for muenze, anzahl in muenzfach.items():
                writer.writerow([muenze, anzahl])

            writer.writerow(["Umsatz", umsatz])
    elif auswahl.lower() == "replenish":
        # CSV-Datei mit den aktuellen Ressourcen, Münzen und Umsatz erstellen
        with open("replenish.csv", "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerow(["Zutat", "Menge"])
            for zutat, menge in ressourcen.items():
                writer.writerow([zutat, menge])

            writer.writerow(["Münze", "Anzahl"])
            for muenze, anzahl in muenzfach.items():
                writer.writerow([muenze, anzahl])

            writer.writerow(["Umsatz", umsatz])

        # Ressourcen und Münzen auffüllen
        ressourcen = {zutat: 2000 if zutat == "Water" else 1000 if zutat == "Oat milk" else 500 for zutat in ressourcen}
        muenzfach = {muenze: 10 for muenze in muenzfach}
        print("Die Kaffeemaschine wurde aufgefüllt.")
    elif auswahl.lower() == "off":
        # csv datei weiterschreiben mit aktuellen ressourcen, muenzen und umsatz
        with open("off.csv", "a", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerow([])
            writer.writerow(["Zutat", "Menge"])
            for zutat, menge in ressourcen.items():
                writer.writerow([zutat, menge])

            writer.writerow(["Münze", "Anzahl"])
            for muenze, anzahl in muenzfach.items():
                writer.writerow([muenze, anzahl])
                
            writer.writerow(["Umsatz", umsatz])

        print("Kaffeemaschine wird ausgeschaltet.")
        strom = False
    else:
        print("Ungültige Auswahl. Bitte wählen Sie ein Getränk aus der Liste.")
        erfolg = True
