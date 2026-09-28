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
power = True

while power:
    einwurf=0;
    print("Willkommen bei der Kaffeemaschine!")

    print("Liste der Getränke:")
    for produkt, preis in produkte.items():
        print(f"- {produkt}: {preis} Euro")

    auswahl = input("Geben Sie den Namen des gewünschten Getränks ein: ")
    if auswahl in produkte:
        preis = produkte[auswahl]
        print(f"Der Preis für {auswahl} beträgt {preis} Euro.")

        while einwurf < preis:
            muenze = float(input("Geben Sie den Wert der Münze ein (z.B. 0.1, 0.2, 0.5, 1.0, 2.0) oder '0' zum Abbrechen: "))
            
            if muenze in muenzen:
                einwurf += muenze
                print(f"Sie haben insgesamt {einwurf} Euro eingeworfen.")
            elif muenze == 0:
                print("Transaktion abgebrochen.")
                break
            else:
                print("Ungültige Münze. Bitte geben Sie eine gültige Münze ein.")

        if einwurf >= preis:
            wechselgeld = einwurf - preis
            print(f"Vielen Dank! Ihr {auswahl} wird zubereitet.")
            if wechselgeld > 0:
                print(f"Hier ist Ihr Wechselgeld: {wechselgeld} Euro.")
        else:
            print("Zahlung abgebrochen.")
    else:
        print("Ungültige Auswahl. Bitte wählen Sie ein Getränk aus der Liste.")
