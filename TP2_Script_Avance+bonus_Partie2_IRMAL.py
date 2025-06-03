import re
from collections import Counter
import matplotlib.pyplot as plt
import csv

with open('auth.log', 'r') as file:
    lignes = file.readlines()

regex_ip = r'(\d{1,3}(?:\.\d{1,3}){3})'
lignes_echec = [ligne for ligne in lignes if "Failed password" in ligne]
lignes_success = [ligne for ligne in lignes if "Accepted password" in ligne]

ips_echec = [re.search(regex_ip, ligne).group(1) for ligne in lignes_echec if re.search(regex_ip, ligne)]
ips_success = [re.search(regex_ip, ligne).group(1) for ligne in lignes_success if re.search(regex_ip, ligne)]

compteur_echec = Counter(ips_echec)
compteur_success = Counter(ips_success)

def afficher_top():
    top5_echec = compteur_echec.most_common(5)
    print("\nTop 5 IPs avec tentatives échouées :")
    for ip, count in top5_echec:
        print(f"{ip} : {count} échecs")
    
    ips, counts = zip(*top5_echec)
    plt.figure(figsize=(8, 5))
    plt.bar(ips, counts, color='red')
    plt.title('Top 5 IPs - Tentatives SSH échouées')
    plt.xlabel('Adresse IP')
    plt.ylabel('Nombre d’échecs')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def afficher_comparaison():
    toutes_ips = set(compteur_echec.keys()) | set(compteur_success.keys())
    ips_liste = sorted(toutes_ips)
    echoues = [compteur_echec.get(ip, 0) for ip in ips_liste]
    reussis = [compteur_success.get(ip, 0) for ip in ips_liste]

    plt.figure(figsize=(10, 6))
    x = range(len(ips_liste))
    plt.bar(x, echoues, width=0.4, label='Échecs', color='red', align='center')
    plt.bar(x, reussis, width=0.4, label='Réussites', color='green', align='edge')
    plt.xticks(ticks=x, labels=ips_liste, rotation=45, ha='right')
    plt.title('Comparaison IPs : Échecs vs Réussites')
    plt.xlabel('Adresse IP')
    plt.ylabel('Nombre de tentatives')
    plt.legend()
    plt.tight_layout()
    plt.show()

def exporter_csv():
    toutes_ips = set(compteur_echec.keys()) | set(compteur_success.keys())
    ips_liste = sorted(toutes_ips)

    with open('resultats_connexions_ssh.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['IP', 'Echecs', 'Réussites'])
        for ip in ips_liste:
            writer.writerow([ip, compteur_echec.get(ip, 0), compteur_success.get(ip, 0)])
    print("Résultats exportés dans le fichier 'resultats_connexions_ssh.csv'.")

def menu():
    while True:
        print("\n========= MENU PRINCIPAL =========")
        print("1. Afficher le top 5 des IPs avec le plus d'échecs")
        print("2. Comparer les échecs et les réussites par IP")
        print("3. Exporter tous les résultats en fichier CSV")
        print("4. Quitter le programme")
        print("===================================")

        choix = input("Choisissez une option (1-4) : ")

        if choix == '1':
            afficher_top()
        elif choix == '2':
            afficher_comparaison()
        elif choix == '3':
            exporter_csv()
        elif choix == '4':
            print("Fermeture du programme.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()