import pandas as pd
import matplotlib.pyplot as plt
import re

def analyze_access_log(log_file):
    print(f"Chargement et parsing du fichier : {log_file}")
    
    pattern = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) \S+ "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    
    with open(log_file) as f:
        data = [m.groupdict() for line in f if (m := pattern.match(line))]
    
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    df['status'] = pd.to_numeric(df['status'], errors='coerce')
    
    print("\nAperçu des données chargées :")
    print(df.head())

    errors_404_df = df[df['status'] == 404].copy()
    print(f"\nNombre total d'erreurs 404 : {len(errors_404_df)}")
    print(errors_404_df.head())

    top_ips = errors_404_df['ip'].value_counts().nlargest(5)
    print("\nTop 5 IPs générant des erreurs 404 :")
    print(top_ips)

    plt.figure(figsize=(10, 6))
    top_ips.plot(kind='bar', color='skyblue')
    plt.title('Top 5 des IPs générant des erreurs 404')
    plt.xlabel('Adresses IP')
    plt.ylabel('Nombre d\'erreurs 404')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    bots_df = df[df['user_agent'].str.contains("bot|crawler|spider", case=False, na=False)].copy()
    print(f"\nRequêtes de bots détectées : {len(bots_df)}")

    if not bots_df.empty:
        print("\nIPs suspectes :")
        for ip in bots_df['ip'].unique()[:10]:
            print(f"- {ip}")
        
        bot_404 = bots_df[bots_df['status'] == 404]
        if not errors_404_df.empty:
            perc = (len(bot_404) / len(errors_404_df)) * 100
            print(f"\n% d'erreurs 404 provenant de bots : {perc:.2f}%")
        else:
            print("\nAucune erreur 404 pour calculer le % de bots.")
    else:
        print("\nAucune activité de bot détectée.")

    print("\n--- Discussion ---")
    print("- Identifiez les IPs fautives à bloquer")
    print("- Vérifiez les ressources manquantes")
    print("- Améliorez le fichier robots.txt")
    print("- Analysez les User-Agents suspects")
    print("- Songez à un système IDS/IPS")

analyze_access_log('access.log')
