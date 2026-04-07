## Panoramica del Progetto  

Il **Christmas Project** è un prototipo completo di **piattaforma web per casinò online** sviluppato con **Flask**.  
Nato inizialmente dall'**End-of-Year-Project-for-Computer-Science-Poker**, si è evoluto rapidamente in un ecosistema software funzionale che include:

- Gestione utenti e autenticazione (richiede futuri aggiornamenti e perfezioni) 
- Sistema di cassa e conversione denaro ↔ fiches (non funziona completamente) 
- Interfaccia grafica per diversi giochi (con focus sul **Texas Hold’em Poker**; ancora in fase di sperimentazione)  
- Area amministrazione (richiede futuri aggiornamenti e perfezioni) 
- Dashboard utente (richiede futuri aggiornamenti e perfezioni)  
- Grafici statistici (richiedono futuri aggiornamenti e perfezioni) 
- Musica di sottofondo (identica all'End-of-Year-Project-for-Computer-Science-Poker) 
- Design tematico da casinò migliorato e più ampio

Questa **prima versione** rappresenta un’importante tappa evolutiva: ha permesso di sperimentare molte tecnologie e concetti, ma evidenzia anche i limiti tipici di un progetto monolitico nato in modo organico.

### Obiettivi raggiunti nella Versione 1
  
- Sistema di registrazione e login utenti (richiedono futuri aggiornamenti e perfezioni) 
- Gestione delle credenziali admin (richiedono futuri aggiornamenti e perfezioni)
- Interfacce HTML/CSS responsive con tema casinò aggiornate (richiedono futuri aggiornamenti e perfezioni)
- Generazione di grafici statistici con Matplotlib per primi test grafici (richiedono futuri aggiornamenti e perfezioni)
- Tentativi di separazione della logica in più moduli Python (richiede futuri aggiornamenti e perfezioni)
- Pagine dedicate a login, registrazione, reset password, dashboard, cassa, poker e regole (richiedono futuri aggiornamenti e perfezioni)

### Problemi Principali della Versione 1

Sebbene ricca di funzionalità, questa versione presenta diverse criticità strutturali e tecniche:

1. **Mancanza di modularità**  
   Il file `casino.py` contiene **tutta** la logica dell’applicazione (routing, autenticazione, gioco, cassa, admin). Questo rende il codice difficile da mantenere, estendere e testare.

2. **Sicurezza insufficiente**  
   - Email e password dell’admin sono scritte in chiaro nel codice sorgente.  
   - Esiste un file `plain_passwords.json` con password non hashate.  
   - Il sistema di reset password è solo parzialmente funzionante.

3. **Assenza di un vero database**  
   Tutti i dati (utenti, admin, mazzo, fiches, utenti eliminati) sono salvati in file JSON. Adatto per un prototipo, ma non scalabile né performante per un’applicazione reale.

4. **Funzionalità incomplete o instabili**  
   - Il cassiere non funziona correttamente in tutte le operazioni.  
   - Il form “Forgot Password” non invia email reali.  
   - La pagina di gioco del poker (`play.html`) mostra solo una pagina di test o non funziona correttamente.  
   - Alcuni grafici sono basilari e poco integrati.  
   - Diversi file e immagini sono presenti nella struttura ma non utilizzati.

5. **Problemi di UI/UX**  
   - L’icona dell’occhio (mostra/nascondi password) smette di funzionare dopo il primo click.  
   - Alcuni layout non sono coerenti tra le pagine.  
   - Immagini e risorse statiche non sempre collegate correttamente.

### Struttura del Progetto (Versione 1)

La seguente struttura rappresenta l’organizzazione attuale del progetto Christmas-project.

```text
Christmas-project/
│   
├── python_files/                               # Contiene i file Python che implementano la logica del 
│   ├── admin_data.py                           # Gestisce caricamento, salvataggio e verifica delle credenziali amministrative tramite file JSON, includendo hashing SHA‑256 
│   │                                             delle password e una utility da terminale per configurare rapidamente l’account admin.
│   ├── cashier.py                              # Gestisce metodi di pagamento e conversione denaro–fiches: definisce PaymentMethod, salva/carica i metodi in JSON, permette 
│   │                                             aggiunta/rimozione/ricerca e calcola scambi con commissioni tramite CasinoCashier.
│   ├── deck_data.py                            # Gestisce il caricamento, la creazione e il salvataggio del mazzo tramite JSON: genera un deck standard completo per tutti i 
│   │                                             semi e fornisce un’interfaccia per leggere o ricostruire i dati del mazzo.
│   ├── get_data_from_JSON.py                   # Centralizza l’accesso ai dati JSON di utenti, mazzo e fiches: inizializza UserData e DeckData, fornisce utility per aggiungere │   │                                             utenti e genera tabelle riepilogative per fiches, utenti e carte tramite tabulate.
│   ├── password_manager.py                     # Gestisce hashing, reset e aggiornamento delle password utente tramite JSON: genera token di recupero, verifica la loro 
│   │                                             validità e aggiorna in sicurezza le credenziali archiviate.
│   ├── plot_casino_revenue.py                  # Gestisce lettura e aggiornamento dei dati utenti e genera grafici dei ricavi del casinò: salva bilanci, vincite/perdite e   │   │                                             produce un bar chart con Matplotlib basato sui saldi correnti.
│   ├── plot_user_growth.py                     # Analizza le date di registrazione degli utenti dal JSON e genera un grafico dell’andamento iscrizioni nel tempo tramite 
│   │                                             Matplotlib, calcolando registrazioni cumulative e tracciandole cronologicamente.
│   ├── plot_user_wins_losses.py                # Analizza vincite e perdite degli utenti dal JSON e genera un grafico a barre colorato (verde per vincite, rosso per perdite) 
│   │                                             tramite Matplotlib, includendo legenda e salvataggio dell’immagine.
│   └── user_data.py                            # Gestisce archiviazione e gestione completa degli utenti tramite JSON: crea file predefiniti, registra nuovi utenti con 
│                                                 password hashate, autentica credenziali, aggiorna saldo e password, elabora transazioni e consente l’eliminazione sicura degli 
│                                                 account.          
│   
├── static/                                     # Contiene tutte le risorse statiche come immagini, stili CSS e musica.
│   ├── card_images/                            # Contiene le immagini di tutte le carte da gioco riutilizzabili per ogni gioco di carte del casinò.
│   │   ├── hearts/                             # Contiene le immagini delle carte di cuori, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │   │   ├── 01_hearts.png                   # Immagine dell'Asso di cuori.
│   │   │   ├── 02_hearts.png                   # Immagine del 2 di cuori.
│   │   │   ├── 03_hearts.png                   # Immagine del 3 di cuori.
│   │   │   ├── 04_hearts.png                   # Immagine del 4 di cuori.
│   │   │   ├── 05_hearts.png                   # Immagine del 5 di cuori.
│   │   │   ├── 06_hearts.png                   # Immagine del 6 di cuori.
│   │   │   ├── 07_hearts.png                   # Immagine del 7 di cuori.
│   │   │   ├── 08_hearts.png                   # Immagine del 8 di cuori.
│   │   │   ├── 09_hearts.png                   # Immagine del 9 di cuori.
│   │   │   ├── 10_hearts.png                   # Immagine del 10 di cuori.
│   │   │   ├── 11_hearts.png                   # Immagine del Jack di cuori.
│   │   │   ├── 12_hearts.png                   # Immagine della Regina di cuori.
│   │   │   └── 13_hearts.png                   # Immagine del Re di cuori.
│   │   │                   
│   │   ├── diamonds/                           # Contiene le immagini delle carte di quadri, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re). 
│   │   │   ├── 01_diamonds.png                 # Immagine dell'Asso di quadri. 
│   │   │   ├── 02_diamonds.png                 # Immagine del 2 di quadri. 
│   │   │   ├── 03_diamonds.png                 # Immagine del 3 di quadri. 
│   │   │   ├── 04_diamonds.png                 # Immagine del 4 di quadri. 
│   │   │   ├── 05_diamonds.png                 # Immagine del 5 di quadri. 
│   │   │   ├── 06_diamonds.png                 # Immagine del 6 di quadri. 
│   │   │   ├── 07_diamonds.png                 # Immagine del 7 di quadri. 
│   │   │   ├── 08_diamonds.png                 # Immagine del 8 di quadri. 
│   │   │   ├── 09_diamonds.png                 # Immagine del 9 di quadri. 
│   │   │   ├── 10_diamonds.png                 # Immagine del 10 di quadri. 
│   │   │   ├── 11_diamonds.png                 # Immagine del Jack di quadri. 
│   │   │   ├── 12_diamonds.png                 # Immagine della Regina di quadri. 
│   │   │   └── 13_diamonds.png                 # Immagine del Re di quadri. 
│   │   │ 
│   │   ├── clubs/                              # Contiene le immagini delle carte di fiori, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │   │   ├── 01_clubs.png                    # Immagine dell'Asso di fiori.
│   │   │   ├── 02_clubs.png                    # Immagine del 2 di fiori.
│   │   │   ├── 03_clubs.png                    # Immagine del 3 di fiori.
│   │   │   ├── 04_clubs.png                    # Immagine del 4 di fiori.
│   │   │   ├── 05_clubs.png                    # Immagine del 5 di fiori.
│   │   │   ├── 06_clubs.png                    # Immagine del 6 di fiori.
│   │   │   ├── 07_clubs.png                    # Immagine del 7 di fiori.
│   │   │   ├── 08_clubs.png                    # Immagine del 8 di fiori.
│   │   │   ├── 09_clubs.png                    # Immagine del 9 di fiori.
│   │   │   ├── 10_clubs.png                    # Immagine del 10 di fiori.
│   │   │   ├── 11_clubs.png                    # Immagine del Jack di fiori.
│   │   │   ├── 12_clubs.png                    # Immagine della Regina di fiori.
│   │   │   └── 13_clubs.png                    # Immagine del Re di fiori.
│   │   │
│   │   └── spades/                             # Contiene le immagini delle carte di picche, numerate da 1 a 13 (Asso, 2-10, Jack, Regina, Re).
│   │       ├── 01_spades.png                   # Immagine dell'Asso di picche.
│   │       ├── 02_spades.png                   # Immagine del 2 di picche.
│   │       ├── 03_spades.png                   # Immagine del 3 di picche.
│   │       ├── 04_spades.png                   # Immagine del 4 di picche.
│   │       ├── 05_spades.png                   # Immagine del 5 di picche.
│   │       ├── 06_spades.png                   # Immagine del 6 di picche.
│   │       ├── 07_spades.png                   # Immagine del 7 di picche.
│   │       ├── 08_spades.png                   # Immagine del 8 di picche.
│   │       ├── 09_spades.png                   # Immagine del 9 di picche.
│   │       ├── 10_spades.png                   # Immagine del 10 di picche.
│   │       ├── 11_spades.png                   # Immagine del Jack di picche.
│   │       ├── 12_spades.png                   # Immagine della Regina di picche.
│   │       └── 13_spades.png                   # Immagine del Re di picche.
│   │    
│   ├── casino_games_photos/                    # Contiene le immagini dei giochi del casinò.
│   │   ├── american_roulette.jpg               # Placeholder per il gioco della roulette americana.
│   │   ├── baccarat.jpeg                       # Placeholder per il gioco del baccarat.
│   │   ├── big_six_wheel.png                   # Placeholder per il gioco del big six wheel.
│   │   ├── blackjack.jpg                       # Placeholder per il gioco del blackjack.
│   │   ├── caribbean_stud_poker.jpg            # Placeholder per il gioco del caribbean stud poker.
│   │   ├── crabs.jpg                           # Placeholder per il gioco dei crabs. 
│   │   ├── deuces_wild.jpg                     # Placeholder per il gioco del deuces wild.
│   │   ├── dream_catcher.jpg                   # Placeholder per il gioco del dream catcher.
│   │   ├── e_sports.png                        # Placeholder per il gioco dell'e-sports betting. 
│   │   ├── fantasy_sports.jpg                  # Placeholder per il gioco del fantasy sports betting.
│   │   ├── french_roulette.jpeg                # Placeholder per il gioco della roulette francese. 
│   │   ├── greyhound_racing.jpg                # Placeholder per il gioco del greyhound racing.
│   │   ├── horse_racing.jpeg                   # Placeholder per il gioco dell'horse racing. 
│   │   ├── jacks_or_better.jpeg                # Placeholder per il gioco del jacks or better.
│   │   ├── joker_poker.jpg                     # Placeholder per il gioco del joker poker.
│   │   ├── keno.jpeg                           # Placeholder per il gioco del keno.
│   │   ├── let_it_ride.jpeg                    # Placeholder per il gioco del let it ride.
│   │   ├── mini_baccarat.jpeg                  # Placeholder per il gioco del mini baccarat.
│   │   ├── pai_gow_poker.jpeg                  # Placeholder per il gioco del pai gow poker.
│   │   ├── poker_texas_holdem.jpg              # Placeholder per il gioco del poker texas holdem.
│   │   ├── progressive_slot.jpeg               # Placeholder per il gioco del progressive slot.
│   │   ├── punto_banco.jpeg                    # Placeholder per il gioco del punto banco.
│   │   ├── red_dog.jpeg                        # Placeholder per il gioco del red dog.
│   │   ├── roulette.jpg                        # Placeholder per il gioco della roulette. 
│   │   ├── sic_bo.png                          # Placeholder per il gioco del sic bo.
│   │   ├── three_card_poker.jpeg               # Placeholder per il gioco del three card poker.
│   │   ├── video_poker.jpg                     # Placeholder per il gioco del video poker.
│   │   ├── video_slot.jpg                      # Placeholder per il gioco del video slot.
│   │   ├── virtual_sports.jpg                  # Placeholder per il gioco del virtual sports betting.
│   │   └── war.jpeg                            # Placeholder per il gioco del war.
│   │
│   ├── cashier.jpg                             # Sfondo della pagina del cassiere del casinò.
│   ├── cashier.webp                            # Placeholder per il cassiere del casinò.
│   ├── casino_administrator_background.jpg     # Sfondo della pagina dell'admin del casinò.
│   ├── casino_interior.jpg                     # Sfondo della pagina principale del casinò, con un'atmosfera elegante e accogliente che richiama l'ambiente di un vero casinò.
│   ├── casino_photos.jpg                       # Sfondo della copertina del progetto.
│   ├── email.png                               # Icona utilizzata nei form utente per indicare il campo email.
│   ├── eye_closed.jpeg                         # Icona utilizzata nei form utente per indicare il campo password, con l'occhio chiuso che rappresenta la modalità di 
│   │                                             visualizzazione nascosta della password.
│   ├── eye_open.jpeg                           # Icona utilizzata nei form utente per indicare il campo password, con l'occhio aperto che rappresenta la modalità di 
│   │                                             visualizzazione visibile della password.
│   ├── facebook_icon.png                       # Logo di facebook non usato nel progetto, ma tenuto per un'eventuale aggiornamento futuro.
│   ├── github.jpeg                             # Logo di github usato per indicare l'account github del proprietario del casinò.
│   ├── google_icon.png                         # Logo di google non usato nel progetto, ma tenuto per un'eventuale aggiornamento futuro.
│   ├── instagram.jpeg                          # Logo di instagram usato per indicare gli account instagram del proprietario del casinò.
│   ├── lock_icon.png                           # Icona utilizzata nei form utente per indicare il campo password.
│   ├── monopoly_man.png                        # personaggio principale del monopoly per richiamare un'atmosfera sfarzosa ed elegante del casinò.
│   ├── poker_table.jpg                         # Sfondo della pagina di benvenuto al poker pre-pagina delle regole da gioco.
│   ├── twitter_icon.png                        # Logo di twitter (vecchio) non usato nel progetto, ma tenuto per un'eventuale aggiornamento futuro.
│   ├── user_icon.png                           # Icona utilizzata nei form per rappresentare il campo email e, nella home del casinò, per indicare l’account utente. Nella 
│   │                                             versione attuale funge da icona statica, ma nelle release successive è stata sostituita da un sistema dinamico simile a quello 
│   │                                             di Google: il colore di sfondo dell’avatar cambia automaticamente in base al nome dell’utente. L’implementazione completa di 
│   │                                             questa funzionalità è visibile nella versione aggiornata del progetto Christmas-Project v2.0 – Full 
│   │                                             Refresh, in particolare nel file app/utils/color.py.
│   ├── youtube.jpeg                            # Logo di youtube usato per indicare l'account youtube del proprietario del casinò.
│   │
│   ├── css/                                    # Contiene i file CSS usati per lo stile delle pagine del poker, ognuna con il proprio.
│   │   ├── account.css                         # Gestisce layout, tabelle, input, pulsanti, messaggi di errore e modale, con un design pulito e centrato per la gestione dei 
│   │   │                                         dati utente.
│   │   ├── admin_dashboard.css                 # Gestisce layout, tabelle, grafici, overlay, messaggi di errore e pulsanti (incluso logout), con sfondo dedicato e contenitore 
│   │   │                                         centrale opaco per la visualizzazione dei dati amministrativi.
│   │   ├── admin_login.css                     # Definisce layout centrato, form compatto, campi input, pulsante di accesso e messaggi di errore con un design semplice e 
│   │   │                                         pulito.
│   │   ├── cashier_operations.css              # Gestisce layout, tabelle, form di conversione fiches–denaro, selettori personalizzati, messaggi di errore e overlay grafico 
│   │   │                                         con sfondo dedicato.
│   │   ├── casino_home.css                     # Gestisce sfondo, layout dei giochi, card visive, icona account, messaggi di errore e pulsanti, creando una griglia responsive 
│   │   │                                         con estetica da sala casinò.
│   │   ├── forgot_password.css                 # Gestisce layout centrato, campi input con icone, messaggi di errore/successo, pulsanti e link di reset, con estetica pulita e 
│   │   │                                         leggibile.
│   │   ├── home_poker.css                      # Gestisce sfondo del tavolo, header, pulsanti, layout responsive e messaggi di errore, creando un’interfaccia pulita e centrata 
│   │   │                                         per l’accesso alle modalità di gioco.
│   │   ├── login.css                           # Gestisce layout centrato, campi input, pulsanti, link di recupero password e messaggi di errore, con un design pulito basato 
│   │   │                                         su gradienti e form moderni.
│   │   ├── poker_rules.css                     # Definisce layout, pulsanti di navigazione, tabelle, immagini delle carte e tipografia, offrendo una presentazione ordinata e 
│   │   │                                         leggibile delle regole e delle combinazioni di gioco.
│   │   ├── register.css                        # Gestisce layout centrato, campi input, pulsanti, messaggi di errore locali e globali, con un design pulito basato su gradienti 
│   │   │                                         e form moderni.
│   │   ├── reset_password.css                  # Gestisce layout centrato, campi input con icone, messaggi di errore e successo, pulsanti e feedback visivo, mantenendo un 
│   │   │                                         design coerente con le pagine di login e recupero password.
│   │   ├── user_dashboard.css                  # Gestisce layout, tabelle, form di conversione fiches–denaro, selettori personalizzati, messaggi di errore e overlay grafico, 
│   │   │                                         mantenendo coerenza visiva con l’area cassa.
│   │   └── welcome.css                         # Gestisce sfondo, layout centrato, immagine del Monopoly Man, pulsante “Play” animato e riquadro informativo con link social, 
│   │                                             creando un’introduzione scenografica all’esperienza del casinò.
│   │
│   └── music/                                  # Contiene i file audio utilizzati come sottofondo musicale per le pagine del casinò e del poker, 
│       │                                         oltre a versioni compresse in formato ZIP. 
│       ├── Invisible Cities.mp3                # Sottofondo musicale per la pagina di copertina del progetto, con un'atmosfera misteriosa e coinvolgente.
│       ├── Jazzy Smile.mp3                     # Sottofondo musicale per la pagina principale del casinò, con un ritmo rilassante e sofisticato che richiama l'atmosfera 
│       │                                         di un casinò elegante.
│       ├── Two Cigarettes, Please.mp3          # Sottofondo musicale per la pagina di gioco del poker, con un ritmo più vivace e dinamico che accompagna l'azione del gioco.
│       ├── Welcome to New Orleans.mp3          # Sottofondo musicale per la pagina di gioco del poker, con un ritmo allegro e festoso che richiama l'atmosfera di New Orleans, 
│       │                                         famosa per il suo legame con il poker e i casinò.
│       │
│       ├── invisible-cities.zip                # Versione compressa del file Invisible Cities.mp3, utilizzata per facilitare il download e la gestione dei file audio.
│       ├── jazzy-smile.zip                     # Versione compressa del file Jazzy Smile.mp3, utilizzata per facilitare il download e la gestione dei file audio.
│       ├── two-cigarettes-please.zip           # Versione compressa del file Two Cigarettes, Please.mp3, utilizzata per facilitare il download e la gestione dei file audio.
│       └── welcome-to-new-orleans.zip          # Versione compressa del file Welcome to New Orleans.mp3, utilizzata per facilitare il download e la gestione dei file audio.
│
├── templates/                                  # Contiene tutti i file HTML utilizzati per il rendering delle pagine dell'applicazione.
│   ├── account.html                            # Mostra informazioni personali, saldo, fiches, metodo di pagamento e password con opzione di visibilità, includendo pulsanti di 
│   │                                             navigazione, logout ed eliminazione account con modale di conferma.
│   ├── admin_dashboard.html                    # Dashboard dell'amministratore: mostra la lista utenti, statistiche mensili tramite grafici (guadagni e registrazioni), e 
│   │                                             include controlli rapidi per tornare alla home del casinò o effettuare il logout.
│   ├── admin_login.html                        # Fornisce un semplice form per l’accesso degli admin, con campi email e password e gestione degli errori.
│   ├── cashier_operations.html                 # Pagina delle operazioni del cassiere del casinò: permette di convertire denaro in fiches, riconvertire tutte le fiches, 
│   │                                             aggiornare il saldo, cancellare i dati e visualizzare valori e tabelle aggiornate dinamicamente, con gestione errori e musica 
│   │                                             di sottofondo.
│   ├── casino_home.html                        # Pagina principale del casinò: raccoglie tutti i giochi disponibili e in sviluppo, gestisce l’accesso all’account, mostra 
│   │                                             messaggi di errore, integra musica di sottofondo e fornisce collegamenti rapidi alle sezioni principali come poker e cassa.
│   ├── forgot_password.html                    # Pagina del recupero password: permette di inserire l’email per richiedere il reset, mostra errori o conferme, fornisce il link 
│   │                                             di reimpostazione quando disponibile e include musica di sottofondo e validazione del form.
│   ├── home_poker.html                         # Introduce il Texas Hold’em, offre accesso rapido al gioco e alle regole, e gestisce eventuali messaggi di errore con 
│   │                                             reindirizzamento automatico.
│   ├── login.html                              # Consente l’accesso tramite email e password, gestisce errori e validazione dei campi, include link a registrazione e recupero 
│   │                                             password, pulsante di uscita e musica di sottofondo.
│   ├── play.html                               # Pagina di gioco poker: mostra le carte di giocatore, dealer e community sul tavolo, con musica di sottofondo che cambia 
│   │                                             automaticamente e layout visuale basato sulle immagini delle carte (non funziona per niente questa pagina).
│   ├── poker_rules.html                        # Pagina regole del poker: spiega valori delle carte, semi, scale, ranking delle mani, fasi di gioco e condizioni di vittoria, 
│   │                                             con immagini delle carte e pulsanti per tornare al casinò o alla sezione poker.
│   ├── poker.html                              # Pagina poker (versione semplice): mostra le carte del giocatore, del dealer e della community sul tavolo, usando immagini 
│   │                                             dinamiche generate dal backend.
│   ├── register.html                           # Pagina di registrazione: permette la creazione di un nuovo account con validazione dei campi, gestione degli errori, invio 
│   │                                             asincrono del form, link al login e al recupero password, pulsante di uscita e musica di sottofondo.
│   ├── reset_password.html                     # Pagina reset password: permette di inserire una nuova password tramite token, mostra eventuali errori o conferme e include 
│   │                                             musica di sottofondo.
│   ├── user_dashboard.html                     # Pagina dashboard utente: mostra tutte le fiches possedute con valori e quantità, il totale e il denaro rimanente, permette di 
│   │                                             riconvertire le fiches o cancellare i dati, aggiorna tutto dinamicamente via fetch e include musica di sottofondo.
│   └── welcome.html                            # Pagina di benvenuto: introduce il casinò con animazione centrale, pulsante per entrare nella home del casinò, musica di 
│                                                 sottofondo e sezione informativa con i link ai profili social e ai progetti del creatore.
│
├── json/                                       # Contiene tutti i file .
│   ├── admin.json                              # Contiene le credenziali dell’account admin (email e password hashata) utilizzate per l’accesso all’area di gestione del sistema
│   ├── deck_into_json.json                     # File JSON contenente l’intero mazzo standard da 52 carte: valori da 2 ad A e quattro semi (Hearts, Diamonds, Clubs, 
│   │                                             Spades).                    
│   ├── deleted_users.json                      # Conserva i profili rimossi dal sistema, includendo dati personali, stato delle fiches, metodi di pagamento, date di 
│   │                                             registrazione e cancellazione, per garantire tracciabilità e audit delle operazioni.  
│   ├── plain_passwords.json                    # Contiene coppie email–password non criptate, utilizzate esclusivamente per test locali e mai destinate all’ambiente di 
│   │                                             produzione (tenerle in chiaro porterebbe ad una violazione della privacy essendo che si ha accesso ad ogni account).    
│   └── users.json                              # Struttura che conserva i profili registrati, includendo dati personali, password hashate, stato delle fiches, saldo economico 
│                                                 e data di registrazione. Utilizzato come sistema di gestione utenti nella prima versione del progetto, prima della migrazione 
│                                                 a un database SQLite nel Full Refresh.                                               
│
├── casino.py                                   # File principale dell’applicazione Flask: gestisce routing, autenticazione, registrazione, login, reset password, dashboard 
│                                                 utente e amministratore, operazioni di cassa e logica del poker. Coordina la lettura e scrittura dei file JSON (utenti, admin 
│                                                 fiches, mazzo, account eliminati) fungendo da backend completo della prima versione del progetto.
│
├── Christmas_Project.md                        # presenta degli errori nella struttura del diagramma delle classi dato che non sono collegate tra di loro.
│
├── requirements.txt                            # Gestione Dipendenze
│                                               # - Flask: Framework web leggero usato per gestire routing, server HTTP e rendering delle pagine dell’applicazione.
│                                               # - Requests: Libreria per effettuare richieste HTTP semplici e leggibili, utile per comunicazioni client–server o API esterne.
│                                               # - Tabulate: Libreria utilizzata per formattare tabelle in output testuale.
│                                               # - Matplotlib: Libreria di visualizzazione grafica, utile per generare grafici (ad esempio statistiche, analisi delle 
│                                                               registrazioni o dei guadagni) nella fase di sviluppo o debug.                                            
│                                               
├── LICENSE                                     # Licenza MIT: Uso libero, obbligo di citazione
│                                               # - Garantisce il mio copyright.
│                                               # - Permette a chiunque di usare, copiare e modificare il codice.
│                                               # - Esclude la responsabilità (Disclaimer "AS IS").
│
├── .gitignore                                  # Esclude file e cartelle non necessari dal controllo di versione, come __pycache__, file temporanei, dati sensibili, ecc.
│
├── README.md                                   # Contiene una panoramica del progetto, istruzioni per l'installazione e l'uso, e informazioni sullo sviluppo 
│                                                 futuro.                                  
│                                  
└── PROJECT_STRUCTURE.md                        # File più recente del progetto, che funge da panoramica dettagliata della struttura del progetto, con le caratteristiche di 
                                                  ogni elemento del progetto, e una riflessione sulle aree di disorganizzazione e miglioramento.
```