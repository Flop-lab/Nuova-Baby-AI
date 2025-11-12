# FIX FUTURI

## FIX 1

### Dal tuo punto di vista:

- **15:06:03**: Invii "Open Spotify"
- **15:06:11**: ✅ Spotify SI APRE (dopo 8 secondi)
- **15:06:23**: 🔓 L'interfaccia si sblocca (dopo altri 12 secondi)

**Il ritardo che hai notato** sono quei **12 secondi** tra quando Spotify si apre realmente e quando puoi scrivere di nuovo nella chat.

## Perché Succede

L'orchestratore fa **due chiamate all'AI**:

1. **Prima chiamata** (~6s): Decide quale funzione usare
2. **Esecuzione** (~2s): Apre Spotify sul Mac ← **QUI SPOTIFY È GIA APERTO**
3. **Seconda chiamata** (~12s): Genera il messaggio "Spotify opened successfully!" ← **QUESTO È IL RITARDO**

L'interfaccia resta in "loading" per tutti e 3 gli step, ma Spotify si apre allo step 2. Quindi tu vedi Spotify aprirsi, ma devi aspettare altri 12 secondi per poter scrivere di nuovo.

## Soluzioni Possibili

Possiamo risolvere in diversi modi:

### 1. Risposta immediata (la più semplice)

- Dopo che Spotify si apre, risponde subito con un messaggio generico
- Saltiamo la seconda chiamata all'AI
- **Pro**: Interfaccia si sblocca immediatamente
- **Contro**: Messaggi meno "umani" (solo "Spotify aperto" invece di frasi più elaborate)

### 2. Generazione in background (più complessa)

- L'interfaccia si sblocca subito dopo che Spotify si apre
- L'AI genera la risposta "carina" in background
- **Pro**: Puoi continuare a scrivere subito + messaggi "umani"
- **Contro**: Più complesso da implementare

### 3. AI più veloce per le risposte (compromesso)

- Usiamo un modello minuscolo (tipo `qwen3:0.5b`) solo per generare il messaggio finale
- La seconda chiamata diventerebbe ~3 secondi invece di 12
- **Pro**: Riduce il ritardo mantenendo i messaggi "umani"
- **Contro**: Serve scaricare un altro modello

Quale soluzione preferisci? Io consiglierei la **#1** (risposta immediata) perché è semplice e risolve completamente il problema.

---

## FIX 2

### Warmup modello per avvio veloce

*[Sezione da completare]*

---

## Note di Implementazione

- **Data**: 12 novembre 2025
- **Stato**: Da implementare
- **Priorità**: Alta (Fix 1), Media (Fix 2)
- **Versione target**: v0.1.1

## Task List

- [ ] Implementare soluzione #1 per Fix 1
- [ ] Test delle performance post-fix
- [ ] Completare documentazione Fix 2
- [ ] Implementare warmup del modello