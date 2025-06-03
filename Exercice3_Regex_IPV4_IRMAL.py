import re

def check_ipv4():
  ip_address = input("Veuillez entrer une adresse IP : ")
  ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
  
  if re.match(ipv4_pattern, ip_address):
    print(f"'{ip_address}' est une adresse IPv4 valide.")
  else:
    print(f"'{ip_address}' n'est PAS une adresse IPv4 valide.")

if __name__ == "__main__":
  check_ipv4()