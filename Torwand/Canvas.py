from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas

save_path = "/Torwand\\Tor_Wand_4.pdf"

# PDF-Abmessungen
width, height = 200 * mm, 120 * mm  # Maße in mm umwandeln

c = canvas.Canvas(save_path, pagesize=(width, height))
c.setFont("Helvetica", 15)  # Schriftgröße für die Beschriftung

# Buchstaben für die horizontale Beschriftung (bis F)
letters = ["A", "B", "C", "D", "E","F"]

# Horizontale Linien mit Buchstabenbeschriftung
for i in range(len(letters)+1):
    y_position = i * 20 * mm  # Startet korrekt bei 20 mm, dann 40 mm, 60 mm etc.
    c.line(0, y_position, width, y_position)

    # Beschriftung mit Buchstaben links neben der Linie
    text = letters[i-1]
    c.drawString(5, y_position - 20, text)  # Leicht über der Linie platzieren

# Vertikale Linien mit Zahlenbeschriftung (bis 10)
for i in range(11):
    x_position = i * 20 * mm  # Startet korrekt bei 20 mm, dann 40 mm, 60 mm etc.
    c.line(x_position, 0, x_position, height)

    # Beschriftung mit Zahlen unterhalb der Linie
    text = f"{i}"
    c.drawString(x_position - 20, 5, text)  # Direkt unter der Linie platzieren

# Speichern und Datei bereitstellen
c.showPage()
c.save()

print(f"PDF erfolgreich gespeichert unter: {save_path}")
