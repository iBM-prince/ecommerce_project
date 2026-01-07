import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
from performances import measure_query_time

# ==========================
# CONFIGURATION BASE DE DONNÉES
# ==========================
DB_CONFIG = {
    "host": "localhost",
    "user": "admin_bd",      # changer si besoin
    "password": "admin123",
    "database": "e_commerce_db"
}

# ==========================
# CONNEXION MYSQL
# ==========================
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ==========================
# INTERFACE STREAMLIT
# ==========================
st.title("📊 Analyse des performances – Base de données E-commerce")

st.write(
    """
    Cette application permet d'analyser le temps d'exécution des requêtes SQL
    sur une base de données e-commerce MySQL.
    """
)

# ==========================
# CONNEXION
# ==========================
try:
    conn = get_connection()
    cursor = conn.cursor()
    st.success("Connexion à la base de données réussie ✅")
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

# ==========================
# INFORMATIONS GÉNÉRALES
# ==========================
st.subheader("📦 Informations sur la base de données")

cursor.execute("SELECT COUNT(*) FROM produits")
nb_produits = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM utilisateurs")
nb_utilisateurs = cursor.fetchone()[0]

st.write(f"Nombre de produits : **{nb_produits}**")
st.write(f"Nombre d'utilisateurs : **{nb_utilisateurs}**")

# ==========================
# TEST DE PERFORMANCE
# ==========================
st.subheader("⏱️ Test de performance des requêtes")

query = """
SELECT * FROM produits
WHERE nom_prod = 'Produit_500'
"""

st.code(query, language="sql")

if st.button("Tester la requête"):
    time_exec = measure_query_time(cursor, query)
    st.write(f"Temps d'exécution : **{time_exec:.6f} secondes**")

# ==========================
# CRÉATION DE L'INDEX
# ==========================
st.subheader("⚡ Optimisation avec index")

if st.button("Créer un index sur nom_prod"):
    try:
        cursor.execute("CREATE INDEX idx_nom_prod ON produits(nom_prod)")
        conn.commit()
        st.success("Index créé avec succès ✅")
    except mysql.connector.Error as err:
        st.warning(f"Index déjà existant ou erreur : {err}")

# ==========================
# ANALYSE AVANT / APRÈS INDEX
# ==========================
st.subheader("📈 Analyse avant / après index")

sizes = [1000, 5000, 10000]
times = []

for size in sizes:
    test_query = f"""
    SELECT * FROM produits
    WHERE id_prod <= {size}
    """
    exec_time = measure_query_time(cursor, test_query)
    times.append(exec_time)

# ==========================
# COURBE DE PERFORMANCE
# ==========================
st.subheader("📊 Courbe de performance")

fig, ax = plt.subplots()
ax.plot(sizes, times, marker='o')
ax.set_xlabel("Nombre de lignes")
ax.set_ylabel("Temps d'exécution (secondes)")
ax.set_title("Temps d'exécution en fonction du volume de données")

st.pyplot(fig)

# ==========================
# CONCLUSION
# ==========================
st.subheader("📝 Conclusion")

st.write(
    """
    L'analyse montre que le temps d'exécution des requêtes augmente avec
    le nombre de lignes dans la table.  
    L'utilisation d'index permet d'améliorer considérablement les performances
    des requêtes de recherche dans une base de données e-commerce.
    """
)

# ==========================
# FERMETURE CONNEXION
# ==========================
cursor.close()
conn.close()
