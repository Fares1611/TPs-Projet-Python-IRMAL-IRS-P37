import re
from collections import defaultdict

def parse_linux_auth_log(log_file_path):
    ip_occurrences = defaultdict(int)
    pertinent_lines = []
    print(f"Parsing du fichier de log Linux: {log_file_path}")

    suspicious_sshd_patterns = [
        # Tentatives de mot de passe échouées (couvre utilisateurs normaux et invalides)
        re.compile(
            r'Failed password for (invalid user )?\S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ),
        # Déconnexions pendant la phase de pré-authentification (souvent signe de scan ou brute-force)
        re.compile(
            r'Received disconnect from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+:\s*\d+.*\[preauth\]'
        ),
        re.compile(
            r'Disconnected from authenticating user \S+ (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+ \[preauth\]'
        ),
        # Utilisateur invalide (si non couvert par "Failed password for invalid user")
        re.compile(
            r'Invalid user \S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ),
        # Tentatives par des utilisateurs non autorisés par la configuration du serveur
        re.compile(
            r'User \S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) not allowed because not listed in AllowUsers'
        ),
        re.compile(
            r'User \S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) not allowed because not in DenyUsers' # Ajout pour DenyUsers
        ),
        re.compile(
            r'User \S+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) not allowed because (account is locked|password expired)'
        ),
        # Connexion fermée par l'IP, potentiellement suspecte en phase [preauth]
        re.compile(
            r'Connection closed by (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})( port \d+)? \[preauth\]'
        ),
        # PAM: échecs d'authentification qui peuvent aussi indiquer des problèmes
        re.compile(
            r'pam_unix\(sshd:auth\):\s+authentication failure;.*rhost=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ),
    ]

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                extracted_ip = None
                for pattern in suspicious_sshd_patterns:
                    match = pattern.search(line)
                    if match:
                        try:
                            extracted_ip = match.group('ip')
                            if extracted_ip and extracted_ip != '0.0.0.0': 
                                break  
                            else:
                                extracted_ip = None 
                        except IndexError:
                            print(f"Avertissement: Pattern {pattern.pattern} trouvé mais groupe 'ip' manquant dans la ligne: {line.strip()}")
                            continue
                
                if extracted_ip:
                    ip_occurrences[extracted_ip] += 1
                    pertinent_lines.append(line.strip())
        
        if not pertinent_lines:
            print("Aucune ligne SSHD suspecte correspondant aux patterns élargis n'a été trouvée.")
        else:
            print(f"Parsing des logs Linux (événements SSHD suspects) terminé. {len(pertinent_lines)} lignes pertinentes trouvées.")
        return dict(ip_occurrences), pertinent_lines
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {log_file_path} n'a pas été trouvé.")
        return {}, []
    except Exception as e:
        print(f"Une erreur est survenue lors du parsing du fichier de log Linux: {e}")
        return {}, []