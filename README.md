# Progetto 1 — Analisi della Serie A 2025/26

## Gruppo GOLAM_WANG

- **GOLAM**: Sviluppo della funzione di caricamento (`carica`) e della Domanda 1.

- **WANG**:Bozze della Domanda 2, della Domanda 3 e della scrittura del file dei risultati.

## Il dataset
- **Fonte**: (file della Serie A 2025/26)
- **Periodo**: Campionato di Serie A 2025/26 (380 partite)
- **Dimensioni**: 380 righe e 23 colonne principali

## Com'è fatto il file
- **Separatore**: Virgola (`,`)
- **Intestazione**: Presente nella prima riga
- **Colonne principali utilizzate**:
  - `Date`: Data della partita (`gg/mm/aaaa`)
  - `HomeTeam` / `AwayTeam`: Squadra di casa e squadra in trasferta
  - `FTHG` / `FTAG`: Gol a fine partita (Full Time) di casa e trasferta
  - `FTR`: Esito finale (`H` = vittoria casa, `D` = pareggio, `A` = vittoria trasferta)
  - `HTR`: Esito primo tempo (Half Time)
- **Tipi di dato e controlli**: I gol erano memorizzati come testo; durante la fase di caricamento abbiamo verificato con `.isdigit()` la correttezza dei dati e convertito i valori in numeri interi (`int`).

## Dati scartati
All'avvio del programma viene eseguita la funzione `carica()`. Se una riga del file CSV risulta incompleta o presenta campi gol non validi, viene automaticamente scartata e conteggiata. Nel nostro dataset tutte le 380 righe sono risultate valide e 0 righe sono state scartate.

## Risposte alle domande

### 1. Esito delle partite (Vittorie Casa, Pareggi, Trasferta)
- **Vittorie in casa (`H`)**: 172 (45.26%)
- **Pareggi (`D`)**: 98 (25.79%)
- **Vittorie in trasferta (`A`)**: 110 (28.95%)

### 2. Statistiche sui Gol
- **Gol totali del campionato**: 1014 gol
- **Media gol per partita**: 2.67 gol/partita
- **Gol minimi in un incontro**: 0
- **Gol massimi in un incontro**: 8
- **Partita con più gol**: Inter-Juventus (risultato finale 4-4)

### 3. Classifica Finale
La classifica completa calcolata dal programma (assegnando 3 punti per la vittoria e 1 per il pareggio) è stata salvata automaticamente nel file `risultati.csv`.

**Sintesi delle prime posizioni in classifica**:
1. **Inter**: 89 punti (28 vinte, 5 pareggiate, 5 perse | GF: 89, GS: 22, Diff: +67)
2. **Milan**: 82 punti (24 vinte, 10 pareggiate, 4 perse | GF: 76, GS: 35, Diff: +41)
3. **Juventus**: 71 punti (19 vinte, 14 pareggiate, 5 perse | GF: 54, GS: 31, Diff: +23)
4. **Atalanta**: 69 punti (21 vinte, 6 pareggiate, 11 perse | GF: 72, GS: 42, Diff: +30)

## La nostra domanda
**Domanda inventata dal gruppo**: *"Chi vince il primo tempo (HTR) vince anche la partita alla fine (FTR)?"*

- **Partite analizzate**: 380
- **Vantaggio del primo tempo confermato a fine gara**: 184 volte
- **Percentuale di conferma**: 48.42%

**Commento al risultato**:
Analizzando i dati emerge che in meno della metà dei casi (48.42%) la squadra in vantaggio a fine primo tempo riesce a confermare la vittoria nei secondi 45 minuti. Questo dimostra l'elevata incertezza e la frequenza di rimonte o pareggi nella ripresa durante il campionato di Serie A.

## Come si lancia il programma
Eseguire il comando:
   ```bash
   python analisi.py
