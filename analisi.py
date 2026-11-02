import csv

FILE = "dati/serie-a-2025-26.csv"


def carica(nomefile):
    """Legge il file, converte i numeri, scarta le righe sporche.
    Restituisce la lista delle righe buone e il numero di righe scartate."""
    """Legge il file, converte i numeri, scarta le righe sporche.

    Restituisce la lista delle righe buone e il numero di righe scartate.
    """
    righe_buone = []
    righe_scartate = 0

    try:
        with open(nomefile, "r", encoding="utf-8") as f:
            # Usa csv.reader per gestire automaticamente virgole, virgolette e ritorni a capo
            lettore = csv.reader(f)

            # Se il file ha un'intestazione (header), puoi leggerla o saltarla così:
            # header = next(lettore)

            for riga in lettore:
                # Salta le righe completamente vuote
                if not riga:
                    righe_scartate += 1
                    continue

                riga_convertita = []
                riga_pulita = True

                for valore in riga:
                    valore_pulito = valore.strip()
                    # Tenta la conversione in intero
                    try:
                        riga_convertita.append(int(valore_pulito))
                    except ValueError:
                        # Se fallisce, tenta la conversione in float
                        try:
                            riga_convertita.append(float(valore_pulito))
                        except ValueError:
                            # Se non è un numero, mantiene la stringa originale
                            riga_convertita.append(valore_pulito)

                # Opzionale: inserisci qui un controllo sulla struttura della riga
                # Es. se ti aspetti esattamente 5 colonne: if len(riga_convertita) != 5: riga_pulita = False

                if riga_pulita:
                    righe_buone.append(riga_convertita)
                else:
                    righe_scartate += 1

    except FileNotFoundError:
        print(f"Errore: Il file {nomefile} non esiste.")
        return [], 0

    return righe_buone, righe_scartate


def domanda1(dati):
    """Risponde alla domanda 1 della scheda."""
    return None


def domanda2(dati):
    """Risponde alla domanda 2."""
    return None


def domanda3(dati):
    """Risponde alla domanda 3. Restituisce la tabella
    che finirà in risultati.csv: una lista di righe."""
    return []


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return None


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""
    pass


def main():
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
    print("Domanda 1:", domanda1(dati))
    print("Domanda 2:", domanda2(dati))
    tabella = domanda3(dati)
    scrivi_risultati("risultati.csv", ["colonna1", "colonna2"], tabella)
    print("Domanda nostra:", domanda_nostra(dati))


main()