import string 

def verifier_mot_de_passe_cnil():
    # Demande à l'utilisateur de saisir un mot de passe.
    while True:
        mot_de_passe = input("Veuillez saisir un mot de passe : ")
        erreurs = []

        # Longueur (12 à 14 caractères)
        if not 12 <= len(mot_de_passe) <= 14:
            erreurs.append("Le mot de passe doit contenir entre 12 et 14 caractères.")

        # Au moins une lettre majuscule
        if not any(char in string.ascii_uppercase for char in mot_de_passe):
            erreurs.append("Le mot de passe doit contenir au moins une lettre majuscule.")

        # Au moins une lettre minuscule
        if not any(char in string.ascii_lowercase for char in mot_de_passe):
            erreurs.append("Le mot de passe doit contenir au moins une lettre minuscule.")

        # Au moins un chiffre
        if not any(char in string.digits for char in mot_de_passe):
            erreurs.append("Le mot de passe doit contenir au moins un chiffre.")

        # Au moins un caractère spécial
        caracteres_speciaux_a_verifier = "!@#$%^&*(),.?\":{}|<>" # Liste exemple de la CNIL

        if not any(char in caracteres_speciaux_a_verifier for char in mot_de_passe):
            erreurs.append(f"Le mot de passe doit contenir au moins un caractère spécial (ex: {caracteres_speciaux_a_verifier}).")

        # 6. Éviter les caractères ambigus (inchangé)
        caracteres_ambigus = ['l', '1', 'i', 'I', '0', 'O']
        for char_ambigu in caracteres_ambigus:
            if char_ambigu in mot_de_passe:
                erreurs.append(f"Il est recommandé d'éviter les caractères ambigus comme '{char_ambigu}'.")
                break

        if not erreurs:
            print("\nVotre mot de passe respecte les recommandations de la CNIL.")
            break
        else:
            print("\nVotre mot de passe ne respecte pas toutes les recommandations, veuillez réessayer :")
            for erreur in erreurs:
                print(f"- {erreur}")
            print()

if __name__ == "__main__":
    verifier_mot_de_passe_cnil()
