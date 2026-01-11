import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from performances import execute_query
from PIL import Image

# ======================
# CONFIGURATION (OBLIGATOIRE EN PREMIER)
# ======================
favicon = Image.open("logo_esitec.bmp")
st.set_page_config(
    page_title="Gestion Hôpital",
    page_icon=favicon,
    layout="wide"
)

# ======================
# LOGOS + TITRE
# ======================
logo_gauche = Image.open("logo_esitec.bmp")
logo_droite = Image.open("logo-supdeco.png")

col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    st.image(logo_gauche, width=150)

with col3:
    st.image(logo_droite, width=150)

st.title("🏥 Gestion d’un hôpital – Projet Base de Données")

# ======================
# UTILISATEURS ET RÔLES
# ======================
users = {
    "admin": {"password": "admin221", "role": "admin"},
    "medecin": {"password": "medecin221", "role": "medecin"},
    "agent": {"password": "agent221", "role": "agent"}
}

# ======================
# CONNEXION UTILISATEUR
# ======================
st.sidebar.header("🔑 Connexion")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if username in users and users[username]["password"] == password:
    st.sidebar.success(f"Connecté en tant que {username}")
    role = users[username]["role"]
else:
    st.sidebar.warning("Nom d'utilisateur ou mot de passe incorrect")
    st.stop()

# ======================
# MENU
# ======================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Patients",
        "Médecins",
        "Rendez-vous",
        "Hospitalisations",
        "Traitements",
        "Tests de performances"
    ]
)

# ======================
# FONCTION DROITS
# ======================
def check_rights(required_roles):
    return role in required_roles

# ======================
# PATIENTS
# ======================
if menu == "Patients":
    st.header("👤 Gestion des patients")

    def afficher_patients():
        query = "SELECT * FROM patients"
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

    afficher_patients()

    if role in ["admin", "medecin"]:
        st.subheader("➕ Ajouter un patient")
        with st.form("add_patient"):
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            date_naissance = st.date_input("Date de naissance")
            sexe = st.selectbox("Sexe", ["m", "f"])
            telephone = st.number_input("Téléphone", min_value=100000000, max_value=9999999999, step=1)
            submit_add = st.form_submit_button("Ajouter")

            if submit_add:
                query = f"""
                INSERT INTO patients (nom_pat, prenom_pat, date_naissance, sexe, telephone)
                VALUES ('{nom}', '{prenom}', '{date_naissance}', '{sexe}', {telephone})
                """
                _, t = execute_query(query)
                st.success(f"Patient ajouté en {t:.6f} secondes")
                afficher_patients()

    if role == "admin":
        st.subheader("✏️ Modifier un patient")
        with st.form("update_patient"):
            patient_id = st.number_input("ID du patient", min_value=1)
            new_nom = st.text_input("Nouveau nom")
            new_prenom = st.text_input("Nouveau prénom")
            new_date = st.date_input("Nouvelle date de naissance")
            new_sexe = st.selectbox("Nouveau sexe", ["m", "f"])
            new_tel = st.number_input("Nouveau téléphone", min_value=100000000, max_value=9999999999, step=1)
            update_submit = st.form_submit_button("Mettre à jour")

            if update_submit:
                query = f"""
                UPDATE patients
                SET nom_pat='{new_nom}',
                    prenom_pat='{new_prenom}',
                    date_naissance='{new_date}',
                    sexe='{new_sexe}',
                    telephone={new_tel}
                WHERE id_pat={patient_id}
                """
                _, t = execute_query(query)
                st.success(f"Patient modifié en {t:.6f} secondes")
                afficher_patients()

        st.subheader("❌ Supprimer un patient")
        with st.form("delete_patient"):
            delete_id = st.number_input("ID à supprimer", min_value=1)
            delete_submit = st.form_submit_button("Supprimer")

            if delete_submit:
                query = f"DELETE FROM patients WHERE id_pat={delete_id}"
                _, t = execute_query(query)
                st.success(f"Patient supprimé en {t:.6f} secondes")
                afficher_patients()

# ======================
# MÉDECINS
# ======================
elif menu == "Médecins":
    st.header("👨‍⚕️ Gestion des médecins")

    if check_rights(["admin", "medecin"]):
        df, t = execute_query(
            "SELECT id_med, nom_med, prenom_med, specialite FROM medecins"
        )
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

    if role == "admin":
        st.subheader("➕ Ajouter un médecin")
        with st.form("add_medecin"):
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            specialite = st.text_input("Spécialité")
            submit = st.form_submit_button("Ajouter")

            if submit:
                query = f"""
                INSERT INTO medecins (nom_med, prenom_med, specialite)
                VALUES ('{nom}', '{prenom}', '{specialite}')
                """
                _, t = execute_query(query)
                st.success(f"Médecin ajouté en {t:.6f} secondes")

# ======================
# RENDEZ-VOUS
# ======================
elif menu == "Rendez-vous":
    st.header("📅 Rendez-vous")

    if check_rights(["admin", "medecin"]):
        query = """
        SELECT r.id_rdv, p.nom_pat, p.prenom_pat,
               m.nom_med, m.prenom_med, r.date_rdv
        FROM rendez_vous r
        JOIN patients p ON r.id_pat = p.id_pat
        JOIN medecins m ON r.id_med = m.id_med
        """
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# HOSPITALISATIONS
# ======================
elif menu == "Hospitalisations":
    st.header("🏥 Hospitalisations")

    if check_rights(["admin", "medecin"]):
        df, t = execute_query("SELECT * FROM hospitalisations")
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# TRAITEMENTS
# ======================
elif menu == "Traitements":
    st.header("💊 Traitements")

    if check_rights(["admin", "medecin"]):
        df, t = execute_query("SELECT * FROM traitements")
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# TESTS DE PERFORMANCES
# ======================
elif menu == "Tests de performances":
    st.header("📊 Analyse des performances SQL")

    if check_rights(["admin", "medecin"]):
        queries = {
            "Patients": "SELECT * FROM patients",
            "Patients (index)": "SELECT * FROM patients WHERE nom_pat LIKE 'A%'",
            "Rendez-vous": "SELECT * FROM rendez_vous WHERE date_rdv >= '2024-01-01'",
            "Jointure": """
                SELECT r.id_rdv, p.nom_pat, m.nom_med
                FROM rendez_vous r
                JOIN patients p ON r.id_pat = p.id_pat
                JOIN medecins m ON r.id_med = m.id_med
            """
        }

        results = []
        for name, q in queries.items():
            _, t = execute_query(q)
            results.append({"Requête": name, "Temps (s)": t})

        df_perf = pd.DataFrame(results)
        st.dataframe(df_perf)

        fig, ax = plt.subplots()
        ax.plot(df_perf["Requête"], df_perf["Temps (s)"], marker="o")
        ax.set_xlabel("Requêtes")
        ax.set_ylabel("Temps (secondes)")
        ax.set_title("Performance des requêtes SQL")
        plt.xticks(rotation=30)
        st.pyplot(fig)
