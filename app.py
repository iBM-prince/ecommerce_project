import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from performances import execute_query

st.set_page_config(page_title="Gestion Hôpital", layout="wide")

st.title("🏥 Gestion d’un hôpital – Projet Base de Données")

# ======================
# Connexion MySQL
# ======================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # ⚠️ mets ton mot de passe MySQL
        database="hopital_db"
    )

# ======================
# Menu
# ======================
menu = st.sidebar.selectbox(
    "Menu",
    ["Patients", "Médecins", "Rendez-vous", "Hospitalisations", "Traitements", "Tests de performances"]
)

# ======================
# PATIENTS
# ======================
if menu == "Patients":
    st.header("👤 Liste des patients")

    query = "SELECT * FROM patients"
    st.code(query, language="sql")
    df, t = execute_query(query)

    st.dataframe(df)
    st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# MEDECINS
# ======================
elif menu == "Médecins":
    st.header("👨‍⚕️ Liste des médecins")

    query = "SELECT id_med, nom_med, prenom_med, specialite FROM medecins"
    st.code(query, language="sql")
    df, t = execute_query(query)

    st.dataframe(df)
    st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# RENDEZ-VOUS
# ======================
elif menu == "Rendez-vous":
    st.header("📅 Rendez-vous")

    query = """
    SELECT r.id_rdv, p.nom_pat, p.prenom_pat,
           m.nom_med, m.prenom_med, r.date_rdv
    FROM rendez_vous r
    JOIN patients p ON r.id_pat = p.id_pat
    JOIN medecins m ON r.id_med = m.id_med
    """
    st.code(query, language="sql")

    df, t = execute_query(query)

    st.dataframe(df)
    st.success(f"Temps d'exécution : {t:.6f} secondes")

# ======================
# HOSPITALISATIONS
# ======================
elif menu == "Hospitalisations":
    st.header("🏥 Hospitalisations")
    query = "SELECT * FROM hospitalisations"
    st.code(query, language="sql")
    df, t = execute_query(query)
    st.dataframe(df)
    st.success(f"Temps d'exécution : {t:.6f} secondes")



# ======================
# TRAITEMENTS
# ====================    

elif menu == "Traitements":
    st.header("💊 Traitements")
    query = "SELECT * FROM traitements"
    st.code(query, language="sql")
    df, t = execute_query(query)
    st.dataframe(df)
    st.success(f"Temps d'exécution : {t:.6f} secondes")


# PERFORMANCE
# ======================
elif menu == "Tests de performances":
    st.header("📊 Analyse des performances SQL")

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
