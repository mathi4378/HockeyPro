#Funktion für Eingabeselektion
def select_input():
    print("Wähle Eingabequelle:")
    print("1: Video")
    print("2: Kamera")

    choice = input("1 oder 2?")
    return choice.strip()  #strip entfernt leerzeichen


