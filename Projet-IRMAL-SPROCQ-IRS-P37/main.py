import os
import sys
from log_parser import parse_linux_auth_log
from data_analyzer import analyze_and_visualize_ips, detect_bots_or_scanners
from network_scanner import simple_port_scan, multi_threaded_port_scan, COMMON_PORTS
import pandas as pd

def display_menu():
    print("\n--- Menu Principal ---")
    print("1. Analyser les logs Linux (auth.log)")
    print("2. Traiter et visualiser les données (Analyse statistique et Graphique)")
    print("3. Scanner les ports réseau")
    print("4. Quitter")

def main():
    all_extracted_ips = {}
    all_pertinent_log_lines = []
    top_n_ips_for_scan = []
    suspicious_ips_from_analysis = []
    graph_output_path = ""

    while True:
        display_menu()
        choice = input("Choisissez une option: ")

        if choice == '1':
            print("\n--- Analyse de Logs Linux (auth.log) ---")
            auth_log_file = 'logs/auth.log'
            auth_ips, auth_lines = parse_linux_auth_log(auth_log_file)
            if auth_ips:
                all_extracted_ips.update(auth_ips)
                all_pertinent_log_lines.extend(auth_lines)
                print(f"IPs extraites de {auth_log_file}: {auth_ips}")
            else:
                print(f"Aucune IP extraite ou le fichier '{auth_log_file}' n'a pas été trouvé ou est vide.")

            if all_extracted_ips:
                print(f"\nTotal des IPs collectées jusqu'à présent: {sum(all_extracted_ips.values())} occurrences pour {len(all_extracted_ips)} IPs uniques.")
                print("\n--- Lignes de logs pertinentes trouvées ---")
                for line in all_pertinent_log_lines:
                    print(f"- {line}")
                print("------------------------------------------")


        elif choice == '2':
            print("\n--- Traitement & Visualisation (Analyse des données) ---")
            if not all_extracted_ips:
                print("Veuillez d'abord analyser des logs (Option 1) pour avoir des données IP à traiter.")
                continue

            # analyze_and_visualize_ips génère le top N des IPs
            top_n_ips_for_scan, graph_output_path = analyze_and_visualize_ips(all_extracted_ips, "Top IPs Suspectes des Logs Linux")
            
            # Détection des bots/scanners (basé sur User-Agent)
            current_suspicious_ua_ips = detect_bots_or_scanners('logs/auth.log')
            if current_suspicious_ua_ips:
                print(f"IPs suspectes détectées via User-Agent: {current_suspicious_ua_ips}")
                suspicious_ips_from_analysis = current_suspicious_ua_ips # Stocke spécifiquement ces IPs
                # Ajoute les IPs suspectes au Top N si elles n'y sont pas déjà, pour une utilisation ultérieure si besoin
                for ip in current_suspicious_ua_ips:
                    if ip not in top_n_ips_for_scan:
                        top_n_ips_for_scan.append(ip) 
            else:
                print("Aucune IP suspecte détectée via User-Agent.")
                suspicious_ips_from_analysis = [] # S'assurer que la liste est vide si rien n'est trouvé

        elif choice == '3':
            print("\n--- Scan de Ports Réseau ---")
            ips_to_scan = []

            # Proposer UNIQUEMENT les IPs suspectes en premier
            if suspicious_ips_from_analysis:
                print(f"IPs suspectes détectées (pour le scan): {suspicious_ips_from_analysis}")
                confirm_scan = input("Voulez-vous scanner ces IPs suspectes? (oui/non): ").lower()
                if confirm_scan == 'oui':
                    ips_to_scan = suspicious_ips_from_analysis
            
            # Si aucune IP n'a été sélectionnée (soit pas d'IP suspecte, soit l'utilisateur a refusé)
            if not ips_to_scan:
                manual_input = input("Entrez des IPs à scanner (séparées par des virgules, ex: 127.0.0.1,8.8.8.8) ou laissez vide pour annuler: ")
                if manual_input:
                    ips_to_scan = [ip.strip() for ip in manual_input.split(',')]
                else:
                    print("Aucune IP sélectionnée pour le scan.")
                    continue


            if not ips_to_scan:
                print("Aucune IP valide pour le scan.")
                continue

            scan_type = input("Quel type de scan voulez-vous ? (mono-thread / multi-thread): ").lower()
            verbose_option = input("Voulez-vous afficher les ports fermés (--verbose) ? (oui/non): ").lower() == 'oui'

            open_ports_results = {}
            if scan_type == 'mono-thread':
                for ip in ips_to_scan:
                    open_ports_results.update(simple_port_scan(ip, ports=COMMON_PORTS, verbose=verbose_option))
            elif scan_type == 'multi-thread':
                num_threads_str = input("Entrez le nombre de threads (par défaut: 10): ")
                num_threads = int(num_threads_str) if num_threads_str.isdigit() else 10
                open_ports_results = multi_threaded_port_scan(ips_to_scan, ports=COMMON_PORTS, num_threads=num_threads, verbose=verbose_option)
            else:
                print("Type de scan non reconnu.")
                continue

            print("\n--- Résultat du Scan de Ports ---")
            if open_ports_results:
                for ip, ports in open_ports_results.items():
                    print(f"IP: {ip} -> Ports ouverts: {ports if ports else 'Aucun'}")
            else:
                print("Aucun port ouvert trouvé ou aucune IP scannée.")

            export_choice = input("Voulez-vous exporter les résultats du scan au format CSV ? (oui/non): ").lower()
            if export_choice == 'oui':
                export_scan_results_to_csv(open_ports_results, "scan_results.csv")

        elif choice == '4':
            print("Quitting...")
            sys.exit()
        else:
            print("Option invalide. Veuillez choisir une option valide.")

def export_scan_results_to_csv(results, filename="scan_results.csv"):
    """Exporte les résultats du scan dans un fichier CSV."""
    if not results:
        print("Aucun résultat à exporter.")
        return

    output_dir = 'exports'
    os.makedirs(output_dir, exist_ok=True)

    full_path = os.path.join(output_dir, filename)
    try:
        data_for_df = []
        for ip, ports in results.items():
            ports_str = ', '.join(map(str, ports)) if ports else 'None'
            data_for_df.append({'Adresse IP': ip, 'Ports ouverts': ports_str})

        df = pd.DataFrame(data_for_df)
        df.to_csv(full_path, index=False, sep=';') 
        print(f"Résultats exportés en CSV vers {full_path}")
    except Exception as e:
        print(f"Erreur lors de l'export CSV: {e}")

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs('graphs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    main()