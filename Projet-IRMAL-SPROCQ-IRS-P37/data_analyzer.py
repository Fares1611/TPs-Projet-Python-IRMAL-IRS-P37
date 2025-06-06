import pandas as pd
import matplotlib.pyplot as plt
import os
import re

def analyze_and_visualize_ips(ip_data, title="Top 5 des IPs les plus actives", save_path="top_ips_chart.png"):
    if not ip_data:
        print("Aucune donnée IP à analyser ou visualiser.")
        return [], None

    print("Analyse et visualisation des données IP...")

    df = pd.DataFrame(list(ip_data.items()), columns=['IP Address', 'Occurrences'])
    df = df.sort_values(by='Occurrences', ascending=False)

    print("\nDataFrame des IPs et occurrences:")
    print(df)

    top_n = min(5, len(df))
    top_ips = df.head(top_n)

    print(f"\nTop {top_n} des IPs les plus actives:")
    print(top_ips)

    plt.figure(figsize=(10, 6))
    plt.bar(top_ips['IP Address'], top_ips['Occurrences'], color='skyblue')
    plt.xlabel('Adresse IP')
    plt.ylabel('Nombre d\'occurrences')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    output_dir = 'graphs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    full_save_path = os.path.join(output_dir, save_path)
    plt.savefig(full_save_path)
    print(f"Graphique enregistré sous: {full_save_path}")
    plt.close()

    return top_ips['IP Address'].tolist(), full_save_path

def detect_bots_or_scanners(log_file_path):
    print(f"\nTentative de détection de bots/scanners dans {log_file_path} (basé sur User-Agent)...")
    if not os.path.exists(log_file_path):
        print(f"Erreur: Le fichier {log_file_path} n'a pas été trouvé pour la détection de bots.")
        return []

    suspicious_ips = set()
    bot_signatures = [
        "bot", "spider", "crawl", "scanner", "nmap", "nikto", "masscan",
        "ahrefsbot", "semrushbot", "dotbot", "bingbot", "googlebot", "shellbot", "datastealerpro"
    ]

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) -.*?"[^"]*?"\s*\d+\s+\d+\s*"([^"]*)"', line)
                if match:
                    ip = match.group(1)
                    user_agent = match.group(2).lower()
                    for signature in bot_signatures:
                        if signature in user_agent:
                            suspicious_ips.add(ip)
                            break
        if not suspicious_ips:
            print("Aucun User-Agent suspect détecté (correspondant aux signatures et au format attendu).")
        return list(suspicious_ips)
    except Exception as e:
        print(f"Une erreur est survenue lors de la détection de bots: {e}")
        return []