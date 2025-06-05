

- Pour le Exercice 4, utiliser le fichier liste_ips.txt

- Pour le TP1, utiliser le fichier mots_de_passe_faibles.txt

- Pour le TP2, utiliser le fichier auth.log

- Pour le TP3 voici la liste des commandes à executer dans le terminal :

#Execution script en mode mono-threads (par-défaut si l'on indique pas de threads on est en mono-threads) avec export résultat vers fichier CSV
python TP3_Scanner_IRMAL.py --ip 172.16.3.105 --start-port 1 --end-port 200 --output resultat_scan.csv

#Execution script en mode mono-threads (par-défaut si l'on indique pas de threads on est en mono-threads) avec export résultat vers fichier CSV + verbose
python TP3_Scanner_IRMAL.py --ip 172.16.3.105 --start-port 1 --end-port 200 --output resultat_scan.csv

#Execution script en mode multi-threads avec export résultat vers fichier CSV et mode verbose
python TP3_Scanner_IRMAL.py --ip 172.16.3.105 --start-port 1 --end-port 200 --threads 30 --output resultat_scan.csv --verbose

- Pour le TP4, utiliser le fichier de log access.log

- Le mini-Projet Python à été réaliser par IRMAL Farès (moi-même) et SPROCQ Adrien, il est présent sur mon GitHub 




