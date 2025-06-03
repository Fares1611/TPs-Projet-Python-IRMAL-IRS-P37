#Dans ce code le script lis un fichier texte contenant des adresses et le script vérifie s'il respecte le format IPv4
import re

ipv4_patron = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def check_ipv4_fichier():
  try:
    with open('liste_ips.txt', 'r') as file: 
      for line_number, line in enumerate(file, 1):
        ip_address = line.strip()
        
        if not ip_address: 
          continue
          
        if re.fullmatch(ipv4_patron, ip_address): 
          print(f"Ligne {line_number}: '{ip_address}' -> adresse IPv4 VALIDE.")
        else:
          print(f"Ligne {line_number}: '{ip_address}' -> adresse IPv4 INVALIDE.")

  except FileNotFoundError:
      print(f"Erreur : Le fichier n'a pas été trouvé.")

if __name__ == "__main__":
  check_ipv4_fichier()
