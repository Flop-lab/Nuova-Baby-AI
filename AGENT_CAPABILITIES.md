# Capacità degli Agenti di Baby AI
# Baby AI Agent Capabilities

**Versione**: 1.0  
**Data**: 13 Novembre 2025  
**Stato**: Phase 1.1 POC

---

## 🤔 Che Cosa Può Fare di Diverso Baby AI?
## What Can Baby AI Do Differently?

Baby AI è un sistema di automazione desktop **local-first** con architettura multi-agente che si distingue dai tradizionali assistenti AI per le seguenti caratteristiche uniche:

---

## 🎯 Caratteristiche Distintive Principali
## Key Distinctive Features

### 1. **Architettura Multi-Agente Specializzata**
Unlike generic AI assistants (ChatGPT, Claude, etc.) that handle all tasks with a single model, Baby AI uses specialized domain agents:

- **AppAgent**: Controllo completo delle applicazioni macOS
- **BrowserAgent**: Automazione browser avanzata
- **Orchestrator**: Coordina intelligentemente gli agenti specializzati

**Vantaggio**: Ogni agente è ottimizzato per il suo dominio specifico, garantendo precisione ed efficienza superiori.

### 2. **Esecuzione Locale e Privacy-First**
```
❌ Altri Assistenti AI:
   User → Cloud API → Response
   (dati inviati a server esterni)

✅ Baby AI:
   User → Local LLM (Qwen3-4B) → Local Execution → Response
   (tutti i dati rimangono sul tuo Mac)
```

**Vantaggio**: 
- Zero invio di dati a server esterni
- Funzionamento offline completo
- Latenza ridotta (no network calls)
- Privacy garantita al 100%

### 3. **Function Calling Nativo e Deterministico**
Baby AI non si limita a generare testo: **esegue azioni reali** sul tuo Mac attraverso tool calling validato.

**Confronto con Altri Assistenti:**

| Caratteristica | ChatGPT/Claude | Baby AI |
|----------------|----------------|---------|
| Esecuzione Azioni | ❌ Solo suggerimenti testuali | ✅ Esecuzione diretta validata |
| Controllo App macOS | ❌ Non disponibile | ✅ 10 funzioni native |
| Browser Automation | ❌ Non disponibile | ✅ 15 funzioni avanzate |
| Validazione Input | ⚠️ Limitata | ✅ Pydantic type-safe |
| Error Handling | ⚠️ Generico | ✅ Specifico per dominio |

### 4. **Integrazione Profonda con macOS**
Utilizza API native Apple (Appscript, PyObjC, NSWorkspace) invece di simulazione tastiera/mouse.

**Vantaggio**: 
- Affidabilità superiore
- Performance migliori
- Accesso a metadata delle app
- Controllo granulare dello stato

---

## 🔧 Capacità degli Agenti
## Agent Capabilities

### AppAgent - Controllo Applicazioni macOS

L'**AppAgent** fornisce 10 funzioni specializzate per il controllo completo delle applicazioni macOS:

#### 1. **Gestione Base Applicazioni**

##### `open_app(appName: str)`
Apre un'applicazione macOS per nome.

**Esempio:**
```python
# User: "apri Spotify"
open_app("Spotify")
→ "Application 'Spotify' activated successfully"
```

**Differenza da altri sistemi**: Usa Appscript nativo invece di simulare click o comandi shell generici.

##### `close_app(appName: str)`
Chiude un'applicazione macOS in modo pulito (quit, non force quit).

**Esempio:**
```python
# User: "chiudi Chrome"
close_app("Chrome")
→ "Application 'Chrome' closed successfully"
```

##### `restart_app(appName: str)`
Riavvia un'applicazione (chiusura + riapertura con delay).

**Esempio:**
```python
# User: "riavvia Safari"
restart_app("Safari")
→ "Application 'Safari' restarted successfully"
```

#### 2. **Gestione Visibilità e Focus**

##### `focus_app(appName: str)`
Porta un'applicazione in primo piano (attiva la finestra).

**Esempio:**
```python
# User: "metti in primo piano TextEdit"
focus_app("TextEdit")
→ "Application 'TextEdit' brought to foreground"
```

##### `hide_app(appName: str)`
Nasconde un'applicazione (rimane in esecuzione ma invisibile).

**Esempio:**
```python
# User: "nascondi Slack"
hide_app("Slack")
→ "Application 'Slack' hidden successfully"
```

##### `unhide_app(appName: str)`
Mostra nuovamente un'applicazione nascosta.

**Esempio:**
```python
# User: "mostra Slack"
unhide_app("Slack")
→ "Application 'Slack' shown successfully"
```

#### 3. **Monitoraggio e Informazioni**

##### `list_running_apps()`
Elenca tutte le applicazioni attualmente in esecuzione.

**Esempio:**
```python
# User: "quali app sono aperte?"
list_running_apps()
→ "Running applications: Chrome, Safari, Slack, Spotify, TextEdit, Visual Studio Code"
```

**Differenza chiave**: Filtra automaticamente i processi di sistema, mostrando solo app visibili all'utente.

##### `is_app_running(appName: str)`
Verifica se un'applicazione specifica è in esecuzione.

**Esempio:**
```python
# User: "Spotify è aperto?"
is_app_running("Spotify")
→ "Yes, 'Spotify' is currently running"
```

##### `get_app_info(appName: str)`
Ottiene informazioni dettagliate su un'applicazione (Bundle ID, stato, visibilità).

**Esempio:**
```python
# User: "dammi info su Chrome"
get_app_info("Chrome")
→ """
Application: Google Chrome
Bundle ID: com.google.Chrome
Status: Active (foreground)
Visibility: Visible
"""
```

**Capacità unica**: Accede a metadata interni macOS (Bundle ID, activation policy, hidden state).

#### 4. **Operazioni Avanzate**

##### `launch_app_with_file(appName: str, filePath: str)`
Apre un'applicazione con un file specifico.

**Esempio:**
```python
# User: "apri document.txt con TextEdit"
launch_app_with_file("TextEdit", "/Users/username/document.txt")
→ "Opened '/Users/username/document.txt' with 'TextEdit'"
```

**Vantaggio**: Integrazione diretta con il file system per workflow complessi.

---

### BrowserAgent - Automazione Browser

Il **BrowserAgent** fornisce 15 funzioni per controllo avanzato dei browser (Safari, Chrome, Firefox):

#### 1. **Navigazione Base**

##### `browser_open_url(url: str, browser: str = "Safari")`
Apre un URL nel browser specificato.

**Esempio:**
```python
# User: "apri google.com in Safari"
browser_open_url("https://google.com", "Safari")
→ "Opened https://google.com in Safari"
```

##### `browser_new_tab(url: str, browser: str = "Safari")`
Apre un nuovo tab con l'URL specificato.

**Esempio:**
```python
# User: "apri github.com in un nuovo tab"
browser_new_tab("https://github.com", "Safari")
→ "Opened new tab with https://github.com in Safari"
```

**Differenza da altri sistemi**: Usa AppleScript nativo per Safari invece di estensioni browser o Selenium.

##### `browser_close_tab(browser: str = "Safari")`
Chiude il tab corrente.

**Esempio:**
```python
# User: "chiudi questo tab"
browser_close_tab("Safari")
→ "Closed tab in Safari"
```

#### 2. **Navigazione Storico**

##### `browser_go_back(browser: str = "Safari")`
Torna alla pagina precedente (history.back).

##### `browser_go_forward(browser: str = "Safari")`
Vai alla pagina successiva (history.forward).

##### `browser_reload(browser: str = "Safari")`
Ricarica la pagina corrente.

**Esempio:**
```python
# User: "torna indietro e poi ricarica"
browser_go_back("Safari")
browser_reload("Safari")
```

#### 3. **Scrolling Avanzato**

##### `browser_scroll_down(browser: str = "Safari", amount: int = 300)`
Scrolla verso il basso di N pixel.

##### `browser_scroll_up(browser: str = "Safari", amount: int = 300)`
Scrolla verso l'alto di N pixel.

##### `browser_scroll_to_top(browser: str = "Safari")`
Scrolla all'inizio della pagina (window.scrollTo(0, 0)).

##### `browser_scroll_to_bottom(browser: str = "Safari")`
Scrolla alla fine della pagina (scrollHeight).

**Esempio:**
```python
# User: "scrolla fino in fondo alla pagina"
browser_scroll_to_bottom("Safari")
→ "Scrolled to bottom in Safari"
```

**Capacità unica**: Scrolling deterministico via JavaScript injection (più affidabile di simulazione scroll wheel).

#### 4. **Interazione con Contenuti**

##### `browser_find_text(text: str, browser: str = "Safari")`
Cerca testo nella pagina corrente (window.find).

**Esempio:**
```python
# User: "cerca 'privacy policy' nella pagina"
browser_find_text("privacy policy", "Safari")
→ "Searched for 'privacy policy' in Safari"
```

##### `browser_click_link(text: str, browser: str = "Safari")`
Clicca un link identificato dal testo visibile.

**Esempio:**
```python
# User: "clicca sul link 'Learn More'"
browser_click_link("Learn More", "Safari")
→ "Clicked link containing 'Learn More' in Safari"
```

**Vantaggio**: Click deterministico via DOM query invece di coordinate x/y (più robusto a cambiamenti layout).

#### 5. **Informazioni Pagina**

##### `browser_get_current_url(browser: str = "Safari")`
Ottiene l'URL della pagina corrente.

**Esempio:**
```python
# User: "qual è l'URL corrente?"
browser_get_current_url("Safari")
→ "Current URL: https://github.com/Flop-lab/Nuova-Baby-AI"
```

##### `browser_get_page_title(browser: str = "Safari")`
Ottiene il titolo della pagina corrente.

**Esempio:**
```python
# User: "qual è il titolo della pagina?"
browser_get_page_title("Safari")
→ "Page title: Nuova Baby AI - GitHub"
```

#### 6. **Gestione Tab**

##### `browser_switch_tab(index: int, browser: str = "Safari")`
Cambia al tab specificato (1-based index).

**Esempio:**
```python
# User: "vai al primo tab"
browser_switch_tab(1, "Safari")
→ "Switched to tab 1 in Safari"
```

---

## 🔄 Sistema di Orchestrazione Multi-Agente
## Multi-Agent Orchestration System

### Flusso Intelligente di Esecuzione

Baby AI usa un **orchestrator** basato su Pydantic AI che coordina automaticamente gli agenti:

```
User: "apri Spotify e vai su spotify.com"
    ↓
Orchestrator (Qwen3-4B-Thinking)
    ↓
[Thinking] "Devo: 1) aprire app Spotify, 2) aprire URL in browser"
    ↓
AppAgent.open_app("Spotify")
    ↓
BrowserAgent.browser_open_url("https://spotify.com")
    ↓
Response: "Ho aperto Spotify e navigato su spotify.com"
```

**Caratteristiche Uniche dell'Orchestrator:**

1. **Reasoning Esteso (think=True)**
   - Qwen3-4B-Thinking genera ragionamento esplicito prima di agire
   - Log trasparente del processo decisionale
   - Migliore debugging e comprensibilità

2. **Retry Logic Intelligente**
   - Validazione Pydantic rigorosa di tutti i tool calls
   - Retry automatico su errori di validazione (max 3 tentativi)
   - Error handling specifico per dominio

3. **Agentic Loop**
   - Supporto per sequenze multi-step
   - L'LLM decide autonomamente quando fermarsi
   - Max 10 iterazioni per prevenire loop infiniti

4. **Tool Call Validation**
   - Type-safe function calling con Pydantic
   - Validazione argomenti in real-time
   - Error messages user-friendly

---

## 📊 Confronto con Altri Sistemi
## Comparison with Other Systems

### Baby AI vs ChatGPT/Claude

| Caratteristica | ChatGPT/Claude | Baby AI |
|----------------|----------------|---------|
| **Privacy** | Dati inviati a cloud | ✅ 100% locale |
| **Offline** | Richiede connessione | ✅ Funziona offline |
| **macOS Control** | ❌ Non disponibile | ✅ 10 funzioni native |
| **Browser Automation** | ❌ Non disponibile | ✅ 15 funzioni avanzate |
| **Latenza** | 500-2000ms (network) | ⚡ 100-500ms (locale) |
| **Costo** | $20/mese (Plus) | ✅ Gratis (locale) |
| **Validazione** | Testuale | ✅ Type-safe (Pydantic) |
| **Multi-step** | Limitato | ✅ Agentic loop illimitato |

### Baby AI vs Apple Shortcuts

| Caratteristica | Apple Shortcuts | Baby AI |
|----------------|----------------|---------|
| **Natural Language** | ❌ GUI drag-and-drop | ✅ Conversazionale |
| **Complessità** | Limitata | ✅ Ragionamento LLM |
| **Error Handling** | Manuale | ✅ Automatico con retry |
| **Estensibilità** | Limitata a actions built-in | ✅ Plugin system (futuro) |
| **Debugging** | Difficile | ✅ Log strutturati + thinking |

### Baby AI vs Selenium/Playwright

| Caratteristica | Selenium/Playwright | Baby AI |
|----------------|---------------------|---------|
| **Setup** | Complesso (drivers, config) | ✅ Zero-config |
| **Programming** | Richiede codice | ✅ Natural language |
| **Robustezza** | Fragile (selettori CSS) | ✅ Semantic (testo visibile) |
| **AI-Driven** | ❌ Script statici | ✅ Decisioni dinamiche LLM |
| **macOS Integration** | ⚠️ Limitata | ✅ Nativa (Appscript) |

---

## 🚀 Casi d'Uso Unici
## Unique Use Cases

### 1. **Workflow Automation Conversazionale**

```
User: "ogni volta che apro Slack, apri anche Spotify e vai su spotify.com/playlist/focus"

Baby AI:
1. Rileva apertura Slack (future: event triggers)
2. AppAgent.open_app("Spotify")
3. BrowserAgent.browser_open_url("https://spotify.com/playlist/focus")
```

**Vantaggio**: Nessun coding richiesto, tutto in linguaggio naturale.

### 2. **Debug e Monitoring Applicazioni**

```
User: "quali app stanno usando più risorse e chiudi quelle non essenziali?"

Baby AI:
1. AppAgent.list_running_apps() → [app1, app2, ...]
2. AppAgent.get_app_info(app) per ogni app
3. Analisi con LLM
4. AppAgent.close_app(apps_non_essenziali)
```

**Capacità unica**: Combinazione di system monitoring + AI reasoning + azione automatica.

### 3. **Browser Research Automation**

```
User: "cerca 'Pydantic AI tutorial' su Google e apri i primi 3 risultati in tab separati"

Baby AI:
1. BrowserAgent.browser_open_url("https://google.com/search?q=Pydantic+AI+tutorial")
2. BrowserAgent.browser_click_link("primo risultato")
3. BrowserAgent.browser_new_tab("secondo risultato URL")
4. BrowserAgent.browser_new_tab("terzo risultato URL")
```

**Vantaggio**: Automazione semantica invece di scripting position-based.

### 4. **Multi-App Orchestration**

```
User: "prepara il mio setup di lavoro: apri VS Code, Slack, Spotify e vai su github.com"

Baby AI:
1. AppAgent.open_app("Visual Studio Code")
2. AppAgent.open_app("Slack")
3. AppAgent.open_app("Spotify")
4. BrowserAgent.browser_open_url("https://github.com")
```

**Differenza da script**: Gestione errori intelligente + feedback naturale.

---

## 🔮 Roadmap Future (Phase 2+)
## Future Roadmap

### Capacità in Sviluppo

1. **File Agent**
   - Operazioni file system avanzate
   - Ricerca intelligente contenuti
   - Backup automatici

2. **System Agent**
   - Controllo impostazioni macOS
   - Gestione rete e bluetooth
   - Monitoring risorse

3. **Voice Agent**
   - Comandi vocali integrati
   - Text-to-speech responses
   - Sintesi vocale Apple Speech API

4. **Plugin System**
   - Estensioni dinamiche caricate runtime
   - LLM-assisted plugin discovery
   - Marketplace plugin community

5. **Teaching System**
   - Apprendimento da esempi utente
   - RAG database per conoscenza dominio-specifica
   - Miglioramento continuo performance

---

## 💡 Principi Architetturali
## Architectural Principles

### 1. Local-First
Tutti i dati e l'esecuzione rimangono sul tuo Mac. Zero dipendenze da servizi cloud.

### 2. Privacy-First
Nessun telemetry, nessun data collection, nessun tracking. I tuoi comandi e dati sono solo tuoi.

### 3. Deterministic & Validated
Ogni tool call è validato con Pydantic per garantire type-safety e prevenire errori runtime.

### 4. Native Integration
Utilizzo di API native macOS (Appscript, PyObjC) invece di simulazione UI o hack.

### 5. Extensible by Design
Architettura modulare pronta per plugin e estensioni future senza refactoring major.

---

## 📚 Risorse Aggiuntive
## Additional Resources

- **[README.md](./README.md)** - Setup e quick start guide
- **[SDD_NUOVA_BABY_AI_v3.1.md](./SDD_NUOVA_BABY_AI_v3.1.md)** - Documento design completo
- **[ARP_NUOVA_BABY_AI_v2.1.md](./ARP_NUOVA_BABY_AI_v2.1.md)** - Architettura di riferimento
- **[PHASE_1.1_DESIGN_DOCUMENT.md](./PHASE_1.1_DESIGN_DOCUMENT.md)** - Design Phase 1.1 con diagrammi

---

## 🤝 Conclusione
## Conclusion

**Baby AI non è un altro chatbot** - è un sistema di automazione locale con:

✅ **Capacità di Esecuzione Reale**: Non solo suggerimenti, ma azioni concrete sul tuo Mac  
✅ **Privacy Assoluta**: Tutto locale, zero cloud, nessun data sharing  
✅ **Architettura Multi-Agente**: Specializzazione per massima efficienza  
✅ **Type-Safe & Validated**: Pydantic garantisce affidabilità production-grade  
✅ **Natural Language Interface**: Zero coding, tutto conversazionale  
✅ **Extensible**: Plugin system e teaching system in roadmap  

**La differenza chiave**: Baby AI è progettato per **fare cose** invece di solo **parlare di cose**.

---

**Documento creato il:** 13 Novembre 2025  
**Versione:** 1.0  
**Compatibilità:** Baby AI Phase 1.1 POC
