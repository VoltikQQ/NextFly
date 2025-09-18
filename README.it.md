============================

NextFly Project Launcher

============================



NextFly è uno strumento batch per automatizzare la compilazione e l’avvio dei progetti locali.

Permette di gestire più progetti, scambiare versioni JDK, avviare server e lanciare compilazioni Maven facilmente da un’unica interfaccia.



=================================

⦁   Struttura del Repository

=================================



NextFly/

├── scripts/

│   └── NextFly\_launcher.bat  # Script principale per build e avvio

├── config/

│   ├── config.env.example    # Esempio di configurazione (pubblico)

│   └── config.env            # Configurazione reale (locale, non versionata)

├── README.md		           # Versione inglese di questo documento

├── README.it.md              # Questo documento

├── README.ru.md              # Versione russa di questo documento

└── .gitignore                # Documento di esclusione Git



=================================

⦁	Configuazione

=================================



**Clona il repository:**



git clone https://github.com/AngelDragon999/NextFly.git



**Copia il file di esempio e personalizzalo:**



cd NextFly\\config

copy config.env.example config.env



Apri config.env e aggiorna i percorsi dei tuoi progetti locali, JDK, Maven e server secondo il tuo ambiente.



===============================

⦁	Uso dello Script

===============================



Apri il prompt dei comandi nella cartella scripts/:



cd ..\\scripts



Lancia lo script:



NextFly\_launcher.bat



Segui il menu interattivo per:



\- Avviare i server dei progetti

\- Compilare i progetti con Maven

\- Scambiare tra JDK 8, JDK 21 e altri che puoi aggiungere.



===============================

⦁	Note Importanti

===============================



\- Non commitare mai config.env, contiene percorsi locali e configurazioni sensibili.

\- Tutti gli script leggono le variabili da config.env per funzionare correttamente.

\- Per aggiungere nuovi script, mettili nella cartella scripts/ e aggiorna il README con le istruzioni.



===============================

⦁	Vantaggi

===============================



1\. Gestione centralizzata dei progetti

2\. Evita errori di percorso e JDK

3\. Facilita la distribuzione e la collaborazione tramite Git

4\. Pronto per aggiungere nuovi script in futuro



