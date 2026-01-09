import csv
import random
from datetime import datetime, timedelta


# DECLARATION DU NOMBRES DE LIGNES A GENERER

NB_LIGNES = 10000


# DECLARATION DES LISTES DE DONNEES

noms = [
    'Diop','Ndiaye',
    'Fall','Ba','Sow',
    'Gueye','Faye','Sy',
    'Kane','Diallo','Sarr'
]

prenoms_hommes = [
    'Mamadou','Ibrahima','Cheikh',
    'Ousmane','Abdoulaye','Moussa','Oumar'
]

prenoms_femmes = [
    'Awa','Fatou','Aminata','Khady','Mariama'
]


prenoms = prenoms_hommes + prenoms_femmes

roles = [
    'admin',
    'medecin',
    'agent'
]

specialites = [
    'Medecine generale',
    'Cardiologie',
    'Pediatrie',
    'Gynecologie',
    'Chirurgie',
    'Dermatologie'
]

traitements = [
    'Traitement antipaludique',
    'Traitement antibiotique',
    'Suivi hypertension',
    'Soins post-operatoires',
    'Traitement diabetique',
    'Consultation generale'
]

prefix_tel = [
    '77',
    '78',
    '70',
    '76'
]

# FONCTION DE GENERATION D'UNE DATE ALEATOIRE

def random_date(date_debut=1950,date_fin=2024):
    debut=datetime(date_debut,1,1)
    fin=datetime(date_fin,12,31)
    delta=fin - debut
    return debut + timedelta(days=random.randint(0, delta.days))


# FICHIER CSV UTILISATEURS

with open('utilisateurs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nom','prenom','email','mot_de_passe','role'])

    for i in range(1, NB_LIGNES + 1):
        writer.writerow([
            random.choice(noms),
            random.choice(prenoms),
            f'user{i}@hopital.sn',
            'password123',
            random.choice(roles)
        ])

print("Fichier utilisateurs.csv genere avec succes.")


# FICHIER CSV PATIENTS

with open('patients.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nom_pat','prenom_pat','date_naissance','sexe','telephone'])

    for _ in range(NB_LIGNES):
        tel = random.choice(prefix_tel) + f"{random.randint(0,9999999):07d}"
        
        sexe = random.choice(['m', 'f'])
        if sexe == 'm':
            prenom = random.choice(prenoms_hommes)
        else:
            prenom = random.choice(prenoms_femmes)

        writer.writerow([
            random.choice(noms),
            prenom,
            random_date(1940, 2023).strftime('%Y-%m-%d'),
            sexe,
            tel
        ])

print("Fichier patients.csv genere avec succes.")


#FICHIER CSV MEDECINS

# Les médecins sont des utilisateurs avec role='medecin'
# On prend les 3000 premiers utilisateurs (qui vont être les médecins)
medecin_ids = list(range(1, 3001))

with open('medecins.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nom_med','prenom_med','specialite','id_user'])

    for uid in medecin_ids:
        writer.writerow([
            random.choice(noms),
            random.choice(prenoms),
            random.choice(specialites),
            uid
        ])

print("Fichier medecins.csv genere avec succes.")


# FICHIER CSV RENDEZ-VOUS

with open('rendez_vous.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['date_rdv','id_pat','id_med'])

    for _ in range(NB_LIGNES):
        writer.writerow([
            random_date(2024, 2026).strftime('%Y-%m-%d'),
            random.randint(1, NB_LIGNES),
            random.randint(1, 3000)  # Les IDs des médecins vont de 1 à 3000
        ])

print("Fichier rendez_vous.csv genere avec succes.")


# FICHIER CSV HOSPITALISATIONS

with open('hospitalisations.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['date_entree','date_sortie','id_pat'])

    for _ in range(NB_LIGNES):
        entree = random_date(2022, 2025)
        sortie = entree + timedelta(days=random.randint(1, 30))
        writer.writerow([
            entree.strftime('%Y-%m-%d'),
            sortie.strftime('%Y-%m-%d'),
            random.randint(1, NB_LIGNES)
        ])

print("Fichier hospitalisations.csv genere avec succes.")

# FICHIER CSV TRAITEMENTS

with open('traitements.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['description','date_traitement','id_pat'])

    for _ in range(NB_LIGNES):
        writer.writerow([
            random.choice(traitements),
            random_date(2023, 2025).strftime('%Y-%m-%d'),
            random.randint(1, NB_LIGNES)
        ])

print("Fichier traitements.csv genere avec succes.")

print("Tous les fichiers CSV ont été générés avec succès")

