import csv
import json

# Percorso del file dei dati della Serie A all'interno della cartella dati/
FILE = "dati/serie-a-2025-26.csv"


def carica(nomefile):
    """Legge il file CSV con open() tradizionale e DictReader,

    controlla che i gol siano numeri con isdigit(), converte in interi
    e scarta le righe difettose.
    """
    righe_buone = []
    righe_scartate = 0

    with open(nomefile, "r", encoding="utf-8", newline="") as f:
        lettore = csv.DictReader(f)

        for riga in lettore:
            # Controlliamo che i campi dei gol siano cifre numeriche valide
            if (
                "FTHG" in riga
                and "FTAG" in riga
                and riga["FTHG"].isdigit()
                and riga["FTAG"].isdigit()
            ):
                # Convertiamo i gol da stringa a numero intero
                riga["FTHG"] = int(riga["FTHG"])
                riga["FTAG"] = int(riga["FTAG"])
                righe_buone.append(riga)
            else:
                righe_scartate += 1

    return righe_buone, righe_scartate


def domanda1(dati):
    """Calcola quante partite sono finite con la vittoria in casa (H),

    in pareggio (D) o con la vittoria in trasferta (A), sia in numero
    che in percentuale.
    """
    if not dati:
        return None

    totale = len(dati)
    casa = 0
    pareggi = 0
    trasferta = 0

    for p in dati:
        esito = p["FTR"]
        if esito == "H":
            casa += 1
        elif esito == "D":
            pareggi += 1
        elif esito == "A":
            trasferta += 1

    # Arrotondamento delle percentuali a 2 decimali come richiesto dai criteri
    perc_casa = round((casa / totale) * 100, 2)
    perc_pareggi = round((pareggi / totale) * 100, 2)
    perc_trasferta = round((trasferta / totale) * 100, 2)

    return {
        "vittorie_casa": f"{casa} ({perc_casa}%)",
        "pareggi": f"{pareggi} ({perc_pareggi}%)",
        "vittorie_trasferta": f"{trasferta} ({perc_trasferta}%)",
    }


def domanda2(dati):
    """Calcola i gol totali, il minimo, il massimo, la media per partita

    e individua la partita con più gol.
    """
    if not dati:
        return None

    # Sommiamo FTHG (gol casa) + FTAG (gol trasferta) per ogni partita
    gol_partite = [p["FTHG"] + p["FTAG"] for p in dati]

    gol_totali = sum(gol_partite)
    gol_min = min(gol_partite)
    gol_max = max(gol_partite)
    gol_medio = round(
        gol_totali / len(dati), 2
    )  # Arrotondamento della media

    # Troviamo la prima partita con il massimo dei gol
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
        esito = p["FTR"]

        # Inizializziamo le squadre nel dizionario se non sono presenti
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

        # Assegnazione dei punti in base all'esito finale (FTR)
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

    # Prepariamo la tabella finale come lista di tuple
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
    """Domanda personalizzata: Chi vince il primo tempo vince anche la partita?

    Verifica quante volte il vantaggio alla fine del primo tempo (HTR)
    viene confermato al fischio finale (FTR).
    """
    if not dati:
        return None

    totale_partite = len(dati)
    partite_confermate = 0

    for p in dati:
        # Se HTR (primo tempo) è diverso da pareggio ed è uguale a FTR (finale)
        if p["HTR"] != "D" and p["HTR"] == p["FTR"]:
            partite_confermate += 1

    percentuale = round((partite_confermate / totale_partite) * 100, 2)

    return {
        "partite_totali": totale_partite,
        "vantaggio_confermato": partite_confermate,
        "percentuale_conferma": f"{percentuale}%",
    }


def scrivi_risultati(nomefile, intestazione, tabella):
    """Converte la tabella in una lista di dizionari e la salva in formato JSON

    leggibile (indent=2, ensure_ascii=False).
    """
    dati_json = []
    for riga in tabella:
        # Abbina ogni intestazione (chiave) al rispettivo valore della riga
        record = dict(zip(intestazione, riga))
        dati_json.append(record)

    with open(nomefile, "w", encoding="utf-8") as f:
        json.dump(dati_json, f, indent=2, ensure_ascii=False)


def main():
    # 1. Caricamento dei dati
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")

    # 2. Stampa Domanda 1 (Esiti)
    res1 = domanda1(dati)
    print("\n--- DOMANDA 1 (ESITI PARTITE) ---")
    print(f"Vittorie in casa: {res1['vittorie_casa']}")
    print(f"Pareggi: {res1['pareggi']}")
    print(f"Vittorie in trasferta: {res1['vittorie_trasferta']}")

    # 3. Stampa Domanda 2 (Gol)
    res2 = domanda2(dati)
    print("\n--- DOMANDA 2 (GOL) ---")
    print(f"Gol Totali del campionato: {res2['totali']}")
    print(f"Media gol per partita: {res2['media']}")
    print(f"Gol minimi in una partita: {res2['minimo']}")
    print(f"Gol massimi in una partita: {res2['massimo']}")
    print(
        "Partita con più gol:"
        f" {res2['partita_piu_gol']['casa']}-{res2['partita_piu_gol']['trasferta']}"
        f" ({res2['partita_piu_gol']['risultato']})"
    )

    # 4. Calcolo Domanda 3 e salvataggio in risultati.json
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
    scrivi_risultati("risultati.json", intestazione, tabella_classifica)
    print("\n--- DOMANDA 3 ---")
    print(
        "Classifica calcolata e salvata con successo nel file 'risultati.json'."
    )

    # 5. Stampa Domanda Nostra
    res_nostra = domanda_nostra(dati)
    print("\n--- DOMANDA NOSTRA (Primo tempo vs Finale) ---")
    print(f"Partite analizzate: {res_nostra['partite_totali']}")
    print(
        "Vantaggio del primo tempo confermato alla fine:"
        f" {res_nostra['vantaggio_confermato']} volte"
        f" ({res_nostra['percentuale_conferma']})"
    )


if __name__ == "__main__":
    main()
