import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from performances import execute_query

st.set_page_config(page_title="Gestion Hôpital", layout="wide")
st.title("🏥 Gestion d’un hôpital – Projet Base de Données")

# ======================
# Utilisateurs et rôles
# ======================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "medecin": {"password": "med123", "role": "medecin"},
    "agent": {"password": "agent123", "role": "agent"}
}

# ======================
# Connexion utilisateur
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
# Menu
# ======================
menu = st.sidebar.selectbox(
    "Menu",
    ["Patients", "Médecins", "Rendez-vous", "Hospitalisations", "Traitements", "Tests de performances"]
)

# ======================
# Vérifier droits
# ======================
def check_rights(required_roles):
    return role in required_roles

# ======================
# PATIENTS
# ======================
if menu == "Patients":
    st.header("👤 Gestion des patients")

    # Fonction pour afficher les patients
    def afficher_patients():
        query = "SELECT * FROM patients"
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")
    
    afficher_patients()

    # Ajouter un patient (Admin + Médecin)
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
                insert_query = f"""
                INSERT INTO patients (nom_pat, prenom_pat, date_naissance, sexe, telephone)
                VALUES ('{nom}', '{prenom}', '{date_naissance}', '{sexe}', {telephone})
                """
                _, t = execute_query(insert_query)
                st.success(f"Patient ajouté en {t:.6f} secondes")
                afficher_patients()  # Rafraîchir la table

    # Modifier un patient (Admin)
    if role == "admin":
        st.subheader("✏️ Modifier un patient")
        with st.form("update_patient"):
            patient_id = st.number_input("ID du patient à modifier", min_value=1)
            new_nom = st.text_input("Nouveau nom")
            new_prenom = st.text_input("Nouveau prénom")
            new_date = st.date_input("Nouvelle date de naissance")
            new_sexe = st.selectbox("Nouveau sexe", ["m", "f"])
            new_tel = st.number_input("Nouveau téléphone", min_value=100000000, max_value=9999999999, step=1)
            update_submit = st.form_submit_button("Mettre à jour")
            if update_submit:
                update_query = f"""
                UPDATE patients
                SET nom_pat='{new_nom}', prenom_pat='{new_prenom}', date_naissance='{new_date}', sexe='{new_sexe}', telephone={new_tel}
                WHERE id_pat={patient_id}
                """
                _, t = execute_query(update_query)
                st.success(f"Patient mis à jour en {t:.6f} secondes")
                afficher_patients()  # Rafraîchir la table

        # Supprimer un patient (Admin)
        st.subheader("❌ Supprimer un patient")
        with st.form("delete_patient"):
            delete_id = st.number_input("ID du patient à supprimer", min_value=1)
            delete_submit = st.form_submit_button("Supprimer")
            if delete_submit:
                delete_query = f"DELETE FROM patients WHERE id_pat={delete_id}"
                _, t = execute_query(delete_query)
                st.success(f"Patient supprimé en {t:.6f} secondes")
                afficher_patients()  # Rafraîchir la table

# ======================
# MEDECINS
# ======================
elif menu == "Médecins":
    st.header("👨‍⚕️ Gestion des médecins")

    if check_rights(["admin", "medecin"]):
        query = "SELECT id_med, nom_med, prenom_med, specialite FROM medecins"
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

    if role == "admin":
        st.subheader("➕ Ajouter un médecin")
        with st.form("add_medecin"):
            nom = st.text_input("Nom du médecin")
            prenom = st.text_input("Prénom")
            specialite = st.text_input("Spécialité")
            submit = st.form_submit_button("Ajouter")
            if submit:
                insert_query = f"""
                INSERT INTO medecins (nom_med, prenom_med, specialite)
                VALUES ('{nom}', '{prenom}', '{specialite}')
                """
                _, t = execute_query(insert_query)
                st.success(f"Médecin ajouté en {t:.6f} secondes")
                # Recharger la liste
                df, t = execute_query("SELECT id_med, nom_med, prenom_med, specialite FROM medecins")
                st.dataframe(df)

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
        query = "SELECT * FROM hospitalisations"
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# TRAITEMENTS
# ======================
elif menu == "Traitements":
    st.header("💊 Traitements")

    if check_rights(["admin", "medecin"]):
        query = "SELECT * FROM traitements"
        df, t = execute_query(query)
        st.dataframe(df)
        st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# TESTS DE PERFORMANCES
# ======================
elif menu == "Tests de performances":
    st.header("📊 Analyse des performances SQL")

    if check_rights(["admin", "medecin"]):
        queries = {
            "Patients (sans condition)": "SELECT * FROM patients",
            "Patients par nom": "SELECT * FROM patients WHERE nom_pat LIKE 'A%'",
            "Rendez-vous par date": "SELECT * FROM rendez_vous WHERE date_rdv >= '2024-01-01'",
            "Jointure RDV / Patients / Médecins": """
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

        st.subheader("📈 Courbe des temps d'exécution")
        fig, ax = plt.subplots()
        ax.plot(df_perf["Requête"], df_perf["Temps (s)"], marker="o")
        ax.set_ylabel("Temps (secondes)")
        ax.set_xlabel("Requêtes")
        ax.set_title("Performance des requêtes SQL")
        plt.xticks(rotation=30)
        st.pyplot(fig)
