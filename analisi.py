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


    righe_buone = []
    righe_scartate = 0

    with open(nomefile, "r", encoding="utf-8") as f:
        lettore = csv.reader(f)

        for riga in lettore:
            # Scarta le righe vuote o con elementi mancanti
            if not riga or len(riga) == 0:
                righe_scartate += 1
                continue

            riga_convertita = []

            for valore in riga:
                valore_pulito = valore.strip()

                # Controlla se la stringa è composta solo da numeri
                if valore_pulito.isdigit():
                    riga_convertita.append(int(valore_pulito))
                else:
                    riga_convertita.append(valore_pulito)

            righe_buone.append(riga_convertita)

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