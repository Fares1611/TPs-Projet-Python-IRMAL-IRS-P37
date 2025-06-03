import re
from collections import Counter

log_content = []

try:
    with open('auth.log', 'r') as f:
        log_content = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print("Fichier auth.log non trouvé.")

failed_lines = [line for line in log_content if "Failed password" in line]

ip_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
extracted_ips = []
for line in failed_lines:
    match = re.search(ip_regex, line)
    if match:
        extracted_ips.append(match.group(0))

ip_counts = Counter(extracted_ips)

print("\nTop 5 des IPs avec le plus de tentatives de connexion échouées :")
if not ip_counts:
    print("Aucune tentative de connexion échouée trouvée ou le fichier log était vide/non trouvé.")
else:
    for ip, count in ip_counts.most_common(5):
        print(f"  IP: {ip}, Échecs: {count}")
        