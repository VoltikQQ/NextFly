\# NextFly Project Launcher



NextFly è uno strumento batch progettato per automatizzare la compilazione e l’avvio di progetti locali. Consente di gestire più progetti, cambiare versioni di JDK, avviare server e compilare con Maven da un’unica interfaccia.



---



\## 📁 Struttura del Repository



text

NextFly/

├── scripts/

│   └── NextFly\_launcher.bat      # Script principale per build e avvio

├── config/

│   ├── config.env.example        # Esempio di configurazione (pubblico)

│   └── config.env                # Configurazione reale (locale, non versionata)

├── README.md                     # Versione inglese di questo documento

├── README.it.md                  # Questo documento (italiano)

├── README.ru.md                  # Versione russa di questo documento

└── .gitignore                    # Regole di esclusione Git





---



\## ⚙️ Configurazione



1\. Clona il repository:

&nbsp;  bash

&nbsp;  git clone https://github.com/AngelDragon999/NextFly.git

&nbsp;  



2\. Copia il file di esempio e personalizzalo:

&nbsp;  bash

&nbsp;  cd NextFly/config

&nbsp;  copy config.env.example config.env

&nbsp;  



3\. Modifica `config.env`  

&nbsp;  Aggiorna i percorsi dei tuoi progetti locali, JDK, Maven e server secondo il tuo ambiente.



---



\## 🚀 Uso dello Script



1\. Apri il prompt dei comandi nella cartella `scripts/`:

&nbsp;  bash

&nbsp;  cd ..\\scripts

&nbsp;  



2\. Esegui lo script:

&nbsp;  bash

&nbsp;  NextFly\_launcher.bat

&nbsp;  



3\. Segui il menu interattivo per:

&nbsp;  - Avviare i server dei progetti

&nbsp;  - Compilare i progetti con Maven

&nbsp;  - Cambiare tra JDK 8, JDK 21 e altre versioni personalizzabili



---



\## ⚠️ Note Importanti



\- Non committare mai `config.env`: contiene percorsi locali e dati sensibili.

\- Tutti gli script leggono le variabili da `config.env` per funzionare correttamente.

\- Per aggiungere nuovi script, inseriscili nella cartella `scripts/` e aggiorna il README con le istruzioni.



---



\## ✅ Vantaggi



1\. Gestione centralizzata dei progetti

2\. Evita errori di percorso e di versione JDK

3\. Facilita la distribuzione e la collaborazione tramite Git

4\. Pronto per estensioni e nuovi script futuri



