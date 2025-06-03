#Dans ce code le script lis un fichier texte contenant des adresses et le script vérifie si ces adresses respectes le format IPv4
import re

ipv4_patron = r"^(?:(?:0|[1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:0|[1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

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
