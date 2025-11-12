# Documento di Design del Software (SDD) v3.1

## Progetto: Nuova Baby AI - Agente Ibrido macOS
**Basato e unificato con l'ARP 2.1**

| Versione | Data | Stato |
|----------|------|--------|
| 3.1 | 12 Novembre 2025 | SDD Aggiornato - Implementazione Reale |

---

## 1. Architettura del Sistema (System Architecture)

Il sistema adotta un'architettura a **Microservizi disaccoppiati** e a **Orchestrazione Multi-LLM**, ottimizzata per l'efficienza delle risorse su hardware Apple Silicon.

### 1.1 Stack Tecnologico Fondamentale (IMPLEMENTAZIONE ATTUALE)

| Componente | Tecnologia | Ruolo nel Sistema |
|------------|------------|-------------------|
| **Frontend (UI)** | **Tauri 2.9.x + React 19.2.0 + TypeScript 5.9.3** | Interfaccia utente nativa, leggera in termini di RAM, responsabile della gestione dinamica delle Estensioni UI. Design iniziale minimale, con obiettivo di stile Visual Studio Code. |
| **Backend Core** | **Python 3.14 + FastAPI 0.115.0 + Pydantic AI 1.12.0** | Router principale. Gestisce l'orchestrazione LLM, il caricamento dei Plugin e l'esposizione delle API locali. **NON usa LangChain** - usa Pydantic AI per orchestrazione. |
| **LLM Orchestratore** | **Qwen3-4B-Thinking-2507-Q8_0 (Ollama 0.12.10)** | **Ragionamento avanzato** con capacità thinking, controllo del flusso e interprete principale del Function Calling locale. **NON Mistral** - modello più avanzato. |
| **Validazione Tooling** | **Pydantic 2.12.4** | Assicura la validazione e la tipizzazione rigorosa di tutti gli input e output JSON per l'affidabilità del Function Calling. |
| **LLM Remoto** | **Google Gemini Pro (SDK) - FUTURO** | Risoluzione delegata per ragionamento complesso. Template per l'integrazione di LLM esterni (via Estensione/Plugin). **NON implementato in Phase 1.1** |
| **Automazione OS** | **Appscript 1.4.0 / PyObjC / Subprocess / Apple Speech API** | Agenti Esecutori per controllo Mac, file system, shell e Comandi Vocali. |

### 1.2 Architettura Modulare (Espandibilità Bimodale) - ROADMAP FUTURA

> **NOTA:** L'iniezione e l'attivazione di Plugin e Estensioni sono controllate esclusivamente dall'Utente.
> **STATO ATTUALE:** Phase 1.1 POC - Architettura monolitica con singolo App Agent
> **EVOLUZIONE:** Plugin/Estensioni implementati in fasi successive

| Modulo | Tipo | Funzionalità | Metodo di Iniezione (Controllo Utente) |
|--------|------|--------------|----------------------------------------|
| **Plugin Funzionale** | **Logica di Backend (Python)** | Aggiunge nuovi Tools/Function Calling e sorgenti di conoscenza (RAG DB). | Caricamento dinamico tramite `importlib` all'avvio del Backend. L'LLM può assistere nella scrittura, ma non esegue l'iniezione automatica. |
| **Estensione UI** | **Frontend/Backend (Ibrido)** | Aggiunge elementi UI dedicati (es. chat LLM Esterna). | Il Frontend interroga un Manifesto JSON esposto dal Backend per il rendering dinamico dei componenti React. |

### 1.3 Interfacce API (Frontend ↔ Backend Core)

Il Backend Core esporrà un'API REST locale per la comunicazione con il Frontend (Tauri).

#### API IMPLEMENTATE (Phase 1.1):

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/chat` | **POST** | **IMPLEMENTATO** - Invia prompt Utente a Qwen3-4B-Thinking (attiva l'orchestrazione e il Function Calling). |

#### API ROADMAP (Fasi Future):

| Endpoint Proposto | Metodo | Descrizione |
|-------------------|--------|-------------|
| `/api/llm_external/{id}` | POST | **FUTURO** - Invia prompt Utente direttamente all'LLM Esterna (Modalità Esterna Esclusiva), bypassando l'Orchestratore. |
| `/api/extensions/manifest` | GET | **FUTURO** - Il Frontend interroga questo endpoint per ottenere il Manifesto JSON delle Estensioni attive. |
| `/api/teaching/{action}` | POST | **FUTURO** - Gestisce le operazioni CRUD (Create, Read, Update, Delete) sulle lezioni e l'archiviazione. |
| `/api/safety/approve` | POST | **FUTURO** - Riceve la conferma esplicita dell'utente per eseguire un Tool in blocco di sicurezza (Comando Pericoloso/Super Pericoloso). |

---

## 2. Modelli di Dati e Tooling (IMPLEMENTAZIONE ATTUALE)

### 2.1 Archiviazione della Conoscenza - Phase 1.1

**IMPLEMENTATO:**
- **Conversazione Tracking:** Gestione conversation_id per continuità sessioni
- **Step Tracking:** Generazione step_id univoci per ogni interazione
- **Error Handling:** Gestione robusta errori con messaggi user-friendly

**FUTURO:**
- Database RAG per Plugin
- Sistema Teaching/Learning
- Archiviazione estesa conversazioni

### 2.2 Function Calling e Tool Validation

**IMPLEMENTATO (App Agent):**
- `open_app(appName: str)` - Apertura applicazioni macOS
- `close_app(appName: str)` - Chiusura applicazioni macOS  
- Validazione Pydantic rigorosa di input/output
- Gestione errori try/catch completa

**FUTURO (Plugin System):**
- Tool dinamici caricabili
- Validazione schema estesa
- Sistema permessi Tool

---

## 3. Stato Implementazione per Fase

### Phase 1.1 - POC App Agent (COMPLETATO ✅)

**IMPLEMENTATO:**
- ✅ FastAPI Backend con Pydantic AI orchestration
- ✅ Qwen3-4B-Thinking-2507-Q8_0 integration
- ✅ App Agent (open/close apps)
- ✅ JSON validation rigorosa
- ✅ Streaming response support
- ✅ Conversation tracking
- ✅ Error handling robusto
- ✅ Test suite completa (17 tests, 44% coverage)

**ARCHITETTURA:**
- Single endpoint `/api/chat`
- Monolithic agent structure
- Local-first approach

### Phase 9 - Tauri Desktop App (IN CORSO 🚧)

**PIANIFICATO:**
- ✅ Tauri 2.9.x desktop wrapper
- ✅ React 19.2.0 + TypeScript 5.9.3 UI
- ✅ Bundled Python backend (PyInstaller)
- ✅ Bundled Ollama Server 0.12.10
- ✅ Automatic lifecycle management

### Fasi Future - Sistema Modulare (ROADMAP 📋)

**EVOLUZIONE PIANIFICATA:**
- Plugin system con caricamento dinamico
- Estensioni UI con manifesto JSON
- API endpoints complessi
- LLM esterni (Gemini Pro)
- Sistema teaching/learning
- Safety approval system
- RAG database integration

---

## 4. Tecnologie e Versioni Definitive

### Stack di Produzione (Verified)

| Componente | Versione | Status |
|------------|----------|---------|
| **Python** | **3.14.0** | ✅ Installato |
| **FastAPI** | **0.115.0** | ✅ Implementato |
| **Pydantic AI** | **1.12.0** | ✅ Implementato |
| **Pydantic** | **2.12.4** | ✅ Implementato |
| **Ollama Server** | **0.12.10** | ✅ Installato |
| **ollama-python** | **0.6.0** | ✅ Implementato |
| **Appscript** | **1.4.0** | ✅ Implementato |
| **PyInstaller** | **6.16.0** | ✅ Installato |
| **Node.js** | **25.1.0** | ✅ Installato |
| **NPM** | **11.6.2** | ✅ Installato |
| **Tauri CLI** | **2.9.4** | 📋 Da installare (Phase 9) |
| **Tauri API** | **2.9.0** | 📋 Da installare (Phase 9) |
| **React** | **19.2.0** | 📋 Da installare (Phase 9) |
| **TypeScript** | **5.9.3** | 📋 Da installare (Phase 9) |
| **Vite** | **7.2.2** | 📋 Da installare (Phase 9) |
| **Rust** | **1.91.1** | 📋 Da installare (Phase 9) |

### Modelli LLM

| Modello | Versione | Ruolo | Status |
|---------|----------|-------|---------|
| **qwen3:4b-thinking-2507-q8_0** | **4.3GB** | **Orchestratore Principale** | ✅ **ATTIVO** |
| **mistral:7b-instruct** | **4.4GB** | Fallback LLM | ✅ Disponibile |
| **nomic-embed-text:latest** | **274MB** | Embeddings | ✅ Disponibile |
| **Google Gemini Pro** | **Cloud** | LLM Remoto Futuro | 📋 Pianificato |

---

## 5. Differenze con Versioni Precedenti

### SDD v3.0 → v3.1 (Aggiornamenti)

**CORREZIONI PRINCIPALI:**
1. **LLM Principale:** Mistral 7B → **Qwen3-4B-Thinking-2507-Q8_0**
2. **Backend Framework:** FastAPI + LangChain → **FastAPI + Pydantic AI**  
3. **API Status:** Tutti endpoint implementati → **Solo /api/chat implementato** (altri in roadmap)
4. **Architettura:** Modulare completa → **POC monolitico** (modularità in roadmap)
5. **Versioni:** Aggiornate a versioni realmente installate

**ALLINEAMENTO CON REALTÀ:**
- SDD ora riflette **implementazione effettiva** Phase 1.1
- Roadmap chiaramente separata da implementazione corrente
- Versioni verificate e testate

---

## 6. Principi Architetturali Mantenuti

### Local-First Approach ✅
- Ollama locale per privacy e performance
- Dati utente mai inviati a servizi esterni senza consenso
- Funzionamento offline completo

### User Control ✅  
- Controllo esplicito su Plugin/Estensioni
- Conferme per operazioni pericolose
- Trasparenza nelle operazioni LLM

### Apple Silicon Optimization ✅
- Stack ottimizzato per performance M1/M2/M3
- Gestione memoria efficiente
- Sfruttamento accelerazione hardware

### Extensibility by Design ✅
- Architettura pronta per modularità futura
- API design scalabile
- Separazione clean Frontend/Backend

---

**Documento aggiornato il:** 12 Novembre 2025  
**Versione:** 3.1  
**Status:** Riflette implementazione reale Phase 1.1 + Roadmap future  
**Compatibilità:** Baby AI Phase 1.1 POC implementation