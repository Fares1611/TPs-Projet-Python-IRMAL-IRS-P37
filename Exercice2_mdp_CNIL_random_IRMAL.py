#Dans ce code un mot de passe avec les recommandation de la CNIL est généré automatiquement
import random
import string 

LISTE_MAJ = string.ascii_uppercase
LISTE_MIN = string.ascii_lowercase
LISTE_NUM = string.digits
LISTE_SPECIAUX = "!@#$%^&*()-=+[]<>.?;:"
CARACTERES_AMBIGUS = {'l', '1', 'i', 'I', '0', 'O'}

liste_maj_secure = [c for c in LISTE_MAJ if c not in CARACTERES_AMBIGUS]
liste_min_secure = [c for c in LISTE_MIN if c not in CARACTERES_AMBIGUS]
liste_num_secure = [c for c in LISTE_NUM if c not in CARACTERES_AMBIGUS]
liste_speciaux_secure = [c for c in LISTE_SPECIAUX if c not in CARACTERES_AMBIGUS]

pool_total_secure = liste_maj_secure + liste_min_secure + liste_num_secure + liste_speciaux_secure

def generer_mot_de_passe_cnil():

    # Choisir une longueur aléatoire entre 12 et 14
    longueur_mdp = random.randint(12, 14)
    
    mot_de_passe_en_creation = []

    # S'assurer d'avoir au moins un caractère de chaque type sécurisé
    mot_de_passe_en_creation.append(random.choice(liste_maj_secure))
    mot_de_passe_en_creation.append(random.choice(liste_min_secure))
    mot_de_passe_en_creation.append(random.choice(liste_num_secure))
    mot_de_passe_en_creation.append(random.choice(liste_speciaux_secure))

    # Compléter le reste du mot de passe avec des caractères du pool sécurisé
    nombre_caracteres_restants = longueur_mdp - len(mot_de_passe_en_creation)
    for _ in range(nombre_caracteres_restants):
        mot_de_passe_en_creation.append(random.choice(pool_total_secure))

    # Mélanger les caractères
    random.shuffle(mot_de_passe_en_creation)
    
    mdp_genere = "".join(mot_de_passe_en_creation)
    return mdp_genere

# Programme principal
if __name__ == "__main__":
    mot_de_passe_final = generer_mot_de_passe_cnil()
    print(f"\nMot de passe généré : {mot_de_passe_final}")
