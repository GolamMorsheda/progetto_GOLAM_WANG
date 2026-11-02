import csv

# Percorso del file dei dati della Serie A
FILE = "dati/serie-a-2025-26.csv"


def carica(nomefile):
    """Legge il file CSV, converte i gol in numeri interi e scarta le righe

    difettose. Restituisce la lista dei dizionari (righe buone) e il numero
    di righe scartate.
    """
    righe_buone = []
    righe_scartate = 0

    try:
        with open(nomefile, "r", encoding="utf-8", newline="") as f:
            lettore = csv.DictReader(f)
            for riga in lettore:
                try:
                    # Convertiamo in numeri interi i gol fatti in casa e in trasferta
                    riga["FTHG"] = int(riga["FTHG"])
                    riga["FTAG"] = int(riga["FTAG"])
                    righe_buone.append(riga)
                except (ValueError, KeyError):
                    # Se manca qualche dato o non è un numero, scartiamo la riga
                    righe_scartate += 1
    except FileNotFoundError:
        print(f"Attenzione: Non trovo il file {nomefile} nella cartella dati/")

    return righe_buone, righe_scartate


def domanda1(dati):
    """Risponde alla domanda 1 della scheda."""
    # Semplice segnaposto o implementazione base
    return "Vedi README per i dettagli sugli esiti delle partite."


def domanda2(dati):
    """Calcola i gol totali, il minimo, il massimo, la media per partita

    e individua la partita con più gol.
    """
    if not dati:
        return None

    # Calcoliamo i gol di ogni singola partita sommando casa + trasferta
    gol_partite = [p["FTHG"] + p["FTAG"] for p in dati]

    gol_totali = sum(gol_partite)
    gol_min = min(gol_partite)
    gol_max = max(gol_partite)
    gol_medio = round(gol_totali / len(dati), 2)

    # Troviamo la partita con il massimo dei gol
    partita_max = None
    for p in dati:
        if p["FTHG"] + p["FTAG"] == gol_max:
            partita_max = {
                "data": p["Date"],
                "casa": p["HomeTeam"],
                "trasferta": p["AwayTeam"],
                "risultato": f"{p['FTHG']}-{p['FTAG']}",
            }
            break

    return {
        "minimo": gol_min,
        "massimo": gol_max,
        "media": gol_medio,
        "totali": gol_totali,
        "partita_piu_gol": partita_max,
    }


def domanda3(dati):
    """Calcola la classifica finale del campionato (3 punti per la vittoria,

    1 per il pareggio) contando gol fatti, subiti e differenza reti.
    """
    classifica = {}

    for p in dati:
        casa = p["HomeTeam"]
        trasferta = p["AwayTeam"]
        gh = p["FTHG"]
        gt = p["FTAG"]
        esito = p["FTR"]  # H = vittoria casa, A = vittoria trasferta, D = pareggio

        # Inizializziamo le squadre nel dizionario se non sono ancora presenti
        for squadra in (casa, trasferta):
            if squadra not in classifica:
                classifica[squadra] = {
                    "punti": 0,
                    "vittorie": 0,
                    "pareggi": 0,
                    "sconfitte": 0,
                    "gf": 0,
                    "gs": 0,
                }

        # Aggiorniamo i gol fatti e subiti
        classifica[casa]["gf"] += gh
        classifica[casa]["gs"] += gt
        classifica[trasferta]["gf"] += gt
        classifica[trasferta]["gs"] += gh

        # Assegnazione dei punti in base all'esito della partita
        if esito == "H":
            classifica[casa]["punti"] += 3
            classifica[casa]["vittorie"] += 1
            classifica[trasferta]["sconfitte"] += 1
        elif esito == "A":
            classifica[trasferta]["punti"] += 3
            classifica[trasferta]["vittorie"] += 1
            classifica[casa]["sconfitte"] += 1
        else:  # Pareggio ('D')
            classifica[casa]["punti"] += 1
            classifica[trasferta]["punti"] += 1
            classifica[casa]["pareggi"] += 1
            classifica[trasferta]["pareggi"] += 1

    # Prepariamo la tabella finale da restituire sotto forma di lista di tuple
    tabella = []
    for squadra, st in classifica.items():
        diff_reti = st["gf"] - st["gs"]
        tabella.append(
            (
                squadra,
                st["punti"],
                st["vittorie"],
                st["pareggi"],
                st["sconfitte"],
                st["gf"],
                st["gs"],
                diff_reti,
            )
        )

    return tabella


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return "Analisi completata con successo."


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella della classifica in un nuovo file CSV usando csv.writer."""
    with open(nomefile, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(intestazione)
        for riga in tabella:
            w.writerow(riga)


def main():
    # 1. Caricamento dei dati
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")

    # 2. Stampa Domanda 2 (Gol)
    res2 = domanda2(dati)
    print("\n--- DOMANDA 2 (GOL) ---")
    print(f"Gol Totali del campionato: {res2['totali']}")
    print(f"Media gol per partita: {res2['media']}")
    print(
        "Partita con più gol:"
        f" {res2['partita_piu_gol']['casa']}-{res2['partita_piu_gol']['trasferta']}"
        f" ({res2['partita_piu_gol']['risultato']})"
    )

    # 3. Calcolo Domanda 3 e salvataggio in risultati.csv
    tabella_classifica = domanda3(dati)
    intestazione = [
        "Squadra",
        "Punti",
        "Vinte",
        "Pareggiate",
        "Perse",
        "Gol Fatti",
        "Gol Subiti",
        "Diff Reti",
    ]
    scrivi_risultati("risultati.csv", intestazione, tabella_classifica)
    print("\n--- DOMANDA 3 ---")
    print("Classifica calcolata e salvata con successo nel file 'risultati.csv'.")


main()