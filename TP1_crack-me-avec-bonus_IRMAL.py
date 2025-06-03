#Dans ce code, ont met en place un jeux pour trouvé un mot de passe (défini dans un fichier text ou liste si le fichier n'est pas présent) avec plusieurs tentative et un mode triche 
import random

def charger_mots(nom_fichier="mots_de_passe_faibles.txt"):
    # Liste par défaut si le fichier n'est pas trouvé ou vide
    default = ["123456","password","admin","123456789","qwerty","abc123","letmein","welcome","monkey","football"]
    try:
        with open(nom_fichier, 'r') as f:
            mots = [l.strip() for l in f if l.strip()]
        return mots if mots else default
    except: # En cas d'erreur, retourne la liste par défaut
        return default

def main():
    mot_secret = random.choice(charger_mots())
    print("Bienvenue au jeu 'CrackMe de Farès IRMAL' ! Devinez le mot de passe.")

    try: max_essais = int(input("Max essais (0=illimité)? "))
    except ValueError: max_essais = 0
    if max_essais < 0: max_essais = 0 # Assure que max_essais n'est pas négatif

    tentatives, trouve, triche_activee = 0, False, False
    historique = []

    while not trouve and (max_essais == 0 or tentatives < max_essais):
        tentatives += 1
        # Affichage du nombre de tentatives
        prompt_input = f"\nTentative {tentatives}"
        if max_essais > 0: prompt_input += f"/{max_essais}"
        proposition = input(prompt_input + ": ")
        historique.append(proposition)

        # Mise en place de l'option triche
        if proposition.lower() == "triche":
            print(f"TRICHE: Mot secret = '{mot_secret}'.")
            triche_activee = True
            break

        if proposition == mot_secret:
            trouve = True
        else:
            print("Incorrect.")
            # Indices
            len_p, len_s = len(proposition), len(mot_secret)
            print(f"Indice Longueur: {'Plus long.' if len_p < len_s else 'Plus court.' if len_p > len_s else 'Même.'}")
            
            if not proposition: print("Indice 1ère lettre: Proposition vide.")
            else: print(f"Indice 1ère lettre: {'Même.' if proposition[0] == mot_secret[0] else 'Différente.'}")
            
            print(f"Indice Communs: {len(set(proposition) & set(mot_secret))} caractère(s).")

    # Messages de fin de jeu
    print("\n--- Fin ---")
    final_msg = ""
    if trouve: final_msg = f"Bravo! Mot '{mot_secret}' trouvé en {tentatives} essais."
    elif triche_activee: final_msg = f"Triche utilisée. Le mot était '{mot_secret}'."
    else: # Perdu (limite d'essais atteinte)
        final_msg = f"Perdu! Le mot était '{mot_secret}'."
        if max_essais > 0 and tentatives >= max_essais: final_msg += f" (Limite de {max_essais} essais atteinte)"
    print(final_msg)

    if historique: print("Vos essais:", ", ".join(historique))

if __name__ == "__main__":
    main()
